import json
import re

from catalog import catalog_entry, catalog_from_raw, merge_catalog, render_index
from gitea_api import GiteaClient
from utils import now, safe_relpath, sha256_text, slugify, strip_frontmatter, unique

HIGH_VALUE_SCORE_KEYS = ["reuseValue", "synthesisDepth", "evidenceQuality", "stability", "actionability"]
REF_HEADING = "\u53c2\u8003\u6765\u6e90"
SOURCE_TRACE_LABEL = "\u6e90\u6587\u4ef6/\u6765\u6e90"
NO_KB_SOURCE_LINE = "- \u77e5\u8bc6\u5e93\u4e2d\u672a\u627e\u5230\u53ef\u652f\u6491\u672c\u95ee\u9898\u7684\u9875\u9762\u3002"


def apply_answer(payload, answer_doc, context):
    answer = str(answer_doc.get("answer") or "").strip()
    if not answer:
        raise ValueError("OpenClaw answer.json must contain a non-empty answer")
    if "evidence" not in context:
        raise ValueError("kb_query apply requires an evidence JSON produced by fetch")

    knowledge_sufficient = bool(answer_doc.get("knowledgeSufficient"))
    sources = normalize_sources(answer_doc.get("sources") or [], context)
    validate_answer_contract(answer_doc, sources, knowledge_sufficient)
    answer = ensure_reference_section(answer, sources)
    qa_evaluation = normalize_qa_evaluation(answer_doc)
    result = {
        "answer": answer,
        "sources": sources,
        "processedSources": ["team-kb"],
        "createdPages": [],
        "updatedPages": [],
        "skippedSources": [],
        "errors": normalize_errors(answer_doc.get("errors") or []),
        "commitId": "",
        "knowledgeSufficient": knowledge_sufficient,
        "usedAttachments": answer_doc.get("usedAttachments") or [],
        "qaEvaluation": qa_evaluation,
    }

    qa_result = maybe_write_qa(payload, answer_doc, context, answer, sources, knowledge_sufficient, qa_evaluation)
    result.update({key: value for key, value in qa_result.items() if key in {"createdQaPath", "commitId"}})
    result["createdPages"] = qa_result.get("createdPages") or []
    result["updatedPages"] = qa_result.get("updatedPages") or []
    result["skippedSources"] = result["skippedSources"] + (qa_result.get("skippedSources") or [])
    return result


def validate_answer_contract(answer_doc, sources, knowledge_sufficient):
    if knowledge_sufficient and not sources:
        raise ValueError("knowledgeSufficient=true requires at least one fetched KB source")
    if bool(answer_doc.get("highValue") or (answer_doc.get("qa") or {}).get("write")) and not knowledge_sufficient:
        raise ValueError("high-value QA cannot be requested when knowledgeSufficient=false")


def normalize_sources(raw_sources, context):
    evidence_pages = (context.get("kb") or {}).get("evidencePages") or []
    known = {}
    for page in evidence_pages:
        path = page.get("path") or ""
        if path:
            known[path] = page

    if isinstance(raw_sources, (dict, str)):
        raw_sources = [raw_sources]

    normalized = []
    rejected = []
    for item in raw_sources or []:
        if isinstance(item, str):
            item = {"path": item}
        elif not isinstance(item, dict):
            rejected.append("<invalid-source>")
            continue
        path = safe_relpath(item.get("path") or item.get("pagePath") or "")
        if not path or path.startswith("source_files/"):
            rejected.append(path or "<empty>")
            continue
        known_page = known.get(path)
        if not known_page:
            rejected.append(path)
            continue
        normalized.append({
            "path": path,
            "title": known_page.get("title") or item.get("title") or path,
            "type": known_page.get("type") or item.get("type") or path.split("/", 1)[0],
            "snippet": item.get("snippet") or item.get("excerpt") or "",
            "sourceIds": known_page.get("sourceIds") or item.get("sourceIds") or [],
            "sourceTraces": normalize_source_traces(known_page.get("sourceTraces") or []),
            "updatedAt": known_page.get("updatedAt") or item.get("updatedAt") or "",
        })
    if rejected:
        raise ValueError("answer sources must be fetched evidence pages; rejected: " + ", ".join(unique(rejected)))
    return dedupe_sources(normalized)


def normalize_source_traces(raw_traces):
    traces = raw_traces
    if isinstance(traces, dict):
        traces = [traces]
    normalized = []
    for trace in traces or []:
        if not isinstance(trace, dict):
            continue
        item = {
            "sourceId": trace.get("sourceId") or trace.get("id"),
            "sourceType": trace.get("sourceType") or trace.get("type") or "",
            "platform": trace.get("platform") or "",
            "title": trace.get("title") or trace.get("sourceName") or "",
            "fileName": trace.get("fileName") or "",
            "archivedPath": safe_source_file_path(trace.get("archivedPath") or trace.get("archivePath") or ""),
            "url": trace.get("url") or trace.get("repoUrl") or "",
            "commitHash": trace.get("commitHash") or trace.get("latestCommit") or "",
            "branch": trace.get("branch") or trace.get("defaultBranch") or "",
            "sha256": trace.get("sha256") or "",
            "status": trace.get("status") or "",
            "ingestedAt": trace.get("ingestedAt") or trace.get("scannedAt") or "",
        }
        if any(value not in (None, "", []) for value in item.values()):
            normalized.append(item)
    return dedupe_source_traces(normalized)[:10]


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


def dedupe_sources(sources):
    result = []
    seen = set()
    for source in sources:
        path = source.get("path") or ""
        if not path or path in seen:
            continue
        seen.add(path)
        result.append(source)
    return result


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


def ensure_reference_section(answer, sources):
    body = remove_reference_section(answer)
    lines = [body.rstrip(), "", f"## {REF_HEADING}"]
    if sources:
        for source in sources:
            title = source.get("title") or source.get("path")
            path = source.get("path") or ""
            details = []
            snippet = str(source.get("snippet") or "").strip()
            if snippet:
                details.append(snippet)
            trace_text = render_source_traces(source.get("sourceTraces") or [])
            if trace_text:
                details.append(f"{SOURCE_TRACE_LABEL}: {trace_text}")
            suffix = f": {'; '.join(details)}" if details else ""
            lines.append(f"- {title} (`{path}`){suffix}")
    else:
        lines.append(NO_KB_SOURCE_LINE)
    return "\n".join(lines).strip()


def remove_reference_section(answer):
    pattern = r"(?ms)\n{0,2}#{1,6}\s*" + re.escape(REF_HEADING) + r"\s*\n.*\Z"
    return re.sub(pattern, "", answer or "").strip()


def render_source_traces(traces):
    parts = []
    for trace in traces[:5]:
        label = trace.get("title") or trace.get("fileName") or trace.get("sourceType") or trace.get("sourceId") or "source"
        loc = trace.get("archivedPath") or trace.get("url") or ""
        commit = trace.get("commitHash") or ""
        if loc and commit:
            parts.append(f"{label} ({loc} @ {commit})")
        elif loc:
            parts.append(f"{label} ({loc})")
        elif commit:
            parts.append(f"{label} (@ {commit})")
        else:
            parts.append(str(label))
    return "; ".join(parts)


def maybe_write_qa(payload, answer_doc, context, answer, sources, knowledge_sufficient, qa_evaluation):
    qa = answer_doc.get("qa") or {}
    requested = bool(qa.get("write") or answer_doc.get("writeQa") or answer_doc.get("highValue"))
    allowed = bool((payload.get("answerPolicy") or {}).get("writeHighValueAnswerToQa"))
    if not requested:
        return {}
    if not allowed:
        return {"skippedSources": ["high-value QA writing is disabled by answerPolicy"]}
    if not knowledge_sufficient:
        return {"skippedSources": ["KB evidence is insufficient; qa page was not persisted"]}
    stable_sources = [item for item in sources if item.get("path") and not item.get("path", "").startswith("source_files/")]
    if not stable_sources:
        return {"skippedSources": ["missing stable KB sources; qa page was not persisted"]}
    gate = high_value_gate(qa_evaluation, stable_sources)
    if not gate["ok"]:
        return {"skippedSources": [gate["reason"]]}

    client = GiteaClient(payload)
    path = validate_qa_path(qa.get("path") or answer_doc.get("createdQaPath") or generated_qa_path(context.get("question") or payload.get("question")))
    title = qa.get("title") or f"High-value QA: {(context.get('question') or payload.get('question') or '')[:50]}"
    content = qa.get("content") or render_qa_content(title, context.get("question") or payload.get("question") or "", answer, stable_sources, qa, qa_evaluation)
    content = build_qa_page(path, title, content, stable_sources, qa)
    existed = client.exists(path)
    client.upsert_text(path, content, f"OpenClaw update {path}")
    commit = client.last_commit

    page = {
        "path": path,
        "title": title,
        "type": "qa",
        "kbType": "qa",
        "sourceIds": unique(sum([source.get("sourceIds") or [] for source in stable_sources], [])),
        "projectIds": qa.get("projectIds") or ["general"],
        "keywords": qa.get("keywords") or [],
        "contentHash": sha256_text(strip_frontmatter(content)),
        "sourceStatus": "active",
    }
    catalog = catalog_from_raw(client.read_text("catalog.json"))
    catalog = merge_catalog(catalog, [catalog_entry(page)])
    client.upsert_text("catalog.json", json.dumps(catalog, ensure_ascii=False, indent=2), "OpenClaw update catalog.json")
    commit = client.last_commit
    client.upsert_text("index.md", render_index(catalog), "OpenClaw update index.md")
    commit = client.last_commit

    entry = catalog_entry(page)
    return {
        "createdQaPath": path,
        "createdPages": [] if existed else [entry],
        "updatedPages": [entry] if existed else [],
        "commitId": commit,
    }


def normalize_qa_evaluation(answer_doc):
    qa = answer_doc.get("qa") or {}
    evaluation = answer_doc.get("qaEvaluation") or qa.get("evaluation") or {}
    if not isinstance(evaluation, dict):
        return {}
    normalized = dict(evaluation)
    normalized["score"] = high_value_score(normalized)
    return normalized


def high_value_gate(evaluation, stable_sources):
    if not evaluation:
        return {"ok": False, "reason": "missing high-value QA evaluation; qa page was not persisted"}
    if not stable_sources:
        return {"ok": False, "reason": "missing stable KB sources; qa page was not persisted"}
    if bool(evaluation.get("attachmentDriven")):
        return {"ok": False, "reason": "answer is primarily attachment-driven; qa page was not persisted"}
    if bool(evaluation.get("ephemeral")):
        return {"ok": False, "reason": "question is ephemeral or one-off; qa page was not persisted"}
    score = high_value_score(evaluation)
    if score < 4:
        return {"ok": False, "reason": f"high-value QA score is too low ({score}/5); qa page was not persisted"}
    if not str(evaluation.get("reason") or "").strip():
        return {"ok": False, "reason": "missing high-value QA rationale; qa page was not persisted"}
    return {"ok": True, "reason": ""}


def high_value_score(evaluation):
    explicit = evaluation.get("score")
    if isinstance(explicit, (int, float)):
        return max(0, min(5, int(explicit)))
    if isinstance(explicit, str) and explicit.strip().isdigit():
        return max(0, min(5, int(explicit.strip())))
    total = 0
    for key in HIGH_VALUE_SCORE_KEYS:
        total += score_part(evaluation.get(key))
    return max(0, min(5, total))


def score_part(value):
    if isinstance(value, bool):
        return 1 if value else 0
    if isinstance(value, (int, float)):
        return 1 if value > 0 else 0
    if isinstance(value, str):
        lowered = value.strip().lower()
        return 1 if lowered in {"1", "true", "yes", "y", "strong"} else 0
    return 0


def validate_qa_path(path):
    value = safe_relpath(path)
    if not value:
        raise ValueError("QA path is empty")
    if not value.startswith("qa/"):
        value = "qa/" + value.rsplit("/", 1)[-1]
    if not value.endswith(".md"):
        value += ".md"
    return value


def generated_qa_path(question):
    return f"qa/{now()[:10]}-{slugify(question, 60)}.md"


def render_qa_content(title, question, answer, sources, qa, qa_evaluation):
    evidence = "\n".join(render_evidence_line(source) for source in sources)
    scenario = qa.get("scenario") or "Team members can reuse this answer when the same or a similar question appears, then verify details through the references."
    reason = qa_evaluation.get("reason") or "not recorded"
    score = qa_evaluation.get("score")
    return f"""# {title}

## Question

{question}

## Answer

{answer}

## Evidence Pages

{evidence or '- Not recorded'}

## High-Value Evaluation

- Score: {score}/5
- Reason: {reason}

## Reuse Scenario

{scenario}

## Updated At

{now()}
"""


def render_evidence_line(source):
    title = source.get("title") or source.get("path")
    path = source.get("path") or ""
    traces = render_source_traces(source.get("sourceTraces") or [])
    suffix = f"; {SOURCE_TRACE_LABEL}: {traces}" if traces else ""
    return f"- [{title}]({path}){suffix}"


def build_qa_page(path, title, body, sources, qa):
    clean_body = strip_frontmatter(body)
    data = {
        "id": qa.get("id") or path.replace("/", "-").replace(".md", ""),
        "title": title,
        "type": "qa",
        "kbType": "qa",
        "projectIds": qa.get("projectIds") or ["general"],
        "tags": qa.get("tags") or ["high-value-qa"],
        "keywords": qa.get("keywords") or [],
        "createdAt": qa.get("createdAt") or now(),
        "updatedAt": now(),
        "generatedBy": "openclaw:kb_query",
        "contentHash": sha256_text(clean_body),
        "sourceStatus": "active",
        "sources": [{
            "sourceType": "kb_page",
            "platform": "gitea",
            "title": source.get("title") or source.get("path"),
            "url": source.get("path"),
            "status": "active",
            "ingestedAt": now(),
        } for source in sources],
    }
    lines = ["---"]
    for key, value in data.items():
        lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + clean_body.strip() + "\n"


def normalize_errors(errors):
    if not isinstance(errors, list):
        return [str(errors)] if errors else []
    return [str(item) for item in errors if str(item).strip()]
