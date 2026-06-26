#!/usr/bin/env python3
"""
足球联赛查询脚本 — 由聚合数据 (juhe.cn) 提供数据支持
查询足球联赛赛事赛程和积分榜

用法:
    python football_query.py --type zhongchao
    python football_query.py --type yingchao --rank

API Key 配置（任选其一，优先级从高到低）:
    1. 命令行参数：python football_query.py --key your_api_key ...
    2. 环境变量：export JUHE_FOOTBALL_KEY=your_api_key
    3. 脚本同目录的 .env 文件：JUHE_FOOTBALL_KEY=your_api_key

免费申请 API Key: https://www.juhe.cn/docs/api/id/90
"""

import sys
import os
import json
import urllib.request
import urllib.parse
from pathlib import Path

QUERY_API_URL = "http://apis.juhe.cn/fapig/football/query"
RANK_API_URL = "http://apis.juhe.cn/fapig/football/rank"
REGISTER_URL = "https://www.juhe.cn/docs/api/id/90"

# 联赛类型映射
LEAGUE_NAMES = {
    "zhongchao": "中超",
    "yingchao": "英超",
    "yijia": "意甲",
    "dejia": "德甲",
    "fajia": "法甲",
    "xijia": "西乙",
    "jiangsu": "苏超",
}


def load_api_key(cli_key: str = None) -> str:
    """按优先级加载 API Key"""
    if cli_key:
        return cli_key

    env_key = os.environ.get("JUHE_FOOTBALL_KEY", "").strip()
    if env_key:
        return env_key

    env_file = Path(__file__).parent / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("JUHE_FOOTBALL_KEY="):
                val = line.split("=", 1)[1].strip().strip('"').strip("'")
                if val:
                    return val

    return ""


def query_matches(league_type: str, api_key: str = None) -> dict:
    """查询联赛赛事赛程"""
    if not api_key:
        return {"success": False, "error": "未提供 API Key"}

    if not league_type:
        return {"success": False, "error": "未指定联赛类型"}

    params = {
        "key": api_key,
        "type": league_type,
    }
    url = f"{QUERY_API_URL}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "error": f"网络请求失败：{e}"}

    if result.get("error_code") == 0:
        res = result.get("result", {})
        return {
            "success": True,
            "title": res.get("title", ""),
            "duration": res.get("duration", ""),
            "matchs": res.get("matchs", []),
        }

    error_code = result.get("error_code", -1)
    reason = result.get("reason", "查询失败")
    hint = ""
    if error_code in (10001, 10002):
        hint = f"（请检查 API Key 是否正确，免费申请：{REGISTER_URL}）"
    elif error_code == 10012:
        hint = "（今日免费调用次数已用尽，请升级套餐）"

    return {"success": False, "error": f"{reason}{hint}", "error_code": error_code}


def query_ranking(league_type: str, api_key: str = None) -> dict:
    """查询联赛积分榜"""
    if not api_key:
        return {"success": False, "error": "未提供 API Key"}

    if not league_type:
        return {"success": False, "error": "未指定联赛类型"}

    params = {
        "key": api_key,
        "type": league_type,
    }
    url = f"{RANK_API_URL}?{urllib.parse.urlencode(params)}"

    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            result = json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        return {"success": False, "error": f"网络请求失败：{e}"}

    if result.get("error_code") == 0:
        res = result.get("result", {})
        return {
            "success": True,
            "title": res.get("title", ""),
            "duration": res.get("duration", ""),
            "ranking": res.get("ranking", []),
        }

    error_code = result.get("error_code", -1)
    reason = result.get("reason", "查询失败")
    hint = ""
    if error_code in (10001, 10002):
        hint = f"（请检查 API Key 是否正确，免费申请：{REGISTER_URL}）"
    elif error_code == 10012:
        hint = "（今日免费调用次数已用尽，请升级套餐）"
    elif error_code == 209001:
        hint = "（联赛类型参数错误）"
    elif error_code == 209002:
        hint = "（参数为空）"
    elif error_code == 209003:
        hint = "（网络异常）"

    return {"success": False, "error": f"{reason}{hint}", "error_code": error_code}


def format_matches_result(result: dict) -> str:
    """格式化赛事赛程结果"""
    if not result["success"]:
        return f"❌ 查询失败：{result.get('error', '未知错误')}"

    lines = []
    title = result.get("title", "足球联赛")
    duration = result.get("duration", "")
    lines.append(f"⚽ {title} ({duration})")
    lines.append("")

    matchs = result.get("matchs", [])
    if not matchs:
        return "⚽ 暂无赛事数据"

    for match_day in matchs:
        date = match_day.get("date", "")
        week = match_day.get("week", "")
        match_list = match_day.get("list", [])

        lines.append(f"📅 {date} {week}")
        lines.append("")

        for match in match_list:
            time_start = match.get("time_start", "")
            team1 = match.get("team1", "")
            team2 = match.get("team2", "")
            team1_score = match.get("team1_score", "-")
            team2_score = match.get("team2_score", "-")
            status_text = match.get("status_text", "")

            # 格式化比赛信息
            score_str = f"{team1_score} : {team2_score}" if status_text == "已完赛" else "vs"
            lines.append(f"   {time_start}  {team1} {score_str} {team2} [{status_text}]")

        lines.append("")

    return "\n".join(lines)


def format_ranking_result(result: dict) -> str:
    """格式化积分榜结果"""
    if not result["success"]:
        return f"❌ 查询失败：{result.get('error', '未知错误')}"

    lines = []
    title = result.get("title", "足球联赛")
    duration = result.get("duration", "")
    lines.append(f"⚽ {title} 积分榜 ({duration})")
    lines.append("")

    ranking = result.get("ranking", [])
    if not ranking:
        return "⚽ 暂无积分榜数据"

    # 表头
    header = f"{'排名':<4} {'球队':<12} {'场次':<4} {'胜':<3} {'平':<3} {'负':<3} {'进球':<4} {'失球':<4} {'净胜':<5} {'积分':<4}"
    sep = "—" * 70
    lines.append(sep)
    lines.append(header)
    lines.append(sep)

    for team in ranking:
        rank_id = team.get("rank_id", "")
        team_name = team.get("team", "")
        matches = team.get("matches", "")
        wins = team.get("wins", "")
        draw = team.get("draw", "")
        losses = team.get("losses", "")
        goals = team.get("goals", "")
        losing_goals = team.get("losing_goals", "")
        goal_diff = team.get("goal_difference", "")
        scores = team.get("scores", "")

        line = f"{rank_id:<4} {team_name:<12} {matches:<4} {wins:<3} {draw:<3} {losses:<3} {goals:<4} {losing_goals:<4} {goal_diff:<5} {scores:<4}"
        lines.append(line)

    lines.append(sep)

    return "\n".join(lines)


def main():
    args = sys.argv[1:]
    cli_key = None
    league_type = None
    rank_mode = False

    i = 0
    while i < len(args):
        if args[i] == "--key" and i + 1 < len(args):
            cli_key = args[i + 1]
            i += 2
        elif args[i] == "--type" and i + 1 < len(args):
            league_type = args[i + 1]
            i += 2
        elif args[i] == "--rank":
            rank_mode = True
            i += 1
        elif args[i] in ("--help", "-h"):
            print("用法：python football_query.py --type 联赛类型 [--rank] [--key API_KEY]")
            print("")
            print("选项:")
            print("  --type TYPE      联赛类型：zhongchao(中超)/yingchao(英超)/yijia(意甲)/")
            print("                   dejia(德甲)/fajia(法甲)/xijia(西乙)/jiangsu(苏超)")
            print("  --rank           查询积分榜（默认为赛程）")
            print("  --key KEY        API Key（可选，可用环境变量配置）")
            print("  --help, -h       显示帮助信息")
            print("")
            print("示例:")
            print("  python football_query.py --type zhongchao        # 查询中超赛程")
            print("  python football_query.py --type yingchao --rank  # 查询英超积分榜")
            print("")
            print(f"免费申请 API Key: {REGISTER_URL}")
            sys.exit(0)
        else:
            i += 1

    api_key = load_api_key(cli_key)
    if not api_key:
        print("❌ 未找到 API Key，请通过以下方式之一配置：")
        print("   1. 环境变量：export JUHE_FOOTBALL_KEY=your_api_key")
        print("   2. .env 文件：在脚本目录创建 .env，写入 JUHE_FOOTBALL_KEY=your_api_key")
        print("   3. 命令行参数：python football_query.py --key your_api_key --type zhongchao")
        print(f"\n免费申请 Key: {REGISTER_URL}")
        sys.exit(1)

    if not league_type:
        print("错误：缺少必填参数 --type")
        print("使用 --help 查看用法")
        sys.exit(1)

    if league_type not in LEAGUE_NAMES:
        print(f"错误：未知的联赛类型 '{league_type}'")
        print("支持的联赛类型：zhongchao(中超)/yingchao(英超)/yijia(意甲)/dejia(德甲)/fajia(法甲)/xijia(西乙)/jiangsu(苏超)")
        sys.exit(1)

    league_name = LEAGUE_NAMES.get(league_type, league_type)

    if rank_mode:
        # 查询积分榜
        result = query_ranking(league_type, api_key)
        print(format_ranking_result(result))
    else:
        # 查询赛程
        result = query_matches(league_type, api_key)
        print(format_matches_result(result))

    # 输出 JSON 数据
    print("")
    print("JSON 数据:")
    if rank_mode:
        result = query_ranking(league_type, api_key)
    else:
        result = query_matches(league_type, api_key)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
