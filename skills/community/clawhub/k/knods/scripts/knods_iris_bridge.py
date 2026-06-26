#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib import parse, request


def load_env_file(path: Path) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def add_token(url: str, token: str) -> str:
    parsed = parse.urlparse(url)
    qs = parse.parse_qs(parsed.query, keep_blank_values=True)
    if "token" not in qs:
        qs["token"] = [token]
    query = parse.urlencode(qs, doseq=True)
    return parse.urlunparse(parsed._replace(query=query))


def resolve_urls(base_url: str, token: Optional[str]) -> Tuple[str, str]:
    parsed = parse.urlparse(base_url)
    path = parsed.path.rstrip("/")
    qs = parse.parse_qs(parsed.query, keep_blank_values=True)
    has_query_token = "token" in qs and bool(qs["token"] and qs["token"][0])

    if path.endswith("/updates"):
        updates = base_url
        respond = parse.urlunparse(parsed._replace(path=path[:-8] + "/respond"))
    else:
        updates = base_url.rstrip("/") + "/updates"
        respond = base_url.rstrip("/") + "/respond"

    if has_query_token:
        return updates, respond
    if not token:
        raise ValueError("Missing gateway token: provide KNODS_GATEWAY_TOKEN or include token in KNODS_BASE_URL.")

    return add_token(updates, token), add_token(respond, token)


def http_json(method: str, url: str, payload: Optional[Dict] = None, timeout: int = 20) -> Dict:
    data = None
    headers = {
        "Accept": "application/json",
        "User-Agent": "openclaw-knods-bridge/1.0 (+curl-compatible)",
    }
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = request.Request(url=url, method=method.upper(), data=data, headers=headers)
    with request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body) if body else {}


def extract_text_from_result(data: Dict) -> str:
    result = data.get("result") or {}
    payloads = result.get("payloads") or []
    parts: List[str] = []

    for payload in payloads:
        if isinstance(payload, dict):
            text = str(payload.get("text") or "").strip()
            if text:
                parts.append(text)
        elif isinstance(payload, str):
            text = payload.strip()
            if text:
                parts.append(text)

    if parts:
        return "\n\n".join(parts).strip()

    direct = str(result.get("text") or "").strip()
    if direct:
        return direct

    return ""


def run_openclaw_agent(openclaw_bin: str, agent_id: str, message: str, timeout_sec: int) -> str:
    cmd = [
        openclaw_bin,
        "agent",
        "--agent",
        agent_id,
        "--message",
        message,
        "--json",
        "--timeout",
        str(timeout_sec),
    ]
    out = subprocess.check_output(cmd, text=True)
    data = json.loads(out)
    return extract_text_from_result(data)


def format_history(history: List[Dict], max_items: int = 16) -> str:
    if not history:
        return "(none)"
    lines: List[str] = []
    for item in history[-max_items:]:
        role = str(item.get("role") or "unknown").strip().lower()
        content = str(item.get("content") or "").strip()
        if not content:
            continue
        if role not in {"user", "assistant", "system"}:
            role = "user"
        lines.append(f"{role}: {content}")
    return "\n".join(lines) if lines else "(none)"


def build_knods_prompt(message: str, history: List[Dict]) -> str:
    return (
        "Channel context:\n"
        "- You are replying to a user in Knods Iris chat via the Knods polling gateway.\n"
        "- This is not OpenClaw TUI/webchat. Do not mention TUI/webchat unless the user asks.\n"
        "- If relevant, include valid [KNODS_ACTION]{...}[/KNODS_ACTION] blocks.\n\n"
        "Conversation history from Knods:\n"
        f"{format_history(history)}\n\n"
        "Current user message:\n"
        f"{message}"
    )


def respond_chunks(respond_url: str, message_id: str, text: str, chunk_size: int = 500) -> None:
    if not text:
        text = "(no response)"
    for i in range(0, len(text), chunk_size):
        delta = text[i : i + chunk_size]
        http_json("POST", respond_url, {"messageId": message_id, "delta": delta})
    http_json("POST", respond_url, {"messageId": message_id, "done": True})


def poll_once(
    updates_url: str,
    respond_url: str,
    openclaw_bin: str,
    agent_id: str,
    timeout_sec: int,
    dry_run: bool,
) -> int:
    data = http_json("GET", updates_url)
    messages: List[Dict] = data.get("messages") or []
    print(f"messages={len(messages)}")

    for msg in messages:
        message_id = msg.get("messageId")
        message = str(msg.get("message") or "")
        history = msg.get("history") or []
        if not message_id:
            continue
        print(f"handling={message_id}")
        if dry_run:
            continue
        agent_input = build_knods_prompt(message, history)
        try:
            reply = run_openclaw_agent(openclaw_bin, agent_id, agent_input, timeout_sec)
            if not reply.strip():
                print(f"empty_reply_retry={message_id}")
                reply = run_openclaw_agent(openclaw_bin, agent_id, message, timeout_sec)
        except subprocess.CalledProcessError as err:
            reply = f"Agent error: {err}"
        respond_chunks(respond_url, message_id, reply)

    return len(messages)


def main() -> int:
    parser = argparse.ArgumentParser(description="Knods polling bridge for OpenClaw agent.")
    parser.add_argument("--env-file", default=str(Path.home() / ".openclaw" / ".env"))
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--poll-interval", type=float, default=1.5)
    parser.add_argument("--openclaw-bin", default=os.getenv("OPENCLAW_BIN", "openclaw"))
    parser.add_argument("--agent-id", default=os.getenv("OPENCLAW_AGENT_ID", "iris"))
    parser.add_argument("--agent-timeout", type=int, default=90)
    args = parser.parse_args()

    load_env_file(Path(args.env_file))
    base_url = os.getenv("KNODS_BASE_URL", "").strip()
    token = os.getenv("KNODS_GATEWAY_TOKEN", "").strip() or None

    if not base_url:
        raise SystemExit("KNODS_BASE_URL is required.")

    updates_url, respond_url = resolve_urls(base_url, token)
    print(f"updates_url={updates_url}")
    print(f"respond_url={respond_url}")
    print(f"agent_id={args.agent_id}")
    print(f"dry_run={args.dry_run}")

    if args.once:
        poll_once(updates_url, respond_url, args.openclaw_bin, args.agent_id, args.agent_timeout, args.dry_run)
        return 0

    while True:
        try:
            poll_once(updates_url, respond_url, args.openclaw_bin, args.agent_id, args.agent_timeout, args.dry_run)
        except Exception as err:
            print(f"poll_error={err}")
        time.sleep(args.poll_interval)


if __name__ == "__main__":
    raise SystemExit(main())
