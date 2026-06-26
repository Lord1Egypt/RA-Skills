#!/usr/bin/env python3
"""Milestone Check -- 按里程碑阶段验收产物

里程碑定义：
  P0  初始状态
  P1  需求访谈完成 (requirements-interview.txt)
  P2  资料搜集完成 (search.txt / source-brief.txt)
  P3  大纲生成完成 (outline.txt)
  P3.5 风格锁定 (style.json)
  P4  页面生成完成 (slides/*.html + planning*.json)
  P5  导出完成 (presentation-svg.pptx / presentation-png.pptx)

用法:
  python milestone_check.py OUTPUT_DIR/
  python milestone_check.py OUTPUT_DIR/ --verbose
"""

import argparse
import sys
from pathlib import Path


# -------------------------------------------------------------------
# 里程碑定义
# -------------------------------------------------------------------
MILESTONES = [
    {
        "id": "P0",
        "name": "初始状态",
        "check": lambda d: True,
        "required": False,
    },
    {
        "id": "P1",
        "name": "需求访谈完成",
        "files": ["requirements-interview.txt", "interview-qa.txt"],
        "required": False,
    },
    {
        "id": "P2",
        "name": "资料搜集完成",
        "files": ["search.txt"],
        "required": False,
    },
    {
        "id": "P3",
        "name": "大纲生成完成",
        "files": ["outline.txt", "outline.json"],
        "required": False,
    },
    {
        "id": "P3.5",
        "name": "风格锁定",
        "files": ["style.json"],
        "required": False,
    },
    {
        "id": "P4",
        "name": "页面生成完成",
        "globs": ["slides/slide-*.html", "planning.json"],
        "required": False,
    },
    {
        "id": "P5-SVG",
        "name": "SVG PPTX 导出完成",
        "files": ["presentation-svg.pptx"],
        "required": False,
    },
    {
        "id": "P5-PNG",
        "name": "PNG PPTX 导出完成",
        "files": ["presentation-png.pptx"],
        "required": False,
    },
]


# -------------------------------------------------------------------
# 核心检查逻辑
# -------------------------------------------------------------------
def check_milestone(run_dir: Path, milestone: dict, verbose: bool = False) -> tuple[bool, str]:
    """检查单个里程碑是否达成。"""
    files = milestone.get("files", [])
    globs = milestone.get("globs", [])

    # 检查文件是否存在
    for f in files:
        if (run_dir / f).exists():
            return True, f

    # 检查 glob 模式
    for g in globs:
        matches = list(run_dir.glob(g))
        if g == "slides/slide-*.html" and len(matches) >= 1:
            return True, f"{len(matches)} slide files"
        if g == "planning.json" and (run_dir / g).exists():
            return True, "planning.json"

    return False, ""


def find_current_milestone(run_dir: Path) -> tuple[str, str]:
    """扫描产物目录，找到当前最高里程碑。"""
    for milestone in reversed(MILESTONES):
        if not milestone.get("required", True):
            reached, detail = check_milestone(run_dir, milestone)
            if reached:
                return milestone["id"], detail
    return "P0", ""


def list_all_milestones(run_dir: Path, verbose: bool = False) -> list:
    """列出所有里程碑的状态。"""
    results = []
    for milestone in MILESTONES:
        if milestone["id"] == "P0":
            results.append(("P0", True, "初始状态"))
            continue
        reached, detail = check_milestone(run_dir, milestone, verbose)
        status = f"{milestone['name']} ({detail})" if reached else milestone["name"]
        results.append((milestone["id"], reached, status))
    return results


# -------------------------------------------------------------------
# 主函数
# -------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Milestone Check")
    parser.add_argument("run_dir", type=Path, help="Run output directory")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show details")
    parser.add_argument("--check", help="Check specific milestone (e.g. P3)")
    parser.add_argument("--summary", action="store_true", help="Show summary only")

    args = parser.parse_args()

    if not args.run_dir.exists():
        print(f"ERROR: Directory not found: {args.run_dir}", file=sys.stderr)
        sys.exit(1)

    if args.check:
        milestone = next((m for m in MILESTONES if m["id"] == args.check), None)
        if not milestone:
            print(f"ERROR: Unknown milestone: {args.check}", file=sys.stderr)
            sys.exit(1)
        reached, detail = check_milestone(args.run_dir, milestone, args.verbose)
        if reached:
            print(f"✅ [{milestone['id']}] {milestone['name']} -- {detail}")
            sys.exit(0)
        else:
            print(f"❌ [{milestone['id']}] {milestone['name']} -- NOT REACHED")
            sys.exit(1)

    # 列出所有里程碑
    current_id, current_detail = find_current_milestone(args.run_dir)
    results = list_all_milestones(args.run_dir, args.verbose)

    print(f"\n📍 Run: {args.run_dir}")
    print(f"   Current Milestone: [{current_id}] -- {current_detail}\n")

    if args.summary:
        print(f"{current_id} / P5")
    else:
        for mid, reached, status in results:
            if mid == current_id:
                prefix = "👉"
            elif reached:
                prefix = "✅"
            else:
                prefix = "⬜"
            print(f"  {prefix} [{mid}] {status}")

        # 进度条
        reached_count = sum(1 for r in results if r[1])
        total_count = len([r for r in results if r[0] != "P0"])
        pct = int(reached_count / total_count * 100) if total_count > 0 else 0
        bar = "█" * (pct // 10) + "░" * (10 - pct // 10)
        print(f"\n   Progress: [{bar}] {pct}% ({reached_count}/{total_count})")

    print()
    sys.exit(0)


if __name__ == "__main__":
    main()
