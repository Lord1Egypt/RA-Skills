"""OK.com 地域切换 — 人工模拟 vs API 方式对比

提供两种切换城市的方式：
1. UI 模拟（switch_city_via_ui）：模拟人的输入和点击行为
2. API 导航（switch_city_via_api）：直接通过 URL 跳转

通过 compare_locale_switch() 可对比两种方式的耗时和最终结果。
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass

from . import selectors as sel
from .client.base import BaseClient
from .errors import OKElementNotFound, OKTimeout
from .human import medium_delay, short_delay, simulate_human_input
from .locale import build_locale, get_current_locale, navigate_to_locale, search_cities
from .types import Locale

logger = logging.getLogger("ok-locale-human")


@dataclass
class SwitchResult:
    """切换地域的结果"""
    method: str               # "ui" 或 "api"
    success: bool
    elapsed_seconds: float    # 耗时（秒）
    final_locale: Locale | None
    final_url: str
    error: str | None = None


# ─── 方式一：UI 模拟（模拟人类操作）──────────────────────────

def switch_city_via_ui(
    bridge: BaseClient,
    city_name: str,
    timeout: int = 15000,
) -> SwitchResult:
    """通过 UI 模拟人的行为切换城市

    流程：
    1. 点击定位图标，打开城市选择弹窗
    2. 在搜索框中逐步输入城市名
    3. 等待搜索结果出现
    4. 点击匹配的城市条目
    5. 等待页面跳转完成

    Args:
        bridge: BaseClient 实例
        city_name: 要切换到的城市名（如 "Hawaii"）
        timeout: 等待元素超时（ms）

    Returns:
        SwitchResult 对象
    """
    start = time.time()

    try:
        # 1. 点击定位图标打开城市选择弹窗
        logger.info("步骤1: 点击定位图标打开城市选择弹窗")
        try:
            bridge.wait_for_selector(sel.CITY_SELECTOR_TRIGGER, timeout=timeout)
        except Exception:
            raise OKElementNotFound("城市选择器入口未找到")

        bridge.click_element(sel.CITY_SELECTOR_TRIGGER)
        medium_delay()

        # 2. 等待弹窗和搜索框出现
        logger.info("步骤2: 等待城市选择弹窗出现")
        try:
            bridge.wait_for_selector(sel.CITY_SEARCH_INPUT, timeout=timeout)
        except Exception:
            raise OKElementNotFound("城市搜索框未找到")

        short_delay()

        # 3. 在搜索框输入城市名
        logger.info("步骤3: 输入搜索关键词 '%s'", city_name)
        simulate_human_input(bridge, sel.CITY_SEARCH_INPUT, city_name)
        medium_delay()

        # 4. 等待搜索结果加载
        logger.info("步骤4: 等待搜索结果")
        bridge.wait_dom_stable(timeout=5000)
        short_delay()

        # 5. 点击匹配的搜索结果
        logger.info("步骤5: 点击匹配的城市结果")
        clicked = _click_matching_city(bridge, city_name)
        if not clicked:
            raise OKElementNotFound(f"未找到匹配城市: {city_name}")

        # 6. 等待页面跳转完成
        logger.info("步骤6: 等待页面跳转")
        medium_delay()
        bridge.wait_dom_stable(timeout=timeout)

        elapsed = time.time() - start
        final_url = bridge.get_url()
        final_locale = get_current_locale(bridge)

        logger.info("UI 切换完成: %.2fs -> %s", elapsed, final_url)

        return SwitchResult(
            method="ui",
            success=True,
            elapsed_seconds=round(elapsed, 3),
            final_locale=final_locale,
            final_url=final_url,
        )

    except Exception as e:
        elapsed = time.time() - start
        logger.error("UI 切换失败: %s (%.2fs)", e, elapsed)
        return SwitchResult(
            method="ui",
            success=False,
            elapsed_seconds=round(elapsed, 3),
            final_locale=None,
            final_url=bridge.get_url(),
            error=str(e),
        )


def _click_matching_city(bridge: BaseClient, city_name: str) -> bool:
    """在搜索结果中点击匹配的城市

    使用 JS 遍历搜索结果项，找到包含 city_name 的条目并点击。
    """
    js = f"""
    (() => {{
        // 尝试多种可能的结果容器选择器
        const selectors = [
            "[class*='locationWrapperContent'] div",
            "[class*='SearchArea'] div[class*='item']",
            "[class*='cityItem']",
            "[class*='city-item']",
        ];
        const keyword = "{city_name}".toLowerCase();

        for (const sel of selectors) {{
            const items = document.querySelectorAll(sel);
            for (const item of items) {{
                const text = item.textContent?.trim()?.toLowerCase() || '';
                if (text.includes(keyword)) {{
                    item.click();
                    return true;
                }}
            }}
        }}
        return false;
    }})()
    """
    result = bridge.evaluate(js)
    return bool(result)


# ─── 方式二：API 导航（直接 URL 跳转）──────────────────────

def switch_city_via_api(
    bridge: BaseClient,
    country: str,
    city_code: str,
    lang: str = "en",
) -> SwitchResult:
    """通过 URL 直接导航切换城市

    直接构建目标 URL 并导航，无需 UI 交互。

    Args:
        bridge: BaseClient 实例
        country: 国家名、子域名或 ISO code
        city_code: 城市 code（如 "hawaii"，从 fetch_cities / search_cities 获取）
        lang: 语言代码

    Returns:
        SwitchResult 对象
    """
    start = time.time()

    try:
        locale = navigate_to_locale(bridge, country, city_code, lang)
        elapsed = time.time() - start
        final_url = bridge.get_url()

        logger.info("API 切换完成: %.2fs -> %s", elapsed, final_url)

        return SwitchResult(
            method="api",
            success=True,
            elapsed_seconds=round(elapsed, 3),
            final_locale=locale,
            final_url=final_url,
        )

    except Exception as e:
        elapsed = time.time() - start
        logger.error("API 切换失败: %s (%.2fs)", e, elapsed)
        return SwitchResult(
            method="api",
            success=False,
            elapsed_seconds=round(elapsed, 3),
            final_locale=None,
            final_url=bridge.get_url(),
            error=str(e),
        )


# ─── 对比两种方式 ──────────────────────────────────────────

def compare_locale_switch(
    bridge: BaseClient,
    country: str,
    city_name: str,
    city_code: str,
    lang: str = "en",
    start_url: str | None = None,
) -> dict:
    """对比 UI 模拟方式和 API 方式切换城市的效果

    先用 UI 方式切换，返回初始页面，再用 API 方式切换，
    最终对比两者的耗时和结果。

    Args:
        bridge: BaseClient 实例
        country: 国家名（如 "usa"）
        city_name: UI 搜索用的城市名（如 "Hawaii"）
        city_code: API 用的城市 code（如 "hawaii"）
        lang: 语言代码
        start_url: 起始 URL（可选，用于重置）

    Returns:
        对比结果字典
    """
    if start_url is None:
        start_url = bridge.get_url()

    logger.info("=" * 60)
    logger.info("开始对比地域切换: %s -> %s (%s)", country, city_name, city_code)
    logger.info("=" * 60)

    # --- 1. UI 模拟方式 ---
    logger.info("\n--- 方式一：UI 模拟 ---")
    # 先确保在初始页面
    bridge.navigate(start_url)
    bridge.wait_dom_stable()
    medium_delay()

    ui_result = switch_city_via_ui(bridge, city_name)

    # --- 2. API 导航方式 ---
    logger.info("\n--- 方式二：API 导航 ---")
    # 回到初始页面
    bridge.navigate(start_url)
    bridge.wait_dom_stable()
    medium_delay()

    api_result = switch_city_via_api(bridge, country, city_code, lang)

    # --- 3. 对比结果 ---
    comparison = {
        "city_name": city_name,
        "city_code": city_code,
        "country": country,
        "ui": {
            "success": ui_result.success,
            "elapsed_seconds": ui_result.elapsed_seconds,
            "final_url": ui_result.final_url,
            "error": ui_result.error,
        },
        "api": {
            "success": api_result.success,
            "elapsed_seconds": api_result.elapsed_seconds,
            "final_url": api_result.final_url,
            "error": api_result.error,
        },
        "winner": _determine_winner(ui_result, api_result),
    }

    _log_comparison(comparison)
    return comparison


def _determine_winner(ui: SwitchResult, api: SwitchResult) -> str:
    """判断哪种方式更优"""
    if ui.success and not api.success:
        return "ui"
    if api.success and not ui.success:
        return "api"
    if not ui.success and not api.success:
        return "none"

    # 两者都成功，比耗时
    if ui.elapsed_seconds < api.elapsed_seconds:
        return "ui"
    elif api.elapsed_seconds < ui.elapsed_seconds:
        return "api"
    return "tie"


def _log_comparison(comparison: dict) -> None:
    """输出对比结果日志"""
    logger.info("=" * 60)
    logger.info("对比结果")
    logger.info("=" * 60)
    logger.info("城市: %s (%s)", comparison["city_name"], comparison["city_code"])

    for method in ("ui", "api"):
        r = comparison[method]
        status = "✅" if r["success"] else "❌"
        logger.info(
            "  %s %-4s: %s  耗时 %.3fs  -> %s",
            status, method.upper(), "成功" if r["success"] else "失败",
            r["elapsed_seconds"], r["final_url"],
        )
        if r["error"]:
            logger.info("       错误: %s", r["error"])

    logger.info("  🏆 更优方式: %s", comparison["winner"].upper())
    logger.info("=" * 60)
