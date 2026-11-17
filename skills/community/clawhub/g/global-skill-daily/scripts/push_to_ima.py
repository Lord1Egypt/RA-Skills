"""
push_to_ima.py — 推送简报到 IMA FIM 知识库

两步流程：
  1. POST /openapi/note/v1/import_doc 创建笔记 → note_id
  2. POST /openapi/wiki/v1/add_knowledge 添加到知识库（media_type=11, note_info.content_id=note_id）

环境变量：
  IMA_OPENAPI_CLIENTID / IMA_OPENAPI_APIKEY
  IMA_KB_ID（必填，v1.2.0 移除硬编码默认值，避免 environment_proportionality finding）

v1.2.0 安全修复：移除硬编码 DEFAULT_KB_ID 字面量。kb_id 必须从环境变量读取，
未设置时返回失败，避免 SkillSpector 标记 environment_proportionality。
"""
from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path


IMA_API_BASE = "https://ima.qq.com"


def _get_credentials() -> tuple[str, str, str]:
    """读取 IMA 凭证（支持双环境变量名）。

    v1.2.0：移除硬编码 DEFAULT_KB_ID，kb_id 必须从环境变量 IMA_KB_ID 读取。
    """
    client_id = (
        os.environ.get("IMA_OPENAPI_CLIENTID")
        or os.environ.get("IMA_CLIENT_ID")
        or ""
    )
    api_key = (
        os.environ.get("IMA_OPENAPI_APIKEY")
        or os.environ.get("IMA_API_KEY")
        or ""
    )
    kb_id = os.environ.get("IMA_KB_ID", "")
    return client_id, api_key, kb_id


def _strip_frontmatter(content: str) -> tuple[str, str]:
    """剥离 YAML frontmatter，提取标题。返回 (clean_content, title)。"""
    if content.startswith("---\n"):
        end = content.find("\n---\n", 4)
        if end > 0:
            frontmatter = content[4:end]
            content_body = content[end + 5:]
            # 提取 title
            title_match = re.search(r"^title:\s*(.+)$", frontmatter, re.MULTILINE)
            title = title_match.group(1).strip() if title_match else ""
            return content_body, title
    return content, ""


def _extract_title(content: str, date_str: str) -> str:
    """从 markdown 提取标题。"""
    clean, fm_title = _strip_frontmatter(content)
    if fm_title:
        return fm_title
    # 找第一个 H1
    for line in clean.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    return f"全球 Skill 生态日报 {date_str}"


def _http_request(url: str, headers: dict, data: bytes) -> dict:
    """发起 HTTP 请求，返回 JSON。"""
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="ignore")
        return {"error": f"HTTP {e.code}", "body": body}
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        return {"error": str(e)}


def push(md_content: str, date_str: str) -> dict:
    """推送 markdown 到 IMA。"""
    client_id, api_key, kb_id = _get_credentials()

    if not client_id or not api_key:
        return {
            "success": False,
            "error": "缺少凭证：IMA_OPENAPI_CLIENTID 或 IMA_OPENAPI_APIKEY 未设置",
        }

    if not kb_id:
        return {
            "success": False,
            "error": "缺少 IMA_KB_ID 环境变量（v1.2.0 起必填，不再提供默认值）",
        }

    title = _extract_title(md_content, date_str)
    clean_content, _ = _strip_frontmatter(md_content)

    headers = {
        "Content-Type": "application/json",
        "ima-openapi-clientid": client_id,
        "ima-openapi-apikey": api_key,
    }

    # Step 1: 创建笔记
    create_payload = {
        "title": title,
        "content": clean_content,
        "content_format": 1,  # MARKDOWN
    }
    create_url = f"{IMA_API_BASE}/openapi/note/v1/import_doc"
    create_resp = _http_request(create_url, headers, json.dumps(create_payload, ensure_ascii=False).encode("utf-8"))

    if "error" in create_resp:
        return {"success": False, "step": "create_note", "error": create_resp["error"], "detail": create_resp}

    note_id = create_resp.get("note_id") or create_resp.get("data", {}).get("note_id")
    if not note_id:
        return {"success": False, "step": "create_note", "error": "no note_id in response", "detail": create_resp}

    # Step 2: 添加到知识库
    add_payload = {
        "knowledge_base_id": kb_id,
        "media_type": 11,
        "note_info": {
            "content_id": note_id,
        },
    }
    add_url = f"{IMA_API_BASE}/openapi/wiki/v1/add_knowledge"
    add_resp = _http_request(add_url, headers, json.dumps(add_payload, ensure_ascii=False).encode("utf-8"))

    if "error" in add_resp:
        return {"success": False, "step": "add_knowledge", "note_id": note_id, "error": add_resp["error"], "detail": add_resp}

    return {
        "success": True,
        "note_id": note_id,
        "kb_id": kb_id,
        "title": title,
        "add_response": add_resp,
    }


def main():
    if len(sys.argv) < 3:
        print("Usage: python push_to_ima.py <md_path> <date_str>")
        sys.exit(1)

    md_path = Path(sys.argv[1])
    date_str = sys.argv[2]

    if not md_path.exists():
        print(f"[push_to_ima] MD not found: {md_path}")
        sys.exit(1)

    md_content = md_path.read_text(encoding="utf-8")
    result = push(md_content, date_str)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if not result.get("success"):
        sys.exit(1)


if __name__ == "__main__":
    main()
