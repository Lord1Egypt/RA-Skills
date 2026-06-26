#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian Query — 搜索 Obsidian 知识库
用法：
  python3 query.py --query "AI Agent" --type knowledge --limit 5
  python3 query.py --query "OpenClaw" --tags "AI-Agent,安全"

环境变量：
  OBSIDIAN_VAULT_PATH   Obsidian Vault 根目录（必填）
"""
import os
import sys
import re
import json
import argparse
import subprocess
from datetime import datetime
from typing import List, Dict

_SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
if _SKILL_DIR not in sys.path:
    sys.path.insert(0, _SKILL_DIR)

try:
    from config import get_vault
except ImportError:
    def get_vault():
        path = os.environ.get("OBSIDIAN_VAULT_PATH", "").strip()
        if path:
            return path
        import subprocess
        try:
            r = subprocess.run(["obsidian-cli", "print-default", "--path-only"],
                              capture_output=True, text=True, timeout=5)
            if r.returncode == 0:
                return r.stdout.strip()
        except Exception:
            pass
        raise RuntimeError("OBSIDIAN_VAULT_PATH 未设置")


INDEX_FILENAME = ".ai"  # folder containing index.json


def load_index(vault: str) -> Dict:
    """加载 .ai/index.json"""
    index_dir = os.path.join(vault, INDEX_FILENAME)
    index_path = os.path.join(index_dir, "index.json")
    if os.path.exists(index_path):
        with open(index_path) as f:
            return json.load(f)
    return {"items": []}


def search_index(query: str, index: Dict,
                 type_filter: str = None,
                 tags: List[str] = None,
                 limit: int = 10) -> List[Dict]:
    """在 index.json 中搜索"""
    query_lower = query.lower()
    results = []
    seen = set()

    for item in index.get("items", []):
        path = item.get("path", "")
        title = item.get("title", "").lower()
        excerpt = item.get("excerpt", "").lower()
        item_type = item.get("type", "")
        item_tags = item.get("tags", [])

        if "/_review/" in path or path.startswith("_"):
            continue
        if query_lower not in title and query_lower not in excerpt:
            continue
        if type_filter and item_type != type_filter:
            continue
        if tags and not any(t in item_tags for t in tags):
            continue
        if path in seen:
            continue
        seen.add(path)

        results.append(item)
        if len(results) >= limit:
            break
    return results


def search_content(query: str, vault: str, limit: int = 10) -> List[Dict]:
    """用 obsidian-cli 搜索正文内容"""
    try:
        result = subprocess.run(
            ["obsidian-cli", "search-content", query, "--path", vault],
            capture_output=True, text=True, timeout=15
        )
        lines = result.stdout.split('\n')
        results = []
        current = {}
        for line in lines:
            line = line.strip()
            if '::' in line and not line.startswith('#'):
                key, val = line.split('::', 1)
                current[key.strip()] = val.strip()
            elif line.startswith('==='):
                if current:
                    results.append(current)
                    current = {}
        return results[:limit]
    except Exception as e:
        print(f"obsidian-cli search-content error: {e}", file=sys.stderr)
        return []


def build_report(query: str, index_results: List[Dict],
                 content_results: List[Dict], vault: str) -> str:
    """构建输出报告"""
    lines = [
        f"## 📚 Obsidian 知识库搜索：「{query}」",
        "",
        f"找到 **{len(index_results)}** 条索引笔记 + **{len(content_results)}** 条内容匹配",
        "",
    ]

    if index_results:
        lines.append("### 📋 结构化笔记")
        for i, item in enumerate(index_results, 1):
            path = item.get('path', '')
            title = item.get('title', '无标题')
            item_type = item.get('type', '—')
            item_tags = ', '.join(item.get('tags', []) or [])
            excerpt = item.get('excerpt', '')[:150]
            updated = item.get('updated', 0)
            date = datetime.fromtimestamp(updated).strftime('%Y-%m-%d') if updated else '未知'
            lines.extend([
                f"**{i}. {title}**",
                f"- 类型：`{item_type}` | 标签：{item_tags or '无'} | 更新：{date}",
                f"- 路径：`{path}`",
                f"- 摘要：{excerpt}...",
                "",
            ])

    if content_results:
        lines.append("### 📄 内容全文匹配")
        for i, result in enumerate(content_results[:5], 1):
            match = result.get('match', '')
            path = result.get('path', result.get('file', ''))
            if len(match) > 300:
                match = match[:300] + '...'
            lines.extend([
                f"**{i}. {path}**",
                f"```\n{match}\n```",
                "",
            ])

    if not index_results and not content_results:
        lines.append("⚠️ 未找到相关内容。")

    lines.extend([
        "",
        "---",
        f"*知识库索引更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        f"*Vault：{vault}*",
    ])
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description="搜索 Obsidian 知识库")
    parser.add_argument('--query', '-q', required=True, help='搜索关键词')
    parser.add_argument('--type', '-t', default=None,
                        help='按 type 过滤: knowledge/capture/daily-report')
    parser.add_argument('--tags', default=None, help='按标签过滤，逗号分隔')
    parser.add_argument('--limit', '-l', type=int, default=10, help='最大结果数')
    parser.add_argument('--include-content', action='store_true',
                       help='读取笔记正文作为上下文（更多 tokens）')
    parser.add_argument('--dry-run', action='store_true', help='仅预览')
    args = parser.parse_args()

    vault = get_vault()
    index = load_index(vault)
    tags = [t.strip() for t in args.tags.split(',')] if args.tags else None

    index_results = search_index(args.query, index,
                                  type_filter=args.type, tags=tags,
                                  limit=args.limit)
    content_results = []
    if args.include_content:
        content_results = search_content(args.query, vault, limit=args.limit)

    report = build_report(args.query, index_results, content_results, vault)
    print(report)


if __name__ == "__main__":
    main()
