from __future__ import annotations

import json
from pathlib import Path

import gitea_api as g


EMPTY = {"documents": [], "concepts": [], "resources": [], "people": [], "projects": [], "reviews": [], "imports": []}
TYPE_LABELS = {
    "paper": "论文",
    "survey": "综述与调研",
    "project": "项目",
    "doc": "技术文档",
    "experiment": "实验",
    "meeting": "会议",
    "codebase": "代码库",
    "note": "笔记",
}
TYPE_ORDER = ["paper", "survey", "project", "codebase", "doc", "experiment", "meeting", "note"]


def read(owner: str, repo: str) -> dict:
    raw = g.read_text(owner, repo, "catalog.json")
    if not raw:
        return json.loads(json.dumps(EMPTY))
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = json.loads(json.dumps(EMPTY))
    for key, value in EMPTY.items():
        data.setdefault(key, list(value))
    return data


def write(owner: str, repo: str, data: dict) -> None:
    g.put_file(owner, repo, "catalog.json", json.dumps(data, ensure_ascii=False, indent=2) + "\n", "research-kb: update catalog")


def upsert_document(cat: dict, entry: dict) -> bool:
    docs = cat.setdefault("documents", [])
    for index, old in enumerate(docs):
        same_file = old.get("source_file_id") and old.get("source_file_id") == entry.get("source_file_id")
        same_source = old.get("source_id") == entry.get("source_id") and old.get("source_path") == entry.get("source_path")
        if same_file or same_source:
            docs[index] = entry
            return True
    docs.append(entry)
    return False


def regen_index(owner: str, repo: str, title: str, cat: dict) -> None:
    docs = sorted(
        [doc for doc in cat.get("documents", []) if doc.get("file")],
        key=lambda item: (item.get("type_key", "doc"), item.get("title", ""), item.get("file", "")),
    )
    latest = max([doc.get("updated_at", "") for doc in docs] or [""])
    lines = [
        f"# {title}",
        "",
        "## 当前状态",
        "",
        f"- 已编译知识页面：{len(docs)} 个",
        f"- 最近更新：{latest or '暂无'}",
        "",
        "## 快速入口",
        "",
        "- 论文：`summaries/papers/`",
        "- 综述与调研：`summaries/surveys/`",
        "- 项目：`summaries/projects/`",
        "- 代码库：`summaries/codebases/`",
        "- 技术文档：`summaries/docs_tech/`",
        "- 实验：`summaries/experiments/`",
        "- 会议：`summaries/meetings/`",
        "- 笔记：`summaries/notes/`",
        "",
        "## 知识页面",
        "",
    ]
    groups: dict[str, list[dict]] = {}
    for doc in docs:
        groups.setdefault(doc.get("type_key", "doc"), []).append(doc)
    if not groups:
        lines.append("暂无已编译知识页面。")
        lines.append("")
    ordered_types = [item for item in TYPE_ORDER if item in groups] + sorted(key for key in groups if key not in TYPE_ORDER)
    for type_key in ordered_types:
        lines += [f"### {TYPE_LABELS.get(type_key, type_key)}", ""]
        for doc in groups[type_key]:
            path = doc.get("file", "")
            label = doc.get("title") or Path(path).stem
            brief = doc.get("brief") or "暂无摘要"
            source = doc.get("source_path") or doc.get("archived_source_path") or "未记录"
            lines.append(f"- [[{path}|{label}]] - {brief}（来源：{source}）")
        lines.append("")
    g.put_file(owner, repo, "index.md", "\n".join(lines).rstrip() + "\n", "research-kb: regenerate index")
