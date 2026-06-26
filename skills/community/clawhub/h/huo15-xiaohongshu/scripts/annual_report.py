#!/usr/bin/env python3
"""火一五小红书"创作年鉴" — 月/季/年度的成长可视化总结。

为什么需要
==========
weekly_review 是"短期复盘"（7 天 / 30 天）。
annual_report 是"长线仪式感" — 把一段时间的所有数据熬成一份"年鉴"。

包含
====
- 📅 时间轴：每月起草 / 发布 / 互动 / 训练数
- 🏆 高光时刻：互动最高的 5 条 / 最长改稿的 1 条 / 最大单维进步
- 📈 成长曲线：6 维分数走势（从最早 baseline 到最近 promote）
- 🎨 风格变化：开始时的 vs 现在的（标题长度 / emoji / 公式偏好对比）
- 🌱 你给自己的反馈：reject / accept 比例变化
- 🌟 学到了什么：long-form 文字回顾（如 LLM 可用）
- 📦 输出：一份漂亮的 markdown 可直接发布到自己博客 / 知乎

用法
----

    python3 annual_report.py                 # 默认 365 天
    python3 annual_report.py --months 3      # 季度
    python3 annual_report.py --months 12 --out my_2026.md
"""

from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import statistics
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))

from xhs_aesthetic import aesthetic_score  # noqa: E402
from xhs_profile import ProfileStore  # noqa: E402
from xhs_writer import load_draft, score_post  # noqa: E402

# 复用 weekly_review 的 gather_* 函数
from weekly_review import (  # noqa: E402
    gather_post_stats,
    gather_iter_stats,
    gather_practice_stats,
    gather_ab_stats,
    gather_drafts_stats,
    gather_feedback_stats,
)

try:
    import llm_helper
except ImportError:
    llm_helper = None  # type: ignore


# =====================================================================
# 月度时间轴
# =====================================================================


def monthly_timeline(store: ProfileStore, months: int) -> Dict[str, Dict[str, int]]:
    """按月分桶：每月起草 / 发布 / 训练 / 改稿 数。"""
    posts = store.load_posts()
    snaps = store.load_snapshots()
    practice = []
    p_path = store.root / "practice.jsonl"
    if p_path.exists():
        for line in p_path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                practice.append(json.loads(line))
            except json.JSONDecodeError:
                continue

    timeline: Dict[str, Dict[str, int]] = {}
    cutoff = dt.datetime.now() - dt.timedelta(days=months * 30)

    def _month_key(ts: str) -> Optional[str]:
        try:
            d = dt.datetime.fromisoformat(ts.replace("Z", "+00:00")).replace(tzinfo=None)
        except (ValueError, AttributeError):
            return None
        if d < cutoff:
            return None
        return d.strftime("%Y-%m")

    for p in posts:
        m = _month_key(p.get("drafted_at", ""))
        if not m:
            continue
        timeline.setdefault(m, {"drafted": 0, "published": 0, "trained": 0, "snapshots": 0})
        timeline[m]["drafted"] += 1
        if p.get("note_id"):
            timeline[m]["published"] += 1

    for s in snaps:
        m = _month_key(s.get("snapshot_at", ""))
        if not m:
            continue
        timeline.setdefault(m, {"drafted": 0, "published": 0, "trained": 0, "snapshots": 0})
        timeline[m]["snapshots"] += 1

    for r in practice:
        m = _month_key(r.get("issued_at", ""))
        if not m:
            continue
        timeline.setdefault(m, {"drafted": 0, "published": 0, "trained": 0, "snapshots": 0})
        timeline[m]["trained"] += 1

    return dict(sorted(timeline.items()))


# =====================================================================
# 高光时刻
# =====================================================================


def highlight_moments(store: ProfileStore, months: int) -> Dict[str, Any]:
    days = months * 30
    out: Dict[str, Any] = {}

    # Top 5 互动笔记
    posts_s = gather_post_stats(store, days)
    out["top_posts"] = posts_s["perf"][:5]

    # 最长改稿
    iter_root = store.root / "iter_sessions"
    longest_session = None
    if iter_root.exists():
        for sess in iter_root.iterdir():
            if not sess.is_dir():
                continue
            log = sess / "iter.jsonl"
            if not log.exists():
                continue
            n = sum(1 for _ in log.read_text(encoding="utf-8").splitlines() if _.strip())
            if longest_session is None or n > longest_session["rounds"]:
                longest_session = {"id": sess.name, "rounds": n}
    out["longest_session"] = longest_session

    # 最大单维进步
    iter_s = gather_iter_stats(store, days)
    biggest_dim_jump: Optional[Dict[str, Any]] = None
    if iter_s.get("trajectories"):
        sorted_traj = sorted(iter_s["trajectories"], key=lambda x: -(x.get("improved") or 0))
        if sorted_traj and sorted_traj[0].get("improved", 0) > 0:
            biggest_dim_jump = sorted_traj[0]
    out["biggest_jump"] = biggest_dim_jump

    return out


# =====================================================================
# 风格变化对比（始 vs 末）
# =====================================================================


def style_evolution(store: ProfileStore) -> Dict[str, Any]:
    """对比最早 baseline 和最近一篇 — 看用户风格变化。"""
    baselines = store.load_baselines()
    if not baselines:
        return {}

    # 假设 baseline 按时间顺序存（最早的在前）
    earliest = baselines[0]
    latest = baselines[-1] if len(baselines) > 1 else baselines[0]

    def _stats(note: Dict[str, Any]) -> Dict[str, Any]:
        title = note.get("title", "") or ""
        content = note.get("content", "") or ""
        aes = aesthetic_score(title, content)
        return {
            "title_len": len(title),
            "content_len": len(content),
            "allen_total": aes.total,
            "allen_breakdown": {k: v["score"] for k, v in aes.by_dim.items()},
        }

    return {
        "earliest": _stats(earliest),
        "latest": _stats(latest),
    }


# =====================================================================
# LLM 总结（可选）
# =====================================================================


def llm_summary(months: int, timeline: Dict, highlights: Dict,
                evolution: Dict) -> Optional[str]:
    if not llm_helper or not llm_helper.is_enabled():
        return None
    prompt = (
        f"以下是创作者最近 {months} 个月的小红书数据：\n"
        f"月度时间轴：{json.dumps(timeline, ensure_ascii=False)}\n"
        f"高光：{json.dumps(highlights, ensure_ascii=False, default=str)}\n"
        f"风格变化：{json.dumps(evolution, ensure_ascii=False)}\n\n"
        f"基于 Allen 文案体系（缓存里）写一段 200 字以内的"
        f"'年鉴回顾' — 给创作者本人看的，要有温度，不要营销腔。"
        f"提一个具体的进步点 + 一个值得珍视的瞬间。"
    )
    return llm_helper.call(
        prompt, tier="balanced",
        cached_assets=["allen_method"], max_tokens=400, temperature=0.8,
    )


# =====================================================================
# 渲染
# =====================================================================


_DIM_LABELS = {
    "breath": "留白", "ai_speak": "去AI腔", "teach_vs_lead": "带读者",
    "resonance": "共鸣", "invitation": "邀请语", "jarvis_trap": "范本范",
}


def build_report(store: ProfileStore, months: int) -> str:
    days = months * 30
    timeline = monthly_timeline(store, months)
    highlights = highlight_moments(store, months)
    evolution = style_evolution(store)
    profile = store.load_style()

    parts = []
    period = f"{months} 个月" if months < 12 else f"{months // 12} 年"
    parts.append(f"# 火一五小红书 · {period}创作年鉴\n")
    parts.append(f"_{dt.datetime.now().strftime('%Y-%m-%d')} · "
                 f"{profile.persona or '我'} / {profile.niche or '?'}_\n")

    # 概览
    posts_s = gather_post_stats(store, days)
    iter_s = gather_iter_stats(store, days)
    prac_s = gather_practice_stats(store, days)
    drafts_s = gather_drafts_stats(days)

    parts.append("## 一、{period}做了什么\n".replace("{period}", period))
    parts.append(f"- 起草 **{posts_s['drafted']}** 篇 / 发布 **{posts_s['published']}** 篇")
    parts.append(f"- 草稿包 **{drafts_s['in_range']}** 个 / promote **{drafts_s['promoted']}** 终稿")
    parts.append(f"- 教练改稿 **{iter_s['rounds']}** 轮（{iter_s['sessions']} 个 session）")
    parts.append(f"- 写作训练 **{prac_s.get('total', 0)}** 题（平均 {prac_s.get('avg_score', '?')} 分）")
    parts.append("")

    # 月度时间轴
    if timeline:
        parts.append("## 二、月度时间轴\n")
        parts.append("| 月份 | 起草 | 发布 | 改稿 | 训练 | 节奏 |")
        parts.append("|---|---|---|---|---|---|")
        for m, info in timeline.items():
            paced = "🔥" if info["drafted"] >= 8 else "✓" if info["drafted"] >= 3 else "🐢"
            parts.append(f"| {m} | {info['drafted']} | {info['published']} | "
                         f"{info.get('snapshots', 0)} | {info['trained']} | {paced} |")
        parts.append("")

    # 高光
    parts.append("## 三、高光时刻\n")
    if highlights["top_posts"]:
        parts.append("### 🏆 互动 Top 5\n")
        for i, p in enumerate(highlights["top_posts"], 1):
            parts.append(f"{i}. **{p['title'][:30]}** — {p['engagement']} 互动 "
                         f"（CES 加权 {p['ces_engagement']}）")
        parts.append("")
    if highlights["longest_session"]:
        ls = highlights["longest_session"]
        parts.append(f"### 🏋️ 最长一次改稿\n\n"
                     f"`{ls['id']}` 改了 **{ls['rounds']}** 轮才结业 — "
                     f"那篇是你证明自己能 '看出问题就改得动' 的关键时刻。\n")
    if highlights["biggest_jump"]:
        bj = highlights["biggest_jump"]
        parts.append(f"### 📈 最大单篇进步\n\n"
                     f"一篇笔记从 {bj.get('first_total', '?')} 分提到 "
                     f"{bj.get('last_total', '?')} 分（**+{bj.get('improved', 0)}**）— "
                     f"{bj.get('rounds')} 轮 iterate，最终结业。\n")

    # 风格变化
    if evolution:
        parts.append("## 四、风格变化\n")
        e = evolution.get("earliest", {})
        l = evolution.get("latest", {})
        parts.append("| 维度 | 最早 | 最近 | 变化 |")
        parts.append("|---|---|---|---|")
        parts.append(f"| 标题长度 | {e.get('title_len','?')} | {l.get('title_len','?')} | "
                     f"{(l.get('title_len',0) or 0) - (e.get('title_len',0) or 0):+d} |")
        parts.append(f"| 正文长度 | {e.get('content_len','?')} | {l.get('content_len','?')} | "
                     f"{(l.get('content_len',0) or 0) - (e.get('content_len',0) or 0):+d} |")
        parts.append(f"| Allen 总分 | {e.get('allen_total','?')} | {l.get('allen_total','?')} | "
                     f"{(l.get('allen_total',0) or 0) - (e.get('allen_total',0) or 0):+d} |")
        e_b = e.get("allen_breakdown", {}) or {}
        l_b = l.get("allen_breakdown", {}) or {}
        for k, label in _DIM_LABELS.items():
            if k in e_b and k in l_b:
                parts.append(f"| {label} | {e_b[k]} | {l_b[k]} | "
                             f"{(l_b[k] or 0) - (e_b[k] or 0):+d} |")
        parts.append("")

    # LLM 温度回顾
    summary = llm_summary(months, timeline, highlights, evolution)
    if summary:
        parts.append("## 五、回顾\n")
        parts.append(summary)
        parts.append("")

    # 给自己的话
    parts.append("## 尾声\n")
    parts.append(f"_「好文案不是写出来的，是留出来的。」 — Allen_\n")
    parts.append(f"\n继续写。✨\n")

    return "\n".join(parts) + "\n"


# =====================================================================
# 主流程
# =====================================================================


def main() -> int:
    p = argparse.ArgumentParser(prog="annual_report.py", description="月/季/年度创作年鉴")
    p.add_argument("--months", type=int, default=12, help="时间范围（月）")
    p.add_argument("--out", default="", help="保存路径")
    p.add_argument("--format", choices=["md", "json"], default="md")
    args = p.parse_args()

    store = ProfileStore()
    if args.format == "json":
        out_text = json.dumps({
            "months": args.months,
            "timeline": monthly_timeline(store, args.months),
            "highlights": highlight_moments(store, args.months),
            "evolution": style_evolution(store),
        }, ensure_ascii=False, indent=2, default=str)
    else:
        out_text = build_report(store, args.months)

    fname = f"annual_{dt.datetime.now().strftime('%Y%m%d')}_{args.months}m.{args.format}"
    saved = store.reviews_dir / fname
    saved.write_text(out_text, encoding="utf-8")

    if args.out:
        Path(args.out).write_text(out_text, encoding="utf-8")
        print(f"✓ 已写入 {args.out}", file=sys.stderr)
    else:
        print(out_text)
    print(f"✓ 已归档到 {saved}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
