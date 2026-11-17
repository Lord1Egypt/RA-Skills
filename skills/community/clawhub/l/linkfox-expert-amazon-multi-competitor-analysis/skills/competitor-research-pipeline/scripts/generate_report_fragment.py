#!/usr/bin/env python3
"""
Report Fragment Generator - 从结构化JSON自动生成HTML报告片段
减少Agent工作量：Agent只需准备JSON数据，无需手写HTML

Usage:
  python generate_report_fragment.py --stdin < report_data.json > fragment.html
  python generate_report_fragment.py report_data.json > fragment.html

Input JSON structure:
{
  "header": {"title":"...", "subtitle":"...", "meta":"..."},
  "kpi": [{"label":"...", "value":"...", "change":"...", "direction":"up/down/flat"}],
  "sections": [
    {"type":"table", "title":"...", "intro":"...", "headers":[...], "rows":[[...]], "highlight_first_col": true, "source":["tool1","tool2"]},
    {"type":"chart", "title":"...", "intro":"...", "charts":[{"id":"...", "height":300, "option":{...echarts...}}], "note":"...", "source":[...]},
    {"type":"swot", "title":"...", "strengths":[...], "weaknesses":[...], "opportunities":[...], "threats":[...], "source":[...]},
    {"type":"insights", "title":"...", "summary":"...", "items":[{"priority":"high/medium/low", "text":"..."}], "source":[...]},
    {"type":"comparison", "title":"...", "intro":"...", "cards":[{"title":"...", "body":"..."}], "source":[...]},
    {"type":"skip", "title":"...", "reason":"..."}
  ],
  "footer": "..."
}
"""

import json
import sys

def esc(s):
    """HTML escape"""
    if s is None: return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def gen_header(h):
    return f'''<div class="report-header">
  <h1>{esc(h["title"])}</h1>
  <div class="report-subtitle">{esc(h.get("subtitle",""))}</div>
  <div class="report-meta">{esc(h.get("meta",""))}</div>
</div>'''

def gen_kpi(cards):
    n = len(cards)
    cols = f"cols-{n}" if n <= 4 else "cols-4"
    items = []
    for c in cards:
        direction = c.get("direction", "flat")
        items.append(f'''  <div class="kpi-card">
    <div class="kpi-label">{esc(c["label"])}</div>
    <div class="kpi-value">{esc(c["value"])}</div>
    <div class="kpi-change {direction}">{esc(c.get("change",""))}</div>
  </div>''')
    return f'<div class="kpi-grid {cols}">\n' + "\n".join(items) + "\n</div>"

def gen_table(sec):
    headers = sec["headers"]
    rows = sec["rows"]
    highlight = sec.get("highlight_first_col", False)

    th = "".join(f'<th>{esc(h)}</th>' for h in headers)
    trs = []
    for row in rows:
        tds = []
        for i, cell in enumerate(row):
            cls = ' class="num"' if i > 0 else ""
            if highlight and i == 0:
                tds.append(f'<td><strong>{esc(cell)}</strong></td>')
            else:
                tds.append(f'<td{cls}>{esc(cell)}</td>')
        trs.append(f'<tr>{"".join(tds)}</tr>')

    source = gen_source(sec.get("source", []))
    intro = f'<p>{esc(sec.get("intro",""))}</p>' if sec.get("intro") else ""
    return f'''<section class="content-section">
  <h2>{esc(sec["title"])}</h2>
  {intro}
  <div class="data-table-wrapper">
    <table class="data-table">
      <thead><tr>{th}</tr></thead>
      <tbody>
{chr(10).join(trs)}
      </tbody>
    </table>
  </div>
  {source}
</section>'''

def gen_chart_section(sec):
    charts = sec.get("charts", [])
    intro = f'<p>{esc(sec.get("intro",""))}</p>' if sec.get("intro") else ""
    note = f'<p>{esc(sec.get("note",""))}</p>' if sec.get("note") else ""

    chart_html = []
    chart_scripts = []
    for ch in charts:
        cid = ch["id"]
        height = ch.get("height", 340)
        chart_html.append(f'<div class="chart-container"><div id="{cid}" style="width:100%;height:{height}px;"></div></div>')
        option = json.dumps(ch["option"], ensure_ascii=False)
        chart_scripts.append(f'var {cid} = echarts.init(document.getElementById("{cid}"));\n{cid}.setOption({option});')

    source = gen_source(sec.get("source", []))
    charts_str = "\n".join(chart_html)
    scripts_str = "\n".join(chart_scripts)

    return f'''<section class="content-section">
  <h2>{esc(sec["title"])}</h2>
  {intro}
  {charts_str}
  {note}
  {source}
</section>'''

def gen_swot(sec):
    def gen_card(cls, title, items):
        lis = "".join(f'<li>{esc(i)}</li>' for i in items)
        return f'''<div class="swot-card {cls}">
      <div class="swot-title">{title}</div>
      <ul>{lis}</ul>
    </div>'''

    cards = [
        gen_card("strengths", "✅ 优势", sec.get("strengths", [])),
        gen_card("weaknesses", "⚠️ 劣势", sec.get("weaknesses", [])),
        gen_card("opportunities", "🚀 机会", sec.get("opportunities", [])),
        gen_card("threats", "🔴 威胁", sec.get("threats", [])),
    ]
    source = gen_source(sec.get("source", []))
    return f'''<section class="content-section">
  <h2>{esc(sec["title"])}</h2>
  <div class="swot-grid">
{chr(10).join(cards)}
  </div>
  {source}
</section>'''

def gen_insights(sec):
    summary = ""
    if sec.get("summary"):
        summary = f'<div class="summary-box"><h4>核心发现</h4><p>{esc(sec["summary"])}</p></div>'

    items = []
    for item in sec.get("items", []):
        priority = item.get("priority", "medium")
        items.append(f'<li class="priority-{priority}">{esc(item["text"])}</li>')

    source = gen_source(sec.get("source", []))
    return f'''<section class="content-section">
  <h2>{esc(sec["title"])}</h2>
  {summary}
  <ul class="insight-list">
{chr(10).join(items)}
  </ul>
  {source}
</section>'''

def gen_comparison(sec):
    cards = []
    for c in sec.get("cards", []):
        cards.append(f'''<div class="comparison-card">
      <div class="card-title">{esc(c["title"])}</div>
      <p>{esc(c["body"])}</p>
    </div>''')
    n = len(cards)
    cols = f"cols-{n}" if n <= 3 else "cols-3"
    source = gen_source(sec.get("source", []))
    intro = f'<p>{esc(sec.get("intro",""))}</p>' if sec.get("intro") else ""
    return f'''<section class="content-section">
  <h2>{esc(sec["title"])}</h2>
  {intro}
  <div class="comparison-grid {cols}">
{chr(10).join(cards)}
  </div>
  {source}
</section>'''

def gen_skip(sec):
    return f'''<section class="content-section">
  <h2>{esc(sec["title"])}</h2>
  <div class="summary-box"><h4>{esc(sec.get("reason","跳过"))}</h4></div>
</section>'''

def gen_source(tools):
    if not tools:
        return ""
    tool_spans = "".join(f'<span class="ds-tool">{esc(t)}</span>' for t in tools)
    return f'<div class="data-source"><span class="ds-label">数据源：</span>{tool_spans}<span class="ds-time">· 2026-08-07</span></div>'

def main():
    if "--stdin" in sys.argv:
        data = json.load(sys.stdin)
    elif len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    parts = ["<!-- CONTENT_START -->"]
    echarts_scripts = []

    # Header
    if "header" in data:
        parts.append(gen_header(data["header"]))

    # KPI cards
    if "kpi" in data:
        parts.append(gen_kpi(data["kpi"]))

    # Sections
    for sec in data.get("sections", []):
        stype = sec.get("type", "skip")
        if stype == "table":
            parts.append(gen_table(sec))
        elif stype == "chart":
            parts.append(gen_chart_section(sec))
            # Collect ECharts scripts
            for ch in sec.get("charts", []):
                cid = ch["id"]
                option = json.dumps(ch["option"], ensure_ascii=False)
                echarts_scripts.append(f'var {cid} = echarts.init(document.getElementById("{cid}"));\n{cid}.setOption({option});')
        elif stype == "swot":
            parts.append(gen_swot(sec))
        elif stype == "insights":
            parts.append(gen_insights(sec))
        elif stype == "comparison":
            parts.append(gen_comparison(sec))
        elif stype == "skip":
            parts.append(gen_skip(sec))
        else:
            parts.append(gen_skip(sec))

    # Footer
    if "footer" in data:
        parts.append(f'<div class="report-footer">{esc(data["footer"])}</div>')

    # ECharts scripts block
    if echarts_scripts:
        parts.append("<!-- ECHARTS_SCRIPTS -->")
        parts.append("\n".join(echarts_scripts))
        parts.append("<!-- /ECHARTS_SCRIPTS -->")

    parts.append("<!-- CONTENT_END -->")

    print("\n".join(parts))

if __name__ == "__main__":
    main()
