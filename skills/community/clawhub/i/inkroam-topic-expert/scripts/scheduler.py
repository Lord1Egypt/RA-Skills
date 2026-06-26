#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
选题专家调度器
7×24小时运行，定时采集、打分、推送
"""

import json
import time
import sys
from pathlib import Path
from datetime import datetime
import subprocess

# 添加脚本目录到路径
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from topic_database import TopicDatabase
from multi_platform_crawler import MultiPlatformCrawler


class TopicScheduler:
    """选题调度器"""
    
    def __init__(self):
        self.db = TopicDatabase()
        self.crawler = MultiPlatformCrawler()
        self.config = self.load_config()
    
    def load_config(self):
        """加载配置"""
        config_file = SCRIPT_DIR.parent / "config.json"
        if config_file.exists():
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # 默认配置
        return {
            "min_score": 70,
            "max_daily_push": 5,
            "push_immediately_score": 80,
            "account_type": "AI资讯",
            "bijian_space_id": 4616
        }
    
    def fetch_and_store(self):
        """采集数据并存储到数据库"""
        print(f"\n{'='*60}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始数据采集")
        print(f"{'='*60}\n")
        
        # 采集数据
        results = self.crawler.fetch_all()
        
        # 打分并存储
        total_added = 0
        total_updated = 0
        
        for platform, topics in results.items():
            for topic in topics:
                # 简单打分（实际应该调用打分脚本）
                score = self.quick_score(topic)
                
                result = self.db.add_topic(
                    title=topic['title'],
                    source=topic['source'],
                    source_url=topic.get('url', ''),
                    hot_score=score.get('hot', 0),
                    relevance_score=score.get('relevance', 0),
                    total_score=score.get('total', 0),
                    excerpt=topic.get('excerpt', ''),
                    raw_data=topic
                )
                
                if result['status'] == 'added':
                    total_added += 1
                    
                    # 高分选题立即推送
                    if score['total'] >= self.config['push_immediately_score']:
                        print(f"🔥 发现高分选题（{score['total']}分）：{topic['title']}")
                        self.push_topic_immediately(result['topic_id'])
                
                elif result['status'] == 'updated':
                    total_updated += 1
        
        print(f"\n✅ 数据处理完成：新增 {total_added} 条，更新 {total_updated} 条")
        
        # 统计
        stats = self.db.get_stats(days=1)
        print(f"\n📊 今日统计：")
        print(f"   总选题：{stats['total']} 个")
        print(f"   状态分布：{stats['status']}")
        
        return total_added, total_updated
    
    def quick_score(self, topic):
        """快速打分（简化版）"""
        title = topic.get('title', '')
        hot = topic.get('hot', 0)
        
        # 热度分
        if isinstance(hot, int):
            if hot > 100000:
                hot_score = 30
            elif hot > 50000:
                hot_score = 25
            elif hot > 10000:
                hot_score = 20
            else:
                hot_score = 15
        else:
            hot_score = 15
        
        # 相关度分
        ai_keywords = ['AI', '人工智能', 'ChatGPT', 'GPT', 'Claude', 'OpenAI', '大模型']
        relevance_score = 0
        for kw in ai_keywords:
            if kw in title:
                relevance_score = 25
                break
        if relevance_score == 0:
            relevance_score = 10
        
        # 时效性、可写性、差异化
        timeliness_score = 20
        writability_score = 10
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
    
    def push_topic_immediately(self, topic_id):
        """立即推送高分选题"""
        # TODO: 调用 Telegram 推送
        print(f"   → 推送选题 ID: {topic_id}")
    
    def send_daily_report(self):
        """发送每日早报"""
        print(f"\n{'='*60}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 生成每日早报")
        print(f"{'='*60}\n")
        
        # 获取昨日高分选题
        pending = self.db.get_pending_topics(
            min_score=self.config['min_score'],
            limit=self.config['max_daily_push']
        )
        
        if not pending:
            print("⚠️  没有待推送的选题")
            return
        
        print(f"📋 今日推荐 {len(pending)} 个选题：\n")
        for idx, topic in enumerate(pending, 1):
            print(f"{idx}. {topic['title']} ({topic['source']}, {topic['total_score']}分)")
        
        # TODO: 调用 Telegram 推送每日早报
    
    def cleanup_old_data(self, days=30):
        """清理旧数据"""
        # TODO: 删除30天前的已处理选题
        pass
    
    def run_once(self):
        """运行一次完整流程"""
        try:
            self.fetch_and_store()
        except Exception as e:
            print(f"❌ 运行出错: {e}", file=sys.stderr)
            import traceback
            traceback.print_exc()
    
    def run_daemon(self):
        """守护进程模式（持续运行）"""
        print("🚀 选题专家调度器启动（守护进程模式）")
        print(f"   配置：最低分数 {self.config['min_score']}，每日最多推送 {self.config['max_daily_push']} 个\n")
        
        last_daily_report_date = None
        
        while True:
            try:
                # 每小时采集一次
                self.run_once()
                
                # 每天8点发送早报
                now = datetime.now()
                if now.hour == 8 and now.date() != last_daily_report_date:
                    self.send_daily_report()
                    last_daily_report_date = now.date()
                
                # 等待1小时
                print(f"\n⏰ 下次采集时间：{datetime.now().strftime('%H:%M:%S')} + 1小时")
                time.sleep(3600)
                
            except KeyboardInterrupt:
                print("\n\n👋 选题专家调度器已停止")
                break
            except Exception as e:
                print(f"\n❌ 运行出错: {e}", file=sys.stderr)
                import traceback
                traceback.print_exc()
                print("\n⏰ 5分钟后重试...")
                time.sleep(300)
    
    def close(self):
        """关闭资源"""
        self.db.close()


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="选题专家调度器")
    parser.add_argument("--mode", choices=["once", "daemon"], default="once",
                       help="运行模式：once=运行一次，daemon=守护进程")
    parser.add_argument("--daily-report", action="store_true",
                       help="发送每日早报")
    
    args = parser.parse_args()
    
    scheduler = TopicScheduler()
    
    try:
        if args.daily_report:
            scheduler.send_daily_report()
        elif args.mode == "once":
            scheduler.run_once()
        else:
            scheduler.run_daemon()
    finally:
        scheduler.close()


if __name__ == '__main__':
    main()
