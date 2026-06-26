#!/usr/bin/env python3
"""Palest Ink - Web Page Content Collector

Fetches web page content for URLs marked with content_pending=true.
Extracts main text content and keywords, then updates the JSONL records.
"""

import json
import os
import re
import tempfile
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

PALEST_INK_DIR = os.path.expanduser("~/.palest-ink")
CONFIG_FILE = os.path.join(PALEST_INK_DIR, "config.json")
DATA_DIR = os.path.join(PALEST_INK_DIR, "data")

# Tags whose content should be ignored
IGNORE_TAGS = {"script", "style", "noscript", "header", "nav", "footer", "aside", "iframe"}

# Common stop words for keyword extraction (English + Chinese punctuation)
STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "may", "might", "must", "can", "could", "and", "but", "or",
    "nor", "not", "so", "yet", "for", "of", "in", "on", "at", "to", "from",
    "by", "with", "as", "this", "that", "these", "those", "it", "its",
    "i", "you", "he", "she", "we", "they", "me", "him", "her", "us", "them",
    "my", "your", "his", "our", "their", "what", "which", "who", "whom",
    "if", "then", "than", "when", "where", "how", "all", "each", "every",
    "both", "few", "more", "most", "other", "some", "such", "no", "only",
    "own", "same", "too", "very", "just", "about", "above", "after", "before",
    "between", "into", "through", "during", "up", "down", "out", "off", "over",
    "under", "again", "further", "once", "here", "there", "any", "also",
    "的", "了", "在", "是", "我", "有", "和", "就", "不", "人", "都", "一",
    "这", "中", "大", "为", "上", "个", "国", "他", "到", "说", "们", "会",
}


class TextExtractor(HTMLParser):
    """Extract readable text from HTML, ignoring scripts/styles/nav."""

    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.ignore_depth = 0
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in IGNORE_TAGS:
            self.ignore_depth += 1
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in IGNORE_TAGS and self.ignore_depth > 0:
            self.ignore_depth -= 1
        if tag == "title":
            self._in_title = False
        # Add space after block elements
        if tag in ("p", "div", "h1", "h2", "h3", "h4", "h5", "h6",
                    "li", "td", "th", "br", "tr", "section", "article"):
            self.text_parts.append(" ")

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self.ignore_depth == 0:
            self.text_parts.append(data)

    def get_text(self):
        text = " ".join(self.text_parts)
        # Collapse whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        return text


def extract_keywords(text, max_keywords=10):
    """Extract keywords from text using simple word frequency."""
    # Split into words (handles both English and Chinese via simple approach)
    words = re.findall(r'[\w\u4e00-\u9fff]{2,}', text.lower())
    freq = {}
    for w in words:
        if w not in STOP_WORDS and not w.isdigit():
            freq[w] = freq.get(w, 0) + 1

    sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return [w for w, _ in sorted_words[:max_keywords]]


def fetch_content(url, timeout=10):
    """Fetch and extract text content from a URL."""
    try:
        req = Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        with urlopen(req, timeout=timeout) as resp:
            content_type = resp.headers.get("Content-Type", "")
            if "text/html" not in content_type and "text/plain" not in content_type:
                return None, None

            charset = "utf-8"
            if "charset=" in content_type:
                charset = content_type.split("charset=")[-1].split(";")[0].strip()

            html = resp.read(500_000).decode(charset, errors="replace")

        parser = TextExtractor()
        parser.feed(html)
        text = parser.get_text()
        return text, parser.title

    except (URLError, HTTPError, OSError, UnicodeDecodeError, ValueError) as e:
        return None, None


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {}


def collect():
    config = load_config()
    if not config.get("collectors", {}).get("content", True):
        return

    content_cfg = config.get("content_fetch", {})
    max_urls = content_cfg.get("max_urls_per_run", 50)
    summary_max = content_cfg.get("summary_max_chars", 800)
    timeout = content_cfg.get("timeout_seconds", 10)

    # Find today's and yesterday's data files
    now = datetime.now(timezone.utc)
    dates_to_check = [now]
    # Also check yesterday (for late-night browsing)
    from datetime import timedelta
    dates_to_check.append(now - timedelta(days=1))

    urls_processed = 0

    for dt in dates_to_check:
        datafile = os.path.join(
            DATA_DIR, dt.strftime("%Y"), dt.strftime("%m"), f"{dt.strftime('%d')}.jsonl"
        )
        if not os.path.exists(datafile):
            continue

        # Read all records
        with open(datafile, "r") as f:
            lines = f.readlines()

        updated = False
        new_lines = []
        seen_urls = set()

        for line in lines:
            line = line.strip()
            if not line:
                new_lines.append(line)
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                new_lines.append(line)
                continue

            if (record.get("type") == "web_visit"
                    and record.get("data", {}).get("content_pending") is True
                    and urls_processed < max_urls):

                url = record["data"].get("url", "")

                # Skip duplicate URLs in same file
                if url in seen_urls:
                    record["data"]["content_pending"] = False
                    record["data"]["content_note"] = "duplicate_url"
                    new_lines.append(json.dumps(record, ensure_ascii=False))
                    updated = True
                    continue

                seen_urls.add(url)
                text, page_title = fetch_content(url, timeout=timeout)

                if text:
                    record["data"]["content_summary"] = text[:summary_max]
                    record["data"]["content_keywords"] = extract_keywords(text)
                    if page_title and not record["data"].get("title"):
                        record["data"]["title"] = page_title.strip()
                else:
                    record["data"]["content_error"] = True

                record["data"]["content_pending"] = False
                urls_processed += 1
                updated = True
                new_lines.append(json.dumps(record, ensure_ascii=False))
            else:
                new_lines.append(line)

        if updated:
            # Atomic write: write to temp file then rename
            tmp_fd, tmp_path = tempfile.mkstemp(
                dir=os.path.dirname(datafile), suffix=".tmp"
            )
            with os.fdopen(tmp_fd, "w") as f:
                f.write("\n".join(new_lines) + "\n")
            os.replace(tmp_path, datafile)

    if urls_processed > 0:
        print(f"[content] Fetched content for {urls_processed} URLs")


if __name__ == "__main__":
    collect()
