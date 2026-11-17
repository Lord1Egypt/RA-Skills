#!/usr/bin/env python3
"""mcp_tools_archive.py — Infoseek MCP 归档/去重工具（G11 拆分 v1.0.1）"""
import sys
from pathlib import Path
from typing import Any, Dict

from mcp_tools_common import INFOSEEK_ROOT, ensure_dirs


# ══ 以下函数由 G11 拆分脚本从 infoseek_mcp_server.py 提取（v1.0.1）══

def tool_save_archive(args: Dict) -> Dict:
    """存档归档（v1.0.1 PATCH / G1：直接调用 helper 纯函数，弃 subprocess）

    修复：原实现硬编码 'python3' 调子进程，Windows 无此命令且进程依赖重。
    """
    import sys
    sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))
    ensure_dirs()
    try:
        from infoseek_helper import save_content_to_archive
    except ImportError:
        return {"error": "infoseek_helper 模块未找到"}

    metadata = args.get('metadata', {})
    try:
        result = save_content_to_archive(
            subject=args['subject'],
            url=args['url'],
            title=args.get('title', ''),
            content=args.get('content', ''),
            website=metadata.get('website', 'unknown'),
            fmt=metadata.get('format', 'md'),
            date=metadata.get('date', ''),
            author=metadata.get('author', 'unknown'),
            source=metadata.get('source', 'mcp'),
        )
        return {'ok': True, 'filename': result['filename'],
                'archive_path': result['archive_path'],
                'subject_dir': result['subject_dir'], 'sha1': result['sha1']}
    except (ValueError, KeyError) as e:
        return {'ok': False, 'error': str(e)}


def tool_check_dedup(args: Dict) -> Dict:
    """URL 去重检查（v1.0.1 PATCH / G1：直接调用 helper 纯函数，弃 subprocess）"""
    import sys
    sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))
    try:
        from infoseek_helper import check_url_dedup
    except ImportError:
        return {"error": "infoseek_helper 模块未找到"}
    result = check_url_dedup(args.get('url', ''))
    return {
        "url": args.get('url', ''),
        "dedup": result['dedup'],
        "normalized": result['normalized'],
        "sha1": result['sha1'],
        "subject": result['subject'],
        "crawl_time": result['crawl_time'],
        "filename": result['filename'],
    }


def tool_dedup_stats(args: Dict) -> Dict:
    """任务报告统计

    v1.0.1 PATCH (G1/G11): 弃 subprocess('python3') 调 helper（Windows 无 python3
    命令 → 归档统计挂），改为直接调用 helper 纯函数 load_db()，返回结构化统计。
    """
    import sys as _sys
    _sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))
    try:
        from infoseek_helper import load_db
        db = load_db()
        subjects = []
        for subj, stat in (db.get('subjects') or {}).items():
            subjects.append({
                "subject": subj,
                "url_count": stat.get('url_count', 0),
                "last_task_id": (stat.get('last_task_id') or 'N/A')[:8],
            })
        return {
            "db_version": db.get('version'),
            "db_created": db.get('created'),
            "url_total": len(db.get('urls', {})),
            "subject_total": len(subjects),
            "subjects": subjects,
        }
    except Exception as e:
        return {"error": f"dedup_stats 调用失败: {type(e).__name__}: {e}"}

