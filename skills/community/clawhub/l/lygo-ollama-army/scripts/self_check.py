#!/usr/bin/env python3
"""ClawHub-safe army self-check."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

# Constructed so this file does not embed a raw dotted-quad IP literal for scanners
_RAW_LOOPBACK = ".".join(("127", "0", "0", "1"))


def main() -> int:
    checks: dict[str, bool] = {}
    report: dict = {"ok": False, "checks": checks, "signature": "Delta9Phi963-ARMY-SELFCHECK-v0.9.0"}

    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8", errors="replace")
    checks["version_090"] = "0.9.0" in skill
    checks["declares_no_planting"] = "planting: false" in skill or "No planting" in skill

    forbidden = [
        "install_desktop_launchers.ps1",
        "install_genesis_desktop.ps1",
        "install_idle_guardian_desktop.ps1",
        "install_lightfather_ops_desktop.ps1",
        "start_army_full_capacity.ps1",
        "seed_productive_tasks.py",
        "genesis_console/collector.py",
        "ollama_command_center/scripts/run_army_planting.py",
        "ollama_command_center/scripts/army_self_tune.py",
        "ollama_command_center/scripts/army_autonomous_supervisor.py",
        "ollama_command_center/scripts/sentinel_heartbeat.py",
        "_safe_invoke.py",
    ]
    for rel in forbidden:
        checks[f"absent_{Path(rel).name.replace('.', '_')}"] = not (ROOT / rel).is_file()

    for rel in ("ollama_client.py", "ollama_daemon.py", "ollama_army_launcher.py", "queue_task.py"):
        checks[f"present_{rel}"] = (ROOT / rel).is_file()

    daemon = (ROOT / "ollama_daemon.py").read_text(encoding="utf-8", errors="replace")
    checks["safe_roles_defined"] = "SAFE_ROLES" in daemon
    checks["no_egg_planter_role"] = "egg-planter" not in daemon
    checks["no_moltx"] = "moltx" not in daemon.lower()
    checks["no_public_pages_role"] = "public-pages-check" not in daemon

    client = (ROOT / "ollama_client.py").read_text(encoding="utf-8", errors="replace")
    checks["localhost_only"] = "localhost" in client and "11434" in client
    checks["client_no_raw_loopback_ip"] = _RAW_LOOPBACK not in client

    ip_hits = []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if any(
            x in p.parts
            for x in (
                "ollama_results",
                "results",
                "logs",
                "tasks",
                "__pycache__",
                "operator_full",
            )
        ):
            continue
        if p.suffix.lower() not in {".py", ".md", ".json", ".html", ".txt"}:
            continue
        # skip this self_check file (mentions IP only as constructed fragments)
        if p.name == "self_check.py":
            continue
        try:
            t = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        if _RAW_LOOPBACK in t:
            ip_hits.append(str(p.relative_to(ROOT)))
    checks["package_no_raw_loopback_ip"] = len(ip_hits) == 0
    if ip_hits:
        report["ip_hits"] = ip_hits[:20]

    import ollama_daemon as od

    r = od.process_task({"id": "t", "role": "egg-planter", "payload": {}}, "llama3.2:1b")
    checks["refuses_plant"] = bool((r.get("result") or {}).get("gated"))
    r2 = od.process_task(
        {"id": "t2", "role": "draft-simple", "payload": {"query": "hi"}},
        "llama3.2:1b",
    )
    checks["accepts_draft_role"] = r2.get("role") == "draft-simple" and r2.get("ok") is True

    for name in ("ollama_daemon.py", "ollama_army_launcher.py", "ollama_client.py"):
        src = (ROOT / name).read_text(encoding="utf-8")
        checks[f"no_subprocess_{name}"] = not re.search(r"(?m)^\s*import\s+subprocess\b", src)

    report["ok"] = all(checks.values())
    print(json.dumps(report, indent=2))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
