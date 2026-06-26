#!/usr/bin/env python3
"""火一五小红书发布后跟踪 — 记录笔记的 1 天 / 3 天 / 7 天表现。

为什么需要跟踪
==============
小红书的"赛马机制"会在发布后 24~72 小时给一波小流量，
笔记表现 (互动率) 决定后续是否进推荐池。如果你不记录，
就只能凭感觉判断哪些选题真的有效。

工作模式
========
1. **register**：把发布完成的笔记 (note_id) 关联到 publish_helper 生成的 post_uid。
2. **snapshot**：跑一次抓取，给指定笔记拍个"互动快照"（liked/collected/comment）。
3. **report**：列出所有跟踪中的笔记 + 各时间点的快照对比。

数据存储
========
默认 `~/.xiaohongshu/posts.jsonl`（与 publish_helper.py 默认一致）。
快照存到 `~/.xiaohongshu/snapshots.jsonl`。

用法
----

    # 1) 发布后回填 note_id
    python3 track_post.py register --uid abc123 --note-id 64abcd... \\
        --xsec-token xxx

    # 2) 拉一次快照（手动触发，不自动定时）
    python3 track_post.py snapshot --note-id 64abcd... --xsec-token xxx

    # 3) 看表现
    python3 track_post.py report

    # 4) 拉所有还在跟踪期的笔记快照
    python3 track_post.py snapshot-all
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

sys.path.insert(0, str(Path(__file__).parent))

from xhs_client import (  # noqa: E402
    BlockedByCaptcha,
    LoginRequired,
    RateLimited,
    XHSClient,
    XHSError,
    load_cookie_from_env,
)
from xhs_parser import note_to_dict, parse_note_page  # noqa: E402

DEFAULT_LOG = "~/.xiaohongshu/posts.jsonl"
DEFAULT_SNAPSHOTS = "~/.xiaohongshu/snapshots.jsonl"


# ---------- IO ----------


def _read_jsonl(path: str) -> List[Dict[str, Any]]:
    p = Path(os.path.expanduser(path))
    if not p.exists():
        return []
    out = []
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            pass
    return out


def _append_jsonl(path: str, entry: Dict[str, Any]) -> None:
    p = Path(os.path.expanduser(path))
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def _rewrite_jsonl(path: str, entries: List[Dict[str, Any]]) -> None:
    p = Path(os.path.expanduser(path))
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", encoding="utf-8") as f:
        for e in entries:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")


# ---------- 子命令 ----------


def cmd_register(args: argparse.Namespace) -> int:
    posts = _read_jsonl(args.log)
    found = False
    for p in posts:
        if p.get("post_uid") == args.uid:
            p["note_id"] = args.note_id
            p["xsec_token"] = args.xsec_token or ""
            p["published_at"] = dt.datetime.now().isoformat(timespec="seconds")
            found = True
            break
    if not found:
        print(f"❌ 没找到 post_uid={args.uid}，请先用 publish_helper.py 准备并 --log", file=sys.stderr)
        return 1
    _rewrite_jsonl(args.log, posts)
    print(f"✓ 已关联 note_id={args.note_id}")
    return 0


def cmd_snapshot(args: argparse.Namespace) -> int:
    try:
        cookie = load_cookie_from_env()
    except LoginRequired as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    client = XHSClient(cookie=cookie)
    return _do_snapshot(client, args.note_id, args.xsec_token, args.snapshots)


def _do_snapshot(client: XHSClient, note_id: str, xsec_token: str, snapshots_path: str) -> int:
    try:
        html = client.get_explore_page(note_id=note_id, xsec_token=xsec_token or None)
    except (RateLimited, BlockedByCaptcha) as e:
        print(f"❌ 风控触发：{e}", file=sys.stderr)
        return 2
    except XHSError as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    note = parse_note_page(html, note_id=note_id)
    if not note:
        print("❌ 解析失败，可能页面结构变化", file=sys.stderr)
        return 1
    nd = note_to_dict(note)
    inter = nd.get("interactions", {}) or {}
    snap = {
        "note_id": note_id,
        "snapshot_at": dt.datetime.now().isoformat(timespec="seconds"),
        "liked": int(inter.get("liked_count", 0) or 0),
        "collected": int(inter.get("collected_count", 0) or 0),
        "comment": int(inter.get("comment_count", 0) or 0),
        "shared": int(inter.get("shared_count", 0) or 0),
    }
    _append_jsonl(snapshots_path, snap)
    print(f"✓ 快照：{snap['liked']}赞 / {snap['collected']}藏 / {snap['comment']}评")
    return 0


def cmd_snapshot_all(args: argparse.Namespace) -> int:
    posts = _read_jsonl(args.log)
    active = [p for p in posts if p.get("note_id") and _within_tracking_period(p, args.days)]
    if not active:
        print("没有需要快照的笔记（已过 7 天跟踪期或未填 note_id）。")
        return 0

    try:
        cookie = load_cookie_from_env()
    except LoginRequired as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1

    client = XHSClient(cookie=cookie)
    fail = 0
    for p in active:
        print(f"\n→ {p.get('title', '')[:30]}（{p['note_id']}）")
        rc = _do_snapshot(client, p["note_id"], p.get("xsec_token", ""), args.snapshots)
        if rc != 0:
            fail += 1
            if rc == 2:
                # 风控立即停手
                print("⛔ 触发风控，停止后续快照")
                break
    print(f"\n完成 — {len(active) - fail} 成功 / {fail} 失败")
    return 0 if fail == 0 else 1


def _within_tracking_period(post: Dict[str, Any], days: int = 7) -> bool:
    pub = post.get("published_at") or post.get("drafted_at")
    if not pub:
        return False
    try:
        d = dt.datetime.fromisoformat(pub)
    except ValueError:
        return False
    return (dt.datetime.now() - d).total_seconds() < days * 86400


def cmd_report(args: argparse.Namespace) -> int:
    posts = _read_jsonl(args.log)
    snaps = _read_jsonl(args.snapshots)

    by_note: Dict[str, List[Dict[str, Any]]] = {}
    for s in snaps:
        by_note.setdefault(s.get("note_id", ""), []).append(s)
    for k in by_note:
        by_note[k].sort(key=lambda x: x.get("snapshot_at", ""))

    if not posts:
        print("还没有发布日志。先用 publish_helper.py --log <path>")
        return 0

    parts = ["# 火一五小红书发布跟踪报告\n"]
    parts.append(f"_共 {len(posts)} 条发布记录_\n")

    for p in sorted(posts, key=lambda x: x.get("drafted_at", ""), reverse=True):
        parts.append(f"## {p.get('title', '(无标题)')}")
        parts.append("")
        parts.append(f"- 起草：{p.get('drafted_at', '?')}")
        parts.append(f"- 发布：{p.get('published_at', '未发布')}")
        parts.append(f"- 文案分：{p.get('score', '?')}/100")
        parts.append(f"- note_id：{p.get('note_id') or '(待填)'}")

        snaps_for = by_note.get(p.get("note_id", ""), [])
        if snaps_for:
            parts.append("")
            parts.append("| 时间 | 点赞 | 收藏 | 评论 | 互动合计 |")
            parts.append("|---|---|---|---|---|")
            for s in snaps_for:
                total = s["liked"] + s["collected"] + s["comment"]
                parts.append(f"| {s['snapshot_at']} | {s['liked']} | {s['collected']} | {s['comment']} | **{total}** |")
        parts.append("")

    out = "\n".join(parts)
    if args.out:
        Path(args.out).write_text(out, encoding="utf-8")
        print(f"✓ 报告已写入 {args.out}", file=sys.stderr)
    else:
        print(out)
    return 0


# ---------- 入口 ----------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="track_post.py", description="发布后跟踪笔记表现")
    sub = p.add_subparsers(dest="cmd", required=True)

    pr = sub.add_parser("register", help="发布后回填 note_id")
    pr.add_argument("--uid", required=True, help="publish_helper.py 给的 post_uid")
    pr.add_argument("--note-id", required=True, help="发布完成后的笔记 ID")
    pr.add_argument("--xsec-token", default="", help="xsec_token (URL 里取)")
    pr.add_argument("--log", default=DEFAULT_LOG)
    pr.set_defaults(func=cmd_register)

    ps = sub.add_parser("snapshot", help="给指定笔记拍快照")
    ps.add_argument("--note-id", required=True)
    ps.add_argument("--xsec-token", default="")
    ps.add_argument("--snapshots", default=DEFAULT_SNAPSHOTS)
    ps.set_defaults(func=cmd_snapshot)

    psa = sub.add_parser("snapshot-all", help="给跟踪期内所有笔记拍快照（节流）")
    psa.add_argument("--days", type=int, default=7, help="跟踪期天数（默认 7 天）")
    psa.add_argument("--log", default=DEFAULT_LOG)
    psa.add_argument("--snapshots", default=DEFAULT_SNAPSHOTS)
    psa.set_defaults(func=cmd_snapshot_all)

    pre = sub.add_parser("report", help="生成跟踪报告")
    pre.add_argument("--log", default=DEFAULT_LOG)
    pre.add_argument("--snapshots", default=DEFAULT_SNAPSHOTS)
    pre.add_argument("--out", default="")
    pre.set_defaults(func=cmd_report)

    return p


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
