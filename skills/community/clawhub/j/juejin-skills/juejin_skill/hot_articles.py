"""Hot articles ranking and category browsing for Juejin."""

from __future__ import annotations

from typing import Any

from juejin_skill.api import JuejinAPI
from juejin_skill.config import (
    CATEGORY_BRIEFS_URL,
    CATEGORY_TAGS_URL,
    RECOMMEND_ALL_FEED_URL,
    RECOMMEND_CATE_FEED_URL,
    DEFAULT_PAGE_SIZE,
    SORT_TYPE_HOT,
)
from juejin_skill.utils import format_number, timestamp_to_str, truncate_text


class HotArticles:
    """Query Juejin categories and trending / hot articles.

    All methods are synchronous and return plain Python dicts / lists.
    """

    def __init__(self, cookie: str = "") -> None:
        self._api = JuejinAPI(cookie=cookie)

    # ------------------------------------------------------------------ #
    #  Categories
    # ------------------------------------------------------------------ #

    def get_categories(self) -> list[dict[str, Any]]:
        """Return a list of all article categories.

        Each item contains at least ``category_id``, ``category_name``,
        and ``category_url``.
        """
        resp = self._api.get(CATEGORY_BRIEFS_URL)
        categories = resp.get("data", [])
        return [
            {
                "category_id": cat.get("category_id", ""),
                "category_name": cat.get("category_name", ""),
                "category_url": cat.get("category_url", ""),
                "rank": cat.get("rank", 0),
            }
            for cat in categories
        ]

    def get_category_tags(
        self,
        category_id: str,
        cursor: str = "0",
        limit: int = DEFAULT_PAGE_SIZE,
    ) -> list[dict[str, Any]]:
        """Return popular tags under a given category.

        Parameters
        ----------
        category_id : str
            The category to query (e.g. ``"6809637767543259144"`` for frontend).
        cursor : str
            Pagination cursor.
        limit : int
            Number of tags to fetch per page.
        """
        body = {
            "cate_id": category_id,
            "cursor": cursor,
            "limit": limit,
        }
        resp = self._api.post(CATEGORY_TAGS_URL, json_body=body)
        tags = resp.get("data", [])
        return [
            {
                "tag_id": t.get("tag_id", ""),
                "tag_name": t.get("tag_name", ""),
                "concern_num": t.get("concern_num", 0),
                "post_article_count": t.get("post_article_count", 0),
            }
            for t in tags
        ]

    # ------------------------------------------------------------------ #
    #  Hot / recommended articles
    # ------------------------------------------------------------------ #

    def get_hot_articles(
        self,
        category_id: str = "",
        sort_type: int = SORT_TYPE_HOT,
        cursor: str = "0",
        limit: int = DEFAULT_PAGE_SIZE,
    ) -> list[dict[str, Any]]:
        """Fetch hot / recommended articles.

        Parameters
        ----------
        category_id : str
            If empty, fetch from all categories (recommend_all_feed).
            Otherwise fetch from the specified category (recommend_cate_feed).
        sort_type : int
            Sorting strategy (see ``config.py`` for constants).
        cursor : str
            Pagination cursor.
        limit : int
            Number of articles per page.

        Returns
        -------
        list[dict]
            A list of simplified article dicts.
        """
        if category_id:
            url = RECOMMEND_CATE_FEED_URL
            body: dict[str, Any] = {
                "cate_id": category_id,
                "sort_type": sort_type,
                "cursor": cursor,
                "limit": limit,
            }
        else:
            url = RECOMMEND_ALL_FEED_URL
            body = {
                "sort_type": sort_type,
                "cursor": cursor,
                "limit": limit,
                "id_type": 2,
                "client_type": 2608,
            }

        resp = self._api.post(url, json_body=body)
        raw_articles = resp.get("data", [])
        results = []
        for item in raw_articles:
            # The API may wrap data in item_info (recommend_all_feed)
            actual = item.get("item_info", item) if item.get("item_type") else item
            if actual.get("article_info"):
                results.append(self._simplify_article(actual))
        return results

    # ------------------------------------------------------------------ #
    #  Formatting helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def _simplify_article(item: dict[str, Any]) -> dict[str, Any]:
        """Flatten a raw feed item into a simplified dict."""
        info = item.get("article_info", {})
        author = item.get("author_user_info", {})
        tags = item.get("tags", [])

        article_id = info.get("article_id", "")
        return {
            "article_id": article_id,
            "title": info.get("title", ""),
            "url": f"https://juejin.cn/post/{article_id}",
            "author": author.get("user_name", ""),
            "author_id": author.get("user_id", ""),
            "view_count": info.get("view_count", 0),
            "digg_count": info.get("digg_count", 0),
            "comment_count": info.get("comment_count", 0),
            "collect_count": info.get("collect_count", 0),
            "brief_content": truncate_text(info.get("brief_content", ""), 120),
            "cover_image": info.get("cover_image", ""),
            "ctime": timestamp_to_str(info.get("ctime", "0")),
            "tags": [t.get("tag_name", "") for t in tags],
            "category_name": info.get("category", {}).get("category_name", "")
            if isinstance(info.get("category"), dict)
            else "",
        }

    @staticmethod
    def format_ranking(articles: list[dict[str, Any]], top_n: int = 20) -> str:
        """Return a human-readable ranking text.

        Parameters
        ----------
        articles : list[dict]
            Article list returned by :meth:`get_hot_articles`.
        top_n : int
            How many articles to include.

        Returns
        -------
        str
            Formatted ranking text (Markdown table).
        """
        lines: list[str] = [
            "| # | Title | Author | Views | Likes | Comments |",
            "|---|-------|--------|-------|-------|----------|",
        ]
        for idx, art in enumerate(articles[:top_n], 1):
            title = truncate_text(art["title"], 50)
            link = f"[{title}]({art['url']})"
            lines.append(
                f"| {idx} | {link} | {art['author']} "
                f"| {format_number(art['view_count'])} "
                f"| {format_number(art['digg_count'])} "
                f"| {format_number(art['comment_count'])} |"
            )
        return "\n".join(lines)
