# -*- coding: utf-8 -*-
"""
HunYuan Text-to-Image All-in-One Script.
Submits a SubmitTextToImageJob task and automatically polls until the image is generated.
"""

import json
import os
import subprocess
import sys
import time


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
    """Get Tencent Cloud credentials from environment variables."""
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
    """Build AIART API client."""
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
    """Parse command-line arguments."""
    import argparse

    parser = argparse.ArgumentParser(
        description="HunYuan Text-to-Image Generation (submit + auto-poll)"
    )
    parser.add_argument("prompt", nargs="?", help="Text description for image generation (Chinese recommended, max 256 chars)")
    parser.add_argument("--stdin", action="store_true", help="Read JSON parameters from stdin")
    parser.add_argument(
        "--images", nargs="*", default=[],
        help="Reference image URLs for guided generation (max 3, supports jpg/jpeg/png/webp, base64 size <= 10MB each)",
    )
    parser.add_argument(
        "--resolution", default="1024:1024",
        help="Output resolution as W:H (default: 1024:1024). W and H in [512, 2048], area <= 1024*1024",
    )
    parser.add_argument("--seed", type=int, default=None,
                        help="Random seed for reproducible generation (default: random)")
    parser.add_argument("--revise", type=int, default=None, choices=[0, 1],
                        help="Enable prompt rewriting: 0=off, 1=on (default: on). Rewriting improves results but adds ~20s")
    parser.add_argument("--poll-interval", type=int, default=5,
                        help="Polling interval in seconds (default: 5)")
    parser.add_argument("--max-poll-time", type=int, default=300,
                        help="Max total polling time in seconds (default: 300 = 5min)")
    parser.add_argument("--no-poll", action="store_true",
                        help="Submit task only, do not poll (returns JobId)")
    parser.add_argument("--region", default="ap-guangzhou",
                        help="Tencent Cloud region (default: ap-guangzhou)")

    args = parser.parse_args()

    # Handle stdin JSON input
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
                "basic": 'python3 main.py "一只可爱的猫咪在花园里玩耍"',
                "with_images": 'python3 main.py --images "https://xxx.jpg" "一只可爱的猫咪"',
                "with_resolution": 'python3 main.py --resolution 1024:768 "壮丽的山水画"',
                "submit_only": 'python3 main.py --no-poll "一只猫"',
                "stdin": 'echo \'\'{"prompt":"一只猫","images":["https://xxx.jpg"]}\'\'  | python3 main.py --stdin',
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
            "hint": "Resolution W:H, W and H in [512, 2048], area <= 1024*1024. Default: 1024:1024",
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    # Validate images
    if args.images:
        ok, msg = validate_images(args.images)
        if not ok:
            print(json.dumps({
                "error": "INVALID_IMAGES",
                "message": msg,
                "hint": "Max 3 images, supported formats: jpg, jpeg, png, webp. Base64 size <= 10MB each.",
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

    return args


# ===================== Submit Task =====================

def submit_task(client, prompt, images=None, resolution="1024:1024",
                seed=None, revise=None):
    """Submit a SubmitTextToImageJob request and return the response."""
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


# ===================== Query Task =====================

def query_task(client, job_id):
    """Query a single task status via QueryTextToImageJob."""
    req = models.QueryTextToImageJobRequest()
    req.from_json_string(json.dumps({"JobId": job_id}))
    resp = client.QueryTextToImageJob(req)
    return json.loads(resp.to_json_string())


# JobStatusCode 任务状态码：1=排队中, 2=运行中, 4=生成失败, 5=生成完成
JOB_STATUS_WAITING = "1"
JOB_STATUS_RUNNING = "2"
JOB_STATUS_FAILED = "4"
JOB_STATUS_DONE = "5"

JOB_STATUS_DESC = {
    JOB_STATUS_WAITING: "排队中(waiting)",
    JOB_STATUS_RUNNING: "运行中(running)",
    JOB_STATUS_FAILED: "生成失败(failed)",
    JOB_STATUS_DONE: "生成完成(done)",
}


def poll_task(client, job_id, poll_interval, max_poll_time):
    """Poll task status until done/failed or timeout."""
    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        if elapsed > max_poll_time:
            print(json.dumps({
                "error": "POLL_TIMEOUT",
                "message": f"Task {job_id} did not complete within {max_poll_time}s.",
                "job_id": job_id,
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        response = query_task(client, job_id)
        # API returns JobStatusCode as a string number: "1","2","4","5"
        status_code = str(response.get("JobStatusCode", ""))

        if status_code == JOB_STATUS_DONE:
            return response
        elif status_code == JOB_STATUS_FAILED:
            print(json.dumps({
                "error": "TASK_FAILED",
                "job_id": job_id,
                "status_code": status_code,
                "status_desc": JOB_STATUS_DESC.get(status_code, "unknown"),
                "status_msg": response.get("JobStatusMsg", ""),
                "error_code": response.get("JobErrorCode", ""),
                "error_msg": response.get("JobErrorMsg", ""),
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        status_desc = JOB_STATUS_DESC.get(status_code, f"unknown({status_code})")
        print(
            f"[INFO] Job {job_id} status: {status_desc}({status_code}), "
            f"elapsed: {int(elapsed)}s, next poll in {poll_interval}s...",
            file=sys.stderr,
        )
        time.sleep(poll_interval)


# ===================== Main =====================

def main():
    args = parse_args()
    cred = get_credentials()
    client = build_aiart_client(cred, args.region)

    try:
        # Step 1: Submit task
        print("[INFO] Submitting text-to-image generation task...", file=sys.stderr)
        submit_resp = submit_task(
            client,
            prompt=args.prompt,
            images=args.images if args.images else None,
            resolution=args.resolution,
            seed=args.seed,
            revise=args.revise,
        )

        job_id = submit_resp.get("JobId", "")
        if not job_id:
            print(json.dumps({
                "error": "NO_JOB_ID",
"message": "Failed to get JobId from SubmitTextToImageJob response.",
                "response": submit_resp,
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        print(f"[INFO] Task submitted, JobId: {job_id}", file=sys.stderr)

        # If --no-poll, return JobId immediately
        if args.no_poll:
            print(json.dumps({
                "job_id": job_id,
                "request_id": submit_resp.get("RequestId", ""),
                "message": "Task submitted. Use query_job.py to poll for results.",
            }, ensure_ascii=False, indent=2))
            return

        # Step 2: Poll for result
        print(f"[INFO] Polling for results (interval={args.poll_interval}s, max={args.max_poll_time}s)...", file=sys.stderr)
        response = poll_task(client, job_id, args.poll_interval, args.max_poll_time)

        # Step 3: Output result
        result = {
            "job_id": job_id,
            "status": "success",
            "result_image": response.get("ResultImage", ""),
        }

        if response.get("ResultDetails"):
            result["result_details"] = response["ResultDetails"]
        if response.get("RevisedPrompt"):
            result["revised_prompt"] = response["RevisedPrompt"]

        print(json.dumps(result, ensure_ascii=False, indent=2))
        print(f"\n[INFO] Image generated successfully! URL: {result['result_image']}", file=sys.stderr)
        print("[INFO] Note: Image URL is valid for 1 hour. Please save promptly.", file=sys.stderr)

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
