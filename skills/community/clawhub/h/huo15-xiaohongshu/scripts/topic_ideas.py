#!/usr/bin/env python3
"""火一五小红书选题灵感生成器。

工作模式
========
1. 输入：种子关键词 + （可选）已抓取的同行笔记数据集 (.json/.jsonl)。
2. 处理：从数据集里提取爆款笔记的高频关键词 + 话题标签 + 标题模式。
3. 输出：N 条"标题 + 角度 + 推荐骨架 + 推荐话题"的选题清单。

如果不传数据集，就只用内置的 11 种标题公式 + 通用角度组合，给出种子选题。

用法
----

    # 基于已抓取的笔记数据生成选题
    python3 topic_ideas.py --seed "干皮护肤" --notes notes.jsonl --n 10

    # 没数据，只靠公式
    python3 topic_ideas.py --seed "干皮护肤" --persona "30+ 干皮女生" --n 10

    # 输出 markdown 报告
    python3 topic_ideas.py --seed "副业" --notes notes.jsonl --format md --out ideas.md
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))

from xhs_analyzer import keyword_frequency, load_notes, tag_frequency, top_notes  # noqa: E402
from xhs_writer import generate_titles  # noqa: E402

# ---------- 角度（与公式正交的"内容方向"） ----------

_ANGLES = [
    ("误区纠正", "大多数人 X 是错的，正确做法是 Y", "S6"),
    ("入门 SOP", "从零做 X 的 5 个步骤", "S5"),
    ("产品对比", "X 类目里 3 款值得买的", "S3"),
    ("时间维度", "X 这件事，3 天/30 天/3 个月分别是什么样", "S1"),
    ("身份代入", "作为 Y，做 X 我有 5 句心里话", "S2"),
    ("反面避雷", "X 这件事，最坑的 3 个错", "S1"),
    ("清单整理", "X 相关的 7 个工具/资源/技巧", "S4"),
    ("自我经历", "我做 X 的 30 天，发生了什么", "S2"),
    ("反共识", "我有个不太主流的看法 — 关于 X", "S6"),
    ("场景代入", "X 这一刻的细节，我记了下来", "S7"),
]


def derive_personas(notes: List[Dict[str, Any]]) -> List[str]:
    """从抓的爆款笔记里粗略提取受众身份词（出现 >= 2 次的）。"""
    if not notes:
        return []
    candidates = ["女生", "男生", "学生", "职场", "宝妈", "30+", "30 岁", "新手",
                  "小白", "干皮", "油皮", "敏感肌", "微胖", "小个子", "梨形",
                  "i 人", "e 人", "内向", "副业", "上班族", "自由职业"]
    hits = {}
    for n in notes:
        blob = (n.get("title", "") or "") + (n.get("content", "") or "")
        for c in candidates:
            if c in blob:
                hits[c] = hits.get(c, 0) + 1
    return [k for k, v in sorted(hits.items(), key=lambda x: -x[1]) if v >= 2][:5]


def gather_signals(notes_path: str) -> Dict[str, Any]:
    """从抓取的数据集中提取选题信号。"""
    notes = load_notes(notes_path)
    return {
        "sample_size": len(notes),
        "keywords": keyword_frequency(notes, top=30),
        "tags": tag_frequency(notes, top=20),
        "top_notes": top_notes(notes, 5),
        "personas": derive_personas(notes),
    }


def build_ideas(
    seed: str,
    n: int = 10,
    *,
    persona: str = "",
    payoff: str = "",
    signals: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """生成选题清单。"""
    ideas: List[Dict[str, Any]] = []

    # 优先用数据集里挖出来的受众词
    personas: List[str] = []
    if persona:
        personas.append(persona)
    if signals:
        personas += [p for p in signals.get("personas", []) if p not in personas]
    if not personas:
        personas = ["", "新手", "30+"]

    # 推荐话题：seed + 数据集里 top 5 标签
    tag_pool = [seed]
    if signals:
        for tag, _cnt in signals.get("tags", [])[:5]:
            if tag not in tag_pool:
                tag_pool.append(tag)

    # 角度 × 公式 交叉，挑前 n 个
    formulas = ["T2", "T1", "T3", "T5", "T10", "T8", "T6", "T11"]
    pairs = [(angle, formulas[i % len(formulas)]) for i, angle in enumerate(_ANGLES)]

    for i, (angle, formula) in enumerate(pairs):
        if len(ideas) >= n:
            break
        p = personas[i % len(personas)] if personas else ""
        titles = generate_titles(seed, persona=p, payoff=payoff, formulas=[formula], n_each=1)
        if not titles:
            continue
        skeleton = angle[2]
        ideas.append({
            "idea_no": len(ideas) + 1,
            "angle": angle[0],
            "angle_hint": angle[1].replace("X", seed).replace("Y", p or "你"),
            "title": titles[0]["title"],
            "formula": formula,
            "skeleton": skeleton,
            "tags": tag_pool[:5],
        })

    return ideas


def render_markdown(seed: str, ideas: List[Dict[str, Any]], signals: Optional[Dict[str, Any]]) -> str:
    parts = [f"# 「{seed}」选题清单（{len(ideas)} 条）", ""]
    if signals:
        parts.append(f"_基于 {signals['sample_size']} 条同行笔记数据_")
        if signals.get("personas"):
            parts.append(f"- 高频受众：{', '.join(signals['personas'])}")
        if signals.get("tags"):
            top_tags = ", ".join(f"#{t}({c})" for t, c in signals["tags"][:8])
            parts.append(f"- 高频话题：{top_tags}")
        if signals.get("top_notes"):
            parts.append("- 爆款参考：")
            for t in signals["top_notes"]:
                parts.append(f"  - [{t['engagement']} 互动] {t['title']}")
        parts.append("")

    for idx, idea in enumerate(ideas, 1):
        parts.append(f"## {idx}. [{idea['angle']}] {idea['title']}")
        parts.append("")
        parts.append(f"- **角度**：{idea['angle_hint']}")
        parts.append(f"- **标题公式**：{idea['formula']}")
        parts.append(f"- **正文骨架**：{idea['skeleton']}（详见 data/content_structures.md）")
        parts.append(f"- **推荐话题**：{' '.join('#' + t for t in idea['tags'])}")
        parts.append("")

    parts.append("---")
    parts.append("")
    parts.append("下一步：")
    parts.append(f"  python3 write_post.py draft --topic '{seed}' --formula T2 --skeleton S1 --out draft.md")
    return "\n".join(parts) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(prog="topic_ideas.py", description="小红书选题灵感生成")
    p.add_argument("--seed", required=True, help="种子关键词")
    p.add_argument("--persona", default="", help="目标受众身份")
    p.add_argument("--payoff", default="", help="利益点")
    p.add_argument("--notes", default="", help="(可选) 已抓取的笔记数据 .json/.jsonl")
    p.add_argument("--n", type=int, default=10, help="生成几条选题")
    p.add_argument("--format", choices=["md", "json", "text"], default="text")
    p.add_argument("--out", default="", help="输出文件；不填打印到 stdout")
    args = p.parse_args()

    signals: Optional[Dict[str, Any]] = None
    if args.notes:
        try:
            signals = gather_signals(args.notes)
        except FileNotFoundError:
            print(f"数据文件不存在：{args.notes}", file=sys.stderr)
            return 1

    ideas = build_ideas(args.seed, n=args.n, persona=args.persona,
                       payoff=args.payoff, signals=signals)

    if args.format == "md":
        out_text = render_markdown(args.seed, ideas, signals)
    elif args.format == "json":
        out_text = json.dumps({"seed": args.seed, "ideas": ideas, "signals": signals},
                              ensure_ascii=False, indent=2)
    else:
        out_text = "\n".join(f"{i['idea_no']}. [{i['angle']} / {i['formula']}+{i['skeleton']}] {i['title']}"
                             for i in ideas)

    if args.out:
        Path(args.out).write_text(out_text, encoding="utf-8")
        print(f"✓ 已输出到 {args.out}", file=sys.stderr)
    else:
        print(out_text)

    return 0


if __name__ == "__main__":
    sys.exit(main())
