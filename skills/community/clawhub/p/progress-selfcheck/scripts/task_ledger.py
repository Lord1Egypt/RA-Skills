#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Task ledger for assistant work (publishable).

Append-only JSONL events -> derive current state by replay.

Fields:
- id/title/status(next)/auto/repeatable/notes/created_at/updated_at/last_touch

This ledger lives under workspace memory by default.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from _config import load_config


def now_ts() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _ledger_path() -> Path:
    cfg = load_config()
    mem = Path(cfg["memory_dir"]) / "tasks"
    mem.mkdir(parents=True, exist_ok=True)
    return mem / "active_tasks.jsonl"


def append_event(ev: Dict[str, Any]) -> None:
    path = _ledger_path()
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")


def load_events() -> List[Dict[str, Any]]:
    path = _ledger_path()
    if not path.exists():
        return []
    out: List[Dict[str, Any]] = []
    for ln in path.read_text(encoding="utf-8", errors="replace").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            out.append(json.loads(ln))
        except Exception:
            continue
    return out


def derive_state(events: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    tasks: Dict[str, Dict[str, Any]] = {}
    for ev in events:
        tid = ev.get("id")
        if not tid:
            continue
        t = tasks.setdefault(
            tid,
            {
                "id": tid,
                "title": "",
                "status": "todo",
                "next": "",
                "auto": False,
                "repeatable": False,
                "created_at": None,
                "updated_at": None,
                "last_touch": None,
                "notes": "",
            },
        )

        kind = ev.get("event")
        t["updated_at"] = ev.get("ts")

        def _parse_bool(v, default=None):
            if v is None or v == "None":
                return default
            if isinstance(v, bool):
                return v
            s = str(v).strip().lower()
            if s in ("1", "true", "yes", "y"):
                return True
            if s in ("0", "false", "no", "n"):
                return False
            return default

        if kind == "add":
            t["title"] = ev.get("title") or t["title"]
            t["status"] = ev.get("status") or "doing"
            t["next"] = ev.get("next") or t["next"]
            t["auto"] = bool(ev.get("auto"))
            t["repeatable"] = bool(ev.get("repeatable"))
            t["created_at"] = ev.get("ts")
            t["last_touch"] = ev.get("ts")
            t["notes"] = ev.get("notes") or t["notes"]
        elif kind in ("touch", "update"):
            if ev.get("title"):
                t["title"] = ev.get("title")
            if ev.get("status"):
                t["status"] = ev.get("status")
            if ev.get("next") is not None:
                t["next"] = ev.get("next")
            ab = _parse_bool(ev.get("auto"), default=None)
            if ab is not None:
                t["auto"] = ab
            rb = _parse_bool(ev.get("repeatable"), default=None)
            if rb is not None:
                t["repeatable"] = rb
            if ev.get("notes"):
                t["notes"] = ev.get("notes")
            t["last_touch"] = ev.get("ts")
        elif kind == "done":
            t["status"] = "done"
            t["last_touch"] = ev.get("ts")
        elif kind == "block":
            t["status"] = "blocked"
            t["notes"] = ev.get("reason") or t["notes"]
            t["last_touch"] = ev.get("ts")

    return tasks


def gen_id(prefix_date: str, seq: int) -> str:
    return f"T{prefix_date}-{seq:03d}"


def next_seq(tasks: Dict[str, Dict[str, Any]], prefix_date: str) -> int:
    mx = 0
    for tid in tasks.keys():
        if tid.startswith(f"T{prefix_date}-"):
            try:
                mx = max(mx, int(tid.split("-")[-1]))
            except Exception:
                pass
    return mx + 1


def cmd_add(args) -> None:
    tasks = derive_state(load_events())
    prefix = datetime.now().strftime("%Y%m%d")
    tid = gen_id(prefix, next_seq(tasks, prefix))

    append_event(
        {
            "ts": now_ts(),
            "event": "add",
            "id": tid,
            "title": args.title,
            "status": args.status,
            "next": args.next,
            "auto": args.auto,
            "repeatable": args.repeatable,
            "notes": args.notes or "",
        }
    )
    print(tid)


def cmd_touch(args) -> None:
    append_event({"ts": now_ts(), "event": "touch", "id": args.id, "notes": args.notes or ""})


def cmd_update(args) -> None:
    append_event(
        {
            "ts": now_ts(),
            "event": "update",
            "id": args.id,
            "title": args.title,
            "status": args.status,
            "next": args.next,
            "auto": args.auto,
            "repeatable": args.repeatable,
            "notes": args.notes,
        }
    )


def cmd_done(args) -> None:
    append_event({"ts": now_ts(), "event": "done", "id": args.id})


def cmd_block(args) -> None:
    append_event({"ts": now_ts(), "event": "block", "id": args.id, "reason": args.reason})


def cmd_list(args) -> None:
    tasks = derive_state(load_events())
    items = list(tasks.values())
    if args.status:
        items = [t for t in items if t.get("status") == args.status]
    items.sort(key=lambda t: (t.get("status") or "", t.get("updated_at") or ""), reverse=True)
    for t in items:
        print(
            f"{t['id']}\t{t['status']}\tauto={t['auto']}\trepeatable={t.get('repeatable', False)}\t{t['title']}\tlast_touch={t.get('last_touch') or '-'}\tnext={t['next']}"
        )


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add")
    a.add_argument("--title", required=True)
    a.add_argument("--next", default="")
    a.add_argument("--auto", type=lambda s: str(s).lower() in ("1", "true", "yes", "y"), default=False)
    a.add_argument("--repeatable", type=lambda s: str(s).lower() in ("1", "true", "yes", "y"), default=False)
    a.add_argument("--status", default="doing", choices=["todo", "doing", "blocked", "done"])
    a.add_argument("--notes", default="")
    a.set_defaults(func=cmd_add)

    t = sub.add_parser("touch")
    t.add_argument("--id", required=True)
    t.add_argument("--notes", default="")
    t.set_defaults(func=cmd_touch)

    u = sub.add_parser("update")
    u.add_argument("--id", required=True)
    u.add_argument("--title", default=None)
    u.add_argument("--next", default=None)
    u.add_argument("--status", default=None, choices=["todo", "doing", "blocked", "done"])
    u.add_argument("--auto", default=None)
    u.add_argument("--repeatable", default=None)
    u.add_argument("--notes", default=None)
    u.set_defaults(func=cmd_update)

    d = sub.add_parser("done")
    d.add_argument("--id", required=True)
    d.set_defaults(func=cmd_done)

    b = sub.add_parser("block")
    b.add_argument("--id", required=True)
    b.add_argument("--reason", required=True)
    b.set_defaults(func=cmd_block)

    l = sub.add_parser("list")
    l.add_argument("--status", default=None)
    l.set_defaults(func=cmd_list)

    args = ap.parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
