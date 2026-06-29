# -*- coding: utf-8 -*-
"""
save_paper.py — 保存文档到知识库（summary 页 + PDF + catalog + index + log）

用法：
    python3 save_paper.py --open_id ou_xxx \
        --title "论文标题" \
        --summary_file /tmp/paperkb/summary_draft.md \
        --doc_type 论文 \
        --keywords "力控制,强化学习,灵巧手" \
        --score 8 \
        --brief "一句话简介" \
        [--arxiv_id 2401.12345] \
        [--pdf_path /tmp/paperkb/arxiv_2401.12345.pdf] \
        [--text_path /tmp/paperkb/arxiv_2401.12345.txt] \
        [--force]

说明：
    - summary_file：OpenClaw 生成的最终版 summary Markdown，写到临时文件后传入。
    - text_path：用于计算内容指纹存入 catalog（供以后查重）。
    - --force：覆盖模式（catalog 中同 arxiv_id/同标题的条目被替换）。

输出单行 JSON：
    {"success": true, "summary_url": "...", "pdf_url": "...",
     "summary_path": "summaries/xxx.md", "replaced": false}
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import gitea_api as g
import kb_common as kb
import doc_types as dt


def _out(payload: dict) -> None:
    print(json.dumps(payload, ensure_ascii=False))


def _fail(error: str, message: str) -> None:
    _out({"success": False, "error": error, "message": message})
    sys.exit(0)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--open_id", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--summary_file", required=True)
    parser.add_argument("--type_key", default="paper",
                        help="资料类型内部标识：paper/survey/project/doc/experiment/meeting")
    parser.add_argument("--doc_type", default="", help="（可选）中文类型名，留空按 type_key 自动取")
    parser.add_argument("--keywords", default="", help="逗号分隔")
    parser.add_argument("--score", default="", help="相关性评分 1-10")
    parser.add_argument("--brief", default="", help="一句话简介（用于目录）")
    parser.add_argument("--arxiv_id", default="")
    parser.add_argument("--pdf_path", default="")
    parser.add_argument("--text_path", default="")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    user = kb.get_user_by_open_id(args.open_id)
    if user is None:
        _fail("user_not_registered", "该用户尚未注册，请先完成初始化。")
    username = user["gitea_username"]

    summary_src = Path(args.summary_file)
    if not summary_src.exists():
        _fail("summary_file_not_found", f"找不到 summary 文件：{summary_src}")
    summary_content = summary_src.read_text(encoding="utf-8")

    type_key = dt.resolve_type(args.type_key)
    doc_type_cn = args.doc_type.strip() or dt.cn_of(type_key)
    folder = dt.folder_of(type_key)

    fname = kb.build_filename(args.title, type_key)
    summary_path = f"summaries/{folder}/{fname}.md"

    # 1. 上传 summary 页
    try:
        g.put_file(username, kb.REPO_NAME, summary_path, summary_content,
                   f"paper-kb ingest: {fname}")
    except g.GiteaError as exc:
        _fail("upload_summary_failed", f"上传 summary 失败：{exc}")

    # 2. 上传 PDF（可选）
    pdf_url = ""
    if args.pdf_path:
        pdf_src = Path(args.pdf_path)
        if pdf_src.exists():
            pdf_repo_path = f"pdfs/{fname}.pdf"
            try:
                g.put_file_bytes(username, kb.REPO_NAME, pdf_repo_path,
                                 pdf_src.read_bytes(),
                                 f"paper-kb ingest pdf: {fname}")
                pdf_url = f"{g.GITEA_URL}/{username}/{kb.REPO_NAME}/src/branch/main/{pdf_repo_path}"
            except g.GiteaError as exc:
                # PDF 上传失败不阻塞（可能文件过大），在输出中注明
                pdf_url = f"上传失败：{exc}"

    # 3. 内容指纹
    fingerprint = ""
    if args.text_path and Path(args.text_path).exists():
        fingerprint = kb.make_fingerprint(
            Path(args.text_path).read_text(encoding="utf-8", errors="ignore"))

    # 4. 更新 catalog
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    if not dt.is_scored(type_key):
        score = "自有"
    else:
        try:
            score = int(args.score) if args.score else ""
        except ValueError:
            score = ""
    entry = {
        "title": args.title.strip(),
        "file": summary_path,
        "doc_type": doc_type_cn,
        "type_key": type_key,
        "arxiv_id": args.arxiv_id.strip(),
        "keywords": keywords,
        "score": score,
        "brief": args.brief.strip(),
        "fingerprint": fingerprint,
        "created_at": kb.now_str(),
    }
    catalog = kb.read_catalog(username)
    replaced = kb.upsert_document(catalog, entry)
    try:
        kb.write_catalog(username, catalog)
    except g.GiteaError as exc:
        _fail("catalog_failed", f"更新 catalog 失败：{exc}")

    # 5. 重新生成 index.md
    try:
        kb.regen_index(username, user.get("research_direction", ""), catalog)
    except g.GiteaError as exc:
        _fail("index_failed", f"更新 index.md 失败：{exc}")

    # 6. 追加日志（失败不阻塞）
    kb.append_log(username, "ingest", f"{args.doc_type}《{args.title.strip()}》")

    _out({
        "success": True,
        "replaced": replaced,
        "summary_path": summary_path,
        "summary_url": f"{g.GITEA_URL}/{username}/{kb.REPO_NAME}/src/branch/main/{summary_path}",
        "pdf_url": pdf_url,
        "repo_url": f"{g.GITEA_URL}/{username}/{kb.REPO_NAME}",
    })


if __name__ == "__main__":
    main()
