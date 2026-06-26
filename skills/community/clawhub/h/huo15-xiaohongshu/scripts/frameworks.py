#!/usr/bin/env python3
"""火一五小红书"商业文案框架"工具 — 蕉下三式 + 东东枪 AB 点 / 核心体验。

来源：data/copywriting_frameworks.md（Allen 2026-04-28 蕉下教学 + 东东枪
《文案的基本修养》）。

提供
====
1. **蕉下三式生成** — 给主题/产品，输出 「不是…而是…」/ 修辞 / 「每一…」三种候选
2. **AB 点辅助** — 帮你想清楚 A 是什么、B 是什么
3. **核心体验追问** — 引导你说出"读者真正买走的"是什么
4. **创意碰撞器** — 核心体验 × 洞察 = 创意 Idea

工作模式
========
- 规则模式：纯模板填充（零依赖）
- LLM 模式：设置 XHS_LLM_PROVIDER=anthropic 后给更具体候选

用法
----

    # 蕉下三式
    python3 frameworks.py jiaoxia --topic 防晒衣 --value "敢晒太阳的野心"

    # AB 点辅助（交互式）
    python3 frameworks.py ab --topic "周末怎么过"

    # 核心体验追问
    python3 frameworks.py key --product 我的小红书号 --niche 副业

    # 创意碰撞
    python3 frameworks.py spark --key "和我一起活着的感觉" --insight "都市人下班后没人理"
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))

try:
    import llm_helper
except ImportError:
    llm_helper = None  # type: ignore


# =====================================================================
# 蕉下三式
# =====================================================================


_NEGATE_TEMPLATES = [
    "不是{old}，而是{new}",
    "不是{old}，而是回到了{new}",
    "我们不是在{old}，而是在{new}",
    "你以为是{old}，其实是{new}",
]

_METAPHOR_TEMPLATES = [
    "{nature}是最好的{role}",
    "像{thing}一样{verb}",
    "{topic}是{nature}的延伸",
    "用{nature}的方式去{verb}",
]

_EVERY_TEMPLATES = [
    "每一{unit}{action}都是{emotion}",
    "让每一次{scene}都变得{state}",
    "每一{quantity}{topic}都装着{value}",
    "每一刻{action}，都是{value}的练习",
]


def gen_negate(topic: str, value: str = "") -> List[str]:
    """生成"不是…而是…"句式候选。"""
    if not topic:
        return []
    # 基于 topic 推断 old；value 是 new
    common_olds = {
        "防晒": "害怕太阳", "防晒衣": "害怕太阳",
        "户外": "走出门", "周末": "用来恢复元气",
        "护肤": "贴标签的程序", "副业": "多赚一份钱",
        "学习": "为了功利", "健身": "为了瘦",
        "通勤": "无效的时间", "独处": "孤独",
    }
    old = next((v for k, v in common_olds.items() if k in topic), f"应付{topic}")
    new_default = value or f"找回{topic}的本来意义"
    return [t.format(old=old, new=new_default) for t in _NEGATE_TEMPLATES]


def gen_metaphor(topic: str, value: str = "") -> List[str]:
    """生成"修辞/比喻"候选 — 把功能寄生在自然意象上。"""
    natures = ["风", "光", "雨", "海", "山", "雪", "月", "树荫", "晚风", "晨曦"]
    roles = ["造型师", "调色师", "翻译官", "记录者", "陪伴者"]
    things = ["仙人掌", "苔藓", "蒲公英", "一缕风", "一束光", "猫"]
    verbs = ["呼吸", "停一下", "回家", "看见", "活着", "变得柔软"]

    out: List[str] = []
    for t in _METAPHOR_TEMPLATES:
        if "{nature}" in t and "{role}" in t:
            out.append(t.format(nature=natures[0], role=roles[0]))
        elif "{thing}" in t:
            out.append(t.format(thing=things[0], verb=verbs[0]))
        elif "{topic}" in t:
            out.append(t.format(topic=topic, nature=natures[1]))
        elif "{nature}" in t and "{verb}" in t:
            out.append(t.format(nature=natures[2], verb=verbs[1]))
    return out[:4]


def gen_every(topic: str, value: str = "") -> List[str]:
    """生成"每一…都是…"候选 — 把日常拉高成仪式。"""
    units = ["口呼吸", "次出门", "刻", "次选择"]
    actions = [topic or "动作", "决定", "选择", "时刻"]
    emotions = [value or "松弛的味道", "笃定", "属于自己的", "刚刚好"]
    scenes = [topic or "出发", "回家", "醒来", "停下"]
    states = [value or "笃定", "舒服", "明白", "踏实"]

    out: List[str] = []
    out.append(_EVERY_TEMPLATES[0].format(unit=units[0], action="", emotion=emotions[0]))
    out.append(_EVERY_TEMPLATES[1].format(scene=scenes[0], state=states[0]))
    out.append(_EVERY_TEMPLATES[2].format(quantity="次", topic=topic or "出门",
                                          value=value or "笃定"))
    out.append(_EVERY_TEMPLATES[3].format(action=actions[0],
                                          value=value or "回到自己"))
    return out


def cmd_jiaoxia(args: argparse.Namespace) -> int:
    topic = args.topic
    value = args.value
    print(f"🟢 蕉下三式 — 主题：{topic}    价值观：{value or '(未设)'}\n")
    print("=" * 60)
    print("【一】不是 X，而是 Y — 颠覆认知")
    print("=" * 60)
    for i, x in enumerate(gen_negate(topic, value), 1):
        print(f"  {i}. {x}")

    print()
    print("=" * 60)
    print("【二】修辞 / 比喻 — 参数变画面")
    print("=" * 60)
    for i, x in enumerate(gen_metaphor(topic, value), 1):
        print(f"  {i}. {x}")

    print()
    print("=" * 60)
    print("【三】每一 X 都是 Y — 功能升维")
    print("=" * 60)
    for i, x in enumerate(gen_every(topic, value), 1):
        print(f"  {i}. {x}")

    # LLM 增强
    if not args.no_llm and llm_helper and llm_helper.is_enabled():
        print()
        print("=" * 60)
        print("🤖 LLM 增强（基于蕉下方法论 + 你的主题）")
        print("=" * 60)
        prompt = (
            f"参考蕉下品牌方法论（缓存里 copywriting_frameworks.md），"
            f"为主题 '{topic}' 价值观 '{value}' 各产出 1 条更具体、更能用的："
            f"\n  ① 不是…而是… 句式"
            f"\n  ② 修辞/比喻 句式"
            f"\n  ③ 每一…都是… 句式"
            f"\n返回 JSON：{{\"negate\": \"...\", \"metaphor\": \"...\", \"every\": \"...\"}}"
        )
        data = llm_helper.call_json(prompt, tier="balanced",
                                    cached_assets=["allen_method"], max_tokens=400)
        if isinstance(data, dict):
            for k, label in [("negate", "颠覆"), ("metaphor", "修辞"), ("every", "升维")]:
                if data.get(k):
                    print(f"  {label}：{data[k]}")
    return 0


# =====================================================================
# AB 点
# =====================================================================


def cmd_ab(args: argparse.Namespace) -> int:
    print(f"🎯 东东枪 AB 点辅助 — 主题：{args.topic}")
    print()
    print("把读者从 A（现在的看法/感受）→ B（你想让 ta 变成的看法/感受）。")
    print("广告不能直接改变行为，只能改变看法/感受。")
    print()
    print("─" * 60)
    print("请回答 4 个问题：")
    print("─" * 60)

    a_view = input("\n1. 读者**现在**怎么看这件事？（A 看法）\n   > ").strip()
    a_feel = input("\n2. 读者**现在**对它什么感受？（A 感受）\n   > ").strip()
    b_view = input("\n3. 你想让读者**看完后**怎么看？（B 看法）\n   > ").strip()
    b_feel = input("\n4. 你想让读者**看完后**什么感受？（B 感受）\n   > ").strip()

    print()
    print("=" * 60)
    print("📋 AB 点收敛")
    print("=" * 60)
    print(f"\n  主题：{args.topic}")
    print(f"\n  A（起点）")
    print(f"     看法：{a_view or '(未填)'}")
    print(f"     感受：{a_feel or '(未填)'}")
    print(f"\n  B（终点）")
    print(f"     看法：{b_view or '(未填)'}")
    print(f"     感受：{b_feel or '(未填)'}")
    print()

    # 自检
    issues: List[str] = []
    if not a_view or not a_feel:
        issues.append("⚠️ A 没说清楚 → 容易打'假想敌'")
    if b_view and len(b_view) < 8:
        issues.append("⚠️ B 太抽象 → 没有具体感的 B = 没有 B")
    if a_view and b_view and len(set(a_view).intersection(b_view)) > len(a_view) * 0.6:
        issues.append("⚠️ A 和 B 太像 → 没拉开认知差")
    if issues:
        print("─" * 60)
        for x in issues:
            print(f"  {x}")
        print()

    print("─" * 60)
    print("写完笔记后再回来看：A 真的变成 B 了吗？")
    print()

    if not args.no_llm and llm_helper and llm_helper.is_enabled() \
            and a_view and b_view:
        print("🤖 LLM 桥梁建议（基于 AB 点）：")
        prompt = (
            f"主题：{args.topic}\n"
            f"A 看法：{a_view}\nA 感受：{a_feel}\n"
            f"B 看法：{b_view}\nB 感受：{b_feel}\n\n"
            f"基于东东枪《文案的基本修养》(缓存里)，给 1 个'桥梁洞察' — "
            f"读者听了 X，看法/感受会自然从 A 滑向 B。"
            f"洞察必须是'未被表达但人人有过'的真相。100 字内。"
        )
        text = llm_helper.call(prompt, tier="balanced",
                               cached_assets=["allen_method"], max_tokens=300)
        if text:
            print(f"\n   {text}")
    return 0


# =====================================================================
# 核心体验追问
# =====================================================================


def cmd_key(args: argparse.Namespace) -> int:
    print(f"🔑 核心体验（Key Experience）追问")
    print(f"   产品/IP：{args.product}")
    if args.niche:
        print(f"   赛道  ：{args.niche}")
    print()
    print("东东枪：'核心体验 = 品牌真正在售卖、被消费者真正买走的东西。'")
    print("电钻 ≠ 卖洞，卖身份感 / 安全感 / 炫耀感。")
    print()

    questions = [
        ("如果你的产品/IP突然消失，读者最遗憾失去什么？", "最深"),
        ("读者在朋友面前怎么提到你？（一句话）", "外显"),
        ("读者从你这里带走的'感觉'是什么？", "情绪"),
        ("如果你只能用 5 个字描述卖什么，是什么？", "凝练"),
    ]
    answers: List[Dict[str, str]] = []
    for q, label in questions:
        print(f"❓ [{label}] {q}")
        a = input("   > ").strip()
        if a:
            answers.append({"label": label, "q": q, "a": a})
        print()

    if answers:
        print("=" * 60)
        print("📋 核心体验候选")
        print("=" * 60)
        for x in answers:
            print(f"  • [{x['label']}] {x['a']}")
        print()
        print("挑出最让你心动的那条 → 这就是你的 '核心体验'，"
              "未来所有笔记都围着它转。")

        if not args.no_llm and llm_helper and llm_helper.is_enabled():
            prompt = (
                f"产品/IP：{args.product}\n赛道：{args.niche}\n"
                f"读者反馈：{json.dumps(answers, ensure_ascii=False)}\n\n"
                f"基于东东枪'核心体验'概念（缓存里），用一句 ≤ 20 字的话提炼出"
                f"这个 IP 的核心体验。"
            )
            text = llm_helper.call(prompt, tier="balanced",
                                   cached_assets=["allen_method"], max_tokens=200)
            if text:
                print()
                print(f"🤖 LLM 提炼：**{text.strip()}**")
    return 0


# =====================================================================
# 创意碰撞
# =====================================================================


def cmd_spark(args: argparse.Namespace) -> int:
    print("✨ 东东枪创意碰撞法：核心体验 × 洞察 = 创意 Idea")
    print()
    print(f"  核心体验：{args.key}")
    print(f"  洞察    ：{args.insight}")
    print()

    if not args.no_llm and llm_helper and llm_helper.is_enabled():
        prompt = (
            f"东东枪创意碰撞法：核心体验 × 洞察 = 创意 Idea。\n\n"
            f"核心体验：{args.key}\n洞察：{args.insight}\n\n"
            f"基于此（参考缓存里 copywriting_frameworks.md），给 3 个"
            f"创意 Idea 候选 — 每个都要有具体可执行的小红书笔记 angle。"
            f"返回 JSON 数组，每条 {{\"idea\": \"...\", \"angle\": \"...\"}}"
        )
        data = llm_helper.call_json(prompt, tier="balanced",
                                    cached_assets=["allen_method"], max_tokens=600)
        if isinstance(data, list):
            for i, item in enumerate(data, 1):
                if isinstance(item, dict):
                    print(f"  {i}. **{item.get('idea', '')}**")
                    print(f"     笔记 angle：{item.get('angle', '')}")
                    print()
            return 0

    # 规则降级 — 简单组合
    print("规则模式（设置 XHS_LLM_PROVIDER=anthropic 可获更好候选）：")
    print()
    print(f"  Idea 1（直接组合）：把 '{args.key}' 作为答案，把 '{args.insight}' 作为提问")
    print(f"  Idea 2（情景化）：写一个具象场景，让读者认出自己在 '{args.insight}' 里")
    print(f"  Idea 3（反差化）：用 '{args.key}' 作为读者意想不到的解法")
    return 0


# =====================================================================
# 入口
# =====================================================================


def main() -> int:
    p = argparse.ArgumentParser(prog="frameworks.py",
                                description="商业文案框架工具（蕉下三式 / 东东枪 AB 点）")
    sub = p.add_subparsers(dest="cmd", required=True)

    pj = sub.add_parser("jiaoxia", help="蕉下三式生成（颠覆/修辞/升维）")
    pj.add_argument("--topic", required=True)
    pj.add_argument("--value", default="", help="价值观一句话")
    pj.add_argument("--no-llm", action="store_true")
    pj.set_defaults(func=cmd_jiaoxia)

    pa = sub.add_parser("ab", help="东东枪 AB 点辅助（交互式）")
    pa.add_argument("--topic", required=True)
    pa.add_argument("--no-llm", action="store_true")
    pa.set_defaults(func=cmd_ab)

    pk = sub.add_parser("key", help="核心体验追问（4 问凝练）")
    pk.add_argument("--product", required=True)
    pk.add_argument("--niche", default="")
    pk.add_argument("--no-llm", action="store_true")
    pk.set_defaults(func=cmd_key)

    ps = sub.add_parser("spark", help="创意碰撞法：核心体验 × 洞察 → Idea")
    ps.add_argument("--key", required=True, help="核心体验")
    ps.add_argument("--insight", required=True, help="洞察")
    ps.add_argument("--no-llm", action="store_true")
    ps.set_defaults(func=cmd_spark)

    args = p.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
