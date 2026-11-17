import urllib.error
import json
from pathlib import Path

from catalog import catalog_entry, catalog_from_raw, merge_catalog, normalize_relation_paths, render_index
from gitea_api import GiteaClient
from maintenance_context import OVERVIEW_TARGETS
from utils import extract_keywords, now, parse_frontmatter, safe_relpath, sha256_text, strip_frontmatter, unique


ALLOWED_PATHS = {item["path"]: item for item in OVERVIEW_TARGETS}
ALLOWED_FILENAMES = {Path(path).name: path for path in ALLOWED_PATHS}
RELATION_FIELDS = ["relatedConcepts", "relatedResources", "relatedCodePages", "relatedPages"]
STATUS_PATH = ".kb/maintenance/kb_maintenance_status.json"
RUNS_PATH = ".kb/maintenance/kb_maintenance_runs.json"


def pages_from_draft_dir(draft_dir):
    root = Path(draft_dir)
    if not root.exists() or not root.is_dir():
        raise ValueError(f"Draft directory does not exist: {draft_dir}")
    pages = []
    unsupported = []
    for file in sorted(root.rglob("*.md")):
        rel = file.relative_to(root).as_posix()
        if rel in ALLOWED_PATHS:
            path = rel
        elif file.name in ALLOWED_FILENAMES and (file.parent == root or file.parent.name == "overview"):
            path = ALLOWED_FILENAMES[file.name]
        else:
            unsupported.append(rel)
            continue
        raw = file.read_text(encoding="utf-8-sig")
        frontmatter = parse_frontmatter(raw)
        body = strip_frontmatter(raw)
        target = ALLOWED_PATHS[path]
        pages.append({
            "path": path,
            "title": frontmatter.get("title") or target["title"],
            "content": body,
            "keywords": frontmatter.get("keywords") or [],
            "projectIds": frontmatter.get("projectIds") or ["general"],
            "tags": frontmatter.get("tags") or ["overview", "kb-maintenance"],
            "relatedConcepts": frontmatter.get("relatedConcepts") or [],
            "relatedResources": frontmatter.get("relatedResources") or [],
            "relatedCodePages": frontmatter.get("relatedCodePages") or [],
            "relatedPages": frontmatter.get("relatedPages") or [],
        })
    if unsupported:
        raise ValueError("Draft directory contains unsupported Markdown files: " + ", ".join(unsupported[:20]))
    if not pages:
        raise ValueError("Draft directory contains no allowed overview Markdown files")
    return pages


def validate_draft_dir(draft_dir):
    pages = pages_from_draft_dir(draft_dir)
    return validate_pages_doc({}, {"pages": pages}, {})


def apply_draft_dir(payload, draft_dir, summary="", started_at=""):
    pages = pages_from_draft_dir(draft_dir)
    return apply_pages(payload, {"pages": pages, "summary": summary}, {}, summary=summary, started_at=started_at)


def validate_pages_doc(payload, pages_doc, context=None):
    pages = normalize_pages(pages_doc)
    errors = []
    seen = set()
    max_chars = ((context or {}).get("analysisLimits") or {}).get("maxOverviewContentChars") or 30000
    if not pages:
        errors.append("overview pages must contain at least one page")
    for index, page in enumerate(pages):
        if not isinstance(page, dict):
            errors.append(f"pages[{index}] must be an object")
            continue
        try:
            path = validate_overview_path(page.get("path"))
        except Exception as exc:
            errors.append(f"pages[{index}].path: {exc}")
            continue
        if path in seen:
            errors.append(f"duplicate overview page path: {path}")
        seen.add(path)
        title = str(page.get("title") or "").strip()
        if not title:
            errors.append(f"{path}: missing title")
        content = str(page.get("content") or page.get("body") or "").strip()
        if not content:
            errors.append(f"{path}: missing content")
        if len(content) > max_chars:
            errors.append(f"{path}: content exceeds maxOverviewContentChars={max_chars}")
        for field in RELATION_FIELDS:
            normalize_relation_paths(page.get(field) or [])
        normalize_evidence_sources(page.get("evidencePages") or page.get("sources") or [])
    if errors:
        raise ValueError("; ".join(errors[:20]))
    return {
        "success": True,
        "pageCount": len(pages),
        "allowedPaths": sorted(ALLOWED_PATHS),
        "errors": [],
    }


def apply_pages(payload, pages_doc, context=None, summary="", started_at=""):
    context = context or {}
    validate_pages_doc(payload, pages_doc, context)
    pages = [normalize_page(page) for page in normalize_pages(pages_doc)]
    client = GiteaClient(payload)
    created = []
    updated = []
    unchanged = []
    entries = []
    commit = ""

    for page in pages:
        path = page["path"]
        existing_raw = client.read_text(path)
        existing_body = strip_frontmatter(existing_raw)
        body = normalized_body(page)
        if sha256_text(existing_body.strip()) == sha256_text(body.strip()):
            unchanged.append(path)
            continue
        content = build_page_content(page, existing_raw)
        page["contentHash"] = sha256_text(strip_frontmatter(content))
        existed = bool(existing_raw.strip())
        client.upsert_text(path, content, f"OpenClaw maintenance update {path}")
        commit = client.last_commit
        entry = catalog_entry(page)
        entries.append(entry)
        (updated if existed else created).append(entry)

    if entries:
        catalog = write_catalog_with_retry(client, entries)
        commit = client.last_commit
        client.upsert_text("index.md", render_index(catalog), "OpenClaw maintenance update index.md")
        commit = client.last_commit

    pages_meta = pages_doc if isinstance(pages_doc, dict) else {}
    changed_paths = [item.get("path") for item in created + updated if item.get("path")]
    run_summary = summary or pages_meta.get("summary") or "kb_maintenance overview refresh"
    status = write_maintenance_status(
        client,
        status="succeeded",
        started_at=started_at,
        changed_pages=changed_paths,
        unchanged_pages=unchanged,
        commit_id=commit or client.last_commit or "",
        summary=run_summary,
        errors=normalize_errors(pages_meta.get("errors") or []),
    )
    commit = client.last_commit or commit

    return {
        "processedSources": ["team-kb"],
        "createdPages": created,
        "updatedPages": updated,
        "archivedFiles": [],
        "skippedSources": [{"path": path, "reason": "unchanged"} for path in unchanged],
        "errors": status.get("errors") or [],
        "commitId": commit,
        "maintenanceSummary": run_summary,
        "statusFiles": [STATUS_PATH, RUNS_PATH],
        "snapshot": {
            "targetPaths": sorted(ALLOWED_PATHS),
            "generatedPageCount": len(pages),
            "changedPageCount": len(changed_paths),
            "unchangedPageCount": len(unchanged),
            "catalogHash": ((context.get("catalog") or {}).get("hash") or (context.get("kb") or {}).get("catalogHash") or ""),
            "maintainedAt": status.get("lastFinishedAt") or now(),
        },
    }


def write_catalog_with_retry(client, entries, attempts=3):
    last_error = None
    for attempt in range(max(1, attempts)):
        file_info = client.read_file("catalog.json")
        catalog = merge_catalog(catalog_from_raw(file_info.get("content") or ""), entries)
        try:
            client.upsert_text_with_sha(
                "catalog.json",
                json.dumps(catalog, ensure_ascii=False, indent=2),
                "OpenClaw maintenance update catalog.json",
                file_info.get("sha"),
            )
            return catalog
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code in {409, 412, 422} and attempt < attempts - 1:
                continue
            raise
    if last_error:
        raise last_error
    return merge_catalog(catalog_from_raw(""), entries)

def write_maintenance_status(client, status, started_at, changed_pages, unchanged_pages, commit_id, summary, errors):
    finished_at = now()
    status_doc = {
        "skill": "kb_maintenance",
        "status": status,
        "trigger": "openclaw_cron",
        "lastStartedAt": started_at or finished_at,
        "lastFinishedAt": finished_at,
        "changedPages": changed_pages,
        "unchangedPages": unchanged_pages,
        "commitId": commit_id,
        "summary": summary,
        "errors": errors or [],
    }
    client.upsert_text(STATUS_PATH, json.dumps(status_doc, ensure_ascii=False, indent=2), "Record KB maintenance status")
    runs = read_runs(client)
    run_entry = dict(status_doc)
    run_entry["recordedAt"] = finished_at
    runs.insert(0, run_entry)
    runs = runs[:50]
    client.upsert_text(RUNS_PATH, json.dumps(runs, ensure_ascii=False, indent=2), "Record KB maintenance run history")
    return status_doc


def write_failure_status(payload, started_at, summary, errors, raise_on_error=False):
    client = GiteaClient(payload)
    try:
        return write_maintenance_status(
            client,
            status="failed",
            started_at=started_at,
            changed_pages=[],
            unchanged_pages=[],
            commit_id=client.last_commit or "",
            summary=summary or "kb_maintenance failed",
            errors=errors,
        )
    except Exception:
        if raise_on_error:
            raise
        return {}


def read_runs(client):
    try:
        raw = client.read_text(RUNS_PATH)
        data = json.loads(raw) if raw and raw.strip() else []
        return data if isinstance(data, list) else []
    except Exception:
        return []


def normalize_pages(pages_doc):
    if isinstance(pages_doc, list):
        pages = pages_doc
    elif isinstance(pages_doc, dict):
        pages = pages_doc.get("pages") or pages_doc.get("updatedPages") or pages_doc.get("createdPages") or []
    else:
        raise ValueError("overview pages JSON must be an object or array")
    if not isinstance(pages, list):
        raise ValueError("pages must be a list")
    return [page for page in pages if isinstance(page, dict)]


def normalize_page(page):
    path = validate_overview_path(page.get("path"))
    target = ALLOWED_PATHS[path]
    body = normalized_body(page)
    normalized = dict(page)
    normalized["path"] = path
    normalized["title"] = str(page.get("title") or target["title"]).strip()
    normalized["type"] = "overview"
    normalized["kbType"] = "wiki"
    normalized["projectIds"] = unique(page.get("projectIds") or ["general"])
    normalized["tags"] = unique(page.get("tags") or ["overview", "kb-maintenance"])
    normalized["keywords"] = unique(page.get("keywords") or extract_keywords(normalized["title"] + "\n" + body))
    for field in RELATION_FIELDS:
        normalized[field] = normalize_relation_paths(page.get(field) or [])
    normalized["sources"] = normalize_evidence_sources(page.get("evidencePages") or page.get("sources") or [])
    normalized["sourceStatus"] = page.get("sourceStatus") or "active"
    return normalized


def validate_overview_path(path):
    value = safe_relpath(path)
    if value not in ALLOWED_PATHS:
        raise ValueError("kb_maintenance may only write fixed overview pages; got " + value)
    return value


def normalized_body(page):
    path = validate_overview_path(page.get("path"))
    target = ALLOWED_PATHS[path]
    title = str(page.get("title") or target["title"]).strip()
    body = strip_frontmatter(page.get("content") or page.get("body") or "").strip()
    if not body:
        raise ValueError(f"{path}: missing content")
    if not body.startswith("#"):
        body = f"# {title}\n\n{body}"
    return body.strip() + "\n"


def build_page_content(page, existing_raw):
    body = normalized_body(page)
    frontmatter = parse_frontmatter(existing_raw)
    created_at = frontmatter.get("createdAt") or now()
    data = {
        "id": page.get("id") or page["path"].replace("/", "-").replace(".md", ""),
        "title": page["title"],
        "type": "overview",
        "kbType": "wiki",
        "projectIds": page.get("projectIds") or ["general"],
        "tags": page.get("tags") or ["overview", "kb-maintenance"],
        "keywords": page.get("keywords") or extract_keywords(page["title"] + "\n" + body),
        "createdAt": created_at,
        "updatedAt": now(),
        "generatedBy": "openclaw:kb_maintenance",
        "contentHash": sha256_text(body),
        "sourceStatus": page.get("sourceStatus") or "active",
        "relatedConcepts": page.get("relatedConcepts") or [],
        "relatedResources": page.get("relatedResources") or [],
        "relatedCodePages": page.get("relatedCodePages") or [],
        "relatedPages": page.get("relatedPages") or [],
        "sources": page.get("sources") or [],
    }
    lines = ["---"]
    for key, value in data.items():
        lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body


def normalize_evidence_sources(raw_sources):
    if isinstance(raw_sources, (str, dict)):
        raw_sources = [raw_sources]
    result = []
    for item in raw_sources or []:
        if isinstance(item, str):
            item = {"path": item}
        if not isinstance(item, dict):
            continue
        path = item.get("path") or item.get("url") or item.get("pagePath") or ""
        try:
            path = safe_relpath(path)
        except Exception:
            continue
        if not is_stable_kb_page(path):
            continue
        result.append({
            "sourceType": "kb_page",
            "platform": "gitea",
            "title": item.get("title") or path,
            "url": path,
            "status": "active",
            "ingestedAt": now(),
        })
    return unique(result)[:30]


def is_stable_kb_page(path):
    if not path.endswith(".md"):
        return False
    if path.startswith((".kb/", "source_files/")):
        return False
    if path in {"README.md", "index.md", "catalog.json", "AGENTS.md", "log.md"}:
        return False
    return "/" in path


def normalize_errors(errors):
    if not isinstance(errors, list):
        return [str(errors)] if errors else []
    result = []
    for item in errors:
        if isinstance(item, str):
            if item.strip():
                result.append(item)
        elif isinstance(item, dict):
            message = item.get("message") or item.get("error") or str(item)
            if str(message).strip():
                result.append(str(message))
    return result


