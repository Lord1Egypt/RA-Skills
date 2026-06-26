#!/usr/bin/env python3
"""
老张 API 图片生成脚本
使用方法：python generate_image.py "提示词" [--model 模型] [--ratio 2:3|3:2|1:1] [--output 输出路径]
"""

import argparse
import json
import re
import sys
import base64
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("需要安装 requests 库：pip install requests")
    sys.exit(1)

API_URL = "https://api.laozhang.ai/v1/chat/completions"

MODELS = {
    "sora_image": ("Sora Image", "$0.01/张", "url"),
    "gpt-4o-image": ("GPT-4o Image", "$0.01/张", "url"),
    "gemini-2.5-flash-image": ("Nano Banana", "$0.025/张", "base64"),
    "gemini-3.1-flash-image-preview": ("Nano Banana2", "$0.03/张", "base64"),
    "gemini-3-pro-image-preview": ("Nano Banana Pro", "$0.05/张", "base64"),
}

DEFAULT_MODEL = "gemini-3.1-flash-image-preview"
TOKEN_PATH = Path.home() / ".laozhang_api_token"
OUTPUT_DIR = Path.home() / "Pictures" / "laozhang"


def get_token():
    if TOKEN_PATH.exists():
        return TOKEN_PATH.read_text().strip()
    return None


def generate_filename(prompt: str, ratio: str = None) -> str:
    date = datetime.now().strftime("%Y%m%d_%H%M%S")
    keywords = "".join(c for c in prompt[:20] if c.isalnum() or c in " -_").strip().replace(" ", "-")
    ratio_s = f"_{ratio.replace(':', 'x')}" if ratio else ""
    return f"{date}_{keywords}{ratio_s}.png"


def generate(prompt: str, token: str, model: str = None, ratio: str = None, verbose: bool = False):
    model = model or DEFAULT_MODEL
    model_name, price, return_type = MODELS.get(model, ("Unknown", "?", "url"))

    if model == "sora_image" and ratio:
        prompt = f"{prompt}【{ratio}】"

    if verbose:
        print(f"📝 提示词: {prompt}")
        print(f"🤖 模型: {model_name} ({price})")
        if ratio:
            print(f"📐 比例: {ratio}")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        result = resp.json()

        content = result['choices'][0]['message']['content']

        # 处理返回内容
        images = []

        # 提取 Markdown 图片链接
        urls = re.findall(r'!\[.*?\]\((https?://[^)]+)\)', content)
        for url in urls:
            images.append(("url", url))

        # 如果没有找到 URL，可能返回的是 base64
        if not images and return_type == "base64":
            # 尝试从内容中提取 base64
            b64_match = re.search(r'data:image/[^;]+;base64,([A-Za-z0-9+/=]+)', content)
            if b64_match:
                images.append(("base64", b64_match.group(1)))
            elif re.match(r'^[A-Za-z0-9+/=]+$', content.strip()[:100]):
                # 整个内容可能就是 base64
                images.append(("base64", content.strip()))

        if verbose and images:
            print(f"✅ 生成 {len(images)} 张图片")

        return images, result

    except requests.exceptions.RequestException as e:
        print(f"❌ API 调用失败: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"响应: {e.response.text[:500]}")
        return [], None


def save_image(img_type: str, data: str, output: Path):
    output.parent.mkdir(parents=True, exist_ok=True)

    if img_type == "url":
        resp = requests.get(data, timeout=30)
        resp.raise_for_status()
        output.write_bytes(resp.content)
    else:
        # base64
        output.write_bytes(base64.b64decode(data))

    print(f"💾 已保存: {output}")


def main():
    parser = argparse.ArgumentParser(description="老张 API 图片生成")
    parser.add_argument("prompt", help="图片描述")
    parser.add_argument("-m", "--model", choices=list(MODELS.keys()), help=f"模型（默认: {DEFAULT_MODEL}）")
    parser.add_argument("-r", "--ratio", choices=["2:3", "3:2", "1:1"], help="比例（仅 sora_image）")
    parser.add_argument("-o", "--output", type=Path, help="保存路径")
    parser.add_argument("-t", "--token", help="API token")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细信息")
    parser.add_argument("--json", action="store_true", help="输出完整JSON")
    parser.add_argument("--no-save", action="store_true", help="不保存图片")

    args = parser.parse_args()

    token = args.token or get_token()
    if not token:
        print(f"❌ 未找到 token。请创建 {TOKEN_PATH} 或使用 --token")
        sys.exit(1)

    images, result = generate(args.prompt, token, args.model, args.ratio, args.verbose)

    if not images:
        print("❌ 未能生成图片")
        sys.exit(1)

    for i, (img_type, data) in enumerate(images, 1):
        if img_type == "url":
            print(f"🖼️  图片 {i}: {data}")
        else:
            print(f"🖼️  图片 {i}: [base64, {len(data)} 字符]")

        if not args.no_save and i == 1:
            output = args.output or OUTPUT_DIR / generate_filename(args.prompt, args.ratio)
            save_image(img_type, data, output)

    if args.json and result:
        print("\n📄 完整响应:")
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
