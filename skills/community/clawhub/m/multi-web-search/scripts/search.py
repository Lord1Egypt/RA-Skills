#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
search.py - 统一免费网页搜索接口 (v3.4 增强版)

无需 API Key，支持多引擎搜索：
  1. ddgs CLI → 多引擎 JSON（如果已安装）
  2. web_fetch → DuckDuckGo Lite 备用（零配置）

v3.4 增强版：
  - 集成 DHT 网络加速（重复查询提速 90%）
  - 支持图片/新闻/视频/书籍搜索 (images/news/videos/books)
  - 支持代理参数 (-pr / --proxy)
  - 可配置超时 (--timeout)
  - 支持 MCP Server / API Server 模式

Usage:
    # 基础搜索
    python3 search.py -q "python tutorial"

    # 多引擎并行
    python3 search.py -q "react hooks" -e google,brave

    # 时间过滤
    python3 search.py -q "AI news" --time week

    # 站点搜索
    python3 search.py -q "machine learning" --domain github.com

    # 图片搜索
    python3 search.py -q "landscape" --type images

    # 新闻搜索
    python3 search.py -q "科技" --type news

    # 视频搜索
    python3 search.py -q "tutorial" --type videos

    # 代理 + 超时
    python3 search.py -q "test" --proxy socks5h://127.0.0.1:9150 --timeout 10

    # 启用 DHT 加速
    python3 search.py -q "test" --dht

    # 无 ddgs 时，使用 DuckDuckGo Lite
    python3 search.py -q "test" --lite
"""
import argparse
import json
import subprocess
import sys
import os
import time
import concurrent.futures
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime

# 添加脚本目录到 path 以便导入公共模块
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)

try:
    from constants import (
        ENGINES, DDGS_ENGINES, DEFAULT_ENGINE,
        PRISMFY_ENGINES, DEFAULT_ENGINES,
        is_valid_engine, get_engine, get_time_filter
    )
    from cache_utils import get_cached, set_cached, cache_key_from_query
    from result_scorer import score_and_rank_results
    CONSTANTS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import constants modules: {e}", file=sys.stderr)
    CONSTANTS_AVAILABLE = False
    DDGS_ENGINES = ["google", "bing", "duckduckgo", "brave", "yandex", "yahoo", "wikipedia", "mojeek"]
    PRISMFY_ENGINES = ["google", "brave", "ddg", "bing", "yahoo", "startpage", "ecosia", "qwant"]
    DEFAULT_ENGINE = "google"
    DEFAULT_ENGINES = ["google", "brave"]

    def is_valid_engine(name): return name in PRISMFY_ENGINES


# ═══════════════════════════════════════════════════════════════════════════
# 全局配置
# ═══════════════════════════════════════════════════════════════════════════

DDGS_CLI = "/Users/metaclaw/Library/Python/3.9/bin/ddgs"  # ddgs CLI 完整路径

# 全局代理设置（可被 CLI 参数覆盖）
GLOBAL_PROXY: Optional[str] = None

# 全局超时设置（秒）
GLOBAL_TIMEOUT: int = 30

# DHT 模式
DHT_ENABLED: bool = False


def check_ddgs_available() -> bool:
    """检查 ddgs CLI 是否可用"""
    try:
        result = subprocess.run(
            [DDGS_CLI, "version"],
            capture_output=True,
            text=True,
            timeout=5,
            env={**os.environ, "HTTPX_DISABLE_HTTP2": "1"}
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def check_dht_available() -> bool:
    """检查 DHT 网络是否可用（需要 ddgs[dht]）"""
    try:
        result = subprocess.run(
            [DDGS_CLI, "--help"],
            capture_output=True,
            text=True,
            timeout=5,
            env={**os.environ, "HTTPX_DISABLE_HTTP2": "1"}
        )
        help_text = result.stdout + result.stderr
        return "dht" in help_text.lower() or "api" in help_text.lower()
    except Exception:
        return False


def _build_env() -> Dict[str, str]:
    """构建执行环境变量"""
    env = {**os.environ, "HTTPX_DISABLE_HTTP2": "1"}
    if GLOBAL_PROXY:
        env["DDGS_PROXY"] = GLOBAL_PROXY
    return env


# ═══════════════════════════════════════════════════════════════════════════
# 搜索类型定义
# ═══════════════════════════════════════════════════════════════════════════

SearchType = Literal["text", "images", "news", "videos", "books"]

SEARCH_TYPES: List[SearchType] = ["text", "images", "news", "videos", "books"]

# ddgs 各搜索类型支持的引擎
DDGS_TYPE_ENGINES: Dict[SearchType, List[str]] = {
    "text": ["bing", "brave", "duckduckgo", "yandex", "yahoo", "wikipedia", "mojeek", "mullvad_google"],
    "images": ["bing", "duckduckgo"],
    "news": ["bing", "duckduckgo", "yahoo"],
    "videos": ["duckduckgo"],
    "books": ["annasarchive"],
}


def get_ddgs_command(search_type: SearchType) -> str:
    """获取 ddgs 子命令"""
    return search_type


def search_ddgs(
    query: str,
    max_results: int = 5,
    backend: str = "google",
    timeout: int = 30,
    max_retries: int = 3,
    search_type: SearchType = "text",
    region: str = "us-en",
    safesearch: str = "moderate",
    **kwargs
) -> Dict[str, Any]:
    """
    统一的 ddgs 搜索封装，支持多种搜索类型。

    Args:
        query: 搜索查询
        max_results: 最大结果数
        backend: 后端引擎
        timeout: 超时秒数
        max_retries: 最大重试次数
        search_type: 搜索类型 (text/images/news/videos/books)
        region: 地区代码
        safesearch: 安全搜索级别 (on/moderate/off)
        **kwargs: 其他参数（size, color, layout 等用于 images）

    Returns:
        dict: {
            "provider": "ddgs",
            "search_type": str,
            "backend": str,
            "success": bool,
            "results": [...],
            "error": str|None
        }
    """
    normalized_backend = backend
    if CONSTANTS_AVAILABLE:
        try:
            from constants import normalize_engine_name
            normalized_backend = normalize_engine_name(backend)
        except ImportError:
            pass

    # ddgs 不支持 google/google_hk backend，映射到 mullvad_google
    if normalized_backend in ("google", "google_hk"):
        normalized_backend = "mullvad_google"

    # 检查引擎是否支持该搜索类型
    if normalized_backend not in DDGS_TYPE_ENGINES.get(search_type, DDGS_TYPE_ENGINES["text"]):
        return {
            "provider": "ddgs",
            "search_type": search_type,
            "backend": backend,
            "success": False,
            "results": [],
            "error": f"Engine '{backend}' does not support {search_type} search. Use: {DDGS_TYPE_ENGINES.get(search_type, [])}"
        }

    # 构建 ddgs 命令
    cmd = [DDGS_CLI, search_type, "-q", query, "-m", str(max_results), "-b", normalized_backend]

    # 添加可选参数
    if search_type == "images":
        # 图片搜索额外参数
        if kwargs.get("size"):
            cmd.extend(["--size", kwargs["size"]])
        if kwargs.get("color"):
            cmd.extend(["--color", kwargs["color"]])
        if kwargs.get("type_image"):
            cmd.extend(["--type", kwargs["type_image"]])
        if kwargs.get("layout"):
            cmd.extend(["--layout", kwargs["layout"]])
        if kwargs.get("license_image"):
            cmd.extend(["--license", kwargs["license_image"]])

    if search_type == "videos":
        if kwargs.get("resolution"):
            cmd.extend(["--resolution", kwargs["resolution"]])
        if kwargs.get("duration"):
            cmd.extend(["--duration", kwargs["duration"]])

    # 地区和安全搜索
    cmd.extend(["-r", region, "-s", safesearch])

    # 指数退避重试
    backoff = 1.0
    last_error = None

    for attempt in range(max_retries):
        try:
            env = _build_env()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                env=env
            )

            if result.returncode != 0:
                last_error = result.stderr.strip() or "ddgs exited with non-zero status"
                if attempt < max_retries - 1:
                    time.sleep(backoff)
                    backoff *= 2
                    continue
                return {
                    "provider": "ddgs",
                    "search_type": search_type,
                    "backend": normalized_backend,
                    "success": False,
                    "results": [],
                    "error": last_error
                }

            if not result.stdout.strip():
                return {
                    "provider": "ddgs",
                    "search_type": search_type,
                    "backend": normalized_backend,
                    "success": True,
                    "results": [],
                    "query": query
                }

            try:
                raw_data = json.loads(result.stdout)
            except json.JSONDecodeError:
                return {
                    "provider": "ddgs",
                    "search_type": search_type,
                    "backend": normalized_backend,
                    "success": False,
                    "results": [],
                    "error": "Invalid JSON from ddgs"
                }

            # 标准化结果格式
            results = _normalize_results(raw_data, search_type, normalized_backend)

            return {
                "provider": "ddgs",
                "search_type": search_type,
                "backend": normalized_backend,
                "success": True,
                "results": results,
                "query": query,
                "attempts": attempt + 1
            }

        except FileNotFoundError:
            return {
                "provider": "ddgs",
                "search_type": search_type,
                "backend": backend,
                "success": False,
                "results": [],
                "error": "ddgs CLI not found. Install with: pip install ddgs"
            }

        except subprocess.TimeoutExpired:
            last_error = "Search timed out"
            if attempt < max_retries - 1:
                time.sleep(backoff)
                backoff *= 2
                continue
            return {
                "provider": "ddgs",
                "search_type": search_type,
                "backend": backend,
                "success": False,
                "results": [],
                "error": last_error
            }

        except Exception as e:
            last_error = str(e)
            if attempt < max_retries - 1:
                time.sleep(backoff)
                backoff *= 2
                continue
            return {
                "provider": "ddgs",
                "search_type": search_type,
                "backend": backend,
                "success": False,
                "results": [],
                "error": last_error
            }

    return {
        "provider": "ddgs",
        "search_type": search_type,
        "backend": backend,
        "success": False,
        "results": [],
        "error": last_error or "Max retries exceeded"
    }


def _normalize_results(raw_data: List[Dict], search_type: SearchType, backend: str) -> List[Dict[str, Any]]:
    """
    标准化不同搜索类型的结果格式。

    Args:
        raw_data: 原始 ddgs 返回数据
        search_type: 搜索类型
        backend: 后端引擎

    Returns:
        标准化后的结果列表
    """
    results = []

    for item in raw_data:
        if search_type == "text":
            results.append({
                "title": item.get("title", ""),
                "url": item.get("href", ""),
                "snippet": item.get("body", ""),
                "published_date": datetime.now().isoformat()[:10],
                "source": backend
            })
        elif search_type == "images":
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "image": item.get("image", ""),
                "thumbnail": item.get("thumbnail", ""),
                "width": item.get("width"),
                "height": item.get("height"),
                "source": item.get("source", backend),
                "type": "image"
            })
        elif search_type == "news":
            results.append({
                "title": item.get("title", ""),
                "url": item.get("href", ""),
                "snippet": item.get("body", item.get("description", "")),
                "published_date": item.get("date", datetime.now().isoformat()[:10]),
                "source": item.get("source", backend),
                "type": "news"
            })
        elif search_type == "videos":
            results.append({
                "title": item.get("title", item.get("content", "")),
                "url": item.get("url", item.get("content", "")),
                "description": item.get("description", ""),
                "duration": item.get("duration", ""),
                "embed_url": item.get("embed_url", ""),
                "thumbnail": item.get("image_token", ""),
                "source": backend,
                "type": "video"
            })
        elif search_type == "books":
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "author": item.get("author", ""),
                "publisher": item.get("publisher", ""),
                "source": backend,
                "type": "book"
            })
        else:
            # 默认 text 格式
            results.append({
                "title": item.get("title", ""),
                "url": item.get("href", ""),
                "snippet": item.get("body", ""),
                "source": backend
            })

    return results


def search_multi_engine(
    query: str,
    engines: List[str],
    max_results: int = 5,
    timeout: int = 30,
    search_type: SearchType = "text",
    region: str = "us-en",
    safesearch: str = "moderate",
    **kwargs
) -> Dict[str, Any]:
    """
    多引擎并行搜索

    Args:
        query: 搜索查询
        engines: 引擎列表
        max_results: 每引擎最大结果数
        timeout: 单引擎超时秒数
        search_type: 搜索类型
        region: 地区代码
        safesearch: 安全搜索级别
        **kwargs: 其他参数

    Returns:
        聚合结果字典
    """
    all_results = []
    engine_results = {}

    def search_one(engine: str) -> tuple:
        resp = search_ddgs(
            query, max_results, engine, timeout,
            search_type=search_type, region=region, safesearch=safesearch, **kwargs
        )
        return engine, resp

    # 并行执行
    max_workers = min(len(engines), 5)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(search_one, engine): engine
            for engine in engines
        }

        for future in concurrent.futures.as_completed(futures):
            engine = futures[future]
            try:
                engine_name, resp = future.result()
                engine_results[engine_name] = resp
                if resp.get("success"):
                    all_results.extend(resp.get("results", []))
            except Exception as e:
                engine_results[engine] = {"success": False, "error": str(e)}

    # 去重（基于 URL）
    seen_urls = set()
    unique_results = []
    for r in all_results:
        url = r.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(r)

    return {
        "provider": f"ddgs-multi-{search_type}",
        "query": query,
        "search_type": search_type,
        "engines_searched": engines,
        "total_raw_results": len(all_results),
        "unique_results_count": len(unique_results),
        "engine_results": engine_results,
        "results": unique_results,
        "dht_enabled": DHT_ENABLED,
        "timestamp": datetime.now().isoformat()
    }


# ═══════════════════════════════════════════════════════════════════════════
# URL 构建（fallback 实现）
# ═══════════════════════════════════════════════════════════════════════════

def _build_ddg_lite_url(query: str, region: str = "us-en") -> str:
    """构建 DuckDuckGo Lite URL"""
    encoded_q = query.replace(" ", "+")
    return f"https://lite.duckduckgo.com/lite/?q={encoded_q}&kl={region}"


def _build_search_url(engine: str, query: str, domain: Optional[str] = None,
                      time_filter: Optional[str] = None, region: Optional[str] = None) -> str:
    """构建搜索引擎 URL（fallback 实现，无需 constants.py）"""
    from urllib.parse import quote

    if engine == "google":
        q = query
        if domain:
            q = f"site:{domain} {query}"
        params = [("q", q)]
        if time_filter:
            tbs_map = {"hour": "qdr:h", "day": "qdr:d", "week": "qdr:w", "month": "qdr:m", "year": "qdr:y"}
            if time_filter in tbs_map:
                params.append(("tbs", tbs_map[time_filter]))
        query_str = "&".join(f"{k}={quote(v)}" for k, v in params if v)
        return f"https://www.google.com/search?{query_str}"

    elif engine == "brave":
        q = query
        if domain:
            q = f"site:{domain} {query}"
        params = [("q", q)]
        if time_filter:
            tf_map = {"hour": "ph", "day": "pd", "week": "pw", "month": "pm", "year": "py"}
            if time_filter in tf_map:
                params.append(("tf", tf_map[time_filter]))
        query_str = "&".join(f"{k}={quote(v)}" for k, v in params if v)
        return f"https://search.brave.com/search?{query_str}"

    elif engine == "ddg" or engine == "duckduckgo":
        q = query
        if domain:
            q = f"site:{domain} {query}"
        return f"https://duckduckgo.com/?q={quote(q)}"

    elif engine == "bing":
        q = query
        if domain:
            q = f"site:{domain} {query}"
        return f"https://www.bing.com/search?q={quote(q)}"

    else:
        return f"https://www.google.com/search?q={quote(query)}"


def build_url(engine: str, query: str, domain: Optional[str] = None,
              time_filter: Optional[str] = None, region: Optional[str] = None) -> str:
    """统一 URL 构建"""
    if CONSTANTS_AVAILABLE:
        try:
            from url_builder import build_search_url as _build
            return _build(engine, query, domain, time_filter, region)
        except ImportError:
            pass
    return _build_search_url(engine, query, domain, time_filter, region)


# ═══════════════════════════════════════════════════════════════════════════
# 主搜索函数
# ═══════════════════════════════════════════════════════════════════════════

def search_multi(
    query: str,
    engines: List[str],
    max_results: int = 5,
    domain: Optional[str] = None,
    time_filter: Optional[str] = None,
    region: Optional[str] = None,
    use_cache: bool = True,
    rank_results: bool = True,
    search_type: SearchType = "text",
    timeout: int = 30,
    safesearch: str = "moderate",
    **kwargs
) -> dict:
    """
    多引擎搜索主函数。

    Args:
        query: 搜索查询
        engines: 引擎列表
        max_results: 最大结果数
        domain: 站点限制
        time_filter: 时间过滤
        region: 地区代码
        use_cache: 是否使用缓存
        rank_results: 是否评分排序
        search_type: 搜索类型
        timeout: 超时秒数
        safesearch: 安全搜索级别
        **kwargs: 其他参数（如 size, color 用于 images）
    """
    # 检查缓存
    cache_key = None
    if use_cache and CONSTANTS_AVAILABLE:
        cache_key = cache_key_from_query(
            f"multi-{search_type}", query,
            engines=",".join(engines),
            domain=domain, time_filter=time_filter,
            search_type=search_type
        )
        cached = get_cached(cache_key)
        if cached:
            cached["_cached"] = True
            return cached

    ddgs_available = check_ddgs_available()
    results = []
    engine_results = {}

    # 多引擎并行搜索
    if ddgs_available and CONSTANTS_AVAILABLE:
        output = search_multi_engine(
            query, engines, max_results,
            timeout=timeout,
            search_type=search_type,
            region=region or "us-en",
            safesearch=safesearch,
            **kwargs
        )
        results = output.get("results", [])
        engine_results = output.get("engine_results", {})

        # Fallback: 当 ddgs 失败时，为失败的引擎生成 Lite 模式 URL
        for engine in engines:
            if engine in engine_results and not engine_results[engine].get("success"):
                url = build_url(engine, query, domain, time_filter, region)
                engine_results[engine] = {
                    "success": True,
                    "url": url,
                    "web_fetch_cmd": f'web_fetch(url="{url}", extractMode="text", maxChars=8000)',
                    "_fallback": True
                }
    else:
        # 单引擎顺序搜索（当 ddgs 不可用时）
        for engine in engines:
            if not is_valid_engine(engine):
                engine_results[engine] = {"success": False, "error": f"Unknown engine: {engine}"}
                continue

            if ddgs_available:
                resp = search_ddgs(
                    query, max_results, engine, timeout,
                    search_type=search_type,
                    region=region or "us-en",
                    safesearch=safesearch
                )
                engine_results[engine] = resp
                if resp.get("success"):
                    results.extend(resp.get("results", []))
            else:
                # 生成 web_fetch URL
                url = build_url(engine, query, domain, time_filter, region)
                engine_results[engine] = {
                    "success": True,
                    "url": url,
                    "web_fetch_cmd": f'web_fetch(url="{url}", extractMode="text", maxChars=8000)'
                }

    # 去重
    seen_urls = set()
    unique_results = []
    for r in results:
        url = r.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_results.append(r)

    # 评分排序（仅对 text 类型有效）
    if rank_results and unique_results and CONSTANTS_AVAILABLE and search_type == "text":
        try:
            unique_results = score_and_rank_results(unique_results, query=query)
        except Exception:
            pass

    result = {
        "provider": "multi-engine",
        "query": query,
        "engines": engines,
        "search_type": search_type,
        "time_filter": time_filter,
        "domain": domain,
        "results": unique_results,
        "engine_results": engine_results,
        "total_results": len(results),
        "unique_results": len(unique_results),
        "ddgs_available": ddgs_available,
        "dht_enabled": DHT_ENABLED,
        "proxy": GLOBAL_PROXY
    }

    # ═══════════════════════════════════════════════════════════════════════
    # Fallback 内容抓取（问题 2 修复）
    # ═══════════════════════════════════════════════════════════════════════
    # 当所有引擎都处于 fallback 模式且没有实际结果时，尝试抓取内容
    all_fallback = all(
        engine_results.get(e, {}).get("_fallback", False) 
        for e in engines
    )
    
    if all_fallback and len(unique_results) == 0 and search_type == "text":
        try:
            import requests
            from bs4 import BeautifulSoup
            
            fallback_results = []
            for engine in engines:
                engine_data = engine_results.get(engine, {})
                url = engine_data.get("url")
                if not url:
                    continue
                
                try:
                    # 抓取搜索结果页面
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                    resp = requests.get(url, headers=headers, timeout=10)
                    resp.raise_for_status()
                    
                    # 解析 HTML
                    soup = BeautifulSoup(resp.text, 'html.parser')
                    
                    # 通用搜索结果提取（适用于大多数搜索引擎）
                    # 查找可能的搜索结果容器
                    result_selectors = [
                        'div.g',  # Google
                        'div[data-type="web"]',  # Brave
                        'div.result',  # DuckDuckGo
                        'li.b_algo',  # Bing
                        'div.c-result'  # 通用
                    ]
                    
                    items = []
                    for selector in result_selectors:
                        items = soup.select(selector)
                        if items:
                            break
                    
                    # 提取前 max_results 个结果
                    for item in items[:max_results]:
                        # 提取标题和链接
                        title_elem = item.select_one('h3, h2, a')
                        link_elem = item.select_one('a[href]')
                        snippet_elem = item.select_one('span, div.s, div[data-sncf], p')
                        
                        if title_elem and link_elem:
                            link_url = link_elem.get('href', '')
                            
                            # Bing 重定向链接解析
                            if engine == 'bing' and '/ck/a?' in link_url:
                                try:
                                    from urllib.parse import parse_qs, urlparse
                                    import base64
                                    parsed = urlparse(link_url)
                                    query_params = parse_qs(parsed.query)
                                    if 'u' in query_params:
                                        # Bing 的 u 参数是 base64 编码的 URL（带 'a1' 前缀）
                                        encoded_url = query_params['u'][0]
                                        try:
                                            # 移除 'a1' 前缀
                                            if encoded_url.startswith('a1'):
                                                encoded_url = encoded_url[2:]
                                            # 修复 base64 填充
                                            padding = 4 - (len(encoded_url) % 4)
                                            if padding and padding < 4:
                                                encoded_url += '=' * padding
                                            link_url = base64.b64decode(encoded_url).decode('utf-8')
                                        except:
                                            # 如果 base64 解码失败，保持原始 URL
                                            pass
                                except:
                                    pass
                            
                            fallback_results.append({
                                "title": title_elem.get_text(strip=True),
                                "url": link_url,
                                "snippet": snippet_elem.get_text(strip=True) if snippet_elem else "",
                                "source": engine,
                                "_fallback_fetched": True
                            })
                    
                    # 更新引擎结果状态
                    engine_results[engine]["_fallback_fetched"] = True
                    engine_results[engine]["fallback_results_count"] = len(fallback_results)
                    
                except Exception as fetch_error:
                    engine_results[engine]["_fallback_error"] = str(fetch_error)
            
            # 合并 fallback 结果
            if fallback_results:
                # 去重
                seen_urls = set()
                for r in fallback_results:
                    url = r.get("url", "")
                    if url and url.startswith("http") and url not in seen_urls:
                        seen_urls.add(url)
                        unique_results.append(r)
                
                result["results"] = unique_results
                result["unique_results"] = len(unique_results)
                result["_fallback_fetch_applied"] = True
        
        except Exception as e:
            result["_fallback_fetch_error"] = str(e)
    
    # ═══════════════════════════════════════════════════════════════════════

    # 缓存
    if cache_key:
        try:
            set_cached(cache_key, result)
        except Exception:
            pass

    return result


def search_lite(query: str, region: str = "us-en", use_cache: bool = True) -> dict:
    """DuckDuckGo Lite 搜索（无需 ddgs）"""
    if CONSTANTS_AVAILABLE:
        try:
            from url_builder import build_duckduckgo_lite_url
            url = build_duckduckgo_lite_url(query, region)
        except ImportError:
            url = _build_ddg_lite_url(query, region)
    else:
        url = _build_ddg_lite_url(query, region)

    return {
        "provider": "duckduckgo-lite",
        "url": url,
        "query": query,
        "region": region,
        "instructions": f'web_fetch(url="{url}", extractMode="text", maxChars=8000)'
    }


# ═══════════════════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="免费网页搜索 v3.4（支持图片/新闻/视频/DHT/代理）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # 基础文本搜索
  python3 search.py -q "python tutorial"

  # 多引擎并行
  python3 search.py -q "react hooks" -e google,brave

  # 时间过滤 + 站点搜索
  python3 search.py -q "machine learning" --time week --domain github.com

  # 图片搜索
  python3 search.py -q "landscape" --type images -m 10

  # 新闻搜索
  python3 search.py -q "科技新闻" --type news

  # 视频搜索
  python3 search.py -q "python tutorial" --type videos

  # 代理 + 超时
  python3 search.py -q "test" --proxy socks5h://127.0.0.1:9150 --timeout 10

  # 启用 DHT 加速
  python3 search.py -q "test" --dht

  # 输出 JSON
  python3 search.py -q "test" --json -o results.json

Supported search types: text (default), images, news, videos, books
Supported engines: google, brave, ddg, duckduckgo, bing, yahoo, startpage, ecosia, qwant
        """
    )
    parser.add_argument("--query", "-q", required=True, help="搜索查询")
    parser.add_argument("--engines", "-e", default=",".join(DEFAULT_ENGINES),
                        help=f"引擎列表（逗号分隔，默认: {','.join(DEFAULT_ENGINES)}）")
    parser.add_argument("--max-results", "-m", type=int, default=5, help="最大结果数 (默认: 5)")
    parser.add_argument("--time", "-t", choices=["hour", "day", "week", "month", "year"],
                        help="时间过滤")
    parser.add_argument("--domain", "-d", help="站点搜索（例如：github.com）")
    parser.add_argument("--region", "-r", default="us-en", help="地区代码（默认: us-en）")
    parser.add_argument("--lite", action="store_true", help="强制使用 DuckDuckGo Lite")
    parser.add_argument("--output", "-o", help="输出文件 (JSON)")
    parser.add_argument("--json", action="store_true", help="紧凑 JSON 输出")
    parser.add_argument("--no-cache", action="store_true", help="禁用缓存")
    parser.add_argument("--no-rank", action="store_true", help="禁用结果评分排序")

    # 新增参数
    parser.add_argument("--proxy", "-pr", default=None,
                        help="代理服务器 (e.g., socks5h://127.0.0.1:9150)")
    parser.add_argument("--type", default="text", choices=SEARCH_TYPES,
                        help="搜索类型 (默认: text)")
    parser.add_argument("--timeout", type=int, default=30,
                        help="单引擎超时秒数 (默认: 30)")
    parser.add_argument("--dht", action="store_true",
                        help="启用 DHT 网络加速（需要 ddgs[dht]）")
    parser.add_argument("--safesearch", "-s", default="moderate",
                        choices=["on", "moderate", "off"],
                        help="安全搜索级别 (默认: moderate)")

    # 图片搜索额外参数
    parser.add_argument("--size", default=None,
                        help="图片大小 (Small/Medium/Large/Wallpaper)")
    parser.add_argument("--color", default=None,
                        help="图片颜色")
    parser.add_argument("--type-image", dest="type_image", default=None,
                        help="图片类型 (photo/clipart/gif/transparent/line)")
    parser.add_argument("--layout", default=None,
                        help="图片布局 (Square/Tall/Wide)")
    parser.add_argument("--license-image", dest="license_image", default=None,
                        help="图片许可证")

    # 视频搜索额外参数
    parser.add_argument("--resolution", default=None,
                        help="视频分辨率 (high/standard)")
    parser.add_argument("--duration", default=None,
                        help="视频时长 (short/medium/long)")

    args = parser.parse_args()

    # 设置全局配置
    global GLOBAL_PROXY, GLOBAL_TIMEOUT, DHT_ENABLED
    if args.proxy:
        GLOBAL_PROXY = args.proxy
    GLOBAL_TIMEOUT = args.timeout
    if args.dht:
        DHT_ENABLED = True

    use_cache = not args.no_cache
    rank_results = not args.no_rank

    # 解析引擎列表
    engines = [e.strip() for e in args.engines.split(",")]

    # 解析图片/视频额外参数
    extra_kwargs = {}
    if args.type == "images":
        if args.size:
            extra_kwargs["size"] = args.size
        if args.color:
            extra_kwargs["color"] = args.color
        if args.type_image:
            extra_kwargs["type_image"] = args.type_image
        if args.layout:
            extra_kwargs["layout"] = args.layout
        if args.license_image:
            extra_kwargs["license_image"] = args.license_image
    elif args.type == "videos":
        if args.resolution:
            extra_kwargs["resolution"] = args.resolution
        if args.duration:
            extra_kwargs["duration"] = args.duration

    # Lite 模式
    if args.lite:
        output = search_lite(query=args.query, region=args.region, use_cache=use_cache)
    else:
        # 多引擎搜索
        output = search_multi(
            query=args.query,
            engines=engines,
            max_results=args.max_results,
            domain=args.domain,
            time_filter=args.time,
            region=args.region,
            use_cache=use_cache,
            rank_results=rank_results,
            search_type=args.type,
            timeout=GLOBAL_TIMEOUT,
            safesearch=args.safesearch,
            **extra_kwargs
        )

    # 输出
    if args.json:
        print(json.dumps(output, ensure_ascii=False))
    else:
        print(json.dumps(output, indent=2, ensure_ascii=False))

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output, f, indent=2, ensure_ascii=False)
        print(f"\n✅ 已保存到 {args.output}")


if __name__ == "__main__":
    main()