#!/usr/bin/env python
# NOTE: On Windows, `python3` may not exist on PATH. Use `python` (or call python.exe explicitly) to run this script.
"""
Nano Banana 2 (APIYI) - Image Generation Script
Generates images using APIYI's Gemini 3.1 Flash Image Preview API
"""

import argparse
import base64
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import requests


def get_timestamp_filename(prefix: str = "image", suffix: str = "png") -> str:
    """Generate filename with timestamp."""
    now = datetime.now()
    return f"{now.strftime('%Y-%m-%d-%H-%M-%S')}-{prefix}.{suffix}"


def generate_image(
    prompt: str,
    api_key: str,
    filename: Optional[str] = None,
    aspect_ratio: str = "16:9",
    size: str = "2K",
) -> str:
    """Generate image via APIYI API."""
    
    url = "https://api.apiyi.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    # Map aspect ratio and size to API parameters
    aspect_ratios = {
        "1:1": {"width": 1024, "height": 1024},
        "16:9": {"width": 1920, "height": 1080},
        "9:16": {"width": 1080, "height": 1920},
    }
    
    sizes = {
        "1K": 1024,
        "2K": 2048,
    }
    
    # Get dimensions
    dims = aspect_ratios.get(aspect_ratio, {"width": 1920, "height": 1080})
    image_size = sizes.get(size, 2048)
    
    # Use the larger dimension for imageSize
    max_dim = max(dims["width"], dims["height"])
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseModalities": ["IMAGE"],
            "imageConfig": {
                "aspectRatio": aspect_ratio,
                "imageSize": size,  # Use the size string directly
            }
        }
    }
    
    print(f"Generating image with prompt: {prompt[:100]}...", file=sys.stderr)
    print(f"Aspect ratio: {aspect_ratio}, Size: {size}", file=sys.stderr)
    
    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=300,
    )
    
    if response.status_code != 200:
        print(f"API Error: {response.status_code}", file=sys.stderr)
        print(f"Response: {response.text}", file=sys.stderr)
        sys.exit(1)
    
    result = response.json()
    
    # Parse response
    try:
        img_data = result["candidates"][0]["content"]["parts"][0]["inlineData"]["data"]
    except (KeyError, IndexError) as e:
        print(f"Failed to parse response: {e}", file=sys.stderr)
        print(f"Response: {json.dumps(result, indent=2)}", file=sys.stderr)
        sys.exit(1)
    
    # Decode and save
    image_bytes = base64.b64decode(img_data)
    
    if filename is None:
        filename = get_timestamp_filename()
    
    output_path = Path(filename).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "wb") as f:
        f.write(image_bytes)
    
    # Print MEDIA line for OpenClaw to auto-attach
    print(f"MEDIA:{output_path}")
    print(f"Image saved to: {output_path}", file=sys.stderr)
    
    return str(output_path)


def suggest_prompts_zh(user_request: str):
    """Return 3 enriched Chinese prompt options (A/B/C) for a given request."""
    req = (user_request or "").strip()
    # Keep it simple and template-driven for reliability.
    base = req if req else "简约独居冷色治愈"
    return {
        "A": {
            "title": "北欧极简冷色（通透、干净、日常治愈）",
            "prompt": f"{base}，北欧极简风独居公寓客厅，冷色治愈氛围，阴天漫射自然光从大窗户照入，白色纱帘轻微透光，墙面留白，浅灰布艺沙发，浅木色地板与原木小茶几，桌面只有一个陶瓷杯和一本合上的书，角落一盆小型绿植，一盏极简落地灯但不亮，空间非常整洁克制，低饱和蓝灰色调、低对比，柔和阴影，真实摄影质感，细节清晰，轻微景深虚化",
            "negative": "人物，杂乱，强暖黄灯光，强烈阳光光束，霓虹，赛博，恐怖，过饱和，文字水印logo，低清噪点，过度锐化",
        },
        "B": {
            "title": "日系冷淡风（更安静、更情绪一点）",
            "prompt": f"{base}，日系冷淡风独居小屋室内一角，MUJI/无印感，冷色低饱和，阴天自然光，哑光材质，线条简洁，矮桌上放一本书和一杯热饮，浅灰布艺沙发，墙上一幅极简装饰画（无文字），少量绿植点缀，安静、放松、治愈，画面干净留白，低对比，柔焦质感",
            "negative": "人物，强烈阳光光束，暖橙灯光，浓烈色彩，高对比，杂物堆满，文字水印logo，低质量，过度锐化",
        },
        "C": {
            "title": "现代极简冷色夜景（氛围感更强）",
            "prompt": f"{base}，现代极简独居公寓夜景，冷蓝灰环境光，柔和间接灯带（不刺眼），窗外城市夜景散景虚化，浅灰白家具与干净墙面，小茶几上一杯热饮轻微冒气，微弱反光与柔和阴影，空间克制整洁，安静治愈，轻电影感，真实摄影质感，细节清晰，景深虚化",
            "negative": "人物，强霓虹，赛博朋克，过度光晕，杂乱，文字水印logo，低清噪点，过饱和",
        },
    }


def suggest_a_variants_zh(user_request: str):
    """Return A1/A2/A3 variants for the Nordic-minimal direction."""
    base = (user_request or "").strip() or "简约独居冷色治愈"
    common_neg = "人物，杂乱，强暖黄灯光，强烈阳光光束，霓虹，赛博，恐怖，过饱和，文字水印logo，低清噪点，过度锐化"
    return {
        "A1": {
            "title": "通透日光版（最干净、家居摄影感）",
            "prompt": f"{base}，北欧极简风独居公寓客厅，冷色治愈氛围，阴天漫射自然光从大窗户照入，白色纱帘轻微透光，墙面留白，浅灰布艺沙发，浅木色地板与原木小茶几，桌面只有一个陶瓷杯和一本合上的书，角落一盆小型绿植，一盏极简落地灯但不亮，空间非常整洁克制，低饱和蓝灰色调、低对比，柔和阴影，真实摄影质感，细节清晰，轻微景深虚化",
            "negative": common_neg,
        },
        "A2": {
            "title": "温柔冷色版（更软、更治愈）",
            "prompt": f"{base}，北欧极简独居客厅，冷色调为主（蓝灰/雾白/浅木），整体柔和温润，窗外阴天，室内光线柔软不刺眼，浅灰沙发搭配米白针织毯（少量点缀），原木小圆桌，上面一杯热茶轻微冒气，绿植一盆，空间干净留白，材质偏哑光，低对比低饱和，安静治愈，真实摄影质感，细节丰富但不过度锐化",
            "negative": common_neg,
        },
        "A3": {
            "title": "构图高级版（更像杂志封面）",
            "prompt": f"{base}，北欧极简独居公寓客厅一角，冷色高级感，干净几何构图，留白充足，浅灰沙发与原木家具，墙面一幅极简线条装饰画（无文字），窗边纱帘，阴天柔光，画面秩序感强、物件极少，低饱和蓝灰调，轻电影感但仍写实，真实摄影，高级质感，细节清晰，景深虚化",
            "negative": "人物，复杂装饰，花哨色彩，霓虹，文字logo水印，杂乱，低清噪点，过度锐化",
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Generate images via APIYI (Gemini 3.1 Flash)")
    parser.add_argument("--prompt", "-p", help="Image generation prompt")
    parser.add_argument("--filename", "-f", help="Output filename (default: timestamp-based)")
    parser.add_argument(
        "--suggest-zh",
        help="Given a Chinese request, print 3 enriched Chinese prompt options (A/B/C) and exit"
    )
    parser.add_argument(
        "--suggest-zh-a",
        help="Given a Chinese request, print Nordic-minimal variants (A1/A2/A3) and exit"
    )
    parser.add_argument(
        "--aspect-ratio", "-a", default="16:9", 
        choices=["1:1", "16:9", "9:16"],
        help="Image aspect ratio (default: 16:9)"
    )
    parser.add_argument(
        "--size", "-s", default="2K",
        choices=["1K", "2K"],
        help="Image size (default: 2K)"
    )
    parser.add_argument(
        "--api-key",
        help="APIYI API key (override all other sources)"
    )
    parser.add_argument(
        "--debug-key",
        action="store_true",
        help="Print where APIYI_API_KEY is loaded from (never prints the key itself)"
    )
    
    args = parser.parse_args()

    # Suggestion mode (no API call)
    if args.suggest_zh is not None:
        options = suggest_prompts_zh(args.suggest_zh)
        print(json.dumps({"request": args.suggest_zh, "options": options}, ensure_ascii=False, indent=2))
        return

    if args.suggest_zh_a is not None:
        options = suggest_a_variants_zh(args.suggest_zh_a)
        print(json.dumps({"request": args.suggest_zh_a, "options": options}, ensure_ascii=False, indent=2))
        return

    if not args.prompt:
        print("Error: --prompt is required unless using --suggest-zh/--suggest-zh-a", file=sys.stderr)
        sys.exit(2)

    # Get API key
    # Priority:
    # 1) CLI --api-key
    # 2) openclaw.json top-level env.APIYI_API_KEY (requested behavior)
    # 3) OS env var APIYI_API_KEY (fallback)
    api_key = args.api_key
    api_key_source = "cli" if api_key else None

    config_path = Path.home() / ".openclaw" / "openclaw.json"
    config_loaded = False
    config_has_key = False

    if not api_key:
        if config_path.exists():
            try:
                with open(config_path, "r", encoding="utf-8") as f:
                    config = json.load(f)
                config_loaded = True
                api_key = (config.get("env", {}) or {}).get("APIYI_API_KEY")
                config_has_key = bool(api_key)
                if api_key:
                    api_key_source = "openclaw.json:env.APIYI_API_KEY"
            except Exception:
                pass

    if not api_key:
        api_key = os.environ.get("APIYI_API_KEY")
        if api_key:
            api_key_source = "os-env:APIYI_API_KEY"

    if args.debug_key:
        home = str(Path.home())
        print("[debug-key] home=", home, file=sys.stderr)
        print("[debug-key] openclaw_json=", str(config_path), file=sys.stderr)
        print("[debug-key] openclaw_json_exists=", str(config_path.exists()), file=sys.stderr)
        print("[debug-key] openclaw_json_loaded=", str(config_loaded), file=sys.stderr)
        print("[debug-key] openclaw_json_has_env_apiyi_key=", str(config_has_key), file=sys.stderr)
        print("[debug-key] api_key_source=", (api_key_source or "none"), file=sys.stderr)
        # Only reveal length/prefix/suffix to help debugging without leaking secrets
        if api_key:
            k = str(api_key)
            safe = f"len={len(k)}, head={k[:4]}..., tail=...{k[-4:]}" if len(k) >= 8 else f"len={len(k)}"
            print("[debug-key] api_key_fingerprint=", safe, file=sys.stderr)

    if not api_key:
        print("Error: APIYI_API_KEY not set. Use --api-key, or set openclaw.json env.APIYI_API_KEY, or set OS env var APIYI_API_KEY.", file=sys.stderr)
        sys.exit(1)
    
    generate_image(
        prompt=args.prompt,
        api_key=api_key,
        filename=args.filename,
        aspect_ratio=args.aspect_ratio,
        size=args.size,
    )


if __name__ == "__main__":
    main()
