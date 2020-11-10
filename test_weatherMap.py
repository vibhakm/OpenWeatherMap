import json
from datetime import datetime

import jsonpath as jp
import requests


def test_get_no_of_days():
    response = requests.get(
        "https://samples.openweathermap.org/data/2.5/forecast/hourly?q=London,us;appid=b6907d289e10d714a6e88b30761fae22")

    json_text = json.loads(response.text)

    result_list_first = jp.jsonpath(json_text, 'list[0].dt_txt')  # To get the first value from the list
    start_date = result_list_first[0]

    list_length = len(json_text['list']);
    result_list_last = jp.jsonpath(json_text, f"list[{list_length - 1}].dt_txt")  # To get the last value from the list
    end_date = result_list_last[0]

    date1 = datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')  # converting string to datetime format
    date2 = datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

    number_of_days = date2 - date1
    string_days = str(number_of_days)  # converting timedelta to string

    assert string_days == "3 days, 23:00:00"


def test_is_forecast_in_hourly_interval():
    response = requests.get(
        "https://samples.openweathermap.org/data/2.5/forecast/hourly?q=London,us;appid=b6907d289e10d714a6e88b30761fae22")
    json_text = json.loads(response.text)
    count = 1
    for i in range(len(json_text['list']) - 1):
        dt1 = jp.jsonpath(json_text, f"list[{i}].dt_txt")    # To get the first date
        dt2 = jp.jsonpath(json_text, f"list[{i + 1}].dt_txt")  # To get the next date
        date1 = datetime.strptime(dt1[0], '%Y-%m-%d %H:%M:%S')
        date2 = datetime.strptime(dt2[0], '%Y-%m-%d %H:%M:%S')
        difference = date2 - date1

        assert str(difference) == "1:00:00"

        count = count + 1
    print(count)

    assert count == 96


def test_check_temp():
    response = requests.get(
        "https://samples.openweathermap.org/data/2.5/forecast/hourly?q=London,us;appid=b6907d289e10d714a6e88b30761fae22")
    json_text = json.loads(response.text)
    for i in range(len(json_text['list'])):
        main = jp.jsonpath(json_text, f"list[{i}].main")
        list_vals_main = main[0]
        temp = list_vals_main["temp"]
        temp_min = list_vals_main["temp_min"]
        temp_max = list_vals_main["temp_max"]

        assert temp_min <= temp <= temp_max


def test_check_description_for_id_500():
    response = requests.get(
        "https://samples.openweathermap.org/data/2.5/forecast/hourly?q=London,us;appid=b6907d289e10d714a6e88b30761fae22")
    json_text = json.loads(response.text)
    for i in range(len(json_text['list'])):
        weather = jp.jsonpath(json_text, f"list[{i}].weather[0]")
        list_vals_weather = weather[0]
        if (list_vals_weather["id"]) == 500:
            assert list_vals_weather["description"] == "light rain"


def test_check_description_for_id_800():
    response = requests.get(
        "https://samples.openweathermap.org/data/2.5/forecast/hourly?q=London,us;appid=b6907d289e10d714a6e88b30761fae22")
    json_text = json.loads(response.text)
    for i in range(len(json_text['list'])):
        weather = jp.jsonpath(json_text, f"list[{i}].weather[0]")
        list_vals_weather = weather[0]
        if (list_vals_weather["id"]) == 800:
            assert list_vals_weather["description"] == "clear sky"
