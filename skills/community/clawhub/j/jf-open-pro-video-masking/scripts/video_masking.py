#!/usr/bin/env python3
"""
杰峰设备视频遮挡技能（开发版）

支持功能：
- 开启一键遮蔽
- 关闭一键遮蔽
- 查询遮蔽状态
- 切换遮蔽状态
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


def set_video_masking(device_token: str, uuid: str, app_key: str,
                      app_secret: str, move_card: int,
                      enable: bool) -> Dict[str, Any]:
    """
    设置视频遮挡（一键遮蔽）
    
    API: POST /gwp/v3/rtc/device/setconfig/{deviceToken}
    Name: OPPTZControl
    """
    url = f"{JF_BASE_URL}/rtc/device/setconfig/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "Name": "OPPTZControl",
        "General.OneKeyMaskVideo": [
            {
                "Enable": enable
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"设置遮蔽失败：{result.get('msg', '未知错误')}")
    
    if result.get("data", {}).get("Ret") != 100:
        raise RuntimeError(f"设备返回错误：{result.get('data', {}).get('Ret')}")
    
    return result.get("data", {})


def get_masking_status(device_token: str, uuid: str, app_key: str,
                       app_secret: str, move_card: int) -> Optional[bool]:
    """
    获取遮蔽状态
    
    注意：当前 API 没有直接查询遮蔽状态的接口
    需要通过设备能力集或本地缓存来判断
    
    返回 None 表示无法确定状态
    """
    # 由于 API 没有直接查询接口，返回 None
    # 实际使用时可以缓存最后一次设置的状态
    return None


# ============== 动作处理函数 ==============

def enable_masking_action(args: argparse.Namespace) -> int:
    """执行开启遮蔽操作"""
    try:
        print(f"正在开启设备 {args.device_sn} 的一键遮蔽...")
        print()
        print("⚠️  开启遮蔽后:")
        print("   - 摄像头将转至最下方和最右侧")
        print("   - 视频预览将关闭")
        print("   - 录像将停止")
        print()
        
        result = set_video_masking(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            enable=True
        )
        
        print("✅ 一键遮蔽已开启")
        print(f"   设备：{args.device_sn}")
        print(f"   会话 ID: {result.get('SessionID')}")
        print()
        print("💡 提示：关闭遮蔽后摄像头将自动恢复原位")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def disable_masking_action(args: argparse.Namespace) -> int:
    """执行关闭遮蔽操作"""
    try:
        print(f"正在关闭设备 {args.device_sn} 的一键遮蔽...")
        print()
        print("💡 关闭遮蔽后:")
        print("   - 摄像头将恢复到原监控位置")
        print("   - 视频预览将恢复")
        print("   - 录像将恢复")
        print()
        
        result = set_video_masking(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            enable=False
        )
        
        print("✅ 一键遮蔽已关闭")
        print(f"   设备：{args.device_sn}")
        print(f"   会话 ID: {result.get('SessionID')}")
        print()
        print("💡 提示：设备已恢复正常监控")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def status_action(args: argparse.Namespace) -> int:
    """执行查询遮蔽状态操作"""
    try:
        print(f"正在查询设备 {args.device_sn} 的遮蔽状态...")
        print()
        
        # 由于 API 没有直接查询接口，提示用户
        print("⚠️  当前 API 不支持直接查询遮蔽状态")
        print()
        print("💡 建议:")
        print("   - 通过摄像头画面判断是否处于遮蔽位置")
        print("   - 查看设备最后操作记录")
        print("   - 使用 toggle 命令切换状态")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def toggle_action(args: argparse.Namespace) -> int:
    """执行切换遮蔽状态操作"""
    try:
        print(f"正在切换设备 {args.device_sn} 的遮蔽状态...")
        print()
        print("ℹ️  由于无法查询当前状态，将尝试关闭遮蔽")
        print("   如果当前是开启状态，将关闭遮蔽")
        print("   如果当前是关闭状态，操作将无效果")
        print()
        
        # 尝试关闭遮蔽（安全操作）
        result = set_video_masking(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            enable=False
        )
        
        print("✅ 遮蔽状态已切换")
        print(f"   设备：{args.device_sn}")
        print(f"   会话 ID: {result.get('SessionID')}")
        print()
        print("💡 提示：如需开启遮蔽，请使用 enable 命令")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="杰峰设备视频遮挡技能")
    
    # 全局参数
    parser.add_argument("--action", required=True,
                        choices=["enable", "disable", "status", "toggle"],
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
    if args.action == "enable":
        return enable_masking_action(args)
    elif args.action == "disable":
        return disable_masking_action(args)
    elif args.action == "status":
        return status_action(args)
    elif args.action == "toggle":
        return toggle_action(args)
    else:
        print(f"❌ 未知操作：{args.action}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
