"""OK.com 收藏夹管理

支持：列出收藏、添加收藏、取消收藏。
优先通过浏览器 UI 操作，保持与 ok.com 前端行为一致。
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field

from . import selectors as sel
from .client.base import BaseClient
from .errors import OKElementNotFound, OKNotLoggedIn
from .human import medium_delay, short_delay

logger = logging.getLogger("ok-favorites")

_FAV_PAGE_TEMPLATE = "https://{sub}pub.ok.com/biz/{lang}/list/favorites"


@dataclass
class FavItem:
    """收藏列表条目"""

    title: str
    url: str | None = None
    price: str | None = None
    image_url: str | None = None
    address: str | None = None
    company: str | None = None


@dataclass
class FavResult:
    """收藏列表结果"""

    total: int = 0
    items: list[FavItem] = field(default_factory=list)
    url: str | None = None


def _detect_subdomain(client: BaseClient) -> str:
    """从当前页面 URL 推断 subdomain（如 sg / us / ae）。"""
    url = client.get_url() or ""
    m = re.search(r"https?://([a-z]+)(?:pub)?\.ok\.com", url)
    return m.group(1).replace("pub", "") if m else "sg"


def _navigate_to_favourites(
    client: BaseClient,
    subdomain: str = "sg",
    lang: str = "en",
) -> str:
    """导航到收藏页，返回最终 URL。"""
    fav_url = _FAV_PAGE_TEMPLATE.format(sub=subdomain, lang=lang)
    client.navigate(fav_url)
    client.wait_dom_stable(timeout=15000)
    medium_delay()

    current = client.get_url() or ""
    if "login" in current.lower():
        raise OKNotLoggedIn("需要登录才能查看收藏列表")

    if not client.has_element(sel.USER_AVATAR):
        raise OKNotLoggedIn(
            f"未登录 {subdomain}.ok.com，请先在该站点登录"
        )
    return current


def list_favorites(
    client: BaseClient,
    subdomain: str = "sg",
    lang: str = "en",
    max_results: int = 50,
) -> FavResult:
    """获取收藏列表。

    Args:
        client: 浏览器客户端
        subdomain: 国家子域（sg / us / ae …）
        lang: 语言
        max_results: 最大返回条数

    Returns:
        FavResult 包含收藏条目列表
    """
    final_url = _navigate_to_favourites(client, subdomain, lang)

    items = _extract_fav_cards(client, max_results)
    logger.info("收藏列表: 获取 %d 条", len(items))

    return FavResult(total=len(items), items=items, url=final_url)


def _extract_fav_cards(client: BaseClient, max_results: int) -> list[FavItem]:
    """从收藏页提取卡片信息。"""
    js = f"""(() => {{
        const cards = document.querySelectorAll("{sel.FAV_CARD}");
        const results = [];
        const limit = Math.min(cards.length, {max_results});
        for (let i = 0; i < limit; i++) {{
            const c = cards[i];
            const titleEl = c.querySelector("{sel.FAV_CARD_TITLE}");
            const priceEl = c.querySelector("{sel.FAV_CARD_PRICE}");
            const imgEl = c.querySelector("{sel.FAV_CARD_IMAGE}");
            const addrEl = c.querySelector("{sel.FAV_CARD_ADDRESS}");
            const compEl = c.querySelector("{sel.FAV_CARD_COMPANY}");
            results.push({{
                title: titleEl ? titleEl.textContent.trim() : '',
                url: c.href || '',
                price: priceEl ? priceEl.textContent.trim() : '',
                image: imgEl ? imgEl.src : '',
                address: addrEl ? addrEl.textContent.trim() : '',
                company: compEl ? compEl.textContent.trim() : ''
            }});
        }}
        return results;
    }})()"""

    raw = client.evaluate(js) or []
    items: list[FavItem] = []
    for r in raw:
        items.append(
            FavItem(
                title=r.get("title", ""),
                url=r.get("url") or None,
                price=r.get("price") or None,
                image_url=r.get("image") or None,
                address=r.get("address") or None,
                company=r.get("company") or None,
            )
        )
    return items


def add_favorite(client: BaseClient, post_url: str) -> dict:
    """在帖子详情页点击收藏按钮，添加收藏。

    Args:
        client: 浏览器客户端
        post_url: 帖子详情页 URL

    Returns:
        {"success": bool, "url": str, "message": str}
    """
    client.navigate(post_url)
    client.wait_dom_stable(timeout=15000)
    medium_delay()

    current = client.get_url() or ""
    if "login" in current.lower():
        raise OKNotLoggedIn("需要登录才能收藏帖子")

    clicked = _click_detail_fav_btn(client)
    if not clicked:
        raise OKElementNotFound("未找到详情页收藏按钮")

    short_delay()
    return {"success": True, "url": post_url, "message": "已收藏"}


def remove_favorite(client: BaseClient, post_url: str) -> dict:
    """在帖子详情页点击收藏按钮取消收藏（toggle），或在收藏列表页点击心形取消。

    Args:
        client: 浏览器客户端
        post_url: 帖子详情页 URL

    Returns:
        {"success": bool, "url": str, "message": str}
    """
    client.navigate(post_url)
    client.wait_dom_stable(timeout=15000)
    medium_delay()

    current = client.get_url() or ""
    if "login" in current.lower():
        raise OKNotLoggedIn("需要登录才能取消收藏")

    clicked = _click_detail_fav_btn(client)
    if not clicked:
        raise OKElementNotFound("未找到详情页收藏按钮")

    short_delay()
    return {"success": True, "url": post_url, "message": "已取消收藏"}


def remove_favorite_from_list(
    client: BaseClient,
    subdomain: str = "sg",
    lang: str = "en",
    index: int = 0,
) -> dict:
    """在收藏列表页，点击第 index 张卡片的心形按钮取消收藏。

    Args:
        client: 浏览器客户端
        subdomain: 国家子域
        lang: 语言
        index: 第几个收藏（0-based）

    Returns:
        {"success": bool, "index": int, "message": str}
    """
    _navigate_to_favourites(client, subdomain, lang)

    js = f"""(() => {{
        const hearts = document.querySelectorAll("{sel.FAV_HEART_BTN}");
        if ({index} >= hearts.length) return false;
        hearts[{index}].click();
        return true;
    }})()"""

    clicked = client.evaluate(js)
    if not clicked:
        raise OKElementNotFound(f"未找到第 {index} 个收藏的取消按钮")

    short_delay()
    return {"success": True, "index": index, "message": "已从列表取消收藏"}


def _click_detail_fav_btn(client: BaseClient) -> bool:
    """在详情页点击 Favourites 按钮（toggle 收藏状态）。"""
    js = f"""(() => {{
        const area = document.querySelector("{sel.DETAIL_FAV_AREA}");
        if (!area) return false;
        const btns = area.querySelectorAll("{sel.DETAIL_FAV_BTN}");
        for (const btn of btns) {{
            const text = (btn.textContent || '').trim();
            if (text.includes('Favourite') || text.includes('favourite')) {{
                btn.click();
                return true;
            }}
        }}
        return false;
    }})()"""
    return bool(client.evaluate(js))
