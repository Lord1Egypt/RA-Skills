#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
获取热点数据
支持：微博、知乎、网易
"""

import json
import requests
from datetime import datetime
import sys


def fetch_weibo_hot():
    """获取微博热搜"""
    try:
        url = "https://weibo.com/ajax/side/hotSearch"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        
        hot_list = []
        for item in data.get('data', {}).get('realtime', [])[:20]:
            hot_list.append({
                "rank": item.get('rank', 0),
                "title": item.get('word', ''),
                "url": f"https://s.weibo.com/weibo?q=%23{item.get('word', '')}%23",
                "hot": item.get('num', 0),
                "category": item.get('category', ''),
                "source": "weibo"
            })
        return hot_list
    except Exception as e:
        print(f"获取微博热搜失败: {e}", file=sys.stderr)
        return []


def fetch_zhihu_hot():
    """获取知乎热榜"""
    try:
        url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=20"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        
        hot_list = []
        for idx, item in enumerate(data.get('data', [])[:20], 1):
            target = item.get('target', {})
            hot_list.append({
                "rank": idx,
                "title": target.get('title', ''),
                "url": target.get('url', ''),
                "hot": item.get('detail_text', ''),
                "excerpt": target.get('excerpt', ''),
                "source": "zhihu"
            })
        return hot_list
    except Exception as e:
        print(f"获取知乎热榜失败: {e}", file=sys.stderr)
        return []


def fetch_netease_hot():
    """获取网易新闻热榜"""
    try:
        # 使用澎湃新闻作为替代
        url = "https://cache.thepaper.cn/contentapi/wwwIndex/rightSidebar"
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }
        resp = requests.get(url, headers=headers, timeout=10)
        data = resp.json()
        
        hot_list = []
        for idx, item in enumerate(data.get('data', {}).get('hotNews', [])[:20], 1):
            hot_list.append({
                "rank": idx,
                "title": item.get('name', ''),
                "url": f"https://www.thepaper.cn/newsDetail_forward_{item.get('contId', '')}",
                "hot": item.get('praiseTimes', 0),
                "source": "pengpai"
            })
        return hot_list
    except Exception as e:
        print(f"获取澎湃热榜失败: {e}", file=sys.stderr)
        return []


def main():
    """主函数"""
    print("正在获取热点数据...", file=sys.stderr)
    
    weibo_data = fetch_weibo_hot()
    zhihu_data = fetch_zhihu_hot()
    netease_data = fetch_netease_hot()
    
    result = {
        "timestamp": datetime.now().isoformat(),
        "weibo": weibo_data,
        "zhihu": zhihu_data,
        "pengpai": netease_data,
        "total": len(weibo_data) + len(zhihu_data) + len(netease_data)
    }
    
    # 输出 JSON
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 保存到文件
    output_file = "/tmp/hot_topics.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 获取成功：微博 {len(weibo_data)} 条，知乎 {len(zhihu_data)} 条，澎湃 {len(netease_data)} 条", file=sys.stderr)
    print(f"数据已保存到：{output_file}", file=sys.stderr)


if __name__ == '__main__':
    main()
