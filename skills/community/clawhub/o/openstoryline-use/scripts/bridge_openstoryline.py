 #!/usr/bin/env python3
from __future__ import annotations

import argparse
import asyncio
import json
import sys
from urllib.parse import urlparse, urlunparse
import urllib.request

import websockets

def http_to_ws_base(http_base: str) -> str:
    http_base = http_base.rstrip("/")
    p = urlparse(http_base)
    if p.scheme not in ("http", "https"):
        raise ValueError(f"unsupported base url scheme: {p.scheme!r}")
    ws_scheme = "wss" if p.scheme == "https" else "ws"
    return urlunparse((ws_scheme, p.netloc, "", "", "", ""))

def http_json(method: str, url: str, payload: dict | None = None, timeout: float = 30.0) -> dict:
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(
        url=url,
        data=data,
        headers=headers,
        method=method.upper(),
    )

    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()

    if not raw:
        return {}
    return json.loads(raw.decode("utf-8"))

def create_session(base_url: str, timeout: float) -> str:
    obj = http_json("POST", f"{base_url.rstrip('/')}/api/sessions", timeout=timeout)
    sid = obj.get("session_id")
    if not sid:
        raise RuntimeError(f"create session failed: {obj}")
    return str(sid)

async def chat_once(
    *,
    ws_url: str,
    prompt: str,
    lang: str | None,
    timeout: float,
) -> dict:
    payload = {"text": prompt}
    if lang:
        payload["lang"] = lang

    result = {
        "ok": False,
        "text": "",
        "interrupted": False,
    }

    async with websockets.connect(
        ws_url,
        max_size=None,
        open_timeout=timeout,
        close_timeout=10,
    ) as ws:
        await asyncio.wait_for(ws.recv(), timeout=timeout)

        req = {"type": "chat.send", "data": payload}
        await asyncio.wait_for(ws.send(json.dumps(req, ensure_ascii=False)), timeout=timeout)

        while True:
            raw = await asyncio.wait_for(ws.recv(), timeout=timeout)
            try:
                obj = json.loads(raw)
            except Exception:
                continue

            msg_type = obj.get("type")
            data = obj.get("data") or {}

            if msg_type in {
                "chat.user",
                "assistant.start",
                "assistant.delta",
                "assistant.flush",
                "tool.progress",
                "pong",
                "session.lang",
                "session.snapshot",
            }:
                continue

            if msg_type == "assistant.end":
                result["ok"] = True
                result["text"] = str(data.get("text") or "")
                result["interrupted"] = bool(data.get("interrupted", False))
                return result

            if msg_type == "error":
                result["ok"] = False
                result["error"] = str(data.get("message") or "unknown error")
                if "partial_text" in data:
                    result["partial_text"] = str(data.get("partial_text") or "")
                return result


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="OpenStoryline WS bridge.")
    p.add_argument("--base-url", default="http://127.0.0.1:8005", help="OpenStoryline base url")
    p.add_argument("--session-id", default=None, help="Existing session_id. If omitted, create one automatically.")
    p.add_argument("--prompt", default=None, help="Prompt for this turn. If omitted, read from stdin.")
    p.add_argument("--lang", default=None, choices=["zh", "en"], help="Optional language override.")
    p.add_argument("--timeout", type=float, default=1800.0, help="Overall timeout in seconds.")
    return p.parse_args()


def main() -> int:
    args = parse_args()

    prompt = args.prompt
    if prompt is None:
        prompt = sys.stdin.read().strip()

    if not prompt:
        sys.stderr.write(json.dumps({"ok": False, "error": "empty prompt"}, ensure_ascii=False) + "\n")
        return 2

    try:
        base_url = args.base_url.rstrip("/")
        session_id = args.session_id or create_session(base_url, timeout=min(args.timeout, 30.0))
        ws_base = http_to_ws_base(base_url)
        ws_url = f"{ws_base}/ws/sessions/{session_id}/chat"

        result = asyncio.run(
            chat_once(
                ws_url=ws_url,
                prompt=prompt,
                lang=args.lang,
                timeout=args.timeout,
            )
        )
        result["session_id"] = session_id

        sys.stdout.write(json.dumps(result, ensure_ascii=False) + "\n")
        return 0 if result.get("ok") else 1

    except Exception as e:
        sys.stderr.write(
            json.dumps({"ok": False, "error": f"{type(e).__name__}: {e}"}, ensure_ascii=False) + "\n"
        )
        return 1


if __name__ == "__main__":
    raise SystemExit(main())