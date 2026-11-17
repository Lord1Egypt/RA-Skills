#!/usr/bin/env python3
"""
Environment Detection — 自动检测 OpenClaw / Claude Code 环境

OpenClaw 为主路径，Claude Code 为兼容降级。
所有脚本 import 此模块获取路径，不硬编码。
"""

import os

def get_paths():
    """检测环境并返回路径字典。OpenClaw 优先，Claude Code 降级。"""
    openclaw_ws = os.path.expanduser("~/.openclaw/workspace")
    claude_mem = os.path.expanduser("~/.claude/memory")

    if os.path.isdir(openclaw_ws):
        env = "openclaw"
        base = openclaw_ws
        daily_dir = os.path.join(base, "memory")
        learnings_dir = os.path.join(base, ".learnings")
        narratives_dir = os.path.join(base, "memory", "narratives")
        archive_dir = os.path.join(base, "memory", "archive")
    elif os.path.isdir(claude_mem):
        env = "claude_code"
        base = claude_mem
        daily_dir = os.path.join(base, "daily")
        learnings_dir = os.path.join(base, ".learnings")
        narratives_dir = os.path.join(base, "narratives")
        archive_dir = os.path.join(base, "archive")
    else:
        # 默认 OpenClaw（首次初始化时创建）
        env = "openclaw"
        base = openclaw_ws
        daily_dir = os.path.join(base, "memory")
        learnings_dir = os.path.join(base, ".learnings")
        narratives_dir = os.path.join(base, "memory", "narratives")
        archive_dir = os.path.join(base, "memory", "archive")

    return {
        'env': env,
        'base': base,
        'memory_md': os.path.join(base, "MEMORY.md"),
        'soul_md': os.path.join(base, "SOUL.md"),
        'tools_md': os.path.join(base, "TOOLS.md"),
        'agents_md': os.path.join(base, "AGENTS.md"),
        'daily_dir': daily_dir,
        'learnings_dir': learnings_dir,
        'learnings_md': os.path.join(learnings_dir, "LEARNINGS.md"),
        'errors_md': os.path.join(learnings_dir, "ERRORS.md"),
        'feature_requests_md': os.path.join(learnings_dir, "FEATURE_REQUESTS.md"),
        'learnings_archive': os.path.join(learnings_dir, "archive"),
        'narratives_dir': narratives_dir,
        'archive_dir': archive_dir,
    }

def get_cron_cmd():
    """返回调度命令。openclaw cron 优先，系统 crontab 降级。"""
    if os.path.isdir(os.path.expanduser("~/.openclaw")):
        return "openclaw cron"
    else:
        return "crontab"  # Claude Code 或其他环境

if __name__ == '__main__':
    paths = get_paths()
    print(f"环境: {paths['env']}")
    print(f"Base: {paths['base']}")
    print(f"MEMORY.md: {paths['memory_md']}")
    print(f"Daily: {paths['daily_dir']}")
    print(f"LEARNINGS: {paths['learnings_md']}")
    print(f"Cron: {get_cron_cmd()}")
