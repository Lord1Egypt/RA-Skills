#!/usr/bin/env python3
"""PPIO Sandbox CLI — secure remote execution for OpenClaw.

Run untrusted code in isolated PPIO cloud sandboxes (Firecracker microVMs)
and create browser sandboxes for OpenClaw's native browser tool.

Templates:
    browser-chromium    Browser sandbox (Chromium + CDP on port 9223)
    code-interpreter-v1 Code interpreter (Python, Node.js, shell)

Lifecycle:
    - Sandboxes have a timeout. On timeout with auto_pause (default):
      sandbox pauses and resumes automatically on next connect().
    - All process state (including Chromium) is preserved across pause/resume.
    - Use 'list' to find existing sandboxes before creating new ones.

Environment:
    PPIO_API_KEY / E2B_API_KEY    Required. PPIO API key.
    E2B_DOMAIN                    Sandbox domain (default: sandbox.ppio.cn).
"""

import argparse
import json
import sys
import os

from ppio_sandbox.code_interpreter import Sandbox
from ppio_sandbox.core.sandbox.sandbox_api import SandboxQuery

BROWSER_TEMPLATE = "browser-chromium"
SANDBOX_APP_LABEL = "openclaw-sandbox"
SANDBOX_METADATA = {"app": SANDBOX_APP_LABEL}

# Truncate output to protect agent context window.
MAX_OUTPUT_CHARS = 8000


def json_out(data):
    """Print JSON to stdout. All output goes through this."""
    print(json.dumps(data, ensure_ascii=False))


def json_err(message, **extra):
    """Print JSON error to stdout (not stderr — some frameworks treat stderr as failure)."""
    json_out({"status": "error", "message": message, **extra})
    sys.exit(1)


def truncate(text, limit=MAX_OUTPUT_CHARS):
    """Truncate text to limit, preserving the tail (most recent output)."""
    if not text or len(text) <= limit:
        return text
    return f"[...truncated {len(text) - limit} chars...]\n" + text[-limit:]


def get_api_key():
    key = os.environ.get("PPIO_API_KEY") or os.environ.get("E2B_API_KEY", "")
    if not key:
        json_err("PPIO_API_KEY or E2B_API_KEY environment variable is required.")
    return key


def connect(sandbox_id):
    """Connect to a sandbox. Automatically resumes if paused."""
    api_key = get_api_key()
    try:
        return Sandbox.connect(sandbox_id, api_key=api_key)
    except Exception as e:
        err_msg = str(e).lower()
        if "not found" in err_msg or "404" in err_msg:
            json_err(
                f"Sandbox {sandbox_id} not found. It may have been deleted (timeout without auto_pause). Use 'create' to start a new one.",
                sandbox_id=sandbox_id,
            )
        else:
            json_err(f"Failed to connect to sandbox {sandbox_id}: {e}", sandbox_id=sandbox_id)


# ── Commands ──────────────────────────────────────────────────────────────────


def cmd_create(args):
    api_key = get_api_key()
    # PPIO SDK 1.0.5's public create() hardcodes auto_pause=False.
    # Call _create() directly to enable auto_pause.
    sbx = Sandbox._create(
        template=args.template,
        timeout=args.timeout,
        metadata=SANDBOX_METADATA,
        envs=None,
        secure=False,
        allow_internet_access=True,
        auto_pause=True,
        api_key=api_key,
    )
    result = {
        "status": "ok",
        "sandbox_id": sbx.sandbox_id,
        "template": args.template,
        "timeout": args.timeout,
        "auto_pause": True,
    }
    if args.template == BROWSER_TEMPLATE:
        host = sbx.get_host(9223)
        cdp_url = f"https://{host}"
        result["cdp_url"] = cdp_url
        result["usage"] = (
            "Configure OpenClaw browser to use this sandbox: "
            f'set browser.profiles.sandbox.cdpUrl to "{cdp_url}" in openclaw.json, '
            "then use the browser tool with profile 'sandbox'."
        )
    json_out(result)


def cmd_exec(args):
    sbx = connect(args.sandbox_id)
    try:
        result = sbx.commands.run(args.command, timeout=args.timeout)
        if hasattr(result, "stdout"):
            json_out({
                "status": "ok",
                "stdout": truncate(result.stdout or ""),
                "stderr": truncate(result.stderr or ""),
                "exit_code": getattr(result, "exit_code", 0),
            })
        else:
            json_out({"status": "ok", "stdout": truncate(str(result) if result else "")})
    except Exception as e:
        json_err(f"Command failed: {e}", sandbox_id=args.sandbox_id)


def cmd_read(args):
    sbx = connect(args.sandbox_id)
    try:
        content = sbx.files.read(args.path)
        json_out({"status": "ok", "path": args.path, "data": truncate(content or "")})
    except Exception as e:
        json_err(f"Failed to read {args.path}: {e}", sandbox_id=args.sandbox_id)


def cmd_write(args):
    sbx = connect(args.sandbox_id)
    content = sys.stdin.read() if args.stdin else args.content
    if content is None:
        json_err("No content provided. Use --stdin or pass content as argument.")
    try:
        sbx.files.write(args.path, content)
        json_out({"status": "ok", "path": args.path, "bytes": len(content)})
    except Exception as e:
        json_err(f"Failed to write {args.path}: {e}", sandbox_id=args.sandbox_id)


def cmd_upload(args):
    sbx = connect(args.sandbox_id)
    try:
        with open(args.local_path, "rb") as f:
            sbx.files.write(args.sandbox_path, f)
        json_out({"status": "ok", "from": args.local_path, "to": args.sandbox_path})
    except FileNotFoundError:
        json_err(f"Local file not found: {args.local_path}")
    except Exception as e:
        json_err(f"Upload failed: {e}", sandbox_id=args.sandbox_id)


def cmd_download(args):
    sbx = connect(args.sandbox_id)
    try:
        content = sbx.files.read(args.sandbox_path)
        if content is None:
            json_err(f"File not found in sandbox: {args.sandbox_path}", sandbox_id=args.sandbox_id)
        if isinstance(content, bytes):
            with open(args.local_path, "wb") as f:
                f.write(content)
        else:
            with open(args.local_path, "w") as f:
                f.write(content)
        json_out({"status": "ok", "from": args.sandbox_path, "to": args.local_path})
    except Exception as e:
        json_err(f"Download failed: {e}", sandbox_id=args.sandbox_id)


def cmd_status(args):
    sbx = connect(args.sandbox_id)
    try:
        result = sbx.commands.run("echo ok", timeout=5)
        ok = bool(result.stdout.strip() == "ok") if hasattr(result, "stdout") else bool(result)
        json_out({"status": "ok", "sandbox_id": args.sandbox_id, "sandbox_status": "running" if ok else "unknown"})
    except Exception:
        json_out({"status": "ok", "sandbox_id": args.sandbox_id, "sandbox_status": "unreachable"})


def cmd_list(args):
    api_key = get_api_key()
    query = SandboxQuery(metadata=SANDBOX_METADATA)
    paginator = Sandbox.list(query=query, api_key=api_key)
    sandboxes = []
    while paginator.has_next:
        for s in paginator.next_items():
            sandboxes.append({
                "sandbox_id": s.sandbox_id,
                "template_id": getattr(s, "template_id", ""),
                "started_at": str(getattr(s, "started_at", "")),
                "status": getattr(s, "status", "unknown"),
            })
    json_out({"status": "ok", "sandboxes": sandboxes, "count": len(sandboxes)})


def cmd_kill(args):
    sbx = connect(args.sandbox_id)
    try:
        sbx.kill()
        json_out({"status": "ok", "sandbox_id": args.sandbox_id, "sandbox_status": "killed"})
    except Exception as e:
        json_err(f"Failed to kill sandbox: {e}", sandbox_id=args.sandbox_id)


# ── CLI ───────────────────────────────────────────────────────────────────────


def build_parser():
    parser = argparse.ArgumentParser(
        prog="sandbox.py",
        description="PPIO Sandbox CLI — secure remote execution for OpenClaw.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # create
    p = sub.add_parser("create", help="Create a new sandbox")
    p.add_argument("--template", required=True, help="Sandbox template: browser-chromium or code-interpreter-v1")
    p.add_argument("--timeout", type=int, required=True, help="Timeout in seconds (estimate based on task)")
    p.set_defaults(func=cmd_create)

    # exec
    p = sub.add_parser("exec", help="Execute a shell command in sandbox")
    p.add_argument("sandbox_id", help="Sandbox ID")
    p.add_argument("command", help="Shell command to run")
    p.add_argument("--timeout", type=int, default=30, help="Command timeout in seconds (default: 30)")
    p.set_defaults(func=cmd_exec)

    # read
    p = sub.add_parser("read", help="Read a file from sandbox")
    p.add_argument("sandbox_id", help="Sandbox ID")
    p.add_argument("path", help="File path inside sandbox")
    p.set_defaults(func=cmd_read)

    # write
    p = sub.add_parser("write", help="Write content to a file in sandbox")
    p.add_argument("sandbox_id", help="Sandbox ID")
    p.add_argument("path", help="File path inside sandbox")
    p.add_argument("content", nargs="?", default=None, help="Content to write (omit and use --stdin for multi-line)")
    p.add_argument("--stdin", action="store_true", help="Read content from stdin")
    p.set_defaults(func=cmd_write)

    # upload
    p = sub.add_parser("upload", help="Upload a local file to sandbox")
    p.add_argument("sandbox_id", help="Sandbox ID")
    p.add_argument("local_path", help="Local file path")
    p.add_argument("sandbox_path", help="Destination path in sandbox")
    p.set_defaults(func=cmd_upload)

    # download
    p = sub.add_parser("download", help="Download a file from sandbox to local")
    p.add_argument("sandbox_id", help="Sandbox ID")
    p.add_argument("sandbox_path", help="File path in sandbox")
    p.add_argument("local_path", help="Local destination path")
    p.set_defaults(func=cmd_download)

    # status
    p = sub.add_parser("status", help="Check if sandbox is alive")
    p.add_argument("sandbox_id", help="Sandbox ID")
    p.set_defaults(func=cmd_status)

    # list
    p = sub.add_parser("list", help="List all sandbox instances")
    p.set_defaults(func=cmd_list)

    # kill
    p = sub.add_parser("kill", help="Destroy a sandbox")
    p.add_argument("sandbox_id", help="Sandbox ID")
    p.set_defaults(func=cmd_kill)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
