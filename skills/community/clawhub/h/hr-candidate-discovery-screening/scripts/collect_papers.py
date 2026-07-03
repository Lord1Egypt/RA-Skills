from __future__ import annotations

import argparse
import calendar
import html
import json
import os
import re
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Iterable
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

from config import load_settings, load_sources
from db import Database
from models import PaperRecord


def reconstruct_abstract(index: dict[str, list[int]] | None) -> str | None:
    if not index:
        return None
    positions: dict[int, str] = {}
    for word, offsets in index.items():
        for offset in offsets:
            positions[int(offset)] = word
    return " ".join(positions[position] for position in sorted(positions))


def normalize_title(value: str) -> str:
    normalized = unicodedata.normalize("NFKC", value).casefold()
    normalized = re.sub(r"[^\w\s]", " ", normalized)
    return " ".join(normalized.split())


def normalize_doi(value: str | None) -> str | None:
    if not value:
        return None
    lowered = value.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if lowered.startswith(prefix):
            lowered = lowered[len(prefix) :]
            break
    return lowered or None


def parse_date_range(
    start_date: str | None, end_date: str | None
) -> tuple[date, date]:
    if not start_date:
        raise ValueError("start_date is required")
    if not end_date:
        raise ValueError("end_date is required")
    start = date.fromisoformat(start_date)
    end = date.fromisoformat(end_date)
    if start > end:
        raise ValueError("start_date must not be after end_date")
    return start, end


def coerce_config_date(value: str | date) -> date:
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value))


def _is_official_url(url: str | None, official_domains: list[str]) -> bool:
    if not url:
        return False
    hostname = (urlparse(url).hostname or "").lower()
    return any(
        hostname == domain.lower() or hostname.endswith(f".{domain.lower()}")
        for domain in official_domains
    )


def _official_openalex_url(raw: dict, official_domains: list[str]) -> str | None:
    locations = [raw.get("primary_location") or {}, *(raw.get("locations") or [])]
    for location in locations:
        url = location.get("landing_page_url")
        if _is_official_url(url, official_domains):
            return url
    return None


def _source_record_id(value: str) -> str:
    return value.rstrip("/").rsplit("/", 1)[-1]


def _authors(raw: dict) -> tuple[dict, ...]:
    result = []
    for index, authorship in enumerate(raw.get("authorships") or [], start=1):
        author = authorship.get("author") or {}
        result.append(
            {
                "openalex_id": author.get("id"),
                "name": author.get("display_name"),
                "order": index,
                "position": authorship.get("author_position"),
                "affiliations": authorship.get("raw_affiliation_strings") or [],
            }
        )
    return tuple(result)


def normalize_openalex_work(raw: dict, source: dict) -> PaperRecord | None:
    if raw.get("is_retracted"):
        return None
    if raw.get("type") in {"preprint", "posted-content"}:
        return None
    publication_date = raw.get("publication_date")
    title = (raw.get("title") or "").strip()
    source_id = raw.get("id")
    official_url = _official_openalex_url(raw, source.get("official_domains", []))
    if not publication_date or not title or not source_id:
        return None
    if not official_url:
        return None
    source_type = source.get("type")
    if not source_type:
        source_type = (
            "conference"
            if raw.get("type") in {"proceedings-article", "proceedings"}
            else "journal"
        )
    keywords = tuple(
        item["display_name"]
        for item in (raw.get("keywords") or [])
        if isinstance(item, dict) and item.get("display_name")
    )
    return PaperRecord(
        source_key=str(source["key"]),
        source_type=str(source_type),
        source_record_id=_source_record_id(str(source_id)),
        doi=normalize_doi(raw.get("doi")),
        title=title,
        normalized_title=normalize_title(title),
        publication_date=date.fromisoformat(publication_date),
        abstract=reconstruct_abstract(raw.get("abstract_inverted_index")),
        original_keywords=keywords,
        official_url=official_url,
        acceptance_evidence_url=official_url,
        is_retracted=False,
        authors=_authors(raw),
    )


def normalize_openalex_works(
    payload: dict,
    *,
    source: dict,
    start_date: date,
    end_date: date,
) -> list[PaperRecord]:
    records = []
    for raw in payload.get("results", []):
        record = normalize_openalex_work(raw, source)
        if record and start_date <= record.publication_date <= end_date:
            records.append(record)
    return records


def deduplicate_works(records: Iterable[PaperRecord]) -> list[PaperRecord]:
    unique: list[PaperRecord] = []
    seen_dois: set[str] = set()
    seen_source_ids: set[tuple[str, str]] = set()
    seen_titles: set[str] = set()
    for record in records:
        source_key = (record.source_key, record.source_record_id)
        if (
            (record.doi and record.doi in seen_dois)
            or source_key in seen_source_ids
            or record.normalized_title in seen_titles
        ):
            continue
        unique.append(record)
        if record.doi:
            seen_dois.add(record.doi)
        seen_source_ids.add(source_key)
        seen_titles.add(record.normalized_title)
    return unique


@dataclass(frozen=True)
class CollectionResult:
    source_key: str
    saved: int
    pages: int
    completed: bool


class OpenAlexCollector:
    SOURCES_URL = "https://api.openalex.org/sources"
    WORKS_URL = "https://api.openalex.org/works"

    def __init__(
        self,
        *,
        http=None,
        database: Database,
        mailto: str | None = None,
        per_page: int = 100,
        timeout: int = 60,
    ):
        self.http = http or requests.Session()
        self.database = database
        self.mailto = mailto
        self.per_page = per_page
        self.timeout = timeout

    def _params(self, values: dict) -> dict:
        params = dict(values)
        if self.mailto:
            params["mailto"] = self.mailto
        return params

    def resolve_source_id(self, source: dict) -> str:
        configured = source.get("openalex_id")
        if configured:
            return str(configured).rstrip("/").rsplit("/", 1)[-1]
        response = self.http.get(
            self.SOURCES_URL,
            params=self._params({"search": source["name"], "per-page": 10}),
            timeout=self.timeout,
            headers={"User-Agent": "hr-candidate-discovery-screening/1.0"},
        )
        response.raise_for_status()
        results = response.json().get("results", [])
        aliases = [source["name"], *(source.get("aliases") or [])]
        ranked = []
        for item in results:
            display_name = str(item.get("display_name") or "")
            lowered = display_name.casefold()
            if any(alias.casefold() in lowered for alias in aliases):
                ranked.append((len(display_name), item))
        if not ranked:
            raise ValueError(f"Unable to resolve OpenAlex source: {source['key']}")
        selected = sorted(ranked, key=lambda pair: pair[0])[0][1]
        return _source_record_id(str(selected["id"]))

    def collect(
        self,
        source: dict,
        start_date: date,
        end_date: date,
        *,
        limit: int | None = None,
        dry_run: bool = False,
    ) -> CollectionResult:
        source_id = self.resolve_source_id(source)
        start_text = start_date.isoformat()
        end_text = end_date.isoformat()
        cursor = (
            self.database.get_source_checkpoint(source["key"], start_text, end_text)
            or "*"
        )
        saved = 0
        pages = 0
        try:
            while cursor:
                response = self.http.get(
                    self.WORKS_URL,
                    params=self._params(
                        {
                            "filter": (
                                f"from_publication_date:{start_text},"
                                f"to_publication_date:{end_text},"
                                f"primary_location.source.id:{source_id}"
                            ),
                            "per-page": self.per_page,
                            "cursor": cursor,
                        }
                    ),
                    timeout=self.timeout,
                    headers={"User-Agent": "hr-candidate-discovery-screening/1.0"},
                )
                response.raise_for_status()
                payload = response.json()
                records = normalize_openalex_works(
                    payload,
                    source={**source, "type": "conference"},
                    start_date=start_date,
                    end_date=end_date,
                )
                if limit is not None:
                    records = records[: max(limit - saved, 0)]
                next_cursor = (payload.get("meta") or {}).get("next_cursor")
                pages += 1
                if dry_run:
                    saved += len(records)
                else:
                    saved += self.database.save_page_and_checkpoint(
                        records=records,
                        source_key=source["key"],
                        start_date=start_text,
                        end_date=end_text,
                        next_cursor=next_cursor,
                        completed=not next_cursor or (limit is not None and saved >= limit),
                    )
                if not next_cursor or (limit is not None and saved >= limit):
                    return CollectionResult(source["key"], saved, pages, True)
                cursor = next_cursor
        except Exception as exc:
            if not dry_run:
                self.database.mark_source_error(
                    source["key"], start_text, end_text, str(exc)
                )
            raise
        return CollectionResult(source["key"], saved, pages, True)


def _strip_markup(value: str | None) -> str | None:
    if not value:
        return None
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", value)).split())


def _crossref_date(item: dict) -> date | None:
    for key in ("published-online", "published-print", "issued"):
        parts = ((item.get(key) or {}).get("date-parts") or [])
        if not parts:
            continue
        values = list(parts[0])
        while len(values) < 3:
            values.append(1)
        return date(int(values[0]), int(values[1]), int(values[2]))
    return None


def normalize_crossref_item(raw: dict, source: dict) -> PaperRecord | None:
    title_values = raw.get("title") or []
    title = str(title_values[0]).strip() if title_values else ""
    published = _crossref_date(raw)
    official_url = raw.get("URL")
    doi = normalize_doi(raw.get("DOI"))
    url_is_accepted = _is_official_url(
        official_url, source.get("official_domains", [])
    ) or (
        doi is not None
        and (urlparse(official_url or "").hostname or "").lower() == "doi.org"
    )
    if (
        not title
        or published is None
        or not url_is_accepted
        or raw.get("update-to")
        or title.casefold().startswith("retracted:")
    ):
        return None
    authors = []
    for index, author in enumerate(raw.get("author") or [], start=1):
        name = " ".join(
            part for part in (author.get("given"), author.get("family")) if part
        )
        authors.append(
            {
                "name": name,
                "order": index,
                "position": "first" if index == 1 else "middle",
                "orcid": author.get("ORCID"),
                "affiliations": [
                    item.get("name")
                    for item in (author.get("affiliation") or [])
                    if item.get("name")
                ],
            }
        )
    return PaperRecord(
        source_key=str(source["key"]),
        source_type=str(source.get("type", "journal")),
        source_record_id=doi or normalize_title(title),
        doi=doi,
        title=title,
        normalized_title=normalize_title(title),
        publication_date=published,
        abstract=_strip_markup(raw.get("abstract")),
        original_keywords=tuple(raw.get("subject") or []),
        official_url=official_url,
        acceptance_evidence_url=official_url,
        authors=tuple(authors),
    )


def _openreview_value(content: dict, key: str, default=None):
    value = content.get(key, default)
    if isinstance(value, dict) and "value" in value:
        return value["value"]
    return value


def normalize_openreview_note(
    raw: dict,
    source: dict,
    start_date: date,
    end_date: date,
) -> PaperRecord | None:
    timestamp = raw.get("pdate") or raw.get("mdate") or raw.get("cdate")
    if not timestamp:
        return None
    published = datetime.fromtimestamp(int(timestamp) / 1000, tz=UTC).date()
    if not start_date <= published <= end_date:
        return None
    content = raw.get("content") or {}
    title = str(_openreview_value(content, "title", "") or "").strip()
    abstract = str(_openreview_value(content, "abstract", "") or "").strip() or None
    venue_id = str(_openreview_value(content, "venueid", "") or "")
    if not title or not venue_id:
        return None
    author_names = list(_openreview_value(content, "authors", []) or [])
    author_ids = list(_openreview_value(content, "authorids", []) or [])
    authors = []
    for index, name in enumerate(author_names, start=1):
        authors.append(
            {
                "name": name,
                "order": index,
                "position": "first" if index == 1 else "middle",
                "openreview_id": author_ids[index - 1]
                if index - 1 < len(author_ids)
                else None,
                "affiliations": [],
            }
        )
    note_id = str(raw.get("id") or "")
    if not note_id:
        return None
    official_url = f"https://openreview.net/forum?id={note_id}"
    return PaperRecord(
        source_key=str(source["key"]),
        source_type=str(source.get("type", "conference")),
        source_record_id=note_id,
        doi=None,
        title=title,
        normalized_title=normalize_title(title),
        publication_date=published,
        abstract=abstract,
        original_keywords=tuple(_openreview_value(content, "keywords", []) or []),
        official_url=official_url,
        acceptance_evidence_url=official_url,
        authors=tuple(authors),
    )


class OpenReviewCollector:
    NOTES_URL = "https://api2.openreview.net/notes"

    def __init__(
        self,
        *,
        http=None,
        database: Database,
        page_size: int = 1000,
        timeout: int = 60,
    ):
        self.http = http or requests.Session()
        self.database = database
        self.page_size = page_size
        self.timeout = timeout

    def _venue_ids(
        self, source: dict, start_date: date, end_date: date
    ) -> list[str]:
        if source.get("venue_id"):
            return [str(source["venue_id"])]
        template = source.get("venue_id_template")
        if not template:
            raise ValueError(f"OpenReview source lacks venue ID: {source['key']}")
        return [
            str(template).format(year=year)
            for year in range(start_date.year, end_date.year + 1)
        ]

    def collect(
        self,
        source: dict,
        start_date: date,
        end_date: date,
        *,
        limit: int | None = None,
        dry_run: bool = False,
    ) -> CollectionResult:
        start_text = start_date.isoformat()
        end_text = end_date.isoformat()
        saved = 0
        pages = 0
        try:
            for venue_id in self._venue_ids(source, start_date, end_date):
                offset = 0
                while True:
                    response = self.http.get(
                        self.NOTES_URL,
                        params={
                            "content.venueid": venue_id,
                            "limit": self.page_size,
                            "offset": offset,
                        },
                        timeout=self.timeout,
                        headers={
                            "User-Agent": "hr-candidate-discovery-screening/1.0"
                        },
                    )
                    response.raise_for_status()
                    notes = response.json().get("notes") or []
                    records = [
                        record
                        for note in notes
                        if (
                            record := normalize_openreview_note(
                                note, source, start_date, end_date
                            )
                        )
                    ]
                    if limit is not None:
                        records = records[: max(limit - saved, 0)]
                    pages += 1
                    next_offset = offset + len(notes)
                    completed = len(notes) < self.page_size
                    if dry_run:
                        saved += len(records)
                    else:
                        saved += self.database.save_page_and_checkpoint(
                            records=records,
                            source_key=source["key"],
                            start_date=start_text,
                            end_date=end_text,
                            next_cursor=(
                                None
                                if completed
                                else json.dumps(
                                    {"venue_id": venue_id, "offset": next_offset}
                                )
                            ),
                            completed=completed,
                        )
                    if completed or (limit is not None and saved >= limit):
                        break
                    offset = next_offset
                if limit is not None and saved >= limit:
                    break
        except Exception as exc:
            if not dry_run:
                self.database.mark_source_error(
                    source["key"], start_text, end_text, str(exc)
                )
            raise
        return CollectionResult(source["key"], saved, pages, True)


def _parse_citation_date(
    value: str | None, fallback_date: date | None
) -> tuple[date, str] | None:
    if value:
        cleaned = value.strip().replace("/", "-")
        parts = cleaned.split("-")
        try:
            if len(parts) >= 3:
                return date(int(parts[0]), int(parts[1]), int(parts[2])), "day"
            if len(parts) == 2:
                return date(int(parts[0]), int(parts[1]), 1), "month"
            if len(parts) == 1 and len(parts[0]) == 4:
                if fallback_date and fallback_date.year == int(parts[0]):
                    return fallback_date, "day"
                return date(int(parts[0]), 1, 1), "year"
        except ValueError:
            pass
    if fallback_date:
        return fallback_date, "day"
    return None


def normalize_citation_detail(
    html_text: str,
    source: dict,
    official_url: str,
    *,
    fallback_date: date | None = None,
) -> PaperRecord | None:
    soup = BeautifulSoup(html_text, "html.parser")

    def meta_values(name: str) -> list[str]:
        return [
            str(node.get("content")).strip()
            for node in soup.select(f'meta[name="{name}"]')
            if node.get("content")
        ]

    titles = meta_values("citation_title")
    title = titles[0] if titles else ""
    parsed_date = _parse_citation_date(
        (meta_values("citation_publication_date") or [None])[0],
        fallback_date,
    )
    if not title or parsed_date is None:
        return None
    abstract_node = (
        soup.select_one("#abstract")
        or soup.select_one("div.abstract")
        or soup.select_one("p.abstract")
    )
    abstract = (
        " ".join(abstract_node.get_text(" ", strip=True).split())
        if abstract_node
        else None
    )
    authors = tuple(
        {
            "name": name,
            "order": index,
            "position": "first" if index == 1 else "middle",
            "affiliations": [],
        }
        for index, name in enumerate(meta_values("citation_author"), start=1)
    )
    keywords = []
    for value in meta_values("citation_keywords"):
        keywords.extend(
            item.strip() for item in re.split(r"[;,]", value) if item.strip()
        )
    doi_values = meta_values("citation_doi")
    published, precision = parsed_date
    return PaperRecord(
        source_key=str(source["key"]),
        source_type=str(source.get("type", "journal")),
        source_record_id=official_url.rstrip("/").rsplit("/", 1)[-1],
        doi=normalize_doi(doi_values[0]) if doi_values else None,
        title=title,
        normalized_title=normalize_title(title),
        publication_date=published,
        publication_date_precision=precision,
        abstract=abstract,
        original_keywords=tuple(keywords),
        official_url=official_url,
        acceptance_evidence_url=official_url,
        authors=authors,
    )


def extract_official_detail_links(
    index_html: str, strategy: str, index_url: str
) -> list[str]:
    soup = BeautifulSoup(index_html, "html.parser")
    links: list[str] = []
    if strategy == "cvf":
        nodes = soup.select("dt.ptitle a[href]")
    elif strategy == "pmlr":
        nodes = [
            node
            for node in soup.select("div.paper p.links a[href]")
            if node.get_text(" ", strip=True).casefold() == "abs"
        ]
    elif strategy == "jmlr":
        nodes = [
            node
            for node in soup.select("dd a[href]")
            if node.get_text(" ", strip=True).casefold() == "abs"
        ]
    else:
        raise ValueError(f"Unknown official HTML strategy: {strategy}")
    for node in nodes:
        url = urljoin(index_url, node["href"])
        if url not in links:
            links.append(url)
    return links


class OfficialHTMLCollector:
    def __init__(
        self,
        *,
        http=None,
        database: Database,
        timeout: int = 60,
    ):
        self.http = http or requests.Session()
        self.database = database
        self.timeout = timeout

    def collect(
        self,
        source: dict,
        start_date: date,
        end_date: date,
        *,
        limit: int | None = None,
        dry_run: bool = False,
    ) -> CollectionResult:
        indexes = source.get("year_indexes") or {}
        publication_dates = source.get("publication_dates") or {}
        saved = 0
        pages = 0
        attempted = 0
        headers = {"User-Agent": "hr-candidate-discovery-screening/1.0"}
        for year in range(start_date.year, end_date.year + 1):
            index_url = indexes.get(year) or indexes.get(str(year))
            if not index_url:
                continue
            attempted += 1
            response = self.http.get(
                index_url, timeout=self.timeout, headers=headers
            )
            response.raise_for_status()
            links = extract_official_detail_links(
                response.text, source["index_strategy"], index_url
            )
            for position, link in enumerate(links):
                if limit is not None and saved >= limit:
                    break
                detail = self.http.get(link, timeout=self.timeout, headers=headers)
                detail.raise_for_status()
                fallback_value = publication_dates.get(year) or publication_dates.get(
                    str(year)
                )
                fallback = coerce_config_date(fallback_value) if fallback_value else None
                record = normalize_citation_detail(
                    detail.text, source, link, fallback_date=fallback
                )
                pages += 1
                if record is None:
                    continue
                if record.publication_date_precision == "year":
                    in_range = start_date.year <= record.publication_date.year <= end_date.year
                else:
                    in_range = start_date <= record.publication_date <= end_date
                if not in_range:
                    continue
                if dry_run:
                    saved += 1
                else:
                    saved += self.database.save_page_and_checkpoint(
                        records=[record],
                        source_key=source["key"],
                        start_date=start_date.isoformat(),
                        end_date=end_date.isoformat(),
                        next_cursor=str(position + 1),
                        completed=position == len(links) - 1,
                    )
        if attempted == 0:
            raise ValueError(
                f"No official index configured for {source['key']} in requested years"
            )
        return CollectionResult(source["key"], saved, pages, True)


def _element_text(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return "".join(element.itertext()).strip()


def _month_number(value: str | None) -> int:
    if not value:
        return 1
    lowered = value.strip().casefold()
    for month in range(1, 13):
        if lowered in {
            calendar.month_name[month].casefold(),
            calendar.month_abbr[month].casefold(),
        }:
            return month
    return 1


def normalize_acl_xml(
    xml_text: str,
    source: dict,
    start_date: date,
    end_date: date,
) -> list[PaperRecord]:
    root = ET.fromstring(xml_text)
    records: list[PaperRecord] = []
    for volume in root.findall("volume"):
        meta = volume.find("meta")
        year = int(_element_text(meta.find("year")) if meta is not None else 0)
        month = _month_number(_element_text(meta.find("month")) if meta is not None else None)
        published = date(year, month, 1)
        if not start_date <= published <= end_date:
            continue
        for paper in volume.findall("paper"):
            title = _element_text(paper.find("title"))
            abstract = _element_text(paper.find("abstract")) or None
            slug = _element_text(paper.find("url"))
            if not title or not slug:
                continue
            authors = []
            for index, author in enumerate(paper.findall("author"), start=1):
                name = " ".join(
                    part
                    for part in (
                        _element_text(author.find("first")),
                        _element_text(author.find("last")),
                    )
                    if part
                )
                authors.append(
                    {
                        "name": name,
                        "order": index,
                        "position": "first" if index == 1 else "middle",
                        "orcid": author.get("orcid"),
                        "affiliations": [
                            _element_text(item)
                            for item in author.findall("affiliation")
                            if _element_text(item)
                        ],
                    }
                )
            official_url = f"https://aclanthology.org/{slug}/"
            records.append(
                PaperRecord(
                    source_key=str(source["key"]),
                    source_type=str(source.get("type", "conference")),
                    source_record_id=slug,
                    doi=normalize_doi(_element_text(paper.find("doi")) or None),
                    title=title,
                    normalized_title=normalize_title(title),
                    publication_date=published,
                    publication_date_precision="month",
                    abstract=abstract,
                    original_keywords=tuple(
                        item.strip()
                        for item in _element_text(paper.find("keywords")).split(",")
                        if item.strip()
                    ),
                    official_url=official_url,
                    acceptance_evidence_url=official_url,
                    authors=tuple(authors),
                )
            )
    return records


class ACLXMLCollector:
    def __init__(
        self,
        *,
        http=None,
        database: Database,
        timeout: int = 60,
    ):
        self.http = http or requests.Session()
        self.database = database
        self.timeout = timeout

    def collect(
        self,
        source: dict,
        start_date: date,
        end_date: date,
        *,
        limit: int | None = None,
        dry_run: bool = False,
    ) -> CollectionResult:
        collections = source.get("xml_collections") or {}
        records: list[PaperRecord] = []
        pages = 0
        for year in range(start_date.year, end_date.year + 1):
            urls = collections.get(year) or collections.get(str(year)) or []
            for url in urls:
                response = self.http.get(
                    url,
                    timeout=self.timeout,
                    headers={"User-Agent": "hr-candidate-discovery-screening/1.0"},
                )
                response.raise_for_status()
                records.extend(
                    normalize_acl_xml(response.text, source, start_date, end_date)
                )
                pages += 1
        records = deduplicate_works(records)
        if limit is not None:
            records = records[:limit]
        if not pages:
            raise ValueError(
                f"No ACL XML collection configured for requested years"
            )
        if dry_run:
            saved = len(records)
        else:
            saved = self.database.save_page_and_checkpoint(
                records=records,
                source_key=source["key"],
                start_date=start_date.isoformat(),
                end_date=end_date.isoformat(),
                next_cursor=None,
                completed=True,
            )
        return CollectionResult(source["key"], saved, pages, True)


class CrossrefCollector:
    def __init__(
        self,
        *,
        http=None,
        database: Database,
        mailto: str | None = None,
        rows: int = 100,
        timeout: int = 60,
    ):
        self.http = http or requests.Session()
        self.database = database
        self.mailto = mailto
        self.rows = rows
        self.timeout = timeout

    def collect(
        self,
        source: dict,
        start_date: date,
        end_date: date,
        *,
        limit: int | None = None,
        dry_run: bool = False,
    ) -> CollectionResult:
        start_text = start_date.isoformat()
        end_text = end_date.isoformat()
        cursor = (
            self.database.get_source_checkpoint(source["key"], start_text, end_text)
            or "*"
        )
        saved = 0
        pages = 0
        issns = source.get("issns") or []
        if issns:
            url = f"https://api.crossref.org/journals/{issns[0]}/works"
        else:
            url = "https://api.crossref.org/works"
        try:
            while cursor:
                params = {
                    "filter": f"from-pub-date:{start_text},until-pub-date:{end_text}",
                    "rows": self.rows,
                    "cursor": cursor,
                    "select": (
                        "DOI,title,abstract,published-online,published-print,"
                        "issued,URL,author,subject,update-to"
                    ),
                }
                if self.mailto:
                    params["mailto"] = self.mailto
                if source.get("crossref_query"):
                    params["query.container-title"] = source["crossref_query"]
                response = self.http.get(
                    url,
                    params=params,
                    timeout=self.timeout,
                    headers={"User-Agent": "hr-candidate-discovery-screening/1.0"},
                )
                response.raise_for_status()
                message = response.json().get("message", {})
                items = message.get("items") or []
                records = [
                    record
                    for item in items
                    if (record := normalize_crossref_item(item, source))
                    and start_date <= record.publication_date <= end_date
                ]
                records = deduplicate_works(records)
                if limit is not None:
                    records = records[: max(limit - saved, 0)]
                next_cursor = message.get("next-cursor") or None
                if not items or next_cursor == cursor:
                    next_cursor = None
                pages += 1
                if dry_run:
                    saved += len(records)
                else:
                    saved += self.database.save_page_and_checkpoint(
                        records=records,
                        source_key=source["key"],
                        start_date=start_text,
                        end_date=end_text,
                        next_cursor=next_cursor,
                        completed=not next_cursor or (limit is not None and saved >= limit),
                    )
                if not next_cursor or (limit is not None and saved >= limit):
                    return CollectionResult(source["key"], saved, pages, True)
                cursor = next_cursor
        except Exception as exc:
            if not dry_run:
                self.database.mark_source_error(
                    source["key"], start_text, end_text, str(exc)
                )
            raise
        return CollectionResult(source["key"], saved, pages, True)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Collect accepted publication metadata.")
    parser.add_argument("--source", required=True)
    parser.add_argument("--start-date", required=True)
    parser.add_argument("--end-date", required=True)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--settings-config",
        default=str(Path(__file__).resolve().parents[1] / "config" / "settings.yaml"),
    )
    parser.add_argument(
        "--sources-config",
        default=str(Path(__file__).resolve().parents[1] / "config" / "sources.yaml"),
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    start, end = parse_date_range(args.start_date, args.end_date)
    settings = load_settings(args.settings_config)
    configured = load_sources(args.sources_config)
    sources = configured["conferences"] + configured["journals"]
    source = next((item for item in sources if item["key"] == args.source), None)
    if source is None:
        raise ValueError(f"Unknown source: {args.source}")
    database = Database(settings.database_path)
    database.initialize()
    mailto = os.getenv("OPENALEX_MAILTO")
    if source["collector"] == "openalex":
        collector = OpenAlexCollector(
            database=database,
            mailto=mailto,
            per_page=100,
            timeout=settings.timeout_seconds,
        )
    elif source["collector"] == "openreview":
        collector = OpenReviewCollector(
            database=database,
            page_size=1000,
            timeout=settings.timeout_seconds,
        )
    elif source["collector"] == "official_html":
        collector = OfficialHTMLCollector(
            database=database,
            timeout=settings.timeout_seconds,
        )
    elif source["collector"] == "acl_xml":
        collector = ACLXMLCollector(
            database=database,
            timeout=settings.timeout_seconds,
        )
    else:
        collector = CrossrefCollector(
            database=database,
            mailto=mailto,
            rows=100,
            timeout=settings.timeout_seconds,
        )
    result = collector.collect(
        source,
        start,
        end,
        limit=args.limit,
        dry_run=args.dry_run,
    )
    print(json.dumps(result.__dict__, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
