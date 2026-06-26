#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选题专家主程序
整合所有模块，提供统一入口
"""

import sys
from pathlib import Path

# 添加项目根目录到路径
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

from core.database import TopicDatabase
from core.scorer import TopicScorer
from core.filter import TopicFilter
from utils.config import Config


class TopicExpert:
    """选题专家"""
    
    def __init__(self, config_file=None):
        """初始化"""
        self.config = Config(config_file)
        self.db = TopicDatabase()
        self.scorer = TopicScorer()
        self.filter = TopicFilter()
    
    def run(self):
        """运行一次完整流程"""
        print("🚀 选题专家启动\n")
        
        # 1. 获取数据源
        topics = self._fetch_topics()
        print(f"✅ 获取 {len(topics)} 条原始数据\n")
        
        # 2. 筛选
        filtered = self.filter.filter(topics)
        print(f"🔍 筛选后 {len(filtered)} 条\n")
        
        # 3. 打分
        scored = []
        for topic in filtered:
            score = self.scorer.score(topic)
            topic['score'] = score
            scored.append(topic)
        
        # 4. 存储
        result = self._store_topics(scored)
        print(f"💾 新增 {result['added']} 条，更新 {result['updated']} 条\n")
        
        # 5. 高分推送
        if result['high_score']:
            print(f"🔥 发现 {len(result['high_score'])} 个高分选题：")
            for t in result['high_score']:
                print(f"   • {t['title']} ({t['score']}分)")
        
        # 6. 统计
        stats = self.db.get_stats(days=1)
        print(f"\n📊 今日统计：")
        print(f"   总选题：{stats['total']} 个")
        print(f"   状态分布：{stats['status']}")
        
        print("\n✅ 运行完成")
    
    def _fetch_topics(self):
        """获取选题数据"""
        from sources import SourceManager
        
        print("📡 正在获取数据...\n")
        manager = SourceManager(self.config.config)
        topics = manager.fetch_all()
        
        return topics
    
    def _store_topics(self, topics):
        """存储选题到数据库"""
        added = 0
        updated = 0
        high_score = []
        
        for topic in topics:
            score = topic.get('score', {})
            
            result = self.db.add_topic(
                title=topic['title'],
                source=topic.get('source', ''),
                source_url=topic.get('url', ''),
                hot_score=score.get('hot', 0),
                relevance_score=score.get('relevance', 0),
                total_score=score.get('total', 0),
                excerpt=topic.get('summary', ''),
                raw_data=topic
            )
            
            if result['status'] == 'added':
                added += 1
                if score.get('total', 0) >= self.config.get('push_immediately_score', 80):
                    high_score.append({
                        'topic_id': result['topic_id'],
                        'title': topic['title'],
                        'score': score['total']
                    })
            elif result['status'] == 'updated':
                updated += 1
        
        return {'added': added, 'updated': updated, 'high_score': high_score}
    
    def close(self):
        """关闭资源"""
        self.db.close()


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="选题专家系统")
    parser.add_argument("--config", help="配置文件路径")
    
    args = parser.parse_args()
    
    expert = TopicExpert(config_file=args.config)
    
    try:
        expert.run()
    finally:
        expert.close()


if __name__ == '__main__':
    main()
