"""OK.com Client 统一接口定义"""

from __future__ import annotations

import abc
from typing import Any


class BaseClient(abc.ABC):
    """
    Client 抽象基类。
    无论是 Chrome Extension Bridge 还是 Playwright，都必须实现这些方法。
    从而保证上层的业务模块（search.py, locale.py）不需要因为底层引擎变化而改代码。
    """

    @abc.abstractmethod
    def navigate(self, url: str) -> None:
        """导航到指定 URL"""
        ...

    @abc.abstractmethod
    def wait_for_load(self, timeout: int = 60000) -> None:
        """等待页面加载完成"""
        ...

    @abc.abstractmethod
    def get_url(self) -> str:
        """获取当前页面 URL"""
        ...

    @abc.abstractmethod
    def wait_dom_stable(self, timeout: int = 10000, interval: int = 500) -> None:
        """等待 DOM 稳定（即内容不再频繁变化）"""
        ...

    @abc.abstractmethod
    def wait_for_selector(self, selector: str, timeout: int = 30000) -> None:
        """等待指定选择器出现"""
        ...

    @abc.abstractmethod
    def has_element(self, selector: str) -> bool:
        """检查元素是否存在"""
        ...

    @abc.abstractmethod
    def get_elements_count(self, selector: str) -> int:
        """获取匹配元素数量"""
        ...

    @abc.abstractmethod
    def get_element_text(self, selector: str) -> str | None:
        """获取元素文本"""
        ...

    @abc.abstractmethod
    def get_element_attribute(self, selector: str, attr: str) -> str | None:
        """获取元素属性"""
        ...

    @abc.abstractmethod
    def click_element(self, selector: str) -> None:
        """点击元素"""
        ...

    @abc.abstractmethod
    def input_text(self, selector: str, text: str) -> None:
        """输入文本"""
        ...

    @abc.abstractmethod
    def scroll_by(self, x: int = 0, y: int = 0) -> None:
        """滚动页面"""
        ...

    @abc.abstractmethod
    def scroll_to_bottom(self) -> None:
        """滚动到底部"""
        ...

    @abc.abstractmethod
    def scroll_element_into_view(self, selector: str) -> None:
        """滚动元素到可见"""
        ...

    @abc.abstractmethod
    def evaluate(self, expression: str) -> Any:
        """在页面主 world 执行 JS 代码并返回结果"""
        ...

    @abc.abstractmethod
    def send_command(self, method: str, params: dict | None = None) -> Any:
        """底层的统一命令分发方法，部分脚本可能会调用"""
        ...
