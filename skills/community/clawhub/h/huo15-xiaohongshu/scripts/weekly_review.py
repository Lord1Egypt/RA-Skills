#!/usr/bin/env python3
"""火一五小红书"创作复盘" v2 — 整合 6 个数据源，给真正的"成长曲线"。

数据源
======
1. `posts.jsonl`              — 起草历史（publish_helper 写）
2. `snapshots.jsonl`          — 互动快照（track_post 写）
3. `profile/iter_sessions/`   — 渐进式教练改稿轨迹（v3.2）⭐
4. `profile/practice.jsonl`   — 写作训练成绩（v2.5）⭐
5. `profile/ab_tests.jsonl`   — A/B 测试记录（v2.5）⭐
6. `drafts/`                  — 草稿版本库（v3.2）⭐

输出
====
1. **产出概况**：起草 / 发布 / 跟踪 / 训练
2. **互动表现**：Top 笔记、爆款 vs 平均、CES 算法对照
3. **成长曲线** ⭐：6 维分数趋势（Allen 美学 + 工程分）/ iter 改稿轨迹 / practice 成绩
4. **教练反馈分析**：哪一维最常被拒、哪一维改进最快
5. **当前画像**：风格档案、规则覆盖
6. **下周建议**：基于趋势给具体行动

用法
----

    python3 weekly_review.py                       # 最近 7 天
    python3 weekly_review.py --days 30             # 月度
    python3 weekly_review.py --out review.md       # 保存到文件
    python3 weekly_review.py --format json         # pipeline 用
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


# =====================================================================
# 数据加载（统一入口）
# =====================================================================


def _parse_dt(s: str) -> Optional[dt.datetime]:
    if not s:
        return None
    try:
        return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return None


def _within(ts: str, days: int) -> bool:
    d = _parse_dt(ts)
    if not d:
        return False
    return (dt.datetime.now() - d).total_seconds() < days * 86400


def _load_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    out = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return out


# =====================================================================
# 各数据源的统计
# =====================================================================


def gather_post_stats(store: ProfileStore, days: int) -> Dict[str, Any]:
    posts = store.load_posts()
    snaps = store.load_snapshots()

    in_range = [p for p in posts if _within(p.get("drafted_at", ""), days)]
    drafted = len(in_range)
    published = sum(1 for p in in_range if p.get("note_id"))

    # 最新快照 by note_id
    latest_snap: Dict[str, Dict[str, Any]] = {}
    for s in snaps:
        nid = s.get("note_id", "")
        if not nid:
            continue
        prev = latest_snap.get(nid)
        if not prev or s.get("snapshot_at", "") > prev.get("snapshot_at", ""):
            latest_snap[nid] = s

    perf = []
    for p in in_range:
        nid = p.get("note_id", "")
        if nid and nid in latest_snap:
            sn = latest_snap[nid]
            engagement = sn["liked"] + sn["collected"] + sn["comment"]
            perf.append({
                "title": p.get("title", "(无)"),
                "score": p.get("score", 0),
                "liked": sn["liked"], "collected": sn["collected"], "comment": sn["comment"],
                "engagement": engagement,
                "ces_engagement": sn["liked"] + sn["collected"] + 4 * sn["comment"],  # 加权
            })
    perf.sort(key=lambda x: -x["engagement"])

    return {
        "drafted": drafted, "published": published,
        "snapshot_count": len(perf), "perf": perf,
    }


def gather_iter_stats(store: ProfileStore, days: int) -> Dict[str, Any]:
    """从 profile/iter_sessions/ 读教练改稿数据。"""
    iter_root = store.root / "iter_sessions"
    if not iter_root.exists():
        return {"sessions": 0, "rounds": 0, "by_dim": {}, "trajectories": []}

    sessions = list(iter_root.iterdir())
    n_sessions = 0
    n_rounds = 0
    by_dim_attempts: Dict[str, int] = collections.defaultdict(int)
    by_dim_improved: Dict[str, int] = collections.defaultdict(int)
    trajectories: List[Dict[str, Any]] = []

    for sess_dir in sessions:
        if not sess_dir.is_dir():
            continue
        log = _load_jsonl(sess_dir / "iter.jsonl")
        if not log:
            continue
        # 最近的 round 触发时间
        last_at = log[-1].get("at", "")
        if not _within(last_at, days):
            continue
        n_sessions += 1
        n_rounds += len(log)

        # 维度统计
        for r in log:
            dim = r.get("focus", "")
            if dim in ("graduated", ""):
                continue
            by_dim_attempts[dim] += 1
            before = r.get("before_score")
            after = r.get("after_score")
            if before is not None and after is not None and after > before:
                by_dim_improved[dim] += 1

        # 总分轨迹
        totals = [r.get("after_total") for r in log if r.get("after_total") is not None]
        if totals:
            trajectories.append({
                "session_id": sess_dir.name,
                "rounds": len(log),
                "first_total": totals[0],
                "last_total": totals[-1],
                "improved": totals[-1] - totals[0] if len(totals) >= 2 else 0,
                "graduated": any(r.get("focus") == "graduated" for r in log),
            })

    # 按维度算改进率
    dim_rate = {
        d: {
            "attempts": by_dim_attempts[d],
            "improved": by_dim_improved[d],
            "rate": round(by_dim_improved[d] / max(1, by_dim_attempts[d]) * 100, 0),
        }
        for d in by_dim_attempts
    }

    return {
        "sessions": n_sessions, "rounds": n_rounds,
        "by_dim": dim_rate, "trajectories": trajectories,
    }


def gather_practice_stats(store: ProfileStore, days: int) -> Dict[str, Any]:
    log = _load_jsonl(store.root / "practice.jsonl")
    in_range = [r for r in log if _within(r.get("issued_at", ""), days)]
    if not in_range:
        return {"total": 0}
    graded = [r for r in in_range if r.get("score") is not None]
    by_kind: Dict[str, int] = collections.defaultdict(int)
    for r in in_range:
        by_kind[r.get("kind", "?")] += 1
    avg = statistics.mean([r["score"] for r in graded]) if graded else 0
    return {
        "total": len(in_range),
        "graded": len(graded),
        "avg_score": round(avg, 1),
        "best": max((r["score"] for r in graded), default=0),
        "by_kind": dict(by_kind),
    }


def gather_ab_stats(store: ProfileStore, days: int) -> Dict[str, Any]:
    log = _load_jsonl(store.root / "ab_tests.jsonl")
    in_range = [r for r in log if _within(r.get("created_at", ""), days)]
    completed = [r for r in in_range if r.get("winner") in ("A", "B", "TIE")]
    return {
        "total": len(in_range),
        "completed": len(completed),
        "winners": collections.Counter(r["winner"] for r in completed),
    }


def gather_drafts_stats(days: int) -> Dict[str, Any]:
    """读 drafts 目录里最近的草稿。"""
    import os
    base = os.environ.get("XHS_DRAFTS_DIR")
    if base:
        drafts_root = Path(os.path.expanduser(base))
    else:
        drafts_root = Path(os.path.expanduser("~/.xiaohongshu/drafts"))
    if not drafts_root.exists():
        return {"total": 0, "in_range": 0, "promoted": 0,
                "ab_set": 0, "ab_validated": 0, "ab_rate": 0}

    total = 0
    in_range = 0
    promoted = 0
    ab_set = 0
    ab_validated = 0
    for d in drafts_root.iterdir():
        if not d.is_dir():
            continue
        total += 1
        meta_p = d / "meta.json"
        if not meta_p.exists():
            continue
        try:
            meta = json.loads(meta_p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        in_window = _within(meta.get("created_at", "") or meta.get("updated_at", ""), days)
        if in_window:
            in_range += 1
        if meta.get("promoted"):
            promoted += 1
        # v3.5: AB 统计
        if in_window and (meta.get("ab_a_view") or meta.get("ab_b_view")):
            ab_set += 1
            if meta.get("ab_validated") is True:
                ab_validated += 1
    ab_rate = round(ab_validated / ab_set * 100) if ab_set else 0
    return {"total": total, "in_range": in_range, "promoted": promoted,
            "ab_set": ab_set, "ab_validated": ab_validated, "ab_rate": ab_rate}


def gather_feedback_stats(store: ProfileStore, days: int) -> Dict[str, Any]:
    feedback = [fb.to_dict() for fb in store.load_feedback()]
    in_range = [f for f in feedback if _within(f.get("at", ""), days)]
    rejected: collections.Counter = collections.Counter()
    accepted: collections.Counter = collections.Counter()
    for f in in_range:
        key = (f.get("rule_key") or "").split(":", 1)[0]
        if f.get("reaction") == "reject":
            rejected[key] += 1
        elif f.get("reaction") == "accept":
            accepted[key] += 1
    return {
        "total": len(in_range),
        "rejected": dict(rejected),
        "accepted": dict(accepted),
    }


# =====================================================================
# 渲染
# =====================================================================


_DIM_LABELS = {
    "breath": "留白", "ai_speak": "去AI腔", "teach_vs_lead": "带读者",
    "resonance": "共鸣", "invitation": "邀请语", "jarvis_trap": "范本范",
    "title": "标题", "first_lines": "首段", "layout": "排版",
    "emoji": "emoji", "hashtags": "话题", "ces_design": "CES互动",
    "compliance": "合规",
}


def build_review(store: ProfileStore, days: int) -> str:
    profile = store.load_style()
    rules = store.load_rules()

    posts_s = gather_post_stats(store, days)
    iter_s = gather_iter_stats(store, days)
    prac_s = gather_practice_stats(store, days)
    ab_s = gather_ab_stats(store, days)
    drafts_s = gather_drafts_stats(days)
    fb_s = gather_feedback_stats(store, days)

    parts: List[str] = []
    title = "周" if days <= 7 else f"近{days}天" if days < 365 else "年"
    parts.append(f"# 火一五小红书 {title}创作复盘\n")
    parts.append(f"_{dt.datetime.now().isoformat(timespec='minutes')} · 档案 {store.root}_\n")

    # ========== 一、产出概况（合并 6 个数据源）==========
    parts.append("## 一、产出概况\n")
    parts.append(f"- 起草: **{posts_s['drafted']}** 篇    "
                 f"发布: **{posts_s['published']}** 篇    "
                 f"已拍快照: **{posts_s['snapshot_count']}** 篇")
    parts.append(f"- 草稿包: **{drafts_s['in_range']}** 个新建（库存 {drafts_s['total']}，"
                 f"已 promote {drafts_s['promoted']}）")
    if drafts_s.get("ab_set"):
        parts.append(f"- AB 点设定: **{drafts_s['ab_set']}** 个草稿设了 AB / "
                     f"已验证兑现 {drafts_s['ab_validated']} 个（**转化率 {drafts_s['ab_rate']}%**）")
    parts.append(f"- 教练改稿: **{iter_s['sessions']}** 个 session / "
                 f"**{iter_s['rounds']}** 轮")
    parts.append(f"- 写作训练: **{prac_s.get('total', 0)}** 题（"
                 f"已评 {prac_s.get('graded', 0)} 题，平均 {prac_s.get('avg_score', '?')} 分）")
    parts.append(f"- A/B 测试: **{ab_s['total']}** 个（已完成 {ab_s['completed']}）")
    parts.append("")

    # ========== 二、互动表现（CES 加权）==========
    if posts_s["perf"]:
        parts.append("## 二、互动表现（CES 加权）\n")
        parts.append("| 排名 | 标题 | 文案分 | 点赞 | 收藏 | 评论 | 互动 | CES 加权 |")
        parts.append("|---|---|---|---|---|---|---|---|")
        for i, p in enumerate(posts_s["perf"][:8], 1):
            parts.append(f"| {i} | {p['title'][:24]} | {p['score']} | "
                         f"{p['liked']} | {p['collected']} | {p['comment']} | "
                         f"**{p['engagement']}** | **{p['ces_engagement']}** |")
        parts.append("")
        # 爆款洞察
        avg = statistics.mean([x["engagement"] for x in posts_s["perf"]])
        top = posts_s["perf"][0]
        if top["engagement"] > avg * 2:
            parts.append(f"📈 **{top['title']}** 是平均（{avg:.0f}）的 "
                         f"{top['engagement']/max(1, avg):.1f} 倍 — 这条值得复盘共性\n")

    # ========== 三、成长曲线（教练 + 训练）==========
    parts.append("## 三、成长曲线\n")
    if iter_s["sessions"]:
        parts.append("### 教练改稿（iter_sessions）\n")
        parts.append("| 维度 | 改稿次数 | 改进次数 | 改进率 |")
        parts.append("|---|---|---|---|")
        for d, info in sorted(iter_s["by_dim"].items(), key=lambda x: -x[1]["attempts"]):
            label = _DIM_LABELS.get(d, d)
            parts.append(f"| {label} | {info['attempts']} | {info['improved']} | "
                         f"**{info['rate']}%** |")
        parts.append("")

        # 找"长期掉某维"的信号
        weak_dims = [d for d, info in iter_s["by_dim"].items()
                     if info["attempts"] >= 3 and info["rate"] < 40]
        if weak_dims:
            labels = "、".join(_DIM_LABELS.get(d, d) for d in weak_dims)
            parts.append(f"⚠️ **长期掉这些维：{labels}** — 跑 `practice.py rewrite-jarvis` "
                         f"或对应训练加强\n")

        # 总分轨迹
        if iter_s["trajectories"]:
            improved = [t["improved"] for t in iter_s["trajectories"] if t["improved"] is not None]
            if improved:
                avg_improve = statistics.mean(improved)
                graduated = sum(1 for t in iter_s["trajectories"] if t["graduated"])
                parts.append(f"📊 改稿轨迹：平均每篇提升 **{avg_improve:.0f}** 分，"
                             f"{graduated}/{len(iter_s['trajectories'])} 篇结业（6 维都过 7）\n")

    if prac_s.get("graded"):
        parts.append(f"### 写作训练\n")
        parts.append(f"- 平均分 **{prac_s['avg_score']}** / 最高 {prac_s['best']}")
        if prac_s.get("by_kind"):
            parts.append(f"- 类型: {prac_s['by_kind']}")
        parts.append("")

    # ========== 四、教练反馈分析 ==========
    if fb_s["total"]:
        parts.append("## 四、教练反馈分析\n")
        if fb_s["rejected"]:
            parts.append("- 最常 reject 的检查项：")
            for k, v in sorted(fb_s["rejected"].items(), key=lambda x: -x[1])[:5]:
                hint = " ← 跑 `evolve` 自动禁用" if v >= 3 else ""
                parts.append(f"  - {_DIM_LABELS.get(k, k)}（{v} 次）{hint}")
        if fb_s["accepted"]:
            parts.append("- 最常 accept 的检查项：")
            for k, v in sorted(fb_s["accepted"].items(), key=lambda x: -x[1])[:5]:
                parts.append(f"  - {_DIM_LABELS.get(k, k)}（{v} 次）")
        parts.append("")

    # ========== 五、当前画像 ==========
    if profile.sample_count:
        parts.append("## 五、当前画像\n")
        parts.append(f"- 人设 / 赛道: {profile.persona or '?'} / {profile.niche or '?'}")
        parts.append(f"- 标题 {profile.avg_title_len} 字 / 正文 {profile.avg_content_len} 字 / "
                     f"{profile.emoji_per_post} emoji 每篇")
        if profile.favorite_formulas:
            top_f = sorted(profile.favorite_formulas.items(), key=lambda x: -x[1])[:3]
            parts.append(f"- 偏好公式: {', '.join(f'{k}({v})' for k, v in top_f)}")
        if rules.disabled_checks:
            parts.append(f"- 已禁用检查: {rules.disabled_checks}")
        if rules.main_keyword:
            parts.append(f"- 主关键词: {rules.main_keyword}（用于标题前 13 字检查）")
        parts.append("")

    # ========== 六、下周建议 ==========
    parts.append("## 六、下周建议\n")
    suggestions = _make_suggestions(posts_s, iter_s, prac_s, drafts_s, fb_s)
    for s in suggestions:
        parts.append(f"- {s}")

    return "\n".join(parts) + "\n"


def _make_suggestions(posts_s, iter_s, prac_s, drafts_s, fb_s) -> List[str]:
    out: List[str] = []
    if posts_s["drafted"] < 3:
        out.append("🐢 起草 < 3 篇 — 节奏偏慢，跑 `assistant.py today` 看选题")
    elif posts_s["drafted"] > 7:
        out.append("🚀 起草偏多 — 留意'模板化'风险，加跑 `critique.py --watch` 深度分析")

    # 改进率低的维度
    if iter_s.get("by_dim"):
        weak = [d for d, info in iter_s["by_dim"].items()
                if info["attempts"] >= 3 and info["rate"] < 40]
        if weak:
            label = _DIM_LABELS.get(weak[0], weak[0])
            out.append(f"📚 重点训练 **{label}** — 跑 `practice.py rewrite-jarvis` "
                       f"或读 data/allen_method.md 对应章节")

    # 草稿已 promote 但未发布
    if drafts_s["promoted"] > posts_s["published"] and drafts_s["promoted"] >= 1:
        out.append(f"✋ 有 {drafts_s['promoted']} 篇 promote 草稿但未全部发布 — "
                   f"`drafts list` 看进度")

    # feedback 反复 reject
    if fb_s["rejected"]:
        most = max(fb_s["rejected"], key=fb_s["rejected"].get)
        if fb_s["rejected"][most] >= 3:
            out.append(f"🛠 反复 reject **{_DIM_LABELS.get(most, most)}** — "
                       f"跑 `assistant.py evolve` 让助手永久禁用 / 调整")

    if posts_s["perf"]:
        # 下周发到爆款的时段
        tops = sorted(posts_s["perf"], key=lambda x: -x["engagement"])[:3]
        # 简单建议
        out.append("📌 把这周 Top 1 的笔记加到 baseline："
                   "`profile_init.py add path/to/note.json`")

    if not out:
        out.append("✓ 一切正常，继续保持节奏")
    return out


# =====================================================================
# 主流程
# =====================================================================


def main() -> int:
    p = argparse.ArgumentParser(prog="weekly_review.py", description="创作复盘（多源整合）")
    p.add_argument("--days", type=int, default=7, help="时间窗口（天）")
    p.add_argument("--out", default="", help="输出路径")
    p.add_argument("--format", choices=["md", "json"], default="md")
    args = p.parse_args()

    store = ProfileStore()

    if args.format == "json":
        out_text = json.dumps({
            "days": args.days,
            "posts": gather_post_stats(store, args.days),
            "iter": gather_iter_stats(store, args.days),
            "practice": gather_practice_stats(store, args.days),
            "ab": gather_ab_stats(store, args.days),
            "drafts": gather_drafts_stats(args.days),
            "feedback": gather_feedback_stats(store, args.days),
        }, ensure_ascii=False, indent=2, default=str)
    else:
        out_text = build_review(store, args.days)

    fname = f"review_{dt.datetime.now().strftime('%Y%m%d_%H%M')}_{args.days}d.{args.format}"
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
