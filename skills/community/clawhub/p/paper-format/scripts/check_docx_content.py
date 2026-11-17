#!/usr/bin/env python3
"""Reject blank or invalid DOCX inputs before paper formatting."""

from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


def configure_utf8_console() -> None:
    """Make JSON diagnostics stable across Windows GBK and UTF-8 hosts."""
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        reconfigure = getattr(stream, "reconfigure", None)
        if callable(reconfigure):
            reconfigure(encoding="utf-8", errors="replace")


configure_utf8_console()

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "m": "http://schemas.openxmlformats.org/officeDocument/2006/math",
}


def fail(status: str, message: str, code: int) -> int:
    print(json.dumps({"status": status, "message": message}, ensure_ascii=False))
    return code


def main() -> int:
    if len(sys.argv) != 2:
        return fail("invalid", "用法：check_docx_content.py <file.docx>", 3)

    path = Path(sys.argv[1])
    if not path.is_file():
        return fail("invalid", "文件不存在。", 3)
    if path.suffix.lower() != ".docx":
        return fail("invalid", "文件扩展名不是 .docx。", 3)

    try:
        with zipfile.ZipFile(path) as package:
            if "word/document.xml" not in package.namelist():
                return fail("invalid", "文件不是真实的 Word DOCX 文档。", 3)
            root = ET.fromstring(package.read("word/document.xml"))
    except (zipfile.BadZipFile, ET.ParseError, OSError, RuntimeError):
        return fail("invalid", "文档损坏、加密或无法解析，请重新上传可正常打开的 DOCX。", 3)

    texts = [node.text or "" for node in root.findall(".//w:t", NS)]
    normalized = re.sub(r"\s+", "", "".join(texts))
    nonempty_paragraphs = 0
    for paragraph in root.findall(".//w:p", NS):
        content = "".join(node.text or "" for node in paragraph.findall(".//w:t", NS))
        if re.sub(r"\s+", "", content):
            nonempty_paragraphs += 1

    drawings = len(root.findall(".//w:drawing", NS))
    pictures = len(root.findall(".//w:pict", NS))
    objects = len(root.findall(".//w:object", NS))
    equations = len(root.findall(".//m:oMath", NS)) + len(root.findall(".//m:oMathPara", NS))
    has_content_object = any((drawings, pictures, objects, equations))

    result = {
        "status": "content" if normalized or has_content_object else "blank",
        "characters": len(normalized),
        "nonempty_paragraphs": nonempty_paragraphs,
        "drawings": drawings + pictures,
        "embedded_objects": objects,
        "equations": equations,
    }
    if result["status"] == "blank":
        result["message"] = "该 Word 文档为空，无法进行论文排版。请上传包含论文标题、正文或其他实际内容的有效文档。"
        print(json.dumps(result, ensure_ascii=False))
        return 2

    result["message"] = "文档包含可排版内容。"
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
