# -*- coding: utf-8 -*-
"""
HunYuan 3D Generation All-in-One Script.
Submits a SubmitHunyuanTo3DProJob task and automatically polls until the 3D model is generated.
"""

import json
import os
import subprocess
import sys
import time


def ensure_dependencies():
    try:
        import tencentcloud.ai3d  # noqa: F401
    except (ImportError, ModuleNotFoundError):
        print("[INFO] tencentcloud-sdk-python (ai3d) not found. Installing...", file=sys.stderr)
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
from tencentcloud.ai3d.v20250513 import ai3d_client, models


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
                "step1": "开通混元3D服务: https://console.cloud.tencent.com/ai3d",
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

def build_ai3d_client(cred, region="ap-guangzhou"):
    """Build AI3D API client."""
    http_profile = HttpProfile()
    http_profile.endpoint = "ai3d.tencentcloudapi.com"

    client_profile = ClientProfile()
    client_profile.httpProfile = http_profile

    return ai3d_client.Ai3dClient(cred, region, client_profile)


# ===================== Constants =====================

VALID_GENERATE_TYPES = ("Normal", "LowPoly", "Geometry", "Sketch")
VALID_POLYGON_TYPES = ("triangle", "quadrilateral")
VALID_RESULT_FORMATS = ("STL", "USDZ", "FBX")
VALID_MODELS = ("3.0", "3.1")
VALID_VIEW_TYPES = ("left", "right", "back", "top", "bottom", "left_front", "right_front")

MIN_FACE_COUNT = 3000
MAX_FACE_COUNT = 1500000
DEFAULT_FACE_COUNT = 500000

PROMPT_MAX_LENGTH = 1024


# ===================== Validation =====================

def validate_inputs(args):
    """Validate input arguments."""
    # Must provide prompt or image
    has_prompt = bool(args.prompt)
    has_image = bool(args.image_url or args.image_base64)

    if not has_prompt and not has_image:
        return False, "Must provide either --prompt or --image-url/--image-base64"

    # Prompt and image cannot coexist (except Sketch mode)
    if has_prompt and has_image and args.generate_type != "Sketch":
        return False, "Prompt and ImageUrl/ImageBase64 cannot be used together (except in Sketch mode)"

    # Validate prompt length
    if args.prompt and len(args.prompt) > PROMPT_MAX_LENGTH:
        return False, f"Prompt too long: {len(args.prompt)} chars, max {PROMPT_MAX_LENGTH}"

    # Validate model
    if args.model and args.model not in VALID_MODELS:
        return False, f"Invalid model: {args.model}, must be one of {VALID_MODELS}"

    # Validate generate type
    if args.generate_type and args.generate_type not in VALID_GENERATE_TYPES:
        return False, f"Invalid generate type: {args.generate_type}, must be one of {VALID_GENERATE_TYPES}"

    # 3.1 does not support LowPoly
    if args.model == "3.1" and args.generate_type == "LowPoly":
        return False, "Model 3.1 does not support LowPoly generate type"

    # Validate polygon type
    if args.polygon_type:
        if args.polygon_type not in VALID_POLYGON_TYPES:
            return False, f"Invalid polygon type: {args.polygon_type}, must be one of {VALID_POLYGON_TYPES}"
        if args.generate_type != "LowPoly":
            return False, "PolygonType is only effective in LowPoly generate type"

    # Validate face count
    if args.face_count is not None:
        if args.face_count < MIN_FACE_COUNT or args.face_count > MAX_FACE_COUNT:
            return False, f"Face count {args.face_count} out of range [{MIN_FACE_COUNT}, {MAX_FACE_COUNT}]"

    # Validate result format
    if args.result_format and args.result_format not in VALID_RESULT_FORMATS:
        return False, f"Invalid result format: {args.result_format}, must be one of {VALID_RESULT_FORMATS}"

    # Validate multi-view images
    if args.multi_view:
        try:
            views = json.loads(args.multi_view)
            if not isinstance(views, list):
                return False, "MultiViewImages must be a JSON array"
            for v in views:
                vt = v.get("ViewType", "")
                if vt not in VALID_VIEW_TYPES:
                    return False, f"Invalid ViewType: {vt}, must be one of {VALID_VIEW_TYPES}"
                if not v.get("ViewImageUrl") and not v.get("ViewImageBase64"):
                    return False, f"ViewImage for {vt} must have ViewImageUrl or ViewImageBase64"
        except json.JSONDecodeError:
            return False, "MultiViewImages must be valid JSON"

    return True, ""


# ===================== Argument Parsing =====================

def parse_args():
    """Parse command-line arguments."""
    import argparse

    parser = argparse.ArgumentParser(
        description="HunYuan 3D Generation (submit + auto-poll)"
    )
    parser.add_argument("--prompt", type=str, default=None,
                        help="Text description for 3D generation (Chinese recommended, max 1024 chars)")
    parser.add_argument("--image-url", type=str, default=None,
                        help="Input image URL for image-to-3D (resolution 128~5000, size <= 8MB)")
    parser.add_argument("--image-base64", type=str, default=None,
                        help="Input image Base64 for image-to-3D (resolution 128~5000, size <= 6MB)")
    parser.add_argument("--multi-view", type=str, default=None,
                        help='Multi-view images JSON, e.g., \'[{"ViewType":"back","ViewImageUrl":"https://..."}]\'')
    parser.add_argument("--model", type=str, default=None, choices=["3.0", "3.1"],
                        help="Model version: 3.0 (default) or 3.1")
    parser.add_argument("--enable-pbr", action="store_true", default=False,
                        help="Enable PBR material generation (default: false)")
    parser.add_argument("--face-count", type=int, default=None,
                        help="Face count for 3D model (default: 500000, range: 10000-1500000)")
    parser.add_argument("--generate-type", type=str, default=None,
                        choices=["Normal", "LowPoly", "Geometry", "Sketch"],
                        help="Generation type: Normal, LowPoly, Geometry, Sketch (default: Normal)")
    parser.add_argument("--polygon-type", type=str, default=None,
                        choices=["triangle", "quadrilateral"],
                        help="Polygon type (LowPoly only): triangle, quadrilateral")
    parser.add_argument("--result-format", type=str, default=None,
                        choices=["STL", "USDZ", "FBX"],
                        help="Output format: STL, USDZ, FBX (default: obj+glb)")
    parser.add_argument("--stdin", action="store_true",
                        help="Read JSON parameters from stdin")
    parser.add_argument("--poll-interval", type=int, default=10,
                        help="Polling interval in seconds (default: 10)")
    parser.add_argument("--max-poll-time", type=int, default=600,
                        help="Max total polling time in seconds (default: 600 = 10min)")
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
        args.image_url = data.get("image_url", args.image_url)
        args.image_base64 = data.get("image_base64", args.image_base64)
        args.multi_view = data.get("multi_view", args.multi_view)
        if isinstance(args.multi_view, list):
            args.multi_view = json.dumps(args.multi_view)
        args.model = data.get("model", args.model)
        args.enable_pbr = data.get("enable_pbr", args.enable_pbr)
        args.face_count = data.get("face_count", args.face_count)
        args.generate_type = data.get("generate_type", args.generate_type)
        args.polygon_type = data.get("polygon_type", args.polygon_type)
        args.result_format = data.get("result_format", args.result_format)
        args.region = data.get("region", args.region)

    if not args.prompt and not args.image_url and not args.image_base64:
        print(json.dumps({
            "error": "NO_INPUT",
            "message": "No input provided. Please supply --prompt or --image-url/--image-base64.",
            "usage": {
                "text_to_3d": 'python3 main.py --prompt "一只可爱的卡通猫咪"',
                "image_to_3d": 'python3 main.py --image-url "https://example.com/cat.jpg"',
                "with_pbr": 'python3 main.py --prompt "一个茶壶" --enable-pbr',
                "submit_only": 'python3 main.py --prompt "一只猫" --no-poll',
                "stdin": 'echo \'{"prompt":"一只猫"}\' | python3 main.py --stdin',
            },
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    # Validate inputs
    ok, msg = validate_inputs(args)
    if not ok:
        print(json.dumps({
            "error": "INVALID_INPUT",
            "message": msg,
        }, ensure_ascii=False, indent=2))
        sys.exit(1)

    return args


# ===================== Submit Task =====================

def submit_task(client, args):
    """Submit a SubmitHunyuanTo3DProJob request and return the response."""
    req = models.SubmitHunyuanTo3DProJobRequest()
    params = {}

    if args.prompt:
        params["Prompt"] = args.prompt
    if args.image_url:
        params["ImageUrl"] = args.image_url
    if args.image_base64:
        params["ImageBase64"] = args.image_base64
    if args.model:
        params["Model"] = args.model
    if args.enable_pbr:
        params["EnablePBR"] = True
    if args.face_count is not None:
        params["FaceCount"] = args.face_count
    if args.generate_type:
        params["GenerateType"] = args.generate_type
    if args.polygon_type:
        params["PolygonType"] = args.polygon_type
    if args.result_format:
        params["ResultFormat"] = args.result_format

    # Multi-view images
    if args.multi_view:
        views = json.loads(args.multi_view)
        params["MultiViewImages"] = views

    req.from_json_string(json.dumps(params))
    resp = client.SubmitHunyuanTo3DProJob(req)
    return json.loads(resp.to_json_string())


# ===================== Query Task =====================

def query_task(client, job_id):
    """Query a single task status via QueryHunyuanTo3DProJob."""
    req = models.QueryHunyuanTo3DProJobRequest()
    req.from_json_string(json.dumps({"JobId": job_id}))
    resp = client.QueryHunyuanTo3DProJob(req)
    return json.loads(resp.to_json_string())


# Status: WAIT, RUN, FAIL, DONE
JOB_STATUS_WAIT = "WAIT"
JOB_STATUS_RUN = "RUN"
JOB_STATUS_FAIL = "FAIL"
JOB_STATUS_DONE = "DONE"


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
        status = response.get("Status", "")

        if status == JOB_STATUS_DONE:
            return response
        elif status == JOB_STATUS_FAIL:
            print(json.dumps({
                "error": "TASK_FAILED",
                "job_id": job_id,
                "status": status,
                "error_code": response.get("ErrorCode", ""),
                "error_message": response.get("ErrorMessage", ""),
            }, ensure_ascii=False, indent=2))
            sys.exit(1)

        print(
            f"[INFO] Job {job_id} status: {status}, "
            f"elapsed: {int(elapsed)}s, next poll in {poll_interval}s...",
            file=sys.stderr,
        )
        time.sleep(poll_interval)


# ===================== Format Result =====================

def format_result_files(result_file_3ds):
    """Format ResultFile3Ds into a clean list."""
    files = []
    if not result_file_3ds:
        return files
    for f in result_file_3ds:
        item = {
            "type": f.get("Type", ""),
            "url": f.get("Url", ""),
        }
        if f.get("PreviewImageUrl"):
            item["preview_image_url"] = f["PreviewImageUrl"]
        files.append(item)
    return files


# ===================== Main =====================

def main():
    args = parse_args()
    cred = get_credentials()
    client = build_ai3d_client(cred, args.region)

    try:
        # Step 1: Submit task
        input_desc = args.prompt or args.image_url or "(image-base64)"
        print(f"[INFO] Submitting 3D generation task: {input_desc[:80]}...", file=sys.stderr)
        submit_resp = submit_task(client, args)

        job_id = submit_resp.get("JobId", "")
        if not job_id:
            print(json.dumps({
                "error": "NO_JOB_ID",
                "message": "Failed to get JobId from SubmitHunyuanTo3DProJob response.",
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
        result_files = format_result_files(response.get("ResultFile3Ds"))
        result = {
            "job_id": job_id,
            "status": "success",
            "result_files": result_files,
        }

        print(json.dumps(result, ensure_ascii=False, indent=2))

        # Summary to stderr
        print(f"\n[INFO] 3D model generated successfully!", file=sys.stderr)
        for f in result_files:
            print(f"[INFO]   {f['type']}: {f['url']}", file=sys.stderr)
        print("[INFO] Note: File URLs are valid for 24 hours. Please save promptly.", file=sys.stderr)

    except TencentCloudSDKException as err:
        print(json.dumps({
            "error": "AI3D_API_ERROR",
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
