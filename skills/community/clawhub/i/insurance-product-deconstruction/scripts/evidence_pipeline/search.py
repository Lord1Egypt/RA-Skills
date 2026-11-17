"""Deterministic local evidence search and compaction."""

from __future__ import annotations

import re
from collections import defaultdict

# Patterns that identify table-of-contents or reading-guide lines
_TOC_DOTS = re.compile(r"[.…·]{4,}|[．。]{4,}")
_TOC_HEADERS = re.compile(r"条款目录|阅读指引|目\s*录|本条款第\s*\d+\s*页")
_TOC_SECTION_REFS = re.compile(
    r"(?:\d+\.\d+\s*\S+\s*){2,}"  # "3.4保险金给付 8.4撤销已指定的第二投保人"
    r"|\d+\.\S+\s+\d+\.\S+"       # "4.保单红利 9.合同解除"
)
_TOC_PAGE_REFS = re.compile(r"\.{4,}\s*\d+\.?\d*$")  # "的内容..............1.4"
_FOOTER = re.compile(r"本条款第\s*\d+\s*页\s*共\s*\d+\s*页")


def _line_is_toc(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if _TOC_DOTS.search(stripped):
        return True
    if _TOC_HEADERS.search(stripped):
        return True
    if _TOC_PAGE_REFS.search(stripped):
        return True
    if _FOOTER.search(stripped):
        return True
    # Short lines with multiple section references but no real sentence structure
    if len(stripped) < 80 and _TOC_SECTION_REFS.search(stripped):
        # Check it doesn't look like real clause text (real text has commas, periods, longer structure)
        if "，" not in stripped and "。" not in stripped and len(stripped) < 60:
            return True
    return False


def _is_likely_toc_page(text: str) -> float:
    """Return 0.0-1.0 score: 1.0 = definitely TOC, 0.0 = definitely real content."""
    lines = [l for l in text.split("\n") if l.strip()]
    if not lines:
        return 0.0
    toc_count = sum(1 for line in lines if _line_is_toc(line))
    ratio = toc_count / len(lines)
    if ratio >= 0.5:
        return 1.0
    if ratio >= 0.25:
        return 0.7
    if ratio >= 0.1:
        return 0.3
    return 0.0


def _quote_quality_score(quote: str) -> float:
    """Score a quote 0.0-1.0 for substantive content quality."""
    score = 0.5  # base
    # Penalize TOC-style quotes
    if _TOC_DOTS.search(quote):
        score -= 0.4
    if _TOC_PAGE_REFS.search(quote):
        score -= 0.3
    if _FOOTER.search(quote):
        score -= 0.2
    # Reward substantive content signals
    if "，" in quote or "。" in quote:
        score += 0.2  # has Chinese punctuation = real sentence
    if any(kw in quote for kw in ["应当", "有权", "不得", "我们", "您", "保险金", "合同"]):
        score += 0.1  # insurance clause vocabulary
    if len(quote) > 100:
        score += 0.1  # longer = more context
    return max(0.0, min(1.0, score))


def _is_toc_context(text: str, index: int, radius: int = 80) -> bool:
    start = max(0, index - radius)
    end = min(len(text), index + radius)
    context = text[start:end]
    if _TOC_DOTS.search(context):
        return True
    if _TOC_PAGE_REFS.search(context):
        return True
    return False


def _best_snippet(text: str, term: str, radius: int = 150) -> str:
    """Find the best (most substantive) snippet containing *term*."""
    candidates = []
    search_start = 0
    while True:
        index = text.find(term, search_start)
        if index < 0:
            break
        start = max(0, index - radius)
        end = min(len(text), index + len(term) + radius)
        snippet = text[start:end].strip()
        is_toc = _is_toc_context(text, index)
        candidates.append((snippet, is_toc, index))
        search_start = index + len(term)

    if not candidates:
        return text[: radius * 2]

    # Prefer non-TOC snippets
    non_toc = [(s, i, p) for s, i, p in candidates if not i]
    pool = non_toc if non_toc else candidates

    # Pick the one with highest quality score
    best = max(pool, key=lambda item: _quote_quality_score(item[0]))
    return best[0]


def build_evidence(records: list[dict], synonyms: dict[str, list[str]]) -> dict[str, list[dict]]:
    evidence: dict[str, list[dict]] = defaultdict(list)
    for field, terms in synonyms.items():
        for record in records:
            text = str(record.get("text", ""))
            matched = [term for term in terms if term and term in text]
            if not matched:
                continue
            quote = _best_snippet(text, matched[0])
            toc_score = _is_likely_toc_page(text)
            quality = _quote_quality_score(quote)
            evidence[field].append({
                "source_id": record.get("source_id") or record.get("source"),
                "authority_rank": int(record.get("authority_rank", 99)),
                "page": record.get("page"),
                "method": record.get("method"),
                "quote": quote,
                "matched_terms": matched,
                "toc_score": toc_score,
                "quality_score": quality,
            })
        # Sort: lowest authority rank first, then lowest TOC score, then highest quality
        evidence[field].sort(key=lambda item: (
            item["authority_rank"],
            item.get("toc_score", 0),
            -item.get("quality_score", 0),
            item.get("page") or 10**9,
        ))
    return dict(evidence)


def compact_evidence(evidence: dict[str, list[dict]], *, limit_per_field: int = 3) -> dict[str, list[dict]]:
    compact = {}
    for field, hits in evidence.items():
        seen = set()
        selected = []
        for hit in hits:
            normalized = " ".join(hit.get("quote", "").split())
            if normalized in seen:
                continue
            seen.add(normalized)
            selected.append(hit)
            if len(selected) >= limit_per_field:
                break
        compact[field] = selected
    return compact


def query_evidence(evidence: dict[str, list[dict]], field: str, *, limit: int = 20) -> dict[str, list[dict]]:
    return {field: evidence.get(field, [])[:limit]}
