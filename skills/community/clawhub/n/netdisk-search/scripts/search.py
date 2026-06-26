#!/usr/bin/env python3
"""
网盘资源搜索脚本
通过网盘搜索 API 搜索网盘资源，支持多种输出格式和过滤条件。

用法:
    python search.py 速度与激情
    python search.py 速度与激情 --types baidu,quark --format json
    python search.py 教程 --exclude 广告,推广 --limit 10
"""

import argparse
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime

# ---------------------------------------------------------------------------
# 常量 / 网盘中文映射
# ---------------------------------------------------------------------------
CLOUD_TYPE_NAMES = {
    "baidu": "百度网盘",
    "quark": "夸克网盘",
    "alipan": "阿里网盘",
    "aliyun": "阿里云盘",
    "xunlei": "迅雷网盘",
    "115": "115网盘",
    "uc": "UC网盘",
    "tianyi": "天翼网盘",
    "weiyun": "微云",
    "magnet": "磁力链接",
    "ed2k": "电驴链接",
    "mega": "Mega网盘",
    "pikpak": "PikPak",
    "123": "123网盘",
    "lanzou": "蓝奏云",
    "ctfile": "城通网盘",
    "yunpan": "云盘",
    "others": "其他",
}

API_CANDIDATES = [
    "http://localhost:8888",
    "https://netdisk-search.example.com",
]

# ---------------------------------------------------------------------------
# API 探测
# ---------------------------------------------------------------------------

def detect_api(explicit=None):
    """按优先级探测可用的 搜索 API 地址。"""
    candidates = []

    # 1. 命令行显式指定
    if explicit:
        candidates.append(explicit)

    # 2. 环境变量
    env = os.environ.get("NETDISK_API_URL")
    if env:
        candidates.append(env)

    # 3. 默认候选
    candidates.extend(API_CANDIDATES)

    for url in candidates:
        url = url.rstrip("/")
        try:
            req = urllib.request.Request(url, method="GET")
            req.add_header("User-Agent", "NetDisk-Search/1.0")
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status < 500:
                    return url
        except Exception:
            continue

    # 如果全部探测失败，返回第一个候选
    return candidates[0].rstrip("/") if candidates else "http://localhost:8888"


# ---------------------------------------------------------------------------
# API 调用
# ---------------------------------------------------------------------------

def search(api_url, kw, src="all", cloud_types=None, include=None,
           exclude=None, plugins=None, refresh=False, limit=20):
    """调用搜索 API 并返回结果字典。"""

    body = {
        "kw": kw,
        "res": "all",
        "src": src,
    }

    if cloud_types:
        body["cloud_types"] = cloud_types

    filt = {}
    if include:
        filt["include"] = include
    if exclude:
        filt["exclude"] = exclude
    if filt:
        body["filter"] = filt

    if plugins:
        body["plugins"] = plugins

    if refresh:
        body["refresh"] = True

    data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    url = f"{api_url}/api/search"

    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json; charset=utf-8")
    req.add_header("User-Agent", "NetDisk-Search/1.0")

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            result = json.loads(raw)
            # 兼容 {"code":0, "data":{...}} 包装格式
            if "code" in result and "data" in result:
                result = result["data"]
    except urllib.error.HTTPError as e:
        body_text = ""
        try:
            body_text = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        print(f"[错误] API 返回 HTTP {e.code}: {body_text}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"[错误] 无法连接 API ({api_url}): {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"[错误] 请求失败: {e}", file=sys.stderr)
        sys.exit(1)

    # 截断到 limit
    if limit and "merged_by_type" in result:
        truncated = {}
        count = 0
        for ctype, items in result["merged_by_type"].items():
            remaining = limit - count
            if remaining <= 0:
                break
            take = items[:remaining]
            if take:
                truncated[ctype] = take
            count += len(take)
        result["merged_by_type"] = truncated
        result["total"] = count

    return result


# ---------------------------------------------------------------------------
# 输出格式化
# ---------------------------------------------------------------------------

def type_label(code):
    """返回网盘类型的中文名称。"""
    return CLOUD_TYPE_NAMES.get(code, code)


def fmt_datetime(dt_str):
    """尝试解析并格式化日期字符串。"""
    if not dt_str:
        return ""
    for fmt, slen in [("%Y-%m-%dT%H:%M:%S", 19), ("%Y-%m-%d %H:%M:%S", 19), ("%Y-%m-%d", 10)]:
        try:
            return datetime.strptime(dt_str[:slen], fmt).strftime("%Y-%m-%d")
        except (ValueError, IndexError):
            pass
    # 取前10个字符作为日期
    return dt_str[:10]


def format_terminal(result, kw):
    """终端友好的彩色（emoji）输出。"""
    lines = []
    total = result.get("total", 0)
    lines.append(f"🔍 搜索: {kw}")
    lines.append(f"📊 找到 {total} 个资源")
    lines.append("")

    merged = result.get("merged_by_type", {})
    if not merged:
        lines.append("  (无结果)")
        return "\n".join(lines)

    for ctype, items in merged.items():
        label = type_label(ctype)
        lines.append(f"📁 {label} ({len(items)})")
        for i, item in enumerate(items, 1):
            note = item.get("note", "无标题") or "无标题"
            url = item.get("url", "")
            pwd = item.get("password", "")
            src = item.get("source", "")
            dt = fmt_datetime(item.get("datetime", ""))

            pwd_part = f" | 提取码: {pwd}" if pwd else ""
            lines.append(f"  {i}. {note}{pwd_part}")
            lines.append(f"     {url}")
            src_parts = [s for s in [src, dt] if s]
            if src_parts:
                lines.append(f"     来源: {' | '.join(src_parts)}")
        lines.append("")

    return "\n".join(lines).rstrip()


def format_json(result):
    """JSON 原始输出。"""
    return json.dumps(result, ensure_ascii=False, indent=2)


def format_markdown(result, kw):
    """Markdown 表格输出，按网盘类型分组。"""
    lines = []
    total = result.get("total", 0)
    lines.append(f"## 🔍 搜索: {kw}")
    lines.append(f"**📊 找到 {total} 个资源**")
    lines.append("")

    merged = result.get("merged_by_type", {})
    if not merged:
        lines.append("*无结果*")
        return "\n".join(lines)

    for ctype, items in merged.items():
        label = type_label(ctype)
        lines.append(f"### 📁 {label} ({len(items)})")
        lines.append("")
        lines.append("| # | 标题 | 提取码 | 链接 | 来源 | 日期 |")
        lines.append("|---|------|--------|------|------|------|")
        for i, item in enumerate(items, 1):
            note = (item.get("note", "无标题") or "无标题").replace("|", "\\|")
            pwd = (item.get("password", "") or "-").replace("|", "\\|")
            url = item.get("url", "")
            if url:
                url_md = f"[链接]({url})"
            else:
                url_md = "-"
            src = (item.get("source", "") or "-").replace("|", "\\|")
            dt = fmt_datetime(item.get("datetime", "")) or "-"
            lines.append(f"| {i} | {note} | {pwd} | {url_md} | {src} | {dt} |")
        lines.append("")

    return "\n".join(lines).rstrip()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser():
    parser = argparse.ArgumentParser(
        description="网盘资源搜索",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n"
               "  python search.py 速度与激情\n"
               "  python search.py 教程 --types baidu,quark --format json\n"
               "  python search.py 资源 --exclude 广告 --limit 10",
    )
    parser.add_argument("kw", help="搜索关键词")
    parser.add_argument("--types", default=None,
                        help="网盘类型过滤，逗号分隔（如 baidu,quark）")
    parser.add_argument("--include", default=None,
                        help="结果必须包含的关键词（逗号分隔）")
    parser.add_argument("--exclude", default=None,
                        help="结果排除的关键词（逗号分隔）")
    parser.add_argument("--src", default="all", choices=["all", "tg", "plugin"],
                        help="数据来源: all/tg/plugin（默认 all）")
    parser.add_argument("--plugins", default=None,
                        help="指定插件列表（逗号分隔）")
    parser.add_argument("--refresh", action="store_true",
                        help="强制刷新缓存")
    parser.add_argument("--format", dest="output_format", default="terminal",
                        choices=["terminal", "json", "markdown"],
                        help="输出格式: terminal/json/markdown（默认 terminal）")
    parser.add_argument("--api", default=None,
                        help="API 地址（覆盖自动探测）")
    parser.add_argument("--limit", type=int, default=20,
                        help="最大结果数（默认 20）")
    return parser


def split_csv(val):
    """将逗号分隔的字符串拆为列表，去除空白项。"""
    if not val:
        return None
    return [v.strip() for v in val.split(",") if v.strip()]


def main():
    parser = build_parser()
    args = parser.parse_args()

    # 探测 API
    api_url = detect_api(args.api)

    # 解析列表参数
    cloud_types = split_csv(args.types)
    include = split_csv(args.include)
    exclude = split_csv(args.exclude)
    plugins = split_csv(args.plugins)

    # 调用搜索
    result = search(
        api_url=api_url,
        kw=args.kw,
        src=args.src,
        cloud_types=cloud_types,
        include=include,
        exclude=exclude,
        plugins=plugins,
        refresh=args.refresh,
        limit=args.limit,
    )

    # 格式化输出
    if args.output_format == "json":
        print(format_json(result))
    elif args.output_format == "markdown":
        print(format_markdown(result, args.kw))
    else:
        print(format_terminal(result, args.kw))


if __name__ == "__main__":
    main()
