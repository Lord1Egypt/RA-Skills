"""
mindmap_tree.py — 思维导图统一数据模型 + 多格式解析 / 导出

数据模型：
    Node(title, note, children)  — 树形节点

输入（parse_*）：
    - parse_markdown(text)  : Markdown outline（#/##/### 或 '  - ' 列表）
    - parse_json(text)      : 内部 JSON 规约
    - parse_opml(text)      : OPML 2.0
    - parse_xmind(path)     : XMind 2021+ ZIP（content.json）

输出（to_*）：
    - to_markdown(root)
    - to_json(root)
    - to_opml(root, title=None)
    - to_xmind(root, output_path, sheet_name='思维导图')
    - to_freemind(root)
"""

from __future__ import annotations

import json
import os
import re
import time
import uuid
import zipfile
from dataclasses import dataclass, field
from typing import List, Optional, Sequence
from xml.etree import ElementTree as ET


# ============================================================
# 一、数据模型
# ============================================================

@dataclass
class Node:
    title: str
    note: str = ''
    children: List['Node'] = field(default_factory=list)

    def add(self, title, note=''):
        child = Node(title=title, note=note)
        self.children.append(child)
        return child

    def depth(self):
        if not self.children:
            return 1
        return 1 + max(c.depth() for c in self.children)

    def walk(self, depth=0):
        yield self, depth
        for child in self.children:
            yield from child.walk(depth + 1)

    def count_leaves(self):
        if not self.children:
            return 1
        return sum(c.count_leaves() for c in self.children)

    def to_dict(self):
        d = {'title': self.title}
        if self.note:
            d['note'] = self.note
        if self.children:
            d['children'] = [c.to_dict() for c in self.children]
        return d


def _from_dict(data):
    if isinstance(data, str):
        return Node(title=data)
    title = data.get('title') or data.get('topic') or data.get('text') or ''
    note = data.get('note', '')
    children_data = (data.get('children') or data.get('topics')
                     or data.get('nodes') or [])
    children = [_from_dict(c) for c in children_data]
    return Node(title=title, note=note, children=children)


# ============================================================
# 二、Markdown outline 解析
# ============================================================

_MD_HEADING_RE = re.compile(r'^(#{1,6})\s+(.+?)\s*#*\s*$')
_MD_LIST_RE = re.compile(r'^(\s*)[-*+]\s+(.+)$')
_MD_ORDERED_RE = re.compile(r'^(\s*)\d+[\.．)]\s+(.+)$')


def parse_markdown(text):
    r"""把 Markdown 大纲转成 Node 树。

    支持三种分层方式（按行决定层级）：

    1. Markdown 标题  # / ## / ###
    2. 无序列表缩进   - item   （每 2 个空格算一级）
    3. 有序列表       1. item

    规则：
    - 第一行标题（最浅的标题 / 最浅的列表）成为根节点 title；
      若不存在标题级行，以 "思维导图" 为默认根。
    - 同层节点平铺；深层缩进（或 `##`→`###`）成为下层。
    - 连续的同一层非空行合并为节点注释（note）。
    """
    lines = text.split('\n')
    root = Node(title='思维导图')
    stack: List[tuple[int, Node]] = [(-1, root)]  # (depth, node)
    root_set = False

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            continue

        heading = _MD_HEADING_RE.match(line)
        if heading:
            depth = len(heading.group(1))  # 1..6
            title = heading.group(2).strip()
            node = Node(title=title)
            while stack and stack[-1][0] >= depth:
                stack.pop()
            parent = stack[-1][1] if stack else root
            if not root_set and parent is root:
                # 首个标题升格为根
                root.title = title
                root_set = True
                stack = [(depth, root)]
                continue
            parent.children.append(node)
            stack.append((depth, node))
            continue

        list_m = _MD_LIST_RE.match(line) or _MD_ORDERED_RE.match(line)
        if list_m:
            indent = len(list_m.group(1))
            depth = 100 + indent // 2  # 超过 heading 层级
            title = list_m.group(2).strip()
            node = Node(title=title)
            while stack and stack[-1][0] >= depth:
                stack.pop()
            parent = stack[-1][1] if stack else root
            if not root_set and parent is root:
                root.title = title
                root_set = True
                stack = [(depth, root)]
                continue
            parent.children.append(node)
            stack.append((depth, node))
            continue

        # 纯文本行，挂到当前节点的 note 上
        if stack:
            current = stack[-1][1]
            current.note = (current.note + ('\n' if current.note else '')
                            + line.strip())

    return root


def to_markdown(root: Node, max_heading=3):
    """把 Node 树还原成 Markdown outline（前 N 层用标题，其余用列表）。"""
    lines = []

    def _walk(node, depth):
        text = node.title
        if depth == 0:
            lines.append(f'# {text}')
        elif depth < max_heading:
            lines.append('#' * (depth + 1) + ' ' + text)
        else:
            lines.append('  ' * (depth - max_heading) + '- ' + text)
        if node.note:
            lines.append('')
            for ln in node.note.split('\n'):
                lines.append(ln)
        for child in node.children:
            _walk(child, depth + 1)

    _walk(root, 0)
    return '\n'.join(lines) + '\n'


# ============================================================
# 三、JSON 规约
# ============================================================

def parse_json(text):
    data = json.loads(text)
    # 允许顶层包一层 {"title":..., "root":{...}} 或裸节点
    if isinstance(data, dict) and 'root' in data:
        return _from_dict(data['root'])
    return _from_dict(data)


def to_json(root, indent=2):
    return json.dumps(root.to_dict(), ensure_ascii=False, indent=indent)


# ============================================================
# 四、OPML 2.0 解析 / 导出
# ============================================================

def parse_opml(text):
    root_node = Node(title='思维导图')
    try:
        tree = ET.fromstring(text)
    except ET.ParseError:
        return root_node
    head = tree.find('head')
    if head is not None:
        title_el = head.find('title')
        if title_el is not None and (title_el.text or '').strip():
            root_node.title = title_el.text.strip()
    body = tree.find('body')
    if body is None:
        return root_node

    def _walk(el, parent):
        for child_el in el.findall('outline'):
            title = child_el.attrib.get('text') or child_el.attrib.get('title') or ''
            note = child_el.attrib.get('_note', '')
            child = Node(title=title, note=note)
            parent.children.append(child)
            _walk(child_el, child)

    _walk(body, root_node)
    return root_node


def to_opml(root: Node, title=None):
    opml = ET.Element('opml', {'version': '2.0'})
    head = ET.SubElement(opml, 'head')
    ET.SubElement(head, 'title').text = title or root.title
    ET.SubElement(head, 'dateCreated').text = time.strftime(
        '%a, %d %b %Y %H:%M:%S +0000', time.gmtime())
    body = ET.SubElement(opml, 'body')

    def _append(parent_el, node):
        attrs = {'text': node.title}
        if node.note:
            attrs['_note'] = node.note
        outline = ET.SubElement(parent_el, 'outline', attrs)
        for child in node.children:
            _append(outline, child)

    # root 作为第一个 outline，保留根节点信息
    _append(body, root)
    ET.indent(opml, space='  ')
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(
        opml, encoding='unicode')


# ============================================================
# 五、XMind 2021+ 解析 / 导出
# ============================================================

def _node_to_xmind_topic(node: Node):
    topic = {
        'id': uuid.uuid4().hex,
        'title': node.title,
    }
    if node.note:
        topic['notes'] = {'plain': {'content': node.note}}
    if node.children:
        topic['children'] = {
            'attached': [_node_to_xmind_topic(c) for c in node.children]
        }
    return topic


def _xmind_topic_to_node(topic):
    title = topic.get('title', '')
    note = ''
    notes = topic.get('notes') or {}
    plain = notes.get('plain') or {}
    if isinstance(plain, dict):
        note = plain.get('content') or ''
    node = Node(title=title, note=note)
    children = topic.get('children') or {}
    attached = children.get('attached') if isinstance(children, dict) else []
    for c in attached or []:
        node.children.append(_xmind_topic_to_node(c))
    return node


def to_xmind(root: Node, output_path, sheet_name='思维导图'):
    """写 XMind 2021+ 压缩包（content.json）。"""
    root_topic = _node_to_xmind_topic(root)
    content = [{
        'id': uuid.uuid4().hex,
        'class': 'sheet',
        'title': sheet_name,
        'rootTopic': root_topic,
    }]
    metadata = {
        'creator': {
            'name': 'huo15-mind-map',
            'version': '1.0.0',
        },
        'dataStructureVersion': '2',
    }
    manifest = {
        'file-entries': {
            'content.json': {},
            'metadata.json': {},
        },
    }

    os.makedirs(os.path.dirname(os.path.abspath(output_path)) or '.',
                exist_ok=True)
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr('content.json', json.dumps(content, ensure_ascii=False))
        zf.writestr('metadata.json', json.dumps(metadata, ensure_ascii=False))
        zf.writestr('manifest.json', json.dumps(manifest, ensure_ascii=False))
    return output_path


def parse_xmind(path):
    """读 XMind 2021+ 文件。旧版 (content.xml) 暂不支持。"""
    with zipfile.ZipFile(path, 'r') as zf:
        names = zf.namelist()
        if 'content.json' in names:
            data = json.loads(zf.read('content.json').decode('utf-8'))
            sheets = data if isinstance(data, list) else [data]
            if not sheets:
                return Node(title='思维导图')
            root_topic = sheets[0].get('rootTopic') or {}
            return _xmind_topic_to_node(root_topic)
    return Node(title='思维导图')


# ============================================================
# 六、FreeMind .mm 导出
# ============================================================

def to_freemind(root: Node):
    """FreeMind .mm 格式（很多国产思维导图也支持导入）。"""
    doc = ET.Element('map', {'version': '1.0.1'})

    def _append(parent_el, node):
        el = ET.SubElement(parent_el, 'node', {'TEXT': node.title})
        if node.note:
            richcontent = ET.SubElement(el, 'richcontent',
                                        {'TYPE': 'NOTE'})
            body = ET.SubElement(richcontent, 'html')
            body = ET.SubElement(body, 'body')
            p = ET.SubElement(body, 'p')
            p.text = node.note
        for child in node.children:
            _append(el, child)

    _append(doc, root)
    ET.indent(doc, space='  ')
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(
        doc, encoding='unicode')


# ============================================================
# 七、格式派发
# ============================================================

def parse_auto(path_or_text, hint=None):
    """根据 hint (扩展名或 'markdown'/'json'/'opml'/'xmind') 解析。"""
    if hint is None and os.path.exists(path_or_text):
        hint = os.path.splitext(path_or_text)[1].lstrip('.').lower()
        with open(path_or_text, 'rb') as fh:
            raw = fh.read()
        if hint == 'xmind':
            return parse_xmind(path_or_text)
        text = raw.decode('utf-8', errors='replace')
    else:
        text = path_or_text
        hint = (hint or '').lower()

    if hint in ('md', 'markdown', 'txt', ''):
        if text.lstrip().startswith('{'):
            return parse_json(text)
        if text.lstrip().startswith('<opml'):
            return parse_opml(text)
        return parse_markdown(text)
    if hint in ('json',):
        return parse_json(text)
    if hint in ('opml', 'xml'):
        return parse_opml(text)
    return parse_markdown(text)
