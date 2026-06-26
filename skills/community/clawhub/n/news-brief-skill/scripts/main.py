#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
News Brief Skill - Main Scheduler
核心调度器：协调各模块工作，执行每日新闻简报流程
"""

import os
import sys
import json
import logging
from datetime import datetime, time
from pathlib import Path

# 添加项目路径到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scripts.news_fetcher import NewsFetcher
from scripts.summarizer import NewsSummarizer  
from scripts.pusher import NewsPusher
from scripts.feedback_handler import FeedbackHandler
from scripts.config_manager import ConfigManager

class NewsBriefScheduler:
    """新闻简报主调度器"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        """设置日志"""
        log_dir = project_root / "data" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"news_brief_{datetime.now().strftime('%Y%m%d')}.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        return logging.getLogger(__name__)
    
    def daily_briefing_flow(self, user_id=None):
        """
        每日新闻简报主流程
        
        Args:
            user_id: 用户ID，如果为None则处理所有用户
        """
        try:
            self.logger.info("开始每日新闻简报流程")
            
            # 1. 获取用户列表
            if user_id:
                users = [user_id]
            else:
                users = self.config_manager.get_all_users()
            
            for uid in users:
                try:
                    self.logger.info(f"处理用户 {uid}")
                    
                    # 2. 加载用户配置
                    user_config = self.config_manager.load_user_config(uid)
                    if not user_config:
                        self.logger.warning(f"用户 {uid} 配置不存在，跳过")
                        continue
                    
                    # 3. 执行新闻获取
                    fetcher = NewsFetcher(uid, user_config)
                    news_items = fetcher.fetch_news()
                    
                    if not news_items:
                        self.logger.warning(f"用户 {uid} 未获取到新闻")
                        continue
                    
                    # 4. 生成摘要简报
                    summarizer = NewsSummarizer(uid, user_config)
                    brief_content = summarizer.generate_brief(news_items)
                    
                    # 5. 推送简报
                    pusher = NewsPusher(uid, user_config)
                    push_result = pusher.push_brief(brief_content)
                    
                    # 6. 触发反馈交互
                    if push_result['success']:
                        feedback_handler = FeedbackHandler(uid, user_config)
                        feedback_handler.trigger_feedback_prompt()
                        
                    self.logger.info(f"用户 {uid} 简报流程完成")
                    
                except Exception as e:
                    self.logger.error(f"处理用户 {uid} 时出错: {e}")
                    continue
                    
        except Exception as e:
            self.logger.error(f"每日简报流程出错: {e}")
            raise
    
    def handle_user_feedback(self, user_id, feedback_text):
        """
        处理用户反馈
        
        Args:
            user_id: 用户ID
            feedback_text: 用户反馈内容
        """
        try:
            feedback_handler = FeedbackHandler(user_id)
            feedback_handler.process_feedback(feedback_text)
            self.logger.info(f"用户 {user_id} 反馈处理完成")
        except Exception as e:
            self.logger.error(f"处理用户 {user_id} 反馈时出错: {e}")
            raise
    
    def optimize_brief_preview(self, user_id, optimization_type, new_config):
        """
        生成优化预览版简报
        
        Args:
            user_id: 用户ID
            optimization_type: 优化类型
            new_config: 新配置
        """
        try:
            # 临时应用新配置获取新闻
            fetcher = NewsFetcher(user_id, new_config)
            news_items = fetcher.fetch_news()
            
            if news_items:
                summarizer = NewsSummarizer(user_id, new_config)
                preview_content = summarizer.generate_brief(news_items)
                
                # 推送预览
                pusher = NewsPusher(user_id, new_config)
                pusher.push_preview(preview_content, optimization_type)
                
            self.logger.info(f"用户 {user_id} 优化预览生成完成")
            
        except Exception as e:
            self.logger.error(f"生成用户 {user_id} 优化预览时出错: {e}")
            raise

def main():
    """主函数"""
    scheduler = NewsBriefScheduler()
    
    # 命令行参数处理
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "daily":
            # 执行每日简报
            user_id = sys.argv[2] if len(sys.argv) > 2 else None
            scheduler.daily_briefing_flow(user_id)
        elif command == "feedback":
            # 处理用户反馈
            user_id = sys.argv[2]
            feedback_text = " ".join(sys.argv[3:])
            scheduler.handle_user_feedback(user_id, feedback_text)
        elif command == "preview":
            # 生成优化预览
            user_id = sys.argv[2]
            opt_type = sys.argv[3]
            config_file = sys.argv[4]
            with open(config_file, 'r', encoding='utf-8') as f:
                new_config = json.load(f)
            scheduler.optimize_brief_preview(user_id, opt_type, new_config)
    else:
        print("Usage: python main.py [daily|feedback|preview] [args...]")

if __name__ == "__main__":
    main()