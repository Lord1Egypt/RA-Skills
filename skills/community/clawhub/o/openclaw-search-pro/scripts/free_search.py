#!/usr/bin/env python3
"""
Free Search Engine - 免费搜索引擎（无需 API Key）
使用网页搜索方式，安装即用
"""

import sys
import requests
import re
from typing import List, Dict
from pathlib import Path

# 修复Windows GBK编码兼容问题
if sys.platform.startswith('win'):
    try:
        # Python 3.7+ 支持 reconfigure
        sys.stdin.reconfigure(encoding='utf-8')
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        # 旧版本Python兼容
        import io
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', line_buffering=True)

class FreeSearch:
    """免费搜索引擎（无需 API Key）"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
    
    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        搜索接口（自动选择最佳引擎）
        
        优先级：
        1. 必应中国（cn.bing.com）- 国内可访问
        2. 搜狗搜索 - 国内可访问
        3. 360 搜索 - 国内可访问
        """
        all_results = []
        
        # 1. 必应中国（首选）
        try:
            results = self._search_bing_cn(query, max_results)
            if results:
                return results  # 成功则返回
        except Exception as e:
            print(f"必应搜索失败：{e}")
        
        # 2. 搜狗搜索（备选）
        try:
            results = self._search_sogou(query, max_results)
            if results:
                return results
        except Exception as e:
            print(f"搜狗搜索失败：{e}")
        
        # 3. 360 搜索（最后备选）
        try:
            results = self._search_so360(query, max_results)
            return results
        except Exception as e:
            print(f"360 搜索失败：{e}")
        
        return []
    
    def _search_bing_cn(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        必应中国搜索（cn.bing.com）
        国内可访问，无需 API Key
        """
        results = []
        
        url = "https://cn.bing.com/search"
        params = {'q': query, 'first': 1}
        
        response = self.session.get(url, params=params, timeout=10)
        response.raise_for_status()
        html = response.text
        
        # 解析搜索结果
        result_pattern = r'<li class="b_algo"(.*?)</li>'
        results_blocks = re.findall(result_pattern, html, re.DOTALL)
        
        for block in results_blocks[:max_results]:
            # 提取标题和链接
            title_match = re.search(r'<h2><a href="([^"]+)">([^<]+)</a>', block)
            if title_match:
                url = title_match.group(1)
                title = re.sub(r'<[^>]+>', '', title_match.group(2)).strip()
                
                # 提取摘要
                snippet_match = re.search(r'<div class="b_caption">.*?<p>(.*?)</p>', block, re.DOTALL)
                content = ''
                if snippet_match:
                    content = re.sub(r'<[^>]+>', '', snippet_match.group(1)).strip()
                    content = content[:200] + '...' if len(content) > 200 else content
                
                results.append({
                    'title': title,
                    'url': url,
                    'content': content,
                    'score': 0.9 - (len(results) * 0.05),
                    'engine': 'bing-cn'
                })
        
        return results
    
    def _search_sogou(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        搜狗搜索
        国内可访问，无需 API Key
        """
        results = []
        
        url = "https://m.sogou.com/web"
        params = {'query': query}
        
        response = self.session.get(url, params=params, timeout=10)
        response.raise_for_status()
        html = response.text
        
        # 简单解析
        title_pattern = r'<h3 class="vr-title">.*?<a[^>]*>(.*?)</a>'
        titles = re.findall(title_pattern, html, re.DOTALL)
        
        for i, title in enumerate(titles[:max_results]):
            clean_title = re.sub(r'<[^>]+>', '', title).strip()
            results.append({
                'title': clean_title,
                'url': f'https://www.sogou.com/sogou?query={query}',
                'content': '',
                'score': 0.85 - (i * 0.05),
                'engine': 'sogou'
            })
        
        return results
    
    def _search_so360(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        360 搜索
        国内可访问，无需 API Key
        """
        results = []
        
        url = "https://m.so.com/s"
        params = {'q': query}
        
        response = self.session.get(url, params=params, timeout=10)
        response.raise_for_status()
        html = response.text
        
        # 简单解析
        result_pattern = r'<h3 class="res-title">.*?<a[^>]*>(.*?)</a>'
        titles = re.findall(result_pattern, html, re.DOTALL)
        
        for i, title in enumerate(titles[:max_results]):
            clean_title = re.sub(r'<[^>]+>', '', title).strip()
            results.append({
                'title': clean_title,
                'url': f'https://www.so.com/s?q={query}',
                'content': '',
                'score': 0.8 - (i * 0.05),
                'engine': 'so360'
            })
        
        return results


# 测试
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python3 free_search.py \"搜索关键词\"")
        print("\n特点：")
        print("  ✅ 无需 API Key")
        print("  ✅ 安装即用")
        print("  ✅ 国内可访问")
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    search = FreeSearch()
    
    print(f"\n🔍 搜索：{query}\n")
    
    results = search.search(query, max_results=10)
    
    if not results:
        print("未找到结果")
    else:
        print(f"找到 {len(results)} 个结果：\n")
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   链接：{result['url']}")
            print(f"   来源：{result['engine']}")
            if result.get('content'):
                print(f"   摘要：{result['content']}")
            print()
