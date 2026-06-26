#!/usr/bin/env python3
"""
Payroll Audit Report Generator - 审核报告生成器 v5.1

输入: rules_engine.py 输出的 audit_results.json
输出: HTML 可视化报告 / Markdown 报告

用法:
    python3 scripts/generate_report.py --input audit_results.json --format html --output report.html
    python3 scripts/generate_report.py --input audit_results.json --format markdown --output report.md
    python3 scripts/generate_report.py --input audit_results.json --format both
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# SVG Chart Generators
# ---------------------------------------------------------------------------

def svg_pie_chart(data, width=300, height=200):
    """生成 SVG 饼图。data: [(label, value, color), ...]"""
    import math
    total = sum(v for _, v, _ in data)
    if total == 0:
        return f'<svg width="{width}" height="{height}"><text x="{width//2}" y="{height//2}" text-anchor="middle" fill="#999">无数据</text></svg>'

    cx, cy, r = width // 2, height // 2, min(width, height) // 2 - 20
    svg_parts = [f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    start_angle = 0
    legend_y = 20
    legend_x = width - 120

    for label, value, color in data:
        if value == 0:
            continue
        angle = (value / total) * 360
        end_angle = start_angle + angle
        start_rad = math.radians(start_angle - 90)
        end_rad = math.radians(end_angle - 90)
        x1 = cx + r * math.cos(start_rad)
        y1 = cy + r * math.sin(start_rad)
        x2 = cx + r * math.cos(end_rad)
        y2 = cy + r * math.sin(end_rad)
        large_arc = 1 if angle > 180 else 0
        svg_parts.append(
            f'<path d="M {cx} {cy} L {x1:.1f} {y1:.1f} A {r} {r} 0 {large_arc} 1 {x2:.1f} {y2:.1f} Z" '
            f'fill="{color}" stroke="#fff" stroke-width="1">'
            f'<title>{label}: {value}</title></path>'
        )
        svg_parts.append(
            f'<rect x="{legend_x}" y="{legend_y}" width="12" height="12" fill="{color}"/>'
            f'<text x="{legend_x + 18}" y="{legend_y + 10}" font-size="11" fill="#333">{label}: {value}</text>'
        )
        legend_y += 18
        start_angle = end_angle

    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


def svg_bar_chart(data, width=400, height=200):
    """生成 SVG 柱状图。data: [(label, value, color), ...]"""
    if not data:
        return f'<svg width="{width}" height="{height}"><text x="{width//2}" y="{height//2}" text-anchor="middle" fill="#999">无数据</text></svg>'

    padding = 40
    bar_area_w = width - padding * 2
    bar_area_h = height - padding * 2
    max_val = max(v for _, v, _ in data) or 1
    bar_width = bar_area_w / len(data) * 0.7
    gap = bar_area_w / len(data) * 0.3

    svg_parts = [f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}">']
    for i in range(5):
        y = padding + (bar_area_h / 4) * i
        val = max_val * (1 - i / 4)
        svg_parts.append(f'<line x1="{padding}" y1="{y}" x2="{width - padding}" y2="{y}" stroke="#eee" stroke-width="1"/>')
        svg_parts.append(f'<text x="{padding - 5}" y="{y + 4}" text-anchor="end" font-size="10" fill="#999">{val:.0f}</text>')

    for i, (label, value, color) in enumerate(data):
        x = padding + i * (bar_width + gap) + gap / 2
        h = (value / max_val) * bar_area_h
        y = padding + bar_area_h - h
        svg_parts.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width:.1f}" height="{h:.1f}" fill="{color}" rx="3">'
            f'<title>{label}: {value}</title></rect>'
        )
        svg_parts.append(
            f'<text x="{x + bar_width / 2:.1f}" y="{height - padding + 15}" text-anchor="middle" '
            f'font-size="10" fill="#666" transform="rotate(-45, {x + bar_width / 2:.1f}, {height - padding + 15})">{label}</text>'
        )

    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


# ---------------------------------------------------------------------------
# Report Data Aggregator (v5.1 format)
# ---------------------------------------------------------------------------

def aggregate_results_v5(results):
    """将 rules_engine.py v5.1 输出聚合为报告数据结构"""
    summary = {
        "format": "v5.1",
        "total_records": results.get("total_records", 0),
        "timestamp": results.get("audit_time", datetime.now().isoformat()),
        "version": results.get("version", ""),
        # 异常计数
        "red_count": 0,
        "yellow_count": 0,
        "blue_count": 0,
        "policy_violation_count": 0,
        "business_violation_count": 0,
        # 详细数据
        "red_details": [],
        "yellow_details": [],
        "blue_details": [],
        "policy_details": [],
        "business_details": [],
        # 数据支撑
        "formula_results": [],
        "field_check": {},
        "comparison": results.get("comparison", None),
        "summary": results.get("summary", {}),
    }

    # 红线
    rl = results.get("red_lines", {})
    for r in rl.get("rule_results", []):
        summary["red_count"] += r.get("triggered", 0)
        summary["red_details"].append(r)

    # 黄线
    yl = results.get("yellow_lines", {})
    for r in yl.get("rule_results", []):
        summary["yellow_count"] += r.get("triggered", 0)
        summary["yellow_details"].append(r)

    # 蓝线
    bl = results.get("blue_lines", {})
    for r in bl.get("rule_results", []):
        summary["blue_count"] += r.get("triggered", 0)
        summary["blue_details"].append(r)

    # 政策校验
    pc = results.get("policy_check", {})
    for r in pc.get("rule_results", []):
        summary["policy_violation_count"] += r.get("violation_count", 0)
        summary["policy_details"].append(r)

    # 业务规则校验
    bc = results.get("business_check", {})
    for r in bc.get("rule_results", []):
        summary["business_violation_count"] += r.get("triggered", 0)
        summary["business_details"].append(r)

    # 公式校验（数据支撑）
    fc = results.get("formula_check", {})
    summary["formula_results"] = fc.get("formula_results", [])

    # 字段检查（数据支撑）
    summary["field_check"] = results.get("field_check", {})

    return summary


def aggregate_results_old(results):
    """兼容旧格式"""
    summary = {
        "format": "old",
        "total_records": results.get("data_rows", 0),
        "timestamp": results.get("timestamp", datetime.now().isoformat()),
        "version": results.get("version", ""),
        "red_count": 0,
        "yellow_count": 0,
        "blue_count": 0,
        "policy_violation_count": 0,
        "business_violation_count": 0,
        "red_details": [],
        "yellow_details": [],
        "blue_details": [],
        "policy_details": [],
        "business_details": [],
        "formula_results": [],
        "field_check": {},
        "comparison": None,
        "summary": {},
    }
    for r in results.get("results", []):
        step = r.get("step", "")
        if step == "red_lines":
            summary["red_count"] += r.get("triggered", 0)
            summary["red_details"].append(r)
        elif step == "yellow_lines":
            summary["yellow_count"] += r.get("triggered", 0)
            summary["yellow_details"].append(r)
        elif step == "blue_lines":
            summary["blue_count"] += r.get("triggered", 0)
            summary["blue_details"].append(r)
        elif step == "formula_check":
            summary["formula_results"].append(r)
    return summary


def aggregate_results(results):
    if "total_records" in results:
        return aggregate_results_v5(results)
    return aggregate_results_old(results)


# ---------------------------------------------------------------------------
# Data Evidence Support
# ---------------------------------------------------------------------------

def get_evidence_passed(summary):
    """生成"审核通过"的数据支撑说明"""
    evidences = []
    total = summary.get("total_records", 0)

    # 公式校验支撑
    for fr in summary.get("formula_results", []):
        if fr.get("passed", False):
            evidences.append(
                f"公式校验通过：{fr.get('total_checked', 0)}条记录全部在容差范围内，"
                f"零误差"
            )

    # 字段检查支撑
    fc = summary.get("field_check", {})
    if fc.get("passed", False):
        evidences.append(
            f"字段完整性通过：{fc.get('total_fields_checked', 0)}个必填字段全部存在，"
            f"零缺失"
        )

    # 红线支撑
    if summary.get("red_count", 0) == 0:
        rl = summary.get("red_details", [])
        red_rules = len(rl)
        evidences.append(
            f"红线校验通过：{red_rules}项红线规则扫描{total}人，"
            f"零触发（实发≤0、加班超36h、低于最低工资、社保未缴）"
        )

    # 政策校验支撑
    if summary.get("policy_violation_count", 0) == 0:
        pc = summary.get("policy_details", [])
        if pc:
            evidences.append(
                f"特殊政策执行通过：{len(pc)}项政策校验零违规"
            )

    # 业务规则支撑
    if summary.get("business_violation_count", 0) == 0:
        bc = summary.get("business_details", [])
        if bc:
            evidences.append(
                f"业务逻辑校验通过：{len(bc)}项规则校验{total}人，零异常"
            )

    # 总额对比支撑
    comp = summary.get("comparison")
    if comp and comp.get("metrics"):
        for metric, data in comp.get("metrics", {}).items():
            change = data.get("change_pct", 0)
            curr = data.get("current", 0)
            prev = data.get("previous", 0)
            if abs(change) <= 10:
                evidences.append(
                    f"总额环比正常：{metric} 从¥{prev:,.0f}→¥{curr:,.0f}，"
                    f"变化{change:+.1f}%，在±10%正常范围内"
                )

    return evidences


def get_evidence_failed(summary):
    """生成异常项的数据支撑"""
    evidences = []

    for r in summary.get("red_details", []):
        if r.get("triggered", 0) > 0:
            evidences.append(
                f"🔴 {r['rule_name']}：{r['triggered']}人触发，"
                f"共检查{r.get('total_checked', 0)}人"
            )

    for r in summary.get("yellow_details", []):
        if r.get("triggered", 0) > 0:
            evidences.append(
                f"⚠️ {r['rule_name']}：{r['triggered']}人触发，"
                f"共检查{r.get('total_checked', 0)}人"
            )

    for r in summary.get("policy_details", []):
        if r.get("violation_count", 0) > 0:
            evidences.append(
                f"📋 {r['policy_name']}：{r['matched_count']}人符合政策条件，"
                f"{r['violation_count']}人未正确执行"
            )

    for r in summary.get("business_details", []):
        if r.get("triggered", 0) > 0:
            evidences.append(
                f"📐 {r['rule_name']}：{r['triggered']}人异常，"
                f"共检查{r.get('total_checked', 0)}人"
            )

    # 公式失败支撑
    for fr in summary.get("formula_results", []):
        if fr.get("violation_count", 0) > 0:
            evidences.append(
                f"📐 {fr['rule_name']}：{fr['violation_count']}条公式误差超标"
            )

    return evidences


# ---------------------------------------------------------------------------
# HTML Report Generator v5.1
# ---------------------------------------------------------------------------

def generate_html(summary):
    """生成 HTML 可视化报告 v5.1（对齐 SOP 结构）"""
    red_count = summary["red_count"]
    yellow_count = summary["yellow_count"]
    blue_count = summary["blue_count"]
    total = summary["total_records"]
    status = summary.get("summary", {})
    blocked = status.get("blocked", False)

    if blocked:
        status_color = "#dc2626"
        status_text = "🔴 存在红线异常，禁止出报告"
    elif red_count > 0:
        status_color = "#dc2626"
        status_text = "🔴 存在红线异常，需立即处理"
    elif yellow_count > 0:
        status_color = "#ea580c"
        status_text = "⚠️ 存在黄线异常，需关注核实"
    elif blue_count > 0:
        status_color = "#2563eb"
        status_text = "ℹ️ 有蓝线波动，了解即可"
    else:
        status_color = "#16a34a"
        status_text = "✅ 审核通过，无异常"

    # Evidence
    passed_evidence = get_evidence_passed(summary)
    failed_evidence = get_evidence_failed(summary)

    # Pie chart
    pie_data = [
        ("红线", red_count, "#dc2626"),
        ("黄线", yellow_count, "#f59e0b"),
        ("蓝线", blue_count, "#3b82f6"),
        ("通过", max(1, total - red_count - yellow_count), "#22c55e"),
    ]

    # Bar chart
    bar_data = []
    for r in summary.get("red_details", []) + summary.get("yellow_details", []):
        if r.get("triggered", 0) > 0:
            bar_data.append((r["rule_name"], r["triggered"], "#dc2626"))
    if not bar_data:
        bar_data = [("无异常", 0, "#22c55e")]

    # --- HTML sections ---
    html_parts = []

    # Header
    html_parts.append(f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>工资审核报告 - {summary['timestamp'][:10]}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f8fafc; color: #1e293b; line-height: 1.6; }}
  .container {{ max-width: 960px; margin: 0 auto; padding: 24px; }}
  .header {{ background: white; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
  .header h1 {{ font-size: 24px; margin-bottom: 8px; }}
  .header .meta {{ color: #64748b; font-size: 14px; }}
  .status-badge {{ display: inline-block; padding: 6px 16px; border-radius: 20px; color: white; font-weight: 600; margin-top: 12px; background: {status_color}; }}
  .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); gap: 16px; margin-bottom: 24px; }}
  .stat-card {{ background: white; border-radius: 12px; padding: 20px; text-align: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
  .stat-card .number {{ font-size: 32px; font-weight: 700; }}
  .stat-card .label {{ color: #64748b; font-size: 14px; margin-top: 4px; }}
  .stat-card.red .number {{ color: #dc2626; }}
  .stat-card.yellow .number {{ color: #f59e0b; }}
  .stat-card.blue .number {{ color: #3b82f6; }}
  .stat-card.green .number {{ color: #16a34a; }}
  .section {{ background: white; border-radius: 12px; padding: 24px; margin-bottom: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
  .section h2 {{ font-size: 18px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid #f1f5f9; }}
  .evidence {{ background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 16px; margin: 8px 0; }}
  .evidence.failed {{ background: #fef2f2; border-color: #fecaca; }}
  .evidence li {{ margin: 4px 0; font-size: 14px; }}
  .rule-group {{ margin-bottom: 12px; }}
  .rule-group summary {{ cursor: pointer; padding: 12px 16px; background: #f8fafc; border-radius: 8px; font-weight: 500; list-style: none; display: flex; align-items: center; gap: 8px; }}
  .rule-group summary::before {{ content: '▸'; font-size: 12px; transition: transform 0.2s; }}
  .rule-group[open] summary::before {{ content: '▾'; }}
  .rule-details {{ padding: 12px 16px; }}
  .person-tag {{ display: inline-block; padding: 2px 8px; background: #fef2f2; color: #dc2626; border-radius: 4px; font-size: 12px; margin: 2px; }}
  .person-tag.yellow {{ background: #fffbeb; color: #d97706; }}
  table {{ width: 100%; border-collapse: collapse; margin-top: 8px; }}
  th, td {{ padding: 8px 12px; text-align: left; border-bottom: 1px solid #f1f5f9; font-size: 14px; }}
  th {{ background: #f8fafc; color: #64748b; font-weight: 500; }}
  .charts {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
  .chart {{ text-align: center; }}
  .chart h3 {{ font-size: 14px; color: #64748b; margin-bottom: 8px; }}
  .footer {{ text-align: center; color: #94a3b8; font-size: 12px; padding: 24px 0; }}
  @media (max-width: 600px) {{ .charts {{ grid-template-columns: 1fr; }} .stats {{ grid-template-columns: repeat(2, 1fr); }} }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>📋 工资审核报告</h1>
    <div class="meta">审核时间: {summary['timestamp'][:19].replace('T', ' ')} | 规则版本: {summary['version']} | 数据量: {total} 人</div>
    <div class="status-badge">{status_text}</div>
  </div>

  <div class="stats">
    <div class="stat-card red"><div class="number">{red_count}</div><div class="label">🔴 红线异常</div></div>
    <div class="stat-card yellow"><div class="number">{yellow_count}</div><div class="label">⚠️ 黄线异常</div></div>
    <div class="stat-card blue"><div class="number">{blue_count}</div><div class="label">ℹ️ 蓝线波动</div></div>
    <div class="stat-card green"><div class="number">{summary.get('policy_violation_count', 0)}</div><div class="label">📋 政策违规</div></div>
  </div>""")

    # Data Evidence section (NEW)
    html_parts.append("""
  <div class="section">
    <h2>📊 数据可视化</h2>
    <div class="charts">
      <div class="chart"><h3>异常分布</h3>""")
    html_parts.append(svg_pie_chart(pie_data))
    html_parts.append("</div><div class='chart'><h3>异常项对比</h3>")
    html_parts.append(svg_bar_chart(bar_data))
    html_parts.append("</div></div></div>")

    # Evidence section
    if passed_evidence or failed_evidence:
        html_parts.append("""
  <div class="section">
    <h2>📝 审核结论与数据支撑</h2>""")
        if failed_evidence:
            html_parts.append('<div class="evidence failed"><strong>异常项（需核实）：</strong><ul>')
            for e in failed_evidence:
                html_parts.append(f'<li>{e}</li>')
            html_parts.append('</ul></div>')
        if passed_evidence:
            html_parts.append('<div class="evidence"><strong>通过项（数据支撑）：</strong><ul>')
            for e in passed_evidence:
                html_parts.append(f'<li>✅ {e}</li>')
            html_parts.append('</ul></div>')
        html_parts.append("</div>")

    # 1. 基础数据概览
    comp = summary.get("comparison")
    if comp:
        hc = comp.get("headcount", {})
        html_parts.append(f"""
  <div class="section">
    <h2>👥 1. 基础数据概览</h2>
    <table>
    <tr><th>指标</th><th>本月</th><th>上月</th><th>变化</th></tr>
    <tr><td>人数</td><td>{hc.get('current', 0)}</td><td>{hc.get('previous', 0)}</td><td>{hc.get('change_pct', 0):+.1f}%</td></tr>""")
        for metric, data in comp.get("metrics", {}).items():
            html_parts.append(
                f'<tr><td>{metric}</td><td>¥{data["current"]:,.0f}</td>'
                f'<td>¥{data["previous"]:,.0f}</td><td>{data["change_pct"]:+.1f}%</td></tr>'
            )
        html_parts.append("</table></div>")

    # 2. 特殊政策执行情况
    if summary.get("policy_details"):
        html_parts.append("""
  <div class="section">
    <h2>🏛️ 2. 特殊政策执行情况</h2>""")
        for r in summary["policy_details"]:
            color = "green" if r.get("passed", True) else "red"
            status_icon = "✅" if r.get("passed", True) else "❌"
            html_parts.append(f"""
    <details class="rule-group" {"open" if not r.get("passed", True) else ""}>
      <summary>{status_icon} {r['policy_name']} (符合条件{r.get('matched_count', 0)}人)</summary>
      <div class="rule-details">
        <p>违规人数: {r.get('violation_count', 0)}</p>""")
            for v in r.get("violations", [])[:10]:
                html_parts.append(
                    f'<p><span class="person-tag">{v.get("姓名代号", "")}({v.get("工号", "")})'
                    f': {v.get("field", "")} 预期{v.get("expected", "")} 实际{v.get("actual", "")}</span></p>'
                )
            html_parts.append("</div></details>")
        html_parts.append("</div>")

    # 3. 异常数据扫描
    html_parts.append("""
  <div class="section">
    <h2>🔍 3. 异常数据扫描结果</h2>
    <h3>🔴 红线异常（必须核实）</h3>""")
    for r in summary.get("red_details", []):
        if r.get("triggered", 0) > 0:
            html_parts.append(f"""
    <details class="rule-group" open>
      <summary>{r['rule_name']} ({r['triggered']}人触发 / 共{r.get('total_checked', 0)}人)</summary>
      <div class="rule-details">""")
            for d in r.get("details", [])[:20]:
                html_parts.append(
                    f'<span class="person-tag">{d.get("姓名代号", "")}({d.get("工号", "")})'
                    f': {d.get("value", "")}</span>'
                )
            html_parts.append("</div></details>")
    if summary["red_count"] == 0:
        html_parts.append('<p style="color:#16a34a">✅ 无红线异常</p>')

    # Yellow
    html_parts.append("<h3 style='margin-top:16px'>⚠️ 黄线异常（关注核实）</h3>")
    for r in summary.get("yellow_details", []):
        if r.get("triggered", 0) > 0:
            html_parts.append(f"""
    <details class="rule-group">
      <summary>{r['rule_name']} ({r['triggered']}人触发 / 共{r.get('total_checked', 0)}人)</summary>
      <div class="rule-details">""")
            for d in r.get("details", [])[:20]:
                html_parts.append(
                    f'<span class="person-tag yellow">{d.get("姓名代号", "")}({d.get("工号", "")})</span>'
                )
            html_parts.append("</div></details>")
    if summary["yellow_count"] == 0:
        html_parts.append('<p style="color:#16a34a">✅ 无黄线异常</p>')

    # Blue
    html_parts.append("<h3 style='margin-top:16px'>ℹ️ 蓝线波动（了解即可）</h3>")
    for r in summary.get("blue_details", []):
        if r.get("triggered", 0) > 0:
            html_parts.append(f"""
    <details class="rule-group">
      <summary>{r['rule_name']} ({r['triggered']}人)</summary>
      <div class="rule-details"><p>了解即可，通常无需深入</p></div></details>""")
    if summary["blue_count"] == 0:
        html_parts.append('<p style="color:#16a34a">✅ 无需关注</p>')
    html_parts.append("</div>")

    # 4. 总额分析
    if comp:
        html_parts.append("""
  <div class="section">
    <h2>📈 4. 总额分析</h2>
    <h3>总额环比</h3>
    <table><tr><th>计薪项</th><th>本月总额</th><th>上月总额</th><th>变化率</th><th>状态</th></tr>""")
        for metric, data in comp.get("metrics", {}).items():
            change = data["change_pct"]
            status_icon = "✅" if abs(change) <= 10 else "⚠️"
            html_parts.append(
                f'<tr><td>{metric}</td><td>¥{data["current"]:,.0f}</td>'
                f'<td>¥{data["previous"]:,.0f}</td><td>{change:+.1f}%</td>'
                f'<td>{status_icon} {"正常" if abs(change) <= 10 else "需分析"}</td></tr>'
            )
        html_parts.append("</table></div>")

    # 5. 公式校验 & 字段完整性
    if summary.get("formula_results") or summary.get("field_check"):
        html_parts.append("""
  <div class="section">
    <h2>📐 公式校验 & 字段完整性</h2>""")
        if summary.get("formula_results"):
            html_parts.append("<h3>公式校验</h3><table><tr><th>公式</th><th>检查数</th><th>通过</th><th>失败</th></tr>")
            for fr in summary["formula_results"]:
                fail = fr.get("violation_count", 0)
                status_icon = "✅" if fail == 0 else "❌"
                html_parts.append(
                    f'<tr><td>{status_icon} {fr.get("rule_name", "")}</td>'
                    f'<td>{fr.get("total_checked", 0)}</td><td>{fr.get("total_checked", 0) - fail}</td>'
                    f'<td style="color:{"red" if fail > 0 else "green"}">{fail}</td></tr>'
                )
            html_parts.append("</table>")

        fc = summary.get("field_check", {})
        if fc:
            html_parts.append(f"""<h3>字段完整性</h3>
<p>检查字段数: {fc.get('total_fields_checked', 0)} | 缺失: {len(fc.get('missing', {}))} | 格式错误: {len(fc.get('format_errors', {}))}</p>""")
            if fc.get("missing"):
                html_parts.append("<p>缺失字段:</p><ul>")
                for field, reason in fc["missing"].items():
                    html_parts.append(f"<li>{field}: {reason}</li>")
                html_parts.append("</ul>")
        html_parts.append("</div>")

    # Footer
    html_parts.append(f"""
  <div class="footer">
    <p>由 payroll-data-audit v5.1 自动生成 | 全量对齐 SOP v1.0 | 数据来源: rules_engine.py</p>
  </div>
</div>
</body>
</html>""")

    return '\n'.join(html_parts)


# ---------------------------------------------------------------------------
# Markdown Report Generator v5.1
# ---------------------------------------------------------------------------

def generate_markdown(summary):
    """生成 Markdown 报告 v5.1（对齐 SOP 结构）"""
    lines = []
    total = summary["total_records"]
    status = summary.get("summary", {})
    blocked = status.get("blocked", False)

    if blocked:
        status_text = "🔴 存在红线异常，禁止出报告"
    elif summary["red_count"] > 0:
        status_text = "🔴 存在红线异常，需立即处理"
    elif summary["yellow_count"] > 0:
        status_text = "⚠️ 存在黄线异常，需关注核实"
    elif summary["blue_count"] > 0:
        status_text = "ℹ️ 有蓝线波动，了解即可"
    else:
        status_text = "✅ 审核通过，无异常"

    lines.append("# 📋 工资审核报告\n")
    lines.append(f"**审核时间**: {summary['timestamp'][:19].replace('T', ' ')}  ")
    lines.append(f"**规则版本**: {summary['version']}  ")
    lines.append(f"**数据量**: {total} 人  ")
    lines.append(f"**审核结论**: {status_text}\n")

    # Data Evidence (NEW)
    passed_evidence = get_evidence_passed(summary)
    failed_evidence = get_evidence_failed(summary)

    if passed_evidence or failed_evidence:
        lines.append("## 📝 审核结论与数据支撑\n")
        if failed_evidence:
            lines.append("**异常项（需核实）：**")
            for e in failed_evidence:
                lines.append(f"- ❌ {e}")
            lines.append("")
        if passed_evidence:
            lines.append("**通过项（数据支撑）：**")
            for e in passed_evidence:
                lines.append(f"- ✅ {e}")
            lines.append("")

    # 1. 基础数据概览
    comp = summary.get("comparison")
    if comp:
        hc = comp.get("headcount", {})
        lines.append("## 👥 1. 基础数据概览\n")
        lines.append("| 指标 | 本月 | 上月 | 变化 |")
        lines.append("|------|------|------|------|")
        lines.append(f"| 人数 | {hc.get('current', 0)} | {hc.get('previous', 0)} | {hc.get('change_pct', 0):+.1f}% |")
        for metric, data in comp.get("metrics", {}).items():
            lines.append(
                f"| {metric} | ¥{data['current']:,.0f} | ¥{data['previous']:,.0f} | {data['change_pct']:+.1f}% |"
            )
        lines.append("")

    # 2. 特殊政策执行情况
    if summary.get("policy_details"):
        lines.append("## 🏛️ 2. 特殊政策执行情况\n")
        for r in summary["policy_details"]:
            status_icon = "✅" if r.get("passed", True) else "❌"
            lines.append(f"- {status_icon} {r['policy_name']} (符合条件{r.get('matched_count', 0)}人，违规{r.get('violation_count', 0)}人)")
            for v in r.get("violations", [])[:10]:
                lines.append(f"  - {v.get('姓名代号', '')}({v.get('工号', '')}): {v.get('field', '')} 预期{v.get('expected', '')} 实际{v.get('actual', '')}")
        lines.append("")

    # 3. 异常数据扫描
    lines.append("## 🔍 3. 异常数据扫描结果\n")

    # Red
    lines.append("### 🔴 红线异常（必须核实）\n")
    if summary["red_count"] > 0:
        for r in summary.get("red_details", []):
            if r.get("triggered", 0) > 0:
                lines.append(f"**{r['rule_name']}** ({r['triggered']}人触发 / 共{r.get('total_checked', 0)}人)")
                for d in r.get("details", [])[:20]:
                    lines.append(f"- {d.get('姓名代号', '')}({d.get('工号', '')}): {d.get('value', '')}")
                lines.append("")
    else:
        lines.append("✅ 无红线异常\n")

    # Yellow
    lines.append("### ⚠️ 黄线异常（关注核实）\n")
    if summary["yellow_count"] > 0:
        for r in summary.get("yellow_details", []):
            if r.get("triggered", 0) > 0:
                lines.append(f"**{r['rule_name']}** ({r['triggered']}人触发)")
                persons = [f"{d.get('姓名代号', '')}({d.get('工号', '')})" for d in r.get("details", [])[:10]]
                lines.append(f"  - {', '.join(persons)}")
                lines.append("")
    else:
        lines.append("✅ 无黄线异常\n")

    # Blue
    lines.append("### ℹ️ 蓝线波动（了解即可）\n")
    if summary["blue_count"] > 0:
        for r in summary.get("blue_details", []):
            if r.get("triggered", 0) > 0:
                lines.append(f"- {r['rule_name']} ({r['triggered']}人)")
        lines.append("")
    else:
        lines.append("✅ 无需关注\n")

    # 4. 总额分析
    if comp:
        lines.append("## 📈 4. 总额分析\n")
        lines.append("| 计薪项 | 本月总额 | 上月总额 | 变化率 | 状态 |")
        lines.append("|--------|---------|---------|--------|------|")
        for metric, data in comp.get("metrics", {}).items():
            change = data["change_pct"]
            status_icon = "✅" if abs(change) <= 10 else "⚠️"
            lines.append(
                f"| {metric} | ¥{data['current']:,.0f} | ¥{data['previous']:,.0f} | {change:+.1f}% | {status_icon} |"
            )
        lines.append("")

    # 公式 & 字段
    if summary.get("formula_results") or summary.get("field_check"):
        lines.append("## 📐 公式校验 & 字段完整性\n")
        if summary.get("formula_results"):
            lines.append("| 公式 | 检查数 | 通过 | 失败 |")
            lines.append("|------|--------|------|------|")
            for fr in summary["formula_results"]:
                fail = fr.get("violation_count", 0)
                status_icon = "✅" if fail == 0 else "❌"
                lines.append(f"| {status_icon} {fr.get('rule_name', '')} | {fr.get('total_checked', 0)} | {fr.get('total_checked', 0) - fail} | {fail} |")
            lines.append("")

        fc = summary.get("field_check", {})
        if fc:
            lines.append(f"**字段完整性**: 检查{fc.get('total_fields_checked', 0)}个字段，缺失{len(fc.get('missing', {}))}个，格式错误{len(fc.get('format_errors', {}))}个")
            if fc.get("missing"):
                for field, reason in fc["missing"].items():
                    lines.append(f"- ❌ {field}: {reason}")
            lines.append("")

    lines.append("---")
    lines.append(f"*由 payroll-data-audit v5.1 自动生成 | 全量对齐 SOP v1.0*")

    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="工资审核报告生成器 v5.1")
    parser.add_argument("--input", required=True, help="audit_results.json 路径")
    parser.add_argument("--format", choices=["html", "markdown", "both"], default="both", help="输出格式")
    parser.add_argument("--output", help="输出文件路径（默认自动生成）")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        results = json.load(f)

    summary = aggregate_results(results)

    if args.format in ("html", "both"):
        html = generate_html(summary)
        output_path = args.output or "audit_report.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ HTML 报告: {output_path} ({len(html):,} bytes)")

    if args.format in ("markdown", "both"):
        md = generate_markdown(summary)
        output_path = args.output.replace(".html", ".md") if args.output else "audit_report.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"✅ Markdown 报告: {output_path} ({len(md):,} bytes)")


if __name__ == "__main__":
    main()
