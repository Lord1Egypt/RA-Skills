#!/usr/bin/env python3
"""
杰峰设备列表查询技能（开发版）

支持功能：
- 分页查询设备列表
- 按设备序列号条件查询
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


def query_device_list(uuid: str, app_key: str, app_secret: str, move_card: int,
                      page: int = 1, limit: int = 100) -> Dict[str, Any]:
    """
    分页查询设备列表
    
    API: POST /gwp/v3/rtc/device/list
    """
    url = f"{JF_BASE_URL}/rtc/device/list"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "page": page,
        "limit": limit
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"查询设备列表失败：{result.get('msg', '未知错误')}")
    
    return result.get("data", {})


def query_by_sns(uuid: str, app_key: str, app_secret: str, move_card: int,
                 sns: List[str]) -> Dict[str, Any]:
    """
    按设备序列号查询
    
    API: POST /gwp/v3/rtc/device/list
    """
    url = f"{JF_BASE_URL}/rtc/device/list"
    headers = get_headers(uuid, app_key, app_secret, move_card)
    
    body = {
        "sns": sns
    }
    
    response = requests.post(url, headers=headers, json=body, timeout=30)
    result = response.json()
    
    if result.get("code") != 2000:
        raise RuntimeError(f"查询设备列表失败：{result.get('msg', '未知错误')}")
    
    return result.get("data", {})


def load_sns_file(file_path: str) -> List[str]:
    """加载设备序列号列表文件"""
    sns_list = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            sns_list.append(line)
    
    return sns_list


def print_table(device_list: List[Dict[str, Any]]):
    """表格格式输出"""
    if not device_list:
        print("⚠️  无设备数据")
        return
    
    print()
    print("=" * 90)
    print(f"{'设备序列号':<22} {'用户名':<12} {'昵称':<20} {'Token':<30}")
    print("=" * 90)
    
    for device in device_list:
        sn = device.get("sn", "未知")[:20]
        username = device.get("username", "-")[:10]
        nickname = device.get("nickname", "-")[:18]
        token = device.get("loginToken", "-")
        
        if token and len(token) > 28:
            token = token[:25] + "..."
        
        print(f"{sn:<22} {username:<12} {nickname:<20} {token:<30}")
    
    print("=" * 90)
    print(f"📊 总计：{len(device_list)} 个设备")
    print()


def print_json(device_list: List[Dict[str, Any]]):
    """JSON 格式输出"""
    print(json.dumps(device_list, indent=2, ensure_ascii=False))


def print_simple(device_list: List[Dict[str, Any]]):
    """简洁格式输出"""
    if not device_list:
        print("⚠️  无设备数据")
        return
    
    print()
    for i, device in enumerate(device_list, 1):
        sn = device.get("sn", "未知")
        username = device.get("username", "-")
        nickname = device.get("nickname", "")
        
        nickname_text = f" ({nickname})" if nickname else ""
        print(f"{i}. 📱 {sn}{nickname_text}")
        print(f"   用户名：{username}")
        
        token = device.get("loginToken", "")
        if token:
            print(f"   Token: {token[:50]}...")
        print()
    
    print(f"📊 总计：{len(device_list)} 个设备")
    print()


# ============== 动作处理函数 ==============

def list_action(args: argparse.Namespace) -> int:
    """执行分页查询操作"""
    try:
        print(f"正在查询设备列表（第 {args.page} 页，每页 {args.limit} 个）...")
        
        result = query_device_list(
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            page=args.page,
            limit=args.limit
        )
        
        device_list = result.get("deviceList", [])
        
        # 根据格式输出
        if args.format == "json":
            print_json(device_list)
        elif args.format == "table":
            print_table(device_list)
        else:
            print_simple(device_list)
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def query_by_sns_action(args: argparse.Namespace) -> int:
    """执行按序列号查询操作"""
    try:
        # 加载设备序列号
        sns_list = []
        
        if args.sns_file:
            print(f"正在从文件加载设备序列号：{args.sns_file}")
            sns_list = load_sns_file(args.sns_file)
        elif args.sns:
            sns_list = [s.strip() for s in args.sns.split(',')]
        
        if not sns_list:
            print("❌ 设备序列号为空")
            return 1
        
        if len(sns_list) > 100:
            print(f"⚠️  设备序列号超过 100 个，只查询前 100 个")
            sns_list = sns_list[:100]
        
        print(f"正在查询 {len(sns_list)} 个设备...")
        
        result = query_by_sns(
            uuid=args.uuid,
            app_key=args.app_key,
            app_secret=args.app_secret,
            move_card=args.move_card,
            sns=sns_list
        )
        
        device_list = result.get("deviceList", [])
        
        # 根据格式输出
        if args.format == "json":
            print_json(device_list)
        elif args.format == "table":
            print_table(device_list)
        else:
            print_simple(device_list)
        
        return 0
        
    except RuntimeError as e:
        print(f"❌ 错误：{e}", file=sys.stderr)
        return 1


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="杰峰设备列表查询技能")
    
    # 全局参数
    parser.add_argument("--action", required=True,
                        choices=["list", "query-by-sns"],
                        help="操作类型")
    parser.add_argument("--uuid", default=os.getenv("JF_UUID"),
                        help="开放平台用户 uuid")
    parser.add_argument("--app-key", default=os.getenv("JF_APP_KEY"),
                        help="应用 appKey")
    parser.add_argument("--app-secret", default=os.getenv("JF_APP_SECRET"),
                        help="应用密钥")
    parser.add_argument("--move-card", type=int, default=os.getenv("JF_MOVE_CARD", "2"),
                        help="移动卡标识")
    parser.add_argument("--format", default="simple", choices=["simple", "table", "json"],
                        help="输出格式（simple=简洁，table=表格，json=JSON）")
    
    # list 参数
    parser.add_argument("--page", type=int, default=1,
                        help="页码（默认 1）")
    parser.add_argument("--limit", type=int, default=100,
                        help="每页数量（默认 100，最大 100）")
    
    # query-by-sns 参数
    parser.add_argument("--sns",
                        help="设备序列号列表（逗号分隔）")
    parser.add_argument("--sns-file",
                        help="设备序列号列表文件路径")
    
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
    if args.action == "query-by-sns":
        if not args.sns and not args.sns_file:
            print("❌ 错误：query-by-sns 需要 --sns 或 --sns-file 参数", file=sys.stderr)
            return 1
    
    # 执行对应操作
    if args.action == "list":
        return list_action(args)
    elif args.action == "query-by-sns":
        return query_by_sns_action(args)
    else:
        print(f"❌ 未知操作：{args.action}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
