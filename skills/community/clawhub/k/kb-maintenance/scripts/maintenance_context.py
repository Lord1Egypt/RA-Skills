from collections import Counter
import json

from catalog import catalog_from_raw, page_type_from_path, visible_catalog_pages
from gitea_api import GiteaClient
from utils import clip, parse_frontmatter, safe_relpath, sha256_text, strip_frontmatter, unique


OVERVIEW_TARGETS = [
    {"path": "overview/team-overview.md", "title": "团队总览", "role": "team identity, KB entrance, reading path"},
    {"path": "overview/research-map.md", "title": "研究方向地图", "role": "research themes, projects, concepts, resources"},
    {"path": "overview/recent-updates.md", "title": "近期更新", "role": "important recent KB changes"},
    {"path": "overview/source-summary.md", "title": "资料源概况", "role": "source coverage and gaps"},
    {"path": "overview/open-questions.md", "title": "开放问题", "role": "research questions, risks, missing evidence"},
    {"path": "overview/roadmap.md", "title": "整理路线", "role": "maintenance priorities and next actions"},
]

DEFAULT_MAX_PAGES = 500
MAX_INDEX_PREVIEW_CHARS = 8000
MAX_OVERVIEW_CHARS = 16000
MAX_PAGE_BODY_CHARS = 12000


def inspect_context(payload):
    client = GiteaClient(payload)
    maintenance = payload.get("maintenance") or {}
    max_pages = int_value(maintenance.get("maxCatalogPages"), DEFAULT_MAX_PAGES)

    catalog_raw = client.read_text("catalog.json")
    index_text = client.read_text("index.md")
    catalog = catalog_from_raw(catalog_raw)
    pages = visible_catalog_pages(catalog)[:max_pages]
    overview_pages = read_overview_pages(client)
    status = read_status_files(client)
    stats = build_stats(pages)

    return {
        "schema": "research-kb/kb-maintenance-inspection@2",
        "mode": "openclaw_led_overview_maintenance",
        "team": payload.get("team") or {},
        "platform": safe_platform(payload.get("platform") or {}),
        "overviewTargets": OVERVIEW_TARGETS,
        "currentOverviewPages": overview_pages,
        "maintenanceStatus": status,
        "catalog": {
            "updatedAt": catalog.get("updatedAt") or "",
            "hash": sha256_text(catalog_raw),
            "pageCount": len(pages),
            "pages": compact_catalog_pages(pages),
            "stats": stats,
            "recentPages": recent_pages(pages, 80),
        },
        "indexPreview": clip(strip_frontmatter(index_text), MAX_INDEX_PREVIEW_CHARS),
        "availableCommands": {
            "readPages": "python3 scripts/run_task.py read-pages --paths <comma-separated-page-paths> --output maintenance-evidence.json --quiet",
            "validateDrafts": "python3 scripts/run_task.py validate-pages --draft-dir overview-drafts --quiet",
            "applyDrafts": "python3 scripts/run_task.py apply --draft-dir overview-drafts --summary <summary> --quiet",
            "recordFailure": "python3 scripts/run_task.py record-failure --summary <summary> --error <error> --quiet",
        },
        "instructions": {
            "decisionOwner": "OpenClaw chooses which pages to read and how to update overview pages. The scripts only fetch, validate, and write.",
            "draftFormat": "Write normal Markdown files under overview-drafts/overview/*.md. Do not put long Markdown inside JSON unless using the optional compatibility path.",
            "scope": "Only the six fixed overview pages may be written.",
            "statusFiles": "apply writes succeeded status; record-failure writes failed status. Backend reads .kb/maintenance/kb_maintenance_status.json and .kb/maintenance/kb_maintenance_runs.json for frontend display.",
        },
    }


# Backwards-compatible name used by older run_task.py/tests.
def prepare_context(payload):
    return inspect_context(payload)


def read_selected_pages(payload, paths):
    client = GiteaClient(payload)
    result = []
    missing = []
    seen = set()
    for raw_path in paths:
        try:
            path = validate_read_path(raw_path)
        except Exception as exc:
            missing.append({"path": str(raw_path), "reason": str(exc)})
            continue
        if path in seen:
            continue
        seen.add(path)
        raw = client.read_text(path)
        if not raw.strip():
            missing.append({"path": path, "reason": "not_found_or_empty"})
            continue
        frontmatter = parse_frontmatter(raw)
        body = strip_frontmatter(raw)
        result.append({
            "path": path,
            "title": frontmatter.get("title") or path,
            "type": frontmatter.get("type") or page_type_from_path(path),
            "updatedAt": frontmatter.get("updatedAt") or "",
            "keywords": compact_list(frontmatter.get("keywords") or [], 20),
            "projectIds": compact_list(frontmatter.get("projectIds") or [], 20),
            "sourceIds": compact_list(frontmatter.get("sourceIds") or [], 20),
            "sourceTypes": source_types(frontmatter.get("sources") or []),
            "relatedConcepts": compact_list(frontmatter.get("relatedConcepts") or [], 20),
            "relatedResources": compact_list(frontmatter.get("relatedResources") or [], 20),
            "relatedCodePages": compact_list(frontmatter.get("relatedCodePages") or [], 20),
            "relatedPages": compact_list(frontmatter.get("relatedPages") or [], 20),
            "content": clip(body, MAX_PAGE_BODY_CHARS),
        })
    return {
        "schema": "research-kb/kb-maintenance-evidence@1",
        "requestedPaths": list(paths),
        "pages": result,
        "missingPages": missing,
        "instructions": {
            "useForOverviewMaintenanceOnly": True,
            "doNotQuoteLongPassages": True,
        },
    }


def validate_read_path(path):
    value = safe_relpath(path)
    if not value.endswith(".md"):
        raise ValueError("only Markdown KB pages can be read")
    if value.startswith((".kb/", "source_files/")):
        raise ValueError("hidden metadata and source_files are not evidence pages")
    if value in {"README.md", "index.md", "catalog.json", "AGENTS.md", "log.md"}:
        raise ValueError("system files are not evidence pages")
    if "/" not in value:
        raise ValueError("page path must include a KB root directory")
    return value


def read_overview_pages(client):
    result = []
    for target in OVERVIEW_TARGETS:
        raw = client.read_text(target["path"])
        frontmatter = parse_frontmatter(raw)
        body = strip_frontmatter(raw)
        result.append({
            "path": target["path"],
            "expectedTitle": target["title"],
            "role": target["role"],
            "exists": bool(raw.strip()),
            "title": frontmatter.get("title") or target["title"],
            "updatedAt": frontmatter.get("updatedAt") or "",
            "contentHash": frontmatter.get("contentHash") or sha256_text(body),
            "content": clip(body, MAX_OVERVIEW_CHARS),
        })
    return result


def read_status_files(client):
    return {
        "lastStatus": parse_json(client.read_text(".kb/maintenance/kb_maintenance_status.json"), {}),
        "recentRuns": parse_json(client.read_text(".kb/maintenance/kb_maintenance_runs.json"), []),
    }


def parse_json(raw, fallback):
    try:
        return json.loads(raw) if raw and raw.strip() else fallback
    except Exception:
        return fallback


def compact_catalog_pages(pages):
    result = []
    for page in pages:
        result.append({
            "path": page.get("path") or "",
            "title": page.get("title") or page.get("path") or "",
            "type": page.get("type") or page_type_from_path(page.get("path")),
            "kbType": page.get("kbType") or "",
            "updatedAt": page.get("updatedAt") or "",
            "sourceIds": compact_list(page.get("sourceIds") or [], 8),
            "projectIds": compact_list(page.get("projectIds") or [], 8),
            "keywords": compact_list(page.get("keywords") or [], 10),
            "sourceStatus": page.get("sourceStatus") or "active",
            "relatedConcepts": compact_list(page.get("relatedConcepts") or [], 8),
            "relatedResources": compact_list(page.get("relatedResources") or [], 8),
            "relatedCodePages": compact_list(page.get("relatedCodePages") or [], 8),
            "relatedPages": compact_list(page.get("relatedPages") or [], 8),
        })
    return result


def build_stats(pages):
    by_root = Counter((page.get("path") or "").split("/", 1)[0] for page in pages)
    by_type = Counter(page.get("type") or page_type_from_path(page.get("path")) for page in pages)
    by_status = Counter(page.get("sourceStatus") or "active" for page in pages)
    return {
        "byRoot": dict(sorted(by_root.items())),
        "byType": dict(sorted(by_type.items())),
        "bySourceStatus": dict(sorted(by_status.items())),
    }


def recent_pages(pages, limit):
    items = []
    for page in pages:
        items.append({
            "path": page.get("path") or "",
            "title": page.get("title") or page.get("path") or "",
            "type": page.get("type") or page_type_from_path(page.get("path")),
            "updatedAt": page.get("updatedAt") or "",
            "keywords": compact_list(page.get("keywords") or [], 6),
        })
    items.sort(key=lambda item: item.get("updatedAt") or "", reverse=True)
    return items[:limit]


def source_types(sources):
    if isinstance(sources, dict):
        sources = [sources]
    result = []
    for source in sources or []:
        if not isinstance(source, dict):
            continue
        value = source.get("sourceType") or source.get("type") or source.get("platform")
        if value:
            result.append(str(value))
    return unique(result)


def compact_list(values, limit):
    if isinstance(values, (str, int, float)):
        values = [values]
    return [str(item) for item in (values or []) if str(item).strip()][:limit]


def safe_platform(platform):
    return {
        "giteaUrl": platform.get("giteaUrl") or "",
        "giteaOwner": platform.get("giteaOwner") or "",
        "sharedDirConfigured": bool(platform.get("sharedDir")),
    }


def int_value(value, fallback):
    try:
        value = int(value)
        return value if value > 0 else fallback
    except Exception:
        return fallback

