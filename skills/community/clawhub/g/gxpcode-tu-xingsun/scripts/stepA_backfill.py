# GxpCode Skill — Step A 新源 history 回填
# 保留最新条目用于验证，其余写入 history.json

import json
import os
import re
import sys
import io
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _parse_date(date_str: str) -> datetime | None:
    """尝试解析日期字符串为 datetime，支持多种格式"""
    if not date_str or not date_str.strip():
        return None

    s = date_str.strip()

    # "2026.06  01" / "2026.06 01"  → "2026-06-01"
    cleaned = re.sub(r"[.\s]+", "-", s)

    for fmt in ("%Y-%m-%d", "%Y-%m-%d"):
        try:
            return datetime.strptime(cleaned, fmt)
        except ValueError:
            continue

    # 纯日期部分 "2026-06" → 补 "2026-06-01"
    m = re.match(r"^(\d{4})-(\d{2})$", cleaned)
    if m:
        try:
            return datetime.strptime(f"{m.group(1)}-{m.group(2)}-01", "%Y-%m-%d")
        except ValueError:
            pass

    return None


def _sort_by_date_desc(items: list) -> list:
    """按 date 倒序，date 为空/null 的排最后"""
    with_date = []
    without_date = []
    for item in items:
        dt = _parse_date(item.get("date", ""))
        if dt:
            with_date.append((dt, item))
        else:
            without_date.append(item)
    with_date.sort(key=lambda x: x[0], reverse=True)
    return [item for _, item in with_date] + without_date


def backfill(source_name: str, gxpcode_dir: str):
    """回填新源条目到 history.json，保留最新 1 条用于测试"""
    today = datetime.now().strftime("%Y-%m-%d")
    safe_name = source_name.replace("/", "_")

    # 1. 读 SA.3 提取结果
    items_path = os.path.join(gxpcode_dir, "stepA", f"{safe_name}_items.json")
    if not os.path.exists(items_path):
        print(f"[SKIP] Items file not found: {items_path}")
        return

    with open(items_path, "r", encoding="utf-8") as f:
        items = json.load(f)

    if not items:
        print("[SKIP] No items to backfill")
        return

    # 2. 按 date 倒排，剔除最新
    sorted_items = _sort_by_date_desc(items)
    test_item = sorted_items[0]
    to_backfill = sorted_items[1:]

    if not to_backfill:
        print(f"[WARN] 仅 1 条，无法回填。测试条目: {test_item.get('title', '')[:50]}")
        return

    # 3. 输出测试条目
    print("=" * 50)
    print("[TEST ITEM] 保留用于验证（最新，不写入 history）：")
    print(f"  标题: {test_item.get('title', '')}")
    print(f"  日期: {test_item.get('date', '未知')}")
    print(f"  URL:  {test_item.get('url', '')}")
    print(f"[BACKFILL] 其余 {len(to_backfill)} 条写入 history.json")
    print("=" * 50)

    # 4. 读现有 history
    history_path = os.path.join(SKILL_DIR, "gxpcode_data", "history.json")
    os.makedirs(os.path.dirname(history_path), exist_ok=True)
    if os.path.exists(history_path):
        with open(history_path, "r", encoding="utf-8") as f:
            history = json.load(f)
    else:
        history = {}

    # 5. 追加（幂等，按 (title, url) 去重）
    history.setdefault(source_name, [])
    existing = {(r["title"], r["url"]) for r in history[source_name]}
    added = 0
    for item in to_backfill:
        key = (item["title"], item["url"])
        if key not in existing:
            history[source_name].append({
                "title": item["title"],
                "url": item["url"],
                "date": item.get("date", today),
                "first_seen": today,
                "last_updated": today,
            })
            existing.add(key)
            added += 1

    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    # 6. 写回填标记
    marker_path = os.path.join(SKILL_DIR, "gxpcode_data", f".backfilled_{safe_name}")
    with open(marker_path, "w", encoding="utf-8") as f:
        f.write(f"backfilled {today}, {added} items\n")

    total = sum(len(v) for v in history.values())
    print(f"[DONE] {source_name}: {added} backfilled, history total: {total}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python stepA_backfill.py <gxpcode_dir> <source_name>")
        sys.exit(1)
    backfill(sys.argv[2], sys.argv[1])
