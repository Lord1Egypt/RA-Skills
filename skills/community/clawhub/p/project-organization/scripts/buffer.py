#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""buffer.py — 人类 ⇄ AI 交换缓冲区（skill: project-organization）。

**扁平设计（2026-10-08 改）**：`<大项目根>/buffer/` 下**直接放文件**，不再有 `inbox/`/`outbox/`。
它的角色是**双向**的：
  - 人 → AI：用户把文件丢进 `buffer/`，对 AI 说「读取 buffer」。
  - AI → 人：**AI 把交付物优先放进 `buffer/`**（`deliver`），交给用户。

**TTL 铁律**：**每次进入 buffer（任何子命令）先自动检查**，**超过 N 天（默认 2）的项自动清掉**
（默认软删进 `.trash/`，`--hard` 才真删；用 `--no-purge` 跳过；`--days N` 改窗口）。

子命令：
  init                  建扁平 buffer/（幂等）
  list                  列 buffer 项（进入前自动 TTL 检查）
  add   <files...>      把外部文件放进 buffer（人→AI；--move/--copy）
  deliver --file F      把产物放进 buffer（AI→人；--move/--copy）
  take  --item F ...    把 buffer 项移动到目标目录（--subproject X --subdir data --apply）
  purge [--days N] [--hard]   清掉超期项
  discard --item F ...  立即把项弃入暂存区
  tidy  [--apply]       ★ 同一交付物只留最新一版（同族旧版软删进 .trash/，保持 buffer 简洁）

根定位：--root 显式；否则从 cwd 向上找 `.bigproject.json`，再回退到含 `projects/`+`README.md` 的目录。
stdout: {"status":"ok", ...}
"""
import argparse
import os
import re
import shutil
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True  # keep the (synced) skill dir free of __pycache__
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

TTL_DAYS = 2                      # ★ 缓冲区自动清理窗口
SECONDS_PER_DAY = 86400


# ----------------------------------------------------------------- helpers ---
def resolve_root(explicit):
    if explicit:
        root = Path(explicit).expanduser().resolve()
        return root, C.is_big_project(root)
    return C.find_project_root(Path.cwd())


def require_root(explicit):
    root, is_big = resolve_root(explicit)
    if root is None:
        C.emit({"status": "error",
                "message": "未找到项目根（无 .bigproject.json，也非 projects/+README.md 结构）；"
                           "请用 --root 指定大项目根"}, 1)
    return root, is_big


def entry_info(path, root):
    p = Path(path)
    if p.is_dir():
        n = sum(1 for _ in p.rglob("*"))
        size = sum(f.stat().st_size for f in p.rglob("*") if f.is_file())
        kind = "dir"
    else:
        n, size, kind = 1, p.stat().st_size, "file"
    age = (time.time() - p.stat().st_mtime) / SECONDS_PER_DAY
    return {"name": p.name, "rel": str(p.relative_to(root)).replace("\\", "/"),
            "type": kind, "size": size, "files": n,
            "age_days": round(age, 2),
            "mtime": C.datetime.datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="seconds")}


def buffer_items(root):
    """扁平 buffer 下的项（跳过 README.md 与点开头）。"""
    bdir = C.buffer_dir(root)
    if not bdir.is_dir():
        return []
    return [c for c in sorted(bdir.iterdir())
            if not c.name.startswith(".") and c.name != "README.md"]


def resolve_dest(args, root):
    if args.dest:
        return Path(args.dest).expanduser()
    if args.subproject:
        base = Path(root) / C.PROJECTS_DIR / C.slugify(args.subproject)
        return base / args.subdir if args.subdir else base
    C.emit({"status": "error",
            "message": "需要 --dest DIR 或 --subproject NAME [--subdir SUB]"}, 2)


# --------------------------------------------------- ★ TTL 自动清理（每次进入）
def auto_purge(root, is_big, days, hard, enabled=True, dry_run=False, quiet=False):
    """清掉 mtime 超过 days 天的 buffer 项。默认软删到 .trash/（可恢复）。"""
    if not enabled:
        return []
    cutoff = time.time() - days * SECONDS_PER_DAY
    expired = []
    for c in buffer_items(root):
        try:                                   # 并发下文件可能已消失 → 跳过，不崩
            st = c.stat()
        except OSError:
            continue
        if st.st_mtime < cutoff:
            expired.append((c, round((time.time() - st.st_mtime) / SECONDS_PER_DAY, 2)))
    purged = []
    for c, age in expired:
        if dry_run:
            purged.append({"item": c.name, "age_days": age, "trashed": None})
            continue
        if hard:
            if c.is_dir():
                shutil.rmtree(c, ignore_errors=True)
            else:
                try:
                    c.unlink()
                except OSError:
                    pass
            dest = None
        else:
            dest = C.soft_remove(root, is_big, c, reason="buffer TTL 超期(%d天)" % days)
        purged.append({"item": c.name, "age_days": age,
                       "trashed": str(dest) if dest else None})
        C.project_log(root, is_big, "buffer.purge", target=c,
                      days=days, hard=hard, trashed=str(dest) if dest else None)
    if purged and not quiet:
        C.log("★ TTL 清理：%d 项超 %d 天 → %s" % (len(purged), days, "硬删" if hard else "软删进 .trash/"))
    return purged


# -------------------------------------------------------------------- init ---
def cmd_init(args):
    root, is_big = require_root(args.root)
    bdir = C.buffer_dir(root)
    readme = bdir / "README.md"
    created = []
    if not bdir.is_dir():
        bdir.mkdir(parents=True, exist_ok=True); created.append(str(bdir))
    # 迁移旧版 inbox/outbox → 扁平
    moved = []
    for legacy in ("inbox", "outbox"):
        d = bdir / legacy
        if d.is_dir():
            for c in sorted(d.iterdir()):
                if c.name.startswith("."):
                    continue
                dst = bdir / c.name
                if dst.exists():
                    stem, suf = c.stem, c.suffix
                    k = 1
                    while (bdir / ("%s.%d%s" % (stem, k, suf))).exists():
                        k += 1
                    dst = bdir / ("%s.%d%s" % (stem, k, suf))
                shutil.move(str(c), str(dst))
                moved.append({"from": "%s/%s" % (legacy, c.name), "to": dst.name})
            try:
                d.rmdir()
            except OSError:
                pass
            created.append("merged %s/ -> buffer/ (flat)" % legacy)
    if not readme.is_file() or args.force:
        content = C.render_template(C.load_template("buffer_README.md"),
                                    {"NAME": root.name, "DATE": C.today(), "TTL": TTL_DAYS})
        C.write_text(readme, content); created.append(str(readme))
    C.emit({"status": "ok", "root": str(root), "buffer": str(bdir),
            "is_big_project": is_big, "created": created, "migrated": moved,
            "ttl_days": TTL_DAYS})


# -------------------------------------------------------------------- list ---
def cmd_list(args):
    root, is_big = require_root(args.root)
    purged = auto_purge(root, is_big, args.days, args.hard, enabled=not args.no_purge)
    items = [entry_info(c, root) for c in buffer_items(root)]
    expiring = [i for i in items if i["age_days"] >= args.days - 0.5]
    C.emit({"status": "ok", "root": str(root), "is_big_project": is_big,
            "buffer": str(C.buffer_dir(root)), "ttl_days": args.days,
            "items": items, "count": len(items),
            "purged": purged, "expiring_soon": expiring})


# ------------------------------------------------------- move primitive -----
def do_move(src, dst, root, is_big, overwrite, reason, dry_run):
    dst = Path(dst)
    existed = dst.exists()
    if existed:
        if not overwrite:
            raise RuntimeError("目标已存在: %s（如需覆盖加 --overwrite）" % dst)
        if not dry_run:
            C.soft_remove(root, is_big, dst, reason="buffer 覆盖: %s" % reason)
    if not dry_run:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(src), str(dst))
    return {"from": str(src), "to": str(dst), "overwrote": existed}


# -------------------------------------------------------------------- take ---
def cmd_take(args):
    root, is_big = require_root(args.root)
    purged = auto_purge(root, is_big, args.days, args.hard, enabled=not args.no_purge)
    bdir = C.buffer_dir(root)
    if not bdir.is_dir():
        C.emit({"status": "error", "message": "无 buffer/，先跑 buffer.py init"}, 1)
    items = args.item or [c.name for c in buffer_items(root)]
    if not items:
        C.emit({"status": "ok", "root": str(root), "moves": [], "purged": purged,
                "message": "buffer 为空，无需处理"})
        return
    dest = Path(resolve_dest(args, root))
    dry_run = not args.apply
    if not dest.exists() and not args.mkdir and not dry_run:
        C.emit({"status": "error",
                "message": "目标目录不存在: %s（确认后加 --mkdir 或先新建子项目）" % dest}, 1)
    moves = []
    for name in items:
        src = bdir / name
        if not src.exists():
            C.emit({"status": "error", "message": "buffer 中不存在: %s" % name}, 1)
        moves.append(do_move(src, dest / name, root, is_big,
                             args.overwrite, args.reason, dry_run))
    if not dry_run:
        C.project_log(root, is_big, "buffer.take", target=dest,
                      items=[Path(m["from"]).name for m in moves],
                      dest=str(dest), reason=args.reason)
    C.emit({"status": "ok", "root": str(root), "dry_run": dry_run,
            "dest": str(dest), "moves": moves, "purged": purged})


# --------------------------------------------------------- deliver / add -----
# ------------------------------------------- 版本归并（tidy / supersede）---
VER_RE = re.compile(r"(?i)[_\-.\s]*v(\d+(?:[.\-]\d+)*)[_\-.\s]*$")
FINAL_RE = re.compile(r"(?i)[_\-.\s]*(final|latest|new|终版|定稿)[_\-.\s]*$")


def split_ver(name):
    """名字 → (family, ver)。family =「去掉版本号的名字+扩展名」，ver 供比较新旧。"""
    base, ext = os.path.splitext(name)
    m = VER_RE.search(base)
    if m:
        ver = tuple(int(x) for x in re.split(r"[.\-]", m.group(1)))
        return base[:m.start()].rstrip("_-. ") + ext, ver
    m2 = FINAL_RE.search(base)
    if m2:
        return base[:m2.start()].rstrip("_-. ") + ext, (9999,)
    return base + ext, (0,)


def version_families(bdir):
    """buffer 里「同一交付物多版本」的家族（只返回 >1 件的族）。"""
    fam = {}
    for p in sorted(Path(bdir).iterdir()):
        if p.name in (".replaced", "README.md") or p.name.startswith("."):
            continue
        k, v = split_ver(p.name)
        fam.setdefault(k, []).append((v, p.name))
    return {k: sorted(v) for k, v in fam.items() if len(v) > 1}


def _supersede(root, is_big, keep_name, bdir, dry_run):
    """把与 keep_name 同族、但当次之外的旧版**软删进 .trash**（★ 保持 buffer 简洁）。"""
    out = []
    for _k, lst in version_families(bdir).items():
        names = [n for _, n in lst]
        if keep_name not in names:
            continue
        for _v, n in lst:
            if n == keep_name:
                continue
            dest = None
            if not dry_run:
                dest = C.soft_remove(root, is_big, Path(bdir) / n,
                                     reason="buffer supersede: 被 %s 取代" % keep_name)
                C.project_log(root, is_big, "buffer.supersede", target=n,
                              superseded_by=keep_name, trashed=str(dest))
            out.append({"item": n, "superseded_by": keep_name,
                        "trashed": str(dest) if dest else None})
    return out


def _put(args, root, is_big, dst_name=None):
    src = Path(args.file).expanduser()
    if not src.exists():
        C.emit({"status": "error", "message": "文件不存在: %s" % src}, 1)
    bdir = C.buffer_dir(root)
    bdir.mkdir(parents=True, exist_ok=True)
    dst = bdir / (dst_name or src.name)
    dry_run = not args.apply
    if dst.exists():
        if not args.overwrite:
            C.emit({"status": "error",
                    "message": "buffer 已存在同名: %s（加 --overwrite 覆盖）" % dst}, 1)
        if not dry_run:
            C.soft_remove(root, is_big, dst, reason="buffer 覆盖")
    if not dry_run:
        if args.move:
            shutil.move(str(src), str(dst))
        else:
            shutil.copy2(str(src), str(dst))
    return {"from": str(src), "to": str(dst), "mode": "move" if args.move else "copy"}


def cmd_deliver(args):
    """AI → 人：把交付物放进 buffer/（★ 交付优先放这里）。"""
    root, is_big = require_root(args.root)
    purged = auto_purge(root, is_big, args.days, args.hard, enabled=not args.no_purge)
    r = _put(args, root, is_big, args.name)
    if args.apply:
        C.project_log(root, is_big, "buffer.deliver", target=r["to"],
                      src=r["from"], mode=r["mode"])
    superseded = []
    if not getattr(args, "no_supersede", False):
        # ★ 同一交付物只留最新一版：把同族旧版一并软删进 .trash（保持 buffer 简洁）
        superseded = _supersede(root, is_big, Path(r["to"]).name,
                                C.buffer_dir(root), not args.apply)
    C.emit({"status": "ok", "root": str(root), "dry_run": not args.apply,
            "to": r["to"], "mode": r["mode"], "purged": purged,
            "superseded": superseded})


def cmd_add(args):
    """人 → AI：把外部文件放进 buffer/。"""
    root, is_big = require_root(args.root)
    purged = auto_purge(root, is_big, args.days, args.hard, enabled=not args.no_purge)
    moves = []
    for f in args.file:
        ns = argparse.Namespace(file=f, apply=args.apply, move=args.move,
                                overwrite=args.overwrite)
        moves.append(_put(ns, root, is_big))
    if args.apply:
        C.project_log(root, is_big, "buffer.add",
                      files=[Path(m["from"]).name for m in moves],
                      mode="move" if args.move else "copy")
    C.emit({"status": "ok", "root": str(root), "dry_run": not args.apply,
            "moves": moves, "purged": purged})


# -------------------------------------------------------- purge / discard ---
def cmd_purge(args):
    root, is_big = require_root(args.root)
    purged = auto_purge(root, is_big, args.days, args.hard,
                        enabled=True, dry_run=not args.apply)
    C.emit({"status": "ok", "root": str(root), "dry_run": not args.apply,
            "days": args.days, "hard": args.hard,
            "purged": purged, "count": len(purged)})


def cmd_discard(args):
    root, is_big = require_root(args.root)
    bdir = C.buffer_dir(root)
    dry_run = not args.apply
    discarded = []
    for name in args.item:
        src = bdir / name
        if not src.exists():
            C.emit({"status": "error", "message": "buffer 中不存在: %s" % name}, 1)
        dest = None
        if not dry_run:
            dest = C.soft_remove(root, is_big, src, reason=args.reason or "buffer discard")
            C.project_log(root, is_big, "buffer.discard", target=src, trashed=str(dest))
        discarded.append({"item": name, "trashed": str(dest) if dest else None})
    C.emit({"status": "ok", "root": str(root), "dry_run": dry_run, "discarded": discarded})


# -------------------------------------------------------------------- tidy ---
def cmd_tidy(args):
    """★ 同一交付物只留最新一版：同族旧版一并软删进 .trash（保持 buffer 简洁）。"""
    root, is_big = require_root(args.root)
    purged = auto_purge(root, is_big, args.days, args.hard, enabled=not args.no_purge)
    bdir = C.buffer_dir(root)
    dry_run = not args.apply
    plan, done = [], []
    for _k, lst in version_families(bdir).items():
        keep = lst[-1][1]                     # 版本号最大者留下
        for _v, n in lst[:-1]:
            rec = {"item": n, "superseded_by": keep}
            plan.append(rec)
            if not dry_run:
                dest = C.soft_remove(root, is_big, bdir / n,
                                     reason="buffer tidy: 被 %s 取代" % keep)
                C.project_log(root, is_big, "buffer.tidy", target=n,
                              superseded_by=keep, trashed=str(dest))
                done.append({**rec, "trashed": str(dest)})
    C.emit({"status": "ok", "root": str(root), "dry_run": dry_run,
            "purged": purged, "would_supersede": plan,
            "superseded": done, "count": len(plan)})


# -------------------------------------------------------------------- main ---
def _ttl_opts(p, default_days=TTL_DAYS):
    p.add_argument("--days", type=int, default=default_days,
                   help="TTL 天数（默认 %d）" % default_days)
    p.add_argument("--hard", action="store_true", help="真删（默认软删进 .trash/）")
    p.add_argument("--no-purge", action="store_true", help="本次不做 TTL 检查")


def main():
    ap = argparse.ArgumentParser(description="人类 ⇄ AI 交换缓冲区（扁平 + %d 天 TTL）" % TTL_DAYS)
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init", help="建扁平 buffer/（幂等；自动合并旧版 inbox/outbox）")
    p.add_argument("--root"); p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("list", help="列 buffer 项（进入前自动 TTL 检查）")
    p.add_argument("--root"); _ttl_opts(p)
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("take", help="把 buffer 项移动到目标目录")
    p.add_argument("--root")
    p.add_argument("--item", action="append", help="buffer 中的名字（可重复；默认全部）")
    p.add_argument("--dest", help="目标目录（绝对或相对）")
    p.add_argument("--subproject", help="目标子项目名（→ projects/<名>/）")
    p.add_argument("--subdir", help="子项目内子目录（如 data/scripts/output/results）")
    p.add_argument("--mkdir", action="store_true", help="目标目录不存在时创建")
    p.add_argument("--overwrite", action="store_true", help="覆盖同名（旧物入暂存）")
    p.add_argument("--reason", default="buffer take")
    p.add_argument("--apply", action="store_true", help="真正执行（默认只预演）")
    _ttl_opts(p)
    p.set_defaults(func=cmd_take)

    p = sub.add_parser("deliver", help="★ AI 把交付物放进 buffer/（交付优先放这里）")
    p.add_argument("--root"); p.add_argument("--file", required=True)
    p.add_argument("--name"); p.add_argument("--move", action="store_true")
    p.add_argument("--overwrite", action="store_true")
    p.add_argument("--no-supersede", action="store_true",
                   help="不把同族旧版移入暂存（默认会——保持 buffer 只留最新一版）")
    p.add_argument("--apply", action="store_true")
    _ttl_opts(p)
    p.set_defaults(func=cmd_deliver)

    p = sub.add_parser("add", help="把外部文件放进 buffer/（人→AI）")
    p.add_argument("--root"); p.add_argument("--file", nargs="+", required=True)
    p.add_argument("--move", action="store_true"); p.add_argument("--overwrite", action="store_true")
    p.add_argument("--apply", action="store_true")
    _ttl_opts(p)
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("purge", help="清掉超期项（默认软删进 .trash/）")
    p.add_argument("--root"); _ttl_opts(p)
    p.add_argument("--apply", action="store_true", help="真正执行（默认只预演）")
    p.set_defaults(func=cmd_purge)

    p = sub.add_parser("discard", help="把 buffer 项立即弃入暂存区")
    p.add_argument("--root"); p.add_argument("--item", nargs="+", required=True)
    p.add_argument("--reason"); p.add_argument("--apply", action="store_true")
    p.set_defaults(func=cmd_discard)

    p = sub.add_parser("tidy", help="★ 同一交付物只留最新一版（旧版软删进 .trash/）")
    p.add_argument("--root"); p.add_argument("--apply", action="store_true",
                                             help="真正执行（默认只预演）")
    _ttl_opts(p)
    p.set_defaults(func=cmd_tidy)

    args = ap.parse_args()
    try:
        args.func(args)
    except RuntimeError as e:
        C.emit({"status": "error", "message": str(e)}, 1)


if __name__ == "__main__":
    main()
