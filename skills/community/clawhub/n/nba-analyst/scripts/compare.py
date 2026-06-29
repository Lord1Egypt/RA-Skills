"""
对比模块 — 球员/球队对比分析
"""

from .nba_client import NBAClient
from .i18n import I18N

client = NBAClient()
i18n = I18N()


def compare_players(name1: str, name2: str, season: str = '2025-26') -> str:
    """对比两个球员

    Args:
        name1: 球员1（中英文均可）
        name2: 球员2（中英文均可）
        season: 赛季

    Returns:
        格式化对比文本
    """
    try:
        en1, cn1 = i18n.resolve_player_name(name1)
        en2, cn2 = i18n.resolve_player_name(name2)

        id1 = client.get_player_id(en1)
        id2 = client.get_player_id(en2)

        if not id1:
            return f"❌ 未找到球员: {name1}"
        if not id2:
            return f"❌ 未找到球员: {name2}"

        data = client.compare_players(id1, id2)
        p1 = data.get('player_1', {})
        p2 = data.get('player_2', {})

        if not p1 or not p2:
            # Fallback: 获取生涯最新赛季数据
            from .players import query_player as query_p
            p1_str = query_p(name1, season)
            p2_str = query_p(name2, season)
            return f"📊 球员对比\n{'='*60}\n\n{p1_str}\n\n{'='*60}\n\n{p2_str}"

        lines = [f"🏀 球员对比: {cn1} vs {cn2}", "=" * 70, ""]

        # 表头
        label_w = 18
        lines.append(f"{'指标':<{label_w}} {cn1:<20} {cn2:<20} {'差异':>10}")
        lines.append("-" * 70)

        # 对比指标
        stats_to_compare = [
            ('PTS', '得分'), ('REB', '篮板'), ('AST', '助攻'),
            ('STL', '抢断'), ('BLK', '盖帽'), ('TOV', '失误'),
            ('MIN', '上场时间'), ('GP', '出场数'),
        ]

        for key, label in stats_to_compare:
            v1 = float(p1.get(key, 0) or 0)
            v2 = float(p2.get(key, 0) or 0)
            diff = v1 - v2
            diff_str = f"+{diff:.1f}" if diff > 0 else f"{diff:.1f}"
            winner = "◀" if diff > 0 else ("▶" if diff < 0 else "=")
            lines.append(f"{label:<{label_w}} {v1:<20.1f} {v2:<20.1f} {diff_str:<10} {winner}")

        # 命中率对比
        lines.append("")
        lines.append(f"{'命中率':<{label_w}} {cn1:<20} {cn2:<20} {'差异':>10}")
        lines.append("-" * 70)

        pct_stats = [('FG_PCT', '投篮%'), ('FG3_PCT', '三分%'), ('FT_PCT', '罚球%')]
        for key, label in pct_stats:
            v1 = float(p1.get(key, 0) or 0)
            v2 = float(p2.get(key, 0) or 0)
            v1_pct = v1 * 100 if v1 < 1 else v1
            v2_pct = v2 * 100 if v2 < 1 else v2
            diff = v1_pct - v2_pct
            diff_str = f"+{diff:.1f}%" if diff > 0 else f"{diff:.1f}%"
            winner = "◀" if diff > 0 else ("▶" if diff < 0 else "=")
            lines.append(f"{label:<{label_w}} {v1_pct:<19.1f}% {v2_pct:<19.1f}% {diff_str:<10} {winner}")

        return '\n'.join(lines)

    except Exception as e:
        return f"❌ 球员对比失败: {e}"


def compare_teams(name1: str, name2: str, season: str = '2025-26') -> str:
    """对比两个球队

    Args:
        name1: 球队1
        name2: 球队2
        season: 赛季

    Returns:
        格式化对比文本
    """
    try:
        en1, cn1 = i18n.resolve_team_name(name1)
        en2, cn2 = i18n.resolve_team_name(name2)

        id1 = client.get_team_id(en1)
        id2 = client.get_team_id(en2)

        if not id1:
            return f"❌ 未找到球队: {name1}"
        if not id2:
            return f"❌ 未找到球队: {name2}"

        s1 = client.get_team_season_stats(id1, season)
        s2 = client.get_team_season_stats(id2, season)

        if not s1 or not s2:
            return f"❌ 无法获取球队数据"

        lines = [f"🏀 球队对比: {cn1} vs {cn2}", "=" * 70, ""]

        # 战绩
        lines.append(f"{'战绩':<18} {cn1:<20} {cn2:<20}")
        lines.append("-" * 70)
        lines.append(f"{'胜-负':<18} {s1.get('w',0):<20} {s2.get('w',0):<20}")
        lines.append(f"{'胜率':<18} {s1.get('win_pct',0):<20.3f} {s2.get('win_pct',0):<20.3f}")
        lines.append("")

        # 攻防
        lines.append(f"{'进攻':<18} {cn1:<20} {cn2:<20} {'差异':>10}")
        lines.append("-" * 70)

        stat_items = [
            ('pts', '场均得分'), ('reb', '场均篮板'), ('ast', '场均助攻'),
            ('stl', '场均抢断'), ('blk', '场均盖帽'), ('tov', '场均失误'),
        ]
        for key, label in stat_items:
            v1 = s1.get(key, 0)
            v2 = s2.get(key, 0)
            diff = v1 - v2
            diff_str = f"+{diff:.1f}" if diff > 0 else f"{diff:.1f}"
            lines.append(f"{label:<18} {v1:<20.1f} {v2:<20.1f} {diff_str:<10}")

        lines.append("")
        lines.append(f"{'命中率':<18} {cn1:<20} {cn2:<20} {'差异':>10}")
        lines.append("-" * 70)
        for key, label in [('fg_pct', '投篮%'), ('fg3_pct', '三分%'), ('ft_pct', '罚球%')]:
            v1 = s1.get(key, 0)
            v2 = s2.get(key, 0)
            diff = v1 - v2
            diff_str = f"+{diff:.1f}%" if diff > 0 else f"{diff:.1f}%"
            lines.append(f"{label:<18} {v1:<19.1f}% {v2:<19.1f}% {diff_str:<10}")

        lines.append("")
        lines.append(f"{'效率':<18} {cn1:<20} {cn2:<20} {'差异':>10}")
        lines.append("-" * 70)
        for key, label in [('off_rtg', '进攻效率'), ('def_rtg', '防守效率'), ('net_rtg', '净效率'), ('pace', '节奏')]:
            v1 = s1.get(key, 0)
            v2 = s2.get(key, 0)
            diff = v1 - v2
            diff_str = f"+{diff:.1f}" if diff > 0 else f"{diff:.1f}"
            lines.append(f"{label:<18} {v1:<20.1f} {v2:<20.1f} {diff_str:<10}")

        # 交锋记录
        lines.append("")
        lines.append(f"📋 近期交锋记录:")
        try:
            matchups = client.get_matchup_history(id1, id2, season)
            if matchups:
                for m in matchups[:5]:
                    result = '✅' if m['wl'] == 'W' else '❌'
                    lines.append(f"  {m['date']} {m['matchup']} {result}")
            else:
                lines.append("  (暂无交锋数据)")
        except:
            lines.append("  (暂无交锋数据)")

        return '\n'.join(lines)

    except Exception as e:
        return f"❌ 球队对比失败: {e}"
