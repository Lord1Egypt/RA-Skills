#!/usr/bin/env python3
"""
杰峰设备在线状态查询技能（开发版）

专注于查询设备是否在线，支持单设备或批量查询。
保留低功耗设备唤醒状态显示。
"""

import os
import sys
import argparse
import requests
import json
from typing import Optional, Dict, Any, List

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


def query_device_status(device_tokens: List[str], uuid: str, app_key: str,
                        app_secret: str, move_card: int,
                        region: str = "Local") -> List[Dict[str, Any]]:
    """
    查询设备在线状态
    
    API: POST /gwp/v3/rtc/device/status
    """
    url = f"{JF_BASE_URL}/rtc/device/status"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "deviceTokenList": device_tokens,
        "region": region
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"查询设备状态失败：{result.get('msg', '未知错误')}")
    
    return result.get("data", [])


def load_tokens_file(file_path: str) -> List[str]:
    """加载设备 Token 列表文件"""
    tokens = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            tokens.append(line)
    
    return tokens


def format_wake_status(wake_status: str, wake_enable: str) -> str:
    """格式化低功耗设备唤醒状态"""
    if not wake_status:
        return "-"
    
    if wake_status == "0" and wake_enable == "0":
        return "💤 深度休眠"
    elif wake_status == "0":
        return "💤 已休眠"
    elif wake_status == "1":
        return "✅ 已唤醒"
    elif wake_status == "2":
        return "⏳ 准备休眠"
    
    return wake_status


def print_simple(devices: List[Dict[str, Any]]):
    """简洁格式：显示在线/离线和唤醒状态"""
    if not devices:
        print("⚠️  无设备数据")
        return
    
    online_count = 0
    offline_count = 0
    sleep_count = 0
    
    for device in devices:
        uuid = device.get("uuid", "未知")
        status = device.get("status", "unknown")
        wake_status = device.get("wakeUpStatus", "")
        wake_enable = device.get("wakeUpEnable", "")
        
        if status == "online":
            if wake_status:
                wake_text = format_wake_status(wake_status, wake_enable)
                print(f"🟢 {uuid}: 在线 ({wake_text})")
                if wake_status == "0":
                    sleep_count += 1
            else:
                print(f"🟢 {uuid}: 在线")
            online_count += 1
        else:
            print(f"🔴 {uuid}: 离线")
            offline_count += 1
    
    print()
    print(f"📊 统计：在线 {online_count} 个 | 离线 {offline_count} 个", end="")
    if sleep_count > 0:
        print(f" | 休眠 {sleep_count} 个", end="")
    print(f" | 总计 {len(devices)} 个")


def print_table(devices: List[Dict[str, Any]]):
    """表格格式：显示设备列表和统计"""
    if not devices:
        print("⚠️  无设备数据")
        return
    
    print()
    print("=" * 70)
    print(f"{'设备序列号':<20} {'状态':<12} {'唤醒状态':<15} {'外网 IP':<18}")
    print("=" * 70)
    
    online_count = 0
    offline_count = 0
    sleep_count = 0
    
    for device in devices:
        uuid = device.get("uuid", "未知")[:18]
        status = device.get("status", "")
        status_text = "🟢 在线" if status == "online" else "🔴 离线"
        
        wake_status = device.get("wakeUpStatus", "")
        wake_enable = device.get("wakeUpEnable", "")
        wake_text = format_wake_status(wake_status, wake_enable)
        
        wan_ip = device.get("wanIp", "-")
        if wan_ip and len(wan_ip) > 15:
            wan_ip = wan_ip[:15] + "..."
        
        print(f"{uuid:<20} {status_text:<12} {wake_text:<15} {wan_ip:<18}")
        
        if status == "online":
            online_count += 1
            if wake_status == "0":
                sleep_count += 1
        else:
            offline_count += 1
    
    print("=" * 70)
    print(f"📊 统计：在线 {online_count} 个 | 离线 {offline_count} 个", end="")
    if sleep_count > 0:
        print(f" | 休眠 {sleep_count} 个", end="")
    print(f" | 总计 {len(devices)} 个")
    print()


def print_json(devices: List[Dict[str, Any]]):
    """JSON 格式输出"""
    # 简化输出，保留必要字段
    simplified = []
    for device in devices:
        item = {
            "uuid": device.get("uuid", ""),
            "status": "online" if device.get("status") == "online" else "offline"
        }
        
        # 保留低功耗设备状态
        wake_status = device.get("wakeUpStatus", "")
        wake_enable = device.get("wakeUpEnable", "")
        if wake_status:
            item["wakeUpStatus"] = wake_status
            item["wakeUpEnable"] = wake_enable
        
        simplified.append(item)
    
    print(json.dumps(simplified, indent=2, ensure_ascii=False))


# ============== 动作处理函数 ==============

def query_action(args: argparse.Namespace) -> int:
    """执行单设备查询操作"""
    try:
        devices = query_device_status(
            device_tokens=[args.device_token],
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            region=args.region
        )
        
        if not devices:
            print("⚠️  未查询到设备数据")
            return 1
        
        # 根据格式输出
        if args.format == "json":
            print_json(devices)
        elif args.format == "table":
            print_table(devices)
        else:
            print_simple(devices)
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def batch_query_action(args: argparse.Namespace) -> int:
    """执行批量查询操作"""
    try:
        # 加载设备 Token 列表
        tokens = load_tokens_file(args.tokens_file)
        
        if not tokens:
            print(f"❌ 设备 Token 列表为空")
            return 1
        
        # 分批查询（每批最多 500 个）
        batch_size = 500
        all_devices = []
        
        for i in range(0, len(tokens), batch_size):
            batch_tokens = tokens[i:i + batch_size]
            devices = query_device_status(
                device_tokens=batch_tokens,
                uuid=args.uuid,
                app_key=args.app_key,
                app_secret=args.app_secret,
                move_card=args.move_card,
                region=args.region
            )
            all_devices.extend(devices)
        
        # 根据格式输出
        if args.format == "json":
            print_json(all_devices)
        elif args.format == "table":
            print_table(all_devices)
        else:
            print_simple(all_devices)
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="杰峰设备在线状态查询技能")
    
    # 全局参数
    parser.add_argument("--action", required=True,
                        choices=["query", "batch-query"],
                        help="操作类型")
    parser.add_argument("--uuid", default=os.getenv("JF_UUID"),
                        help="开放平台用户 uuid")
    parser.add_argument("--app-key", default=os.getenv("JF_APP_KEY"),
                        help="应用 appKey")
    parser.add_argument("--app-secret", default=os.getenv("JF_APP_SECRET"),
                        help="应用密钥")
    parser.add_argument("--move-card", type=int, default=os.getenv("JF_MOVE_CARD", "2"),
                        help="移动卡标识")
    parser.add_argument("--region", default="Local", choices=["Local", "Global"],
                        help="查询区域（Local=当前区域，Global=全球）")
    parser.add_argument("--format", default="simple", choices=["simple", "table", "json"],
                        help="输出格式（simple=简洁，table=表格，json=JSON）")
    
    # query 参数
    parser.add_argument("--device-token",
                        help="设备接口访问令牌")
    
    # batch-query 参数
    parser.add_argument("--tokens-file",
                        help="设备 Token 列表文件路径")
    
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
    
    # 特定操作验证
    if args.action == "query" and not args.device_token:
        print("❌ 错误：query 需要 --device-token 参数", file=sys.stderr)
        return 1
    if args.action == "batch-query" and not args.tokens_file:
        print("❌ 错误：batch-query 需要 --tokens-file 参数", file=sys.stderr)
        return 1
    
    # 执行对应操作
    if args.action == "query":
        return query_action(args)
    elif args.action == "batch-query":
        return batch_query_action(args)
    else:
        print(f"❌ 未知操作：{args.action}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
