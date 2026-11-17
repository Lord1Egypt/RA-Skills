#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MCP Server — stdio JSON-RPC 2.0 服务（V1.7 新增）

功能：将 privacy-search 暴露为 MCP Server，供 Claude Code / Cursor / n8n 等
      MCP Client 直接挂载。搜索能力成为任何 Agent 的即插组件。

暴露工具：
  1. search     多引擎并行搜索
  2. synthesize Perplexity 式答案合成（引用+正文抓取+citation）
  3. fetch      抓取网页正文

遵循死规则 9：基础功能自研，外部 API 按需接入，必须提供降级方案。
遵循死规则 10：MCP Server 需控制资源占用，不影响用户电脑。
遵循死规则 13：不生成 __pycache__。

架构：纯标准库实现，不依赖外部 MCP 库。
      协议为公开的 JSON-RPC 2.0 标准，不复制任何第三方代码。

运行方式：
  python -m scripts.mcp_server
  # 或
  python scripts/mcp_server.py

配置（config.yaml）：
  mcp_server:
    enabled: true
    timeout: 30          # 单次工具调用超时（秒）
    max_results: 10      # search 工具默认最大结果数
    max_sources: 5       # synthesize 工具默认最大引用来源数
"""

import json
import os
import sys
import time
import traceback
from typing import Any, Dict, List, Optional

sys.dont_write_bytecode = True


# ============================================================
# JSON-RPC 2.0 消息处理
# ============================================================

def _read_message() -> Optional[Dict[str, Any]]:
    """
    从 stdin 读取一条 JSON-RPC 消息（Content-Length 帧格式）

    MCP 协议使用 Content-Length 帧格式：
      Content-Length: <length>\r\n
      \r\n
      <json body>
    """
    content_length = None
    while True:
        line = sys.stdin.readline()
        if not line:
            return None  # EOF
        line = line.strip()
        if not line:
            break  # 空行表示头部结束
        if line.lower().startswith("content-length:"):
            content_length = int(line.split(":", 1)[1].strip())
    if content_length is None:
        return None
    body = sys.stdin.read(content_length)
    if not body:
        return None
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return None


def _write_message(message: Dict[str, Any]) -> None:
    """向 stdout 写入一条 JSON-RPC 消息（Content-Length 帧格式）"""
    body = json.dumps(message, ensure_ascii=False)
    length = len(body.encode("utf-8"))
    sys.stdout.write(f"Content-Length: {length}\r\n\r\n{body}")
    sys.stdout.flush()


def _make_response(request_id: Any, result: Any) -> Dict[str, Any]:
    """构造 JSON-RPC 2.0 成功响应"""
    return {
        "jsonrpc": "2.0",
        "id": request_id,
        "result": result,
    }


def _make_error(request_id: Any, code: int, message: str, data: Any = None) -> Dict[str, Any]:
    """构造 JSON-RPC 2.0 错误响应"""
    err = {
        "jsonrpc": "2.0",
        "id": request_id,
        "error": {"code": code, "message": message},
    }
    if data is not None:
        err["error"]["data"] = data
    return err


# ============================================================
# MCP 协议方法
# ============================================================

# MCP 标准错误码
PARSE_ERROR = -32700
INVALID_REQUEST = -32600
METHOD_NOT_FOUND = -32601
INVALID_PARAMS = -32602
INTERNAL_ERROR = -32603


def _handle_initialize(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理 MCP initialize 请求

    返回服务器信息、能力和工具 schema。
    """
    try:
        from version_util import get_current_version
        version = get_current_version()
    except Exception:
        version = "1.7.0"

    return {
        "protocolVersion": "2024-11-05",
        "capabilities": {
            "tools": {},
        },
        "serverInfo": {
            "name": "privacy-search",
            "version": version,
        },
    }


def _get_tools_schema(config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    获取工具 schema 列表

    每个工具定义包含：
    - name: 工具名
    - description: 描述
    - inputSchema: JSON Schema 格式的输入参数

    可通过 config.yaml 的 mcp_server.tools 缩减暴露的工具子集。
    """
    max_results = int((config.get("mcp_server", {}) or {}).get("max_results", 10))
    max_sources = int((config.get("mcp_server", {}) or {}).get("max_sources", 5))

    # 读取允许暴露的工具子集（默认全部）
    mcp_cfg = config.get("mcp_server", {}) or {}
    allowed_tools = mcp_cfg.get("tools", None)  # None 表示全部

    all_tools = [
        {
            "name": "search",
            "description": (
                "多引擎并行搜索。同时检索百度、必应、DuckDuckGo、Yandex 等"
                "十大搜索引擎，SimHash 去重、多因子加权排序。"
                "支持 normal/strict 隐私模式。strict 模式仅使用隐私友好引擎。"
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索查询词",
                    },
                    "engines": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": (
                            "指定引擎列表，如 [\"baidu\",\"bing\"]。"
                            "可选值：baidu, bing, sogou, 360, duckduckgo, "
                            "yandex, startpage, qwant, brave, searxng。"
                            "留空时按隐私模式自动选择。"
                        ),
                    },
                    "num": {
                        "type": "integer",
                        "description": f"每个引擎返回结果数（默认 {max_results}，最大 20）",
                        "default": max_results,
                    },
                    "privacy": {
                        "type": "string",
                        "enum": ["normal", "strict"],
                        "description": "隐私模式：normal（全引擎）或 strict（仅隐私友好引擎）",
                        "default": "normal",
                    },
                    "no_cache": {
                        "type": "boolean",
                        "description": "跳过缓存，强制重新搜索",
                        "default": False,
                    },
                },
                "required": ["query"],
            },
        },
        {
            "name": "synthesize",
            "description": (
                "Perplexity 式答案合成。抓取搜索结果正文，分块编号后"
                "调用 LLM 生成带 citation 的答案。V1.8 新增事实核查层："
                "逐论断回链原文做相似度比对，标注支撑度三级（充分/部分/无源），"
                "无源论断默认剔除。无 API Key 时自动降级为抽取式摘要。"
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "用户问题",
                    },
                    "results": {
                        "type": "array",
                        "description": (
                            "搜索结果数组（可选）。未提供时自动先执行搜索。"
                            "格式：[{\"title\":\"...\",\"url\":\"...\",\"snippet\":\"...\"}, ...]"
                        ),
                    },
                    "max_sources": {
                        "type": "integer",
                        "description": f"最多引用几个来源（默认 {max_sources}，最大 10）",
                        "default": max_sources,
                    },
                },
                "required": ["query"],
            },
        },
        {
            "name": "fetch",
            "description": (
                "抓取网页正文。从指定 URL 提取正文内容，"
                "三层降级：trafilatura → boilerpy3 → 正则 <p> 标签。"
            ),
            "inputSchema": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "目标网页 URL",
                    },
                    "timeout": {
                        "type": "integer",
                        "description": "抓取超时（秒），默认 10",
                        "default": 10,
                    },
                },
                "required": ["url"],
            },
        },
    ]

    # 按 allowed_tools 过滤
    if allowed_tools is not None:
        all_tools = [t for t in all_tools if t["name"] in allowed_tools]

    return all_tools


async def _tool_search(args: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """执行 search 工具"""
    query = args.get("query", "")
    if not query:
        return {"error": "query 参数必填"}

    engines = args.get("engines")
    num = args.get("num")
    privacy = args.get("privacy", "normal")
    no_cache = args.get("no_cache", False)

    try:
        from search import SearchOrchestrator
    except ImportError:
        from .search import SearchOrchestrator

    orchestrator = SearchOrchestrator(config)

    try:
        from ranking import deduplicate, rank_results, weights_from_config
    except ImportError:
        from .ranking import deduplicate, rank_results, weights_from_config

    results = await orchestrator.search(
        query=query,
        engines=engines,
        num=num,
        privacy_mode=privacy,
        use_cache=not no_cache,
    )

    return {
        "results": [r.to_dict() for r in results],
        "notices": orchestrator.notices,
        "from_cache": orchestrator.cache_hit,
        "count": len(results),
    }


async def _tool_synthesize(args: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """执行 synthesize 工具"""
    query = args.get("query", "")
    if not query:
        return {"error": "query 参数必填"}

    results = args.get("results")
    max_sources = args.get("max_sources")

    # 如果没有提供 results，自动搜索
    if not results:
        try:
            from search import SearchOrchestrator
        except ImportError:
            from .search import SearchOrchestrator
        orchestrator = SearchOrchestrator(config)
        search_results = await orchestrator.search(
            query=query,
            privacy_mode="normal",
            use_cache=True,
        )
        results = [r.to_dict() for r in search_results]
        notices = orchestrator.notices
    else:
        notices = []

    # 转为 SearchResult 对象供 synthesiser 使用
    try:
        from search import SearchResult
    except ImportError:
        from .search import SearchResult

    search_result_objects = [SearchResult.from_dict(r) if isinstance(r, dict) else r for r in (results or [])]

    # 覆盖配置中的 max_sources
    synth_cfg = (config.get("synthesis", {}) or {}).copy()
    if max_sources is not None:
        synth_cfg["max_sources"] = max_sources

    merged_config = dict(config)
    merged_config["synthesis"] = synth_cfg

    try:
        from synthesiser import synthesize_pro
    except ImportError:
        from .synthesiser import synthesize_pro

    answer = synthesize_pro(query, search_result_objects, merged_config)

    return {
        "answer": answer,
        "notices": notices,
    }


async def _tool_fetch(args: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """执行 fetch 工具"""
    url = args.get("url", "")
    if not url:
        return {"error": "url 参数必填"}

    timeout = args.get("timeout", 10)

    try:
        from page_fetcher import fetch_and_extract
    except ImportError:
        from .page_fetcher import fetch_and_extract

    # 读取代理配置
    proxy = None
    privacy_cfg = (config.get("privacy", {}) or {})
    strict_cfg = privacy_cfg.get("strict", {}) or {}
    proxy = strict_cfg.get("proxy", None)

    try:
        _html, text = fetch_and_extract(url, timeout=timeout, proxy=proxy)
        if text:
            return {
                "url": url,
                "text": text,
                "success": True,
                "length": len(text),
            }
        else:
            return {
                "url": url,
                "text": "",
                "success": False,
                "error": "无法提取正文",
            }
    except Exception as e:
        return {
            "url": url,
            "text": "",
            "success": False,
            "error": str(e),
        }


# 工具注册表
_TOOL_HANDLERS = {
    "search": _tool_search,
    "synthesize": _tool_synthesize,
    "fetch": _tool_fetch,
}


def _handle_tools_list(params: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """处理 tools/list 请求"""
    return {"tools": _get_tools_schema(config)}


async def _handle_tools_call(params: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    """处理 tools/call 请求"""
    name = params.get("name", "")
    arguments = params.get("arguments", {}) or {}

    # 检查工具是否在允许列表中
    mcp_cfg = config.get("mcp_server", {}) or {}
    allowed_tools = mcp_cfg.get("tools", None)
    if allowed_tools is not None and name not in allowed_tools:
        return _make_error(None, METHOD_NOT_FOUND, f"工具未启用: {name}")

    handler = _TOOL_HANDLERS.get(name)
    if not handler:
        return _make_error(None, METHOD_NOT_FOUND, f"未知工具: {name}")

    # 超时控制（死规则 10）
    mcp_cfg = config.get("mcp_server", {}) or {}
    timeout_seconds = int(mcp_cfg.get("timeout", 30))

    try:
        import asyncio
        result = await asyncio.wait_for(handler(arguments, config), timeout=timeout_seconds)
        return _make_response(None, {"content": [{"type": "text", "text": json.dumps(result, ensure_ascii=False)}]})
    except asyncio.TimeoutError:
        return _make_error(None, INTERNAL_ERROR, f"工具调用超时（>{timeout_seconds}s），请稍后重试或减小查询范围")
    except Exception as e:
        return _make_error(None, INTERNAL_ERROR, f"工具调用失败: {str(e)}", traceback.format_exc())


def _handle_request(request: Dict[str, Any], config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    处理一条 JSON-RPC 请求

    Returns:
        响应字典，或 None（通知消息无需响应）
    """
    method = request.get("method", "")
    params = request.get("params", {}) or {}
    request_id = request.get("id")

    if method == "initialize":
        result = _handle_initialize(params)
        return _make_response(request_id, result)

    elif method == "tools/list":
        result = _handle_tools_list(params, config)
        return _make_response(request_id, result)

    elif method == "tools/call":
        import asyncio
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(_handle_tools_call(params, config))

    elif method == "notifications/initialized":
        # 客户端通知：初始化完成，无需响应
        return None

    else:
        return _make_error(request_id, METHOD_NOT_FOUND, f"未知方法: {method}")


# ============================================================
# 服务主循环
# ============================================================

def _load_config() -> Dict[str, Any]:
    """加载配置文件"""
    try:
        import yaml
    except ImportError:
        return {}

    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)

    candidates = [
        os.path.join(root, "config.yaml"),
        os.path.join(root, "references", "config.yaml.example"),
    ]

    for path in candidates:
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                return yaml.safe_load(f) or {}
        except (FileNotFoundError, IsADirectoryError):
            continue
        except Exception:
            continue
    return {}


def run_server() -> None:
    """
    运行 MCP Server（阻塞式）

    从 stdin 读取 JSON-RPC 请求，向 stdout 写入响应。
    stderr 用于日志输出（不干扰协议通信）。
    """
    config = _load_config()

    mcp_cfg = config.get("mcp_server", {}) or {}
    if not mcp_cfg.get("enabled", True):
        print("MCP Server 已禁用", file=sys.stderr)
        return

    print("privacy-search MCP Server 已启动", file=sys.stderr)

    while True:
        try:
            request = _read_message()
            if request is None:
                break  # EOF，退出

            response = _handle_request(request, config)
            if response is not None:
                _write_message(response)

        except Exception as e:
            # 协议层错误不应导致服务器崩溃
            print(f"处理请求出错: {e}", file=sys.stderr)
            try:
                error_response = _make_error(None, INTERNAL_ERROR, str(e))
                _write_message(error_response)
            except Exception:
                pass


# ============================================================
# CLI 入口
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="MCP Server（V1.7 新增）")
    parser.add_argument("--schema", action="store_true", help="输出工具 schema JSON")
    parser.add_argument("--test", action="store_true", help="运行协议自测")
    args = parser.parse_args()

    config = _load_config()

    if args.schema:
        schema = _get_tools_schema(config)
        print(json.dumps(schema, ensure_ascii=False, indent=2))
        return

    if args.test:
        _run_selftest(config)
        return

    # 默认：启动 MCP Server
    run_server()


def _run_selftest(config: Dict[str, Any]) -> None:
    """协议自测"""
    print("=== MCP Server 协议自测 ===\n", file=sys.stderr)

    # 测试 initialize
    result = _handle_initialize({})
    print(f"✓ initialize: serverInfo={result['serverInfo']['name']} v{result['serverInfo']['version']}", file=sys.stderr)

    # 测试 tools/list
    result = _handle_tools_list({}, config)
    tool_names = [t["name"] for t in result["tools"]]
    print(f"✓ tools/list: {tool_names}", file=sys.stderr)

    # 测试 tools/call (search)
    import asyncio
    async def test_search():
        return await _tool_search({"query": "python", "num": 3}, config)

    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(asyncio.wait_for(test_search(), timeout=30))
    print(f"✓ tools/call(search): count={result.get('count', '?')}", file=sys.stderr)

    # 测试 tools/call (fetch)
    async def test_fetch():
        return await _tool_fetch({"url": "https://example.com"}, config)

    result = loop.run_until_complete(asyncio.wait_for(test_fetch(), timeout=15))
    print(f"✓ tools/call(fetch): success={result.get('success', '?')}", file=sys.stderr)

    loop.close()
    print("\n=== 自测完成 ===", file=sys.stderr)


if __name__ == "__main__":
    main()
