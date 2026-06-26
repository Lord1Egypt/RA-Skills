# -*- coding: utf-8 -*-
"""
Submit a HunYuan text-to-image generation task (SubmitTextToImageJob).
Returns the JobId for subsequent status polling via query_job.py.
"""

import json
import os
import subprocess
import sys


def ensure_dependencies():
    try:
        import tencentcloud  # noqa: F401
    except ImportError:
        print("[INFO] tencentcloud-sdk-python not found. Installing...", file=sys.stderr)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "tencentcloud-sdk-python", "-q"],
            stdout=sys.stderr,
            stderr=sys.stderr,
        )
        print("[INFO] tencentcloud-sdk-python installed successfully.", file=sys.stderr)


ensure_dependencies()

from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import (
    TencentCloudSDKException,
)
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.aiart.v20221229 import aiart_client, models


# ===================== Credentials =====================

def get_credentials():
    secret_id = os.getenv("TENCENTCLOUD_SECRET_ID")
    secret_key = os.getenv("TENCENTCLOUD_SECRET_KEY")

    if not secret_id or not secret_key:
        error_msg = {
            "error": "CREDENTIALS_NOT_CONFIGURED",
            "message": (
                "Tencent Cloud API credentials not found in environment variables. "
                "Please set TENCENTCLOUD_SECRET_ID and TENCENTCLOUD_SECRET_KEY."
            ),
            "guide": {
                "step1": "开通混元生图服务: https://console.cloud.tencent.com/aiart",
                "step2": "获取 API 密钥: https://console.cloud.tencent.com/cam/capi",
                "step3_linux": 'export TENCENTCLOUD_SECRET_ID="your_id" && export TENCENTCLOUD_SECRET_KEY="your_key"',
                "step3_windows": '$env:TENCENTCLOUD_SECRET_ID="your_id"; $env:TENCENTCLOUD_SECRET_KEY="your_key"',
            },
        }
        print(json.dumps(error_msg, ensure_ascii=False, indent=2))
        sys.exit(1)

    token = os.getenv("TENCENTCLOUD_TOKEN")
    if token:
        return credential.Credential(secret_id, secret_key, token)
    return credential.Credential(secret_id, secret_key)


# ===================== Client =====================

def build_aiart_client(cred, region="ap-guangzhou"):
    http_profile = HttpProfile()
    http_profile.endpoint = "aiart.tencentcloudapi.com"

    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    return aiart_client.AiartClient(cred, region, client_profile)


# ===================== Validation =====================

SUPPORTED_IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")
MAX_IMAGES = 3


def validate_resolution(resolution):
    """Validate resolution: W and H in [512, 2048], area <= 1024*1024."""
    parts = resolution.split(":")
    if len(parts) != 2:
        return False, "Resolution must be in W:H format (e.g., 1024:1024)"
    try:
        w, h = int(parts[0]), int(parts[1])
    except ValueError:
        return False, "Resolution width and height must be integers"
    if not (512 <= w <= 2048):
        return False, f"Width {w} out of range [512, 2048]"
    if not (512 <= h <= 2048):
        return False, f"Height {h} out of range [512, 2048]"
    if w * h > 1024 * 1024:
        return False, f"Image area {w}x{h}={w*h} exceeds max 1024x1024={1024*1024}"
    return True, ""


def validate_images(images):
    """Validate reference images list."""
    if len(images) > MAX_IMAGES:
        return False, f"Too many images: {len(images)}, max allowed is {MAX_IMAGES}"
    for img in images:
        lower = img.lower()
        if not any(lower.endswith(ext) for ext in SUPPORTED_IMAGE_EXTENSIONS):
            return False, (
                f"Unsupported image format: {img}. "
                f"Supported formats: {', '.join(SUPPORTED_IMAGE_EXTENSIONS)}"
            )
    return True, ""


# ===================== Argument Parsing =====================

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Submit a HunYuan Text-to-Image generation task (SubmitTextToImageJob)"
    )
    parser.add_argument("prompt", nargs="?", help="Text description for image generation (Chinese recommended)")
    parser.add_argument("--stdin", action="store_true", help="Read JSON parameters from stdin")
    parser.add_argument(
        "--images", nargs="*", default=[],
        help="Reference image URLs for guided generation (max 3, supports jpg/jpeg/png/webp, base64 size <= 10MB each)",
    )
    parser.add_argument(
        "--resolution", default="1024:1024",
        help="Output resolution as W:H (default: 1024:1024). W and H in [512, 2048], area <= 1024*1024",
    )
    parser.add_argument("--seed", type=int, default=None, help="Random seed for reproducible generation")
    parser.add_argument("--revise", type=int, default=None, choices=[0, 1],
                        help="Enable prompt rewriting: 0=off, 1=on (default: on). Rewriting improves results but adds ~20s")
    parser.add_argument("--region", default="ap-guangzhou", help="Tencent Cloud region (default: ap-guangzhou)")

    args = parser.parse_args()

    # Handle stdin input
    if args.stdin:
        raw = sys.stdin.read().strip()
        data = json.loads(raw)
        args.prompt = data.get("prompt", args.prompt)
        args.images = data.get("images", args.images)
        args.resolution = data.get("resolution", args.resolution)
        args.seed = data.get("seed", args.seed)
        args.revise = data.get("revise", args.revise)
        args.region = data.get("region", args.region)

    if not args.prompt:
        print(json.dumps({
            "error": "NO_PROMPT",
            "message": "No prompt provided. Please supply a text description for image generation.",
            "usage": {
                "basic": 'python3 submit_job.py "一只可爱的猫咪在花园里玩耍"',
                "with_images": 'python3 submit_job.py --images "https://xxx.jpg" "一只可爱的猫咪"',
                "with_resolution": 'python3 submit_job.py --resolution 1024:768 "山水画"',
                "stdin": 'echo \'\'{"prompt":"一只猫","images":["https://xxx.jpg"]}\'\'  | python3 submit_job.py --stdin',
            },
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    # Validate prompt length (API 限制最多 256 个 utf-8 字符)
    if len(args.prompt) > 256:
        print(json.dumps({
            "error": "PROMPT_TOO_LONG",
            "message": f"Prompt length {len(args.prompt)} exceeds max 256 characters.",
            "hint": "请缩短文本描述，最多支持 256 个 utf-8 字符。",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    # Validate resolution
    ok, msg = validate_resolution(args.resolution)
    if not ok:
        print(json.dumps({
            "error": "INVALID_RESOLUTION",
            "message": msg,
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    # Validate images
    if args.images:
        ok, msg = validate_images(args.images)
        if not ok:
            print(json.dumps({
                "error": "INVALID_IMAGES",
                "message": msg,
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

    return args


# ===================== Submit Task =====================

def submit_task(client, prompt, images=None, resolution="1024:1024",
                seed=None, revise=None):
    """Submit a SubmitTextToImageJob request."""
    req = models.SubmitTextToImageJobRequest()
    params = {
        "Prompt": prompt,
        "Resolution": resolution,
    }

    if images:
        params["Images"] = images

    if seed is not None:
        params["Seed"] = seed

    if revise is not None:
        params["Revise"] = revise

    req.from_json_string(json.dumps(params))
    resp = client.SubmitTextToImageJob(req)
    return json.loads(resp.to_json_string())


# ===================== Main =====================

def main():
    args = parse_args()
    cred = get_credentials()
    client = build_aiart_client(cred, args.region)

    try:
        response = submit_task(
            client,
            prompt=args.prompt,
            images=args.images if args.images else None,
            resolution=args.resolution,
            seed=args.seed,
            revise=args.revise,
        )

        result = {
            "job_id": response.get("JobId", ""),
            "request_id": response.get("RequestId", ""),
            "message": "Task submitted successfully. Use query_job.py to poll for results.",
        }

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except TencentCloudSDKException as err:
        print(json.dumps({
            "error": "AIART_API_ERROR",
            "code": err.code if hasattr(err, "code") else "UNKNOWN",
            "message": str(err),
        }, ensure_ascii=False, indent=2))
        sys.exit(1)
    except Exception as err:
        print(json.dumps({
            "error": "UNEXPECTED_ERROR",
            "message": str(err),
        }, ensure_ascii=False, indent=2))
        sys.exit(1)


if __name__ == "__main__":
    main()
