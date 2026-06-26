#!/usr/bin/env python3
"""
快代理 - 获取代理IP

Usage:
    python get_proxies.py --num 10 --format json
    python get_proxies.py --type dedicated --num 5 --area 北京
"""

import argparse
import os
import sys
import requests
from urllib.parse import urlencode

# API配置
API_BASE = "https://dev.kdlapi.com/api/getproxy"

# 代理类型端点
PROXY_TYPES = {
    "private": "https://dps.kdlapi.com/api/getdps/",  # 私密代理
    "dedicated": "https://dps.kdlapi.com/api/getdps/",  # 独享代理
    "tunnel": "https://tps.kdlapi.com/api/gettps/",  # 隧道代理
}


def get_proxies(
    secret_id: str = None,
    signature: str = None,
    proxy_type: str = "private",
    num: int = 10,
    format: str = "json",
    area: str = None,
    protocol: str = "http",
    sep: int = 1,
    order_id: str = None,
):
    """
    获取代理IP列表

    Args:
        secret_id: API密钥ID (或从环境变量KUAIDAILI_SECRET_ID读取)
        signature: API签名 (或从环境变量KUAIDAILI_SIGNATURE读取)
        proxy_type: 代理类型 (private/dedicated/tunnel)
        num: 获取数量
        format: 返回格式 (json/text)
        area: 地区筛选
        protocol: 协议类型
        sep: 分隔符 (1=\n, 2=\r, 3=空格)
        order_id: 订单号
    """
    # 从环境变量获取凭证
    secret_id = secret_id or os.environ.get("KUAIDAILI_SECRET_ID")
    signature = signature or os.environ.get("KUAIDAILI_SIGNATURE")

    if not secret_id or not signature:
        print("错误: 缺少API凭证", file=sys.stderr)
        print("请设置环境变量 KUAIDAILI_SECRET_ID 和 KUAIDAILI_SIGNATURE", file=sys.stderr)
        sys.exit(1)

    # 构建请求参数
    params = {
        "secret_id": secret_id,
        "signature": signature,
        "num": num,
        "format": format,
        "sep": sep,
    }

    if area:
        params["area"] = area
    if protocol:
        params["protocol"] = protocol
    if order_id:
        params["order_id"] = order_id

    # 选择API端点
    api_url = PROXY_TYPES.get(proxy_type, API_BASE)

    try:
        resp = requests.get(api_url, params=params, timeout=10)
        resp.raise_for_status()

        if format == "json":
            data = resp.json()
            if data.get("code") == 0:
                return data.get("data", {}).get("proxy_list", [])
            else:
                print(f"API错误: {data.get('msg')}", file=sys.stderr)
                sys.exit(1)
        else:
            return resp.text.strip().split("\n")

    except requests.RequestException as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="获取快代理IP")
    parser.add_argument("--secret-id", help="API密钥ID")
    parser.add_argument("--signature", help="API签名")
    parser.add_argument(
        "--type",
        choices=["private", "dedicated", "tunnel"],
        default="private",
        help="代理类型",
    )
    parser.add_argument("--num", type=int, default=10, help="获取数量")
    parser.add_argument("--format", choices=["json", "text"], default="json", help="返回格式")
    parser.add_argument("--area", help="地区筛选")
    parser.add_argument("--protocol", default="http", help="协议类型")
    parser.add_argument("--sep", type=int, default=1, help="分隔符")
    parser.add_argument("--order-id", help="订单号")

    args = parser.parse_args()

    proxies = get_proxies(
        secret_id=args.secret_id,
        signature=args.signature,
        proxy_type=args.type,
        num=args.num,
        format=args.format,
        area=args.area,
        protocol=args.protocol,
        sep=args.sep,
        order_id=args.order_id,
    )

    if args.format == "json":
        import json

        print(json.dumps(proxies, indent=2, ensure_ascii=False))
    else:
        for p in proxies:
            print(p)


if __name__ == "__main__":
    main()
