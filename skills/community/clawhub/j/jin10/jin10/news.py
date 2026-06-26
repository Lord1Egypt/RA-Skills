"""
资讯模块
支持获取最新资讯列表、搜索资讯、获取资讯详情
"""

from typing import List, Dict, Optional, Union
from .client import BaseClient


class NewsItem(Dict):
    """资讯列表项"""
    pass


class NewsDetail(Dict):
    """资讯详情"""
    pass


class NewsListResult(Dict):
    """资讯列表响应"""
    pass


class NewsDetailResult(Dict):
    """资讯详情响应"""
    pass


class NewsClient(BaseClient):
    """资讯客户端"""

    def list(self, cursor: Optional[str] = None) -> NewsListResult:
        """
        获取最新资讯列表

        Args:
            cursor: 分页游标

        Returns:
            包含 items, next_cursor, has_more 的响应
        """
        params = {}
        if cursor:
            params['cursor'] = cursor
        return self.call_tool('list_news', params)

    def search(self, keyword: str, cursor: Optional[str] = None) -> NewsListResult:
        """
        按关键词搜索资讯

        Args:
            keyword: 搜索关键词
            cursor: 分页游标

        Returns:
            包含搜索结果的响应
        """
        params = {'keyword': keyword}
        if cursor:
            params['cursor'] = cursor
        return self.call_tool('search_news', params)

    def get(self, id: Union[str, int]) -> NewsDetailResult:
        """
        获取单篇资讯详情

        Args:
            id: 资讯ID

        Returns:
            资讯详情响应
        """
        return self.call_tool('get_news', {'id': id})

    def list_all(self, max_pages: int = 3) -> List[NewsItem]:
        """
        获取所有最新资讯（自动翻页）

        Args:
            max_pages: 最大页数限制

        Returns:
            所有资讯项的列表
        """
        items: List[NewsItem] = []
        cursor = None
        page_count = 0

        while page_count < max_pages:
            result = self.list(cursor)
            items.extend(result.get('data', {}).get('items', []))

            data = result.get('data', {})
            if not data.get('has_more') or not data.get('next_cursor'):
                break

            cursor = data['next_cursor']
            page_count += 1

        return items

    @staticmethod
    def format_news_list(news_list: NewsListResult) -> str:
        """格式化资讯列表为可读字符串"""
        data = news_list.get('data', {})
        items = data.get('items', [])
        has_more = data.get('has_more', False)

        lines = []
        for item in items:
            lines.append(
                f"[{item.get('time', '')}] {item.get('title', '')}\n"
                f"{item.get('introduction', '')}\n"
                f"链接: {item.get('url', '')}"
            )

        result = '\n\n'.join(lines)
        if has_more:
            result += '\n\n... 还有更多资讯'

        return result

    @staticmethod
    def format_news_detail(detail: NewsDetail) -> str:
        """格式化资讯详情为可读字符串"""
        data = detail.get('data', detail)
        return (
            f"【{data.get('title', '')}】\n"
            f"{data.get('introduction', '')}\n\n"
            f"{data.get('content', '')}\n\n"
            f"发布时间: {data.get('time', 'N/A')}\n"
            f"链接: {data.get('url', 'N/A')}"
        )
