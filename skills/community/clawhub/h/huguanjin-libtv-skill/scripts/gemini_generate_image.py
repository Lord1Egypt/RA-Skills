#!/usr/bin/env python3
"""Gemini 文生图：POST /v1beta/models/{model}:generateContent"""

import argparse
import base64
import json
import mimetypes
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))
from _config import resolve_env_file_from_argv, load_env_file
from _logger import error_exit, warn, print_json

DEFAULT_BASE_URL = "https://generativelanguage.googleapis.com"
DEFAULT_MODEL = "gemini-3-pro-image-preview"
DEFAULT_ASPECT_RATIO = "1:1"
DEFAULT_IMAGE_SIZE = "1K"
ALLOWED_IMAGE_SIZES = {"512", "1K", "2K", "4K"}
DEFAULT_ENV_FILE = ".env"


def normalize_image_size(raw: str) -> str:
    """标准化并校验 imageSize，避免 4k/非法值导致请求失败。"""
    value = (raw or "").strip().upper()
    if not value:
        value = DEFAULT_IMAGE_SIZE

    if value not in ALLOWED_IMAGE_SIZES:
        error_exit("--image-size 仅支持 512 / 1K / 2K / 4K（注意 K 必须大写）")

    return value


def guess_ext(mime_type: str) -> str:
    """根据 MIME 类型推断扩展名。"""
    if not mime_type:
        return ".png"
    mime_type = mime_type.strip().lower()
    ext = mimetypes.guess_extension(mime_type)
    if ext:
        return ext
    if mime_type.startswith("image/"):
        return ".png"
    return ".bin"


def walk_nodes(obj):
    """深度遍历 JSON 节点。"""
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from walk_nodes(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from walk_nodes(item)


def extract_images_and_texts(payload: dict):
    """从 Gemini 响应中尽可能提取图片和文本。"""
    images = []
    texts = []
    seen_images = set()
    seen_texts = set()

    for node in walk_nodes(payload):
        if not isinstance(node, dict):
            continue

        txt = node.get("text")
        if isinstance(txt, str):
            text_value = txt.strip()
            if text_value and text_value not in seen_texts:
                seen_texts.add(text_value)
                texts.append(text_value)

        for inline_key in ("inlineData", "inline_data"):
            inline_obj = node.get(inline_key)
            if not isinstance(inline_obj, dict):
                continue
            mime_type = inline_obj.get("mimeType") or inline_obj.get("mime_type") or "image/png"
            data = inline_obj.get("data")
            if isinstance(data, str) and data.strip():
                signature = (mime_type, data[:96])
                if signature not in seen_images:
                    seen_images.add(signature)
                    images.append({"mime_type": mime_type, "data": data})

        # 兼容某些代理把图片字段直接放在当前层级。
        data = node.get("data")
        mime_type = node.get("mimeType") or node.get("mime_type")
        if isinstance(data, str) and data.strip() and isinstance(mime_type, str) and mime_type.startswith("image/"):
            signature = (mime_type, data[:96])
            if signature not in seen_images:
                seen_images.add(signature)
                images.append({"mime_type": mime_type, "data": data})

    return images, texts


def decode_base64_data(raw: str) -> bytes:
    """解码标准 base64 或 data URI。"""
    data = raw.strip()
    if data.startswith("data:") and "," in data:
        data = data.split(",", 1)[1]
    # 容错补齐 padding
    pad = len(data) % 4
    if pad:
        data = data + ("=" * (4 - pad))
    return base64.b64decode(data, validate=False)


def build_request_url(base_url: str, model: str, api_key: str) -> str:
    quoted_model = urllib.parse.quote(model, safe="")
    query = urllib.parse.urlencode({"key": api_key})
    return f"{base_url.rstrip('/')}/v1beta/models/{quoted_model}:generateContent?{query}"


def post_json(url: str, body: dict, auth_token: str, timeout: int) -> dict:
    headers = {"Content-Type": "application/json"}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers=headers,
    )

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8")
            if not raw.strip():
                error_exit("Gemini API 返回空响应")
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                error_exit(f"Gemini API 返回非 JSON：{raw[:500]}")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8") if e.fp else ""
        if e.code in (401, 403):
            warn("若使用中转接口，请确认 Authorization: Bearer <token> 与 key 参数是否都已配置。")
        error_exit(f"API 错误 {e.code}: {err_body}")
    except urllib.error.URLError as e:
        error_exit(f"网络错误: {e.reason}")


def save_images(images, output_dir: str, prefix: str):
    os.makedirs(output_dir, exist_ok=True)
    saved = []
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for i, item in enumerate(images, 1):
        mime_type = item.get("mime_type", "image/png")
        raw_data = item.get("data", "")
        try:
            binary = decode_base64_data(raw_data)
        except Exception as e:
            warn(f"第 {i} 张图片 base64 解码失败：{e}")
            continue

        ext = guess_ext(mime_type)
        filename = f"{prefix}_{stamp}_{i:02d}{ext}"
        path = os.path.join(output_dir, filename)
        with open(path, "wb") as f:
            f.write(binary)
        saved.append(path)

    return saved


def main():
    env_file = resolve_env_file_from_argv(sys.argv[1:], env_var_name="GEMINI_ENV_FILE")
    loaded_env_file = load_env_file(env_file)

    parser = argparse.ArgumentParser(
        description="Gemini 文生图（支持宽高比与清晰度）",
        epilog="""
环境变量：
  API_KEY         必填，同时用作 query 参数 key 和 Bearer 鉴权
  API_BASE_URL    可选，默认 https://generativelanguage.googleapis.com

示例：
    python3 gemini_generate_image.py "一只宇航员猫在月球上喝咖啡" --env-file .env --aspect-ratio 16:9 --image-size 2K
  python3 gemini_generate_image.py "电影海报" --api-key YOUR_KEY
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--env-file",
        default=env_file,
        help="环境变量文件路径（默认 .env）",
    )
    parser.add_argument("prompt", help="文生图提示词")
    parser.add_argument("--model", default=os.environ.get("GEMINI_MODEL", DEFAULT_MODEL), help="模型名")
    parser.add_argument(
        "--aspect-ratio",
        default=os.environ.get("GEMINI_ASPECT_RATIO", DEFAULT_ASPECT_RATIO),
        help="宽高比，如 1:1 / 16:9 / 9:16",
    )
    parser.add_argument(
        "--image-size",
        default=os.environ.get("GEMINI_IMAGE_SIZE", DEFAULT_IMAGE_SIZE),
        help="分辨率档位，如 512 / 1K / 2K / 4K",
    )
    parser.add_argument(
        "--response-modalities",
        nargs="+",
        default=["TEXT", "IMAGE"],
        help="返回模态，默认 TEXT IMAGE",
    )
    parser.add_argument(
        "--output-dir",
        default=os.environ.get("GEMINI_OUTPUT_DIR", ""),
        help="输出目录（默认 ~/Downloads/gemini_results）",
    )
    parser.add_argument("--prefix", default="gemini", help="输出文件名前缀")
    parser.add_argument(
        "--base-url",
        default=os.environ.get("API_BASE_URL", DEFAULT_BASE_URL),
        help="Gemini API Base URL",
    )
    parser.add_argument("--api-key", default=os.environ.get("API_KEY", ""), help="API Key")
    parser.add_argument(
        "--auth-token",
        default=os.environ.get("API_KEY", ""),
        help="Bearer Token（中转接口要求时填写，默认与 api-key 相同）",
    )
    parser.add_argument("--timeout", type=int, default=120, help="请求超时秒数（默认 120）")
    args = parser.parse_args()

    args.image_size = normalize_image_size(args.image_size)

    if not args.api_key:
        error_exit("请通过 --api-key 或 API_KEY 提供 key")

    modalities = [m.strip().upper() for m in args.response_modalities if m.strip()]
    if not modalities:
        modalities = ["TEXT", "IMAGE"]

    body = {
        "contents": [
            {
                "role": "user",
                "parts": [{"text": args.prompt}],
            }
        ],
        "generationConfig": {
            "responseModalities": modalities,
            "imageConfig": {
                "aspectRatio": args.aspect_ratio,
                "imageSize": args.image_size,
            },
        },
    }

    request_url = build_request_url(args.base_url, args.model, args.api_key)
    payload = post_json(request_url, body, args.auth_token, args.timeout)

    images, texts = extract_images_and_texts(payload)

    output_dir = args.output_dir or os.path.expanduser("~/Downloads/gemini_results")
    saved = save_images(images, output_dir, args.prefix)

    if not saved:
        payload_preview = json.dumps(payload, ensure_ascii=False)
        if len(payload_preview) > 1200:
            payload_preview = payload_preview[:1200] + "..."
        print_json({
            "error": "未在响应中提取到可保存的图片数据",
            "hint": "请检查 key/token/base_url、模型名以及 responseModalities 是否包含 IMAGE",
            "response_preview": payload_preview,
        })
        raise SystemExit(1)

    out = {
        "model": args.model,
        "output_dir": output_dir,
        "saved": saved,
        "total": len(saved),
    }
    if loaded_env_file:
        out["env_file"] = loaded_env_file
    if texts:
        out["texts"] = texts

    print_json(out)


if __name__ == "__main__":
    main()
