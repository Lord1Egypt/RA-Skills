"""Этапы 1–2: отбор новостей агентами + агент замены новости."""
from __future__ import annotations

import asyncio
import json
from datetime import datetime
from typing import Callable, Literal, Optional

import pandas as pd
from langchain_core.tools import tool
from loguru import logger

from .config import ctx, read_prompt
from .utils import df_to_records, run_agent, web_search as _web_search

NewsType = Literal["telegram", "google_news"]
BASE_COLS = ["id", "source", "description", "type", "url"]


# ---------------- общие инструменты ----------------
@tool
def web_search(query: str, geo: Literal["RU", "US"] = "US"):
    """Инструмент для поиска в интернете. Возвращает первые 10 новостей из news.google.com.
    Для начала поиска нужно задать запрос и в каком регионе искать (RU или US)"""
    return _web_search(query, geo)


@tool
def current_date():
    """Инструмент показывает текущую дату"""
    return datetime.now().strftime("%Y-%m-%d")


def digests_history(n: int) -> str:
    history = ""
    for p in ctx().previous_selected(n):
        try:
            df = pd.read_excel(p)
            cols = [c for c in ("description", "type") if c in df.columns]
            history += f"ПОДБОРКА {p.stem}\n\n{df[cols].to_json(orient='records', lines=True, force_ascii=False)}\n\n"
        except Exception as e:
            logger.warning(f"Не прочитана прошлая подборка {p.name}: {e}")
    return history or "Предыдущих подборок нет."


def make_previous_digest_tool(n: int):
    @tool
    def get_previous_digest():
        """Инструмент для получения предыдущих выборок новостей"""
        return digests_history(n)
    return get_previous_digest


def make_list_tools(get_df: Callable[[], pd.DataFrame], cols: list[str], batch_hint: int):
    @tool
    def get_news_by_id(range_start: int, range_end: int):
        """Инструмент для получения информации по нескольким новостям по индексам. Новости извлекаются
        из выборки для ранжирования. Нумерация индекса начинается с 0. Нужно указать начальный и конечный индекс."""
        df = get_df()
        df = df[[c for c in cols if c in df.columns]]
        return df_to_records(df.iloc[range_start:range_end])

    get_news_by_id.description += f" Оптимальное максимальное число извлекаемых новостей -- {batch_hint}"

    @tool
    def get_news_count():
        """Возвращает общее количество новостей в выборке"""
        return {"response": int(get_df().shape[0])}

    return [get_news_by_id, get_news_count]


def limits_factory(limit_list_tool: bool = True):
    def build():
        from langchain.agents.middleware import ToolCallLimitMiddleware
        mws = [ToolCallLimitMiddleware(tool_name="web_search", run_limit=30, exit_behavior="continue")]
        if limit_list_tool:
            mws.append(ToolCallLimitMiddleware(tool_name="get_news_by_id", run_limit=30,
                                               exit_behavior="continue"))
        return mws
    return build


# ---------------- Этап 1: первичный отбор (3 агента параллельно) ----------------
def _load_sources() -> dict[str, pd.DataFrame]:
    c = ctx()
    src = {}
    if c.tg_csv.exists():
        src["telegram"] = pd.read_csv(c.tg_csv)
    if c.google_csv.exists():
        src["google"] = pd.read_csv(c.google_csv)
    if c.claude_xlsx and c.claude_xlsx.exists():
        src["claude"] = pd.read_excel(c.claude_xlsx)
    return src


async def stage1_select() -> int:
    sources = _load_sources()
    if not sources:
        raise RuntimeError("Нет собранных новостей ни из одного источника")

    prompts = {"telegram": read_prompt("prompt_tg.txt"),
               "google": read_prompt("prompt_google.txt"),
               "claude": read_prompt("prompt_google.txt")}
    batch = {"telegram": 50, "google": 30, "claude": 30}

    async def one(name: str, df: pd.DataFrame):
        tools = [web_search, current_date, make_previous_digest_tool(1),
                 *make_list_tools(lambda d=df: d, ["id", "source", "description", "type"], batch[name])]
        ids = await run_agent(f"{name}-agent", prompts[name], tools, "Подготовь топ 10 новости",
                              limits_factory())
        return name, ids

    results = await asyncio.gather(*(one(n, d) for n, d in sources.items()), return_exceptions=True)

    parts = []
    for res in results:
        if isinstance(res, Exception):
            logger.error(f"Агент этапа 1 упал: {res}")
            continue
        name, ids = res
        df = sources[name]
        rows = df[df["id"].isin(ids)][[c for c in BASE_COLS if c in df.columns]]
        logger.info(f"{name}: в первичную выборку попало {len(rows)}")
        parts.append(rows)

    if not parts or all(p.empty for p in parts):
        raise RuntimeError("Агенты этапа 1 ничего не отобрали")

    coll = pd.concat(parts).reset_index(drop=True)
    coll["id_original"] = coll["id"]
    coll["id"] = coll.index + 1
    coll.to_excel(ctx().collection_xlsx, index=False)
    return len(coll)


# ---------------- Этап 2: итоговая выборка ----------------
def final_pool() -> pd.DataFrame:
    """Текущая коллекция минус новости, уже бывшие в предыдущей коллекции."""
    c = ctx()
    cur = pd.read_excel(c.collection_xlsx)
    prev = c.previous_collection()
    if prev is not None:
        prev_urls = set(pd.read_excel(prev)["url"].dropna().tolist())
        cur = cur[~cur["url"].isin(prev_urls)]
    return cur


async def stage2_final_select() -> int:
    pool = final_pool()
    if pool.empty:
        raise RuntimeError("После дедупликации с прошлым запуском выборка пуста")
    tools = [web_search, current_date, make_previous_digest_tool(5),
             *make_list_tools(lambda: pool, list(pool.columns), 5)]
    ids = await run_agent("final-agent", read_prompt("prompt_final_select.txt"), tools,
                          "Подготовь топ 5 новостей для пользователя.", limits_factory(False))
    if not ids:
        raise RuntimeError("Финальный агент не вернул выборку")
    df = pool[pool["id"].isin(ids)].copy()
    # сохраняем порядок, в котором агент вернул id
    df["__order"] = df["id"].map({v: i for i, v in enumerate(ids)})
    df = df.sort_values("__order").drop(columns="__order")
    df.to_excel(ctx().selected_xlsx, index=False)
    return len(df)


# ---------------- Агент замены новости ----------------
def pool_for_change(news_type: NewsType) -> pd.DataFrame:
    c = ctx()
    selected = pd.read_excel(c.selected_xlsx)
    coll = pd.read_excel(c.collection_xlsx)
    coll = coll[coll["type"] == news_type]
    coll = coll[~coll["id"].isin(selected[selected["type"] == news_type]["id"].tolist())]
    coll = coll[~coll["url"].isin(selected["url"].tolist())]
    prev = c.previous_collection()
    if prev is not None:
        coll = coll[~coll["url"].isin(pd.read_excel(prev)["url"].tolist())]
    return coll


async def change_news(news_type: NewsType, exclude_ids: set[int]) -> Optional[int]:
    """Возвращает id новости из коллекции на замену (или None)."""
    def pool():
        p = pool_for_change(news_type)
        return p[~p["id"].isin(exclude_ids)]

    if pool().empty:
        return None
    tools = [web_search, current_date, make_previous_digest_tool(10),
             *make_list_tools(pool, ["id", "source", "description"], 5)]
    ids = await run_agent(f"change-agent[{news_type}]", read_prompt("prompt_change_news.txt"), tools,
                          "Выбери самую интересную новость для пользователя", limits_factory(False))
    valid = [i for i in ids if i in set(pool()["id"].tolist())]
    return valid[0] if valid else None
