#!/usr/bin/env python3
"""
HappyHorse Video Magic - Video Generation & Editing Tool

Supports:
- happyhorse-1.0-t2v: Text to Video
- happyhorse-1.0-i2v: Image to Video (first-frame based)
- happyhorse-1.0-r2v: Reference to Video (multi-image character fusion)
- happyhorse-1.0-video-edit: Video Editing (instruction + reference image)
"""

import sys
import json
import requests
import os
import argparse
import base64
import mimetypes

BASE_URL = "https://dashscope.aliyuncs.com"


def get_api_key():
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("Error: DASHSCOPE_API_KEY environment variable is not set.", file=sys.stderr)
        sys.exit(1)
    return api_key


def encode_local_file(path):
    """If path is a local file, return a data URI (data:{mime};base64,...).
    Otherwise return the original string (assumed to be a URL)."""
    if path.startswith(("http://", "https://", "oss://", "data:")):
        return path
    abs_path = os.path.expanduser(path)
    if not os.path.isfile(abs_path):
        print(f"Error: file not found: {abs_path}", file=sys.stderr)
        sys.exit(1)
    mime, _ = mimetypes.guess_type(abs_path)
    if mime is None:
        mime = "application/octet-stream"
    with open(abs_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    print(f"  [base64] Encoded local file: {abs_path} ({mime}, {len(b64)} chars)")
    return f"data:{mime};base64,{b64}"


def get_headers(api_key, async_mode=False):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    if async_mode:
        headers["X-DashScope-Async"] = "enable"
    return headers


# ──────────────────────────────────────────────
#  text2video-gen  (happyhorse-1.0-t2v, HTTP async)
# ──────────────────────────────────────────────
def text2video_gen(args):
    api_key = get_api_key()
    url = f"{BASE_URL}/api/v1/services/aigc/video-generation/video-synthesis"

    input_data = {"prompt": args.prompt}

    parameters = {
        "resolution": args.resolution,
        "ratio": args.ratio,
        "duration": args.duration,
        "watermark": args.watermark,
    }
    if args.seed is not None:
        parameters["seed"] = args.seed

    payload = {
        "model": "happyhorse-1.0-t2v",
        "input": input_data,
        "parameters": parameters,
    }

    headers = get_headers(api_key, async_mode=True)

    print(f"[text2video-gen] Submitting task ...")
    print(f"  Model     : happyhorse-1.0-t2v")
    print(f"  Prompt    : {args.prompt[:80]}..." if len(args.prompt) > 80 else f"  Prompt    : {args.prompt}")
    print(f"  Resolution: {args.resolution}")
    print(f"  Ratio     : {args.ratio}")
    print(f"  Duration  : {args.duration}s")
    print(f"  Watermark : {args.watermark}")

    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    result = resp.json()

    if "code" in result:
        print(f"Error: {result.get('code')} - {result.get('message')}", file=sys.stderr)
        sys.exit(1)

    output = result.get("output", {})
    task_id = output.get("task_id", "")
    task_status = output.get("task_status", "")

    print(f"\nTask submitted successfully!")
    print(f"  Task ID : {task_id}")
    print(f"  Status  : {task_status}")
    print(f"\nTo check the result, run:")
    print(f"  python3 happyhorse-magic.py text2video-get --task-id {task_id}")

    print("\n--- Full Response ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def text2video_get(args):
    api_key = get_api_key()
    url = f"{BASE_URL}/api/v1/tasks/{args.task_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    print(f"[text2video-get] Checking task: {args.task_id}")

    resp = requests.get(url, headers=headers, timeout=60)
    result = resp.json()

    if "code" in result:
        print(f"Error: {result.get('code')} - {result.get('message')}", file=sys.stderr)
        sys.exit(1)

    output = result.get("output", {})
    task_status = output.get("task_status", "")

    print(f"  Task ID : {output.get('task_id', '')}")
    print(f"  Status  : {task_status}")

    if task_status == "SUCCEEDED":
        video_url = output.get("video_url", "")
        print(f"  Video   : {video_url}")
    elif task_status == "FAILED":
        print(f"  Error   : {output.get('code', '')} - {output.get('message', '')}")
    else:
        print(f"\nTask is still {task_status}. Please check again later:")
        print(f"  python3 happyhorse-magic.py text2video-get --task-id {args.task_id}")

    print("\n--- Full Response ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ──────────────────────────────────────────────
#  image2video-gen  (happyhorse-1.0-i2v, HTTP async)
# ──────────────────────────────────────────────
def image2video_gen(args):
    api_key = get_api_key()
    url = f"{BASE_URL}/api/v1/services/aigc/video-generation/video-synthesis"

    # Build media array - only first_frame supported
    media = [{"type": "first_frame", "url": encode_local_file(args.first_frame)}]

    input_data = {"media": media}
    if args.prompt:
        input_data["prompt"] = args.prompt

    parameters = {
        "resolution": args.resolution,
        "duration": args.duration,
        "watermark": args.watermark,
    }
    if args.seed is not None:
        parameters["seed"] = args.seed

    payload = {
        "model": "happyhorse-1.0-i2v",
        "input": input_data,
        "parameters": parameters,
    }

    headers = get_headers(api_key, async_mode=True)

    print(f"[image2video-gen] Submitting task ...")
    print(f"  Model      : happyhorse-1.0-i2v")
    if args.prompt:
        print(f"  Prompt     : {args.prompt[:60]}..." if len(args.prompt) > 60 else f"  Prompt     : {args.prompt}")
    print(f"  First Frame: {args.first_frame}")
    print(f"  Resolution : {args.resolution}")
    print(f"  Duration   : {args.duration}s")

    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    result = resp.json()

    if "code" in result:
        print(f"Error: {result.get('code')} - {result.get('message')}", file=sys.stderr)
        sys.exit(1)

    output = result.get("output", {})
    task_id = output.get("task_id", "")
    task_status = output.get("task_status", "")

    print(f"\nTask submitted successfully!")
    print(f"  Task ID : {task_id}")
    print(f"  Status  : {task_status}")
    print(f"\nTo check the result, run:")
    print(f"  python3 happyhorse-magic.py image2video-get --task-id {task_id}")

    print("\n--- Full Response ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def image2video_get(args):
    api_key = get_api_key()
    url = f"{BASE_URL}/api/v1/tasks/{args.task_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    print(f"[image2video-get] Checking task: {args.task_id}")

    resp = requests.get(url, headers=headers, timeout=60)
    result = resp.json()

    if "code" in result:
        print(f"Error: {result.get('code')} - {result.get('message')}", file=sys.stderr)
        sys.exit(1)

    output = result.get("output", {})
    task_status = output.get("task_status", "")

    print(f"  Task ID : {output.get('task_id', '')}")
    print(f"  Status  : {task_status}")

    if task_status == "SUCCEEDED":
        video_url = output.get("video_url", "")
        print(f"  Video   : {video_url}")
    elif task_status == "FAILED":
        print(f"  Error   : {output.get('code', '')} - {output.get('message', '')}")
    else:
        print(f"\nTask is still {task_status}. Please check again later:")
        print(f"  python3 happyhorse-magic.py image2video-get --task-id {args.task_id}")

    print("\n--- Full Response ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ──────────────────────────────────────────────
#  reference2video-gen  (happyhorse-1.0-r2v, HTTP async)
# ──────────────────────────────────────────────
def reference2video_gen(args):
    api_key = get_api_key()
    url = f"{BASE_URL}/api/v1/services/aigc/video-generation/video-synthesis"

    # Build media array from reference images (1-9 images)
    media = []
    if args.reference_images:
        for ref_image in args.reference_images:
            media.append({"type": "reference_image", "url": encode_local_file(ref_image)})

    if not media:
        print("Error: At least one --reference-images is required.", file=sys.stderr)
        sys.exit(1)

    input_data = {
        "prompt": args.prompt,
        "media": media,
    }

    parameters = {
        "resolution": args.resolution,
        "ratio": args.ratio,
        "duration": args.duration,
        "watermark": args.watermark,
    }
    if args.seed is not None:
        parameters["seed"] = args.seed

    payload = {
        "model": "happyhorse-1.0-r2v",
        "input": input_data,
        "parameters": parameters,
    }

    headers = get_headers(api_key, async_mode=True)

    print(f"[reference2video-gen] Submitting task ...")
    print(f"  Model      : happyhorse-1.0-r2v")
    print(f"  Prompt     : {args.prompt[:60]}..." if len(args.prompt) > 60 else f"  Prompt     : {args.prompt}")
    print(f"  Ref Images : {args.reference_images}")
    print(f"  Resolution : {args.resolution}")
    print(f"  Ratio      : {args.ratio}")
    print(f"  Duration   : {args.duration}s")

    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    result = resp.json()

    if "code" in result:
        print(f"Error: {result.get('code')} - {result.get('message')}", file=sys.stderr)
        sys.exit(1)

    output = result.get("output", {})
    task_id = output.get("task_id", "")
    task_status = output.get("task_status", "")

    print(f"\nTask submitted successfully!")
    print(f"  Task ID : {task_id}")
    print(f"  Status  : {task_status}")
    print(f"\nTo check the result, run:")
    print(f"  python3 happyhorse-magic.py reference2video-get --task-id {task_id}")

    print("\n--- Full Response ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def reference2video_get(args):
    api_key = get_api_key()
    url = f"{BASE_URL}/api/v1/tasks/{args.task_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    print(f"[reference2video-get] Checking task: {args.task_id}")

    resp = requests.get(url, headers=headers, timeout=60)
    result = resp.json()

    if "code" in result:
        print(f"Error: {result.get('code')} - {result.get('message')}", file=sys.stderr)
        sys.exit(1)

    output = result.get("output", {})
    task_status = output.get("task_status", "")

    print(f"  Task ID : {output.get('task_id', '')}")
    print(f"  Status  : {task_status}")

    if task_status == "SUCCEEDED":
        video_url = output.get("video_url", "")
        print(f"  Video   : {video_url}")
    elif task_status == "FAILED":
        print(f"  Error   : {output.get('code', '')} - {output.get('message', '')}")
    else:
        print(f"\nTask is still {task_status}. Please check again later:")
        print(f"  python3 happyhorse-magic.py reference2video-get --task-id {args.task_id}")

    print("\n--- Full Response ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ──────────────────────────────────────────────
#  video-edit  (happyhorse-1.0-video-edit, HTTP async)
# ──────────────────────────────────────────────
def video_edit(args):
    api_key = get_api_key()
    url = f"{BASE_URL}/api/v1/services/aigc/video-generation/video-synthesis"

    # Build media array
    media = [{"type": "video", "url": encode_local_file(args.video)}]

    if args.reference_images:
        for img in args.reference_images:
            media.append({"type": "reference_image", "url": encode_local_file(img)})

    input_data = {
        "prompt": args.prompt,
        "media": media,
    }

    parameters = {
        "resolution": args.resolution,
        "watermark": args.watermark,
        "audio_setting": args.audio_setting,
    }
    if args.seed is not None:
        parameters["seed"] = args.seed

    payload = {
        "model": "happyhorse-1.0-video-edit",
        "input": input_data,
        "parameters": parameters,
    }

    headers = get_headers(api_key, async_mode=True)

    print(f"[video-edit] Submitting task ...")
    print(f"  Model      : happyhorse-1.0-video-edit")
    print(f"  Prompt     : {args.prompt[:60]}..." if len(args.prompt) > 60 else f"  Prompt     : {args.prompt}")
    print(f"  Video      : {args.video}")
    if args.reference_images:
        print(f"  References : {args.reference_images}")
    print(f"  Resolution : {args.resolution}")
    print(f"  Audio      : {args.audio_setting}")

    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    result = resp.json()

    if "code" in result:
        print(f"Error: {result.get('code')} - {result.get('message')}", file=sys.stderr)
        sys.exit(1)

    output = result.get("output", {})
    task_id = output.get("task_id", "")
    task_status = output.get("task_status", "")

    print(f"\nTask submitted successfully!")
    print(f"  Task ID : {task_id}")
    print(f"  Status  : {task_status}")
    print(f"\nTo check the result, run:")
    print(f"  python3 happyhorse-magic.py video-edit-get --task-id {task_id}")

    print("\n--- Full Response ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))


def video_edit_get(args):
    api_key = get_api_key()
    url = f"{BASE_URL}/api/v1/tasks/{args.task_id}"
    headers = {"Authorization": f"Bearer {api_key}"}

    print(f"[video-edit-get] Checking task: {args.task_id}")

    resp = requests.get(url, headers=headers, timeout=60)
    result = resp.json()

    if "code" in result:
        print(f"Error: {result.get('code')} - {result.get('message')}", file=sys.stderr)
        sys.exit(1)

    output = result.get("output", {})
    task_status = output.get("task_status", "")

    print(f"  Task ID : {output.get('task_id', '')}")
    print(f"  Status  : {task_status}")

    if task_status == "SUCCEEDED":
        video_url = output.get("video_url", "")
        print(f"  Video   : {video_url}")
    elif task_status == "FAILED":
        print(f"  Error   : {output.get('code', '')} - {output.get('message', '')}")
    else:
        print(f"\nTask is still {task_status}. Please check again later:")
        print(f"  python3 happyhorse-magic.py video-edit-get --task-id {args.task_id}")

    print("\n--- Full Response ---")
    print(json.dumps(result, ensure_ascii=False, indent=2))


# ──────────────────────────────────────────────
#  CLI entry point
# ──────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="HappyHorse Video Magic - Video Generation & Editing Tool"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- text2video-gen ---
    p = subparsers.add_parser("text2video-gen", help="Submit text-to-video task (happyhorse-1.0-t2v)")
    p.add_argument("--prompt", required=True, help="Text prompt for video generation (max 5000 non-Chinese chars or 2500 Chinese chars)")
    p.add_argument("--resolution", default="1080P", choices=["720P", "1080P"], help="Video resolution (default: 1080P)")
    p.add_argument("--ratio", default="16:9", choices=["16:9", "9:16", "1:1", "4:3", "3:4"], help="Aspect ratio (default: 16:9)")
    p.add_argument("--duration", type=int, default=5, help="Video duration in seconds, 3-15 (default: 5)")
    p.add_argument("--no-watermark", action="store_false", dest="watermark", help="Disable 'Happy Horse' watermark (default: enabled)")
    p.add_argument("--seed", type=int, help="Random seed [0, 2147483647] for reproducibility")

    # --- text2video-get ---
    p = subparsers.add_parser("text2video-get", help="Get text-to-video task result")
    p.add_argument("--task-id", required=True, help="Task ID from text2video-gen")

    # --- image2video-gen ---
    p = subparsers.add_parser("image2video-gen", help="Submit image-to-video task (happyhorse-1.0-i2v)")
    p.add_argument("--prompt", help="Text prompt for video generation (optional)")
    p.add_argument("--first-frame", required=True, help="First frame image URL (required)")
    p.add_argument("--resolution", default="1080P", choices=["720P", "1080P"], help="Video resolution (default: 1080P). Output ratio follows input image.")
    p.add_argument("--duration", type=int, default=5, help="Video duration in seconds, 3-15 (default: 5)")
    p.add_argument("--no-watermark", action="store_false", dest="watermark", help="Disable 'Happy Horse' watermark (default: enabled)")
    p.add_argument("--seed", type=int, help="Random seed [0, 2147483647] for reproducibility")

    # --- image2video-get ---
    p = subparsers.add_parser("image2video-get", help="Get image-to-video task result")
    p.add_argument("--task-id", required=True, help="Task ID from image2video-gen")

    # --- reference2video-gen ---
    p = subparsers.add_parser("reference2video-gen", help="Submit reference-to-video task (happyhorse-1.0-r2v)")
    p.add_argument("--prompt", required=True, help="Text prompt with character references like 'character1', 'character2' (max 5000 non-Chinese chars)")
    p.add_argument("--reference-images", nargs="+", required=True, help="Reference image URLs (1-9 images, use 'character1/character2/...' in prompt)")
    p.add_argument("--resolution", default="1080P", choices=["720P", "1080P"], help="Video resolution (default: 1080P)")
    p.add_argument("--ratio", default="16:9", choices=["16:9", "9:16", "1:1", "4:3", "3:4"], help="Aspect ratio (default: 16:9)")
    p.add_argument("--duration", type=int, default=5, help="Video duration in seconds, 3-15 (default: 5)")
    p.add_argument("--no-watermark", action="store_false", dest="watermark", help="Disable 'Happy Horse' watermark (default: enabled)")
    p.add_argument("--seed", type=int, help="Random seed [0, 2147483647] for reproducibility")

    # --- reference2video-get ---
    p = subparsers.add_parser("reference2video-get", help="Get reference-to-video task result")
    p.add_argument("--task-id", required=True, help="Task ID from reference2video-gen")

    # --- video-edit ---
    p = subparsers.add_parser("video-edit", help="Submit video editing task (happyhorse-1.0-video-edit)")
    p.add_argument("--prompt", required=True, help="Editing instruction (required, max 5000 non-Chinese chars)")
    p.add_argument("--video", required=True, help="Input video URL to edit (mp4/mov, 3-60s, output max 15s)")
    p.add_argument("--reference-images", nargs="+", help="Reference image URLs for editing (0-5 images)")
    p.add_argument("--resolution", default="1080P", choices=["720P", "1080P"], help="Output resolution (default: 1080P)")
    p.add_argument("--audio-setting", default="auto", choices=["auto", "origin"], help="Audio handling: auto (default) or origin (keep original)")
    p.add_argument("--no-watermark", action="store_false", dest="watermark", help="Disable 'Happy Horse' watermark (default: enabled)")
    p.add_argument("--seed", type=int, help="Random seed [0, 2147483647] for reproducibility")

    # --- video-edit-get ---
    p = subparsers.add_parser("video-edit-get", help="Get video editing task result")
    p.add_argument("--task-id", required=True, help="Task ID from video-edit")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Default watermark to True for all commands
    if not hasattr(args, "watermark"):
        args.watermark = True

    command_map = {
        "text2video-gen": text2video_gen,
        "text2video-get": text2video_get,
        "image2video-gen": image2video_gen,
        "image2video-get": image2video_get,
        "reference2video-gen": reference2video_gen,
        "reference2video-get": reference2video_get,
        "video-edit": video_edit,
        "video-edit-get": video_edit_get,
    }

    handler = command_map.get(args.command)
    if handler:
        handler(args)
    else:
        print(f"Unknown command: {args.command}", file=sys.stderr)
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
