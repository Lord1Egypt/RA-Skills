#!/usr/bin/env python3
"""
Git LFS 专用工具
支持跟踪模式管理、LFS 文件扫描、迁移等功能
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def run_git_lfs(args_list, repo_path):
    """运行 git lfs 命令"""
    cmd = ["git", "lfs"] + args_list
    result = subprocess.run(
        cmd,
        cwd=repo_path,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result


def cmd_install(args):
    """初始化 Git LFS"""
    print(f"[Git LFS] 初始化仓库: {args.repo_dir}")
    result = run_git_lfs(["install"], args.repo_dir)
    if result.returncode == 0:
        print("[成功] Git LFS 已初始化")
        if result.stdout:
            print(result.stdout.strip())
    else:
        print(f"[失败] {result.stderr.strip()}")


def cmd_track(args):
    """添加 LFS 跟踪模式"""
    if not args.patterns:
        print("[错误] 必须指定至少一个文件模式，如 --track '*.zip'")
        return
    print(f"[Git LFS] 添加跟踪模式: {args.patterns}")
    for pattern in args.patterns:
        result = run_git_lfs(["track", pattern], args.repo_dir)
        if result.returncode == 0:
            print(f"  [OK] {pattern}")
        else:
            print(f"  [失败] {pattern}: {result.stderr.strip()}")


def cmd_untrack(args):
    """取消 LFS 跟踪模式"""
    if not args.patterns:
        print("[错误] 必须指定至少一个文件模式")
        return
    print(f"[Git LFS] 取消跟踪模式: {args.patterns}")
    gitattributes = Path(args.repo_dir) / ".gitattributes"
    if not gitattributes.exists():
        print("[提示] .gitattributes 文件不存在")
        return
    content = gitattributes.read_text(encoding="utf-8")
    removed = []
    for pattern in args.patterns:
        new_lines = []
        for line in content.splitlines():
            if not (f'"{pattern}"' in line or pattern in line):
                new_lines.append(line)
        removed_count = len(content.splitlines()) - len(new_lines)
        if removed_count > 0:
            removed.append(pattern)
        content = "\n".join(new_lines)
    gitattributes.write_text(content, encoding="utf-8")
    if removed:
        print(f"  [已移除] {', '.join(removed)}")
    else:
        print("  [未找到匹配项]")


def cmd_fetch(args):
    """LFS Fetch"""
    print(f"[Git LFS] Fetch: {args.repo_dir}")
    extra = ["--all"] if args.all else []
    result = run_git_lfs(["fetch"] + extra, args.repo_dir)
    if result.returncode == 0:
        print("[成功]")
        if result.stdout:
            print(result.stdout.strip())
    else:
        print(f"[失败] {result.stderr.strip()}")


def cmd_pull(args):
    """LFS Pull"""
    print(f"[Git LFS] Pull: {args.repo_dir}")
    result = run_git_lfs(["pull"], args.repo_dir)
    if result.returncode == 0:
        print("[成功]")
        if result.stdout:
            print(result.stdout.strip())
    else:
        print(f"[失败] {result.stderr.strip()}")


def cmd_push(args):
    """LFS Push"""
    print(f"[Git LFS] Push: {args.repo_dir}")
    extra = ["--all"] if args.all else []
    result = run_git_lfs(["push"] + extra + ["origin", args.branch or "main"], args.repo_dir)
    if result.returncode == 0:
        print("[成功]")
        if result.stdout:
            print(result.stdout.strip())
    else:
        print(f"[失败] {result.stderr.strip()}")


def cmd_ls_files(args):
    """列出 LFS 跟踪的文件"""
    print(f"[Git LFS] 列出跟踪文件: {args.repo_dir}")
    result = run_git_lfs(["ls-files", "--long"], args.repo_dir)
    if result.returncode == 0:
        lines = result.stdout.strip().splitlines()
        if lines:
            print(f"[{len(lines)} 个文件]")
            for line in lines:
                print(f"  {line}")
        else:
            print("[无 LFS 文件]")
    else:
        print(f"[失败] {result.stderr.strip()}")


def cmd_ls_tracks(args):
    """列出当前跟踪模式"""
    print(f"[Git LFS] 当前跟踪模式: {args.repo_dir}")
    gitattributes = Path(args.repo_dir) / ".gitattributes"
    if not gitattributes.exists():
        print("[无] .gitattributes 不存在")
        return
    content = gitattributes.read_text(encoding="utf-8")
    lines = [l.strip() for l in content.splitlines() if l.strip() and not l.strip().startswith("#")]
    if lines:
        print(f"[{len(lines)} 个规则]")
        for line in lines:
            print(f"  {line}")
    else:
        print("[无跟踪规则]")


def cmd_scan(args):
    """扫描仓库中的 LFS 对象"""
    print(f"[Git LFS] 扫描仓库: {args.repo_dir}")
    result = run_git_lfs(["ls-files", "--size"], args.repo_dir)
    if result.returncode == 0:
        lines = [l for l in result.stdout.strip().splitlines() if l.strip()]
        print(f"[{len(lines)} 个 LFS 对象]")
        for line in lines[: args.limit or 20]:
            print(f"  {line}")
        if len(lines) > (args.limit or 20):
            print(f"  ... 还有 {len(lines) - (args.limit or 20)} 个")
    else:
        print(f"[失败] {result.stderr.strip()}")


def cmd_status(args):
    """显示 LFS 状态"""
    print(f"[Git LFS] 状态: {args.repo_dir}")
    result = run_git_lfs(["status"], args.repo_dir)
    if result.returncode == 0:
        print(result.stdout.strip())
    else:
        print(f"[失败] {result.stderr.strip()}")


def cmd_migrate(args):
    """迁移文件到 LFS 或从 LFS 迁出"""
    print(f"[Git LFS] 迁移: {args.repo_dir}")
    if not args.pattern:
        print("[错误] 必须指定 --pattern 参数")
        return
    to_backend = args.to or "lfs"
    print(f"[迁移] 模式: {args.pattern} -> {to_backend}")
    result = run_git_lfs(
        ["migrate", "import", "--include=" + args.pattern, "--fixup"],
        args.repo_dir,
    )
    if result.returncode == 0:
        print("[成功] 迁移完成")
        if result.stdout:
            print(result.stdout.strip())
        print("\n[提示] 迁移后请提交更改: git add -A && git commit -m 'Migrate to LFS'")
    else:
        print(f"[失败] {result.stderr.strip()}")


def main():
    parser = argparse.ArgumentParser(
        description="Git LFS 专用工具 - 跟踪模式管理、文件扫描、迁移",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_install = sub.add_parser("install", help="初始化 Git LFS")
    p_install.add_argument("repo_dir", help="仓库路径")

    p_track = sub.add_parser("track", help="添加 LFS 跟踪模式")
    p_track.add_argument("repo_dir", help="仓库路径")
    p_track.add_argument("patterns", nargs="+", help="文件模式，如 *.zip *.psd")

    p_untrack = sub.add_parser("untrack", help="取消 LFS 跟踪模式")
    p_untrack.add_argument("repo_dir", help="仓库路径")
    p_untrack.add_argument("patterns", nargs="+", help="文件模式")

    p_fetch = sub.add_parser("fetch", help="LFS Fetch")
    p_fetch.add_argument("repo_dir", help="仓库路径")
    p_fetch.add_argument("--all", action="store_true", help="抓取所有引用")

    p_pull = sub.add_parser("pull", help="LFS Pull")
    p_pull.add_argument("repo_dir", help="仓库路径")

    p_push = sub.add_parser("push", help="LFS Push")
    p_push.add_argument("repo_dir", help="仓库路径")
    p_push.add_argument("--all", action="store_true", help="推送所有引用")
    p_push.add_argument("--branch", default=None, help="指定分支")

    p_ls_files = sub.add_parser("ls-files", help="列出 LFS 跟踪的文件")
    p_ls_files.add_argument("repo_dir", help="仓库路径")

    p_ls_tracks = sub.add_parser("ls-tracks", help="列出当前跟踪模式")
    p_ls_tracks.add_argument("repo_dir", help="仓库路径")

    p_scan = sub.add_parser("scan", help="扫描仓库中的 LFS 对象")
    p_scan.add_argument("repo_dir", help="仓库路径")
    p_scan.add_argument("--limit", type=int, default=20, help="最多显示数量")

    p_status = sub.add_parser("status", help="显示 LFS 状态")
    p_status.add_argument("repo_dir", help="仓库路径")

    p_migrate = sub.add_parser("migrate", help="迁移文件到 LFS 或从 LFS 迁出")
    p_migrate.add_argument("repo_dir", help="仓库路径")
    p_migrate.add_argument("--pattern", required=True, help="文件模式，如 '*.zip'")
    p_migrate.add_argument(
        "--to",
        default="lfs",
        choices=["lfs", "git"],
        help="迁移目标: lfs 或 git (默认: lfs)",
    )

    args = parser.parse_args()

    cmd_map = {
        "install": cmd_install,
        "track": cmd_track,
        "untrack": cmd_untrack,
        "fetch": cmd_fetch,
        "pull": cmd_pull,
        "push": cmd_push,
        "ls-files": cmd_ls_files,
        "ls-tracks": cmd_ls_tracks,
        "scan": cmd_scan,
        "status": cmd_status,
        "migrate": cmd_migrate,
    }

    cmd_map[args.cmd](args)


if __name__ == "__main__":
    main()
