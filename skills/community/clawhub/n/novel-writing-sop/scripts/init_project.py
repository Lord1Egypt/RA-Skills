#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""初始化一个网文项目目录骨架。

用法：python scripts/init_project.py <小说名> [根目录]
默认根目录为当前工作目录。
"""
from __future__ import annotations

import datetime
import sys
from pathlib import Path

TEMPLATES = {
    "1-选题.txt": "# 选题\n\n## 书名\n（15 字内，含标点）\n\n## 简介（≤150 字）\n\n## 核心卖点\n\n## 目标受众\n\n## 差异化\n",
    "2-核心设定.txt": "# 核心设定 + 人物群像\n\n## 一、世界观\n\n## 二、力量体系\n\n## 三、核心悬念\n\n## 四、主角档案\n\n## 五、重要角色（3-5 人）\n\n## 六、反派档案（2-3 人）\n",
    "3-标签简介.txt": "# 标签 + 黄金简介\n\n## 作品标签（6-8 个）\n\n## 黄金简介（500 字，含黄金三句式）\n",
    "4-分卷大纲.txt": "# 五卷框架\n\n### 第一卷：启程\n- 核心主题：\n- 章节范围：\n- 关键事件：\n- 结尾悬念：\n\n### 第二卷：初露锋芒\n\n### 第三卷：风云激荡\n\n### 第四卷：强者之路\n\n### 第五卷：巅峰对决\n",
    "6-节奏控制.txt": "# 升级节奏 + 情绪节奏 + 爽点分布\n\n## 等级-卷数对照\n\n## 情绪周期\n\n## 日常/打斗比例\n\n## 打脸节奏模型\n",
    "6-执行附录.txt": "# 伏笔 + 道具 + 进度追踪\n\n## 伏笔清单\n\n## 道具清单\n\n## 世界观补充\n\n## 创作进度\n\n## 变更记录\n",
}

HELP_FLAGS = {"-h", "--help", "help"}


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in HELP_FLAGS:
        print("用法: python init_project.py <小说名> [根目录]")
        print("示例: python init_project.py 凤还朝阳 ./novels")
        return 0 if args and args[0] in HELP_FLAGS else 1

    name = args[0].strip()
    if not name or name.startswith("-"):
        print("小说名不能为空，也不能以 - 开头（避免把 --help 当成书名）")
        return 1

    root = Path(args[1]).expanduser().resolve() if len(args) > 1 else Path.cwd()
    proj = root / name
    if proj.exists() and any(proj.iterdir()):
        print(f"[WARN] {proj} 已存在且非空，跳过")
        return 2

    proj.mkdir(parents=True, exist_ok=True)
    (proj / "素材").mkdir(exist_ok=True)
    for fname, content in TEMPLATES.items():
        (proj / fname).write_text(content, encoding="utf-8")

    (proj / "README.md").write_text(
        f"# {name}\n\n初始化时间：{datetime.datetime.now():%Y-%m-%d %H:%M}\n\n"
        "按 novel-writing-sop 三模式推进：\n"
        "1. 快速：填 1-选题迷你版 → 写第1章\n"
        "2. 标准：完成 6 个大纲文档\n"
        "3. 量产：5 章一批 + 三审\n",
        encoding="utf-8",
    )
    print(f"[OK] 已创建 {proj}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
