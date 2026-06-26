#!/usr/bin/env python3
"""火一五小红书 "Allen 风格诊断" — 哲学家视角的文案体检。

和 polish_post / coach 的差别
============================
- polish 是工程师视角：标题钩子 / 首段抓力 / 排版 / emoji / 话题 / 合规。
- coach  是教练视角：what/why/how/example，覆盖工程维度。
- critique 是 Allen 视角：留白 / AI腔 / 教带 / 共鸣 / 邀请语，看"文案的气韵"。

什么时候用哪个？
================
- **干货 / 教程 / 工具类**：polish 即可，不开 critique（过度强调留白会让步骤教学失真）
- **生活 / 情绪 / 品牌 / 情感共鸣类**：coach + critique 一起用最有效
- **要发出去前**：polish 验工程合规 → critique 验美学 → publish_helper

用法
----

    # 标准 Allen 诊断
    python3 critique.py --in draft.md

    # 合并工程 + Allen 综合分
    python3 critique.py --in draft.md --merged

    # 关闭某个维度（写到 profile/rules.json 也可以）
    python3 critique.py --in draft.md --disable breath ai_speak

    # 输出 markdown 报告
    python3 critique.py --in draft.md --format md --out critique.md

    # JSON for pipeline
    python3 critique.py --in draft.md --format json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from xhs_aesthetic import (  # noqa: E402
    AestheticScore,
    aesthetic_score,
    merge_with_engineering_score,
)
from xhs_profile import ProfileStore  # noqa: E402
from xhs_writer import load_draft, score_post  # noqa: E402

try:
    import llm_helper
except ImportError:
    llm_helper = None  # type: ignore


_LABEL_ORDER = ["breath", "ai_speak", "teach_vs_lead", "resonance", "invitation", "jarvis_trap"]
_LABELS = {
    "breath": "留白度",
    "ai_speak": "去 AI 腔",
    "teach_vs_lead": "带读者",
    "resonance": "共鸣度",
    "invitation": "邀请语",
    "jarvis_trap": "范本范",
}


def render_text(score: AestheticScore, merged: dict | None = None) -> str:
    parts = []
    parts.append("=" * 50)
    parts.append(f"🎨 Allen 风格诊断 — 总分 {score.total}/100")
    parts.append("=" * 50)
    parts.append("")
    parts.append("各维度（0~10）:")
    for k in _LABEL_ORDER:
        if k not in score.by_dim:
            continue
        v = score.by_dim[k]["score"]
        bar = "█" * v + "░" * (10 - v)
        parts.append(f"  {_LABELS[k]:<10} {bar} {v}/10")
    parts.append("")

    if merged:
        parts.append("─" * 50)
        parts.append(f"🧮 综合分（工程 × {1 - merged['aesthetic_weight']:.0%} + "
                     f"Allen × {merged['aesthetic_weight']:.0%}）：**{merged['final']}/100**")
        parts.append(f"   工程分: {merged['engineering']}/100   Allen 分: {merged['aesthetic']}/100")
        parts.append("")

    if score.issues:
        parts.append("📋 命中问题（按维度）:")
        for it in score.issues:
            parts.append(f"  • {it}")
        parts.append("")

    if score.suggestions:
        parts.append("💡 改写建议:")
        for s in score.suggestions:
            parts.append(f"  → {s}")
        parts.append("")

    parts.append("─" * 50)
    parts.append("📚 配套阅读:")
    parts.append("  • Allen 三课与五技法：data/allen_method.md")
    parts.append("  • AI 腔黑名单 + 替换：data/ai_speak_patterns.json")
    parts.append("  • 节气借势画面库：data/seasonal_themes.md")
    return "\n".join(parts)


def render_md(score: AestheticScore, merged: dict | None = None) -> str:
    parts = [f"# Allen 风格诊断报告\n\n**总分：{score.total}/100**\n"]
    parts.append("## 各维度\n")
    for k in _LABEL_ORDER:
        if k not in score.by_dim:
            continue
        v = score.by_dim[k]["score"]
        parts.append(f"- {_LABELS[k]}：**{v}/10**")
    parts.append("")
    if merged:
        parts.append("## 综合分（与工程打分合并）\n")
        parts.append(f"- **最终分：{merged['final']}/100**")
        parts.append(f"- 工程分：{merged['engineering']}（权重 {1 - merged['aesthetic_weight']:.0%}）")
        parts.append(f"- Allen 分：{merged['aesthetic']}（权重 {merged['aesthetic_weight']:.0%}）")
        parts.append("")

    if score.issues:
        parts.append("## 命中问题\n")
        for it in score.issues:
            parts.append(f"- {it}")
        parts.append("")
    if score.suggestions:
        parts.append("## 改写建议\n")
        for s in score.suggestions:
            parts.append(f"- {s}")
        parts.append("")
    return "\n".join(parts) + "\n"


def cmd_rewrite(draft) -> int:
    """LLM 自动改写 — 把 AI 腔 / 教读者 / 攻略型 改成 Allen 范本范。"""
    if not llm_helper or not llm_helper.is_enabled():
        print("❌ 自动改写需要 LLM。请：", file=sys.stderr)
        print("   pip install anthropic", file=sys.stderr)
        print("   export XHS_LLM_PROVIDER=anthropic", file=sys.stderr)
        print("   export ANTHROPIC_API_KEY=sk-...", file=sys.stderr)
        return 1

    score = aesthetic_score(draft.title, draft.content)
    issues_brief = "\n".join(f"- {i}" for i in score.issues[:10])

    prompt = (
        f"以下是一篇小红书草稿，已识别的问题如下：\n{issues_brief}\n\n"
        f"原标题：{draft.title}\n\n"
        f"原正文：\n{draft.content}\n\n"
        f"请基于 Allen 文案体系（缓存里的 allen_method.md）重写这篇笔记，要求：\n"
        f"1. 保留原意 + 用户的话题 + 长度大致不变\n"
        f"2. 把'教读者怎么做'改成'展示什么样的人已经在做'\n"
        f"3. 把汇报化词汇换成人话（参考 ai_speak_patterns.json）\n"
        f"4. 加 1~2 处共同记忆的具体画面（草地/晚风/凉席等）\n"
        f"5. 互动结尾用邀请语而非任务指令\n"
        f"返回 JSON：{{\"title\": \"...\", \"content\": \"...\", \"changes\": [\"改动1\", \"改动2\", ...]}}"
    )
    print("🤖 正在用 LLM 改写...", file=sys.stderr)
    data = llm_helper.call_json(
        prompt,
        tier="balanced",
        cached_assets=["allen_method", "ai_speak"],
        max_tokens=2500,
    )
    if not data:
        print("❌ LLM 调用失败。", file=sys.stderr)
        return 1

    print("=" * 60)
    print(f"📝 重写后标题：{data.get('title', '')}")
    print("=" * 60)
    print()
    print(data.get("content", ""))
    print()
    print("=" * 60)
    print("✏️  改动说明：")
    for c in data.get("changes", []):
        print(f"  • {c}")
    print()

    # 重新跑分对比
    new_score = aesthetic_score(data.get("title", ""), data.get("content", ""))
    print(f"📊 美学分变化：{score.total} → {new_score.total} (+{new_score.total - score.total})")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(prog="critique.py", description="Allen 风格诊断")
    p.add_argument("--in", dest="path", required=True)
    p.add_argument("--format", choices=["text", "md", "json"], default="text")
    p.add_argument("--out", default="")
    p.add_argument("--disable", nargs="*", default=[],
                   help="要跳过的维度：breath / ai_speak / teach_vs_lead / resonance / invitation / jarvis_trap")
    p.add_argument("--merged", action="store_true",
                   help="同时跑工程打分并合并（默认权重 Allen 0.4）")
    p.add_argument("--allen-weight", type=float, default=0.4,
                   help="Allen 在综合分里的权重（0~1，配合 --merged）")
    p.add_argument("--no-profile", action="store_true",
                   help="不读 profile/rules.json 的 disabled_aesthetic")
    p.add_argument("--rewrite", action="store_true",
                   help="LLM 自动改写（需要 XHS_LLM_PROVIDER=anthropic + API key）")
    p.add_argument("--watch", action="store_true",
                   help="流式输出 LLM 详细分析（需要 LLM）")
    args = p.parse_args()

    draft = load_draft(args.path)

    if args.rewrite:
        return cmd_rewrite(draft)

    # 收集要禁用的维度（CLI 优先 + profile 补充）
    disabled = list(args.disable)
    if not args.no_profile:
        rules = ProfileStore().load_rules()
        for k in (rules.disabled_checks or []):
            # 复用 disabled_checks，前缀 aesthetic: 表示 Allen 维度
            if k.startswith("aesthetic:"):
                key = k.split(":", 1)[1]
                if key not in disabled:
                    disabled.append(key)

    score = aesthetic_score(draft.title, draft.content, disabled=disabled)

    merged = None
    if args.merged:
        rules = None if args.no_profile else ProfileStore().load_rules()
        eng = score_post(draft.title, draft.content, draft.tags, rules=rules)
        merged = merge_with_engineering_score(
            eng.breakdown, eng.total, score, aesthetic_weight=args.allen_weight,
        )

    if args.format == "json":
        out_text = json.dumps({
            "aesthetic": score.to_dict(),
            "merged": merged,
        }, ensure_ascii=False, indent=2)
    elif args.format == "md":
        out_text = render_md(score, merged)
    else:
        out_text = render_text(score, merged)

    if args.out:
        Path(args.out).write_text(out_text, encoding="utf-8")
        print(f"✓ 已写入 {args.out}", file=sys.stderr)
    else:
        print(out_text)

    # 流式深度分析
    if args.watch and llm_helper and llm_helper.is_enabled():
        print()
        print("─" * 60)
        print("🔍 LLM 深度解读（streaming）...")
        print()
        prompt = (
            f"以下是一篇小红书笔记，请基于 Allen 文案体系（缓存里的 allen_method.md）"
            f"用 200~400 字给出'最值得改的 3 个点'，每点都要给具体的改写示意。\n\n"
            f"标题：{draft.title}\n\n"
            f"正文：\n{draft.content[:1500]}\n\n"
            f"已识别的问题（仅供参考，请基于全文判断）：\n"
            f"{chr(10).join(score.issues[:5])}"
        )
        gen = llm_helper.stream(
            prompt,
            tier="balanced",
            cached_assets=["allen_method"],
            max_tokens=1200,
        )
        if gen:
            for chunk in gen:
                print(chunk, end="", flush=True)
            print()
        else:
            print("（LLM 调用失败，跳过）")

    # 退出码：分 < 60 视为失败
    return 0 if score.total >= 60 else 1


if __name__ == "__main__":
    sys.exit(main())
