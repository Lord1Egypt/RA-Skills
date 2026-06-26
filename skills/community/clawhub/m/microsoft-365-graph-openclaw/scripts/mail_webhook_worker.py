#!/usr/bin/env python3
"""Process queued Graph mail notifications and call OpenClaw hook."""
import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

import requests

from utils import STATE_DIR, append_log, authorized_request, cli_main, graph_url

DEFAULT_QUEUE_FILE = STATE_DIR / "mail_webhook_queue.jsonl"
DEFAULT_DEDUPE_FILE = STATE_DIR / "mail_webhook_dedupe.json"
DEFAULT_HOOK_URL = "http://127.0.0.1:3000/hooks/wake"
DEFAULT_HOOK_ACTION = "wake"
DEFAULT_WAKE_MODE = "now"
DEFAULT_DEDUPE_WINDOW_SECONDS = 60 * 60 * 6
DEFAULT_MAX_RETRIES = 5


def now_ts() -> int:
    return int(time.time())


def read_queue(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    events: List[Dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            append_log({"op": "mail_webhook_queue_corrupt_line", "line": line[:120]})
    return events


def write_queue(path: Path, events: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for event in events:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")


def load_dedupe(path: Path) -> Dict[str, int]:
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        append_log({"op": "mail_webhook_dedupe_corrupt"})
        return {}


def save_dedupe(path: Path, dedupe: Dict[str, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(dedupe, indent=2), encoding="utf-8")


def dedupe_key(event: Dict[str, Any]) -> str:
    return f"{event.get('subscriptionId', '-')}/{event.get('messageId', '-')}/{event.get('changeType', '-')}"


def prune_dedupe(dedupe: Dict[str, int], window_seconds: int) -> Dict[str, int]:
    threshold = now_ts() - window_seconds
    return {k: ts for k, ts in dedupe.items() if ts >= threshold}


def fetch_message(message_id: str) -> Dict[str, Any]:
    select_fields = ",".join(
        [
            "id",
            "subject",
            "from",
            "sender",
            "receivedDateTime",
            "webLink",
            "internetMessageId",
            "bodyPreview",
            "hasAttachments",
        ]
    )
    resp = authorized_request("GET", graph_url(f"/me/messages/{message_id}?$select={select_fields}"))
    return resp.json()


def post_hook(
    hook_url: str,
    hook_token: str,
    hook_action: str,
    wake_mode: str,
    session_key: str,
    event: Dict[str, Any],
    message: Dict[str, Any] | None = None,
) -> None:
    if hook_action == "wake":
        payload = {
            "text": (
                "New Graph mail notification received. "
                f"subscriptionId={event.get('subscriptionId')} "
                f"messageId={event.get('messageId')} "
                f"changeType={event.get('changeType')}. "
                "Process inbox now."
            ),
            "mode": wake_mode,
        }
    else:
        if not message:
            raise ValueError("message is required when hook_action=agent")
        sender = (message.get("from") or {}).get("emailAddress", {}).get("address") or "unknown"
        subject = message.get("subject") or "(no subject)"
        payload = {
            "message": f"New email received via Graph webhook.\nFrom: {sender}\nSubject: {subject}\nMessageId: {message.get('id')}",
            "name": "Graph Mail",
            "sessionKey": session_key,
            "source": "microsoft-365-graph-openclaw",
            "eventType": "graph.mail.notification",
            "event": event,
            "mail": {
                "id": message.get("id"),
                "subject": message.get("subject"),
                "from": (message.get("from") or {}).get("emailAddress", {}).get("address"),
                "receivedDateTime": message.get("receivedDateTime"),
                "bodyPreview": message.get("bodyPreview"),
                "webLink": message.get("webLink"),
                "hasAttachments": message.get("hasAttachments"),
                "internetMessageId": message.get("internetMessageId"),
            },
            "receivedAt": datetime.now(timezone.utc).isoformat(),
        }
    headers = {"Content-Type": "application/json"}
    if hook_token:
        headers["Authorization"] = f"Bearer {hook_token}"
        headers["X-Hook-Token"] = hook_token
    resp = requests.post(hook_url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()


def process_once(args: argparse.Namespace) -> Tuple[int, int, int]:
    queue_file = Path(args.queue_file).expanduser().resolve()
    dedupe_file = Path(args.dedupe_file).expanduser().resolve()

    events = read_queue(queue_file)
    if not events:
        print("Queue is empty.")
        return 0, 0, 0

    dedupe = prune_dedupe(load_dedupe(dedupe_file), args.dedupe_window_seconds)
    kept: List[Dict[str, Any]] = []
    processed = 0
    duplicates = 0
    failed = 0

    for event in events:
        key = dedupe_key(event)
        if key in dedupe:
            duplicates += 1
            append_log({"op": "mail_webhook_skip_duplicate", "key": key})
            continue

        try:
            msg = None
            if args.hook_action == "agent":
                msg = fetch_message(event["messageId"])
            if not args.dry_run:
                post_hook(
                    args.hook_url,
                    args.hook_token,
                    args.hook_action,
                    args.wake_mode,
                    args.session_key,
                    event,
                    msg,
                )
            dedupe[key] = now_ts()
            processed += 1
            append_log({"op": "mail_webhook_processed", "messageId": event.get("messageId"), "dryRun": args.dry_run})
        except Exception as exc:  # noqa: BLE001
            retries = int(event.get("retries", 0)) + 1
            event["retries"] = retries
            event["lastError"] = str(exc)
            if retries < args.max_retries:
                kept.append(event)
            else:
                append_log(
                    {
                        "op": "mail_webhook_drop_max_retries",
                        "messageId": event.get("messageId"),
                        "error": str(exc),
                        "retries": retries,
                    }
                )
            failed += 1

    write_queue(queue_file, kept)
    save_dedupe(dedupe_file, dedupe)
    print(json.dumps({"processed": processed, "duplicates": duplicates, "failed": failed, "remaining": len(kept)}, indent=2))
    return processed, duplicates, failed


def handle_once(args: argparse.Namespace) -> None:
    process_once(args)


def handle_loop(args: argparse.Namespace) -> None:
    print(f"Starting worker loop. Poll interval: {args.poll_seconds}s")
    while True:
        process_once(args)
        time.sleep(args.poll_seconds)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Process queued Graph mail webhook notifications.")
    sub = parser.add_subparsers(dest="command", required=True)

    def add_shared(p: argparse.ArgumentParser) -> None:
        p.add_argument("--queue-file", default=str(DEFAULT_QUEUE_FILE), help="Queue file path.")
        p.add_argument("--dedupe-file", default=str(DEFAULT_DEDUPE_FILE), help="Dedupe state file path.")
        p.add_argument("--dedupe-window-seconds", type=int, default=DEFAULT_DEDUPE_WINDOW_SECONDS, help="Dedupe time window.")
        p.add_argument("--max-retries", type=int, default=DEFAULT_MAX_RETRIES, help="Max retries before dropping.")
        p.add_argument("--hook-url", default=DEFAULT_HOOK_URL, help="OpenClaw hook URL (/hooks/wake by default).")
        p.add_argument(
            "--hook-action",
            choices=["wake", "agent"],
            default=DEFAULT_HOOK_ACTION,
            help="Webhook action mode: wake (default) or agent.",
        )
        p.add_argument(
            "--wake-mode",
            choices=["now", "next-heartbeat"],
            default=DEFAULT_WAKE_MODE,
            help="Wake mode used when --hook-action wake.",
        )
        p.add_argument("--hook-token", default="", help="OpenClaw hook token.")
        p.add_argument("--session-key", default="hook:graph-mail", help="OpenClaw session key (used by agent mode).")
        p.add_argument("--dry-run", action="store_true", help="Fetch mail but do not call hook.")

    p_once = sub.add_parser("once", help="Process queued events once.")
    add_shared(p_once)

    p_loop = sub.add_parser("loop", help="Run worker in continuous loop.")
    add_shared(p_loop)
    p_loop.add_argument("--poll-seconds", type=int, default=10, help="Loop sleep interval.")

    return parser


def handler() -> None:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "once":
        handle_once(args)
    elif args.command == "loop":
        handle_loop(args)


if __name__ == "__main__":
    cli_main(handler)
