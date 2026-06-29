"""
HTML 报告生成器 - 生成美观的数据分析报告
"""
import json
from config_manager import (
    tier_cn, rank_cn, queue_cn, get_region_name,
)
from riot_client import get_champion_name


def generate_profile_html(data: dict, region: str) -> str:
    """生成召唤师档案报告"""
    account = data["account"]
    summoner = data["summoner"]
    ranked_data = data.get("ranked", [])
    masteries = data.get("masteries", [])

    name = f"{account['gameName']}#{account['tagLine']}"
    region_name = get_region_name(region)

    ranked_rows = ""
    if ranked_data:
        for r in ranked_data:
            tier = tier_cn(r.get("tier", "?"))
            rank = rank_cn(r.get("rank", ""))
            queue = queue_cn(r.get("queueType", "?"))
            wins = r.get("wins", 0)
            losses = r.get("losses", 0)
            total = wins + losses
            wr = round(wins / total * 100, 1) if total > 0 else 0
            lp = r.get("leaguePoints", 0)
            ranked_rows += f"""
            <tr>
                <td>{queue}</td>
                <td><strong>{tier} {rank}</strong></td>
                <td>{lp} LP</td>
                <td>{wins}W / {losses}L</td>
                <td style="color: {'#e74c3c' if wr >= 50 else '#27ae60'}">{wr}%</td>
            </tr>"""
    else:
        ranked_rows = '<tr><td colspan="5" style="text-align:center;color:#888">暂无排位数据</td></tr>'

    mastery_rows = ""
    if masteries:
        for m in masteries[:10]:
            champ_name = get_champion_name(m.get("championId", 0))
            level = m.get("championLevel", 0)
            points = m.get("championPoints", 0)
            mastery_rows += f"""
            <tr>
                <td>{champ_name}</td>
                <td>{level} 级</td>
                <td>{points:,}</td>
            </tr>"""
    else:
        mastery_rows = '<tr><td colspan="3" style="text-align:center;color:#888">暂无英雄熟练度数据</td></tr>'

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} - 召唤师档案</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
    background: linear-gradient(135deg, #0a0a2e 0%, #1a1a4e 50%, #0d0d3d 100%);
    color: #e0e0e0;
    min-height: 100vh;
    padding: 20px;
}}
.container {{ max-width: 900px; margin: 0 auto; }}
.header {{
    text-align: center;
    padding: 40px 20px;
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
    margin-bottom: 24px;
    border: 1px solid rgba(255,255,255,0.1);
}}
.header h1 {{ font-size: 28px; color: #fff; margin-bottom: 8px; }}
.header .level {{ color: #c9a84c; font-size: 14px; }}
.header .region-tag {{
    display: inline-block;
    background: #c9a84c;
    color: #0a0a2e;
    padding: 2px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: bold;
    margin-top: 8px;
}}
.section {{
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.1);
}}
.section h2 {{
    font-size: 18px;
    color: #c9a84c;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}}
table {{
    width: 100%;
    border-collapse: collapse;
}}
th, td {{
    padding: 10px 12px;
    text-align: left;
    border-bottom: 1px solid rgba(255,255,255,0.08);
}}
th {{ color: #888; font-size: 12px; text-transform: uppercase; font-weight: 600; }}
td {{ font-size: 14px; }}
.footer {{
    text-align: center;
    color: #666;
    font-size: 12px;
    padding: 20px;
}}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>🏆 {name}</h1>
        <div class="level">召唤师等级 {summoner.get('summonerLevel', '?')}</div>
        <span class="region-tag">{region_name} ({region.upper()})</span>
    </div>

    <div class="section">
        <h2>📊 排位数据</h2>
        <table>
            <thead>
                <tr><th>队列</th><th>段位</th><th>胜点</th><th>战绩</th><th>胜率</th></tr>
            </thead>
            <tbody>{ranked_rows}</tbody>
        </table>
    </div>

    <div class="section">
        <h2>⭐ 英雄熟练度 Top 10</h2>
        <table>
            <thead>
                <tr><th>英雄</th><th>熟练度</th><th>点数</th></tr>
            </thead>
            <tbody>{mastery_rows}</tbody>
        </table>
    </div>

    <div class="footer">
        Powered by lol-analyst | Riot Games API | 数据可能有延迟
    </div>
</div>
</body>
</html>"""
    return html


def generate_match_history_html(name: str, region: str, matches: list,
                                  puuid: str) -> str:
    """生成对局历史报告"""
    region_name = get_region_name(region)

    match_rows = ""
    wins = 0
    total = len(matches)
    total_kills = 0
    total_deaths = 0
    total_assists = 0

    for m in matches:
        win = m.get("win", False)
        if win:
            wins += 1
        total_kills += m.get("kills", 0)
        total_deaths += m.get("deaths", 0)
        total_assists += m.get("assists", 0)

        win_bg = "rgba(46,204,113,0.15)" if win else "rgba(231,76,60,0.15)"
        win_text = "#2ecc71" if win else "#e74c3c"
        win_icon = "✅" if win else "❌"

        kda = m.get("kda", 0)
        kda_color = "#2ecc71" if kda >= 3 else "#f39c12" if kda >= 1.5 else "#e74c3c"

        match_rows += f"""
        <tr style="background: {win_bg}">
            <td style="color: {win_text}">{win_icon}</td>
            <td>{get_champion_name(m.get('champion_id', 0))}</td>
            <td style="color: {kda_color}; font-weight: bold">{kda}</td>
            <td>{m.get('kills', 0)}/{m.get('deaths', 0)}/{m.get('assists', 0)}</td>
            <td>{m.get('cs', 0)}</td>
            <td>{m.get('kill_participation', 0)}%</td>
            <td>{m.get('gold_earned', 0):,}</td>
            <td style="font-size: 12px; color: #888">{m.get('game_mode', '')}</td>
        </tr>"""

    # 汇总统计
    avg_kda = round((total_kills + total_assists) / max(total_deaths, 1), 2)
    win_rate = round(wins / total * 100, 1) if total > 0 else 0

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} - 对局历史</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
    background: linear-gradient(135deg, #0a0a2e 0%, #1a1a4e 50%, #0d0d3d 100%);
    color: #e0e0e0;
    min-height: 100vh;
    padding: 20px;
}}
.container {{ max-width: 1100px; margin: 0 auto; }}
.header {{
    text-align: center;
    padding: 30px 20px;
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.1);
}}
.header h1 {{ font-size: 24px; color: #fff; margin-bottom: 12px; }}
.stats-bar {{
    display: flex;
    justify-content: center;
    gap: 32px;
    flex-wrap: wrap;
}}
.stat-item {{ text-align: center; }}
.stat-value {{
    font-size: 24px;
    font-weight: bold;
    color: #c9a84c;
}}
.stat-label {{ font-size: 12px; color: #888; margin-top: 4px; }}
.section {{
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    overflow-x: auto;
}}
.section h2 {{
    font-size: 16px;
    color: #c9a84c;
    margin-bottom: 14px;
}}
table {{
    width: 100%;
    border-collapse: collapse;
    min-width: 700px;
}}
th, td {{
    padding: 8px 10px;
    text-align: left;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    font-size: 13px;
}}
th {{ color: #888; font-size: 11px; text-transform: uppercase; }}
.footer {{
    text-align: center;
    color: #666;
    font-size: 12px;
    padding: 20px;
}}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>📜 {name} 的对局历史</h1>
        <div class="stats-bar">
            <div class="stat-item">
                <div class="stat-value">{total}</div>
                <div class="stat-label">对局数</div>
            </div>
            <div class="stat-item">
                <div class="stat-value" style="color: {'#2ecc71' if win_rate >= 50 else '#e74c3c'}">{win_rate}%</div>
                <div class="stat-label">胜率 ({wins}W/{total-wins}L)</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{avg_kda}</div>
                <div class="stat-label">场均 KDA</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{get_region_name(region)}</div>
                <div class="stat-label">区域</div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>🎮 对局详情</h2>
        <table>
            <thead>
                <tr><th>结果</th><th>英雄</th><th>KDA</th><th>K/D/A</th><th>补刀</th><th>参团</th><th>经济</th><th>模式</th></tr>
            </thead>
            <tbody>{match_rows}</tbody>
        </table>
    </div>

    <div class="footer">
        Powered by lol-analyst | Riot Games API | 数据可能有延迟
    </div>
</div>
</body>
</html>"""
    return html


def generate_analysis_html(name: str, region: str, profile: dict,
                             matches: list, masteries: list,
                             summoner_level: int = 0) -> str:
    """生成综合分析报告（含AI解读区）"""
    # 基础统计
    total = len(matches)
    if total == 0:
        wins = win_rate = avg_kda = 0
        champ_stats = {}
    else:
        wins = sum(1 for m in matches if m.get("win"))
        win_rate = round(wins / total * 100, 1)
        total_k = sum(m.get("kills", 0) for m in matches)
        total_d = sum(m.get("deaths", 0) for m in matches)
        total_a = sum(m.get("assists", 0) for m in matches)
        avg_kda = round((total_k + total_a) / max(total_d, 1), 2)

        # 按英雄分组统计
        champ_stats = {}
        for m in matches:
            cid = m.get("champion_id", 0)
            if cid not in champ_stats:
                champ_stats[cid] = {"games": 0, "wins": 0, "kills": 0, "deaths": 0, "assists": 0}
            champ_stats[cid]["games"] += 1
            if m.get("win"):
                champ_stats[cid]["wins"] += 1
            champ_stats[cid]["kills"] += m.get("kills", 0)
            champ_stats[cid]["deaths"] += m.get("deaths", 0)
            champ_stats[cid]["assists"] += m.get("assists", 0)

    # 英雄表现排行
    champ_rows = ""
    sorted_champs = sorted(champ_stats.items(), key=lambda x: x[1]["games"], reverse=True)
    for cid, stats in sorted_champs[:10]:
        g = stats["games"]
        cwr = round(stats["wins"] / g * 100, 1) if g > 0 else 0
        ckda = round(
            (stats["kills"] + stats["assists"]) / max(stats["deaths"], 1), 2
        )
        champ_rows += f"""
        <tr>
            <td>{get_champion_name(cid)}</td>
            <td>{g}</td>
            <td style="color: {'#2ecc71' if cwr >= 50 else '#e74c3c'}">{cwr}%</td>
            <td>{ckda}</td>
        </tr>"""

    if not champ_rows:
        champ_rows = '<tr><td colspan="4" style="text-align:center;color:#888">暂无对局数据</td></tr>'

    # 输出HTML
    region_name = get_region_name(region)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{name} - 综合分析报告</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif;
    background: linear-gradient(135deg, #0a0a2e 0%, #1a1a4e 50%, #0d0d3d 100%);
    color: #e0e0e0;
    min-height: 100vh;
    padding: 20px;
}}
.container {{ max-width: 900px; margin: 0 auto; }}
.header {{
    text-align: center;
    padding: 40px 20px;
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
    margin-bottom: 24px;
    border: 1px solid rgba(255,255,255,0.1);
}}
.header h1 {{ font-size: 28px; color: #fff; margin-bottom: 12px; }}
.stats-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 16px;
    margin-top: 20px;
}}
.stat-card {{
    background: rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
}}
.stat-card .value {{
    font-size: 28px;
    font-weight: bold;
    color: #c9a84c;
}}
.stat-card .label {{ font-size: 12px; color: #888; margin-top: 4px; }}
.section {{
    background: rgba(255,255,255,0.05);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.1);
}}
.section h2 {{
    font-size: 18px;
    color: #c9a84c;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
}}
table {{ width: 100%; border-collapse: collapse; }}
th, td {{
    padding: 10px 12px;
    text-align: left;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    font-size: 14px;
}}
th {{ color: #888; font-size: 12px; text-transform: uppercase; }}
.insight-box {{
    background: rgba(201,168,76,0.1);
    border-left: 3px solid #c9a84c;
    border-radius: 8px;
    padding: 16px 20px;
    margin-top: 16px;
}}
.insight-box h3 {{ color: #c9a84c; font-size: 14px; margin-bottom: 8px; }}
.insight-box p {{ font-size: 14px; line-height: 1.8; color: #ccc; }}
.footer {{
    text-align: center;
    color: #666;
    font-size: 12px;
    padding: 20px;
}}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>📊 {name} 综合分析报告</h1>
        <p style="color: #888; font-size: 14px;">{region_name} | 最近 {total} 场对局</p>
        <div class="stats-grid">
            <div class="stat-card">
                <div class="value" style="color: {'#2ecc71' if win_rate >= 50 else '#e74c3c'}">{win_rate}%</div>
                <div class="label">胜率 ({wins}W/{total-wins}L)</div>
            </div>
            <div class="stat-card">
                <div class="value">{avg_kda}</div>
                <div class="label">场均 KDA</div>
            </div>
            <div class="stat-card">
                <div class="value">{len(champ_stats)}</div>
                <div class="label">使用英雄数</div>
            </div>
            <div class="stat-card">
                <div class="value">{summoner_level}</div>
                <div class="label">召唤师等级</div>
            </div>
        </div>
    </div>

    <div class="section">
        <h2>🎮 英雄表现排行</h2>
        <table>
            <thead><tr><th>英雄</th><th>场次</th><th>胜率</th><th>KDA</th></tr></thead>
            <tbody>{champ_rows}</tbody>
        </table>
    </div>

    <div class="section">
        <h2>💡 AI 洞察（待 LLM 解读）</h2>
        <div class="insight-box">
            <h3>📋 数据摘要</h3>
            <p>
                共 {total} 场对局，胜率 {win_rate}%，场均KDA {avg_kda}。使用了 {len(champ_stats)} 个不同英雄。
            </p>
        </div>
        <div class="insight-box">
            <h3>⚠️ 待优化点</h3>
            <p>
                <em>此处应由大语言模型基于数据生成个性化分析和上分建议。请在 WorkBuddy 中调用 lol-analyst Skill 以获取 AI 解读。</em>
            </p>
        </div>
    </div>

    <div class="footer">
        Powered by lol-analyst | Riot Games API | 数据可能有延迟
    </div>
</div>
</body>
</html>"""
    return html


HTML_TEMPLATES = {
    "profile": generate_profile_html,
    "matches": generate_match_history_html,
    "analysis": generate_analysis_html,
}
