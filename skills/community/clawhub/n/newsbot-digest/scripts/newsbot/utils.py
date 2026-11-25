"""Общие утилиты: JSON из ответа LLM, очистка текста, поиск по Google News, ретраи LLM."""
from __future__ import annotations

import asyncio
import json
import random
import re
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, Callable, Literal, Optional

import emoji
import requests
from bs4 import BeautifulSoup
from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger

from .config import get_llm

MONTHS_RU = {1: "января", 2: "февраля", 3: "марта", 4: "апреля", 5: "мая", 6: "июня",
             7: "июля", 8: "августа", 9: "сентября", 10: "октября", 11: "ноября", 12: "декабря"}

HTTP_HEADERS = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                              "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"}


def get_date_ru(now: Optional[datetime] = None) -> str:
    now = now or datetime.now()
    return f"{now.day} {MONTHS_RU[now.month]} {now.year}"


def clean_text_simple(text) -> str:
    if not isinstance(text, str):
        text = str(text)
    text = re.sub(r"https?://\S+", "", text)
    text = re.sub(r"\.{3,}", "", text)
    text = emoji.replace_emoji(text, "")
    return re.sub(r"\s+", " ", text).strip()


def extract_json_from_string(text: str):
    """Достаёт первый JSON-объект/массив из произвольного текста ответа модели."""
    if not isinstance(text, str):
        text = str(text)
    for open_ch, close_ch in (("{", "}"), ("[", "]")):
        start = text.find(open_ch)
        if start == -1:
            continue
        depth = 0
        for i in range(start, len(text)):
            if text[i] == open_ch:
                depth += 1
            elif text[i] == close_ch:
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start:i + 1])
                    except json.JSONDecodeError:
                        break
    m = re.search(r"(\{(?:[^{}]|(?:\{[^{}]*\}))*\})", text)
    if m:
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            pass
    return None


def first_list_from_json(text: str) -> list:
    """Ответ агентов вида {"top": [..]} -> список id (int)."""
    data = extract_json_from_string(text)
    if isinstance(data, dict) and data:
        data = data[list(data.keys())[0]]
    if not isinstance(data, list):
        raise ValueError(f"В ответе модели нет списка id: {str(text)[:300]}")
    return [int(x) for x in data]


def parse_rss_date(s: str) -> Optional[datetime]:
    try:
        dt = parsedate_to_datetime(s)
        return dt if dt.tzinfo else dt.replace(tzinfo=timezone.utc)
    except Exception:
        return None


def decode_google_url(url: str) -> str:
    """news.google.com/rss/articles/... -> реальный URL издания."""
    if "news.google.com" not in url:
        return url
    try:
        from googlenewsdecoder import gnewsdecoder
        res = gnewsdecoder(url, interval=None, proxy=None)
        if res and res.get("status") and res.get("decoded_url"):
            return res["decoded_url"]
    except Exception as e:
        logger.debug(f"gnewsdecoder: {e}")
    return url


def web_search(query: str, geo: Literal["RU", "US"] = "US") -> str:
    """Инструмент для поиска в интернете. Возвращает первые 10 новостей из news.google.com.
    Для начала поиска нужно задать запрос и в каком регионе искать (RU или US)"""
    logger.debug(f"web_search | query: {query} | geo: {geo}")
    results = []
    year = datetime.now().year
    try:
        r = requests.get("https://news.google.com/rss/search",
                         params={"q": query, "gl": geo}, headers=HTTP_HEADERS, timeout=30)
        if r.status_code != 200:
            return json.dumps({"response": f"status_code: {r.status_code}"})
        for item in BeautifulSoup(r.text, "xml").find_all("item")[:10]:
            dt = parse_rss_date(item.find("pubDate").text) if item.find("pubDate") else None
            if dt and dt.year != year:
                continue
            results.append({
                "title": item.find("title").text,
                "url": decode_google_url(item.find("link").text),
                "date": item.find("pubDate").text if item.find("pubDate") else "",
                "source": item.find("source").text if item.find("source") else "",
            })
        return json.dumps(results, ensure_ascii=False, indent=2)
    except Exception as e:
        return json.dumps({"response": f"error: {e}"}, ensure_ascii=False)


# ---------------- ретраи LLM ----------------
def _is_rate_limit(e: Exception) -> bool:
    s = str(e)
    return "429" in s or "TooManyRequests" in s or "rate limit" in s.lower()


def llm_call(system_prompt: str, user_text: str, max_retries: int = 5, switch_at: int = 3) -> str:
    """Один вызов модели с ретраями: cloud -> (с попытки switch_at) deepseek."""
    llm = get_llm("cloud")
    last = None
    for attempt in range(max_retries):
        if attempt == switch_at:
            logger.info("Переключение на DeepSeek")
            llm = get_llm("deepseek")
        try:
            resp = llm.invoke([SystemMessage(content=system_prompt), HumanMessage(content=user_text)])
            return resp.content
        except Exception as e:
            last = e
            logger.warning(f"LLM попытка {attempt + 1}/{max_retries}: {e}")
            if _is_rate_limit(e):
                import time
                time.sleep(min(60 * (2 ** attempt), 300) + random.uniform(0, 1))
    raise RuntimeError(f"LLM недоступна после {max_retries} попыток: {last}")


async def run_agent(name: str, system_prompt: str, tools: list, user_msg: str,
                    middleware_factory: Callable[[], list], max_retries: int = 5,
                    switch_at: int = 3) -> list[int]:
    """Запуск LangChain-агента с инструментами; ожидается JSON вида {"top": [id, ...]}."""
    from langchain.agents import create_agent

    llm = get_llm("cloud")
    for attempt in range(max_retries):
        if attempt == switch_at:
            logger.info(f"{name}: переключение на DeepSeek")
            llm = get_llm("deepseek")
        try:
            agent = create_agent(model=llm, tools=tools, system_prompt=system_prompt,
                                 middleware=middleware_factory())
            result = await agent.ainvoke({"messages": [HumanMessage(user_msg)]})
            ids = first_list_from_json(result["messages"][-1].content)
            logger.info(f"{name}: успех с попытки {attempt + 1}, выбрано {len(ids)}")
            return ids
        except Exception as e:
            logger.warning(f"{name}: попытка {attempt + 1}/{max_retries} не удалась: {e}")
            if _is_rate_limit(e):
                await asyncio.sleep(60)
    logger.error(f"{name}: все попытки исчерпаны")
    return []


def df_to_records(df) -> Any:
    return json.loads(df.to_json(orient="records", force_ascii=False))
