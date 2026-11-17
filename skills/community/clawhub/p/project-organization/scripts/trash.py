#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""trash.py — 大项目根内的软删除暂存（**压缩 · 可精确还原**）（skill: project-organization）。

"删除"一律把目标**压缩**进 `<大项目根>/.trash/<时间戳>__<名>.tar.<algo>`（默认 **zstd**，
`gb`/`xz` 可选）；包内含 `_manifest.json`（路径一律 **相对大项目根** → 跨机可精确还原），
并登记到 `.trash/_index.json`。可随时 `restore`；唯有 `purge` 才真正删除（须 `--confirm`）。

子命令:
  put       压缩入暂存（默认预演；--apply 执行；--algo zst|gz|xz|bz2）
  list      列出条目（读 `_index.json` + 兼容旧「目录式」条目）
  restore   还原（--id；默认预演；--apply 执行；--force 覆盖）
  purge     彻底删除（--id | --all | --older-than N；须 --confirm）
  compress  把旧「目录式」条目补压成压缩包（一次性迁移）
  status    统计（条目数 / 压缩后 / 原始 / 压缩比）

用法:
  python scripts/trash.py put 旧目录 --reason "迁移" --apply
  python scripts/trash.py put 旧目录 --reason "迁移" --algo xz --apply
  python scripts/trash.py list
  python scripts/trash.py restore --id 20261016-101500__旧目录 --apply
  python scripts/trash.py purge --older-than 30 --confirm
  python scripts/trash.py compress --apply

stdout: {"status":"ok",...}（每条命令一份 JSON）
"""
import argparse
import datetime
import json
import os
import shutil
import sys
import tarfile
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True  # keep the (synced) skill dir free of __pycache__
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

ARCHIVE_EXTS = tuple(C.TRASH_ALGO_EXT.values())


# ------------------------------------------------------------------ helpers ---
def resolve_root(explicit, target=None):
    if explicit:
        root = Path(explicit).expanduser().resolve()
        if not C.is_big_project(root):
            C.emit({"status": "error",
                    "message": "指定目录不是大项目根（缺 %s）" % C.MARKER, "root": str(root)}, 1)
        return root
    start = target or Path.cwd()
    root = C.find_root(start)
    if root is None:
        C.emit({"status": "error",
                "message": "未找到大项目根（缺 %s）；请用 --root 指定" % C.MARKER}, 1)
    return root


def trash_dir(root):
    return Path(root) / C.TRASH_DIR


def _rel(root, path):
    return C.rel_to_root(root, path)


def _safe_target(root, rel):
    """把相对路径解回 root 下的绝对路径（防路径穿越）。rel 为空或越界 → None。"""
    if not rel:
        return None
    root = Path(root).resolve()
    target = (root / rel).resolve()
    if target == root or root not in target.parents:
        return None
    return target


def _is_archive(p):
    return p.is_file() and p.name.endswith(ARCHIVE_EXTS)


def iter_entries(trash, root):
    """统一列出条目：压缩包（读 _index.json）+ 旧「目录式」。"""
    out = []
    idx = C.trash_index_load(trash)
    for eid, meta in idx.items():
        f = trash / meta.get("file", "")
        if not f.is_file():
            cand = [p for p in trash.glob(eid + ".tar.*") if p.is_file()]
            f = cand[0] if cand else None
        if f is None:
            continue
        try:
            packed = f.stat().st_size
        except OSError:
            packed = None
        out.append({"id": eid, "kind": "archive", "file": f.name,
                    "time": meta.get("time", ""), "reason": meta.get("reason", ""),
                    "algo": meta.get("algo", ""), "items": meta.get("items", []),
                    "orig_bytes": meta.get("orig_bytes"), "packed_bytes": packed})
    if trash.is_dir():
        known_files = {m.get("file") for m in idx.values()}
        for p in sorted(trash.iterdir()):
            if p.is_file() and _is_archive(p) and p.name not in known_files:
                # ★ 孤儿包：在 .trash 但不在 _index.json（如索引写入前中断）→ 也要能被 see/manage
                eid = next((p.name[: -len(e)] for e in ARCHIVE_EXTS if p.name.endswith(e)), p.name)
                try:
                    mt = datetime.datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="seconds")
                    sz = p.stat().st_size
                except OSError:
                    mt, sz = "", None
                out.append({"id": eid, "kind": "archive", "file": p.name, "time": mt,
                            "reason": "(孤儿包：不在索引)", "algo": p.name.rsplit(".", 1)[-1],
                            "items": [], "has_manifest": False, "orphan": True,
                            "orig_bytes": None, "packed_bytes": sz})
                continue
            if p.is_dir() and p.name != C.TRASH_DIR:
                m = C.read_json(p / C.TRASH_MANIFEST, default={}) or {}
                items = [{"name": i.get("name"), "orig_rel": _rel(root, i.get("from"))}
                         for i in m.get("items", [])]
                out.append({"id": p.name, "kind": "dir", "file": None,
                            "time": m.get("time", ""), "reason": m.get("reason", ""),
                            "algo": None, "items": items, "has_manifest": bool(m.get("items")),
                            "orig_bytes": C._tree_bytes(p), "packed_bytes": None})
            elif (p.is_file() and p.name not in (C.TRASH_INDEX, "README.md")
                  and not _is_archive(p)):
                # 旧格式遗留：散落在 .trash/ 根的直接文件（无原路径信息）
                try:
                    mt = datetime.datetime.fromtimestamp(p.stat().st_mtime).isoformat(timespec="seconds")
                    sz = p.stat().st_size
                except OSError:
                    mt, sz = "", None
                out.append({"id": p.name, "kind": "loose", "file": p.name, "time": mt,
                            "reason": "(旧格式散落文件，无原路径)", "algo": None, "items": [],
                            "has_manifest": False, "orig_bytes": sz, "packed_bytes": None})
    return out


def find_entry(trash, root, eid):
    for e in iter_entries(trash, root):
        if e["id"] == eid:
            return e
    return None


# ---------------------------------------------------------------------- put ---
def cmd_put(args):
    targets = [Path(t).expanduser() for t in args.paths]
    for t in targets:
        if not t.exists():
            C.emit({"status": "error", "message": "路径不存在: %s" % t}, 1)
    root = resolve_root(args.root, target=targets[0])
    trash = trash_dir(root)
    for t in targets:
        src = t.resolve()
        if src == root:
            C.emit({"status": "error", "message": "拒绝移动大项目根本身", "path": str(src)}, 1)
        if trash == src or trash in src.parents:
            C.emit({"status": "error", "message": "路径已在 .trash 内", "path": str(src)}, 1)
    plan = [{"from": str(t.resolve()), "name": t.name, "bytes": C._tree_bytes(t)} for t in targets]
    if not args.apply:
        C.emit({"status": "ok", "dry_run": True, "root": str(root), "algo": args.algo,
                "reason": args.reason, "items": plan}, 0)
    try:
        arc, man = C.trash_entry(trash, root, [Path(p["from"]) for p in plan],
                                 reason=args.reason or "", algo=args.algo)
    except Exception as e:
        C.emit({"status": "error", "message": "压缩入暂存失败: %s" % e, "items": plan}, 1)
    C.journal(root, "trash.put", target=arc.name, reason=args.reason or "",
              algo=args.algo, items=[i["name"] for i in man["items"]])
    C.log("已压缩入暂存: %s" % arc)
    C.emit({"status": "ok", "dry_run": False, "root": str(root), "entry": arc.name,
            "id": man["id"], "algo": man["algo"], "reason": args.reason or "",
            "packed_bytes": arc.stat().st_size,
            "orig_bytes": sum(p["bytes"] for p in plan),
            "items": [{"name": i["name"], "orig_rel": i["orig_rel"]} for i in man["items"]]}, 0)


# --------------------------------------------------------------------- list ---
def cmd_list(args):
    start = Path(args.root).expanduser() if args.root else Path.cwd()
    root = C.find_root(start)
    if root is None:
        C.emit({"status": "error",
                "message": "未找到大项目根（缺 %s）；请用 --root 指定" % C.MARKER}, 1)
    trash = trash_dir(root)
    entries = iter_entries(trash, root)
    C.emit({"status": "ok", "root": str(root), "count": len(entries), "entries": entries}, 0)


# ------------------------------------------------------------------ restore ---
def _restore_archive(entry, root, force):
    trash = trash_dir(root)
    f = trash / entry["file"]
    algo = entry.get("algo") or f.name.rsplit(".", 1)[-1]
    restored = []
    with tarfile.open(f, "r:" + algo) as t:
        mf = t.extractfile(C.TRASH_MANIFEST) if C.TRASH_MANIFEST in t.getnames() else None
        man = json.loads(mf.read().decode("utf-8")) if mf else {"items": entry["items"]}
        for item in man.get("items", []):
            name = item.get("name")
            target = _safe_target(root, item.get("orig_rel"))
            if target is None:
                restored.append({"name": name, "error": "orig_rel 缺失或越界"})
                continue
            if target.exists() and not force:
                restored.append({"name": name, "error": "目标已存在（加 --force）", "to": str(target)})
                continue
            members = [m for m in t.getmembers()
                       if m.name == name or m.name.startswith(name + "/")]
            tmp = Path(tempfile.mkdtemp(prefix="trash_restore_"))
            t.extractall(tmp, members=members)
            src = tmp / name
            if target.exists():
                if target.is_dir():
                    shutil.rmtree(target)
                else:
                    target.unlink()
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(target))
            shutil.rmtree(tmp, ignore_errors=True)
            restored.append({"name": name, "to": str(target)})
    return restored


def _restore_dir(entry, root, force):
    trash = trash_dir(root)
    d = trash / entry["id"]
    m = C.read_json(d / C.TRASH_MANIFEST, default={}) or {}
    restored = []
    for it in m.get("items", []):
        target = _safe_target(root, _rel(root, it.get("from")))
        src = d / it.get("name")
        if target is None or not src.exists():
            restored.append({"name": it.get("name"), "error": "缺失/越界"})
            continue
        if target.exists() and not force:
            restored.append({"name": it.get("name"), "error": "目标已存在（加 --force）", "to": str(target)})
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            if target.is_dir():
                shutil.rmtree(target)
            else:
                target.unlink()
        shutil.move(str(src), str(target))
        restored.append({"name": it.get("name"), "to": str(target)})
    return restored


def cmd_restore(args):
    root = resolve_root(args.root)
    trash = trash_dir(root)
    entry = find_entry(trash, root, args.id)
    if entry is None:
        C.emit({"status": "error", "message": "条目不存在: %s" % args.id}, 1)
    plan = [{"name": i.get("name"),
             "to": str(_safe_target(root, i.get("orig_rel")) or "<越界/缺失>"),
             "exists": bool(_safe_target(root, i.get("orig_rel")) and
                            _safe_target(root, i.get("orig_rel")).exists())}
            for i in entry["items"]]
    if not args.apply:
        C.emit({"status": "ok", "dry_run": True, "entry": args.id, "kind": entry["kind"],
                "restore": plan}, 0)
    restored = (_restore_archive(entry, root, args.force) if entry["kind"] == "archive"
                else _restore_dir(entry, root, args.force))
    # 全还原后清掉条目
    ok = [r for r in restored if r.get("to")]
    if entry["kind"] == "archive":
        if ok and len(ok) == len(entry["items"]):
            f = trash / entry["file"]
            if f.exists():
                f.unlink()
            idx = C.trash_index_load(trash)
            idx.pop(entry["id"], None)
            C.write_json(trash / C.TRASH_INDEX, idx)
    else:
        d = trash / entry["id"]
        remaining = [p for p in d.iterdir() if p.name != C.TRASH_MANIFEST] if d.is_dir() else []
        if not remaining:
            shutil.rmtree(d, ignore_errors=True)
    C.journal(root, "trash.restore", target=args.id, restored=[r.get("to") for r in ok])
    C.log("已还原: %s" % args.id)
    C.emit({"status": "ok", "dry_run": False, "entry": args.id, "restored": restored}, 0)


# -------------------------------------------------------------------- purge ---
def _entry_time(trash, root, eid):
    e = find_entry(trash, root, eid)
    return (e or {}).get("time", "")


def cmd_purge(args):
    root = resolve_root(args.root)
    trash = trash_dir(root)
    entries = iter_entries(trash, root)
    if args.id:
        entries = [e for e in entries if e["id"] == args.id]
        if not entries:
            C.emit({"status": "error", "message": "条目不存在: %s" % args.id}, 1)
    elif args.legacy:
        # ★ 无「原路径」的遗留项：散落文件 + 无 manifest 的旧目录（无法自动还原）
        entries = [e for e in entries
                   if e["kind"] == "loose" or (e["kind"] == "dir" and not e.get("has_manifest"))]
    elif not (args.all or args.older_than is not None):
        C.emit({"status": "error", "message": "须指定 --id、--all、--older-than DAYS 或 --legacy"}, 1)
    else:
        if args.older_than is not None:
            cutoff = datetime.datetime.now() - datetime.timedelta(days=args.older_than)
            keep = []
            for e in entries:
                try:
                    if datetime.datetime.fromisoformat(e["time"]) < cutoff:
                        keep.append(e)
                except Exception:
                    pass
            entries = [] if args.all else keep
    listing = [e["id"] for e in entries]
    if not entries:
        C.emit({"status": "ok", "purged": [], "message": "无匹配条目"}, 0)
    if not args.confirm:
        C.emit({"status": "error",
                "message": "彻底删除不可恢复；确认后加 --confirm（并确保已获用户同意）",
                "would_purge": listing}, 1)
    idx = C.trash_index_load(trash)
    freed = 0
    for e in entries:
        freed += e.get("orig_bytes") or 0
        if e["kind"] == "archive" and e.get("file"):
            f = trash / e["file"]
            if f.exists():
                f.unlink()
            idx.pop(e["id"], None)
        elif e["kind"] == "loose":
            f = trash / e["id"]
            if f.exists():
                f.unlink()
        else:
            d = trash / e["id"]
            if d.is_file():
                d.unlink()
            else:
                try:
                    C.rmtree_robust(d)          # 长路径稳健删除
                except Exception:
                    pass
    C.write_json(trash / C.TRASH_INDEX, idx)
    C.journal(root, "trash.purge", target=str(trash), entries=listing)
    C.log("已彻底删除 %d 个条目（约释放 %.2f GB）" % (len(entries), freed / 1e9))
    C.emit({"status": "ok", "purged_count": len(entries), "freed_bytes": freed}, 0)


# ----------------------------------------------------------------- compress ---
def cmd_compress(args):
    """把旧「目录式」条目（.trash/<id>/）补压成压缩包（一次性迁移）。"""
    root = resolve_root(args.root)
    trash = trash_dir(root)
    dirs = [e for e in iter_entries(trash, root) if e["kind"] == "dir"]
    # ★ 安全闸：**只压有 `_manifest.json`（含原路径）的条目**；旧格式（无原路径）**跳过**，
    #   否则压出来的包失去"原路径"→ 不可自动还原。
    plan, skipped = [], []
    for e in dirs:
        if e.get("has_manifest") and any((i.get("orig_rel") or "") for i in e["items"]):
            plan.append({"id": e["id"], "items": [i.get("name") for i in e["items"]]})
        else:
            skipped.append({"id": e["id"], "reason": "无 _manifest.json / 无原路径 → 跳过（不盲压）"})
    if not args.apply:
        C.emit({"status": "ok", "dry_run": True, "root": str(root),
                "would_compress": plan, "skipped": skipped}, 0)
    done, errors = [], []
    for e in dirs:
        if not (e.get("has_manifest") and any((i.get("orig_rel") or "") for i in e["items"])):
            continue
        d = trash / e["id"]
        rels, paths = [], []
        for it in e["items"]:
            src = d / it.get("name")
            if src.exists():
                paths.append(src)
                rels.append(it.get("orig_rel", ""))
        if not paths:
            try:
                C.rmtree_robust(d)
            except Exception:
                pass
            continue
        try:                                   # ★ 逐条目兜底：一条失败不影响其余
            arc, man = C.trash_entry(trash, root, paths, reason=e.get("reason", ""),
                                     algo=args.algo, rels=rels)
        except Exception as ex:
            errors.append({"id": e["id"], "error": str(ex)[:160]})
            continue
        # 压缩成功、且无成员被跳过 → 删掉原目录；有跳过则保留原目录（数据不丢）
        if not man.get("skipped_members"):
            try:
                C.rmtree_robust(d)
            except Exception:
                pass
        else:
            errors.append({"id": e["id"], "note": "部分成员读不到（长路径等）→ 原目录保留，包已生成",
                           "skipped_members": len(man["skipped_members"])})
        done.append({"from": e["id"], "to": arc.name,
                     "orig_bytes": e.get("orig_bytes"), "packed_bytes": arc.stat().st_size})
    C.journal(root, "trash.compress", target=str(trash), count=len(done),
              skipped=len(skipped), errors=len(errors))
    C.emit({"status": "ok", "dry_run": False, "compressed": done,
            "skipped": skipped, "errors": errors}, 0)


# ------------------------------------------------------------------- status ---
def cmd_status(args):
    start = Path(args.root).expanduser() if args.root else Path.cwd()
    root = C.find_root(start)
    if root is None:
        C.emit({"status": "error",
                "message": "未找到大项目根（缺 %s）；请用 --root 指定" % C.MARKER}, 1)
    trash = trash_dir(root)
    entries = iter_entries(trash, root)
    packed = sum(e["packed_bytes"] or 0 for e in entries)
    orig = sum(e["orig_bytes"] or 0 for e in entries)
    ratio = round(orig / packed, 2) if packed else None
    legacy = sum(1 for e in entries if e["kind"] == "dir")
    C.emit({"status": "ok", "root": str(root), "trash": str(trash),
            "count": len(entries), "legacy_dir_entries": legacy,
            "orig_bytes": orig, "packed_bytes": packed, "compress_ratio": ratio}, 0)


# --------------------------------------------------------------------- main ---
def main():
    ap = argparse.ArgumentParser(description="大项目根 .trash 软删除暂存（压缩 · 可还原）")
    sub = ap.add_subparsers(dest="action", required=True)

    p = sub.add_parser("put", help="压缩入暂存（默认预演，--apply 执行）")
    p.add_argument("paths", nargs="+", help="要移入的路径")
    p.add_argument("--reason", default="", help="删除原因")
    p.add_argument("--algo", choices=list(C.TRASH_ALGO_EXT), default=C.TRASH_ALGO,
                   help="压缩算法（默认 %s）" % C.TRASH_ALGO)
    p.add_argument("--root", help="大项目根（默认从路径向上查找标记）")
    p.add_argument("--apply", action="store_true", help="真正执行（默认仅预演）")
    p.set_defaults(func=cmd_put)

    p = sub.add_parser("list", help="列出暂存条目")
    p.add_argument("--root", help="大项目根")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("restore", help="还原到原路径（默认预演，--apply 执行）")
    p.add_argument("--id", required=True, help="条目 id")
    p.add_argument("--root", help="大项目根")
    p.add_argument("--apply", action="store_true", help="真正执行（默认仅预演）")
    p.add_argument("--force", action="store_true", help="目标已存在时覆盖")
    p.set_defaults(func=cmd_restore)

    p = sub.add_parser("purge", help="彻底删除（需 --confirm）")
    p.add_argument("--id", help="条目 id")
    p.add_argument("--all", action="store_true", help="全部条目")
    p.add_argument("--legacy", action="store_true",
                   help="★ 只删「无原路径」的遗留项（散落文件 + 无 manifest 的旧目录）")
    p.add_argument("--older-than", type=float, default=None, help="早于 N 天的条目")
    p.add_argument("--root", help="大项目根")
    p.add_argument("--confirm", action="store_true", help="确认彻底删除（不可恢复）")
    p.set_defaults(func=cmd_purge)

    p = sub.add_parser("compress", help="把旧目录式条目补压成压缩包")
    p.add_argument("--algo", choices=list(C.TRASH_ALGO_EXT), default=C.TRASH_ALGO)
    p.add_argument("--root", help="大项目根")
    p.add_argument("--apply", action="store_true", help="真正执行（默认仅预演）")
    p.set_defaults(func=cmd_compress)

    p = sub.add_parser("status", help="暂存区统计")
    p.add_argument("--root", help="大项目根")
    p.set_defaults(func=cmd_status)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
