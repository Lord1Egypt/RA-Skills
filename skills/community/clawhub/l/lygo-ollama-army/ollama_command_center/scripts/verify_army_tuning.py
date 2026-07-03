#!/usr/bin/env python3
"""One-shot army tuning verify — config, roles, stack, ollama, lattice."""

from __future__ import annotations

import json
import subprocess
import sys
import urllib.request
from pathlib import Path

CC = Path(__file__).resolve().parents[1]
ARMY = CC.parent
CONFIG = CC / "config" / "army_config.json"
OUT = CC / "workspace" / "army_tuning_last_run.json"


def main() -> int:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    stack = Path(cfg.get("lygo_stack_root", ""))
    cap = cfg.get("army_capacity") or {}
    roles = cap.get("roles") or []
    checks: list[dict] = []

    def add(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    add("config_v3", cfg.get("signature") == "Δ9Φ963-ARMY-CC-v3", cfg.get("signature", "?"))
    add("mesh_cartographer_in_roles", "mesh-cartographer" in roles, f"{len(roles)} roles")
    add("planting_enabled", bool((cfg.get("planting") or {}).get("enabled")), "")
    add("access_locked", not (cfg.get("access") or {}).get("github_push"), "no external push")

    daemon = (ARMY / "ollama_daemon.py").read_text(encoding="utf-8")
    add("daemon_mesh_handler", 'role == "mesh-cartographer"' in daemon, "")
    add("daemon_deterministic_set", "mesh-cartographer" in daemon, "")
    st = CC / "scripts" / "army_self_tune.py"
    add("self_tune_script", st.is_file(), "")
    self_last = CC / "workspace" / "army_self_tune_last_run.json"
    if self_last.is_file():
        sl = json.loads(self_last.read_text(encoding="utf-8"))
        add("self_tune_recent", sl.get("verdict") in ("SELF_TUNED", "NOOP"), sl.get("verdict", "?"))

    try:
        with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=5) as resp:
            models = json.loads(resp.read().decode()).get("models", [])
        want = cap.get("model", "llama3.2:1b")
        names = [m.get("name", "") for m in models]
        add("ollama_reachable", True, str(names[:3]))
        add("ollama_model", any(want in n for n in names), want)
    except Exception as exc:
        add("ollama_reachable", False, str(exc)[:80])
        add("ollama_model", False, "n/a")

    lat = stack / "tools" / "verify_lattice_alignment.py"
    if lat.is_file():
        cp = subprocess.run([sys.executable, str(lat)], cwd=stack, capture_output=True, text=True, timeout=240)
        add("lattice_aligned", cp.returncode == 0, "ALIGNED" if cp.returncode == 0 else "NEEDS_FIX")
    else:
        add("lattice_aligned", False, "missing script")

    all_ok = all(c["ok"] for c in checks if c["name"] != "ollama_model")
    report = {
        "signature": "Δ9Φ963-ARMY-TUNING-VERIFY-v1",
        "checks": checks,
        "all_pass": all_ok,
        "verdict": "TUNED" if all_ok else "NEEDS_FIX",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())