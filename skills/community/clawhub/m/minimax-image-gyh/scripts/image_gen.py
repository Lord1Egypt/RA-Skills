#!/usr/bin/env python3
"""
MiniMax 图像生成脚本
"""

import os
import sys
import time
import argparse
import requests

API_KEY = os.environ.get("MINIMAX_API_KEY")
if not API_KEY:
    print("Error: MINIMAX_API_KEY environment variable not set")
    print("Please set it with: export MINIMAX_API_KEY=\"your-api-key\"")
    sys.exit(1)

HEADERS = {"Authorization": f"Bearer {API_KEY}"}
API_HOST = "https://api.minimaxi.com"


def generate_image(prompt: str, model: str = "image-01",
                   size: str = "1024x1024", n: int = 1,
                   output_path: str = "output.png") -> list:
    """调用 MiniMax 图像生成 API"""
    url = f"{API_HOST}/v1/image_generation"

    # size 映射
    size_map = {
        "1024x1024": "1:1",
        "1024x1792": "9:16",
        "1792x1024": "16:9",
        "1024x1536": "2:3",
        "1536x1024": "3:2",
    }
    aspect_ratio = size_map.get(size, "1:1")

    payload = {
        "model": model,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "num_images": n,
    }

    print(f"🖼️  正在生成图片...")
    print(f"   模型: {model} | 尺寸: {size} | 数量: {n}")
    print(f"   描述: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")

    resp = requests.post(url, headers=HEADERS, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()

    base_resp = data.get("base_resp", {})
    if base_resp.get("status_code") != 0:
        task_id = data.get("task_id")
        if task_id:
            print(f"⏳ 异步任务 ID: {task_id}，开始轮询...")
            image_urls = poll_image_task(task_id)
            if image_urls:
                download_images(image_urls, output_path)
                return image_urls
        raise Exception(f"API Error: {base_resp.get('status_msg', 'unknown')}")

    # 同步返回图片 URL 列表
    image_urls = data.get("image_urls", [])
    if image_urls:
        download_images(image_urls, output_path)
        return image_urls

    raise Exception("未获取到图片数据")


def poll_image_task(task_id: str, max_wait: int = 300) -> list:
    """轮询图像生成任务状态"""
    url = f"{API_HOST}/v1/query/image_generation"
    params = {"task_id": task_id}

    for i in range(max_wait // 10):
        time.sleep(10)
        resp = requests.get(url, headers=HEADERS, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        status = data.get("status", "")
        print(f"  状态: {status}")
        if status == "Success":
            return data.get("image_urls", [])
        elif status == "Fail":
            raise Exception(f"图片生成失败: {data.get('error_message', 'unknown')}")
    raise Exception("图片生成任务超时")


def download_images(image_urls: list, output_path: str):
    """下载图片"""
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    base, ext = os.path.splitext(output_path)

    for i, url in enumerate(image_urls):
        path = output_path if len(image_urls) == 1 else f"{base}_{i+1}{ext}"
        print(f"📥 下载图片: {path}")
        resp = requests.get(url, timeout=60)
        resp.raise_for_status()
        with open(path, "wb") as f:
            f.write(resp.content)
        print(f"✅ 已保存: {path}")


def main():
    parser = argparse.ArgumentParser(description="MiniMax 图像生成")
    parser.add_argument("--prompt", required=True, help="图片描述文本")
    parser.add_argument("--model", default="image-01", help="模型名称")
    parser.add_argument("--size", default="1024x1024",
                        help="尺寸: 1024x1024, 1024x1792, 1792x1024, 1024x1536, 1536x1024")
    parser.add_argument("--n", type=int, default=1, help="生成图片数量")
    parser.add_argument("--output", default="output.png", help="输出文件路径")

    args = parser.parse_args()

    try:
        urls = generate_image(
            prompt=args.prompt,
            model=args.model,
            size=args.size,
            n=args.n,
            output_path=args.output,
        )
        print(f"\n📎 输出文件: {args.output}")
    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
