#!/usr/bin/env python3
"""
获取可灵图像生成任务列表
"""

import os
import sys
import json
import base64
import argparse
import requests
from datetime import datetime, timedelta
from jwt import JWT, jwk_from_dict

API_BASE = "https://api-beijing.klingai.com"


def generate_jwt_token(access_key: str, secret_key: str) -> str:
    """生成JWT鉴权Token"""
    jwt_instance = JWT()
    
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    
    now = datetime.utcnow()
    payload = {
        "iss": access_key,
        "exp": int((now + timedelta(hours=1)).timestamp()),
        "nbf": int(now.timestamp()),
        "iat": int(now.timestamp())
    }
    
    secret = jwk_from_dict({
        "kty": "oct",
        "k": base64.urlsafe_b64encode(secret_key.encode()).decode().rstrip('=')
    })
    
    token = jwt_instance.encode(payload, secret, alg='HS256', header=header)
    return token


def list_tasks(access_key: str, secret_key: str, api_type: str, page_num: int = 1, page_size: int = 30):
    """获取任务列表"""
    
    token = generate_jwt_token(access_key, secret_key)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # API路径映射
    api_paths = {
        "generation": "/v1/images/generations",
        "omni": "/v1/images/omni-image",
        "expansion": "/v1/images/expansion",
        "multishot": "/v1/images/ai-multishot",
        "tryon": "/v1/images/virtual-try-on",
        "multi2image": "/v1/images/multi-image-to-image"
    }
    
    base_path = api_paths.get(api_type, "/v1/images/generations")
    url = f"{API_BASE}{base_path}?pageNum={page_num}&pageSize={page_size}"
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="获取可灵图像生成任务列表")
    parser.add_argument("--api_type", default="generation",
                       choices=["generation", "omni", "expansion", "multishot", "tryon", "multi2image"],
                       help="API类型")
    parser.add_argument("--page", type=int, default=1, help="页码 [1,1000]")
    parser.add_argument("--page_size", type=int, default=30, help="每页数量 [1,500]")
    
    args = parser.parse_args()
    
    # 从环境变量获取密钥
    access_key = os.environ.get("KLING_ACCESS_KEY")
    secret_key = os.environ.get("KLING_SECRET_KEY")
    
    if not access_key or not secret_key:
        print("错误: 请设置环境变量 KLING_ACCESS_KEY 和 KLING_SECRET_KEY", file=sys.stderr)
        sys.exit(1)
    
    result = list_tasks(
        access_key=access_key,
        secret_key=secret_key,
        api_type=args.api_type,
        page_num=args.page,
        page_size=args.page_size
    )
    
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
