#!/usr/bin/env python3
"""
杰峰设备人形检测技能（开发版）

支持功能：
- 人形检测开关设置
- 人形检测灵敏度设置
- 人形追踪开关设置
- 人形追踪灵敏度设置
- 追踪返回时间设置
"""

import os
import sys
import argparse
import requests
from typing import Optional, Dict, Any, List

# 导入加密工具（复用 smart-alarm 的 crypto.py）
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from crypto import get_time_millis, generate_signature
except ImportError:
    print("❌ 错误：找不到 crypto.py 模块")
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


def get_human_detect_config(device_token: str, uuid: str, app_key: str,
                             app_secret: str, move_card: int,
                             channel: int = 0) -> Dict[str, Any]:
    """
    获取人形检测配置
    
    API: POST /gwp/v3/rtc/device/getconfig/{deviceToken}
    Name: Detect.HumanDetection
    """
    url = f"{JF_BASE_URL}/rtc/device/getconfig/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {"Name": "Detect.HumanDetection"}
    if channel is not None:
        body["Channel"] = str(channel)
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取人形检测配置失败：{result.get('msg', '未知错误')}")
    
    return result.get("data", {})


def set_human_detect_config(device_token: str, uuid: str, app_key: str,
                             app_secret: str, move_card: int,
                             config: Dict[str, Any]) -> Dict[str, Any]:
    """
    设置人形检测配置
    
    API: POST /gwp/v3/rtc/device/setconfig/{deviceToken}
    Name: Detect.HumanDetection
    """
    url = f"{JF_BASE_URL}/rtc/device/setconfig/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "Name": "Detect.HumanDetection",
        "Detect.HumanDetection": config
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"设置人形检测配置失败：{result.get('msg', '未知错误')}")
    
    if result.get("data", {}).get("Ret") != 100:
        raise RuntimeError(f"设备返回错误：{result.get('data', {}).get('Ret')}")
    
    return result.get("data", {})


def get_human_track_config(device_token: str, uuid: str, app_key: str,
                            app_secret: str, move_card: int,
                            channel: int = 0) -> Dict[str, Any]:
    """
    获取人形追踪配置
    
    API: POST /gwp/v3/rtc/device/getconfig/{deviceToken}
    Name: Detect.DetectTrack
    """
    url = f"{JF_BASE_URL}/rtc/device/getconfig/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {"Name": "Detect.DetectTrack"}
    if channel is not None:
        body["Channel"] = str(channel)
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取人形追踪配置失败：{result.get('msg', '未知错误')}")
    
    return result.get("data", {})


def set_human_track_config(device_token: str, uuid: str, app_key: str,
                            app_secret: str, move_card: int,
                            config: Dict[str, Any]) -> Dict[str, Any]:
    """
    设置人形追踪配置
    
    API: POST /gwp/v3/rtc/device/setconfig/{deviceToken}
    Name: Detect.DetectTrack
    """
    url = f"{JF_BASE_URL}/rtc/device/setconfig/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "Name": "Detect.DetectTrack",
        "Detect.DetectTrack": config
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"设置人形追踪配置失败：{result.get('msg', '未知错误')}")
    
    if result.get("data", {}).get("Ret") != 100:
        raise RuntimeError(f"设备返回错误：{result.get('data', {}).get('Ret')}")
    
    return result.get("data", {})


def get_default_human_detect_config() -> Dict[str, Any]:
    """获取默认的人形检测配置"""
    return {
        "Enable": False,
        "ObjectType": 0,
        "PedFdrAlg": 0,
        "AlgoCreate": True,
        "ShowRule": False,
        "ShowTrack": False,
        "Sensitivity": 1,
        "PushInterval": 3000,
        "PedRule": [
            {
                "Enable": False,
                "RuleType": 1,
                "RuleRegion": {
                    "PtsNum": 4,
                    "AlarmDirect": 2,
                    "Pts": [
                        {"X": 100, "Y": 100},
                        {"X": 8191, "Y": 100},
                        {"X": 8191, "Y": 8191},
                        {"X": 100, "Y": 8191}
                    ],
                    "Sensitivity": 1
                },
                "RuleLine": {
                    "AlarmDirect": 2,
                    "Pts": {
                        "StartX": 100,
                        "StartY": 100,
                        "StopX": 8191,
                        "StopY": 8191
                    }
                }
            }
        ] * 4  # 4 个警戒区域
    }


def get_default_human_track_config() -> Dict[str, Any]:
    """获取默认的人形追踪配置"""
    return {
        "Enable": 0,
        "Sensitivity": 1,
        "ReturnTime": 10
    }


# ============== 动作处理函数 ==============

def get_human_detect_config_action(args: argparse.Namespace) -> int:
    """执行获取人形检测配置操作"""
    try:
        print(f"正在获取设备 {args.device_sn} 的人形检测配置...")
        
        config = get_human_detect_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel
        )
        
        human_detect = config.get("Detect.HumanDetection", [])
        if human_detect:
            hd = human_detect[0]
            event_map = {
                0: "单人形检测",
                1: "人形 + 人脸检测",
                2: "人形 + 人脸识别",
                3: "人形 + 车形检测",
                4: "人形 + 车形 + 人脸",
                5: "宠物检测"
            }
            sens_map = {0: "低", 1: "中", 2: "高", 3: "灵敏度数量"}
            
            print(f"✅ 获取配置成功")
            print(f"   人形检测开关：{'开启' if hd.get('Enable') else '关闭'}")
            print(f"   算法类型：{hd.get('PedFdrAlg', 0)} ({event_map.get(hd.get('PedFdrAlg', 0), '未知')})")
            print(f"   检测灵敏度：{hd.get('Sensitivity', 1)} ({sens_map.get(hd.get('Sensitivity', 1), '未知')})")
            print(f"   目标类型：{'人' if hd.get('ObjectType', 0) == 0 else '物体'}")
            print(f"   叠加规则框：{'是' if hd.get('ShowRule') else '否'}")
            print(f"   叠加移动框：{'是' if hd.get('ShowTrack') else '否'}")
            print(f"   推图间隔：{hd.get('PushInterval', -1)}ms")
            print(f"   会话 ID: {config.get('SessionID')}")
        else:
            print("⚠️  未找到人形检测配置")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def set_human_detect_switch_action(args: argparse.Namespace) -> int:
    """执行设置人形检测开关操作"""
    try:
        enable = args.enable.lower() == 'true'
        print(f"正在{'开启' if enable else '关闭'}设备 {args.device_sn} 的人形检测...")
        
        config_data = get_human_detect_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel
        )
        
        human_detect = config_data.get("Detect.HumanDetection", [])
        if not human_detect:
            human_detect = [get_default_human_detect_config()]
        
        human_detect[0]["Enable"] = enable
        
        result = set_human_detect_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            config=human_detect
        )
        
        print(f"✅ 设置成功")
        print(f"   人形检测：{'开启' if enable else '关闭'}")
        print(f"   会话 ID: {result.get('SessionID')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def set_human_detect_sensitivity_action(args: argparse.Namespace) -> int:
    """执行设置人形检测灵敏度操作"""
    try:
        level = args.level
        sens_map = {0: "低", 1: "中", 2: "高", 3: "灵敏度数量"}
        
        if level not in [0, 1, 2, 3]:
            print(f"❌ 错误：灵敏度级别必须是 0-3 之间的整数", file=sys.stderr)
            return 1
        
        print(f"正在设置设备 {args.device_sn} 的人形检测灵敏度为 {level} ({sens_map.get(level, '未知')})...")
        
        config_data = get_human_detect_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel
        )
        
        human_detect = config_data.get("Detect.HumanDetection", [])
        if not human_detect:
            human_detect = [get_default_human_detect_config()]
        
        human_detect[0]["Sensitivity"] = level
        
        result = set_human_detect_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            config=human_detect
        )
        
        print(f"✅ 设置成功")
        print(f"   检测灵敏度：{level} ({sens_map.get(level, '未知')})")
        print(f"   会话 ID: {result.get('SessionID')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def get_human_track_config_action(args: argparse.Namespace) -> int:
    """执行获取人形追踪配置操作"""
    try:
        print(f"正在获取设备 {args.device_sn} 的人形追踪配置...")
        
        config = get_human_track_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel
        )
        
        track = config.get("Detect.DetectTrack", {})
        if track:
            sens_map = {0: "低", 1: "中", 2: "高"}
            
            print(f"✅ 获取配置成功")
            print(f"   人形追踪开关：{'开启' if track.get('Enable', 0) == 1 else '关闭'}")
            print(f"   追踪灵敏度：{track.get('Sensitivity', 1)} ({sens_map.get(track.get('Sensitivity', 1), '未知')})")
            print(f"   返回时间：{track.get('ReturnTime', 1)}秒")
            print(f"   会话 ID: {config.get('SessionID')}")
        else:
            print("⚠️  未找到人形追踪配置")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def set_human_track_switch_action(args: argparse.Namespace) -> int:
    """执行设置人形追踪开关操作"""
    try:
        enable = 1 if args.enable.lower() == 'true' else 0
        print(f"正在{'开启' if enable == 1 else '关闭'}设备 {args.device_sn} 的人形追踪...")
        
        config_data = get_human_track_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel
        )
        
        track = config_data.get("Detect.DetectTrack", get_default_human_track_config())
        track["Enable"] = enable
        
        result = set_human_track_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            config=track
        )
        
        print(f"✅ 设置成功")
        print(f"   人形追踪：{'开启' if enable == 1 else '关闭'}")
        print(f"   会话 ID: {result.get('SessionID')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def set_human_track_sensitivity_action(args: argparse.Namespace) -> int:
    """执行设置人形追踪灵敏度操作"""
    try:
        level = args.level
        sens_map = {0: "低", 1: "中", 2: "高"}
        
        if level not in [0, 1, 2]:
            print(f"❌ 错误：灵敏度级别必须是 0-2 之间的整数", file=sys.stderr)
            return 1
        
        print(f"正在设置设备 {args.device_sn} 的人形追踪灵敏度为 {level} ({sens_map.get(level, '未知')})...")
        
        config_data = get_human_track_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel
        )
        
        track = config_data.get("Detect.DetectTrack", get_default_human_track_config())
        track["Sensitivity"] = level
        
        result = set_human_track_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            config=track
        )
        
        print(f"✅ 设置成功")
        print(f"   追踪灵敏度：{level} ({sens_map.get(level, '未知')})")
        print(f"   会话 ID: {result.get('SessionID')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def set_track_return_time_action(args: argparse.Namespace) -> int:
    """执行设置追踪返回时间操作"""
    try:
        seconds = args.seconds
        
        if seconds < 0 or seconds > 600:
            print(f"❌ 错误：返回时间必须是 0-600 之间的整数", file=sys.stderr)
            return 1
        
        desc = "不返回" if seconds == 0 else f"{seconds}秒后返回"
        print(f"正在设置设备 {args.device_sn} 的追踪返回时间为 {desc}...")
        
        config_data = get_human_track_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel
        )
        
        track = config_data.get("Detect.DetectTrack", get_default_human_track_config())
        track["ReturnTime"] = seconds
        
        result = set_human_track_config(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            config=track
        )
        
        print(f"✅ 设置成功")
        print(f"   返回时间：{desc}")
        print(f"   会话 ID: {result.get('SessionID')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="杰峰设备人形检测技能")
    
    # 全局参数
    parser.add_argument("--action", required=True,
                        choices=[
                            "get-human-detect-config", "set-human-detect-switch",
                            "set-human-detect-sensitivity", "get-human-track-config",
                            "set-human-track-switch", "set-human-track-sensitivity",
                            "set-track-return-time"
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
    
    # set-human-detect-switch 参数
    parser.add_argument("--enable", default="true",
                        help="是否开启（true/false）")
    
    # set-human-detect-sensitivity 参数
    parser.add_argument("--level", type=int, default=1,
                        help="灵敏度级别（0=低，1=中，2=高，3=灵敏度数量）")
    
    # set-human-track-switch 参数
    parser.add_argument("--enable", dest="track_enable", default="true",
                        help="是否开启（true/false）")
    
    # set-human-track-sensitivity 参数
    parser.add_argument("--level", dest="track_level", type=int, default=1,
                        help="追踪灵敏度级别（0=低，1=中，2=高）")
    
    # set-track-return-time 参数
    parser.add_argument("--seconds", type=int, default=10,
                        help="返回时间（秒），0=不返回，1-600=指定时间")
    
    args = parser.parse_args()
    
    # 验证必需参数
    if not args.uuid:
        print("❌ 错误：缺少 --uuid 或 JF_UUID 环境变量", file=sys.stderr)
        return 1
    if not args.app_key:
        print("❌ 错误：缺少 --app-key 或 JF_APP_KEY 环境变量", file=sys.stderr)
        return 1
    if not args.app_secret:
        print("❌ 错误：缺少 --app-secret 或 JF_APP_SECRET 环境变量", file=sys.stderr)
        return 1
    if not args.device_token:
        print("❌ 错误：缺少 --device-token 或 JF_DEVICE_TOKEN 环境变量", file=sys.stderr)
        return 1
    
    # 处理参数覆盖
    if args.action == "set-human-track-switch":
        args.enable = args.track_enable
    if args.action == "set-human-track-sensitivity":
        args.level = args.track_level
    
    # 执行对应操作
    if args.action == "get-human-detect-config":
        return get_human_detect_config_action(args)
    elif args.action == "set-human-detect-switch":
        return set_human_detect_switch_action(args)
    elif args.action == "set-human-detect-sensitivity":
        return set_human_detect_sensitivity_action(args)
    elif args.action == "get-human-track-config":
        return get_human_track_config_action(args)
    elif args.action == "set-human-track-switch":
        return set_human_track_switch_action(args)
    elif args.action == "set-human-track-sensitivity":
        return set_human_track_sensitivity_action(args)
    elif args.action == "set-track-return-time":
        return set_track_return_time_action(args)
    else:
        print(f"❌ 未知操作：{args.action}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
