#!/usr/bin/env python3
"""
build_html.py - data.json + template → self-contained HTML
Usage: python build_html.py <data.json> <output.html> [--template template.html] [--pixel-font pixel-font.js] [--echarts echarts.js]

Reads:
  - data.json:  all numeric/text data (per data contract spec)
  - template.html:  stable skeleton with __PLACEHOLDER__ tokens
  - pixel-font.js:  A-Z+0-9 pixel font (injected inline)
  - echarts.5.5.0.min.js:  ECharts library (injected inline)

Writes:
  - output.html:  self-contained, offline-ready HTML
"""
import json, sys, os, re, pathlib, argparse, math

def hex_to_rgb(h):
    """#76b900 → (118, 185, 0)"""
    h = h.lstrip('#')
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

def rgba(hex_color, alpha):
    """#76b900, 0.18 → 'rgba(118,185,0,.18)'"""
    r, g, b = hex_to_rgb(hex_color)
    # Use short alpha format (.18 instead of 0.18) to match original
    a_str = str(alpha)
    if a_str.startswith('0.'):
        a_str = a_str[1:]
    return f'rgba({r},{g},{b},{a_str})'

def rgb_str(hex_color):
    """#76b900 → '118,185,0'"""
    r, g, b = hex_to_rgb(hex_color)
    return f'{r},{g},{b}'

def js_val(v):
    """Python value → JS literal string (JSON-compatible, no ASCII escaping)"""
    return json.dumps(v, ensure_ascii=False)

def calc_pixel_x(text, scale, canvas_width=64):
    """Calculate x position to center text on canvas.
    Uses same advance logic as the text() function: i * (glyph_width + 1) * sc.
    For variable-width fonts, uses average width as approximation."""
    if not text:
        return canvas_width / 2
    # Approximate: average glyph width is ~3.5, advance = 4.5
    # Total width ≈ len(text) * 4.5 * scale - 1 * scale (last char doesn't need trailing space)
    avg_advance = 4.5
    total_width = len(text) * avg_advance * scale - scale
    x = (canvas_width - total_width) / 2
    return round(x, 1)

def calc_kline_yrange(prices, focus=False):
    """Calculate K-line y-axis range from price data.
    Floors min to nearest standard tick, ceilings max to nearest tick."""
    if not prices:
        return (0.01, 100)
    pmin = min(prices)
    pmax = max(prices)
    # Downward ticks (yMin)
    down_ticks = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1, 2, 5, 10, 20, 50]
    # Upward ticks (yMax)
    up_ticks = [50, 100, 200, 400, 800, 1600, 3200]

    # Find appropriate yMin (≤ pmin * 0.7 to give some padding)
    ymin = down_ticks[0]
    for t in down_ticks:
        if t <= pmin * 0.7:
            ymin = t
        else:
            break

    # Find appropriate yMax (≥ pmax * 1.3 to give some padding)
    ymax = up_ticks[-1]
    for t in up_ticks:
        if t >= pmax * 1.2:
            ymax = t
            break

    return (ymin, ymax)

def generate_data_block(data):
    """Generate the JS data block from data.json"""
    lines = ['/* ================= 数据 ================= */']
    lines.append('// 稀疏史前点（拆股复权近似，不连线）：[日期, 价格, 标签]')
    lines.append(f'var PRE = {js_val(data["pre"])};')
    lines.append('// 早期月线收盘：[日期, 收盘]')
    lines.append(f'var CLOSES = {js_val(data["closes"])};')
    lines.append('// 月线 K：[日期, 开, 收, 低, 高]')
    lines.append(f'var CANDLES = {js_val(data["candles"])};')
    lines.append('// K线事件标注')
    lines.append(f'var EVENTS = {js_val(data["events"])};')
    lines.append('// 财务（真实财季）：[季, 营收(亿$), 净利(亿$), 毛利率%]')
    lines.append(f'var FIN = {js_val(data["fin"])};')
    lines.append('// 分部（财年，亿$）')
    lines.append(f'var SEG = {js_val(data["seg"])};')
    lines.append('// 高频·需求')
    lines.append(f'var HF = {js_val(data["hf"])};')
    lines.append('// 库存（财季）')
    lines.append(f'var INV = {js_val(data["inv"])};')
    lines.append('// 格局墙')
    lines.append(f'var WALL = {js_val(data["wall"])};')
    lines.append(f'var FATE_CLASS = {js_val(data["fateClass"])};')
    lines.append('// 类比打分卡')
    lines.append(f'var SCORES = {js_val(data["scores"])};')
    lines.append(f'var EXCLUDED = {js_val(data["excluded"])};')
    lines.append('// 雷达')
    lines.append(f'var RADAR = {js_val(data["radar"])};')
    if 'radarLabels' in data:
        lines.append(f'var RADAR_LABELS = {js_val(data["radarLabels"])};')
    lines.append('// 时钟')
    lines.append(f'var STAGES = {js_val(data["stages"])};')
    lines.append(f'var CLOCK = {js_val(data["clock"])};')
    lines.append('// 八信号')
    lines.append(f'var SIGNALS = {js_val(data["signals"])};')
    lines.append('// 步骤元数据')
    lines.append(f'var STEP_META = {js_val(data["stepMeta"])};')
    return '\n'.join(lines)

def generate_step_html(step):
    """Generate HTML for a single step section"""
    html = f'    <section class="step" id="{step["id"]}" data-vp="{step["vp"]}"'
    if step.get('state'):
        html += f' data-state="{step["state"]}"'
    html += '>\n'
    html += f'      <div class="step-tag"><span class="bar"></span>{step["tag"]}</div>\n'
    html += f'      <h2>{step["h2"]}</h2>\n'
    for p in step.get('paragraphs', []):
        html += f'      <p>{p}</p>\n'
    fig = step.get('figure')
    if fig and fig.get('src'):
        html += '      <figure>\n'
        html += f'        <img src="{fig["src"]}" alt="{fig.get("alt", "")}" loading="lazy">\n'
        html += f'        <figcaption>{fig.get("caption", "")}</figcaption>\n'
        html += '      </figure>\n'
    html += '    </section>\n'
    return html

def generate_meta_row_html(meta_items):
    """Generate meta row HTML from data"""
    parts = []
    for item in meta_items:
        cls = item.get('cls', '')
        if cls == 'pos':
            parts.append(f'      <span class="pos">{item.get("tail", "")}</span>')
        else:
            label = item.get('label', '')
            value = item.get('value', '')
            tail = item.get('tail', '')
            inner = label
            if value:
                inner += f'<b>{value}</b>'
            inner += tail
            parts.append(f'      <span>{inner}</span>')
    return '\n'.join(parts)

def generate_wall_buttons_html(wall_data):
    """Generate wall wave buttons from WALL data"""
    parts = []
    wave_keys = [k for k in wall_data.keys() if k.startswith('w')]
    for i, k in enumerate(wave_keys):
        cls = 'wbtn seg act' if i == 0 else 'wbtn seg'
        # Use a generic label if available
        parts.append(f'            <button class="{cls}" data-wave="{k}">第{i+1}波</button>')
    return '\n'.join(parts)

def generate_footgrid_html(footgrid):
    """Generate footgrid HTML"""
    parts = []
    for fc in footgrid:
        parts.append(f'    <div class="fc"><b>{fc["title"]}</b>{fc["body"]}</div>')
    return '\n'.join(parts)

def build_html(data, template_html, font_js, echarts_js):
    """Main build function: replace all placeholders in template"""

    brand = data.get('brand', {})
    green = brand.get('green', '#76b900')
    green_d = brand.get('greenD', '#5a9200')

    # —— Derive brand-color JS values ——
    green_js = f"'{green}'"
    area_js = f"'{rgba(green, 0.18)}'"
    pixel_bottom_color = f"'{rgba(green, 0.9)}'"
    led_glow = f"'rgba({rgb_str(green)},'+glow.toFixed(3)+')'"
    particle_color = f"'{rgb_str(green)}'"
    filler_color = f"'{rgba(green, 0.18)}'"

    # —— Pixel text positions ——
    pixel_top = brand.get('pixelTextTop', 'RTX')
    pixel_bottom = brand.get('pixelTextBottom', 'NVIDIA')
    # Use provided positions or auto-calculate
    pixel_top_x = brand.get('pixelTopX', calc_pixel_x(pixel_top, 0.85))
    pixel_bottom_x = brand.get('pixelBottomX', calc_pixel_x(pixel_bottom, 0.62))

    # —— K-line ranges ——
    kline = data.get('kline', {})
    if 'yMin' in kline:
        kline_ymin = kline['yMin']
        kline_ymax = kline['yMax']
    else:
        # Auto-calculate from price data
        all_prices = [p[1] for p in data.get('pre', [])]
        all_prices += [c[1] for c in data.get('closes', [])]
        for cd in data.get('candles', []):
            all_prices.extend([cd[1], cd[2], cd[3], cd[4]])
        kline_ymin, kline_ymax = calc_kline_yrange(all_prices)

    if 'focusYMin' in kline:
        focus_ymin = kline['focusYMin']
        focus_ymax = kline['focusYMax']
    else:
        # Auto-calculate from focus range data
        fr = kline.get('focusRange', ['2016-12', '2023-06'])
        focus_prices = []
        for cd in data.get('candles', []):
            if fr[0] <= cd[0] <= fr[1]:
                focus_prices.extend([cd[1], cd[2], cd[3], cd[4]])
        if focus_prices:
            focus_ymin, focus_ymax = calc_kline_yrange(focus_prices, focus=True)
        else:
            focus_ymin, focus_ymax = 0.5, 70

    focus_range = kline.get('focusRange', ['2016-12', '2023-06'])
    focus_range_js = f"'{focus_range[0]}','{focus_range[1]}'"

    # —— Markpoints ——
    fin_mp = data.get('finMarkpoints', [])
    inv_mp = data.get('invMarkpoints', [])

    # —— K-line markArea ——
    markarea = kline.get('markArea', [])
    markarea_js = js_val(markarea) if markarea else '[]'

    # —— K-line foot HTML ——
    kline_foot = kline.get('footHtml', '')
    kline_foot_js = js_val(kline_foot)

    # —— Build replacements dict ——
    repl = {
        # CSS / brand
        '__TITLE__': data.get('title', '产业周期 Scrollytelling 复盘'),
        '__BRAND_GREEN__': green,
        '__BRAND_GREEN_D__': green_d,
        # Hero
        '__HERO_KICKER__': data.get('hero', {}).get('kicker', ''),
        '__HERO_H1_PREFIX__': data.get('hero', {}).get('h1Prefix', ''),
        '__HERO_H1_EM__': data.get('hero', {}).get('h1Em', ''),
        '__HERO_THESIS__': data.get('hero', {}).get('thesis', ''),
        '__META_ROW_HTML__': generate_meta_row_html(data.get('hero', {}).get('metaRow', [])),
        '__VIZ_NOTE__': data.get('vizNote', f'数据截至 {data.get("asOf", "")}'),
        # vp-foots
        '__VPFOOT_FIN__': data.get('vpFoots', {}).get('fin', ''),
        '__VPFOOT_SEG__': data.get('vpFoots', {}).get('seg', ''),
        '__VPFOOT_WALL__': data.get('vpFoots', {}).get('wall', ''),
        '__VPFOOT_HF__': data.get('vpFoots', {}).get('hf', ''),
        '__VPFOOT_INV__': data.get('vpFoots', {}).get('inv', ''),
        '__VPFOOT_SCORE__': data.get('vpFoots', {}).get('score', ''),
        '__VPFOOT_SIGNAL__': data.get('vpFoots', {}).get('signal', ''),
        # Wall
        '__WALL_WAVE_BUTTONS__': generate_wall_buttons_html(data.get('wall', {})),
        '__WALL_EMPTY_FALLBACK__': js_val(data.get('wallEmptyFallback', '该结局在当前波次为空。')),
        '__WALL_W1_LABEL__': js_val(data.get('wallLabels', {}).get('w1', '第一波')),
        '__WALL_W2_LABEL__': js_val(data.get('wallLabels', {}).get('w2', '第二波')),
        # Steps
        **{f'__STEP_{i+1}_HTML__': generate_step_html(s) for i, s in enumerate(data.get('steps', []))},
        # Outro
        '__OUTRO_H2__': data.get('outro', {}).get('h2', ''),
        '__OUTRO_P__': data.get('outro', {}).get('p', ''),
        '__OUTRO_VERDICT__': data.get('outro', {}).get('verdict', ''),
        '__FOOTGRID_HTML__': generate_footgrid_html(data.get('outro', {}).get('footgrid', [])),
        '__FOOTER__': data.get('footer', ''),
        # Clock
        '__CLOCK_CENTER_TEXT__': js_val(data.get('clockCenterText', data.get('quarter', ''))),
        # JS brand color derivatives
        '__BRAND_GREEN_JS__': green_js,
        '__BRAND_AREA_JS__': area_js,
        '__PIXEL_BOTTOM_COLOR_JS__': pixel_bottom_color,
        '__LED_GLOW_JS__': led_glow,
        '__PARTICLE_COLOR_JS__': particle_color,
        '__FILLER_COLOR_JS__': filler_color,
        # Pixel text
        '__PIXEL_TEXT_TOP__': js_val(pixel_top),
        '__PIXEL_TEXT_BOTTOM__': js_val(pixel_bottom),
        '__PIXEL_TOP_X__': str(pixel_top_x),
        '__PIXEL_BOTTOM_X__': str(pixel_bottom_x),
        # K-line
        '__KLINE_YMIN__': str(kline_ymin),
        '__KLINE_YMAX__': str(kline_ymax),
        '__KLINE_FOCUS_YMIN__': str(focus_ymin),
        '__KLINE_FOCUS_YMAX__': str(focus_ymax),
        '__KLINE_FOCUS_RANGE__': focus_range_js,
        '__KLINE_MARKAREA__': markarea_js,
        '__KLINE_FOOT_HTML__': kline_foot_js,
        # Markpoints
        '__FIN_MARKPOINTS__': js_val(fin_mp) if fin_mp else '[]',
        '__INV_MARKPOINTS__': js_val(inv_mp) if inv_mp else '[]',
        # Inline assets
        '__ECHARTS_INLINE__': echarts_js,
        '__FONT_BLOCK__': font_js,
        '__DATA_BLOCK__': generate_data_block(data),
    }

    # —— Apply replacements ——
    result = template_html
    for placeholder, value in repl.items():
        result = result.replace(placeholder, value)

    # —— Fill empty step placeholders (if fewer than 10 steps) ——
    for i in range(10):
        placeholder = f'__STEP_{i+1}_HTML__'
        if placeholder in result:
            result = result.replace(placeholder, '')

    return result

def main():
    parser = argparse.ArgumentParser(description='Build self-contained HTML from data.json + template')
    parser.add_argument('data_json', help='Path to data.json')
    parser.add_argument('output_html', help='Path to output HTML')
    parser.add_argument('--template', default=None, help='Path to template.html')
    parser.add_argument('--pixel-font', default=None, help='Path to pixel-font.js')
    parser.add_argument('--echarts', default=None, help='Path to echarts.5.5.0.min.js')
    args = parser.parse_args()

    # Resolve default paths
    script_dir = pathlib.Path(__file__).parent.parent
    template_path = pathlib.Path(args.template) if args.template else script_dir / 'template' / 'template.html'
    font_path = pathlib.Path(args.pixel_font) if args.pixel_font else script_dir / 'template' / 'pixel-font.js'
    echarts_path = pathlib.Path(args.echarts) if args.echarts else script_dir / 'template' / 'echarts.5.5.0.min.js'

    # Read inputs
    print(f"[1/4] Reading data: {args.data_json}")
    data = json.loads(pathlib.Path(args.data_json).read_text(encoding='utf-8'))
    print(f"      {len(data)} top-level keys")

    print(f"[2/4] Reading template: {template_path}")
    template_html = template_path.read_text(encoding='utf-8')
    print(f"      {len(template_html):,} chars")

    print(f"[3/4] Reading assets:")
    font_js = font_path.read_text(encoding='utf-8')
    print(f"      pixel-font.js: {len(font_js):,} chars")
    echarts_js = echarts_path.read_text(encoding='utf-8')
    print(f"      echarts.js: {len(echarts_js):,} chars")

    # Build
    print(f"[4/4] Building HTML...")
    html = build_html(data, template_html, font_js, echarts_js)

    # Write output
    out_path = pathlib.Path(args.output_html)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(html, encoding='utf-8')
    size_mb = out_path.stat().st_size / 1024 / 1024
    print(f"\n✓ Output: {out_path} ({size_mb:.2f} MB)")

    # Check for unreplaced placeholders
    remaining = re.findall(r'__[A-Z_]+__', html)
    if remaining:
        print(f"\n⚠ Warning: {len(set(remaining))} unreplaced placeholders:")
        for p in sorted(set(remaining)):
            print(f"  {p}")
    else:
        print("\n✓ All placeholders replaced successfully")

if __name__ == '__main__':
    main()
