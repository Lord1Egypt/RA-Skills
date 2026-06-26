#!/usr/bin/env python3
"""
IATerm WebSocket API Client

Standalone CLI client for interacting with IATerm's local WebSocket API.
Each command establishes an independent WebSocket connection, executes, and disconnects.

Connection flow:
  - Session ID from IATERM_SESSION_ID env var (required)
  - First connection: identify(session_id) → IATerm UI approval → ws_token → cached
  - Subsequent connections: identify(session_id + cached token) → server recognizes → skip approval
  - Token invalidated: auto-clear cache, re-prompt approval

Usage:
    python ws_client.py list_workspaces
    python ws_client.py list_panels
    python ws_client.py list_panels --workspace-id <id>
    python ws_client.py list_displays --workspace-id <id>
    python ws_client.py list_connections
    python ws_client.py list_connections --type ssh
    python ws_client.py get_panel_info --panel-id <id>
    python ws_client.py send_input --connection-id <id> --data "ls -la\\n"
    python ws_client.py subscribe_output --connection-id <id>
    python ws_client.py interactive
"""

import asyncio
import json
import sys
import uuid
import argparse
import os
import time

try:
    import websockets
except ImportError:
    print("Error: 'websockets' package required. Install with: pip install websockets", file=sys.stderr)
    sys.exit(1)


# ─── Configuration ───────────────────────────────────────────────────────────

_cache_home = os.environ.get("XDG_CACHE_HOME", os.path.join(os.path.expanduser("~"), ".cache"))
_state_dir = os.path.join(_cache_home, "iaterm-ws-client")
_token_file = os.path.join(_state_dir, "ws_token.json")
_approval_file = os.path.join(_state_dir, "approval.json")


def get_ws_url():
    """Build the WebSocket URL."""
    port = os.environ.get("IATERM_WS_PORT", "19790")
    return f"ws://127.0.0.1:{port}/ws"


def _ensure_dirs():
    os.makedirs(_state_dir, exist_ok=True)


def _get_session_id():
    """Get session ID from IATERM_SESSION_ID environment variable."""
    sid = os.environ.get("IATERM_SESSION_ID")
    if not sid:
        print("Error: IATERM_SESSION_ID environment variable is not set.", file=sys.stderr)
        print("This variable should be set by the host application (e.g. IATerm).", file=sys.stderr)
        sys.exit(1)
    return sid


def _log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, file=sys.stderr, flush=True)


# ─── Token cache ─────────────────────────────────────────────────────────────

def _load_cached_token(session_id):
    """Load cached WS token for this session_id. Returns token string or None."""
    try:
        with open(_token_file, "r") as f:
            data = json.load(f)
        if data.get("session_id") == session_id:
            return data.get("token")
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        pass
    return None


def _save_cached_token(session_id, token):
    """Save WS token to cache file (permissions 0600)."""
    _ensure_dirs()
    data = {"session_id": session_id, "token": token}
    fd = os.open(_token_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(data, f)


def _clear_cached_token():
    """Remove cached token file."""
    try:
        os.unlink(_token_file)
    except FileNotFoundError:
        pass


# ─── Approval ────────────────────────────────────────────────────────────────

def _load_approvals():
    """Load the approval whitelist."""
    try:
        with open(_approval_file, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def _save_approvals(approvals):
    """Save the approval whitelist."""
    _ensure_dirs()
    fd = os.open(_approval_file, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w") as f:
        json.dump(approvals, f, indent=2)


def _check_approval(method, params, auto_approve=False):
    """Check if an operation needs approval. Returns True if approved, False if rejected."""
    # Only gate sensitive operations
    if method not in ("send_input", "subscribe_output"):
        return True

    if auto_approve:
        return True

    # Check persistent approvals
    approvals = _load_approvals()
    approval_key = method
    if method == "send_input":
        conn_id = params.get("connection_id", "")
        approval_key = f"send_input:{conn_id}"
    elif method == "subscribe_output":
        conn_id = params.get("connection_id", "")
        approval_key = f"subscribe_output:{conn_id}"

    if approvals.get(approval_key) == "always":
        return True

    # Interactive confirmation
    desc = method
    if method == "send_input":
        data_preview = params.get("data", "")
        if len(data_preview) > 80:
            data_preview = data_preview[:77] + "..."
        desc = f"send_input to {params.get('connection_id', '?')}: {repr(data_preview)}"
    elif method == "subscribe_output":
        desc = f"subscribe_output on {params.get('connection_id', '?')}"

    print(f"\n[Approval] {desc}", file=sys.stderr)
    print("  y = approve this time  |  n = reject  |  a = always approve for this target", file=sys.stderr)
    try:
        choice = input("  [y/n/a]: ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("", file=sys.stderr)
        return False

    if choice == "a":
        approvals[approval_key] = "always"
        _save_approvals(approvals)
        return True
    elif choice == "y":
        return True
    else:
        return False


# ─── WebSocket connection ────────────────────────────────────────────────────

async def _connect_and_identify(session_id, client_type="ws-client", client_id=None):
    """
    Connect to IATerm WS, send identify, handle approval.
    Returns (ws, token) on success.
    Raises SystemExit on failure.
    """
    url = get_ws_url()
    cached_token = _load_cached_token(session_id)

    try:
        ws = await websockets.connect(url)
    except (ConnectionRefusedError, OSError) as e:
        print(f"Cannot connect to IATerm at {url}: {e}", file=sys.stderr)
        print("Ensure IATerm is running.", file=sys.stderr)
        sys.exit(1)

    # Send identify with session_id and optional cached token
    identify_msg = {
        "type": "identify",
        "client_type": client_type,
        "client_id": client_id or f"agent-{os.getpid()}",
        "session_id": session_id,
    }
    if cached_token:
        identify_msg["token"] = cached_token

    await ws.send(json.dumps(identify_msg))

    # Wait for approval response
    if not cached_token:
        _log("Waiting for connection approval in IATerm...")

    try:
        raw = await asyncio.wait_for(ws.recv(), timeout=65)
    except asyncio.TimeoutError:
        _log("Approval timeout (65s)")
        await ws.close()
        sys.exit(1)
    except websockets.exceptions.ConnectionClosed:
        _log("Connection closed during approval")
        sys.exit(1)

    data = json.loads(raw)

    if "event" in data:
        if data["event"] == "connected":
            token = data.get("data", {}).get("token")
            sid = data.get("data", {}).get("session_id", session_id)
            if token:
                _save_cached_token(session_id, token)
            _log(f"Connected (session: {sid})")
            return ws, token

        elif data["event"] == "connection_rejected":
            msg = data.get("data", {}).get("message", "rejected")
            # Token might be stale — clear cache and retry once
            if cached_token:
                _log(f"Connection rejected (cached token may be stale): {msg}")
                _clear_cached_token()
                await ws.close()
                return await _connect_and_identify(session_id, client_type, client_id)
            _log(f"Connection rejected: {msg}")
            await ws.close()
            sys.exit(1)

    if "error" in data:
        err_code = data["error"].get("code")
        err_msg = data["error"].get("message", "")
        # Auth failure with cached token — clear and retry
        if cached_token and err_code == -15:
            _log(f"Token expired: {err_msg}")
            _clear_cached_token()
            await ws.close()
            return await _connect_and_identify(session_id, client_type, client_id)
        _log(f"Connection error: {err_msg}")
        await ws.close()
        sys.exit(1)

    _log(f"Unexpected response: {json.dumps(data)}")
    await ws.close()
    sys.exit(1)


async def _ws_request(ws, method, params=None, token=None):
    """Send a request on a WS and wait for the response."""
    req_id = str(uuid.uuid4())[:8]
    msg = {"id": req_id, "method": method, "params": params or {}}
    if token:
        msg["token"] = token
    await ws.send(json.dumps(msg))
    while True:
        raw = await ws.recv()
        data = json.loads(raw)
        if "event" in data:
            continue
        if data.get("id") == req_id:
            return data


# ─── CLI command execution ───────────────────────────────────────────────────

def print_result(data):
    """Pretty-print a response."""
    if "error" in data:
        print(f"Error ({data['error']['code']}): {data['error']['message']}", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(data.get("result", data), ensure_ascii=False, indent=2))


async def cmd_execute(method, params=None, auto_approve=False, client_type="ws-client", client_id=None):
    """Execute a single command: connect, request, disconnect."""
    session_id = _get_session_id()
    params = params or {}

    # Check approval for sensitive operations
    if not _check_approval(method, params, auto_approve=auto_approve):
        print("Operation rejected by user.", file=sys.stderr)
        sys.exit(1)

    ws, token = await _connect_and_identify(session_id, client_type, client_id)
    try:
        result = await _ws_request(ws, method, params, token=token)
        print_result(result)
    finally:
        await ws.close()


async def cmd_subscribe(connection_id, auto_approve=False, client_type="ws-client", client_id=None):
    """Subscribe to terminal output."""
    session_id = _get_session_id()
    params = {"connection_id": connection_id}

    if not _check_approval("subscribe_output", params, auto_approve=auto_approve):
        print("Operation rejected by user.", file=sys.stderr)
        sys.exit(1)

    ws, token = await _connect_and_identify(session_id, client_type, client_id)
    try:
        result = await _ws_request(ws, "subscribe_output", params, token=token)
        if "error" in result:
            print_result(result)
            return

        print(f"Subscribed to {connection_id}. Press Ctrl-C to stop.", file=sys.stderr)
        try:
            while True:
                raw = await ws.recv()
                data = json.loads(raw)
                if "event" in data and data["event"] == "terminal_output":
                    sys.stdout.write(data["data"].get("output", ""))
                    sys.stdout.flush()
                elif "event" in data and data["event"] == "disconnected":
                    print("\nServer disconnected.", file=sys.stderr)
                    break
        except (KeyboardInterrupt, asyncio.CancelledError):
            await _ws_request(ws, "unsubscribe_output", {"connection_id": connection_id}, token=token)
            print("\nUnsubscribed.", file=sys.stderr)
    finally:
        await ws.close()


async def cmd_interactive(client_type="ws-client", client_id=None):
    """Interactive mode."""
    session_id = _get_session_id()
    ws, token = await _connect_and_identify(session_id, client_type, client_id)
    try:
        print("Connected. Type JSON requests or use shortcuts:", file=sys.stderr)
        print("  lw = list_workspaces | lp = list_panels | lc = list_connections", file=sys.stderr)
        print("  q = quit", file=sys.stderr)

        shortcuts = {
            "lw": ("list_workspaces", {}),
            "lp": ("list_panels", {}),
            "lc": ("list_connections", {}),
        }

        async def reader():
            try:
                while True:
                    raw = await ws.recv()
                    data = json.loads(raw)
                    if "event" in data:
                        print(f"\n[EVENT] {json.dumps(data, ensure_ascii=False)}")
                    else:
                        print(f"\n[RESP] {json.dumps(data, ensure_ascii=False, indent=2)}")
                    print("> ", end="", flush=True)
            except websockets.exceptions.ConnectionClosed:
                pass

        reader_task = asyncio.create_task(reader())
        loop = asyncio.get_event_loop()
        try:
            while True:
                print("> ", end="", flush=True)
                line = await loop.run_in_executor(None, sys.stdin.readline)
                line = line.strip()
                if not line:
                    continue
                if line == "q":
                    break

                if line in shortcuts:
                    method, params = shortcuts[line]
                    req_id = str(uuid.uuid4())[:8]
                    msg = {"id": req_id, "method": method, "params": params, "token": token}
                else:
                    try:
                        msg = json.loads(line)
                        if "id" not in msg:
                            msg["id"] = str(uuid.uuid4())[:8]
                        if "token" not in msg:
                            msg["token"] = token
                    except json.JSONDecodeError:
                        print("Invalid JSON. Use shortcuts (lw/lp/lc) or full JSON.", file=sys.stderr)
                        continue
                await ws.send(json.dumps(msg))
        except (KeyboardInterrupt, EOFError):
            pass
        finally:
            reader_task.cancel()
            print("\nDisconnected.", file=sys.stderr)
    finally:
        await ws.close()


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="IATerm WebSocket API Client")
    parser.add_argument("--auto-approve", action="store_true",
                        help="Skip interactive approval for send_input/subscribe_output")
    parser.add_argument("--client-type", default=None, help="Client type identifier (e.g. claude-code, gemini)")
    parser.add_argument("--client-id", default=None, help="Client instance identifier")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list_workspaces", help="List all workspaces")

    p_ld = sub.add_parser("list_displays", help="List displays for a workspace")
    p_ld.add_argument("--workspace-id", required=True)

    p_lp = sub.add_parser("list_panels", help="List panels")
    p_lp.add_argument("--workspace-id", default=None)

    p_pi = sub.add_parser("get_panel_info", help="Get panel details")
    p_pi.add_argument("--panel-id", required=True)

    p_lc = sub.add_parser("list_connections", help="List active connections")
    p_lc.add_argument("--type", default=None, dest="conn_type")

    p_si = sub.add_parser("send_input", help="Send input to terminal")
    p_si.add_argument("--connection-id", required=True)
    p_si.add_argument("--data", required=True, help="Text to send (supports \\n, \\t escapes)")

    p_so = sub.add_parser("subscribe_output", help="Subscribe to terminal output")
    p_so.add_argument("--connection-id", required=True)

    sub.add_parser("interactive", help="Interactive mode")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    ct = args.client_type
    ci = args.client_id
    aa = args.auto_approve

    if args.command == "list_workspaces":
        asyncio.run(cmd_execute("list_workspaces", auto_approve=aa, client_type=ct, client_id=ci))
    elif args.command == "list_displays":
        asyncio.run(cmd_execute("list_displays", {"workspace_id": args.workspace_id}, auto_approve=aa, client_type=ct, client_id=ci))
    elif args.command == "list_panels":
        params = {}
        if args.workspace_id:
            params["workspace_id"] = args.workspace_id
        asyncio.run(cmd_execute("list_panels", params, auto_approve=aa, client_type=ct, client_id=ci))
    elif args.command == "get_panel_info":
        asyncio.run(cmd_execute("get_panel_info", {"panel_id": args.panel_id}, auto_approve=aa, client_type=ct, client_id=ci))
    elif args.command == "list_connections":
        params = {}
        if args.conn_type:
            params["type"] = args.conn_type
        asyncio.run(cmd_execute("list_connections", params, auto_approve=aa, client_type=ct, client_id=ci))
    elif args.command == "send_input":
        data = args.data.replace("\\n", "\n").replace("\\t", "\t").replace("\\r", "\r")
        asyncio.run(cmd_execute("send_input", {"connection_id": args.connection_id, "data": data}, auto_approve=aa, client_type=ct, client_id=ci))
    elif args.command == "subscribe_output":
        asyncio.run(cmd_subscribe(args.connection_id, auto_approve=aa, client_type=ct, client_id=ci))
    elif args.command == "interactive":
        asyncio.run(cmd_interactive(client_type=ct, client_id=ci))


if __name__ == "__main__":
    main()
