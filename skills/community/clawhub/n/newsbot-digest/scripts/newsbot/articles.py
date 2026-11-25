"""Этап 3: извлечение текста статей (Camoufox, headless), проверка на paywall,
поиск аналогов/замена, перевод, PDF, заголовки."""
from __future__ import annotations

import asyncio
import json
import os
import re
from difflib import SequenceMatcher
from pathlib import Path
from typing import Optional

import pandas as pd
from loguru import logger

from .config import ctx, read_prompt
from .selection import change_news
from .utils import decode_google_url, extract_json_from_string, llm_call, web_search

COOKIE_SELECTOR = ("button:has-text('Accept'), button:has-text('Continue'), button:has-text('Agree'), "
                   "button:has-text('Принять'), button:has-text('Accept All'), "
                   "button:has-text('Принять все'), button:has-text('Allow All')")
EXPAND_SELECTOR = ("button:has-text('Expand to continue reading ↓'), "
                   "button:has-text('Expand to continue reading'), button:has-text('Story Continues')")
MAX_REPLACEMENTS = int(os.getenv("NEWSBOT_MAX_REPLACEMENTS", "3"))


# ---------------- браузер ----------------
async def _accept_cookie(page, bloomberg: bool) -> None:
    try:
        if bloomberg:
            frame = page.get_by_title("SP Consent Message").content_frame
            await frame.get_by_role("button", name="Accept all").click(timeout=5000)
            return
        buttons = await page.query_selector_all(COOKIE_SELECTOR)
        if buttons:
            await buttons[0].click()
            await asyncio.sleep(2)
    except Exception:
        logger.debug("cookie-баннер не найден")


async def _expand_article(page) -> None:
    try:
        buttons = await page.query_selector_all(EXPAND_SELECTOR)
        if buttons:
            await buttons[0].click()
    except Exception:
        pass


async def extract_article_text(url: str) -> tuple[str, str]:
    """Открывает страницу в Camoufox БЕЗ показа окна браузера и извлекает заголовок + текст."""
    import trafilatura
    from camoufox.async_api import AsyncCamoufox
    from readability import Document

    real_url = decode_google_url(url)
    try:
        async with AsyncCamoufox(headless=ctx().headless, humanize=True) as browser:
            page = await browser.new_page()
            await page.goto(real_url, timeout=80000)
            await asyncio.sleep(3)
            await _accept_cookie(page, "bloomberg.com" in real_url)
            await _expand_article(page)
            html = await page.content()
        return Document(html).title(), trafilatura.extract(html) or ""
    except Exception as e:
        logger.warning(f"Не удалось извлечь статью {real_url}: {e}")
        return "", ""


def check_article(text: str) -> bool:
    """LLM-проверка: текст извлечён целиком (нет paywall/обрыва)."""
    if not text or len(text.strip()) < 200:
        return False
    try:
        answer = llm_call(read_prompt("promp_check_article_prompt.txt"), f"Проверь эту статью: \n\n {text}")
        status = (extract_json_from_string(answer) or {}).get("check_status", "")
        return str(status).strip().lower() in ("ок", "ok")
    except Exception as e:
        logger.warning(f"Проверка статьи не удалась: {e}")
        return False


async def fetch_checked(url: str) -> Optional[tuple[str, str]]:
    title, text = await extract_article_text(url)
    return (title, text) if check_article(text) else None


# ---------------- извлечение + замена ----------------
def _norm_title(s: str) -> str:
    s = re.sub(r"\s+-\s+[^-]+$", "", str(s))  # "Заголовок - Издание" -> "Заголовок"
    return re.sub(r"\W+", " ", s).strip().lower()


def _same_story(a: str, b: str) -> bool:
    a, b = _norm_title(a), _norm_title(b)
    return bool(a and b) and (a.startswith(b) or b.startswith(a) or SequenceMatcher(None, a, b).ratio() > 0.8)


def _save_en(news_id: int, title: str, text: str) -> None:
    (ctx().en_dir / f"google_news_{int(news_id)}.md").write_text(f"{title}\n\n{text}", encoding="utf-8")


async def extract_and_save_articles() -> dict:
    c = ctx()
    df = pd.read_excel(c.selected_xlsx)
    stats = {"ok": 0, "analogue": 0, "replaced": 0, "failed": 0}

    for i in df.index:
        row = df.loc[i]
        if row["type"] != "google_news":
            continue
        logger.info(f"Статья: {row['description']}")

        got = await fetch_checked(row["url"])
        if got:
            _save_en(row["id"], *got)
            stats["ok"] += 1
            continue

        # 1. ищем ту же новость у другого издания
        logger.info("Текст недоступен (paywall/ошибка) — ищу аналог")
        found = False
        try:
            for a in json.loads(web_search(str(row["description"]))):
                if not isinstance(a, dict) or not _same_story(a.get("title", ""), row["description"]):
                    continue
                if a.get("url") == row["url"]:
                    continue
                got = await fetch_checked(a["url"])
                if got:
                    df.loc[i, ["source", "description", "url"]] = [a["source"], a["title"], a["url"]]
                    _save_en(row["id"], *got)
                    logger.info(f"Найден аналог: {a['source']} | {a['url']}")
                    stats["analogue"] += 1
                    found = True
                    break
        except Exception as e:
            logger.warning(f"Ошибка поиска аналогов: {e}")

        # 2. просим агента подобрать замену из коллекции
        if not found:
            df.to_excel(c.selected_xlsx, index=False)
            coll = pd.read_excel(c.collection_xlsx)
            tried: set[int] = set()
            for _ in range(MAX_REPLACEMENTS):
                rid = await change_news("google_news", tried)
                if rid is None:
                    break
                tried.add(rid)
                rep = coll[coll["id"] == rid]
                if rep.empty:
                    continue
                rep = rep.iloc[0]
                got = await fetch_checked(rep["url"])
                if got:
                    for col in ("id", "source", "description", "url", "id_original"):
                        if col in rep.index:
                            df.loc[i, col] = rep[col]
                    _save_en(rid, *got)
                    logger.info(f"Новость заменена агентом: {rep['source']} | {rep['description']}")
                    stats["replaced"] += 1
                    found = True
                    break
                df.to_excel(c.selected_xlsx, index=False)

        if not found:
            logger.warning(f"Не удалось получить текст: {row['description']}")
            stats["failed"] += 1
        df.to_excel(c.selected_xlsx, index=False)

    df.to_excel(c.selected_xlsx, index=False)
    return stats


# ---------------- перевод + PDF ----------------
def md_to_pdf(md_text: str, output_path: Path) -> None:
    from markdown_pdf import MarkdownPdf, Section
    pdf = MarkdownPdf()
    pdf.add_section(Section(md_text, toc=False))
    pdf.save(str(output_path))


def translate_articles() -> int:
    c = ctx()
    df = pd.read_excel(c.selected_xlsx)
    prompt = read_prompt("prompt_article_translation.txt")
    if "translation_pdf" not in df.columns:
        df["translation_pdf"] = ""
    df["translation_pdf"] = df["translation_pdf"].astype("object")
    done = 0
    for i in df.index:
        if df.loc[i, "type"] != "google_news":
            continue
        name = f"google_news_{int(df.loc[i, 'id'])}"
        en = c.en_dir / f"{name}.md"
        if not en.exists():
            continue
        try:
            ru_text = llm_call(prompt, en.read_text(encoding="utf-8"))
            (c.ru_dir / f"{name}.md").write_text(ru_text, encoding="utf-8")
            pdf_path = c.pdf_dir / f"{name}.pdf"
            md_to_pdf(ru_text, pdf_path)
            df.loc[i, "translation_pdf"] = str(pdf_path.resolve())
            done += 1
            logger.info(f"Перевод готов: {pdf_path.name}")
        except Exception as e:
            logger.error(f"Ошибка перевода {name}: {e}")
    df.to_excel(c.selected_xlsx, index=False)
    return done


# ---------------- заголовки ----------------
def add_titles() -> None:
    c = ctx()
    df = pd.read_excel(c.selected_xlsx)
    p_google = read_prompt("prompt_title_google.txt")
    p_tg = read_prompt("prompt_title_telegram.txt")
    df["RU_TITLE"] = ""
    df["RU_TITLE"] = df["RU_TITLE"].astype("object")
    for i in df.index:
        row = df.loc[i]
        try:
            if row["type"] == "google_news":
                ru = c.ru_dir / f"google_news_{int(row['id'])}.md"
                if ru.exists():
                    title = llm_call(p_google, f"текст статьи:\n\n{ru.read_text(encoding='utf-8')}")
                else:
                    title = llm_call(p_tg, str(row["description"])) + " [текст статьи недоступен]"
            else:
                title = llm_call(p_tg, str(row["description"]))
            df.loc[i, "RU_TITLE"] = f"{title.strip()} ({row['source']})"
        except Exception as e:
            logger.error(f"Ошибка заголовка: {e}")
            df.loc[i, "RU_TITLE"] = f"{row['description']} ({row['source']})"
    df.to_excel(c.selected_xlsx, index=False)
