#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Love Companion v1 → v2 数据迁移（M0 交付物）

做什么：
1. 把 v1 的 memory.json（条目只有 id/content/created_at）补齐为 v2 六类记忆结构
2. 生成 v2 新增文件：settings.json（不存在时按模板生成）
3. 全程**不删除、不改写原文件**：先整目录备份，再写目标文件

为什么可以放心跑：
v2 的记忆结构是 v1 的**超集**——id / content / created_at 原样保留，
只追加 type / importance / 召回计数等元数据。因此：
- v1 的 manager.py 仍能正常读取迁移后的 memory.json（向下兼容）
- 迁移出问题时直接用备份目录覆盖回去即可（可回退）

用法：
    python scripts/migrate/migrate_v1.py --data-dir ~/.love-companion/data
    python scripts/migrate/migrate_v1.py --data-dir <路径> --dry-run   # 只预演不落盘
"""

import argparse
import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# 让 `scripts.core.schema` 可被导入（直接运行本脚本时 sys.path[0] 是脚本所在目录）
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.core import schema  # noqa: E402


def _read_json(path: Path, default):
    if not path.exists():
        return default
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _write_json(path: Path, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def backup(data_dir: Path, dry_run: bool) -> Optional[Path]:
    """整目录备份到 <data_dir>/backup_v1_<时间戳>/"""
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = data_dir / f"backup_v1_{stamp}"
    if dry_run:
        return target
    if data_dir.exists():
        shutil.copytree(data_dir, target, ignore=shutil.ignore_patterns("backup_v1_*"))
    return target


def migrate_memories(memories) -> list:
    """把记忆列表（v1 或 v2 混排）统一为 v2 结构"""
    if not isinstance(memories, list):
        raise ValueError(f"memory.json 结构异常：期望 list，实际 {type(memories).__name__}")
    result = []
    for idx, entry in enumerate(memories, 1):
        normalized = schema.normalize_memory_entry(entry, entry_id=idx)
        normalized["id"] = idx
        result.append(normalized)
    return result


def run(data_dir: Path, dry_run: bool = False) -> dict:
    data_dir = Path(os.path.expanduser(str(data_dir)))
    report = {
        "data_dir": str(data_dir),
        "dry_run": dry_run,
        "backup": None,
        "memory_before": 0,
        "memory_after": 0,
        "v1_entries": 0,
        "created_settings": False,
        "errors": [],
    }

    if not data_dir.exists():
        report["errors"].append(f"数据目录不存在：{data_dir}（若从未启用过，可直接跳过迁移）")
        return report

    memories_path = data_dir / "memory.json"
    settings_path = data_dir / "settings.json"

    old_memories = _read_json(memories_path, [])
    report["memory_before"] = len(old_memories) if isinstance(old_memories, list) else 0
    report["v1_entries"] = sum(
        1 for m in old_memories if isinstance(m, dict) and schema.is_v1_memory_entry(m)
    )

    try:
        new_memories = migrate_memories(old_memories)
    except Exception as exc:  # noqa: BLE001
        report["errors"].append(f"记忆迁移失败：{exc}")
        return report
    report["memory_after"] = len(new_memories)

    if dry_run:
        return report

    report["backup"] = str(backup(data_dir, dry_run=False))

    if memories_path.exists():
        _write_json(memories_path, new_memories)

    if not settings_path.exists():
        _write_json(settings_path, schema.settings_template())
        report["created_settings"] = True

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Love Companion v1 → v2 数据迁移")
    parser.add_argument(
        "--data-dir",
        default=os.environ.get("LOVE_COMPANION_DATA_DIR", "~/.love-companion/data"),
        help="数据目录，默认 ~/.love-companion/data",
    )
    parser.add_argument("--dry-run", action="store_true", help="只预演，不写盘")
    args = parser.parse_args()

    report = run(Path(args.data_dir), dry_run=args.dry_run)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
