#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""oc_project_link.py — 检查/修复 OpenCode 对「本大项目根」的 project 记录（skill: project-organization）。

背景（2026-10-10 事故）：
  一个目录**先**被 OpenCode 认成项目（当时还没有 .git），**之后**才 `git init`
  → OpenCode 会为**同一目录**再建一条 git project，两条并存。它的「目录 → 项目」
  解析器取**最早创建**的那条（无会话），于是该文件夹的会话列表变空。
  （SQLite 里：`project` 表同一 worktree 两行；会话只挂在其中一行。）

本脚本只做两件事，且**绝不删除任何有会话的 project 行**：
  status  列出该目录在本地 opencode.db 里的所有 project 行 + 解析器倾向取哪条（最早）、哪条有会话。
  fix     删掉「0 会话」的冗余行，保留下有会话的那条；可选 --hub 一并清同步中枢（oc-sync）。

子命令:
  status [--root R] [--db PATH]
  fix    [--root R] [--db PATH] [--hub] [--ssh ALIAS] [--hub-root PATH] [--dry-run]

★ 修复后必须做两件事（脚本会打印提醒）：
  1) **重启 OpenCode 后台服务**（`... serve --service`）——项目缓存是启动时加载的，
     外部改库不刷新；不重启的话界面仍解析到旧 id。
  2) 其他机器若也有该行，需各自清一次；否则 oc-sync 会把它推回中枢、再灌回来。

stdout: JSON {"status":"ok"|"error", ...}
"""
import argparse
import json
import os
import shlex
import sqlite3
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # keep the (synced) skill dir free of __pycache__
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C  # noqa: E402

LOGIN_TABLES = ("session_v2", "session")   # 会话可能落在这两张表（V2 / V1）


def _nowin():
    """Windows：让子进程（opencode/ssh）不弹出控制台窗口。"""
    if os.name != "nt":
        return {}
    si = subprocess.STARTUPINFO()
    si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    si.wShowWindow = 0
    return {"creationflags": 0x08000000, "startupinfo": si}


def norm(p):
    """目录归一化：反斜杠→斜杠；Windows 下忽略大小写。仅用于比对。"""
    s = str(p).replace("\\", "/")
    return s.lower() if os.name == "nt" else s


def resolve_db(explicit=None):
    """定位本地 opencode.db：--db > $OPENCODE_DATA_DIR > `opencode debug paths db` > 默认。"""
    if explicit:
        p = Path(explicit).expanduser()
        return p if p.is_file() else None
    env = os.environ.get("OPENCODE_DATA_DIR")
    if env:
        cand = Path(env) / "opencode.db"
        if cand.is_file():
            return cand
    try:
        r = subprocess.run(["opencode", "debug", "paths", "db"], capture_output=True,
                           text=True, encoding="utf-8", errors="replace", timeout=30, **_nowin())
        lines = [l.strip() for l in (r.stdout or "").splitlines() if l.strip()]
        if lines and Path(lines[-1]).is_file():
            return Path(lines[-1])
    except Exception:
        pass
    p = Path.home() / ".local" / "share" / "opencode" / "opencode.db"
    return p if p.is_file() else None


def _session_counts(con, ids):
    """给定 project id 列表 → {id: 会话条数}（合并 V2/V1 两表）。"""
    tabs = {r[0] for r in con.execute("select name from sqlite_master where type='table'")}
    out = {i: 0 for i in ids}
    for t in LOGIN_TABLES:
        if t not in tabs:
            continue
        for i in ids:
            try:
                out[i] += con.execute('select count(*) from "%s" where project_id=?' % t, (i,)).fetchone()[0]
            except Exception:
                pass
    return out


def scan(db, root):
    """返回该目录在 opencode.db 里的所有 project 行（含会话数）。"""
    con = sqlite3.connect("file:%s?mode=ro" % str(db).replace("\\", "/"), uri=True)
    try:
        rows = list(con.execute("select rowid,id,worktree,vcs,time_created from project"))
        match = [{"rowid": r[0], "id": r[1], "worktree": r[2], "vcs": r[3],
                  "created": r[4]} for r in rows if norm(r[2]) == norm(root)]
        cnt = _session_counts(con, [m["id"] for m in match])
        for m in match:
            m["sessions"] = cnt.get(m["id"], 0)
        match.sort(key=lambda m: m["rowid"])
        return match
    finally:
        con.close()


def analyze(db, root):
    """给出「解析器倾向取哪条 / 保留哪条 / 可删哪些」。"""
    match = scan(db, root)
    n = len(match)
    likely = match[0]["id"] if match else None       # 实测：解析器取最早创建（rowid 最小）那条
    has_sess = [m for m in match if m["sessions"] > 0]
    if has_sess:
        keeper = max(has_sess, key=lambda m: (m["sessions"], 1 if m["vcs"] else 0, -m["rowid"]))
    elif match:
        keeper = max(match, key=lambda m: ((1 if m["vcs"] else 0), -m["rowid"]))
    else:
        keeper = None
    stale = [m for m in match if m["sessions"] == 0 and (keeper is None or m["id"] != keeper["id"])]
    dup = n > 1
    return {"root": str(root), "rows": match, "duplicates": dup, "count": n,
            "likely_resolved": likely, "keeper": (keeper or {}).get("id"),
            "stale": stale,
            "healthy": (not dup) or (len(stale) == 0 and keeper is not None and likely == keeper["id"])}


def quick_warning(root, db=None):
    """给 git_setup/audit 用的轻量检查：有重复则返回告警 dict，否则 None。不抛异常。"""
    try:
        root = Path(root).resolve()
        db = resolve_db(db)
        if not db:
            return None
        a = analyze(db, root)
        if not a["duplicates"]:
            return None
        stale_ids = [m["id"] for m in a["stale"]]
        return {"duplicates": True, "count": a["count"],
                "likely_resolved": a["likely_resolved"], "keeper": a["keeper"],
                "stale_ids": stale_ids,
                "hint": "OpenCode 对同一目录有 %d 条 project 记录（会话挂在其中一条）。"
                        "跑 `oc_project_link.py fix --hub` 去重，然后重启 OpenCode 服务。"
                        % a["count"]}
    except Exception:
        return None


# --------------------------------------------------------------------- fix ---

def _backup_rows(root, rows):
    ts = C.timestamp()
    base = Path(root)
    out = (base / C.TOOLS_DIR / ("oc_project_link-backup-%s.json" % ts)) if C.is_big_project(base) \
        else (Path.cwd() / ("oc_project_link-backup-%s.json" % ts))
    C.write_json(out, {"time": C.now_iso(), "root": str(root), "rows": rows})
    return out


def do_fix(db, root, stale, dry=False):
    """删掉 stale 中 0 会话的行（双保险：再查一次会话数）。返回 (deleted_ids, backup)。"""
    safe, refused = [], []
    con = sqlite3.connect(db, timeout=30)
    try:
        tabs = {r[0] for r in con.execute("select name from sqlite_master where type='table'")}
        for m in stale:
            s = 0
            for t in LOGIN_TABLES:
                if t in tabs:
                    try:
                        s += con.execute('select count(*) from "%s" where project_id=?' % t, (m["id"],)).fetchone()[0]
                    except Exception:
                        pass
            (refused if s else safe).append(m["id"])
        if dry or not safe:
            return {"deleted": [], "would_delete": safe, "refused_has_sessions": refused}, None
        backup = _backup_rows(root, [m for m in stale if m["id"] in safe])
        cur = con.cursor()
        cur.execute("PRAGMA foreign_keys=OFF")   # 删的是 0 会话行，无级联；关 FK 更稳
        cur.execute("PRAGMA busy_timeout=30000")
        for i in safe:
            cur.execute("DELETE FROM project WHERE id=?", (i,))
        con.commit()
        return {"deleted": safe, "refused_has_sessions": refused}, backup
    finally:
        con.close()


def hub_remove(ssh, hub_root, ids):
    """经 ssh 从中枢 tables/project.json 删掉给定 id（先备份）。返回 dict，失败不抛。"""
    code = (
        "import json,os,sys,shutil,time\n"
        "p=os.path.join(sys.argv[1],'tables','project.json')\n"
        "ids=set(json.loads(sys.argv[2]))\n"
        "d=json.load(open(p,encoding='utf-8'))\n"
        "shutil.copy(p,p+'.bak-'+time.strftime('%Y%m%d-%H%M%S'))\n"
        "before=len(d)\n"
        "d=[r for r in d if r.get('id') not in ids]\n"
        "tmp=p+'.tmp'\n"
        "json.dump(d,open(tmp,'w',encoding='utf-8'),ensure_ascii=False)\n"
        "os.replace(tmp,p)\n"
        "print(json.dumps({'ok':True,'rows':len(d),'removed':before-len(d)}))\n"
    )
    try:
        r = subprocess.run(["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=10", ssh,
                            "python3 - %s %s" % (hub_root, shlex.quote(json.dumps(ids)))],
                           input=code.encode("utf-8"), capture_output=True, timeout=60, **_nowin())
        if r.returncode != 0:
            return {"ok": False, "error": (r.stderr or b"")[:300].decode("utf-8", "replace")}
        last = [l for l in r.stdout.decode("utf-8", "replace").splitlines() if l.strip()]
        return json.loads(last[-1]) if last else {"ok": True}
    except Exception as e:  # noqa: BLE001
        return {"ok": False, "error": str(e)}


# -------------------------------------------------------------------- main ---

def _resolve_root(args):
    if getattr(args, "root", None):
        return Path(args.root).expanduser().resolve()
    r = C.find_root(Path.cwd())
    if r is None:
        C.emit({"status": "error",
                "message": "未找到大项目根（缺 %s）；请用 --root 指定" % C.MARKER}, 1)
    return r


def main():
    ap = argparse.ArgumentParser(description="OpenCode 对大项目根的 project 记录：检查/去重")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("status", help="列出该目录的 project 行 / 哪条有会话 / 解析器取向")
    p.add_argument("--root"); p.add_argument("--db")
    p = sub.add_parser("fix", help="删掉 0 会话的冗余 project 行（保留有会话的那条）")
    p.add_argument("--root"); p.add_argument("--db")
    p.add_argument("--hub", action="store_true", help="同时清同步中枢 tables/project.json")
    p.add_argument("--ssh", default=os.environ.get("OC_SYNC_SSH", ""),
                   help="中枢 ssh 别名（默认取 $OC_SYNC_SSH）")
    p.add_argument("--hub-root", default=os.environ.get("OC_SYNC_ROOT", ""),
                   help="中枢目录（默认取 $OC_SYNC_ROOT）")
    p.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = _resolve_root(args)
    db = resolve_db(args.db)
    if not db:
        C.emit({"status": "ok", "root": str(root), "db": None, "note":
                "未找到 opencode.db（--db / $OPENCODE_DATA_DIR / `opencode debug paths db` 都失败）",
                "duplicates": False, "rows": []}, 0)

    a = analyze(db, root)

    if args.cmd == "status":
        warnings = []
        if a["duplicates"]:
            warnings.append("同一目录有 %d 条 project 记录；解析器倾向取最早的 %s"
                            % (a["count"], a["likely_resolved"]))
            if a["stale"]:
                warnings.append("可去掉 0 会话冗余行：%s → 跑 `oc_project_link.py fix --hub`"
                                % ", ".join(m["id"] for m in a["stale"]))
            warnings.append("修复后必须重启 OpenCode 后台服务；多机需各自清一次")
        C.emit({"status": "ok", "db": str(db), **a, "warnings": warnings}, 0)

    # fix
    if not a["duplicates"]:
        C.emit({"status": "ok", "root": str(root), "db": str(db), "result": "no_duplicates",
                "rows": a["rows"]}, 0)
    if not a["stale"]:
        C.emit({"status": "error", "root": str(root), "db": str(db),
                "result": "cannot_auto_fix",
                "message": "多条记录都带会话，不能自动删；请人工确认（rows 见下）",
                "rows": a["rows"]}, 1)

    res, backup = do_fix(db, root, a["stale"], dry=args.dry_run)
    hub = None
    if args.hub and res["deleted"] and not args.dry_run:
        if not (args.ssh and args.hub_root):
            hub = {"status": "skipped",
                   "reason": "未配置同步中枢（需 --ssh/--hub-root 或 $OC_SYNC_SSH/$OC_SYNC_ROOT）"}
        else:
            hub = hub_remove(args.ssh, args.hub_root, res["deleted"])

    warnings = []
    if res["deleted"]:
        warnings.append("★ 必须重启 OpenCode 后台服务（`... serve --service`）才生效："
                        "项目缓存是启动时加载的，改库不刷新。")
        warnings.append("★ 其他机器若也有这些 id，需各自清一次；否则 oc-sync 会回灌。")
    if backup:
        C.journal(root, "oc_project.fix", target=root,
                  deleted=res["deleted"], backup=str(backup), hub=hub)

    C.emit({"status": "ok", "root": str(root), "db": str(db), "dry_run": args.dry_run,
            "result": "deleted" if res["deleted"] else "dry_run",
            "deleted": res["deleted"], "would_delete": res.get("would_delete", []),
            "refused_has_sessions": res.get("refused_has_sessions", []),
            "backup": str(backup) if backup else None,
            "hub": hub, "likely_resolved_before": a["likely_resolved"],
            "keeper": a["keeper"], "warnings": warnings}, 0)


if __name__ == "__main__":
    main()
