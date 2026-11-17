"""Result quality verification — auto-detect and handle Perplexity's known issues.

Based on community-reported problems (297+ Reddit posts):
- 37% of cited URLs are broken/wrong
- Answers may contain fabricated claims
- Self-correction only triggers when challenged
"""

import logging
import re
import urllib.request
from typing import Any, List, Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

# Patterns that indicate potential fabrication
_WEAK_INDICATORS = [
    "i could not find",
    "i'm not sure",
    "i don't have",
    "note:",
    "disclaimer:",
    "as an ai",
    "i apologize",
    "may not be accurate",
    "please verify",
    "无法找到",
    "我不确定",
    "请注意",
    "可能不准确",
]


_READBACK_MAX_BYTES = 256 * 1024
_TEXT_CONTENT_TYPES = (
    "text/", "application/json", "application/xml", "application/xhtml+xml",
)


def _status_ok(status: int) -> bool:
    try:
        return 200 <= int(status) < 400
    except (TypeError, ValueError):
        return False


def _content_type(headers) -> str:
    """Read a response content type without assuming a concrete headers type."""
    try:
        value = headers.get_content_type()
        if value:
            return str(value).lower()
    except (AttributeError, TypeError):
        pass
    try:
        value = headers.get("Content-Type", "")
    except AttributeError:
        value = ""
    return str(value).split(";", 1)[0].strip().lower()


def _readback_source(src: Dict, timeout: float) -> Dict:
    """Fetch bounded page content for a source without retaining the body."""
    url = src.get("href", "")
    base = {"text": src.get("text", "")[:80], "href": url,
            "claim_support": "not_evaluated"}
    if not url or not url.startswith("http"):
        return {**base, "status": 0, "state": "invalid"}

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "perplexity-toolkit-source-check/1.0"},
            method="GET",
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = getattr(resp, "status", 0)
            content_type = _content_type(getattr(resp, "headers", {}))
            raw = resp.read(_READBACK_MAX_BYTES)
            if isinstance(raw, str):
                chars = len(raw)
            else:
                charset = "utf-8"
                try:
                    charset = resp.headers.get_content_charset() or charset
                except (AttributeError, TypeError):
                    pass
                text = raw.decode(charset, errors="replace")
                chars = len(text)

            if not _status_ok(status):
                state = "blocked"
            elif content_type and not content_type.startswith(_TEXT_CONTENT_TYPES):
                state = "non_text"
            elif chars == 0:
                state = "empty"
            else:
                state = "readable"
            return {**base, "status": status, "state": state,
                    "content_type": content_type, "characters": chars}
    except Exception as exc:
        return {**base, "status": getattr(exc, "code", 0),
                "state": "error", "error_type": type(exc).__name__}


def verify_sources(
    sources: List[Dict], timeout: float = 5.0, max_workers: int = 5,
    readback: bool = False,
) -> Dict:
    """Check source reachability and optionally read back bounded page content.

    ``valid``/``broken`` describe the HTTP HEAD check only. When ``readback``
    is true, ``page_content`` reports whether a text response was actually
    readable. Neither check proves that a page supports a particular claim;
    each entry therefore carries ``claim_support: not_evaluated``.
    """
    empty = {"total": 0, "valid": 0, "broken": 0, "broken_urls": []}
    if not sources:
        if readback:
            empty.update({
                "page_content": [],
                "readback": {
                    "attempted": 0, "readable": 0, "unreadable": 0,
                    "claim_support": "not_evaluated",
                },
            })
        return empty

    def check_url(src):
        url = src.get("href", "")
        if not url or not url.startswith("http"):
            return src, 0
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "perplexity-toolkit-source-check/1.0"},
                method="HEAD",
            )
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return src, getattr(resp, "status", 0)
        except Exception as exc:
            return src, getattr(exc, "code", 0)

    broken = []
    valid = 0
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        futures = {pool.submit(check_url, s): s for s in sources}
        for f in as_completed(futures):
            src, status = f.result()
            if _status_ok(status):
                valid += 1
            else:
                broken.append({
                    "text": src.get("text", "")[:80],
                    "href": src.get("href", ""),
                    "status": status,
                })

    result = {
        "total": len(sources),
        "valid": valid,
        "broken": len(broken),
        "broken_urls": sorted(broken, key=lambda item: item["href"]),
    }

    if readback:
        page_content = []
        with ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = {pool.submit(_readback_source, s, timeout): s for s in sources}
            for f in as_completed(futures):
                page_content.append(f.result())
        page_content.sort(key=lambda item: item["href"])
        readable = sum(item["state"] == "readable" for item in page_content)
        result["page_content"] = page_content
        result["readback"] = {
            "attempted": len(page_content),
            "readable": readable,
            "unreadable": len(page_content) - readable,
            "claim_support": "not_evaluated",
        }

    if broken:
        logger.warning("Broken sources: %d/%d URLs unreachable by HEAD", len(broken), len(sources))
        for b in result["broken_urls"]:
            logger.warning("  ✗ %s [%d] %s", b["text"][:50], b["status"], b["href"])
    else:
        logger.info("All %d sources responded to HEAD", valid)
    return result


def check_answer_quality(answer: str, sources: List[Dict]) -> Dict:
    """Analyze answer quality and flag potential issues.

    Returns:
        {score: 0-100, issues: [str], needs_verification: bool}
    """
    issues = []
    score = 100

    # Empty or very short
    if not answer:
        return {"score": 0, "issues": ["Empty answer"], "needs_verification": True}
    if len(answer) < 100:
        issues.append("Very short answer (< 100 chars)")
        score -= 30

    # No sources
    if not sources:
        issues.append("No sources cited")
        score -= 25

    # Weak/hedging language
    answer_lower = answer.lower()
    weak_count = sum(1 for p in _WEAK_INDICATORS if p in answer_lower)
    if weak_count >= 3:
        issues.append(f"Multiple hedging phrases ({weak_count})")
        score -= 20

    # Suspiciously specific claims without numbers
    # (fabricated answers often have very specific but wrong details)
    if re.search(r'\d{4}', answer) and not re.search(r'\[\d+\]', answer):
        issues.append("Year references without citation markers")
        score -= 10

    # Answer is mostly questions (not actually answering)
    question_count = answer.count('?') + answer.count('？')
    if question_count > 3 and len(answer) < 500:
        issues.append("Answer contains many questions — may not be answering directly")
        score -= 15

    score = max(0, score)
    needs_verification = score < 70

    if issues:
        logger.warning("Answer quality issues (score=%d): %s", score, "; ".join(issues))
    else:
        logger.info("Answer quality: %d/100 — clean", score)

    return {"score": score, "issues": issues, "needs_verification": needs_verification}


def generate_verification_prompt(answer: str, query: str) -> str:
    """Generate a follow-up prompt to trigger Perplexity's self-correction.

    Community finding: Perplexity only self-corrects when explicitly challenged.
    """
    return (
        f"请验证你上面关于「{query[:50]}」的回答。"
        f"特别检查：1) 所有引用链接是否真实可访问且内容相关；"
        f"2) 数据和日期是否准确；3) 是否有编造或推测的内容。"
        f"如果有错误，请给出正确答案。"
    )


def generate_cross_check_queries(query: str, answer: str) -> List[str]:
    """Generate alternative queries to cross-validate the answer.

    Returns 2 queries phrased differently to catch inconsistencies.
    """
    # Extract key claims from answer (sentences with numbers or specific names)
    claims = re.findall(r'[A-Z][^.]*?\d+[^.]*\.', answer)
    if not claims:
        claims = [answer[:100]]

    queries = []
    # Rephrase from different angle
    queries.append(f"{query} — 验证准确性，请引用可靠来源")
    # Ask for counter-evidence
    queries.append(f"{query} 常见误解和错误是什么？")

    return queries[:2]


def verify_result(result: dict, verify_urls: bool = True) -> dict:
    """Run all quality checks on a search result and annotate it.

    Adds a 'quality' field to the result dict with verification results.
    """
    answer = result.get("answer", "")
    sources = result.get("sources", [])

    quality: Dict[str, Any] = {
        "answer_check": check_answer_quality(answer, sources),
    }

    if verify_urls and sources:
        # A HEAD response only proves that a URL answered. Read back bounded
        # page content as a separate diagnostic and keep claim support
        # explicitly unevaluated until a semantic evidence pass is performed.
        quality["source_check"] = verify_sources(sources, readback=True)
        quality["verification_state"] = "candidate"
        quality["claim_support"] = "not_evaluated"
    else:
        quality["source_check"] = {"total": 0, "valid": 0, "broken": 0, "broken_urls": []}
        quality["verification_state"] = "unverified"
        quality["claim_support"] = "not_evaluated"

    # Overall quality verdict
    answer_score = quality["answer_check"]["score"]
    broken_ratio = 0
    if quality["source_check"]["total"] > 0:
        readback = quality["source_check"].get("readback", {})
        if readback:
            broken_ratio = readback["unreadable"] / readback["attempted"]
        else:
            broken_ratio = quality["source_check"]["broken"] / quality["source_check"]["total"]

    if answer_score < 50 or broken_ratio > 0.5:
        quality["verdict"] = "poor"
        quality["suggestion"] = "Answer likely unreliable. Consider re-searching or cross-checking."
    elif answer_score < 70 or broken_ratio > 0.3:
        quality["verdict"] = "questionable"
        quality["suggestion"] = "Some issues detected. Verify key claims before using."
    else:
        quality["verdict"] = "good"
        quality["suggestion"] = (
            "Answer appears reliable at a heuristic level; canonical claim "
            "support still requires semantic review."
        )

    logger.info("Quality verdict: %s (answer=%d, broken_sources=%d/%d)",
                quality["verdict"], answer_score,
                quality["source_check"]["broken"], quality["source_check"]["total"])

    result["quality"] = quality
    return result
