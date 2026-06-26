import argparse
import os

from utils import jiuma_request, output_result, save_jiuma_api_key,save_jiuma_rand_str, get_jiuma_rand_str, \
    JIUMA_RAND_STR_SAVE_PATH

LOGIN_API = "https://api.jiuma.com/user/getLoginQrcode"
CHECK_API = "https://api.jiuma.com/user/checkLoginStatus"


def login_prepare():
    if os.path.exists(JIUMA_RAND_STR_SAVE_PATH):
        rand_str = get_jiuma_rand_str()
    else:
        rand_str = ''
    request_data = {"rand_string": rand_str}
    data = jiuma_request(LOGIN_API, request_data)
    if not data:
        return

    if os.path.exists(JIUMA_RAND_STR_SAVE_PATH):
        if get_jiuma_rand_str() != data["rand_string"]:
            save_jiuma_rand_str(data["rand_string"])
    else:
        save_jiuma_rand_str(data["rand_string"])

    output_result({
        "status": "success",
        "message": "获取登录通行证成功",
        "data": {
            "login_qrcode": data["login_code_url"],
            "login_url": data["login_url"],
            "access_token": data["rand_string"]
        }
    })
    return {
        "status": "success",
        "message": "获取登录通行证成功",
        "data": {
            "login_qrcode": data["login_code_url"],
            "login_url": data["login_url"],
            "access_token": data["rand_string"]
        }
    }


def check_login_status(access_token):
    data = jiuma_request(f"{CHECK_API}?rand_string={access_token}")
    if not data:
        return
    save_jiuma_api_key(data["secret_key"])
    output_result({
        "status": "success",
        "message": "登录成功，已保存api_key",
        "data": {}
    })


def main():
    parser = argparse.ArgumentParser(description="九马AI登录注册入口",
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--login', action='store_true', help="获取登录渠道和access_token")
    parser.add_argument('--check', action='store_true', help="检测是否完整注册/登录，并获取API_KEY")
    parser.add_argument('--access_token', type=str, default='', help="获取API_KEY的通行证")
    args = parser.parse_args()
    if args.login:
        login_prepare()
    else:
        check_login_status(args.access_token)


if __name__ == '__main__':
    main()
