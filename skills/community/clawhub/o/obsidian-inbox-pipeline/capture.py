#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian Capture — 写入 Obsidian inbox
用法：
  python3 capture.py --type daily-report --title "标题" --source "来源" --tags "[AI,日报]" --category ai --content "正文"

环境变量：
  OBSIDIAN_VAULT_PATH   Obsidian Vault 根目录（必填）
  OBSIDIAN_INBOX_DIR    inbox 子目录（默认: inbox）
"""
import os
import sys
import argparse
from datetime import datetime

# 注入 skill 目录到 path，方便同目录 import
_SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
if _SKILL_DIR not in sys.path:
    sys.path.insert(0, _SKILL_DIR)

try:
    from config import get_vault, slugify
except ImportError:
    # 降级：定义最小版本（允许单独运行）
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
    def slugify(s):
        import re
        s = re.sub(r'[^\w\s-]', '', s)
        return re.sub(r'[-\s]+', '-', s).strip('-')[:40]

DATETIME = datetime.now().strftime("%Y-%m-%d %H:%M")
DATE = datetime.now().strftime("%Y-%m-%d")


def build_capture_md(args) -> str:
    """构建 capture 格式 Markdown"""
    lines = [
        "---",
        f"type: {args.type}",
        f"created: {DATETIME}",
        f"tags: {args.tags or '[]'}",
        f"source: {args.source or ''}",
        "status: inbox",
        "---",
        "",
        f"# {args.title}",
        "",
        "## TL;DR",
        "",
        (args.tldr or "").strip(),
        "",
        "## 内容摘要",
        "",
        args.content.strip()[:3000] if args.content else "",
        "",
        "## 链接索引",
        "",
    ]

    import re
    if args.content:
        urls = re.findall(r'https?://[^\s\)）\]\n]+', args.content)
        for url in urls[:10]:
            fname = url.split('/')[-1][:50] or "链接"
            lines.append(f"- [{fname}]({url})")
        lines.append("")

    lines.extend([
        "## 下一步",
        "- [ ] ",
        "",
        f"<!-- source: {args.source or 'manual'} -->",
        f"<!-- category: {args.category or 'general'} -->",
    ])
    return '\n'.join(lines)


def write_note(path: str, content: str) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    return path


def main():
    parser = argparse.ArgumentParser(description="写入 Obsidian inbox")
    parser.add_argument('--type', default='capture',
                        help='笔记类型: capture/daily-report/knowledge')
    parser.add_argument('--title', required=True, help='笔记标题')
    parser.add_argument('--source', default='', help='来源')
    parser.add_argument('--tags', default='[]', help='标签，如 [AI,日报]')
    parser.add_argument('--content', default='', help='正文内容')
    parser.add_argument('--tldr', default='', help='TL;DR 一句话摘要')
    parser.add_argument('--category', default='general',
                        help='分类: ai/economy/travel/investment/general')
    parser.add_argument('--dry-run', action='store_true', help='仅预览，不写入')
    args = parser.parse_args()

    vault = get_vault()
    inbox_dir = os.environ.get("OBSIDIAN_INBOX_DIR", "inbox").strip().lstrip("/")
    inbox_path = os.path.join(vault, inbox_dir)
    os.makedirs(inbox_path, exist_ok=True)

    content = build_capture_md(args)
    filename = f"{DATE}-{slugify(args.title)}.md"
    filepath = os.path.join(inbox_path, filename)

    if args.dry_run:
        print(f"[DRY RUN] 文件: {filename}")
        print(content)
        return

    write_note(filepath, content)
    print(f"✅ 已写入: {filepath}")
    print(f"📝 类型: {args.type} | 标签: {args.tags} | 来源: {args.source}")


if __name__ == "__main__":
    main()
