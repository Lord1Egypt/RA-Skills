#!/usr/bin/env python3
"""
Skill Marketplace - Install Skills
从 ClawHub 安装技能

Usage:
  python3 install.py auto-backup
  python3 install.py model-switch --force
"""

import subprocess
import sys
import argparse
from pathlib import Path

class Colors:
    BLUE = '\033[0;34m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    CYAN = '\033[0;36m'
    RED = '\033[0;31m'
    NC = '\033[0m'
    BOLD = '\033[1m'

def log_info(msg): print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")
def log_success(msg): print(f"{Colors.GREEN}[✓]{Colors.NC} {msg}")
def log_warning(msg): print(f"{Colors.YELLOW}[⚠]{Colors.NC} {msg}")
def log_error(msg): print(f"{Colors.RED}[✗]{Colors.NC} {msg}")

def check_clawhub_installed():
    """检查 ClawHub CLI 是否已安装"""
    try:
        result = subprocess.run(['npx', 'clawhub', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except Exception:
        return False

def install_skill(skill_name, force=False):
    """从 ClawHub 安装技能"""
    log_info(f"正在安装技能：{skill_name}")
    
    # 检查是否已安装
    skills_dir = Path.home() / ".openclaw" / "workspace" / "skills"
    skill_path = skills_dir / skill_name
    
    if skill_path.exists() and not force:
        log_warning(f"技能已存在：{skill_path}")
        log_info("使用 --force 参数强制重新安装")
        return False
    
    # 使用 ClawHub CLI 安装
    try:
        log_info("调用 ClawHub CLI 安装...")
        result = subprocess.run(
            ['npx', 'clawhub', 'install', skill_name],
            cwd=str(skills_dir),
            timeout=120
        )
        
        if result.returncode == 0:
            log_success(f"技能安装成功：{skill_name}")
            return True
        else:
            log_error(f"安装失败，退出码：{result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        log_error("安装超时（超过 2 分钟）")
        return False
    except FileNotFoundError:
        log_error("未找到 npx 命令，请确保已安装 Node.js")
        return False
    except Exception as e:
        log_error(f"安装失败：{e}")
        return False

def main():
    parser = argparse.ArgumentParser(description='从 ClawHub 安装技能')
    parser.add_argument('skill', type=str, help='技能名称')
    parser.add_argument('--force', action='store_true', help='强制重新安装')
    parser.add_argument('--list', action='store_true', help='列出已安装技能')
    
    args = parser.parse_args()
    
    if args.list:
        # 列出已安装技能
        skills_dir = Path.home() / ".openclaw" / "workspace" / "skills"
        if not skills_dir.exists():
            log_warning("技能目录不存在")
            return 0
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}已安装的技能：{Colors.NC}\n")
        installed = []
        for item in skills_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                skill_md = item / "SKILL.md"
                if skill_md.exists():
                    installed.append(item.name)
        
        if installed:
            for skill in sorted(installed):
                print(f"  ✅ {skill}")
            print(f"\n共 {len(installed)} 个技能")
        else:
            print("  暂无技能")
        print()
        return 0
    
    # 检查 ClawHub CLI
    if not check_clawhub_installed():
        log_error("未找到 ClawHub CLI")
        print(f"\n{Colors.YELLOW}请先安装 ClawHub CLI：{Colors.NC}")
        print(f"  npm install -g @openclaw/clawhub")
        print(f"\n或使用 npx 运行：")
        print(f"  npx clawhub install {args.skill}")
        print()
        return 1
    
    # 安装技能
    success = install_skill(args.skill, args.force)
    
    if success:
        print(f"\n{Colors.GREEN}✓ 安装完成！{Colors.NC}")
        print(f"\n{Colors.CYAN}使用技能：{Colors.NC}")
        print(f"  cd ~/.openclaw/workspace/skills/{args.skill}")
        print(f"  ls -la")
        print()
        return 0
    else:
        print(f"\n{Colors.RED}✗ 安装失败{Colors.NC}")
        print(f"\n{Colors.YELLOW}可能的原因：{Colors.NC}")
        print(f"  1. 技能名称错误")
        print(f"  2. 技能不存在于 ClawHub")
        print(f"  3. 网络连接问题")
        print(f"  4. 权限不足")
        print(f"\n{Colors.CYAN}建议：{Colors.NC}")
        print(f"  1. 检查技能名称：python3 skill-marketplace/scripts/search.py {args.skill} --from-clawhub")
        print(f"  2. 手动安装：npx clawhub install {args.skill}")
        print()
        return 1

if __name__ == "__main__":
    sys.exit(main())
