"""
generate_report.py - 景气度简报报告生成

从评分数据生成HTML一页纸简报。
使用 assets/report_template.html 作为模板。

用法:
    python generate_report.py --input data/semiconductor_scored.json --output output/semiconductor_report.html
"""

import json
import argparse
import os
from datetime import datetime


def load_template():
    """加载HTML模板"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    template_path = os.path.join(base_dir, "assets", "report_template.html")
    with open(template_path, "r", encoding="utf-8") as f:
        return f.read()


def render_score_gauge(score):
    """生成评分仪表盘SVG"""
    # 0-100映射到0-180度
    angle = (score / 100) * 180
    # 颜色: <40红, 40-60黄, >60绿
    if score > 60:
        color = "#2f9e44"
    elif score >= 40:
        color = "#e8590c"
    else:
        color = "#e03131"
    
    return f"""
    <svg viewBox="0 0 200 120" width="200" height="120">
        <path d="M 20 100 A 80 80 0 0 1 180 100" fill="none" stroke="#e9ecef" stroke-width="12" stroke-linecap="round"/>
        <path d="M 20 100 A 80 80 0 0 1 {20 + 160 * score / 100:.1f} {100 - 80 * (1 - (1 - score / 100) ** 2) ** 0.5:.1f}" 
              fill="none" stroke="{color}" stroke-width="12" stroke-linecap="round" 
              stroke-dasharray="{251.3 * score / 100:.1f} 251.3"/>
        <text x="100" y="90" text-anchor="middle" font-size="32" font-weight="500" fill="{color}">{score}</text>
        <text x="100" y="110" text-anchor="middle" font-size="11" fill="#868e96">综合景气评分</text>
    </svg>
    """


def render_indicator_table(indicators):
    """生成指标明细表HTML行"""
    tier_labels = {"leading": "领先", "coincident": "同步", "lagging": "滞后"}
    direction_colors = {1: "#2f9e44", 0: "#868e96", -1: "#e03131"}
    direction_arrows = {1: "&uarr;", 0: "&rarr;", -1: "&darr;"}
    
    rows = ""
    for ind in indicators:
        tier = tier_labels.get(ind["tier"], ind["tier"])
        dir_color = direction_colors.get(ind["direction"], "#868e96")
        dir_arrow = direction_arrows.get(ind["direction"], "")
        
        value_str = ""
        if ind.get("value") is not None:
            unit = ind.get("value_unit", "")
            value_str = f"{ind['value']}{' ' + unit if unit else ''}"
        
        mom_str = ""
        if ind.get("mom_change") is not None:
            mom_str = f"{ind['mom_change']:+.2f}%"
        
        rows += f"""
        <tr>
            <td><span class="tier-badge tier-{ind['tier']}">{tier}</span></td>
            <td>{ind['name']}</td>
            <td>{value_str}</td>
            <td>{mom_str}</td>
            <td style="color:{dir_color};font-weight:500">{dir_arrow} {ind['direction_label']}</td>
            <td>{ind['weight']*100:.0f}%</td>
            <td>{ind.get('data_date', '')}</td>
        </tr>
        """
    
    return rows


def render_signals(signals, signal_type):
    """生成关键信号列表"""
    if not signals:
        return "<p class='no-signal'>暂无</p>"
    
    color = "#2f9e44" if signal_type == "positive" else "#e03131"
    arrow = "&uarr;" if signal_type == "positive" else "&darr;"
    
    items = ""
    for s in signals:
        items += f"""
        <div class="signal-item">
            <span class="signal-arrow" style="color:{color}">{arrow}</span>
            <span class="signal-name">{s['name']}</span>
            <span class="signal-weight">权重 {s['weight']*100:.0f}%</span>
        </div>
        """
    
    return items


def render_report(scored_data):
    """渲染完整报告"""
    template = load_template()
    
    # 评分仪表盘
    gauge_svg = render_score_gauge(scored_data["prosperity_score"])
    
    # 指标表格
    table_rows = render_indicator_table(scored_data["indicators"])
    
    # 关键信号
    positive_html = render_signals(scored_data.get("positive_signals", []), "positive")
    negative_html = render_signals(scored_data.get("negative_signals", []), "negative")
    
    # 填充模板
    report = template
    report = report.replace("{{INDUSTRY_NAME}}", scored_data.get("industry_name", ""))
    report = report.replace("{{REPORT_DATE}}", scored_data.get("report_period", ""))
    report = report.replace("{{SCORE}}", str(scored_data.get("prosperity_score", 0)))
    # 方向徽章CSS类
    direction = scored_data.get("direction", "")
    if "上行" in direction:
        badge_class = "direction-up"
    elif "下行" in direction:
        badge_class = "direction-down"
    else:
        badge_class = "direction-neutral"
    
    report = report.replace("{{DIRECTION}}", direction)
    report = report.replace("{{DIRECTION_DESC}}", scored_data.get("direction_description", ""))
    report = report.replace("{{DIRECTION_BADGE_CLASS}}", badge_class)
    report = report.replace("{{GAUGE_SVG}}", gauge_svg)
    report = report.replace("{{INDICATOR_ROWS}}", table_rows)
    report = report.replace("{{POSITIVE_SIGNALS}}", positive_html)
    report = report.replace("{{NEGATIVE_SIGNALS}}", negative_html)
    report = report.replace("{{GENERATE_TIME}}", datetime.now().strftime("%Y-%m-%d %H:%M"))
    
    # 数据来源说明
    sources = set()
    for ind in scored_data.get("indicators", []):
        sources.add(ind.get("data_source", ""))
    source_list = "、".join(sorted(sources)) if sources else "数据源待补充"
    report = report.replace("{{DATA_SOURCES}}", source_list)
    
    # 示例数据标记
    if scored_data.get("sample_data"):
        report = report.replace("{{SAMPLE_WARNING}}", 
            '<div style="background:#fff3cd;border:1px solid #ffe08a;padding:8px 16px;border-radius:6px;margin:12px 0;font-size:13px;color:#854F0B;">&#9888; 本报告使用示例数据，仅供开发测试，不可用于任何实际决策。</div>')
    else:
        report = report.replace("{{SAMPLE_WARNING}}", "")
    
    return report


def main():
    parser = argparse.ArgumentParser(description="景气度简报报告生成")
    parser.add_argument("--input", type=str, required=True,
                       help="输入JSON文件路径 (calculate_score.py的输出)")
    parser.add_argument("--output", type=str, required=True,
                       help="输出HTML文件路径")
    args = parser.parse_args()
    
    # 加载评分数据
    with open(args.input, "r", encoding="utf-8") as f:
        scored_data = json.load(f)
    
    # 渲染报告
    report_html = render_report(scored_data)
    
    # 保存
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(report_html)
    
    print(f"[OK] 报告已生成: {args.output}")
    print(f"     行业: {scored_data.get('industry_name', '')}")
    print(f"     评分: {scored_data.get('prosperity_score', 0)}/100")
    print(f"     方向: {scored_data.get('direction', '')}")


if __name__ == "__main__":
    main()
