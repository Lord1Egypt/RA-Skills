import re
from datetime import datetime, timezone

from utils import clip, safe_relpath, unique

REF_HEADING = "参考来源"
NO_TEAM_CONTEXT_LINE = "- 本轮未明确引用团队 overview 页面。"
NO_WEB_SOURCE_LINE = "- 本轮未记录可核验的外部网页、论文或官方文档来源。"


def apply_answer(payload, answer_doc, context):
    answer = str(answer_doc.get("answer") or "").strip()
    if not answer:
        raise ValueError("OpenClaw answer.json must contain a non-empty answer")

    team_sources, rejected_team_sources = normalize_team_sources(answer_doc, context)
    web_sources = normalize_web_sources(answer_doc)
    answer = ensure_reference_section(answer, team_sources, web_sources)
    errors = normalize_errors(answer_doc.get("errors") or [])
    skipped_sources = []
    if rejected_team_sources:
        rejected_text = ", ".join(rejected_team_sources[:12])
        message = "Ignored teamSources that were not overview pages or fetched supplemental KB pages: " + rejected_text
        errors.append(message)
        skipped_sources.append(message)

    combined_sources = []
    combined_sources.extend(team_sources)
    combined_sources.extend(web_sources)
    result = {
        "answer": answer,
        "sources": combined_sources,
        "processedSources": ["team-kb-overview", "external-web"],
        "createdPages": [],
        "updatedPages": [],
        "skippedSources": skipped_sources,
        "errors": errors,
        "commitId": "",
        "createdQaPath": "",
        "knowledgeSufficient": bool(web_sources),
        "teamContextSources": team_sources,
        "webSources": web_sources,
        "usedSearchQueries": normalize_text_list(answer_doc.get("usedSearchQueries") or answer_doc.get("searchQueries") or []),
        "usedAttachments": answer_doc.get("usedAttachments") or [],
        "qaEvaluation": {
            "score": 0,
            "ephemeral": True,
            "reason": "kb_web_query disables QA persistence because the answer may depend on time-sensitive external web sources.",
        },
    }
    if not web_sources:
        result["skippedSources"].append("No external webSources were recorded; answer can be shown but should be treated as uncited external analysis.")
    return result


def normalize_team_sources(answer_doc, context):
    raw_sources = first_list(
        answer_doc.get("teamSources"),
        answer_doc.get("teamContextSources"),
        answer_doc.get("kbSources"),
    )
    if not raw_sources:
        raw_sources = [item for item in listify(answer_doc.get("sources")) if not source_url(item)]
    if not raw_sources:
        raw_sources = default_overview_sources(context)

    known = known_team_pages(context)
    normalized = []
    rejected = []
    for item in listify(raw_sources):
        source = normalize_known_team_source(item, known, rejected)
        if source:
            normalized.append(source)

    if not normalized:
        for item in default_overview_sources(context):
            source = normalize_known_team_source(item, known, [])
            if source:
                normalized.append(source)

    return dedupe_by(normalized, "path"), unique(rejected)


def normalize_known_team_source(item, known, rejected):
    if isinstance(item, str):
        item = {"path": item}
    if not isinstance(item, dict):
        return None
    path = safe_team_path(item.get("path") or item.get("pagePath") or item.get("url") or "")
    if not path:
        rejected.append(str(item.get("path") or item.get("url") or "<empty>"))
        return None
    known_page = known.get(path)
    if not known_page:
        rejected.append(path)
        return None
    return {
        "kind": "team_context",
        "sourceType": "team_context",
        "path": path,
        "title": item.get("title") or known_page.get("title") or known_page.get("expectedTitle") or path,
        "type": item.get("type") or known_page.get("type") or path.split("/", 1)[0],
        "snippet": clip(item.get("snippet") or item.get("excerpt") or first_text_line(known_page.get("content") or ""), 240),
        "role": item.get("role") or known_page.get("role") or "",
        "updatedAt": item.get("updatedAt") or known_page.get("updatedAt") or "",
    }


def normalize_web_sources(answer_doc):
    raw_sources = first_list(
        answer_doc.get("webSources"),
        answer_doc.get("externalSources"),
        answer_doc.get("externalReferences"),
    )
    if not raw_sources:
        raw_sources = [item for item in listify(answer_doc.get("sources")) if source_url(item)]

    normalized = []
    for item in listify(raw_sources):
        if isinstance(item, str):
            item = {"url": item}
        if not isinstance(item, dict):
            continue
        url = str(item.get("url") or item.get("href") or item.get("link") or item.get("path") or "").strip()
        if not is_http_url(url):
            continue
        title = str(item.get("title") or item.get("name") or url).strip()
        normalized.append({
            "kind": "web",
            "sourceType": item.get("sourceType") or item.get("type") or infer_source_type(url),
            "title": title,
            "url": url,
            "path": url,
            "publisher": item.get("publisher") or item.get("site") or item.get("domain") or "",
            "authors": normalize_text_list(item.get("authors") or []),
            "publishedAt": item.get("publishedAt") or item.get("date") or item.get("year") or "",
            "accessedAt": item.get("accessedAt") or now_iso(),
            "snippet": clip(item.get("snippet") or item.get("excerpt") or item.get("summary") or "", 360),
        })
    return dedupe_by(normalized, "url")[:12]


def default_overview_sources(context):
    pages = ((context.get("teamContext") or {}).get("overviewPages") or [])
    return [
        {"path": page.get("path"), "title": page.get("title") or page.get("expectedTitle") or page.get("path")}
        for page in pages
        if page.get("path") and page.get("available")
    ]


def known_team_pages(context):
    known = {}
    for page in ((context.get("teamContext") or {}).get("overviewPages") or []):
        path = page.get("path") or ""
        if path:
            known[path] = page
    for page in ((context.get("kb") or {}).get("evidencePages") or []):
        path = page.get("path") or ""
        if path:
            known[path] = page
    return known


def ensure_reference_section(answer, team_sources, web_sources):
    body = remove_reference_section(answer)
    lines = [body.rstrip(), "", f"## {REF_HEADING}", "", "### 团队上下文"]
    if team_sources:
        for source in team_sources:
            title = source.get("title") or source.get("path")
            path = source.get("path") or ""
            role = source.get("role") or ""
            suffix = f"：{role}" if role else ""
            lines.append(f"- {title} (`{path}`){suffix}")
    else:
        lines.append(NO_TEAM_CONTEXT_LINE)

    lines.extend(["", "### 外部资料"])
    if web_sources:
        for source in web_sources:
            source_type = source.get("sourceType") or "web"
            title = source.get("title") or source.get("url")
            url = source.get("url") or ""
            details = []
            for key in ["publisher", "publishedAt", "accessedAt"]:
                value = source.get(key)
                if value:
                    details.append(str(value))
            suffix = f" — {'; '.join(details)}" if details else ""
            lines.append(f"- [{source_type}] [{title}]({url}){suffix}")
    else:
        lines.append(NO_WEB_SOURCE_LINE)
    return "\n".join(lines).strip()


def remove_reference_section(answer):
    pattern = r"(?ms)\n{0,2}#{1,6}\s*" + re.escape(REF_HEADING) + r"\s*\n.*\Z"
    return re.sub(pattern, "", answer or "").strip()


def safe_team_path(path):
    if not path:
        return ""
    try:
        value = safe_relpath(path)
    except ValueError:
        return ""
    if value.startswith((".kb/", "source_files/")):
        return ""
    if value in {"README.md", "index.md", "catalog.json", "AGENTS.md", "log.md"}:
        return ""
    if not value.endswith(".md"):
        return ""
    return value


def source_url(item):
    if isinstance(item, str):
        return item if is_http_url(item) else ""
    if isinstance(item, dict):
        for key in ["url", "href", "link"]:
            value = str(item.get(key) or "").strip()
            if is_http_url(value):
                return value
        path = str(item.get("path") or "").strip()
        return path if is_http_url(path) else ""
    return ""


def is_http_url(value):
    text = str(value or "").strip().lower()
    return text.startswith("http://") or text.startswith("https://")


def infer_source_type(url):
    lower = str(url or "").lower()
    if "arxiv.org" in lower or "doi.org" in lower or "acm.org" in lower or "ieee.org" in lower or "springer" in lower:
        return "paper"
    if "docs." in lower or "/docs/" in lower or "developer." in lower or "learn.microsoft.com" in lower:
        return "official_doc"
    if "github.com" in lower or "gitlab.com" in lower:
        return "repository"
    return "web"


def first_list(*values):
    for value in values:
        items = listify(value)
        if items:
            return items
    return []


def listify(value):
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def normalize_text_list(items):
    if isinstance(items, (str, int, float)):
        items = [items]
    return [str(item).strip() for item in items or [] if str(item).strip()]


def dedupe_by(items, key):
    result = []
    seen = set()
    for item in items:
        value = item.get(key) or ""
        if not value or value in seen:
            continue
        seen.add(value)
        result.append(item)
    return result


def first_text_line(text):
    for line in str(text or "").splitlines():
        clean = line.strip().lstrip("#").strip()
        if clean:
            return clean
    return ""


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_errors(errors):
    if not isinstance(errors, list):
        return [str(errors)] if errors else []
    return [str(item) for item in errors if str(item).strip()]
