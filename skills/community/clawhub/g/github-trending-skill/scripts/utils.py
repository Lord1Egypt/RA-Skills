import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

import requests
from bs4 import BeautifulSoup

DEFAULT_HEADERS = {
    "User-Agent": "github-trending-skill/1.0 (+https://github.com)"
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_star_count(text: str) -> int:
    if not text:
        return 0
    cleaned = text.strip().lower().replace(",", "")
    match = re.search(r"(\d+(?:\.\d+)?)([km]?)", cleaned)
    if not match:
        return 0
    value = float(match.group(1))
    suffix = match.group(2)
    if suffix == "k":
        value *= 1000
    elif suffix == "m":
        value *= 1000000
    return int(value)


def fetch_html(url: str, timeout: int = 20) -> str:
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    response.raise_for_status()
    return response.text


def parse_trending(html: str) -> List[Dict[str, object]]:
    soup = BeautifulSoup(html, "html.parser")
    items = []
    for article in soup.select("article.Box-row"):
        name = ""
        link = article.select_one("h2 a")
        if link and link.get("href"):
            name = link["href"].strip("/")
        description = ""
        desc_el = article.select_one("p")
        if desc_el:
            description = " ".join(desc_el.get_text(" ", strip=True).split())
        language = ""
        lang_el = article.select_one("[itemprop=programmingLanguage]")
        if lang_el:
            language = lang_el.get_text(strip=True)
        stars_total = 0
        for star_link in article.select("a[href*='stargazers']"):
            stars_total = parse_star_count(star_link.get_text(strip=True))
            if stars_total:
                break
        stars_period = 0
        period_span = None
        for span in article.select("span"):
            text = span.get_text(" ", strip=True).lower()
            if "stars today" in text or "stars this month" in text:
                period_span = span
                break
        if period_span:
            stars_period = parse_star_count(period_span.get_text(strip=True))
        items.append(
            {
                "name": name,
                "description": description,
                "language": language,
                "stars_total": stars_total,
                "stars_period": stars_period,
            }
        )
    return items


def load_cache(path: Path) -> Optional[Dict[str, object]]:
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def save_cache(path: Path, data: Dict[str, object]) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def sleep_if_needed(seconds: int) -> None:
    if seconds > 0:
        time.sleep(seconds)

