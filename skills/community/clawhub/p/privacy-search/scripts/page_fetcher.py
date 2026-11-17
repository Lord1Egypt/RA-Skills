#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网页正文抓取

V1.5 新增。为搜索结果中的 URL 抓取正文，供摘要/导出使用。

三层降级：
    1. trafilatura（主方案，专为学术/新闻正文提取）
    2. boilerpy3（降级，纯 Python）
    3. 正则 <p> 标签（兜底）

遵循死规则 9：基础功能自研，外部依赖按需接入，必须提供降级方案。
"""

import re
import sys
from typing import Optional, Tuple

sys.dont_write_bytecode = True

try:
    from version_util import require_dependencies
except ImportError:
    from .version_util import require_dependencies

# trafilatura 和 boilerpy3 为可选依赖，不装也能跑（降级到正则）
_trafilatura_mod = None
_boilerpy3_mod = None
_trafilatura_tried = False
_boilerpy3_tried = False


def _load_trafilatura():
    """懒加载 trafilatura"""
    global _trafilatura_mod, _trafilatura_tried
    if _trafilatura_tried:
        return _trafilatura_mod
    _trafilatura_tried = True
    try:
        import trafilatura as _t
        _trafilatura_mod = _t
    except Exception:
        _trafilatura_mod = None
    return _trafilatura_mod


def _load_boilerpy3():
    """懒加载 boilerpy3"""
    global _boilerpy3_mod, _boilerpy3_tried
    if _boilerpy3_tried:
        return _boilerpy3_mod
    _boilerpy3_tried = True
    try:
        from boilerpy3.extractors import Extractor as _b
        _boilerpy3_mod = _b
    except Exception:
        _boilerpy3_mod = None
    return _boilerpy3_mod


def fetch_page(url: str, timeout: int = 10, proxy: Optional[str] = None) -> Optional[str]:
    """
    抓取网页 HTML

    复用 http_client 的 UA 池/代理/重试
    """
    import asyncio

    try:
        import aiohttp
        from http_client import RequestContext, fetch_text, build_connector
    except ImportError:
        from .http_client import RequestContext, fetch_text, build_connector
        import aiohttp

    ctx = RequestContext(
        headers={},
        proxy=proxy,
        timeout=timeout,
    )

    async def _do():
        async with aiohttp.ClientSession(connector=build_connector(1)) as session:
            return await fetch_text(session, url, ctx)

    try:
        return asyncio.run(_do())
    except Exception:
        return None


def extract_text(html: str) -> Optional[str]:
    """
    从 HTML 中提取正文

    三层降级，任一成功即返回
    """
    if not html:
        return None

    # 方案 1：trafilatura（最准确）
    trafilatura = _load_trafilatura()
    if trafilatura is not None:
        try:
            result = trafilatura.extract(
                html,
                include_comments=False,
                include_tables=False,
                no_fallback=False,
            )
            if result and len(result.strip()) > 50:
                return result.strip()
        except Exception:
            pass

    # 方案 2：boilerpy3
    boilerpy3 = _load_boilerpy3()
    if boilerpy3 is not None:
        try:
            from boilerpy3 import Document
            doc = Document(html)
            result = doc.content()
            if result and len(result.strip()) > 50:
                return result.strip()
        except Exception:
            pass

    # 方案 3：正则 <p> 标签拼接（兜底）
    return _extract_text_regex(html)


def _extract_text_regex(html: str) -> Optional[str]:
    """正则 <p> 标签拼接（最后兜底）"""
    from bs4 import BeautifulSoup
    try:
        soup = BeautifulSoup(html, "lxml")
        # 移除脚本、样式、导航等
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        # 提取 <p> 标签文本
        paragraphs = soup.find_all("p")
        texts = []
        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) > 20:  # 过滤太短的
                texts.append(text)
        if texts:
            return "\n\n".join(texts)
        # 最后尝试 body 全部文本
        body = soup.find("body")
        if body:
            text = body.get_text(separator="\n", strip=True)
            return text[:5000] if text else None
    except Exception:
        pass
    return None


def fetch_and_extract(url: str, timeout: int = 10, proxy: Optional[str] = None) -> Tuple[Optional[str], Optional[str]]:
    """
    抓取网页并提取正文

    Returns:
        (html, text) 元组，任一可能为 None
    """
    html = fetch_page(url, timeout, proxy)
    if not html:
        return None, None
    text = extract_text(html)
    return html, text
