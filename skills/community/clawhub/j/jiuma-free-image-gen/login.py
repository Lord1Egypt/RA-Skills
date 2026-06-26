import argparse

from utils import jiuma_request, output_result, save_jiuma_api_key

LOGIN_API = "https://api.jiuma.com/user/getLoginQrcode"
CHECK_API = "https://api.jiuma.com/user/checkLoginStatus"


def login_prepare():
    data, message = jiuma_request(LOGIN_API)
    if not data:
        return

    output_result({
        "status": "success",
        "message": "获取登录通行证成功",
        "data": {
            "login_qrcode": data["login_code_url"],
            "login_url": data["login_url"],
            "access_token": data["rand_string"]
        }
    })


def check_login_status(access_token):
    data, message = jiuma_request(f"{CHECK_API}?rand_string={access_token}")
    if not data:
        return
    save_jiuma_api_key(data["secret_key"])
    output_result({
        "status": "success",
        "message": "登录成功，已保存api_key，可以继续使用九马AI工具",
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
