"""
球员模块 — 查询球员信息、生涯数据、近期状态、投篮图
"""

from .nba_client import NBAClient
from .i18n import I18N

client = NBAClient()
i18n = I18N()


def query_player(name: str, season: str = '2025-26') -> str:
    """查询球员基本信息 + 生涯数据

    Args:
        name: 球员名（中英文均可）
        season: 赛季

    Returns:
        格式化的球员信息文本
    """
    try:
        en_name, cn_name = i18n.resolve_player_name(name)
        player_id = client.get_player_id(en_name)

        if not player_id:
            return f"❌ 未找到球员: {name}"

        info = client.get_player_info(player_id)
        career = client.get_player_career_stats(player_id)

        lines = [f"🏀 {cn_name} ({en_name})", "=" * 50, ""]

        if info:
            team_cn = i18n.team_en_to_cn(info.get('team', ''))
            lines.append(f"  球队: {team_cn or info.get('team', 'N/A')}")
            lines.append(f"  位置: {info.get('position', 'N/A')}")
            lines.append(f"  身高: {info.get('height', 'N/A')} | 体重: {info.get('weight', 'N/A')} 磅")
            lines.append(f"  球衣号: #{info.get('jersey', 'N/A')}")
            lines.append(f"  经验: {info.get('experience', 'N/A')}赛季")
            if info.get('college'):
                lines.append(f"  大学: {info.get('college', 'N/A')}")
            if info.get('draft_year'):
                lines.append(f"  选秀: {info.get('draft_year', '')} 年第 {info.get('draft_round', '')} 轮第 {info.get('draft_number', '')} 顺位")
            lines.append("")

        if career is not None and not career.empty:
            lines.append("📊 生涯场均数据:")
            lines.append("-" * 50)
            latest = career.iloc[-1]
            stats = [
                ('pts', '得分'), ('reb', '篮板'), ('ast', '助攻'),
                ('stl', '抢断'), ('blk', '盖帽'), ('tov', '失误'),
            ]
            stat_parts = []
            for key, label in stats:
                val = latest.get(key.upper(), 0)
                stat_parts.append(f"{label} {val}")
            lines.append("  " + " | ".join(stat_parts))

            lines.append("")
            pct_stats = [
                ('fg_pct', '投篮命中率'), ('fg3_pct', '三分命中率'), ('ft_pct', '罚球命中率'),
            ]
            pct_parts = []
            for key, label in pct_stats:
                val = latest.get(key.upper(), 0)
                pct_parts.append(f"{label} {val*100:.1f}%")
            lines.append("  " + " | ".join(pct_parts))

            # 赛季数
            seasons = len(career)
            lines.append(f"\n  📅 已征战 {seasons} 个赛季")

        return '\n'.join(lines)

    except Exception as e:
        return f"❌ 查询球员失败: {e}"


def query_player_recent(name: str, n: int = 10, season: str = '2025-26') -> str:
    """查询球员最近 N 场比赛 + 滚动均值

    Args:
        name: 球员名
        n: 最近场次
        season: 赛季

    Returns:
        格式化的近期表现文本
    """
    try:
        en_name, cn_name = i18n.resolve_player_name(name)
        player_id = client.get_player_id(en_name)

        if not player_id:
            return f"❌ 未找到球员: {name}"

        data = client.get_player_recent_games(player_id, n, season)

        lines = [f"🏀 {cn_name} — 最近 {n} 场表现", "=" * 60, ""]

        # 场均
        avgs = data.get('averages', {})
        if avgs:
            lines.append("📊 场均数据:")
            lines.append(f"  得分 {avgs.get('PTS', 0):.1f} | 篮板 {avgs.get('REB', 0):.1f} | 助攻 {avgs.get('AST', 0):.1f}")
            lines.append(f"  抢断 {avgs.get('STL', 0):.1f} | 盖帽 {avgs.get('BLK', 0):.1f} | 失误 {avgs.get('TOV', 0):.1f}")
            if 'FG_PCT' in avgs:
                lines.append(f"  命中率: FG {avgs['FG_PCT']}% | 3P {avgs.get('FG3_PCT', '-')}% | FT {avgs.get('FT_PCT', '-')}%")
            lines.append("")

        # 每场数据
        lines.append("📋 比赛详情:")
        lines.append(f"{'日期':<12} {'对阵':<30} {'得分':<6} {'篮板':<6} {'助攻':<6} {'±':<6} {'结果'}")
        lines.append("-" * 80)

        for g in data.get('games', []):
            matchup_parts = g['matchup'].split(' ')
            opp = matchup_parts[-1] if len(matchup_parts) > 1 else g['matchup']
            opp_cn = i18n.team_en_to_cn(opp)

            result = '✅胜' if g['wl'] == 'W' else '❌负'
            lines.append(
                f"{g['date']:<12} {opp_cn or g['matchup']:<30} "
                f"{g['pts']:<6} {g['reb']:<6} {g['ast']:<6} {g['plus_minus']:<6} {result}"
            )

        return '\n'.join(lines)

    except Exception as e:
        return f"❌ 查询近期表现失败: {e}"


def query_player_shot_chart(name: str, season: str = '2025-26') -> str:
    """查询球员投篮热力图总结

    Args:
        name: 球员名
        season: 赛季

    Returns:
        投篮表现总结文本
    """
    try:
        en_name, cn_name = i18n.resolve_player_name(name)
        player_id = client.get_player_id(en_name)

        if not player_id:
            return f"❌ 未找到球员: {name}"

        data = client.get_shot_chart(player_id, season)
        summary = data.get('summary', {})

        lines = [f"🏀 {cn_name} — 投篮分布 ({season} 赛季)", "=" * 50, ""]
        lines.append(f"  总出手: {summary.get('total', 0)}")
        lines.append(f"  命中: {summary.get('made', 0)}")
        lines.append(f"  整体命中率: {summary.get('fg_pct', 0)}%")
        lines.append("")
        lines.append(f"  三分出手: {summary.get('fg3_total', 0)}")
        lines.append(f"  三分命中: {summary.get('fg3_made', 0)}")
        lines.append(f"  三分命中率: {summary.get('fg3_pct', 0)}%")

        # 按区域统计
        if data.get('shots'):
            zone_count = {}
            zone_made = {}
            for s in data['shots']:
                zone = s.get('zone', '其他')
                zone_count[zone] = zone_count.get(zone, 0) + 1
                if s['made']:
                    zone_made[zone] = zone_made.get(zone, 0) + 1

            lines.append("")
            lines.append("📊 区域命中率:")
            for zone in sorted(zone_count.keys()):
                total = zone_count[zone]
                made = zone_made.get(zone, 0)
                pct = made / total * 100 if total > 0 else 0
                bar = '█' * int(pct / 5) + '░' * (20 - int(pct / 5))
                lines.append(f"  {zone:<12} {bar} {pct:.1f}% ({made}/{total})")

        return '\n'.join(lines)

    except Exception as e:
        return f"❌ 查询投篮数据失败: {e}"


def search_players(keyword: str) -> str:
    """模糊搜索球员"""
    try:
        # 先尝试中文→英文
        en_name, cn_name = i18n.resolve_player_name(keyword)
        if en_name != keyword:
            results = client.find_player(en_name)
        else:
            results = client.find_player(keyword)

        if not results:
            return f"❌ 未找到匹配球员: {keyword}"

        lines = [f"🔍 搜索 '{keyword}' 结果:", "=" * 50]
        for p in results[:15]:
            cn = i18n.player_en_to_cn(p['full_name'])
            name_str = f"{cn} ({p['full_name']})" if cn != p['full_name'] else p['full_name']
            lines.append(f"  {name_str} — ID: {p['id']}")

        return '\n'.join(lines)

    except Exception as e:
        return f"❌ 搜索球员失败: {e}"
