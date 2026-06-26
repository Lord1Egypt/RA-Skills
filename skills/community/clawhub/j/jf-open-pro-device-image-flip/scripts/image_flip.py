#!/usr/bin/env python3
"""
杰峰设备画面翻转技能（开发版）

支持功能：
- 画面左右翻转（镜像）
- 画面上下翻转（倒置）
- 翻转状态查询
"""

import os
import sys
import argparse
import requests
from typing import Optional, Dict, Any

# 导入加密工具（复用）
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


def get_camera_param(device_token: str, uuid: str, app_key: str,
                     app_secret: str, move_card: int,
                     channel: int = 0) -> Dict[str, Any]:
    """
    获取摄像头基本参数配置
    
    API: POST /gwp/v3/rtc/device/getconfig/{deviceToken}
    Name: Camera.Param
    """
    url = f"{JF_BASE_URL}/rtc/device/getconfig/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {"Name": "Camera.Param"}
    if channel is not None:
        body["Channel"] = str(channel)
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取配置失败：{result.get('msg', '未知错误')}")
    
    return result.get("data", {})


def set_camera_param(device_token: str, uuid: str, app_key: str,
                     app_secret: str, move_card: int,
                     config: Dict[str, Any]) -> Dict[str, Any]:
    """
    设置摄像头基本参数配置
    
    API: POST /gwp/v3/rtc/device/setconfig/{deviceToken}
    Name: Camera.Param
    """
    url = f"{JF_BASE_URL}/rtc/device/setconfig/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "Name": "Camera.Param",
        "Camera.Param": config
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"设置配置失败：{result.get('msg', '未知错误')}")
    
    if result.get("data", {}).get("Ret") != 100:
        raise RuntimeError(f"设备返回错误：{result.get('data', {}).get('Ret')}")
    
    return result.get("data", {})


def hex_to_bool(hex_str: str) -> bool:
    """将十六进制字符串转换为布尔值"""
    return hex_str == "0x00000001"


def bool_to_hex(value: bool) -> str:
    """将布尔值转换为十六进制字符串"""
    return "0x00000001" if value else "0x00000000"


def get_default_camera_param() -> Dict[str, Any]:
    """获取默认的摄像头参数配置"""
    return {
        "AeSensitivity": 0,
        "ApertureMode": "0x00000000",
        "BLCMode": "0x00000000",
        "DayNightColor": "0x00000000",
        "Day_nfLevel": 0,
        "Night_nfLevel": 0,
        "DncThr": 0,
        "ElecLevel": 0,
        "EsShutter": "0x00000000",
        "ExposureParam": {
            "LeastTime": "0x00000000",
            "Level": 0,
            "MostTime": "0x00000000"
        },
        "GainParam": {
            "AutoGain": 0,
            "Gain": 50
        },
        "IRCUTMode": 0,
        "InfraredSwap": 0,
        "IrcutSwap": 0,
        "PictureFlip": "0x00000000",
        "PictureMirror": "0x00000000",
        "RejectFlicker": "0x00000000",
        "WhiteBalance": "0x00000000"
    }


# ============== 动作处理函数 ==============

def get_flip_config_action(args: argparse.Namespace) -> int:
    """执行获取画面翻转配置操作"""
    try:
        print(f"正在获取设备 {args.device_sn} 的画面翻转配置...")
        
        config_data = get_camera_param(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel
        )
        
        camera_param = config_data.get("Camera.Param", [])
        if camera_param:
            cp = camera_param[0]
            mirror = hex_to_bool(cp.get("PictureMirror", "0x00000000"))
            flip = hex_to_bool(cp.get("PictureFlip", "0x00000000"))
            
            print()
            print("✅ 获取配置成功")
            print()
            print("📋 画面翻转状态:")
            print(f"   左右翻转（镜像）: {'开启' if mirror else '关闭'}")
            print(f"   上下翻转（倒置）: {'开启' if flip else '关闭'}")
            print()
            
            # 显示效果说明
            if mirror and flip:
                print("   💡 效果：画面旋转 180 度")
            elif mirror:
                print("   💡 效果：画面左右镜像")
            elif flip:
                print("   💡 效果：画面上下倒置")
            else:
                print("   💡 效果：原始画面（无翻转）")
            
            print()
            print(f"   会话 ID: {config_data.get('SessionID')}")
        else:
            print("⚠️  未找到摄像头参数配置")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def set_mirror_action(args: argparse.Namespace) -> int:
    """执行设置左右翻转（镜像）操作"""
    try:
        enable = args.enable.lower() == 'true'
        print(f"正在{'开启' if enable else '关闭'}设备 {args.device_sn} 的左右翻转（镜像）...")
        
        config_data = get_camera_param(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel
        )
        
        camera_param = config_data.get("Camera.Param", [])
        if not camera_param:
            camera_param = [get_default_camera_param()]
        
        camera_param[0]["PictureMirror"] = bool_to_hex(enable)
        
        result = set_camera_param(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            config=camera_param
        )
        
        print()
        print("✅ 设置成功")
        print(f"   左右翻转（镜像）: {'开启' if enable else '关闭'}")
        print(f"   会话 ID: {result.get('SessionID')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def set_flip_action(args: argparse.Namespace) -> int:
    """执行设置上下翻转操作"""
    try:
        enable = args.enable.lower() == 'true'
        print(f"正在{'开启' if enable else '关闭'}设备 {args.device_sn} 的上下翻转...")
        
        config_data = get_camera_param(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel
        )
        
        camera_param = config_data.get("Camera.Param", [])
        if not camera_param:
            camera_param = [get_default_camera_param()]
        
        camera_param[0]["PictureFlip"] = bool_to_hex(enable)
        
        result = set_camera_param(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            config=camera_param
        )
        
        print()
        print("✅ 设置成功")
        print(f"   上下翻转（倒置）: {'开启' if enable else '关闭'}")
        print(f"   会话 ID: {result.get('SessionID')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def set_both_action(args: argparse.Namespace) -> int:
    """执行同时设置左右和上下翻转操作"""
    try:
        mirror = args.mirror.lower() == 'true'
        flip = args.flip.lower() == 'true'
        
        print(f"正在设置设备 {args.device_sn} 的画面翻转...")
        print(f"   左右翻转（镜像）: {'开启' if mirror else '关闭'}")
        print(f"   上下翻转（倒置）: {'开启' if flip else '关闭'}")
        
        config_data = get_camera_param(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel
        )
        
        camera_param = config_data.get("Camera.Param", [])
        if not camera_param:
            camera_param = [get_default_camera_param()]
        
        camera_param[0]["PictureMirror"] = bool_to_hex(mirror)
        camera_param[0]["PictureFlip"] = bool_to_hex(flip)
        
        result = set_camera_param(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            config=camera_param
        )
        
        print()
        print("✅ 设置成功")
        
        if mirror and flip:
            print("   效果：画面旋转 180 度")
        elif mirror:
            print("   效果：画面左右镜像")
        elif flip:
            print("   效果：画面上下倒置")
        else:
            print("   效果：原始画面（无翻转）")
        
        print(f"   会话 ID: {result.get('SessionID')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def reset_action(args: argparse.Namespace) -> int:
    """执行重置画面方向操作"""
    try:
        print(f"正在重置设备 {args.device_sn} 的画面方向...")
        
        config_data = get_camera_param(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            channel=args.channel
        )
        
        camera_param = config_data.get("Camera.Param", [])
        if not camera_param:
            camera_param = [get_default_camera_param()]
        
        camera_param[0]["PictureMirror"] = "0x00000000"
        camera_param[0]["PictureFlip"] = "0x00000000"
        
        result = set_camera_param(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            config=camera_param
        )
        
        print()
        print("✅ 重置成功")
        print("   画面已恢复为原始方向（无翻转）")
        print(f"   会话 ID: {result.get('SessionID')}")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="杰峰设备画面翻转技能")
    
    # 全局参数
    parser.add_argument("--action", required=True,
                        choices=[
                            "get-flip-config", "set-mirror", "set-flip",
                            "set-both", "reset"
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
    
    # set-mirror / set-flip 参数
    parser.add_argument("--enable", default="true",
                        help="是否开启（true/false）")
    
    # set-both 参数
    parser.add_argument("--mirror", default="true",
                        help="是否开启左右翻转（true/false）")
    parser.add_argument("--flip", default="true",
                        help="是否开启上下翻转（true/false）")
    
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
    
    # 执行对应操作
    if args.action == "get-flip-config":
        return get_flip_config_action(args)
    elif args.action == "set-mirror":
        return set_mirror_action(args)
    elif args.action == "set-flip":
        return set_flip_action(args)
    elif args.action == "set-both":
        return set_both_action(args)
    elif args.action == "reset":
        return reset_action(args)
    else:
        print(f"❌ 未知操作：{args.action}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
