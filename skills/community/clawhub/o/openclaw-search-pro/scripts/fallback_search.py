#!/usr/bin/env python3
"""
Fallback Search - 备用搜索引擎
使用国内可访问的搜索引擎
"""

import requests
import json
from typing import List, Dict

class FallbackSearch:
    """备用搜索引擎（国内可访问）"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_baidu(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        百度搜索（简化版，通过 web 搜索）
        
        注意：这只是演示，实际应该用百度 API
        """
        results = []
        
        # 使用百度搜索的移动端页面（更容易解析）
        url = "https://m.baidu.com/s"
        params = {'word': query, 'from': 'wapsi'}
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            # 简单解析（实际应该用 BeautifulSoup）
            html = response.text
            
            # 提取标题和链接（简化版）
            import re
            title_pattern = r'<h3 class="c-title">(.*?)</h3>'
            url_pattern = r'<a href="(https?://[^"]+)"'
            
            titles = re.findall(title_pattern, html, re.DOTALL)
            urls = re.findall(url_pattern, html)
            
            for i, (title, url) in enumerate(zip(titles[:max_results], urls[:max_results])):
                # 清理 HTML 标签
                clean_title = re.sub(r'<[^>]+>', '', title).strip()
                
                results.append({
                    'title': clean_title,
                    'url': url,
                    'content': '',
                    'score': 0.9 - (i * 0.05),
                    'engine': 'baidu'
                })
        
        except Exception as e:
            print(f"百度搜索失败：{e}")
        
        return results
    
    def search_bing_cn(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        必应中国搜索（cn.bing.com）
        """
        results = []
        
        url = "https://cn.bing.com/search"
        params = {'q': query, 'first': 1}
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            html = response.text
            
            # 简单解析
            import re
            result_pattern = r'<li class="b_algo"(.*?)</li>'
            results_blocks = re.findall(result_pattern, html, re.DOTALL)
            
            for block in results_blocks[:max_results]:
                title_match = re.search(r'<h2><a href="([^"]+)">([^<]+)</a>', block)
                if title_match:
                    url = title_match.group(1)
                    title = title_match.group(2)
                    
                    snippet_match = re.search(r'<div class="b_caption">.*?<p>(.*?)</p>', block, re.DOTALL)
                    content = re.sub(r'<[^>]+>', '', snippet_match.group(1)).strip() if snippet_match else ''
                    
                    results.append({
                        'title': title,
                        'url': url,
                        'content': content[:200],
                        'score': 0.85,
                        'engine': 'bing-cn'
                    })
        
        except Exception as e:
            print(f"Bing 中国搜索失败：{e}")
        
        return results
    
    def search_sogou(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        搜狗搜索
        """
        results = []
        
        url = "https://m.sogou.com/web"
        params = {'query': query}
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            # 简化解析
            html = response.text
            
            import re
            title_pattern = r'<h3 class="vr-title">.*?<a href="[^"]*" target="_blank">(.*?)</a>'
            titles = re.findall(title_pattern, html, re.DOTALL)
            
            for i, title in enumerate(titles[:max_results]):
                clean_title = re.sub(r'<[^>]+>', '', title).strip()
                results.append({
                    'title': clean_title,
                    'url': f'https://www.sogou.com/sogou?query={query}',
                    'content': '',
                    'score': 0.8 - (i * 0.05),
                    'engine': 'sogou'
                })
        
        except Exception as e:
            print(f"搜狗搜索失败：{e}")
        
        return results


# 测试
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python3 fallback_search.py \"搜索关键词\"")
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    search = FallbackSearch()
    
    print(f"\n搜索：{query}\n")
    
    # 测试 Bing 中国
    print("Bing 中国搜索：")
    results = search.search_bing_cn(query, max_results=5)
    for i, r in enumerate(results, 1):
        print(f"{i}. {r['title']}")
        print(f"   链接：{r['url']}")
        print()
