"""
报告生成模块 — 生成 NBA 数据分析 HTML 报告
"""

import os
from datetime import datetime
from .nba_client import NBAClient
from .i18n import I18N

client = NBAClient()
i18n = I18N()

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..')


def _html_page(title: str, body: str, extra_head: str = '') -> str:
    """生成完整 HTML 页面"""
    return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: -apple-system, "Microsoft YaHei", sans-serif; background: #0a0e27; color: #e0e6ed; padding: 20px; line-height:1.6; }}
.container {{ max-width: 960px; margin: 0 auto; }}
.header {{ background: linear-gradient(135deg, #1a1f3a, #2d1b4e); border-radius: 16px; padding: 30px; text-align: center; margin-bottom: 24px; border: 1px solid rgba(255,255,255,0.08); }}
.header h1 {{ font-size: 28px; color: #fff; margin-bottom: 8px; }}
.header .sub {{ color: #94a3b8; font-size: 14px; }}
.card {{ background: rgba(26,31,58,0.8); border-radius: 12px; padding: 20px; margin-bottom: 16px; border: 1px solid rgba(255,255,255,0.06); backdrop-filter: blur(10px); }}
.card h2 {{ font-size: 18px; color: #e2e8f0; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 2px solid rgba(99,102,241,0.4); }}
table {{ width: 100%; border-collapse: collapse; }}
th {{ text-align: left; padding: 10px 8px; color: #94a3b8; font-size: 12px; text-transform: uppercase; border-bottom: 1px solid rgba(255,255,255,0.08); }}
td {{ padding: 10px 8px; border-bottom: 1px solid rgba(255,255,255,0.04); font-size: 14px; }}
tr:hover {{ background: rgba(99,102,241,0.08); }}
.stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(150px,1fr)); gap: 12px; }}
.stat-box {{ background: rgba(99,102,241,0.1); border-radius: 10px; padding: 16px; text-align: center; border: 1px solid rgba(99,102,241,0.2); }}
.stat-box .value {{ font-size: 28px; font-weight: bold; color: #818cf8; }}
.stat-box .label {{ font-size: 12px; color: #94a3b8; margin-top: 4px; }}
.comparison {{ display: grid; grid-template-columns: 1fr 60px 1fr; gap: 0; align-items: center; margin: 20px 0; }}
.comp-col {{ background: rgba(26,31,58,0.8); border-radius: 12px; padding: 20px; }}
.comp-col h3 {{ text-align: center; margin-bottom: 12px; }}
.comp-vs {{ text-align: center; font-size: 24px; font-weight: bold; color: #818cf8; }}
.comp-row {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.06); }}
.winner {{ color: #34d399; }}
.loser {{ color: #f87171; }}
.bar-container {{ margin: 8px 0; }}
.bar-bg {{ background: rgba(255,255,255,0.08); border-radius: 4px; height: 8px; overflow: hidden; }}
.bar-fill {{ background: linear-gradient(90deg, #6366f1, #818cf8); border-radius: 4px; height: 100%; transition: width 0.5s; }}
.footer {{ text-align: center; color: #64748b; font-size: 12px; margin-top: 40px; padding: 20px; }}
.positive {{ color: #34d399; }}
.negative {{ color: #f87171; }}
.tag {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; margin: 2px; }}
.tag-win {{ background: rgba(52,211,153,0.15); color: #34d399; }}
.tag-loss {{ background: rgba(248,113,113,0.15); color: #f87171; }}
@media (max-width: 600px) {{ .comparison {{ grid-template-columns: 1fr; }} }}
</style>
{extra_head}
</head>
<body>
<div class="container">
{body}
<div class="footer">
  <p>NBA Analyst 🏀 | 数据来源: NBA.com | 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
</div>
</div>
</body>
</html>'''


def generate_player_report(name: str, season: str = '2025-26') -> str:
    """生成球员 HTML 报告

    Returns:
        HTML 文件路径
    """
    en_name, cn_name = i18n.resolve_player_name(name)
    player_id = client.get_player_id(en_name)

    if not player_id:
        return f"❌ 未找到球员: {name}"

    info = client.get_player_info(player_id)
    recent = client.get_player_recent_games(player_id, 10, season)
    career = client.get_player_career_stats(player_id)
    shot_data = client.get_shot_chart(player_id, season)

    # 基本信息卡片
    team_cn = i18n.team_en_to_cn(info.get('team', '')) if info else ''
    info_section = ''
    if info:
        info_section = f'''
    <div class="card">
      <h2>📋 基本信息</h2>
      <div class="stats-grid">
        <div class="stat-box"><div class="value">{info.get('jersey', '-')}</div><div class="label">球衣号</div></div>
        <div class="stat-box"><div class="value">{info.get('position', '-')}</div><div class="label">位置</div></div>
        <div class="stat-box"><div class="value">{info.get('height', '-')}</div><div class="label">身高</div></div>
        <div class="stat-box"><div class="value">{info.get('weight', '-')}</div><div class="label">体重(磅)</div></div>
        <div class="stat-box"><div class="value">{info.get('experience', '-')}</div><div class="label">经验(年)</div></div>
        <div class="stat-box"><div class="value">{info.get('draft_year', '-')}</div><div class="label">选秀年份</div></div>
      </div>
      <div style="margin-top:12px; color:#94a3b8;">
        球队: {team_cn or info.get('team','')} | 大学: {info.get('college','')} | 国籍: {info.get('country','')}
      </div>
    </div>'''

    # 近期表现表格
    games_rows = ''
    for g in recent.get('games', [])[:10]:
        opp = g['matchup'].split(' ')[-1] if ' ' in g['matchup'] else g['matchup']
        opp_cn = i18n.team_en_to_cn(opp) or opp
        result_cls = 'tag-win' if g['wl'] == 'W' else 'tag-loss'
        result_text = 'W' if g['wl'] == 'W' else 'L'
        games_rows += f'''<tr>
          <td>{g['date']}</td><td>{opp_cn}</td>
          <td>{g['pts']}</td><td>{g['reb']}</td><td>{g['ast']}</td>
          <td>{g['stl']}</td><td>{g['blk']}</td><td>{g['plus_minus']}</td>
          <td><span class="tag {result_cls}">{result_text}</span></td>
        </tr>'''

    recent_section = ''
    if games_rows:
        avgs = recent.get('averages', {})
        recent_section = f'''
    <div class="card">
      <h2>📊 近期数据 — 最近 10 场</h2>
      <div class="stats-grid">
        <div class="stat-box"><div class="value">{avgs.get('PTS', 0):.1f}</div><div class="label">得分</div></div>
        <div class="stat-box"><div class="value">{avgs.get('REB', 0):.1f}</div><div class="label">篮板</div></div>
        <div class="stat-box"><div class="value">{avgs.get('AST', 0):.1f}</div><div class="label">助攻</div></div>
        <div class="stat-box"><div class="value">{avgs.get('STL', 0):.1f}</div><div class="label">抢断</div></div>
        <div class="stat-box"><div class="value">{avgs.get('BLK', 0):.1f}</div><div class="label">盖帽</div></div>
      </div>
      <h3 style="margin-top:16px; color:#94a3b8;">命中率</h3>
      <div class="bar-container"><span style="color:#94a3b8;font-size:13px;">投篮 {avgs.get("FG_PCT","-")}%</span>
        <div class="bar-bg"><div class="bar-fill" style="width:{min(avgs.get("FG_PCT",50),100)}%"></div></div></div>
      <div class="bar-container"><span style="color:#94a3b8;font-size:13px;">三分 {avgs.get("FG3_PCT","-")}%</span>
        <div class="bar-bg"><div class="bar-fill" style="width:{min(avgs.get("FG3_PCT",40),100)}%"></div></div></div>
      <div class="bar-container"><span style="color:#94a3b8;font-size:13px;">罚球 {avgs.get("FT_PCT","-")}%</span>
        <div class="bar-bg"><div class="bar-fill" style="width:{min(avgs.get("FT_PCT",80),100)}%"></div></div></div>
      <h3 style="margin-top:20px; color:#94a3b8;">比赛详情</h3>
      <table>
        <tr><th>日期</th><th>对手</th><th>得分</th><th>篮板</th><th>助攻</th><th>抢断</th><th>盖帽</th><th>±</th><th>结果</th></tr>
        {games_rows}
      </table>
    </div>'''

    # 投篮分布
    shot_section = ''
    shot_summary = shot_data.get('summary', {})
    if shot_summary.get('total', 0) > 0:
        zones_html = ''
        zone_count = {}
        zone_made = {}
        for s in shot_data.get('shots', []):
            zone = s.get('zone', 'Other')
            zone_count[zone] = zone_count.get(zone, 0) + 1
            if s['made']:
                zone_made[zone] = zone_made.get(zone, 0) + 1
        for zone in sorted(zone_count.keys()):
            total = zone_count[zone]
            made = zone_made.get(zone, 0)
            pct = made / total * 100 if total > 0 else 0
            zones_html += f'''<div class="comp-row">
              <span>{zone}</span><span>{made}/{total}</span>
              <span class="{'positive' if pct >= 50 else 'negative' if pct < 35 else ''}">{pct:.1f}%</span>
            </div>'''

        shot_section = f'''
    <div class="card">
      <h2>🎯 投篮分布 — {season} 赛季</h2>
      <div class="stats-grid">
        <div class="stat-box"><div class="value">{shot_summary.get('total',0)}</div><div class="label">总出手</div></div>
        <div class="stat-box"><div class="value">{shot_summary.get('fg_pct',0)}%</div><div class="label">命中率</div></div>
        <div class="stat-box"><div class="value">{shot_summary.get('fg3_total',0)}</div><div class="label">三分出手</div></div>
        <div class="stat-box"><div class="value">{shot_summary.get('fg3_pct',0)}%</div><div class="label">三分命中率</div></div>
      </div>
      <h3 style="margin-top:16px; color:#94a3b8;">区域命中率</h3>
      <div style="max-width:500px;">
        {zones_html}
      </div>
    </div>'''

    # 生涯趋势
    career_section = ''
    if career is not None and not career.empty and len(career) > 1:
        seasons_rows = ''
        for _, row in career.tail(8).iterrows():
            seasons_rows += f'<tr><td>{row.get("SEASON_ID","")}</td><td>{row.get("TEAM_ABBREVIATION","")}</td><td>{row.get("GP","")}</td><td>{row.get("PTS",""):.1f}</td><td>{row.get("REB",""):.1f}</td><td>{row.get("AST",""):.1f}</td></tr>'
        career_section = f'''
    <div class="card">
      <h2>📈 生涯趋势</h2>
      <table>
        <tr><th>赛季</th><th>球队</th><th>出场</th><th>得分</th><th>篮板</th><th>助攻</th></tr>
        {seasons_rows}
      </table>
    </div>'''

    display_name = f"{cn_name} ({en_name})" if cn_name != en_name else en_name
    body = f'''
  <div class="header">
    <h1>🏀 {display_name}</h1>
    <div class="sub">球员分析报告 | {season} 赛季</div>
  </div>
  {info_section}
  {recent_section}
  {shot_section}
  {career_section}
'''

    html = _html_page(f"NBA 球员报告 - {cn_name}", body)
    filepath = os.path.join(OUTPUT_DIR, f"nba_report_{player_id}.html")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return filepath


def generate_team_report(name: str, season: str = '2025-26') -> str:
    """生成球队 HTML 报告"""
    en_name, cn_name = i18n.resolve_team_name(name)
    team_id = client.get_team_id(en_name)

    if not team_id:
        return f"❌ 未找到球队: {name}"

    info = client.get_team_info(team_id)
    stats = client.get_team_season_stats(team_id, season)
    schedule = client.get_team_schedule(team_id, season, 10)
    roster = client.get_team_roster(team_id, season)

    # 基本信息
    conf_cn = '西部' if info.get('conference') == 'West' else '东部' if info else ''
    info_section = ''
    if info:
        info_section = f'''
    <div class="card">
      <h2>📋 球队信息</h2>
      <div class="stats-grid">
        <div class="stat-box"><div class="value">{info.get('city','')}</div><div class="label">城市</div></div>
        <div class="stat-box"><div class="value">{conf_cn}</div><div class="label">分区</div></div>
        <div class="stat-box"><div class="value">{info.get('division','')}</div><div class="label">赛区</div></div>
        <div class="stat-box"><div class="value">{info.get('founded','')}</div><div class="label">成立年份</div></div>
      </div>
    </div>'''

    # 赛季数据
    stats_section = ''
    if stats:
        stats_section = f'''
    <div class="card">
      <h2>📊 {season} 赛季数据</h2>
      <div class="stats-grid">
        <div class="stat-box"><div class="value">{stats.get('w',0)}-{stats.get('l',0)}</div><div class="label">战绩</div></div>
        <div class="stat-box"><div class="value">{stats.get('win_pct',0):.3f}</div><div class="label">胜率</div></div>
        <div class="stat-box"><div class="value">{stats.get('pts',0):.1f}</div><div class="label">场均得分</div></div>
        <div class="stat-box"><div class="value">{stats.get('reb',0):.1f}</div><div class="label">场均篮板</div></div>
        <div class="stat-box"><div class="value">{stats.get('ast',0):.1f}</div><div class="label">场均助攻</div></div>
        <div class="stat-box"><div class="value">{stats.get('off_rtg',0):.1f}/{stats.get('def_rtg',0):.1f}</div><div class="label">进攻/防守效率</div></div>
      </div>
      <h3 style="margin-top:20px; color:#94a3b8;">命中率</h3>
      <div class="bar-container"><span style="color:#94a3b8;font-size:13px;">投篮 {stats.get("fg_pct",0):.1f}%</span>
        <div class="bar-bg"><div class="bar-fill" style="width:{min(stats.get('fg_pct',45),100)}%"></div></div></div>
      <div class="bar-container"><span style="color:#94a3b8;font-size:13px;">三分 {stats.get("fg3_pct",0):.1f}%</span>
        <div class="bar-bg"><div class="bar-fill" style="width:{min(stats.get('fg3_pct',35),100)}%"></div></div></div>
    </div>'''

    # 赛程
    schedule_rows = ''
    for g in schedule:
        result_cls = 'tag-win' if g['wl'] == 'W' else 'tag-loss'
        result_text = 'W' if g['wl'] == 'W' else 'L'
        schedule_rows += f'<tr><td>{g["date"]}</td><td>{g["matchup"]}</td><td>{g["pts"]}</td><td><span class="tag {result_cls}">{result_text}</span></td></tr>'

    schedule_section = ''
    if schedule_rows:
        schedule_section = f'''
    <div class="card">
      <h2>📅 近期赛程</h2>
      <table>
        <tr><th>日期</th><th>对阵</th><th>得分</th><th>结果</th></tr>
        {schedule_rows}
      </table>
    </div>'''

    # 阵容
    roster_rows = ''
    for p in roster[:15]:
        name_cn = i18n.player_en_to_cn(p['name'])
        name_str = f"{name_cn} ({p['name']})" if name_cn != p['name'] else p['name']
        roster_rows += f'<tr><td>#{p["number"]}</td><td>{name_str}</td><td>{p["position"]}</td><td>{p["height"]}</td></tr>'

    roster_section = ''
    if roster_rows:
        roster_section = f'''
    <div class="card">
      <h2>👥 球员阵容</h2>
      <table>
        <tr><th>号码</th><th>球员</th><th>位置</th><th>身高</th></tr>
        {roster_rows}
      </table>
    </div>'''

    body = f'''
  <div class="header">
    <h1>🏀 {cn_name}</h1>
    <div class="sub">球队分析报告 | {season} 赛季</div>
  </div>
  {info_section}
  {stats_section}
  {schedule_section}
  {roster_section}
'''

    html = _html_page(f"NBA 球队报告 - {cn_name}", body)
    filepath = os.path.join(OUTPUT_DIR, f"nba_report_team_{team_id}.html")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return filepath


def generate_today_report(date_str: str = None) -> str:
    """生成今日比赛汇总报告"""
    if date_str is None:
        date_str = datetime.now().strftime('%Y-%m-%d')

    games = client.get_today_scoreboard(date_str)

    if not games:
        body = f'''
  <div class="header">
    <h1>🏀 NBA 今日比赛</h1>
    <div class="sub">{date_str}</div>
  </div>
  <div class="card">
    <p style="text-align:center;color:#94a3b8;padding:40px;">暂无比赛数据</p>
  </div>'''

    else:
        games_html = ''
        for g in games:
            home_cn = i18n.team_en_to_cn(g['home_team']) or g['home_team']
            away_cn = i18n.team_en_to_cn(g['away_team']) or g['away_team']
            status_text = g.get('status', '')
            status_class = 'tag-win' if 'Final' in str(status_text) else ''
            games_html += f'''
    <div class="card">
      <h2>{away_cn} @ {home_cn} <span class="tag {status_class}" style="float:right">{status_text}</span></h2>
      <div class="stats-grid">
        <div class="stat-box"><div class="value">{g['away_score']}</div><div class="label">{away_cn}</div></div>
        <div class="stat-box"><div class="value" style="font-size:18px;">VS</div><div class="label">比分</div></div>
        <div class="stat-box"><div class="value">{g['home_score']}</div><div class="label">{home_cn}</div></div>
      </div>
    </div>'''

        body = f'''
  <div class="header">
    <h1>🏀 NBA 今日比赛</h1>
    <div class="sub">{date_str}</div>
  </div>
  {games_html}'''

    html = _html_page(f"NBA 今日比赛 - {date_str}", body)
    filepath = os.path.join(OUTPUT_DIR, f"nba_report_today_{date_str}.html")
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(html)
    return filepath
