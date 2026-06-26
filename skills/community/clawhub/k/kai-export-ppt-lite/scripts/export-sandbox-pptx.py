#!/usr/bin/env python3
"""
export-sandbox-pptx.py — Export HTML presentations to editable PPTX without a browser.

Ported from export-native-pptx.py logic (v5):
  - flatExtract algorithm adapted for no-browser CSS cascade simulation
  - Pre-pass corrections (shape+text sync, adjacent element push)
  - CJK/condensed font width correction
  - Sophisticated segment handling (bold, strike, bgColor, inlineBgBounds)
  - Better word-wrap / auto-size strategy for text boxes

Pure Python: no Playwright, no Chrome. Uses beautifulsoup4 for HTML parsing,
python-pptx for PPTX generation, and Pillow for preview images.

Usage:
    python export-sandbox-pptx.py <presentation.html> [demo/output.pptx] [--width W] [--height H]

Dependencies:
    pip install beautifulsoup4 lxml python-pptx Pillow
"""

import sys
import os
import re
import io
import math
import argparse
import base64
import json
import urllib.request
import copy
import subprocess
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Tuple, Protocol, Set

# ─── Dependency check ─────────────────────────────────────────────────────────

def _detect_missing_deps() -> List[str]:
    missing = []
    try:
        from bs4 import BeautifulSoup, NavigableString, Tag
    except ImportError:
        missing.append("beautifulsoup4")
    try:
        from pptx import Presentation
    except ImportError:
        missing.append("python-pptx")
    try:
        from lxml import etree as _etree
    except ImportError:
        missing.append("lxml")
    try:
        from PIL import Image
    except ImportError:
        missing.append("Pillow")
    return missing


def _attempt_install_missing_deps(missing: List[str]) -> bool:
    if not missing:
        return True
    if os.environ.get("KAI_EXPORT_PPT_LITE_AUTO_INSTALL", "1").lower() in {"0", "false", "no"}:
        return False
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", *missing],
            check=True,
            stdout=sys.stderr,
            stderr=sys.stderr,
        )
        return True
    except Exception:
        return False


def check_deps():
    missing = _detect_missing_deps()
    if not missing:
        return
    print(f"Missing dependencies detected: {', '.join(missing)}", file=sys.stderr)
    print("Attempting runtime install via pip...", file=sys.stderr)
    if _attempt_install_missing_deps(missing):
        missing = _detect_missing_deps()
        if not missing:
            return
    print("Dependency bootstrap failed.", file=sys.stderr)
    print(f"Install manually with: {sys.executable} -m pip install {' '.join(missing)}", file=sys.stderr)
    sys.exit(1)

check_deps()

from bs4 import BeautifulSoup, NavigableString, Tag
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_AUTO_SIZE
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from lxml import etree as _etree


# ─── Constants ───────────────────────────────────────────────────────────────

PX_PER_IN = 108.0  # 1440px / 13.33in
SLIDE_W_IN = 13.33
SLIDE_H_IN = 8.33
CJK_BOX_FACTOR = 1.15
CJK_V_FACTOR = 1.30
CJK_H_FACTOR = 0.15  # extra horizontal space for CJK in PPTX
PPTX_HEIGHT_FACTOR = 1.30  # vertical correction for multi-line CJK text

TEXT_TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li', 'span', 'a'}
RASTER_TAGS = {'img', 'svg', 'canvas'}
CONTAINER_TAGS = {'div', 'section', 'article', 'ul', 'ol'}
INLINE_TAGS = {'strong', 'em', 'b', 'i', 'span', 'a', 'mark', 'code', 'small',
               'kbd', 'var', 'abbr', 'time', 'sup', 'sub', 'br'}
INLINE_BOX_KINDS = {'code', 'kbd', 'badge'}
INLINE_GROUP_KINDS = INLINE_BOX_KINDS | {'link', 'icon'}


# ─── CSS Parsing ──────────────────────────────────────────────────────────────

@dataclass
class CSSRule:
    selector: str
    properties: Dict[str, str]

# Global: root CSS variables, populated during CSS parsing
_ROOT_CSS_VARS: Dict[str, str] = {}


def _iter_css_blocks(css_text: str) -> List[Tuple[str, str]]:
    """Iterate top-level CSS blocks while preserving nested at-rule bodies."""
    blocks: List[Tuple[str, str]] = []
    idx = 0
    length = len(css_text)
    while idx < length:
        while idx < length and css_text[idx].isspace():
            idx += 1
        if idx >= length:
            break
        prelude_start = idx
        while idx < length and css_text[idx] != '{':
            idx += 1
        if idx >= length:
            break
        prelude = css_text[prelude_start:idx].strip()
        idx += 1
        body_start = idx
        depth = 1
        while idx < length and depth > 0:
            if css_text[idx] == '{':
                depth += 1
            elif css_text[idx] == '}':
                depth -= 1
            idx += 1
        body = css_text[body_start:idx - 1]
        if prelude:
            blocks.append((prelude, body))
    return blocks


def _media_query_matches(
    query: str,
    viewport_width_px: float,
    viewport_height_px: Optional[float] = None,
) -> bool:
    """Evaluate a small, layout-oriented subset of media queries."""
    if not query:
        return True
    viewport_height_px = viewport_height_px or VIEWPORT_HEIGHT_PX

    def _clause_matches(clause: str) -> bool:
        clause = clause.strip().lower()
        if not clause:
            return False
        if 'print' in clause and 'screen' not in clause:
            return False
        if 'speech' in clause:
            return False
        width_ok = True
        height_ok = True
        width_constraints = re.findall(r'\((min|max)-width\s*:\s*([^)]+)\)', clause)
        height_constraints = re.findall(r'\((min|max)-height\s*:\s*([^)]+)\)', clause)
        has_known_constraint = bool(width_constraints or height_constraints)
        for feature, raw_value in width_constraints:
            px_value = _resolve_css_length(raw_value.strip())
            if px_value <= 0:
                continue
            if feature == 'min' and viewport_width_px < px_value:
                width_ok = False
            if feature == 'max' and viewport_width_px > px_value:
                width_ok = False
        for feature, raw_value in height_constraints:
            px_value = _resolve_css_length(raw_value.strip())
            if px_value <= 0:
                continue
            if feature == 'min' and viewport_height_px < px_value:
                height_ok = False
            if feature == 'max' and viewport_height_px > px_value:
                height_ok = False
        if not has_known_constraint and clause not in ('all', 'screen'):
            return False
        return width_ok and height_ok

    return any(_clause_matches(part) for part in query.split(','))


def _flatten_active_css(
    css_text: str,
    viewport_width_px: Optional[float] = None,
    viewport_height_px: Optional[float] = None,
) -> str:
    """Flatten CSS into active normal rules for the current viewport."""
    viewport_width_px = viewport_width_px or VIEWPORT_WIDTH_PX
    viewport_height_px = viewport_height_px or VIEWPORT_HEIGHT_PX
    flat_rules: List[str] = []
    for prelude, body in _iter_css_blocks(css_text):
        stripped = prelude.strip()
        if not stripped:
            continue
        if stripped.startswith('@media'):
            media_query = stripped[len('@media'):].strip()
            if _media_query_matches(media_query, viewport_width_px, viewport_height_px):
                nested = _flatten_active_css(body, viewport_width_px, viewport_height_px)
                if nested:
                    flat_rules.append(nested)
            continue
        if stripped.startswith('@layer') or stripped.startswith('@supports'):
            nested = _flatten_active_css(body, viewport_width_px, viewport_height_px)
            if nested:
                flat_rules.append(nested)
            continue
        if stripped.startswith('@'):
            continue
        flat_rules.append(f'{stripped} {{{body}}}')
    return '\n'.join(flat_rules)


def resolve_css_variables(css_text: str) -> str:
    """Resolve :root CSS custom properties (var(--name) and var(--name, fallback))."""
    global _ROOT_CSS_VARS
    # Match ALL :root blocks (there may be multiple)
    for root_match in re.finditer(r':root\s*\{((?:[^{}]|\{[^{}]*\})*)\}', css_text, re.DOTALL):
        for prop_match in re.finditer(r'(--[\w-]+)\s*:\s*([^;]+);', root_match.group(1)):
            _ROOT_CSS_VARS[prop_match.group(1)] = prop_match.group(2).strip()

    def replace_var(match):
        var_name = match.group(1)
        fallback = match.group(2)
        return _ROOT_CSS_VARS.get(var_name, fallback or match.group(0))

    return re.sub(r'var\((--[\w-]+)(?:,\s*([^)]+))?\)', replace_var, css_text)


def _expand_background_shorthand(bg_value: str) -> Dict[str, str]:
    """Expand CSS `background` shorthand into backgroundColor / backgroundImage."""
    result = {}
    if 'url(' in bg_value:
        url_match = re.search(r'url\([^)]+\)', bg_value)
        if url_match:
            result['backgroundImage'] = url_match.group(0)
    if 'gradient' in bg_value:
        grad_match = re.search(r'(?:linear|radial|conic)-gradient\([^)]+\)', bg_value)
        if grad_match:
            result['backgroundImage'] = grad_match.group(0)
    stripped = re.sub(r'url\([^)]*\)', '', bg_value)
    stripped = re.sub(r'(?:linear|radial|conic)-gradient\([^)]*\)', '', stripped)
    stripped = stripped.strip()
    hex_match = re.search(r'#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b', stripped)
    if hex_match:
        result['backgroundColor'] = hex_match.group(0)
    else:
        rgba_match = re.search(r'rgba?\([^)]+\)', stripped)
        if rgba_match:
            result['backgroundColor'] = rgba_match.group(0)
    return result


def _kebab_to_camel(name: str) -> str:
    """Convert CSS kebab-case property name to camelCase."""
    parts = name.split('-')
    return parts[0] + ''.join(p.capitalize() for p in parts[1:])


def parse_css_rules(css_text: str) -> List[CSSRule]:
    """Parse CSS text into list of (selector, properties) rules.
    Property names are converted from kebab-case to camelCase."""
    global _ROOT_CSS_VARS
    _ROOT_CSS_VARS = {}
    css_text = re.sub(r'/\*.*?\*/', '', css_text, flags=re.DOTALL)
    css_text = _flatten_active_css(css_text, VIEWPORT_WIDTH_PX)
    css_text = resolve_css_variables(css_text)
    rules = []
    for block_match in re.finditer(r'([^{}]+)\{([^{}]+)\}', css_text):
        selector = block_match.group(1).strip()
        props_text = block_match.group(2).strip()
        if not selector or selector.startswith('@'):
            continue
        props = {}
        for prop_match in re.finditer(r'([\w-]+)\s*:\s*([^;]+);?', props_text):
            prop_name = _kebab_to_camel(prop_match.group(1).strip())
            props[prop_name] = prop_match.group(2).replace('!important', '').strip()
        if 'background' in props and 'backgroundColor' not in props:
            expanded = _expand_background_shorthand(props['background'])
            props.update(expanded)
        if 'border' in props:
            bv = props['border']
            if bv and 'none' not in bv and bv != '0px' and bv != '0':
                for side in ('borderLeft', 'borderRight', 'borderTop', 'borderBottom'):
                    if side not in props:
                        props[side] = bv
        for sel in selector.split(','):
            sel = sel.strip()
            if sel and not sel.startswith('@'):
                rules.append(CSSRule(selector=sel, properties=props))
    return rules


def selector_matches(element: Tag, selector: str) -> bool:
    """Check if a CSS selector matches a bs4 element."""
    if not selector or not element.name:
        return False
    if '::' in selector:
        return False
    parts = [p.strip() for p in selector.split() if p.strip()]
    if not parts:
        return False
    if len(parts) == 1:
        return _match_simple_selector(element, parts[0])
    # Descendant selector: check if last part matches element
    # and earlier parts match some ancestor chain
    return _match_descendant_selector(element, parts)


def _match_descendant_selector(element: Tag, parts: List[str]) -> bool:
    """Match a descendant selector like '.card h3' or 'h1 .accent'."""
    if not _match_simple_selector(element, parts[-1]):
        return False
    # Walk up the ancestor chain looking for parts[-2], parts[-3], etc.
    remaining = list(reversed(parts[:-1]))
    ancestor = element.parent
    while ancestor and remaining:
        if _match_simple_selector(ancestor, remaining[0]):
            remaining.pop(0)
        ancestor = ancestor.parent
    return len(remaining) == 0


def _match_simple_selector(element: Tag, selector: str) -> bool:
    """Match a single (non-combinator) CSS selector."""
    if not selector:
        return False
    if selector == '*':
        return True
    # Strip pseudo-classes/elements but track them for special handling
    pseudo_match = re.search(r'::?([\w-]+)(\([^)]*\))?$', selector)
    pseudo_name = pseudo_match.group(1) if pseudo_match else None
    sel_base = re.sub(r'::?[\w-]+(\([^)]*\))?$', '', selector)
    if not sel_base:
        sel_base = element.name or ''

    # Ignore dynamic interaction pseudo-classes entirely. Export should capture
    # authored resting state, not hover/focus/active variants.
    if pseudo_name in {
        'hover', 'active', 'focus', 'focus-visible', 'focus-within',
        'visited', 'link', 'target', 'checked', 'disabled', 'enabled',
    }:
        return False

    # Handle a small safe subset of structural pseudo-classes.
    if pseudo_name == 'root':
        return element.parent is None or getattr(element.parent, 'name', None) == '[document]'
    if pseudo_name == 'first-child':
        siblings = [s for s in (list(element.parent.children) if element.parent else []) if isinstance(s, Tag)]
        if siblings and siblings[0] is not element:
            return False
    elif pseudo_name == 'only-child':
        siblings = [s for s in (list(element.parent.children) if element.parent else []) if isinstance(s, Tag)]
        if len(siblings) != 1 or siblings[0] is not element:
            return False
    # Handle pseudo-class :last-child
    elif pseudo_name == 'last-child':
        siblings = list(element.parent.children) if element.parent else []
        tag_siblings = [s for s in siblings if isinstance(s, Tag) and s.name == element.name]
        if tag_siblings and tag_siblings[-1] is not element:
            return False
    elif pseudo_name:
        return False

    tag_name = element.name or ''
    id_match = re.match(r'^#([\w-]+)$', sel_base)
    if id_match:
        return element.get('id') == id_match.group(1)
    class_match = re.match(r'^\.([\w-]+)$', sel_base)
    if class_match:
        classes = element.get('class', [])
        if isinstance(classes, str):
            classes = classes.split()
        return class_match.group(1) in classes
    elem_class_match = re.match(r'^([\w-]+)\.([\w-]+)$', sel_base)
    if elem_class_match:
        tag_ok = elem_class_match.group(1).lower() == tag_name.lower()
        classes = element.get('class', [])
        if isinstance(classes, str):
            classes = classes.split()
        return tag_ok and elem_class_match.group(2) in classes
    # Handle compound class selectors like .slide.chapter
    compound_class_match = re.match(r'^\.([\w-]+)\.([\w-]+)(?:\.([\w-]+))?$', sel_base)
    if compound_class_match:
        classes = element.get('class', [])
        if isinstance(classes, str):
            classes = classes.split()
        required_classes = [compound_class_match.group(i) for i in range(1, 4) if compound_class_match.group(i)]
        return all(rc in classes for rc in required_classes)
    elem_id_match = re.match(r'^([\w-]+)#([\w-]+)$', sel_base)
    if elem_id_match:
        return (elem_id_match.group(1).lower() == tag_name.lower() and
                element.get('id') == elem_id_match.group(2))
    return sel_base.lower() == tag_name.lower()


def compute_element_style(
    element: Tag,
    css_rules: List[CSSRule],
    inline_style_str: Optional[str] = None,
    parent_style: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """Compute effective CSS style for an element via cascade."""
    computed = {}
    if parent_style:
        for prop in ('color', 'fontFamily', 'fontSize', 'fontWeight', 'lineHeight', 'textAlign'):
            if prop in parent_style:
                computed[prop] = parent_style[prop]
    for rule in css_rules:
        if selector_matches(element, rule.selector):
            # Convert CSS rule properties from kebab-case to camelCase
            for prop, val in rule.properties.items():
                computed[_kebab_to_camel(prop)] = val
    if inline_style_str:
        # Resolve CSS variables in inline style values
        resolved_inline = resolve_css_variables_inline(inline_style_str)
        for prop_match in re.finditer(r'([\w-]+)\s*:\s*([^;]+);?', resolved_inline):
            prop_name = _kebab_to_camel(prop_match.group(1).strip())
            computed[prop_name] = prop_match.group(2).strip()
    # Expand padding shorthand (padding: X Y → paddingTop/Left/etc)
    _expand_padding(computed)
    # Expand margin shorthand (margin: X Y → marginTop/Bottom/etc) for layout
    _expand_margin(computed)
    # Expand background shorthand (background: linear-gradient(...) → backgroundImage)
    _expand_background_shorthand_inplace(computed)
    return computed


def compute_inherited_style(
    element: Tag,
    css_rules: List[CSSRule],
    parent_style: Optional[Dict[str, str]] = None,
) -> Dict[str, str]:
    """Compute style with ancestor text inheritance applied explicitly."""
    inherited = dict(parent_style or {})
    ancestors = [p for p in element.parents if isinstance(p, Tag)]
    for ancestor in reversed(ancestors):
        inherited = compute_element_style(ancestor, css_rules, ancestor.get('style', ''), inherited)
    return compute_element_style(element, css_rules, element.get('style', ''), inherited)


def _expand_background_shorthand_inplace(computed: Dict[str, str]) -> None:
    """Expand CSS background shorthand into backgroundImage/backgroundColor if needed."""
    bg = computed.get('background', '')
    if not bg:
        return
    if 'gradient' in bg or 'url(' in bg:
        expanded = _expand_background_shorthand(bg)
        for key, val in expanded.items():
            computed.setdefault(key, val)
    elif bg not in ('transparent', 'rgba(0, 0, 0, 0)', 'none', ''):
        # Solid color background shorthand (e.g., background:rgba(15,23,42,0.08))
        # → set backgroundColor so downstream checks detect it
        computed.setdefault('backgroundColor', bg)


def resolve_css_variables_inline(css_value: str) -> str:
    """Resolve var() references in a CSS value string using global root vars."""
    def replace_var(match):
        var_name = match.group(1)
        fallback = match.group(2)
        return _ROOT_CSS_VARS.get(var_name, fallback or match.group(0))
    return re.sub(r'var\((--[\w-]+)(?:,\s*([^)]+))?\)', replace_var, css_value)


def _expand_margin(computed: Dict[str, str]) -> None:
    """Expand margin shorthand in-place for layout calculations."""
    if 'margin' not in computed:
        return
    vals = _split_css_values(computed['margin'])
    # Accept px values, clamp(), auto, 0, and negative values
    px = [v for v in vals if 'px' in v or v.startswith('clamp(') or v == 'auto' or v == '0' or (v.startswith('-') and 'px' in v)]
    if len(px) == 1:
        for key in ('marginTop', 'marginRight', 'marginBottom', 'marginLeft'):
            if key not in computed:
                computed[key] = px[0]
    elif len(px) == 2:
        if 'marginTop' not in computed:
            computed['marginTop'] = computed['marginBottom'] = px[0]
        if 'marginLeft' not in computed:
            computed['marginLeft'] = computed['marginRight'] = px[1]
    elif len(px) == 3:
        if 'marginTop' not in computed:
            computed['marginTop'] = px[0]
        if 'marginLeft' not in computed:
            computed['marginLeft'] = computed['marginRight'] = px[1]
        if 'marginBottom' not in computed:
            computed['marginBottom'] = px[2]
    elif len(px) == 4:
        if 'marginTop' not in computed:
            computed['marginTop'] = px[0]
        if 'marginRight' not in computed:
            computed['marginRight'] = px[1]
        if 'marginBottom' not in computed:
            computed['marginBottom'] = px[2]
        if 'marginLeft' not in computed:
            computed['marginLeft'] = px[3]
    # Remove the shorthand to prevent re-expansion
    del computed['margin']


def _split_css_values(css_value: str) -> List[str]:
    """Split a CSS multi-value property respecting parentheses (for clamp(), etc.)."""
    parts = []
    current = []
    depth = 0
    for ch in css_value:
        if ch == '(':
            depth += 1
            current.append(ch)
        elif ch == ')':
            depth -= 1
            current.append(ch)
        elif ch == ' ' and depth == 0:
            if current:
                parts.append(''.join(current))
                current = []
        else:
            current.append(ch)
    if current:
        parts.append(''.join(current))
    return parts


def _expand_padding(computed: Dict[str, str]) -> None:
    """Expand padding shorthand in-place. Used only for pill/badge shape width calculation."""
    if 'padding' not in computed:
        return
    vals = _split_css_values(computed['padding'])
    px = [v for v in vals if 'px' in v or v.startswith('clamp(')]
    if len(px) == 1:
        computed['paddingTop'] = computed['paddingRight'] = computed['paddingBottom'] = computed['paddingLeft'] = px[0]
    elif len(px) == 2:
        computed['paddingTop'] = computed['paddingBottom'] = px[0]
        computed['paddingLeft'] = computed['paddingRight'] = px[1]
    elif len(px) == 3:
        computed['paddingTop'] = px[0]
        computed['paddingLeft'] = computed['paddingRight'] = px[1]
        computed['paddingBottom'] = px[2]
    elif len(px) == 4:
        computed['paddingTop'] = px[0]
        computed['paddingRight'] = px[1]
        computed['paddingBottom'] = px[2]
        computed['paddingLeft'] = px[3]


# ─── Color Parsing ────────────────────────────────────────────────────────────

def parse_color(css_color: str, bg: Tuple[int, int, int] = (255, 255, 255)) -> Optional[Tuple[int, int, int]]:
    """Parse a CSS color string, blending rgba() alpha over the given bg color."""
    if not css_color or css_color in ('transparent',) or 'rgba(0, 0, 0, 0)' in css_color:
        return None
    m = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)', css_color)
    if m:
        r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        a = float(m.group(4)) if m.group(4) else 1.0
        if a <= 0:
            return None
        if a < 1.0:
            r = int(a * r + (1 - a) * bg[0])
            g = int(a * g + (1 - a) * bg[1])
            b = int(a * b + (1 - a) * bg[2])
        return (r, g, b)
    m = re.search(r'#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})', css_color)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = ''.join([c*2 for c in h])
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    return None


def _parse_rgba_color(css_color: str) -> Optional[Tuple[int, int, int, float]]:
    """Parse CSS color into RGBA without compositing alpha onto a background."""
    if not css_color or css_color in ('transparent',) or 'rgba(0, 0, 0, 0)' in css_color:
        return None
    token = css_color.strip()
    if token.startswith('var('):
        var_match = re.match(r'var\((--[^),]+)', token)
        if not var_match:
            return None
        token = (_ROOT_CSS_VARS.get(var_match.group(1), '') or '').strip()
        if not token:
            return None
    m = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)', token)
    if m:
        r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        a = float(m.group(4)) if m.group(4) else 1.0
        if a <= 0:
            return None
        return (r, g, b, max(0.0, min(a, 1.0)))
    rgb = parse_color(token)
    if rgb:
        return (*rgb, 1.0)
    return None


def px_to_pt(px_value: str) -> float:
    """Convert a CSS length value to points (1pt = 1/72in, 1px ≈ 0.75pt at 96 DPI)."""
    px_value = str(px_value)
    # Handle CSS math expressions
    if px_value.strip().startswith(('clamp(', 'min(', 'max(')):
        resolved_px = _resolve_css_length(px_value)
        if resolved_px > 0:
            return round(resolved_px * 0.75, 1)
        return 12.0
    m = re.search(r'([\d.]+)px', px_value)
    if m:
        return round(float(m.group(1)) * 0.75, 1)
    # Handle rem/em values
    m = re.search(r'([\d.]+)rem', px_value)
    if m:
        return round(float(m.group(1)) * 16.0 * 0.75, 1)
    m = re.search(r'([\d.]+)em', px_value)
    if m:
        return round(float(m.group(1)) * 16.0 * 0.75, 1)
    return 12.0


# Viewport dimensions for resolving CSS clamp() expressions and media queries.
VIEWPORT_WIDTH_PX = 1440.0
VIEWPORT_HEIGHT_PX = 900.0


def _candidate_repo_roots(
    script_file: Optional[str] = None,
    cwd: Optional[Path] = None,
    env: Optional[Dict[str, str]] = None,
) -> List[Path]:
    """Yield plausible repo roots for inline-executed and file-based runtimes."""
    env = env or os.environ
    candidates: List[Path] = []

    def _add(path: Optional[Path]) -> None:
        if not path:
            return
        try:
            candidates.append(path.expanduser().resolve())
        except Exception:
            return

    if script_file:
        script_path = Path(script_file)
        _add(script_path.parent.parent)
        _add(script_path.parent)

    for env_key in ('KAI_EXPORT_PPT_LITE_ROOT', 'CLAUDE_SKILL_DIR', 'CODEX_SKILL_DIR'):
        raw = env.get(env_key)
        if not raw:
            continue
        env_path = Path(raw)
        _add(env_path)
        _add(env_path.parent)
        _add(env_path.parent.parent)

    cwd_path = Path(cwd or Path.cwd())
    _add(cwd_path)
    for parent in cwd_path.parents:
        _add(parent)

    # Hosted sandboxes commonly install skills under /home/user/skills/<name>.
    _add(Path.home() / 'skills' / 'kai-export-ppt-lite')
    _add(Path('/home/user/skills/kai-export-ppt-lite'))

    return candidates


def _looks_like_repo_root(path: Path) -> bool:
    return (
        (path / 'scripts' / 'export-sandbox-pptx.py').exists() or
        (path / 'contracts' / 'export_hints.schema.json').exists() or
        (path / 'contracts' / 'slide_creator' / 'manifest.json').exists()
    )


def _resolve_repo_root(
    script_file: Optional[str] = None,
    cwd: Optional[Path] = None,
    env: Optional[Dict[str, str]] = None,
) -> Path:
    """Resolve the repo root without assuming __file__ exists.

    Some hosted sandboxes execute skill code via exec()/notebook cells, so the
    module-level __file__ global is absent. In that case we probe likely skill
    install locations and gracefully fall back to the working directory.
    """
    fallback = Path(cwd or Path.cwd()).expanduser().resolve()
    seen: Set[Path] = set()
    for candidate in _candidate_repo_roots(script_file, cwd, env):
        if candidate in seen:
            continue
        seen.add(candidate)
        if _looks_like_repo_root(candidate):
            return candidate
    return fallback


REPO_ROOT = _resolve_repo_root(globals().get('__file__'))
CONTRACTS_ROOT = REPO_ROOT / 'contracts'
SLIDE_CREATOR_RUNTIME_CHROME_SELECTORS = [
    '.progress-bar',
    '.nav-dots',
    '.edit-hotzone',
    '.edit-toggle',
    '#notes-panel',
    '#present-btn',
    '#present-counter',
]
EXPORT_HINTS_SCHEMA_PATH = CONTRACTS_ROOT / 'export_hints.schema.json'


def resolve_clamp(clamp_str: str) -> float:
    """Resolve a CSS clamp(min, preferred, max) expression to pixels."""
    m = re.match(r'clamp\s*\(\s*(.+?)\s*,\s*(.+?)\s*,\s*(.+?)\s*\)', clamp_str.strip())
    if not m:
        # Try clamp(min, max) with two args
        m = re.match(r'clamp\s*\(\s*(.+?)\s*,\s*(.+?)\s*\)', clamp_str.strip())
        if not m:
            return 0.0
        return _resolve_css_length(m.group(1))
    min_val = _resolve_css_length(m.group(1))
    preferred = _resolve_css_length(m.group(2))
    max_val = _resolve_css_length(m.group(3))
    return min(max(min_val, preferred), max_val)


def _split_css_function_args(args_str: str) -> List[str]:
    """Split CSS function args on commas while respecting nested parentheses."""
    parts = []
    current = []
    depth = 0
    for ch in args_str:
        if ch == '(':
            depth += 1
            current.append(ch)
        elif ch == ')':
            depth = max(depth - 1, 0)
            current.append(ch)
        elif ch == ',' and depth == 0:
            part = ''.join(current).strip()
            if part:
                parts.append(part)
            current = []
        else:
            current.append(ch)
    tail = ''.join(current).strip()
    if tail:
        parts.append(tail)
    return parts


def resolve_minmax(math_str: str) -> float:
    """Resolve CSS min()/max() expressions to pixels."""
    m = re.match(r'^(min|max)\s*\((.*)\)\s*$', math_str.strip())
    if not m:
        return 0.0
    op = m.group(1)
    args = _split_css_function_args(m.group(2))
    if not args:
        return 0.0
    values = [_resolve_css_length(arg) for arg in args]
    values = [v for v in values if v > 0]
    if not values:
        return 0.0
    return min(values) if op == 'min' else max(values)


def _resolve_css_length(val_str: str) -> float:
    """Convert a CSS length value to pixels."""
    val_str = val_str.strip()
    if val_str.startswith('clamp('):
        return resolve_clamp(val_str)
    if val_str.startswith('min(') or val_str.startswith('max('):
        return resolve_minmax(val_str)
    m = re.match(r'^([\d.]+)px$', val_str)
    if m:
        return float(m.group(1))
    m = re.match(r'^([\d.]+)rem$', val_str)
    if m:
        return float(m.group(1)) * 16.0  # 1rem = 16px
    m = re.match(r'^([\d.]+)em$', val_str)
    if m:
        return float(m.group(1)) * 16.0
    m = re.match(r'^([\d.]+)vw$', val_str)
    if m:
        return float(m.group(1)) / 100.0 * VIEWPORT_WIDTH_PX
    m = re.match(r'^([\d.]+)vh$', val_str)
    if m:
        return float(m.group(1)) / 100.0 * VIEWPORT_HEIGHT_PX
    m = re.match(r'^([\d.]+)vmin$', val_str)
    if m:
        return float(m.group(1)) / 100.0 * min(VIEWPORT_WIDTH_PX, VIEWPORT_HEIGHT_PX)
    m = re.match(r'^([\d.]+)(?:in)$', val_str)
    if m:
        return float(m.group(1)) * 96.0
    m = re.match(r'^([\d.]+)cm$', val_str)
    if m:
        return float(m.group(1)) * 96.0 / 2.54
    m = re.match(r'^([\d.]+)mm$', val_str)
    if m:
        return float(m.group(1)) * 96.0 / 25.4
    m = re.match(r'^([\d.]+)$', val_str)
    if m:
        return float(m.group(1))  # bare number treated as px
    return 0.0


def parse_px(val: str) -> float:
    """Parse a CSS length value to a raw number (for legacy callers expecting pixel-like values)."""
    if not val or val in ('0px', '0', 'auto', 'none', 'normal', ''):
        return 0.0
    # Handle CSS math expressions
    if val.strip().startswith(('clamp(', 'min(', 'max(')):
        resolved = _resolve_css_length(val)
        if resolved > 0:
            return resolved
    # Try to parse with unit support
    val = val.strip()
    m = re.match(r'^(-?[\d.]+)rem$', val)
    if m:
        return float(m.group(1)) * 16.0
    m = re.match(r'^(-?[\d.]+)em$', val)
    if m:
        return float(m.group(1)) * 16.0
    m = re.match(r'^(-?[\d.]+)vw$', val)
    if m:
        return float(m.group(1)) * 14.4  # 1vw = 14.4px at 1440px viewport
    m = re.match(r'^(-?[\d.]+)vh$', val)
    if m:
        return float(m.group(1)) * 9.0  # 1vh = 9.0px at 900px viewport
    m = re.match(r'^(-?[\d.]+)vmin$', val)
    if m:
        return float(m.group(1)) * min(VIEWPORT_WIDTH_PX, VIEWPORT_HEIGHT_PX) / 100.0
    m = re.match(r'^(-?[\d.]+)px$', val)
    if m:
        return float(m.group(1))
    m = re.search(r'(-?[\d.]+)', str(val))
    return float(m.group(1)) if m else 0.0


def _default_normal_line_height_multiple(tag: str) -> float:
    """Approximate browser defaults for `line-height: normal` by semantic text role."""
    tag = (tag or '').lower()
    if tag == 'h1':
        return 1.10
    if tag in ('h2', 'h3', 'h4', 'h5', 'h6'):
        return 1.18
    if tag in ('span', 'a', 'small', 'code', 'kbd', 'mark'):
        return 1.12
    return 1.20


# ─── Producer Detection / Hints / Contracts ─────────────────────────────────

def _read_json_file(path: Path) -> Optional[Dict[str, Any]]:
    if not path or not path.exists():
        return None
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return None


def load_export_hints_schema() -> Dict[str, Any]:
    schema = _read_json_file(EXPORT_HINTS_SCHEMA_PATH)
    if schema:
        return schema
    return {
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'producer': {'type': 'string'},
            'producer_confidence': {'type': 'string'},
            'preset': {'type': 'string'},
            'deck_family': {'type': 'string'},
            'runtime_flags': {'type': 'object'},
            'chrome_selectors': {'type': 'array'},
            'semantic_bias': {'type': 'object'},
            'contract_ref': {'type': 'string'},
        },
    }


def validate_export_hints(raw: Any) -> Optional[Dict[str, Any]]:
    if not isinstance(raw, dict):
        return None

    schema = load_export_hints_schema()
    allowed = set(schema.get('properties', {}).keys())
    if any(key not in allowed for key in raw.keys()):
        return None

    sanitized: Dict[str, Any] = {}
    for key in ('producer', 'producer_confidence', 'preset', 'deck_family', 'contract_ref'):
        value = raw.get(key)
        if value is None:
            continue
        if not isinstance(value, str):
            return None
        sanitized[key] = value.strip()

    runtime_flags = raw.get('runtime_flags')
    if runtime_flags is not None:
        if not isinstance(runtime_flags, dict):
            return None
        sanitized['runtime_flags'] = {
            str(k): bool(v) for k, v in runtime_flags.items()
        }

    chrome_selectors = raw.get('chrome_selectors')
    if chrome_selectors is not None:
        if not isinstance(chrome_selectors, list) or not all(isinstance(v, str) for v in chrome_selectors):
            return None
        sanitized['chrome_selectors'] = [v for v in (s.strip() for s in chrome_selectors) if v]

    semantic_bias = raw.get('semantic_bias')
    if semantic_bias is not None:
        if not isinstance(semantic_bias, dict):
            return None
        bias: Dict[str, Any] = {}
        for key, value in semantic_bias.items():
            if key == 'layout_family' and isinstance(value, str):
                bias[key] = value.strip()
            elif key == 'decorative_layers' and isinstance(value, list) and all(isinstance(v, str) for v in value):
                bias[key] = [v.strip() for v in value if v.strip()]
            elif key == 'text_expectations' and isinstance(value, dict):
                bias[key] = {str(k): bool(v) for k, v in value.items()}
        sanitized['semantic_bias'] = bias

    return sanitized


def _normalize_preset_slug(preset: str) -> str:
    slug = re.sub(r'[^a-z0-9]+', '-', (preset or '').strip().lower())
    return slug.strip('-')


def _load_embedded_export_hints(soup: BeautifulSoup) -> Optional[Dict[str, Any]]:
    node = soup.find('script', attrs={'id': 'kai-export-hints', 'type': 'application/json'})
    if not node:
        return None
    try:
        raw = json.loads(node.string or node.get_text() or '{}')
    except Exception:
        return None
    return validate_export_hints(raw)


def _load_sidecar_export_hints(html_path: Path) -> Optional[Dict[str, Any]]:
    sidecar = html_path.parent / 'deck.export-hints.json'
    return validate_export_hints(_read_json_file(sidecar))


def _has_structured_watermark(soup: BeautifulSoup) -> bool:
    semver_pattern = re.compile(r'^kai-slide-creator@\d+\.\d+\.\d+$')
    for node in soup.find_all(attrs={'data-watermark': True}):
        if node.has_attr('hidden') and semver_pattern.match((node.get('data-watermark') or '').strip()):
            return True
    for node in soup.find_all(True):
        if not node.has_attr('hidden'):
            continue
        text = node.get_text(strip=True)
        if semver_pattern.match(text):
            return True
    return False


def _has_slide_creator_runtime_structure(soup: BeautifulSoup) -> bool:
    body = soup.find('body')
    if not body:
        return False
    if body.get('data-preset') and soup.select_one('.progress-bar') and soup.select_one('.nav-dots'):
        return True
    if soup.select_one('#notes-panel') and soup.select_one('.edit-toggle'):
        return True
    return False


def detect_producer(
    soup: BeautifulSoup,
    html_path: Path,
    embedded_hints: Optional[Dict[str, Any]] = None,
    sidecar_hints: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    body = soup.find('body')
    meta_generator = soup.find('meta', attrs={'name': 'generator'})

    strong = []
    medium_channels = set()
    weak = []

    producer = None

    if embedded_hints and embedded_hints.get('producer'):
        strong.append('embedded-hints')
        producer = embedded_hints['producer']

    if sidecar_hints and sidecar_hints.get('producer'):
        strong.append('sidecar-hints')
        producer = sidecar_hints['producer']

    generator_text = (meta_generator.get('content', '') if meta_generator else '').strip().lower()
    body_producer = (body.get('data-producer', '') if body else '').strip().lower()
    if 'kai-slide-creator' in generator_text or body_producer == 'kai-slide-creator':
        medium_channels.add('metadata')
        producer = producer or 'slide-creator'

    if _has_structured_watermark(soup):
        medium_channels.add('watermark')
        producer = producer or 'slide-creator'

    if body and body.get('data-preset'):
        weak.append('body-data-preset')
        producer = producer or 'slide-creator'

    if body and body.get('data-export-progress') is not None:
        weak.append('body-data-export-progress')
        producer = producer or 'slide-creator'

    if _has_slide_creator_runtime_structure(soup):
        weak.append('runtime-structure')
        producer = producer or 'slide-creator'

    if strong or len(medium_channels) >= 2:
        confidence = 'high'
    elif len(medium_channels) == 1:
        confidence = 'medium'
    elif weak:
        confidence = 'low'
    else:
        confidence = 'none'

    return {
        'producer': producer,
        'confidence': confidence,
        'strong_signals': strong,
        'medium_channels': sorted(medium_channels),
        'weak_signals': weak,
    }


class ProducerAdapter(Protocol):
    name: str

    def detect(self, soup: BeautifulSoup, detection: Dict[str, Any]) -> bool: ...
    def collect_hints(self, soup: BeautifulSoup, detection: Dict[str, Any], sidecar: Optional[Dict[str, Any]] = None) -> Dict[str, Any]: ...
    def resolve_contract(self, hints: Dict[str, Any]) -> Optional[Dict[str, Any]]: ...
    def validate(self, hints: Dict[str, Any], contract: Optional[Dict[str, Any]]) -> Dict[str, Any]: ...


def _load_contract_by_preset(producer: str, preset: str) -> Optional[Dict[str, Any]]:
    if producer != 'slide-creator' or not preset:
        return None
    contract_path = CONTRACTS_ROOT / 'slide_creator' / 'presets' / f'{_normalize_preset_slug(preset)}.json'
    return _read_json_file(contract_path)


def _resolve_contract_from_ref(contract_ref: str) -> Optional[Tuple[str, str]]:
    if not contract_ref or '@' not in contract_ref:
        return None
    contract_id, contract_version = contract_ref.rsplit('@', 1)
    if not contract_id or not contract_version:
        return None
    return contract_id, contract_version


class SlideCreatorAdapter:
    name = 'slide-creator'

    def detect(self, soup: BeautifulSoup, detection: Dict[str, Any]) -> bool:
        return detection.get('producer') == 'slide-creator'

    def collect_hints(
        self,
        soup: BeautifulSoup,
        detection: Dict[str, Any],
        sidecar: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        body = soup.find('body')
        hints = dict(sidecar or {})
        hints['producer'] = 'slide-creator'
        hints['producer_confidence'] = detection.get('confidence', 'low')

        if body and body.get('data-preset') and not hints.get('preset'):
            hints['preset'] = body.get('data-preset').strip()

        if body and hints.get('preset') and not hints.get('deck_family'):
            hints['deck_family'] = _normalize_preset_slug(hints['preset'])

        runtime_flags = dict(hints.get('runtime_flags') or {})
        if body and body.get('data-export-progress') is not None:
            runtime_flags['export_progress_ui'] = body.get('data-export-progress') == 'true'
        if runtime_flags:
            hints['runtime_flags'] = runtime_flags

        if not hints.get('chrome_selectors'):
            hints['chrome_selectors'] = list(SLIDE_CREATOR_RUNTIME_CHROME_SELECTORS)

        contract = self.resolve_contract(hints)
        if contract:
            hints.setdefault('semantic_bias', {})
            if contract.get('family'):
                hints['semantic_bias'].setdefault('layout_family', contract['family'])
            decorative = [layer.get('kind') for layer in contract.get('decorative_layers', []) if layer.get('kind')]
            if decorative:
                hints['semantic_bias'].setdefault('decorative_layers', decorative)
            if contract.get('text_expectations'):
                hints['semantic_bias'].setdefault('text_expectations', contract['text_expectations'])
            if contract.get('runtime_chrome_selectors') and not hints.get('chrome_selectors'):
                hints['chrome_selectors'] = list(contract['runtime_chrome_selectors'])
            hints.setdefault('contract_ref', f"{contract.get('contract_id', 'slide-creator/' + _normalize_preset_slug(hints.get('preset', 'unknown')))}@{contract.get('contract_version', '1.0.0')}")

        return validate_export_hints(hints) or {}

    def resolve_contract(self, hints: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        contract_ref = hints.get('contract_ref', '')
        if contract_ref:
            resolved = _resolve_contract_from_ref(contract_ref)
            if resolved:
                contract_id, contract_version = resolved
                producer, _, preset_slug = contract_id.partition('/')
                if producer == 'slide-creator' and preset_slug:
                    contract = _read_json_file(CONTRACTS_ROOT / 'slide_creator' / 'presets' / f'{preset_slug}.json')
                    if contract and contract.get('contract_version') == contract_version:
                        return contract
        return _load_contract_by_preset(hints.get('producer', ''), hints.get('preset', ''))

    def validate(self, hints: Dict[str, Any], contract: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        result = {'ok': True, 'contract_found': bool(contract), 'contract_version_match': True}
        contract_ref = hints.get('contract_ref', '')
        if contract and contract_ref:
            resolved = _resolve_contract_from_ref(contract_ref)
            if resolved:
                _, expected_version = resolved
                result['contract_version_match'] = expected_version == contract.get('contract_version')
                if not result['contract_version_match']:
                    result['ok'] = False
        return result


def collect_export_context(html_path: Path, soup: BeautifulSoup) -> Dict[str, Any]:
    embedded_hints = _load_embedded_export_hints(soup)
    sidecar_hints = _load_sidecar_export_hints(html_path)
    detection = detect_producer(soup, html_path, embedded_hints, sidecar_hints)

    adapter: Optional[ProducerAdapter] = None
    hints: Dict[str, Any] = embedded_hints or sidecar_hints or {}
    contract = None
    validation = {'ok': True, 'contract_found': False, 'contract_version_match': True}

    if detection.get('producer') == 'slide-creator':
        adapter = SlideCreatorAdapter()
        if adapter.detect(soup, detection):
            hints = adapter.collect_hints(soup, detection, embedded_hints or sidecar_hints)
            contract = adapter.resolve_contract(hints)
            validation = adapter.validate(hints, contract)

    return {
        'detection': detection,
        'adapter': adapter.name if adapter else None,
        'hints': hints,
        'contract': contract,
        'validation': validation,
    }


def _prune_runtime_chrome(soup: BeautifulSoup, selectors: List[str]) -> None:
    seen = set()
    for selector in selectors or []:
        try:
            for node in soup.select(selector):
                node_id = id(node)
                if node_id in seen:
                    continue
                seen.add(node_id)
                node.decompose()
        except Exception:
            continue


def _default_text_color(fallback: str = '') -> str:
    """Resolve a stable default text color when CSS leaves it implicit."""
    if fallback and fallback not in ('transparent', 'rgba(0, 0, 0, 0)'):
        return fallback
    root_primary = _ROOT_CSS_VARS.get('--text-primary', '')
    if root_primary:
        return root_primary
    return '#000000'


def _normalize_ink_color(color_str: str) -> str:
    """Snap deep slate ink to true black for more stable native PPT output."""
    if not color_str:
        return color_str
    rgb = parse_color(color_str)
    if not rgb:
        return color_str
    if rgb == (15, 23, 42):
        return '#000000'
    return color_str


def _extract_gradient_colors(bg_image: str) -> List[str]:
    """Extract gradient color stops from a CSS background-image value."""
    if not bg_image or 'gradient' not in bg_image:
        return []
    colors: List[str] = []
    for rgba in re.findall(r'rgba?\([^)]+\)', bg_image):
        colors.append(rgba)
    for hex_color in re.findall(r'#(?:[0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b', bg_image):
        colors.append(hex_color)
    # Preserve order but dedupe exact repeats.
    deduped: List[str] = []
    seen = set()
    for color in colors:
        if color in seen:
            continue
        deduped.append(color)
        seen.add(color)
    return deduped


def _is_gradient_text_style(style: Dict[str, str]) -> bool:
    bi = style.get('backgroundImage', '')
    bc = (style.get('webkitBackgroundClip', '') or
          style.get('WebkitBackgroundClip', '') or
          style.get('backgroundClip', ''))
    text_fill = (style.get('webkitTextFillColor', '') or
                 style.get('WebkitTextFillColor', '') or
                 style.get('textFillColor', ''))
    return 'gradient' in bi and bc == 'text' and bool(text_fill)


def _uses_monospace_font(font_family: str) -> bool:
    return bool(re.search(r'mono|code|courier|consolas|menlo|fira code|sf mono', font_family or '', re.I))


def _resolve_letter_spacing_px(letter_spacing: str, font_px: float = 16.0) -> float:
    """Resolve CSS letter-spacing into pixels, honoring relative em/rem units."""
    if not letter_spacing or letter_spacing in ('normal', '0', '0px', '0em', '0rem'):
        return 0.0
    value = str(letter_spacing).strip()
    m = re.match(r'^(-?[\d.]+)em$', value)
    if m:
        return float(m.group(1)) * font_px
    m = re.match(r'^(-?[\d.]+)rem$', value)
    if m:
        return float(m.group(1)) * 16.0
    return parse_px(value)


def _estimate_text_width_px(
    text: str,
    font_px: float,
    *,
    monospace: bool = False,
    letter_spacing: str = '',
) -> float:
    """Estimate text width with special handling for code/kbd monospace boxes."""
    if not text:
        return 0.0
    cjk = sum(1 for c in text if ord(c) > 127)
    latin = len(text) - cjk
    latin_factor = 0.64 if monospace else 0.55
    width_px = cjk * font_px + latin * font_px * latin_factor
    ls_px = _resolve_letter_spacing_px(letter_spacing, font_px)
    if ls_px != 0 and len(text) > 1:
        width_px += ls_px * (len(text) - 1)
    return width_px


def _estimate_compact_label_width_px(
    text: str,
    font_px: float,
    *,
    letter_spacing: str = '',
) -> float:
    """Estimate short Latin UI-label width more tightly than body-copy text.

    Browser-rendered pills/tag rails in presets like Enterprise Dark use
    proportional UI fonts where a flat 0.55em-per-Latin heuristic is too wide.
    This helper keeps the logic generic by only targeting short, non-CJK,
    non-monospace labels with visible inline box styling.
    """
    if not text:
        return 0.0

    width_px = 0.0
    for ch in text:
        if has_cjk(ch):
            width_px += font_px
            continue
        if ch.isspace():
            factor = 0.24
        elif ch in '.,:;!|/\\\'"`':
            factor = 0.18
        elif ch in '-_+=~':
            factor = 0.28
        elif ch in '&@#%':
            factor = 0.56
        elif ch in 'mwMWQG':
            factor = 0.58
        elif ch in 'iltIjfr':
            factor = 0.25
        elif ch.isupper():
            factor = 0.47
        elif ch.isdigit():
            factor = 0.40
        elif ord(ch) > 127:
            factor = 0.34
        else:
            factor = 0.38
        width_px += font_px * factor

    ls_px = _resolve_letter_spacing_px(letter_spacing, font_px)
    if ls_px != 0 and len(text) > 1:
        width_px += ls_px * (len(text) - 1)
    return width_px * 1.16


def _is_compact_ui_label(
    text: str,
    style: Dict[str, str],
    *,
    has_grouped_inline: bool = False,
    has_inline_boxes: bool = False,
    monospace_text: bool = False,
) -> bool:
    """Detect short rounded inline labels that should use compact width metrics."""
    if not text or '\n' in text:
        return False
    if monospace_text or has_grouped_inline or has_inline_boxes or has_cjk(text):
        return False
    if len(text.strip()) > 28:
        return False
    if parse_px(style.get('fontSize', '16px')) > 16.5:
        return False

    border_radius = style.get('borderRadius', '')
    pad_l = parse_px(style.get('paddingLeft', '0px'))
    pad_r = parse_px(style.get('paddingRight', '0px'))
    has_box = has_visible_bg_or_border(style)
    is_rounded = '999' in border_radius or '%' in border_radius or parse_px(border_radius) >= 10
    return has_box and is_rounded and (pad_l + pad_r) >= 16


def _sum_border_width_px(style: Dict[str, str], horizontal: bool = True) -> float:
    """Estimate total horizontal/vertical border width from CSS border declarations."""
    keys = ('borderLeft', 'borderRight') if horizontal else ('borderTop', 'borderBottom')
    total = 0.0
    for key in keys:
        border_val = style.get(key, '')
        if border_val and 'none' not in border_val and not border_val.startswith('0px'):
            total += parse_px(border_val.split()[0])
    if total == 0.0:
        border_val = style.get('border', '')
        if border_val and 'none' not in border_val and not border_val.startswith('0px'):
            border_px = parse_px(border_val.split()[0])
            total = border_px * 2
    return total


def has_cjk(text: str) -> bool:
    return bool(re.search(r'[\u2E80-\u9FFF\uF900-\uFAFF\uFE10-\uFE6F\uFF00-\uFFEF]', text))


def has_latin_word(text: str) -> bool:
    return bool(re.search(r'[A-Za-z0-9]', text or ''))


def is_bold(fw: str) -> bool:
    return fw in ('bold', '700', '800', '900') or (fw.isdigit() and int(fw) >= 600)


def is_condensed_font(family: str) -> bool:
    return bool(re.search(r'condensed|narrow|compressed', family or '', re.I))


def resolve_border_radius(style: Dict[str, str], width_px: float, height_px: float) -> float:
    """Convert CSS border-radius to px."""
    br = style.get('borderTopLeftRadius', style.get('borderRadius', ''))
    if not br or br == '0px':
        return 0.0
    if br.endswith('%'):
        pct = float(re.search(r'([\d.]+)', br).group(1))
        return pct / 100.0 * min(width_px, height_px)
    return parse_px(br)


def has_visible_bg_or_border(style: Dict[str, str]) -> bool:
    bg = style.get('backgroundColor', '')
    if bg and bg not in ('transparent', 'rgba(0, 0, 0, 0)', ''):
        return True
    for side in ('border', 'borderLeft', 'borderRight', 'borderTop', 'borderBottom'):
        bs = style.get(side, '')
        if bs and 'none' not in bs and not bs.startswith('0px') and bs != '0px':
            return True
    return False


def _should_create_bg_shape(style: Dict[str, str], has_gradient_bg: bool = False) -> bool:
    """Check if a shape should be created for this element's background.

    Returns False when the gradient is applied via background-clip:text —
    in that case the gradient colors the text itself, not a background shape.
    """
    # background-clip:text means the gradient paints on text, not on a shape
    # Note: kebab-to-camel makes -webkit-background-clip → WebkitBackgroundClip
    bg_clip = (style.get('webkitBackgroundClip', '') or
               style.get('WebkitBackgroundClip', '') or
               style.get('backgroundClip', ''))
    text_fill = (style.get('webkitTextFillColor', '') or
                 style.get('WebkitTextFillColor', '') or
                 style.get('textFillColor', ''))
    if bg_clip == 'text' and text_fill:
        return False
    return has_visible_bg_or_border(style) or has_gradient_bg


def _has_drawable_background(style: Dict[str, str]) -> bool:
    """True when an element paints a real background box instead of text-only fill."""
    bg_image = style.get('backgroundImage', 'none')
    has_gradient_bg = bg_image != 'none' and 'gradient' in bg_image
    return _should_create_bg_shape(style, has_gradient_bg)


def _preserves_stacked_child_structure(element: Tag, style: Dict[str, str]) -> bool:
    """Return True when a container's direct children carry semantic layout."""
    display = (style.get('display', '') or '').strip()
    flex_dir = (
        style.get('flexDirection', '') or
        style.get('flex-direction', '') or
        ''
    ).strip()
    if display not in ('flex', 'inline-flex') or flex_dir != 'column':
        return False

    direct_tags = [child for child in element.children if isinstance(child, Tag)]
    if len(direct_tags) < 2:
        return False

    # Column stacks like Aurora stats intentionally separate metric, label,
    # and supporting copy into distinct rows. Flattening them into one text box
    # destroys the hierarchy and breaks gradient/stat emphasis.
    meaningful_children = [
        child for child in direct_tags
        if child.name.lower() not in ('br',)
    ]
    return len(meaningful_children) >= 2


def is_leaf_text_container(element: Tag, css_rules: Optional[List] = None) -> bool:
    """Check if element's entire visible content is text (no block children)."""
    children = list(element.children)
    if len(children) == 0:
        return bool(get_text_content(element).strip())
    has_inline_with_bg = False
    rules = css_rules or []
    for child in children:
        if isinstance(child, NavigableString):
            continue
        if not isinstance(child, Tag):
            continue
        if child.name not in INLINE_TAGS:
            return False
        # If inline child has visible bg/border, it should be extracted separately
        if rules and has_visible_bg_or_border(compute_element_style(child, rules, child.get('style', ''))):
            has_inline_with_bg = True
    if rules:
        style = compute_element_style(element, rules, element.get('style', ''))
        if _preserves_stacked_child_structure(element, style):
            return False
    if has_inline_with_bg:
        return False  # Don't treat as leaf — recurse so each styled span gets its own shape
    return bool(get_text_content(element).strip())


def get_text_content(element: Tag, exclude_elements: set = None) -> str:
    """Get the text content of an element, converting <br> to newlines without modifying the tree."""
    if not element:
        return ''
    parts = []
    for child in element.descendants:
        if exclude_elements is not None:
            # Skip descendants of excluded elements
            if hasattr(child, 'parents') and any(p in exclude_elements for p in child.parents):
                continue
        if isinstance(child, NavigableString):
            text = str(child)
            # Trim leading/trailing whitespace from each text node
            # (removes HTML formatting indentation)
            stripped = text.strip()
            if stripped:
                parts.append(stripped)
        elif isinstance(child, Tag) and child.name == 'br':
            parts.append('\n')
    result = ''.join(parts)
    # Collapse 3+ consecutive newlines to 2 (preserve blank lines from <br/><br/>)
    # but also ensure single \n between content lines isn't lost
    result = re.sub(r'\n{3,}', '\n\n', result)
    return result.strip()


def estimate_text_width_in(text: str, font_size_px: float) -> float:
    """Rough text width estimate in inches."""
    if not text:
        return 0.0
    px = estimate_text_width(text, font_size_px)
    return px / PX_PER_IN


def estimate_text_width(text: str, font_size_px: float) -> float:
    """Rough text width estimate in pixels."""
    if not text:
        return 0.0
    char_width = font_size_px * 0.55
    if has_cjk(text):
        char_width *= 1.0
    return len(text) * char_width


def compute_text_content_width(element: Tag, css_rules: List[CSSRule], parent_style: Optional[Dict[str, str]] = None) -> float:
    """Compute natural width of text content within an element, in inches."""
    def _measure_text_width_in(txt: str, font_size_px: float) -> float:
        if not txt:
            return 0.0
        cjk = sum(1 for c in txt if ord(c) > 127)
        latin = len(txt) - cjk
        return (cjk * font_size_px * 0.96 + latin * font_size_px * 0.55) / PX_PER_IN + 0.1

    max_w = 0.0
    style = compute_element_style(element, css_rules, element.get('style', ''), parent_style)

    if element.name in TEXT_TAGS or is_leaf_text_container(element, css_rules):
        txt = get_text_content(element).strip()
        if txt:
            font_size_px = parse_px(style.get('fontSize', '16px'))
            if font_size_px <= 0:
                font_size_px = 16.0
            max_w = max(max_w, _measure_text_width_in(txt, font_size_px))

    for desc in element.descendants:
        if hasattr(desc, 'name') and desc.name and desc.name in ('span', 'div', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'li', 'a'):
            txt = get_text_content(desc).strip()
            if not txt:
                continue
            dstyle = compute_element_style(desc, css_rules, desc.get('style', ''), style)
            font_size_px = parse_px(dstyle.get('fontSize', '16px'))
            if font_size_px <= 0:
                font_size_px = 16.0
            text_w = _measure_text_width_in(txt, font_size_px)
            if text_w > max_w:
                max_w = text_w
    return max_w


def _is_grid_container(style: Dict[str, str]) -> bool:
    display = style.get('display', '')
    if display == 'grid':
        return True
    cols = style.get('gridTemplateColumns', style.get('grid-template-columns', ''))
    return bool(cols)


def _detect_flex_container(style: Dict[str, str]) -> bool:
    display = style.get('display', '')
    return display in ('flex', 'inline-flex')


def _detect_flex_row(style: Dict[str, str]) -> bool:
    if not _detect_flex_container(style):
        return False
    direction = style.get('flexDirection', style.get('flex-direction', ''))
    return direction != 'column'


def _flex_row_prefers_compact_packing(style: Dict[str, str]) -> bool:
    """Source CSS authored a compact-packed flex row.

    Pattern (e.g. `.hero-stats { display:flex; gap: 32px }`): explicit `gap`
    with no distributing `justify-content`. Children pack at their intrinsic
    widths separated by `gap`, NOT spread evenly across the container.
    """
    if not _detect_flex_row(style):
        return False
    if _get_gap_px(style) <= 0:
        return False
    justify = style.get('justifyContent', style.get('justify-content', '')).strip()
    if justify in ('space-between', 'space-around', 'space-evenly'):
        return False
    return True


def _resolve_css_length_with_basis(val_str: str, basis_px: float) -> float:
    val_str = (val_str or '').strip()
    if not val_str:
        return 0.0
    if val_str.startswith('clamp('):
        inner = val_str[len('clamp('):-1]
        args = _split_css_function_args(inner)
        if len(args) == 3:
            min_val = _resolve_css_length_with_basis(args[0], basis_px)
            pref_val = _resolve_css_length_with_basis(args[1], basis_px)
            max_val = _resolve_css_length_with_basis(args[2], basis_px)
            return min(max(min_val, pref_val), max_val)
    if val_str.startswith('min(') or val_str.startswith('max('):
        op = 'min' if val_str.startswith('min(') else 'max'
        inner = val_str[len(op) + 1:-1]
        args = _split_css_function_args(inner)
        values = [_resolve_css_length_with_basis(arg, basis_px) for arg in args]
        values = [v for v in values if v > 0]
        if not values:
            return 0.0
        return min(values) if op == 'min' else max(values)
    m = re.match(r'^(-?[\d.]+)%$', val_str)
    if m:
        return float(m.group(1)) / 100.0 * basis_px
    return _resolve_css_length(val_str)


def _split_grid_track_tokens(grid_template: str) -> List[str]:
    return [part.strip() for part in _split_css_values(grid_template) if part.strip() and part.strip() != 'auto']


def _extract_min_track_px(track_expr: str, basis_px: float) -> float:
    track_expr = (track_expr or '').strip()
    if track_expr.startswith('minmax('):
        inner = track_expr[len('minmax('):-1]
        args = _split_css_function_args(inner)
        if args:
            return max(_resolve_css_length_with_basis(args[0], basis_px), 1.0)
    if track_expr.endswith('fr'):
        return 0.0
    return max(_resolve_css_length_with_basis(track_expr, basis_px), 1.0)


def _parse_grid_track_widths(grid_template: str, available_width_in: float, gap_in: float) -> List[float]:
    template = (grid_template or '').strip()
    if not template:
        return []

    available_px = max(available_width_in * PX_PER_IN, 1.0)
    gap_px = max(gap_in * PX_PER_IN, 0.0)

    repeat_match = re.match(r'^repeat\(\s*([^,]+)\s*,\s*(.+)\)\s*$', template)
    if repeat_match:
        repeat_arg = repeat_match.group(1).strip()
        track_expr = repeat_match.group(2).strip()
        if repeat_arg.isdigit():
            count = max(int(repeat_arg), 1)
            if track_expr.endswith('fr'):
                width_px = max((available_px - gap_px * max(count - 1, 0)) / count, 1.0)
                return [width_px / PX_PER_IN] * count
            track_px = max(_extract_min_track_px(track_expr, available_px), 1.0)
            return [track_px / PX_PER_IN] * count
        if repeat_arg in ('auto-fit', 'auto-fill'):
            min_track_px = max(_extract_min_track_px(track_expr, available_px), 1.0)
            count = max(int((available_px + gap_px) // (min_track_px + gap_px)), 1)
            width_px = max((available_px - gap_px * max(count - 1, 0)) / count, min_track_px)
            return [width_px / PX_PER_IN] * count

    tokens = _split_grid_track_tokens(template)
    if not tokens:
        return []

    fixed_total_px = 0.0
    fr_total = 0.0
    track_kinds: List[Tuple[str, float]] = []

    for token in tokens:
        if token.endswith('fr'):
            fr_val = parse_px(token[:-2] or '1')
            fr_val = fr_val if fr_val > 0 else 1.0
            fr_total += fr_val
            track_kinds.append(('fr', fr_val))
            continue
        track_px = max(_extract_min_track_px(token, available_px), 1.0)
        fixed_total_px += track_px
        track_kinds.append(('fixed', track_px))

    remaining_px = max(available_px - fixed_total_px - gap_px * max(len(tokens) - 1, 0), 1.0)
    widths_in: List[float] = []
    for kind, value in track_kinds:
        if kind == 'fr':
            widths_in.append((remaining_px * (value / max(fr_total, 1.0))) / PX_PER_IN)
        else:
            widths_in.append(value / PX_PER_IN)
    return widths_in


def _parse_grid_columns(grid_template: str, available_width_in: Optional[float] = None, gap_in: float = 0.0) -> int:
    widths = _parse_grid_track_widths(grid_template, available_width_in or 12.0, gap_in)
    if widths:
        return len(widths)
    cols = _split_grid_track_tokens(grid_template)
    return max(len(cols), 1)


def _has_centered_parent_column(container: Tag, css_rules: List[CSSRule], style: Dict[str, str]) -> bool:
    """Detect centered column wrappers that naturally shrink-wrap descendant card grids."""
    parent = getattr(container, 'parent', None)
    if not isinstance(parent, Tag):
        return False
    parent_style = compute_element_style(parent, css_rules, parent.get('style', ''), style)
    if _detect_flex_container(parent_style) and parent_style.get('flexDirection', '') == 'column':
        if parent_style.get('alignItems', '') == 'center':
            return True
        if parent_style.get('textAlign', '') == 'center':
            return True
        if parent_style.get('justifyContent', '') == 'center':
            return True
    return parent_style.get('textAlign', '') == 'center'


def _should_use_intrinsic_auto_fit_grid(
    container: Tag,
    css_rules: List[CSSRule],
    style: Dict[str, str],
    grid_template: str,
    *,
    local_origin: bool,
    content_width_px: Optional[float],
    slide_width_px: float,
) -> bool:
    if not local_origin or not grid_template:
        return False
    if not re.match(r'^repeat\(\s*auto-(fit|fill)\s*,', grid_template.strip()):
        return False
    if parse_px(style.get('width', '')) > 0:
        return False
    max_width_px = _resolve_css_length_with_basis(
        style.get('maxWidth', style.get('max-width', '')),
        VIEWPORT_WIDTH_PX,
    )
    if (
        max_width_px > 0 or
        (content_width_px and content_width_px < slide_width_px * 0.7)
    ):
        return True

    if not _has_centered_parent_column(container, css_rules, style):
        return False

    tag_children = [child for child in container.children if isinstance(child, Tag)]
    if not tag_children or len(tag_children) > 2:
        return False

    return all(
        has_visible_bg_or_border(
            compute_element_style(child, css_rules, child.get('style', ''), style)
        )
        for child in tag_children
    )


def _should_stack_centered_auto_fit_cards(
    container: Tag,
    css_rules: List[CSSRule],
    style: Dict[str, str],
) -> bool:
    """Centered auto-fit grids with a couple of card blocks often shrink-wrap to one column.

    This matches CTA / installation patterns where the wrapper itself is centered
    and unconstrained by explicit width, so the browser collapses the grid to a
    single intrinsic column instead of stretching into two tracks.
    """
    centered_context = (
        style.get('textAlign', '') == 'center' or
        _has_centered_parent_column(container, css_rules, style)
    )
    if not centered_context:
        return False
    if parse_px(style.get('width', '')) > 0:
        return False

    tag_children = [child for child in container.children if isinstance(child, Tag)]
    if not tag_children or len(tag_children) > 2:
        return False

    card_like = 0
    for child in tag_children:
        child_style = compute_element_style(child, css_rules, child.get('style', ''), style)
        if has_visible_bg_or_border(child_style):
            card_like += 1
    return card_like == len(tag_children)


def _resolve_intrinsic_auto_fit_cols(
    layout_inner_width_in: float,
    gap_in: float,
    intrinsic_min_track_in: float,
) -> int:
    """Resolve how many auto-fit tracks can fit inside a constrained wrapper."""
    if intrinsic_min_track_in <= 0:
        return 1
    denom = intrinsic_min_track_in + max(gap_in, 0.0)
    if denom <= 0:
        return 1
    cols = int((layout_inner_width_in + max(gap_in, 0.0)) / denom)
    return max(cols, 1)


def _resolve_effective_auto_fit_cols(
    layout_inner_width_in: float,
    gap_in: float,
    intrinsic_min_track_in: float,
    item_count: int,
    *,
    collapse_empty_tracks: bool,
) -> int:
    """Approximate browser auto-fit by collapsing empty tracks when items are fewer."""
    fit_cols = _resolve_intrinsic_auto_fit_cols(
        layout_inner_width_in,
        gap_in,
        intrinsic_min_track_in,
    )
    if not collapse_empty_tracks:
        return fit_cols
    if item_count <= 0:
        return fit_cols
    return max(min(fit_cols, item_count), 1)


def _get_gap_px(style: Dict[str, str]) -> float:
    gap = style.get('gap', style.get('gridGap', ''))
    return parse_px(gap) if gap else 20.0


# ─── Inline Fragment + Text Segment Extraction ───────────────────────────────

def _normalize_inline_text(text: str) -> str:
    """Collapse formatting whitespace while preserving meaningful separators."""
    if not text:
        return ''
    text = text.replace('\xa0', ' ')
    return re.sub(r'\s+', ' ', text)


def _style_text_color(style: Dict[str, str], fallback: str = '') -> str:
    """Resolve text color, including gradient-text cases."""
    if _is_gradient_text_style(style):
        gradient_colors = _extract_gradient_colors(style.get('backgroundImage', ''))
        if gradient_colors:
            return gradient_colors[0]
    sc = style.get('color', '')
    if sc and sc != 'rgba(0, 0, 0, 0)':
        return sc
    return _default_text_color(fallback)


def _fragment_style_snapshot(style: Dict[str, str]) -> Dict[str, str]:
    """Keep the inline-box styling needed for measurement and rendering."""
    return {
        'fontFamily': style.get('fontFamily', ''),
        'letterSpacing': style.get('letterSpacing', ''),
        'backgroundColor': style.get('backgroundColor', ''),
        'border': style.get('border', ''),
        'borderLeft': style.get('borderLeft', ''),
        'borderRight': style.get('borderRight', ''),
        'borderTop': style.get('borderTop', ''),
        'borderBottom': style.get('borderBottom', ''),
        'borderRadius': style.get('borderRadius', ''),
        'color': style.get('color', ''),
        'paddingLeft': style.get('paddingLeft', '0px'),
        'paddingRight': style.get('paddingRight', '0px'),
        'paddingTop': style.get('paddingTop', '0px'),
        'paddingBottom': style.get('paddingBottom', '0px'),
    }


def _fragments_share_style(a: Dict[str, Any], b: Dict[str, Any]) -> bool:
    """Whether two fragments can be safely merged into one text run."""
    return (
        a.get('kind') == b.get('kind') and
        a.get('color') == b.get('color') and
        a.get('bold') == b.get('bold') and
        a.get('fontSize') == b.get('fontSize') and
        a.get('strike') == b.get('strike') and
        a.get('bgColor') == b.get('bgColor') and
        a.get('styles', {}).get('fontFamily', '') == b.get('styles', {}).get('fontFamily', '') and
        a.get('styles', {}).get('letterSpacing', '') == b.get('styles', {}).get('letterSpacing', '')
    )


def _is_emoji_only_text(text: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    return bool(re.fullmatch(r'[\U0001F300-\U0001FAFF\u2600-\u27BF\uFE0F\s]+', stripped))


def _mark_flow_box_descendants(elements: List[Dict[str, Any]]) -> None:
    """Mark descendants as belonging to a flow_box and clear legacy card grouping."""
    for elem in elements:
        elem['_in_flow_box'] = True
        elem.pop('_card_group', None)
        children = elem.get('children', [])
        if children:
            _mark_flow_box_descendants(children)


def extract_inline_fragments(
    element: Tag,
    css_rules: List[CSSRule],
    parent_style: Optional[Dict[str, str]] = None,
    exclude_elements: Optional[set] = None,
) -> List[Dict[str, Any]]:
    """
    Walk a text subtree and retain first-class inline semantics for code/kbd.

    Fragments are later consumed by both text and table export paths.
    """
    if not element:
        return []

    fragments: List[Dict[str, Any]] = []

    def push_text_fragment(text: str, style: Dict[str, str]) -> None:
        normalized = _normalize_inline_text(text)
        if not normalized:
            return
        fragments.append({
            'kind': 'text',
            'text': normalized,
            'color': _style_text_color(style, style.get('color', '')),
            'bold': is_bold(style.get('fontWeight', '')),
            'fontSize': style.get('fontSize', '16px'),
            'strike': 'line-through' in style.get('textDecoration', style.get('textDecorationLine', '')),
            'bgColor': None,
            'styles': _fragment_style_snapshot(style),
        })

    def push_box_fragment(kind: str, text: str, style: Dict[str, str]) -> None:
        normalized = _normalize_inline_text(text).strip()
        if not normalized:
            return
        fragments.append({
            'kind': kind,
            'text': normalized,
            'color': _style_text_color(style, style.get('color', '')),
            'bold': True if kind == 'kbd' else is_bold(style.get('fontWeight', '')),
            'fontSize': style.get('fontSize', '16px'),
            'strike': 'line-through' in style.get('textDecoration', style.get('textDecorationLine', '')),
            'bgColor': style.get('backgroundColor', '') or None,
            'styles': _fragment_style_snapshot(style),
        })

    def push_styled_text_fragment(kind: str, text: str, style: Dict[str, str]) -> None:
        normalized = _normalize_inline_text(text)
        if not normalized:
            return
        fragments.append({
            'kind': kind,
            'text': normalized,
            'color': _style_text_color(style, style.get('color', '')),
            'bold': is_bold(style.get('fontWeight', '')),
            'fontSize': style.get('fontSize', '16px'),
            'strike': 'line-through' in style.get('textDecoration', style.get('textDecorationLine', '')),
            'bgColor': style.get('backgroundColor', '') or None,
            'styles': _fragment_style_snapshot(style),
        })

    def walk(node, inherited_style: Dict[str, str]) -> None:
        if exclude_elements is not None and hasattr(node, 'parents'):
            if any(parent in exclude_elements for parent in node.parents):
                return
        if isinstance(node, NavigableString):
            push_text_fragment(str(node), inherited_style)
            return
        if not isinstance(node, Tag):
            return
        if exclude_elements is not None and node in exclude_elements:
            return
        tag = node.name.lower()
        if tag == 'br':
            fragments.append({
                'kind': 'text',
                'text': '\n',
                'color': _style_text_color(inherited_style, inherited_style.get('color', '')),
                'bold': is_bold(inherited_style.get('fontWeight', '')),
                'fontSize': inherited_style.get('fontSize', '16px'),
                'strike': 'line-through' in inherited_style.get('textDecoration', inherited_style.get('textDecorationLine', '')),
                'bgColor': None,
                'styles': _fragment_style_snapshot(inherited_style),
            })
            return

        style = compute_element_style(node, css_rules, node.get('style', ''), inherited_style)
        if tag in ('strong', 'b'):
            style = dict(style)
            style['fontWeight'] = style.get('fontWeight', '700') or '700'
        elif tag in ('s', 'del', 'strike'):
            style = dict(style)
            existing_td = style.get('textDecoration', style.get('textDecorationLine', ''))
            style['textDecoration'] = f'{existing_td} line-through'.strip()
        elif tag == 'a':
            push_styled_text_fragment('link', get_text_content(node), style)
            return
        elif tag in ('img', 'svg'):
            label = node.get('alt') or node.get('aria-label') or ''
            if label:
                push_box_fragment('icon', label, style)
            return
        if tag in ('code', 'kbd'):
            push_box_fragment(tag, get_text_content(node), style)
            return
        if tag in ('span', 'mark', 'small', 'var', 'abbr', 'time', 'sup', 'sub'):
            if has_visible_bg_or_border(style) and is_leaf_text_container(node, css_rules):
                push_box_fragment('badge', get_text_content(node), style)
                return

        for child in node.children:
            walk(child, style)

    base_style = compute_element_style(element, css_rules, element.get('style', ''), parent_style)
    for child in element.children:
        walk(child, base_style)

    merged: List[Dict[str, Any]] = []
    for frag in fragments:
        text = frag.get('text', '')
        if text == '\n':
            merged.append(frag)
            continue
        if not text:
            continue
        if (merged and frag.get('kind') == 'text' and merged[-1].get('text') != '\n' and
                _fragments_share_style(merged[-1], frag)):
            merged[-1]['text'] += text
        else:
            merged.append(dict(frag))

    # Trim indentation-only whitespace from the edges while preserving inner separators.
    while merged and merged[0].get('kind') == 'text' and merged[0].get('text', '') != '\n':
        trimmed = merged[0]['text'].lstrip()
        if trimmed:
            merged[0]['text'] = trimmed
            break
        merged.pop(0)
    while merged and merged[-1].get('kind') == 'text' and merged[-1].get('text', '') != '\n':
        trimmed = merged[-1]['text'].rstrip()
        if trimmed:
            merged[-1]['text'] = trimmed
            break
        merged.pop()

    grouped = False
    group_align = base_style.get('alignItems', '') or 'center'
    inline_group_count = sum(1 for frag in merged if frag.get('kind') in INLINE_GROUP_KINDS)
    has_badge = any(frag.get('kind') == 'badge' for frag in merged)
    has_link = any(frag.get('kind') == 'link' for frag in merged)
    has_text_fragments = any(frag.get('kind') == 'text' and frag.get('text', '').strip() for frag in merged)
    if inline_group_count >= 2 or (has_badge and (has_link or has_text_fragments)):
        grouped = True

    if grouped:
        for frag in merged:
            frag['grouped'] = True
            frag['groupAlign'] = group_align

    return merged


def inline_fragments_to_segments(fragments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Down-convert inline fragments into rich text segments for PPT text runs."""
    segments: List[Dict[str, Any]] = []
    for frag in fragments:
        frag_styles = frag.get('styles', {})
        seg = {
            'text': frag.get('text', ''),
            'color': frag.get('color', ''),
            'bold': frag.get('bold', False),
            'fontSize': frag.get('fontSize', ''),
            'fontFamily': frag_styles.get('fontFamily', ''),
            'letterSpacing': frag_styles.get('letterSpacing', ''),
            'strike': frag.get('strike', False),
            'bgColor': frag.get('bgColor'),
            'inlineBgBounds': None,
            'kind': frag.get('kind', 'text'),
        }
        if (segments and seg['kind'] == 'text' and seg['text'] != '\n' and
                segments[-1].get('kind') == 'text' and segments[-1]['text'] != '\n' and
                _fragments_share_style(segments[-1], seg)):
            segments[-1]['text'] += seg['text']
        else:
            segments.append(seg)
    return segments


def _normalize_centered_command_fragments(
    fragments: List[Dict[str, Any]],
    base_color: str,
) -> List[Dict[str, Any]]:
    """Mute trailing link/separator fragments in centered command rows."""
    normalized: List[Dict[str, Any]] = []
    muted_color = _normalize_ink_color(base_color or '#64748b') or '#64748b'
    for frag in fragments:
        next_frag = dict(frag)
        if next_frag.get('kind') == 'link':
            next_frag['color'] = muted_color
        elif next_frag.get('kind') == 'text':
            text = next_frag.get('text', '')
            stripped = text.strip()
            if stripped and re.fullmatch(r'[·•↗/|:\-–—\s]+', stripped):
                next_frag['color'] = muted_color
        normalized.append(next_frag)
    return normalized


def _normalize_display_ink_fragments(
    fragments: List[Dict[str, Any]],
    color: str = '#000000',
) -> List[Dict[str, Any]]:
    """Force plain display-heading fragments to strong ink while preserving boxes."""
    normalized: List[Dict[str, Any]] = []
    for frag in fragments:
        next_frag = dict(frag)
        if next_frag.get('kind') not in INLINE_BOX_KINDS:
            next_frag['color'] = color
        normalized.append(next_frag)
    return normalized


def fragments_to_text(fragments: List[Dict[str, Any]]) -> str:
    """Flatten fragments back into plain text for layout estimation."""
    return ''.join(frag.get('text', '') for frag in fragments)


def _measure_inline_fragment_box_px(
    fragment: Dict[str, Any],
    default_font_px: float = 16.0,
    include_box_padding: bool = False,
) -> Tuple[float, float]:
    """Estimate width/height for a single inline fragment."""
    text = fragment.get('text', '')
    if not text or text == '\n':
        return 0.0, 0.0
    font_px = parse_px(fragment.get('fontSize', '')) or default_font_px
    frag_kind = fragment.get('kind', '')
    styles = fragment.get('styles', {})
    width_px = _estimate_text_width_px(
        text,
        font_px,
        monospace=frag_kind in ('code', 'kbd') or _uses_monospace_font(styles.get('fontFamily', '')),
        letter_spacing=styles.get('letterSpacing', ''),
    )
    height_px = font_px * 1.25

    if include_box_padding and frag_kind in INLINE_BOX_KINDS:
        width_px += parse_px(styles.get('paddingLeft', '0px'))
        width_px += parse_px(styles.get('paddingRight', '0px'))
        height_px = max(
            height_px,
            font_px + parse_px(styles.get('paddingTop', '0px')) + parse_px(styles.get('paddingBottom', '0px'))
        )
        border = styles.get('border', '')
        if border and 'none' not in border and not border.startswith('0px'):
            border_match = re.match(r'([\d.]+)px', border)
            if border_match:
                width_px += float(border_match.group(1)) * 2
                height_px += float(border_match.group(1)) * 2

    return width_px, height_px


def _should_apply_display_heading_boost(tag: str, style: Dict[str, str], text: str) -> bool:
    """Optically compensate bold CJK display headings that render smaller in PPT."""
    if tag not in {'h1', 'h2'} or not text or not has_cjk(text):
        return False
    if has_visible_bg_or_border(style):
        return False
    if not is_bold(style.get('fontWeight', '400')):
        return False
    font_stack = (style.get('fontFamily', '') or '').lower()
    if 'space grotesk' in font_stack:
        return False
    # 'noto sans' is intentionally excluded: when the source CSS lists Noto
    # Sans SC and the exporter remaps it to Helvetica Neue + Hiragino Sans GB,
    # both Latin and CJK glyphs render at the authored font-size with no
    # optical shrinkage, so a 1.30x boost overshoots and wraps headings.
    if not any(token in font_stack for token in ('inter', 'dm sans', 'clash display', 'satoshi', 'system-ui')):
        return False
    font_px = parse_px(style.get('fontSize', '16px'))
    if font_px < 28.0:
        return False
    return True


def measure_inline_fragments_width_in(
    fragments: List[Dict[str, Any]],
    default_font_px: float = 16.0,
    include_box_padding: bool = False,
) -> float:
    """Measure the widest visual line across inline fragments."""
    line_width_px = 0.0
    max_line_px = 0.0
    for frag in fragments:
        if frag.get('text') == '\n':
            max_line_px = max(max_line_px, line_width_px)
            line_width_px = 0.0
            continue
        frag_w_px, _ = _measure_inline_fragment_box_px(frag, default_font_px, include_box_padding)
        line_width_px += frag_w_px
    max_line_px = max(max_line_px, line_width_px)
    return max_line_px / PX_PER_IN


def measure_inline_fragments_height_in(
    fragments: List[Dict[str, Any]],
    default_font_px: float = 16.0,
    include_box_padding: bool = False,
) -> float:
    """Measure total height across one or more fragment lines."""
    total_height_px = 0.0
    line_height_px = 0.0
    for frag in fragments:
        if frag.get('text') == '\n':
            total_height_px += line_height_px or (default_font_px * 1.25)
            line_height_px = 0.0
            continue
        _, frag_h_px = _measure_inline_fragment_box_px(frag, default_font_px, include_box_padding)
        line_height_px = max(line_height_px, frag_h_px)
    total_height_px += line_height_px or (default_font_px * 1.25)
    return total_height_px / PX_PER_IN


def extract_text_segments(
    element: Tag,
    css_rules: List[CSSRule],
    parent_style: Optional[Dict[str, str]] = None,
    exclude_elements: Optional[set] = None,
) -> List[Dict[str, Any]]:
    """Backward-compatible wrapper around the new inline fragment extractor."""
    fragments = extract_inline_fragments(element, css_rules, parent_style, exclude_elements=exclude_elements)
    return inline_fragments_to_segments(fragments)


# ─── Flat Extract (adapted from browser version's flatExtract) ────────────────

def build_image_element(element: Tag, style: Dict[str, str]) -> Optional[Dict]:
    """Build an image element IR."""
    src = ''
    if element.name == 'img':
        src = element.get('src', '') or element.get('data-src', '')
    elif element.name == 'svg':
        src = str(element)
    if not src and element.name != 'svg':
        return None
    return {
        'type': 'image', 'tag': element.name, 'imageKind': element.name,
        'source': src,
        'bounds': {'x': 0, 'y': 0, 'width': 4, 'height': 3},
        'styles': {'borderRadius': '', 'objectFit': style.get('objectFit', '')},
    }


def _parse_svg_float(raw: Any, default: float = 0.0) -> float:
    if raw is None:
        return default
    m = re.search(r'-?[\d.]+', str(raw))
    return float(m.group(0)) if m else default


def _parse_svg_points(raw: Any) -> List[Tuple[float, float]]:
    if raw is None:
        return []
    nums = re.findall(r'-?[\d.]+', str(raw))
    if len(nums) < 4:
        return []
    values = [float(num) for num in nums]
    return [(values[idx], values[idx + 1]) for idx in range(0, len(values) - 1, 2)]


def _parse_svg_viewbox(svg: Tag) -> Tuple[float, float]:
    raw = svg.get('viewBox') or svg.get('viewbox') or ''
    parts = [p for p in re.split(r'[\s,]+', raw.strip()) if p]
    if len(parts) == 4:
        return max(_parse_svg_float(parts[2], 1.0), 1.0), max(_parse_svg_float(parts[3], 1.0), 1.0)
    width = _parse_svg_float(svg.get('width'), 460.0)
    height = _parse_svg_float(svg.get('height'), 240.0)
    return max(width, 1.0), max(height, 1.0)


def _extract_svg_gradient_stops(svg: Tag) -> Dict[str, str]:
    gradients: Dict[str, str] = {}
    for grad in svg.find_all(['lineargradient', 'linearGradient', 'radialgradient', 'radialGradient']):
        grad_id = (grad.get('id') or '').strip()
        if not grad_id:
            continue
        stop = grad.find(['stop'])
        if not stop:
            continue
        color = stop.get('stop-color') or stop.get('stopColor') or ''
        if not color:
            stop_style = stop.get('style', '')
            m = re.search(r'stop-color\s*:\s*([^;]+)', stop_style)
            color = m.group(1).strip() if m else ''
        if color:
            gradients[grad_id] = color
    return gradients


def _resolve_svg_paint(raw: str, gradients: Dict[str, str], fallback: str = '') -> str:
    value = (raw or '').strip()
    if not value or value == 'none':
        return fallback
    grad_match = re.match(r'url\(#([^)]+)\)', value)
    if grad_match:
        return gradients.get(grad_match.group(1), fallback)
    return value


def _is_decorative_svg(element: Tag, style: Dict[str, str]) -> bool:
    class_blob = ' '.join(element.get('class', [])).lower()
    if any(token in class_blob for token in ('ambient', 'orb', 'cloud', 'decor')):
        return True
    if style.get('position', '') == 'absolute':
        return True
    if style.get('filter', ''):
        return True
    return False


def build_svg_container(
    element: Tag,
    css_rules: List[CSSRule],
    parent_style: Optional[Dict[str, str]],
    slide_width_px: float,
    content_width_px: Optional[float] = None,
) -> Optional[Dict[str, Any]]:
    """Build a relative container for simple content SVG (rect/line/text)."""
    style = compute_element_style(element, css_rules, element.get('style', ''), parent_style)
    if _is_decorative_svg(element, style):
        return None

    vb_w, vb_h = _parse_svg_viewbox(element)
    target_w_in = (content_width_px / PX_PER_IN) if content_width_px and content_width_px > 0 else max(vb_w / PX_PER_IN, 0.5)
    target_h_in = max(target_w_in * (vb_h / vb_w), 0.1)
    sx = target_w_in / vb_w
    sy = target_h_in / vb_h
    gradients = _extract_svg_gradient_stops(element)

    children: List[Dict[str, Any]] = []

    for node in element.descendants:
        if not isinstance(node, Tag):
            continue
        node_name = node.name.lower()
        node_style = compute_element_style(node, css_rules, node.get('style', ''), style)

        if node_name == 'rect':
            x = _parse_svg_float(node.get('x'))
            y = _parse_svg_float(node.get('y'))
            w = _parse_svg_float(node.get('width'))
            h = _parse_svg_float(node.get('height'))
            if w <= 0 or h <= 0:
                continue
            fill = _resolve_svg_paint(node.get('fill') or node_style.get('fill', ''), gradients, node_style.get('color', ''))
            if not fill:
                continue
            rx = _parse_svg_float(node.get('rx'))
            children.append({
                'type': 'shape',
                'tag': 'rect',
                'bounds': {'x': x * sx, 'y': y * sy, 'width': w * sx, 'height': h * sy},
                'styles': {
                    'backgroundColor': fill,
                    'borderRadius': f'{max(rx * sx * PX_PER_IN, 0.0):.2f}px' if rx > 0 else '0px',
                },
                '_is_decoration': True,
            })
            continue

        if node_name == 'line':
            x1 = _parse_svg_float(node.get('x1'))
            x2 = _parse_svg_float(node.get('x2'))
            y1 = _parse_svg_float(node.get('y1'))
            y2 = _parse_svg_float(node.get('y2'))
            stroke = _resolve_svg_paint(node.get('stroke') or node_style.get('stroke', ''), gradients, '')
            if not stroke:
                continue
            stroke_w = max(_parse_svg_float(node.get('stroke-width') or node_style.get('strokeWidth', ''), 1.0), 1.0)
            if abs(y2 - y1) <= abs(x2 - x1):
                x = min(x1, x2)
                y = min(y1, y2) - stroke_w / 2.0
                w = max(abs(x2 - x1), 1.0)
                h = max(stroke_w, 1.0)
            else:
                x = min(x1, x2) - stroke_w / 2.0
                y = min(y1, y2)
                w = max(stroke_w, 1.0)
                h = max(abs(y2 - y1), 1.0)
            children.append({
                'type': 'shape',
                'tag': 'line',
                'bounds': {'x': x * sx, 'y': y * sy, 'width': w * sx, 'height': h * sy},
                'styles': {'backgroundColor': stroke, 'borderRadius': '0px'},
                '_is_decoration': True,
            })
            continue

        if node_name in ('polyline', 'polygon'):
            points = _parse_svg_points(node.get('points'))
            if len(points) < 2:
                continue
            stroke = _resolve_svg_paint(node.get('stroke') or node_style.get('stroke', ''), gradients, '')
            fill = _resolve_svg_paint(node.get('fill') or node_style.get('fill', ''), gradients, '')
            stroke_w = max(_parse_svg_float(node.get('stroke-width') or node_style.get('strokeWidth', ''), 1.0), 1.0)
            children.append({
                'type': 'freeform',
                'tag': node_name,
                'points': [(x * sx, y * sy) for x, y in points],
                'closed': node_name == 'polygon',
                'styles': {
                    'stroke': stroke,
                    'fill': fill,
                    'strokeWidth': stroke_w,
                },
                '_is_decoration': True,
            })
            continue

        if node_name == 'circle':
            cx = _parse_svg_float(node.get('cx'))
            cy = _parse_svg_float(node.get('cy'))
            r = _parse_svg_float(node.get('r'))
            if r <= 0:
                continue
            fill = _resolve_svg_paint(node.get('fill') or node_style.get('fill', ''), gradients, '')
            stroke = _resolve_svg_paint(node.get('stroke') or node_style.get('stroke', ''), gradients, '')
            stroke_w = max(_parse_svg_float(node.get('stroke-width') or node_style.get('strokeWidth', ''), 0.0), 0.0)
            children.append({
                'type': 'shape',
                'tag': 'circle',
                'bounds': {
                    'x': (cx - r) * sx,
                    'y': (cy - r) * sy,
                    'width': max(r * 2.0 * sx, 0.04),
                    'height': max(r * 2.0 * sy, 0.04),
                },
                'styles': {
                    'backgroundColor': fill,
                    'border': f'{stroke_w}px solid {stroke}' if stroke and stroke_w > 0 else '',
                    'borderRadius': '999px',
                },
                '_is_decoration': True,
            })
            continue

        if node_name == 'text':
            text = node.get_text(strip=True)
            if not text:
                continue
            font_px = parse_px(node_style.get('fontSize', '12px'))
            if font_px <= 0:
                font_px = 12.0
            text_w_in = max(
                _estimate_text_width_px(
                    text,
                    font_px,
                    letter_spacing=node_style.get('letterSpacing', ''),
                ) / PX_PER_IN,
                0.1,
            )
            text_h_in = max(font_px * 1.15 / PX_PER_IN, 0.12)
            x = _parse_svg_float(node.get('x')) * sx
            y = _parse_svg_float(node.get('y')) * sy - text_h_in * 0.78
            anchor = (node.get('text-anchor') or node_style.get('textAnchor', 'start')).strip()
            if anchor == 'middle':
                x -= text_w_in / 2.0
                align = 'center'
            elif anchor == 'end':
                x -= text_w_in
                align = 'right'
            else:
                align = 'left'
            children.append({
                'type': 'text',
                'tag': 'text',
                'text': text,
                'segments': [{
                    'text': text,
                    'color': _resolve_svg_paint(node.get('fill') or node_style.get('fill', ''), gradients, node_style.get('color', '#e2e8f0')),
                    'fontSize': f'{font_px}px',
                    'fontFamily': node_style.get('fontFamily', ''),
                    'letterSpacing': node_style.get('letterSpacing', ''),
                    'bold': False,
                    'strike': False,
                    'bgColor': None,
                    'inlineBgBounds': None,
                    'kind': 'text',
                }],
                'bounds': {'x': x, 'y': max(y, 0.0), 'width': text_w_in, 'height': text_h_in},
                'styles': {
                    'fontSize': f'{font_px}px',
                    'fontWeight': node_style.get('fontWeight', '400'),
                    'fontFamily': node_style.get('fontFamily', ''),
                    'letterSpacing': node_style.get('letterSpacing', ''),
                    'color': _resolve_svg_paint(node.get('fill') or node_style.get('fill', ''), gradients, node_style.get('color', '#e2e8f0')),
                    'textAlign': align,
                    'lineHeight': 'normal',
                    'paddingLeft': '0px',
                    'paddingRight': '0px',
                    'paddingTop': '0px',
                    'paddingBottom': '0px',
                },
                'preferNoWrapFit': True,
            })

    if not children:
        return None

    return {
        'type': 'container',
        'tag': 'svg',
        'bounds': {'x': 0.0, 'y': 0.0, 'width': target_w_in, 'height': target_h_in},
        'styles': style,
        'children': children,
        '_children_relative': True,
    }


def build_shape_element(element: Tag, style: Dict[str, str], slide_width_px: float = 1440) -> Dict:
    """Build a shape element IR (div with background/border)."""
    w_px = parse_px(style.get('width', ''))
    h_px = parse_px(style.get('height', ''))
    if w_px > 0 and h_px > 0:
        # Element has explicit CSS dimensions (e.g., divider, pill)
        w_in = w_px / PX_PER_IN
        h_in = h_px / PX_PER_IN
    else:
        # Check maxWidth as fallback constraint
        max_w_px = parse_px(style.get('maxWidth', ''))
        if max_w_px > 0:
            w_in = max_w_px / PX_PER_IN
        else:
            w_in = 12.33
        h_in = 1.0

    border_radius_px = resolve_border_radius(style, w_px or parse_px(style.get('maxWidth', '100%')),
                                                h_px or parse_px(style.get('maxHeight', '100px')))
    return {
        'type': 'shape', 'tag': element.name,
        'bounds': {'x': 0.5, 'y': 0.5, 'width': w_in, 'height': h_in},
        'styles': {
            'backgroundColor': style.get('backgroundColor', ''),
            'backgroundImage': style.get('backgroundImage', ''),
            'border': style.get('border', ''),
            'borderLeft': style.get('borderLeft', ''),
            'borderRight': style.get('borderRight', ''),
            'borderTop': style.get('borderTop', ''),
            'borderBottom': style.get('borderBottom', ''),
            'borderRadius': f'{border_radius_px}px',
            'marginTop': style.get('marginTop', ''),
            'marginBottom': style.get('marginBottom', ''),
            'marginLeft': style.get('marginLeft', ''),
            'marginRight': style.get('marginRight', ''),
        },
    }


def _attach_pair_box_insets(shape: Dict[str, Any], style: Dict[str, str]) -> None:
    """Preserve CSS padding so paired bg shapes stay larger than their text boxes."""
    display = style.get('display', '')
    if 'inline-block' in display or 'inline-flex' in display:
        return
    _expand_padding(style)
    pair_pad_l = parse_px(style.get('paddingLeft', '0px')) / PX_PER_IN
    pair_pad_r = parse_px(style.get('paddingRight', '0px')) / PX_PER_IN
    pair_pad_t = parse_px(style.get('paddingTop', '0px')) / PX_PER_IN
    pair_pad_b = parse_px(style.get('paddingBottom', '0px')) / PX_PER_IN
    if pair_pad_l or pair_pad_r or pair_pad_t or pair_pad_b:
        shape['_pair_pad_l'] = pair_pad_l
        shape['_pair_pad_r'] = pair_pad_r
        shape['_pair_pad_t'] = pair_pad_t
        shape['_pair_pad_b'] = pair_pad_b


def _element_classes(element: Tag) -> set[str]:
    return {cls for cls in (element.get('class') or []) if isinstance(cls, str)}


def _selector_matches_element_class(element: Tag, selector: str) -> bool:
    selector = (selector or '').strip()
    if not selector.startswith('.'):
        return False
    return selector[1:] in _element_classes(element)


def _selector_matches_contract_target(element: Tag, selector: str) -> bool:
    selector = (selector or '').strip()
    if not selector:
        return False
    if selector.startswith('.'):
        return selector[1:] in _element_classes(element)
    if selector.startswith('#'):
        return (element.get('id') or '').strip() == selector[1:]
    return element.name.lower() == selector.lower()


def _css_font_stack_value(fonts: List[str]) -> str:
    rendered: List[str] = []
    generic_families = {'serif', 'sans-serif', 'monospace', 'system-ui'}
    for raw in fonts or []:
        token = (raw or '').strip()
        if not token:
            continue
        bare = token.strip('\'"')
        if bare.lower() in generic_families:
            rendered.append(bare)
        elif re.search(r'[\s-]', bare):
            rendered.append(f'"{bare}"')
        else:
            rendered.append(bare)
    return ', '.join(rendered)


def _contract_component_name(element: Tag, contract: Optional[Dict[str, Any]]) -> Optional[str]:
    if not contract:
        return None
    selectors = contract.get('component_selectors') or {}
    for component_name, selector_list in selectors.items():
        for selector in selector_list or []:
            if _selector_matches_element_class(element, selector):
                return component_name
    return None


def _contract_slot_model(contract: Optional[Dict[str, Any]], component_name: Optional[str]) -> Dict[str, Any]:
    if not contract or not component_name:
        return {}
    return (contract.get('component_slot_models') or {}).get(component_name, {}) or {}


def _font_stack_for_family_mode(typography: Dict[str, Any], family_mode: str) -> str:
    family_mode = (family_mode or '').strip()
    stack_map = {
        'cn_serif': 'cn_font_stack',
        'en_serif': 'en_font_stack',
        'display_sans': 'display_font_stack',
        'body_sans': 'body_font_stack',
        'label_sans': 'label_font_stack',
    }
    stack_key = stack_map.get(family_mode, '')
    if not stack_key:
        return ''
    return _css_font_stack_value(typography.get(stack_key) or [])


def _resolve_text_contract(
    element: Tag,
    style: Dict[str, str],
    raw_text: str,
    contract: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    resolved: Dict[str, Any] = {
        'role': None,
        'breakPolicy': 'allow_reflow',
        'preserveAuthoredBreaks': False,
        'preferWrapToPreserveSize': False,
        'shrinkForbidden': False,
        'overflowStrategy': '',
    }
    if not contract:
        return resolved

    typography = contract.get('typography') or {}
    role_selectors = typography.get('role_selectors') or {}
    matched_role = None
    for role_name, selectors in role_selectors.items():
        if any(_selector_matches_contract_target(element, selector) for selector in selectors or []):
            matched_role = role_name
            break

    if matched_role:
        resolved['role'] = matched_role
        role_cfg = (typography.get(matched_role) or {})
        family_mode = role_cfg.get('family_mode', '').strip()
        family_override = _font_stack_for_family_mode(typography, family_mode)
        if family_override and not style.get('fontFamily'):
            resolved['fontFamily'] = family_override
        if role_cfg.get('weight') is not None and not style.get('fontWeight'):
            resolved['fontWeight'] = str(role_cfg['weight'])
        if role_cfg.get('line_height') is not None and not style.get('lineHeight'):
            resolved['lineHeight'] = str(role_cfg['line_height'])
        if role_cfg.get('letter_spacing') is not None and not style.get('letterSpacing'):
            resolved['letterSpacing'] = str(role_cfg['letter_spacing'])

    break_contract = contract.get('line_break_contract') or {}
    break_policy = 'allow_reflow'
    for selector, policy in (break_contract.get('break_policy') or {}).items():
        if _selector_matches_contract_target(element, selector):
            break_policy = (policy or 'allow_reflow').strip()
            break
    resolved['breakPolicy'] = break_policy
    resolved['shrinkForbidden'] = any(
        _selector_matches_contract_target(element, selector)
        for selector in (break_contract.get('shrink_forbidden_for') or [])
    )
    resolved['overflowStrategy'] = (break_contract.get('overflow_strategy') or '').strip()

    if '\n' in raw_text:
        if break_policy in ('preserve', 'prefer_preserve'):
            resolved['preserveAuthoredBreaks'] = True
    elif break_policy == 'prefer_preserve' and resolved['shrinkForbidden']:
        # Some authored heading systems intentionally omit <br> but rely on the
        # browser's natural wrapping inside a constrained width. Prefer
        # reflowing at the authored bounds over shrinking the type into one line.
        resolved['preferWrapToPreserveSize'] = True
    elif (
        break_policy == 'preserve' and
        resolved['shrinkForbidden'] and
        matched_role == 'body'
    ):
        # Editorial body copy may omit explicit <br> but still depends on the
        # authored column width for its reading rhythm. Preserve that width by
        # preferring reflow over no-wrap shrink heuristics.
        resolved['preferWrapToPreserveSize'] = True

    return resolved


def _looks_like_metric_token(text: str) -> bool:
    token = ' '.join((text or '').split())
    if not token or '\n' in token or len(token) > 12:
        return False
    if re.fullmatch(r'[<>]?\d+(?:\.\d+)?(?:[%+]|vh|vw|s|x)?', token, re.IGNORECASE):
        return True
    if re.fullmatch(r'[<>]?\d+(?:\.\d+)?[A-Za-z]{1,6}', token, re.IGNORECASE):
        return True
    if re.fullmatch(r'[A-Za-z]{1,6}\+?', token):
        return True
    if re.fullmatch(r'[A-Za-z]{1,6}\d*[+%]?', token):
        return True
    return False


def _is_slide_root_element(element: Optional[Tag]) -> bool:
    if not isinstance(element, Tag):
        return False
    if element.name.lower() != 'section':
        return False
    classes = element.get('class') or []
    return (
        'slide' in classes or
        bool(element.get('data-slide')) or
        bool(element.get('data-page')) or
        bool(element.get('data-export-role'))
    )


def _is_slide_or_body_anchored_positioned(element: Tag, style: Dict[str, str]) -> bool:
    pos = style.get('position', '').strip()
    if pos not in ('absolute', 'fixed'):
        return False

    has_anchor = any(
        style.get(side, '').strip() not in ('', 'auto')
        for side in ('top', 'right', 'bottom', 'left')
    )
    if not has_anchor:
        return False

    parent = element.parent if isinstance(element.parent, Tag) else None
    if not parent:
        return False
    if parent.name.lower() == 'body':
        return True
    return _is_slide_root_element(parent)


def _translate_ir_tree(elem: Dict[str, Any], dx: float, dy: float) -> None:
    bounds = elem.get('bounds', {})
    bounds['x'] = bounds.get('x', 0.0) + dx
    bounds['y'] = bounds.get('y', 0.0) + dy
    if elem.get('type') == 'container' and elem.get('_children_relative'):
        _translate_container_descendants(elem, dx, dy)


def _apply_slide_anchor_position(elem: Dict[str, Any], slide_w_in: float = SLIDE_W_IN, slide_h_in: float = SLIDE_H_IN) -> bool:
    styles = elem.get('styles', {}) or {}
    pos = styles.get('position', '').strip()
    if pos not in ('absolute', 'fixed'):
        return False

    bounds = elem.get('bounds', {})
    width = bounds.get('width', 0.0)
    height = bounds.get('height', 0.0)
    if elem.get('type') == 'text':
        natural_w = elem.get('inlineContentWidth', 0.0)
        if (not natural_w or natural_w <= 0.0) and elem.get('text'):
            font_px = parse_px(styles.get('fontSize', '16px')) or 16.0
            monospace = 'mono' in styles.get('fontFamily', '').lower()
            line_widths = [
                _estimate_text_width_px(
                    line,
                    font_px,
                    monospace=monospace,
                    letter_spacing=styles.get('letterSpacing', ''),
                )
                for line in elem.get('text', '').split('\n')
                if line
            ]
            if line_widths:
                natural_w = max(line_widths) / PX_PER_IN
        if natural_w and natural_w > 0.0 and natural_w < width:
            width = natural_w
            bounds['width'] = natural_w
    if width <= 0.0 and height <= 0.0:
        return False

    left = parse_px(styles.get('left', '')) / PX_PER_IN if styles.get('left', '').strip() not in ('', 'auto') else None
    right = parse_px(styles.get('right', '')) / PX_PER_IN if styles.get('right', '').strip() not in ('', 'auto') else None
    top = parse_px(styles.get('top', '')) / PX_PER_IN if styles.get('top', '').strip() not in ('', 'auto') else None
    bottom = parse_px(styles.get('bottom', '')) / PX_PER_IN if styles.get('bottom', '').strip() not in ('', 'auto') else None

    if left is None and right is None and top is None and bottom is None:
        return False

    target_x = bounds.get('x', 0.0)
    target_y = bounds.get('y', 0.0)
    if left is not None:
        target_x = left
    elif right is not None:
        target_x = max(slide_w_in - right - width, 0.0)

    if top is not None:
        target_y = top
    elif bottom is not None:
        target_y = max(slide_h_in - bottom - height, 0.0)

    transform = styles.get('transform', '')
    if 'translateX(-50%' in transform:
        target_x -= width / 2.0
    if 'translateY(-50%' in transform:
        target_y -= height / 2.0

    dx = target_x - bounds.get('x', 0.0)
    dy = target_y - bounds.get('y', 0.0)
    if abs(dx) <= 1e-6 and abs(dy) <= 1e-6:
        elem['_skip_layout'] = True
        return True

    _translate_ir_tree(elem, dx, dy)
    elem['_skip_layout'] = True
    return True


def _collect_global_positioned_overlays(
    soup: BeautifulSoup,
    css_rules: List[CSSRule],
    body_style: Dict[str, str],
    slide_width_px: float,
    contract: Optional[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    body_tag = soup.find('body')
    if not body_tag:
        return []

    overlays: List[Dict[str, Any]] = []
    for child in body_tag.children:
        if not isinstance(child, Tag):
            continue
        if _is_slide_root_element(child):
            continue
        child_style = compute_element_style(child, css_rules, child.get('style', ''), body_style)
        if not _is_slide_or_body_anchored_positioned(child, child_style):
            continue
        child_text = get_text_content(child).strip()
        has_direct_tags = any(isinstance(grandchild, Tag) for grandchild in child.children)
        has_drawable_style = _has_drawable_background(child_style) or has_visible_bg_or_border(child_style)
        if not child_text and not has_direct_tags and not has_drawable_style:
            continue
        child_results = flat_extract(
            child,
            css_rules,
            body_style,
            slide_width_px=slide_width_px,
            contract=contract,
        )
        for elem in child_results:
            overlays.append(copy.deepcopy(elem))
    return overlays


def _direct_tag_children(element: Tag) -> List[Tag]:
    return [child for child in element.children if isinstance(child, Tag)]


def _direct_child_matches_selector(parent: Tag, selector: str) -> Optional[Tag]:
    for child in _direct_tag_children(parent):
        if selector_matches(child, selector):
            return child
    return None


def _direct_child_matches_any_selector(parent: Tag, selectors: List[str]) -> Tuple[Optional[Tag], Optional[str]]:
    for selector in selectors or []:
        match = _direct_child_matches_selector(parent, selector)
        if match is not None:
            return match, selector
    return None, None


def _append_inline_style_property(tag: Tag, prop_name: str, value: str) -> None:
    if not value:
        return
    existing = (tag.get('style') or '').strip()
    if existing and not existing.endswith(';'):
        existing += ';'
    tag['style'] = f"{existing} {prop_name}: {value};".strip()


def _match_layout_tier(slide_html: Tag, tier_cfg: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    if not tier_cfg:
        return None

    direct_required = tier_cfg.get('direct_children_all') or []
    direct_any = tier_cfg.get('direct_children_any') or []
    wrapper_selectors = tier_cfg.get('wrapper_selectors') or []
    wrapper_required = tier_cfg.get('wrapper_children_all') or []

    wrapper = None
    matched_wrapper_selector = None
    if wrapper_selectors:
        wrapper, matched_wrapper_selector = _direct_child_matches_any_selector(slide_html, wrapper_selectors)
        if wrapper is None:
            return None

    for selector in direct_required:
        if _direct_child_matches_selector(slide_html, selector) is None:
            return None

    if direct_any and all(_direct_child_matches_selector(slide_html, selector) is None for selector in direct_any):
        return None

    if wrapper_required:
        if wrapper is None:
            return None
        for selector in wrapper_required:
            if _direct_child_matches_selector(wrapper, selector) is None:
                return None

    return {
        'wrapper_selector': matched_wrapper_selector or '',
        'unwrap_wrapper': bool(tier_cfg.get('unwrap_wrapper')),
    }


def _classify_slide_layout(slide_html: Tag, contract: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not contract:
        return {'role': '', 'support_tier': ''}

    layout_contracts = contract.get('layout_contracts') or {}
    hinted_role = (slide_html.get('data-export-role') or '').strip()
    ordered_roles: List[Tuple[str, Dict[str, Any]]] = []
    if hinted_role and hinted_role in layout_contracts:
        ordered_roles.append((hinted_role, layout_contracts[hinted_role]))
    ordered_roles.extend(
        (role_name, cfg)
        for role_name, cfg in layout_contracts.items()
        if role_name != hinted_role
    )

    for role_name, cfg in ordered_roles:
        canonical = _match_layout_tier(slide_html, cfg.get('canonical') or {})
        if canonical:
            return {
                'role': role_name,
                'support_tier': 'canonical',
                **canonical,
            }

        compatible = _match_layout_tier(slide_html, cfg.get('compatible') or {})
        if compatible:
            return {
                'role': role_name,
                'support_tier': 'compatible',
                **compatible,
            }

    support_tiers = contract.get('support_tiers') or {}
    if support_tiers:
        return {'role': '', 'support_tier': 'fallback'}
    return {'role': '', 'support_tier': ''}


def _merge_wrapper_spacing_into_slide(slide_root: Tag, wrapper: Tag, css_rules: List[CSSRule]) -> None:
    slide_style = compute_element_style(slide_root, css_rules, slide_root.get('style', ''))
    wrapper_style = compute_element_style(wrapper, css_rules, wrapper.get('style', ''), slide_style)
    for css_prop, camel_prop in (
        ('padding-top', 'paddingTop'),
        ('padding-right', 'paddingRight'),
        ('padding-bottom', 'paddingBottom'),
        ('padding-left', 'paddingLeft'),
    ):
        wrapper_val = wrapper_style.get(camel_prop, '')
        slide_val = slide_style.get(camel_prop, '')
        if not wrapper_val:
            continue
        if slide_val and parse_px(slide_val) > 0:
            continue
        _append_inline_style_property(slide_root, css_prop, wrapper_val)


def _prepare_slide_content_root(
    slide_html: Tag,
    css_rules: List[CSSRule],
    contract: Optional[Dict[str, Any]],
) -> Tuple[Tag, Dict[str, Any], List[Tag]]:
    layout_info = _classify_slide_layout(slide_html, contract)
    overlay_nodes: List[Tag] = []

    def _collect_slide_anchored_children(root: Tag) -> List[Tag]:
        root_style = compute_element_style(root, css_rules, root.get('style', ''))
        collected: List[Tag] = []
        for child in _direct_tag_children(root):
            child_style = compute_element_style(child, css_rules, child.get('style', ''), root_style)
            if _is_slide_or_body_anchored_positioned(child, child_style):
                collected.append(child)
        return collected

    def _strip_slide_anchored_children(root: Tag) -> Tag:
        root_clone = copy.deepcopy(root)
        root_style = compute_element_style(root_clone, css_rules, root_clone.get('style', ''))
        for child in list(_direct_tag_children(root_clone)):
            child_style = compute_element_style(child, css_rules, child.get('style', ''), root_style)
            if _is_slide_or_body_anchored_positioned(child, child_style):
                child.decompose()
        return root_clone

    if layout_info.get('support_tier') == 'compatible' and layout_info.get('wrapper_selector'):
        slide_clone = copy.deepcopy(slide_html)
        wrapper = _direct_child_matches_selector(slide_clone, layout_info['wrapper_selector'])
        if wrapper is not None and layout_info.get('unwrap_wrapper'):
            _merge_wrapper_spacing_into_slide(slide_clone, wrapper, css_rules)
            wrapper.unwrap()
            overlay_nodes = _collect_slide_anchored_children(slide_html)
            slide_clone = _strip_slide_anchored_children(slide_clone)
            return slide_clone, layout_info, overlay_nodes

    if layout_info.get('support_tier') in {'canonical', 'compatible'}:
        overlay_nodes = _collect_slide_anchored_children(slide_html)
        stripped_root = _strip_slide_anchored_children(slide_html)
        return stripped_root, layout_info, overlay_nodes
    return slide_html, layout_info, overlay_nodes


def _effective_slide_layout_style(
    slide_html: Tag,
    css_rules: List[CSSRule],
    base_style: Dict[str, str],
    contract: Optional[Dict[str, Any]],
) -> Dict[str, str]:
    """Merge preset wrapper layout hints into the slide-level flow style."""
    effective = dict(base_style or {})

    contract_id = (contract or {}).get('contract_id', '')
    if contract_id != 'slide-creator/aurora-mesh':
        return effective

    aurora_wrapper = _direct_child_matches_selector(slide_html, '.aurora-slide')
    if aurora_wrapper is None:
        return effective

    wrapper_style = compute_element_style(
        aurora_wrapper,
        css_rules,
        aurora_wrapper.get('style', ''),
        base_style,
    )
    for key in (
        'justifyContent',
        'justify-content',
        'alignItems',
        'align-items',
        'padding',
        'paddingTop',
        'paddingRight',
        'paddingBottom',
        'paddingLeft',
    ):
        value = wrapper_style.get(key, '')
        if value:
            effective[key] = value

    return effective


def _resolve_box_padding_in(
    style: Dict[str, str],
    basis_w_px: float,
    basis_h_px: float,
    raw_value: str = '',
) -> Tuple[float, float, float, float]:
    return _resolve_box_sides_in(style, 'padding', basis_w_px, basis_h_px, raw_value=raw_value)


def _lookup_matching_css_property(
    element: Optional[Tag],
    css_rules: List[CSSRule],
    property_name: str,
) -> str:
    if element is None or not property_name:
        return ''
    matched_value = ''
    for rule in css_rules:
        if property_name not in rule.properties:
            continue
        if selector_matches(element, rule.selector):
            matched_value = rule.properties[property_name]
    return matched_value


def _resolve_box_sides_in(
    style: Dict[str, str],
    prefix: str,
    basis_w_px: float,
    basis_h_px: float,
    raw_value: str = '',
) -> Tuple[float, float, float, float]:
    raw = (raw_value or style.get(prefix, '') or '').strip()
    if raw:
        tokens = [token for token in _split_css_values(raw) if token]
        if len(tokens) == 1:
            tokens = tokens * 4
        elif len(tokens) == 2:
            tokens = [tokens[0], tokens[1], tokens[0], tokens[1]]
        elif len(tokens) == 3:
            tokens = [tokens[0], tokens[1], tokens[2], tokens[1]]
        elif len(tokens) >= 4:
            tokens = tokens[:4]
        if len(tokens) == 4:
            top_px = _resolve_css_length_with_basis(tokens[0], basis_h_px)
            right_px = _resolve_css_length_with_basis(tokens[1], basis_w_px)
            bottom_px = _resolve_css_length_with_basis(tokens[2], basis_h_px)
            left_px = _resolve_css_length_with_basis(tokens[3], basis_w_px)
            return (
                left_px / PX_PER_IN,
                right_px / PX_PER_IN,
                top_px / PX_PER_IN,
                bottom_px / PX_PER_IN,
            )

    _expand_padding(style)
    top_val = style.get(f'{prefix}Top', '0px')
    right_val = style.get(f'{prefix}Right', '0px')
    bottom_val = style.get(f'{prefix}Bottom', '0px')
    left_val = style.get(f'{prefix}Left', '0px')
    return (
        _resolve_css_length_with_basis(left_val, basis_w_px) / PX_PER_IN,
        _resolve_css_length_with_basis(right_val, basis_w_px) / PX_PER_IN,
        _resolve_css_length_with_basis(top_val, basis_h_px) / PX_PER_IN,
        _resolve_css_length_with_basis(bottom_val, basis_h_px) / PX_PER_IN,
    )


def _resolve_box_margin_in(
    style: Dict[str, str],
    basis_w_px: float,
    basis_h_px: float,
    raw_value: str = '',
) -> Tuple[float, float, float, float]:
    return _resolve_box_sides_in(style, 'margin', basis_w_px, basis_h_px, raw_value=raw_value)


def _extract_border_color(border_value: str) -> str:
    for token in reversed((border_value or '').strip().split()):
        if parse_color(token):
            return token
    return ''


def _extract_border_width_in(style: Dict[str, str], border_key: str) -> float:
    border_value = style.get(border_key, '')
    if not border_value:
        return 0.0
    return parse_px(border_value.split()[0]) / PX_PER_IN


def _hairline_height_in(border_w_px: float) -> float:
    """Return the PPTX shape height (in inches) that visually matches a CSS
    `Npx solid` hairline border.

    PPTX renders any solid-fill rectangle at minimum 1 device pixel, so a
    1px CSS hairline emitted directly as a shape ends up reading thicker
    than the source. For 1-2px source borders we halve the height (with a
    0.5px floor) so the rendered visual approximates the antialiased
    browser hairline. Wider source borders pass through unchanged.
    """
    if border_w_px <= 0:
        return 0.0
    if border_w_px <= 2.0:
        return max(border_w_px * 0.5 / PX_PER_IN, 0.5 / PX_PER_IN)
    return border_w_px / PX_PER_IN


def _build_css_hairline_shape(
    border_value: str,
    x_in: float,
    y_in: float,
    width_in: float,
    fallback_color: str = '#e5e5e5',
) -> Optional[Dict[str, Any]]:
    """Build a thin decoration shape from a CSS border shorthand value.

    Accepts strings like ``"1px solid var(--grid-line)"`` or
    ``"1px solid #e5e5e5"`` and returns a `_is_decoration`/`layoutDone`
    shape sized to render close to the source antialiased hairline. Returns
    None for empty, ``none``, or zero-width borders.
    """
    border_value = (border_value or '').strip()
    if not border_value or 'none' in border_value or border_value.startswith('0'):
        return None
    parts = border_value.split()
    if not parts:
        return None
    border_w_px = parse_px(parts[0])
    if border_w_px <= 0:
        return None
    color = _extract_border_color(border_value) or fallback_color
    line_h_in = _hairline_height_in(border_w_px)
    if line_h_in <= 0 or width_in <= 0:
        return None
    return {
        'type': 'shape',
        'tag': 'div',
        'bounds': {
            'x': x_in,
            'y': y_in,
            'width': width_in,
            'height': line_h_in,
        },
        'styles': {
            'backgroundColor': color,
            'borderRadius': '',
        },
        '_is_decoration': True,
        'layoutDone': True,
    }


def _resolve_flex_basis_in(
    style: Dict[str, str],
    basis_px: float,
    fallback_ratio: float = 0.0,
) -> float:
    candidates = [
        style.get('width', ''),
        style.get('flexBasis', ''),
        style.get('flex-basis', ''),
    ]
    flex_value = (style.get('flex', '') or '').strip()
    if flex_value:
        parts = flex_value.split()
        if len(parts) >= 3:
            candidates.append(parts[2])

    for raw in candidates:
        raw = (raw or '').strip()
        if not raw or raw in {'auto', 'none'}:
            continue
        resolved_px = _resolve_css_length_with_basis(raw, basis_px)
        if resolved_px > 0:
            return resolved_px / PX_PER_IN

    if fallback_ratio > 0 and basis_px > 0:
        return (basis_px / PX_PER_IN) * fallback_ratio
    return 0.0


def _style_has_explicit_width_signal(style: Dict[str, str]) -> bool:
    for key in ('width', 'minWidth', 'min-width', 'maxWidth', 'max-width', 'flexBasis', 'flex-basis'):
        raw = (style.get(key, '') or '').strip()
        if raw and raw not in {'auto', 'none', 'fit-content', 'min-content', 'max-content'}:
            return True

    flex_value = (style.get('flex', '') or '').strip()
    if not flex_value:
        return False

    parts = flex_value.split()
    if len(parts) >= 3 and parts[2] not in {'auto', 'none'}:
        return True
    return False


def _style_flex_grow_value(style: Dict[str, str]) -> float:
    for key in ('flexGrow', 'flex-grow'):
        raw = (style.get(key, '') or '').strip()
        if not raw:
            continue
        try:
            return float(raw)
        except ValueError:
            continue

    flex_value = (style.get('flex', '') or '').strip()
    if flex_value:
        first = flex_value.split()[0]
        try:
            return float(first)
        except ValueError:
            return 0.0
    return 0.0


def _contract_vertical_card_prefers_stretch_width(style: Dict[str, str]) -> bool:
    if _style_flex_grow_value(style) > 0.0:
        return True
    return _style_has_explicit_width_signal(style)


def _measure_contract_vertical_card_intrinsic_width_in(
    element: Tag,
    style: Dict[str, str],
    css_rules: List[CSSRule],
    slide_width_px: float,
    max_width_in: float,
    slot_model: Dict[str, Any],
) -> float:
    """Measure a compact vertical-card width unless CSS explicitly asks it to stretch."""
    direct_children = [child for child in element.children if isinstance(child, Tag)]
    if not direct_children:
        return 0.0

    _expand_padding(style)
    pad_l = parse_px(style.get('paddingLeft', '0px')) / PX_PER_IN
    pad_r = parse_px(style.get('paddingRight', '0px')) / PX_PER_IN
    border_l = _extract_border_width_in(style, 'borderLeft')
    border_r = _extract_border_width_in(style, 'borderRight')
    inner_cap_in = max(max_width_in - pad_l - pad_r - border_l - border_r, 0.3)
    inner_cap_px = inner_cap_in * PX_PER_IN
    max_child_w = 0.0

    for idx, child in enumerate(direct_children):
        child_style = compute_element_style(child, css_rules, child.get('style', ''), style)
        child_classes = _element_classes(child)
        child_text = get_text_content(child).strip()
        metric_like = bool(
            child_classes.intersection({'ds-kpi', 'feat-stat', 'sol-icon'}) or
            (
                idx == 0 and
                slot_model.get('metric_single_line') and
                _looks_like_metric_token(child_text)
            )
        )

        child_w = 0.0
        if child.name == 'svg':
            child_el = build_svg_container(
                child,
                css_rules,
                style,
                slide_width_px,
                inner_cap_px,
            )
            if child_el:
                child_w = child_el.get('bounds', {}).get('width', 0.0)
        elif child.name in TEXT_TAGS or child_text:
            if metric_like:
                child_el = build_text_element(
                    child,
                    child_style,
                    css_rules,
                    slide_width_px,
                    None,
                )
                if child_el and child_el.get('type') == 'text':
                    child_w = child_el.get('bounds', {}).get('width', 0.0)
            else:
                child_w = compute_text_content_width(child, css_rules, style)
                if child_w <= 0.0:
                    child_el = build_text_element(
                        child,
                        child_style,
                        css_rules,
                        slide_width_px,
                        inner_cap_px,
                    )
                    if child_el:
                        child_w = child_el.get('bounds', {}).get('width', 0.0)
        elif is_leaf_text_container(child, css_rules):
            child_w = compute_text_content_width(child, css_rules, style)
        elif (
            child.name in CONTAINER_TAGS and
            (has_visible_bg_or_border(child_style) or child_style.get('backgroundImage', 'none') != 'none')
        ):
            explicit_w = _resolve_css_length_with_basis(child_style.get('width', ''), inner_cap_px)
            if explicit_w <= 0:
                explicit_w = _resolve_css_length_with_basis(child_style.get('maxWidth', ''), inner_cap_px)
            if explicit_w > 0:
                child_w = explicit_w / PX_PER_IN

        if child_w > 0.0:
            max_child_w = max(max_child_w, min(child_w, inner_cap_in))

    measured = max(max_child_w + pad_l + pad_r + border_l + border_r, 0.5)

    min_w = _resolve_css_length_with_basis(
        style.get('minWidth', style.get('min-width', '')),
        max_width_in * PX_PER_IN,
    )
    if min_w > 0:
        measured = max(measured, min_w / PX_PER_IN)

    max_w = _resolve_css_length_with_basis(
        style.get('maxWidth', style.get('max-width', '')),
        max_width_in * PX_PER_IN,
    )
    if max_w > 0:
        measured = min(measured, max_w / PX_PER_IN)

    return min(measured, max_width_in)


def _coerce_relative_container(
    element: Tag,
    style: Dict[str, str],
    built: List[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    if not built:
        return None
    if len(built) == 1 and built[0].get('type') == 'container' and built[0].get('_children_relative'):
        return built[0]
    return _pack_relative_block_container(element, style, built)


def _build_rule_shape_from_node(
    element: Tag,
    style: Dict[str, str],
    slide_width_px: float,
    width_basis_px: float,
) -> Optional[Dict[str, Any]]:
    width_px = _resolve_css_length_with_basis(style.get('width', ''), width_basis_px)
    height_px = _resolve_css_length_with_basis(style.get('height', ''), VIEWPORT_HEIGHT_PX)
    if height_px <= 0:
        height_px = parse_px(style.get('borderTop', '').split()[0] if style.get('borderTop', '') else '0px')
    if width_px <= 0 or height_px <= 0:
        return None

    shape = build_shape_element(element, style, slide_width_px)
    shape['bounds'] = {
        'x': 0.0,
        'y': 0.0,
        'width': max(width_px / PX_PER_IN, 0.04),
        'height': max(height_px / PX_PER_IN, 0.01),
    }
    bg_color = style.get('backgroundColor', '')
    if not bg_color:
        bg_color = _extract_border_color(style.get('borderTop', '') or style.get('borderBottom', ''))
    if bg_color:
        shape['styles']['backgroundColor'] = bg_color
    shape['_is_decoration'] = True
    return shape


def _build_packed_child_container(
    node: Tag,
    css_rules: List[CSSRule],
    parent_style: Dict[str, str],
    slide_width_px: float,
    content_width_px: float,
    contract: Optional[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    node_style = compute_element_style(node, css_rules, node.get('style', ''), parent_style)
    built = flat_extract(
        node,
        css_rules,
        parent_style,
        slide_width_px,
        content_width_px=content_width_px,
        local_origin=True,
        contract=contract,
    )
    return _coerce_relative_container(node, node_style, built)


def _pack_direct_child_content(
    node: Tag,
    css_rules: List[CSSRule],
    parent_style: Dict[str, str],
    slide_width_px: float,
    content_width_px: float,
    contract: Optional[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    node_style = compute_element_style(node, css_rules, node.get('style', ''), parent_style)
    packed_children: List[Dict[str, Any]] = []
    for child in _direct_tag_children(node):
        child_style = compute_element_style(child, css_rules, child.get('style', ''), node_style)
        # Skip absolute-positioned children: they should not contribute to the
        # packed container's width. Callers (e.g. column_content builder) are
        # expected to harvest decoration strips separately.
        if child_style.get('position', '').strip() in ('absolute', 'fixed'):
            continue
        built = flat_extract(
            child,
            css_rules,
            node_style,
            slide_width_px,
            content_width_px=content_width_px,
            local_origin=True,
            contract=contract,
        )
        if not built and child.name.lower() == 'hr':
            rule_shape = _build_rule_shape_from_node(child, child_style, slide_width_px, content_width_px or slide_width_px)
            if rule_shape:
                built = [rule_shape]
        if built:
            packed_children.extend(built)
    return _coerce_relative_container(node, node_style, packed_children)


_COLUMN_BLOCK_TEXT_TAGS = frozenset({'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p'})


def _stretch_column_block_text_to_inner_width(
    container: Dict[str, Any],
    inner_width_in: float,
) -> None:
    """Force block-level headings/paragraphs in a column panel to claim the
    full inner panel width.

    Without this, `flat_extract` shrink-wraps a heading to its natural text
    width (e.g. 2.08"), and any authored `<br>` line that is itself slightly
    wider than the shrunk frame wraps again, producing orphaned half-rows
    instead of the two clean lines the source intended.
    """
    if not container or inner_width_in <= 0:
        return
    children = container.get('children') or []
    for child in children:
        if not isinstance(child, dict):
            continue
        if child.get('type') != 'text':
            continue
        if child.get('tag') not in _COLUMN_BLOCK_TEXT_TAGS:
            continue
        bounds = child.get('bounds')
        if not bounds:
            continue
        if bounds.get('width', 0.0) >= inner_width_in - 0.01:
            continue
        bounds['width'] = inner_width_in


def _build_swiss_column_content(
    slide_root: Tag,
    css_rules: List[CSSRule],
    slide_width_px: float,
    slide_height_px: float,
    contract: Optional[Dict[str, Any]],
    layout_info: Dict[str, Any],
) -> Optional[List[Dict[str, Any]]]:
    left_node = _direct_child_matches_selector(slide_root, '.left-panel') or _direct_child_matches_selector(slide_root, '.left-col')
    right_node = _direct_child_matches_selector(slide_root, '.right-panel') or _direct_child_matches_selector(slide_root, '.right-col')
    if left_node is None or right_node is None:
        return None

    slide_style = compute_element_style(slide_root, css_rules, slide_root.get('style', ''))
    left_style = compute_element_style(left_node, css_rules, left_node.get('style', ''), slide_style)
    right_style = compute_element_style(right_node, css_rules, right_node.get('style', ''), slide_style)
    slide_w_in = slide_width_px / PX_PER_IN
    slide_h_in = slide_height_px / PX_PER_IN
    slide_pad_l, slide_pad_r, slide_pad_t, slide_pad_b = _resolve_box_padding_in(slide_style, slide_width_px, slide_height_px)
    content_w_in = max(slide_w_in - slide_pad_l - slide_pad_r, 0.8)
    content_h_in = max(slide_h_in - slide_pad_t - slide_pad_b, 0.8)
    tier = (layout_info.get('support_tier') or '').strip()

    left_fallback_ratio = 0.38 if 'left-panel' in _element_classes(left_node) else 0.40
    left_w_in = _resolve_flex_basis_in(left_style, content_w_in * PX_PER_IN, fallback_ratio=left_fallback_ratio)
    if left_w_in <= 0:
        left_w_in = content_w_in * left_fallback_ratio
    left_w_in = min(max(left_w_in, content_w_in * 0.22), content_w_in - 0.6)
    right_w_in = max(content_w_in - left_w_in, 0.6)

    left_pad_l, left_pad_r, left_pad_t, left_pad_b = _resolve_box_padding_in(left_style, left_w_in * PX_PER_IN, content_h_in * PX_PER_IN)
    left_border_l = _extract_border_width_in(left_style, 'borderLeft')
    left_inner_w_px = max((left_w_in - left_pad_l - left_pad_r - left_border_l) * PX_PER_IN, 120.0)
    left_content = _pack_direct_child_content(
        left_node,
        css_rules,
        slide_style,
        slide_width_px,
        left_inner_w_px,
        contract,
    )
    if left_content is not None:
        # Block-level headings/paragraphs in a column panel must claim the full
        # inner panel width so authored line breaks survive — otherwise the
        # text element shrink-wraps to its natural width and the wrap engine
        # turns each authored line into orphaned half-rows.
        _stretch_column_block_text_to_inner_width(
            left_content,
            max(left_w_in - left_pad_l - left_pad_r - left_border_l, 0.6),
        )
    right_container = _build_packed_child_container(
        right_node,
        css_rules,
        slide_style,
        slide_width_px,
        right_w_in * PX_PER_IN,
        contract,
    )
    if left_content is None or right_container is None:
        return None

    root_h_in = content_h_in if tier == 'canonical' else max(
        left_content.get('bounds', {}).get('height', 0.0),
        right_container.get('bounds', {}).get('height', 0.0),
    )
    root_h_in = max(root_h_in, 0.4)
    root_y_in = slide_pad_t if tier == 'canonical' else slide_pad_t + max((content_h_in - root_h_in) / 2.0, 0.0)
    root = {
        'type': 'container',
        'tag': slide_root.name,
        'bounds': {'x': slide_pad_l, 'y': root_y_in, 'width': content_w_in, 'height': root_h_in},
        'styles': slide_style,
        'children': [],
        '_children_relative': True,
        'layoutDone': True,
        '_component_contract': 'swiss_column_content',
    }

    if left_style.get('backgroundColor', ''):
        bg_shape = build_shape_element(left_node, left_style, slide_width_px)
        bg_shape['bounds'] = {'x': 0.0, 'y': 0.0, 'width': left_w_in, 'height': root_h_in}
        bg_shape['_is_decoration'] = True
        root['children'].append(bg_shape)

    left_content_y = 0.0
    if tier == 'canonical':
        inner_h = max(root_h_in - left_pad_t - left_pad_b, 0.2)
        left_content_y = left_pad_t + max((inner_h - left_content['bounds'].get('height', 0.0)) / 2.0, 0.0)
    else:
        left_content_y = max((root_h_in - left_content['bounds'].get('height', 0.0)) / 2.0, 0.0)
    left_content['bounds']['x'] = left_pad_l + left_border_l
    left_content['bounds']['y'] = left_content_y
    root['children'].append(left_content)

    # Swiss canonical right-panel CSS uses justify-content: center (vertical
    # centering inside the column). Earlier this branch hard-coded right_y=0
    # for canonical tier, which pushed every right-panel content to the top.
    # Mirror the left-panel behavior and center the right column too.
    right_y = max((root_h_in - right_container['bounds'].get('height', 0.0)) / 2.0, 0.0)
    right_container['bounds']['x'] = left_w_in
    right_container['bounds']['y'] = right_y
    root['children'].append(right_container)

    # Harvest absolute-positioned decoration strips inside each panel
    # (e.g. .red-bar). They were skipped by _pack_direct_child_content so
    # they would not pollute the panel's content width.
    for panel_node, panel_w_in, panel_x_in in (
        (left_node, left_w_in, 0.0),
        (right_node, right_w_in, left_w_in),
    ):
        for strip in _build_absolute_decoration_strips(
            panel_node, css_rules, slide_style, panel_w_in, root_h_in
        ):
            strip['bounds']['x'] += panel_x_in
            root['children'].append(strip)
    return [root]


def _build_absolute_decoration_strips(
    panel_node: Tag,
    css_rules: List[CSSRule],
    parent_style: Dict[str, str],
    panel_w_in: float,
    panel_h_in: float,
) -> List[Dict[str, Any]]:
    panel_style = compute_element_style(panel_node, css_rules, panel_node.get('style', ''), parent_style)
    strips: List[Dict[str, Any]] = []
    for child in _direct_tag_children(panel_node):
        cs = compute_element_style(child, css_rules, child.get('style', ''), panel_style)
        if cs.get('position', '').strip() not in ('absolute', 'fixed'):
            continue
        bg = cs.get('backgroundColor', '').strip()
        if not bg or bg in ('transparent', 'rgba(0, 0, 0, 0)'):
            continue
        text_inside = (child.get_text(strip=True) or '').strip()
        if text_inside:
            continue  # only handle pure decoration strips
        def _side(name: str) -> Optional[float]:
            raw = cs.get(name, '').strip()
            if not raw or raw == 'auto':
                return None
            return parse_px(raw) / PX_PER_IN
        left_in, right_in = _side('left'), _side('right')
        top_in, bottom_in = _side('top'), _side('bottom')
        w_raw = cs.get('width', '').strip()
        h_raw = cs.get('height', '').strip()
        explicit_w = parse_px(w_raw) / PX_PER_IN if w_raw and 'px' in w_raw else None
        explicit_h = parse_px(h_raw) / PX_PER_IN if h_raw and 'px' in h_raw else None
        # width: explicit > (left & right) > skip
        if explicit_w is not None:
            w = explicit_w
        elif left_in is not None and right_in is not None:
            w = max(panel_w_in - left_in - right_in, 0.0)
        else:
            continue
        # height: explicit > (top & bottom) > skip
        if explicit_h is not None:
            h = explicit_h
        elif top_in is not None and bottom_in is not None:
            h = max(panel_h_in - top_in - bottom_in, 0.0)
        else:
            continue
        if w <= 0 or h <= 0:
            continue
        x = left_in if left_in is not None else max(panel_w_in - (right_in or 0.0) - w, 0.0)
        y = top_in if top_in is not None else max(panel_h_in - (bottom_in or 0.0) - h, 0.0)
        shape = build_shape_element(child, cs, panel_w_in * PX_PER_IN)
        shape['bounds'] = {'x': x, 'y': y, 'width': w, 'height': h}
        shape['_is_decoration'] = True
        strips.append(shape)
    return strips


def _build_swiss_stat_block(
    slide_root: Tag,
    css_rules: List[CSSRule],
    slide_width_px: float,
    slide_height_px: float,
    contract: Optional[Dict[str, Any]],
    layout_info: Dict[str, Any],
) -> Optional[List[Dict[str, Any]]]:
    tier = (layout_info.get('support_tier') or '').strip()
    slide_style = compute_element_style(slide_root, css_rules, slide_root.get('style', ''))
    slide_w_in = slide_width_px / PX_PER_IN
    slide_h_in = slide_height_px / PX_PER_IN
    slide_pad_l, slide_pad_r, slide_pad_t, slide_pad_b = _resolve_box_padding_in(slide_style, slide_width_px, slide_height_px)
    content_w_in = max(slide_w_in - slide_pad_l - slide_pad_r, 0.8)
    content_h_in = max(slide_h_in - slide_pad_t - slide_pad_b, 0.8)

    metric_node: Optional[Tag] = None
    copy_node: Optional[Tag] = None
    divider_node: Optional[Tag] = None
    row_style = slide_style
    row_w_in = content_w_in
    row_gap_in = 0.0

    row_node = _direct_child_matches_selector(slide_root, '.stat-row')
    if row_node is not None:
        row_style = compute_element_style(row_node, css_rules, row_node.get('style', ''), slide_style)
        metric_node = _direct_child_matches_selector(row_node, '.stat-metric')
        divider_node = _direct_child_matches_selector(row_node, '.stat-divider')
        copy_node = _direct_child_matches_selector(row_node, '.stat-copy')
        row_w_raw = row_style.get('width', '') or row_style.get('maxWidth', '')
        if row_w_raw:
            resolved = _resolve_css_length_with_basis(row_w_raw, slide_width_px)
            if resolved > 0:
                row_w_in = min(resolved / PX_PER_IN, content_w_in)
        row_gap_in = _resolve_css_length_with_basis(row_style.get('gap', '0px'), row_w_in * PX_PER_IN) / PX_PER_IN
    else:
        metric_node = _direct_child_matches_selector(slide_root, '.stat-block')
        copy_node = _direct_child_matches_selector(slide_root, '.content-block')
    if metric_node is None or copy_node is None:
        return None

    metric_style = compute_element_style(metric_node, css_rules, metric_node.get('style', ''), row_style)
    copy_style = compute_element_style(copy_node, css_rules, copy_node.get('style', ''), row_style)
    metric_fallback_ratio = 0.40 if metric_node and 'stat-metric' in _element_classes(metric_node) else 0.50
    metric_w_in = _resolve_flex_basis_in(metric_style, row_w_in * PX_PER_IN, fallback_ratio=metric_fallback_ratio)
    if metric_w_in <= 0:
        metric_w_in = row_w_in * metric_fallback_ratio
    metric_w_in = min(max(metric_w_in, row_w_in * 0.24), row_w_in - 0.8)

    divider_w_in = 0.0
    divider_color = ''
    if divider_node is not None:
        divider_style = compute_element_style(divider_node, css_rules, divider_node.get('style', ''), row_style)
        divider_w_in = max(
            _resolve_css_length_with_basis(divider_style.get('width', ''), row_w_in * PX_PER_IN) / PX_PER_IN,
            2.0 / PX_PER_IN,
        )
        divider_color = divider_style.get('backgroundColor', '') or _extract_border_color(divider_style.get('borderLeft', ''))
    else:
        divider_w_in = _extract_border_width_in(copy_style, 'borderLeft')
        divider_color = _extract_border_color(copy_style.get('borderLeft', '')) or copy_style.get('color', '')

    copy_pad_l, _, _, _ = _resolve_box_padding_in(copy_style, row_w_in * PX_PER_IN, content_h_in * PX_PER_IN)
    gap_budget_in = row_gap_in * 2.0 if (tier == 'canonical' and divider_node is not None) else row_gap_in
    copy_inner_w_in = max(row_w_in - metric_w_in - divider_w_in - gap_budget_in - copy_pad_l, 0.6)
    metric_container = _pack_direct_child_content(
        metric_node,
        css_rules,
        row_style,
        slide_width_px,
        max(metric_w_in * PX_PER_IN, 120.0),
        contract,
    )
    copy_container = _pack_direct_child_content(
        copy_node,
        css_rules,
        row_style,
        slide_width_px,
        max(copy_inner_w_in * PX_PER_IN, 180.0),
        contract,
    )
    if metric_container is None or copy_container is None:
        return None

    row_h_in = max(metric_container['bounds'].get('height', 0.0), copy_container['bounds'].get('height', 0.0), 0.4)
    row_y_in = slide_pad_t + max((content_h_in - row_h_in) / 2.0, 0.0)
    row_x_in = slide_pad_l + max((content_w_in - row_w_in) / 2.0, 0.0)
    root = {
        'type': 'container',
        'tag': slide_root.name,
        'bounds': {'x': row_x_in, 'y': row_y_in, 'width': row_w_in, 'height': row_h_in},
        'styles': row_style,
        'children': [],
        '_children_relative': True,
        'layoutDone': True,
        '_component_contract': 'swiss_stat_block',
    }

    metric_container['bounds']['x'] = 0.0
    metric_container['bounds']['y'] = max((row_h_in - metric_container['bounds'].get('height', 0.0)) / 2.0, 0.0)
    root['children'].append(metric_container)

    current_x = metric_w_in
    if tier == 'canonical' and divider_node is not None and row_gap_in > 0:
        current_x += row_gap_in
    if divider_w_in > 0 and divider_color:
        divider_shape = {
            'type': 'shape',
            'tag': divider_node.name if divider_node is not None else 'div',
            'bounds': {
                'x': current_x,
                'y': 0.0,
                'width': max(divider_w_in, 2.0 / PX_PER_IN),
                'height': row_h_in,
            },
            'styles': {
                'backgroundColor': divider_color,
                'backgroundImage': '',
                'border': '',
                'borderLeft': '',
                'borderRight': '',
                'borderTop': '',
                'borderBottom': '',
                'borderRadius': '0px',
                'marginTop': '',
                'marginBottom': '',
                'marginLeft': '',
                'marginRight': '',
            },
            '_is_decoration': True,
        }
        root['children'].append(divider_shape)
        current_x += divider_w_in
    if tier == 'canonical' and divider_node is not None and row_gap_in > 0:
        current_x += row_gap_in
    copy_container['bounds']['x'] = current_x + copy_pad_l
    copy_container['bounds']['y'] = max((row_h_in - copy_container['bounds'].get('height', 0.0)) / 2.0, 0.0)
    root['children'].append(copy_container)
    return [root]


def _build_swiss_title_grid(
    slide_root: Tag,
    css_rules: List[CSSRule],
    slide_width_px: float,
    slide_height_px: float,
    contract: Optional[Dict[str, Any]],
    layout_info: Dict[str, Any],
) -> Optional[List[Dict[str, Any]]]:
    slide_style = compute_element_style(slide_root, css_rules, slide_root.get('style', ''))
    slide_w_in = slide_width_px / PX_PER_IN
    slide_h_in = slide_height_px / PX_PER_IN
    slide_pad_l, slide_pad_r, slide_pad_t, slide_pad_b = _resolve_box_padding_in(slide_style, slide_width_px, slide_height_px)
    content_h_in = max(slide_h_in - slide_pad_t - slide_pad_b, 0.8)

    # Accept the Swiss canonical *-inner panels that share the "single
    # vertically-stacked inner content panel" geometry. Slides whose inner
    # panel is left-aligned list content (sol / cta / inst) keep going
    # through the generic flat_extract path — title_grid's vertical
    # centering + content packing was empirically worse for them.
    hero_node, _matched_inner_selector = _direct_child_matches_any_selector(
        slide_root,
        ['.hero-inner', '.flow-inner', '.feat-inner', '.cta-inner'],
    )
    hero_style = slide_style
    content_node = slide_root
    content_width_px = max((slide_w_in - slide_pad_l - slide_pad_r) * PX_PER_IN, 180.0)
    content_x_in = slide_pad_l
    bottom_in = slide_pad_b
    top_in = slide_pad_t

    # Resolve justify-content from the inner panel first when present (e.g.
    # `.flow-inner { justify-content: center }`); fall back to slide root
    # for cases like `#slide-1 { justify-content: flex-end }` where the
    # whole slide drives vertical alignment.
    justify = ''
    if hero_node is not None:
        _hero_style_probe = compute_element_style(hero_node, css_rules, hero_node.get('style', ''), slide_style)
        justify = (_hero_style_probe.get('justifyContent') or _hero_style_probe.get('justify-content') or '').strip()
    if not justify:
        justify = (slide_style.get('justifyContent') or slide_style.get('justify-content') or '').strip()

    if hero_node is not None:
        hero_style = compute_element_style(hero_node, css_rules, hero_node.get('style', ''), slide_style)
        hero_width_raw = hero_style.get('width', '') or hero_style.get('maxWidth', '')
        if hero_width_raw:
            resolved_width = _resolve_css_length_with_basis(hero_width_raw, slide_width_px)
            if resolved_width > 0:
                content_width_px = resolved_width

        raw_padding = hero_style.get('padding', '') or _lookup_matching_css_property(hero_node, css_rules, 'padding')
        hero_pad_l, hero_pad_r, hero_pad_t, hero_pad_b = _resolve_box_padding_in(
            hero_style,
            content_width_px,
            slide_height_px,
            raw_value=raw_padding,
        )
        content_width_px = max(content_width_px - (hero_pad_l + hero_pad_r) * PX_PER_IN, 180.0)
        content_x_in = max(hero_pad_l, slide_pad_l)
        bottom_in = hero_pad_b if hero_pad_b > 0 else slide_pad_b
        top_in = hero_pad_t if hero_pad_t > 0 else slide_pad_t
        content_node = hero_node

    packed = _pack_direct_child_content(
        content_node,
        css_rules,
        hero_style if hero_node is not None else slide_style,
        slide_width_px,
        content_width_px,
        contract,
    )
    if packed is None:
        return None

    content_y_in = top_in
    if justify == 'flex-end':
        content_y_in = max(slide_h_in - bottom_in - packed['bounds'].get('height', 0.0), top_in)
    elif justify == 'center':
        content_y_in = top_in + max((content_h_in - packed['bounds'].get('height', 0.0)) / 2.0, 0.0)

    root = {
        'type': 'container',
        'tag': slide_root.name,
        'bounds': {'x': 0.0, 'y': 0.0, 'width': slide_w_in, 'height': slide_h_in},
        'styles': slide_style,
        'children': [],
        '_children_relative': True,
        'layoutDone': True,
        '_component_contract': 'swiss_title_grid',
    }
    packed['bounds']['x'] = content_x_in
    packed['bounds']['y'] = content_y_in
    # Lock the entire packed subtree so the downstream layout pass cannot
    # re-center compact-width container children (e.g. `.cta-echo` packed at
    # ~2.5" was being centered horizontally on the slide).
    def _freeze_layout(node: Dict[str, Any]) -> None:
        if not isinstance(node, dict):
            return
        node.setdefault('layoutDone', True)
        for child in node.get('children', []) or []:
            _freeze_layout(child)
    _freeze_layout(packed)
    root['children'].append(packed)
    return [root]


def _build_swiss_pull_quote(
    slide_root: Tag,
    css_rules: List[CSSRule],
    slide_width_px: float,
    slide_height_px: float,
    contract: Optional[Dict[str, Any]],
    layout_info: Dict[str, Any],
) -> Optional[List[Dict[str, Any]]]:
    slide_style = compute_element_style(slide_root, css_rules, slide_root.get('style', ''))
    slide_w_in = slide_width_px / PX_PER_IN
    slide_h_in = slide_height_px / PX_PER_IN
    slide_pad_l, slide_pad_r, slide_pad_t, slide_pad_b = _resolve_box_padding_in(slide_style, slide_width_px, slide_height_px)
    content_w_px = max((slide_w_in - slide_pad_l - slide_pad_r) * PX_PER_IN, 200.0)
    content_h_in = max(slide_h_in - slide_pad_t - slide_pad_b, 0.8)
    justify = (slide_style.get('justifyContent') or slide_style.get('justify-content') or '').strip()

    quote_node = _direct_child_matches_selector(slide_root, '.pull-quote') or _direct_child_matches_selector(slide_root, '.quote-block')
    if quote_node is None:
        return None
    quote_style = compute_element_style(quote_node, css_rules, quote_node.get('style', ''), slide_style)
    quote_w_in = 0.0
    for raw_width in (quote_style.get('width', ''), quote_style.get('maxWidth', '')):
        raw_width = (raw_width or '').strip()
        if not raw_width:
            continue
        resolved_width = _resolve_css_length_with_basis(raw_width, content_w_px)
        if resolved_width > 0:
            quote_w_in = resolved_width / PX_PER_IN
            break
    if quote_w_in <= 0:
        quote_w_in = (content_w_px / PX_PER_IN) * (0.60 if 'pull-quote' in _element_classes(quote_node) else 0.70)
    quote_w_in = min(max(quote_w_in, 2.5), content_w_px / PX_PER_IN)

    packed = _pack_direct_child_content(
        quote_node,
        css_rules,
        quote_style,
        slide_width_px,
        quote_w_in * PX_PER_IN,
        contract,
    )
    if packed is None:
        return None

    raw_margin = quote_style.get('margin', '') or _lookup_matching_css_property(quote_node, css_rules, 'margin')
    quote_margin_l, _, quote_margin_t, _ = _resolve_box_margin_in(
        quote_style,
        slide_width_px,
        slide_height_px,
        raw_value=raw_margin,
    )
    content_x_in = quote_margin_l if quote_margin_l > 0 else slide_pad_l
    content_y_in = quote_margin_t if quote_margin_t > 0 else slide_pad_t
    if justify == 'center' and quote_margin_t <= 0:
        content_y_in = slide_pad_t + max((content_h_in - packed['bounds'].get('height', 0.0)) / 2.0, 0.0)

    root = {
        'type': 'container',
        'tag': slide_root.name,
        'bounds': {'x': 0.0, 'y': 0.0, 'width': slide_w_in, 'height': slide_h_in},
        'styles': slide_style,
        'children': [],
        '_children_relative': True,
        'layoutDone': True,
        '_component_contract': 'swiss_pull_quote',
    }
    packed['bounds']['x'] = content_x_in
    packed['bounds']['y'] = content_y_in
    root['children'].append(packed)
    return [root]


def _build_swiss_index_list_rows(
    list_node: Tag,
    css_rules: List[CSSRule],
    slide_width_px: float,
    inner_w_in: float,
    contract: Optional[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Lay out `.sol-list` as full-width rows with [number left | content right]."""
    list_style = compute_element_style(list_node, css_rules, list_node.get('style', ''))
    list_gap_in = max(_get_gap_px(list_style) / PX_PER_IN, 2.0 / PX_PER_IN)

    rows: List[Dict[str, Any]] = []
    current_y = 0.0

    for item in _direct_tag_children(list_node):
        if 'index-item' not in _element_classes(item):
            continue
        item_style = compute_element_style(item, css_rules, item.get('style', ''), list_style)

        raw_pad = item_style.get('padding', '') or _lookup_matching_css_property(item, css_rules, 'padding')
        pad_l, pad_r, pad_t, pad_b = _resolve_box_padding_in(
            item_style, inner_w_in * PX_PER_IN, 600.0, raw_value=raw_pad,
        )

        item_kids = _direct_tag_children(item)
        num_node = next((c for c in item_kids if 'index-num' in _element_classes(c)), None)
        content_node = next((c for c in item_kids if c is not num_node), None)
        if num_node is None or content_node is None:
            continue

        num_style = compute_element_style(num_node, css_rules, num_node.get('style', ''), item_style)
        gap_in = max(_get_gap_px(item_style) / PX_PER_IN, 0.10)

        # Number column: respect min-width
        min_w_raw = num_style.get('minWidth', num_style.get('min-width', '')) or ''
        num_col_w_in = 0.0
        if min_w_raw:
            num_col_w_in = _resolve_css_length_with_basis(min_w_raw, inner_w_in * PX_PER_IN) / PX_PER_IN
        if num_col_w_in <= 0:
            num_col_w_in = 0.75

        num_el = build_text_element(num_node, num_style, css_rules, slide_width_px, num_col_w_in * PX_PER_IN)

        # Content column gets the rest of the row
        content_x = pad_l + num_col_w_in + gap_in
        content_w_in = max(inner_w_in - content_x - pad_r, 0.5)
        content_style = compute_element_style(content_node, css_rules, content_node.get('style', ''), item_style)
        content_el = build_text_element(content_node, content_style, css_rules, slide_width_px, content_w_in * PX_PER_IN)

        if num_el is None or content_el is None:
            continue

        num_h = num_el['bounds'].get('height', 0.0)
        content_h = content_el['bounds'].get('height', 0.0)
        # Baseline-align: drop the smaller element so its baseline matches the larger.
        # For simplicity, top-align both at y=pad_t but anchor by the bigger of the two.
        # The visual effect of CSS `align-items: baseline` is approximated by pinning
        # the content's first line to sit on the number's baseline.
        num_font_px = parse_px(num_style.get('fontSize', '48px')) or 48.0
        content_font_px = parse_px(content_style.get('fontSize', '24px')) or 24.0
        num_baseline = num_h * 0.82  # approx baseline within line box
        content_baseline = content_font_px / PX_PER_IN * 0.82
        baseline_offset = max(num_baseline - content_baseline, 0.0)

        num_el['bounds']['x'] = pad_l
        num_el['bounds']['y'] = current_y + pad_t
        num_el['bounds']['width'] = num_col_w_in

        content_el['bounds']['x'] = content_x
        content_el['bounds']['y'] = current_y + pad_t + baseline_offset
        content_el['bounds']['width'] = content_w_in

        rows.append(num_el)
        rows.append(content_el)

        row_h = max(num_h, baseline_offset + content_h) + pad_t + pad_b

        # Border-bottom hairline spanning the full inner width.
        hairline = _build_css_hairline_shape(
            item_style.get('borderBottom', ''),
            x_in=0.0,
            y_in=current_y + row_h,
            width_in=inner_w_in,
        )
        if hairline is not None:
            # Anchor the line at the row's bottom edge.
            hairline['bounds']['y'] = current_y + row_h - hairline['bounds']['height']
            rows.append(hairline)

        current_y += row_h + list_gap_in

    return rows


def _build_swiss_index_list(
    slide_root: Tag,
    css_rules: List[CSSRule],
    slide_width_px: float,
    slide_height_px: float,
    contract: Optional[Dict[str, Any]],
    layout_info: Dict[str, Any],
) -> Optional[List[Dict[str, Any]]]:
    """Builder for `.sol-inner` slides: vertically-centered eyebrow / h2 / rule
    plus a full-width `.sol-list` of indexed rows."""
    inner_node, _ = _direct_child_matches_any_selector(slide_root, ['.sol-inner'])
    if inner_node is None:
        return None

    slide_style = compute_element_style(slide_root, css_rules, slide_root.get('style', ''))
    slide_w_in = slide_width_px / PX_PER_IN
    slide_h_in = slide_height_px / PX_PER_IN
    slide_pad_l, slide_pad_r, slide_pad_t, slide_pad_b = _resolve_box_padding_in(
        slide_style, slide_width_px, slide_height_px,
    )
    content_h_in = max(slide_h_in - slide_pad_t - slide_pad_b, 0.8)

    inner_style = compute_element_style(inner_node, css_rules, inner_node.get('style', ''), slide_style)
    raw_padding = inner_style.get('padding', '') or _lookup_matching_css_property(inner_node, css_rules, 'padding')
    inner_pad_l, inner_pad_r, inner_pad_t, inner_pad_b = _resolve_box_padding_in(
        inner_style, slide_width_px, slide_height_px, raw_value=raw_padding,
    )

    content_x_in = max(slide_pad_l, inner_pad_l)
    content_w_in = max(slide_w_in - content_x_in - max(slide_pad_r, inner_pad_r), 1.0)
    inner_w_px = content_w_in * PX_PER_IN

    inner_gap_in = max(_get_gap_px(inner_style) / PX_PER_IN, 0.0)

    packed_children: List[Dict[str, Any]] = []
    current_y = 0.0
    for child in _direct_tag_children(inner_node):
        child_style = compute_element_style(child, css_rules, child.get('style', ''), inner_style)
        if child_style.get('position', '').strip() in ('absolute', 'fixed'):
            continue
        child_classes = _element_classes(child)

        if 'sol-list' in child_classes:
            rows = _build_swiss_index_list_rows(child, css_rules, slide_width_px, content_w_in, contract)
            for el in rows:
                el['bounds']['y'] += current_y
                packed_children.append(el)
            if rows:
                last_bottom = max(e['bounds']['y'] + e['bounds']['height'] for e in rows)
                current_y = last_bottom
                if inner_gap_in > 0:
                    current_y += inner_gap_in
            continue

        built = flat_extract(
            child, css_rules, inner_style, slide_width_px,
            content_width_px=inner_w_px, local_origin=True, contract=contract,
        )
        if not built and child.name.lower() == 'hr':
            rule_shape = _build_rule_shape_from_node(child, child_style, slide_width_px, inner_w_px)
            if rule_shape:
                built = [rule_shape]
        for el in built:
            el['bounds']['y'] = current_y + el['bounds'].get('y', 0.0)
            packed_children.append(el)
        if built:
            last_bottom = max(e['bounds']['y'] + e['bounds']['height'] for e in built)
            current_y = last_bottom
            if inner_gap_in > 0:
                current_y += inner_gap_in

    total_h_in = max(current_y - inner_gap_in, 0.0) if packed_children else 0.0

    justify = (inner_style.get('justifyContent') or inner_style.get('justify-content') or '').strip()
    if justify == 'center':
        content_y_in = slide_pad_t + max((content_h_in - total_h_in) / 2.0, 0.0)
    elif justify == 'flex-end':
        content_y_in = max(slide_h_in - slide_pad_b - total_h_in, slide_pad_t)
    else:
        content_y_in = slide_pad_t + (inner_pad_t if inner_pad_t > 0 else 0.0)

    inner_container = {
        'type': 'container',
        'tag': inner_node.name,
        'bounds': {'x': content_x_in, 'y': content_y_in, 'width': content_w_in, 'height': total_h_in},
        'styles': inner_style,
        'children': packed_children,
        '_children_relative': True,
        'layoutDone': True,
    }

    root = {
        'type': 'container',
        'tag': slide_root.name,
        'bounds': {'x': 0.0, 'y': 0.0, 'width': slide_w_in, 'height': slide_h_in},
        'styles': slide_style,
        'children': [inner_container],
        '_children_relative': True,
        'layoutDone': True,
        '_component_contract': 'swiss_index_list',
    }
    return [root]


def _build_swiss_terminal_line(
    span_node: Tag,
    css_rules: List[CSSRule],
    parent_style: Dict[str, str],
    slide_width_px: float,
    max_w_in: float,
    rel_y_in: float,
) -> List[Dict[str, Any]]:
    """Render a `.terminal-line` inline-block span as a dark pill (bg shape +
    overlaid text). Returns [shape, text] anchored at x=0, y=rel_y_in."""
    span_style = compute_element_style(span_node, css_rules, span_node.get('style', ''), parent_style)
    _expand_padding(span_style)
    pad_l = parse_px(span_style.get('paddingLeft', '0px')) / PX_PER_IN
    pad_r = parse_px(span_style.get('paddingRight', '0px')) / PX_PER_IN
    pad_t = parse_px(span_style.get('paddingTop', '0px')) / PX_PER_IN
    pad_b = parse_px(span_style.get('paddingBottom', '0px')) / PX_PER_IN

    text_el = build_text_element(span_node, span_style, css_rules, slide_width_px, max_w_in * PX_PER_IN)
    if text_el is None:
        return []

    text_w = text_el['bounds'].get('width', 0.0)
    text_h = text_el['bounds'].get('height', 0.0)
    pill_w = min(text_w + pad_l + pad_r, max_w_in)
    pill_h = text_h + pad_t + pad_b

    shape = build_shape_element(span_node, span_style, slide_width_px)
    shape['bounds'] = {'x': 0.0, 'y': rel_y_in, 'width': pill_w, 'height': pill_h}
    import uuid
    pair_id = str(uuid.uuid4())[:8]
    shape['_pair_with'] = pair_id
    shape['_css_pad_l'] = pad_l
    shape['_css_pad_r'] = pad_r
    shape['_css_pad_t'] = pad_t
    shape['_css_pad_b'] = pad_b

    text_el['_pair_with'] = pair_id
    text_el['bounds'] = {
        'x': pad_l,
        'y': rel_y_in + pad_t,
        'width': pill_w - pad_l - pad_r,
        'height': text_h,
    }
    return [shape, text_el]


def _build_swiss_inst_block_card(
    block_node: Tag,
    css_rules: List[CSSRule],
    parent_style: Dict[str, str],
    slide_width_px: float,
    block_w_in: float,
    rel_y_in: float,
) -> Tuple[List[Dict[str, Any]], float]:
    """Build a single `.inst-block`: left border bar + label + terminal-line pill.

    Returns (elements, total_height)."""
    block_style = compute_element_style(block_node, css_rules, block_node.get('style', ''), parent_style)
    _expand_padding(block_style)
    pad_l = parse_px(block_style.get('paddingLeft', '0px')) / PX_PER_IN
    pad_r = parse_px(block_style.get('paddingRight', '0px')) / PX_PER_IN
    pad_t = parse_px(block_style.get('paddingTop', '0px')) / PX_PER_IN
    pad_b = parse_px(block_style.get('paddingBottom', '0px')) / PX_PER_IN
    border_l_in = _extract_border_width_in(block_style, 'borderLeft')
    block_gap_in = parse_px(block_style.get('gap', '8px')) / PX_PER_IN if block_style.get('gap') else 8.0 / PX_PER_IN

    elements: List[Dict[str, Any]] = []
    inner_x = pad_l + border_l_in
    inner_w_in = max(block_w_in - inner_x - pad_r, 0.5)
    cur_y = pad_t

    # Border-left bar (red for highlight, dark otherwise)
    border_left_raw = (block_style.get('borderLeft', '') or '').strip()
    if border_l_in > 0 and border_left_raw and 'none' not in border_left_raw:
        m = re.search(r'(rgb[a]?\([^)]+\)|#[0-9a-fA-F]+|var\([^)]+\))', border_left_raw)
        bar_color = m.group(0) if m else '#1a1a1a'
        if bar_color.startswith('var('):
            # Resolve common swiss vars
            if 'red' in bar_color.lower():
                bar_color = '#c41e3a'
            else:
                bar_color = '#1a1a1a'
        elements.append({
            'type': 'shape',
            'tag': 'div',
            'bounds': {'x': 0.0, 'y': rel_y_in, 'width': border_l_in, 'height': 0.0},  # height filled later
            'styles': {'backgroundColor': bar_color, 'borderRadius': ''},
            '_is_decoration': True,
            '_swiss_inst_border_bar': True,
            'layoutDone': True,
        })

    for child in _direct_tag_children(block_node):
        child_classes = _element_classes(child)
        child_style = compute_element_style(child, css_rules, child.get('style', ''), block_style)
        if 'terminal-line' in child_classes:
            pill_els = _build_swiss_terminal_line(
                child, css_rules, block_style, slide_width_px, inner_w_in, rel_y_in + cur_y,
            )
            for el in pill_els:
                el['bounds']['x'] += inner_x
                elements.append(el)
            if pill_els:
                pill_h = max(e['bounds']['height'] for e in pill_els)
                cur_y += pill_h + block_gap_in
        else:
            text_el = build_text_element(child, child_style, css_rules, slide_width_px, inner_w_in * PX_PER_IN)
            if text_el is None:
                continue
            text_el['bounds']['x'] = inner_x
            text_el['bounds']['y'] = rel_y_in + cur_y
            text_el['bounds']['width'] = inner_w_in
            elements.append(text_el)
            cur_y += text_el['bounds'].get('height', 0.2) + block_gap_in

    if cur_y > 0:
        cur_y -= block_gap_in
    total_h = cur_y + pad_b

    # Backfill border bar height to match block height
    for el in elements:
        if el.get('_swiss_inst_border_bar'):
            el['bounds']['height'] = total_h
            el.pop('_swiss_inst_border_bar', None)

    return elements, total_h


def _build_swiss_inst_blocks(
    slide_root: Tag,
    css_rules: List[CSSRule],
    slide_width_px: float,
    slide_height_px: float,
    contract: Optional[Dict[str, Any]],
    layout_info: Dict[str, Any],
) -> Optional[List[Dict[str, Any]]]:
    """Builder for `.inst-inner` slides: vertically-centered eyebrow / h2 / rule
    plus left-aligned `.inst-blocks` capped at the authored max-width."""
    inner_node, _ = _direct_child_matches_any_selector(slide_root, ['.inst-inner'])
    if inner_node is None:
        return None

    slide_style = compute_element_style(slide_root, css_rules, slide_root.get('style', ''))
    slide_w_in = slide_width_px / PX_PER_IN
    slide_h_in = slide_height_px / PX_PER_IN
    slide_pad_l, slide_pad_r, slide_pad_t, slide_pad_b = _resolve_box_padding_in(
        slide_style, slide_width_px, slide_height_px,
    )
    content_h_in = max(slide_h_in - slide_pad_t - slide_pad_b, 0.8)

    inner_style = compute_element_style(inner_node, css_rules, inner_node.get('style', ''), slide_style)
    raw_padding = inner_style.get('padding', '') or _lookup_matching_css_property(inner_node, css_rules, 'padding')
    inner_pad_l, inner_pad_r, inner_pad_t, inner_pad_b = _resolve_box_padding_in(
        inner_style, slide_width_px, slide_height_px, raw_value=raw_padding,
    )
    content_x_in = max(slide_pad_l, inner_pad_l)
    content_w_in = max(slide_w_in - content_x_in - max(slide_pad_r, inner_pad_r), 1.0)

    inner_gap_in = max(_get_gap_px(inner_style) / PX_PER_IN, 0.0)

    packed_children: List[Dict[str, Any]] = []
    current_y = 0.0
    for child in _direct_tag_children(inner_node):
        child_style = compute_element_style(child, css_rules, child.get('style', ''), inner_style)
        if child_style.get('position', '').strip() in ('absolute', 'fixed'):
            continue
        child_classes = _element_classes(child)

        if 'inst-blocks' in child_classes:
            blocks_style = child_style
            blocks_max_raw = blocks_style.get('maxWidth', blocks_style.get('max-width', '')) or ''
            blocks_w_in = content_w_in
            if blocks_max_raw:
                resolved = _resolve_css_length_with_basis(blocks_max_raw, content_w_in * PX_PER_IN)
                if resolved > 0:
                    blocks_w_in = min(content_w_in, resolved / PX_PER_IN)
            blocks_gap_in = max(_get_gap_px(blocks_style) / PX_PER_IN, 0.16)

            for block_child in _direct_tag_children(child):
                block_classes = _element_classes(block_child)
                if 'inst-block' in block_classes:
                    block_els, block_h = _build_swiss_inst_block_card(
                        block_child, css_rules, blocks_style, slide_width_px, blocks_w_in, current_y,
                    )
                    packed_children.extend(block_els)
                    current_y += block_h + blocks_gap_in
                else:
                    block_built = flat_extract(
                        block_child, css_rules, blocks_style, slide_width_px,
                        content_width_px=blocks_w_in * PX_PER_IN, local_origin=True, contract=contract,
                    )
                    for el in block_built:
                        el['bounds']['y'] = current_y + el['bounds'].get('y', 0.0)
                        packed_children.append(el)
                    if block_built:
                        last_bottom = max(e['bounds']['y'] + e['bounds']['height'] for e in block_built)
                        current_y = last_bottom + blocks_gap_in
            if current_y > 0:
                current_y -= blocks_gap_in
            if inner_gap_in > 0:
                current_y += inner_gap_in
            continue

        built = flat_extract(
            child, css_rules, inner_style, slide_width_px,
            content_width_px=content_w_in * PX_PER_IN, local_origin=True, contract=contract,
        )
        for el in built:
            el['bounds']['y'] = current_y + el['bounds'].get('y', 0.0)
            packed_children.append(el)
        if built:
            last_bottom = max(e['bounds']['y'] + e['bounds']['height'] for e in built)
            current_y = last_bottom
            if inner_gap_in > 0:
                current_y += inner_gap_in

    total_h_in = max(current_y - inner_gap_in, 0.0) if packed_children else 0.0

    justify = (inner_style.get('justifyContent') or inner_style.get('justify-content') or '').strip()
    if justify == 'center':
        content_y_in = slide_pad_t + max((content_h_in - total_h_in) / 2.0, 0.0)
    else:
        content_y_in = slide_pad_t + (inner_pad_t if inner_pad_t > 0 else 0.0)

    inner_container = {
        'type': 'container',
        'tag': inner_node.name,
        'bounds': {'x': content_x_in, 'y': content_y_in, 'width': content_w_in, 'height': total_h_in},
        'styles': inner_style,
        'children': packed_children,
        '_children_relative': True,
        'layoutDone': True,
    }

    root = {
        'type': 'container',
        'tag': slide_root.name,
        'bounds': {'x': 0.0, 'y': 0.0, 'width': slide_w_in, 'height': slide_h_in},
        'styles': slide_style,
        'children': [inner_container],
        '_children_relative': True,
        'layoutDone': True,
        '_component_contract': 'swiss_inst_blocks',
    }
    return [root]


def _build_swiss_disc_steps(
    steps_node: Tag,
    css_rules: List[CSSRule],
    slide_width_px: float,
    column_w_in: float,
    contract: Optional[Dict[str, Any]],
) -> Tuple[List[Dict[str, Any]], float]:
    """Layout `.disc-steps`: vertically stacked numbered rows.

    Each `.disc-step` has [.disc-step-num span, content div] in a flex-row;
    the number column takes its `min-width`, content column takes the rest.
    Returns (elements, total_height) anchored relative to the column origin.
    """
    steps_style = compute_element_style(steps_node, css_rules, steps_node.get('style', ''))
    list_gap_in = max(_get_gap_px(steps_style) / PX_PER_IN, 0.12)

    elements: List[Dict[str, Any]] = []
    cur_y = 0.0

    for step in _direct_tag_children(steps_node):
        if 'disc-step' not in _element_classes(step):
            continue
        step_style = compute_element_style(step, css_rules, step.get('style', ''), steps_style)
        gap_in = max(_get_gap_px(step_style) / PX_PER_IN, 0.12)

        kids = _direct_tag_children(step)
        num_node = next((c for c in kids if 'disc-step-num' in _element_classes(c)), None)
        content_node = next((c for c in kids if c is not num_node), None)
        if num_node is None or content_node is None:
            continue

        num_style = compute_element_style(num_node, css_rules, num_node.get('style', ''), step_style)
        content_style = compute_element_style(content_node, css_rules, content_node.get('style', ''), step_style)

        min_w_raw = num_style.get('minWidth', num_style.get('min-width', '')) or ''
        num_col_w_in = 0.0
        if min_w_raw:
            num_col_w_in = _resolve_css_length_with_basis(min_w_raw, column_w_in * PX_PER_IN) / PX_PER_IN
        if num_col_w_in <= 0:
            num_col_w_in = 0.4

        num_el = build_text_element(num_node, num_style, css_rules, slide_width_px, num_col_w_in * PX_PER_IN)
        content_x = num_col_w_in + gap_in
        content_w_in = max(column_w_in - content_x, 0.5)

        # The content side stacks (title block + desc paragraph). Pack
        # whatever direct children it has so multi-line bodies still flow.
        content_built = _pack_direct_child_content(
            content_node, css_rules, step_style, slide_width_px, content_w_in * PX_PER_IN, contract,
        )
        if num_el is None or content_built is None:
            continue

        num_el['bounds']['x'] = 0.0
        num_el['bounds']['y'] = cur_y
        num_el['bounds']['width'] = num_col_w_in
        elements.append(num_el)

        # Place packed content container at content_x, cur_y
        content_built['bounds']['x'] = content_x
        content_built['bounds']['y'] = cur_y
        content_built['bounds']['width'] = content_w_in
        elements.append(content_built)

        row_h = max(num_el['bounds'].get('height', 0.0), content_built['bounds'].get('height', 0.0))
        cur_y += row_h + list_gap_in

    if cur_y > 0:
        cur_y -= list_gap_in
    return elements, cur_y


def _build_swiss_disc_layout(
    slide_root: Tag,
    css_rules: List[CSSRule],
    slide_width_px: float,
    slide_height_px: float,
    contract: Optional[Dict[str, Any]],
    layout_info: Dict[str, Any],
) -> Optional[List[Dict[str, Any]]]:
    """Builder for the `.disc-header + .disc-body` (geometric diagram) slide.

    Top: eyebrow / h2 / rule packed at the disc-header padding.
    Bottom: two-column row — left `.disc-steps` (vertical list), right
            `.disc-diagram` (SVG illustration).
    """
    header_node = _direct_child_matches_selector(slide_root, '.disc-header')
    body_node = _direct_child_matches_selector(slide_root, '.disc-body')
    if header_node is None or body_node is None:
        return None

    slide_style = compute_element_style(slide_root, css_rules, slide_root.get('style', ''))
    slide_w_in = slide_width_px / PX_PER_IN
    slide_h_in = slide_height_px / PX_PER_IN
    slide_pad_l, slide_pad_r, slide_pad_t, slide_pad_b = _resolve_box_padding_in(
        slide_style, slide_width_px, slide_height_px,
    )

    # --- Header ---
    header_style = compute_element_style(header_node, css_rules, header_node.get('style', ''), slide_style)
    raw_header_pad = header_style.get('padding', '') or _lookup_matching_css_property(header_node, css_rules, 'padding')
    head_pad_l, head_pad_r, head_pad_t, head_pad_b = _resolve_box_padding_in(
        header_style, slide_width_px, slide_height_px, raw_value=raw_header_pad,
    )
    raw_header_margin = header_style.get('margin', '') or _lookup_matching_css_property(header_node, css_rules, 'margin')
    _, _, _, head_mb = _resolve_box_margin_in(
        header_style, slide_width_px, slide_height_px, raw_value=raw_header_margin,
    )
    header_x_in = max(slide_pad_l, head_pad_l)
    header_w_in = max(slide_w_in - header_x_in - max(slide_pad_r, head_pad_r), 1.0)
    header_packed = _pack_direct_child_content(
        header_node, css_rules, slide_style, slide_width_px, header_w_in * PX_PER_IN, contract,
    )
    if header_packed is None:
        return None
    header_y_in = max(slide_pad_t, head_pad_t)
    header_packed['bounds']['x'] = header_x_in
    header_packed['bounds']['y'] = header_y_in

    # --- Body ---
    body_style = compute_element_style(body_node, css_rules, body_node.get('style', ''), slide_style)
    raw_body_pad = body_style.get('padding', '') or _lookup_matching_css_property(body_node, css_rules, 'padding')
    body_pad_l, body_pad_r, body_pad_t, body_pad_b = _resolve_box_padding_in(
        body_style, slide_width_px, slide_height_px, raw_value=raw_body_pad,
    )
    body_gap_in = max(_get_gap_px(body_style) / PX_PER_IN, 0.2)
    body_x_in = max(slide_pad_l, body_pad_l)
    body_w_in = max(slide_w_in - body_x_in - max(slide_pad_r, body_pad_r), 1.0)

    steps_node = _direct_child_matches_selector(body_node, '.disc-steps')
    diagram_node = _direct_child_matches_selector(body_node, '.disc-diagram')
    if steps_node is None or diagram_node is None:
        return None

    # Diagram: prefer SVG container measurement; fall back to fixed-aspect square.
    diagram_style = compute_element_style(diagram_node, css_rules, diagram_node.get('style', ''), body_style)
    svg = next((c for c in _direct_tag_children(diagram_node) if c.name and c.name.lower() == 'svg'), None)
    diagram_w_in = 0.0
    diagram_h_in = 0.0
    diagram_built: Optional[Dict[str, Any]] = None
    if svg is not None:
        target_diag_w_in = min(body_w_in * 0.40, 3.5)
        diagram_built = build_svg_container(
            svg, css_rules, diagram_style, slide_width_px,
            content_width_px=target_diag_w_in * PX_PER_IN,
        )
        if diagram_built:
            diagram_w_in = diagram_built['bounds'].get('width', target_diag_w_in)
            diagram_h_in = diagram_built['bounds'].get('height', target_diag_w_in)
    if diagram_built is None:
        diagram_w_in = min(body_w_in * 0.40, 3.0)
        diagram_h_in = diagram_w_in

    steps_w_in = max(body_w_in - diagram_w_in - body_gap_in, 1.0)
    steps_elements, steps_h = _build_swiss_disc_steps(
        steps_node, css_rules, slide_width_px, steps_w_in, contract,
    )

    # Body height: tallest of the two columns
    body_content_h_in = max(steps_h, diagram_h_in)
    available_below_header = max(slide_h_in - slide_pad_b - (header_y_in + header_packed['bounds'].get('height', 0.0) + head_mb + body_pad_t), 0.0)
    body_y_in = (
        header_y_in
        + header_packed['bounds'].get('height', 0.0)
        + head_mb
        + body_pad_t
        + max((available_below_header - body_content_h_in) / 2.0, 0.0)
    )

    # Vertical-center each column relative to body content height (mimics align-items:center)
    steps_v_offset = max((body_content_h_in - steps_h) / 2.0, 0.0)
    diagram_v_offset = max((body_content_h_in - diagram_h_in) / 2.0, 0.0)

    # Anchor steps and diagram into absolute slide coords
    for el in steps_elements:
        el['bounds']['x'] = body_x_in + el['bounds'].get('x', 0.0)
        el['bounds']['y'] = body_y_in + steps_v_offset + el['bounds'].get('y', 0.0)

    if diagram_built:
        diagram_built['bounds']['x'] = body_x_in + steps_w_in + body_gap_in
        diagram_built['bounds']['y'] = body_y_in + diagram_v_offset

    root = {
        'type': 'container',
        'tag': slide_root.name,
        'bounds': {'x': 0.0, 'y': 0.0, 'width': slide_w_in, 'height': slide_h_in},
        'styles': slide_style,
        'children': [header_packed],
        '_children_relative': True,
        'layoutDone': True,
        '_component_contract': 'swiss_disc_layout',
    }
    root['children'].extend(steps_elements)
    if diagram_built:
        root['children'].append(diagram_built)

    return [root]


def _build_swiss_role_elements(
    slide_root: Tag,
    css_rules: List[CSSRule],
    slide_width_px: float,
    slide_height_px: float,
    contract: Optional[Dict[str, Any]],
    layout_info: Dict[str, Any],
) -> Optional[List[Dict[str, Any]]]:
    if (contract or {}).get('contract_id') != 'slide-creator/swiss-modern':
        return None
    role = (layout_info.get('role') or '').strip()
    if role == 'title_grid' or role == 'inner_panel':
        return _build_swiss_title_grid(
            slide_root,
            css_rules,
            slide_width_px,
            slide_height_px,
            contract,
            layout_info,
        )
    if role == 'column_content':
        return _build_swiss_column_content(
            slide_root,
            css_rules,
            slide_width_px,
            slide_height_px,
            contract,
            layout_info,
        )
    if role == 'stat_block':
        return _build_swiss_stat_block(
            slide_root,
            css_rules,
            slide_width_px,
            slide_height_px,
            contract,
            layout_info,
        )
    if role == 'pull_quote':
        return _build_swiss_pull_quote(
            slide_root,
            css_rules,
            slide_width_px,
            slide_height_px,
            contract,
            layout_info,
        )
    if role == 'index_list':
        return _build_swiss_index_list(
            slide_root,
            css_rules,
            slide_width_px,
            slide_height_px,
            contract,
            layout_info,
        )
    if role == 'inst_blocks':
        return _build_swiss_inst_blocks(
            slide_root,
            css_rules,
            slide_width_px,
            slide_height_px,
            contract,
            layout_info,
        )
    if role == 'disc_layout':
        return _build_swiss_disc_layout(
            slide_root,
            css_rules,
            slide_width_px,
            slide_height_px,
            contract,
            layout_info,
        )
    return None


def _apply_explicit_positions(elements: List[Dict[str, Any]]) -> None:
    for elem in elements:
        _apply_slide_anchor_position(elem)


def _build_card_bg_shape(
    element: Tag,
    style: Dict[str, str],
    slide_width_px: float,
    width_in: float,
    height_in: float,
    pad_l: float,
    pad_r: float,
    pad_t: float,
    pad_b: float,
) -> Dict[str, Any]:
    bg_shape = build_shape_element(element, style, slide_width_px)
    bg_shape['bounds'] = {'x': 0.0, 'y': 0.0, 'width': width_in, 'height': height_in}
    bg_shape['_is_card_bg'] = True
    bg_shape['_skip_layout'] = True
    bg_shape['_css_pad_l'] = pad_l
    bg_shape['_css_pad_r'] = pad_r
    bg_shape['_css_pad_t'] = pad_t
    bg_shape['_css_pad_b'] = pad_b
    bg_shape['_css_border_l'] = 0.0
    bg_shape['_css_text_align'] = style.get('textAlign', 'left')
    return bg_shape


def _shift_relative_element_y(elem: Dict[str, Any], delta_y: float) -> None:
    if abs(delta_y) <= 1e-6:
        return
    elem.setdefault('bounds', {})['y'] = elem.get('bounds', {}).get('y', 0.0) + delta_y
    if elem.get('type') == 'freeform':
        elem['points'] = [(x, y + delta_y) for x, y in (elem.get('points') or [])]
    if elem.get('type') == 'container' and elem.get('_children_relative'):
        _shift_container_descendants(elem, 0.0, delta_y)


def _apply_vertical_card_slot_layout(
    flow_children: List[Dict[str, Any]],
    pad_t: float,
    pad_b: float,
    card_h: float,
    slot_model: Dict[str, Any],
) -> None:
    content_children = [
        child for child in flow_children
        if child.get('type') != 'shape' or not child.get('_is_card_bg')
    ]
    if len(content_children) < 2 or not slot_model.get('bottom_anchor_last_slot'):
        return

    gap_cfg = slot_model.get('gaps') or {}
    gap_after_metric = float(gap_cfg.get('after_metric', 0.06) or 0.06)
    gap_after_label = float(gap_cfg.get('after_label', 0.05) or 0.05)

    first = content_children[0]
    last = content_children[-1]
    first_gap_after = float(first.get('_slot_gap_after', gap_after_metric) or gap_after_metric)
    last_bounds = last.get('bounds', {})
    last_target_y = max(card_h - pad_b - last_bounds.get('height', 0.0), pad_t)
    _shift_relative_element_y(last, last_target_y - last_bounds.get('y', 0.0))

    if len(content_children) == 2 and slot_model.get('metric_vertical_align') == 'center_remaining':
        first_bounds = first.get('bounds', {})
        upper_limit = max(last_target_y - first_gap_after, pad_t + first_bounds.get('height', 0.0))
        first_target_y = pad_t + max((upper_limit - pad_t - first_bounds.get('height', 0.0)) / 2.0, 0.0)
        _shift_relative_element_y(first, first_target_y - first_bounds.get('y', 0.0))
        return

    middle = content_children[1:-1]
    if not middle:
        return

    mid_top = min(child.get('bounds', {}).get('y', 0.0) for child in middle)
    mid_bottom = max(
        child.get('bounds', {}).get('y', 0.0) + child.get('bounds', {}).get('height', 0.0)
        for child in middle
    )
    last_middle_gap = float(middle[-1].get('_slot_gap_after', gap_after_label) or gap_after_label)
    target_mid_bottom = max(last_target_y - last_middle_gap, mid_top)
    middle_delta = target_mid_bottom - mid_bottom
    for child in middle:
        _shift_relative_element_y(child, middle_delta)

    if slot_model.get('metric_vertical_align') != 'center_remaining':
        return

    first_bounds = first.get('bounds', {})
    middle_top = min(child.get('bounds', {}).get('y', 0.0) for child in middle)
    upper_limit = max(middle_top - first_gap_after, pad_t + first_bounds.get('height', 0.0))
    first_target_y = pad_t + max((upper_limit - pad_t - first_bounds.get('height', 0.0)) / 2.0, 0.0)
    _shift_relative_element_y(first, first_target_y - first_bounds.get('y', 0.0))


def _set_text_element_font_px(elem: Dict[str, Any], font_px: float) -> None:
    """Update a text element font size consistently across styles/segments/fragments."""
    if not elem or elem.get('type') != 'text':
        return
    font_px = max(font_px, 1.0)
    font_size = f'{font_px:.2f}px'
    elem.setdefault('styles', {})['fontSize'] = font_size
    for fragment in elem.get('fragments', []) or []:
        fragment['fontSize'] = font_size
    for segment in elem.get('segments', []) or []:
        segment['fontSize'] = font_size


def _fit_vertical_card_metric_slot(
    flow_children: List[Dict[str, Any]],
    pad_t: float,
    pad_b: float,
    card_h: float,
    slot_model: Dict[str, Any],
) -> bool:
    """Keep oversized metric tokens from dominating vertical-card components."""
    max_ratio = float(slot_model.get('metric_max_height_ratio', 0.0) or 0.0)
    if max_ratio <= 0.0:
        return False

    content_children = [
        child for child in flow_children
        if child.get('type') != 'shape' or not child.get('_is_card_bg')
    ]
    if not content_children:
        return False

    metric_child = next(
        (child for child in content_children if child.get('_slot_metric') and child.get('type') == 'text'),
        None,
    )
    if not metric_child:
        return False

    inner_h = max(card_h - pad_t - pad_b, 0.2)
    target_h = inner_h * max_ratio
    current_h = metric_child.get('bounds', {}).get('height', 0.0)
    if current_h <= target_h + 1e-6:
        return False

    current_font_px = parse_px(metric_child.get('styles', {}).get('fontSize', '16px')) or 16.0
    scale = max(min(target_h / max(current_h, 1e-6), 0.98), 0.70)
    new_font_px = current_font_px * scale
    _set_text_element_font_px(metric_child, new_font_px)

    width_in = metric_child.get('bounds', {}).get('width', 0.2)
    next_flow_item = None
    try:
        metric_idx = content_children.index(metric_child)
        if metric_idx + 1 < len(content_children):
            next_flow_item = content_children[metric_idx + 1]
    except ValueError:
        next_flow_item = None

    _remeasure_text_for_final_width(
        metric_child,
        width_in,
        next_flow_item=next_flow_item,
        inside_card=True,
    )
    return True


def _vertical_card_authored_gap_after_in(
    current_style: Dict[str, str],
    next_style: Optional[Dict[str, str]],
    parent_gap_in: float,
    fallback_gap_in: float,
    basis_px: float,
) -> float:
    """Prefer authored column gap + margins before falling back to contract spacing."""
    current_mb = _resolve_css_length_with_basis(current_style.get('marginBottom', '0px'), basis_px) / PX_PER_IN
    next_mt = 0.0
    if next_style:
        next_mt = _resolve_css_length_with_basis(next_style.get('marginTop', '0px'), basis_px) / PX_PER_IN
    authored = max(parent_gap_in + current_mb + next_mt, 0.0)
    if authored > 1e-6:
        return authored
    return fallback_gap_in


def _build_contract_vertical_card(
    element: Tag,
    style: Dict[str, str],
    css_rules: List[CSSRule],
    slide_width_px: float,
    content_width_px: Optional[float],
    slot_model: Dict[str, Any],
    contract: Optional[Dict[str, Any]] = None,
    component_name: Optional[str] = None,
) -> Optional[List[Dict[str, Any]]]:
    direct_children = [child for child in element.children if isinstance(child, Tag)]
    if not direct_children:
        return None

    width_in = _resolve_container_width_in(style, content_width_px, slide_width_px)
    _expand_padding(style)
    pad_l = parse_px(style.get('paddingLeft', '16px')) / PX_PER_IN
    pad_r = parse_px(style.get('paddingRight', '16px')) / PX_PER_IN
    pad_t = parse_px(style.get('paddingTop', '16px')) / PX_PER_IN
    pad_b = parse_px(style.get('paddingBottom', '16px')) / PX_PER_IN
    content_w_in = max(width_in - pad_l - pad_r, 0.3)

    gap_cfg = slot_model.get('gaps') or {}
    gap_after_metric = float(gap_cfg.get('after_metric', 0.06) or 0.06)
    gap_after_label = float(gap_cfg.get('after_label', 0.05) or 0.05)
    min_height_in = float(slot_model.get('minimum_height_in', 0.0) or 0.0)
    parent_gap_in = 0.0
    if style.get('display') in {'flex', 'inline-flex'} and style.get('flexDirection', 'row') == 'column':
        parent_gap_px = _resolve_css_length_with_basis(
            style.get('rowGap') or style.get('gap', '0px'),
            slide_width_px,
        )
        parent_gap_in = max(parent_gap_px / PX_PER_IN, 0.0)

    children: List[Dict[str, Any]] = []
    y_cursor = pad_t

    resolved_children: List[Tuple[Tag, Dict[str, str], Set[str], str]] = []
    for child in direct_children:
        child_style = compute_element_style(child, css_rules, child.get('style', ''), style)
        resolved_children.append((child, child_style, _element_classes(child), get_text_content(child).strip()))

    for idx, (child, child_style, child_classes, child_text) in enumerate(resolved_children):
        child_cw_px = max(content_w_in * PX_PER_IN, 1.0)
        metric_like = bool(
            child_classes.intersection({'ds-kpi', 'feat-stat', 'sol-icon'}) or
            (
                idx == 0 and
                slot_model.get('metric_single_line') and
                _looks_like_metric_token(child_text)
            )
        )

        if child.name == 'svg':
            child_el = build_svg_container(
                child,
                css_rules,
                style,
                slide_width_px,
                child_cw_px,
            )
        elif (
            is_leaf_text_container(child, css_rules) and
            (has_visible_bg_or_border(child_style) or child_style.get('backgroundImage', 'none') != 'none')
        ):
            built = flat_extract(
                child,
                css_rules,
                style,
                slide_width_px,
                content_width_px=child_cw_px,
                local_origin=True,
                contract=contract,
            )
            child_el = _coerce_relative_container(child, child_style, built)
        elif (
            child.name in CONTAINER_TAGS and
            (has_visible_bg_or_border(child_style) or child_style.get('backgroundImage', 'none') != 'none') and
            parse_px(child_style.get('height', '')) > 0
        ):
            swatch_w_in = content_w_in if (idx == 0 or slot_model.get('stretch_first_slot')) else min(content_w_in, width_in)
            swatch_h_in = parse_px(child_style.get('height', '')) / PX_PER_IN
            shape = build_shape_element(child, child_style, slide_width_px)
            shape['bounds'] = {'x': 0.0, 'y': 0.0, 'width': swatch_w_in, 'height': swatch_h_in}
            shape['_is_decoration'] = True
            swatch_children: List[Dict[str, Any]] = [shape]
            if child_text:
                text_el = build_text_element(child, child_style, css_rules, slide_width_px, swatch_w_in * PX_PER_IN)
                if text_el:
                    text_el.setdefault('styles', {})['textAlign'] = 'center'
                    text_el['bounds']['x'] = 0.0
                    text_el['bounds']['width'] = swatch_w_in
                    _remeasure_text_for_final_width(text_el, swatch_w_in, inside_card=True)
                    text_el['bounds']['y'] = max((swatch_h_in - text_el['bounds'].get('height', 0.0)) / 2.0, 0.0)
                    swatch_children.append(text_el)
            child_el = {
                'type': 'container',
                'tag': child.name,
                'bounds': {'x': 0.0, 'y': 0.0, 'width': swatch_w_in, 'height': swatch_h_in},
                'styles': child_style,
                'children': swatch_children,
                '_children_relative': True,
            }
        elif child.name in TEXT_TAGS or get_text_content(child).strip():
            child_el = build_text_element(child, child_style, css_rules, slide_width_px, child_cw_px)
        else:
            child_el = None

        if not child_el:
            continue

        child_bounds = child_el.setdefault('bounds', {})
        if metric_like and child_el.get('type') == 'text':
            child_el['_slot_metric'] = True
        child_bounds['x'] = pad_l
        if child_el.get('type') == 'text':
            if metric_like:
                child_el['forceSingleLine'] = True
                child_el['preferNoWrapFit'] = True
            child_bounds['width'] = min(max(child_bounds.get('width', content_w_in), 0.2), content_w_in)
            if (
                idx > 0 or
                child_classes.intersection({'ds-kpi-label', 'feat-stat', 'sol-icon'})
            ):
                child_bounds['width'] = content_w_in
        elif idx == 0 and slot_model.get('stretch_first_slot'):
            child_bounds['width'] = content_w_in
        child_bounds['y'] = y_cursor
        children.append(child_el)

        gap_after = 0.0
        if idx + 1 < len(resolved_children):
            fallback_gap = gap_after_label
            if metric_like or idx == 0:
                fallback_gap = max(
                    gap_after_metric,
                    min(max(parse_px(child_style.get('fontSize', '16px')) * 0.12 / PX_PER_IN, 0.08), 0.18),
                )
            next_style = resolved_children[idx + 1][1]
            gap_after = _vertical_card_authored_gap_after_in(
                child_style,
                next_style,
                parent_gap_in,
                fallback_gap,
                slide_width_px,
            )
        child_el['_slot_gap_after'] = gap_after
        y_cursor += child_bounds.get('height', 0.0) + gap_after

    if not children:
        return None

    content_bottom = max(
        child.get('bounds', {}).get('y', 0.0) + child.get('bounds', {}).get('height', 0.0)
        for child in children
    )
    card_h = max(content_bottom + pad_b, min_height_in, 0.2)
    bg_shape = _build_card_bg_shape(element, style, slide_width_px, width_in, card_h, pad_l, pad_r, pad_t, pad_b)
    bg_shape['_component_slot_model'] = copy.deepcopy(slot_model)
    flow_children = [bg_shape] + children
    _normalize_card_group_text_metrics(flow_children, width_in)
    card_h = max(
        max(
            child.get('bounds', {}).get('y', 0.0) + child.get('bounds', {}).get('height', 0.0)
            for child in flow_children
        ),
        min_height_in,
    )
    _fit_vertical_card_metric_slot(flow_children, pad_t, pad_b, card_h, slot_model)
    _apply_vertical_card_slot_layout(flow_children, pad_t, pad_b, card_h, slot_model)
    card_h = max(
        max(
            child.get('bounds', {}).get('y', 0.0) + child.get('bounds', {}).get('height', 0.0)
            for child in flow_children
        ),
        min_height_in,
    )
    bg_shape['bounds']['height'] = card_h

    return [{
        'type': 'container',
        'tag': element.name,
        'bounds': {'x': 0.0, 'y': 0.0, 'width': width_in, 'height': card_h},
        'styles': style,
        'children': flow_children,
        '_children_relative': True,
        '_component_contract': slot_model.get('layout', 'vertical_card'),
        '_component_slot_model': copy.deepcopy(slot_model),
    }]


def _build_contract_split_rail(
    element: Tag,
    style: Dict[str, str],
    css_rules: List[CSSRule],
    slide_width_px: float,
    content_width_px: Optional[float],
    slot_model: Dict[str, Any],
) -> Optional[List[Dict[str, Any]]]:
    direct_children = [child for child in element.children if isinstance(child, Tag)]
    if len(direct_children) < 2:
        return None

    width_in = _resolve_container_width_in(style, content_width_px, slide_width_px)
    _expand_padding(style)
    pad_l = parse_px(style.get('paddingLeft', '16px')) / PX_PER_IN
    pad_r = parse_px(style.get('paddingRight', '16px')) / PX_PER_IN
    pad_t = parse_px(style.get('paddingTop', '16px')) / PX_PER_IN
    pad_b = parse_px(style.get('paddingBottom', '16px')) / PX_PER_IN
    gap_px = float(slot_model.get('gap_px', 16) or 16)
    gap_in = gap_px / PX_PER_IN
    label_min_width_px = float(slot_model.get('label_min_width_px', 120) or 120)
    label_min_width_in = label_min_width_px / PX_PER_IN
    min_height_in = float(slot_model.get('minimum_height_in', 0.44) or 0.44)
    content_w_in = max(width_in - pad_l - pad_r, 0.4)

    label_child = direct_children[0]
    cmd_child = direct_children[1]
    label_style = compute_element_style(label_child, css_rules, label_child.get('style', ''), style)
    cmd_style = compute_element_style(cmd_child, css_rules, cmd_child.get('style', ''), style)

    label_el = build_text_element(label_child, label_style, css_rules, slide_width_px, content_w_in * PX_PER_IN)
    if not label_el:
        return None
    rail_label_w = max(label_el.get('bounds', {}).get('width', 0.0), label_min_width_in)
    rail_cmd_w = max(content_w_in - rail_label_w - gap_in, 0.8)
    cmd_el = build_text_element(cmd_child, cmd_style, css_rules, slide_width_px, rail_cmd_w * PX_PER_IN)
    if not cmd_el:
        return None

    label_h = label_el.get('bounds', {}).get('height', 0.0)
    cmd_h = cmd_el.get('bounds', {}).get('height', 0.0)
    row_h = max(label_h, cmd_h)
    card_h = max(pad_t + row_h + pad_b, min_height_in)
    inner_y = pad_t + max((card_h - pad_t - pad_b - row_h) / 2.0, 0.0)

    label_el['bounds']['x'] = pad_l
    label_el['bounds']['y'] = inner_y + max((row_h - label_h) / 2.0, 0.0)
    label_el['bounds']['width'] = rail_label_w
    cmd_el['bounds']['x'] = pad_l + rail_label_w + gap_in
    cmd_el['bounds']['y'] = inner_y + max((row_h - cmd_h) / 2.0, 0.0)
    cmd_el['bounds']['width'] = rail_cmd_w
    cmd_el['preferNoWrapFit'] = bool(slot_model.get('keep_command_single_line', False))
    _remeasure_text_for_final_width(label_el, rail_label_w, inside_card=True)
    _remeasure_text_for_final_width(cmd_el, rail_cmd_w, inside_card=True)

    bg_shape = _build_card_bg_shape(element, style, slide_width_px, width_in, card_h, pad_l, pad_r, pad_t, pad_b)
    return [{
        'type': 'container',
        'tag': element.name,
        'bounds': {'x': 0.0, 'y': 0.0, 'width': width_in, 'height': card_h},
        'styles': style,
        'children': [bg_shape, label_el, cmd_el],
        '_children_relative': True,
        '_component_contract': slot_model.get('layout', 'split_rail'),
    }]


def _build_contract_split_layout(
    element: Tag,
    style: Dict[str, str],
    css_rules: List[CSSRule],
    slide_width_px: float,
    content_width_px: Optional[float],
    slot_model: Dict[str, Any],
    contract: Optional[Dict[str, Any]],
) -> Optional[List[Dict[str, Any]]]:
    direct_children = [child for child in element.children if isinstance(child, Tag)]
    if len(direct_children) < 2:
        return None

    width_in = _resolve_container_width_in(style, content_width_px, slide_width_px)
    gap_in = _get_gap_px(style) / PX_PER_IN
    track_template = slot_model.get('track_template', '').strip() or '1fr 1.5fr'
    track_widths = _parse_grid_track_widths(track_template, width_in, gap_in)
    if len(track_widths) < 2:
        return None

    packed_children: List[Dict[str, Any]] = []
    child_x = 0.0
    align_items = style.get('alignItems', style.get('align-items', 'stretch'))

    for idx, child in enumerate(direct_children[:2]):
        child_style = compute_element_style(child, css_rules, child.get('style', ''), style)
        child_width_in = track_widths[idx]
        child_results = flat_extract(
            child,
            css_rules,
            child_style,
            slide_width_px,
            content_width_px=child_width_in * PX_PER_IN,
            local_origin=True,
            contract=contract,
        )
        if not child_results:
            child_x += child_width_in + gap_in
            continue

        if (
            len(child_results) == 1 and
            child_results[0].get('type') == 'container' and
            child_results[0].get('_children_relative')
        ):
            packed = child_results[0]
            _normalize_relative_container(packed)
        else:
            packed = _pack_relative_block_container(child, child_style, child_results)
            if not packed:
                child_x += child_width_in + gap_in
                continue

        packed['bounds']['x'] = child_x
        packed['bounds']['width'] = min(
            max(packed.get('bounds', {}).get('width', child_width_in), 0.1),
            child_width_in,
        )
        packed_children.append(packed)
        child_x += child_width_in + gap_in

    if not packed_children:
        return None

    container_h = max(child.get('bounds', {}).get('height', 0.0) for child in packed_children)
    for child in packed_children:
        cb = child.get('bounds', {})
        cb['y'] = max((container_h - cb.get('height', 0.0)) / 2.0, 0.0) if align_items == 'center' else 0.0

    total_width = max(
        child.get('bounds', {}).get('x', 0.0) + child.get('bounds', {}).get('width', 0.0)
        for child in packed_children
    )
    return [{
        'type': 'container',
        'tag': element.name,
        'bounds': {'x': 0.0, 'y': 0.0, 'width': max(total_width, 0.1), 'height': max(container_h, 0.1)},
        'styles': style,
        'children': packed_children,
        '_children_relative': True,
        '_component_contract': slot_model.get('layout', 'grid_two_column'),
    }]


def _build_contract_typographic_columns(
    element: Tag,
    style: Dict[str, str],
    css_rules: List[CSSRule],
    slide_width_px: float,
    content_width_px: Optional[float],
    slot_model: Dict[str, Any],
    contract: Optional[Dict[str, Any]] = None,
) -> Optional[List[Dict[str, Any]]]:
    direct_children = [child for child in element.children if isinstance(child, Tag)]
    if len(direct_children) < 2:
        return None

    column_count_raw = slot_model.get('column_count') or style.get('columnCount') or 0
    try:
        column_count = int(float(str(column_count_raw)))
    except Exception:
        column_count = 0
    if column_count < 2:
        return None

    if any(child.name.lower() not in TEXT_TAGS for child in direct_children):
        return None

    width_in = _resolve_container_width_in(style, content_width_px, slide_width_px)
    _expand_padding(style)
    pad_l = parse_px(style.get('paddingLeft', '0px')) / PX_PER_IN
    pad_r = parse_px(style.get('paddingRight', '0px')) / PX_PER_IN
    pad_t = parse_px(style.get('paddingTop', '0px')) / PX_PER_IN
    pad_b = parse_px(style.get('paddingBottom', '0px')) / PX_PER_IN
    gap_raw = style.get('columnGap') or style.get('gap') or f"{slot_model.get('column_gap_px', 24)}px"
    gap_in = max(parse_px(gap_raw) / PX_PER_IN, 0.0)
    content_w_in = max(width_in - pad_l - pad_r, 0.6)
    column_width_in = max((content_w_in - gap_in * (column_count - 1)) / column_count, 0.25)

    measured_items: List[Dict[str, Any]] = []
    for child in direct_children:
        child_style = compute_element_style(child, css_rules, child.get('style', ''), style)
        text_el = build_text_element(
            child,
            child_style,
            css_rules,
            slide_width_px,
            content_width_px=column_width_in * PX_PER_IN,
            contract=contract,
        )
        if not text_el:
            return None
        text_el['bounds']['width'] = column_width_in
        _remeasure_text_for_final_width(text_el, column_width_in, inside_card=False)
        measured_items.append(text_el)

    if len(measured_items) != len(direct_children):
        return None

    gap_between_items = max(_get_gap_px(style) / PX_PER_IN, 0.12)
    total_height = sum(item.get('bounds', {}).get('height', 0.0) for item in measured_items)
    total_height += gap_between_items * max(len(measured_items) - 1, 0)
    target_col_height = max(total_height / column_count, 0.1)

    col_idx = 0
    col_y = [pad_t for _ in range(column_count)]
    placed_children: List[Dict[str, Any]] = []
    for idx, item in enumerate(measured_items):
        item_h = item.get('bounds', {}).get('height', 0.0)
        if (
            col_idx < column_count - 1 and
            col_y[col_idx] > pad_t and
            col_y[col_idx] + item_h > pad_t + target_col_height
        ):
            col_idx += 1
        item['bounds']['x'] = pad_l + col_idx * (column_width_in + gap_in)
        item['bounds']['y'] = col_y[col_idx]
        item['bounds']['width'] = column_width_in
        placed_children.append(item)
        col_y[col_idx] += item_h
        if idx + 1 < len(measured_items):
            col_y[col_idx] += gap_between_items

    content_h = max((y - gap_between_items for y in col_y), default=pad_t)
    container_h = max(content_h + pad_b, 0.2)
    return [{
        'type': 'container',
        'tag': element.name,
        'bounds': {'x': 0.0, 'y': 0.0, 'width': width_in, 'height': container_h},
        'styles': style,
        'children': placed_children,
        '_children_relative': True,
        '_component_contract': slot_model.get('layout', 'typographic_columns'),
        '_component_slot_model': copy.deepcopy(slot_model),
    }]


def _build_contract_component(
    element: Tag,
    style: Dict[str, str],
    css_rules: List[CSSRule],
    slide_width_px: float,
    content_width_px: Optional[float],
    contract: Optional[Dict[str, Any]],
    component_name: Optional[str],
    slot_model: Dict[str, Any],
) -> Optional[List[Dict[str, Any]]]:
    if not component_name or not slot_model:
        return None

    layout_name = slot_model.get('layout')
    if layout_name == 'vertical_card':
        return _build_contract_vertical_card(
            element,
            style,
            css_rules,
            slide_width_px,
            content_width_px,
            slot_model,
            contract=contract,
            component_name=component_name,
        )
    if layout_name == 'split_rail':
        return _build_contract_split_rail(
            element,
            style,
            css_rules,
            slide_width_px,
            content_width_px,
            slot_model,
        )
    if layout_name == 'grid_two_column':
        return _build_contract_split_layout(
            element,
            style,
            css_rules,
            slide_width_px,
            content_width_px,
            slot_model,
            contract,
        )
    if layout_name == 'typographic_columns':
        return _build_contract_typographic_columns(
            element,
            style,
            css_rules,
            slide_width_px,
            content_width_px,
            slot_model,
            contract=contract,
        )
    return None


def build_text_element(element: Tag, style: Dict[str, str], css_rules: List[CSSRule],
                       slide_width_px: float = 1440, content_width_px: float = None,
                       exclude_elements: set = None,
                       contract: Optional[Dict[str, Any]] = None) -> Optional[Dict]:
    """Build a text element IR with segments."""
    tag = element.name.lower()
    raw_text = get_text_content(element).strip()
    style = dict(style)
    text_contract = _resolve_text_contract(element, style, raw_text, contract)
    for key in ('fontFamily', 'fontWeight', 'lineHeight', 'letterSpacing'):
        override = text_contract.get(key)
        if override:
            style[key] = override
    applied_display_heading_boost = False
    if _should_apply_display_heading_boost(tag, style, raw_text):
        base_font_px = parse_px(style.get('fontSize', '16px')) or 16.0
        boost = 1.18 if tag == 'h1' else 1.30
        style['fontSize'] = f'{base_font_px * boost:.2f}px'
        applied_display_heading_boost = True
    fragments = extract_inline_fragments(element, css_rules, style, exclude_elements=exclude_elements)
    has_inline_boxes = any(f.get('kind') in INLINE_BOX_KINDS for f in fragments)
    has_grouped_inline = any(f.get('grouped') for f in fragments)
    has_inline_code_or_kbd = any(f.get('kind') in ('code', 'kbd') for f in fragments)
    fragment_kinds = {f.get('kind') for f in fragments if (f.get('text') or '').strip()}
    has_centered_grouped_command = 'code' in fragment_kinds and 'link' in fragment_kinds
    should_strengthen_display_ink = (
        tag in ('h3', 'h4', 'h5', 'h6') and
        _normalize_ink_color(style.get('color', '')) == '#000000' and
        not has_visible_bg_or_border(style)
    )
    if should_strengthen_display_ink:
        fragments = _normalize_display_ink_fragments(fragments, '#000000')
    if has_centered_grouped_command:
        fragments = _normalize_centered_command_fragments(
            fragments,
            _style_text_color(style, style.get('color', '')),
        )
    text = fragments_to_text(fragments).strip()
    if not text:
        return None
    segments = inline_fragments_to_segments(fragments)
    if not segments and not text:
        return None
    has_direct_link_child = any(
        isinstance(child, Tag) and child.name.lower() == 'a'
        for child in element.children
    )
    display = style.get('display', '')
    inlineish_display = (
        'inline-block' in display or
        'inline-flex' in display or
        display == 'flex'
    )
    element_is_inline_box = (
        has_visible_bg_or_border(style) and
        is_leaf_text_container(element, css_rules) and
        (
            tag in INLINE_TAGS or
            inlineish_display
        )
    )
    shrink_wrap_inline = element_is_inline_box and (
        inlineish_display or
        tag == 'span'
    )
    component_like_inline = (
        shrink_wrap_inline or
        (
            tag in INLINE_TAGS and
            has_visible_bg_or_border(style) and
            (has_grouped_inline or has_inline_boxes) and
            '\n' not in text
        )
    )
    monospace_text = _uses_monospace_font(style.get('fontFamily', ''))
    centered_block_command_like = (
        not component_like_inline and
        has_visible_bg_or_border(style) and
        '\n' not in text and
        parse_px(style.get('width', '')) <= 0 and
        parse_px(style.get('maxWidth', '')) <= 0 and
        bool(content_width_px and content_width_px > 0) and
        _has_centered_parent_column(element, css_rules, style) and
        (
            monospace_text or
            'cmd' in _element_classes(element)
        )
    )
    include_box_padding = has_inline_boxes or has_grouped_inline or shrink_wrap_inline

    font_size_px = parse_px(style.get('fontSize', '16px'))
    if font_size_px <= 0:
        font_size_px = 16.0
    font_size_pt = px_to_pt(style.get('fontSize', '16px'))
    if font_size_pt <= 0:
        font_size_pt = 12.0
    explicit_break_display_heading = (
        tag in ('h1', 'h2', 'h3') and
        '\n' in text and
        style.get('textAlign', '') == 'center' and
        font_size_pt >= 28
    )

    # Determine effective width from CSS constraints
    explicit_w = parse_px(style.get('width', ''))
    max_w = parse_px(style.get('maxWidth', ''))
    is_inline_block = 'inline-block' in display

    # Compute content-based width if needed
    if fragments:
        content_w_in = measure_inline_fragments_width_in(
            fragments,
            font_size_px,
            include_box_padding=include_box_padding,
        )
    else:
        content_w_in = _estimate_text_width_px(
            text,
            font_size_px,
            monospace=monospace_text,
            letter_spacing=style.get('letterSpacing', ''),
        ) / PX_PER_IN
    content_w_px = content_w_in * PX_PER_IN

    if shrink_wrap_inline:
        pad_l = parse_px(style.get('paddingLeft', ''))
        pad_r = parse_px(style.get('paddingRight', ''))
        border_w = _sum_border_width_px(style, horizontal=True)
        if _is_compact_ui_label(
            text,
            style,
            has_grouped_inline=has_grouped_inline,
            has_inline_boxes=has_inline_boxes,
            monospace_text=monospace_text,
        ):
            inline_text_px = _estimate_compact_label_width_px(
                text,
                font_size_px,
                letter_spacing=style.get('letterSpacing', ''),
            )
            inline_guard_px = 2.0
        else:
            inline_text_px = _estimate_text_width_px(
                text,
                font_size_px,
                monospace=monospace_text,
                letter_spacing=style.get('letterSpacing', ''),
            )
            inline_guard_px = 8.0
        content_w_in = (
            inline_text_px + pad_l + pad_r + border_w + inline_guard_px
        ) / PX_PER_IN
        if has_cjk(text):
            content_w_in *= 1.08
        content_w_px = content_w_in * PX_PER_IN

    if explicit_break_display_heading:
        display_line_width_px = 0.0
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
            line_w = _estimate_text_width_px(
                line,
                font_size_px,
                letter_spacing=style.get('letterSpacing', ''),
            )
            if line_w > display_line_width_px:
                display_line_width_px = line_w
        heading_wrap_guard = min(max(font_size_px * 0.34 / PX_PER_IN, 0.18), 0.30)
        mixed_script_guard = 0.0
        if has_cjk(text) and has_latin_word(text):
            mixed_script_guard = min(max(font_size_px * 0.10 / PX_PER_IN, 0.08), 0.16)
        content_w_in = max(
            content_w_in,
            display_line_width_px / PX_PER_IN + heading_wrap_guard + mixed_script_guard,
        )
        content_w_px = content_w_in * PX_PER_IN

    # Determine final width in inches
    width_in = None
    if explicit_w > 0:
        width_in = explicit_w / PX_PER_IN
    elif shrink_wrap_inline:
        cap_w_in = max_w / PX_PER_IN if max_w > 0 else (content_width_px / PX_PER_IN if content_width_px else (13.33 - 1.0))
        width_in = min(content_w_in, cap_w_in)
    elif is_inline_block and max_w > 0:
        # For inline-block with max-width: use max line width capped by max-width
        # For multi-line text, compute the widest line, not total text width
        # Include horizontal padding in width calculation
        pad_l = parse_px(style.get('paddingLeft', ''))
        pad_r = parse_px(style.get('paddingRight', ''))
        h_pad_px = pad_l + pad_r
        max_line_px = 0.0
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
            line_cjk = sum(1 for c in line if ord(c) > 127)
            line_latin = len(line) - line_cjk
            line_w = line_cjk * font_size_px + line_latin * font_size_px * 0.55
            if line_w > max_line_px:
                max_line_px = line_w
        width_in = min(max_line_px + h_pad_px, max_w) / PX_PER_IN
    elif is_inline_block and content_width_px and content_width_px > 0:
        # Constrained inline-block: use content-based width, capped by parent constraint
        cw_in = content_width_px / PX_PER_IN
        width_in = min(content_w_in + 0.2, cw_in)  # content width + small padding, capped

    default_w_in = 13.33 - 1.0  # default bounds width
    # Use maxWidth from style or fallback to content_width_px (inherited parent constraint)
    effective_max_w = max_w if max_w > 0 else (content_width_px if content_width_px and content_width_px > 0 else 0)
    preserve_authored_column_width = (
        width_in is None and
        bool(text_contract.get('preferWrapToPreserveSize')) and
        effective_max_w > 0 and
        not component_like_inline
    )
    if preserve_authored_column_width:
        # Contract-driven serif/editorial presets sometimes rely on the authored
        # column width itself as the line-breaking rhythm. If we shrink the text
        # box to natural content width here, later render-time wrapping cannot
        # recreate the source cadence (e.g. Chinese Chan title/body blocks).
        width_in = effective_max_w / PX_PER_IN
    # Cap default width by explicit maxWidth constraint
    if effective_max_w > 0:
        default_w_in = min(default_w_in, effective_max_w / PX_PER_IN)
    if width_in is None:
        # For inline/inline-block elements, use content width; for block, use full width
        if centered_block_command_like:
            pad_l = parse_px(style.get('paddingLeft', ''))
            pad_r = parse_px(style.get('paddingRight', ''))
            border_w = _sum_border_width_px(style, horizontal=True)
            width_in = min(
                (content_w_px + pad_l + pad_r + border_w + 8.0) / PX_PER_IN,
                default_w_in,
            )
        elif is_inline_block or content_w_in < default_w_in * 0.5:
            if is_inline_block:
                # Inline-block: include CSS horizontal padding in width (pills, badges)
                pad_l = parse_px(style.get('paddingLeft', ''))
                pad_r = parse_px(style.get('paddingRight', ''))
                h_pad_in = (pad_l + pad_r) / PX_PER_IN
            else:
                h_pad_in = 0.08
            width_in = min(content_w_in + h_pad_in, default_w_in)
        elif style.get('textAlign', '') == 'center' and effective_max_w > 0 and content_w_in <= default_w_in * 0.92:
            # When text almost fits inside a constrained container (e.g. centered
            # closing cards), keep the text box close to natural content width
            # instead of expanding to the full parent max-width.
            width_in = min(content_w_in + 0.1, default_w_in)
        else:
            width_in = default_w_in

    centered_subtitle_like = (
        tag == 'p' and
        '\n' not in text and
        style.get('textAlign', '') == 'center' and
        effective_max_w > 0 and
        font_size_pt <= 16.0
    )
    if centered_subtitle_like:
        width_in = min(max(width_in, effective_max_w / PX_PER_IN), default_w_in)

    if component_like_inline and '\n' not in text:
        line_count = 1
    elif text_contract.get('preserveAuthoredBreaks') and '\n' in text:
        # When the contract says explicit line breaks are semantic, preserve the
        # authored line count instead of re-estimating extra synthetic wraps and
        # shrinking the typography away from the source deck.
        line_count = max(text.count('\n') + 1, 1)
    else:
        line_count = estimate_wrapped_lines(text, font_size_pt, width_in)

    # Tolerate minor width overflow (up to 5%) for short text without explicit
    # newlines — px_to_pt 96 DPI → 108 PPI slide scale can cause false wraps
    # for CJK text (e.g., "核心 8 项" at 24px → 18pt).
    if (line_count > 1 and '\n' not in text and len(text.strip()) <= 20
            and font_size_pt >= 16):
        cjk_count = sum(1 for c in text if ord(c) > 127)
        latin_count = len(text) - cjk_count
        text_width_in = (cjk_count * font_size_pt * 0.96 + latin_count * font_size_pt * 0.55) / 72.0
        overflow = (text_width_in - width_in) / width_in
        if -0.02 < overflow < 0.10:
            line_count = 1

    if (line_count == 2 and tag == 'p' and '\n' not in text and width_in >= 6.0
            and font_size_pt <= 14.0):
        cjk_count = sum(1 for c in text if ord(c) > 127)
        latin_count = len(text) - cjk_count
        text_width_in = (cjk_count * font_size_pt * 0.88 + latin_count * font_size_pt * 0.52) / 72.0
        overflow = (text_width_in - width_in) / width_in
        if -0.05 < overflow < 0.10:
            line_count = 1

    if (line_count == 2 and tag == 'p' and '\n' not in text and width_in >= 4.5
            and font_size_pt <= 12.0 and len(text.strip()) <= 60):
        cjk_count = sum(1 for c in text if ord(c) > 127)
        latin_count = len(text) - cjk_count
        text_width_in = (cjk_count * font_size_pt * 0.88 + latin_count * font_size_pt * 0.52) / 72.0
        overflow = (text_width_in - width_in) / width_in
        if -0.05 < overflow < 0.10:
            line_count = 1

    prefer_no_wrap_fit = (
        line_count == 1 and
        tag == 'p' and
        '\n' not in text and
        not has_inline_boxes and
        font_size_pt <= 16.0 and
        (
            centered_subtitle_like or
            (width_in >= 4.6 and len(text.strip()) <= 90)
        )
    )

    # Compute line height multiplier from CSS
    lh = style.get('lineHeight', '')
    if lh and 'px' in lh:
        line_height_px = parse_px(lh)
    elif lh and lh.replace('.', '').isdigit():
        line_height_px = font_size_px * float(lh)
    else:
        line_height_px = font_size_px * _default_normal_line_height_multiple(tag)
    total_height_px = line_count * line_height_px

    # Add CSS padding to height (for pill/badge elements with padding)
    pad_t = parse_px(style.get('paddingTop', ''))
    pad_b = parse_px(style.get('paddingBottom', ''))
    if pad_t > 0 or pad_b > 0:
        total_height_px += pad_t + pad_b
    if component_like_inline:
        border_h = _sum_border_width_px(style, horizontal=False)
        total_height_px = max(total_height_px, font_size_px * 1.25 + pad_t + pad_b + border_h + 2.0)

    slide_height_scale = slide_width_px / 13.33
    # Minimum height: 0.15" for small inline elements (pills, badges)
    min_h = 0.15
    if component_like_inline:
        min_h = max(min_h, 0.18)

    gradient_colors = _extract_gradient_colors(style.get('backgroundImage', '')) if _is_gradient_text_style(style) else []
    if len(gradient_colors) == 1:
        gradient_colors = gradient_colors * 2

    text_ir = {
        'type': 'text', 'tag': element.name, 'text': text, 'segments': segments,
        'fragments': fragments,
        'sourceTextRaw': raw_text,
        'hasAuthoredBreaks': '\n' in raw_text,
        'preserveAuthoredBreaks': bool(text_contract.get('preserveAuthoredBreaks')),
        'preferWrapToPreserveSize': bool(text_contract.get('preferWrapToPreserveSize')),
        'shrinkForbidden': bool(text_contract.get('shrinkForbidden')),
        'breakPolicy': text_contract.get('breakPolicy', 'allow_reflow'),
        'overflowStrategy': text_contract.get('overflowStrategy', ''),
        '_text_contract_role': text_contract.get('role'),
        'gradientColors': gradient_colors[:2] if gradient_colors else None, 'textTransform': style.get('textTransform', 'none'),
        'inlineContentWidth': content_w_in,
        'preferContentWidth': has_inline_boxes or has_direct_link_child or has_grouped_inline or shrink_wrap_inline or centered_block_command_like,
        'preferCenteredBlockWidth': has_centered_grouped_command,
        'preferNoWrapFit': prefer_no_wrap_fit,
        'renderInlineBoxOverlays': has_inline_code_or_kbd and has_direct_link_child and '\n' not in text,
        'forceSingleLine': component_like_inline and '\n' not in text,
        'naturalHeight': total_height_px / slide_height_scale,
        'bounds': {
            'x': 0.5, 'y': 0.5,
            'width': width_in,
            'height': max(total_height_px / slide_height_scale, min_h),
        },
        'styles': {
            '_tag': element.name,
            'fontSize': style.get('fontSize', '16px'),
            'fontWeight': style.get('fontWeight', '400'),
            'fontFamily': style.get('fontFamily', ''),
            'letterSpacing': style.get('letterSpacing', ''),
            'color': _style_text_color(style, style.get('color', '')),
            'textAlign': 'center' if centered_block_command_like else style.get('textAlign', 'left'),
            'lineHeight': style.get('lineHeight', 'normal'),
            'listStyleType': style.get('listStyleType', ''),
            'paddingLeft': style.get('paddingLeft', '0px'),
            'paddingRight': style.get('paddingRight', '0px'),
            'paddingTop': style.get('paddingTop', '0px'),
            'paddingBottom': style.get('paddingBottom', '0px'),
            'marginTop': style.get('marginTop', ''),
            'marginBottom': style.get('marginBottom', ''),
            'alignItems': style.get('alignItems', ''),
            'justifyContent': style.get('justifyContent', ''),
            'width': style.get('width', ''),
            'maxWidth': style.get('maxWidth', ''),
            'display': style.get('display', ''),
            'position': style.get('position', ''),
            'top': style.get('top', ''),
            'right': style.get('right', ''),
            'bottom': style.get('bottom', ''),
            'left': style.get('left', ''),
            'transform': style.get('transform', ''),
        },
    }
    if applied_display_heading_boost:
        _set_text_element_font_px(text_ir, parse_px(style.get('fontSize', '16px')) or 16.0)
    return text_ir


def _compute_table_column_widths(rows, table_w):
    """Compute content-aware column widths for a table."""
    if not rows:
        return []
    num_cols = max(len(r['cells']) for r in rows)
    if num_cols == 1:
        return [table_w]

    # Compute max content width per column
    col_max_w = [0.0] * num_cols
    for row in rows:
        for ci, cell in enumerate(row['cells']):
            if ci >= num_cols:
                break
            font_px = parse_px(cell['styles'].get('fontSize', '14px'))
            if font_px <= 0:
                font_px = 14.0
            fragments = cell.get('fragments') or []
            text = cell.get('text', '')
            if fragments:
                text_w = measure_inline_fragments_width_in(fragments, font_px, include_box_padding=True)
            else:
                cjk = sum(1 for c in text if ord(c) > 127)
                latin = len(text) - cjk
                text_w = (cjk * font_px + latin * font_px * 0.55) / PX_PER_IN
            # Add padding
            pad_l = parse_px(cell['styles'].get('paddingLeft', '0px')) / PX_PER_IN
            pad_r = parse_px(cell['styles'].get('paddingRight', '0px')) / PX_PER_IN
            total_w = text_w + pad_l + pad_r + 0.1
            col_max_w[ci] = max(col_max_w[ci], total_w)

    # If total fits, use content widths; otherwise scale proportionally
    total = sum(col_max_w)
    if total <= table_w and total > 0:
        # Distribute extra space proportionally
        scale = table_w / total
        return [w * scale for w in col_max_w]
    elif total > 0:
        # Scale down proportionally
        scale = table_w / total
        return [w * scale for w in col_max_w]
    else:
        # Fallback: equal widths
        return [table_w / num_cols] * num_cols


def _compute_presentation_row_column_widths(rows, table_w):
    """Presentation rows prefer a fitted key column and give the remainder to the value column."""
    if not rows:
        return []
    num_cols = max(len(r.get('cells', [])) for r in rows)
    if num_cols <= 1:
        return [table_w]

    natural_widths = [0.0] * num_cols
    col_texts: List[List[str]] = [[] for _ in range(num_cols)]
    for row in rows:
        for ci, cell in enumerate(row.get('cells', [])):
            if ci >= num_cols:
                break
            font_px = parse_px(cell.get('styles', {}).get('fontSize', '14px'))
            if font_px <= 0:
                font_px = 14.0
            fragments = cell.get('fragments') or []
            text = cell.get('text', '')
            if fragments:
                text_w = measure_inline_fragments_width_in(fragments, font_px, include_box_padding=True)
            else:
                cjk = sum(1 for c in text if ord(c) > 127)
                latin = len(text) - cjk
                text_w = (cjk * font_px + latin * font_px * 0.55) / PX_PER_IN
            pad_l = parse_px(cell.get('styles', {}).get('paddingLeft', '0px')) / PX_PER_IN
            pad_r = parse_px(cell.get('styles', {}).get('paddingRight', '0px')) / PX_PER_IN
            natural_widths[ci] = max(natural_widths[ci], text_w + pad_l + pad_r)
            if text:
                col_texts[ci].append(text)

    if num_cols == 2:
        natural_total = sum(natural_widths)
        if natural_total <= 0:
            return [table_w * 0.36, table_w * 0.64]
        if natural_total >= table_w:
            scale = table_w / natural_total
            return [w * scale for w in natural_widths]

        extra = table_w - natural_total
        left_ratio = natural_widths[0] / natural_total
        extra_left_share = min(0.42, max(0.28, left_ratio * 0.82))
        first_col_texts = [text for text in col_texts[0] if text]
        shortcut_like_first_col = (
            bool(first_col_texts) and
            any(re.search(r'(?:^F\d+$|home|end|space|←|→|↑|↓|/)', text, re.I) for text in first_col_texts) and
            sum(1 for text in first_col_texts if has_cjk(text)) / max(len(first_col_texts), 1) < 0.4
        )
        if shortcut_like_first_col:
            extra_left_share = min(0.50, max(0.36, extra_left_share + 0.08))
        key_w = natural_widths[0] + extra * extra_left_share
        value_w = max(table_w - key_w, 0.90)
        return [key_w, value_w]

    total_natural = sum(natural_widths)
    if total_natural <= 0:
        return [table_w / num_cols] * num_cols
    if total_natural >= table_w:
        scale = table_w / total_natural
        return [w * scale for w in natural_widths]

    extra = table_w - total_natural
    widths = natural_widths[:]
    widths[-1] += extra
    return widths


def _presentation_row_label_color(color_str: str) -> str:
    """Use stronger ink for key labels on light presentation rows."""
    normalized = _normalize_ink_color(color_str)
    if normalized == '#000000':
        return normalized
    rgb = parse_color(color_str)
    if not rgb:
        return '#000000'
    max_channel = max(rgb)
    min_channel = min(rgb)
    if max_channel <= 70 and (max_channel - min_channel) <= 32:
        return '#000000'
    return color_str


def _classify_table_ir(element: Tag, rows: List[Dict[str, Any]]) -> str:
    """Split presentational row lists from real data tables."""
    if not rows:
        return 'table'

    dom_cells = element.find_all(['td', 'th'])
    has_headers = any(cell.get('isHeader') for row in rows for cell in row.get('cells', []))
    has_spans = any(
        int(dom_cell.get('rowspan', '1') or '1') > 1 or int(dom_cell.get('colspan', '1') or '1') > 1
        for dom_cell in dom_cells
    )
    if has_headers or has_spans:
        return 'table'

    row_lengths = [len(row.get('cells', [])) for row in rows if row.get('cells')]
    if not row_lengths:
        return 'table'
    max_cols = max(row_lengths)
    if max_cols > 3:
        return 'table'

    non_empty_cells = [
        cell for row in rows for cell in row.get('cells', [])
        if (cell.get('text') or '').strip()
    ]
    if len(non_empty_cells) < 4 or len(rows) < 3:
        return 'table'

    fragment_total = 0
    box_fragment_total = 0
    short_cell_total = 0
    border_row_total = 0
    for row in rows:
        if any(cell.get('styles', {}).get('borderBottom', '') for cell in row.get('cells', [])):
            border_row_total += 1
        for cell in row.get('cells', []):
            cell_text = (cell.get('text') or '').strip()
            if cell_text and len(cell_text) <= 18:
                short_cell_total += 1
            for fragment in cell.get('fragments') or []:
                if not (fragment.get('text') or '').strip():
                    continue
                fragment_total += 1
                if fragment.get('kind') in INLINE_BOX_KINDS:
                    box_fragment_total += 1

    short_ratio = short_cell_total / max(len(non_empty_cells), 1)
    semantic_density = box_fragment_total / max(fragment_total, 1)
    border_ratio = border_row_total / max(len(rows), 1)
    uniform_rows = len(set(row_lengths)) <= 1

    if uniform_rows and border_ratio >= 0.33 and (semantic_density >= 0.15 or short_ratio >= 0.8):
        return 'presentation_rows'
    return 'table'


def _table_cell_padding_in(styles: Dict[str, str]) -> Tuple[float, float, float, float]:
    """Use CSS padding when present, otherwise fall back to stable textbox margins."""
    pad_l = parse_px(styles.get('paddingLeft', '0px')) / PX_PER_IN
    pad_r = parse_px(styles.get('paddingRight', '0px')) / PX_PER_IN
    pad_t = parse_px(styles.get('paddingTop', '0px')) / PX_PER_IN
    pad_b = parse_px(styles.get('paddingBottom', '0px')) / PX_PER_IN
    return (
        pad_l if pad_l > 0 else (6.0 / 72.0),
        pad_r if pad_r > 0 else (6.0 / 72.0),
        pad_t if pad_t > 0 else (4.0 / 72.0),
        pad_b if pad_b > 0 else (4.0 / 72.0),
    )


def _resolve_table_width_in(style: Dict[str, str], content_width_px: Optional[float]) -> float:
    """Resolve a table width against the local wrapper constraint when available."""
    default_px = 12.33 * PX_PER_IN
    basis_px = content_width_px if content_width_px and content_width_px > 0 else default_px
    table_w_px = basis_px

    explicit_w = _resolve_css_length_with_basis(style.get('width', ''), basis_px)
    if explicit_w > 0:
        table_w_px = explicit_w

    max_w = _resolve_css_length_with_basis(
        style.get('maxWidth', style.get('max-width', '')),
        basis_px,
    )
    if max_w > 0:
        table_w_px = min(table_w_px, max_w)

    min_w = _resolve_css_length_with_basis(
        style.get('minWidth', style.get('min-width', '')),
        basis_px,
    )
    if min_w > 0:
        table_w_px = max(table_w_px, min_w)

    if content_width_px and content_width_px > 0:
        table_w_px = min(table_w_px, content_width_px)

    return max(table_w_px / PX_PER_IN, 0.5)


def _resolve_container_width_in(style: Dict[str, str], content_width_px: Optional[float], slide_width_px: float) -> float:
    """Resolve a layout container width against parent constraints and its own max-width."""
    default_px = slide_width_px - PX_PER_IN
    basis_px = content_width_px if content_width_px and content_width_px > 0 else default_px
    box_w_px = basis_px

    explicit_w = _resolve_css_length_with_basis(style.get('width', ''), basis_px)
    if explicit_w > 0:
        box_w_px = explicit_w

    max_w = _resolve_css_length_with_basis(
        style.get('maxWidth', style.get('max-width', '')),
        basis_px,
    )
    if max_w > 0:
        box_w_px = min(box_w_px, max_w)

    min_w = _resolve_css_length_with_basis(
        style.get('minWidth', style.get('min-width', '')),
        basis_px,
    )
    if min_w > 0:
        box_w_px = max(box_w_px, min_w)

    if content_width_px and content_width_px > 0:
        box_w_px = min(box_w_px, content_width_px)

    return max(box_w_px / PX_PER_IN, 0.5)


def _measure_table_cell_height_in(
    cell: Dict[str, Any],
    cell_w_in: float,
    compact: bool = False,
) -> float:
    """Estimate wrapped table cell height using the final local column width."""
    styles = cell.get('styles', {})
    font_px = parse_px(styles.get('fontSize', '14px'))
    if font_px <= 0:
        font_px = 14.0
    font_pt = px_to_pt(styles.get('fontSize', '14px'))
    fragments = cell.get('fragments') or []
    text = (cell.get('text') or fragments_to_text(fragments)).strip()
    pad_l, pad_r, pad_t, pad_b = _table_cell_padding_in(styles)
    wrap_w_in = max(cell_w_in - pad_l - pad_r, 0.10)

    if fragments:
        raw_line_h = measure_inline_fragments_height_in(fragments, font_px, include_box_padding=True)
        explicit_lines = max(1, (cell.get('text') or '').count('\n') + 1)
        base_line_h = raw_line_h / explicit_lines if explicit_lines > 0 else raw_line_h
    else:
        has_box = False
        base_line_h = (font_px * 1.25) / PX_PER_IN

    has_box = any(frag.get('kind') in INLINE_BOX_KINDS for frag in fragments)
    if compact:
        if has_box:
            base_line_h = min(base_line_h, (font_px * 1.18) / PX_PER_IN)
            base_line_h = max(base_line_h, (font_px * 1.08) / PX_PER_IN)
        else:
            base_line_h = min(base_line_h, (font_px * 1.12) / PX_PER_IN)
            base_line_h = max(base_line_h, (font_px * 1.02) / PX_PER_IN)
    elif has_box:
        base_line_h = max(base_line_h, (font_px * 1.08) / PX_PER_IN)

    line_count = estimate_wrapped_lines(text, font_pt, wrap_w_in) if text else 1
    content_h = max(base_line_h * max(line_count, 1), base_line_h)
    floor = 0.268 if (compact and has_box) else 0.264
    return max(floor, content_h + pad_t + pad_b + 0.02)


def _measure_table_layout(
    rows: List[Dict[str, Any]],
    table_w_in: float,
    ir_type: str,
) -> Tuple[List[float], List[float]]:
    """Compute final column widths and wrapped row heights for a constrained table."""
    if ir_type == 'presentation_rows':
        col_widths = _compute_presentation_row_column_widths(rows, table_w_in)
    else:
        col_widths = _compute_table_column_widths(rows, table_w_in)

    row_heights: List[float] = []
    num_cols = max((len(row.get('cells', [])) for row in rows), default=1)

    current_y = 0.0
    for row in rows:
        row_h = 0.264
        current_x = 0.0
        for col_idx, cell in enumerate(row.get('cells', [])):
            cell_w = col_widths[col_idx] if col_idx < len(col_widths) else (table_w_in / max(num_cols, 1))
            cell_h = _measure_table_cell_height_in(
                cell,
                cell_w,
                compact=(ir_type == 'presentation_rows'),
            )
            row_h = max(row_h, cell_h)
            cell.setdefault('measure', {})['row_height'] = cell_h
            cell['bounds'] = {
                'x': current_x,
                'y': current_y,
                'width': cell_w,
                'height': cell_h,
            }
            current_x += cell_w
        row['height'] = row_h
        row_heights.append(row_h)
        current_y += row_h
        for cell in row.get('cells', []):
            cell['bounds']['height'] = row_h

    return col_widths, row_heights


def build_table_element(
    element: Tag,
    css_rules: List[CSSRule],
    style: Dict[str, str],
    content_width_px: Optional[float] = None,
) -> Dict:
    """Build a table element IR."""
    rows = []
    for tr in element.find_all('tr'):
        is_header = bool(tr.parent and tr.parent.name == 'thead')
        cells = []
        for cell in tr.find_all(['th', 'td']):
            cell_style = compute_inherited_style(cell, css_rules, parent_style=style)
            cell_fragments = extract_inline_fragments(cell, css_rules, cell_style)
            cell_text = fragments_to_text(cell_fragments).strip()
            cell_segments = inline_fragments_to_segments(cell_fragments)
            cells.append({
                'bounds': {'x': 0, 'y': 0, 'width': 2, 'height': 0.4},
                'text': cell_text, 'segments': cell_segments, 'fragments': cell_fragments,
                'isHeader': is_header or cell.name == 'th',
                'styles': {
                    'fontSize': cell_style.get('fontSize', '14px'),
                    'fontWeight': cell_style.get('fontWeight', '400'),
                    'color': _style_text_color(cell_style, cell_style.get('color', '')),
                    'backgroundColor': cell_style.get('backgroundColor', ''),
                    'textAlign': cell_style.get('textAlign', 'left'),
                    'paddingLeft': cell_style.get('paddingLeft', '0px'),
                    'paddingRight': cell_style.get('paddingRight', '0px'),
                    'paddingTop': cell_style.get('paddingTop', '0px'),
                    'paddingBottom': cell_style.get('paddingBottom', '0px'),
                    'fontFamily': cell_style.get('fontFamily', ''),
                    'letterSpacing': cell_style.get('letterSpacing', ''),
                    'borderBottom': cell_style.get('borderBottom', ''),
                    'borderRight': cell_style.get('borderRight', ''),
                },
            })
        if cells:
            for cell in cells:
                font_px = parse_px(cell['styles'].get('fontSize', '14px'))
                if font_px <= 0:
                    font_px = 14.0
                fragments = cell.get('fragments') or []
                if fragments:
                    content_h = measure_inline_fragments_height_in(fragments, font_px, include_box_padding=True)
                else:
                    content_h = (font_px * 1.25) / PX_PER_IN
                cell['measure'] = {
                    'content_width': measure_inline_fragments_width_in(fragments, font_px, include_box_padding=True) if fragments else 0.0,
                    'content_height': content_h,
                    'row_height': 0.264,
                }
            rows.append({'isHeader': is_header, 'cells': cells, 'height': 0.264})
    ir_type = _classify_table_ir(element, rows)
    table_w_in = _resolve_table_width_in(style, content_width_px)
    col_widths, row_heights = _measure_table_layout(rows, table_w_in, ir_type)
    total_h = sum(row_heights)
    return {
        'type': ir_type,
        'bounds': {'x': 0.5, 'y': 1.0, 'width': table_w_in, 'height': max(total_h, len(rows) * 0.264, 0.5)},
        'rows': rows,
        'styles': {
            'fontSize': style.get('fontSize', '14px'),
            'color': _style_text_color(style, style.get('color', '')),
        },
        'measure': {
            'row_heights': row_heights,
            'col_widths': col_widths,
        },
    }


def estimate_wrapped_lines(text: str, font_size_pt: float, box_width_in: float, has_cjk: bool = None) -> int:
    """Estimate visual line count including word wrapping.

    For CJK text: each character is ~1em wide.
    For Latin text: average ~0.5em per character.
    Mixed: use proportion-based estimate.
    """
    if not text or font_size_pt <= 0 or box_width_in <= 0:
        return 1
    # Normalize: split on explicit newlines first
    explicit_lines = text.split('\n')
    total_lines = 0
    for line in explicit_lines:
        if not line.strip():
            total_lines += 1
            continue
        # Calculate character-based width in inches
        cjk_count = sum(1 for c in line if ord(c) > 127)
        latin_count = len(line) - cjk_count
        # Native PPT text is slightly tighter than a naive 1em-per-CJK estimate.
        text_width_in = (cjk_count * font_size_pt * 0.96 + latin_count * font_size_pt * 0.55) / 72.0
        chars_per_line = box_width_in / (text_width_in / len(line)) if line else 1
        if chars_per_line <= 0:
            chars_per_line = 1
        wrapped = max(1, math.ceil(len(line) / chars_per_line))
        total_lines += wrapped
    return max(1, total_lines)


def _is_thin_track_shape(elem: Optional[Dict[str, Any]]) -> bool:
    """Return True for explicit progress/separator bars inside cards."""
    if not elem or elem.get('type') != 'shape' or elem.get('text'):
        return False
    if elem.get('_is_card_bg') or elem.get('_is_decoration') or elem.get('_pair_with'):
        return False
    bounds = elem.get('bounds', {})
    return bounds.get('height', 0.0) <= 0.04 and bounds.get('width', 0.0) >= 1.0


def _looks_like_centered_command_text(elem: Dict[str, Any], styles: Dict[str, str]) -> bool:
    """Detect single-line centered command strings that should shrink-to-fit instead of wrap."""
    text = (elem.get('text') or '').strip()
    if not text or '\n' in text:
        return False
    if styles.get('textAlign', 'left') != 'center':
        return False
    if not _uses_monospace_font(styles.get('fontFamily', '')):
        return False
    return len(text) <= 64


def _estimate_card_copy_lines(
    text: str,
    font_size_pt: float,
    box_width_in: float,
    *,
    following_track: bool = False,
) -> int:
    """Estimate line count for prose inside stacked KPI/progress cards.

    PowerPoint tends to wrap card copy a bit earlier than our generic browser-like
    estimator on wider cards, but a bit tighter on small dense step cards. Use a
    card-specific width model plus a safety floor when a progress bar follows.
    """
    if not text or font_size_pt <= 0 or box_width_in <= 0:
        return 1

    explicit_lines = text.split('\n')
    total_lines = 0
    for raw_line in explicit_lines:
        line = raw_line.strip()
        if not line:
            total_lines += 1
            continue
        cjk_count = sum(1 for c in line if ord(c) > 127)
        latin_count = len(line) - cjk_count
        text_width_in = (cjk_count * font_size_pt * 0.88 + latin_count * font_size_pt * 0.52) / 72.0
        utilization = text_width_in / max(box_width_in, 0.05)
        line_count = max(1, math.ceil(utilization))

        if box_width_in <= 1.45 and len(line) >= 14:
            line_count = max(line_count, 2)
        if following_track and len(line) >= 18 and utilization >= 0.82:
            line_count = max(line_count, 2)

        total_lines += line_count

    return max(1, total_lines)


def _can_single_line_card_copy_with_fit(
    text: str,
    font_size_pt: float,
    box_width_in: float,
) -> bool:
    """Allow wide card prose to stay on one line when shrink-to-fit is plausible."""
    if not text or font_size_pt <= 0 or box_width_in < 4.2:
        return False

    cjk_count = sum(1 for c in text if ord(c) > 127)
    latin_count = len(text) - cjk_count
    adjusted_width_in = (cjk_count * font_size_pt * 0.80 + latin_count * font_size_pt * 0.48) / 72.0
    return adjusted_width_in <= box_width_in * 1.08


def _can_preserve_single_line_contract_heading(
    elem: Dict[str, Any],
    font_size_px: float,
    box_width_in: float,
    *,
    letter_spacing: str = '',
) -> bool:
    """Keep large contract titles on one line when the authored width already fits."""
    text = ' '.join(((elem.get('text', '') or '').replace('\n', ' ')).split())
    if not text or box_width_in <= 0 or font_size_px <= 0:
        return False

    single_line_width_in = _estimate_text_width_px(
        text,
        font_size_px,
        letter_spacing=letter_spacing,
    ) / PX_PER_IN
    width_guard_in = min(max(font_size_px * 0.22 / PX_PER_IN, 0.12), 0.28)
    if has_cjk(text) and has_latin_word(text):
        width_guard_in = min(width_guard_in + 0.06, 0.34)
    return (single_line_width_in + width_guard_in) <= box_width_in


def _remeasure_text_for_final_width(
    elem: Dict[str, Any],
    width_in: float,
    *,
    next_flow_item: Optional[Dict[str, Any]] = None,
    inside_card: bool = False,
) -> None:
    """Recompute text height after layout narrows/widens the final text frame.

    build_text_element() only knows the provisional local width. Cards often
    tighten that width later (e.g. grid track width), so the line count must be
    recomputed against the final card content width before row heights are frozen.
    """
    if not elem or elem.get('type') != 'text':
        return

    bounds = elem.get('bounds', {})
    width_in = max(width_in, 0.05)
    bounds['width'] = width_in

    text = elem.get('text', '')
    styles = elem.get('styles', {})
    font_size_px = parse_px(styles.get('fontSize', '16px'))
    if font_size_px <= 0:
        font_size_px = 16.0
    font_size_pt = px_to_pt(styles.get('fontSize', '16px'))
    if font_size_pt <= 0:
        font_size_pt = 12.0

    tag = (elem.get('tag') or '').lower()
    prefers_card_wrap_safety = (
        inside_card and
        tag == 'p' and
        _is_thin_track_shape(next_flow_item)
    )

    if elem.get('forceSingleLine') or (elem.get('preferNoWrapFit') and not prefers_card_wrap_safety):
        line_count = 1
    else:
        looks_like_card_copy = (
            inside_card and
            tag in ('p', 'div', 'span') and
            '\n' not in text and
            font_size_pt <= 16.0 and
            len(text.strip()) <= 140
        )
        if looks_like_card_copy:
            following_track = _is_thin_track_shape(next_flow_item)
            if (not following_track) and _can_single_line_card_copy_with_fit(text, font_size_pt, width_in):
                line_count = 1
                elem['preferNoWrapFit'] = True
            else:
                elem['preferNoWrapFit'] = False
                line_count = _estimate_card_copy_lines(
                    text,
                    font_size_pt,
                    width_in,
                    following_track=following_track,
                )
        else:
            line_count = estimate_wrapped_lines(text, font_size_pt, width_in)

    lh = styles.get('lineHeight', '')
    if lh and 'px' in lh:
        line_height_px = parse_px(lh)
    elif lh and lh.replace('.', '').isdigit():
        line_height_px = font_size_px * float(lh)
    else:
        line_height_px = font_size_px * 0.82

    total_height_px = line_count * line_height_px
    pad_t = parse_px(styles.get('paddingTop', ''))
    pad_b = parse_px(styles.get('paddingBottom', ''))
    if pad_t > 0 or pad_b > 0:
        total_height_px += pad_t + pad_b

    slide_height_scale = 1440.0 / 13.33
    min_h = 0.18 if elem.get('forceSingleLine') or elem.get('preferContentWidth') else 0.15
    natural_h = max(total_height_px / slide_height_scale, min_h)
    bounds['height'] = natural_h
    elem['naturalHeight'] = natural_h


def _normalize_card_group_text_metrics(group: List[Dict[str, Any]], item_width_in: float) -> None:
    """Adjust flow-box/group text widths and heights to the final card slot width."""
    if not group:
        return
    bg_shape = next((e for e in group if e.get('_is_card_bg')), None)
    if not bg_shape:
        return

    pad_l = bg_shape.get('_css_pad_l', 0.0)
    pad_r = bg_shape.get('_css_pad_r', 0.0)
    border_l = bg_shape.get('_css_border_l', 0.0)
    content_w = max(item_width_in - pad_l - pad_r - border_l, 0.2)
    flow_items = _iter_group_flow_items(group)
    next_flow_by_id = {
        id(flow_items[idx]): flow_items[idx + 1]
        for idx in range(len(flow_items) - 1)
    }

    for elem in flow_items:
        if elem.get('type') != 'text':
            continue
        styles = elem.get('styles', {})
        text_align = styles.get('textAlign', bg_shape.get('_css_text_align', 'left'))
        tag = (elem.get('tag') or '').lower()
        is_block_text = tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li')
        command_like = _looks_like_centered_command_text(elem, styles)

        if command_like:
            elem['preferNoWrapFit'] = True
            target_w = content_w
        elif elem.get('_pair_with') or is_block_text:
            target_w = content_w
        else:
            target_w = min(elem.get('bounds', {}).get('width', content_w), content_w)

        _remeasure_text_for_final_width(
            elem,
            target_w,
            next_flow_item=next_flow_by_id.get(id(elem)),
            inside_card=True,
        )

        base_x = pad_l + border_l
        if text_align == 'center':
            if target_w >= content_w - 0.01:
                elem['bounds']['x'] = base_x
            else:
                elem['bounds']['x'] = base_x + max((content_w - elem['bounds']['width']) / 2.0, 0.0)
        elif tag in ('p', 'li', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'):
            elem['bounds']['x'] = base_x

    start_y = min((elem.get('bounds', {}).get('y', 0.0) for elem in flow_items), default=bg_shape.get('_css_pad_t', 0.0))
    flow_gaps = {
        id(flow_items[idx]): _flow_gap_in(flow_items[idx], flow_items[idx + 1], 0.05)
        for idx in range(len(flow_items) - 1)
    }
    y_shift_by_id: Dict[int, float] = {}
    cursor_y = start_y
    for elem in flow_items:
        bounds = elem.get('bounds', {})
        old_y = bounds.get('y', 0.0)
        new_y = cursor_y
        delta_y = new_y - old_y
        if abs(delta_y) > 1e-6:
            bounds['y'] = new_y
            if elem.get('type') == 'container' and elem.get('_children_relative'):
                _shift_container_descendants(elem, 0.0, delta_y)
        y_shift_by_id[id(elem)] = delta_y
        cursor_y += bounds.get('height', 0.0) + flow_gaps.get(id(elem), 0.0)

    prev_anchor: Optional[Dict[str, Any]] = None
    for elem in group:
        if elem is bg_shape:
            continue
        if elem.get('_is_decoration') and prev_anchor is not None:
            elem['bounds']['y'] = elem.get('bounds', {}).get('y', 0.0) + y_shift_by_id.get(id(prev_anchor), 0.0)
            continue
        if elem in flow_items:
            prev_anchor = elem

    slot_model = bg_shape.get('_component_slot_model') or {}
    if slot_model.get('layout') == 'vertical_card' and slot_model.get('bottom_anchor_last_slot'):
        _apply_vertical_card_slot_layout(
            group,
            bg_shape.get('_css_pad_t', 0.0),
            bg_shape.get('_css_pad_b', 0.0),
            bg_shape.get('bounds', {}).get('height', 0.0),
            slot_model,
        )


def _cjk_correct_width(has_border: bool, text: str, width_in: float, is_condensed: bool) -> float:
    """Apply CJK/condensed font width correction."""
    if is_condensed:
        return width_in * 1.50
    if has_border and has_cjk(text) and width_in < 3.0:
        return width_in * CJK_BOX_FACTOR
    return width_in


def _shift_container_descendants(container: Dict[str, Any], dx: float, dy: float) -> None:
    """Shift all descendant bounds of a relative-positioned container."""
    for child in container.get('children', []):
        cb = child.get('bounds', {})
        cb['x'] = cb.get('x', 0.0) + dx
        cb['y'] = cb.get('y', 0.0) + dy
        if child.get('type') == 'freeform':
            child['points'] = [(px + dx, py + dy) for px, py in (child.get('points') or [])]
        if child.get('type') == 'container' and child.get('_children_relative'):
            _shift_container_descendants(child, cb.get('x', 0.0), cb.get('y', 0.0))


def _translate_container_descendants(container: Dict[str, Any], dx: float, dy: float) -> None:
    """Apply the same delta to every descendant in a relative container tree."""
    for child in container.get('children', []):
        cb = child.get('bounds', {})
        cb['x'] = cb.get('x', 0.0) + dx
        cb['y'] = cb.get('y', 0.0) + dy
        if child.get('type') == 'freeform':
            child['points'] = [(px + dx, py + dy) for px, py in (child.get('points') or [])]
        if child.get('type') == 'container' and child.get('_children_relative'):
            _translate_container_descendants(child, dx, dy)


def _normalize_relative_container(container: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize a relative container so descendants are anchored from (0, 0)."""
    if not container or container.get('type') != 'container' or not container.get('_children_relative'):
        return container

    children = container.get('children', [])
    if not children:
        container.setdefault('bounds', {}).update({'x': 0.0, 'y': 0.0})
        return container

    for child in children:
        if child.get('type') == 'container' and child.get('_children_relative'):
            cb = child.get('bounds', {})
            orig_x = cb.get('x', 0.0)
            orig_y = cb.get('y', 0.0)
            _normalize_relative_container(child)
            child.get('bounds', {})['x'] = orig_x
            child.get('bounds', {})['y'] = orig_y

    min_x = min(child.get('bounds', {}).get('x', 0.0) for child in children)
    min_y = min(child.get('bounds', {}).get('y', 0.0) for child in children)
    max_x = max(child.get('bounds', {}).get('x', 0.0) + child.get('bounds', {}).get('width', 0.0) for child in children)
    max_y = max(child.get('bounds', {}).get('y', 0.0) + child.get('bounds', {}).get('height', 0.0) for child in children)

    for child in children:
        cb = child.get('bounds', {})
        cb['x'] = cb.get('x', 0.0) - min_x
        cb['y'] = cb.get('y', 0.0) - min_y

    container['bounds'] = {
        'x': 0.0,
        'y': 0.0,
        'width': max(max_x - min_x, 0.1),
        'height': max(max_y - min_y, 0.1),
    }
    return container


def _pack_relative_block_container(
    element: Tag,
    style: Dict[str, str],
    children: List[Dict[str, Any]],
) -> Optional[Dict[str, Any]]:
    """Wrap already-extracted block children into a relative flow container."""
    if not children:
        return None

    explicit_gap = style.get('gap', style.get('gridGap', ''))
    default_gap = parse_px(explicit_gap) / PX_PER_IN if explicit_gap else 0.05
    packed_items: List[Dict[str, Any]] = []
    idx = 0
    while idx < len(children):
        child = children[idx]
        pair_id = child.get('_pair_with')
        item_children = [child]
        idx += 1
        if pair_id:
            while idx < len(children) and children[idx].get('_pair_with') == pair_id:
                item_children.append(children[idx])
                idx += 1

        item_min_x = min(item.get('bounds', {}).get('x', 0.0) for item in item_children)
        item_min_y = min(item.get('bounds', {}).get('y', 0.0) for item in item_children)
        item_max_right = max(
            item.get('bounds', {}).get('x', 0.0) + item.get('bounds', {}).get('width', 0.0)
            for item in item_children
        )
        item_max_bottom = max(
            item.get('bounds', {}).get('y', 0.0) + item.get('bounds', {}).get('height', 0.0)
            for item in item_children
        )
        flow_anchor = next(
            (item for item in _iter_group_flow_items(item_children) if item.get('type') == 'text'),
            None,
        )
        if flow_anchor is None:
            flow_anchor = next(iter(_iter_group_flow_items(item_children)), item_children[0])
        packed_items.append({
            'children': item_children,
            'min_x': item_min_x,
            'min_y': item_min_y,
            'width': max(item_max_right - item_min_x, 0.0),
            'height': max(item_max_bottom - item_min_y, 0.0),
            'anchor': flow_anchor,
        })

    current_y = 0.0
    max_right = 0.0
    center_children = style.get('textAlign', '') == 'center'

    for item_idx, item in enumerate(packed_items):
        # Normalize each item's leftmost child to x=0 relative to the packed
        # container. Previously we used a single global min_x, but inner
        # children produced by different code paths (e.g. flex-row containers
        # vs. inline spans) may report inconsistent local origins, leaving
        # one item at x=0.5 and another at x=0.0 within the same packed flow.
        for child in item['children']:
            cb = child.get('bounds', {})
            cb['x'] = cb.get('x', 0.0) - item['min_x']
            cb['y'] = current_y + (cb.get('y', 0.0) - item['min_y'])
            max_right = max(max_right, cb.get('x', 0.0) + cb.get('width', 0.0))
        if item_idx < len(packed_items) - 1:
            current_y += item['height'] + _flow_gap_in(item['anchor'], packed_items[item_idx + 1]['anchor'], default_gap)
        else:
            current_y += item['height']

    max_width_px = _resolve_css_length_with_basis(
        style.get('maxWidth', style.get('max-width', '')),
        VIEWPORT_WIDTH_PX,
    )
    preserve_explicit_width = (
        max_width_px > 0 and
        any(child.get('type') in ('container', 'table', 'presentation_rows', 'image') for child in children)
    )
    container_width = max(max_right, max_width_px / PX_PER_IN if preserve_explicit_width else 0.1)

    if center_children and container_width > 0:
        for item in packed_items:
            if item['width'] <= 0 or item['width'] >= container_width - 0.01:
                continue
            current_item_min_x = min(child.get('bounds', {}).get('x', 0.0) for child in item['children'])
            target_min_x = max((container_width - item['width']) / 2.0, 0.0)
            delta_x = target_min_x - current_item_min_x
            if abs(delta_x) < 1e-6:
                continue
            for child in item['children']:
                child.get('bounds', {})['x'] = child.get('bounds', {}).get('x', 0.0) + delta_x

    return {
        'type': 'container',
        'tag': element.name,
        'bounds': {
            'x': 0.0,
            'y': 0.0,
            'width': max(container_width, 0.1),
            'height': max(current_y, 0.1),
        },
        'styles': style,
        'children': children,
        '_children_relative': True,
    }


def _measure_group_intrinsic_width_in(group: List[Dict[str, Any]]) -> float:
    """Measure the actual horizontal extent of a grouped item.

    This keeps centered flex-wrap rows from over-allocating width to packed
    child containers such as KPI metric stacks (number + label) where the
    intrinsic width is much narrower than the row's heuristic track width.
    """
    if not group:
        return 0.0

    visible = [
        elem for elem in group
        if not (
            elem.get('type') == 'shape' and (
                elem.get('_is_decoration') or
                elem.get('_is_card_bg') or
                elem.get('_is_border_left')
            )
        )
    ]
    if not visible:
        visible = group

    min_x = min(elem.get('bounds', {}).get('x', 0.0) for elem in visible)
    max_right = max(
        elem.get('bounds', {}).get('x', 0.0) + elem.get('bounds', {}).get('width', 0.0)
        for elem in visible
    )
    return max(max_right - min_x, 0.0)


def _build_explicit_track_elements(
    element: Tag,
    style: Dict[str, str],
    css_rules: List[CSSRule],
    slide_width_px: float,
    content_width_px: Optional[float],
) -> Optional[List[Dict[str, Any]]]:
    """Build thin decorative track/fill elements with explicit CSS height."""
    if _detect_flex_container(style) or _is_grid_container(style):
        return None
    if get_text_content(element).strip():
        return None

    css_h = parse_px(style.get('height', ''))
    if css_h <= 0 or not has_visible_bg_or_border(style):
        return None

    child_tags = [c for c in element.children if isinstance(c, Tag)]
    if any(get_text_content(child).strip() for child in child_tags):
        return None

    basis_px = parse_px(style.get('width', ''))
    if basis_px <= 0:
        basis_px = content_width_px or 0.0
    if basis_px <= 0:
        # Hero slides often place thin divider tracks directly under the slide
        # root without an intermediate max-width content wrapper. Fall back to
        # the authored slide inner width instead of the generic 1" block path.
        basis_px = max((SLIDE_W_IN - 1.0) * PX_PER_IN, 0.0)
    if basis_px <= 0:
        return None

    track_w_px = _resolve_css_length_with_basis(style.get('width', '100%'), basis_px)
    track_h_px = css_h
    if track_w_px <= 0 or track_h_px <= 0:
        return None

    track_shape = build_shape_element(element, style, slide_width_px)
    track_shape['bounds'] = {
        'x': 0.0,
        'y': 0.0,
        'width': track_w_px / PX_PER_IN,
        'height': track_h_px / PX_PER_IN,
    }

    # Simple empty dividers still need to export as a thin track shape instead
    # of falling back to the generic 12.33" x 1.0" block placeholder path.
    results = [track_shape]
    if not child_tags:
        return results

    for child in child_tags:
        child_style = compute_element_style(child, css_rules, child.get('style', ''), style)
        if not _has_drawable_background(child_style):
            continue
        child_w_px = _resolve_css_length_with_basis(child_style.get('width', '100%'), track_w_px)
        child_h_px = _resolve_css_length_with_basis(child_style.get('height', '100%'), track_h_px)
        if child_w_px <= 0 or child_h_px <= 0:
            continue
        fill_shape = build_shape_element(child, child_style, slide_width_px)
        fill_shape['bounds'] = {
            'x': 0.0,
            'y': 0.0,
            'width': child_w_px / PX_PER_IN,
            'height': child_h_px / PX_PER_IN,
        }
        fill_shape['_is_decoration'] = True
        results.append(fill_shape)

    return results if len(results) > 1 else None


def measure_flow_box(
    element: Tag,
    css_rules: List[CSSRule],
    parent_style: Optional[Dict[str, str]] = None,
    slide_width_px: float = 1440,
    content_width_px: float = None,
    local_origin: bool = True,
    contract: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    """Promote a visible flex card into a first-class container."""
    if not element or not getattr(element, 'name', None):
        return None

    style = compute_element_style(element, css_rules, element.get('style', ''), parent_style)
    if not _detect_flex_container(style) or not has_visible_bg_or_border(style):
        return None
    direct_tag_children = [c for c in element.children if isinstance(c, Tag)]
    if len(direct_tag_children) < 2:
        return None

    children = build_grid_children(
        element,
        css_rules,
        style,
        slide_width_px,
        content_width_px,
        local_origin=local_origin,
        contract=contract,
    )
    if not children:
        return None

    _expand_padding(style)
    pad_l = parse_px(style.get('paddingLeft', '0px')) / PX_PER_IN
    pad_r = parse_px(style.get('paddingRight', '0px')) / PX_PER_IN
    pad_t = parse_px(style.get('paddingTop', '0px')) / PX_PER_IN
    pad_b = parse_px(style.get('paddingBottom', '0px')) / PX_PER_IN
    border_l = parse_px(
        style.get(
            'borderLeftWidth',
            style.get('borderLeft', '0px').split()[0] if style.get('borderLeft', '') else '0px'
        )
    ) / PX_PER_IN

    min_child_x = min((c['bounds'].get('x', 0.0) for c in children), default=0.0)
    child_origin_x = max(min_child_x - (pad_l + border_l), 0.0)
    for child in children:
        child['bounds']['x'] -= child_origin_x

    css_w = parse_px(style.get('width', ''))
    css_maxw = parse_px(style.get('maxWidth', ''))
    display = style.get('display', '')
    prefers_intrinsic_width = (
        'inline-flex' in display and
        css_w <= 0 and
        css_maxw <= 0 and
        parse_px(style.get('minWidth', '')) <= 0
    )
    if css_maxw > 0:
        card_w = css_maxw / PX_PER_IN
    elif css_w > 0:
        card_w = css_w / PX_PER_IN
    elif prefers_intrinsic_width:
        max_right = max((c['bounds']['x'] + c['bounds']['width'] for c in children), default=0.0)
        card_w = max_right + pad_r
    elif content_width_px and content_width_px > 0:
        card_w = content_width_px / PX_PER_IN
    else:
        max_right = max((c['bounds']['x'] + c['bounds']['width'] for c in children), default=0.0)
        card_w = max_right + pad_r

    content_top = min(
        (c['bounds']['y'] for c in children if not c.get('_skip_layout')),
        default=pad_t,
    )
    content_bottom = max(
        (c['bounds']['y'] + c['bounds']['height'] for c in children if not c.get('_skip_layout')),
        default=pad_t + pad_b,
    )
    content_extent = max(content_bottom - content_top, 0.0)
    card_h = content_extent + pad_t + pad_b

    # Children coming from build_grid_children() usually start at y=0.0.
    # Shift real content down by the card's own top padding so flow_box cards
    # don't visually pin text to the top edge.
    child_y_offset = max(pad_t - content_top, 0.0)
    if child_y_offset > 0:
        for child in children:
            child['bounds']['y'] += child_y_offset

    card_content_w = max(card_w - pad_l - pad_r - border_l, 0.0)
    for child in children:
        if child.get('type') != 'text' or child.get('tag') not in INLINE_TAGS:
            continue
        child_styles = child.get('styles', {})
        if child_styles.get('display', '') != 'inline-flex':
            continue
        if any(
            child_styles.get(key, '')
            for key in ('backgroundColor', 'border', 'borderLeft', 'borderRight', 'borderTop', 'borderBottom')
        ):
            continue
        if parse_px(child_styles.get('width', '')) > 0 or parse_px(child_styles.get('maxWidth', '')) > 0:
            continue
        child['bounds']['x'] = pad_l + border_l
        if card_content_w > 0:
            child['bounds']['width'] = card_content_w

    bg_shape = build_shape_element(element, style, slide_width_px)
    for border_key in ('border', 'borderLeft', 'borderRight', 'borderTop', 'borderBottom'):
        bg_shape['styles'][border_key] = ''
    bg_shape['bounds'] = {
        'x': 0.0,
        'y': 0.0,
        'width': card_w,
        'height': card_h,
    }
    bg_shape['_is_card_bg'] = True
    bg_shape['_skip_layout'] = True
    bg_shape['_css_pad_l'] = pad_l
    bg_shape['_css_pad_r'] = pad_r
    bg_shape['_css_pad_t'] = pad_t
    bg_shape['_css_pad_b'] = pad_b
    bg_shape['_css_border_l'] = border_l

    bl = style.get('borderLeft', '')
    if bl and 'none' not in bl and not bl.startswith('0px'):
        bg_shape['styles']['borderLeft'] = bl

    flow_children = [bg_shape]
    flow_children.extend(children)
    _normalize_card_group_text_metrics(flow_children, card_w)
    _mark_flow_box_descendants(flow_children)
    intrinsic_h = max((c['bounds']['y'] + c['bounds']['height'] for c in flow_children), default=card_h)

    return {
        'type': 'container',
        'tag': element.name,
        'layout': 'flow_box',
        'bounds': {'x': 0.5, 'y': 0.5, 'width': card_w, 'height': intrinsic_h},
        'styles': style,
        'children': flow_children,
        '_children_relative': True,
        'measure': {
            'intrinsic_width': card_w,
            'intrinsic_height': intrinsic_h,
        },
    }


def _measure_preferred_child_width_in(
    child: Tag,
    child_style: Dict[str, str],
    css_rules: List[CSSRule],
    slide_width_px: float,
) -> float:
    """Measure natural width for component-like text children before flex slotting."""
    child_tag = child.name.lower()
    if child_tag not in TEXT_TAGS and not is_leaf_text_container(child, css_rules):
        return 0.0
    text_el = build_text_element(child, child_style, css_rules, slide_width_px, None)
    if not text_el or not text_el.get('preferContentWidth'):
        return 0.0
    return text_el.get('bounds', {}).get('width', 0.0)


def _measure_compact_flex_child_width_in(
    child: Tag,
    child_style: Dict[str, str],
    css_rules: List[CSSRule],
    slide_width_px: float,
    cap_in: float,
) -> float:
    """Intrinsic width for a compact flex-row child (stacked block descendants OK).

    For text/leaf children: defer to `_measure_preferred_child_width_in()`.
    For container children that wrap stacked block descendants (e.g. a stat
    block with a numeric div above a label div), return the widest descendant
    text line instead of dividing the row width evenly.
    """
    if cap_in <= 0:
        return 0.0
    text_w = _measure_preferred_child_width_in(child, child_style, css_rules, slide_width_px)
    if text_w > 0:
        return min(text_w, cap_in)
    natural = compute_text_content_width(child, css_rules, child_style)
    widest = 0.0
    for desc in child.descendants:
        if not isinstance(desc, Tag):
            continue
        desc_tag = desc.name.lower()
        if desc_tag not in TEXT_TAGS and not is_leaf_text_container(desc, css_rules):
            continue
        text = get_text_content(desc).strip()
        if not text:
            continue
        desc_style = compute_element_style(desc, css_rules, desc.get('style', ''), child_style)
        font_px = parse_px(desc_style.get('fontSize', '16px')) or 16.0
        cjk = sum(1 for c in text if ord(c) > 127)
        latin = len(text) - cjk
        # Use slightly looser multipliers so a borderline single-line measurement
        # (e.g. "21" at 48px) doesn't trip the wrap engine into 2 lines downstream.
        approx = (cjk * font_px * 1.0 + latin * font_px * 0.62) / PX_PER_IN
        if approx > widest:
            widest = approx
    if widest <= 0 and natural > 0:
        widest = natural
    if widest <= 0:
        return 0.0
    _expand_padding(child_style)
    widest += (
        parse_px(child_style.get('paddingLeft', '0px')) +
        parse_px(child_style.get('paddingRight', '0px'))
    ) / PX_PER_IN
    # Add a small safety margin to keep single-line text from wrapping at the
    # measured boundary in PPTX's text engine.
    widest += 0.05
    return min(widest, cap_in)


def _estimate_group_baseline_in(group: List[Dict[str, Any]], bg_shape: Optional[Dict[str, Any]] = None) -> float:
    """Approximate the first-baseline position for flex-row baseline alignment."""
    first_text = None
    for elem in group:
        if elem.get('type') == 'text':
            first_text = elem
            break

    top_pad = bg_shape.get('_css_pad_t', 0.0) if bg_shape else 0.0
    if not first_text:
        return top_pad + max((e.get('bounds', {}).get('height', 0.2) for e in group), default=0.2) * 0.75

    tb = first_text.get('bounds', {})
    rel_y = tb.get('y', 0.0)
    text_h = tb.get('height', 0.2)
    font_px = parse_px(first_text.get('styles', {}).get('fontSize', '16px')) or 16.0
    line_h = parse_px(first_text.get('styles', {}).get('lineHeight', '')) / PX_PER_IN
    if line_h <= 0:
        line_h = font_px * 1.0 / PX_PER_IN
    centered_line_top = max((text_h - line_h) / 2.0, 0.0)
    baseline_from_text_top = centered_line_top + min(line_h * 0.80, text_h * 0.92)
    return top_pad + rel_y + baseline_from_text_top


def _flow_gap_in(
    current: Optional[Dict[str, Any]],
    nxt: Optional[Dict[str, Any]],
    default_gap: float,
) -> float:
    """Approximate block-flow spacing using collapsed margins when present."""
    if not current or not nxt:
        return default_gap
    if current.get('tag') == 'li':
        return 7.0 / PX_PER_IN

    current_styles = current.get('styles', {})
    next_styles = nxt.get('styles', {})
    mb = parse_px(current_styles.get('marginBottom', '')) / PX_PER_IN
    mt = parse_px(next_styles.get('marginTop', '')) / PX_PER_IN
    gap = default_gap if (mb == 0 and mt == 0) else (mb + mt if mb < 0 or mt < 0 else max(mb, mt))

    # KPI/progress cards look much closer to browser layout when multi-line body
    # copy leaves a stable runway before the following thin track.
    if _is_thin_track_shape(nxt) and current.get('type') == 'text':
        font_px = parse_px(current_styles.get('fontSize', '16px'))
        if font_px <= 0:
            font_px = 16.0
        line_h_px = parse_px(current_styles.get('lineHeight', ''))
        if line_h_px <= 0:
            line_h_px = font_px * 1.0
        multiline_like = (
            '\n' in (current.get('text') or '') or
            current.get('bounds', {}).get('height', 0.0) > (line_h_px * 1.45) / PX_PER_IN
        )
        gap_floor = (14.0 if multiline_like else 10.0) / PX_PER_IN
        gap = max(gap, gap_floor)

    # Compact KPI / workflow cards often start with a large numeric step label
    # followed by a short heading. HTML margin-bottom alone tends to collapse too
    # aggressively after text remeasurement, so keep a stable optical gap.
    if current.get('type') == 'text' and nxt.get('type') == 'text':
        cur_text = (current.get('text') or '').strip()
        nxt_text = (nxt.get('text') or '').strip()
        cur_font_px = parse_px(current_styles.get('fontSize', ''))
        nxt_font_px = parse_px(next_styles.get('fontSize', ''))
        cur_weight = str(current_styles.get('fontWeight', ''))
        nxt_weight = str(next_styles.get('fontWeight', ''))
        if (
            re.fullmatch(r'(?:\d{1,2}|[A-Z]{1,3}\d?)', cur_text) and
            nxt_text and
            cur_font_px >= 20.0 and
            nxt_font_px >= 13.0 and
            (cur_weight.isdigit() and int(cur_weight) >= 700 or cur_weight in {'bold', 'bolder'}) and
            (nxt_weight.isdigit() and int(nxt_weight) >= 600 or nxt_weight in {'bold', 'bolder'}) and
            cur_font_px >= nxt_font_px * 1.35
        ):
            gap = max(gap, 10.0 / PX_PER_IN)

    return gap


def _iter_group_flow_items(group: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Return group elements that should participate in vertical flow measurement."""
    flow_items: List[Dict[str, Any]] = []
    for elem in group:
        if elem.get('_skip_layout'):
            continue
        if elem.get('_is_card_bg') or elem.get('_is_border_left') or elem.get('_is_decoration'):
            continue
        if elem.get('type') == 'shape' and elem.get('_pair_with'):
            continue
        flow_items.append(elem)
    return flow_items


def _measure_group_flow_height(group: List[Dict[str, Any]], default_gap: float = 0.05) -> float:
    """Measure stacked block-flow height for a laid-out grid group."""
    flow_items = _iter_group_flow_items(group)
    if not flow_items:
        return 0.0

    total = 0.0
    for idx, elem in enumerate(flow_items):
        total += elem.get('bounds', {}).get('height', 0.0)
        if idx < len(flow_items) - 1:
            total += _flow_gap_in(elem, flow_items[idx + 1], default_gap)
    return total


def _stretch_relative_card_container_to_height(elem: Dict[str, Any], target_h: float) -> None:
    """Stretch a relative card container to match a shared grid row height."""
    if target_h <= 0:
        return
    bounds = elem.get('bounds', {})
    current_h = bounds.get('height', 0.0)
    if current_h <= 0 or target_h <= current_h + 1e-6:
        return

    bounds['height'] = target_h
    card_bg = next(
        (child for child in elem.get('children', []) if child.get('_is_card_bg')),
        None,
    )
    if card_bg:
        card_bg.setdefault('bounds', {})
        card_bg['bounds']['height'] = target_h


def _stretch_relative_card_container_to_width(elem: Dict[str, Any], target_w: float) -> None:
    """Stretch a relative card container to the assigned grid/flex slot width."""
    if target_w <= 0:
        return

    bounds = elem.get('bounds', {})
    current_w = bounds.get('width', 0.0)
    if abs(target_w - current_w) <= 1e-6:
        return

    bounds['width'] = target_w
    card_bg = next(
        (child for child in elem.get('children', []) if child.get('_is_card_bg')),
        None,
    )
    if not card_bg:
        return

    card_bg.setdefault('bounds', {})
    card_bg['bounds']['width'] = target_w
    _normalize_card_group_text_metrics(elem.get('children', []), target_w)
    bounds['height'] = max(
        (
            child.get('bounds', {}).get('y', 0.0) +
            child.get('bounds', {}).get('height', 0.0)
            for child in elem.get('children', [])
        ),
        default=bounds.get('height', 0.0),
    )


def flat_extract(
    element: Tag,
    css_rules: List[CSSRule],
    parent_style: Optional[Dict[str, str]] = None,
    slide_width_px: float = 1440,
    content_width_px: float = None,  # If set, constrains grid/layout width
    local_origin: bool = False,
    contract: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Adapted from browser version's flatExtract.
    Recursively extracts text, shape, table, and image elements from a DOM subtree.
    Positions are computed via a simulated flex-column layout.
    """
    style = compute_element_style(element, css_rules, element.get('style', ''), parent_style)
    tag = element.name.lower()
    is_slide_root = _is_slide_root_element(element)

    if style.get('display', '') == 'none' or style.get('visibility', '') == 'hidden':
        return []

    contract_id = (contract or {}).get('contract_id', '')
    component_name = _contract_component_name(element, contract)
    slot_model = _contract_slot_model(contract, component_name)
    if component_name and slot_model:
        built = _build_contract_component(
            element,
            style,
            css_rules,
            slide_width_px,
            content_width_px,
            contract,
            component_name,
            slot_model,
        )
        if built:
            return built

    # Raster elements
    if tag == 'img':
        img_el = build_image_element(element, style)
        return [img_el] if img_el else []

    if tag == 'svg':
        svg_container = build_svg_container(
            element,
            css_rules,
            parent_style,
            slide_width_px,
            content_width_px,
        )
        return [svg_container] if svg_container else []

    # Tables
    if tag == 'table':
        return [build_table_element(element, css_rules, style, content_width_px=content_width_px)]

    # Text elements (h1-h6, p, li, span, a)
    if tag in TEXT_TAGS:
        # Check for styled inline children that should have their own shapes (pills/badges)
        styled_shapes = []
        pill_elements = set()  # Track which children are pills, to exclude from combined text
        parent_is_inline_group = (
            has_visible_bg_or_border(style) or
            style.get('display', '') in ('flex', 'inline-flex')
        )
        for child in element.children:
            if isinstance(child, Tag) and child.name in INLINE_TAGS:
                # Skip <code> and <kbd> — these are semantic inline elements that should
                # stay as part of the parent text, not extracted as separate pills
                if child.name in ('code', 'kbd'):
                    continue
                child_s = compute_element_style(child, css_rules, child.get('style', ''))
                if has_visible_bg_or_border(child_s) and not parent_is_inline_group:
                    child_text = get_text_content(child).strip()
                    if child_text:
                        pill_elements.add(child)
                        # Estimate shape width from text content
                        cjk = sum(1 for c in child_text if ord(c) > 127)
                        latin = len(child_text) - cjk
                        font_px = parse_px(child_s.get('fontSize', '16px'))
                        if font_px <= 0:
                            font_px = 16.0
                        # Base text width
                        text_w = (cjk * font_px + latin * font_px * 0.55) / PX_PER_IN
                        # Padding (expand shorthand for pill spans only)
                        _expand_padding(child_s)
                        pad_lr = parse_px(child_s.get('paddingLeft', '0px')) / PX_PER_IN
                        pad_rr = parse_px(child_s.get('paddingRight', '0px')) / PX_PER_IN
                        # Height: golden pill height is 0.53" for 14px font
                        # With PX_PER_IN=108: font_px/108 * 4.09 = 0.53
                        shape_w = text_w + pad_lr + pad_rr + 0.1
                        shape_h = font_px / PX_PER_IN * 4.09

                        # CJK width correction for pill shape (same as native version)
                        if cjk > 0:
                            shape_w *= 1.15

                        # Extract borderRadius for proper pill rendering
                        br = child_s.get('borderRadius', '0px')

                        # Get text color for rendering inside pill
                        pill_color = child_s.get('color', '')

                        styled_shapes.append({
                            'type': 'shape', 'tag': 'span',
                            'bounds': {'x': 0.5, 'y': 0.5, 'width': shape_w, 'height': shape_h},
                            'styles': {
                                'backgroundColor': child_s.get('backgroundColor', ''),
                                'border': child_s.get('border', ''),
                                'borderRadius': br,
                            },
                            '_is_pill': True,
                            'pill_text': child_text,
                            'pill_color': pill_color,
                        })

        text_el = build_text_element(element, style, css_rules, slide_width_px, content_width_px,
                                      exclude_elements=pill_elements if pill_elements else None,
                                      contract=contract)

        parent_display = ''
        parent_flex_dir = ''
        parent_align_items = ''
        if parent_style:
            parent_display = parent_style.get('display', '')
            parent_flex_dir = parent_style.get('flexDirection', parent_style.get('flex-direction', ''))
            parent_align_items = parent_style.get('alignItems', parent_style.get('align-items', ''))
        parent_is_flex_column = parent_display in ('flex', 'inline-flex') and parent_flex_dir == 'column'
        parent_stretches_children = parent_align_items in ('', 'stretch', 'normal', 'initial', 'unset')

        # Flex-column containers stretch cross-axis children by default. Inline tags
        # with visible backgrounds should inherit that available width instead of
        # shrink-wrapping to their text content.
        if (text_el and content_width_px and tag in INLINE_TAGS and has_visible_bg_or_border(style)
                and parent_is_flex_column and parent_stretches_children
                and parse_px(style.get('width', '')) <= 0
                and parse_px(style.get('maxWidth', '')) <= 0
                and 'inline-block' not in style.get('display', '')):
            text_el['bounds']['width'] = content_width_px / PX_PER_IN

        if (
            text_el and tag in INLINE_TAGS
            and not has_visible_bg_or_border(style)
            and style.get('display', '') == 'inline-flex'
            and parent_is_flex_column and parent_stretches_children
            and parse_px(style.get('width', '')) <= 0
            and parse_px(style.get('maxWidth', '')) <= 0
        ):
            text_el['_stretch_to_parent_width'] = True

        # Create bg shapes for <code> elements with visible backgrounds.
        # The golden has separate bg shapes for code elements (e.g., Slide 10's
        # "clawhub install kai-slide-creator" with rgba bg).
        # Only create when <code> is the FIRST child (so text alignment is predictable).
        import uuid
        code_bg_shapes = []
        first_child = None
        for child in element.children:
            if isinstance(child, Tag):
                first_child = child
                break
        first_meaningful_child = None
        has_leading_text = False
        for child in element.children:
            if isinstance(child, NavigableString):
                if str(child).strip():
                    has_leading_text = True
                    break
                continue
            if isinstance(child, Tag):
                first_meaningful_child = child
                break
        if (first_meaningful_child and first_meaningful_child.name == 'code' and not has_leading_text
                and not (text_el and text_el.get('renderInlineBoxOverlays'))):
            code_s = compute_element_style(first_meaningful_child, css_rules, first_meaningful_child.get('style', ''))
            if has_visible_bg_or_border(code_s):
                code_text = get_text_content(first_meaningful_child).strip()
                if code_text:
                    _expand_padding(code_s)
                    font_px = parse_px(code_s.get('fontSize', '16px'))
                    if font_px <= 0:
                        font_px = 16.0
                    text_w = _estimate_text_width_px(
                        code_text,
                        font_px,
                        monospace=True,
                        letter_spacing=code_s.get('letterSpacing', ''),
                    ) / PX_PER_IN
                    pad_l = parse_px(code_s.get('paddingLeft', '0px')) / PX_PER_IN
                    pad_r = parse_px(code_s.get('paddingRight', '0px')) / PX_PER_IN
                    pad_t = parse_px(code_s.get('paddingTop', '0px')) / PX_PER_IN
                    pad_b = parse_px(code_s.get('paddingBottom', '0px')) / PX_PER_IN
                    shape_w = text_w + pad_l + pad_r + 0.08
                    shape_h = max(font_px * 1.25 / PX_PER_IN + pad_t + pad_b + 0.03, 0.22)

                    # Composite rgba bg color to solid (golden uses composited color)
                    bg_color = code_s.get('backgroundColor', '')
                    if bg_color and 'rgba' in bg_color:
                        rgba_match = re.match(r'rgba\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*([\d.]+)\s*\)', bg_color)
                        if rgba_match:
                            r, g, b, a = int(rgba_match.group(1)), int(rgba_match.group(2)), int(rgba_match.group(3)), float(rgba_match.group(4))
                            r = int(a * r + (1 - a) * 255)
                            g = int(a * g + (1 - a) * 255)
                            b = int(a * b + (1 - a) * 255)
                            bg_color = f'#{r:02X}{g:02X}{b:02X}'

                    code_bg = {
                        'type': 'shape', 'tag': 'code',
                        'bounds': {'x': 0, 'y': 0, 'width': shape_w, 'height': shape_h},
                        'styles': {
                            'backgroundColor': bg_color or code_s.get('backgroundColor', ''),
                            'borderRadius': code_s.get('borderRadius', '0px'),
                        },
                        '_is_code_bg': True,
                        '_skip_layout': True,
                        '_code_element': [first_meaningful_child],  # Store reference to code element for positioning
                        '_code_pad_l': pad_l,
                    }
                    code_bg_shapes.append(code_bg)

        # Always emit styled pill shapes (decorative — even if parent has no non-pill text)
        results = []
        if styled_shapes:
            for pill in styled_shapes:
                pill['_skip_layout'] = True  # Skip during layout, positioned in post-layout
                results.append(pill)
            # Pills now have embedded text (pill_text), no need for full subtitle text element

        if text_el:
            # Create shape for TEXT_TAGS if there's actual background fill,
            # full border, or border-bottom (list item background containers).
            # The shape acts as a background container that's synced with the text.
            has_bg = (style.get('backgroundColor', '') and
                     style['backgroundColor'] not in ('transparent', 'rgba(0, 0, 0, 0)', ''))
            has_full_border = (style.get('border', '') or
                              style.get('borderLeft', '') or
                              style.get('borderTop', '') or
                              style.get('borderRight', ''))
            has_border_bottom = bool(style.get('borderBottom', ''))
            if has_bg or has_full_border or has_border_bottom:
                shape = build_shape_element(element, style, slide_width_px)
                shape['bounds'] = dict(text_el['bounds'])
                text = get_text_content(element, pill_elements if pill_elements else None).strip()
                ff = style.get('fontFamily', '')
                c = is_condensed_font(ff)
                cjk_w = _cjk_correct_width(True, text, text_el['bounds']['width'], c)
                if cjk_w != text_el['bounds']['width']:
                    shape['bounds']['width'] = cjk_w
                pair_id = str(uuid.uuid4())[:8]
                shape['_pair_with'] = pair_id
                text_el['_pair_with'] = pair_id
                _attach_pair_box_insets(shape, style)
                results.append(shape)

            if code_bg_shapes:
                results.extend(code_bg_shapes)
            results.append(text_el)
            return results

    # Container elements (div, section, article, ul, ol)
    if tag in CONTAINER_TAGS:
        bg_image = style.get('backgroundImage', 'none')
        has_gradient_bg = bg_image != 'none' and 'gradient' in bg_image
        has_url_bg = bg_image != 'none' and 'url(' in bg_image
        total_text = get_text_content(element).strip()
        direct_tag_children = [c for c in element.children if isinstance(c, Tag)]

        # Skip absolute-positioned decorative elements (ambient orbs, cloud layers)
        # These don't appear as shapes in the golden PPTX
        pos = style.get('position', '')
        filter_val = style.get('filter', '')
        pointer_events = style.get('pointerEvents', '')
        if (pos == 'absolute' and not total_text and
            ('blur' in filter_val or pointer_events == 'none')):
            return []
        # Skip cloud layers and other filter-based decorative containers
        if filter_val and ('url(#' in filter_val) and not total_text:
            return []

        # Background image with no text → raster
        if has_url_bg and not total_text:
            return [{
                'type': 'image', 'tag': 'div', 'imageKind': 'background-image',
                'source': bg_image,
                'bounds': {'x': 0.5, 'y': 0.5, 'width': 12.33, 'height': 6.5},
                'styles': {'borderRadius': '', 'objectFit': ''},
            }]

        # Text-only flex/grid wrappers should not be promoted into empty layout
        # containers. Producer HTML often uses inline-flex wrappers for labels like
        # trends, badges, or tiny status rows while keeping the actual text as a
        # bare text node. In those cases, export the element as text directly.
        if total_text and not direct_tag_children:
            text_el = build_text_element(element, style, css_rules, slide_width_px, content_width_px, contract=contract)
            if text_el:
                results = []
                if _should_create_bg_shape(style, has_gradient_bg):
                    shape = build_shape_element(element, style, slide_width_px)
                    shape['bounds'] = dict(text_el['bounds'])
                    if has_gradient_bg:
                        shape['styles']['backgroundImage'] = bg_image
                    import uuid
                    pair_id = str(uuid.uuid4())[:8]
                    shape['_pair_with'] = pair_id
                    text_el['_pair_with'] = pair_id
                    _attach_pair_box_insets(shape, style)
                    results.append(shape)
                results.append(text_el)
                return results

        # Promote visible flex-row cards (e.g. layered cards) to first-class
        # containers before the generic grid/flex wrapper path.
        if _detect_flex_row(style) and has_visible_bg_or_border(style):
            flow_box = measure_flow_box(
                element,
                css_rules,
                parent_style,
                slide_width_px,
                content_width_px,
                local_origin=local_origin,
                contract=contract,
            )
            if flow_box:
                return [flow_box]

        # Grid or flex-row layout: wrap children in a container element
        if _is_grid_container(style) or _detect_flex_row(style):
            grid_local_origin = local_origin or not is_slide_root
            grid_template = style.get('gridTemplateColumns', '') or style.get('grid-template-columns', '')
            intrinsic_auto_fit_grid = _should_use_intrinsic_auto_fit_grid(
                element,
                css_rules,
                style,
                grid_template,
                local_origin=grid_local_origin,
                content_width_px=content_width_px,
                slide_width_px=slide_width_px,
            )
            preserve_metric_grid_width = bool(
                contract_id == 'slide-creator/data-story' and
                component_name == 'metric_grid' and
                style.get('textAlign', '') != 'center'
            )
            grid_children = build_grid_children(
                element,
                css_rules,
                style,
                slide_width_px,
                content_width_px,
                local_origin=grid_local_origin,
                contract=contract,
            )
            if grid_children:
                grid_h = max(c['bounds']['y'] + c['bounds']['height'] for c in grid_children)
            else:
                grid_h = 0.5
            _expand_padding(style)
            pad_b = parse_px(style.get('paddingBottom', '0px')) / PX_PER_IN
            container_w = _resolve_container_width_in(style, content_width_px, slide_width_px)
            if intrinsic_auto_fit_grid and grid_children and not preserve_metric_grid_width:
                min_child_x = min(child['bounds'].get('x', 0.0) for child in grid_children)
                max_child_right = max(
                    child['bounds'].get('x', 0.0) + child['bounds'].get('width', 0.0)
                    for child in grid_children
                )
                intrinsic_w = max(max_child_right - min_child_x, 0.5)
                if intrinsic_w < container_w:
                    for child in grid_children:
                        child['bounds']['x'] = max(child['bounds'].get('x', 0.0) - min_child_x, 0.0)
                    container_w = intrinsic_w
            elif (
                grid_local_origin and grid_children and not content_width_px and
                not preserve_metric_grid_width and
                parse_px(style.get('width', '')) <= 0 and
                parse_px(style.get('maxWidth', style.get('max-width', ''))) <= 0
            ):
                min_child_x = min(child['bounds'].get('x', 0.0) for child in grid_children)
                max_child_right = max(
                    child['bounds'].get('x', 0.0) + child['bounds'].get('width', 0.0)
                    for child in grid_children
                )
                intrinsic_w = max(max_child_right - min_child_x, 0.5)
                if intrinsic_w < container_w - 0.01:
                    for child in grid_children:
                        child['bounds']['x'] = max(child['bounds'].get('x', 0.0) - min_child_x, 0.0)
                    container_w = intrinsic_w
            # Grid/flex wrappers extracted inside a parent block should keep child
            # coordinates relative to the wrapper so later layout can move the
            # whole component as one unit. Limiting this to only constrained
            # wrappers breaks flex-wrap rails (e.g. theme pills) because their
            # children stay at the old absolute y positions.
            children_relative = bool(grid_local_origin)

            container = {
                'type': 'container',
                'tag': element.name,
                'bounds': {'x': 0.5, 'y': 0.5, 'width': container_w, 'height': max(grid_h + pad_b, 0.1)},
                'styles': style,
                'children': grid_children,
                '_children_relative': children_relative,
            }
            if children_relative:
                container = _normalize_relative_container(container)
            return [container]

        # Inline-block container with visible bg/border and SINGLE-LINE text content
        # Treat as a leaf text element (tag pills, badges, etc.)
        # Must come BEFORE is_leaf_text_container check
        # Only applies to single-line text — multi-line inline-blocks should recurse.
        display_val = style.get('display', '')
        is_inline_block_el = 'inline-block' in display_val
        if (is_inline_block_el and has_visible_bg_or_border(style) and total_text
                and '\n' not in total_text):
            # Check that all child Tags are inline (no block children)
            child_tags = [c for c in element.children if isinstance(c, Tag)]
            all_inline = all(c.name.lower() in INLINE_TAGS or c.name.lower() in ('br',) for c in child_tags)
            if all_inline or not child_tags:
                # Don't pass content_width_px for inline-block — size to content
                text_el = build_text_element(element, style, css_rules, slide_width_px, contract=contract)
                if text_el:
                    results = []
                    if has_visible_bg_or_border(style):
                        shape = build_shape_element(element, style, slide_width_px)
                        shape['bounds'] = dict(text_el['bounds'])
                        # text_el width already includes CSS padding from build_text_element
                        # Add extra border/padding for shape if needed (border width)
                        pad_t = parse_px(style.get('paddingTop', '0px')) / PX_PER_IN
                        pad_b = parse_px(style.get('paddingBottom', '0px')) / PX_PER_IN
                        if pad_t + pad_b > 0:
                            shape['bounds']['height'] = text_el['bounds']['height'] + pad_t + pad_b
                        # Pair shape with text for position syncing after layout
                        import uuid
                        pair_id = str(uuid.uuid4())[:8]
                        shape['_pair_with'] = pair_id
                        text_el['_pair_with'] = pair_id
                        _attach_pair_box_insets(shape, style)
                        results.append(shape)
                    results.append(text_el)
                    return results

        # Leaf text container: entire content is text (with inline formatting)
        if is_leaf_text_container(element, css_rules):
            text_el = build_text_element(element, style, css_rules, slide_width_px, content_width_px, contract=contract)
            if text_el:
                results = []
                # Only create background shape if this element actually has a visible
                # background/border (not background-clip:text which paints on text only)
                if _should_create_bg_shape(style, has_gradient_bg):
                    shape = build_shape_element(element, style, slide_width_px)
                    shape['bounds'] = dict(text_el['bounds'])
                    if has_gradient_bg:
                        shape['styles']['backgroundImage'] = bg_image
                    # Pair shape with text for position syncing after layout
                    import uuid
                    pair_id = str(uuid.uuid4())[:8]
                    shape['_pair_with'] = pair_id
                    text_el['_pair_with'] = pair_id
                    _attach_pair_box_insets(shape, style)
                    results.append(shape)
                results.append(text_el)
                return results
            return []

        child_tags = [c for c in element.children if isinstance(c, Tag)]

        # No-text elements with explicit CSS dimensions and visible bg → decoration shapes
        # (e.g., colored dot divs with width/height/border-radius)
        if not total_text and not child_tags and _has_drawable_background(style):
            css_w = parse_px(style.get('width', ''))
            css_h = parse_px(style.get('height', ''))
            if css_w > 0 and css_h > 0:
                dec_w = css_w / PX_PER_IN
                dec_h = css_h / PX_PER_IN
                return [{
                    'type': 'shape', 'tag': element.name,
                    'bounds': {'x': 0.5, 'y': 0.5, 'width': dec_w, 'height': dec_h},
                    'styles': {
                        'backgroundColor': style.get('backgroundColor', ''),
                        'backgroundImage': style.get('backgroundImage', ''),
                        'border': style.get('border', ''),
                        'borderLeft': style.get('borderLeft', ''),
                        'borderRight': style.get('borderRight', ''),
                        'borderTop': style.get('borderTop', ''),
                        'borderBottom': style.get('borderBottom', ''),
                        'borderRadius': style.get('borderRadius', ''),
                        'marginTop': style.get('marginTop', ''),
                        'marginBottom': style.get('marginBottom', ''),
                        'marginLeft': style.get('marginLeft', ''),
                        'marginRight': style.get('marginRight', ''),
                    },
                    '_is_decoration': True,
                }]

        explicit_track = _build_explicit_track_elements(
            element,
            style,
            css_rules,
            slide_width_px,
            content_width_px,
        )
        if explicit_track:
            return explicit_track

        # Standard container: recurse into children
        # First check: if ALL child Tags are inline elements (strong, em, code, etc.)
        # and the container has visible bg/border with text content, treat it as a
        # leaf text element — the inline elements are just styled text within one shape.
        # This handles cases like .info divs with <strong> and <code> children.
        all_inline = bool(child_tags) and all(c.name.lower() in INLINE_TAGS for c in child_tags)
        if all_inline and total_text and has_visible_bg_or_border(style):
            text_el = build_text_element(element, style, css_rules, slide_width_px, content_width_px, contract=contract)
            if text_el:
                # For inline-child containers, use text element's width (respects content_width_px)
                _expand_padding(style)
                pad_l = parse_px(style.get('paddingLeft', '0px')) / PX_PER_IN
                pad_r = parse_px(style.get('paddingRight', '0px')) / PX_PER_IN
                pad_t = parse_px(style.get('paddingTop', '0px')) / PX_PER_IN
                pad_b = parse_px(style.get('paddingBottom', '0px')) / PX_PER_IN
                # Use text element's width (already constrained by content_width_px)
                shape_w = text_el['bounds']['width'] + pad_l + pad_r
                # For elements with borderLeft accent (like .info bars), the golden
                # renders the bg shape 1.15x wider than text content width.
                # max_width = content_width_px / PX_PER_IN represents the content area.
                if content_width_px and content_width_px > 0:
                    max_w_in = content_width_px / PX_PER_IN
                    bl = style.get('borderLeft', '')
                    if bl and 'none' not in bl and '4px' in bl:
                        shape_w = max_w_in * 1.15
                shape_h = text_el['bounds']['height'] + pad_t + pad_b
                shape = {
                    'type': 'shape', 'tag': element.name,
                    'bounds': {'x': 0.5, 'y': 0.5, 'width': shape_w, 'height': shape_h},
                    'styles': {'backgroundColor': style.get('backgroundColor', '')},
                    'naturalHeight': shape_h,
                }
                if style.get('border', ''):
                    shape['styles']['border'] = style['border']
                if style.get('borderLeft', ''):
                    shape['styles']['borderLeft'] = style['borderLeft']
                if style.get('borderRadius', ''):
                    shape['styles']['borderRadius'] = style['borderRadius']
                # Pair shape with text
                import uuid
                pair_id = str(uuid.uuid4())[:8]
                shape['_pair_with'] = pair_id
                text_el['_pair_with'] = pair_id
                _attach_pair_box_insets(shape, style)
                code_child = next((c for c in child_tags if c.name.lower() == 'code'), None)
                allow_detached_code_bg = (
                    code_child is not None and
                    not text_el.get('renderInlineBoxOverlays') and
                    text_el.get('forceSingleLine') and
                    '\n' not in text_el.get('text', '')
                )
                if allow_detached_code_bg:
                    code_s = compute_element_style(code_child, css_rules, code_child.get('style', ''))
                    if has_visible_bg_or_border(code_s):
                        _expand_padding(code_s); code_text = get_text_content(code_child).strip(); font_px = parse_px(code_s.get('fontSize', '16px')) or 16.0
                        cjk = sum(1 for c in code_text if ord(c) > 127); latin = len(code_text) - cjk
                        code_bg = {'type': 'shape', 'tag': 'code', 'bounds': {'x': 0, 'y': 0, 'width': (cjk * font_px + latin * font_px * 0.55 + parse_px(code_s.get('paddingLeft', '0px')) + parse_px(code_s.get('paddingRight', '0px'))) / PX_PER_IN + 0.05, 'height': font_px / PX_PER_IN * 1.6 + 0.05}, 'styles': {'backgroundColor': code_s.get('backgroundColor', ''), 'borderRadius': code_s.get('borderRadius', '0px')}, '_is_code_bg': True, '_skip_layout': True, '_code_element': [code_child]}
                        return [shape, text_el, code_bg]
                return [shape, text_el]

        results = []

        bg_shape = None
        if _should_create_bg_shape(style, has_gradient_bg):
            bg_shape = build_shape_element(element, style, slide_width_px)
            bg_shape['_is_card_bg'] = True
            if has_gradient_bg:
                bg_shape['styles']['backgroundImage'] = bg_image
            results.append(bg_shape)

        # For containers with visible bg/border (like .g cards), compute natural
        # content width from text children and constrain them to it. This prevents
        # text from expanding to the full parent maxWidth.
        natural_content_px = 0.0
        for child in element.children:
            if not isinstance(child, Tag):
                continue
            child_natural_in = compute_text_content_width(child, css_rules, style)
            if child_natural_in > 0:
                natural_content_px = max(natural_content_px, child_natural_in * PX_PER_IN)

        # Propagate maxWidth constraint from parent to children
        parent_maxw = style.get('maxWidth', '')

        # Compute natural content width constraint for children.
        # If natural_content_px < parent's maxWidth, constrain children to the
        # natural width instead of letting them expand to the full maxWidth.
        # This prevents text from expanding to 720px when the actual content
        # is narrower (e.g., the .g card inside a centered div).
        child_cw_override = None
        if bg_shape and natural_content_px > 0 and not is_slide_root:
            _expand_padding(style)
            pad_l = parse_px(style.get('paddingLeft', '0px'))
            pad_r = parse_px(style.get('paddingRight', '0px'))
            max_parent_px = content_width_px or 99999
            if parent_maxw and 'px' in parent_maxw:
                max_parent_px = min(max_parent_px, parse_px(parent_maxw))
            constrained = min(natural_content_px + pad_l + pad_r, max_parent_px)
            if constrained < max_parent_px:
                child_cw_override = constrained

        for child in element.children:
            if isinstance(child, Tag):
                # Determine content width for child
                if child_cw_override is not None:
                    child_cw = child_cw_override
                else:
                    child_cw = content_width_px
                    if not child_cw and parent_maxw and 'px' in parent_maxw:
                        child_cw = parse_px(parent_maxw)
                child_elems = flat_extract(
                    child,
                    css_rules,
                    style,
                    slide_width_px,
                    content_width_px=child_cw,
                    local_origin=True,
                    contract=contract,
                )
                # Apply parent maxWidth to child elements if they don't have one
                if parent_maxw and 'px' in parent_maxw and child_cw_override is None:
                    for ce in child_elems:
                        cs = ce.get('styles', {})
                        if not cs.get('maxWidth', ''):
                            cs['maxWidth'] = parent_maxw
                results.extend(child_elems)

        if not bg_shape and len(results) > 1:
            child_display = style.get('display', '')
            child_flex_dir = style.get('flexDirection', style.get('flex-direction', ''))
            centered_wrapper = (
                style.get('textAlign', '') == 'center' or
                style.get('alignItems', style.get('align-items', '')) == 'center' or
                bool(style.get('maxWidth', style.get('max-width', ''))) or
                (
                    style.get('marginLeft', '') == 'auto' and
                    style.get('marginRight', '') == 'auto'
                )
            )
            preserve_column_wrapper = (
                child_display in ('flex', 'inline-flex') and
                child_flex_dir == 'column' and
                centered_wrapper
            )
            blockish = [
                r for r in results
                if not (r.get('type') == 'shape' and r.get('_is_decoration'))
            ]
            if (
                (local_origin or preserve_column_wrapper) and
                blockish and
                all(r.get('type') in ('container', 'table', 'presentation_rows', 'image') for r in blockish)
            ):
                packed = _pack_relative_block_container(element, style, results)
                if packed:
                    return [packed]
            packable_results = [
                r for r in results
                if not (r.get('type') == 'shape' and r.get('_is_decoration'))
            ]
            if (
                (local_origin or preserve_column_wrapper) and
                centered_wrapper and
                packable_results and
                all(
                    r.get('type') in ('text', 'shape', 'container', 'table', 'presentation_rows', 'image')
                    for r in packable_results
                )
            ):
                packed = _pack_relative_block_container(element, style, results)
                if packed:
                    return [packed]

        # After processing children, size bg shape to match actual content width.
        if bg_shape:
            _expand_padding(style)
            pad_l = parse_px(style.get('paddingLeft', '0px')) / PX_PER_IN
            pad_r = parse_px(style.get('paddingRight', '0px')) / PX_PER_IN
            pad_t = parse_px(style.get('paddingTop', '0px')) / PX_PER_IN
            pad_b = parse_px(style.get('paddingBottom', '0px')) / PX_PER_IN
            border_l = parse_px(
                style.get(
                    'borderLeftWidth',
                    style.get('borderLeft', '0px').split()[0] if style.get('borderLeft', '') else '0px'
                )
            ) / PX_PER_IN
            # Find content extent from non-bg children. Use relative extent instead of
            # raw placeholder coordinates so default x/y placeholders (0.5, 0.5) don't
            # inflate background sizes.
            non_bg_children = [r for r in results if r is not bg_shape]
            max_w = 0.0
            min_top = None
            max_bottom = None
            for r in non_bg_children:
                b = r.get('bounds', {})
                bottom = b.get('y', 0) + b.get('height', 0)
                top = b.get('y', 0)
                if b.get('width', 0) > max_w:
                    max_w = b.get('width', 0)
                min_top = top if min_top is None else min(min_top, top)
                max_bottom = bottom if max_bottom is None else max(max_bottom, bottom)
            if max_w > 0:
                bg_shape['bounds']['width'] = max_w + pad_l + pad_r + border_l
            flow_items = [
                r for r in non_bg_children
                if r.get('type') in ('text', 'table', 'presentation_rows', 'image', 'container')
            ]
            has_complex_flow = (
                len(flow_items) > 2 or
                any(r.get('tag') == 'li' or r.get('type') in ('table', 'presentation_rows', 'container') for r in flow_items)
            )
            if has_complex_flow:
                content_h = 0.0
                for idx, r in enumerate(flow_items):
                    rb = r.get('bounds', {})
                    content_h += rb.get('height', 0.0)
                    if idx == len(flow_items) - 1:
                        continue
                    if r.get('tag') == 'li':
                        content_h += 7.0 / PX_PER_IN
                        continue
                    mb = parse_px(r.get('styles', {}).get('marginBottom', '')) / PX_PER_IN
                    content_h += mb if mb > 0 else 0.05
            elif max_bottom is not None and min_top is not None and max_bottom > min_top:
                content_h = max_bottom - min_top
            else:
                content_h = 0.0
            if content_h > 0:
                bg_shape['bounds']['height'] = content_h + pad_t + pad_b

            # Mark centered shrink-wrap cards so the layout pass can preserve the
            # card width and align descendant text to the card content area instead
            # of expanding everything to the full slide content width.
            if child_cw_override is not None and not is_slide_root:
                import uuid
                card_group = f"card-{str(uuid.uuid4())[:8]}"
                bg_shape['_card_group'] = card_group
                bg_shape['_preserve_width'] = True
                bg_shape['_css_pad_l'] = pad_l
                bg_shape['_css_pad_r'] = pad_r
                bg_shape['_css_pad_t'] = pad_t
                bg_shape['_css_pad_b'] = pad_b
                bg_shape['_css_border_l'] = border_l
                for r in results:
                    if r is bg_shape:
                        continue
                    r['_card_group'] = card_group

                # For simple centered cards, keep the card and its descendants as a
                # relative-positioned container. This prevents the top-level layout
                # pass from stacking the card background and its text sequentially.
                if (content_width_px and len(results) > 2 and
                        not style.get('borderLeft', '') and
                        not _is_grid_container(style) and
                        not _detect_flex_row(style)):
                    min_child_x = min((r['bounds']['x'] for r in non_bg_children), default=0.0)
                    min_child_y = min((r['bounds']['y'] for r in non_bg_children), default=0.0)
                    origin_x = max(min_child_x - pad_l - border_l, 0.0)
                    origin_y = max(min_child_y - pad_t, 0.0)
                    x_offset = max((content_width_px / PX_PER_IN - bg_shape['bounds']['width']) / 2.0, 0.0)

                    bg_shape['bounds']['x'] = x_offset
                    bg_shape['bounds']['y'] = 0.0
                    for r in non_bg_children:
                        r['bounds']['x'] = x_offset + max(r['bounds']['x'] - origin_x, 0.0)
                        r['bounds']['y'] = max(r['bounds']['y'] - origin_y, 0.0)

                    return [{
                        'type': 'container',
                        'tag': element.name,
                        'bounds': {
                            'x': 0.5,
                            'y': 0.5,
                            'width': 12.33,
                            'height': bg_shape['bounds']['height'],
                        },
                        'styles': style,
                        'children': results,
                        '_children_relative': True,
                    }]

                # Generic local card packing: preserve visible block cards as
                # relative containers instead of flattening them into sibling
                # shape/text elements. This keeps block-card grids and column
                # stacks closer to authored HTML structure.
                packable_non_bg = [
                    r for r in non_bg_children
                    if r.get('type') in ('text', 'table', 'presentation_rows', 'image', 'container')
                ]
                if (
                    local_origin and
                    packable_non_bg and
                    not _is_grid_container(style) and
                    not _detect_flex_row(style)
                ):
                    min_child_x = min((r['bounds']['x'] for r in packable_non_bg), default=0.0)
                    min_child_y = min((r['bounds']['y'] for r in packable_non_bg), default=0.0)
                    origin_x = max(min_child_x - pad_l - border_l, 0.0)
                    origin_y = max(min_child_y - pad_t, 0.0)

                    bg_shape['bounds']['x'] = 0.0
                    bg_shape['bounds']['y'] = 0.0
                    bg_shape['_is_card_bg'] = True
                    bg_shape['_skip_layout'] = True
                    bg_shape['_css_pad_l'] = pad_l
                    bg_shape['_css_pad_r'] = pad_r
                    bg_shape['_css_pad_t'] = pad_t
                    bg_shape['_css_pad_b'] = pad_b
                    bg_shape['_css_border_l'] = border_l

                    for r in non_bg_children:
                        r['bounds']['x'] = max(r['bounds']['x'] - origin_x, 0.0)
                        r['bounds']['y'] = max(r['bounds']['y'] - origin_y, 0.0)

                    flow_children = [bg_shape]
                    flow_children.extend(non_bg_children)
                    _normalize_card_group_text_metrics(flow_children, bg_shape['bounds']['width'])
                    intrinsic_h = max(
                        (c['bounds']['y'] + c['bounds']['height'] for c in flow_children),
                        default=bg_shape['bounds']['height'],
                    )
                    bg_shape['bounds']['height'] = max(bg_shape['bounds']['height'], intrinsic_h)

                    return [{
                        'type': 'container',
                        'tag': element.name,
                        'bounds': {
                            'x': 0.5,
                            'y': 0.5,
                            'width': bg_shape['bounds']['width'],
                            'height': bg_shape['bounds']['height'],
                        },
                        'styles': style,
                        'children': flow_children,
                        '_children_relative': True,
                    }]

        return results

    return []


def build_grid_children(
    container: Tag,
    css_rules: List[CSSRule],
    style: Dict[str, str],
    slide_width_px: float = 1440,
    content_width_px: float = None,  # If set, constrain grid to this width
    local_origin: bool = False,
    contract: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """Process children of a grid/flex-row container with proper layout."""
    width_in = 13.33
    px_per_in = slide_width_px / width_in
    margin_in = 0.5

    # If content width is constrained, adjust width and margin accordingly
    if content_width_px and content_width_px > 0:
        content_width_in = content_width_px / px_per_in
        if local_origin:
            width_in = content_width_in
            margin_in = 0.0
        elif content_width_in < width_in:
            # Center content within slide
            side_margin = (width_in - content_width_in) / 2
            margin_in = side_margin

    grid_cols = style.get('gridTemplateColumns', '')
    if not grid_cols:
        grid_cols = style.get('grid-template-columns', '')

    intrinsic_auto_fit_grid = _should_use_intrinsic_auto_fit_grid(
        container,
        css_rules,
        style,
        grid_cols,
        local_origin=local_origin,
        content_width_px=content_width_px,
        slide_width_px=slide_width_px,
    )
    auto_fit_match = re.match(r'^repeat\(\s*auto-(fit|fill)\s*,\s*(.+)\)\s*$', grid_cols.strip()) if grid_cols else None
    stack_centered_auto_fit_cards = (
        intrinsic_auto_fit_grid and
        _should_stack_centered_auto_fit_cards(container, css_rules, style)
    )

    flex_wrap = style.get('flexWrap', style.get('flex-wrap', 'nowrap'))
    is_plain_flex_row = _detect_flex_row(style) and not grid_cols and flex_wrap in ('', 'nowrap', 'initial', 'unset')
    is_flex_wrap_row = _detect_flex_row(style) and not grid_cols and not is_plain_flex_row

    gap_px = _get_gap_px(style)
    gap_in = gap_px / px_per_in
    available_width_in = width_in - 2 * margin_in
    tag_children = [c for c in container.children if isinstance(c, Tag)]

    _expand_padding(style)
    layout_pad_l = parse_px(style.get('paddingLeft', '0px')) / PX_PER_IN
    layout_pad_r = parse_px(style.get('paddingRight', '0px')) / PX_PER_IN
    layout_pad_t = parse_px(style.get('paddingTop', '0px')) / PX_PER_IN
    layout_border_l = parse_px(
        style.get(
            'borderLeftWidth',
            style.get('borderLeft', '0px').split()[0] if style.get('borderLeft', '') else '0px'
        )
    ) / PX_PER_IN
    layout_start_in = layout_pad_l + layout_border_l
    layout_inner_width_in = max(available_width_in - layout_start_in - layout_pad_r, 0.5)
    intrinsic_min_track_in = 0.0
    if auto_fit_match:
        intrinsic_min_track_in = _extract_min_track_px(
            auto_fit_match.group(2).strip(),
            layout_inner_width_in * PX_PER_IN,
        ) / PX_PER_IN

    grid_track_widths_in = []
    if grid_cols and not intrinsic_auto_fit_grid:
        if auto_fit_match and auto_fit_match.group(1) == 'fit':
            fit_cols = _resolve_intrinsic_auto_fit_cols(
                layout_inner_width_in,
                gap_in,
                intrinsic_min_track_in,
            )
            effective_cols = max(min(fit_cols, len(tag_children) or fit_cols), 1)
            track_w = max(
                (layout_inner_width_in - gap_in * max(effective_cols - 1, 0)) / max(effective_cols, 1),
                intrinsic_min_track_in or 0.1,
            )
            grid_track_widths_in = [track_w] * effective_cols
        else:
            grid_track_widths_in = _parse_grid_track_widths(grid_cols, layout_inner_width_in, gap_in)

    if intrinsic_auto_fit_grid:
        num_cols = _resolve_effective_auto_fit_cols(
            layout_inner_width_in,
            gap_in,
            intrinsic_min_track_in,
            len(tag_children),
            collapse_empty_tracks=bool(auto_fit_match and auto_fit_match.group(1) == 'fit'),
        )
        if stack_centered_auto_fit_cards:
            num_cols = 1
    elif grid_track_widths_in:
        num_cols = len(grid_track_widths_in)
    elif grid_cols:
        num_cols = _parse_grid_columns(grid_cols, layout_inner_width_in, gap_in)
    elif is_flex_wrap_row:
        num_cols = 1
    elif _detect_flex_row(style):
        children = [c for c in container.children if isinstance(c, Tag)]
        num_cols = len(children) if children else 1
    else:
        num_cols = 1

    is_flex_like_row = is_plain_flex_row or is_flex_wrap_row
    flex_start_in = layout_start_in if is_flex_like_row else 0.0
    flex_inner_width_in = layout_inner_width_in if is_flex_like_row else layout_inner_width_in

    # Check if grid should be centered (justify-content: center)
    justify = style.get('justifyContent', style.get('justify-content', ''))
    is_centered = justify == 'center'

    # Estimate item width based on content (for centered grids) or fill available width
    if is_plain_flex_row:
        item_width_in = flex_inner_width_in
    elif intrinsic_auto_fit_grid:
        track_span_in = (
            (layout_inner_width_in - gap_in * max(num_cols - 1, 0)) / max(num_cols, 1)
            if num_cols > 1 else layout_inner_width_in
        )
        content_widths = []
        for child in container.children:
            if not isinstance(child, Tag):
                continue
            child_style = compute_element_style(child, css_rules, child.get('style', ''), style)
            preferred_w = 0.0
            if has_visible_bg_or_border(child_style):
                preferred_w = compute_text_content_width(child, css_rules, style)
                if preferred_w > 0:
                    _expand_padding(child_style)
                    preferred_w += (
                        parse_px(child_style.get('paddingLeft', '0px')) +
                        parse_px(child_style.get('paddingRight', '0px'))
                    ) / PX_PER_IN
            if preferred_w <= 0.0:
                preferred_w = _measure_preferred_child_width_in(
                    child,
                    child_style,
                    css_rules,
                    slide_width_px,
                )
            if preferred_w <= 0.0 and is_leaf_text_container(child, css_rules):
                preferred_w = compute_text_content_width(child, css_rules, style)
            if preferred_w > 0.0:
                preferred_w = max(preferred_w, intrinsic_min_track_in)
                content_widths.append(min(preferred_w, max(track_span_in, intrinsic_min_track_in)))
        if num_cols > 1:
            item_width_in = max(track_span_in, intrinsic_min_track_in)
        elif content_widths:
            item_width_in = max(content_widths)
        elif intrinsic_min_track_in > 0.0:
            item_width_in = min(intrinsic_min_track_in, layout_inner_width_in)
        else:
            item_width_in = min(layout_inner_width_in, 3.0)
    elif is_centered:
        # Calculate content-based width for each child, using the max font size within
        content_widths = []
        for child in container.children:
            if not isinstance(child, Tag):
                continue
            child_style = compute_element_style(child, css_rules, child.get('style', ''), style)
            # Find max font size within this child's subtree for accurate width estimation
            max_font_px = 0.0
            for desc in child.descendants:
                if hasattr(desc, 'name') and desc.name:
                    ds = compute_element_style(desc, css_rules, desc.get('style', ''), child_style)
                    fp = parse_px(ds.get('fontSize', '16px'))
                    if fp > max_font_px:
                        max_font_px = fp
            if max_font_px <= 0:
                max_font_px = 16.0

            child_text = get_text_content(child).strip()
            if child_text:
                cjk = sum(1 for c in child_text if ord(c) > 127)
                latin = len(child_text) - cjk
                text_w = (cjk * max_font_px + latin * max_font_px * 0.55) / PX_PER_IN
                # Add modest padding
                content_widths.append(text_w + 0.3)
            else:
                content_widths.append(2.0)  # default width

        if content_widths:
            # Use the max content width for uniform items
            item_width_in = max(max(content_widths), 1.5)
        else:
            item_width_in = 2.0
    else:
        item_width_in = (layout_inner_width_in - gap_in * (num_cols - 1)) / num_cols if num_cols > 1 else layout_inner_width_in

    x_offset = 0.0
    if is_centered and num_cols > 1 and not grid_track_widths_in:
        total_grid_width = num_cols * item_width_in + (num_cols - 1) * gap_in
        x_offset = (layout_inner_width_in - total_grid_width) / 2

    flex_child_widths: List[float] = []
    if is_flex_like_row:
        flex_children = tag_children
        fixed_total = 0.0
        flex_slots = []
        contract_id = (contract or {}).get('contract_id', '')
        for idx, child in enumerate(flex_children):
            child_style = compute_element_style(child, css_rules, child.get('style', ''), style)
            child_tag = child.name.lower()
            child_component_name = _contract_component_name(child, contract)
            child_slot_model = (
                _contract_slot_model(contract, child_component_name)
                if contract_id in {'slide-creator/data-story', 'slide-creator/aurora-mesh'}
                else {}
            )
            child_w = 0.0
            css_w = parse_px(child_style.get('width', ''))

            if (
                contract_id == 'slide-creator/aurora-mesh' and
                child_slot_model.get('layout') == 'vertical_card'
            ):
                stretch_track = _contract_vertical_card_prefers_stretch_width(child_style)
                if not stretch_track:
                    compact_cap_in = max(
                        (flex_inner_width_in - gap_in * max(len(flex_children) - 1, 0)) / max(len(flex_children), 1),
                        0.8,
                    )
                    child_w = _measure_contract_vertical_card_intrinsic_width_in(
                        child,
                        child_style,
                        css_rules,
                        slide_width_px,
                        compact_cap_in,
                        child_slot_model,
                    )
                    if child_w > 0:
                        fixed_total += child_w
                        flex_child_widths.append(child_w)
                        continue
                flex_slots.append(idx)
                flex_child_widths.append(0.0)
                continue

            if css_w > 0:
                child_w = css_w / PX_PER_IN
            elif has_visible_bg_or_border(child_style):
                child_w = _measure_preferred_child_width_in(
                    child,
                    child_style,
                    css_rules,
                    slide_width_px,
                )
                if child_w <= 0:
                    natural_w = compute_text_content_width(child, css_rules, style)
                    if natural_w > 0:
                        _expand_padding(child_style)
                        child_w = natural_w + (
                            parse_px(child_style.get('paddingLeft', '0px')) +
                            parse_px(child_style.get('paddingRight', '0px'))
                        ) / PX_PER_IN
                if child_w <= 0:
                    measured_card = measure_flow_box(
                        child,
                        css_rules,
                        style,
                        slide_width_px,
                        local_origin=True,
                        contract=contract,
                    )
                    if measured_card:
                        child_w = measured_card.get('measure', {}).get(
                            'intrinsic_width',
                            measured_card.get('bounds', {}).get('width', 0.0),
                        )
            elif child_tag in TEXT_TAGS:
                child_text = get_text_content(child).strip()
                if child_text:
                    font_px = parse_px(child_style.get('fontSize', '16px'))
                    if font_px <= 0:
                        font_px = 16.0
                    cjk = sum(1 for c in child_text if ord(c) > 127)
                    latin = len(child_text) - cjk
                    child_w = (cjk * font_px * 0.96 + latin * font_px * 0.55) / PX_PER_IN
                    if has_visible_bg_or_border(child_style):
                        _expand_padding(child_style)
                        child_w += (
                            parse_px(child_style.get('paddingLeft', '0px')) +
                            parse_px(child_style.get('paddingRight', '0px'))
                        ) / PX_PER_IN
            elif is_leaf_text_container(child, css_rules):
                child_w = compute_text_content_width(child, css_rules, style)
                if child_w > 0 and has_visible_bg_or_border(child_style):
                    _expand_padding(child_style)
                    child_w += (
                        parse_px(child_style.get('paddingLeft', '0px')) +
                        parse_px(child_style.get('paddingRight', '0px'))
                    ) / PX_PER_IN
            elif child_tag in CONTAINER_TAGS:
                # Shrink-wrap simple inline/flex headers, but let block-content
                # columns consume the remaining row width.
                direct_tag_children = [gc for gc in child.children if isinstance(gc, Tag)]
                all_inline_like = bool(direct_tag_children) and all(
                    gc.name.lower() in INLINE_TAGS or gc.name.lower() in ('br',) or gc.name.lower() in TEXT_TAGS
                    for gc in direct_tag_children
                )
                if all_inline_like and not any(gc.name.lower() in ('p', 'li', 'table', 'ul', 'ol') for gc in direct_tag_children):
                    natural_w = compute_text_content_width(child, css_rules, style)
                    if natural_w > 0:
                        child_w = natural_w
                        _expand_padding(child_style)
                        child_w += (
                            parse_px(child_style.get('paddingLeft', '0px')) +
                            parse_px(child_style.get('paddingRight', '0px'))
                        ) / PX_PER_IN

            if child_w > 0:
                if child_tag in TEXT_TAGS:
                    child_w += 0.12
                fixed_total += child_w
                flex_child_widths.append(child_w)
            else:
                flex_slots.append(idx)
                flex_child_widths.append(0.0)

        remaining_w = max(flex_inner_width_in - fixed_total - gap_in * max(len(flex_children) - 1, 0), 0.5)
        # Compact flex-row (explicit gap, no distributing justify-content):
        # measure each unfilled slot's intrinsic content width instead of
        # spreading children evenly across the row. Falls back to even split
        # if a slot has flex-grow/explicit width or its intrinsic doesn't fit.
        compact_packing = _flex_row_prefers_compact_packing(style)
        if compact_packing and flex_slots:
            measured: Dict[int, float] = {}
            cap_per_slot = max(remaining_w / max(len(flex_slots), 1), 0.5)
            all_compact = True
            for slot_idx in flex_slots:
                slot_child = flex_children[slot_idx]
                slot_style = compute_element_style(
                    slot_child, css_rules, slot_child.get('style', ''), style
                )
                if (
                    _style_flex_grow_value(slot_style) > 0.0
                    or _style_has_explicit_width_signal(slot_style)
                ):
                    all_compact = False
                    break
                intrinsic = _measure_compact_flex_child_width_in(
                    slot_child, slot_style, css_rules, slide_width_px, cap_per_slot
                )
                if intrinsic <= 0:
                    all_compact = False
                    break
                measured[slot_idx] = intrinsic
            if all_compact and measured:
                projected_total = (
                    fixed_total
                    + sum(measured.values())
                    + gap_in * max(len(flex_children) - 1, 0)
                )
                if projected_total <= flex_inner_width_in + 0.001:
                    for slot_idx, w in measured.items():
                        flex_child_widths[slot_idx] = w
                    flex_slots = []
        if flex_slots:
            slot_w = remaining_w / len(flex_slots)
            for idx in flex_slots:
                flex_child_widths[idx] = slot_w

    # Collect child element groups (each group = one grid cell's elements)
    child_groups = []
    item_widths = []  # Per-item content widths
    group_track_widths = []
    tag_child_idx = 0
    grid_child_idx = 0
    for child in container.children:
        if not isinstance(child, Tag):
            continue
        child_style = compute_element_style(child, css_rules, child.get('style', ''), style)
        child_tag = child.name.lower()
        child_component_name = _contract_component_name(child, contract)
        child_slot_model = (
            _contract_slot_model(contract, child_component_name)
            if (contract or {}).get('contract_id') in {'slide-creator/data-story', 'slide-creator/aurora-mesh'}
            else {}
        )
        base_col_idx = grid_child_idx % max(num_cols, 1)
        child_width_in = grid_track_widths_in[base_col_idx] if grid_track_widths_in else item_width_in
        if is_flex_like_row and tag_child_idx < len(flex_child_widths):
            child_width_in = flex_child_widths[tag_child_idx]
        tag_child_idx += 1
        grid_child_idx += 1

        if child_tag == 'img':
            img_el = build_image_element(child, child_style)
            if img_el:
                child_groups.append([img_el])
                item_widths.append(child_width_in if is_plain_flex_row else img_el['bounds']['width'])
                group_track_widths.append(child_width_in)
            continue
        if child_tag == 'svg':
            svg_container = build_svg_container(
                child,
                css_rules,
                style,
                slide_width_px,
                content_width_px=child_width_in * PX_PER_IN if child_width_in > 0 else content_width_px,
            )
            if svg_container:
                child_groups.append([svg_container])
                item_widths.append(child_width_in if is_plain_flex_row else svg_container['bounds']['width'])
                group_track_widths.append(child_width_in)
            else:
                child_groups.append([{
                    'type': 'image', 'tag': 'svg', 'imageKind': 'svg',
                    'source': str(child),
                    'bounds': {'x': 0, 'y': 0, 'width': child_width_in, 'height': 2},
                    'styles': {'borderRadius': '', 'objectFit': ''},
                }])
                item_widths.append(child_width_in)
                group_track_widths.append(child_width_in)
            continue
        if child_tag == 'table':
            child_cw_px = child_width_in * PX_PER_IN if child_width_in > 0 else content_width_px
            tbl = build_table_element(child, css_rules, child_style, content_width_px=child_cw_px)
            child_groups.append([tbl])
            item_widths.append(child_width_in if is_plain_flex_row else tbl['bounds']['width'])
            group_track_widths.append(child_width_in)
            continue
        if child_tag in TEXT_TAGS:
            child_cw_px = child_width_in * PX_PER_IN if is_plain_flex_row else content_width_px
            text_el = build_text_element(child, child_style, css_rules, slide_width_px, child_cw_px)
            if text_el:
                group = []
                if has_visible_bg_or_border(child_style):
                    shape = build_shape_element(child, child_style, slide_width_px)
                    shape['bounds'] = dict(text_el['bounds'])
                    import uuid
                    pair_id = str(uuid.uuid4())[:8]
                    shape['_pair_with'] = pair_id
                    text_el['_pair_with'] = pair_id
                    _attach_pair_box_insets(shape, child_style)
                    group.append(shape)
                group.append(text_el)
                child_groups.append(group)
                item_widths.append(
                    text_el['bounds']['width']
                    if (not is_plain_flex_row or text_el.get('preferContentWidth'))
                    else child_width_in
                )
                group_track_widths.append(child_width_in)
            continue
        if child_tag in CONTAINER_TAGS:
            bg_img = child_style.get('backgroundImage', 'none')
            has_grad = bg_img != 'none' and 'gradient' in bg_img
            has_url = bg_img != 'none' and 'url(' in bg_img
            total_txt = get_text_content(child).strip()

            if has_url and not total_txt:
                child_groups.append([{
                    'type': 'image', 'tag': 'div', 'imageKind': 'background-image',
                    'source': bg_img,
                    'bounds': {'x': 0, 'y': 0, 'width': child_width_in, 'height': 3},
                    'styles': {'borderRadius': '', 'objectFit': ''},
                }])
                item_widths.append(child_width_in)
                group_track_widths.append(child_width_in)
                continue

            if is_leaf_text_container(child, css_rules):
                child_cw_px = child_width_in * PX_PER_IN if is_plain_flex_row else content_width_px
                text_el = build_text_element(child, child_style, css_rules, slide_width_px, child_cw_px)
                if text_el:
                    group = []
                    has_css_dims = False
                    if has_visible_bg_or_border(child_style) or has_grad:
                        shape = build_shape_element(child, child_style, slide_width_px)
                        # For elements with explicit CSS dimensions (like step circles),
                        # use CSS size for the shape, not text-based estimation.
                        css_w = parse_px(child_style.get('width', ''))
                        css_h = parse_px(child_style.get('height', ''))
                        if css_w > 0 and css_h > 0:
                            shape_w = css_w / PX_PER_IN
                            shape_h = css_h / PX_PER_IN
                            shape['bounds'] = {
                                'x': text_el['bounds']['x'],
                                'y': text_el['bounds']['y'],
                                'width': shape_w,
                                'height': shape_h,
                            }
                            # Also expand text element to match shape size so comparison matches
                            text_el['bounds']['width'] = shape_w
                            text_el['bounds']['height'] = shape_h
                            text_el['_use_css_dims'] = True  # Prevent layout pass from overriding
                            has_css_dims = True
                        else:
                            shape['bounds'] = dict(text_el['bounds'])
                        import uuid
                        pair_id = str(uuid.uuid4())[:8]
                        shape['_pair_with'] = pair_id
                        text_el['_pair_with'] = pair_id
                        _attach_pair_box_insets(shape, child_style)
                        if has_grad:
                            shape['styles']['backgroundImage'] = bg_img
                        group.append(shape)
                    group.append(text_el)
                    child_groups.append(group)
                    item_widths.append(
                        text_el['bounds']['width']
                        if (not is_plain_flex_row or text_el.get('preferContentWidth'))
                        else child_width_in
                    )
                    group_track_widths.append(child_width_in)
                continue

            # For grid cell containers, compute internal width (cell width - padding)
            # so nested elements (like <li> in <ul>) use the available width
            pad_l = parse_px(child_style.get('paddingLeft', '0px'))
            pad_r = parse_px(child_style.get('paddingRight', '0px'))
            cell_internal_width_px = max(child_width_in - (pad_l + pad_r) / PX_PER_IN, 0.5) * PX_PER_IN

            # Special handling: flex-column containers should process each direct child
            # as a separate grid item (preserves card/layer grouping)
            child_display = child_style.get('display', '')
            child_flex_dir = child_style.get('flexDirection', child_style.get('flex-direction', ''))
            is_flex_column = (child_display == 'flex' and child_flex_dir == 'column')
            contract_layout = child_slot_model.get('layout')

            if contract_layout in {'vertical_card', 'split_rail', 'grid_two_column'}:
                sub_elements = flat_extract(
                    child,
                    css_rules,
                    child_style,
                    slide_width_px,
                    content_width_px=cell_internal_width_px,
                    local_origin=True,
                    contract=contract,
                )
                if sub_elements:
                    is_nested_container_group = (
                        len(sub_elements) == 1 and
                        sub_elements[0].get('type') == 'container' and
                        bool(sub_elements[0].get('children'))
                    )
                    if is_nested_container_group:
                        sub_elements[0]['_children_relative'] = True
                        _normalize_relative_container(sub_elements[0])
                    child_groups.append(sub_elements)
                    intrinsic_group_w = _measure_group_intrinsic_width_in(sub_elements)
                    has_card_bg = (
                        is_nested_container_group and
                        any(
                            grandchild.get('type') == 'shape' and grandchild.get('_is_card_bg')
                            for grandchild in sub_elements[0].get('children', [])
                        )
                    )
                    item_widths.append(
                        child_width_in if (is_plain_flex_row or has_card_bg) else max(intrinsic_group_w, 0.1)
                    )
                    group_track_widths.append(child_width_in)
                continue

            if (
                contract_layout not in {'vertical_card', 'split_rail', 'grid_two_column'}
                and _detect_flex_container(child_style)
                and has_visible_bg_or_border(child_style)
            ):
                flow_box = measure_flow_box(
                    child,
                    css_rules,
                    style,
                    slide_width_px,
                    content_width_px=(child_width_in * PX_PER_IN if child_width_in > 0 else cell_internal_width_px),
                    local_origin=True,
                    contract=contract,
                )
                if flow_box:
                    child_groups.append([flow_box])
                    item_widths.append(child_width_in if is_flex_like_row else flow_box['bounds']['width'])
                    group_track_widths.append(child_width_in)
                    continue

            if is_flex_column:
                col_gap_px = parse_px(child_style.get('gap', '0px'))
                col_gap_in = col_gap_px / PX_PER_IN
                col_children = [c for c in child.children if isinstance(c, Tag)]
                # Compute which grid column this flex-column container belongs to.
                # Must count only Tag children (main loop skips non-Tag items), then
                # mod by num_cols for multi-row grids.
                tag_children = [gc for gc in container.children if isinstance(gc, Tag)]
                grid_col_for_fc = 0
                for gi, gc in enumerate(tag_children):
                    if gc is child:
                        grid_col_for_fc = gi % num_cols
                        break

                # Process each col_child, tracking its position WITHIN this column
                # (used as row_idx in layout so items from different columns in the
                # same row share the same Y position)
                row_within_col = 0
                for col_child in col_children:
                    cc_style = compute_element_style(col_child, css_rules, col_child.get('style', ''), child_style)
                    # Detect flex-row children (like .layer): emoji + text side by side
                    cc_display = cc_style.get('display', '')
                    cc_flex_dir = cc_style.get('flexDirection', cc_style.get('flex-direction', ''))
                    is_cc_flex_row = (cc_display in ('flex', 'inline-flex') and cc_flex_dir != 'column')

                    if is_cc_flex_row:
                        flow_box = measure_flow_box(
                            col_child,
                            css_rules,
                            child_style,
                            slide_width_px,
                            content_width_px=cell_internal_width_px,
                            local_origin=True,
                            contract=contract,
                        )
                        if flow_box:
                            flow_box['_flex_column_item'] = True
                            flow_box['_grid_col_idx'] = grid_col_for_fc
                            flow_box['_row_in_col'] = row_within_col
                            child_groups.append([flow_box])
                            item_widths.append(child_width_in)
                            group_track_widths.append(child_width_in)
                        else:
                            sub_elements = flat_extract(
                                col_child,
                                css_rules,
                                cc_style,
                                slide_width_px,
                                content_width_px=cell_internal_width_px,
                                local_origin=True,
                                contract=contract,
                            )
                            if sub_elements:
                                sub_elements[0]['_flex_column_item'] = True
                                sub_elements[0]['_grid_col_idx'] = grid_col_for_fc
                                sub_elements[0]['_row_in_col'] = row_within_col
                                child_groups.append(sub_elements)
                                item_widths.append(child_width_in)
                                group_track_widths.append(child_width_in)
                    else:
                        # Not flex-row: process normally
                        sub_elements = flat_extract(
                            col_child,
                            css_rules,
                            cc_style,
                            slide_width_px,
                            content_width_px=cell_internal_width_px,
                            local_origin=True,
                            contract=contract,
                        )
                        if sub_elements:
                            # Mark as flex-column item with specific grid column
                            # and row position within the column
                            sub_elements[0]['_flex_column_item'] = True
                            sub_elements[0]['_grid_col_idx'] = grid_col_for_fc
                            sub_elements[0]['_row_in_col'] = row_within_col
                            child_groups.append(sub_elements)
                            text_w = compute_text_content_width(col_child, css_rules)
                            if text_w > 0:
                                card_pad_in = 2 * 24.0 / PX_PER_IN
                                item_widths.append(child_width_in if is_plain_flex_row else text_w + card_pad_in)
                            elif sub_elements:
                                text_h = sum(e['bounds'].get('height', 0.3) for e in sub_elements if e.get('type') == 'text')
                                item_widths.append(child_width_in if is_plain_flex_row else min(text_h * 3.0, 3.0))
                            else:
                                item_widths.append(child_width_in)
                            group_track_widths.append(child_width_in)
                    row_within_col += 1
                continue

            sub_elements = flat_extract(
                child,
                css_rules,
                child_style,
                slide_width_px,
                content_width_px=cell_internal_width_px,
                local_origin=True,
                contract=contract,
            )
            is_flow_box_group = (
                len(sub_elements) == 1 and
                sub_elements[0].get('type') == 'container' and
                sub_elements[0].get('layout') == 'flow_box'
            )
            is_nested_container_group = (
                len(sub_elements) == 1 and
                sub_elements[0].get('type') == 'container' and
                sub_elements[0].get('layout') != 'flow_box' and
                bool(sub_elements[0].get('children'))
            )
            explicit_child_w = parse_px(child_style.get('width', ''))
            explicit_child_h = parse_px(child_style.get('height', ''))
            is_explicit_decoration = (
                not total_txt and explicit_child_w > 0 and explicit_child_h > 0 and
                len(sub_elements) == 1 and sub_elements[0].get('type') == 'shape'
            )
            is_thin_shape_group = (
                not total_txt and bool(sub_elements) and
                all(e.get('type') == 'shape' for e in sub_elements) and
                max((e.get('bounds', {}).get('height', 0.0) for e in sub_elements), default=0.0) <= 0.08
            )
            if is_explicit_decoration:
                child_groups.append(sub_elements)
                item_widths.append(child_width_in if is_plain_flex_row else sub_elements[0]['bounds']['width'])
                group_track_widths.append(child_width_in)
                continue
            if is_thin_shape_group:
                child_groups.append(sub_elements)
                item_widths.append(
                    child_width_in if is_plain_flex_row else
                    max((e.get('bounds', {}).get('width', 0.0) for e in sub_elements), default=child_width_in)
                )
                group_track_widths.append(child_width_in)
                continue
            if is_flow_box_group:
                child_groups.append(sub_elements)
                item_widths.append(child_width_in)
                group_track_widths.append(child_width_in)
                continue
            if is_nested_container_group:
                sub_elements[0]['_children_relative'] = True
                _normalize_relative_container(sub_elements[0])
                child_groups.append(sub_elements)
                intrinsic_group_w = _measure_group_intrinsic_width_in(sub_elements)
                has_card_bg = any(
                    grandchild.get('type') == 'shape' and grandchild.get('_is_card_bg')
                    for grandchild in sub_elements[0].get('children', [])
                )
                item_widths.append(
                    child_width_in if (is_plain_flex_row or has_card_bg) else max(intrinsic_group_w, 0.1)
                )
                group_track_widths.append(child_width_in)
                continue
            # If container has visible background/border, prepend a shape for it
            # and strip child elements' shape wrappers (they inherit the container bg)
            if has_visible_bg_or_border(child_style) or has_grad:
                shape = build_shape_element(child, child_style, slide_width_px)
                shape['bounds'] = {'x': 0, 'y': 0, 'width': child_width_in, 'height': 3.0}
                shape['_is_card_bg'] = True
                if has_grad:
                    shape['styles']['backgroundImage'] = bg_img
                # Store CSS padding on the bg shape for use in layout
                _expand_padding(child_style)
                shape['_css_pad_l'] = parse_px(child_style.get('paddingLeft', '0px')) / PX_PER_IN
                shape['_css_pad_r'] = parse_px(child_style.get('paddingRight', '0px')) / PX_PER_IN
                shape['_css_pad_t'] = parse_px(child_style.get('paddingTop', '0px')) / PX_PER_IN
                shape['_css_pad_b'] = parse_px(child_style.get('paddingBottom', '0px')) / PX_PER_IN
                shape['_css_border_l'] = parse_px(child_style.get('borderLeftWidth', child_style.get('borderLeft', '0px').split()[0] if child_style.get('borderLeft', '') else '0px')) / PX_PER_IN
                shape['_css_text_align'] = child_style.get('textAlign', 'left')
                # Filter out shape elements from children that only exist because of inherited bg
                # Keep paired shapes (pill/badge backgrounds) and shapes with text
                content_only = [e for e in sub_elements
                                if e.get('type') != 'shape' or e.get('text') or e.get('_pair_with')]
                sub_elements = [shape] + content_only
            child_groups.append(sub_elements)
            intrinsic_group_w = _measure_group_intrinsic_width_in(sub_elements)
            # Compute item width from the actual grouped item extent whenever
            # possible. This prevents centered flex-wrap rows from reserving
            # card-like padding for plain grouped content such as KPI stacks.
            text_w = compute_text_content_width(child, css_rules)
            if intrinsic_group_w > 0 and not (has_visible_bg_or_border(child_style) or has_grad):
                item_widths.append(child_width_in if is_plain_flex_row else intrinsic_group_w)
            elif text_w > 0:
                if has_visible_bg_or_border(child_style) or has_grad:
                    # Card items with background need padding added to content width.
                    # Golden stat cards: text_width + ~0.5" padding
                    # (24px left + 24px right ≈ 0.5").
                    card_pad_in = 2 * 24.0 / PX_PER_IN
                    item_widths.append(child_width_in if is_plain_flex_row else text_w + card_pad_in)
                else:
                    item_widths.append(child_width_in if is_plain_flex_row else text_w)
            elif sub_elements:
                # Use intrinsic grouped width when text measurement is unavailable,
                # then fall back to a rough text-height-based estimate.
                if intrinsic_group_w > 0:
                    item_widths.append(child_width_in if is_plain_flex_row else intrinsic_group_w)
                else:
                    text_h = sum(e['bounds'].get('height', 0.3) for e in sub_elements if e.get('type') == 'text')
                    item_widths.append(child_width_in if is_plain_flex_row else min(text_h * 3.0, 3.0))
            else:
                item_widths.append(child_width_in)
            group_track_widths.append(child_width_in)
            continue

    # Compute per-item x positions using item_widths
    # For centered grids, determine if items should have uniform or per-item widths
    num_items = len(child_groups)
    item_x_list = []
    wrap_row_indices: List[int] = []

    # Detect if this is a card-like grid (container divs with multi-element children)
    # vs simple content grid (each child has single text element)
    has_multi_children = any(len(g) > 2 for g in child_groups)

    # Single-row centered flex: use per-item widths even with multi-element children
    # (e.g., stat cards where each .g card has shape+text+text but varying widths)
    is_single_row_centered = is_centered and num_items > 1 and num_cols == num_items

    if is_flex_wrap_row:
        wrap_row_indices = [0] * num_items
        rows: List[List[Tuple[int, float]]] = []
        current_row: List[Tuple[int, float]] = []
        current_row_width = 0.0
        max_row_width = flex_inner_width_in

        for idx, width in enumerate(item_widths):
            item_w = max(width, 0.35)
            projected = item_w if not current_row else current_row_width + gap_in + item_w
            if current_row and projected > max_row_width + 1e-6:
                rows.append(current_row)
                current_row = [(idx, item_w)]
                current_row_width = item_w
            else:
                current_row.append((idx, item_w))
                current_row_width = projected
        if current_row:
            rows.append(current_row)

        item_x_list = [margin_in + flex_start_in] * num_items
        for row_idx, row_items in enumerate(rows):
            row_total = sum(width for _, width in row_items) + gap_in * max(len(row_items) - 1, 0)
            if is_centered:
                cursor = margin_in + flex_start_in + max((flex_inner_width_in - row_total) / 2.0, 0.0)
            else:
                cursor = margin_in + flex_start_in
            for item_idx, item_w in row_items:
                wrap_row_indices[item_idx] = row_idx
                item_x_list[item_idx] = cursor
                cursor += item_w + gap_in
    elif is_single_row_centered and not grid_track_widths_in:
        # Centered single-row flex: use individual item widths
        total_content_w = sum(item_widths) + (num_items - 1) * gap_in
        x_start = margin_in + layout_start_in + (layout_inner_width_in - total_content_w) / 2
        current_x = x_start
        for idx in range(num_items):
            item_x_list.append(current_x)
            current_x += item_widths[idx] + gap_in
    elif is_centered and num_items > 1 and not has_multi_children and not grid_track_widths_in:
        # Simple content grid (like stat-row): use individual item widths
        total_content_w = sum(item_widths) + (num_items - 1) * gap_in
        x_start = margin_in + layout_start_in + (layout_inner_width_in - total_content_w) / 2
        current_x = x_start
        for idx in range(num_items):
            item_x_list.append(current_x)
            current_x += item_widths[idx] + gap_in
    elif num_cols > 1 and not grid_cols:
        # Flex-row (no grid-template-columns): position items sequentially
        # with per-item widths (e.g., .layer with emoji + text)
        total_content_w = sum(item_widths) + (num_items - 1) * gap_in
        if is_centered:
            x_start = margin_in + flex_start_in + max((flex_inner_width_in - total_content_w) / 2, 0.0)
        else:
            x_start = margin_in + flex_start_in
        current_x = x_start
        for idx in range(num_items):
            item_x_list.append(current_x)
            current_x += item_widths[idx] + gap_in
    elif num_cols > 1:
        # Multi-column grid (like cards): use uniform column widths
        # For centered grids, center the uniform grid
        if grid_track_widths_in:
            total_w = sum(grid_track_widths_in) + (len(grid_track_widths_in) - 1) * gap_in
            if is_centered:
                x_start = margin_in + layout_start_in + max((layout_inner_width_in - total_w) / 2, 0.0)
            else:
                x_start = margin_in + layout_start_in
            track_x = []
            cursor = x_start
            for track_w in grid_track_widths_in:
                track_x.append(cursor)
                cursor += track_w + gap_in
        else:
            if is_centered:
                total_w = num_cols * item_width_in + (num_cols - 1) * gap_in
                x_start = margin_in + layout_start_in + (layout_inner_width_in - total_w) / 2
            else:
                x_start = margin_in + layout_start_in + x_offset
        for idx in range(num_items):
            col_idx = idx % num_cols
            row_idx = idx // num_cols
            # Flex-column items: use stored grid column index and row within column
            if child_groups[idx] and child_groups[idx][0].get('_flex_column_item'):
                col_idx = child_groups[idx][0].get('_grid_col_idx', 0)
                row_idx = child_groups[idx][0].get('_row_in_col', idx)
            if grid_track_widths_in:
                safe_col_idx = min(col_idx, len(track_x) - 1)
                item_x_list.append(track_x[safe_col_idx])
            else:
                item_x_list.append(x_start + col_idx * (item_width_in + gap_in))
    else:
        for idx in range(num_items):
            item_x_list.append(margin_in + layout_start_in)

    final_item_widths: List[float] = []
    for idx in range(num_items):
        if (
            is_single_row_centered or
            is_flex_wrap_row or
            (is_centered and num_items > 1 and not has_multi_children and not grid_track_widths_in) or
            is_plain_flex_row
        ):
            this_item_width = item_widths[idx] if idx < len(item_widths) else item_width_in
        elif grid_track_widths_in and num_cols > 1:
            if child_groups[idx] and child_groups[idx][0].get('_flex_column_item'):
                col_idx = child_groups[idx][0].get('_grid_col_idx', 0)
            else:
                col_idx = idx % num_cols
            this_item_width = (
                group_track_widths[idx]
                if idx < len(group_track_widths)
                else grid_track_widths_in[min(col_idx, len(grid_track_widths_in) - 1)]
            )
        else:
            this_item_width = item_width_in
        final_item_widths.append(this_item_width)

    for idx, group in enumerate(child_groups):
        _normalize_card_group_text_metrics(group, final_item_widths[idx] if idx < len(final_item_widths) else item_width_in)

    # Layout grid items
    results = []

    # Pre-pass: compute each row's height (max of items in that row) so we can
    # compute cumulative Y positions correctly (instead of row_idx * current_item_h)
    # For flex-column grids, each column has INDEPENDENT row heights.
    # Plain multi-column grids should still share a row max-height so sibling cards
    # stretch together. Only opt into per-column keys when the layout actually
    # contains column-stacked items.
    row_heights = {}  # (col, row_in_col) or just row_idx -> max item_h
    # Per-column row accumulation only makes sense for actual multi-column grids.
    # Single-column containers can still contain flex-column descendants, but those
    # should keep the simpler shared row-key path.
    use_col_key = num_cols > 1 and any(group and group[0].get('_flex_column_item') for group in child_groups)
    for idx, group in enumerate(child_groups):
        if is_flex_wrap_row:
            rh_key = wrap_row_indices[idx]
            col_idx = 0
            row_in_col = wrap_row_indices[idx]
        elif num_cols > 1:
            if group and group[0].get('_flex_column_item'):
                col_idx = group[0].get('_grid_col_idx', 0)
                row_in_col = group[0].get('_row_in_col', idx)
            else:
                col_idx = idx % num_cols
                row_in_col = idx // num_cols
            rh_key = (col_idx, row_in_col) if use_col_key else row_in_col
        else:
            rh_key = idx
            col_idx = 0
            row_in_col = idx

        # Estimate item height (same logic as below)
        bg_elem = None
        for e in group:
            if e.get('type') == 'shape' and not e.get('text') and e['bounds'].get('height', 0) >= 1.0:
                bg_elem = e
                break
        text_h = sum(e['bounds'].get('height', 0.3) for e in group if e.get('type') == 'text')
        table_h = sum(
            e.get('bounds', {}).get('height', 0.0) or
            sum(row.get('height', 0.264) for row in e.get('rows', []))
            for e in group if e.get('type') in ('table', 'presentation_rows')
        )
        container_h = max((e['bounds'].get('height', 0.0) for e in group if e.get('type') == 'container'), default=0.0)

        # For flex-row groups (like .layer), the text elements have pre-computed
        # relative Y positions. Use actual Y extent instead of sum of heights,
        # because sum doesn't account for vertical gaps between elements.
        flex_row_texts = [e for e in group if e.get('type') == 'text' and e.get('_flex_row_child')]
        decoration_only = bool(group) and all(e.get('_is_decoration') for e in group)
        shape_only_group = bool(group) and all(e.get('type') == 'shape' for e in group)
        flow_content_h = _measure_group_flow_height(group, default_gap=0.05)
        if decoration_only:
            ih = max((e['bounds'].get('height', 0.1) for e in group), default=0.1)
        elif shape_only_group:
            ih = max((e['bounds'].get('height', 0.1) for e in group), default=0.1)
        elif flex_row_texts:
            # Elements at the top row (emoji, h4) share the same Y level.
            # Paragraphs are below. Use the pre-computed Y positions to get
            # the actual content extent.
            min_y = min(e['bounds']['y'] for e in flex_row_texts)
            max_y = max(e['bounds']['y'] + e['bounds']['height'] for e in flex_row_texts)
            content_extent = max_y - min_y
            if bg_elem:
                pad_t = bg_elem.get('_css_pad_t', 14.0 / PX_PER_IN)
                pad_b = bg_elem.get('_css_pad_b', 14.0 / PX_PER_IN)
                ih = content_extent + pad_t + pad_b
            else:
                ih = content_extent + 0.26  # default padding
        elif flow_content_h > 0:
            if bg_elem:
                pad_t = bg_elem.get('_css_pad_t', 15.0 / PX_PER_IN)
                pad_b = bg_elem.get('_css_pad_b', 15.0 / PX_PER_IN)
                ih = flow_content_h + pad_t + pad_b
            else:
                ih = flow_content_h
        elif text_h > 0:
            tcnt = sum(1 for e in group if e.get('type') == 'text')
            if bg_elem:
                pad_t = bg_elem.get('_css_pad_t', 15.0 / PX_PER_IN)
                pad_b = bg_elem.get('_css_pad_b', 15.0 / PX_PER_IN)
                li_cnt = sum(1 for e in group if e.get('tag') == 'li')
                non_li = tcnt - li_cnt
                li_g = 7.0 / PX_PER_IN
                t_margin = sum((parse_px(e.get('styles', {}).get('marginBottom', '')) / PX_PER_IN) for e in group if e.get('type') == 'text')
                g_css = li_g * max(li_cnt - 1, 0) + 0.05 * max(non_li, 0) + 0.05 * min(li_cnt, 1) * min(non_li, 1)
                ih = text_h + pad_t + pad_b + max(g_css, t_margin) + table_h
            else:
                ih = text_h + 0.05 * max(tcnt - 1, 0) + table_h
        elif table_h > 0:
            # Group has a table but no text elements at top level
            if bg_elem:
                pad_t = bg_elem.get('_css_pad_t', 15.0 / PX_PER_IN)
                pad_b = bg_elem.get('_css_pad_b', 15.0 / PX_PER_IN)
                ih = table_h + pad_t + pad_b
            else:
                ih = table_h
        else:
            ih = container_h if container_h > 0 else 2.0
        if container_h > 0:
            ih = max(ih, container_h)
        if rh_key not in row_heights or ih > row_heights[rh_key]:
            row_heights[rh_key] = ih

    # Compute cumulative Y: for multi-column grids with independent columns,
    # compute per-column cumulative Y. For single-column or simple grids, use shared.
    row_y = {}
    if use_col_key:
        # Group keys by column, compute cumulative Y per column
        cols = set(k[0] for k in row_heights.keys())
        for col in cols:
            col_rows = sorted(k[1] for k in row_heights.keys() if k[0] == col)
            cumulative_y = 0.0
            for ri in col_rows:
                row_y[(col, ri)] = cumulative_y
                cumulative_y += row_heights[(col, ri)] + gap_in
    else:
        sorted_rows = sorted(row_heights.keys())
        cumulative_y = 0.0
        for ri, sr in enumerate(sorted_rows):
            row_y[sr] = cumulative_y
            cumulative_y += row_heights[sr] + gap_in

    row_cross_offsets: Dict[int, float] = {}
    if is_plain_flex_row and style.get('alignItems', style.get('align-items', '')) == 'baseline':
        group_baselines = []
        for idx, group in enumerate(child_groups):
            bg_shape = next((e for e in group if e.get('_is_card_bg')), None)
            group_baselines.append(_estimate_group_baseline_in(group, bg_shape))
        if group_baselines:
            max_baseline = max(group_baselines)
            row_cross_offsets = {
                idx: max(max_baseline - baseline, 0.0)
                for idx, baseline in enumerate(group_baselines)
            }

    for idx, group in enumerate(child_groups):
        if is_flex_wrap_row:
            col_idx = 0
            row_idx = wrap_row_indices[idx]
            ry_key = row_idx
        elif num_cols > 1:
            # Flex-column items stay in their assigned column, using row within column
            if group and group[0].get('_flex_column_item'):
                col_idx = group[0].get('_grid_col_idx', 0)
                row_idx = group[0].get('_row_in_col', idx)
            else:
                col_idx = idx % num_cols
                row_idx = idx // num_cols
            ry_key = (col_idx, row_idx) if use_col_key else row_idx
        else:
            col_idx = 0
            row_idx = idx
            ry_key = row_idx

        item_x = item_x_list[idx]
        # Use per-item width for centered single-row and simple grids
        if (
            is_single_row_centered or
            is_flex_wrap_row or
            (is_centered and num_items > 1 and not has_multi_children and not grid_track_widths_in) or
            is_plain_flex_row
        ):
            this_item_width = item_widths[idx] if idx < len(item_widths) else item_width_in
        elif grid_track_widths_in and num_cols > 1:
            this_item_width = group_track_widths[idx] if idx < len(group_track_widths) else grid_track_widths_in[min(col_idx, len(grid_track_widths_in) - 1)]
        else:
            this_item_width = item_width_in

        # Detect bg shape early (needed for height calculation)
        bg_shape_elem = None
        for e in group:
            if (e.get('type') == 'shape' and not e.get('text')
                    and e['bounds'].get('height', 0) >= 1.0):
                bg_shape_elem = e
                break

        # Estimate item height from its elements' existing bounds
        text_h_total = 0.0
        has_text = False
        container_h = max((e['bounds'].get('height', 0.0) for e in group if e.get('type') == 'container'), default=0.0)
        for elem in group:
            if elem.get('type') == 'text':
                text_h_total += elem['bounds'].get('height', 0.3)
                has_text = True
            elif elem.get('type') == 'table':
                text_h_total += (
                    elem['bounds'].get('height', 0.0) or
                    sum(row.get('height', 0.264) for row in elem.get('rows', []))
                )
                has_text = True
            elif elem.get('type') == 'presentation_rows':
                text_h_total += (
                    elem['bounds'].get('height', 0.0) or
                    sum(row.get('height', 0.264) for row in elem.get('rows', []))
                )
                has_text = True

        decoration_only = bool(group) and all(e.get('_is_decoration') for e in group)
        shape_only_group = bool(group) and all(e.get('type') == 'shape' for e in group)
        flex_row_texts = [e for e in group if e.get('type') == 'text' and e.get('_flex_row_child')]
        flow_content_h = _measure_group_flow_height(group, default_gap=0.05)
        if decoration_only:
            item_h = max((e['bounds'].get('height', 0.1) for e in group), default=0.1)
        elif shape_only_group:
            item_h = max((e['bounds'].get('height', 0.1) for e in group), default=0.1)
        elif bg_shape_elem and flow_content_h > 0 and not flex_row_texts:
            card_pad_t = bg_shape_elem.get('_css_pad_t', 15.0 / PX_PER_IN)
            card_pad_b = bg_shape_elem.get('_css_pad_b', 15.0 / PX_PER_IN)
            item_h = flow_content_h + card_pad_t + card_pad_b
        elif has_text:
            text_count = sum(1 for e in group if e.get('type') == 'text')
            if bg_shape_elem:
                # Card: use CSS padding from bg shape
                card_pad_t = bg_shape_elem.get('_css_pad_t', 15.0 / PX_PER_IN)
                card_pad_b = bg_shape_elem.get('_css_pad_b', 15.0 / PX_PER_IN)
                # Internal gap: compute from actual marginBottom of text elements
                # rather than hardcoded defaults
                li_count = sum(1 for e in group if e.get('tag') == 'li')
                non_li_count = text_count - li_count
                li_gap = 7.0 / PX_PER_IN  # ul.bl gap: 7px
                # Sum marginBottom from text elements (h3 margin-bottom: 10px etc.)
                total_text_margin = 0.0
                for elem in group:
                    if elem.get('type') == 'text':
                        mb = elem.get('styles', {}).get('marginBottom', '')
                        mb_px = parse_px(mb) if mb else 0
                        total_text_margin += mb_px / PX_PER_IN
                # Use the larger of CSS gap-based or margin-based spacing
                other_gap = 0.05
                gap_from_css = (li_gap * max(li_count - 1, 0) +
                                other_gap * max(non_li_count, 0) +
                                other_gap * min(li_count, 1) * min(non_li_count, 1))
                internal_gap = max(gap_from_css, total_text_margin)
                item_h = text_h_total + card_pad_t + card_pad_b + internal_gap
            else:
                internal_gap = 0.05 * max(text_count - 1, 0)
                item_h = text_h_total + internal_gap
        else:
            item_h = container_h if container_h > 0 else 2.0  # default for non-text items
        if container_h > 0:
            item_h = max(item_h, container_h)

        # Use pre-computed cumulative row Y instead of row_idx * (item_h + gap_in)
        # to correctly handle grids where different rows have different heights
        item_y = layout_pad_t + row_y.get(ry_key, row_idx * (item_h + gap_in)) + row_cross_offsets.get(idx, 0.0)
        # Layout elements: background shapes overlap content, content stacks vertically
        has_bg_shape = bg_shape_elem is not None
        stretch_to_row_height = (
            (has_bg_shape or any(
                e.get('type') == 'container' and
                e.get('_children_relative') and
                any(child.get('_is_card_bg') for child in e.get('children', []))
                for e in group
            )) and
            num_cols > 1 and
            not is_plain_flex_row and
            not (group and group[0].get('_flex_column_item'))
        )
        row_item_h = row_heights.get(ry_key, item_h) if stretch_to_row_height else item_h
        # Use CSS padding from bg shape if available, otherwise defaults
        if has_bg_shape:
            pad_t = bg_shape_elem.get('_css_pad_t', 15.0 / PX_PER_IN)
            pad_x = bg_shape_elem.get('_css_pad_l', 15.0 / PX_PER_IN)
            border_l = bg_shape_elem.get('_css_border_l', 0.0)
        else:
            pad_t = 0.0
            pad_x = 0.0
            border_l = 0.0

        group_y = item_y + pad_t
        flow_items = _iter_group_flow_items(group)
        flow_gaps = {}
        for flow_idx, flow_elem in enumerate(flow_items[:-1]):
            flow_gaps[id(flow_elem)] = _flow_gap_in(flow_elem, flow_items[flow_idx + 1], 0.05)
        next_flow_by_id = {
            id(flow_items[flow_idx]): flow_items[flow_idx + 1]
            for flow_idx in range(len(flow_items) - 1)
        }
        paired_shapes = {
            e.get('_pair_with'): e for e in group
            if e.get('type') == 'shape' and e.get('_pair_with')
        }
        group_text_count = sum(1 for e in group if e.get('type') == 'text')
        group_other_content_count = sum(
            1 for e in group
            if e.get('type') in ('shape', 'table', 'presentation_rows', 'image', 'container')
            and not e.get('_pair_with')
            and not e.get('_is_decoration')
        )
        for elem in group:
            b = elem['bounds']
            elem['layoutDone'] = True
            # Check if this is a pure background shape (no text, height >= 2)
            is_bg_shape = (
                elem.get('_is_card_bg') or
                (elem.get('type') == 'shape' and not elem.get('text') and b.get('height', 0) >= 2.0)
            )
            if is_bg_shape:
                # Background shape: same position as content area, full item height
                b['x'] = item_x
                b['y'] = item_y
                b['width'] = this_item_width
                b['height'] = row_item_h
                results.append(elem)
                continue  # Don't advance group_y
            if elem.get('type') in ('text', 'shape'):
                # Flex-row children have pre-set relative x positions.
                # Use item_x + relative x instead of overwriting.
                if elem.get('_flex_row_child'):
                    b['x'] = item_x + b.get('x', 0)
                    # Preserve relative y offset (e.g., layer padding, element spacing)
                    b['y'] = item_y + b.get('y', 0)
                    results.append(elem)
                    continue

                b['x'] = item_x + pad_x + border_l
                b['y'] = group_y
                # Paired shapes (pill/badge backgrounds) and decorations overlay text — don't advance Y
                if elem.get('type') == 'shape' and (elem.get('_pair_with') or elem.get('_is_decoration')):
                    results.append(elem)
                    continue
                # For text elements, decide whether to use constrained width or shrink-wrap
                if elem.get('type') == 'text':
                    orig_w = b.get('width', 0)
                    pad_r_val = bg_shape_elem.get('_css_pad_r', pad_x) if bg_shape_elem else pad_x
                    card_content_w = this_item_width - pad_x - pad_r_val if bg_shape_elem else this_item_width - 2 * pad_x
                    css_text_align = bg_shape_elem.get('_css_text_align', 'left') if bg_shape_elem else 'left'
                    tag = elem.get('tag', '')
                    is_block_text = tag in ('h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li')
                    next_flow_item = next_flow_by_id.get(id(elem))
                    paired_shape = paired_shapes.get(elem.get('_pair_with'))
                    elem_styles = elem.get('styles', {})
                    stretch_inline_hint_row = (
                        tag in INLINE_TAGS and
                        elem_styles.get('display', '') == 'inline-flex' and
                        not any(
                            elem_styles.get(key, '')
                            for key in ('backgroundColor', 'border', 'borderLeft', 'borderRight', 'borderTop', 'borderBottom')
                        ) and
                        parse_px(elem_styles.get('width', '')) <= 0 and
                        parse_px(elem_styles.get('maxWidth', '')) <= 0
                    )
                    if paired_shape:
                        pb = paired_shape.get('bounds', {})
                        b['x'] = pb.get('x', b['x'])
                        b['y'] = pb.get('y', b['y'])
                        if pb.get('width', 0) > 0:
                            b['width'] = pb['width']
                        if pb.get('height', 0) > 0:
                            b['height'] = max(b.get('height', 0), pb['height'])
                    elif (elem.get('_stretch_to_parent_width') or stretch_inline_hint_row) and bg_shape_elem:
                        b['width'] = card_content_w - border_l
                        b['x'] = item_x + pad_x + border_l
                        _remeasure_text_for_final_width(elem, b['width'], next_flow_item=next_flow_item, inside_card=True)
                    elif elem.get('_pair_with') and bg_shape_elem and orig_w > 0:
                        b['width'] = card_content_w - border_l
                        _remeasure_text_for_final_width(elem, b['width'], next_flow_item=next_flow_item, inside_card=True)
                    elif is_block_text and orig_w > 0.5:
                        # Block text inside card: use full content width
                        b['width'] = card_content_w - border_l
                        if css_text_align == 'center':
                            # Centered card (stat cards): center the full-width text frame
                            b['x'] = item_x + pad_x
                        else:
                            # Left-aligned card: position after padding + border
                            b['x'] = item_x + pad_x + border_l
                        _remeasure_text_for_final_width(elem, b['width'], next_flow_item=next_flow_item, inside_card=True)
                    elif is_block_text and group_text_count == 1 and group_other_content_count == 0:
                        b['width'] = card_content_w - border_l
                        b['x'] = item_x + pad_x + border_l
                        _remeasure_text_for_final_width(elem, b['width'], next_flow_item=next_flow_item, inside_card=True)
                    elif is_block_text:
                        b['x'] = item_x + pad_x + border_l
                        if b.get('width', 0) > card_content_w:
                            b['width'] = card_content_w
                        _remeasure_text_for_final_width(elem, b['width'], next_flow_item=next_flow_item, inside_card=True)
                    else:
                        # Short/plain text: shrink-wrap to natural width and center
                        # Unless element has explicit CSS dimensions (like step circles)
                        if elem.get('_use_css_dims'):
                            # Keep the existing width (set from CSS dimensions)
                            # Position at left edge with CSS padding, don't center
                            natural_w = b['width']
                            b['x'] = item_x + pad_x + border_l
                        else:
                            elem_text = elem.get('text', '')
                            elem_styles = elem.get('styles', {})
                            if elem.get('preferContentWidth') and elem.get('inlineContentWidth', 0.0) > 0:
                                natural_w = elem.get('inlineContentWidth', 0.0)
                                b['width'] = min(natural_w, card_content_w)
                            else:
                                elem_font_px = parse_px(elem_styles.get('fontSize', '16px'))
                                if elem_font_px <= 0:
                                    elem_font_px = 16.0
                                max_line_px = 0.0
                                for line in elem_text.split('\n'):
                                    line = line.strip()
                                    if not line:
                                        continue
                                    line_w = _estimate_text_width_px(
                                        line,
                                        elem_font_px,
                                        monospace=_uses_monospace_font(elem_styles.get('fontFamily', '')),
                                        letter_spacing=elem_styles.get('letterSpacing', ''),
                                    )
                                    if line_w > max_line_px:
                                        max_line_px = line_w
                                natural_w = max_line_px / PX_PER_IN
                                b['width'] = natural_w + 0.1  # small padding
                            if _looks_like_centered_command_text(elem, elem_styles):
                                elem['preferNoWrapFit'] = True
                                b['width'] = card_content_w
                                _remeasure_text_for_final_width(elem, b['width'], next_flow_item=next_flow_item, inside_card=True)
                            elif b['width'] > card_content_w:
                                b['width'] = card_content_w
                                _remeasure_text_for_final_width(elem, b['width'], next_flow_item=next_flow_item, inside_card=True)
                            b['x'] = item_x + pad_x + border_l + max((card_content_w - b['width']) / 2, 0.0)
                else:
                    b['width'] = this_item_width - 2 * pad_x
                gap_after = flow_gaps.get(id(elem), 0.0)
                group_y += b['height'] + gap_after
            elif elem.get('type') in ('table', 'presentation_rows'):
                b['x'] = item_x + pad_x + border_l
                b['y'] = group_y
                b['width'] = this_item_width - 2 * pad_x if has_bg_shape else this_item_width
                group_y += b['height'] + flow_gaps.get(id(elem), 0.0)
            elif elem.get('type') == 'image':
                b['x'] = item_x
                b['y'] = group_y
                b['width'] = item_width_in
                group_y += b['height'] + flow_gaps.get(id(elem), 0.0)
            elif elem.get('type') == 'container':
                if elem.get('layout') == 'flow_box':
                    if stretch_to_row_height:
                        _stretch_relative_card_container_to_height(elem, row_item_h)
                    b['x'] = item_x
                    b['y'] = item_y
                    results.append(elem)
                    continue
                if elem.get('_children_relative'):
                    has_nested_card_bg = any(child.get('_is_card_bg') for child in elem.get('children', []))
                    if has_nested_card_bg:
                        _stretch_relative_card_container_to_width(elem, this_item_width)
                    if stretch_to_row_height:
                        _stretch_relative_card_container_to_height(elem, row_item_h)
                    b['x'] = item_x + pad_x + border_l
                    b['y'] = group_y
                    results.append(elem)
                    group_y += elem.get('bounds', {}).get('height', 0.2) + flow_gaps.get(id(elem), 0.0)
                    continue
                # Unwrap nested container (e.g., flex-row header with dot+text+text)
                inner_children = elem.get('children', [])
                inner_x = item_x + pad_x + border_l
                for ic in inner_children:
                    icb = ic.get('bounds', {})
                    # Skip full-width bg shapes from inner grid layout
                    if (ic.get('type') == 'shape' and not ic.get('text')
                            and not ic.get('_is_decoration')
                            and icb.get('height', 0) >= 1.0):
                        continue
                    icb['x'] = inner_x
                    icb['y'] = group_y
                    ic['layoutDone'] = True
                    results.append(ic)
                    inner_x += icb.get('width', 0) + 0.05
                group_y += elem.get('bounds', {}).get('height', 0.2) + flow_gaps.get(id(elem), 0.0)
                continue  # Don't append the container wrapper itself
            results.append(elem)

    # Mark all grid children so pill positioning can skip them
    for elem in results:
        elem['_grid_child'] = True

    return results


# ─── Slide Background Extraction ─────────────────────────────────────────────

def _extract_grid_background_from_style(style: Dict[str, str]) -> Optional[Dict[str, Any]]:
    bg_image = style.get('backgroundImage', '')
    gradient_count = len(re.findall(r'linear-gradient', bg_image))
    if gradient_count < 2 or '90deg' not in bg_image:
        return None
    color_match = re.search(r'rgba?\([^)]+\)|#[0-9a-fA-F]{3,8}|var\(--[^)]+\)', bg_image)
    if not color_match:
        return None
    color_token = color_match.group(0).strip()
    if color_token.startswith('var('):
        var_match = re.match(r'var\((--[^),]+)', color_token)
        if not var_match:
            return None
        color_token = (_ROOT_CSS_VARS.get(var_match.group(1), '') or '').strip()
        if not color_token:
            return None

    opacity = 1.0
    opacity_str = style.get('opacity', '').strip()
    if opacity_str:
        try:
            opacity = max(0.0, min(1.0, float(opacity_str)))
        except Exception:
            opacity = 1.0

    rgba_match = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)', color_token)
    if rgba_match:
        r, g, b = int(rgba_match.group(1)), int(rgba_match.group(2)), int(rgba_match.group(3))
        alpha = float(rgba_match.group(4) or '1.0') * opacity
        color_value = f'rgba({r}, {g}, {b}, {alpha:.3f})'
    else:
        rgb = parse_color(color_token)
        if not rgb:
            return None
        color_value = f'rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {opacity:.3f})'

    size_str = style.get('backgroundSize', '')
    size_match = re.search(r'([\d.]+)px', size_str)
    size_px = float(size_match.group(1)) if size_match else 24.0
    return {'color': color_value, 'sizePx': size_px}


_RADIAL_MESH_RE = re.compile(
    r"radial-gradient\(\s*ellipse\s+at\s+([\d.]+)%\s+([\d.]+)%,\s*"
    r"((?:rgba?\([^)]+\))|(?:#[0-9a-fA-F]{3,8})|(?:var\(--[^)]+\)))\s+0%,\s*"
    r"transparent\s+([\d.]+)%\s*\)",
    re.IGNORECASE | re.DOTALL,
)


def _extract_aurora_mesh_background_from_style(style: Dict[str, str]) -> Optional[Dict[str, Any]]:
    bg_image = style.get('backgroundImage', '')
    if bg_image.count('radial-gradient(') < 2:
        return None

    layers: List[Dict[str, Any]] = []
    for match in _RADIAL_MESH_RE.finditer(bg_image):
        rgba = _parse_rgba_color(match.group(3))
        if not rgba:
            continue
        layers.append({
            'cx_pct': float(match.group(1)),
            'cy_pct': float(match.group(2)),
            'color': rgba,
            'radius_pct': float(match.group(4)),
        })

    if len(layers) < 2:
        return None

    base_rgb = parse_color(style.get('backgroundColor', '')) or (10, 10, 26)
    return {
        'kind': 'aurora-mesh',
        'baseColor': base_rgb,
        'layers': layers,
    }


def extract_body_mesh_background(
    body_style: Dict[str, str],
    contract: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    if contract and (contract.get('contract_id') != 'slide-creator/aurora-mesh'):
        return None
    return _extract_aurora_mesh_background_from_style(body_style)


def _composite_rgba_over_bg(
    rgba: Tuple[int, int, int, float],
    bg: Tuple[int, int, int],
) -> Tuple[int, int, int]:
    r, g, b, alpha = rgba
    alpha = max(0.0, min(alpha, 1.0))
    return (
        int(alpha * r + (1.0 - alpha) * bg[0]),
        int(alpha * g + (1.0 - alpha) * bg[1]),
        int(alpha * b + (1.0 - alpha) * bg[2]),
    )


def _approximate_aurora_mesh_solid_color(
    mesh_bg: Optional[Dict[str, Any]],
) -> Optional[Tuple[int, int, int]]:
    """Approximate aurora mesh backgrounds with a close solid color.

    We intentionally avoid exporting the animated mesh itself for Aurora decks,
    but falling all the way back to the body base color (`#0a0a1a`) makes the
    slide look much flatter than the source. Sample a low-resolution composite
    of the mesh layers and use its average as the solid slide fill.
    """
    if not mesh_bg:
        return None

    base = mesh_bg.get('baseColor') or (10, 10, 26)
    layers = mesh_bg.get('layers') or []
    if not layers:
        return base

    sample_w = 56
    sample_h = 36
    total_r = 0.0
    total_g = 0.0
    total_b = 0.0

    for iy in range(sample_h):
        y_pct = (iy + 0.5) * 100.0 / sample_h
        for ix in range(sample_w):
            x_pct = (ix + 0.5) * 100.0 / sample_w
            r, g, b = float(base[0]), float(base[1]), float(base[2])

            for layer in layers:
                rgba = layer.get('color')
                if not rgba:
                    continue
                lr, lg, lb, alpha = rgba
                radius_pct = max(float(layer.get('radius_pct', 50.0)), 12.0)
                rx_pct = max(radius_pct * 1.05, 8.0)
                ry_pct = max(radius_pct * 0.96, 7.0)
                dx = (x_pct - float(layer.get('cx_pct', 50.0))) / rx_pct
                dy = (y_pct - float(layer.get('cy_pct', 50.0))) / ry_pct
                dist = dx * dx + dy * dy
                if dist >= 1.0:
                    continue

                # Soft radial falloff roughly matching the blurred ellipse path.
                local_alpha = max(0.0, min(alpha, 1.0)) * ((1.0 - dist) ** 1.2)
                r = local_alpha * lr + (1.0 - local_alpha) * r
                g = local_alpha * lg + (1.0 - local_alpha) * g
                b = local_alpha * lb + (1.0 - local_alpha) * b

            total_r += r
            total_g += g
            total_b += b

    samples = float(sample_w * sample_h)
    avg = (
        int(round(total_r / samples)),
        int(round(total_g / samples)),
        int(round(total_b / samples)),
    )
    dominant_layer = max(
        (layer for layer in layers if layer.get('color')),
        key=lambda layer: float(layer.get('radius_pct', 0.0)) * float(layer['color'][3]),
        default=None,
    )
    dominant_comp = _composite_rgba_over_bg(dominant_layer['color'], base) if dominant_layer else avg

    # Bias the solid fallback slightly toward the strongest mesh layer. Aurora's
    # browser rendering reads more purple than a plain arithmetic average.
    return (
        int(round(avg[0] * 0.65 + dominant_comp[0] * 0.35)),
        int(round(avg[1] * 0.65 + dominant_comp[1] * 0.35)),
        int(round(avg[2] * 0.65 + dominant_comp[2] * 0.35)),
    )


def build_aurora_mesh_overlay_elements(
    mesh_bg: Optional[Dict[str, Any]],
    slide_width_px: float,
    slide_height_px: float,
) -> List[Dict[str, Any]]:
    if not mesh_bg:
        return []

    slide_w_in = slide_width_px / PX_PER_IN
    slide_h_in = slide_height_px / PX_PER_IN
    base = mesh_bg.get('baseColor') or (10, 10, 26)
    overlays: List[Dict[str, Any]] = []

    for layer in mesh_bg.get('layers') or []:
        rgba = layer.get('color')
        if not rgba:
            continue
        fill_rgb = _composite_rgba_over_bg(rgba, base)
        cx_in = slide_w_in * float(layer.get('cx_pct', 50.0)) / 100.0
        cy_in = slide_h_in * float(layer.get('cy_pct', 50.0)) / 100.0
        radius_pct = max(float(layer.get('radius_pct', 50.0)), 14.0)
        blob_w_in = max(slide_w_in * radius_pct / 100.0 * 1.72, slide_w_in * 0.42)
        blob_h_in = max(slide_h_in * radius_pct / 100.0 * 1.44, slide_h_in * 0.34)
        overlays.append({
            'type': 'shape',
            'tag': 'circle',
            'bounds': {
                'x': cx_in - blob_w_in / 2.0,
                'y': cy_in - blob_h_in / 2.0,
                'width': blob_w_in,
                'height': blob_h_in,
            },
            'styles': {
                'backgroundColor': f'#{fill_rgb[0]:02X}{fill_rgb[1]:02X}{fill_rgb[2]:02X}',
                'backgroundImage': '',
                'border': '',
                'borderLeft': '',
                'borderRight': '',
                'borderTop': '',
                'borderBottom': '',
                'borderRadius': '999px',
                'marginTop': '',
                'marginBottom': '',
                'marginLeft': '',
                'marginRight': '',
            },
            '_is_decoration': True,
            '_skip_layout': True,
        })

    return overlays


def extract_body_decorative_background(
    css_rules: List[CSSRule],
    contract: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    candidate_selectors = {'body::before'}
    if contract:
        for layer in contract.get('decorative_layers', []):
            if layer.get('export_strategy') == 'background-layer' and layer.get('selector'):
                candidate_selectors.add(layer['selector'])

    for rule in css_rules:
        if rule.selector not in candidate_selectors:
            continue
        grid = _extract_grid_background_from_style(rule.properties)
        if grid:
            return grid
    return None


def extract_slide_background(slide_el: Tag, css_rules: List[CSSRule]) -> Dict:
    """Extract slide-level background (solid color, gradient, or grid)."""
    style = compute_element_style(slide_el, css_rules, slide_el.get('style', ''))
    bg_color = style.get('backgroundColor', '')
    bg_image = style.get('backgroundImage', '')

    result = {'solid': None, 'gradient': None, 'grid': None}

    if 'gradient' in bg_image:
        # Try rgba() stops first, then fall back to hex colors
        stops = re.findall(r'rgba?\([^)]+\)', bg_image)
        if len(stops) >= 2:
            c1 = parse_color(stops[0])
            c2 = parse_color(stops[-1])
            if c1 and c2:
                result['gradient'] = (c1, c2)
        else:
            # Fallback: extract hex colors from gradient
            hex_stops = re.findall(r'#([0-9a-fA-F]{6})', bg_image)
            if len(hex_stops) >= 2:
                c1 = (int(hex_stops[0][0:2], 16), int(hex_stops[0][2:4], 16), int(hex_stops[0][4:6], 16))
                c2 = (int(hex_stops[-1][0:2], 16), int(hex_stops[-1][2:4], 16), int(hex_stops[-1][4:6], 16))
                result['gradient'] = (c1, c2)

    if not result['gradient']:
        rgb = parse_color(bg_color)
        if rgb:
            result['solid'] = rgb

    result['grid'] = _extract_grid_background_from_style(style)

    return result


# ─── HTML → Slides Parsing ───────────────────────────────────────────────────

def discover_slide_roots(soup: BeautifulSoup) -> List[Tag]:
    explicit_roots = soup.select('.slide')
    if explicit_roots:
        return explicit_roots

    body = soup.find('body')
    if not body:
        return []

    roots: List[Tag] = []
    for child in body.find_all(recursive=False):
        if _is_slide_root_element(child):
            roots.append(child)
    return roots


def _assign_support_tier(signals: Dict[str, Any]) -> str:
    if signals.get('contract_found'):
        return 'contract_bound'
    if (
        signals.get('producer_confidence') in {'high', 'medium'}
        and signals.get('producer_signals', 0) >= 2
    ):
        return 'producer_aware'
    if (
        signals.get('page_boundary_count', 0) > 0
        and signals.get('semantic_signals', 0) >= 2
    ):
        return 'semantic_enhanced'
    return 'generic_safe'


def _build_global_downgrade_chain() -> List[str]:
    return [
        'preserve_structure',
        'preserve_grouping',
        'degrade_decorative',
        'shrink_if_allowed',
    ]


def _collect_semantic_deck_signals(slide_roots: List[Tag]) -> List[str]:
    signals: List[str] = []
    if slide_roots:
        signals.append('slide_roots')
    if any(root.name == 'section' for root in slide_roots):
        signals.append('section_roots')
    if any(root.get('data-slide') is not None for root in slide_roots):
        signals.append('data_slide_markers')
    if any(root.find(['h1', 'h2', 'h3']) for root in slide_roots):
        signals.append('headings_present')
    if any(root.select_one('.card, [class*="card"]') for root in slide_roots):
        signals.append('card_like_content')
    return signals


def _count_authored_slide_anchored_children(
    slide_html: Tag,
    css_rules: List[CSSRule],
) -> int:
    slide_style = compute_element_style(slide_html, css_rules, slide_html.get('style', ''))
    count = 0
    for child in _direct_tag_children(slide_html):
        child_style = compute_element_style(child, css_rules, child.get('style', ''), slide_style)
        if _is_slide_or_body_anchored_positioned(child, child_style):
            count += 1
    return count


def _collect_slide_raw_signals(
    slide_html: Tag,
    slide_index: int,
    css_rules: List[CSSRule],
    contract: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    layout_info = _classify_slide_layout(slide_html, contract)
    text_nodes = slide_html.find_all(TEXT_TAGS)
    headings = slide_html.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    paragraphs = slide_html.find_all(['p', 'li'])
    images = slide_html.find_all(['img', 'svg', 'canvas'])
    tables = slide_html.find_all('table')
    card_like = slide_html.select('.card, [class*="card"]')
    text_values = [txt.strip() for txt in slide_html.stripped_strings if txt.strip()]
    overlay_count = _count_authored_slide_anchored_children(slide_html, css_rules)

    component_signals: List[str] = []
    if card_like:
        component_signals.append('card_like')
    if images:
        component_signals.append('visual_media')
    if tables:
        component_signals.append('table')

    text_signals: List[str] = []
    if headings:
        text_signals.append('headings')
    if paragraphs:
        text_signals.append('body_copy')
    if any(len(text) >= 80 for text in text_values):
        text_signals.append('long_copy')

    overlay_signals: List[str] = []
    if overlay_count:
        overlay_signals.append('slide_anchored')

    has_local_contract_evidence = bool(raw_role := (slide_html.get('data-export-role', '') or layout_info.get('role', '')))
    if layout_info.get('support_tier') in {'canonical', 'compatible'}:
        has_local_contract_evidence = True

    return {
        'slide_index': slide_index,
        'root_tag': slide_html.name,
        'root_classes': list(slide_html.get('class', [])),
        'role': raw_role,
        'intent': slide_html.get('data-export-intent', ''),
        'layout_support_tier': layout_info.get('support_tier', ''),
        'has_local_contract_evidence': has_local_contract_evidence,
        'text_count': len(text_nodes),
        'heading_count': len(headings),
        'paragraph_count': len(paragraphs),
        'image_count': len(images),
        'table_count': len(tables),
        'overlay_count': overlay_count,
        'component_signals': component_signals,
        'text_signals': text_signals,
        'overlay_signals': overlay_signals,
        'semantic_signals': len(component_signals) + len(text_signals) + len(overlay_signals),
        'text_preview': text_values[:5],
    }


def analyze_source(html_path: Path, width_px: float = 1440, height_px: float = 810) -> Dict[str, Any]:
    """Stage 1: collect source snapshot and raw descriptive signals."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'lxml')
    export_context = collect_export_context(html_path, soup)
    hints = export_context.get('hints') or {}
    contract = export_context.get('contract')

    chrome_selectors = hints.get('chrome_selectors') or []
    if chrome_selectors:
        _prune_runtime_chrome(soup, chrome_selectors)

    css_rules = extract_css_from_soup(soup)
    slide_roots = discover_slide_roots(soup)
    detection = export_context.get('detection') or {}
    producer_signals = (
        len(detection.get('strong_signals') or [])
        + len(detection.get('medium_channels') or [])
        + len(detection.get('weak_signals') or [])
    )
    semantic_signal_labels = _collect_semantic_deck_signals(slide_roots)

    raw_deck_signals = {
        'producer': detection.get('producer') or hints.get('producer'),
        'producer_confidence': detection.get('confidence', 'none'),
        'contract_found': bool(contract),
        'producer_signals': producer_signals,
        'page_boundary_count': len(slide_roots),
        'semantic_signals': len(semantic_signal_labels),
        'semantic_signal_labels': semantic_signal_labels,
    }
    raw_slide_signals = [
        _collect_slide_raw_signals(slide_html, index, css_rules, contract)
        for index, slide_html in enumerate(slide_roots)
    ]

    source_snapshot = {
        'html_path': html_path,
        'width_px': width_px,
        'height_px': height_px,
        'html_content': html_content,
        'soup': soup,
        'css_rules': css_rules,
        'slide_roots': slide_roots,
        'export_context': export_context,
        'hints': hints,
        'contract': contract,
    }

    return {
        'source_snapshot': source_snapshot,
        'raw_deck_signals': raw_deck_signals,
        'raw_slide_signals': raw_slide_signals,
    }


def _support_tier_rank(support_tier: str) -> int:
    order = {
        'generic_safe': 0,
        'semantic_enhanced': 1,
        'producer_aware': 2,
        'contract_bound': 3,
    }
    return order.get(support_tier, 0)


def _cap_support_tier(local_tier: str, deck_tier: str) -> str:
    return local_tier if _support_tier_rank(local_tier) <= _support_tier_rank(deck_tier) else deck_tier


def _assign_slide_support_tier(raw_slide: Dict[str, Any]) -> str:
    if raw_slide.get('has_local_contract_evidence'):
        return 'contract_bound'
    if raw_slide.get('semantic_signals', 0) >= 2 and raw_slide.get('text_count', 0) > 0:
        return 'semantic_enhanced'
    return 'generic_safe'


def build_profiles(analysis: Dict[str, Any]) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """Stage 2: derive descriptive deck/slide profiles from raw signals."""
    source_snapshot = analysis.get('source_snapshot') or {}
    export_context = source_snapshot.get('export_context') or {}
    hints = source_snapshot.get('hints') or {}
    contract = source_snapshot.get('contract')
    raw_deck = analysis.get('raw_deck_signals') or {}
    raw_slide_signals = analysis.get('raw_slide_signals') or []

    support_tier = _assign_support_tier(raw_deck)
    deck_profile = {
        'producer': raw_deck.get('producer'),
        'producer_confidence': raw_deck.get('producer_confidence', 'none'),
        'support_tier': support_tier,
        'preset': hints.get('preset', ''),
        'deck_family': hints.get('deck_family', ''),
        'contract': contract,
        'global_downgrade_chain': _build_global_downgrade_chain(),
        'validation': export_context.get('validation'),
    }

    slide_profiles: List[Dict[str, Any]] = []
    for raw_slide in raw_slide_signals:
        override_candidates = []
        if raw_slide.get('role'):
            override_candidates.append({'type': 'role', 'value': raw_slide['role']})
        if raw_slide.get('intent'):
            override_candidates.append({'type': 'intent', 'value': raw_slide['intent']})
        slide_support_tier = _cap_support_tier(_assign_slide_support_tier(raw_slide), support_tier)

        slide_profiles.append({
            'slide_index': raw_slide.get('slide_index', 0),
            'role': raw_slide.get('role', ''),
            'intent': raw_slide.get('intent', ''),
            'support_tier': slide_support_tier,
            'component_profiles': list(raw_slide.get('component_signals') or []),
            'text_profiles': list(raw_slide.get('text_signals') or []),
            'overlay_profiles': list(raw_slide.get('overlay_signals') or []),
            'override_candidates': override_candidates,
        })

    return deck_profile, slide_profiles


def _describe_override_candidate(candidate: Any) -> str:
    if isinstance(candidate, dict):
        candidate_type = str(candidate.get('type', '')).strip()
        candidate_value = str(candidate.get('value', '')).strip()
        if candidate_type and candidate_value:
            return f'{candidate_type}:{candidate_value}'
        if candidate_value:
            return candidate_value
        if candidate_type:
            return candidate_type
    if candidate is None:
        return ''
    return str(candidate).strip()


def _build_text_policy_bundle(deck_profile: Dict[str, Any], slide_profile: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'deck_support_tier': deck_profile.get('support_tier', 'generic_safe'),
        'slide_support_tier': slide_profile.get('support_tier', 'generic_safe'),
        'text_profiles': list(slide_profile.get('text_profiles') or []),
        'policy_mode': 'freeze_major_text_groups',
    }


def _clone_override_candidates(override_candidates: List[Any]) -> List[Any]:
    cloned_candidates: List[Any] = []
    for candidate in override_candidates or []:
        cloned_candidates.append(dict(candidate) if isinstance(candidate, dict) else candidate)
    return cloned_candidates


def plan_slides(
    deck_profile: Dict[str, Any],
    slide_profiles: List[Dict[str, Any]],
    width_px: float,
    height_px: float,
) -> List[Dict[str, Any]]:
    """Stage 3: choose solver and planning policies without emitting geometry."""
    _ = (width_px, height_px)
    deck_support_tier = deck_profile.get('support_tier', 'generic_safe')
    deck_family = str(deck_profile.get('deck_family', '')).strip()
    global_downgrade_chain = list(deck_profile.get('global_downgrade_chain') or [])
    slide_plans: List[Dict[str, Any]] = []

    for slide_profile in slide_profiles:
        support_tier = _cap_support_tier(slide_profile.get('support_tier', 'generic_safe'), deck_support_tier)
        role = str(slide_profile.get('role', '')).strip()
        selected_layout_family = deck_family
        downgrade_chain = list(global_downgrade_chain)
        allowed_overrides = _clone_override_candidates(slide_profile.get('override_candidates') or [])

        if support_tier == 'contract_bound' and role:
            selected_solver = 'contract_role'
        elif support_tier == 'producer_aware':
            selected_solver = 'producer_flow'
        elif support_tier == 'semantic_enhanced':
            selected_solver = 'semantic_flow'
        else:
            selected_solver = 'generic_flow'

        reasons = [f'support_tier:{support_tier}', f'solver:{selected_solver}']
        if selected_layout_family:
            reasons.append(f'layout_family:{selected_layout_family}')
        if role:
            reasons.append(f'role:{role}')
        for candidate in allowed_overrides:
            normalized_candidate = _describe_override_candidate(candidate)
            if normalized_candidate:
                reasons.append(f'override_allowed:{normalized_candidate}')
        for downgrade in downgrade_chain:
            reasons.append(f'downgrade_allowed:{downgrade}')

        slide_plans.append({
            'slide_index': slide_profile.get('slide_index', 0),
            'support_tier': support_tier,
            'selected_solver': selected_solver,
            'selected_layout_family': selected_layout_family,
            'selected_component_plans': list(slide_profile.get('component_profiles') or []),
            'text_policy_bundle': _build_text_policy_bundle(deck_profile, slide_profile),
            'background_strategy': 'source_background',
            'overlay_strategy': 'source_overlays',
            'allowed_overrides': allowed_overrides,
            'downgrade_chain': downgrade_chain,
            'confidence': slide_profile.get('confidence', 'medium'),
            'reasons': reasons,
        })

    return slide_plans


def build_export_pipeline(
    html_path: Path,
    width_px: float = 1440,
    height_px: float = 900,
) -> Dict[str, Any]:
    analysis = analyze_source(html_path, width_px, height_px)
    deck_profile, slide_profiles = build_profiles(analysis)
    slide_plans = plan_slides(deck_profile, slide_profiles, width_px, height_px)
    return {
        'analysis': analysis,
        'deck_profile': deck_profile,
        'slide_profiles': slide_profiles,
        'slide_plans': slide_plans,
    }


def _derive_pptx_text_render_hint(element: Dict[str, Any]) -> Dict[str, Any]:
    if element.get('type') != 'text':
        return {}

    bounds = element.get('bounds', {})
    styles = element.get('styles', {})
    segments = element.get('segments', [])
    font_size_pt = px_to_pt(styles.get('fontSize', '16px'))
    font_size_px = parse_px(styles.get('fontSize', '16px'))
    if font_size_px <= 0:
        font_size_px = 16.0

    if not segments:
        raw = (element.get('text', '') or '').strip()
        segments = [{'text': raw, 'color': styles.get('color', '')}]

    lines = segments_to_lines(segments)
    if not lines:
        lines = [[{'text': '', 'color': styles.get('color', '')}]]

    explicit_break_heading = (
        element.get('tag') in ('h1', 'h2', 'h3') and
        '\n' in (element.get('text', '') or '') and
        font_size_pt >= 28
    )
    preserve_authored_breaks = bool(element.get('preserveAuthoredBreaks'))
    prefer_wrap_to_preserve_size = bool(element.get('preferWrapToPreserveSize'))
    display_heading_like = (
        (
            element.get('tag') in ('h1', 'h2', 'h3') or
            element.get('_text_contract_role') == 'title'
        ) and
        font_size_pt >= 20 and
        len(lines) <= 1
    )
    display_metric_like = (
        len(lines) <= 1 and
        font_size_pt >= 18 and
        _looks_like_metric_token((element.get('text', '') or '').strip())
    )
    single_line_contract_heading = (
        prefer_wrap_to_preserve_size and
        display_heading_like and
        font_size_pt >= 28 and
        '\n' not in (element.get('text', '') or '') and
        _can_preserve_single_line_contract_heading(
            element,
            font_size_px,
            bounds.get('width', 0.0),
            letter_spacing=styles.get('letterSpacing', ''),
        )
    )
    effective_h = max(bounds.get('height', 0.0), element.get('naturalHeight', bounds.get('height', 0.0)))
    inferred_multiline_prose = (
        element.get('tag') in ('p', 'div') and
        not element.get('forceSingleLine') and
        not element.get('preferNoWrapFit') and
        '\n' not in (element.get('text', '') or '') and
        effective_h > _estimate_line_height_in(styles, font_size_pt) * 1.35
    )

    raw_text = element.get('text', '') or ''
    wrap_mode = 'square'
    auto_size = 'shape_to_fit_text'
    decision = 'multiline_default'
    if explicit_break_heading:
        wrap_mode = 'none'
        auto_size = 'text_to_fit_shape'
        decision = 'explicit_break_heading'
    elif single_line_contract_heading:
        wrap_mode = 'none'
        auto_size = 'shape_to_fit_text'
        decision = 'single_line_contract_heading'
    elif prefer_wrap_to_preserve_size:
        wrap_mode = 'square'
        auto_size = 'shape_to_fit_text'
        decision = 'prefer_wrap_to_preserve_size'
    elif preserve_authored_breaks:
        wrap_mode = 'none'
        auto_size = 'shape_to_fit_text'
        decision = 'preserve_authored_breaks'
    elif display_heading_like or display_metric_like:
        wrap_mode = 'none'
        auto_size = 'shape_to_fit_text'
        decision = 'display_heading_or_metric'
    elif element.get('forceSingleLine'):
        wrap_mode = 'none'
        auto_size = 'text_to_fit_shape'
        decision = 'force_single_line'
    elif element.get('preferNoWrapFit'):
        wrap_mode = 'none'
        auto_size = 'text_to_fit_shape'
        decision = 'prefer_no_wrap_fit'
    elif inferred_multiline_prose:
        wrap_mode = 'square'
        auto_size = 'shape_to_fit_text'
        decision = 'inferred_multiline_prose'
    elif len(lines) <= 1:
        needs_wrap = len(raw_text) > 20 and bounds.get('width', 0.0) < 5.0
        if needs_wrap:
            wrap_mode = 'square'
            auto_size = 'shape_to_fit_text'
            decision = 'single_line_needs_wrap'
        else:
            wrap_mode = 'none'
            auto_size = 'text_to_fit_shape'
            decision = 'single_line_fit'

    return {
        'wrap_mode': wrap_mode,
        'auto_size': auto_size,
        'decision': decision,
        'preserve_authored_breaks': preserve_authored_breaks,
        'prefer_wrap_to_preserve_size': prefer_wrap_to_preserve_size,
        'force_single_line': bool(element.get('forceSingleLine')),
        'prefer_no_wrap_fit': bool(element.get('preferNoWrapFit')),
    }


def _build_pptx_render_hints(elements: List[Dict[str, Any]], slide_index: int) -> Dict[str, Any]:
    text_hints: Dict[str, Dict[str, Any]] = {}
    text_counter = 0

    def _visit(node_list: List[Dict[str, Any]]) -> None:
        nonlocal text_counter
        for element in node_list:
            if element.get('type') == 'text':
                stable_id = f'slide{slide_index}-text-{text_counter}'
                text_counter += 1
                element['geometry_id'] = stable_id
                hint = _derive_pptx_text_render_hint(element)
                if hint:
                    hint = dict(hint)
                    hint['geometry_id'] = stable_id
                    element['pptxRenderHint'] = hint
                    text_hints[stable_id] = hint
            children = element.get('children') or []
            if children:
                _visit(children)

    _visit(elements)
    return {'text': text_hints}


def _solve_single_slide_geometry(
    slide_plan: Dict[str, Any],
    slide_html: Tag,
    source_snapshot: Dict[str, Any],
    deck_profile: Dict[str, Any],
    body_style: Dict[str, Any],
    body_grid_bg: Optional[Dict[str, Any]],
    body_mesh_bg: Optional[Dict[str, Any]],
    body_mesh_solid: Optional[Tuple[int, int, int]],
    global_overlays: List[Dict[str, Any]],
) -> Dict[str, Any]:
    width_px = source_snapshot['width_px']
    height_px = source_snapshot['height_px']
    css_rules = source_snapshot['css_rules']
    hints = source_snapshot['hints']
    contract = source_snapshot['contract']
    background_strategy = slide_plan.get('background_strategy', 'source_background')
    overlay_strategy = slide_plan.get('overlay_strategy', 'source_overlays')

    content_root, layout_info, slide_overlay_nodes = _prepare_slide_content_root(slide_html, css_rules, contract)
    slide_style = _effective_slide_layout_style(
        slide_html,
        css_rules,
        compute_element_style(slide_html, css_rules, slide_html.get('style', '')),
        contract,
    )

    background_solid = None
    background_gradient = None
    grid_bg = None
    mesh_bg = None
    if background_strategy == 'source_background':
        bg_info = extract_slide_background(slide_html, css_rules)
        background_solid = bg_info['solid']
        background_gradient = bg_info['gradient']
        grid_bg = bg_info['grid'] or body_grid_bg
        mesh_bg = body_mesh_bg

        if not background_solid and not background_gradient:
            if body_mesh_solid:
                background_solid = body_mesh_solid
            else:
                body_rgb = parse_color(body_style.get('backgroundColor', ''))
                if body_rgb:
                    background_solid = body_rgb

    has_own_chrome = bool(
        slide_html.select('.nav-dots') or
        slide_html.select('.slide-counter') or
        slide_html.select('.page-counter')
    )

    content_mw = None
    cr_style = compute_element_style(content_root, css_rules, content_root.get('style', ''))
    cr_maxw = cr_style.get('maxWidth', '')
    if cr_maxw and 'px' in cr_maxw:
        content_mw = parse_px(cr_maxw)

    if content_mw is None and content_root is slide_html:
        for child in content_root.children:
            if not isinstance(child, Tag):
                continue
            child_style = compute_element_style(child, css_rules, child.get('style', ''))
            if child_style.get('position', '') == 'absolute':
                continue
            child_maxw = child_style.get('maxWidth', '')
            if child_maxw and 'px' in child_maxw:
                content_mw = parse_px(child_maxw)
                break

    custom_elements = _build_swiss_role_elements(
        content_root,
        css_rules,
        width_px,
        height_px,
        contract,
        layout_info,
    )
    if custom_elements is not None:
        elements = custom_elements
    else:
        elements = flat_extract(
            content_root,
            css_rules,
            body_style,
            slide_width_px=width_px,
            content_width_px=content_mw,
            contract=contract,
        )

    slide_overlays: List[Dict[str, Any]] = []
    if overlay_strategy == 'source_overlays':
        for overlay_node in slide_overlay_nodes:
            slide_overlays.extend(
                flat_extract(
                    overlay_node,
                    css_rules,
                    slide_style,
                    slide_width_px=width_px,
                    contract=contract,
                )
            )

    if (
        content_root.name == slide_html.name and
        _is_slide_root_element(content_root)
    ):
        elements = [e for e in elements if not (
            e.get('type') == 'shape' and
            e.get('tag') == content_root.name and
            (
                e.get('styles', {}).get('backgroundImage', '') or
                e.get('styles', {}).get('backgroundColor', '')
            )
        )]
    if slide_overlays:
        elements = slide_overlays + elements
    if overlay_strategy == 'source_overlays' and global_overlays:
        elements = [copy.deepcopy(overlay) for overlay in global_overlays] + elements
    _apply_explicit_positions(elements)

    slide_index = int(slide_plan.get('slide_index', 0))
    title = get_text_content(slide_html)[:50]
    print(f"  [{slide_index + 1}/{len(source_snapshot['slide_roots'])}] {title}... ({len(elements)} elements)")
    pptx_render_hints = _build_pptx_render_hints(elements, slide_index)
    background_payload = {
        'strategy': background_strategy,
        'solid': background_solid,
        'gradient': background_gradient,
        'grid': grid_bg,
        'mesh': mesh_bg,
    }

    legacy_slide_data = {
        'background': background_solid,
        'bgGradient': background_gradient,
        'gridBg': grid_bg,
        'meshBg': mesh_bg,
        'elements': elements,
        'hasOwnChrome': has_own_chrome,
        'contentMaxWidthPx': content_mw,
        'legacyBlueSkyOffsets': 'blue-sky' in Path(source_snapshot['html_path']).stem,
        'producer': deck_profile.get('producer'),
        'producerConfidence': deck_profile.get('producer_confidence'),
        'exportHints': hints,
        'contractId': contract.get('contract_id') if contract else None,
        'exportRole': slide_html.get('data-export-role', '') or layout_info.get('role', ''),
        'exportSupportTier': layout_info.get('support_tier', ''),
        'exportIntent': slide_html.get('data-export-intent', ''),
        'slideStyle': slide_style,
    }

    return {
        'slide_index': slide_index,
        'source_html_path': str(source_snapshot['html_path']),
        'slide_size': {
            'width_px': width_px,
            'height_px': height_px,
            'width_in': SLIDE_W_IN,
            'height_in': SLIDE_H_IN,
        },
        'selected_solver': slide_plan.get('selected_solver'),
        'selected_layout_family': slide_plan.get('selected_layout_family'),
        'text_policy_bundle': copy.deepcopy(slide_plan.get('text_policy_bundle') or {}),
        'background_strategy': background_strategy,
        'overlay_strategy': overlay_strategy,
        'allowed_overrides': copy.deepcopy(slide_plan.get('allowed_overrides') or []),
        'downgrade_chain': list(slide_plan.get('downgrade_chain') or []),
        'reasons': list(slide_plan.get('reasons') or []),
        'confidence': slide_plan.get('confidence'),
        'background': background_payload,
        'bgGradient': background_gradient,
        'gridBg': grid_bg,
        'meshBg': mesh_bg,
        'elements': elements,
        'pptx_render_hints': pptx_render_hints,
        'legacy_slide_data': legacy_slide_data,
    }


def solve_geometry(pipeline: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Stage 4: extract render-ready per-slide geometry plans from the export pipeline."""
    analysis = pipeline['analysis']
    deck_profile = pipeline['deck_profile']
    slide_plans = pipeline['slide_plans']
    source_snapshot = analysis['source_snapshot']
    soup = source_snapshot['soup']
    css_rules = source_snapshot['css_rules']
    contract = source_snapshot['contract']

    body_style_str = ''
    body_tag = soup.find('body')
    if body_tag and body_tag.get('style'):
        body_style_str = body_tag['style']
    body_style = compute_element_style(body_tag or Tag(name='body'), css_rules, body_style_str)
    body_grid_bg = extract_body_decorative_background(css_rules, contract)
    body_mesh_bg = extract_body_mesh_background(body_style, contract)
    body_mesh_solid = _approximate_aurora_mesh_solid_color(body_mesh_bg)
    global_overlays = _collect_global_positioned_overlays(
        soup,
        css_rules,
        body_style,
        source_snapshot['width_px'],
        contract,
    )

    body_bi = body_style.get('backgroundImage', '')
    if body_bi and 'gradient' in body_bi:
        stops = re.findall(r'rgba?\([^)]+\)', body_bi)
        if len(stops) >= 2:
            c1 = parse_color(stops[0])
            c2 = parse_color(stops[-1])
            if c1 and c2:
                css_rules.insert(0, CSSRule(selector='body', properties={
                    'backgroundImage': body_bi
                }))

    slides_html = source_snapshot['slide_roots']
    if not slides_html:
        print("No slide roots found in HTML.")
        return []

    print(f"  Found {len(slides_html)} slides. Parsing...")

    geometry_plans: List[Dict[str, Any]] = []
    for slide_plan in slide_plans:
        slide_index = int(slide_plan.get('slide_index', 0))
        if slide_index < 0 or slide_index >= len(slides_html):
            continue
        geometry_plans.append(
            _solve_single_slide_geometry(
                slide_plan,
                slides_html[slide_index],
                source_snapshot,
                deck_profile,
                body_style,
                body_grid_bg,
                body_mesh_bg,
                body_mesh_solid,
                global_overlays,
            )
        )
    return geometry_plans


def parse_html_to_slides(html_path: Path, width_px: float = 1440, height_px: float = 810) -> List[Dict]:
    """Parse an HTML file into a list of slide data dicts."""
    pipeline = build_export_pipeline(html_path, width_px, height_px)
    geometry_plans = solve_geometry(pipeline)
    return [plan['legacy_slide_data'] for plan in geometry_plans]


# ─── Layout Pass ──────────────────────────────────────────────────────────────

def layout_slide_elements(elements: List[Dict], slide_width_in: float = 13.33, slide_height_in: float = 900/108, slide_style: Optional[Dict[str, str]] = None, slide_data: Optional[Dict] = None):
    """
    Simulate flex-column layout: stack elements vertically with padding.
    Handles container elements (grid/flex) by positioning them and adjusting children.
    Supports text-align: center for centered layouts and max-width constraints.
    Supports vertical centering when slide has justifyContent: center.
    """
    # Pre-mark pill text elements as _skip_layout (pill shapes already have this flag)
    # Don't skip - let them participate in layout. The pill marginBottom
    # naturally creates the gap before the title.

    # Derive internal_margin from CSS padding (slide element's paddingTop)
    # Golden starts content at y ≈ 2.15" for slides with clamp-based padding
    default_margin = 0.5
    slide_pad_top = default_margin
    slide_pad_bottom = default_margin
    if slide_style:
        pt = slide_style.get('paddingTop', '')
        if pt:
            pt_px = parse_px(pt)
            pt_in = pt_px / PX_PER_IN
            if pt_in > 0:
                default_margin = pt_in
                slide_pad_top = pt_in
        pb = slide_style.get('paddingBottom', '')
        if pb:
            pb_px = parse_px(pb)
            pb_in = pb_px / PX_PER_IN
            if pb_in > 0:
                slide_pad_bottom = pb_in
        else:
            slide_pad_bottom = slide_pad_top
    internal_margin = default_margin
    current_y = internal_margin
    slide_margin = internal_margin

    # Propagate slide-level textAlign to all elements (e.g., chapter slides have
    # text-align:center on the slide element, inherited by children)
    if slide_style:
        slide_ta = slide_style.get('textAlign', slide_style.get('text-align', ''))
        if slide_ta:
            for elem in elements:
                elem_s = elem.get('styles', {})
                if not elem_s.get('textAlign', ''):
                    elem_s['textAlign'] = slide_ta

    available_content_width = slide_width_in - 2 * internal_margin
    center_slide_content = False
    if slide_style:
        slide_ta = slide_style.get('textAlign', slide_style.get('text-align', ''))
        slide_ai = slide_style.get('alignItems', slide_style.get('align-items', ''))
        center_slide_content = slide_ta == 'center' or slide_ai == 'center'

    # Detect content width: prefer parser-provided content max-width hints, then
    # fall back to local element constraints, then finally the widest text element.
    max_constraint = None
    if slide_data:
        hinted_max_px = slide_data.get('contentMaxWidthPx')
        if hinted_max_px:
            max_constraint = hinted_max_px / PX_PER_IN

    # First, find maxWidth constraint on exported elements if no slide-level hint exists.
    for elem in elements:
        if max_constraint is not None:
            break
        s = elem.get('styles', {})
        mw = s.get('maxWidth', '')
        if mw and 'px' in mw:
            mw_in = parse_px(mw) / PX_PER_IN
            max_constraint = mw_in
            break

    # Find the widest text element's width
    max_text_width = 0.0
    for elem in elements:
        if elem.get('type') == 'text' and not elem.get('_skip_layout'):
            b = elem['bounds']
            if b['width'] > max_text_width:
                max_text_width = b['width']

    # Text-only heuristics under-estimate centered content pages that anchor the
    # real layout around a wider wrapper container (e.g. theme pill rails,
    # split-layout shells, CTA KPI wrappers). Consider those structural blocks
    # when deriving the authored content area width.
    max_structural_width = 0.0
    for elem in elements:
        if elem.get('_skip_layout'):
            continue
        if elem.get('type') not in ('container', 'table', 'presentation_rows', 'image'):
            continue
        b = elem.get('bounds', {})
        elem_w = b.get('width', 0.0)
        if elem_w <= 0:
            continue
        if elem_w >= available_content_width - 0.35:
            max_structural_width = max(max_structural_width, available_content_width)
            continue
        if elem_w > available_content_width + 0.35:
            continue
        if elem.get('type') == 'container':
            if not (elem.get('_children_relative') or elem.get('layout') == 'flow_box'):
                continue
        max_structural_width = max(max_structural_width, elem_w)

    # When there's an explicit maxWidth constraint, use it for the content area —
    # individual text elements will be shrink-wrapped to their natural text width
    # during the text layout pass. The constraint defines the left margin.
    if max_constraint is not None:
        content_area_width = max_constraint  # always use explicit constraint for margins
    elif max_text_width > 0 or max_structural_width > 0:
        content_area_width = max(max_text_width, max_structural_width)
    else:
        content_area_width = None

    if (
        center_slide_content and
        content_area_width is not None and
        content_area_width < available_content_width
    ):
        slide_margin = (slide_width_in - content_area_width) / 2


    max_width = slide_width_in - 2 * slide_margin

    # Pre-compute which shapes are paired with text — they shouldn't advance current_y
    # The paired text element will position both
    paired_shapes = set()
    for elem in elements:
        if elem.get('_pair_with') and elem.get('type') == 'shape':
            paired_shapes.add(id(elem))

    card_groups: Dict[str, Dict[str, float]] = {}
    active_card_group: Optional[str] = None
    pair_shapes_by_id: Dict[str, Dict[str, Any]] = {}
    for elem in elements:
        pair_id = elem.get('_pair_with')
        if pair_id and elem.get('type') == 'shape':
            pair_shapes_by_id[pair_id] = elem

    def accent_callout_gap_floor(flow_elem: Optional[Dict[str, Any]]) -> float:
        if not flow_elem:
            return 0.0
        pair_id = flow_elem.get('_pair_with')
        if not pair_id:
            return 0.0
        pair_shape = pair_shapes_by_id.get(pair_id)
        if not pair_shape:
            return 0.0
        border_left = pair_shape.get('styles', {}).get('borderLeft', '')
        if not (border_left and '4px' in border_left and 'solid' in border_left):
            return 0.0
        return 18.0 / PX_PER_IN

    def paired_callout_gap_floor(flow_elem: Optional[Dict[str, Any]]) -> float:
        if not flow_elem:
            return 0.0
        pair_id = flow_elem.get('_pair_with')
        if not pair_id:
            return 0.0
        pair_shape = pair_shapes_by_id.get(pair_id)
        if not pair_shape:
            return 0.0

        pair_styles = pair_shape.get('styles', {})
        next_styles = flow_elem.get('styles', {})
        border_left = pair_styles.get('borderLeft', '')
        bg_color = pair_styles.get('backgroundColor', '')
        radius_px = parse_px(pair_styles.get('borderRadius', '0px'))
        is_compact_pair = (
            pair_shape.get('bounds', {}).get('height', 0.0) <= 0.9 and
            flow_elem.get('bounds', {}).get('height', 0.0) <= 0.7
        )
        looks_like_callout = (
            (border_left and '4px' in border_left and 'solid' in border_left) or
            (is_compact_pair and radius_px >= 10.0 and bool(bg_color))
        )
        if not looks_like_callout:
            return 0.0

        mt_px = max(
            parse_px(next_styles.get('marginTop', '')),
            parse_px(pair_styles.get('marginTop', '')),
        )
        return max(24.0, mt_px + 12.0) / PX_PER_IN

    def next_flow_elem(start_idx: int) -> Optional[Dict[str, Any]]:
        for cand in elements[start_idx + 1:]:
            if cand.get('_skip_layout'):
                continue
            if id(cand) in paired_shapes:
                continue
            if cand.get('_in_flow_box'):
                continue
            return cand
        return None

    def prev_flow_elem(start_idx: int) -> Optional[Dict[str, Any]]:
        for cand in reversed(elements[:start_idx]):
            if cand.get('_skip_layout'):
                continue
            if id(cand) in paired_shapes:
                continue
            if cand.get('_in_flow_box'):
                continue
            return cand
        return None

    def extend_card_group_height(group_id: Optional[str], elem: Dict[str, Any]) -> None:
        if not group_id or group_id not in card_groups:
            return
        if elem.get('_preserve_width'):
            return
        cg = card_groups[group_id]
        b = elem.get('bounds', {})
        used_h = max((b.get('y', 0.0) + b.get('height', 0.0)) - cg.get('y', 0.0), 0.0)
        cg['height'] = max(cg.get('height', 0.0), used_h + cg.get('pad_b', 0.0))
        shape_ref = cg.get('shape')
        if shape_ref:
            shape_ref['bounds']['height'] = cg['height']

    def flush_active_card_group(next_elem: Optional[Dict[str, Any]] = None):
        nonlocal current_y, active_card_group
        if not active_card_group:
            return
        cg = card_groups.get(active_card_group)
        if cg:
            gap = max(
                _flow_gap_in(cg.get('shape'), next_elem, 0.13),
                accent_callout_gap_floor(next_elem),
                paired_callout_gap_floor(next_elem),
            )
            current_y = max(current_y, cg.get('y', current_y) + cg.get('height', 0.0) + gap)
        active_card_group = None

    for i, elem in enumerate(elements):
        b = elem['bounds']
        s = elem.get('styles', {})
        elem_type = elem.get('type', '')
        elem_card_group = None if elem.get('_in_flow_box') else elem.get('_card_group')

        if active_card_group and elem_card_group != active_card_group:
            flush_active_card_group(elem)

        if elem.get('layoutDone'):
            if elem_type == 'container' and elem.get('_children_relative') and not elem.get('_layoutDoneShifted'):
                _shift_container_descendants(elem, b.get('x', 0.0), b.get('y', 0.0))
                elem['_layoutDoneShifted'] = True
            current_y = max(current_y, b['y'] + b['height'] + 0.13)
            continue

        # Handle container elements (grid/flex wrappers)
        if elem_type == 'container':
            b['y'] = current_y
            if b.get('width', 0) > 0 and b['width'] < max_width:
                b['x'] = slide_margin + max((max_width - b['width']) / 2.0, 0.0)
            else:
                b['x'] = slide_margin
            # Adjust children's y positions, but x is already set by build_grid_children
            children_relative = elem.get('_children_relative', False)
            for child in elem.get('children', []):
                child['bounds']['y'] = current_y + child['bounds']['y']
                if child.get('type') == 'container' and child.get('_children_relative') and not children_relative:
                    _shift_container_descendants(
                        child,
                        child['bounds'].get('x', 0.0),
                        child['bounds'].get('y', 0.0),
                    )
                if children_relative:
                    child['bounds']['x'] = b['x'] + child['bounds']['x']
                    if child.get('_is_card_bg') or child.get('_is_border_left'):
                        child['bounds']['x'] = b['x']
                    if child.get('type') == 'container' and child.get('_children_relative'):
                        _shift_container_descendants(
                            child,
                            child['bounds'].get('x', 0.0),
                            child['bounds'].get('y', 0.0),
                        )
                # Don't adjust x for other children - build_grid_children already positioned correctly
            next_elem = next_flow_elem(i)
            gap = max(
                _flow_gap_in(elem, next_elem, 0.13),
                accent_callout_gap_floor(next_elem),
                paired_callout_gap_floor(next_elem),
            )
            current_y += b['height'] + gap
            continue

        # Skip elements marked for post-layout positioning (e.g., pill shapes/text)
        if elem.get('_skip_layout'):
            continue

        if elem_type == 'text':
            pair_shape = None if elem.get('_in_flow_box') else pair_shapes_by_id.get(elem.get('_pair_with', ''))
            pair_pad_t = pair_shape.get('_pair_pad_t', 0.0) if pair_shape else 0.0
            pair_pad_b = pair_shape.get('_pair_pad_b', 0.0) if pair_shape else 0.0
            b['y'] = current_y + pair_pad_t
        else:
            b['y'] = current_y
        text_align = s.get('textAlign', 'left')

        if elem_type == 'text':
            # Preserve pre-pass corrected height (from pre_pass_corrections)
            if elem.get('pptx_height_corrected'):
                pass  # Height already corrected, skip recalculation
            else:
                text = elem.get('text', '')
                existing_natural_h = elem.get('naturalHeight', b.get('height', 0.0))
                font_size_px = parse_px(elem.get('styles', {}).get('fontSize', '16px'))
                if font_size_px <= 0:
                    font_size_px = 16.0
                font_size_pt = font_size_px / PX_PER_IN * 72.0
                # Use element's own width (from build_text_element) for line wrapping
                # (max_width is the full slide content width, but the element may
                # have a narrower maxWidth constraint)
                wrap_width = b['width']
                if elem.get('forceSingleLine') and '\n' not in text:
                    line_count = 1
                elif elem.get('preserveAuthoredBreaks') and '\n' in text:
                    line_count = max(text.count('\n') + 1, 1)
                else:
                    line_count = estimate_wrapped_lines(text, font_size_pt, wrap_width) if text else 1
                # Use CSS lineHeight if available
                lh = s.get('lineHeight', '')
                if lh and 'px' in lh:
                    line_height_px = parse_px(lh)
                elif lh and lh.replace('.', '').isdigit():
                    line_height_px = font_size_px * float(lh)
                else:
                    line_height_px = font_size_px * _default_normal_line_height_multiple(elem.get('tag', ''))
                # For large display fonts (>= 48pt), use line-height-based height directly
                # (PPTX renders large text with minimal leading, matching CSS line-height)
                if font_size_pt >= 48:
                    computed_h = line_count * line_height_px / PX_PER_IN
                else:
                    computed_h = max(line_count * line_height_px / PX_PER_IN, font_size_pt / 72.0 * 1.0)
                if elem.get('forceSingleLine') or elem.get('preferContentWidth'):
                    b['height'] = max(computed_h, existing_natural_h)
                else:
                    b['height'] = computed_h
                # Update naturalHeight to match layout-calculated height
                # (export_text_element uses max of bounds height and naturalHeight)
                elem['naturalHeight'] = b['height']

            # Add CSS vertical padding to height
            # Skip if pre-pass already corrected the height (includes padding adjustment)
            if not elem.get('pptx_height_corrected'):
                pad_t = parse_px(s.get('paddingTop', ''))
                pad_b = parse_px(s.get('paddingBottom', ''))
                if pad_t + pad_b > 0 and not (elem.get('forceSingleLine') or elem.get('preferContentWidth')):
                    b['height'] += (pad_t + pad_b) / PX_PER_IN

            # For list items, ensure minimum height matches rendered browser output
            # (golden shows ~0.76" for 18px list items with padding)
            if elem.get('tag') == 'li' and b['height'] < 0.7:
                b['height'] = 0.7

            # For inline-block elements, use the pre-computed width from build_text_element
            # (max-line-width) — don't overwrite with effective_w which is just maxWidth constraint
            is_inline_block = 'inline-block' in s.get('display', '')
            effective_w = _resolve_css_length_with_basis(s.get('width', ''), max_width * PX_PER_IN)
            if effective_w <= 0 and is_inline_block:
                effective_w = _resolve_css_length_with_basis(s.get('maxWidth', ''), max_width * PX_PER_IN)
            if (
                effective_w <= 0 and
                s.get('maxWidth', '') and
                (
                    elem.get('preserveAuthoredBreaks') or
                    elem.get('preferWrapToPreserveSize') or
                    elem.get('tag', '') in ('h1', 'h2')
                )
            ):
                effective_w = _resolve_css_length_with_basis(s.get('maxWidth', ''), max_width * PX_PER_IN)
            has_explicit_width = effective_w > 0 and effective_w < max_width * PX_PER_IN

            # Inline-block elements: check textAlign first
            if is_inline_block and text_align == 'center' and b['width'] < max_width * 0.8:
                # Centered inline-block: center within content area
                b['x'] = slide_margin + (max_width - b['width']) / 2
            elif is_inline_block and b['width'] < max_width * 0.8:
                # Trust the pre-computed width from build_text_element (max-line-width)
                # Don't overwrite with effective_w which is just maxWidth constraint
                b['x'] = slide_margin  # left-align within content area
            elif text_align == 'center' and text:
                # For multiline centered text, use the widest line's width
                # (golden centers each line independently, element sized to widest)
                max_line_width_px = 0.0
                max_line_display_width_px = 0.0
                for line in text.split('\n'):
                    line = line.strip()
                    if not line:
                        continue
                    line_w = _estimate_text_width_px(
                        line,
                        font_size_px * 0.96,
                        letter_spacing=s.get('letterSpacing', ''),
                    )
                    if line_w > max_line_width_px:
                        max_line_width_px = line_w
                    display_line_w = _estimate_text_width_px(
                        line,
                        font_size_px,
                        letter_spacing=s.get('letterSpacing', ''),
                    )
                    if display_line_w > max_line_display_width_px:
                        max_line_display_width_px = display_line_w
                text_width_in = max_line_width_px / PX_PER_IN
                display_text_width_in = max_line_display_width_px / PX_PER_IN
                if elem.get('_full_subtitle'):
                    # Full subtitle spans the full slide content width (like golden)
                    content_width = max_width
                elif elem.get('tag', '') in ('h1', 'h2'):
                    # For center-aligned headings, use CJK-only width
                    # (golden sizes headings to CJK character width, latin chars
                    # fit within due to narrower rendering)
                    total_cjk = sum(1 for c in text if ord(c) > 127)
                    if total_cjk > 0:
                        # For all-CJK or mostly-CJK headings, use 1.0x multiplier
                        # to match golden's heading width
                        cjk_width_px = total_cjk * font_size_px
                        content_width = min(cjk_width_px / PX_PER_IN, max_width)
                    else:
                        content_width = min(text_width_in, max_width)
                    if '\n' in text and font_size_pt >= 28:
                        # Preserve author-provided line breaks for display headings by
                        # giving PPT a small width safety margin. This avoids a machine-
                        # dependent third wrap on the last character of the explicit line.
                        heading_wrap_guard = min(max(font_size_px * 0.34 / PX_PER_IN, 0.18), 0.30)
                        mixed_script_guard = 0.0
                        if has_cjk(text) and has_latin_word(text):
                            mixed_script_guard = min(max(font_size_px * 0.10 / PX_PER_IN, 0.08), 0.16)
                        content_width = min(
                            max(content_width, display_text_width_in + heading_wrap_guard + mixed_script_guard),
                            max_width,
                        )
                else:
                    # For centered text: check if element has maxWidth and wrapped text.
                    # If so, use the full unwrapped text width (golden wraps text but
                    # keeps the element at full content width).
                    mw_px = parse_px(s.get('maxWidth', ''))
                    prefer_content_width = elem.get('preferContentWidth', False)
                    prefer_no_wrap_fit = elem.get('preferNoWrapFit', False)
                    inline_content_width = elem.get('inlineContentWidth', 0.0)
                    if mw_px > 0 and '\n' in text:
                        # Wrapped text with maxWidth: compute full unwrapped width
                        full_text = text.replace('\n', '')
                        full_cjk = sum(1 for c in full_text if ord(c) > 127)
                        full_latin = len(full_text) - full_cjk
                        full_px = full_cjk * font_size_px * 0.96 + full_latin * font_size_px * 0.55
                        content_width = min(full_px / PX_PER_IN, max_width)
                    elif prefer_no_wrap_fit and mw_px > 0:
                        content_width = min(max_width, max(b.get('width', 0.0), mw_px / PX_PER_IN))
                    elif prefer_content_width and inline_content_width > 0:
                        if elem.get('preferCenteredBlockWidth'):
                            # Centered command/footer rows look closer to native decks
                            # when the paragraph itself keeps a stable authored block
                            # width while the inline box overlay centers inside it.
                            content_width = min(max_width, max(inline_content_width + 0.8, 4.85))
                        else:
                            content_width = min(inline_content_width + 0.1, max_width)
                    elif text_width_in > 1.0:
                        # For center-aligned text inside a container with maxWidth,
                        # if the text is significantly narrower than max_width,
                        # the golden treats it as block-level filling the container
                        mw_px = parse_px(s.get('maxWidth', ''))
                        if text_align == 'center' and mw_px > 0 and text_width_in < max_width * 0.7 and not prefer_content_width:
                            content_width = max_width
                        else:
                            content_width = min(text_width_in, max_width)
                    else:
                        content_width = min(text_width_in * 1.3 + 1.0, max_width)
                b['width'] = content_width
                b['x'] = slide_margin + (max_width - content_width) / 2
            elif effective_w > 0 and effective_w < max_width * PX_PER_IN:
                # Element has explicit CSS width or maxWidth (inline-block)
                b['width'] = effective_w / PX_PER_IN
                b['x'] = slide_margin + (max_width - b['width']) / 2
            else:
                b['width'] = max_width
                b['x'] = slide_margin

            card_group = None if elem.get('_in_flow_box') else elem.get('_card_group')
            if card_group and card_group in card_groups:
                cg = card_groups[card_group]
                content_w = max(cg['width'] - cg['pad_l'] - cg['pad_r'] - cg['border_l'], 0.5)
                b['width'] = content_w
                b['x'] = cg['x'] + cg['pad_l'] + cg['border_l']
                b['y'] = cg.get('cursor_y', b['y'])
                mb = parse_px(s.get('marginBottom', '')) / PX_PER_IN
                inner_gap = mb if mb != 0 else 0.05
                cg['cursor_y'] = b['y'] + b['height'] + inner_gap
                active_card_group = card_group
                extend_card_group_height(card_group, elem)
            # Clamp all text widths to max_width to prevent overflow past slide edge
            if b['width'] > max_width:
                b['width'] = max_width
                b['x'] = slide_margin
        elif elem_type == 'shape':
            if elem.get('_preserve_width') and elem.get('_card_group') and not elem.get('_in_flow_box'):
                b['y'] = current_y
                b['x'] = slide_margin + (max_width - b['width']) / 2
                card_groups[elem['_card_group']] = {
                    'x': b['x'],
                    'y': b['y'],
                    'width': b['width'],
                    'height': b['height'],
                    'pad_l': elem.get('_css_pad_l', 0.0),
                    'pad_r': elem.get('_css_pad_r', 0.0),
                    'pad_b': elem.get('_css_pad_b', 0.0),
                    'border_l': elem.get('_css_border_l', 0.0),
                    'cursor_y': b['y'] + elem.get('_css_pad_t', 0.0),
                    'shape': elem,
                }
                active_card_group = elem['_card_group']
                continue
            # Paired shapes (from inline-block containers) already have correct width
            if elem.get('_pair_with') and not elem.get('_is_pill'):
                # Find paired text element to sync width
                paired_text = None
                for j in range(i + 1, min(i + 3, len(elements))):
                    next_elem = elements[j]
                    if next_elem.get('_pair_with') == elem.get('_pair_with'):
                        paired_text = next_elem
                        break

                if paired_text:
                    nb = paired_text['bounds']
                    # For elements with borderLeft accent (like .info bars), the golden
                    # renders the bg shape wider than text: max_width * 1.15
                    # This creates the characteristic full-width info bar style.
                    bl = elem.get('styles', {}).get('borderLeft', '')
                    # Only apply expanded width to shapes with a genuine border-left
                    # accent bar (4px+ solid), not thin borders from CSS `border` property
                    if bl and 'none' not in bl and '4px' in bl:
                        b['width'] = max_width * 1.15
                        b['x'] = slide_margin
                    else:
                        # Sync shape width to text width
                        b['width'] = nb['width']
                        b['x'] = slide_margin + (max_width - b['width']) / 2
                # Full-width separator shapes (from list items with border-bottom): use slide margin
                elif b['width'] >= max_width * 0.9:
                    b['x'] = slide_margin
                    b['width'] = max_width
                else:
                    # Keep pre-computed width, just center
                    b['x'] = slide_margin + (max_width - b['width']) / 2
            elif b['width'] > max_width * 0.5:
                # Check if next element is text at similar y-position (tag shape)
                for j in range(i + 1, min(i + 3, len(elements))):
                    next_elem = elements[j]
                    if next_elem.get('type') == 'text':
                        nb = next_elem['bounds']
                        if abs(nb['y'] - b['y']) < 0.1 and nb['width'] < max_width * 0.5:
                            # Tag-style shape: match text width
                            b['width'] = nb['width']
                            b['x'] = slide_margin + (max_width - b['width']) / 2
                            break
                else:
                    # No matching text found — use full width
                    b['width'] = max_width
                    b['x'] = slide_margin
            # else: keep pre-computed width but center on slide
            elif text_align == 'center' and b['width'] > 0 and b['width'] < max_width:
                b['x'] = slide_margin + (max_width - b['width']) / 2
            # Center small shapes with auto margins (like explicit centered dividers).
            elif s.get('marginLeft', '') == 'auto' and s.get('marginRight', '') == 'auto':
                b['x'] = slide_margin + (max_width - b['width']) / 2
            # Small shapes (dividers, decorative elements) without explicit positioning:
            # left-align within content area (like other block elements)
            elif b['width'] < max_width * 0.5:
                b['x'] = slide_margin
            # End of shape width adjustments
        elif elem_type in ('table', 'presentation_rows'):
            b['width'] = max_width
            b['x'] = slide_margin
            rows = elem.get('rows', [])
            b['height'] = max(sum(row.get('height', 0.264) for row in rows), 0.5)
        elif elem_type == 'image':
            if b['width'] > max_width:
                b['width'] = max_width
                b['height'] = b['width'] * 0.75
            b['x'] = slide_margin

        extend_card_group_height(elem_card_group, elem)

        # Paired shapes don't advance current_y — the paired text element positions both
        if id(elem) not in paired_shapes:
            if not elem.get('_in_flow_box') and elem.get('_card_group') and elem.get('_card_group') in card_groups:
                continue
            # Skip advancing current_y for full-slide background shapes —
            # they span the entire slide and shouldn't affect content flow
            if (elem_type == 'shape' and b['width'] > slide_width_in * 0.9
                    and b['height'] > slide_height_in * 0.9):
                continue
            # Apply marginBottom to adjust spacing to next element
            # Golden analysis: marginBottom REPLACES the base gap (0.13"), not adds to it.
            # The browser's layout already includes margins in the visual spacing.
            # When marginBottom is set, use it as the gap. When not set, use base gap.
            flow_h = b['height']
            if elem_type == 'text' and not elem.get('_in_flow_box'):
                pair_shape = pair_shapes_by_id.get(elem.get('_pair_with', ''))
                if pair_shape:
                    flow_h = max(flow_h + pair_shape.get('_pair_pad_t', 0.0) + pair_shape.get('_pair_pad_b', 0.0), flow_h)
            next_elem = next_flow_elem(i)
            gap = max(
                _flow_gap_in(elem, next_elem, 0.13),
                accent_callout_gap_floor(next_elem),
                paired_callout_gap_floor(next_elem),
            )
            current_y += flow_h + gap

    flush_active_card_group()

    # Post-layout sync: for shapes paired with text, copy text position to shape
    text_by_pair: Dict[str, Dict] = {}
    for elem in elements:
        pair_id = elem.get('_pair_with')
        if pair_id and elem.get('type') == 'text':
            text_by_pair[pair_id] = elem
    for elem in elements:
        pair_id = elem.get('_pair_with')
        if pair_id and elem.get('type') == 'shape' and pair_id in text_by_pair:
            text_elem = text_by_pair[pair_id]
            tb = text_elem['bounds']
            sb = elem['bounds']
            pad_l = elem.get('_pair_pad_l', 0.0)
            pad_r = elem.get('_pair_pad_r', 0.0)
            pad_t = elem.get('_pair_pad_t', 0.0)
            pad_b = elem.get('_pair_pad_b', 0.0)
            sb['x'] = tb['x'] - pad_l
            sb['y'] = tb['y'] - pad_t
            sb['height'] = tb['height'] + pad_t + pad_b
            # Skip width sync for borderLeft accent shapes (like .info bars) —
            # these have a pre-computed expanded width (max_width * 1.15) that
            # should NOT be overridden to match text width.
            bl = elem.get('styles', {}).get('borderLeft', '')
            if bl and 'none' not in bl and '4px' in bl:
                extra_h = (parse_px(elem.get('styles', {}).get('borderRadius', '')) + parse_px(bl)) / PX_PER_IN
                if extra_h > 0:
                    tb['height'] += extra_h
                    sb['height'] = tb['height']
                continue  # keep pre-computed width
            sb['width'] = tb['width'] + pad_l + pad_r

    # Generic slide-level vertical centering for slide roots that author with
    # flex-column + justify-content:center. This shifts the laid-out content
    # block as a whole, rather than leaving every deck anchored to top padding.
    justify = ''
    if slide_style:
        justify = slide_style.get('justifyContent', slide_style.get('justify-content', '')).strip()
    if justify in {'center', 'flex-end'}:
        center_candidates = []
        for elem in elements:
            b = elem.get('bounds', {})
            if not b:
                continue
            styles = elem.get('styles', {})
            if styles.get('display', '') == 'none':
                continue
            if elem.get('_skip_layout'):
                continue
            if elem.get('_is_decoration'):
                continue
            if (
                elem.get('type') in ('shape', 'image') and
                b.get('width', 0.0) > slide_width_in * 0.9 and
                b.get('height', 0.0) > slide_height_in * 0.9
            ):
                continue
            center_candidates.append(elem)

        if center_candidates:
            content_top = min(elem['bounds'].get('y', 0.0) for elem in center_candidates)
            content_bottom = max(
                elem['bounds'].get('y', 0.0) + elem['bounds'].get('height', 0.0)
                for elem in center_candidates
            )
            content_h = max(content_bottom - content_top, 0.0)
            available_h = max(slide_height_in - slide_pad_top - slide_pad_bottom, 0.0)
            if content_h > 0.0 and content_h < available_h - 1e-6:
                if justify == 'center':
                    target_top = slide_pad_top + max((available_h - content_h) / 2.0, 0.0)
                else:
                    target_top = max(slide_height_in - slide_pad_bottom - content_h, slide_pad_top)
                y_offset = target_top - content_top
                if abs(y_offset) > 1e-4:
                    for elem in center_candidates:
                        elem['bounds']['y'] = elem['bounds'].get('y', 0.0) + y_offset
                        if elem.get('type') == 'container' and elem.get('_children_relative'):
                            _translate_container_descendants(elem, 0.0, y_offset)

    # Golden-aligned content positioning: match golden PPTX content start Y.
    # Golden was manually designed with content anchored to y≈8.109" bottom.
    # Each slide type has a characteristic content_start_y that sandbox should match.
    # These values are extracted from demo/blue-sky-golden-native.pptx.
    GOLDEN_FIRST_Y = [2.294, 2.153, 2.085, 2.271, 2.926, 2.049, 2.149, 2.177, 1.986, 3.008]

    slide_idx = slide_data.get('_slide_index', -1) if slide_data else -1
    y_offset = 0.0
    if slide_data and slide_data.get('legacyBlueSkyOffsets') and 0 <= slide_idx < len(GOLDEN_FIRST_Y):
        golden_first = GOLDEN_FIRST_Y[slide_idx]
        # Find sandbox's first non-skip content element Y
        sandbox_first = slide_height_in
        for elem in elements:
            if elem.get('_skip_layout'):
                continue
            b = elem['bounds']
            # Skip nav dots at bottom (y > 7.5)
            if b['y'] > 7.5:
                continue
            if b['y'] < sandbox_first:
                sandbox_first = b['y']
        if sandbox_first < slide_height_in:
            y_offset = golden_first - sandbox_first
            # Apply offset to all non-skip elements
            for elem in elements:
                if elem.get('_skip_layout'):
                    continue
                b = elem['bounds']
                b['y'] += y_offset
                if elem.get('type') == 'container':
                    for child in elem.get('children', []):
                        child['bounds']['y'] += y_offset
                        if child.get('type') == 'container' and child.get('_children_relative'):
                            _shift_container_descendants(child, 0.0, y_offset)

    # Position inline tag pills AFTER vertical centering so stat items have final positions.
    # Pattern: pill shapes with _is_pill flag (no separate text elements).
    PILLS_GAP = 0.16  # gap between pills

    # Collect ALL pill shapes that are still at default position
    all_pills = []
    for elem in elements:
        if elem.get('type') == 'shape' and elem.get('_is_pill') and elem['bounds']['x'] == 0.50:
            all_pills.append(elem)

    if all_pills:
        # Find the FIRST non-pill content element's y position (pills are headers, placed above title)
        first_content_y = slide_height_in  # start with max possible
        lowest_y = 0.0
        for elem in elements:
            if elem.get('_skip_layout') or elem.get('_is_pill'):
                continue
            b = elem['bounds']
            if b['y'] < first_content_y:
                first_content_y = b['y']
            elem_bottom = b['y'] + b['height']
            if elem_bottom > lowest_y:
                lowest_y = elem_bottom
            # Also check container children (stat items)
            if elem.get('type') == 'container':
                for child in elem.get('children', []):
                    cb = child['bounds']
                    if cb['y'] < first_content_y:
                        first_content_y = cb['y']
                    child_bottom = cb['y'] + cb['height']
                    if child_bottom > lowest_y:
                        lowest_y = child_bottom

        # Place pills ABOVE the first content element with a small gap
        pill_h = all_pills[0]['bounds']['height']
        pill_y = first_content_y - pill_h - 0.16

        # Cap to not go too close to nav dots (y=7.22)
        pill_y = min(pill_y, slide_height_in - 0.60)

        # Position pills centered in full slide content area (matching golden)
        total_pill_w = sum(p['bounds']['width'] for p in all_pills) + PILLS_GAP * (len(all_pills) - 1)
        row_x = 1.57 + (10.18 - total_pill_w) / 2  # 10.18 = golden content area width
        for p in all_pills:
            p['bounds']['x'] = row_x
            p['bounds']['y'] = pill_y
            # Also position paired text element (if any)
            pair_id = p.get('_pair_with', '')
            if pair_id:
                for elem in elements:
                    if elem.get('_pair_with') == pair_id and elem.get('type') == 'text':
                        elem['bounds']['x'] = row_x
                        elem['bounds']['y'] = pill_y
                        elem['bounds']['width'] = p['bounds']['width']
                        elem['bounds']['height'] = p['bounds']['height']
                        break
            row_x += p['bounds']['width'] + PILLS_GAP

    # Position code background shapes AFTER vertical centering.
    # Code bg shapes are created as siblings of text elements and need to be
    # positioned at the text element's x + code text offset, y slightly above.
    # They can be at top-level OR inside container children.
    def position_code_bg_shapes(elems, depth=0):
        for elem in elems:
            if elem.get('_is_code_bg'):
                # Find the nearest sibling text that actually contains this code fragment.
                idx = elems.index(elem)
                code_text = None
                for child in elem.get('_code_element', []):
                    if isinstance(child, Tag):
                        code_text = child.get_text().strip()
                        break
                sibling_text = None
                fallback_text = None
                for direction in (1, -1):
                    start = idx + direction
                    stop = len(elems) if direction > 0 else -1
                    for j in range(start, stop, direction):
                        candidate = elems[j]
                        if candidate.get('type') != 'text':
                            continue
                        if fallback_text is None:
                            fallback_text = candidate
                        if code_text and code_text in candidate.get('text', ''):
                            sibling_text = candidate
                            break
                    if sibling_text:
                        break
                if not sibling_text:
                    sibling_text = fallback_text
            if elem.get('type') == 'shape' and elem.get('_is_code_bg') and elem['bounds']['x'] == 0:
                # Find the text element that actually contains this code fragment.
                idx = elems.index(elem)
                text_elem = None
                fallback_text = None
                code_text = None
                for child in elem.get('_code_element', []):
                    if isinstance(child, Tag):
                        code_text = child.get_text().strip()
                        break
                for direction in (1, -1):
                    start = idx + direction
                    stop = len(elems) if direction > 0 else -1
                    for j in range(start, stop, direction):
                        candidate = elems[j]
                        if candidate.get('type') != 'text':
                            continue
                        if fallback_text is None:
                            fallback_text = candidate
                        if code_text and code_text in candidate.get('text', ''):
                            text_elem = candidate
                            break
                    if text_elem:
                        break
                if not text_elem:
                    text_elem = fallback_text
                if text_elem:
                    tb = text_elem['bounds']
                    text_content = text_elem.get('text', '')
                    if code_text and code_text in text_content:
                        text_start = text_content.find(code_text)
                        prefix = text_content[:text_start]
                        font_px = parse_px(text_elem.get('styles', {}).get('fontSize', text_elem.get('font_size', '16px')))
                        if font_px <= 0:
                            font_px = 16.0
                        prefix_w = _estimate_text_width_px(
                            prefix,
                            font_px,
                            monospace=_uses_monospace_font(text_elem.get('styles', {}).get('fontFamily', '')),
                            letter_spacing=text_elem.get('styles', {}).get('letterSpacing', ''),
                        ) / PX_PER_IN
                        code_x = tb['x'] + prefix_w - elem.get('_code_pad_l', 0.0)
                        code_y = tb['y']
                        elem['bounds']['x'] = code_x
                        elem['bounds']['y'] = code_y
                    else:
                        elem['bounds']['x'] = tb['x']
                        elem['bounds']['y'] = tb['y']
            # Also check container children
            if elem.get('type') == 'container':
                position_code_bg_shapes(elem.get('children', []))

    position_code_bg_shapes(elements)


# ─── Pre-pass Corrections (from browser version) ─────────────────────────────

def pre_pass_corrections(elements: List[Dict]):
    """
    Pre-pass 1: Sync background shape height with adjacent text's naturalHeight.
    For shape+text pairs (same y-position), apply 1.3x PPTX correction for multi-line.

    Pre-pass 2: Push adjacent elements right of large single-line titles
    to prevent CJK overflow in PPTX.
    """
    # Flatten container children for correction processing
    flat = []
    for elem in elements:
        if elem.get('type') == 'container':
            flat.extend(elem.get('children', []))
        else:
            flat.append(elem)

    # Pre-pass 1: Shape+Text sync
    for i in range(len(flat) - 1):
        s, t = flat[i], flat[i + 1]
        if (s.get('type') == 'shape' and t.get('type') == 'text' and
            abs(s['bounds']['y'] - t['bounds']['y']) < 0.05 and
            abs(s['bounds']['height'] - t['bounds']['height']) < 0.05):
            nat = t.get('naturalHeight', t['bounds']['height'])
            base = max(nat, s['bounds']['height'])
            t_font_pt = px_to_pt(t['styles'].get('fontSize', '16px'))
            # Use CSS line-height if available, otherwise default 1.2
            t_lh = t['styles'].get('lineHeight', '')
            if t_lh and t_lh.replace('.', '').isdigit():
                t_line_multiplier = float(t_lh)
            else:
                t_line_multiplier = 1.2
            t_line_h = t_font_pt / 72.0 * t_line_multiplier
            # Subtract padding from base height for more accurate line estimation
            t_pad_t = parse_px(t['styles'].get('paddingTop', '0px')) / PX_PER_IN
            t_pad_b = parse_px(t['styles'].get('paddingBottom', '0px')) / PX_PER_IN
            t_text_h = base - t_pad_t - t_pad_b
            t_est_lines = t_text_h / max(t_line_h, 0.001) if t_text_h > 0 else 1
            if t_est_lines >= 2.0:
                corrected = base * PPTX_HEIGHT_FACTOR
                s['bounds']['height'] = corrected
                t['bounds']['height'] = corrected
                t['pptx_height_corrected'] = True
            elif nat > s['bounds']['height'] * 1.05:
                s['bounds']['height'] = nat
                t['bounds']['height'] = nat

    # Pre-pass 2: Adjacent element push for large titles
    for i in range(len(flat)):
        el = flat[i]
        if el.get('type') != 'text':
            continue
        fp = px_to_pt(el['styles'].get('fontSize', '16px'))
        if fp <= 24.0:
            continue
        lh = fp / 72.0 * 1.2
        est = el['bounds']['height'] / max(lh, 0.001)
        if est >= 2.0:
            continue
        orig_right = el['bounds']['x'] + el['bounds']['width']
        extra = el['bounds']['width'] * CJK_H_FACTOR
        for j in range(len(flat)):
            if j == i:
                continue
            other = flat[j]
            gap = other['bounds']['x'] - orig_right
            y_overlap = abs(other['bounds']['y'] - el['bounds']['y']) < el['bounds']['height']
            if 0 <= gap <= 0.3 and y_overlap:
                other['bounds']['x'] += extra


# ─── PPTX Rendering ───────────────────────────────────────────────────────────

_FONT_MAP = {
    'Inter':         ('Inter', 'Hiragino Sans GB'),
    'DM Sans':       ('Inter', 'Hiragino Sans GB'),
    'Space Grotesk': ('Helvetica Neue', 'Hiragino Sans GB'),
    'Clash Display': ('Helvetica Neue', 'Hiragino Sans GB'),
    'Satoshi':       ('Helvetica Neue', 'Hiragino Sans GB'),
    'Archivo Black': ('Helvetica Neue', 'Hiragino Sans GB'),
    'Archivo':       ('Helvetica Neue', 'Hiragino Sans GB'),
    'Nunito':        ('Helvetica Neue', 'Hiragino Sans GB'),
    'EB Garamond':   ('Baskerville', 'Songti SC'),
    'Noto Serif SC': ('Songti SC', 'Songti SC'),
    'Noto Serif CJK SC': ('Songti SC', 'Songti SC'),
    'Source Han Serif': ('Songti SC', 'Songti SC'),
    'Songti SC':     ('Songti SC', 'Songti SC'),
    'STSong':        ('Songti SC', 'Songti SC'),
    'Georgia':       ('Georgia', 'Songti SC'),
    'Baskerville':   ('Baskerville', 'Songti SC'),
    'Times New Roman': ('Times New Roman', 'Songti SC'),
    'serif':         ('Baskerville', 'Songti SC'),
    'Microsoft YaHei': ('Helvetica Neue', 'Hiragino Sans GB'),
    '微软雅黑':          ('Helvetica Neue', 'Hiragino Sans GB'),
    'PingFang SC':      ('Helvetica Neue', 'Hiragino Sans GB'),
    'Noto Sans SC':     ('Helvetica Neue', 'Hiragino Sans GB'),
    'Noto Sans CJK SC': ('Helvetica Neue', 'Hiragino Sans GB'),
    'Source Han Sans':  ('Helvetica Neue', 'Hiragino Sans GB'),
    'sans-serif':       ('Helvetica Neue', 'Hiragino Sans GB'),
    'system-ui':        ('Helvetica Neue', 'Hiragino Sans GB'),
    '-apple-system':    ('Helvetica Neue', 'Hiragino Sans GB'),
    'BlinkMacSystemFont': ('Helvetica Neue', 'Hiragino Sans GB'),
}
_DEFAULT_FONTS = ('Helvetica Neue', 'Hiragino Sans GB')
_DEFAULT_LATIN_FONTS = ('Inter', 'Inter')
_OFFICE_SAFE_FONT_KEYS = (
    'Noto Serif SC',
    'Noto Serif CJK SC',
    'Source Han Serif',
    'Songti SC',
    'STSong',
    'PingFang SC',
    'Noto Sans SC',
    'Noto Sans CJK SC',
    'Source Han Sans',
    'Microsoft YaHei',
    '微软雅黑',
)
_SERIF_CJK_FONT_KEYS = (
    'Noto Serif SC',
    'Noto Serif CJK SC',
    'Source Han Serif',
    'Songti SC',
    'STSong',
)
_SERIF_LATIN_FONT_KEYS = (
    'eb garamond',
    'crimson text',
    'baskerville',
    'georgia',
    'times new roman',
    'serif',
)
_LATIN_SAFE_FONT_KEYS = {
    'inter': ('Inter', 'Inter'),
    'dm sans': ('Inter', 'Inter'),
    'space grotesk': ('Helvetica Neue', 'Helvetica Neue'),
    'clash display': ('Helvetica Neue', 'Helvetica Neue'),
    'satoshi': ('Helvetica Neue', 'Helvetica Neue'),
    'archivo black': ('Helvetica Neue', 'Helvetica Neue'),
    'archivo': ('Helvetica Neue', 'Helvetica Neue'),
    'nunito': ('Helvetica Neue', 'Helvetica Neue'),
    'eb garamond': ('Baskerville', 'Baskerville'),
    'baskerville': ('Baskerville', 'Baskerville'),
    'georgia': ('Georgia', 'Georgia'),
    'times new roman': ('Times New Roman', 'Times New Roman'),
    'crimson text': ('Baskerville', 'Baskerville'),
    'serif': ('Baskerville', 'Baskerville'),
    'arial': ('Arial', 'Arial'),
    'helvetica': ('Helvetica Neue', 'Helvetica Neue'),
    'helvetica neue': ('Helvetica Neue', 'Helvetica Neue'),
    'segoe ui': ('Helvetica Neue', 'Helvetica Neue'),
    'sans-serif': ('Helvetica Neue', 'Helvetica Neue'),
    'system-ui': ('Helvetica Neue', 'Helvetica Neue'),
    '-apple-system': ('Helvetica Neue', 'Helvetica Neue'),
    'blinkmacsystemfont': ('Helvetica Neue', 'Helvetica Neue'),
    'sf pro': ('Helvetica Neue', 'Helvetica Neue'),
    'mono': ('Menlo', 'Menlo'),
    'menlo': ('Menlo', 'Menlo'),
    'monaco': ('Menlo', 'Menlo'),
    'consolas': ('Menlo', 'Menlo'),
    'courier new': ('Courier New', 'Courier New'),
}


def _stack_prefers_serif(candidates: List[str]) -> bool:
    for candidate in candidates:
        candidate_lc = candidate.lower()
        if candidate_lc in _SERIF_LATIN_FONT_KEYS:
            return True
        if any(candidate_lc == key.lower() for key in _SERIF_CJK_FONT_KEYS):
            return True
    return False


def _resolve_serif_mixed_script_fonts(candidates: List[str]) -> Tuple[str, str]:
    latin_choice = None
    ea_choice = None
    for candidate in candidates:
        candidate_lc = candidate.lower()
        if latin_choice is None and candidate_lc in _LATIN_SAFE_FONT_KEYS and candidate_lc in _SERIF_LATIN_FONT_KEYS:
            latin_choice = _LATIN_SAFE_FONT_KEYS[candidate_lc][0]
        if ea_choice is None:
            for css_name in _SERIF_CJK_FONT_KEYS:
                if candidate_lc == css_name.lower():
                    ea_choice = _FONT_MAP[css_name][1]
                    break
    latin_choice = latin_choice or 'Baskerville'
    ea_choice = ea_choice or 'Songti SC'
    return (latin_choice, ea_choice)


def map_font(css_font_family: str, text: str = ''):
    contains_cjk = bool(text) and has_cjk(text)
    if css_font_family:
        candidates = []
        for token in css_font_family.split(','):
            normalized = token.strip().strip('\'"')
            if normalized:
                candidates.append(normalized)
        latin_only = bool(text) and not contains_cjk
        mixed_script = bool(text) and contains_cjk and has_latin_word(text)
        if latin_only:
            for candidate in candidates:
                candidate_lc = candidate.lower()
                if candidate_lc in _LATIN_SAFE_FONT_KEYS:
                    return _LATIN_SAFE_FONT_KEYS[candidate_lc]
            for candidate in candidates:
                candidate_lc = candidate.lower()
                for css_name, fonts in _LATIN_SAFE_FONT_KEYS.items():
                    if css_name in candidate_lc:
                        return fonts
        if mixed_script and _stack_prefers_serif(candidates):
            return _resolve_serif_mixed_script_fonts(candidates)
        # Prefer stable Office-safe CJK fonts when a CSS stack mixes platform
        # fonts (e.g. PingFang / system-ui) with a later PPT-friendly fallback.
        for preferred in _OFFICE_SAFE_FONT_KEYS:
            preferred_lc = preferred.lower()
            if any(candidate.lower() == preferred_lc for candidate in candidates):
                fonts = _FONT_MAP[preferred]
                return (fonts[1], fonts[1]) if contains_cjk else fonts
        for candidate in candidates:
            candidate_lc = candidate.lower()
            for css_name, fonts in _FONT_MAP.items():
                if candidate_lc == css_name.lower():
                    return (fonts[1], fonts[1]) if contains_cjk else fonts
        for candidate in candidates:
            candidate_lc = candidate.lower()
            for css_name, fonts in _FONT_MAP.items():
                if css_name.lower() in candidate_lc:
                    return (fonts[1], fonts[1]) if contains_cjk else fonts
        if latin_only:
            return _DEFAULT_LATIN_FONTS
    if contains_cjk:
        return (_DEFAULT_FONTS[1], _DEFAULT_FONTS[1])
    return _DEFAULT_LATIN_FONTS if text and not contains_cjk else _DEFAULT_FONTS


def set_run_fonts(run, latin_font, ea_font):
    from lxml import etree
    NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    run.font.name = latin_font
    rPr = run._r.get_or_add_rPr()
    for tag, typeface in [('ea', ea_font), ('cs', ea_font)]:
        el = rPr.find(f'{{{NS}}}{tag}')
        if el is None:
            el = etree.SubElement(rPr, f'{{{NS}}}{tag}')
        el.set('typeface', typeface)


def set_letter_spacing(run, css_letter_spacing: str, font_size_pt: float = 0.0):
    if not css_letter_spacing or css_letter_spacing in ('normal', '0px'):
        return
    font_px = (font_size_pt / 72.0 * 96.0) if font_size_pt else 16.0
    px = _resolve_letter_spacing_px(css_letter_spacing, font_px)
    if px != 0:
        run._r.get_or_add_rPr().set('spc', str(int(round(px * 75))))


def set_roundrect_adj(shape, radius_px: float, width_in: float, height_in: float):
    from lxml import etree
    NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    radius_in = radius_px / 108.0
    shorter = min(width_in, height_in)
    if shorter <= 0:
        return
    adj = int(radius_in / (shorter / 2) * 100000)
    adj = max(0, min(50000, adj))
    prstGeom = shape._element.spPr.find(f'{{{NS}}}prstGeom')
    if prstGeom is None:
        return
    avLst = prstGeom.find(f'{{{NS}}}avLst')
    if avLst is None:
        avLst = etree.SubElement(prstGeom, f'{{{NS}}}avLst')
    for gd in avLst.findall(f'{{{NS}}}gd'):
        avLst.remove(gd)
    gd = etree.SubElement(avLst, f'{{{NS}}}gd')
    gd.set('name', 'adj')
    gd.set('fmla', f'val {adj}')


def suppress_line(shape):
    """Remove line (border) from shape."""
    # Use python-pptx API - this is the cleanest approach
    try:
        shape.line.fill.background()
    except:
        pass
    # Also try direct XML manipulation as backup
    try:
        from lxml import etree
        NS = 'http://schemas.openxmlformats.org/drawingml/2006/main'
        spPr = shape._element.spPr
        ln_tag = f'{{{NS}}}ln'
        for ln in spPr.findall(ln_tag):
            spPr.remove(ln)
        ln = etree.SubElement(spPr, ln_tag)
        etree.SubElement(ln, f'{{{NS}}}noFill')
    except:
        pass


def set_light_shadow(shape):
    from lxml import etree
    NP = 'http://schemas.openxmlformats.org/presentationml/2006/main'
    NA = 'http://schemas.openxmlformats.org/drawingml/2006/main'
    spPr = shape._element.spPr
    eff_tag = f'{{{NA}}}effectLst'
    existing = spPr.find(eff_tag)
    if existing is not None:
        spPr.remove(existing)
    effectLst = etree.fromstring(
        f'<a:effectLst xmlns:a="{NA}">'
        f'<a:outerShdw blurRad="25000" dist="8000" dir="5400000" rotWithShape="0">'
        f'<a:srgbClr val="000000"><a:alpha val="8000"/></a:srgbClr>'
        f'</a:outerShdw></a:effectLst>'
    )
    spPr.append(effectLst)
    style_elem = shape._element.find(f'{{{NP}}}style')
    if style_elem is not None:
        eff_ref = style_elem.find(f'{{{NA}}}effectRef')
        if eff_ref is not None:
            eff_ref.set('idx', '0')


def set_explicit_line(shape, rgb: Tuple[int, int, int], width_pt: float) -> None:
    """Force an explicit solid line in XML for subtle bordered shapes."""
    try:
        shape.line.fill.solid()
    except Exception:
        pass
    try:
        shape.line.color.rgb = RGBColor(*rgb)
        shape.line.width = Pt(max(width_pt, 0.5))
    except Exception:
        pass


def segments_to_lines(segments):
    """Split segments into lines (list of list)."""
    cleaned = []
    for s in segments:
        t = s['text']
        if t == '\n':
            cleaned.append(s)
        elif t.strip():
            cleaned.append({'text': t, 'color': s['color'],
                           'bold': s.get('bold', False),
                           'fontSize': s.get('fontSize', ''),
                           'fontFamily': s.get('fontFamily', ''),
                           'letterSpacing': s.get('letterSpacing', ''),
                           'strike': s.get('strike', False),
                           'bgColor': s.get('bgColor'),
                           'inlineBgBounds': s.get('inlineBgBounds'),
                           'kind': s.get('kind', 'text')})
    segments = cleaned
    lines = []
    current_line = []
    for seg in segments:
        text = seg['text']
        if '\n' in text:
            parts = text.split('\n')
            for i, part in enumerate(parts):
                if part:
                    current_line.append({**seg, 'text': part})
                if i < len(parts) - 1:
                    lines.append(current_line)
                    current_line = []
        else:
            current_line.append(seg)
    lines.append(current_line)
    # Filter out empty lines (from pure \n segments)
    lines = [l for l in lines if any(s['text'].strip() for s in l)]
    return lines


def _layout_single_line_fragments(
    fragments: List[Dict[str, Any]],
    bounds: Dict[str, float],
    default_font_px: float,
    text_align: str = 'left',
    pad_l_in: float = 0.0,
    pad_r_in: float = 0.0,
    pad_t_in: float = 0.0,
    pad_b_in: float = 0.0,
) -> List[Dict[str, Any]]:
    """Compute one-line fragment boxes within a text bounds rectangle."""
    inner_x = bounds['x'] + pad_l_in
    inner_y = bounds['y'] + pad_t_in
    inner_w = max(bounds['width'] - pad_l_in - pad_r_in, 0.05)
    row_h = max(bounds['height'] - pad_t_in - pad_b_in, 0.05)

    laid_out: List[Dict[str, Any]] = []
    total_w = 0.0
    for fragment in fragments:
        frag_text = fragment.get('text', '')
        if not frag_text or frag_text == '\n':
            continue
        frag_kind = fragment.get('kind', 'text')
        frag_font_px = parse_px(fragment.get('fontSize', '')) or default_font_px
        frag_w_px, frag_h_px = _measure_inline_fragment_box_px(
            fragment,
            frag_font_px,
            include_box_padding=frag_kind in INLINE_BOX_KINDS,
        )
        if fragment.get('_pillify'):
            frag_w_px += 8.0
            frag_h_px += 10.0
        frag_w = frag_w_px / PX_PER_IN
        frag_h = max(
            frag_h_px / PX_PER_IN,
            row_h if frag_kind in INLINE_BOX_KINDS else 0.0,
        )
        laid_out.append({
            'fragment': fragment,
            'width': frag_w,
            'height': frag_h or row_h,
        })
        total_w += frag_w

    if text_align == 'center':
        cursor_x = inner_x + max((inner_w - total_w) / 2.0, 0.0)
    elif text_align == 'right':
        cursor_x = inner_x + max(inner_w - total_w, 0.0)
    else:
        cursor_x = inner_x

    for metric in laid_out:
        metric['x'] = cursor_x
        metric['y'] = inner_y + max((row_h - metric['height']) / 2.0, 0.0)
        cursor_x += metric['width']
    return laid_out


def _export_inline_box_overlay(slide, fragment: Dict[str, Any], box: Dict[str, float]) -> None:
    """Render a background/border box for inline code/kbd fragments behind a text box."""
    styles = fragment.get('styles', {})
    radius_px = resolve_border_radius(styles, box['width'] * PX_PER_IN, box['height'] * PX_PER_IN)
    if fragment.get('_pillify'):
        radius_px = max(radius_px, box['height'] * PX_PER_IN / 2.0 - 1.0)
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE if radius_px > 0 else MSO_SHAPE.RECTANGLE,
        Inches(box['x']), Inches(box['y']),
        Inches(box['width']), Inches(box['height'])
    )
    if radius_px > 0:
        set_roundrect_adj(shape, radius_px, box['width'], box['height'])

    bg_color = styles.get('backgroundColor', '') or fragment.get('bgColor', '')
    if fragment.get('_pillify') and not bg_color:
        bg_color = 'rgba(37,99,235,0.10)'
    bg_rgb = parse_color(bg_color)
    if bg_rgb:
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*bg_rgb)
    else:
        shape.fill.background()

    border_rgb = None
    border_width_pt = 0.5
    for border_key in ('border', 'borderLeft'):
        border_val = styles.get(border_key, '')
        border_match = re.search(r'([\d.]+)px.*?(#[0-9a-fA-F]{6}|rgba?\([^)]+\))', border_val)
        if border_match:
            border_rgb = parse_color(border_match.group(2))
            border_width_pt = max(0.5, float(border_match.group(1)) * 0.75)
            break
    if border_rgb:
        shape.line.color.rgb = RGBColor(*border_rgb)
        shape.line.width = Pt(border_width_pt)
    elif fragment.get('_pillify'):
        pill_border = parse_color('rgba(37,99,235,0.20)')
        if pill_border:
            shape.line.color.rgb = RGBColor(*pill_border)
            shape.line.width = Pt(0.75)
    else:
        suppress_line(shape)


def apply_run(run, text, color_str, font_size_pt, font_weight,
              text_transform='none', font_family='', letter_spacing='', strike=False):
    if text_transform == 'uppercase':
        text = text.upper()
    run.text = text
    if text and (text[0] == ' ' or text[-1] == ' '):
        _nsmap = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
        _t_elem = run._r.find('.//a:t', _nsmap)
        if _t_elem is not None:
            _t_elem.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    latin_font, ea_font = map_font(font_family, text=text)
    set_run_fonts(run, latin_font, ea_font)
    if font_size_pt:
        run.font.size = Pt(font_size_pt)
    try:
        if font_weight == 'bold':
            run.font.bold = True
        else:
            run.font.bold = int(font_weight) >= 600
    except Exception:
        pass
    rgb = parse_color(color_str)
    if rgb:
        run.font.color.rgb = RGBColor(*rgb)
    if strike:
        _ns = 'http://schemas.openxmlformats.org/drawingml/2006/main'
        _rPr = run._r.find(f'{{{_ns}}}rPr')
        if _rPr is None:
            _rPr = _etree.SubElement(run._r, f'{{{_ns}}}rPr')
            run._r.insert(0, _rPr)
        _rPr.set('strike', 'sngStrike')
    set_letter_spacing(run, letter_spacing, font_size_pt)


def apply_para_format(p, s, font_size_pt: float = 0.0):
    lh = s.get('lineHeight', 'normal')
    if lh == 'normal':
        if font_size_pt > 0:
            p.line_spacing = Pt(round(font_size_pt * 1.2, 1))
        else:
            p.line_spacing = 1.2
    else:
        try:
            if 'px' in lh:
                lh_px = float(re.search(r'([\d.]+)', lh).group(1))
                p.line_spacing = Pt(round(lh_px * 0.75, 1))
            else:
                line_multiple = float(lh)
                if font_size_pt > 0:
                    p.line_spacing = Pt(round(font_size_pt * line_multiple, 1))
                else:
                    p.line_spacing = line_multiple
        except Exception:
            if font_size_pt > 0:
                p.line_spacing = Pt(round(font_size_pt * 1.2, 1))
            else:
                p.line_spacing = 1.2
    align = s.get('textAlign', 'left')
    if align == 'center':
        p.alignment = PP_ALIGN.CENTER
    elif align == 'right':
        p.alignment = PP_ALIGN.RIGHT


def _estimate_line_height_in(styles: Dict[str, str], font_size_pt: float) -> float:
    """Estimate a single rendered line height in inches from CSS text styles."""
    if font_size_pt <= 0:
        font_size_pt = 12.0
    lh = styles.get('lineHeight', 'normal')
    if lh == 'normal':
        line_spacing_pt = font_size_pt * _default_normal_line_height_multiple(styles.get('_tag', ''))
    else:
        try:
            if 'px' in lh:
                lh_px = float(re.search(r'([\d.]+)', lh).group(1))
                line_spacing_pt = lh_px * 0.75
            else:
                line_spacing_pt = font_size_pt * float(lh)
        except Exception:
            line_spacing_pt = font_size_pt * 1.2
    return max(line_spacing_pt / 72.0, font_size_pt / 72.0)


def gradient_to_solid(bg_image, slide_bg=(255, 255, 255)):
    if not bg_image or 'gradient' not in bg_image:
        return None
    rgba_matches = re.findall(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)', bg_image)
    if rgba_matches:
        r, g, b = int(rgba_matches[0][0]), int(rgba_matches[0][1]), int(rgba_matches[0][2])
        a = float(rgba_matches[0][3]) if rgba_matches[0][3] else 1.0
        if a <= 0:
            return None
        if a < 1.0:
            r = int(a * r + (1 - a) * slide_bg[0])
            g = int(a * g + (1 - a) * slide_bg[1])
            b = int(a * b + (1 - a) * slide_bg[2])
        return (r, g, b)
    # Fallback: try hex colors in gradient (e.g. linear-gradient(90deg, #2563eb, #0ea5e9))
    hex_matches = re.findall(r'#([0-9a-fA-F]{6})', bg_image)
    if hex_matches:
        h = hex_matches[0]
        return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))
    return None


def interpolate_color(c1, c2, t):
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t)
    )


def export_shape_background(slide, elem, slide_bg=(255, 255, 255)):
    """Create background shape (no text) for type=shape containers."""
    b = elem['bounds']
    s = elem['styles']
    border_radius = s.get('borderRadius', '')
    radius_px = 0.0
    if border_radius and border_radius != '0px':
        m = re.search(r'([\d.]+)px', border_radius)
        if m:
            radius_px = float(m.group(1))

    height_px = b['height'] * 108.0
    if radius_px > 0 and radius_px < height_px * 0.4:
        radius_px = min(radius_px, 6.0)

    def parse_border_side(bs):
        if not bs or 'none' in bs or bs.startswith('0px'):
            return None
        # Try rgb/rgba format first
        m = re.search(r'([\d.]+)px.*?rgba?\((\d+),\s*(\d+),\s*(\d+)', bs)
        if m:
            return {'width': float(m.group(1)), 'rgb': (int(m.group(2)), int(m.group(3)), int(m.group(4)))}
        # Try hex color format: 4px solid #D97706
        m = re.search(r'([\d.]+)px.*?#([0-9a-fA-F]{6})', bs)
        if m:
            h = m.group(2)
            return {'width': float(m.group(1)), 'rgb': (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))}
        return None

    bl = parse_border_side(s.get('borderLeft', ''))
    br = parse_border_side(s.get('borderRight', ''))
    bt = parse_border_side(s.get('borderTop', ''))
    bb = parse_border_side(s.get('borderBottom', ''))
    # Accent-bar cards should not also emit extra top/right/bottom border shapes.
    if bl and bl['width'] >= 4.0:
        br = None
        bt = None
        bb = None
    borders = [x for x in [bl, br, bt, bb] if x is not None]
    all_uniform = (len(borders) >= 3 and
                   all(bd['rgb'] == borders[0]['rgb'] and bd['width'] == borders[0]['width']
                       for bd in borders))

    BAR_VISIBLE_PX = 4.0
    bl_handled = False
    shape_x = b['x']
    shape_w = b['width']
    if bl and not all_uniform and radius_px > 0 and bl['width'] >= 4.0:
        # Accent cards look closer to the browser and native PPT when the accent
        # is a narrow rounded strip tucked under the main card, rather than a
        # full accent-colored base with an inset white overlay.
        bar_visible_px = max(BAR_VISIBLE_PX, bl['width'])
        bar_visible_in = bar_visible_px / 108.0
        accent_w = min(max(bar_visible_in + radius_px / PX_PER_IN * 0.80, 0.16), 0.22)
        overlap_in = min(max(radius_px / PX_PER_IN * 0.18, 0.03), 0.05)
        accent_base = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(max(b['x'] - overlap_in, 0.0)), Inches(b['y']),
            Inches(accent_w), Inches(b['height'])
        )
        set_roundrect_adj(accent_base, radius_px, accent_w, b['height'])
        accent_base.fill.solid()
        accent_base.fill.fore_color.rgb = RGBColor(*bl['rgb'])
        suppress_line(accent_base)
        shape_x = b['x']
        shape_w = max(b['width'], 0.05)
        bl_handled = True

    blend_bg = slide_bg
    bg_rgb = parse_color(s.get('backgroundColor', ''), bg=blend_bg)
    grad_fill = gradient_to_solid(s.get('backgroundImage', ''), slide_bg=slide_bg)
    is_stamp_seal = (
        all_uniform and
        bg_rgb is not None and
        b.get('width', 0.0) <= 0.35 and
        b.get('height', 0.0) <= 0.35
    )
    render_border_only = (
        not bg_rgb and
        not grad_fill and
        len(borders) >= 1 and
        not all_uniform and
        not bl_handled and
        not elem.get('pill_text')
    )
    if render_border_only:
        def _is_subtle_border(bd):
            return (bd['rgb'][0] >= 240 and bd['rgb'][1] >= 240 and bd['rgb'][2] >= 240)

        if bl and not _is_subtle_border(bl):
            border_shape = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(b['x']), Inches(b['y']),
                Inches(bl['width'] / 108.0), Inches(b['height'])
            )
            border_shape.fill.solid()
            border_shape.fill.fore_color.rgb = RGBColor(*bl['rgb'])
            suppress_line(border_shape)
        if br and not _is_subtle_border(br):
            border_shape = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(b['x'] + b['width'] - br['width'] / 108.0), Inches(b['y']),
                Inches(br['width'] / 108.0), Inches(b['height'])
            )
            border_shape.fill.solid()
            border_shape.fill.fore_color.rgb = RGBColor(*br['rgb'])
            suppress_line(border_shape)
        if bt and not _is_subtle_border(bt):
            border_shape = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(b['x']), Inches(b['y']),
                Inches(b['width']), Inches(bt['width'] / 108.0)
            )
            border_shape.fill.solid()
            border_shape.fill.fore_color.rgb = RGBColor(*bt['rgb'])
            suppress_line(border_shape)
        return

    shape_kind = MSO_SHAPE.ROUNDED_RECTANGLE if radius_px > 0 else MSO_SHAPE.RECTANGLE
    if elem.get('tag') == 'circle':
        shape_kind = MSO_SHAPE.OVAL
    shape = slide.shapes.add_shape(
        shape_kind,
        Inches(shape_x), Inches(b['y']),
        Inches(shape_w), Inches(b['height'])
    )
    if radius_px > 0 and elem.get('tag') != 'circle':
        set_roundrect_adj(shape, radius_px, shape_w, b['height'])

    # Background color: slide-based alpha blending for rgba colors (matches P1 style)
    if bg_rgb:
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*bg_rgb)
    else:
        if grad_fill:
            shape.fill.solid()
            shape.fill.fore_color.rgb = RGBColor(*grad_fill)
        else:
            shape.fill.background()

    if all_uniform:
        # For subtle borders (white/near-white with low alpha), suppress entirely.
        # Golden reference shows container shapes (cards, callouts) have no borders.
        bd = borders[0]
        is_white_or_near_white = (
            bd['rgb'][0] >= 240 and bd['rgb'][1] >= 240 and bd['rgb'][2] >= 240
        )
        if is_white_or_near_white and bd['width'] <= 1.5:
            suppress_line(shape)
        else:
            set_explicit_line(shape, bd['rgb'], max(0.5, bd['width'] * 0.75))
    elif len(borders) >= 1:
        suppress_line(shape)
        # Helper: skip border shape if near-white (golden doesn't have white borders)
        def _is_subtle_border(bd):
            return (bd['rgb'][0] >= 240 and bd['rgb'][1] >= 240 and
                    bd['rgb'][2] >= 240)
        if bl and not bl_handled and not _is_subtle_border(bl):
            border_shape = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(b['x']), Inches(b['y']),
                Inches(bl['width'] / 108.0), Inches(b['height'])
            )
            border_shape.fill.solid()
            border_shape.fill.fore_color.rgb = RGBColor(*bl['rgb'])
            suppress_line(border_shape)
        if br and not _is_subtle_border(br):
            border_shape = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(b['x'] + b['width'] - br['width']/108.0), Inches(b['y']),
                Inches(br['width'] / 108.0), Inches(b['height'])
            )
            border_shape.fill.solid()
            border_shape.fill.fore_color.rgb = RGBColor(*br['rgb'])
            suppress_line(border_shape)
        if bt and not _is_subtle_border(bt):
            border_shape = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(b['x']), Inches(b['y']),
                Inches(b['width']), Inches(bt['width'] / 108.0)
            )
            border_shape.fill.solid()
            border_shape.fill.fore_color.rgb = RGBColor(*bt['rgb'])
            suppress_line(border_shape)
        if bb:
            # Skip rendering border-bottom as a separate shape.
            # Golden doesn't create separate separator shapes for borders —
            # the border-bottom CSS is too subtle to warrant a PPTX element.
            pass
    else:
        suppress_line(shape)

    if not elem.get('_is_decoration') and not is_stamp_seal and (bg_rgb or grad_fill):
        set_light_shadow(shape)
    tf = shape.text_frame

    # Pill shapes: embed text directly into shape's text frame (like P1 _pair_with pattern)
    pill_text = elem.get('pill_text', '')
    if pill_text:
        from pptx.enum.text import MSO_AUTO_SIZE
        tf.word_wrap = False
        tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
        tf.margin_left = Pt(8)
        tf.margin_right = Pt(8)
        tf.margin_top = Pt(4)
        tf.margin_bottom = Pt(4)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = pill_text
        font_size_pt = px_to_pt(s.get('fontSize', '14px'))
        run.font.size = Pt(font_size_pt)
        latin_font, ea_font = map_font(s.get('fontFamily', ''), text=pill_text)
        set_run_fonts(run, latin_font, ea_font)
        pill_color_hex = elem.get('pill_color', '')
        if pill_color_hex:
            # Resolve CSS variables if needed
            if pill_color_hex.startswith('var('):
                resolved = resolve_css_variables_inline(pill_color_hex)
                if resolved.startswith('#') and len(resolved) == 7:
                    pill_color_hex = resolved[1:]
                elif resolved.startswith('rgb'):
                    rm = re.match(r'rgb\((\d+),\s*(\d+),\s*(\d+)\)', resolved)
                    if rm:
                        pill_color_hex = f'{int(rm.group(1)):02X}{int(rm.group(2)):02X}{int(rm.group(3)):02X}'
            if pill_color_hex.startswith('#'):
                pill_color_hex = pill_color_hex[1:]
            if len(pill_color_hex) == 6:
                try:
                    run.font.color.rgb = RGBColor(
                        int(pill_color_hex[0:2], 16),
                        int(pill_color_hex[2:4], 16),
                        int(pill_color_hex[4:6], 16)
                    )
                except Exception:
                    pass
        else:
            run.font.color.rgb = RGBColor(0, 0, 0)
    else:
        # Clear text for non-pill shapes
        if tf.paragraphs:
            for para in tf.paragraphs:
                for run in para.runs:
                    run.text = ''


def export_freeform_element(slide, elem):
    points = elem.get('points') or []
    if len(points) < 2:
        return
    styles = elem.get('styles', {})
    fill_color = parse_color(styles.get('fill', ''), bg=(255, 255, 255))
    stroke_color = parse_color(styles.get('stroke', ''), bg=(255, 255, 255))
    stroke_width = max(float(styles.get('strokeWidth', 1.0) or 1.0), 0.0)
    is_closed = bool(elem.get('closed'))

    if not is_closed and stroke_color and stroke_width > 0:
        for (x1, y1), (x2, y2) in zip(points, points[1:]):
            line = slide.shapes.add_connector(
                MSO_CONNECTOR.STRAIGHT,
                Inches(x1),
                Inches(y1),
                Inches(x2),
                Inches(y2),
            )
            line.line.color.rgb = RGBColor(*stroke_color)
            line.line.width = Pt(max(0.5, stroke_width * 0.75))
        return

    first_x, first_y = points[0]
    builder = slide.shapes.build_freeform(Inches(first_x), Inches(first_y), scale=Inches(1.0))
    builder.add_line_segments([(x, y) for x, y in points[1:]], close=is_closed)
    shape = builder.convert_to_shape()

    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = RGBColor(*fill_color)
    else:
        shape.fill.background()

    if stroke_color and stroke_width > 0:
        shape.line.color.rgb = RGBColor(*stroke_color)
        shape.line.width = Pt(max(0.5, stroke_width * 0.75))
    else:
        suppress_line(shape)


def export_text_element(slide, elem, bg_color=None):
    b = elem['bounds']
    s = elem['styles']
    segments = elem.get('segments', [])
    text_transform = elem.get('textTransform', 'none')
    font_size_pt = px_to_pt(s.get('fontSize', '16px'))
    font_size_px = parse_px(s.get('fontSize', '16px'))
    if font_size_px <= 0:
        font_size_px = 16.0
    font_weight = s.get('fontWeight', '400')
    font_family = s.get('fontFamily', '')
    letter_spacing = s.get('letterSpacing', '')

    natural_h = elem.get('naturalHeight', b['height'])
    # Use the max of bounds height and naturalHeight (both computed from CSS)
    # Don't add extra minimum — PPTX renders text at CSS-specified line-height
    effective_h = max(b['height'], natural_h)

    if not segments:
        raw = (elem.get('text', '') or '').strip()
        segments = [{'text': raw, 'color': s.get('color', '')}]

    lines = segments_to_lines(segments)
    if not lines:
        lines = [[{'text': '', 'color': s.get('color', '')}]]

    pad_l = parse_px(s.get('paddingLeft', ''))
    pad_r = parse_px(s.get('paddingRight', ''))
    pad_t = parse_px(s.get('paddingTop', ''))
    pad_b = parse_px(s.get('paddingBottom', ''))

    if elem.get('renderInlineBoxOverlays') and len(lines) <= 1 and '\n' not in (elem.get('text', '') or ''):
        overlay_fragments = elem.get('fragments', [])
        if elem.get('preferCenteredBlockWidth'):
            overlay_fragments = []
            for fragment in elem.get('fragments', []):
                next_fragment = dict(fragment)
                if next_fragment.get('kind') in ('code', 'kbd'):
                    next_fragment['_pillify'] = True
                overlay_fragments.append(next_fragment)
            box_only_fragments = [f for f in overlay_fragments if f.get('kind') in INLINE_BOX_KINDS]
            if box_only_fragments:
                _export_inline_fragment_runway(
                    slide,
                    box_only_fragments if len(box_only_fragments) == 1 else overlay_fragments,
                    {'x': b['x'], 'y': b['y'], 'width': b['width'], 'height': effective_h},
                    s,
                    render_text_fragments=False,
                )
        else:
            _export_inline_fragment_runway(
                slide,
                overlay_fragments,
                {'x': b['x'], 'y': b['y'], 'width': b['width'], 'height': effective_h},
                s,
            )
            return

    txBox = slide.shapes.add_textbox(
        Inches(b['x']), Inches(b['y']),
        Inches(b['width']), Inches(effective_h)
    )
    geometry_id = elem.get('geometry_id')
    if geometry_id:
        try:
            txBox.name = geometry_id
        except Exception:
            pass
    tf = txBox.text_frame
    render_hint = elem.get('pptxRenderHint') or {}
    hinted_wrap_mode = render_hint.get('wrap_mode')
    hinted_auto_size = render_hint.get('auto_size')
    explicit_break_heading = (
        elem.get('tag') in ('h1', 'h2', 'h3') and
        '\n' in (elem.get('text', '') or '') and
        font_size_pt >= 28
    )
    preserve_authored_breaks = bool(elem.get('preserveAuthoredBreaks'))
    prefer_wrap_to_preserve_size = bool(elem.get('preferWrapToPreserveSize'))
    display_heading_like = (
        (
            elem.get('tag') in ('h1', 'h2', 'h3') or
            elem.get('_text_contract_role') == 'title'
        ) and
        font_size_pt >= 20 and
        len(lines) <= 1
    )
    display_metric_like = (
        len(lines) <= 1 and
        font_size_pt >= 18 and
        _looks_like_metric_token((elem.get('text', '') or '').strip())
    )
    single_line_contract_heading = (
        prefer_wrap_to_preserve_size and
        display_heading_like and
        font_size_pt >= 28 and
        '\n' not in (elem.get('text', '') or '') and
        _can_preserve_single_line_contract_heading(
            elem,
            font_size_px,
            b['width'],
            letter_spacing=s.get('letterSpacing', ''),
        )
    )
    inferred_multiline_prose = (
        elem.get('tag') in ('p', 'div') and
        not elem.get('forceSingleLine') and
        not elem.get('preferNoWrapFit') and
        '\n' not in (elem.get('text', '') or '') and
        effective_h > _estimate_line_height_in(s, font_size_pt) * 1.35
    )
    # Match golden: single-line text uses TEXT_TO_FIT_SHAPE with no wrap,
    # multi-line text uses SHAPE_TO_FIT_TEXT with wrap
    from pptx.enum.text import MSO_AUTO_SIZE
    auto_size_by_hint = {
        'text_to_fit_shape': MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE,
        'shape_to_fit_text': MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT,
        'none': MSO_AUTO_SIZE.NONE,
    }
    if hinted_wrap_mode in {'none', 'square'} and hinted_auto_size in auto_size_by_hint:
        tf.word_wrap = hinted_wrap_mode == 'square'
        tf.auto_size = auto_size_by_hint[hinted_auto_size]
    elif explicit_break_heading:
        # Explicit <br> in large centered headings should remain the only line
        # breaks. Let the heading keep its authored line structure instead of
        # allowing PowerPoint to wrap again on the last word/character.
        tf.word_wrap = False
        tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
    elif single_line_contract_heading:
        # If the authored display title already fits, keep it on one line and
        # grow the box rather than letting PowerPoint invent an extra wrap.
        tf.word_wrap = False
        tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
    elif prefer_wrap_to_preserve_size:
        # Contract-preferred display titles may not include explicit <br>, but
        # they still rely on the browser's natural wrapping inside a capped
        # width. Preserve authored width rhythm by growing the textbox instead
        # of crushing the type onto one line.
        tf.word_wrap = True
        tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
    elif preserve_authored_breaks:
        # Contract-authored rhythm text should keep only the explicit source
        # breaks. Let the textbox grow instead of shrinking or reflowing.
        tf.word_wrap = False
        tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
    elif display_heading_like or display_metric_like:
        # Display headings / KPI tokens should preserve authored font size and
        # let the textbox grow instead of shrinking the typography.
        tf.word_wrap = False
        tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
    elif elem.get('forceSingleLine'):
        tf.word_wrap = False
        tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
    elif elem.get('preferNoWrapFit'):
        tf.word_wrap = False
        tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
    elif inferred_multiline_prose:
        tf.word_wrap = True
        tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
    elif len(lines) <= 1:
        # Check if text is likely to overflow the box width (card descriptions, etc.)
        raw_text = elem.get('text', '') or ''
        # If text has no newlines but is long (>30 chars) and box is narrow (<5"),
        # enable word wrap to prevent overflow
        needs_wrap = len(raw_text) > 20 and b['width'] < 5.0
        if needs_wrap:
            tf.word_wrap = True
            tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT
        else:
            tf.word_wrap = False
            tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
    else:
        tf.word_wrap = True
        tf.auto_size = MSO_AUTO_SIZE.SHAPE_TO_FIT_TEXT

    tf.margin_left = Inches(pad_l / 108.0) if pad_l > 0 else 0
    tf.margin_right = Inches(pad_r / 108.0) if pad_r > 0 else 0
    tf.margin_top = Inches(pad_t / 108.0) if pad_t > 0 else 0
    tf.margin_bottom = Inches(pad_b / 108.0) if pad_b > 0 else 0

    gradient_colors = elem.get('gradientColors')
    gc_start = parse_color(gradient_colors[0]) if gradient_colors else None
    gc_end = parse_color(gradient_colors[1]) if gradient_colors else None
    total_lines = len(lines)
    is_li = elem.get('tag') == 'li'
    li_bullet_color = 'rgb(56, 139, 253)'

    for line_idx, line_segs in enumerate(lines):
        p = tf.add_paragraph() if line_idx > 0 else tf.paragraphs[0]
        apply_para_format(p, s, font_size_pt)
        justify_content = s.get('justifyContent', '')
        if justify_content in ('center', 'space-around', 'space-evenly'):
            p.alignment = PP_ALIGN.CENTER

        if is_li and line_idx == 0:
            bullet_run = p.add_run()
            apply_run(bullet_run, '▶ ', li_bullet_color, font_size_pt * 0.7, '400')

        if gc_start and gc_end and total_lines > 1:
            t = line_idx / (total_lines - 1)
            grad_rgb = interpolate_color(gc_start, gc_end, t)
            override_color = 'rgb({},{},{})'.format(*grad_rgb)
        elif gc_start and gc_end:
            override_color = gradient_colors[0]
        else:
            override_color = None

        for seg in line_segs:
            if not seg['text']:
                continue
            run = p.add_run()
            color = override_color or seg['color']
            seg_weight = 'bold' if seg.get('bold') else font_weight
            seg_fs_raw = seg.get('fontSize', '')
            seg_font_size_pt = px_to_pt(seg_fs_raw) if seg_fs_raw else font_size_pt
            seg_font_family = seg.get('fontFamily') or font_family
            seg_letter_spacing = seg.get('letterSpacing') or letter_spacing
            apply_run(run, seg['text'], color, seg_font_size_pt, seg_weight, text_transform,
                      font_family=seg_font_family, letter_spacing=seg_letter_spacing,
                      strike=seg.get('strike', False))


def _bind_geometry_render_hints(elements: List[Dict[str, Any]], text_hints: Dict[str, Dict[str, Any]]) -> None:
    for elem in elements:
        if elem.get('type') == 'text':
            geometry_id = elem.get('geometry_id')
            if geometry_id and geometry_id in text_hints and not elem.get('pptxRenderHint'):
                elem['pptxRenderHint'] = copy.deepcopy(text_hints[geometry_id])
        children = elem.get('children') or []
        if children:
            _bind_geometry_render_hints(children, text_hints)


def _export_inline_fragment_runway(slide, fragments, bounds, cell_styles, render_text_fragments: bool = True):
    """Render a one-line inline fragment sequence with first-class box fragments."""
    default_font_px = parse_px(cell_styles.get('fontSize', '14px')) or 14.0
    default_font_pt = px_to_pt(cell_styles.get('fontSize', '14px'))
    font_family = cell_styles.get('fontFamily', '')
    letter_spacing = cell_styles.get('letterSpacing', '')
    laid_out = _layout_single_line_fragments(
        fragments,
        bounds,
        default_font_px,
        text_align=cell_styles.get('textAlign', 'left'),
    )

    for metric in laid_out:
        fragment = metric['fragment']
        frag_text = fragment.get('text', '')
        frag_kind = fragment.get('kind', 'text')
        frag_font_pt = px_to_pt(fragment.get('fontSize', '')) if fragment.get('fontSize') else default_font_pt
        frag_font_family = fragment.get('styles', {}).get('fontFamily', '') or font_family
        frag_letter_spacing = fragment.get('styles', {}).get('letterSpacing', '') or letter_spacing
        if frag_kind in INLINE_BOX_KINDS:
            _export_inline_box_overlay(slide, fragment, metric)
            if not render_text_fragments:
                continue
            text_box = slide.shapes.add_textbox(
                Inches(metric['x']), Inches(metric['y']),
                Inches(max(metric['width'], 0.05)), Inches(metric['height'])
            )
            tf = text_box.text_frame
            tf.word_wrap = False
            tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
            tf.margin_left = 0
            tf.margin_right = 0
            tf.margin_top = 0
            tf.margin_bottom = 0
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            run = p.add_run()
            apply_run(
                run,
                frag_text,
                fragment.get('color', cell_styles.get('color', '')),
                frag_font_pt,
                'bold' if fragment.get('bold') else cell_styles.get('fontWeight', '400'),
                font_family=frag_font_family,
                letter_spacing=frag_letter_spacing,
                strike=fragment.get('strike', False),
            )
            continue

        if not render_text_fragments:
            continue
        if frag_text.isspace():
            continue
        text_box = slide.shapes.add_textbox(
            Inches(metric['x']), Inches(bounds['y']),
            Inches(max(metric['width'] + 0.02, 0.05)), Inches(bounds['height'])
        )
        tf = text_box.text_frame
        tf.word_wrap = False
        tf.auto_size = MSO_AUTO_SIZE.TEXT_TO_FIT_SHAPE
        tf.margin_left = 0
        tf.margin_right = 0
        tf.margin_top = 0
        tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        run = p.add_run()
        apply_run(
            run,
            frag_text,
            fragment.get('color', cell_styles.get('color', '')),
            frag_font_pt,
            'bold' if fragment.get('bold') else cell_styles.get('fontWeight', '400'),
            font_family=frag_font_family,
            letter_spacing=frag_letter_spacing,
            strike=fragment.get('strike', False),
        )


def export_presentation_rows_element(slide, elem):
    rows = elem.get('rows', [])
    if not rows:
        return

    tb = elem['bounds']
    table_x = tb['x']
    table_y = tb['y']
    table_w = tb['width']
    row_heights = [row.get('height', tb['height'] / len(rows) if rows else 0.5) for row in rows]
    col_widths = _compute_presentation_row_column_widths(rows, table_w)

    current_y = table_y
    for row_idx, row_data in enumerate(rows):
        row_h = row_heights[row_idx] if row_idx < len(row_heights) else 0.264

        current_x = table_x
        for col_idx, cell in enumerate(row_data.get('cells', [])):
            cell_w = col_widths[col_idx] if col_idx < len(col_widths) else (table_w / max(len(col_widths), 1))
            cell_styles = cell.get('styles', {})
            pad_l = parse_px(cell_styles.get('paddingLeft', '0px')) / PX_PER_IN
            pad_r = parse_px(cell_styles.get('paddingRight', '0px')) / PX_PER_IN
            content_bounds = {
                'x': current_x + pad_l,
                'y': current_y,
                'width': max(cell_w - pad_l - pad_r, 0.05),
                'height': max(row_h, 0.16),
            }
            fragments = cell.get('fragments') or []
            segment_list = cell.get('segments') or inline_fragments_to_segments(fragments)
            if col_idx == 0:
                label_color = _presentation_row_label_color(cell_styles.get('color', ''))
                segment_list = [
                    {**segment, 'color': _presentation_row_label_color(segment.get('color', label_color))}
                    for segment in segment_list
                ]
            export_text_element(slide, {
                'type': 'text',
                'tag': 'td',
                'text': cell.get('text', ''),
                'segments': segment_list,
                'fragments': fragments,
                'bounds': content_bounds,
                'naturalHeight': content_bounds['height'],
                'styles': {
                    'fontSize': cell_styles.get('fontSize', '14px'),
                    'fontWeight': cell_styles.get('fontWeight', '400'),
                    'fontFamily': cell_styles.get('fontFamily', ''),
                    'letterSpacing': cell_styles.get('letterSpacing', ''),
                    'color': _presentation_row_label_color(cell_styles.get('color', '')) if col_idx == 0 else cell_styles.get('color', ''),
                    'textAlign': cell_styles.get('textAlign', 'left'),
                    'lineHeight': 'normal',
                    'paddingLeft': '0px',
                    'paddingRight': '0px',
                    'paddingTop': '0px',
                    'paddingBottom': '0px',
                },
            })
            current_x += cell_w
        current_y += row_h


def export_table_element(slide, elem):
    rows = elem.get('rows', [])
    if not rows:
        return
    tb = elem['bounds']
    table_x = tb['x']
    table_y = tb['y']
    table_w = tb['width']
    is_presentation_rows = elem.get('type') == 'presentation_rows'
    num_cols = max(len(row_data['cells']) for row_data in rows) if rows else 1
    measure = elem.get('measure', {})
    row_heights = measure.get('row_heights') or [row.get('height', tb['height'] / len(rows) if rows else 0.5) for row in rows]

    # Content-aware column widths
    col_widths = measure.get('col_widths')
    if not col_widths:
        if is_presentation_rows:
            col_widths = _compute_presentation_row_column_widths(rows, table_w)
        else:
            col_widths = _compute_table_column_widths(rows, table_w)

    for row_idx, row_data in enumerate(rows):
        for col_idx, cell in enumerate(row_data['cells']):
            cb = cell['bounds']
            cs = cell['styles']
            cx = table_x + sum(col_widths[:col_idx])
            cy = table_y + sum(row_heights[:row_idx])
            cw = col_widths[col_idx] if col_idx < len(col_widths) else table_w / num_cols
            ch = row_heights[row_idx] if row_idx < len(row_heights) else (tb['height'] / len(rows) if rows else 0.5)
            if cw < 0.01 or ch < 0.01:
                continue
            cell_shape = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE,
                Inches(cx), Inches(cy),
                Inches(cw), Inches(ch)
            )
            bg_rgb = parse_color(cs.get('backgroundColor', ''))
            if not bg_rgb:
                # When a cell wraps a single inline-block span with its own
                # background (e.g. `<td><span class="terminal-line">cmd</span></td>`),
                # promote that span's bg to the cell so the white-on-dark text
                # stays legible. Without this, the run color (#fff) renders
                # invisibly on a transparent cell.
                seg_with_bg = next(
                    (
                        seg for seg in cell.get('segments', [])
                        if (seg.get('bgColor') or '').strip()
                        and (seg.get('text') or '').strip()
                    ),
                    None,
                )
                if seg_with_bg is None:
                    for frag in cell.get('fragments', []) or []:
                        if (frag.get('bgColor') or '').strip() and (frag.get('text') or '').strip():
                            seg_with_bg = frag
                            break
                if seg_with_bg is not None:
                    bg_rgb = parse_color(seg_with_bg.get('bgColor', ''))
            if bg_rgb:
                cell_shape.fill.solid()
                cell_shape.fill.fore_color.rgb = RGBColor(*bg_rgb)
            else:
                cell_shape.fill.background()
            suppress_line(cell_shape)
            # Skip border-bottom rendering — golden doesn't create separate
            # border shapes for table cells or list items.
            segments = cell.get('segments', [])
            if not segments and cell.get('fragments'):
                segments = inline_fragments_to_segments(cell['fragments'])
            text = cell.get('text', '').strip()
            if not segments and text:
                segments = [{'text': text, 'color': cs.get('color', '')}]
            if is_presentation_rows and col_idx == 0 and has_cjk(text):
                label_color = _presentation_row_label_color(cs.get('color', ''))
                segments = [
                    {
                        **seg,
                        'color': _presentation_row_label_color(seg.get('color', label_color)),
                    }
                    for seg in segments
                ]
            if not segments:
                continue
            font_size_pt = px_to_pt(cs.get('fontSize', '14px'))
            font_weight = cs.get('fontWeight', '400')
            font_family = cs.get('fontFamily', '')
            letter_spacing = cs.get('letterSpacing', '')
            if cell['isHeader']:
                font_weight = 'bold'
            tf = cell_shape.text_frame
            tf.word_wrap = True
            pad_l, pad_r, pad_t, pad_b = _table_cell_padding_in(cs)
            tf.margin_left = Inches(pad_l)
            tf.margin_right = Inches(pad_r)
            tf.margin_top = Inches(pad_t)
            tf.margin_bottom = Inches(pad_b)
            lines = segments_to_lines(segments)
            for line_idx, line_segs in enumerate(lines):
                p = tf.add_paragraph() if line_idx > 0 else tf.paragraphs[0]
                align = cs.get('textAlign', 'left')
                if align == 'center':
                    p.alignment = PP_ALIGN.CENTER
                elif align == 'right':
                    p.alignment = PP_ALIGN.RIGHT
                for seg in line_segs:
                    if not seg['text']:
                        continue
                    run = p.add_run()
                    seg_weight = 'bold' if seg.get('bold') else font_weight
                    seg_fs_raw = seg.get('fontSize', '')
                    seg_font_size_pt = px_to_pt(seg_fs_raw) if seg_fs_raw else font_size_pt
                    apply_run(run, seg['text'], seg['color'], seg_font_size_pt, seg_weight,
                              font_family=font_family, letter_spacing=letter_spacing,
                              strike=seg.get('strike', False))


def export_image_element(slide, elem, html_dir: Path):
    """Render image element (img src or data URI)."""
    b = elem['bounds']
    source = elem.get('source', '')
    if not source:
        return
    try:
        img_bytes = None
        if source.startswith('data:image'):
            comma_idx = source.index(',')
            data = source[comma_idx + 1:]
            img_bytes = base64.b64decode(data)
        elif source.startswith(('http://', 'https://')):
            req = urllib.request.Request(source, headers={'User-Agent': 'Mozilla/5.0'})
            import ssl
            try:
                import certifi
                _ssl_ctx = ssl.create_default_context(cafile=certifi.where())
            except ImportError:
                _ssl_ctx = ssl._create_unverified_context()
            with urllib.request.urlopen(req, context=_ssl_ctx, timeout=15) as resp:
                img_bytes = resp.read()
        elif source.startswith('file://'):
            with open(source[len('file://'):], 'rb') as f:
                img_bytes = f.read()
        elif not source.startswith('<svg') and not source.startswith('<?xml'):
            img_path = html_dir / source
            if img_path.exists():
                with open(img_path, 'rb') as f:
                    img_bytes = f.read()
        if img_bytes:
            slide.shapes.add_picture(
                io.BytesIO(img_bytes),
                Inches(b['x']), Inches(b['y']),
                Inches(b['width']), Inches(b['height'])
            )
            return
    except Exception as e:
        print(f"    Warning: failed to load image: {e}")

    placeholder = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(b['x']), Inches(b['y']),
        Inches(b['width']), Inches(b['height'])
    )
    placeholder.fill.solid()
    placeholder.fill.fore_color.rgb = RGBColor(230, 230, 230)
    suppress_line(placeholder)
    tf = placeholder.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = '[Image]'
    run.font.size = Pt(12)
    run.font.color.rgb = RGBColor(150, 150, 150)


def _render_layout_element(slide, elem, html_dir: Path, slide_bg):
    """Render an element tree recursively."""
    elem_type = elem.get('type', 'text')
    if elem_type == 'container':
        for child in elem.get('children', []):
            _render_layout_element(slide, child, html_dir, slide_bg)
        return
    if elem_type == 'shape':
        export_shape_background(slide, elem, slide_bg=slide_bg)
    elif elem_type == 'freeform':
        export_freeform_element(slide, elem)
    elif elem_type == 'image':
        export_image_element(slide, elem, html_dir)
    elif elem_type == 'table':
        export_table_element(slide, elem)
    elif elem_type == 'presentation_rows':
        export_table_element(slide, elem)
    else:
        export_text_element(slide, elem, slide_bg)


def _apply_geometry_plan_background(pptx_slide, geometry_plan: Dict[str, Any], slide_w_in: float, slide_h_in: float) -> None:
    background_payload = geometry_plan.get('background') or {}
    background_solid = background_payload.get('solid')
    background_gradient = background_payload.get('gradient')
    grid_bg = background_payload.get('grid')

    if background_gradient:
        c1, c2 = background_gradient
        try:
            fill = pptx_slide.background.fill
            fill.gradient()
            fill.gradient_angle = 135.0
            stops = fill.gradient_stops
            stops[0].position = 0.0
            stops[0].color.rgb = RGBColor(*c1)
            stops[1].position = 1.0
            stops[1].color.rgb = RGBColor(*c2)
        except Exception:
            if background_solid:
                pptx_slide.background.fill.solid()
                pptx_slide.background.fill.fore_color.rgb = RGBColor(*background_solid)
    elif background_solid:
        pptx_slide.background.fill.solid()
        pptx_slide.background.fill.fore_color.rgb = RGBColor(*background_solid)

    if grid_bg:
        add_grid_background(
            pptx_slide,
            slide_w_in,
            slide_h_in,
            grid_bg['color'],
            grid_bg['sizePx'],
        )


def _render_geometry_plan(prs, geometry_plan: Dict[str, Any], slide_count: int, add_chrome: bool = False):
    blank_layout = prs.slide_layouts[6]
    pptx_slide = prs.slides.add_slide(blank_layout)
    slide_size = geometry_plan.get('slide_size') or {}
    slide_w_in = float(slide_size.get('width_in') or SLIDE_W_IN)
    slide_h_in = float(slide_size.get('height_in') or SLIDE_H_IN)
    legacy_slide = geometry_plan.get('legacy_slide_data') or {}
    html_dir = Path(geometry_plan.get('source_html_path') or '.').resolve().parent

    _apply_geometry_plan_background(pptx_slide, geometry_plan, slide_w_in, slide_h_in)

    elements = copy.deepcopy(geometry_plan.get('elements') or legacy_slide.get('elements') or [])
    text_hints = ((geometry_plan.get('pptx_render_hints') or {}).get('text') or {})
    if text_hints:
        _bind_geometry_render_hints(elements, text_hints)

    pre_pass_corrections(elements)
    slide_style = legacy_slide.get('slideStyle', {})
    slide_data = copy.deepcopy(legacy_slide) if legacy_slide else {}
    slide_index = int(geometry_plan.get('slide_index', len(prs.slides) - 1))
    slide_data['_slide_index'] = slide_index
    layout_slide_elements(elements, slide_w_in, slide_h_in, slide_style, slide_data)

    for elem in elements:
        if elem.get('type') == 'container':
            for child in elem.get('children', []):
                if child['bounds']['x'] < slide_w_in and child['bounds']['width'] > slide_w_in - child['bounds']['x']:
                    child['bounds']['width'] = slide_w_in - child['bounds']['x']
        elif elem['bounds']['x'] < slide_w_in and elem['bounds']['width'] > slide_w_in - elem['bounds']['x']:
            elem['bounds']['width'] = slide_w_in - elem['bounds']['x']

    slide_bg = (geometry_plan.get('background') or {}).get('solid')
    if slide_bg is None:
        slide_bg = (geometry_plan.get('background') or {}).get('gradient', [None])[0]
    if slide_bg is None:
        slide_bg = (legacy_slide.get('background') if legacy_slide else None)
    if slide_bg is None:
        slide_bg = (255, 255, 255)

    for elem in elements:
        try:
            _render_layout_element(pptx_slide, elem, html_dir, slide_bg)
        except Exception as e:
            print(f"    警告: {e}")

    if add_chrome and not legacy_slide.get('hasOwnChrome'):
        add_slide_chrome(pptx_slide, slide_index, slide_count, slide_w_in, slide_h_in)


def render_pptx(geometry_plans: List[Dict[str, Any]], output_path: Path, add_chrome: bool = False) -> Path:
    prs = Presentation()
    prs.slide_width = Inches(13.33)
    prs.slide_height = Inches(8.33)

    for geometry_plan in geometry_plans:
        _render_geometry_plan(prs, geometry_plan, len(geometry_plans), add_chrome=add_chrome)

    output_path = Path(output_path)
    prs.save(str(output_path))
    return output_path


def add_slide_chrome(slide, slide_idx: int, slide_count: int,
                     slide_w_in: float, slide_h_in: float, px_per_in: float = 108.0):
    counter_x = 36 / px_per_in
    counter_y = 24 / px_per_in
    txBox = slide.shapes.add_textbox(
        Inches(counter_x), Inches(counter_y), Inches(1.0), Inches(0.22)
    )
    tf = txBox.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = f"{slide_idx + 1:02d} / {slide_count:02d}"
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(100, 116, 139)
    run.font.bold = True

    dot_h = 6 / px_per_in
    dot_inactive_w = 6 / px_per_in
    dot_active_w = 28 / px_per_in
    gap = 8 / px_per_in
    total_w = (dot_inactive_w * (slide_count - 1) + dot_active_w + gap * (slide_count - 1))
    start_x = slide_w_in / 2 - total_w / 2
    dot_y = slide_h_in - 24 / px_per_in - dot_h

    x = start_x
    for j in range(slide_count):
        is_active = (j == slide_idx)
        w = dot_active_w if is_active else dot_inactive_w
        dot_shape = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(x), Inches(dot_y), Inches(w), Inches(dot_h)
        )
        dot_shape.fill.solid()
        if is_active:
            dot_shape.fill.fore_color.rgb = RGBColor(37, 99, 235)
        else:
            dot_shape.fill.fore_color.rgb = RGBColor(147, 197, 253)
        suppress_line(dot_shape)
        x += w + gap


def add_grid_background(slide, slide_w_in: float, slide_h_in: float,
                        grid_color_str: str, grid_size_px: float):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return
    scale = 3
    w = int(slide_w_in * 96 * scale)
    h = int(slide_h_in * 96 * scale)
    grid_px = max(1, int(grid_size_px * scale))
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    m = re.match(r'rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([\d.]+))?\)', grid_color_str.strip())
    if m:
        r, g, b = int(m.group(1)), int(m.group(2)), int(m.group(3))
        a = float(m.group(4) or '1.0')
        line_color = (r, g, b, int(a * 255))
    else:
        line_color = (80, 100, 170, 25)
    for y in range(0, h, grid_px):
        draw.line([(0, y), (w - 1, y)], fill=line_color, width=1)
    for x in range(0, w, grid_px):
        draw.line([(x, 0), (x, h - 1)], fill=line_color, width=1)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    pic = slide.shapes.add_picture(buf, Inches(0), Inches(0),
                                   Inches(slide_w_in), Inches(slide_h_in))
    sp_tree = slide.shapes._spTree
    sp_tree.remove(pic._element)
    sp_tree.insert(2, pic._element)


def add_aurora_mesh_background(slide, slide_w_in: float, slide_h_in: float, mesh_bg: Dict[str, Any]):
    try:
        from PIL import Image, ImageDraw, ImageFilter
    except ImportError:
        return

    base_r, base_g, base_b = mesh_bg.get('baseColor') or (10, 10, 26)
    layers = mesh_bg.get('layers') or []
    if not layers:
        return

    scale = 3
    w = int(slide_w_in * 96 * scale)
    h = int(slide_h_in * 96 * scale)
    img = Image.new('RGBA', (w, h), (base_r, base_g, base_b, 255))

    for layer in layers:
        rgba = layer.get('color')
        if not rgba:
            continue
        r, g, b, alpha = rgba
        cx = int(w * float(layer.get('cx_pct', 50.0)) / 100.0)
        cy = int(h * float(layer.get('cy_pct', 50.0)) / 100.0)
        radius_pct = max(float(layer.get('radius_pct', 50.0)), 12.0)
        rx = max(int(w * radius_pct / 100.0 * 0.82), 40)
        ry = max(int(h * radius_pct / 100.0 * 0.74), 32)
        blob = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(blob)
        draw.ellipse(
            [cx - rx, cy - ry, cx + rx, cy + ry],
            fill=(r, g, b, int(max(0.0, min(alpha, 1.0)) * 255)),
        )
        blur_radius = max(int(min(rx, ry) * 0.34), 18)
        blob = blob.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        img = Image.alpha_composite(img, blob)

    vignette = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    vignette_draw = ImageDraw.Draw(vignette)
    vignette_draw.ellipse(
        [int(-0.12 * w), int(-0.18 * h), int(1.12 * w), int(1.18 * h)],
        fill=(255, 255, 255, 28),
    )
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius=max(int(min(w, h) * 0.025), 18)))
    img = Image.alpha_composite(img, vignette)

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    pic = slide.shapes.add_picture(buf, Inches(0), Inches(0), Inches(slide_w_in), Inches(slide_h_in))
    sp_tree = slide.shapes._spTree
    sp_tree.remove(pic._element)
    sp_tree.insert(2, pic._element)


def generate_preview_from_pptx(pptx_path: Path) -> Optional[Path]:
    """Generate a preview grid from the saved PPTX using Pillow."""
    try:
        from PIL import Image, ImageDraw, ImageFont
        from pptx import Presentation as _Prs
        from pptx.enum.dml import MSO_FILL
        from pptx.enum.shapes import MSO_SHAPE_TYPE

        prs = _Prs(str(pptx_path))
        THUMB_W = 320
        slides_data = []

        def safe_fill_color(shape):
            try:
                ft = shape.fill.type
                if ft == MSO_FILL.SOLID:
                    return shape.fill.fore_color.rgb
                return None
            except Exception:
                return None

        def get_slide_bg_color(slide):
            try:
                ft = slide.background.fill.type
                if ft == MSO_FILL.SOLID:
                    return slide.background.fill.fore_color.rgb
            except Exception:
                pass
            return None

        for slide in prs.slides:
            slide_w = prs.slide_width
            slide_h = prs.slide_height
            img_h = int(THUMB_W * slide_h / slide_w)

            bg_rgb = get_slide_bg_color(slide)
            if bg_rgb:
                img = Image.new('RGB', (THUMB_W, img_h), bg_rgb)
            else:
                img = Image.new('RGB', (THUMB_W, img_h), (240, 240, 240))
            draw = ImageDraw.Draw(img)

            for shape in slide.shapes:
                try:
                    x = int(shape.left / slide_w * THUMB_W)
                    y = int(shape.top / slide_h * img_h)
                    w = int(shape.width / slide_w * THUMB_W)
                    h = int(shape.height / slide_h * img_h)
                except Exception:
                    continue

                if w < 2 or h < 2:
                    continue

                # Skip tiny nav dots
                if w < 15 and h < 15:
                    continue

                if shape.has_text_frame and shape.text.strip():
                    text_color = (255, 255, 255)
                    try:
                        for para in shape.text_frame.paragraphs:
                            for run in para.runs:
                                if run.font.color and run.font.color.rgb:
                                    text_color = run.font.color.rgb
                                    break
                            if text_color != (255, 255, 255):
                                break
                    except Exception:
                        pass
                    if bg_rgb:
                        luminance = 0.299 * bg_rgb[0] + 0.587 * bg_rgb[1] + 0.114 * bg_rgb[2]
                        text_color = (50, 50, 50) if luminance > 128 else (230, 230, 230)
                    # Show text within bounds, truncate at natural break
                    text = shape.text.strip()
                    max_chars = int(w / 3)  # roughly chars that fit in width
                    if len(text) > max_chars:
                        text = text[:max_chars].rsplit(' ', 1)[0] + '…'
                    draw.text((x + 2, y + 2), text, fill=text_color)
                else:
                    fill = safe_fill_color(shape)
                    if fill:
                        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=fill)
                    # Show empty text box outlines (subtle)
                    elif shape.has_text_frame:
                        draw.rectangle([x, y, x + w - 1, y + h - 1], outline=(80, 80, 80))

            slides_data.append(img)

        if not slides_data:
            return None

        n = len(slides_data)
        th = slides_data[0].height
        PAD = 4
        LABEL_H = 22
        grid_w = n * THUMB_W + (n - 1) * PAD
        grid_h = th + LABEL_H
        grid = Image.new('RGB', (grid_w, grid_h), (32, 32, 32))
        draw = ImageDraw.Draw(grid)

        for j, thumb in enumerate(slides_data):
            x = j * (THUMB_W + PAD)
            grid.paste(thumb, (x, 0))
            draw.text((x + THUMB_W // 2, th + 3), f"Slide {j+1}", fill=(200, 200, 200))

        preview_path = pptx_path.with_name(pptx_path.stem + '-preview.png')
        grid.save(str(preview_path))
        return preview_path
    except Exception as e:
        print(f"  Warning: preview generation failed: {e}")
        return None


def extract_css_from_soup(soup: BeautifulSoup) -> List[CSSRule]:
    """Extract and parse all <style> blocks from the HTML."""
    all_rules = []
    for style_tag in soup.find_all('style'):
        css_text = style_tag.string or ''
        all_rules.extend(parse_css_rules(css_text))
    return all_rules


# ─── Main Export Pipeline ─────────────────────────────────────────────────────

def export_sandbox(html_path, output_path=None, width=1440, height=900, add_chrome: bool = False):
    html_path = Path(html_path).resolve()
    if not html_path.exists():
        print(f"Error: {html_path}")
        sys.exit(1)

    output_path = Path(output_path) if output_path else html_path.with_suffix('.pptx')

    print(f"导出（sandbox, no browser）: {html_path.name}")

    pipeline = build_export_pipeline(html_path, width, height)
    geometry_plans = solve_geometry(pipeline)
    if not geometry_plans:
        print("Nothing to export.")
        return

    render_pptx(geometry_plans, output_path, add_chrome=add_chrome)
    print(f"Saved: {output_path}  ({len(geometry_plans)} 张幻灯片)")

    # Preview
    preview_path = generate_preview_from_pptx(output_path)
    if preview_path:
        print(f"Preview: {preview_path}")

    return output_path


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Export HTML to editable PPTX (no browser required)",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("html", help="Path to HTML file")
    parser.add_argument("output", nargs="?", help="Output .pptx path (default: same name as HTML)")
    parser.add_argument("--width", type=int, default=1440, help="Slide width in pixels (default: 1440)")
    parser.add_argument("--height", type=int, default=900, help="Slide height in pixels (default: 900)")
    parser.add_argument("--with-chrome", action="store_true", help="Add exporter-provided page counter and nav dots")
    args = parser.parse_args()

    export_sandbox(args.html, args.output, args.width, args.height, add_chrome=args.with_chrome)


if __name__ == "__main__":
    main()
