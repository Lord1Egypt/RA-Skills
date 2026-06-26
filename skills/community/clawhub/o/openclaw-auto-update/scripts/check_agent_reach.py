#!/usr/bin/env python3
"""
Agent-Reach 可用性检测工具
用于检查用户是否已安装并可正常使用 agent-reach
"""

import subprocess
import sys

def check_agent_reach():
    """检测 agent-reach 是否可用"""
    try:
        # 检查是否安装
        result = subprocess.run(
            ["agent-reach", "--version"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.returncode == 0:
            return True, result.stdout.strip()
        return False, "未安装或版本检测失败"
    except FileNotFoundError:
        return False, "agent-reach 未安装"
    except Exception as e:
        return False, f"检测失败：{e}"

def test_github_access():
    """测试 GitHub 访问能力"""
    try:
        result = subprocess.run(
            ["agent-reach", "read", "https://github.com/openclaw/openclaw", "--timeout", "10"],
            capture_output=True,
            text=True,
            timeout=15
        )
        if result.returncode == 0 and len(result.stdout) > 100:
            return True, "GitHub 访问正常"
        return False, "GitHub 访问失败或超时"
    except Exception as e:
        return False, f"测试失败：{e}"

def print_install_guide():
    """打印安装指南"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║  agent-reach 安装指南                                      ║
╠═══════════════════════════════════════════════════════════╣
║                                                           ║
║  方法 1：pipx 安装（推荐）                                 ║
║  ───────────────────────                                  ║
║  pipx install https://github.com/Panniantong/            ║
║                   agent-reach/archive/main.zip           ║
║  agent-reach install --env=auto                          ║
║                                                           ║
║  方法 2：检查其他 GitHub 访问方式                           ║
║  ──────────────────────────                               ║
║  如 gh CLI、curl 等（不推荐，可能被拦截）                  ║
║                                                           ║
║  安装后验证：                                             ║
║  ────────────                                             ║
║  agent-reach --version                                   ║
║  agent-reach read "https://github.com"                   ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
""")

def main():
    print("🔍 检测 agent-reach 可用性...\n")
    
    # 检查是否安装
    installed, version_msg = check_agent_reach()
    
    if installed:
        print(f"✅ agent-reach 已安装：{version_msg}")
        
        # 测试 GitHub 访问
        print("\n🌐 测试 GitHub 访问能力...")
        access_ok, access_msg = test_github_access()
        
        if access_ok:
            print(f"✅ {access_msg}")
            print("\n✅ 可以正常使用 openclaw-update skill！")
            return 0
        else:
            print(f"⚠️ {access_msg}")
            print("\n⚠️ agent-reach 已安装但无法访问 GitHub")
            print_install_guide()
            return 1
    else:
        print(f"❌ {version_msg}")
        print("\n❌ 需要先安装 agent-reach 才能使用 openclaw-update skill")
        print_install_guide()
        return 1

if __name__ == "__main__":
    sys.exit(main())
