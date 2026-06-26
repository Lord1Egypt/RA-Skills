#!/usr/bin/env python3
"""
华尔街见闻数据获取模块
参考NewsNow实现：https://api-one.wallstcn.com/apiv1/content/lives
"""

import json
import urllib.request
from datetime import datetime

def fetch_wallstreetcn():
    """获取华尔街见闻实时快讯"""
    try:
        url = "https://api-one.wallstcn.com/apiv1/content/lives?channel=global-channel&limit=30"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode('utf-8'))
            
            items = []
            for item in data['data']['items']:
                items.append({
                    'id': item['id'],
                    'title': item.get('title') or item.get('content_text', ''),
                    'url': item['uri'],
                    'date': datetime.fromtimestamp(item['display_time']).isoformat(),
                    'source': '华尔街见闻',
                    'category': '财经资讯'
                })
            
            return items[:20]
    except Exception as e:
        return [{'error': str(e), 'source': '华尔街见闻'}]

if __name__ == "__main__":
    news = fetch_wallstreetcn()
    print(f"✅ 获取华尔街见闻 {len([n for n in news if 'error' not in n])} 条")
    print(json.dumps(news[:5], indent=2, ensure_ascii=False))