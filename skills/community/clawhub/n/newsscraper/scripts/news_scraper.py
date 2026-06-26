#!/usr/bin/env python3
"""
新闻数据爬取脚本
支持 API 和直接爬取两种方式获取新闻数据

使用方法:
    # 使用 API 方式获取多平台热点
    python news_scraper.py --mode api --platforms weibo,zhihu --limit 20

    # 直接爬取特定平台
    python news_scraper.py --mode scrape --platform weibo --limit 10

    # 根据主题爬取新闻
    python news_scraper.py --mode scrape --keyword "人工智能" --platforms weibo,zhihu --limit 15
"""

import requests
import json
import time
import argparse
from datetime import datetime
from typing import List, Dict, Optional
from bs4 import BeautifulSoup


class NewsScraper:
    """新闻爬虫类,支持多种平台和数据获取方式"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def scrape_by_api(self, platforms: List[str], limit: int = 20) -> List[Dict]:
        """
        使用 API 方式获取多平台热点数据

        Args:
            platforms: 平台列表,如 ['weibo', 'zhihu']
            limit: 每个平台获取的新闻数量

        Returns:
            新闻数据列表
        """
        all_news = []

        # 使用全网热榜聚合 API (uapis.cn)
        api_url = "https://uapis.cn/api/get-misc-hotboard"

        for platform in platforms:
            try:
                print(f"正在通过 API 获取 {platform} 热点...")

                # 根据平台映射 API 参数
                platform_map = {
                    'weibo': 'weibo',
                    'zhihu': 'zhihu',
                    'bilibili': 'bilibili',
                    'douyin': 'douyin',
                    'toutiao': 'toutiao',
                    'tencent': 'tencent',
                    'thepaper': 'thepaper'
                }

                api_platform = platform_map.get(platform, platform)
                params = {
                    'name': api_platform,
                    'limit': limit
                }

                response = self.session.get(api_url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()

                if data.get('code') == 200 and data.get('data'):
                    news_list = data['data'][:limit]
                    for item in news_list:
                        news_item = {
                            'title': item.get('title', ''),
                            'platform': platform,
                            'url': item.get('url', ''),
                            'hot': item.get('hot', 0),
                            'timestamp': datetime.now().isoformat(),
                            'summary': ''  # 稍后生成摘要
                        }
                        all_news.append(news_item)
                    print(f"✓ 从 {platform} 获取了 {len(news_list)} 条热点")
                else:
                    print(f"✗ {platform} API 返回数据格式异常")

                # 礼貌性延时
                time.sleep(1)

            except Exception as e:
                print(f"✗ 获取 {platform} 失败: {str(e)}")

        return all_news

    def scrape_by_direct(self, platform: str, keyword: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """
        直接爬取新闻网站获取数据

        Args:
            platform: 平台名称
            keyword: 搜索关键词(可选)
            limit: 获取的新闻数量

        Returns:
            新闻数据列表
        """
        print(f"正在直接爬取 {platform}...")
        all_news = []

        if platform == 'weibo':
            all_news = self._scrape_weibo(keyword, limit)
        elif platform == 'zhihu':
            all_news = self._scrape_zhihu(keyword, limit)
        elif platform == 'bilibili':
            all_news = self._scrape_bilibili(keyword, limit)
        elif platform == 'tencent':
            all_news = self._scrape_tencent(keyword, limit)
        elif platform == 'thepaper':
            all_news = self._scrape_thepaper(keyword, limit)
        else:
            print(f"✗ 暂不支持直接爬取平台: {platform}")

        return all_news

    def _scrape_weibo(self, keyword: Optional[str], limit: int) -> List[Dict]:
        """爬取微博热搜"""
        news_list = []

        try:
            url = "https://s.weibo.com/top/summary"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 微博热搜列表
            hot_items = soup.find_all('a', {'href': lambda x: x and '/weibo?q=' in x})

            for i, item in enumerate(hot_items[:limit]):
                title = item.get_text().strip()
                url = "https://s.weibo.com" + item.get('href', '')

                if title:
                    news_item = {
                        'title': title,
                        'platform': 'weibo',
                        'url': url,
                        'rank': i + 1,
                        'timestamp': datetime.now().isoformat(),
                        'summary': ''
                    }
                    news_list.append(news_item)

            print(f"✓ 从微博获取了 {len(news_list)} 条热搜")

        except Exception as e:
            print(f"✗ 爬取微博失败: {str(e)}")

        return news_list

    def _scrape_zhihu(self, keyword: Optional[str], limit: int) -> List[Dict]:
        """爬取知乎热榜"""
        news_list = []

        try:
            url = "https://www.zhihu.com/hot"
            headers = {
                'User-Agent': self.headers['User-Agent'],
                'Referer': 'https://www.zhihu.com/'
            }
            response = self.session.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 知乎热榜项
            hot_items = soup.find_all('div', {'class': 'HotItem'})

            for i, item in enumerate(hot_items[:limit]):
                title_elem = item.find('h2', {'class': 'HotItem-title'})
                link_elem = item.find('a')

                if title_elem:
                    title = title_elem.get_text().strip()
                    url = link_elem.get('href', '')
                    if url and not url.startswith('http'):
                        url = 'https://www.zhihu.com' + url

                    news_item = {
                        'title': title,
                        'platform': 'zhihu',
                        'url': url,
                        'rank': i + 1,
                        'timestamp': datetime.now().isoformat(),
                        'summary': ''
                    }
                    news_list.append(news_item)

            print(f"✓ 从知乎获取了 {len(news_list)} 条热榜")

        except Exception as e:
            print(f"✗ 爬取知乎失败: {str(e)}")

        return news_list

    def _scrape_bilibili(self, keyword: Optional[str], limit: int) -> List[Dict]:
        """爬取B站热门"""
        news_list = []

        try:
            url = "https://www.bilibili.com/v/popular/all"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # B站热门视频项
            video_items = soup.find_all('a', {'class': 'video-title'})

            for i, item in enumerate(video_items[:limit]):
                title = item.get('title', '').strip()
                url = "https:" + item.get('href', '') if item.get('href', '').startswith('//') else item.get('href', '')

                if title:
                    news_item = {
                        'title': title,
                        'platform': 'bilibili',
                        'url': url,
                        'rank': i + 1,
                        'timestamp': datetime.now().isoformat(),
                        'summary': ''
                    }
                    news_list.append(news_item)

            print(f"✓ 从B站获取了 {len(news_list)} 条热门")

        except Exception as e:
            print(f"✗ 爬取B站失败: {str(e)}")

        return news_list

    def _scrape_tencent(self, keyword: Optional[str], limit: int) -> List[Dict]:
        """爬取腾讯新闻"""
        news_list = []

        try:
            url = "https://news.qq.com/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 腾讯新闻链接
            news_links = soup.find_all('a', {'href': lambda x: x and '/a/' in x})

            for i, item in enumerate(news_links[:limit]):
                title = item.get_text().strip()
                url = item.get('href', '')

                if title and url:
                    news_item = {
                        'title': title,
                        'platform': 'tencent',
                        'url': url,
                        'timestamp': datetime.now().isoformat(),
                        'summary': ''
                    }
                    news_list.append(news_item)

            print(f"✓ 从腾讯新闻获取了 {len(news_list)} 条")

        except Exception as e:
            print(f"✗ 爬取腾讯新闻失败: {str(e)}")

        return news_list

    def _scrape_thepaper(self, keyword: Optional[str], limit: int) -> List[Dict]:
        """爬取澎湃新闻"""
        news_list = []

        try:
            url = "https://www.thepaper.cn/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            # 澎湃新闻标题
            news_titles = soup.find_all('h2')

            for i, item in enumerate(news_titles[:limit]):
                title = item.get_text().strip()
                link = item.find('a')
                url = link.get('href', '') if link else ''

                if title:
                    news_item = {
                        'title': title,
                        'platform': 'thepaper',
                        'url': url,
                        'timestamp': datetime.now().isoformat(),
                        'summary': ''
                    }
                    news_list.append(news_item)

            print(f"✓ 从澎湃新闻获取了 {len(news_list)} 条")

        except Exception as e:
            print(f"✗ 爬取澎湃新闻失败: {str(e)}")

        return news_list

    def save_to_json(self, news_list: List[Dict], output_file: str):
        """保存新闻数据到 JSON 文件"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(news_list, f, ensure_ascii=False, indent=2)
        print(f"✓ 数据已保存到 {output_file}")


def main():
    parser = argparse.ArgumentParser(description='新闻数据爬取工具')
    parser.add_argument('--mode', type=str, choices=['api', 'scrape'], required=True,
                        help='数据获取方式: api(使用API) 或 scrape(直接爬取)')
    parser.add_argument('--platform', type=str, help='单个平台名称(直接爬取模式)')
    parser.add_argument('--platforms', type=str, help='多个平台名称,逗号分隔(API模式)')
    parser.add_argument('--keyword', type=str, help='搜索关键词(可选)')
    parser.add_argument('--limit', type=int, default=20, help='获取的新闻数量限制')
    parser.add_argument('--output', type=str, default='news_data.json', help='输出文件路径')

    args = parser.parse_args()

    scraper = NewsScraper()
    all_news = []

    if args.mode == 'api':
        if not args.platforms:
            print("错误: API 模式需要指定 --platforms 参数")
            return

        platforms = [p.strip() for p in args.platforms.split(',')]
        all_news = scraper.scrape_by_api(platforms, args.limit)

    elif args.mode == 'scrape':
        if not args.platform:
            print("错误: 直接爬取模式需要指定 --platform 参数")
            return

        all_news = scraper.scrape_by_direct(args.platform, args.keyword, args.limit)

    # 保存数据
    if all_news:
        scraper.save_to_json(all_news, args.output)
        print(f"\n总计获取了 {len(all_news)} 条新闻数据")
    else:
        print("\n未获取到任何新闻数据")


if __name__ == "__main__":
    main()
