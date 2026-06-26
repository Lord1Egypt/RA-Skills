#!/usr/bin/env python3
"""火一五小红书"创作伙伴" — 一个把所有能力串起来的主入口。

定位
====
**这才是这个技能的"助手"。** 单点 CLI 是"工具"，这个脚本是"工作流"。
它做三件事：
  1. **看上下文** — 读 profile / posts / snapshots / feedback，知道你在哪一步。
  2. **推荐下一步** — 你"刚来"还是"在写"还是"发完了"，给不一样的建议。
  3. **路由** — 直接帮你跑下一步该跑的脚本。

子命令
======
- `status`       — 一句话：你现在该干什么
- `next`         — 推荐下一步 + 直接执行
- `init`         — 引导第一次建档案（profile_init.py init 的友好包装）
- `brainstorm`   — 进入对话式选题
- `write <topic>` — 在风格档案约束下起草
- `coach <draft>` — 教练模式
- `polish <draft>` — 打分模式（轻量）
- `publish <draft>` — 进入发布前流程
- `review`       — 周复盘
- `learn <kv>`   — 教助手新规则（profile_init.py rules 的友好包装）

`status` 与 `next` 的判断依据
==============================
- 没有 profile → 引导建 baseline
- 有 profile 没起草过 → 推荐 brainstorm
- 有起草中（最近 24h 内）→ 推荐 coach / polish 那篇
- 有发布超 24h 但未拍快照 → 推荐 track snapshot
- 距上次复盘 ≥ 7 天 → 推荐 weekly_review
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))

from xhs_profile import ProfileStore  # noqa: E402

_SCRIPTS_DIR = Path(__file__).resolve().parent
_PY = sys.executable


def _run(*args: str) -> int:
    return subprocess.call([_PY, str(_SCRIPTS_DIR / args[0]), *args[1:]])


# =====================================================================
# 上下文判断
# =====================================================================


def detect_context() -> Dict[str, Any]:
    store = ProfileStore()
    has_profile = store.style_path.exists()
    profile = store.load_style() if has_profile else None
    posts = store.load_posts()
    snaps = store.load_snapshots()
    reviews = sorted(store.reviews_dir.glob("review_*.md")) if store.reviews_dir.exists() else []

    now = dt.datetime.now()

    last_drafted: Optional[Dict[str, Any]] = None
    last_drafted_at: Optional[dt.datetime] = None
    for p in posts:
        d = _parse(p.get("drafted_at"))
        if d and (not last_drafted_at or d > last_drafted_at):
            last_drafted_at, last_drafted = d, p

    last_review_at: Optional[dt.datetime] = None
    if reviews:
        # 文件名形如 review_20260427_1820_7d.md
        for r in reviews:
            try:
                ts = r.stem.split("_")[1] + r.stem.split("_")[2]
                last_review_at = dt.datetime.strptime(ts, "%Y%m%d%H%M")
            except (IndexError, ValueError):
                continue

    # 未拍快照的发布
    snap_note_ids = {s.get("note_id") for s in snaps}
    pending_snap = [
        p for p in posts
        if p.get("note_id") and p["note_id"] not in snap_note_ids
        and _hours_since(_parse(p.get("published_at"))) >= 24
    ]

    return {
        "has_profile": has_profile,
        "profile": profile,
        "post_count": len(posts),
        "snapshot_count": len(snaps),
        "last_drafted": last_drafted,
        "last_drafted_at": last_drafted_at,
        "last_drafted_hours_ago": _hours_since(last_drafted_at),
        "pending_snap": pending_snap,
        "last_review_at": last_review_at,
        "days_since_review": (now - last_review_at).days if last_review_at else None,
    }


def _parse(s: Optional[str]) -> Optional[dt.datetime]:
    if not s:
        return None
    try:
        return dt.datetime.fromisoformat(s)
    except ValueError:
        return None


def _hours_since(d: Optional[dt.datetime]) -> float:
    if not d:
        return 1e9
    return (dt.datetime.now() - d).total_seconds() / 3600


# =====================================================================
# 推荐下一步
# =====================================================================


def recommend(ctx: Dict[str, Any]) -> List[Dict[str, str]]:
    """返回一组推荐 [{"label": ..., "command": ..., "why": ...}]，越靠前越优先。"""
    rec: List[Dict[str, str]] = []

    if not ctx["has_profile"]:
        rec.append({
            "label": "🌱 跑五步上手向导（5 分钟）",
            "command": "assistant.py wizard",
            "why": "助手还不认识你 — 5 步问答帮你建好风格档案 + 选好预设。",
        })
        return rec

    # 有未拍快照的发布
    if ctx["pending_snap"]:
        for p in ctx["pending_snap"][:3]:
            note_id = p["note_id"]
            rec.append({
                "label": f"📊 拍快照：{p.get('title', '')[:25]}",
                "command": f"track_post.py snapshot --note-id {note_id} --xsec-token {p.get('xsec_token','')}",
                "why": f"这篇发布超过 24h 还没拉表现数据。",
            })

    # 距上次复盘 ≥ 7 天
    if ctx["days_since_review"] is None or ctx["days_since_review"] >= 7:
        rec.append({
            "label": "🔁 跑一份周复盘",
            "command": "assistant.py review",
            "why": "上次复盘已超 7 天 — 不复盘的话，'哪些选题真有用' 会变成猜。",
        })

    # 起草中
    if ctx["last_drafted"] and ctx["last_drafted_hours_ago"] < 24:
        rec.append({
            "label": f"🏋️ 给最近这篇做个教练诊断",
            "command": "coach.py --in <你的最新草稿>",
            "why": f"{ctx['last_drafted_hours_ago']:.0f}h 前起草了一篇 — 教练能告诉你哪里还可以再打磨。",
        })

    # 没起草过 / 起草过但最近一周没动
    if not ctx["last_drafted"] or ctx["last_drafted_hours_ago"] > 7 * 24:
        rec.append({
            "label": "☕ 看今日推荐",
            "command": "assistant.py today",
            "why": "结合节气 + 你的公式偏好，给 1~3 条选题推荐。",
        })
        rec.append({
            "label": "🧠 找个新选题（多轮对话）",
            "command": "assistant.py brainstorm",
            "why": "想自己想清楚就用 brainstorm 5 轮对话。",
        })

    return rec or [{
        "label": "✓ 看起来一切顺利",
        "command": "assistant.py status",
        "why": "没有特别紧迫的事 — 想写就跑 brainstorm 或 write。",
    }]


# =====================================================================
# 命令实现
# =====================================================================


def cmd_status(args: argparse.Namespace) -> int:
    ctx = detect_context()
    p = ctx["profile"]

    print("━" * 60)
    print("📒 火一五小红书创作伙伴 — 状态")
    print("━" * 60)
    if ctx["has_profile"] and p:
        print(f"  人设：{p.persona or '(未设置)'}    赛道：{p.niche or '(未设置)'}    "
              f"样本：{p.sample_count} 篇")
        print(f"  历史起草：{ctx['post_count']} 篇    快照：{ctx['snapshot_count']} 条")
        if ctx["last_drafted_at"]:
            print(f"  最近起草：{ctx['last_drafted_hours_ago']:.0f}h 前 — "
                  f"{ctx['last_drafted'].get('title', '')[:30]}")
        if ctx["last_review_at"]:
            print(f"  上次复盘：{ctx['days_since_review']} 天前")
        if ctx["pending_snap"]:
            print(f"  ⚠️  {len(ctx['pending_snap'])} 篇发布超 24h 未拍快照")
    else:
        print("  ❗ 还没建立风格档案")

    print()
    print("🧭 接下来推荐：")
    for r in recommend(ctx)[:3]:
        print(f"  {r['label']}")
        print(f"     ↳ {r['why']}")
        print(f"     $ python3 scripts/{r['command']}")
        print()
    return 0


def cmd_next(args: argparse.Namespace) -> int:
    ctx = detect_context()
    rec = recommend(ctx)
    if not rec:
        print("没有特别推荐。")
        return 0
    top = rec[0]
    print(f"🧭 推荐执行：{top['label']}")
    print(f"   ↳ {top['why']}")

    # 直接跑（除了占位类推荐）
    cmd_parts = top["command"].split()
    if not cmd_parts or "<" in top["command"]:
        # 含尖括号占位的 — 不能直接跑
        print(f"   $ python3 scripts/{top['command']}")
        print("   （需要参数，请手动执行上面的命令）")
        return 0
    if not args.dry_run:
        return _run(*cmd_parts)
    print(f"   $ python3 scripts/{top['command']}  (dry-run)")
    return 0


def cmd_init(args: argparse.Namespace) -> int:
    """引导建立 baseline — 包装 profile_init.py init。"""
    extra = []
    if args.persona:
        extra += ["--persona", args.persona]
    if args.voice:
        extra += ["--voice", args.voice]
    if args.niche:
        extra += ["--niche", args.niche]
    if args.baseline:
        extra += ["--baseline", *args.baseline]
    if args.note_id:
        extra += ["--note-id", *args.note_id]
        if args.xsec_token:
            extra += ["--xsec-token", args.xsec_token]
    return _run("profile_init.py", "init", *extra)


def cmd_brainstorm(args: argparse.Namespace) -> int:
    extra = []
    if args.seed:
        extra += ["--seed", args.seed]
    if args.format:
        extra += ["--format", args.format]
    if args.out:
        extra += ["--out", args.out]
    return _run("brainstorm.py", *extra)


def cmd_write(args: argparse.Namespace) -> int:
    """根据风格档案预填一些参数。"""
    profile = ProfileStore().load_style()
    extra = ["--topic", args.topic]
    if args.persona or profile.persona:
        extra += ["--persona", args.persona or profile.persona]
    if args.payoff:
        extra += ["--payoff", args.payoff]
    formula = args.formula or _favorite_formula(profile) or "T2"
    skeleton = args.skeleton or _favorite_skeleton(profile) or "S1"
    extra += ["--formula", formula, "--skeleton", skeleton]
    if profile.common_tags:
        extra += ["--tags", ",".join(profile.common_tags[:5])]
    if args.out:
        extra += ["--out", args.out]
    return _run("write_post.py", "draft", *extra)


def _favorite_formula(profile) -> Optional[str]:
    if profile and profile.favorite_formulas:
        return max(profile.favorite_formulas, key=profile.favorite_formulas.get)
    return None


def _favorite_skeleton(profile) -> Optional[str]:
    if profile and profile.favorite_skeletons:
        return max(profile.favorite_skeletons, key=profile.favorite_skeletons.get)
    return None


def cmd_coach(args: argparse.Namespace) -> int:
    extra = ["--in", args.draft]
    if args.format:
        extra += ["--format", args.format]
    if args.out:
        extra += ["--out", args.out]
    if args.feedback:
        for f in args.feedback:
            extra += ["--feedback", f]
    return _run("coach.py", *extra)


def cmd_polish(args: argparse.Namespace) -> int:
    return _run("polish_post.py", "--in", args.draft)


def cmd_critique(args: argparse.Namespace) -> int:
    extra = ["--in", args.draft]
    if args.merged:
        extra.append("--merged")
    if args.allen_weight is not None:
        extra += ["--allen-weight", str(args.allen_weight)]
    if args.format:
        extra += ["--format", args.format]
    if args.out:
        extra += ["--out", args.out]
    return _run("critique.py", *extra)


def cmd_coin(args: argparse.Namespace) -> int:
    extra = ["--brand", args.brand]
    if args.value:
        extra += ["--value", args.value]
    if args.n:
        extra += ["--n", str(args.n)]
    return _run("coin_word.py", *extra)


def cmd_series(args: argparse.Namespace) -> int:
    extra = ["--theme", args.theme]
    if args.persona:
        extra += ["--persona", args.persona]
    if args.n:
        extra += ["--n", str(args.n)]
    return _run("series_design.py", *extra)


def cmd_simulate(args: argparse.Namespace) -> int:
    return _run("reader_simulate.py", "--in", args.draft)


def cmd_reverse(args: argparse.Namespace) -> int:
    extra = []
    if args.url:
        extra += ["--url", args.url]
    if args.path:
        extra += ["--in", args.path]
    if args.add_baseline:
        extra.append("--add-baseline")
    if args.format:
        extra += ["--format", args.format]
    return _run("reverse_engineer.py", *extra)


def cmd_cover(args: argparse.Namespace) -> int:
    extra = ["--in", args.draft]
    if args.niche:
        extra += ["--niche", args.niche]
    return _run("cover_brief.py", *extra)


def cmd_rewrite(args: argparse.Namespace) -> int:
    return _run("critique.py", "--in", args.draft, "--rewrite")


def cmd_coach_iterate(args: argparse.Namespace) -> int:
    extra = ["--in", args.draft]
    if args.focus:
        extra += ["--focus", args.focus]
    if args.history:
        extra.append("--history")
    if args.reset:
        extra.append("--reset")
    return _run("coach_iterate.py", *extra)


def cmd_drafts(args: argparse.Namespace) -> int:
    return _run("drafts.py", *args.passthrough)


def cmd_today(args: argparse.Namespace) -> int:
    extra = []
    if args.n:
        extra += ["--n", str(args.n)]
    if args.format:
        extra += ["--format", args.format]
    if args.out:
        extra += ["--out", args.out]
    return _run("today.py", *extra)


def cmd_find(args: argparse.Namespace) -> int:
    extra = [args.query]
    if args.source:
        extra += ["--in", args.source]
    if args.regex:
        extra.append("--regex")
    if args.word:
        extra.append("--word")
    if args.limit:
        extra += ["--limit", str(args.limit)]
    return _run("find.py", *extra)


def cmd_wizard(args: argparse.Namespace) -> int:
    extra = []
    if args.baseline:
        extra += ["--baseline", *args.baseline]
    if args.rerun:
        extra.append("--rerun")
    return _run("wizard.py", *extra)


def cmd_annual(args: argparse.Namespace) -> int:
    extra = []
    if args.months:
        extra += ["--months", str(args.months)]
    if args.out:
        extra += ["--out", args.out]
    return _run("annual_report.py", *extra)


def cmd_frameworks(args: argparse.Namespace) -> int:
    return _run("frameworks.py", *args.passthrough)


def cmd_scene(args: argparse.Namespace) -> int:
    extra = []
    if args.n:
        extra += ["--n", str(args.n)]
    if args.category:
        extra += ["--category", args.category]
    if args.history:
        extra.append("--history")
    return _run("scene_prompt.py", *extra)


def cmd_case(args: argparse.Namespace) -> int:
    return _run("case_study.py", *args.passthrough)


def cmd_publish(args: argparse.Namespace) -> int:
    extra = ["--in", args.draft, "--log", str(ProfileStore().posts_path)]
    return _run("publish_helper.py", *extra)


def cmd_review(args: argparse.Namespace) -> int:
    extra = []
    if args.days:
        extra += ["--days", str(args.days)]
    if args.out:
        extra += ["--out", args.out]
    return _run("weekly_review.py", *extra)


def cmd_learn(args: argparse.Namespace) -> int:
    """教助手一条规则。

    支持的简化语法：
      - `disable=emoji`        → 禁用 emoji 检查
      - `add-sensitive=卷王`   → 加敏感词
      - `allow=最佳`           → 解禁某词
      - `max-emoji=4`          → 单篇上限
    """
    extra = []
    for kv in args.rules:
        if "=" not in kv:
            continue
        k, v = kv.split("=", 1)
        k = k.strip().lower()
        v = v.strip()
        if k == "disable":
            extra += ["--disable", v]
        elif k == "enable":
            extra += ["--enable", v]
        elif k == "add-sensitive":
            extra += ["--add-sensitive", v]
        elif k == "remove-sensitive":
            extra += ["--remove-sensitive", v]
        elif k == "allow":
            extra += ["--allow", v]
        elif k == "max-emoji":
            extra += ["--max-emoji", v]
        elif k == "weight":
            extra += ["--weight", v]
        elif k == "prefer-emoji":
            extra += ["--prefer-emoji", v]
    if not extra:
        print("用法举例：assistant.py learn disable=emoji add-sensitive=卷王", file=sys.stderr)
        return 1
    return _run("profile_init.py", "rules", *extra)


def cmd_evolve(args: argparse.Namespace) -> int:
    return _run("profile_init.py", "evolve", "--threshold", str(args.threshold))


def cmd_warmup(args: argparse.Namespace) -> int:
    return _run(
        "warmup.py",
        *(["--quick"] if args.quick else []),
        *(["--freewrite"] if args.freewrite else []),
    )


def cmd_browser(args: argparse.Namespace) -> int:
    return _run(
        "browser_bridge.py", args.action,
        *([args.target] if args.target else []),
    )


def cmd_philosophy(args: argparse.Namespace) -> int:
    return _run(
        "philosophy.py",
        *(["--layer", str(args.layer)] if args.layer else []),
        *(["--mantra"] if args.mantra else []),
        *(["--checklist"] if args.checklist else []),
    )


def cmd_preset(args: argparse.Namespace) -> int:
    if args.list:
        return _run("profile_init.py", "preset", "--list")
    if not args.name:
        print("用法：assistant.py preset <allen|engineer|balanced>  或  --list 查看", file=sys.stderr)
        return 1
    return _run("profile_init.py", "preset", args.name)


# =====================================================================
# 入口
# =====================================================================


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="assistant.py",
        description="火一五小红书创作伙伴 — 一个入口把所有能力串起来",
    )
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("status", help="状态 + 推荐").set_defaults(func=cmd_status)

    pn = sub.add_parser("next", help="按推荐执行下一步")
    pn.add_argument("--dry-run", action="store_true")
    pn.set_defaults(func=cmd_next)

    pi = sub.add_parser("init", help="引导建立风格档案")
    pi.add_argument("--persona", default="")
    pi.add_argument("--voice", choices=["casual", "formal", "playful", "pro"], default="")
    pi.add_argument("--niche", default="")
    pi.add_argument("--baseline", nargs="*", default=[])
    pi.add_argument("--note-id", nargs="*", default=[])
    pi.add_argument("--xsec-token", default="")
    pi.set_defaults(func=cmd_init)

    pb = sub.add_parser("brainstorm", help="对话式选题")
    pb.add_argument("--seed", default="")
    pb.add_argument("--format", choices=["text", "md", "json"], default="")
    pb.add_argument("--out", default="")
    pb.set_defaults(func=cmd_brainstorm)

    pw = sub.add_parser("write", help="在风格约束下起草")
    pw.add_argument("topic")
    pw.add_argument("--persona", default="")
    pw.add_argument("--payoff", default="")
    pw.add_argument("--formula", default="")
    pw.add_argument("--skeleton", default="")
    pw.add_argument("--out", default="")
    pw.set_defaults(func=cmd_write)

    pc = sub.add_parser("coach", help="教练诊断")
    pc.add_argument("draft")
    pc.add_argument("--format", choices=["text", "md", "json"], default="")
    pc.add_argument("--out", default="")
    pc.add_argument("--feedback", action="append", default=[])
    pc.set_defaults(func=cmd_coach)

    pl = sub.add_parser("polish", help="打分模式（轻量）")
    pl.add_argument("draft")
    pl.set_defaults(func=cmd_polish)

    pcr = sub.add_parser("critique", help="Allen 风格诊断（留白/AI腔/带读者/共鸣/邀请语）")
    pcr.add_argument("draft")
    pcr.add_argument("--merged", action="store_true", help="同时合并工程打分")
    pcr.add_argument("--allen-weight", type=float, default=None)
    pcr.add_argument("--format", choices=["text", "md", "json"], default="")
    pcr.add_argument("--out", default="")
    pcr.set_defaults(func=cmd_critique)

    pco = sub.add_parser("coin", help="造词工具（Allen 待修炼方向之一）")
    pco.add_argument("--brand", required=True)
    pco.add_argument("--value", default="")
    pco.add_argument("--n", type=int, default=8)
    pco.set_defaults(func=cmd_coin)

    pse = sub.add_parser("series", help="栏目化设计 + 互动阶梯")
    pse.add_argument("--theme", required=True)
    pse.add_argument("--persona", default="")
    pse.add_argument("--n", type=int, default=5)
    pse.set_defaults(func=cmd_series)

    psm = sub.add_parser("simulate", help="模拟多读者画像走完文案的情绪流")
    psm.add_argument("draft")
    psm.set_defaults(func=cmd_simulate)

    pre = sub.add_parser("reverse", help="对标笔记反向拆解（URL → 公式/骨架/钩子/Allen 5 维）")
    pre.add_argument("--url", default="")
    pre.add_argument("--in", dest="path", default="")
    pre.add_argument("--add-baseline", action="store_true")
    pre.add_argument("--format", choices=["text", "md", "json"], default="")
    pre.set_defaults(func=cmd_reverse)

    pcv = sub.add_parser("cover", help="封面文案 + 版式建议（3 套方案）")
    pcv.add_argument("draft")
    pcv.add_argument("--niche", default="")
    pcv.set_defaults(func=cmd_cover)

    prw = sub.add_parser("rewrite", help="LLM 自动改写（去 AI 腔 + 范本范）")
    prw.add_argument("draft")
    prw.set_defaults(func=cmd_rewrite)

    pci = sub.add_parser("coach-iterate",
                         help="渐进式教练 — 一次只 focus 一维（推荐用法）")
    pci.add_argument("draft")
    pci.add_argument("--focus", default="",
                     help="强制 focus 某维：jarvis_trap/ai_speak/teach_vs_lead/resonance/breath/invitation")
    pci.add_argument("--history", action="store_true")
    pci.add_argument("--reset", action="store_true")
    pci.set_defaults(func=cmd_coach_iterate)

    pdr = sub.add_parser("drafts", help="草稿版本管理（list/new/add/diff/show/promote）")
    pdr.add_argument("passthrough", nargs=argparse.REMAINDER,
                     help="直接转发给 drafts.py")
    pdr.set_defaults(func=cmd_drafts)

    ptd = sub.add_parser("today", help="今日选题推荐（节气 + 公式轮换 + 风格画像）")
    ptd.add_argument("--n", type=int, default=3)
    ptd.add_argument("--format", choices=["text", "md", "json"], default="")
    ptd.add_argument("--out", default="")
    ptd.set_defaults(func=cmd_today)

    pfi = sub.add_parser("find", help="跨数据全文搜索（drafts/baseline/posts/reviews/iter）")
    pfi.add_argument("query")
    pfi.add_argument("--in", dest="source", default="all",
                     choices=["all", "drafts", "baseline", "posts", "reviews", "iter"])
    pfi.add_argument("--regex", action="store_true")
    pfi.add_argument("--word", action="store_true")
    pfi.add_argument("--limit", type=int, default=10)
    pfi.set_defaults(func=cmd_find)

    pwz = sub.add_parser("wizard", help="五步上手向导（新用户首选）")
    pwz.add_argument("--baseline", nargs="*", default=[])
    pwz.add_argument("--rerun", action="store_true")
    pwz.set_defaults(func=cmd_wizard)

    pan = sub.add_parser("annual", help="月/季/年度创作年鉴")
    pan.add_argument("--months", type=int, default=12)
    pan.add_argument("--out", default="")
    pan.set_defaults(func=cmd_annual)

    pfm = sub.add_parser("frameworks",
                         help="商业文案框架工具（jiaoxia/ab/key/spark）")
    pfm.add_argument("passthrough", nargs=argparse.REMAINDER)
    pfm.set_defaults(func=cmd_frameworks)

    psc = sub.add_parser("scene", help="每日场景词触发器（解 AI 场景库窄）")
    psc.add_argument("--n", type=int, default=5)
    psc.add_argument("--category", default="")
    psc.add_argument("--history", action="store_true")
    psc.set_defaults(func=cmd_scene)

    pcs = sub.add_parser("case", help="案例库苏格拉底学习（list/study/show/related/history）")
    pcs.add_argument("passthrough", nargs=argparse.REMAINDER)
    pcs.set_defaults(func=cmd_case)

    pp = sub.add_parser("publish", help="进入发布前流程")
    pp.add_argument("draft")
    pp.set_defaults(func=cmd_publish)

    pr = sub.add_parser("review", help="周/月复盘")
    pr.add_argument("--days", type=int, default=7)
    pr.add_argument("--out", default="")
    pr.set_defaults(func=cmd_review)

    pe = sub.add_parser("learn", help="教助手一条规则（短语法）")
    pe.add_argument("rules", nargs="+",
                    help="如 disable=emoji  add-sensitive=卷王  allow=最佳  max-emoji=4")
    pe.set_defaults(func=cmd_learn)

    pv = sub.add_parser("evolve", help="基于 feedback 自动演进规则")
    pv.add_argument("--threshold", type=int, default=3)
    pv.set_defaults(func=cmd_evolve)

    pps = sub.add_parser("preset", help="切风格预设：allen / engineer / balanced")
    pps.add_argument("name", nargs="?", default="")
    pps.add_argument("--list", action="store_true")
    pps.set_defaults(func=cmd_preset)

    pwm = sub.add_parser("warmup", help="创作热身（动笔前2分钟唤醒仪式）")
    pwm.add_argument("--quick", action="store_true")
    pwm.add_argument("--freewrite", action="store_true")
    pwm.set_defaults(func=cmd_warmup)

    pbr = sub.add_parser("browser", help="浏览器桥接（CDP 安全浏览小红书）")
    pbr.add_argument("action", nargs="?", default="status",
                     choices=["start", "stop", "status", "explore", "search", "note", "analyze"])
    pbr.add_argument("target", nargs="?", default="",
                     help="搜索关键词 或 笔记URL")
    pbr.set_defaults(func=cmd_browser)

    pph = sub.add_parser("philosophy", help="创作哲学速查（动笔前30秒8问）")
    pph.add_argument("--layer", type=int, choices=[1, 2, 3, 4, 5])
    pph.add_argument("--mantra", action="store_true")
    pph.add_argument("--checklist", action="store_true")
    pph.set_defaults(func=cmd_philosophy)

    return p


def main() -> int:
    args = build_parser().parse_args()
    if not getattr(args, "cmd", None):
        # 默认 = status
        return cmd_status(argparse.Namespace())
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
