"""
NBA Analyst — 主入口模块
路由用户请求到对应业务模块
"""

import sys
from .scoreboard import get_scoreboard, get_live_scoreboard
from .standings import get_standings
from .players import query_player, query_player_recent, query_player_shot_chart, search_players
from .teams import query_team, query_team_schedule, query_team_roster, search_teams
from .compare import compare_players, compare_teams


def run(command: str, *args) -> str:
    """执行 NBA 命令

    Args:
        command: 命令名 (scoreboard, standings, player, team, compare, search, report)
        args: 命令参数

    Returns:
        格式化结果文本
    """
    cmd = command.lower().strip()

    if cmd in ('scoreboard', '比分', 'sb'):
        live = '--live' in args or '-l' in args
        if live:
            return get_live_scoreboard()
        date_str = args[0] if args and not args[0].startswith('-') else None
        return get_scoreboard(date_str)

    elif cmd in ('standings', '排名', 'st'):
        conf = None
        for a in args:
            a_lower = a.lower()
            if a_lower in ('west', '西部', '西'):
                conf = 'west'
            elif a_lower in ('east', '东部', '东'):
                conf = 'east'
        return get_standings(conf)

    elif cmd in ('player', '球员', 'p'):
        if not args:
            return "用法: /nba player <球员名> [recent|shot|search]"

        name = args[0]
        sub = args[1].lower() if len(args) > 1 else 'info'
        n = int(args[2]) if len(args) > 2 and args[2].isdigit() else 10

        if sub in ('recent', 're', '最近', '近期', 'r'):
            return query_player_recent(name, n)
        elif sub in ('shot', '投篮', 'sh', '投篮图'):
            return query_player_shot_chart(name)
        elif sub in ('search', '搜索', 's'):
            return search_players(name)
        else:
            return query_player(name)

    elif cmd in ('team', '球队', 't'):
        if not args:
            return "用法: /nba team <球队名> [schedule|roster|search]"

        name = args[0]
        sub = args[1].lower() if len(args) > 1 else 'info'
        n = int(args[2]) if len(args) > 2 and args[2].isdigit() else 10

        if sub in ('schedule', 'sc', '赛程', 's'):
            return query_team_schedule(name, n=n)
        elif sub in ('roster', 'ro', '阵容', 'r'):
            return query_team_roster(name)
        elif sub in ('search', '搜索', 'se'):
            return search_teams(name)
        else:
            return query_team(name)

    elif cmd in ('compare', '对比', 'comp', 'c'):
        if len(args) < 2:
            return "用法: /nba compare <球员1/球队1> <球员2/球队2>"

        # 判断是球员还是球队
        name1, name2 = args[0], args[1]

        # 简单启发: 含中文字符且是球队名
        from .i18n import I18N
        i18n = I18N()

        # 尝试判断类型
        p1_is_player = False
        for p in i18n.players_cn.values():
            if name1 in p or p in name1:
                p1_is_player = True
                break

        if p1_is_player:
            return compare_players(name1, name2)
        else:
            return compare_teams(name1, name2)

    elif cmd in ('search', '搜索'):
        if not args:
            return "用法: /nba search <球员名或球队名>"
        q = args[0]
        p_result = search_players(q)
        t_result = search_teams(q)
        return f"{p_result}\n\n{t_result}"

    elif cmd in ('report', '报告', 'r'):
        from .report import generate_player_report, generate_team_report, generate_today_report

        if not args:
            return "用法: /nba report <球员名|team 球队名|today>"

        if args[0].lower() in ('today', '今天', '今日'):
            return generate_today_report()
        elif args[0].lower() in ('team', 't'):
            if len(args) < 2:
                return "用法: /nba report team <球队名>"
            return generate_team_report(args[1])
        else:
            return generate_player_report(args[0])

    elif cmd in ('draft', '选秀', 'd'):
        if not args:
            return "用法: /nba draft <年份> (如: /nba draft 2025)"
        from .nba_client import NBAClient
        client = NBAClient()
        year = int(args[0])
        picks = client.get_draft_history(year)
        if not picks:
            return f"❌ 暂无 {year} 年选秀数据"

        lines = [f"🏀 {year} 年 NBA 选秀结果", "=" * 60, ""]
        for p in picks[:30]:  # 首轮
            lines.append(f"  #{p['pick']:<4} {p['team']:<22} {p['name']}")
        return '\n'.join(lines)

    elif cmd in ('leaders', '领先者', 'l'):
        stat = args[0] if args else 'PTS'
        top = int(args[1]) if len(args) > 1 else 10
        from .nba_client import NBAClient
        client = NBAClient()
        leaders = client.get_league_leaders(stat, top=top)
        from .i18n import I18N
        i18n = I18N()

        lines = [f"🏀 NBA 数据领先者 — {stat}", "=" * 50]
        for l in leaders:
            cn = i18n.player_en_to_cn(l['name'])
            team_cn = i18n.team_en_to_cn(l['team'])
            name_str = f"{cn} ({l['name']})" if cn != l['name'] else l['name']
            lines.append(f"  #{l['rank']:<3} {name_str:<30} {l['value']}")
        return '\n'.join(lines)

    elif cmd in ('help', '帮助', 'h', '?'):
        return _help_text()

    else:
        return f"未知命令: {command}\n\n{_help_text()}"


def _help_text() -> str:
    return """🏀 NBA Analyst — 帮助

可用命令:

  比分:
    /nba scoreboard           今日比分
    /nba scoreboard --live    实时比分

  排名:
    /nba standings            全联盟排名
    /nba standings west       西部排名
    /nba standings east       东部排名

  球员:
    /nba player <名>           球员信息+生涯数据
    /nba player <名> recent N  最近N场表现
    /nba player <名> shot      投篮分布

  球队:
    /nba team <名>            球队信息+赛季统计
    /nba team <名> schedule N  赛程(最近N场)
    /nba team <名> roster     球队阵容

  对比:
    /nba compare A B          球员/球队对比

  报告:
    /nba report <球员名>      生成球员HTML报告
    /nba report team <球队名> 生成球队HTML报告
    /nba report today         今日比赛报告

  其他:
    /nba leaders PTS 10       数据领先者
    /nba draft 2025           选秀结果
    /nba search <关键词>      搜索球员/球队
    /nba help                 显示此帮助"""
