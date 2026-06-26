"""
财经日历模块
支持获取重要经济数据发布日程
"""

from typing import List, Dict
from .client import BaseClient


class CalendarEvent(Dict):
    """日历事件"""
    pass


class CalendarResult(Dict):
    """日历响应"""
    pass


# 星级重要性标签
STAR_LABELS = {
    '1': '低',
    '2': '中',
    '3': '高',
    '4': '很高',
    '5': '极高',
}

# 常见财经数据关键词
COMMON_KEYWORDS = [
    '非农', '失业率', 'CPI', 'PPI', 'GDP',
    'ISM', '零售销售', '消费者信心', '初请失业金',
    '利率决议', '美联储', '欧洲央行', '日本央行',
]


class CalendarClient(BaseClient):
    """财经日历客户端"""

    def list(self) -> CalendarResult:
        """
        获取财经日历数据

        Returns:
            日历事件列表响应
        """
        return self.call_tool('list_calendar', {})

    def get_high_importance(self) -> List[CalendarEvent]:
        """
        获取高重要性事件（星级 >= 3）

        Returns:
            高重要性事件列表
        """
        result = self.list()
        events = result.get('data', [])

        high_events = []
        for event in events:
            star_str = event.get('star', '0')
            # 提取星级数字
            try:
                star = int(''.join(filter(str.isdigit, star_str))) or 0
            except (ValueError, TypeError):
                star = 0

            if star >= 3:
                high_events.append(event)

        return high_events

    def search(self, keyword: str) -> List[CalendarEvent]:
        """
        按关键词筛选事件

        Args:
            keyword: 搜索关键词

        Returns:
            匹配的事件列表
        """
        result = self.list()
        events = result.get('data', [])
        keyword_lower = keyword.lower()

        return [
            event for event in events
            if keyword_lower in event.get('title', '').lower()
        ]

    @staticmethod
    def _get_star_level(star_str: str) -> str:
        """获取星级标签"""
        return STAR_LABELS.get(star_str, star_str)

    @staticmethod
    def _format_star(star_str: str) -> str:
        """格式化星级显示"""
        try:
            star = int(''.join(filter(str.isdigit, star_str))) or 0
            return '★' * star
        except (ValueError, TypeError):
            return star_str

    @staticmethod
    def format_event(event: CalendarEvent) -> str:
        """格式化单个日历事件为可读字符串"""
        star = event.get('star', '0')
        star_display = CalendarClient._format_star(star)
        star_label = CalendarClient._get_star_level(star)

        lines = [
            f"[{event.get('pub_time', '')}] {event.get('title', '')} ({star_display} {star_label})",
            f"前值: {event.get('previous', 'N/A')} | "
            f"预期: {event.get('consensus', 'N/A')} | "
            f"实际: {event.get('actual', 'N/A')}",
        ]

        if event.get('revised'):
            lines.append(f"修正: {event.get('revised')}")

        if event.get('affect_txt'):
            lines.append(f"影响: {event.get('affect_txt')}")

        return '\n'.join(lines)

    @staticmethod
    def format_calendar(calendar: CalendarResult) -> str:
        """格式化日历列表为可读字符串"""
        events = calendar.get('data', [])
        return '\n\n'.join(
            CalendarClient.format_event(event) for event in events
        )

    @staticmethod
    def format_high_importance(events: List[CalendarEvent]) -> str:
        """格式化高重要性事件列表"""
        if not events:
            return '没有找到高重要性的财经事件'

        header = f"重要财经事件 ({len(events)} 项)\n{'=' * 40}\n"
        return header + '\n\n'.join(
            CalendarClient.format_event(event) for event in events
        )
