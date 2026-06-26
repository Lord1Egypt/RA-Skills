#!/usr/bin/env python3
"""Text chat client supporting multi-turn conversation."""

import argparse
import html
from typing import Any, Dict

from client_common import has_error, load_env_file, load_session, post_json, print_json, require_env


def text_to_html_payload(text: str) -> str:
    escaped = html.escape(text)
    return f"<p>{escaped.replace(chr(10), '<br/>')}</p>"


def send_message(
    user_id: str,
    session_id: str,
    text: str,
    stream: bool = False,
    trace_id: str = "",
) -> Dict[str, Any]:
    api_base_url = require_env("API_BASE_URL").rstrip("/")
    token = require_env("CLAWHUB_SKILL_TOKEN")

    payload: Dict[str, Any] = {
        "user_id": user_id,
        "session_id": session_id,
        "html_payload": text_to_html_payload(text),
        "stream": stream,
    }
    if trace_id:
        payload["metadata"] = {"trace_id": trace_id, "source": "clawhub_client"}

    url = f"{api_base_url}/session/message"
    return post_json(url, payload, token=token)


def run_multi_turn(user_id: str, session_id: str, stream: bool, trace_id: str) -> None:
    print("Multi-turn chat started. Type /exit to stop.")
    while True:
        text = input("You: ").strip()
        if not text:
            continue
        if text.lower() in {"/exit", "exit", "quit", "/quit"}:
            print("Chat ended.")
            break

        result = send_message(user_id, session_id, text, stream=stream, trace_id=trace_id)
        if has_error(result):
            print_json(result)
            raise SystemExit(1)
        answer = result.get("answer_text") or result.get("answer_html") or ""
        if answer:
            print(f"Bot: {answer}")
        else:
            print_json(result)


def main() -> None:
    parser = argparse.ArgumentParser(description="Send text message to skill and chat multi-turn")
    parser.add_argument("--env", default=".env", help="Path to env file, default: .env")
    parser.add_argument("--text", default="", help="Single-turn text input")
    parser.add_argument("--stream", action="store_true", help="Enable stream mode")
    parser.add_argument("--trace-id", default="")
    parser.add_argument(
        "--session-file",
        default=".session.json",
        help="Read user_id/session_id from this file, default: .session.json",
    )
    parser.add_argument("--user-id", default="", help="Optional override user id")
    parser.add_argument("--session-id", default="", help="Optional override session id")
    parser.add_argument("--multi-turn", action="store_true", help="Interactive multi-turn mode")
    args = parser.parse_args()

    load_env_file(args.env)

    session = load_session(args.session_file)
    user_id = args.user_id or session.get("user_id", "")
    session_id = args.session_id or session.get("session_id", "")

    if not user_id or not session_id:
        raise SystemExit("[ERROR] Missing user_id/session_id. Run login_client.py first or pass --user-id and --session-id.")

    if args.multi_turn or not args.text:
        run_multi_turn(user_id, session_id, args.stream, args.trace_id)
        return

    result = send_message(user_id, session_id, args.text, stream=args.stream, trace_id=args.trace_id)
    print_json(result)
    if has_error(result):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
