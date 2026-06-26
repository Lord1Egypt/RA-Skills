#!/usr/bin/env python3
"""
查询可灵图像生成任务状态
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


def query_task(access_key: str, secret_key: str, api_type: str, task_id: str = None, external_task_id: str = None):
    """查询单个任务状态"""
    
    if not task_id and not external_task_id:
        print("请提供 task_id 或 external_task_id", file=sys.stderr)
        sys.exit(1)
    
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
    
    if task_id:
        url = f"{API_BASE}{base_path}/{task_id}"
    else:
        url = f"{API_BASE}{base_path}/{external_task_id}?external_task_id=true"
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="查询可灵图像生成任务状态")
    parser.add_argument("--task_id", help="任务ID")
    parser.add_argument("--external_task_id", help="自定义任务ID")
    parser.add_argument("--api_type", default="generation",
                       choices=["generation", "omni", "expansion", "multishot", "tryon", "multi2image"],
                       help="API类型")
    
    args = parser.parse_args()
    
    # 从环境变量获取密钥
    access_key = os.environ.get("KLING_ACCESS_KEY")
    secret_key = os.environ.get("KLING_SECRET_KEY")
    
    if not access_key or not secret_key:
        print("错误: 请设置环境变量 KLING_ACCESS_KEY 和 KLING_SECRET_KEY", file=sys.stderr)
        sys.exit(1)
    
    result = query_task(
        access_key=access_key,
        secret_key=secret_key,
        api_type=args.api_type,
        task_id=args.task_id,
        external_task_id=args.external_task_id
    )
    
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
