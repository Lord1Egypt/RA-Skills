#!/usr/bin/env python3
"""
Send a message via LCP/1.1 daemon (IPC).
Falls back to direct UDP if daemon is not running.

Usage:
    python3 lcp_send.py "Hello!"
    python3 lcp_send.py --type task "Please do X"
    python3 lcp_send.py --type pong --reply-to msg_id "pong"
"""

import sys
import os
import json
import socket

IPC_SOCKET = "/tmp/lcp.sock"

def send_via_ipc(message, msg_type="chat", reply_to=None):
    """Send message through running LCP daemon."""
    payload = {
        "type": msg_type,
        "message": message,
    }
    if reply_to:
        payload["replyTo"] = reply_to

    req = json.dumps({"cmd": "SEND", "payload": payload}, ensure_ascii=False)

    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(15.0)
    try:
        sock.connect(IPC_SOCKET)
        sock.sendall(req.encode('utf-8'))
        raw = sock.recv(65536)
        resp = json.loads(raw.decode('utf-8'))
        return resp
    except ConnectionRefusedError:
        return {"error": "Daemon not running. Start with: python3 lcp_node.py"}
    except FileNotFoundError:
        return {"error": "Daemon not running (no IPC socket). Start with: python3 lcp_node.py"}
    finally:
        sock.close()

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="Send LCP/1.1 message")
    p.add_argument("message", nargs="?", default="ping")
    p.add_argument("--type", default="chat", help="Message type: chat|task|result|ping|pong")
    p.add_argument("--reply-to", default=None, help="Reply to message ID")
    args = p.parse_args()

    resp = send_via_ipc(args.message, args.type, args.reply_to)
    print(json.dumps(resp, ensure_ascii=False, indent=2))

    if resp.get("ok"):
        print(f"✅ Sent [{args.type}]: {args.message[:80]}")
    elif "error" in resp:
        print(f"❌ {resp['error']}", file=sys.stderr)
        sys.exit(1)
    else:
        print(f"⚠️ Send failed (no ACK from peer)", file=sys.stderr)
        sys.exit(1)
