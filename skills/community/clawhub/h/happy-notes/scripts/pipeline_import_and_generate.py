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
    upload_file, upload_url,
    poll_parsing, submit_creation, poll_creation, output,
    validate_output_type, validate_preset, validate_files, validate_urls,
    create_kb,
)


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
    parser.add_argument("--create-if-missing", action="store_true",
                        help="知识库不存在时自动创建（用 --kb 的值作为名称）")
    args = parser.parse_args()

    # 参数校验
    args.output_type = validate_output_type(args.output_type)
    validate_preset(args.preset, args.output_type)
    file_list = validate_files(args.files.split(",")) if args.files else []
    url_list = validate_urls(args.urls.split(",")) if args.urls else []
    if not file_list and not url_list and not args.text:
        log("--files、--urls 或 --text 至少提供一个")
        sys.exit(1)

    # 短文本 + 无其他文件 + 未禁止生成 → 警告（大概率用户只想记录，不需要生成报告）
    if args.text and not file_list and not url_list and not args.no_generate and len(args.text) < 200:
        log("警告: 仅有短文本内容且未指定 --no-generate，将尝试生成报告。如仅需记录文本，建议加 --no-generate")

    # 查找知识库，--create-if-missing 时找不到自动创建
    kb_created = False
    if args.create_if_missing:
        kb_id = find_kb(args.kb or None, args.kb_id or None, exit_on_missing=False)
        if kb_id is None:
            if not args.kb:
                log("--create-if-missing 需要 --kb 提供知识库名称")
                sys.exit(1)
            kb_id = create_kb(args.kb)
            kb_created = True
    else:
        kb_id = find_kb(args.kb or None, args.kb_id or None)
    log(f"知识库 ID: {kb_id}")

    # 步骤 2: 上传/导入
    new_content_ids = []
    failed_uploads = []
    text_cid = None
    futures = {}

    with ThreadPoolExecutor(max_workers=5) as pool:
        for f in file_list:
            fut = pool.submit(upload_file, kb_id, f)
            futures[fut] = f
        for u in url_list:
            fut = pool.submit(upload_url, kb_id, u)
            futures[fut] = u
        for fut in as_completed(futures):
            source = futures[fut]
            try:
                cid = fut.result()
            except Exception as e:
                log(f"上传异常: {source} — {e}")
                failed_uploads.append({"source": source, "error": str(e)})
                continue
            if cid:
                new_content_ids.append(cid)
            else:
                failed_uploads.append({"source": source, "error": "上传返回空 contentId"})

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
            else:
                failed_uploads.append({"source": "(文本导入)", "error": "上传返回空 contentId"})
        finally:
            os.unlink(tmp_path)

    if failed_uploads:
        log(f"已导入 {len(new_content_ids)} 个内容, {len(failed_uploads)} 个失败")
    else:
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
                            "extra": {"fileName": args.text_title if args.text_title.endswith(".md") else f"{args.text_title}.md"},
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

    result = {
        "collectionId": kb_id,
        "contentIds": new_content_ids,
        "totalFiles": total_files,
        "creationId": creation_id,
        "creationStatus": creation_status,
    }
    if kb_created:
        result["kbCreated"] = True
        result["kbName"] = args.kb
    if failed_uploads:
        result["failedCount"] = len(failed_uploads)
        result["failedItems"] = failed_uploads
    output(result)


if __name__ == "__main__":
    main()
