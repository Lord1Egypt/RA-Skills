#!/usr/bin/env python3
"""
hermes-memory-bridge / bridge.py
WorkBuddy 与 Hermes Agent 双向记忆互通主引擎

用法（作为 Skill 被 WorkBuddy 调用）：
    python3 bridge.py <command> [args...]

命令：
    sync_to_hermes    <summary> <work_type> [tags...]
    sync_from_hermes  [days]
    search            <keyword> [days]
    status
    stats             [days]
    sessions          [days] [limit]
    memory            [memory|user]
    events            [limit]
    help
"""
from __future__ import annotations

import json
import logging
import sys
import textwrap
from datetime import datetime
from pathlib import Path

from config import _get_logger, logger

logger = _get_logger("bridge")


def cmd_sync_to_hermes(args: list) -> bool:
    """同步 WorkBuddy 工作到 Hermes，返回是否成功"""
    from sync import sync_workbuddy_to_hermes

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
    from sync import sync_hermes_to_workbuddy_context

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
    from sync import search_both_memories

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

    _print_search_results(results, keyword)
    return True


def cmd_status(args: list) -> bool:
    """桥接状态总览"""
    from sync import read_bridge_status

    try:
        status = read_bridge_status()
    except Exception as e:
        logger.error(f"读取状态失败: {e}")
        print(f"❌ 读取状态失败: {e}")
        return False

    print("=" * 48)
    print("  Hermes-Memory-Bridge 状态总览")
    print("=" * 48)
    print(f"  数据库:      {'✅ 存在' if status['db_exists'] else '❌ 不存在'}")
    print(f"  WorkBuddy 记忆: {status.get('workbuddy_memory_dir') or '（未找到）'}")
    print(f"  记忆文件:    {', '.join(status['hermes_memory_files']) or '（暂无）'}")
    print(f"  共用文件:    {', '.join(status['shared_files']) or '（暂无）'}")
    print(f"  近期事件:    {len(status['recent_events'])} 条")
    print("=" * 48)

    for ev in status["recent_events"][-5:]:
        ts = ev.get("timestamp", "")[:16]
        etype = ev.get("type", "")
        # 去除 timestamp 字段避免重复显示
        ev_clean = {k: v for k, v in ev.items() if k != "timestamp"}
        info = json.dumps(ev_clean, ensure_ascii=False)[:60]
        print(f"  [{ts}] {etype}: {info}")
    return True


def cmd_stats(args: list) -> bool:
    """Hermes 使用统计"""
    from queries import get_session_stats

    days = int(args[0]) if args else 30
    try:
        stats = get_session_stats(days=days)
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
    """列出最近会话"""
    from queries import get_recent_sessions

    days = int(args[0]) if args else 7
    limit = int(args[1]) if len(args) > 1 else 10

    try:
        sessions = get_recent_sessions(days=days, limit=limit)
    except Exception as e:
        logger.error(f"获取会话列表失败: {e}")
        print(f"❌ 获取会话失败: {e}")
        return False

    if not sessions:
        print(f"近 {days} 天无会话记录")
        return True

    print(f"📋 近 {days} 天会话（共 {len(sessions)} 条）")
    for s in sessions:
        try:
            ts = datetime.fromtimestamp(s["started_at"]).strftime("%m-%d %H:%M")
        except (ValueError, KeyError, TypeError):
            ts = "??-?? ??:??"
        title = s.get("title") or s.get("source") or "无标题"
        msgs = s.get("message_count", 0)
        cost = s.get("estimated_cost_usd") or 0
        print(f"  [{ts}] {title} | {msgs}条消息 | ${cost:.4f}")
    return True


def cmd_memory(args: list) -> bool:
    """读取 Hermes 记忆文件"""
    from queries import read_hermes_memory

    target = args[0] if args else "memory"
    try:
        mem = read_hermes_memory()
    except Exception as e:
        logger.error(f"读取 Hermes 记忆失败: {e}")
        print(f"❌ 读取失败: {e}")
        return False

    key = "MEMORY.md" if target == "memory" else "USER.md"
    data = mem.get(key, {})
    entries = data.get("entries", [])

    print(f"🧠 Hermes {key}（共 {len(entries)} 条记忆）")
    print("-" * 48)
    if not entries:
        print("  （记忆为空）")
    else:
        for i, entry in enumerate(entries, 1):
            print(f"  [{i}] {entry[:300]}")
            print()
    return True


def cmd_events(args: list) -> bool:
    """读取桥接事件历史"""
    from memory_writer import read_shared_events

    limit = int(args[0]) if args else 20
    try:
        events = read_shared_events(limit=limit)
    except Exception as e:
        logger.error(f"读取事件历史失败: {e}")
        print(f"❌ 读取失败: {e}")
        return False

    print(f"🔗 桥接事件历史（共 {len(events)} 条）")
    for ev in events[-limit:]:
        ts = ev.get("timestamp", "")[:16]
        etype = ev.get("type", "")
        ev_clean = {k: v for k, v in ev.items() if k != "timestamp"}
        info = json.dumps(ev_clean, ensure_ascii=False)[:100]
        print(f"  [{ts}] {etype}: {info}")
    return True


def _print_search_results(results: dict, keyword: str) -> None:
    print(f"\n🔍 搜索「{keyword}」\n")

    hermes = results.get("hermes", [])
    workbuddy = results.get("workbuddy", [])

    if hermes:
        print(f"**Hermes 会话**（{len(hermes)} 条）")
        for r in hermes[:5]:
            try:
                ts = (
                    datetime.fromtimestamp(r["timestamp"]).strftime("%m-%d %H:%M")
                    if isinstance(r.get("timestamp"), float)
                    else "?"
                )
            except (ValueError, TypeError):
                ts = "?"
            role = r.get("role", "")
            content = (r.get("content") or "")[:120]
            print(f"  [{ts}] [{role}]: {content}...")
    else:
        print("**Hermes 会话**：无匹配结果")

    print()

    if workbuddy:
        print(f"**WorkBuddy 记忆文件**（{len(workbuddy)} 条）")
        for r in workbuddy[:5]:
            print(f"  [{r['file']}:{r['line']}] {r['snippet']}")
    else:
        print("**WorkBuddy 记忆文件**：无匹配结果")


def main() -> int:
    """返回退出码：0=成功，1=失败"""
    if len(sys.argv) < 2 or sys.argv[1] == "help":
        print(textwrap.dedent("""
        hermes-memory-bridge v1.1.0
        用法: python3 bridge.py <command> [args...]

        命令:
          sync_to_hermes   <summary> [work_type] [tags...]
          sync_from_hermes [days]
          search           <keyword> [days]
          status
          stats            [days]
          sessions         [days] [limit]
          memory           [memory|user]
          events           [limit]

        环境变量:
          HERMES_HOME           Hermes 根目录（默认 ~/.hermes）
          WORKBUDDY_HOME        WorkBuddy 根目录（默认 ~/WorkBuddy）
          BRIDGE_LOG_LEVEL      DEBUG|INFO|WARNING|ERROR（默认 INFO）
        """.strip()))
        return 0

    cmd = sys.argv[1]
    args = sys.argv[2:]

    commands: dict[str, tuple] = {
        "sync_to_hermes":   (cmd_sync_to_hermes,   "同步工作到 Hermes"),
        "sync_from_hermes": (cmd_sync_from_hermes, "拉取 Hermes 上下文"),
        "search":           (cmd_search,           "跨系统搜索"),
        "status":          (cmd_status,            "桥接状态"),
        "stats":           (cmd_stats,             "Hermes 统计"),
        "sessions":        (cmd_sessions,           "会话列表"),
        "memory":          (cmd_memory,             "读取记忆"),
        "events":          (cmd_events,             "事件历史"),
    }

    if cmd not in commands:
        print(f"未知命令: {cmd}", file=sys.stderr)
        print(f"可用命令: {', '.join(commands)}", file=sys.stderr)
        return 1

    handler, description = commands[cmd]
    logger.info(f"执行命令: {cmd} {args}")

    try:
        success = handler(args)
    except Exception as e:
        logger.exception(f"命令 {cmd} 异常: {e}")
        print(f"❌ 命令执行异常: {e}", file=sys.stderr)
        return 1

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
