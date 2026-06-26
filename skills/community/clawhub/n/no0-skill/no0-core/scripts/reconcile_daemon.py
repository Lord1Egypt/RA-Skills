#!/usr/bin/env python3
import argparse
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_LOG_FILE = SCRIPT_DIR.parent / "heartbeat_log.txt"
LOG_FILE = DEFAULT_LOG_FILE
HEARTBEAT_SCRIPT = SCRIPT_DIR / "heartbeat_processor.py"


def now_text() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def append_log(message: str) -> None:
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message + "\n")


def main() -> int:
    global LOG_FILE

    parser = argparse.ArgumentParser(description="Run heartbeat processor every N seconds")
    parser.add_argument("--interval", type=int, default=120)
    parser.add_argument("--once", action="store_true")
    parser.add_argument("--log-file", default=str(DEFAULT_LOG_FILE), help="Path of heartbeat log file")
    args = parser.parse_args()

    interval = max(30, int(args.interval))
    LOG_FILE = Path(args.log_file).expanduser().resolve()

    while True:
        tick_time = now_text()
        print(f"[{tick_time}] heartbeat (classify + reconcile)")
        append_log(f"[{tick_time}] heartbeat started")

        hb = subprocess.run([sys.executable, str(HEARTBEAT_SCRIPT)], cwd=str(SCRIPT_DIR), check=False)
        append_log(f"[{now_text()}] heartbeat exit_code={hb.returncode}")

        if args.once:
            return int(hb.returncode)
        time.sleep(interval)


if __name__ == "__main__":
    raise SystemExit(main())
