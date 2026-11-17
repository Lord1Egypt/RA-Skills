#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""掘金定时发布驱动（通用版）——Windows 计划任务调用，无需 Claude 在线。

流程：自然排序 posts/*.md → 与掘金已发布文章按标题去重 → 发布第一篇未发布的。
护栏：当日上限 / 距最近一篇最小间隔 / 全部发完自动注销计划任务。
日志：stdout（bat 重定向到 _wf/auto_publish.log）。

用法（参数可写进计划任务，也可改下面的 DEFAULTS）：
  uv run auto_publish.py --daily-limit 2 --min-gap-hours 1
  uv run auto_publish.py --task-names Blog_am,Blog_pm     # 发完自动注销这些任务
  uv run auto_publish.py --only 某篇.md                    # 只发指定一篇（一次性任务）

⚠ 没有干跑模式：跑一次就是真发一次（验证即生产）。
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
import traceback
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
import publish as P

DEFAULTS = {
    "daily_limit": 0,        # 每日发布上限（0=不限，2026-09-19 用户决策：节奏自担）
    "min_gap_hours": 1.0,    # 距最近一篇的最小间隔（防同时段重复触发）
    "task_names": "",        # 队列发完自动注销的计划任务名（逗号分隔）
}


def natural_key(s: str):
    """自然排序：第9辩 < 第10辩（字典序会排反）。"""
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]


def log(msg: str) -> None:
    print(f"[{datetime.now():%Y-%m-%d %H:%M:%S}] {msg}", flush=True)


def published_articles(cookie: str) -> list[dict]:
    meta = P.load_meta()
    uid = meta.get("user_id")
    if not uid:
        u = P.api(P.USER_URL, None, cookie).get("data") or {}
        uid = str(u.get("user_id") or "")
        if uid:
            meta["user_id"] = uid
            P.save_meta(meta)
    r = P.api("/content_api/v1/article/list_by_user",
              {"user_id": uid, "cursor": "0", "limit": 30, "sort_type": 2}, cookie)
    data = r.get("data")
    items = data if isinstance(data, list) else (data or {}).get("data") or []
    return [(it.get("article_info") or {}) for it in items]


def publish_one(post: dict, cookie: str) -> str:
    """发一篇：建稿→封面→挂专栏→发布，返回 article_id。"""
    brief, _ = P.check_brief(post["description"])
    tag_ids = P.resolve_tag_ids(post, cookie, interactive=False)
    log(f"标签：{tag_ids}")
    time.sleep(P.CALL_GAP_SECONDS)
    draft_id = P.create_draft(post, brief, tag_ids, cookie)
    meta = P.load_meta()
    meta[f"draft_{post['file'].stem}"] = draft_id
    P.save_meta(meta)
    if not post["cover_image"]:
        P.upload_cover(post, draft_id)
    word_count = len(re.sub(r"\s", "", post["body"]))
    column_id = P.column_id_from_meta()
    time.sleep(P.CALL_GAP_SECONDS)
    return P.publish_draft(draft_id, cookie, word_count, column_id)


def main() -> int:
    ap = argparse.ArgumentParser(description="掘金定时发布驱动（配合 Windows 计划任务）")
    ap.add_argument("--posts-dir", default=str(P.POSTS), help="文章目录（默认 posts/）")
    ap.add_argument("--daily-limit", type=int, default=DEFAULTS["daily_limit"])
    ap.add_argument("--min-gap-hours", type=float, default=DEFAULTS["min_gap_hours"])
    ap.add_argument("--task-names", default=DEFAULTS["task_names"],
                    help="队列发完自动注销的计划任务名，逗号分隔")
    ap.add_argument("--only", default="", help="只发指定文件（跳过队列去重逻辑，用于一次性任务）")
    args = ap.parse_args()

    cookie = P.load_cookie()
    arts = published_articles(cookie)
    titles = {a.get("title", "") for a in arts}

    if args.only:
        path = Path(args.only)
        if not path.is_absolute():
            path = Path(args.posts_dir) / args.only
        log(f"一次性发布：{path.name}")
        article_id = publish_one(P.parse_post(path), cookie)
        log(f"✓ 已发布：https://juejin.cn/post/{article_id}（审核中属正常）")
        return 0

    # 护栏一：当日达上限 → 跳过；护栏二：最近一篇间隔不足 → 同时段重复触发，跳过
    today = datetime.now().date()
    if arts:
        today_n = sum(1 for a in arts
                      if datetime.fromtimestamp(float(a.get("ctime") or 0)).date() == today)
        newest_age_h = (time.time() - float(arts[0].get("ctime") or 0)) / 3600
        log(f"当日已发 {today_n} 篇；最近一篇 {newest_age_h:.1f} 小时前")
        if today_n >= args.daily_limit:
            log(f"已达每日上限 {args.daily_limit} 篇，跳过")
            return 0
        if newest_age_h < args.min_gap_hours:
            log(f"最近一篇不足 {args.min_gap_hours} 小时，跳过")
            return 0

    queue = sorted(Path(args.posts_dir).glob("*.md"), key=lambda p: natural_key(p.name))
    for f in queue:
        post = P.parse_post(f)
        if post["title_juejin"] in titles:
            continue
        log(f"发布下一篇：{f.name}")
        article_id = publish_one(post, cookie)
        log(f"✓ 已发布：https://juejin.cn/post/{article_id}（审核中属正常）")
        return 0

    log(f"队列 {len(queue)} 篇已全部发布")
    for tn in filter(None, args.task_names.split(",")):
        subprocess.run(["schtasks", "/Delete", "/TN", tn, "/F"], capture_output=True)
        log(f"已注销计划任务 {tn}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except SystemExit as e:
        if e.code not in (0, None):
            log(f"✗ 退出码 {e.code}")
        raise
    except Exception:
        log("✗ 异常：\n" + traceback.format_exc())
        sys.exit(1)
