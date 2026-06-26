#!/usr/bin/env python3
"""
新闻爬取智能体 - H5 页面生成器 V2.0
支持5大分类 + 分析研判板块 + 评分系统
"""

from datetime import datetime

# 媒体权威性评分
MEDIA_AUTHORITY = {
    # 权威媒体 (35分)
    "新华社": 35, "人民日报": 35, "财新": 35, "证券时报": 35, "中国证券报": 35, "上海证券报": 35,
    "证监会": 35, "发改委": 35, "工信部": 35, "科技部": 35,
    # 头部财经/科技媒体 (30分)
    "36氪": 30, "钛媒体": 30, "虎嗅": 30, "界面": 30, "第一财经": 30, "经济观察报": 30,
    "21世纪经济报道": 30, "证券日报": 30, "每日经济新闻": 30,
    # 行业垂直媒体 (25分)
    "IT之家": 25, "cnBeta": 25, "驱动之家": 25, "爱范儿": 25, "少数派": 25, "量子位": 25,
    "新智元": 25, "机器之心": 25, "AI之家": 25, "开源中国": 25, "思否": 25,
    "鸿蒙开发者社区": 25, "华为开发者联盟": 25,
    # 地方媒体/门户 (20分)
    "新浪": 20, "搜狐": 20, "网易": 20, "腾讯": 20, "凤凰网": 20, "今日头条": 20,
    "百家号": 20, "东方财富网": 20, "新浪财经": 20, "新浪科技": 20, "网易科技": 20,
    "环球网": 20, "中证网": 20, "金融时报": 20,
    # 自媒体/公众号 (15分)
    "微信公众号": 15, "知乎": 15, "雪球": 15, "微博": 15, "小红书": 15, "脉脉": 15,
}

# 行业影响力评分
def calc_impact_score(title: str, summary: str) -> int:
    text = (title + " " + summary).lower()
    # 全局性影响 (30分)
    global_keywords = ["发布", "发布", "国家", "政策", "标准", "战略", "巨头", "GPT", "OpenAI", "英伟达", "华为", "鸿蒙", "Meta", "谷歌", "苹果"]
    # 局部性影响 (20分)
    local_keywords = ["融资", "产品", "上线", "更新", "版本", "合作", "签约", "中标", "芯片", "模型"]
    # 个体性影响 (10分)
    individual_keywords = ["公司", "企业"]
    
    for kw in global_keywords:
        if kw.lower() in text:
            return 30
    for kw in local_keywords:
        if kw.lower() in text:
            return 20
    return 10

# 传播量评分 (根据来源预估)
def calc_spread_score(source: str) -> int:
    high_spread = ["36氪", "虎嗅", "钛媒体", "新浪", "腾讯", "今日头条", "微博", "网易", "搜狐"]
    medium_spread = ["IT之家", "东方财富网", "雪球", "凤凰网", "AI之家", "开源中国"]
    
    if source in high_spread:
        return 20
    elif source in medium_spread:
        return 12
    return 5

# 内容新颖性评分
def calc_novelty_score(title: str, summary: str) -> int:
    text = (title + " " + summary).lower()
    # 重大突破 (15分)
    breakthrough = ["首发", "首款", "首次", "突破", "革命", "全新", "重磅", "发布", "诞生", "里程碑"]
    # 常规更新 (8分)
    regular = ["上线", "更新", "升级", "推出", "发布", "推出"]
    # 重复信息 (3分)
    
    for kw in breakthrough:
        if kw in text:
            return 15
    for kw in regular:
        if kw in text:
            return 8
    return 3

def calculate_news_score(news: dict) -> int:
    """计算单条新闻的综合评分"""
    # 媒体权威性 (35%)
    source = news.get("source", "")
    media_score = MEDIA_AUTHORITY.get(source, 15)
    
    # 行业影响力 (30%)
    title = news.get("title", "")
    summary = news.get("summary", "")
    impact_score = calc_impact_score(title, summary)
    
    # 传播量 (20%)
    spread_score = calc_spread_score(source)
    
    # 内容新颖性 (15%)
    novelty_score = calc_novelty_score(title, summary)
    
    # 综合评分
    total = media_score * 0.35 + impact_score * 0.30 + spread_score * 0.20 + novelty_score * 0.15
    return int(total)

def get_score_color(score: int) -> str:
    """根据分数返回颜色"""
    if score >= 80:
        return "#10b981"  # 绿色 - 高质量
    elif score >= 70:
        return "#3b82f6"  # 蓝色 - 良好
    elif score >= 60:
        return "#f59e0b"  # 黄色 - 及格
    else:
        return "#ef4444"  # 红色 - 不及格

def generate_news_html(news_data: dict) -> str:
    categories = {
        "彩讯股份": {"icon": "🏢", "color": "#ec4899"},
        "AI": {"icon": "🤖", "color": "#6366f1"},
        "算力": {"icon": "💻", "color": "#10b981"},
        "协同办公": {"icon": "📊", "color": "#f59e0b"},
        "鸿蒙": {"icon": "📱", "color": "#ef4444"}
    }
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>科技新闻速递 - {datetime.now().strftime("%Y年%m月%d日")}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%); min-height: 100vh; color: #fff; }}
        .header {{ background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); padding: 25px 20px; text-align: center; }}
        .header h1 {{ font-size: 24px; margin-bottom: 8px; }}
        .header p {{ opacity: 0.9; font-size: 13px; }}
        .tabs {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; padding: 15px; background: rgba(255,255,255,0.05); }}
        .tab {{ padding: 8px 16px; border: none; border-radius: 20px; cursor: pointer; font-size: 13px; background: rgba(255,255,255,0.1); color: #fff; }}
        .tab.active {{ background: linear-gradient(135deg, #667eea, #764ba2); }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 15px; }}
        .category-section {{ display: none; }}
        .category-section.active {{ display: block; }}
        .stock-info {{ background: rgba(255,255,255,0.08); border-radius: 12px; padding: 15px; margin-bottom: 15px; display: flex; align-items: center; gap: 15px; flex-wrap: wrap; }}
        .stock-price {{ font-size: 22px; font-weight: bold; color: #10b981; }}
        .score-badge {{ display: inline-block; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: bold; margin-left: 8px; }}
        .news-card {{ background: rgba(255,255,255,0.08); border-radius: 12px; padding: 15px; margin-bottom: 12px; border-left: 4px solid; }}
        .news-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }}
        .news-title {{ font-size: 15px; font-weight: 600; flex: 1; }}
        .news-title a {{ color: inherit; text-decoration: none; }}
        .news-meta {{ font-size: 12px; opacity: 0.7; margin-bottom: 8px; }}
        .news-summary {{ font-size: 13px; margin: 10px 0; padding: 10px; background: rgba(255,255,255,0.05); border-radius: 8px; line-height: 1.6; }}
        .news-link {{ font-size: 11px; color: #667eea; word-break: break-all; }}
        .announcement-card {{ background: rgba(255,255,255,0.08); border-radius: 10px; padding: 12px; margin-bottom: 10px; }}
        .announcement-card h4 {{ font-size: 14px; color: #f59e0b; margin-bottom: 6px; }}
        .announcement-card h4 a {{ color: inherit; text-decoration: none; }}
        .announcement-date {{ font-size: 11px; opacity: 0.6; }}
        .analysis-section {{ background: rgba(255,255,255,0.08); border-radius: 16px; padding: 20px; margin-top: 20px; }}
        .analysis-section h2 {{ font-size: 18px; margin-bottom: 15px; }}
        .analysis-section h3 {{ font-size: 15px; margin: 15px 0 10px; }}
        .analysis-section p {{ font-size: 14px; line-height: 1.8; opacity: 0.9; }}
        .analysis-section ul {{ padding-left: 20px; font-size: 13px; line-height: 1.8; opacity: 0.9; }}
        .caixun-section {{ background: linear-gradient(135deg, rgba(255,107,107,0.1) 0%, rgba(255,142,83,0.1) 100%); border-radius: 16px; padding: 20px; margin-top: 20px; border: 1px solid rgba(255,107,107,0.3); }}
        .footer {{ text-align: center; padding: 20px; opacity: 0.6; font-size: 12px; }}
        @media (max-width: 600px) {{ .header h1 {{ font-size: 20px; }} .tabs {{ gap: 5px; }} .tab {{ padding: 6px 12px; font-size: 12px; }} }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📰 科技新闻速递</h1>
        <p>{datetime.now().strftime("%Y年%m月%d日 %H:%M")} | 时间范围: 昨日8:00-今日8:00 | 评分阈值: 60分</p>
    </div>
    <div class="tabs">
        <button class="tab active" onclick="showTab('all')">全部</button>
'''
    
    for cat_id, cat_info in categories.items():
        html += f'<button class="tab" onclick="showTab(\'{cat_id}\')">{cat_info["icon"]} {cat_id}</button>'
    
    html += '</div><div class="container">'
    
    for cat_id, cat_info in categories.items():
        news_list = news_data.get(cat_id, [])
        if not news_list:
            continue
        
        html += f'<div class="category-section active" id="{cat_id}">'
        
        if cat_id == "彩讯股份" and news_data.get("stock"):
            stock = news_data["stock"]
            html += f'''<div class="stock-info">
            <span style="font-size:16px;">📈 彩讯股份(300634)</span>
            <span class="stock-price">{stock.get('price', '')}</span>
            <span style="font-size:14px;">{stock.get('change', '')}</span>
            <span style="font-size:13px;opacity:0.8;">📊 创业板:{stock.get('chinese_stock', '')} ({stock.get('chinese_change', '')})</span>
        </div>'''
        
        for i, news in enumerate(news_list[:10], 1):
            title = news.get("title", "")
            url = news.get("url", "#")
            source = news.get("source", "")
            time_ago = news.get("time_ago", "")
            score = news.get("score", 0)
            score_color = get_score_color(score)
            
            if cat_id == "彩讯股份" and news.get("type"):
                ann_type = news.get("type", "公告")
                ann_date = news.get("date", "")
                html += f'''<div class="announcement-card">
                    <h4><a href="{url}" target="_blank">{ann_type}: {title}</a></h4>
                    <div class="announcement-date">{ann_date}</div>
                </div>'''
            else:
                html += f'''<div class="news-card" style="border-left-color:{cat_info['color']}">
                    <div class="news-header">
                        <div class="news-title"><span style="opacity:0.5;margin-right:5px;">{i}</span><a href="{url}" target="_blank">{title}</a></div>
                        <span class="score-badge" style="background:{score_color};color:#fff;">{score}分</span>
                    </div>
                    <div class="news-meta">📮 {source} 🕐 {time_ago}</div>
                    <div class="news-summary">{news.get("summary", "")}</div>
                    <div class="news-link"><a href="{url}" target="_blank">{url}</a></div>
                </div>'''
        
        html += '</div>'
    
    # 分析研判板块
    analysis = news_data.get("analysis", {})
    if analysis:
        html += '<div class="container">'
        
        if analysis.get("ai"):
            html += f'''<div class="analysis-section">
                <h2>🤖 AI行业分析</h2>
                <p>{analysis["ai"]}</p>
            </div>'''
        
        if analysis.get("hongmeng"):
            html += f'''<div class="analysis-section">
                <h2>📱 鸿蒙行业分析</h2>
                <p>{analysis["hongmeng"]}</p>
            </div>'''
        
        caixun = analysis.get("caixun", {})
        if caixun:
            html += '''<div class="caixun-section">
                <h2>🏢 彩讯股份(300634)分析研判</h2>'''
            
            if caixun.get("opportunities"):
                html += '<h3>🎯 机遇</h3><ul>'
                for item in caixun.get("opportunities", []):
                    html += f'<li>{item}</li>'
                html += '</ul>'
            
            if caixun.get("risks"):
                html += '<h3>⚠️ 风险</h3><ul>'
                for item in caixun.get("risks", []):
                    html += f'<li>{item}</li>'
                html += '</ul>'
            
            if caixun.get("recommendations"):
                html += '<h3>💼 投资建议</h3><ul>'
                for item in caixun.get("recommendations", []):
                    html += f'<li>{item}</li>'
                html += '</ul>'
            
            html += '</div>'
        
        html += '</div>'
    
    html += '''<div class="footer"><p>由 OpenClaw 新闻智能体 V2.0 生成 | 评分系统已启用</p></div>
    <script>
        function showTab(category) {
            document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
            document.querySelectorAll(".category-section").forEach(s => s.classList.remove("active"));
            if (category === "all") {
                document.querySelectorAll(".category-section").forEach(s => s.classList.add("active"));
                document.querySelector(".tab").classList.add("active");
            } else {
                document.getElementById(category).classList.add("active");
                event.target.classList.add("active");
            }
        }
    </script></body></html>'''
    
    return html


def save_html(html: str, filename: str = "news_report.html") -> str:
    filepath = f"/workspace/news-agent/{filename}"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return filepath


if __name__ == "__main__":
    test_data = {
        "彩讯股份": [
            {"title": "募投项目收益情况", "type": "董秘回复", "date": "2026-03-09", "url": "https://www.sohu.com/a/994404645_122121789"}
        ],
        "AI": [
            {"title": "OpenClaw支持GPT-5.4", "url": "https://www.aibase.com/zh/news/26036", "source": "AI之家", "time_ago": "3月10日", "summary": "OpenClaw宣布支持GPT-5.4"},
            {"title": "腾讯发布WorkBuddy", "url": "https://www.aibase.com/zh/news/26048", "source": "AI之家", "time_ago": "3月9日", "summary": "腾讯发布AI办公助手"}
        ],
        "算力": [],
        "协同办公": [],
        "鸿蒙": [
            {"title": "鸿蒙智选春季发布会", "url": "https://www.ithome.com/0/926/906.htm", "source": "IT之家", "time_ago": "3月10日", "summary": "华为举办春季发布会"}
        ],
        "stock": {"price": "26.99元", "change": "+3.02%", "chinese_stock": "3208.58", "chinese_change": "-0.64%"},
        "analysis": {
            "ai": "AI分析测试",
            "hongmeng": "鸿蒙分析测试",
            "caixun": {"opportunities": ["测试"], "risks": ["测试"], "recommendations": ["测试"]}
        }
    }
    
    # 计算分数
    for cat in ["AI", "彩讯股份", "算力", "协同办公", "鸿蒙"]:
        if cat in test_data:
            for news in test_data[cat]:
                news["score"] = calculate_news_score(news)
    
    # 过滤60分以下
    for cat in ["AI", "彩讯股份", "算力", "协同办公", "鸿蒙"]:
        if cat in test_data:
            test_data[cat] = [n for n in test_data[cat] if n.get("score", 0) >= 60]
    
    html = generate_news_html(test_data)
    path = save_html(html)
    print(f"已生成: {path}")
