#!/usr/bin/env python3
"""
MiniMax Image Generation (image-01) wrapper.

Usage:
  python3 generate.py --prompt "描述" [--aspect-ratio 16:9] [--n 1] \
      [--api-key KEY] [--base-url URL] \
      [--prompt-optimizer] [--output /path/to/output.png] \
      [--response-format base64|url]

Rules:
  - model: 固定使用 image-01
  - prompt_optimizer: 默认自动判断（短描述 <40 字符自动优化，长描述关闭）
  - aigc_watermark: 默认 false，检测到水印/版权关键词时自动开启
  - aspect_ratio: default 16:9
  - n: default 1, max 9
  - response_format: 默认 base64（脚本自动解码保存），用户要求URL时传 url
  - 输出文件名: minimax-YYYY-MM-DD-prompt_slug.png
  - 输出目录: ~/.openclaw/media/minimax/
"""

import argparse
import base64
import os
import re
import sys
from datetime import date

# ------------------ 配置区（可被命令行参数覆盖）------------------
# TODO: 初始化时填入实际值
API_KEY = "YOUR_API_KEY_HERE"
BASE_URL = "https://api.minimaxi.com"  # CN: api.minimaxi.com, global: api.minimaxi.io
# ----------------------------------------------------------------

URL = f"{BASE_URL}/v1/image_generation"
DEFAULT_ASPECT_RATIO = "16:9"
DEFAULT_N = 1
DEFAULT_PROMPT_OPTIMIZER = True
OUTPUT_DIR = os.path.expanduser("~/.openclaw/media/minimax/")

# 水印关键词 → 启用 aigc_watermark
WATERMARK_KEYWORDS = [
    "水印", "版权", "标识", "商标", "logo", "watermark", "copyright",
    "署名", "签名", "credit", "品牌标识", "trademark",
]


def make_slug(prompt: str) -> str:
    """将 prompt 转换为 safe 文件名：取英文/中文关键词，前20字符，空格变-"""
    # 提取英文词和中文（分开处理）
    english = re.sub(r'[^a-zA-Z\s]', '', prompt)
    chinese = re.sub(r'[\x00-\x7f]', '', prompt)
    words = english.split()
    slug_parts = words[:6]  # 最多6个英文词
    if chinese:
        # 取前3个中文字
        cn = re.findall(r'[\u4e00-\u9fff]+', prompt)
        slug_parts.extend(cn[:3])
    slug = '-'.join(slug_parts).lower()
    # 去除一切非字母数字和连字符
    slug = re.sub(r'[^a-z0-9\-]', '', slug)
    slug = slug[:40]  # 最多40字符
    return slug or "image"


def generate(
    prompt: str,
    output: str = None,
    aspect_ratio: str = DEFAULT_ASPECT_RATIO,
    n: int = DEFAULT_N,
    prompt_optimizer: bool = DEFAULT_PROMPT_OPTIMIZER,
    image_url: str = None,
    api_key: str = API_KEY,
    base_url: str = BASE_URL,
    response_format: str = "base64",
):
    # 固定使用 image-01
    selected_model = "image-01"
    print(f"[INFO] 使用模型: {selected_model}", file=sys.stderr)

    # 自动判断 prompt_optimizer（None 表示用户没有显式指定）
    # 短描述（< 40字符）→ 开启优化；长描述 → 关闭优化保留原意
    if prompt_optimizer is None:
        if len(prompt) < 40:
            prompt_optimizer = True
            print(f"[INFO] Prompt 较短（{len(prompt)} 字符），自动开启 prompt 优化", file=sys.stderr)
        else:
            prompt_optimizer = False
            print(f"[INFO] Prompt 较长（{len(prompt)} 字符），关闭 prompt 优化以保留原意", file=sys.stderr)
    else:
        print(f"[INFO] 使用用户指定的 prompt_optimizer={prompt_optimizer}", file=sys.stderr)

    # 自动判断 aigc_watermark：检测水印/版权关键词
    prompt_lower = prompt.lower()
    aigc_watermark = False
    for kw in WATERMARK_KEYWORDS:
        if kw.lower() in prompt_lower:
            aigc_watermark = True
            print(f"[INFO] 检测到水印关键词 '{kw}'，启用 aigc_watermark", file=sys.stderr)
            break

    # Prompt 长度校验（最大 1500 字符）
    if len(prompt) > 1500:
        print(f"[ERROR] Prompt 长度 {len(prompt)} 超过最大限制 1500 字符，请缩短描述。", file=sys.stderr)
        sys.exit(1)

    # 更新 URL（如果 base_url 传入）
    url = f"{base_url}/v1/image_generation"

    payload = {
        "model": selected_model,
        "prompt": prompt,
        "aspect_ratio": aspect_ratio,
        "response_format": response_format,
        "n": n,
        "prompt_optimizer": prompt_optimizer,
        "aigc_watermark": aigc_watermark,
    }

    # 图生图模式：传入参考图 URL 或本地文件路径
    if image_url:
        # http 开头 → 直接作为公网 URL 传给模型
        if image_url.startswith("http://") or image_url.startswith("https://"):
            print(f"[INFO] 使用公网 URL 作为参考图: {image_url[:60]}...", file=sys.stderr)
        # 本地文件路径 → 读取并转为 base64 Data URL
        elif os.path.isfile(image_url):
            with open(image_url, "rb") as f:
                img_data = f.read()
            ext = os.path.splitext(image_url)[1].lower()
            if ext == ".png":
                mime = "image/png"
            elif ext in [".jpg", ".jpeg"]:
                mime = "image/jpeg"
            elif ext == ".gif":
                mime = "image/gif"
            elif ext == ".webp":
                mime = "image/webp"
            else:
                mime = "image/jpeg"  # 默认
            b64_data = base64.b64encode(img_data).decode("utf-8")
            image_url = f"data:{mime};base64,{b64_data}"
            print(f"[INFO] 已将本地图片转为 base64 Data URL ({len(img_data)} bytes)", file=sys.stderr)
        else:
            print(f"[WARN] 参考图路径不存在或无效: {image_url}", file=sys.stderr)
        # image_url 可以是 Data URL 或公网 URL，直接使用
        payload["subject_reference"] = [
            {
                "type": "character",
                "image_file": image_url,
            }
        ]

    import requests

    resp = requests.post(
        url,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=180,
    )
    resp.raise_for_status()
    data = resp.json()

    # 检查业务错误码
    base_resp = data.get("base_resp", {})
    code = base_resp.get("status_code", 0)
    if code != 0:
        msg = base_resp.get("status_msg", "unknown error")
        error_map = {
            1002: f"限流中 (code={code})，请稍后重试: {msg}",
            1004: f"账号鉴权失败 (code={code})，请检查 API Key: {msg}",
            1008: f"账号余额不足 (code={code}): {msg}",
            1026: f"内容涉及敏感词 (code={code})，请修改描述后重试: {msg}",
            2013: f"参数异常 (code={code}): {msg}",
            2049: f"无效的 API Key (code={code}): {msg}",
        }
        err_msg = error_map.get(code, f"API error code={code}: {msg}")
        print(err_msg, file=sys.stderr)
        sys.exit(1)

    # 取图片数据（base64 或 url）
    if response_format == "url":
        images = data.get("data", {}).get("image_urls", [])
        is_url_mode = True
    else:
        images = data.get("data", {}).get("image_base64", [])
        is_url_mode = False

    if not images:
        print("Error: no image in response", data, file=sys.stderr)
        sys.exit(1)

    if output is None:
        today = date.today().isoformat()
        slug = make_slug(prompt)
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output = os.path.join(OUTPUT_DIR, f"minimax-{today}-{slug}.png")

    os.makedirs(os.path.dirname(output) or ".", exist_ok=True)

    # 保存所有图片，文件名加序号
    saved = []
    for i, img_item in enumerate(images):
        if is_url_mode:
            # URL 模式：直接保存 URL 到文件
            img_url = img_item.get("url") if isinstance(img_item, dict) else img_item
            if len(images) > 1:
                name, ext = os.path.splitext(output)
                out_path = f"{name}_{i+1}.txt"
            else:
                out_path = output.replace(".png", ".txt")
            with open(out_path, "w") as f:
                f.write(img_url)
            saved.append(img_url)  # 打印 URL 而不是路径
        else:
            # base64 模式：解码并保存图片
            img_data = base64.b64decode(img_item)
            if len(images) > 1:
                name, ext = os.path.splitext(output)
                out_path = f"{name}_{i+1}{ext}"
            else:
                out_path = output
            with open(out_path, "wb") as f:
                f.write(img_data)
            saved.append(out_path)

    print(" | ".join(saved))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MiniMax Image Generation")
    parser.add_argument("--prompt", "-p", required=True, help="图片描述（必填）")
    parser.add_argument(
        "--aspect-ratio", "-r", default=DEFAULT_ASPECT_RATIO,
        help=f"宽高比，默认 {DEFAULT_ASPECT_RATIO}"
    )
    parser.add_argument(
        "--output", "-o", default=None,
        help=f"输出路径（默认自动生成到 {OUTPUT_DIR}）"
    )
    parser.add_argument(
        "--n", "-n", type=int, default=DEFAULT_N,
        help=f"生成数量，默认 {DEFAULT_N}，最大 9"
    )
    parser.add_argument(
        "--prompt-optimizer", dest="prompt_optimizer", action="store_true",
        default=None,
        help="开启 prompt 自动优化（默认自动判断：短描述自动优化，长描述关闭）"
    )
    parser.add_argument(
        "--no-prompt-optimizer", dest="prompt_optimizer", action="store_const",
        const=False,
        help="关闭 prompt 自动优化（强制不优化）"
    )
    parser.add_argument(
        "--image-url", default=None,
        help="参考图片 URL（传入则启用图生图模式，保持参考图主体特征）"
    )
    parser.add_argument(
        "--api-key", default=None,
        help=f"API Key（默认使用文件顶部配置）"
    )
    parser.add_argument(
        "--base-url", default=None,
        help=f"API Base URL（默认使用文件顶部配置）"
    )
    parser.add_argument(
        "--response-format", default="base64",
        choices=["base64", "url"],
        help="返回格式：base64（自动解码保存，默认）或 url（返回网络链接，24小时有效）"
    )
    args = parser.parse_args()

    # 如果命令行传入，覆盖全局配置
    final_api_key = args.api_key if args.api_key else API_KEY
    final_base_url = args.base_url if args.base_url else BASE_URL

    generate(
        prompt=args.prompt,
        output=args.output,
        aspect_ratio=args.aspect_ratio,
        n=args.n,
        prompt_optimizer=args.prompt_optimizer,
        image_url=args.image_url,
        api_key=final_api_key,
        base_url=final_base_url,
        response_format=args.response_format,
    )
