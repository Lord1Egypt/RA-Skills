#!/usr/bin/env python3
"""
Archive processed inbox messages via LCP daemon (IPC).
Replaces ack.py for UDP mode.

Usage:
    python3 lcp_ack.py
"""

import sys
import os
import json
import socket
import glob

IPC_SOCKET = "/tmp/lcp.sock"

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INBOX_DIR = os.path.join(SKILL_DIR, "data", "inbox")
INBOX_ARCHIVE = os.path.join(SKILL_DIR, "data", "inbox_archive")
os.makedirs(INBOX_ARCHIVE, exist_ok=True)

def ack_via_ipc():
    req = json.dumps({"cmd": "ACK"})
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(10.0)
    try:
        sock.connect(IPC_SOCKET)
        sock.sendall(req.encode('utf-8'))
        raw = sock.recv(65536)
        return json.loads(raw.decode('utf-8'))
    except (ConnectionRefusedError, FileNotFoundError):
        return None
    finally:
        sock.close()

def ack_direct():
    """Fallback: archive directly."""
    archived = 0
    for fp in glob.glob(os.path.join(INBOX_DIR, "msg_*.json")):
        try:
            fname = os.path.basename(fp)
            dst = os.path.join(INBOX_ARCHIVE, fname)
            os.rename(fp, dst)
            archived += 1
        except:
            pass
    return {"archived": archived}

if __name__ == "__main__":
    result = ack_via_ipc()
    if result is None:
        result = ack_direct()
        result["_source"] = "direct"
    else:
        result["_source"] = "daemon"

    print(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"✅ Archived {result.get('archived', 0)} message(s)")
