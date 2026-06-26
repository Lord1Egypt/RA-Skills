#!/usr/bin/env python3
"""
OpenClaw 配置管理入口脚本
统一入口，支持迪逗和 Hermes 调用
"""

import sys
import subprocess
from pathlib import Path

# 支持两个位置：workspace (开发) 和 skills (已安装)
WORKSPACE_SKILL = Path.home() / ".openclaw" / "workspace" / "openclaw-config-expert"
INSTALLED_SKILL = Path.home() / ".openclaw" / "skills" / "openclaw-config-expert"

SKILL_DIR = INSTALLED_SKILL if INSTALLED_SKILL.exists() else WORKSPACE_SKILL
SCRIPTS_DIR = SKILL_DIR / "scripts"


def print_help():
    """打印帮助信息"""
    help_text = """
╔═══════════════════════════════════════════════════════════╗
║  OpenClaw 配置专家 Skill                                  ║
║  版本：1.1.0                                              ║
╠═══════════════════════════════════════════════════════════╣
║  使用方式：                                               ║
║                                                           ║
║  1. 验证配置                                              ║
║     python3 config.py validate                            ║
║                                                           ║
║  2. 修复配置                                              ║
║     python3 config.py fix                                 ║
║                                                           ║
║  3. 修改配置                                              ║
║     python3 config.py modify --key <key> --value <value>  ║
║     python3 config.py modify --updates '<json>'           ║
║                                                           ║
║  4. 优化配置                                              ║
║     python3 config.py optimize --target cost-saving       ║
║                                                           ║
║  5. 紧急恢复 (Hermes)                                     ║
║     python3 config.py recover                             ║
║                                                           ║
║  6. 查看帮助                                              ║
║     python3 config.py help                                ║
╚═══════════════════════════════════════════════════════════╝
"""
    print(help_text)


def run_script(script_name: str, args: list) -> int:
    """运行脚本"""
    script_path = SCRIPTS_DIR / script_name
    
    if not script_path.exists():
        print(f"❌ 脚本不存在：{script_path}")
        return 1
    
    cmd = [sys.executable, str(script_path)] + args
    result = subprocess.run(cmd)
    return result.returncode


def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)
    
    action = sys.argv[1]
    args = sys.argv[2:]
    
    if action == "help":
        print_help()
        sys.exit(0)
    
    elif action == "validate":
        sys.exit(run_script("config_validator.py", ["validate"] + args))
    
    elif action == "fix":
        sys.exit(run_script("config_validator.py", ["fix"] + args))
    
    elif action == "modify":
        sys.exit(run_script("config_validator.py", ["modify"] + args))
    
    elif action == "optimize":
        sys.exit(run_script("agent_optimizer.py", args))
    
    elif action == "recover":
        sys.exit(run_script("emergency_recovery.py", ["recover"] + args))
    
    elif action == "rollback":
        sys.exit(run_script("emergency_recovery.py", ["rollback"] + args))
    
    elif action == "restart":
        sys.exit(run_script("emergency_recovery.py", ["restart"] + args))
    
    elif action == "status":
        sys.exit(run_script("emergency_recovery.py", ["status"] + args))
    
    else:
        print(f"❌ 未知操作：{action}")
        print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
