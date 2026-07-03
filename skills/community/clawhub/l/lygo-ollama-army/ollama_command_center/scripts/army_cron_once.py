#!/usr/bin/env python3
"""Single cron tick: sentinel pulse + seed deterministic army tasks (no LLM)."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

CC = Path(__file__).resolve().parents[1]
ARMY = CC.parent
STACK = Path(json.loads((CC / "config" / "army_config.json").read_text(encoding="utf-8")).get("lygo_stack_root", r"I:\E Drive\lygo-protocol-stack"))
TASKS = CC / "tasks"
TASKS.mkdir(parents=True, exist_ok=True)


def main() -> int:
    subprocess.run([sys.executable, str(CC / "scripts" / "army_self_tune.py")], check=False, timeout=120)
    subprocess.run([sys.executable, str(CC / "scripts" / "sentinel_heartbeat.py")], check=False)

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    for role, tid in [
        ("lattice-check", f"cron-lattice-{ts}"),
        ("stack-integrity", f"cron-stack-{ts}"),
        ("clawhub-catalog-audit", f"cron-clawhub-{ts}"),
        ("public-pages-check", f"cron-pages-{ts}"),
        ("audit-suite", f"cron-audit-suite-{ts}"),
        ("memory-sync", f"cron-memory-{ts}"),
        ("anchor-health", f"cron-anchor-{ts}"),
        ("mesh-cartographer", f"cron-mesh-{ts}"),
        ("self-tune", f"cron-self-tune-{ts}"),
        ("egg-planter", f"cron-egg-plant-{ts}"),
        ("registry-planter", f"cron-registry-plant-{ts}"),
    ]:
        path = TASKS / f"{tid}.task.json"
        if not path.exists():
            path.write_text(json.dumps({"id": tid, "role": role, "payload": {}}), encoding="utf-8")

    # Mirror into legacy queue for existing daemons
    legacy = ARMY / "ollama_queue"
    legacy.mkdir(parents=True, exist_ok=True)
    for p in TASKS.glob("cron-*.task.json"):
        dest = legacy / p.name
        if not dest.exists():
            dest.write_text(p.read_text(encoding="utf-8"), encoding="utf-8")

    print(f"Cron tick OK — tasks in {TASKS} and {legacy}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())