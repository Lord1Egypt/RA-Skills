#!/usr/bin/env python3
"""火一五小红书"五步上手向导" — 让新用户 5 分钟跑通全流程。

为什么需要
==========
新用户打开技能后要：
- 准备 1~5 篇 baseline 笔记
- 设 persona / niche / voice
- 选 preset
- 跑 status 看推荐
- 还得猜下一步该干什么

这 5 步散在多个命令里。wizard 把它们做成一个对话式 5 步流程：
**主题 → 受众 → 风格 → 上传样本 → 选预设**，5 分钟完事。

LLM 增强
========
设置 `XHS_LLM_PROVIDER=anthropic` 后：
- 你随便答（"想写护肤""我是 30 多岁的"），Claude 自动抽 niche / persona
- 没设也能跑 — 用规则解析

用法
----

    python3 wizard.py                        # 交互式 5 步
    python3 wizard.py --baseline a.json b.md # 跳过样本输入
    python3 wizard.py --rerun                # 重新跑（已有档案也覆盖）
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))

from xhs_profile import ProfileStore, RuleOverride, derive_style  # noqa: E402
from xhs_writer import load_draft  # noqa: E402

try:
    import llm_helper
except ImportError:
    llm_helper = None  # type: ignore


def _ask(prompt: str, default: str = "", examples: Optional[List[str]] = None) -> str:
    if examples:
        print(f"\n❓ {prompt}")
        print(f"   例：{' / '.join(examples[:3])}")
    else:
        print(f"\n❓ {prompt}")
    if default:
        print(f"   （回车 = {default}）")
    ans = input("> ").strip()
    return ans or default


def _llm_extract(text: str, hint: str) -> Optional[Dict[str, str]]:
    """让 Claude 从用户随意回答里抽出结构化字段。"""
    if not llm_helper or not llm_helper.is_enabled():
        return None
    prompt = (
        f"用户在小红书创作助手的上手向导里回答了一句：'{text}'\n\n"
        f"任务：{hint}\n"
        f"返回严格 JSON。"
    )
    return llm_helper.call_json(prompt, tier="fast", max_tokens=200)


def step1_topic() -> Dict[str, str]:
    print("=" * 60)
    print("📝 第 1 步 / 5：你最想写什么？")
    print("=" * 60)
    raw = _ask(
        "用一句话告诉我你的赛道方向（可以很模糊）",
        examples=["护肤", "30+ 干皮女生 / 我做护肤", "下班后副业 / 互联网打工人"],
    )
    if not raw:
        return {"niche": "", "persona": ""}
    # LLM 增强抽取
    extracted = _llm_extract(
        raw,
        "从这句话抽出 {niche: 1~3 字赛道词如 '护肤'/'副业', "
        "persona: '30+ 干皮女生'/'互联网打工人' 等}。如果某项抽不出，留空。",
    )
    if extracted:
        return {
            "niche": extracted.get("niche", ""),
            "persona": extracted.get("persona", ""),
        }
    # 规则降级 — 简单关键词识别
    niche_kw = ["护肤", "美妆", "穿搭", "美食", "旅行", "健身", "数码", "育儿",
                "家居", "学习", "职场", "情感", "副业"]
    niche = next((k for k in niche_kw if k in raw), "")
    return {"niche": niche, "persona": raw if not niche else ""}


def step2_persona(current: Dict[str, str]) -> str:
    if current.get("persona") and len(current["persona"]) > 3:
        print(f"\n✓ 已识别受众：{current['persona']}")
        keep = _ask("保留？(y/N)", default="y")
        if keep.lower() == "y":
            return current["persona"]
    print("\n" + "=" * 60)
    print("👥 第 2 步 / 5：你的目标读者是谁？")
    print("=" * 60)
    return _ask(
        "越具体越好（年龄 + 身份 + 典型痛点）",
        examples=["30+ 干皮女生", "i 人独居打工人", "二线城市新手妈妈", "考研党"],
        default=current.get("persona", ""),
    )


def step3_voice() -> str:
    print("\n" + "=" * 60)
    print("🎤 第 3 步 / 5：你的语调偏向？")
    print("=" * 60)
    print("\n  1. casual — 朋友聊天感（最多人选）")
    print("  2. playful — 跳脱有梗")
    print("  3. formal — 严肃专业")
    print("  4. pro — 行业内行人")
    ans = _ask("选一个数字（默认 1）", default="1")
    return {"1": "casual", "2": "playful", "3": "formal", "4": "pro"}.get(ans, "casual")


def step4_baseline(args: argparse.Namespace) -> List[Path]:
    print("\n" + "=" * 60)
    print("📚 第 4 步 / 5：上传 1~5 篇你的代表作")
    print("=" * 60)
    if args.baseline:
        paths = [Path(p) for p in args.baseline]
        print(f"\n✓ 已通过参数提供 {len(paths)} 篇")
        return paths

    print("\n💡 没有也行 — 可以跳过，之后用 `profile_init.py add` 补。")
    print("   有的话粘贴绝对路径，每行一个，空行结束：\n")
    paths: List[Path] = []
    while len(paths) < 5:
        line = input(f"  样本 {len(paths)+1}（回车跳过）> ").strip()
        if not line:
            break
        p = Path(line).expanduser()
        if not p.exists():
            print(f"  ⚠️ 找不到 {p}，跳过")
            continue
        paths.append(p)
    return paths


def step5_preset(answers: Dict[str, Any]) -> str:
    print("\n" + "=" * 60)
    print("🎨 第 5 步 / 5：选风格预设")
    print("=" * 60)
    niche = answers.get("niche", "").lower()
    voice = answers.get("voice", "")

    # 智能推荐
    if niche in ("情感", "副业", "生活") or voice == "casual":
        rec = "allen"
        why = f"你的赛道（{niche or '生活感'}）+ 语调（{voice}）适合品牌 / 共鸣型 — Allen 流"
    elif niche in ("数码", "学习", "职场", "技术") or voice == "pro":
        rec = "engineer"
        why = f"你的赛道偏干货 / 工具类 — 工程师流（关掉 Allen 美学加权）"
    else:
        rec = "balanced"
        why = "默认平衡流（30% Allen + 70% 工程）— 综合个人号最稳"

    print(f"\n💡 我推荐：**{rec}**")
    print(f"   理由：{why}")
    print()
    print("  1. balanced — 工程 70% + Allen 30%（默认）")
    print("  2. allen    — 工程 50% + Allen 50%（品牌/情感/共鸣）")
    print("  3. engineer — 纯工程（干货/教程/工具）")
    ans = _ask("选一个数字，回车 = 推荐", default={"balanced": "1", "allen": "2", "engineer": "3"}[rec])
    return {"1": "balanced", "2": "allen", "3": "engineer"}.get(ans, rec)


# =====================================================================
# 主流程
# =====================================================================


def run_wizard(args: argparse.Namespace) -> int:
    store = ProfileStore()
    if store.style_path.exists() and not args.rerun:
        print("⚠️ 已有风格档案。要重新跑请加 --rerun（会覆盖）。", file=sys.stderr)
        return 1

    print("\n" + "🌱" * 30)
    print("  火一五小红书创作伙伴 · 五步上手向导")
    print("🌱" * 30)
    print("\n这个向导只问 5 个问题，5 分钟跑通全流程。")
    print("不确定的可以直接回车 — 之后随时改。")

    # 1. 主题 / niche
    step1 = step1_topic()
    # 2. persona
    persona = step2_persona(step1)
    # 3. voice
    voice = step3_voice()
    # 4. baseline
    baselines = step4_baseline(args)
    # 5. preset
    answers = {"niche": step1["niche"], "persona": persona, "voice": voice}
    preset = step5_preset(answers)

    # 写档案
    print("\n" + "─" * 60)
    print("⏳ 正在写入档案...")

    samples: List[Dict[str, Any]] = []
    for p in baselines:
        try:
            if p.suffix.lower() == ".json":
                samples.append(json.loads(p.read_text(encoding="utf-8")))
            else:
                draft = load_draft(str(p))
                samples.append(draft.to_dict())
        except Exception as e:
            print(f"  ⚠️ {p.name} 加载失败：{e}")

    for s in samples:
        store.add_baseline(s)

    profile = derive_style(samples) if samples else type(store.load_style())()
    profile.persona = persona
    profile.niche = step1["niche"]
    profile.voice = voice
    store.save_style(profile)

    # 应用 preset
    rules = store.load_rules()
    if step1["niche"]:
        rules.main_keyword = step1["niche"]   # v3.3 加的字段
    store.save_rules(rules)

    # preset 通过 profile_init.py 生效（保持 single source of truth）
    import subprocess
    subprocess.call([sys.executable,
                     str(Path(__file__).parent / "profile_init.py"),
                     "preset", preset])

    print("\n" + "🎉" * 30)
    print("  完成！你的创作伙伴已就位。")
    print("🎉" * 30)
    print(f"""
📋 风格档案：
   人设      : {persona or '(未设)'}
   赛道      : {step1['niche'] or '(未设)'}
   语调      : {voice}
   主关键词  : {step1['niche'] or '(未设)'}
   预设      : {preset}
   样本数    : {len(samples)}

🚀 下一步（选一个）：
   python3 scripts/assistant.py today        # 看今日推荐
   python3 scripts/assistant.py status       # 看完整状态
   python3 scripts/assistant.py drafts new --topic '某主题'  # 直接开写
""")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="wizard.py", description="五步上手向导")
    p.add_argument("--baseline", nargs="*", default=[], help="跳过样本输入步骤")
    p.add_argument("--rerun", action="store_true", help="覆盖已有档案")
    args = p.parse_args()
    return run_wizard(args)


if __name__ == "__main__":
    sys.exit(main())
