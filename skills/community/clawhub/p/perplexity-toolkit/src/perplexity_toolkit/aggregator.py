"""Result aggregation — dedup sources, rank by frequency, generate reports."""

import json
import logging
from collections import Counter
from typing import List
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


def aggregate(results: List[dict]) -> dict:
    """Aggregate multiple search results into a consolidated report."""
    sources = _dedup_sources(results)
    key_facts = _extract_key_facts(results)
    follow_ups = list(dict.fromkeys(
        f for r in results for f in r.get("follow_ups", [])
    ))

    modes = Counter(r.get("mode", "search") for r in results)
    errors = [r for r in results if r.get("error")]

    logger.info("Aggregated: %d searches, %d errors, %d unique sources",
                len(results), len(errors), len(sources))
    return {
        "total_searches": len(results),
        "successful": len(results) - len(errors),
        "errors": len(errors),
        "modes_used": dict(modes),
        "unique_sources": len(sources),
        "top_sources": sources[:20],
        "key_facts": key_facts[:10],
        "follow_up_questions": follow_ups[:10],
        "queries": [
            {"query": r.get("query", ""), "mode": r.get("mode", "search"),
             "url": r.get("url", ""), "answer_len": len(r.get("answer", "")),
             "sources_count": len(r.get("sources", []))}
            for r in results
        ],
    }


def _dedup_sources(results: List[dict]) -> List[dict]:
    counts = Counter()
    info = {}
    for r in results:
        for src in r.get("sources", []):
            href = src.get("href", "")
            if not href:
                continue
            parsed = urlparse(href)
            norm = f"{parsed.scheme}://{parsed.netloc}{parsed.path}".rstrip("/")
            counts[norm] += 1
            if norm not in info:
                info[norm] = {"url": href, "text": src.get("text", "")[:150],
                              "domain": parsed.netloc, "cited_count": 0}
    for url, c in counts.items():
        info[url]["cited_count"] = c
    return sorted(info.values(), key=lambda x: x["cited_count"], reverse=True)


def _extract_key_facts(results: List[dict]) -> List[str]:
    skip = ("答案", "链接", "图片", "分享", "已完成", "进行中", "搜索结果", "新闻", "视频")
    facts = []
    for r in results:
        answer = r.get("answer", "")
        if not answer:
            continue
        for line in answer.split("\n"):
            line = line.strip()
            if not line or any(line.startswith(p) for p in skip):
                continue
            if line.startswith(r.get("query", "")):
                continue
            if len(line) > 40 and not line.startswith(("http", "www.")):
                facts.append(line[:300])
                break
    return facts


def to_markdown(report: dict) -> str:
    """Convert aggregated report to markdown."""
    lines = [
        "# Perplexity Search Report",
        f"\n**Total searches:** {report['total_searches']}",
        f"**Successful:** {report['successful']}",
        f"**Errors:** {report['errors']}",
        f"**Unique sources:** {report['unique_sources']}",
        f"\n**Modes used:** {', '.join(f'{k}({v})' for k, v in report['modes_used'].items())}",
        "\n---",
        "\n## Top Sources (by citation frequency)",
    ]
    for i, src in enumerate(report["top_sources"][:15], 1):
        lines.append(f"{i}. **[{src['domain']}]({src['url']})** "
                     f"({src['cited_count']}x cited) — {src['text'][:80]}")

    lines.append("\n## Key Findings")
    for i, fact in enumerate(report["key_facts"], 1):
        lines.append(f"{i}. {fact}")

    lines.append("\n## Suggested Follow-ups")
    for q in report["follow_up_questions"]:
        lines.append(f"- {q}")

    lines.append("\n## Query Details")
    lines.append("| Query | Mode | Sources | Answer Len |")
    lines.append("|-------|------|---------|------------|")
    for q in report["queries"]:
        lines.append(f"| {q['query'][:50]} | {q['mode']} | {q['sources_count']} | {q['answer_len']} |")

    return "\n".join(lines)
