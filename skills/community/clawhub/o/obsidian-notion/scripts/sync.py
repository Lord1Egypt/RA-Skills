#!/usr/bin/env python3
"""
Markdown → Notion 同步脚本（通用版）
=====================================

【使用前必读】修改下方 CONFIG 字典中的配置：
  1. NOTION_KEY: API Token
  2. DB_ID: 数据库 ID
  3. OBSIDIAN_ROOT: Obsidian 仓库根目录
  4. TARGET_DIRS: 要同步的子目录列表
  5. EXCLUDE: 排除的文件名列表
  6. PROPERTY_MAP: 数据库属性名映射（根据你的实际属性名修改）
"""

import re, json, os, glob, subprocess
from typing import List, Dict, Any, Optional

# ============ 配置区（修改这里） ============
CONFIG = {
    # 必填：Notion API Token
    "NOTION_KEY": os.environ.get("NOTION_API_KEY", ""),
    
    # 必填：数据库 ID（从数据库 URL 获取）
    "DB_ID": "",
    
    # 必填：Obsidian 仓库根目录
    "OBSIDIAN_ROOT": "",
    
    # 要同步的子目录（相对于 OBSIDIAN_ROOT）
    "TARGET_DIRS": [],
    
    # 排除的文件
    "EXCLUDE": ["README.md", "template.md"],
    
    # 数据库属性名映射（修改为你的实际属性名）
    "PROPERTY_MAP": {
        "title": "名称",         # title 属性名
        "date": "日期",          # date 属性名
        "category": "笔记分类",   # select 属性名
        "tags": "主要标签",      # multi_select 属性名
        "status": "整理状态"     # select 属性名
    },
    
    # 日期默认值（当 frontmatter/文件名都无日期时）
    "DEFAULT_DATE": "2026-01-01",
    
    # 笔记分类默认值
    "DEFAULT_CATEGORY": "未分类",
    
    # 整理状态默认值
    "DEFAULT_STATUS": "已整理",
}
# ===========================================


# ---------- 以下代码通常不需要修改 ----------

NOTION_LANGS = {
    'python','javascript','typescript','bash','cpp','java','c','go','rust',
    'ruby','swift','kotlin','scala','r','matlab','lua','perl','powershell',
    'dockerfile','yaml','json','xml','html','css','sql','markdown','plain text'
}
LANG_MAP = {
    'py':'python','js':'javascript','ts':'typescript','sh':'bash','shell':'bash',
    'yml':'yaml','md':'markdown','c++':'cpp','c#':'csharp','rb':'ruby',
    'rs':'rust','lua':'lua','r':'r','scala':'scala','pl':'perl'
}


def notion_api(url: str, payload: dict) -> dict:
    headers = [
        "-H", f"Authorization: Bearer {CONFIG['NOTION_KEY']}",
        "-H", "Notion-Version: 2026-03-11",
        "-H", "Content-Type: application/json"
    ]
    cmd = ["curl", "-s", "-X", "POST", url, "-d", json.dumps(payload)] + headers
    return json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)


def notion_patch(url: str, payload: dict) -> dict:
    headers = [
        "-H", f"Authorization: Bearer {CONFIG['NOTION_KEY']}",
        "-H", "Notion-Version: 2026-03-11",
        "-H", "Content-Type: application/json"
    ]
    cmd = ["curl", "-s", "-X", "PATCH", url, "-d", json.dumps(payload)] + headers
    return json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout)


# title property name from config
def _title_prop() -> str:
    return CONFIG["PROPERTY_MAP"]["title"]

def _date_prop() -> str:
    return CONFIG["PROPERTY_MAP"]["date"]

def _cat_prop() -> str:
    return CONFIG["PROPERTY_MAP"]["category"]

def _tags_prop() -> str:
    return CONFIG["PROPERTY_MAP"]["tags"]

def _status_prop() -> str:
    return CONFIG["PROPERTY_MAP"]["status"]


def get_existing_pages(db_id: str) -> Dict[str, str]:
    """Query all pages in DB, return {title: page_id} dict"""
    url = f"https://api.notion.com/v1/databases/{db_id}/query"
    payload = {"page_size": 100}
    all_pages = []
    while True:
        resp = notion_api(url, payload)
        all_pages.extend(resp.get('results', []))
        if not resp.get('has_more'):
            break
        payload["start_cursor"] = resp.get('next_cursor')
    cache = {}
    for p in all_pages:
        title_list = p.get('properties', {}).get(_title_prop(), {}).get('title', [])
        for t in title_list:
            txt = t.get('text', {}).get('content', '')
            if txt:
                cache[txt] = p['id']
    return cache


def upsert_page(db_id: str, fname: str, tags: List[str], 
                 date: str, cat: str, blocks: List[dict],
                 existing_cache: Dict[str, str]) -> Optional[str]:
    """Delete existing page with same title, then create new one"""
    if fname in existing_cache:
        old_id = existing_cache[fname]
        notion_patch(f"https://api.notion.com/v1/pages/{old_id}", {"in_trash": True})
        del existing_cache[fname]
    if not blocks:
        return None
    payload = {
        "parent": {"database_id": db_id},
        "properties": {
            _title_prop(): {"title": [{"text": {"content": fname}}]},
            _date_prop(): {"date": {"start": date}},
            _cat_prop(): {"select": {"name": cat}},
            _tags_prop(): {"multi_select": [{"name": t} for t in tags]},
            _status_prop(): {"select": {"name": CONFIG["DEFAULT_STATUS"]}}
        },
        "children": blocks[:100]
    }
    resp = notion_api('https://api.notion.com/v1/pages', payload)
    if resp.get('object') == 'error':
        return f"Error: {resp.get('message', '')[:80]}"
    page_id = resp.get('id')
    if not page_id:
        return 'no_page_id'
    for i in range(100, len(blocks), 100):
        batch = blocks[i:i+100]
        notion_api(f'https://api.notion.com/v1/blocks/{page_id}/children', batch)
    return page_id


def make_rich(text: str, bold: bool = False, italic: bool = False,
               code: bool = False, url: Optional[str] = None) -> dict:
    item = {"type": "text", "text": {"content": text}}
    if url:
        item["text"]["link"] = {"url": url}
    ann = {}
    if bold: ann["bold"] = True
    if italic: ann["italic"] = True
    if code: ann["code"] = True
    if ann: item["annotations"] = ann
    return item


def parse_inline(text: str) -> List[dict]:
    if not text:
        return [make_rich("")]
    result = []
    pattern = re.compile(
        r'\*\*(.+?)\*\*|`([^`]+)`|\[([^\]]+)\]\(([^\)]+)\)|\*([^\*\n]+?)\*|\$([^\$]+?)\$',
        re.DOTALL)
    last = 0
    for m in pattern.finditer(text):
        if m.start() > last:
            result.append(make_rich(text[last:m.start()]))
        if m.group(1) is not None:
            result.append(make_rich(m.group(1), bold=True))
        elif m.group(2) is not None:
            result.append(make_rich(m.group(2), code=True))
        elif m.group(3) is not None:
            url = m.group(4)
            if url and url.startswith(('http://', 'https://', 'file://')):
                result.append(make_rich(m.group(3), url=url))
            else:
                result.append(make_rich(m.group(3)))
        elif m.group(5) is not None:
            result.append(make_rich(m.group(5), italic=True))
        elif m.group(6) is not None:
            result.append(make_rich(m.group(6), code=True))
        last = m.end()
    if last < len(text):
        result.append(make_rich(text[last:]))
    return result if result else [make_rich(text)]


def make_callout(text: str, callout_type: str = "info") -> dict:
    color_map = {
        "info": "blue_background", "tip": "green_background",
        "success": "green_background", "warning": "yellow_background",
        "danger": "red_background", "error": "red_background",
        "caution": "orange_background", "abstract": "purple_background",
        "note": "gray_background"
    }
    icon_map = {
        "info": "ℹ️", "tip": "💡", "success": "✅", "warning": "⚠️",
        "danger": "🚨", "error": "❌", "caution": "🔶", "abstract": "📋", "note": "📝"
    }
    color = color_map.get(callout_type.lower(), "gray_background")
    icon_str = icon_map.get(callout_type.lower(), "💡")
    return {
        "object": "block", "type": "callout", "callout": {
            "rich_text": parse_inline(text),
            "icon": {"emoji": icon_str}, "color": color
        }
    }


def md_to_blocks(content: str) -> List[dict]:
    content = re.sub(r'^---\n.*?\n---\n', '', content, flags=re.DOTALL)
    lines = content.split('\n')
    blocks = []
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        # 独立行公式
        if line.strip().startswith('$$') and line.strip().endswith('$$'):
            expr = line.strip()[2:-2].strip()
            blocks.append({"object": "block", "type": "equation",
                           "equation": {"expression": expr[:1000]}})
            i += 1
            continue
        # 表格
        if re.match(r'^\|.+\|.+\|$', line) and i+1 < len(lines) \
           and re.match(r'^\|[\s\-:|]+\|$', lines[i+1]):
            table_rows_raw = [line]
            i += 2
            while i < len(lines):
                row = lines[i].strip()
                if row.startswith('|') and row.endswith('|'):
                    table_rows_raw.append(lines[i])
                    i += 1
                else:
                    break
            col_count = len([c.strip() for c in table_rows_raw[0].strip('|').split('|')])
            parsed_rows = []
            for row in table_rows_raw:
                cells = [c.strip() for c in row.strip('|').split('|')]
                if len(cells) < col_count:
                    cells += [''] * (col_count - len(cells))
                elif len(cells) > col_count:
                    cells = cells[:col_count]
                parsed_rows.append(cells)
            table_children = []
            for row_cells in parsed_rows:
                cells_rich = [parse_inline(c) for c in row_cells]
                table_children.append({"object": "block", "type": "table_row",
                                       "table_row": {"cells": cells_rich}})
            blocks.append({"object": "block", "type": "table", "table": {
                "table_width": col_count, "has_column_header": True,
                "has_row_header": False, "children": table_children}})
            continue
        if line.startswith('##### '):
            blocks.append({"object": "block", "type": "paragraph",
                           "paragraph": {"rich_text": parse_inline(line[6:])}})
        elif line.startswith('#### '):
            blocks.append({"object": "block", "type": "heading_4",
                           "heading_4": {"rich_text": parse_inline(line[5:])}})
        elif line.startswith('### '):
            blocks.append({"object": "block", "type": "heading_3",
                           "heading_3": {"rich_text": parse_inline(line[4:])}})
        elif line.startswith('## '):
            blocks.append({"object": "block", "type": "heading_2",
                           "heading_2": {"rich_text": parse_inline(line[3:])}})
        elif line.startswith('# '):
            blocks.append({"object": "block", "type": "heading_1",
                           "heading_1": {"rich_text": parse_inline(line[2:])}})
        elif re.match(r'^[-*]\s', line):
            blocks.append({"object": "block", "type": "bulleted_list_item",
                           "bulleted_list_item": {"rich_text": parse_inline(line[2:])}})
        elif re.match(r'^\d+\.\s', line):
            blocks.append({"object": "block", "type": "numbered_list_item",
                           "numbered_list_item": {"rich_text": parse_inline(
                               re.sub(r'^\d+\.\s', '', line))}})
        elif line.strip().startswith('```'):
            lang_raw = line.strip()[3:].strip() or 'plain text'
            lang = LANG_MAP.get(lang_raw.lower(), lang_raw.lower())
            if lang not in NOTION_LANGS:
                lang = 'plain text'
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                code_lines.append(lines[i])
                i += 1
            blocks.append({"object": "block", "type": "code", "code": {
                "rich_text": [{"type": "text", "text": {
                    "content": '\n'.join(code_lines)[:1990]}}],
                "language": lang}})
        elif re.match(r'^> \[!\w+\]', line):
            callout_lines = [line]
            i_back = i
            for j in range(i+1, len(lines)):
                lj = lines[j]
                if lj.startswith('>') or lj.strip() == '':
                    callout_lines.append(lj)
                else:
                    break
            raw = '\n'.join([ln[1:].strip() for ln in callout_lines])
            m = re.match(r'^!(\w+)\s*(.*)', raw, re.DOTALL)
            if m:
                callout_type = m.group(1)
                callout_text = m.group(2).strip()
            else:
                callout_type = "info"
                callout_text = re.sub(r'^\[!\w+\]\s*', '', raw, count=1)
            blocks.append(make_callout(callout_text, callout_type))
            i = i_back + len(callout_lines) - 1
        elif re.match(r'^>\s', line):
            text = re.sub(r'^>\s?', '', line)
            blocks.append({"object": "block", "type": "quote",
                           "quote": {"rich_text": parse_inline(text)}})
        elif line.strip() == '---':
            blocks.append({"object": "block", "type": "divider", "divider": {}})
        elif line.strip():
            blocks.append({"object": "block", "type": "paragraph",
                           "paragraph": {"rich_text": parse_inline(line)}})
        i += 1
    return blocks


def infer_category(path: str) -> str:
    """根据路径推断笔记分类（可重写为自定义逻辑）"""
    p = path.replace(CONFIG['OBSIDIAN_ROOT'], '')
    for d in CONFIG.get('CATEGORY_RULES', []):
        if d['path_keyword'] in p:
            return d['category']
    return CONFIG["DEFAULT_CATEGORY"]


def get_date_from_frontmatter(content: str, path: str) -> str:
    """从 frontmatter 或文件名提取日期"""
    m = re.search(r'^date:\s*(.+)$', content, re.MULTILINE)
    if m:
        d = m.group(1).strip()[:10]
        if re.match(r'^\d{4}-\d{2}-\d{2}$', d):
            return d
    fn = os.path.basename(path)
    m2 = re.match(r'^(\d{4}-\d{2}-\d{2})', fn)
    if m2:
        return m2.group(1)
    return CONFIG["DEFAULT_DATE"]


def get_tags_from_frontmatter(content: str) -> List[str]:
    """从 frontmatter 提取 tags"""
    tags = []
    m = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if m:
        for line in m.group(1).split('\n'):
            if line.startswith('tags:'):
                for t in re.findall(r'[\w/]+', line):
                    if '/' in t:
                        tags.append(t)
    return tags[:10]


def sync_file(path: str, db_id: str, existing_cache: Dict[str, str]) -> Optional[str]:
    with open(path) as f:
        content = f.read()
    fname = os.path.basename(path).replace('.md', '')
    tags = get_tags_from_frontmatter(content)
    date = get_date_from_frontmatter(content, path)
    cat = infer_category(path)
    blocks = md_to_blocks(content)
    return upsert_page(db_id, fname, tags, date, cat, blocks, existing_cache)


def main():
    db_id = CONFIG["DB_ID"]
    if not CONFIG["NOTION_KEY"] or not db_id or not CONFIG["OBSIDIAN_ROOT"]:
        print("❌ 错误：请先配置 CONFIG 中的 NOTION_KEY、DB_ID、OBSIDIAN_ROOT")
        return
    
    # 扫描文件
    files = []
    for d in CONFIG.get("TARGET_DIRS", []):
        pattern = os.path.join(CONFIG["OBSIDIAN_ROOT"], d, '*.md')
        files.extend(glob.glob(pattern))
    files = [f for f in files
             if '/assets/' not in f
             and os.path.basename(f) not in CONFIG["EXCLUDE"]]
    print(f'Found {len(files)} files')
    
    # 构建已有页面缓存
    print('Querying existing pages...')
    existing_cache = get_existing_pages(db_id)
    print(f'Found {len(existing_cache)} existing pages')
    
    success, failed, empty = 0, 0, 0
    errors = []
    for i, path in enumerate(files):
        result = sync_file(path, db_id, existing_cache)
        if result is None:
            empty += 1
        elif str(result).startswith('Error'):
            failed += 1
            errors.append(f'{os.path.basename(path)}: {result}')
        else:
            success += 1
        if (i+1) % 20 == 0:
            print(f'Progress: {i+1}/{len(files)} | Success: {success} | Failed: {failed} | Empty: {empty}')
    
    print(f'\n=== DONE ===')
    print(f'Total: {len(files)}, Success: {success}, Failed: {failed}, Empty: {empty}')
    for e in errors[:10]:
        print(f'  {e}')


if __name__ == '__main__':
    main()
