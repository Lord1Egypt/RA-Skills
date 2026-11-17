#!/usr/bin/env python3
"""
extract_nvidia_data.py - Extract data + images from original NVIDIA HTML → nvidia_data.json + nvidia_images.json
Usage: python extract_nvidia_data.py <original.html> <output_dir>

Both arguments are required. Example:
  python extract_nvidia_data.py path/to/nvidia.html ./references
"""
import json, re, sys, os, pathlib

def main():
    if len(sys.argv) < 3:
        print("Error: both <original.html> and <output_dir> are required.", file=sys.stderr)
        print("Usage: python extract_nvidia_data.py <original.html> <output_dir>", file=sys.stderr)
        sys.exit(1)
    src = sys.argv[1]
    out_dir = pathlib.Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)

    html = pathlib.Path(src).read_text(encoding='utf-8')
    print(f"[1/4] Read {len(html):,} chars from {src}")

    # —— Extract base64 images ——
    # Pattern: <img src="data:image/jpeg;base64,XXXX" ...>
    img_pattern = re.compile(r'<img\s+src="(data:image/[^"]+)"\s+alt="([^"]*)"[^>]*>', re.S)
    img_matches = img_pattern.findall(html)
    print(f"[2/4] Found {len(img_matches)} base64 images")

    # Also extract figcaption for each
    fig_pattern = re.compile(r'<img\s+src="data:image/[^"]+"\s+alt="([^"]*)"[^>]*>\s*<figcaption>(.*?)</figcaption>', re.S)
    fig_matches = fig_pattern.findall(html)

    images = {}
    for i, (alt, caption) in enumerate(fig_matches):
        # Find the corresponding base64
        for src_data, alt2 in img_matches:
            if alt2 == alt:
                images[f"fig_{i+1}"] = {
                    "alt": alt,
                    "caption": caption.strip(),
                    "src": src_data
                }
                break

    # Save images separately (large file)
    img_out = out_dir / "nvidia_images.json"
    with open(img_out, 'w', encoding='utf-8') as f:
        json.dump(images, f, ensure_ascii=False, indent=2)
    print(f"      → {img_out} ({sum(len(v['src']) for v in images.values()):,} chars of base64)")

    # —— Extract data arrays from inline JS ——
    # Use balanced bracket matching for ALL variables (handles nested arrays)
    def extract_balanced(name, html):
        """Extract any var value by finding balanced brackets"""
        pattern = rf'var\s+{name}\s*=\s*'
        m = re.search(pattern, html)
        if not m:
            return None
        start = m.end()
        # Skip whitespace to find first bracket
        i = start
        while i < len(html) and html[i] in ' \t\n\r':
            i += 1
        if i >= len(html) or html[i] not in '[{':
            return None
        open_char = html[i]
        close_char = ']' if open_char == '[' else '}'
        depth = 0
        in_string = False
        string_char = None
        while i < len(html):
            c = html[i]
            if in_string:
                if c == '\\':
                    i += 2
                    continue
                if c == string_char:
                    in_string = False
            else:
                if c in ('"', "'"):
                    in_string = True
                    string_char = c
                elif c == '[' or c == '{':
                    depth += 1
                elif c == ']' or c == '}':
                    depth -= 1
                    if depth == 0:
                        return html[start:i+1]
            i += 1
        return None

    # For arrays/objects, try to parse as JSON (after fixing JS→JSON)
    def js_to_json(js_str):
        """Convert JS literal to valid JSON for parsing.
        Careful: don't touch single quotes inside double-quoted strings."""
        # Remove comments (only outside strings — simple heuristic: line comments)
        # We'll process char by char to be safe
        result = []
        i = 0
        in_string = False
        string_char = None
        n = len(js_str)
        while i < n:
            c = js_str[i]
            if in_string:
                if c == '\\':
                    result.append(c)
                    if i+1 < n:
                        result.append(js_str[i+1])
                        i += 2
                        continue
                elif c == string_char:
                    in_string = False
                result.append(c)
            else:
                # Check for line comment
                if c == '/' and i+1 < n and js_str[i+1] == '/':
                    # Skip to end of line
                    while i < n and js_str[i] != '\n':
                        i += 1
                    continue
                # Check for block comment
                if c == '/' and i+1 < n and js_str[i+1] == '*':
                    i += 2
                    while i+1 < n and not (js_str[i] == '*' and js_str[i+1] == '/'):
                        i += 1
                    i += 2
                    continue
                if c in ('"', "'"):
                    in_string = True
                    string_char = c
                    # Convert single-quoted strings to double-quoted
                    if c == "'":
                        result.append('"')
                    else:
                        result.append(c)
                else:
                    result.append(c)
            i += 1
        js_str = ''.join(result)

        # Remove trailing commas (outside strings — safe now since comments are gone)
        js_str = re.sub(r',(\s*[}\]])', r'\1', js_str)
        # Quote unquoted keys: {key: → {"key": and , key: → , "key":
        # Only match word chars followed by colon, preceded by { or , (with optional whitespace)
        js_str = re.sub(r'([{,]\s*)([a-zA-Z_]\w*)\s*:', r'\1"\2":', js_str)
        return js_str

    data = {}

    # All variables to extract
    all_vars = [
        ('PRE', 'pre'),
        ('CLOSES', 'closes'),
        ('CANDLES', 'candles'),
        ('EVENTS', 'events'),
        ('FIN', 'fin'),
        ('INV', 'inv'),
        ('SEG', 'seg'),
        ('HF', 'hf'),
        ('WALL', 'wall'),
        ('FATE_CLASS', 'fateClass'),
        ('RADAR', 'radar'),
        ('STAGES', 'stages'),
        ('SCORES', 'scores'),
        ('EXCLUDED', 'excluded'),
        ('CLOCK', 'clock'),
        ('SIGNALS', 'signals'),
        ('STEP_META', 'stepMeta'),
    ]

    for js_name, json_key in all_vars:
        raw = extract_balanced(js_name, html)
        if raw:
            try:
                parsed = json.loads(js_to_json(raw))
                data[json_key] = parsed
                count = len(parsed) if isinstance(parsed, (list, dict)) else '?'
                print(f"      ✓ {js_name}: {count} items")
            except Exception as e:
                print(f"      ✗ {js_name}: parse error: {e}")
                debug_path = out_dir / f"_debug_{js_name}.txt"
                debug_path.write_text(raw, encoding='utf-8')
                print(f"        (raw saved to {debug_path})")

    # —— Extract text content from HTML ——
    # Hero
    hero = {}
    m = re.search(r'<div class="kicker">(.*?)</div>', html)
    if m: hero['kicker'] = m.group(1).strip()
    m = re.search(r'<h1>(.*?)<em>(.*?)</em></h1>', html)
    if m:
        hero['h1Prefix'] = m.group(1).strip()
        hero['h1Em'] = m.group(2).strip()
    m = re.search(r'<p class="thesis">(.*?)</p>', html, re.S)
    if m: hero['thesis'] = m.group(1).strip()
    # Meta row
    m = re.search(r'<div class="meta-row">(.*?)</div>', html, re.S)
    if m:
        meta_html = m.group(1)
        meta_items = []
        for sm in re.finditer(r'<span>(.*?)(?:<b>(.*?)</b>)?(.*?)</span>', meta_html, re.S):
            label = sm.group(1).strip()
            value = sm.group(2).strip() if sm.group(2) else ''
            tail = sm.group(3).strip()
            meta_items.append({"label": label, "value": value, "tail": tail})
        # Also handle <span class="pos"> items
        for sm in re.finditer(r'<span class="pos">(.*?)</span>', meta_html):
            meta_items.append({"label": "", "value": "", "tail": sm.group(1).strip(), "cls": "pos"})
        hero['metaRow'] = meta_items
    data['hero'] = hero

    # Steps
    steps = []
    step_pattern = re.compile(r'<section class="step" id="(s\d+)" data-vp="([^"]+)"(?: data-state="([^"]+)")?>(.*?)</section>', re.S)
    for sm in step_pattern.finditer(html):
        step_id = sm.group(1)
        vp = sm.group(2)
        state = sm.group(3) or ''
        content = sm.group(4)

        # Tag
        tag_m = re.search(r'<div class="step-tag">.*?<span class="bar"></span>(.*?)</div>', content, re.S)
        tag = tag_m.group(1).strip() if tag_m else ''

        # H2
        h2_m = re.search(r'<h2>(.*?)</h2>', content, re.S)
        h2 = h2_m.group(1).strip() if h2_m else ''

        # Paragraphs
        paragraphs = []
        for pm in re.finditer(r'<p>(.*?)</p>', content, re.S):
            paragraphs.append(pm.group(1).strip())

        # Figure
        figure = None
        fig_m = re.search(r'<figure>.*?<img[^>]*alt="([^"]*)"[^>]*>.*?<figcaption>(.*?)</figcaption>', content, re.S)
        if fig_m:
            figure = {
                "alt": fig_m.group(1).strip(),
                "caption": fig_m.group(2).strip(),
                "src": ""  # Will be filled from images
            }

        steps.append({
            "id": step_id,
            "vp": vp,
            "state": state,
            "tag": tag,
            "h2": h2,
            "paragraphs": paragraphs,
            "figure": figure
        })
    data['steps'] = steps
    print(f"      ✓ steps: {len(steps)} items")

    # Outro
    outro = {}
    m = re.search(r'<section class="outro">\s*<h2>(.*?)</h2>', html, re.S)
    if m: outro['h2'] = m.group(1).strip()
    m = re.search(r'</h2>\s*<p>(.*?)</p>', html, re.S)
    if m: outro['p'] = m.group(1).strip()
    m = re.search(r'<div class="verdict">(.*?)</div>', html, re.S)
    if m: outro['verdict'] = m.group(1).strip()
    # Footgrid
    footgrid = []
    m = re.search(r'<div class="footgrid">(.*?)</div>\s*</section>', html, re.S)
    if m:
        for fm in re.finditer(r'<div class="fc"><b>(.*?)</b>(.*?)</div>', m.group(1), re.S):
            footgrid.append({"title": fm.group(1).strip(), "body": fm.group(2).strip()})
    outro['footgrid'] = footgrid
    data['outro'] = outro

    # Footer
    m = re.search(r'<footer>(.*?)</footer>', html, re.S)
    if m: data['footer'] = m.group(1).strip()

    # —— Brand & meta ——
    data['brand'] = {
        "green": "#76b900",
        "greenD": "#5a9200",
        "pixelTextTop": "RTX",
        "pixelTextBottom": "NVIDIA"
    }
    data['quarter'] = "2026Q3"
    data['asOf'] = "2026-07-23"

    # —— Chart-specific values (extracted from original JS) ——
    # K-line y-axis ranges
    data['kline'] = {
        "yMin": 0.02,
        "yMax": 400,
        "focusYMin": 0.5,
        "focusYMax": 70,
        "focusRange": ["2016-12", "2023-06"],
        "footHtml": "E1 Pascal · E2 Volta 财报 · E3 矿难起点 · E4 Arm 收购宣布 · E5 疫情顶 $34.5 · E6 谷底 -69% · E7 ChatGPT · E8 核弹级指引 · E9 1拆10/3万亿 · E10 DeepSeek -17% · E11 H20 禁售 $86.5 · E12 破 5 万亿 · E13 新高 $236.3 · E14 现价 $212。<b>灰点（2010 前）为拆股复权近似值，只画点不连线。</b>",
        "markArea": [
            [{"name": "矿难 -56%", "xAxis": "2018-10"}, {"xAxis": "2018-12"}],
            [{"name": "库存崩盘 -69%", "xAxis": "2021-11"}, {"xAxis": "2022-10"}]
        ]
    }

    # Fin markpoints
    data['finMarkpoints'] = [
        {"coord": ["FY26Q1", 60.5], "value": "H20 减记", "itemStyle": {"color": "#e0a800"}},
        {"coord": ["FY23Q2", 43.5], "value": "库存洗澡", "itemStyle": {"color": "#98a1ab"}}
    ]

    # Inv markpoints
    data['invMarkpoints'] = [
        {"coord": ["FY23Q4", 212], "value": "游戏崩盘 212天", "itemStyle": {"color": "#c0392b"}},
        {"coord": ["FY26Q2", 106], "value": "Rubin 备料 106天", "itemStyle": {"color": "#e0a800"}}
    ]

    # Wall empty fallback
    data['wallEmptyFallback'] = "这一波没有破产者——2016–2026 的 AI 芯片出清以「并购」而非「破产」完成：Graphcore 卖身软银、Habana 并入 Intel。资本泡沫期的失败者，被更大的资产负债表吸收了。"

    # Wall labels
    data['wallLabels'] = {
        "w1": "第一波 · 图形卡大逃杀",
        "w2": "第二波 · AI 芯片"
    }

    # Clock center text
    data['clockCenterText'] = "2026-07"

    # Radar labels
    data['radarLabels'] = {
        "now": "今天：NVDA 2026",
        "cisco": "思科 2000",
        "mine": "NVDA 2018 矿潮"
    }

    # Viz note
    data['vizNote'] = "数据截至 2026-07-23"

    # vp-foot texts
    data['vpFoots'] = {
        "fin": "单季营收（柱，左轴，亿美元）与 GAAP 毛利率（线，右轴）。FY26Q1 毛利率 60.5% 系 H20 出口管制 45 亿美元减记；FY27Q1 净利率 71% 含大额非经营性收益（投资公允价值变动，口径注意）。来源：公司财报 / SEC。",
        "seg": "财年分部营收（堆叠柱，亿美元）与数据中心占比（线，右轴）。FY2026 全年营收 2,159 亿美元（+65%），数据中心 1,937 亿、占 90%。来源：公司 10-K / 财报。",
        "wall": "结局徽章：破产 / 被并购 / 重整 / 幸存（利基或转型存活）/ 在桌（仍是主要玩家）。幸存者名单是破产、重整、并购筛出来的。",
        "hf": "柱：四大云厂（微软/谷歌/亚马逊/Meta）资本开支，2026 为 4 月财报季上修后指引（约 7,250 亿美元，+77%）；线 1：英伟达数据中心收入（财年口径，对应次年）；线 2：H100 现货租金（右轴，行业报价近似）。capex 领先英伟达收入约 2–4 个季度。",
        "inv": "柱：库存（亿美元，财季末）；线：库存天数＝库存÷当季销售成本×91（右轴）。游戏崩盘峰值 212 天 → 缺货期 78–90 天 → FY26Q2 约 106 天（Blackwell→Rubin 换机备料）。阈值 150 天。CoWoS 月产能约 1.3 万片(2023)→7.5 万(2025)→约 10 万片(2026E，TrendForce 近似)——瓶颈已从封装让位给电力与 HBM。",
        "score": "雷达末维\"估值透支\"为反向计分：越高越危险。形状相似 ≠ 机制相似。",
        "signal": "每个信号独立配阈值 / 时滞 / 证伪点——监控不能共用一个仪表盘。状态：已确认（绿）/ 部分（黄）/ 观察（灰），截至 2026-07-23。"
    }

    # Title
    data['title'] = "英伟达产业周期 Scrollytelling 复盘 · 2026Q3"

    # —— Save ——
    out_path = out_dir / "nvidia_data.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[3/4] → {out_path} ({out_path.stat().st_size:,} bytes)")

    # —— Link images to steps ——
    if images:
        for i, step in enumerate(data['steps']):
            if step.get('figure') and f"fig_{i+1}" in images:
                step['figure']['src'] = images[f"fig_{i+1}"]['src']
        # Re-save with image links
        with open(out_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"[4/4] Linked {len(images)} images to steps, re-saved")

    print(f"\n✓ Done. Data: {out_path}")
    print(f"  Images: {img_out}")
    print(f"  Keys: {len(data)} top-level fields")

if __name__ == '__main__':
    main()
