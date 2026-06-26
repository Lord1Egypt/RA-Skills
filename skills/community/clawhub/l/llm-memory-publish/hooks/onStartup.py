#!/usr/bin/env python3
"""
On-Startup Hook - OpenClaw Gateway 启动时自动检查私有包

触发时机：OpenClaw Gateway 服务每次启动时
功能：
1. 检查私有包是否存在
2. 检查是否有更新版本
3. 自动拉取更新（可选）
4. 记录启动日志

安全说明：
- 仅检查本地文件和 Git 仓库状态
- 不自动执行更新（需用户确认）
- 不修改系统配置
"""

import os
import sys
import subprocess
from pathlib import Path
from datetime import datetime


def log(message: str, level: str = "INFO"):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")


def get_skill_dir() -> Path:
    """获取技能目录"""
    skill_dir = os.environ.get("OPENCLAW_SKILL_DIR")
    if skill_dir:
        return Path(skill_dir)
    return Path.home() / ".openclaw" / "workspace" / "skills" / "llm-memory-integration"


def check_privileged_package(privileged_dir: Path) -> dict:
    """
    检查私有包状态
    
    Returns:
        dict: {
            "exists": bool,
            "has_git": bool,
            "current_commit": str,
            "remote_commit": str,
            "needs_update": bool
        }
    """
    result = {
        "exists": False,
        "has_git": False,
        "current_commit": None,
        "remote_commit": None,
        "needs_update": False
    }
    
    if not privileged_dir.exists():
        return result
    
    result["exists"] = True
    
    # 检查是否是 Git 仓库
    git_dir = privileged_dir / ".git"
    if not git_dir.exists():
        return result
    
    result["has_git"] = True
    
    try:
        # 获取当前 commit
        current = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(privileged_dir),
            capture_output=True,
            text=True,
            timeout=10
        )
        if current.returncode == 0:
            result["current_commit"] = current.stdout.strip()[:8]
        
        # 获取远程最新 commit（不拉取）
        subprocess.run(
            ["git", "fetch", "--dry-run"],
            cwd=str(privileged_dir),
            capture_output=True,
            text=True,
            timeout=30
        )
        
        remote = subprocess.run(
            ["git", "rev-parse", "@{u}"],
            cwd=str(privileged_dir),
            capture_output=True,
            text=True,
            timeout=10
        )
        if remote.returncode == 0:
            result["remote_commit"] = remote.stdout.strip()[:8]
        
        # 检查是否需要更新
        if result["current_commit"] and result["remote_commit"]:
            result["needs_update"] = result["current_commit"] != result["remote_commit"]
        
    except Exception as e:
        log(f"检查 Git 状态失败: {e}", "WARN")
    
    return result


def write_startup_log(skill_dir: Path, status: dict):
    """写入启动日志"""
    log_file = skill_dir / ".privileged_status.log"
    
    with open(log_file, "w") as f:
        f.write(f"timestamp: {datetime.now().isoformat()}\n")
        f.write(f"exists: {status['exists']}\n")
        f.write(f"has_git: {status['has_git']}\n")
        f.write(f"current_commit: {status['current_commit'] or 'N/A'}\n")
        f.write(f"remote_commit: {status['remote_commit'] or 'N/A'}\n")
        f.write(f"needs_update: {status['needs_update']}\n")


def main():
    """主函数"""
    log("=" * 60)
    log("LLM Memory Integration - On-Startup Hook")
    log("=" * 60)
    
    skill_dir = get_skill_dir()
    privileged_dir = skill_dir / "src" / "privileged"
    
    log(f"检查私有包状态: {privileged_dir}")
    
    # 检查状态
    status = check_privileged_package(privileged_dir)
    
    if not status["exists"]:
        log("⚠️  私有包未安装")
        log("   运行以下命令安装:")
        log("   cd ~/.openclaw/workspace/skills/llm-memory-integration")
        log("   python3 hooks/postinstall.py")
    elif status["needs_update"]:
        log(f"📦 检测到更新: {status['current_commit']} → {status['remote_commit']}")
        log("   运行以下命令更新:")
        log("   cd ~/.openclaw/workspace/skills/llm-memory-integration/src/privileged")
        log("   git pull")
    else:
        log(f"✅ 私有包已是最新版本 ({status['current_commit']})")
    
    # 写入日志
    write_startup_log(skill_dir, status)
    
    log("=" * 60)
    log("On-Startup Hook 完成")
    log("=" * 60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
