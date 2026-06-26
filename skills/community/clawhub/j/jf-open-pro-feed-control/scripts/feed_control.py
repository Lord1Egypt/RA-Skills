#!/usr/bin/env python3
"""
杰峰智能宠物喂食器设备控制技能（开发版）

支持功能：
- 查询设备是否支持喂食
- 一键喂食
- 定时喂食计划查询和设置
- 宠物检测功能开关查询和设置
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

    Args:
        uuid: 开放平台用户 uuid
        app_key: 开放平台应用 appKey
        app_secret: 开放平台应用密钥
        move_card: 移动卡标识
        sns: 设备序列号数组（最多 500 个）
        endpoint: API 接入地址
        access_token: 杰峰 AMS 用户系统 accessToken（可选）

    Returns:
        设备 token 列表，每项包含 sn 和 token
    """
    base_url = f"https://{endpoint}/gwp/v3"
    url = f"{base_url}/rtc/device/token"
    headers = get_headers(uuid, app_key, app_secret, move_card)

    body = {
        "sns": sns
    }
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


def check_feed_support(device_token: str, uuid: str, app_key: str,
                        app_secret: str, move_card: int) -> Dict[str, Any]:
    """
    查询设备是否支持喂食功能（FeederAbility）

    API: POST /gwp/v3/rtc/device/getability/{deviceToken}
    Name: FeederAbility
    """
    url = f"{JF_BASE_URL}/rtc/device/getability/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)

    body = {"Name": "FeederAbility"}

    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()

    if result.get("code") != 2000:
        raise RuntimeError(f"查询设备能力失败：{result.get('msg', '未知错误')}")

    return result.get("data", {})


def feed_once(device_token: str, uuid: str, app_key: str,
              app_secret: str, move_card: int,
              device_sn: str, portion: int = 1) -> Dict[str, Any]:
    """
    一键喂食

    API: POST /gwp/v3/rtc/device/feeder/{deviceToken}
    """
    url = f"{JF_BASE_URL}/rtc/device/feeder/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)

    body = {
        "sn": device_sn,
        "props": {
            "feed": portion
        }
    }

    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()

    if result.get("code") != 2000:
        raise RuntimeError(f"喂食指令发送失败：{result.get('msg', '未知错误')}")

    if result.get("data", {}).get("Ret") != 100:
        raise RuntimeError(f"设备返回错误：{result.get('data', {}).get('Ret')}")

    return result.get("data", {})


def get_feed_schedule(device_token: str, uuid: str, app_key: str,
                       app_secret: str, move_card: int,
                       device_sn: str) -> Dict[str, Any]:
    """
    获取定时喂食计划

    API: POST /gwp/v3/rtc/device/iotPropSet/{deviceToken}
    """
    url = f"{JF_BASE_URL}/rtc/device/iotPropSet/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)

    body = {
        "sn": device_sn,
        "props": ["feedPlan"]
    }

    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()

    if result.get("code") != 2000:
        raise RuntimeError(f"获取定时喂食计划失败：{result.get('msg', '未知错误')}")

    return result.get("data", {})


def set_feed_schedule(device_token: str, uuid: str, app_key: str,
                       app_secret: str, move_card: int,
                       device_sn: str,
                       config: Dict[str, Any],
                       method: str = "") -> Dict[str, Any]:
    """
    设置定时喂食计划

    API: POST /gwp/v3/rtc/device/iotPropSet/{deviceToken}
    """
    url = f"{JF_BASE_URL}/rtc/device/iotPropSet/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)

    body = {
        "sn": device_sn,
        "props": {
            "feedPlan": config
        }
    }
    if method:
        body["props"]["method"] = method

    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()

    if result.get("code") != 2000:
        raise RuntimeError(f"设置定时喂食计划失败：{result.get('msg', '未知错误')}")

    if result.get("data", {}).get("Ret") != 100:
        raise RuntimeError(f"设备返回错误：{result.get('data', {}).get('Ret')}")

    return result.get("data", {})


def get_pet_detect_config(device_token: str, uuid: str, app_key: str,
                           app_secret: str, move_card: int) -> Dict[str, Any]:
    """
    获取宠物检测开关状态

    API: POST /gwp/v3/rtc/device/petDetectionSwitchStatus/{deviceToken}
    """
    url = f"{JF_BASE_URL}/rtc/device/petDetectionSwitchStatus/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)

    response = requests.post(url, headers=headers, timeout=30)
    result = response.json()

    if result.get("code") != 2000:
        raise RuntimeError(f"获取宠物检测状态失败：{result.get('msg', '未知错误')}")

    return result.get("data", {})


def set_pet_detect_config(device_token: str, uuid: str, app_key: str,
                           app_secret: str, move_card: int,
                           switch: str) -> Dict[str, Any]:
    """
    设置宠物检测开关状态

    API: POST /gwp/v3/rtc/device/petDetectionSwitchSetting/{deviceToken}
    """
    url = f"{JF_BASE_URL}/rtc/device/petDetectionSwitchSetting/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)

    body = {"Switch": switch}

    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()

    if result.get("code") != 2000:
        raise RuntimeError(f"设置宠物检测状态失败：{result.get('msg', '未知错误')}")

    if result.get("data", {}).get("Ret") != 100:
        raise RuntimeError(f"设备返回错误：{result.get('data', {}).get('Ret')}")

    return result.get("data", {})


def get_default_schedule_config() -> Dict[str, Any]:
    """获取默认定时喂食计划配置"""
    return [
        {
            "enable": True,
            "cron": "0 0 8 * * 1,2,3,4,5,6,0",
            "action": {
                "feed": 2
            }
        },
        {
            "enable": True,
            "cron": "0 0 18 * * 1,2,3,4,5,6,0",
            "action": {
                "feed": 2
            }
        }
    ]


# ============== 动作处理函数 ==============

def get_token_action(args: argparse.Namespace) -> int:
    """执行获取设备 Token 操作"""
    try:
        sns = args.device_sn.split(",") if args.device_sn else []
        if not sns:
            print("[错误] 错误：缺少 --device-sn 或 JF_DEVICE_SN 环境变量", file=sys.stderr)
            return 1

        print(f"正在获取 {len(sns)} 个设备的接口访问令牌...")

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
            print()

        # 如果只查询一个设备，提示可以直接使用
        if len(tokens) == 1:
            print("[提示] 可将上述 token 设置为环境变量后继续操作")
            print(f"   export JF_DEVICE_TOKEN=\"{tokens[0].get('token')}\"")

        return 0

    except RuntimeError as e:
        print(f"[错误] 错误：{e}", file=sys.stderr)
        return 1


def check_feed_support_action(args: argparse.Namespace) -> int:
    """执行查询设备是否支持喂食操作"""
    try:
        print(f"正在查询设备 {args.device_sn} 的喂食能力...")

        result = check_feed_support(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card
        )

        feeder = result.get("FeederAbility", {})
        if feeder:
            print("[OK] 查询成功")
            print(f"   堵粮报警：{'显示' if feeder.get('FeedBlockAlarm') else '不显示'}")
            print(f"   余粮报警：{'显示' if feeder.get('FoodShortageAlarm') else '不显示'}")

            box_nums = feeder.get("BoxNums")
            if box_nums is not None:
                print(f"   食物餐盘个数：{box_nums}")
            else:
                print("   食物餐盘个数：1（老设备默认值）")

            feed_snap = feeder.get("FeedSnap")
            if feed_snap is not None:
                print(f"   喂食抓图：{'支持' if feed_snap else '不支持'}")
            else:
                print("   喂食抓图：不支持")
        else:
            print("[警告] 设备未返回 FeederAbility 能力信息")

        print(f"   会话 ID: {result.get('SessionID')}")
        print(f"   Ret: {result.get('Ret')}")
        return 0

    except RuntimeError as e:
        print(f"[错误] {e}", file=sys.stderr)
        return 1


def feed_once_action(args: argparse.Namespace) -> int:
    """执行一键喂食操作"""
    try:
        portion = args.portion
        print(f"正在向设备 {args.device_sn} 发送喂食指令（{portion} 份）...")
        
        result = feed_once(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            device_sn=args.device_sn,
            portion=portion
        )
        
        print(f"[OK] 喂食指令发送成功")
        print(f"   出粮份数：{portion}")
        print(f"   会话 ID: {result.get('SessionID')}")
        return 0
        
    except RuntimeError as e:
        print(f"[错误] 错误：{e}", file=sys.stderr)
        return 1


def get_feed_schedule_action(args: argparse.Namespace) -> int:
    """执行获取定时喂食计划操作"""
    try:
        print(f"正在获取设备 {args.device_sn} 的定时喂食计划...")

        config = get_feed_schedule(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            device_sn=args.device_sn
        )

        props = config.get("props", {})
        schedules = props.get("feedPlan", [])
        if schedules is not None:
            print("[OK] 获取成功")
            print(f"   计划数量：{len(schedules)}")
            print()
            for i, s in enumerate(schedules):
                status = "启用" if s.get("enable") else "禁用"
                cron = s.get("cron", "")
                feed = s.get("action", {}).get("feed", 1)
                print(f"   [{i + 1}] cron={cron}  {feed}份  [{status}]")
        else:
            print("[警告] 设备未返回定时喂食计划配置")

        print(f"   会话 ID: {config.get('SessionID')}")
        return 0

    except RuntimeError as e:
        print(f"[错误] {e}", file=sys.stderr)
        return 1


def set_feed_schedule_action(args: argparse.Namespace) -> int:
    """执行设置定时喂食计划操作"""
    try:
        if args.schedule_file:
            with open(args.schedule_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            print(f"正在从文件 {args.schedule_file} 设置定时喂食计划...")
        else:
            print(f"正在设置设备 {args.device_sn} 的定时喂食计划...")
            config = get_default_schedule_config()

        result = set_feed_schedule(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            device_sn=args.device_sn,
            config=config
        )

        print("[OK] 设置成功")
        print(f"   会话 ID: {result.get('SessionID')}")
        return 0

    except RuntimeError as e:
        print(f"[错误] {e}", file=sys.stderr)
        return 1


def add_schedule_action(args: argparse.Namespace) -> int:
    """执行添加单条定时计划操作"""
    try:
        print(f"正在添加定时计划到设备 {args.device_sn}...")

        # 星期映射: Mon=1, Tue=2, Wed=3, Thu=4, Fri=5, Sat=6, Sun=0
        weekday_map = {
            "Mon": "1", "Tue": "2", "Wed": "3", "Thu": "4",
            "Fri": "5", "Sat": "6", "Sun": "0"
        }
        repeat_days = args.repeat.split(",") if args.repeat else ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        cron_weekdays = ",".join([weekday_map.get(d, d) for d in repeat_days])

        # cron 格式: 0 {minute} {hour} * * {weekdays}
        cron = f"0 {args.minute} {args.hour} * * {cron_weekdays}"

        # 先获取现有配置
        config_data = get_feed_schedule(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            device_sn=args.device_sn
        )

        props = config_data.get("props", {})
        schedules = props.get("feedPlan", []) if props else []
        if schedules is None:
            schedules = []

        # 构建新计划
        new_plan = {
            "enable": True,
            "cron": cron,
            "action": {
                "feed": args.portion
            }
        }

        schedules.append(new_plan)

        result = set_feed_schedule(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            device_sn=args.device_sn,
            config=schedules
        )

        print("[OK] 添加成功")
        print(f"   cron: {cron}")
        print(f"   份数: {args.portion}")
        print(f"   重复: {','.join(repeat_days)}")
        print(f"   会话 ID: {result.get('SessionID')}")
        return 0

    except RuntimeError as e:
        print(f"[错误] {e}", file=sys.stderr)
        return 1


def get_pet_detect_action(args: argparse.Namespace) -> int:
    """执行获取宠物检测开关状态操作"""
    try:
        print(f"正在获取设备 {args.device_sn} 的宠物检测开关状态...")

        config = get_pet_detect_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card
        )

        switch = config.get("Switch", "")
        if switch:
            print("[OK] 获取成功")
            print(f"   宠物检测开关：{'开启' if switch == 'ON' else '关闭'}")
        else:
            print("[警告] 未返回宠物检测开关状态")

        print(f"   Ret: {config.get('Ret')}")
        return 0

    except RuntimeError as e:
        print(f"[错误] {e}", file=sys.stderr)
        return 1


def set_pet_detect_action(args: argparse.Namespace) -> int:
    """执行设置宠物检测开关操作"""
    try:
        enable = args.enable.lower() == 'true'
        switch = "ON" if enable else "OFF"
        print(f"正在{'开启' if enable else '关闭'}设备 {args.device_sn} 的宠物检测...")

        result = set_pet_detect_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            switch=switch
        )

        print("[OK] 设置成功")
        print(f"   宠物检测：{'开启' if enable else '关闭'}")
        print(f"   Ret: {result.get('Ret')}")
        return 0

    except RuntimeError as e:
        print(f"[错误] {e}", file=sys.stderr)
        return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="杰峰智能宠物喂食器设备控制技能")
    
    # 全局参数
    parser.add_argument("--action", required=True,
                        choices=[
                            "get-token", "check-support", "feed-once",
                            "get-schedule", "set-schedule", "add-schedule",
                            "get-pet-detect", "set-pet-detect"
                        ],
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
    parser.add_argument("--channel", type=int, default=0,
                        help="通道号（默认 0）")
    
    # feed-once 参数
    parser.add_argument("--portion", type=int, default=1,
                        help="出粮份数（默认 1）")
    
    # set-schedule 参数
    parser.add_argument("--schedule-file", default=None,
                        help="定时计划配置文件路径")
    
    # add-schedule 参数
    parser.add_argument("--schedule-id", type=int, default=1,
                        help="计划编号（默认 1）")
    parser.add_argument("--hour", type=int, default=8,
                        help="小时（默认 8）")
    parser.add_argument("--minute", type=int, default=0,
                        help="分钟（默认 0）")
    parser.add_argument("--repeat", default="Mon,Tue,Wed,Thu,Fri,Sat,Sun",
                        help="重复周期（默认每天）")
    
    # set-pet-detect 参数
    parser.add_argument("--enable", default="true",
                        help="是否开启（true/false）")

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
        print("   提示：可先使用 --action get-token 获取 deviceToken", file=sys.stderr)
        return 1

    # 执行对应操作
    if args.action == "get-token":
        return get_token_action(args)
    elif args.action == "check-support":
        return check_feed_support_action(args)
    elif args.action == "feed-once":
        return feed_once_action(args)
    elif args.action == "get-schedule":
        return get_feed_schedule_action(args)
    elif args.action == "set-schedule":
        return set_feed_schedule_action(args)
    elif args.action == "add-schedule":
        return add_schedule_action(args)
    elif args.action == "get-pet-detect":
        return get_pet_detect_action(args)
    elif args.action == "set-pet-detect":
        return set_pet_detect_action(args)
    else:
        print(f"[错误] 未知操作：{args.action}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
