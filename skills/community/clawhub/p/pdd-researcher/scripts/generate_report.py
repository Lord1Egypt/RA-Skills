#!/usr/bin/env python3
"""
拼多多研究员 - 交互式HTML报告生成器
读取分析结果JSON，生成专业的可视化HTML报告

用法:
  python generate_report.py <input_json> <output_html>
"""

import json
import sys
import os
from datetime import datetime


def load_data(json_path):
    """加载分析结果JSON"""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_html(data):
    """构建完整HTML报告"""
    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>拼多多研究报告 - {data.get('query', '')} | PDD Researcher</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
{get_css()}
</style>
</head>
<body>
<div class="container">
  {build_header(data)}
  {build_score_dashboard(data)}
  {build_dimension_cards(data)}
  {build_charts_section(data)}
  {build_insights_section(data)}
  {build_action_plan(data)}
  {build_footer(data)}
</div>
<script>
{get_js(data)}
</script>
</body>
</html>"""


def get_css():
    return """
:root {
  --primary: #E02E24;
  --primary-light: #FFF0EF;
  --secondary: #FF6B35;
  --bg: #F5F5F5;
  --card-bg: #FFFFFF;
  --text: #222222;
  --text-secondary: #666666;
  --border: #E8E8E8;
  --success: #00A870;
  --warning: #FF9800;
  --danger: #E02E24;
  --info: #1976D2;
  --tag-bg: #F3F4F6;
  --tag-text: #555;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
}

.container {
  max-width: 1080px;
  margin: 0 auto;
  padding: 24px 20px 60px;
}

/* Header */
.header {
  background: linear-gradient(135deg, #E02E24 0%, #FF6B35 100%);
  border-radius: 16px;
  padding: 32px 36px;
  color: white;
  margin-bottom: 24px;
  position: relative;
  overflow: hidden;
}

.header::after {
  content: '';
  position: absolute;
  top: -60px;
  right: -60px;
  width: 200px;
  height: 200px;
  background: rgba(255,255,255,0.06);
  border-radius: 50%;
}

.header h1 {
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 8px;
  position: relative;
  z-index: 1;
}

.header .subtitle {
  font-size: 14px;
  opacity: 0.9;
  position: relative;
  z-index: 1;
}

.header .meta {
  display: flex;
  gap: 20px;
  margin-top: 16px;
  flex-wrap: wrap;
  position: relative;
  z-index: 1;
}

.header .meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  opacity: 0.85;
}

.header .meta-item .badge {
  background: rgba(255,255,255,0.25);
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 12px;
}

/* Score Dashboard */
.score-dashboard {
  background: var(--card-bg);
  border-radius: 16px;
  padding: 28px 32px;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 32px;
  flex-wrap: wrap;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.score-circle {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  flex-shrink: 0;
}

.score-circle.high { background: #E8F5E9; color: #2E7D32; border: 3px solid #4CAF50; }
.score-circle.medium { background: #FFF3E0; color: #E65100; border: 3px solid #FF9800; }
.score-circle.low { background: #FFEBEE; color: #C62828; border: 3px solid #E53935; }

.score-value {
  font-size: 42px;
  line-height: 1;
}

.score-label {
  font-size: 13px;
  margin-top: 4px;
}

.score-details {
  flex: 1;
  min-width: 280px;
}

.score-details h3 {
  font-size: 20px;
  margin-bottom: 6px;
}

.score-details .verdict {
  font-size: 15px;
  color: var(--text-secondary);
  margin-bottom: 12px;
  line-height: 1.7;
}

.score-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.tag {
  padding: 4px 12px;
  border-radius: 14px;
  font-size: 12px;
  font-weight: 600;
}

.tag-green { background: #E8F5E9; color: #2E7D32; }
.tag-orange { background: #FFF3E0; color: #E65100; }
.tag-red { background: #FFEBEE; color: #C62828; }
.tag-blue { background: #E3F2FD; color: #1565C0; }
.tag-purple { background: #F3E5F5; color: #7B1FA2; }

/* Section Title */
.section-title {
  font-size: 20px;
  font-weight: 700;
  margin: 32px 0 16px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.section-title::before {
  content: '';
  width: 4px;
  height: 24px;
  background: var(--primary);
  border-radius: 2px;
}

/* Dimension Cards */
.dim-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.dim-card {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 20px 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  transition: transform 0.15s;
}

.dim-card:hover { transform: translateY(-2px); }

.dim-card .dim-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.dim-card .dim-icon {
  font-size: 24px;
}

.dim-card .dim-name {
  font-size: 15px;
  font-weight: 600;
}

.dim-card .dim-score {
  font-size: 28px;
  font-weight: 700;
}

.dim-card .dim-bar {
  height: 6px;
  background: #F0F0F0;
  border-radius: 3px;
  margin: 10px 0;
  overflow: hidden;
}

.dim-card .dim-bar-fill {
  height: 100%;
  border-radius: 3px;
  transition: width 0.5s ease;
}

.dim-card .dim-desc {
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
}

.dim-bar-fill.high { background: linear-gradient(90deg, #4CAF50, #66BB6A); }
.dim-bar-fill.medium { background: linear-gradient(90deg, #FF9800, #FFB74D); }
.dim-bar-fill.low { background: linear-gradient(90deg, #E53935, #EF5350); }

/* Charts */
.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}

@media (max-width: 768px) {
  .charts-row { grid-template-columns: 1fr; }
  .dim-grid { grid-template-columns: 1fr; }
}

.chart-card {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 20px 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.chart-card h4 {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 12px;
}

.chart-card canvas {
  max-height: 280px;
}

/* Insights Cards */
.insights-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.insight-card {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 20px 24px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  border-left: 4px solid var(--primary);
}

.insight-card h4 {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.insight-card ul {
  list-style: none;
  padding: 0;
}

.insight-card li {
  padding: 5px 0;
  font-size: 13px;
  color: var(--text-secondary);
  line-height: 1.6;
  padding-left: 18px;
  position: relative;
}

.insight-card li::before {
  content: '→';
  position: absolute;
  left: 0;
  color: var(--primary);
  font-size: 12px;
}

/* Action Plan */
.action-list {
  list-style: none;
  padding: 0;
}

.action-item {
  background: var(--card-bg);
  border-radius: 12px;
  padding: 16px 20px;
  margin-bottom: 10px;
  display: flex;
  align-items: flex-start;
  gap: 14px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.action-priority {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
  color: white;
}

.action-priority.p0 { background: #E53935; }
.action-priority.p1 { background: #FF9800; }
.action-priority.p2 { background: #1976D2; }

.action-content h5 {
  font-size: 15px;
  font-weight: 600;
  margin-bottom: 3px;
}

.action-content p {
  font-size: 13px;
  color: var(--text-secondary);
}

/* Competitor Table */
.comp-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--card-bg);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
  margin-bottom: 24px;
}

.comp-table th {
  background: #FAFAFA;
  padding: 12px 16px;
  text-align: left;
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid var(--border);
}

.comp-table td {
  padding: 14px 16px;
  font-size: 13px;
  border-bottom: 1px solid var(--border);
}

.comp-table tr:hover td {
  background: #FFFBF0;
}

.comp-table .price-highlight {
  color: var(--primary);
  font-weight: 700;
  font-size: 15px;
}

.comp-table .keyword-tag {
  display: inline-block;
  background: var(--tag-bg);
  color: var(--tag-text);
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 11px;
  margin: 2px 3px;
}

/* Footer */
.footer {
  text-align: center;
  padding: 24px 0;
  font-size: 12px;
  color: #999;
  border-top: 1px solid var(--border);
  margin-top: 32px;
}

.footer .disclaimer {
  background: #FFFBF0;
  border: 1px solid #FFE082;
  border-radius: 8px;
  padding: 12px 16px;
  margin-bottom: 12px;
  font-size: 12px;
  color: #795548;
  text-align: left;
}

/* Summary Strip */
.summary-strip {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  flex-wrap: wrap;
}

.summary-item {
  flex: 1;
  min-width: 150px;
  background: var(--card-bg);
  border-radius: 12px;
  padding: 16px 20px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

.summary-item .num {
  font-size: 28px;
  font-weight: 700;
  color: var(--primary);
}

.summary-item .num.secondary { color: var(--secondary); }
.summary-item .num.green { color: var(--success); }
.summary-item .num.blue { color: var(--info); }

.summary-item .lbl {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 4px;
}
"""


def build_header(data):
    query = data.get("query", "拼多多分析")
    analysis_type = data.get("analysis_type", "综合研究")
    created_at = data.get("created_at", datetime.now().strftime("%Y-%m-%d %H:%M"))
    data_source = data.get("data_source", "WebSearch + 公开信息")
    return f"""
<div class="header">
  <h1>🔍 拼多多研究报告</h1>
  <div class="subtitle">{analysis_type} · {query}</div>
  <div class="meta">
    <span class="meta-item">📅 {created_at}</span>
    <span class="meta-item">📊 <span class="badge">{data_source}</span></span>
    <span class="meta-item">🏷️ <span class="badge">拼多多</span></span>
  </div>
</div>"""


def build_score_dashboard(data):
    score_data = data.get("scores", {})
    overall = score_data.get("overall", {})
    score_val = overall.get("value", 0)
    score_class = "high" if score_val >= 75 else ("medium" if score_val >= 50 else "low")
    verdict = overall.get("verdict", "数据收集中")
    tags_html = "".join(f'<span class="tag {t.get("class", "tag-blue")}">{t.get("text", "")}</span>' for t in overall.get("tags", []))

    return f"""
<div class="score-dashboard">
  <div class="score-circle {score_class}">
    <span class="score-value">{score_val}</span>
    <span class="score-label">综合评分</span>
  </div>
  <div class="score-details">
    <h3>研究结论</h3>
    <p class="verdict">{verdict}</p>
    <div class="score-tags">{tags_html}</div>
  </div>
</div>"""


def build_dimension_cards(data):
    dims = data.get("dimensions", [])
    cards = []
    for d in dims:
        score = d.get("score", 0)
        bar_class = "high" if score >= 75 else ("medium" if score >= 50 else "low")
        cards.append(f"""
<div class="dim-card">
  <div class="dim-header">
    <span class="dim-name">{d.get("icon", "📊")} {d.get("name", "")}</span>
    <span class="dim-score">{score}</span>
  </div>
  <div class="dim-bar"><div class="dim-bar-fill {bar_class}" style="width:{score}%"></div></div>
  <div class="dim-desc">{d.get("desc", "")}</div>
</div>""")
    return '<div class="section-title">📊 多维度分析</div>\n<div class="dim-grid">' + "".join(cards) + "</div>"


def build_charts_section(data):
    charts = data.get("charts", {})
    sections = []
    if charts.get("price_distribution"):
        sections.append(f"""
<div class="chart-card">
  <h4>💰 价格带分布</h4>
  <canvas id="priceChart"></canvas>
</div>""")
    if charts.get("keyword_ranking"):
        sections.append(f"""
<div class="chart-card">
  <h4>🔑 关键词热度排行</h4>
  <canvas id="keywordChart"></canvas>
</div>""")
    if sections:
        return '<div class="section-title">📈 数据可视化</div>\n<div class="charts-row">' + "".join(sections) + "</div>"
    return ""


def build_insights_section(data):
    insights = data.get("insights", [])
    cards = []
    for ins in insights:
        items = "".join(f"<li>{item}</li>" for item in ins.get("items", []))
        cards.append(f"""
<div class="insight-card" style="border-left-color: {ins.get('color', 'var(--primary)')}">
  <h4>{ins.get('icon', '💡')} {ins.get('title', '')}</h4>
  <ul>{items}</ul>
</div>""")
    if cards:
        return '<div class="section-title">💡 核心洞察</div>\n<div class="insights-grid">' + "".join(cards) + "</div>"
    return ""


def build_action_plan(data):
    actions = data.get("actions", [])
    items = []
    for a in actions:
        items.append(f"""
<div class="action-item">
  <div class="action-priority {a.get('priority', 'p2').lower()}">{a.get('priority', 'P2')}</div>
  <div class="action-content">
    <h5>{a.get('title', '')}</h5>
    <p>{a.get('desc', '')}</p>
  </div>
</div>""")
    if items:
        return '<div class="section-title">📋 行动建议</div>\n<div class="action-list">' + "".join(items) + "</div>"
    return ""


def build_footer(data):
    disclaimers = data.get("disclaimers", [
        "本报告数据来源于公开网络搜索，仅供研究参考，不构成商业决策建议。",
        "价格和销量数据为搜索时刻的快照，实际数据可能有变化。",
        "拼多多平台数据受反爬机制限制，部分数据为估算值。"
    ])
    disc_html = "".join(f"<p>⚠️ {d}</p>" for d in disclaimers)
    return f"""
<div class="footer">
  <div class="disclaimer">{disc_html}</div>
  <p>Generated by 拼多多研究员 (PDD Researcher) · WorkBuddy AI</p>
  <p>数据驱动电商决策 · 让每一分钱都花在刀刃上</p>
</div>"""


def get_js(data):
    charts = data.get("charts", {})
    js_parts = []

    if charts.get("price_distribution"):
        pd = charts["price_distribution"]
        js_parts.append(f"""
new Chart(document.getElementById('priceChart'), {{
  type: 'bar',
  data: {{
    labels: {json.dumps(pd.get("labels", []))},
    datasets: [{{
      label: '商品数量',
      data: {json.dumps(pd.get("data", []))},
      backgroundColor: ['#FFCDD2','#EF9A9A','#E57373','#EF5350','#E53935','#C62828','#B71C1C'],
      borderRadius: 6
    }}]
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ display: false }} }},
    scales: {{ y: {{ beginAtZero: true, grid: {{ color: '#F0F0F0' }} }} }}
  }}
}});
""")

    if charts.get("keyword_ranking"):
        kw = charts["keyword_ranking"]
        js_parts.append(f"""
new Chart(document.getElementById('keywordChart'), {{
  type: 'bar',
  data: {{
    labels: {json.dumps(kw.get("labels", []))},
    datasets: [{{
      label: '搜索热度',
      data: {json.dumps(kw.get("data", []))},
      backgroundColor: ['#FF9800','#FFB74D','#FFCC80','#FFE0B2','#FFF3E0','#FFE0B2','#FFCC80','#FFB74D','#FF9800','#FB8C00'],
      borderRadius: 6
    }}]
  }},
  options: {{
    indexAxis: 'y',
    responsive: true,
    plugins: {{ legend: {{ display: false }} }},
    scales: {{ x: {{ beginAtZero: true, grid: {{ color: '#F0F0F0' }} }} }}
  }}
}});
""")

    return "\n".join(js_parts)


def main():
    if len(sys.argv) < 3:
        print("Usage: python generate_report.py <input_json> <output_html>")
        sys.exit(1)

    input_json = sys.argv[1]
    output_html = sys.argv[2]

    if not os.path.exists(input_json):
        print(f"Error: Input file not found: {input_json}")
        sys.exit(1)

    data = load_data(input_json)
    html = build_html(data)

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Report generated: {output_html}")


if __name__ == "__main__":
    main()
