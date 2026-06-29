# -*- coding: utf-8 -*-
"""
kb_common.py — paper-kb 知识库公共逻辑（全类型版）

相比旧版的变化：
  - catalog 文档条目增加 type_key 字段
  - summaries 支持六个类型子文件夹
  - 文件名支持日期前缀（会议/实验）
  - regen_index 按类型分区展示，去掉"查询记录"区块
  - 新增 append_query_log（查询日志，供 kb_read 顺手调用）
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone, timedelta
from pathlib import Path

import gitea_api as g
import doc_types as dt

REPO_NAME = "paper-kb"
CATALOG_FILE = "catalog.json"
TMP_DIR = Path("/tmp/paperkb")

_TZ = timezone(timedelta(hours=8))


def now_str() -> str:
    return datetime.now(_TZ).strftime("%Y-%m-%d %H:%M:%S")


def today_str() -> str:
    return datetime.now(_TZ).strftime("%Y-%m-%d")


def ensure_tmp() -> Path:
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    return TMP_DIR


# ---------------------------------------------------------------- 用户

def get_user_by_open_id(open_id: str) -> dict | None:
    users = g.read_users()
    return users.get(open_id)


# ---------------------------------------------------------------- 文件名

def sanitize_filename(title: str, max_len: int = 80) -> str:
    name = re.sub(r'[\\/:*?"<>|\r\n\t]', " ", title)
    name = re.sub(r"\s+", " ", name).strip()
    name = name.strip(". ")
    if len(name) > max_len:
        name = name[:max_len].rstrip()
    return name or "untitled"


def build_filename(title: str, type_key: str) -> str:
    """根据类型决定文件名：会议/实验加日期前缀，其余用标题。"""
    safe = sanitize_filename(title)
    if dt.is_dated(type_key):
        return f"{today_str()} {safe}"
    return safe


def normalize_for_match(text: str) -> str:
    return re.sub(r"[^0-9a-z\u4e00-\u9fff]", "", (text or "").lower())


def make_fingerprint(full_text: str, length: int = 200) -> str:
    return normalize_for_match(full_text)[:length]


# ---------------------------------------------------------------- catalog

_EMPTY_CATALOG = {"documents": [], "concepts": [], "resources": []}


def read_catalog(gitea_username: str) -> dict:
    result = g.get_file(gitea_username, REPO_NAME, CATALOG_FILE)
    if result is None:
        return json.loads(json.dumps(_EMPTY_CATALOG))
    content, _ = result
    try:
        cat = json.loads(content)
    except json.JSONDecodeError:
        return json.loads(json.dumps(_EMPTY_CATALOG))
    for key in _EMPTY_CATALOG:
        cat.setdefault(key, [])
    return cat


def write_catalog(gitea_username: str, catalog: dict) -> None:
    g.put_file(
        gitea_username, REPO_NAME, CATALOG_FILE,
        json.dumps(catalog, ensure_ascii=False, indent=2),
        "paper-kb: update catalog",
    )


def upsert_document(catalog: dict, entry: dict) -> bool:
    docs = catalog["documents"]
    for i, d in enumerate(docs):
        same_arxiv = entry.get("arxiv_id") and d.get("arxiv_id") == entry["arxiv_id"]
        same_title = normalize_for_match(d.get("title", "")) == normalize_for_match(entry.get("title", ""))
        if same_arxiv or same_title:
            docs[i] = entry
            return True
    docs.append(entry)
    return False


def upsert_page(catalog: dict, kind: str, entry: dict) -> bool:
    pages = catalog[kind]
    for i, p in enumerate(pages):
        if normalize_for_match(p.get("name", "")) == normalize_for_match(entry.get("name", "")):
            pages[i] = entry
            return True
    pages.append(entry)
    return False


# ---------------------------------------------------------------- index.md（按类型分区）

def regen_index(gitea_username: str, research_direction: str, catalog: dict) -> None:
    """从 catalog 整体重新生成 index.md，文档按类型分区展示。"""
    lines = [
        "# 知识库索引", "",
        "## 研究方向", research_direction or "（未填写）", "",
        "## 文档", "",
    ]
    docs = catalog["documents"]
    for type_key, meta in dt.DOC_TYPES.items():
        group = [d for d in docs if d.get("type_key") == type_key]
        if not group:
            continue
        lines.append(f"### {meta['cn']}")
        for d in sorted(group, key=lambda x: x.get("created_at", ""), reverse=True):
            stem = Path(d["file"]).stem
            score = d.get("score", "")
            score_part = f"｜相关性{score}" if (score != "" and score != "自有") else ""
            lines.append(f"- [[{stem}]] — {d.get('brief', '')}{score_part}")
        lines.append("")
    legacy = [d for d in docs if not d.get("type_key")]
    if legacy:
        lines.append("### 其他")
        for d in legacy:
            lines.append(f"- [[{Path(d['file']).stem}]] — {d.get('brief', '')}")
        lines.append("")

    lines += ["## 概念", ""]
    for c in sorted(catalog["concepts"], key=lambda x: x.get("name", "")):
        stem = Path(c["file"]).stem
        lines.append(f"- [[{stem}]] — {c.get('brief', '')}")
    lines += ["", "## 科研资源", ""]
    for r in sorted(catalog["resources"], key=lambda x: x.get("name", "")):
        stem = Path(r["file"]).stem
        rtype = r.get("resource_type", "资源")
        lines.append(f"- [[{stem}]]（{rtype}）— {r.get('brief', '')}")
    lines.append("")

    g.put_file(
        gitea_username, REPO_NAME, "index.md",
        "\n".join(lines) + "\n",
        "paper-kb: regenerate index",
    )


# ---------------------------------------------------------------- log.md

def _append_log(gitea_username: str, operation: str, description: str) -> None:
    try:
        existing = g.get_file(gitea_username, REPO_NAME, "log.md")
        entry = f"- `{now_str()}` **{operation}** | {description}\n"
        if existing is None:
            content = "# 操作日志\n\n" + entry
            g.put_file(gitea_username, REPO_NAME, "log.md", content, "paper-kb: init log")
        else:
            old, sha = existing
            g.put_file(gitea_username, REPO_NAME, "log.md", old + entry,
                       "paper-kb: append log", sha=sha)
    except Exception:  # noqa: BLE001
        pass


def append_log(gitea_username: str, operation: str, description: str) -> None:
    _append_log(gitea_username, operation, description)


def append_query_log(gitea_username: str, question: str) -> None:
    """查询日志。供 kb_read 在列目录时顺手调用，确保查询必被记录。"""
    q = (question or "").strip()
    if not q:
        return
    if len(q) > 100:
        q = q[:100] + "…"
    _append_log(gitea_username, "query", q)
