#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian Review — 读取 inbox 内容，生成整理报告
用法：
  python3 review.py
  python3 review.py --dry-run

环境变量：
  OBSIDIAN_VAULT_PATH   Obsidian Vault 根目录（必填）
  OBSIDIAN_INBOX_DIR    inbox 子目录（默认: inbox）
"""
import os
import sys
import glob
from datetime import datetime

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

DATETIME = datetime.now().strftime("%Y-%m-%d %H:%M")
DATE = datetime.now().strftime("%Y-%m-%d")


def parse_frontmatter(text: str) -> tuple:
    """返回 (frontmatter_dict, body)"""
    if not text.startswith('---'):
        return {}, text
    end = text.find('\n---\n', 4)
    if end == -1:
        return {}, text
    fm_text = text[4:end]
    body = text[end+5:]
    fm = {}
    for line in fm_text.split('\n'):
        if ':' in line:
            key, val = line.split(':', 1)
            fm[key.strip()] = val.strip()
    return fm, body


def extract_title(body: str) -> str:
    for line in body.split('\n'):
        line = line.strip()
        if line.startswith('# ') and len(line) > 2:
            return line[2:].strip()
    return "无标题"


def read_inbox_items(vault: str, inbox_dir: str) -> list:
    inbox_path = os.path.join(vault, inbox_dir)
    pattern = os.path.join(inbox_path, "*.md")
    files = glob.glob(pattern)
    items = []
    for path in sorted(files, key=os.path.getmtime, reverse=True):
        try:
            with open(path, encoding='utf-8') as f:
                content = f.read()
            fm, body = parse_frontmatter(content)
            items.append({
                'path': os.path.basename(path),
                'title': extract_title(body),
                'type': fm.get('type', 'unknown'),
                'source': fm.get('source', 'unknown'),
                'tags': fm.get('tags', ''),
                'status': fm.get('status', ''),
                'size': len(content),
                'mtime': os.path.getmtime(path),
                'excerpt': body[:200].strip(),
            })
        except Exception as e:
            print(f"Error reading {path}: {e}", file=sys.stderr)
    return items


def build_review_report(items: list, vault: str) -> str:
    lines = [
        f"## 🗂️ Inbox Review — {DATE}",
        "",
        f"**Inbox 共 {len(items)} 条待整理内容**",
        "",
        "---",
        "",
    ]

    by_type = {}
    for item in items:
        t = item['type'] or 'unknown'
        by_type.setdefault(t, []).append(item)

    for note_type, notes in by_type.items():
        lines.append(f"### 📁 {note_type}（{len(notes)} 条）")
        for item in notes:
            path = item['path'].replace('.md', '')
            title = item['title']
            source = item['source']
            tags = item['tags']
            excerpt = item['excerpt'].replace('\n', ' ')[:100].strip()
            lines.append(
                f"**[[inbox/{path}|{title}]]**\n"
                f"- 来源：{source or '未知'} | 标签：{tags or '无'} | "
                f"大小：{item['size']} bytes\n"
                f"- 摘要：{excerpt}..."
            )
        lines.append("")

    lines.extend([
        "## ✍️ 整理建议",
        "",
        f"**{DATETIME}** 当前 inbox 共 **{len(items)}** 条内容待处理：",
        "",
    ])

    capture_items = by_type.get('capture', [])
    daily_items = [i for i in items
                   if '日报' in i['title'] or 'radar' in i['title'].lower()]

    if capture_items:
        lines.append(f"- **{len(capture_items)} 条 capture** 内容，建议阅读 TL;DR 后选择性归档")
    if daily_items:
        lines.append(f"- **{len(daily_items)} 条日报**，可选择性存入归档目录")

    lines.extend([
        "",
        "## 📋 下一步行动",
        "",
        "- [ ] 阅读每条 inbox 的 TL;DR",
        "- [ ] 将需要保留的内容打上 `type: knowledge` 标签",
        "- [ ] 将已整理内容移出 inbox（删除或归档）",
        "",
        f"*Vault：{vault}*",
    ])
    return '\n'.join(lines)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Inbox 整理")
    parser.add_argument('--dry-run', action='store_true', help='预览报告，不输出文件')
    args = parser.parse_args()

    vault = get_vault()
    inbox_dir = os.environ.get("OBSIDIAN_INBOX_DIR", "inbox").strip().lstrip("/")
    items = read_inbox_items(vault, inbox_dir)

    if not items:
        print("📭 Inbox 为空，无需整理。")
        return

    report = build_review_report(items, vault)
    print(report)

    if not args.dry_run:
        review_dir = os.path.join(vault, "notes", "_review")
        os.makedirs(review_dir, exist_ok=True)
        out_path = os.path.join(review_dir, f"inbox-review-{DATE}.md")
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"\n✅ Review 已写入：{out_path}")


if __name__ == "__main__":
    main()
