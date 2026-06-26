#!/usr/bin/env python3
"""
飞书文件桥接脚本
将飞书下载的文件自动导入知识库

使用场景：
1. 用户在飞书发送文件
2. OpenClaw 下载文件到 /tmp/openclaw/xxx.pdf
3. 调用此脚本自动导入知识库
"""
import os
import sys
import json
from pathlib import Path

scripts_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, scripts_dir)

from kb_manager import ingest_file


def ingest_lark_file(file_path, category=None):
    """导入飞书下载的文件"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")
    
    result = ingest_file(file_path, suggested_category=category)
    return result


def ingest_lark_files_batch(file_paths, category=None):
    """批量导入多个飞书文件"""
    results = []
    for fp in file_paths:
        try:
            result = ingest_file(fp, suggested_category=category)
            results.append({"success": True, "file": fp, "result": result})
        except Exception as e:
            results.append({"success": False, "file": fp, "error": str(e)})
    return results


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="飞书文件导入知识库")
    parser.add_argument("file", help="飞书下载的文件路径")
    parser.add_argument("--category", "-c", help="指定分类")
    parser.add_argument("--json", "-j", action="store_true", help="JSON输出")
    
    args = parser.parse_args()
    
    try:
        result = ingest_lark_file(args.file, args.category)
        if args.json:
            print(json.dumps({"success": True, "result": result}, ensure_ascii=False, indent=2))
        else:
            print(f"✅ 已导入: {result['title']}")
            print(f"   分类: {result['category']}")
            print(f"   关键词: {', '.join(result['keywords'][:5])}")
    except Exception as e:
        if args.json:
            print(json.dumps({"success": False, "error": str(e)}, ensure_ascii=False))
        else:
            print(f"❌ 导入失败: {e}", file=sys.stderr)
        sys.exit(1)
