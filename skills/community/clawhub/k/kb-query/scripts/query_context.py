from catalog import catalog_from_raw, visible_catalog_pages
from gitea_api import GiteaClient
from text_extractors import read_text_preview
from utils import clip, parse_frontmatter, query_tokens, safe_relpath, score_text, strip_frontmatter, unique

MAX_CATALOG_PAGES = 350
MAX_RANKED_CATALOG_PAGES = 60
MAX_READ_POOL = 40
MAX_STARTER_CARDS = 10
MAX_STARTER_CARD_CHARS = 1200
MAX_EVIDENCE_PAGES = 6
MAX_PAGE_CHARS = 8000
MAX_TOTAL_PAGE_CHARS = 45000
MAX_ATTACHMENT_CHARS = 8000
MAX_TOTAL_ATTACHMENT_CHARS = 16000
MAX_HISTORY_MESSAGES = 6
MAX_HISTORY_CONTENT_CHARS = 1500
MAX_INDEX_PREVIEW_CHARS = 8000
MAX_COMPACT_LIST_ITEMS = 10
MAX_SELECTION_REASON_CHARS = 600
MAX_SELECTION_RATIONALE_CHARS = 1200

PREFERRED_ROOTS = ("overview/", "projects/", "papers/", "surveys/", "code/", "meetings/", "experiments/", "tech-notes/", "notes/", "concepts/", "resources/", "qa/")


def prepare_context(payload):
    question = str(payload.get("question") or "").strip()
    if not question:
        raise ValueError("Missing question")

    client = GiteaClient(payload)
    catalog_raw = client.read_text("catalog.json")
    index_text = client.read_text("index.md")
    catalog = catalog_from_raw(catalog_raw)
    pages = visible_catalog_pages(catalog)
    attachments = prepare_attachments(payload.get("attachments") or [])

    token_text = question + "\n" + "\n".join(item.get("fileName") or "" for item in attachments)
    tokens = query_tokens(token_text)
    metadata_ranked = rank_pages_by_metadata(pages, tokens)
    read_pool = build_read_pool(pages, metadata_ranked)
    starter_page_cards = read_starter_page_cards(client, read_pool, tokens)

    return {
        "schema": "research-kb/kb-query-context@2",
        "mode": "query_planning",
        "question": question,
        "conversation": {
            "conversationId": payload.get("conversationId"),
            "messageId": payload.get("messageId"),
            "history": compact_conversation_history(payload.get("conversationHistory") or []),
        },
        "answerPolicy": payload.get("answerPolicy") or {},
        "team": payload.get("team") or {},
        "kb": {
            "catalogPageCount": len(pages),
            "indexPreview": clip(strip_frontmatter(index_text), MAX_INDEX_PREVIEW_CHARS),
            "catalogPages": compact_catalog_pages(pages[:MAX_CATALOG_PAGES]),
            "rankedCatalogPages": compact_catalog_pages(metadata_ranked[:MAX_RANKED_CATALOG_PAGES]),
            "starterPageCards": starter_page_cards,
            "evidencePages": [],
        },
        "attachments": attachments,
        "analysisLimits": {
            "maxCatalogPagesInContext": MAX_CATALOG_PAGES,
            "maxRankedCatalogPages": MAX_RANKED_CATALOG_PAGES,
            "maxStarterPageCards": MAX_STARTER_CARDS,
            "maxSelectedPages": MAX_EVIDENCE_PAGES,
            "recommendedSelectedPages": "1-4",
            "maxEvidencePageChars": MAX_PAGE_CHARS,
            "maxTotalEvidenceChars": MAX_TOTAL_PAGE_CHARS,
            "maxAttachmentCharsPerFile": MAX_ATTACHMENT_CHARS,
            "maxTotalAttachmentChars": MAX_TOTAL_ATTACHMENT_CHARS,
            "maxHistoryMessages": MAX_HISTORY_MESSAGES,
        },
        "instructions": {
            "scopeSelection": "openclaw_must_decide",
            "knowledgeBaseFirst": True,
            "allowNonKbSupplementWhenInsufficient": True,
            "answerBodyTemplate": "free_form: organize naturally for the user question; do not force a rigid body template.",
            "mustEndWithReferences": True,
            "referenceSection": "Answer must end with ## \u53c2\u8003\u6765\u6e90. List supporting wiki pages and, when available, sourceTraces such as archived source files, repository URLs, commits, or file names.",
            "selectionRule": "Use catalogPages, rankedCatalogPages, indexPreview, starterPageCards, the user question, and temporary attachments to reason about which KB pages are needed. starterPageCards are only exploration aids, not final evidence. Select the smallest sufficient set of KB pages, normally 1-4 pages and never more than analysisLimits.maxSelectedPages. You may select any visible catalog page, including pages not shown in starterPageCards.",
            "fetchRule": "Before producing the final answer, write a page selection JSON and run the fetch command. Cite only stable KB pages returned in fetched evidencePages.",
            "contextBudgetRule": "Do not paste full context or evidence JSON into chat. Read the JSON files from disk, keep page-selection.json and answer.json compact, and write valid JSON files before running the next command. For Markdown answers with quotes or tables, write answer.json through json.dump/json.dumps instead of hand-escaping a long JSON string.",
            "insufficientEvidenceRule": "If fetched KB evidence is insufficient, state that the knowledge base content cannot answer first, then optionally add clearly labelled non-KB or attachment-based supplement.",
            "qaPersistenceRule": "Only persist high-value reusable QA when stable KB pages support the answer; do not persist answers primarily grounded in temporary attachments.",
            "qaEvaluationRule": "Before setting highValue or qa.write, output qaEvaluation with reuseValue, synthesisDepth, evidenceQuality, stability, actionability, attachmentDriven, ephemeral, and reason. Each score is 0 or 1; total must be at least 4 and all hard gates must pass.",
        },
        "resultContract": {
            "pageSelectionFields": ["selectedPages", "rationale", "unresolvedQuestions"],
            "fetchCommand": "python3 scripts/run_task.py fetch --input <payload.json> --context <context.json> --selection <page-selection.json> --evidence-output <evidence.json>",
            "answerJsonFields": ["answer", "knowledgeSufficient", "sources", "usedAttachments", "highValue", "qaEvaluation", "qa", "errors"],
            "applyCommand": "python3 scripts/run_task.py apply --input <payload.json> --context <context.json> --evidence <evidence.json> --answer <answer.json>",
        },
    }


def fetch_evidence(payload, context, selection_doc):
    selection_doc = normalize_selection_doc(selection_doc)
    question = str(context.get("question") or payload.get("question") or "").strip()
    client = GiteaClient(payload)
    catalog = catalog_from_raw(client.read_text("catalog.json"))
    pages = visible_catalog_pages(catalog)
    by_path = {page.get("path") or "": page for page in pages if page.get("path")}
    selected = selected_page_requests(selection_doc)

    evidence_pages = []
    missing_pages = []
    total_chars = 0
    seen = set()
    for request in selected:
        path = request.get("path") or ""
        if not path or path in seen:
            continue
        seen.add(path)
        catalog_page = by_path.get(path)
        if not catalog_page:
            missing_pages.append({"path": path, "reason": "not_found_or_hidden"})
            continue
        raw = client.read_text(path)
        frontmatter = parse_frontmatter(raw)
        body = strip_frontmatter(raw)
        remaining_chars = MAX_TOTAL_PAGE_CHARS - total_chars
        if remaining_chars <= 0:
            break
        clipped = clip(body, min(MAX_PAGE_CHARS, remaining_chars))
        total_chars += len(clipped)
        evidence_pages.append({
            "path": path,
            "title": frontmatter.get("title") or catalog_page.get("title") or path,
            "type": frontmatter.get("type") or catalog_page.get("type") or path.split("/", 1)[0],
            "keywords": compact_text_list(frontmatter.get("keywords") or catalog_page.get("keywords") or [], MAX_COMPACT_LIST_ITEMS, 80),
            "projectIds": compact_text_list(frontmatter.get("projectIds") or catalog_page.get("projectIds") or [], MAX_COMPACT_LIST_ITEMS, 80),
            "sourceIds": compact_text_list(frontmatter.get("sourceIds") or catalog_page.get("sourceIds") or [], MAX_COMPACT_LIST_ITEMS, 80),
            "sourceTraces": normalize_source_traces(frontmatter.get("sources") or [], frontmatter.get("sourceIds") or catalog_page.get("sourceIds") or []),
            "updatedAt": frontmatter.get("updatedAt") or catalog_page.get("updatedAt") or "",
            "selectionReason": clip(request.get("reason") or request.get("expectedUse") or "", MAX_SELECTION_REASON_CHARS),
            "content": clipped,
        })
        if len(evidence_pages) >= MAX_EVIDENCE_PAGES or total_chars >= MAX_TOTAL_PAGE_CHARS:
            break

    return {
        "schema": "research-kb/kb-query-evidence@1",
        "question": question,
        "selectionRationale": clip(selection_doc.get("rationale") or selection_doc.get("reason") or "", MAX_SELECTION_RATIONALE_CHARS),
        "selectionParseError": clip(selection_doc.get("selectionParseError") or "", MAX_SELECTION_RATIONALE_CHARS),
        "unresolvedQuestions": compact_text_list(selection_doc.get("unresolvedQuestions") or [], 6, MAX_SELECTION_REASON_CHARS),
        "selectedPageCount": len(selected),
        "evidencePages": evidence_pages,
        "missingPages": missing_pages,
        "attachments": context.get("attachments") or [],
        "analysisLimits": context.get("analysisLimits") or {},
        "instructions": {
            "citeOnlyEvidencePages": True,
            "mustEndWithReferences": True,
            "temporaryAttachmentsAreNotStableSources": True,
        },
    }


def normalize_selection_doc(selection_doc):
    if isinstance(selection_doc, dict):
        return selection_doc
    if isinstance(selection_doc, list):
        return {"selectedPages": selection_doc}
    raise ValueError("page-selection JSON must be an object or an array of selected pages")


def selected_page_requests(selection_doc):
    raw_items = (
        selection_doc.get("selectedPages")
        or selection_doc.get("pages")
        or selection_doc.get("sources")
        or selection_doc.get("pagePaths")
        or []
    )
    if isinstance(raw_items, (str, dict)):
        raw_items = [raw_items]
    result = []
    for item in raw_items:
        if isinstance(item, str):
            path = item
            request = {"path": path}
        elif isinstance(item, dict):
            path = item.get("path") or item.get("pagePath") or item.get("url") or ""
            request = dict(item)
            request["path"] = path
        else:
            continue
        path = safe_catalog_path(request.get("path") or "")
        if not path:
            continue
        request["path"] = path
        result.append(request)
    return result[:MAX_EVIDENCE_PAGES]


def safe_catalog_path(path):
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


def compact_conversation_history(raw_history):
    if not isinstance(raw_history, list):
        return []
    result = []
    for item in raw_history[-MAX_HISTORY_MESSAGES:]:
        if not isinstance(item, dict):
            continue
        result.append({
            "id": item.get("id"),
            "role": item.get("role") or "",
            "content": clip(item.get("content") or "", MAX_HISTORY_CONTENT_CHARS),
            "sources": compact_history_sources(item.get("sources") or []),
            "createdQaPath": item.get("createdQaPath") or "",
            "createdAt": item.get("createdAt") or "",
        })
    return result


def compact_history_sources(raw_sources):
    if isinstance(raw_sources, dict):
        raw_sources = [raw_sources]
    result = []
    for source in raw_sources or []:
        if not isinstance(source, dict):
            continue
        result.append({
            "path": source.get("path") or "",
            "title": source.get("title") or "",
            "type": source.get("type") or "",
        })
    return result[:10]


def prepare_attachments(raw_attachments):
    prepared = []
    total = 0
    for item in raw_attachments:
        if not isinstance(item, dict):
            continue
        preview = read_text_preview(item.get("storagePath"), max_chars=MAX_ATTACHMENT_CHARS)
        total += len(preview)
        if total > MAX_TOTAL_ATTACHMENT_CHARS:
            preview = preview[: max(0, len(preview) - (total - MAX_TOTAL_ATTACHMENT_CHARS))]
        prepared.append({
            "attachmentId": item.get("attachmentId"),
            "fileName": item.get("fileName") or "",
            "mimeType": item.get("mimeType") or "",
            "sha256": item.get("sha256") or "",
            "size": item.get("size") or 0,
            "temporary": True,
            "textPreview": preview,
            "previewAvailable": bool(preview.strip()),
            "note": "This attachment is a temporary query reference and must not be ingested or cited as a stable KB source.",
        })
    return prepared


def compact_catalog_pages(pages):
    result = []
    for page in pages or []:
        result.append({
            "path": page.get("path") or "",
            "title": page.get("title") or page.get("path") or "",
            "type": page.get("type") or "",
            "kbType": page.get("kbType") or "",
            "keywords": compact_text_list(page.get("keywords") or [], MAX_COMPACT_LIST_ITEMS, 80),
            "projectIds": compact_text_list(page.get("projectIds") or [], MAX_COMPACT_LIST_ITEMS, 80),
            "sourceIds": compact_text_list(page.get("sourceIds") or [], MAX_COMPACT_LIST_ITEMS, 80),
            "updatedAt": page.get("updatedAt") or "",
            "relatedConcepts": compact_text_list(page.get("relatedConcepts") or [], MAX_COMPACT_LIST_ITEMS, 120),
            "relatedResources": compact_text_list(page.get("relatedResources") or [], MAX_COMPACT_LIST_ITEMS, 120),
            "relatedCodePages": compact_text_list(page.get("relatedCodePages") or [], MAX_COMPACT_LIST_ITEMS, 120),
            "relatedPages": compact_text_list(page.get("relatedPages") or [], MAX_COMPACT_LIST_ITEMS, 120),
        })
    return result


def compact_text_list(items, limit, max_chars):
    if isinstance(items, (str, int, float)):
        items = [items]
    result = []
    for item in items or []:
        text = str(item).strip()
        if not text:
            continue
        result.append(clip(text, max_chars))
        if len(result) >= limit:
            break
    return result


def rank_pages_by_metadata(pages, tokens):
    scored = []
    for page in pages:
        haystack = " ".join([
            str(page.get("path") or ""),
            str(page.get("title") or ""),
            str(page.get("type") or ""),
            " ".join(str(item) for item in page.get("keywords") or []),
            " ".join(str(item) for item in page.get("projectIds") or []),
            " ".join(str(item) for item in page.get("relatedConcepts") or []),
            " ".join(str(item) for item in page.get("relatedResources") or []),
            " ".join(str(item) for item in page.get("relatedCodePages") or []),
            " ".join(str(item) for item in page.get("relatedPages") or []),
        ])
        score = score_text(haystack, tokens)
        title_score = score_text(str(page.get("title") or ""), tokens) * 2
        if score or title_score:
            scored.append((score + title_score, page))
    scored.sort(key=lambda item: (-item[0], item[1].get("updatedAt") or "", item[1].get("path") or ""))
    return [page for _, page in scored]


def build_read_pool(pages, metadata_ranked):
    pool = []
    pool.extend(metadata_ranked[:MAX_READ_POOL])
    for root in PREFERRED_ROOTS:
        for page in pages:
            path = page.get("path") or ""
            if path.startswith(root):
                pool.append(page)
                break
    if not pool:
        pool.extend(pages[:30])
    result = []
    seen = set()
    for page in pool:
        path = page.get("path") or ""
        if not path or path in seen:
            continue
        seen.add(path)
        result.append(page)
        if len(result) >= MAX_READ_POOL:
            break
    return result


def read_starter_page_cards(client, pages, tokens):
    cards = []
    for page in pages:
        path = page.get("path") or ""
        if not path:
            continue
        raw = client.read_text(path)
        frontmatter = parse_frontmatter(raw)
        body = strip_frontmatter(raw)
        if not body.strip():
            continue
        score = score_text(body, tokens) * 3 + score_text(" ".join([path, page.get("title") or "", " ".join(page.get("keywords") or [])]), tokens)
        if not score and not path.startswith(("overview/", "qa/")):
            continue
        cards.append((score, {
            "path": path,
            "title": frontmatter.get("title") or page.get("title") or path,
            "type": frontmatter.get("type") or page.get("type") or path.split("/", 1)[0],
            "keywords": compact_text_list(frontmatter.get("keywords") or page.get("keywords") or [], MAX_COMPACT_LIST_ITEMS, 80),
            "projectIds": compact_text_list(frontmatter.get("projectIds") or page.get("projectIds") or [], MAX_COMPACT_LIST_ITEMS, 80),
            "sourceIds": compact_text_list(frontmatter.get("sourceIds") or page.get("sourceIds") or [], MAX_COMPACT_LIST_ITEMS, 80),
            "updatedAt": frontmatter.get("updatedAt") or page.get("updatedAt") or "",
            "contentPreview": clip(body, MAX_STARTER_CARD_CHARS),
            "note": "Exploration card only. OpenClaw must still decide whether to fetch and cite this page.",
        }))
    cards.sort(key=lambda item: (-item[0], item[1].get("updatedAt") or "", item[1].get("path") or ""))
    return [card for _, card in cards[:MAX_STARTER_CARDS]]


def normalize_source_traces(raw_sources, source_ids):
    sources = raw_sources
    if isinstance(sources, dict):
        sources = [sources]
    result = []
    for source in sources or []:
        if not isinstance(source, dict):
            continue
        trace = {
            "sourceId": source.get("sourceId") or source.get("id"),
            "sourceType": source.get("sourceType") or source.get("type") or "",
            "platform": source.get("platform") or "",
            "title": source.get("title") or source.get("sourceName") or "",
            "fileName": source.get("fileName") or "",
            "archivedPath": safe_source_file_path(source.get("archivedPath") or source.get("archivePath") or ""),
            "url": source.get("url") or source.get("repoUrl") or "",
            "commitHash": source.get("commitHash") or source.get("latestCommit") or "",
            "branch": source.get("branch") or source.get("defaultBranch") or "",
            "sha256": source.get("sha256") or "",
            "status": source.get("status") or "",
            "ingestedAt": source.get("ingestedAt") or source.get("scannedAt") or "",
        }
        if any(value not in (None, "", []) for value in trace.values()):
            result.append(trace)
    if not result:
        for source_id in source_ids or []:
            if source_id in (None, ""):
                continue
            result.append({"sourceId": source_id})
    return dedupe_source_traces(result)[:10]


def safe_source_file_path(path):
    if not path:
        return ""
    try:
        value = safe_relpath(path)
    except ValueError:
        return ""
    if value.startswith("source_files/"):
        return value
    return ""


def dedupe_source_traces(traces):
    result = []
    seen = set()
    for trace in traces or []:
        key = "|".join(str(trace.get(field) or "") for field in ["sourceId", "archivedPath", "url", "commitHash", "fileName", "title"])
        if key in seen:
            continue
        seen.add(key)
        result.append(trace)
    return result

