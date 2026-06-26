#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
头条发布器 - 发布文章到头条（API方式）
支持从配置文件读取账号信息
"""

import requests
import json
import os
from datetime import datetime
from .cookie_manager import CookieManager
from .feishu_notifier import FeishuNotifier


class Publisher:
    """头条发布器"""

    def __init__(self, account_id=None, account_name=None, config_file=None):
        """
        初始化发布器

        Args:
            account_id: 头条账号ID（优先使用直接传入值）
            account_name: 头条账号名称
            config_file: 配置文件路径
        """
        # 从配置文件读取
        config = {}
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)

        self.account_id = account_id or config.get("account_id")
        self.account_name = account_name or config.get("account_name")

        # 初始化Cookie管理器
        cookie_path = config.get("cookie_file")
        self.cookie_manager = CookieManager(cookie_path=cookie_path)

        # 初始化飞书通知器
        self.feishu_notifier = FeishuNotifier(config_file=config_file)

        # 头条API配置
        self.base_url = "https://mp.toutiao.com"

        # 发布日志
        self.publish_log = []

    def get_topic_invitations(self):
        """
        获取话题邀请列表

        Returns:
            list: 话题邀请列表（按围观人数排序）
        """
        url = f"{self.base_url}/api/topic/invitation/list"
        headers = self.cookie_manager.get_headers()

        try:
            response = requests.get(url, headers=headers)
            data = response.json()

            if data.get("code") == 0:
                topics = data.get("data", {}).get("topics", [])

                # 按围观人数排序
                sorted_topics = sorted(
                    topics,
                    key=lambda x: x.get("view_count", 0),
                    reverse=True
                )

                return sorted_topics
            else:
                print(f"[发布器] 获取话题邀请失败: {data}")
                return []

        except Exception as e:
            print(f"[发布器] 获取话题邀请异常: {e}")
            return []

    def get_hot_topic(self):
        """
        获取最热门的话题

        Returns:
            dict: 最热门的话题
        """
        topics = self.get_topic_invitations()

        if topics:
            return topics[0]
        else:
            print("[发布器] 没有获取到话题邀请")
            return None

    def publish_article(self, article, images=None):
        """
        发布文章

        Args:
            article: 文章数据（包含标题、内容等）
            images: 配图列表

        Returns:
            dict: 发布结果
        """
        print(f"[发布器] 开始发布文章: {article['title']}")

        # 1. 准备发布数据
        publish_data = self._prepare_publish_data(article, images)

        # 2. 发布文章
        url = f"{self.base_url}/api/article/publish"
        headers = self.cookie_manager.get_headers()

        try:
            response = requests.post(url, json=publish_data, headers=headers)
            data = response.json()

            if data.get("code") == 0:
                article_url = data.get("data", {}).get("article_url", "")
                print(f"[发布器] 文章发布成功: {article_url}")

                # 记录发布日志
                log_entry = {
                    "title": article['title'],
                    "topic": article.get('topic', ''),
                    "url": article_url,
                    "status": "success",
                    "published_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                self.publish_log.append(log_entry)

                # 发送飞书通知
                self._send_success_notification(article, article_url)

                return {
                    "success": True,
                    "url": article_url,
                    "data": log_entry
                }
            else:
                error_msg = data.get("message", "未知错误")
                print(f"[发布器] 文章发布失败: {error_msg}")
                self._send_error_notification(article, error_msg)
                return {
                    "success": False,
                    "error": error_msg
                }

        except Exception as e:
            print(f"[发布器] 发布文章异常: {e}")
            self._send_error_notification(article, str(e))
            return {
                "success": False,
                "error": str(e)
            }

    def _prepare_publish_data(self, article, images):
        """准备发布数据"""
        data = {
            "title": article['title'],
            "content": article['content'],
            "article_type": "article",
            "abstract": article['content'][:100],
            "category": "情感",
            "tags": ["中年", "人生", "成长"],
            "is_original": True,
            "disclaimer": True,
            "account_id": self.account_id
        }

        if images:
            data["cover_images"] = [img.get('url') if isinstance(img, dict) else img for img in images]

        return data

    def _send_success_notification(self, article, article_url):
        """发送成功通知"""
        title = "文章发布成功"
        body = f"**标题**: {article['title']}\n"
        body += f"**话题**: {article.get('topic', '无')}\n"
        body += f"**链接**: {article_url}\n"
        body += f"**账号**: {self.account_name}"
        self.feishu_notifier.send_notification(title, body, "success")

    def _send_error_notification(self, article, error_msg):
        """发送失败通知"""
        title = "文章发布失败"
        body = f"**标题**: {article['title']}\n"
        body += f"**话题**: {article.get('topic', '无')}\n"
        body += f"**错误**: {error_msg}\n"
        body += f"**账号**: {self.account_name}"
        self.feishu_notifier.send_notification(title, body, "error")

    def get_publish_log(self):
        """获取发布日志"""
        return self.publish_log

    def save_publish_log(self, log_path):
        """保存发布日志到文件"""
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(self.publish_log, f, ensure_ascii=False, indent=2)
        print(f"[发布器] 发布日志已保存到: {log_path}")


def main():
    """测试发布器"""
    # 查找配置文件
    config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config")
    config_file = os.path.join(config_dir, "account_config.json")

    if os.path.exists(config_file):
        publisher = Publisher(config_file=config_file)
    else:
        print("[发布器] 未找到配置文件，请先配置 config/account_config.json")
        return

    # 获取热门话题
    hot_topic = publisher.get_hot_topic()
    print(f"最热门的话题: {hot_topic}")

    # 测试发布文章
    if hot_topic:
        article = {
            "title": f"关于{hot_topic['title']}的思考",
            "content": f"今天刷到一个话题：{hot_topic['title']}\n\n这篇文章的内容...",
            "topic": hot_topic['title']
        }
        result = publisher.publish_article(article)
        print(f"发布结果: {result}")


if __name__ == "__main__":
    main()
