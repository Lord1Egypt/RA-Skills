#!/usr/bin/env python3
"""Prompt history and favorites management."""

import argparse, json, os, sys
from datetime import datetime

HISTORY_FILE = os.path.expanduser("~/.openclaw/workspace/prompt-artist/data/history.json")


def load():
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    if os.path.exists(HISTORY_FILE):
        return json.load(open(HISTORY_FILE))
    return {"history": [], "favorites": []}


def save(data):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    json.dump(data, open(HISTORY_FILE, "w"), indent=2, ensure_ascii=False)


def add_to_history(original, optimized, platform, style=None, ratio="1:1"):
    data = load()
    entry = {
        "id": len(data["history"]) + 1,
        "original": original,
        "optimized": optimized,
        "platform": platform,
        "style": style,
        "ratio": ratio,
        "created": datetime.now().isoformat(),
        "favorite": False,
    }
    data["history"].append(entry)
    # Keep last 100
    data["history"] = data["history"][-100:]
    save(data)
    return entry


def add_favorite(item_id):
    data = load()
    for item in data["history"]:
        if item["id"] == item_id:
            item["favorite"] = True
            data["favorites"].append(item)
            save(data)
            return item
    return None


def remove_favorite(item_id):
    data = load()
    for item in data["history"]:
        if item["id"] == item_id:
            item["favorite"] = False
    data["favorites"] = [f for f in data["favorites"] if f["id"] != item_id]
    save(data)


def show(limit=20, favorites_only=False):
    data = load()
    if favorites_only:
        return {"favorites": data["favorites"]}
    return {"history": data["history"][-limit:]}


def format_output(data, favorites_only=False):
    items = data.get("favorites", []) if favorites_only else data.get("history", [])
    title = "⭐ 收藏提示词" if favorites_only else "📜 提示词历史"
    
    lines = [title, ""]
    for item in items:
        fav_icon = "⭐" if item.get("favorite") else "  "
        lines.append(f"{fav_icon} [{item['id']}] {item['platform']} - {item['original'][:40]}")
        lines.append(f"    ✨ {item['optimized'][:80]}...")
        if item.get("style"):
            lines.append(f"    🎨 风格：{item['style']}")
        lines.append(f"    📅 {item['created'][:10]}")
        lines.append("")
    
    if not items:
        lines.append("  (空列表)")
    
    return "\n".join(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--action", choices=["show", "add", "favorite", "unfavorite", "favorites"], default="show")
    p.add_argument("--id", type=int, default=None)
    p.add_argument("--original", default=None)
    p.add_argument("--optimized", default=None)
    p.add_argument("--platform", default=None)
    p.add_argument("--style", default=None)
    p.add_argument("--ratio", default="1:1")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    
    if a.action == "add":
        r = add_to_history(a.original, a.optimized, a.platform, a.style, a.ratio)
        print(f"✅ 已保存：[{r['id']}] {r['original'][:30]}")
    elif a.action == "favorite":
        r = add_favorite(a.id)
        if r:
            print(f"⭐ 已收藏：[{a.id}]")
        else:
            print(f"❌ 未找到 #{a.id}")
    elif a.action == "unfavorite":
        remove_favorite(a.id)
        print(f"✅ 已取消收藏：#{a.id}")
    elif a.action == "favorites":
        data = show(favorites_only=True)
        print(json.dumps(data, indent=2) if a.json else format_output(data, favorites_only=True))
    else:
        data = show(a.limit)
        print(json.dumps(data, indent=2) if a.json else format_output(data))
