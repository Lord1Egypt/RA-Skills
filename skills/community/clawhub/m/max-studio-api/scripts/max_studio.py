import argparse
import json
import sys
import time

import requests
from requests import RequestException

BASE_URL = "https://max-studio.store"

ASYNC_ENDPOINTS = {
    "text-to-video",
    "text-to-image",
    "image-to-image",
    "image-to-video",
    "reference-images-to-video",
    "start-end-image-to-video",
    "extend-video",
    "upscale-video",
    "upscale-image",
}

SYNC_ENDPOINTS = {"upload-image"}

ALL_ENDPOINTS = ASYNC_ENDPOINTS | SYNC_ENDPOINTS


class MaxStudioError(Exception):
    pass


def get_api_key(value=None):
    api_key = value
    if not api_key:
        raise MaxStudioError("Missing API key. Provide it via --api-key.")
    return api_key


def get_jwt(value=None, required=True):
    jwt = value
    if required and not jwt:
        raise MaxStudioError("Missing JWT (Google access token). Provide it via --jwt for this endpoint.")
    return jwt


def api_headers(api_key):
    return {"X-API-Key": api_key}


def request_json(method, path, api_key, payload=None, timeout=120, retries=3, retry_delay=2):
    url = f"{BASE_URL}{path}"
    headers = api_headers(api_key)

    for attempt in range(1, retries + 1):
        try:
            if payload is None:
                resp = requests.request(method, url, headers=headers, timeout=timeout)
            else:
                resp = requests.request(
                    method,
                    url,
                    headers={**headers, "Content-Type": "application/json"},
                    json=payload,
                    timeout=timeout,
                )
            resp.raise_for_status()
            return resp.json()
        except RequestException as exc:
            if attempt < retries:
                time.sleep(retry_delay)
            else:
                raise MaxStudioError(f"API request failed after {retries} attempts: {exc}")


def wait_task_completion(api_key, task_id, interval=5, timeout=600):
    elapsed = 0
    while elapsed < timeout:
        data = request_json("GET", f"/api/v1/check-status/{task_id}", api_key)
        status = data.get("status")
        if status in ("successfully", "succeeded"):
            return data
        if status == "failed":
            raise MaxStudioError(data.get("messages") or "Task failed")
        time.sleep(interval)
        elapsed += interval
    raise MaxStudioError("Task timeout")


def download_file(url, output_path):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)


def main():
    parser = argparse.ArgumentParser(description="Max Studio API CLI wrapper")

    subparsers = parser.add_subparsers(dest="command", required=True)

    p_status = subparsers.add_parser("status", help="Check API key status")
    p_status.add_argument("--api-key", required=True, help="Max Studio API key")

    p_run = subparsers.add_parser("run", help="Create a task")
    p_run.add_argument("--api-key", required=True, help="Max Studio API key")
    p_run.add_argument("--jwt", help="JWT (Google access token) for media endpoints")
    p_run.add_argument("--endpoint", required=True, choices=ALL_ENDPOINTS, help="API endpoint to call")
    p_run.add_argument("--prompt", help="Prompt text")
    p_run.add_argument("--json", help="Raw JSON payload string")
    p_run.add_argument("--ratio", default="LANDSCAPE", help="Aspect ratio (e.g., LANDSCAPE/PORTRAIT or 16:9/9:16)")
    p_run.add_argument("--quantity", type=int, default=1, help="Number of results")
    p_run.add_argument("--model", default="Nano_Banana_Pro", help="Model name")
    p_run.add_argument("--wait", action="store_true", help="Wait for async task completion")

    p_download = subparsers.add_parser("download", help="Download a signed URL")
    p_download.add_argument("--url", required=True, help="Signed URL to download")
    p_download.add_argument("--output", required=True, help="Output filename")

    args = parser.parse_args()

    try:
        if args.command == "status":
            data = request_json("GET", "/api/v1/check-apikey-status", args.api_key)
            print(json.dumps(data, indent=2))
            return

        if args.command == "run":
            required_jwt = args.endpoint not in SYNC_ENDPOINTS
            jwt = get_jwt(args.jwt, required=required_jwt)

            if args.json:
                payload = json.loads(args.json)
            else:
                payload = {}
                if args.prompt is not None:
                    payload["prompt"] = args.prompt
                if args.ratio is not None:
                    payload["ratio"] = args.ratio
                if args.quantity is not None:
                    payload["quantity"] = args.quantity
                if args.model is not None:
                    payload["model"] = args.model

            # The API docs indicate JWT field in payload.
            if required_jwt:
                payload["jwt"] = jwt

            data = request_json("POST", f"/api/v1/create-task/{args.endpoint}", args.api_key, payload=payload)

            if args.wait and args.endpoint in ASYNC_ENDPOINTS:
                task_id = data.get("taskid") or data.get("taskId")
                if not task_id:
                    raise MaxStudioError("No task id returned from API")
                data = wait_task_completion(args.api_key, task_id)

            print(json.dumps(data, indent=2))
            return

        if args.command == "download":
            download_file(args.url, args.output)
            print(f"Downloaded to {args.output}")
            return

        parser.print_help()

    except MaxStudioError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
