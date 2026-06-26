#!/usr/bin/env python3
"""
杰峰设备重启技能（开发版）

支持功能：
- 设备重启
- 设备关闭（部分设备支持）
"""

import os
import sys
import argparse
import requests
import time
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


def device_reboot(device_token: str, uuid: str, app_key: str,
                  app_secret: str, move_card: int,
                  action: str = "Reboot") -> Dict[str, Any]:
    """
    设备重启/关闭
    
    API: POST /gwp/v3/rtc/device/opdev/{deviceToken}
    Name: OPMachine
    """
    url = f"{JF_BASE_URL}/rtc/device/opdev/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "Name": "OPMachine",
        "OPMachine": {
            "Action": action
        }
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"设备{action}失败：{result.get('msg', '未知错误')}")
    
    if result.get("data", {}).get("Ret") != 100:
        raise RuntimeError(f"设备返回错误：{result.get('data', {}).get('Ret')}")
    
    return result.get("data", {})


def confirm_action(action: str) -> bool:
    """确认操作"""
    action_name = "重启" if action == "Reboot" else "关闭"
    print()
    print(f"⚠️  警告：即将{action_name}设备！")
    print()
    print(f"   - 设备将暂时离线")
    print(f"   - 重启通常需要 1-3 分钟")
    print(f"   - 重启期间无法进行任何操作")
    print()
    
    confirm = input(f"确认{action_name}设备？(yes/no): ")
    return confirm.lower() in ["yes", "y"]


# ============== 动作处理函数 ==============

def reboot_action(args: argparse.Namespace) -> int:
    """执行设备重启操作"""
    try:
        # 确认操作
        if args.confirm:
            if not confirm_action("Reboot"):
                print("❌ 操作已取消")
                return 1
        
        print(f"正在重启设备 {args.device_sn}...")
        print()
        
        result = device_reboot(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            action="Reboot"
        )
        
        print("✅ 设备重启指令已发送")
        print(f"   设备：{args.device_sn}")
        print(f"   会话 ID: {result.get('SessionID')}")
        print()
        print("⚠️  注意:")
        print("   - 设备将暂时离线")
        print("   - 重启通常需要 1-3 分钟")
        print("   - 请稍后查询设备状态确认重启完成")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def shutdown_action(args: argparse.Namespace) -> int:
    """执行设备关闭操作"""
    try:
        # 确认操作
        if args.confirm:
            if not confirm_action("Shutdown"):
                print("❌ 操作已取消")
                return 1
        
        print(f"正在关闭设备 {args.device_sn}...")
        print()
        print("⚠️  注意：大部分设备只支持重启，不支持关闭")
        print()
        
        result = device_reboot(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            action="Shutdown"
        )
        
        print("✅ 设备关闭指令已发送")
        print(f"   设备：{args.device_sn}")
        print(f"   会话 ID: {result.get('SessionID')}")
        print()
        print("⚠️  注意:")
        print("   - 大部分设备会执行重启而非关闭")
        print("   - 设备将暂时离线")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="杰峰设备重启技能")
    
    # 全局参数
    parser.add_argument("--action", required=True,
                        choices=["reboot", "shutdown"],
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
    
    # 确认参数
    parser.add_argument("--confirm", action="store_true",
                        help="操作前确认")
    
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
    if args.action == "reboot":
        return reboot_action(args)
    elif args.action == "shutdown":
        return shutdown_action(args)
    else:
        print(f"❌ 未知操作：{args.action}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
