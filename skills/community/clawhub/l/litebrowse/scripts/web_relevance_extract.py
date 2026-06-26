#!/usr/bin/env python3

import argparse
import json
import math
import re
import sys
from collections import Counter
from dataclasses import dataclass
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from typing import List
from urllib.error import URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen


BLOCK_TAGS = {
    "article",
    "aside",
    "blockquote",
    "dd",
    "details",
    "div",
    "dl",
    "dt",
    "fieldset",
    "figcaption",
    "figure",
    "footer",
    "form",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "header",
    "li",
    "main",
    "nav",
    "p",
    "pre",
    "section",
    "summary",
    "td",
}
SKIP_TAGS = {"script", "style", "noscript", "svg", "canvas", "iframe"}
NOISE_HINTS = {
    "cookie",
    "privacy",
    "subscribe",
    "sign in",
    "log in",
    "advertisement",
    "promo",
    "menu",
    "navigation",
    "footer",
}
WORD_RE = re.compile(r"[a-z0-9][a-z0-9_\-./]{1,}", re.I)
SPACE_RE = re.compile(r"\s+")


def normalize_space(text: str) -> str:
    return SPACE_RE.sub(" ", text).strip()


def tokenize(text: str) -> List[str]:
    return [token.lower() for token in WORD_RE.findall(text)]


def split_sentences(text: str) -> List[str]:
    parts = re.split(r"(?<=[.!?])\s+", text)
    return [normalize_space(part) for part in parts if normalize_space(part)]


@dataclass
class Block:
    tag: str
    text: str
    depth: int


class ContentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.blocks: List[Block] = []
        self._current_parts: List[str] = []
        self._current_tag = "document"
        self._depth = 0
        self._skip_depth = 0

    def handle_starttag(self, tag: str, attrs) -> None:
        tag = tag.lower()
        if tag in SKIP_TAGS:
            self._skip_depth += 1
            return
        if self._skip_depth:
            return
        self._depth += 1
        if tag in BLOCK_TAGS:
            self._flush()
            self._current_tag = tag

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in SKIP_TAGS and self._skip_depth:
            self._skip_depth -= 1
            return
        if self._skip_depth:
            return
        if tag in BLOCK_TAGS:
            self._flush()
            self._current_tag = "document"
        self._depth = max(0, self._depth - 1)

    def handle_data(self, data: str) -> None:
        if self._skip_depth:
            return
        text = normalize_space(unescape(data))
        if text:
            self._current_parts.append(text)

    def _flush(self) -> None:
        text = normalize_space(" ".join(self._current_parts))
        if text:
            self.blocks.append(Block(tag=self._current_tag, text=text, depth=self._depth))
        self._current_parts = []

    def close(self) -> None:
        self._flush()
        super().close()


def load_source(source: str, timeout: float) -> str:
    parsed = urlparse(source)
    if parsed.scheme in {"http", "https"}:
        request = Request(
            source,
            headers={
                "User-Agent": "Mozilla/5.0 (compatible; web-relevance-extract/1.0)"
            },
        )
        try:
            with urlopen(request, timeout=timeout) as response:
                charset = response.headers.get_content_charset() or "utf-8"
                return response.read().decode(charset, errors="replace")
        except URLError as exc:
            raise SystemExit(f"Failed to fetch {source}: {exc}") from exc
    return Path(source).read_text(encoding="utf-8")


def compact_text(text: str, max_chars: int) -> str:
    text = normalize_space(text)
    if len(text) <= max_chars:
        return text
    sentences = split_sentences(text)
    if not sentences:
        return text[: max_chars - 1].rstrip() + "..."
    parts = []
    size = 0
    for sentence in sentences:
        extra = len(sentence) + (1 if parts else 0)
        if size + extra > max_chars:
            break
        parts.append(sentence)
        size += extra
    if parts:
        return " ".join(parts)
    return text[: max_chars - 1].rstrip() + "..."


def score_block(text: str, tag: str, query_terms: Counter, global_counts: Counter) -> float:
    lowered = text.lower()
    tokens = tokenize(lowered)
    if not tokens:
        return -1.0

    token_counts = Counter(tokens)
    overlap = sum(min(token_counts[term], weight) for term, weight in query_terms.items())
    unique_overlap = sum(1 for term in query_terms if term in token_counts)
    rarity = sum(1.0 / math.log(global_counts[term] + 2.0) for term in query_terms if term in token_counts)
    density = overlap / max(len(tokens), 1)

    baseline = min(len(tokens), 80) / 80.0
    if tag in {"h1", "h2", "h3", "p", "li", "article", "section"}:
        baseline += 0.2

    score = baseline + overlap * 2.5 + unique_overlap * 1.8 + rarity * 2.0 + density * 25.0

    if len(tokens) < 8:
        score -= 1.5
    if any(hint in lowered for hint in NOISE_HINTS):
        score -= 4.0
    if re.fullmatch(r"[\W\d_]+", text):
        score -= 5.0
    return score


def rank_blocks(blocks: List[Block], query: str, per_block_chars: int) -> List[dict]:
    query_terms = Counter(tokenize(query))
    if not query_terms:
        raise SystemExit("Query must contain at least one searchable term.")

    global_counts = Counter()
    for block in blocks:
        global_counts.update(set(tokenize(block.text)))

    ranked = []
    seen = set()
    for index, block in enumerate(blocks):
        snippet = compact_text(block.text, per_block_chars)
        if len(snippet) < 10:
            continue
        normalized = snippet.lower()
        if normalized in seen:
            continue
        seen.add(normalized)
        score = score_block(snippet, block.tag, query_terms, global_counts)
        if score <= 0:
            continue
        ranked.append(
            {
                "rank": 0,
                "score": round(score, 3),
                "tag": block.tag,
                "index": index,
                "text": snippet,
                "approx_tokens": max(1, math.ceil(len(snippet) / 4)),
            }
        )

    ranked.sort(key=lambda item: item["score"], reverse=True)
    for rank, item in enumerate(ranked, start=1):
        item["rank"] = rank
    return ranked


def build_output(source: str, query: str, ranked: List[dict], top_k: int, max_chars: int) -> dict:
    selected = []
    used_chars = 0
    for item in ranked:
        if len(selected) >= top_k:
            break
        text = item["text"]
        extra = len(text) + (2 if selected else 0)
        if selected and used_chars + extra > max_chars:
            continue
        if not selected and len(text) > max_chars:
            item = {**item, "text": compact_text(text, max_chars)}
            extra = len(item["text"])
        selected.append(item)
        used_chars += extra

    return {
        "source": source,
        "query": query,
        "selected_blocks": len(selected),
        "used_chars": used_chars,
        "approx_tokens": max(1, math.ceil(used_chars / 4)),
        "results": selected,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract the most query-relevant blocks from a webpage with a strict token budget."
    )
    parser.add_argument("source", help="HTTP(S) URL or local HTML file path.")
    parser.add_argument("query", help="What you want to find on the page.")
    parser.add_argument("--top-k", type=int, default=5, help="Maximum number of blocks to return.")
    parser.add_argument(
        "--max-chars",
        type=int,
        default=2400,
        help="Total character budget across selected blocks.",
    )
    parser.add_argument(
        "--per-block-chars",
        type=int,
        default=700,
        help="Character budget per candidate block before ranking.",
    )
    parser.add_argument("--timeout", type=float, default=20.0, help="HTTP timeout in seconds.")
    parser.add_argument(
        "--format",
        choices=("json", "text"),
        default="json",
        help="Output format.",
    )
    return parser.parse_args()


def render_text(payload: dict) -> str:
    lines = [
        f"Source: {payload['source']}",
        f"Query: {payload['query']}",
        f"Selected blocks: {payload['selected_blocks']}",
        f"Approx tokens: {payload['approx_tokens']}",
    ]
    for item in payload["results"]:
        lines.append("")
        lines.append(f"[{item['rank']}] score={item['score']} tag={item['tag']} approx_tokens={item['approx_tokens']}")
        lines.append(item["text"])
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    html = load_source(args.source, args.timeout)
    parser = ContentParser()
    parser.feed(html)
    parser.close()
    ranked = rank_blocks(parser.blocks, args.query, args.per_block_chars)
    payload = build_output(args.source, args.query, ranked, args.top_k, args.max_chars)

    if args.format == "text":
        print(render_text(payload))
    else:
        json.dump(payload, sys.stdout, indent=2, ensure_ascii=True)
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
