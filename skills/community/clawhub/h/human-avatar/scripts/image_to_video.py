#!/usr/bin/env python3
"""
万相图生视频 (wan2.x-i2v)

SECURITY NOTES:
- subprocess: used ONLY for ffmpeg image format conversion. No shell=True.
- OSS credentials: env-only, used ONLY to upload user media to their own
  OSS bucket and generate signed GET URLs for Alibaba Cloud API access.
- All API calls target dashscope.aliyuncs.com (Alibaba Cloud official).
默认模型：wan2.6-i2v-flash

用法:
  python image_to_video.py --image ./portrait.jpg --prompt "她在草地上微笑跳舞" --download
  python image_to_video.py --image-url https://... --prompt "..." --model wan2.2-i2v-plus
  python image_to_video.py --image ./portrait.jpg --audio ./bgm.mp3 --prompt "..." --download
  python image_to_video.py --image ./portrait.jpg --resolution 720P --duration 5 --download

  # 先文生图再图生视频（一条龙）
  python image_to_video.py --t2i-prompt "一位身着汉服的女性站在桃花林中" --prompt "她缓缓转身，花瓣飘落" --download
"""

import argparse
import json
import os
import sys
import time
import urllib.request
from pathlib import Path

import requests

BASE_URL = os.getenv("DASHSCOPE_BASE_URL", "https://dashscope.aliyuncs.com")
_OSS_SIGNED_URL_EXPIRES = int(os.environ.get("OSS_SIGNED_URL_EXPIRES", str(3 * 24 * 3600)))


def _headers(async_mode: bool = True) -> dict:
    key = os.environ.get("DASHSCOPE_API_KEY")
    if not key:
        raise RuntimeError("DASHSCOPE_API_KEY not set")
    h = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    if async_mode:
        h["X-DashScope-Async"] = "enable"
    return h


def _wait_task(task_id: str, interval: int = 10, max_wait: int = 600) -> dict:
    url = f"{BASE_URL}/api/v1/tasks/{task_id}"
    start = time.time()
    while time.time() - start < max_wait:
        r = requests.get(url, headers=_headers(async_mode=False), timeout=30)
        r.raise_for_status()
        data = r.json()
        out = data.get("output", {})
        status = out.get("task_status", "UNKNOWN")
        elapsed = int(time.time() - start)
        print(f"  [{elapsed}s] status={status}")
        if status == "SUCCEEDED":
            return out
        if status in ("FAILED", "CANCELED", "UNKNOWN"):
            raise RuntimeError(f"Task failed: {json.dumps(data, ensure_ascii=False)}")
        time.sleep(interval)
    raise TimeoutError(f"Task {task_id} timed out")


def upload_to_oss(local_path: str, expires: int = _OSS_SIGNED_URL_EXPIRES) -> str:
    """Upload to OSS, return signed GET URL (default 3 days)."""
    import oss2
    auth = oss2.Auth(
        os.environ["ALIBABA_CLOUD_ACCESS_KEY_ID"],
        os.environ["ALIBABA_CLOUD_ACCESS_KEY_SECRET"],
    )
    bucket_name = os.environ["OSS_BUCKET"]
    endpoint = os.environ.get("OSS_ENDPOINT", "oss-cn-beijing.aliyuncs.com")
    endpoint = endpoint.replace("https://", "").replace("http://", "").rstrip("/")
    bucket = oss2.Bucket(auth, f"https://{endpoint}", bucket_name)
    key = f"human-avatar/{Path(local_path).name}"
    print(f"[oss] uploading {Path(local_path).name} …")
    bucket.put_object_from_file(key, local_path)
    url = bucket.sign_url("GET", key, expires)
    print(f"[oss] signed_url ok ({expires//3600}h)")
    return url


def convert_image(src: str) -> str:
    """Convert image to jpg/png if not compatible."""
    import shutil, subprocess
    p = Path(src)
    if p.suffix.lower() in (".jpg", ".jpeg", ".png", ".bmp", ".webp"):
        return src
    ff = shutil.which("ffmpeg") or "ffmpeg"
    dst = f"/tmp/i2v_img_{p.stem}.jpg"
    subprocess.run([ff, "-y", "-i", src, "-q:v", "2", dst], check=True, capture_output=True)
    return dst


def image_to_video(
    img_url: str,
    prompt: str = "",
    model: str = "wan2.6-i2v-flash",
    resolution: str = "720P",
    duration: int = 5,
    negative_prompt: str = "",
    prompt_extend: bool = True,
    audio_url: str = None,
    audio: bool = True,
) -> str:
    """
    Call 万相 image-to-video API. Returns video URL.

    Args:
        img_url:         首帧图像 URL（公网可访问）或 base64
        prompt:          描述视频动作的提示词
        model:           模型名，默认 wan2.6-i2v-flash
        resolution:      分辨率，480P / 720P（默认 720P）
        duration:        视频时长（秒），wan2.6 支持 3/5/10s，默认 5
        negative_prompt: 反向提示词
        prompt_extend:   是否开启提示词智能改写
        audio_url:       自定义背景音频 URL（可选，wan2.6/2.5 支持）
        audio:           是否生成音频（wan2.6 默认 True；False=无声）
    """
    endpoint = f"{BASE_URL}/api/v1/services/aigc/video-generation/video-synthesis"

    inp = {"img_url": img_url}
    if prompt:
        inp["prompt"] = prompt
    if negative_prompt:
        inp["negative_prompt"] = negative_prompt
    if audio_url:
        inp["audio_url"] = audio_url

    params = {
        "resolution": resolution,
        "prompt_extend": prompt_extend,
        "duration": duration,
    }
    # wan2.6-i2v-flash generates audio by default; set False to disable
    if not audio:
        params["audio"] = False

    payload = {"model": model, "input": inp, "parameters": params}

    print(f"\n[i2v] submit  model={model}  resolution={resolution}  duration={duration}s")
    r = requests.post(endpoint, headers=_headers(async_mode=True), json=payload, timeout=60)
    r.raise_for_status()
    data = r.json()
    task_id = (data.get("output") or {}).get("task_id")
    if not task_id:
        raise RuntimeError(f"No task_id: {json.dumps(data, ensure_ascii=False)}")
    print(f"  task_id={task_id}")

    out = _wait_task(task_id, interval=10, max_wait=600)
    video_url = out.get("video_url")
    if not video_url:
        raise RuntimeError(f"No video_url in result: {out}")
    print(f"\n✅ video_url = {video_url}")
    return video_url


def main():
    p = argparse.ArgumentParser(description="万相图生视频")
    # image input
    img_grp = p.add_mutually_exclusive_group()
    img_grp.add_argument("--image", help="本地图片路径（自动上传 OSS）")
    img_grp.add_argument("--image-url", help="图片公网 URL")
    img_grp.add_argument("--t2i-prompt", help="先文生图再图生视频（调用 text_to_image）")

    p.add_argument("--prompt", default="", help="描述视频内容的提示词")
    p.add_argument("--model", default="wan2.6-i2v-flash",
                   help="模型名 (default: wan2.6-i2v-flash)，可选: wan2.5-i2v-preview, wan2.2-i2v-plus 等")
    p.add_argument("--t2i-model", default="wan2.2-t2i-flash",
                   help="文生图模型（--t2i-prompt 模式下使用，default: wan2.2-t2i-flash）")
    p.add_argument("--resolution", default="720P", choices=["480P", "720P"],
                   help="分辨率 (default: 720P)")
    p.add_argument("--duration", type=int, default=5, choices=[3, 5, 10],
                   help="视频时长（秒），default: 5")
    p.add_argument("--negative-prompt", default="", help="反向提示词")
    p.add_argument("--no-prompt-extend", action="store_true", help="关闭提示词智能改写")
    p.add_argument("--audio-url", default=None, help="背景音频 URL（wan2.6/2.5 支持）")
    p.add_argument("--no-audio", action="store_true", help="生成无声视频")
    p.add_argument("--download", action="store_true", help="下载生成视频到本地")
    p.add_argument("--output", default="i2v_output.mp4", help="输出文件名")
    args = p.parse_args()

    # ── get image URL ────────────────────────────────────────────────────
    img_url = args.image_url
    tmp_files = []

    if args.t2i_prompt:
        # Generate image first using text_to_image
        print(f"\n[step0] text-to-image  model={args.t2i_model}")
        from text_to_image import text_to_image
        images = text_to_image(
            prompt=args.t2i_prompt,
            model=args.t2i_model,
            size="960*1696",  # 9:16 default for portrait
            n=1,
            prompt_extend=not args.no_prompt_extend,
        )
        img_url = images[0]
        print(f"  t2i image_url = {img_url}")

    elif args.image:
        converted = convert_image(args.image)
        if converted != args.image:
            tmp_files.append(converted)
        img_url = upload_to_oss(converted)

    if not img_url:
        p.error("需要 --image, --image-url 或 --t2i-prompt 之一")

    # ── submit i2v ───────────────────────────────────────────────────────
    try:
        video_url = image_to_video(
            img_url=img_url,
            prompt=args.prompt,
            model=args.model,
            resolution=args.resolution,
            duration=args.duration,
            negative_prompt=args.negative_prompt,
            prompt_extend=not args.no_prompt_extend,
            audio_url=args.audio_url,
            audio=not args.no_audio,
        )

        if args.download:
            print(f"Downloading → {args.output} …")
            urllib.request.urlretrieve(video_url, args.output)
            size_kb = Path(args.output).stat().st_size // 1024
            print(f"Saved {args.output} ({size_kb}KB)")

    finally:
        for f in tmp_files:
            try:
                os.unlink(f)
            except Exception:
                pass


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nERROR: {e}", file=sys.stderr)
        sys.exit(1)
