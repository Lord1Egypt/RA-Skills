"""
Semantic Scholar API

增强功能：
- 添加更长的延迟和更多重试次数
- 指数退避策略
"""

import requests
import time
import random


def search_semantic(query, max_results=20, max_retries=3):
    """
    调用 Semantic Scholar API 获取论文
    
    参数:
        query: 查询字符串
        max_results: 最大返回数
        max_retries: 最大重试次数（增加到 3 次）
    
    返回:
        List[dict]
    """
    url = "https://api.semanticscholar.org/graph/v1/paper/search"

    # 限制单次请求数量，避免速率限制
    actual_limit = min(max_results, 10)
    
    params = {
        "query": query,
        "limit": actual_limit,
        "fields": "title,abstract,year,url,authors,venue,publicationTypes"
    }

    # 请求前添加随机延迟（3-8 秒），增加延迟避免速率限制
    initial_delay = random.uniform(3, 8)
    print(f"  [Semantic Scholar] 等待 {initial_delay:.1f} 秒后开始检索...")
    time.sleep(initial_delay)

    # 重试逻辑 - 增加重试次数
    for attempt in range(max_retries):
        try:
            print(f"  [Semantic Scholar] 正在检索 (尝试 {attempt + 1}/{max_retries})...")
            # 增加超时到 120 秒
            r = requests.get(url, params=params, timeout=120)
            
            if r.status_code == 429:
                # 速率限制，指数退避（更长的等待时间）
                wait_time = (2 ** attempt) * 5 + random.uniform(0, 3)
                print(f"  [Semantic Scholar] 速率限制，等待 {wait_time:.1f} 秒后重试...")
                time.sleep(wait_time)
                continue
                
            r.raise_for_status()
            data = r.json()
            results = _process_results(data, max_results)
            print(f"  [Semantic Scholar] 检索到 {len(results)} 篇")
            return results
            
        except requests.exceptions.Timeout as e:
            # 超时错误，增加更长的等待时间
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 10 + random.uniform(0, 5)
                print(f"  [Semantic Scholar] 请求超时：{e}，等待 {wait_time:.1f} 秒后重试...")
                time.sleep(wait_time)
            else:
                print(f"  [Semantic Scholar 检索失败]: 超时 - {e}")
                return []
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 5 + random.uniform(0, 3)
                print(f"  [Semantic Scholar] 请求错误：{e}，等待 {wait_time:.1f} 秒后重试...")
                time.sleep(wait_time)
            else:
                print(f"  [Semantic Scholar 检索失败]: {e}")
                return []
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = (2 ** attempt) * 3
                print(f"  [Semantic Scholar] 错误：{e}，等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
            else:
                print(f"  [Semantic Scholar 检索失败]: {e}")
                return []
    
    return []


def _process_results(data, max_results):
    """处理检索结果"""
    results = []

    for p in data.get("data", []):
        if not p.get("title"):
            continue

        authors = [a["name"] for a in p.get("authors", [])] if p.get("authors") else []
        
        # 获取 venue 信息
        venue = p.get("venue", "")
        publication_types = p.get("publicationTypes", [])

        results.append({
            "title": p["title"],
            "abstract": p.get("abstract", "") or "",
            "url": p.get("url", ""),
            "year": p.get("year", 0),
            "authors": authors,
            "source": "semantic",
            "venue": venue,
            "publication_types": publication_types
        })
        
        if len(results) >= max_results:
            break

    return results
