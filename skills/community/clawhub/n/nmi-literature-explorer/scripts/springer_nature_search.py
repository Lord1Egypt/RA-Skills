#!/usr/bin/env python3
"""Search Springer Nature's Meta API for NMI metadata; no full text is fetched."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from datetime import datetime, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


API_URL = "https://api.springernature.com/meta/v2/json"
JOURNAL_TITLE = "Nature Machine Intelligence"
FIELDS = (
    "title",
    "authors",
    "doi",
    "publication_date",
    "online_date",
    "cover_date",
    "journal_title",
    "content_type",
    "url",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Search the Springer Nature Meta API for Nature Machine Intelligence "
            "metadata. Verify matches against the official NMI article page."
        )
    )
    parser.add_argument(
        "--query",
        help="A literal search phrase, for example: material large language model",
    )
    parser.add_argument(
        "--year",
        type=int,
        help="Publication year constraint, for example: 2026",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Number of results in this single request (1-100; default: 20)",
    )
    parser.add_argument(
        "--format",
        choices=("json", "csv"),
        default="json",
        help="Output format (default: json)",
    )
    args = parser.parse_args()

    if args.query is not None:
        args.query = args.query.strip()
    if not args.query and args.year is None:
        parser.error("provide --query, --year, or both")
    if args.query and ('"' in args.query or "\n" in args.query or "\r" in args.query):
        parser.error('--query must be plain text and must not contain quotation marks')
    if args.year is not None and not 1900 <= args.year <= 2200:
        parser.error("--year must be between 1900 and 2200")
    if not 1 <= args.limit <= 100:
        parser.error("--limit must be between 1 and 100")
    return args


def build_query(query: str | None, year: int | None) -> str:
    parts = [f'pub:"{JOURNAL_TITLE}"']
    if year is not None:
        parts.append(f"year:{year}")
    if query:
        phrase = " ".join(query.split())
        parts.append(f'"{phrase}"')
    return " ".join(parts)


def text_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, (int, float)):
        return str(value)
    return ""


def extract_authors(record: dict[str, Any]) -> str:
    authors = record.get("creators") or record.get("authors") or record.get("creator")
    if isinstance(authors, str):
        return authors.strip()
    if not isinstance(authors, list):
        return ""

    names: list[str] = []
    for author in authors:
        if isinstance(author, str):
            name = author.strip()
        elif isinstance(author, dict):
            name = (
                text_value(author.get("creator"))
                or text_value(author.get("name"))
                or text_value(author.get("fullName"))
            )
        else:
            name = ""
        if name:
            names.append(name)
    return "; ".join(names)


def extract_genres(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "; ".join(text_value(item) for item in value if text_value(item))
    return ""


def normalize_record(record: dict[str, Any]) -> dict[str, str]:
    doi = text_value(record.get("doi"))
    title = text_value(record.get("title"))
    journal_title = text_value(record.get("publicationName")) or text_value(
        record.get("journalTitle")
    )
    content_type = (
        text_value(record.get("contentType"))
        or text_value(record.get("articleType"))
        or extract_genres(record.get("genre"))
    )
    return {
        "title": title,
        "authors": extract_authors(record),
        "doi": doi,
        "publication_date": text_value(record.get("publicationDate")),
        "online_date": text_value(record.get("onlineDate")),
        "cover_date": text_value(record.get("coverDate")),
        "journal_title": journal_title,
        "content_type": content_type,
        "url": f"https://doi.org/{doi}" if doi else "",
    }


def fetch_records(api_key: str, query: str, limit: int) -> list[dict[str, Any]]:
    params = urlencode(
        {
            "api_key": api_key,
            "q": query,
            "s": 1,
            "p": limit,
        }
    )
    request = Request(
        f"{API_URL}?{params}",
        headers={
            "Accept": "application/json",
            "User-Agent": "nmi-literature-explorer/1.0 (metadata search)",
        },
    )
    try:
        with urlopen(request, timeout=30) as response:
            payload = json.load(response)
    except HTTPError as error:
        if error.code == 401:
            raise RuntimeError("Springer Nature rejected the API key (HTTP 401).") from None
        if error.code == 429:
            raise RuntimeError(
                "Springer Nature rate limit or daily quota reached (HTTP 429); retry later."
            ) from None
        raise RuntimeError(
            f"Springer Nature API request failed with HTTP {error.code}."
        ) from None
    except (URLError, TimeoutError):
        raise RuntimeError("Could not reach Springer Nature API (network error).") from None
    except json.JSONDecodeError:
        raise RuntimeError("Springer Nature API returned invalid JSON.") from None

    if not isinstance(payload, dict):
        raise RuntimeError("Springer Nature API returned an unexpected JSON response.")
    records = payload.get("records", [])
    if not isinstance(records, list):
        raise RuntimeError("Springer Nature API response did not contain a records list.")
    return [record for record in records if isinstance(record, dict)]


def emit_json(query: str, records: list[dict[str, str]]) -> None:
    result = {
        "source": "Springer Nature Meta API v2",
        "query": query,
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "metadata_only": True,
        "records": records,
    }
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


def emit_csv(records: list[dict[str, str]]) -> None:
    writer = csv.DictWriter(sys.stdout, fieldnames=FIELDS, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(records)


def main() -> int:
    args = parse_args()
    api_key = os.environ.get("SN_API_KEY", "").strip()
    if not api_key:
        print(
            "Set SN_API_KEY in the process environment to use the optional Springer Nature API.",
            file=sys.stderr,
        )
        return 2

    query = build_query(args.query, args.year)
    try:
        api_records = fetch_records(api_key, query, args.limit)
    except RuntimeError as error:
        print(str(error), file=sys.stderr)
        return 1

    records = [
        normalize_record(record)
        for record in api_records
        if (
            text_value(record.get("publicationName"))
            or text_value(record.get("journalTitle"))
        ).casefold()
        == JOURNAL_TITLE.casefold()
    ]
    if not records:
        print(
            "No exact Nature Machine Intelligence journalTitle matches were returned. "
            "Check the NMI archive and current API query constraints.",
            file=sys.stderr,
        )

    if args.format == "csv":
        emit_csv(records)
    else:
        emit_json(query, records)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
