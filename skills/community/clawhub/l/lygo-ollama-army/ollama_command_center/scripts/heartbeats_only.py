#!/usr/bin/env python3
"""
LYGO Ollama Heartbeats ONLY — sentinel pulse every 5 minutes.
No LLM daemons, no monitoring UI. Runs until Ctrl+C or window closed.
"""

from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
SENTINEL = HERE / "sentinel_heartbeat.py"
GENESIS_COLLECTOR = HERE.parents[1] / "genesis_console" / "collector.py"
INTERVAL = 300


def main() -> int:
    print("LYGO Heartbeats ONLY — sentinel every 5 min (Ctrl+C to stop)")
    while True:
        try:
            subprocess.run([sys.executable, str(SENTINEL)], check=False, timeout=240)
            if GENESIS_COLLECTOR.is_file():
                subprocess.run([sys.executable, str(GENESIS_COLLECTOR)], check=False, timeout=300)
        except Exception as exc:
            print(f"[heartbeat] {exc}")
        time.sleep(INTERVAL)


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("Heartbeats stopped.")
        raise SystemExit(0)