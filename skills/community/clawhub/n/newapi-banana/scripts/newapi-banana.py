#!/usr/bin/env python3
"""
NewAPI Banana image generation client for OpenClaw.

Supports image generation via nano-banana and Gemini APIs.
Uses only Python stdlib and curl.

Modes:
  --check                          Account health check
  --list                           List available tasks
  --info TASK                      Show task details
  --task TASK --prompt "..." ...   Execute a generation task
"""

from __future__ import annotations

import argparse
import base64
import json
import mimetypes
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# API host（只使用主地址，避免切到你没有权限的备份域名）
DEFAULT_HOST = "http://nen.baynn.com"

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR.parent / "data"
CAPABILITIES_PATH = DATA_DIR / "capabilities.json"


# ---------------------------------------------------------------------------
# API key resolution
# ---------------------------------------------------------------------------

def read_key_from_openclaw_config() -> str | None:
    cfg_path = Path.home() / ".openclaw" / "openclaw.json"
    if not cfg_path.exists():
        return None
    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    entry = cfg.get("skills", {}).get("entries", {}).get("newapi-banana", {})
    api_key = entry.get("apiKey")
    if isinstance(api_key, str) and api_key.strip():
        return api_key.strip()
    env_val = entry.get("env", {}).get("NEWAPI_API_KEY")
    if isinstance(env_val, str) and env_val.strip():
        return env_val.strip()
    return None


def resolve_api_key(provided_key: str | None) -> str | None:
    """Resolve API key without exiting. Returns None if not found."""
    if provided_key:
        normalized = provided_key.strip()
        placeholders = {
            "your_api_key_here", "<your_api_key>",
            "YOUR_API_KEY", "NEWAPI_API_KEY",
        }
        if normalized and normalized not in placeholders:
            return normalized

    env_key = os.environ.get("NEWAPI_API_KEY", "").strip()
    if env_key:
        return env_key

    return read_key_from_openclaw_config()


def require_api_key(provided_key: str | None) -> str:
    key = resolve_api_key(provided_key)
    if key:
        return key
    result = {
        "error": "NO_API_KEY",
        "message": "No API key configured",
        "steps": [
            "1. Get API key from your NewAPI Banana service provider",
            "2. Send the key in chat or add to ~/.openclaw/openclaw.json: skills.entries.newapi-banana.apiKey",
        ],
    }
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(1)


# ---------------------------------------------------------------------------
# HTTP helpers (curl-based, stdlib only)
# ---------------------------------------------------------------------------

def curl_post_json(url: str, payload: dict, headers: dict, timeout: int = 60) -> subprocess.CompletedProcess:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(payload, f)
        tmp_path = f.name
    try:
        cmd = ["curl", "-s", "-S", "--fail-with-body", "-X", "POST", url,
               "--max-time", str(timeout), "-d", f"@{tmp_path}"]
        for k, v in headers.items():
            cmd += ["-H", f"{k}: {v}"]
        return subprocess.run(cmd, capture_output=True, text=True)
    finally:
        os.unlink(tmp_path)


def curl_post_form_data(url: str, form_data: dict, headers: dict, timeout: int = 120) -> subprocess.CompletedProcess:
    """Post multipart/form-data using curl.

    支持直接传入 Path / 文件路径，会自动按文件处理：
    - key=Path(...) 或 key=\"C:/path/to/file.png\" => -F key=@C:/path/to/file.png
    """
    cmd = ["curl", "-s", "-S", "--fail-with-body", "-X", "POST", url,
           "--max-time", str(timeout)]
    for k, v in headers.items():
        cmd += ["-H", f"{k}: {v}"]

    for key, value in form_data.items():
        # 多值（暂时不需要文件列表，这里保持简单）
        if isinstance(value, (list, tuple)):
            for item in value:
                if isinstance(item, Path):
                    cmd += ["-F", f"{key}=@{str(item)}"]
                elif isinstance(item, str) and os.path.exists(item):
                    cmd += ["-F", f"{key}=@{item}"]
                else:
                    cmd += ["-F", f"{key}={item}"]
        else:
            # 单值：优先按文件处理
            if isinstance(value, Path):
                cmd += ["-F", f"{key}=@{str(value)}"]
            elif isinstance(value, str) and os.path.exists(value):
                cmd += ["-F", f"{key}=@{value}"]
            else:
                cmd += ["-F", f"{key}={value}"]

    return subprocess.run(cmd, capture_output=True, text=True)


def api_request_with_backup(api_key: str, endpoint_suffix: str, payload: dict,
                            method: str = "POST", timeout: int = 60,
                            is_form_data: bool = False) -> dict:
    """单一主机请求封装（历史上支持多备份，这里只用 DEFAULT_HOST）。

    这样可以避免脚本自动切到你没有权限的其它域名（比如 api.gptbest.vip）。
    """
    url = f"{DEFAULT_HOST}{endpoint_suffix}"
    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    if not is_form_data:
        headers["Content-Type"] = "application/json"

    max_retries = 3
    last_error: dict | None = None

    for retry in range(max_retries):
        try:
            if is_form_data:
                result = curl_post_form_data(url, payload, headers, timeout)
            else:
                if method == "POST":
                    result = curl_post_json(url, payload, headers, timeout)
                else:  # GET
                    cmd = [
                        "curl", "-s", "-S", "--fail-with-body", "-X", "GET", url,
                        "--max-time", str(timeout),
                    ]
                    for k, v in headers.items():
                        cmd += ["-H", f"{k}: {v}"]
                    result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode == 0:
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    print(f"Error: Invalid JSON response from {url}", file=sys.stderr)
                    print(f"Response: {result.stdout[:500]}", file=sys.stderr)
                    sys.exit(1)
            else:
                error_body = result.stdout or result.stderr
                try:
                    err = json.loads(error_body)
                    msg = err.get("msg", error_body)
                except (json.JSONDecodeError, TypeError):
                    msg = error_body

                last_error = {
                    "error": "API_ERROR",
                    "message": f"API request failed: {msg}",
                    "host": DEFAULT_HOST,
                    "url": url,
                }

        except Exception as e:
            last_error = {
                "error": "REQUEST_ERROR",
                "message": str(e),
                "host": DEFAULT_HOST,
            }

        if retry < max_retries - 1:
            wait_time = 1000 * (retry + 1)
            time.sleep(wait_time / 1000)
            continue

    # 所有重试失败
    if last_error:
        print(json.dumps(last_error, ensure_ascii=False), file=sys.stderr)
    else:
        print(json.dumps({
            "error": "ALL_HOSTS_FAILED",
            "message": "Primary host failed to respond"
        }, ensure_ascii=False), file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# --check: account health check
# ---------------------------------------------------------------------------

def cmd_check(api_key_arg: str | None, host_url: str | None):
    key = resolve_api_key(api_key_arg)
    host = host_url or DEFAULT_HOST
    
    if not key:
        print(json.dumps({
            "status": "no_key",
            "message": "No API key configured",
            "steps": [
                "1. Get API key from your NewAPI Banana service provider",
                "2. Send the key in chat or add to ~/.openclaw/openclaw.json: skills.entries.newapi-banana.apiKey",
            ],
        }, ensure_ascii=False))
        return
    
    key_prefix = key[:4] + "****"
    
    # Try to check API by making a simple request directly (avoid sys.exit from wrapper)
    try:
        cmd = [
            "curl", "-s", "-S", "--fail-with-body", "-X", "GET",
            f"{host}/v1/models",
            "--max-time", "10",
            "-H", f"Authorization: Bearer {key}",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            print(json.dumps({
                "status": "ready",
                "key_prefix": key_prefix,
                "host": host,
                "message": "API key is valid"
            }, ensure_ascii=False))
        else:
            print(json.dumps({
                "status": "invalid_key",
                "key_prefix": key_prefix,
                "host": host,
                "message": "API key verification failed"
            }, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({
            "status": "error",
            "key_prefix": key_prefix,
            "host": host,
            "message": str(e)
        }, ensure_ascii=False))


# ---------------------------------------------------------------------------
# Media handling
# ---------------------------------------------------------------------------

def image_to_data_uri(file_path: str) -> str:
    mime_type = mimetypes.guess_type(file_path)[0] or "image/png"
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    return f"data:{mime_type};base64,{encoded}"


# ---------------------------------------------------------------------------
# Image generation
# ---------------------------------------------------------------------------

def cmd_generate_image(args):
    """Generate image (text-to-image or image-to-image)."""
    api_key = require_api_key(args.api_key)

    if not args.prompt:
        print("Error: --prompt is required", file=sys.stderr)
        sys.exit(1)

    model = args.model or "nano-banana"
    aspect_ratio = args.aspect_ratio or "auto"

    if "gemini" in model.lower():
        # Gemini via NewAPI relay — same host, Bearer auth, Gemini request format
        endpoint = f"/v1beta/models/{model}:generateContent"
        url = f"{DEFAULT_HOST}{endpoint}"

        parts = [{"text": args.prompt}]

        if args.image:
            image_path = Path(args.image)
            if not image_path.exists():
                print(f"Error: image file not found: {args.image}", file=sys.stderr)
                sys.exit(1)
            mime_type = mimetypes.guess_type(str(image_path))[0] or "image/png"
            with open(image_path, "rb") as f:
                b64_data = base64.b64encode(f.read()).decode()
            parts.append({
                "inlineData": {
                    "mimeType": mime_type,
                    "data": b64_data
                }
            })

        payload = {
            "contents": [{"parts": parts}],
            "generationConfig": {"responseModalities": ["TEXT", "IMAGE"]}
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        result = curl_post_json(url, payload, headers, timeout=120)

        if result.returncode != 0:
            error_body = result.stdout or result.stderr
            print(f"Gemini API error: {error_body[:500]}", file=sys.stderr)
            sys.exit(1)

        try:
            resp = json.loads(result.stdout)
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON from Gemini API", file=sys.stderr)
            print(result.stdout[:500], file=sys.stderr)
            sys.exit(1)

        # Extract inline image from response
        image_b64 = None
        image_mime = "image/png"
        candidates = resp.get("candidates", [])
        if candidates:
            for part in candidates[0].get("content", {}).get("parts", []):
                inline = part.get("inlineData")
                if inline:
                    image_b64 = inline.get("data")
                    image_mime = inline.get("mimeType", "image/png")
                    break

        if not image_b64:
            print("Error: No image data in Gemini response", file=sys.stderr)
            print(json.dumps(resp, indent=2, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)

        ext = image_mime.split("/")[-1].replace("jpeg", "jpg")
        output_path = args.output or f"/tmp/openclaw/newapi-output/image_{int(time.time())}.{ext}"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(base64.b64decode(image_b64))

        print(f"OUTPUT_FILE:{Path(output_path).resolve()}")
        return

    # nano-banana series: unified endpoint for text-to-image and image-to-image
    endpoint = "/v1/images/generations"
    payload = {
        "model": model,
        "prompt": args.prompt,
        "aspectRatio": aspect_ratio,
        "imageSize": "1K",
        "shutProgress": False,
    }

    # If image provided, encode as base64 and add to payload
    if args.image:
        image_path = Path(args.image)
        if not image_path.exists():
            print(f"Error: image file not found: {args.image}", file=sys.stderr)
            sys.exit(1)
        mime_type = mimetypes.guess_type(str(image_path))[0] or "image/png"
        with open(image_path, "rb") as f:
            b64_data = base64.b64encode(f.read()).decode()
        payload["base64"] = f"data:{mime_type};base64,{b64_data}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    url = f"{DEFAULT_HOST}{endpoint}"
    result = curl_post_json(url, payload, headers, timeout=120)

    if result.returncode != 0:
        error_body = result.stdout or result.stderr
        print(f"API error: {error_body[:500]}", file=sys.stderr)
        sys.exit(1)

    try:
        resp = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON response", file=sys.stderr)
        print(result.stdout[:500], file=sys.stderr)
        sys.exit(1)

    # Extract image URL from response
    image_url = None
    if resp.get("data") and len(resp["data"]) > 0:
        image_url = resp["data"][0].get("url")
    elif resp.get("url"):
        image_url = resp["url"]

    if not image_url:
        print("Error: No image URL in response", file=sys.stderr)
        print(json.dumps(resp, indent=2, ensure_ascii=False), file=sys.stderr)
        sys.exit(1)

    # Download image
    output_path = args.output or f"/tmp/openclaw/newapi-output/image_{int(time.time())}.png"
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    cmd = ["curl", "-s", "-S", "-L", "-o", output_path, "--max-time", "300", image_url]
    dl = subprocess.run(cmd, capture_output=True, text=True)
    if dl.returncode != 0:
        print(f"Download failed: {dl.stderr}", file=sys.stderr)
        sys.exit(1)

    print(f"OUTPUT_FILE:{Path(output_path).resolve()}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="NewAPI Banana image generation client for OpenClaw",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Modes:
  --check                           Check API key
  --list                            List available tasks
  --info TASK                       Show task details
  --task TASK [options]             Execute a generation task

Tasks:
  text-to-image                     Generate image from text
  image-to-image                    Generate image from image

Examples:
  python3 newapi-banana.py --check
  python3 newapi-banana.py --task text-to-image --prompt "a cute dog" --output /tmp/dog.png
  python3 newapi-banana.py --task image-to-image --prompt "change background to night" --image /tmp/input.png
""",
    )

    # Mode flags
    parser.add_argument("--check", action="store_true", help="Check API key")
    parser.add_argument("--list", action="store_true", help="List available tasks")
    parser.add_argument("--info", metavar="TASK", help="Show details for a task")

    # Execution params
    parser.add_argument("--task", "-t", help="Task type")
    parser.add_argument("--prompt", "-p", help="Text prompt")
    parser.add_argument("--image", "-i", help="Input image path")
    parser.add_argument("--model", "-m", help="Model name")
    parser.add_argument("--aspect-ratio", help="Aspect ratio (4:3, 16:9, 9:16, etc.)")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--api-key", "-k", help="API key (optional, resolved from config)")
    parser.add_argument("--host-url", help="API host URL (default: http://nen.baynn.com)")

    args = parser.parse_args()

    if args.check:
        cmd_check(args.api_key, args.host_url)
    elif args.list:
        tasks = [
            "text-to-image - Generate image from text",
            "image-to-image - Generate image from image",
        ]
        print("Available tasks:")
        for task in tasks:
            print(f"  {task}")
    elif args.info:
        print(f"Task info for: {args.info}")
        print("Use --list to see all available tasks")
    elif args.task:
        if args.task in ("text-to-image", "image-to-image"):
            cmd_generate_image(args)
        else:
            print(f"Error: Unknown task: {args.task}", file=sys.stderr)
            print("Use --list to see available tasks", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
