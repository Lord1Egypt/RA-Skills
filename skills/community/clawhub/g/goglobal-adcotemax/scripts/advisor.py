#!/usr/bin/env python3
"""Max全球升学路径顾问 - CLI入口"""
import sys

def cmd_help():
    print("🎓 Max Global Pathway Advisor - 可用命令")
    print("="*50)
    print("  destinations     列出所有升学目的地国家/地区")
    print("  pathway <国家>   查看特定国家的升学路径和要求")
    print("  match <条件>     根据条件推荐匹配的升学方向")
    print("  timeline <国家>  查看申请时间线")
    print("  requirements     通用申请要求概览")
    print("  help             帮助")
    print()
    print("示例: pathway 英国 | pathway 新加坡 | match 数学强 雅思6.5")

def cmd_destinations():
    print("🌍 升学目的地一览")
    print("="*50)
    print("🇬🇧 英国 — UCAS系统，3年本科")
    print("🇦🇺 澳洲 — 八大名校，移民友好")
    print("🇳🇿 新西兰 — 性价比高，工作签证灵活")
    print("🇭🇰 香港 — 港大/港中文/港科大，离家近")
    print("🇲🇴 澳门 — 葡语+英语双轨")
    print("🇸🇬 新加坡 — NUS/NTU，亚洲顶级")
    print("🇲🇾 马来西亚 — 英澳分校，成本1/3")
    print("🇰🇷 韩国 — SKY联盟，文化输出强")
    print("🇯🇵 日本 — SGU英文项目，37所大学")
    print("🇹🇭 泰国 — 国际学校路径，性价比")

def cmd_pathway(country):
    pathways = {
        "英国": "🇬🇧 英国升学\nA-Level: 3A（牛剑需A*AA+）\n雅思: 6.5-7.5\nUCAS截止: 10月15日(牛剑)/1月14日(常规)\nPS: 2027年起改为3个结构化问题\n签证: Student Route Visa\n毕业后: Graduate Route 2年工签",
        "香港": "🇭🇰 香港升学\nA-Level: 3A（港大）\n雅思: 6.5+\n方式: 自主招生（港大/港科大等）/统招提前批（港中文/港城大）\n学费: 约18万港币/年\n新趋势: 港大新增11个本科专业+2学院",
        "新加坡": "🇸🇬 新加坡升学\nA-Level: 3A（含数学）\n雅思: 6.5+\n竞争: NUS录取率5-8%\n截止: 约每年2月\n新政策: 2027年起所有学生必修AI课程",
        "日本": "🇯🇵 日本升学(SGU)\n方式: 37所大学英文授课，无需日语N1\nA-Level/IB/SAT 均可\n雅思: 6.0+ / 托福80+\n新兴专业: AI治理、生成式AI与创意计算",
        "澳洲": "🇦🇺 澳洲升学\nA-Level: 6-9分（换算制）\n雅思: 6.5-7.0\n移民: AI/数据科学入技能短缺长名单\n学制: 3年本科"
    }
    for k, v in pathways.items():
        if k in country:
            print(v)
            return
    print(f"查看完整信息请运行: pathway <国家名>")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("help","--help","-h"):
        cmd_help()
        return
    cmd = sys.argv[1]
    if cmd == "destinations":
        cmd_destinations()
    elif cmd == "pathway":
        cmd_pathway(" ".join(sys.argv[2:]) if len(sys.argv) > 2 else "")
    elif cmd == "match":
        print("匹配功能: 请提供具体条件")
    elif cmd == "timeline" or cmd == "requirements":
        print("请指定国家，如: timeline 英国")
    else:
        cmd_help()

if __name__ == "__main__":
    main()
