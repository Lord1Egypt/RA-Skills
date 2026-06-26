#!/usr/bin/env python3
"""
杰峰低功耗设备电池管理技能（开发版）

支持功能：
- 查询低电量阈值范围（使用 Ability.AovAbility）
- 查询当前低电量阈值（使用 Dev.LowElectrMode）
- 设置低电量阈值（使用 Dev.LowElectrMode）
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


def get_low_elect_range(device_token: str, uuid: str, app_key: str, app_secret: str, move_card: int) -> Dict[str, Any]:
    """
    获取低电量阈值范围
    
    API: POST /gwp/v3/rtc/device/getconfig/{deviceToken}
    Name: Ability.AovAbility
    
    只返回 LowElectrMin 和 LowElectrMax
    PowerThreshold 从 Dev.LowElectrMode 获取
    """
    url = f"{JF_BASE_URL}/rtc/device/getconfig/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "Name": "Ability.AovAbility"
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取低电量阈值范围失败：{result.get('msg', '未知错误')}")
    
    data = result.get("data", {})
    aov_ability = data.get("Ability.AovAbility", {})
    
    # 只解析 LowElectrMin 和 LowElectrMax
    # PowerThreshold 从 Dev.LowElectrMode 获取
    return {
        "LowElectrMin": aov_ability.get("LowElectrMin", 0),
        "LowElectrMax": aov_ability.get("LowElectrMax", 0)
    }


def get_current_threshold(device_token: str, uuid: str, app_key: str, app_secret: str, move_card: int) -> Dict[str, Any]:
    """
    获取当前低电量阈值（已生效的值）
    
    API: POST /gwp/v3/rtc/device/getconfig/{deviceToken}
    Name: Dev.LowElectrMode
    
    返回 PowerThreshold
    """
    url = f"{JF_BASE_URL}/rtc/device/getconfig/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "Name": "Dev.LowElectrMode"
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"获取当前阈值失败：{result.get('msg', '未知错误')}")
    
    data = result.get("data", {})
    low_elect_mode = data.get("Dev.LowElectrMode", {})
    
    return {
        "PowerThreshold": low_elect_mode.get("PowerThreshold")
    }


def set_low_elect_threshold(device_token: str, uuid: str, app_key: str, app_secret: str, move_card: int, threshold: int) -> Dict[str, Any]:
    """
    设置低电量阈值
    
    API: POST /gwp/v3/rtc/device/setconfig/{deviceToken}
    Name: Dev.LowElectrMode
    
    官方文档：https://docs.jftech.com/docs?menusId=54582398fd8d4248962354e92ac2e47a&siderId=b246b44faa8c4d41a3f10e3de95b892a&lang=zh
    """
    url = f"{JF_BASE_URL}/rtc/device/setconfig/{device_token}"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "Name": "Dev.LowElectrMode",
        "Dev.LowElectrMode": {
            "PowerThreshold": threshold
        }
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"设置低电量阈值失败：{result.get('msg', '未知错误')}")
    
    return result.get("data", {})


# ============== 动作处理函数 ==============

def get_range_action(args: argparse.Namespace) -> int:
    """执行查询低电量阈值范围操作"""
    try:
        # 步骤 1: 查询阈值范围 (使用 Ability.AovAbility)
        print("步骤 1/2: 正在查询阈值范围 (Ability.AovAbility)...")
        range_result = get_low_elect_range(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card
        )
        
        min_val = range_result.get('LowElectrMin', 0)
        max_val = range_result.get('LowElectrMax', 0)
        print(f"✅ 阈值范围：{min_val}% ~ {max_val}%")
        print()
        
        # 步骤 2: 查询当前阈值 (使用 Dev.LowElectrMode)
        print("步骤 2/2: 正在查询当前阈值 (Dev.LowElectrMode)...")
        current_result = get_current_threshold(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card
        )
        
        current = current_result.get('PowerThreshold')
        print()
        print("✅ 查询成功")
        print()
        print("设备信息:")
        print(f"  设备：{args.device_sn}")
        if current is not None:
            print(f"  当前阈值：{current}%  (来源：Dev.LowElectrMode.PowerThreshold)")
        else:
            print(f"  当前阈值：未设置")
        print(f"  最小阈值：{min_val}%  (来源：Ability.AovAbility.LowElectrMin)")
        print(f"  最大阈值：{max_val}%  (来源：Ability.AovAbility.LowElectrMax)")
        print()
        print(f"💡 提示：设置阈值时请在 {min_val}% ~ {max_val}% 范围内")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def get_and_set_action(args: argparse.Namespace) -> int:
    """执行获取范围 + 设置阈值的组合操作"""
    try:
        # 验证阈值参数
        if args.threshold is None:
            print("❌ 错误：get-and-set 操作需要 --threshold 参数", file=sys.stderr)
            return 1
        
        if args.threshold < 0 or args.threshold > 100:
            print(f"❌ 错误：阈值必须在 0-100 之间，当前值为 {args.threshold}", file=sys.stderr)
            return 1
        
        # 步骤 1: 获取阈值范围 (使用 Ability.AovAbility)
        print("步骤 1/3: 正在获取阈值范围 (Ability.AovAbility)...")
        range_result = get_low_elect_range(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card
        )
        
        min_val = range_result.get('LowElectrMin', 0)
        max_val = range_result.get('LowElectrMax', 100)
        print(f"✅ 阈值范围：{min_val}% ~ {max_val}%")
        print(f"   来源：Ability.AovAbility.LowElectrMin/Max")
        print()
        
        # 步骤 2: 查询当前阈值 (使用 Dev.LowElectrMode)
        print("步骤 2/3: 正在查询当前阈值 (Dev.LowElectrMode)...")
        current_result = get_current_threshold(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card
        )
        
        current = current_result.get('PowerThreshold')
        if current is not None:
            print(f"✅ 当前阈值：{current}%")
            print(f"   来源：Dev.LowElectrMode.PowerThreshold")
        else:
            print(f"✅ 当前阈值：未设置")
        print()
        
        # 步骤 3: 验证并设置阈值 (使用 Dev.LowElectrMode)
        if args.threshold < min_val or args.threshold > max_val:
            print(f"❌ 错误：阈值 {args.threshold}% 超出设备支持范围 ({min_val}% ~ {max_val}%)", file=sys.stderr)
            print()
            print("💡 建议:")
            print(f"   - 请使用 {min_val}% ~ {max_val}% 之间的值")
            print(f"   - 例如：--threshold {min_val} 或 --threshold {max_val}")
            return 1
        
        print(f"步骤 3/3: 设置阈值为 {args.threshold}% (Dev.LowElectrMode)...")
        print()
        
        result = set_low_elect_threshold(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            threshold=args.threshold
        )
        
        print("✅ 低电量阈值设置成功")
        print(f"   设备：{args.device_sn}")
        print(f"   新阈值：{args.threshold}%")
        print(f"   来源：Dev.LowElectrMode.PowerThreshold")
        if result.get('SessionID'):
            print(f"   会话 ID: {result.get('SessionID')}")
        print()
        print("💡 提示：设备将在电量低于设定值时自动进入低电量模式")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def set_threshold_action(args: argparse.Namespace) -> int:
    """执行设置低电量阈值操作"""
    try:
        # 验证阈值范围
        if args.threshold < 0 or args.threshold > 100:
            print(f"❌ 错误：阈值必须在 0-100 之间，当前值为 {args.threshold}", file=sys.stderr)
            return 1
        
        print(f"正在设置低电量阈值为 {args.threshold}% (Dev.LowElectrMode)...")
        print()
        print("⚠️  设置后:")
        print(f"   - 当设备电量低于 {args.threshold}% 时，自动进入低电量模式")
        print("   - 低电量模式下设备功能可能受限")
        print()
        
        result = set_low_elect_threshold(
            device_token=args.device_token,
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            threshold=args.threshold
        )
        
        print("✅ 低电量阈值设置成功")
        print(f"   设备：{args.device_sn}")
        print(f"   新阈值：{args.threshold}%")
        print(f"   来源：Dev.LowElectrMode.PowerThreshold")
        if result.get('SessionID'):
            print(f"   会话 ID: {result.get('SessionID')}")
        print()
        print("💡 提示：设备将在电量低于设定值时自动进入低电量模式")
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="杰峰低功耗设备电池管理技能")
    
    # 全局参数
    parser.add_argument("--action", required=True,
                        choices=["get-range", "set-threshold", "get-and-set"],
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
    
    # 操作特定参数
    parser.add_argument("--threshold", type=int,
                        help="低电量阈值（0-100）")
    
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
    
    # 验证需要 threshold 参数的操作
    if args.action in ["set-threshold", "get-and-set"]:
        if args.threshold is None:
            print(f"❌ 错误：{args.action} 操作需要 --threshold 参数", file=sys.stderr)
            return 1
    
    # 执行对应操作
    if args.action == "get-range":
        return get_range_action(args)
    elif args.action == "set-threshold":
        return set_threshold_action(args)
    elif args.action == "get-and-set":
        return get_and_set_action(args)
    else:
        print(f"❌ 未知操作：{args.action}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
