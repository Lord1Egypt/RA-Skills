#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据源基类
所有数据源必须继承此类并实现 fetch() 方法
"""

from abc import ABC, abstractmethod
from datetime import datetime


class BaseSource(ABC):
    """数据源基类"""
    
    def __init__(self, name, platform_name):
        """
        Args:
            name: 数据源标识（如 weibo, zhihu）
            platform_name: 平台显示名称（如 微博, 知乎）
        """
        self.name = name
        self.platform_name = platform_name
        self.enabled = True
    
    @abstractmethod
    def fetch(self):
        """
        获取热点数据（子类必须实现）
        
        Returns:
            list: 选题列表，每个选题包含：
                - title: 标题（必填）
                - url: 链接（必填）
                - summary: 摘要（选填）
                - hot: 热度值（选填）
                - source: 数据源标识（自动填充）
                - platform: 平台名称（自动填充）
                - fetch_time: 获取时间（自动填充）
        """
        pass
    
    def _normalize_topic(self, topic):
        """标准化选题数据"""
        return {
            'title': topic.get('title', '').strip(),
            'url': topic.get('url', ''),
            'summary': topic.get('summary', ''),
            'hot': topic.get('hot', 0),
            'source': self.name,
            'platform': self.platform_name,
            'fetch_time': datetime.now().isoformat()
        }
    
    def fetch_with_error_handling(self):
        """带错误处理的获取方法"""
        if not self.enabled:
            return []
        
        try:
            topics = self.fetch()
            return [self._normalize_topic(t) for t in topics if t.get('title')]
        except Exception as e:
            print(f"[{self.platform_name}] 获取失败: {e}")
            return []


# 使用示例
if __name__ == '__main__':
    # 子类必须实现 fetch() 方法
    class ExampleSource(BaseSource):
        def __init__(self):
            super().__init__('example', '示例平台')
        
        def fetch(self):
            return [
                {'title': '测试标题1', 'url': 'https://example.com/1'},
                {'title': '测试标题2', 'url': 'https://example.com/2', 'hot': 1000}
            ]
    
    source = ExampleSource()
    topics = source.fetch_with_error_handling()
    print(f"获取 {len(topics)} 条")
    for t in topics:
        print(f"  - {t['title']} ({t['platform']})")
