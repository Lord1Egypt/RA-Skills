#!/usr/bin/env python3
"""Macaron Card Generator - Generate beautiful card HTML from text content."""

import argparse
import json
import os
import sys

# ── Macaron colour palette ──────────────────────────────────────────────
PALETTE = {
    "pink":      {"bg": "#FFF0F3", "accent": "#FF8FAB", "text": "#C9184A", "light": "#FFB5C2"},
    "blue":      {"bg": "#F0F4FF", "accent": "#8FC7FF", "text": "#1A56DB", "light": "#B5D8FF"},
    "green":     {"bg": "#F0FFF2", "accent": "#8FD9A5", "text": "#0E6B2E", "light": "#B5E8C3"},
    "yellow":    {"bg": "#FFF9F0", "accent": "#FFD68F", "text": "#B45309", "light": "#FFE5B4"},
    "purple":    {"bg": "#F8F0FF", "accent": "#C2A8FF", "text": "#6D28D9", "light": "#D4BFFF"},
    "orange":    {"bg": "#FFF6F0", "accent": "#FFB88F", "text": "#C2410C", "light": "#FFD1B5"},
    "mint":      {"bg": "#F0FFFB", "accent": "#8FD5CE", "text": "#0F766E", "light": "#B5E5E0"},
    "lavender":  {"bg": "#F5F0FF", "accent": "#D4BFFF", "text": "#7C3AED", "light": "#E8D5FF"},
}

# ── Aspect ratio to viewport size mapping ───────────────────────────────
RATIOS = {
    "1:1":   (800, 800),
    "3:4":   (750, 1000),
    "4:3":   (1000, 750),
    "9:16":  (720, 1280),
    "16:9":  (1280, 720),
    "2:3":   (700, 1050),
}


def pick_palette(card_type, idx=0):
    """Pick a macaron palette based on card type."""
    map_ = {
        "book":      ["mint", "blue", "pink"],
        "concept":   ["purple", "lavender", "blue"],
        "quote":     ["pink", "orange", "purple"],
        "compare":   ["blue", "mint", "green"],
        "chapter":   ["yellow", "orange", "pink"],
        "character": ["lavender", "purple", "pink"],
    }
    keys = map_.get(card_type, list(PALETTE.keys()))
    return keys[idx % len(keys)], PALETTE[keys[idx % len(keys)]]


def css_decorations():
    """Return shared CSS for cartoon-style decorations."""
    return """
/* ── Decorative elements ── */
.deco-circle {
    position: absolute;
    border-radius: 50%;
    opacity: 0.35;
    pointer-events: none;
}
.deco-dot {
    position: absolute;
    border-radius: 50%;
    opacity: 0.25;
    pointer-events: none;
}
.deco-star {
    position: absolute;
    opacity: 0.3;
    pointer-events: none;
    font-size: 28px;
}
.deco-wavy {
    position: absolute;
    opacity: 0.2;
    pointer-events: none;
    border: 3px dashed currentColor;
    border-radius: 50%;
}
"""


def base_html(title, body_html, w, h, colors, extra_css=""):
    """Wrap content in a full HTML page with macaron cartoon styling."""
    name, c = colors
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={w}, height={h}">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    width: {w}px;
    height: {h}px;
    overflow: hidden;
    font-family: 'PingFang SC', 'Microsoft YaHei', 'Noto Sans SC', sans-serif;
    background: {c['bg']};
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}}

/* ── Macaron card container ── */
.card {{
    position: relative;
    width: 88%;
    max-height: 90%;
    background: #ffffff;
    border-radius: 32px;
    padding: 48px 40px;
    box-shadow:
        0 8px 32px rgba(0,0,0,0.06),
        0 2px 8px rgba(0,0,0,0.04);
    border: 3px solid {c['light']};
    overflow-y: auto;
}}
.card::after {{
    content: '';
    position: absolute;
    inset: 6px;
    border: 2px dashed {c['light']};
    border-radius: 26px;
    pointer-events: none;
    opacity: 0.6;
}}

{css_decorations()}
{extra_css}

/* ── Typography ── */
.card-title {{
    font-size: 42px;
    font-weight: 800;
    color: {c['text']};
    text-align: center;
    margin-bottom: 8px;
    letter-spacing: 2px;
}}
.card-subtitle {{
    font-size: 20px;
    color: {c['accent']};
    text-align: center;
    margin-bottom: 32px;
    font-weight: 500;
    letter-spacing: 4px;
}}
.card-body {{
    font-size: 20px;
    color: #374151;
    line-height: 1.8;
}}
.tag {{
    display: inline-block;
    background: {c['bg']};
    color: {c['text']};
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 16px;
    font-weight: 600;
    margin: 4px 6px;
    border: 1.5px solid {c['light']};
}}
</style>
</head>
<body>
<!-- Background decorations -->
<div class="deco-circle" style="top:-60px;right:-40px;width:160px;height:160px;background:{c['light']};"></div>
<div class="deco-circle" style="bottom:-50px;left:-30px;width:120px;height:120px;background:{c['accent']};opacity:0.2;"></div>
<div class="deco-dot" style="top:40px;left:30px;width:18px;height:18px;background:{c['accent']};"></div>
<div class="deco-dot" style="bottom:80px;right:40px;width:14px;height:14px;background:{c['light']};"></div>
<div class="deco-dot" style="top:120px;right:50px;width:10px;height:10px;background:{c['accent']};opacity:0.5;"></div>
<div class="deco-star" style="top:50px;right:60px;color:{c['accent']};">✦</div>
<div class="deco-star" style="bottom:100px;left:50px;color:{c['light']};">✦</div>
<div class="deco-wavy" style="top:30px;left:80px;width:60px;height:60px;color:{c['accent']};"></div>

<div class="card">
    <div class="card-title">{title}</div>
    {body_html}
</div>
</body>
</html>"""


# ── Card type builders ──────────────────────────────────────────────────

def build_book_card(data):
    """Build a book recommendation card."""
    colors = pick_palette("book")
    title = data.get("title", "Book Recommendation")
    author = data.get("author", "")
    cover_desc = data.get("cover_description", "A heartwarming and healing book")
    reason = data.get("recommendation_reason", "")
    rating = data.get("rating", "")
    takeaway = data.get("key_takeaway", "")
    tags = data.get("tags", [])

    rating_html = ""
    if rating:
        stars = "⭐" * int(float(rating)) if rating.replace('.','').isdigit() else rating
        rating_html = f'<div style="text-align:center;font-size:28px;margin-bottom:16px;letter-spacing:4px;">{stars}</div>'

    tags_html = ""
    if tags:
        tags_html = '<div style="text-align:center;margin-top:16px;">' + \
            ''.join(f'<span class="tag">{t}</span>' for t in tags) + '</div>'

    body = f"""
    <div class="card-subtitle">{author}</div>
    {rating_html}
    <div style="text-align:center;margin-bottom:24px;">
        <div style="display:inline-block;background:{colors[1]['bg']};border-radius:20px;padding:20px 30px;
            border:2px dashed {colors[1]['light']};font-size:18px;color:#6B7280;max-width:500px;">
            📖 {cover_desc}
        </div>
    </div>
    <div class="card-body">
        {('<p style="margin-bottom:12px;"><strong>💡 Reason to read：</strong>' + reason + '</p>') if reason else ''}
        {('<p><strong>📝 Key takeaway：</strong>' + takeaway + '</p>') if takeaway else ''}
    </div>
    {tags_html}
    """
    return base_html(title, body, *size_from_ratio(data.get("ratio", "3:4")), colors)


def build_concept_card(data):
    """Build a concept explanation card."""
    colors = pick_palette("concept")
    name = data.get("concept_name", "Core Concept")
    definition = data.get("definition", "")
    examples = data.get("examples", [])
    related = data.get("related_concepts", [])

    examples_html = ""
    if examples:
        items = ''.join(f'<li style="margin-bottom:8px;">💡 {e}</li>' for e in examples)
        examples_html = f'<div style="margin-top:16px;"><strong>Examples：</strong><ul style="padding-left:20px;margin-top:8px;">{items}</ul></div>'

    related_html = ""
    if related:
        tags = ''.join(f'<span class="tag">{r}</span>' for r in related)
        related_html = f'<div style="text-align:center;margin-top:20px;">{tags}</div>'

    body = f"""
    <div class="card-subtitle">Knowledge Card · Understand at a Glance</div>
    <div class="card-body">
        <p style="font-size:22px;margin-bottom:20px;text-align:center;color:{colors[1]['accent']};font-weight:600;">
            {definition}
        </p>
        {examples_html}
    </div>
    {related_html}
    """
    return base_html(name, body, *size_from_ratio(data.get("ratio", "3:4")), colors)


def build_quote_card(data):
    """Build a quote card."""
    colors = pick_palette("quote")
    quote = data.get("quote_text", "")
    author = data.get("author", "")
    source = data.get("source", "")
    context = data.get("context", "")

    body = f"""
    <div style="text-align:center;margin:20px 0;">
        <span style="font-size:80px;color:{colors[1]['accent']};opacity:0.4;line-height:0;">&ldquo;</span>
        <p style="font-size:30px;line-height:1.6;color:{colors[1]['text']};font-weight:600;margin:20px 0;">
            {quote}
        </p>
        <span style="font-size:80px;color:{colors[1]['accent']};opacity:0.4;line-height:0;">&rdquo;</span>
    </div>
    <div style="text-align:center;margin-top:24px;">
        <p style="font-size:22px;color:{colors[1]['accent']};font-weight:700;">{author}</p>
        {('<p style="font-size:16px;color:#9CA3AF;margin-top:4px;">' + source + '</p>') if source else ''}
    </div>
    {('<div style="text-align:center;margin-top:20px;font-size:16px;color:#6B7280;background:' + colors[1]['bg'] + ';padding:16px;border-radius:16px;">' + context + '</div>') if context else ''}
    """
    return base_html("✨ Quote of the Day", body, *size_from_ratio(data.get("ratio", "3:4")), colors)


def build_compare_card(data):
    """Build a comparison card."""
    colors = pick_palette("compare")
    topic = data.get("topic", "Comparison Analysis")
    left_label = data.get("left_label", "A")
    left_items = data.get("left_items", [])
    right_label = data.get("right_label", "B")
    right_items = data.get("right_items", [])
    conclusion = data.get("conclusion", "")

    def items_html(items):
        return ''.join(f'<p style="margin:10px 0;font-size:17px;">• {item}</p>' for item in items)

    body = f"""
    <div class="card-subtitle">Understand at a Glance · No More Dilemma</div>
    <div style="display:flex;gap:24px;margin-top:8px;">
        <div style="flex:1;background:{colors[1]['bg']};border-radius:20px;padding:24px;
            border:2px solid {colors[1]['light']};text-align:center;">
            <p style="font-size:24px;font-weight:800;color:{colors[1]['accent']};margin-bottom:16px;">{left_label}</p>
            {items_html(left_items)}
        </div>
        <div style="flex:1;background:{colors[1]['bg']};border-radius:20px;padding:24px;
            border:2px solid {colors[1]['light']};text-align:center;">
            <p style="font-size:24px;font-weight:800;color:{colors[1]['accent']};margin-bottom:16px;">{right_label}</p>
            {items_html(right_items)}
        </div>
    </div>
    {('<div style="text-align:center;margin-top:24px;font-size:18px;color:' + colors[1]['text'] + ';font-weight:600;background:' + colors[1]['bg'] + ';padding:18px;border-radius:16px;">💡 {conclusion}</div>') if conclusion else ''}
    """
    return base_html(topic, body, *size_from_ratio(data.get("ratio", "3:4")), colors)


def size_from_ratio(ratio_str):
    """Convert ratio string to (width, height) tuple."""
    return RATIOS.get(ratio_str, RATIOS["3:4"])


BUILDERS = {
    "book":      build_book_card,
    "concept":   build_concept_card,
    "quote":     build_quote_card,
    "compare":   build_compare_card,
}


def main():
    parser = argparse.ArgumentParser(description="Generate Macaron Card HTML")
    parser.add_argument("--type", required=True, choices=list(BUILDERS.keys()),
                        help="Card type")
    parser.add_argument("--content", default="{}",
                        help="JSON string with card content data")
    parser.add_argument("--output", required=True,
                        help="Output HTML file path")
    args = parser.parse_args()

    try:
        content = json.loads(args.content)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON content: {e}", file=sys.stderr)
        sys.exit(1)

    builder = BUILDERS[args.type]
    html = builder(content)

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Generated: {args.output}")
    print(f"   Type: {args.type}")
    w, h = size_from_ratio(content.get("ratio", "3:4"))
    print(f"   Size: {w}×{h}")


if __name__ == "__main__":
    main()