#!/usr/bin/env python3
"""
Pipeline 3: 向已有知识库追加内容 → 等待解析 → 生成

用法:
  python pipeline_import_and_generate.py \
    --kb "竞品分析" --files "/path/to/new.pdf" \
    --urls "https://mp.weixin.qq.com/s/xxx" \
    --output-type PDF --query "总结所有资料"

  python pipeline_import_and_generate.py \
    --kb "项目文档" --text "会议纪要内容..." \
    --text-title "Q1会议纪要" --rename --no-generate
"""
import argparse
import os
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(__file__))
from iflow_common import (
    log, api_post, api_upload, extract_content_id, check_success, find_kb,
    get_file_type, poll_parsing, submit_creation, poll_creation, output,
)


def upload_file(collection_id, filepath):
    filepath = filepath.strip()
    if not os.path.isfile(filepath):
        log(f"文件不存在: {filepath}")
        return None
    ft = get_file_type(filepath)
    log(f"上传: {os.path.basename(filepath)}")
    resp = api_upload(collection_id, file_path=filepath, file_type=ft)
    return extract_content_id(resp) or None


def upload_url(collection_id, url):
    url = url.strip()
    log(f"导入 URL: {url}")
    resp = api_upload(collection_id, url=url, file_type="HTML")
    return extract_content_id(resp) or None


def main():
    parser = argparse.ArgumentParser(description="Pipeline 3: 追加内容并生成")
    parser.add_argument("--kb", default="", help="知识库名称")
    parser.add_argument("--kb-id", default="", help="知识库 ID")
    parser.add_argument("--files", default="", help="本地文件，逗号分隔")
    parser.add_argument("--urls", default="", help="网页 URL，逗号分隔")
    parser.add_argument("--text", default="", help="纯文本内容")
    parser.add_argument("--text-title", default="", help="文本文件名")
    parser.add_argument("--output-type", default="PDF", help="生成类型")
    parser.add_argument("--query", default="", help="创作要求")
    parser.add_argument("--preset", default="", help="PPT 风格")
    parser.add_argument("--use-new-only", action="store_true", help="仅用新文件生成")
    parser.add_argument("--no-generate", action="store_true", help="只导入不生成")
    parser.add_argument("--poll-creation", action="store_true", help="轮询等待创作完成")
    parser.add_argument("--rename", action="store_true", help="文本导入后重命名")
    args = parser.parse_args()

    kb_id = find_kb(args.kb or None, args.kb_id or None)
    log(f"知识库 ID: {kb_id}")

    # 步骤 2: 上传/导入
    new_content_ids = []
    text_cid = None
    futures = []

    with ThreadPoolExecutor(max_workers=5) as pool:
        if args.files:
            for f in args.files.split(","):
                futures.append(pool.submit(upload_file, kb_id, f))
        if args.urls:
            for u in args.urls.split(","):
                futures.append(pool.submit(upload_url, kb_id, u))
        for fut in as_completed(futures):
            cid = fut.result()
            if cid:
                new_content_ids.append(cid)

    # 纯文本导入（同步，因为需要临时文件）
    if args.text:
        log("导入纯文本...")
        fd, tmp_path = tempfile.mkstemp(suffix=".md", prefix="iflow_text_")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(args.text)
            resp = api_upload(kb_id, file_path=tmp_path, file_type="MARKDOWN")
            text_cid = extract_content_id(resp)
            if text_cid:
                new_content_ids.append(text_cid)
                log(f"文本已上传: {text_cid}")
        finally:
            os.unlink(tmp_path)

    log(f"已导入 {len(new_content_ids)} 个内容")

    # 步骤 3: 轮询解析
    if new_content_ids:
        failed_ids = poll_parsing(kb_id, new_content_ids)
        new_content_ids = [cid for cid in new_content_ids if cid not in failed_ids]

        # 文本重命名（仅解析成功时）
        if args.rename and text_cid and args.text_title and text_cid not in failed_ids:
            log(f'重命名文本文件为「{args.text_title}」')
            files_resp = api_post(f"/api/v1/knowledge/pageQueryContents?collectionId={kb_id}&pageNum=1&pageSize=100")
            for item in files_resp.get("data", []):
                if item.get("contentId") == text_cid:
                    ct = item.get("contentType", "")
                    if ct:
                        rename_resp = api_post("/api/v1/knowledge/updateContent2Collection", {
                            "collectionId": kb_id,
                            "contentType": ct,
                            "contentId": text_cid,
                            "removeFlag": False,
                            "extra": {"fileName": f"{args.text_title}.md"},
                        })
                        if not check_success(rename_resp, "重命名"):
                            log("重命名失败，文件将保留临时名称")
                    break

    # 获取文件总数
    total_resp = api_post(f"/api/v1/knowledge/pageQueryContents?collectionId={kb_id}&pageNum=1&pageSize=50")
    total_files = int(total_resp.get("total", 0))

    # 步骤 4: 生成
    creation_id = None
    creation_status = None
    if not args.no_generate and new_content_ids:
        log(f"步骤 4: 提交创作任务 ({args.output_type})")
        files_param = None
        if args.use_new_only:
            files_param = [{"contentId": cid} for cid in new_content_ids]
        creation_id = submit_creation(
            kb_id, args.output_type,
            query=args.query or None,
            preset=args.preset or None,
            files=files_param,
        )
        creation_status = "submitted" if creation_id else "failed"

        if creation_id and args.poll_creation:
            creation_status = poll_creation(kb_id, creation_id)

    output({
        "collectionId": kb_id,
        "newContentIds": new_content_ids,
        "totalFiles": total_files,
        "creationId": creation_id,
        "creationStatus": creation_status,
    })


if __name__ == "__main__":
    main()
