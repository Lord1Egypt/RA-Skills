#!/usr/bin/env python3
"""
examples/acp_demo.py — End-to-end demo of the OpenCode ACP workflow.

What this script does:
    1. Spawns `opencode acp` as a subprocess (stdio JSON-RPC 2.0 transport).
    2. Sends an `initialize` request using this skill's own clientInfo.
    3. Sends a `session/new` request and captures the returned sessionId.
    4. Sends a single `session/prompt` request with a tiny code task.
    5. Streams all session/update notifications until the prompt completes.
    6. Gracefully shuts the subprocess down.

Usage:
    python3 examples/acp_demo.py                       # full run, real OpenCode
    python3 examples/acp_demo.py --dry-run             # print the JSON-RPC frames without spawning
    python3 examples/acp_demo.py --no-prompt           # stop after session/new (no LLM call)
    python3 examples/acp_demo.py --cwd /path/to/proj   # opencode starts in that directory
    python3 examples/acp_demo.py --prompt "list files" # custom prompt

Notes:
    The default flow sends a `session/prompt`, which requires a configured LLM
    provider (`opencode providers list` should show at least one credential).
    If no provider is configured, run with `--no-prompt` to verify the ACP
    handshake (`initialize` + `session/new`) without invoking the model.

Requirements:
    - opencode >= 1.1.0 available on $PATH
    - Python 3.8+ (uses subprocess, json, argparse from stdlib only)
    - No third-party dependencies

Exit codes:
    0  success
    1  opencode binary not found
    2  initialize failed
    3  session/new failed
    4  session/prompt failed or returned an error
    5  unexpected subprocess exit
"""
from __future__ import annotations

import argparse
import json
import os
import select
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

PROTOCOL_VERSION = 1
CLIENT_INFO = {
    "name": "opencode-acp-control",
    "title": "OpenCode ACP Control",
    "version": "0.3.0",
}
CLIENT_CAPABILITIES = {
    "fs": {"readTextFile": True, "writeTextFile": True},
    "terminal": True,
}


def frame(request: dict[str, Any]) -> bytes:
    """Serialize a JSON-RPC request as newline-delimited JSON.

    OpenCode's ACP transport uses nd-JSON (one JSON object per line) on stdio,
    not the LSP `Content-Length` framing.
    """
    return (json.dumps(request) + "\n").encode("utf-8")


def read_frame(stream, timeout: float = 0.0) -> dict[str, Any] | None:
    """Read one newline-delimited JSON-RPC message from stdin.

    If timeout > 0, waits for readability before reading.
    Returns None on EOF.
    """
    if timeout > 0:
        ready, _, _ = select.select([stream], [], [], timeout)
        if not ready:
            raise TimeoutError("timed out waiting for data from opencode")
    line = stream.readline()
    if not line:
        return None
    line = line.strip()
    if not line:
        return None
    try:
        return json.loads(line.decode("utf-8"))
    except json.JSONDecodeError as exc:
        print(f"[demo] malformed JSON from opencode: {exc} line={line!r}", file=sys.stderr)
        return None


def send_request(proc, method: str, params: Any, msg_id: int) -> int:
    """Send a JSON-RPC request framed for the ACP transport. Returns the id used."""
    payload = {"jsonrpc": "2.0", "id": msg_id, "method": method, "params": params}
    proc.stdin.write(frame(payload))
    proc.stdin.flush()
    return msg_id


def wait_for_id(stream, target_id: int, *, timeout: float = 30.0) -> dict[str, Any]:
    """Drain notifications until we see the response for `target_id` or time out."""
    deadline = time.time() + timeout
    while True:
        remaining = deadline - time.time()
        if remaining <= 0:
            raise TimeoutError(f"timed out waiting for response id={target_id}")
        msg = read_frame(stream, timeout=max(0.1, remaining))
        if msg is None:
            raise EOFError("opencode closed stdio before responding")
        if "id" in msg and msg["id"] == target_id:
            return msg
        # Notifications (no "id" key) are ignored here; session/update is handled
        # separately by stream_session_updates().
        if "method" in msg and msg["method"] != "session/update":
            print(f"[demo] notification: {msg['method']}")


def stream_session_updates(stream, proc, until_id: int, *, timeout: float = 60.0) -> dict[str, Any] | None:
    """Print session/update notifications and handles permission requests until the prompt response arrives.

    Returns the matching response frame, or None.
    """
    deadline = time.time() + timeout
    text_chunks: list[str] = []
    while True:
        remaining = deadline - time.time()
        if remaining <= 0:
            print("[demo] warning: session/prompt timed out", file=sys.stderr)
            return None
        try:
            msg = read_frame(stream, timeout=max(0.1, remaining))
        except TimeoutError:
            continue
        if msg is None:
            return None
        if msg.get("id") == until_id:
            return msg
        
        # Handle Server-to-Client Requests (e.g., requestPermission)
        if "method" in msg and "id" in msg:
            if msg["method"] == "requestPermission":
                params = msg.get("params", {})
                tool_call = params.get("toolCall", {})
                title = tool_call.get("title", "unknown")
                print(f"[demo] server request: requestPermission for '{title}' (id={msg['id']})")
                
                # Auto-approve permission request to prevent deadlocks
                reply = {
                    "jsonrpc": "2.0",
                    "id": msg["id"],
                    "result": {"reply": "once"}
                }
                proc.stdin.write(frame(reply))
                proc.stdin.flush()
                print(f"[demo] auto-approved permission request id={msg['id']}")
            continue

        if msg.get("method") == "session/update":
            params = msg.get("params", {}) or {}
            update = params.get("update", {}) or {}
            kind = update.get("sessionUpdate") or update.get("type") or "update"
            content = update.get("content") or update.get("message") or ""
            if isinstance(content, dict):
                content = content.get("text", "")
            if kind == "agent_message_chunk" and content:
                text_chunks.append(str(content))
            print(f"[session] {kind}: {str(content)[:160]}")
            continue
        if "method" in msg:
            print(f"[demo] notification: {msg['method']}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--cwd", default=os.getcwd(), help="working directory for opencode (default: current dir)")
    parser.add_argument("--prompt", default="List the files in the current directory and print their names.",
                        help="prompt text to send via session/prompt")
    parser.add_argument("--dry-run", action="store_true", help="print JSON-RPC frames without spawning opencode")
    parser.add_argument("--timeout", type=float, default=60.0, help="seconds to wait for the prompt to finish")
    parser.add_argument("--no-prompt", action="store_true",
                        help="stop after session/new (skips the LLM call, useful when no provider is configured)")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.dry_run:
        print("=== initialize ===")
        print(json.dumps({"jsonrpc": "2.0", "id": 0, "method": "initialize",
                          "params": {"protocolVersion": PROTOCOL_VERSION,
                                     "clientCapabilities": CLIENT_CAPABILITIES,
                                     "clientInfo": CLIENT_INFO}}, indent=2))
        print("=== session/new ===")
        print(json.dumps({"jsonrpc": "2.0", "id": 1, "method": "session/new", "params": {"cwd": args.cwd, "mcpServers": []}}, indent=2))
        print("=== session/prompt ===")
        print(json.dumps({"jsonrpc": "2.0", "id": 2, "method": "session/prompt",
                          "params": {"sessionId": "<from session/new>", "prompt": [{"type": "text", "text": args.prompt}]}}, indent=2))
        return 0

    opencode_bin = shutil.which("opencode")
    if opencode_bin is None:
        print("[demo] opencode binary not found on $PATH", file=sys.stderr)
        print("[demo] install it from https://opencode.ai or pass --dry-run", file=sys.stderr)
        return 1

    cwd = Path(args.cwd).expanduser().resolve()
    if not cwd.is_dir():
        print(f"[demo] --cwd is not a directory: {cwd}", file=sys.stderr)
        return 1

    print(f"[demo] spawning: {opencode_bin} acp (cwd={cwd})")
    proc = subprocess.Popen(
        [opencode_bin, "acp"],
        cwd=str(cwd),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=sys.stderr,  # Redirect to sys.stderr to avoid deadlock
        text=False,
        bufsize=0,
    )
    assert proc.stdin and proc.stdout

    try:
        # 1. initialize
        send_request(proc, "initialize",
                     {"protocolVersion": PROTOCOL_VERSION,
                      "clientCapabilities": CLIENT_CAPABILITIES,
                      "clientInfo": CLIENT_INFO}, msg_id=0)
        init_resp = wait_for_id(proc.stdout, 0, timeout=15.0)
        if "error" in init_resp:
            print(f"[demo] initialize error: {init_resp['error']}", file=sys.stderr)
            return 2
        server_info = (init_resp.get("result") or {}).get("serverInfo") or {}
        print(f"[demo] initialized: serverInfo={server_info}")

        # 2. session/new
        send_request(proc, "session/new", {"cwd": str(cwd), "mcpServers": []}, msg_id=1)
        new_resp = wait_for_id(proc.stdout, 1, timeout=15.0)
        if "error" in new_resp:
            print(f"[demo] session/new error: {new_resp['error']}", file=sys.stderr)
            return 3
        session_id = (new_resp.get("result") or {}).get("sessionId")
        if not session_id:
            print("[demo] session/new response missing sessionId", file=sys.stderr)
            return 3
        print(f"[demo] sessionId={session_id}")

        if args.no_prompt:
            print("[demo] --no-prompt set, skipping session/prompt (no LLM call required)")
            return 0

        # 3. session/prompt
        send_request(proc, "session/prompt",
                     {"sessionId": session_id,
                      "prompt": [{"type": "text", "text": args.prompt}]}, msg_id=2)
        prompt_resp = stream_session_updates(proc.stdout, proc, until_id=2, timeout=args.timeout)
        if prompt_resp is None:
            print("[demo] session/prompt response not received or timed out", file=sys.stderr)
            return 4
        if "error" in prompt_resp:
            print(f"[demo] session/prompt error: {prompt_resp['error']}", file=sys.stderr)
            return 4
        result = prompt_resp.get("result") or {}
        print(f"[demo] session/prompt completed: stopReason={result.get('stopReason')}")
        return 0
    except (TimeoutError, EOFError) as exc:
        print(f"[demo] protocol error: {exc}", file=sys.stderr)
        return 5
    finally:
        if proc.poll() is None:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


if __name__ == "__main__":
    sys.exit(main())
