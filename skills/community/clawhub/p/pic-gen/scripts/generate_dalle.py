#!/usr/bin/env python3
"""
pic-gen: DALL-E 3 图片生成器
"""

import argparse
import os
import sys
import json
import time
import yaml
import requests

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
CONFIG_PATH = os.path.join(SKILL_DIR, "config", "models.yaml")


def load_config() -> dict:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    return {}


def get_api_key(config: dict) -> str:
    api_key = config.get("models", {}).get("dalle", {}).get("api_key", "")
    if not api_key:
        api_key = os.environ.get("OPENAI_API_KEY", "")
    return api_key


def generate_image(prompt: str, api_key: str = None,
                   size: str = "1024x1024", style: str = "vivid",
                   quality: str = "standard", n: int = 1,
                   download: bool = False, output: str = ".") -> dict:
    """
    调用 DALL-E 3 生成图片（仅支持英文提示词）
    """
    if not api_key:
        return {"error": "OpenAI API Key 未设置，请在 config/models.yaml 中配置 dalle.api_key"}

    url = "https://api.openai.com/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    size_map = {
        "1024x1024": "1024x1024",
        "1024x1792": "1024x1792",
        "1792x1024": "1792x1024",
    }
    actual_size = size_map.get(size, "1024x1024")

    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": n,
        "size": actual_size,
        "style": style,
        "quality": quality,
        "response_format": "url"
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)
        data = response.json()

        if response.status_code != 200:
            return {"error": f"请求失败 ({response.status_code}): {data}"}

        images = data.get("data", [])
        urls = [item["url"] for item in images if "url" in item]

        result = {"status": "succeeded", "images": urls, "model": "dall-e-3"}

        if download and urls:
            result["files"] = download_images(urls, output)

        return result

    except Exception as e:
        return {"error": f"生成失败: {str(e)}"}


def download_images(urls: list, output_dir: str) -> list:
    os.makedirs(output_dir, exist_ok=True)
    files = []
    for i, url in enumerate(urls):
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                ext = "png"
                filepath = os.path.join(output_dir, f"pic_gen_dalle_{int(time.time())}_{i+1}.{ext}")
                with open(filepath, "wb") as f:
                    f.write(resp.content)
                files.append(filepath)
        except Exception as e:
            files.append({"index": i, "error": str(e)})
    return files


import time


def main():
    parser = argparse.ArgumentParser(description="pic-gen DALL-E 3 图片生成")
    parser.add_argument("--prompt", "-p", required=True, help="图片提示词（建议英文）")
    parser.add_argument("--size", "-s", default="1024x1024",
                        choices=["1024x1024", "1024x1792", "1792x1024"],
                        help="图片尺寸")
    parser.add_argument("--style", default="vivid",
                        choices=["vivid", "natural"],
                        help="风格 vivid=鲜动 natural=自然")
    parser.add_argument("--quality", default="standard",
                        choices=["standard", "hd"],
                        help="质量 hd=更高细节")
    parser.add_argument("--count", "-c", type=int, default=1, help="生成数量（仅 dall-e-3 支持多张）")
    parser.add_argument("--download", "-d", action="store_true", help="下载图片")
    parser.add_argument("--output", "-o", default="./output", help="下载目录")
    parser.add_argument("--api-key", "-k", help="OpenAI API Key")
    args = parser.parse_args()

    config = load_config()
    api_key = args.api_key or get_api_key(config)

    result = generate_image(
        prompt=args.prompt,
        api_key=api_key,
        size=args.size,
        style=args.style,
        quality=args.quality,
        n=args.count,
        download=args.download,
        output=args.output
    )

    if "error" in result:
        print(f"❌ 错误: {result['error']}", file=sys.stderr)
        sys.exit(1)
    elif result.get("status") == "succeeded":
        for url in result.get("images", []):
            print(f"✅ 图片生成成功: {url}")
        for f in result.get("files", []):
            if isinstance(f, str):
                print(f"📁 已保存: {f}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
