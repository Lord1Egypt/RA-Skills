"""
比分板模块 — 查询当日/指定日期 NBA 比分
"""

from datetime import datetime
from .nba_client import NBAClient
from .i18n import I18N

client = NBAClient()
i18n = I18N()


def get_scoreboard(date_str: str = None) -> str:
    """获取比分板并格式化为文本

    Args:
        date_str: 日期字符串 YYYY-MM-DD，默认今天

    Returns:
        格式化的比分板文本
    """
    try:
        if date_str is None:
            date_str = datetime.now().strftime('%Y-%m-%d')

        games = client.get_today_scoreboard(date_str)

        if not games:
            return f"📅 {date_str}\n\n暂无比赛数据（可能今日无比赛或赛季未开始）"

        lines = [f"🏀 NBA 比分 — {date_str}", "=" * 50, ""]

        for g in games:
            home_cn = i18n.team_en_to_cn(g['home_team']) or g['home_team']
            away_cn = i18n.team_en_to_cn(g['away_team']) or g['away_team']
            home_score = g['home_score'] or 0
            away_score = g['away_score'] or 0
            status = g.get('status', '未开始')

            lines.append(f"  {away_cn} @ {home_cn}")
            lines.append(f"  比分: {away_score} - {home_score}")

            if 'Final' in str(status):
                winner = away_cn if away_score > home_score else home_cn
                diff = abs(away_score - home_score)
                lines.append(f"  ✅ 已结束 ({winner} 胜, 分差 {diff})")
            elif 'Q' in str(status) or 'OT' in str(status):
                period = g.get('period', '')
                clock = g.get('clock', '')
                lines.append(f"  🔴 进行中 [{status}] 剩余 {clock}")
            else:
                lines.append(f"  ⏰ {status}")
            lines.append("")

        return '\n'.join(lines)

    except Exception as e:
        return f"❌ 获取比分失败: {e}"


def get_live_scoreboard() -> str:
    """获取实时比分板 (live endpoint)"""
    try:
        from nba_api.live.nba.endpoints import scoreboard as live_sb
        board = live_sb.ScoreBoard()
        data = board.get_dict()

        games = data.get('scoreboard', {}).get('games', [])
        if not games:
            return "🏀 当前无直播比赛"

        lines = ["🏀 NBA 实时比分 (Live)", "=" * 50, ""]

        for g in games:
            home = g.get('homeTeam', {})
            away = g.get('awayTeam', {})
            home_cn = i18n.team_en_to_cn(home.get('teamName', ''))
            away_cn = i18n.team_en_to_cn(away.get('teamName', ''))
            home_score = home.get('score', 0)
            away_score = away.get('score', 0)
            status = g.get('gameStatusText', '')

            lines.append(f"  {away_cn} @ {home_cn}")
            lines.append(f"  比分: {away_score} - {home_score}")

            if g.get('gameStatus') == 2:
                period = g.get('period', '')
                clock = g.get('gameClock', '')
                lines.append(f"  🔴 进行中 [{status}] Q{period} {clock}")
            elif g.get('gameStatus') == 3:
                lines.append(f"  ✅ 已结束")
            else:
                lines.append(f"  ⏰ {status}")
            lines.append("")

        return '\n'.join(lines)

    except Exception as e:
        return f"❌ 获取实时比分失败: {e}"
