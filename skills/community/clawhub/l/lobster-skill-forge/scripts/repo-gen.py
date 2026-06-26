#!/usr/bin/env python3
"""
Skill Repo - 技能仓库生成器
生成技能仓库的HTML索引页，便于管理和发布
"""

import os, json, datetime

BASE = "/root/.openclaw/workspace/skills"

# 自研融合技能（要发布到ClawHub）
SELF_SKILLS = {
    "biz-doc-pro": {
        "name": "BizDoc Pro 商务文档三件套",
        "emoji": "📄",
        "color": "#4A90D9",
        "sources": "proposal + contract + invoice",
        "cat": "企业办公",
        "desc": "方案书+发票+合同一条龙生成",
        "status": "✅ 已完成"
    },
    "travel-biz": {
        "name": "TravelBiz 差旅报销助手",
        "emoji": "✈️",
        "color": "#50C878",
        "sources": "travel + expense + receipt + invoice",
        "cat": "企业办公",
        "desc": "出差规划→费用记录→报销单生成",
        "status": "✅ v1.0"
    },
    "proj-sync": {
        "name": "ProjSync 项目管理同步器",
        "emoji": "📋",
        "color": "#FF6B6B",
        "sources": "taskr + project + calendar",
        "cat": "企业办公",
        "desc": "项目+任务+日程一站式管理",
        "status": "✅ v1.0"
    },
    "video-craft-pro": {
        "name": "VideoCraft Pro 视频创作工坊",
        "emoji": "🎬",
        "color": "#9B59B6",
        "sources": "video-script + TTS + subtitle",
        "cat": "内容创作",
        "desc": "脚本+配音+字幕+合成全自动",
        "status": "✅ 已完成"
    },
    "content-pilot": {
        "name": "ContentPilot 内容运营全能手",
        "emoji": "📢",
        "color": "#E67E22",
        "sources": "caption + hashtag + quote + newsletter",
        "cat": "内容创作",
        "desc": "社媒文案+公众号长文+内容矩阵",
        "status": "✅ v2.0 含卡兹克写作风格"
    },
    "video-monetizer": {
        "name": "Video Monetizer 视频号变现助手",
        "emoji": "💰",
        "color": "#F1C40F",
        "sources": "热点 + 脚本 + 话术 + 发布",
        "cat": "电商变现",
        "desc": "热点追踪→脚本生成→变现话术→发布",
        "status": "✅ v2.0 含龙虾辩论模式"
    },
    "ecom-intel": {
        "name": "EcomIntel 电商情报站",
        "emoji": "🛒",
        "color": "#E74C3C",
        "sources": "competitor + review + price",
        "cat": "电商变现",
        "desc": "竞品分析+评论分析+价格监控",
        "status": "✅ v2.0 含横纵深度分析"
    },
    "one-man-conglomerate": {
        "name": "一人财团 Agent群聊协作",
        "emoji": "🏢",
        "color": "#2C3E50",
        "sources": "orchestration + swarm + debate",
        "cat": "决策协作",
        "desc": "多Agent群聊协作+辩论+COO协调",
        "status": "✅ v2.0 含洁癖整理"
    },
    "life-pal": {
        "name": "LifePal 生活管家",
        "emoji": "🌿",
        "color": "#27AE60",
        "sources": "recipe + workout + meditation + gift",
        "cat": "生活健康",
        "desc": "菜谱计划+健身方案+冥想引导+送礼",
        "status": "✅ v1.0"
    },
    "skill-forge": {
        "name": "SkillForge 技能熔炉生产线",
        "emoji": "🔨",
        "color": "#8E44AD",
        "sources": "skill-factory + workflows + swarm",
        "cat": "基础设施",
        "desc": "需求→融合方案→自动生成技能→Agent部署",
        "status": "✅ v1.0 超自动化"
    }
}

def generate_html():
    """生成技能仓库HTML"""
    now = datetime.datetime.now()
    
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🦞 智美人 · 技能仓库</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, 'Segoe UI', Roboto, sans-serif; background: #0f0f1a; color: #e0e0e0; min-height: 100vh; }}
.container {{ max-width: 1200px; margin: 0 auto; padding: 40px 20px; }}

/* Header */
.header {{ text-align: center; margin-bottom: 50px; }}
.header h1 {{ font-size: 42px; background: linear-gradient(135deg, #FF6B6B, #F1C40F, #4A90D9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; }}
.header p {{ color: #888; font-size: 16px; }}
.header .stats {{ display: flex; justify-content: center; gap: 30px; margin-top: 20px; }}
.header .stat {{ text-align: center; }}
.header .stat-num {{ font-size: 28px; font-weight: bold; color: #F1C40F; }}
.header .stat-label {{ font-size: 12px; color: #666; }}

/* Category */
.category {{ margin-bottom: 40px; }}
.category h2 {{ font-size: 22px; color: #ccc; margin-bottom: 16px; padding-left: 8px; border-left: 3px solid #F1C40F; }}

/* Grid */
.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 16px; }}

/* Card */
.card {{ background: linear-gradient(135deg, #1a1a2e, #16213e); border-radius: 12px; padding: 20px; border: 1px solid #2a2a4a; transition: all 0.3s; position: relative; overflow: hidden; }}
.card:hover {{ transform: translateY(-3px); border-color: #4a4a6a; box-shadow: 0 8px 25px rgba(0,0,0,0.4); }}
.card .header-top {{ display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }}
.card .emoji {{ font-size: 28px; }}
.card .badge {{ font-size: 10px; padding: 2px 8px; border-radius: 10px; font-weight: bold; }}
.card h3 {{ font-size: 16px; font-weight: 600; }}
.card .desc {{ font-size: 13px; color: #999; margin: 8px 0; line-height: 1.5; }}
.card .sources {{ font-size: 11px; color: #666; margin: 6px 0; }}
.card .sources span {{ background: #252540; padding: 2px 6px; border-radius: 4px; margin: 2px; display: inline-block; }}
.card .status {{ margin-top: 12px; padding: 4px 10px; font-size: 11px; border-radius: 6px; display: inline-block; }}
.card .actions {{ margin-top: 12px; display: flex; gap: 8px; }}
.card .actions a {{ padding: 5px 12px; border-radius: 6px; font-size: 12px; text-decoration: none; }}
.card .btn-view {{ background: #252540; color: #e0e0e0; }}
.card .btn-publish {{ background: #F1C40F; color: #000; font-weight: 600; }}

/* Categories */
.cat-企业办公 {{ border-left: 3px solid #4A90D9; }}
.cat-内容创作 {{ border-left: 3px solid #9B59B6; }}
.cat-电商变现 {{ border-left: 3px solid #F1C40F; }}
.cat-决策协作 {{ border-left: 3px solid #2C3E50; border-right: 3px solid #2C3E50; }}
.cat-生活健康 {{ border-left: 3px solid #27AE60; }}
.cat-基础设施 {{ border-left: 3px solid #8E44AD; }}

/* Timeline */
.timeline {{ margin: 40px 0; background: #1a1a2e; border-radius: 12px; padding: 24px; border: 1px solid #2a2a4a; }}
.timeline h2 {{ margin-bottom: 16px; }}
.timeline-items {{ display: flex; flex-direction: column; gap: 10px; }}
.timeline-item {{ display: flex; gap: 12px; align-items: center; font-size: 13px; }}
.timeline-time {{ color: #666; min-width: 80px; }}
.timeline-dot {{ width: 8px; height: 8px; border-radius: 50%; background: #F1C40F; }}
.timeline-text {{ color: #ccc; }}

/* Footer */
.footer {{ text-align: center; padding: 30px; color: #555; font-size: 13px; border-top: 1px solid #222; margin-top: 40px; }}
</style>
</head>
<body>
<div class="container">

<div class="header">
    <h1>🦞 智美人 · 技能仓库</h1>
    <p>一个人就是一个公司 · 融合技能全览</p>
    <div class="stats">
        <div class="stat"><div class="stat-num">10</div><div class="stat-label">自研技能</div></div>
        <div class="stat"><div class="stat-num">3</div><div class="stat-label">开源技能</div></div>
        <div class="stat"><div class="stat-num">163</div><div class="stat-label">总技能</div></div>
        <div class="stat"><div class="stat-num">6</div><div class="stat-label">品类</div></div>
    </div>
</div>
"""

    # 按品类分组
    categories = {}
    for slug, info in SELF_SKILLS.items():
        cat = info["cat"]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((slug, info))
    
    # 排序
    cat_order = ["企业办公", "内容创作", "电商变现", "决策协作", "生活健康", "基础设施"]
    
    for cat in cat_order:
        if cat not in categories:
            continue
        items = categories[cat]
        html += f'<div class="category">\n<h2>{cat}</h2>\n<div class="grid">\n'
        
        for slug, info in items:
            card_class = f"cat-{cat}"
            html += f'''
<div class="card {card_class}">
    <div class="header-top">
        <span class="emoji">{info['emoji']}</span>
        <h3>{info['name']}</h3>
    </div>
    <div class="desc">{info['desc']}</div>
    <div class="sources">
        {" ".join(f'<span>{s.strip()}</span>' for s in info['sources'].split('+'))}
    </div>
    <div class="status" style="background: {info['color']}20; color: {info['color']}; border: 1px solid {info['color']}40;">
        {info['status']}
    </div>
    <div class="actions">
        <a class="btn-view" href="#">📖 查看</a>
        <a class="btn-publish" href="#">🚀 发布到ClawHub</a>
    </div>
</div>
'''
        html += '</div></div>\n'
    
    # 时间线
    html += f'''
<div class="timeline">
    <h2>📅 开发时间线</h2>
    <div class="timeline-items">
        <div class="timeline-item">
            <span class="timeline-time">04-26</span>
            <span class="timeline-dot"></span>
            <span class="timeline-text">BizDoc Pro · VideoCraft Pro · EcomIntel · Video Monetizer</span>
        </div>
        <div class="timeline-item">
            <span class="timeline-time">04-28</span>
            <span class="timeline-dot"></span>
            <span class="timeline-text">安装138技能 · 技能库大扩容</span>
        </div>
        <div class="timeline-item">
            <span class="timeline-time">04-29</span>
            <span class="timeline-dot"></span>
            <span class="timeline-text">融合Kimi Claw → 一人财团 · 卡兹克3技能融合</span>
        </div>
        <div class="timeline-item">
            <span class="timeline-time">04-30</span>
            <span class="timeline-dot" style="background: #FF6B6B;"></span>
            <span class="timeline-text" style="color: #FF6B6B; font-weight: 600;">
                TravelBiz · ContentPilot · LifePal · ProjSync · SkillForge
            </span>
        </div>
        <div class="timeline-item">
            <span class="timeline-time">待发布</span>
            <span class="timeline-dot" style="background: #888;"></span>
            <span class="timeline-text" style="color: #888;">GitHub开发者注册 → ClawHub发布10技能</span>
        </div>
    </div>
</div>
'''

    html += f'''
<div class="footer">
    🦞 智美人 · 技能仓库 · 生成于 {now.strftime('%Y-%m-%d %H:%M')}
</div>

</div>
</body>
</html>
'''
    return html


def main():
    out_dir = os.path.join(BASE, "..", "docs")
    os.makedirs(out_dir, exist_ok=True)
    
    html = generate_html()
    path = os.path.join(out_dir, "skill-repo.html")
    with open(path, "w") as f:
        f.write(html)
    
    print(f"✅ 技能仓库已生成: {path}")
    print(f"   {len(SELF_SKILLS)} 个自研技能")
    print(f"   {os.path.getsize(path)} bytes")
    
    # 也存一份到技能目录
    path2 = os.path.join(BASE, "..", "skills", "skill-repo.html")
    with open(path2, "w") as f:
        f.write(html)
    print(f"   Mirror: {path2}")

if __name__ == "__main__":
    main()
