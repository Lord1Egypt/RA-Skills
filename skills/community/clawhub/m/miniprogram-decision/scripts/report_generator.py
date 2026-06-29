#!/usr/bin/env python3
"""
微信小程序开发辅助决策报告生成器
Generate professional feasibility decision report for WeChat Mini Program development.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# ============================================================
# Scoring Engine
# ============================================================

DIMENSIONS = {
    "wechat_heat": {"name": "微信热度", "weight": 0.25, "icon": "🔥"},
    "competition": {"name": "竞争格局", "weight": 0.20, "icon": "⚔️"},
    "market": {"name": "市场前景", "weight": 0.20, "icon": "📈"},
    "monetization": {"name": "变现能力", "weight": 0.15, "icon": "💰"},
    "dev_feasibility": {"name": "开发可行性", "weight": 0.10, "icon": "🔧"},
    "traffic": {"name": "流量获取", "weight": 0.10, "icon": "🚀"},
}


def calculate_total_score(scores: dict) -> dict:
    """Calculate weighted total score and rating."""
    total = 0
    dim_scores = {}
    for key, dim in DIMENSIONS.items():
        s = scores.get(key, 50)
        dim_scores[key] = s
        total += s * dim["weight"]

    total = round(total, 1)

    if total >= 80:
        rating = "✅ 强烈建议做"
        rating_desc = "市场机会明确，竞争格局有利，建议尽快立项推进"
        color = "#10B981"
        bg = "#ECFDF5"
        icon = "🚀"
    elif total >= 65:
        rating = "🟡 谨慎推进"
        rating_desc = "有一定市场机会，但需要差异化策略和更深入的需求验证"
        color = "#F59E0B"
        bg = "#FFFBEB"
        icon = "🔍"
    elif total >= 50:
        rating = "⚠️ 暂缓观望"
        rating_desc = "市场风险较高，建议先验证核心假设后再决定是否投入"
        color = "#F97316"
        bg = "#FFF7ED"
        icon = "⏸️"
    else:
        rating = "❌ 不建议做"
        rating_desc = "当前市场条件下风险过高，建议调整方向或等待时机"
        color = "#EF4444"
        bg = "#FEF2F2"
        icon = "🛑"

    return {
        "total": total,
        "dimensions": dim_scores,
        "rating": rating,
        "rating_desc": rating_desc,
        "color": color,
        "bg": bg,
        "icon": icon,
    }


# ============================================================
# Data processing helpers
# ============================================================

def safe_get(d, key, default=""):
    """Safely get nested dict value."""
    if isinstance(d, dict):
        return d.get(key, default)
    return default


def make_score_bar(score, max_score=100, color="#3B82F6", width=200):
    """Generate an SVG score bar."""
    pct = min(score / max_score, 1.0)
    bar_width = int(width * pct)

    # Color based on score
    if score >= 80:
        color = "#10B981"
    elif score >= 65:
        color = "#3B82F6"
    elif score >= 50:
        color = "#F59E0B"
    else:
        color = "#EF4444"

    return f"""<div style="display:flex;align-items:center;gap:10px;margin:6px 0;">
  <div style="flex:1;height:10px;background:#E5E7EB;border-radius:5px;overflow:hidden;">
    <div style="width:{pct*100}%;height:100%;background:{color};border-radius:5px;transition:width 0.6s;"></div>
  </div>
  <span style="font-weight:700;font-size:14px;color:{color};min-width:45px;text-align:right;">{score}分</span>
</div>"""


def make_tag(text, color="#3B82F6"):
    """Generate a colored tag."""
    return f'<span style="display:inline-block;padding:3px 10px;background:{color}15;color:{color};border-radius:12px;font-size:12px;font-weight:600;margin:2px;">{text}</span>'


# ============================================================
# HTML Report Generator
# ============================================================

def generate_report(data: dict) -> str:
    """Generate the complete HTML decision report."""

    name = safe_get(data, "name", "未命名产品")
    direction = safe_get(data, "direction", "未指定方向")
    now = datetime.now().strftime("%Y年%m月%d日 %H:%M")

    # Extract scores
    scores = safe_get(data, "scores", {})
    score_result = calculate_total_score(scores)

    # Extract sections
    wechat_index = safe_get(data, "wechat_index", {})
    competitors = safe_get(data, "competitors", {})
    industry = safe_get(data, "industry", {})
    business_model = safe_get(data, "business_model", {})
    promotion = safe_get(data, "promotion", {})
    development = safe_get(data, "development", {})
    risks = safe_get(data, "risks", {})

    # ============================================================
    # HTML Template
    # ============================================================
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>小程序可行性决策报告 - {name}</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #F3F4F6; color: #1F2937; line-height:1.7; }}
  .container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}

  /* Cover */
  .cover {{ background: linear-gradient(135deg, #1F2937 0%, #374151 100%); color: white; padding: 60px 40px; border-radius: 16px; text-align: center; margin-bottom: 24px; position: relative; overflow: hidden; }}
  .cover::before {{ content: ''; position: absolute; top: -50%; right: -20%; width: 400px; height: 400px; background: radial-gradient(circle, rgba(59,130,246,0.3) 0%, transparent 70%); border-radius: 50%; }}
  .cover h1 {{ font-size: 32px; font-weight: 800; margin-bottom: 8px; position: relative; }}
  .cover .subtitle {{ font-size: 16px; opacity: 0.7; position: relative; }}
  .cover .date {{ font-size: 13px; opacity: 0.5; margin-top: 12px; position: relative; }}

  /* Score Card */
  .score-card {{ background: {score_result['bg']}; border: 2px solid {score_result['color']}; border-radius: 16px; padding: 32px; text-align: center; margin-bottom: 24px; }}
  .score-card .big-score {{ font-size: 72px; font-weight: 900; color: {score_result['color']}; line-height: 1; }}
  .score-card .rating {{ font-size: 24px; font-weight: 700; color: {score_result['color']}; margin: 8px 0; }}
  .score-card .rating-desc {{ font-size: 14px; color: #6B7280; max-width: 500px; margin: 0 auto; }}

  /* Section */
  .section {{ background: white; border-radius: 16px; padding: 32px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.06); }}
  .section h2 {{ font-size: 22px; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }}
  .section h3 {{ font-size: 16px; font-weight: 600; color: #374151; margin: 16px 0 8px; }}
  .section p {{ margin-bottom: 10px; color: #4B5563; font-size: 14px; }}
  .section ul {{ padding-left: 20px; margin: 8px 0; }}
  .section li {{ color: #4B5563; font-size: 14px; margin: 4px 0; }}

  /* Dimension grid */
  .dim-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin: 16px 0; }}
  @media (max-width: 600px) {{ .dim-grid {{ grid-template-columns: 1fr; }} }}
  .dim-card {{ background: #F9FAFB; border-radius: 12px; padding: 20px; text-align: center; }}
  .dim-card .dim-icon {{ font-size: 28px; margin-bottom: 8px; }}
  .dim-card .dim-name {{ font-size: 13px; color: #6B7280; margin-bottom: 4px; }}
  .dim-card .dim-score {{ font-size: 28px; font-weight: 800; }}
  .dim-card .dim-weight {{ font-size: 11px; color: #9CA3AF; }}

  /* Info card */
  .info-card {{ background: #F0F9FF; border-left: 4px solid #3B82F6; border-radius: 0 8px 8px 0; padding: 16px 20px; margin: 12px 0; }}
  .info-card.warn {{ background: #FFFBEB; border-color: #F59E0B; }}
  .info-card.success {{ background: #ECFDF5; border-color: #10B981; }}
  .info-card.danger {{ background: #FEF2F2; border-color: #EF4444; }}

  /* Table */
  table {{ width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 13px; }}
  th {{ background: #F9FAFB; padding: 10px 14px; text-align: left; font-weight: 600; color: #374151; border-bottom: 2px solid #E5E7EB; }}
  td {{ padding: 10px 14px; border-bottom: 1px solid #F3F4F6; color: #4B5563; }}

  /* Tags */
  .tag {{ display: inline-block; padding: 3px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; margin: 2px; }}
  .tag-blue {{ background: #DBEAFE; color: #1D4ED8; }}
  .tag-green {{ background: #D1FAE5; color: #065F46; }}
  .tag-yellow {{ background: #FEF3C7; color: #92400E; }}
  .tag-red {{ background: #FEE2E2; color: #991B1B; }}

  /* Risk matrix */
  .risk-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }}
  @media (max-width: 600px) {{ .risk-grid {{ grid-template-columns: 1fr; }} }}
  .risk-item {{ background: #F9FAFB; border-radius: 10px; padding: 16px; }}
  .risk-item .risk-level {{ font-size: 12px; font-weight: 600; margin-bottom: 4px; }}

  /* Footer */
  .footer {{ text-align: center; padding: 24px; color: #9CA3AF; font-size: 12px; }}

  /* Print */
  @media print {{ body {{ background: white; }} .section {{ box-shadow: none; break-inside: avoid; }} }}

  /* Prospect counter */
  .prospect-meter {{ display: flex; gap: 4px; margin: 8px 0; }}
  .prospect-meter div {{ flex: 1; height: 8px; border-radius: 4px; background: #E5E7EB; }}
  .prospect-meter div.active {{ background: {score_result['color']}; }}
</style>
</head>
<body>
<div class="container">

  <!-- Cover -->
  <div class="cover">
    <h1>📱 {name}</h1>
    <div class="subtitle">{direction}</div>
    <div class="date">微信小程序开发可行性决策报告 · {now}</div>
  </div>

  <!-- Score Card -->
  <div class="score-card">
    <div class="big-score">{score_result['total']}</div>
    <div class="rating">{score_result['icon']} {score_result['rating']}</div>
    <div class="rating-desc">{score_result['rating_desc']}</div>
  </div>

  <!-- Dimension Scores -->
  <div class="section">
    <h2>📊 多维度评分矩阵</h2>
    <div class="dim-grid">
"""

    # Dimension cards
    for key, dim in DIMENSIONS.items():
        s = score_result["dimensions"].get(key, 50)
        color = "#10B981" if s >= 80 else ("#3B82F6" if s >= 65 else ("#F59E0B" if s >= 50 else "#EF4444"))
        html += f"""
      <div class="dim-card">
        <div class="dim-icon">{dim['icon']}</div>
        <div class="dim-name">{dim['name']}</div>
        <div class="dim-score" style="color:{color}">{s}</div>
        <div class="dim-weight">权重 {int(dim['weight']*100)}%</div>
      </div>"""

    html += """
    </div>
  </div>
"""

    # ============================================================
    # 1. WeChat Index Section
    # ============================================================
    wx_score = safe_get(wechat_index, "score", 50)
    wx_trend = safe_get(wechat_index, "trend", "平稳")
    wx_detail = safe_get(wechat_index, "detail", "暂无详细数据")
    wx_keywords = safe_get(wechat_index, "keywords", [])

    trend_icon = "📈" if "上升" in str(wx_trend) else ("📉" if "下降" in str(wx_trend) else "➡️")
    trend_color = "#10B981" if "上升" in str(wx_trend) else ("#EF4444" if "下降" in str(wx_trend) else "#6B7280")

    html += f"""
  <!-- 1. WeChat Index -->
  <div class="section">
    <h2>🔍 一、微信指数分析</h2>
    {make_score_bar(wx_score)}
    <div class="info-card">
      <strong>搜索热度趋势：</strong><span style="color:{trend_color};font-weight:700;">{trend_icon} {wx_trend}</span>
    </div>
    <p>{wx_detail}</p>
"""

    if wx_keywords:
        html += '<div style="margin-top:8px;"><strong>关联热词：</strong> '
        for kw in wx_keywords:
            html += f'<span class="tag tag-blue">{kw}</span> '
        html += '</div>'

    html += """
  </div>
"""

    # ============================================================
    # 2. Competitors Section
    # ============================================================
    comp_count = safe_get(competitors, "count", "未知")
    comp_top3 = safe_get(competitors, "top3", [])
    comp_detail = safe_get(competitors, "detail", "暂无详细数据")
    comp_saturation = safe_get(competitors, "saturation", "中等")

    sat_color = "#10B981" if "低" in str(comp_saturation) else ("#F59E0B" if "中" in str(comp_saturation) else "#EF4444")

    html += f"""
  <!-- 2. Competitors -->
  <div class="section">
    <h2>⚔️ 二、竞品格局分析</h2>
    <div class="info-card">
      <strong>同类小程序数量：</strong>约 <span style="font-size:20px;font-weight:800;color:#3B82F6;">{comp_count}</span> 个 &nbsp;&nbsp;
      <strong>市场饱和度：</strong><span style="color:{sat_color};font-weight:700;">{comp_saturation}</span>
    </div>
    <p>{comp_detail}</p>
"""

    if comp_top3:
        html += """
    <h3>头部竞品</h3>
    <table>
      <tr><th>排名</th><th>小程序名称</th><th>核心功能</th><th>用户规模</th></tr>"""
        for i, c in enumerate(comp_top3):
            html += f"""
      <tr>
        <td>#{i+1}</td>
        <td><strong>{safe_get(c, 'name', '未知')}</strong></td>
        <td>{safe_get(c, 'feature', '-')}</td>
        <td>{safe_get(c, 'users', '-')}</td>
      </tr>"""
        html += """
    </table>"""

    html += """
  </div>
"""

    # ============================================================
    # 3. Industry Market
    # ============================================================
    market_size = safe_get(industry, "market_size", "暂无数据")
    growth = safe_get(industry, "growth", "暂无数据")
    ind_detail = safe_get(industry, "detail", "暂无详细数据")
    policy = safe_get(industry, "policy", "暂无特殊政策风险")

    html += f"""
  <!-- 3. Industry -->
  <div class="section">
    <h2>📈 三、行业市场分析</h2>
    <div style="display:flex;gap:16px;flex-wrap:wrap;">
      <div style="flex:1;min-width:180px;background:#F0F9FF;border-radius:12px;padding:20px;text-align:center;">
        <div style="font-size:13px;color:#6B7280;margin-bottom:4px;">市场规模</div>
        <div style="font-size:24px;font-weight:800;color:#1D4ED8;">{market_size}</div>
      </div>
      <div style="flex:1;min-width:180px;background:#ECFDF5;border-radius:12px;padding:20px;text-align:center;">
        <div style="font-size:13px;color:#6B7280;margin-bottom:4px;">年增长率</div>
        <div style="font-size:24px;font-weight:800;color:#065F46;">{growth}</div>
      </div>
    </div>
    <p style="margin-top:12px;">{ind_detail}</p>
    <div class="info-card">
      <strong>政策环境：</strong>{policy}
    </div>
  </div>
"""

    # ============================================================
    # 4. Traffic Potential
    # ============================================================
    traffic_data = safe_get(data, "traffic", {})
    search_volume = safe_get(traffic_data, "search_volume", "中等")
    seo_potential = safe_get(traffic_data, "seo_potential", "中等")
    social_potential = safe_get(traffic_data, "social_potential", "中等")
    traffic_detail = safe_get(traffic_data, "detail", "暂无详细数据")

    html += f"""
  <!-- 4. Traffic -->
  <div class="section">
    <h2>🚀 四、流量潜力评估</h2>
    <table>
      <tr><th>流量渠道</th><th>潜力评级</th><th>说明</th></tr>
      <tr><td>微信搜一搜</td><td>{make_tag(search_volume, '#3B82F6')}</td><td>用户主动搜索需求，高转化</td></tr>
      <tr><td>搜一搜SEO</td><td>{make_tag(seo_potential, '#10B981')}</td><td>关键词覆盖与排名优化空间</td></tr>
      <tr><td>社交裂变</td><td>{make_tag(social_potential, '#8B5CF6')}</td><td>分享、社群、朋友圈传播</td></tr>
    </table>
    <p>{traffic_detail}</p>
    <div class="info-card success">
      <strong>💡 流量获取建议：</strong>优先布局微信搜一搜SEO，名称+描述+服务类目精准匹配；设计分享激励机制驱动社交裂变。
    </div>
  </div>
"""

    # ============================================================
    # 5. Business Model
    # ============================================================
    bm_recommend = safe_get(business_model, "recommend", [])
    bm_detail = safe_get(business_model, "detail", "暂无详细数据")

    html += f"""
  <!-- 5. Business Model -->
  <div class="section">
    <h2>💰 五、商业模式建议</h2>
    <p>{bm_detail}</p>
"""

    if bm_recommend:
        html += '<div style="display:flex;flex-wrap:wrap;gap:12px;margin:12px 0;">'
        model_colors = ["#1D4ED8", "#065F46", "#92400E", "#7C3AED", "#BE185D", "#0E7490"]
        for i, bm in enumerate(bm_recommend):
            color = model_colors[i % len(model_colors)]
            priority = "⭐" * (3 - i) if i < 3 else ""
            html += f"""
        <div style="flex:1;min-width:160px;background:white;border:2px solid {color}20;border-radius:12px;padding:16px;text-align:center;">
          <div style="font-size:20px;margin-bottom:4px;">{priority}</div>
          <div style="font-weight:700;color:{color};margin-bottom:4px;">{safe_get(bm, 'name', '')}</div>
          <div style="font-size:12px;color:#6B7280;">{safe_get(bm, 'desc', '')}</div>
        </div>"""
        html += '</div>'

    # Common monetization reference
    html += """
    <h3>主流变现模式参考</h3>
    <table>
      <tr><th>模式</th><th>适用场景</th><th>收入潜力</th></tr>
      <tr><td>流量主广告</td><td>内容/工具类</td><td>⭐~⭐⭐⭐</td></tr>
      <tr><td>电商变现</td><td>实物/虚拟商品</td><td>⭐⭐~⭐⭐⭐⭐⭐</td></tr>
      <tr><td>会员订阅</td><td>SaaS/社区/知识付费</td><td>⭐⭐⭐~⭐⭐⭐⭐</td></tr>
      <tr><td>佣金/平台抽成</td><td>撮合交易类</td><td>⭐⭐⭐⭐~⭐⭐⭐⭐⭐</td></tr>
      <tr><td>游戏内购</td><td>小游戏</td><td>⭐⭐⭐~⭐⭐⭐⭐⭐</td></tr>
      <tr><td>SaaS服务费</td><td>B端工具</td><td>⭐⭐⭐~⭐⭐⭐⭐⭐</td></tr>
    </table>
  </div>
"""

    # ============================================================
    # 6. Promotion Strategy
    # ============================================================
    promo_strategies = safe_get(promotion, "strategies", [])
    promo_detail = safe_get(promotion, "detail", "暂无详细数据")

    html += f"""
  <!-- 6. Promotion -->
  <div class="section">
    <h2>📢 六、推广策略建议</h2>
    <p>{promo_detail}</p>
"""

    if promo_strategies:
        html += '<div style="display:flex;flex-direction:column;gap:10px;">'
        for i, st in enumerate(promo_strategies):
            html += f"""
        <div class="info-card">
          <strong>策略{['一','二','三','四','五','六'][i] if i < 6 else i+1}：{safe_get(st, 'title', '')}</strong>
          <p style="margin-top:4px;">{safe_get(st, 'desc', '')}</p>
        </div>"""
        html += '</div>'

    # Default promotion strategies
    html += """
    <h3>通用推广路径</h3>
    <table>
      <tr><th>阶段</th><th>策略</th><th>预期效果</th></tr>
      <tr><td>冷启动（0-1K用户）</td><td>朋友圈+社群种子用户邀请</td><td>获取首批真实反馈</td></tr>
      <tr><td>增长期（1K-10K）</td><td>搜一搜SEO+分享有奖裂变</td><td>自然流量稳定增长</td></tr>
      <tr><td>规模化（10K+）</td><td>公众号导流+广告投放+矩阵</td><td>规模化获客</td></tr>
    </table>
  </div>
"""

    # ============================================================
    # 7. Development Guide
    # ============================================================
    dev_tech = safe_get(development, "tech_stack", "推荐使用微信原生框架或Taro/uni-app跨端方案")
    dev_cost = safe_get(development, "cost", "基础版3-10万，SaaS模板700-6800元/年")
    dev_tips = safe_get(development, "tips", [])
    dev_detail = safe_get(development, "detail", "暂无详细数据")

    html += f"""
  <!-- 7. Development -->
  <div class="section">
    <h2>🔧 七、开发指南</h2>
    <div class="info-card">
      <strong>推荐技术栈：</strong>{dev_tech}
    </div>
    <div class="info-card warn">
      <strong>预估开发成本：</strong>{dev_cost}
    </div>
    <p>{dev_detail}</p>
"""

    if dev_tips:
        html += '<h3>关键避坑要点</h3><ul>'
        for tip in dev_tips:
            html += f'<li>{tip}</li>'
        html += '</ul>'

    html += """
    <h3>开发检查清单</h3>
    <table>
      <tr><th>阶段</th><th>关键事项</th><th>常见坑</th></tr>
      <tr><td>注册认证</td><td>企业/个体户资质、微信认证（300元/年）</td><td>个人主体功能受限</td></tr>
      <tr><td>类目选择</td><td>确认所需服务类目与资质要求</td><td>类目不匹配导致审核失败</td></tr>
      <tr><td>UI/UX设计</td><td>遵循微信设计规范，适配不同机型</td><td>过度定制导致体验不一致</td></tr>
      <tr><td>功能开发</td><td>先MVP验证，再迭代丰富</td><td>贪大求全，开发周期失控</td></tr>
      <tr><td>审核上线</td><td>准备齐全资质材料，注册即审核</td><td>资质不全反复被拒</td></tr>
      <tr><td>持续迭代</td><td>数据驱动，周迭代节奏</td><td>上线后无人维护</td></tr>
    </table>
  </div>
"""

    # ============================================================
    # 8. Risk Assessment
    # ============================================================
    risk_items = safe_get(risks, "items", [])
    if not risk_items:
        risk_items = [
            {"name": "政策合规风险", "level": "中", "desc": "微信平台规则变化可能影响运营"},
            {"name": "竞争加剧风险", "level": "中", "desc": "同类产品快速涌入导致获客成本上升"},
            {"name": "用户留存风险", "level": "高", "desc": "小程序用完即走特性导致留存难"},
            {"name": "变现难度风险", "level": "中", "desc": "用户付费意愿培养需要时间"},
        ]

    html += """
  <!-- 8. Risks -->
  <div class="section">
    <h2>⚠️ 八、风险提示</h2>
    <div class="risk-grid">
"""
    level_colors = {"高": "#EF4444", "中": "#F59E0B", "低": "#10B981"}
    level_bg = {"高": "#FEE2E2", "中": "#FEF3C7", "低": "#D1FAE5"}
    for risk in risk_items:
        r_level = safe_get(risk, "level", "中")
        r_color = level_colors.get(r_level, "#F59E0B")
        r_bg = level_bg.get(r_level, "#FEF3C7")
        html += f"""
      <div class="risk-item">
        <div class="risk-level" style="color:{r_color};">⚠️ {r_level}风险</div>
        <strong>{safe_get(risk, 'name', '')}</strong>
        <p style="font-size:13px;margin-top:4px;">{safe_get(risk, 'desc', '')}</p>
      </div>"""
    html += """
    </div>
  </div>
"""

    # ============================================================
    # 9. Final Decision
    # ============================================================
    html += f"""
  <!-- 9. Final Decision -->
  <div class="section" style="background: {score_result['bg']}; border: 2px solid {score_result['color']};">
    <h2>🎯 九、综合决策建议</h2>
    <div style="text-align:center;padding:20px;">
      <div style="font-size:48px;margin-bottom:8px;">{score_result['icon']}</div>
      <div style="font-size:28px;font-weight:800;color:{score_result['color']};margin-bottom:8px;">{score_result['rating']}</div>
      <div style="font-size:16px;color:#374151;margin-bottom:16px;">综合评分：<span style="font-size:36px;font-weight:900;color:{score_result['color']};">{score_result['total']}</span> / 100</div>
      <p style="max-width:500px;margin:0 auto;color:#6B7280;">{score_result['rating_desc']}</p>
    </div>

    <h3>下一步行动建议</h3>
    <table>
      <tr><th>优先级</th><th>行动项</th><th>建议时间</th></tr>
      <tr><td>P0</td><td>完成详细需求调研与用户访谈（10+目标用户）</td><td>第1-2周</td></tr>
      <tr><td>P0</td><td>深度体验3-5款头部竞品，输出竞品分析文档</td><td>第1-2周</td></tr>
      <tr><td>P1</td><td>设计MVP功能范围，制作产品原型</td><td>第2-3周</td></tr>
      <tr><td>P1</td><td>注册小程序账号，完成认证与类目申请</td><td>第3周</td></tr>
      <tr><td>P2</td><td>启动MVP开发（2-4周内完成）</td><td>第4-8周</td></tr>
      <tr><td>P2</td><td>种子用户招募与灰度测试</td><td>第8-10周</td></tr>
    </table>
  </div>

  <!-- Footer -->
  <div class="footer">
    <p>本报告由 AI 辅助生成 · 数据来源：公开信息搜索 · 仅供参考，不构成投资建议</p>
    <p>报告生成时间：{now}</p>
  </div>

</div>
</body>
</html>"""

    return html


# ============================================================
# CLI Entry Point
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="微信小程序可行性决策报告生成器")
    parser.add_argument("--name", required=True, help="产品名称")
    parser.add_argument("--direction", required=True, help="产品方向")
    parser.add_argument("--output", required=True, help="输出HTML文件路径")
    parser.add_argument("--scores", default="{}", help="评分JSON")
    parser.add_argument("--wechat-index", default="{}", help="微信指数数据JSON")
    parser.add_argument("--competitors", default="{}", help="竞品数据JSON")
    parser.add_argument("--industry", default="{}", help="行业数据JSON")
    parser.add_argument("--business-model", default="{}", help="商业模式数据JSON")
    parser.add_argument("--promotion", default="{}", help="推广策略数据JSON")
    parser.add_argument("--development", default="{}", help="开发指南数据JSON")
    parser.add_argument("--traffic", default="{}", help="流量数据JSON")
    parser.add_argument("--risks", default="{}", help="风险数据JSON")

    args = parser.parse_args()

    data = {
        "name": args.name,
        "direction": args.direction,
        "scores": json.loads(args.scores),
        "wechat_index": json.loads(args.wechat_index),
        "competitors": json.loads(args.competitors),
        "industry": json.loads(args.industry),
        "business_model": json.loads(args.business_model),
        "promotion": json.loads(args.promotion),
        "development": json.loads(args.development),
        "traffic": json.loads(args.traffic),
        "risks": json.loads(args.risks),
    }

    html = generate_report(data)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html, encoding="utf-8")

    print(f"✅ 报告已生成: {output_path}")


if __name__ == "__main__":
    main()
