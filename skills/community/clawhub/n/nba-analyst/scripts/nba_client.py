"""
NBA 数据访问封装层
统一管理 nba_api 调用、缓存、错误处理、重试
"""

import time
from datetime import datetime, timedelta
from functools import wraps
import pandas as pd
import json
import os

# nba_api imports
from nba_api.stats.endpoints import (
    leaguegamefinder,
    leaguestandingsv3,
    commonallplayers,
    commonplayerinfo,
    playercareerstats,
    playergamelog,
    teaminfocommon,
    teamdashboardbygeneralsplits,
    teamgamelog,
    teamplayerdashboard,
    boxscoretraditionalv2,
    boxscoreadvancedv2,
    boxscorefourfactorsv2,
    playercompare,
    commonteamroster,
    matchupsrollup,
    shotchartdetail,
    leaguedashplayerstats,
    leagueleaders,
    draftboard,
    drafthistory,
    scoreboardv2,
)

from nba_api.stats.static import players, teams
from nba_api.live.nba.endpoints import scoreboard as live_scoreboard

# 缓存目录
CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', '.cache')
os.makedirs(CACHE_DIR, exist_ok=True)


def cached(ttl=300):
    """缓存装饰器，TTL单位秒"""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            cache_key = f"{func.__name__}_{args}_{kwargs}"
            cache_file = os.path.join(CACHE_DIR, f"{hash(cache_key)}.json")

            if os.path.exists(cache_file):
                age = time.time() - os.path.getmtime(cache_file)
                if age < ttl:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        if isinstance(data, dict) and '_df' in data:
                            return pd.read_json(data['_df'])
                        return data

            result = func(self, *args, **kwargs)
            try:
                if isinstance(result, pd.DataFrame):
                    cache_data = {'_df': result.to_json()}
                elif isinstance(result, dict):
                    cache_data = json.loads(json.dumps(result, default=str))
                else:
                    cache_data = {'data': str(result)}
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(cache_data, f)
            except:
                pass
            return result
        return wrapper
    return decorator


def retry(max_retries=2, delay=2):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for i in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if i < max_retries:
                        time.sleep(delay * (i + 1))
            raise last_error
        return wrapper
    return decorator


class NBAClient:
    """NBA 数据访问客户端"""

    def __init__(self):
        self._all_players = None
        self._all_teams = None

    # ==================== 基础查询 ====================

    def get_all_players(self) -> list:
        """获取所有球员列表 (静态数据)"""
        if self._all_players is None:
            self._all_players = players.get_players()
        return self._all_players

    def get_all_teams(self) -> list:
        """获取所有球队列表 (静态数据)"""
        if self._all_teams is None:
            self._all_teams = teams.get_teams()
        return self._all_teams

    def find_player(self, name: str) -> list:
        """模糊搜索球员名 (英文)"""
        all_players = self.get_all_players()
        name_lower = name.lower()
        results = []
        for p in all_players:
            if name_lower in p['full_name'].lower():
                results.append(p)
        return results[:10]

    def find_team(self, name: str) -> list:
        """模糊搜索球队名"""
        all_teams = self.get_all_teams()
        name_lower = name.lower()
        results = []
        for t in all_teams:
            if name_lower in t['full_name'].lower() or \
               name_lower in t.get('nickname', '').lower() or \
               name_lower in t.get('abbreviation', '').lower():
                results.append(t)
        return results[:10]

    def get_player_id(self, full_name: str) -> int:
        """根据全名获取球员ID"""
        all_players = self.get_all_players()
        name_lower = full_name.lower()
        for p in all_players:
            if p['full_name'].lower() == name_lower:
                return p['id']
        # 模糊匹配
        matches = self.find_player(full_name)
        if matches:
            return matches[0]['id']
        return None

    def get_team_id(self, team_name: str) -> int:
        """根据队名获取球队ID"""
        all_teams = self.get_all_teams()
        name_lower = team_name.lower()
        for t in all_teams:
            if name_lower == t['full_name'].lower() or \
               name_lower == t.get('nickname', '').lower() or \
               name_lower == t.get('abbreviation', '').lower():
                return t['id']
        matches = self.find_team(team_name)
        if matches:
            return matches[0]['id']
        return None

    # ==================== 比分板 ====================

    @retry(max_retries=2)
    def get_today_scoreboard(self, date_str: str = None) -> list:
        """获取指定日期比分板 (赛季中有效)"""
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')

        try:
            board = scoreboardv2.ScoreboardV2(game_date=date_str, league_id='00')
            games = board.get_normalized_dict().get('GameHeader', [])

            result = []
            for g in games:
                result.append({
                    'game_id': g.get('GAME_ID'),
                    'date': g.get('GAME_DATE_EST', date_str),
                    'home_team': g.get('HOME_TEAM_NAME', '?'),
                    'away_team': g.get('VISITOR_TEAM_NAME', '?'),
                    'home_score': g.get('HOME_TEAM_SCORE', 0),
                    'away_score': g.get('VISITOR_TEAM_SCORE', 0),
                    'status': g.get('GAME_STATUS_TEXT', ''),
                    'period': g.get('LIVE_PERIOD', 0),
                    'clock': g.get('LIVE_PC_TIME', ''),
                    'home_team_id': g.get('HOME_TEAM_ID'),
                    'away_team_id': g.get('VISITOR_TEAM_ID'),
                })
            return result
        except Exception as e:
            raise Exception(f"获取比分板失败: {e}")

    # ==================== 排名 ====================

    @retry(max_retries=2)
    def get_standings(self, season: str = '2025-26') -> pd.DataFrame:
        """获取联盟排名"""
        try:
            s = leaguestandingsv3.LeagueStandingsV3(
                season=season,
                league_id='00'
            )
            df = s.get_data_frames()[0]
            return df
        except Exception as e:
            raise Exception(f"获取排名失败: {e}")

    def get_standings_by_conference(self, conference: str = 'west', season: str = '2025-26') -> dict:
        """获取分区排名"""
        df = self.get_standings(season)
        conf = 'West' if conference.lower() in ('west', '西部', '西') else 'East'

        conf_df = df[df['Conference'] == conf].copy()
        conf_df = conf_df.sort_values('PlayoffRank')

        result = {
            'conference': conf,
            'season': season,
            'teams': []
        }
        for _, row in conf_df.iterrows():
            result['teams'].append({
                'rank': row['PlayoffRank'],
                'name': row['TeamName'],
                'wins': row['WINS'],
                'losses': row['LOSSES'],
                'win_pct': round(row['WinPCT'], 3),
                'home_record': row.get('HOME', ''),
                'road_record': row.get('ROAD', ''),
                'streak': row.get('strCurrentStreak', ''),
                'last10': row.get('L10', ''),
                'gb': row.get('GB', ''),
                'division': row.get('Division', ''),
            })
        return result

    # ==================== 球员 ====================

    @retry(max_retries=2)
    def get_player_info(self, player_id: int) -> dict:
        """获取球员基本信息"""
        try:
            info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
            df = info.get_data_frames()[0]
            if df.empty:
                return None

            row = df.iloc[0]
            return {
                'name': row.get('DISPLAY_FIRST_LAST', ''),
                'team': row.get('TEAM_NAME', ''),
                'team_abbr': row.get('TEAM_ABBREVIATION', ''),
                'position': row.get('POSITION', ''),
                'height': row.get('HEIGHT', ''),
                'weight': row.get('WEIGHT', ''),
                'jersey': row.get('JERSEY', ''),
                'experience': row.get('FROM_YEAR', ''),
                'college': row.get('SCHOOL', ''),
                'country': row.get('COUNTRY', ''),
                'draft_year': row.get('DRAFT_YEAR', ''),
                'draft_round': row.get('DRAFT_ROUND', ''),
                'draft_number': row.get('DRAFT_NUMBER', ''),
            }
        except Exception as e:
            raise Exception(f"获取球员信息失败: {e}")

    @retry(max_retries=2)
    def get_player_career_stats(self, player_id: int) -> pd.DataFrame:
        """获取球员生涯统计"""
        try:
            stats = playercareerstats.PlayerCareerStats(player_id=player_id, per_mode36='PerGame')
            df = stats.get_data_frames()[0]
            return df
        except Exception as e:
            raise Exception(f"获取球员生涯统计失败: {e}")

    @retry(max_retries=2)
    def get_player_game_log(self, player_id: int, season: str = '2025-26') -> pd.DataFrame:
        """获取球员比赛日志"""
        try:
            log = playergamelog.PlayerGameLog(player_id=player_id, season=season)
            df = log.get_data_frames()[0]
            return df
        except Exception as e:
            raise Exception(f"获取球员比赛日志失败: {e}")

    def get_player_recent_games(self, player_id: int, n: int = 10, season: str = '2025-26') -> dict:
        """获取球员最近N场比赛 + 滚动均值"""
        df = self.get_player_game_log(player_id, season)
        if df.empty:
            return {'games': [], 'averages': {}}

        recent = df.head(n).copy()
        games = []
        for _, row in recent.iterrows():
            games.append({
                'date': row.get('GAME_DATE', ''),
                'matchup': row.get('MATCHUP', ''),
                'wl': row.get('WL', ''),
                'min': row.get('MIN', 0),
                'pts': row.get('PTS', 0),
                'reb': row.get('REB', 0),
                'ast': row.get('AST', 0),
                'stl': row.get('STL', 0),
                'blk': row.get('BLK', 0),
                'tov': row.get('TOV', 0),
                'fgm': row.get('FGM', 0),
                'fga': row.get('FGA', 0),
                'fg3m': row.get('FG3M', 0),
                'fg3a': row.get('FG3A', 0),
                'ftm': row.get('FTM', 0),
                'fta': row.get('FTA', 0),
                'plus_minus': row.get('PLUS_MINUS', 0),
            })

        # 滚动均值
        numeric_cols = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA']
        avg_df = df.head(n)[numeric_cols].apply(pd.to_numeric, errors='coerce')
        averages = avg_df.mean().to_dict()

        # 计算命中率
        if averages.get('FGA', 0) > 0:
            averages['FG_PCT'] = round(averages['FGM'] / averages['FGA'] * 100, 1)
        if averages.get('FG3A', 0) > 0:
            averages['FG3_PCT'] = round(averages['FG3M'] / averages['FG3A'] * 100, 1)
        if averages.get('FTA', 0) > 0:
            averages['FT_PCT'] = round(averages['FTM'] / averages['FTA'] * 100, 1)

        return {
            'games': games,
            'averages': {k: round(v, 1) if isinstance(v, float) else v for k, v in averages.items()}
        }

    # ==================== 球队 ====================

    @retry(max_retries=2)
    def get_team_info(self, team_id: int) -> dict:
        """获取球队基本信息"""
        try:
            info = teaminfocommon.TeamInfoCommon(team_id=team_id)
            dfs = info.get_data_frames()
            if len(dfs) >= 2 and not dfs[0].empty:
                row = dfs[0].iloc[0]
                return {
                    'name': row.get('TEAM_NAME', ''),
                    'abbreviation': row.get('TEAM_ABBREVIATION', ''),
                    'city': row.get('TEAM_CITY', ''),
                    'conference': row.get('TEAM_CONFERENCE', ''),
                    'division': row.get('TEAM_DIVISION', ''),
                    'founded': row.get('MIN_YEAR', ''),
                }
        except Exception as e:
            raise Exception(f"获取球队信息失败: {e}")
        return None

    @retry(max_retries=2)
    def get_team_season_stats(self, team_id: int, season: str = '2025-26') -> dict:
        """获取球队赛季统计"""
        try:
            dash = teamdashboardbygeneralsplits.TeamDashboardByGeneralSplits(
                team_id=team_id, season=season
            )
            df = dash.get_data_frames()[0]
            if df.empty:
                return None
            row = df.iloc[0]
            return {
                'gp': row.get('GP', 0),
                'w': row.get('W', 0),
                'l': row.get('L', 0),
                'win_pct': round(row.get('W_PCT', 0), 3),
                'min': row.get('MIN', 0),
                'pts': row.get('PTS', 0),
                'reb': row.get('REB', 0),
                'ast': row.get('AST', 0),
                'stl': row.get('STL', 0),
                'blk': row.get('BLK', 0),
                'tov': row.get('TOV', 0),
                'fg_pct': round(row.get('FG_PCT', 0) * 100, 1),
                'fg3_pct': round(row.get('FG3_PCT', 0) * 100, 1),
                'ft_pct': round(row.get('FT_PCT', 0) * 100, 1),
                'oreb': row.get('OREB', 0),
                'dreb': row.get('DREB', 0),
                'pts_rank': row.get('PTS_RANK', ''),
                'ast_rank': row.get('AST_RANK', ''),
                'off_rtg': row.get('OFF_RATING', 0),
                'def_rtg': row.get('DEF_RATING', 0),
                'net_rtg': row.get('NET_RATING', 0),
                'pace': row.get('PACE', 0),
            }
        except Exception as e:
            raise Exception(f"获取球队赛季统计失败: {e}")

    @retry(max_retries=2)
    def get_team_schedule(self, team_id: int, season: str = '2025-26', n: int = 10) -> list:
        """获取球队最近/即将比赛"""
        try:
            log = teamgamelog.TeamGameLog(team_id=team_id, season=season)
            df = log.get_data_frames()[0]
            games = []
            for _, row in df.head(n).iterrows():
                games.append({
                    'date': row.get('GAME_DATE', ''),
                    'matchup': row.get('MATCHUP', ''),
                    'wl': row.get('WL', ''),
                    'pts': row.get('PTS', 0),
                    'opp_pts': row.get('PLUS_MINUS', 0),
                })
            return games
        except Exception as e:
            raise Exception(f"获取球队赛程失败: {e}")

    @retry(max_retries=2)
    def get_team_roster(self, team_id: int, season: str = '2025-26') -> list:
        """获取球队阵容"""
        try:
            roster = commonteamroster.CommonTeamRoster(team_id=team_id, season=season)
            dfs = roster.get_data_frames()
            if dfs and not dfs[0].empty:
                df = dfs[0]
                players_list = []
                for _, row in df.iterrows():
                    players_list.append({
                        'name': row.get('PLAYER', ''),
                        'number': row.get('NUM', ''),
                        'position': row.get('POSITION', ''),
                        'height': row.get('HEIGHT', ''),
                        'weight': row.get('WEIGHT', ''),
                        'experience': row.get('EXP', ''),
                        'college': row.get('SCHOOL', ''),
                        'player_id': row.get('PLAYER_ID', ''),
                    })
                return players_list
        except Exception as e:
            raise Exception(f"获取球队阵容失败: {e}")
        return []

    # ==================== Box Score ====================

    @retry(max_retries=2)
    def get_box_score(self, game_id: str) -> dict:
        """获取比赛Box Score"""
        try:
            trad = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)
            adv = boxscoreadvancedv2.BoxScoreAdvancedV2(game_id=game_id)
            four = boxscorefourfactorsv2.BoxScoreFourFactorsV2(game_id=game_id)

            # 传统数据
            trad_dfs = trad.get_data_frames()
            # 高阶数据
            adv_dfs = adv.get_data_frames()
            # 四因素
            four_dfs = four.get_data_frames()

            def df_to_records(df):
                if df.empty:
                    return []
                records = []
                for _, row in df.iterrows():
                    d = {}
                    for col in df.columns:
                        val = row[col]
                        d[col] = val
                    records.append(d)
                return records

            return {
                'game_id': game_id,
                'traditional': {
                    'home': df_to_records(trad_dfs[1]) if len(trad_dfs) > 1 else [],
                    'away': df_to_records(trad_dfs[0]) if len(trad_dfs) > 0 else [],
                },
                'advanced': {
                    'home': df_to_records(adv_dfs[1]) if len(adv_dfs) > 1 else [],
                    'away': df_to_records(adv_dfs[0]) if len(adv_dfs) > 0 else [],
                },
                'four_factors': {
                    'home': df_to_records(four_dfs[1]) if len(four_dfs) > 1 else [],
                    'away': df_to_records(four_dfs[0]) if len(four_dfs) > 0 else [],
                },
            }
        except Exception as e:
            raise Exception(f"获取Box Score失败: {e}")

    # ==================== 对比 ====================

    @retry(max_retries=2)
    def compare_players(self, player_id_1: int, player_id_2: int) -> dict:
        """球员对比"""
        try:
            comp = playercompare.PlayerCompare(
                player_id_list=f"{player_id_1},{player_id_2}",
                vs_player_id_list=f"{player_id_1},{player_id_2}"
            )
            dfs = comp.get_data_frames()
            if dfs and not dfs[0].empty:
                df = dfs[0]
                p1 = {}
                p2 = {}
                for _, row in df.iterrows():
                    pid = row.get('PLAYER_ID', 0)
                    target = p1 if pid == player_id_1 else p2
                    for col in df.columns:
                        target[col] = row[col]
                return {'player_1': p1, 'player_2': p2}

            # Fallback: 分别获取生涯数据
            s1 = self.get_player_career_stats(player_id_1)
            s2 = self.get_player_career_stats(player_id_2)

            def extract_recent(row):
                return {
                    'PTS': row.get('PTS', 0), 'REB': row.get('REB', 0),
                    'AST': row.get('AST', 0), 'STL': row.get('STL', 0),
                    'BLK': row.get('BLK', 0), 'FG_PCT': row.get('FG_PCT', 0),
                    'FG3_PCT': row.get('FG3_PCT', 0), 'FT_PCT': row.get('FT_PCT', 0),
                    'MIN': row.get('MIN', 0), 'GP': row.get('GP', 0),
                }

            p1 = extract_recent(s1.iloc[-1]) if not s1.empty else {}
            p2 = extract_recent(s2.iloc[-1]) if not s2.empty else {}
            return {'player_1': p1, 'player_2': p2}

        except Exception as e:
            raise Exception(f"球员对比失败: {e}")

    # ==================== 投篮图 ====================

    @retry(max_retries=2)
    def get_shot_chart(self, player_id: int, season: str = '2025-26') -> dict:
        """获取球员投篮热力图数据"""
        try:
            chart = shotchartdetail.ShotChartDetail(
                team_id=0,
                player_id=player_id,
                season_nullable=season,
                context_measure_simple='FGA'
            )
            dfs = chart.get_data_frames()
            if dfs and not dfs[0].empty:
                df = dfs[0]
                shots = []
                for _, row in df.iterrows():
                    shots.append({
                        'x': row.get('LOC_X', 0),
                        'y': row.get('LOC_Y', 0),
                        'made': row.get('SHOT_MADE_FLAG', 0) == 1,
                        'type': row.get('SHOT_TYPE', ''),
                        'zone': row.get('SHOT_ZONE_BASIC', ''),
                        'distance': row.get('SHOT_DISTANCE', 0),
                    })

                # 统计
                total = len(shots)
                made = sum(1 for s in shots if s['made'])
                fg3_shots = [s for s in shots if s['type'] and '3PT' in s['type']]
                fg3_made = sum(1 for s in fg3_shots if s['made'])

                return {
                    'shots': shots,
                    'summary': {
                        'total': total,
                        'made': made,
                        'fg_pct': round(made / total * 100, 1) if total > 0 else 0,
                        'fg3_total': len(fg3_shots),
                        'fg3_made': fg3_made,
                        'fg3_pct': round(fg3_made / len(fg3_shots) * 100, 1) if fg3_shots else 0,
                    }
                }
        except Exception as e:
            raise Exception(f"获取投篮图失败: {e}")
        return {'shots': [], 'summary': {}}

    # ==================== 历史交锋 ====================

    @retry(max_retries=2)
    def get_matchup_history(self, team_id_1: int, team_id_2: int, season: str = '2025-26') -> list:
        """获取两队历史交锋"""
        try:
            matchups = matchupsrollup.MatchupsRollup(
                def_team_id_nullable=team_id_1,
                off_team_id_nullable=team_id_2,
                season=season
            )
            dfs = matchups.get_data_frames()
            if dfs and not dfs[0].empty:
                df = dfs[0]
                games = []
                for _, row in df.head(10).iterrows():
                    games.append({
                        'date': row.get('GAME_DATE', ''),
                        'matchup': row.get('MATCHUP', ''),
                        'wl': row.get('WL', ''),
                        'pts': row.get('PTS', 0),
                        'opp_pts': row.get('PLUS_MINUS', 0),
                    })
                return games
        except Exception as e:
            raise Exception(f"获取历史交锋失败: {e}")
        return []

    # ==================== 联盟领先者 ====================

    @retry(max_retries=2)
    def get_league_leaders(self, stat_category: str = 'PTS', season: str = '2025-26', top: int = 10) -> list:
        """获取联盟数据领先者"""
        try:
            leaders = leagueleaders.LeagueLeaders(
                season=season,
                per_mode48='PerGame',
                stat_category_abbreviation=stat_category
            )
            df = leaders.get_data_frames()[0]
            result = []
            for _, row in df.head(top).iterrows():
                result.append({
                    'rank': row.get('RANK', 0),
                    'name': row.get('PLAYER', ''),
                    'team': row.get('TEAM', ''),
                    'value': row.get(stat_category, 0),
                })
            return result
        except Exception as e:
            raise Exception(f"获取联盟领先者失败: {e}")

    # ==================== 选秀 ====================

    @retry(max_retries=2)
    def get_draft_history(self, draft_year: int) -> list:
        """获取某年选秀结果"""
        try:
            draft = drafthistory.DraftHistory(season=str(draft_year))
            dfs = draft.get_data_frames()
            if dfs and not dfs[0].empty:
                df = dfs[0]
                picks = []
                for _, row in df.iterrows():
                    picks.append({
                        'pick': row.get('OVERALL_PICK', 0),
                        'round': row.get('ROUND_NUMBER', 0),
                        'round_pick': row.get('ROUND_PICK', 0),
                        'name': row.get('PLAYER_NAME', ''),
                        'team': row.get('TEAM_NAME', ''),
                        'college': row.get('ORGANIZATION', ''),
                    })
                return picks
        except Exception as e:
            raise Exception(f"获取选秀历史失败: {e}")
        return []
