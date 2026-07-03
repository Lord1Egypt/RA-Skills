#!/usr/bin/env python3
"""
LYGO Network Sentinel — lattice + local git + optional HF Space probe.
Read-only on remotes. Writes status to workspace for dashboard.

  python sentinel_heartbeat.py           # one shot
  python sentinel_heartbeat.py --loop    # every 5 min (configurable)
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

CC = Path(__file__).resolve().parents[1]
CONFIG_PATH = CC / "config" / "army_config.json"
LOGS = CC / "logs"
WORKSPACE = CC / "workspace"
STATUS_FILE = WORKSPACE / "sentinel_status.json"
HEARTBEAT_LOG = LOGS / "sentinel.log"


def load_config() -> dict:
    if CONFIG_PATH.is_file():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {"lygo_stack_root": os.environ.get("LYGO_STACK_ROOT", ""), "sentinel": {"interval_seconds": 300}}


def run_lattice(stack_root: Path) -> dict:
    script = stack_root / "tools" / "verify_lattice_alignment.py"
    if not script.is_file():
        return {"ok": False, "detail": "verify_lattice_alignment.py missing"}
    cp = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(stack_root),
        capture_output=True,
        text=True,
        timeout=180,
    )
    aligned = cp.returncode == 0 and "ALIGNED" in (cp.stdout or "")
    return {
        "ok": aligned,
        "exit_code": cp.returncode,
        "summary": "ALIGNED" if aligned else "NEEDS_FIX",
        "tail": (cp.stdout or "")[-1500:],
    }


def run_git_clean(stack_root: Path) -> dict:
    if not (stack_root / ".git").is_dir():
        return {"ok": True, "detail": "not a git checkout"}
    cp = subprocess.run(
        ["git", "status", "-sb"],
        cwd=str(stack_root),
        capture_output=True,
        text=True,
        timeout=60,
    )
    lines = [ln for ln in (cp.stdout or "").splitlines() if ln.strip()]
    # First line is branch summary (## ...); dirty only if more lines or modified/untracked markers
    dirty = len(lines) > 1 or any(
        ln.startswith("??") or ln.startswith(" M") or ln.startswith("M ") or ln.startswith("A ")
        for ln in lines[1:]
    )
    return {"ok": cp.returncode == 0, "clean": not dirty, "status_line": lines[0][:200] if lines else ""}


def probe_hf_space() -> dict:
    url = "https://huggingface.co/api/spaces/DeepSeekOracle/LYGO-Resonance-Engine"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "LYGO-Sentinel/1.0"})
        with urllib.request.urlopen(req, timeout=25) as resp:
            data = json.loads(resp.read().decode())
        runtime = data.get("runtime") or {}
        stage = runtime.get("stage") or data.get("stage") or "unknown"
        err = (runtime.get("errorMessage") or "")[:240]
        stage_ok = stage in (
            "RUNNING",
            "BUILDING",
            "STARTING",
            "PAUSED",
            "APP_STARTING",
            "RUNNING_APP_STARTING",
        )
        return {
            "ok": stage_ok,
            "stage": stage,
            "id": data.get("id", "LYGO-Resonance-Engine"),
            "error_preview": err or None,
        }
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return {"ok": False, "error": str(exc)[:200]}


def probe_public_pages(cfg: dict) -> dict:
    """HEAD/GET check of stack public URLs from army_config system_profile."""
    profile = cfg.get("system_profile") or {}
    urls = profile.get("public_pages") or []
    if not urls:
        return {"ok": True, "detail": "no urls configured", "checked": 0}
    ok_count = 0
    rows: list[dict] = []
    for url in urls:
        row = {"url": url, "status": None, "ok": False}
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "LYGO-Sentinel/2.0"}, method="HEAD")
            try:
                with urllib.request.urlopen(req, timeout=20) as resp:
                    row["status"] = resp.status
                    row["ok"] = 200 <= resp.status < 400
            except urllib.error.HTTPError as he:
                if he.code == 405:
                    req = urllib.request.Request(url, headers={"User-Agent": "LYGO-Sentinel/2.0"})
                    with urllib.request.urlopen(req, timeout=25) as resp:
                        row["status"] = resp.status
                        row["ok"] = 200 <= resp.status < 400
                else:
                    row["status"] = he.code
                    row["ok"] = False
        except Exception as exc:
            row["error"] = str(exc)[:160]
        if row.get("ok"):
            ok_count += 1
        rows.append(row)
    return {"ok": ok_count == len(urls), "checked": len(urls), "live": ok_count, "pages": rows}


def probe_ollama() -> dict:
    try:
        req = urllib.request.Request("http://127.0.0.1:11434/api/tags")
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode())
        models = [m.get("name") for m in data.get("models", [])]
        return {"ok": bool(models), "models": models[:8]}
    except Exception as exc:
        return {"ok": False, "error": str(exc)[:120]}


def run_network_builder(stack_root: Path) -> dict:
    script = stack_root / "tools" / "lygo_network_builder_verify.py"
    if not script.is_file():
        return {"ok": True, "detail": "network builder tool not in stack"}
    cp = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(stack_root),
        capture_output=True,
        text=True,
        timeout=180,
    )
    try:
        blob = json.loads(cp.stdout or "{}")
        ok = bool(blob.get("all_pass"))
        return {"ok": ok, "verdict": blob.get("verdict"), "anchors_sha256": blob.get("anchors_sha256")}
    except json.JSONDecodeError:
        return {"ok": cp.returncode == 0, "parse_error": True}


def queue_depth(cc: Path) -> dict:
    tasks = CC / "tasks"
    legacy = cc.parent / "ollama_queue"
    n = len(list(tasks.glob("*.task.json"))) if tasks.is_dir() else 0
    n += len(list(legacy.glob("*.task.json"))) if legacy.is_dir() else 0
    results = CC / "results"
    legacy_r = cc.parent / "ollama_results"
    nr = len(list(results.glob("*.json"))) if results.is_dir() else 0
    nr += len(list(legacy_r.glob("*.json"))) if legacy_r.is_dir() else 0
    return {"queued": n, "results": nr}


def send_alert(message: str, cfg: dict) -> None:
    print(f"[ALERT] {message}")
    webhook = os.environ.get(cfg.get("notifications", {}).get("webhook_url_env", "LYGO_ARMY_WEBHOOK_URL") or "")
    if not webhook:
        return
    try:
        body = json.dumps({"text": message}).encode()
        urllib.request.urlopen(
            urllib.request.Request(webhook, data=body, headers={"Content-Type": "application/json"}),
            timeout=10,
        )
    except Exception as exc:
        print(f"[ALERT] webhook failed: {exc}")


def one_pulse(cfg: dict, army_root: Path) -> dict:
    army_root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(army_root))
    from lygo_stack_root import resolve_stack_root

    stack = resolve_stack_root(config_path=army_root / "ollama_command_center" / "config" / "army_config.json")
    ts = datetime.now(timezone.utc).isoformat()
    report = {
        "timestamp": ts,
        "signature": cfg.get("signature", "Δ9Φ963-SENTINEL"),
        "lattice": run_lattice(stack),
        "git": run_git_clean(stack),
        "hf_space": probe_hf_space(),
        "ollama": probe_ollama(),
        "queue": queue_depth(army_root),
    }
    if cfg.get("sentinel", {}).get("probe_public_pages", True):
        report["public_pages"] = probe_public_pages(cfg)
    else:
        report["public_pages"] = {"ok": True, "detail": "probe disabled"}
    sent = cfg.get("sentinel") or {}
    if sent.get("probe_network_builder", False):
        report["network_builder"] = run_network_builder(stack)
    require_ollama = bool(sent.get("require_ollama_for_healthy", True))
    ollama_ok = report["ollama"].get("ok", True) if require_ollama else True
    nb_ok = (report.get("network_builder") or {}).get("ok", True)
    report["healthy"] = (
        report["lattice"]["ok"]
        and report["hf_space"].get("ok", True)
        and report["public_pages"].get("ok", True)
        and nb_ok
        and ollama_ok
    )

    LOGS.mkdir(parents=True, exist_ok=True)
    WORKSPACE.mkdir(parents=True, exist_ok=True)
    pp = report.get("public_pages") or {}
    line = (
        f"{ts} | lattice={report['lattice'].get('summary')} | "
        f"hf={report['hf_space'].get('stage', report['hf_space'].get('error', '?'))} | "
        f"pages={pp.get('live', '?')}/{pp.get('checked', '?')} | "
        f"queue={report['queue']['queued']} | ollama={report['ollama']['ok']}\n"
    )
    with HEARTBEAT_LOG.open("a", encoding="utf-8") as f:
        f.write(line)
    STATUS_FILE.write_text(json.dumps(report, indent=2), encoding="utf-8")

    if cfg.get("sentinel", {}).get("alert_on_lattice_fail") and not report["lattice"]["ok"]:
        send_alert(f"LYGO lattice check FAILED at {ts}", cfg)
    return report


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--loop", action="store_true", help="Run every interval (default 300s)")
    ap.add_argument("--interval", type=int, default=0, help="Override interval seconds")
    args = ap.parse_args()
    cfg = load_config()
    army_root = Path(__file__).resolve().parents[2]
    interval = args.interval or int(cfg.get("sentinel", {}).get("interval_seconds", 300))

    if not args.loop:
        one_pulse(cfg, army_root)
        print(json.dumps(json.loads(STATUS_FILE.read_text(encoding="utf-8")), indent=2))
        return 0 if json.loads(STATUS_FILE.read_text(encoding="utf-8"))["lattice"]["ok"] else 1

    print(f"Sentinel loop every {interval}s — Ctrl+C to stop")
    while True:
        try:
            one_pulse(cfg, army_root)
        except Exception as exc:
            print(f"[sentinel err] {exc}")
        time.sleep(interval)


if __name__ == "__main__":
    raise SystemExit(main())