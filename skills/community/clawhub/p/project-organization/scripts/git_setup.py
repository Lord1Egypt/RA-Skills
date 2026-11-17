#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""git_setup.py — 大项目「版本控制（git）」必备件（skill: project-organization）。

★ 强制规则（2026-10-10 起）：所有 project-organization 大项目根都必须配备 git。
   理由：本项目曾因「手动改动被覆盖 + 无版本控制 + Syncthing 版本功能关闭」而**不可逆丢失**。
   纪律：**每次改动项目文件之前先 commit**；之后任何一步都能 `git diff` / `git checkout` 找回。

子命令:
  init    [--root R] [--message M] [--force]
          在项目根 `git init` + 写 .gitignore（缺失时）+ 首次提交；幂等。
  commit  [--root R] -m MESSAGE
          `git add -A` 并提交（改前/改后打点）。无改动时返回 nothing_to_commit。
  status  [--root R]
          报告是否已 git 化 / 分支 / 是否脏 / HEAD。
  log     [--root R] [-n N]
          最近 N 条提交（默认 10）。
  tag     [--root R] NAME [-m MESSAGE]
          给当前 HEAD 打标签（版本 / 确认 / 冻结打点）。
  snapshot [--root R] -m MESSAGE [--tag NAME]
          ★「覆盖 / 重跑 / 批量替换前」的安全绳：commit（可再 tag）。
          任何会盖掉用户改动的操作之前，先跑它。

stdout: JSON {"status": "ok"|"error", ...}
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # keep the (synced) skill dir free of __pycache__
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

GITIGNORE_FALLBACK = (
    "# —— project-organization 默认忽略（可自行增补）——\n"
    "__pycache__/\n*.pyc\n.DS_Store\nThumbs.db\ndesktop.ini\n"
    ".trash/\n"
    "# 大体积产物（按需开启；开启后不进版本库）\n"
    "# *.pptx\n# *.zip\n# *.mp4\n"
)


def _git(root, *args, timeout=120):
    return subprocess.run(["git", *args], cwd=str(root), capture_output=True,
                          text=True, encoding="utf-8", errors="replace", timeout=timeout)


def git_available():
    try:
        r = subprocess.run(["git", "--version"], capture_output=True, text=True, timeout=20)
        return r.returncode == 0, (r.stdout or r.stderr or "").strip()
    except Exception as e:  # noqa: BLE001
        return False, str(e)


def is_repo(root):
    return (Path(root) / ".git").exists()


def _ensure_identity(root):
    if not (_git(root, "config", "user.email").stdout or "").strip():
        _git(root, "config", "user.email", "opencode@local")
        _git(root, "config", "user.name",
             os.environ.get("OPENCODE_ACTOR") or os.environ.get("USERNAME") or "opencode")


def _write_gitignore(root, force=False):
    """写 .gitignore（已存在且非 force 时不动）。返回是否写入。"""
    p = Path(root) / ".gitignore"
    if p.exists() and not force:
        return False
    C.write_text(p, (C.load_template("gitignore.txt") or GITIGNORE_FALLBACK))
    return True


def ensure_git(root, message="chore: 首次提交（project-organization）", force=False):
    """确保 root 是 git 仓库并做首次提交。返回结果 dict（供 new_big_project.py 复用）。"""
    root = Path(root)
    ok, ver = git_available()
    if not ok:
        return {"status": "error", "message": "未找到 git：%s" % ver, "root": str(root)}
    created = False
    if not is_repo(root):
        r = _git(root, "init")
        if r.returncode != 0:
            return {"status": "error", "message": (r.stderr or r.stdout).strip(), "root": str(root)}
        created = True
    gi = _write_gitignore(root, force=force)
    _ensure_identity(root)
    _git(root, "add", "-A")
    r = _git(root, "commit", "-m", message)
    committed = (r.returncode == 0)
    head = _git(root, "rev-parse", "--short", "HEAD").stdout.strip() if committed else None
    C.journal(root, "git.init", target=root, created=created, committed=committed,
              gitignore=gi, head=head)
    out = {"status": "ok", "root": str(root), "git": ver, "created": created,
           "gitignore_written": gi, "committed": committed, "head": head,
           "commit_msg": message}
    # ★ 事后自检：若该目录在 git init **之前**已被 OpenCode 认成项目，会出现「同目录两条
    #   project」记录，导致该文件夹 session 列表变空。这里**只告警、不自动改库**。
    try:
        import oc_project_link
        warn = oc_project_link.quick_warning(root)
        if warn:
            out["oc_project_warning"] = warn
    except Exception:
        pass
    return out


def do_commit(root, message):
    root = Path(root)
    if not is_repo(root):
        return {"status": "error", "root": str(root),
                "message": "不是 git 仓库（先跑 git_setup.py init）"}
    _ensure_identity(root)
    _git(root, "add", "-A")
    r = _git(root, "commit", "-m", message)
    out = ((r.stdout or "") + (r.stderr or "")).strip()
    if r.returncode != 0 and ("nothing to commit" in out or "无文件要提交" in out
                              or "nothing added to commit" in out):
        C.journal(root, "git.commit", target=root, message=message, result="nothing")
        return {"status": "ok", "root": str(root), "result": "nothing_to_commit",
                "message": message}
    if r.returncode != 0:
        return {"status": "error", "root": str(root), "message": out}
    head = _git(root, "rev-parse", "--short", "HEAD").stdout.strip()
    C.journal(root, "git.commit", target=root, message=message, head=head)
    return {"status": "ok", "root": str(root), "result": "committed", "head": head,
            "message": message}


def do_status(root):
    root = Path(root)
    if not is_repo(root):
        return {"status": "ok", "root": str(root), "is_repo": False}
    branch = _git(root, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    head = _git(root, "rev-parse", "--short", "HEAD").stdout.strip()
    p = _git(root, "status", "--porcelain").stdout
    dirty = [l for l in p.splitlines() if l.strip()]
    return {"status": "ok", "root": str(root), "is_repo": True, "branch": branch,
            "head": head, "dirty": len(dirty), "dirty_sample": dirty[:20]}


def do_tag(root, name, message=None):
    root = Path(root)
    if not is_repo(root):
        return {"status": "error", "root": str(root), "message": "不是 git 仓库（先跑 git_setup.py init）"}
    r = _git(root, "tag", "-a", name, "-m", message) if message else _git(root, "tag", name)
    if r.returncode != 0:
        return {"status": "error", "root": str(root), "message": (r.stderr or r.stdout).strip()}
    C.journal(root, "git.tag", target=root, tag=name)
    return {"status": "ok", "root": str(root), "tag": name}


def do_snapshot(root, message, tag=None):
    """★ 覆盖 / 重跑 / 批量替换前的安全绳：commit（+ 可选 tag）。"""
    res = do_commit(root, message)
    if res.get("status") != "ok":
        return res
    out = {"status": "ok", "root": str(res.get("root")), "result": res.get("result"),
           "head": res.get("head"), "message": message}
    if tag:
        t = do_tag(root, tag, message)
        if t.get("status") == "ok":
            out["tag"] = tag
        else:
            out["tag_error"] = t.get("message")
    return out


def do_log(root, n):
    root = Path(root)
    if not is_repo(root):
        return {"status": "ok", "root": str(root), "is_repo": False, "commits": []}
    r = _git(root, "log", "--oneline", "-n", str(n))
    lines = [l for l in (r.stdout or "").splitlines() if l.strip()]
    return {"status": "ok", "root": str(root), "count": len(lines), "commits": lines}


def _resolve_root(args):
    if getattr(args, "root", None):
        return Path(args.root).expanduser().resolve()
    r = C.find_root(Path.cwd())
    if r is None:
        C.emit({"status": "error",
                "message": "未找到大项目根（缺 %s）；请用 --root 指定" % C.MARKER}, 1)
    return r


def main():
    ap = argparse.ArgumentParser(description="大项目 git 版本控制（project-organization）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init", help="git init + .gitignore + 首次提交（幂等）")
    p.add_argument("--root")
    p.add_argument("--message", default="chore: 首次提交（project-organization）")
    p.add_argument("--force", action="store_true", help="覆盖已存在的 .gitignore")
    p = sub.add_parser("commit", help="提交当前改动（改前/改后打点）")
    p.add_argument("--root")
    p.add_argument("-m", "--message", required=True)
    p = sub.add_parser("status", help="报告 git 状态")
    p.add_argument("--root")
    p = sub.add_parser("log", help="最近提交")
    p.add_argument("--root")
    p.add_argument("-n", type=int, default=10)
    p = sub.add_parser("tag", help="给当前 HEAD 打标签（版本/确认/冻结打点）")
    p.add_argument("--root")
    p.add_argument("name")
    p.add_argument("-m", "--message", default=None)
    p = sub.add_parser("snapshot", help="覆盖/重跑前安全绳：commit（+ 可选 tag）")
    p.add_argument("--root")
    p.add_argument("-m", "--message", required=True)
    p.add_argument("--tag", default=None)
    args = ap.parse_args()

    root = _resolve_root(args)
    if args.cmd == "init":
        res = ensure_git(root, args.message, args.force)
    elif args.cmd == "commit":
        res = do_commit(root, args.message)
    elif args.cmd == "status":
        res = do_status(root)
    elif args.cmd == "tag":
        res = do_tag(root, args.name, args.message)
    elif args.cmd == "snapshot":
        res = do_snapshot(root, args.message, args.tag)
    else:
        res = do_log(root, args.n)
    C.emit(res, 0 if res.get("status") == "ok" else 1)


if __name__ == "__main__":
    main()
