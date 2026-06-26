#!/usr/bin/env python3
"""
Pipeline 6: 联网搜索 → 导入知识库 → 等待解析 → 生成内容

支持快速搜索(FAST_SEARCH)和深度研究(DEEP_RESEARCH)，数据源分为全网(WEB)和学术(SCHOLAR)。

用法:
  # 快速搜索网页，导入知识库并生成报告
  python pipeline_web_search.py \
    --kb "AI研究" --query "大模型 Agent" --source WEB --output-type PDF

  # 快速搜索学术论文，导入知识库，不生成
  python pipeline_web_search.py \
    --kb "论文集" --query "transformer attention" --source SCHOLAR --no-generate

  # 深度研究，导入报告到知识库
  python pipeline_web_search.py \
    --kb "AI研究" --query "大模型最新进展" --type DEEP_RESEARCH --source WEB

  # 只搜索，不导入不生成
  python pipeline_web_search.py \
    --kb "AI研究" --query "AI Agent" --search-only
"""
import argparse
import os
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

sys.path.insert(0, os.path.dirname(__file__))
from iflow_common import (
    log, api_upload, extract_content_id, find_kb,
    poll_parsing, submit_creation, poll_creation,
    start_search, poll_search, output,
)


def import_url(collection_id, url, content_type="WEBSITE"):
    """导入搜索结果 URL 到知识库"""
    url = url.strip()
    if content_type == "PAPER" and "arxiv.org/pdf/" in url:
        # arxiv PDF URL 转为摘要页（可被网页抓取）: arxiv.org/pdf/xxx → arxiv.org/abs/xxx
        url = url.replace("arxiv.org/pdf/", "arxiv.org/abs/")
    log(f"导入: {url[:80]}")
    resp = api_upload(collection_id, url=url, file_type="HTML")
    return extract_content_id(resp) or None


def import_report(collection_id, report_url):
    """下载 REPORT 的 .md 文件并上传到知识库"""
    log(f"下载报告: {report_url[:80]}")
    try:
        r = requests.get(report_url, timeout=(10, 60))
        r.raise_for_status()
        content = r.text
    except Exception as e:
        log(f"下载报告失败: {e}")
        return None

    fd, tmp_path = tempfile.mkstemp(suffix=".md", prefix="iflow_report_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(content)
        resp = api_upload(collection_id, file_path=tmp_path, file_type="MARKDOWN")
        cid = extract_content_id(resp)
        if cid:
            log(f"报告已导入: {cid}")
        return cid
    finally:
        os.unlink(tmp_path)


def main():
    parser = argparse.ArgumentParser(description="Pipeline 6: 联网搜索 → 导入 → 生成")
    parser.add_argument("--kb", default="", help="知识库名称")
    parser.add_argument("--kb-id", default="", help="知识库 ID")
    parser.add_argument("--query", required=True, help="搜索关键词")
    parser.add_argument("--type", default="FAST_SEARCH", choices=["FAST_SEARCH", "DEEP_RESEARCH"],
                        help="搜索类型 (默认 FAST_SEARCH)")
    parser.add_argument("--source", default="WEB", choices=["WEB", "SCHOLAR"],
                        help="数据源 (默认 WEB)")
    parser.add_argument("--max-results", type=int, default=0, help="限制导入结果数量 (0=全部)")
    parser.add_argument("--output-type", default="PDF", help="生成类型: PDF/DOCX/MARKDOWN/PPT/XMIND/PODCAST/VIDEO")
    parser.add_argument("--creation-query", default="", help="生成内容的 prompt")
    parser.add_argument("--preset", default="", help="PPT 风格预设")
    parser.add_argument("--no-generate", action="store_true", help="只搜索+导入，不生成内容")
    parser.add_argument("--search-only", action="store_true", help="只搜索，不导入也不生成")
    parser.add_argument("--poll-creation", action="store_true", help="等待生成完成")
    args = parser.parse_args()

    search_type = args.type
    source = args.source

    # 步骤 1: 查找知识库
    log("步骤 1: 查找知识库")
    kb_id = find_kb(args.kb or None, args.kb_id or None)
    log(f"知识库 ID: {kb_id}")

    # 步骤 2: 发起搜索
    log(f"步骤 2: 发起搜索 ({search_type} + {source})")
    search_id = start_search(kb_id, args.query, search_type, source)
    if not search_id:
        output({"error": "搜索发起失败", "collectionId": kb_id})
        sys.exit(1)

    # 步骤 3: 轮询搜索结果
    log("步骤 3: 等待搜索结果")
    if search_type == "DEEP_RESEARCH":
        max_wait, interval = 600, 10
    else:
        max_wait, interval = 60, 3
    search_data = poll_search(kb_id, search_id, max_wait=max_wait, interval=interval)

    if not search_data or search_data.get("status") != "completed":
        output({
            "error": "搜索未完成",
            "collectionId": kb_id,
            "searchId": search_id,
            "searchStatus": (search_data or {}).get("status", "timeout"),
        })
        sys.exit(1)

    # 提取搜索结果
    results = search_data.get("results", [])
    result_count = len(results)
    log(f"搜索返回 {result_count} 条结果")

    # 分类结果
    report_url = None
    importable_results = []
    for item in results:
        ct = item.get("contentType", "")
        if ct == "REPORT":
            report_url = item.get("url", "")
        else:
            importable_results.append(item)

    # 限制数量
    if args.max_results > 0:
        importable_results = importable_results[:args.max_results]

    # 搜索结果摘要输出
    result_summary = []
    for item in results:
        entry = {
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "contentType": item.get("contentType", ""),
        }
        if item.get("score") is not None:
            entry["score"] = item["score"]
        result_summary.append(entry)

    # --search-only: 只输出结果，不导入
    if args.search_only:
        output({
            "collectionId": kb_id,
            "searchId": search_id,
            "searchType": search_type,
            "source": source,
            "searchStatus": "completed",
            "resultCount": result_count,
            "results": result_summary,
            "reportUrl": report_url,
        })
        return

    # 步骤 4: 导入知识库
    log(f"步骤 4: 导入搜索结果到知识库 ({len(importable_results)} 个网页/论文"
        + (", 1 份报告" if report_url else "") + ")")
    content_ids = []

    # 并行导入网页/论文 URL
    fail_count = 0
    if importable_results:
        with ThreadPoolExecutor(max_workers=5) as pool:
            futures = {}
            for item in importable_results:
                url = item.get("url", "")
                ct = item.get("contentType", "WEBSITE")
                if url:
                    fut = pool.submit(import_url, kb_id, url, ct)
                    futures[fut] = url
            for fut in as_completed(futures):
                try:
                    cid = fut.result()
                except Exception as e:
                    log(f"导入异常: {e}")
                    fail_count += 1
                    continue
                if cid:
                    content_ids.append(cid)
                else:
                    fail_count += 1

    # 导入报告（同步，需要下载）
    if report_url:
        cid = import_report(kb_id, report_url)
        if cid:
            content_ids.append(cid)

    if fail_count:
        log(f"成功导入 {len(content_ids)} 个内容, {fail_count} 个失败")
    else:
        log(f"成功导入 {len(content_ids)} 个内容")

    # 步骤 5: 轮询解析
    if content_ids:
        log("步骤 5: 等待文件解析")
        failed_ids = poll_parsing(kb_id, content_ids)
        content_ids = [cid for cid in content_ids if cid not in failed_ids]

    # 步骤 6: 生成内容
    creation_id = None
    creation_status = None
    if not args.no_generate and not content_ids:
        log("所有内容导入失败，无法生成")
        creation_status = "skipped_no_content"
    elif not args.no_generate and content_ids:
        log(f"步骤 6: 提交创作任务 ({args.output_type})")
        cq = args.creation_query or f"请基于搜索到的关于「{args.query}」的资料，撰写一份全面的分析报告。"
        creation_id = submit_creation(
            kb_id, args.output_type,
            query=cq,
            preset=args.preset or None,
            files=[{"contentId": cid} for cid in content_ids],
        )
        creation_status = "submitted" if creation_id else "failed"

        if args.poll_creation and creation_id:
            log("等待创作完成...")
            creation_status = poll_creation(kb_id, creation_id)

    output({
        "collectionId": kb_id,
        "searchId": search_id,
        "searchType": search_type,
        "source": source,
        "searchStatus": "completed",
        "resultCount": result_count,
        "results": result_summary,
        "reportUrl": report_url,
        "importedContentIds": content_ids,
        "creationId": creation_id,
        "creationStatus": creation_status,
    })


if __name__ == "__main__":
    main()
