#!/usr/bin/env python3
"""
LYGO Ollama Army Launcher v0.9.0 — ClawHub-safe

In-process threads only. Local Ollama only.
No subprocess. No desktop installers. No planting. No social outbound.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import ollama_daemon as od  # noqa: E402
from ollama_client import is_ollama_ready  # noqa: E402

DEFAULT_MODEL = os.environ.get("LYGO_OLLAMA_MODEL", "llama3.2:1b")
DEFAULT_ROLES = ["hb-light", "draft-simple", "memory-triage"]
SIG = "Delta9Phi963-ARMY-LAUNCHER-v0.9.0"


def launch_daemon(role: str, model: str, champion: str | None, poll: float) -> threading.Thread:
    def worker() -> None:
        od.run_daemon(role, model, poll, champion)

    thr = threading.Thread(target=worker, name=f"army-{role}", daemon=True)
    thr.start()
    print(f"[LAUNCHED] army-{role} (thread)")
    return thr


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="ollama_army_launcher")
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument(
        "--roles",
        default=",".join(DEFAULT_ROLES),
        help="Comma-separated SAFE roles only",
    )
    ap.add_argument("--count", type=int, default=1)
    ap.add_argument("--champion", default=None)
    ap.add_argument("--poll", type=float, default=5.0)
    ap.add_argument("--once-check", action="store_true", help="Only check Ollama and exit")
    args = ap.parse_args(argv)

    roles = [r.strip() for r in args.roles.split(",") if r.strip()]
    bad = [r for r in roles if r not in od.SAFE_ROLES]
    if bad:
        print(json.dumps({"ok": False, "error": "roles_not_allowlisted", "bad": bad, "allowed": sorted(od.SAFE_ROLES)}))
        return 2

    ready = is_ollama_ready()
    print(json.dumps({"ok": True, "signature": SIG, "ollama_ready": ready, "model": args.model, "roles": roles}))
    if args.once_check:
        return 0 if ready else 1
    if not ready:
        print("Ollama not ready on localhost — start Ollama then re-run.", file=sys.stderr)
        return 1

    threads: list[threading.Thread] = []
    for role in roles:
        for _ in range(max(1, args.count)):
            threads.append(launch_daemon(role, args.model, args.champion, args.poll))
            time.sleep(0.05)

    print("Army live (Ctrl+C to stop). Queue: ollama_queue/ or ollama_command_center/tasks/")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping launcher (daemon threads exit with process).")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
