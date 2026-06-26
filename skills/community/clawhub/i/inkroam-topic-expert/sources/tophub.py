#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TopHub.today 聚合数据源
最稳定的数据源，聚合全网 80+ 平台热榜
"""

import re
import requests
from bs4 import BeautifulSoup
from .base import BaseSource


# 我们关注的平台（过滤电商、游戏等无关内容）
WANTED_PLATFORMS = {
    '微博', '知乎', '微信', '百度', '36氪', '少数派',
    '虎嗅网', 'IT之家', '掘金', '机器之心', '量子位',
    'Readhub', '哔哩哔哩', '抖音', '快手', '澎湃新闻',
    '今日头条', 'GitHub', '实时榜中榜',
}


class TophubSource(BaseSource):
    """TopHub.today 聚合热榜"""

    def __init__(self, platforms=None):
        super().__init__('tophub', 'TopHub聚合')
        self.url = "https://tophub.today/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/131.0.0.0 Safari/537.36",
        }
        self.wanted = platforms or WANTED_PLATFORMS

    def fetch(self):
        """抓取 tophub.today 首页"""
        resp = requests.get(self.url, headers=self.headers, timeout=15)
        resp.encoding = 'utf-8'
        soup = BeautifulSoup(resp.text, 'html.parser')

        topics = []
        cards = soup.select('.cc-cd')

        for card in cards:
            # 平台名
            lb = card.select_one('.cc-cd-lb')
            platform = lb.get_text(strip=True).split('‧')[0].strip() if lb else ''

            # 只要我们关注的平台
            if not any(w in platform for w in self.wanted):
                continue

            # 条目列表
            items = card.select('.cc-cd-cb-ll')
            for i, item in enumerate(items):
                t_tag = item.select_one('.t')
                e_tag = item.select_one('.e')

                title = t_tag.get_text(strip=True) if t_tag else ''
                if not title:
                    continue

                hot_text = e_tag.get_text(strip=True) if e_tag else ''
                hot_val = self._parse_hot(hot_text)

                topics.append({
                    'title': title,
                    'url': '',  # tophub 首页条目无链接
                    'hot': hot_val,
                    'summary': hot_text,
                    'sub_platform': platform,
                    'rank': i + 1,
                })

        return topics

    def _normalize_topic(self, topic):
        """重写标准化，加入 sub_platform"""
        base = super()._normalize_topic(topic)
        base['sub_platform'] = topic.get('sub_platform', '')
        base['rank'] = topic.get('rank', 0)
        # 用子平台做 platform 展示
        if topic.get('sub_platform'):
            base['platform'] = topic['sub_platform']
        return base

    @staticmethod
    def _parse_hot(text):
        """
        解析热度文本:
          '1062 万热度' -> 1062
          '105万' -> 105
          '10.0万' -> 10
          '790.5万' -> 790
          '34819055次播放' -> 3481
          '92评' -> 0
          '' -> 0
        """
        if not text:
            return 0
        text = text.replace(',', '').replace(' ', '')
        try:
            if '亿' in text:
                num = re.search(r'([\d.]+)\s*亿', text)
                return int(float(num.group(1)) * 10000) if num else 0
            elif '万' in text:
                num = re.search(r'([\d.]+)\s*万', text)
                return int(float(num.group(1))) if num else 0
            else:
                # 纯数字（如播放量）
                num = re.search(r'(\d+)', text)
                if num:
                    val = int(num.group(1))
                    if val > 10000:
                        return val // 10000  # 转成万
                return 0
        except (ValueError, TypeError):
            return 0


if __name__ == '__main__':
    source = TophubSource()
    topics = source.fetch_with_error_handling()
    print(f"✅ TopHub聚合：{len(topics)} 条\n")

    from collections import Counter
    platforms = Counter(t.get('platform', '?') for t in topics)
    print("各平台数量:")
    for p, c in platforms.most_common():
        print(f"  {p}: {c} 条")

    print(f"\n前15条:")
    for i, t in enumerate(topics[:15], 1):
        print(f"{i}. [{t.get('platform')}] {t['title'][:45]} ({t['hot']}万)")
