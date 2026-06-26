#!/usr/bin/env python3
"""
Payroll Audit Report Generator v6.0 - 审核报告（表格为主）

设计原则：
- 整体以表格形式呈现，信息密度高
- 顶部结论汇总表 + 各维度明细表
- 支持锚定跳转（#rule-RL-001）关联看板和数据索引
- 保留可选的 SVG 图表作为附录

输入: rules_engine.py 输出的 audit_result.json
输出: HTML 表格化报告 / Markdown 报告

用法:
    python3 scripts/generate_report_v6.py --input audit_result.json --format both
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path


# ---------------------------------------------------------------------------
# SVG Charts (optional appendix)
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
# Data Aggregation
# ---------------------------------------------------------------------------

def aggregate_results(results):
    """将 rules_engine.py 输出聚合为报告数据结构"""
    summary = {
        "total_records": results.get("total_records", 0),
        "timestamp": results.get("audit_time", datetime.now().isoformat()),
        "version": results.get("version", ""),
        "blocked": results.get("summary", {}).get("blocked", False),
        # Counts
        "red_count": 0,
        "yellow_count": 0,
        "blue_count": 0,
        "policy_violation_count": 0,
        "business_violation_count": 0,
        "formula_check_passed": True,
        "field_check_passed": True,
        # Detail lists
        "red_details": [],
        "yellow_details": [],
        "blue_details": [],
        "policy_details": [],
        "business_details": [],
        "formula_results": [],
        "field_check": {},
        "comparison": results.get("comparison", None),
    }

    # Red lines
    rl = results.get("red_lines", {})
    for r in rl.get("rule_results", []):
        summary["red_count"] += r.get("triggered", 0)
        summary["red_details"].append(r)

    # Yellow lines
    yl = results.get("yellow_lines", {})
    for r in yl.get("rule_results", []):
        summary["yellow_count"] += r.get("triggered", 0)
        summary["yellow_details"].append(r)

    # Blue lines
    bl = results.get("blue_lines", {})
    for r in bl.get("rule_results", []):
        summary["blue_count"] += r.get("triggered", 0)
        summary["blue_details"].append(r)

    # Policy check
    pc = results.get("policy_check", {})
    for r in pc.get("rule_results", []):
        summary["policy_violation_count"] += r.get("violation_count", 0)
        summary["policy_details"].append(r)

    # Business check
    bc = results.get("business_check", {})
    for r in bc.get("rule_results", []):
        summary["business_violation_count"] += r.get("triggered", 0)
        summary["business_details"].append(r)

    # Formula check
    fc = results.get("formula_check", {})
    summary["formula_results"] = fc.get("formula_results", [])
    for fr in summary["formula_results"]:
        if fr.get("violation_count", 0) > 0:
            summary["formula_check_passed"] = False

    # Field check
    summary["field_check"] = results.get("field_check", {})
    if not summary["field_check"].get("passed", True):
        summary["field_check_passed"] = False

    return summary


# ---------------------------------------------------------------------------
# Evidence helpers
# ---------------------------------------------------------------------------

def get_evidence_passed(summary):
    """生成"审核通过"的数据支撑说明"""
    evidences = []
    total = summary.get("total_records", 0)

    if summary.get("field_check_passed", True):
        fc = summary.get("field_check", {})
        evidences.append(
            f"字段完整性通过：{fc.get('total_fields_checked', 0)}个必填字段全部存在，零缺失"
        )

    for fr in summary.get("formula_results", []):
        if fr.get("passed", False) or fr.get("violation_count", 0) == 0:
            evidences.append(
                f"公式校验通过：{fr.get('total_checked', 0)}条记录全部在容差范围内，零误差"
            )

    if summary.get("red_count", 0) == 0:
        rl = summary.get("red_details", [])
        red_rules = len(rl)
        evidences.append(
            f"红线校验通过：{red_rules}项红线规则扫描{total}人，零触发"
        )

    if summary.get("policy_violation_count", 0) == 0 and summary.get("policy_details"):
        evidences.append(
            f"特殊政策执行通过：{len(summary['policy_details'])}项政策校验零违规"
        )

    if summary.get("business_violation_count", 0) == 0 and summary.get("business_details"):
        evidences.append(
            f"业务逻辑校验通过：{len(summary['business_details'])}项规则校验{total}人，零异常"
        )

    comp = summary.get("comparison")
    if comp and comp.get("metrics"):
        for metric, data in comp.get("metrics", {}).items():
            change = data.get("change_pct", 0)
            curr = data.get("current", 0)
            prev = data.get("previous", 0)
            if abs(change) <= 10:
                evidences.append(
                    f"总额环比正常：{metric} 从¥{prev:,.0f}→¥{curr:,.0f}，变化{change:+.1f}%，在±10%正常范围内"
                )

    return evidences


def get_evidence_failed(summary):
    """生成异常项的数据支撑"""
    evidences = []

    for r in summary.get("red_details", []):
        if r.get("triggered", 0) > 0:
            evidences.append({
                "rule_id": r.get("rule_id", ""),
                "rule_name": r.get("name", r.get("rule_name", "")),
                "category": "红线",
                "triggered": r["triggered"],
                "total_checked": r.get("total_checked", 0),
                "details": r.get("details", []),
            })

    for r in summary.get("yellow_details", []):
        if r.get("triggered", 0) > 0:
            evidences.append({
                "rule_id": r.get("rule_id", ""),
                "rule_name": r.get("name", r.get("rule_name", "")),
                "category": "黄线",
                "triggered": r["triggered"],
                "total_checked": r.get("total_checked", 0),
                "details": r.get("details", []),
            })

    for r in summary.get("policy_details", []):
        if r.get("violation_count", 0) > 0:
            evidences.append({
                "rule_id": r.get("rule_id", ""),
                "rule_name": r.get("name", r.get("policy_name", "")),
                "category": "政策",
                "triggered": r["violation_count"],
                "total_checked": r.get("matched_count", 0),
                "details": r.get("violations", []),
            })

    for r in summary.get("business_details", []):
        if r.get("triggered", 0) > 0:
            evidences.append({
                "rule_id": r.get("rule_id", ""),
                "rule_name": r.get("name", r.get("rule_name", "")),
                "category": "业务规则",
                "triggered": r["triggered"],
                "total_checked": r.get("total_checked", 0),
                "details": r.get("details", []),
            })

    for fr in summary.get("formula_results", []):
        if fr.get("violation_count", 0) > 0:
            evidences.append({
                "rule_id": fr.get("rule_id", ""),
                "rule_name": fr.get("rule_name", ""),
                "category": "公式",
                "triggered": fr["violation_count"],
                "total_checked": fr.get("total_checked", 0),
                "details": fr.get("violations", []),
            })

    return evidences


# ---------------------------------------------------------------------------
# HTML Report v6.0 — 表格为主
# ---------------------------------------------------------------------------

def generate_html(summary, link_template=None):
    """生成 HTML 表格化报告 v6.0"""
    total = summary["total_records"]
    blocked = summary.get("blocked", False)
    red_count = summary["red_count"]
    yellow_count = summary["yellow_count"]
    blue_count = summary["blue_count"]

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

    # Build dimension summary table rows
    dim_rows = []

    # Field check
    fc = summary.get("field_check", {})
    fc_checked = fc.get("total_fields_checked", 0)
    fc_passed_val = fc_checked if fc.get("passed", True) else 0
    fc_failed = fc_checked - fc_passed_val
    fc_rate = "100.0%" if fc.get("passed", True) else f"{(fc_passed_val / max(fc_checked, 1)) * 100:.1f}%"
    fc_status = "✅ 通过" if fc.get("passed", True) else "❌ 异常"
    dim_rows.append(("字段完整性", "FC-001", fc_checked, fc_passed_val, fc_failed, fc_rate, fc_status, "#fields"))

    # Formula check
    for fr in summary.get("formula_results", []):
        fail = fr.get("violation_count", 0)
        chk = fr.get("total_checked", 0)
        pass_val = chk - fail
        rate = f"{(pass_val / max(chk, 1)) * 100:.1f}%"
        status = "✅ 通过" if fail == 0 else "❌ 异常"
        rid = fr.get("rule_id", "")
        dim_rows.append((fr.get("rule_name", "公式校验"), rid, chk, pass_val, fail, rate, status, f"#formulas"))

    # Red lines
    for r in summary.get("red_details", []):
        triggered = r.get("triggered", 0)
        j = r.get("judgment", {})
        chk = j.get("actually_checked", r.get("total_checked", total))
        pass_val = chk - triggered
        rate = j.get("pass_rate", f"{(pass_val / max(chk, 1)) * 100:.1f}%")
        status = "✅ 通过" if triggered == 0 else "🔴 阻断"
        rid = r.get("rule_id", "")
        dim_rows.append((r.get("name", ""), rid, chk, pass_val, triggered, rate, status, f"#{rid}"))

    # Yellow lines
    for r in summary.get("yellow_details", []):
        triggered = r.get("triggered", 0)
        j = r.get("judgment", {})
        chk = j.get("actually_checked", r.get("total_checked", total))
        pass_val = chk - triggered
        rate = j.get("pass_rate", f"{(pass_val / max(chk, 1)) * 100:.1f}%")
        status = "✅ 通过" if triggered == 0 else "🟠 异常"
        rid = r.get("rule_id", "")
        dim_rows.append((r.get("name", ""), rid, chk, pass_val, triggered, rate, status, f"#{rid}"))

    # Blue lines
    for r in summary.get("blue_details", []):
        triggered = r.get("triggered", 0)
        j = r.get("judgment", {})
        chk = j.get("actually_checked", r.get("total_checked", total))
        pass_val = chk - triggered
        rate = j.get("pass_rate", f"{(pass_val / max(chk, 1)) * 100:.1f}%")
        status = "✅ 通过" if triggered == 0 else "🔵 提示"
        rid = r.get("rule_id", "")
        dim_rows.append((r.get("name", ""), rid, chk, pass_val, triggered, rate, status, f"#{rid}"))

    # Policy
    for r in summary.get("policy_details", []):
        triggered = r.get("violation_count", 0)
        chk = r.get("matched_count", total)
        pass_val = chk - triggered
        rate = f"{(pass_val / max(chk, 1)) * 100:.1f}%"
        status = "✅ 通过" if triggered == 0 else "🟠 异常"
        rid = r.get("rule_id", "")
        dim_rows.append((r.get("name", r.get("policy_name", "")), rid, chk, pass_val, triggered, rate, status, f"#{rid}"))

    # Business
    for r in summary.get("business_details", []):
        triggered = r.get("triggered", 0)
        chk = r.get("total_checked", total)
        pass_val = chk - triggered
        rate = f"{(pass_val / max(chk, 1)) * 100:.1f}%"
        status = "✅ 通过" if triggered == 0 else "🟠 异常"
        rid = r.get("rule_id", "")
        dim_rows.append((r.get("name", ""), rid, chk, pass_val, triggered, rate, status, f"#{rid}"))

    # Evidence lists
    passed_evidence = get_evidence_passed(summary)
    failed_evidence = get_evidence_failed(summary)

    # Charts data
    pie_data = [
        ("红线", red_count, "#dc2626"),
        ("黄线", yellow_count, "#f59e0b"),
        ("蓝线", blue_count, "#3b82f6"),
        ("通过", max(1, total - red_count - yellow_count), "#22c55e"),
    ]
    bar_data = []
    for r in summary.get("red_details", []) + summary.get("yellow_details", []):
        if r.get("triggered", 0) > 0:
            bar_data.append((r.get("name", r.get("rule_name", "")), r["triggered"], "#dc2626"))
    if not bar_data:
        bar_data = [("无异常", 0, "#22c55e")]

    # --- HTML ---
    html_parts = []
    html_parts.append(f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>工资审核报告 v6 - {summary['timestamp'][:10]}</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #f1f5f9; color: #1e293b; line-height: 1.6; }}
  .container {{ max-width: 1200px; margin: 0 auto; padding: 24px; }}
  .header {{ background: white; border-radius: 12px; padding: 24px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 16px; }}
  .header h1 {{ font-size: 22px; }}
  .header .meta {{ color: #64748b; font-size: 13px; }}
  .status-badge {{ display: inline-block; padding: 6px 16px; border-radius: 20px; color: white; font-weight: 600; background: {status_color}; font-size: 14px; }}
  .section {{ background: white; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }}
  .section h2 {{ font-size: 16px; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 2px solid #e2e8f0; color: #0f172a; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{ background: #f8fafc; padding: 10px 12px; text-align: left; color: #475569; font-weight: 600; border-bottom: 2px solid #e2e8f0; white-space: nowrap; }}
  td {{ padding: 8px 12px; border-bottom: 1px solid #f1f5f9; }}
  tr:hover td {{ background: #f8fafc; }}
  .num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  .rate-col {{ text-align: right; white-space: nowrap; }}
  .status-pass {{ color: #16a34a; font-weight: 600; }}
  .status-fail {{ color: #dc2626; font-weight: 600; }}
  .status-warn {{ color: #ea580c; font-weight: 600; }}
  .status-note {{ color: #6366f1; font-weight: 600; }}
  .evidence-list {{ background: #f0fdf4; border: 1px solid #bbf7d0; border-radius: 8px; padding: 12px 16px; }}
  .evidence-list.failed {{ background: #fef2f2; border-color: #fecaca; }}
  .evidence-list li {{ margin: 4px 0; font-size: 13px; }}
  .charts {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-top: 12px; }}
  .chart {{ text-align: center; }}
  .chart h3 {{ font-size: 13px; color: #64748b; margin-bottom: 8px; }}
  .detail-table td {{ font-size: 12px; }}
  .detail-table .person-tag {{ display: inline-block; padding: 2px 8px; background: #fef2f2; color: #dc2626; border-radius: 4px; font-size: 11px; margin: 2px; }}
  .detail-table .person-tag.yellow {{ background: #fffbeb; color: #d97706; }}
  .footer {{ text-align: center; color: #94a3b8; font-size: 12px; padding: 16px 0; }}
  .kanban-link {{ color: #3b82f6; text-decoration: none; font-size: 12px; }}
  .kanban-link:hover {{ text-decoration: underline; }}
  @media (max-width: 768px) {{ .charts {{ grid-template-columns: 1fr; }} .header {{ flex-direction: column; align-items: flex-start; }} }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div>
      <h1>📋 工资审核报告 v6.0</h1>
      <div class="meta">审核时间: {summary['timestamp'][:19].replace('T', ' ')} | 规则版本: {summary['version']} | 数据量: {total} 人</div>
    </div>
    <div class="status-badge">{status_text}</div>
  </div>""")

    # --- Section 1: 结论汇总表（核心表格） ---
    html_parts.append("""
  <div class="section">
    <h2>📊 审核结论汇总表</h2>
    <table>
      <thead>
        <tr>
          <th>维度</th>
          <th>规则ID</th>
          <th style="text-align:right">检查数</th>
          <th style="text-align:right">通过数</th>
          <th style="text-align:right">异常数</th>
          <th style="text-align:right">通过率</th>
          <th>结论</th>
          <th>详情</th>
        </tr>
      </thead>
      <tbody>""")

    for name, rid, checked, passed_val, failed_val, rate, status, anchor in dim_rows:
        status_class = "status-pass"
        if "阻断" in status:
            status_class = "status-fail"
        elif "异常" in status:
            status_class = "status-warn"
        elif "提示" in status:
            status_class = "status-note"

        kanban_href = f"kanban.html?rule={rid}" if rid else ""
        kanban_link = f'<a href="{kanban_href}" class="kanban-link" target="_blank">看板↗</a>' if rid else ""

        html_parts.append(f"""<tr id="{rid or anchor.replace('#', '')}">
          <td>{name}</td>
          <td style="font-family:monospace;color:#94a3b8;font-size:11px">{rid}</td>
          <td class="num">{checked:,}</td>
          <td class="num" style="color:#16a34a">{passed_val:,}</td>
          <td class="num" style="color:#dc2626;font-weight:600">{failed_val:,}</td>
          <td class="rate-col">{rate}</td>
          <td class="{status_class}">{status}</td>
          <td>{kanban_link}</td>
        </tr>""")

    html_parts.append("""      </tbody>
    </table>
  </div>""")

    # --- Section 2: 数据支撑 ---
    if passed_evidence or failed_evidence:
        html_parts.append("""
  <div class="section">
    <h2>📝 审核结论与数据支撑</h2>""")
        if failed_evidence:
            html_parts.append('<div class="evidence-list failed"><strong>异常项（需核实）：</strong><ul>')
            for e in failed_evidence:
                detail_link = f"kanban.html?rule={e['rule_id']}" if e.get("rule_id") else ""
                link_tag = f'<a href="{detail_link}" class="kanban-link" target="_blank">查看明细↗</a>' if detail_link else ""
                html_parts.append(f'<li>{e["category"]} {e["rule_name"]}：{e["triggered"]}人异常，检查{e["total_checked"]}人 {link_tag}</li>')
            html_parts.append('</ul></div>')
        if passed_evidence:
            html_parts.append('<div class="evidence-list"><strong>通过项（数据支撑）：</strong><ul>')
            for e in passed_evidence:
                html_parts.append(f'<li>✅ {e}</li>')
            html_parts.append('</ul></div>')
        html_parts.append("</div>")

    # --- Section 3: 异常明细表（按规则展开） ---
    all_failed = (
        [(r, "红线", "red") for r in summary.get("red_details", []) if r.get("triggered", 0) > 0] +
        [(r, "黄线", "yellow") for r in summary.get("yellow_details", []) if r.get("triggered", 0) > 0] +
        [(r, "政策", "yellow") for r in summary.get("policy_details", []) if r.get("violation_count", 0) > 0] +
        [(r, "业务规则", "yellow") for r in summary.get("business_details", []) if r.get("triggered", 0) > 0] +
        [(r, "公式", "yellow") for r in summary.get("formula_results", []) if r.get("violation_count", 0) > 0]
    )

    if all_failed:
        html_parts.append("""
  <div class="section">
    <h2>🔍 异常明细</h2>""")
        for rule, category, color_tag in all_failed:
            triggered = rule.get("triggered", rule.get("violation_count", 0))
            name = rule.get("name", rule.get("rule_name", rule.get("policy_name", "")))
            rid = rule.get("rule_id", "")
            details = rule.get("details", rule.get("violations", []))

            html_parts.append(f"""
    <h3 id="{rid}">🔴 [{category}] {name} ({rid}) — {triggered}人异常</h3>
    <table class="detail-table">
      <thead><tr><th>工号</th><th>姓名</th><th>异常值</th><th>预期值</th><th>详情</th></tr></thead>
      <tbody>""")
            for d in details[:30]:
                emp_id = d.get("工号", "")
                emp_name = d.get("姓名代号", "")
                val = d.get("value", d.get("diff", ""))
                expected = d.get("expected", "")
                idx = d.get("index", "")
                detail_href = ""
                if link_template and emp_id:
                    detail_href = link_template.replace("{emp_id}", emp_id).replace("{emp_name}", emp_name).replace("{row_index}", str(idx))
                detail_link = f'<a href="{detail_href}" target="_blank">🔗</a>' if detail_href else ""
                tag_class = "person-tag" if color_tag == "red" else "person-tag yellow"
                html_parts.append(f"""<tr>
          <td>{emp_id}</td>
          <td><span class="{tag_class}">{emp_name}</span></td>
          <td>{val}</td>
          <td>{expected}</td>
          <td>{detail_link}</td>
        </tr>""")
            if len(details) > 30:
                html_parts.append(f'<tr><td colspan="5" style="color:#94a3b8;font-style:italic">… 还有 {len(details) - 30} 条，见数据索引表</td></tr>')
            html_parts.append("</tbody></table>")
        html_parts.append("</div>")

    # --- Section 4: 总额分析 ---
    comp = summary.get("comparison")
    if comp:
        hc = comp.get("headcount", {})
        html_parts.append(f"""
  <div class="section">
    <h2>📈 总额环比分析</h2>
    <table>
      <thead><tr><th>指标</th><th style="text-align:right">本月</th><th style="text-align:right">上月</th><th style="text-align:right">变化率</th><th>状态</th></tr></thead>
      <tbody>
      <tr><td>人数</td><td class="num">{hc.get('current', 0):,}</td><td class="num">{hc.get('previous', 0):,}</td><td class="rate-col">{hc.get('change_pct', 0):+.1f}%</td><td>{"✅ 正常" if abs(hc.get('change_pct', 0)) <= 5 else "⚠️ 关注"}</td></tr>""")
        for metric, data in comp.get("metrics", {}).items():
            change = data["change_pct"]
            status_icon = "✅" if abs(change) <= 10 else "⚠️"
            status_label = "正常" if abs(change) <= 10 else "需分析"
            html_parts.append(
                f'<tr><td>{metric}</td><td class="num">¥{data["current"]:,.0f}</td>'
                f'<td class="num">¥{data["previous"]:,.0f}</td><td class="rate-col">{change:+.1f}%</td>'
                f'<td>{status_icon} {status_label}</td></tr>'
            )
        html_parts.append("</tbody></table></div>")

    # --- Appendix: Charts (optional) ---
    html_parts.append("""
  <div class="section">
    <h2>📊 可视化附录</h2>
    <div class="charts">
      <div class="chart"><h3>异常分布</h3>""")
    html_parts.append(svg_pie_chart(pie_data))
    html_parts.append("</div><div class='chart'><h3>异常项对比</h3>")
    html_parts.append(svg_bar_chart(bar_data))
    html_parts.append("</div></div></div>")

    # Footer
    html_parts.append(f"""
  <div class="footer">
    <p>由 payroll-data-audit v6.0 自动生成 | 全量对齐 SOP | 数据来源: rules_engine.py | 关联文件: data_index.json + kanban.html</p>
  </div>
</div>
</body>
</html>""")

    return '\n'.join(html_parts)


# ---------------------------------------------------------------------------
# Markdown Report v6.0 — 表格为主
# ---------------------------------------------------------------------------

def generate_markdown(summary):
    """生成 Markdown 表格化报告 v6.0"""
    lines = []
    total = summary["total_records"]
    blocked = summary.get("blocked", False)
    red_count = summary["red_count"]
    yellow_count = summary["yellow_count"]
    blue_count = summary["blue_count"]

    if blocked:
        status_text = "🔴 存在红线异常，禁止出报告"
    elif red_count > 0:
        status_text = "🔴 存在红线异常，需立即处理"
    elif yellow_count > 0:
        status_text = "⚠️ 存在黄线异常，需关注核实"
    elif blue_count > 0:
        status_text = "ℹ️ 有蓝线波动，了解即可"
    else:
        status_text = "✅ 审核通过，无异常"

    lines.append("# 📋 工资审核报告 v6.0\n")
    lines.append(f"**审核时间**: {summary['timestamp'][:19].replace('T', ' ')}  ")
    lines.append(f"**规则版本**: {summary['version']}  ")
    lines.append(f"**数据量**: {total} 人  ")
    lines.append(f"**审核结论**: {status_text}\n")

    # 结论汇总表
    lines.append("## 📊 审核结论汇总表\n")
    lines.append("| 维度 | 规则ID | 检查数 | 通过数 | 异常数 | 通过率 | 结论 |")
    lines.append("|------|--------|--------|--------|--------|--------|------|")

    # Field check
    fc = summary.get("field_check", {})
    fc_checked = fc.get("total_fields_checked", 0)
    fc_passed_val = fc_checked if fc.get("passed", True) else 0
    fc_failed = fc_checked - fc_passed_val
    fc_rate = "100.0%" if fc.get("passed", True) else f"{(fc_passed_val / max(fc_checked, 1)) * 100:.1f}%"
    fc_status = "✅ 通过" if fc.get("passed", True) else "❌ 异常"
    lines.append(f"| 字段完整性 | FC-001 | {fc_checked:,} | {fc_passed_val:,} | {fc_failed:,} | {fc_rate} | {fc_status} |")

    # Formula
    for fr in summary.get("formula_results", []):
        fail = fr.get("violation_count", 0)
        chk = fr.get("total_checked", 0)
        pass_val = chk - fail
        rate = f"{(pass_val / max(chk, 1)) * 100:.1f}%"
        status = "✅ 通过" if fail == 0 else "❌ 异常"
        rid = fr.get("rule_id", "")
        lines.append(f"| {fr.get('rule_name', '公式校验')} | {rid} | {chk:,} | {pass_val:,} | {fail:,} | {rate} | {status} |")

    # Red
    for r in summary.get("red_details", []):
        triggered = r.get("triggered", 0)
        chk = r.get("total_checked", total)
        pass_val = chk - triggered
        rate = f"{(pass_val / max(chk, 1)) * 100:.1f}%"
        status = "✅ 通过" if triggered == 0 else "🔴 阻断"
        rid = r.get("rule_id", "")
        lines.append(f"| {r.get('name', '')} | {rid} | {chk:,} | {pass_val:,} | {triggered:,} | {rate} | {status} |")

    # Yellow
    for r in summary.get("yellow_details", []):
        triggered = r.get("triggered", 0)
        chk = r.get("total_checked", total)
        pass_val = chk - triggered
        rate = f"{(pass_val / max(chk, 1)) * 100:.1f}%"
        status = "✅ 通过" if triggered == 0 else "🟠 异常"
        rid = r.get("rule_id", "")
        lines.append(f"| {r.get('name', '')} | {rid} | {chk:,} | {pass_val:,} | {triggered:,} | {rate} | {status} |")

    # Blue
    for r in summary.get("blue_details", []):
        triggered = r.get("triggered", 0)
        chk = r.get("total_checked", total)
        pass_val = chk - triggered
        rate = f"{(pass_val / max(chk, 1)) * 100:.1f}%"
        status = "✅ 通过" if triggered == 0 else "🔵 提示"
        rid = r.get("rule_id", "")
        lines.append(f"| {r.get('name', '')} | {rid} | {chk:,} | {pass_val:,} | {triggered:,} | {rate} | {status} |")

    # Policy
    for r in summary.get("policy_details", []):
        triggered = r.get("violation_count", 0)
        chk = r.get("matched_count", total)
        pass_val = chk - triggered
        rate = f"{(pass_val / max(chk, 1)) * 100:.1f}%"
        status = "✅ 通过" if triggered == 0 else "🟠 异常"
        rid = r.get("rule_id", "")
        lines.append(f"| {r.get('name', r.get('policy_name', ''))} | {rid} | {chk:,} | {pass_val:,} | {triggered:,} | {rate} | {status} |")

    # Business
    for r in summary.get("business_details", []):
        triggered = r.get("triggered", 0)
        chk = r.get("total_checked", total)
        pass_val = chk - triggered
        rate = f"{(pass_val / max(chk, 1)) * 100:.1f}%"
        status = "✅ 通过" if triggered == 0 else "🟠 异常"
        rid = r.get("rule_id", "")
        lines.append(f"| {r.get('name', '')} | {rid} | {chk:,} | {pass_val:,} | {triggered:,} | {rate} | {status} |")

    lines.append("")

    # 数据支撑
    passed_evidence = get_evidence_passed(summary)
    failed_evidence = get_evidence_failed(summary)

    if passed_evidence or failed_evidence:
        lines.append("## 📝 审核结论与数据支撑\n")
        if failed_evidence:
            lines.append("**异常项（需核实）：**")
            for e in failed_evidence:
                lines.append(f"- ❌ {e['category']} {e['rule_name']}：{e['triggered']}人异常，检查{e['total_checked']}人")
            lines.append("")
        if passed_evidence:
            lines.append("**通过项（数据支撑）：**")
            for e in passed_evidence:
                lines.append(f"- ✅ {e}")
            lines.append("")

    # 总额分析
    comp = summary.get("comparison")
    if comp:
        hc = comp.get("headcount", {})
        lines.append("## 📈 总额环比分析\n")
        lines.append("| 指标 | 本月 | 上月 | 变化率 | 状态 |")
        lines.append("|------|------|------|--------|------|")
        lines.append(f"| 人数 | {hc.get('current', 0):,} | {hc.get('previous', 0):,} | {hc.get('change_pct', 0):+.1f}% | {'✅ 正常' if abs(hc.get('change_pct', 0)) <= 5 else '⚠️ 关注'} |")
        for metric, data in comp.get("metrics", {}).items():
            change = data["change_pct"]
            status_icon = "✅" if abs(change) <= 10 else "⚠️"
            lines.append(
                f"| {metric} | ¥{data['current']:,.0f} | ¥{data['previous']:,.0f} | {change:+.1f}% | {status_icon} |"
            )
        lines.append("")

    lines.append("---")
    lines.append("*由 payroll-data-audit v6.0 自动生成 | 全量对齐 SOP | 关联文件: data_index.json + kanban.html*")

    return '\n'.join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="工资审核报告生成器 v6.0（表格为主）")
    parser.add_argument("--input", required=True, help="audit_result.json 路径")
    parser.add_argument("--format", choices=["html", "markdown", "both"], default="both", help="输出格式")
    parser.add_argument("--output", help="输出文件路径（默认自动生成）")
    parser.add_argument("--review-link", help="异常项人工复核超链接模板")
    args = parser.parse_args()

    with open(args.input, encoding="utf-8") as f:
        results = json.load(f)

    summary = aggregate_results(results)
    link_template = getattr(args, 'review_link', None)

    if args.format in ("html", "both"):
        html = generate_html(summary, link_template=link_template)
        output_path = args.output if args.output else "audit_report_v6.html"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ HTML 报告 v6: {output_path} ({len(html):,} bytes)")

    if args.format in ("markdown", "both"):
        md = generate_markdown(summary)
        output_path = (args.output.replace(".html", ".md") if args.output else "audit_report_v6.md")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"✅ Markdown 报告 v6: {output_path} ({len(md):,} bytes)")


if __name__ == "__main__":
    main()
