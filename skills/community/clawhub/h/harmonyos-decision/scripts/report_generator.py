#!/usr/bin/env python3
"""
鸿蒙原生应用开发辅助决策报告生成器
Generate professional feasibility decision report for HarmonyOS Native App development.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

# ============================================================
# Scoring Engine
# ============================================================

DIMENSIONS = {
    "ecosystem_heat": {"name": "生态热度", "weight": 0.25, "icon": "🔥"},
    "competition": {"name": "竞争格局", "weight": 0.20, "icon": "⚔️"},
    "market": {"name": "市场前景", "weight": 0.20, "icon": "📈"},
    "monetization": {"name": "变现能力", "weight": 0.15, "icon": "💰"},
    "dev_feasibility": {"name": "开发可行性", "weight": 0.10, "icon": "🔧"},
    "distribution": {"name": "分发获客", "weight": 0.10, "icon": "📲"},
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
        rating_desc = "鸿蒙生态红利窗口期明确，竞争格局有利，建议尽快立项推进"
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
        rating_desc = "当前市场条件下风险过高，建议调整方向或等待生态更成熟"
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


def make_score_bar(score, max_score=100, width=200):
    """Generate an HTML score bar."""
    pct = min(score / max_score, 1.0)

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
    """Generate the complete HTML decision report for HarmonyOS app development."""

    name = safe_get(data, "name", "未命名产品")
    direction = safe_get(data, "direction", "未指定方向")
    now = datetime.now().strftime("%Y年%m月%d日 %H:%M")

    # Extract scores
    scores = safe_get(data, "scores", {})
    score_result = calculate_total_score(scores)

    # Extract sections
    ecosystem = safe_get(data, "ecosystem", {})
    competitors = safe_get(data, "competitors", {})
    industry = safe_get(data, "industry", {})
    user_profile = safe_get(data, "user_profile", {})
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
<title>鸿蒙原生应用可行性决策报告 - {name}</title>
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', 'Microsoft YaHei', sans-serif; background: #F3F4F6; color: #1F2937; line-height:1.7; }}
  .container {{ max-width: 900px; margin: 0 auto; padding: 20px; }}

  /* Cover */
  .cover {{ background: linear-gradient(135deg, #0D1B2A 0%, #1B2838 50%, #2C3E50 100%); color: white; padding: 60px 40px; border-radius: 16px; text-align: center; margin-bottom: 24px; position: relative; overflow: hidden; }}
  .cover::before {{ content: ''; position: absolute; top: -50%; right: -20%; width: 400px; height: 400px; background: radial-gradient(circle, rgba(251, 104, 16, 0.3) 0%, transparent 70%); border-radius: 50%; }}
  .cover::after {{ content: ''; position: absolute; bottom: -30%; left: -10%; width: 300px; height: 300px; background: radial-gradient(circle, rgba(0, 180, 216, 0.2) 0%, transparent 70%); border-radius: 50%; }}
  .cover h1 {{ font-size: 32px; font-weight: 800; margin-bottom: 8px; position: relative; }}
  .cover .subtitle {{ font-size: 16px; opacity: 0.7; position: relative; }}
  .cover .date {{ font-size: 13px; opacity: 0.5; margin-top: 12px; position: relative; }}
  .cover .badge {{ display: inline-block; background: rgba(251, 104, 16, 0.3); border: 1px solid rgba(251, 104, 16, 0.5); padding: 4px 14px; border-radius: 20px; font-size: 13px; margin-top: 12px; position: relative; }}

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
  .info-card.purple {{ background: #F5F3FF; border-color: #7C3AED; }}

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
  .tag-orange {{ background: #FED7AA; color: #9A3412; }}

  /* Risk grid */
  .risk-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }}
  @media (max-width: 600px) {{ .risk-grid {{ grid-template-columns: 1fr; }} }}
  .risk-item {{ background: #F9FAFB; border-radius: 10px; padding: 16px; }}
  .risk-item .risk-level {{ font-size: 12px; font-weight: 600; margin-bottom: 4px; }}

  /* Pain point grid */
  .pain-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; margin: 16px 0; }}
  @media (max-width: 600px) {{ .pain-grid {{ grid-template-columns: 1fr; }} }}
  .pain-card {{ background: #FFF7ED; border: 1px solid #FED7AA; border-radius: 10px; padding: 16px; }}
  .pain-card .pain-icon {{ font-size: 20px; margin-bottom: 4px; }}
  .pain-card .pain-title {{ font-weight: 700; color: #9A3412; font-size: 14px; margin-bottom: 4px; }}
  .pain-card .pain-desc {{ font-size: 12px; color: #78350F; }}
  .pain-card .pain-fix {{ font-size: 12px; color: #065F46; margin-top: 4px; }}

  /* Stat cards */
  .stat-row {{ display: flex; gap: 16px; flex-wrap: wrap; margin: 12px 0; }}
  .stat-card {{ flex: 1; min-width: 160px; border-radius: 12px; padding: 20px; text-align: center; }}
  .stat-card .stat-value {{ font-size: 26px; font-weight: 800; }}
  .stat-card .stat-label {{ font-size: 12px; color: #6B7280; margin-top: 4px; }}

  /* Footer */
  .footer {{ text-align: center; padding: 24px; color: #9CA3AF; font-size: 12px; }}

  /* Print */
  @media print {{ body {{ background: white; }} .section {{ box-shadow: none; break-inside: avoid; }} }}
</style>
</head>
<body>
<div class="container">

  <!-- Cover -->
  <div class="cover">
    <h1>🦋 {name}</h1>
    <div class="subtitle">{direction}</div>
    <div class="badge">HarmonyOS 原生应用开发可行性决策报告</div>
    <div class="date">{now}</div>
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
    # 1. HarmonyOS Ecosystem Section
    # ============================================================
    eco_score = safe_get(ecosystem, "score", 50)
    eco_trend = safe_get(ecosystem, "trend", "快速上升")
    eco_devices = safe_get(ecosystem, "device_count", "5.1亿+")
    eco_share = safe_get(ecosystem, "market_share", "18%")
    eco_detail = safe_get(ecosystem, "detail", "鸿蒙已成为中国第二大移动操作系统，市场份额达18%。\"纯血\"鸿蒙设备从2025年11月的2300万台增长到2026年初的5100万台，4个月内翻倍，增长速度行业最快。华为每年投入60亿元激励开发者，生态正处价值洼地。")

    trend_icon = "📈" if "上升" in str(eco_trend) else ("📉" if "下降" in str(eco_trend) else "➡️")
    trend_color = "#10B981" if "上升" in str(eco_trend) else ("#EF4444" if "下降" in str(eco_trend) else "#6B7280")

    html += f"""
  <!-- 1. Ecosystem -->
  <div class="section">
    <h2>🔥 一、鸿蒙生态热度分析</h2>
    {make_score_bar(eco_score)}
    <div class="stat-row">
      <div class="stat-card" style="background:#F0F9FF;">
        <div class="stat-value" style="color:#1D4ED8;">{eco_share}</div>
        <div class="stat-label">中国市场份额</div>
      </div>
      <div class="stat-card" style="background:#ECFDF5;">
        <div class="stat-value" style="color:#065F46;">{eco_devices}</div>
        <div class="stat-label">纯血鸿蒙设备数</div>
      </div>
      <div class="stat-card" style="background:#FFFBEB;">
        <div class="stat-value" style="color:#92400E;">35万+</div>
        <div class="stat-label">原生应用/服务数</div>
      </div>
    </div>
    <div class="info-card">
      <strong>生态增长趋势：</strong><span style="color:{trend_color};font-weight:700;">{trend_icon} {eco_trend}</span>
      <span style="margin-left:12px;font-size:13px;color:#6B7280;">中国第二大移动OS | 华为年投60亿激励</span>
    </div>
    <p>{eco_detail}</p>
    <div class="info-card success">
      <strong>💡 生态红利判断：</strong>当前鸿蒙生态处于"价值洼地"阶段，是独立开发者和中小团队弯道超车的最佳时机。华为应用市场推荐位对早期入场者倾斜明显。
    </div>
  </div>
"""

    # ============================================================
    # 2. Competitors Section
    # ============================================================
    comp_count = safe_get(competitors, "count", "未知")
    comp_top3 = safe_get(competitors, "top3", [])
    comp_detail = safe_get(competitors, "detail", "暂无详细数据")
    comp_saturation = safe_get(competitors, "saturation", "低")

    sat_color = "#10B981" if "低" in str(comp_saturation) else ("#F59E0B" if "中" in str(comp_saturation) else "#EF4444")

    html += f"""
  <!-- 2. Competitors -->
  <div class="section">
    <h2>⚔️ 二、竞品格局分析</h2>
    <div class="info-card">
      <strong>AppGallery同类应用：</strong>约 <span style="font-size:20px;font-weight:800;color:#3B82F6;">{comp_count}</span> 个 &nbsp;&nbsp;
      <strong>市场饱和度：</strong><span style="color:{sat_color};font-weight:700;">{comp_saturation}</span>
    </div>
    <p>{comp_detail}</p>
"""

    if comp_top3:
        html += """
    <h3>头部竞品</h3>
    <table>
      <tr><th>排名</th><th>应用名称</th><th>核心功能</th><th>下载量级</th></tr>"""
        for i, c in enumerate(comp_top3):
            html += f"""
      <tr>
        <td>#{i+1}</td>
        <td><strong>{safe_get(c, 'name', '未知')}</strong></td>
        <td>{safe_get(c, 'feature', '-')}</td>
        <td>{safe_get(c, 'downloads', '-')}</td>
      </tr>"""
        html += """
    </table>"""

    html += f"""
    <div class="info-card warn">
      <strong>⚠️ 竞争窗口期评估：</strong>鸿蒙原生应用生态仍处早期，竞争远低于Android/iOS。传统大厂App虽有鸿蒙版但体验参差不齐，垂直领域存在大量空白机会。
    </div>
  </div>
"""

    # ============================================================
    # 3. Industry Market
    # ============================================================
    market_size = safe_get(industry, "market_size", "暂无数据")
    growth = safe_get(industry, "growth", "暂无数据")
    ind_detail = safe_get(industry, "detail", "暂无详细数据")
    policy = safe_get(industry, "policy", "国家大力支持国产操作系统生态建设")

    html += f"""
  <!-- 3. Industry -->
  <div class="section">
    <h2>📈 三、行业市场分析</h2>
    <div class="stat-row">
      <div class="stat-card" style="background:#F0F9FF;">
        <div class="stat-value" style="color:#1D4ED8;">{market_size}</div>
        <div class="stat-label">市场规模</div>
      </div>
      <div class="stat-card" style="background:#ECFDF5;">
        <div class="stat-value" style="color:#065F46;">{growth}</div>
        <div class="stat-label">年增长率</div>
      </div>
    </div>
    <p>{ind_detail}</p>
    <div class="info-card">
      <strong>📋 政策环境：</strong>{policy}
    </div>
  </div>
"""

    # ============================================================
    # 4. User Profile
    # ============================================================
    up_age = safe_get(user_profile, "age_range", "25-45岁为主")
    up_cities = safe_get(user_profile, "tier_cities", "新一线及二三线城市")
    up_consumption = safe_get(user_profile, "consumption", "中等偏上，品牌忠诚度高")
    up_detail = safe_get(user_profile, "detail", "鸿蒙用户以华为/荣耀手机用户为主，年龄集中在25-45岁，覆盖一二线到下沉市场。用户群体消费力中等偏上，对国产品牌认同感强，换机周期约2-3年。")

    html += f"""
  <!-- 4. User Profile -->
  <div class="section">
    <h2>👥 四、鸿蒙用户画像</h2>
    <table>
      <tr><th>维度</th><th>特征</th><th>对产品的影响</th></tr>
      <tr><td>👤 年龄分布</td><td>{up_age}</td><td>成熟用户群体，付费意愿较高</td></tr>
      <tr><td>🏙️ 城市等级</td><td>{up_cities}</td><td>覆盖广泛，适合大众化产品</td></tr>
      <tr><td>💳 消费力</td><td>{up_consumption}</td><td>可支撑中高客单价变现</td></tr>
      <tr><td>🔄 换机周期</td><td>约2-3年</td><td>用户粘性较强，长期留存机会大</td></tr>
    </table>
    <p>{up_detail}</p>
  </div>
"""

    # ============================================================
    # 5. Distribution & Traffic
    # ============================================================
    traffic_data = safe_get(data, "traffic", {})
    appgallery_potential = safe_get(traffic_data, "appgallery_potential", "高")
    yuanservice_potential = safe_get(traffic_data, "yuanservice_potential", "中")
    huawei_search_potential = safe_get(traffic_data, "huawei_search_potential", "中")
    traffic_detail = safe_get(traffic_data, "detail", "")

    html += f"""
  <!-- 5. Distribution -->
  <div class="section">
    <h2>📲 五、分发与流量评估</h2>
    <table>
      <tr><th>分发渠道</th><th>潜力评级</th><th>特点</th></tr>
      <tr>
        <td><strong>AppGallery推荐位</strong></td>
        <td>{make_tag(appgallery_potential, '#3B82F6')}</td>
        <td>早期入场者获推荐倾斜，免费流量红利期</td>
      </tr>
      <tr>
        <td><strong>元服务卡片</strong></td>
        <td>{make_tag(yuanservice_potential, '#8B5CF6')}</td>
        <td>免安装即用，桌面/负一屏直达，获客成本极低</td>
      </tr>
      <tr>
        <td><strong>华为搜索SEO</strong></td>
        <td>{make_tag(huawei_search_potential, '#F59E0B')}</td>
        <td>关键词覆盖与排名优化，精准流量入口</td>
      </tr>
      <tr>
        <td><strong>华为广告(Ads Kit)</strong></td>
        <td>{make_tag('中等', '#EF4444')}</td>
        <td>精准投放，但用户规模限制天花板</td>
      </tr>
      <tr>
        <td><strong>多设备协同流量</strong></td>
        <td>{make_tag('高', '#10B981')}</td>
        <td>手机+平板+手表+车机，多端一次触达</td>
      </tr>
    </table>
    <p>{traffic_detail}</p>
    <div class="info-card success">
      <strong>💡 分发策略建议：</strong>优先利用元服务（免安装）降低获客门槛 + AppGallery推荐位获取免费流量。元服务特别适合工具类、信息类产品，可实现"即用即走"体验。
    </div>
  </div>
"""

    # ============================================================
    # 6. Business Model
    # ============================================================
    bm_recommend = safe_get(business_model, "recommend", [])
    bm_detail = safe_get(business_model, "detail", "暂无详细数据")

    html += f"""
  <!-- 6. Business Model -->
  <div class="section">
    <h2>💰 六、商业模式建议</h2>
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

    # Monetization reference
    html += """
    <h3>鸿蒙生态变现模式参考</h3>
    <table>
      <tr><th>模式</th><th>适用场景</th><th>鸿蒙特有优势</th></tr>
      <tr><td>应用内购买(IAP)</td><td>游戏/会员/虚拟商品</td><td>华为支付(HMS Core)集成便捷</td></tr>
      <tr><td>订阅制</td><td>SaaS/社区/知识付费</td><td>用户品牌忠诚度高，续费率好</td></tr>
      <tr><td>广告变现</td><td>工具/内容类</td><td>华为广告(Ads Kit)生态内闭环</td></tr>
      <tr><td>元服务付费</td><td>轻量工具/生活服务</td><td>免安装+桌面卡片，转化路径极短</td></tr>
      <tr><td>IoT联动付费</td><td>智能家居/健康/出行</td><td>鸿蒙分布式能力，多设备场景变现</td></tr>
      <tr><td>开发者激励</td><td>创新应用/AI类</td><td>华为60亿激励+天工计划10亿，个人最高600万</td></tr>
    </table>
    <div class="info-card purple">
      <strong>🎁 激励计划利用：</strong>华为"鸿蒙应用开发者激励计划"覆盖应用、游戏、元服务三类。个人开发者最高可获600万元奖金。天工计划10亿元专项扶持AI生态创新。建议产品规划阶段就对齐激励要求。
    </div>
  </div>
"""

    # ============================================================
    # 7. Promotion Strategy & Cost
    # ============================================================
    promo_strategies = safe_get(promotion, "strategies", [])
    promo_detail = safe_get(promotion, "detail", "暂无详细数据")
    promo_cost = safe_get(promotion, "cost_estimate", "初期预算建议5-15万")

    html += f"""
  <!-- 7. Promotion -->
  <div class="section">
    <h2>📢 七、推广策略与成本估算</h2>
    <div class="info-card warn">
      <strong>💰 推广成本预估：</strong>{promo_cost}
    </div>
    <p>{promo_detail}</p>
"""

    if promo_strategies:
        html += '<div style="display:flex;flex-direction:column;gap:10px;">'
        stage_labels = ['一', '二', '三', '四', '五', '六']
        for i, st in enumerate(promo_strategies):
            html += f"""
        <div class="info-card">
          <strong>策略{stage_labels[i] if i < 6 else i+1}：{safe_get(st, 'title', '')}</strong>
          <p style="margin-top:4px;">{safe_get(st, 'desc', '')}</p>
        </div>"""
        html += '</div>'

    html += """
    <h3>鸿蒙推广阶段路径</h3>
    <table>
      <tr><th>阶段</th><th>策略</th><th>预算建议</th><th>预期效果</th></tr>
      <tr><td>冷启动（0-5K用户）</td><td>元服务卡片+AppGallery推荐位+华为社区</td><td>1-3万</td><td>获取种子用户与评价</td></tr>
      <tr><td>增长期（5K-50K）</td><td>华为广告投放+SEO优化+社交裂变</td><td>5-15万</td><td>自然流量稳定增长</td></tr>
      <tr><td>规模化（50K+）</td><td>多端协同推广+KOL合作+矩阵运营</td><td>15万+</td><td>规模化获客与品牌建设</td></tr>
    </table>
    <div class="info-card">
      <strong>📌 鸿蒙特有推广优势：</strong>元服务支持桌面卡片直达，用户无需下载即可使用核心功能，极大降低获客门槛。AppGallery对原生鸿蒙新应用有推荐位倾斜政策。
    </div>
  </div>
"""

    # ============================================================
    # 8. Development Guide
    # ============================================================
    dev_tech = safe_get(development, "tech_stack", "ArkTS + ArkUI + DevEco Studio")
    dev_cost = safe_get(development, "cost", "基础版15-30万，中大型50万+")
    dev_talent = safe_get(development, "talent_gap", "人才缺口百万级，资深工程师50万+/年")
    dev_tips = safe_get(development, "tips", [])
    dev_detail = safe_get(development, "detail", "")

    html += f"""
  <!-- 8. Development -->
  <div class="section">
    <h2>🔧 八、开发指南与成本</h2>
    <div class="info-card">
      <strong>🛠️ 推荐技术栈：</strong>{dev_tech}
    </div>
    <div class="info-card warn">
      <strong>💵 预估开发成本：</strong>{dev_cost}
    </div>
    <div class="info-card danger">
      <strong>👨‍💻 人才市场：</strong>{dev_talent}
    </div>
    <p>{dev_detail}</p>
"""

    if dev_tips:
        html += '<h3>关键避坑要点</h3><ul>'
        for tip in dev_tips:
            html += f'<li>✅ {tip}</li>'
        html += '</ul>'

    # Default pain points
    html += """
    <h3>鸿蒙开发核心痛点与应对</h3>
    <div class="pain-grid">
      <div class="pain-card">
        <div class="pain-icon">📚</div>
        <div class="pain-title">ArkTS学习成本</div>
        <div class="pain-desc">基于TS但声明式UI范式不同，有React/TS经验者1-2周上手，纯新手1-2月</div>
        <div class="pain-fix">➡️ 优先招TS/React背景开发者；利用华为官方文档和示例代码</div>
      </div>
      <div class="pain-card">
        <div class="pain-icon">👥</div>
        <div class="pain-title">人才缺口百万级</div>
        <div class="pain-desc">2025年缺口100-300万，资深工程师薪资溢价35%+，招聘难度大</div>
        <div class="pain-fix">➡️ 利用华为激励计划补贴人力成本；考虑外部技术团队合作</div>
      </div>
      <div class="pain-card">
        <div class="pain-icon">📦</div>
        <div class="pain-title">第三方库不成熟</div>
        <div class="pain-desc">ohpm生态仍早期，npm生态不可用，部分功能需自研</div>
        <div class="pain-fix">➡️ MVP阶段简化功能依赖；核心模块自研；关注ohpm生态更新</div>
      </div>
      <div class="pain-card">
        <div class="pain-icon">📱</div>
        <div class="pain-title">设备碎片化适配</div>
        <div class="pain-desc">需适配手机/平板/手表/车机/PC多端，测试工作量大</div>
        <div class="pain-fix">➡️ 利用"一次开发多端部署"架构；优先手机端，逐步扩展</div>
      </div>
      <div class="pain-card">
        <div class="pain-icon">✅</div>
        <div class="pain-title">审核上架流程</div>
        <div class="pain-desc">首次上架3-7个工作日，需准备软著、隐私政策等多项材料</div>
        <div class="pain-fix">➡️ 提前准备材料清单；元服务选"单机工具类"可免软著</div>
      </div>
      <div class="pain-card">
        <div class="pain-icon">🌍</div>
        <div class="pain-title">纯血鸿蒙用户规模</div>
        <div class="pain-desc">当前仅5100万+纯血设备，用户基数远小于Android/iOS</div>
        <div class="pain-fix">➡️ 优先做高频刚需场景；同时规划Android/iOS版本兜底</div>
      </div>
    </div>

    <h3>开发上架检查清单</h3>
    <table>
      <tr><th>阶段</th><th>关键事项</th><th>常见坑</th></tr>
      <tr><td>注册认证</td><td>华为开发者联盟注册、实名认证（个人/企业）</td><td>企业账号需营业执照，个人功能受限</td></tr>
      <tr><td>环境搭建</td><td>DevEco Studio安装、SDK配置、模拟器</td><td>Windows/Mac环境差异，API版本兼容</td></tr>
      <tr><td>签名配置</td><td>生成.p12证书→申请.cer发布证书→配置Profile</td><td>调试/发布证书混用导致打包失败</td></tr>
      <tr><td>UI/UX设计</td><td>遵循华为设计规范，适配多设备分辨率</td><td>图标须用华为官方模板，否则拒审</td></tr>
      <tr><td>功能开发</td><td>先MVP验证核心功能，再迭代丰富</td><td>贪大求全，忽略鸿蒙特有API学习</td></tr>
      <tr><td>测试适配</td><td>多设备兼容性测试(手机/平板/手表)</td><td>模拟器与真机行为差异</td></tr>
      <tr><td>审核上线</td><td>准备截图(3张+)、隐私政策、软著等</td><td>重名、材料不全反复被拒</td></tr>
      <tr><td>持续迭代</td><td>数据驱动，关注AppGallery评分与反馈</td><td>上线后无人维护，被市场下架</td></tr>
    </table>
  </div>
"""

    # ============================================================
    # 9. Risk Assessment
    # ============================================================
    risk_items = safe_get(risks, "items", [])
    if not risk_items:
        risk_items = [
            {"name": "生态依赖风险", "level": "高", "desc": "鸿蒙增长完全依赖华为自有设备出货量，无第三方OEM支持，一旦华为手机市场下滑将直接影响应用分发"},
            {"name": "用户规模风险", "level": "高", "desc": "纯血鸿蒙设备仅5100万+，DAU天花板较低，大规模商业化需等待用户基数进一步提升"},
            {"name": "技术迭代风险", "level": "中", "desc": "ArkTS/ArkUI快速迭代中，API可能变动，需持续投入适配成本"},
            {"name": "人才短缺风险", "level": "中", "desc": "鸿蒙开发者缺口百万级，资深人才招聘困难且成本高"},
            {"name": "变现不确定性", "level": "中", "desc": "鸿蒙生态变现体系仍在完善中，部分品类付费转化数据不足"},
            {"name": "审核政策风险", "level": "低", "desc": "华为审核规则相对透明，但政策可能调整影响应用运营"},
        ]

    html += """
  <!-- 9. Risks -->
  <div class="section">
    <h2>⚠️ 九、风险提示</h2>
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
    # 10. Final Decision
    # ============================================================
    html += f"""
  <!-- 10. Final Decision -->
  <div class="section" style="background: {score_result['bg']}; border: 2px solid {score_result['color']};">
    <h2>🎯 十、综合决策建议</h2>
    <div style="text-align:center;padding:20px;">
      <div style="font-size:48px;margin-bottom:8px;">{score_result['icon']}</div>
      <div style="font-size:28px;font-weight:800;color:{score_result['color']};margin-bottom:8px;">{score_result['rating']}</div>
      <div style="font-size:16px;color:#374151;margin-bottom:16px;">综合评分：<span style="font-size:36px;font-weight:900;color:{score_result['color']};">{score_result['total']}</span> / 100</div>
      <p style="max-width:500px;margin:0 auto;color:#6B7280;">{score_result['rating_desc']}</p>
    </div>

    <h3>下一步行动建议</h3>
    <table>
      <tr><th>优先级</th><th>行动项</th><th>建议时间</th></tr>
      <tr><td>P0</td><td>完成详细需求调研与目标用户访谈（10+鸿蒙用户）</td><td>第1-2周</td></tr>
      <tr><td>P0</td><td>深度体验3-5款竞品（含Android/iOS同类），输出竞品分析文档</td><td>第1-2周</td></tr>
      <tr><td>P0</td><td>注册华为开发者账号，开通AppGallery Connect</td><td>第1周</td></tr>
      <tr><td>P1</td><td>设计MVP功能范围，评估是否同步推出元服务版本</td><td>第2-3周</td></tr>
      <tr><td>P1</td><td>评估团队ArkTS能力，规划培训或招聘时间线</td><td>第2-3周</td></tr>
      <tr><td>P1</td><td>查阅华为开发者激励计划细则，对齐产品规划</td><td>第3周</td></tr>
      <tr><td>P2</td><td>搭建DevEco Studio环境，启动MVP开发（4-8周）</td><td>第4-12周</td></tr>
      <tr><td>P2</td><td>种子用户招募与灰度测试（AppGallery封闭测试）</td><td>第12-14周</td></tr>
    </table>

    <h3>💡 差异化建议</h3>
    <ul>
      <li>🎯 <strong>优先开发元服务版本</strong>：免安装+桌面卡片=极低获客成本，适合冷启动验证</li>
      <li>🔗 <strong>利用鸿蒙分布式能力</strong>：如果产品涉及多设备场景（如健康数据跨设备同步），这是iOS/Android无法做到的差异化体验</li>
      <li>💰 <strong>对齐华为激励计划</strong>：在立项阶段就确保产品方向符合激励要求，最高可获600万奖金</li>
      <li>📱 <strong>预留跨平台架构</strong>：虽然聚焦鸿蒙，但建议采用分层架构，为未来Android/iOS扩展留接口</li>
    </ul>
  </div>

  <!-- Footer -->
  <div class="footer">
    <p>🦋 本报告由 AI 辅助生成 · 数据来源：公开信息搜索 · 仅供参考，不构成投资建议</p>
    <p>报告生成时间：{now} | 鸿蒙开发决策助手</p>
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

    parser = argparse.ArgumentParser(description="鸿蒙原生应用可行性决策报告生成器")
    parser.add_argument("--name", required=True, help="产品名称")
    parser.add_argument("--direction", required=True, help="产品方向")
    parser.add_argument("--output", required=True, help="输出HTML文件路径")
    parser.add_argument("--scores", default="{}", help="评分JSON")
    parser.add_argument("--ecosystem", default="{}", help="鸿蒙生态数据JSON")
    parser.add_argument("--competitors", default="{}", help="竞品数据JSON")
    parser.add_argument("--industry", default="{}", help="行业数据JSON")
    parser.add_argument("--user-profile", default="{}", help="用户画像数据JSON")
    parser.add_argument("--business-model", default="{}", help="商业模式数据JSON")
    parser.add_argument("--promotion", default="{}", help="推广策略数据JSON")
    parser.add_argument("--development", default="{}", help="开发指南数据JSON")
    parser.add_argument("--traffic", default="{}", help="分发流量数据JSON")
    parser.add_argument("--risks", default="{}", help="风险数据JSON")

    args = parser.parse_args()

    data = {
        "name": args.name,
        "direction": args.direction,
        "scores": json.loads(args.scores),
        "ecosystem": json.loads(args.ecosystem),
        "competitors": json.loads(args.competitors),
        "industry": json.loads(args.industry),
        "user_profile": json.loads(args.user_profile),
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

    print(f"✅ 鸿蒙开发决策报告已生成: {output_path}")


if __name__ == "__main__":
    main()
