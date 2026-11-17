#!/usr/bin/env python3
"""
OpenClaw Skill 脚本：调用个人知识库 API

用法:
    python kb_api.py search "查询内容"              # 搜索文档
    python kb_api.py search_answer "查询内容"        # 搜索并获取 AI 整理答案
    python kb_api.py list                            # 列出所有文档
    python kb_api.py detail "document_id"            # 查看文档详情
    python kb_api.py upload "/path/to/file" "标题"   # 上传文件
    python kb_api.py create "标题" "文本内容"         # 创建纯文本文档

环境变量:
    KB_API_BASE: 知识库 API 地址 (默认: http://127.0.0.1:8080)
"""
import sys
import os
import json
import urllib.request
import urllib.error
import urllib.parse

API_BASE = os.getenv("KB_API_BASE", "http://127.0.0.1:8080")
API_PREFIX = f"{API_BASE}/api/v1"


def _post_json(url, payload, timeout=30):
    """发送 POST JSON 请求"""
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _get_json(url, timeout=15):
    """发送 GET 请求"""
    req = urllib.request.Request(url, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def search_documents(query, limit=5, score_threshold=0.7):
    """搜索知识库文档"""
    data = _post_json(
        f"{API_PREFIX}/documents/search",
        {"query": query, "limit": limit, "score_threshold": score_threshold},
        timeout=30,
    )
    results = data.get("results", [])
    return {
        "total": data.get("total", len(results)),
        "took": data.get("took"),
        "results": [
            {
                "title": r.get("title", ""),
                "content": r.get("content", "")[:500],
                "score": r.get("score"),
                "document_id": r.get("document_id"),
            }
            for r in results
        ],
    }


def search_with_answer(query, limit=5, score_threshold=0.7):
    """搜索知识库并获取 AI 整理答案"""
    data = _post_json(
        f"{API_PREFIX}/documents/search/answer",
        {"query": query, "limit": limit, "score_threshold": score_threshold},
        timeout=60,
    )
    results = data.get("results", [])
    return {
        "query": data.get("query", query),
        "answer": data.get("answer", ""),
        "total": data.get("total", len(results)),
        "sources": [
            {
                "title": r.get("title", ""),
                "score": r.get("score"),
                "content_preview": r.get("content", "")[:200],
            }
            for r in results
        ],
    }


def list_documents(limit=50):
    """列出所有文档"""
    data = _get_json(f"{API_PREFIX}/documents/?limit={limit}")
    documents = data.get("documents", data) if isinstance(data, dict) else data
    return {
        "total": data.get("total", len(documents)) if isinstance(data, dict) else len(documents),
        "documents": [
            {
                "document_id": d.get("document_id"),
                "title": d.get("title", ""),
                "file_type": d.get("file_type"),
                "created_at": d.get("created_at"),
                "tags": d.get("tags", []),
            }
            for d in documents
        ],
    }


def get_document_detail(document_id):
    """获取文档详情"""
    data = _get_json(f"{API_PREFIX}/documents/{document_id}")
    return {
        "document_id": data.get("document_id"),
        "title": data.get("title", ""),
        "content": data.get("content", ""),
        "file_type": data.get("file_type"),
        "created_at": data.get("created_at"),
        "tags": data.get("tags", []),
    }


def upload_file(file_path, title):
    """上传文件到知识库（支持 .txt .pdf .docx .md）"""
    import mimetypes
    import uuid

    file_path = os.path.expanduser(file_path)
    if not os.path.isfile(file_path):
        return {"error": f"文件不存在: {file_path}"}

    filename = os.path.basename(file_path)
    content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"

    with open(file_path, "rb") as f:
        file_data = f.read()

    # 构造 multipart/form-data
    boundary = uuid.uuid4().hex
    parts = []

    # file 字段
    parts.append(f"--{boundary}\r\n".encode())
    parts.append(f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'.encode())
    parts.append(f"Content-Type: {content_type}\r\n\r\n".encode())
    parts.append(file_data)
    parts.append(b"\r\n")

    # title 字段
    parts.append(f"--{boundary}\r\n".encode())
    parts.append(b'Content-Disposition: form-data; name="title"\r\n\r\n')
    parts.append(title.encode("utf-8"))
    parts.append(b"\r\n")

    parts.append(f"--{boundary}--\r\n".encode())

    body = b"".join(parts)

    req = urllib.request.Request(
        f"{API_PREFIX}/documents/upload",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    return {
        "status": "success",
        "document_id": data.get("document_id"),
        "title": data.get("title", ""),
        "file_type": data.get("file_type"),
        "message": f"文件 '{filename}' 已成功上传到知识库",
    }


def create_text_document(title, content):
    """创建纯文本文档"""
    data = _post_json(
        f"{API_PREFIX}/documents/create",
        {"title": title, "content": content, "file_type": "text", "tags": [], "metadata": {}},
        timeout=30,
    )
    return {
        "status": "success",
        "document_id": data.get("document_id"),
        "title": data.get("title", ""),
        "message": f"文档 '{title}' 已成功创建",
    }


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "用法: kb_api.py <command> [args]"}, ensure_ascii=False))
        sys.exit(1)

    command = sys.argv[1].lower()

    try:
        if command == "search":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "search 需要查询参数"}, ensure_ascii=False))
                sys.exit(1)
            result = search_documents(sys.argv[2])

        elif command == "search_answer":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "search_answer 需要查询参数"}, ensure_ascii=False))
                sys.exit(1)
            result = search_with_answer(sys.argv[2])

        elif command == "list":
            result = list_documents()

        elif command == "detail":
            if len(sys.argv) < 3:
                print(json.dumps({"error": "detail 需要 document_id 参数"}, ensure_ascii=False))
                sys.exit(1)
            result = get_document_detail(sys.argv[2])

        elif command == "upload":
            if len(sys.argv) < 4:
                print(json.dumps({"error": "upload 需要文件路径和标题参数: upload /path/to/file 标题"}, ensure_ascii=False))
                sys.exit(1)
            result = upload_file(sys.argv[2], sys.argv[3])

        elif command == "create":
            if len(sys.argv) < 4:
                print(json.dumps({"error": "create 需要标题和内容参数: create 标题 内容"}, ensure_ascii=False))
                sys.exit(1)
            result = create_text_document(sys.argv[2], sys.argv[3])

        else:
            result = {"error": f"未知命令: {command}，支持: search, search_answer, list, detail, upload, create"}

        print(json.dumps(result, ensure_ascii=False, indent=2))

    except urllib.error.URLError as e:
        print(json.dumps({"error": f"无法连接到知识库服务 ({API_BASE}): {e.reason}"}, ensure_ascii=False))
        sys.exit(1)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")[:200]
        print(json.dumps({"error": f"API 请求失败: {e.code} - {body}"}, ensure_ascii=False))
        sys.exit(1)
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
