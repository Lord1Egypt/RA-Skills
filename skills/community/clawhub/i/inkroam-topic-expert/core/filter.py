#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选题筛选模块
根据关键词、分数等条件筛选选题
"""


class TopicFilter:
    """选题筛选器"""
    
    def __init__(self, config=None):
        """
        Args:
            config: 配置字典
        """
        self.config = config or self._default_config()
    
    def _default_config(self):
        """默认配置"""
        return {
            'keywords': {
                'include': ['AI', '人工智能', 'ChatGPT', 'GPT', 'Claude', 'OpenAI', '大模型'],
                'exclude': ['广告', '营销', '推广']
            },
            'min_score': 70,
            'platforms': ['weibo', 'zhihu', 'douyin', 'xiaohongshu', 'bilibili']
        }
    
    def filter(self, topics):
        """
        筛选选题列表
        
        Args:
            topics: 选题列表
        
        Returns:
            list: 筛选后的选题列表
        """
        filtered = []
        
        for topic in topics:
            if self._should_include(topic):
                filtered.append(topic)
        
        return filtered
    
    def _should_include(self, topic):
        """判断是否应该包含该选题"""
        title = topic.get('title', '')
        summary = topic.get('summary', '')
        content = f"{title} {summary}"
        
        # 检查排除关键词
        for kw in self.config['keywords']['exclude']:
            if kw in content:
                return False
        
        # 检查包含关键词
        has_include_keyword = False
        for kw in self.config['keywords']['include']:
            if kw in content:
                has_include_keyword = True
                break
        
        return has_include_keyword
    
    def filter_by_score(self, topics, min_score=None):
        """根据分数筛选"""
        min_score = min_score or self.config['min_score']
        return [t for t in topics if t.get('score', {}).get('total', 0) >= min_score]
    
    def filter_by_platform(self, topics, platforms=None):
        """根据平台筛选"""
        platforms = platforms or seconfig['platforms']
        return [t for t in topics if t.get('source') in platforms]


# 使用示例
if __name__ == '__main__':
    filter = TopicFilter()
    
    topics = [
        {'title': 'OpenAI 发布新模型', 'summary': '...', 'source': 'weibo'},
        {'title': '某品牌广告推广', 'summary': '...', 'source': 'weibo'},
        {'title': 'AI 工具使用技巧', 'summary': '...', 'source': 'zhihu'},
    ]
    
    filtered = filter.filter(topics)
    print(f"原始：{len(topics)} 条")
    print(f"筛选后：{len(filtered)} 条")
    for t in filtered:
        print(f"  - {t['title']}")
