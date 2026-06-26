#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import os
import re
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any


GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta"
APIFY_API_BASE = "https://api.apify.com/v2"


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, text: str) -> None:
    ensure_parent(path)
    path.write_text(text, encoding="utf-8")


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def slugify(value: str, *, fallback: str = "note") -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or fallback


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def timestamp_slug(label: str) -> str:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{stamp}-{slugify(label)}"


def extract_json_text(text: str) -> Any:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, count=1)
        cleaned = re.sub(r"\s*```$", "", cleaned, count=1)
    return json.loads(cleaned)


def http_request(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    json_body: Any | None = None,
    timeout: int = 120,
) -> bytes:
    request_headers = dict(headers or {})
    data: bytes | None = None
    if json_body is not None:
        request_headers.setdefault("Content-Type", "application/json")
        data = json.dumps(json_body).encode("utf-8")

    request = urllib.request.Request(url, data=data, method=method, headers=request_headers)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.read()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} for {url}: {body}") from exc
    except urllib.error.URLError as exc:
        if "CERTIFICATE_VERIFY_FAILED" in str(exc):
            return curl_request(
                url,
                method=method,
                headers=request_headers,
                json_body=json_body,
                timeout=timeout,
            )
        raise RuntimeError(f"Request failed for {url}: {exc}") from exc


def curl_request(
    url: str,
    *,
    method: str,
    headers: dict[str, str],
    json_body: Any | None,
    timeout: int,
) -> bytes:
    command = [
        "curl",
        "-fsSL",
        "--max-time",
        str(timeout),
        "-X",
        method,
        url,
    ]
    for key, value in headers.items():
        command.extend(["-H", f"{key}: {value}"])
    body_bytes: bytes | None = None
    if json_body is not None:
        body_bytes = json.dumps(json_body).encode("utf-8")
        command.extend(["--data-binary", "@-"])

    result = subprocess.run(
        command,
        input=body_bytes,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        stderr = result.stderr.decode("utf-8", errors="replace")
        raise RuntimeError(f"curl failed for {url}: {stderr}")
    return result.stdout


def http_json_request(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    json_body: Any | None = None,
    timeout: int = 120,
) -> Any:
    raw = http_request(url, method=method, headers=headers, json_body=json_body, timeout=timeout)
    if not raw:
        return {}
    return json.loads(raw.decode("utf-8"))


def is_retryable_error(message: str) -> bool:
    lowered = message.lower()
    retry_markers = (
        "429",
        "500",
        "502",
        "503",
        "504",
        "resource_exhausted",
        "unavailable",
        "timeout",
        "deadline",
        "temporarily",
        "connection reset",
    )
    return any(marker in lowered for marker in retry_markers)


def gemini_generate_text(
    *,
    api_key: str,
    model: str,
    prompt: str,
    temperature: float = 0.4,
    system_instruction: str | None = None,
    retries: int = 0,
) -> str:
    clean_model = model.removeprefix("models/")
    url = (
        f"{GEMINI_API_BASE}/models/{urllib.parse.quote(clean_model)}:generateContent"
        f"?key={urllib.parse.quote(api_key)}"
    )
    payload: dict[str, Any] = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
        },
    }
    if system_instruction:
        payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}

    attempt = 0
    while True:
        attempt += 1
        try:
            response = http_json_request(url, method="POST", json_body=payload, timeout=180)
            candidates = response.get("candidates") or []
            for candidate in candidates:
                parts = candidate.get("content", {}).get("parts", [])
                for part in parts:
                    text = part.get("text")
                    if text:
                        return text
            raise RuntimeError(f"No text candidate found in Gemini response: {response}")
        except Exception as exc:
            if attempt > retries + 1 or not is_retryable_error(str(exc)):
                raise
            time.sleep(min(20, attempt * 2))


def gemini_generate_json(
    *,
    api_key: str,
    model: str,
    prompt: str,
    schema: dict[str, Any],
    temperature: float = 0.2,
    retries: int = 0,
) -> Any:
    clean_model = model.removeprefix("models/")
    url = (
        f"{GEMINI_API_BASE}/models/{urllib.parse.quote(clean_model)}:generateContent"
        f"?key={urllib.parse.quote(api_key)}"
    )
    payload: dict[str, Any] = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": temperature,
            "responseMimeType": "application/json",
            "responseJsonSchema": schema,
        },
    }

    attempt = 0
    while True:
        attempt += 1
        try:
            response = http_json_request(url, method="POST", json_body=payload, timeout=180)
            candidates = response.get("candidates") or []
            for candidate in candidates:
                parts = candidate.get("content", {}).get("parts", [])
                for part in parts:
                    text = part.get("text")
                    if text:
                        return extract_json_text(text)
            raise RuntimeError(f"No JSON candidate found in Gemini response: {response}")
        except Exception as exc:
            if attempt > retries + 1 or not is_retryable_error(str(exc)):
                raise
            time.sleep(min(20, attempt * 2))


class ArticleTextParser(HTMLParser):
    BLOCK_TAGS = {"title", "h1", "h2", "h3", "h4", "p", "li", "blockquote", "pre"}
    SKIP_TAGS = {"script", "style", "noscript", "svg", "path"}

    def __init__(self) -> None:
        super().__init__()
        self._skip_depth = 0
        self._capture_tag: str | None = None
        self._buffer: list[str] = []
        self.chunks: list[str] = []
        self.title: str = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in self.SKIP_TAGS:
            self._skip_depth += 1
            return
        if self._skip_depth:
            return
        if tag in self.BLOCK_TAGS:
            self._capture_tag = tag
            self._buffer = []

    def handle_endtag(self, tag: str) -> None:
        if tag in self.SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1
            return
        if self._skip_depth:
            return
        if tag == self._capture_tag:
            text = re.sub(r"\s+", " ", "".join(self._buffer)).strip()
            if text:
                if tag == "title" and not self.title:
                    self.title = text
                else:
                    self.chunks.append(text)
            self._capture_tag = None
            self._buffer = []

    def handle_data(self, data: str) -> None:
        if self._skip_depth or self._capture_tag is None:
            return
        self._buffer.append(data)


def extract_text_from_html(html: str) -> tuple[str, str]:
    parser = ArticleTextParser()
    parser.feed(html)
    title = parser.title.strip()
    text = "\n\n".join(chunk for chunk in parser.chunks if chunk.strip())
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    return title, text


def apify_run_sync(actor_id: str, payload: dict[str, Any], *, memory_mb: int | None = None) -> Any:
    api_key = os.environ.get("APIFY_API_KEY")
    if not api_key:
        raise RuntimeError("Missing APIFY_API_KEY in environment")
    safe_actor_id = urllib.parse.quote(actor_id, safe="~")
    query = f"token={urllib.parse.quote(api_key)}"
    if memory_mb is not None:
        query += f"&memory={int(memory_mb)}"
    url = f"{APIFY_API_BASE}/acts/{safe_actor_id}/run-sync-get-dataset-items?{query}"
    return http_json_request(url, method="POST", json_body=payload, timeout=180)


def fetch_url_source(url: str) -> tuple[str, str]:
    return _fetch_url_source(url, visited={canonicalize_url(url)})


def _fetch_url_source(url: str, *, visited: set[str]) -> tuple[str, str]:
    resolved = resolve_redirects(url)
    if resolved and resolved != url:
        resolved_canonical = canonicalize_url(resolved)
        if resolved_canonical in visited:
            raise RuntimeError(f"Resolved URL already visited: {resolved}")
        visited = visited | {resolved_canonical}
        url = resolved
    try:
        return fetch_url_source_via_apify(url, visited=visited)
    except Exception as direct_exc:
        try:
            return search_web_fallback(url)
        except Exception as search_exc:
            raise RuntimeError(
                f"URL ingestion failed for {url}. "
                f"Apify direct read error: {direct_exc}. "
                f"Web search fallback error: {search_exc}"
            ) from search_exc


def resolve_redirects(url: str, *, max_hops: int = 5, timeout: float = 10.0) -> str:
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    shortener_hosts = {"t.co", "bit.ly", "buff.ly", "ow.ly", "tinyurl.com", "goo.gl", "lnkd.in"}
    if host not in shortener_hosts:
        return url

    current = url
    for _ in range(max_hops):
        try:
            request = urllib.request.Request(current, method="HEAD", headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(request, timeout=timeout) as response:
                final = response.geturl()
        except Exception:
            try:
                request = urllib.request.Request(current, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(request, timeout=timeout) as response:
                    final = response.geturl()
            except Exception:
                return current
        if final == current:
            return final
        current = final
        next_parsed = urllib.parse.urlparse(current)
        next_host = next_parsed.netloc.lower()
        if next_host.startswith("www."):
            next_host = next_host[4:]
        if next_host not in shortener_hosts:
            return current
    return current


def fetch_url_source_via_apify(url: str, *, visited: set[str] | None = None) -> tuple[str, str]:
    parsed_url = urllib.parse.urlparse(url)
    host = parsed_url.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    visited = set(visited or {canonicalize_url(url)})

    if host in {"x.com", "twitter.com"}:
        tweet_id = extract_tweet_id(url)
        if tweet_id:
            items = apify_run_sync(
                "kawsar~unlimited-twitter-scraper",
                {"tweetIds": [tweet_id]},
            )
            if isinstance(items, list) and items:
                return normalize_tweet_item(items[0], visited=visited)
            raise RuntimeError(f"No tweet data returned for {url}")

    items = apify_run_sync(
        "apify~website-content-crawler",
        {
            "startUrls": [{"url": url}],
            "maxCrawlPages": 1,
            "outputFormat": "markdown",
            "crawlerType": "playwright:adaptive",
        },
        memory_mb=2048,
    )
    if not isinstance(items, list) or not items:
        raise RuntimeError(f"No page data returned for {url}")
    return normalize_page_item(items[0], url)


def search_web_fallback(url: str) -> tuple[str, str]:
    queries = build_search_queries(url)
    errors: list[str] = []
    parsed_url = urllib.parse.urlparse(url)
    host = parsed_url.netloc.lower()
    if host.startswith("www."):
        host = host[4:]

    for query in queries:
        try:
            search_url = "https://search.brave.com/search?q=" + urllib.parse.quote(query) + "&source=web"
            raw_html = http_request(
                search_url,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                },
                timeout=60,
            )
            title, body = extract_text_from_html(raw_html.decode("utf-8", errors="replace"))
            body = body.strip()
            if len(body) < 120:
                raise RuntimeError(f"Search results page was too thin for query {query!r}")
            if not search_results_match_url(url, host, body):
                raise RuntimeError(f"Search results were not relevant enough for query {query!r}")
            title = title or f"Search fallback for {url}"
            wrapped = (
                f"Original URL: {url}\n"
                f"Search query: {query}\n"
                f"Search engine URL: {search_url}\n\n"
                f"{body}"
            )
            return title, wrapped
        except Exception as exc:
            errors.append(f"{query!r}: {exc}")

    raise RuntimeError("; ".join(errors) or f"No search fallback results for {url}")


def build_search_queries(url: str) -> list[str]:
    parsed = urllib.parse.urlparse(url)
    host = parsed.netloc.lower()
    if host.startswith("www."):
        host = host[4:]

    queries: list[str] = [f'"{url}"']
    tweet_id = extract_tweet_id(url)
    if host in {"x.com", "twitter.com"} and tweet_id:
        path_parts = [part for part in parsed.path.split("/") if part]
        handle = path_parts[0] if path_parts else ""
        if handle:
            queries.append(f'"{tweet_id}" site:x.com/{handle}')
        queries.append(f'"{tweet_id}" site:x.com')
        queries.append(f'"{tweet_id}" site:twitter.com')
    else:
        path_hint = parsed.path.strip("/").replace("-", " ").replace("/", " ").strip()
        if path_hint:
            queries.append(f'site:{host} "{path_hint[:120]}"')
        queries.append(f"site:{host} {host}")

    seen: set[str] = set()
    ordered: list[str] = []
    for query in queries:
        clean = query.strip()
        if clean and clean not in seen:
            seen.add(clean)
            ordered.append(clean)
    return ordered


def search_results_match_url(url: str, host: str, body: str) -> bool:
    lowered = body.lower()
    if host not in lowered:
        return False

    parsed = urllib.parse.urlparse(url)
    tweet_id = extract_tweet_id(url)
    if tweet_id:
        return tweet_id in lowered

    path_tokens = [
        token
        for token in re.split(r"[^a-z0-9]+", parsed.path.lower())
        if len(token) >= 4 and token not in {"html", "amp", "index", "article", "blog", "post", "posts"}
    ]
    if not path_tokens:
        return lowered.count(host) >= 2
    return any(token in lowered for token in path_tokens[:4])


def extract_tweet_id(url: str) -> str | None:
    match = re.search(r"/status/(\d+)", url)
    if match:
        return match.group(1)
    return None


def canonicalize_url(url: str) -> str:
    parsed = urllib.parse.urlsplit(url.strip())
    scheme = (parsed.scheme or "https").lower()
    netloc = parsed.netloc.lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    path = parsed.path or "/"
    query = parsed.query
    if netloc in {"x.com", "twitter.com"}:
        status_match = re.match(r"^(/[^/]+/status/\d+)", path)
        if status_match:
            path = status_match.group(1)
            query = ""
    return urllib.parse.urlunsplit((scheme, netloc, path, query, ""))


def extract_external_urls(item: dict[str, Any]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []

    def _add(candidate: Any) -> None:
        if not isinstance(candidate, str):
            return
        url = candidate.strip().rstrip(".,);]")
        if not url:
            return
        normalized = canonicalize_url(url)
        if normalized in seen:
            return
        seen.add(normalized)
        ordered.append(url)

    for candidate in item.get("externalUrls") or []:
        _add(candidate)

    text = str(item.get("text") or "")
    for match in re.findall(r"https?://[^\s<>\"']+", text):
        _add(match)

    return ordered


def text_is_plain_url(text: str) -> bool:
    return bool(re.fullmatch(r"https?://\S+", text.strip()))


def expand_external_sources(urls: list[str], *, visited: set[str]) -> list[tuple[str, str, str]]:
    expanded: list[tuple[str, str, str]] = []
    for external_url in urls:
        normalized = canonicalize_url(external_url)
        if normalized in visited:
            continue
        try:
            linked_title, linked_body = _fetch_url_source(
                external_url,
                visited=visited | {normalized},
            )
        except Exception:
            continue
        expanded.append((external_url, linked_title, linked_body))
    return expanded


def normalize_tweet_item(item: dict[str, Any], *, visited: set[str]) -> tuple[str, str]:
    raw_text = str(item.get("text") or "")
    text = html.unescape(raw_text).strip()
    if not text:
        raise RuntimeError("Tweet payload contained no text")
    item = {**item, "text": text}
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    author_name = item.get("authorName") or "Unknown author"
    author_username = item.get("authorUsername") or ""
    created_at = item.get("createdAt") or ""
    likes = item.get("likes")
    replies = item.get("replies")
    url = item.get("url") or ""
    external_urls = extract_external_urls(item)
    expanded_sources = expand_external_sources(external_urls, visited=visited)

    if lines and not text_is_plain_url(text):
        title = lines[0][:120]
    elif expanded_sources:
        title = expanded_sources[0][1][:120]
    else:
        title = f"X Post by {author_name}"

    body_lines = [
        f"Source URL: {url}",
        f"Author: {author_name}" + (f" (@{author_username})" if author_username else ""),
    ]
    if created_at:
        body_lines.append(f"Published: {created_at}")
    if likes is not None:
        body_lines.append(f"Likes: {likes}")
    if replies is not None:
        body_lines.append(f"Replies: {replies}")
    body_lines.append("")
    body_lines.append(text)
    if external_urls:
        body_lines.append("")
        body_lines.append("External URLs:")
        for external_url in external_urls:
            body_lines.append(f"- {external_url}")
    for external_url, linked_title, linked_body in expanded_sources:
        body_lines.append("")
        body_lines.append(f"## Linked Source: {linked_title}")
        body_lines.append(f"Linked URL: {external_url}")
        body_lines.append("")
        body_lines.append(linked_body.strip())
    return title, "\n".join(body_lines).strip()


def normalize_page_item(item: dict[str, Any], original_url: str) -> tuple[str, str]:
    metadata = item.get("metadata") or {}
    title = str(metadata.get("title") or "").strip()
    markdown = str(item.get("markdown") or "").strip()
    text = str(item.get("text") or "").strip()
    body = markdown or text
    if not body:
        raise RuntimeError(f"Apify page reader returned no body for {original_url}")
    if not title:
        parsed = urllib.parse.urlparse(original_url)
        title = slugify(parsed.netloc + "-" + parsed.path, fallback="source").replace("-", " ").title()
    if is_placeholder_page(title, body, original_url):
        raise RuntimeError(f"Apify page reader returned a placeholder page for {original_url}")
    return title, body


def is_placeholder_page(title: str, body: str, original_url: str) -> bool:
    lowered_title = title.lower()
    lowered_body = body.lower()

    placeholder_markers = (
        "page not found / x",
        "# page not found",
        "don’t miss what’s happening",
        "don't miss what's happening",
        "people on x are the first to know",
    )
    if lowered_title == "page not found / x":
        return True
    if any(marker in lowered_body for marker in placeholder_markers):
        return True
    return False
