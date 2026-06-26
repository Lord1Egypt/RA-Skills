"""OK.com 一站式搜索流程

在同一个浏览器会话中完成：打开网站 → 切换城市 → 点击分类 → 搜索关键词 → 提取结果。
解决多次 CLI 调用在不同 agent 会话中状态不可控的问题。
"""

from __future__ import annotations

import contextlib
import logging
import re
from dataclasses import dataclass, field

from . import selectors as sel
from .client.base import BaseClient
from .human import medium_delay, short_delay
from .locale import build_locale, get_country_info, get_current_locale, search_cities
from .search import _extract_listings, _filter_by_price
from .types import Listing
from .urls import build_base_url

logger = logging.getLogger("ok-full-search")


@dataclass
class StepResult:
    step: str
    success: bool
    detail: dict = field(default_factory=dict)
    error: str | None = None


@dataclass
class FullSearchResult:
    flow: dict = field(default_factory=dict)
    steps: list[StepResult] = field(default_factory=list)
    total: int = 0
    listings: list[Listing] = field(default_factory=list)
    final_url: str = ""


def full_search_flow(
    client: BaseClient,
    country: str,
    city_keyword: str,
    category: str | None = None,
    keyword: str | None = None,
    lang: str = "en",
    max_results: int = 20,
    price_min: float | None = None,
    price_max: float | None = None,
) -> FullSearchResult:
    """一站式搜索：打开 → 切换城市 → 点击分类 → 搜索 → 提取结果

    Args:
        client: 浏览器客户端
        country: 国家名（如 usa, singapore）
        city_keyword: 城市名关键词，用于 UI 搜索（如 hawaii, tokyo）
        category: 分类 code（如 property, jobs），可选
        keyword: 搜索关键词，可选
        lang: 语言代码
        max_results: 最大结果数
        price_min: 最低价格
        price_max: 最高价格
    """
    # 归一化：agent 可能传入 code 格式（如 "new-york"），转为 UI 可搜索的格式
    city_keyword = city_keyword.replace("-", " ")

    result = FullSearchResult(flow={
        "country": country,
        "city_keyword": city_keyword,
        "category": category,
        "keyword": keyword,
        "price_min": price_min,
        "price_max": price_max,
    })

    # --- Step 1: 打开 ok.com 并切换到目标国家 ---
    step1 = _step_open_site(client, country, lang)
    result.steps.append(step1)
    if not step1.success:
        result.final_url = client.get_url()
        return result

    # --- Step 2: 进入分类页（匹配 slug + URL 导航）---
    resolved_category = category
    if category:
        step2 = _step_click_category(client, category)
        result.steps.append(step2)
        resolved_category = step2.detail.get("resolved_slug", category)
        result.flow["resolved_category"] = resolved_category

    # --- Step 3: 切换城市（优先 UI，fallback API+URL）---
    step3 = _step_switch_city(client, country, city_keyword, lang, resolved_category)
    result.steps.append(step3)
    city_code = step3.detail.get("city_code", city_keyword)
    result.flow["city_code"] = city_code

    if not step3.success:
        result.final_url = client.get_url()
        return result

    # --- Step 4: 输入搜索词并搜索（可选）---
    if keyword:
        step4 = _step_search_keyword(client, keyword)
        result.steps.append(step4)

    # --- Step 5: 页面上设置价格筛选（可选）---
    price_filter_ok = False
    if price_min is not None or price_max is not None:
        step5 = _step_apply_price_filter(client, price_min, price_max)
        result.steps.append(step5)
        price_filter_ok = step5.success

    # --- Step 6: 提取结果 ---
    fallback_price_min = None if price_filter_ok else price_min
    fallback_price_max = None if price_filter_ok else price_max
    step6 = _step_extract_results(
        client, max_results, fallback_price_min, fallback_price_max,
    )
    result.steps.append(step6)
    result.listings = step6.detail.get("raw_listings", [])
    result.total = len(result.listings)
    result.final_url = client.get_url()

    logger.info(
        "一站式搜索完成: country=%s city=%s category=%s keyword=%s → %d 条结果",
        country, city_keyword, category, keyword, result.total,
    )
    return result


# ─── 各步骤实现 ──────────────────────────────────────────────


def _step_open_site(client: BaseClient, country: str, lang: str) -> StepResult:
    """Step 1: 导航到目标国家的 ok.com"""
    try:
        info = get_country_info(country)
        subdomain = info["subdomain"]
        url = f"https://{subdomain}.ok.com/{lang}/"

        logger.info("Step 1: 打开 %s", url)
        client.navigate(url)
        client.wait_dom_stable(timeout=15000)
        medium_delay()

        _dismiss_cookie_banner(client)

        return StepResult(step="open_site", success=True, detail={"url": url})
    except Exception as e:
        logger.error("Step 1 失败: %s", e)
        return StepResult(step="open_site", success=False, error=str(e))


def _step_switch_city(
    client: BaseClient,
    country: str,
    city_keyword: str,
    lang: str,
    category: str | None = None,
) -> StepResult:
    """Step 3: 切换城市 — 优先 UI（筛选栏城市弹窗），失败 fallback API+URL

    UI 流程：点击筛选栏城市 filter → 弹出 LocationWrapperNew 面板
    → 输入城市名搜索 → 点击搜索结果项
    """
    # 先尝试 UI 方式
    ui_result = _switch_city_via_ui(client, city_keyword, category)
    if ui_result and ui_result.success:
        return ui_result

    logger.info("UI 城市切换失败，降级到 API+URL 方式")
    return _switch_city_via_api(client, country, city_keyword, lang, category)


def _switch_city_via_ui(
    client: BaseClient,
    city_keyword: str,
    category: str | None = None,
) -> StepResult | None:
    """通过筛选栏的城市 filter 弹窗切换城市"""
    try:
        # 等待 filter bar 渲染完成
        try:
            client.wait_for_selector(sel.CITY_FILTER_ITEM, timeout=8000)
        except Exception:
            logger.info("filter bar 未加载，跳过 UI 城市切换")
            return None

        cat_lower = (category or "").lower()

        # 1. 获取所有候选 filter（排除固定标签和分类名）
        candidates = client.evaluate(f"""(() => {{
            const fixedLabels = new Set([
                'best match', 'filter', 'price', 'sort',
                'newest', 'oldest', 'clear',
            ]);
            const catLower = '{cat_lower}';
            const items = [...document.querySelectorAll("{sel.CITY_FILTER_ITEM}")];
            const result = [];
            items.forEach((item, idx) => {{
                const text = item.textContent?.trim();
                if (!text) return;
                const cleanText = text.replace(/·\\d+$/, '').trim();
                const lower = cleanText.toLowerCase();
                if (fixedLabels.has(lower)) return;
                if (catLower && lower === catLower) return;
                result.push({{ index: idx, text: cleanText }});
            }});
            return result;
        }})()""")

        if not candidates:
            logger.info("筛选栏未找到候选城市 filter")
            return None

        # 2. 逐个点击候选项，检查是否弹出城市搜索面板
        city_filter_text = None
        for cand in candidates:
            idx = cand["index"]
            client.evaluate(f"""(() => {{
                const items = document.querySelectorAll("{sel.CITY_FILTER_ITEM}");
                if (items[{idx}]) items[{idx}].click();
            }})()""")
            short_delay()

            has_city_input = client.evaluate(f"""(() => {{
                const input = document.querySelector("{sel.CITY_SEARCH_INPUT}");
                return !!(input && input.offsetParent !== null);
            }})()""")

            if has_city_input:
                city_filter_text = cand["text"]
                break

            # 关闭弹出的面板
            client.evaluate("document.body.click()")
            short_delay()

        if not city_filter_text:
            logger.info("所有候选 filter 均未弹出城市搜索面板")
            return None

        logger.info(
            "Step 3 (UI): 点击城市 filter '%s'，弹出城市搜索面板",
            city_filter_text,
        )

        # 3. 在搜索框输入城市名
        client.evaluate(f"""(() => {{
            const input = document.querySelector("{sel.CITY_SEARCH_INPUT}");
            if (!input) return;
            input.focus();
            const nativeSetter = Object.getOwnPropertyDescriptor(
                window.HTMLInputElement.prototype, 'value'
            ).set;
            nativeSetter.call(input, '{city_keyword}');
            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
            input.dispatchEvent(new Event('change', {{ bubbles: true }}));
        }})()""")

        # 4. 等待搜索结果渲染（API 响应需要时间）并点击匹配项
        click_result = None
        for _attempt in range(4):
            medium_delay()
            click_result = client.evaluate(f"""(() => {{
                const items = document.querySelectorAll("{sel.CITY_SEARCH_RESULT_ITEM}");
                if (items.length === 0) return {{ found: false }};
                const kw = '{city_keyword}'.toLowerCase();
                for (const item of items) {{
                    const nameEl = item.querySelector("{sel.CITY_SEARCH_RESULT_NAME}");
                    const name = nameEl?.textContent?.trim() || '';
                    if (name.toLowerCase().includes(kw)) {{
                        item.click();
                        return {{ found: true, clicked: name }};
                    }}
                }}
                const firstName = items[0].querySelector("{sel.CITY_SEARCH_RESULT_NAME}");
                items[0].click();
                return {{ found: true, clicked: firstName?.textContent?.trim() || 'first' }};
            }})()""")
            if click_result and click_result.get("found"):
                break

        if not click_result or not click_result.get("found"):
            logger.info("城市搜索无结果: %s", city_keyword)
            return StepResult(
                step="switch_city_ui", success=False,
                error=f"搜索无结果: {city_keyword}",
            )

        clicked_name = click_result.get("clicked", "")
        logger.info("Step 3 (UI): 选择城市 → %s", clicked_name)

        medium_delay()
        client.wait_dom_stable(timeout=15000)
        medium_delay()

        current_url = client.get_url()
        city_code = _extract_city_code_from_url(current_url) or city_keyword

        return StepResult(
            step="switch_city_ui", success=True,
            detail={
                "city_code": city_code,
                "city_name": clicked_name,
                "method": "ui",
                "url": current_url,
            },
        )

    except Exception as e:
        logger.warning("UI 城市切换异常: %s", e)
        return None


def _switch_city_via_api(
    client: BaseClient,
    country: str,
    city_keyword: str,
    lang: str,
    category: str | None = None,
) -> StepResult:
    """通过 API 查找城市 code + URL 导航（fallback 方式）"""
    try:
        cities = search_cities(country, city_keyword, lang)
        if not cities:
            return StepResult(
                step="switch_city_api", success=False,
                error=f"未找到匹配城市: {city_keyword}",
                detail={"city_keyword": city_keyword},
            )

        best_match = _pick_best_city(cities, city_keyword)
        city_code = best_match.code
        city_name = best_match.name

        locale = build_locale(country, city_code, lang)
        if category:
            from .urls import build_category_url
            url = build_category_url(
                locale.subdomain, locale.lang, locale.city, category,
            )
        else:
            url = build_base_url(locale.subdomain, locale.lang, locale.city)

        logger.info(
            "Step 3 (API): 切换城市 → %s (code=%s) url=%s",
            city_name, city_code, url,
        )
        client.navigate(url)
        client.wait_dom_stable(timeout=15000)
        medium_delay()

        return StepResult(
            step="switch_city_api", success=True,
            detail={
                "city_code": city_code,
                "city_name": city_name,
                "method": "api",
                "url": url,
            },
        )

    except Exception as e:
        logger.error("API 城市切换失败: %s", e)
        return StepResult(
            step="switch_city_api", success=False, error=str(e),
            detail={"city_keyword": city_keyword},
        )


def _step_click_category(client: BaseClient, category_code: str) -> StepResult:
    """Step 2: 在首页点击 QuickAccessArea 分类图标

    流程：
    1. 等待首页 QuickAccessArea 渲染
    2. 提取所有可见分类图标的 slug + 文本
    3. 将用户输入模糊匹配到实际 slug
    4. 点击对应图标
    5. 清理 URL 中的 ?iconSource= 参数
    """
    try:
        logger.info("Step 2: 点击分类 → %s", category_code)

        # 等待首页分类图标区域渲染
        qa_sel = sel.HOMEPAGE_QUICK_ACCESS_ITEM
        try:
            client.wait_for_selector(qa_sel, timeout=8000)
        except Exception:
            logger.warning("QuickAccessArea 未加载，降级 URL 导航")
            return _step_click_category_fallback(client, category_code)

        short_delay()

        # 提取可见分类图标（QuickAccessArea_item）
        page_cats = client.evaluate(f"""(() => {{
            const icons = document.querySelectorAll("{qa_sel}");
            const seen = new Set();
            const result = [];
            for (const el of icons) {{
                const href = el.getAttribute('href') || '';
                const match = href.match(/\\/cate-([^/?]+)/);
                if (!match) continue;
                const slug = match[1];
                if (seen.has(slug)) continue;
                seen.add(slug);
                const text = el.textContent?.trim() || '';
                const rect = el.getBoundingClientRect();
                if (rect.width === 0 || rect.height === 0) continue;
                result.push({{ slug, text: text.substring(0, 60) }});
            }}
            return result;
        }})()""")

        if not page_cats:
            logger.warning("QuickAccessArea 中未找到分类图标")
            return _step_click_category_fallback(client, category_code)

        logger.info(
            "首页分类: %s",
            [f"{c['slug']}({c['text']})" for c in page_cats],
        )

        matched_slug = _match_category_slug(category_code, page_cats)
        if not matched_slug:
            logger.warning(
                "分类 '%s' 无法匹配到首页图标: %s",
                category_code,
                [c["slug"] for c in page_cats],
            )
            return _step_click_category_fallback(client, category_code)

        logger.info("分类匹配: '%s' → '%s'", category_code, matched_slug)

        # 点击 QuickAccessArea 中对应的可见图标
        click_ok = client.evaluate(f"""(() => {{
            const icons = document.querySelectorAll("{qa_sel}");
            for (const el of icons) {{
                const href = el.getAttribute('href') || '';
                if (href.includes('/cate-{matched_slug}/') || href.includes('/cate-{matched_slug}?')) {{
                    el.scrollIntoViewIfNeeded?.();
                    el.click();
                    return true;
                }}
            }}
            return false;
        }})()""")

        if not click_ok:
            logger.warning("图标点击失败，降级 URL 导航")
            return _step_click_category_fallback(client, matched_slug)

        medium_delay()
        client.wait_dom_stable(timeout=15000)

        # iconSource 参数会导致后续筛选栏异常，清理掉
        current_url = client.get_url()
        if "iconSource" in current_url:
            clean_url = current_url.split("?")[0]
            client.navigate(clean_url)
            client.wait_dom_stable(timeout=10000)
            medium_delay()

        return StepResult(
            step="click_category", success=True,
            detail={
                "category": category_code,
                "resolved_slug": matched_slug,
                "url": client.get_url(),
            },
        )

    except Exception as e:
        logger.error("Step 2 失败: %s", e)
        return _step_click_category_fallback(client, category_code)


def _match_category_slug(
    user_input: str,
    page_cats: list[dict],
) -> str | None:
    """将用户输入的分类 code 匹配到页面上的实际 slug。

    Handles mismatches like "real-estate-property" -> "property",
    "jobs" -> "jobs", "Real Estate" -> "property".
    """
    code = user_input.lower().strip()
    code_words = set(code.replace("-", " ").replace("_", " ").split())

    # Priority 1: exact slug match
    for cat in page_cats:
        if cat["slug"].lower() == code:
            return cat["slug"]

    # Priority 2: slug is a suffix of the input (real-estate-property → property)
    for cat in page_cats:
        slug = cat["slug"].lower()
        if code.endswith(slug) or code.endswith(f"-{slug}"):
            return cat["slug"]

    # Priority 3: slug contained in input or vice versa
    for cat in page_cats:
        slug = cat["slug"].lower()
        if slug in code or code in slug:
            return cat["slug"]

    # Priority 4: word overlap with display text
    for cat in page_cats:
        text_words = set(cat["text"].lower().replace("-", " ").split())
        if code_words & text_words:
            return cat["slug"]

    # Priority 5: word overlap with slug
    for cat in page_cats:
        slug_words = set(cat["slug"].lower().replace("-", " ").split())
        if code_words & slug_words:
            return cat["slug"]

    return None


def _step_click_category_fallback(client: BaseClient, category_code: str) -> StepResult:
    """Step 2 降级：从当前 URL 构造分类 URL 并导航"""
    try:
        locale = get_current_locale(client)
        if not locale:
            return StepResult(
                step="click_category_fallback", success=False,
                error="无法解析当前 locale",
            )

        from .urls import build_category_url
        url = build_category_url(locale.subdomain, locale.lang, locale.city, category_code)
        logger.info("Step 2 降级: 导航到分类页 %s", url)

        client.navigate(url)
        client.wait_dom_stable(timeout=15000)
        medium_delay()

        return StepResult(
            step="click_category_fallback", success=True,
            detail={"category": category_code, "url": url},
        )
    except Exception as e:
        logger.error("Step 2 降级失败: %s", e)
        return StepResult(step="click_category_fallback", success=False, error=str(e))


def _step_search_keyword(client: BaseClient, keyword: str) -> StepResult:
    """Step 4: 搜索关键词 — 优先 UI，失败 fallback URL 导航

    UI 流程：点击搜索框 → 输入关键词 → Enter → 等待结果加载
    URL 流程：在当前 URL 上追加 ?keyword=X → 直接导航
    """
    # 先尝试 UI 方式
    ui_result = _search_keyword_via_ui(client, keyword)
    if ui_result.success:
        return ui_result

    logger.info("UI 搜索失败，降级到 URL 方式")
    return _search_keyword_via_url(client, keyword)


def _search_keyword_via_ui(client: BaseClient, keyword: str) -> StepResult:
    """通过搜索框 UI 交互输入关键词"""
    try:
        logger.info("Step 4 (UI): 搜索关键词 → %s", keyword)

        # 先尝试关闭 cookie 弹窗，避免遮挡搜索框
        _dismiss_cookie_banner(client)

        client.wait_for_selector(sel.SEARCH_INPUT, timeout=15000)
        client.click_element(sel.SEARCH_INPUT)
        short_delay()
        client.input_text(sel.SEARCH_INPUT, keyword)
        short_delay()

        client.send_command("press_key", {"key": "Enter"})
        medium_delay()

        client.wait_dom_stable(timeout=15000)
        medium_delay()

        return StepResult(
            step="search_ui", success=True,
            detail={"keyword": keyword, "method": "ui", "url": client.get_url()},
        )
    except Exception as e:
        logger.warning("Step 4 (UI) 失败: %s", e)
        return StepResult(step="search_ui", success=False, error=str(e))


def _search_keyword_via_url(client: BaseClient, keyword: str) -> StepResult:
    """通过 URL 追加 keyword 参数直接导航（fallback 方式）"""
    try:
        from .urls import append_keyword_to_url

        current_url = client.get_url()
        search_url = append_keyword_to_url(current_url, keyword)

        logger.info("Step 4 (URL): 导航到 %s", search_url)
        client.navigate(search_url)
        client.wait_dom_stable(timeout=15000)
        medium_delay()

        return StepResult(
            step="search_url", success=True,
            detail={"keyword": keyword, "method": "url", "url": client.get_url()},
        )
    except Exception as e:
        logger.error("Step 4 (URL) 失败: %s", e)
        return StepResult(step="search_url", success=False, error=str(e))


def _step_apply_price_filter(
    client: BaseClient,
    price_min: float | None,
    price_max: float | None,
) -> StepResult:
    """Step 5: 在页面筛选栏上设置价格范围

    ok.com 筛选栏结构：
    - FilterItem_filterItem 按钮（文本 "Price"）→ 点击展开浮层
    - 浮层内 input.native-numeric-input placeholder=Min/Max
    - 底部有 Clear / Confirm 两个按钮，点击 Confirm 触发筛选
    """
    try:
        logger.info(
            "Step 5: 设置价格筛选 min=%s max=%s", price_min, price_max,
        )

        # 1. 点击 Price 按钮展开筛选浮层
        clicked = client.evaluate(f"""(() => {{
            const items = document.querySelectorAll("{sel.FILTER_ITEM}");
            for (const item of items) {{
                const text = item.textContent?.trim();
                if (text === 'Price' || text === 'price') {{
                    item.click();
                    return true;
                }}
            }}
            return false;
        }})()""")

        if not clicked:
            logger.warning("未找到 Price 筛选按钮")
            return StepResult(
                step="price_filter", success=False,
                error="未找到 Price 筛选按钮",
            )

        short_delay()

        # 2. 等待价格输入框出现并填写
        min_sel = sel.FILTER_PRICE_MIN
        max_sel = sel.FILTER_PRICE_MAX

        filled = client.evaluate(f"""(() => {{
            const setVal = (el, val) => {{
                if (!el || val === null || val === undefined) return false;
                el.focus();
                const nativeSetter = Object.getOwnPropertyDescriptor(
                    window.HTMLInputElement.prototype, 'value'
                ).set;
                nativeSetter.call(el, String(val));
                el.dispatchEvent(new Event('input', {{ bubbles: true }}));
                el.dispatchEvent(new Event('change', {{ bubbles: true }}));
                return true;
            }};

            const minInput = document.querySelector("{min_sel}");
            const maxInput = document.querySelector("{max_sel}");

            if (!minInput && !maxInput) return {{ found: false }};

            const minVal = {price_min if price_min is not None else 'null'};
            const maxVal = {price_max if price_max is not None else 'null'};
            const minOk = setVal(minInput, minVal);
            const maxOk = setVal(maxInput, maxVal);

            return {{ found: true, min: minVal, max: maxVal }};
        }})()""")

        if not filled or not filled.get("found"):
            logger.warning("价格输入框未出现")
            return StepResult(
                step="price_filter", success=False,
                error="Price 浮层展开后未找到 Min/Max 输入框",
            )

        short_delay()

        # 3. 点击 Confirm 按钮提交价格筛选
        confirmed = client.evaluate(f"""(() => {{
            const btn = document.querySelector("{sel.FILTER_CONFIRM_BTN}");
            if (btn) {{ btn.click(); return true; }}
            return false;
        }})()""")

        if not confirmed:
            logger.warning("未找到 Confirm 按钮，尝试 Enter 降级")
            with contextlib.suppress(Exception):
                client.send_command("press_key", {"key": "Enter"})

        medium_delay()
        client.wait_dom_stable(timeout=10000)
        medium_delay()

        return StepResult(
            step="price_filter", success=True,
            detail={
                "price_min": price_min,
                "price_max": price_max,
                "confirmed": bool(confirmed),
            },
        )

    except Exception as e:
        logger.error("Step 5 价格筛选失败: %s", e)
        return StepResult(
            step="price_filter", success=False, error=str(e),
        )


def _step_extract_results(
    client: BaseClient,
    max_results: int,
    price_min: float | None,
    price_max: float | None,
) -> StepResult:
    """Step 6: 提取当前页面的结果列表"""
    try:
        logger.info("Step 6: 提取结果")

        # 等待卡片元素渲染（Playwright 无头模式下 React 水合较慢）
        for selector in (sel.LISTING_CARD_LIST, sel.LISTING_CARD_HOME):
            try:
                client.wait_for_selector(selector, timeout=10000)
                break
            except Exception:
                continue

        fetch_count = max_results * 3 if (price_min or price_max) else max_results
        listings = _extract_listings(client, fetch_count)
        listings = _filter_by_price(listings, price_min, price_max)
        listings = listings[:max_results]

        return StepResult(
            step="extract_results", success=True,
            detail={"count": len(listings), "raw_listings": listings},
        )
    except Exception as e:
        logger.error("Step 5 失败: %s", e)
        return StepResult(step="extract_results", success=False, error=str(e))


# ─── 辅助函数 ──────────────────────────────────────────────


def _pick_best_city(cities: list, keyword: str):
    """从城市列表中选择最佳匹配"""
    kw = keyword.lower()
    for c in cities:
        if c.name.lower() == kw or c.code.lower() == kw:
            return c
    for c in cities:
        if kw in c.name.lower() or kw in c.code.lower():
            return c
    return cities[0]


def _extract_city_code_from_url(url: str) -> str | None:
    """从 URL 中提取城市 code，如 /city-hawaii/ → hawaii"""
    m = re.search(r"/city-([^/]+)/", url)
    return m.group(1) if m else None


def _dismiss_cookie_banner(client: BaseClient) -> None:
    """尝试关闭 cookie 横幅"""
    try:
        if client.has_element(sel.COOKIE_ACCEPT_BTN):
            client.click_element(sel.COOKIE_ACCEPT_BTN)
            short_delay()
    except Exception:
        pass
