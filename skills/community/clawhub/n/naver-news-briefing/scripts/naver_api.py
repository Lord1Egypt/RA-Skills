from __future__ import annotations

import html
import json
import re
import urllib.parse
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, Dict, List, Protocol

import requests

RE_BOLD_TAGS = re.compile(r"</?b>")
API_URL = "https://openapi.naver.com/v1/search/news.json"


class ResponseLike(Protocol):
    status_code: int
    text: str

    def json(self) -> Dict[str, Any]: ...


class SessionLike(Protocol):
    def get(self, url: str, *, headers: Dict[str, str], params: Dict[str, Any], timeout: int) -> ResponseLike: ...


@dataclass
class NewsItem:
    title: str
    description: str
    link: str
    original_link: str
    publisher: str
    pub_date: str
    pub_date_iso: str | None

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__.copy()


def parse_pub_date(value: str) -> str | None:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        dt = parsedate_to_datetime(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone().isoformat(timespec="seconds")
    except Exception:
        return None


def clean_item(item: Dict[str, Any]) -> NewsItem:
    title = html.unescape(RE_BOLD_TAGS.sub("", str(item.get("title", ""))))
    desc = html.unescape(RE_BOLD_TAGS.sub("", str(item.get("description", ""))))
    naver_link = str(item.get("link", "") or "")
    original_link = str(item.get("originallink", "") or "")
    if "news.naver.com" in naver_link:
        final_link = naver_link
    elif "news.naver.com" in original_link:
        final_link = original_link
    else:
        final_link = naver_link or original_link

    publisher = "정보 없음"
    if original_link:
        publisher = urllib.parse.urlparse(original_link).netloc.replace("www.", "") or publisher
    elif final_link:
        publisher = "네이버뉴스" if "news.naver.com" in final_link else urllib.parse.urlparse(final_link).netloc.replace("www.", "")
    return NewsItem(
        title=title,
        description=desc,
        link=final_link,
        original_link=original_link,
        publisher=publisher or "정보 없음",
        pub_date=str(item.get("pubDate", "") or ""),
        pub_date_iso=parse_pub_date(str(item.get("pubDate", "") or "")),
    )


def fetch_news(
    *,
    client_id: str,
    client_secret: str,
    search_query: str,
    exclude_words: List[str],
    limit: int = 10,
    days: int | None = None,
    timeout: int = 15,
    session: SessionLike | None = None,
) -> Dict[str, Any]:
    if not search_query.strip():
        raise ValueError("검색어가 비어 있습니다.")
    if not client_id.strip() or not client_secret.strip():
        raise ValueError("네이버 API 자격증명이 설정되지 않았습니다.")

    active_session = session or requests.Session()
    resp = active_session.get(
        API_URL,
        headers={
            "X-Naver-Client-Id": client_id.strip(),
            "X-Naver-Client-Secret": client_secret.strip(),
        },
        params={"query": search_query, "display": min(max(limit, 10), 100), "start": 1, "sort": "date"},
        timeout=timeout,
    )
    if resp.status_code != 200:
        try:
            payload = resp.json()
            msg = f"API 오류 {resp.status_code} ({payload.get('errorCode', '')}): {payload.get('errorMessage', '알 수 없는 오류')}"
        except Exception:
            msg = f"API 오류 {resp.status_code}: {getattr(resp, 'text', '')[:200]}"
        raise RuntimeError(msg)

    data = resp.json()
    exclude_words_lc = [w.lower() for w in exclude_words if w]
    cutoff = None
    if days:
        cutoff = datetime.now().astimezone().timestamp() - (days * 86400)

    items: List[NewsItem] = []
    filtered_out = 0
    too_old = 0
    for raw in data.get("items", []):
        item = clean_item(raw)
        text_blob = f"{item.title}\n{item.description}".lower()
        if exclude_words_lc and any(ex in text_blob for ex in exclude_words_lc):
            filtered_out += 1
            continue
        if cutoff is not None and item.pub_date_iso:
            try:
                if datetime.fromisoformat(item.pub_date_iso).timestamp() < cutoff:
                    too_old += 1
                    continue
            except Exception:
                pass
        items.append(item)
        if len(items) >= limit:
            break

    return {
        "query": search_query,
        "exclude_words": exclude_words,
        "days": days,
        "total": int(data.get("total", 0) or 0),
        "displayed": len(items),
        "filtered_out": filtered_out,
        "too_old": too_old,
        "items": [item.to_dict() for item in items],
        "raw_meta": {"lastBuildDate": data.get("lastBuildDate", "")},
    }
