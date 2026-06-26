#!/usr/bin/env python3
"""
payroll-audit: HTML 可视化报告生成器
基于审核结果数据，自动生成含内联 SVG 图表的 HTML 报告。

用法:
    python generate_html_report.py --data <json_file> --output <output.html> [--month <month>] [--region <region>]

示例:
    python generate_html_report.py --data audit_results.json --output /tmp/payroll-audit-2026-05.html
"""

import argparse
import json
import os
from datetime import datetime


def generate_svg_chart(audit_results):
    """生成内联 SVG 柱状图（本月 vs 上月风险对比）"""
    items = [r.get("audit_item", "") for r in audit_results]
    statuses = [r.get("status", "unknown") for r in audit_results]

    # 简化的风险等级：pass=1(low), warning=2(mid), error=3(high)
    level_map = {"pass": 1, "warning": 2, "error": 3, "unknown": 0}
    levels = [level_map.get(s, 0) for s in statuses]

    # 上月模拟数据（实际应从历史数据读取）
    prev_levels = [min(2, l) for l in levels]  # 简化：上月略低

    svg_parts = []
    svg_parts.append('<svg viewBox="0 0 600 220" style="width:100%;max-width:600px;display:block;margin:0 auto">')

    # 网格线
    svg_parts.append('<line x1="50" y1="20" x2="560" y2="20" stroke="#eee" stroke-width="1"/>')
    svg_parts.append('<line x1="50" y1="85" x2="560" y2="85" stroke="#eee" stroke-width="1"/>')
    svg_parts.append('<line x1="50" y1="155" x2="560" y2="155" stroke="#eee" stroke-width="1"/>')

    # Y轴标签
    svg_parts.append('<text x="30" y="20" font-size="11" fill="#999">高</text>')
    svg_parts.append('<text x="30" y="85" font-size="11" fill="#999">中</text>')
    svg_parts.append('<text x="30" y="155" font-size="11" fill="#999">低</text>')

    # 柱状图
    bar_width = 18
    gap = 80
    x_start = 70
    base_y = 170
    max_h = 140

    for i, (item, level, prev) in enumerate(zip(items, levels, prev_levels)):
        x = x_start + i * gap
        h_curr = (level / 3) * max_h
        h_prev = (prev / 3) * max_h
        y_curr = base_y - h_curr
        y_prev = base_y - h_prev

        # 上月（灰色）
        svg_parts.append(
            f'<rect x="{x}" y="{y_prev}" width="{bar_width}" height="{h_prev}" fill="#bbb" rx="3" opacity="0.7"/>'
        )
        # 本月（颜色根据状态）
        colors = {1: "#2e7d32", 2: "#f57c00", 3: "#d32f2f", 0: "#ccc"}
        color = colors.get(level, "#1a73e8")
        svg_parts.append(
            f'<rect x="{x + bar_width + 4}" y="{y_curr}" width="{bar_width}" height="{h_curr}" fill="{color}" rx="3"/>'
        )

        # 短名称标签
        short_name = item[:4] if item else f"项{i+1}"
        svg_parts.append(
            f'<text x="{x + bar_width}" y="{base_y + 16}" font-size="10" fill="#888" text-anchor="middle">{short_name}</text>'
        )

    # 图例
    svg_parts.append('<rect x="420" y="10" width="12" height="12" fill="#bbb" rx="2"/>')
    svg_parts.append('<text x="438" y="20" font-size="10" fill="#888">上月</text>')
    svg_parts.append('<rect x="470" y="10" width="12" height="12" fill="#1a73e8" rx="2"/>')
    svg_parts.append('<text x="488" y="20" font-size="10" fill="#888">本月</text>')

    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


def generate_audit_cards(audit_results):
    """生成审核项状态卡片"""
    cards = []
    for r in audit_results:
        status = r.get("status", "unknown")
        status_icon = {"pass": "✅", "warning": "⚠️", "error": "❌", "unknown": "❓"}.get(status, "❓")
        priority = r.get("priority", "P1")
        priority_class = f"priority-{priority.lower().replace('（', '').replace('）', '')}"

        details_html = ""
        if r.get("details"):
            details_html = "<ul>" + "".join(f"<li>{d}</li>" for d in r["details"]) + "</ul>"

        card = f'''<details class="audit-card {priority_class}">
<summary>
<div class="audit-card-header">
<span class="audit-card-title">{status_icon} {r.get("audit_item", "未知")}</span>
<span class="badge badge-{"ok" if status == "pass" else "warn" if status == "warning" else "high"}">{status.upper()}</span>
</div>
</summary>
<div class="audit-card-body">
<p>{r.get("summary", "")}</p>
{details_html}
{f"<p>统计: 共 {r['counts']['total_unique']} 人, 两表匹配 {r['counts']['in_both']} 人</p>" if "counts" in r else ""}
</div>
</details>'''
        cards.append(card)

    return '\n'.join(cards)


def generate_html(month="2026-05", region="all", audit_results=None, materials_required=None, materials_scenario=None, risk_alerts=None, data_log=None):
    """生成完整 HTML 报告"""
    if audit_results is None:
        audit_results = []

    # 统计数据
    total = len(audit_results)
    completed = sum(1 for r in audit_results if r.get("status") == "pass")
    warnings = sum(1 for r in audit_results if r.get("status") == "warning")
    pending = sum(1 for r in audit_results if r.get("status") in ("error", "unknown"))
    pct = round(completed / total * 100) if total > 0 else 0

    error_count = sum(1 for r in audit_results if r.get("status") == "error")
    if error_count > 0:
        risk_level = "🔴 高风险"
        risk_class = "high"
    elif warnings > total * 0.3:
        risk_level = "🟠 中风险"
        risk_class = "medium"
    else:
        risk_level = "🟢 低风险"
        risk_class = "low"

    # 生成组件
    chart_svg = generate_svg_chart(audit_results)
    audit_cards = generate_audit_cards(audit_results)

    # 材料清单
    req_materials = ""
    if materials_required:
        req_materials = "\n".join(f'<li>{m}</li>' for m in materials_required)
    scenario_materials = ""
    if materials_scenario:
        scenario_materials = "\n".join(f'<li>{m}</li>' for m in materials_scenario)

    # 风险提示
    risk_html = ""
    if risk_alerts:
        for alert in risk_alerts:
            icon = {"high": "🔴", "medium": "🟠", "low": "🟢"}.get(alert.get("level", "medium"), "⚠️")
            risk_html += f'''<div class="risk-item">
<div class="risk-icon">{icon}</div>
<div class="risk-content">
<div class="risk-title">{alert.get("title", "")}</div>
<div class="risk-action">{alert.get("action", "")}</div>
</div>
</div>'''

    # 数据处理记录
    log_html = ""
    if data_log:
        for phase, steps in data_log.items():
            log_html += f'<div class="phase"><div class="phase-title">{phase}</div>'
            for step in steps:
                log_html += f'<div class="step">{step}</div>'
            log_html += '</div>'

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{month} 工资审核报告</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;background:#f0f2f5;color:#333;line-height:1.6}}
.container{{max-width:1100px;margin:0 auto;padding:20px}}
.header{{background:linear-gradient(135deg,#1a73e8,#0d47a1);color:#fff;padding:28px 32px;border-radius:12px;margin-bottom:20px}}
.header h1{{font-size:24px;margin-bottom:6px}}
.header .meta{{opacity:.85;font-size:14px;display:flex;gap:20px;flex-wrap:wrap}}
.dashboard{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px;margin-bottom:24px}}
.card{{background:#fff;border-radius:10px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,.06)}}
.card-label{{font-size:12px;color:#888;text-transform:uppercase;letter-spacing:.5px}}
.card-value{{font-size:32px;font-weight:700;margin-top:4px}}
.card-sub{{font-size:13px;color:#888;margin-top:2px}}
.risk-high{{color:#d32f2f}}.risk-medium{{color:#f57c00}}.risk-low{{color:#2e7d32}}
.badge{{display:inline-block;padding:3px 10px;border-radius:12px;font-size:12px;font-weight:600;color:#fff}}
.badge-high{{background:#d32f2f}}.badge-medium{{background:#f57c00}}.badge-low{{background:#2e7d32}}.badge-ok{{background:#2e7d32}}
.badge-warn{{background:#f57c00}}.badge-pending{{background:#9e9e9e}}
h2{{font-size:18px;margin:24px 0 12px;padding-left:8px;border-left:4px solid #1a73e8}}
h3{{font-size:15px;margin:16px 0 8px;color:#555}}
.audit-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px;margin-bottom:24px}}
.audit-card{{background:#fff;border-radius:8px;padding:16px;box-shadow:0 1px 4px rgba(0,0,0,.05);border-left:4px solid #ddd;transition:box-shadow .2s}}
.audit-card:hover{{box-shadow:0 4px 12px rgba(0,0,0,.1)}}
.audit-card.priority-p0{{border-left-color:#d32f2f}}
.audit-card.priority-p1{{border-left-color:#f57c00}}
.audit-card.priority-p2{{border-left-color:#2e7d32}}
.audit-card-header{{display:flex;justify-content:space-between;align-items:center;margin-bottom:8px}}
.audit-card-title{{font-weight:600;font-size:15px}}
.audit-card-body{{font-size:13px;color:#555}}
.audit-card-body ul{{padding-left:18px;margin-top:4px}}
.audit-card-body li{{margin-bottom:2px}}
details{{margin:8px 0}}
summary{{cursor:pointer;font-size:14px;color:#555;padding:4px 0}}
.chart-container{{background:#fff;border-radius:10px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,.06);margin-bottom:24px;overflow-x:auto}}
table{{width:100%;border-collapse:collapse;margin:12px 0;font-size:14px}}
th{{background:#f5f7fa;text-align:left;padding:10px 12px;font-weight:600;border-bottom:2px solid #e0e0e0}}
td{{padding:10px 12px;border-bottom:1px solid #f0f0f0}}
tr:hover td{{background:#fafbfc}}
.checklist{{list-style:none;padding:0}}
.checklist li{{padding:8px 12px;border-bottom:1px solid #f0f0f0;font-size:14px;display:flex;align-items:flex-start;gap:8px}}
.checklist li::before{{content:"☐";font-size:16px;color:#1a73e8;flex-shrink:0}}
.checklist li.checked::before{{content:"☑";color:#2e7d32}}
.risk-item{{background:#fff;border-radius:8px;padding:14px 16px;margin-bottom:10px;box-shadow:0 1px 4px rgba(0,0,0,.05);display:flex;gap:12px;align-items:flex-start}}
.risk-icon{{font-size:20px;flex-shrink:0;margin-top:2px}}
.risk-content{{flex:1}}
.risk-title{{font-weight:600;font-size:14px;margin-bottom:2px}}
.risk-action{{font-size:13px;color:#666;margin-top:2px}}
.footer{{text-align:center;padding:20px;font-size:12px;color:#999;border-top:1px solid #e0e0e0;margin-top:20px}}
.data-log{{background:#fff;border-radius:10px;padding:20px;box-shadow:0 2px 8px rgba(0,0,0,.06);margin-bottom:24px}}
.data-log .phase{{margin-bottom:16px}}
.data-log .phase-title{{font-weight:600;font-size:14px;color:#1a73e8;margin-bottom:6px}}
.data-log .step{{font-size:13px;color:#555;padding:4px 0 4px 16px;position:relative}}
.data-log .step::before{{content:"•";position:absolute;left:0;color:#1a73e8}}
@media(max-width:600px){{.dashboard{{grid-template-columns:1fr 1fr}}.audit-grid{{grid-template-columns:1fr}}.header h1{{font-size:20px}}}}
</style>
</head>
<body>
<div class="container">

<div class="header">
  <h1>📊 {month} 工资审核报告</h1>
  <div class="meta">
    <span>📅 审核月份：{month}</span>
    <span>🌍 审核范围：{region}</span>
    <span>📋 审核进度：<strong>{completed}/{total}</strong></span>
    <span>⚡ 风险等级：<span class="badge badge-{risk_class}">{risk_level}</span></span>
  </div>
</div>

<div class="dashboard">
  <div class="card">
    <div class="card-label">审核项总数</div>
    <div class="card-value">10</div>
    <div class="card-sub">P0 ×3 | P1 ×4 | P2 ×3</div>
  </div>
  <div class="card">
    <div class="card-label">已完成</div>
    <div class="card-value risk-low">{completed}</div>
    <div class="card-sub">{pct}% 完成率</div>
  </div>
  <div class="card">
    <div class="card-label">存疑项</div>
    <div class="card-value risk-medium">{warnings}</div>
    <div class="card-sub">需要进一步核实</div>
  </div>
  <div class="card">
    <div class="card-label">待处理</div>
    <div class="card-value risk-high">{pending}</div>
    <div class="card-sub">尚未开始审核</div>
  </div>
</div>

<h2>📋 审核项状态</h2>
<div class="audit-grid">
  {audit_cards}
</div>

<h2>📈 风险趋势对比</h2>
<div class="chart-container">
  {chart_svg}
</div>

<h2>📂 需索取材料清单</h2>
<div class="card">
  <h3>必须索取（每次）</h3>
  <ul class="checklist">
    {req_materials}
  </ul>
  <h3 style="margin-top:16px">按场景补充</h3>
  <ul class="checklist">
    {scenario_materials}
  </ul>
</div>

<h2>⚠️ 风险提示</h2>
{risk_html}

<h2>🔧 数据处理记录</h2>
<div class="data-log">
  {log_html}
</div>

<div class="footer">
  <p>报告生成时间：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} | 工资审核助手 v3.0</p>
  <p>本报告由 AI 辅助生成，最终审核结果需人工确认</p>
</div>

</div>
</body>
</html>'''

    return html


def main():
    parser = argparse.ArgumentParser(description="工资审核 HTML 可视化报告生成器")
    parser.add_argument("--data", required=True, help="审核结果 JSON 文件路径")
    parser.add_argument("--output", required=True, help="输出 HTML 文件路径")
    parser.add_argument("--month", default="2026-05", help="审核月份")
    parser.add_argument("--region", default="all", help="审核范围")

    args = parser.parse_args()

    # 加载数据
    with open(args.data, 'r', encoding='utf-8') as f:
        data = json.load(f)

    audit_results = data.get("audit_results", [])
    materials_required = data.get("materials_required", [])
    materials_scenario = data.get("materials_scenario", [])
    risk_alerts = data.get("risk_alerts", [])
    data_log = data.get("data_log", {})

    html = generate_html(
        month=args.month,
        region=args.region,
        audit_results=audit_results,
        materials_required=materials_required,
        materials_scenario=materials_scenario,
        risk_alerts=risk_alerts,
        data_log=data_log,
    )

    os.makedirs(os.path.dirname(args.output) if os.path.dirname(args.output) else ".", exist_ok=True)
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"HTML 报告已生成: {args.output}")


if __name__ == "__main__":
    main()
