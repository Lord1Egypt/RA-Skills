#!/usr/bin/env python3
import argparse
import json
import re
import sys
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple

import requests
from bs4 import BeautifulSoup

DEFAULT_TIMEOUT = 20
DEFAULT_UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)


@dataclass
class FetchResult:
    url: str
    final_url: str
    status_code: int
    title: Optional[str]
    description: Optional[str]
    author: Optional[str]
    published_time: Optional[str]
    method: str
    text: str
    excerpt: Optional[str]
    notes: List[str]


def clean_text(value: str) -> str:
    value = re.sub(r"\s+", " ", value or "").strip()
    return value


def get_html(url: str, timeout: int) -> Tuple[str, requests.Response, List[str]]:
    notes = []
    headers = {"User-Agent": DEFAULT_UA, "Accept-Language": "en-US,en;q=0.9"}
    try:
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        return response.text, response, notes
    except requests.RequestException as exc:
        notes.append(f"requests failed: {exc}")
        raise


def extract_meta(soup: BeautifulSoup) -> Dict[str, Optional[str]]:
    def by_meta(*names: str) -> Optional[str]:
        for name in names:
            tag = soup.find("meta", attrs={"property": name}) or soup.find("meta", attrs={"name": name})
            if tag and tag.get("content"):
                return clean_text(tag["content"])
        return None

    title = None
    if soup.title and soup.title.string:
        title = clean_text(soup.title.string)
    og_title = by_meta("og:title", "twitter:title")
    if og_title:
        title = og_title

    return {
        "title": title,
        "description": by_meta("description", "og:description", "twitter:description"),
        "author": by_meta("author", "article:author"),
        "published_time": by_meta("article:published_time", "pubdate", "datePublished"),
    }


def parse_json_ld(soup: BeautifulSoup) -> Dict[str, Optional[str]]:
    out: Dict[str, Optional[str]] = {
        "title": None,
        "description": None,
        "author": None,
        "published_time": None,
        "article_body": None,
    }
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = script.string or script.get_text(" ", strip=True)
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except Exception:
            continue
        items = data if isinstance(data, list) else [data]
        for item in items:
            if not isinstance(item, dict):
                continue
            out["title"] = out["title"] or item.get("headline") or item.get("name")
            out["description"] = out["description"] or item.get("description")
            author = item.get("author")
            if isinstance(author, dict):
                author = author.get("name")
            elif isinstance(author, list):
                names = []
                for a in author:
                    if isinstance(a, dict) and a.get("name"):
                        names.append(a["name"])
                    elif isinstance(a, str):
                        names.append(a)
                author = ", ".join(names) if names else None
            out["author"] = out["author"] or author
            out["published_time"] = out["published_time"] or item.get("datePublished")
            out["article_body"] = out["article_body"] or item.get("articleBody")
    return out


NEXT_DATA_RE = re.compile(r'<script[^>]*id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.S)
WINDOW_DATA_PATTERNS = [
    re.compile(r"window\.__INITIAL_DATA__\s*=\s*(\{.*?\})\s*;", re.S),
    re.compile(r"window\.__PRELOADED_STATE__\s*=\s*(\{.*?\})\s*;", re.S),
]


TEXT_KEYS = {
    "articleBody", "body", "content", "text", "description", "summary", "headline", "title", "name"
}


def harvest_text(value, results: List[str]) -> None:
    if isinstance(value, str):
        raw = value.strip()
        if raw.startswith("{") or raw.startswith("["):
            try:
                decoded = json.loads(raw)
                harvest_text(decoded, results)
                return
            except Exception:
                pass
        text = clean_text(value)
        if len(text) >= 80 and any(ch.isalpha() for ch in text):
            results.append(text)
    elif isinstance(value, list):
        for item in value:
            harvest_text(item, results)
    elif isinstance(value, dict):
        for key, item in value.items():
            if key in TEXT_KEYS:
                harvest_text(item, results)
            else:
                harvest_text(item, results)


def extract_embedded_text(html: str) -> Tuple[Optional[str], Optional[str]]:
    # Prefer __NEXT_DATA__
    m = NEXT_DATA_RE.search(html)
    if m:
        try:
            data = json.loads(m.group(1))
            results: List[str] = []
            harvest_text(data, results)
            best = choose_best_text(results)
            if best:
                return best, "__NEXT_DATA__"
        except Exception:
            pass

    for pattern in WINDOW_DATA_PATTERNS:
        m = pattern.search(html)
        if not m:
            continue
        try:
            data = json.loads(m.group(1))
            results = []
            harvest_text(data, results)
            best = choose_best_text(results)
            if best:
                return best, "embedded-window-data"
        except Exception:
            continue
    return None, None


def extract_dom_text(soup: BeautifulSoup) -> Tuple[str, str]:
    selectors = [
        "article p",
        "main p",
        "[role='main'] p",
        "div[data-component='text-block'] p",
        "section p",
    ]
    texts: List[str] = []
    for selector in selectors:
        nodes = soup.select(selector)
        candidate = [clean_text(node.get_text(' ', strip=True)) for node in nodes]
        candidate = [c for c in candidate if len(c) >= 40]
        joined = "\n\n".join(candidate)
        if len(joined) > len("\n\n".join(texts)):
            texts = candidate
    if not texts:
        nodes = soup.find_all("p")
        texts = [clean_text(node.get_text(' ', strip=True)) for node in nodes]
        texts = [c for c in texts if len(c) >= 40]
    return "\n\n".join(texts), "dom-paragraphs"


def choose_best_text(candidates: List[str]) -> Optional[str]:
    cleaned = []
    seen = set()
    for item in candidates:
        c = clean_text(item)
        if len(c) < 120:
            continue
        lowered = c.lower()
        if lowered.startswith("copyright ") and len(c) < 1000:
            continue
        if c in seen:
            continue
        seen.add(c)
        cleaned.append(c)
    if not cleaned:
        return None
    cleaned.sort(key=len, reverse=True)
    return cleaned[0]


def build_result(url: str, html: str, response: requests.Response) -> FetchResult:
    soup = BeautifulSoup(html, "html.parser")
    meta = extract_meta(soup)
    json_ld = parse_json_ld(soup)
    notes: List[str] = []

    text = None
    method = None

    if json_ld.get("article_body"):
        text = clean_text(json_ld["article_body"])
        method = "json-ld"
        notes.append("used articleBody from JSON-LD")

    if not text or len(text) < 400:
        embedded_text, source = extract_embedded_text(html)
        if embedded_text:
            text = embedded_text
            method = f"embedded-data:{source}"
            notes.append(f"used text from {source}")

    if not text or len(text) < 400:
        dom_text, dom_method = extract_dom_text(soup)
        if dom_text:
            text = dom_text
            method = dom_method
            notes.append("used DOM paragraph extraction")

    if not text:
        text = ""
        method = "metadata-only"
        notes.append("failed to recover meaningful body text")

    title = json_ld.get("title") or meta.get("title")
    description = json_ld.get("description") or meta.get("description")
    author = json_ld.get("author") or meta.get("author")
    published_time = json_ld.get("published_time") or meta.get("published_time")
    excerpt = clean_text(text[:280]) if text else description

    return FetchResult(
        url=url,
        final_url=str(response.url),
        status_code=response.status_code,
        title=title,
        description=description,
        author=author,
        published_time=published_time,
        method=method,
        text=text,
        excerpt=excerpt,
        notes=notes,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch and extract webpage content with lightweight fallbacks.")
    parser.add_argument("url")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--format", choices=["json", "text"], default="json")
    parser.add_argument("--max-chars", type=int, default=8000)
    args = parser.parse_args()

    try:
        html, response, notes = get_html(args.url, args.timeout)
        result = build_result(args.url, html, response)
        result.notes = notes + result.notes
    except requests.RequestException as exc:
        error = {
            "url": args.url,
            "error": str(exc),
            "method": "requests-failed",
            "next_step": "Try browser rendering or an alternate accessible source.",
        }
        if args.format == "json":
            print(json.dumps(error, ensure_ascii=False, indent=2))
        else:
            print(f"ERROR: {error['error']}")
            print(error["next_step"])
        return 1

    if args.max_chars and result.text:
        result.text = result.text[: args.max_chars]

    if args.format == "json":
        print(json.dumps(asdict(result), ensure_ascii=False, indent=2))
        return 0

    print(f"Title: {result.title or ''}")
    if result.author:
        print(f"Author: {result.author}")
    if result.published_time:
        print(f"Published: {result.published_time}")
    if result.description:
        print(f"Description: {result.description}")
    print(f"Method: {result.method}")
    print(f"Status: {result.status_code}")
    print()
    print(result.text)
    if result.notes:
        print()
        print("Notes:")
        for note in result.notes:
            print(f"- {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
