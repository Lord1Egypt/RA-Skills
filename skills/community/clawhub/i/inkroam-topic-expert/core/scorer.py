#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选题打分模块
5维度评分：热度、相关度、时效性、可写性、差异化
"""


class TopicScorer:
    """选题打分器"""
    
    def __init__(self, config=None):
        """
        Args:
            config: 配置字典，包含权重等参数
        """
        self.config = config or self._default_config()
    
    def _default_config(self):
        """默认配置"""
        return {
            'weights': {
                'hot': 0.30,
                'relevance': 0.25,
                'timeliness': 0.20,
                'writability': 0.15,
                'differentiation': 0.10
            },
            'keywords': {
                'core': ['AI', '人工智能', 'ChatGPT', 'GPT', 'Claude', 'OpenAI', '大模型'],
                'related': ['效率', '工具', '自动化', '智能', '机器学习'],
                'industry': ['科技', '互联网', '创业', '产品']
            }
        }
    
    def score(self, topic):
        """
        对选题进行综合打分
        
        Args:
            topic: 选题字典 {title, url, summary, hot, source, ...}
        
        Returns:
            dict: {hot, relevance, timeliness, writability, differentiation, total}
        """
        scores = {
            'hot': self._score_hot(topic),
            'relevance': self._score_relevance(topic),
            'timeliness': self._score_timeliness(topic),
            'writability': self._score_writability(topic),
            'differentiation': self._score_differentiation(topic)
        }
        
        scores['total'] = sum(scores.values())
        return scores
    
    def _score_hot(self, topic):
        """热度分（满分30）"""
        hot = topic.get('hot', 0)
        source = topic.get('source', '')
        
        # 根据热度值打分
        if isinstance(hot, int):
            if hot > 100000:
                return 30
            elif hot > 50000:
                return 25
            elif hot > 10000:
                return 20
            else:
                return 15
        
        # 根据平台打分
        hot_platforms = ['weibo', 'zhihu', 'douyin', 'xiaohongshu']
        if source in hot_platforms:
            return 25
        
        return 15
    
    def _score_relevance(self, topic):
        """相关度分（满分25）"""
        title = topic.get('title', '')
        summary = topic.get('summary', '')
        
        keywords = self.config['keywords']
        
        # 核心关键词匹配（每个10分，最多20分）
        for kw in keywords['core']:
            if kw in title:
                return 25  # 标题包含核心词，直接给满分
        
        # 摘要包含核心词
        for kw in keywords['core']:
            if kw in summary:
                return 20
        
        # 相关关键词匹配
        score = 0
        for kw in keywords['related']:
            if kw in title or kw in summary:
                score += 5
        
        # 行业关键词匹配
        for kw in keywords['industry']:
            if kw in title or kw in summary:
                score += 3
        
        return min(score, 25)
    
    def _score_timeliness(self, topic):
        """时效性分（满分20）"""
        # 所有热榜数据都是实时的，给满分
        return 20
    
    def _score_writability(self, topic):
        """可写性分（满分15）"""
        title = topic.get('title', '')
        summary = topic.get('summary', '')
        
        score = 5
        
        # 标题长度适中
        if 10 <= len(title) <= 30:
            score += 5
        
        # 有摘要加分
        if summary and len(summary) > 50:
            score += 5
        
        return min(score, 15)
    
    def _score_differentiation(self, topic):
        """差异化分（满分10）"""
        title = topic.get('title', '')
        
        score = 5
        
        # 包含数字
        if any(char.isdigit() for char in title):
            score += 2
        
        # 包含问号
        if '？' in title or '?' in title:
            score += 2
        
        # 包含"如何"、"怎么"等
        if any(kw in title for kw in ['如何', '怎么', '为什么', '什么']):
            score += 1
        
        return min(score, 10)


# 使用示例
if __name__ == '__main__':
    scorer = TopicScorer()
    
    # 测试选题
    topic = {
        'title': 'OpenAI多位负责人抗议辞职',
        'summary': 'OpenAI 公司内部出现重大人事变动...',
        'hot': 50000,
        'source': 'weibo'
    }
    
    scores = scorer.score(topic)
    print(f"选题：{topic['title']}")
    print(f"热度分：{scores['hot']}/30")
    print(f"相关度：{scores['relevance']}/25")
    print(f"时效性：{scores['timeliness']}/20")
    print(f"可写性：{scores['writability']}/15")
    print(f"差异化：{scores['differentiation']}/10")
    print(f"总分：{scores['total']}/100")
