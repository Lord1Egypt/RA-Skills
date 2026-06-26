#!/usr/bin/env python3
"""
可灵Omni图像生成脚本
支持多图参考、主体参考的高级图像生成
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


def create_omni_task(
    access_key: str,
    secret_key: str,
    model_name: str,
    prompt: str,
    image_list: list = None,
    element_list: list = None,
    resolution: str = "1k",
    result_type: str = "single",
    n: int = 1,
    series_amount: int = 4,
    aspect_ratio: str = "auto",
    watermark_info: dict = None,
    callback_url: str = None,
    external_task_id: str = None
):
    """创建Omni图像生成任务"""
    
    token = generate_jwt_token(access_key, secret_key)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model_name": model_name,
        "prompt": prompt,
        "resolution": resolution,
        "result_type": result_type,
        "aspect_ratio": aspect_ratio
    }
    
    if result_type == "single":
        data["n"] = n
    else:
        data["series_amount"] = series_amount
    
    if image_list:
        data["image_list"] = [{"image": img} for img in image_list]
    
    if element_list:
        data["element_list"] = [{"element_id": eid} for eid in element_list]
    
    if watermark_info:
        data["watermark_info"] = watermark_info
    
    if callback_url:
        data["callback_url"] = callback_url
    
    if external_task_id:
        data["external_task_id"] = external_task_id
    
    url = f"{API_BASE}/v1/images/omni-image"
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}", file=sys.stderr)
        if hasattr(e.response, 'text'):
            print(f"响应: {e.response.text}", file=sys.stderr)
        sys.exit(1)


def query_omni_task(access_key: str, secret_key: str, task_id: str = None, external_task_id: str = None):
    """查询Omni任务状态"""
    
    if not task_id and not external_task_id:
        print("请提供 task_id 或 external_task_id", file=sys.stderr)
        sys.exit(1)
    
    token = generate_jwt_token(access_key, secret_key)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    if task_id:
        url = f"{API_BASE}/v1/images/omni-image/{task_id}"
    else:
        url = f"{API_BASE}/v1/images/omni-image/{external_task_id}?external_task_id=true"
    
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
        result = query_omni_task(access_key, secret_key, task_id)
        
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
    parser = argparse.ArgumentParser(description="可灵Omni图像生成工具")
    parser.add_argument("--model", default="kling-v3-omni", 
                       choices=["kling-image-o1", "kling-v3-omni"],
                       help="模型名称")
    parser.add_argument("--prompt", required=True, help="提示词")
    parser.add_argument("--images", help="参考图片URL列表，逗号分隔")
    parser.add_argument("--elements", help="主体ID列表，逗号分隔")
    parser.add_argument("--resolution", default="1k", choices=["1k", "2k", "4k"], help="清晰度")
    parser.add_argument("--result_type", default="single", choices=["single", "series"], help="结果类型")
    parser.add_argument("--n", type=int, default=1, help="生成数量 [1,9] (single时有效)")
    parser.add_argument("--series_amount", type=int, default=4, help="组图数量 [2,9] (series时有效)")
    parser.add_argument("--aspect_ratio", default="auto", 
                       choices=["16:9", "9:16", "1:1", "4:3", "3:4", "3:2", "2:3", "21:9", "auto"],
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
    
    # 解析图片列表
    image_list = None
    if args.images:
        image_list = [img.strip() for img in args.images.split(",")]
    
    # 解析主体列表
    element_list = None
    if args.elements:
        element_list = [int(e.strip()) for e in args.elements.split(",")]
    
    # 水印信息
    watermark_info = None
    if args.watermark:
        watermark_info = {"enabled": True}
    
    # 创建任务
    result = create_omni_task(
        access_key=access_key,
        secret_key=secret_key,
        model_name=args.model,
        prompt=args.prompt,
        image_list=image_list,
        element_list=element_list,
        resolution=args.resolution,
        result_type=args.result_type,
        n=args.n,
        series_amount=args.series_amount,
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
