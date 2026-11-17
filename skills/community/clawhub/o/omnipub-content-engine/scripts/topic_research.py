# -*- coding: utf-8 -*-
"""
Topic Research Module
=====================
Searches for hot topics with viral potential and scores them.

Usage:
    python topic_research.py "AI医疗" --platforms all
    python topic_research.py "AI医疗" --redfox-key xxx --verbose
"""
import argparse
import json
import sys
import os
import urllib.request
import urllib.parse
from datetime import datetime


def search_websearch(query: str, limit: int = 10) -> list:
    """Fallback: format query for WebSearch tool (AI agent will execute)."""
    return [{
        "source": "websearch",
        "query": query,
        "instruction": f"Use WebSearch to search: '{query} 热门 讨论 2025' and return top {limit} results with titles, URLs, and brief summaries."
    }]


def search_redfox(query: str, api_key: str, days: int = 7, limit: int = 20) -> list:
    """Search Red Fox API for trending articles."""
    url = "https://redfox.hk/story/api/gzh/search/hotArticleNew"
    data = urllib.parse.urlencode({
        "keyword": query,
        "days": days,
        "limit": limit,
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/x-www-form-urlencoded",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result.get("data", {}).get("list", [])
    except Exception as e:
        print(f"Red Fox API error: {e}", file=sys.stderr)
        return []


def score_topic(topic: dict) -> dict:
    """Score a topic using HCTFD framework.
    H=Heat(30), C=Competition(20), T=Trend(20), F=Fit(15), D=Depth(15)
    """
    h = min(30, topic.get("heat_score", 15))
    c = 20 - min(20, topic.get("competition_count", 10))
    t = min(20, topic.get("trend_momentum", 10))
    f = min(15, topic.get("persona_match", 8))
    d = min(15, topic.get("content_depth", 8))
    total = h + c + t + f + d
    return {
        "topic": topic.get("title", ""),
        "url": topic.get("url", ""),
        "scores": {"heat": h, "competition": c, "trend": t, "fit": f, "depth": d},
        "total": total,
        "recommendation": "high" if total >= 70 else "medium" if total >= 50 else "low",
    }


def format_report(query: str, results: list, scores: list) -> str:
    """Format topic research report as Markdown."""
    lines = [
        f"# Topic Research Report",
        f"",
        f"**Query:** {query}",
        f"**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        f"**Results:** {len(results)} topics found",
        f"",
        f"## HCTFD Scoring",
        f"",
        f"| # | Topic | Heat | Comp | Trend | Fit | Depth | Total | Rating |",
        f"|---|-------|------|------|-------|-----|-------|-------|--------|",
    ]
    for i, s in enumerate(sorted(scores, key=lambda x: x["total"], reverse=True), 1):
        sc = s["scores"]
        lines.append(
            f"| {i} | {s['topic'][:40]} | {sc['heat']} | {sc['competition']} | {sc['trend']} | {sc['fit']} | {sc['depth']} | {s['total']} | {s['recommendation']} |"
        )
    lines.append("")
    lines.append("## Next Steps")
    lines.append("")
    lines.append("1. Review high-rated topics above")
    lines.append("2. Select one topic and confirm direction")
    lines.append("3. AI will generate article outline for approval (Gate G1)")
    return "\n".join(lines)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search and score hot topics")
    parser.add_argument("query", help="Search keyword or topic")
    parser.add_argument("--platforms", default="all", help="Platform filter (all/wechat/toutiao)")
    parser.add_argument("--redfox-key", default=os.environ.get("REDFOX_API_KEY", ""), help="Red Fox API key (optional)")
    parser.add_argument("--days", type=int, default=7, help="Search period in days")
    parser.add_argument("--limit", type=int, default=20, help="Max results")
    parser.add_argument("--output", "-o", help="Output file path (default: stdout)")
    parser.add_argument("--verbose", "-v", action="store_true")
    args = parser.parse_args()

    results = []
    if args.redfox_key:
        results = search_redfox(args.query, args.redfox_key, args.days, args.limit)
        if args.verbose:
            print(f"Red Fox: {len(results)} results", file=sys.stderr)
    else:
        results = search_websearch(args.query, args.limit)
        if args.verbose:
            print("Using WebSearch fallback (no Red Fox key)", file=sys.stderr)

    scores = [score_topic(r) for r in results] if results else []
    report = format_report(args.query, results, scores)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"Report saved: {args.output}")
    else:
        print(report)
