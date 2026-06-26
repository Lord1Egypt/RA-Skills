#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""news Hot Hub — 中文热点数据聚合调度器

统一入口，调度 scripts/ 目录下各平台脚本，支持单平台、多平台、全平台获取与对比。

Usage:
    python hub.py fetch <platform> [subcmd] [--limit N] [--query Q]
    python hub.py all [--limit N]
    python hub.py compare [--limit N]
    python hub.py status
"""

import argparse
import concurrent.futures
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

# ──────────────────────────── Platform Registry ────────────────────

SCRIPTS_DIR = Path(__file__).resolve().parent

PLATFORMS = {
    "zhihu": {
        "name": "知乎",
        "script": "zhihu.py",
        "default_cmd": "hot-search",
        "commands": ["hot-search"],
    },
    "toutiao": {
        "name": "今日头条",
        "script": "toutiao.py",
        "default_cmd": "hot-search",
        "commands": ["hot-search"],
    },
    "aibase": {
        "name": "AIBase",
        "script": "aibase.py",
        "default_cmd": "hot-search",
        "commands": ["hot-search", "news", "daily", "all"],
    },
}

ALIASES = {
    "zh": "zhihu", "知乎": "zhihu",
    "tt": "toutiao", "头条": "toutiao", "今日头条": "toutiao",
    "aibase": "aibase", "ai基地": "aibase", "ab": "aibase",
}

ALL_KEYS = list(PLATFORMS.keys())


# ──────────────────────────── Helpers ──────────────────────────────

def _now():
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %z")


def _resolve(name: str) -> str:
    """Resolve platform alias to canonical key."""
    name = name.strip().lower()
    return ALIASES.get(name, name)


def _script_path(platform: str) -> Path:
    meta = PLATFORMS.get(platform)
    if not meta:
        return None
    return SCRIPTS_DIR / meta["script"]


def _run_platform(platform: str, subcmd: str = None, limit: int = 50, query: str = None) -> dict:
    """Execute a platform script and return parsed result."""
    meta = PLATFORMS.get(platform)
    if not meta:
        return {"platform": platform, "success": False, "error": f"未知平台: {platform}"}

    script = _script_path(platform)
    if not script or not script.exists():
        return {"platform": meta["name"], "success": False, "error": "脚本文件不存在"}

    subcmd = subcmd or meta["default_cmd"]
    cmd = [sys.executable, str(script), subcmd]

    # 知乎 topic 命令需要 query 参数
    if subcmd == "topic" and query:
        cmd.append(query)

    # 只有支持 --limit 的子命令才传
    no_limit_cmds = {"all"}
    # 知乎 hot-search 不接受 --limit 参数
    if platform == "zhihu":
        no_limit_cmds.add("hot-search")

    if subcmd not in no_limit_cmds:
        cmd.extend(["--limit", str(limit)])

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=30)

        if result.returncode != 0:
            return {
                "platform": meta["name"],
                "success": False,
                "error": result.stderr.strip() or f"退出码 {result.returncode}",
            }

        output = result.stdout.strip()
        if not output:
            return {"platform": meta["name"], "success": False, "error": "输出为空"}

        data = json.loads(output)

        # 检测 not_implemented 脚手架响应
        if isinstance(data, dict) and data.get("error") == "not_implemented":
            return {
                "platform": meta["name"],
                "success": False,
                "error": data.get("message", "脚本尚未实现"),
            }

        return {"platform": meta["name"], "success": True, "data": data}

    except subprocess.TimeoutExpired:
        return {"platform": meta["name"], "success": False, "error": "请求超时 (30s)"}
    except json.JSONDecodeError as e:
        return {"platform": meta["name"], "success": False, "error": f"JSON 解析错误: {e}"}
    except Exception as e:
        return {"platform": meta["name"], "success": False, "error": str(e)}


def _extract_titles(data) -> list:
    """从平台数据中提取标题列表。"""
    titles = []
    if isinstance(data, dict):
        for key in ("data", "hot_search", "hot_question", "hot_video"):
            val = data.get(key)
            if isinstance(val, dict) and "data" in val:
                val = val["data"]
            if isinstance(val, list):
                for item in val:
                    if isinstance(item, dict):
                        t = item.get("title") or item.get("query", "")
                        if t:
                            titles.append(t)
                if titles:
                    break
    return titles


# ──────────────────────────── Commands ─────────────────────────────

def cmd_fetch(args):
    """获取指定平台热榜。"""
    limit = args.limit or int(os.environ.get("HOT_HUB_LIMIT", "50"))
    raw_platforms = args.platforms.split(",")
    results = []

    for p in raw_platforms:
        key = _resolve(p)
        if key not in PLATFORMS:
            print(json.dumps({"platform": p, "success": False,
                  "error": f"未知平台: {p}"}, ensure_ascii=False))
            continue
        res = _run_platform(key, subcmd=args.subcmd,
                            limit=limit, query=args.query)
        results.append(res)

    for res in results:
        print(json.dumps(res, ensure_ascii=False))


def cmd_all(args):
    """并行获取全部平台。"""
    limit = args.limit or int(os.environ.get("HOT_HUB_LIMIT", "50"))

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        futures = {pool.submit(_run_platform, p, limit=limit)
                               : p for p in ALL_KEYS}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            print(json.dumps(res, ensure_ascii=False))


def cmd_compare(args):
    """跨平台热点词频对比。"""
    limit = args.limit or int(os.environ.get("HOT_HUB_LIMIT", "50"))

    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        futures = {pool.submit(_run_platform, p, limit=limit)
                               : p for p in ALL_KEYS}
        for future in concurrent.futures.as_completed(futures):
            p = futures[future]
            results[p] = future.result()

    per_platform = {}
    keyword_counter = Counter()

    for p, res in results.items():
        name = PLATFORMS[p]["name"]
        if not res["success"]:
            per_platform[name] = {
                "status": "unavailable", "error": res["error"]}
            continue
        titles = _extract_titles(res["data"])
        per_platform[name] = {"status": "ok", "titles": titles}
        for title in titles:
            for seg in re.findall(r"[\u4e00-\u9fff]{2,}", title):
                keyword_counter[seg] += 1
            for word in re.findall(r"[a-zA-Z0-9]{2,}", title):
                keyword_counter[word.lower()] += 1

    # 跨平台关键词统计
    top_keywords = []
    for kw, count in keyword_counter.most_common(30):
        sources = set()
        for name, info in per_platform.items():
            if info["status"] != "ok":
                continue
            if any(kw in t for t in info["titles"]):
                sources.add(name)
        top_keywords.append({
            "keyword": kw,
            "platforms": len(sources),
            "total_mentions": count,
            "platform_names": sorted(sources),
        })

    top_keywords.sort(key=lambda x: (
        x["platforms"], x["total_mentions"]), reverse=True)

    output = {
        "summary": "跨平台热点词频分析",
        "timestamp": _now(),
        "platforms_total": len(ALL_KEYS),
        "platforms_success": sum(1 for v in results.values() if v["success"]),
        "top_keywords": top_keywords[:20],
        "per_platform": per_platform,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


def cmd_status(args):
    """检查各平台脚本可用性。"""
    status = {"timestamp": _now(), "scripts_dir": str(
        SCRIPTS_DIR), "platforms": {}}

    for key, meta in PLATFORMS.items():
        script = _script_path(key)
        status["platforms"][meta["name"]] = {
            "key": key,
            "script": meta["script"],
            "available": script is not None and script.exists(),
            "commands": meta["commands"],
        }

    print(json.dumps(status, ensure_ascii=False, indent=2))


# ──────────────────────────── Main ─────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="news Hot Hub — 中文热点数据聚合器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
示例:
  python hub.py fetch zhihu                     # 知乎热搜
  python hub.py fetch toutiao --limit 20        # 今日头条热榜
  python hub.py fetch aibase                    # AIBase AI新闻
  python hub.py fetch aibase daily              # AIBase AI日报
  python hub.py fetch zhihu,toutiao             # 多平台
  python hub.py all                             # 全部平台
  python hub.py compare                         # 跨平台词频对比
  python hub.py status                          # 脚本可用性

平台缩写: zh=知乎  tt=头条  ab=AIBase
""",
    )
    sub = parser.add_subparsers(dest="command")

    # fetch
    p_fetch = sub.add_parser("fetch", help="获取指定平台热榜")
    p_fetch.add_argument("platforms", help="平台名（逗号分隔多平台，如 zhihu,weibo）")
    p_fetch.add_argument("subcmd", nargs="?", help="子命令（默认 hot-search）")
    p_fetch.add_argument("--query", "-q", help="搜索关键词（知乎 topic 用）")
    p_fetch.add_argument("--limit", type=int, help="结果数量限制")

    # all
    p_all = sub.add_parser("all", help="并行获取全部平台（知乎、今日头条、AIBase）")
    p_all.add_argument("--limit", type=int, help="结果数量限制")

    # compare
    p_cmp = sub.add_parser("compare", help="跨平台热点词频对比分析")
    p_cmp.add_argument("--limit", type=int, help="结果数量限制")

    # status
    sub.add_parser("status", help="检查各平台脚本可用性")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return 1

    handlers = {
        "fetch": cmd_fetch,
        "all": cmd_all,
        "compare": cmd_compare,
        "status": cmd_status,
    }

    try:
        return handlers[args.command](args)
    except KeyboardInterrupt:
        print("\n中断。", file=sys.stderr)
        return 130
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main() or 0)
