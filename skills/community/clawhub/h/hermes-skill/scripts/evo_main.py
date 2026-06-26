#!/usr/bin/env python3
"""
自进化系统统一入口
Usage: python3 evo_main.py <command>

Commands:
  nudge [type]          - 检查/触发 nudge
  remember <text>       - 添加记忆
  forget <text>         - 删除记忆
  search <query>        - 搜索记忆
  stats                 - 显示记忆统计
  skills                - 列出自动创建的 skills
  eval <skill,rating>   - 评估 skill
  improve <skill,notes>  - 改进 skill
  upstream <cmd>         - 上游追踪 (check|status|diff|list|fuse)
  check                  - 运行完整自检
"""

import sys
import subprocess
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
UPSTREAM_SCRIPT = SCRIPT_DIR / "upstream_tracker.py"

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]
    args = sys.argv[2:]

    if cmd == "upstream":
        sub = args[0] if args else "status"
        result = subprocess.run(
            ["python3", str(UPSTREAM_SCRIPT), sub] + args[1:],
            capture_output=True, text=True, timeout=120
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return

    if cmd not in ["nudge", "remember", "forget", "recall", "stats", "skills", "eval", "improve", "check"]:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        return

    if cmd in ["nudge"]:
        if args:
            result = subprocess.run(
                ["python3", str(SCRIPT_DIR / "nudge_system.py"), "--trigger", args[0]],
                capture_output=True, text=True
            )
        else:
            result = subprocess.run(
                ["python3", str(SCRIPT_DIR / "nudge_system.py"), "--check"],
                capture_output=True, text=True
            )
    elif cmd in ["remember", "forget", "recall"]:
        result = subprocess.run(
            ["python3", str(SCRIPT_DIR / "memory_tool.py"), cmd] + args,
            capture_output=True, text=True
        )
    elif cmd == "stats":
        result = subprocess.run(
            ["python3", str(SCRIPT_DIR / "memory_tool.py"), "stats"],
            capture_output=True, text=True
        )
    elif cmd == "skills":
        result = subprocess.run(
            ["python3", str(SCRIPT_DIR / "auto_skill_creator.py"), "--list"],
            capture_output=True, text=True
        )
    elif cmd in ["eval", "improve"]:
        result = subprocess.run(
            ["python3", str(SCRIPT_DIR / "skill_evaluator.py")] + [f"--{cmd}", args[0]],
            capture_output=True, text=True
        )
    elif cmd == "check":
        result = subprocess.run(
            ["bash", str(SCRIPT_DIR / "self_check_cron.sh")],
            capture_output=True, text=True
        )

    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)

if __name__ == "__main__":
    main()