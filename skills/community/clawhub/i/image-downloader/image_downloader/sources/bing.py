import html
import json
import re
from urllib.parse import quote

import requests

from image_downloader.models import ImageCandidate
from image_downloader.sources.base import BaseSource


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
}


def _extract_image_metadata(html_text):
    patterns = [
        r"m='(\{.*?\})'",
        r'm="(\{.*?\})"',
    ]

    seen = set()
    items = []

    for pattern in patterns:
        matches = re.findall(pattern, html_text)
        for raw in matches:
            try:
                data = json.loads(html.unescape(raw))
            except json.JSONDecodeError:
                continue

            image_url = data.get("murl")
            if image_url and image_url not in seen:
                seen.add(image_url)
                items.append(data)

    return items


def extract_image_urls(html_text):
    return [item["murl"] for item in _extract_image_metadata(html_text) if item.get("murl")]


class BingSource(BaseSource):
    name = "bing"

    def collect(self, keyword, limit, pages):
        candidates = []
        seen = set()
        max_pages = max(1, pages)

        for page in range(max_pages):
            if limit is not None and len(candidates) >= limit:
                break

            first = page * 35 + 1
            url = f"https://www.bing.com/images/search?q={quote(keyword)}&form=HDRSC3&first={first}"
            response = requests.get(url=url, headers=HEADERS, timeout=15)
            response.raise_for_status()

            for data in _extract_image_metadata(response.text):
                image_url = data.get("murl")
                if not image_url or image_url in seen:
                    continue

                seen.add(image_url)
                candidates.append(
                    ImageCandidate(
                        source="bing",
                        keyword=keyword,
                        image_url=image_url,
                        page_url=data.get("purl"),
                        thumbnail_url=data.get("turl"),
                        title=data.get("t"),
                        width=data.get("w"),
                        height=data.get("h"),
                        content_type=None,
                        source_rank=len(candidates) + 1,
                        metadata={"bing_page": page + 1},
                    )
                )

                if limit is not None and len(candidates) >= limit:
                    break

        return candidates
