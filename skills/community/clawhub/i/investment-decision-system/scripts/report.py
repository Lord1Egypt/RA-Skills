"""
Investment Decision System - HTML Report Generator
Generates interactive HTML reports: dashboard, decision review, portfolio analysis.
"""

import json
import os
from datetime import datetime


def _get_db():
    """Lazy import to avoid circular dependency issues."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "db", os.path.join(os.path.dirname(__file__), "db.py"))
    db = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(db)
    return db


def generate_css():
    """Generate shared CSS for all reports."""
    return """
    :root {
        --bg: #f8fafc;
        --card-bg: #ffffff;
        --text: #1e293b;
        --text-secondary: #64748b;
        --border: #e2e8f0;
        --primary: #3b82f6;
        --success: #22c55e;
        --warning: #eab308;
        --danger: #ef4444;
        --orange: #f97316;
        --radius: 12px;
        --shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06);
    }
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC',
                     'Microsoft YaHei', sans-serif;
        background: var(--bg);
        color: var(--text);
        line-height: 1.6;
        padding: 20px;
    }
    .container { max-width: 1200px; margin: 0 auto; }
    .header {
        text-align: center;
        padding: 30px 0;
        border-bottom: 2px solid var(--border);
        margin-bottom: 30px;
    }
    .header h1 { font-size: 28px; color: var(--text); }
    .header .subtitle { color: var(--text-secondary); margin-top: 8px; }
    .header .date { color: var(--text-secondary); font-size: 14px; }

    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 16px;
        margin-bottom: 24px;
    }
    .stat-card {
        background: var(--card-bg);
        border-radius: var(--radius);
        padding: 20px;
        box-shadow: var(--shadow);
        border-left: 4px solid var(--primary);
    }
    .stat-card.danger { border-left-color: var(--danger); }
    .stat-card.success { border-left-color: var(--success); }
    .stat-card.warning { border-left-color: var(--warning); }
    .stat-card .label { font-size: 13px; color: var(--text-secondary); margin-bottom: 6px; }
    .stat-card .value { font-size: 28px; font-weight: 700; }
    .stat-card .sub { font-size: 12px; color: var(--text-secondary); margin-top: 4px; }

    .card {
        background: var(--card-bg);
        border-radius: var(--radius);
        padding: 24px;
        box-shadow: var(--shadow);
        margin-bottom: 24px;
    }
    .card h2 {
        font-size: 18px;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid var(--border);
        display: flex; align-items: center; gap: 8px;
    }

    .radar-container {
        display: flex;
        justify-content: center;
        padding: 20px 0;
    }

    .bar-row {
        display: flex;
        align-items: center;
        margin-bottom: 12px;
        gap: 12px;
    }
    .bar-label {
        width: 100px;
        font-size: 14px;
        font-weight: 500;
        text-align: right;
        flex-shrink: 0;
    }
    .bar-track {
        flex: 1;
        height: 24px;
        background: #f1f5f9;
        border-radius: 12px;
        overflow: hidden;
    }
    .bar-fill {
        height: 100%;
        border-radius: 12px;
        transition: width 0.6s ease;
        display: flex;
        align-items: center;
        justify-content: flex-end;
        padding-right: 8px;
        font-size: 12px;
        font-weight: 600;
        color: white;
        min-width: 30px;
    }
    .bar-fill.good { background: linear-gradient(90deg, #22c55e, #16a34a); }
    .bar-fill.warning { background: linear-gradient(90deg, #eab308, #ca8a04); }
    .bar-fill.danger { background: linear-gradient(90deg, #ef4444, #dc2626); }

    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 14px;
    }
    th, td {
        padding: 12px 16px;
        text-align: left;
        border-bottom: 1px solid var(--border);
    }
    th {
        background: #f8fafc;
        font-weight: 600;
        color: var(--text-secondary);
        font-size: 12px;
        text-transform: uppercase;
    }
    tr:hover { background: #f8fafc; }

    .badge {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    .badge.good { background: #dcfce7; color: #16a34a; }
    .badge.warning { background: #fef9c3; color: #ca8a04; }
    .badge.danger { background: #fee2e2; color: #dc2626; }
    .badge.info { background: #dbeafe; color: #2563eb; }

    .pnl-positive { color: #ef4444; font-weight: 600; }
    .pnl-negative { color: #22c55e; font-weight: 600; }

    .action-list { list-style: none; }
    .action-list li {
        padding: 10px 16px;
        margin-bottom: 8px;
        border-radius: 8px;
        background: #f8fafc;
        border-left: 4px solid var(--primary);
    }
    .action-list li.P0 { border-left-color: var(--danger); background: #fef2f2; }
    .action-list li.P1 { border-left-color: var(--warning); background: #fefce8; }
    .action-list li.P2 { border-left-color: var(--primary); background: #eff6ff; }

    .grid-2 {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 24px;
    }
    @media (max-width: 768px) {
        .grid-2 { grid-template-columns: 1fr; }
        .stats-grid { grid-template-columns: repeat(2, 1fr); }
    }

    .donut-container {
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
    }
    .legend { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 12px; }
    .legend-item { display: flex; align-items: center; gap: 6px; font-size: 13px; }
    .legend-color { width: 12px; height: 12px; border-radius: 3px; }

    .summary-banner {
        padding: 16px 24px;
        border-radius: var(--radius);
        margin-bottom: 24px;
        font-weight: 600;
        font-size: 16px;
    }
    .summary-banner.good { background: #dcfce7; color: #16a34a; border: 1px solid #86efac; }
    .summary-banner.warning { background: #fef9c3; color: #a16207; border: 1px solid #fde047; }
    .summary-banner.danger { background: #fee2e2; color: #dc2626; border: 1px solid #fca5a5; }

    .footer {
        text-align: center;
        padding: 30px 0;
        color: var(--text-secondary);
        font-size: 12px;
    }
    """


def generate_svg_radar(scores, size=300):
    """Generate inline SVG radar chart for INVEST dimensions."""
    labels = ['意图', '数字', '价值', '优势', '安全', '时机']
    dim_keys = ['intent_score', 'numbers_score', 'value_score',
                'edge_score', 'safety_score', 'timing_score']

    values = [scores.get(k, 0) or 0 for k in dim_keys]
    n = len(labels)
    cx, cy = size / 2, size / 2
    max_r = size / 2 - 40

    svg_parts = [f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">']

    # Background grid
    for level in range(1, 6):
        r = max_r * level / 5
        points = []
        for i in range(n):
            angle = -90 + i * 360 / n
            rad = angle * 3.14159 / 180
            x = cx + r * __import__('math').cos(rad)
            y = cy + r * __import__('math').sin(rad)
            points.append(f"{x:.1f},{y:.1f}")
        svg_parts.append(f'<polygon points="{" ".join(points)}" fill="none" stroke="#e2e8f0" stroke-width="1"/>')

    # Axis lines
    for i in range(n):
        angle = -90 + i * 360 / n
        rad = angle * 3.14159 / 180
        x = cx + max_r * __import__('math').cos(rad)
        y = cy + max_r * __import__('math').sin(rad)
        svg_parts.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#e2e8f0" stroke-width="1"/>')

        # Label
        lx = cx + (max_r + 25) * __import__('math').cos(rad)
        ly = cy + (max_r + 25) * __import__('math').sin(rad)
        svg_parts.append(f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="middle" dominant-baseline="middle" font-size="13" fill="#475569" font-weight="600">{labels[i]}</text>')

        # Score label
        score_r = (max_r - 20) * 0
        sx = cx + score_r * __import__('math').cos(rad)
        sy = cy + score_r * __import__('math').sin(rad)

    # Data polygon
    data_points = []
    for i in range(n):
        angle = -90 + i * 360 / n
        rad = angle * 3.14159 / 180
        r = max_r * values[i] / 10
        x = cx + r * __import__('math').cos(rad)
        y = cy + r * __import__('math').sin(rad)
        data_points.append(f"{x:.1f},{y:.1f}")
    svg_parts.append(f'<polygon points="{" ".join(data_points)}" fill="#3b82f6" fill-opacity="0.3" stroke="#3b82f6" stroke-width="2"/>')

    # Data dots
    for i in range(n):
        angle = -90 + i * 360 / n
        rad = angle * 3.14159 / 180
        r = max_r * values[i] / 10
        x = cx + r * __import__('math').cos(rad)
        y = cy + r * __import__('math').sin(rad)
        svg_parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#3b82f6" stroke="white" stroke-width="2"/>')

    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


def generate_svg_donut(allocation, size=200):
    """Generate inline SVG donut chart for asset allocation."""
    colors = {
        'stock': '#ef4444', 'fund': '#3b82f6', 'bond': '#22c55e',
        'cash': '#94a3b8', 'crypto': '#f97316', 'other': '#8b5cf6',
    }
    cx, cy = size / 2, size / 2
    r = size / 2 - 15
    ir = r * 0.6

    svg_parts = [f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">']

    total = sum(allocation.values())
    if total == 0:
        svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#e2e8f0" stroke-width="{r - ir}"/>')
    else:
        start_angle = -90
        for asset, value in allocation.items():
            pct = value / total
            sweep = pct * 360
            if sweep < 0.5:
                start_angle += sweep
                continue

            color = colors.get(asset, '#94a3b8')

            start_rad = start_angle * 3.14159 / 180
            end_rad = (start_angle + sweep) * 3.14159 / 180

            x1 = cx + r * __import__('math').cos(start_rad)
            y1 = cy + r * __import__('math').sin(start_rad)
            x2 = cx + r * __import__('math').cos(end_rad)
            y2 = cy + r * __import__('math').sin(end_rad)
            ix1 = cx + ir * __import__('math').cos(start_rad)
            iy1 = cy + ir * __import__('math').sin(start_rad)
            ix2 = cx + ir * __import__('math').cos(end_rad)
            iy2 = cy + ir * __import__('math').sin(end_rad)

            large_arc = 1 if sweep > 180 else 0

            path = (
                f'M {x1:.1f} {y1:.1f} '
                f'A {r:.1f} {r:.1f} 0 {large_arc} 1 {x2:.1f} {y2:.1f} '
                f'L {ix2:.1f} {iy2:.1f} '
                f'A {ir:.1f} {ir:.1f} 0 {large_arc} 0 {ix1:.1f} {iy1:.1f} Z'
            )
            svg_parts.append(f'<path d="{path}" fill="{color}" stroke="white" stroke-width="2"/>')
            start_angle += sweep

    svg_parts.append(f'<circle cx="{cx}" cy="{cy}" r="{ir}" fill="white"/>')
    svg_parts.append(f'<text x="{cx}" y="{cy - 8}" text-anchor="middle" font-size="22" font-weight="700" fill="#1e293b">{total:.0f}%</text>')
    svg_parts.append(f'<text x="{cx}" y="{cy + 14}" text-anchor="middle" font-size="12" fill="#64748b">配置比例</text>')
    svg_parts.append('</svg>')
    return '\n'.join(svg_parts)


def generate_dashboard_html():
    """Generate investment dashboard HTML report."""
    db = _get_db()
    portfolio = db.get_portfolio_summary()
    profile = db.get_profile()
    stats = db.get_decision_stats()
    violations = db.check_risk_compliance()
    watchlist = db.get_watchlist()
    recent_decisions = db.get_all_decisions(limit=10)

    css = generate_css()
    total_val = portfolio['total_market_value'] or portfolio['total_cost'] or 0
    pnl_class = 'pnl-positive' if portfolio['total_pnl'] >= 0 else 'pnl-negative'

    # Asset allocation donut
    donut_svg = generate_svg_donut(portfolio['asset_allocation'])

    # Recent decisions table
    decision_rows = ""
    for d in recent_decisions:
        score_class = 'good' if d['total_score'] >= 7 else 'warning' if d['total_score'] >= 5 else 'danger'
        status_map = {'pending': '待执行', 'executed': '已执行', 'cancelled': '已取消', 'reviewed': '已复盘'}
        decision_rows += f"""
        <tr>
            <td>{d.get('name', d['symbol'])}</td>
            <td>{d['decision_type']}</td>
            <td><span class="badge {score_class}">{d['total_score']}</span></td>
            <td>{status_map.get(d['status'], d['status'])}</td>
            <td>{d.get('decision_date', '')}</td>
        </tr>"""

    # Holdings table
    holdings_rows = ""
    for h in portfolio['holdings']:
        mv = h['quantity'] * (h['current_price'] or h['avg_cost'])
        cost = h['quantity'] * h['avg_cost']
        pnl = mv - cost
        pnl_pct = (pnl / cost * 100) if cost > 0 else 0
        pnl_c = 'pnl-positive' if pnl >= 0 else 'pnl-negative'
        holdings_rows += f"""
        <tr>
            <td><strong>{h['symbol']}</strong></td>
            <td>{h.get('name', '')}</td>
            <td>{h['asset_class']}</td>
            <td>{h['quantity']}</td>
            <td>¥{h['avg_cost']:.2f}</td>
            <td>¥{mv:,.2f}</td>
            <td class="{pnl_c}">{pnl:+,.2f} ({pnl_pct:+.1f}%)</td>
        </tr>"""

    # Violations
    violations_html = ""
    if violations:
        for v in violations:
            sev_class = 'danger' if v['severity'] == 'high' else 'warning'
            violations_html += f'<li class="{v["severity"].upper()}" style="border-left-color: {"var(--danger)" if v["severity"]=="high" else "var(--warning)"}">{v["detail"]}</li>'
    else:
        violations_html = '<li style="border-left-color: var(--success); background: #f0fdf4;">✅ 当前持仓符合所有风控规则</li>'

    # Watchlist
    watchlist_rows = ""
    for w in watchlist:
        watchlist_rows += f"""
        <tr>
            <td><strong>{w['symbol']}</strong></td>
            <td>{w.get('name', '')}</td>
            <td>{w.get('reason', '')}</td>
            <td>{f"¥{w['target_price']:.2f}" if w['target_price'] else '-'}</td>
        </tr>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>投资决策仪表盘 - Investment Dashboard</title>
<style>{css}</style>
</head>
<body>
<div class="container">

<div class="header">
    <h1>📊 投资决策仪表盘</h1>
    <p class="subtitle">INVEST Decision System — 信息·资产·目标·纪律</p>
    <p class="date">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
</div>

<!-- Summary Stats -->
<div class="stats-grid">
    <div class="stat-card">
        <div class="label">持仓总市值</div>
        <div class="value">¥{total_val:,.0f}</div>
        <div class="sub">{portfolio['holding_count']} 个持仓</div>
    </div>
    <div class="stat-card {'success' if portfolio['total_pnl'] >= 0 else 'danger'}">
        <div class="label">浮动盈亏</div>
        <div class="value {pnl_class}">{portfolio['total_pnl']:+,.0f}</div>
        <div class="sub">{portfolio['total_pnl_pct']:+.1f}%</div>
    </div>
    <div class="stat-card success">
        <div class="label">决策胜率</div>
        <div class="value">{stats['win_rate']}%</div>
        <div class="sub">{stats['wins']}胜/{stats['losses']}负 ({stats['total_decisions']}笔)</div>
    </div>
    <div class="stat-card">
        <div class="label">累计已实现盈亏</div>
        <div class="value {pnl_class}">{stats['total_pnl']:+,.0f}</div>
        <div class="sub">盈亏比 {stats['profit_factor']}</div>
    </div>
</div>

<div class="grid-2">
    <!-- Asset Allocation -->
    <div class="card">
        <h2>📈 资产配置</h2>
        <div class="donut-container">{donut_svg}</div>
        <div class="legend">
            {''.join(f'<div class="legend-item"><div class="legend-color" style="background: {"#ef4444" if k=="stock" else "#3b82f6" if k=="fund" else "#22c55e" if k=="bond" else "#94a3b8" if k=="cash" else "#f97316" if k=="crypto" else "#8b5cf6"}"></div>{k}: {v}%</div>' for k, v in portfolio['asset_allocation'].items())}
        </div>
    </div>

    <!-- Risk Compliance -->
    <div class="card">
        <h2>🛡️ 风控合规检查</h2>
        <ul class="action-list">{violations_html}</ul>
        <div style="margin-top: 12px; font-size: 13px; color: var(--text-secondary);">
            投资目标: {profile.get('investment_goal', '未设置')} | 风险偏好: {profile.get('risk_tolerance', '未设置')} | 时间维度: {profile.get('time_horizon', '未设置')}
        </div>
    </div>
</div>

<!-- Holdings -->
<div class="card">
    <h2>💼 当前持仓</h2>
    <table>
        <thead>
            <tr><th>代码</th><th>名称</th><th>类型</th><th>数量</th><th>成本</th><th>市值</th><th>盈亏</th></tr>
        </thead>
        <tbody>{holdings_rows}</tbody>
    </table>
</div>

<!-- Recent Decisions -->
<div class="card">
    <h2>🧠 近期决策</h2>
    <table>
        <thead>
            <tr><th>标的</th><th>类型</th><th>评分</th><th>状态</th><th>日期</th></tr>
        </thead>
        <tbody>{decision_rows}</tbody>
    </table>
</div>

{f'''<!-- Watchlist -->
<div class="card">
    <h2>👀 关注列表</h2>
    <table>
        <thead>
            <tr><th>代码</th><th>名称</th><th>关注理由</th><th>目标价</th></tr>
        </thead>
        <tbody>{watchlist_rows}</tbody>
    </table>
</div>''' if watchlist_rows else ''}

<div class="footer">
    INVEST Decision System · 个人投资决策辅助 · 不构成投资建议
</div>

</div>
</body>
</html>"""

    return html


def generate_decision_html(decision_id):
    """Generate a single decision review HTML report."""
    db = _get_db()
    decision = db.get_decision(decision_id)
    if not decision:
        return "<html><body><h1>决策记录不存在</h1></body></html>"

    # Build scores dict for radar
    scores = {
        'intent_score': decision.get('intent_score', 0) or 0,
        'numbers_score': decision.get('numbers_score', 0) or 0,
        'value_score': decision.get('value_score', 0) or 0,
        'edge_score': decision.get('edge_score', 0) or 0,
        'safety_score': decision.get('safety_score', 0) or 0,
        'timing_score': decision.get('timing_score', 0) or 0,
    }

    radar_svg = generate_svg_radar(scores)

    # Score bars
    dims = [
        ('intent_score', '意图 Intent', 0.15),
        ('numbers_score', '数字 Numbers', 0.20),
        ('value_score', '价值 Value', 0.20),
        ('edge_score', '优势 Edge', 0.10),
        ('safety_score', '安全 Safety', 0.20),
        ('timing_score', '时机 Timing', 0.15),
    ]
    bars = ""
    for key, name, weight in dims:
        score = scores[key]
        level = 'good' if score >= 7 else 'warning' if score >= 4 else 'danger'
        bars += f"""
        <div class="bar-row">
            <div class="bar-label">{name} ({weight*100:.0f}%)</div>
            <div class="bar-track">
                <div class="bar-fill {level}" style="width: {score*10}%">{score}/10</div>
            </div>
        </div>"""

    # Recommendation banner
    total = decision['total_score'] or 0
    if total >= 7:
        banner_class, banner_text = 'good', f'✅ 强烈推荐 — 综合评分 {total}/10，信心充足'
    elif total >= 5:
        banner_class, banner_text = 'warning', f'⚠️ 谨慎推荐 — 综合评分 {total}/10，需关注薄弱维度'
    elif total >= 3:
        banner_class, banner_text = 'danger', f'⏸️ 建议等待 — 综合评分 {total}/10，多维度不满足'
    else:
        banner_class, banner_text = 'danger', f'❌ 不建议 — 综合评分 {total}/10，应回避'

    css = generate_css()

    # Outcome section
    outcome_html = ""
    if decision.get('outcome'):
        outcome_color = '#ef4444' if decision['outcome'] == 'win' else '#22c55e'
        outcome_icon = '🏆' if decision['outcome'] == 'win' else '📉'
        outcome_text = '盈利' if decision['outcome'] == 'win' else '亏损'
        outcome_html = f"""
        <div class="card">
            <h2>📊 复盘结果</h2>
            <div style="text-align: center; padding: 20px;">
                <div style="font-size: 48px;">{outcome_icon}</div>
                <div style="font-size: 24px; font-weight: 700; color: {outcome_color}; margin: 8px 0;">{outcome_text}</div>
                <div style="font-size: 20px; color: {outcome_color};">{decision.get('outcome_pnl', 0):+,.2f}</div>
                <div style="color: var(--text-secondary); margin-top: 8px;">{decision.get('outcome_notes', '')}</div>
            </div>
        </div>"""

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>INVEST 决策报告 - {decision.get('name', decision['symbol'])}</title>
<style>{css}</style>
</head>
<body>
<div class="container">

<div class="header">
    <h1>🧠 INVEST 投资决策报告</h1>
    <p class="subtitle">{decision.get('name', decision['symbol'])} · {decision['decision_type']} · {decision.get('decision_date', '')}</p>
</div>

<div class="summary-banner {banner_class}">{banner_text}</div>

<div class="grid-2">
    <div class="card">
        <h2>🎯 六维雷达图</h2>
        <div class="radar-container">{radar_svg}</div>
    </div>
    <div class="card">
        <h2>📊 维度评分</h2>
        {bars}
        <div style="margin-top: 16px; padding: 12px; background: #f8fafc; border-radius: 8px;">
            <strong>加权总分: {total}/10</strong>
        </div>
    </div>
</div>

<!-- Thesis & Risks -->
<div class="grid-2">
    <div class="card">
        <h2>💡 投资论点</h2>
        <p style="white-space: pre-wrap;">{decision.get('thesis', '未记录')}</p>
    </div>
    <div class="card">
        <h2>⚠️ 风险因素</h2>
        <p style="white-space: pre-wrap;">{decision.get('risks', '未记录')}</p>
    </div>
</div>

<!-- Position Sizing -->
<div class="card">
    <h2>💰 仓位与风控参数</h2>
    <div class="stats-grid">
        <div class="stat-card">
            <div class="label">建议仓位占比</div>
            <div class="value">{decision.get('position_size_pct', '-')}%</div>
        </div>
        <div class="stat-card danger">
            <div class="label">止损比例</div>
            <div class="value">{decision.get('stop_loss_pct', '-')}%</div>
        </div>
        <div class="stat-card success">
            <div class="label">止盈比例</div>
            <div class="value">{decision.get('take_profit_pct', '-')}%</div>
        </div>
        <div class="stat-card">
            <div class="label">决策状态</div>
            <div class="value" style="font-size: 18px;">{decision.get('status', '-')}</div>
        </div>
    </div>
</div>

{outcome_html}

<div class="footer">
    INVEST Decision System · 个人投资决策辅助 · 不构成投资建议
</div>

</div>
</body>
</html>"""

    return html


def generate_review_html():
    """Generate a comprehensive review report of all past decisions."""
    db = _get_db()
    stats = db.get_decision_stats()
    decisions = db.get_all_decisions(limit=100)
    portfolio = db.get_portfolio_summary()

    css = generate_css()

    # Decision history table
    decision_rows = ""
    for d in decisions:
        score_class = 'good' if d['total_score'] >= 7 else 'warning' if d['total_score'] >= 5 else 'danger'
        outcome_display = '-'
        if d.get('outcome') == 'win':
            outcome_display = f'<span class="badge good">🏆 盈利</span>'
        elif d.get('outcome') == 'loss':
            outcome_display = f'<span class="badge danger">📉 亏损</span>'

        pnl_val = d.get('outcome_pnl')
        if pnl_val is not None:
            pnl_str = f"{pnl_val:+,.2f}"
            pnl_class = 'pnl-positive' if pnl_val >= 0 else 'pnl-negative'
        else:
            pnl_str = '-'
            pnl_class = ''
        decision_rows += f"""
        <tr>
            <td>{d.get('decision_date', '')}</td>
            <td><strong>{d.get('name', d['symbol'])}</strong></td>
            <td>{d['decision_type']}</td>
            <td><span class="badge {score_class}">{d['total_score']}</span></td>
            <td>{outcome_display}</td>
            <td class="{pnl_class}">{pnl_str}</td>
        </tr>"""

    # Score distribution analysis
    reviewed = [d for d in decisions if d.get('outcome') in ('win', 'loss')]
    high_score_wins = len([d for d in reviewed if d['total_score'] >= 7 and d['outcome'] == 'win'])
    high_score_losses = len([d for d in reviewed if d['total_score'] >= 7 and d['outcome'] == 'loss'])
    low_score_wins = len([d for d in reviewed if d['total_score'] < 5 and d['outcome'] == 'win'])
    low_score_losses = len([d for d in reviewed if d['total_score'] < 5 and d['outcome'] == 'loss'])

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>投资决策复盘报告</title>
<style>{css}</style>
</head>
<body>
<div class="container">

<div class="header">
    <h1>📋 投资决策复盘报告</h1>
    <p class="subtitle">回顾每一笔决策，优化你的决策系统</p>
    <p class="date">生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
</div>

<!-- Performance Stats -->
<div class="stats-grid">
    <div class="stat-card {'success' if stats['win_rate'] >= 50 else 'danger'}">
        <div class="label">决策胜率</div>
        <div class="value">{stats['win_rate']}%</div>
        <div class="sub">{stats['wins']}胜 {stats['losses']}负</div>
    </div>
    <div class="stat-card">
        <div class="label">累计已实现盈亏</div>
        <div class="value {'pnl-positive' if stats['total_pnl'] >= 0 else 'pnl-negative'}">{stats['total_pnl']:+,.0f}</div>
    </div>
    <div class="stat-card">
        <div class="label">盈利因子</div>
        <div class="value">{stats['profit_factor']}</div>
        <div class="sub">平均盈利 ¥{stats['avg_pnl_win']:,.0f} / 亏损 ¥{abs(stats['avg_pnl_loss']):,.0f}</div>
    </div>
    <div class="stat-card">
        <div class="label">胜方平均评分</div>
        <div class="value">{stats['avg_score_win']}</div>
        <div class="sub">负方: {stats['avg_score_loss']}</div>
    </div>
</div>

<!-- Score vs Outcome Analysis -->
<div class="card">
    <h2>🔍 评分与结果关联分析</h2>
    <div class="grid-2">
        <div style="padding: 16px; background: #f0fdf4; border-radius: 8px;">
            <h3 style="color: #16a34a; margin-bottom: 8px;">高分决策 (≥7分)</h3>
            <p>🏆 盈利: {high_score_wins} 笔</p>
            <p>📉 亏损: {high_score_losses} 笔</p>
            <p style="margin-top: 8px; font-weight: 600;">高分胜率: {round(high_score_wins/(high_score_wins+high_score_losses)*100, 1) if (high_score_wins+high_score_losses) > 0 else 0}%</p>
        </div>
        <div style="padding: 16px; background: #fef2f2; border-radius: 8px;">
            <h3 style="color: #dc2626; margin-bottom: 8px;">低分决策 (&lt;5分)</h3>
            <p>🏆 盈利: {low_score_wins} 笔</p>
            <p>📉 亏损: {low_score_losses} 笔</p>
            <p style="margin-top: 8px; font-weight: 600;">低分胜率: {round(low_score_wins/(low_score_wins+low_score_losses)*100, 1) if (low_score_wins+low_score_losses) > 0 else 0}%</p>
        </div>
    </div>
</div>

<!-- Decision History -->
<div class="card">
    <h2>📜 决策历史</h2>
    <table>
        <thead>
            <tr><th>日期</th><th>标的</th><th>类型</th><th>评分</th><th>结果</th><th>盈亏</th></tr>
        </thead>
        <tbody>{decision_rows}</tbody>
    </table>
</div>

<div class="footer">
    INVEST Decision System · 个人投资决策辅助 · 不构成投资建议
</div>

</div>
</body>
</html>"""

    return html


def save_report(html_content, filename):
    """Save HTML report to the outputs directory."""
    outputs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "outputs")
    os.makedirs(outputs_dir, exist_ok=True)
    path = os.path.join(outputs_dir, filename)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return path


if __name__ == '__main__':
    # Quick test - generate dashboard
    db = _get_db()
    db.init_db()

    # Add sample data for testing
    try:
        db.add_holding('600519', '贵州茅台', 'stock', 'A-share', 100, 1600, 1650, 'CNY', '白酒')
        db.add_holding('000858', '五粮液', 'stock', 'A-share', 200, 140, 138, 'CNY', '白酒')
        db.add_holding('510300', '沪深300ETF', 'fund', 'A-share', 10000, 3.8, 3.85, 'CNY')
        db.create_decision('600519', '贵州茅台', 'buy',
                          intent_score=8, numbers_score=7, value_score=7,
                          edge_score=6, safety_score=6, timing_score=5,
                          thesis='白酒龙头，估值回调后具备配置价值',
                          risks='消费降级、政策风险',
                          position_size_pct=15, stop_loss_pct=8, take_profit_pct=20)
    except:
        pass

    html = generate_dashboard_html()
    path = save_report(html, 'dashboard_test.html')
    print(f"Test report saved: {path}")
