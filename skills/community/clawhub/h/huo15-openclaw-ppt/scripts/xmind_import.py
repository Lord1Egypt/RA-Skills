#!/usr/bin/env python3
"""
xmind_import.py — v4.4 XMind .xmind → JSON deck

XMind 8+ 是 ZIP 含 content.json，老版本是 content.xml。
两种都支持：JSON 优先 → XML fallback。

把思维导图转为 PPT：
- 中心主题 → hero_cover
- 一级分支 → section_divider
- 二级分支 → content_list 的 items

用法：
    python3 scripts/xmind_import.py /tmp/mindmap.xmind --output /tmp/d.json
"""

from __future__ import annotations
import argparse
import json
import os
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def parse_xmind(xmind_path: Path) -> dict:
    """返回结构化 dict {root_topic, branches: [{title, sub: [...]}]}"""
    with zipfile.ZipFile(xmind_path, 'r') as z:
        names = z.namelist()
        # 新版 XMind 8+：content.json
        if 'content.json' in names:
            data = json.loads(z.read('content.json'))
            if isinstance(data, list) and data:
                root_topic = data[0].get('rootTopic', {})
                return _walk_topic_json(root_topic)
        # 老版本：content.xml
        if 'content.xml' in names:
            xml = z.read('content.xml').decode('utf-8')
            return _parse_xmind_xml(xml)
    raise RuntimeError("无法解析 .xmind（既无 content.json 也无 content.xml）")


def _walk_topic_json(topic: dict) -> dict:
    title = topic.get('title', '').strip()
    children = topic.get('children', {}).get('attached', [])
    return {
        'title': title,
        'note': topic.get('notes', {}).get('plain', {}).get('content', ''),
        'children': [_walk_topic_json(c) for c in children],
    }


def _parse_xmind_xml(xml: str) -> dict:
    """老版 XMind XML 解析（lxml 优先 / 退到正则）"""
    try:
        import xml.etree.ElementTree as ET
        root = ET.fromstring(xml)
        ns = {'x': 'urn:xmind:xmap:xmlns:content:2.0'}
        sheet = root.find('.//x:sheet', ns)
        if sheet is None:
            sheet = root[0] if len(root) > 0 else None
        if sheet is None:
            return {'title': 'Untitled', 'children': []}
        topic = sheet.find('x:topic', ns) or sheet.find('topic')
        return _walk_topic_xml(topic)
    except Exception:
        # 极简 fallback：抓 title 元素
        titles = re.findall(r'<title[^>]*>([^<]+)</title>', xml)
        return {
            'title': titles[0] if titles else 'Untitled',
            'children': [{'title': t, 'children': []} for t in titles[1:8]],
        }


def _walk_topic_xml(topic) -> dict:
    if topic is None:
        return {'title': '', 'children': []}
    ns = {'x': 'urn:xmind:xmap:xmlns:content:2.0'}
    title_el = topic.find('x:title', ns) or topic.find('title')
    title = (title_el.text or '').strip() if title_el is not None else ''
    children_container = topic.find('x:children/x:topics', ns) or \
                         topic.find('children/topics')
    children = []
    if children_container is not None:
        for child in children_container.findall('x:topic', ns) or \
                     children_container.findall('topic'):
            children.append(_walk_topic_xml(child))
    return {'title': title, 'children': children}


def tree_to_text(tree: dict, max_chars: int = 20000) -> str:
    """把树结构转 markdown 文本喂给 Claude"""
    lines = []
    def walk(node, level):
        title = node.get('title', '').strip()
        if not title:
            return
        lines.append(('#' * min(level, 6)) + ' ' + title)
        if node.get('note'):
            lines.append(node['note'])
        for child in node.get('children', []):
            walk(child, level + 1)
    walk(tree, 1)
    text = '\n'.join(lines)
    if len(text) > max_chars:
        text = text[:max_chars] + f'\n\n...（已截断，原 {len(text)} 字符）'
    return text


def main():
    parser = argparse.ArgumentParser(description='火一五 PPT v4.4 xmind → deck')
    parser.add_argument('xmind', help='.xmind 路径')
    parser.add_argument('--output', '-o', required=True)
    parser.add_argument('--pack', help='强制 pack')
    parser.add_argument('--slides', type=int)
    parser.add_argument('--build', help='顺便出 PPTX')
    parser.add_argument('--print-extracted', action='store_true')
    args = parser.parse_args()

    print(f"  📄 解析 {args.xmind}...", file=sys.stderr)
    tree = parse_xmind(Path(args.xmind))
    print(f"  🌳 中心主题: {tree.get('title', '?')}", file=sys.stderr)
    print(f"  📂 一级分支: {len(tree.get('children', []))} 个", file=sys.stderr)

    text = tree_to_text(tree)
    if args.print_extracted:
        print(text)
        return

    from prompt_to_deck import call_claude, is_llm_enabled
    enabled, reason = is_llm_enabled()
    if not enabled:
        print(f"  ✗ LLM 未启用：{reason}", file=sys.stderr)
        sys.exit(1)

    full_prompt = (
        f"基于以下思维导图做一份 PPT。中心主题适合做封面，一级分支做章节。\n\n"
        f"=== 思维导图 ===\n\n{text}"
    )
    print(f"  🤖 Claude 转 deck...", file=sys.stderr)
    deck = call_claude(full_prompt, pack_override=args.pack, slides=args.slides)

    print(f"  ✅ {len(deck.get('slides', []))} slides, pack={deck.get('pack')}",
          file=sys.stderr)
    Path(args.output).write_text(json.dumps(deck, ensure_ascii=False, indent=2))

    if args.build:
        import subprocess
        scripts = Path(__file__).parent
        script = (scripts / 'create_pptx_combined.py'
                  if (scripts / 'create_pptx_combined.py').exists()
                  else scripts / 'create-pptx.py')
        subprocess.run([sys.executable, str(script),
                       '--spec', args.output,
                       '--pack', deck.get('pack', 'apple-light'),
                       '--output', args.build], check=True)
        print(f"  🎯 PPTX: {args.build}", file=sys.stderr)


if __name__ == '__main__':
    main()
