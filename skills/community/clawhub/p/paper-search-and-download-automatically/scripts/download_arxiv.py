#!/usr/bin/env python3
"""Search and download related arXiv papers."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Iterable

ARXIV_API = "https://export.arxiv.org/api/query"
ATOM_NS = {"atom": "http://www.w3.org/2005/Atom"}


class TLSVerificationError(RuntimeError):
    """Raised when HTTPS certificate verification fails for arXiv endpoints."""


STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "that",
    "this",
    "using",
    "into",
    "via",
    "based",
    "learning",
    "model",
    "models",
    "approach",
    "method",
    "methods",
    "paper",
    "study",
}

_SSL_CONTEXT = ssl.create_default_context()


def _raise_if_bad_cert(err: BaseException) -> None:
    if "CERTIFICATE_VERIFY_FAILED" in str(err):
        raise TLSVerificationError(
            "TLS certificate verification failed (HTTPS to arXiv). "
            "Fix your Python trust store (e.g. on macOS run "
            "'Install Certificates.command' in the Python folder, or use a "
            "Python build with up-to-date CA certificates). "
            "This script does not disable TLS verification."
        ) from err


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Download arXiv PDFs by (topic + date range) or from a seed paper "
            "(id/title) and save into ./arxiv."
        )
    )
    parser.add_argument("--topic", help="Search topic, e.g. 'graph neural network'")
    parser.add_argument("--start-date", help="YYYY-MM-DD")
    parser.add_argument("--end-date", help="YYYY-MM-DD")
    parser.add_argument("--seed-id", help="Seed arXiv id, e.g. 2401.12345v1")
    parser.add_argument("--seed-title", help="Seed paper title")
    parser.add_argument(
        "--max-results", type=int, default=20, help="Number of papers to fetch (default 20)"
    )
    parser.add_argument(
        "--output-dir",
        default="arxiv",
        help="Directory to save PDFs (default ./arxiv)",
    )
    return parser.parse_args()


def ensure_valid_dates(start_date: str | None, end_date: str | None) -> tuple[str | None, str | None]:
    if not start_date and not end_date:
        return None, None
    if not (start_date and end_date):
        raise ValueError("Both --start-date and --end-date are required when using date range.")
    start = dt.date.fromisoformat(start_date)
    end = dt.date.fromisoformat(end_date)
    if start > end:
        raise ValueError("--start-date must be earlier than or equal to --end-date.")
    return start.isoformat(), end.isoformat()


def date_clause(start_date: str | None, end_date: str | None) -> str | None:
    if not start_date or not end_date:
        return None
    start = start_date.replace("-", "") + "0000"
    end = end_date.replace("-", "") + "2359"
    return f"submittedDate:[{start} TO {end}]"


def fetch_xml(url: str, timeout: int = 30) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "arxiv-related-papers-skill/1.0"})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=_SSL_CONTEXT) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as err:
            if err.code not in (429, 503) or attempt == 3:
                raise
            sleep_s = 1.5 * (2**attempt)
            print(f"WARN: arXiv rate limited ({err.code}), retrying in {sleep_s:.1f}s.", file=sys.stderr)
            time.sleep(sleep_s)
        except urllib.error.URLError as err:
            _raise_if_bad_cert(err)
            raise
    raise RuntimeError("Unexpected fetch loop termination")


def arxiv_query(search_query: str, max_results: int) -> list[dict]:
    params = {
        "search_query": search_query,
        "start": "0",
        "max_results": str(max_results),
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    url = ARXIV_API + "?" + urllib.parse.urlencode(params)
    xml_text = fetch_xml(url)
    return parse_feed(xml_text)


def get_seed_by_id(seed_id: str) -> dict | None:
    params = {"id_list": seed_id}
    url = ARXIV_API + "?" + urllib.parse.urlencode(params)
    entries = parse_feed(fetch_xml(url))
    return entries[0] if entries else None


def get_seed_by_title(seed_title: str) -> dict | None:
    q = f'ti:"{seed_title}"'
    entries = arxiv_query(q, max_results=1)
    return entries[0] if entries else None


def parse_feed(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    entries = []
    for entry in root.findall("atom:entry", ATOM_NS):
        eid = text_or_none(entry.find("atom:id", ATOM_NS))
        title = normalize_space(text_or_none(entry.find("atom:title", ATOM_NS)) or "")
        updated = text_or_none(entry.find("atom:updated", ATOM_NS))
        summary = normalize_space(text_or_none(entry.find("atom:summary", ATOM_NS)) or "")
        categories = [cat.attrib.get("term", "") for cat in entry.findall("atom:category", ATOM_NS)]
        pdf_url = None
        for link in entry.findall("atom:link", ATOM_NS):
            href = link.attrib.get("href")
            ltype = link.attrib.get("type")
            title_attr = link.attrib.get("title")
            if (title_attr == "pdf" or ltype == "application/pdf") and href:
                pdf_url = href
                break
        if not pdf_url and eid:
            arxiv_id = eid.rsplit("/", 1)[-1]
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
        entries.append(
            {
                "id": eid,
                "title": title,
                "updated": updated,
                "summary": summary,
                "categories": [c for c in categories if c],
                "pdf_url": pdf_url,
            }
        )
    return entries


def text_or_none(node: ET.Element | None) -> str | None:
    return node.text if node is not None else None


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def extract_keywords(text: str, limit: int = 6) -> list[str]:
    words = re.findall(r"[A-Za-z0-9\-]{4,}", text.lower())
    keys = []
    for w in words:
        if w in STOPWORDS:
            continue
        if w not in keys:
            keys.append(w)
        if len(keys) >= limit:
            break
    return keys


def build_related_query(seed: dict, start_date: str | None, end_date: str | None) -> str:
    title = seed.get("title", "")
    categories = seed.get("categories", [])
    keywords = extract_keywords(title)
    clauses: list[str] = []

    if categories:
        top_cats = categories[:3]
        clauses.append("(" + " OR ".join(f"cat:{c}" for c in top_cats) + ")")

    if keywords:
        clauses.append(f'all:"{" ".join(keywords)}"')

    if not clauses:
        clauses.append('all:"machine learning"')

    d_clause = date_clause(start_date, end_date)
    if d_clause:
        clauses.append(d_clause)
    return " AND ".join(clauses)


def build_topic_query(topic: str, start_date: str | None, end_date: str | None) -> str:
    clauses = [f'all:"{topic}"']
    d_clause = date_clause(start_date, end_date)
    if d_clause:
        clauses.append(d_clause)
    return " AND ".join(clauses)


def sanitize_title(title: str, max_len: int = 140) -> str:
    cleaned = re.sub(r"[^\w\-\s]", "", title, flags=re.UNICODE)
    cleaned = re.sub(r"\s+", "_", cleaned).strip("_")
    return (cleaned[:max_len] or "untitled").rstrip("_")


def version_and_date(arxiv_id_url: str | None, updated: str | None) -> str:
    version = "v1"
    if arxiv_id_url:
        raw = arxiv_id_url.rsplit("/", 1)[-1]
        m = re.search(r"v(\d+)$", raw)
        if m:
            version = f"v{m.group(1)}"
    date = "00000000"
    if updated:
        try:
            date_obj = dt.datetime.fromisoformat(updated.replace("Z", "+00:00"))
            date = date_obj.strftime("%Y%m%d")
        except ValueError:
            pass
    return f"{version}_{date}"


def download_file(url: str, destination: Path, timeout: int = 60) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": "arxiv-related-papers-skill/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=_SSL_CONTEXT) as resp:
            data = resp.read()
    except urllib.error.URLError as err:
        _raise_if_bad_cert(err)
        raise
    destination.write_bytes(data)


def dedupe_entries(entries: Iterable[dict]) -> list[dict]:
    seen = set()
    out = []
    for e in entries:
        key = e.get("id") or e.get("title")
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(e)
    return out


def main() -> int:
    args = parse_args()
    try:
        start_date, end_date = ensure_valid_dates(args.start_date, args.end_date)
    except ValueError as err:
        print(f"ERROR: {err}", file=sys.stderr)
        return 2

    if args.max_results <= 0:
        print("ERROR: --max-results must be > 0", file=sys.stderr)
        return 2

    has_topic_mode = bool(args.topic)
    has_seed_mode = bool(args.seed_id or args.seed_title)
    if has_topic_mode == has_seed_mode:
        print(
            "ERROR: Provide either topic mode (--topic) or seed mode (--seed-id/--seed-title), not both.",
            file=sys.stderr,
        )
        return 2

    try:
        if has_topic_mode:
            query = build_topic_query(args.topic, start_date, end_date)
            entries = arxiv_query(query, args.max_results)
        else:
            seed = get_seed_by_id(args.seed_id) if args.seed_id else get_seed_by_title(args.seed_title)
            if not seed:
                print("ERROR: Seed paper not found on arXiv.", file=sys.stderr)
                return 1
            query = build_related_query(seed, start_date, end_date)
            entries = arxiv_query(query, args.max_results + 1)
            seed_id = seed.get("id")
            entries = [e for e in entries if e.get("id") != seed_id][: args.max_results]
    except (urllib.error.URLError, ET.ParseError, TLSVerificationError) as err:
        print(f"ERROR: failed to query arXiv API: {err}", file=sys.stderr)
        return 1

    entries = dedupe_entries(entries)
    if not entries:
        print("No papers found.")
        return 0

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    downloaded = 0
    skipped = 0
    for idx, entry in enumerate(entries, start=1):
        title = entry.get("title") or "untitled"
        stamp = version_and_date(entry.get("id"), entry.get("updated"))
        file_name = f"{stamp}-{sanitize_title(title)}.pdf"
        destination = out_dir / file_name

        if destination.exists():
            skipped += 1
            print(f"[{idx}/{len(entries)}] SKIP exists: {destination.name}")
            continue

        pdf_url = entry.get("pdf_url")
        if not pdf_url:
            skipped += 1
            print(f"[{idx}/{len(entries)}] SKIP no PDF URL: {title}")
            continue

        try:
            download_file(pdf_url, destination)
            downloaded += 1
            print(f"[{idx}/{len(entries)}] DOWNLOADED: {destination.name}")
            time.sleep(0.4)
        except (urllib.error.URLError, TLSVerificationError) as err:
            skipped += 1
            print(f"[{idx}/{len(entries)}] FAIL {title}: {err}")

    print("---")
    print(f"Query: {query}")
    print(f"Found: {len(entries)}")
    print(f"Downloaded: {downloaded}")
    print(f"Skipped: {skipped}")
    print(f"Output: {out_dir.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
