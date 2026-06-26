#!/usr/bin/env python3
"""
system-check.py — 项目管理系统完整性检查

基于 Git 检测 D:/projects 仓库下的文件是否被意外修改。
仓库包含 system/（规则文件）及未来可能添加的其他内容。
项目数据存放在 D:/projects-data（独立目录，不在仓库内）。

用法：
    python system-check.py              # 检查是否有未提交的变更
    python system-check.py --commit "说明"  # 合法修改后提交（记录变更）
    python system-check.py --restore    # 恢复所有未提交的变更
    python system-check.py --diff       # 查看具体改了什么

原理：
    每次合法修改后，用 --commit 提交。
    之后任何未提交的变更都视为异常（被意外修改）。
    --restore 可以一键恢复到最后一次合法提交的状态。
"""

import subprocess
import sys
import os

# Windows 终端编码兼容
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# 仓库根目录（Git 仓库在 D:\projects）
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_git(*args):
    result = subprocess.run(
        ["git"] + list(args),
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    return result

def check():
    """检查是否有未提交的变更"""
    result = run_git("status", "--porcelain")
    if result.returncode != 0:
        print("❌ Git 错误：", result.stderr)
        return 1

    changes = result.stdout.strip()
    if not changes:
        print("✅ 系统文件完整，无异常变更。")
        return 0

    print("⚠️  检测到未提交的变更：")
    print()
    for line in changes.split("\n"):
        status = line[:2].strip()
        filepath = line[3:]
        if status == "M":
            print(f"  📝 已修改：{filepath}")
        elif status == "D":
            print(f"  🗑️  已删除：{filepath}")
        elif status == "??" or status == "A":
            print(f"  ➕ 新增文件：{filepath}")
        else:
            print(f"  ❓ {status}：{filepath}")

    print()
    print("如果是合法修改，运行：python system-check.py --commit \"修改说明\"")
    print("如果是异常修改，运行：python system-check.py --restore")
    print("查看具体改动，运行：python system-check.py --diff")
    return 1

def commit(message):
    """提交合法修改"""
    run_git("add", "-A")
    result = run_git("commit", "-m", message)
    if result.returncode == 0:
        print(f"✅ 已提交：{message}")
    else:
        print("❌ 提交失败：", result.stderr or result.stdout)
    return result.returncode

def restore():
    """恢复所有未提交的变更"""
    # 恢复已跟踪文件的修改
    run_git("checkout", "--", ".")
    # 删除未跟踪的新文件
    run_git("clean", "-fd")
    print("✅ 已恢复到最后一次合法提交的状态。")
    return 0

def diff():
    """显示具体改动"""
    result = run_git("diff")
    if result.stdout:
        print(result.stdout)
    else:
        print("无已跟踪文件的改动。")

    # 检查未跟踪文件
    untracked = run_git("ls-files", "--others", "--exclude-standard")
    if untracked.stdout.strip():
        print("\n未跟踪的新文件：")
        print(untracked.stdout)
    return 0

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        sys.exit(check())
    elif args[0] == "--commit":
        if len(args) < 2:
            print("用法：python system-check.py --commit \"修改说明\"")
            sys.exit(1)
        sys.exit(commit(args[1]))
    elif args[0] == "--restore":
        sys.exit(restore())
    elif args[0] == "--diff":
        sys.exit(diff())
    else:
        print("未知参数。用法：")
        print("  python system-check.py              # 检查")
        print('  python system-check.py --commit "说明"  # 提交')
        print("  python system-check.py --restore     # 恢复")
        print("  python system-check.py --diff        # 查看改动")
        sys.exit(1)
