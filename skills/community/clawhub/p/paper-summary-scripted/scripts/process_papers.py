#!/usr/bin/env python3
"""Preprocess arXiv paper URLs and local files for LLM-based summarization workflows.

This script normalizes arXiv inputs, downloads PDFs, extracts text from supported
formats, cleans text, and emits a manifest.json plus per-paper text files.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path
from typing import Iterable
import xml.etree.ElementTree as ET


TEXT_EXTENSIONS = {".txt", ".md", ".markdown", ".json", ".csv"}
MAX_PREVIEW_CHARS = 400
ARXIV_HOSTS = {"arxiv.org", "www.arxiv.org"}
ARXIV_ID_PATTERN = re.compile(
    r"^(?:arxiv:)?(?P<id>(?:\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?/\d{7})(?:v\d+)?)$",
    re.IGNORECASE,
)


class ProcessingError(Exception):
    """Raised when a source cannot be processed."""


def parse_multi_value(raw: str | None) -> list[str]:
    if raw is None:
        return []
    value = raw.strip()
    if not value or value.lower() in {"none", "null", "[]"}:
        return []

    try:
        parsed = json.loads(value)
        if isinstance(parsed, list):
            return [str(item).strip() for item in parsed if str(item).strip()]
        if isinstance(parsed, str) and parsed.strip():
            return [parsed.strip()]
    except json.JSONDecodeError:
        pass

    if "\n" in value:
        return [item.strip() for item in value.splitlines() if item.strip()]
    if "," in value:
        return [item.strip() for item in value.split(",") if item.strip()]
    return [value]


def safe_slug(text: str, fallback: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", text).strip("-._").lower()
    return slug[:80] or fallback


def ensure_text(text: str) -> str:
    text = text.replace("\x00", " ")
    text = re.sub(r"\r\n?", "\n", text)
    text = re.sub(r"[\t\f\v]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"[ ]{2,}", " ", text)
    return text.strip()


def read_text_file(path: Path) -> str:
    data = path.read_bytes()
    for encoding in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return data.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise ProcessingError(f"cannot decode text file: {path}")


def extract_docx_text(path: Path) -> str:
    try:
        with zipfile.ZipFile(path) as zf:
            xml_bytes = zf.read("word/document.xml")
    except Exception as exc:
        raise ProcessingError(f"cannot open docx: {exc}") from exc

    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError as exc:
        raise ProcessingError(f"invalid docx xml: {exc}") from exc

    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    texts = [node.text for node in root.findall(".//w:t", ns) if node.text]
    if not texts:
        raise ProcessingError("docx contains no extractable text")
    return ensure_text(" ".join(texts))


def extract_pdf_text(path: Path) -> str:
    try:
        from pypdf import PdfReader  # type: ignore
    except Exception as exc:
        raise ProcessingError("pdf extraction requires pypdf in the runtime") from exc

    try:
        reader = PdfReader(str(path))
        pieces = []
        for page in reader.pages:
            pieces.append(page.extract_text() or "")
        text = ensure_text("\n\n".join(pieces))
        if not text:
            raise ProcessingError("pdf contains no extractable text")
        return text
    except Exception as exc:
        raise ProcessingError(f"cannot extract pdf text: {exc}") from exc


def extract_text_from_path(path: Path) -> tuple[str, list[str]]:
    notes: list[str] = []
    ext = path.suffix.lower()
    if ext in TEXT_EXTENSIONS:
        return ensure_text(read_text_file(path)), notes
    if ext == ".docx":
        notes.append("parsed docx via zipped xml extraction")
        return extract_docx_text(path), notes
    if ext == ".pdf":
        notes.append("parsed pdf via pypdf when available")
        return extract_pdf_text(path), notes

    # Fallback: attempt text decode for local text-like files only.
    try:
        notes.append("used fallback text decode for unknown extension")
        return ensure_text(read_text_file(path)), notes
    except ProcessingError as exc:
        raise ProcessingError(f"unsupported or unreadable file type {ext or '[no extension]'}: {exc}") from exc


def extract_arxiv_id(source: str) -> tuple[str, list[str]]:
    value = source.strip()
    notes: list[str] = []
    match = ARXIV_ID_PATTERN.fullmatch(value)
    if match:
        notes.append("normalized arxiv id to direct pdf download")
        return match.group("id"), notes

    parsed = urllib.parse.urlparse(value)
    host = parsed.netloc.lower()
    if host not in ARXIV_HOSTS:
        raise ProcessingError("paperurls only supports arXiv IDs or arXiv abs/pdf URLs")

    path = parsed.path.strip("/")
    if not path:
        raise ProcessingError("arXiv URL is missing a paper identifier")

    parts = [part for part in path.split("/") if part]
    if len(parts) < 2:
        raise ProcessingError("unsupported arXiv URL format")

    prefix = parts[0].lower()
    identifier = "/".join(parts[1:])
    if prefix == "pdf" and identifier.lower().endswith(".pdf"):
        identifier = identifier[:-4]
    elif prefix == "abs":
        notes.append("normalized arxiv abs URL to direct pdf download")
    else:
        raise ProcessingError("unsupported arXiv URL format")

    if not ARXIV_ID_PATTERN.fullmatch(identifier):
        raise ProcessingError("unsupported or invalid arXiv identifier")
    return identifier, notes


def download_arxiv_pdf(source: str, downloads_dir: Path, index: int) -> tuple[Path, list[str]]:
    arxiv_id, notes = extract_arxiv_id(source)
    url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    request = urllib.request.Request(url, headers={"User-Agent": "paper-summary-script/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            headers = dict(response.headers.items())
            content_type = headers.get("Content-Type", "").lower()
            if "pdf" not in content_type and not url.lower().endswith(".pdf"):
                raise ProcessingError("arXiv source did not resolve to a PDF download")
            base = safe_slug(arxiv_id.replace("/", "-"), f"arxiv-{index}")
            target = downloads_dir / f"{index:03d}-{base}.pdf"
            target.write_bytes(response.read())
            return target, notes
    except Exception as exc:
        raise ProcessingError(f"failed to download arXiv pdf: {exc}") from exc


def process_source(index: int, source_type: str, source_label: str, work_dir: Path) -> dict:
    downloads_dir = work_dir / "downloads"
    texts_dir = work_dir / "texts"
    downloads_dir.mkdir(parents=True, exist_ok=True)
    texts_dir.mkdir(parents=True, exist_ok=True)

    record = {
        "index": index,
        "source_type": source_type,
        "source_label": source_label,
        "status": "failed",
        "error": None,
        "download_path": None,
        "extracted_text_path": None,
        "characters": 0,
        "preview": "",
        "notes": [],
    }

    try:
        if source_type == "url":
            local_path, download_notes = download_arxiv_pdf(source_label, downloads_dir, index)
            record["download_path"] = str(local_path)
            record["notes"].extend(download_notes)
        else:
            local_path = Path(source_label).expanduser().resolve()
            if not local_path.exists() or not local_path.is_file():
                raise ProcessingError("local file does not exist or is not a file")
            record["download_path"] = str(local_path)

        text, notes = extract_text_from_path(local_path)
        record["notes"].extend(notes)
        if not text:
            raise ProcessingError("no extractable text found")

        label = Path(local_path).stem or f"paper-{index}"
        text_path = texts_dir / f"{index:03d}-{safe_slug(label, f'paper-{index}')}.txt"
        text_path.write_text(text + "\n", encoding="utf-8")

        record["status"] = "success"
        record["extracted_text_path"] = str(text_path)
        record["characters"] = len(text)
        record["preview"] = text[:MAX_PREVIEW_CHARS]
        return record
    except Exception as exc:
        record["error"] = str(exc)
        return record


def combine_texts(records: Iterable[dict], output_path: Path) -> None:
    chunks: list[str] = []
    for record in records:
        if record.get("status") != "success":
            continue
        text_path = record.get("extracted_text_path")
        if not text_path:
            continue
        try:
            text = Path(text_path).read_text(encoding="utf-8")
        except Exception:
            continue
        chunks.append(
            f"## Paper {record['index']}: {record['source_label']}\n\n{text.strip()}\n"
        )
    output_path.write_text("\n\n".join(chunks).strip() + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Preprocess arXiv paper URLs and local files for summarization workflows.")
    parser.add_argument("--language", default="", help="Requested output language.")
    parser.add_argument("--paperurls", default="", help="JSON array, newline list, comma list, or single arXiv URL/ID.")
    parser.add_argument("--paperfiles", default="", help="JSON array, newline list, comma list, or single file path.")
    parser.add_argument("--output-dir", required=True, help="Directory to write manifest and extracted text files.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    urls = parse_multi_value(args.paperurls)
    files = parse_multi_value(args.paperfiles)

    if not urls and not files:
        print(json.dumps({
            "status": "error",
            "message": "paperurls and paperfiles cannot both be empty",
        }, ensure_ascii=False, indent=2))
        return 1

    work_dir = Path(args.output_dir).expanduser().resolve()
    work_dir.mkdir(parents=True, exist_ok=True)

    records: list[dict] = []
    index = 1
    for url in urls:
        records.append(process_source(index, "url", url, work_dir))
        index += 1
    for file_path in files:
        records.append(process_source(index, "file", file_path, work_dir))
        index += 1

    manifest = {
        "status": "ok",
        "language": args.language,
        "paperurls_count": len(urls),
        "paperfiles_count": len(files),
        "success_count": sum(1 for r in records if r["status"] == "success"),
        "failure_count": sum(1 for r in records if r["status"] != "success"),
        "records": records,
    }

    manifest_path = work_dir / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    combine_texts(records, work_dir / "combined_extracted_text.md")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
