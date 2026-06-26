#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选题专家 v2.0 - 基于 TrendRadar
通过 TrendRadar 的 RSS 订阅获取全网热点
"""

import json
import feedparser
import requests
from datetime import datetime
import sys
from pathlib import Path

# 添加脚本目录到路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from topic_database import TopicDatabase


class TrendRadarIntegration:
    """TrendRadar 集成"""
    
    def __init__(self, trendradar_url="http://localhost:8000"):
        """
        Args:
            trendradar_url: TrendRadar 服务地址
        """
        self.base_url = trendradar_url
        self.db = TopicDatabase()
    
    def fetch_from_rss(self, platform="all"):
        """
        从 TrendRadar RSS 获取热点
        
        Args:
            platform: 平台名称（weibo/zhihu/douyin/xiaohongshu/bilibili/all）
        """
        try:
            # TrendRadar RSS 地址
            rss_url = f"{self.base_url}/rss/{platform}"
            
            print(f"📡 正在获取 {platform} 热点...", file=sys.stderr)
            
            feed = feedparser.parse(rss_url)
            
            hot_list = []
            for entry in feed.entries:
                hot_list.append({
                    "title": entry.get('title', ''),
                    "url": entry.get('link', ''),
                    "summary": entry.get('summary', ''),
                    "published": entry.get('published', ''),
                    "source": platform,
                    "platform": platform
                })
            
            print(f"   ✓ {len(hot_list)} 条", file=sys.stderr)
            return hot_list
            
        except Exception as e:
            print(f"[{platform}] 获取失败: {e}", file=sys.stderr)
            return []
    
    def fetch_all_platforms(self):
        """获取所有平台热点"""
        platforms = [
            "weibo",        # 微博
            "zhihu",        # 知乎
            "douyin",       # 抖音
            "xiaohongshu",  # 小红书
            "bilibili",     # B站
            "toutiao",      # 今日头条
            "baidu",        # 百度
            "36kr",         # 36氪
            "ithome",       # IT之家
            "github",       # GitHub
        ]
        
        all_cs = []
        
        for platform in platforms:
            topics = self.fetch_from_rss(platform)
            all_topics.extend(topics)
        
        return all_topics
    
    def filter_ai_related(self, topics):
        """筛选 AI 相关热点"""
        ai_keywords = [
            'AI', '人工智能', 'ChatGPT', 'GPT', 'Claude', '大模型', 
            'OpenAI', '智能', '机器学习', '深度学习', 'LLM',
            '效率工具', '自动化', 'Copilot', 'Gemini'
        ]
        
        filtered = []
        for topic in topics:
            title = topic.get('title', '')
            summary = topic.get('summary', '')
            
            if any(kw in title or kw in summary for kw in ai_keywords):
                filtered.append(topic)
        
        return filtered
    
    def score_and_store(self, topics):
        """打分并存储到数据库"""
        total_added = 0
        total_updated = 0
        high_score_topics = []
        
        for topic in topics:
            # 简单打分
            score = self.quick_score(topic)
            
            result = self.db.add_topic(
                title=topic['title'],
                source=topic['source'],
                source_url=topic.get('url', ''),
                hot_score=score.get('hot', 0),
                relevance_score=score.get('relevance', 0),
                total_score=score.get('total', 0),
                excerpt=topic.get('summary', ''),
                raw_data=topic
            )
            
            if result['status'] == 'added':
                total_added += 1
                
                # 收集高分选题
                if score['total'] >= 80:
                    high_score_topics.append({
                        'topic_id': result['topic_id'],
                        'title': topic['title'],
                        'score': score['total']
                    })
            
            elif result['status'] == 'updated':
                total_updated += 1
        
        return {
            'added': total_added,
            'updated': total_updated,
            'high_score': high_score_topics
        }
    
    def quick_score(self, topic):
        """快速打分"""
        title = topic.get('title', '')
        summary = topic.get('summary', '')
        
        # 相关度分（最重要）
        ai_core_keywords = ['AI', '人工智能', 'ChatGPT', 'GPT', 'Claude', 'OpenAI', '大模型']
        if any(kw in title for kw in ai_core_keywords):
            relevance_score = 25
        elif any(kw in summary for kw in ai_core_keywords):
            relevance_score = 20
        else:
            relevance_score = 10
        
        # 热度分（基于平台）
        hot_platforms = ['weibo', 'zhihu', 'douyin', 'xiaohongshu']
        if topic.get('source') in hot_platforms:
            hot_score = 25
        else:
            hot_score = 15
        
        # 时效性、可写性、差异化
        timeliness_score = 20
        writability_score = 15 if len(summary) > 50 else 10
        differentiation_score = 5
        
        total = hot_score + relevance_score + timeliness_score + writability_score + differentiation_score
        
        return {
            'hot': hot_score,
            'relevance': relevance_score,
            'timeliness': timeliness_score,
            'writability': writability_score,
            'differentiation': differentiation_score,
            'total': total
        }
    
    def run(self):
        """运行完整流程"""
        print(f"\n{'='*60}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 选题专家 v2.0 启动")
        print(f"{'='*60}\n")
        
        # 1. 获取全网热点
        print("🌐 正在从 TrendRadar 获取全网热点...\n")
        all_topics = self.fetch_all_platforms()
        print(f"\n✅ 共获取 {len(all_topics)} 条热点\n")
        
        # 2. 筛选 AI 相关
        print("🔍 筛选 AI 相关热点...")
        ai_topics = self.filter_ai_related(all_topics)
        print(f"   ✓ 筛选出 {len(ai_topics)} 条 AI 相关热点\n")
        
        # 3. 打分并存储
        print("📊 打分并存储到选题库...")
        result = self.score_and_store(ai_topics)
        print(f"   ✓ 新增 {result['added']} 条")
        print(f"   ✓ 更新 {result['updated']} 条")
        
        # 4. 高分选题推送
        if result['high_score']:
            print(f"\n🔥 发现 {len(result['high_score'])} 个高分选题：")
            for topic in result['high_score']:
                print(f"   • {topic['title']} ({topic['score']}分)")
        
        # 5. 统计
        stats = self.db.get_stats(days=1)
        print(f"\n📈 今日统计：")
        print(f"   总选题：{stats['total']} 个")
        print(f"   状态分布：{stats['status']}")
        print(f"   来源分布：{stats['sources'][:5]}")  # 只显示前5个
        
        print(f"\n{'='*60}")
        print(f"✅ 选题专家运行完成")
        print(f"{'='*60}\n")
    
    def close(self):
        """关闭资源"""
        self.db.close()


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="选题专家 v2.0 - 基于 TrendRadar")
    parser.add_argument("--trendradar-url", default="http://localhost:8000",
                       help="TrendRadar 服务地址")
    
    args = parser.parse_args()
    
    integration = TrendRadarIntegration(trendradar_url=args.trendradar_url)
    
    try:
        integration.run()
    finally:
        integration.close()


if __name__ == '__main__':
    main()
