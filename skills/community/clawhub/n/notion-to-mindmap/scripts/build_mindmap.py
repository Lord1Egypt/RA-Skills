#!/usr/bin/env python3
"""
build_mindmap.py - Parse Notion HTML export and generate mindmap data JSON.
Usage: python build_mindmap.py <exported_html_file> [notion_base_url]

Examples:
  python build_mindmap.py index.html
  python build_mindmap.py index.html https://www.notion.so/myworkspace/
"""
import re, json, sys
from pathlib import Path
from bs4 import BeautifulSoup

# Default base URL (override via CLI arg 2)
DEFAULT_NOTION_BASE = None  # Auto-detected from HTML


def extract_notion_base_from_html(soup, content):
    """Try to extract workspace name and notion base URL from HTML content."""
    # Try to find a notion.so link in the HTML
    links = soup.find_all('a', href=True)
    for link in links:
        href = link.get('href', '')
        if 'notion.so/' in href:
            # Extract base URL like https://www.notion.so/workspace/
            match = re.match(r'(https://[^/]+/[^/]+/)', href)
            if match:
                return match.group(1)
            # Try without www
            match = re.match(r'(https://[^/]+/)', href)
            if match:
                return match.group(1)
    return None


def extract_workspace_name_from_html(soup, content):
    """Extract workspace name from HTML content."""
    # Pattern: 工作空间名称: <name>
    match = re.search(r'工作空间名称[:：]\s*(.+?)(?:</p>|<li>|$)', content)
    if match:
        return match.group(1).strip()
    # Fallback: use first <title> content
    title = soup.find('title')
    if title:
        t = title.get_text().strip()
        # Remove "Export-" prefix
        t = re.sub(r'^Export[-_]?\s*', '', t, flags=re.IGNORECASE)
        return t or "Notion"
    return "Notion"


def extract_id_from_ul(ul):
    """Extract page ID from ul id attribute like 'id::xxxx-xxxx-...'"""
    uid = ul.get('id', '')
    uid = uid.replace('id::', '')
    return uid.replace('-', '')


def is_csv_entry(ul):
    """Check if this ul represents a CSV database entry (skip it)."""
    uid = ul.get('id', '')
    return uid.endswith('.csv')


def clean_title(text):
    """Clean title: remove file suffixes and trailing 32-char hex ID."""
    if not text:
        return None
    text = text.strip()
    text = re.sub(r'\.(html|csv)$', '', text)
    text = re.sub(r'\s*\(Inline database\)$', '', text, flags=re.IGNORECASE)
    text = re.sub(r'\s+[a-f0-9]{32}$', '', text, flags=re.IGNORECASE)
    return text.strip() or None


def parse_ul(ul_elem, notion_base, depth=0):
    """Parse a <ul> element representing a Notion page."""
    if is_csv_entry(ul_elem):
        return None

    page_id = extract_id_from_ul(ul_elem)
    link = notion_base + page_id if (notion_base and page_id) else None

    # Get title from direct <a> child
    title = None
    direct_a = ul_elem.find('a', recursive=False)
    if direct_a:
        title = clean_title(direct_a.get_text().strip())

    if not title:
        title = "Untitled"

    children = []
    for li in ul_elem.find_all('li', recursive=False):
        child_ul = li.find('ul', recursive=False)
        if child_ul:
            child = parse_ul(child_ul, notion_base, depth + 1)
            if child:
                children.append(child)

    node = {"t": title, "id": page_id, "l": link}
    if children:
        node["c"] = children
    return node


def parse_index(html_path, notion_base):
    """Parse the Notion export index.html."""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    soup = BeautifulSoup(content, 'html.parser')
    root_ul = soup.find('ul')
    if not root_ul:
        return {"t": "Notion", "c": []}

    workspace_name = extract_workspace_name_from_html(soup, content)

    children = []
    for li in root_ul.find_all('li', recursive=False):
        child_ul = li.find('ul', recursive=False)
        if child_ul:
            node = parse_ul(child_ul, notion_base, depth=1)
            if node:
                children.append(node)

    return {"t": workspace_name, "id": None, "l": None, "c": children}


def count_nodes(node):
    c = 1
    for ch in node.get("c", []):
        c += count_nodes(ch)
    return c


def max_depth(node, d=0):
    if not node.get("c"):
        return d
    return max(max_depth(ch, d+1) for ch in node["c"])


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python build_mindmap.py <notion_export_html> [notion_base_url]")
        print("  notion_base_url is optional. If not provided, auto-detected from HTML.")
        sys.exit(1)

    src = sys.argv[1]
    notion_base = sys.argv[2] if len(sys.argv) > 2 else None

    # Auto-detect notion_base if not provided
    if not notion_base:
        with open(src, 'r', encoding='utf-8') as f:
            content = f.read()
        soup = BeautifulSoup(content, 'html.parser')
        detected = extract_notion_base_from_html(soup, content)
        if detected:
            notion_base = detected
            print(f"Detected workspace: {notion_base}", flush=True)
        else:
            notion_base = DEFAULT_NOTION_BASE
            print("Could not detect workspace URL. Notion links will not be generated.", flush=True)

    data = parse_index(src, notion_base)

    out = "mindmap_data.json"
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',', ':'))

    print(f"Nodes: {count_nodes(data)}, Max depth: {max_depth(data)}", flush=True)
    print(f"Saved: {out}", flush=True)
