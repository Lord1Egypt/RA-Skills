#!/usr/bin/env python3
"""Pipeline: 分享知识库

用法:
  python3 scripts/pipeline_share.py --kb "知识库名称"
  python3 scripts/pipeline_share.py --kb-id "xxx"
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from iflow_common import log, api_post, find_kb, output, build_share_url


def main():
    parser = argparse.ArgumentParser(description="分享知识库")
    parser.add_argument("--kb", default="", help="知识库名称")
    parser.add_argument("--kb-id", default="", help="知识库 ID")
    args = parser.parse_args()

    kb_id = find_kb(args.kb or None, args.kb_id or None)
    log(f"知识库 ID: {kb_id}")

    resp = api_post("/api/v1/knowledge/shareNotebook", {"collectionId": kb_id})
    share_data = resp.get("data")
    if share_data:
        share_url = build_share_url(share_data)
        log(f"分享链接: {share_url}")
        output({"collectionId": kb_id, "shareUrl": share_url})
    else:
        msg = resp.get("message", "未知错误")
        log(f"分享失败: {msg}")
        output({"collectionId": kb_id, "error": msg})
        sys.exit(1)


if __name__ == "__main__":
    main()
