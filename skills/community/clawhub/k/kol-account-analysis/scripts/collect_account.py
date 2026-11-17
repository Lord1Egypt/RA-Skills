#!/usr/bin/env python3
"""
达人账号数据采集骨架（T4 公开页面路径）
用于 kol-account-analysis skill Step 2：采集作品列表与评论区，输出结构化 CSV。

依赖:
    pip install playwright && playwright install chromium

用法:
    python scripts/collect_account.py --platform douyin --url "https://..." --out ./out
    python scripts/collect_account.py --platform xiaohongshu --url "https://..." --max-works 45

限制与责任:
    - 平台 DOM 持续变动，SELECTORS 需按目标平台当前页面适配后使用（见 collection-playbook.md 2.3）。
    - 仅采集公开可见数据；评论输出不含昵称/头像（去标识化，对齐 data-collection.md 合规红线）。
    - 内置拟人化延时控制频率；触发平台风控/封禁的风险由使用者自担。
"""

import argparse
import csv
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

# ---- 平台选择器配置（占位示例，运行时必须按实际 DOM 适配）----
# 值可以是 CSS 选择器字符串。选择器失效时脚本会记录缺失并继续，不会硬失败。
SELECTORS = {
    "douyin": {
        "work_card": "a[href*='/video/']",
        "work_like": "div[data-e2e='like-count']",
        "work_comment": "div[data-e2e='comment-count']",
        "comment_item": "div[data-e2e='comment-item']",
        "comment_content": "span[data-e2e='comment-text']",
        "comment_like": "div[data-e2e='comment-like']",
    },
    "xiaohongshu": {
        "work_card": "section.note-item a",
        "work_like": "span.count",
        "comment_item": "div.comment-item",
        "comment_content": "span.content",
        "comment_like": "span.like",
    },
    "bilibili": {
        "work_card": "a[href*='/video/BV']",
        "comment_item": "div.reply-item",
        "comment_content": "span.reply-content",
        "comment_like": "span.like",
    },
}

DEFAULT_SELECTORS = {
    "work_card": "a",
    "comment_item": "[class*='comment']",
    "comment_content": "[class*='content']",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def human_delay(base: float = 1.5) -> None:
    """拟人化延时：降低触发平台风控的概率。"""
    time.sleep(random_range(base))


def random_range(base: float) -> float:
    return base * random.uniform(0.6, 1.6)


def text_of(page, selector, default: str = "") -> str:
    try:
        el = page.query_selector(selector)
        return el.inner_text().strip() if el else default
    except Exception:
        return default


def scroll_to_load(page, max_scrolls: int) -> int:
    """向下滚动触发懒加载，返回新增作品卡数量（粗略）。"""
    added = 0
    for _ in range(max_scrolls):
        before = page.query_selector_all(SELECTORS[page.platform]["work_card"])
        page.mouse.wheel(0, 1800)
        page.wait_for_timeout(random_range(1200))
        after = page.query_selector_all(SELECTORS[page.platform]["work_card"])
        if len(after) <= len(before):
            break
        added = len(after) - len(before)
    return added


def collect_comments(page, work_id: str, max_comments: int) -> list:
    """展开并采集一条作品的可见评论（去标识化：只取内容与点赞数）。"""
    comments = []
    page.mouse.wheel(0, 1200)
    page.wait_for_timeout(random_range(1200))

    while len(comments) < max_comments:
        items = page.query_selector_all(SELECTORS[page.platform]["comment_item"])
        if not items:
            break
        for item in items:
            if len(comments) >= max_comments:
                break
            content = text_of(
                item, SELECTORS[page.platform].get("comment_content", DEFAULT_SELECTORS["comment_content"])
            )
            likes = text_of(
                item, SELECTORS[page.platform].get("comment_like", ""), "0"
            )
            if not content:
                continue
            comments.append(
                {
                    "work_id": work_id,
                    "content": content,
                    "likes": likes,
                    "is_top": "",
                    "fetch_time": now_iso(),
                }
            )
        # 尝试加载更多评论；加载不出新条目即结束
        before = len(comments)
        page.mouse.wheel(0, 1600)
        page.wait_for_timeout(random_range(1200))
        after_load = page.query_selector_all(SELECTORS[page.platform]["comment_item"])
        if len(after_load) <= len(items):
            break
        if len(comments) == before:
            break
    return comments


def main() -> int:
    parser = argparse.ArgumentParser(description="达人账号 T4 公开数据采集骨架")
    parser.add_argument("--platform", required=True, choices=list(SELECTORS.keys()))
    parser.add_argument("--url", required=True, help="达人主页 URL")
    parser.add_argument("--out", default="./out", help="输出目录（默认 ./out）")
    parser.add_argument("--max-works", type=int, default=40, help="最多采集作品数")
    parser.add_argument("--max-comments", type=int, default=1000, help="每条作品最多采集评论数")
    parser.add_argument("--max-scrolls", type=int, default=15, help="列表页最大滚动次数")
    parser.add_argument("--headless", action="store_true", help="无头模式（默认 False，便于人工适配选择器）")
    args = parser.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    works_path = out_dir / "works.csv"
    comments_path = out_dir / "comments.csv"

    works_fields = ["work_id", "platform", "url", "publish_time", "likes", "comments", "favorites", "is_pinned", "caption", "fetch_time"]
    comments_fields = ["work_id", "content", "likes", "is_top", "fetch_time"]

    fetch_time = now_iso()
    works_rows, comment_rows = [], []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        page = browser.new_page()
        page.platform = args.platform  # 供 text_of/scroll 读取选择器
        page.goto(args.url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(3000)
        human_delay()

        scroll_to_load(page, args.max_scrolls)

        cards = page.query_selector_all(SELECTORS[args.platform]["work_card"])[: args.max_works]
        for idx, card in enumerate(cards, start=1):
            work_id = f"{args.platform}_{fetch_time}_{idx}"
            href = card.get_attribute("href") or ""
            url = href if href.startswith("http") else page.url.split("?")[0] + href
            works_rows.append(
                {
                    "work_id": work_id,
                    "platform": args.platform,
                    "url": url,
                    "publish_time": text_of(card, "[time], [data-e2e='publish-time']"),
                    "likes": text_of(card, SELECTORS[args.platform].get("work_like", "")),
                    "comments": text_of(card, SELECTORS[args.platform].get("work_comment", "")),
                    "favorites": text_of(card, "[data-e2e='favorite-count']"),
                    "is_pinned": "",
                    "caption": text_of(card, "[class*='title'], [class*='desc']"),
                    "fetch_time": fetch_time,
                }
            )
            # 打开详情页采集评论（公开可见部分）
            try:
                with page.expect_popup() as popup_info:
                    card.click()
                detail = popup_info.value
                detail.wait_for_load_state("domcontentloaded", timeout=30000)
                detail.wait_for_timeout(2000)
                comment_rows.extend(
                    collect_comments(detail, work_id, args.max_comments)
                )
                detail.close()
            except Exception as exc:
                sys.stderr.write(f"[warn] 作品 {work_id} 详情/评论采集失败: {exc}\n")
            human_delay(2.0)
        browser.close()

    with works_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=works_fields)
        writer.writeheader()
        writer.writerows(works_rows)
    with comments_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=comments_fields)
        writer.writeheader()
        writer.writerows(comment_rows)

    print(f"[ok] works={len(works_rows)} comments={len(comment_rows)}")
    print(f"[ok] 输出: {works_path} / {comments_path}")
    print("[note] 选择器为占位配置，若采集为空请按 collection-playbook.md 2.3 适配当前 DOM。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
