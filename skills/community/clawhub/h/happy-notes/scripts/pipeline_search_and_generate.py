#!/usr/bin/env python3
"""
Pipeline 2: 搜索定位 → 定向生成

用法:
  python pipeline_search_and_generate.py \
    --kb "AI 论文集" --search "注意力机制" \
    --mode semantic --output-type PDF --query "对比分析"
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from iflow_common import (
    log, api_post, find_kb, submit_creation, poll_creation, output,
    validate_output_type, validate_preset,
)


def main():
    parser = argparse.ArgumentParser(description="Pipeline 2: 搜索并定向生成")
    parser.add_argument("--kb", default="", help="知识库名称")
    parser.add_argument("--kb-id", default="", help="知识库 ID")
    parser.add_argument("--search", required=True, help="搜索关键词")
    parser.add_argument("--mode", default="file", choices=["file", "semantic"], help="搜索模式")
    parser.add_argument("--output-type", default="PDF", help="生成类型")
    parser.add_argument("--query", default="", help="创作要求")
    parser.add_argument("--preset", default="", help="PPT 风格")
    parser.add_argument("--search-only", action="store_true", help="只搜索不生成")
    parser.add_argument("--poll-creation", action="store_true", help="轮询等待创作完成")
    args = parser.parse_args()

    # 参数校验
    args.output_type = validate_output_type(args.output_type)
    validate_preset(args.preset, args.output_type)

    kb_id = find_kb(args.kb or None, args.kb_id or None)
    log(f"知识库 ID: {kb_id}")

    matched_files = []
    search_results = []

    if args.mode == "semantic":
        log(f'步骤 2: 语义检索「{args.search}」(可能需要几秒到几十秒)...')
        body = {"query": args.search, "collectionId": kb_id}
        chunk_resp = api_post("/api/v1/knowledge/searchChunk", body, timeout=(10, 120))

        if chunk_resp.get("success") is not True:
            log(f"检索失败: {chunk_resp.get('message', '超时或服务异常')}")
            output({"error": "检索失败", "collectionId": kb_id})
            sys.exit(1)

        nodes = (chunk_resp.get("data") or {}).get("nodes", [])
        search_results = nodes
        node_count = len(nodes)
        log(f"检索到 {node_count} 个相关片段")

        # 提取去重 contentId
        unique_cids = list(set(n.get("contentId", "") for n in nodes))
        if unique_cids:
            files_resp = api_post(f"/api/v1/knowledge/pageQueryContents?collectionId={kb_id}&pageNum=1&pageSize=100")
            for item in files_resp.get("data", []):
                if item.get("contentId") in unique_cids:
                    matched_files.append({
                        "contentId": item["contentId"],
                        "fileName": item.get("fileName"),
                        "summary": item.get("summary"),
                        "status": item.get("status"),
                    })
    else:
        log(f'步骤 2: 文件级搜索「{args.search}」')
        files_resp = api_post(f"/api/v1/knowledge/pageQueryContents?collectionId={kb_id}&pageNum=1&pageSize=200")
        # 多 token OR 匹配：分词后任一命中即匹配（有意选择 OR 而非 AND，召回率更高）
        tokens = [t.strip().lower() for t in args.search.split() if t.strip()]
        for item in files_resp.get("data", []):
            fname = (item.get("fileName") or "").lower()
            summary = (item.get("summary") or "").lower()
            text = fname + " " + summary
            if any(tok in text for tok in tokens):
                matched_files.append({
                    "contentId": item["contentId"],
                    "fileName": item.get("fileName"),
                    "summary": item.get("summary"),
                    "status": item.get("status"),
                })
        log(f"找到 {len(matched_files)} 个匹配文件")

    for f in matched_files:
        log(f"  - {f['fileName']} ({f['status']})")

    creation_id = None
    creation_status = None
    if not args.search_only and matched_files:
        ready_files = [{"contentId": f["contentId"]} for f in matched_files if f["status"] == "success"]
        not_ready = len(matched_files) - len(ready_files)
        if not_ready > 0:
            log(f"警告: {not_ready} 个文件尚未解析完成")

        if ready_files:
            log(f"步骤 3: 提交创作任务 ({args.output_type})")
            creation_id = submit_creation(
                kb_id, args.output_type,
                query=args.query or None,
                preset=args.preset or None,
                files=ready_files,
            )
            creation_status = "submitted" if creation_id else "failed"

            if creation_id and args.poll_creation:
                creation_status = poll_creation(kb_id, creation_id)

    output({
        "collectionId": kb_id,
        "matchedFiles": matched_files,
        "searchResults": search_results,
        "creationId": creation_id,
        "creationStatus": creation_status,
    })


if __name__ == "__main__":
    main()
