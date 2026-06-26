#!/usr/bin/env python3
"""
多搜索聚合器 - Multi-Search Aggregator
同时调用多个搜索引擎，返回统一格式的结果
"""
import argparse
import json
import os
import pathlib
import re
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional

TAVILY_URL = "https://api.tavily.com/search"
BRAVE_URL = "https://api.search.brave.com/res/v1/web_search"


def load_env_key(key_name: str) -> Optional[str]:
    """从环境变量或 ~/.openclaw/.env 加载 API Key"""
    key = os.environ.get(key_name)
    if key:
        return key.strip()

    env_path = pathlib.Path.home() / ".openclaw" / ".env"
    if env_path.exists():
        try:
            txt = env_path.read_text(encoding="utf-8", errors="ignore")
            m = re.search(rf"^\s*{key_name}\s*=\s*(.+?)\s*$", txt, re.M)
            if m:
                v = m.group(1).strip().strip('"').strip("'")
                if v:
                    return v
        except Exception:
            pass
    return None


def search_tavily(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Tavily 搜索"""
    key = load_env_key("TAVILY_API_KEY")
    if not key:
        return {"source": "tavily", "error": "Missing TAVILY_API_KEY", "results": []}

    try:
        payload = {
            "api_key": key,
            "query": query,
            "max_results": max_results,
            "search_depth": "basic",
            "include_answer": True,
            "include_images": False,
            "include_raw_content": False,
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            TAVILY_URL,
            data=data,
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")

        obj = json.loads(body)
        results = []
        for r in (obj.get("results") or [])[:max_results]:
            results.append({
                "title": r.get("title"),
                "url": r.get("url"),
                "snippet": r.get("content"),
            })

        return {
            "source": "tavily",
            "answer": obj.get("answer"),
            "results": results,
        }
    except Exception as e:
        return {"source": "tavily", "error": str(e), "results": []}


def search_brave(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Brave Search"""
    key = load_env_key("BRAVE_API_KEY")
    if not key:
        return {"source": "brave", "error": "未配置 BRAVE_API_KEY（可选）", "results": []}

    try:
        url = f"{BRAVE_URL}?q={urllib.parse.quote(query)}&count={max_results}"
        req = urllib.request.Request(
            url,
            headers={
                "Accept": "application/json",
                "X-Subscription-Token": key,
            },
            method="GET",
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")

        obj = json.loads(body)
        results = []
        for r in (obj.get("web", {}).get("results", []))[:max_results]:
            results.append({
                "title": r.get("title"),
                "url": r.get("url"),
                "snippet": r.get("description"),
            })

        return {"source": "brave", "results": results}
    except urllib.error.HTTPError as e:
        return {"source": "brave", "error": f"Brave API 错误 ({e.code})，请检查 API Key", "results": []}
    except Exception as e:
        return {"source": "brave", "error": f"请求失败: {str(e)[:50]}", "results": []}


def search_perplexity(query: str, max_results: int = 5) -> Dict[str, Any]:
    """Perplexity 搜索 (如果配置了 API)"""
    key = load_env_key("PERPLEXITY_API_KEY")
    if not key:
        return {"source": "perplexity", "error": "Missing PERPLEXITY_API_KEY", "results": []}

    try:
        url = "https://api.perplexity.ai/chat/completions"
        payload = {
            "model": "llama-3.1-sonar-small-128k-online",
            "messages": [
                {"role": "system", "content": "You are a helpful search assistant."},
                {"role": "user", "content": f"Search for: {query}"}
            ],
            "max_tokens": 1000,
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}",
            },
            method="POST",
        )

        with urllib.request.urlopen(req, timeout=30) as resp:
            body = resp.read().decode("utf-8", errors="replace")

        obj = json.loads(body)
        content = obj.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # 简单解析，Perplexity 返回的是文本内容
        return {
            "source": "perplexity",
            "answer": content[:500],
            "results": [{"title": "Perplexity Result", "url": "", "snippet": content[:200]}]
        }
    except Exception as e:
        return {"source": "perplexity", "error": str(e), "results": []}


def aggregate_search(query: str, sources: List[str], max_results: int = 5) -> Dict[str, Any]:
    """聚合多个搜索引擎结果"""
    available_sources = {
        "tavily": search_tavily,
        "brave": search_brave,
        "perplexity": search_perplexity,
    }

    results = {
        "query": query,
        "sources_used": [],
        "results": {},
    }

    # 并行搜索所有启用的源
    with ThreadPoolExecutor(max_workers=len(sources)) as executor:
        futures = {}
        for source in sources:
            if source in available_sources:
                future = executor.submit(available_sources[source], query, max_results)
                futures[future] = source

        for future in as_completed(futures):
            source = futures[future]
            try:
                result = future.result()
                results["results"][source] = result
                if "error" not in result:
                    results["sources_used"].append(source)
            except Exception as e:
                results["results"][source] = {"source": source, "error": str(e)}

    return results


def to_markdown(results: Dict[str, Any]) -> str:
    """转换为 Markdown 格式"""
    lines = [f"# 🔍 搜索结果: {results['query']}", ""]
    lines.append(f"**调用源**: {', '.join(results['sources_used']) or '无'}")
    lines.append("")

    for source, data in results.get("results", {}).items():
        lines.append(f"## 📡 {source.upper()}")
        
        if "error" in data:
            lines.append(f"❌ 错误: {data['error']}")
            lines.append("")
            continue

        if data.get("answer"):
            lines.append(f"**摘要**: {data['answer']}")
            lines.append("")

        for i, r in enumerate(data.get("results", []), 1):
            title = r.get("title", "无标题")
            url = r.get("url", "")
            snippet = r.get("snippet", "")
            
            lines.append(f"{i}. **{title}**")
            if url:
                lines.append(f"   🔗 {url}")
            if snippet:
                lines.append(f"   📝 {snippet[:150]}...")
            lines.append("")

    return "\n".join(lines)


def to_unified_json(results: Dict[str, Any], max_per_source: int = 3) -> Dict[str, Any]:
    """转换为统一 JSON 格式"""
    unified = {
        "query": results["query"],
        "sources": results["sources_used"],
        "answer": None,
        "results": []
    }

    # 收集所有答案（优先用 tavily 的）
    for source in ["tavily", "brave", "perplexity"]:
        data = results.get("results", {}).get(source, {})
        if data.get("answer") and not unified["answer"]:
            unified["answer"] = data["answer"]

    # 收集所有结果
    for source, data in results.get("results", {}).items():
        if "error" in data:
            continue
        for r in data.get("results", [])[:max_per_source]:
            unified["results"].append({
                "source": source,
                **r
            })

    return unified


def main():
    ap = argparse.ArgumentParser(description="多搜索聚合器")
    ap.add_argument("--query", "-q", required=True, help="搜索关键词")
    ap.add_argument("--sources", "-s", default="tavily,brave", help="搜索源，用逗号分隔: tavily,brave,perplexity")
    ap.add_argument("--max-results", "-n", type=int, default=5, help="每个源的最大结果数")
    ap.add_argument("--format", "-f", default="md", choices=["md", "json", "unified"], help="输出格式")
    
    args = ap.parse_args()

    sources = [s.strip() for s in args.sources.split(",") if s.strip()]
    if not sources:
        sources = ["tavily"]

    results = aggregate_search(args.query, sources, args.max_results)

    if args.format == "md":
        sys.stdout.write(to_markdown(results))
    elif args.format == "unified":
        json.dump(to_unified_json(results, args.max_results), sys.stdout, ensure_ascii=False, indent=2)
    else:
        json.dump(results, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
