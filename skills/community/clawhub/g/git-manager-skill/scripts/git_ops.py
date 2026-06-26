#!/usr/bin/env python3
"""
git_ops.py - Git 仓库操作工具（增强版）
支持：克隆、拉取、合并、衍合、提交、暂存区操作、Git LFS
"""

import argparse
import subprocess
import sys
import re
import os
from pathlib import Path
from typing import Optional


# ─────────────────────────────────────────────
# 工具函数
# ─────────────────────────────────────────────

def run_git(args: list, cwd: str = None, capture: bool = True,
            check: bool = True, env: dict = None) -> subprocess.CompletedProcess:
    """执行 git 命令并返回结果"""
    cmd = ["git"] + args
    cwd = cwd or os.getcwd()
    # 统一路径为绝对路径
    cwd = str(Path(cwd).resolve())

    print(f"  $ git {' '.join(args)}")

    full_env = os.environ.copy()
    if env:
        full_env.update(env)

    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=capture,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=full_env,
        )
        if result.stdout:
            sys.stdout.write(result.stdout)
        if result.stderr:
            sys.stderr.write(result.stderr)
        if check and result.returncode != 0:
            return result
        return result
    except FileNotFoundError:
        print("[ERROR] git 未安装或不在 PATH 中")
        sys.exit(1)


def _check_repo(path: str) -> bool:
    """检查目录是否为 git 仓库"""
    p = Path(path)
    if not p.exists():
        print(f"[ERROR] 路径不存在: {path}")
        return False
    if not (p / ".git").exists():
        print(f"[ERROR] 不是 git 仓库（缺少 .git 目录）: {path}")
        return False
    return True


def _fmt_bytes(n: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if abs(n) < 1024:
            return f"{n:.1f}{unit}"
        n /= 1024
    return f"{n:.1f}TB"


# ─────────────────────────────────────────────
# 基础操作：clone / pull / fetch
# ─────────────────────────────────────────────

def cmd_clone(args):
    """克隆仓库"""
    cmd = ["clone", "--progress"]
    if args.branch:
        cmd += ["-b", args.branch]
    if args.depth:
        cmd += ["--depth", str(args.depth)]
    if args.bare:
        cmd.append("--bare")
    if args.single_branch:
        cmd.append("--single-branch")
    if args.shallow_submodules:
        cmd.append("--shallow-submodules")
    cmd.append(args.url)
    if args.dest:
        cmd.append(args.dest)

    print(f"\n[克隆] {args.url} -> {args.dest or '当前目录'}")
    result = run_git(cmd, check=False)
    if result.returncode == 0:
        print("[OK] 克隆成功")
        if args.lfs:
            target = args.dest or Path.cwd() / Path(args.url).stem
            cmd_lfs_install(target, quiet=False)
    else:
        print("[FAIL] 克隆失败")
        sys.exit(1)


def cmd_pull(args):
    """拉取更新"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["pull", "--progress"]
    if args.rebase:
        cmd = ["pull", "--rebase", "--progress"]
    if args.ff_only:
        cmd.append("--ff-only")
    if args.no_commit:
        cmd.append("--no-commit")
    cmd.append(args.remote or "origin")
    if args.branch:
        cmd.append(args.branch)

    print(f"\n[拉取] {args.repo_path}")
    result = run_git(cmd, cwd=args.repo_path, check=False)
    if result.returncode == 0:
        print("[OK] 拉取成功")
    else:
        print("[FAIL] 拉取失败")
        sys.exit(1)


def cmd_fetch(args):
    """获取远端更新"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["fetch", "--progress"]
    if args.all:
        cmd.append("--all")
    elif args.remote:
        cmd.append(args.remote)
    if args.prune:
        cmd.append("--prune")
    if args.tags:
        cmd.append("--tags")
    if args.depth:
        cmd += ["--depth", str(args.depth)]

    print(f"\n[Fetch] {args.repo_path}")
    result = run_git(cmd, cwd=args.repo_path, check=False)
    if result.returncode == 0:
        print("[OK] Fetch 成功")
    else:
        print("[FAIL] Fetch 失败")
        sys.exit(1)


# ─────────────────────────────────────────────
# 分支操作：branch / checkout
# ─────────────────────────────────────────────

def cmd_branch(args):
    """分支管理"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["branch"]
    if args.list:
        cmd.append("-a")
    elif args.create:
        cmd = ["checkout", "-b", args.branch_name]
    elif args.delete and args.branch_name:
        if args.force:
            cmd = ["branch", "-D", args.branch_name]
        else:
            cmd = ["branch", "-d", args.branch_name]
    elif args.rename and args.branch_name:
        cmd = ["branch", "-m", args.branch_name, args.new_name]
    elif args.copy and args.branch_name:
        cmd = ["branch", "-c", args.branch_name, args.new_name]
    elif args.set_upstream:
        cmd = ["branch", "-u", args.set_upstream]
        if args.branch_name:
            cmd.insert(2, args.branch_name)

    result = run_git(cmd, cwd=args.repo_path, check=False)
    if result.returncode == 0:
        print("[OK] 分支操作成功")
    else:
        sys.exit(1)


def cmd_checkout(args):
    """切换分支"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["checkout"]
    if args.create:
        cmd.append("-b")
    if args.force:
        cmd.append("--force")
    if args.orphan:
        cmd = ["checkout", "--orphan", args.branch]
    elif args.branch:
        cmd.append(args.branch)

    print(f"\n[切换分支] {args.repo_path} -> {args.branch or '(当前)'}")
    result = run_git(cmd, cwd=args.repo_path, check=False)
    if result.returncode == 0:
        print("[OK] 切换成功")
    else:
        sys.exit(1)


# ─────────────────────────────────────────────
# 合并与衍合
# ─────────────────────────────────────────────

def cmd_merge(args):
    """合并分支"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["merge"]
    if args.no_ff:
        cmd.append("--no-ff")
    if args.squash:
        cmd.append("--squash")
    if args.abort:
        cmd = ["merge", "--abort"]
    if args.continue_:
        cmd = ["merge", "--continue"]
    if args.message:
        cmd += ["-m", args.message]
    if args.branch:
        cmd.append(args.branch)

    print(f"\n[合并] {args.repo_path} <- {args.branch or '继续'}")
    result = run_git(cmd, cwd=args.repo_path, check=False)
    if result.returncode == 0:
        print("[OK] 合并成功")
    else:
        print("[FAIL] 合并失败（可能存在冲突，请手动解决）")
        sys.exit(1)


def cmd_rebase(args):
    """衍合"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["rebase"]
    if args.interactive:
        cmd.append("-i")
    if args.onto:
        cmd += ["--onto", args.onto]
    if args.abort:
        cmd = ["rebase", "--abort"]
    if args.continue_:
        cmd = ["rebase", "--continue"]
    if args.skip:
        cmd = ["rebase", "--skip"]
    if args.branch:
        cmd.append(args.branch)

    print(f"\n[衍合] {args.repo_path} onto {args.onto or args.branch or 'upstream'}")
    result = run_git(cmd, cwd=args.repo_path, check=False)
    if result.returncode == 0:
        print("[OK] 衍合成功")
    else:
        print("[FAIL] 衍合失败（可能存在冲突，请手动解决）")
        sys.exit(1)


# ─────────────────────────────────────────────
# 暂存区 / 提交
# ─────────────────────────────────────────────

def cmd_add(args):
    """暂存文件"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["add"]
    if args.all:
        cmd = ["add", "-A"]
    elif args.update:
        cmd = ["add", "-u"]
    elif args.patch:
        cmd = ["add", "-p"]
    elif args.interactive:
        cmd = ["add", "-i"]
    else:
        cmd += args.files

    print(f"\n[暂存] {args.repo_path}: {' '.join(args.files) if args.files else '全部'}")
    result = run_git(cmd, cwd=args.repo_path, check=False)
    if result.returncode == 0:
        print("[OK] 暂存成功")
    else:
        sys.exit(1)


def cmd_reset(args):
    """重置暂存区"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["reset"]
    if args.soft:
        cmd.append("--soft")
    elif args.mixed:
        cmd.append("--mixed")
    elif args.hard:
        cmd.append("--hard")
    if args.commit:
        cmd.append(args.commit)
    elif args.files:
        cmd += args.files

    scope = "HEAD" if not args.commit and not args.files else (args.commit or "文件")
    print(f"\n[Reset {scope}] {args.repo_path}")
    result = run_git(cmd, cwd=args.repo_path, check=False)
    if result.returncode == 0:
        print("[OK] 重置成功")
    else:
        sys.exit(1)


def cmd_commit(args):
    """提交暂存区"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["commit"]
    if args.message:
        cmd += ["-m", args.message]
    if args.amend:
        cmd.append("--amend")
    if args.no_edit:
        cmd.append("--no-edit")
    if args.all:
        cmd.append("-a")
    if args.allow_empty:
        cmd.append("--allow-empty")
    if args.allow_new:
        cmd.append("--allow-empty")

    print(f"\n[提交] {args.repo_path}")
    result = run_git(cmd, cwd=args.repo_path, check=False)
    if result.returncode == 0:
        print("[OK] 提交成功")
    else:
        sys.exit(1)


def cmd_stash(args):
    """暂存工作区修改"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["stash"]
    if args.save:
        cmd += ["save", args.save]
        if args.include_untracked:
            cmd.append("--include-untracked")
    elif args.pop:
        cmd = ["stash", "pop"]
        if args.stash_id:
            cmd.append(args.stash_id)
    elif args.apply:
        cmd = ["stash", "apply"]
        if args.stash_id:
            cmd.append(args.stash_id)
    elif args.list:
        cmd = ["stash", "list"]
        run_git(cmd, cwd=args.repo_path)
        return
    elif args.show:
        cmd = ["stash", "show"]
        if args.stash_id:
            cmd.append(args.stash_id)
        run_git(cmd, cwd=args.repo_path)
        return
    elif args.drop:
        cmd = ["stash", "drop"]
        if args.stash_id:
            cmd.append(args.stash_id)
    elif args.clear:
        cmd = ["stash", "clear"]

    print(f"\n[Stash] {args.repo_path}")
    result = run_git(cmd, cwd=args.repo_path, check=False)
    if result.returncode == 0:
        print("[OK] 操作成功")
    else:
        sys.exit(1)


# ─────────────────────────────────────────────
# 查看操作：diff / log / status / show / blame
# ─────────────────────────────────────────────

def cmd_diff(args):
    """查看差异"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["diff"]
    if args.staged:
        cmd.append("--cached")
    if args.stat:
        cmd.append("--stat")
    if args.name_only:
        cmd.append("--name-only")
    if args.name_status:
        cmd.append("--name-status")
    if args.color == "never":
        cmd.append("--no-color")
    if args.color == "always":
        cmd.append("--color=always")
    if args.branch:
        cmd.append(args.branch)
    if args.compare:
        cmd.append(args.compare)
    if args.color_words:
        cmd.append("--color-words")
    if args.ws_error_highlight:
        cmd.append("--ws-error-highlight=all")
    if args.files:
        cmd += args.files

    print(f"\n[Diff] {args.repo_path}")
    run_git(cmd, cwd=args.repo_path)


def cmd_status(args):
    """查看状态"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["status"]
    if args.short:
        cmd.append("-s")
    if args.branch:
        cmd.append("-b")
    if args.ignored:
        cmd.append("--ignored")
    if args.untracked_files == "all":
        cmd.append("--untracked-files=all")
    elif args.untracked_files == "no":
        cmd.append("--untracked-files=no")

    print(f"\n[状态] {args.repo_path}")
    run_git(cmd, cwd=args.repo_path)


def cmd_log(args):
    """查看提交历史"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["log"]
    if args.oneline:
        cmd.append("--oneline")
    if args.stat:
        cmd.append("--stat")
    if args.patch:
        cmd.append("-p")
    if args.format_:
        cmd += ["--format", args.format_]
    if args.graph:
        cmd.append("--graph")
    if args.all:
        cmd.append("--all")
    if args.decorate:
        cmd.append("--decorate")
    if args.n:
        cmd.append(f"-{args.n}")
    if args.author:
        cmd += ["--author", args.author]
    if args.since:
        cmd += ["--since", args.since]
    if args.until:
        cmd += ["--until", args.until]
    if args.grep:
        cmd += ["--grep", args.grep]
    if args.file:
        cmd += ["--", args.file]
    if args.branch:
        cmd.append(args.branch)
    if args.reverse:
        cmd.append("--reverse")
    if args.follow:
        cmd.append("--follow")

    print(f"\n[Log] {args.repo_path}")
    run_git(cmd, cwd=args.repo_path)


def cmd_show(args):
    """查看提交或文件详情"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["show"]
    if args.stat:
        cmd.append("--stat")
    if args.name_only:
        cmd.append("--name-only")
    if args.format:
        cmd += ["--format", args.format]
    if args.object:
        cmd.append(args.object)

    print(f"\n[Show] {args.repo_path}")
    run_git(cmd, cwd=args.repo_path)


def cmd_blame(args):
    """文件 blame"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["blame"]
    if args.L:
        cmd += ["-L", f"{args.L},{args.L_end or args.L}"]
    if args.numbers:
        cmd.append("-n")
    cmd.append(args.file)

    print(f"\n[Blame] {args.file}")
    run_git(cmd, cwd=args.repo_path)


def cmd_tag(args):
    """标签管理"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["tag"]
    if args.list:
        run_git(["tag", "-l"], cwd=args.repo_path)
        return
    if args.create:
        cmd.append(args.tag_name)
        if args.message:
            cmd += ["-m", args.message]
        if args.commit:
            cmd.append(args.commit)
    elif args.delete:
        cmd = ["tag", "-d", args.tag_name]
    elif args.push:
        cmd = ["push", args.remote or "origin", args.tag_name]

    print(f"\n[Tag] {args.tag_name}")
    result = run_git(cmd, cwd=args.repo_path, check=False)
    if result.returncode == 0:
        print("[OK] 操作成功")
    else:
        sys.exit(1)


def cmd_remote(args):
    """远端管理"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["remote"]
    if args.list:
        run_git(["remote", "-v"], cwd=args.repo_path)
        return
    if args.add:
        cmd = ["remote", "add", args.remote_name, args.url]
    elif args.remove:
        cmd = ["remote", "remove", args.remote_name]
    elif args.rename:
        cmd = ["remote", "rename", args.remote_name, args.new_name]
    elif args.set_url:
        cmd = ["remote", "set-url", args.remote_name, args.url]
    elif args.show:
        cmd = ["remote", "show", args.remote_name]

    print(f"\n[Remote] {args.remote_name or ''}")
    result = run_git(cmd, cwd=args.repo_path, check=False)
    if result.returncode == 0:
        print("[OK] 操作成功")
    else:
        sys.exit(1)


def cmd_clean(args):
    """清理未跟踪文件"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["clean"]
    if args.dry_run:
        cmd.append("--dry-run")
    if args.dirs:
        cmd.append("-d")
    if args.force:
        cmd.append("-f")
    if args.files:
        cmd += args.files

    print(f"\n[Clean] {args.repo_path}")
    result = run_git(cmd, cwd=args.repo_path, check=False)
    if result.returncode == 0:
        print("[OK] 清理完成")
    else:
        sys.exit(1)


def cmd_gc(args):
    """垃圾回收"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["gc"]
    if args.aggressive:
        cmd.append("--aggressive")
    if args.prune:
        cmd += ["--prune=now"]
    if args.auto:
        cmd.append("--auto")

    print(f"\n[GC] {args.repo_path}")
    result = run_git(cmd, cwd=args.repo_path, check=False)
    if result.returncode == 0:
        print("[OK] GC 完成")
    else:
        sys.exit(1)


def cmd_reflog(args):
    """查看引用日志（找回丢失的提交）"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["reflog"]
    if args.show:
        cmd = ["reflog", "show"]
    if args.expire:
        cmd = ["reflog", "expire"]
        if args.dry_run:
            cmd.append("--dry-run")
        if args.all:
            cmd.append("--all")
    if args.n:
        cmd.append(f"-{args.n}")
    if args.ref:
        cmd.append(args.ref)

    print(f"\n[Reflog] {args.repo_path}")
    run_git(cmd, cwd=args.repo_path)


def cmd_describe(args):
    """显示基于最近标签的语义化版本"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["describe"]
    if args.all:
        cmd.append("--all")
    if args.tags:
        cmd.append("--tags")
    if args.always:
        cmd.append("--always")
    if args.abbrev:
        cmd += ["--abbrev", str(args.abbrev)]
    if args.exact_match:
        cmd.append("--exact-match")
    if args.long:
        cmd.append("--long")
    if args.candidates:
        cmd += ["--candidates", str(args.candidates)]
    if args.match:
        cmd += ["--match", args.match]
    if args.exclude:
        cmd += ["--exclude", args.exclude]
    if args.contains:
        cmd += ["--contains", args.contains]
    if args.connected:
        cmd.append("--always")
    if args.debug:
        cmd.append("--debug")
    if args.object:
        cmd.append(args.object)

    print(f"\n[Describe] {args.repo_path}")
    result = run_git(cmd, cwd=args.repo_path, check=False)
    if result.returncode != 0:
        print("[提示] 当前没有任何标签，请先使用 tag 命令创建标签")
        sys.exit(1)


def cmd_worktree(args):
    """工作树管理"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["worktree"]
    if args.list:
        run_git(["worktree", "list"], cwd=args.repo_path)
        return
    if args.add:
        cmd = ["worktree", "add"]
        if args.force:
            cmd.append("--force")
        if args.checkout:
            cmd += ["-b", args.checkout]
        cmd.append(args.path)
        if args.branch:
            cmd.append(args.branch)
    elif args.remove:
        cmd = ["worktree", "remove"]
        if args.force:
            cmd.append("--force")
        cmd.append(args.path)
    elif args.prune:
        cmd = ["worktree", "prune"]
        if args.dry_run:
            cmd.append("--dry-run")
        if args.verbose:
            cmd.append("--verbose")
    elif args.lock:
        cmd = ["worktree", "lock"]
        if args.reason:
            cmd += ["--reason", args.reason]
        cmd.append(args.path)
    elif args.unlock:
        cmd = ["worktree", "unlock"]
        cmd.append(args.path)

    print(f"\n[Worktree] {args.repo_path}")
    result = run_git(cmd, cwd=args.repo_path, check=False)
    if result.returncode == 0:
        print("[OK] 操作成功")
    else:
        sys.exit(1)


def cmd_grep(args):
    """在仓库中搜索文本"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["grep"]
    if args.ignore_case:
        cmd.append("-i")
    if args.regexp_extended:
        cmd.append("-E")
    if args.regexp_basic:
        cmd.append("-G")
    if args.fixed_strings:
        cmd.append("-F")
    if args.invert:
        cmd.append("--invert-match")
    if args.word_regexp:
        cmd.append("-w")
    if args.line_no:
        cmd.append("-n")
    if args.count:
        cmd.append("-c")
    if args.files_with_matches:
        cmd.append("-l")
    if args.files_without_match:
        cmd.append("-L")
    if args.column:
        cmd.append("--column")
    if args.extended:
        cmd.append("--extended-regexp")
    if args.only_matching:
        cmd.append("-o")
    if args.max_count:
        cmd += ["--max-count", str(args.max_count)]
    if args.context:
        cmd += ["--context", str(args.context)]
    if args.before_context:
        cmd += ["-B", str(args.before_context)]
    if args.after_context:
        cmd += ["-A", str(args.after_context)]
    if args.branch:
        cmd.append(args.branch)
    if args.pattern:
        cmd.append(args.pattern)
    if args.files:
        cmd += ["--"] + args.files

    print(f"\n[Grep] {args.repo_path}: {args.pattern or ''}")
    run_git(cmd, cwd=args.repo_path)


def cmd_cherry_pick(args):
    """选取性应用提交"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["cherry-pick"]
    if args.continue_:
        cmd = ["cherry-pick", "--continue"]
    elif args.abort:
        cmd = ["cherry-pick", "--abort"]
    elif args.skip:
        cmd = ["cherry-pick", "--skip"]
    else:
        if args.no_commit:
            cmd.append("--no-commit")
        if args.mainline:
            cmd += ["--mainline", str(args.mainline)]
        if args.edit:
            cmd.append("--edit")
        if args.cleanup:
            cmd += ["--cleanup", args.cleanup]
        if args.no_verify:
            cmd.append("-n")
        if args.include:
            for c in args.include:
                cmd += ["-x", c]
        if args.exclude:
            for c in args.exclude:
                cmd += ["--no-commit"]  # 跳过
        if args.ff:
            cmd.append("--ff")
        if args.force:
            cmd.append("--force")
        if args.quiet:
            cmd.append("-q")
        if args.commit:
            cmd.append(args.commit)

    print(f"\n[Cherry-Pick] {args.repo_path}")
    result = run_git(cmd, cwd=args.repo_path, check=False)
    if result.returncode == 0:
        print("[OK] Cherry-pick 成功")
    else:
        print("[FAIL] Cherry-pick 失败（可能存在冲突，请手动解决）")
        sys.exit(1)


def cmd_revert(args):
    """生成反向提交（安全撤销）"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["revert"]
    if args.continue_:
        cmd = ["revert", "--continue"]
    elif args.abort:
        cmd = ["revert", "--abort"]
    elif args.skip:
        cmd = ["revert", "--skip"]
    else:
        if args.no_commit:
            cmd.append("--no-commit")
        if args.edit:
            cmd.append("--edit")
        if args.no_verify:
            cmd.append("-n")
        if args.cleanup:
            cmd += ["--cleanup", args.cleanup]
        if args.quiet:
            cmd.append("-q")
        if args.include:
            for c in args.include:
                cmd.append(c)
        if args.exclude:
            for c in args.exclude:
                cmd.append(c)
        if args.ff:
            cmd.append("--ff")
        if args.commit:
            cmd.append(args.commit)

    print(f"\n[Revert] {args.repo_path}")
    result = run_git(cmd, cwd=args.repo_path, check=False)
    if result.returncode == 0:
        print("[OK] Revert 成功")
    else:
        print("[FAIL] Revert 失败（可能存在冲突，请手动解决）")
        sys.exit(1)


def cmd_bisect(args):
    """二分查找定位 bug"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["bisect"]
    if args.start:
        cmd = ["bisect", "start"]
        if args.bad:
            cmd.append(args.bad)
        if args.good:
            cmd.append(args.good)
    elif args.good:
        cmd = ["bisect", "good", args.good]
    elif args.bad:
        cmd = ["bisect", "bad", args.bad]
    elif args.skip:
        cmd = ["bisect", "skip"]
        if args.revision:
            cmd.append(args.revision)
    elif args.reset:
        cmd = ["bisect", "reset"]
        if args.revision:
            cmd.append(args.revision)
    elif args.terms:
        cmd = ["bisect", "terms", args.terms]
    elif args.visual:
        cmd = ["bisect", "visualize"]
    elif args.log:
        cmd = ["bisect", "log"]
    elif args.run:
        cmd = ["bisect", "run"]
        if args.command:
            cmd.append(args.command)
    else:
        # 默认：启动 bisect
        cmd = ["bisect", "start"]

    print(f"\n[Bisect] {args.repo_path}")
    result = run_git(cmd, cwd=args.repo_path, check=False)
    if result.returncode != 0:
        print("[提示] bisect 需要提供已知 good/bad 提交，如: git_ops.py bisect ./repo --start HEAD v1.0.0")
        sys.exit(1)
    else:
        print("[OK] Bisect 操作成功")


def cmd_lfs(args):
    """Git LFS 操作"""
    if not _check_repo(args.repo_path):
        sys.exit(1)
    cmd = ["lfs"]
    if args.install:
        run_git(["lfs", "install"], cwd=args.repo_path)
        print("[OK] Git LFS 初始化完成")
        return
    if args.track:
        patterns = args.patterns or ["*"]
        for p in patterns:
            run_git(["lfs", "track", p], cwd=args.repo_path)
        print(f"[OK] 跟踪模式: {', '.join(patterns)}")
        return
    if args.untrack:
        patterns = args.untrack
        for p in patterns:
            run_git(["lfs", "track", "--exclude", p], cwd=args.repo_path)
        print(f"[OK] 取消跟踪: {', '.join(patterns)}")
        return
    if args.fetch:
        run_git(["lfs", "fetch"], cwd=args.repo_path)
        print("[OK] LFS Fetch 完成")
        return
    if args.pull:
        run_git(["lfs", "pull"], cwd=args.repo_path)
        print("[OK] LFS Pull 完成")
        return
    if args.push:
        cmd = ["lfs", "push"]
        if args.remote:
            cmd += [args.remote, args.branch or "main"]
        run_git(cmd, cwd=args.repo_path)
        print("[OK] LFS Push 完成")
        return
    if args.ls_files:
        run_git(["lfs", "ls-files"], cwd=args.repo_path)
        return
    if args.track_list:
        run_git(["lfs", "track"], cwd=args.repo_path)
        return
    if args.scan:
        run_git(["lfs", "scan"], cwd=args.repo_path)
        return

    # 默认显示状态
    run_git(["lfs", "status"], cwd=args.repo_path)


# ─────────────────────────────────────────────
# LFS 初始化（克隆时自动调用）
# ─────────────────────────────────────────────

def cmd_lfs_install(repo_path: str, quiet: bool = True):
    """对已有仓库初始化 LFS"""
    cmd = ["lfs", "install"]
    if quiet:
        cmd.append("--quiet")
    result = run_git(cmd, cwd=repo_path, check=False)
    if result.returncode == 0:
        print(f"  [LFS] 已初始化 Git LFS: {repo_path}")
    else:
        print(f"  [LFS] LFS 初始化失败（git-lfs 可能未安装）")


# ─────────────────────────────────────────────
# 主入口
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Git 仓库操作工具（增强版）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", help="操作命令")

    # ── clone ─────────────────────────────────
    p = subparsers.add_parser("clone", help="克隆仓库")
    p.add_argument("url", help="仓库 URL")
    p.add_argument("dest", nargs="?", help="目标目录")
    p.add_argument("-b", "--branch", help="指定分支")
    p.add_argument("--depth", type=int, help="浅克隆深度")
    p.add_argument("--bare", action="store_true", help="裸仓库")
    p.add_argument("--single-branch", action="store_true", help="只克隆一个分支")
    p.add_argument("--shallow-submodules", action="store_true", help="子模块浅克隆")
    p.add_argument("--lfs", action="store_true", help="克隆后初始化 Git LFS")

    # ── pull ──────────────────────────────────
    p = subparsers.add_parser("pull", help="拉取更新")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("--remote", help="远端名称（默认 origin）")
    p.add_argument("--branch", help="目标分支")
    p.add_argument("--rebase", action="store_true", help="使用 rebase 方式拉取")
    p.add_argument("--ff-only", action="store_true", help="仅快进合并")
    p.add_argument("--no-commit", action="store_true", help="拉取后不自动提交")

    # ── fetch ─────────────────────────────────
    p = subparsers.add_parser("fetch", help="获取远端更新")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("--remote", help="远端名称")
    p.add_argument("--all", action="store_true", help="获取所有远端")
    p.add_argument("--prune", action="store_true", default=True, help="清理失效引用")
    p.add_argument("--tags", action="store_true", help="获取标签")
    p.add_argument("--depth", type=int, help="获取深度")

    # ── branch ─────────────────────────────────
    p = subparsers.add_parser("branch", help="分支管理")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("--list", action="store_true", help="列出分支")
    p.add_argument("--create", action="store_true", help="创建分支")
    p.add_argument("--delete", action="store_true", help="删除分支")
    p.add_argument("--rename", action="store_true", help="重命名分支")
    p.add_argument("--copy", action="store_true", help="复制分支")
    p.add_argument("--force", action="store_true", help="强制操作")
    p.add_argument("-u", "--set-upstream-to", dest="set_upstream", help="设置上游分支（如 -u origin/main）")
    p.add_argument("branch_name", nargs="?", help="分支名")
    p.add_argument("new_name", nargs="?", help="新分支名")

    # ── checkout ───────────────────────────────
    p = subparsers.add_parser("checkout", help="切换分支")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("branch", nargs="?", help="目标分支")
    p.add_argument("--create", "-b", action="store_true", help="创建并切换")
    p.add_argument("--force", "-f", action="store_true", help="强制切换")
    p.add_argument("--orphan", action="store_true", help="切换到新孤儿分支")

    # ── merge ──────────────────────────────────
    p = subparsers.add_parser("merge", help="合并分支")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("branch", nargs="?", help="要合并的分支")
    p.add_argument("--no-ff", action="store_true", help="禁止快进合并")
    p.add_argument("--squash", action="store_true", help="压缩合并")
    p.add_argument("--message", "-m", help="合并提交信息")
    p.add_argument("--abort", action="store_true", help="放弃合并")
    p.add_argument("--continue", dest="continue_", action="store_true", help="继续合并")

    # ── rebase ─────────────────────────────────
    p = subparsers.add_parser("rebase", help="衍合")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("branch", nargs="?", help="要衍合的分支")
    p.add_argument("--onto", help="目标基底")
    p.add_argument("-i", "--interactive", action="store_true", help="交互式衍合")
    p.add_argument("--abort", action="store_true", help="放弃衍合")
    p.add_argument("--continue", dest="continue_", action="store_true", help="继续衍合")
    p.add_argument("--skip", action="store_true", help="跳过当前提交")

    # ── add ─────────────────────────────────────
    p = subparsers.add_parser("add", help="暂存文件")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("files", nargs="*", help="要暂存的文件")
    p.add_argument("-A", "--all", action="store_true", help="暂存全部（包括未跟踪）")
    p.add_argument("-u", "--update", action="store_true", help="暂存已跟踪文件")
    p.add_argument("-p", "--patch", action="store_true", help="交互式暂存补丁")
    p.add_argument("-i", "--interactive", action="store_true", help="交互式暂存")

    # ── commit ─────────────────────────────────
    p = subparsers.add_parser("commit", help="提交")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("-m", "--message", required=True, help="提交信息")
    p.add_argument("-a", "--all", action="store_true", help="自动暂存已跟踪文件")
    p.add_argument("--amend", action="store_true", help="修改上一次提交")
    p.add_argument("--no-edit", action="store_true", help="仅修改提交信息不改变内容")
    p.add_argument("--allow-empty", action="store_true", help="允许空提交")

    # ── reset ───────────────────────────────────
    p = subparsers.add_parser("reset", help="重置暂存区")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("commit", nargs="?", help="重置到指定提交")
    p.add_argument("files", nargs="*", help="要取消暂存的文件")
    p.add_argument("--soft", action="store_true", help="软重置（保留修改）")
    p.add_argument("--mixed", action="store_true", help="混合重置（默认）")
    p.add_argument("--hard", action="store_true", help="硬重置（丢弃修改）")

    # ── stash ───────────────────────────────────
    p = subparsers.add_parser("stash", help="暂存工作区修改")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("--save", metavar="MSG", help="保存并附加信息")
    p.add_argument("-u", "--include-untracked", action="store_true", help="同时暂存未跟踪文件")
    p.add_argument("--pop", action="store_true", help="弹出最近 stash")
    p.add_argument("--apply", action="store_true", help="应用最近 stash（不删除）")
    p.add_argument("--list", action="store_true", help="列出所有 stash")
    p.add_argument("--show", action="store_true", help="显示 stash 内容")
    p.add_argument("--drop", action="store_true", help="删除 stash")
    p.add_argument("--clear", action="store_true", help="清空所有 stash")
    p.add_argument("stash_id", nargs="?", help="Stash 编号（如 stash@{0}）")

    # ── diff ────────────────────────────────────
    p = subparsers.add_parser("diff", help="查看差异")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("files", nargs="*", help="比较的文件")
    p.add_argument("--staged", action="store_true", help="比较暂存区与 HEAD")
    p.add_argument("--stat", action="store_true", help="显示统计信息")
    p.add_argument("--name-only", action="store_true", help="只显示文件名")
    p.add_argument("--name-status", action="store_true", help="显示文件状态")
    p.add_argument("--branch", help="比较分支")
    p.add_argument("--compare", help="比较两个提交（如 abc..def）")
    p.add_argument("--color", choices=["auto", "always", "never"], default="auto")
    p.add_argument("--color-words", action="store_true", help="词级别高亮差异")
    p.add_argument("--ws-error-highlight", action="store_true", help="高亮空白符错误")

    # ── status ──────────────────────────────────
    p = subparsers.add_parser("status", help="查看状态")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("-s", "--short", action="store_true", help="简洁格式")
    p.add_argument("-b", "--branch", action="store_true", help="显示分支信息")
    p.add_argument("--ignored", action="store_true", help="显示忽略文件")
    p.add_argument("--untracked-files", choices=["all", "no"], default="normal",
                    help="未跟踪文件处理")

    # ── log ─────────────────────────────────────
    p = subparsers.add_parser("log", help="查看提交历史")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("branch", nargs="?", help="分支名")
    p.add_argument("-n", type=int, help="显示条数")
    p.add_argument("--oneline", action="store_true", help="单行格式")
    p.add_argument("--graph", action="store_true", help="图形化显示")
    p.add_argument("--all", action="store_true", help="显示所有分支")
    p.add_argument("--decorate", action="store_true", help="显示分支标签")
    p.add_argument("--stat", action="store_true", help="显示统计")
    p.add_argument("-p", "--patch", action="store_true", help="显示补丁")
    p.add_argument("--author", help="按作者过滤")
    p.add_argument("--since", help="起始日期（如 2024-01-01）")
    p.add_argument("--until", help="截止日期")
    p.add_argument("--grep", help="按提交信息过滤")
    p.add_argument("--file", help="只看某文件的提交")
    p.add_argument("--format", dest="format_", help="输出格式（如 oneline, short）")
    p.add_argument("--reverse", action="store_true", help="逆序显示")
    p.add_argument("--follow", action="store_true", help="追踪文件重命名历史")

    # ── show ─────────────────────────────────────
    p = subparsers.add_parser("show", help="查看提交详情")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("object", nargs="?", help="对象（提交/标签等）")
    p.add_argument("--stat", action="store_true", help="显示统计")
    p.add_argument("--name-only", action="store_true", help="只显示文件名")
    p.add_argument("--format", help="输出格式（如 oneline, short）")

    # ── blame ────────────────────────────────────
    p = subparsers.add_parser("blame", help="文件逐行历史")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("file", help="文件路径")
    p.add_argument("-L", type=int, help="起始行")
    p.add_argument("--L-end", type=int, dest="L_end", help="结束行")
    p.add_argument("-n", "--numbers", action="store_true", help="显示行号")

    # ── tag ─────────────────────────────────────
    p = subparsers.add_parser("tag", help="标签管理")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("--list", action="store_true", help="列出标签")
    p.add_argument("--create", action="store_true", help="创建标签")
    p.add_argument("--delete", action="store_true", help="删除标签")
    p.add_argument("--push", action="store_true", help="推送标签")
    p.add_argument("tag_name", nargs="?", help="标签名")
    p.add_argument("-m", "--message", help="标签信息")
    p.add_argument("--commit", help="指定提交（默认 HEAD）")
    p.add_argument("--remote", help="远端名称")

    # ── remote ──────────────────────────────────
    p = subparsers.add_parser("remote", help="远端管理")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("--list", action="store_true", help="列出远端")
    p.add_argument("--add", action="store_true", help="添加远端")
    p.add_argument("--remove", action="store_true", help="删除远端")
    p.add_argument("--rename", action="store_true", help="重命名远端")
    p.add_argument("--set-url", action="store_true", help="修改 URL")
    p.add_argument("--show", action="store_true", help="显示远端详情")
    p.add_argument("remote_name", nargs="?", help="远端名称")
    p.add_argument("new_name", nargs="?", help="新名称")
    p.add_argument("url", nargs="?", help="URL")

    # ── clean ────────────────────────────────────
    p = subparsers.add_parser("clean", help="清理未跟踪文件")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("--dry-run", action="store_true", help="预览模式")
    p.add_argument("-d", "--dirs", action="store_true", help="清理目录")
    p.add_argument("-f", "--force", action="store_true", help="强制执行")
    p.add_argument("files", nargs="*", help="指定文件/目录")

    # ── gc ──────────────────────────────────────
    p = subparsers.add_parser("gc", help="垃圾回收")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("--aggressive", action="store_true", help="激进压缩")
    p.add_argument("--prune", action="store_true", help="清理悬空对象")
    p.add_argument("--auto", action="store_true", help="自动模式")

    # ── reflog ───────────────────────────────────
    p = subparsers.add_parser("reflog", help="查看引用日志（找回丢失的提交）")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("ref", nargs="?", help="指定引用（如 HEAD、origin/main）")
    p.add_argument("-n", "--max-count", type=int, dest="n", help="显示条数")
    p.add_argument("--show", action="store_true", help="相当于 git show")
    p.add_argument("--expire", action="store_true", help="清理过期条目")
    p.add_argument("--dry-run", action="store_true", help="预览模式")
    p.add_argument("--all", action="store_true", help="处理所有引用")

    # ── describe ─────────────────────────────────
    p = subparsers.add_parser("describe", help="显示语义化版本（基于最近标签）")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("object", nargs="?", help="描述对象（默认 HEAD）")
    p.add_argument("--all", action="store_true", help="考虑所有分支的标签")
    p.add_argument("--tags", action="store_true", help="只考虑标签")
    p.add_argument("--always", action="store_true", help="当无标签时使用 commit hash")
    p.add_argument("--abbrev", type=int, default=7, help="commit hash 缩写长度（默认 7）")
    p.add_argument("--exact-match", action="store_true", help="只匹配精确的标签")
    p.add_argument("--long", action="store_true", help="始终输出长格式")
    p.add_argument("--candidates", type=int, default=10, help="最多候选标签数（默认 10）")
    p.add_argument("--match", help="只匹配符合条件的标签（glob 模式）")
    p.add_argument("--exclude", help="排除符合条件的标签（glob 模式）")
    p.add_argument("--contains", help="在包含指定提交的标签上停止")
    p.add_argument("--connected", action="store_true", help="验证描述对象连通性")
    p.add_argument("--debug", action="store_true", help="调试信息")

    # ── worktree ─────────────────────────────────
    p = subparsers.add_parser("worktree", help="管理工作树（多分支同时工作）")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("path", nargs="?", help="工作树路径")
    p.add_argument("branch", nargs="?", help="分支名")
    p.add_argument("--list", action="store_true", help="列出所有工作树")
    p.add_argument("--add", action="store_true", help="添加工作树")
    p.add_argument("--remove", action="store_true", help="删除工作树")
    p.add_argument("--prune", action="store_true", help="清理失效工作树")
    p.add_argument("--lock", action="store_true", help="锁定工作树")
    p.add_argument("--unlock", action="store_true", help="解锁工作树")
    p.add_argument("--force", action="store_true", help="强制操作")
    p.add_argument("-b", "--checkout", help="创建并切换到新分支")
    p.add_argument("--reason", help="锁定原因")
    p.add_argument("--dry-run", dest="dry_run", action="store_true", help="预览模式")
    p.add_argument("--verbose", action="store_true", help="详细输出")

    # ── grep ─────────────────────────────────────
    p = subparsers.add_parser("grep", help="在仓库中搜索文本")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("pattern", nargs="?", help="搜索模式（字符串或正则）")
    p.add_argument("files", nargs="*", help="搜索的文件")
    p.add_argument("-i", "--ignore-case", action="store_true", help="忽略大小写")
    p.add_argument("-E", "--regexp-extended", action="store_true", help="扩展正则")
    p.add_argument("-G", "--regexp-basic", action="store_true", help="基本正则（默认）")
    p.add_argument("-F", "--fixed-strings", action="store_true", help="固定字符串")
    p.add_argument("--invert-match", action="store_true", help="反向匹配")
    p.add_argument("-w", "--word-regexp", action="store_true", help="整词匹配")
    p.add_argument("-n", "--line-no", action="store_true", help="显示行号")
    p.add_argument("-c", "--count", action="store_true", help="显示匹配行数")
    p.add_argument("-l", "--files-with-matches", action="store_true", help="只显示文件名")
    p.add_argument("-L", "--files-without-match", action="store_true", help="只显示不匹配的文件")
    p.add_argument("--column", action="store_true", help="显示列号")
    p.add_argument("--extended-regexp", action="store_true", help="扩展正则")
    p.add_argument("-o", "--only-matching", action="store_true", help="只显示匹配部分")
    p.add_argument("--max-count", type=int, help="最多匹配次数")
    p.add_argument("--context", type=int, help="显示前后上下文行数")
    p.add_argument("-B", "--before-context", type=int, help="显示前导上下文")
    p.add_argument("-A", "--after-context", type=int, help="显示后续上下文")
    p.add_argument("branch", nargs="?", help="在指定分支搜索")

    # ── cherry-pick ──────────────────────────────
    p = subparsers.add_parser("cherry-pick", help="选取性应用提交")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("commit", nargs="?", help="要 cherry-pick 的提交")
    p.add_argument("--no-commit", "-n", action="store_true", help="执行但不自动提交")
    p.add_argument("--mainline", type=int, help="主提交号（用于合并提交）")
    p.add_argument("--edit", "-e", action="store_true", help="编辑提交信息")
    p.add_argument("--cleanup", choices=["default", "scissors", "whitespace", "verbatim", "none"],
                   default="default", help="清理模式")
    p.add_argument("--no-verify", action="store_true", help="跳过 pre-commit hook")
    p.add_argument("--include", nargs="+", help="包含指定提交")
    p.add_argument("--exclude", nargs="+", help="排除指定提交")
    p.add_argument("--ff", action="store_true", help="允许快进")
    p.add_argument("--force", "-f", action="store_true", help="强制继续")
    p.add_argument("-q", "--quiet", action="store_true", help="静默模式")
    p.add_argument("--continue", dest="continue_", action="store_true", help="继续 cherry-pick")
    p.add_argument("--abort", action="store_true", help="放弃并恢复")
    p.add_argument("--skip", action="store_true", help="跳过当前提交")

    # ── revert ───────────────────────────────────
    p = subparsers.add_parser("revert", help="生成反向提交（安全撤销）")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("commit", nargs="?", help="要 revert 的提交")
    p.add_argument("--no-commit", "-n", action="store_true", help="执行但不自动提交")
    p.add_argument("--edit", "-e", action="store_true", help="编辑提交信息")
    p.add_argument("--no-verify", action="store_true", help="跳过 pre-commit hook")
    p.add_argument("--cleanup", choices=["default", "scissors", "whitespace", "verbatim", "none"],
                   default="default", help="清理模式")
    p.add_argument("-q", "--quiet", action="store_true", help="静默模式")
    p.add_argument("--ff", action="store_true", help="允许快进")
    p.add_argument("--include", nargs="+", help="包含指定提交")
    p.add_argument("--exclude", nargs="+", help="排除指定提交")
    p.add_argument("--continue", dest="continue_", action="store_true", help="继续 revert")
    p.add_argument("--abort", action="store_true", help="放弃并恢复")
    p.add_argument("--skip", action="store_true", help="跳过当前提交")

    # ── bisect ───────────────────────────────────
    p = subparsers.add_parser("bisect", help="二分查找定位 bug")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("bad", nargs="?", help="已知有问题的提交（默认 HEAD）")
    p.add_argument("good", nargs="?", help="已知正常的提交")
    p.add_argument("--start", action="store_true", help="启动二分查找")
    p.add_argument("--reset", action="store_true", help="重置并退出 bisect")
    p.add_argument("--skip", action="store_true", help="跳过当前提交")
    p.add_argument("--visualize", action="store_true", help="可视化 bisect")
    p.add_argument("--log", action="store_true", help="显示 bisect 日志")
    p.add_argument("--run", action="store_true", help="自动运行 bisect")
    p.add_argument("--command", help="自动 bisect 的测试命令")
    p.add_argument("--terms", choices=["old", "new"], help="显示术语")
    p.add_argument("revision", nargs="?", help="指定版本")

    # ── lfs ─────────────────────────────────────
    p = subparsers.add_parser("lfs", help="Git LFS 操作")
    p.add_argument("repo_path", help="本地仓库路径")
    p.add_argument("--install", action="store_true", help="初始化 LFS")
    p.add_argument("--track", action="store_true", help="跟踪文件模式")
    p.add_argument("--untrack", nargs="+", help="取消跟踪模式")
    p.add_argument("--fetch", action="store_true", help="LFS Fetch")
    p.add_argument("--pull", action="store_true", help="LFS Pull")
    p.add_argument("--push", action="store_true", help="LFS Push")
    p.add_argument("--remote", help="指定远端")
    p.add_argument("--branch", help="指定分支")
    p.add_argument("--ls-files", action="store_true", help="列出 LFS 文件")
    p.add_argument("--track-list", action="store_true", help="列出跟踪模式")
    p.add_argument("--scan", action="store_true", help="扫描 LFS 对象")
    p.add_argument("patterns", nargs="*", help="文件模式（如 *.psd, *.zip）")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(0)

    # 命令分发
    dispatch = {
        "clone": cmd_clone, "pull": cmd_pull, "fetch": cmd_fetch,
        "branch": cmd_branch, "checkout": cmd_checkout,
        "merge": cmd_merge, "rebase": cmd_rebase,
        "add": cmd_add, "commit": cmd_commit, "reset": cmd_reset, "stash": cmd_stash,
        "diff": cmd_diff, "status": cmd_status, "log": cmd_log,
        "show": cmd_show, "blame": cmd_blame,
        "tag": cmd_tag, "remote": cmd_remote,
        "clean": cmd_clean, "gc": cmd_gc,
        "lfs": cmd_lfs,
        "reflog": cmd_reflog, "describe": cmd_describe,
        "worktree": cmd_worktree, "grep": cmd_grep,
        "cherry-pick": cmd_cherry_pick, "revert": cmd_revert,
        "bisect": cmd_bisect,
    }
    dispatch[args.command](args)


if __name__ == "__main__":
    main()
