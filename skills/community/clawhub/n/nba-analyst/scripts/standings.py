"""
排名模块 — 查询 NBA 联盟/分区排名
"""

from .nba_client import NBAClient
from .i18n import I18N

client = NBAClient()
i18n = I18N()


def get_standings(conference: str = None, season: str = '2025-26') -> str:
    """获取排名并格式化为文本

    Args:
        conference: 'west'/'east'/None(全部)
        season: 赛季字符串

    Returns:
        格式化排名文本
    """
    try:
        if conference and conference.lower() in ('west', '西部', '西'):
            data = client.get_standings_by_conference('west', season)
            return _format_conference_standings(data)
        elif conference and conference.lower() in ('east', '东部', '东'):
            data = client.get_standings_by_conference('east', season)
            return _format_conference_standings(data)
        else:
            # 全部排名
            west = client.get_standings_by_conference('west', season)
            east = client.get_standings_by_conference('east', season)
            return _format_conference_standings(west) + '\n\n' + _format_conference_standings(east)

    except Exception as e:
        return f"❌ 获取排名失败: {e}"


def _format_conference_standings(data: dict) -> str:
    """格式化分区排名"""
    conf_cn = '西部' if data['conference'] == 'West' else '东部'
    lines = [
        f"📊 NBA {conf_cn}排名 — {data['season']} 赛季",
        "=" * 60,
        f"{'排名':<4} {'球队':<12} {'胜':<5} {'负':<5} {'胜率':<8} {'胜场差':<6} {'近10场'}",
        "-" * 60,
    ]

    for t in data['teams']:
        name_cn = i18n.team_en_to_cn(t['name']) or t['name']
        lines.append(
            f"{t['rank']:<4} {name_cn:<12} {t['wins']:<5} {t['losses']:<5} "
            f"{t['win_pct']:.3f}   {t['gb']:<6} {t['last10']}"
        )

    return '\n'.join(lines)


def get_standings_json(conference: str = None, season: str = '2025-26') -> dict:
    """获取排名 JSON 格式（供 HTML 报告使用）"""
    if conference and conference.lower() in ('west', '西部', '西'):
        return client.get_standings_by_conference('west', season)
    elif conference and conference.lower() in ('east', '东部', '东'):
        return client.get_standings_by_conference('east', season)
    else:
        return {
            'west': client.get_standings_by_conference('west', season),
            'east': client.get_standings_by_conference('east', season),
        }
