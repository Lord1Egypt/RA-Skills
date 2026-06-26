#!/usr/bin/env python3
"""文件完整性校验：检测损坏文件并修复"""

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.filelock import safe_read, safe_write_json, safe_read_json

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
CHECKSUM_FILE = ".checksums.json"


def compute_checksum(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def load_checksums(memory_dir: Path) -> dict:
    fp = memory_dir / CHECKSUM_FILE
    if fp.exists():
        return safe_read_json(fp)
    return {}


def save_checksums(memory_dir: Path, checksums: dict):
    safe_write_json(memory_dir / CHECKSUM_FILE, checksums)


def validate_all(memory_dir: Path, fix: bool = False) -> dict:
    """校验所有记忆文件"""
    checksums = load_checksums(memory_dir)
    report = {
        "valid": [],
        "corrupted": [],
        "new": [],
        "modified": [],
        "missing": [],
        "fixed": [],
    }

    # 收集所有 md 文件
    all_files = []
    for subdir in ["conversations", "summaries", "distillations"]:
        d = memory_dir / subdir
        if d.exists():
            for fp in d.glob("*.md"):
                all_files.append(fp)

    # 检查每个文件
    for fp in sorted(all_files):
        rel = str(fp.relative_to(memory_dir))
        
        if not fp.exists():
            report["missing"].append(rel)
            continue

        try:
            content = fp.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            report["corrupted"].append({"file": rel, "error": "编码错误"})
            if fix:
                fix_encoding(fp)
                report["fixed"].append(rel)
            continue
        except Exception as e:
            report["corrupted"].append({"file": rel, "error": str(e)})
            continue

        # 检查基本结构
        if fp.parent.name == "conversations":
            if not content.strip().startswith("#"):
                report["corrupted"].append({"file": rel, "error": "缺少标题行"})
                if fix:
                    fix_missing_title(fp, fp.stem)
                    report["fixed"].append(rel)
                continue

        # 检查校验和
        current_hash = compute_checksum(content)
        if rel not in checksums:
            report["new"].append(rel)
            checksums[rel] = {
                "hash": current_hash,
                "size": len(content),
                "checked": datetime.now().isoformat(),
            }
        elif checksums[rel]["hash"] != current_hash:
            report["modified"].append({
                "file": rel,
                "old_hash": checksums[rel]["hash"],
                "new_hash": current_hash,
            })
            checksums[rel] = {
                "hash": current_hash,
                "size": len(content),
                "checked": datetime.now().isoformat(),
            }
        else:
            report["valid"].append(rel)

    # 检查已记录但文件不存在的
    for rel in checksums:
        if not (memory_dir / rel).exists():
            report["missing"].append(rel)

    # 保存更新后的校验和
    save_checksums(memory_dir, checksums)

    return report


def fix_encoding(fp: Path):
    """尝试修复编码问题"""
    try:
        raw = fp.read_bytes()
        # 尝试 latin-1
        content = raw.decode("latin-1")
        # 修复常见的编码错误
        content = content.encode("latin-1").decode("utf-8", errors="replace")
        fp.write_text(content, encoding="utf-8")
        print(f"  🔧 修复编码: {fp.name}")
    except Exception as e:
        print(f"  ❌ 无法修复: {fp.name}: {e}")


def fix_missing_title(fp: Path, date_str: str):
    """修复缺少标题的文件"""
    content = fp.read_text(encoding="utf-8")
    fp.write_text(f"# {date_str} 对话记录\n{content}", encoding="utf-8")
    print(f"  🔧 修复标题: {fp.name}")


def print_report(report: dict):
    total = (len(report["valid"]) + len(report["corrupted"]) + 
             len(report["new"]) + len(report["modified"]) + len(report["missing"]))
    
    print("=" * 60)
    print(f"🔍 文件完整性校验（{total} 个文件）")
    print("=" * 60)
    print(f"\n  ✅ 正常: {len(report['valid'])}")
    print(f"  🆕 新增: {len(report['new'])}")
    print(f"  ✏️  变更: {len(report['modified'])}")

    if report["corrupted"]:
        print(f"\n  🔴 损坏: {len(report['corrupted'])}")
        for item in report["corrupted"]:
            print(f"     {item['file'] if isinstance(item, dict) else item}: "
                  f"{item.get('error', '未知') if isinstance(item, dict) else '未知'}")

    if report["missing"]:
        print(f"\n  ❓ 缺失: {len(report['missing'])}")
        for item in report["missing"]:
            print(f"     {item}")

    if report["fixed"]:
        print(f"\n  🔧 已修复: {len(report['fixed'])}")
        for item in report["fixed"]:
            print(f"     {item}")

    healthy = len(report["corrupted"]) == 0 and len(report["missing"]) == 0
    print(f"\n  {'✅ 系统健康' if healthy else '⚠️ 需要关注'}")


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="文件完整性校验")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--fix", action="store_true", help="自动修复")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)

    report = validate_all(md, fix=args.fix)

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_report(report)
