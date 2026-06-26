#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多平台数据采集器
支持：微博、知乎、小红书、抖音、X、脉脉、36氪、虎嗅、GitHub
"""

import json
import requests
from datetime import datetime
import sys
from bs4 import BeautifulSoup
import time


class MultiPlatformCrawler:
    """多平台爬虫"""
    
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        self.results = {}
    
    def fetch_weibo(self):
        """微博热搜 - AI 相关"""
        try:
            url = "https://weibo.com/ajax/side/hotSearch"
            headers = {**self.headers, "Referer": "https://weibo.com/"}
            resp = requests.get(url, headers=headers, timeout=10)
            data = resp.json()
            
            if data.get('ok') != 1:
                return []
            
            hot_list = []
            ai_keywords = ['AI', '人工智能', 'ChatGPT', 'GPT', 'Claude', '大模型', 
                          'OpenAI', '智能', '机器人', '算法', '科技', '互联网']
            
            for item in data.get('data', {}).get('realtime', []):
                if item.get('ad_channel') == 1 or item.get('is_ad') == 1:
                    continue
                
                title = item.get('word', '')
                if any(kw in title for kw in ai_keywords):
                    hot_list.append({
                        "title": title,
                        "url": f"https://m.weibo.cn/search?containerid=100103&q=%23{title}%23",
                        "hot": item.get('num', 0),
                        "rank": item.get('rank', 0),
                        "source": "weibo",
                        "platform": "微博"
                    })
            
            return hot_list[:20]
        except Exception as e:
            print(f"[微博] 获取失败: {e}", file=sys.stderr)
            return []
    
    def fetch_zhihu(self):
        """知乎热榜 - AI 相关"""
        try:
            url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=50"
            resp = requests.get(url, headers=self.headers, timeout=10)
            data = resp.json()
            
            hot_list = []
            ai_keywords = ['AI', '人工智能', 'ChatGPT', 'GPT', 'Claude', '大模型', 
                          'OpenAI', '效率', '工具', '自动化', '科技']
            
            for item in data.get('data', []):
                target = item.get('target', {})
                title = target.get('title', '')
                
                if any(kw in title for kw in ai_keywords):
                    hot_list.append({
                        "title": title,
                        "url": target.get('url', ''),
                        "excerpt": target.get('excerpt', ''),
                        "hot": item.get('detail_text', ''),
                        "source": "zhihu",
                        "platform": "知乎"
                    })
            
            return hot_list[:20]
        except Exception as e:
            print(f"[知乎] 获取失败: {e}", file=sys.stderr)
            return []
    
    def fetch_xiaohongshu(self):
        """小红书热门 - 通过搜索 API"""
        try:
            # 小红书需要登录，这里用搜索关键词的方式
            keywords = ["AI工具", "人工智能", "ChatGPT", "效率工具"]
            hot_list = []
            
            for keyword in keywords:
                # 实际需要小红书 API 或爬虫，这里先返回空
                # TODO: 接入小红书数据源
                pass
            
            return hot_list
        except Exception as e:
            print(f"[小红书] 获取失败: {e}", file=sys.stderr)
            return []
    
    def fetch_douyin(self):
        """抖音热点 - 通过热榜 API"""
        try:
            # 抖音需要 APP 端 API，这里先返回空
            # TODO: 接入抖音数据源
            return []
        except Exception as e:
            print(f"[抖音] 获取失败: {e}", file=sys.stderr)
            return []
    
    def fetch_twitter(self):
        """X (Twitter) - AI 相关话题"""
        try:
            # Twitter API 需要认证，这里先返回空
            # TODO: 接入 Twitter API
            return []
        except Exception as e:
            print(f"[Twitter] 获取失败: {e}", file=sys.stderr)
            return []
    
    def fetch_maimai(self):
        """脉脉职场 - AI 相关讨论"""
        try:
            # 脉脉这里先返回空
            # TODO: 接入脉脉数据源
            return []
        except Exception as e:
            print(f"[脉脉] 获取失败: {e}", file=sys.stderr)
            return []
    
    def fetch_36kr(self):
        """36氪 - AI 频道"""
        try:
            url = "https://www.36kr.com/information/artificial_intelligence/"
            resp = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            hot_list = []
            # 36氪页面结构可能变化，需要实际调试
            # TODO: 优化 36氪解析逻辑
            
            return hot_list
        except Exception as e:
            print(f"[36氪] 获取失败: {e}", file=sys.stderr)
            return []
    
    def fetch_huxiu(self):
        """虎嗅 - 科技资讯"""
        try:
            url = "https://www.huxiu.com/channel/105.html"
            resp = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            hot_list = []
            # TODO: 优化虎嗅解析逻辑
            
            return hot_list
        except Exception as e:
            print(f"[虎嗅] 获取失败: {e}", file=sys.stderr)
            return []
    
    def fetch_github_trending(self):
        """GitHub Trending - AI 相关项目"""
        try:
            url = "https://github.com/trending?since=daily&spoken_language_code=en"
            resp = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            hot_list = []
            ai_keywords = ['ai', 'machine-learning', 'deep-learning', 'llm', 
                          'chatgpt', 'gpt', 'transformer']
            
            repos = soup.select('article.Box-row')[:20]
            for repo in repos:
                title_elem = repo.select_one('h2 a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True).replace('\n', '').replace(' ', '')
                desc_elem = repo.select_one('p')
                desc = desc_elem.get_text(strip=True) if desc_elem else ''
                
                # 筛选 AI 相关项目
                if any(kw in title.lower() or kw in desc.lower() for kw in ai_keywords):
                    hot_list.append({
                        "title": title,
                        "url": f"https://github.com{title_elem.get('href', '')}",
                        "excerpt": desc,
                        "source": "github",
                        "platform": "GitHub"
                    })
            
            return hot_list
        except Exception as e:
            print(f"[GitHub] 获取失败: {e}", file=sys.stderr)
            return []
    
    def fetch_all(self):
        """获取所有平台数据"""
        print("🌐 开始全网数据采集...\n", file=sys.stderr)
        
        platforms = [
            ("微博", self.fetch_weibo),
            ("知乎", self.fetch_zhihu),
            ("小红书", self.fetch_xiaohongshu),
            ("抖音", self.fetch_douyin),
            ("Twitter", self.fetch_twitter),
            ("脉脉", self.fetch_maimai),
            ("36氪", self.fetch_36kr),
            ("虎嗅", self.fetch_huxiu),
            ("GitHub", self.fetch_github_trending),
        ]
        
        for platform_name, fetch_func in platforms:
            print(f"📡 {platform_name}...", file=sys.stderr)
            data = fetch_func()
            self.results[platform_name.lower()] = data
            print(f"   ✓ {len(data)} 条", file=sys.stderr)
            time.sleep(1)  # 避免请求过快
        
        total = sum(len(v) for v in self.results.values())
        print(f"\n✅ 采集完成：共 {total} 条", file=sys.stderr)
        
        return self.results


def main():
    """主函数"""
    crawler = MultiPlatformCrawler()
    results = crawler.fetch_all()
    
    # 输出 JSON
    output = {
        "timestamp": datetime.now().isoformat(),
        "platforms": results,
        "total": sum(len(v) for v in results.values())
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))
    
    # 保存到文件
    output_file = "/tmp/multi_platform_topics.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n数据已保存到：{output_file}", file=sys.stderr)


if __name__ == '__main__':
    main()
