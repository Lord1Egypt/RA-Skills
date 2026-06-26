#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main entry point for openclaw-coe skill
"""

import sys
from cot_tracker import CoETracker

def main():
    """Main function"""
    # Check if we're being called to enable/disable
    args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    if len(args) == 0:
        print("OpenClaw CoE (Chain of Execution) Skill")
        print("")
        print("Usage:")
        print("  python main.py enable  - Enable CoE for current session")
        print("  python main.py disable - Disable CoE for current session")
        print("  python main.py status  - Show current status")
        return

    cmd = args[0].lower()
    if cmd == "enable":
        print("✅ OpenClaw CoE 已启用，接下来的任务会分步输出执行过程")
        # Note: Session-level enable is handled by the agent
        return
    elif cmd == "disable":
        print("✅ OpenClaw CoE 已禁用")
        return
    elif cmd == "status":
        print("ℹ️  OpenClaw CoE 已安装，可以用 'enable' 开启")
        return
    else:
        print(f"❓ Unknown command: {cmd}")
        return

if __name__ == "__main__":
    main()
