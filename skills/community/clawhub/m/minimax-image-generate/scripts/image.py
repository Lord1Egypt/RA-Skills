#!/usr/bin/env python3
"""
MiniMax Image API Client
图片生成、图片编辑等功能
"""

import os
import json
import base64
import argparse
from typing import Optional, List, Dict, Any

import requests


# API 配置
BASE_URL_CN = "https://api.minimaxi.com/v1"
BASE_URL_INT = "https://api.minimax.io/v1"


def get_base_url() -> str:
    """获取 API 基础 URL"""
    return BASE_URL_CN if os.getenv("MINIMAX_REGION", "cn") == "cn" else BASE_URL_INT


def get_headers() -> Dict[str, str]:
    """获取请求头"""
    api_key = os.getenv("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("MINIMAX_API_KEY environment variable is not set")
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }


def generate_image(
    prompt: str,
    output_path: Optional[str] = None,
    aspect_ratio: str = "1:1",
    response_format: str = "url",
    model: str = "image-01"
) -> str:
    """
    文生图 - 根据文本描述生成图片并保存到本地

    Args:
        prompt: 图片描述文本
        output_path: 本地保存路径，如不提供则自动生成
        aspect_ratio: 宽高比 (1:1, 16:9, 9:16, 4:3, 3:4)
        response_format: 返回格式 (url, base64)
        model: 图片生成模型

    Returns:
        保存的本地文件路径
    """
    url = f"{get_base_url()}/image_generation"

    payload = {
        "model": model,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "response_format": response_format
    }

    response = requests.post(url, headers=get_headers(), json=payload, timeout=120)
    response.raise_for_status()

    result = response.json()
    data = result.get("data", {})

    if not data:
        raise ValueError("No image data returned")

    # 自动生成文件名
    if output_path is None:
        import uuid
        output_path = f"image_{uuid.uuid4().hex[:8]}.png"

    if response_format == "url":
        image_urls = data.get("image_urls", [])
        if image_urls:
            return download_image(image_urls[0], output_path)
        raise ValueError("No image URL in response")
    else:
        b64_jsons = data.get("b64_json", [])
        if b64_jsons:
            return save_base64_image(b64_jsons[0], output_path)
        raise ValueError("No base64 data in response")


def generate_image_from_image(
    prompt: str,
    output_path: Optional[str] = None,
    image_file: Optional[str] = None,
    image_url: Optional[str] = None,
    aspect_ratio: str = "1:1",
    response_format: str = "url",
    model: str = "image-01"
) -> str:
    """
    图生图 - 根据参考图和文本描述生成新图片并保存到本地

    Args:
        prompt: 图片修改描述
        output_path: 本地保存路径，如不提供则自动生成
        image_file: 参考图文件路径 (本地文件)
        image_url: 参考图URL
        aspect_ratio: 宽高比
        response_format: 返回格式
        model: 图片生成模型

    Returns:
        保存的本地文件路径
    """
    url = f"{get_base_url()}/image_generation"

    payload = {
        "model": model,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "response_format": response_format
    }

    # 添加参考图
    if image_url:
        payload["image_url"] = image_url
    elif image_file:
        # 读取并编码本地图片
        with open(image_file, "rb") as f:
            image_data = base64.b64encode(f.read()).decode("utf-8")
        # 从base64数据构建URL或直接传递
        ext = image_file.split(".")[-1].lower()
        mime_type = f"image/{ext}" if ext in ["jpg", "jpeg", "png", "gif", "webp"] else "image/jpeg"
        payload["image_url"] = f"data:{mime_type};base64,{image_data}"

    response = requests.post(url, headers=get_headers(), json=payload, timeout=120)
    response.raise_for_status()

    result = response.json()
    data = result.get("data", {})

    if not data:
        raise ValueError("No image data returned")

    # 自动生成文件名
    if output_path is None:
        import uuid
        output_path = f"image_{uuid.uuid4().hex[:8]}.png"

    if response_format == "url":
        image_urls = data.get("image_urls", [])
        if image_urls:
            return download_image(image_urls[0], output_path)
        raise ValueError("No image URL in response")
    else:
        b64_jsons = data.get("b64_json", [])
        if b64_jsons:
            return save_base64_image(b64_jsons[0], output_path)
        raise ValueError("No base64 data in response")


def download_image(image_url: str, output_path: str) -> str:
    """
    下载图片到本地

    Args:
        image_url: 图片URL
        output_path: 保存路径

    Returns:
        保存的文件路径
    """
    response = requests.get(image_url, timeout=60)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)

    return output_path


def save_base64_image(base64_data: str, output_path: str) -> str:
    """
    保存base64编码的图片

    Args:
        base64_data: base64编码的图片数据
        output_path: 保存路径

    Returns:
        保存的文件路径
    """
    # 移除可能的 data URI 前缀
    if "," in base64_data:
        base64_data = base64_data.split(",")[1]

    image_data = base64.b64decode(base64_data)

    with open(output_path, "wb") as f:
        f.write(image_data)

    return output_path


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(description="MiniMax Image API Client")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # 文生图命令
    gen_parser = subparsers.add_parser("generate", help="文生图")
    gen_parser.add_argument("prompt", help="图片描述")
    gen_parser.add_argument("-o", "--output", required=True, help="输出文件路径")
    gen_parser.add_argument("-r", "--ratio", default="1:1", help="宽高比")
    gen_parser.add_argument("-f", "--format", default="url", choices=["url", "base64"], help="返回格式")

    # 图生图命令
    img2img_parser = subparsers.add_parser("edit", help="图生图")
    img2img_parser.add_argument("prompt", help="图片修改描述")
    img2img_parser.add_argument("-i", "--image", help="参考图文件路径或URL")
    img2img_parser.add_argument("-o", "--output", required=True, help="输出文件路径")
    img2img_parser.add_argument("-r", "--ratio", default="1:1", help="宽高比")

    args = parser.parse_args()

    try:
        if args.command == "generate":
            output_path = generate_image(
                args.prompt,
                output_path=args.output,
                aspect_ratio=args.ratio,
                response_format=args.format
            )
            print(f"Image saved to: {output_path}")

        elif args.command == "edit":
            output_path = generate_image_from_image(
                args.prompt,
                output_path=args.output,
                image_url=args.image if args.image and args.image.startswith("http") else None,
                image_file=args.image if args.image and not args.image.startswith("http") else None,
                aspect_ratio=args.ratio
            )
            print(f"Image saved to: {output_path}")

        else:
            parser.print_help()

    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")
        print(e.response.text)
        raise


if __name__ == "__main__":
    main()
