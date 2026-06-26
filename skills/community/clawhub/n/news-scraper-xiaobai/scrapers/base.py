"""
爬虫基类
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Optional
import requests
import config


class BaseScraper(ABC):
    """新闻爬虫基类"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(config.HEADERS)

    @property
    @abstractmethod
    def name(self) -> str:
        """网站名称"""
        pass

    @property
    @abstractmethod
    def site_id(self) -> str:
        """网站标识符"""
        pass

    @property
    @abstractmethod
    def list_url(self) -> str:
        """新闻列表页URL"""
        pass

    @abstractmethod
    def parse_list(self, html: str) -> List[Dict]:
        """
        解析新闻列表页
        返回: [{"title", "url", "publish_time", "source"}, ...]
        """
        pass

    @abstractmethod
    def parse_detail(self, html: str, url: str) -> Dict:
        """
        解析新闻详情页
        返回: {"title", "content", "publish_time", "source"}
        """
        pass

    def fetch(self, url: str, timeout: int = None) -> Optional[str]:
        """获取页面内容"""
        timeout = timeout or config.REQUEST_TIMEOUT
        try:
            resp = self.session.get(url, timeout=timeout)
            resp.raise_for_status()
            resp.encoding = resp.apparent_encoding
            return resp.text
        except Exception as e:
            print(f"[{self.site_id}] 获取页面失败: {url}, 错误: {e}")
            return None

    def crawl(self, limit: int = None) -> List[Dict]:
        """
        执行爬取
        返回: [{"title", "content", "url", "publish_time", "source", "keywords", "summary"}, ...]
        """
        limit = limit or config.MAX_NEWS_PER_CRAWL
        print(f"[{self.site_id}] 开始爬取，最多 {limit} 条...")

        # 1. 获取列表页
        html = self.fetch(self.list_url)
        if not html:
            print(f"[{self.site_id}] 获取列表页失败")
            return []

        # 2. 解析列表
        news_list = self.parse_list(html)
        # 按时间倒序（从新到旧）
        news_list.sort(key=lambda x: x.get("publish_time", ""), reverse=True)
        news_list = news_list[:limit]

        print(f"[{self.site_id}] 获取到 {len(news_list)} 条新闻")

        # 3. 爬取详情页
        results = []
        for i, item in enumerate(news_list):
            print(f"[{self.site_id}] 爬取第 {i+1}/{len(news_list)} 条: {item['title'][:30]}...")

            # 保留列表页的时间
            list_publish_time = item.get("publish_time", "")

            detail_html = self.fetch(item["url"])
            if detail_html:
                detail = self.parse_detail(detail_html, item["url"])
                # 只更新content，保留列表页的publish_time（更准确）
                item["content"] = detail.get("content", "")
                # 只有当详情页有更准确的时间时才更新
                if detail.get("publish_time") and not detail.get("publish_time").startswith(("6", "7", "8", "9", "10")):
                    item["publish_time"] = detail["publish_time"]
                elif not list_publish_time:
                    item["publish_time"] = detail.get("publish_time", "")
                item["url"] = item["url"]  # 确保URL正确
                results.append(item)
            else:
                # 如果获取详情失败，使用列表页信息
                results.append(item)

        return results
