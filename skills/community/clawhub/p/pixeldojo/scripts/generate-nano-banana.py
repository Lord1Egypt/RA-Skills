#!/usr/bin/env python3
import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request

API_KEY = os.environ.get("PIXELDOJO_API_KEY")
API_BASE = os.environ.get("PIXELDOJO_API_BASE", "https://pixeldojo.ai/api/v1")

if not API_KEY:
    print("Error: PIXELDOJO_API_KEY is not set")
    sys.exit(1)


def http_json(method, url, payload=None, timeout=60):
    data = None
    headers = {"Authorization": f"Bearer {API_KEY}"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            body = response.read().decode("utf-8")
            return response.status, body, json.loads(body)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        return exc.code, body, None


def http_download(url, timeout=120):
    request = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.status, response.read()


parser = argparse.ArgumentParser(
    description="Generate an image with PixelDojo's Nano Banana 2 helper"
)
parser.add_argument("prompt", help="Image prompt")
parser.add_argument("--aspect-ratio", default="16:9", help="Aspect ratio, for example 16:9")
parser.add_argument("--output", help="Output file path")
args = parser.parse_args()

print(f"Submitting Nano Banana 2 job: {args.prompt!r} (AR: {args.aspect_ratio})")

status_code, raw_body, job = http_json(
    "POST",
    f"{API_BASE}/models/nano-banana-2/run",
    payload={
        "prompt": args.prompt,
        "aspect_ratio": args.aspect_ratio,
    },
    timeout=60,
)

if status_code not in (200, 202):
    print(f"Error submitting job: {status_code} {raw_body}")
    sys.exit(1)

job_id = job.get("jobId")
if not job_id:
    print(f"Error: jobId missing in response: {job}")
    sys.exit(1)

print(f"Job submitted. ID: {job_id}")
print("Polling for completion...")

output_url = None
start_time = time.time()
while time.time() - start_time < 180:
    status_code, raw_body, status = http_json(
        "GET",
        f"{API_BASE}/jobs/{job_id}",
        timeout=60,
    )

    if status_code != 200:
        print(f"Error checking status: {status_code} {raw_body}")
        time.sleep(5)
        continue

    state = status.get("status")

    if state == "completed":
        output_data = status.get("output", {})
        images = output_data.get("images", [])
        if images:
            output_url = images[0]
            print(f"Generation complete. URL: {output_url}")
            break
        print("Completed but no image URL was returned")
        sys.exit(1)

    if state == "failed":
        print(f"Job failed: {status.get('error')}")
        sys.exit(1)

    time.sleep(3)

if not output_url:
    print("Timed out waiting for completion")
    sys.exit(1)

if args.output:
    out_path = args.output
else:
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    out_path = f"{os.path.expanduser('~/Pictures/AI Generated/images')}/{timestamp}_nano_banana_gen.png"

os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)

print(f"Downloading to {out_path}...")
try:
    download_status, content = http_download(output_url, timeout=120)
except urllib.error.HTTPError as exc:
    print(f"Failed to download image: {exc.code}")
    sys.exit(1)

if download_status == 200:
    with open(out_path, "wb") as f:
        f.write(content)
    print(f"Saved to {out_path}")
else:
    print(f"Failed to download image: {download_status}")
    sys.exit(1)
