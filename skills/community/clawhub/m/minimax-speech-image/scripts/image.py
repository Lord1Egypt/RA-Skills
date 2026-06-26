#!/usr/bin/env python3
"""MiniMax Image API Client"""
import os, base64, uuid, argparse
from typing import Optional, Dict, Any
import requests

BASE_URL_CN = "https://api.minimaxi.com/v1"
BASE_URL_INT = "https://api.minimax.io/v1"

def get_base_url() -> str:
    return BASE_URL_CN if os.getenv("MINIMAX_REGION", "cn") == "cn" else BASE_URL_INT

def get_headers() -> Dict[str, str]:
    api_key = os.getenv("MINIMAX_API_KEY")
    if not api_key:
        raise ValueError("MINIMAX_API_KEY environment variable is not set")
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

def generate_image(prompt: str, output_path: Optional[str] = None,
                   aspect_ratio: str = "1:1", response_format: str = "url",
                   model: str = "image-01") -> str:
    url = f"{get_base_url()}/image_generation"
    payload = {"model": model, "prompt": prompt,
               "aspect_ratio": aspect_ratio, "response_format": response_format}
    resp = requests.post(url, headers=get_headers(), json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json().get("data", {})
    if not data:
        raise ValueError("No image data returned")
    if output_path is None:
        output_path = f"image_{uuid.uuid4().hex[:8]}.png"
    # 兼容多种响应字段名：image_urls / url / b64_json
    if response_format == "url":
        urls = data.get("image_urls") or ([data.get("url")] if data.get("url") else [])
        if urls and urls[0]:
            return download_image(urls[0], output_path)
        raise ValueError(f"No image URL in response. Available keys: {list(data.keys())}")
    else:
        b64s = data.get("b64_json") or data.get("b64") or []
        if b64s and b64s[0]:
            return save_base64_image(b64s[0], output_path)
        raise ValueError(f"No base64 data in response. Available keys: {list(data.keys())}")

def generate_image_from_image(prompt: str, output_path: Optional[str] = None,
                             image_file: Optional[str] = None, image_url: Optional[str] = None,
                             aspect_ratio: str = "1:1", response_format: str = "url",
                             model: str = "image-01") -> str:
    if not image_url and not image_file:
        raise ValueError("Either image_url or image_file must be provided")
    url = f"{get_base_url()}/image_generation"
    payload = {"model": model, "prompt": prompt,
               "aspect_ratio": aspect_ratio, "response_format": response_format}
    if image_url:
        payload["image_url"] = image_url
    elif image_file:
        ext = image_file.lower().split(".")[-1]
        if ext not in ("jpg", "jpeg", "png", "gif", "webp"):
            raise ValueError(f"Unsupported image format: {ext}")
        with open(image_file, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode("utf-8")
        mime = f"image/{ext}" if ext != "jpg" else "image/jpeg"
        payload["image_url"] = f"data:{mime};base64,{img_b64}"
    resp = requests.post(url, headers=get_headers(), json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json().get("data", {})
    if not data:
        raise ValueError("No image data returned")
    if output_path is None:
        output_path = f"image_{uuid.uuid4().hex[:8]}.png"
    # 兼容多种响应字段名：image_urls / url / b64_json
    if response_format == "url":
        urls = data.get("image_urls") or ([data.get("url")] if data.get("url") else [])
        if urls and urls[0]:
            return download_image(urls[0], output_path)
        raise ValueError(f"No image URL in response. Available keys: {list(data.keys())}")
    else:
        b64s = data.get("b64_json") or data.get("b64") or []
        if b64s and b64s[0]:
            return save_base64_image(b64s[0], output_path)
        raise ValueError(f"No base64 data in response. Available keys: {list(data.keys())}")

def download_image(image_url: str, output_path: str) -> str:
    resp = requests.get(image_url, timeout=60)
    resp.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(resp.content)
    return output_path

def save_base64_image(base64_data: str, output_path: str) -> str:
    if "," in base64_data:
        base64_data = base64_data.split(",", 1)[1]
    with open(output_path, "wb") as f:
        f.write(base64.b64decode(base64_data))
    return output_path

def main():
    parser = argparse.ArgumentParser(description="MiniMax Image API Client")
    sub = parser.add_subparsers(dest="command", help="Available commands")
    p = sub.add_parser("generate", help="文生图")
    p.add_argument("prompt", help="图片描述")
    p.add_argument("-o", "--output", required=True, help="输出文件路径")
    p.add_argument("-r", "--ratio", default="1:1", help="宽高比")
    p.add_argument("-f", "--format", default="url", choices=["url", "base64"], help="返回格式")
    p = sub.add_parser("edit", help="图生图")
    p.add_argument("prompt", help="图片修改描述")
    p.add_argument("-i", "--image", required=True, help="参考图文件路径或URL")
    p.add_argument("-o", "--output", required=True, help="输出文件路径")
    p.add_argument("-r", "--ratio", default="1:1", help="宽高比")
    args = parser.parse_args()
    try:
        if args.command == "generate":
            path = generate_image(args.prompt, output_path=args.output,
                                 aspect_ratio=args.ratio, response_format=args.format)
            print(f"Image saved to: {path}")
        elif args.command == "edit":
            is_url = args.image.startswith("http")
            path = generate_image_from_image(args.prompt, output_path=args.output,
                                            image_url=args.image if is_url else None,
                                            image_file=args.image if not is_url else None,
                                            aspect_ratio=args.ratio)
            print(f"Image saved to: {path}")
        else:
            parser.print_help()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e.response.status_code}")
        print(e.response.text)
        raise

if __name__ == "__main__":
    main()
