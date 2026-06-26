#!/usr/bin/env python3
"""
Liquipedia Overwatch — 本地缓存管理工具
路径: /workspace/liquipedia-cache/
用法:
  python3 cache_manager.py save <type> <id> <json_data>
  python3 cache_manager.py load <type> <id>
  python3 cache_manager.py list <type>
  python3 cache_manager.py query <keyword>
  python3 cache_manager.py update-index
"""

import json
import os
import sys
import hashlib
from datetime import datetime, timezone
from pathlib import Path

CACHE_DIR = Path("/workspace/liquipedia-cache")
INDEX_FILE = CACHE_DIR / "index.json"

TYPE_DIRS = {
    "tournament": CACHE_DIR / "tournaments",
    "team":        CACHE_DIR / "teams",
    "player":      CACHE_DIR / "players",
    "hero_picks":  CACHE_DIR / "hero_picks",
    "match":       CACHE_DIR / "matches",
    "earnings":    CACHE_DIR / "earnings",
}

# ──────────────────────────────────────────
# 工具函数
# ──────────────────────────────────────────

def ensure_dirs():
    for d in TYPE_DIRS.values():
        d.mkdir(parents=True, exist_ok=True)
    CACHE_DIR.mkdir(exist_ok=True)

def load_index() -> dict:
    if INDEX_FILE.exists():
        return json.loads(INDEX_FILE.read_text())
    return {
        "version": "1.0",
        "last_updated": None,
        "sources": {
            "liquipedia_net": "UNAVAILABLE",
            "owtv_gg": "PRIMARY",
            "google_search": "PRIMARY"
        },
        "files": {}
    }

def save_index(idx: dict):
    idx["last_updated"] = datetime.now(timezone.utc).isoformat()
    INDEX_FILE.write_text(json.dumps(idx, ensure_ascii=False, indent=2))

def compute_hash(data: dict) -> str:
    s = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return "sha256:" + hashlib.sha256(s.encode()).hexdigest()[:12]

def type_to_dir(t: str) -> Path:
    return TYPE_DIRS.get(t, CACHE_DIR)

def id_to_filename(t: str, i: str) -> str:
    # player/team ID → lower-hyphen.json
    safe = i.lower().replace(" ", "-")
    if t in ("tournament", "earnings"):
        return f"{safe}.json"
    if t == "hero_picks":
        return f"{safe}.json"
    return f"{safe}.json"

# ──────────────────────────────────────────
# 命令：save
# ──────────────────────────────────────────

def cmd_save(data_type: str, item_id: str, json_data: str | None = None):
    """保存数据到缓存"""
    if data_type not in TYPE_DIRS:
        print(f"错误：未知类型 {data_type}，可选: {list(TYPE_DIRS.keys())}")
        return

    if json_data is None:
        print("错误：请提供 JSON 数据（从 stdin 或 --data 参数）")
        return

    # 支持从 stdin 读取完整 JSON
    if json_data == "-":
        raw = sys.stdin.read()
    else:
        raw = json_data

    data = json.loads(raw)
    data["schema_version"] = data.get("schema_version", "1.0")
    data["cached_at"] = datetime.now(timezone.utc).isoformat()

    dir_ = type_to_dir(data_type)
    filename = id_to_filename(data_type, item_id)
    filepath = dir_ / filename

    old_data = {}
    if filepath.exists():
        old_data = json.loads(filepath.read_text())

    filepath.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    new_hash = compute_hash(data)
    source_url = data.get("source_url", "")

    # 更新 index
    idx = load_index()
    index_key = f"{data_type}/{item_id}"
    idx["files"][index_key] = {
        "path": str(filepath.relative_to(CACHE_DIR)),
        "url_source": source_url,
        "last_fetched": data["cached_at"],
        "data_hash": new_hash,
        "changed": old_data.get("cached_at") != data["cached_at"]
    }
    save_index(idx)

    action = "更新" if old_data else "新增"
    print(f"✅ [{action}] {data_type}/{item_id}")
    print(f"   文件: {filepath.relative_to(CACHE_DIR)}")
    print(f"   哈希: {new_hash}")
    if source_url:
        print(f"   来源: {source_url}")

# ──────────────────────────────────────────
# 命令：load
# ──────────────────────────────────────────

def cmd_load(data_type: str, item_id: str):
    """从缓存读取数据"""
    idx = load_index()
    index_key = f"{data_type}/{item_id}"

    if index_key not in idx["files"]:
        print(f"❌ 缓存不存在: {data_type}/{item_id}")
        print(f"   可用数据: {list(idx['files'].keys())[:10]}...")
        return None

    path = CACHE_DIR / idx["files"][index_key]["path"]
    if not path.exists():
        print(f"⚠️  索引存在但文件缺失: {path}")
        return None

    data = json.loads(path.read_text())
    meta = idx["files"][index_key]
    print(f"📦 已缓存: {data_type}/{item_id}")
    print(f"   来源: {meta['url_source']}")
    print(f"   抓取时间: {meta['last_fetched']}")
    print(f"   哈希: {meta['data_hash']}")
    return data

# ──────────────────────────────────────────
# 命令：list
# ──────────────────────────────────────────

def cmd_list(data_type: str | None = None):
    """列出缓存数据"""
    idx = load_index()
    files = idx.get("files", {})

    if data_type:
        filtered = {k: v for k, v in files.items() if k.startswith(data_type + "/")}
    else:
        filtered = files

    if not filtered:
        print("📭 缓存为空（或无匹配数据）")
        return

    print(f"📋 缓存文件 ({len(filtered)} 项)\n")
    for key, meta in sorted(filtered.items()):
        freshness = meta.get("last_fetched", "?")
        source = meta.get("url_source", "?")
        if source and len(source) > 60:
            source = source[:60] + "..."
        print(f"  [{key}]")
        print(f"    抓取: {freshness}")
        print(f"    来源: {source}")
        print()

# ──────────────────────────────────────────
# 命令：query
# ──────────────────────────────────────────

def cmd_query(keyword: str):
    """按关键词搜索缓存内容"""
    idx = load_index()
    results = []
    keyword_lower = keyword.lower()

    for key, meta in idx["files"].items():
        path = CACHE_DIR / meta["path"]
        if not path.exists():
            continue
        data = json.loads(path.read_text())
        data_str = json.dumps(data, ensure_ascii=False).lower()
        if keyword_lower in data_str:
            results.append((key, meta, data))

    if not results:
        print(f"🔍 未找到包含「{keyword}」的数据")
        return

    print(f"🔍 找到 {len(results)} 条结果:\n")
    for key, meta, data in results:
        print(f"  [{key}] — {meta['last_fetched']}")
        # 打印关键字段
        for field in ("team_name_zh", "team_name_en", "name_zh",
                       "player_id", "tournament_id"):
            if field in data:
                print(f"    {field}: {data[field]}")
                break

# ──────────────────────────────────────────
# 命令：update-index
# ──────────────────────────────────────────

def cmd_update_index():
    """扫描所有目录，重新构建 index"""
    idx = load_index()
    new_files = {}

    for type_name, dir_ in TYPE_DIRS.items():
        if not dir_.exists():
            continue
        for fp in dir_.iterdir():
            if fp.suffix != ".json":
                continue
            try:
                data = json.loads(fp.read_text())
                item_id = fp.stem
                index_key = f"{type_name}/{item_id}"
                source = data.get("source_url", "")
                cached = data.get("cached_at", "")
                new_files[index_key] = {
                    "path": str(fp.relative_to(CACHE_DIR)),
                    "url_source": source,
                    "last_fetched": cached,
                    "data_hash": compute_hash(data)
                }
            except Exception:
                pass

    idx["files"] = new_files
    save_index(idx)
    print(f"✅ index 已更新，共 {len(new_files)} 条记录")

# ──────────────────────────────────────────
# CLI 入口
# ──────────────────────────────────────────

def main():
    ensure_dirs()

    if len(sys.argv) < 2:
        print(__doc__)
        return

    cmd = sys.argv[1]

    if cmd == "save" and len(sys.argv) >= 4:
        data_type, item_id = sys.argv[2], sys.argv[3]
        json_raw = sys.argv[4] if len(sys.argv) > 4 else "-"
        cmd_save(data_type, item_id, json_raw)

    elif cmd == "load" and len(sys.argv) >= 4:
        cmd_load(sys.argv[2], sys.argv[3])

    elif cmd == "list":
        dt = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_list(dt)

    elif cmd == "query" and len(sys.argv) >= 3:
        cmd_query(sys.argv[2])

    elif cmd == "update-index":
        cmd_update_index()

    else:
        print(__doc__)

if __name__ == "__main__":
    main()
