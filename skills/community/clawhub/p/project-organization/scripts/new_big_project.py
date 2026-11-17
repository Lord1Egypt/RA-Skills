#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""new_big_project.py — 建立「大项目根」骨架（skill: project-organization）。

按 AGENTS.md「本地项目目录规范」把 --kind 映射到 base 根（全部走环境变量），
或由 --root / --path 显式指定。生成 projects/ shared/ archive/ .tools/ .trash/
与顶层 README、各索引，并写下 .bigproject.json 标记。

用法:
  python scripts/new_big_project.py --name "my-research" --kind thu
  python scripts/new_big_project.py --name myproj --root /some/base
  python scripts/new_big_project.py --name myproj --path /exact/big/root --dry-run

stdout: {"status":"ok","root":...,"created":[...],"dry_run":bool}
"""
import argparse
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # keep the (synced) skill dir free of __pycache__
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402


def build_plan(root, name):
    root = Path(root)
    dirs = [root, root / C.PROJECTS_DIR, root / C.SHARED_DIR]
    dirs += [root / C.SHARED_DIR / d for d in C.SHARED_SUBDIRS]
    dirs += [root / C.ARCHIVE_DIR, root / C.TOOLS_DIR, root / C.TRASH_DIR]
    dirs += [root / C.BUFFER_DIR]        # buffer 扁平（无 inbox/outbox）

    ctx = {"NAME": name, "DATE": C.today()}
    files = {
        root / "README.md": C.render_template(C.load_template("root_README.md"), ctx),
        root / C.PROJECTS_DIR / "_index.md": C.load_template("projects_index.md"),
        root / C.ARCHIVE_DIR / "README.md": C.load_template("archive_index.md"),
        root / C.TRASH_DIR / "README.md": C.load_template("trash_README.md"),
        root / C.BUFFER_DIR / "README.md":
            C.render_template(C.load_template("buffer_README.md"), ctx),
    }
    return dirs, files


def main():
    ap = argparse.ArgumentParser(description="建立 project-organization 大项目根骨架")
    ap.add_argument("--name", required=True, help="大项目名（用于目录名与 README）")
    ap.add_argument("--kind", default="custom",
                    choices=["thu", "tencent", "shared", "scratch", "custom"],
                    help="按 AGENTS 项目目录规范解析 base 根（custom 时须给 --root）")
    ap.add_argument("--root", help="base 根目录（在其下建 <name>/）")
    ap.add_argument("--path", help="直接指定大项目根的完整路径（优先于 --kind/--root）")
    ap.add_argument("--force", action="store_true", help="目录已存在且非空时复用")
    ap.add_argument("--dry-run", action="store_true", help="只预演，不落盘")
    args = ap.parse_args()

    if args.path:
        root = Path(args.path).expanduser()
    else:
        base = C.resolve_base_root(args.kind, explicit=args.root)
        if base is None:
            C.emit({"status": "error",
                    "message": "无法解析 base 根：kind=%s 且未提供 --root/--path" % args.kind}, 2)
        root = Path(base) / C.slugify(args.name)
    root = root.resolve()

    if C.is_big_project(root):
        C.emit({"status": "error", "message": "该目录已是大项目根（含 %s）" % C.MARKER,
                "root": str(root)}, 1)
    if root.exists() and any(root.iterdir()) and not args.force:
        C.emit({"status": "error",
                "message": "目录已存在且非空，确认可复用请加 --force",
                "root": str(root)}, 1)

    dirs, files = build_plan(root, args.name)
    if args.dry_run:
        C.emit({"status": "ok", "dry_run": True, "root": str(root),
                "plan": {"dirs": [str(d) for d in dirs],
                         "files": [str(f) for f in files],
                         "git": "git init + .gitignore + 首次提交"},
                "created": []}, 0)

    created = []
    for d in dirs:
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            created.append(str(d))
    for f, content in files.items():
        if (not f.exists()) or args.force:
            C.write_text(f, content)
            created.append(str(f))
    C.write_json(root / C.MARKER,
                 {"name": args.name, "kind": args.kind, "created": C.now_iso(), "version": 1})
    created.append(str(root / C.MARKER))
    C.journal(root, "root.created", target=root, name=args.name, kind=args.kind)

    # ★ 强制：大项目根必须配备 git（见 SKILL.md「版本控制（git，强制）」）
    git_res = {"status": "skipped"}
    try:
        import git_setup
        git_res = git_setup.ensure_git(root, message="chore: 初始化项目（project-organization）")
        if git_res.get("status") == "ok":
            created.append(str(root / ".git"))
    except Exception as e:  # git 不可用不阻断目录建立（由 audit 报 no_git）
        git_res = {"status": "error", "message": str(e)}

    C.log("大项目根已建立: %s" % root)
    C.emit({"status": "ok", "dry_run": False, "root": str(root),
            "marker": str(root / C.MARKER), "created": created, "git": git_res}, 0)


if __name__ == "__main__":
    main()
