import json
import os

import requests

JIUMA_API_KEY_SAVE_DIR = f"{os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))}/.jiuma"
os.makedirs(JIUMA_API_KEY_SAVE_DIR, exist_ok=True)
JIUMA_API_KEY_SAVE_PATH = f"{JIUMA_API_KEY_SAVE_DIR}/jiuma_api_key"
JIUMA_RAND_STR_SAVE_PATH = f"{JIUMA_API_KEY_SAVE_DIR}/jiuma_rand_str"


def output_result(json_data):
    """输出JSON格式结果"""
    print(json.dumps(json_data, ensure_ascii=False, indent=2))


def jiuma_request(url, data={}):
    try:
        response = requests.post(url, data, timeout=30)
        if response.status_code != 200:
            output_result({
                "status": "error",
                "message": f"请求远程API失败，状态码: {response.status_code}",
                "data": {}
            })
            return None
        json_result = response.json()
        if json_result.get("code") != 200:
            output_result({
                "status": "error",
                "message": f"API返回错误: {json_result.get('message', '未知错误')}",
                "data": json_result
            })
            return
        print(json_result)
        return json_result.get("data")
    except requests.exceptions.Timeout:
        output_result({
            "status": "error",
            "message": "请求超时，请检查网络连接",
            "data": {}
        })
        return None
    except requests.exceptions.RequestException as e:
        output_result({
            "status": "error",
            "message": f"请求异常: {str(e)}",
            "data": {}
        })
        return None
    except json.JSONDecodeError as e:
        output_result({
            "status": "error",
            "message": f"API返回格式错误: {str(e)}",
            "data": {}
        })
        return None
    except Exception as e:
        output_result({
            "status": "error",
            "message": f"未知错误: {str(e)}",
            "data": {}
        })
        return None


def save_jiuma_api_key(api_key):
    with open(JIUMA_API_KEY_SAVE_PATH, "w") as f:
        f.write(api_key)


def save_jiuma_rand_str(rand_str):
    with open(JIUMA_RAND_STR_SAVE_PATH, "w") as f:
        f.write(rand_str)


def get_jiuma_api_key():
    api_key = ""
    try:
        with open(JIUMA_API_KEY_SAVE_PATH, "r") as f:
            api_key = f.read()
    except Exception as e:
        print("get api key failed")
    return api_key


def get_jiuma_rand_str():
    rand_str = ""
    try:
        with open(JIUMA_RAND_STR_SAVE_PATH, "r") as f:
            rand_str = f.read()
    except Exception as e:
        print("get rand str failed")
    return rand_str
