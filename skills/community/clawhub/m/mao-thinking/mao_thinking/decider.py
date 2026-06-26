#!/usr/bin/env python3
"""
群众路线决策助手 - 基于毛泽东《群众路线》的决策工具

核心思想：
- 从群众中来，到群众中去
- 一切为了群众，一切依靠群众
- 集中起来，坚持下去

用法:
    python decider.py "决策问题" '[{"name":"方案A","pros":["优点1"],"cons":["缺点1"]},{"name":"方案B",...}]'
    
或作为模块导入:
    from decider import mass_line_decide
    result = mass_line_decide("选择哪份工作", options)
"""

import sys
import json
from typing import List, Dict, Any, Optional


# 评分权重
WEIGHTS = {
    "pros": 10,    # 每个优点加10分
    "cons": -5,    # 每个缺点减5分
    "base": 50     # 基础分
}


class DecisionOption:
    """决策选项类"""
    def __init__(self, name: str, pros: List[str] = None, cons: List[str] = None, 
                 support_rate: float = 0.5, feasibility: int = 5):
        self.name = name
        self.pros = pros or []
        self.cons = cons or []
        self.support_rate = support_rate  # 群众支持率 0-1
        self.feasibility = feasibility    # 可行性 1-10
    
    def score(self) -> int:
        """计算得分"""
        score = WEIGHTS["base"]
        score += len(self.pros) * WEIGHTS["pros"]
        score += len(self.cons) * WEIGHTS["cons"]
        score += int(self.support_rate * 20)  # 支持率加权
        score += self.feasibility             # 可行性加权
        return score
    
    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "pros": self.pros,
            "cons": self.cons,
            "support_rate": self.support_rate,
            "feasibility": self.feasibility,
            "score": self.score()
        }


def mass_line_decide(
    decision: str, 
    options: List[Dict[str, Any]],
    include_analysis: bool = True
) -> Dict[str, Any]:
    """
    群众路线决策助手
    
    Args:
        decision: 决策问题描述
        options: 方案列表，每个方案包含:
            - name: 方案名称
            - pros: 优点列表
            - cons: 缺点列表
            - support_rate: 群众支持率 (0-1，可选)
            - feasibility: 可行性 (1-10，可选)
        include_analysis: 是否包含详细分析
    
    Returns:
        决策建议字典
    
    Example:
        >>> options = [
        ...     {"name": "大厂", "pros": ["工资高", "平台大"], "cons": ["加班多"]},
        ...     {"name": "创业", "pros": ["成长快"], "cons": ["风险高"]}
        ... ]
        >>> result = mass_line_decide("选择哪份工作", options)
        >>> print(result["推荐方案"])
        大厂
    """
    if not options:
        return {
            "status": "error",
            "message": "需要提供至少一个方案"
        }
    
    print(f"\n🤝 群众路线决策：{decision}")
    print("=" * 50)
    
    # 解析选项
    decision_options = []
    for opt in options:
        if isinstance(opt, dict):
            decision_options.append(DecisionOption(
                name=opt.get("name", "未命名"),
                pros=opt.get("pros", []),
                cons=opt.get("cons", []),
                support_rate=opt.get("support_rate", 0.5),
                feasibility=opt.get("feasibility", 5)
            ))
        elif isinstance(opt, DecisionOption):
            decision_options.append(opt)
    
    # 打印方案分析
    print("\n📋 方案分析：")
    option_scores = []
    for opt in decision_options:
        score = opt.score()
        option_scores.append((opt.name, score, opt))
        print(f"\n【{opt.name}】")
        print(f"  优点: {', '.join(opt.pros) if opt.pros else '无'}")
        print(f"  缺点: {', '.join(opt.cons) if opt.cons else '无'}")
        print(f"  群众支持率: {opt.support_rate*100:.0f}%")
        print(f"  可行性: {opt.feasibility}/10")
        print(f"  综合得分: {score}")
    
    # 排序
    option_scores.sort(key=lambda x: x[1], reverse=True)
    winner = option_scores[0]
    
    # 构建结果
    result = {
        "status": "success",
        "决策问题": decision,
        "推荐方案": winner[0],
        "推荐得分": winner[1],
        "全部方案评分": [
            {"方案": name, "得分": score} 
            for name, score, _ in option_scores
        ],
        "方法论": "从群众中来，到群众中去",
        "决策思路": {
            "step1": "收集各方意见和方案",
            "step2": "分析各方案的优缺点",
            "step3": "评估群众支持率和可行性",
            "step4": "综合评分确定推荐方案",
            "step5": "在实践中检验和调整"
        }
    }
    
    # 添加详细分析
    if include_analysis:
        result["详细分析"] = {
            "推荐理由": f"{winner[0]}方案综合得分最高，兼顾了各方意见",
            "风险提示": f"需要注意{winner[2].cons[0] if winner[2].cons else '潜在风险'}",
            "群众基础": f"支持率 {winner[2].support_rate*100:.0f}%",
            "实施建议": "广泛征求意见后确定方案，方案确定后要坚决执行"
        }
    
    print(f"\n🏆 推荐方案：{winner[0]} (得分: {winner[1]})")
    print(f"💡 方法论：{result['方法论']}")
    
    return result


def decide_interactive(decision: str) -> Dict[str, Any]:
    """交互式决策"""
    print(f"\n🤝 交互式决策：{decision}")
    print("=" * 50)
    
    options = []
    print("\n请输入方案（输入空行结束）：")
    
    while True:
        name = input("\n方案名称: ").strip()
        if not name:
            break
        
        pros_input = input("优点（用逗号分隔）: ").strip()
        pros = [p.strip() for p in pros_input.split(",") if p.strip()]
        
        cons_input = input("缺点（用逗号分隔）: ").strip()
        cons = [c.strip() for c in cons_input.split(",") if c.strip()]
        
        options.append({
            "name": name,
            "pros": pros,
            "cons": cons
        })
        
        print(f"✓ 已添加方案: {name}")
    
    if not options:
        return {"status": "error", "message": "未添加任何方案"}
    
    return mass_line_decide(decision, options)


def main():
    """命令行入口"""
    if len(sys.argv) < 2:
        print(__doc__)
        print("\n用法示例:")
        print('  python decider.py "选择哪份工作" \'[{"name":"A公司","pros":["工资高"],"cons":["加班多"]}]\'')
        print("\n交互模式:")
        print("  python decider.py -i \"选择哪份工作\"")
        sys.exit(1)
    
    # 交互模式
    if sys.argv[1] == "-i":
        decision = sys.argv[2] if len(sys.argv) > 2 else "未命名决策"
        result = decide_interactive(decision)
    else:
        # 解析参数
        decision = sys.argv[1]
        
        if len(sys.argv) > 2:
            try:
                options = json.loads(sys.argv[2])
            except json.JSONDecodeError:
                print("错误: 选项格式应为JSON数组")
                sys.exit(1)
        else:
            options = []
        
        if not options:
            # 尝试交互模式
            result = decide_interactive(decision)
        else:
            result = mass_line_decide(decision, options)
    
    # 如果指定了 --json 选项，输出 JSON 格式
    if "--json" in sys.argv:
        print("\n" + json.dumps(result, ensure_ascii=False, indent=2))
    
    return result


if __name__ == "__main__":
    main()