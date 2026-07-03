#!/usr/bin/env python3
"""JD智能解读报告生成器 — 读取 analysis.json → 渲染交互式 HTML 报告"""

import json
import sys
import os
from datetime import datetime
from pathlib import Path


def load_analysis(json_path: str) -> dict:
    """加载分析结果 JSON"""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)


def render_stars(count: int, max_stars: int = 5) -> str:
    """渲染星级评分"""
    filled = "★" * count
    empty = "☆" * (max_stars - count)
    return f'<span class="stars">{filled}</span><span class="stars-empty">{empty}</span>'


def render_signal_badge(strength: str) -> str:
    """渲染信号强度标签"""
    colors = {"高": "#e74c3c", "中": "#f39c12", "低": "#27ae60"}
    color = colors.get(strength, "#95a5a6")
    return f'<span class="signal-badge" style="background:{color}">{strength}</span>'


def render_module_one(data: dict) -> str:
    """模块一：岗位画像卡片"""
    info = data.get("module_1_basic_info", {})
    responsibilities = data.get("module_1_responsibilities", [])
    hard_skills_required = data.get("module_1_hard_skills_required", [])
    hard_skills_plus = data.get("module_1_hard_skills_plus", [])
    soft_skills = data.get("module_1_soft_skills", [])
    education = data.get("module_1_education", "")

    resp_items = "".join(
        f'<li><span class="resp-num">{i+1}</span>{r}</li>'
        for i, r in enumerate(responsibilities)
    )

    hard_req_tags = "".join(
        f'<span class="tag tag-required">{s}</span>' for s in hard_skills_required
    )
    hard_plus_tags = "".join(
        f'<span class="tag tag-plus">{s}</span>' for s in hard_skills_plus
    )
    soft_tags = "".join(
        f'<span class="tag tag-soft">{s}</span>' for s in soft_skills
    )

    return f"""
    <div class="module-card" id="module-1">
      <h3><span class="module-icon">📋</span> 岗位画像</h3>
      <div class="info-grid">
        <div class="info-item"><label>职位</label><span>{info.get('title', '-')}</span></div>
        <div class="info-item"><label>公司/行业</label><span>{info.get('company', '-')}</span></div>
        <div class="info-item"><label>地点</label><span>{info.get('location', '-')}</span></div>
        <div class="info-item"><label>薪资</label><span>{info.get('salary', '-')}</span></div>
        <div class="info-item"><label>性质</label><span>{info.get('type', '-')}</span></div>
        <div class="info-item"><label>学历/经验</label><span>{education}</span></div>
      </div>
      <div class="resp-section">
        <h4>核心职责</h4>
        <ol class="resp-list">{resp_items}</ol>
      </div>
      <div class="skills-section">
        <div class="skill-group">
          <h4>🔧 硬技能 — 必需</h4>
          <div class="tag-cloud">{hard_req_tags or '<span class="no-data">未提取到</span>'}</div>
        </div>
        <div class="skill-group">
          <h4>➕ 硬技能 — 加分</h4>
          <div class="tag-cloud">{hard_plus_tags or '<span class="no-data">未提取到</span>'}</div>
        </div>
        <div class="skill-group">
          <h4>💬 软技能</h4>
          <div class="tag-cloud">{soft_tags or '<span class="no-data">未提取到</span>'}</div>
        </div>
      </div>
    </div>"""


def render_module_two(data: dict) -> str:
    """模块二：显性 vs 隐性需求"""
    mappings = data.get("module_2_explicit_implicit", [])
    if not mappings:
        return ""

    rows = ""
    for m in mappings:
        explicit = m.get("explicit", "")
        implicit = m.get("implicit", "")
        strength = m.get("strength", "低")
        rows += f"""
        <tr>
          <td class="explicit-cell">{explicit}</td>
          <td class="arrow-cell">→</td>
          <td class="implicit-cell">{implicit}</td>
          <td>{render_signal_badge(strength)}</td>
        </tr>"""

    return f"""
    <div class="module-card" id="module-2">
      <h3><span class="module-icon">🔍</span> 显性 vs 隐性需求解构</h3>
      <p class="module-desc">左边是 JD 的字面意思，右边是可能隐藏的真实信号。信号强度标注仅供参考。</p>
      <div class="table-wrap">
        <table class="mapping-table">
          <thead>
            <tr><th>显性措辞</th><th></th><th>隐性信号</th><th>信号强度</th></tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>"""


def render_module_three(data: dict) -> str:
    """模块三：需求权重评分"""
    items = data.get("module_3_weighted_requirements", [])
    if not items:
        return ""

    rows = ""
    for item in items:
        name = item.get("name", "")
        category = item.get("category", "")
        stars = min(max(int(item.get("weight", 3)), 1), 5)
        necessity = item.get("necessity", "建议")
        note = item.get("note", "")

        necessity_colors = {"必须": "#e74c3c", "重要": "#f39c12", "建议": "#3498db", "加分": "#27ae60"}
        nc = necessity_colors.get(necessity, "#95a5a6")

        rows += f"""
        <tr>
          <td><strong>{name}</strong></td>
          <td><span class="cat-tag">{category}</span></td>
          <td>{render_stars(stars)}</td>
          <td><span class="necessity-badge" style="background:{nc}">{necessity}</span></td>
          <td class="note-cell">{note}</td>
        </tr>"""

    return f"""
    <div class="module-card" id="module-3">
      <h3><span class="module-icon">⭐</span> 需求权重评分</h3>
      <p class="module-desc">权重基于措辞强度、出现位置和行业常识综合评定。星级越高越重要。</p>
      <div class="table-wrap">
        <table class="weight-table">
          <thead>
            <tr><th>要求</th><th>类别</th><th>权重</th><th>必要程度</th><th>备注</th></tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
    </div>"""


def render_module_four(data: dict) -> str:
    """模块四：能力差距自评引导"""
    items = data.get("module_4_gap_assessment", [])
    if not items:
        return """
    <div class="module-card" id="module-4">
      <h3><span class="module-icon">🎯</span> 能力差距自评</h3>
      <div class="gap-placeholder">
        <p>💡 对照上方需求权重表，对每项核心要求给自己打分（1-5分）。</p>
        <div class="gap-scale">
          <span class="gap-level gap-red">1-2分：严重不足 — 需重点学习</span>
          <span class="gap-level gap-yellow">3分：部分满足 — 需强化提升</span>
          <span class="gap-level gap-green">4-5分：完全满足 — 保持即可</span>
        </div>
        <p class="hint">需要精确简历匹配评分？试试说 <strong>"用 resume-jd-scorer 帮我精确评分"</strong></p>
      </div>
    </div>"""

    rows = ""
    for item in items:
        name = item.get("name", "")
        score = min(max(int(item.get("self_score", 3)), 1), 5)
        priority = item.get("priority", "P2")

        if score <= 2:
            gap_class = "gap-red"
            gap_text = "严重不足"
        elif score == 3:
            gap_class = "gap-yellow"
            gap_text = "部分满足"
        else:
            gap_class = "gap-green"
            gap_text = "完全满足"

        priority_colors = {"P0": "#e74c3c", "P1": "#f39c12", "P2": "#3498db"}
        pc = priority_colors.get(priority, "#95a5a6")

        rows += f"""
        <tr>
          <td>{name}</td>
          <td><span class="gap-indicator {gap_class}">{'■' * score}{'□' * (5 - score)}</span> {gap_text}</td>
          <td><span class="priority-badge" style="background:{pc}">{priority}</span></td>
        </tr>"""

    return f"""
    <div class="module-card" id="module-4">
      <h3><span class="module-icon">🎯</span> 能力差距自评</h3>
      <p class="module-desc">对照岗位核心要求进行自我评估，红/黄/绿三色标注差距程度。</p>
      <div class="table-wrap">
        <table class="gap-table">
          <thead>
            <tr><th>能力要求</th><th>自评得分</th><th>优先级</th></tr>
          </thead>
          <tbody>{rows}</tbody>
        </table>
      </div>
      <p class="hint">需要精确简历匹配评分？试试说 <strong>"用 resume-jd-scorer 帮我精确评分"</strong></p>
    </div>"""


def render_module_five(data: dict) -> str:
    """模块五：面试考点预测"""
    questions = data.get("module_5_interview_questions", [])
    if not questions:
        return ""

    # Group by category
    categories = {}
    for q in questions:
        cat = q.get("category", "其他")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(q)

    cards = ""
    for cat, qs in categories.items():
        q_items = ""
        for q in qs:
            probability = q.get("probability", 2)
            prob_stars = "★★★" if probability >= 3 else ("★★" if probability == 2 else "★")
            q_items += f"""
            <div class="question-item">
              <span class="prob-stars">{prob_stars}</span>
              <span class="question-text">{q.get('question', '')}</span>
            </div>"""
        cards += f"""
        <div class="question-category">
          <h4>{cat}</h4>
          {q_items}
        </div>"""

    return f"""
    <div class="module-card" id="module-5">
      <h3><span class="module-icon">🎤</span> 面试考点预测</h3>
      <p class="module-desc">基于 JD 内容反向推测可能的面试问题。概率标注：★★★高 ★★中 ★低</p>
      <div class="question-grid">{cards}</div>
      <div class="reverse-questions">
        <h4>🤔 建议反问面试官</h4>
        <ul>
          {''.join(f'<li>{r}</li>' for r in data.get('module_5_reverse_questions', []))}
        </ul>
      </div>
    </div>"""


def render_module_six(data: dict) -> str:
    """模块六：学习提升路线图"""
    phases = data.get("module_6_learning_roadmap", [])
    if not phases:
        return ""

    phase_cards = ""
    for i, p in enumerate(phases):
        phase_num = p.get("phase", i + 1)
        title = p.get("title", "")
        duration = p.get("duration", "")
        items_html = "".join(f"<li>{item}</li>" for item in p.get("items", []))
        projects = p.get("projects", "")

        phase_cards += f"""
        <div class="phase-card">
          <div class="phase-header">
            <span class="phase-num">第 {phase_num} 阶段</span>
            <span class="phase-duration">⏱ {duration}</span>
          </div>
          <h4>{title}</h4>
          <ul class="phase-items">{items_html}</ul>
          {f'<div class="phase-projects"><strong>🛠 实战项目：</strong>{projects}</div>' if projects else ''}
        </div>"""

    return f"""
    <div class="module-card" id="module-6">
      <h3><span class="module-icon">🗺</span> 学习提升路线图</h3>
      <p class="module-desc">按优先级排序的分阶段学习计划，聚焦 ROI 最高的技能。</p>
      <div class="phase-timeline">{phase_cards}</div>
    </div>"""


def render_module_seven(data: dict) -> str:
    """模块七：ATS 关键词注入"""
    keywords = data.get("module_7_ats_keywords", {})
    if not keywords:
        return ""

    sections = ""
    for cat, items in keywords.items():
        if not items:
            continue
        tags = "".join(f'<span class="keyword-tag">{k}</span>' for k in items)
        sections += f"""
        <div class="ats-category">
          <h4>{cat}</h4>
          <div class="keyword-cloud">{tags}</div>
        </div>"""

    tips = "".join(
        f"<li>{t}</li>" for t in data.get("module_7_integration_tips", [])
    )

    return f"""
    <div class="module-card" id="module-7">
      <h3><span class="module-icon">🤖</span> ATS 关键词注入</h3>
      <p class="module-desc">从 JD 中提取的高频关键词，建议在简历中自然融入以提高 ATS 通过率。</p>
      {sections}
      {f'<div class="ats-tips"><h4>💡 融入建议</h4><ul>{tips}</ul></div>' if tips else ''}
    </div>"""


def render_module_eight(data: dict) -> str:
    """模块八：薪资与市场对标"""
    benchmark = data.get("module_8_salary_benchmark")
    if not benchmark:
        return ""

    cities = ""
    for city_info in benchmark.get("by_city", []):
        cities += f"""
        <div class="salary-city">
          <span class="city-name">{city_info.get('city', '')}</span>
          <span class="city-range">{city_info.get('range', '')}</span>
        </div>"""

    return f"""
    <div class="module-card" id="module-8">
      <h3><span class="module-icon">💰</span> 薪资与市场对标</h3>
      <div class="salary-overview">
        <div class="salary-item">
          <label>JD 标注薪资</label>
          <span class="salary-value">{benchmark.get('jd_salary', '-')}</span>
        </div>
        <div class="salary-item">
          <label>市场参考区间</label>
          <span class="salary-value highlight">{benchmark.get('market_range', '-')}</span>
        </div>
        <div class="salary-item">
          <label>建议谈判区间</label>
          <span class="salary-value highlight-green">{benchmark.get('negotiation_range', '-')}</span>
        </div>
      </div>
      {f'<div class="salary-cities"><h4>各城市对标</h4><div class="city-grid">{cities}</div></div>' if cities else ''}
      {f'<div class="salary-tips"><h4>💡 谈判建议</h4><p>{benchmark.get("strategy", "")}</p></div>' if benchmark.get("strategy") else ''}
      <p class="disclaimer">⚠️ 薪资数据来自公开信息，仅供参考。实际薪资受个人能力、谈判、市场波动等多因素影响。</p>
    </div>"""


def render_radar_chart(data: dict) -> str:
    """渲染需求维度雷达图（SVG）"""
    items = data.get("module_3_weighted_requirements", [])
    if not items:
        return ""

    # Group by category and compute average weight
    cat_weights = {}
    for item in items:
        cat = item.get("category", "其他")
        w = item.get("weight", 3)
        if cat not in cat_weights:
            cat_weights[cat] = []
        cat_weights[cat].append(w)

    dimensions = []
    for cat, weights in cat_weights.items():
        avg = sum(weights) / len(weights)
        dimensions.append({"name": cat, "value": avg})

    if len(dimensions) < 3:
        return ""

    # Generate SVG radar chart
    n = len(dimensions)
    cx, cy = 200, 200
    radius = 140
    levels = 5

    svg_parts = [f'<svg viewBox="0 0 400 400" class="radar-chart">']

    # Background grid
    for level in range(1, levels + 1):
        r = radius * level / levels
        points = []
        for i in range(n):
            angle = -90 + i * 360 / n
            import math
            x = cx + r * math.cos(math.radians(angle))
            y = cy + r * math.sin(math.radians(angle))
            points.append(f"{x:.1f},{y:.1f}")
        svg_parts.append(
            f'<polygon points="{" ".join(points)}" fill="none" stroke="#e0e0e0" stroke-width="1"/>'
        )

    # Axis lines
    for i in range(n):
        angle = -90 + i * 360 / n
        import math
        x = cx + radius * math.cos(math.radians(angle))
        y = cy + radius * math.sin(math.radians(angle))
        svg_parts.append(
            f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="#e0e0e0" stroke-width="1"/>'
        )

    # Data polygon
    data_points = []
    for i, d in enumerate(dimensions):
        angle = -90 + i * 360 / n
        import math
        v = d["value"] / 5  # normalize to 0-1
        r = radius * v
        x = cx + r * math.cos(math.radians(angle))
        y = cy + r * math.sin(math.radians(angle))
        data_points.append(f"{x:.1f},{y:.1f}")

    svg_parts.append(
        f'<polygon points="{" ".join(data_points)}" fill="rgba(52,152,219,0.3)" stroke="#3498db" stroke-width="2"/>'
    )

    # Data dots
    for i, d in enumerate(dimensions):
        angle = -90 + i * 360 / n
        import math
        v = d["value"] / 5
        r = radius * v
        x = cx + r * math.cos(math.radians(angle))
        y = cy + r * math.sin(math.radians(angle))
        svg_parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#3498db"/>'
        )

    # Labels
    for i, d in enumerate(dimensions):
        angle = -90 + i * 360 / n
        import math
        label_r = radius + 30
        x = cx + label_r * math.cos(math.radians(angle))
        y = cy + label_r * math.sin(math.radians(angle))
        anchor = "middle"
        if x < cx - 50:
            anchor = "end"
        elif x > cx + 50:
            anchor = "start"
        svg_parts.append(
            f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" dominant-baseline="middle" font-size="12" fill="#2c3e50">{d["name"]}</text>'
        )

    svg_parts.append("</svg>")
    return "\n".join(svg_parts)


def generate_html(data: dict, output_path: str):
    """生成完整 HTML 报告"""

    radar_svg = render_radar_chart(data)

    has_module_8 = bool(data.get("module_8_salary_benchmark"))

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JD 智能解读报告 — {data.get('module_1_basic_info', {}).get('title', '岗位分析')}</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #f5f7fa; color: #2c3e50; line-height:1.6; }}
.container {{ max-width:960px; margin:0 auto; padding:20px; }}

/* Header */
.header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color:#fff; padding:40px 30px; border-radius:16px; margin-bottom:24px; position:relative; overflow:hidden; }}
.header::after {{ content:''; position:absolute; top:-50%; right:-10%; width:300px; height:300px; background:rgba(255,255,255,0.05); border-radius:50%; }}
.header h1 {{ font-size:28px; margin-bottom:8px; position:relative; z-index:1; }}
.header .subtitle {{ font-size:14px; opacity:0.85; position:relative; z-index:1; }}
.header .meta {{ display:flex; gap:16px; margin-top:12px; flex-wrap:wrap; position:relative; z-index:1; }}
.header .meta span {{ background:rgba(255,255,255,0.2); padding:4px 12px; border-radius:20px; font-size:13px; }}

/* Tabs */
.tabs {{ display:flex; gap:8px; flex-wrap:wrap; margin-bottom:20px; position:sticky; top:10px; z-index:100; background:#f5f7fa; padding:10px 0; }}
.tab-btn {{ padding:8px 16px; border:none; background:#fff; border-radius:8px; cursor:pointer; font-size:13px; color:#7f8c8d; transition:all 0.2s; box-shadow:0 1px 3px rgba(0,0,0,0.06); white-space:nowrap; }}
.tab-btn:hover, .tab-btn.active {{ background:#667eea; color:#fff; box-shadow:0 2px 8px rgba(102,126,234,0.3); }}

/* Module Cards */
.module-card {{ background:#fff; border-radius:12px; padding:24px; margin-bottom:16px; box-shadow:0 2px 8px rgba(0,0,0,0.04); }}
.module-card h3 {{ font-size:18px; margin-bottom:4px; color:#2c3e50; }}
.module-icon {{ margin-right:6px; }}
.module-desc {{ font-size:13px; color:#95a5a6; margin-bottom:16px; }}

/* Info Grid */
.info-grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(180px, 1fr)); gap:12px; margin-bottom:20px; }}
.info-item {{ background:#f8f9fa; padding:12px 16px; border-radius:8px; }}
.info-item label {{ display:block; font-size:12px; color:#95a5a6; margin-bottom:4px; }}
.info-item span {{ font-size:15px; font-weight:600; color:#2c3e50; }}

/* Responsibilities */
.resp-section {{ margin-bottom:16px; }}
.resp-section h4 {{ font-size:14px; color:#7f8c8d; margin-bottom:8px; }}
.resp-list {{ padding-left:0; list-style:none; }}
.resp-list li {{ padding:8px 0; border-bottom:1px solid #f0f0f0; display:flex; align-items:flex-start; gap:10px; font-size:14px; }}
.resp-num {{ display:inline-flex; align-items:center; justify-content:center; width:22px; height:22px; background:#667eea; color:#fff; border-radius:50%; font-size:11px; flex-shrink:0; }}

/* Tags */
.tag-cloud {{ display:flex; flex-wrap:wrap; gap:6px; }}
.tag {{ padding:4px 12px; border-radius:6px; font-size:12px; font-weight:500; }}
.tag-required {{ background:#fdecea; color:#e74c3c; }}
.tag-plus {{ background:#e8f5e9; color:#27ae60; }}
.tag-soft {{ background:#e3f2fd; color:#2196f3; }}
.skill-group {{ margin-bottom:16px; }}
.skill-group h4 {{ font-size:13px; color:#7f8c8d; margin-bottom:8px; }}

/* Tables */
.table-wrap {{ overflow-x:auto; }}
table {{ width:100%; border-collapse:collapse; font-size:14px; }}
th {{ background:#f8f9fa; padding:10px 12px; text-align:left; font-weight:600; color:#7f8c8d; font-size:13px; border-bottom:2px solid #e0e0e0; }}
td {{ padding:10px 12px; border-bottom:1px solid #f0f0f0; }}

/* Stars */
.stars {{ color:#f39c12; letter-spacing:1px; }}
.stars-empty {{ color:#e0e0e0; letter-spacing:1px; }}

/* Badges */
.signal-badge {{ display:inline-block; padding:2px 8px; border-radius:4px; color:#fff; font-size:11px; font-weight:600; }}
.necessity-badge {{ display:inline-block; padding:2px 8px; border-radius:4px; color:#fff; font-size:11px; font-weight:600; }}
.priority-badge {{ display:inline-block; padding:2px 8px; border-radius:4px; color:#fff; font-size:11px; font-weight:600; }}
.cat-tag {{ display:inline-block; padding:2px 8px; border-radius:4px; background:#f0f0f0; font-size:11px; color:#7f8c8d; }}

/* Explicit vs Implicit */
.explicit-cell {{ font-weight:500; color:#2c3e50; max-width:200px; }}
.arrow-cell {{ color:#95a5a6; font-size:18px; text-align:center; width:40px; }}
.implicit-cell {{ color:#e67e22; max-width:250px; }}

/* Gap */
.gap-indicator {{ font-size:16px; letter-spacing:2px; }}
.gap-red {{ color:#e74c3c; }}
.gap-yellow {{ color:#f39c12; }}
.gap-green {{ color:#27ae60; }}
.gap-placeholder {{ background:#f8f9fa; border-radius:8px; padding:20px; text-align:center; }}
.gap-scale {{ display:flex; gap:12px; justify-content:center; margin:16px 0; flex-wrap:wrap; }}
.gap-level {{ padding:8px 16px; border-radius:6px; font-size:13px; font-weight:500; }}
.gap-level.gap-red {{ background:#fdecea; color:#c0392b; }}
.gap-level.gap-yellow {{ background:#fef9e7; color:#d68910; }}
.gap-level.gap-green {{ background:#e8f5e9; color:#1e8449; }}
.hint {{ font-size:12px; color:#95a5a6; margin-top:12px; text-align:center; }}

/* Interview Questions */
.question-grid {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(280px, 1fr)); gap:16px; }}
.question-category {{ background:#f8f9fa; border-radius:8px; padding:16px; }}
.question-category h4 {{ font-size:14px; color:#667eea; margin-bottom:10px; }}
.question-item {{ display:flex; gap:8px; padding:6px 0; font-size:13px; align-items:flex-start; }}
.prob-stars {{ color:#f39c12; flex-shrink:0; }}
.question-text {{ color:#2c3e50; }}
.reverse-questions {{ margin-top:16px; background:#f8f9fa; border-radius:8px; padding:16px; }}
.reverse-questions h4 {{ font-size:14px; color:#667eea; margin-bottom:8px; }}
.reverse-questions ul {{ padding-left:20px; }}
.reverse-questions li {{ font-size:13px; padding:3px 0; }}

/* Learning Roadmap */
.phase-timeline {{ display:flex; flex-direction:column; gap:16px; }}
.phase-card {{ border-left:3px solid #667eea; padding:0 0 0 20px; position:relative; }}
.phase-card::before {{ content:''; position:absolute; left:-7px; top:8px; width:11px; height:11px; background:#667eea; border-radius:50%; }}
.phase-header {{ display:flex; gap:10px; align-items:center; margin-bottom:6px; }}
.phase-num {{ background:#667eea; color:#fff; padding:2px 10px; border-radius:4px; font-size:12px; font-weight:600; }}
.phase-duration {{ font-size:12px; color:#95a5a6; }}
.phase-card h4 {{ font-size:15px; color:#2c3e50; margin-bottom:8px; }}
.phase-items {{ padding-left:18px; }}
.phase-items li {{ font-size:13px; padding:2px 0; color:#555; }}
.phase-projects {{ margin-top:8px; background:#fef9e7; padding:8px 12px; border-radius:6px; font-size:13px; }}

/* ATS Keywords */
.ats-category {{ margin-bottom:12px; }}
.ats-category h4 {{ font-size:13px; color:#7f8c8d; margin-bottom:6px; }}
.keyword-cloud {{ display:flex; flex-wrap:wrap; gap:6px; }}
.keyword-tag {{ padding:4px 12px; background:#e8eaf6; color:#5c6bc0; border-radius:6px; font-size:12px; font-weight:500; }}
.ats-tips {{ margin-top:16px; background:#f8f9fa; border-radius:8px; padding:16px; }}
.ats-tips h4 {{ font-size:14px; color:#667eea; margin-bottom:8px; }}
.ats-tips ul {{ padding-left:20px; }}
.ats-tips li {{ font-size:13px; padding:3px 0; color:#555; }}

/* Salary */
.salary-overview {{ display:grid; grid-template-columns:repeat(auto-fill, minmax(200px, 1fr)); gap:12px; margin-bottom:16px; }}
.salary-item {{ background:#f8f9fa; padding:14px 16px; border-radius:8px; }}
.salary-item label {{ display:block; font-size:12px; color:#95a5a6; margin-bottom:4px; }}
.salary-value {{ font-size:18px; font-weight:700; color:#2c3e50; }}
.salary-value.highlight {{ color:#667eea; }}
.salary-value.highlight-green {{ color:#27ae60; }}
.salary-cities {{ margin-bottom:16px; }}
.salary-cities h4 {{ font-size:13px; color:#7f8c8d; margin-bottom:8px; }}
.city-grid {{ display:flex; flex-wrap:wrap; gap:10px; }}
.salary-city {{ background:#f8f9fa; padding:8px 14px; border-radius:8px; display:flex; gap:8px; align-items:center; }}
.city-name {{ font-size:13px; color:#7f8c8d; }}
.city-range {{ font-size:14px; font-weight:600; color:#2c3e50; }}
.salary-tips {{ background:#fef9e7; border-radius:8px; padding:16px; margin-bottom:12px; }}
.salary-tips h4 {{ font-size:14px; color:#e67e22; margin-bottom:8px; }}
.salary-tips p {{ font-size:13px; color:#555; }}
.disclaimer {{ font-size:11px; color:#bdc3c7; text-align:center; }}

/* Radar Chart */
.radar-chart {{ display:block; margin:0 auto; max-width:400px; }}

/* Footer */
.footer {{ text-align:center; padding:20px; color:#bdc3c7; font-size:12px; margin-top:20px; }}
.footer a {{ color:#667eea; text-decoration:none; }}

/* Responsive */
@media (max-width:640px) {{
  .header {{ padding:24px 16px; }}
  .header h1 {{ font-size:22px; }}
  .tabs {{ gap:4px; }}
  .tab-btn {{ padding:6px 10px; font-size:11px; }}
  .info-grid {{ grid-template-columns:1fr 1fr; }}
  .question-grid {{ grid-template-columns:1fr; }}
  .salary-overview {{ grid-template-columns:1fr; }}
}}

/* Print */
@media print {{
  .tabs {{ display:none; }}
  .module-card {{ break-inside:avoid; box-shadow:none; border:1px solid #e0e0e0; }}
  body {{ background:#fff; }}
}}
</style>
</head>
<body>
<div class="container">

<!-- Header -->
<div class="header">
  <h1>📊 {data.get('module_1_basic_info', {}).get('title', '岗位解读报告')}</h1>
  <div class="subtitle">AI 智能深度解读 · 8 维分析</div>
  <div class="meta">
    <span>🏢 {data.get('module_1_basic_info', {}).get('company', '未知公司')}</span>
    <span>📍 {data.get('module_1_basic_info', {}).get('location', '未知')}</span>
    <span>💰 {data.get('module_1_basic_info', {}).get('salary', '面议')}</span>
    <span>📅 {datetime.now().strftime('%Y-%m-%d')}</span>
  </div>
</div>

<!-- Tabs -->
<div class="tabs">
  <button class="tab-btn active" onclick="scrollToModule('module-1')">📋 岗位画像</button>
  <button class="tab-btn" onclick="scrollToModule('module-2')">🔍 显性隐性</button>
  <button class="tab-btn" onclick="scrollToModule('module-3')">⭐ 权重评分</button>
  <button class="tab-btn" onclick="scrollToModule('module-4')">🎯 差距自评</button>
  <button class="tab-btn" onclick="scrollToModule('module-5')">🎤 面试预测</button>
  <button class="tab-btn" onclick="scrollToModule('module-6')">🗺 学习路线</button>
  <button class="tab-btn" onclick="scrollToModule('module-7')">🤖 ATS关键词</button>
  {f'<button class="tab-btn" onclick="scrollToModule(\'module-8\')">💰 薪资对标</button>' if has_module_8 else ''}
</div>

{render_module_one(data)}

{render_module_two(data)}

{render_module_three(data)}

{radar_svg if radar_svg else ''}

{render_module_four(data)}

{render_module_five(data)}

{render_module_six(data)}

{render_module_seven(data)}

{render_module_eight(data)}

<!-- Footer -->
<div class="footer">
  <p>🤖 由 WorkBuddy JD 智能解读技能生成 · 分析结果仅供参考</p>
  <p>💡 下一步：<a href="#" onclick="alert('请说：用 resume-jd-scorer 帮我的简历对这份 JD 打分')">简历匹配评分</a> | <a href="#" onclick="alert('请说：用 resume-assistant 按这份 JD 改写我的简历')">简历定制改写</a></p>
</div>

</div>

<script>
// Smooth scroll to module
function scrollToModule(id) {{
  const el = document.getElementById(id);
  if (el) {{
    el.scrollIntoView({{ behavior:'smooth', block:'start' }});
    // Update active tab
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
    event.target.classList.add('active');
  }}
}}

// Update active tab on scroll
const observer = new IntersectionObserver((entries) => {{
  entries.forEach(entry => {{
    if (entry.isIntersecting) {{
      const id = entry.target.id;
      document.querySelectorAll('.tab-btn').forEach(b => {{
        b.classList.toggle('active', b.getAttribute('onclick')?.includes(id));
      }});
    }}
  }});
}}, {{ threshold: 0.3 }});

document.querySelectorAll('.module-card').forEach(card => observer.observe(card));
</script>

</body>
</html>"""

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_report.py <analysis.json> [output.html]")
        sys.exit(1)

    json_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else "jd-interpretation-report.html"

    data = load_analysis(json_path)
    result_path = generate_html(data, output_path)
    # Use ASCII-safe output to avoid Windows GBK encoding issues
    print(f"[OK] Report generated: {result_path}")
    print(f"      Modules: 8-dimension JD analysis report")


if __name__ == "__main__":
    main()
