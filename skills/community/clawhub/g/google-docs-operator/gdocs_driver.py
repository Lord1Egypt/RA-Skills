#!/usr/bin/env python3
"""
gdocs_driver.py — Google Docs CLI via Maton API

通过 Maton API 网关调用 Google Docs REST API，无需本地 Chrome 或 OAuth 配置。

环境变量：
  MATON_API_KEY   — 必须，从 https://maton.ai/settings 获取

支持命令：
  get       读取文档内容（提取纯文本）
  create    创建新文档
  append    追加文本到文档末尾
  write     覆盖全文（清空后写入）
  replace   搜索并替换文本
  heading   将指定文本设为标题（H1~H6）
  bold      将指定文本设为粗体
  export    导出为 PDF / DOCX / TXT（通过 Google Drive API）

用法示例：
  export MATON_API_KEY="your_key"
  python3 gdocs_driver.py create --title "新文档"
  python3 gdocs_driver.py get --id DOCUMENT_ID
  python3 gdocs_driver.py append --id DOCUMENT_ID --content "追加内容"
  python3 gdocs_driver.py replace --id DOCUMENT_ID --find "旧词" --replace "新词"
  python3 gdocs_driver.py heading --id DOCUMENT_ID --text "章节标题" --level 1
  python3 gdocs_driver.py export --id DOCUMENT_ID --format pdf --output /tmp/out.pdf
"""

import argparse
import json
import os
import sys
import re

import requests
try:
    import certifi
    _SSL_VERIFY = certifi.where()
except ImportError:
    _SSL_VERIFY = True

# ─────────────────────── 配置 ───────────────────────

MATON_API_KEY = os.environ.get("MATON_API_KEY", "")
GATEWAY_BASE = "https://gateway.maton.ai/google-docs/v1/documents"
CTRL_BASE = "https://ctrl.maton.ai"

HEADING_STYLES = {
    0: "NORMAL_TEXT",
    1: "HEADING_1",
    2: "HEADING_2",
    3: "HEADING_3",
    4: "HEADING_4",
    5: "HEADING_5",
    6: "HEADING_6",
}

# ─────────────────────── HTTP 辅助 ───────────────────────


def _headers(connection_id: str = None) -> dict:
    if not MATON_API_KEY:
        print("❌ 未设置 MATON_API_KEY 环境变量", file=sys.stderr)
        print("   请运行: export MATON_API_KEY='your_key'", file=sys.stderr)
        sys.exit(1)
    h = {
        "Authorization": f"Bearer {MATON_API_KEY}",
        "Content-Type": "application/json",
    }
    if connection_id:
        h["Maton-Connection"] = connection_id
    return h


def _get(path: str, connection_id: str = None) -> dict:
    url = f"{GATEWAY_BASE}{path}"
    resp = requests.get(url, headers=_headers(connection_id), verify=_SSL_VERIFY)
    resp.raise_for_status()
    return resp.json()


def _post(path: str, body: dict, connection_id: str = None) -> dict:
    url = f"{GATEWAY_BASE}{path}"
    resp = requests.post(url, headers=_headers(connection_id), json=body, verify=_SSL_VERIFY)
    resp.raise_for_status()
    return resp.json()


def _get_bytes(path: str, connection_id: str = None) -> bytes:
    url = f"{GATEWAY_BASE}{path}"
    resp = requests.get(url, headers=_headers(connection_id), verify=_SSL_VERIFY)
    resp.raise_for_status()
    return resp.content


def extract_doc_id(url_or_id: str) -> str:
    """从 URL 或直接 ID 中提取文档 ID。"""
    m = re.search(r"/document/d/([a-zA-Z0-9_-]+)", url_or_id)
    if m:
        return m.group(1)
    # 如果已经是纯 ID
    if re.match(r"^[a-zA-Z0-9_-]+$", url_or_id):
        return url_or_id
    raise ValueError(f"无法解析文档 ID: {url_or_id}")


# ─────────────────────── 连接管理 ───────────────────────


def list_connections():
    """列出所有 Google Docs 连接。"""
    resp = requests.get(
        f"{CTRL_BASE}/connections?app=google-docs&status=ACTIVE",
        headers={"Authorization": f"Bearer {MATON_API_KEY}"},
        verify=_SSL_VERIFY,
    )
    resp.raise_for_status()
    return resp.json()


def create_connection():
    """创建新的 Google Docs OAuth 连接，返回授权 URL。"""
    resp = requests.post(
        f"{CTRL_BASE}/connections",
        headers={
            "Authorization": f"Bearer {MATON_API_KEY}",
            "Content-Type": "application/json",
        },
        json={"app": "google-docs"},
        verify=_SSL_VERIFY,
    )
    resp.raise_for_status()
    return resp.json()


# ─────────────────────── 文档操作 ───────────────────────


def cmd_get(args):
    """读取文档内容，提取纯文本。"""
    doc_id = extract_doc_id(args.id)
    data = _get(f"/{doc_id}", args.connection)

    # 从 Document 结构中提取纯文本
    text_parts = []
    for elem in data.get("body", {}).get("content", []):
        para = elem.get("paragraph")
        if not para:
            # 可能是 sectionBreak / tableOfContents 等，跳过
            continue
        for pe in para.get("elements", []):
            tr = pe.get("textRun")
            if tr:
                text_parts.append(tr.get("content", ""))

    full_text = "".join(text_parts)

    result = {
        "documentId": data.get("documentId"),
        "title": data.get("title"),
        "content": full_text,
        "char_count": len(full_text),
        "revision": data.get("revisionId"),
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_create(args):
    """创建新文档。"""
    body = {"title": args.title or ""}
    data = _post("", body, args.connection)
    result = {
        "documentId": data.get("documentId"),
        "title": data.get("title"),
        "url": f"https://docs.google.com/document/d/{data.get('documentId')}/edit",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


def cmd_append(args):
    """追加文本到文档末尾。"""
    doc_id = extract_doc_id(args.id)

    # 先获取文档以取得末尾 index
    doc = _get(f"/{doc_id}", args.connection)
    content = doc.get("body", {}).get("content", [])
    # 末尾 index（最后一个 endIndex 之前一位，避免在段落结束符后插入）
    end_index = content[-1].get("endIndex", 1) - 1 if content else 1

    # 读取内容（支持 --file）
    text = args.content or ""
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    text = text.replace("\\n", "\n")

    requests_body = {
        "requests": [
            {
                "insertText": {
                    "location": {"index": end_index},
                    "text": text,
                }
            }
        ]
    }
    _post(f"/{doc_id}:batchUpdate", requests_body, args.connection)
    print(json.dumps({"status": "ok", "action": "append", "chars": len(text)}, ensure_ascii=False, indent=2))


def cmd_write(args):
    """覆盖全文内容（先删除再写入）。"""
    doc_id = extract_doc_id(args.id)

    # 读取内容
    text = args.content or ""
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    text = text.replace("\\n", "\n")

    # 先获取当前文档内容范围
    doc = _get(f"/{doc_id}", args.connection)
    content = doc.get("body", {}).get("content", [])
    end_index = content[-1].get("endIndex", 1) if content else 1

    # 构建批量请求：先删除全部现有内容（从 index 1 到 endIndex-1），再插入新内容
    batch_requests = []

    # 只有文档有内容才需要删除
    if end_index > 2:
        batch_requests.append({
            "deleteContentRange": {
                "range": {
                    "startIndex": 1,
                    "endIndex": end_index - 1,
                }
            }
        })

    # 插入新内容
    batch_requests.append({
        "insertText": {
            "location": {"index": 1},
            "text": text,
        }
    })

    _post(f"/{doc_id}:batchUpdate", {"requests": batch_requests}, args.connection)
    print(json.dumps({"status": "ok", "action": "write", "chars": len(text)}, ensure_ascii=False, indent=2))


def cmd_replace(args):
    """搜索并替换所有匹配文本。"""
    doc_id = extract_doc_id(args.id)
    requests_body = {
        "requests": [
            {
                "replaceAllText": {
                    "containsText": {
                        "text": args.find,
                        "matchCase": not args.ignore_case,
                    },
                    "replaceText": args.replace_with,
                }
            }
        ]
    }
    data = _post(f"/{doc_id}:batchUpdate", requests_body, args.connection)
    # 提取替换次数
    replies = data.get("replies", [{}])
    occurrences = replies[0].get("replaceAllText", {}).get("occurrencesChanged", 0)
    print(json.dumps({
        "status": "ok",
        "action": "replace",
        "find": args.find,
        "replace": args.replace_with,
        "occurrences_changed": occurrences,
    }, ensure_ascii=False, indent=2))


def cmd_heading(args):
    """将指定文本的第一个匹配段落设为标题样式。"""
    doc_id = extract_doc_id(args.id)

    level = args.level
    if level < 0 or level > 6:
        print("❌ --level 必须在 0（正文）~ 6 之间", file=sys.stderr)
        sys.exit(1)
    style_name = HEADING_STYLES[level]

    # 先读取文档，找到目标文本的段落范围
    doc = _get(f"/{doc_id}", args.connection)
    target_range = _find_paragraph_range(doc, args.text)
    if not target_range:
        print(f"❌ 未在文档中找到段落: {args.text!r}", file=sys.stderr)
        sys.exit(1)

    requests_body = {
        "requests": [
            {
                "updateParagraphStyle": {
                    "range": target_range,
                    "paragraphStyle": {"namedStyleType": style_name},
                    "fields": "namedStyleType",
                }
            }
        ]
    }
    _post(f"/{doc_id}:batchUpdate", requests_body, args.connection)
    print(json.dumps({
        "status": "ok",
        "action": "heading",
        "text": args.text,
        "style": style_name,
        "range": target_range,
    }, ensure_ascii=False, indent=2))


def cmd_bold(args):
    """将指定文本范围设为粗体。"""
    doc_id = extract_doc_id(args.id)

    # 先读取文档，找到目标文本的字符范围
    doc = _get(f"/{doc_id}", args.connection)
    text_range = _find_text_range(doc, args.text)
    if not text_range:
        print(f"❌ 未在文档中找到文本: {args.text!r}", file=sys.stderr)
        sys.exit(1)

    requests_body = {
        "requests": [
            {
                "updateTextStyle": {
                    "range": text_range,
                    "textStyle": {"bold": True},
                    "fields": "bold",
                }
            }
        ]
    }
    _post(f"/{doc_id}:batchUpdate", requests_body, args.connection)
    print(json.dumps({
        "status": "ok",
        "action": "bold",
        "text": args.text,
        "range": text_range,
    }, ensure_ascii=False, indent=2))


def cmd_export(args):
    """通过 Google Drive 导出文档（PDF / DOCX / TXT 等）。"""
    doc_id = extract_doc_id(args.id)

    fmt_map = {
        "pdf": "application/pdf",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "doc": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "txt": "text/plain",
        "html": "text/html",
        "odt": "application/vnd.oasis.opendocument.text",
        "rtf": "application/rtf",
        "epub": "application/epub+zip",
    }
    mime = fmt_map.get(args.format.lower())
    if not mime:
        print(f"❌ 不支持的格式: {args.format}，可选: {list(fmt_map.keys())}", file=sys.stderr)
        sys.exit(1)

    # Google Drive 导出接口（Maton 也代理 google-drive）
    export_url = (
        f"https://gateway.maton.ai/google-drive/drive/v3/files/{doc_id}/export"
        f"?mimeType={mime}"
    )
    import urllib.parse
    export_url = (
        f"https://gateway.maton.ai/google-drive/drive/v3/files/{doc_id}/export"
        f"?mimeType={urllib.parse.quote(mime)}"
    )

    resp = requests.get(
        export_url,
        headers={"Authorization": f"Bearer {MATON_API_KEY}"},
        verify=_SSL_VERIFY,
    )
    if resp.status_code != 200:
        print(f"❌ 导出失败 (HTTP {resp.status_code}): {resp.text}", file=sys.stderr)
        sys.exit(1)

    output_path = os.path.abspath(args.output)
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(resp.content)

    print(json.dumps({
        "status": "ok",
        "action": "export",
        "format": args.format,
        "output": output_path,
        "size_bytes": len(resp.content),
    }, ensure_ascii=False, indent=2))


def cmd_connections(args):
    """管理 Maton 连接。"""
    if args.action == "list":
        data = list_connections()
        print(json.dumps(data, ensure_ascii=False, indent=2))
    elif args.action == "create":
        data = create_connection()
        print(json.dumps(data, ensure_ascii=False, indent=2))
        url = data.get("connection", {}).get("url")
        if url:
            print(f"\n🔗 请在浏览器中打开以下链接完成 Google 授权：\n{url}", file=sys.stderr)


# ─────────────────────── 内部辅助 ───────────────────────


def _find_paragraph_range(doc: dict, text: str) -> dict | None:
    """在文档中找到包含指定文本的第一个段落范围。"""
    for elem in doc.get("body", {}).get("content", []):
        para = elem.get("paragraph")
        if not para:
            continue
        para_text = "".join(
            pe.get("textRun", {}).get("content", "")
            for pe in para.get("elements", [])
        )
        if text in para_text:
            return {
                "startIndex": elem.get("startIndex", 0),
                "endIndex": elem.get("endIndex", 0),
            }
    return None


def _find_text_range(doc: dict, text: str) -> dict | None:
    """在文档中找到指定文本的字符级范围（第一次匹配）。"""
    for elem in doc.get("body", {}).get("content", []):
        para = elem.get("paragraph")
        if not para:
            continue
        for pe in para.get("elements", []):
            tr = pe.get("textRun", {})
            content = tr.get("content", "")
            if text in content:
                offset = content.index(text)
                start = pe.get("startIndex", 0) + offset
                return {
                    "startIndex": start,
                    "endIndex": start + len(text),
                }
    return None


# ─────────────────────── CLI 入口 ───────────────────────


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Google Docs CLI via Maton API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--connection", default=None, metavar="CONNECTION_ID",
                        help="指定 Maton 连接 ID（多账号时使用）")
    sub = parser.add_subparsers(dest="command", required=True)

    # connections
    p_conn = sub.add_parser("connections", help="管理 Maton Google 连接")
    p_conn.add_argument("action", choices=["list", "create"], help="list=列出连接 create=新建连接")

    # get
    p_get = sub.add_parser("get", help="读取文档内容")
    p_get.add_argument("--id", required=True, help="文档 ID 或完整 URL")

    # create
    p_create = sub.add_parser("create", help="创建新文档")
    p_create.add_argument("--title", default="", help="文档标题")

    # append
    p_append = sub.add_parser("append", help="追加文本到文档末尾")
    p_append.add_argument("--id", required=True, help="文档 ID 或完整 URL")
    p_append.add_argument("--content", default="", help="追加内容（\\n 表示换行）")
    p_append.add_argument("--file", default=None, help="从文件读取内容（优先于 --content）")

    # write
    p_write = sub.add_parser("write", help="覆盖全文内容")
    p_write.add_argument("--id", required=True, help="文档 ID 或完整 URL")
    p_write.add_argument("--content", default="", help="新内容（\\n 表示换行）")
    p_write.add_argument("--file", default=None, help="从文件读取内容（优先于 --content）")

    # replace
    p_replace = sub.add_parser("replace", help="搜索并替换文本（全部匹配）")
    p_replace.add_argument("--id", required=True, help="文档 ID 或完整 URL")
    p_replace.add_argument("--find", required=True, help="要查找的文本")
    p_replace.add_argument("--replace", dest="replace_with", required=True, help="替换为的文本")
    p_replace.add_argument("--ignore-case", action="store_true", help="忽略大小写")

    # heading
    p_heading = sub.add_parser("heading", help="将段落设为标题样式（0=正文, 1~6=H1~H6）")
    p_heading.add_argument("--id", required=True, help="文档 ID 或完整 URL")
    p_heading.add_argument("--text", required=True, help="目标段落文本（精确匹配）")
    p_heading.add_argument("--level", type=int, required=True, choices=range(7),
                           help="标题级别 0=正文 1=H1 2=H2 ... 6=H6")

    # bold
    p_bold = sub.add_parser("bold", help="将指定文本设为粗体")
    p_bold.add_argument("--id", required=True, help="文档 ID 或完整 URL")
    p_bold.add_argument("--text", required=True, help="要加粗的文本（第一次匹配）")

    # export
    p_export = sub.add_parser("export", help="导出为 PDF/DOCX/TXT 等")
    p_export.add_argument("--id", required=True, help="文档 ID 或完整 URL")
    p_export.add_argument("--format", default="pdf",
                          choices=["pdf", "docx", "doc", "txt", "html", "odt", "rtf", "epub"],
                          help="导出格式，默认 pdf")
    p_export.add_argument("--output", required=True, help="输出文件路径")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        dispatch = {
            "connections": cmd_connections,
            "get": cmd_get,
            "create": cmd_create,
            "append": cmd_append,
            "write": cmd_write,
            "replace": cmd_replace,
            "heading": cmd_heading,
            "bold": cmd_bold,
            "export": cmd_export,
        }
        dispatch[args.command](args)
    except requests.HTTPError as e:
        print(f"❌ HTTP 错误: {e.response.status_code} — {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"❌ 错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
