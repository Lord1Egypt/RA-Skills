#!/usr/bin/env python3
"""
Kaipai skill CLI - 使用SDK的CLI入口

Commands:
    run-task, query-task, upload, list-tasks
    last-task, history, resolve-input, notify

用法:
    python kaipai_ai.py --ak xxx --sk yyy run-task --task txt2img
    python kaipai_ai.py run-task --task eraser_watermark --input /path/to/image.jpg
    python kaipai_ai.py query-task --task-id abc123
    python kaipai_ai.py last-task
    python kaipai_ai.py history
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Add parent directory to path to import sdk
PROJECT_DIR = Path(__file__).resolve().parent.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

# Import SDK CLI commands
from sdk import SkillClient, TaskRunner
from sdk.core.client import ConsumeDeniedError
from sdk.core.config import INVOKE

# State directory
STATE_DIR = Path.home() / ".openclaw" / "workspace" / "openclaw-kaipai-ai"
LAST_TASK_FILE = STATE_DIR / "last_task.json"
HISTORY_DIR = STATE_DIR / "history"


def _print_json(data: dict) -> None:
    """Print result as JSON"""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def _save_task_record(record: dict) -> None:
    """Save task record to state directory"""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    with open(LAST_TASK_FILE, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    # Also save to history
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    hist_path = HISTORY_DIR / f"task_{ts}.json"
    with open(hist_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    # Keep only last 50 records
    history_files = sorted(HISTORY_DIR.glob("task_*.json"))
    if len(history_files) > 50:
        for old in history_files[:-50]:
            old.unlink(missing_ok=True)


def cmd_run_task(args: argparse.Namespace) -> int:
    """Run algorithm task"""
    try:
        runner = TaskRunner(ak=args.ak, sk=args.sk)

        # Parse params
        params = {}
        if args.params:
            params = json.loads(args.params)

        # Callback for async submission
        def on_submitted(task_id: str):
            record = {
                "saved_at": datetime.now(timezone.utc).isoformat(),
                "task_name": args.task,
                "input": args.input or "",
                "task_id": task_id,
                "skill_status": "polling",
            }
            _save_task_record(record)
            print(f"[info] Task submitted: {task_id}", file=sys.stderr)

        # Run task
        result = runner.run(
            task_name=args.task,
            input_src=args.input or "",
            params=params,
            on_async_submitted=on_submitted
        )

        # Save successful record
        if result.get("skill_status") == "completed":
            record = {
                "saved_at": datetime.now(timezone.utc).isoformat(),
                "task_name": args.task,
                "input": args.input or "",
                "task_id": result.get("task_id"),
                "skill_status": "completed",
                "primary_result_url": result.get("primary_result_url"),
                "output_urls": result.get("output_urls", []),
            }
            _save_task_record(record)

        _print_json(result)
        return 0 if result.get("skill_status") == "completed" else 1

    except ConsumeDeniedError as e:
        error_result = {
            "error": "quota_error",
            "code": e.code,
            "message": e.msg,
            "skill_status": "failed",
            "failure_stage": "consume_quota",
        }
        _print_json(error_result)
        return 1
    except Exception as e:
        _print_json({
            "error": str(e),
            "skill_status": "failed"
        })
        return 1


def cmd_query_task(args: argparse.Namespace) -> int:
    """Query task status"""
    try:
        client = SkillClient(ak=args.ak, sk=args.sk)
        result = client.query(args.task_id)

        _print_json(result)
        return 0 if result.get("skill_status") == "completed" else 1

    except Exception as e:
        _print_json({
            "error": str(e),
            "skill_status": "failed"
        })
        return 1


def cmd_upload(args: argparse.Namespace) -> int:
    """Upload file to OSS"""
    if not os.path.isfile(args.file):
        _print_json({
            "error": f"File not found: {args.file}",
            "status": "failed"
        })
        return 1

    try:
        client = SkillClient(ak=args.ak, sk=args.sk)
        url_data = client.api.upload_file(args.file)

        _print_json({
            "status": "success",
            "url_data": url_data
        })
        return 0

    except Exception as e:
        _print_json({
            "error": str(e),
            "status": "failed"
        })
        return 1


def cmd_list_tasks(args: argparse.Namespace) -> int:
    """List available tasks"""
    try:
        # Initialize client to fetch remote config
        SkillClient(ak=args.ak, sk=args.sk)

        tasks = []
        for name, config in INVOKE.items():
            tasks.append({
                "name": name,
                "task": config.get("task"),
                "task_type": config.get("task_type", "mtlab"),
                "params": config.get("params", {})
            })

        _print_json({
            "status": "success",
            "tasks": tasks,
            "count": len(tasks)
        })
        return 0

    except Exception as e:
        _print_json({
            "error": str(e),
            "status": "failed"
        })
        return 1


def cmd_last_task(args: argparse.Namespace) -> int:
    """Show last task record"""
    if not LAST_TASK_FILE.is_file():
        _print_json({"message": "No saved task yet.", "record": None})
        return 0

    try:
        with open(LAST_TASK_FILE, encoding="utf-8") as f:
            record = json.load(f)
        _print_json(record)
        return 0
    except (json.JSONDecodeError, OSError) as e:
        _print_json({"error": "Failed to read last_task.json", "detail": str(e)})
        return 1


def cmd_history(args: argparse.Namespace) -> int:
    """Show task history"""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(HISTORY_DIR.glob("task_*.json"))
    jobs = []
    for path in files[-50:]:
        try:
            with open(path, encoding="utf-8") as f:
                jobs.append(json.load(f))
        except (json.JSONDecodeError, OSError):
            continue

    _print_json({"jobs": jobs, "count": len(jobs)})
    return 0


def cmd_resolve_input(args: argparse.Namespace) -> int:
    """Resolve input (download from URL or copy file)"""
    import shutil
    import uuid

    out_dir = Path(args.output_dir).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        if args.file:
            # Copy local file
            src = Path(args.file).expanduser()
            if not src.is_file():
                _print_json({"error": f"File not found: {args.file}"})
                return 1

            dest = out_dir / f"kaipai_in_{uuid.uuid4().hex[:10]}_{src.name}"
            shutil.copy2(src, dest)

            _print_json({
                "path": str(dest.resolve()),
                "filename": src.name,
                "bytes": src.stat().st_size,
            })
            return 0

        elif args.url:
            # Download from URL
            import requests

            url = args.url.strip()
            if not url.startswith(("http://", "https://")):
                _print_json({"error": "Only http:// and https:// URLs are allowed"})
                return 1

            resp = requests.get(url, stream=True, timeout=(15, 120))
            resp.raise_for_status()

            # Determine filename
            url_path = url.split("?")[0]
            ext = url_path.rsplit(".", 1)[-1] if "." in url_path else "bin"
            filename = f"download_{uuid.uuid4().hex[:8]}.{ext}"

            dest = out_dir / f"kaipai_in_{uuid.uuid4().hex[:10]}_{filename}"

            # Download with size limit
            max_bytes = 100 * 1024 * 1024  # 100MB
            total = 0
            with open(dest, "wb") as f:
                for chunk in resp.iter_content(chunk_size=65536):
                    if chunk:
                        total += len(chunk)
                        if total > max_bytes:
                            dest.unlink()
                            _print_json({"error": "File too large (max 100MB)"})
                            return 1
                        f.write(chunk)

            _print_json({
                "path": str(dest.resolve()),
                "filename": filename,
                "bytes": total,
            })
            return 0

        else:
            _print_json({"error": "Please provide --file or --url"})
            return 1

    except Exception as e:
        _print_json({"error": str(e)})
        return 1


def cmd_notify(args: argparse.Namespace) -> int:
    """Send notification (Feishu or Telegram)"""
    try:
        from notifications import get_notifier

        notifier = get_notifier(args.channel)

        if args.type == "image":
            result = notifier.send_image(
                image_source=args.source,
                recipient=args.to,
                caption=args.caption or ""
            )
        elif args.type == "video":
            result = notifier.send_video(
                video_path=args.source,
                recipient=args.to,
                video_url=args.video_url or "",
                caption=args.caption or ""
            )
        else:
            _print_json({"error": f"Unknown type: {args.type}"})
            return 1

        _print_json(result)
        return 0 if result.get("status") == "ok" else 1

    except Exception as e:
        _print_json({"error": str(e), "status": "failed"})
        return 1


def main() -> int:
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Kaipai skill CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run task (using env vars MT_AK, MT_SK)
  python kaipai_ai.py run-task --task txt2img

  # Run with explicit credentials
  python kaipai_ai.py --ak xxx --sk yyy run-task --task eraser_watermark --input image.jpg

  # Query task status
  python kaipai_ai.py query-task --task-id abc123

  # Upload file
  python kaipai_ai.py upload --file image.jpg

  # Show last task
  python kaipai_ai.py last-task

  # Show history
  python kaipai_ai.py history

  # Send notification
  python kaipai_ai.py notify --channel feishu --type image --source result.jpg --to oc_xxx
        """
    )

    # Global options
    parser.add_argument("--ak", default=os.environ.get("MT_AK"), help="Access Key (or MT_AK env var)")
    parser.add_argument("--sk", default=os.environ.get("MT_SK"), help="Secret Key (or MT_SK env var)")

    sub = parser.add_subparsers(dest="command", help="Available commands")

    # run-task
    p_run = sub.add_parser("run-task", help="Run algorithm task")
    p_run.add_argument("--task", required=True, help="Task name")
    p_run.add_argument("--input", default="", help="Input file or URL")
    p_run.add_argument("--params", help="Task params (JSON)")
    p_run.set_defaults(func=cmd_run_task)

    # query-task
    p_query = sub.add_parser("query-task", help="Query task status")
    p_query.add_argument("--task-id", required=True, help="Task ID")
    p_query.set_defaults(func=cmd_query_task)

    # upload
    p_upload = sub.add_parser("upload", help="Upload file to OSS")
    p_upload.add_argument("--file", required=True, help="File path")
    p_upload.set_defaults(func=cmd_upload)

    # list-tasks
    p_list = sub.add_parser("list-tasks", help="List available tasks")
    p_list.set_defaults(func=cmd_list_tasks)

    # last-task
    p_last = sub.add_parser("last-task", help="Show last task record")
    p_last.set_defaults(func=cmd_last_task)

    # history
    p_hist = sub.add_parser("history", help="Show task history")
    p_hist.set_defaults(func=cmd_history)

    # resolve-input
    p_res = sub.add_parser("resolve-input", help="Resolve input file/URL")
    p_res.add_argument("--file", help="Local file path")
    p_res.add_argument("--url", help="URL to download")
    p_res.add_argument("--output-dir", default="/tmp", help="Output directory")
    p_res.set_defaults(func=cmd_resolve_input)

    # notify
    p_notify = sub.add_parser("notify", help="Send notification")
    p_notify.add_argument("--channel", required=True, choices=["feishu", "telegram"], help="Notification channel")
    p_notify.add_argument("--type", required=True, choices=["image", "video"], help="Content type")
    p_notify.add_argument("--source", required=True, help="File path or URL")
    p_notify.add_argument("--to", required=True, help="Recipient ID")
    p_notify.add_argument("--caption", help="Caption text")
    p_notify.add_argument("--video-url", help="Video download URL")
    p_notify.set_defaults(func=cmd_notify)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    # Check AK/SK for commands that need them
    commands_needing_auth = ["run-task", "query-task", "upload", "list-tasks"]
    if args.command in commands_needing_auth:
        if not args.ak or not args.sk:
            parser.error(f"Command '{args.command}' requires --ak and --sk (or MT_AK/MT_SK env vars)")

    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
