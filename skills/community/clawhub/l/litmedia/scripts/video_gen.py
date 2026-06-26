#!/usr/bin/env python3
"""Generate videos using Litmedia Common Task APIs.

## AGENT INSTRUCTIONS — READ FIRST
- Default workflow: ALWAYS use `run` (submit + auto-poll).
  Do NOT ask the user to run query manually.
- Only use `query` when `run` has already timed out and a taskId exists,
  or when the user explicitly provides a taskId to resume.
- When using `query`, keep polling (default timeout=900s) until
  status is 'success' or 'fail'. Do NOT stop after a single check.
- Never hand a pending taskId back to the user and say "check it later".
  Always poll to completion within the timeout window.

Supported task types:
    i2v   Image-to-Video      — generate video from a first/end frame image
    t2v   Text-to-Video       — generate video from a text prompt
    extend Video Extension    — generate video from an input video + prompt
    anim   Animation          — generate animation from an input image + style + prompt
    a2ls  Audio-to-Lip-sync   — generate lip-synced video from an input image + audio + prompt

Subcommands:
    run     Submit task AND poll until done — DEFAULT, use this first
    submit  Submit only, print taskId, exit — use for parallel batch jobs
    query   Poll an existing taskId until done (or timeout) — use for recovery

Usage:
    python video_gen.py run  --type i2v  --model "LitAI 5" --first-frame <fileId|path> --prompt "..." [options]
    python video_gen.py run  --type t2v  --model "LitAI 5" --prompt "..." [options]
    python video_gen.py run  --type extend --model "LitAI 5" --input_video <fileId|path> --prompt "..." [options]
    python video_gen.py run  --type anim --model "LitAI 5" --input_image <fileId|path> --prompt "..." options
    python video_gen.py run  --type a2ls --model "LitAI 5" --input_image <fileId|path> --input_sound <fileId|path> --prompt "..." [options]
    python video_gen.py query  --type <i2v|t2v|extend|anim|a2ls> --task-id <taskId> [options]
    
"""

import argparse
import json as json_mod
import os
import sys
import time
import uuid
import datetime
import tempfile

sys.path.insert(0, os.path.dirname(__file__))

from typing import Any
from shared.client import LitMediaClient, LitMediaError
from shared.upload import resolve_local_file
from shared.media_util import MediaUtils

TASK_TYPES = ("i2v", "t2v", "extend", "anim", "a2ls")

ENDPOINTS = {
    "i2v": {
        "submit": "/lit-video/do-image-video",
        "query": "/lit-video/do-process",
    },
    "t2v": {
        "submit": "/lit-video/do-text-video",
        "query": "/lit-video/do-process",
    },
    "extend": { 
        "submit": "/lit-video/do-extend-video",
        "query": "/lit-video/do-process",
    },
    "anim": { 
        "submit": "/lit-video/ai-animation",
        "query": "/lit-video/do-process",
    },
    "a2ls": { 
        "submit": "/lit-video/image-lip-sync",
        "query": "/lit-video/do-process",
    },
}

DEFAULT_TIMEOUT = 900
DEFAULT_INTERVAL = 30

# ---------------------------------------------------------------------------
# Model constraints — `model` must use display names, NOT code names.
# Each entry: { "aspectRatio": list|None, "resolution": list|None, "duration": str }
#   None = not supported / do not send
# ---------------------------------------------------------------------------

I2V_MODELS = {
    "LitAI 5":                      {"aspectRatio": None,                                          "resolution": [360, 540, 720, 1080],        "duration": "5,8,12",   "nativeAudio": True,  "inputMode": "first_end"},
    "Seedance 2.0":                 {"aspectRatio": ["9:16", "3:4", "1:1", "4:3", "16:9"],         "resolution": [480, 720],              "duration": "5,10,15",   "nativeAudio": True,  "inputMode": "first_end"},
    "Seedance 2.0 Fast":            {"aspectRatio": ["9:16", "3:4", "1:1", "4:3", "16:9"],         "resolution": [480, 720],              "duration": "5,10,15",   "nativeAudio": True,  "inputMode": "first_end"},
    "Seedance 1.5 Pro":             {"aspectRatio": ["9:16", "3:4", "1:1", "4:3", "16:9"],         "resolution": [480, 720],       "duration": "5",   "nativeAudio": True,  "inputMode": "first_end"},
    "Kling V3":                     {"aspectRatio": None,                                          "resolution": [480, 720],       "duration": "5,10,15",   "nativeAudio": True,  "inputMode": "first_end"},
    "LoveAI 1.0":                   {"aspectRatio": None,                                          "resolution": [480, 720, 1080],       "duration": "5,10","nativeAudio": False, "inputMode": "first_end"},
}

T2V_MODELS = {
    "LitAI 5":                      {"aspectRatio": ["9:16", "1:1", "4:3", "16:9"],                "resolution": [360, 540, 720, 1080],        "duration": "5,8,12",   "nativeAudio": True},
    "Seedance 2.0":                 {"aspectRatio": ["9:16", "3:4", "1:1", "4:3", "16:9"],         "resolution": [480, 720],              "duration": "5,10,15",   "nativeAudio": True},
    "Seedance 2.0 Fast":            {"aspectRatio": ["9:16", "3:4", "1:1", "4:3", "16:9"],         "resolution": [480, 720],              "duration": "5,10,15",   "nativeAudio": True},
    "Seedance 1.5 Pro":             {"aspectRatio": ["9:16", "3:4", "1:1", "4:3", "16:9"],         "resolution": [480, 720],        "duration": "5",   "nativeAudio": True},
    "Kling V3":                     {"aspectRatio": ["9:16", "1:1", "16:9"],                       "resolution": [480, 720],        "duration": "5,10,15",   "nativeAudio": True},
    "Wan 2.6":                      {"aspectRatio": ["9:16", "3:4", "1:1", "4:3", "16:9"],         "resolution": [720, 1080],       "duration": "5,10","nativeAudio": True},
}


EXTEND_MODELS = {
    "LitAI 5":              {"aspectRatio": None, "resolution": None,  "duration": "5,8",  "internetSearch": False,  "nativeAudio": False},
}

ANIM_MODELS = {
    "LitAI 5":              {"style": ["","comic", "anime", "3d_animation", "clay", "cyberpunk"], "aspectRatio": None, "resolution": [360, 540, 720, 1080],  "duration": "5,8", "nativeAudio": False, "inputMode": "first_end"},
}

A2LS_MODELS = {
    "LitAI 5":              {"sound_speed": "0.5-2.0", "aspectRatio": None, "resolution": None,  "duration": None, "nativeAudio": True, "inputMode": "first_end"},
}

MODEL_REGISTRY = {"i2v": I2V_MODELS, "t2v": T2V_MODELS, "extend": EXTEND_MODELS, "anim": ANIM_MODELS, "a2ls": A2LS_MODELS}
# ---------------------------------------------------------------------------
# Per-second pricing rates (credits, generatingCount=1).
# Key: (resolution_or_0, sound_on_or_None). 0 = resolution-independent, None = sound irrelevant.
# totalCost = rate * duration * generatingCount
# See references/api-docs.md for full pricing tables.
# ---------------------------------------------------------------------------

_RATE = {
    "Standard":                {(0, None): 1.0},
    "Fast":                    {(0, None): 1.0},
    "Seedance 1.5 Pro":        {(720, False): 0.12, (720, True): 0.25, (1080, False): 0.28, (1080, True): 0.55},
    "Seedance 1.0 Pro Fast":   {(720, None): 0.07, (1080, None): 0.15},
    "Seedance 1.0 Pro":        {(720, None): 0.20, (1080, None): 0.45},
    "LitAI 5":        {(720, None): 0.20, (1080, None): 0.10},
    "Kling V3":                {(720, False): 0.50, (720, True): 0.80, (1080, False): 0.80, (1080, True): 1.00},
    "Kling V3 Reference Video":{(720, False): 0.50, (720, True): 0.80, (1080, False): 0.80, (1080, True): 1.00},
    "Kling O3":                {(720, False): 0.50, (720, True): 0.60, (1080, False): 0.80, (1080, True): 0.90},
    "Kling O3 Reference-to-Video": {(720, False): 0.50, (720, True): 0.60, (1080, False): 0.80, (1080, True): 0.90},
    "Kling 2.6":               {(0, False): 0.31, (0, True): 0.65},
    "Kling O1 Reference-to-Video": {(1080, None): 0.50},
    "Kling 2.5 Turbo Pro":     {(1080, None): 0.31},
    "Kling 2.5 Turbo Std":     {(1080, None): 0.20},
    "Sora 2":                  {(0, None): 0.56},
    "Sora 2 Pro":              {(720, None): 1.68, (1080, None): 2.80},
    "Veo 3.1":                 {(720, False): 1.10, (720, True): 2.20, (1080, False): 1.10, (1080, True): 2.20, (2160, False): 2.20, (2160, True): 3.30},
    "Veo 3.1 Reference to video": {(720, False): 1.10, (720, True): 2.20, (1080, False): 1.10, (1080, True): 2.20, (2160, False): 2.20, (2160, True): 3.30},
    "Veo 3.1 Fast":            {(720, False): 0.60, (720, True): 0.90, (1080, False): 0.60, (1080, True): 0.90, (2160, False): 1.70, (2160, True): 2.00},
    "Veo 3.1 Fast Reference to video": {(720, False): 0.60, (720, True): 0.90, (1080, False): 0.60, (1080, True): 0.90, (2160, False): 1.70, (2160, True): 2.00},
    "MiniMax-Hailuo-02":       {(768, None): 0.32, (1080, None): 0.47},
    "MiniMax-Hailuo-2.3":      {(768, None): 0.32, (1080, None): 0.47},
    "MiniMax-Hailuo-2.3-Fast": {(768, None): 0.18, (1080, None): 0.30},
    "Vidu Q3 Pro":             {(540, None): 0.40, (720, None): 0.90, (1080, None): 1.00},
    "Vidu Q2":                 {(1080, None): 0.28},
    "Vidu Q2 Reference to Video": {(1080, None): 0.56},
    "Wan 2.6":                 {(720, None): 0.46, (1080, None): 0.77},
    "Kling O3 Video-Edit":     {(720, None): 1.70, (1080, None): 2.00},
    "Kling O1 Video-Edit":     {(0, None): 0.80},
}

MODEL_MAP = {
    "litvideo": 1,
    "pix": 2,
    "vidu1.5": 3,
    "jimeng/seedance 1.0 lite -安全版": 4,
    "kling1.6": 5,
    "viduq1": 6,
    "vidu2.0": 7,
    "wan2.2": 8,
    "LoveAI 1.0": 9,
    "veo3 fast": 10,
    "veo3": 11,
    "minimax-hailuo-02": 12,
    "viduq2 pro": 13,
    "viduq2 turbo": 14,
    "wan2.5": 15,
    "sora2": 16,
    "sora2-pro": 17,
    "veo3.1-fast": 18,
    "veo3.1-pro": 19,
    "viduq2": 20,
    "minimax-hailuo-2.3(海螺活动专用)": 21,
    "minimax-hailuo-2.3 fast(海螺活动专用)": 22,
    "Seedance 1.0 pro -安全版": 23,
    "Seedance 1.0 pro fast -安全版": 24,
    "minimax-hailuo-2.3": 25,
    "minimax-hailuo-2.3 fast": 26,
    "LitAI 5 pro": 27,
    "viduq2-参考生音视频模型": 28,
    "kling-2.5 turbo": 29,
    "Seedance 1.5 Pro": 30,
    "Wan 2.6": 31,
    "kling o1": 32,
    "kling 2.6": 33,
    "vidu q2 pro fast": 34,
    "sora2 free": 35,
    "LitAI 5": 1,
    "kling ai（数字人专用）": 37,
    "wan 2.6  flash": 38,
    "Seedance 1.5 pro fast": 39,
    "ai mv 5.0": 40,
    "Seedance 2.0": 41,
    "Seedance 2.0 Fast": 42,
    "Kling V3": 43,
    "kling o3": 44,
    "wan 2.2-角色替换": 45,
    "kling 动作模仿": 46,
    "视频增强": 47,
    "ai mv 5.5": 50,
}

def get_model_id_by_name(model_name: str) -> int | None:
    """
    根据模型名称获取对应的模型 ID（忽略大小写比较）。
    
    Args:
        model_name: 模型名称
        
    Returns:
        模型 ID，如果未找到则返回 None
    """
    model_name_lower = model_name.lower()
    for name, model_id in MODEL_MAP.items():
        if name.lower() == model_name_lower:
            return model_id
    
    return None
def estimate_cost(model: str, resolution: int | None, duration: int,
                  sound_on: bool = False, count: int = 1) -> float | None:
    """Return estimated total cost in credits, or None if model/params unknown."""
    rates = _RATE.get(model)
    if not rates:
        return None
    res = resolution or 0
    for key in [(res, sound_on), (res, None), (0, sound_on), (0, None)]:
        if key in rates:
            return round(rates[key] * duration * count, 2)
    return None


def _parse_duration_spec(spec: str) -> str:
    """Convert duration spec to human-readable hint for error messages."""
    if not spec:
        return "N/A"
    if "," in spec:
        return f"one of [{spec}]s"
    if "-" in spec:
        lo, hi = spec.split("-")
        return f"{lo}–{hi}s"
    return f"{spec}s"


def validate_model_params(task_type: str, model: str, aspect_ratio: str | None,
                          resolution: int | None, duration: int | None,
                          quiet: bool) -> None:
    """Warn on stderr if parameters are incompatible with model constraints."""
    registry = MODEL_REGISTRY.get(task_type, {})
    if model not in registry:
        if not quiet:
            known = ", ".join(sorted(registry.keys()))
            print(
                f"Warning: unknown model '{model}' for {task_type}. "
                f"Known models: {known}",
                file=sys.stderr,
            )
        return

    spec = registry[model]

    if aspect_ratio and spec["aspectRatio"] is None:
        if not quiet:
            print(
                f"Warning: model '{model}' does not support aspectRatio "
                f"(got '{aspect_ratio}'). Parameter will be ignored by the API.",
                file=sys.stderr,
            )
    elif aspect_ratio and spec["aspectRatio"] and aspect_ratio not in spec["aspectRatio"]:
        if not quiet:
            print(
                f"Warning: model '{model}' supports aspectRatio "
                f"{spec['aspectRatio']}, got '{aspect_ratio}'.",
                file=sys.stderr,
            )

    if resolution and spec["resolution"] is None:
        if not quiet:
            print(
                f"Warning: model '{model}' does not support resolution "
                f"(got {resolution}). Parameter will be ignored by the API.",
                file=sys.stderr,
            )
    elif resolution and spec["resolution"] and resolution not in spec["resolution"]:
        if not quiet:
            print(
                f"Warning: model '{model}' supports resolution "
                f"{spec['resolution']}, got {resolution}.",
                file=sys.stderr,
            )

    if duration and spec["duration"]:
        dur_str = spec["duration"]
        valid = True
        if "," in dur_str:
            valid = duration in [int(x) for x in dur_str.split(",")]
        elif "-" in dur_str:
            lo, hi = [int(x) for x in dur_str.split("-")]
            valid = lo <= duration <= hi
        else:
            valid = duration == int(dur_str)
        if not valid and not quiet:
            print(
                f"Warning: model '{model}' supports duration "
                f"{_parse_duration_spec(dur_str)}, got {duration}s.",
                file=sys.stderr,
            )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def resolve_file(client: LitMediaClient, file_ref: str, quiet: bool) -> str:
    """If file_ref looks like a local path, upload it and return fileId."""
    return resolve_local_file(file_ref, quiet=quiet, client=client)

def get_video_duration(file_ref: str, quiet: bool) -> float:
    """If file_ref looks like a local path, upload it and return fileId."""
    local_file = file_ref
    is_url = file_ref.startswith(("http://", "https://"))
    if is_url:
        time_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        temp_dir = tempfile.gettempdir()
        out_path = os.path.join(temp_dir, f"video_{time_name}.mp4")
        download_video(file_ref, out_path, quiet)
        local_file = out_path

    return MediaUtils.get_duration(local_file)

def build_a2ls_body(args, client: LitMediaClient) -> dict:
    """Build request body for Audio-to-Lip-sync."""
    body: dict[str, Any] = {
        # "model": args.model,
        "prompt": "",
    }
    if args.prompt:
        body["prompt"] = args.prompt
    if args.model:
        body["video_model"] = 36
    if args.input_image:
        if os.path.isfile(args.input_image):
            body["img_url"] = resolve_file(client, args.input_image, args.quiet)
        else:
            body["img_url"] = args.input_image
    if args.input_sound:
        if os.path.isfile(args.input_sound):
            duration = int(get_video_duration(args.input_sound, args.quiet) / 1000)
            body["duration"] = duration
            body["sound_url"] = resolve_file(client, args.input_sound, args.quiet)
        else:
            body["sound_url"] = args.input_sound
            duration = int(get_video_duration(args.input_sound, args.quiet) / 1000)
            body["duration"] = duration
    
    # 默认语速1.0
    body["sound_speed"] = 1

    # 是否是数字人
    body["is_ai_avatar"] = 0

    return body

def build_anim_body(args, client: LitMediaClient) -> dict:
    """Build request body for Text-to-Video."""
    body = {
        # "model": args.model,
        "prompt": args.prompt,
    }
    if args.model:
        body["video_model"] = 1
    if args.input_image:
        if os.path.isfile(args.input_image):
            body["img_url"] = resolve_file(client, args.input_image, args.quiet)
        else:
            body["img_url"] = args.input_image
    if args.resolution:
        body["quality"] = str(args.resolution) + "p"
    if args.duration:
        body["duration"] = args.duration
    if args.style:
        body["style"] = args.style
    return body

def calculate_extend_quality_from_height(height: int) -> str:
    """Calculate video quality based on video height.
    
    Args:
        height: Video height in pixels
        
    Returns:
        Quality string: '1080p', '720p', '540p', or '360p'
    """
    if height >= 1080:
        return '1080p'
    elif height >= 720:
        return '720p'
    elif height >= 540:
        return '540p'
    else:
        return '360p'

def build_extend_body(args, client: LitMediaClient) -> dict:
    """Build request body for Text-to-Video."""
    body = {
        # "model": args.model,
        "prompt": args.prompt,
    }
    if args.model:
        body["video_model"] = 1
    if args.input_video:
        if os.path.isfile(args.input_video):
            resolution = MediaUtils.get_resolution(args.input_video)
            body["upload_video_url"] = resolve_file(client, args.input_video, args.quiet)
        else:
            resolution = MediaUtils.get_resolution_from_url(args.input_video)
            body["upload_video_url"] = args.input_video

    if resolution:
        body["quality"] = calculate_extend_quality_from_height(resolution)

    if args.duration:
        body["duration"] = args.duration
    # if args.sound:
    #     body["sound"] = args.sound
    # if args.count:
    #     body["video_num"] = args.count
    return body

def build_i2v_body(args, client: LitMediaClient) -> dict:
    """Build request body for Image-to-Video."""
    body = {}
    if args.model:
        body["video_model"] = get_model_id_by_name(args.model)
    if args.first_frame:
        body["img_url"] = resolve_file(client, args.first_frame, args.quiet)
    if args.end_frame:
        body["last_img_url"] = resolve_file(client, args.end_frame, args.quiet)
    if args.ref_images:
        body["img_url_list"] = [
            resolve_file(client, ref, args.quiet) for ref in args.ref_images
        ]
    if args.prompt:
        body["prompt"] = args.prompt

    registry = MODEL_REGISTRY.get(args.type, {})
    if args.model in registry:
        spec = registry[args.model]
        if args.resolution and spec["resolution"] is not None:
            body["quality"] = str(args.resolution) + "p"

        if args.aspect_ratio and spec["aspectRatio"] is not None:
            body["ratio"] = args.aspect_ratio

    if args.duration:
        body["duration"] = args.duration
    # if args.sound:
    #     body["sound"] = args.sound
    if args.count:
        body["video_num"] = args.count
    return body


def build_t2v_body(args) -> dict:
    """Build request body for Text-to-Video."""
    body = {
        # "model": args.model,
        "prompt": args.prompt,
    }

    if args.model:
        body["video_model"] = get_model_id_by_name(args.model)

    registry = MODEL_REGISTRY.get(args.type, {})
    if args.model in registry:
        spec = registry[args.model]
        if args.resolution and spec["resolution"] is not None:
            body["quality"] = str(args.resolution) + "p"

        if args.aspect_ratio and spec["aspectRatio"] is not None:
            body["ratio"] = args.aspect_ratio

    if args.duration:
        body["duration"] = args.duration
    # if args.sound:
    #     body["sound"] = args.sound
    if args.count:
        body["video_num"] = args.count
    return body

def build_body(args, client: LitMediaClient) -> dict:
    """Dispatch to the type-specific body builder, with model constraint checks."""
    if args.model:
        validate_model_params(
            args.type, args.model,
            getattr(args, "aspect_ratio", None),
            getattr(args, "resolution", None),
            getattr(args, "duration", None),
            args.quiet,
        )
    if args.type == "i2v":
        return build_i2v_body(args, client)
    elif args.type == "t2v":
        return build_t2v_body(args)
    elif args.type == "extend":
        return build_extend_body(args, client)
    elif args.type == "anim":
        return build_anim_body(args, client)
    elif args.type == "a2ls":
        return build_a2ls_body(args, client)
    raise ValueError(f"Unknown type: {args.type}")


def do_submit(client: LitMediaClient, task_type: str, body: dict, quiet: bool) -> str:
    """POST submit task, return taskId."""
    path = ENDPOINTS[task_type]["submit"]
    label = {"i2v": "image-to-video", "t2v": "text-to-video", "extend": "video-extension", "anim": "animation", "a2ls": "audio-to-lip-sync"}
    if not quiet:
        print(f"Submitting {label[task_type]} task...", file=sys.stderr)
    result = client.post(path, json=body)
    # print(f"client.post result: {result}")
    task_id = result["create_id"]
    if not quiet:
        print(f"Task submitted. taskId: {task_id}", file=sys.stderr)
    return task_id


def do_poll(client: LitMediaClient, task_type: str, task_id: str,
            timeout: float, interval: float, quiet: bool) -> dict:
    """Poll until status is terminal or timeout is exceeded."""
    path = ENDPOINTS[task_type]["query"]
    if not quiet:
        print(
            f"Polling task {task_id} (timeout={timeout}s, interval={interval}s)...",
            file=sys.stderr,
        )
    return client.poll_task(
        path,
        task_id,
        interval=interval,
        timeout=timeout,
        verbose=not quiet,
    )


def download_video(url: str, output: str, quiet: bool) -> None:
    """Download a video from URL to a local file."""
    import requests as req

    if not quiet:
        print(f"Downloading video to {output}...", file=sys.stderr)

    resp = req.get(url, stream=True)
    resp.raise_for_status()

    with open(output, "wb") as f:
        for chunk in resp.iter_content(chunk_size=8192):
            f.write(chunk)

    if not quiet:
        size_mb = os.path.getsize(output) / (1024 * 1024)
        print(f"Downloaded: {output} ({size_mb:.1f} MB)", file=sys.stderr)


def print_result(result: dict, args, client: LitMediaClient) -> None:
    """Print final result: video URLs by default, full JSON with --json."""
    video_url = result.get("video_url", "")
    video_num = result.get("video_num", 0)

    if args.output_dir and video_url:
        os.makedirs(args.output_dir, exist_ok=True)
        ext = "mp4"
        if video_num > 1:
            # For multiple videos, we assume the API returns a list of URLs in "video_url"
            urls = result.get("child_data", [])
            for idx, item in enumerate(urls):
                # Extract video_url from the object (prefer down_video_url if available)
                url = item.get("down_video_url") or item.get("video_url", "")
                if not url:
                    continue
                time_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
                out_path = os.path.join(args.output_dir, f"video_{time_name}_{idx+1}.{ext}")
                download_video(url, out_path, args.quiet)
        else:
            # 获取当前时间: 2023050911
            time_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            out_path = os.path.join(args.output_dir, f"video_{time_name}.{ext}")
            download_video(video_url, out_path, args.quiet)

    if args.json:
        print(json_mod.dumps(result, indent=2, ensure_ascii=False))
    else:
        cost = result.get("cost_credit", "N/A")
        print(f"status: {result.get('status')}  cost: {cost} credits")
        
        video_url = result.get("video_url", "")
        error_msg = result.get("error", "") or result.get("real_error", "")
        video_num = result.get("video_num", 0)
        
        if video_num > 1:
            # Print all video URLs from child_data
            urls = result.get("child_data", [])
            for idx, item in enumerate(urls):
                url = item.get("down_video_url") or item.get("video_url", "")
                status = item.get("status", 0)
                if url and status == 1:
                    print(f" [{idx+1}] video_url:{url}")
                else:
                    error = item.get("error", "") or item.get("real_error", "Unknown error")
                    print(f" [{idx+1}] failed: {error}")
        elif video_url and result.get("status") == 1:
            print(f" [1] video_url:{video_url}")
        else:
            print(f"  [1] failed: {error_msg or 'Unknown error'}")

# ---------------------------------------------------------------------------
# Argument definitions
# ---------------------------------------------------------------------------

def add_common_args(p):
    """Add arguments shared by all task types."""
    p.add_argument("--type", required=True, choices=TASK_TYPES,
                   help="Task type: i2v (image-to-video), t2v (text-to-video), extend (video extension), anim (animation), or a2ls (audio-to-lip-sync)")
    p.add_argument("--model", default="LitAI 5",
                   help="Model name/ID (required for t2v and i2v; optional for others). See 'list-models' command for supported models. default value: 'LitAI 5' ")
    p.add_argument("--prompt", default=None,
                   help="Text prompt (required for t2v and omni)")
    p.add_argument("--aspect-ratio", default=None,
                   help='Aspect ratio, e.g. "16:9", "9:16", "1:1", "4:3", "3:4" ')
    p.add_argument("--resolution", type=int, default=720, choices=[360, 480, 540, 720, 1080],
                   help="Resolution (model-dependent): 360, 480, 540, 720, 1080")
    p.add_argument("--duration", type=int, default=None,
                   help="Video duration in seconds")
    p.add_argument("--count", type=int, default=1,
                   help="Number of videos to generate (1-4) default: 1")
    p.add_argument("--sound", default=None, choices=["on", "off"],
                   help='Native audio: "on"/"off". Only models with nativeAudio=True support this; may affect cost')
    p.add_argument("--input_image", default=None,
                   help="Input image for animation/a2ls (fileId or local path)")

def add_extend_args(p):
    """Add video-extension specific arguments."""
    p.add_argument("--input_video", default=None,
                   help="Need to extend the video")

def add_anim_args(p):
    """Add animation specific arguments."""
    p.add_argument("--style", default=None,
                   help="Animation style, e.g. '', 'comic', 'anime', '3d_animation', 'clay', 'cyberpunk'")
    
def add_a2ls_args(p):
    """Add audio-to-Lip-sync specific arguments."""
    p.add_argument("--input_sound", default=None,
                   help="Input sound for audio-to-lip-sync (fileId or local path)")

def add_i2v_args(p):
    """Add image-to-video specific arguments."""
    p.add_argument("--first-frame", default=None,
                   help="First frame image fileId or local path")
    p.add_argument("--end-frame", default=None,
                   help="End frame image fileId or local path")
    p.add_argument("--ref-images", nargs="+", default=None,
                   help="Reference image fileIds or local paths (multi-image mode, >=2)")


def add_omni_args(p):
    """Add omni-reference specific arguments."""
    p.add_argument("--input-images", default=None,
                   help='JSON array of input images, e.g. \'[{"fileId":"xxx","name":"Image1"}]\'')
    p.add_argument("--input-videos", default=None,
                   help='JSON array of input videos, e.g. \'[{"fileId":"xxx","name":"Video1"}]\'')
    p.add_argument("--internet-search", action="store_true",
                   help="Enable internet search for omni reference")


def add_poll_args(p):
    """Add polling control arguments."""
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                   help=f"Max polling time in seconds (default: {DEFAULT_TIMEOUT})")
    p.add_argument("--interval", type=float, default=DEFAULT_INTERVAL,
                   help=f"Polling interval in seconds (default: {DEFAULT_INTERVAL})")


def add_output_args(p):
    """Add output/download arguments."""
    p.add_argument("--output-dir", default=None,
                   help="Download result videos to this directory")
    p.add_argument("--json", action="store_true",
                   help="Output full JSON response")
    p.add_argument("-q", "--quiet", action="store_true",
                   help="Suppress status messages on stderr")


def validate_args(args, parser):
    """Validate type-specific required arguments."""
    if args.type == "t2v":
        if not args.model:
            parser.error("--model is required for text-to-video (t2v)")
        if not args.prompt:
            parser.error("--prompt is required for text-to-video (t2v)")
    # elif args.type == "omni":
    #     if not args.model:
    #         parser.error("--model is required for omni reference")
    #     if not args.prompt:
    #         parser.error("--prompt is required for omni reference")
    elif args.type == "i2v":
        if not args.first_frame and not args.ref_images:
            parser.error("--first-frame or --ref-images is required for image-to-video (i2v)")
    elif args.type == "extend":
        if not args.input_video:
            parser.error("--input_video is required for video extension")
    elif args.type == "anim":
        if not args.input_image:
            parser.error("--input_image is required for animation")
    elif args.type == "a2ls":
        if not args.input_image:
            parser.error("--input_image is required for audio-to-lip-sync")
        if not args.input_sound:
            parser.error("--input_sound is required for audio-to-lip-sync")

    
# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------

def cmd_list_models(args, parser):
    """Print supported models and their parameter constraints."""
    task_type = args.type
    registry = MODEL_REGISTRY.get(task_type, {})
    if not registry:
        print(f"No models registered for type '{task_type}'.")
        return

    if args.json:
        print(json_mod.dumps(registry, indent=2, ensure_ascii=False))
        return

    type_label = {"i2v": "Image-to-Video", "t2v": "Text-to-Video", "extend": "Video Extension",
                  "anim": "Animation", "a2ls": "Audio-to-Lip-sync"}
    print(f"\n{type_label.get(task_type, task_type)} — Supported Models\n")
    print(f"{'Model':<25} {'Aspect Ratio':<35} {'Resolution':<22} {'Duration':<32} {'Audio'}")
    print("-" * 120)
    for name, spec in registry.items():
        ar = ", ".join(spec["aspectRatio"]) if spec["aspectRatio"] else "by image" if task_type == "i2v" else "N/A"
        res = ", ".join(str(r) for r in spec["resolution"]) if spec["resolution"] else "N/A"
        dur = _parse_duration_spec(spec["duration"])
        audio = "Yes" if spec.get("nativeAudio") else "No"
        print(f"{name:<25} {ar:<35} {res:<22} {dur:<32} {audio}")
    print()


def cmd_estimate_cost(args, parser):
    """Print estimated cost for a given model + parameters."""
    sound_on = args.sound == "on" if args.sound else False
    cost = estimate_cost(args.model, args.resolution, args.duration, sound_on, args.count or 1)
    if cost is None:
        print(f"Cannot estimate cost for model '{args.model}' with given parameters.", file=sys.stderr)
        print("Use list-models to see available models, or check references/api-docs.md.", file=sys.stderr)
        sys.exit(1)
    count = args.count or 1
    unit = round(cost / count, 2)
    if args.json:
        print(json_mod.dumps({"model": args.model, "resolution": args.resolution,
                               "duration": args.duration, "sound": args.sound or "off",
                               "count": count, "unitCost": unit, "totalCost": cost}))
    else:
        print(f"model: {args.model}  resolution: {args.resolution or 'default'}  "
              f"duration: {args.duration}s  sound: {args.sound or 'off'}  count: {count}")
        print(f"estimated unit cost: {unit} credits")
        print(f"estimated total cost: {cost} credits")


def cmd_run(args, parser):
    """Submit task then poll until done — full flow (default)."""
    validate_args(args, parser)
    client = LitMediaClient()
    body = build_body(args, client)
    print(f"Request body: {json_mod.dumps(body, ensure_ascii=False)}", file=sys.stderr)
    # Debug: print the request body to stderr
    if not args.quiet:
        print(f"Request body: {json_mod.dumps(body, ensure_ascii=False)}", file=sys.stderr)
    task_id = do_submit(client, args.type, body, args.quiet)
    result = do_poll(client, args.type, task_id, args.timeout, args.interval, args.quiet)
    # print(f"result: {result}")
    # 打印args类型和值
    # print(f"args类型：{type(args)}")
    print_result(result, args, client)


def cmd_submit(args, parser):
    """Submit task only — print taskId and exit immediately."""
    validate_args(args, parser)
    client = LitMediaClient()
    body = build_body(args, client)
    task_id = do_submit(client, args.type, body, args.quiet)
    print(task_id)


def cmd_query(args, parser):
    """Poll an existing task by taskId until done or timeout."""
    client = LitMediaClient()
    try:
        result = do_poll(
            client, args.type, args.task_id,
            args.timeout, args.interval, args.quiet,
        )
        print_result(result, args, client)
    except TimeoutError as e:
        if not args.quiet:
            print(f"Timeout reached: {e}", file=sys.stderr)
            print("Fetching last known status...", file=sys.stderr)
        path = ENDPOINTS[args.type]["query"]
        last = client.get(path, params={"taskId": args.task_id})
        status = last.get("status", "unknown")
        task_id = last.get("taskId", args.task_id)
        if args.json:
            print(json_mod.dumps(last, indent=2, ensure_ascii=False))
        else:
            print(f"status: {status}  taskId: {task_id}", file=sys.stderr)
        sys.exit(2)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="LitMedia Video Generation — i2v / t2v / extend / anim / a2ls.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
AGENT WORKFLOW RULES:
  1. ALWAYS start with `run` — it submits and polls automatically.
  2. Only use `query` if `run` timed out and you have a taskId to resume.
  3. `query` polls continuously (not once) until done or --timeout.
  4. NEVER hand a pending taskId back to the user — always poll to completion.

Task types:
  i2v   Image-to-Video      (first/end frame + prompt)
  t2v   Text-to-Video       (model + prompt, no image needed)
  extend Video Extension    (input video + prompt)
  anim   Animation           (input image + style + prompt)
  a2ls   Audio-to-Lip-sync   (input image + input sound + prompt)

Examples:
  # List available models for a task type
  python video_gen.py list-models --type t2v

  # Image-to-video with first frame
  python video_gen.py run --type i2v --model "LitAI 5" \\
      --first-frame photo.png --prompt "A rotating product" --resolution 1080

  # Text-to-video
  python video_gen.py run --type t2v --model "LitAI 5" \\
      --prompt "A futuristic city" --aspect-ratio "16:9" --duration 5

  # Video extension
  python video_gen.py run --type extend --model "LitAI 5" \\
      --input_video "input.mp4" --prompt "video description" --duration 5 

  # Animation with style
  python video_gen.py run --type anim --model "LitAI 5" \\
      --input_image "input.png" --prompt "video description" --duration 5 --style "cyberpunk" --resolution 720 

  # Audio-to-lip-sync
  python video_gen.py run --type a2ls --model "LitAI 5" \\
      --input_image "input.png" --input_sound "audio.mp3" 

  # Estimate cost before running
  python video_gen.py estimate-cost --model "LitAI 5" \\
      --resolution 1080 --duration 5 --sound on --count 2

  # Query a timed-out task
  python video_gen.py query --type i2v --task-id <taskId>
""",
    )

    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    # -- run (default full flow) --
    p_run = sub.add_parser("run", help="[DEFAULT] Submit task and poll until done")
    add_common_args(p_run)
    add_i2v_args(p_run)
    # add_omni_args(p_run)
    add_extend_args(p_run)
    add_anim_args(p_run)
    add_a2ls_args(p_run)
    add_poll_args(p_run)
    add_output_args(p_run)

    # -- submit only --
    p_submit = sub.add_parser("submit", help="Submit task only, print taskId and exit")
    add_common_args(p_submit)
    add_i2v_args(p_submit)
    add_extend_args(p_submit)
    add_anim_args(p_submit)
    add_a2ls_args(p_submit)
    # add_omni_args(p_submit)
    add_output_args(p_submit)

    # -- query / poll existing task --
    p_query = sub.add_parser("query", help="Poll existing taskId until done or timeout")
    p_query.add_argument("--type", required=True, choices=TASK_TYPES,
                         help="Task type (needed to select correct query endpoint)")
    p_query.add_argument("--task-id", required=True,
                         help="taskId returned by 'submit' or a previous 'run'")
    add_poll_args(p_query)
    add_output_args(p_query)

    # -- list-models --
    p_list = sub.add_parser("list-models", help="Show supported models and parameter constraints")
    p_list.add_argument("--type", required=True, choices=TASK_TYPES,
                        help="Task type to list models for")
    p_list.add_argument("--json", action="store_true",
                        help="Output as JSON")

    # -- estimate-cost --
    p_cost = sub.add_parser("estimate-cost", help="Estimate credit cost before running a task")
    p_cost.add_argument("--model", required=True, help="Model display name")
    p_cost.add_argument("--resolution", type=int, required=True, default="720", help="Resolution")
    p_cost.add_argument("--duration", type=int, required=True, help="Duration in seconds")
    p_cost.add_argument("--sound", default=None, choices=["on", "off"], help="Sound on/off")
    p_cost.add_argument("--count", type=int, required=True, default=1, help="generatingCount (1-4)")
    p_cost.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    if args.subcommand == "run":
        cmd_run(args, p_run)
    elif args.subcommand == "submit":
        cmd_submit(args, p_submit)
    elif args.subcommand == "query":
        cmd_query(args, p_query)
    elif args.subcommand == "list-models":
        cmd_list_models(args, p_list)
    elif args.subcommand == "estimate-cost":
        cmd_estimate_cost(args, p_cost)


if __name__ == "__main__":
    main()