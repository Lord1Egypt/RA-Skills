#!/usr/bin/env python3
"""
Knowledge Base 批量导入脚本
递归扫描目录，批量导入所有支持的文件
"""
import os
import sys
import json
from pathlib import Path
from collections import defaultdict

scripts_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, scripts_dir)

# 依赖检测
from _check_deps import check_dependencies, check_kb_ready
if not check_dependencies():
    sys.exit(1)
if not check_kb_ready():
    sys.exit(1)

from kb_manager import ingest_file, ensure_kb_exists

SUPPORTED_EXTS = {
    '.pdf', '.docx', '.pptx', '.xlsx', '.xls', '.html', '.htm',
    '.epub', '.txt', '.csv', '.json', '.xml', '.zip', '.png',
    '.jpg', '.jpeg', '.gif', '.webp', '.mp3', '.wav', '.mp4'
}


def find_files(root_dir, recursive=True):
    """查找所有支持的文件"""
    root = Path(root_dir).expanduser().resolve()
    if not root.exists():
        raise FileNotFoundError(f"目录不存在: {root}")
    
    files = []
    if recursive:
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTS:
                files.append(path)
    else:
        for path in root.iterdir():
            if path.is_file() and path.suffix.lower() in SUPPORTED_EXTS:
                files.append(path)
    
    return sorted(files)


def batch_ingest(root_dir, recursive=True, category=None, dry_run=False):
    """批量导入目录中的文件"""
    ensure_kb_exists()
    files = find_files(root_dir, recursive)
    
    imported = []
    skipped = []
    errors = []
    
    print(f"发现 {len(files)} 个待导入文件\n")
    
    for i, filepath in enumerate(files, 1):
        print(f"[{i}/{len(files)}] {filepath.name} ... ", end="", flush=True)
        
        if dry_run:
            print("[预览跳过]")
            imported.append({"file": str(filepath), "dry_run": True})
            continue
        
        try:
            result = ingest_file(str(filepath), suggested_category=category)
            imported.append({
                "file": str(filepath),
                "title": result["title"],
                "category": result["category"],
                "doc_id": result["id"]
            })
            print(f"✅ [{result['category']}] {result['title']}")
        except Exception as e:
            errors.append({"file": str(filepath), "error": str(e)})
            print(f"❌ {e}")
    
    # 统计
    cat_dist = defaultdict(int)
    for item in imported:
        if "category" in item:
            cat_dist[item["category"]] += 1
    
    return {
        "imported": imported,
        "skipped": skipped,
        "errors": errors,
        "total": len(files),
        "category_distribution": dict(cat_dist)
    }


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="批量导入文件到知识库")
    parser.add_argument("directory", help="要扫描的目录")
    parser.add_argument("--recursive", "-r", action="store_true", default=True, help="递归扫描（默认）")
    parser.add_argument("--no-recursive", action="store_true", help="不递归扫描")
    parser.add_argument("--category", "-c", help="指定分类（自动分类会覆盖此值）")
    parser.add_argument("--dry-run", "-d", action="store_true", help="预览模式")
    parser.add_argument("--json", "-j", action="store_true", help="输出JSON格式")
    
    args = parser.parse_args()
    
    recursive = not args.no_recursive
    
    try:
        result = batch_ingest(args.directory, recursive, args.category, args.dry_run)
        
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f"\n{'='*40}")
            print(f"总计: {result['total']}")
            print(f"成功: {len(result['imported'])}")
            print(f"失败: {len(result['errors'])}")
            if result["category_distribution"]:
                print("\n分类分布:")
                for cat, count in sorted(result["category_distribution"].items(), key=lambda x: -x[1]):
                    print(f"  • {cat}: {count}")
            if result["errors"]:
                print("\n失败文件:")
                for err in result["errors"]:
                    print(f"  • {err['file']}: {err['error']}")
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)
