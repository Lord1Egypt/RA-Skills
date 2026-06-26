#!/usr/bin/env python3
"""
可灵图像生成脚本
支持文生图、图生图功能
"""

import os
import sys
import json
import time
import base64
import argparse
import requests
from datetime import datetime, timedelta
from jwt import JWT, jwk_from_dict

API_BASE = "https://api-beijing.klingai.com"


def generate_jwt_token(access_key: str, secret_key: str) -> str:
    """生成JWT鉴权Token"""
    jwt_instance = JWT()
    
    # 构建header
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }
    
    # 构建payload
    now = datetime.utcnow()
    payload = {
        "iss": access_key,
        "exp": int((now + timedelta(hours=1)).timestamp()),
        "nbf": int(now.timestamp()),
        "iat": int(now.timestamp())
    }
    
    # 使用secret_key作为HMAC密钥
    secret = jwk_from_dict({
        "kty": "oct",
        "k": base64.urlsafe_b64encode(secret_key.encode()).decode().rstrip('=')
    })
    
    token = jwt_instance.encode(payload, secret, alg='HS256', header=header)
    return token


def create_task(
    access_key: str,
    secret_key: str,
    model_name: str,
    prompt: str,
    negative_prompt: str = None,
    image: str = None,
    image_reference: str = None,
    image_fidelity: float = None,
    human_fidelity: float = None,
    element_list: list = None,
    resolution: str = "1k",
    n: int = 1,
    aspect_ratio: str = "16:9",
    watermark_info: dict = None,
    callback_url: str = None,
    external_task_id: str = None
):
    """创建图像生成任务"""
    
    token = generate_jwt_token(access_key, secret_key)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model_name": model_name,
        "prompt": prompt,
        "resolution": resolution,
        "n": n,
        "aspect_ratio": aspect_ratio
    }
    
    if negative_prompt:
        data["negative_prompt"] = negative_prompt
    if image:
        data["image"] = image
    if image_reference:
        data["image_reference"] = image_reference
    if image_fidelity is not None:
        data["image_fidelity"] = image_fidelity
    if human_fidelity is not None:
        data["human_fidelity"] = human_fidelity
    if element_list:
        data["element_list"] = [{"element_id": eid} for eid in element_list]
    if watermark_info:
        data["watermark_info"] = watermark_info
    if callback_url:
        data["callback_url"] = callback_url
    if external_task_id:
        data["external_task_id"] = external_task_id
    
    url = f"{API_BASE}/v1/images/generations"
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}", file=sys.stderr)
        if hasattr(e.response, 'text'):
            print(f"响应: {e.response.text}", file=sys.stderr)
        sys.exit(1)


def query_task(access_key: str, secret_key: str, task_id: str = None, external_task_id: str = None):
    """查询单个任务状态"""
    
    if not task_id and not external_task_id:
        print("请提供 task_id 或 external_task_id", file=sys.stderr)
        sys.exit(1)
    
    token = generate_jwt_token(access_key, secret_key)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    if task_id:
        url = f"{API_BASE}/v1/images/generations/{task_id}"
    else:
        url = f"{API_BASE}/v1/images/generations/{external_task_id}?external_task_id=true"
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}", file=sys.stderr)
        sys.exit(1)


def wait_for_completion(access_key: str, secret_key: str, task_id: str, timeout: int = 300):
    """等待任务完成"""
    print(f"等待任务完成，任务ID: {task_id}")
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        result = query_task(access_key, secret_key, task_id)
        
        if result.get("code") != 0:
            print(f"查询失败: {result.get('message')}", file=sys.stderr)
            return result
        
        task_data = result.get("data", {})
        status = task_data.get("task_status")
        
        print(f"当前状态: {status}")
        
        if status == "succeed":
            print("任务完成！")
            return result
        elif status == "failed":
            print(f"任务失败: {task_data.get('task_status_msg', '未知错误')}", file=sys.stderr)
            return result
        
        time.sleep(5)
    
    print("等待超时", file=sys.stderr)
    return result


def main():
    parser = argparse.ArgumentParser(description="可灵图像生成工具")
    parser.add_argument("--model", default="kling-v3", help="模型名称")
    parser.add_argument("--prompt", required=True, help="提示词")
    parser.add_argument("--negative_prompt", help="负向提示词")
    parser.add_argument("--image", help="参考图片URL或Base64")
    parser.add_argument("--image_reference", choices=["subject", "face"], help="图片参考类型")
    parser.add_argument("--image_fidelity", type=float, help="图片参考强度 [0,1]")
    parser.add_argument("--human_fidelity", type=float, help="面部参考强度 [0,1]")
    parser.add_argument("--elements", help="主体ID列表，逗号分隔")
    parser.add_argument("--resolution", default="1k", choices=["1k", "2k"], help="清晰度")
    parser.add_argument("--n", type=int, default=1, help="生成数量 [1,9]")
    parser.add_argument("--aspect_ratio", default="16:9", 
                       choices=["16:9", "9:16", "1:1", "4:3", "3:4", "3:2", "2:3", "21:9"],
                       help="宽高比")
    parser.add_argument("--watermark", action="store_true", help="生成带水印图片")
    parser.add_argument("--callback_url", help="回调地址")
    parser.add_argument("--external_task_id", help="自定义任务ID")
    parser.add_argument("--wait", action="store_true", help="等待任务完成")
    parser.add_argument("--timeout", type=int, default=300, help="等待超时时间(秒)")
    
    args = parser.parse_args()
    
    # 从环境变量获取密钥
    access_key = os.environ.get("KLING_ACCESS_KEY")
    secret_key = os.environ.get("KLING_SECRET_KEY")
    
    if not access_key or not secret_key:
        print("错误: 请设置环境变量 KLING_ACCESS_KEY 和 KLING_SECRET_KEY", file=sys.stderr)
        sys.exit(1)
    
    # 解析主体列表
    element_list = None
    if args.elements:
        element_list = [int(e.strip()) for e in args.elements.split(",")]
    
    # 水印信息
    watermark_info = None
    if args.watermark:
        watermark_info = {"enabled": True}
    
    # 创建任务
    result = create_task(
        access_key=access_key,
        secret_key=secret_key,
        model_name=args.model,
        prompt=args.prompt,
        negative_prompt=args.negative_prompt,
        image=args.image,
        image_reference=args.image_reference,
        image_fidelity=args.image_fidelity,
        human_fidelity=args.human_fidelity,
        element_list=element_list,
        resolution=args.resolution,
        n=args.n,
        aspect_ratio=args.aspect_ratio,
        watermark_info=watermark_info,
        callback_url=args.callback_url,
        external_task_id=args.external_task_id
    )
    
    if result.get("code") != 0:
        print(f"创建任务失败: {result.get('message')}", file=sys.stderr)
        sys.exit(1)
    
    task_data = result.get("data", {})
    task_id = task_data.get("task_id")
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # 等待任务完成
    if args.wait and task_id:
        final_result = wait_for_completion(access_key, secret_key, task_id, args.timeout)
        print(json.dumps(final_result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
