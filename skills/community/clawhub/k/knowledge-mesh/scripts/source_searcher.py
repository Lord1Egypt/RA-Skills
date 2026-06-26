#!/usr/bin/env python3
"""
knowledge-mesh 知识源搜索模块

统一搜索 GitHub Discussions/Issues、Stack Overflow、Discord、
Confluence、Notion、Slack 等平台，返回标准化搜索结果。

用法:
    python3 source_searcher.py --action search --data '{"query":"python async"}'
    python3 source_searcher.py --action search-source --data '{"query":"fastapi","source":"github"}'
    python3 source_searcher.py --action list-sources
    python3 source_searcher.py --action test-source --data '{"source":"github"}'
"""

import json
import os
import re
import sys
import urllib.request
import urllib.error
import urllib.parse
from datetime import datetime
from typing import Any, Dict, List, Optional

from utils import (
    SUPPORTED_SOURCES,
    SOURCE_DISPLAY_NAMES,
    SOURCE_ENV_KEYS,
    check_subscription,
    check_search_quota,
    increment_search_count,
    clean_html,
    days_ago,
    generate_id,
    load_input_data,
    now_iso,
    output_error,
    output_success,
    parse_common_args,
    parse_iso_datetime,
    read_json_file,
    truncate_text,
    write_json_file,
    get_data_file,
)


# ============================================================
# 常量
# ============================================================

# 搜索配置文件
SOURCES_CONFIG_FILE = "sources_config.json"

# 默认请求超时秒数
REQUEST_TIMEOUT = 15

# 各平台 API 基础地址
GITHUB_API_BASE = "https://api.github.com"
STACKOVERFLOW_API_BASE = "https://api.stackexchange.com/2.3"
DISCORD_API_BASE = "https://discord.com/api/v10"
NOTION_API_BASE = "https://api.notion.com/v1"
BAIDU_SEARCH_API = "https://www.baidu.com/s"


# ============================================================
# HTTP 请求辅助
# ============================================================

def _http_get(url: str, headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """发送 HTTP GET 请求并返回 JSON 响应。

    Args:
        url: 请求地址。
        headers: 可选的请求头。

    Returns:
        解析后的 JSON 字典。

    Raises:
        RuntimeError: 请求失败时抛出。
    """
    req = urllib.request.Request(url, method="GET")
    req.add_header("User-Agent", "knowledge-mesh/1.0")
    req.add_header("Accept", "application/json")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)

    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP 请求失败: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"网络请求失败: {e.reason}")
    except json.JSONDecodeError:
        raise RuntimeError("响应解析失败：非有效 JSON")


def _http_post(url: str, payload: Dict[str, Any],
               headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    """发送 HTTP POST 请求并返回 JSON 响应。

    Args:
        url: 请求地址。
        payload: 请求体数据。
        headers: 可选的请求头。

    Returns:
        解析后的 JSON 字典。

    Raises:
        RuntimeError: 请求失败时抛出。
    """
    body_bytes = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=body_bytes, method="POST")
    req.add_header("User-Agent", "knowledge-mesh/1.0")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)

    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
            resp_body = resp.read().decode("utf-8")
            return json.loads(resp_body)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP 请求失败: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"网络请求失败: {e.reason}")
    except json.JSONDecodeError:
        raise RuntimeError("响应解析失败：非有效 JSON")


# ============================================================
# 统一搜索结果格式
# ============================================================

def _make_result(
    source: str,
    title: str,
    url: str,
    snippet: str,
    author: str = "",
    created_at: str = "",
    score: float = 0.0,
    tags: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """构造标准化搜索结果条目。

    Args:
        source: 来源平台名称。
        title: 结果标题。
        url: 结果链接。
        snippet: 内容摘要。
        author: 作者名。
        created_at: 创建时间。
        score: 相关性分数。
        tags: 标签列表。

    Returns:
        标准化的搜索结果字典。
    """
    return {
        "id": generate_id("SR"),
        "source": source,
        "title": title,
        "url": url,
        "snippet": truncate_text(snippet, 300),
        "author": author,
        "created_at": created_at,
        "score": score,
        "tags": tags or [],
    }


# ============================================================
# GitHub 搜索适配器
# ============================================================

def _search_github(query: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """搜索 GitHub Issues 和 Discussions。

    使用 GitHub Search API /search/issues 接口，支持搜索
    Issues 和 Pull Requests（Discussions 需要 GraphQL）。

    Args:
        query: 搜索关键词。
        max_results: 最大返回结果数。

    Returns:
        标准化搜索结果列表。
    """
    token = os.environ.get("KM_GITHUB_TOKEN", "")
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"

    # 搜索 Issues 和 Discussions
    encoded_query = urllib.parse.quote(query)
    url = f"{GITHUB_API_BASE}/search/issues?q={encoded_query}&per_page={max_results}&sort=relevance"

    try:
        data = _http_get(url, headers=headers)
    except RuntimeError as e:
        return [_make_result("github", f"GitHub 搜索失败: {e}", "", str(e))]

    results = []
    items = data.get("items", [])
    for item in items[:max_results]:
        title = item.get("title", "")
        html_url = item.get("html_url", "")
        body = item.get("body", "") or ""
        user = item.get("user", {})
        author = user.get("login", "") if user else ""
        created = item.get("created_at", "")
        score_val = item.get("score", 0.0)
        labels = [lb.get("name", "") for lb in item.get("labels", [])]

        results.append(_make_result(
            source="github",
            title=title,
            url=html_url,
            snippet=clean_html(body),
            author=author,
            created_at=created,
            score=float(score_val),
            tags=labels,
        ))

    return results


# ============================================================
# Stack Overflow 搜索适配器
# ============================================================

def _search_stackoverflow(query: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """搜索 Stack Overflow 问题。

    使用 Stack Exchange API v2.3 /search/advanced 接口。

    Args:
        query: 搜索关键词。
        max_results: 最大返回结果数。

    Returns:
        标准化搜索结果列表。
    """
    api_key = os.environ.get("KM_STACKOVERFLOW_KEY", "")
    params = {
        "order": "desc",
        "sort": "relevance",
        "q": query,
        "site": "stackoverflow",
        "pagesize": str(min(max_results, 30)),
        "filter": "withbody",
    }
    if api_key:
        params["key"] = api_key

    query_string = urllib.parse.urlencode(params)
    url = f"{STACKOVERFLOW_API_BASE}/search/advanced?{query_string}"

    try:
        data = _http_get(url)
    except RuntimeError as e:
        return [_make_result("stackoverflow", f"Stack Overflow 搜索失败: {e}", "", str(e))]

    results = []
    items = data.get("items", [])
    for item in items[:max_results]:
        title = item.get("title", "")
        link = item.get("link", "")
        body = clean_html(item.get("body", "") or "")
        owner = item.get("owner", {})
        author = owner.get("display_name", "") if owner else ""
        # Stack Overflow 时间戳为 Unix 秒
        creation_date = item.get("creation_date", 0)
        created_at = ""
        if creation_date:
            try:
                created_at = datetime.utcfromtimestamp(creation_date).strftime("%Y-%m-%dT%H:%M:%S")
            except (OSError, ValueError):
                created_at = ""
        score_val = float(item.get("score", 0))
        tags = item.get("tags", [])

        results.append(_make_result(
            source="stackoverflow",
            title=clean_html(title),
            url=link,
            snippet=body,
            author=author,
            created_at=created_at,
            score=score_val,
            tags=tags,
        ))

    return results


# ============================================================
# Discord 搜索适配器
# ============================================================

def _search_discord(query: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """搜索 Discord 频道消息。

    使用 Discord Bot API /channels/{id}/messages 接口。
    需要设置 KM_DISCORD_BOT_TOKEN 和 KM_DISCORD_CHANNEL_ID。

    Args:
        query: 搜索关键词。
        max_results: 最大返回结果数。

    Returns:
        标准化搜索结果列表。
    """
    token = os.environ.get("KM_DISCORD_BOT_TOKEN", "")
    channel_id = os.environ.get("KM_DISCORD_CHANNEL_ID", "")

    if not token:
        return [_make_result("discord", "Discord 未配置", "", "请设置 KM_DISCORD_BOT_TOKEN 环境变量")]
    if not channel_id:
        return [_make_result("discord", "Discord 频道未配置", "", "请设置 KM_DISCORD_CHANNEL_ID 环境变量")]

    headers = {
        "Authorization": f"Bot {token}",
    }

    url = f"{DISCORD_API_BASE}/channels/{channel_id}/messages?limit={min(max_results, 100)}"

    try:
        messages = _http_get(url, headers=headers)
    except RuntimeError as e:
        return [_make_result("discord", f"Discord 搜索失败: {e}", "", str(e))]

    if not isinstance(messages, list):
        return []

    # 在客户端过滤匹配消息
    query_lower = query.lower()
    keywords = query_lower.split()
    results = []

    for msg in messages:
        content = msg.get("content", "")
        if not content:
            continue
        content_lower = content.lower()
        # 检查是否包含任一关键词
        if not any(kw in content_lower for kw in keywords):
            continue

        msg_id = msg.get("id", "")
        author_info = msg.get("author", {})
        author = author_info.get("username", "") if author_info else ""
        timestamp = msg.get("timestamp", "")
        msg_url = f"https://discord.com/channels/{channel_id}/{msg_id}"

        # 简单相关性评分：匹配关键词数量
        match_count = sum(1 for kw in keywords if kw in content_lower)
        score_val = match_count / max(len(keywords), 1)

        results.append(_make_result(
            source="discord",
            title=truncate_text(content, 80),
            url=msg_url,
            snippet=content,
            author=author,
            created_at=timestamp,
            score=score_val,
        ))

        if len(results) >= max_results:
            break

    return results


# ============================================================
# Confluence 搜索适配器
# ============================================================

def _search_confluence(query: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """搜索 Confluence 内容。

    使用 Confluence REST API /wiki/rest/api/content/search 接口。

    Args:
        query: 搜索关键词。
        max_results: 最大返回结果数。

    Returns:
        标准化搜索结果列表。
    """
    base_url = os.environ.get("KM_CONFLUENCE_URL", "")
    token = os.environ.get("KM_CONFLUENCE_TOKEN", "")

    if not base_url:
        return [_make_result("confluence", "Confluence 未配置", "", "请设置 KM_CONFLUENCE_URL 环境变量")]
    if not token:
        return [_make_result("confluence", "Confluence 未认证", "", "请设置 KM_CONFLUENCE_TOKEN 环境变量")]

    # 构造 CQL 查询
    cql = urllib.parse.quote(f'text ~ "{query}"')
    url = f"{base_url.rstrip('/')}/wiki/rest/api/content/search?cql={cql}&limit={max_results}&expand=body.view,version"

    headers = {
        "Authorization": f"Bearer {token}",
    }

    try:
        data = _http_get(url, headers=headers)
    except RuntimeError as e:
        return [_make_result("confluence", f"Confluence 搜索失败: {e}", "", str(e))]

    results = []
    items = data.get("results", [])
    for item in items[:max_results]:
        title = item.get("title", "")
        content_id = item.get("id", "")
        page_url = f"{base_url.rstrip('/')}/wiki{item.get('_links', {}).get('webui', '')}"

        # 提取正文摘要
        body_view = item.get("body", {}).get("view", {}).get("value", "")
        snippet = clean_html(body_view)

        # 版本信息中的作者和时间
        version = item.get("version", {})
        author = ""
        created_at = ""
        if version:
            by_info = version.get("by", {})
            author = by_info.get("displayName", "") if by_info else ""
            created_at = version.get("when", "")

        results.append(_make_result(
            source="confluence",
            title=title,
            url=page_url,
            snippet=snippet,
            author=author,
            created_at=created_at,
            score=1.0,
            tags=[item.get("type", "page")],
        ))

    return results


# ============================================================
# Notion 搜索适配器
# ============================================================

def _search_notion(query: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """搜索 Notion 页面和数据库。

    使用 Notion API POST /v1/search 接口。

    Args:
        query: 搜索关键词。
        max_results: 最大返回结果数。

    Returns:
        标准化搜索结果列表。
    """
    token = os.environ.get("KM_NOTION_TOKEN", "")

    if not token:
        return [_make_result("notion", "Notion 未配置", "", "请设置 KM_NOTION_TOKEN 环境变量")]

    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
    }

    payload = {
        "query": query,
        "page_size": min(max_results, 100),
    }

    url = f"{NOTION_API_BASE}/search"

    try:
        data = _http_post(url, payload, headers=headers)
    except RuntimeError as e:
        return [_make_result("notion", f"Notion 搜索失败: {e}", "", str(e))]

    results = []
    items = data.get("results", [])
    for item in items[:max_results]:
        obj_type = item.get("object", "")
        page_id = item.get("id", "")
        page_url = item.get("url", "") or f"https://notion.so/{page_id.replace('-', '')}"

        # 提取标题
        title = ""
        properties = item.get("properties", {})
        if "title" in properties:
            title_arr = properties["title"].get("title", [])
            if title_arr:
                title = title_arr[0].get("plain_text", "")
        elif "Name" in properties:
            name_info = properties["Name"]
            if name_info.get("type") == "title":
                title_arr = name_info.get("title", [])
                if title_arr:
                    title = title_arr[0].get("plain_text", "")

        if not title:
            title = f"Notion {obj_type} {page_id[:8]}"

        # 创建时间和作者
        created_at = item.get("created_time", "")
        created_by = item.get("created_by", {})
        author = ""
        if created_by:
            author = created_by.get("name", "") or created_by.get("id", "")

        results.append(_make_result(
            source="notion",
            title=title,
            url=page_url,
            snippet=f"Notion {obj_type}: {title}",
            author=author,
            created_at=created_at,
            score=1.0,
            tags=[obj_type],
        ))

    return results


# ============================================================
# Slack 搜索适配器
# ============================================================

def _search_slack(query: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """搜索 Slack 消息。

    使用 Slack Web API search.messages 接口。

    Args:
        query: 搜索关键词。
        max_results: 最大返回结果数。

    Returns:
        标准化搜索结果列表。
    """
    token = os.environ.get("KM_SLACK_TOKEN", "")

    if not token:
        return [_make_result("slack", "Slack 未配置", "", "请设置 KM_SLACK_TOKEN 环境变量")]

    headers = {
        "Authorization": f"Bearer {token}",
    }

    encoded_query = urllib.parse.quote(query)
    url = f"https://slack.com/api/search.messages?query={encoded_query}&count={max_results}&sort=score"

    try:
        data = _http_get(url, headers=headers)
    except RuntimeError as e:
        return [_make_result("slack", f"Slack 搜索失败: {e}", "", str(e))]

    if not data.get("ok", False):
        error_msg = data.get("error", "未知错误")
        return [_make_result("slack", f"Slack API 错误: {error_msg}", "", error_msg)]

    results = []
    messages_data = data.get("messages", {})
    matches = messages_data.get("matches", [])

    for msg in matches[:max_results]:
        text = msg.get("text", "")
        permalink = msg.get("permalink", "")
        username = msg.get("username", "")
        ts = msg.get("ts", "")
        channel_info = msg.get("channel", {})
        channel_name = channel_info.get("name", "") if isinstance(channel_info, dict) else ""

        # 将 Slack 时间戳转换为 ISO 格式
        created_at = ""
        if ts:
            try:
                dt = datetime.utcfromtimestamp(float(ts))
                created_at = dt.strftime("%Y-%m-%dT%H:%M:%S")
            except (ValueError, OSError):
                created_at = ""

        tags = [f"#{channel_name}"] if channel_name else []

        results.append(_make_result(
            source="slack",
            title=truncate_text(text, 80),
            url=permalink,
            snippet=text,
            author=username,
            created_at=created_at,
            score=1.0,
            tags=tags,
        ))

    return results


# ============================================================
# 百度搜索适配器
# ============================================================

def _search_baidu(query: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """搜索百度，获取中文内容搜索结果。

    使用百度搜索 API 或 Web 端点，解析结果为统一格式。
    需要设置 KM_BAIDU_API_KEY 环境变量。

    Args:
        query: 搜索关键词。
        max_results: 最大返回结果数。

    Returns:
        标准化搜索结果列表。
    """
    api_key = os.environ.get("KM_BAIDU_API_KEY", "")

    # 使用百度开发者搜索 API
    encoded_query = urllib.parse.quote(query)
    params = {
        "wd": query,
        "rn": str(min(max_results, 50)),
        "ie": "utf-8",
        "oe": "utf-8",
    }
    if api_key:
        params["apikey"] = api_key

    query_string = urllib.parse.urlencode(params)
    url = f"https://api.baidu.com/json/custom/tongji?{query_string}"

    # 备用：使用百度搜索结果页面解析
    headers = {
        "User-Agent": "knowledge-mesh/1.0",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    try:
        data = _http_get(url, headers=headers)
    except RuntimeError:
        # API 不可用时返回空结果
        return [_make_result(
            "baidu",
            "百度搜索需要配置 API",
            "",
            "请设置 KM_BAIDU_API_KEY 环境变量以启用百度搜索",
        )]

    results = []
    items = data.get("results", data.get("items", []))
    if not isinstance(items, list):
        items = []

    for item in items[:max_results]:
        title = item.get("title", "")
        link = item.get("url", item.get("link", ""))
        abstract = item.get("abstract", item.get("snippet", item.get("description", "")))
        author = item.get("source", item.get("author", ""))
        created_at = item.get("date", item.get("created_at", ""))
        score_val = float(item.get("score", 0.5))

        # 清理 HTML 标签
        title = clean_html(title)
        abstract = clean_html(abstract)

        results.append(_make_result(
            source="baidu",
            title=title,
            url=link,
            snippet=abstract,
            author=author,
            created_at=created_at,
            score=score_val,
            tags=["baidu"],
        ))

    return results


# ============================================================
# Obsidian 搜索适配器
# ============================================================

def _search_obsidian(query: str, max_results: int = 20) -> List[Dict[str, Any]]:
    """搜索 Obsidian 知识库。

    委托给 obsidian_connector 模块执行搜索。

    Args:
        query: 搜索关键词。
        max_results: 最大返回结果数。

    Returns:
        标准化搜索结果列表。
    """
    try:
        from obsidian_connector import search_obsidian
        results = search_obsidian(query, max_results=max_results)
        return results
    except ImportError:
        return [_make_result(
            "obsidian",
            "Obsidian 连接器未安装",
            "",
            "obsidian_connector 模块不可用",
        )]
    except Exception as e:
        return [_make_result(
            "obsidian",
            f"Obsidian 搜索失败: {e}",
            "",
            str(e),
        )]


# ============================================================
# 搜索适配器路由
# ============================================================

_SOURCE_ADAPTERS = {
    "github": _search_github,
    "stackoverflow": _search_stackoverflow,
    "discord": _search_discord,
    "confluence": _search_confluence,
    "notion": _search_notion,
    "slack": _search_slack,
    "baidu": _search_baidu,
    "obsidian": _search_obsidian,
}

# 免费版可用的知识源
_FREE_SOURCES = {"github", "stackoverflow", "baidu", "obsidian"}


def _get_available_sources() -> List[str]:
    """获取当前订阅等级下可用的知识源列表。

    Returns:
        可用知识源名称列表。
    """
    sub = check_subscription()
    features = sub.get("features", [])

    available = []
    for source in SUPPORTED_SOURCES:
        feature_name = f"{source}_search"
        # basic_search 对应免费源
        if source in _FREE_SOURCES or feature_name in features:
            available.append(source)

    return available


def _get_configured_sources() -> List[str]:
    """获取已配置认证凭据的知识源列表。

    Returns:
        已配置的知识源名称列表。
    """
    configured = []
    for source in SUPPORTED_SOURCES:
        env_key = SOURCE_ENV_KEYS.get(source, "")
        if env_key and os.environ.get(env_key, ""):
            configured.append(source)
        elif source == "stackoverflow":
            # Stack Overflow 不需要 API key 也能搜索（有速率限制）
            configured.append(source)
    return configured


# ============================================================
# 操作实现
# ============================================================

def action_search(data: Dict[str, Any]) -> None:
    """统一搜索：查询所有已配置的可用知识源。

    Args:
        data: 包含 query（搜索关键词）的字典，可选 max_results。
    """
    query = data.get("query", "").strip()
    if not query:
        output_error("请提供搜索关键词（query）", code="VALIDATION_ERROR")
        return

    # 检查搜索配额
    if not check_search_quota():
        return

    sub = check_subscription()
    max_results = min(data.get("max_results", 20), sub.get("max_results", 20))
    available = _get_available_sources()
    configured = _get_configured_sources()

    # 取交集：既可用又已配置
    sources_to_search = [s for s in available if s in configured]

    if not sources_to_search:
        output_error(
            "没有可用的知识源。请先配置至少一个知识源的 API 凭据。",
            code="NO_SOURCES",
        )
        return

    all_results = []
    source_stats = {}
    errors = []

    for source in sources_to_search:
        adapter = _SOURCE_ADAPTERS.get(source)
        if not adapter:
            continue

        try:
            results = adapter(query, max_results=max_results)
            source_stats[source] = len(results)
            all_results.extend(results)
        except Exception as e:
            errors.append(f"{SOURCE_DISPLAY_NAMES.get(source, source)}: {e}")
            source_stats[source] = 0

    # 按分数降序排列
    all_results.sort(key=lambda r: r.get("score", 0), reverse=True)
    all_results = all_results[:max_results]

    # 递增搜索计数
    increment_search_count()

    # 记录查询到自学习引擎
    try:
        from learning_engine import record_query_data
        record_query_data(query, sources_to_search, source_stats)
    except (ImportError, Exception):
        pass  # 自学习模块不可用时静默跳过

    output_success({
        "query": query,
        "total": len(all_results),
        "sources_searched": sources_to_search,
        "source_stats": source_stats,
        "results": all_results,
        "errors": errors if errors else None,
    })


def action_search_source(data: Dict[str, Any]) -> None:
    """搜索指定的单个知识源。

    Args:
        data: 包含 query 和 source 的字典。
    """
    query = data.get("query", "").strip()
    source = data.get("source", "").strip().lower()

    if not query:
        output_error("请提供搜索关键词（query）", code="VALIDATION_ERROR")
        return
    if not source:
        output_error("请指定知识源（source）", code="VALIDATION_ERROR")
        return

    if source not in SUPPORTED_SOURCES:
        valid = "、".join(SUPPORTED_SOURCES)
        output_error(f"不支持的知识源: {source}，支持: {valid}", code="INVALID_SOURCE")
        return

    # 检查订阅权限
    available = _get_available_sources()
    if source not in available:
        output_error(
            f"{SOURCE_DISPLAY_NAMES.get(source, source)} 搜索为付费版功能，请升级至付费版（¥129/月）。",
            code="SUBSCRIPTION_REQUIRED",
        )
        return

    # 检查搜索配额
    if not check_search_quota():
        return

    sub = check_subscription()
    max_results = min(data.get("max_results", 20), sub.get("max_results", 20))

    adapter = _SOURCE_ADAPTERS.get(source)
    if not adapter:
        output_error(f"知识源适配器不存在: {source}", code="ADAPTER_ERROR")
        return

    try:
        results = adapter(query, max_results=max_results)
    except Exception as e:
        output_error(f"搜索失败: {e}", code="SEARCH_ERROR")
        return

    # 递增搜索计数
    increment_search_count()

    output_success({
        "query": query,
        "source": source,
        "total": len(results),
        "results": results,
    })


def action_list_sources(data: Optional[Dict[str, Any]] = None) -> None:
    """列出所有支持的知识源及其配置状态。"""
    available = _get_available_sources()
    configured = _get_configured_sources()
    sub = check_subscription()

    sources_info = []
    for source in SUPPORTED_SOURCES:
        env_key = SOURCE_ENV_KEYS.get(source, "")
        is_available = source in available
        is_configured = source in configured

        sources_info.append({
            "name": source,
            "display_name": SOURCE_DISPLAY_NAMES.get(source, source),
            "env_key": env_key,
            "available": is_available,
            "configured": is_configured,
            "status": "ready" if (is_available and is_configured) else
                      "not_configured" if is_available else "paid_only",
        })

    output_success({
        "subscription_tier": sub["tier"],
        "total_sources": len(SUPPORTED_SOURCES),
        "available_count": len(available),
        "configured_count": len(configured),
        "sources": sources_info,
    })


def action_test_source(data: Dict[str, Any]) -> None:
    """测试指定知识源的连接状态。

    Args:
        data: 包含 source 的字典。
    """
    source = data.get("source", "").strip().lower()

    if not source:
        output_error("请指定知识源（source）", code="VALIDATION_ERROR")
        return

    if source not in SUPPORTED_SOURCES:
        valid = "、".join(SUPPORTED_SOURCES)
        output_error(f"不支持的知识源: {source}，支持: {valid}", code="INVALID_SOURCE")
        return

    env_key = SOURCE_ENV_KEYS.get(source, "")
    token = os.environ.get(env_key, "") if env_key else ""

    # 测试连接
    test_result = {
        "source": source,
        "display_name": SOURCE_DISPLAY_NAMES.get(source, source),
        "env_key": env_key,
        "token_configured": bool(token),
    }

    if source == "github":
        if token:
            try:
                data_resp = _http_get(f"{GITHUB_API_BASE}/user", headers={"Authorization": f"token {token}"})
                test_result["status"] = "connected"
                test_result["user"] = data_resp.get("login", "")
            except RuntimeError as e:
                test_result["status"] = "error"
                test_result["error"] = str(e)
        else:
            test_result["status"] = "no_token"
            test_result["message"] = "GitHub 搜索可在无 Token 下使用，但有速率限制"

    elif source == "stackoverflow":
        # Stack Overflow 不需要强制 API key
        test_result["status"] = "available"
        test_result["message"] = "Stack Overflow API 可直接访问（API key 可选）"

    elif source == "confluence":
        base_url = os.environ.get("KM_CONFLUENCE_URL", "")
        if not base_url:
            test_result["status"] = "not_configured"
            test_result["error"] = "请设置 KM_CONFLUENCE_URL 环境变量"
        elif not token:
            test_result["status"] = "no_token"
            test_result["error"] = "请设置 KM_CONFLUENCE_TOKEN 环境变量"
        else:
            test_result["status"] = "configured"
            test_result["base_url"] = base_url

    else:
        if token:
            test_result["status"] = "configured"
        else:
            test_result["status"] = "no_token"
            test_result["error"] = f"请设置 {env_key} 环境变量"

    output_success(test_result)


# ============================================================
# 主入口
# ============================================================

def main() -> None:
    """主函数：解析命令行参数并分发操作。"""
    parser = parse_common_args("knowledge-mesh 知识源搜索")
    args = parser.parse_args()

    action = args.action.lower()

    try:
        data = load_input_data(args)
    except ValueError as e:
        output_error(str(e), code="INPUT_ERROR")
        return

    actions = {
        "search": lambda: action_search(data or {}),
        "search-source": lambda: action_search_source(data or {}),
        "list-sources": lambda: action_list_sources(data),
        "test-source": lambda: action_test_source(data or {}),
    }

    handler = actions.get(action)
    if handler:
        handler()
    else:
        valid_actions = "、".join(actions.keys())
        output_error(f"未知操作: {action}，支持的操作: {valid_actions}", code="INVALID_ACTION")


if __name__ == "__main__":
    main()
