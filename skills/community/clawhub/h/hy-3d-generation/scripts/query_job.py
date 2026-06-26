# -*- coding: utf-8 -*-
"""
Query a HunYuan 3D generation task (QueryHunyuanTo3DProJob).
Polls the task status until completion or timeout.
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
                "step3": 'export TENCENTCLOUD_SECRET_ID="your_id" && export TENCENTCLOUD_SECRET_KEY="your_key"',
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


# ===================== Argument Parsing =====================

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Query a HunYuan 3D task (QueryHunyuanTo3DProJob)"
    )
    parser.add_argument("job_id", help="Job ID returned by SubmitHunyuanTo3DProJob")
    parser.add_argument("--poll-interval", type=int, default=10,
                        help="Polling interval in seconds (default: 10)")
    parser.add_argument("--max-poll-time", type=int, default=600,
                        help="Max polling time in seconds (default: 600 = 10min)")
    parser.add_argument("--no-poll", action="store_true",
                        help="Query once without polling (returns current status)")
    parser.add_argument("--region", default="ap-guangzhou",
                        help="Tencent Cloud region (default: ap-guangzhou)")

    return parser.parse_args()


# ===================== Query Task =====================

def query_task(client, job_id):
    """Query a single task status."""
    req = models.QueryHunyuanTo3DProJobRequest()
    req.from_json_string(json.dumps({"JobId": job_id}))
    resp = client.QueryHunyuanTo3DProJob(req)
    return json.loads(resp.to_json_string())


# Status: WAIT, RUN, FAIL, DONE
JOB_STATUS_WAIT = "WAIT"
JOB_STATUS_RUN = "RUN"
JOB_STATUS_FAIL = "FAIL"
JOB_STATUS_DONE = "DONE"


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


# ===================== Main =====================

def main():
    args = parse_args()
    cred = get_credentials()
    client = build_ai3d_client(cred, args.region)

    try:
        if args.no_poll:
            # Single query
            response = query_task(client, args.job_id)
            result = {
                "job_id": args.job_id,
                "status": response.get("Status", ""),
            }
            if response.get("ErrorCode"):
                result["error_code"] = response["ErrorCode"]
                result["error_message"] = response.get("ErrorMessage", "")
            if response.get("ResultFile3Ds"):
                result["result_files"] = format_result_files(response["ResultFile3Ds"])
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # Poll until done
            print(f"[INFO] Polling task {args.job_id}...", file=sys.stderr)
            response = poll_task(client, args.job_id, args.poll_interval, args.max_poll_time)

            result_files = format_result_files(response.get("ResultFile3Ds"))
            result = {
                "job_id": args.job_id,
                "status": "success",
                "result_files": result_files,
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
