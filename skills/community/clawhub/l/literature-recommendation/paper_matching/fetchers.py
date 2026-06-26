"""Paper source fetchers."""

from __future__ import annotations

import html
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Iterable
from urllib.parse import quote_plus

import requests

from .models import Paper


ARXIV_API = "https://export.arxiv.org/api/query"


def _clean_text(value: str) -> str:
    value = re.sub(r"\s+", " ", value or "")
    return html.unescape(value).strip()


def _parse_arxiv_time(value: str) -> str:
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        dt = datetime.now(timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()


@dataclass
class ArxivFetcher:
    timeout: int = 20

    def search(self, query: str, max_results: int = 20) -> list[Paper]:
        params = {
            "search_query": query,
            "start": 0,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
        }
        response = requests.get(ARXIV_API, params=params, timeout=self.timeout)
        response.raise_for_status()
        return self._parse_feed(response.text)

    def _parse_feed(self, xml_text: str) -> list[Paper]:
        root = ET.fromstring(xml_text)
        ns = {
            "atom": "http://www.w3.org/2005/Atom",
            "arxiv": "http://arxiv.org/schemas/atom",
        }
        papers: list[Paper] = []
        for entry in root.findall("atom:entry", ns):
            paper_id = (entry.findtext("atom:id", default="", namespaces=ns) or "").split("/")[-1]
            title = _clean_text(entry.findtext("atom:title", default="", namespaces=ns))
            summary = _clean_text(entry.findtext("atom:summary", default="", namespaces=ns))
            published = _parse_arxiv_time(entry.findtext("atom:published", default="", namespaces=ns))
            links = entry.findall("atom:link", ns)
            url = ""
            for link in links:
                if link.attrib.get("rel") == "alternate":
                    url = link.attrib.get("href", "")
                    break
            if not url and paper_id:
                url = f"https://arxiv.org/abs/{paper_id}"
            authors = [
                _clean_text(author.findtext("atom:name", default="", namespaces=ns))
                for author in entry.findall("atom:author", ns)
            ]
            tags = [
                tag.attrib.get("term", "")
                for tag in entry.findall("atom:category", ns)
                if tag.attrib.get("term")
            ]
            papers.append(
                Paper(
                    paper_id=paper_id or url,
                    title=title,
                    abstract=summary,
                    authors=[author for author in authors if author],
                    published_at=published,
                    source="arxiv",
                    url=url,
                    tags=tags,
                    raw={"entry_id": paper_id, "source": "arxiv"},
                )
            )
        return papers

    def fetch_for_keywords(self, keywords: Iterable[str], max_results: int = 20) -> list[Paper]:
        terms = [term.strip() for term in keywords if term and term.strip()]
        if not terms:
            return []
        query = " OR ".join(f'all:"{term}"' for term in terms[:6])
        return self.search(query, max_results=max_results)
