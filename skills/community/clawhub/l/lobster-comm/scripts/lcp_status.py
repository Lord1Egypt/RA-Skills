#!/usr/bin/env python3
"""
Query LCP daemon status.

Usage:
    python3 lcp_status.py
"""

import sys
import os
import json
import socket
from datetime import datetime, timedelta, timezone

IPC_SOCKET = "/tmp/lcp.sock"

def status():
    req = json.dumps({"cmd": "STATUS"})
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.settimeout(5.0)
    try:
        sock.connect(IPC_SOCKET)
        sock.sendall(req.encode('utf-8'))
        raw = sock.recv(65536)
        return json.loads(raw.decode('utf-8'))
    except (ConnectionRefusedError, FileNotFoundError):
        return {"error": "Daemon not running"}
    finally:
        sock.close()

if __name__ == "__main__":
    s = status()
    if "error" in s:
        print(f"❌ {s['error']}")
        sys.exit(1)

    tz = timezone(timedelta(hours=8))
    uptime_m = s.get("uptime", 0) / 60
    peer_online = "🟢 Online" if s.get("peer_online") else "🔴 Offline"

    last_seen = s.get("peer_last_seen", 0)
    if last_seen > 0:
        last_seen_str = datetime.fromtimestamp(last_seen, tz).strftime("%H:%M:%S")
    else:
        last_seen_str = "never"

    print(f"🦞 LCP/1.1 Node Status")
    print(f"  Peer: {s.get('peer')} ({s.get('peer_ip')})")
    print(f"  Status: {peer_online}")
    print(f"  Last seen: {last_seen_str}")
    print(f"  Inbox: {s.get('inbox_count', 0)} message(s)")
    print(f"  Uptime: {uptime_m:.1f} min")
