#!/usr/bin/env python3
"""
web_export.py — v3.8 JSON deck → HTML（媲美 Gamma "publish as website"）

每张 slide 一个 <section>，CSS scroll-snap 实现 PPT 浏览体验。
- 用 StylePack 的 palette 注入 CSS variables
- 中文字体 fallback（PingFang SC / Noto Sans CJK SC）
- 反 AI Slop：默认字体 IBM Plex Sans 而非 Inter
- 响应式：桌面全屏 / 移动端可竖向滑动

用法：
    python3 scripts/web_export.py /path/deck.json --pack apple-light \\
        --output ./presentation.html

    # 浏览器打开
    open ./presentation.html
"""

from __future__ import annotations
import argparse
import html
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def get_pack_tokens(pack_name: str | None) -> dict:
    defaults = {
        'bg': '#FFFFFF', 'bg_elevated': '#F5F5F7',
        'text': '#1D1D1F', 'text_sec': '#424245', 'text_muted': '#86868B',
        'accent': '#0071E3', 'border': '#D2D2D7',
        'font_display': 'IBM Plex Sans', 'font_body': 'IBM Plex Sans',
    }
    if not pack_name:
        return defaults
    try:
        from style_packs import REGISTRY
        if pack_name not in REGISTRY:
            return defaults
        p = REGISTRY[pack_name]
        return {
            'bg': p.palette.bg,
            'bg_elevated': p.palette.bg_elevated,
            'text': p.palette.text_primary,
            'text_sec': p.palette.text_secondary,
            'text_muted': getattr(p.palette, 'text_muted', '#86868B'),
            'accent': p.palette.accent,
            'border': p.palette.border,
            'font_display': p.typography.display_font,
            'font_body': p.typography.body_font,
        }
    except Exception:
        return defaults


CSS_TEMPLATE = """\
:root {{
  --bg: {bg};
  --bg-elevated: {bg_elevated};
  --text: {text};
  --text-sec: {text_sec};
  --text-muted: {text_muted};
  --accent: {accent};
  --border: {border};
  --font-display: '{font_display}', 'PingFang SC', 'Heiti SC', 'Noto Sans CJK SC', sans-serif;
  --font-body: '{font_body}', 'PingFang SC', 'Heiti SC', 'Noto Sans CJK SC', sans-serif;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
html, body {{
  background: var(--bg);
  color: var(--text);
  font-family: var(--font-body);
  scroll-behavior: smooth;
  scroll-snap-type: y mandatory;
  overflow-y: scroll;
  height: 100vh;
}}
.slide {{
  height: 100vh;
  scroll-snap-align: start;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 5vw 8vw;
  position: relative;
  border-bottom: 1px solid var(--border);
}}
.slide.cover {{ justify-content: center; align-items: flex-start; }}
.eyebrow {{ font-size: 0.875rem; letter-spacing: 0.15em; text-transform: uppercase;
           color: var(--accent); margin-bottom: 1rem; font-weight: 600; }}
.slide-title {{ font-family: var(--font-display); font-size: clamp(2.5rem, 6vw, 6rem);
                font-weight: 700; line-height: 1.05; letter-spacing: -0.02em;
                color: var(--text); margin-bottom: 1rem; }}
.slide-subtitle {{ font-size: clamp(1rem, 2vw, 1.5rem); color: var(--text-sec);
                   line-height: 1.5; margin-bottom: 2rem; }}
.slide-footnote {{ font-size: 0.875rem; color: var(--text-muted); margin-top: auto; }}
.section-number {{ font-family: var(--font-display); font-size: clamp(4rem, 12vw, 12rem);
                   font-weight: 700; color: var(--accent); line-height: 1; opacity: 0.4; }}
.big-stat-value {{ font-family: var(--font-display);
                   font-size: clamp(6rem, 18vw, 18rem); font-weight: 700;
                   color: var(--accent); line-height: 0.9;
                   letter-spacing: -0.04em; }}
.big-stat-unit {{ font-size: clamp(1.25rem, 2.5vw, 2rem); color: var(--text-sec); margin-top: 1rem; }}
.kpi-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem;
             margin: 2rem 0; }}
.kpi-card {{ padding: 2rem; background: var(--bg-elevated); border-radius: 4px;
             border: 1px solid var(--border); }}
.kpi-value {{ font-family: var(--font-display); font-size: clamp(2.5rem, 5vw, 4rem);
              font-weight: 700; color: var(--accent); }}
.kpi-label {{ font-size: 1rem; color: var(--text); margin-top: 0.5rem; font-weight: 600; }}
.kpi-caption {{ font-size: 0.875rem; color: var(--text-muted); margin-top: 0.25rem; }}
.quote-block {{ font-family: var(--font-display); font-size: clamp(1.5rem, 3vw, 2.5rem);
                font-weight: 500; line-height: 1.4; color: var(--text);
                border-left: 4px solid var(--accent); padding-left: 2rem; }}
.quote-author {{ margin-top: 2rem; font-size: 1rem; color: var(--text-sec); }}
.list-item {{ display: flex; gap: 1.5rem; padding: 1.5rem 0;
              border-bottom: 1px solid var(--border); }}
.list-item-num {{ font-family: var(--font-display); font-size: 2rem; color: var(--accent);
                  font-weight: 700; min-width: 3rem; }}
.list-item-label {{ font-size: 1.25rem; color: var(--text); font-weight: 600; }}
.list-item-desc {{ color: var(--text-sec); margin-top: 0.5rem; }}
.compare {{ display: grid; grid-template-columns: 1fr 1fr; gap: 3rem; margin-top: 2rem; }}
.compare-col {{ padding: 2rem; background: var(--bg-elevated); border-radius: 4px; }}
.compare-label {{ font-size: 0.875rem; color: var(--accent); text-transform: uppercase;
                  letter-spacing: 0.1em; margin-bottom: 1rem; }}
.cta-large {{ display: inline-block; padding: 1rem 2rem; background: var(--accent);
              color: var(--bg); border-radius: 4px; font-weight: 600;
              font-size: 1.25rem; margin-top: 1.5rem; text-decoration: none; }}
.page-num {{ position: absolute; bottom: 2rem; right: 2rem; color: var(--text-muted);
             font-size: 0.875rem; font-variant-numeric: tabular-nums; }}
@media (max-width: 768px) {{
  .kpi-grid {{ grid-template-columns: 1fr; }}
  .compare {{ grid-template-columns: 1fr; gap: 1.5rem; }}
}}
"""


def render_slide(slide: dict, idx: int, total: int) -> str:
    """单 slide → HTML section"""
    t = slide.get('type', '')
    e = lambda s: html.escape(str(s or ''))

    if t == 'hero_cover':
        return f'''<section class="slide cover">
  {f'<div class="eyebrow">{e(slide.get("eyebrow"))}</div>' if slide.get('eyebrow') else ''}
  <h1 class="slide-title">{e(slide.get('title'))}</h1>
  {f'<p class="slide-subtitle">{e(slide.get("subtitle"))}</p>' if slide.get('subtitle') else ''}
  {f'<p class="slide-footnote">{e(slide.get("footnote"))}</p>' if slide.get('footnote') else ''}
  <div class="page-num">{idx} / {total}</div>
</section>'''

    if t == 'section_divider':
        return f'''<section class="slide">
  <div class="section-number">{e(slide.get('number'))}</div>
  <h2 class="slide-title">{e(slide.get('title'))}</h2>
  {f'<p class="slide-subtitle">{e(slide.get("subtitle"))}</p>' if slide.get('subtitle') else ''}
  <div class="page-num">{idx} / {total}</div>
</section>'''

    if t == 'big_stat':
        return f'''<section class="slide">
  {f'<div class="eyebrow">{e(slide.get("caption"))}</div>' if slide.get('caption') else ''}
  <div class="big-stat-value">{e(slide.get('value'))}</div>
  {f'<div class="big-stat-unit">{e(slide.get("unit"))}</div>' if slide.get('unit') else ''}
  {f'<p class="slide-footnote">{e(slide.get("footnote"))}</p>' if slide.get('footnote') else ''}
  <div class="page-num">{idx} / {total}</div>
</section>'''

    if t == 'kpi_triple':
        items = slide.get('items', [])
        cards = '\n'.join(
            f'''  <div class="kpi-card">
    <div class="kpi-value">{e(it.get('value'))}</div>
    <div class="kpi-label">{e(it.get('label'))}</div>
    {f'<div class="kpi-caption">{e(it.get("caption"))}</div>' if it.get('caption') else ''}
  </div>'''
            for it in items
        )
        return f'''<section class="slide">
  <h2 class="slide-title">{e(slide.get('title'))}</h2>
  {f'<div class="eyebrow">{e(slide.get("en_sub"))}</div>' if slide.get('en_sub') else ''}
  <div class="kpi-grid">
{cards}
  </div>
  <div class="page-num">{idx} / {total}</div>
</section>'''

    if t == 'quote_card':
        return f'''<section class="slide">
  <blockquote class="quote-block">"{e(slide.get('quote'))}"</blockquote>
  <p class="quote-author">— {e(slide.get('author'))}{f", {e(slide.get('role'))}" if slide.get('role') else ''}</p>
  <div class="page-num">{idx} / {total}</div>
</section>'''

    if t == 'content_list':
        items = slide.get('items', [])
        rows = '\n'.join(
            f'''  <div class="list-item">
    <div class="list-item-num">{n+1:02d}</div>
    <div>
      <div class="list-item-label">{e(it.get('label'))}</div>
      {f'<div class="list-item-desc">{e(it.get("desc"))}</div>' if it.get('desc') else ''}
    </div>
  </div>'''
            for n, it in enumerate(items)
        )
        return f'''<section class="slide">
  <h2 class="slide-title">{e(slide.get('title'))}</h2>
{rows}
  <div class="page-num">{idx} / {total}</div>
</section>'''

    if t == 'compare_columns':
        left = slide.get('left', {})
        right = slide.get('right', {})
        left_pts = '\n'.join(f'      <li>{e(p)}</li>' for p in left.get('points', []))
        right_pts = '\n'.join(f'      <li>{e(p)}</li>' for p in right.get('points', []))
        return f'''<section class="slide">
  <h2 class="slide-title">{e(slide.get('title'))}</h2>
  <div class="compare">
    <div class="compare-col">
      <div class="compare-label">{e(left.get('label'))}</div>
      <ul>
{left_pts}
      </ul>
    </div>
    <div class="compare-col">
      <div class="compare-label">{e(right.get('label'))}</div>
      <ul>
{right_pts}
      </ul>
    </div>
  </div>
  <div class="page-num">{idx} / {total}</div>
</section>'''

    if t == 'call_to_action':
        cta = slide.get('cta', '')
        cta_el = (f'<a href="https://{cta}" class="cta-large">{e(cta)}</a>'
                  if cta and not cta.startswith(('http', 'mailto:')) else
                  f'<a href="{e(cta)}" class="cta-large">{e(cta)}</a>' if cta else '')
        return f'''<section class="slide">
  <h2 class="slide-title">{e(slide.get('title'))}</h2>
  {f'<p class="slide-subtitle">{e(slide.get("subtitle"))}</p>' if slide.get('subtitle') else ''}
  {cta_el}
  {f'<p class="slide-footnote" style="margin-top: 2rem">{e(slide.get("footnote"))}</p>' if slide.get('footnote') else ''}
  <div class="page-num">{idx} / {total}</div>
</section>'''

    # 兜底：未知 type 用通用 title + content
    return f'''<section class="slide">
  <h2 class="slide-title">{e(slide.get('title') or t)}</h2>
  <pre style="font-family: var(--font-body); white-space: pre-wrap; color: var(--text-sec)">{e(json.dumps(slide, ensure_ascii=False, indent=2))}</pre>
  <div class="page-num">{idx} / {total}</div>
</section>'''


def render_html(deck: dict, pack_name: str | None) -> str:
    tokens = get_pack_tokens(pack_name)
    css = CSS_TEMPLATE.format(**tokens)
    slides = deck.get('slides', [])
    total = len(slides)
    sections = '\n'.join(render_slide(s, i + 1, total) for i, s in enumerate(slides))
    title = ''
    if slides and slides[0].get('type') == 'hero_cover':
        title = slides[0].get('title', '')
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title or '火一五演示稿')}</title>
<style>
{css}
</style>
</head>
<body>
{sections}
</body>
</html>
'''


def main():
    parser = argparse.ArgumentParser(description='火一五 PPT v3.8 Web 导出（scroll-snap HTML）')
    parser.add_argument('deck', help='JSON deck 路径')
    parser.add_argument('--pack', help='style pack 名（决定配色字体）')
    parser.add_argument('--output', '-o', required=True)
    args = parser.parse_args()

    deck = json.loads(Path(args.deck).read_text())
    pack = args.pack or deck.get('pack')
    html_content = render_html(deck, pack)
    Path(args.output).write_text(html_content)
    print(f"  ✅ {args.output} ({len(html_content)} bytes, {len(deck.get('slides', []))} slides)",
          file=sys.stderr)
    print(f"  浏览器打开: open {args.output}", file=sys.stderr)


if __name__ == '__main__':
    main()
