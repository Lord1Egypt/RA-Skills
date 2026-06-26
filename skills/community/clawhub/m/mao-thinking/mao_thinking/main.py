#!/usr/bin/env python3
"""
毛泽东思想实践工具包 - 主入口

用法:
    python mao_thinking.py <command> [options]
    
Commands:
    analyze   - 矛盾分析：分析问题的主要矛盾
    decide    - 决策助手：结合群众路线做决策  
    situation - 形势分析：战略藐视 vs 战术重视
    summary   - 核心原则汇总
    principle - 查看特定原则详情
    
Examples:
    python mao_thinking.py analyze "项目延期" "需求变更" "人手不足"
    python mao_thinking.py situation "面临竞争" 6 8
    python mao_thinking.py decide "选择哪份工作"
    python mao_thinking.py summary
    python mao_thinking.py principle 矛盾论
    python mao_thinking.py --scenario "团队意见不统一"
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mao_thinking.analyzer import analyze_contradiction
from mao_thinking.situator import situation_analysis
from mao_thinking.decider import mass_line_decide, decide_interactive
from mao_thinking.summary import show_summary, get_principle, get_principle_by_scenario


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        show_summary()
        sys.exit(1)
    
    command = sys.argv[1]
    
    # 矛盾分析
    if command == "analyze":
        problem = sys.argv[2] if len(sys.argv) > 2 else "待分析问题"
        factors = sys.argv[3:] if len(sys.argv) > 3 else []
        if not factors:
            print("错误: 需要提供影响因素")
            sys.exit(1)
        analyze_contradiction(problem, factors)
    
    # 形势分析
    elif command == "situation":
        situation = sys.argv[2] if len(sys.argv) > 2 else "待分析形势"
        our = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        enemy = int(sys.argv[4]) if len(sys.argv) > 4 else 8
        situation_analysis(situation, our, enemy)
    
    # 决策助手
    elif command == "decide":
        decision = sys.argv[2] if len(sys.argv) > 2 else "待决策问题"
        decide_interactive(decision)
    
    # 原则汇总
    elif command == "summary":
        show_summary()
    
    # 查看特定原则
    elif command == "principle":
        name = sys.argv[2] if len(sys.argv) > 2 else None
        if name:
            info = get_principle(name)
            print(f"\n🔹 {name}")
            for k, v in info.items():
                print(f"   {k}: {v}")
        else:
            print("用法: python mao_thinking.py principle <原则名>")
    
    # 场景推荐
    elif command == "--scenario" or command == "-s":
        scenario = sys.argv[2] if len(sys.argv) > 2 else "一般问题"
        result = get_principle_by_scenario(scenario)
        print(f"\n🎯 场景: {result['场景']}")
        print(f"📌 推荐原则: {result['推荐原则']}")
        print(f"\n详细信息:")
        for k, v in result["详细信息"].items():
            print(f"   {k}: {v}")
    
    else:
        print(f"未知命令: {command}")
        print(__doc__)


if __name__ == "__main__":
    main()