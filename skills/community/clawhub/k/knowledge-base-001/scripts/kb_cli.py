#!/usr/bin/env python3
"""
Knowledge Base 主交互脚本
提供友好的命令行接口供 OpenClaw 调用
"""
import os
import sys
import json
import argparse

# 将 scripts 目录加入路径
scripts_dir = os.path.dirname(os.path.abspath(__file__))
import sys
sys.path.insert(0, scripts_dir)

from _check_deps import check_dependencies, check_kb_ready
if not check_dependencies(auto_install=True):
    sys.exit(1)
if not check_kb_ready():
    sys.exit(1)

from kb_manager import (
    ingest_file, search_kb, list_documents, get_document,
    delete_document, add_category, get_stats, ensure_kb_exists
)

def main():
    parser = argparse.ArgumentParser(description="Knowledge Base CLI")
    subparsers = parser.add_subparsers(dest="command")
    
    # ingest
    p = subparsers.add_parser("ingest", help="导入文件到知识库")
    p.add_argument("filepath")
    p.add_argument("--category", "-c", default=None)
    
    # search
    p = subparsers.add_parser("search", help="搜索知识库")
    p.add_argument("query")
    p.add_argument("--category", "-c", default=None)
    p.add_argument("--limit", "-l", type=int, default=10)
    
    # list
    p = subparsers.add_parser("list", help="列出文档")
    p.add_argument("--category", "-c", default=None)
    
    # stats
    subparsers.add_parser("stats", help="统计信息")
    
    # get
    p = subparsers.add_parser("get", help="获取文档详情")
    p.add_argument("doc_id")
    
    # delete
    p = subparsers.add_parser("delete", help="删除文档")
    p.add_argument("doc_id")
    
    # add-category
    p = subparsers.add_parser("add-category", help="添加分类")
    p.add_argument("name")
    
    args = parser.parse_args()
    
    ensure_kb_exists()
    
    if args.command == "ingest":
        try:
            result = ingest_file(args.filepath, args.category)
            print(json.dumps({"success": True, "document": result}, ensure_ascii=False, indent=2))
        except Exception as e:
            print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)
    
    elif args.command == "search":
        results = search_kb(args.query, args.category, args.limit)
        print(json.dumps({"success": True, "results": results, "count": len(results)}, ensure_ascii=False, indent=2))
    
    elif args.command == "list":
        docs = list_documents(args.category)
        print(json.dumps({"success": True, "documents": docs, "count": len(docs)}, ensure_ascii=False, indent=2))
    
    elif args.command == "stats":
        stats = get_stats()
        print(json.dumps({"success": True, "stats": stats}, ensure_ascii=False, indent=2))
    
    elif args.command == "get":
        doc = get_document(args.doc_id)
        if doc:
            print(json.dumps({"success": True, "document": doc}, ensure_ascii=False, indent=2))
        else:
            print(json.dumps({"success": False, "error": "Document not found"}, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)
    
    elif args.command == "delete":
        if delete_document(args.doc_id):
            print(json.dumps({"success": True, "message": "Deleted"}, ensure_ascii=False))
        else:
            print(json.dumps({"success": False, "error": "Document not found"}, ensure_ascii=False), file=sys.stderr)
            sys.exit(1)
    
    elif args.command == "add-category":
        added = add_category(args.name)
        print(json.dumps({"success": True, "added": added}, ensure_ascii=False))
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
