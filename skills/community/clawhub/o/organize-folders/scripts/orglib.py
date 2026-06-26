from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_DIRS = [
    ("00.inbox", "收件箱", "新文件入口", "下载、临时接收、待分类文件", "长期资料、唯一重要文件", "每周"),
    ("01.projects", "项目", "当前项目", "正在推进的代码、文档、素材", "已完成旧项目、纯备份", "每月"),
    ("02.areas", "领域", "长期责任", "长期维护的主题和责任", "一次性项目、临时下载", "每月"),
    ("03.resources", "资源", "可复用资料库", "电子书、教程、规范、素材", "当前任务过程文件", "每月"),
    ("04.knowledge", "知识", "沉淀后的知识", "笔记、总结、知识卡片", "原始大文件、安装包", "每月"),
    ("10.documents", "文档", "正式文件", "合同、报销、证明、简历、表格", "临时截图、无关下载", "每季度"),
    ("20.media", "媒体", "媒体资料", "照片、视频、录屏、素材", "项目专属素材主文件", "每季度"),
    ("30.software", "软件", "软件工具", "安装包、驱动、工具、绿色软件", "学习资料、电子书", "每季度"),
    ("90.archive", "归档", "已完成资料", "完成项目、旧课程、历史材料", "当前工作文件", "每季度"),
    ("99.backup", "备份", "防丢副本", "重要资料备份、照片备份", "唯一主文件、日常编辑文件", "每季度"),
]

SYSTEM_NAMES = {"$RECYCLE.BIN", "System Volume Information", "Windows", "Program Files", "Program Files (x86)"}

EXTENSIONS = {
    "software": {".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".apk", ".iso", ".appx"},
    "media": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp", ".heic", ".mp4", ".mov", ".mkv", ".avi", ".wmv", ".mp3", ".wav", ".flac"},
    "resources": {".pdf", ".epub", ".mobi", ".azw3", ".chm"},
    "documents": {".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".csv"},
    "knowledge": {".md", ".org"},
    "archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "code": {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java", ".c", ".cpp", ".h", ".cs", ".php", ".rb", ".sh", ".ps1"},
}

KEYWORDS = {
    "documents": ["合同", "报销", "发票", "简历", "证明", "invoice", "receipt", "resume", "contract"],
    "software": ["driver", "驱动", "installer", "setup", "portable", "安装包"],
    "resources": ["教程", "课程", "手册", "规范", "book", "manual", "tutorial", "guide", "spec"],
    "knowledge": ["笔记", "总结", "复盘", "note", "summary"],
    "backup": ["backup", "bak", "备份", "homebk", "snapshot"],
    "archive": ["archive", "归档", "done", "完成"],
}


def configure_stdout() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def load_json(path: str | Path) -> Any:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: str | Path, data: Any) -> None:
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(value) for value in row) + " |")
    return "\n".join(lines)


def safe_filename(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*]+', "_", name)
    return cleaned.strip() or "unnamed"


def is_system_path(path: Path) -> bool:
    return any(part in SYSTEM_NAMES for part in path.parts)


def classify_path(path: Path) -> dict[str, Any]:
    name = path.name
    lower = name.lower()
    ext = path.suffix.lower()
    parts = [part.lower() for part in path.parts]

    def has_keyword(group: str) -> bool:
        return any(word.lower() in lower or word.lower() in " ".join(parts) for word in KEYWORDS[group])

    result = {
        "path": str(path),
        "name": name,
        "extension": ext or "[无扩展名]",
        "irk": "Information",
        "para": "Projects",
        "lifecycle": "inbox",
        "suggested_dir": "00.inbox",
        "type": "待处理",
        "reason": "无法高置信度判断，先放收件箱等待人工分类。",
        "confidence": "low",
        "risk": "low",
        "requires_confirmation": True,
    }

    if is_system_path(path):
        result.update(
            type="系统或程序目录",
            suggested_dir="skip",
            reason="路径疑似系统或程序目录，默认跳过。",
            confidence="high",
            risk="high",
            requires_confirmation=True,
        )
        return result

    if has_keyword("backup"):
        result.update(type="备份", irk="Information", para="Archives", lifecycle="backup", suggested_dir="99.backup", reason="名称或路径疑似备份。", confidence="medium", risk="high")
    elif has_keyword("archive"):
        result.update(type="归档", irk="Information", para="Archives", lifecycle="archive", suggested_dir="90.archive", reason="名称或路径疑似已完成或归档内容。", confidence="medium", risk="medium")
    elif ext in EXTENSIONS["software"] or has_keyword("software"):
        result.update(type="软件工具", irk="Resource", para="Resources", lifecycle="active", suggested_dir="30.software", reason="扩展名或名称疑似安装包、驱动或工具。", confidence="high", risk="medium")
    elif has_keyword("documents"):
        result.update(type="正式文档", irk="Information", para="Areas", lifecycle="active", suggested_dir="10.documents", reason="名称疑似合同、报销、发票、简历或证明。", confidence="medium", risk="high")
    elif ext in EXTENSIONS["documents"]:
        result.update(type="文档", irk="Information", para="Areas", lifecycle="active", suggested_dir="10.documents", reason="扩展名属于常见办公文档。", confidence="medium", risk="medium")
    elif ext in EXTENSIONS["media"]:
        result.update(type="媒体", irk="Resource", para="Resources", lifecycle="active", suggested_dir="20.media", reason="扩展名属于图片、视频或音频。", confidence="high", risk="medium")
    elif ext in EXTENSIONS["resources"] or has_keyword("resources"):
        result.update(type="资源", irk="Resource", para="Resources", lifecycle="active", suggested_dir="03.resources", reason="疑似电子书、教程、手册、规范或参考资料。", confidence="medium", risk="low")
    elif ext in EXTENSIONS["knowledge"] or has_keyword("knowledge"):
        result.update(type="知识", irk="Knowledge", para="Areas", lifecycle="active", suggested_dir="04.knowledge", reason="疑似笔记、总结或知识沉淀。", confidence="medium", risk="low")
    elif ext in EXTENSIONS["code"] or any(part in {"src", "project", "workspace", "repo", "repos"} for part in parts):
        result.update(type="项目文件", irk="Information", para="Projects", lifecycle="active", suggested_dir="01.projects", reason="疑似代码或项目工作文件。", confidence="medium", risk="high")
    elif ext in EXTENSIONS["archives"]:
        result.update(type="压缩包", irk="Information", para="Projects", lifecycle="inbox", suggested_dir="00.inbox", reason="压缩包用途不明确，先进入收件箱或人工确认。", confidence="low", risk="medium")

    result["requires_confirmation"] = result["risk"] != "low" or result["confidence"] == "low"
    return result


def default_directory_rows() -> list[list[str]]:
    return [list(row) for row in DEFAULT_DIRS]


def default_dir_names() -> list[str]:
    return [row[0] for row in DEFAULT_DIRS]
