#!/usr/bin/env python3
"""
可灵图像生成脚本（带进度估算）
支持文生图、图生图功能，带实时进度显示
"""

import os
import sys
import json
import time
import base64
import hmac
import hashlib
import argparse
import requests
from datetime import datetime, timedelta

API_BASE = "https://api-beijing.klingai.com"

# 任务类型平均耗时（秒）- 基于实际测试数据
TASK_ESTIMATED_TIME = {
    "text2image": 45,    # 文生图
    "image2image": 35,   # 图生图
    "omni": 60,          # Omni生成
    "expansion": 40,     # 扩图
}


def base64url_encode(data: bytes) -> str:
    """Base64URL编码"""
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode('ascii')


def generate_jwt_token(access_key: str, secret_key: str) -> str:
    """生成JWT鉴权Token"""
    now = int(time.time())
    
    header = json.dumps({"alg": "HS256", "typ": "JWT"}, separators=(',', ':'))
    header_b64 = base64url_encode(header.encode())
    
    payload = json.dumps({
        "iss": access_key,
        "iat": now,
        "nbf": now - 60,
        "exp": now + 3600
    }, separators=(',', ':'))
    payload_b64 = base64url_encode(payload.encode())
    
    message = f"{header_b64}.{payload_b64}"
    signature = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()
    signature_b64 = base64url_encode(signature)
    
    return f"{message}.{signature_b64}"


def get_auth_headers(access_key: str, secret_key: str):
    """获取认证头"""
    token = generate_jwt_token(access_key, secret_key)
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }


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
    
    headers = get_auth_headers(access_key, secret_key)
    
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
        response = requests.post(url, headers=headers, json=data, timeout=60)
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
    
    headers = get_auth_headers(access_key, secret_key)
    
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


def format_time(seconds: int) -> str:
    """格式化时间"""
    if seconds < 60:
        return f"{seconds}秒"
    else:
        return f"{seconds // 60}分{seconds % 60}秒"


def print_progress_bar(progress: float, width: int = 30):
    """打印进度条"""
    filled = int(width * progress)
    empty = width - filled
    bar = "█" * filled + "░" * empty
    percentage = int(progress * 100)
    print(f"\r[{bar}] {percentage}%", end="", flush=True)


def wait_with_progress(
    access_key: str,
    secret_key: str,
    task_id: str,
    task_type: str = "text2image",
    timeout: int = 300,
    poll_interval: int = 3
):
    """
    等待任务完成并显示进度
    
    参数:
    - task_type: 任务类型，用于估算时间 (text2image/image2image/omni/expansion)
    """
    estimated_total = TASK_ESTIMATED_TIME.get(task_type, 45)
    
    print(f"\n{'='*50}")
    print(f"任务ID: {task_id}")
    print(f"任务类型: {task_type}")
    print(f"预计耗时: {format_time(estimated_total)}")
    print(f"{'='*50}\n")
    
    start_time = time.time()
    last_status = None
    status_start_time = start_time
    
    while time.time() - start_time < timeout:
        result = query_task(access_key, secret_key, task_id)
        
        if result.get("code") != 0:
            print(f"\n❌ 查询失败: {result.get('message')}")
            return result
        
        task_data = result.get("data", {})
        status = task_data.get("task_status")
        current_time = time.time()
        elapsed = int(current_time - start_time)
        
        # 状态变更时更新计时
        if status != last_status:
            if last_status is not None:
                status_duration = int(current_time - status_start_time)
                print(f"  (耗时: {format_time(status_duration)})")
            status_start_time = current_time
            last_status = status
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 状态: {status.upper()}")
        
        # 计算进度
        if status == "submitted":
            # 已提交阶段：0-10%
            progress = min(0.1, elapsed / 10)
            remaining = estimated_total - elapsed
            print_progress_bar(progress)
            print(f" 等待处理... 已等待 {format_time(elapsed)}", end="")
            
        elif status == "processing":
            # 处理中阶段：10-90%
            processing_time = current_time - status_start_time
            # 假设处理占预计时间的70%
            process_progress = min(0.8, processing_time / (estimated_total * 0.7))
            progress = 0.1 + process_progress * 0.8
            remaining = max(0, estimated_total - elapsed)
            print_progress_bar(progress)
            print(f" 处理中... 预计还需 {format_time(int(remaining))}", end="")
            
        elif status == "succeed":
            print_progress_bar(1.0)
            print(f"\n\n{'='*50}")
            print("✅ 任务完成！")
            print(f"总耗时: {format_time(elapsed)}")
            print(f"{'='*50}")
            return result
            
        elif status == "failed":
            print(f"\n\n{'='*50}")
            print("❌ 任务失败")
            print(f"失败原因: {task_data.get('task_status_msg', '未知错误')}")
            print(f"{'='*50}")
            return result
        
        time.sleep(poll_interval)
    
    print(f"\n\n{'='*50}")
    print("⏱️ 等待超时")
    print(f"{'='*50}")
    return result


def main():
    parser = argparse.ArgumentParser(description="可灵图像生成工具（带进度估算）")
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
    parser.add_argument("--wait", action="store_true", help="等待任务完成并显示进度")
    parser.add_argument("--timeout", type=int, default=300, help="等待超时时间(秒)")
    parser.add_argument("--poll_interval", type=int, default=3, help="轮询间隔(秒)")
    
    args = parser.parse_args()
    
    # 从环境变量获取密钥
    access_key = os.environ.get("KLING_ACCESS_KEY")
    secret_key = os.environ.get("KLING_SECRET_KEY")
    
    if not access_key or not secret_key:
        print("错误: 请设置环境变量 KLING_ACCESS_KEY 和 KLING_SECRET_KEY", file=sys.stderr)
        print("\n示例:", file=sys.stderr)
        print("  export KLING_ACCESS_KEY='your_access_key'", file=sys.stderr)
        print("  export KLING_SECRET_KEY='your_secret_key'", file=sys.stderr)
        sys.exit(1)
    
    # 解析主体列表
    element_list = None
    if args.elements:
        element_list = [int(e.strip()) for e in args.elements.split(",")]
    
    # 水印信息
    watermark_info = None
    if args.watermark:
        watermark_info = {"enabled": True}
    
    # 判断任务类型
    if args.image:
        task_type = "image2image"
    else:
        task_type = "text2image"
    
    print(f"🎨 正在创建图像生成任务...")
    print(f"   模型: {args.model}")
    print(f"   类型: {'图生图' if args.image else '文生图'}")
    print(f"   提示: {args.prompt[:50]}{'...' if len(args.prompt) > 50 else ''}")
    
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
        print(f"\n❌ 创建任务失败: {result.get('message')}", file=sys.stderr)
        sys.exit(1)
    
    task_data = result.get("data", {})
    task_id = task_data.get("task_id")
    
    print(f"\n✅ 任务创建成功！")
    print(f"   任务ID: {task_id}")
    print(f"   初始状态: {task_data.get('task_status')}")
    
    # 等待任务完成并显示进度
    if args.wait and task_id:
        final_result = wait_with_progress(
            access_key=access_key,
            secret_key=secret_key,
            task_id=task_id,
            task_type=task_type,
            timeout=args.timeout,
            poll_interval=args.poll_interval
        )
        
        # 输出最终结果
        if final_result.get("code") == 0:
            task_data = final_result.get("data", {})
            if task_data.get("task_status") == "succeed":
                images = task_data.get("task_result", {}).get("images", [])
                print(f"\n📸 生成结果 ({len(images)} 张):")
                for i, img in enumerate(images):
                    print(f"   [{i+1}] {img.get('url', 'N/A')[:80]}...")
        
        print("\n完整结果:")
        print(json.dumps(final_result, indent=2, ensure_ascii=False))
    else:
        print("\n使用以下命令查询进度:")
        print(f"  python3 scripts/query_task.py --task_id {task_id}")


if __name__ == "__main__":
    main()
