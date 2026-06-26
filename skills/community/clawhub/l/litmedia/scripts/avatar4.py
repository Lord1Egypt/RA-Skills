#!/usr/bin/env python3
"""Generate a talking avatar video from a photo using LitMedia Avatar4.

## AGENT INSTRUCTIONS — READ FIRST
- Default workflow: ALWAYS use `run` (submit + auto-poll).
  Do NOT ask the user to run query manually.
- Only use `query` when `run` has already timed out and a taskId exists,
  or when the user explicitly provides a taskId to resume.
- When using `query`, keep polling (default timeout=600s) until
  status is 'success' or 'failed'. Do NOT stop after a single check.
- Never hand a pending taskId back to the user and say "check it later".
  Always poll to completion within the timeout window.

Subcommands:
    run            Submit task AND poll until done — DEFAULT, use this first
    submit         Submit only, print taskId, exit — use for parallel batch jobs
    query          Poll an existing taskId until done (or timeout) — use for recovery
    list-captions  List available caption styles (captionId + thumbnail)

Usage:
    python avatar4.py run    --image <fileId|path> --text "..." --voice <id> [options]
    python avatar4.py submit --image <fileId|path> --text "..." --voice <id> [options]
    python avatar4.py query  --task-id <taskId> [--timeout 600] [--interval 5] [options]
    python avatar4.py list-captions [--json]
"""

import argparse
import json as json_mod
import os
import sys
import datetime

sys.path.insert(0, os.path.dirname(__file__))

from typing import Any
from shared.client import LitMediaClient, LitMediaError
from shared.upload import resolve_local_file
from shared.media_util import MediaUtils

SUBMIT_PATH = "/lit-video/image-lip-sync"
QUERY_PATH = "/lit-video/do-process"
CAPTION_LIST_PATH = "/v1/caption/list"
VALID_MODES = ("LitAI 5")

DEFAULT_TIMEOUT = 900
DEFAULT_INTERVAL = 10


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def build_body(args, file_id: str, audio_id: str | None) -> dict:
    """Build the submit-task request body from parsed args."""
    body: dict[str, Any] = { "prompt": "" }
    body["video_model"] = 36
    body["img_url"] = file_id
    body["sound_url"] = audio_id
    duration = round(MediaUtils.get_duration_from_url(audio_id) / 1000)
    body["duration"] = duration

    if args.motion:
        body["prompt"] = args.motion
    
    # 默认语速1.0
    body["sound_speed"] = 1

    # 是否是数字人
    body["is_ai_avatar"] = 1

    return body


def do_submit(client: LitMediaClient, body: dict, quiet: bool) -> str:
    """POST submit task, return taskId."""
    if not quiet:
        print("Submitting avatar4 task...", file=sys.stderr)
    result = client.post(SUBMIT_PATH, json=body)
    task_id = result["create_id"]
    if not quiet:
        print(f"Task submitted. taskId: {task_id}", file=sys.stderr)
    return task_id


def do_poll(client: LitMediaClient, task_id: str, timeout: float, interval: float,
            quiet: bool) -> dict:
    """Poll until status is 'success' or 'failed', or timeout is exceeded."""
    if not quiet:
        print(
            f"Polling task {task_id} (timeout={timeout}s, interval={interval}s)...",
            file=sys.stderr,
        )
    return client.poll_task(
        QUERY_PATH,
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

    if args.output and video_url:
        os.makedirs(args.output, exist_ok=True)
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
                out_path = os.path.join(args.output, f"video_{time_name}_{idx+1}.{ext}")
                download_video(url, out_path, args.quiet)
        else:
            # 获取当前时间: 2023050911
            time_name = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            out_path = os.path.join(args.output, f"video_{time_name}.{ext}")
            download_video(video_url, out_path, args.quiet)

    if args.json:
        print(json_mod.dumps(result, indent=2, ensure_ascii=False))
    else:
        cost = result.get("cost_credit", "N/A")
        board_id = result.get("boardId", "") or getattr(args, "board_id", "") or ""
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
        
        btid = result.get("image_task_id", "")
        if btid and board_id:
            print(f"       edit: https://www.litmedia.ai/board/{board_id}?boardResultId={btid}")


# ---------------------------------------------------------------------------
# Shared argument definitions
# ---------------------------------------------------------------------------

def add_submit_args(p):
    """Add arguments used by 'submit' and 'run' subcommands."""
    p.add_argument("--image", required=True,
                   help="Image fileId or local file path")
    # p.add_argument("--text", default=None,
    #                help="TTS text for the avatar to speak (use with --voice)")
    # p.add_argument("--voice", default=None,
    #                help="Voice ID (required when using --text)")
    p.add_argument("--audio", default=None,
                   help="Audio fileId for audio-driven mode")
    p.add_argument("--mode", default="LitAI 5", choices=VALID_MODES,
                   help="Generation mode (default: avatar4)")
    p.add_argument("--motion", default=None,
                   help="Custom action description or video description (max 600 chars)")


def add_poll_args(p):
    """Add polling control arguments."""
    p.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT,
                   help=f"Max polling time in seconds (default: {DEFAULT_TIMEOUT})")
    p.add_argument("--interval", type=float, default=DEFAULT_INTERVAL,
                   help=f"Polling interval in seconds (default: {DEFAULT_INTERVAL})")


def add_output_args(p):
    """Add output/download arguments."""
    p.add_argument("--output", default=None,
                   help="Download result video to this local path")
    p.add_argument("--json", action="store_true",
                   help="Output full JSON response")
    p.add_argument("-q", "--quiet", action="store_true",
                   help="Suppress status messages on stderr")


def validate_submit_args(args, parser):
    if not args.image and not args.audio:
        parser.error("Either --image or --audio is required")
    # if args.text and not args.voice:
    #     parser.error("--voice is required when using --text")


# ---------------------------------------------------------------------------
# Subcommand handlers
# ---------------------------------------------------------------------------

def _resolve_inputs(args) -> tuple[str, str | None]:
    """Upload local image/audio paths and return (image_fileId, audio_fileId_or_None)."""
    client = LitMediaClient()
    file_id = resolve_local_file(args.image, quiet=args.quiet, client=client)
    audio_id = None
    if args.audio:
        audio_id = resolve_local_file(args.audio, quiet=args.quiet, client=client)
    return file_id, audio_id


def cmd_run(args, parser):
    """Submit task then poll until done — full flow (default)."""
    validate_submit_args(args, parser)
    file_id, audio_id = _resolve_inputs(args)
    client = LitMediaClient()
    body = build_body(args, file_id, audio_id)
    task_id = do_submit(client, body, args.quiet)
    result = do_poll(client, task_id, args.timeout, args.interval, args.quiet)
    print_result(result, args, client)


def cmd_submit(args, parser):
    """Submit task only — print taskId and exit immediately."""
    validate_submit_args(args, parser)
    file_id, audio_id = _resolve_inputs(args)
    client = LitMediaClient()
    body = build_body(args, file_id, audio_id)
    task_id = do_submit(client, body, args.quiet)
    print(task_id)


def cmd_query(args, parser):
    """Poll an existing task by taskId until done or timeout.

    Keeps retrying until status == 'success' or 'failed', or --timeout expires.
    Does NOT stop after a single check — always polls to completion.
    """
    client = LitMediaClient()
    try:
        result = do_poll(
            client, args.task_id, args.timeout, args.interval, args.quiet
        )
        print_result(result, args, client)
    except TimeoutError as e:
        if not args.quiet:
            print(f"Timeout reached: {e}", file=sys.stderr)
            print("Fetching last known status...", file=sys.stderr)
        last = client.get(QUERY_PATH, params={"taskId": args.task_id})
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
        description="LitMedia Avatar4 — generate a talking avatar video from a photo.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
AGENT WORKFLOW RULES:
  1. ALWAYS start with `run` — it submits and polls automatically.
  2. Only use `query` if `run` timed out and you have a taskId to resume.
  3. `query` polls continuously (not once) until done or --timeout.
  4. NEVER hand a pending taskId back to the user — always poll to completion.

Subcommands:
  run            Submit + poll until done (DEFAULT — use this)
  submit         Submit only, print taskId, exit (for parallel batch)
  query          Poll existing taskId until done (for recovery after timeout)

Examples:
  # Standard usage — submit and wait (agent default)
  python avatar4.py run --image photo.png --audio audio.mp3

  # Batch: submit multiple tasks without waiting
  python avatar4.py submit --image photo.png --audio audio.mp3
  python avatar4.py submit --image photo2.png --audio audio2.mp3

  # Recovery: resume polling a taskId from a previous timed-out run
  python avatar4.py query --task-id <taskId>

  # Recovery with longer timeout
  python avatar4.py query --task-id <taskId> --timeout 1200
""",
    )

    sub = parser.add_subparsers(dest="subcommand")
    sub.required = True

    # -- run (default full flow) --
    p_run = sub.add_parser(
        "run",
        help="[DEFAULT] Submit task and poll until done",
    )
    add_submit_args(p_run)
    add_poll_args(p_run)
    add_output_args(p_run)

    # -- submit only --
    p_submit = sub.add_parser(
        "submit",
        help="Submit task only, print taskId and exit immediately",
    )
    add_submit_args(p_submit)
    add_output_args(p_submit)

    # -- query / poll existing task --
    p_query = sub.add_parser(
        "query",
        help="Poll existing taskId until done or timeout (for recovery)",
    )
    p_query.add_argument("--task-id", required=True,
                         help="taskId returned by 'submit' or a previous 'run'")
    add_poll_args(p_query)
    add_output_args(p_query)

    # -- list-captions --
    # p_captions = sub.add_parser(
    #     "list-captions",
    #     help="List available caption styles (captionId + thumbnail)",
    # )
    # p_captions.add_argument("--json", action="store_true",
    #                         help="Output full JSON response")
    # p_captions.add_argument("-q", "--quiet", action="store_true",
    #                         help="Suppress status messages on stderr")

    args = parser.parse_args()

    handlers = {
        "run": (cmd_run, p_run),
        "submit": (cmd_submit, p_submit),
        "query": (cmd_query, p_query),
    }

    fn, p = handlers[args.subcommand]
    fn(args, p)


if __name__ == "__main__":
    main()
