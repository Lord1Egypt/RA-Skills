#!/usr/bin/env python3
"""
Custom Search Engine - 自研搜索引擎
Usage: from custom_search import CustomSearchEngine
"""

import requests
import json
from typing import List, Dict, Optional
from pathlib import Path

class CustomSearchEngine:
    """自研搜索引擎 - 聚合多源搜索结果"""
    
    def __init__(self, config_path: str = None):
        """
        初始化搜索引擎
        
        Args:
            config_path: 配置文件路径
        """
        self.config = self._load_config(config_path)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def _load_config(self, config_path: str = None) -> Dict:
        """加载配置文件"""
        if config_path is None:
            config_path = Path(__file__).parent / "../config/search-config.json"
        
        default_config = {
            "engines": {
                "duckduckgo": {"enabled": True},
                "bing": {"enabled": False, "apiKey": ""},
                "google": {"enabled": False, "apiKey": "", "searchEngineId": ""},
                "tavily": {"enabled": False, "apiKey": ""}
            },
            "maxResults": 10,
            "deduplication": True,
            "sortBy": "relevance"
        }
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                return {**default_config, **config}
        except:
            return default_config
    
    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        搜索接口（与 Tavily 兼容）
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
        
        Returns:
            [
                {
                    "title": "标题",
                    "url": "链接",
                    "content": "内容摘要",
                    "score": 0.95,
                    "engine": "来源引擎"
                }
            ]
        """
        all_results = []
        
        # 1. DuckDuckGo（无需 API Key）
        if self.config['engines'].get('duckduckgo', {}).get('enabled', True):
            try:
                results = self._search_duckduckgo(query)
                all_results.extend(results)
            except Exception as e:
                print(f"DuckDuckGo 搜索失败：{e}")
        
        # 2. Bing API
        if self.config['engines'].get('bing', {}).get('enabled', False):
            api_key = self.config['engines']['bing'].get('apiKey', '')
            if api_key:
                try:
                    results = self._search_bing(query, api_key)
                    all_results.extend(results)
                except Exception as e:
                    print(f"Bing 搜索失败：{e}")
        
        # 3. Google API
        if self.config['engines'].get('google', {}).get('enabled', False):
            api_key = self.config['engines']['google'].get('apiKey', '')
            search_id = self.config['engines']['google'].get('searchEngineId', '')
            if api_key and search_id:
                try:
                    results = self._search_google(query, api_key, search_id)
                    all_results.extend(results)
                except Exception as e:
                    print(f"Google 搜索失败：{e}")
        
        # 4. Tavily（备用）
        if self.config['engines'].get('tavily', {}).get('enabled', False):
            api_key = self.config['engines']['tavily'].get('apiKey', '')
            if api_key:
                try:
                    results = self._search_tavily(query, api_key)
                    all_results.extend(results)
                except Exception as e:
                    print(f"Tavily 搜索失败：{e}")
        
        # 5. 去重排序
        if self.config.get('deduplication', True):
            all_results = self._deduplicate(all_results)
        
        all_results = self._sort_results(all_results, self.config.get('sortBy', 'relevance'))
        
        return all_results[:max_results]
    
    def _search_duckduckgo(self, query: str) -> List[Dict]:
        """
        DuckDuckGo 搜索（无需 API Key）
        
        使用 HTML 解析方式获取搜索结果
        """
        results = []
        
        # DuckDuckGo HTML 搜索
        url = "https://html.duckduckgo.com/html/"
        payload = {'q': query}
        
        try:
            response = self.session.post(url, data=payload, timeout=10)
            response.raise_for_status()
            
            # 简单解析 HTML（实际应该用 BeautifulSoup）
            html = response.text
            
            # 提取结果（简化版）
            import re
            result_pattern = r'<a class="result__a" href="([^"]+)">([^<]+)</a>'
            matches = re.findall(result_pattern, html)
            
            for url, title in matches[:10]:
                results.append({
                    'title': title,
                    'url': url,
                    'content': '',  # DuckDuckGo HTML 不返回摘要
                    'score': 0.8,
                    'engine': 'duckduckgo'
                })
        
        except Exception as e:
            # 如果 HTML 解析失败，返回空结果
            print(f"DuckDuckGo HTML 解析失败：{e}")
        
        return results
    
    def _search_bing(self, query: str, api_key: str) -> List[Dict]:
        """Bing Search API"""
        results = []
        
        endpoint = "https://api.bing.microsoft.com/v7.0/search"
        headers = {'Ocp-Apim-Subscription-Key': api_key}
        params = {'q': query, 'count': 10}
        
        response = self.session.get(endpoint, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        for item in data.get('webPages', {}).get('value', []):
            results.append({
                'title': item.get('name', ''),
                'url': item.get('url', ''),
                'content': item.get('snippet', ''),
                'score': item.get('id', 0.8),
                'engine': 'bing'
            })
        
        return results
    
    def _search_google(self, query: str, api_key: str, search_id: str) -> List[Dict]:
        """Google Custom Search API"""
        results = []
        
        endpoint = "https://www.googleapis.com/customsearch/v1"
        params = {
            'key': api_key,
            'cx': search_id,
            'q': query,
            'num': 10
        }
        
        response = self.session.get(endpoint, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        for item in data.get('items', []):
            results.append({
                'title': item.get('title', ''),
                'url': item.get('link', ''),
                'content': item.get('snippet', ''),
                'score': 0.8,
                'engine': 'google'
            })
        
        return results
    
    def _search_tavily(self, query: str, api_key: str) -> List[Dict]:
        """Tavily Search API"""
        results = []
        
        endpoint = "https://api.tavily.com/search"
        headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
        payload = {
            'query': query,
            'max_results': 10,
            'search_depth': 'basic'
        }
        
        response = self.session.post(endpoint, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        for item in data.get('results', []):
            results.append({
                'title': item.get('title', ''),
                'url': item.get('url', ''),
                'content': item.get('content', ''),
                'score': item.get('score', 0.8),
                'engine': 'tavily'
            })
        
        return results
    
    def _deduplicate(self, results: List[Dict]) -> List[Dict]:
        """按 URL 去重"""
        seen_urls = set()
        unique_results = []
        
        for result in results:
            url = result.get('url', '')
            if url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        return unique_results
    
    def _sort_results(self, results: List[Dict], sort_by: str) -> List[Dict]:
        """排序"""
        if sort_by == 'relevance':
            # 按相关性评分排序
            results.sort(key=lambda x: x.get('score', 0), reverse=True)
        elif sort_by == 'engine':
            # 按引擎优先级排序（DuckDuckGo > Bing > Google > Tavily）
            engine_priority = {'duckduckgo': 0, 'bing': 1, 'google': 2, 'tavily': 3}
            results.sort(key=lambda x: engine_priority.get(x.get('engine', 'unknown'), 99))
        
        return results


# 测试
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python3 custom_search.py \"搜索关键词\"")
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    engine = CustomSearchEngine()
    results = engine.search(query, max_results=10)
    
    print(f"\n搜索结果：{query}\n")
    for i, result in enumerate(results, 1):
        print(f"{i}. {result['title']}")
        print(f"   链接：{result['url']}")
        print(f"   来源：{result['engine']}")
        print(f"   评分：{result['score']}")
        if result.get('content'):
            print(f"   摘要：{result['content'][:100]}...")
        print()
