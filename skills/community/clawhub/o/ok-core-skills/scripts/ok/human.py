"""OK.com 行为模拟

模拟真实用户操作节奏，降低风控风险。
"""

from __future__ import annotations

import random
import time


def random_delay(min_s: float = 0.5, max_s: float = 2.0) -> None:
    """随机等待一段时间"""
    time.sleep(random.uniform(min_s, max_s))


def short_delay() -> None:
    """短暂延迟（操作间）"""
    random_delay(0.3, 0.8)


def medium_delay() -> None:
    """中等延迟（页面加载后）"""
    random_delay(1.0, 2.5)


def long_delay() -> None:
    """长延迟（重要操作间）"""
    random_delay(2.0, 5.0)


def typing_delay() -> None:
    """打字间隔"""
    random_delay(0.05, 0.15)


def scroll_delay() -> None:
    """滚动间隔"""
    random_delay(0.5, 1.5)


def simulate_human_scroll(bridge, total_distance: int = 1000, step: int = 300) -> None:
    """模拟人类滚动行为

    Args:
        bridge: BridgeClient 实例
        total_distance: 总滚动距离
        step: 每次滚动步长（会在 ±30% 范围内随机）
    """
    scrolled = 0
    while scrolled < total_distance:
        actual_step = int(step * random.uniform(0.7, 1.3))
        remaining = total_distance - scrolled
        actual_step = min(actual_step, remaining)
        bridge.scroll_by(y=actual_step)
        scrolled += actual_step
        scroll_delay()


def simulate_human_input(bridge, selector: str, text: str) -> None:
    """模拟人类输入行为

    先点击输入框，然后逐字输入。

    Args:
        bridge: BridgeClient 实例
        selector: 输入框 CSS 选择器
        text: 要输入的文本
    """
    bridge.click_element(selector)
    short_delay()
    # 使用 input_text 一次性设置（ok.com 的搜索框使用 React controlled input）
    bridge.input_text(selector, text)
    short_delay()
