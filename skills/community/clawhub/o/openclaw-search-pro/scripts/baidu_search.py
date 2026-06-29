#!/usr/bin/env python3
"""
Baidu Search Engine - 百度搜索 API
Usage: from baidu_search import BaiduSearch
"""

import requests
import json
import time
from typing import List, Dict, Optional
from pathlib import Path

class BaiduSearch:
    """百度搜索 API"""
    
    def __init__(self, api_key: str = None, secret_key: str = None):
        """
        初始化百度搜索
        
        Args:
            api_key: 百度 API Key
            secret_key: 百度 Secret Key
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.access_token = None
        self.token_expires_at = 0
        
        # 百度 API 端点
        self.token_url = "https://aip.baidubce.com/oauth/2.0/token"
        self.search_url = "https://aip.baidubce.com/rpc/2.0/kg/v1/cognitive/get_sp?sp_id=5006"
    
    def _get_access_token(self) -> Optional[str]:
        """获取访问令牌"""
        if not self.api_key or not self.secret_key:
            return None
        
        # 检查 token 是否过期
        if self.access_token and time.time() < self.token_expires_at:
            return self.access_token
        
        try:
            params = {
                'grant_type': 'client_credentials',
                'client_id': self.api_key,
                'client_secret': self.secret_key
            }
            
            response = requests.post(self.token_url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            self.access_token = data.get('access_token')
            # Token 有效期 30 天，提前 1 天刷新
            expires_in = data.get('expires_in', 2592000)
            self.token_expires_at = time.time() + expires_in - 86400
            
            return self.access_token
        
        except Exception as e:
            print(f"获取百度 Token 失败：{e}")
            return None
    
    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        百度搜索（使用百度智能云 API）
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
        
        Returns:
            [
                {
                    "title": "标题",
                    "url": "链接",
                    "content": "摘要",
                    "score": 0.9,
                    "engine": "baidu"
                }
            ]
        """
        results = []
        
        # 如果没有配置 API Key，返回空结果
        if not self.api_key or not self.secret_key:
            print("⚠️  未配置百度 API Key，请获取后配置")
            print("   获取地址：https://ai.baidu.com/tech/search")
            return results
        
        # 获取 Token
        token = self._get_access_token()
        if not token:
            return results
        
        # 调用搜索 API
        try:
            url = f"{self.search_url}?access_token={token}"
            headers = {'Content-Type': 'application/json'}
            payload = {
                'query': query,
                'rn': max_results,  # 结果数量
                'bs': 0  # 起始位置
            }
            
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # 解析结果
            if 'result' in data:
                for item in data['result'].get('list', []):
                    results.append({
                        'title': item.get('title', ''),
                        'url': item.get('url', ''),
                        'content': item.get('abstract', ''),
                        'score': item.get('score', 0.8),
                        'engine': 'baidu'
                    })
        
        except Exception as e:
            print(f"百度搜索失败：{e}")
        
        return results
    
    def search_simple(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        简化版百度搜索（无需 API Key，通过网页搜索）
        
        注意：这是临时方案，建议使用官方 API
        """
        results = []
        
        # 使用百度移动端搜索
        url = "https://m.baidu.com/s"
        params = {'word': query, 'from': 'wapsi', 'pn': 0}
        
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15'
        })
        
        try:
            response = session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            html = response.text
            
            # 简单解析（实际应该用 BeautifulSoup）
            import re
            
            # 提取搜索结果
            result_pattern = r'<div class="result c-container".*?</div>'
            results_blocks = re.findall(result_pattern, html, re.DOTALL)
            
            for block in results_blocks[:max_results]:
                # 提取标题
                title_match = re.search(r'<h3[^>]*>.*?<a[^>]*>(.*?)</a>', block, re.DOTALL)
                title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip() if title_match else ''
                
                # 提取链接
                url_match = re.search(r'<a[^>]*href="(https?://[^"]+)"', block)
                url = url_match.group(1) if url_match else ''
                
                # 提取摘要
                abstract_match = re.search(r'<span class="c-color-text1">.*?</span>(.*?)</span>', block, re.DOTALL)
                content = re.sub(r'<[^>]+>', '', abstract_match.group(0)).strip() if abstract_match else ''
                
                if title and url:
                    results.append({
                        'title': title,
                        'url': url,
                        'content': content[:200] if content else '',
                        'score': 0.85,
                        'engine': 'baidu-web'
                    })
        
        except Exception as e:
            print(f"百度网页搜索失败：{e}")
        
        return results


# 测试
if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法：python3 baidu_search.py \"搜索关键词\"")
        print("\n配置 API Key：")
        print("  1. 访问 https://ai.baidu.com/tech/search")
        print("  2. 注册并创建应用获取 API Key")
        print("  3. 编辑 config/search-config.json 配置")
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    
    # 从配置文件读取 API Key
    config_path = Path(__file__).parent / "../config/search-config.json"
    api_key = ""
    secret_key = ""
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            api_key = config.get('baidu', {}).get('apiKey', '')
            secret_key = config.get('baidu', {}).get('secretKey', '')
    except:
        pass
    
    baidu = BaiduSearch(api_key=api_key, secret_key=secret_key)
    
    print(f"\n🔍 百度搜索：{query}\n")
    
    # 优先使用 API，失败则使用网页搜索
    results = baidu.search(query, max_results=10)
    
    if not results:
        print("API 搜索失败，尝试网页搜索...\n")
        results = baidu.search_simple(query, max_results=10)
    
    if not results:
        print("未找到结果")
    else:
        for i, result in enumerate(results, 1):
            print(f"{i}. {result['title']}")
            print(f"   链接：{result['url']}")
            print(f"   来源：{result['engine']}")
            if result.get('content'):
                print(f"   摘要：{result['content'][:100]}...")
            print()
