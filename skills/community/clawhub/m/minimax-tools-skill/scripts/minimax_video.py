#!/usr/bin/env python3
import argparse
import base64
import mimetypes
import time
from pathlib import Path

from common import (
    MiniMaxError,
    OUTPUT_DIR,
    print_json,
    request_json,
    request_stream_download,
    timestamp_slug,
)


def file_to_data_url(path: str) -> str:
    p = Path(path).expanduser().resolve()
    mime, _ = mimetypes.guess_type(str(p))
    if not mime:
        mime = "image/png"
    b64 = base64.b64encode(p.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def normalize_image_ref(value: str) -> str:
    if value.startswith("http://") or value.startswith("https://") or value.startswith("data:"):
        return value
    return file_to_data_url(value)


def build_video_body(args):
    body = {
        "model": args.model,
        "prompt_optimizer": not args.no_prompt_optimizer,
        "duration": args.duration,
        "resolution": args.resolution,
        "aigc_watermark": args.watermark,
    }
    if getattr(args, "prompt", None):
        body["prompt"] = args.prompt
    if getattr(args, "fast_pretreatment", False):
        body["fast_pretreatment"] = args.fast_pretreatment
    if getattr(args, "first_frame_image", None):
        body["first_frame_image"] = normalize_image_ref(args.first_frame_image)
    if getattr(args, "last_frame_image", None):
        body["last_frame_image"] = normalize_image_ref(args.last_frame_image)
    return body


def cmd_create(args):
    body = build_video_body(args)
    data = request_json("POST", "/v1/video_generation", json_body=body, timeout=180)
    task_id = data.get("task_id")
    result = {
        "ok": True,
        "task_id": task_id,
        "base_resp": data.get("base_resp"),
    }
    if args.wait:
        status_data = wait_for_task(task_id, args.poll_interval, args.max_wait)
        result["status"] = status_data
        if status_data.get("status") == "Success" and status_data.get("file_id"):
            if args.download:
                path = download_file(status_data["file_id"], args.output)
                result["path"] = str(path)
    print_json(result)


def cmd_query(args):
    data = request_json("GET", "/v1/query/video_generation", params={"task_id": args.task_id}, timeout=60)
    print_json({"ok": True, **data})


def wait_for_task(task_id: str, poll_interval: int, max_wait: int):
    deadline = time.time() + max_wait
    last = None
    while time.time() < deadline:
        data = request_json("GET", "/v1/query/video_generation", params={"task_id": task_id}, timeout=60)
        last = data
        status = data.get("status")
        if status in ("Success", "Fail"):
            return data
        time.sleep(poll_interval)
    raise MiniMaxError(f"Timed out waiting for task {task_id}. Last status: {last}")


def download_file(file_id: str, output: str | None):
    if output:
        out_path = Path(output).expanduser().resolve()
    else:
        out_path = (OUTPUT_DIR / f"video-{timestamp_slug()}.mp4").resolve()
    return request_stream_download("/v1/files/retrieve_content", {"file_id": file_id}, out_path, timeout=1800)


def cmd_wait(args):
    data = wait_for_task(args.task_id, args.poll_interval, args.max_wait)
    result = {"ok": True, **data}
    if data.get("status") == "Success" and data.get("file_id") and args.download:
        result["path"] = str(download_file(data["file_id"], args.output))
    print_json(result)


def cmd_download(args):
    path = download_file(args.file_id, args.output)
    print_json({"ok": True, "file_id": args.file_id, "path": str(path)})


def main():
    ap = argparse.ArgumentParser(description="MiniMax video generation wrapper")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_create = sub.add_parser("create")
    p_create.add_argument("--prompt", required=True)
    p_create.add_argument("--model", default="MiniMax-Hailuo-2.3")
    p_create.add_argument("--duration", type=int, default=6)
    p_create.add_argument("--resolution", default="768P", choices=["720P", "768P", "1080P"])
    p_create.add_argument("--no-prompt-optimizer", action="store_true")
    p_create.add_argument("--fast-pretreatment", action="store_true")
    p_create.add_argument("--watermark", action="store_true")
    p_create.add_argument("--wait", action="store_true")
    p_create.add_argument("--download", action="store_true")
    p_create.add_argument("--poll-interval", type=int, default=10)
    p_create.add_argument("--max-wait", type=int, default=1800)
    p_create.add_argument("--output")
    p_create.set_defaults(func=cmd_create)

    p_i2v = sub.add_parser("i2v")
    p_i2v.add_argument("--first-frame-image", required=True, help="URL, data URL, or local image path")
    p_i2v.add_argument("--prompt")
    p_i2v.add_argument("--model", default="MiniMax-Hailuo-2.3")
    p_i2v.add_argument("--duration", type=int, default=6)
    p_i2v.add_argument("--resolution", default="768P", choices=["512P", "720P", "768P", "1080P"])
    p_i2v.add_argument("--no-prompt-optimizer", action="store_true")
    p_i2v.add_argument("--fast-pretreatment", action="store_true")
    p_i2v.add_argument("--watermark", action="store_true")
    p_i2v.add_argument("--wait", action="store_true")
    p_i2v.add_argument("--download", action="store_true")
    p_i2v.add_argument("--poll-interval", type=int, default=10)
    p_i2v.add_argument("--max-wait", type=int, default=1800)
    p_i2v.add_argument("--output")
    p_i2v.set_defaults(func=cmd_create)

    p_fl2v = sub.add_parser("fl2v")
    p_fl2v.add_argument("--first-frame-image", help="URL, data URL, or local image path")
    p_fl2v.add_argument("--last-frame-image", required=True, help="URL, data URL, or local image path")
    p_fl2v.add_argument("--prompt")
    p_fl2v.add_argument("--model", default="MiniMax-Hailuo-02", choices=["MiniMax-Hailuo-02"])
    p_fl2v.add_argument("--duration", type=int, default=6)
    p_fl2v.add_argument("--resolution", default="768P", choices=["768P", "1080P"])
    p_fl2v.add_argument("--no-prompt-optimizer", action="store_true")
    p_fl2v.add_argument("--watermark", action="store_true")
    p_fl2v.add_argument("--wait", action="store_true")
    p_fl2v.add_argument("--download", action="store_true")
    p_fl2v.add_argument("--poll-interval", type=int, default=10)
    p_fl2v.add_argument("--max-wait", type=int, default=1800)
    p_fl2v.add_argument("--output")
    p_fl2v.set_defaults(func=cmd_create)

    p_query = sub.add_parser("query")
    p_query.add_argument("task_id")
    p_query.set_defaults(func=cmd_query)

    p_wait = sub.add_parser("wait")
    p_wait.add_argument("task_id")
    p_wait.add_argument("--poll-interval", type=int, default=10)
    p_wait.add_argument("--max-wait", type=int, default=1800)
    p_wait.add_argument("--download", action="store_true")
    p_wait.add_argument("--output")
    p_wait.set_defaults(func=cmd_wait)

    p_download = sub.add_parser("download")
    p_download.add_argument("file_id")
    p_download.add_argument("--output")
    p_download.set_defaults(func=cmd_download)

    args = ap.parse_args()
    try:
        args.func(args)
    except MiniMaxError as e:
        raise SystemExit(str(e))


if __name__ == "__main__":
    main()
