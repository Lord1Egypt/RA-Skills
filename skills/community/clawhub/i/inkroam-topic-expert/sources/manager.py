#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据源管理器
统一管理所有数据源，方便添加/启用/禁用
"""

from .tophub import TophubSource
from .weibo import WeiboSource
from .zhihu import ZhihuSource
from .github import GitHubSource
from .xiaohongshu import XiaohongshuSource
from .kr36 import Kr36Source
from .huxiu import HuxiuSource
from .ithome import IthomeSource
from .baidu import BaiduSource


class SourceManager:
    """数据源管理器"""
    
    def __init__(self, config=None):
        """
        Args:
            config: 配置字典，可以控制哪些数据源启用
        """
        self.config = config or {}
        self.sources = self._init_sources()
    
    def _init_sources(self):
        """
        初始化所有数据源
        
        添加新数据源只需3步：
        1. 在 sources/ 目录创建新文件（如 douyin.py）
        2. 继承 BaseSource 并实现 fetch() 方法
        3. 在这里导入并添加到列表
        """
        sources = [
            TophubSource(),         # TopHub聚合（主数据源，最稳定）
            WeiboSource(),          # 微博热搜
            ZhihuSource(),          # 知乎热榜
            GitHubSource(),         # GitHub Trending
            BaiduSource(),          # 百度热搜
            Kr36Source(),           # 36氪
            HuxiuSource(),          # 虎嗅
            IthomeSource(),         # IT之家
            XiaohongshuSource(),    # 小红书（待接入）
            
            # 添加新数据源示例：
            # DouyinSource(),       # 抖音
            # TwitterSource(),      # Twitter
            # MaimaiSource(),       # 脉脉
        ]
        
        # 根据配置启用/禁用数据源
        for source in sources:
            enabled = self.config.get(f'sources.{source.name}.enabled', True)
            source.enabled = enabled
        
        return sources
    
    def fetch_all(self):
        """获取所有启用的数据源"""
        all_topics = []
        
        for source in self.sources:
            if source.enabled:
                topics = source.fetch_with_error_handling()
                all_topics.extend(topics)
                print(f"  [{source.platform_name}] {len(topics)} 条")
        
        return all_topics
    
    def get_source(self, name):
        """获取指定数据源"""
        for source in self.sources:
            if source.name == name:
                return source
        return None
    
    def list_sources(self):
        """列出所有数据源"""
        return [
            {
                'name': s.name,
                'platform': s.platform_name,
                'enabled': s.enabled
            }
            for s in self.sources
        ]


# 使用示例
if __name__ == '__main__':
    print("📡 数据源管理器测试\n")
    
    manager = SourceManager()
    
    # 列出所有数据源
    print("可用数据源：")
    for s in manager.list_sources():
        status = "✅" if s['enabled'] else "❌"
        print(f"  {status} {s['platform']} ({s['name']})")
    
    print("\n开始获取数据...\n")
    
    # 获取所有数据
    topics = manager.fetch_all()
    
    print(f"\n✅ 共获取 {len(topics)} 条\n")
    
    # 统计各平台数量
    from collections import Counter
    platform_counts = Counter(t['platform'] for t in topics)
    print("各平台数量：")
    for platform, count in platform_counts.most_common():
        print(f"  {platform}: {count} 条")
    
    # 显示前5条
    print("\n前5条热点：")
    for i, topic in enumerate(topics[:5], 1):
        print(f"{i}. [{topic['platform']}] {topic['title']}")
