#!/usr/bin/env python3
"""
可灵图像扩图脚本
智能扩展图像边界
"""

import os
import sys
import json
import time
import base64
import argparse
import requests
import math
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


def calculate_expansion_ratios(width: int, height: int, area_multiplier: float, aspect_ratio: float):
    """
    计算图片外围扩展区域的上下左右比例
    
    参数:
    - width: 原始图片宽度
    - height: 原始图片高度
    - area_multiplier: 外围区域面积是原图的倍数
    - aspect_ratio: 外围区域的宽高比（width/height）
    
    返回:
    - (up_ratio, down_ratio, left_ratio, right_ratio)
    """
    # 计算目标总面积
    target_area = area_multiplier * width * height
    
    # 计算目标高度和宽度（保持宽高比）
    target_height = math.sqrt(target_area / aspect_ratio)
    target_width = target_height * aspect_ratio
    
    # 计算扩展像素
    expand_top = (target_height - height) / 2
    expand_bottom = expand_top
    expand_left = (target_width - width) / 2
    expand_right = expand_left
    
    # 计算相对比例
    top_ratio = expand_top / height
    bottom_ratio = expand_bottom / height
    left_ratio = expand_left / width
    right_ratio = expand_right / width
    
    return round(top_ratio, 4), round(bottom_ratio, 4), round(left_ratio, 4), round(right_ratio, 4)


def create_expansion_task(
    access_key: str,
    secret_key: str,
    image: str,
    up_expansion_ratio: float,
    down_expansion_ratio: float,
    left_expansion_ratio: float,
    right_expansion_ratio: float,
    prompt: str = None,
    n: int = 1,
    watermark_info: dict = None,
    callback_url: str = None,
    external_task_id: str = None
):
    """创建扩图任务"""
    
    token = generate_jwt_token(access_key, secret_key)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "image": image,
        "up_expansion_ratio": up_expansion_ratio,
        "down_expansion_ratio": down_expansion_ratio,
        "left_expansion_ratio": left_expansion_ratio,
        "right_expansion_ratio": right_expansion_ratio,
        "n": n
    }
    
    if prompt:
        data["prompt"] = prompt
    if watermark_info:
        data["watermark_info"] = watermark_info
    if callback_url:
        data["callback_url"] = callback_url
    if external_task_id:
        data["external_task_id"] = external_task_id
    
    url = f"{API_BASE}/v1/images/editing/expand"
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}", file=sys.stderr)
        if hasattr(e.response, 'text'):
            print(f"响应: {e.response.text}", file=sys.stderr)
        sys.exit(1)


def query_expansion_task(access_key: str, secret_key: str, task_id: str = None, external_task_id: str = None):
    """查询扩图任务状态"""
    
    if not task_id and not external_task_id:
        print("请提供 task_id 或 external_task_id", file=sys.stderr)
        sys.exit(1)
    
    token = generate_jwt_token(access_key, secret_key)
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    if task_id:
        url = f"{API_BASE}/v1/images/editing/expand/{task_id}"
    else:
        url = f"{API_BASE}/v1/images/editing/expand/{external_task_id}?external_task_id=true"
    
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
        result = query_expansion_task(access_key, secret_key, task_id)
        
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
    parser = argparse.ArgumentParser(description="可灵图像扩图工具")
    parser.add_argument("--image", required=True, help="参考图片URL或Base64")
    parser.add_argument("--up", type=float, required=True, help="向上扩展比例 [0,2]")
    parser.add_argument("--down", type=float, required=True, help="向下扩展比例 [0,2]")
    parser.add_argument("--left", type=float, required=True, help="向左扩展比例 [0,2]")
    parser.add_argument("--right", type=float, required=True, help="向右扩展比例 [0,2]")
    parser.add_argument("--prompt", help="提示词")
    parser.add_argument("--n", type=int, default=1, help="生成数量 [1,9]")
    parser.add_argument("--watermark", action="store_true", help="生成带水印图片")
    parser.add_argument("--callback_url", help="回调地址")
    parser.add_argument("--external_task_id", help="自定义任务ID")
    parser.add_argument("--wait", action="store_true", help="等待任务完成")
    parser.add_argument("--timeout", type=int, default=300, help="等待超时时间(秒)")
    parser.add_argument("--auto_ratio", action="store_true", help="使用自动计算扩展比例")
    parser.add_argument("--width", type=int, help="原图宽度（用于自动计算）")
    parser.add_argument("--height", type=int, help="原图高度（用于自动计算）")
    parser.add_argument("--area_multiplier", type=float, default=3.0, help="面积倍数（用于自动计算）")
    parser.add_argument("--aspect_ratio", type=float, default=16/9, help="目标宽高比（用于自动计算）")
    
    args = parser.parse_args()
    
    # 从环境变量获取密钥
    access_key = os.environ.get("KLING_ACCESS_KEY")
    secret_key = os.environ.get("KLING_SECRET_KEY")
    
    if not access_key or not secret_key:
        print("错误: 请设置环境变量 KLING_ACCESS_KEY 和 KLING_SECRET_KEY", file=sys.stderr)
        sys.exit(1)
    
    # 自动计算扩展比例
    if args.auto_ratio:
        if not args.width or not args.height:
            print("错误: 使用自动计算时需要提供 --width 和 --height", file=sys.stderr)
            sys.exit(1)
        up_ratio, down_ratio, left_ratio, right_ratio = calculate_expansion_ratios(
            args.width, args.height, args.area_multiplier, args.aspect_ratio
        )
        print(f"自动计算扩展比例: up={up_ratio}, down={down_ratio}, left={left_ratio}, right={right_ratio}")
    else:
        up_ratio = args.up
        down_ratio = args.down
        left_ratio = args.left
        right_ratio = args.right
    
    # 水印信息
    watermark_info = None
    if args.watermark:
        watermark_info = {"enabled": True}
    
    # 创建任务
    result = create_expansion_task(
        access_key=access_key,
        secret_key=secret_key,
        image=args.image,
        up_expansion_ratio=up_ratio,
        down_expansion_ratio=down_ratio,
        left_expansion_ratio=left_ratio,
        right_expansion_ratio=right_ratio,
        prompt=args.prompt,
        n=args.n,
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
