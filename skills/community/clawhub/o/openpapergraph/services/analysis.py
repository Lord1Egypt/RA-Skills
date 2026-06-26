"""Topic analysis and AI summary — pure functions, no framework dependency."""
import re
import os
import sys
from collections import Counter
from typing import List

from schemas import Paper

STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with",
    "by", "from", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
    "do", "does", "did", "will", "would", "could", "should", "may", "might", "can",
    "this", "that", "these", "those", "it", "its", "we", "our", "they", "their", "them",
    "not", "no", "as", "if", "than", "more", "most", "also", "such", "which", "each",
    "both", "between", "through", "over", "under", "about", "into", "during", "before",
    "after", "above", "below", "all", "any", "some", "other", "new", "using", "based",
    "show", "shows", "shown", "proposed", "propose", "paper", "method", "methods",
    "approach", "results", "result", "model", "models", "data", "use", "used",
}


def extract_keywords(texts: List[str], top_n: int = 50) -> list:
    counts = Counter()
    for text in texts:
        if not text:
            continue
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())
        counts.update(w for w in words if w not in STOP_WORDS)
    return [{"word": w, "count": c} for w, c in counts.most_common(top_n)]


def detect_topics(papers: List[Paper], num_topics: int = 5) -> list:
    abstracts = [p.abstract for p in papers if p.abstract]
    if not abstracts:
        return []
    all_kw = extract_keywords(abstracts, top_n=100)
    if not all_kw:
        return []
    seeds = [kw["word"] for kw in all_kw[:num_topics * 3:3]][:num_topics]
    topics = []
    for i, seed in enumerate(seeds):
        matching = [p for p in papers if p.abstract and seed in p.abstract.lower()]
        if not matching:
            continue
        group_kw = extract_keywords([p.abstract for p in matching if p.abstract], top_n=8)
        topics.append({"id": i, "label": seed.capitalize(), "words": group_kw, "paper_count": len(matching)})
    return topics


def analyze(papers: List[Paper]) -> dict:
    topics = detect_topics(papers)
    year_counts = Counter(p.year for p in papers if p.year)
    year_dist = [{"year": y, "count": c} for y, c in sorted(year_counts.items())]
    author_counts = Counter()
    for p in papers:
        for a in p.authors:
            if a:
                author_counts[a] += 1
    top_authors = [{"name": n, "paper_count": c} for n, c in author_counts.most_common(15)]
    keyword_cloud = extract_keywords([p.abstract for p in papers if p.abstract], top_n=40)
    return {"topics": topics, "year_distribution": year_dist, "top_authors": top_authors, "keyword_cloud": keyword_cloud}


def _extractive_summary(papers: List[Paper], style: str = "overview") -> dict:
    """Extractive (keyword/statistical) summary — no LLM required."""
    top = sorted(papers, key=lambda p: p.citation_count, reverse=True)
    years = [p.year for p in papers if p.year]
    year_counts = Counter(years)
    total = len(papers)
    avg_cite = sum(p.citation_count for p in papers) // max(total, 1)
    year_range = f"{min(years)}-{max(years)}" if years else "unknown"

    stop = {"the", "a", "an", "and", "or", "for", "of", "in", "on", "to", "with", "by", "from", "is", "are", "using", "based", "via"}
    word_counts = Counter()
    for p in papers:
        word_counts.update(w for w in p.title.lower().split() if len(w) > 3 and w not in stop)
    top_kw = [w for w, _ in word_counts.most_common(10)]

    parts = [f"This collection contains {total} papers spanning {year_range}, with an average of {avg_cite} citations per paper."]
    if top[:3]:
        parts.append("Most influential: " + "; ".join(f'"{p.title}" ({p.citation_count} cites)' for p in top[:3]) + ".")
    if top_kw:
        parts.append(f"Key themes: {', '.join(top_kw[:7])}.")

    findings = []
    for p in top[:5]:
        if p.abstract:
            sentences = p.abstract.split(". ")
            if sentences and len(sentences[-1]) > 20:
                findings.append(f"[{p.year}] {sentences[-1].strip()}")

    trends = []
    if top_kw[:3]:
        trends.append(f"Dominant topics: {', '.join(top_kw[:3])}")
    sorted_years = sorted(year_counts.items())
    if len(sorted_years) >= 3:
        early = sum(c for _, c in sorted_years[:len(sorted_years)//2])
        late = sum(c for _, c in sorted_years[len(sorted_years)//2:])
        if late > early * 1.5:
            trends.append("Publication rate accelerating")

    directions = []
    if len(top_kw) >= 2:
        directions.append(f"Explore intersections between {top_kw[0]} and {top_kw[-1]}")
    directions.append("Check recent preprints extending top-cited works")

    return {"summary": " ".join(parts), "key_findings": findings[:5], "research_trends": trends,
            "suggested_directions": directions, "method": "extractive"}


def _build_llm_prompt(papers: List[Paper], style: str) -> str:
    """Build a prompt for LLM-powered summarization."""
    top = sorted(papers, key=lambda p: p.citation_count, reverse=True)[:20]
    total = len(papers)
    years = [p.year for p in papers if p.year]
    year_range = f"{min(years)}-{max(years)}" if years else "unknown"

    paper_list = []
    for i, p in enumerate(top, 1):
        entry = f"{i}. \"{p.title}\" ({p.year}, {p.citation_count} citations)"
        if p.authors:
            entry += f" — {', '.join(p.authors[:3])}"
        if p.abstract:
            entry += f"\n   Abstract: {p.abstract[:300]}..."
        paper_list.append(entry)

    style_instructions = {
        "overview": "Provide a comprehensive overview of the research area: main themes, key contributions, and how the papers relate to each other.",
        "trends": "Focus on research trends: what topics are gaining momentum, how the field has evolved over time, and where it is heading.",
        "gaps": "Identify research gaps: what questions remain unanswered, what areas are underexplored, and what promising directions lack sufficient work.",
    }

    return f"""Analyze this collection of {total} academic papers spanning {year_range}.

{style_instructions.get(style, style_instructions['overview'])}

Top papers (by citations):
{chr(10).join(paper_list)}

Respond in JSON format with exactly these keys:
- "summary": A 3-5 sentence overview paragraph
- "key_findings": Array of 3-5 key findings (one sentence each)
- "research_trends": Array of 3-5 research trends
- "suggested_directions": Array of 3-5 suggested future directions
"""


def _llm_summary(papers: List[Paper], style: str = "overview") -> dict:
    """LLM-powered summary — uses any configured provider via llm_client."""
    import json as _json
    from services.llm_client import llm_chat, get_provider_info

    prompt = _build_llm_prompt(papers, style)
    raw = llm_chat(prompt, temperature=0.3, max_tokens=2000)
    if not raw:
        return None

    # Parse JSON from LLM response (handle markdown code blocks)
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r'^```(?:json)?\s*', '', text)
        text = re.sub(r'\s*```$', '', text)

    try:
        result = _json.loads(text)
        provider_info = get_provider_info() or {}
        result["method"] = "llm"
        result["provider"] = provider_info.get("display_name", "unknown")
        result["model"] = provider_info.get("model", "unknown")
        return result
    except _json.JSONDecodeError:
        # LLM returned non-JSON — wrap raw text as summary
        provider_info = get_provider_info() or {}
        return {
            "summary": text,
            "key_findings": [],
            "research_trends": [],
            "suggested_directions": [],
            "method": "llm",
            "provider": provider_info.get("display_name", "unknown"),
            "model": provider_info.get("model", "unknown"),
        }


def summarize(papers: List[Paper], style: str = "overview") -> dict:
    """Generate a research summary — LLM-powered if a provider is configured, extractive otherwise."""
    if not papers:
        return {"summary": "No papers.", "key_findings": [], "research_trends": [], "suggested_directions": [], "method": "extractive"}

    # Try LLM first
    from services.llm_client import is_llm_available
    if is_llm_available():
        result = _llm_summary(papers, style)
        if result:
            return result
        print("[summary] LLM call failed, falling back to extractive analysis", file=sys.stderr)

    return _extractive_summary(papers, style)
