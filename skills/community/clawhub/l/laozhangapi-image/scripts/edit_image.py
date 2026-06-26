#!/usr/bin/env python3
"""
老张 API 图片编辑脚本
使用方法：python edit_image.py "图片URL" "编辑描述" [--style 风格] [--model 模型]
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
    "gpt-4o-image": ("GPT-4o Image", "$0.01/张", "url"),
    "sora_image": ("Sora Image", "$0.01/张", "url"),
    "gemini-2.5-flash-image": ("Nano Banana", "$0.025/张", "base64"),
    "gemini-3.1-flash-image-preview": ("Nano Banana2", "$0.03/张", "base64"),
    "gemini-3-pro-image-preview": ("Nano Banana Pro", "$0.05/张", "base64"),
}

DEFAULT_MODEL = "gpt-4o-image"
TOKEN_PATH = Path.home() / ".laozhang_api_token"
OUTPUT_DIR = Path.home() / "Pictures" / "laozhang"

STYLES = {
    "卡通": "转换成迪士尼卡通风格，色彩鲜艳",
    "油画": "转换成古典油画风格，如梵高画风",
    "水墨": "转换成中国水墨画风格，留白意境",
    "赛博朋克": "转换成赛博朋克风格，霓虹灯光效果",
    "素描": "转换成铅笔素描风格，黑白线条",
    "水彩": "转换成水彩画风格，透明感，色彩流动"
}


def get_token():
    if TOKEN_PATH.exists():
        return TOKEN_PATH.read_text().strip()
    return None


def generate_filename(prompt: str, suffix: str = ""):
    date = datetime.now().strftime("%Y-%m-%d")
    keywords = "".join(c for c in prompt[:15] if c.isalnum() or c in " -_").strip()
    keywords = keywords.replace(" ", "-")
    return f"{date}-edit-{keywords}{suffix}.png"


def edit(image_urls: list, prompt: str, token: str, model: str = None, verbose: bool = False):
    model = model or DEFAULT_MODEL
    model_name, price, return_type = MODELS.get(model, ("Unknown", "?", "url"))

    if verbose:
        print(f"📝 编辑提示: {prompt}")
        print(f"🖼️  输入: {len(image_urls)} 张图")
        print(f"🤖 模型: {model_name} ({price})")

    # 构建消息内容
    content = [{"type": "text", "text": prompt}]
    for url in image_urls:
        content.append({"type": "image_url", "image_url": {"url": url}})

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model,
        "messages": [{"role": "user", "content": content}]
    }

    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=120)
        resp.raise_for_status()
        result = resp.json()

        content = result['choices'][0]['message']['content']

        images = []
        urls = re.findall(r'!\[.*?\]\((https?://[^)]+)\)', content)
        for url in urls:
            images.append(("url", url))

        if not images and return_type == "base64":
            b64_match = re.search(r'data:image/[^;]+;base64,([A-Za-z0-9+/=]+)', content)
            if b64_match:
                images.append(("base64", b64_match.group(1)))
            elif re.match(r'^[A-Za-z0-9+/=]+$', content.strip()[:100]):
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
        output.write_bytes(base64.b64decode(data))

    print(f"💾 已保存: {output}")


def main():
    parser = argparse.ArgumentParser(
        description="老张 API 图片编辑",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
风格: 卡通/油画/水墨/赛博朋克/素描/水彩

示例:
  %(prog)s "https://example.com/cat.jpg" "毛色改成彩虹色"
  %(prog)s "https://example.com/photo.jpg" --style 卡通
  %(prog)s "https://a.jpg,https://b.jpg" "融合两张图"
        """
    )

    parser.add_argument("images", help="图片URL（多图用逗号分隔）")
    parser.add_argument("prompt", nargs="?", help="编辑描述（--style 时可省略）")
    parser.add_argument("-m", "--model", choices=list(MODELS.keys()), help=f"模型（默认: {DEFAULT_MODEL}）")
    parser.add_argument("-s", "--style", choices=list(STYLES.keys()), help="预设风格")
    parser.add_argument("-o", "--output", type=Path, help="保存路径")
    parser.add_argument("-t", "--token", help="API token")
    parser.add_argument("-v", "--verbose", action="store_true", help="详细信息")
    parser.add_argument("--json", action="store_true", help="输出完整JSON")
    parser.add_argument("--no-save", action="store_true", help="不保存图片")

    args = parser.parse_args()

    prompt = STYLES[args.style] if args.style else args.prompt
    if not prompt:
        print("❌ 请提供编辑描述或使用 --style")
        sys.exit(1)

    image_urls = [u.strip() for u in args.images.split(",")]

    token = args.token or get_token()
    if not token:
        print(f"❌ 未找到 token。请创建 {TOKEN_PATH} 或使用 --token")
        sys.exit(1)

    images, result = edit(image_urls, prompt, token, args.model, args.verbose)

    if not images:
        print("❌ 未能生成图片")
        sys.exit(1)

    for i, (img_type, data) in enumerate(images, 1):
        if img_type == "url":
            print(f"🖼️  图片 {i}: {data}")
        else:
            print(f"🖼️  图片 {i}: [base64, {len(data)} 字符]")

        if not args.no_save and i == 1:
            suffix = f"-{args.style}" if args.style else ""
            output = args.output or OUTPUT_DIR / generate_filename(prompt, suffix)
            save_image(img_type, data, output)

    if args.json and result:
        print("\n📄 完整响应:")
        print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
