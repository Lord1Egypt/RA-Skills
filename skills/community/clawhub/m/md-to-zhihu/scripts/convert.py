#!/usr/bin/env python3
"""
Markdown to Zhihu (知乎) article HTML converter.

Converts markdown files into formatted HTML optimized for Zhihu articles,
with multiple theme presets and preview support.

Usage:
    python convert.py input.md [-o output.html] [--theme zhihu]
    python convert.py input.md --content-only  # Output clean HTML for API

Dependencies:
    pip install markdown pygments beautifulsoup4
"""

import argparse
import re
import sys
from pathlib import Path

try:
    import markdown
    from markdown.extensions.codehilite import CodeHiliteExtension
    from markdown.extensions.fenced_code import FencedCodeExtension
    from markdown.extensions.tables import TableExtension
    from markdown.extensions.toc import TocExtension
    from markdown.extensions.footnotes import FootnoteExtension
except ImportError:
    print("Error: 'markdown' package not installed. Run: pip install markdown")
    sys.exit(1)

try:
    from pygments.formatters import HtmlFormatter
except ImportError:
    print("Error: 'pygments' package not installed. Run: pip install pygments")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup, Tag
except ImportError:
    print("Error: 'beautifulsoup4' package not installed. Run: pip install beautifulsoup4")
    sys.exit(1)


# ──────────────────────────────────────────────
# Theme Definitions
# ──────────────────────────────────────────────

THEMES = {
    "zhihu": {
        "name": "知乎蓝",
        "primary": "#0066FF",
        "primary_light": "#EBF3FF",
        "primary_dark": "#0052CC",
        "primary_gradient": "linear-gradient(135deg, #0066FF 0%, #4D94FF 100%)",
        "text": "#1A1A1A",
        "text_secondary": "#646464",
        "text_light": "#999999",
        "bg": "#ffffff",
        "bg_code": "#1e1e2e",
        "bg_code_text": "#d4d4d4",
        "bg_code_inline": "#EBF3FF",
        "bg_blockquote": "#F6F8FA",
        "border": "#E5E5E5",
        "border_light": "#F0F0F0",
        "font_body": "-apple-system, BlinkMacSystemFont, 'PingFang SC', 'Helvetica Neue', 'Microsoft YaHei', sans-serif",
        "font_size": "15px",
        "line_height": "1.8",
        "font_code": "'Fira Code', 'JetBrains Mono', Consolas, Monaco, 'Courier New', monospace",
        "pygments_style": "monokai",
    },
    "elegant": {
        "name": "优雅灰",
        "primary": "#34495E",
        "primary_light": "#F0F3F5",
        "primary_dark": "#2C3E50",
        "primary_gradient": "linear-gradient(135deg, #34495E 0%, #5D7B93 100%)",
        "text": "#2C3E50",
        "text_secondary": "#7F8C8D",
        "text_light": "#999999",
        "bg": "#ffffff",
        "bg_code": "#282C34",
        "bg_code_text": "#ABB2BF",
        "bg_code_inline": "#F0F3F5",
        "bg_blockquote": "#F8F9FA",
        "border": "#DCE1E4",
        "border_light": "#F0F0F0",
        "font_body": "'Georgia', 'Songti SC', 'SimSun', -apple-system, serif",
        "font_size": "16px",
        "line_height": "2.0",
        "font_code": "Consolas, Monaco, 'Courier New', monospace",
        "pygments_style": "one-dark",
    },
    "tech": {
        "name": "科技紫",
        "primary": "#6C5CE7",
        "primary_light": "#F0EDFD",
        "primary_dark": "#5A4BD1",
        "primary_gradient": "linear-gradient(135deg, #6C5CE7 0%, #A29BFE 100%)",
        "text": "#2D3436",
        "text_secondary": "#636E72",
        "text_light": "#999999",
        "bg": "#ffffff",
        "bg_code": "#1E1E2E",
        "bg_code_text": "#CDD6F4",
        "bg_code_inline": "#F0EDFD",
        "bg_blockquote": "#F8F7FC",
        "border": "#DDD6FE",
        "border_light": "#F0F0F0",
        "font_body": "-apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', 'Segoe UI', sans-serif",
        "font_size": "15px",
        "line_height": "1.8",
        "font_code": "'Fira Code', 'JetBrains Mono', Consolas, monospace",
        "pygments_style": "dracula",
    },
    "warm": {
        "name": "温暖橙",
        "primary": "#E67E22",
        "primary_light": "#FEF5EC",
        "primary_dark": "#D35400",
        "primary_gradient": "linear-gradient(135deg, #E67E22 0%, #F0A653 100%)",
        "text": "#34495E",
        "text_secondary": "#7F8C8D",
        "text_light": "#999999",
        "bg": "#ffffff",
        "bg_code": "#2D2D2D",
        "bg_code_text": "#D4D4D4",
        "bg_code_inline": "#FEF5EC",
        "bg_blockquote": "#FFFAF5",
        "border": "#F0D0B0",
        "border_light": "#F5EAD8",
        "font_body": "-apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif",
        "font_size": "15px",
        "line_height": "1.8",
        "font_code": "Consolas, Monaco, 'Courier New', monospace",
        "pygments_style": "monokai",
    },
    "nature": {
        "name": "自然绿",
        "primary": "#00B894",
        "primary_light": "#E8FAF5",
        "primary_dark": "#00A381",
        "primary_gradient": "linear-gradient(135deg, #00B894 0%, #55EFC4 100%)",
        "text": "#2D3436",
        "text_secondary": "#636E72",
        "text_light": "#999999",
        "bg": "#ffffff",
        "bg_code": "#1E272E",
        "bg_code_text": "#D4D4D4",
        "bg_code_inline": "#E8FAF5",
        "bg_blockquote": "#F5FBF8",
        "border": "#B2DFDB",
        "border_light": "#E0F2F1",
        "font_body": "-apple-system, BlinkMacSystemFont, 'PingFang SC', 'Microsoft YaHei', sans-serif",
        "font_size": "15px",
        "line_height": "1.8",
        "font_code": "Consolas, Monaco, 'Courier New', monospace",
        "pygments_style": "monokai",
    },
}


# ──────────────────────────────────────────────
# Style Generator
# ──────────────────────────────────────────────

def build_styles(theme_name: str = "zhihu") -> dict:
    """Build a complete inline-styles dictionary from a theme."""
    t = THEMES.get(theme_name, THEMES["zhihu"])
    return {
        "container": (
            f"max-width: 100%;"
            f"font-family: {t['font_body']};"
            f"font-size: {t['font_size']};"
            f"line-height: {t['line_height']};"
            f"color: {t['text']};"
            f"word-wrap: break-word;"
            f"overflow-wrap: break-word;"
        ),
        "h1": (
            f"font-size: 24px;"
            f"font-weight: bold;"
            f"color: {t['primary']};"
            f"text-align: center;"
            f"margin: 30px 0 20px 0;"
            f"padding-bottom: 12px;"
            f"border-bottom: 2px solid {t['primary']};"
            f"line-height: 1.4;"
        ),
        "h2": (
            f"font-size: 20px;"
            f"font-weight: bold;"
            f"color: {t['primary']};"
            f"margin: 28px 0 16px 0;"
            f"padding: 4px 0 4px 12px;"
            f"border-left: 4px solid {t['primary']};"
            f"line-height: 1.4;"
        ),
        "h3": (
            f"font-size: 17px;"
            f"font-weight: bold;"
            f"color: {t['text']};"
            f"margin: 24px 0 12px 0;"
            f"padding-left: 8px;"
            f"line-height: 1.4;"
        ),
        "h4": (
            f"font-size: 15px;"
            f"font-weight: bold;"
            f"color: {t['text_secondary']};"
            f"margin: 20px 0 10px 0;"
            f"line-height: 1.4;"
        ),
        "p": (
            f"margin: 0 0 16px 0;"
            f"text-align: justify;"
            f"line-height: {t['line_height']};"
            f"color: {t['text']};"
        ),
        "strong": f"font-weight: bold; color: {t['primary_dark']};",
        "em": f"font-style: italic;",
        "del": f"text-decoration: line-through; color: {t['text_light']};",
        "a": (
            f"color: {t['primary']};"
            f"text-decoration: none;"
            f"border-bottom: 1px solid {t['primary']};"
            f"word-break: break-all;"
            f"padding-bottom: 1px;"
        ),
        "ul": f"margin: 8px 0 16px 0; padding-left: 2em; list-style-type: disc;",
        "ol": f"margin: 8px 0 16px 0; padding-left: 2em;",
        "li": f"margin: 5px 0; line-height: {t['line_height']};",
        "blockquote": (
            f"margin: 16px 0;"
            f"padding: 16px 20px;"
            f"background: {t['bg_blockquote']};"
            f"border-left: 4px solid {t['primary']};"
            f"color: {t['text_secondary']};"
            f"font-size: 14px;"
            f"line-height: 1.75;"
            f"border-radius: 0 6px 6px 0;"
        ),
        "blockquote_p": (
            f"margin: 0 0 8px 0;"
            f"text-align: justify;"
            f"line-height: 1.75;"
            f"color: {t['text_secondary']};"
        ),
        "code_inline": (
            f"background: {t['bg_code_inline']};"
            f"color: {t['primary']};"
            f"padding: 2px 6px;"
            f"border-radius: 3px;"
            f"font-family: {t['font_code']};"
            f"font-size: 90%;"
            f"word-break: break-all;"
        ),
        "code_block_wrapper": (
            f"background: {t['bg_code']};"
            f"border-radius: 8px;"
            f"margin: 16px 0;"
            f"overflow: hidden;"
        ),
        "code_block_header": (
            f"display: flex;"
            f"justify-content: space-between;"
            f"align-items: center;"
            f"padding: 8px 16px;"
            f"background: rgba(255,255,255,0.06);"
            f"border-bottom: 1px solid rgba(255,255,255,0.08);"
        ),
        "code_block_lang": (
            f"font-size: 12px;"
            f"color: rgba(255,255,255,0.5);"
            f"font-family: {t['font_code']};"
            f"text-transform: uppercase;"
            f"letter-spacing: 0.5px;"
        ),
        "code_block_dots": "display: flex; gap: 6px;",
        "code_block_dot": "width: 10px; height: 10px; border-radius: 50%;",
        "code_block_body": (
            f"padding: 16px;"
            f"overflow-x: auto;"
            f"font-family: {t['font_code']};"
            f"font-size: 13px;"
            f"line-height: 1.6;"
            f"color: {t['bg_code_text']};"
            f"-webkit-overflow-scrolling: touch;"
        ),
        "table_wrapper": (
            f"overflow-x: auto;"
            f"margin: 16px 0;"
            f"-webkit-overflow-scrolling: touch;"
        ),
        "table": (
            f"width: 100%;"
            f"border-collapse: collapse;"
            f"font-size: 14px;"
            f"border: 1px solid {t['border']};"
        ),
        "th": (
            f"background: {t['primary']};"
            f"color: #ffffff;"
            f"font-weight: bold;"
            f"padding: 10px 14px;"
            f"text-align: left;"
            f"border: 1px solid {t['primary_dark']};"
            f"font-size: 14px;"
            f"white-space: nowrap;"
        ),
        "td": (
            f"padding: 9px 14px;"
            f"border: 1px solid {t['border']};"
            f"line-height: 1.6;"
            f"font-size: 14px;"
        ),
        "td_even": (
            f"padding: 9px 14px;"
            f"border: 1px solid {t['border']};"
            f"line-height: 1.6;"
            f"font-size: 14px;"
            f"background: {t['primary_light']};"
        ),
        "hr": (
            f"border: none;"
            f"height: 1px;"
            f"background: {t['border']};"
            f"margin: 30px 0;"
        ),
        "img": (
            f"max-width: 100%;"
            f"height: auto;"
            f"border-radius: 6px;"
            f"margin: 10px auto;"
            f"display: block;"
        ),
        "img_caption": (
            f"text-align: center;"
            f"font-size: 13px;"
            f"color: {t['text_light']};"
            f"margin: 6px 0 16px 0;"
            f"line-height: 1.5;"
        ),
        "task_done": (
            f"color: {t['text_light']};"
            f"text-decoration: line-through;"
        ),
        "footnote_section": (
            f"margin-top: 30px;"
            f"padding-top: 15px;"
            f"border-top: 1px solid {t['border']};"
            f"font-size: 13px;"
            f"color: {t['text_secondary']};"
        ),
        "footnote_ref": (
            f"color: {t['primary']};"
            f"font-size: 12px;"
            f"vertical-align: super;"
            f"text-decoration: none;"
            f"font-weight: bold;"
        ),
    }


# ──────────────────────────────────────────────
# Markdown Pre-processing
# ──────────────────────────────────────────────

def preprocess_markdown(md_text: str) -> str:
    """Pre-process markdown for better compatibility."""
    # Convert task lists: - [ ] and - [x]
    md_text = re.sub(
        r"^(\s*[-*])\s*\[x\]\s+(.+)$",
        '\\1 <span class="task-done">\u2705 \\2</span>',
        md_text, flags=re.MULTILINE
    )
    md_text = re.sub(
        r"^(\s*[-*])\s*\[ \]\s+(.+)$",
        "\\1 \u2B1C \\2",
        md_text, flags=re.MULTILINE
    )
    return md_text


def extract_title(md_text: str) -> str:
    """Extract title from first h1 heading."""
    match = re.match(r"^#\s+(.+)", md_text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    for line in md_text.split("\n"):
        line = line.strip()
        if line:
            return line[:100]
    return "Untitled"


def remove_title(md_text: str) -> str:
    """Remove the first h1 heading from markdown (used as article title)."""
    return re.sub(r"^#\s+.+\n*", "", md_text, count=1).lstrip()


# ──────────────────────────────────────────────
# HTML Post-processing with BeautifulSoup
# ──────────────────────────────────────────────

def apply_styles(html: str, styles: dict, theme: dict) -> str:
    """Apply inline styles to all HTML elements using BeautifulSoup."""
    soup = BeautifulSoup(html, "html.parser")

    # --- Headings ---
    for tag_name in ["h1", "h2", "h3", "h4"]:
        for tag in soup.find_all(tag_name):
            tag["style"] = styles[tag_name]

    # --- Paragraphs ---
    for p in soup.find_all("p"):
        if p.parent and p.parent.name == "blockquote":
            p["style"] = styles["blockquote_p"]
        else:
            p["style"] = styles["p"]

    # --- Inline formatting ---
    for strong in soup.find_all("strong"):
        strong["style"] = styles["strong"]
    for em in soup.find_all("em"):
        em["style"] = styles["em"]
    for del_tag in soup.find_all("del"):
        del_tag["style"] = styles["del"]

    # --- Links (Zhihu supports clickable links!) ---
    for a in soup.find_all("a"):
        cls = a.get("class", [])
        if "footnote-backref" in cls or "footnote-ref" in cls:
            a["style"] = styles["footnote_ref"]
        else:
            a["style"] = styles["a"]

    # --- Lists ---
    for ul in soup.find_all("ul"):
        ul["style"] = styles["ul"]
    for ol in soup.find_all("ol"):
        ol["style"] = styles["ol"]
    for li in soup.find_all("li"):
        li["style"] = styles["li"]

    # --- Blockquotes ---
    for bq in soup.find_all("blockquote"):
        bq["style"] = styles["blockquote"]

    # --- Code blocks (codehilite) ---
    for div in soup.find_all("div", class_="codehilite"):
        lang = ""
        classes = div.get("class", [])
        for cls in classes:
            if cls.startswith("language-"):
                lang = cls.replace("language-", "")

        if not lang:
            code_tag = div.find("code")
            if code_tag:
                code_classes = code_tag.get("class", [])
                for cls in code_classes:
                    if cls.startswith("language-"):
                        lang = cls.replace("language-", "")

        inner_html = div.decode_contents()

        # Create styled wrapper
        new_div = soup.new_tag("div")
        new_div["style"] = styles["code_block_wrapper"]

        # Header with dots + language label
        header = soup.new_tag("div")
        header["style"] = styles["code_block_header"]

        dots_div = soup.new_tag("div")
        dots_div["style"] = styles["code_block_dots"]
        for color in ["#FF5F57", "#FEBC2E", "#28C840"]:
            dot = soup.new_tag("span")
            dot["style"] = styles["code_block_dot"] + f" background: {color};"
            dots_div.append(dot)
        header.append(dots_div)

        if lang:
            lang_span = soup.new_tag("span")
            lang_span["style"] = styles["code_block_lang"]
            lang_span.string = lang.upper()
            header.append(lang_span)

        new_div.append(header)

        # Code body
        body_div = soup.new_tag("div")
        body_div["style"] = styles["code_block_body"]
        body_div.append(BeautifulSoup(inner_html, "html.parser"))
        new_div.append(body_div)

        inner_pre = new_div.find("pre")
        if inner_pre:
            inner_pre["style"] = "margin: 0; padding: 0; background: transparent; overflow: visible;"

        div.replace_with(new_div)

    # --- Bare <pre> blocks (non-highlighted) ---
    for pre in soup.find_all("pre"):
        if pre.parent and pre.parent.get("style", "").startswith("padding:"):
            continue
        wrapper = soup.new_tag("div")
        wrapper["style"] = styles["code_block_wrapper"]
        body = soup.new_tag("div")
        body["style"] = styles["code_block_body"]
        pre_copy = pre.extract()
        pre_copy["style"] = "margin: 0; padding: 0; background: transparent; overflow: visible;"
        body.append(pre_copy)
        wrapper.append(body)
        pre.insert_after(wrapper) if pre.parent else None

    # --- Inline code ---
    for code in soup.find_all("code"):
        if code.parent and code.parent.name == "pre":
            continue
        if code.parent and code.parent.name == "div":
            parent_style = code.parent.get("style", "")
            if "overflow-x" in parent_style or "font-family" in parent_style:
                continue
        code["style"] = styles["code_inline"]

    # --- Tables ---
    for table in soup.find_all("table"):
        wrapper = soup.new_tag("div")
        wrapper["style"] = styles["table_wrapper"]
        table["style"] = styles["table"]
        for th in table.find_all("th"):
            th["style"] = styles["th"]
        tbody = table.find("tbody")
        if tbody:
            for i, tr in enumerate(tbody.find_all("tr")):
                for td in tr.find_all("td"):
                    td["style"] = styles["td_even"] if i % 2 == 1 else styles["td"]
        table.wrap(wrapper)

    # --- Horizontal rules ---
    for hr in soup.find_all("hr"):
        hr["style"] = styles["hr"]

    # --- Images ---
    for img in soup.find_all("img"):
        img["style"] = styles["img"]
        alt = img.get("alt", "").strip()
        if alt and alt.lower() not in ("image", "img", ""):
            caption = soup.new_tag("p")
            caption["style"] = styles["img_caption"]
            caption.string = alt
            img.insert_after(caption)

    # --- Task list done items ---
    for span in soup.find_all("span", class_="task-done"):
        span["style"] = styles["task_done"]

    # --- Footnote section ---
    for div in soup.find_all("div", class_="footnote"):
        div["style"] = styles["footnote_section"]
        for hr_in_fn in div.find_all("hr"):
            hr_in_fn.decompose()

    return str(soup)


# ──────────────────────────────────────────────
# Content Converter (clean HTML for Zhihu API)
# ──────────────────────────────────────────────

def convert_to_zhihu_content(md_content: str) -> str:
    """Convert markdown to clean HTML suitable for Zhihu article content.
    
    Returns HTML without excessive inline styles - Zhihu applies its own styling.
    This is used by the publisher for API-based article creation.
    """
    md_content = preprocess_markdown(md_content)
    md_content = remove_title(md_content)

    extensions = [
        TableExtension(),
        FencedCodeExtension(),
        FootnoteExtension(),
        TocExtension(permalink=False),
        CodeHiliteExtension(
            noclasses=True,
            linenums=False,
            guess_lang=True,
            pygments_style="monokai",
        ),
    ]

    md_parser = markdown.Markdown(extensions=extensions)
    html = md_parser.convert(md_content)

    # Light post-processing for Zhihu compatibility
    soup = BeautifulSoup(html, "html.parser")

    # Ensure code blocks use Zhihu-friendly structure
    for div in soup.find_all("div", class_="codehilite"):
        lang = ""
        code_tag = div.find("code")
        if code_tag:
            for cls in code_tag.get("class", []):
                if cls.startswith("language-"):
                    lang = cls.replace("language-", "")

        pre = div.find("pre")
        if pre:
            new_pre = soup.new_tag("pre")
            new_code = soup.new_tag("code")
            if lang:
                new_code["class"] = [f"language-{lang}"]
            new_code.append(BeautifulSoup(pre.decode_contents(), "html.parser"))
            new_pre.append(new_code)
            div.replace_with(new_pre)

    # Ensure images are wrapped in figure tags for Zhihu
    for img in soup.find_all("img"):
        if img.parent and img.parent.name != "figure":
            figure = soup.new_tag("figure")
            img_copy = img.extract()
            figure.append(img_copy)
            alt = img_copy.get("alt", "").strip()
            if alt and alt.lower() not in ("image", "img", ""):
                figcaption = soup.new_tag("figcaption")
                figcaption.string = alt
                figure.append(figcaption)
            img.insert_after(figure) if img.parent else soup.append(figure)

    return str(soup)


# ──────────────────────────────────────────────
# Preview Converter (styled HTML with themes)
# ──────────────────────────────────────────────

def convert_to_preview(md_content: str, theme_name: str = "zhihu") -> str:
    """Convert markdown to a full preview HTML page with inline styles and copy functionality."""
    t = THEMES.get(theme_name, THEMES["zhihu"])
    styles = build_styles(theme_name)

    title = extract_title(md_content)
    md_body = remove_title(md_content)
    md_body = preprocess_markdown(md_body)

    extensions = [
        TableExtension(),
        FencedCodeExtension(),
        FootnoteExtension(),
        TocExtension(permalink=False),
        CodeHiliteExtension(
            pygments_style=t["pygments_style"],
            noclasses=True,
            linenums=False,
            guess_lang=True,
        ),
    ]

    md_parser = markdown.Markdown(extensions=extensions)
    raw_html = md_parser.convert(md_body)
    styled_html = apply_styles(raw_html, styles, t)

    return build_document(title, styled_html, styles, t, theme_name)


def build_document(title: str, body_html: str, styles: dict, theme: dict, theme_name: str) -> str:
    """Generate a complete HTML document with copy-to-clipboard and preview frame."""
    primary = theme["primary"]
    font = theme["font_body"]

    # Build theme selector options
    theme_options = ""
    for key, val in THEMES.items():
        selected = "selected" if key == theme_name else ""
        theme_options += f'<option value="{key}" {selected}>{val["name"]} ({key})</option>\n'

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>知乎文章预览 - {title}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: #F6F7F8;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            font-family: {font};
        }}
        .toolbar {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: #fff;
            padding: 14px 24px;
            border-radius: 10px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.08);
            margin-bottom: 24px;
            display: flex;
            gap: 16px;
            align-items: center;
            flex-wrap: wrap;
            max-width: 750px;
            width: 100%;
        }}
        .toolbar button {{
            background: {primary};
            color: #fff;
            border: none;
            padding: 10px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 500;
            transition: all 0.2s;
            box-shadow: 0 2px 6px rgba(0,0,0,0.12);
        }}
        .toolbar button:hover {{
            opacity: 0.9;
            transform: translateY(-1px);
            box-shadow: 0 4px 10px rgba(0,0,0,0.15);
        }}
        .toolbar button:active {{ transform: translateY(0); }}
        .toolbar .hint {{
            color: #888;
            font-size: 13px;
        }}
        .toolbar .status {{
            font-size: 13px;
            font-weight: 500;
            transition: opacity 0.3s;
        }}
        .toolbar select {{
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 6px;
            font-size: 13px;
            cursor: pointer;
            background: #fff;
        }}
        .article-frame {{
            background: #fff;
            max-width: 750px;
            width: 100%;
            border-radius: 4px;
            box-shadow: 0 1px 3px rgba(26,26,26,0.1);
            overflow: hidden;
        }}
        .article-header {{
            padding: 32px 24px 0;
        }}
        .article-title {{
            font-size: 24px;
            font-weight: 600;
            color: #1A1A1A;
            line-height: 1.4;
            margin-bottom: 16px;
        }}
        .article-meta {{
            font-size: 14px;
            color: #8590A6;
            padding-bottom: 16px;
            border-bottom: 1px solid #F0F2F7;
        }}
        .article-content {{
            padding: 24px;
        }}
        #content {{
            font-family: {font};
        }}
        #content pre {{ background: transparent !important; }}
        .zhihu-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: #F6F7F8;
            padding: 4px 12px;
            border-radius: 4px;
            font-size: 12px;
            color: #8590A6;
        }}
        .zhihu-badge svg {{
            width: 16px;
            height: 16px;
        }}
    </style>
</head>
<body>
    <div class="toolbar">
        <button onclick="copyContent()">复制内容到剪贴板</button>
        <select onchange="switchTheme(this.value)" title="切换主题">
            {theme_options}
        </select>
        <span class="hint">复制后粘贴到知乎编辑器</span>
        <span class="status" id="status"></span>
    </div>
    <div class="article-frame">
        <div class="article-header">
            <h1 class="article-title">{title}</h1>
            <div class="article-meta">
                <span class="zhihu-badge">
                    <svg viewBox="0 0 24 24" fill="#0066FF"><path d="M5.721 0C2.251 0 0 2.25 0 5.719V18.28C0 21.751 2.252 24 5.721 24h12.56C21.751 24 24 21.75 24 18.281V5.72C24 2.249 21.75 0 18.281 0zm1.964 4.078h6.46l.09 1.252h-3.85l-.5 3.797h3.478c0 0-.074 5.089-.26 6.291-.186 1.201-.54 1.862-1.1 2.254-.56.392-1.17.54-2.07.576-.598.024-1.597.009-1.597.009l-.32-1.473s.985.03 1.564.009c.579-.021.913-.1 1.177-.345.264-.246.383-.702.45-1.36.068-.659.194-4.508.194-4.508H9.273l-.658 8.67H7.17l.66-8.67H5.504V9.127h2.465l.5-3.797H6.05z"/></svg>
                    知乎文章预览
                </span>
            </div>
        </div>
        <div class="article-content">
            <div id="content" style="{styles['container']}">
{body_html}
            </div>
        </div>
    </div>
    <script>
        function copyContent() {{
            const content = document.getElementById('content');
            const range = document.createRange();
            range.selectNodeContents(content);
            const sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(range);
            try {{
                document.execCommand('copy');
                showStatus('\u2705 已复制！可直接粘贴到知乎文章编辑器', '#52C41A');
            }} catch (e) {{
                showStatus('\u274c 复制失败，请手动 Ctrl+A 全选后复制', '#F5222D');
            }}
            sel.removeAllRanges();
        }}
        function showStatus(msg, color) {{
            const el = document.getElementById('status');
            el.textContent = msg;
            el.style.color = color;
            setTimeout(() => {{
                el.style.opacity = '0';
                setTimeout(() => {{ el.textContent = ''; el.style.opacity = '1'; }}, 300);
            }}, 3000);
        }}
        function switchTheme(theme) {{
            const url = new URL(window.location.href);
            // Reload page can't change server-rendered theme, so we just hint the user
            showStatus('请重新运行转换命令并添加 --theme ' + theme, '#0066FF');
        }}
    </script>
</body>
</html>"""


# ──────────────────────────────────────────────
# CLI Entry Point
# ──────────────────────────────────────────────

def _out(msg: str):
    """Print with UTF-8 encoding for Windows compatibility."""
    import io
    try:
        out = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace", line_buffering=True)
        out.write(msg + "\n")
        out.flush()
        out.detach()
    except Exception:
        print(msg)


def convert_single(input_path: Path, output_path: Path | None, theme: str, content_only: bool):
    """Convert a single markdown file. Returns output path."""
    if not input_path.exists():
        _out(f"错误: 文件不存在: {input_path}")
        return None

    suffix = "_zhihu_content.html" if content_only else "_zhihu.html"
    if not output_path:
        output_path = input_path.with_name(f"{input_path.stem}{suffix}")

    md_content = input_path.read_text(encoding="utf-8")

    if content_only:
        html_content = convert_to_zhihu_content(md_content)
    else:
        html_content = convert_to_preview(md_content, theme)

    output_path.write_text(html_content, encoding="utf-8")
    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Markdown \u2192 知乎文章 HTML 转换器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python convert.py article.md                     # 转换单篇文章
  python convert.py article.md --theme tech        # 科技紫主题
  python convert.py article.md -o output.html      # 指定输出文件
  python convert.py article.md --content-only      # 仅输出纯净 HTML
  python convert.py --dir ./articles               # 批量转换目录下所有 .md
  python convert.py --dir ./articles --theme warm  # 批量转换，温暖橙主题
        """,
    )
    parser.add_argument("input", nargs="?", help="输入 Markdown 文件路径")
    parser.add_argument("-o", "--output", help="输出 HTML 文件路径 (默认: {input}_zhihu.html)")
    parser.add_argument(
        "--theme",
        choices=list(THEMES.keys()),
        default="zhihu",
        help="主题风格 (默认: zhihu)",
    )
    parser.add_argument(
        "--content-only",
        action="store_true",
        help="仅输出纯净 HTML 内容 (用于 API 发布)",
    )
    parser.add_argument(
        "--dir",
        help="批量转换：指定目录路径，转换该目录下所有 .md 文件",
    )

    args = parser.parse_args()

    theme = THEMES[args.theme]

    # ── Batch mode ──
    if args.dir:
        dir_path = Path(args.dir)
        if not dir_path.is_dir():
            _out(f"错误: 目录不存在: {dir_path}")
            sys.exit(1)

        md_files = sorted(dir_path.glob("*.md"))
        if not md_files:
            _out(f"目录下没有找到 .md 文件: {dir_path}")
            sys.exit(1)

        _out(f"批量转换: 找到 {len(md_files)} 个 Markdown 文件")
        _out(f"主题: {theme['name']}")
        _out("-" * 50)

        success = 0
        failed = 0
        for md_file in md_files:
            out_path = convert_single(md_file, None, args.theme, args.content_only)
            if out_path:
                _out(f"  [OK] {md_file.name} -> {out_path.name}")
                success += 1
            else:
                _out(f"  [FAIL] {md_file.name}")
                failed += 1

        _out("-" * 50)
        _out(f"批量转换完成: 成功 {success}, 失败 {failed}, 共 {len(md_files)}")
        sys.exit(0)

    # ── Single file mode ──
    if not args.input:
        parser.print_help()
        sys.exit(0)

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else None
    result = convert_single(input_path, output_path, args.theme, args.content_only)

    if not result:
        sys.exit(1)

    _out(f"[OK] 转换完成!")
    _out(f"  输入:  {input_path}")
    _out(f"  输出:  {result}")
    if not args.content_only:
        _out(f"  主题:  {theme['name']}")
        _out(f"\n使用方法:")
        _out(f"  1. 浏览器打开 {result}")
        _out(f"  2. 点击「复制内容到剪贴板」")
        _out(f"  3. 在知乎文章编辑器中粘贴")
    else:
        _out(f"\n内容已转换为知乎兼容 HTML，可用于 API 发布")


if __name__ == "__main__":
    main()
