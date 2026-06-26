#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Progress selfcheck (Feishu send + Webchat pull artifacts).

- Cron runtime snapshot from cron store jobs.json
- Task ledger snapshot + eligible auto-reactivation
- Artifacts written to output/ for webchat pull

Designed for publishing: all paths/targets configurable.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from _config import load_config

# local imports
import sys
HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from task_ledger import derive_state, load_events as load_task_events


def _ms_to_hm(ms: int | None) -> str:
    if not ms:
        return "-"
    try:
        dt = datetime.fromtimestamp(ms / 1000)
        return dt.strftime("%H:%M")
    except Exception:
        return "-"


def _ms_ago(ms: int | None) -> str:
    if not ms:
        return "-"
    try:
        now = datetime.now().timestamp() * 1000
        delta = max(0, int(now - ms))
        mins = delta // 60000
        if mins < 60:
            return f"{mins}m"
        return f"{mins//60}h{mins%60}m"
    except Exception:
        return "-"


def _read_recent_events(cfg: dict, limit: int = 5) -> list[dict]:
    memdir = Path(cfg["memory_dir"])
    day = datetime.now().strftime("%Y-%m-%d")
    path = memdir / f"events_{day}.jsonl"
    if not path.exists():
        return []
    lines = [ln.strip() for ln in path.read_text(encoding="utf-8", errors="replace").splitlines() if ln.strip()]
    out = []
    for ln in lines[-max(limit, 1):]:
        try:
            out.append(json.loads(ln))
        except Exception:
            continue
    return out


def _load_cron_jobs(cfg: dict) -> list[dict]:
    p = Path(cfg["cron_store"])
    if not p.exists():
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8", errors="replace"))
        return data.get("jobs", []) or []
    except Exception:
        return []


def _cron_snapshot(jobs: list[dict], limits: dict) -> dict:
    now_ms = int(datetime.now().timestamp() * 1000)
    running, recent, alerts = [], [], []

    for j in jobs:
        name = j.get("name")
        enabled = bool(j.get("enabled"))
        state = j.get("state") or {}

        running_at = state.get("runningAtMs")
        last_at = state.get("lastRunAtMs")
        last_status = state.get("lastRunStatus") or state.get("lastStatus")
        last_dur = state.get("lastDurationMs")
        next_at = state.get("nextRunAtMs")
        consec_err = int(state.get("consecutiveErrors") or 0)

        if enabled and running_at:
            running.append({"name": name, "since": _ms_ago(running_at)})

        if enabled and last_at and (now_ms - int(last_at) <= 20 * 60 * 1000):
            recent.append({
                "name": name,
                "at": _ms_to_hm(last_at),
                "status": last_status or "-",
                "dur": f"{int(last_dur)//1000}s" if last_dur else "-",
            })

        if enabled and consec_err > 0:
            alerts.append({"name": name, "issue": f"consecutiveErrors={consec_err}", "last": _ms_to_hm(last_at)})

        if enabled and next_at and int(next_at) < now_ms - 5 * 60 * 1000:
            alerts.append({"name": name, "issue": f"overdue nextRun ({_ms_ago(int(next_at))} ago)", "last": _ms_to_hm(last_at)})

    running.sort(key=lambda x: x["name"] or "")
    recent.sort(key=lambda x: (x["at"], x["name"] or ""), reverse=True)

    return {
        "running": running[: limits.get("running", 6)],
        "recent": recent[: limits.get("recent", 8)],
        "alerts": alerts[: limits.get("alerts", 6)],
    }


def _parse(ts: str | None):
    if not ts:
        return None
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M"):
        try:
            return datetime.strptime(ts, fmt)
        except Exception:
            pass
    return None


def _task_snapshot(cfg: dict, stale_min: int, limits: dict) -> dict:
    tasks = derive_state(load_task_events())
    now = datetime.now()

    unfinished = []
    eligible = []
    done_today = []

    today = datetime.now().strftime("%Y-%m-%d")

    for t in tasks.values():
        lt = _parse(t.get("last_touch")) or _parse(t.get("updated_at"))
        mins = None
        if lt:
            mins = (now - lt).total_seconds() / 60.0

        rec = {
            "id": t.get("id"),
            "status": t.get("status"),
            "title": t.get("title"),
            "auto": bool(t.get("auto")),
            "repeatable": bool(t.get("repeatable")),
            "stale_min": int(mins) if mins is not None else None,
            "next": t.get("next") or "",
            "updated_at": t.get("updated_at") or "",
        }

        if rec["status"] in ("todo", "doing", "blocked"):
            unfinished.append(rec)

        if rec["status"] == "done":
            if cfg.get("done_display", {}).get("today_only", True):
                if (rec["updated_at"] or "").startswith(today):
                    done_today.append(rec)
            else:
                done_today.append(rec)

        if rec["status"] in ("doing", "blocked") and rec["auto"] and mins is not None and mins >= stale_min and rec["next"]:
            eligible.append(rec)

    unfinished.sort(key=lambda x: (x.get("stale_min") or -1), reverse=True)
    eligible.sort(key=lambda x: (x.get("stale_min") or 0), reverse=True)
    done_today.sort(key=lambda x: x.get("updated_at") or "", reverse=True)

    return {
        "unfinished": unfinished[: limits.get("unfinished", 5)],
        "eligible": eligible[: limits.get("eligible", 5)],
        "done_today": done_today[: limits.get("done_today", 3)],
    }


def _write_artifacts(cfg: dict, message: str) -> None:
    outdir = Path(cfg["output_dir"])
    outdir.mkdir(parents=True, exist_ok=True)
    latest = outdir / "progress_selfcheck_latest.md"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    archived = outdir / f"progress_selfcheck_{ts}.md"
    latest.write_text(message, encoding="utf-8")
    archived.write_text(message, encoding="utf-8")


def _send_feishu(cfg: dict, message: str) -> None:
    if not cfg.get("feishu", {}).get("enabled", True):
        return
    account = cfg["feishu"]["account"]
    target = cfg["feishu"]["target"]

    safe = message.replace("`", "``")
    ps = (
        "$m = @'\n" + safe + "\n'@; "
        + f"openclaw message send --channel feishu --account {account} --target {target} --message \"$m\""
    )
    cmd = ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps]

    workdir = Path(cfg["workdir"])
    res = subprocess.run(cmd, cwd=str(workdir), capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        raise SystemExit(f"openclaw message send failed rc={res.returncode}: {res.stderr.strip() or res.stdout.strip()}")


def _format(cfg: dict, events: list[dict], cron_snap: dict, task_snap: dict) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines: List[str] = []
    lines.append(f"🧾 进度自检 {now}")

    lines.append("")
    lines.append("【正在运行】")
    if cron_snap.get("running"):
        for r in cron_snap["running"]:
            lines.append(f"- {r['name']}（已运行 {r['since']}）")
    else:
        lines.append("- （无）")

    lines.append("")
    lines.append("【最近完成（≤20分钟）】")
    if cron_snap.get("recent"):
        for r in cron_snap["recent"]:
            lines.append(f"- {r['at']} {r['name']}：{r['status']}（{r['dur']}）")
    else:
        lines.append("- （无）")

    lines.append("")
    lines.append("【异常/风险】")
    if cron_snap.get("alerts"):
        for a in cron_snap["alerts"]:
            lines.append(f"- {a['name']}：{a['issue']}（last {a['last']}）")
    else:
        lines.append("- （无）")

    lines.append("")
    lines.append("【未完成任务（任务账本）】")
    if task_snap.get("unfinished"):
        for t in task_snap["unfinished"]:
            stale = f"{t['stale_min']}m" if t.get("stale_min") is not None else "-"
            lines.append(f"- {t['id']} {t['status']} auto={t['auto']} rep={t['repeatable']} stale={stale}：{t['title']}")
    else:
        lines.append("- （无）")

    lines.append("")
    lines.append(f"【可自动激活（≥{cfg.get('stale_minutes',5)}分钟未 touch，且 auto=true）】")
    if task_snap.get("eligible"):
        for t in task_snap["eligible"]:
            lines.append(f"- {t['id']} stale={t.get('stale_min','-')}m rep={t.get('repeatable', False)}：{t['title']}")
            lines.append(f"  next: {t['next']}")
    else:
        lines.append("- （无）")

    lines.append("")
    lines.append("【今日已完成（仅当日，Top）】")
    if task_snap.get("done_today"):
        for t in task_snap["done_today"]:
            lines.append(f"- {t['id']}：{t['title']}")
    else:
        lines.append("- （无）")

    lines.append("")
    lines.append("【事件流（语义进度）】")
    if events:
        for ev in reversed(events):
            ts = ev.get("ts") or ev.get("time") or ev.get("timestamp") or ""
            kind = ev.get("kind") or ev.get("type") or "event"
            msg = ev.get("msg") or ev.get("message") or ev.get("summary") or ""
            msg = " ".join(str(msg).split())
            lines.append(f"- [{kind}] {ts} {msg}".strip())
    else:
        lines.append("- （今日暂无事件）")

    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=5, help="events tail limit")
    args = ap.parse_args()

    cfg = load_config()

    jobs = _load_cron_jobs(cfg)
    events = _read_recent_events(cfg, limit=args.limit)

    limits = cfg.get("display_limits", {})
    cron_snap = _cron_snapshot(jobs, limits)
    task_snap = _task_snapshot(cfg, stale_min=int(cfg.get("stale_minutes", 5)), limits=limits)

    # Auto-reactivate safe tasks
    if task_snap.get("eligible"):
        try:
            subprocess.run(["python", str(HERE / "task_reactivate.py"), "--stale-min", str(cfg.get("stale_minutes", 5)), "--max", str(cfg.get("max_reactivate_per_run", 2))],
                           cwd=str(Path(cfg["workdir"])), capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=180)
            task_snap = _task_snapshot(cfg, stale_min=int(cfg.get("stale_minutes", 5)), limits=limits)
        except Exception:
            pass

    msg = _format(cfg, events, cron_snap, task_snap)
    _write_artifacts(cfg, msg)
    _send_feishu(cfg, msg)

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
