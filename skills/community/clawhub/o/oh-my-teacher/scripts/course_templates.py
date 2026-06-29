#!/usr/bin/env python3
"""Manage course templates for quick-start profiles.

Usage:
  python scripts/course_templates.py list
  python scripts/course_templates.py show "data-structures"
  python scripts/course_templates.py apply "data-structures" [--workspace DIR] [--active]
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

TEMPLATES: dict[str, dict[str, str]] = {
    "advanced-math": {
        "name": "高等数学",
        "subject_family": "mathematics",
        "assessment": "paper exam (closed-book)",
        "level": "shaky",
        "materials": "low-confidence / no syllabus yet",
        "environment": "unknown",
        "weak_points": "[]",
        "completed": "[]",
        "accuracy": '"unknown"',
        "notes": "常规工科/经管高数：极限、连续、导数、一元积分、多元微分、重积分、级数、微分方程；先用 /diagnose 校准章节范围。",
    },
    "data-structures": {
        "name": "数据结构与算法",
        "subject_family": "programming",
        "assessment": "coding exam",
        "level": "shaky",
        "materials": "low-confidence / no syllabus yet",
        "environment": "agent-shell",
        "weak_points": "[]",
        "completed": "[]",
        "accuracy": '"unknown"',
        "notes": "C++ or Java, textbook common curriculum",
    },
    "programming-c-cpp": {
        "name": "程序设计（C/C++）",
        "subject_family": "programming",
        "assessment": "mixed (paper + coding)",
        "level": "shaky",
        "materials": "low-confidence / no syllabus yet",
        "environment": "unknown",
        "weak_points": "[]",
        "completed": "[]",
        "accuracy": '"unknown"',
        "notes": "常规程序设计：变量与类型、分支循环、数组、函数、指针/引用、结构体、文件、基础类与对象；优先练输入输出、边界用例和代码 trace。",
    },
    "digital-logic": {
        "name": "数字电路与逻辑设计",
        "subject_family": "engineering",
        "assessment": "paper exam (closed-book)",
        "level": "shaky",
        "materials": "low-confidence / no syllabus yet",
        "environment": "unknown",
        "weak_points": "[]",
        "completed": "[]",
        "accuracy": '"unknown"',
        "notes": "常规数字逻辑：数制与编码、逻辑门、布尔代数、卡诺图、组合逻辑、触发器、时序逻辑、计数器、寄存器、状态机；优先画真值表、状态图和时序图。",
    },
    "math-analysis": {
        "name": "数学分析 / 高等数学",
        "subject_family": "mathematics",
        "assessment": "paper exam (closed-book)",
        "level": "shaky",
        "materials": "low-confidence / no syllabus yet",
        "environment": "plain-chat",
        "weak_points": "[]",
        "completed": "[]",
        "accuracy": '"unknown"',
        "notes": "同济第七版 or common university syllabus",
    },
    "linear-algebra": {
        "name": "线性代数",
        "subject_family": "mathematics",
        "assessment": "paper exam (closed-book)",
        "level": "shaky",
        "materials": "low-confidence / no syllabus yet",
        "environment": "plain-chat",
        "weak_points": "[]",
        "completed": "[]",
        "accuracy": '"unknown"',
        "notes": "common university syllabus, eigenvalues and SVD likely exam focus",
    },
    "marxism-basic-principles": {
        "name": "马克思主义基本原理",
        "subject_family": "politics",
        "assessment": "paper exam (closed-book / essay)",
        "level": "shaky",
        "materials": "low-confidence / no syllabus yet",
        "environment": "unknown",
        "weak_points": "[]",
        "completed": "[]",
        "accuracy": '"unknown"',
        "notes": "常规思政课：哲学基本问题、唯物论、辩证法、认识论、历史唯物主义、资本主义批判、科学社会主义；优先做概念辨析、简答模板和论述题结构。",
    },
    "computer-networks": {
        "name": "计算机网络",
        "subject_family": "computer science",
        "assessment": "paper exam (closed-book)",
        "level": "shaky",
        "materials": "low-confidence / no syllabus yet",
        "environment": "plain-chat",
        "weak_points": "[]",
        "completed": "[]",
        "accuracy": '"unknown"',
        "notes": "谢希仁第八版 or Top-Down Approach",
    },
    "operating-system": {
        "name": "操作系统",
        "subject_family": "computer science",
        "assessment": "mixed (paper + coding)",
        "level": "shaky",
        "materials": "low-confidence / no syllabus yet",
        "environment": "agent-shell",
        "weak_points": "[]",
        "completed": "[]",
        "accuracy": '"unknown"',
        "notes": "汤子瀛 or modern OS textbook",
    },
    "physics": {
        "name": "大学物理 / 普通物理",
        "subject_family": "physics",
        "assessment": "paper exam (closed-book)",
        "level": "shaky",
        "materials": "low-confidence / no syllabus yet",
        "environment": "unknown",
        "weak_points": "[]",
        "completed": "[]",
        "accuracy": '"unknown"',
        "notes": "常规大学物理：力学、电磁学、热学、振动与波、光学、近代物理；优先做单位检查、受力图、电路/场图和标准题型。",
    },
    "university-physics": {
        "name": "大学物理",
        "subject_family": "physics",
        "assessment": "paper exam (closed-book)",
        "level": "shaky",
        "materials": "low-confidence / no syllabus yet",
        "environment": "plain-chat",
        "weak_points": "[]",
        "completed": "[]",
        "accuracy": '"unknown"',
        "notes": "mechanics, E&M, thermodynamics, optics — common engineering syllabus",
    },
}

SNAPSHOT_TEMPLATE = """## Current Course Snapshot
- **Course**: {name} / {subject_family}
- **Assessment**: {assessment}
- **Days left**: unknown
- **Level**: {level}
- **Environment**: {environment}
- **Materials**: {materials}
- **LaTeX**: not applicable
- **Weak points**: {weak_points}
- **Completed**: {completed}
- **Accuracy**: {accuracy}
- **Last action**: /profile (from template "{template_name}")
- **Next recommended**: /diagnose or tell me more about your exam date and goals

## Additional Notes
{notes}
"""


def cmd_list(args: argparse.Namespace) -> int:
    max_name = max(len(t["name"]) for t in TEMPLATES.values())
    print(f"  {'Name'.ljust(max_name+2)} Key")
    print(f"  {'----'.ljust(max_name+2)} ---")
    for key, tpl in sorted(TEMPLATES.items()):
        print(f"  {tpl['name'].ljust(max_name+2)} {key}")
    print()
    print(f"Total: {len(TEMPLATES)} templates")
    print("Use: python scripts/course_templates.py show <key>")
    print("     python scripts/course_templates.py apply <key> [--active]")
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    tpl = TEMPLATES.get(args.template)
    if not tpl:
        print(f"Template '{args.template}' not found.", file=sys.stderr)
        print(f"Available: {', '.join(sorted(TEMPLATES.keys()))}", file=sys.stderr)
        return 1
    snapshot = SNAPSHOT_TEMPLATE.format(template_name=args.template, **tpl)
    print(snapshot)
    return 0


def cmd_apply(args: argparse.Namespace) -> int:
    tpl = TEMPLATES.get(args.template)
    if not tpl:
        print(f"Template '{args.template}' not found.", file=sys.stderr)
        print(f"Available: {', '.join(sorted(TEMPLATES.keys()))}", file=sys.stderr)
        return 1

    from snapshot import active_path, slugify, snapshot_path, write_state_json  # noqa: E402

    snapshot_text = SNAPSHOT_TEMPLATE.format(template_name=args.template, **tpl)
    slug = slugify(tpl["name"])
    workspace = Path(args.workspace).resolve()
    path = snapshot_path(workspace, slug)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(snapshot_text, encoding="utf-8")
    if args.active:
        active_path(workspace).write_text(slug, encoding="utf-8")
    write_state_json(workspace, snapshot_text, slug, path)
    print(f"Applied template '{args.template}' -> {slug}")
    print(path)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Manage course templates.")
    parser.add_argument("--workspace", default=".", help="Workspace root.")
    sub = parser.add_subparsers(dest="command", required=True)

    list_cmd = sub.add_parser("list", help="List available templates.")
    list_cmd.set_defaults(func=cmd_list)

    show = sub.add_parser("show", help="Show template details as a snapshot.")
    show.add_argument("template")
    show.set_defaults(func=cmd_show)

    apply = sub.add_parser("apply", help="Apply a template (save snapshot).")
    apply.add_argument("template")
    apply.add_argument("--active", action="store_true", help="Set as active course.")
    apply.set_defaults(func=cmd_apply)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
