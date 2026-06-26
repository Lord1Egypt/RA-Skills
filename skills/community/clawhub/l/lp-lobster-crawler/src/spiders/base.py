"""爬虫基类。

所有站点 Spider 都应继承 BaseSpider，它提供：
- 站点配置自动加载
- 通用请求头设置
- 增量抓取辅助方法
"""

from typing import Any

import scrapy

from src.config import load_site_config


class BaseSpider(scrapy.Spider):
    """爬虫基类。

    子类需设置 class 属性：
        site_name: 站点配置名称（对应 config/sites/{site_name}.yaml）
    """

    site_name: str = ""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._site_config: dict[str, Any] = {}
        if self.site_name:
            try:
                self._site_config = load_site_config(self.site_name)
            except FileNotFoundError:
                self.logger.warning("Site config not found for %s", self.site_name)

    @property
    def site_config(self) -> dict[str, Any]:
        """当前站点配置。"""
        return self._site_config

    @property
    def base_url(self) -> str:
        """站点基础 URL。"""
        site = self._site_config.get("site", {})
        return site.get("base_url", "")

    @property
    def content_type(self) -> str:
        """内容类型（novel / short_drama）。"""
        site = self._site_config.get("site", {})
        return site.get("content_type", "novel")

    def get_url_pattern(self, key: str) -> str:
        """获取站点 URL 模式。

        Args:
            key: URL 模式键名，如 "book_list"。

        Returns:
            URL 模式字符串。
        """
        urls = self._site_config.get("urls", {})
        return urls.get(key, "")

    def get_field_mapping(self) -> dict[str, str]:
        """获取字段映射配置。

        Returns:
            {目标字段: 源字段} 映射。
        """
        return self._site_config.get("field_mapping", {})
