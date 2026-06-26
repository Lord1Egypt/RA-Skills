"""GitHub Trending source — scrapes the trending page."""

from __future__ import annotations

import re

import requests
from bs4 import BeautifulSoup

from src.models import BaseSource, FeedItem
from src.sources import register


@register("github_trending")
class GitHubTrendingSource(BaseSource):

    BASE_URL = "https://github.com/trending"
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
    }

    def fetch(self) -> list[FeedItem]:
        since = self.config.get("since", "daily")
        language = self.config.get("language", "")  # e.g. "python"

        params: dict[str, str] = {"since": since}
        if language:
            params["spoken_language_code"] = ""
            # GitHub uses the URL path for language filter
            url = f"{self.BASE_URL}/{language}"
        else:
            url = self.BASE_URL

        resp = requests.get(url, params={"since": since}, headers=self.HEADERS, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        items: list[FeedItem] = []
        for article in soup.select("article.Box-row"):
            # Repo name
            h2_a = article.select_one("h2.h3 a")
            if not h2_a:
                continue
            full_name = h2_a["href"].strip("/")  # "owner/repo"

            # Description
            desc_tag = article.select_one("p.color-fg-muted")
            description = desc_tag.get_text(strip=True) if desc_tag else ""

            # Language
            lang_tag = article.select_one("span[itemprop='programmingLanguage']")
            language_name = lang_tag.get_text(strip=True) if lang_tag else ""

            # Total stars
            star_link = article.select_one('a[href$="/stargazers"]')
            total_stars = _parse_int(star_link.get_text(strip=True)) if star_link else 0

            # Total forks
            fork_link = article.select_one('a[href$="/forks"]')
            total_forks = _parse_int(fork_link.get_text(strip=True)) if fork_link else 0

            # Stars today
            stars_today_tag = article.select_one("span.d-inline-block.float-sm-right")
            stars_today = 0
            if stars_today_tag:
                m = re.search(r"([\d,]+)\s+stars", stars_today_tag.get_text())
                if m:
                    stars_today = _parse_int(m.group(1))

            items.append(
                FeedItem(
                    source=f"github:{self.name}",
                    title=full_name,
                    url=f"https://github.com/{full_name}",
                    author=full_name.split("/")[0],
                    content=description,
                    timestamp="",  # GitHub trending has no per-repo timestamp
                    tags=self.config.get("tags", []) + ([language_name] if language_name else []),
                    metrics={
                        "stars_today": stars_today,
                        "total_stars": total_stars,
                        "total_forks": total_forks,
                    },
                    extra={"language": language_name},
                )
            )

        return items


def _parse_int(s: str) -> int:
    return int(s.replace(",", "").strip()) if s.strip() else 0
