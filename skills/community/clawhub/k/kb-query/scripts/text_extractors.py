import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

from utils import clip

TEXT_SUFFIXES = {
    ".txt", ".md", ".csv", ".json", ".yaml", ".yml", ".py", ".java", ".js", ".ts",
    ".vue", ".html", ".css", ".sql", ".r", ".sh", ".ps1", ".xml", ".toml", ".ini",
}


def read_text_preview(path, max_chars=12000):
    if not path:
        return ""
    file_path = Path(path)
    if not file_path.exists() or not file_path.is_file():
        return ""
    if file_path.stat().st_size > 50 * 1024 * 1024:
        return ""
    suffix = file_path.suffix.lower()
    try:
        if suffix == ".docx":
            return read_docx_text(file_path, max_chars)
        if suffix == ".pptx":
            return read_pptx_text(file_path, max_chars)
        if suffix in TEXT_SUFFIXES:
            return clip(file_path.read_text(encoding="utf-8", errors="replace"), max_chars)
        return ""
    except Exception:
        return ""


def read_docx_text(file_path, max_chars):
    with zipfile.ZipFile(file_path) as archive:
        xml = archive.read("word/document.xml")
    root = ET.fromstring(xml)
    texts = []
    for node in root.iter():
        if node.tag.endswith("}t") and node.text:
            texts.append(node.text)
    return clip("\n".join(texts), max_chars)


def read_pptx_text(file_path, max_chars):
    texts = []
    with zipfile.ZipFile(file_path) as archive:
        slide_names = sorted(name for name in archive.namelist() if name.startswith("ppt/slides/slide") and name.endswith(".xml"))
        for name in slide_names:
            root = ET.fromstring(archive.read(name))
            slide_text = []
            for node in root.iter():
                if node.tag.endswith("}t") and node.text:
                    slide_text.append(node.text)
            if slide_text:
                texts.append(" ".join(slide_text))
            if sum(len(item) for item in texts) >= max_chars:
                break
    return clip("\n\n".join(texts), max_chars)
