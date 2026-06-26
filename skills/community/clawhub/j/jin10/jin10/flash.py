"""
快讯模块
支持获取最新快讯列表和搜索快讯
"""

from typing import List, Dict, Optional
from .client import BaseClient


class FlashItem(Dict):
    """快讯项"""
    pass


class FlashListResult(Dict):
    """快讯列表响应"""
    pass


class FlashClient(BaseClient):
    """快讯客户端"""

    def list(self, cursor: Optional[str] = None) -> FlashListResult:
        """
        获取最新快讯列表

        Args:
            cursor: 分页游标，用于获取下一页

        Returns:
            包含 items, next_cursor, has_more 的响应
        """
        params = {}
        if cursor:
            params['cursor'] = cursor
        return self.call_tool('list_flash', params)

    def search(self, keyword: str) -> FlashListResult:
        """
        按关键词搜索快讯

        Args:
            keyword: 搜索关键词

        Returns:
            包含搜索结果的响应
        """
        return self.call_tool('search_flash', {'keyword': keyword})

    def list_all(self, max_pages: int = 3) -> List[FlashItem]:
        """
        获取所有最新快讯（自动翻页）

        Args:
            max_pages: 最大页数限制

        Returns:
            所有快讯项的列表
        """
        items: List[FlashItem] = []
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
    def format_flash_list(flash_list: FlashListResult) -> str:
        """格式化快讯列表为可读字符串"""
        data = flash_list.get('data', {})
        items = data.get('items', [])
        has_more = data.get('has_more', False)

        lines = []
        for item in items:
            lines.append(
                f"[{item.get('time', '')}] {item.get('title', '')}\n"
                f"  {item.get('url', '')}"
            )

        result = '\n\n'.join(lines)
        if has_more:
            result += '\n\n... 还有更多快讯'

        return result

    @staticmethod
    def format_flash_item(item: FlashItem) -> str:
        """格式化单个快讯为可读字符串"""
        return (
            f"[{item.get('time', '')}] {item.get('title', '')}\n"
            f"链接: {item.get('url', '')}"
        )
