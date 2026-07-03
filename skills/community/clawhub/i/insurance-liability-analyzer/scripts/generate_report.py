#!/usr/bin/env python3
"""
保险责任分析报告生成器
将分析结果JSON转换为交互式HTML可视化报告
用法: python generate_report.py <input_json> [--output <output_html>]
"""

import argparse
import json
import os
import sys
from datetime import datetime


def get_dimension_weight(dimension):
    """获取各维度权重"""
    weights = {
        "保障责任": 0.20,
        "责任免除": 0.20,
        "时间条件": 0.10,
        "金额规则": 0.15,
        "理赔条件": 0.10,
        "可持续性": 0.15,
        "健康告知": 0.05,
        "特别约定": 0.05
    }
    return weights.get(dimension, 0.05)


def score_to_color(score):
    """评分转颜色"""
    if score >= 4:
        return "#52c41a"
    elif score >= 3:
        return "#faad14"
    elif score >= 2:
        return "#fa8c16"
    else:
        return "#f5222d"


def score_to_label(score):
    """评分转标签"""
    if score >= 4.5:
        return "优秀"
    elif score >= 3.5:
        return "良好"
    elif score >= 2.5:
        return "一般"
    elif score >= 1.5:
        return "较差"
    else:
        return "很差"


def generate_radar_chart(dimensions):
    """生成雷达图SVG"""
    labels = [d["name"] for d in dimensions]
    scores = [d["score"] for d in dimensions]
    n = len(labels)

    cx, cy, r = 200, 200, 140
    angles = [(-90 + i * 360 / n) for i in range(n)]

    # 计算多边形顶点
    def polar_to_cartesian(angle_deg, radius):
        import math
        angle_rad = math.radians(angle_deg)
        return cx + radius * math.cos(angle_rad), cy + radius * math.sin(angle_rad)

    # 网格圆
    grid_circles = ""
    for scale in [1, 2, 3, 4, 5]:
        points = []
        for angle in angles:
            x, y = polar_to_cartesian(angle, r * scale / 5)
            points.append(f"{x:.1f},{y:.1f}")
        grid_circles += f'<polygon points="{" ".join(points)}" fill="none" stroke="#e8e8e8" stroke-width="1"/>'

    # 轴线
    axis_lines = ""
    for angle in angles:
        x, y = polar_to_cartesian(angle, r)
        axis_lines += f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#d9d9d9" stroke-width="1"/>'

    # 数据多边形
    data_points = []
    for i, score in enumerate(scores):
        x, y = polar_to_cartesian(angles[i], r * score / 5)
        data_points.append(f"{x:.1f},{y:.1f}")
    data_polygon = f'<polygon points="{" ".join(data_points)}" fill="rgba(24,144,255,0.15)" stroke="#1890ff" stroke-width="2"/>'

    # 数据点
    data_dots = ""
    for i, score in enumerate(scores):
        x, y = polar_to_cartesian(angles[i], r * score / 5)
        data_dots += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#1890ff"/>'

    # 标签
    label_elements = ""
    for i, label in enumerate(labels):
        x, y = polar_to_cartesian(angles[i], r + 25)
        anchor = "middle"
        if x < cx - 10:
            anchor = "end"
        elif x > cx + 10:
            anchor = "start"
        label_elements += f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" dominant-baseline="middle" font-size="12" fill="#333">{label}</text>'

    return f'''
<svg viewBox="0 0 400 400" xmlns="http://www.w3.org/2000/svg" style="width:100%;max-width:400px;margin:0 auto;display:block">
    {grid_circles}
    {axis_lines}
    {data_polygon}
    {data_dots}
    {label_elements}
</svg>
'''


def generate_html_report(data):
    """生成完整HTML报告"""
    product_name = data.get("product_name", "未知产品")
    insurance_type = data.get("insurance_type", "未知")
    input_type = data.get("input_type", "")
    analysis_date = data.get("analysis_date", datetime.now().strftime("%Y-%m-%d"))
    overall_score = data.get("overall_score", 0)
    dimensions = data.get("dimensions", [])
    risks = data.get("risks", [])
    recommendations = data.get("recommendations", [])
    summary = data.get("summary", "")
    disclaimer = data.get("disclaimer", "")

    # 生成维度表格行
    dimension_rows = ""
    for d in dimensions:
        color = score_to_color(d["score"])
        label = score_to_label(d["score"])
        items_html = ""
        for item in d.get("items", []):
            items_html += f'<div class="item"><span class="item-label">{item["label"]}</span><span class="item-value">{item["value"]}</span></div>'
        risk_signals_html = ""
        for sig in d.get("risk_signals", []):
            risk_signals_html += f'<div class="risk-signal-item"><span class="risk-dot"></span>{sig}</div>'

        dimension_rows += f'''
        <div class="dimension-card" style="border-left-color: {color}">
            <div class="dimension-header">
                <div class="dimension-name">{d["name"]}</div>
                <div class="dimension-score" style="background:{color}">{d["score"]:.1f} <span class="score-label">{label}</span></div>
            </div>
            <div class="dimension-items">
                {items_html}
            </div>
            {f'<div class="risk-signals"><div class="risk-signals-title">风险信号</div>{risk_signals_html}</div>' if risk_signals_html else ''}
        </div>
        '''

    # 生成风险提示
    risk_cards = ""
    for i, risk in enumerate(risks):
        severity = risk.get("severity", "中")
        severity_color = {"高": "#f5222d", "中": "#faad14", "低": "#1890ff"}.get(severity, "#faad14")
        risk_cards += f'''
        <div class="risk-card" style="border-left-color:{severity_color}">
            <div class="risk-header">
                <span class="risk-badge" style="background:{severity_color}">{severity}风险</span>
                <span class="risk-title">{risk.get("title", "")}</span>
            </div>
            <div class="risk-desc">{risk.get("description", "")}</div>
        </div>
        '''

    # 生成建议
    rec_cards = ""
    for i, rec in enumerate(recommendations):
        rec_cards += f'''
        <div class="rec-card">
            <div class="rec-number">{i+1}</div>
            <div class="rec-content">
                <div class="rec-title">{rec.get("title", "")}</div>
                <div class="rec-desc">{rec.get("description", "")}</div>
            </div>
        </div>
        '''

    # 综合评分颜色
    overall_color = score_to_color(overall_score)
    overall_label = score_to_label(overall_score)

    # 雷达图
    radar_svg = generate_radar_chart(dimensions) if dimensions else ""

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>保险责任分析报告 - {product_name}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC", "Microsoft YaHei", sans-serif;
            background: #f5f7fa; color: #333; line-height: 1.6;
        }}
        .container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}

        /* 头部 */
        .header {{
            background: linear-gradient(135deg, #1890ff, #0050b3);
            color: white; border-radius: 16px; padding: 32px;
            margin-bottom: 24px; box-shadow: 0 4px 20px rgba(24,144,255,0.2);
        }}
        .header h1 {{ font-size: 24px; margin-bottom: 8px; }}
        .header-meta {{ display: flex; gap: 16px; flex-wrap: wrap; margin-top: 12px; opacity: 0.9; font-size: 14px; }}
        .header-meta span {{ background: rgba(255,255,255,0.2); padding: 4px 12px; border-radius: 20px; }}

        /* 概览区 */
        .overview {{ display: flex; gap: 24px; margin-bottom: 24px; flex-wrap: wrap; }}
        .overview-left {{ flex: 1; min-width: 300px; }}
        .overview-right {{ flex: 0 0 400px; }}

        .score-card {{
            background: white; border-radius: 16px; padding: 24px;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06); text-align: center;
        }}
        .score-card .score-num {{ font-size: 48px; font-weight: 700; color: {overall_color}; }}
        .score-card .score-label {{ font-size: 16px; color: #666; margin-top: 4px; }}
        .score-card .score-bar {{
            height: 8px; background: #f0f0f0; border-radius: 4px;
            margin-top: 16px; overflow: hidden;
        }}
        .score-card .score-bar-fill {{
            height: 100%; background: {overall_color};
            border-radius: 4px; transition: width 0.6s;
            width: {overall_score * 20}%;
        }}

        /* 维度分析 */
        .section-title {{
            font-size: 20px; font-weight: 600; margin-bottom: 16px;
            padding-left: 12px; border-left: 4px solid #1890ff;
        }}
        .dimensions {{ display: flex; flex-direction: column; gap: 16px; margin-bottom: 32px; }}

        .dimension-card {{
            background: white; border-radius: 12px; padding: 20px;
            border-left: 4px solid #1890ff;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }}
        .dimension-header {{
            display: flex; justify-content: space-between; align-items: center;
            margin-bottom: 12px;
        }}
        .dimension-name {{ font-size: 16px; font-weight: 600; }}
        .dimension-score {{
            padding: 4px 12px; border-radius: 20px;
            color: white; font-size: 14px; font-weight: 600;
        }}
        .score-label {{ font-size: 12px; opacity: 0.9; }}

        .dimension-items {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 8px; }}
        .item {{ display: flex; gap: 8px; padding: 6px 0; font-size: 14px; border-bottom: 1px dashed #f0f0f0; }}
        .item-label {{ color: #888; min-width: 80px; flex-shrink: 0; }}
        .item-value {{ color: #333; flex: 1; }}

        .risk-signals {{ margin-top: 12px; padding-top: 12px; border-top: 1px solid #f0f0f0; }}
        .risk-signals-title {{ font-size: 13px; color: #fa8c16; font-weight: 600; margin-bottom: 6px; }}
        .risk-signal-item {{ font-size: 13px; color: #666; padding: 2px 0; display: flex; align-items: center; gap: 6px; }}
        .risk-dot {{ width: 6px; height: 6px; background: #fa8c16; border-radius: 50%; flex-shrink: 0; }}

        /* 风险提示 */
        .risks {{ margin-bottom: 32px; display: flex; flex-direction: column; gap: 12px; }}
        .risk-card {{
            background: white; border-radius: 12px; padding: 16px 20px;
            border-left: 4px solid #faad14;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }}
        .risk-header {{ display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }}
        .risk-badge {{ padding: 2px 8px; border-radius: 4px; color: white; font-size: 12px; }}
        .risk-title {{ font-size: 15px; font-weight: 600; }}
        .risk-desc {{ font-size: 14px; color: #666; }}

        /* 建议 */
        .recommendations {{ margin-bottom: 32px; display: flex; flex-direction: column; gap: 12px; }}
        .rec-card {{
            background: white; border-radius: 12px; padding: 16px 20px;
            display: flex; gap: 16px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }}
        .rec-number {{
            width: 32px; height: 32px; background: #1890ff; color: white;
            border-radius: 50%; display: flex; align-items: center; justify-content: center;
            font-weight: 600; flex-shrink: 0;
        }}
        .rec-title {{ font-size: 15px; font-weight: 600; margin-bottom: 4px; }}
        .rec-desc {{ font-size: 14px; color: #666; }}

        /* 摘要 */
        .summary {{
            background: white; border-radius: 12px; padding: 20px;
            margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.04);
        }}
        .summary-text {{ font-size: 14px; color: #555; line-height: 1.8; }}

        /* 免责声明 */
        .disclaimer {{
            background: #fffbe6; border: 1px solid #ffe58f; border-radius: 8px;
            padding: 16px; margin-top: 24px; font-size: 13px; color: #8c6d1f;
        }}

        /* 响应式 */
        @media (max-width: 600px) {{
            .overview {{ flex-direction: column; }}
            .overview-right {{ flex: 1; }}
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>保险责任分析报告</h1>
        <div class="header-meta">
            <span>产品: {product_name}</span>
            <span>类型: {insurance_type}</span>
            <span>分析日期: {analysis_date}</span>
            <span>输入方式: {input_type}</span>
        </div>
    </div>

    <div class="overview">
        <div class="overview-left">
            <div class="score-card">
                <div class="score-num">{overall_score:.1f}</div>
                <div class="score-label">综合评分 / 5.0 - {overall_label}</div>
                <div class="score-bar"><div class="score-bar-fill"></div></div>
            </div>
        </div>
        <div class="overview-right">
            {radar_svg}
        </div>
    </div>

    {f'<div class="summary"><div class="section-title">分析摘要</div><div class="summary-text">{summary}</div></div>' if summary else ''}

    <div class="section-title">八维责任分析</div>
    <div class="dimensions">
        {dimension_rows}
    </div>

    {f'<div class="section-title">风险提示</div><div class="risks">{risk_cards}</div>' if risks else ''}

    {f'<div class="section-title">综合建议</div><div class="recommendations">{rec_cards}</div>' if recommendations else ''}

    <div class="disclaimer">
        <strong>免责声明：</strong>{disclaimer if disclaimer else "本报告基于AI对保险条款文本的自动分析生成，仅供参考，不构成保险购买建议。最终保险责任以正式保险合同条款为准。如有疑问，请咨询专业保险顾问或查阅保险合同原文。"}
    </div>
</div>
</body>
</html>'''

    return html


def main():
    parser = argparse.ArgumentParser(description='保险责任分析报告生成器')
    parser.add_argument('input', help='分析结果JSON文件路径')
    parser.add_argument('--output', '-o', help='输出HTML文件路径')

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"错误: 输入文件不存在: {args.input}", file=sys.stderr)
        sys.exit(1)

    with open(args.input, 'r', encoding='utf-8') as f:
        data = json.load(f)

    html = generate_html_report(data)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"报告已生成: {args.output}", file=sys.stderr)
    else:
        print(html)


if __name__ == '__main__':
    main()
