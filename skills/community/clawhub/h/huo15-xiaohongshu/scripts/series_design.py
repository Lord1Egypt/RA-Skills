#!/usr/bin/env python3
"""火一五小红书"栏目化设计 + 互动阶梯" — Allen 待修炼方向之一。

Allen 教训
==========
- 单次活动 → **可持续的内容 IP**（"周三存档"、"尽兴放映厅"、"尽兴请回答"）
- 互动是**邀请阶梯**，不是任务清单：
    关注 → 评论 → 发图 → 被收录 → 带走大礼
- 「不是收，是开」 — 一个灵感能延伸出多少种可能性

输出
====
1. 5~8 个栏目名候选（按风格分类）
2. 配套的互动阶梯设计（5 级）
3. 12 个月节奏建议（怎么把单次变成长期 IP）

用法
----

    python3 series_design.py --theme "尽兴" --persona "30+ 都市女性"
    python3 series_design.py --theme "下班后" --persona "互联网打工人" --n 8
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List

sys.path.insert(0, str(Path(__file__).parent))


# ---------- 栏目名模板 ----------


_SERIES_TEMPLATES = {
    "时间型（强韵律）": [
        "{theme}周三存档",
        "{theme}周日小记",
        "{theme}月初剪贴簿",
        "{theme}月末复盘册",
        "周一{theme}信",
    ],
    "动作型（轻量）": [
        "{theme}请回答",
        "{theme}小练习",
        "{theme}笔记本",
        "{theme}打开方式",
        "{theme}收录册",
    ],
    "形式型（包装）": [
        "{theme}图鉴",
        "{theme}指南",
        "{theme}百宝书",
        "{theme}白皮书",
        "{theme}小词典",
    ],
    "活动型（高门槛）": [
        "{theme}放映厅",
        "{theme}电台",
        "{theme}市集",
        "{theme}季报",
        "{theme}年鉴",
    ],
    "情绪型（共鸣）": [
        "{theme}的瞬间",
        "{theme}时刻",
        "{theme}清单",
        "{theme}存档",
        "{theme}地图",
    ],
}


def generate_series_names(theme: str, n: int = 8) -> List[Dict[str, str]]:
    out: List[Dict[str, str]] = []
    for category, templates in _SERIES_TEMPLATES.items():
        for t in templates[:2]:
            out.append({
                "name": t.format(theme=theme),
                "category": category,
            })
    return out[:n]


# ---------- 互动阶梯 ----------


_LADDER_TEMPLATE = [
    {
        "level": 1,
        "name": "关注（最低门槛）",
        "invitation_pattern": "如果你也喜欢这种感觉",
        "for_reader": "几乎零成本，只是举一下手",
        "drives": "持续看到你的下一篇",
    },
    {
        "level": 2,
        "name": "评论（自我表达）",
        "invitation_pattern": "你呢？/ 你那一天是怎样的？",
        "for_reader": "把自己的故事说出来一点",
        "drives": "归属感 — 这是个能聊的地方",
    },
    {
        "level": 3,
        "name": "发图 / 发笔记（参与共创）",
        "invitation_pattern": "拍一张你自己的 X，在我这里留个落脚点",
        "for_reader": "贡献内容，参与品牌叙事",
        "drives": "我的作品也是这个故事的一部分",
    },
    {
        "level": 4,
        "name": "被收录（被认可）",
        "invitation_pattern": "我会精选 N 篇放到下一期",
        "for_reader": "得到肯定 / 被看见",
        "drives": "我没白发，我被认真对待",
    },
    {
        "level": 5,
        "name": "带走大礼（实物）",
        "invitation_pattern": "前 N 名收录者，会有 X 寄到家里",
        "for_reader": "实体感、仪式感",
        "drives": "故事到真实生活的延伸",
    },
]


def build_ladder(theme: str, persona: str = "") -> List[Dict[str, str]]:
    """根据主题填充邀请语模板。"""
    out = []
    for step in _LADDER_TEMPLATE:
        s = dict(step)
        s["invitation_pattern"] = s["invitation_pattern"].replace(
            "X", theme).replace("Y", persona or "你的故事")
        out.append(s)
    return out


# ---------- 12 个月节奏 ----------


def yearly_cadence(theme: str) -> List[Dict[str, str]]:
    """把单次栏目变成长期 IP 的 12 个月节奏建议。"""
    return [
        {"month": "M1-M3 启动期", "task": f"每周固定一次「{theme}」相关笔记，找到稳定钩子"},
        {"month": "M2-M4 召集期", "task": "首篇正式栏目化笔记，给出明确互动阶梯（1~3 级）"},
        {"month": "M3-M5 收录期", "task": "每月一次精选收录帖（Level 4），给读者被看见的位置"},
        {"month": "M4-M6 实物期", "task": "做一次小实物联动（明信片/书签/贴纸），升 Level 5"},
        {"month": "M6-M7 借势期", "task": "结合一个节气 / 节日（参考 seasonal_themes.md）做主题季"},
        {"month": "M7-M9 联动期", "task": "邀 1~2 个相邻 IP 联动（KOL / 兄弟品牌），扩圈"},
        {"month": "M9-M10 沉淀期", "task": "把过去 9 个月的精华做成栏目'白皮书 / 年鉴'，沉淀"},
        {"month": "M10-M12 跨界期", "task": "把栏目从内容延伸到实物 / 服务 / 周边"},
    ]


# ---------- 渲染 ----------


def render_text(theme: str, persona: str, names: List, ladder: List, cadence: List) -> str:
    parts = []
    parts.append(f"📚 「{theme}」栏目化设计")
    if persona:
        parts.append(f"   面向：{persona}")
    parts.append("")

    parts.append("=" * 60)
    parts.append("一、栏目名候选\n")
    by_cat: Dict[str, List[str]] = {}
    for n in names:
        by_cat.setdefault(n["category"], []).append(n["name"])
    for cat, items in by_cat.items():
        parts.append(f"  {cat}:")
        for it in items:
            parts.append(f"    • {it}")
        parts.append("")

    parts.append("=" * 60)
    parts.append("二、互动阶梯（5 级）\n")
    for step in ladder:
        parts.append(f"  Level {step['level']}: {step['name']}")
        parts.append(f"     邀请语模板：{step['invitation_pattern']}")
        parts.append(f"     读者得到  ：{step['for_reader']}")
        parts.append(f"     驱动情绪  ：{step['drives']}")
        parts.append("")

    parts.append("=" * 60)
    parts.append("三、12 个月节奏\n")
    for c in cadence:
        parts.append(f"  • {c['month']}：{c['task']}")
    parts.append("")

    parts.append("─" * 60)
    parts.append("Allen 提醒：")
    parts.append("  • 不是收，是开 — 栏目是延展性的容器，不是收尾的圈")
    parts.append("  • 一个灵感的真正价值不在它本身有多好，在它能延伸出多少新的可能性")
    parts.append("  • 互动阶梯每一级都要有'读者为什么会做'的情绪驱动力，不是命令")
    return "\n".join(parts)


def main() -> int:
    p = argparse.ArgumentParser(prog="series_design.py", description="栏目化 + 互动阶梯")
    p.add_argument("--theme", required=True, help="主题词，如：尽兴 / 下班后 / 早八")
    p.add_argument("--persona", default="", help="目标读者画像")
    p.add_argument("--n", type=int, default=8, help="栏目名候选数")
    p.add_argument("--format", choices=["text", "json"], default="text")
    args = p.parse_args()

    names = generate_series_names(args.theme, args.n)
    ladder = build_ladder(args.theme, args.persona)
    cadence = yearly_cadence(args.theme)

    if args.format == "json":
        print(json.dumps({
            "theme": args.theme, "persona": args.persona,
            "names": names, "ladder": ladder, "cadence": cadence,
        }, ensure_ascii=False, indent=2))
    else:
        print(render_text(args.theme, args.persona, names, ladder, cadence))
    return 0


if __name__ == "__main__":
    sys.exit(main())
