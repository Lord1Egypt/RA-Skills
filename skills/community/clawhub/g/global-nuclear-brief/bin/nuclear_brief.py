#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, List

APIFY_API_URL = "https://api.apify.com/v2/acts/{actor_id}/run-sync-get-dataset-items"
CONTEXTUAL_API_URL = "https://api.contextual.ai/v1/generate"
DEFAULT_ACTOR = "practicaltools/apify-google-news-scraper"
DEFAULT_QUERY = "nuclear energy policy OR nuclear power regulation"


def eprint(msg: str) -> None:
    sys.stderr.write(msg + "\n")


def http_post_json(url: str, payload: Dict[str, Any], headers: Dict[str, str], timeout: int) -> Any:
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as err:
        body = err.read().decode("utf-8") if err.fp else ""
        raise RuntimeError(f"HTTP {err.code} error from {url}: {body}") from err
    except urllib.error.URLError as err:
        raise RuntimeError(f"Network error calling {url}: {err}") from err
    except json.JSONDecodeError as err:
        raise RuntimeError(f"Failed to parse JSON response from {url}") from err


def fetch_news(
    token: str,
    actor_id: str,
    query: str,
    language: str,
    country: str,
    timeframe: str,
    max_articles: int,
    timeout: int,
) -> List[Dict[str, Any]]:
    url = APIFY_API_URL.format(actor_id=actor_id)
    payload = {
        "searchTerm": query,
        "language": language,
        "country": country,
        "timeframe": timeframe,
        "maxArticles": max_articles,
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    data = http_post_json(url, payload, headers, timeout)
    if isinstance(data, dict) and "items" in data:
        return data["items"]
    if isinstance(data, list):
        return data
    raise RuntimeError("Unexpected Apify response format")


def normalize_article(item: Dict[str, Any]) -> Dict[str, str]:
    title = item.get("title") or item.get("headline") or ""
    link = item.get("link") or item.get("articleUrl") or item.get("url") or ""
    source = item.get("source") or item.get("publisher") or ""
    date = item.get("datetime") or item.get("publishedDate") or item.get("publishedAt") or item.get("date") or item.get("time") or ""
    snippet = item.get("snippet") or item.get("description") or item.get("summary") or ""
    return {
        "title": title.strip(),
        "link": link.strip(),
        "source": str(source).strip(),
        "date": str(date).strip(),
        "snippet": str(snippet).strip(),
    }


def build_knowledge(items: List[Dict[str, Any]], limit: int) -> List[str]:
    knowledge: List[str] = []
    count = 0
    for raw in items:
        if count >= limit:
            break
        article = normalize_article(raw)
        if not article["title"] or not article["link"]:
            continue
        parts = [
            f"Title: {article['title']}",
            f"Source: {article['source'] or 'Unknown'}",
            f"Date: {article['date'] or 'Unknown'}",
            f"Link: {article['link']}",
        ]
        if article["snippet"]:
            parts.append(f"Snippet: {article['snippet']}")
        knowledge.append("\n".join(parts))
        count += 1
    return knowledge


def generate_brief(
    token: str,
    model: str,
    topic: str,
    audience: str,
    knowledge: List[str],
    max_tokens: int,
    timeout: int,
) -> str:
    system_prompt = (
        "You are a policy analyst assistant. Use ONLY the provided knowledge. "
        "If evidence is missing, say so. Do not invent facts."
    )
    user_prompt = (
        f"Create a concise nuclear energy policy brief for {audience}.\n"
        f"Topic focus: {topic}.\n\n"
        "Format:\n"
        "1. Top changes (3-5 bullets)\n"
        "2. Why it matters (3 bullets)\n"
        "3. Risks and uncertainties (2-3 bullets)\n"
        "4. Recommended actions (3 bullets)\n"
        "5. Sources (list of titles + links)\n"
    )
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": user_prompt}],
        "knowledge": knowledge,
        "system_prompt": system_prompt,
        "avoid_commentary": True,
        "temperature": 0.2,
        "top_p": 0.9,
        "max_new_tokens": max_tokens,
    }
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }
    data = http_post_json(CONTEXTUAL_API_URL, payload, headers, timeout)
    if isinstance(data, dict) and "response" in data:
        return str(data["response"]).strip()
    raise RuntimeError("Unexpected Contextual response format")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a nuclear policy brief using Apify + Contextual")
    parser.add_argument("--query", default=DEFAULT_QUERY, help="Search query for news")
    parser.add_argument("--topic", default="Global nuclear energy policy", help="Brief topic focus")
    parser.add_argument("--audience", default="energy policy analysts", help="Target audience")
    parser.add_argument("--language", default="en", help="Language code for news")
    parser.add_argument("--country", default="US", help="Country code for news")
    parser.add_argument("--timeframe", default="7d", help="Timeframe filter (e.g., 1d, 7d, 1m)")
    parser.add_argument("--max-articles", type=int, default=12, help="Max news items to fetch")
    parser.add_argument("--knowledge-limit", type=int, default=10, help="Max items passed to Contextual")
    parser.add_argument("--actor", default=DEFAULT_ACTOR, help="Apify actor ID")
    parser.add_argument("--contextual-model", default=os.getenv("CONTEXTUAL_MODEL", "v2"), help="Contextual model version")
    parser.add_argument("--max-tokens", type=int, default=900, help="Max tokens in output")
    parser.add_argument("--timeout", type=int, default=120, help="HTTP timeout in seconds")
    args = parser.parse_args()

    apify_token = os.getenv("APIFY_API_TOKEN")
    contextual_token = os.getenv("CONTEXTUAL_API_KEY")

    if not apify_token:
        eprint("Missing APIFY_API_TOKEN in environment.")
        return 2
    if not contextual_token:
        eprint("Missing CONTEXTUAL_API_KEY in environment.")
        return 2

    try:
        items = fetch_news(
            apify_token,
            args.actor,
            args.query,
            args.language,
            args.country,
            args.timeframe,
            args.max_articles,
            args.timeout,
        )
        knowledge = build_knowledge(items, args.knowledge_limit)
        if not knowledge:
            eprint("No usable news items found. Try a different query or timeframe.")
            return 3
        brief = generate_brief(
            contextual_token,
            args.contextual_model,
            args.topic,
            args.audience,
            knowledge,
            args.max_tokens,
            args.timeout,
        )
        print(brief)
        return 0
    except Exception as exc:
        eprint(str(exc))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
