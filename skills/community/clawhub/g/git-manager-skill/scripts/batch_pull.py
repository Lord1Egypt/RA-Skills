#!/usr/bin/env python3
"""
batch_pull.py - 批量拉取/更新本地 Git 仓库
扫描指定目录下所有 git 仓库并执行 pull/fetch/rebase
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


def is_git_repo(path: Path) -> bool:
    return (path / ".git").exists() or (path / "HEAD").exists()


def find_git_repos(root: str, max_depth: int = 3) -> list:
    """递归查找指定目录下所有 git 仓库"""
    repos = []
    root_path = Path(root)
    if not root_path.exists():
        print(f"[ERROR] 目录不存在: {root}")
        return repos

    def _scan(path: Path, depth: int):
        if depth > max_depth:
            return
        if is_git_repo(path):
            repos.append(str(path))
            return  # 找到 git 仓库就不再深入
        try:
            for child in sorted(path.iterdir()):
                if child.is_dir() and not child.name.startswith("."):
                    _scan(child, depth + 1)
        except PermissionError:
            pass

    _scan(root_path, 0)
    return repos


def git_run(args: list, cwd: str) -> tuple[int, str, str]:
    """执行 git 命令，返回 (returncode, stdout, stderr)"""
    result = subprocess.run(
        ["git"] + args,
        cwd=cwd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=120,
    )
    return result.returncode, result.stdout.strip(), result.stderr.strip()


def get_repo_info(repo_path: str) -> dict:
    """获取仓库基本信息"""
    info = {"path": repo_path, "name": Path(repo_path).name}
    rc, branch, _ = git_run(["rev-parse", "--abbrev-ref", "HEAD"], repo_path)
    info["branch"] = branch if rc == 0 else "unknown"
    rc, remote, _ = git_run(["remote", "get-url", "origin"], repo_path)
    info["remote"] = remote if rc == 0 else "none"
    return info


def update_repo(repo_path: str, mode: str = "pull", rebase: bool = False,
                stash: bool = False, remote: str = "origin", branch: str = None) -> dict:
    """更新单个仓库，返回操作结果"""
    result = {
        "path": repo_path,
        "name": Path(repo_path).name,
        "status": "unknown",
        "message": "",
    }

    try:
        # 获取当前分支
        rc, current_branch, _ = git_run(["rev-parse", "--abbrev-ref", "HEAD"], repo_path)
        result["branch"] = current_branch if rc == 0 else "detached"

        # 检查是否有未提交更改
        rc, diff_stat, _ = git_run(["status", "--porcelain"], repo_path)
        has_changes = bool(diff_stat)

        # 可选：stash 暂存未提交修改
        stashed = False
        if has_changes and stash:
            rc, _, err = git_run(["stash", "push", "-m", "git-manager auto stash"], repo_path)
            if rc == 0:
                stashed = True
                result["message"] += "[stash] "
            else:
                result["status"] = "warn"
                result["message"] += f"stash 失败: {err} "

        if mode == "fetch":
            rc, out, err = git_run(["fetch", remote, "--prune"], repo_path)
            if rc == 0:
                result["status"] = "ok"
                result["message"] += "fetch 成功"
            else:
                result["status"] = "failed"
                result["message"] += err[:100]

        elif mode == "pull":
            pull_args = ["pull"]
            if rebase:
                pull_args.append("--rebase")
            else:
                pull_args.append("--ff-only")
            pull_args.append(remote)
            if branch:
                pull_args.append(branch)

            rc, out, err = git_run(pull_args, repo_path)
            if rc == 0:
                result["status"] = "ok"
                if "Already up to date" in out or "up to date" in out.lower():
                    result["message"] += "已是最新"
                else:
                    result["message"] += "已更新"
            else:
                result["status"] = "failed"
                result["message"] += err[:100]

        # 恢复 stash
        if stashed:
            rc, _, err = git_run(["stash", "pop"], repo_path)
            if rc != 0:
                result["message"] += f" [stash pop 失败: {err[:60]}]"

    except subprocess.TimeoutExpired:
        result["status"] = "timeout"
        result["message"] = "操作超时（>120s）"
    except Exception as e:
        result["status"] = "error"
        result["message"] = str(e)

    return result


def print_result(res: dict, idx: int, total: int):
    status_icons = {
        "ok": "✅",
        "failed": "❌",
        "warn": "⚠️",
        "skipped": "⏭️",
        "timeout": "⏰",
        "error": "💥",
        "unknown": "❓",
    }
    icon = status_icons.get(res["status"], "?")
    branch = res.get("branch", "")
    name = res.get("name", res["path"])
    msg = res.get("message", "")
    print(f"  [{idx:3}/{total}] {icon} {name} [{branch}] - {msg}")


def main():
    parser = argparse.ArgumentParser(
        description="批量拉取/更新本地 Git 仓库",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 扫描 ./repos 下所有仓库并 pull
  python batch_pull.py ./repos

  # 使用 rebase 方式拉取
  python batch_pull.py ./repos --rebase

  # 仅 fetch，不合并
  python batch_pull.py ./repos --fetch

  # 有未提交修改时自动 stash
  python batch_pull.py ./repos --stash

  # 并发执行（加速）
  python batch_pull.py ./repos --workers 4

  # 只更新仓库名含 'api' 的
  python batch_pull.py ./repos --filter api
"""
    )
    parser.add_argument("root", help="要扫描的根目录")
    parser.add_argument("--fetch", action="store_true", help="仅 fetch，不合并")
    parser.add_argument("--rebase", action="store_true", help="使用 rebase 拉取")
    parser.add_argument("--stash", action="store_true", help="遇到未提交修改时自动 stash")
    parser.add_argument("--remote", default="origin", help="远端名称（默认 origin）")
    parser.add_argument("--branch", default=None, help="指定拉取分支")
    parser.add_argument("--max-depth", type=int, default=3, help="扫描目录深度（默认 3）")
    parser.add_argument("--filter", default=None, help="只处理仓库名含该字符串的仓库")
    parser.add_argument("--workers", type=int, default=1, help="并发线程数（默认 1）")
    parser.add_argument("--dry-run", action="store_true", help="仅列出，不执行")

    args = parser.parse_args()

    # 查找仓库
    print(f"\n[扫描] {args.root}（最大深度: {args.max_depth}）")
    repos = find_git_repos(args.root, args.max_depth)

    if args.filter:
        repos = [r for r in repos if args.filter.lower() in Path(r).name.lower()]
        print(f"[过滤] 名称含 '{args.filter}'")

    if not repos:
        print("[WARN] 未找到任何 git 仓库")
        sys.exit(0)

    print(f"[找到] {len(repos)} 个仓库\n")

    if args.dry_run:
        for i, r in enumerate(repos, 1):
            info = get_repo_info(r)
            print(f"  {i:3}. {info['name']} [{info['branch']}]  {info['remote']}")
        sys.exit(0)

    mode = "fetch" if args.fetch else "pull"
    print(f"操作模式: {mode.upper()}" + (" --rebase" if args.rebase else "") + "\n")
    print("─" * 60)

    results = []
    total = len(repos)

    if args.workers > 1:
        # 并发模式
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            futures = {
                executor.submit(
                    update_repo, r, mode, args.rebase, args.stash, args.remote, args.branch
                ): r
                for r in repos
            }
            done_count = 0
            for future in as_completed(futures):
                done_count += 1
                res = future.result()
                results.append(res)
                print_result(res, done_count, total)
    else:
        # 顺序模式
        for i, r in enumerate(repos, 1):
            res = update_repo(r, mode, args.rebase, args.stash, args.remote, args.branch)
            results.append(res)
            print_result(res, i, total)

    # 统计
    ok = sum(1 for r in results if r["status"] == "ok")
    failed = sum(1 for r in results if r["status"] in ("failed", "error", "timeout"))
    print("\n" + "=" * 60)
    print(f"完成  ✅ 成功: {ok}  ❌ 失败: {failed}  总计: {total}")
    if failed:
        print("\n失败列表:")
        for r in results:
            if r["status"] in ("failed", "error", "timeout"):
                print(f"  - {r['name']}: {r['message']}")
    print("=" * 60)

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
