#!/usr/bin/env python3
"""火一五小红书"半自动发布"助手 — 不做自动化发布。

为什么不做自动化发布
====================
1. 小红书发布接口需要 X-s/X-t 签名 + 设备指纹 + 风控验证；
2. 自动化发布会立刻被识别为机器行为，账号轻则限流、重则永久封禁；
3. 即使绕过当前风控，一次平台升级你就要重写所有签名，账号还得跟着重置；
4. 个人号的核心资产是"信任画像" — 不值得为节省 30 秒发布时间冒险。

所以本脚本做的是 **"发布前把所有事做好"**：
- 跑合规扫描 + 打分；
- 整合标题 / 正文 / 话题 / 配图说明，复制到剪贴板；
- 给一份"打开 App 后的操作清单"；
- 记录到本地发布日志，方便后续 track_post.py 跟踪。

你只需要：
1. 跑这个脚本；
2. 打开小红书 App，粘贴；
3. 选好图，按发布 — 完事。

用法
----

    # 用一个准备好的草稿
    python3 publish_helper.py --in draft.md

    # 跳过打分（快速复制走人）
    python3 publish_helper.py --in draft.md --skip-score

    # 同时记录到日志
    python3 publish_helper.py --in draft.md --log ~/.xiaohongshu/posts.jsonl
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import platform
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any, Optional

sys.path.insert(0, str(Path(__file__).parent))

from xhs_writer import Draft, load_draft, score_post  # noqa: E402


# ---------- 剪贴板（跨平台） ----------


def copy_to_clipboard(text: str) -> bool:
    sysname = platform.system()
    try:
        if sysname == "Darwin":
            subprocess.run(["pbcopy"], input=text.encode("utf-8"), check=True)
            return True
        if sysname == "Linux":
            for cmd in (["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"]):
                try:
                    subprocess.run(cmd, input=text.encode("utf-8"), check=True)
                    return True
                except (FileNotFoundError, subprocess.CalledProcessError):
                    continue
            return False
        if sysname == "Windows":
            subprocess.run(["clip"], input=text.encode("utf-16"), check=True)
            return True
    except Exception:
        return False
    return False


# ---------- 检查表 ----------


_CHECKLIST = """
📋 发布前最后检查（请逐条确认）

  □ 1. 配图至少 3 张，首图清晰、信息密度合适
  □ 2. 配图无水印 / 别人的 logo / 截图侵权
  □ 3. 路人面部已打码（如果有路人入镜）
  □ 4. 视频笔记：前 3 秒有钩子，封面字号大
  □ 5. 标题已粘贴 → 检查没被截断；**核心关键词在前 13 字内**（搜索权重 40%）
  □ 6. 正文已粘贴 → emoji 显示正常、空行没丢
  □ 7. 话题 # 已选 3~6 个（建议 2泛词+2垂直+1长尾分级）
  □ 8. AI 创作请加 #AI生成内容（自 2026/01 起强制，未标会限流）
  □ 9. 地点 / 商品标签按需添加（自购请打 #自购分享）
  □ 10. 是否商业合作？是 → 走"蒲公英"申报
  □ 11. 发布时段：参考你账号的最佳时段（建议 7-9 / 12-13 / 17-21 时）
  □ 12. 互动引导优先评论（CES 4分）+ 软关注（CES 8分），少求点赞（CES 1分）
"""


def check_publish_cadence(log_path: str, *, today_max: int = 2,
                          interval_min_h: float = 2.0) -> Optional[str]:
    """根据本地 posts.jsonl 检查发布节奏。返回警告字符串（None=没问题）。"""
    p = Path(os.path.expanduser(log_path))
    if not p.exists():
        return None
    try:
        entries = []
        for line in p.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entries.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    except OSError:
        return None

    # 看今天已经发了几条 + 上次发的时间
    now = dt.datetime.now()
    today = now.date()
    todays = []
    last_publish: Optional[dt.datetime] = None
    for e in entries:
        ts = e.get("published_at") or e.get("drafted_at")
        if not ts:
            continue
        try:
            d = dt.datetime.fromisoformat(ts)
        except ValueError:
            continue
        if d.date() == today and e.get("note_id"):
            todays.append(d)
        if e.get("note_id") and (last_publish is None or d > last_publish):
            last_publish = d

    warnings = []
    if len(todays) >= today_max:
        warnings.append(
            f"⚠️ 今天已发布 {len(todays)} 篇 — 小红书风控建议每天 ≤ {today_max} 篇。"
            f"再发可能触发限流。"
        )
    if last_publish:
        elapsed_h = (now - last_publish).total_seconds() / 3600
        if elapsed_h < interval_min_h:
            warnings.append(
                f"⚠️ 距上次发布仅 {elapsed_h:.1f} 小时 — 建议间隔 ≥ {interval_min_h} 小时。"
                f"短时连发会被识别为异常。"
            )
    return "\n".join(warnings) if warnings else None


# ---------- 发布日志 ----------


def append_log(log_path: str, draft: Draft, score_total: int) -> str:
    """在本地追加一条发布日志（jsonl），返回生成的 post_uid。"""
    log = Path(os.path.expanduser(log_path))
    log.parent.mkdir(parents=True, exist_ok=True)
    post_uid = uuid.uuid4().hex[:10]
    entry = {
        "post_uid": post_uid,
        "title": draft.title,
        "tags": draft.tags,
        "score": score_total,
        "drafted_at": dt.datetime.now().isoformat(timespec="seconds"),
        "note_id": "",  # 用户发布后回填，给 track_post.py 用
    }
    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    return post_uid


# ---------- 主流程 ----------


def main() -> int:
    p = argparse.ArgumentParser(prog="publish_helper.py", description="发布前一站式准备")
    p.add_argument("--in", dest="path", required=True, help="草稿路径 (.md 或 .json)")
    p.add_argument("--skip-score", action="store_true", help="跳过打分，直接复制")
    p.add_argument("--skip-clipboard", action="store_true", help="不复制到剪贴板")
    p.add_argument("--log", default="", help="发布日志路径（jsonl）；不填则不记录")
    p.add_argument("--copy-mode", choices=["body", "all"], default="body",
                   help="body = 只复制正文+话题；all = 复制标题+正文+话题")
    args = p.parse_args()

    draft = load_draft(args.path)
    if not draft.title:
        print("❌ 草稿没有标题，请补上 (markdown 用 # 开头)", file=sys.stderr)
        return 1
    if not draft.content.strip():
        print("❌ 草稿没有正文", file=sys.stderr)
        return 1

    # 1. 打分（除非跳过）
    score_total = 0
    if not args.skip_score:
        score = score_post(draft.title, draft.content, draft.tags)
        score_total = score.total
        print(f"📊 文案分：{score.total}/100")
        if score.total < 60:
            print("\n⚠️  分数偏低，建议先跑 polish_post.py 看修改建议：")
            print(f"   python3 polish_post.py --in {args.path}")
            ans = input("仍然继续准备发布？[y/N] ").strip().lower()
            if ans != "y":
                return 1

    # 2. 拼好剪贴板内容
    if args.copy_mode == "all":
        clipboard = f"{draft.title}\n\n{draft.to_clipboard_text()}"
    else:
        clipboard = draft.to_clipboard_text()

    # 3. 复制
    if not args.skip_clipboard:
        ok = copy_to_clipboard(clipboard)
        if ok:
            chars = len(clipboard)
            print(f"✓ 已复制 {chars} 字到剪贴板（{args.copy_mode} 模式）")
        else:
            print("⚠️  剪贴板复制失败，下面手动复制：\n")
            print("-" * 40)
            print(clipboard)
            print("-" * 40)

    # 4. 记日志 + 节奏检查
    if args.log:
        warning = check_publish_cadence(args.log)
        if warning:
            print()
            print(warning)
            print()
            ans = input("仍要继续？[y/N] ").strip().lower()
            if ans != "y":
                print("已取消。建议明天再发，或先休息至少 2 小时。", file=sys.stderr)
                return 1
        post_uid = append_log(args.log, draft, score_total)
        print(f"✓ 已记录到 {args.log}（post_uid: {post_uid}）")
        print(f"   发布完成后回填 note_id：python3 track_post.py register --uid {post_uid} --note-id <id>")

    # 5. 显示标题（提醒：标题需要单独粘贴）
    print(f"\n📝 标题（请单独粘贴到 App 标题框）：")
    print(f"   {draft.title}")

    if draft.cover_hint:
        print(f"\n🖼️  封面建议：{draft.cover_hint}")
    if draft.image_hints:
        print("\n🖼️  配图建议：")
        for i, h in enumerate(draft.image_hints, 1):
            print(f"   图{i}：{h}")

    # 6. Checklist
    print(_CHECKLIST)

    print("👉 现在打开小红书 App / 创作中心，粘贴并发布。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
