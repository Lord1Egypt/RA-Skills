from __future__ import annotations


DOC_FOLDERS = {
    "paper": "summaries/papers",
    "survey": "summaries/surveys",
    "project": "summaries/projects",
    "doc": "summaries/docs_tech",
    "experiment": "summaries/experiments",
    "meeting": "summaries/meetings",
    "codebase": "summaries/codebases",
    "note": "summaries/notes",
}


def detect_type(file_kind: str, filename: str, text: str) -> str:
    kind = (file_kind or "").lower()
    name = (filename or "").lower()
    sample = (text or "")[:5000].lower()
    if kind == "code_pack" or name.endswith("-code-pack.zip"):
        return "codebase"
    if "meeting" in name or "会议" in name or "纪要" in name or "minutes" in name:
        return "meeting"
    if "experiment" in name or "实验" in name or "评测" in name or "benchmark" in name:
        return "experiment"
    if "survey" in name or "review" in name or "综述" in name or "调研" in name:
        return "survey"
    if "github" in sample or "installation" in sample or "readme" in name or "安装" in sample:
        return "project"
    if ("abstract" in sample or "摘要" in sample) and (
        "references" in sample or "doi" in sample or "arxiv" in sample or "参考文献" in sample
    ):
        return "paper"
    if kind in {"pdf", "word"}:
        return "doc"
    return "note"


def folder_for(type_key: str) -> str:
    return DOC_FOLDERS.get(type_key, DOC_FOLDERS["doc"])
