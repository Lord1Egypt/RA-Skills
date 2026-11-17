import argparse
import re
import sys
from pathlib import Path

from query_context import fetch_evidence, prepare_context
from qa_writer import apply_answer
from task_io import parse_json_lenient, print_json, read_json_file, read_json_file_lenient, read_payload, write_json_file, write_result


ANSWER_BOUNDARY_KEYS = (
    "knowledgeSufficient",
    "sources",
    "usedAttachments",
    "highValue",
    "qaEvaluation",
    "qa",
    "errors",
)


def main():
    parser = argparse.ArgumentParser(description="Research KB query helper")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare", help="Read KB catalog, page cards, and reference attachments into a query planning context")
    prepare.add_argument("--input", required=True, help="Backend payload JSON path")
    prepare.add_argument("--context-output", required=True, help="Where to write the generated context JSON")

    fetch = subparsers.add_parser("fetch", help="Read OpenClaw-selected KB pages into an evidence bundle")
    fetch.add_argument("--input", required=True, help="Backend payload JSON path")
    fetch.add_argument("--context", required=True, help="Context JSON produced by prepare")
    fetch.add_argument("--selection", required=True, help="OpenClaw page-selection JSON path")
    fetch.add_argument("--evidence-output", required=True, help="Where to write fetched evidence JSON")

    apply = subparsers.add_parser("apply", help="Validate OpenClaw answer, optionally persist QA, and write backend result")
    apply.add_argument("--input", required=True, help="Backend payload JSON path")
    apply.add_argument("--context", required=True, help="Context JSON produced by prepare")
    apply.add_argument("--evidence", required=True, help="Evidence JSON produced by fetch")
    apply.add_argument("--answer", required=True, help="OpenClaw-generated answer JSON path")
    apply.add_argument("--result-output", help="Where to write backend result JSON; defaults to payload.resultFile")

    args = parser.parse_args()
    if args.command == "prepare":
        run_prepare(args)
    elif args.command == "fetch":
        run_fetch(args)
    elif args.command == "apply":
        run_apply(args)


def run_prepare(args):
    payload = read_payload(args.input)
    try:
        context = prepare_context(payload)
        write_json_file(args.context_output, context)
        print_json(context_summary(context, args.context_output))
    except Exception as exc:
        result = {"success": False, "errors": [str(exc)], "commitId": ""}
        result_path = payload.get("resultFile")
        if result_path:
            write_result(result_path, result)
        print_json(result)
        sys.exit(1)


def run_fetch(args):
    payload = read_payload(args.input)
    try:
        context = read_json_file(args.context)
        try:
            selection_doc = read_json_file_lenient(args.selection)
        except Exception as selection_exc:
            selection_doc = invalid_selection_doc(selection_exc)
        evidence = fetch_evidence(payload, context, selection_doc)
        write_json_file(args.evidence_output, evidence)
        print_json(evidence_summary(evidence, args.evidence_output))
    except Exception as exc:
        result = {"success": False, "errors": [str(exc)], "commitId": ""}
        result_path = payload.get("resultFile")
        if result_path:
            write_result(result_path, result)
        print_json(result)
        sys.exit(1)


def run_apply(args):
    payload = read_payload(args.input)
    try:
        context = read_json_file(args.context)
        evidence = read_json_file(args.evidence)
        context = merge_evidence_context(context, evidence)
        try:
            answer_doc = read_json_file_lenient(args.answer)
        except Exception as answer_exc:
            answer_doc = recover_invalid_answer_doc(args.answer, context, answer_exc)
        result = apply_answer_safely(payload, answer_doc, context)
        result_path = args.result_output or payload.get("resultFile")
        if result_path:
            write_result(result_path, result)
        print_json(result)
    except Exception as exc:
        context = failure_context(payload, locals().get("context") if isinstance(locals().get("context"), dict) else {})
        result = apply_answer(payload, invalid_answer_doc(context, exc), context)
        result_path = args.result_output or payload.get("resultFile")
        if result_path:
            write_result(result_path, result)
        print_json(result)


def apply_answer_safely(payload, answer_doc, context):
    try:
        return apply_answer(payload, answer_doc, context)
    except Exception as exc:
        if not isinstance(answer_doc, dict) or not answer_doc.get("_recoveredFromMalformedAnswerJson"):
            raise
        fallback = dict(answer_doc)
        fallback["sources"] = evidence_page_sources(context)
        if bool(fallback.get("knowledgeSufficient")) and not fallback["sources"]:
            fallback["knowledgeSufficient"] = False
        fallback["highValue"] = False
        fallback["qa"] = {"write": False}
        fallback["qaEvaluation"] = recovered_qa_evaluation(
            "Recovered from malformed answer JSON; QA persistence is disabled."
        )
        errors = fallback.get("errors") if isinstance(fallback.get("errors"), list) else []
        fallback["errors"] = errors + [f"Recovered answer source fallback: {exc}"]
        try:
            return apply_answer(payload, fallback, context)
        except Exception as fallback_exc:
            final = invalid_answer_doc(context, fallback_exc)
            final["errors"] = final.get("errors", []) + fallback["errors"]
            return apply_answer(payload, final, context)


def merge_evidence_context(context, evidence):
    merged = dict(context or {})
    kb = dict(merged.get("kb") or {})
    kb["evidencePages"] = evidence.get("evidencePages") or []
    merged["kb"] = kb
    merged["evidence"] = evidence
    return merged


def invalid_selection_doc(exc):
    message = str(exc)
    return {
        "selectedPages": [],
        "rationale": "OpenClaw page-selection.json was not valid JSON, so no KB page could be fetched deterministically.",
        "unresolvedQuestions": [
            "page-selection.json parse failed; answer must treat fetched KB evidence as insufficient."
        ],
        "selectionParseError": message,
    }


def recover_invalid_answer_doc(answer_path, context, exc):
    message = str(exc)
    raw = read_text_lossy(answer_path)
    answer = extract_loose_json_string_field(raw, "answer")
    if not answer:
        return invalid_answer_doc(context, exc)

    metadata = recover_answer_metadata(answer_metadata_region(raw))
    sources = metadata.get("sources") if isinstance(metadata.get("sources"), list) else []
    if not sources:
        sources = evidence_page_sources(context)

    knowledge_sufficient = metadata.get("knowledgeSufficient")
    if not isinstance(knowledge_sufficient, bool):
        knowledge_sufficient = bool(sources)

    errors = metadata.get("errors") if isinstance(metadata.get("errors"), list) else []
    return {
        "answer": answer,
        "knowledgeSufficient": knowledge_sufficient,
        "sources": sources,
        "usedAttachments": metadata.get("usedAttachments") if isinstance(metadata.get("usedAttachments"), list) else [],
        "highValue": False,
        "qaEvaluation": recovered_qa_evaluation(
            "Recovered from malformed answer JSON; QA persistence is disabled."
        ),
        "qa": {"write": False},
        "errors": errors + [f"answer.json was malformed and recovered: {message}"],
        "_recoveredFromMalformedAnswerJson": True,
    }


def recover_answer_metadata(raw):
    metadata = {}
    for key in ["knowledgeSufficient", "highValue"]:
        match = re.search(rf'"{re.escape(key)}"\s*:\s*(true|false)', raw, flags=re.IGNORECASE)
        if match:
            metadata[key] = match.group(1).lower() == "true"

    for key in ["sources", "usedAttachments", "errors"]:
        value_text = extract_json_value(raw, key)
        if not value_text:
            continue
        try:
            value = parse_json_lenient(value_text, f"answer.{key}")
        except Exception:
            continue
        metadata[key] = value
    return metadata


def read_text_lossy(path):
    try:
        return Path(path).read_bytes().decode("utf-8-sig", errors="replace")
    except Exception:
        return ""


def answer_metadata_region(raw):
    if not raw:
        return ""
    match = re.search(r'"answer"\s*:\s*"', raw)
    if not match:
        return raw
    tail = raw[match.end():]
    boundary = find_answer_metadata_boundary(tail)
    return tail[boundary.start():] if boundary else raw


def extract_loose_json_string_field(raw, field):
    if not raw:
        return ""
    match = re.search(rf'"{re.escape(field)}"\s*:\s*"', raw)
    if not match:
        return ""
    start = match.end()
    tail = raw[start:]
    boundary = find_answer_metadata_boundary(tail)
    if boundary:
        content = tail[:boundary.start()]
    else:
        content = tail
        brace = content.rfind("}")
        if brace >= 0:
            content = content[:brace]
    content = strip_json_string_terminator(content)
    return decode_jsonish_string(content).strip()


def find_answer_metadata_boundary(tail):
    key_pattern = "(?:" + "|".join(re.escape(key) for key in ANSWER_BOUNDARY_KEYS) + ")"
    patterns = [
        r'"\s*,\s*"' + key_pattern + r'"\s*:',
        r'"\s*\n\s*"' + key_pattern + r'"\s*:',
    ]
    matches = [match for pattern in patterns for match in [re.search(pattern, tail, flags=re.DOTALL)] if match]
    if not matches:
        return None
    return min(matches, key=lambda match: match.start())


def strip_json_string_terminator(value):
    content = str(value or "").rstrip()
    if content.endswith(","):
        content = content[:-1].rstrip()
    if content.endswith('"'):
        content = content[:-1]
    return content


def decode_jsonish_string(value):
    result = []
    index = 0
    while index < len(value):
        char = value[index]
        if char != "\\" or index + 1 >= len(value):
            result.append(char)
            index += 1
            continue

        next_char = value[index + 1]
        if next_char == "n":
            result.append("\n")
            index += 2
        elif next_char == "r":
            result.append("\r")
            index += 2
        elif next_char == "t":
            result.append("\t")
            index += 2
        elif next_char == "b":
            result.append("\b")
            index += 2
        elif next_char == "f":
            result.append("\f")
            index += 2
        elif next_char in {'"', "\\", "/"}:
            result.append(next_char)
            index += 2
        elif next_char == "u" and index + 5 < len(value):
            hex_value = value[index + 2:index + 6]
            try:
                result.append(chr(int(hex_value, 16)))
                index += 6
            except ValueError:
                result.append(char)
                index += 1
        else:
            result.append(char)
            index += 1
    return "".join(result)


def extract_json_value(raw, key):
    match = re.search(rf'"{re.escape(key)}"\s*:', raw)
    if not match:
        return ""
    index = match.end()
    while index < len(raw) and raw[index].isspace():
        index += 1
    if index >= len(raw):
        return ""

    if raw[index] in "[{":
        return extract_balanced_json(raw, index)

    literal = re.match(r"(true|false|null|-?\d+(?:\.\d+)?)", raw[index:], flags=re.IGNORECASE)
    return literal.group(1) if literal else ""


def extract_balanced_json(raw, start):
    open_char = raw[start]
    close_char = "]" if open_char == "[" else "}"
    depth = 0
    in_string = False
    escape = False
    for index in range(start, len(raw)):
        char = raw[index]
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == open_char:
            depth += 1
        elif char == close_char:
            depth -= 1
            if depth == 0:
                return raw[start:index + 1]
    return ""


def evidence_page_sources(context):
    pages = (context.get("kb") or {}).get("evidencePages") or []
    sources = []
    for page in pages:
        path = page.get("path") or ""
        if not path:
            continue
        content = str(page.get("content") or "")
        snippet = first_text_line(content)[:240]
        sources.append({
            "path": path,
            "title": page.get("title") or path,
            "type": page.get("type") or path.split("/", 1)[0],
            "snippet": snippet,
        })
    return sources


def first_text_line(text):
    for line in str(text or "").splitlines():
        clean = line.strip().lstrip("#").strip()
        if clean:
            return clean
    return ""


def recovered_qa_evaluation(reason):
    return {
        "reuseValue": 0,
        "synthesisDepth": 0,
        "evidenceQuality": 0,
        "stability": 0,
        "actionability": 0,
        "attachmentDriven": False,
        "ephemeral": True,
        "reason": reason,
    }


def invalid_answer_doc(context, exc):
    message = str(exc)
    question = context.get("question") or ""
    return {
        "answer": (
            "OpenClaw 没有写出可用的 answer.json，且无法从文件中救出可展示答案，因此本轮没有可用答案。\n\n"
            f"问题：{question}\n\n"
            f"错误信息：{message}\n\n"
            "可以重新提问，或把问题范围缩小后再试。"
        ),
        "knowledgeSufficient": False,
        "sources": [],
        "usedAttachments": [],
        "highValue": False,
        "qaEvaluation": recovered_qa_evaluation("OpenClaw answer JSON was invalid; QA persistence is not allowed."),
        "qa": {"write": False},
        "errors": [message],
    }


def failure_context(payload, context):
    merged = dict(context or {})
    merged.setdefault("question", payload.get("question") or "")
    kb = dict(merged.get("kb") or {})
    kb.setdefault("evidencePages", [])
    merged["kb"] = kb
    merged.setdefault("evidence", {
        "schema": "research-kb/kb-query-evidence@1",
        "question": merged.get("question") or "",
        "evidencePages": [],
        "missingPages": [],
        "attachments": merged.get("attachments") or [],
    })
    return merged


def context_summary(context, context_output):
    kb = context.get("kb") or {}
    return {
        "success": True,
        "mode": "prepare",
        "contextFile": context_output,
        "schema": context.get("schema"),
        "question": context.get("question") or "",
        "catalogPageCount": kb.get("catalogPageCount") or 0,
        "visibleCatalogPageCount": len(kb.get("catalogPages") or []),
        "rankedCatalogPageCount": len(kb.get("rankedCatalogPages") or []),
        "starterPageCardCount": len(kb.get("starterPageCards") or []),
        "attachmentCount": len(context.get("attachments") or []),
        "analysisLimits": context.get("analysisLimits") or {},
        "next": "Read contextFile from disk, keep it out of chat, write page-selection.json, then run fetch.",
    }


def evidence_summary(evidence, evidence_output):
    pages = evidence.get("evidencePages") or []
    return {
        "success": True,
        "mode": "fetch",
        "evidenceFile": evidence_output,
        "schema": evidence.get("schema"),
        "evidencePageCount": len(pages),
        "evidenceChars": sum(len(page.get("content") or "") for page in pages),
        "evidencePages": [
            {
                "path": page.get("path") or "",
                "title": page.get("title") or "",
                "type": page.get("type") or "",
                "contentChars": len(page.get("content") or ""),
            }
            for page in pages
        ],
        "missingPageCount": len(evidence.get("missingPages") or []),
        "analysisLimits": evidence.get("analysisLimits") or {},
        "next": "Read evidenceFile from disk, keep it out of chat, write valid answer.json, then run apply.",
    }


if __name__ == "__main__":
    main()


