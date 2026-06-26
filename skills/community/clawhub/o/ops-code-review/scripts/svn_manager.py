#!/usr/bin/env python3
"""
SVN 仓库管理：检出、更新、获取变更文件
敏感配置通过环境变量或 config.json 注入，不随 skill 上传
"""
import subprocess
import sys
import os
import re
import json
import os
from typing import List, Dict, Optional

# === 敏感配置：从环境变量读取 ===
SVN_USER = os.environ.get("CODE_REVIEW_SVN_USER", "")
SVN_PASS = os.environ.get("CODE_REVIEW_SVN_PASS", "")

# === 仓库配置：从环境变量或 config.json 读取 ===
# config.json 不随 skill 上传，用户需要自行创建
_config_cache = None


def _load_config() -> dict:
    """加载配置文件"""
    global _config_cache
    if _config_cache is not None:
        return _config_cache

    config_paths = [
        os.environ.get("CODE_REVIEW_CONFIG", ""),
        "/etc/code-review/config.json",
        os.path.expanduser("~/.config/code-review/config.json"),
        "/tmp/code_review_config.json",
    ]

    for path in config_paths:
        if path and os.path.exists(path):
            with open(path) as f:
                _config_cache = json.load(f)
                return _config_cache

    # 没有配置文件时的默认值（用户必须配置）
    _config_cache = {}
    return _config_cache


def get_repo_url(repo_name: str) -> str:
    """获取仓库 URL"""
    config = _load_config()
    repos = config.get("repos", {})
    if repo_name in repos:
        return repos[repo_name].get("url", "")
    return ""


def get_feishu_chat_id() -> str:
    """获取飞书群 ID，优先从环境变量读取"""
    return os.environ.get("CODE_REVIEW_FEISHU_CHAT_ID", "")


# === 仓库配置（通用模板，上传时脱敏）===
# URL 和认证信息通过 config.json 配置
REPOS_TEMPLATE = {
    # 模板占位符，实际配置在 config.json 中
    # 格式：repo_name: { "lang": "python|react|mixed", "type": "incremental|full|both" }
}


def get_repos() -> dict:
    """动态获取仓库配置"""
    config = _load_config()
    return config.get("repos", {})


def svn_auth_cmd(cmd: List[str]) -> List[str]:
    """给 SVN 命令加上账密（避免命令行暴露密码）"""
    if SVN_USER:
        cmd = cmd + ["--username", SVN_USER]
        if SVN_PASS:
            cmd = cmd + ["--password", SVN_PASS, "--no-auth-cache"]
        else:
            cmd = cmd + ["--no-auth-cache"]
    return cmd


def run_cmd(cmd: List[str], cwd: Optional[str] = None) -> tuple:
    """执行命令，返回 (returncode, stdout, stderr)

    若提供了 SVN_PASS，改用 stdin 管道传递密码，避免在 cmdline 中暴露。
    """
    env = None
    stdin_data = None
    if SVN_USER and SVN_PASS:
        # SVN 1.10+ 支持 --password-from-stdin
        cmd = cmd + ["--password-from-stdin"]
        stdin_data = SVN_PASS.encode()
        env = {**os.environ}

    result = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        input=stdin_data,
        env=env,
    )
    return result.returncode, result.stdout, result.stderr


def checkout_or_update(repo_name: str) -> bool:
    """检出或更新仓库"""
    repos = get_repos()
    if repo_name not in repos:
        print(f"[ERROR] Repo {repo_name} not configured. Add it to config.json", file=sys.stderr)
        return False

    repo = repos[repo_name]
    url = repo.get("url", "")
    local_path = repo.get("local", f"/tmp/svn_repos/{repo_name}")

    if not url:
        print(f"[ERROR] No URL configured for {repo_name}", file=sys.stderr)
        return False

    os.makedirs(os.path.dirname(local_path.rstrip("/")), exist_ok=True)

    if os.path.exists(os.path.join(local_path, ".svn")):
        cmd = svn_auth_cmd(["svn", "update", "--accept", "theirs-full"])
        rc, out, err = run_cmd(cmd, cwd=local_path)
    else:
        cmd = svn_auth_cmd(["svn", "checkout", url, local_path])
        rc, out, err = run_cmd(cmd)

    if rc != 0:
        print(f"[ERROR] SVN {repo_name} failed: {err}", file=sys.stderr)
        return False
    print(f"[OK] SVN {repo_name} updated")
    return True


def get_changed_files_local(repo_name: str) -> List[str]:
    """本地获取最新变更文件（用于增量扫描）"""
    repos = get_repos()
    if repo_name not in repos:
        return []

    repo = repos[repo_name]
    local_path = repo.get("local", f"/tmp/svn_repos/{repo_name}")

    if not os.path.exists(os.path.join(local_path, ".svn")):
        print(f"[WARN] {repo_name} not checked out yet", file=sys.stderr)
        return []

    # 获取当前版本
    cmd = svn_auth_cmd(["svn", "info", "--show-item", "revision"])
    rc, out, err = run_cmd(cmd, cwd=local_path)
    if rc != 0:
        return []
    current_rev = out.strip()

    # 与上一个已扫版本比较
    state_file = f"/tmp/svn_repos/.scan_state_{repo_name}.json"
    last_rev = "1"
    if os.path.exists(state_file):
        with open(state_file) as f:
            last_rev = json.load(f).get("last_rev", "1")

    if last_rev == current_rev:
        return []

    cmd = svn_auth_cmd([
        "svn", "diff",
        "--revision", f"{last_rev}:{current_rev}",
        local_path,
    ])
    rc, out, err = run_cmd(cmd)
    if rc != 0:
        return []

    files = []
    for line in out.splitlines():
        if line.startswith(("A ", "M ", "MM ")):
            f = line[4:].strip()
            if f:
                files.append(os.path.join(local_path, f))
    return files


def update_scan_state(repo_name: str):
    """更新扫描状态"""
    repos = get_repos()
    if repo_name not in repos:
        return
    local_path = repos[repo_name].get("local", f"/tmp/svn_repos/{repo_name}")

    os.makedirs("/tmp/svn_repos", exist_ok=True)
    state_file = f"/tmp/svn_repos/.scan_state_{repo_name}.json"

    cmd = svn_auth_cmd(["svn", "info", "--show-item", "revision"])
    rc, out, err = run_cmd(cmd, cwd=local_path)
    if rc == 0:
        with open(state_file, "w") as f:
            json.dump({"last_rev": out.strip()}, f)


def sync_all_repos():
    """同步所有仓库"""
    for repo_name in get_repos():
        checkout_or_update(repo_name)


def list_repos():
    """列出所有已配置的仓库"""
    repos = get_repos()
    if not repos:
        print("No repos configured. Create config.json first.")
        return
    for name, info in repos.items():
        print(f"  {name}: {info.get('lang')} - {info.get('url')}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 svn_manager.py <action> [args]")
        print("  list              - 列出所有已配置仓库")
        print("  sync              - 同步所有仓库")
        print("  sync <repo_name>  - 同步指定仓库")
        print("  changed <repo>    - 获取变更文件")
        sys.exit(1)

    action = sys.argv[1]

    if action == "list":
        list_repos()
    elif action == "sync":
        if len(sys.argv) >= 3:
            checkout_or_update(sys.argv[2])
        else:
            sync_all_repos()
    elif action == "changed" and len(sys.argv) >= 3:
        files = get_changed_files_local(sys.argv[2])
        print("\n".join(files))
    else:
        print(f"Unknown action: {action}", file=sys.stderr)
        sys.exit(1)
