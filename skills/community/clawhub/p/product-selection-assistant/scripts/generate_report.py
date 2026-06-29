#!/usr/bin/env python3
"""
选品助手 - HTML报告生成器
接收JSON分析数据, 生成交互式可视化HTML选品报告
"""

import json
import sys
from datetime import datetime

TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>选品分析报告 - {product_name}</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
:root {{
  --bg: #f8fafc;
  --card-bg: #ffffff;
  --text: #1e293b;
  --text-secondary: #64748b;
  --border: #e2e8f0;
  --accent: #3b82f6;
  --accent-light: #eff6ff;
  --green: #10b981;
  --green-light: #ecfdf5;
  --yellow: #f59e0b;
  --yellow-light: #fffbeb;
  --red: #ef4444;
  --red-light: #fef2f2;
  --purple: #8b5cf6;
  --radius: 16px;
  --shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
  --shadow-lg: 0 10px 25px rgba(0,0,0,0.08);
}}
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "PingFang SC", "Microsoft YaHei", sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.6;
  padding: 24px;
}}
.container {{ max-width: 960px; margin: 0 auto; }}

/* Header */
.header {{
  background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
  border-radius: var(--radius);
  padding: 40px 36px;
  margin-bottom: 24px;
  color: #fff;
}}
.header .badge {{
  display: inline-block;
  background: rgba(255,255,255,0.15);
  padding: 4px 14px;
  border-radius: 100px;
  font-size: 13px;
  margin-bottom: 16px;
}}
.header h1 {{ font-size: 28px; font-weight: 700; margin-bottom: 8px; }}
.header .meta {{ font-size: 14px; opacity: 0.7; }}

/* Recommendation Card */
.rec-card {{
  background: var(--card-bg);
  border-radius: var(--radius);
  padding: 32px;
  margin-bottom: 24px;
  box-shadow: var(--shadow);
  display: flex;
  align-items: center;
  gap: 28px;
}}
.rec-badge {{
  width: 130px;
  height: 130px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  flex-shrink: 0;
}}
.rec-badge .score {{ font-size: 42px; line-height: 1; }}
.rec-badge .label {{ font-size: 14px; margin-top: 4px; }}
.rec-badge.high {{ background: var(--green-light); color: #059669; border: 3px solid var(--green); }}
.rec-badge.medium {{ background: var(--yellow-light); color: #b45309; border: 3px solid var(--yellow); }}
.rec-badge.low {{ background: var(--red-light); color: #dc2626; border: 3px solid var(--red); }}
.rec-detail h2 {{ font-size: 22px; margin-bottom: 8px; }}
.rec-detail p {{ color: var(--text-secondary); font-size: 15px; }}
.rec-actions {{ margin-top: 12px; display: flex; gap: 10px; flex-wrap: wrap; }}
.rec-tag {{
  display: inline-block;
  padding: 4px 12px;
  border-radius: 100px;
  font-size: 13px;
  font-weight: 500;
}}
.rec-tag.positive {{ background: var(--green-light); color: #059669; }}
.rec-tag.warning {{ background: var(--yellow-light); color: #b45309; }}
.rec-tag.negative {{ background: var(--red-light); color: #dc2626; }}

/* Score Grid */
.section-title {{
  font-size: 18px;
  font-weight: 700;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}}
.scoring-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(440px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}}
.chart-card {{
  background: var(--card-bg);
  border-radius: var(--radius);
  padding: 24px;
  box-shadow: var(--shadow);
}}
.chart-card canvas {{ max-height: 320px; }}
.score-list {{
  background: var(--card-bg);
  border-radius: var(--radius);
  padding: 24px;
  box-shadow: var(--shadow);
}}
.score-item {{
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 0;
  border-bottom: 1px solid var(--border);
}}
.score-item:last-child {{ border-bottom: none; }}
.score-item .dim-name {{ font-weight: 600; font-size: 14px; }}
.score-item .dim-desc {{ font-size: 12px; color: var(--text-secondary); margin-top: 2px; }}
.score-bar-wrap {{
  display: flex;
  align-items: center;
  gap: 12px;
  min-width: 180px;
}}
.score-bar-bg {{
  flex: 1;
  height: 8px;
  background: #f1f5f9;
  border-radius: 4px;
  overflow: hidden;
}}
.score-bar-fill {{
  height: 100%;
  border-radius: 4px;
  transition: width 0.6s ease;
}}
.score-value {{ font-size: 15px; font-weight: 700; min-width: 36px; text-align: right; }}

/* Analysis Cards */
.analysis-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}}
.analysis-card {{
  background: var(--card-bg);
  border-radius: var(--radius);
  padding: 24px;
  box-shadow: var(--shadow);
  border-left: 4px solid var(--accent);
}}
.analysis-card h3 {{ font-size: 15px; margin-bottom: 10px; display: flex; align-items: center; gap: 6px; }}
.analysis-card p, .analysis-card li {{ font-size: 13px; color: var(--text-secondary); line-height: 1.8; }}
.analysis-card ul {{ padding-left: 16px; }}
.analysis-card.demand {{ border-left-color: #3b82f6; }}
.analysis-card.competition {{ border-left-color: #f59e0b; }}
.analysis-card.profit {{ border-left-color: #10b981; }}
.analysis-card.seasonality {{ border-left-color: #8b5cf6; }}
.analysis-card.risk {{ border-left-color: #ef4444; }}
.analysis-card.opportunity {{ border-left-color: #06b6d4; }}

/* Action Items */
.action-list {{
  background: var(--card-bg);
  border-radius: var(--radius);
  padding: 24px;
  box-shadow: var(--shadow);
  margin-bottom: 24px;
}}
.action-item {{
  display: flex;
  gap: 14px;
  padding: 16px 0;
  border-bottom: 1px solid var(--border);
}}
.action-item:last-child {{ border-bottom: none; }}
.action-priority {{
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
}}
.action-priority.p0 {{ background: #fef2f2; color: #dc2626; }}
.action-priority.p1 {{ background: #fffbeb; color: #b45309; }}
.action-priority.p2 {{ background: #f0f9ff; color: #0284c7; }}
.action-content h4 {{ font-size: 14px; margin-bottom: 4px; }}
.action-content p {{ font-size: 13px; color: var(--text-secondary); }}

/* Footer */
.footer {{
  text-align: center;
  padding: 32px;
  color: var(--text-secondary);
  font-size: 13px;
}}

@media (max-width: 600px) {{
  .rec-card {{ flex-direction: column; text-align: center; }}
  .scoring-grid {{ grid-template-columns: 1fr; }}
  .analysis-grid {{ grid-template-columns: 1fr; }}
}}
</style>
</head>
<body>
<div class="container">

<!-- Header -->
<div class="header">
  <div class="badge">📊 选品助手 · 智能分析报告</div>
  <h1>{product_name}</h1>
  <div class="meta">分析时间: {analysis_time} | 品类: {category}</div>
</div>

<!-- Recommendation Card -->
<div class="rec-card">
  <div class="rec-badge {rec_class}">
    <div class="score">{overall_score}</div>
    <div class="label">综合评分</div>
  </div>
  <div class="rec-detail">
    <h2>{recommendation}</h2>
    <p>{recommendation_reason}</p>
    <div class="rec-actions">
      {rec_tags}
    </div>
  </div>
</div>

<!-- Scoring Section -->
<div class="section-title">📈 六维评分</div>
<div class="scoring-grid">
  <div class="chart-card">
    <canvas id="radarChart"></canvas>
  </div>
  <div class="score-list">
    {score_items}
  </div>
</div>

<!-- Analysis Section -->
<div class="section-title">🔍 深度分析</div>
<div class="analysis-grid">
  {analysis_cards}
</div>

<!-- Action Items -->
<div class="section-title">📋 行动建议</div>
<div class="action-list">
  {action_items}
</div>

<!-- Footer -->
<div class="footer">
  选品助手 · AI驱动的电商选品决策工具 · {analysis_time}
</div>

</div>

<script>
const ctx = document.getElementById('radarChart').getContext('2d');
new Chart(ctx, {{
  type: 'radar',
  data: {{
    labels: {dim_labels},
    datasets: [{{
      label: '评分',
      data: {dim_scores},
      backgroundColor: 'rgba(59, 130, 246, 0.15)',
      borderColor: 'rgba(59, 130, 246, 0.9)',
      borderWidth: 2.5,
      pointBackgroundColor: 'rgba(59, 130, 246, 1)',
      pointBorderColor: '#fff',
      pointBorderWidth: 2,
      pointRadius: 5,
      pointHoverRadius: 7,
    }}]
  }},
  options: {{
    responsive: true,
    maintainAspectRatio: true,
    scales: {{
      r: {{
        beginAtZero: true,
        max: 100,
        min: 0,
        ticks: {{ stepSize: 20, backdropColor: 'transparent', font: {{ size: 10 }} }},
        pointLabels: {{ font: {{ size: 12, weight: '600' }}, color: '#334155' }},
        grid: {{ color: '#e2e8f0' }},
        angleLines: {{ color: '#e2e8f0' }},
      }}
    }},
    plugins: {{
      legend: {{ display: false }},
    }}
  }}
}});
</script>
</body>
</html>'''


def get_score_class(score):
    if score >= 75:
        return 'high'
    elif score >= 55:
        return 'medium'
    else:
        return 'low'


def get_recommendation(score):
    if score >= 80:
        return '🔥 强烈推荐上架', '市场需求旺盛、竞争格局良好、利润空间可观，建议优先安排上架计划。'
    elif score >= 65:
        return '✅ 建议上架', '整体表现良好，部分维度需关注风险点，建议制定差异化策略后上架。'
    elif score >= 50:
        return '⚠️ 谨慎上架', '存在一定风险，需解决关键问题后方可考虑上架，建议小批量试销验证。'
    else:
        return '❌ 不建议上架', '当前市场环境不利于该产品，建议寻找替代品或等待市场变化。'


def build_score_bar(score):
    if score >= 75:
        color = '#10b981'
    elif score >= 55:
        color = '#f59e0b'
    else:
        color = '#ef4444'
    return f'<div class="score-bar-bg"><div class="score-bar-fill" style="width:{score}%;background:{color}"></div></div>'


def build_score_items(dimensions):
    items = []
    for dim in dimensions:
        bar = build_score_bar(dim['score'])
        items.append(f'''<div class="score-item">
          <div>
            <div class="dim-name">{dim['name']}</div>
            <div class="dim-desc">{dim['desc']}</div>
          </div>
          <div class="score-bar-wrap">{bar}<span class="score-value">{dim['score']}</span></div>
        </div>''')
    return '\n'.join(items)


def build_analysis_cards(analyses):
    type_map = {
        'demand': ('demand', '📊'),
        'competition': ('competition', '🏪'),
        'profit': ('profit', '💰'),
        'seasonality': ('seasonality', '📅'),
        'risk': ('risk', '⚠️'),
        'opportunity': ('opportunity', '💡'),
    }
    cards = []
    for a in analyses:
        css_class, icon = type_map.get(a.get('type', ''), ('', '📌'))
        content = a.get('content', '')
        if isinstance(content, list):
            content = '<ul>' + ''.join(f'<li>{item}</li>' for item in content) + '</ul>'
        else:
            content = f'<p>{content}</p>'
        cards.append(f'''<div class="analysis-card {css_class}">
          <h3>{icon} {a['title']}</h3>
          {content}
        </div>''')
    return '\n'.join(cards)


def build_rec_tags(data):
    tags = []
    score = data.get('overall_score', 0)
    dims = data.get('dimensions', [])

    # Positive tags
    high_dims = [d['name'] for d in dims if d['score'] >= 75]
    if high_dims:
        tags.append(f'<span class="rec-tag positive">✅ {"、".join(high_dims[:3])}表现优秀</span>')

    # Warning tags
    mid_dims = [d['name'] for d in dims if 50 <= d['score'] < 75]
    if mid_dims:
        tags.append(f'<span class="rec-tag warning">⚡ 关注{"、".join(mid_dims[:2])}</span>')

    # Negative tags
    low_dims = [d['name'] for d in dims if d['score'] < 50]
    if low_dims:
        tags.append(f'<span class="rec-tag negative">🚫 {"、".join(low_dims[:2])}需改善</span>')

    return '\n'.join(tags)


def build_action_items(actions):
    items = []
    for a in actions:
        priority = a.get('priority', 'P2').lower()
        items.append(f'''<div class="action-item">
          <div class="action-priority {priority}">{a.get('priority', 'P2')}</div>
          <div class="action-content">
            <h4>{a['title']}</h4>
            <p>{a['desc']}</p>
          </div>
        </div>''')
    return '\n'.join(items)


def validate_data(data):
    """Validate input data structure"""
    required = ['product_name', 'category', 'overall_score', 'dimensions']
    for key in required:
        if key not in data:
            raise ValueError(f"Missing required field: {key}")

    if not (0 <= data['overall_score'] <= 100):
        raise ValueError("overall_score must be between 0 and 100")

    dim_names = ['市场需求', '竞争强度', '利润空间', '季节性风险', '入场难度', '增长趋势']
    for dim in data['dimensions']:
        if 'name' not in dim or 'score' not in dim or 'desc' not in dim:
            raise ValueError(f"Each dimension must have name, score, desc: {dim}")


def generate_report(data):
    """Generate complete HTML report from analysis data"""
    validate_data(data)

    product_name = data['product_name']
    category = data.get('category', '综合')
    overall_score = data['overall_score']
    dimensions = data['dimensions']
    analyses = data.get('analyses', [])
    actions = data.get('actions', [])
    analysis_time = datetime.now().strftime('%Y-%m-%d %H:%M')

    rec_text, rec_reason = get_recommendation(overall_score)
    rec_class = get_score_class(overall_score)

    dim_labels = json.dumps([d['name'] for d in dimensions], ensure_ascii=False)
    dim_scores = json.dumps([d['score'] for d in dimensions])

    return TEMPLATE.format(
        product_name=product_name,
        category=category,
        analysis_time=analysis_time,
        overall_score=overall_score,
        rec_class=rec_class,
        recommendation=rec_text,
        recommendation_reason=rec_reason,
        rec_tags=build_rec_tags(data),
        score_items=build_score_items(dimensions),
        dim_labels=dim_labels,
        dim_scores=dim_scores,
        analysis_cards=build_analysis_cards(analyses),
        action_items=build_action_items(actions),
    )


def main():
    input_file = None
    output_file = None

    if len(sys.argv) == 1:
        # stdin -> stdout
        pass
    elif len(sys.argv) == 2:
        # stdin -> file (arg is output file)
        output_file = sys.argv[1]
    else:
        # file -> file (arg1 is input JSON, arg2 is output)
        input_file = sys.argv[1]
        output_file = sys.argv[2]

    if input_file:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = json.load(sys.stdin)

    html = generate_report(data)

    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f"Report saved to: {output_file}")
    else:
        print(html)


if __name__ == '__main__':
    main()
