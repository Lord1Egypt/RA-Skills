#!/usr/bin/env python3
"""Fetch trending agent-related repos from GitHub and output a formatted leaderboard."""

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone

PERIOD_DAYS = {"daily": 1, "weekly": 7, "monthly": 30}
PERIOD_LABELS = {"daily": "日榜", "weekly": "周榜", "monthly": "月榜"}
PERIOD_EMOJI = {"daily": "📅", "weekly": "📊", "monthly": "📈"}

# Keyword searches: agent-focused (name/description), recent pushes
SEARCH_KEYWORDS = [
    "ai-agent",
    "agent",
    "multi-agent",
    "autonomous agent",
    "llm agent",
    "coding agent",
    "agent framework",
    "agentic",
]

# Topic filters (narrower than generic "ai")
SEARCH_TOPICS = [
    "ai-agent",
    "multi-agent",
    "agents",
    "llm",
    "langchain",
    "autogen",
]

UA = "github-agent-trends/1.0 (skill; +https://github.com)"


def gh_search(query, sort="stars", order="desc", per_page=30, token=None):
    params = urllib.parse.urlencode({
        "q": query, "sort": sort, "order": order, "per_page": per_page
    })
    url = f"https://api.github.com/search/repositories?{params}"
    headers = {"Accept": "application/vnd.github+json", "User-Agent": UA}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read()).get("items", [])
    except Exception as e:
        print(f"[WARN] GitHub API error: {e}", file=sys.stderr)
        return []


def fetch_trending(period="weekly", limit=30, token=None):
    days = PERIOD_DAYS.get(period, 7)
    since = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")
    seen, results = set(), []
    base_filter = f"pushed:>={since} stars:>=10"

    for kw in SEARCH_KEYWORDS:
        if len(results) >= limit * 3:
            break
        q = f"{kw} in:name,description {base_filter}"
        items = gh_search(q, sort="stars", per_page=30, token=token)
        for item in items:
            if item["full_name"] not in seen:
                seen.add(item["full_name"])
                results.append(item)

    for topic in SEARCH_TOPICS:
        if len(results) >= limit * 4:
            break
        q = f"topic:{topic} {base_filter}"
        items = gh_search(q, sort="stars", per_page=30, token=token)
        for item in items:
            if item["full_name"] not in seen:
                seen.add(item["full_name"])
                results.append(item)

    results.sort(key=lambda r: r.get("stargazers_count", 0), reverse=True)
    return results[:limit]


def fmt_num(n):
    return f"{n/1000:.1f}k" if n >= 1000 else str(n)


def format_output(repos, period):
    label = PERIOD_LABELS.get(period, period)
    emoji = PERIOD_EMOJI.get(period, "📊")
    now = datetime.now(timezone(timedelta(hours=8))).strftime("%Y-%m-%d %H:%M")

    lines = [f"{emoji} **GitHub Agent 趋势榜 — {label}**", f"生成时间：{now}", ""]

    for i, r in enumerate(repos, 1):
        stars = fmt_num(r["stargazers_count"])
        forks = fmt_num(r.get("forks_count", 0))
        lang = r.get("language") or "N/A"
        desc = r.get("description") or ""
        if len(desc) > 80:
            desc = desc[:77] + "..."
        name = r["full_name"]
        url = r["html_url"]

        lines.append(f"**#{i}** [{name}]({url})")
        lines.append(f"⭐ {stars} · 🍴 {forks} · {lang}")
        if desc:
            lines.append(f"_{desc}_")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="GitHub Agent Trends — leaderboard of agent-related repositories (search API)"
    )
    parser.add_argument("--period", choices=["daily", "weekly", "monthly"],
                        default="weekly")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--token", default=os.environ.get("GITHUB_TOKEN"))
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    print(f"Fetching {args.period} agent trends (GitHub search)...", file=sys.stderr)
    repos = fetch_trending(args.period, args.limit, args.token)

    if not repos:
        print(
            "No repos found. Try another --period, raise --limit, or set GITHUB_TOKEN.",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.json:
        json.dump([{
            "rank": i, "name": r["full_name"], "url": r["html_url"],
            "stars": r["stargazers_count"], "forks": r.get("forks_count", 0),
            "language": r.get("language"), "description": r.get("description"),
        } for i, r in enumerate(repos, 1)], sys.stdout, ensure_ascii=False, indent=2)
    else:
        print(format_output(repos, args.period))


if __name__ == "__main__":
    main()
