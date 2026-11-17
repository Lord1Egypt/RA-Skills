import csv
import hashlib
import json
import mimetypes
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

from catalog import catalog_from_raw
from gitea_api import GiteaClient
from utils import extract_keywords, read_text_limited, slugify, strip_frontmatter, unique

MAX_TEXT_CHARS = 24000
MAX_CONTEXT_CHARS = 6000
MAX_CATALOG_PAGES = 400
MAX_RELATED_CARDS = 12
MAX_CARD_CHARS = 1200
TEXT_EXTS = {
    ".md", ".txt", ".csv", ".json", ".yaml", ".yml", ".py", ".java", ".js", ".ts",
    ".vue", ".html", ".css", ".sql", ".r", ".ipynb",
}
OFFICE_EXTS = {".docx", ".pptx", ".xlsx"}
BINARY_HINT_EXTS = {".png", ".jpg", ".jpeg", ".mp3", ".wav", ".m4a", ".aac", ".flac", ".mp4", ".mov", ".webm"}
PAGE_ROOTS = ["overview", "projects", "papers", "surveys", "code", "meetings", "experiments", "tech-notes", "notes", "concepts", "resources"]
ENTITY_TYPE_TO_ROOT = {
    "paper": "papers",
    "survey": "surveys",
    "project": "projects",
    "code": "code",
    "meeting": "meetings",
    "experiment": "experiments",
    "tech-note": "tech-notes",
    "note": "notes",
}


def prepare_context(payload):
    source = payload.get("source") or {}
    if source.get("type") != "local_folder":
        raise ValueError("local_document_ingest requires source.type=local_folder")
    raw_items = source.get("items") or []
    if not isinstance(raw_items, list):
        raise ValueError("source.items must be a list")

    client = GiteaClient(payload)
    catalog = catalog_from_raw(client.read_text("catalog.json"))
    index_preview = clip(strip_frontmatter(client.read_text("index.md")), 6000)
    prepared_items = []
    skipped = []

    for idx, item in enumerate(raw_items):
        if not isinstance(item, dict):
            skipped.append({"index": idx, "reason": "invalid_item"})
            continue
        prepared, skip = prepare_item(item, source, idx)
        if skip:
            skipped.append(skip)
        if prepared:
            prepared_items.append(prepared)

    tokens = query_tokens("\n".join(item.get("title") or item.get("relativePath") or "" for item in prepared_items))
    catalog_pages = compact_catalog_pages((catalog.get("pages") or [])[:MAX_CATALOG_PAGES])
    related_cards = related_page_cards(client, catalog.get("pages") or [], tokens)

    return {
        "schema": "research-kb/local-document-context@1",
        "mode": "local_document_ingest_prepare",
        "taskId": payload.get("taskId"),
        "trigger": payload.get("trigger") or "local_desktop_upload",
        "team": payload.get("team") or {},
        "platform": safe_platform(payload.get("platform") or {}),
        "source": {
            "id": source.get("id") or payload.get("sourceId"),
            "name": source.get("name") or "",
            "type": source.get("type") or "",
            "config": safe_source_config(source.get("config") or {}),
        },
        "inputItems": prepared_items,
        "skippedSources": skipped,
        "kb": {
            "catalogPageCount": len(catalog.get("pages") or []),
            "catalogPages": catalog_pages,
            "indexPreview": index_preview,
            "relatedPageCards": related_cards,
        },
        "analysisLimits": analysis_limits(prepared_items),
        "instructions": {
            "mustProcessOnlyInputItems": True,
            "mustCreateEntityPageForEveryReadableItem": True,
            "doNotScanUploadsDirectory": True,
            "doNotCreateQaPages": True,
            "allowedPageRoots": PAGE_ROOTS,
            "sourceItemKeyRule": "Every generated or updated page must include sourceItemKeys listing the input itemKey values that support that page. Every readable input item must appear in at least one entity page under projects/, papers/, surveys/, code/, meetings/, experiments/, tech-notes/, or notes/; overview/, concepts/, and resources/ cannot replace the entity page.",
            "unreadableInputRule": "Do not create entity pages for inputItems where readable=false unless you first extract enough evidence with allowed tools. Otherwise put them in skippedSources with parseWarnings; do not infer substantive content from filenames or public memory.",
            "batchingRule": "This context is one backend batch. Process only the inputItems in this context, keep each page concise, follow analysisLimits, and create concept/resource pages only when the batch has evidence for durable reuse.",
            "knowledgeGraphRule": "Before writing pages.json, make a private graph plan: entity pages first, then decide whether existing overview/project/concept/resource/other pages need updates. Concepts are stable reusable abstractions; resources are concrete reusable objects; overview pages are navigation or synthesis pages for themes, projects, source packages, or research areas. Do not force a page when evidence is weak, but do not skip an overview/concept/resource update when it would materially improve navigation or reuse.",
            "linkingRule": "Use relatedConcepts, relatedResources, relatedCodePages, and relatedPages to express catalog edges. relatedPages is for ordinary wiki page links such as overview/, projects/, papers/, surveys/, meetings/, experiments/, tech-notes/, and notes/. Also include explanatory wikilinks in the Markdown body.",
            "archiveRule": "Do not write source_files directly in pages.json. The apply script archives originals to source_files/local_folder/<sourceId>/... and injects archivedPath into page sources.",
            "entityTypeRouting": ENTITY_TYPE_TO_ROOT,
            "outputContract": {
                "pagesJson": {
                    "pages": [
                        {
                            "path": "papers/example.md",
                            "title": "论文：Example",
                            "type": "paper",
                            "kbType": "wiki",
                            "sourceItemKeys": ["input-item-key"],
                            "content": "Markdown body without frontmatter",
                            "keywords": [],
                            "projectIds": [],
                            "relatedConcepts": ["concepts/example.md"],
                            "relatedResources": ["resources/example.md"],
                            "relatedPages": ["overview/example.md"],
                        }
                    ],
                    "skippedSources": [],
                    "errors": [],
                    "snapshot": {},
                }
            },
        },
    }


def analysis_limits(prepared_items):
    readable_count = sum(1 for item in prepared_items if item.get("readable"))
    optional_related_pages = 3 if readable_count <= 5 else 5
    return {
        "maxPages": readable_count + optional_related_pages,
        "maxEntityPages": readable_count,
        "maxOverviewPages": 1,
        "maxConceptPages": 1 if readable_count <= 3 else 2,
        "maxResourcePages": 1 if readable_count <= 3 else 2,
        "maxPageContentChars": 5000,
        "guidance": "Prioritize required entity pages, then use the remaining budget for overview/concept/resource/related page updates that materially improve navigation or reuse. These are budgets, not quotas; do not expand into a broad report."
    }
def prepare_item(item, source, index):
    storage_path = first_text(item.get("storagePath"), item.get("archived_path"), item.get("archivedPath"))
    relative_path = normalize_relative(first_text(item.get("original_path"), item.get("originalPath"), item.get("title"), (item.get("metadata") or {}).get("relativePath"), item.get("fileName")))
    item_key = first_text(item.get("itemKey"), item.get("sha256"), relative_path)
    sha_expected = first_text(item.get("sha256"), (item.get("metadata") or {}).get("scanSha256"))
    title = first_text(item.get("title"), relative_path, item.get("fileName"), item_key)
    if not storage_path:
        return None, skip_item(item, index, item_key, relative_path, "missing_storage_path")
    path = Path(storage_path)
    if not path.exists() or not path.is_file():
        return None, skip_item(item, index, item_key, relative_path, "storage_path_not_found")

    stat = path.stat()
    sha_actual = sha256_file(path)
    if sha_expected and sha_actual.lower() != sha_expected.lower():
        return None, skip_item(item, index, item_key, relative_path, "sha256_mismatch", {"expected": sha_expected, "actual": sha_actual})

    ext = path.suffix.lower()
    extraction = extract_file(path, ext)
    prepared = {
        "index": index,
        "sourceId": source.get("id"),
        "itemKey": item_key or sha_actual,
        "title": title,
        "fileName": first_text(item.get("fileName"), path.name),
        "relativePath": relative_path or path.name,
        "storagePath": str(path),
        "sha256": sha_actual,
        "size": item.get("size") or stat.st_size,
        "mimeType": first_text((item.get("metadata") or {}).get("mimeType"), mimetypes.guess_type(path.name)[0] or ""),
        "uploadBatchId": first_text((item.get("metadata") or {}).get("uploadBatchId")),
        "localMtimeMs": (item.get("metadata") or {}).get("localMtimeMs"),
        "extension": ext,
        "readable": extraction.get("readable"),
        "extractionMethod": extraction.get("method"),
        "textPreview": clip(extraction.get("text") or "", MAX_CONTEXT_CHARS),
        "structure": extraction.get("structure") or {},
        "parseWarnings": extraction.get("warnings") or [],
        "suggestedSlug": slugify(Path(relative_path or path.name).stem),
        "weakTypeHints": weak_type_hints(title + "\n" + relative_path + "\n" + (extraction.get("text") or "")[:6000], ext),
    }
    if not prepared["readable"]:
        prepared["parseWarnings"] = unique(prepared["parseWarnings"] + ["no_text_extracted"])
    return prepared, None


def extract_file(path, ext):
    if ext in TEXT_EXTS:
        return extract_text_file(path, ext)
    if ext == ".pdf":
        return extract_pdf(path)
    if ext in OFFICE_EXTS:
        return extract_office_zip(path, ext)
    if ext == ".doc":
        return {"readable": False, "method": "legacy-doc-metadata", "text": "", "structure": {}, "warnings": ["legacy_doc_text_extraction_not_available"]}
    if ext == ".zip":
        return extract_zip_listing(path)
    if ext in BINARY_HINT_EXTS:
        return {"readable": False, "method": "binary-metadata", "text": "", "structure": {"kind": "binary_media"}, "warnings": ["binary_media_requires_openclaw_or_external_tool"]}
    return {"readable": False, "method": "unsupported-extension", "text": "", "structure": {}, "warnings": ["unsupported_extension"]}


def extract_text_file(path, ext):
    text = read_text_limited(path, MAX_TEXT_CHARS)
    structure = {}
    warnings = []
    if ext == ".csv":
        structure = csv_structure(path)
    if ext == ".json":
        structure = json_structure(text)
    return {"readable": bool(text.strip()), "method": "plain-text", "text": text, "structure": structure, "warnings": warnings}


def extract_pdf(path):
    warnings = []
    text = ""
    method = "pdf-optional-library"
    try:
        import pypdf  # type: ignore
        reader = pypdf.PdfReader(str(path))
        pages = []
        for page in reader.pages[:30]:
            pages.append(page.extract_text() or "")
            if sum(len(p) for p in pages) >= MAX_TEXT_CHARS:
                break
        text = "\n\n".join(pages)[:MAX_TEXT_CHARS]
        structure = {"pageCount": len(reader.pages)}
        return {"readable": bool(text.strip()), "method": method, "text": text, "structure": structure, "warnings": warnings}
    except Exception as exc:
        warnings.append("pdf_text_extraction_unavailable: " + str(exc)[:160])
    return {"readable": False, "method": "pdf-metadata-only", "text": "", "structure": {"fileType": "pdf"}, "warnings": warnings}


def extract_office_zip(path, ext):
    warnings = []
    try:
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            targets = office_xml_targets(names, ext)
            parts = []
            for name in targets:
                try:
                    raw = archive.read(name)
                    parts.append(xml_text(raw))
                except Exception as exc:
                    warnings.append(f"failed_to_read_{name}: {str(exc)[:80]}")
                if sum(len(p) for p in parts) >= MAX_TEXT_CHARS:
                    break
            text = "\n".join(part for part in parts if part).strip()[:MAX_TEXT_CHARS]
            return {
                "readable": bool(text),
                "method": "office-xml",
                "text": text,
                "structure": {"xmlParts": targets[:80], "fileCount": len(names)},
                "warnings": warnings,
            }
    except Exception as exc:
        return {"readable": False, "method": "office-xml", "text": "", "structure": {}, "warnings": ["office_zip_read_failed: " + str(exc)[:160]]}


def office_xml_targets(names, ext):
    if ext == ".docx":
        return [name for name in names if name.startswith("word/") and name.endswith(".xml") and ("document" in name or "footnotes" in name or "endnotes" in name)]
    if ext == ".pptx":
        return sorted([name for name in names if name.startswith("ppt/slides/slide") and name.endswith(".xml")])
    if ext == ".xlsx":
        shared = [name for name in names if name == "xl/sharedStrings.xml"]
        sheets = sorted([name for name in names if name.startswith("xl/worksheets/sheet") and name.endswith(".xml")])
        return shared + sheets
    return []


def xml_text(raw):
    try:
        root = ET.fromstring(raw)
    except ET.ParseError:
        return ""
    values = []
    for elem in root.iter():
        if elem.text and elem.text.strip():
            values.append(elem.text.strip())
    return "\n".join(values)


def extract_zip_listing(path):
    try:
        with zipfile.ZipFile(path) as archive:
            infos = archive.infolist()
            entries = [{"name": item.filename, "size": item.file_size} for item in infos[:300]]
            text = "\n".join(f"{entry['name']} ({entry['size']} bytes)" for entry in entries)
            return {"readable": bool(entries), "method": "zip-listing", "text": text, "structure": {"entryCount": len(infos), "entries": entries[:80]}, "warnings": ["zip_content_not_fully_extracted"]}
    except Exception as exc:
        return {"readable": False, "method": "zip-listing", "text": "", "structure": {}, "warnings": ["zip_read_failed: " + str(exc)[:160]]}


def csv_structure(path):
    try:
        text = read_text_limited(path, 4000)
        reader = csv.reader(text.splitlines())
        rows = list(reader)
        if not rows:
            return {}
        return {"columns": rows[0][:40], "sampleRowCount": max(0, len(rows) - 1)}
    except Exception:
        return {}


def json_structure(text):
    try:
        data = json.loads(text)
    except Exception:
        return {}
    if isinstance(data, dict):
        return {"jsonType": "object", "topLevelKeys": list(data.keys())[:60]}
    if isinstance(data, list):
        return {"jsonType": "array", "length": len(data)}
    return {"jsonType": type(data).__name__}


def related_page_cards(client, pages, tokens):
    if not tokens:
        return []
    ranked = []
    for page in pages or []:
        haystack = " ".join(str(page.get(key) or "") for key in ["path", "title", "type"]) + " " + " ".join(page.get("keywords") or [])
        score = sum(1 for token in tokens if token.lower() in haystack.lower())
        if score:
            ranked.append((score, page))
    cards = []
    for _, page in sorted(ranked, key=lambda pair: pair[0], reverse=True)[:MAX_RELATED_CARDS]:
        path = page.get("path") or ""
        if not path or path.startswith("source_files/"):
            continue
        raw = client.read_text(path)
        cards.append({
            "path": path,
            "title": page.get("title") or path,
            "type": page.get("type") or path.split("/", 1)[0],
            "keywords": page.get("keywords") or [],
            "relatedConcepts": page.get("relatedConcepts") or [],
            "relatedResources": page.get("relatedResources") or [],
            "relatedCodePages": page.get("relatedCodePages") or [],
            "relatedPages": page.get("relatedPages") or [],
            "contentPreview": clip(strip_frontmatter(raw), MAX_CARD_CHARS),
        })
    return cards


def compact_catalog_pages(pages):
    result = []
    for page in pages or []:
        path = page.get("path") or ""
        if not path or path.startswith("source_files/"):
            continue
        result.append({
            "path": path,
            "title": page.get("title") or path,
            "type": page.get("type") or path.split("/", 1)[0],
            "kbType": page.get("kbType") or page.get("kb_type") or "wiki",
            "keywords": page.get("keywords") or [],
            "sourceIds": page.get("sourceIds") or [],
            "projectIds": page.get("projectIds") or [],
            "relatedConcepts": page.get("relatedConcepts") or [],
            "relatedResources": page.get("relatedResources") or [],
            "relatedCodePages": page.get("relatedCodePages") or [],
            "relatedPages": page.get("relatedPages") or [],
            "sourceStatus": page.get("sourceStatus") or "active",
        })
    return result


def weak_type_hints(text, ext):
    value = (text or "").lower()
    hints = []
    if ext in {".py", ".java", ".js", ".ts", ".vue", ".html", ".css", ".sql", ".ipynb"}:
        hints.append("code")
    if any(word in value for word in ["abstract", "method", "experiment", "references", "doi", "arxiv"]):
        hints.append("paper")
    if any(word in value for word in ["综述", "调研", "survey", "review", "landscape", "趋势", "比较"]):
        hints.append("survey")
    if any(word in value for word in ["会议", "meeting", "纪要", "议程", "行动项", "决议"]):
        hints.append("meeting")
    if any(word in value for word in ["实验", "experiment", "ablation", "baseline", "metric", "结果"]):
        hints.append("experiment")
    if any(word in value for word in ["api", "配置", "安装", "部署", "命令", "troubleshoot", "排障"]):
        hints.append("tech-note")
    if any(word in value for word in ["项目", "需求", "roadmap", "milestone", "验收", "范围"]):
        hints.append("project")
    if not hints:
        hints.append("note")
    return unique(hints)[:5]


def query_tokens(text):
    return unique(re.findall(r"[\u4e00-\u9fff]{2,}|[A-Za-z][A-Za-z0-9_+.-]{2,}", text or ""))[:80]


def sha256_file(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def skip_item(item, index, item_key, relative_path, reason, extra=None):
    result = {
        "index": index,
        "itemKey": item_key or first_text(item.get("itemKey"), item.get("sha256"), relative_path),
        "relativePath": relative_path,
        "reason": reason,
    }
    if extra:
        result.update(extra)
    return result


def safe_platform(platform):
    return {
        "giteaUrl": platform.get("giteaUrl") or "",
        "giteaOwner": platform.get("giteaOwner") or "",
        "sharedDir": platform.get("sharedDir") or "",
    }


def safe_source_config(config):
    result = dict(config or {})
    result.pop("path", None)
    result.pop("localPath", None)
    return result


def normalize_relative(value):
    return str(value or "").replace("\\", "/").strip("/")


def first_text(*values):
    for value in values:
        text = str(value or "").strip()
        if text:
            return text
    return ""


def clip(text, limit):
    value = str(text or "")
    if len(value) <= limit:
        return value
    return value[:limit] + "\n...[truncated]"
