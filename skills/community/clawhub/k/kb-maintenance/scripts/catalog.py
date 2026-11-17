import json

from utils import now, unique


SYSTEM_PATHS = {"README.md", "index.md", "catalog.json", "AGENTS.md", "log.md"}
RELATION_ROOTS = {"overview", "projects", "papers", "surveys", "code", "meetings", "experiments", "tech-notes", "notes", "concepts", "resources", "qa"}
LABELS = {
    "overview": "Overview",
    "projects": "Projects",
    "project": "Projects",
    "papers": "Papers",
    "paper": "Papers",
    "surveys": "Surveys",
    "survey": "Surveys",
    "code": "Code Repositories",
    "meetings": "Meetings",
    "meeting": "Meetings",
    "experiments": "Experiments",
    "experiment": "Experiments",
    "tech-notes": "Tech Notes",
    "tech-note": "Tech Notes",
    "notes": "Notes",
    "note": "Notes",
    "concepts": "Concepts",
    "concept": "Concepts",
    "resources": "Resources",
    "resource": "Resources",
    "qa": "Q&A",
}


def catalog_from_raw(raw):
    try:
        data = json.loads(raw) if raw else {"version": 1, "pages": []}
        if not isinstance(data.get("pages"), list):
            data["pages"] = []
        return data
    except json.JSONDecodeError:
        return {"version": 1, "pages": []}


def visible_catalog_pages(catalog):
    result = []
    for page in catalog.get("pages") or []:
        if not isinstance(page, dict):
            continue
        path = page.get("path") or ""
        if not path or path in SYSTEM_PATHS:
            continue
        if path.startswith((".kb/", "source_files/")):
            continue
        if not path.endswith(".md"):
            continue
        result.append(dict(page))
    return result


def page_type_from_path(path):
    folder = str(path or "").split("/", 1)[0]
    if folder == "concepts":
        return "concept"
    if folder == "resources":
        return "resource"
    if folder == "tech-notes":
        return "tech-note"
    if folder == "projects":
        return "project"
    if folder == "papers":
        return "paper"
    if folder == "surveys":
        return "survey"
    if folder == "meetings":
        return "meeting"
    if folder == "experiments":
        return "experiment"
    if folder == "notes":
        return "note"
    return folder or "wiki"


def catalog_entry(page):
    return {
        "path": page.get("path"),
        "title": page.get("title"),
        "type": page.get("type") or page_type_from_path(page.get("path")),
        "kbType": page.get("kbType") or "wiki",
        "sourceIds": unique(page.get("sourceIds") or []),
        "projectIds": unique(page.get("projectIds") or ["general"]),
        "updatedAt": now(),
        "keywords": unique(page.get("keywords") or []),
        "relatedConcepts": normalize_relation_paths(page.get("relatedConcepts") or []),
        "relatedResources": normalize_relation_paths(page.get("relatedResources") or []),
        "relatedCodePages": normalize_relation_paths(page.get("relatedCodePages") or []),
        "relatedPages": normalize_relation_paths(page.get("relatedPages") or []),
        "contentHash": page.get("contentHash") or "",
        "sourceStatus": page.get("sourceStatus") or "active",
    }


def merge_catalog(catalog, entries):
    pages_by_path = {}
    for item in catalog.get("pages") or []:
        path = item.get("path")
        if path:
            pages_by_path[path] = dict(item)
    for entry in entries:
        path = entry.get("path")
        if not path:
            continue
        old = pages_by_path.get(path, {})
        merged = dict(old)
        merged.update({key: value for key, value in entry.items() if value not in (None, "")})
        for key in ["sourceIds", "projectIds", "keywords", "relatedConcepts", "relatedResources", "relatedCodePages", "relatedPages"]:
            merged[key] = unique((old.get(key) or []) + (entry.get(key) or []))
        pages_by_path[path] = merged
    catalog["version"] = catalog.get("version") or 1
    catalog["updatedAt"] = now()
    catalog["pages"] = sorted(normalize_graph(list(pages_by_path.values())), key=lambda item: item.get("path") or "")
    return catalog


def normalize_graph(pages):
    by_path = {page.get("path"): dict(page) for page in pages if page.get("path")}
    for page in list(by_path.values()):
        path = page.get("path")
        for key in ["relatedConcepts", "relatedResources", "relatedCodePages", "relatedPages"]:
            page[key] = normalize_relation_paths(page.get(key) or [])
        for related_path in page.get("relatedPages") or []:
            if related_path in by_path:
                by_path[related_path]["relatedPages"] = unique((by_path[related_path].get("relatedPages") or []) + [path])
    return list(by_path.values())


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
        value = value.replace("\\", "/").strip("/")
        if not value:
            continue
        if not value.endswith(".md"):
            value = value.rstrip("/") + ".md"
        if value.startswith("../") or "/../" in value or value == "..":
            continue
        root = value.split("/", 1)[0]
        if root not in RELATION_ROOTS or value.startswith("source_files/") or "/" not in value:
            continue
        result.append(value)
    return unique(result)


def render_index(catalog):
    groups = {}
    for page in visible_catalog_pages(catalog):
        page_type = page.get("type") or page_type_from_path(page.get("path"))
        label = LABELS.get(page_type, LABELS.get(str(page.get("path") or "").split("/", 1)[0], page_type))
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
