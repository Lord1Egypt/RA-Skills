"""
HTML 报表生成器
支持 PC / Pad / 手机响应式布局，集成 Chart.js 图表统计
"""
import os
import json
from datetime import datetime
from typing import Dict, Any

from config import OUTPUT_DIR
from utils import format_date_display, format_date_range_display, generate_report_filename, write_html_file

# 暂无数据占位 HTML
NO_DATA_HTML = '<div class="no-data-placeholder"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>暂无数据</div>'

CSS = """
        *, *::before, *::after {
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", "PingFang SC", "Helvetica Neue", Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 16px;
            background: #f0f2f5;
            color: #333;
            line-height: 1.6;
            -webkit-font-smoothing: antialiased;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 24px 28px;
            border-radius: 12px;
            margin-bottom: 16px;
            box-shadow: 0 4px 16px rgba(102, 126, 234, 0.3);
        }
        .header h1 {
            margin: 0 0 8px 0;
            font-size: 24px;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .header .date {
            font-size: 14px;
            opacity: 0.9;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .empty-notice {
            background: #fff8e1;
            color: #856404;
            border: 1px solid #ffe082;
            border-radius: 8px;
            padding: 12px 16px;
            margin-bottom: 16px;
            font-size: 14px;
            text-align: center;
        }
        .section {
            background: white;
            padding: 20px 24px;
            margin-bottom: 16px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }
        .section h2 {
            color: #333;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
            margin: 0 0 16px 0;
            font-size: 18px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .section h3 {
            font-size: 15px;
            color: #555;
            margin: 16px 0 10px 0;
        }
        .section h4 {
            font-size: 14px;
            color: #666;
            margin: 12px 0 8px 0;
        }
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 12px;
            margin-bottom: 12px;
        }
        .metric {
            background: #f8f9fa;
            padding: 14px 16px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }
        .metric:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }
        .metric-value {
            font-size: 22px;
            font-weight: bold;
            color: #667eea;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .metric-icon {
            width: 18px;
            height: 18px;
            flex-shrink: 0;
            opacity: 0.6;
        }
        .metric-unit {
            font-size: 13px;
            font-weight: normal;
            color: #888;
            margin-left: 2px;
        }
        .metric-label {
            font-size: 13px;
            color: #666;
            margin-top: 4px;
        }
        .chart-container {
            position: relative;
            width: 100%;
            max-width: 100%;
            margin: 16px 0;
            padding: 12px;
            background: #fafbfc;
            border-radius: 8px;
            border: 1px solid #eee;
        }
        .chart-container canvas {
            max-width: 100%;
            height: auto;
        }
        .chart-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin: 16px 0;
        }
        .chart-row .chart-container {
            margin: 0;
        }
        .table-responsive {
            width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            border-radius: 8px;
            border: 1px solid #e8e8e8;
            margin-top: 12px;
        }
        .compliance-table {
            width: 100%;
            border-collapse: collapse;
            table-layout: fixed;
        }
        .compliance-table.compliance-metrics-table {
            min-width: 520px;
        }
        .compliance-table.score-table {
            min-width: 680px;
        }
        .compliance-table th,
        .compliance-table td {
            padding: 10px 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
            word-wrap: break-word;
            overflow-wrap: break-word;
            vertical-align: top;
        }
        .compliance-table th {
            background: #f8f9fa;
            font-weight: 600;
            color: #444;
            white-space: nowrap;
            position: sticky;
            top: 0;
            z-index: 1;
        }
        .compliance-table.compliance-metrics-table th:nth-child(1) { width: 22%; }
        .compliance-table.compliance-metrics-table th:nth-child(2) { width: 14%; }
        .compliance-table.compliance-metrics-table th:nth-child(3) { width: 10%; }
        .compliance-table.compliance-metrics-table th:nth-child(4) { width: 54%; }
        .compliance-table.score-table th:nth-child(1) { width: 20%; }
        .compliance-table.score-table th:nth-child(2) { width: 14%; }
        .compliance-table.score-table th:nth-child(3) { width: 12%; }
        .compliance-table.score-table th:nth-child(4) { width: 14%; }
        .compliance-table.score-table th:nth-child(5) { width: 12%; }
        .compliance-table.score-table th:nth-child(6) { width: 12%; }
        .compliance-table.score-table th,
        .compliance-table.score-table td {
            text-align: center;
            white-space: nowrap;
        }
        .compliance-table.score-table th:nth-child(1),
        .compliance-table.score-table td:nth-child(1) {
            text-align: left;
            white-space: normal;
        }
        .compliance-table tbody tr:hover {
            background: #f5f7ff;
        }
        .compliance-table tbody tr:last-child td {
            border-bottom: none;
        }
        .status-badge {
            display: inline-block;
            padding: 2px 10px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: 600;
            white-space: nowrap;
        }
        .status-normal { background: #d4edda; color: #155724; }
        .status-warning { background: #fff3cd; color: #856404; }
        .status-danger { background: #f8d7da; color: #721c24; }
        .performer-card {
            background: #f8f9fa;
            padding: 14px 16px;
            margin: 8px 0;
            border-radius: 8px;
            border-left: 4px solid #28a745;
        }
        .performer-card.warning {
            border-left-color: #ffc107;
        }
        .performer-card .rank {
            font-size: 16px;
            font-weight: bold;
            color: #28a745;
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 6px;
        }
        .performer-card.warning .rank {
            color: #ffc107;
        }
        .performer-card p {
            margin: 4px 0 0 0;
            font-size: 13px;
            color: #555;
        }
        .lead-levels-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin: 12px 0;
        }
        .lead-level-card {
            border-radius: 8px;
            padding: 16px;
            text-align: center;
        }
        .lead-level-card .lead-count {
            font-size: 32px;
            font-weight: bold;
            margin: 8px 0;
        }
        .lead-level-card .lead-label {
            font-size: 14px;
            font-weight: 600;
        }
        .lead-level-card .lead-desc {
            font-size: 12px;
            margin-top: 8px;
            line-height: 1.5;
        }
        .lead-a-card { background: linear-gradient(135deg, #d4edda, #c3e6cb); color: #155724; }
        .lead-b-card { background: linear-gradient(135deg, #fff3cd, #ffeeba); color: #856404; }
        .lead-c-card { background: linear-gradient(135deg, #f8d7da, #f5c6cb); color: #721c24; }
        .suggestion {
            background: #e7f3ff;
            padding: 14px 16px;
            margin: 8px 0;
            border-radius: 8px;
            border-left: 4px solid #2196F3;
        }
        .suggestion h4 {
            margin: 0 0 6px 0;
            color: #1976D2;
            font-size: 15px;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .suggestion p {
            margin: 0;
            font-size: 13px;
            color: #444;
        }
        .distribution-list {
            margin: 8px 0;
            padding-left: 20px;
        }
        .distribution-list li {
            padding: 4px 0;
            font-size: 14px;
            color: #555;
        }
        .no-data-placeholder {
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
            color: #bbb;
            font-size: 14px;
            gap: 8px;
        }
        .no-data-placeholder svg {
            width: 20px;
            height: 20px;
            opacity: 0.5;
        }
        .footer {
            text-align: center;
            color: #999;
            padding: 16px;
            font-size: 12px;
        }
        .icon {
            display: inline-block;
            width: 20px;
            height: 20px;
            vertical-align: middle;
            flex-shrink: 0;
        }
        .icon-large { width: 28px; height: 28px; }
        .section h2 .icon { width: 22px; height: 22px; }
        .metric-icon {
            display: inline-block;
            width: 16px;
            height: 16px;
            vertical-align: text-bottom;
            opacity: 0.7;
            flex-shrink: 0;
        }
        .header .icon { width: 28px; height: 28px; vertical-align: middle; }

        @media screen and (max-width: 1024px) {
            body { padding: 12px; }
            .header { padding: 20px; }
            .header h1 { font-size: 20px; }
            .section { padding: 16px 18px; }
            .metrics-grid { grid-template-columns: repeat(2, 1fr); }
            .chart-row { grid-template-columns: 1fr; }
            .lead-levels-grid { grid-template-columns: repeat(3, 1fr); }
            .compliance-table th, .compliance-table td { padding: 8px 10px; font-size: 13px; }
        }
        @media screen and (max-width: 767px) {
            body { padding: 8px; }
            .header { padding: 16px; border-radius: 8px; }
            .header h1 { font-size: 17px; flex-wrap: wrap; }
            .header .date { font-size: 12px; }
            .section { padding: 14px; margin-bottom: 12px; border-radius: 8px; }
            .section h2 { font-size: 15px; padding-bottom: 8px; margin-bottom: 12px; }
            .section h3 { font-size: 14px; }
            .metrics-grid { grid-template-columns: repeat(2, 1fr); gap: 8px; }
            .metric { padding: 10px 12px; }
            .metric-value { font-size: 18px; }
            .metric-label { font-size: 11px; }
            .chart-row { grid-template-columns: 1fr; gap: 12px; }
            .chart-container { padding: 8px; }
            .lead-levels-grid { grid-template-columns: 1fr; gap: 8px; }
            .lead-level-card .lead-count { font-size: 26px; }
            .performer-card { padding: 12px; }
            .performer-card .rank { font-size: 14px; }
            .suggestion { padding: 12px; }
            .compliance-table.compliance-metrics-table { min-width: 480px; }
            .compliance-table.score-table { min-width: 680px; }
            .compliance-table th, .compliance-table td { padding: 8px 8px; font-size: 12px; }
        }
        @media screen and (max-width: 479px) {
            .header h1 { font-size: 15px; }
            .metrics-grid { grid-template-columns: 1fr 1fr; gap: 6px; }
            .metric { padding: 8px 10px; }
            .metric-value { font-size: 16px; }
            .metric-label { font-size: 10px; }
        }
"""


class SimpleHTMLGenerator:
    """简单 HTML 生成器（不依赖 Jinja2）"""

    def generate(self, analysis: Dict[str, Any], context: Dict[str, Any]) -> str:
        """生成 HTML 报表"""
        report_title = "系统驾驶舱报告"
        start_time = context.get('date_str', '')
        end_time = context.get('end_time', start_time)
        date_display = format_date_range_display(start_time, end_time)
        is_empty = context.get('is_empty', False)

        chart_data = self._build_chart_data(analysis)

        empty_notice = ''
        if is_empty:
            empty_notice = '\n    <div class="empty-notice">当前查询周期暂无录音数据，以下指标均为 0。</div>\n'

        # ===== 第一板块图表 =====
        if is_empty:
            section1_charts = f"""
        <div class="chart-row">
            <div class="chart-container">
                <h3 style="margin-top:0;display:flex;align-items:center;gap:6px;"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>客群结构分布</h3>
                {NO_DATA_HTML}
            </div>
            <div class="chart-container">
                <h3 style="margin-top:0;display:flex;align-items:center;gap:6px;"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>区域拜访分布</h3>
                {NO_DATA_HTML}
            </div>
        </div>
"""
        else:
            section1_charts = """
        <div class="chart-row">
            <div class="chart-container">
                <h3 style="margin-top:0;display:flex;align-items:center;gap:6px;"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>客群结构分布</h3>
                <canvas id="customerDistChart"></canvas>
            </div>
            <div class="chart-container">
                <h3 style="margin-top:0;display:flex;align-items:center;gap:6px;"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>区域拜访分布</h3>
                <canvas id="regionChart"></canvas>
            </div>
        </div>
"""

        # 产业带轨迹分布
        regions = analysis['daily_efficiency']['regional_distribution']
        if not regions:
            regional_list = f'            {NO_DATA_HTML}\n'
        else:
            regional_list = ''
            for region in regions:
                regional_list += f"""            <li style="display:flex;align-items:center;gap:8px;padding:6px 0;"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>{region.get('region', '未知区域')}（{region.get('visit_count', 0)} 笔实地）</li>
"""

        # ===== 第二板块：合规监控 =====
        compliance_metrics = analysis['compliance_monitoring']['compliance_metrics']
        if is_empty or not compliance_metrics:
            compliance_chart = f"""        <div class="chart-container">
            <h3 style="margin-top:0;display:flex;align-items:center;gap:6px;"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>合规指标达成率总览</h3>
            {NO_DATA_HTML}
        </div>
"""
            compliance_tbody = f'                    <tr><td colspan="4">{NO_DATA_HTML}</td></tr>\n'
        else:
            compliance_chart = """        <div class="chart-container">
            <h3 style="margin-top:0;display:flex;align-items:center;gap:6px;"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>合规指标达成率总览</h3>
            <canvas id="complianceChart"></canvas>
        </div>
"""
            compliance_tbody = ''
            for metric in compliance_metrics:
                status_class = 'status-normal'
                if metric.get('status') == '警告':
                    status_class = 'status-warning'
                elif metric.get('status') == '危险':
                    status_class = 'status-danger'
                compliance_tbody += f"""                    <tr>
                        <td>{metric.get('metric_name', '')}</td>
                        <td>{metric.get('achievement_rate', '')}</td>
                        <td><span class="status-badge {status_class}">{metric.get('status', '')}</span></td>
                        <td>{metric.get('ai_audit_opinion', '')}</td>
                    </tr>
"""

        # ===== 第三板块：RM 业务水平 =====
        user_scores = analysis['rm_performance'].get('user_scores', [])
        top_performers = analysis['rm_performance']['top_performers']
        needs_improvement = analysis['rm_performance']['needs_improvement']
        all_performers = top_performers + needs_improvement
        chart_source = user_scores if user_scores else all_performers

        if is_empty and not chart_source:
            rm_section = f'        {NO_DATA_HTML}\n'
            rm_score_table = ''
        else:
            rm_section = ''
            if chart_source:
                rm_section += """        <div class="chart-container">
            <h3 style="margin-top:0;display:flex;align-items:center;gap:6px;"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><line x1="18" y1="20" x2="18" y2="10"/><line x1="12" y1="20" x2="12" y2="4"/><line x1="6" y1="20" x2="6" y2="14"/></svg>RM 得分排行</h3>
            <canvas id="rmScoreChart"></canvas>
        </div>
"""
            for performer in top_performers:
                rm_section += f"""        <div class="performer-card">
            <div class="rank"><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#28a745" stroke-width="2"><circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/></svg>第{performer.get('rank', '')}名：{performer.get('region', '')}・{performer.get('name', '')}（{performer.get('score', 0)} 分）</div>
            <p><strong>销冠行为描述：</strong>{performer.get('behavior_description', '')}</p>
        </div>
"""
            for performer in needs_improvement:
                rm_section += f"""        <div class="performer-card warning">
            <div class="rank"><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#ffc107" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>待提升：{performer.get('region', '')}・{performer.get('name', '')}（{performer.get('score', 0)} 分）</div>
            <p><strong>问题诊断：</strong>{performer.get('problem_diagnosis', '')}</p>
        </div>
"""

            rm_score_table = ''
            if user_scores:
                score_rows = ''
                for user in user_scores:
                    score_rows += f"""                    <tr>
                        <td>{user.get('user_name', '')}</td>
                        <td>{user.get('recording_count', 0)} 条</td>
                        <td>{user.get('total_score', 0)} 分</td>
                        <td>{user.get('avg_score', 0):.1f} 分</td>
                        <td>{user.get('top_score', 0)} 分</td>
                        <td>{user.get('min_score', 0)} 分</td>
                    </tr>
"""
                rm_score_table = f"""
        <h3 style="display:flex;align-items:center;gap:6px;margin-top:20px;"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>成员得分统计</h3>
        <div class="chart-container">
            <canvas id="userScoreChart"></canvas>
        </div>
        <div class="table-responsive">
            <table class="compliance-table score-table">
                <thead>
                    <tr>
                        <th>成员姓名</th>
                        <th>录音条数</th>
                        <th>总分</th>
                        <th>平均分</th>
                        <th>最高分</th>
                        <th>最低分</th>
                    </tr>
                </thead>
                <tbody>
{score_rows}                </tbody>
            </table>
        </div>
"""

        # ===== 第四板块：线索转化 =====
        lead = analysis.get('lead_conversion', {})
        has_lead_data = any([
            lead.get('a_level_count', 0),
            lead.get('b_level_count', 0),
            lead.get('c_level_count', 0)
        ])
        if is_empty or not has_lead_data:
            lead_chart = f"""        <div class="chart-container">
            <h3 style="margin-top:0;display:flex;align-items:center;gap:6px;"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>线索意向分级占比</h3>
            {NO_DATA_HTML}
        </div>
"""
        else:
            lead_chart = """        <div class="chart-container">
            <h3 style="margin-top:0;display:flex;align-items:center;gap:6px;"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/></svg>线索意向分级占比</h3>
            <canvas id="leadChart"></canvas>
        </div>
"""

        # 管理建议
        suggestions_html = ''
        for suggestion in analysis['management_suggestions']:
            suggestions_html += f"""        <div class="suggestion">
            <h4><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#1976D2" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>{suggestion.get('title', '')}</h4>
            <p>{suggestion.get('content', '')}</p>
        </div>
"""
        if not suggestions_html:
            suggestions_html = f'        {NO_DATA_HTML}\n'

        # ===== 组装完整 HTML =====
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0">
    <title>{report_title}</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
    <style>{CSS}
    </style>
</head>
<body>
    <div class="header">
        <h1><svg class="icon icon-large" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 3v18h18"/><path d="M18.7 8l-5.1 5.2-2.8-2.7L7 14.3"/></svg>{report_title}</h1>
        <div class="date"><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>数据日期：{date_display}</div>
    </div>
{empty_notice}
    <!-- 团队资产沉淀大盘 -->
    <div class="section">
        <h2><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>团队资产沉淀大盘（长期累积维度）</h2>
        <div class="metrics-grid">
            <div class="metric">
                <div class="metric-value"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>{analysis['team_assets']['total_customers']}<span class="metric-unit">条</span></div>
                <div class="metric-label">历史累积拜访客户总量</div>
            </div>
            <div class="metric">
                <div class="metric-value"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>{analysis['team_assets']['month_customers']}<span class="metric-unit">条</span></div>
                <div class="metric-label">本月至今累积拜访</div>
            </div>
            <div class="metric">
                <div class="metric-value"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>{analysis['team_assets']['today_customers']}<span class="metric-unit">条</span></div>
                <div class="metric-label">今日新增实地拜访</div>
            </div>
            <div class="metric">
                <div class="metric-value"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>{analysis['team_assets']['avg_per_person']}<span class="metric-unit">人</span></div>
                <div class="metric-label">人均长期维护客群深度</div>
            </div>
        </div>
    </div>

    <!-- 每日外勤实地效能监测 -->
    <div class="section">
        <h2><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><circle cx="12" cy="10" r="3"/><path d="M12 21.7C17.3 17 20 13 20 10a8 8 0 1 0-16 0c0 3 2.7 7 8 11.7z"/></svg>第一板块：每日外勤实地效能监测</h2>
        <h3>1. 今日实地拜访核心漏斗</h3>
        <div class="metrics-grid">
            <div class="metric">
                <div class="metric-value"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/><path d="M19 10v2a7 7 0 0 1-14 0v-2"/><line x1="12" y1="19" x2="12" y2="23"/><line x1="8" y1="23" x2="16" y2="23"/></svg>{analysis['daily_efficiency']['total_recording_minutes']}<span class="metric-unit">分钟</span></div>
                <div class="metric-label">录音总时长</div>
            </div>
            <div class="metric">
                <div class="metric-value"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>{analysis['daily_efficiency']['avg_minutes_per_person']:.1f}<span class="metric-unit">分钟</span></div>
                <div class="metric-label">人均面谈时长</div>
            </div>
            <div class="metric">
                <div class="metric-value"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>{analysis['daily_efficiency']['total_visits']}<span class="metric-unit">条</span></div>
                <div class="metric-label">实地有效面谈总数</div>
            </div>
            <div class="metric">
                <div class="metric-value"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>{analysis['daily_efficiency']['avg_visits_per_person']:.1f}<span class="metric-unit">次</span></div>
                <div class="metric-label">人均探店次数</div>
            </div>
        </div>
{section1_charts}
        <h4 style="display:flex;align-items:center;gap:6px;"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>今日产业带轨迹分布</h4>
        <ul class="distribution-list" style="list-style:none;padding-left:0;">
{regional_list}        </ul>
    </div>

    <!-- 当日合规与红线监控 -->
    <div class="section">
        <h2><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>第二板块：当日合规与红线监控红绿灯</h2>
{compliance_chart}
        <div class="table-responsive">
            <table class="compliance-table compliance-metrics-table">
                <thead>
                    <tr>
                        <th>监控指标</th>
                        <th>达成率</th>
                        <th>状态</th>
                        <th>AI 每日穿透审计意见</th>
                    </tr>
                </thead>
                <tbody>
{compliance_tbody}                </tbody>
            </table>
        </div>
    </div>

    <!-- 当日 RM 业务水平 -->
    <div class="section">
        <h2><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5C7 4 7 7 7 7"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5C17 4 17 7 17 7"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20.24 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20.24 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>第三板块：当日 RM 业务水平</h2>
        <h3 style="display:flex;align-items:center;gap:6px;"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z"/></svg>今日团队沟通技能得分排行（百分制）</h3>
{rm_section}{rm_score_table}    </div>

    <!-- 当日线索转化效率 -->
    <div class="section">
        <h2><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>第四板块：当日线索转化效率与前置风控</h2>
        <h3 style="display:flex;align-items:center;gap:6px;"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>今日实地录音客户意向分级</h3>

{lead_chart}
        <div class="lead-levels-grid">
            <div class="lead-level-card lead-a-card">
                <div class="lead-label"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-right:4px;"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>A 级商机</div>
                <div class="lead-count">{analysis['lead_conversion']['a_level_count']}</div>
                <div class="lead-desc">{analysis['lead_conversion']['a_level_details']}</div>
            </div>
            <div class="lead-level-card lead-b-card">
                <div class="lead-label"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-right:4px;"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>B 级商机</div>
                <div class="lead-count">{analysis['lead_conversion']['b_level_count']}</div>
                <div class="lead-desc">{analysis['lead_conversion']['b_level_followup']}</div>
            </div>
            <div class="lead-level-card lead-c-card">
                <div class="lead-label"><svg class="metric-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="vertical-align:middle;margin-right:4px;"><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>C 级商机</div>
                <div class="lead-count">{analysis['lead_conversion']['c_level_count']}</div>
                <div class="lead-desc">{analysis['lead_conversion']['c_level_interception']}</div>
            </div>
        </div>
    </div>

    <!-- 管理者跟进与靶向督导建议 -->
    <div class="section">
        <h2><svg class="icon" viewBox="0 0 24 24" fill="none" stroke="#667eea" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>管理者跟进与靶向督导建议</h2>
{suggestions_html}    </div>

    <div class="footer">
        <p>数据来源：AI教练 | 由 LegionClaw 管理驾驶舱生成 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </div>

    <script>
    {self._build_chart_script(chart_data)}
    </script>
</body>
</html>
"""

        # 保存文件
        filename = generate_report_filename(
            context.get('date_str', ''),
            context.get('end_time', ''),
        )
        file_path = os.path.join(OUTPUT_DIR, filename)
        write_html_file(file_path, html)
        return file_path

    def _build_chart_data(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """从分析数据中提取图表数据"""
        chart_data = {}

        cust_dist = analysis.get('daily_efficiency', {}).get('customer_distribution', {})
        chart_data['customer_dist'] = {
            'labels': ['老客维护与转介绍', '陌生新商圈扫街'],
            'values': [
                cust_dist.get('old_customer_maintenance', 0),
                cust_dist.get('new_customer_prospecting', 0)
            ]
        }

        regions = analysis.get('daily_efficiency', {}).get('regional_distribution', [])
        chart_data['region_dist'] = {
            'labels': [r.get('region', '未知') for r in regions],
            'values': [r.get('visit_count', 0) for r in regions]
        }

        compliance = analysis.get('compliance_monitoring', {}).get('compliance_metrics', [])
        chart_data['compliance'] = {
            'labels': [m.get('metric_name', '') for m in compliance],
            'values': [self._parse_rate(m.get('achievement_rate', '0%')) for m in compliance],
            'statuses': [m.get('status', '正常') for m in compliance]
        }

        user_scores = analysis.get('rm_performance', {}).get('user_scores', [])
        if user_scores:
            chart_data['rm_scores'] = {
                'labels': [u.get('user_name', '') for u in user_scores],
                'values': [u.get('avg_score', 0) for u in user_scores],
                'colors': ['#28a745' if u.get('avg_score', 0) >= 60 else '#ffc107' for u in user_scores]
            }
        else:
            top = analysis.get('rm_performance', {}).get('top_performers', [])
            low = analysis.get('rm_performance', {}).get('needs_improvement', [])
            all_rm = top + low
            chart_data['rm_scores'] = {
                'labels': [f"{p.get('name', '')}" for p in all_rm],
                'values': [p.get('score', 0) for p in all_rm],
                'colors': ['#28a745' if p in top else '#ffc107' for p in all_rm]
            }

        lead = analysis.get('lead_conversion', {})
        chart_data['lead_conversion'] = {
            'labels': ['A 级商机', 'B 级商机', 'C 级商机'],
            'values': [
                lead.get('a_level_count', 0),
                lead.get('b_level_count', 0),
                lead.get('c_level_count', 0)
            ]
        }

        chart_data['user_scores'] = {
            'labels': [u.get('user_name', '') for u in user_scores],
            'values': [u.get('avg_score', 0) for u in user_scores],
            'counts': [u.get('recording_count', 0) for u in user_scores]
        }

        return chart_data

    def _parse_rate(self, rate_str: str) -> float:
        """解析百分比字符串为数值"""
        try:
            return float(rate_str.replace('%', '').strip())
        except (ValueError, AttributeError):
            return 0.0

    def _build_chart_script(self, chart_data: Dict[str, Any]) -> str:
        """生成 Chart.js 初始化 JavaScript 代码"""
        data_json = json.dumps(chart_data, ensure_ascii=False)

        script = f"""
    (function() {{
        var data = {data_json};
        var isMobile = window.innerWidth < 768;
        var fontSize = isMobile ? 10 : 12;
        var titleFontSize = isMobile ? 12 : 14;

        Chart.defaults.font.size = fontSize;
        Chart.defaults.font.family = '-apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif';

        // 客群结构分布 - 饼图
        if (data.customer_dist && data.customer_dist.values.some(function(v) {{ return v > 0; }})) {{
            new Chart(document.getElementById('customerDistChart'), {{
                type: 'pie',
                data: {{
                    labels: data.customer_dist.labels,
                    datasets: [{{
                        data: data.customer_dist.values,
                        backgroundColor: ['#667eea', '#f97316'],
                        borderWidth: 2,
                        borderColor: '#fff'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {{
                        legend: {{
                            position: 'bottom',
                            labels: {{ padding: isMobile ? 8 : 16, font: {{ size: fontSize }} }}
                        }}
                    }}
                }}
            }});
        }}

        // 区域拜访分布 - 柱状图
        if (data.region_dist && data.region_dist.labels.length > 0) {{
            new Chart(document.getElementById('regionChart'), {{
                type: 'bar',
                data: {{
                    labels: data.region_dist.labels,
                    datasets: [{{
                        label: '拜访笔数',
                        data: data.region_dist.values,
                        backgroundColor: 'rgba(102, 126, 234, 0.7)',
                        borderColor: '#667eea',
                        borderWidth: 1,
                        borderRadius: 4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        y: {{ beginAtZero: true, ticks: {{ stepSize: 1, font: {{ size: fontSize }} }} }},
                        x: {{ ticks: {{ font: {{ size: fontSize }}, maxRotation: 45, minRotation: 0 }} }}
                    }}
                }}
            }});
        }}

        // 合规指标达成率 - 折线图
        if (data.compliance && data.compliance.labels.length > 0) {{
            var pointColors = data.compliance.statuses.map(function(s) {{
                if (s === '危险') return '#dc3545';
                if (s === '警告') return '#ffc107';
                return '#28a745';
            }});
            new Chart(document.getElementById('complianceChart'), {{
                type: 'line',
                data: {{
                    labels: data.compliance.labels,
                    datasets: [{{
                        label: '达成率 (%)',
                        data: data.compliance.values,
                        borderColor: '#667eea',
                        backgroundColor: 'rgba(102, 126, 234, 0.1)',
                        fill: true,
                        tension: 0.3,
                        pointBackgroundColor: pointColors,
                        pointBorderColor: pointColors,
                        pointRadius: isMobile ? 4 : 6,
                        pointHoverRadius: isMobile ? 6 : 8
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{ callbacks: {{ label: function(ctx) {{ return ctx.parsed.y + '%'; }} }} }}
                    }},
                    scales: {{
                        y: {{ beginAtZero: true, max: 100, ticks: {{ callback: function(v) {{ return v + '%'; }}, font: {{ size: fontSize }} }} }},
                        x: {{ ticks: {{ font: {{ size: fontSize }}, maxRotation: 45, minRotation: 0 }} }}
                    }}
                }}
            }});
        }}

        // RM 得分排行 - 柱状图
        if (data.rm_scores && data.rm_scores.labels.length > 0) {{
            new Chart(document.getElementById('rmScoreChart'), {{
                type: 'bar',
                data: {{
                    labels: data.rm_scores.labels,
                    datasets: [{{
                        label: '得分',
                        data: data.rm_scores.values,
                        backgroundColor: data.rm_scores.colors.map(function(c) {{ return c + 'b3'; }}),
                        borderColor: data.rm_scores.colors,
                        borderWidth: 1,
                        borderRadius: 4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: true,
                    indexAxis: isMobile ? 'y' : 'x',
                    plugins: {{ legend: {{ display: false }} }},
                    scales: {{
                        x: {{ beginAtZero: true, max: 100, ticks: {{ font: {{ size: fontSize }} }} }},
                        y: {{ ticks: {{ font: {{ size: fontSize }} }} }}
                    }}
                }}
            }});
        }}

        // 线索转化 - 饼图
        if (data.lead_conversion && data.lead_conversion.values.some(function(v) {{ return v > 0; }})) {{
            new Chart(document.getElementById('leadChart'), {{
                type: 'doughnut',
                data: {{
                    labels: data.lead_conversion.labels,
                    datasets: [{{
                        data: data.lead_conversion.values,
                        backgroundColor: ['#28a745', '#ffc107', '#dc3545'],
                        borderWidth: 2,
                        borderColor: '#fff'
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: true,
                    plugins: {{
                        legend: {{ position: 'bottom', labels: {{ padding: isMobile ? 8 : 16, font: {{ size: fontSize }} }} }}
                    }}
                }}
            }});
        }}

        // 成员得分统计 - 柱状图
        if (data.user_scores && data.user_scores.labels.length > 0) {{
            new Chart(document.getElementById('userScoreChart'), {{
                type: 'bar',
                data: {{
                    labels: data.user_scores.labels,
                    datasets: [{{
                        label: '平均分',
                        data: data.user_scores.values,
                        backgroundColor: 'rgba(102, 126, 234, 0.7)',
                        borderColor: '#667eea',
                        borderWidth: 1,
                        borderRadius: 4
                    }}]
                }},
                options: {{
                    responsive: true,
                    maintainAspectRatio: true,
                    indexAxis: isMobile ? 'y' : 'x',
                    plugins: {{
                        legend: {{ display: false }},
                        tooltip: {{
                            callbacks: {{
                                afterLabel: function(ctx) {{
                                    var count = data.user_scores.counts[ctx.dataIndex];
                                    return '录音条数：' + count + ' 条';
                                }}
                            }}
                        }}
                    }},
                    scales: {{
                        x: {{ beginAtZero: true, max: 100, ticks: {{ font: {{ size: fontSize }} }} }},
                        y: {{ ticks: {{ font: {{ size: fontSize }} }} }}
                    }}
                }}
            }});
        }}
    }})();
"""
        return script
