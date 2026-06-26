#!/usr/bin/env python3
"""
Ollama 文生图工具
分辨率: 1024x1024，每张图约耗时 90 秒
模型: x/z-image-turbo
"""

import argparse
import base64
import os
import random
import time
from datetime import datetime

import requests


def save_to_image_file(file_name: str, data: str) -> None:
    """将 base64 数据保存为图片文件"""
    image_data = base64.b64decode(data)
    with open(file_name, "wb") as f:
        f.write(image_data)
    print(f"✅ 成功！图片已保存为: {file_name}")
    print(f"📏 文件大小: {len(data)} 字节")


def ollama_t2i(prompt: str, output_dir: str = "images") -> str:
    """
    使用 Ollama 本地模型生成图片

    Args:
        prompt: 中文提示词
        output_dir: 输出目录

    Returns:
        保存的文件路径
    """
    os.makedirs(output_dir, exist_ok=True)

    start_time = time.perf_counter()

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "x/z-image-turbo",
            "prompt": prompt,
            "stream": False,
        },
        timeout=180,  # 180 秒超时，覆盖 90 秒生图时间
    )

    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"✅ 请求成功！总耗时: {duration:.4f} 秒（约 {duration/60:.1f} 分钟）")

    resp_json = response.json()

    if "error" not in resp_json:
        now = datetime.now().strftime("%Y-%m-%d_%H-%M")
        file_name = os.path.join(
            output_dir,
            f"{now}_image_{random.randint(0, 10000000)}.png",
        )
        save_to_image_file(file_name, resp_json["image"])
        return file_name
    else:
        raise Exception(resp_json["error"])


def main():
    parser = argparse.ArgumentParser(description="Ollama 本地文生图工具")
    parser.add_argument("prompts", nargs="+", help="中文提示词（支持多个）")
    parser.add_argument(
        "--output", "-o", default="images", help="输出目录（默认: images）"
    )
    args = parser.parse_args()

    for i, prompt in enumerate(args.prompts, 1):
        print(f"\n{'='*50}")
        print(f"🖼️  生成第 {i}/{len(args.prompts)} 张图片...")
        print(f"📝 提示词: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")
        try:
            path = ollama_t2i(prompt, args.output)
            print(f"📁 输出: {path}")
        except Exception as e:
            print(f"❌ 生成失败: {e}")


if __name__ == "__main__":
    main()
