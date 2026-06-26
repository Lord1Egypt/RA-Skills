#!/usr/bin/env python3
"""
hermes-memory-bridge / bridge_enhanced.py - v1.1.0 兼容版
添加学习材料同步功能，与 v1.1.0 改进完全兼容
"""

import sys
import textwrap
from datetime import datetime

from config import _get_logger, logger

logger = _get_logger("bridge_enhanced")

# 导入基础模块
try:
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
    HAS_BASE_MODULES = True
except ImportError as e:
    logger.error(f"导入基础模块失败: {e}")
    HAS_BASE_MODULES = False

# 导入学习材料同步模块
try:
    from hermes_learning_sync import sync_learning_materials, get_learning_stats
    HAS_LEARNING_SYNC = True
except ImportError:
    logger.warning("学习材料同步模块未找到，相关功能将不可用")
    HAS_LEARNING_SYNC = False


def cmd_sync_to_hermes(args: list) -> bool:
    """同步 WorkBuddy 工作到 Hermes，返回是否成功"""
    if not HAS_BASE_MODULES:
        print("❌ 基础模块加载失败")
        return False
    
    summary = args[0] if args else ""
    work_type = args[1] if len(args) > 1 else "task"
    tags = args[2:] if len(args) > 2 else []

    if not summary:
        print("用法: sync_to_hermes <summary> [work_type] [tags...]", file=sys.stderr)
        return False

    try:
        result = sync_workbuddy_to_hermes(summary, work_type, tags)
    except Exception as e:
        logger.error(f"同步失败: {e}")
        print(f"❌ 同步失败: {e}")
        return False

    if result["status"] in ("synced", "partial"):
        icon = "✅" if result["status"] == "synced" else "⚠️"
        print(f"{icon} 已同步到 Hermes（{result['status']}）")
        if result.get("entry"):
            print(f"   记忆: {result['entry'][:80]}...")
        if result.get("log_path"):
            print(f"   日志: {result['log_path']}")
        return True
    else:
        print(f"❌ 同步失败（全部写入操作均未成功）")
        return False


def cmd_sync_from_hermes(args: list) -> bool:
    """拉取 Hermes 最新上下文到 WorkBuddy"""
    if not HAS_BASE_MODULES:
        print("❌ 基础模块加载失败")
        return False
    
    days = int(args[0]) if args else 7
    try:
        result = sync_hermes_to_workbuddy_context(days=days)
        print(result["summary_text"])
        return True
    except Exception as e:
        logger.error(f"拉取 Hermes 上下文失败: {e}")
        print(f"❌ 拉取失败: {e}")
        return False


def cmd_search(args: list) -> bool:
    """跨 WorkBuddy + Hermes 全文搜索"""
    if not HAS_BASE_MODULES:
        print("❌ 基础模块加载失败")
        return False
    
    keyword = args[0] if args else ""
    days = int(args[1]) if len(args) > 1 else 30

    if not keyword:
        print("用法: search <keyword> [days]", file=sys.stderr)
        return False

    try:
        results = search_both_memories(keyword, days=days)
    except Exception as e:
        logger.error(f"搜索失败: {e}")
        print(f"❌ 搜索失败: {e}")
        return False

    from sync import _format_results_for_user
    print(_format_results_for_user(results, keyword))
    return True


def cmd_status(args: list) -> bool:
    """显示桥接状态"""
    if not HAS_BASE_MODULES:
        print("❌ 基础模块加载失败")
        return False
    
    try:
        status = read_bridge_status()
    except Exception as e:
        logger.error(f"读取状态失败: {e}")
        print(f"❌ 读取状态失败: {e}")
        return False

    print("=" * 48)
    print("  Hermes-Memory-Bridge 状态总览 (增强版)")
    print("=" * 48)
    print(f"  数据库:      {'✅ 存在' if status['db_exists'] else '❌ 缺失'}")
    
    # 显示 WorkBuddy 记忆目录（如果找到）
    wb_mem_dir = status.get('workbuddy_memory_dir')
    if wb_mem_dir:
        print(f"  WorkBuddy 记忆: {wb_mem_dir}")
    
    print(f"  记忆文件:    {', '.join(status['hermes_memory_files']) or '无'}")
    print(f"  共用文件:    {', '.join(status['shared_files'])[:40]}...")
    print(f"  近期事件:    {len(status['recent_events'])} 条")
    print("=" * 48)
    
    for ev in status["recent_events"][:3]:
        ts = ev.get("timestamp", "").split("T")[0]
        ev_type = ev.get("type", "unknown")
        summary = ev.get("summary", "")[:40]
        print(f"  [{ts}] {ev_type}: {summary}...")
    
    return True


def cmd_stats(args: list) -> bool:
    """显示统计信息"""
    if not HAS_BASE_MODULES:
        print("❌ 基础模块加载失败")
        return False
    
    days = int(args[0]) if args else 7
    try:
        stats = get_session_stats(days)
    except Exception as e:
        logger.error(f"获取统计失败: {e}")
        print(f"❌ 获取统计失败: {e}")
        return False
    
    print(f"📊 Hermes 近 {days} 天统计")
    print(f"   会话数:   {stats.get('total_sessions', 0)}")
    print(f"   消息数:   {stats.get('total_messages', 0)}")
    print(f"   Token数: {stats.get('total_tokens', 0):,}")
    print(f"   估算费用: ${stats.get('estimated_cost_usd', 0):.4f}")
    return True


def cmd_sessions(args: list) -> bool:
    """显示会话列表"""
    if not HAS_BASE_MODULES:
        print("❌ 基础模块加载失败")
        return False
    
    days = int(args[0]) if args else 7
    limit = int(args[1]) if len(args) > 1 else 10

    try:
        sessions = get_recent_sessions(days, limit)
    except Exception as e:
        logger.error(f"获取会话列表失败: {e}")
        print(f"❌ 获取会话列表失败: {e}")
        return False
    
    print(f"📋 近 {days} 天会话（共 {len(sessions)} 条）")
    for s in sessions:
        ts = datetime.fromtimestamp(s["started_at"]).strftime("%m-%d %H:%M")
        title = s.get("title") or s["source"] or "无标题"
        msg_count = s.get("message_count", 0)
        cost = s.get("estimated_cost_usd", 0)
        print(f"  [{ts}] {title} | {msg_count}条消息 | ${cost:.4f}")
    
    return True


def cmd_memory(args: list) -> bool:
    """读取 Hermes 记忆"""
    if not HAS_BASE_MODULES:
        print("❌ 基础模块加载失败")
        return False
    
    target = args[0] if args else "memory"
    
    try:
        mem = read_hermes_memory()
    except Exception as e:
        logger.error(f"读取记忆失败: {e}")
        print(f"❌ 读取记忆失败: {e}")
        return False
    
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
        return False
    
    return True


def cmd_events(args: list) -> bool:
    """显示桥接事件"""
    if not HAS_BASE_MODULES:
        print("❌ 基础模块加载失败")
        return False
    
    limit = int(args[0]) if args else 10
    
    try:
        events = read_bridge_events(limit=limit)
    except Exception as e:
        logger.error(f"读取事件失败: {e}")
        print(f"❌ 读取事件失败: {e}")
        return False
    
    print(f"🔗 桥接事件历史（共 {len(events)} 条）")
    for ev in events:
        ts = ev.get("timestamp", "").split("T")[1][:8]
        ev_type = ev.get("type", "unknown")
        summary = ev.get("summary", "")[:60]
        print(f"  [{ts}] {ev_type}: {summary}...")
    
    return True


def cmd_learning_sync(args: list) -> bool:
    """同步学习材料到 WorkBuddy"""
    if not HAS_LEARNING_SYNC:
        print("❌ 学习材料同步模块未找到")
        print("请确保 hermes_learning_sync.py 在技能目录中")
        return False
    
    print("🔄 开始同步 Hermes 学习材料到 WorkBuddy...")
    
    try:
        success = sync_learning_materials()
    except Exception as e:
        logger.error(f"学习材料同步失败: {e}")
        print(f"❌ 学习材料同步失败: {e}")
        return False
    
    if success:
        print("✅ 学习材料同步完成！")
        try:
            stats = get_learning_stats()
            print(f"📊 同步统计:")
            print(f"  学习材料: {stats.get('materials_count', 0)} 类")
            print(f"  记忆条目: {stats.get('summary_entries', 0)} 条")
            print(f"  关键学习点: {stats.get('key_insights', 0)} 个")
        except Exception as e:
            logger.warning(f"获取统计失败: {e}")
    else:
        print("❌ 学习材料同步失败")
    
    return success


def cmd_learning_stats(args: list) -> bool:
    """显示学习材料统计"""
    if not HAS_LEARNING_SYNC:
        print("❌ 学习材料同步模块未找到")
        return False
    
    try:
        stats = get_learning_stats()
    except Exception as e:
        logger.error(f"获取学习统计失败: {e}")
        print(f"❌ 获取学习统计失败: {e}")
        return False
    
    print("📚 Hermes 学习材料统计")
    print("=" * 40)
    print(f"最后同步: {stats.get('last_sync_time', '从未同步')}")
    print(f"学习材料: {stats.get('materials_count', 0)} 类")
    print(f"记忆条目: {stats.get('summary_entries', 0)} 条")
    print(f"关键学习点: {stats.get('key_insights', 0)} 个")
    print(f"同步状态: {stats.get('status', 'unknown')}")
    
    return True


def cmd_help() -> bool:
    """显示帮助信息"""
    help_text = """
hermes-memory-bridge 增强版命令列表 (v1.1.0 兼容)

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

环境变量:
  HERMES_HOME          Hermes 根目录（默认 ~/.hermes）
  WORKBUDDY_HOME      WorkBuddy 根目录（默认 ~/WorkBuddy）
  WORKBUDDY_MEMORY_DIR 强制指定 WorkBuddy 记忆目录
  BRIDGE_LOG_LEVEL    日志级别 DEBUG|INFO|WARNING|ERROR

示例:
  python3 bridge_enhanced.py sync_to_hermes "完成XXX任务" work "tag1,tag2"
  python3 bridge_enhanced.py search "MCP" 7
  python3 bridge_enhanced.py learning_sync
  python3 bridge_enhanced.py status
    """
    print(textwrap.dedent(help_text).strip())
    return True


def main():
    if len(sys.argv) < 2:
        cmd_help()
        sys.exit(0)

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
            success = commands[command](args)
            sys.exit(0 if success else 1)
        except Exception as e:
            logger.error(f"命令执行错误: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    else:
        print(f"❌ 未知命令: {command}")
        cmd_help()
        sys.exit(1)


if __name__ == "__main__":
    main()