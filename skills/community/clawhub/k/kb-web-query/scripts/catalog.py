import json

from utils import now, safe_relpath, sha256_text, unique

SYSTEM_PATHS = {"README.md", "index.md", "catalog.json", "AGENTS.md", "log.md"}
HIDDEN_PREFIXES = (".kb/", "source_files/")

LABELS = {
    "overview": "Overview",
    "project": "Projects",
    "projects": "Projects",
    "paper": "Papers",
    "papers": "Papers",
    "survey": "Surveys",
    "surveys": "Surveys",
    "code": "Code",
    "meeting": "Meetings",
    "meetings": "Meetings",
    "experiment": "Experiments",
    "experiments": "Experiments",
    "tech-note": "Tech Notes",
    "tech-notes": "Tech Notes",
    "note": "Notes",
    "notes": "Notes",
    "concept": "Concepts",
    "concepts": "Concepts",
    "resource": "Resources",
    "resources": "Resources",
    "qa": "Q&A",
}
RELATION_ROOTS = {"overview", "projects", "papers", "surveys", "code", "meetings", "experiments", "tech-notes", "notes", "concepts", "resources", "qa"}


def catalog_from_raw(raw):
    try:
        parsed = json.loads(raw) if raw else {"version": 1, "pages": []}
        if not isinstance(parsed, dict):
            return {"version": 1, "pages": []}
        parsed.setdefault("pages", [])
        return parsed
    except json.JSONDecodeError:
        return {"version": 1, "pages": []}


def visible_catalog_pages(catalog):
    pages = []
    for item in catalog.get("pages") or []:
        if not isinstance(item, dict):
            continue
        path = item.get("path") or ""
        if not path or path in SYSTEM_PATHS or path.startswith(HIDDEN_PREFIXES):
            continue
        pages.append(item)
    return pages


def catalog_entry(page):
    path = safe_relpath(page.get("path"))
    return {
        "path": path,
        "title": page.get("title") or path,
        "type": page.get("type") or path.split("/", 1)[0],
        "kbType": page.get("kbType") or "qa",
        "sourceIds": unique(page.get("sourceIds") or []),
        "updatedAt": now(),
        "keywords": unique(page.get("keywords") or []),
        "projectIds": unique(page.get("projectIds") or ["general"]),
        "relatedConcepts": normalize_relation_paths(page.get("relatedConcepts") or []),
        "relatedResources": normalize_relation_paths(page.get("relatedResources") or []),
        "relatedCodePages": normalize_relation_paths(page.get("relatedCodePages") or []),
        "relatedPages": normalize_relation_paths(page.get("relatedPages") or []),
        "contentHash": page.get("contentHash") or sha256_text(page.get("content") or ""),
        "sourceStatus": page.get("sourceStatus") or "active",
    }


def merge_catalog(catalog, entries):
    by_path = {}
    for item in catalog.get("pages") or []:
        path = item.get("path")
        if path:
            by_path[path] = dict(item)
    for entry in entries or []:
        path = entry.get("path")
        if not path:
            continue
        current = by_path.get(path, {})
        merged = dict(current)
        merged.update(entry)
        for key in ["sourceIds", "projectIds", "keywords", "relatedConcepts", "relatedResources", "relatedCodePages", "relatedPages"]:
            merged[key] = unique((current.get(key) or []) + (entry.get(key) or []))
        for key in ["relatedConcepts", "relatedResources", "relatedCodePages", "relatedPages"]:
            merged[key] = normalize_relation_paths(merged.get(key) or [])
        by_path[path] = merged
    for page in by_path.values():
        for key in ["relatedConcepts", "relatedResources", "relatedCodePages", "relatedPages"]:
            page[key] = normalize_relation_paths(page.get(key) or [])
    catalog["version"] = catalog.get("version") or 1
    catalog["updatedAt"] = now()
    catalog["pages"] = sorted(by_path.values(), key=lambda item: item.get("path") or "")
    return catalog


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


def render_index(catalog):
    groups = {}
    for page in visible_catalog_pages(catalog):
        path = page.get("path") or ""
        page_type = page.get("type") or path.split("/", 1)[0] or "resource"
        label = LABELS.get(page_type, LABELS.get(path.split("/", 1)[0], page_type))
        groups.setdefault(label, []).append(page)

    lines = ["# Knowledge Base Index", "", f"Updated at: {catalog.get('updatedAt') or now()}", ""]
    for label in sorted(groups):
        lines.extend([f"## {label}", ""])
        for page in sorted(groups[label], key=lambda item: item.get("title") or item.get("path") or ""):
            title = page.get("title") or page.get("path")
            path = page.get("path") or ""
            keywords = page.get("keywords") or []
            suffix = f" - {', '.join(keywords[:5])}" if keywords else ""
            lines.append(f"- [{title}]({path}){suffix}")
        lines.append("")
    return "\n".join(lines).strip() + "\n"
