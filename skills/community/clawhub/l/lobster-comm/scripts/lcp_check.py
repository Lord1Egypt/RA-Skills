#!/usr/bin/env python3
"""
Check inbox via LCP/1.1 daemon (IPC).
Replaces check_and_notify.py for UDP mode.

Usage:
    python3 lcp_check.py           # JSON output
    python3 lcp_check.py --pretty  # Human-readable
"""

import sys
import os
import json
import socket
import glob

IPC_SOCKET = "/tmp/lcp.sock"

# Fallback: direct file read if daemon is not running
SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INBOX_DIR = os.path.join(SKILL_DIR, "data", "inbox")

def check_via_ipc():
    """Query daemon for inbox messages."""
    req = json.dumps({"cmd": "CHECK"})
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(10.0)
    try:
        sock.connect(IPC_SOCKET)
        sock.sendall(req.encode('utf-8'))
        raw = sock.recv(1048576)
        return json.loads(raw.decode('utf-8'))
    except (ConnectionRefusedError, FileNotFoundError):
        return None
    finally:
        sock.close()

def check_direct():
    """Fallback: read inbox files directly."""
    messages = []
    for fp in sorted(glob.glob(os.path.join(INBOX_DIR, "msg_*.json"))):
        try:
            with open(fp, 'r', encoding='utf-8-sig') as f:
                m = json.load(f)
            m["_filepath"] = fp
            messages.append(m)
        except:
            pass
    return {"count": len(messages), "messages": messages}

def check():
    """Try IPC first, fallback to direct file read."""
    result = check_via_ipc()
    if result is None:
        result = check_direct()
        result["_source"] = "direct"
    else:
        result["_source"] = "daemon"
    return result

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--pretty", action="store_true")
    args = p.parse_args()

    result = check()

    if args.pretty:
        print(f"📬 Inbox: {result['count']} message(s) [via {result.get('_source', '?')}]")
        for m in result.get("messages", []):
            print(f"  [{m.get('type','?')}] {m.get('from','?')}: {m.get('message','')[:80]}")
            print(f"    ID: {m.get('id','?')[:8]}  Time: {m.get('timestamp','?')}")
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
