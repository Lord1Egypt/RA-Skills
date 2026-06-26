#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Append a progress event to memory/events_YYYY-MM-DD.jsonl."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

from _config import load_config


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", default="event")
    ap.add_argument("--msg", required=True)
    args = ap.parse_args()

    cfg = load_config()
    memdir = Path(cfg["memory_dir"])
    memdir.mkdir(parents=True, exist_ok=True)

    day = datetime.now().strftime("%Y-%m-%d")
    path = memdir / f"events_{day}.jsonl"

    ev = {"ts": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "kind": args.kind, "msg": args.msg}
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")

    print(f"OK appended {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
