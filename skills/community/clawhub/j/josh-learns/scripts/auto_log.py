#!/usr/bin/env python3
"""MeshMorize Auto-Logger — appends to today's daily log.

Usage: ONLY call this when there's something to remember.
Format: auto_log "What was said/done/decided"

Call this as the LAST step before responding to the user.
"""
import sys, os
from datetime import datetime

LOG_DIR = os.path.expanduser("~/.openclaw/workspace/memory")
now = datetime.now()
filename = f"{LOG_DIR}/{now.strftime('%Y-%m-%d')}.md"
timestamp = now.strftime("%H:%M")

if len(sys.argv) < 2:
    print("Usage: auto_log 'what happened'")
    sys.exit(1)

message = sys.argv[1]
entry = f"\n## {timestamp} — auto\n> {message}\n"

with open(filename, "a") as f:
    f.write(entry)

# Also update LATEST.md
latest = os.path.join(LOG_DIR, "LATEST.md")
ts = now.strftime('%Y-%m-%d %H:%M')
latest_entry = f"\n**{ts}**\n> {message}\n"
with open(latest, "a") as f:
    f.write(latest_entry)

print(f"✅ Logged at {timestamp}")
