#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit_project.py — 大项目「层级结构」自检（skill: project-organization）。

检查大项目根是否符合 project-organization 约定：顶层只允许规定文件/目录、
每个子项目有 README.md、必备目录齐全、.trash 存在等。

用法:
  python scripts/audit_project.py
  python scripts/audit_project.py --root /path/to/big/root
  python scripts/audit_project.py --strict        # 有 high 问题则退出码 1

stdout: {"status":"ok","root":...,"summary":{...},"issues":[...]}
"""
import argparse
import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # keep the (synced) skill dir free of __pycache__
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402


def audit(root):
    root = Path(root)
    issues = []

    def add(sev, kind, path, detail):
        issues.append({"severity": sev, "kind": kind,
                       "path": str(path), "detail": detail})

    if not C.is_big_project(root):
        add("high", "missing_marker", root / C.MARKER,
            "缺少大项目标记 %s（可能不是 project-organization 根）" % C.MARKER)
    if not (root / "README.md").is_file():
        add("high", "missing_readme", root / "README.md", "大项目根缺 README.md")

    # ★ 强制：大项目根必须配备 git（2026-10-10 起）
    if not (root / ".git").exists():
        add("high", "no_git", root / ".git",
            "大项目根未配备 git（强制要求）：跑 scripts/git_setup.py init --root \"%s\"" % root)

    # ★ OpenCode 项目记录重复（git init 晚于「首次被 OpenCode 打开」时会触发）
    #   症状：该文件夹 session 列表变空（会话其实没丢，只是挂在了另一条 project 上）。
    try:
        import oc_project_link
        warn = oc_project_link.quick_warning(root)
    except Exception:
        warn = None
    if warn:
        add("high", "oc_project_dup", root,
            "OpenCode 同目录有 %d 条 project 记录（会话未丢、但界面会显示为空）；"
            "跑 scripts/oc_project_link.py fix --hub 去重，再重启 OpenCode 服务。可删的 0 会话行: %s"
            % (warn["count"], ", ".join(warn["stale_ids"]) or "（都带会话，需人工确认）"))

    for d in (C.PROJECTS_DIR, C.SHARED_DIR, C.ARCHIVE_DIR, C.TRASH_DIR):
        if not (root / d).is_dir():
            add("medium", "missing_dir", root / d, "缺少目录 %s/" % d)
    if (root / C.ARCHIVE_DIR).is_dir() and not (root / C.ARCHIVE_DIR / "README.md").is_file():
        add("low", "missing_index", root / C.ARCHIVE_DIR / "README.md", "归档缺索引 README.md")
    if (root / C.TRASH_DIR).is_dir() and not (root / C.TRASH_DIR / "README.md").is_file():
        add("low", "missing_readme", root / C.TRASH_DIR / "README.md", ".trash 缺说明 README.md")

    # 缓冲区（人类 ⇄ AI 交换区，★ 2026-10-08 起为「扁平 + 2 天 TTL」）
    bdir = root / C.BUFFER_DIR
    if bdir.is_dir():
        if not (bdir / "README.md").is_file():
            add("low", "missing_readme", bdir / "README.md", "缓冲区缺 README.md（跑 buffer.py init）")
        items = [c for c in sorted(bdir.iterdir())
                 if not c.name.startswith(".") and c.name != "README.md"]
        if items:
            import time as _t
            expired = [c for c in items if (_t.time() - c.stat().st_mtime) > 2 * 86400]
            if expired:
                add("low", "buffer_expired", bdir,
                    "缓冲区有 %d 项超过 2 天 TTL（跑 buffer.py purge --apply 清理）" % len(expired))
            else:
                add("info", "buffer_pending", bdir,
                    "缓冲区有 %d 项未处理（交付优先放这里；超 2 天会自动清理）" % len(items))

            # ★ 一一对应：buffer 每一项都应在 projects/ shared/ archive/ 有归宿。
            #   判定 = **同名** 或 **内容一致**（同 ext+size 且 md5 相同 → 允许改名）。
            known, by_size, cap = set(), {}, 300000
            for d in (C.PROJECTS_DIR, C.SHARED_DIR, C.ARCHIVE_DIR):
                dp = root / d
                if not dp.is_dir():
                    continue
                for _a, dns, fns in os.walk(dp):
                    known.update(dns)
                    for f in fns:
                        known.add(f)
                        fp = os.path.join(_a, f)
                        try:
                            st = os.stat(fp)
                        except OSError:
                            continue
                        by_size.setdefault((os.path.splitext(f)[1].lower(), st.st_size), []).append(fp)
                    if len(known) > cap:
                        break

            import hashlib

            def _md5(p):
                h = hashlib.md5()
                with open(p, "rb") as fh:
                    for chunk in iter(lambda: fh.read(1 << 20), b""):
                        h.update(chunk)
                return h.hexdigest()

            def _has_home(it):
                inner = [it] if it.is_file() else [q for q in it.rglob("*") if q.is_file()]
                for q in inner:
                    if q.name in known:                       # 同名 → 有归宿
                        continue
                    try:                                      # 改名但内容一致 → 也算有归宿
                        st = q.stat()
                        cands = by_size.get((q.suffix.lower(), st.st_size), [])
                        if not cands or _md5(q) not in {_md5(Path(c)) for c in cands}:
                            return False
                    except OSError:
                        return False
                return True

            orphans = [c for c in items if not _has_home(c)]
            if orphans:
                add("medium", "buffer_no_counterpart", bdir,
                    "缓冲区 %d 项在 projects/shared/archive 无同名归宿（buffer 不应存唯一副本，"
                    "应先归位或清理）：%s"
                    % (len(orphans), ", ".join(c.name for c in orphans[:6])))

            # ★ 同一交付物多版本堆积（buffer 只应留最新一版）
            _VER = re.compile(r"(?i)[_\-.\s]*v(\d+(?:[.\-]\d+)*)[_\-.\s]*$")
            fam = {}
            for c in items:
                base, ext = os.path.splitext(c.name)
                m = _VER.search(base)
                key = (base[:m.start()].rstrip("_-. ") + ext) if m else c.name
                fam.setdefault(key, []).append(c.name)
            pile = {k: v for k, v in fam.items() if len(v) > 1}
            if pile:
                add("low", "buffer_version_pileup", bdir,
                    "缓冲区 %d 个交付物堆了多版本（应只留最新一版；跑 buffer.py tidy --apply）：%s"
                    % (len(pile), "; ".join("%s ← %s" % (k, ", ".join(sorted(v)))
                                            for k, v in list(pile.items())[:3])))

    # 顶层散落物（默认允许集 + 项目在 .bigproject.json 中声明的有意扩展）
    ext_files, ext_dirs = C.root_allow_extensions(root)
    allowed_files = set(C.ROOT_ALLOWED_FILES) | ext_files
    allowed_dirs = set(C.ROOT_ALLOWED_DIRS) | ext_dirs
    if root.is_dir():
        for child in sorted(root.iterdir()):
            name = child.name
            if child.is_dir():
                if name not in allowed_dirs:
                    add("medium", "stray_dir", child, "顶层出现非约定目录（应归入 projects/shared/archive）")
            else:
                if name not in allowed_files:
                    add("medium", "stray_file", child, "顶层出现非约定文件（应归入某个子项目）")

    # 每个子项目必须有 README.md
    projects = root / C.PROJECTS_DIR
    if projects.is_dir():
        for child in sorted(projects.iterdir()):
            if not child.is_dir() or child.name.startswith("."):
                continue
            if not (child / "README.md").is_file():
                add("high", "missing_readme", child / "README.md",
                    "子项目 %s 缺 README.md（无 README 视为未完成）" % child.name)
            # code-repo：含 .git 的嵌套版本库必须被父仓库忽略（否则产生「半 submodule」混乱）
            if (child / ".git").exists():
                rel = child.relative_to(root).as_posix()
                ignored = False
                try:
                    r = subprocess.run(["git", "-C", str(root), "check-ignore", "-q", rel],
                                       capture_output=True)
                    ignored = (r.returncode == 0)
                except Exception:
                    ignored = False
                if not ignored:
                    add("medium", "nested_repo_not_ignored", child,
                        "子项目 %s 是独立 git 仓（含 .git）但未被父仓库忽略；请在根 .gitignore "
                        "加 `/projects/%s/`（见 SKILL §3.1）" % (child.name, child.name))

    summary = {"total": len(issues)}
    by_sev, by_kind = {}, {}
    for it in issues:
        by_sev[it["severity"]] = by_sev.get(it["severity"], 0) + 1
        by_kind[it["kind"]] = by_kind.get(it["kind"], 0) + 1
    summary["by_severity"] = by_sev
    summary["by_kind"] = by_kind
    return summary, issues


def main():
    ap = argparse.ArgumentParser(description="大项目层级结构自检")
    ap.add_argument("--root", help="大项目根（默认从当前目录向上查找标记）")
    ap.add_argument("--strict", action="store_true", help="存在 high 问题时以非 0 退出")
    args = ap.parse_args()

    if args.root:
        root = Path(args.root).expanduser().resolve()
    else:
        root = C.find_root(Path.cwd())
        if root is None:
            C.emit({"status": "error",
                    "message": "未找到大项目根（缺 %s）；请用 --root 指定" % C.MARKER}, 1)

    summary, issues = audit(root)
    if C.is_big_project(root):
        C.journal(root, "audit.run", target=root, total=summary.get("total", 0),
                  by_severity=summary.get("by_severity", {}))
    code = 1 if (args.strict and summary.get("by_severity", {}).get("high")) else 0
    C.emit({"status": "ok", "root": str(root), "summary": summary, "issues": issues}, code)


if __name__ == "__main__":
    main()
