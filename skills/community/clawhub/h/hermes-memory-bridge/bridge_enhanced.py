#!/usr/bin/env python3
"""
hermes-memory-bridge / bridge.py - 增强版
添加学习材料同步功能
"""

import json
import sys
import textwrap
from datetime import datetime

from config import HERMES_DB
from memory_writer import read_shared_events as read_bridge_events, read_workbuddy_log
from queries import (
    get_recent_sessions,
    get_session_messages,
    get_session_stats,
    read_hermes_memory,
    search_fts,
    search_messages,
)
from sync import (
    read_bridge_status,
    search_both_memories,
    sync_hermes_to_workbuddy_context,
    sync_workbuddy_to_hermes,
)

# 导入学习材料同步模块
try:
    from hermes_learning_sync import sync_learning_materials, get_learning_stats
    HAS_LEARNING_SYNC = True
except ImportError:
    HAS_LEARNING_SYNC = False


def cmd_sync_to_hermes(args: list) -> None:
    """同步 WorkBuddy 工作到 Hermes"""
    summary = args[0] if args else ""
    work_type = args[1] if len(args) > 1 else "task"
    tags = args[2:] if len(args) > 2 else []

    if not summary:
        print("❌ 需要提供工作摘要")
        print("用法: sync_to_hermes <summary> <work_type> [tags...]")
        return

    result = sync_workbuddy_to_hermes(summary, work_type, tags)
    print("✅ 已同步到 Hermes")
    print(f"   记忆条目: {result['entry'][:80]}...")
    print(f"   日志路径: {result['log_path']}")


def cmd_sync_from_hermes(args: list) -> None:
    """从 Hermes 同步上下文到 WorkBuddy"""
    days = int(args[0]) if args else 7
    result = sync_hermes_to_workbuddy_context(days)
    print(result["summary_text"])


def cmd_search(args: list) -> None:
    """跨系统搜索"""
    if not args:
        print("❌ 需要提供搜索关键词")
        print("用法: search <keyword> [days]")
        return

    keyword = args[0]
    days = int(args[1]) if len(args) > 1 else 30

    results = search_both_memories(keyword, days)
    from sync import _format_results_for_user
    print(_format_results_for_user(results, keyword))


def cmd_status(args: list) -> None:
    """显示桥接状态"""
    status = read_bridge_status()
    print("=" * 48)
    print("  Hermes-Memory-Bridge 状态总览")
    print("=" * 48)
    print(f"  数据库:      {'✅ 存在' if status['db_exists'] else '❌ 缺失'}")
    print(f"  记忆文件:    {', '.join(status['hermes_memory_files']) or '无'}")
    print(f"  共用文件:    {', '.join(status['shared_files'])[:40]}...")
    print(f"  近期事件:    {len(status['recent_events'])} 条")
    print("=" * 48)
    
    for ev in status["recent_events"][:3]:
        ts = ev.get("timestamp", "").split("T")[0]
        ev_type = ev.get("type", "unknown")
        summary = ev.get("summary", "")[:40]
        print(f"  [{ts}] {ev_type}: {summary}...")


def cmd_stats(args: list) -> None:
    """显示统计信息"""
    days = int(args[0]) if args else 7
    stats = get_session_stats(days)
    print(f"📊 Hermes 近 {days} 天统计")
    print(f"   会话数:   {stats.get('total_sessions', 0)}")
    print(f"   消息数:   {stats.get('total_messages', 0)}")
    print(f"   Token数: {stats.get('total_tokens', 0):,}")
    print(f"   估算费用: ${stats.get('estimated_cost_usd', 0):.4f}")


def cmd_sessions(args: list) -> None:
    """显示会话列表"""
    days = int(args[0]) if args else 7
    limit = int(args[1]) if len(args) > 1 else 10

    sessions = get_recent_sessions(days, limit)
    print(f"📋 近 {days} 天会话（共 {len(sessions)} 条）")
    for s in sessions:
        ts = datetime.fromtimestamp(s["started_at"]).strftime("%m-%d %H:%M")
        title = s.get("title") or s["source"] or "无标题"
        msg_count = s.get("message_count", 0)
        cost = s.get("estimated_cost_usd", 0)
        print(f"  [{ts}] {title} | {msg_count}条消息 | ${cost:.4f}")


def cmd_memory(args: list) -> None:
    """读取 Hermes 记忆"""
    target = args[0] if args else "memory"
    mem = read_hermes_memory()
    
    if target == "memory":
        entries = mem.get("MEMORY.md", {}).get("entries", [])
        print(f"🧠 Hermes MEMORY.md（共 {len(entries)} 条记忆）")
        print("-" * 48)
        for i, entry in enumerate(entries[-10:], 1):
            print(f"  [{i}] {entry[:80]}...")
    elif target == "user":
        entries = mem.get("USER.md", {}).get("entries", [])
        print(f"👤 Hermes USER.md（共 {len(entries)} 条用户记忆）")
        print("-" * 48)
        for i, entry in enumerate(entries[-10:], 1):
            print(f"  [{i}] {entry[:80]}...")
    else:
        print("❌ 未知目标，使用 'memory' 或 'user'")


def cmd_events(args: list) -> None:
    """显示桥接事件"""
    limit = int(args[0]) if args else 10
    events = read_bridge_events(limit=limit)
    print(f"🔗 桥接事件历史（共 {len(events)} 条）")
    for ev in events:
        ts = ev.get("timestamp", "").split("T")[1][:8]
        ev_type = ev.get("type", "unknown")
        summary = ev.get("summary", "")[:60]
        print(f"  [{ts}] {ev_type}: {summary}...")


def cmd_learning_sync(args: list) -> None:
    """同步学习材料到 WorkBuddy"""
    if not HAS_LEARNING_SYNC:
        print("❌ 学习材料同步模块未找到")
        print("请确保 hermes_learning_sync.py 在技能目录中")
        return
    
    print("🔄 开始同步 Hermes 学习材料到 WorkBuddy...")
    success = sync_learning_materials()
    
    if success:
        print("✅ 学习材料同步完成！")
        stats = get_learning_stats()
        print(f"📊 同步统计:")
        print(f"  学习材料: {stats.get('materials_count', 0)} 类")
        print(f"  记忆条目: {stats.get('summary_entries', 0)} 条")
        print(f"  关键学习点: {stats.get('key_insights', 0)} 个")
    else:
        print("❌ 学习材料同步失败")


def cmd_learning_stats(args: list) -> None:
    """显示学习材料统计"""
    if not HAS_LEARNING_SYNC:
        print("❌ 学习材料同步模块未找到")
        return
    
    stats = get_learning_stats()
    print("📚 Hermes 学习材料统计")
    print("=" * 40)
    print(f"最后同步: {stats.get('last_sync_time', '从未同步')}")
    print(f"学习材料: {stats.get('materials_count', 0)} 类")
    print(f"记忆条目: {stats.get('summary_entries', 0)} 条")
    print(f"关键学习点: {stats.get('key_insights', 0)} 个")
    print(f"同步状态: {stats.get('status', 'unknown')}")


def cmd_help() -> None:
    """显示帮助信息"""
    help_text = """
hermes-memory-bridge 命令列表:

  基础命令:
    sync_to_hermes    <summary> <work_type> [tags...]
    sync_from_hermes  [days]
    search            <keyword> [days]
    status
    stats             [days]
    sessions          [days] [limit]
    memory            [memory|user]
    events            [limit]

  学习材料命令 (新增):
    learning_sync     同步 Hermes 学习材料到 WorkBuddy
    learning_stats    显示学习材料统计

  帮助:
    help              显示此帮助信息

示例:
  python3 bridge.py sync_to_hermes "完成XXX任务" work "tag1,tag2"
  python3 bridge.py search "MCP" 7
  python3 bridge.py learning_sync
  python3 bridge.py status
    """
    print(textwrap.dedent(help_text).strip())


def main():
    if len(sys.argv) < 2:
        cmd_help()
        return

    command = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        "sync_to_hermes": cmd_sync_to_hermes,
        "sync_from_hermes": cmd_sync_from_hermes,
        "search": cmd_search,
        "status": cmd_status,
        "stats": cmd_stats,
        "sessions": cmd_sessions,
        "memory": cmd_memory,
        "events": cmd_events,
        "learning_sync": cmd_learning_sync,
        "learning_stats": cmd_learning_stats,
        "help": cmd_help,
    }

    if command in commands:
        try:
            commands[command](args)
        except Exception as e:
            print(f"❌ 命令执行错误: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"❌ 未知命令: {command}")
        cmd_help()


if __name__ == "__main__":
    main()