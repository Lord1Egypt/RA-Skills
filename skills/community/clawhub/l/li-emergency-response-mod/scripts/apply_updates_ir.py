#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
企业应急响应指导 Skill - 候选合并器（防污染门禁）

从 ir-patterns.candidates.json 中选取指定 cand-id，合并进 ir-patterns.json（主模式库）。
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Set


ROOT = Path(__file__).resolve().parents[1]
PATTERNS_PATH = ROOT / "memory" / "semantic" / "ir-patterns.json"
CAND_PATH = ROOT / "memory" / "semantic" / "ir-patterns.candidates.json"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Apply IR candidates into main patterns (manual gate)")
    ap.add_argument("--list", action="store_true", help="列出候选 cand-id（不合并）")
    ap.add_argument("--ids", nargs="*", default=[], help="要合并的 cand-id 列表")
    ap.add_argument("--reviewer", default="", help="审核人标识（写入审计字段，可选）")
    args = ap.parse_args()

    cand_obj = load_json(CAND_PATH, {"meta": {}, "candidates": []})
    candidates: List[Dict[str, Any]] = cand_obj.get("candidates") or []

    if args.list or not args.ids:
        print("候选列表（candidates）：")
        for c in candidates:
            print(f"- {c.get('id')}\t{c.get('title')}")
        print("\n使用方式：")
        print("  python3 scripts/apply_updates_ir.py --ids cand-... cand-... --reviewer \"负责人\"")
        return 0

    ids: Set[str] = set(args.ids)
    selected = [c for c in candidates if c.get("id") in ids]
    if not selected:
        print("未找到匹配的 cand-id，先用 --list 查看可用候选。")
        return 2

    patterns_obj = load_json(PATTERNS_PATH, {"meta": {}, "patterns": []})
    patterns: List[Dict[str, Any]] = patterns_obj.get("patterns") or []
    existing_ids = {p.get("id") for p in patterns if isinstance(p, dict)}

    merged = 0
    for c in selected:
        cid = c.get("id")
        if cid in existing_ids:
            continue
        item = dict(c)
        item["review"] = item.get("review") or {}
        item["review"].update(
            {
                "status": "approved",
                "reviewer": args.reviewer or "unknown",
                "reviewed_at": now_iso(),
                "decision": "merge",
            }
        )
        patterns.append(item)
        merged += 1

    patterns_obj["patterns"] = patterns
    patterns_obj["meta"] = patterns_obj.get("meta") or {}
    patterns_obj["meta"]["updated_at"] = now_iso()
    patterns_obj["meta"]["version"] = int(patterns_obj["meta"].get("version") or 1) + 1
    save_json(PATTERNS_PATH, patterns_obj)

    print(f"[ok] merged {merged} candidates into: {PATTERNS_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

