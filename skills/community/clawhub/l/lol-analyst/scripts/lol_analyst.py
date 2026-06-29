"""
lol-analyst — 英雄联盟数据分析助手

主入口脚本，通过命令行参数支持多种查询模式：
  --profile    : 召唤师档案
  --matches    : 对局历史
  --analysis   : 综合分析
  --setup      : 配置 API Key
  --region     : 区域（默认 KR）
  --name       : Riot ID（name#tag 格式）
  --count      : 对局数量（默认 20）
  --output     : 输出文件路径
  --api-key    : API Key（可选，也可用环境变量/配置文件）
  --format     : 输出格式（html/json，默认 html）
"""
import argparse
import sys
import os
import json

# 添加 scripts 目录到 path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config_manager import (
    get_api_key, set_api_key, get_region_name,
    tier_cn, rank_cn, queue_cn,
)
from riot_client import RiotClient, get_champion_name
from report_generator import (
    generate_profile_html,
    generate_match_history_html,
    generate_analysis_html,
)


def parse_riot_id(riot_id: str):
    """解析 Riot ID: name#tag"""
    if "#" in riot_id:
        parts = riot_id.split("#", 1)
        return parts[0], parts[1]
    else:
        # 没有 tag 时默认使用区域代码作为 tag
        return riot_id, ""


def cmd_setup(api_key: str):
    """配置 API Key"""
    if not api_key:
        print("❌ 请提供 API Key")
        print("获取方式：访问 https://developer.riotgames.com/ 登录后自动生成")
        print("\n用法: lol-analyst --setup --api-key RGAPI-xxxxxxxx")
        return

    set_api_key(api_key)
    print("✅ API Key 已保存到配置文件")
    print(f"   位置: ~/.lol-analyst/config.json")
    print("\n现在可以开始查询了！例如：")
    print('   lol-analyst --profile --name "Faker#KR1" --region kr')


def cmd_profile(client: RiotClient, region: str, name: str, tag: str):
    """查询召唤师档案"""
    print(f"\n🔍 正在查询 {name}#{tag}（{get_region_name(region)}）...")

    try:
        # 获取召唤师信息
        account_data = client.get_summoner_by_name(region, name, tag)
        summoner = account_data["summoner"]

        # 获取排位数据
        ranked = client.get_ranked_stats(region, summoner["id"])

        # 获取英雄熟练度
        masteries = client.get_champion_masteries(region, summoner["puuid"], count=10)

        print(f"\n✅ 找到玩家！")
        print(f"   召唤师等级: {summoner.get('summonerLevel', '?')}")

        if ranked:
            for r in ranked:
                tier = tier_cn(r.get("tier", "?"))
                rank = rank_cn(r.get("rank", ""))
                queue = queue_cn(r.get("queueType", "?"))
                wins = r.get("wins", 0)
                losses = r.get("losses", 0)
                wr = round(wins / (wins + losses) * 100, 1) if (wins + losses) > 0 else 0
                print(f"   {queue}: {tier} {rank} ({wins}W/{losses}L, {wr}%)")
        else:
            print("   暂无排位数据")

        if masteries:
            print(f"\n   英雄熟练度 Top 5:")
            for m in masteries[:5]:
                champ = get_champion_name(m.get("championId", 0))
                level = m.get("championLevel", 0)
                pts = m.get("championPoints", 0)
                print(f"   - {champ}: {level}级 ({pts:,} 点)")

        return {
            "account": account_data["account"],
            "summoner": summoner,
            "ranked": ranked,
            "masteries": masteries,
        }

    except ValueError as e:
        print(f"\n❌ {e}")
        return None
    except Exception as e:
        print(f"\n❌ 查询失败: {e}")
        return None


def cmd_matches(client: RiotClient, region: str, name: str, tag: str,
                count: int = 20):
    """查询对局历史"""
    print(f"\n📜 正在查询 {name}#{tag} 最近 {count} 场对局...")

    try:
        # 获取 PUUID
        account_data = client.get_summoner_by_name(region, name, tag)
        puuid = account_data["summoner"]["puuid"]

        # 获取对局 ID 列表
        match_ids = client.get_match_history(region, puuid, count=count)
        print(f"   找到 {len(match_ids)} 场对局，正在获取详情...")

        # 批量获取对局详情
        matches = client.get_match_details_batch(region, match_ids, puuid)
        print(f"   成功获取 {len(matches)} 场对局详情")

        # 汇总统计
        if matches:
            wins = sum(1 for m in matches if m.get("win"))
            total_k = sum(m.get("kills", 0) for m in matches)
            total_d = sum(m.get("deaths", 0) for m in matches)
            total_a = sum(m.get("assists", 0) for m in matches)
            kda = round((total_k + total_a) / max(total_d, 1), 2)
            wr = round(wins / len(matches) * 100, 1)

            print(f"\n📊 汇总统计:")
            print(f"   胜率: {wr}% ({wins}W/{len(matches)-wins}L)")
            print(f"   场均 KDA: {kda}")
            print(f"   场均击杀/死亡/助攻: {total_k//len(matches)}/{total_d//len(matches)}/{total_a//len(matches)}")

        return matches

    except Exception as e:
        print(f"\n❌ 查询失败: {e}")
        return None


def cmd_analysis(client: RiotClient, region: str, name: str, tag: str,
                 count: int = 20):
    """生成综合分析报告"""
    print(f"\n📊 正在生成 {name}#{tag} 的综合分析报告...")

    # 获取基础数据
    profile = cmd_profile(client, region, name, tag)
    if not profile:
        return None

    matches = cmd_matches(client, region, name, tag, count)
    if matches is None:
        return None

    return {
        "profile": profile,
        "matches": matches,
    }


def main():
    parser = argparse.ArgumentParser(
        description="lol-analyst — 英雄联盟数据分析助手",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  lol-analyst --setup --api-key RGAPI-xxx      # 配置 API Key
  lol-analyst --profile --name "Faker#KR1"     # 查询召唤师档案
  lol-analyst --matches --name "Faker#KR1"     # 查询对局历史
  lol-analyst --analysis --name "Faker#KR1"    # 综合分析报告
  lol-analyst --profile --name "name#tag" --region euw1  # 指定区域
  lol-analyst --matches --name "name#tag" --count 10      # 指定对局数
        """
    )

    parser.add_argument("--setup", action="store_true", help="配置 API Key")
    parser.add_argument("--profile", action="store_true", help="查询召唤师档案")
    parser.add_argument("--matches", action="store_true", help="查询对局历史")
    parser.add_argument("--analysis", action="store_true", help="生成综合分析报告")
    parser.add_argument("--name", type=str, help="Riot ID (name#tag 格式)")
    parser.add_argument("--region", type=str, default="kr", help="区域代码 (默认: kr)")
    parser.add_argument("--count", type=int, default=20, help="对局数量 (默认: 20)")
    parser.add_argument("--api-key", type=str, help="Riot API Key")
    parser.add_argument("--output", type=str, help="输出文件路径")
    parser.add_argument("--format", type=str, default="html",
                        choices=["html", "json"], help="输出格式 (默认: html)")

    args = parser.parse_args()

    # --setup 模式
    if args.setup:
        cmd_setup(args.api_key or "")
        return

    # 需要 --name 参数的模式
    if not args.name:
        parser.print_help()
        print("\n❌ 请提供 --name 参数 (Riot ID, 格式: name#tag)")
        return

    name, tag = parse_riot_id(args.name)
    if not tag:
        # 自动使用区域代码作为 tag
        tag = args.region.upper()
        print(f"💡 未提供 tag，自动使用区域代码: {tag}")

    # 创建客户端
    try:
        client = RiotClient(args.api_key)
    except ValueError as e:
        print(f"\n❌ {e}")
        print("\n请先配置 API Key：")
        print("   lol-analyst --setup --api-key RGAPI-xxxxxxxx")
        return

    # 执行查询
    result = None
    mode = ""

    if args.analysis:
        result = cmd_analysis(client, args.region, name, tag, args.count)
        mode = "analysis"
    elif args.matches:
        result = cmd_matches(client, args.region, name, tag, args.count)
        mode = "matches"
    elif args.profile:
        result = cmd_profile(client, args.region, name, tag)
        mode = "profile"
    else:
        # 默认：显示 profile
        result = cmd_profile(client, args.region, name, tag)
        mode = "profile"

    if result is None:
        sys.exit(1)

    # 生成输出
    output_path = args.output

    if args.format == "json":
        json_output = json.dumps(result, ensure_ascii=False, indent=2)
        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(json_output)
            print(f"\n✅ JSON 已保存到: {output_path}")
        else:
            print("\n" + json_output)
    else:
        # HTML 格式
        if mode == "profile":
            summ = result["summoner"]
            rank = result.get("ranked", [])
            mast = result.get("masteries", [])
            data = {
                "account": result["account"],
                "summoner": summ,
                "ranked": rank,
                "masteries": mast,
            }
            html = generate_profile_html(data, args.region)
        elif mode == "matches":
            html = generate_match_history_html(
                f"{name}#{tag}", args.region, result,
                ""  # puuid not needed here
            )
        elif mode == "analysis":
            prof = result["profile"]
            summoner_level = prof.get("summoner", {}).get("summonerLevel", 0)
            html = generate_analysis_html(
                f"{name}#{tag}", args.region,
                prof, result["matches"], prof.get("masteries", []),
                summoner_level=summoner_level
            )
        else:
            html = "<html><body><h1>No data</h1></body></html>"

        if output_path:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"\n✅ HTML 报告已保存到: {output_path}")
        else:
            # 默认输出到临时文件
            output_path = f"lol_{mode}_{name}_{args.region}.html"
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(html)
            print(f"\n✅ HTML 报告已保存到: {os.path.abspath(output_path)}")

        return output_path


if __name__ == "__main__":
    result_path = main()
    if result_path:
        # 输出结果文件路径供 WorkBuddy 读取
        print(f"__OUTPUT_FILE__:{os.path.abspath(result_path)}")
