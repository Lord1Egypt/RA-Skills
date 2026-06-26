#!/usr/bin/env python3
"""
Pipeline 4: 语义检索 + 可选生成/分享

用法:
  python pipeline_semantic_search.py \
    --kb "天文论文集" --query "宇宙演化巡天"

  python pipeline_semantic_search.py \
    --kb "AI 论文集" --query "注意力机制" \
    --generate --output-type PDF --gen-query "总结研究进展" --share
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from iflow_common import (
    log, api_post, find_kb, submit_creation, poll_creation, output,
    validate_output_type, validate_preset, build_share_url,
)


def main():
    parser = argparse.ArgumentParser(description="Pipeline 4: 语义检索 + 生成/分享")
    parser.add_argument("--kb", default="", help="知识库名称")
    parser.add_argument("--kb-id", default="", help="知识库 ID")
    parser.add_argument("--query", required=True, help="检索关键词")
    parser.add_argument("--content-ids", default="", help="限定文件范围，逗号分隔")
    parser.add_argument("--generate", action="store_true", help="基于结果生成")
    parser.add_argument("--output-type", default="PDF", help="生成类型")
    parser.add_argument("--gen-query", default="", help="创作要求")
    parser.add_argument("--preset", default="", help="PPT 风格")
    parser.add_argument("--share", action="store_true", help="生成分享链接")
    parser.add_argument("--poll-creation", action="store_true", help="轮询等待创作完成")
    parser.add_argument("--timeout", type=int, default=120, help="searchChunk 超时秒数")
    args = parser.parse_args()

    # 参数校验
    args.output_type = validate_output_type(args.output_type)
    validate_preset(args.preset, args.output_type)

    kb_id = find_kb(args.kb or None, args.kb_id or None)
    log(f"知识库 ID: {kb_id}")

    # 步骤 2: 语义检索
    log(f'步骤 2: 语义检索「{args.query}」(可能需要几秒到几十秒)...')
    body = {"query": args.query, "collectionId": kb_id}
    if args.content_ids:
        body["contentIds"] = [c.strip() for c in args.content_ids.split(",")]

    chunk_resp = api_post("/api/v1/knowledge/searchChunk", body, timeout=(10, args.timeout))

    if chunk_resp.get("success") is not True:
        log(f"检索失败: {chunk_resp.get('message', '超时或服务异常')}")
        output({"error": "检索失败", "collectionId": kb_id})
        sys.exit(1)

    data = chunk_resp.get("data", {})
    nodes = data.get("nodes", [])
    node_count = data.get("node_count", 0)
    elapsed_ms = data.get("elapsed_ms", 0)

    log(f"检索到 {node_count} 个相关片段 (耗时 {elapsed_ms}ms)")
    for n in nodes:
        text_preview = (n.get("summary") or n.get("text", ""))[:80]
        log(f"  [{n.get('type')}] [{n.get('confidence')}] {text_preview}...")

    # 提取去重来源文件
    unique_cids = list(set(n.get("contentId", "") for n in nodes))
    files_resp = api_post(f"/api/v1/knowledge/pageQueryContents?collectionId={kb_id}&pageNum=1&pageSize=100")
    source_files = []
    for item in files_resp.get("data", []):
        if item.get("contentId") in unique_cids:
            source_files.append({
                "contentId": item["contentId"],
                "fileName": item.get("fileName"),
                "status": item.get("status"),
            })

    log("来源文件:")
    for f in source_files:
        log(f"  - {f['fileName']}")

    # 步骤 3: 生成（可选）
    creation_id = None
    creation_status = None
    if args.generate and node_count > 0:
        log(f"步骤 3: 基于检索结果生成 {args.output_type}")
        ready_files = [{"contentId": f["contentId"]} for f in source_files if f["status"] == "success"]
        if ready_files:
            creation_id = submit_creation(
                kb_id, args.output_type,
                query=args.gen_query or None,
                preset=args.preset or None,
                files=ready_files,
            )
            creation_status = "submitted" if creation_id else "failed"

            if creation_id and args.poll_creation:
                creation_status = poll_creation(kb_id, creation_id)

    # 步骤 4: 分享（可选）
    share_url = None
    if args.share:
        log("分享知识库...")
        share_resp = api_post("/api/v1/knowledge/shareNotebook", {"collectionId": kb_id})
        share_data = share_resp.get("data")
        if share_data:
            share_url = build_share_url(share_data)
            log(f"分享链接: {share_url}")

    output({
        "collectionId": kb_id,
        "searchQuery": args.query,
        "nodeCount": node_count,
        "nodes": nodes,
        "sourceFiles": source_files,
        "creationId": creation_id,
        "creationStatus": creation_status,
        "shareUrl": share_url,
    })


if __name__ == "__main__":
    main()
