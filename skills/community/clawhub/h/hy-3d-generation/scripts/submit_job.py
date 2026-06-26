# -*- coding: utf-8 -*-
"""
Submit a HunYuan 3D generation task (SubmitHunyuanTo3DProJob).
Returns the JobId for subsequent status polling via query_job.py.
"""

import json
import os
import subprocess
import sys


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
PROMPT_MAX_LENGTH = 1024


# ===================== Validation =====================

def validate_inputs(args):
    """Validate input arguments."""
    has_prompt = bool(args.prompt)
    has_image = bool(args.image_url or args.image_base64)

    if not has_prompt and not has_image:
        return False, "Must provide either --prompt or --image-url/--image-base64"

    if has_prompt and has_image and args.generate_type != "Sketch":
        return False, "Prompt and ImageUrl/ImageBase64 cannot be used together (except in Sketch mode)"

    if args.prompt and len(args.prompt) > PROMPT_MAX_LENGTH:
        return False, f"Prompt too long: {len(args.prompt)} chars, max {PROMPT_MAX_LENGTH}"

    if args.model and args.model not in VALID_MODELS:
        return False, f"Invalid model: {args.model}, must be one of {VALID_MODELS}"

    if args.generate_type and args.generate_type not in VALID_GENERATE_TYPES:
        return False, f"Invalid generate type: {args.generate_type}, must be one of {VALID_GENERATE_TYPES}"

    if args.model == "3.1" and args.generate_type == "LowPoly":
        return False, "Model 3.1 does not support LowPoly generate type"

    if args.polygon_type:
        if args.polygon_type not in VALID_POLYGON_TYPES:
            return False, f"Invalid polygon type: {args.polygon_type}, must be one of {VALID_POLYGON_TYPES}"
        if args.generate_type != "LowPoly":
            return False, "PolygonType is only effective in LowPoly generate type"

    if args.face_count is not None:
        if args.face_count < MIN_FACE_COUNT or args.face_count > MAX_FACE_COUNT:
            return False, f"Face count {args.face_count} out of range [{MIN_FACE_COUNT}, {MAX_FACE_COUNT}]"

    if args.result_format and args.result_format not in VALID_RESULT_FORMATS:
        return False, f"Invalid result format: {args.result_format}, must be one of {VALID_RESULT_FORMATS}"

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
    import argparse

    parser = argparse.ArgumentParser(
        description="Submit a HunYuan 3D generation task (SubmitHunyuanTo3DProJob)"
    )
    parser.add_argument("--prompt", type=str, default=None,
                        help="Text description for 3D generation (Chinese recommended)")
    parser.add_argument("--image-url", type=str, default=None,
                        help="Input image URL for image-to-3D")
    parser.add_argument("--image-base64", type=str, default=None,
                        help="Input image Base64 for image-to-3D")
    parser.add_argument("--multi-view", type=str, default=None,
                        help='Multi-view images JSON')
    parser.add_argument("--model", type=str, default=None, choices=["3.0", "3.1"],
                        help="Model version: 3.0 (default) or 3.1")
    parser.add_argument("--enable-pbr", action="store_true", default=False,
                        help="Enable PBR material generation")
    parser.add_argument("--face-count", type=int, default=None,
                        help="Face count (default: 500000, range: 10000-1500000)")
    parser.add_argument("--generate-type", type=str, default=None,
                        choices=["Normal", "LowPoly", "Geometry", "Sketch"],
                        help="Generation type")
    parser.add_argument("--polygon-type", type=str, default=None,
                        choices=["triangle", "quadrilateral"],
                        help="Polygon type (LowPoly only)")
    parser.add_argument("--result-format", type=str, default=None,
                        choices=["STL", "USDZ", "FBX"],
                        help="Output format")
    parser.add_argument("--stdin", action="store_true",
                        help="Read JSON parameters from stdin")
    parser.add_argument("--region", default="ap-guangzhou",
                        help="Tencent Cloud region (default: ap-guangzhou)")

    args = parser.parse_args()

    # Handle stdin input
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
                "text_to_3d": 'python3 submit_job.py --prompt "一只可爱的卡通猫咪"',
                "image_to_3d": 'python3 submit_job.py --image-url "https://example.com/cat.jpg"',
                "stdin": 'echo \'{"prompt":"一只猫"}\' | python3 submit_job.py --stdin',
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
    """Submit a SubmitHunyuanTo3DProJob request."""
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

    if args.multi_view:
        views = json.loads(args.multi_view)
        params["MultiViewImages"] = views

    req.from_json_string(json.dumps(params))
    resp = client.SubmitHunyuanTo3DProJob(req)
    return json.loads(resp.to_json_string())


# ===================== Main =====================

def main():
    args = parse_args()
    cred = get_credentials()
    client = build_ai3d_client(cred, args.region)

    try:
        response = submit_task(client, args)

        result = {
            "job_id": response.get("JobId", ""),
            "request_id": response.get("RequestId", ""),
            "message": "Task submitted successfully. Use query_job.py to poll for results.",
        }

        print(json.dumps(result, ensure_ascii=False, indent=2))

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
