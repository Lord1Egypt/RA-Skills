import json
from pathlib import Path

from catalog import catalog_entry, catalog_from_raw, merge_catalog, render_index
from gitea_api import GiteaClient
from utils import extract_keywords, now, safe_relpath, sha256_text, slugify, strip_frontmatter, unique

ALLOWED_ROOTS = {
    "overview",
    "projects",
    "papers",
    "surveys",
    "code",
    "meetings",
    "experiments",
    "tech-notes",
    "notes",
    "concepts",
    "resources",
}
TYPE_BY_ROOT = {
    "overview": "overview",
    "projects": "project",
    "papers": "paper",
    "surveys": "survey",
    "code": "code",
    "meetings": "meeting",
    "experiments": "experiment",
    "tech-notes": "tech-note",
    "notes": "note",
    "concepts": "concept",
    "resources": "resource",
}
ENTITY_ROOTS = ALLOWED_ROOTS - {"overview", "concepts", "resources"}
RELATION_ROOTS = ALLOWED_ROOTS | {"qa"}
RELATION_FIELDS = (
    ("relatedConcepts", "相关概念"),
    ("relatedResources", "相关资源"),
    ("relatedCodePages", "相关代码页"),
    ("relatedPages", "相关页面"),
)


def apply_pages(payload, pages_doc, context=None):
    context = context or {}
    pages_meta = pages_doc if isinstance(pages_doc, dict) else {}
    pages = normalize_pages(pages_doc)

    source = payload.get("source") or {}
    source_id = source.get("id") or payload.get("sourceId") or "unknown"
    items = {str(item.get("itemKey") or ""): item for item in context.get("inputItems") or [] if item.get("itemKey")}
    if not items:
        items = source_items_from_payload(payload)
    if not items:
        raise ValueError("No source items available for local_document_ingest apply")

    required_keys = {key for key, item in items.items() if item.get("readable", True)}
    skipped_sources = normalize_skipped(context.get("skippedSources") or []) + normalize_skipped(pages_meta.get("skippedSources") or [])
    skipped_sources = skipped_sources + skipped_for_unreadable(items, skipped_sources)
    errors = normalize_errors(pages_meta.get("errors") or [])

    client = GiteaClient(payload)
    if not pages:
        if required_keys:
            raise ValueError("OpenClaw pages JSON must contain entity pages for every readable local input item")
        archive_map = archive_source_files(client, source_id, items, set(items.keys()))
        snapshot = build_snapshot(source_id, items, [], archive_map, pages_meta)
        return {
            "processedSources": [],
            "createdPages": [],
            "updatedPages": [],
            "archivedFiles": [archive_map[key] for key in sorted(archive_map)],
            "skippedSources": skipped_sources,
            "errors": errors,
            "commitId": client.last_commit or "",
            "snapshot": snapshot,
            "sourceItems": source_items_result(items, archive_map, set(), skipped_sources),
        }

    normalized_pages = []
    covered_item_keys = set()
    for page in pages:
        normalized = normalize_page(page, items)
        normalized_pages.append(normalized)
        if normalized["path"].split("/", 1)[0] in ENTITY_ROOTS:
            covered_item_keys.update(normalized.get("sourceItemKeys") or [])

    missing = sorted(required_keys - covered_item_keys)
    if missing:
        raise ValueError("Every readable local input item must appear in at least one entity page; missing itemKeys: " + ", ".join(missing))

    archive_map = archive_source_files(client, source_id, items, set(items.keys()))
    catalog = catalog_from_raw(client.read_text("catalog.json"))
    created = []
    updated = []
    entries = []
    commit = ""

    for page in normalized_pages:
        path = page["path"]
        content = build_page_content(payload, page, items, archive_map)
        page["contentHash"] = sha256_text(strip_frontmatter(content))
        existed = client.exists(path)
        client.upsert_text(path, content, f"OpenClaw update {path}")
        commit = client.last_commit
        entry = catalog_entry(page)
        entries.append(entry)
        (updated if existed else created).append(entry)

    catalog = merge_catalog(catalog, entries)
    client.upsert_text("catalog.json", json.dumps(catalog, ensure_ascii=False, indent=2), "OpenClaw update catalog.json")
    commit = client.last_commit
    client.upsert_text("index.md", render_index(catalog), "OpenClaw update index.md")
    commit = client.last_commit

    snapshot = build_snapshot(source_id, items, normalized_pages, archive_map, pages_meta)
    return {
        "processedSources": sorted(covered_item_keys),
        "createdPages": created,
        "updatedPages": updated,
        "archivedFiles": [archive_map[key] for key in sorted(archive_map)],
        "skippedSources": skipped_sources,
        "errors": errors,
        "commitId": commit,
        "snapshot": snapshot,
        "sourceItems": source_items_result(items, archive_map, covered_item_keys, skipped_sources),
    }


def validate_pages_doc(payload, pages_doc, context=None):
    context = context or {}
    pages = normalize_pages(pages_doc)
    source = payload.get("source") or {}
    source_id = source.get("id") or payload.get("sourceId") or "unknown"
    items = {str(item.get("itemKey") or ""): item for item in context.get("inputItems") or [] if item.get("itemKey")}
    if not items:
        items = source_items_from_payload(payload)
    if not items:
        raise ValueError("No source items available for local_document_ingest validation")

    required_keys = {key for key, item in items.items() if item.get("readable", True)}
    normalized_pages = []
    covered_item_keys = set()
    for page in pages:
        normalized = normalize_page(page, items)
        normalized_pages.append(normalized)
        if normalized["path"].split("/", 1)[0] in ENTITY_ROOTS:
            covered_item_keys.update(normalized.get("sourceItemKeys") or [])

    missing = sorted(required_keys - covered_item_keys)
    if missing:
        raise ValueError("Every readable local input item must appear in at least one entity page; missing itemKeys: " + ", ".join(missing))

    return {
        "success": True,
        "sourceId": source_id,
        "pageCount": len(normalized_pages),
        "entityPageCount": sum(1 for page in normalized_pages if page["path"].split("/", 1)[0] in ENTITY_ROOTS),
        "coveredItemCount": len(covered_item_keys),
        "requiredItemCount": len(required_keys),
    }

def normalize_pages(pages_doc):
    if isinstance(pages_doc, list):
        return pages_doc
    if not isinstance(pages_doc, dict):
        raise ValueError("pages JSON must be an object or array")
    pages = pages_doc.get("pages")
    if pages is None:
        pages = (pages_doc.get("createdPages") or []) + (pages_doc.get("updatedPages") or [])
    if not isinstance(pages, list):
        raise ValueError("pages must be a list")
    return [page for page in pages if isinstance(page, dict)]


def normalize_page(page, items):
    path = validate_page_path(page.get("path") or "")
    content = str(page.get("content") or page.get("body") or "").strip()
    if not content:
        raise ValueError(f"Page {path} is missing content/body")
    source_item_keys = source_keys_for_page(page, items)
    if not source_item_keys:
        raise ValueError(f"Page {path} must include sourceItemKeys referencing input items")
    page = dict(page)
    page["path"] = path
    page["type"] = page.get("type") or type_from_path(path)
    page["title"] = page.get("title") or title_from_path(path)
    page["kbType"] = page.get("kbType") or page.get("kb_type") or kb_type_for_path(path)
    page["sourceItemKeys"] = source_item_keys
    page["sourceIds"] = unique(page.get("sourceIds") or [source_id for source_id in [items[key].get("sourceId") for key in source_item_keys if key in items] if source_id not in (None, "")])
    page["projectIds"] = unique(page.get("projectIds") or ["general"])
    page["keywords"] = unique(page.get("keywords") or extract_keywords((page.get("title") or "") + "\n" + content))
    page["relatedConcepts"] = normalize_relation_paths(page.get("relatedConcepts") or [])
    page["relatedResources"] = normalize_relation_paths(page.get("relatedResources") or [])
    page["relatedCodePages"] = normalize_relation_paths(page.get("relatedCodePages") or [])
    page["relatedPages"] = normalize_relation_paths(page.get("relatedPages") or [])
    page["sourceStatus"] = page.get("sourceStatus") or "active"
    return page


def source_keys_for_page(page, items):
    raw = page.get("sourceItemKeys") or page.get("sourceItemKey") or page.get("itemKeys") or page.get("itemKey") or []
    if isinstance(raw, (str, int)):
        raw = [raw]
    keys = []
    for key in raw or []:
        keys.extend(match_source_candidate(key, items))
    for source in page.get("sources") or []:
        if not isinstance(source, dict):
            continue
        for candidate in [source.get("itemKey"), source.get("sourceItemKey"), source.get("sha256")]:
            keys.extend(match_source_candidate(candidate, items))
    if not keys and len(items) == 1:
        keys = list(items.keys())
    return unique(keys)


def match_source_candidate(candidate, items):
    key = str(candidate or "")
    if not key:
        return []
    if key in items:
        return [key]
    matches = [item_key for item_key, item in items.items() if str(item.get("sha256") or "") == key]
    return matches if len(matches) == 1 else []


def normalize_relation_paths(values):
    result = []
    for raw in values or []:
        value = raw
        if isinstance(raw, dict):
            value = raw.get("path") or raw.get("target") or raw.get("href") or ""
        if not isinstance(value, str):
            continue
        value = value.strip()
        if value.startswith("[[") and "]]" in value:
            value = value[2:value.find("]]")]
        if "|" in value:
            value = value.split("|", 1)[0].strip()
        if not value:
            continue
        if not value.endswith(".md"):
            value = value.rstrip("/") + ".md"
        try:
            path = safe_relpath(value)
        except ValueError:
            continue
        root = path.split("/", 1)[0]
        if root not in RELATION_ROOTS or path.startswith("source_files/") or "/" not in path:
            continue
        result.append(path)
    return unique(result)


def validate_page_path(path):
    value = safe_relpath(path)
    if not value.endswith(".md"):
        raise ValueError(f"Page path must end with .md: {path}")
    root = value.split("/", 1)[0]
    if root not in ALLOWED_ROOTS:
        raise ValueError(f"local_document_ingest cannot write {path}. Allowed roots: {', '.join(sorted(ALLOWED_ROOTS))}")
    if root == "qa":
        raise ValueError("local_document_ingest must not write qa/ pages")
    return value


def archive_source_files(client, source_id, items, keys_to_archive):
    archive_map = {}
    for key in sorted(keys_to_archive):
        item = items.get(key)
        if not item:
            continue
        storage_path = item.get("storagePath") or item.get("archived_path") or item.get("archivedPath")
        relative_path = item.get("relativePath") or item.get("original_path") or item.get("originalPath") or item.get("fileName") or key
        source_path = Path(str(storage_path or ""))
        hash8 = str(item.get("sha256") or key)[:8]
        identity8 = sha256_text(str(key) + "\n" + str(relative_path))[:8]
        ext = source_path.suffix or Path(str(relative_path)).suffix
        base = slugify(Path(str(relative_path)).stem or item.get("title") or item.get("fileName") or key)
        archive_path = f"source_files/local_folder/{source_id}/{now()[:10]}-{base}-{hash8}-{identity8}{ext or '.bin'}"
        try:
            data = source_path.read_bytes()
            client.upsert_bytes(archive_path, data, f"Archive local source file {archive_path}")
        except Exception as exc:
            archive_path = f"source_files/local_folder/{source_id}/{now()[:10]}-{base}-{hash8}-{identity8}.md"
            client.upsert_text(archive_path, render_source_registration(item, str(exc)), f"Register local source file {archive_path}")
        archive_map[key] = archive_path
    return archive_map


def build_page_content(payload, page, items, archive_map):
    body = strip_frontmatter(page.get("content") or page.get("body") or "")
    title = page.get("title") or title_from_path(page.get("path"))
    if not body.startswith("#"):
        body = f"# {title}\n\n{body}".strip()
    body = append_relation_section(body, page)
    data = {
        "id": page.get("id") or page.get("path", "").replace("/", "-").replace(".md", ""),
        "title": title,
        "type": page.get("type") or type_from_path(page.get("path")),
        "kbType": page.get("kbType") or kb_type_for_path(page.get("path")),
        "projectIds": page.get("projectIds") or ["general"],
        "tags": page.get("tags") or [],
        "keywords": page.get("keywords") or extract_keywords(title + "\n" + body),
        "createdAt": page.get("createdAt") or now(),
        "updatedAt": now(),
        "generatedBy": "openclaw:local_document_ingest",
        "contentHash": sha256_text(body),
        "sourceStatus": page.get("sourceStatus") or "active",
        "relatedConcepts": page.get("relatedConcepts") or [],
        "relatedResources": page.get("relatedResources") or [],
        "relatedCodePages": page.get("relatedCodePages") or [],
        "relatedPages": page.get("relatedPages") or [],
        "sources": source_traces(payload, page, items, archive_map),
    }
    lines = ["---"]
    for key, value in data.items():
        lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.strip() + "\n"


def append_relation_section(body, page):
    if any(heading in body for heading in ("## 关联页面", "## 知识关联", "## 相关页面")):
        return body
    lines = []
    seen = set()
    for field, label in RELATION_FIELDS:
        for raw in page.get(field) or []:
            path, title = relation_target(raw)
            if not path or path in seen:
                continue
            seen.add(path)
            lines.append(f"- {label}: [[{path}|{title}]]")
    if not lines:
        return body
    return body.rstrip() + "\n\n## 关联页面\n\n" + "\n".join(lines)


def relation_target(raw):
    title = ""
    value = raw
    if isinstance(raw, dict):
        title = str(raw.get("title") or raw.get("label") or "")
        value = raw.get("path") or raw.get("target") or ""
    if not isinstance(value, str):
        return "", ""
    value = value.strip()
    if value.startswith("[[") and "]]" in value:
        value = value[2:value.find("]]")]
    if "|" in value:
        value, alias = value.split("|", 1)
        title = title or alias.strip()
    if value.endswith(".md"):
        value = value[:-3]
    try:
        path = safe_relpath(value)
    except ValueError:
        return "", ""
    if not path or path.startswith("source_files/"):
        return "", ""
    return path, title or title_from_path(path)


def source_traces(payload, page, items, archive_map):
    source = payload.get("source") or {}
    traces = []
    for key in page.get("sourceItemKeys") or []:
        item = items.get(key)
        if not item:
            continue
        traces.append({
            "sourceId": source.get("id") or payload.get("sourceId") or item.get("sourceId"),
            "sourceType": "local_folder",
            "platform": "desktop",
            "title": item.get("title") or item.get("relativePath") or item.get("fileName") or key,
            "fileName": item.get("fileName") or "",
            "originalPath": item.get("relativePath") or item.get("original_path") or item.get("originalPath") or "",
            "archivedPath": archive_map.get(key) or "",
            "sha256": item.get("sha256") or key,
            "status": "active",
            "ingestedAt": now(),
            "uploadBatchId": item.get("uploadBatchId") or "",
        })
    return traces


def source_items_from_payload(payload):
    source = payload.get("source") or {}
    result = {}
    for item in source.get("items") or []:
        if not isinstance(item, dict):
            continue
        key = str(item.get("itemKey") or item.get("sha256") or item.get("original_path") or "")
        if not key:
            continue
        metadata = item.get("metadata") or {}
        result[key] = {
            "sourceId": source.get("id") or payload.get("sourceId"),
            "itemKey": key,
            "title": item.get("title") or item.get("fileName") or item.get("original_path") or key,
            "fileName": item.get("fileName") or "",
            "relativePath": item.get("original_path") or metadata.get("relativePath") or item.get("title") or "",
            "storagePath": item.get("storagePath") or item.get("archived_path") or item.get("archivedPath") or "",
            "sha256": item.get("sha256") or key,
            "size": item.get("size"),
            "mimeType": metadata.get("mimeType") or "",
            "uploadBatchId": metadata.get("uploadBatchId") or "",
            "readable": True,
        }
    return result


def render_source_registration(item, error):
    title = item.get("title") or item.get("relativePath") or item.get("fileName") or item.get("itemKey") or "local source file"
    data = {
        "sourceType": "local_folder",
        "title": title,
        "relativePath": item.get("relativePath") or "",
        "sha256": item.get("sha256") or item.get("itemKey") or "",
        "size": item.get("size") or 0,
        "mimeType": item.get("mimeType") or "",
        "uploadBatchId": item.get("uploadBatchId") or "",
        "storagePath": item.get("storagePath") or "",
        "archiveError": error,
        "registeredAt": now(),
    }
    return "\n".join([
        f"# 本地源文件登记：{title}",
        "",
        "原始字节未能归档，以下为来源登记。",
        "",
        "```json",
        json.dumps(data, ensure_ascii=False, indent=2),
        "```",
        "",
    ])


def type_from_path(path):
    root = str(path or "").split("/", 1)[0]
    return TYPE_BY_ROOT.get(root, root or "wiki")


def kb_type_for_path(path):
    root = str(path or "").split("/", 1)[0]
    if root == "concepts":
        return "concept"
    if root == "resources":
        return "resource"
    if root == "projects":
        return "project"
    if root == "source_files":
        return "source"
    return "wiki"


def title_from_path(path):
    value = str(path or "page.md")
    return value.rsplit("/", 1)[-1].replace(".md", "")


def normalize_skipped(items):
    result = []
    for item in items or []:
        if isinstance(item, str):
            result.append({"reason": item})
        elif isinstance(item, dict):
            result.append(item)
    return result


def normalize_errors(items):
    result = []
    for item in items or []:
        if isinstance(item, str):
            result.append({"message": item})
        elif isinstance(item, dict):
            result.append(item)
    return result


def build_snapshot(source_id, items, normalized_pages, archive_map, pages_meta):
    snapshot = dict(pages_meta.get("snapshot") or {})
    processed_hashes = unique([items[key].get("sha256") for key in sorted(archive_map) if key in items])
    snapshot.update({
        "sourceId": source_id,
        "uploadBatchId": first_upload_batch(items),
        "processedItemHashes": processed_hashes,
        "entityPageCount": sum(1 for page in normalized_pages if page["path"].split("/", 1)[0] in ENTITY_ROOTS),
        "relatedPageUpdateCount": len([page for page in normalized_pages if page["path"].split("/", 1)[0] == "overview"]),
        "conceptPageCount": len([page for page in normalized_pages if page["path"].startswith("concepts/")]),
        "resourcePageCount": len([page for page in normalized_pages if page["path"].startswith("resources/")]),
        "archivedFiles": [archive_map[key] for key in sorted(archive_map)],
    })
    return snapshot


def skipped_for_unreadable(items, existing_skipped):
    existing_keys = set()
    for item in existing_skipped or []:
        if isinstance(item, dict) and item.get("itemKey"):
            existing_keys.add(str(item.get("itemKey")))
    result = []
    for key, item in sorted(items.items()):
        if item.get("readable", True) or key in existing_keys:
            continue
        result.append({
            "itemKey": key,
            "relativePath": item.get("relativePath") or item.get("fileName") or key,
            "reason": "unreadable_or_no_text_extracted",
            "parseWarnings": item.get("parseWarnings") or [],
        })
    return result


def source_items_result(items, archive_map, covered_item_keys, skipped_sources):
    skipped_reason_by_key = {}
    for item in skipped_sources or []:
        if isinstance(item, dict) and item.get("itemKey"):
            skipped_reason_by_key[str(item.get("itemKey"))] = item.get("reason") or item.get("message") or "skipped"
    result = []
    for key, item in sorted(items.items()):
        ingested = key in covered_item_keys
        result.append({
            "itemKey": key,
            "title": item.get("title") or item.get("relativePath") or item.get("fileName") or key,
            "sourceKind": "file",
            "kind": "file",
            "status": "ingested" if ingested else "skipped",
            "sha256": item.get("sha256") or key,
            "originalPath": item.get("relativePath") or item.get("originalPath") or item.get("fileName") or "",
            "archivedPath": archive_map.get(key) or "",
            "size": item.get("size") or 0,
            "mimeType": item.get("mimeType") or "",
            "uploadBatchId": item.get("uploadBatchId") or "",
            "lastError": "" if ingested else skipped_reason_by_key.get(key, "not_covered_by_entity_page"),
        })
    return result

def first_upload_batch(items):
    for item in items.values():
        if item.get("uploadBatchId"):
            return item.get("uploadBatchId")
    return ""
