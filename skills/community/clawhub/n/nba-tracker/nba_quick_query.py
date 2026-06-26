#!/usr/bin/env python3
"""
NBA 快速查询脚本
用法: python nba_quick_query.py [command] [args]

示例:
  python nba_quick_query.py standings hornets
  python nba_quick_query.py schedule today
  python nba_quick_query.py player "LaMelo Ball"
  python nba_quick_query.py crunch-time
"""

import sys
import json
from datetime import datetime

# 安装: pip install nba_api pandas
try:
    from nba_api.stats.endpoints import (
        leaguestandings,
        scoreboardv2,
        playercareerstats,
        playerinjuries
    )
    from nba_api.stats.static import players, teams
    from nba_api.live.nba.endpoints import scoreboard, playbyplay
except ImportError:
    print("请先安装依赖: pip install nba_api pandas")
    sys.exit(1)


def get_standings(team_name=None):
    """查询战绩"""
    
    standings = leaguestandings.LeagueStandings()
    df = standings.get_data_frames()[0]
    
    if team_name:
        result = df[df['TeamName'].str.contains(team_name, case=False, na=False)]
        if result.empty:
            print(f"未找到球队: {team_name}")
            return
    else:
        # 返回东/西部前8
        east = df[df['Conference'] == 'East'].sort_values('PCT', ascending=False).head(8)
        west = df[df['Conference'] == 'West'].sort_values('PCT', ascending=False).head(8)
        result = pd.concat([east, west])
    
    print(result[['TeamName', 'W', 'L', 'PCT', 'Conference']].to_string(index=False))


def get_schedule(date_str=None):
    """查询赛程"""
    
    if date_str:
        game_date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%m/%d/%Y')
    else:
        game_date = datetime.now().strftime('%m/%d/%Y')
    
    board = scoreboardv2.ScoreboardV2(game_date=game_date)
    df = board.get_data_frames()[1]  # LineScore
    
    if df.empty:
        print(f"该日期无比赛: {game_date}")
        return
    
    games = df.groupby('GAME_ID')
    for game_id, group in games:
        home = group[group['TEAM_ID'] == group['TEAM_ID'].max()].iloc[0]
        away = group[group['TEAM_ID'] == group['TEAM_ID'].min()].iloc[0]
        print(f"{away['TEAM_CITY_NAME']} {away['TEAM_NICKNAME']} @ {home['TEAM_CITY_NAME']} {home['TEAM_NICKNAME']}")


def get_player_info(player_name):
    """查询球员信息"""
    
    player_list = players.find_players_by_full_name(player_name)
    if not player_list:
        print(f"未找到球员: {player_name}")
        return
    
    player = player_list[0]
    print(f"\n球员: {player['full_name']}")
    print(f"ID: {player['id']}")
    print(f"现役: {'是' if player['is_active'] else '否'}")
    
    # 生涯数据
    try:
        career = playercareerstats.PlayerCareerStats(player_id=player['id'])
        df = career.season_totals_regular_season.get_data_frame()
        
        if not df.empty:
            latest = df.iloc[-1]
            print(f"\n最近赛季 ({latest['SEASON_ID']}):")
            print(f"  得分: {latest['PTS']} 场均 {latest.get('PTS', 0) / latest.get('GP', 1):.1f}")
            print(f"  篮板: {latest['REB']}")
            print(f"  助攻: {latest['AST']}")
            print(f"  命中率: {latest['FG_PCT']:.3f}")
    except Exception as e:
        print(f"获取生涯数据失败: {e}")
    
    # 伤病情况
    try:
        injuries = playerinjuries.PlayerInjuries(player_id=player['id'])
        injury_df = injuries.get_data_frames()[0]
        
        if not injury_df.empty:
            print(f"\n⚠️ 伤病信息:")
            print(injury_df[['INJURY', 'STATUS', 'DATE']].to_string(index=False))
        else:
            print("\n✅ 无伤病")
    except:
        pass


def check_crunch_time():
    """检查关键时刻比赛"""
    
    games = scoreboard.ScoreBoard()
    data = games.get_dict()
    
    crunch_games = []
    
    for game in data['scoreboard']['games']:
        if game['gameStatus'] != 2:  # 只检查进行中的比赛
            continue
        
        home_score = game['homeTeam']['score']
        away_score = game['awayTeam']['score']
        score_diff = abs(home_score - away_score)
        
        if score_diff >= 5:
            continue
        
        # 简化：只检查比分，不深入查时间
        crunch_games.append({
            'home': game['homeTeam']['teamName'],
            'away': game['awayTeam']['teamName'],
            'home_score': home_score,
            'away_score': away_score,
            'status': game['gameStatusText']
        })
    
    if crunch_games:
        print("🔥 关键时刻比赛:")
        for g in crunch_games:
            print(f"  {g['away']} @ {g['home']}: {g['away_score']}-{g['home_score']} ({g['status']})")
    else:
        print("暂无关键时刻比赛")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    command = sys.argv[1].lower()
    
    if command == 'standings':
        team = sys.argv[2] if len(sys.argv) > 2 else None
        get_standings(team)
    
    elif command == 'schedule':
        date = sys.argv[2] if len(sys.argv) > 2 else None
        get_schedule(date)
    
    elif command == 'player':
        if len(sys.argv) < 3:
            print("请提供球员名字: python nba_quick_query.py player 'LaMelo Ball'")
            return
        get_player_info(sys.argv[2])
    
    elif command == 'crunch-time':
        check_crunch_time()
    
    else:
        print(f"未知命令: {command}")
        print(__doc__)


if __name__ == '__main__':
    main()
