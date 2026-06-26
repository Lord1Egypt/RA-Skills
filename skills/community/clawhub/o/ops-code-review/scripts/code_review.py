#!/usr/bin/env python3
"""
代码审计主调度脚本
用法:
  python3 code_review.py incremental <repo_name>    # 增量扫描（post-commit hook 调用）
  python3 code_review.py full <repo_name>           # 全量扫描（定时任务调用）
  python3 code_review.py fullall                     # 全量扫描所有仓库
  python3 code_review.py sync                        # 同步所有仓库
  python3 code_review.py setup-hooks                 # 生成 SVN post-commit hook 脚本
  python3 code_review.py check-deps                 # 检查工具依赖
  python3 code_review.py install-deps               # 安装缺失工具
"""
import sys
import os
import json
import subprocess
from datetime import datetime

# 添加脚本目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 依赖检查
from check_dependencies import ensure_tools, check_all

# 延迟导入（确保环境变量已加载）
from svn_manager import get_repos, checkout_or_update, get_changed_files_local, update_scan_state, get_feishu_chat_id
from analyzer_runner import scan_repo
from report_generator import build_report


def send_feishu_message(message: str, chat_id: str = None):
    """发送飞书消息"""
    if chat_id is None:
        chat_id = get_feishu_chat_id()

    if not chat_id:
        print("[WARN] No feishu chat_id configured. Message not sent.")
        print(message)
        return

    # 保存消息到文件，由 OpenClaw 读取推送（权限 600 防止其他用户读取）
    msg_file = "/tmp/code_review_pending_msg.json"
    with open(msg_file, "w") as f:
        json.dump({"chat_id": chat_id, "message": message, "time": datetime.now().isoformat()}, f)
    os.chmod(msg_file, 0o600)
    print(f"[OK] Message saved to {msg_file}")


def run_incremental_scan(repo_name: str):
    """增量扫描：post-commit 触发"""
    print(f"[INFO] Starting incremental scan for {repo_name}")

    # 1. 检查工具
    print(f"[STEP 0/5] Checking dependencies...")
    if not ensure_tools():
        print(f"[WARN] Some tools missing. Run 'code_review.py install-deps' first.")

    # 2. 更新仓库
    print(f"[STEP 1/5] Syncing repo {repo_name}...")
    ok = checkout_or_update(repo_name)
    if not ok:
        print(f"[ERROR] Failed to sync repo {repo_name}")
        return

    # 3. 获取变更文件
    print(f"[STEP 2/5] Getting changed files...")
    changed_files = get_changed_files_local(repo_name)

    if not changed_files:
        print(f"[OK] No changes detected for {repo_name}")
        return

    print(f"[INFO] Found {len(changed_files)} changed files")

    # 4. 过滤有效文件
    valid_extensions = (".py", ".ts", ".tsx", ".js", ".jsx", ".php", ".java")
    valid_files = [f for f in changed_files if any(f.endswith(ext) for ext in valid_extensions)]

    if not valid_files:
        print(f"[OK] No scannable files changed")
        return

    print(f"[INFO] {len(valid_files)} files to scan")

    # 5. 运行分析
    print(f"[STEP 3/5] Running analysis...")
    repos = get_repos()
    repo_info = repos.get(repo_name, {})
    base_path = repo_info.get("local", f"/tmp/svn_repos/{repo_name}")
    lang = repo_info.get("lang", "python")

    if lang == "mixed":
        all_results = {}
        php_files = [f for f in valid_files if f.endswith(".php")]
        react_files = [f for f in valid_files if any(f.endswith(ext) for ext in [".ts", ".tsx", ".js", ".jsx"])]

        if php_files:
            all_results["php"] = scan_repo("gm_php", php_files, base_path)
        if react_files:
            all_results["react"] = scan_repo("gm_react", react_files, base_path)
    else:
        all_results = scan_repo(repo_name, valid_files, base_path)

    # 6. 生成报告
    print(f"[STEP 4/5] Generating report...")
    report = build_report(repo_name, lang, all_results, "incremental", valid_files)

    # 7. 推送飞书
    print(f"[STEP 5/5] Sending to Feishu...")
    send_feishu_message(report["text"])

    # 保存报告（权限 600 防止其他用户读取）
    report_file = f"/tmp/code_review_{repo_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    os.chmod(report_file, 0o600)
    print(f"[OK] Report saved to {report_file}")

    # 更新状态
    update_scan_state(repo_name)

    return report


def run_full_scan(repo_name: str):
    """全量扫描：定时任务调用"""
    print(f"[INFO] Starting full scan for {repo_name}")

    # 0. 检查工具
    print(f"[STEP 0/4] Checking dependencies...")
    if not ensure_tools():
        print(f"[WARN] Some tools missing. Run 'code_review.py install-deps' first.")

    # 1. 更新仓库
    print(f"[STEP 1/4] Syncing repo {repo_name}...")
    ok = checkout_or_update(repo_name)
    if not ok:
        print(f"[ERROR] Failed to sync repo {repo_name}")
        return

    # 2. 获取全量文件
    print(f"[STEP 2/4] Getting all files...")
    repos = get_repos()
    repo_info = repos.get(repo_name, {})
    base_path = repo_info.get("local", f"/tmp/svn_repos/{repo_name}")
    lang = repo_info.get("lang", "python")

    valid_extensions = (".py", ".ts", ".tsx", ".js", ".jsx", ".php", ".java")
    all_files = []
    skip_dirs = ["__pycache__", ".git", "node_modules", ".svn", "migrations", "vendor", "target", "dist", "build", ".next", "venv", ".venv", "tests"]
    for root, dirs, files in os.walk(base_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for file in files:
            if any(file.endswith(ext) for ext in valid_extensions):
                all_files.append(os.path.join(root, file))

    if not all_files:
        print(f"[WARN] No files found in {repo_name}")
        return

    print(f"[INFO] Found {len(all_files)} files to scan")

    # 3. 运行分析
    print(f"[STEP 3/4] Running analysis...")
    if lang == "mixed":
        all_results = {}
        php_files = [f for f in all_files if f.endswith(".php")]
        react_files = [f for f in all_files if any(f.endswith(ext) for ext in [".ts", ".tsx", ".js", ".jsx"])]

        if php_files:
            all_results["php"] = scan_repo("gm_php", php_files, base_path, lang="php")
        if react_files:
            all_results["react"] = scan_repo("gm_react", react_files, base_path, lang="react")
    else:
        all_results = scan_repo(repo_name, all_files, base_path)

    # 4. 生成报告
    print(f"[STEP 4/4] Generating report...")
    report = build_report(repo_name, lang, all_results, "full", all_files)
    send_feishu_message(report["text"])

    # 保存报告（权限 600 防止其他用户读取）
    report_file = f"/tmp/code_review_full_{repo_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    os.chmod(report_file, 0o600)
    print(f"[OK] Report saved to {report_file}")

    return report


def generate_hook_script() -> str:
    """生成 SVN post-commit hook 脚本"""
    hook_script = """#!/bin/bash
# SVN Post-Commit Hook - 代码审计触发脚本
# 将此脚本放到 SVN 仓库的 hooks 目录，重命名为 post-commit
# 确保有执行权限: chmod +x post-commit

REPOS="$${1}"
REV="$${2}"

# 仓库名称映射（根据实际路径修改）
case "$${REPOS}" in
    */ops_api*) REPO_NAME="ops_api" ;;
    */ops_web*) REPO_NAME="ops_web" ;;
    */gm*) REPO_NAME="gm" ;;
    *) echo "Unknown repo: $${REPOS}" && exit 0 ;;
esac

# 调用代码审计（后台执行，避免阻塞提交）
python3 /path/to/code-review/scripts/code_review.py incremental "$${REPO_NAME}" >> /var/log/svn_code_review.log 2>&1 &

exit 0
"""
    return hook_script


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    action = sys.argv[1]

    if action == "incremental" and len(sys.argv) >= 3:
        run_incremental_scan(sys.argv[2])
    elif action == "full" and len(sys.argv) >= 3:
        run_full_scan(sys.argv[2])
    elif action == "fullall":
        repos = get_repos()
        for repo_name in repos:
            repo_info = repos[repo_name]
            if repo_info.get("type") in ("full", "both"):
                run_full_scan(repo_name)
    elif action == "sync":
        from svn_manager import sync_all_repos
        sync_all_repos()
    elif action == "setup-hooks":
        print(generate_hook_script())
    elif action == "check-deps":
        missing = check_all()
        if missing:
            for tool, info in missing.items():
                print(f"MISSING: {tool} - {info['help']}")
                print(f"  Install: {info['install']}")
            sys.exit(1)
        print("All tools OK")
        sys.exit(0)
    elif action == "install-deps":
        from check_dependencies import install_all
        results = install_all()
        failed = [t for t, ok in results.items() if not ok]
        if failed:
            print(f"Failed: {', '.join(failed)}")
            sys.exit(1)
        print("All installed")
    else:
        print(f"Unknown action: {action}", file=sys.stderr)
        print(__doc__)
        sys.exit(1)
