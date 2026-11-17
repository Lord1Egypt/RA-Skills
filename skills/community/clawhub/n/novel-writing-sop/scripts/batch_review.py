#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""每批 5 章写完后的门禁检查 + 三审提醒清单。

用法：python scripts/batch_review.py <项目目录> <起始章号>
起始章号 N，则本批为 N ~ N+4。

说明：
- 检查正文是否存在、中文字数是否 ≥2500
- 输出编剧审 / 读者审 / 去 AI 腔清单
- 不做模型打分（打分由 Agent 按 SKILL.md 评分卡完成）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

MIN_CHARS = 2500
HELP_FLAGS = {"-h", "--help", "help"}


def count_body(text: str) -> int:
    """去除标题行与【本章完】标记后统计中文字符数。"""
    lines = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if re.match(r"^第[一二三四五六七八九十百千0-9]+章", s):
            continue
        if s in ("【本章完】", "本章完"):
            continue
        lines.append(line)
    body = "\n".join(lines)
    return len(re.findall(r"[\u4e00-\u9fff]", body))


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in HELP_FLAGS or len(args) < 2:
        print("用法: python batch_review.py <项目目录> <起始章号>")
        print("示例: python batch_review.py ./凤还朝阳 1")
        return 0 if args and args[0] in HELP_FLAGS else 1

    root = Path(args[0]).expanduser().resolve()
    try:
        start = int(args[1])
    except ValueError:
        print("起始章号必须是整数")
        return 1

    if not root.exists():
        print(f"[ERR] 项目目录不存在: {root}")
        return 1

    chapters = list(range(start, start + 5))
    print(f"=== 批次审核门禁检查：第 {chapters[0]}-{chapters[-1]} 章 ===\n")

    missing: list[int] = []
    short: list[tuple[int, int]] = []
    for n in chapters:
        p = root / f"8-正文-第{n}章.txt"
        if not p.exists():
            missing.append(n)
            print(f"  ✗ 第{n}章：缺失 {p.name}")
            continue
        text = p.read_text(encoding="utf-8")
        wc = count_body(text)
        ok = wc >= MIN_CHARS
        print(f"  {'✓' if ok else '✗'} 第{n}章：{wc} 字" + ("" if ok else " (不足，需扩)"))
        if not ok:
            short.append((n, wc))

    if missing:
        print(f"\n[WARN] 缺失文件：第{missing}章")

    print("\n--- 编剧审（100 分制 ≥80）---")
    print("  □ 剧情连贯性 30：与大纲一致、前后衔接、逻辑通")
    print("  □ 内容质量   30：人物合理、对话自然、描写到位")
    print("  □ 字数要求   20：≥2500、无注水")
    print("  □ 节奏可读性 20：爽点分布、钩子设置、张弛有度")

    print("\n--- 读者审（100 分制 ≥80）---")
    print("  □ 故事连贯性 25：5 章成完整小故事、衔接自然")
    print("  □ 吸引力与可读性 25：节奏悬念钩子")
    print("  □ 爽点密度 25：类型多样、节奏匀")
    print("  □ 剧情 Bug 检测 25：设定矛盾、人设崩坏、时间线错误")

    print("\n--- 去 AI 腔过滤（50 分制 ≥38）---")
    print("  □ 直接性 / 干净度 / 真实感 / 动作化 / 具体性 各 10 分")
    print("  □ 重点扫：不是…而是… / 值得注意的是 / 突然忽然 / 心中一凛 /")
    print("    身形一闪 / 非常十分极其 / 一排数据流 / 瞳孔一缩")

    print("\n--- 通过条件 ---")
    print("  编剧审 ≥80 且 读者审 ≥80 且 去 AI 腔 ≥38 → 进入下一批")
    print("  任一不达标 → 修改模式重审")
    print("  评分由 Agent 按 SKILL.md 内嵌评分卡完成；本脚本只做字数/文件门禁")

    return 0 if not missing and not short else 2


if __name__ == "__main__":
    raise SystemExit(main())
