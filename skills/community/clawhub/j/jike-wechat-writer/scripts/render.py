#!/usr/bin/env python3
"""
MD → HTML 渲染脚本 — 将 Markdown 文章渲染为带内联样式的 HTML，用于微信公众号排版。

Usage:
  python3 render.py render article.md --theme blue-minimal -o article.html
  python3 render.py list-themes
  python3 render.py extract-style "https://mp.weixin.qq.com/s/xxx" --name "主题名" --id theme-id

零外部依赖，纯 stdlib 实现。复刻后端 Go renderNode 的 fragment 模板逻辑。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.request
from html.parser import HTMLParser

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)
STYLES_DIR = os.path.join(SKILL_DIR, "styles")

# ---------------------------------------------------------------------------
# Placeholder image
# ---------------------------------------------------------------------------

PLACEHOLDER_URL = "https://qiniu-cloud.dso100.com/f/u/CEirD/upload/oN04jwC.png"

# ---------------------------------------------------------------------------
# Theme loading
# ---------------------------------------------------------------------------


def list_themes() -> list[dict]:
    """Scan styles/ for valid theme JSON files."""
    themes = []
    if not os.path.isdir(STYLES_DIR):
        return themes
    for fname in sorted(os.listdir(STYLES_DIR)):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(STYLES_DIR, fname)
        theme_id = fname[:-5]  # strip .json
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                meta = json.load(f)
            themes.append({"id": theme_id, "name": meta.get("name", theme_id), "description": meta.get("description", "")})
        except (json.JSONDecodeError, OSError):
            pass
    return themes


def load_theme(theme_id: str) -> dict:
    """Load and return a theme JSON."""
    fpath = os.path.join(STYLES_DIR, f"{theme_id}.json")
    if not os.path.isfile(fpath):
        print(f"Error: theme '{theme_id}' not found at {fpath}", file=sys.stderr)
        sys.exit(1)
    with open(fpath, "r", encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Inline formatting
# ---------------------------------------------------------------------------

def _escape_html(text: str) -> str:
    """Escape HTML entities — must run before inline formatting."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _apply_inline(text: str) -> str:
    """Apply inline Markdown formatting to a single text string."""
    text = _escape_html(text)
    # images: ![alt](url)
    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1" style="max-width:100%;" />', text)
    # links: [text](url) → keep text only (replicate Go logic)
    text = re.sub(r"\[([^\]]*)\]\([^)]+\)", r"\1", text)
    # inline code
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    # bold
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    # italic
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


# ---------------------------------------------------------------------------
# Block-level Markdown parser
# ---------------------------------------------------------------------------

def _parse_blocks(md_text: str) -> list[dict]:
    """Parse Markdown text into a list of block dicts.

    Each block: {"type": str, "text": str, "items": list[str] | None}
    """
    lines = md_text.split("\n")
    blocks: list[dict] = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # skip blank lines
        if not stripped:
            i += 1
            continue

        # image placeholder: <!-- IMG: ... -->
        m_img = re.match(r"^<!--\s*IMG:\s*(.+?)\s*-->$", stripped)
        if m_img:
            blocks.append({"type": "image_placeholder", "text": m_img.group(1).strip()})
            i += 1
            continue

        # blockquote: > text (merge consecutive)
        if stripped.startswith("> "):
            buf = []
            while i < n and lines[i].strip().startswith("> "):
                buf.append(lines[i].strip()[2:])
                i += 1
            blocks.append({"type": "blockquote", "text": "\n".join(buf)})
            continue

        # h2: ## text
        if stripped.startswith("## ") and not stripped.startswith("### "):
            blocks.append({"type": "h2", "text": stripped[3:].strip()})
            i += 1
            continue

        # h3: ### text
        if stripped.startswith("### "):
            blocks.append({"type": "h3", "text": stripped[4:].strip()})
            i += 1
            continue

        # unordered list: - or *
        if re.match(r"^[-*]\s+", stripped):
            items = []
            while i < n and re.match(r"^[-*]\s+", lines[i].strip()):
                items.append(re.sub(r"^[-*]\s+", "", lines[i].strip()))
                i += 1
            blocks.append({"type": "ul", "items": items})
            continue

        # ordered list: 1. 2. etc
        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < n and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip()))
                i += 1
            blocks.append({"type": "ol", "items": items})
            continue

        # paragraph: merge consecutive non-blank, non-special lines
        buf = []
        while i < n and lines[i].strip():
            s = lines[i].strip()
            if (s.startswith("> ") or s.startswith("## ") or s.startswith("### ")
                    or re.match(r"^[-*]\s+", s) or re.match(r"^\d+\.\s+", s)
                    or re.match(r"^<!--\s*IMG:", s)):
                break
            buf.append(s)
            i += 1
        if buf:
            blocks.append({"type": "paragraph", "text": " ".join(buf)})

    return blocks


# ---------------------------------------------------------------------------
# Fragment-based rendering (replicates Go renderNode logic)
# ---------------------------------------------------------------------------

def _render_blocks(blocks: list[dict], fragments: dict) -> str:
    """Render parsed blocks into HTML using fragment templates."""
    parts: list[str] = []
    section_num = 0
    first_blockquote = True

    for block in blocks:
        btype = block["type"]

        if btype == "blockquote":
            if first_blockquote:
                tpl = fragments.get("hero", fragments.get("blockquote", "<blockquote>{TEXT}</blockquote>"))
                first_blockquote = False
            else:
                tpl = fragments.get("blockquote", "<blockquote>{TEXT}</blockquote>")
            text = _apply_inline(block["text"]).replace("\n", "<br/>")
            parts.append(tpl.replace("{TEXT}", text))

        elif btype == "h2":
            section_num += 1
            tpl = fragments.get("section_title", "<h2>{NUM} {TEXT}</h2>")
            text = _apply_inline(block["text"])
            parts.append(tpl.replace("{NUM}", f"{section_num:02d}").replace("{TEXT}", text))

        elif btype == "h3":
            tpl = fragments.get("highlight", "<h3>{TEXT}</h3>")
            parts.append(tpl.replace("{TEXT}", _apply_inline(block["text"])))

        elif btype == "paragraph":
            tpl = fragments.get("paragraph", "<p>{TEXT}</p>")
            parts.append(tpl.replace("{TEXT}", _apply_inline(block["text"])))

        elif btype in ("ul", "ol"):
            item_tpl = fragments.get("list_item", "<li>{TEXT}</li>")
            items_html = "\n".join(item_tpl.replace("{TEXT}", _apply_inline(it)) for it in block["items"])
            if btype == "ol":
                list_tpl = fragments.get("list_ordered", "<ol>{ITEMS}</ol>")
            else:
                list_tpl = fragments.get("list_unordered", "<ul>{ITEMS}</ul>")
            parts.append(list_tpl.replace("{ITEMS}", items_html))

        elif btype == "image_placeholder":
            alt = _escape_html(block["text"])
            img_tpl = fragments.get("image_placeholder",
                '<section style="margin:0 0 16px 0;text-align:center;">'
                '<img src="{SRC}" alt="{ALT}" style="max-width:100%;" />'
                '<p style="font-size:13px;color:#999;margin:8px 0 0 0;">{ALT}</p>'
                '</section>')
            parts.append(img_tpl.replace("{SRC}", PLACEHOLDER_URL).replace("{ALT}", alt))

    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Full document assembly
# ---------------------------------------------------------------------------

def render_md_to_html(md_text: str, theme: dict) -> str:
    """Render Markdown text to a full HTML document using the given theme."""
    frags = theme.get("fragments", {})
    blocks = _parse_blocks(md_text)
    body_inner = _render_blocks(blocks, frags)

    body_wrapper = frags.get("body_wrapper", "<div>")
    body_wrapper_end = frags.get("body_wrapper_end", "</div>")
    header_image = frags.get("header_image", "")
    top_decoration = frags.get("top_decoration", "")

    body_parts = [body_wrapper, header_image, top_decoration, body_inner, body_wrapper_end]
    body_html = "\n".join(p for p in body_parts if p)

    return (
        "<!DOCTYPE html>\n<html>\n<head>\n"
        '<meta charset="UTF-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
        f"<title>{theme.get('name', 'Article')}</title>\n"
        "</head>\n<body>\n"
        f"{body_html}\n"
        "</body>\n</html>\n"
    )


# ---------------------------------------------------------------------------
# Simple DOM tree for HTML parsing (extract-style)
# ---------------------------------------------------------------------------

class _Node:
    """Lightweight DOM node."""
    __slots__ = ("tag", "attrs", "children", "text", "parent")

    def __init__(self, tag: str = "", attrs: dict | None = None):
        self.tag = tag
        self.attrs: dict = attrs or {}
        self.children: list[_Node] = []
        self.text: str = ""
        self.parent: _Node | None = None

    def get_style(self) -> str:
        return self.attrs.get("style", "")

    def get_class(self) -> str:
        return self.attrs.get("class", "")

    def outer_html(self) -> str:
        """Reconstruct the outer HTML of this node."""
        if not self.tag:
            return self.text
        attr_str = ""
        for k, v in self.attrs.items():
            attr_str += f' {k}="{v}"'
        if self.tag in ("img", "br", "hr"):
            return f"<{self.tag}{attr_str} />"
        inner = self._inner_html()
        return f"<{self.tag}{attr_str}>{inner}</{self.tag}>"

    def _inner_html(self) -> str:
        parts = []
        if self.text:
            parts.append(self.text)
        for c in self.children:
            parts.append(c.outer_html())
        return "".join(parts)

    def find_all(self, tag: str) -> list[_Node]:
        """BFS find all descendants with given tag."""
        result = []
        queue = list(self.children)
        while queue:
            node = queue.pop(0)
            if node.tag == tag:
                result.append(node)
            queue.extend(node.children)
        return result

    def get_text(self) -> str:
        """Get all text content recursively."""
        parts = []
        if self.text:
            parts.append(self.text)
        for c in self.children:
            parts.append(c.get_text())
        return "".join(parts)


class _DOMBuilder(HTMLParser):
    """Build a simple DOM tree from HTML."""

    SELF_CLOSING = {"img", "br", "hr", "input", "meta", "link", "area", "base", "col", "embed", "source", "track", "wbr"}

    def __init__(self):
        super().__init__()
        self.root = _Node(tag="root")
        self._stack: list[_Node] = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]):
        attr_dict = {k: (v or "") for k, v in attrs}
        node = _Node(tag=tag, attrs=attr_dict)
        node.parent = self._stack[-1]
        self._stack[-1].children.append(node)
        if tag not in self.SELF_CLOSING:
            self._stack.append(node)

    def handle_endtag(self, tag: str):
        # Pop back to matching open tag
        for i in range(len(self._stack) - 1, 0, -1):
            if self._stack[i].tag == tag:
                self._stack[i:] = []
                break

    def handle_data(self, data: str):
        if data.strip():
            text_node = _Node()
            text_node.text = data
            text_node.parent = self._stack[-1]
            self._stack[-1].children.append(text_node)


# ---------------------------------------------------------------------------
# Style extraction helpers
# ---------------------------------------------------------------------------

def _fetch_html(url: str) -> str:
    """Fetch HTML from a URL."""
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    })
    with urllib.request.urlopen(req, timeout=30) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset)


def _parse_dom(html: str) -> _Node:
    """Parse HTML string into a DOM tree."""
    builder = _DOMBuilder()
    builder.feed(html)
    return builder.root


def _find_content_root(root: _Node) -> _Node:
    """Find the main content area (rich_media_content for WeChat articles)."""
    for node in root.find_all("div"):
        cls = node.get_class()
        if "rich_media_content" in cls:
            return node
    # Fallback: look for <article> or largest <div>
    articles = root.find_all("article")
    if articles:
        return articles[0]
    # Last resort: use body or root
    bodies = root.find_all("body")
    return bodies[0] if bodies else root


def _parse_css_value(style: str, prop: str) -> str:
    """Extract a CSS property value from an inline style string."""
    m = re.search(rf"{re.escape(prop)}\s*:\s*([^;]+)", style)
    return m.group(1).strip() if m else ""


def _parse_font_size(style: str) -> float:
    """Extract font-size in px from inline style. Returns 0 if not found."""
    val = _parse_css_value(style, "font-size")
    m = re.match(r"([\d.]+)\s*px", val)
    return float(m.group(1)) if m else 0


def _is_bold(style: str) -> bool:
    """Check if style indicates bold text."""
    fw = _parse_css_value(style, "font-weight")
    return fw in ("bold", "700", "800", "900") or "font-weight:bold" in style.replace(" ", "")


def _has_background(style: str) -> bool:
    """Check if element has a visible background."""
    bg = _parse_css_value(style, "background") or _parse_css_value(style, "background-color")
    return bool(bg) and bg not in ("transparent", "none", "#fff", "#ffffff", "white", "inherit")


def _has_border_left(style: str) -> bool:
    return bool(_parse_css_value(style, "border-left"))


def _clean_style(style: str) -> str:
    """Remove WeChat lazy-load CSS properties that break rendering."""
    # Remove visibility:hidden, opacity:0, etc.
    style = re.sub(r'visibility\s*:\s*[^;]+;?\s*', '', style)
    style = re.sub(r'opacity\s*:\s*0[^;]*;?\s*', '', style)
    return style.strip().rstrip(';').strip()


def _templatize(node: _Node, frag_type: str) -> str:
    """Convert a node's HTML into a fragment template with placeholders."""
    html = node.outer_html()
    text = node.get_text().strip()

    # Clean WeChat lazy-load styles from all fragments
    html = re.sub(r'style="([^"]*)"', lambda m: f'style="{_clean_style(m.group(1))}"', html)

    if frag_type == "image":
        # WeChat uses data-src for lazy loading, normalize to src
        html = re.sub(r'data-src="[^"]*"', 'src="{SRC}"', html)
        html = re.sub(r'src="[^"]*"', 'src="{SRC}"', html)
        html = re.sub(r"src='[^']*'", "src='{SRC}'", html)
        html = re.sub(r'alt="[^"]*"', 'alt="{ALT}"', html)
        return html
    if frag_type == "section_title":
        title_text = re.sub(r'^\d{1,2}[.、]?\s*', '', text).strip()
        html = re.sub(r'>\s*\d{1,2}[.、]?\s*', '>{NUM} ', html, count=1)
        if title_text and title_text in html:
            html = html.replace(title_text, "{TEXT}", 1)
        elif text and text in html:
            html = html.replace(text, "{NUM} {TEXT}", 1)
        return html

    # For text-bearing fragments: if get_text() result isn't found as a
    # contiguous string in the HTML (common with WeChat's <span leaf=""> wrapping),
    # strip all inner content and rebuild with just the outer tag + {TEXT}.
    if text and frag_type not in ("list_ordered", "list_unordered"):
        if text in html:
            html = html.replace(text, "{TEXT}", 1)
        else:
            # Rebuild: keep outermost tag with its style, replace inner with {TEXT}
            m = re.match(r'^(<[^>]+>)(.*)(</[^>]+>)$', html, re.DOTALL)
            if m:
                html = f"{m.group(1)}{{TEXT}}{m.group(3)}"

    if frag_type in ("list_ordered", "list_unordered"):
        html = re.sub(r'(<[ou]l[^>]*>).*?(</[ou]l>)', r'\1{ITEMS}\2', html, flags=re.DOTALL)
    if frag_type == "list_item" and text:
        if text not in html:
            m = re.match(r'^(<[^>]+>)(.*)(</[^>]+>)$', html, re.DOTALL)
            if m:
                html = f"{m.group(1)}{{TEXT}}{m.group(3)}"
        else:
            html = html.replace(text, "{TEXT}", 1)
    return html


def _classify_node(node: _Node, seen_blockquote: list[bool]) -> tuple[str, _Node] | None:
    """Classify a DOM node into a fragment type. Returns (type, node) or None."""
    tag = node.tag
    style = node.get_style()
    text = node.get_text().strip()

    # Images
    if tag == "img":
        return ("image", node)
    # Check for img inside a wrapper
    imgs = node.find_all("img")
    if imgs and not text:
        return ("image", node)

    # Headings
    if tag == "h2":
        return ("section_title", node)
    if tag == "h3":
        return ("highlight", node)

    # Styled section_title: large bold text
    if tag in ("section", "p", "div") and text:
        fs = _parse_font_size(style)
        child_styles = "".join(c.get_style() for c in node.children if c.tag)
        if fs >= 17 and (_is_bold(style) or _is_bold(child_styles)):
            return ("section_title", node)
        if 15 <= fs < 17 and (_is_bold(style) or _is_bold(child_styles)):
            return ("highlight", node)

    # Blockquote
    if tag == "blockquote":
        if not seen_blockquote[0]:
            seen_blockquote[0] = True
            return ("hero", node)
        return ("blockquote", node)
    # Styled blockquote: background + border-left
    if tag in ("section", "div") and _has_background(style) and _has_border_left(style):
        if not seen_blockquote[0]:
            seen_blockquote[0] = True
            return ("hero", node)
        return ("blockquote", node)

    # Lists
    if tag == "ol":
        return ("list_ordered", node)
    if tag == "ul":
        return ("list_unordered", node)
    if tag == "li":
        return ("list_item", node)

    # Paragraph
    if tag == "p" and text:
        return ("paragraph", node)

    return None


def _extract_fragments_from_dom(root: _Node) -> dict[str, str]:
    """Walk the content root and extract fragment templates."""
    content = _find_content_root(root)
    extracted: dict[str, str] = {}
    seen_bq: list[bool] = [False]

    def walk(node: _Node):
        result = _classify_node(node, seen_bq)
        if result:
            ftype, matched = result
            if ftype not in extracted:
                extracted[ftype] = _templatize(matched, ftype)
            # Extract list_item from list containers
            if ftype in ("list_ordered", "list_unordered") and "list_item" not in extracted:
                lis = matched.find_all("li")
                if lis:
                    extracted["list_item"] = _templatize(lis[0], "list_item")
            return  # Don't recurse into matched nodes
        for child in node.children:
            if child.tag:
                walk(child)

    walk(content)

    # Extract body_wrapper from content root
    style = content.get_style()
    if style:
        cleaned_attrs = dict(content.attrs)
        if "style" in cleaned_attrs:
            cleaned_attrs["style"] = _clean_style(cleaned_attrs["style"])
        # Remove WeChat-specific classes
        if "class" in cleaned_attrs:
            del cleaned_attrs["class"]
        if "id" in cleaned_attrs:
            del cleaned_attrs["id"]
        attr_str = ""
        for k, v in cleaned_attrs.items():
            attr_str += f' {k}="{v}"'
        extracted["body_wrapper"] = f"<div{attr_str}>"
        extracted["body_wrapper_end"] = "</div>"

    return extracted


def _build_theme_json(extracted: dict[str, str], name: str, theme_id: str, description: str) -> dict:
    """Build a theme JSON from extracted fragments only (no fallbacks)."""
    # Detect accent color from extracted fragments
    accent = "#2563eb"
    for v in extracted.values():
        m = re.search(r'#[0-9a-fA-F]{6}', v)
        if m:
            accent = m.group(0)
            break

    return {
        "name": name,
        "description": description,
        "accent_color": accent,
        "fragments": dict(extracted),
    }


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------

def cmd_list_themes(_args):
    """List available themes."""
    themes = list_themes()
    if not themes:
        print("No themes found. Add theme directories under styles/.")
        return
    for t in themes:
        print(f"  {t['id']:20s}  {t['name']}  — {t['description']}")


def cmd_extract_style(args):
    """Extract style fragments from a WeChat article URL."""
    url = args.url
    name = args.name
    theme_id = args.id
    description = args.description or "从公众号文章拆解的自定义主题"

    if not url.startswith("http://") and not url.startswith("https://"):
        print("Error: 请提供公众号文章 URL（以 http:// 或 https:// 开头）", file=sys.stderr)
        sys.exit(1)

    # Fetch HTML
    print(f"正在获取文章: {url}")
    try:
        html = _fetch_html(url)
    except Exception as e:
        print(f"Error: 无法获取文章 — {e}", file=sys.stderr)
        sys.exit(1)

    # Parse and extract
    print("正在解析 DOM 并提取样式...")
    dom = _parse_dom(html)
    extracted = _extract_fragments_from_dom(dom)

    if not extracted:
        print("Error: 未能从文章中提取到任何样式片段，请确认链接是否为有效的公众号文章", file=sys.stderr)
        sys.exit(1)

    # Build theme JSON
    theme_data = _build_theme_json(extracted, name, theme_id, description)

    # Save
    out_path = os.path.join(STYLES_DIR, f"{theme_id}.json")
    os.makedirs(STYLES_DIR, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(theme_data, f, ensure_ascii=False, indent=2)

    # Report
    keys = list(extracted.keys())
    print(f"\nOK: {out_path}")
    print(f"  提取到: {', '.join(keys)}")
    print(f"  建议: 用浏览器打开一篇测试文章的渲染结果，确认效果后再微调 {theme_id}.json")


def cmd_render(args):
    """Render a Markdown file to HTML."""
    md_path = args.input
    if not os.path.isfile(md_path):
        print(f"Error: file not found: {md_path}", file=sys.stderr)
        sys.exit(1)

    with open(md_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    theme = load_theme(args.theme)
    html = render_md_to_html(md_text, theme)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"OK: {args.output} ({len(html)} bytes, theme={args.theme})")
    else:
        sys.stdout.write(html)


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MD → HTML 渲染器（微信公众号排版）")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list-themes", help="列出可用主题")

    p = sub.add_parser("render", help="渲染 MD 为 HTML")
    p.add_argument("input", help="Markdown 文件路径")
    p.add_argument("--theme", "-t", default="blue-minimal", help="主题 ID（默认 blue-minimal）")
    p.add_argument("--output", "-o", default=None, help="输出 HTML 文件路径（不指定则输出到 stdout）")

    e = sub.add_parser("extract-style", help="从公众号文章 URL 中拆解排版样式")
    e.add_argument("url", help="公众号文章 URL")
    e.add_argument("--name", required=True, help="主题中文名（必填）")
    e.add_argument("--id", required=True, help="主题目录名（必填，英文，用于 --theme 参数）")
    e.add_argument("--description", default=None, help="主题描述（可选）")

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "list-themes":
        cmd_list_themes(args)
    elif args.command == "render":
        cmd_render(args)
    elif args.command == "extract-style":
        cmd_extract_style(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
