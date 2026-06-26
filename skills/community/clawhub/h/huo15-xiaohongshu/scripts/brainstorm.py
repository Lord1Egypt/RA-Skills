#!/usr/bin/env python3
"""火一五小红书"对话式选题"助手 — 多轮收敛找选题。

和 topic_ideas.py 的差别
========================
- topic_ideas 是"一次性输出 N 条" — 你拿走自己挑。
- brainstorm  是"和你对话 5 轮" — 把模糊感觉收敛到具体可写的选题。

工作流
======
1. 启动 → 检查近况：你最近写了什么？粉丝在评论什么？最近一周关注了什么？
2. 收集 → 主题模糊度 → 受众身份 → 利益点 → 反差 / 角度 → 排序
3. 输出 → 3 个候选选题，每个带：标题 / 公式 / 骨架 / 第一段钩子 / 推荐配图

支持非交互模式（脚本式 / Claude 调用）：把一系列回答用 --turn 传进来。

用法
----

    # 交互模式
    python3 brainstorm.py

    # 一句话模糊种子（仍然进交互）
    python3 brainstorm.py --seed "想写点关于副业的"

    # 非交互模式（每个 --turn 是一个回答）
    python3 brainstorm.py --seed "副业" \\
        --turn "30 岁互联网打工人" \\
        --turn "想写'下班后的另一种活法'" \\
        --turn "不想说赚多少钱，想说时间自由" \\
        --format md --out ideas.md
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))

from xhs_profile import ProfileStore, StyleProfile  # noqa: E402
from xhs_writer import generate_titles  # noqa: E402


# ---------- 5 轮对话 ----------


@dataclass
class Turn:
    prompt: str
    field_name: str
    examples: List[str] = field(default_factory=list)


_TURNS = [
    Turn(
        prompt="你这次想写的主题是什么？（可以模糊，比如'副业'、'秋冬护肤'）",
        field_name="topic",
        examples=["秋冬干皮护肤", "下班后的副业", "30+ 互联网职场"],
    ),
    Turn(
        prompt="目标读者是谁？（年龄/身份/痛点 — 越具体越好）",
        field_name="persona",
        examples=["30+ 干皮女生", "刚毕业 1 年想换工作的", "二胎宝妈"],
    ),
    Turn(
        prompt="读者读完能得到什么？（避免'变美/变好'这种空话）",
        field_name="payoff",
        examples=["不再下午脸起皮", "副业月入 3000 不影响主业", "通勤地铁上背完单词"],
    ),
    Turn(
        prompt="你最想表达的核心观点 / 反差是什么？（一句话）",
        field_name="angle",
        examples=["其实不堆产品，皮肤反而更稳",
                  "副业不是为了赚钱，是为了证明'我不止这一种活法'",
                  "通勤时间是被低估的成长池"],
    ),
    Turn(
        prompt="有什么 '读者可能反对' 的点？（你打算怎么回应？）",
        field_name="objection",
        examples=["读者可能说'又是鸡汤'，我会用具体数据回应",
                  "可能说'这样很卷'，我会反过来说为什么不卷"],
    ),
]


# ---------- 收集回答 ----------


def collect_interactive(seed: str = "") -> Dict[str, str]:
    answers: Dict[str, str] = {}
    if seed:
        answers["topic"] = seed
        print(f"💬 已收到种子：{seed}\n")

    for t in _TURNS:
        if t.field_name in answers:
            continue
        print(f"❓ {t.prompt}")
        if t.examples:
            print(f"   例子：{' / '.join(t.examples[:2])}")
        ans = input("> ").strip()
        if not ans:
            ans = ""  # 允许跳过
        answers[t.field_name] = ans
        print()
    return answers


def collect_from_args(seed: str, turns: List[str]) -> Dict[str, str]:
    answers: Dict[str, str] = {}
    if seed:
        answers["topic"] = seed
    fields_left = [t.field_name for t in _TURNS if t.field_name not in answers]
    for ans, name in zip(turns, fields_left):
        answers[name] = ans
    for name in fields_left:
        answers.setdefault(name, "")
    return answers


# ---------- 收敛产出选题 ----------


def synthesize_ideas(answers: Dict[str, str], profile: Optional[StyleProfile]) -> List[Dict[str, Any]]:
    topic = answers.get("topic") or "新选题"
    persona = answers.get("persona") or (profile.persona if profile else "")
    payoff = answers.get("payoff") or ""
    angle = answers.get("angle") or ""
    objection = answers.get("objection") or ""

    # 基于回答匹配最合适的 3 种公式
    formulas: List[str] = []
    if angle:
        formulas.append("T3")  # 反差冲突
        formulas.append("T6")  # 观点（用 S6 骨架）
    if "为什么" in (angle + topic):
        formulas.append("T8")  # 提问
    if persona:
        formulas.append("T5")  # 身份代入
    if payoff:
        formulas.append("T1")  # 数字对比
    formulas.append("T2")  # 痛点共情兜底
    # 去重保留前 3
    seen = []
    for f in formulas:
        if f not in seen:
            seen.append(f)
    formulas = seen[:3]

    skeletons_for_formula = {
        "T1": "S1", "T2": "S1", "T3": "S6", "T5": "S2",
        "T6": "S6", "T8": "S6", "T10": "S5",
    }

    ideas = []
    for code in formulas:
        cand = generate_titles(topic, persona=persona, payoff=payoff,
                               formulas=[code], n_each=1)
        if not cand:
            continue
        skeleton = skeletons_for_formula.get(code, "S1")
        first_hook = _build_first_hook(answers)
        cover = _suggest_cover(answers, profile)
        ideas.append({
            "title": cand[0]["title"],
            "formula": code,
            "skeleton": skeleton,
            "first_paragraph_hook": first_hook,
            "cover_hint": cover,
            "objection_response_hint": (
                f"在文末或正文后段 1~2 句回应：{objection}" if objection else ""
            ),
            "tags_seed": _tags_seed(topic, profile),
        })
    return ideas


def _build_first_hook(answers: Dict[str, str]) -> str:
    persona = answers.get("persona", "").strip()
    payoff = answers.get("payoff", "").strip()
    angle = answers.get("angle", "").strip()

    if angle and persona:
        return f"✨ 作为 {persona}，我有个不太主流的看法：{angle}"
    if persona and payoff:
        return f"✨ {persona}是不是也想过 {payoff}？我自己尝试了 30 天，结果出乎意料"
    if angle:
        return f"💡 {angle}"
    if payoff:
        return f"✨ 你是不是也想 {payoff}？"
    return "✨ 你是不是也遇到过这种情况？"


def _suggest_cover(answers: Dict[str, str], profile: Optional[StyleProfile]) -> str:
    topic = answers.get("topic", "")
    persona = answers.get("persona", "")
    base = f"{topic} 主题图（手写字 + 简洁背景）"
    if persona:
        base += f"，标题字号大，提及'{persona[:8]}'"
    return base


def _tags_seed(topic: str, profile: Optional[StyleProfile]) -> List[str]:
    out = [topic.strip()] if topic else []
    if profile and profile.common_tags:
        out += [t for t in profile.common_tags[:5] if t not in out]
    return out[:5]


# ---------- 渲染 ----------


def render_text(answers: Dict[str, str], ideas: List[Dict[str, Any]]) -> str:
    parts = ["🧠 选题对话总结\n"]
    for k in ["topic", "persona", "payoff", "angle", "objection"]:
        if answers.get(k):
            parts.append(f"  {k:<10}: {answers[k]}")
    parts.append("")
    parts.append("=" * 50)
    parts.append(f"💡 收敛出 {len(ideas)} 个候选选题：\n")
    for i, idea in enumerate(ideas, 1):
        parts.append(f"{i}. [{idea['formula']} + {idea['skeleton']}] {idea['title']}")
        parts.append(f"   首段钩子: {idea['first_paragraph_hook']}")
        parts.append(f"   封面建议: {idea['cover_hint']}")
        parts.append(f"   推荐话题: {' '.join('#' + t for t in idea['tags_seed'])}")
        if idea.get("objection_response_hint"):
            parts.append(f"   反方回应: {idea['objection_response_hint']}")
        parts.append("")
    parts.append("=" * 50)
    parts.append("下一步：")
    parts.append(f"  python3 scripts/write_post.py draft --topic '{answers.get('topic','')}' \\")
    parts.append(f"      --formula {ideas[0]['formula'] if ideas else 'T2'} "
                 f"--skeleton {ideas[0]['skeleton'] if ideas else 'S1'} \\")
    parts.append(f"      --persona '{answers.get('persona','')}' \\")
    parts.append(f"      --payoff '{answers.get('payoff','')}' --out draft.md")
    return "\n".join(parts)


def render_md(answers: Dict[str, str], ideas: List[Dict[str, Any]]) -> str:
    parts = ["# 选题对话产出\n", "## 收敛要点\n"]
    for k, label in [("topic", "主题"), ("persona", "受众"),
                     ("payoff", "利益点"), ("angle", "核心角度"),
                     ("objection", "反方")]:
        if answers.get(k):
            parts.append(f"- **{label}**：{answers[k]}")
    parts.append("\n## 候选选题\n")
    for i, idea in enumerate(ideas, 1):
        parts.append(f"### {i}. {idea['title']}\n")
        parts.append(f"- **公式 / 骨架**：{idea['formula']} + {idea['skeleton']}")
        parts.append(f"- **首段钩子**：{idea['first_paragraph_hook']}")
        parts.append(f"- **封面建议**：{idea['cover_hint']}")
        parts.append(f"- **推荐话题**：{' '.join('#' + t for t in idea['tags_seed'])}")
        if idea.get("objection_response_hint"):
            parts.append(f"- **反方回应**：{idea['objection_response_hint']}")
        parts.append("")
    return "\n".join(parts) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(prog="brainstorm.py", description="对话式选题")
    p.add_argument("--seed", default="", help="模糊种子主题")
    p.add_argument("--turn", action="append", default=[],
                   help="非交互：按 _TURNS 顺序传回答，可重复")
    p.add_argument("--format", choices=["text", "md", "json"], default="text")
    p.add_argument("--out", default="")
    p.add_argument("--no-profile", action="store_true")
    args = p.parse_args()

    profile = None
    if not args.no_profile:
        profile = ProfileStore().load_style()

    if args.turn:
        answers = collect_from_args(args.seed, args.turn)
    else:
        answers = collect_interactive(args.seed)

    ideas = synthesize_ideas(answers, profile)

    if args.format == "json":
        out_text = json.dumps({"answers": answers, "ideas": ideas},
                              ensure_ascii=False, indent=2)
    elif args.format == "md":
        out_text = render_md(answers, ideas)
    else:
        out_text = render_text(answers, ideas)

    if args.out:
        Path(args.out).write_text(out_text, encoding="utf-8")
        print(f"✓ 已写入 {args.out}", file=sys.stderr)
    else:
        print(out_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
