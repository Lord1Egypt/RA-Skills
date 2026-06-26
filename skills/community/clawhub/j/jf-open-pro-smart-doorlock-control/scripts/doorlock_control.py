#!/usr/bin/env python3
"""
杰峰智能门锁设备控制技能（开发版）

支持功能：
- 查询设备是否支持开锁
- 登录设备
- 获取设备接口访问令牌
- 远程一键开锁
"""

import os
import sys
import json
import argparse
import requests
from typing import Optional, Dict, Any, List

# 导入加密工具（复用）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from crypto import get_time_millis, generate_signature
except ImportError:
    print("[错误] 错误：找不到 crypto.py 模块")
    print("   请确保 scripts/crypto.py 存在")
    sys.exit(1)

# API 基础地址（可通过环境变量切换）
JF_ENDPOINT = os.getenv("JF_ENDPOINT", "api-cn.jftechws.com")
JF_BASE_URL = f"https://{JF_ENDPOINT}/gwp/v3"


def get_headers(uuid: str, app_key: str, app_secret: str, move_card: int) -> Dict[str, str]:
    """生成请求头（包含签名和时间戳）"""
    time_millis = get_time_millis()
    signature = generate_signature(uuid, app_key, app_secret, time_millis, move_card)

    return {
        "Content-Type": "application/json; charset=UTF-8",
        "uuid": uuid,
        "appKey": app_key,
        "timeMillis": time_millis,
        "signature": signature,
        "X-Request-Id": os.urandom(16).hex()
    }


def get_device_token(uuid: str, app_key: str, app_secret: str,
                     move_card: int, sns: List[str],
                     endpoint: str = "api-cn.jftechws.com",
                     access_token: str = "") -> List[Dict[str, str]]:
    """
    获取设备接口访问令牌（通用函数）

    API: POST /gwp/v3/rtc/device/token
    """
    base_url = f"https://{endpoint}/gwp/v3"
    url = f"{base_url}/rtc/device/token"
    headers = get_headers(uuid, app_key, app_secret, move_card)

    body = {"sns": sns}
    if access_token:
        body["accessToken"] = access_token

    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()

    if result.get("code") != 2000:
        raise RuntimeError(f"获取设备 Token 失败：{result.get('msg', '未知错误')}")

    data = result.get("data", [])
    if not data:
        raise RuntimeError("设备不属于当前用户，或设备未绑定")

    return data


def check_doorlock_support(device_token: str, uuid: str, app_key: str,
                            app_secret: str, move_card: int) -> Dict[str, Any]:
    """
    查询设备是否支持门锁功能

    API: POST /gwp/v3/rtc/device/getability/{deviceToken}
    Name: DoorFunction
    """
    url = f"{JF_BASE_URL}/rtc/device/getability/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)

    body = {"Name": "DoorFunction"}

    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()

    if result.get("code") != 2000:
        raise RuntimeError(f"查询设备能力失败：{result.get('msg', '未知错误')}")

    return result.get("data", {})


def get_door_config(device_token: str, uuid: str, app_key: str,
                     app_secret: str, move_card: int) -> Dict[str, Any]:
    """
    获取门锁配置

    API: POST /gwp/v3/rtc/device/doorLockTransparent/{deviceToken}
    """
    url = f"{JF_BASE_URL}/rtc/device/doorLockTransparent/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)

    body = {
        "Name": "OPDoorLockProCmd",
        "OPDoorLockProCmd": {
            "Cmd": "GetDoorConfig"
        }
    }

    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()

    if result.get("code") != 2000:
        raise RuntimeError(f"获取门锁配置失败：{result.get('msg', '未知错误')}")

    return result.get("data", {})


def login_device(device_token: str, uuid: str, app_key: str,
                 app_secret: str, move_card: int,
                 device_sn: str, username: str, password: str = "",
                 keepalive_time: int = 0) -> Dict[str, Any]:
    """
    登录设备

    API: POST /gwp/v3/rtc/device/login/{deviceToken}
    """
    url = f"{JF_BASE_URL}/rtc/device/login/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)

    body = {"UserName": username}
    if password:
        body["PassWord"] = password
    if keepalive_time > 0:
        body["KeepaliveTime"] = keepalive_time

    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()

    if result.get("code") != 2000:
        raise RuntimeError(f"设备登录失败：{result.get('msg', '未知错误')}")

    if result.get("data", {}).get("Ret") != 100:
        raise RuntimeError(f"设备返回错误：Ret={result.get('data', {}).get('Ret')}")

    return result.get("data", {})


def unlock_door(device_token: str, uuid: str, app_key: str,
                app_secret: str, move_card: int,
                device_sn: str, password: str = "") -> Dict[str, Any]:
    """
    远程一键开锁

    API: POST /gwp/v3/rtc/device/doorLockRemoteUnlock/{deviceToken}
    """
    url = f"{JF_BASE_URL}/rtc/device/doorLockRemoteUnlock/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)

    body = {"sn": device_sn, "props": {}}

    if password:
        body["props"]["doorLock"] = {
            "remoteUnlock": {
                "password": password
            }
        }
    else:
        body["props"]["doorLock"] = {
            "remoteOneKeyUnlock": 1,
            "userType": 5,
            "memberID": 1
        }

    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()

    if result.get("code") != 2000:
        raise RuntimeError(f"远程开锁失败：{result.get('msg', '未知错误')}")

    if result.get("data", {}).get("Ret") != 100:
        ret_msg = result.get("data", {}).get("retMsg", "")
        raise RuntimeError(f"设备返回错误：Ret={result.get('data', {}).get('Ret')}{f' ({ret_msg})' if ret_msg else ''}")

    return result.get("data", {})


# ============== 动作处理函数 ==============

def get_token_action(args: argparse.Namespace) -> int:
    """执行获取设备 Token 操作"""
    try:
        sns = args.device_sn.split(",") if args.device_sn else []
        if not sns:
            print("[错误] 错误：缺少 --device-sn 或 JF_DEVICE_SN 环境变量", file=sys.stderr)
            return 1

        tokens = get_device_token(
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            sns=sns,
            endpoint=JF_ENDPOINT
        )

        print("[OK] 获取成功")
        for item in tokens:
            print(f"   设备 SN: {item.get('sn')}")
            print(f"   DeviceToken: {item.get('token')}")

        return 0

    except RuntimeError as e:
        print(f"[错误] 错误：{e}", file=sys.stderr)
        return 1


def check_support_action(args: argparse.Namespace) -> int:
    """执行查询设备是否支持开锁操作"""
    try:
        result = check_doorlock_support(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card
        )

        door_func = result.get("DoorFunction", {})
        if not door_func and "DoorAbilityMask" in result:
            door_func = result

        if door_func:
            for key, value in door_func.items():
                print(f"   {key}: {value}")
        else:
            print("[警告] 设备未返回 DoorFunction 能力信息")

        return 0

    except RuntimeError as e:
        print(f"[错误] {e}", file=sys.stderr)
        return 1


def get_config_action(args: argparse.Namespace) -> int:
    """执行获取门锁配置操作"""
    try:
        result = get_door_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card
        )

        config = result.get("DoorConfig", {})
        if config:
            for key, value in config.items():
                print(f"   {key}: {value}")
        else:
            print("[警告] 设备未返回门锁配置信息")

        return 0

    except RuntimeError as e:
        print(f"[错误] {e}", file=sys.stderr)
        return 1


def login_action(args: argparse.Namespace) -> int:
    """执行登录设备操作"""
    try:
        result = login_device(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            device_sn=args.device_sn,
            username=args.username,
            password=args.password,
            keepalive_time=args.keepalive_time
        )

        print("[OK] 登录成功")
        for key, value in result.items():
            print(f"   {key}: {value}")
        return 0

    except RuntimeError as e:
        print(f"[错误] {e}", file=sys.stderr)
        return 1


def unlock_action(args: argparse.Namespace) -> int:
    """执行远程一键开锁操作"""
    try:
        result = unlock_door(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            device_sn=args.device_sn,
            password=args.password
        )

        print("[OK] 开锁指令发送成功")
        for key, value in result.items():
            print(f"   {key}: {value}")
        return 0

    except RuntimeError as e:
        print(f"[错误] {e}", file=sys.stderr)
        return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="杰峰智能门锁设备控制技能")

    # 全局参数
    parser.add_argument("--action", required=True,
                        choices=["get-token", "check-support", "get-config", "login", "unlock"],
                        help="操作类型")
    parser.add_argument("--uuid", default=os.getenv("JF_UUID"),
                        help="开放平台用户 uuid")
    parser.add_argument("--app-key", default=os.getenv("JF_APP_KEY"),
                        help="应用 appKey")
    parser.add_argument("--app-secret", default=os.getenv("JF_APP_SECRET"),
                        help="应用密钥")
    parser.add_argument("--move-card", type=int, default=os.getenv("JF_MOVE_CARD", "2"),
                        help="移动卡标识")
    parser.add_argument("--device-sn", default=os.getenv("JF_DEVICE_SN"),
                        help="设备序列号")
    parser.add_argument("--device-token", default=os.getenv("JF_DEVICE_TOKEN"),
                        help="设备接口访问令牌")
    parser.add_argument("--password", default="",
                        help="锁端密码/设备登录密码（根据操作类型使用）")
    parser.add_argument("--username", default="admin",
                        help="设备登录用户名（默认 admin）")
    parser.add_argument("--keepalive-time", type=int, default=0,
                        help="设备登录保活时长，单位秒（默认 0 表示使用设备默认）")

    args = parser.parse_args()

    # 验证必需参数
    if not args.uuid:
        print("[错误] 错误：缺少 --uuid 或 JF_UUID 环境变量", file=sys.stderr)
        return 1
    if not args.app_key:
        print("[错误] 错误：缺少 --app-key 或 JF_APP_KEY 环境变量", file=sys.stderr)
        return 1
    if not args.app_secret:
        print("[错误] 错误：缺少 --app-secret 或 JF_APP_SECRET 环境变量", file=sys.stderr)
        return 1
    if args.action != "get-token" and not args.device_token:
        print("[错误] 错误：缺少 --device-token 或 JF_DEVICE_TOKEN 环境变量", file=sys.stderr)
        return 1

    # 执行对应操作
    if args.action == "get-token":
        return get_token_action(args)
    elif args.action == "check-support":
        return check_support_action(args)
    elif args.action == "get-config":
        return get_config_action(args)
    elif args.action == "login":
        return login_action(args)
    elif args.action == "unlock":
        return unlock_action(args)
    else:
        print(f"[错误] 未知操作：{args.action}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
