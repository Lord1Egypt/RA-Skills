#!/usr/bin/env python3
"""
MemCore CLI — 对标 MemOS 的记忆增强系统命令行入口。

用法:
  python3 -m scripts.memcore.cli index              # 解析所有日志 → L1 traces
  python3 -m scripts.memcore.cli induce             # L1 → L2 模式归纳
  python3 -m scripts.memcore.cli search <query>     # 三层检索
  python3 -m scripts.memcore.cli crystallize        # 扫描可结晶的 Skills
  python3 -m scripts.memcore.cli feedback           # 运行反馈衰减
  python3 -m scripts.memcore.cli stats              # 系统状态
  python3 -m scripts.memcore.cli run-all            # 运行完整流程
  python3 -m scripts.memcore.cli update-memory      # 更新 MEMORY.md（自动提取教训）
"""

import argparse
import sys
from pathlib import Path

# Add workspace to path
_ws = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_ws))


def cmd_index(args):
    """解析 memory/ 目录下所有日志 + SESSION-STATE.md 为 L1 traces"""
    from scripts.memcore.trace import DailyLogParser, TraceIndex

    memory_dir = Path.home() / ".openclaw" / "workspace" / "memory"
    index = TraceIndex()

    log_files = sorted(memory_dir.glob("20*.md"))
    print(f"📂 扫描到 {len(log_files)} 个日志文件")

    total = 0
    for f in log_files:
        entries = DailyLogParser.parse_file(f)
        if entries:
            n = index.insert_batch(entries)
            total += n
            print(f"  {f.name}: {len(entries)} sections → {n} traces")

    # ⭐ WAL Protocol: also index SESSION-STATE.md
    session_state = Path.home() / ".openclaw" / "workspace" / "SESSION-STATE.md"
    if session_state.exists():
        wal_entries = DailyLogParser.parse_session_state(session_state)
        if wal_entries:
            n_wal = index.insert_batch(wal_entries)
            total += n_wal
            print(f"  SESSION-STATE.md (WAL): {len(wal_entries)} entries → {n_wal} traces")

    print(f"\n✅ 总计 {total} 条 L1 traces 已索引")
    d_min, d_max = index.date_range()
    print(f"📅 日期范围: {d_min} ~ {d_max}")


def cmd_induce(args):
    """从 L1 traces 归纳 L2 patterns"""
    from scripts.memcore.pattern import PatternInducer

    inducer = PatternInducer()
    patterns = inducer.induce()

    print(f"🔍 从 traces 中归纳出 {len(patterns)} 个模式:\n")
    for i, p in enumerate(patterns, 1):
        tags = ", ".join(p.tags) if p.tags else "无"
        print(f"  {i}. [{p.confidence:.0%}] {p.name}")
        print(f"     频率: {p.frequency}次 | 标签: {tags}")
        print(f"     {p.description[:120]}")
        print()

    # 高置信度模式建议写入 MEMORY.md
    high_conf = [p for p in patterns if p.confidence >= 0.8]
    if high_conf:
        print(f"💡 {len(high_conf)} 个高置信度模式可考虑写入 MEMORY.md")


def cmd_search(args):
    """三层检索"""
    from scripts.memcore.retriever import ThreeTierRetriever

    retriever = ThreeTierRetriever()
    results = retriever.retrieve(args.query, max_results=args.limit)

    tier_names = {1: "🎯 Skill", 2: "📊 Trace", 3: "🌍 WorldModel"}
    print(f"🔍 '{args.query}' → {len(results)} 条结果:\n")

    for i, r in enumerate(results, 1):
        tier_label = tier_names.get(r.tier, f"T{r.tier}")
        print(f"  {i}. {tier_label} [{r.score:.2f}] {r.source}")
        # 截断内容
        content_preview = r.content[:150].replace("\n", " ")
        print(f"     {content_preview}...")
        print()


def cmd_crystallize(args):
    """扫描可结晶的 Skills"""
    from scripts.memcore.crystallize import SkillCrystallizer

    crystallizer = SkillCrystallizer()
    suggestions = crystallizer.scan_candidates()

    if not suggestions:
        print("📭 暂无可结晶的 Skill")
        return

    print(f"💎 {len(suggestions)} 个 Skill 结晶建议:\n")
    for i, s in enumerate(suggestions, 1):
        action_emoji = {"create": "🆕", "update": "📝", "merge": "🔀"}
        emoji = action_emoji.get(s.action, "❓")
        print(f"  {i}. {emoji} {s.action.upper()}: {s.skill_name}")
        print(f"     模式: {s.pattern_name}")
        print(f"     原因: {s.reason}")
        print(f"     置信度: {s.confidence:.0%}")
        if args.verbose:
            print(f"     模板:\n{s.template_content[:500]}")
        print()


def cmd_feedback(args):
    """运行反馈衰减"""
    from scripts.memcore.feedback import FeedbackLoop

    loop = FeedbackLoop()
    loop.apply_decay_if_needed()
    stats = loop.get_stats()

    print("📊 反馈系统状态:")
    print(f"  总反馈事件: {stats['total_feedback']}")
    print(f"  总引用: {stats['total_references']}")
    print(f"  使用率: {stats['use_rate']:.1%}")
    print(f"  上次衰减: {stats['last_decay']}")


def cmd_stats(args):
    """系统状态"""
    from scripts.memcore.trace import TraceIndex
    from scripts.memcore.pattern import PatternInducer
    from scripts.memcore.feedback import FeedbackLoop

    print("🧠 MemCore 状态\n" + "=" * 40)

    # Traces
    idx = TraceIndex()
    count = idx.count()
    d_min, d_max = idx.date_range()
    print(f"📊 L1 Traces: {count} 条 ({d_min} ~ {d_max})")

    top = idx.top_by_value(5)
    if top:
        print("   Top 5 高价值记录:")
        for t in top:
            action_preview = t.action[:50]
            print(f"   [{t.value_score:.2f}] {t.date}: {action_preview}...")

    # Patterns
    inducer = PatternInducer()
    patterns = inducer.list_patterns(min_conf=0.5)
    hq = [p for p in patterns if p.confidence >= 0.8]
    print(f"\n📈 L2 Patterns: {len(patterns)} 个 ({len(hq)} 高置信度)")

    # Feedback
    loop = FeedbackLoop()
    stats = loop.get_stats()
    print(f"\n🔄 反馈: {stats['total_feedback']} 事件, 使用率 {stats['use_rate']:.1%}")


def cmd_run_all(args):
    """运行完整流程"""
    print("🚀 MemCore 完整流程\n")
    cmd_index(args)
    print("\n" + "-" * 40 + "\n")
    cmd_induce(args)
    print("\n" + "-" * 40 + "\n")
    cmd_crystallize(args)
    print("\n" + "-" * 40 + "\n")
    cmd_feedback(args)


def cmd_brief(args):
    """生成启动简报 MEMORY_BRIEF.md"""
    from scripts.memcore.bootstrap_context import generate_brief
    brief = generate_brief()
    brief_path = Path.home() / ".openclaw" / "workspace" / "MEMORY_BRIEF.md"
    brief_path.write_text(brief, encoding="utf-8")
    
    from scripts.memcore.bootstrap_context import count_tokens
    token_count = count_tokens(brief)
    
    print(brief)
    print(f"\n📄 已写入: {brief_path}")
    print(f"📊 Token: ~{token_count} (全量 MEMORY.md ~3500, 节省 {int((1 - token_count/3500) * 100)}%)")


def cmd_feedback_log(args):
    """记录记忆使用反馈"""
    from scripts.memcore.feedback import FeedbackLoop
    loop = FeedbackLoop()
    
    if args.action == "used":
        loop.record_implicit(args.trace_id, was_used=True)
        print(f"✅ trace {args.trace_id} 标记为已使用")
    elif args.action == "skipped":
        loop.record_implicit(args.trace_id, was_used=False)
        print(f"⏭️ trace {args.trace_id} 标记为跳过")
    elif args.action == "good":
        loop.record_explicit(args.trace_id, score=1.0, note=args.note or "")
        print(f"👍 trace {args.trace_id} 显式好评")
    elif args.action == "bad":
        loop.record_explicit(args.trace_id, score=-0.5, note=args.note or "")
        print(f"👎 trace {args.trace_id} 显式差评")
    elif args.action == "error":
        loop.record_error_feedback(args.trace_id, args.note or "")
        print(f"🚨 trace {args.trace_id} 错误复现反馈")


def cmd_vfm(args):
    """VFM 评分分析：对高价值 traces 计算四维评分"""
    from scripts.memcore.trace import TraceIndex
    from scripts.memcore.feedback import FeedbackLoop
    
    idx = TraceIndex()
    loop = FeedbackLoop()
    top = idx.top_by_value(20)
    
    print("📊 VFM 评分分析 (proactive-agent v3.1.0)\n" + "=" * 55)
    print(f"{'Trace':<8} {'VFM':>5} {'判定':<8} {'动作'}")
    print("-" * 55)
    
    for t in top[:10]:
        d = {"action": t.action, "reflection": t.reflection, 
             "observation": t.observation, "feedback_count": t.feedback_count}
        result = loop.vfm_score_trace(d)
        verdict = "✅✅" if result["total"] >= 70 else ("✅" if result["total"] >= 50 else "⏭️")
        action_preview = t.action[:35]
        print(f"{t.date:<8} {result['total']:>5.0f} {verdict:<8} {action_preview}")
    
    print(f"\n💡 VFM 阈值: {FeedbackLoop.VFM_THRESHOLD}分 (≥{FeedbackLoop.VFM_THRESHOLD}=采纳, <{FeedbackLoop.VFM_THRESHOLD}=跳过)")


def cmd_update_memory(args):
    """从 traces + patterns 生成 MEMORY.md 更新建议"""
    from scripts.memcore.trace import TraceIndex
    from scripts.memcore.pattern import PatternInducer

    idx = TraceIndex()
    top = idx.top_by_value(20)

    inducer = PatternInducer()
    inducer.induce()
    patterns = inducer.list_patterns(min_conf=0.7)

    print("📝 MEMORY.md 更新建议\n" + "=" * 50)

    # 最近7天高价值教训
    from datetime import date, timedelta
    today = date.today()
    week_ago = today - timedelta(days=7)

    print(f"\n## 近期教训 ({week_ago} ~ {today})\n")
    recent = [t for t in top if t.date >= week_ago.isoformat()]
    for t in recent[:5]:
        if t.reflection:
            print(f"- [{t.date}] {t.reflection[:120]}")

    # 新归纳的模式
    if patterns:
        print(f"\n## 自动归纳的模式 ({len(patterns)}个)\n")
        for p in patterns[:8]:
            print(f"- [{p.confidence:.0%}] {p.name}: {p.description[:100]}")

    # 未被引用但高价值的痕迹（可能需要关注）
    from scripts.memcore.feedback import FeedbackLoop
    loop = FeedbackLoop()
    unreferenced = [t for t in top if t.feedback_count == 0 and t.value_score >= 0.6]
    if unreferenced:
        print(f"\n## ⚠️ 高价值但未引用 ({len(unreferenced)}条)\n")
        for t in unreferenced[:5]:
            print(f"- [{t.date}] {t.action[:80]}")


def main():
    parser = argparse.ArgumentParser(
        description="MemCore — MemOS-inspired memory enhancement",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("index", help="解析日志 → L1 traces")
    sub.add_parser("induce", help="L1 → L2 模式归纳")
    p = sub.add_parser("search", help="三层检索")
    p.add_argument("query", help="搜索关键词")
    p.add_argument("-n", "--limit", type=int, default=10, help="最大结果数")
    p = sub.add_parser("crystallize", help="扫描可结晶 Skills")
    p.add_argument("-v", "--verbose", action="store_true", help="显示模板")
    sub.add_parser("feedback", help="运行反馈衰减")
    sub.add_parser("stats", help="系统状态")
    sub.add_parser("run-all", help="运行完整流程")
    sub.add_parser("brief", help="生成启动简报 MEMORY_BRIEF.md")
    p = sub.add_parser("feedback-log", help="记录记忆使用反馈")
    p.add_argument("trace_id", type=int, help="Trace ID")
    p.add_argument("action", choices=["used", "skipped", "good", "bad", "error"], help="反馈动作")
    p.add_argument("--note", "-m", default="", help="备注")
    sub.add_parser("vfm", help="VFM 评分分析 (proactive-agent)")
    sub.add_parser("update-memory", help="生成 MEMORY.md 更新建议")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return

    cmds = {
        "index": cmd_index,
        "induce": cmd_induce,
        "search": cmd_search,
        "crystallize": cmd_crystallize,
        "feedback": cmd_feedback,
        "stats": cmd_stats,
        "run-all": cmd_run_all,
        "brief": cmd_brief,
        "feedback-log": cmd_feedback_log,
        "vfm": cmd_vfm,
        "update-memory": cmd_update_memory,
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
