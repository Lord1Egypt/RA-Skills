#!/usr/bin/env python3
"""
Pipeline 1: 端到端 — 创建知识库 → 上传文件 → 等待解析 → 生成内容

用法:
  python pipeline_create_kb_and_generate.py \
    --name "毕业论文参考文献" \
    --files "/path/to/a.pdf,/path/to/b.docx" \
    --urls "https://example.com/article1" \
    --output-type PDF --query "请生成一份文献综述"
"""
import argparse
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(__file__))
from iflow_common import (
    log, api_post, api_upload, extract_content_id, find_kb,
    get_file_type, poll_parsing, submit_creation, poll_creation, output,
)


def upload_file(collection_id, filepath):
    filepath = filepath.strip()
    if not os.path.isfile(filepath):
        log(f"文件不存在: {filepath}")
        return None
    ft = get_file_type(filepath)
    log(f"上传本地文件: {os.path.basename(filepath)} ({ft})")
    resp = api_upload(collection_id, file_path=filepath, file_type=ft)
    cid = extract_content_id(resp)
    if not cid:
        log(f"上传失败 {os.path.basename(filepath)}: {resp.get('message', '未知错误')}")
    return cid


def upload_url(collection_id, url):
    url = url.strip()
    log(f"导入 URL: {url}")
    resp = api_upload(collection_id, url=url, file_type="HTML")
    cid = extract_content_id(resp)
    if not cid:
        log(f"导入失败 {url}: {resp.get('message', '未知错误')}")
    return cid


def main():
    parser = argparse.ArgumentParser(description="Pipeline 1: 创建知识库并生成内容")
    parser.add_argument("--name", required=True, help="知识库名称")
    parser.add_argument("--description", default="", help="知识库描述")
    parser.add_argument("--files", default="", help="本地文件路径，逗号分隔")
    parser.add_argument("--urls", default="", help="网页 URL，逗号分隔")
    parser.add_argument("--output-type", default="PDF", help="生成类型")
    parser.add_argument("--query", default="", help="创作要求")
    parser.add_argument("--preset", default="", help="PPT 风格")
    parser.add_argument("--no-generate", action="store_true", help="只建库+上传")
    parser.add_argument("--poll-creation", action="store_true", help="轮询等待创作完成")
    args = parser.parse_args()

    desc = args.description or args.name

    # 步骤 1: 创建知识库
    log(f'步骤 1: 创建知识库「{args.name}」')
    resp = api_post("/api/v1/knowledge/saveCollection",
                    {"collectionName": args.name, "description": desc})
    collection_id = resp.get("data")
    if not collection_id:
        log(f"创建知识库失败: {resp.get('message', '未知错误')}")
        sys.exit(1)
    log(f"知识库已创建: {collection_id}")

    # 步骤 2: 并行上传
    content_ids = []
    futures = []
    with ThreadPoolExecutor(max_workers=5) as pool:
        if args.files:
            for f in args.files.split(","):
                futures.append(pool.submit(upload_file, collection_id, f))
        if args.urls:
            for u in args.urls.split(","):
                futures.append(pool.submit(upload_url, collection_id, u))
        for fut in as_completed(futures):
            cid = fut.result()
            if cid:
                content_ids.append(cid)

    log(f"已上传 {len(content_ids)} 个文件")

    if not content_ids:
        output({"collectionId": collection_id, "contentIds": [],
                "creationId": None, "creationStatus": None})
        return

    # 步骤 3: 轮询解析
    failed_ids = poll_parsing(collection_id, content_ids)
    content_ids = [cid for cid in content_ids if cid not in failed_ids]

    # 步骤 4: 生成
    creation_id = None
    creation_status = None
    if not args.no_generate and not content_ids:
        log("所有文件解析失败，跳过生成")
        creation_status = "skipped_no_content"
    elif not args.no_generate:
        log(f"步骤 4: 提交创作任务 ({args.output_type})")
        creation_id = submit_creation(
            collection_id, args.output_type,
            query=args.query or None,
            preset=args.preset or None,
        )
        creation_status = "submitted" if creation_id else "failed"

        if creation_id and args.poll_creation:
            creation_status = poll_creation(collection_id, creation_id)

    output({
        "collectionId": collection_id,
        "contentIds": content_ids,
        "creationId": creation_id,
        "creationStatus": creation_status,
    })


if __name__ == "__main__":
    main()
