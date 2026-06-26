#!/usr/bin/env python3
"""Pipeline: 查看生成任务进度

用法:
  python3 scripts/pipeline_check_status.py --kb "知识库名称"
  python3 scripts/pipeline_check_status.py --kb-id "xxx" --creation-id "yyy"
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from iflow_common import log, api_get, find_kb, output


def main():
    parser = argparse.ArgumentParser(description="查看生成任务进度")
    parser.add_argument("--kb", default="", help="知识库名称")
    parser.add_argument("--kb-id", default="", help="知识库 ID")
    parser.add_argument("--creation-id", default="", help="特定创作任务 ID（不传则列出全部）")
    args = parser.parse_args()

    kb_id = find_kb(args.kb or None, args.kb_id or None)
    log(f"知识库 ID: {kb_id}")

    resp = api_get(f"/api/v1/knowledge/creationList?collectionId={kb_id}&pageSize=50")
    items = resp.get("data", [])

    if args.creation_id:
        items = [i for i in items if i.get("contentId") == args.creation_id]

    results = []
    for item in items:
        extra = item.get("extra") or {}
        status = extra.get("status", "unknown")
        results.append({
            "creationId": item.get("contentId"),
            "type": extra.get("fileType", ""),
            "status": status,
            "query": extra.get("query", ""),
            "fileName": item.get("fileName", ""),
        })

    # 日志摘要
    for r in results:
        status_text = {"success": "已完成", "failed": "失败", "processing": "生成中", "pending": "排队中"}.get(r["status"], r["status"])
        log(f"  {r['type'] or '?'} — {status_text}")

    output({"collectionId": kb_id, "total": len(results), "creations": results})


if __name__ == "__main__":
    main()
