#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时任务脚本 - 支持定时发布文章和微头条
"""

import sys
import os
import time
import json
import argparse
import schedule

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

from core.article_generator import ArticleGenerator
from core.publisher import Publisher
from core.feishu_notifier import FeishuNotifier


def load_config():
    """加载配置文件"""
    config_path = os.path.join(ROOT_DIR, "config", "account_config.json")
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def load_automation_config():
    """加载自动化配置"""
    auto_path = os.path.join(ROOT_DIR, "config", "automation_settings.json")
    if os.path.exists(auto_path):
        with open(auto_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "article": {"enabled": True, "schedule": "0 * 6-23 * * *"},
        "weitoutiao": {"enabled": True, "schedule": "0 * 6-23 * * *", "auto_select_topic": True}
    }


def run_article_task(config):
    """执行文章发布任务"""
    from datetime import datetime
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行文章发布任务...")

    try:
        publisher = Publisher(config_file=os.path.join(ROOT_DIR, "config", "account_config.json"))
        article_gen = ArticleGenerator()
        notifier = FeishuNotifier(config_file=os.path.join(ROOT_DIR, "config", "account_config.json"))

        # 获取热门话题
        hot_topic = publisher.get_hot_topic()
        if not hot_topic:
            print("[定时] 没有获取到话题邀请，跳过")
            return

        topic_title = hot_topic.get('title', '未知话题')
        topic_views = hot_topic.get('view_count', 0)
        print(f"[定时] 热门话题: {topic_title} (围观: {topic_views})")

        # 生成文章
        article = article_gen.generate_article(topic_title, view_count=topic_views)
        print(f"[定时] 文章标题: {article['title']}")

        # 发布文章
        result = publisher.publish_article(article)

        if result['success']:
            print(f"[定时] 发布成功!")
            notifier.send_notification(
                title="定时文章发布成功",
                body=f"标题: {article['title']}\n话题: {topic_title}",
                notification_type="success"
            )
        else:
            print(f"[定时] 发布失败: {result.get('error')}")
            notifier.send_notification(
                title="定时文章发布失败",
                body=f"错误: {result.get('error')}",
                notification_type="error"
            )

    except Exception as e:
        print(f"[定时] 执行异常: {e}")
        import traceback
        traceback.print_exc()


def main():
    parser = argparse.ArgumentParser(description="头条定时发布脚本")
    parser.add_argument("--type", choices=["article", "weitoutiao", "both"], default="article",
                        help="发布类型（article/weitoutiao/both）")
    parser.add_argument("--now", action="store_true", help="立即执行一次")
    args = parser.parse_args()

    config = load_config()
    if not config:
        print("[错误] 请先配置 config/account_config.json")
        sys.exit(1)

    auto_config = load_automation_config()

    print("=" * 60)
    print(f"头条定时发布器启动 (类型: {args.type})")
    print(f"账号: {config.get('account_name')}")
    print("=" * 60)

    # 配置定时任务
    if args.type in ("article", "both"):
        if auto_config["article"].get("enabled", True):
            schedule.every().hour.do(lambda: run_article_task(config))
            print("文章定时任务: 每小时执行一次")

    if args.now:
        print("立即执行一次...")
        run_article_task(config)

    # 持续运行
    print("\n定时器已启动，等待下一次执行...")
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()
