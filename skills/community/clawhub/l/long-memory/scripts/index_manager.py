#!/usr/bin/env python3
"""索引系统：加速大量文件检索"""

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

import sys
sys.path.insert(0, str(Path(__file__).parent))
from lib.filelock import safe_read, safe_write_json, safe_read_json, file_lock

DEFAULT_MEMORY_DIR = Path.home() / ".openclaw" / "workspace" / "memory"
INDEX_FILE = ".memory_index.json"


def build_index(memory_dir: Path) -> dict:
    """构建全量索引"""
    index = {
        "version": "1.0",
        "updated": datetime.now().isoformat(),
        "files": {},
        "topics": {},
        "tags": {},
        "dates": [],
        "stats": {"total_files": 0, "total_size": 0, "total_sessions": 0}
    }

    subdirs = ["conversations", "summaries", "distillations"]
    
    for subdir in subdirs:
        d = memory_dir / subdir
        if not d.exists():
            continue
        for fp in sorted(d.glob("*.md")):
            try:
                stat = fp.stat()
                mtime = datetime.fromtimestamp(stat.st_mtime).isoformat()
                content = fp.read_text(encoding="utf-8")
                
                file_entry = {
                    "path": str(fp.relative_to(memory_dir)),
                    "size": stat.st_size,
                    "mtime": mtime,
                    "type": subdir.rstrip("s"),
                    "topics": [],
                    "tags": [],
                    "session_count": content.count("## ["),
                    "keywords": set(),
                }

                # 提取话题
                topics = re.findall(r'###\s*话题[：:]\s*(.+)', content)
                file_entry["topics"] = [t.strip() for t in topics]
                for t in file_entry["topics"]:
                    if t not in index["topics"]:
                        index["topics"][t] = []
                    index["topics"][t].append(fp.stem)

                # 提取标签
                tag_lines = re.findall(r'\*\*标签[：:]\*\*\s*(.+)', content)
                tags = []
                for tl in tag_lines:
                    for tag in tl.split("，"):
                        tag = tag.strip()
                        if tag:
                            tags.append(tag)
                file_entry["tags"] = tags
                for tag in tags:
                    if tag not in index["tags"]:
                        index["tags"][tag] = []
                    index["tags"][tag].append(fp.stem)

                # 提取关键词（用户消息中的名词短语）
                user_msgs = re.findall(r'\*\*用户[：:]\*\*\s*(.+)', content)
                keywords = set()
                for msg in user_msgs:
                    # 简单中文分词：提取2-4字的中文片段
                    words = re.findall(r'[\u4e00-\u9fff]{2,4}', msg)
                    keywords.update(words)
                file_entry["keywords"] = sorted(keywords)

                index["files"][fp.stem] = file_entry
                index["stats"]["total_files"] += 1
                index["stats"]["total_size"] += stat.st_size
                index["stats"]["total_sessions"] += file_entry["session_count"]
                index["dates"].append(fp.stem)

            except Exception as e:
                print(f"⚠️ 索引跳过 {fp.name}: {e}")

    index["dates"] = sorted(set(index["dates"]))
    
    # 序列化时把 set 转为 list
    for f in index["files"].values():
        f["keywords"] = list(f.get("keywords", []))
    
    return index


def get_index(memory_dir: Path, rebuild: bool = False) -> dict:
    """获取索引，过期自动重建"""
    index_path = memory_dir / INDEX_FILE
    
    if rebuild or not index_path.exists():
        return rebuild_and_save(memory_dir)
    
    index = safe_read_json(index_path)
    
    # 检查是否有文件变更
    for name, entry in index.get("files", {}).items():
        fp = memory_dir / entry["path"]
        if not fp.exists():
            return rebuild_and_save(memory_dir)
        try:
            actual_mtime = datetime.fromtimestamp(fp.stat().st_mtime).isoformat()
            if actual_mtime != entry.get("mtime"):
                return rebuild_and_save(memory_dir)
        except OSError:
            return rebuild_and_save(memory_dir)
    
    # 检查是否有新文件
    actual_count = 0
    for subdir in ["conversations", "summaries", "distillations"]:
        d = memory_dir / subdir
        if d.exists():
            actual_count += len(list(d.glob("*.md")))
    if actual_count != index.get("stats", {}).get("total_files", 0):
        return rebuild_and_save(memory_dir)
    
    return index


def rebuild_and_save(memory_dir: Path) -> dict:
    """重建并保存索引"""
    print("🔄 重建索引...")
    index = build_index(memory_dir)
    safe_write_json(memory_dir / INDEX_FILE, index)
    print(f"✅ 索引已更新（{index['stats']['total_files']} 个文件）")
    return index


def search_index(index: dict, query: str | None = None,
                 topic: str | None = None, tag: str | None = None,
                 start_date: str | None = None, end_date: str | None = None,
                 days: int | None = None) -> list[dict]:
    """基于索引快速搜索"""
    from datetime import timedelta
    results = []
    
    if days:
        start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    if not end_date:
        end_date = datetime.now().strftime("%Y-%m-%d")
    
    for name, entry in index.get("files", {}).items():
        # 日期过滤
        if start_date and name < start_date:
            continue
        if name > end_date:
            continue
        
        # 标签过滤
        if tag:
            if tag.lower() not in [t.lower() for t in entry.get("tags", [])]:
                continue
        
        # 话题过滤
        if topic:
            if not any(topic.lower() in t.lower() for t in entry.get("topics", [])):
                continue
        
        # 关键词搜索
        if query:
            query_lower = query.lower()
            found = False
            if query_lower in name:
                found = True
            if not found:
                for kw in entry.get("keywords", []):
                    if query_lower in kw.lower():
                        found = True
                        break
            if not found:
                # 检查话题和标签
                for t in entry.get("topics", []):
                    if query_lower in t.lower():
                        found = True
                        break
            if not found:
                for t in entry.get("tags", []):
                    if query_lower in t.lower():
                        found = True
                        break
            if not found:
                continue
        
        results.append({"name": name, **entry})
    
    return sorted(results, key=lambda x: x["name"], reverse=True)


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="索引管理")
    p.add_argument("--memory-dir", default=None)
    p.add_argument("--rebuild", action="store_true", help="强制重建索引")
    p.add_argument("--search", "-q", default=None)
    p.add_argument("--topic", "-t", default=None)
    p.add_argument("--tag", default=None)
    p.add_argument("--days", type=int, default=None)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    md = args.memory_dir if args.memory_dir else DEFAULT_MEMORY_DIR
    md = Path(md)

    if args.rebuild:
        index = rebuild_and_save(md)
    else:
        index = get_index(md)
    
    if args.search or args.topic or args.tag or args.days:
        results = search_index(index, args.search, args.topic, args.tag, days=args.days)
        if args.json:
            print(json.dumps(results, ensure_ascii=False, indent=2))
        else:
            for r in results:
                print(f"📄 {r['name']} [{r['type']}] "
                      f"{' '.join(f'#{t}' for t in r['tags'])}")
                print(f"   {r['session_count']} sessions, {r['size']}B")
                if r['topics']:
                    print(f"   话题: {', '.join(r['topics'])}")
    else:
        stats = index.get("stats", {})
        print(f"📊 索引状态：{stats.get('total_files', 0)} 文件, "
              f"{stats.get('total_sessions', 0)} sessions, "
              f"{stats.get('total_size', 0)}B")
        print(f"📝 话题: {len(index.get('topics', {}))} 个")
        print(f"🏷️  标签: {len(index.get('tags', {}))} 个")
        print(f"📅 日期范围: {index['dates'][0] if index['dates'] else '-'} ~ "
              f"{index['dates'][-1] if index['dates'] else '-'}")
