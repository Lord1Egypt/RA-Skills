#!/usr/bin/env python3
import argparse
import json
import os
import time
from pathlib import Path

import requests

CREATE_URL = "https://api.minimaxi.com/v1/video_generation"
QUERY_URL = "https://api.minimaxi.com/v1/query/video_generation"
DOWNLOAD_URL = "https://api.minimaxi.com/v1/files/retrieve"


def post_json(url: str, api_key: str, payload: dict) -> dict:
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate video with MiniMax video API")
    parser.add_argument("--prompt", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--model", default="MiniMax-Hailuo-2.3")
    parser.add_argument("--first-frame-image", default=None)
    parser.add_argument("--last-frame-image", default=None)
    parser.add_argument("--subject-reference", default=None)
    parser.add_argument("--timeout", type=int, default=1800)
    args = parser.parse_args()

    api_key = os.environ.get("MINIMAX_API_KEY")
    if not api_key:
        raise SystemExit("MINIMAX_API_KEY is required")

    payload = {"model": args.model, "prompt": args.prompt}
    if args.first_frame_image:
        payload["first_frame_image"] = args.first_frame_image
    if args.last_frame_image:
        payload["last_frame_image"] = args.last_frame_image
    if args.subject_reference:
        payload["subject_reference"] = json.loads(args.subject_reference)

    create_data = post_json(CREATE_URL, api_key, payload)
    task_id = create_data.get("task_id") or create_data.get("data", {}).get("task_id")
    if not task_id:
        raise SystemExit(f"No task id returned: {json.dumps(create_data, ensure_ascii=False)}")

    deadline = time.time() + args.timeout
    file_id = None
    while time.time() < deadline:
        query_response = requests.get(
            QUERY_URL,
            headers={"Authorization": f"Bearer {api_key}"},
            params={"task_id": task_id},
            timeout=60,
        )
        query_response.raise_for_status()
        query_data = query_response.json()
        data = query_data.get("data", query_data)
        status = str(data.get("status", "")).lower()
        file_id = data.get("file_id") or data.get("file", {}).get("file_id")
        if status in {"success", "succeeded", "completed", "done"} and file_id:
            break
        if status in {"fail", "failed", "error"}:
            raise SystemExit(f"Video generation failed: {json.dumps(query_data, ensure_ascii=False)}")
        time.sleep(5)

    if not file_id:
        raise SystemExit("Timed out waiting for video generation")

    file_response = requests.get(
        DOWNLOAD_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        params={"file_id": file_id},
        timeout=120,
    )
    file_response.raise_for_status()
    file_data = file_response.json()
    download_url = file_data.get("file", {}).get("download_url") or file_data.get("data", {}).get("download_url")
    if not download_url:
        raise SystemExit(f"No download url returned: {json.dumps(file_data, ensure_ascii=False)}")

    video_response = requests.get(download_url, timeout=300)
    video_response.raise_for_status()
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(video_response.content)
    print(str(output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
