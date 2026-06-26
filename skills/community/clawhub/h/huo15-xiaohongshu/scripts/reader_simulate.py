#!/usr/bin/env python3
"""火一五小红书"模拟读者画像走全文" — 落地 Allen 第三课。

Allen 第三课
============
**「站文案里面读文案，不是站在外面分析。」**

这个脚本不让你"分析文案"，而是模拟 6 种典型读者画像走完全文，
给出每个画像在【开头 / 中段 / 结尾】的预期情绪曲线 + 是否会做后续动作。

工作模式
========
1. **规则模式**（默认）：根据画像 + 文案语言特征推断情绪曲线
2. **LLM 模式**（XHS_LLM_PROVIDER=anthropic）：调一次 LLM 让"读者"真的读

输出：每个读者画像三段情绪 + 总反应（停留 / 下滑 / 互动 / 收藏 / 关注）

用法
----

    # 默认 6 个画像
    python3 reader_simulate.py --in draft.md

    # 指定画像
    python3 reader_simulate.py --in draft.md --persona "30+ 干皮女生" "新手妈妈"

    # JSON pipeline
    python3 reader_simulate.py --in draft.md --format json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))

from xhs_writer import Draft, load_draft  # noqa: E402


# ---------- 默认读者画像 ----------


_DEFAULT_PERSONAS = [
    {"name": "30+ 干皮女生", "cares_about": ["护肤", "情绪", "自我犒赏"], "warm_to": ["亲测", "30+", "干皮", "妈妈"]},
    {"name": "互联网打工人", "cares_about": ["效率", "副业", "下班"], "warm_to": ["早八", "周三", "通勤", "副业"]},
    {"name": "新手妈妈", "cares_about": ["育儿", "省时", "情绪"], "warm_to": ["宝宝", "辅食", "睡眠", "陪伴"]},
    {"name": "大学生", "cares_about": ["学习", "省钱", "氛围感"], "warm_to": ["白嫖", "宿舍", "考研", "图书馆"]},
    {"name": "i 人独居者", "cares_about": ["独处", "周末", "氛围"], "warm_to": ["一个人", "独处", "周末", "在家"]},
    {"name": "二线小城自由职业", "cares_about": ["慢生活", "副业", "降级"], "warm_to": ["回老家", "数字游民", "县城"]},
]


_HOOK_WORDS = {
    "代入型": ["你是不是", "你也", "你最近", "你那一天"],
    "数据型": ["%", "天", "斤", "块", "万"],
    "反差型": ["我以为", "本以为", "结果", "没想到"],
    "故事型": ["上周", "那天", "今天", "周一", "周五"],
    "权威型": ["作为", "亲测", "我自己", "我体感"],
}


_LEAD_VS_TEACH_TEACH = ["你应该", "你必须", "记住", "划重点", "敲黑板"]
_LEAD_VS_TEACH_LEAD = ["你可以试试", "我自己", "我体感", "也许", "或许", "你呢"]


# ---------- 数据结构 ----------


@dataclass
class ReaderTrace:
    persona: str
    opening_emotion: str       # 开头读完的情绪
    midway_emotion: str        # 中段读完的情绪
    ending_emotion: str        # 结尾读完的情绪
    will_continue: bool        # 会读到底吗
    will_interact: List[str]   # 会做哪些动作 [stay/comment/like/save/follow/share]
    pull_quote: str            # 这个读者最被打动的一句

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ---------- 规则引擎 ----------


def _split_thirds(text: str) -> tuple[str, str, str]:
    lines = [ln for ln in text.splitlines() if ln.strip()]
    if not lines:
        return "", "", ""
    n = len(lines)
    a = "\n".join(lines[: max(1, n // 3)])
    b = "\n".join(lines[n // 3: 2 * n // 3])
    c = "\n".join(lines[2 * n // 3:])
    return a, b, c


def _has_warm(text: str, words: List[str]) -> bool:
    return any(w in text for w in words)


def _pick_pull_quote(text: str) -> str:
    """挑一句最有"金句感"的当 pull quote。"""
    lines = [ln.strip() for ln in text.splitlines() if 8 < len(ln.strip()) < 40]
    if not lines:
        return ""
    # 偏好独立成段、短而有反差词的
    for ln in lines:
        if any(w in ln for w in ["其实", "我以为", "原来", "没想到", "亲测", "你也"]):
            return ln
    return lines[0]


def simulate_reader_rules(draft: Draft, persona: Dict[str, Any]) -> ReaderTrace:
    full = f"{draft.title}\n{draft.content}"
    a, b, c = _split_thirds(draft.content)

    # 开头判断：是否有钩子
    hook_hit = any(any(w in (draft.title + a) for w in ws) for ws in _HOOK_WORDS.values())
    warm_hit = _has_warm(full, persona["warm_to"])
    teach_count = sum(full.count(w) for w in _LEAD_VS_TEACH_TEACH)
    lead_count = sum(full.count(w) for w in _LEAD_VS_TEACH_LEAD)

    # 开头情绪
    if hook_hit and warm_hit:
        opening = "✨ 被勾住，想继续读"
    elif hook_hit:
        opening = "🤔 有点好奇，但题材不是我特别关心的"
    elif warm_hit:
        opening = "👀 题材有关联，开头平淡"
    else:
        opening = "😴 没钩到我，可能下滑"

    # 中段情绪
    if teach_count > lead_count + 2:
        midway = "🥱 教师讲课感，开始走神"
    elif lead_count >= 2:
        midway = "🌷 像在听朋友说话，舒服"
    else:
        midway = "🙂 节奏中规中矩"

    # 结尾情绪 + 是否互动
    invite = bool(re.search(r"你呢|你那一天|留个|评论区聊聊|你最近|如果你也", c))
    if invite:
        ending = "💬 想说点什么"
    elif "总结" in c or "划重点" in c:
        ending = "📋 像被检查作业，没动力互动"
    else:
        ending = "🌒 自然结束，没特别冲动"

    will_continue = (opening != "😴 没钩到我，可能下滑")
    actions: List[str] = []
    if will_continue:
        actions.append("stay")
    if midway == "🌷 像在听朋友说话，舒服":
        actions.append("like")
    if invite:
        actions.append("comment")
    if warm_hit and lead_count >= 2:
        actions.append("save")
    if warm_hit and lead_count >= 3:
        actions.append("follow")

    return ReaderTrace(
        persona=persona["name"],
        opening_emotion=opening,
        midway_emotion=midway,
        ending_emotion=ending,
        will_continue=will_continue,
        will_interact=actions,
        pull_quote=_pick_pull_quote(draft.content),
    )


# ---------- LLM 模式 ----------


def simulate_reader_llm(draft: Draft, persona: Dict[str, Any]) -> Optional[ReaderTrace]:
    if os.environ.get("XHS_LLM_PROVIDER", "").lower() != "anthropic":
        return None
    try:
        from anthropic import Anthropic
        client = Anthropic()
        sys_prompt = (
            f"你现在是「{persona['name']}」，关心：{', '.join(persona['cares_about'])}。"
            f"你打开小红书随意浏览，遇到这篇笔记。请如实给出三段情绪反馈："
            "①开头三句你是什么感觉；②中段你的注意力如何；③结尾你会做什么动作。"
            "返回 JSON: {opening_emotion, midway_emotion, ending_emotion, will_continue (bool), "
            "will_interact (array of stay/like/save/comment/follow/share), pull_quote (你最被打动的那句话)}"
        )
        msg = client.messages.create(
            model=os.environ.get("XHS_LLM_MODEL", "claude-haiku-4-5-20251001"),
            max_tokens=600,
            system=sys_prompt,
            messages=[{"role": "user",
                       "content": f"标题：{draft.title}\n\n正文：\n{draft.content[:1500]}"}],
        )
        text = msg.content[0].text if msg.content else ""
        try:
            data = json.loads(text)
            return ReaderTrace(
                persona=persona["name"],
                opening_emotion=data.get("opening_emotion", ""),
                midway_emotion=data.get("midway_emotion", ""),
                ending_emotion=data.get("ending_emotion", ""),
                will_continue=bool(data.get("will_continue", True)),
                will_interact=list(data.get("will_interact", [])),
                pull_quote=data.get("pull_quote", ""),
            )
        except Exception:
            return None
    except Exception:
        return None


def simulate_reader(draft: Draft, persona: Dict[str, Any], use_llm: bool = True) -> ReaderTrace:
    if use_llm:
        llm = simulate_reader_llm(draft, persona)
        if llm:
            return llm
    return simulate_reader_rules(draft, persona)


# ---------- 渲染 ----------


def render_text(traces: List[ReaderTrace]) -> str:
    parts = []
    parts.append("👥 多读者模拟（Allen 第三课：站文案里面读）\n")
    for t in traces:
        parts.append(f"━━━ {t.persona} ━━━")
        parts.append(f"  开头：{t.opening_emotion}")
        parts.append(f"  中段：{t.midway_emotion}")
        parts.append(f"  结尾：{t.ending_emotion}")
        parts.append(f"  读完会做：{', '.join(t.will_interact) if t.will_interact else '（什么都不做）'}")
        if t.pull_quote:
            parts.append(f"  🎯 最被打动：「{t.pull_quote}」")
        parts.append("")

    # 总结
    will_stay = sum(1 for t in traces if t.will_continue)
    will_save = sum(1 for t in traces if "save" in t.will_interact)
    will_comment = sum(1 for t in traces if "comment" in t.will_interact)
    parts.append("─" * 50)
    parts.append(f"📊 {will_stay}/{len(traces)} 个读者会读完  /  "
                 f"{will_save} 收藏  /  {will_comment} 评论")
    if will_stay <= len(traces) // 2:
        parts.append("⚠️ 多数读者读不完 — 检查开头钩子和中段是否有'教读者'语气")
    return "\n".join(parts)


def main() -> int:
    p = argparse.ArgumentParser(prog="reader_simulate.py", description="多读者画像模拟")
    p.add_argument("--in", dest="path", required=True)
    p.add_argument("--persona", nargs="*", default=[],
                   help="只模拟指定画像（按名称）；空 = 全部 6 个")
    p.add_argument("--format", choices=["text", "json"], default="text")
    p.add_argument("--out", default="")
    p.add_argument("--no-llm", action="store_true")
    args = p.parse_args()

    draft = load_draft(args.path)

    if args.persona:
        chosen = [p for p in _DEFAULT_PERSONAS if p["name"] in args.persona]
        if not chosen:
            chosen = [{"name": n, "cares_about": [], "warm_to": []} for n in args.persona]
    else:
        chosen = _DEFAULT_PERSONAS

    traces = [simulate_reader(draft, p, use_llm=not args.no_llm) for p in chosen]

    if args.format == "json":
        out_text = json.dumps([t.to_dict() for t in traces], ensure_ascii=False, indent=2)
    else:
        out_text = render_text(traces)

    if args.out:
        Path(args.out).write_text(out_text, encoding="utf-8")
        print(f"✓ 已写入 {args.out}", file=sys.stderr)
    else:
        print(out_text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
