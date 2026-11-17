#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lis-skill-bus 客户端（纯 stdlib）：供各 SKILL 通过 CLI 读写共享状态。

与 skillbus.py 共享同一份 state.json。客户端仍属于 lis-skill-bus 包；
未注册 MCP 时可直接使用同一包的 CLI，正式识图链路不能绕过 bus。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skillbus as _bus  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="lis-skill-bus 客户端（skill 接线用）")
    ap.add_argument("command", choices=["push", "pull", "list", "resolve", "find-contract", "detect"])
    ap.add_argument("--project", default="", help="项目标识")
    ap.add_argument("--building", default="", help="楼栋（可选）")
    ap.add_argument("--floor", default="", help="楼层（可选）")
    ap.add_argument("--skill", default="unknown", help="来源 skill 名")
    ap.add_argument("--entry-file", default="", help="push 使用的契约 JSON 文件")
    ap.add_argument("--contract", default="", help="resolve 的契约名")
    ap.add_argument("--out", default="", help="pull 输出到文件（可选）")
    ap.add_argument("--entry-id", default="", help="只取指定 entry（默认取 _last 或第一个）")
    ap.add_argument("--source-file", default="", help="find-contract 原始图纸路径")
    ap.add_argument("--source-sha256", default="", help="find-contract sha256（可选）")
    ap.add_argument("--skill-dir", default="", help="detect 的目录")
    args = ap.parse_args()

    if args.command == "push":
        if not args.entry_file:
            print(json.dumps({"error": "需要 --entry-file"}, ensure_ascii=False), file=sys.stderr)
            return 2
        entry = json.loads(Path(args.entry_file).read_text(encoding="utf-8"))
        r = _bus.push_project_state(args.project, entry, args.building, args.floor,
                                    source_skill=args.skill)
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0

    if args.command == "pull":
        r = _bus.get_project_state(args.project, args.building, args.floor)
        entries = r["entries"]
        if args.entry_id:
            e = entries.get(args.entry_id)
            if e is None:
                print(json.dumps({"project_key": r["project_key"], "hit": False,
                                  "reason": f"entry {args.entry_id!r} 未命中"}, ensure_ascii=False, indent=2))
                return 0
            picked = e
        else:
            picked = entries.get("_last") or next(iter(entries.values()), None)
        if picked is None:
            print(json.dumps({"project_key": r["project_key"], "hit": False,
                              "reason": "无共享状态（未命中）"}, ensure_ascii=False, indent=2))
            return 0
        if args.out:
            Path(args.out).write_text(json.dumps(picked, ensure_ascii=False, indent=2), encoding="utf-8")
        print(json.dumps({"project_key": r["project_key"], "hit": True,
                          "entry": picked}, ensure_ascii=False, indent=2))
        return 0

    if args.command == "list":
        print(json.dumps(_bus.list_skills(), ensure_ascii=False, indent=2))
        return 0

    if args.command == "resolve":
        print(json.dumps(_bus.resolve_contract(args.contract), ensure_ascii=False, indent=2))
        return 0

    if args.command == "find-contract":
        print(json.dumps(_bus.find_contract(args.project, args.building, args.floor,
                                            args.source_file, args.source_sha256),
                         ensure_ascii=False, indent=2))
        return 0

    if args.command == "detect":
        print(json.dumps(_bus.detect_skill(args.skill_dir or _bus.DEFAULT_SKILLS_DIR),
                         ensure_ascii=False, indent=2))
        return 0

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
