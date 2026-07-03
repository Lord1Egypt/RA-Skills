#!/usr/bin/env python3
"""
Autonomous army self-tune — read-only stack probes + safe local config/queue hygiene.
Never enables github_push, hf_write, or clawhub_publish.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CC = Path(__file__).resolve().parents[1]
ARMY = CC.parent
CONFIG_PATH = CC / "config" / "army_config.json"
WORKSPACE = CC / "workspace"
STATUS_FILE = WORKSPACE / "sentinel_status.json"
OUT = WORKSPACE / "army_self_tune_last_run.json"
LOG = CC / "logs" / "self_tune.log"


def load_json(path: Path, default: dict | None = None) -> dict:
    if not path.is_file():
        return default or {}
    return json.loads(path.read_text(encoding="utf-8"))


def ollama_up() -> bool:
    try:
        with urllib.request.urlopen("http://127.0.0.1:11434/api/tags", timeout=4) as resp:
            data = json.loads(resp.read().decode())
        return bool(data.get("models"))
    except Exception:
        return False


def sync_clawhub_expect(cfg: dict, stack: Path) -> list[str]:
    actions: list[str] = []
    skills = stack / "clawhub" / "skills.json"
    if not skills.is_file():
        return actions
    data = json.loads(skills.read_text(encoding="utf-8"))
    profile = cfg.setdefault("system_profile", {})
    expect = profile.setdefault("clawhub_expect", {})
    pub = data.get("count_published")
    if pub and expect.get("count_published") != pub:
        expect["count_published"] = pub
        actions.append(f"clawhub_expect.count_published={pub}")
    slugs = {s.get("slug") for s in data.get("skills", [])}
    req = list(expect.get("required_slugs") or [])
    for must in ("lygo-network-builder", "lygo-kernel-egg-planter", "lygo-protocol-stack-operator"):
        if must in slugs and must not in req:
            req.append(must)
            actions.append(f"required_slugs+={must}")
    expect["required_slugs"] = req
    return actions


def prune_completed_tasks(max_keep: int) -> list[str]:
    actions: list[str] = []
    result_stems: set[str] = set()
    for d in (CC / "results", ARMY / "ollama_results"):
        if not d.is_dir():
            continue
        for p in d.glob("*.result.json"):
            result_stems.add(p.name.replace(".result.json", ""))
        for p in d.glob("*.json"):
            if p.name.endswith(".result.json"):
                continue
            result_stems.add(p.stem)

    removed = 0
    for qdir in (CC / "tasks", ARMY / "ollama_queue"):
        if not qdir.is_dir():
            continue
        for task in list(qdir.glob("*.task.json")):
            tid = task.stem.replace(".task", "")
            if tid in result_stems:
                task.unlink(missing_ok=True)
                removed += 1

    queued = sum(len(list(d.glob("*.task.json"))) for d in (CC / "tasks", ARMY / "ollama_queue") if d.is_dir())
    if queued > max_keep:
        excess = queued - max_keep
        for qdir in (CC / "tasks", ARMY / "ollama_queue"):
            if not qdir.is_dir() or excess <= 0:
                continue
            for task in sorted(qdir.glob("cron-*.task.json"), key=lambda p: p.stat().st_mtime):
                if excess <= 0:
                    break
                task.unlink(missing_ok=True)
                excess -= 1
                removed += 1
        actions.append(f"pruned_queue_overflow removed={removed} target<={max_keep}")
    elif removed:
        actions.append(f"pruned_completed_tasks removed={removed}")
    return actions


def apply_runtime_tuning(cfg: dict, sentinel: dict) -> list[str]:
    actions: list[str] = []
    healthy = bool(sentinel.get("healthy"))
    lattice_ok = (sentinel.get("lattice") or {}).get("ok", False)
    sent = cfg.setdefault("sentinel", {})
    cap = cfg.setdefault("army_capacity", {})
    tune = cfg.get("self_tune") or {}

    want_interval = 300 if healthy else 180
    if sent.get("interval_seconds") != want_interval:
        sent["interval_seconds"] = want_interval
        cfg["poll_seconds"] = want_interval
        actions.append(f"sentinel.interval_seconds={want_interval}")

    if ollama_up():
        if int(cap.get("hb_light_instances", 1)) < 2:
            cap["hb_light_instances"] = 2
            actions.append("hb_light_instances=2")
    else:
        cap["hb_light_instances"] = 1
        actions.append("hb_light_instances=1 (ollama offline)")

    sent["require_ollama_for_healthy"] = False

    planting = cfg.setdefault("planting", {})
    if lattice_ok and tune.get("auto_enable_planting", True):
        if not planting.get("enabled"):
            planting["enabled"] = True
            actions.append("planting.enabled=true (lattice OK)")
    elif not lattice_ok and tune.get("pause_planting_on_lattice_fail", True):
        if planting.get("enabled"):
            planting["enabled"] = False
            actions.append("planting.enabled=false (lattice fail)")

    if not sent.get("probe_network_builder"):
        sent["probe_network_builder"] = True
        actions.append("probe_network_builder=true")

    return actions


def main() -> int:
    cfg = load_json(CONFIG_PATH)
    if not cfg.get("self_tune", {}).get("enabled", True):
        print(json.dumps({"skipped": "self_tune.disabled"}))
        return 0

    stack = Path(cfg.get("lygo_stack_root", r"I:\E Drive\lygo-protocol-stack"))
    sentinel = load_json(STATUS_FILE)
    if not sentinel and (CC / "scripts" / "sentinel_heartbeat.py").is_file():
        subprocess.run([sys.executable, str(CC / "scripts" / "sentinel_heartbeat.py")], check=False, timeout=240)
        sentinel = load_json(STATUS_FILE)

    actions: list[str] = []
    if (cfg.get("self_tune") or {}).get("sync_clawhub_expect_from_stack", True):
        actions.extend(sync_clawhub_expect(cfg, stack))
    max_q = int((cfg.get("self_tune") or {}).get("max_queued_tasks", 30))
    actions.extend(prune_completed_tasks(max_q))
    actions.extend(apply_runtime_tuning(cfg, sentinel))

    hsc = cfg.get("haven_star_chart") or {}
    if hsc.get("rebuild_on_self_tune", True) and (sentinel.get("lattice") or {}).get("ok"):
        builder = stack / "tools" / "build_haven_star_chart.py"
        if builder.is_file():
            import subprocess
            import sys

            cp = subprocess.run([sys.executable, str(builder)], cwd=stack, capture_output=True, text=True, timeout=120)
            if cp.returncode == 0:
                actions.append("haven_star_chart.rebuilt")
            else:
                actions.append("haven_star_chart.rebuild_failed")

    backup = CONFIG_PATH.with_suffix(".json.bak")
    shutil.copy2(CONFIG_PATH, backup)
    CONFIG_PATH.write_text(json.dumps(cfg, indent=2) + "\n", encoding="utf-8")

    report = {
        "signature": "Δ9Φ963-ARMY-SELF-TUNE-v1",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actions": actions,
        "healthy": sentinel.get("healthy"),
        "lattice": (sentinel.get("lattice") or {}).get("summary"),
        "queue": sentinel.get("queue"),
        "config_backup": str(backup),
        "verdict": "SELF_TUNED" if actions else "NOOP",
    }
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"{report['timestamp']} | {len(actions)} actions | {actions}\n")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())