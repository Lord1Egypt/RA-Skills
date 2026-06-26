#!/usr/bin/env python3
"""
LinkFoxAgent CLI - Cross-border e-commerce AI Agent.

Submit tasks to LinkFoxAgent and retrieve structured results.
Supports 80 tools for product research, competitor analysis, keyword tracking,
review insights, patent detection, and more.

Default mode is background: submit task and return messageId immediately,
so the caller can continue while the task runs (tasks typically take 1-5 min).
Use --status for a quick non-blocking progress check, --poll to keep waiting,
or --wait to block until done.

Usage:
    linkfox.py "<task>"                       # Submit in background, return messageId (default)
    linkfox.py --wait "<task>"               # Submit and wait for result (blocking)
    linkfox.py --status <messageId>           # One-shot status & progress check (NO polling)
    linkfox.py --poll <messageId>             # Poll result for a messageId until terminal
    linkfox.py --list-recent [N]              # Show the N most recent local tasks (default 10)
    linkfox.py --timeout 600 --poll <id>     # Custom timeout when polling (seconds)
    linkfox.py --format json --poll <id>     # Output raw JSON

Every successful submission immediately writes scripts/output/{ts}/result.json
containing the messageId + original task text — so even if the background mode's
stdout is not captured, you can recover the messageId later with --list-recent.

While polling, the script emits server-side progress to stderr in the form
"[progress] 3/10 当前步骤名" whenever it changes, and folds it into the periodic
heartbeat. The progress line is informational; the final result is on stdout.

Environment:
    LINKFOXAGENT_API_KEY - Required API key for LinkFoxAgent
"""

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


LINKFOXAGENT_BASE_URL = "https://agent-api.linkfox.com/"
SUBMIT_ENDPOINT = "chat/saveMessageForApi"
POLL_ENDPOINT = "chat/getMessageForApi"

TERMINAL_STATUSES = {"finished", "error", "cancel"}

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_ROOT = os.path.join(SCRIPT_DIR, "output")
META_FILENAME = "result.json"


def get_api_key() -> str:
    """Get API key from environment."""
    key = os.environ.get("LINKFOXAGENT_API_KEY")
    if not key:
        print(
            "Error: LINKFOXAGENT_API_KEY environment variable not set.\n"
            "Get your API key from: https://skill.linkfox.com/linkfoxagent/guid.htm\n"
            "Then set it:\n"
            "  export LINKFOXAGENT_API_KEY=your-key-here",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def api_request(endpoint: str, payload: dict) -> dict:
    """Make a POST request to the LinkFoxAgent API."""
    api_key = get_api_key()
    url = f"{LINKFOXAGENT_BASE_URL}{endpoint}"
    data = json.dumps(payload).encode("utf-8")

    req = Request(
        url,
        data=data,
        headers={
            "Authorization": api_key,
            "Content-Type": "application/json",
            "User-Agent": "LinkFoxAgent-Skill/1.0",
        },
        method="POST",
    )

    try:
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))
    except HTTPError as e:
        body = e.read().decode("utf-8") if e.fp else ""
        return {"error": f"HTTP {e.code}: {e.reason}", "details": body}
    except URLError as e:
        return {"error": f"Connection failed: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def submit_task(text: str) -> dict:
    """Submit a task to LinkFoxAgent. Returns response with messageId."""
    return api_request(SUBMIT_ENDPOINT, {"text": text})


# ---------- Per-task output directory bookkeeping ---------------------------
#
# Each task gets its own folder under scripts/output/{YYYYMMDDHHmm}/, created
# the moment the task is submitted (NOT when results arrive). The folder
# always contains a result.json describing the task — `messageId`, original
# `task` text, `submittedAt`, `status`, and once the task ends, `url`
# (shareUrl) and `completedAt`.
#
# Why submit-time creation: the default background mode returns immediately
# after submitting, so the messageId would otherwise live only on stdout.
# By dropping a result.json at submit time, the user (or agent) can later
# `ls -t output/` to find the most recent task and recover its messageId
# without having captured the original stdout.

def _meta_path(task_dir: str) -> str:
    return os.path.join(task_dir, META_FILENAME)


def find_task_dir(message_id: str):
    """Return the existing output dir for a messageId, or None.

    Cheap: each task has its own dir and we only read tiny JSON files.
    """
    if not message_id or not os.path.isdir(OUTPUT_ROOT):
        return None
    for name in sorted(os.listdir(OUTPUT_ROOT), reverse=True):
        d = os.path.join(OUTPUT_ROOT, name)
        meta_file = _meta_path(d)
        if not os.path.isfile(meta_file):
            continue
        try:
            with open(meta_file, encoding="utf-8") as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue
        if isinstance(data, dict) and data.get("messageId") == message_id:
            return d
    return None


def ensure_task_dir(message_id: str, task: str = "") -> str:
    """Get the dir for messageId, creating a new timestamped folder if missing.

    On first creation, writes an initial result.json with
    {messageId, task, status='submitted', submittedAt, url=''}.
    Re-runs (poll/status of an already-tracked task) reuse the same folder.
    """
    existing = find_task_dir(message_id)
    if existing:
        return existing

    os.makedirs(OUTPUT_ROOT, exist_ok=True)
    base = datetime.now().strftime("%Y%m%d%H%M")
    task_dir = os.path.join(OUTPUT_ROOT, base)
    # Two tasks in the same minute → suffix to keep them separate
    suffix = 0
    while os.path.isdir(task_dir):
        suffix += 1
        task_dir = os.path.join(OUTPUT_ROOT, f"{base}_{suffix}")
    os.makedirs(task_dir, exist_ok=True)

    meta = {
        "messageId": message_id,
        "task": task or "",
        "status": "submitted",
        "submittedAt": datetime.now().isoformat(timespec="seconds"),
        "url": "",
    }
    try:
        with open(_meta_path(task_dir), "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2, ensure_ascii=False)
    except OSError as e:
        print(f"Warning: failed to write initial meta for {message_id}: {e}", file=sys.stderr)
    return task_dir


def update_meta(task_dir: str, **fields) -> None:
    """Merge `fields` into the dir's result.json. Skips empty/None values
    so we never blank out a value that an earlier write already set
    (e.g. preserving original `task` when --poll has no task text)."""
    meta_path = _meta_path(task_dir)
    data: dict = {}
    if os.path.isfile(meta_path):
        try:
            with open(meta_path, encoding="utf-8") as f:
                data = json.load(f) or {}
        except (json.JSONDecodeError, OSError):
            data = {}
    for k, v in fields.items():
        if v in (None, ""):
            continue
        data[k] = v
    try:
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except OSError as e:
        print(f"Warning: failed to update meta at {meta_path}: {e}", file=sys.stderr)
# -----------------------------------------------------------------------------


def poll_result(message_id: str, max_wait: int = 300, interval: int = 5) -> dict:
    """Poll for task result until terminal status or timeout.

    While the task is running, the server returns a `progress` field of the form
    "n/m 当前步骤名"（empty once the task ends）. This function emits that progress
    to stderr whenever it changes and folds it into the 30-second heartbeat, so an
    observer tailing stderr can tell what step the agent is on. The final API
    response is returned as-is for the caller to inspect.
    """
    elapsed = 0
    last_progress = ""
    last_result: dict = {}
    while elapsed < max_wait:
        result = api_request(POLL_ENDPOINT, {"id": message_id})
        if isinstance(result, dict):
            last_result = result

        if "error" in result:
            return result

        status = result.get("status", "")
        if status in TERMINAL_STATUSES:
            return result

        # Surface server-side progress when it changes (avoid spamming stderr)
        progress = result.get("progress") or ""
        if progress and progress != last_progress:
            print(f"[progress] {progress}", file=sys.stderr)
            last_progress = progress

        time.sleep(interval)
        elapsed += interval

        if elapsed % 30 == 0:
            heartbeat = f"... still working ({elapsed}s elapsed)"
            if last_progress:
                heartbeat += f" — {last_progress}"
            print(heartbeat, file=sys.stderr)

    return {
        "error": (
            f"Timeout after {max_wait}s. messageId: {message_id}. "
            f"Use --status {message_id} to check current progress, "
            f"or --poll {message_id} to keep waiting."
        ),
        "lastProgress": last_result.get("progress") if isinstance(last_result, dict) else None,
    }


def json_to_csv(parsed, result_name: str, result_index: int, output_dir: str) -> str | None:
    """Convert a JSON result to a CSV file.

    Handles these payload shapes:
    - Object with 'columns' (field→title map) + data array in 'data', 'products',
      'items', etc.  columns[].title is used as Chinese column header.
    - Plain array of objects: headers derived from field names in first-appearance
      order; no Chinese title mapping.
    - Wrapper object whose first list-of-dicts value is the data array (fallback).

    If 'columns' is absent, raw English field names are used as headers.

    Returns the absolute path of the written CSV, or None if not a tabular shape.
    """
    col_map: dict[str, str] = {}
    ordered_fields: list[str] = []
    data = None

    if isinstance(parsed, dict):
        # Extract columns mapping when present (field → Chinese title)
        columns = parsed.get("columns")
        if isinstance(columns, list):
            col_map = {
                col["field"]: col["title"]
                for col in columns
                if isinstance(col, dict) and "field" in col and "title" in col
            }
            ordered_fields = [col["field"] for col in columns if isinstance(col, dict) and "field" in col]

        # Locate data array: prefer common keys first, then any list-of-dicts
        for candidate_key in ("data", "products", "items", "list"):
            v = parsed.get(candidate_key)
            if isinstance(v, list) and v and isinstance(v[0], dict):
                data = v
                break
        if data is None:
            for v in parsed.values():
                if isinstance(v, list) and v and isinstance(v[0], dict):
                    data = v
                    break
        if data is None:
            return None

        # Append any extra fields from data rows not already in ordered_fields
        seen: set[str] = set(ordered_fields)
        for row in data:
            for key in row:
                if key not in seen:
                    ordered_fields.append(key)
                    seen.add(key)

    elif isinstance(parsed, list) and parsed and isinstance(parsed[0], dict):
        data = parsed
        seen_b: set[str] = set()
        for row in data:
            for key in row:
                if key not in seen_b:
                    ordered_fields.append(key)
                    seen_b.add(key)

    else:
        return None

    if not data or not ordered_fields:
        return None

    safe_name = "".join(c if (c.isalnum() or c in "-_") else "_" for c in result_name)
    filename = f"result_{result_index}_{safe_name}.csv"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        # Header: Chinese title if available, otherwise raw field name
        writer.writerow([col_map.get(field, field) for field in ordered_fields])
        for row in data:
            writer.writerow([row.get(field, "") for field in ordered_fields])

    return filepath


def format_result(result: dict, message_id: str = "", task_text: str = "") -> str:
    """Format a poll result as human-readable text.

    JSON results that contain both 'columns' and 'data' are automatically
    exported to a CSV file (with Chinese column headers from columns[].title).
    The output reports the local CSV path instead of dumping raw JSON, so the
    LLM can decide whether to read and forward the file to the user.
    """
    if "error" in result:
        return f"Error: {result['error']}"

    lines = []

    # Reuse the dir created at submit time (or create one now if this is a
    # --poll of a task we've never seen before, e.g. submitted in another session).
    output_dir = ensure_task_dir(message_id or "unknown", task=task_text)

    status = result.get("status", "unknown")
    lines.append(f"Status: {status}")

    # Server-side progress is non-empty only while the task is still running.
    # In a terminal state (finished/error/cancel/stop) it is "" and we omit the line.
    progress = result.get("progress")
    if progress:
        lines.append(f"Progress: {progress}")

    share_url = result.get("shareUrl")
    if share_url:
        lines.append(f"ShareURL: {share_url}")

    reflection = result.get("reflection")
    if reflection:
        lines.append(f"\n{reflection}")

    results = result.get("results", [])
    for i, item in enumerate(results, 1):
        content_type = item.get("type", "unknown")
        content = item.get("content", "")
        name = item.get("name", f"result_{i}")

        if content_type == "html":
            lines.append(f"\n--- Result {i} (HTML URL) ---")
            lines.append(content)
        elif content_type == "json":
            try:
                parsed = json.loads(content) if isinstance(content, str) else content
            except (json.JSONDecodeError, TypeError):
                parsed = None

            if parsed is not None:
                # Save raw JSON
                safe_name = "".join(c if (c.isalnum() or c in "-_") else "_" for c in name)
                json_filename = f"{i}_{safe_name}.json"
                json_path = os.path.join(output_dir, json_filename)
                with open(json_path, "w", encoding="utf-8") as jf:
                    json.dump(parsed, jf, indent=2, ensure_ascii=False)

                # tablesListWorkbenches: multiple tables → multiple CSVs
                if isinstance(parsed, dict) and parsed.get("type") == "tablesListWorkbenches":
                    tables = parsed.get("tables", [])
                    lines.append(f"\n--- Result {i} (JSON → {len(tables)} CSV) ---")
                    lines.append(f"Name: {name}")
                    lines.append(f"JSON saved to: {json_path}")
                    for j, table in enumerate(tables, 1):
                        tname = table.get("name", f"{name}_table{j}")
                        csv_path = json_to_csv(table, tname, i * 100 + j, output_dir)
                        if csv_path:
                            lines.append(f"CSV[{j}] ({tname}) saved to: {csv_path}")
                        else:
                            lines.append(f"CSV[{j}] ({tname}): 无法转换")
                else:
                    csv_path = json_to_csv(parsed, name, i, output_dir)
                    if csv_path:
                        lines.append(f"\n--- Result {i} (JSON → CSV) ---")
                        lines.append(f"Name: {name}")
                        lines.append(f"JSON saved to: {json_path}")
                        lines.append(f"CSV saved to: {csv_path}")
                    else:
                        lines.append(f"\n--- Result {i} (JSON Data) ---")
                        lines.append(f"JSON saved to: {json_path}")
                        lines.append(json.dumps(parsed, indent=2, ensure_ascii=False))
            else:
                lines.append(f"\n--- Result {i} (JSON Data, unparseable) ---")
                lines.append(str(content))
        else:
            lines.append(f"\n--- Result {i} ({content_type}) ---")
            lines.append(str(content))

    # Update result.json with terminal info (preserving submittedAt + initial fields)
    update_meta(
        output_dir,
        status=result.get("status"),
        url=result.get("shareUrl"),
        messageId=message_id,
        task=task_text,
        completedAt=datetime.now().isoformat(timespec="seconds"),
    )
    lines.append(f"\nResult meta saved to: {os.path.join(output_dir, META_FILENAME)}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="LinkFoxAgent - Cross-border e-commerce AI Agent CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("task", nargs="?", help="Task description to submit")
    parser.add_argument(
        "--stdin", action="store_true",
        help="Read task from stdin instead of positional argument (safe against shell injection)",
    )
    parser.add_argument(
        "--wait", action="store_true",
        help="Block until task completes and return the result (default: background, return messageId immediately)",
    )
    parser.add_argument(
        "--poll", dest="poll_id", metavar="MESSAGE_ID",
        help="Poll result for an existing messageId until terminal or timeout",
    )
    parser.add_argument(
        "--status", dest="status_id", metavar="MESSAGE_ID",
        help="One-shot check of current status & progress for a messageId (no polling)",
    )
    parser.add_argument(
        "--list-recent", dest="list_recent", type=int, nargs="?", const=10, metavar="N",
        help="List the most recent N tasks (default 10) with messageId / task / status from local output/",
    )
    parser.add_argument(
        "--timeout", type=int, default=300,
        help="Max wait time in seconds (default: 300)",
    )
    parser.add_argument(
        "--interval", type=int, default=5,
        help="Poll interval in seconds (default: 5)",
    )
    parser.add_argument(
        "--format", "-f", choices=["json", "text"], default="text",
        help="Output format (default: text)",
    )

    args = parser.parse_args()

    # Mode: list recent tasks from local output/ — pure local, no API call.
    # Useful when the user / agent forgot a messageId and wants to recover it.
    if args.list_recent is not None:
        n = max(1, args.list_recent)
        if not os.path.isdir(OUTPUT_ROOT):
            print(f"(no local tasks yet — output dir not found: {OUTPUT_ROOT})")
            return
        rows = []
        for name in sorted(os.listdir(OUTPUT_ROOT), reverse=True):
            d = os.path.join(OUTPUT_ROOT, name)
            meta_file = _meta_path(d)
            if not os.path.isfile(meta_file):
                continue
            try:
                with open(meta_file, encoding="utf-8") as f:
                    data = json.load(f) or {}
            except (json.JSONDecodeError, OSError):
                continue
            rows.append({
                "submittedAt": data.get("submittedAt", name),
                "messageId": data.get("messageId", ""),
                "status": data.get("status", "submitted"),
                "task": (data.get("task") or "")[:80],
                "dir": d,
            })
            if len(rows) >= n:
                break
        if args.format == "json":
            print(json.dumps(rows, indent=2, ensure_ascii=False))
        else:
            if not rows:
                print("(no local tasks recorded yet)")
                return
            for r in rows:
                print(f"{r['submittedAt']}  {r['status']:<10}  {r['messageId']}  {r['task']}")
        return

    # Mode: one-shot status — single API call, no polling, returns immediately.
    # Useful when the main session wants to peek at "where is the task now?"
    # without spawning another sub-agent.
    if args.status_id:
        result = api_request(POLL_ENDPOINT, {"id": args.status_id})
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            if "error" in result:
                print(f"Error: {result['error']}")
            else:
                status = result.get("status", "unknown")
                progress = result.get("progress") or ""
                print(f"Status: {status}")
                if progress:
                    print(f"Progress: {progress}")
                elif status in TERMINAL_STATUSES:
                    print(f"Progress: (task ended; use --poll {args.status_id} to fetch full result)")
                else:
                    print("Progress: (no progress info yet)")
        return

    # Mode: poll existing messageId
    if args.poll_id:
        result = poll_result(args.poll_id, max_wait=args.timeout, interval=args.interval)
        if args.format == "json":
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(format_result(result, message_id=args.poll_id))
        return

    # Require task for submit modes
    if args.stdin:
        task_text = sys.stdin.read().strip()
        if not task_text:
            parser.error("stdin was empty")
    elif args.task:
        task_text = args.task
    else:
        parser.error("task is required (or use --stdin, --status MESSAGE_ID, or --poll MESSAGE_ID)")

    response = submit_task(task_text)
    if "error" in response:
        error_msg = response["error"]
        print(f"Error: {error_msg}", file=sys.stderr)
        if response.get("details"):
            print(f"Details: {response['details']}", file=sys.stderr)
        # HTTP 401/403 almost always means a bad or missing API key
        if "401" in error_msg or "403" in error_msg or "Unauthorized" in error_msg or "Forbidden" in error_msg:
            key_val = os.environ.get("LINKFOXAGENT_API_KEY") or ""
            masked = key_val[:4] + "****" + key_val[-4:] if len(key_val) > 8 else ("(未设置)" if not key_val else "****")
            print(
                "\nHint: 任务发起失败，请检查 LINKFOXAGENT_API_KEY 是否正确。\n"
                f"  当前值: {masked}\n"
                "  获取 API Key: https://skill.linkfox.com/linkfoxagent/guid.htm",
                file=sys.stderr,
            )
        sys.exit(1)

    message_id = response.get("messageId") or ""
    if not message_id:
        key_val = os.environ.get("LINKFOXAGENT_API_KEY") or ""
        masked = key_val[:4] + "****" + key_val[-4:] if len(key_val) > 8 else ("(未设置)" if not key_val else "****")
        print(
            "Error: 任务发起失败，服务器未返回 messageId。\n"
            "请检查 LINKFOXAGENT_API_KEY 是否正确。\n"
            f"  当前值: {masked}\n"
            "  获取 API Key: https://skill.linkfox.com/linkfoxagent/guid.htm\n"
            f"  服务器原始响应: {response}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Drop a result.json the moment submission succeeds, so the user / agent can
    # always recover the messageId by listing scripts/output/ later — even if
    # the background mode's stdout was not captured.
    task_dir = ""
    try:
        task_dir = ensure_task_dir(message_id, task=task_text)
    except Exception as e:
        print(f"Warning: 无法落盘 messageId 元数据: {e}", file=sys.stderr)

    # Mode: background (default) — return messageId immediately so the caller can continue
    if not args.wait:
        out = {"messageId": message_id}
        if task_dir:
            out["taskDir"] = task_dir
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    # Mode: --wait — block until task completes
    print(f"Task submitted. messageId: {message_id}", file=sys.stderr)
    print("Waiting for result...", file=sys.stderr)

    result = poll_result(message_id, max_wait=args.timeout, interval=args.interval)
    if args.format == "json":
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(format_result(result, message_id=message_id, task_text=task_text))

    if result.get("status") == "error":
        sys.exit(1)


if __name__ == "__main__":
    main()
