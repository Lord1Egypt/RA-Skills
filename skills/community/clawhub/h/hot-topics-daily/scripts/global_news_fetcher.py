#!/usr/bin/env python3
"""
国际新闻获取模块
支持 Currents API, GNews
为 hot-topics-daily 添加国际新闻源
"""

import os
import requests
from datetime import datetime
from typing import Optional, Dict, List, Any

class GlobalNewsFetcher:
    """国际新闻获取器"""

    def __init__(self):
        self.currents_key = os.getenv('CURRENTS_API_KEY')
        self.gnews_key = os.getenv('GNEWS_API_KEY')

        self.CURRENTS_URL = "https://api.currentsapi.services/v1"
        self.GNEWS_URL = "https://gnews.io/api/v4"

    def get_world_news_currents(self, limit: int = 10) -> Optional[List[Dict]]:
        """
        使用 Currents API 获取国际新闻
        免费额度: 200 次/天
        """
        if not self.currents_key:
            return None

        try:
            url = f"{self.CURRENTS_URL}/latest-news"
            params = {
                "language": "en",
                "country": "US,GB,JP,KR",  # 美英日韩
                "limit": limit,
                "apiKey": self.currents_key
            }

            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if "news" in data:
                return [{
                    "title": article["title"],
                    "description": article.get("description", "")[:100],
                    "url": article["url"],
                    "source": article.get("author", "Unknown"),
                    "published": article.get("published", ""),
                    "category": article.get("category", ["general"])[0] if article.get("category") else "general"
                } for article in data["news"]]
        except Exception as e:
            print(f"Currents API error: {e}")

        return None

    def get_tech_headlines_gnews(self, limit: int = 10) -> Optional[List[Dict]]:
        """
        使用 GNews 获取科技头条
        免费额度: 100 次/天
        """
        if not self.gnews_key:
            return None

        try:
            url = f"{self.GNEWS_URL}/top-headlines"
            params = {
                "topic": "technology",
                "lang": "en",
                "country": "us",
                "max": limit,
                "token": self.gnews_key
            }

            response = requests.get(url, params=params, timeout=10)
            data = response.json()

            if "articles" in data:
                return [{
                    "title": article["title"],
                    "description": article.get("description", "")[:100],
                    "url": article["url"],
                    "source": article.get("source", {}).get("name", ""),
                    "published": article.get("publishedAt", ""),
                    "image": article.get("image", "")
                } for article in data["articles"]]
        except Exception as e:
            print(f"GNews error: {e}")

        return None

    def get_global_hot_topics(self) -> Dict[str, List[Dict]]:
        """
        获取全球热门话题（聚合多源）
        """
        result = {
            "world_news": [],
            "tech_news": [],
            "timestamp": datetime.now().isoformat()
        }

        # 国际新闻
        world_news = self.get_world_news_currents(15)
        if world_news:
            result["world_news"] = world_news

        # 科技头条
        tech_news = self.get_tech_headlines_gnews(10)
        if tech_news:
            result["tech_news"] = tech_news

        return result


def format_for_discord(news_list: List[Dict], emoji: str = "🌍") -> str:
    """
    格式化为 Discord 消息
    """
    if not news_list:
        return ""

    lines = [f"{emoji} **国际新闻**\n"]

    for i, news in enumerate(news_list[:10], 1):
        title = news["title"][:50] + "..." if len(news["title"]) > 50 else news["title"]
        source = news.get("source", "")
        lines.append(f"{i}. {title}")
        if source:
            lines.append(f"   📰 {source}")

    return "\n".join(lines)


def main():
    """测试入口"""
    fetcher = GlobalNewsFetcher()

    print("=== 国际新闻 ===")
    news = fetcher.get_global_hot_topics()

    if news["world_news"]:
        print(format_for_discord(news["world_news"], "🌍"))
    else:
        print("未获取到国际新闻（可能需要配置 CURRENTS_API_KEY）")

    if news["tech_news"]:
        print(format_for_discord(news["tech_news"], "💻"))
    else:
        print("未获取到科技新闻（可能需要配置 GNEWS_API_KEY）")


if __name__ == "__main__":
    main()
