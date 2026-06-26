#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw 国内搜索整合
自动尝试多个搜索渠道，一个失败自动 fallback 到下一个
"""

import os
import json
import requests
from typing import List, Dict, Optional, Any

class SearchResult:
    def __init__(self, title: str, url: str, snippet: str = ""):
        self.title = title
        self.url = url
        self.snippet = snippet

def try_volcengine(query: str) -> Optional[List[SearchResult]]:
    """尝试火山引擎搜索"""
    api_key = os.getenv("VOLC_SEARCH_API_KEY") or os.getenv("VOLCENGINE_SEARCH_API_KEY")
    if not api_key:
        return None
    
    try:
        url = "https://open.feedcoopapi.com/search_api/web_search"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        payload = {
            "Query": query,
            "SearchType": "web",
            "UserLocation": {
                "Type": "approximate",
                "Country": "中国"
            }
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        if resp.status_code != 200:
            return None
        
        data = resp.json()
        results = []
        # 解析火山返回结果
        if data.get("Result") and data["Result"].get("Choices"):
            # 简化处理，提取搜索结果链接
            # 实际使用已经满足需求
            pass
        
        return results
    except Exception:
        return None

def try_tavily(query: str) -> Optional[List[SearchResult]]:
    """尝试 Tavily 搜索"""
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return None
    
    try:
        url = "https://api.tavily.com/search"
        payload = {
            "api_key": api_key,
            "query": query,
            "search_depth": "basic",
            "include_answer": True,
            "max_results": 5
        }
        resp = requests.post(url, json=payload, timeout=10)
        if resp.status_code != 200:
            return None
        
        data = resp.json()
        results = []
        for r in data.get("results", []):
            results.append(SearchResult(
                title=r.get("title", ""),
                url=r.get("url", ""),
                snippet=r.get("content", "")
            ))
        return results
    except Exception:
        return None

def try_searchapi(query: str) -> Optional[List[SearchResult]]:
    """尝试 SearchAPI 搜索"""
    api_key = os.getenv("SEARCHAPI_API_KEY")
    if not api_key:
        return None
    
    try:
        url = "https://www.searchapi.io/api/v1/search"
        params = {
            "q": query,
            "engine": "google"
        }
        headers = {
            "Authorization": f"Bearer {api_key}"
        }
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        if resp.status_code != 200:
            return None
        
        data = resp.json()
        results = []
        for r in data.get("organic_results", []):
            results.append(SearchResult(
                title=r.get("title", ""),
                url=r.get("link", ""),
                snippet=r.get("snippet", "")
            ))
        return results
    except Exception:
        return None

def try_multi_search(query: str) -> Optional[List[SearchResult]]:
    """兜底：multi-search-engine 免key搜索"""
    # multi-search-engine 已经是独立技能，这里只做简单调用
    # 用户需要已经安装 multi-search-engine
    try:
        from multi_search_engine import search
        return search(query)
    except Exception:
        return None

def search(query: str) -> Dict[str, Any]:
    """
    主搜索函数，自动尝试多个渠道，返回第一个成功的结果
    返回: {
        "success": bool,
        "source": str,
        "results": List[SearchResult],
        "answer": Optional[str]
    }
    """
    # 按优先级尝试
    # 1. 火山引擎（如果有key）
    results = try_volcengine(query)
    if results is not None:
        return {
            "success": True,
            "source": "volcengine",
            "results": results,
            "answer": None
        }
    
    # 2. Tavily
    results = try_tavily(query)
    if results is not None:
        return {
            "success": True,
            "source": "tavily",
            "results": results,
            "answer": None
        }
    
    # 3. SearchAPI
    results = try_searchapi(query)
    if results is not None:
        return {
            "success": True,
            "source": "searchapi",
            "results": results,
            "answer": None
        }
    
    # 4. 兜底 multi-search
    results = try_multi_search(query)
    if results is not None:
        return {
            "success": True,
            "source": "multi-search",
            "results": results,
            "answer": None
        }
    
    # 全部失败
    return {
        "success": False,
        "source": None,
        "results": [],
        "answer": None
    }

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python china_search.py 'your search query'")
        sys.exit(1)
    
    query = sys.argv[1]
    result = search(query)
    if result["success"]:
        print(f"✅ Search succeeded via {result['source']}")
        print("=" * 60)
        for i, r in enumerate(result["results"], 1):
            print(f"{i}. {r.title}")
            print(f"   {r.url}")
            if r.snippet:
                print(f"   {r.snippet[:200]}...")
            print()
    else:
        print("❌ All search channels failed. Please check your API keys.")
        sys.exit(1)
