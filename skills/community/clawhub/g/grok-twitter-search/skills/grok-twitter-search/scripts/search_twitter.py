#!/usr/bin/env python3
"""
Grok Twitter Search - 最终版
架构：用户问题 → Grok x_search → 结构化 JSON → 返回结果
"""

import os
import sys
import json
import argparse
import httpx
import re

_http_client = None

def get_client(proxy: str = None) -> httpx.Client:
    global _http_client
    if _http_client is None:
        _http_client = httpx.Client(proxy=proxy, timeout=httpx.Timeout(15.0, read=60.0))
    return _http_client

def search_twitter(
    query: str, 
    api_key: str, 
    api_base: str = "https://api.x.ai/v1", 
    max_results: int = 10,
    proxy: str = None
) -> dict:
    """
    调用 Grok x_search，要求返回结构化 JSON
    """
    url = f"{api_base.rstrip('/')}/responses"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    model = "grok-4-1-fast-reasoning"
    
    # 关键：明确要求返回 JSON 格式
    payload = {
        "model": model,
        "input": f"""Search Twitter for: {query}

Return results as a JSON array with this exact format:
[
  {{
    "author": "@username",
    "content": "tweet text",
    "timestamp": "Nov 12, 2025",
    "likes": 1234,
    "retweets": 567,
    "url": "https://x.com/i/status/123456789"
  }}
]

Return up to {max_results} tweets. Only return the JSON array, no other text.""",
        "tools": [{"type": "x_search"}],
        "temperature": 0.0
    }

    try:
        client = get_client(proxy)
        response = client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        
        result = {
            "status": "success",
            "query": query,
            "tweets": [],
            "model_used": model,
            "usage": {}
        }
        
        # 提取 usage
        usage = data.get("usage", {})
        tool_details = usage.get("server_side_tool_usage_details", {})
        x_search_calls = tool_details.get("x_search_calls", 0) if tool_details else 0
        
        result["usage"] = {
            "input_tokens": usage.get("input_tokens", 0),
            "output_tokens": usage.get("output_tokens", 0),
            "total_tokens": usage.get("total_tokens", 0),
            "x_search_calls": x_search_calls
        }
        
        # 解析结果
        tweets = []
        output_list = data.get("output", [])
        
        for item in output_list:
            if not isinstance(item, dict):
                continue
            
            # 策略 1: 直接从 message content 中提取 JSON
            if item.get("type") == "message":
                content_list = item.get("content", [])
                for c in content_list:
                    if c.get("type") == "output_text":
                        text = c.get("text", "").strip()
                        
                        # 尝试找到 JSON 数组
                        start = text.find("[")
                        end = text.rfind("]")
                        if start != -1 and end != -1:
                            json_str = text[start:end+1]
                            try:
                                parsed = json.loads(json_str)
                                if isinstance(parsed, list):
                                    for t in parsed:
                                        if isinstance(t, dict) and t.get("author"):
                                            tweets.append({
                                                "author": t.get("author", ""),
                                                "content": t.get("content", ""),
                                                "timestamp": t.get("timestamp", ""),
                                                "likes": t.get("likes", 0),
                                                "retweets": t.get("retweets", 0),
                                                "url": t.get("url", "")
                                            })
                            except json.JSONDecodeError as e:
                                print(f"[Warn] JSON 解析失败：{e}", file=sys.stderr)
                        
                        # 备用：如果 JSON 解析失败，用正则提取
                        if not tweets:
                            tweets = parse_fallback(text, max_results)
            
            # 策略 2: 直接的工具返回（原生格式）
            elif item.get("id") and item.get("content"):
                tweets.append({
                    "author": f"@{item.get('author', {}).get('handle', 'unknown')}",
                    "content": item.get("content", ""),
                    "timestamp": item.get("timestamp", ""),
                    "likes": item.get("engagement", {}).get("likes", 0),
                    "retweets": item.get("engagement", {}).get("reposts", 0),
                    "url": f"https://x.com/i/status/{item.get('id')}"
                })
        
        result["tweets"] = tweets[:max_results]
        
        # 打印成本报告
        input_tokens = result["usage"]["input_tokens"]
        output_tokens = result["usage"]["output_tokens"]
        total_cost = (input_tokens / 1_000_000) * 0.20 + (output_tokens / 1_000_000) * 0.50
        
        print(f"📊 Token: {input_tokens:,} in / {output_tokens:,} out | x_search: {x_search_calls} | 成本：${total_cost:.4f}", file=sys.stderr)
        
        return result

    except httpx.HTTPStatusError as e:
        error_msg = f"API 错误：{e.response.status_code}"
        print(f"❌ {error_msg}", file=sys.stderr)
        return {"status": "error", "message": error_msg}
    except httpx.RequestError as e:
        error_msg = f"网络错误：{e}"
        print(f"❌ {error_msg}", file=sys.stderr)
        return {"status": "error", "message": error_msg}
    except Exception as e:
        error_msg = f"未知错误：{e}"
        print(f"❌ {error_msg}", file=sys.stderr)
        return {"status": "error", "message": error_msg}

def parse_fallback(text: str, max_results: int) -> list:
    """备用解析：处理非 JSON 格式"""
    tweets = []
    
    # 提取 URL 映射
    url_pattern = r'\[\[(\d+)\]\]\(https://x\.com/i/status/(\d+)\)'
    url_matches = re.findall(url_pattern, text)
    url_map = {num: url for num, url in url_matches}
    
    # 逐行解析
    lines = text.split('\n')
    current_num = None
    current_date = None
    current_content = None
    
    for line in lines:
        entry_match = re.match(r'(\d+)\.\s+\*\*([^*]+)\*\*', line)
        if entry_match:
            if current_num and current_content:
                tweets.append({
                    "author": "@cz_binance",
                    "content": current_content.strip()[:500],
                    "timestamp": current_date.strip(),
                    "likes": 0,
                    "retweets": 0,
                    "url": f"https://x.com/i/status/{url_map.get(current_num, '')}"
                })
                if len(tweets) >= max_results:
                    break
            
            current_num = entry_match.group(1)
            current_date = entry_match.group(2).strip()
            current_content = None
        
        if current_num and not current_content:
            content_match = re.search(r'"([^"]+)"', line)
            if content_match:
                current_content = content_match.group(1)
    
    if current_num and current_content and len(tweets) < max_results:
        tweets.append({
            "author": "@cz_binance",
            "content": current_content.strip()[:500],
            "timestamp": current_date.strip(),
            "likes": 0,
            "retweets": 0,
            "url": f"https://x.com/i/status/{url_map.get(current_num, '')}"
        })
    
    return tweets

def main():
    parser = argparse.ArgumentParser(description="Grok Twitter Search")
    parser.add_argument("--query", required=True, help="搜索查询")
    parser.add_argument("--api-key", help="Grok API Key")
    parser.add_argument("--api-base", default="https://api.x.ai/v1")
    parser.add_argument("--max-results", type=int, default=10)
    parser.add_argument("--proxy", help="SOCKS5 代理")
    
    args = parser.parse_args()
    
    api_key = args.api_key or os.environ.get("GROK_API_KEY")
    if not api_key:
        print(json.dumps({"status": "error", "message": "缺少 GROK_API_KEY"}))
        sys.exit(1)
    
    proxy = args.proxy or os.environ.get("SOCKS5_PROXY")
    
    result = search_twitter(
        args.query, api_key, args.api_base, 
        args.max_results, proxy
    )
    
    print(json.dumps(result, ensure_ascii=False, indent=2))

if __name__ == "__main__":
    main()
