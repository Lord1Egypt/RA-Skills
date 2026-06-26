#!/usr/bin/env python3
"""CLI 入口：统一命令行工具"""

import argparse
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent


def run_script(name: str, args: list[str]):
    script = SCRIPTS_DIR / f"{name}.py"
    if not script.exists():
        print(f"❌ 未知命令: {name}")
        print(f"   可用命令: archive, capture, summary, distill, stats, "
              f"timeline, search, contradictions, quality, integrity, "
              f"backup, graph, forgetting, tags, export, clean, index")
        sys.exit(1)
    
    import subprocess
    result = subprocess.run([sys.executable, str(script)] + args)
    sys.exit(result.returncode)


def main():
    p = argparse.ArgumentParser(
        prog="long-memory",
        description="🧠 全量对话记忆系统 — 企业级 CLI",
    )
    p.add_argument("command", help="子命令")
    p.add_argument("args", nargs="*", help="子命令参数")

    # 快捷别名
    aliases = {
        "archive": "archive_conversation",
        "capture": "capture_session",
        "summary": "generate_summary",
        "distill": "distill_week",
        "stats": "memory_stats",
        "timeline": "topic_timeline",
        "search": "search_memory",
        "contradictions": "detect_contradictions",
        "quality": "quality_check",
        "integrity": "integrity_check",
        "backup": "auto_backup",
        "graph": "memory_graph",
        "forgetting": "forgetting_curve",
        "tags": "tag_optimizer",
        "export": "export_memory",
        "clean": "clean_old",
        "index": "index_manager",
        "emotion": "emotion_analyzer",
        "persons": "person_graph",
        "recommend": "smart_recommend",
        "health": "health_dashboard",
        "privacy": "privacy",
        "import": "import_memory",
        "scheduler": "scheduler",
        "template": "memory_templates",
        "users": "user_manager",
        "config": "config_manager",
        "changelog": "changelog",
        "benchmark": "benchmark",
        "report": "html_report",
        "api": "api_server",
        "tfidf": "tfidf_search",
        "semantic": "semantic_search",
        "sqlite": "sqlite_engine",
        "embedding": "embedding_search",
        "log": "operation_log",
        "self": "self_memory",
    }

    args = p.parse_args()
    cmd = aliases.get(args.command, args.command)
    run_script(cmd, args.args)


if __name__ == "__main__":
    main()
