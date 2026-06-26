#!/usr/bin/env python3
"""Character Replace in Videos with Scene Consistency using LitMedia Common Task APIs.

## AGENT INSTRUCTIONS — READ FIRST
- Default workflow: ALWAYS use `run` (submit + auto-poll).
  Do NOT ask the user to run query manually.
- Only use `query` when `run` has already timed out and a taskId exists,
  or when the user explicitly provides a taskId to resume.
- When using `query`, keep polling (default timeout=600s) until
  status is 'success' or 'fail'. Do NOT stop after a single check.
- Never hand a pending taskId back to the user and say "check it later".
  Always poll to completion within the timeout window.

Supported task types:
    Full_Scene   — Use the whole image's person and  background in the video.
    Body_Only    — Use the image's person in the video, keep the video's background.

Subcommands:
    run     Submit task AND poll until done — DEFAULT, use this first
    submit  Submit only, print taskId, exit — use for parallel batch jobs
    query   Poll an existing taskId until done (or timeout) — use for recovery

Usage:
    python video_mimic.py run  --type Full_Scene  --first-frame <fileId|path> [options]
    python video_mimic.py run  --type Body_Only  --model "Seedance 1.5 Pro" [options]
    python video_mimic.py submit --type <Full_Scene|Body_Only> [task-specific options]
    python video_mimic.py query --task-id <taskId> [options]
"""

import argparse
import json as json_mod
import os
import sys
import time
import uuid
import tempfile
import datetime

sys.path.insert(0, os.path.dirname(__file__))

from typing import Any
from shared.client import LitMediaClient, LitMediaError, TaskStatus
from shared.upload import resolve_local_file
from shared.media_util import MediaUtils

TASK_TYPES = ("Full_Scene", "Body_Only")

ENDPOINTS = {
    "submit": "/lit-video/video-replace-character",
    "query": "/lit-video/do-process",
}

DEFAULT_TIMEOUT = 600
DEFAULT_INTERVAL = 60

# ---------------------------------------------------------------------------
# Model constraints — `model` must use display names, NOT code names.
# Each entry: { "aspectRatio": list|None, "resolution": list|None, "duration": str }
#   None = not supported / do not send
# ---------------------------------------------------------------------------

FULL_SCENE_MODELS = {
    "Kling V3.0":       {"resolution": [480, 720]},
    "Seedance 2.0":     {"resolution": [480]},
    "Wan 2.2":          {"resolution": [480, 720]},
}

BODY_ONLY_MODELS = {
    "Wan 2.2":          {"resolution": [480, 720]},
}

MODEL_REGISTRY = {"Full_Scene": FULL_SCENE_MODELS, "Body_Only": BODY_ONLY_MODELS}

# ---------------------------------------------------------------------------
# Pricing — credits per video (generateCount=1).
# Key: resolution string for models without resolution.
# totalCost = unitCost × generateCount
# See references/api-docs.md for full pricing tables.
# ---------------------------------------------------------------------------

_RATE = {
    "Kling V3.0":           {"unitCost" :12, "resolution" : {480: 1, 720: 1.5}},
    "Seedance 2.0":         {"unitCost" :1, "resolution" : {480: 3}},
    "Wan 2.2":              {"unitCost" :6, "resolution" : {480: 1, 720: 2}},
}

MODEL_MAP = {
    "Wan 2.2": 45,
    "Kling V3.0": 46,
    "Seedance 2.0": 51,
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


def estimate_cost(model: str, resolution: int | None, duration: int) -> float | None:
    """Return estimated total cost in credits, or None if model/params unknown."""

    config = _RATE.get(model)
    if not config or resolution is None:
        return None

    unit_cost = config.get("unitCost")
    resolution_map = config.get("resolution", {})

    if resolution not in resolution_map:
        return None

    multiplier = resolution_map[resolution]
    total_cost = unit_cost * multiplier * duration

    return round(total_cost, 2)

def validate_model_params(task_type: str, model: str,
                          resolution: int | None,
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


def build_full_scene_body(args, client: LitMediaClient) -> dict:
    """Build request body for Character Replace(full scene replace)."""
    body = {}
    if args.model:
        body["video_model"] = get_model_id_by_name(args.model)
    if args.input_image:
        body["img_url"] = resolve_file(client, args.input_image, args.quiet)
    if args.input_video:
        body["video_url"] = resolve_file(client, args.input_video, args.quiet)
        body["duration"] = int(get_video_duration(args.input_video, args.quiet) / 1000)
    if args.resolution:
        body["quality"] = str(args.resolution) + "p"
    return body


def build_body_only_body(args, client: LitMediaClient) -> dict:
    """Build request body for Character Replace(only replacing the body)."""
    body: dict[str, Any] = {
        "mode": "replace",
    }
    if args.model:
        body["video_model"] = get_model_id_by_name(args.model)
    if args.input_image:
        body["img_url"] = resolve_file(client, args.input_image, args.quiet)
    if args.input_video:
        body["video_url"] = resolve_file(client, args.input_video, args.quiet)
        body["duration"] = int(get_video_duration(args.input_video, args.quiet) / 1000)
    if args.resolution:
        body["quality"] = str(args.resolution) + "p"
    return body

def build_body(args, client: LitMediaClient) -> dict:
    """Dispatch to the type-specific body builder, with model constraint checks."""
    if args.model:
        validate_model_params(
            args.type, args.model,
            getattr(args, "resolution", None),
            args.quiet,
        )
    if args.type == "Full_Scene":
        return build_full_scene_body(args, client)
    elif args.type == "Body_Only":
        return build_body_only_body(args, client)
    raise ValueError(f"Unknown type: {args.type}")

def do_submit(client: LitMediaClient, task_type: str, body: dict, quiet: bool) -> str:
    """POST submit task, return taskId."""
    path = ENDPOINTS["submit"]
    if not quiet:
        print(f"Submitting {task_type} task...", file=sys.stderr)
    result = client.post(path, json=body)
    task_id = result["create_id"]
    if not quiet:
        print(f"Task submitted. taskId: {task_id}", file=sys.stderr)
    return task_id


def do_poll(client: LitMediaClient, task_id: str,
            timeout: float, interval: float, quiet: bool) -> dict:
    """Poll until status is terminal or timeout is exceeded."""
    path = ENDPOINTS["query"]
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
    status = TaskStatus(result.get("status"))


    video_url = result.get("video_url", "")
    if status == TaskStatus.COMPLETED:
        if args.output_dir and video_url:
            os.makedirs(args.output_dir, exist_ok=True)
            ext = "mp4"
            # 获取当前时间: 2023050911
            time_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            out_path = os.path.join(args.output_dir, f"video_{time_name}.{ext}")
            download_video(video_url, out_path, args.quiet)

    if args.json:
        print(json_mod.dumps(result, indent=2, ensure_ascii=False))
    else:
        cost = result.get("cost_credit", "N/A")
        print(f"status: {status.label}  cost: {cost} credits")
        
        video_url = result.get("video_url", "")
        error_msg = result.get("error", "") or result.get("real_error", "")
        
        if video_url and status == TaskStatus.COMPLETED:
            print(f"Character Replace completed, video_url:{video_url}")
        else:
            print(f"  [1] failed: {error_msg or 'Unknown error'}")

# ---------------------------------------------------------------------------
# Argument definitions
# ---------------------------------------------------------------------------

def add_common_args(p):
    """Add arguments shared by all task types."""
    p.add_argument("--type", required=True, choices=TASK_TYPES,
                   help="Task type: Full_Scene, Body_Only")
    p.add_argument("--model", default=None,
                   help="Model name/ID (required for Full_Scene and Body_Only)")
    p.add_argument("--resolution", type=int, default=720, choices=[480, 720],
                   help="Resolution (model-dependent): 480, 720")
    p.add_argument("--input-image", default=None,
                   help="Reference image fileUrl or local paths")
    p.add_argument("--input-video", default=None,
                   help="Reference video fileUrl or local paths")

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
    if args.type == "Full_Scene":
        if not args.model:
            parser.error("--model is required for Character Replace (Full Scene Replace)")
        if not args.input_image:
            parser.error("--input-image is required for Character Replace (Full Scene Replace)")
        if not args.input_video:
            parser.error("--input-video is required for Character Replace (Full Scene Replace)")
    elif args.type == "Body_Only":
        if not args.model:
            parser.error("--model is required for Character Replace (Only Body Replace)")
        if not args.input_image:
            parser.error("--input-image is required for Character Replace (Only Body Replace)")
        if not args.input_video:
            parser.error("--input-video is required for Character Replace (Only Body Replace)")


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

    print(f"\n{task_type} — Supported Models\n")
    print(f"{'Model':<25}  {'Resolution':<18}")
    print("-" * 50)
    for name, spec in registry.items():
        res = ", ".join(str(r) for r in spec["resolution"]) if spec["resolution"] else "N/A"
        print(f"{name:<25} {res:<18}")
    print()

def cmd_estimate_cost(args, parser):
    """Print estimated cost for a given model + parameters."""
    duration = int(get_video_duration(args.input_video, False) / 1000)
    cost = estimate_cost(args.model, args.resolution, duration)
    if cost is None:
        print(f"Cannot estimate cost for model '{args.model}' with given parameters.", file=sys.stderr)
        print("Use list-models to see available models, or check references/api-docs.md.", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json_mod.dumps({"model": args.model, "resolution": args.resolution,
                              "duration": duration, "totalCost": cost}))
    else:
        print(f"model: {args.model} duration: {duration}s  resolution: {args.resolution or 'default'}")
        print(f"estimated total cost: {cost} credits")


def cmd_run(args, parser):
    """Submit task then poll until done — full flow (default)."""
    validate_args(args, parser)
    client = LitMediaClient()
    body = build_body(args, client)
    task_id = do_submit(client, args.type, body, args.quiet)
    result = do_poll(client, task_id, args.timeout, args.interval, args.quiet)
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
            client, args.task_id,
            args.timeout, args.interval, args.quiet,
        )
        print_result(result, args, client)
    except TimeoutError as e:
        if not args.quiet:
            print(f"Timeout reached: {e}", file=sys.stderr)
            print("Fetching last known status...", file=sys.stderr)
        path = ENDPOINTS["query"]
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
        description="Character Replace in Videos with Scene Consistency using LitMedia Common Task APIs.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
AGENT WORKFLOW RULES:
  1. ALWAYS start with `run` — it submits and polls automatically.
  2. Only use `query` if `run` timed out and you have a taskId to resume.
  3. `query` polls continuously (not once) until done or --timeout.
  4. NEVER hand a pending taskId back to the user — always poll to completion.

Task types:
  Full_Scene   — Use the whole image's person and  background in the video.
  Body_Only    — Use the image's person in the video, keep the video's background.

Examples:
  # List available models for a task type
  python video_mimic.py list-models --type Full_Scene

  # Full Scene Replace (Full_Scene)
  python video_mimic.py run --type Full_Scene --model "Kling V3.0" --resolution 720 \\
      --input-image character.jpg --input-video video.mp4

  # Only Body Replace (Body_Only)
  python video_mimic.py run --type Body_Only --model "Wan 2.2" --resolution 480 \\
      --input-image character.jpg --input-video video.mp4

  # Estimate cost before running
  python video_mimic.py estimate-cost --model "Kling V3.0" --resolution 720 --input-video video.mp4

  # Query a timed-out task
  python video_mimic.py query --task-id <taskId>
""",
    )

    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    # -- run (default full flow) --
    p_run = sub.add_parser("run", help="[DEFAULT] Submit task and poll until done")
    add_common_args(p_run)
    add_poll_args(p_run)
    add_output_args(p_run)

    # -- submit only --
    p_submit = sub.add_parser("submit", help="Submit task only, print taskId and exit")
    add_common_args(p_submit)
    add_output_args(p_submit)

    # -- query / poll existing task --
    p_query = sub.add_parser("query", help="Poll existing taskId until done or timeout")
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
    p_cost.add_argument("--input-video", required=True, help="Reference video fileUrl or local paths")
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