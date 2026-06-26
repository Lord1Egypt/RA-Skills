# -*- coding: utf-8 -*-
"""
Query a HunYuan text-to-image generation task (QueryTextToImageJob).
Polls the task status until completion or timeout.
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


# ===================== Argument Parsing =====================

def parse_args():
    import argparse

    parser = argparse.ArgumentParser(
        description="Query a HunYuan Text-to-Image task (QueryTextToImageJob)"
    )
    parser.add_argument("job_id", help="Job ID returned by SubmitTextToImageJob")
    parser.add_argument("--poll-interval", type=int, default=5,
                        help="Polling interval in seconds (default: 5)")
    parser.add_argument("--max-poll-time", type=int, default=300,
                        help="Max polling time in seconds (default: 300 = 5min)")
    parser.add_argument("--no-poll", action="store_true",
                        help="Query once without polling (returns current status)")
    parser.add_argument("--region", default="ap-guangzhou",
                        help="Tencent Cloud region (default: ap-guangzhou)")

    args = parser.parse_args()
    return args


# ===================== Query Task =====================

def query_task(client, job_id):
    """Query a single task status."""
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
        if args.no_poll:
            # Single query
            response = query_task(client, args.job_id)
            result = {
                "job_id": args.job_id,
                "status_code": response.get("JobStatusCode", ""),
                "status_msg": response.get("JobStatusMsg", ""),
            }
            if response.get("JobErrorCode"):
                result["error_code"] = response["JobErrorCode"]
                result["error_msg"] = response.get("JobErrorMsg", "")
            if response.get("ResultImage"):
                result["result_image"] = response["ResultImage"]
            if response.get("ResultDetails"):
                result["result_details"] = response["ResultDetails"]
            if response.get("RevisedPrompt"):
                result["revised_prompt"] = response["RevisedPrompt"]
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            # Poll until done
            print(f"[INFO] Polling task {args.job_id}...", file=sys.stderr)
            response = poll_task(client, args.job_id, args.poll_interval, args.max_poll_time)

            result = {
                "job_id": args.job_id,
                "status": "success",
                "result_image": response.get("ResultImage", ""),
            }

            if response.get("ResultDetails"):
                result["result_details"] = response["ResultDetails"]
            if response.get("RevisedPrompt"):
                result["revised_prompt"] = response["RevisedPrompt"]

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
