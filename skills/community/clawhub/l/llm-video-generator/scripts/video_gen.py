#!/opt/anaconda3/bin/python3
"""
Video generation using ZhipuAI CogVideoX-3 model.

Supports three modes:
  1. text2video   - Generate video from text prompt
  2. image2video  - Generate video from a starting image + text prompt
  3. frames2video - Generate video from first/last frame images + text prompt

Usage:
    python video_gen.py text2video --prompt "A cat playing" [options]
    python video_gen.py image2video --prompt "Make it move" --image-url <url_or_path> [options]
    python video_gen.py frames2video --prompt "Transition" --first-frame <url> --last-frame <url> [options]

Each generation produces ~5 seconds of video.

Environment:
    ZHIPU_API_KEY  Required. ZhipuAI API key.
"""

import argparse
import base64
import json
import os
import sys
import time
import urllib.request


def get_client():
    from zai import ZhipuAiClient
    api_key = os.environ.get("ZHIPU_API_KEY")
    if not api_key:
        print("ERROR: ZHIPU_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)
    return ZhipuAiClient(api_key=api_key)


def generate_text2video(client, prompt, quality="quality", with_audio=True, size="1920x1080", fps=30):
    """Mode 1: Text to video."""
    print(f"[text2video] Submitting...")
    print(f"  Prompt: {prompt}")
    response = client.videos.generations(
        model="cogvideox-3",
        prompt=prompt,
        quality=quality,
        with_audio=with_audio,
        size=size,
        fps=fps,
    )
    print(f"  Task ID: {response.id}")
    return response


def generate_image2video(client, prompt, image_url, quality="quality", with_audio=True, size="1920x1080", fps=30):
    """Mode 2: Image + text to video."""
    print(f"[image2video] Submitting...")
    print(f"  Prompt: {prompt}")
    print(f"  Image: {image_url[:100]}...")
    response = client.videos.generations(
        model="cogvideox-3",
        prompt=prompt,
        image_url=image_url,
        quality=quality,
        with_audio=with_audio,
        size=size,
        fps=fps,
    )
    print(f"  Task ID: {response.id}")
    return response


def generate_frames2video(client, prompt, first_frame, last_frame, quality="quality", with_audio=True, size="1920x1080", fps=30):
    """Mode 3: First + last frame to video."""
    print(f"[frames2video] Submitting...")
    print(f"  Prompt: {prompt}")
    print(f"  First frame: {first_frame[:100]}...")
    print(f"  Last frame: {last_frame[:100]}...")
    response = client.videos.generations(
        model="cogvideox-3",
        prompt=prompt,
        image_url=[first_frame, last_frame],
        quality=quality,
        with_audio=with_audio,
        size=size,
        fps=fps,
    )
    print(f"  Task ID: {response.id}")
    return response


def poll_result(client, task_id, interval=10, max_wait=600):
    """Poll until video generation completes."""
    print(f"\nPolling for result (interval={interval}s, max_wait={max_wait}s)...")
    elapsed = 0
    while elapsed < max_wait:
        result = client.videos.retrieve_videos_result(id=task_id)
        status = getattr(result, "task_status", None) or "unknown"
        print(f"  [{elapsed}s] Status: {status}")

        if status.upper() in ("SUCCESS", "SUCCEEDED"):
            return result
        if status.upper() in ("FAIL", "FAILED"):
            print(f"ERROR: Task failed. Detail: {result}", file=sys.stderr)
            sys.exit(1)

        time.sleep(interval)
        elapsed += interval

    print(f"ERROR: Timed out after {max_wait}s.", file=sys.stderr)
    sys.exit(1)


def extract_video_url(result):
    """Extract video URL from result object."""
    if hasattr(result, "video_result") and result.video_result:
        for item in result.video_result:
            if hasattr(item, "url"):
                return item.url
    if hasattr(result, "results") and result.results:
        for item in result.results:
            if hasattr(item, "url"):
                return item.url
    return None


def download_video(url, output_path):
    """Download video from URL."""
    print(f"Downloading video to {output_path}...")
    urllib.request.urlretrieve(url, output_path)
    size_mb = os.path.getsize(output_path) / 1024 / 1024
    print(f"  Done. File size: {size_mb:.1f} MB")
    return output_path


def image_to_base64_url(image_path):
    """Convert a local image file to a base64 data URL."""
    ext = os.path.splitext(image_path)[1].lower()
    mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
    mime = mime_map.get(ext, "image/png")
    with open(image_path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"


def main():
    parser = argparse.ArgumentParser(description="Video generation via ZhipuAI CogVideoX-3")
    subparsers = parser.add_subparsers(dest="mode", required=True)

    # Common args
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--prompt", required=True, help="Text description / prompt")
    common.add_argument("--quality", default="quality", choices=["quality", "speed"])
    common.add_argument("--audio", default="true", choices=["true", "false"])
    common.add_argument("--size", default="1920x1080")
    common.add_argument("--fps", type=int, default=30, choices=[30, 60])
    common.add_argument("--output-dir", default=".", help="Output directory")
    common.add_argument("--poll-interval", type=int, default=10)
    common.add_argument("--max-wait", type=int, default=600)

    # text2video
    subparsers.add_parser("text2video", parents=[common], help="Generate video from text")

    # image2video
    p_img = subparsers.add_parser("image2video", parents=[common], help="Generate video from image + text")
    p_img.add_argument("--image-url", required=True, help="Image URL or local file path")

    # frames2video
    p_frames = subparsers.add_parser("frames2video", parents=[common], help="Generate video from first/last frames + text")
    p_frames.add_argument("--first-frame", required=True, help="First frame image URL or local path")
    p_frames.add_argument("--last-frame", required=True, help="Last frame image URL or local path")

    args = parser.parse_args()
    client = get_client()

    common_kwargs = dict(
        quality=args.quality,
        with_audio=(args.audio == "true"),
        size=args.size,
        fps=args.fps,
    )

    if args.mode == "text2video":
        response = generate_text2video(client, args.prompt, **common_kwargs)
    elif args.mode == "image2video":
        img = args.image_url
        if os.path.isfile(img):
            img = image_to_base64_url(img)
        response = generate_image2video(client, args.prompt, img, **common_kwargs)
    elif args.mode == "frames2video":
        ff = args.first_frame
        lf = args.last_frame
        if os.path.isfile(ff):
            ff = image_to_base64_url(ff)
        if os.path.isfile(lf):
            lf = image_to_base64_url(lf)
        response = generate_frames2video(client, args.prompt, ff, lf, **common_kwargs)

    task_id = response.id

    # Save task info
    os.makedirs(args.output_dir, exist_ok=True)
    task_info = {
        "task_id": task_id,
        "mode": args.mode,
        "prompt": args.prompt,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    task_path = os.path.join(args.output_dir, f"task_{task_id}.json")
    with open(task_path, "w") as f:
        json.dump(task_info, f, indent=2, ensure_ascii=False)

    # Poll
    result = poll_result(client, task_id, interval=args.poll_interval, max_wait=args.max_wait)
    video_url = extract_video_url(result)

    if video_url:
        output_file = os.path.join(args.output_dir, f"video_{task_id}.mp4")
        download_video(video_url, output_file)
        print(f"\n🎬 Video saved: {output_file}")
        # Output JSON summary for script chaining
        summary = {"task_id": task_id, "video_path": output_file, "video_url": video_url, "status": "success"}
        summary_path = os.path.join(args.output_dir, f"result_{task_id}.json")
        with open(summary_path, "w") as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        print(f"📋 Result summary: {summary_path}")
    else:
        print(f"⚠️ No video URL found in result: {result}")
        sys.exit(1)


if __name__ == "__main__":
    main()
