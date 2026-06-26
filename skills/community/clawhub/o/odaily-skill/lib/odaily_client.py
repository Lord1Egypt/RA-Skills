"""
Odaily 星球日报数据获取 — 基于 Web API

快讯: https://web-api.odaily.news/newsflash/page
文章: https://web-api.odaily.news/post/page
"""

from __future__ import annotations

import re
from datetime import datetime, timezone, timedelta

import requests

from config.settings import settings

BJT = timezone(timedelta(hours=8))

FLASH_API = "https://web-api.odaily.news/newsflash/page"
POST_API = "https://web-api.odaily.news/post/page"


class OdailyClient:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": settings.USER_AGENT,
            "Accept": "application/json",
            "Referer": "https://www.odaily.news/",
        })

    # ── 快讯 ──────────────────────────────────────────────

    def get_flash_news(self, limit: int = 20) -> list[dict]:
        """从 Web API 获取最新快讯"""
        out = []
        page = 1
        while len(out) < limit:
            try:
                resp = self.session.get(
                    FLASH_API,
                    params={"page": page, "size": min(limit, 20), "groupId": 0, "isImport": "false"},
                    timeout=settings.REQUEST_TIMEOUT,
                )
                resp.raise_for_status()
                items = self._extract_list(resp.json())
                if not items:
                    break
                for it in items:
                    news_id = it.get("id", "")
                    out.append({
                        "title": it.get("title", ""),
                        "description": self._clean_text(it.get("description") or it.get("content") or ""),
                        "url": f"https://www.odaily.news/zh-CN/newsflash/{news_id}" if news_id else "",
                        "published_at": self._fmt_ts(it.get("publishTimestamp") or it.get("published_at") or it.get("created_at")),
                        "pub_ts": self._raw_ts(it.get("publishTimestamp") or it.get("published_at") or it.get("created_at")),
                        "news_type": "flash",
                    })
                    if len(out) >= limit:
                        break
                page += 1
            except Exception:
                break
        return out

    # ── 文章 ──────────────────────────────────────────────

    def get_hot_articles(self, limit: int = 10, category: str = "all") -> list[dict]:
        """从 Web API 获取最新文章"""
        out = []
        try:
            resp = self.session.get(
                POST_API,
                params={"page": 1, "size": limit},
                timeout=settings.REQUEST_TIMEOUT,
            )
            resp.raise_for_status()
            items = self._extract_list(resp.json())
            for it in items[:limit]:
                post_id = it.get("id", "")
                summary = it.get("summary") or it.get("description") or ""
                out.append({
                    "title": it.get("title") or it.get("name") or "",
                    "summary": self._clean_text(summary),
                    "url": it.get("url") or it.get("link") or (
                        f"https://www.odaily.news/post/{post_id}" if post_id else ""
                    ),
                    "published_at": self._fmt_ts(it.get("publishTimestamp") or it.get("published_at") or it.get("created_at")),
                    "pub_ts": self._raw_ts(it.get("publishTimestamp") or it.get("published_at") or it.get("created_at")),
                    "author": it.get("author") or "",
                    "news_type": "article",
                })
        except Exception:
            pass
        return out

    # ── 行情播报 ──────────────────────────────────────────

    def get_market_news(self, limit: int = 5) -> list[dict]:
        """从 Odaily newsflash API 获取最新行情播报（groupId=1）"""
        out = []
        try:
            resp = self.session.get(
                FLASH_API,
                params={"page": 1, "size": 10, "groupId": 1, "isImport": "false"},
                timeout=settings.REQUEST_TIMEOUT,
            )
            resp.raise_for_status()
            items = self._extract_list(resp.json())
            for it in items[:limit]:
                news_id = it.get("id", "")
                out.append({
                    "title": it.get("title", ""),
                    "description": self._clean_text(it.get("description") or it.get("content") or ""),
                    "url": f"https://www.odaily.news/zh-CN/newsflash/{news_id}" if news_id else "",
                    "published_at": self._fmt_ts(it.get("publishTimestamp") or it.get("published_at") or it.get("created_at")),
                    "pub_ts": self._raw_ts(it.get("publishTimestamp") or it.get("published_at") or it.get("created_at")),
                })
        except Exception:
            pass
        return out

    # ── Polymarket 预测市场快讯 ───────────────────────────

    def get_polymarket_news(self, limit: int = 5) -> list[dict]:
        """从 Odaily newsflash API 获取含"先知频道"的预测市场快讯"""
        out = []
        for page in range(1, 5):
            if len(out) >= limit:
                break
            try:
                resp = self.session.get(
                    FLASH_API,
                    params={"page": page, "size": 20},
                    timeout=settings.REQUEST_TIMEOUT,
                )
                resp.raise_for_status()
                items = self._extract_list(resp.json())
                if not items:
                    break
                for it in items:
                    raw_desc = it.get("description", "")
                    if "先知频道" not in raw_desc:
                        continue
                    news_id = it.get("id", "")
                    ts = self._raw_ts(it.get("publishTimestamp") or it.get("published_at") or it.get("created_at"))
                    out.append({
                        "title": it.get("title", ""),
                        "description": self._clean_text(raw_desc),
                        "url": f"https://www.odaily.news/zh-CN/newsflash/{news_id}" if news_id else "",
                        "published_at": self._fmt_ts(it.get("publishTimestamp") or it.get("published_at") or it.get("created_at")),
                        "pub_ts": ts,
                    })
                    if len(out) >= limit:
                        break
            except Exception:
                break
        return out

    # ── 工具 ──────────────────────────────────────────────

    @staticmethod
    def _extract_list(data: dict) -> list:
        """从 API 响应中提取列表"""
        payload = data.get("data", {})
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict):
            return payload.get("list") or payload.get("items") or payload.get("data") or []
        return []

    @staticmethod
    def _raw_ts(val) -> float:
        """统一转为秒级时间戳"""
        if not val:
            return 0.0
        try:
            t = int(val)
            return t / 1000 if t > 1e10 else float(t)
        except Exception:
            return 0.0

    @classmethod
    def _fmt_ts(cls, val) -> str:
        """时间戳 → 北京时间字符串"""
        ts = cls._raw_ts(val)
        if not ts:
            return ""
        return datetime.fromtimestamp(ts, tz=BJT).strftime("%m-%d %H:%M")

    @staticmethod
    def _clean_text(text: str) -> str:
        if not text:
            return ""
        text = re.sub(r"<[^>]+>", " ", text)
        return re.sub(r"\s+", " ", text).strip()
