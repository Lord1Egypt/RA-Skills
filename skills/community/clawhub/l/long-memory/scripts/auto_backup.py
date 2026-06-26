#!/usr/bin/env python3
"""自动备份：Git commit + push"""

import argparse
import subprocess
from datetime import datetime
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.filelock import file_lock

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
LOCK_FILE = DEFAULT_MEMORY_DIR / ".backup.lock"


def run_git(memory_dir: Path, args_list: list[str], check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git"] + args_list,
        cwd=memory_dir,
        capture_output=True, text=True, timeout=30, check=check
    )


def ensure_git_repo(memory_dir: Path) -> bool:
    """确保 memory 目录是一个 git repo"""
    result = run_git(memory_dir, ["rev-parse", "--git-dir"])
    if result.returncode != 0:
        run_git(memory_dir, ["init"])
        run_git(memory_dir, ["config", "user.email", "long-memory@openclaw"])
        run_git(memory_dir, ["config", "user.name", "Long Memory Bot"])
        return True
    return False


def backup(memory_dir: Path, remote: str | None = None, message: str | None = None):
    """执行自动备份"""
    if not memory_dir.exists():
        print("⚠️ 记忆目录不存在")
        return False

    with file_lock(LOCK_FILE, timeout=10):
        ensure_git_repo(memory_dir)

        # 检查是否有变更
        result = run_git(memory_dir, ["status", "--porcelain"])
        if not result.stdout.strip():
            print("✅ 没有待提交的变更")
            return True

        # 添加所有文件
        run_git(memory_dir, ["add", "-A"])

        # 提交
        msg = message or f"auto-backup: {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        result = run_git(memory_dir, ["commit", "-m", msg])
        if result.returncode != 0:
            # 可能是 nothing to commit
            if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
                print("✅ 没有待提交的变更")
                return True
            print(f"⚠️ 提交失败: {result.stderr}")
            return False

        commit_short = result.stdout.strip().split("\n")[0] if result.stdout else "unknown"
        print(f"✅ 已提交: {commit_short}")

        # 推送
        if remote:
            result = run_git(memory_dir, ["remote", "get-url", "origin"])
            if result.returncode != 0:
                run_git(memory_dir, ["remote", "add", "origin", remote])
            
            result = run_git(memory_dir, ["push", "-u", "origin", "main"])
            if result.returncode != 0:
                # 尝试当前分支
                branch_result = run_git(memory_dir, ["branch", "--show-current"])
                branch = branch_result.stdout.strip() or "main"
                run_git(memory_dir, ["push", "-u", "origin", branch])
            print(f"✅ 已推送到远程")

        return True


def get_backup_status(memory_dir: Path) -> dict:
    """获取备份状态"""
    status = {"is_git_repo": False, "is_clean": True, "remote": None, "last_commit": None}

    result = run_git(memory_dir, ["rev-parse", "--git-dir"])
    if result.returncode == 0:
        status["is_git_repo"] = True
        
        result = run_git(memory_dir, ["status", "--porcelain"])
        status["is_clean"] = not result.stdout.strip()
        
        result = run_git(memory_dir, ["remote", "get-url", "origin"])
        if result.returncode == 0:
            status["remote"] = result.stdout.strip()
        
        result = run_git(memory_dir, ["log", "-1", "--format=%ai %s"])
        if result.returncode == 0:
            status["last_commit"] = result.stdout.strip()

    return status


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="自动备份")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--remote", "-r", default=None, help="Git 远程仓库 URL")
    p.add_argument("--message", "-m", default=None, help="提交消息")
    p.add_argument("--status", action="store_true", help="查看备份状态")
    p.add_argument("--setup", action="store_true", help="初始化 Git 仓库")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)

    if args.status:
        status = get_backup_status(md)
        print("📦 备份状态")
        print(f"  Git 仓库: {'✅' if status['is_git_repo'] else '❌'}")
        print(f"  工作区: {'干净' if status['is_clean'] else '有未提交变更'}")
        print(f"  远程仓库: {status['remote'] or '未配置'}")
        print(f"  最近提交: {status['last_commit'] or '无'}")
    elif args.setup:
        ensure_git_repo(md)
        if args.remote:
            run_git(md, ["remote", "add", "origin", args.remote])
        print("✅ Git 仓库已初始化")
    else:
        backup(md, args.remote, args.message)
