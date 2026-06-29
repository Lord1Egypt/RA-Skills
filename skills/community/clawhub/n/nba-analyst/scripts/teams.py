"""
球队模块 — 查询球队信息、赛季统计、赛程、阵容
"""

from .nba_client import NBAClient
from .i18n import I18N

client = NBAClient()
i18n = I18N()


def query_team(name: str, season: str = '2025-26') -> str:
    """查询球队基本信息 + 赛季统计

    Args:
        name: 球队名（中英文均可）
        season: 赛季

    Returns:
        格式化球队信息文本
    """
    try:
        en_name, cn_name = i18n.resolve_team_name(name)
        team_id = client.get_team_id(en_name)

        if not team_id:
            return f"❌ 未找到球队: {name}"

        info = client.get_team_info(team_id)
        stats = client.get_team_season_stats(team_id, season)

        lines = [f"🏀 {cn_name} ({en_name})", "=" * 50, ""]

        if info:
            conf_cn = '西部' if info.get('conference') == 'West' else '东部'
            lines.append(f"  城市: {info.get('city', 'N/A')}")
            lines.append(f"  分区: {conf_cn} {info.get('division', '')}")
            lines.append(f"  成立: {info.get('founded', 'N/A')}年")
            lines.append("")

        if stats:
            lines.append(f"📊 {season} 赛季数据:")
            lines.append("-" * 50)
            lines.append(f"  战绩: {stats.get('w', 0)}胜 - {stats.get('l', 0)}负  (胜率 {stats.get('win_pct', 0):.3f})")
            lines.append(f"  场均得分: {stats.get('pts', 0):.1f}  |  场均失分: —")
            lines.append(f"  篮板: {stats.get('reb', 0):.1f}  |  助攻: {stats.get('ast', 0):.1f}")
            lines.append(f"  抢断: {stats.get('stl', 0):.1f}  |  盖帽: {stats.get('blk', 0):.1f}")
            lines.append("")
            lines.append(f"  投篮命中率: {stats.get('fg_pct', 0):.1f}%")
            lines.append(f"  三分命中率: {stats.get('fg3_pct', 0):.1f}%")
            lines.append(f"  罚球命中率: {stats.get('ft_pct', 0):.1f}%")
            lines.append("")
            lines.append(f"  进攻效率: {stats.get('off_rtg', 0):.1f}  |  防守效率: {stats.get('def_rtg', 0):.1f}")
            lines.append(f"  净效率: {stats.get('net_rtg', 0):.1f}  |  节奏: {stats.get('pace', 0):.1f}")

        return '\n'.join(lines)

    except Exception as e:
        return f"❌ 查询球队失败: {e}"


def query_team_schedule(name: str, season: str = '2025-26', n: int = 10) -> str:
    """查询球队赛程

    Args:
        name: 球队名
        season: 赛季
        n: 比赛场次

    Returns:
        格式化赛程文本
    """
    try:
        en_name, cn_name = i18n.resolve_team_name(name)
        team_id = client.get_team_id(en_name)

        if not team_id:
            return f"❌ 未找到球队: {name}"

        games = client.get_team_schedule(team_id, season, n)

        lines = [f"🏀 {cn_name} — 最近 {len(games)} 场比赛", "=" * 60, ""]
        lines.append(f"{'日期':<12} {'对阵':<30} {'得分':<6} {'失分':<6} {'结果'}")
        lines.append("-" * 60)

        for g in games:
            matchup = g['matchup']
            result = '✅胜' if g['wl'] == 'W' else '❌负'
            lines.append(
                f"{g['date']:<12} {matchup:<30} "
                f"{g['pts']:<6} {g['pts'] + g.get('opp_pts', 0):<6} {result}"
            )

        return '\n'.join(lines)

    except Exception as e:
        return f"❌ 查询赛程失败: {e}"


def query_team_roster(name: str, season: str = '2025-26') -> str:
    """查询球队阵容

    Args:
        name: 球队名
        season: 赛季

    Returns:
        格式化阵容文本
    """
    try:
        en_name, cn_name = i18n.resolve_team_name(name)
        team_id = client.get_team_id(en_name)

        if not team_id:
            return f"❌ 未找到球队: {name}"

        players_list = client.get_team_roster(team_id, season)

        if not players_list:
            return f"❌ 未找到 {cn_name} 的阵容数据"

        lines = [f"🏀 {cn_name} 阵容 — {season} 赛季", "=" * 60, ""]
        lines.append(f"{'号码':<5} {'球员':<25} {'位置':<6} {'身高':<6} {'经验':<4}")
        lines.append("-" * 60)

        for p in players_list:
            name_cn = i18n.player_en_to_cn(p['name'])
            name_str = f"{name_cn} ({p['name']})" if name_cn != p['name'] else p['name']
            lines.append(
                f"{p['number']:<5} {name_str:<25} {p['position']:<6} "
                f"{p['height']:<6} {p['experience']:<4}"
            )

        return '\n'.join(lines)

    except Exception as e:
        return f"❌ 查询阵容失败: {e}"


def search_teams(keyword: str) -> str:
    """搜索球队"""
    try:
        results = client.find_team(keyword)
        if not results:
            return f"❌ 未找到匹配球队: {keyword}"

        lines = [f"🔍 搜索 '{keyword}' 结果:", "=" * 50]
        for t in results[:15]:
            cn = i18n.team_en_to_cn(t['full_name'])
            lines.append(f"  {cn} ({t['full_name']}) — {t.get('abbreviation', '')}")

        return '\n'.join(lines)

    except Exception as e:
        return f"❌ 搜索球队失败: {e}"
