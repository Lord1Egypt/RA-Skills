#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""new_subproject.py — 在大项目根下新建子项目/阶段骨架（skill: project-organization）。

自动从 --root 或当前目录向上查找 .bigproject.json 定位大项目根。
生成 projects/<name>/{README.md,scripts,data,results,output}（可选 task/），
并在 projects/_index.md 追加一行索引。

type=code-repo 时（★ 2026-10-13）：
  外部代码仓子项目——`git clone` 进来的、**有独立远端**的代码仓。此时：
  - **不建** scripts/data/results/output 骨架（布局以仓库自身为准）；
  - **不覆盖**已存在的 README.md（仓库自带的 README 即子项目说明）；
  - 自动在**父仓库** .gitignore 里忽略 `/projects/<name>/`（避免嵌套版本库）；
  - 允许目录已存在（已 clone 的场景）；
  - 索引类型记为 code-repo，备注含 --repo 远端 URL。

用法:
  python scripts/new_subproject.py --name analysis
  python scripts/new_subproject.py --name data-pipeline --with-task --type stage
  python scripts/new_subproject.py --name evorag --type code-repo --repo git@host:g/evorag.git
  python scripts/new_subproject.py --name my-project --root /path/to/big/root --dry-run

stdout: {"status":"ok","root":...,"project":...,"created":[...],"dry_run":bool}
"""
import argparse
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # keep the (synced) skill dir free of __pycache__
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402


def resolve_root(explicit):
    if explicit:
        root = Path(explicit).expanduser().resolve()
        if not C.is_big_project(root):
            C.emit({"status": "error",
                    "message": "指定目录不是大项目根（缺 %s）" % C.MARKER,
                    "root": str(root)}, 1)
        return root
    root = C.find_root(Path.cwd())
    if root is None:
        C.emit({"status": "error",
                "message": "未找到大项目根（缺 %s）；请用 --root 指定或先运行 new_big_project.py"
                           % C.MARKER}, 1)
    return root


def ensure_ignored(root, rule, dry_run=False):
    """确保父仓库 .gitignore 含 `rule`（如 /projects/evorag/）。返回该规则是否新加。"""
    gi = root / ".gitignore"
    lines = gi.read_text(encoding="utf-8").splitlines() if gi.is_file() else []
    if rule in [ln.strip() for ln in lines]:
        return False
    if not dry_run:
        with open(gi, "a", encoding="utf-8", newline="\n") as f:
            if lines and lines[-1].strip():
                f.write("\n")
            f.write("# code-repo：外部版本库子项目，父仓库不追踪（见 SKILL §3.1）\n")
            f.write(rule + "\n")
    return True


def main():
    ap = argparse.ArgumentParser(description="在大项目根下新建子项目骨架")
    ap.add_argument("--name", required=True, help="子项目名（英文短横线）")
    ap.add_argument("--root", help="大项目根（默认从当前目录向上查找标记）")
    ap.add_argument("--type", default="project", choices=["project", "stage", "code-repo"],
                    help="project=独立子项目；stage=某项目的阶段；"
                         "code-repo=外部代码仓（有独立远端，不建骨架、父仓忽略）")
    ap.add_argument("--repo", default="", help="code-repo 的远端 URL（写入索引备注）")
    ap.add_argument("--with-task", action="store_true", help="额外创建 task/（任务表/任务书）")
    ap.add_argument("--description", default="", help="项目目的（写入 README）")
    ap.add_argument("--force", action="store_true", help="目录已存在且非空时复用")
    ap.add_argument("--dry-run", action="store_true", help="只预演，不落盘")
    args = ap.parse_args()

    root = resolve_root(args.root)
    slug = C.slugify(args.name)
    proj = root / C.PROJECTS_DIR / slug
    is_code = args.type == "code-repo"

    # code-repo 天然允许目录已存在（已 clone）
    if proj.exists() and any(proj.iterdir()) and not args.force and not is_code:
        C.emit({"status": "error",
                "message": "子项目目录已存在且非空，确认可复用请加 --force",
                "project": str(proj)}, 1)

    dirs = [proj]
    if not is_code:
        dirs += [proj / d for d in C.SUBPROJECT_SUBDIRS]
        if args.with_task:
            dirs.append(proj / "task")

    # README：code-repo 且已存在 → 保留仓库自带 README，不覆盖
    write_readme = (not is_code) or (not (proj / "README.md").is_file())
    readme = C.render_template(C.load_template("subproject_README.md"), {"NAME": args.name})
    if args.description:
        readme = readme.replace("<一两句话说明这个项目要做什么>", args.description)
    if is_code:
        readme += (
            "\n## 外部代码仓（code-repo）\n\n"
            + ("- 远端：`%s`\n" % args.repo if args.repo else "")
            + "- 这是**独立 git 仓**：父仓库已忽略 `projects/%s/`，代码版本由它自己的远端管理。\n" % slug
            + "- 同步/分支：一律 `git -C projects/%s …`；只推专属分支（如 `agent/*`），合并走 MR。\n" % slug
        )

    ignore_rule = "/projects/%s/" % slug
    ignore_added = False
    if is_code:
        gi = root / ".gitignore"
        lines = gi.read_text(encoding="utf-8").splitlines() if gi.is_file() else []
        ignore_added = ignore_rule not in [ln.strip() for ln in lines]

    index = root / C.PROJECTS_DIR / "_index.md"
    note = args.description or ""
    if is_code and args.repo:
        note = (note + " | " if note else "") + "远端 %s" % args.repo
    index_row = "| %s | %s | %s | active | %s |" % (slug, args.type, C.today(), note)

    if args.dry_run:
        C.emit({"status": "ok", "dry_run": True, "root": str(root),
                "project": str(proj),
                "plan": {"type": args.type,
                         "dirs": [str(d) for d in dirs],
                         "readme": str(proj / "README.md") if write_readme else "(保留现有 README)",
                         "gitignore_rule": ignore_rule if is_code else None,
                         "gitignore_add": ignore_added if is_code else False,
                         "index": str(index), "index_row": index_row},
                "created": []}, 0)

    created = []
    for d in dirs:
        if not d.exists():
            d.mkdir(parents=True, exist_ok=True)
            created.append(str(d))
    if write_readme:
        C.write_text(proj / "README.md", readme)
        created.append(str(proj / "README.md"))

    if is_code and ignore_added:
        ensure_ignored(root, ignore_rule, dry_run=False)
        created.append(str(root / ".gitignore"))

    if not index.exists():
        C.write_text(index, C.load_template("projects_index.md"))
        created.append(str(index))
    with open(index, "a", encoding="utf-8", newline="\n") as f:
        f.write(index_row + "\n")

    C.journal(root, "subproject.created", target=proj, type=args.type,
              description=args.description or "", repo=args.repo or None)
    C.log("子项目已建立: %s" % proj)
    C.emit({"status": "ok", "dry_run": False, "root": str(root),
            "project": str(proj), "created": created,
            "type": args.type, "gitignore_rule": ignore_rule if is_code else None}, 0)


if __name__ == "__main__":
    main()
