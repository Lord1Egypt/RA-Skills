#!/usr/bin/env python3
"""
Knowledge Base 向量检索增强模块
使用 chromadb 构建语义检索层
"""
import os
import sys
import json
from pathlib import Path

scripts_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, scripts_dir)

# 依赖检测（markitdown/jieba）
from _check_deps import check_dependencies, check_kb_ready
if not check_dependencies():
    sys.exit(1)
if not check_kb_ready():
    sys.exit(1)

from kb_manager import KB_ROOT, load_index, ensure_kb_exists

# chromadb 配置
CHROMA_DIR = KB_ROOT / ".chroma"
COLLECTION_NAME = "knowledge_base"


def ensure_chroma():
    """确保 chromadb 已安装"""
    try:
        import chromadb
        return chromadb
    except ImportError:
        print("正在安装 chromadb...")
        import subprocess
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "--break-system-packages",
            "chromadb"
        ])
        import chromadb
        return chromadb


def get_or_create_collection():
    """获取或创建 chroma collection"""
    chromadb = ensure_chroma()
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    
    try:
        collection = client.get_collection(name=COLLECTION_NAME)
    except Exception:
        collection = client.create_collection(
            name=COLLECTION_NAME,
            metadata={"description": "Knowledge Base semantic search"}
        )
    
    return collection


def build_vector_index(force_rebuild=False):
    """构建/重建向量索引"""
    ensure_kb_exists()
    collection = get_or_create_collection()
    index = load_index()
    
    # 获取已有文档 IDs
    existing_ids = set()
    try:
        result = collection.get()
        existing_ids = set(result["ids"])
    except Exception:
        pass
    
    added = 0
    skipped = 0
    
    for doc in index["documents"]:
        doc_id = doc["id"]
        
        if doc_id in existing_ids and not force_rebuild:
            skipped += 1
            continue
        
        # 读取 markdown 内容
        md_path = KB_ROOT / doc["md_path"]
        content = ""
        if md_path.exists():
            try:
                with open(md_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except:
                pass
        
        # 构建文档文本（标题 + 关键词 + 摘要 + 内容前2000字）
        doc_text = f"""Title: {doc['title']}
Category: {doc['category']}
Keywords: {', '.join(doc.get('keywords', []))}
Summary: {doc.get('summary', '')}
Content: {content[:3000]}"""
        
        # 添加到 chroma
        try:
            collection.add(
                ids=[doc_id],
                documents=[doc_text],
                metadatas=[{
                    "title": doc["title"],
                    "category": doc["category"],
                    "original_name": doc["original_name"],
                    "md_path": str(doc["md_path"]),
                    "keywords": json.dumps(doc.get("keywords", []), ensure_ascii=False)
                }]
            )
            added += 1
        except Exception as e:
            print(f"索引失败 {doc_id}: {e}")
    
    return {"added": added, "skipped": skipped, "total": len(index["documents"])}


def vector_search(query, n_results=10, category=None):
    """语义搜索"""
    collection = get_or_create_collection()
    
    filter_dict = None
    if category:
        filter_dict = {"category": category}
    
    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results,
            where=filter_dict
        )
        
        # 格式化结果
        formatted = []
        if results["ids"] and results["ids"][0]:
            for i, doc_id in enumerate(results["ids"][0]):
                formatted.append({
                    "id": doc_id,
                    "distance": results["distances"][0][i] if results["distances"] else None,
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "snippet": results["documents"][0][i][:200] if results["documents"] else ""
                })
        
        return formatted
    except Exception as e:
        return [{"error": str(e)}]


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="向量检索管理")
    subparsers = parser.add_subparsers(dest="command")
    
    p = subparsers.add_parser("build", help="构建/更新向量索引")
    p.add_argument("--force", "-f", action="store_true", help="强制重建")
    
    p = subparsers.add_parser("search", help="语义搜索")
    p.add_argument("query", help="搜索查询")
    p.add_argument("--limit", "-l", type=int, default=10)
    p.add_argument("--category", "-c", help="按分类过滤")
    
    args = parser.parse_args()
    
    if args.command == "build":
        result = build_vector_index(args.force)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.command == "search":
        results = vector_search(args.query, args.limit, args.category)
        print(json.dumps({"results": results}, ensure_ascii=False, indent=2))
    else:
        parser.print_help()
