#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""给项目追加一条「过程记录」，并同步状态与登记表。

用法：
  python3 scripts/log_step.py assets/output/MV01-xxx \
    --station "①" --role "任务解读官" \
    --output "01-解读/01-任务书.md" \
    --decision "用户授权按默认值执行；30s；无音频先写词" \
    --pending "母题待确认"

  # 可选：
  #   --input "用户原话摘要 / 附件名"
  #   --next "② 出方案"
  #   --status "▶进行中"（默认 ⏸待确认）
  #   --step-label "① 解读任务"（写进状态文件与登记表；默认 = station + role 去掉「官」）

行为：
  1. 追加 `00-过程记录.md`：站/角色/输入/产出/决策/待确认/下一步；
  2. 更新 `00-项目状态.md` 的【当前步骤】【最近更新】【用户最近意见】；
  3. 更新 `assets/output/项目登记.md` 对应行的「当前步骤」「状态」。
"""
from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import OUTPUT_ROOT, resolve_project  # noqa: E402

STATIONS = [
    ("⓪", "建档"),
    ("①", "解读任务"),
    ("②", "出方案"),
    ("③", "写钩子句"),
    ("④", "写歌词"),
    ("⑤", "素材与出曲"),
    ("⑥", "上传外网"),
    ("⑦", "时间轴与提示词"),
    ("⑧", "出片合成"),
    ("⑨", "质检交付"),
]


def append_record(project: Path, args: argparse.Namespace, now: str) -> Path:
    path = project / "00-过程记录.md"
    if not path.is_file():
        path.write_text(
            f"# 过程记录 · {project.name}\n\n"
            "> 每站一块，由 `scripts/log_step.py` 追加。换会话继续时，先读最后一块。\n",
            encoding="utf-8",
        )
    block = [
        "",
        f"## {args.station} {args.step_label} · {now}",
        f"- 角色：{args.role}",
        f"- 输入：{args.input or '—'}",
        f"- 产出：{args.output or '—'}",
        f"- 关键决策：{args.decision or '—'}",
        f"- 待确认：{args.pending or '—'}",
        f"- 下一步：{args.next or '—'}",
        "",
    ]
    with path.open("a", encoding="utf-8") as f:
        f.write("\n".join(block))
    return path


def update_state(project: Path, args: argparse.Namespace, now: str) -> Path | None:
    path = project / "00-项目状态.md"
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    label = f"{args.station} {args.step_label}"

    idx = next((i for i, (s, _) in enumerate(STATIONS) if s == args.station), -1)
    if idx >= 0:
        done = " ".join(f"{s} {name} ✅" for s, name in STATIONS[: idx + 1])
        todo = " → ".join(f"{s} {name}" for s, name in STATIONS[idx + 1:]) or "无（已交付）"
        text = re.sub(
            r"【已完成】.*?(?=\n【待执行】)",
            f"【已完成】{done}",
            text,
            count=1,
            flags=re.S,
        )
        text = re.sub(
            r"【待执行】.*?(?=\n【最近更新】)",
            f"【待执行】{todo}",
            text,
            count=1,
            flags=re.S,
        )

    text = re.sub(r"【当前步骤】.*", f"【当前步骤】{label}（{args.pending or '等待用户确认'}）", text, count=1)
    text = re.sub(r"【最近更新】.*", f"【最近更新】{now}", text, count=1)
    if args.pending:
        text = re.sub(r"【用户最近意见】.*", f"【用户最近意见】{args.pending}", text, count=1)
    path.write_text(text, encoding="utf-8")
    return path


def update_registry(project: Path, args: argparse.Namespace) -> Path | None:
    path = OUTPUT_ROOT / "项目登记.md"
    if not path.is_file():
        return None
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    out = []
    hit = False
    for line in lines:
        if project.name in line and line.lstrip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if len(cells) >= 6:
                cells[3] = f"{args.station} {args.step_label}"
                cells[4] = args.status
                line = "| " + " | ".join(cells) + " |\n"
                hit = True
        out.append(line)
    if hit:
        path.write_text("".join(out), encoding="utf-8")
    return path if hit else None


def main() -> None:
    ap = argparse.ArgumentParser(description="追加一条项目过程记录")
    ap.add_argument("project", help="项目目录 / 项目名（如 MV01-xxx）")
    ap.add_argument("--station", required=True, help="站号，如 ① / ② / ⑦")
    ap.add_argument("--role", required=True, help="角色名，如 任务解读官")
    ap.add_argument("--output", default="", help="本站产出文件（相对项目根）")
    ap.add_argument("--input", default="", help="本站输入（用户原话摘要/附件）")
    ap.add_argument("--decision", default="", help="关键决策")
    ap.add_argument("--pending", default="", help="待确认事项")
    ap.add_argument("--next", default="", help="下一步")
    ap.add_argument("--step-label", default="", help="状态文件里的步骤名，默认由角色推导")
    ap.add_argument("--status", default="⏸待确认", help="登记表状态（默认 ⏸待确认）")
    args = ap.parse_args()

    project = resolve_project(args.project)
    args.step_label = args.step_label or args.role.replace("官", "").strip() or args.role
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    record = append_record(project, args, now)
    state = update_state(project, args, now)
    reg = update_registry(project, args)

    print(f"[OK] 过程记录已追加：{record}")
    if state:
        print(f"     状态已更新：{state}")
    if reg:
        print(f"     登记表已更新：{reg}")
    print(f"     {args.station} {args.step_label} · {args.role} · {now}")


if __name__ == "__main__":
    main()
