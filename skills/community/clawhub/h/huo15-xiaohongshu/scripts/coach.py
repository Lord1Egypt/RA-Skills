#!/usr/bin/env python3
"""火一五小红书写作教练 — 不只打分，给"为什么 + 怎么改 + 例子"。

和 polish_post.py 的差别
========================
- polish 是"打分员"：每个维度 0~10，给一句修改建议。
- coach  是"教练"：每条问题展开成 (what, why, how, example)，
  并对照你的风格档案做"风格偏离"提醒，给长线成长建议。

LLM 增强（可选）
================
设置 `XHS_LLM_PROVIDER=anthropic` + 安装 anthropic SDK 后，
教练会调一次 LLM 把建议写得更具体。未设置时纯规则离线跑。

用法
----

    # 标准教练 — 读 profile + rules
    python3 coach.py --in draft.md

    # 详细 markdown 报告
    python3 coach.py --in draft.md --format md --out coach_report.md

    # 同时记录用户反馈（accept/reject 某条建议）
    python3 coach.py --in draft.md --feedback rule_key=reaction \\
        --feedback emoji=reject --feedback first_lines=accept

    # 不读个人档案（纯通用打分）
    python3 coach.py --in draft.md --no-profile
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from xhs_coach import CoachReport, coach  # noqa: E402
from xhs_profile import Feedback, ProfileStore  # noqa: E402
from xhs_writer import load_draft  # noqa: E402


_SEVERITY_ICON = {"high": "🔴", "medium": "🟡", "low": "🔵"}
_WHERE_LABEL = {
    "title": "标题",
    "first_lines": "首段",
    "structure": "结构",
    "layout": "排版",
    "style": "风格偏离",
    "allen": "Allen 美学",
}


def render_text(report: CoachReport) -> str:
    parts = []
    parts.append(f"🏋️ 写作教练报告 — 总分 {report.overall}/100")
    parts.append("")

    if not report.diagnoses:
        parts.append("✓ 没发现明显问题，可以直接进 polish_post.py 做最后体检。")
    else:
        parts.append(f"发现 {len(report.diagnoses)} 处可优化：\n")
        for i, d in enumerate(report.diagnoses, 1):
            icon = _SEVERITY_ICON.get(d.severity, "•")
            label = _WHERE_LABEL.get(d.where, d.where)
            parts.append(f"{icon} 【{label}】{d.what}")
            parts.append(f"   ▸ 为什么：{d.why}")
            parts.append(f"   ▸ 怎么改：{d.how}")
            if d.example:
                parts.append(f"   ▸ 示例  ：{d.example}")
            parts.append("")

    if report.growth_hints:
        parts.append("─" * 50)
        parts.append("📈 长线成长建议")
        for h in report.growth_hints:
            parts.append(f"   {h}")

    return "\n".join(parts)


def render_md(report: CoachReport) -> str:
    parts = [f"# 写作教练报告\n\n**总分：{report.overall}/100**\n"]
    if report.breakdown:
        parts.append("## 子项分\n")
        for k, v in report.breakdown.items():
            label = _WHERE_LABEL.get(k, k)
            parts.append(f"- {label}：{v}/10")
        parts.append("")

    if report.diagnoses:
        parts.append("## 诊断与建议\n")
        for i, d in enumerate(report.diagnoses, 1):
            icon = _SEVERITY_ICON.get(d.severity, "•")
            label = _WHERE_LABEL.get(d.where, d.where)
            parts.append(f"### {i}. {icon} 【{label}】{d.what}\n")
            parts.append(f"**为什么：** {d.why}\n")
            parts.append(f"**怎么改：** {d.how}\n")
            if d.example:
                parts.append(f"**示例：**\n\n```\n{d.example}\n```\n")
    if report.growth_hints:
        parts.append("## 长线成长\n")
        for h in report.growth_hints:
            parts.append(f"- {h}")
    return "\n".join(parts) + "\n"


def main() -> int:
    p = argparse.ArgumentParser(prog="coach.py", description="小红书写作教练")
    p.add_argument("--in", dest="path", required=True, help="草稿路径 (.md 或 .json)")
    p.add_argument("--format", choices=["text", "md", "json"], default="text")
    p.add_argument("--out", default="")
    p.add_argument("--no-profile", action="store_true", help="不读个人档案")
    p.add_argument("--no-llm", action="store_true", help="禁用 LLM 增强（即使设置了 XHS_LLM_PROVIDER）")
    p.add_argument("--feedback", action="append", default=[],
                   help="对某条建议反馈，格式 rule_key=accept|reject|ignore，可重复")
    args = p.parse_args()

    draft = load_draft(args.path)

    profile = None
    rules = None
    feedback_log = []
    post_history = []
    store: ProfileStore | None = None
    if not args.no_profile:
        store = ProfileStore()
        profile = store.load_style()
        rules = store.load_rules()
        feedback_log = [fb.to_dict() for fb in store.load_feedback()]
        post_history = store.load_posts()

    report = coach(
        draft, profile=profile, rules=rules,
        feedback_log=feedback_log, post_history=post_history,
        enrich_llm=not args.no_llm,
    )

    # 记录反馈
    if args.feedback and store is not None:
        now = dt.datetime.now().isoformat(timespec="seconds")
        for kv in args.feedback:
            if "=" not in kv:
                continue
            rule_key, reaction = kv.split("=", 1)
            store.append_feedback(Feedback(
                at=now,
                rule_key=rule_key.strip(),
                suggestion="(via coach.py)",
                reaction=reaction.strip(),
            ))
        print(f"✓ 已记录 {len(args.feedback)} 条反馈到 {store.feedback_path}", file=sys.stderr)

    # 输出
    if args.format == "json":
        text = json.dumps(report.to_dict(), ensure_ascii=False, indent=2)
    elif args.format == "md":
        text = render_md(report)
    else:
        text = render_text(report)

    if args.out:
        Path(args.out).write_text(text, encoding="utf-8")
        print(f"✓ 已写入 {args.out}", file=sys.stderr)
    else:
        print(text)

    # 退出码
    high_count = sum(1 for d in report.diagnoses if d.severity == "high")
    return 0 if high_count == 0 and report.overall >= 70 else 1


if __name__ == "__main__":
    sys.exit(main())
