"""
Markdown to WeChat-compatible HTML converter.

Key improvements over wewrite:
1. CSS sanitizer: strips WeChat-incompatible properties (border-radius, box-shadow,
   linear-gradient, letter-spacing, opacity, text-shadow) during conversion
2. Always treats images as local files to upload (never trusts existing mmbiz URLs)
3. CJK spacing, bold punctuation fix, list-to-section conversion
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import markdown
from bs4 import BeautifulSoup

from theme import Theme, load_theme, get_inline_css_rules


# ── WeChat CSS compatibility ──────────────────────────────────────────────

# Properties that WeChat's renderer silently strips. Including them wastes
# bandwidth and creates false expectations. We remove them at conversion time.
UNSAFE_CSS_PROPS = {
    "border-radius",
    "box-shadow",
    "text-shadow",
    "letter-spacing",
    "opacity",
    "linear-gradient",
    "background-clip",
    "text-fill-color",
    "backdrop-filter",
    "filter",
    "transition",
    "animation",
    "transform",
    # Flex/grid props — WeChat stores them but renderer ignores flexbox layout
    "flex",
    "flex-shrink",
    "flex-grow",
    "flex-basis",
    "flex-direction",
    "justify-content",
    "align-items",
    "align-self",
    "align-content",
    "gap",
    "row-gap",
    "column-gap",
    "grid-template-columns",
    "grid-template-rows",
    "grid-column",
    "grid-row",
}

# CSS values containing these substrings are also unsafe
UNSAFE_CSS_VALUES = {
    "linear-gradient",
    "radial-gradient",
    "rgba(",  # WeChat strips alpha channel — use solid hex instead
}


def _sanitize_style(style_str: str) -> str:
    """Remove WeChat-incompatible CSS properties and values."""
    if not style_str:
        return style_str
    cleaned = []
    for decl in style_str.split(";"):
        decl = decl.strip()
        if not decl or ":" not in decl:
            continue
        prop, val = decl.split(":", 1)
        prop = prop.strip().lower()
        val = val.strip()
        # Skip unsafe properties
        if prop in UNSAFE_CSS_PROPS:
            continue
        # Skip unsafe values
        val_lower = val.lower()
        if any(unsafe in val_lower for unsafe in UNSAFE_CSS_VALUES):
            # Keep background color if it was a gradient — extract first color
            if prop == "background" and "linear-gradient" in val_lower:
                match = re.search(r'#([0-9a-fA-F]{6})', val)
                if match:
                    cleaned.append(f"{prop}: #{match.group(1)}")
                continue
            continue
        # Replace display:flex/inline-flex/grid with display:block
        if prop == "display" and val_lower in ("flex", "inline-flex", "grid", "inline-grid"):
            val = "block"
        cleaned.append(f"{prop}: {val}")
    return "; ".join(cleaned)


def _sanitize_html_styles(html: str) -> str:
    """Walk all elements with style attributes and sanitize them."""
    soup = BeautifulSoup(html, "html.parser")
    for elem in soup.find_all(attrs={"style": True}):
        original = elem.get("style", "")
        sanitized = _sanitize_style(original)
        if sanitized != original:
            elem["style"] = sanitized
    return str(soup)


# ── Converter ─────────────────────────────────────────────────────────────

@dataclass
class ConvertResult:
    html: str
    title: str
    digest: str
    images: list = field(default_factory=list)  # (src, alt) tuples


class WeChatConverter:
    """Convert Markdown to WeChat-compatible inline-style HTML."""

    def __init__(self, theme: Optional[Theme] = None, theme_name: str = "xinming-lab"):
        if theme is not None:
            self._theme = theme
        else:
            self._theme = load_theme(theme_name)
        self._css_rules = get_inline_css_rules(self._theme)

    def convert(self, markdown_text: str) -> ConvertResult:
        title = self._extract_title(markdown_text)
        markdown_text = self._strip_h1(markdown_text)

        # CJK spacing fix
        markdown_text = self._fix_cjk_spacing(markdown_text)

        # Parse Markdown → HTML
        html = self._markdown_to_html(markdown_text)

        # Process images
        html, images = self._process_images(html)

        # CJK fixes
        html = self._fix_cjk_bold_punctuation(html)
        html = self._convert_lists_to_sections(html)

        # Convert external links to footnotes
        html = self._convert_links_to_footnotes(html)

        # Apply theme inline styles
        html = self._apply_inline_styles(html)

        # WeChat fixes
        html = self._apply_wechat_fixes(html)

        # ★ Sanitize CSS — strip WeChat-incompatible properties
        html = _sanitize_html_styles(html)

        # Generate digest
        digest = self._generate_digest(html)

        return ConvertResult(html=html, title=title, digest=digest, images=images)

    def convert_file(self, input_path: str) -> ConvertResult:
        path = Path(input_path)
        if not path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        text = path.read_text(encoding="utf-8")
        return self.convert(text)

    # -- internal --

    def _extract_title(self, text: str) -> str:
        for line in text.split("\n"):
            stripped = line.strip()
            if stripped.startswith("# ") and not stripped.startswith("## "):
                return stripped[2:].strip()
        return ""

    def _strip_h1(self, text: str) -> str:
        lines = []
        for line in text.split("\n"):
            stripped = line.strip()
            if stripped.startswith("# ") and not stripped.startswith("## "):
                continue
            lines.append(line)
        return "\n".join(lines)

    def _markdown_to_html(self, text: str) -> str:
        extensions = [
            "markdown.extensions.fenced_code",
            "markdown.extensions.tables",
            "markdown.extensions.nl2br",
            "markdown.extensions.sane_lists",
        ]
        md = markdown.Markdown(extensions=extensions)
        return md.convert(text)

    def _process_images(self, html: str) -> tuple:
        """Extract image references and ensure responsive styling."""
        soup = BeautifulSoup(html, "html.parser")
        images = []
        for img in soup.find_all("img"):
            src = img.get("src", "")
            alt = img.get("alt", "")
            if src:
                images.append((src, alt))
            # Responsive styles (no border-radius — WeChat strips it)
            existing = img.get("style", "")
            if "max-width" not in existing:
                additions = "max-width: 100%; height: auto; display: block; margin: 24px auto"
                img["style"] = f"{existing}; {additions}" if existing else additions
        return str(soup), images

    def _apply_inline_styles(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        for selector, styles in self._css_rules.items():
            if selector.strip() == "body":
                continue
            try:
                elements = soup.select(selector)
            except Exception:
                continue
            for elem in elements:
                existing = elem.get("style", "")
                style_dict = {}
                if existing:
                    for item in existing.split(";"):
                        if ":" in item:
                            key, val = item.split(":", 1)
                            style_dict[key.strip()] = val.strip()
                for prop, val in styles.items():
                    if prop not in style_dict:
                        style_dict[prop] = val
                elem["style"] = "; ".join(f"{k}: {v}" for k, v in style_dict.items())
        return str(soup)

    def _apply_wechat_fixes(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        text_color = self._theme.colors.get("text", "#333333")
        for p in soup.find_all("p"):
            style = p.get("style", "")
            if "color" not in style:
                p["style"] = f"{style}; color: {text_color}" if style else f"color: {text_color}"
        for pre in soup.find_all("pre"):
            style = pre.get("style", "")
            if "white-space" not in style:
                pre["style"] = f"{style}; white-space: pre-wrap; word-wrap: break-word" if style else "white-space: pre-wrap; word-wrap: break-word"
        return str(soup)

    # -- CJK fixes --

    def _fix_cjk_spacing(self, text: str) -> str:
        cjk = r'[\u4e00-\u9fff\u3400-\u4dbf\u3000-\u303f\uff00-\uffef]'
        latin = r'[A-Za-z0-9]'
        lines = text.split('\n')
        result = []
        in_code_block = False
        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                result.append(line)
                continue
            if in_code_block:
                result.append(line)
                continue
            # Skip image lines — CJK spacing would corrupt filenames like 配图1.png
            if '![' in line and '](' in line:
                result.append(line)
                continue
            # Skip inline HTML with src/href attributes
            if 'src=' in line or 'href=' in line:
                result.append(line)
                continue
            line = re.sub(f'({cjk})({latin})', r'\1 \2', line)
            line = re.sub(f'({latin})({cjk})', r'\1 \2', line)
            result.append(line)
        return '\n'.join(result)

    def _fix_cjk_bold_punctuation(self, html: str) -> str:
        pattern = r'(<strong>)(.*?)([，。！？；：、]+)(</strong>)'
        return re.sub(pattern, r'\1\2\4\3', html)

    def _convert_lists_to_sections(self, html: str) -> str:
        """Convert <ul>/<ol> to WeChat-safe table layout.

        WeChat renderer ignores flexbox (display:flex, align-items, flex:1,
        flex-shrink) — children collapse to block. Using <table> with <td>
        gives reliable two-column layout (bullet/number + content).
        """
        soup = BeautifulSoup(html, "html.parser")
        text_color = self._theme.colors.get("text", "#333333")
        primary = self._theme.colors.get("primary", "#534AB7")

        for ul in soup.find_all("ul"):
            table = soup.new_tag("table")
            table["style"] = "width: 100%; border-collapse: collapse; margin: 12px 0"
            for li in ul.find_all("li", recursive=False):
                tr = soup.new_tag("tr")
                # Bullet cell
                bullet_td = soup.new_tag("td")
                bullet_td["style"] = (
                    f"width: 24px; vertical-align: top; "
                    f"color: {primary}; font-size: 15px; line-height: 1.8; "
                    f"padding: 0 8px 0 0; text-align: center"
                )
                bullet_td.string = "•"
                # Content cell
                content_td = soup.new_tag("td")
                content_td["style"] = (
                    f"vertical-align: top; color: {text_color}; "
                    f"font-size: 15px; line-height: 1.8; padding: 0 0 8px 0"
                )
                for child in list(li.children):
                    content_td.append(child.extract() if hasattr(child, "extract") else child)
                tr.append(bullet_td)
                tr.append(content_td)
                table.append(tr)
            ul.replace_with(table)

        for ol in soup.find_all("ol"):
            table = soup.new_tag("table")
            table["style"] = "width: 100%; border-collapse: collapse; margin: 12px 0"
            for num, li in enumerate(ol.find_all("li", recursive=False), 1):
                tr = soup.new_tag("tr")
                # Number cell
                num_td = soup.new_tag("td")
                num_td["style"] = (
                    f"width: 28px; vertical-align: top; "
                    f"color: {primary}; font-size: 15px; line-height: 1.8; "
                    f"font-weight: 700; padding: 0 8px 0 0; text-align: right"
                )
                num_td.string = f"{num}."
                # Content cell
                content_td = soup.new_tag("td")
                content_td["style"] = (
                    f"vertical-align: top; color: {text_color}; "
                    f"font-size: 15px; line-height: 1.8; padding: 0 0 8px 0"
                )
                for child in list(li.children):
                    content_td.append(child.extract() if hasattr(child, "extract") else child)
                tr.append(num_td)
                tr.append(content_td)
                table.append(tr)
            ol.replace_with(table)
        return str(soup)

    def _convert_links_to_footnotes(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        footnotes = []
        counter = 0
        primary = self._theme.colors.get("primary", "#534AB7")
        for a in soup.find_all("a"):
            href = a.get("href", "")
            if not href or href.startswith("#"):
                continue
            counter += 1
            text = a.get_text()
            footnotes.append((counter, text, href))
            sup = soup.new_tag("sup")
            sup_link = soup.new_tag("span", style=f"color: {primary}; font-size: 12px")
            sup_link.string = f"[{counter}]"
            sup.append(sup_link)
            a.replace_with(text, sup)
        if footnotes:
            hr = soup.new_tag("hr", style="border: none; border-top: 1px solid #e5e5e5; margin: 32px 0 16px")
            soup.append(hr)
            ref_title = soup.new_tag("p", style="font-size: 13px; color: #999999; margin-bottom: 8px; font-weight: 700")
            ref_title.string = "参考链接"
            soup.append(ref_title)
            for num, text, href in footnotes:
                ref = soup.new_tag("p", style="font-size: 12px; color: #999999; margin: 2px 0; word-break: break-all")
                ref.string = f"[{num}] {text}: {href}"
                soup.append(ref)
        return str(soup)

    def _generate_digest(self, html: str, max_bytes: int = 120) -> str:
        soup = BeautifulSoup(html, "html.parser")
        text = soup.get_text(separator=" ", strip=True)
        text = re.sub(r"\s+", " ", text).strip()
        ellipsis = "..."
        ellipsis_bytes = len(ellipsis.encode("utf-8"))
        target_bytes = max_bytes - ellipsis_bytes
        encoded = text.encode("utf-8")
        if len(encoded) <= max_bytes:
            return text
        truncated = encoded[:target_bytes].decode("utf-8", errors="ignore").rstrip()
        return truncated + ellipsis
