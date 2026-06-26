#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取热点数据 - 针对 AI 资讯类账号优化
数据源：微博、知乎、36氪、虎嗅、机器之心、量子位
"""

import json
import requests
from datetime import datetime
import sys
from bs4 import BeautifulSoup


def fetch_weibo_hot():
    """获取微博热搜 - 筛选 AI 相关"""
    try:
        url = "https://weibo.com/ajax/side/hotSearch"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Referer": "https://weibo.com/"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        
        if data.get('ok') != 1:
            return []
        
        hot_list = []
        for item in data.get('data', {}).get('realtime', []):
            # 过滤广告
            if item.get('ad_channel') == 1 or item.get('is_ad') == 1:
                continue
            
            title = item.get('word', '')
            # 只保留 AI 相关热搜
            ai_keywords = ['AI', '人工智能', 'ChatGPT', 'GPT', 'Claude', '大模型', 'OpenAI', '智能', '机器人', '算法']
            if any(kw.lower() in title.lower() for kw in ai_keywords):
                hot_list.append({
                    "rank": item.get('rank', 0),
                    "title": title,
                    "url": f"https://m.weibo.cn/search?containerid=100103&q=%23{title}%23",
                    "hot": item.get('num', 0),
                    "source": "weibo"
                })
        
        return hot_list[:10]
    except Exception as e:
        print(f"获取微博热搜失败: {e}", file=sys.stderr)
        return []


def fetch_zhihu_hot():
    """获取知乎热榜 - 筛选 AI 相关"""
    try:
        url = "https://www.zhihu.com/api/v4/creators/rank/hot?domain=0&period=hour"
        headers = {
            "r-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        
        hot_list = []
        for item in data.get('data', []):
            question = item.get('question', {})
            title = question.get('title', '')
            
            # 只保留 AI 相关问题
            ai_keywords = ['AI', '人工智能', 'ChatGPT', 'GPT', 'Claude', '大模型', 'OpenAI', '效率工具', '自动化']
            if any(kw.lower() in title.lower() for kw in ai_keywords):
                hot_list.append({
                    "rank": len(hot_list) + 1,
                    "title": title,
                    "url": question.get('url', ''),
                    "excerpt": question.get('excerpt', ''),
                    "source": "zhihu"
                })
        
        return hot_list[:10]
    except Exception as e:
        print(f"获取知乎热榜失败: {e}", file=sys.stderr)
        return []


def fetch_36kr_news():
    """获取 36氪 AI 资讯"""
    try:
        # 36氪 AI 频道
        url = "https://www.36kr.com/information/artificial_intelligence/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        hot_list = []
        articles = soup.select('.article-item-title')[:10]
        
        for idx, article in enumerate(articles, 1):
            title = article.get_text(strip=True)
            url_elem = article.find('a')
            article_url = url_elem.get('href', '') if url_elem else ''
            
            if article_url and not article_url.startswith('http'):
                article_url = f"https://www.36kr.com{article_url}"
            
            hot_list.append({
                "rank": idx,
                "title": title,
                "url": article_url,
                "source": "36kr"
            })
        
        return hot_list
    except Exception as e:
        print(f"获取36氪资讯失败: {e}", file=sys.stderr)
        return []


def fetch_jiqizhixin_news():
    """获取机器之心资讯"""
    try:
        url = "https://www.jiqizhixin.com/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        hot_list = []
        articles = soup.select('.article-title')[:10]
        
        for idx, article in enumerate(articles, 1):
            title = article.get_text(strip=True)
            url_elem = article.find('a')
            article_url = url_elem.get('href', '') if url_elem else ''
            
            if article_url and not article_url.startswith('http'):
                article_url = f"https://www.jiqizhixin.com{article_url}"
            
            hot_list.append({
                "rank": idx,
                "title": title,
                "url": article_url,
                "source": "jiqizhixin"
            })
        
        return hot_list
    except Exception as e:
        print(f"获取机器之心资讯失败: {e}", file=sys.stderr)
        return []


def main():
    """主函数"""
    print("正在获取 AI 资讯热点数据...\n", file=sys.stderr)
    
    # 获取各数据源
    print("📡 微博热搜（AI 相关）...", file=sys.stderr)
    weibo_data = fetch_weibo_hot()
    print(f"   ✓ {len(weibo_data)} 条", file=sys.stderr)
    
    print("📡 知乎热榜（AI 相关）...", file=sys.stderr)
    zhihu_data = fetch_zhihu_hot()
    print(f"   ✓ {len(zhihu_data)} 条", file=sys.stderr)
    
    print("📡 36氪 AI 频道...", file=sys.stderr)
    kr36_data = fetch_36kr_news()
    print(f"   ✓ {len(kr36_data)} 条", file=sys.stderr)
    
    print("📡 机器之心...", file=sys.stderr)
    jqzx_data = fetch_jiqizhixin_news()
    print(f"   ✓ {len(jqzx_data)} 条", file=sys.stderr)
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "weibo": weibo_data,
        "zhihu": zhihu_data,
        "36kr": kr36_data,
        "jiqizhixin": jqzx_data,
        "total": len(weibo_data) + len(zhihu_data) + len(kr36_data) + len(jqzx_data)
    }
    
    # 输出 JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 保存到文件
    output_file = "/tmp/hot_topics.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 获取成功：共 {result['total']} 条 AI 相关热点", file=sys.stderr)
    print(f"数据已保存到：{output_file}", file=sys.stderr)


if __name__ == '__main__':
    main()
