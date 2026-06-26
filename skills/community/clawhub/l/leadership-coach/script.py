#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
leadership-coach v1.0 - 领导力教练

提供完整的领导力与团队管理解决方案：
- 领导力 21 法则（麦克斯维尔）
- 工作效率 26 条（扎克伯格）
- 员工留任 9 因
- 执行力系统设计
- 反浑蛋领导

作者：董国华（清醒建造者）
版本：v1.0
日期：2026-04-02
协议：CC BY-NC-SA 4.0
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime


# 解决方案库定义（完整版）
SOLUTIONS = {
    "leadership-21-laws": {
        "name": "领导力 21 法则",
        "source": "约翰·麦克斯维尔博士《领导力 21 法则》",
        "framework": "领导力就是影响力，决定你是否拥有领导力的关键不在于职位高低",
        "item_count": 21,
        "keywords": ["领导力", "影响力", "管理", "团队", "授权", "传承", "品格"],
        "items": [
            {"id": 1, "name": "盖子法则", "desc": "领导能力是决定一个人成效的盖子因素。领导能力越高，他就越有成效。如果你的领导能力达到 8 分，那么你的成效就不会高过 7 分"},
            {"id": 2, "name": "影响力法则", "desc": "衡量一个人的领导力，全看他的影响力。没有影响力，就绝对无法领导别人。领导是指影响别人来跟随自己，而管理则指维持系统及其流程"},
            {"id": 3, "name": "过程法则", "desc": "领导力来自日积月累而非一日之功。领导力包含各种因素：尊重、经验、感情、待人技巧、纪律、动势、时机……每一位领导者都是学习者"},
            {"id": 4, "name": "导航法则", "desc": "谁都可以使一艘船转变方向，但惟有领导者才能设定航线。领导者必须具备积极的心态才能领导别人踏上未曾走过的道路"},
            {"id": 5, "name": "增值法则", "desc": "领导力的底线不在于我们自己能走多远，而在于我们能够帮助别人走多远。领导者就要服务于他人，提升他人的价值"},
            {"id": 6, "name": "根基法则", "desc": "信任乃是领导的根基。领导力就是策略与品格二者合一。品格带来信任，信任带来领导力。每一个人的成就，都无法超越他品格的上限"},
            {"id": 7, "name": "尊重法则", "desc": "人们自然会跟随比自己强的领导者。值得信赖的坚强的领导者才能赢得尊重"},
            {"id": 8, "name": "直觉法则", "desc": "领导者必定带着领导者的直觉来看每一件事。好领导者必须培养自知的能力，认识自己的长处、技能、弱点及心理状态"},
            {"id": 9, "name": "吸引力法则", "desc": "你是什么样的人就吸引什么样的人。越是好的领导者，就越能吸引好的领导者"},
            {"id": 10, "name": "亲和力法则", "desc": "领导者知道得人之前必先得其心。要别人伸手支持你之前，得先感动他们的心"},
            {"id": 11, "name": "核心圈法则", "desc": "一个领导者的潜力由最接近他的人所决定。你应该把五种人带进核心圈：1)有潜力者，2)积极乐观者，3)助你成功者，4)能增产者，5)能验证价值者"},
            {"id": 12, "name": "授权法则", "desc": "惟有你愿意把功劳给别人时，才会成为真正伟大的事业。领导必须愿意全力扶助跟随者，甚至愿意栽培他们来取代自己"},
            {"id": 13, "name": "镜像法则", "desc": "领导者树立好榜样后，下属会跟着模仿他们的行为从而取得成功。只有当他们亲自开始做的时候，才能算是传授"},
            {"id": 14, "name": "接纳法则", "desc": "人们先接纳领导者，才能接纳他的愿景。人们先拥护一位领导者，接着才拥护领导者的愿景"},
            {"id": 15, "name": "制胜法则", "desc": "领导者都具有一个特质，那就是他们无法接受失败。为了成功他们费心筹划，然后动员一切力量实现它。不成功决不放弃"},
            {"id": 16, "name": "动势法则", "desc": "如果改变团队的方向，领导者必须营造前进的气氛。只有领导者才能激发动势"},
            {"id": 17, "name": "优先次序法则", "desc": "领导者明白忙碌不一定等于成就。好的领导者都格守优先次序法则"},
            {"id": 18, "name": "舍得法则", "desc": "领导者必须先'舍'再'得'。真正的领导力本质，乃是牺牲"},
            {"id": 19, "name": "时机法则", "desc": "时机决定一切：在错误时机采取错误行动，结果是灾难；在错误的时机采取正确行动，结果是抵制；在正确时机采取错误行动，结果是错误；正确时机正确行动，结果是成功"},
            {"id": 20, "name": "爆炸性倍增法则", "desc": "带领跟随者得到相加的效果，带领领导者得到相乘倍增的效果。你要开始栽培领导者"},
            {"id": 21, "name": "传承法则", "desc": "一位领导者的长久价值由其继承者决定。重视由内部培植领导人才，顺利传承是领导者成就的最高点"}
        ],
        "success_formula": "人才决定组织的潜力 | 关系决定组织的士气 | 结构决定组织的规模 | 目标决定组织的方向 | 领导决定组织的成败"
    },
    "productivity-26-rules": {
        "name": "工作效率 26 条",
        "source": "Facebook 创始人马克·扎克伯格内部工作效率原则",
        "framework": "时间优先、专注、迭代、授权",
        "item_count": 26,
        "keywords": ["效率", "时间管理", "专注", "工作", "生产力", "番茄工作法"],
        "items": [
            {"id": 1, "name": "时间常有，时间在于优先", "desc": "时间管理的关键是优先级排序"},
            {"id": 2, "name": "时间总会有的：每天只计划 4～5 小时真正的工作", "desc": "不要试图填满所有时间，保留弹性"},
            {"id": 3, "name": "当你在状态时，就多干点；不然就好好休息", "desc": "接受工作状态的自然波动"},
            {"id": 4, "name": "重视你的时间，并使其值得重视：你的时间值 1000 美元/小时", "desc": "给自己的时间定价，提高时间价值意识"},
            {"id": 5, "name": "不要多任务，这只会消耗注意力；保持专注，一心一用", "desc": "多任务处理会降低效率，专注才是王道"},
            {"id": 6, "name": "养成工作习惯，并持之以恒，你的身体会适应的", "desc": "建立稳定的工作节奏和习惯"},
            {"id": 7, "name": "在有限的时间内，我们总是非常专注并且有效率", "desc": "时间限制反而能提高效率"},
            {"id": 8, "name": "进入工作状态的最佳方式就是工作，从小任务开始做起", "desc": "不要等待完美状态，从小任务开始启动"},
            {"id": 9, "name": "迭代工作，期待完美收工会令人窒息：'做完事情，要胜于完美收工'", "desc": "Facebook 办公室墙壁上贴的箴言。动手做，胜过任何完美的想象"},
            {"id": 10, "name": "工作时间越长，并不等于效率越高", "desc": "长时间工作不等于高产出"},
            {"id": 11, "name": "按重要性工作，提高效率", "desc": "优先处理重要的事情"},
            {"id": 12, "name": "有会议就尽早安排，用于准备会议的时间往往都浪费掉了", "desc": "避免会议前的无效等待和准备"},
            {"id": 13, "name": "把会议和沟通 (邮件或电话) 结合，创造不间断工作时间", "desc": "一个小会，也会毁了一个下午。当看到一个程序员冥思苦想时，不要过去打扰"},
            {"id": 14, "name": "一整天保持相同的工作环境。在项目/客户之间切换，会效率低", "desc": "减少上下文切换成本"},
            {"id": 15, "name": "工作—放松—工作=高效 (番茄工作法)", "desc": "番茄时间 25 分钟，专注工作，休息 5 分钟，每 4 个番茄时段多休息一会儿"},
            {"id": 16, "name": "把不切实际的任务分割成合理的小任务", "desc": "大目标分解为小任务"},
            {"id": 17, "name": "从来没有两个任务会有相同的优先级，总会有个更重要", "desc": "任务优先级总有差异"},
            {"id": 18, "name": "必须清楚白天必须完成的那件事。'Only ever work on the thing that will have the biggest impact'", "desc": "只去做那件有着最大影响的事情"},
            {"id": 19, "name": "把任务按时间分段，就能感觉它快被搞定了", "desc": "时间分段增加完成感"},
            {"id": 20, "name": "授权并擅用他人的力量", "desc": "如果某件事其他人也可以做到八成，那就给他做！"},
            {"id": 21, "name": "把昨天翻过去，只考虑今天和明天", "desc": "面向未来，不沉溺过去"},
            {"id": 22, "name": "给所有事情都设定一个期限。不要让工作无期限地进行下去", "desc": "期限产生紧迫感"},
            {"id": 23, "name": "针对时间紧或有压力的任务，设置结束时间", "desc": "压力任务更需要明确结束时间"},
            {"id": 24, "name": "多记，多做笔记", "desc": "记录帮助记忆和思考"},
            {"id": 25, "name": "进入高效状态后，记下任何分散你注意力的东西", "desc": "记录干扰项，保持专注"},
            {"id": 26, "name": "休息，休息一下～", "desc": "适当休息提高效率"}
        ]
    },
    "employee-retention": {
        "name": "员工留任 9 因",
        "source": "员工离职原因研究",
        "framework": "员工辞的不是工作，而是他的经理",
        "item_count": 9,
        "keywords": ["员工", "离职", "留任", "管理", "认同", "尊重", "成长"],
        "items": [
            {"id": 1, "name": "劳累过度", "desc": "斯坦福大学研究：超过 50 小时/周导致生产率大幅下降，超过 55 小时生产率降到低谷", "solution": "升职、加薪、改变职称，而不是简单粗暴增加工作量"},
            {"id": 2, "name": "员工的努力和贡献没有得到认同和酬劳", "desc": "每个人都喜欢奖赏，尤其是能够自我激励的顶级员工", "solution": "确认员工需要什么，对某些人是升职加薪，对另外的人是公开场合的认同和赞许"},
            {"id": 3, "name": "没有得到尊重", "desc": "超过一半以上的员工离职是因为他们和老板的关系紧张", "solution": "认可员工的成就，安慰项目处于攻坚阶段的员工，激发员工斗志"},
            {"id": 4, "name": "管理者不兑现承诺", "desc": "做出承诺将管理者放在了兑现承诺和引起离职的分界线上", "solution": "管理者必须信守承诺，如果无法兑现，要及时沟通并补偿"},
            {"id": 5, "name": "提拔错误的人", "desc": "如果高层管理者把工作交接给一个只知道谄上欺下的中层管理者，那对敬业的员工来说真是天大的侮辱", "solution": "建立公平的晋升机制，确保提拔的人德才兼备"},
            {"id": 6, "name": "不给员工追求职业梦想的机会", "desc": "有研究显示有机会追求职业梦想，被赋予更多自由度的人比按部就班工作的人效率高五倍", "solution": "为员工提供成长空间和自由度，支持他们追求职业梦想"},
            {"id": 7, "name": "管理者不发展员工的职业技能", "desc": "最优秀的员工渴望得到反馈，管理者有义务将其变为现实", "solution": "持续的接收员工的意见信息并给予反馈"},
            {"id": 8, "name": "员工的创造力无处可用", "desc": "把员工天生对提升知识的渴望困在狭小的牢笼里不仅限制了他们，也限制了管理者", "solution": "为员工提供创新和发挥创造力的空间和渠道"},
            {"id": 9, "name": "大材小用", "desc": "当员工认为现在的工作过于简单和无聊，他们会寻找更有挑战性的工作", "solution": "给员工分配有挑战性的任务，帮助他们成长"}
        ],
        "key_insight": "超过一半的员工离职是因为和老板的关系紧张"
    },
    "execution-system": {
        "name": "执行力系统设计",
        "source": "世界 500 强企业执行力研究（沃尔玛、丰田等）",
        "framework": "执行力是设计出来的，不是依赖个人",
        "item_count": 4,
        "keywords": ["执行力", "制度", "顶层设计", "五问法", "标准化"],
        "items": [
            {"id": 1, "name": "执行力是设计出来的", "desc": "执行力的本质不在于个人，而在于企业的规范。系统、健全的体制是执行力的根本保障"},
            {"id": 2, "name": "执行力是培养出来的", "desc": "执行力的培养是要把道理讲明白的。培训、指导、反馈"},
            {"id": 3, "name": "执行力是检查出来的", "desc": "执行力的检查是要有清单的。检查清单、定期审核"},
            {"id": 4, "name": "执行力是制度化的", "desc": "从'应该'到'必须'。将重要事项制度化、标准化"}
        ],
        "cases": [
            {
                "name": "沃尔玛三米微笑原则",
                "desc": "当离顾客接近 3 米时，必须保持微笑，统一标准：露出 8 颗牙齿。遇到顾客不满，顾客永远是对的"
            },
            {
                "name": "丰田五问法",
                "desc": "通过连续 5 次追问'为什么'找到问题的根本原因。即使是基层员工遇到问题，也必须填写'五问法'的表单"
            }
        ],
        "principles": "好的顶层设计，就是为了减少员工试错、犯错 | 战略决定成败取决于高层决策者的前瞻能力 | 细节决定成败取决于中层与基层的执行力 | 执行力的根本在于高层决策者的顶层设计能力"
    },
    "anti-jerk-leadership": {
        "name": "反浑蛋领导",
        "source": "罗伯特·萨顿教授《不要'浑蛋'原则》",
        "framework": "无论职位多高、利润贡献多大，都要清除浑蛋型领导",
        "item_count": 2,
        "keywords": ["浑蛋领导", "威吓文化", "尊重", "组织健康", "领导力"],
        "characteristics": [
            "严密监视、不信任和怀疑",
            "冷漠和非人性化来往",
            "苛刻以及公开批评他人",
            "故意屈尊以及施恩化行为",
            "感情冲动",
            "强迫高压以及自负行为",
            "过度控制他人",
            "武断、不体贴和惩罚性方式威胁他人"
        ],
        "reasons_to_reject": [
            {
                "reason": "容易对下形成一种威吓文化",
                "desc": "威吓文化像'瘟疫'一样迅速传遍整个组织，让所有人都处于一种压抑，甚至恐怖不安的环境之中。所有的人都在违背自己的心愿和情感做着顺从和讨好上司的事情"
            },
            {
                "reason": "容易遭到下属的厌恶和背弃",
                "desc": "一旦他们失去权力，他们几乎立刻就会遭到他人，特别是下属的反对和背弃。他们的下属有可能为自己的上司背了太多的'黑锅'，承担了太多的心理和道德压力"
            }
        ],
        "solutions": [
            "绝不能容忍这样的领导存在",
            "无论职位多高、利润贡献多大，都要把他'清除'出去",
            "建立零容忍政策",
            "建立举报和保护机制",
            "将'尊重他人'纳入领导力评估和晋升标准",
            "自我觉察：在我们每个人的身上都存在着'浑蛋'因子",
            "情绪控制：很好地控制自己的情绪，调整自己的行为"
        ],
        "key_insight": "我们有太多的领导过于注重手段和效率，而轻视目的和道德"
    }
}


def list_solutions(args):
    """列出所有解决方案"""
    print("\n" + "="*80)
    print("                    领导力教练 v1.0")
    print("="*80)
    print(f"\n共 {len(SOLUTIONS)} 个解决方案：\n")
    
    for i, (key, sol) in enumerate(SOLUTIONS.items(), 1):
        print(f"{i}. {sol['name']} ({key})")
        print(f"   来源：{sol['source']}")
        print(f"   框架：{sol['framework']}")
        print(f"   条目数：{sol['item_count']}条")
        print(f"   关键词：{', '.join(sol['keywords'][:4])}")
        print()
    
    print("使用提示:")
    print("  python3 script.py show <solution>     # 查看方案详情")
    print("  python3 script.py solve --problem '...' # 根据问题找方案")
    print("  python3 script.py plan --goal '...'     # 根据目标找路径")
    print("  python3 script.py diagnose --type ...   # 领导力诊断")
    print("="*80 + "\n")
    
    return {"status": "success", "count": len(SOLUTIONS)}


def show_solution(args):
    """显示解决方案详情"""
    solution_key = args.solution
    
    if solution_key not in SOLUTIONS:
        print(f"❌ 错误：未找到解决方案 '{solution_key}'")
        print(f"可用方案：{', '.join(SOLUTIONS.keys())}")
        return {"status": "error", "message": "Solution not found"}
    
    sol = SOLUTIONS[solution_key]
    
    print("\n" + "="*80)
    print(f"  {sol['name']}")
    print("="*80)
    print(f"\n来源：{sol['source']}")
    print(f"\n核心框架:")
    print(f"  {sol['framework']}")
    
    # 显示完整条目列表
    print(f"\n完整{sol['item_count']}条:")
    print("-" * 80)
    for item in sol['items']:
        print(f"\n{item['id']:02d}. {item['name']}")
        print(f"    {item['desc']}")
    
    # 显示额外信息
    if 'success_formula' in sol:
        print(f"\n成功公式:")
        print(f"  {sol['success_formula']}")
    
    if 'key_insight' in sol:
        print(f"\n核心洞察:")
        print(f"  {sol['key_insight']}")
    
    if 'cases' in sol:
        print(f"\n经典案例:")
        for case in sol['cases']:
            print(f"  • {case['name']}: {case['desc']}")
    
    if 'principles' in sol:
        print(f"\n核心原理:")
        print(f"  {sol['principles']}")
    
    if 'characteristics' in sol:
        print(f"\n典型特征:")
        for i, char in enumerate(sol['characteristics'], 1):
            print(f"  {i}. {char}")
    
    if 'reasons_to_reject' in sol:
        print(f"\n为什么要拒绝:")
        for reason in sol['reasons_to_reject']:
            print(f"\n  • {reason['reason']}")
            print(f"    {reason['desc']}")
    
    if 'solutions' in sol:
        print(f"\n如何应对:")
        for i, solution in enumerate(sol['solutions'], 1):
            print(f"  {i}. {solution}")
    
    # 显示框架文件路径
    framework_path = Path(__file__).parent / "solutions" / solution_key / "framework.md"
    if framework_path.exists():
        print(f"\n详细文档：{framework_path}")
    
    print("="*80 + "\n")
    
    return {"status": "success", "solution": solution_key}


def solve_problem(args):
    """根据问题匹配解决方案"""
    problem = args.problem.lower()
    
    print(f"\n🔍 分析问题：'{args.problem}'\n")
    
    # 关键词匹配
    matches = []
    for key, sol in SOLUTIONS.items():
        score = 0
        matched_keywords = []
        
        for keyword in sol['keywords']:
            if keyword in problem:
                score += 2
                matched_keywords.append(keyword)
        
        # 额外匹配
        if '领导' in problem and key == 'leadership-21-laws':
            score += 3
        if '效率' in problem and key == 'productivity-26-rules':
            score += 3
        if '离职' in problem and key == 'employee-retention':
            score += 3
        if '执行' in problem and key == 'execution-system':
            score += 3
        if '浑蛋' in problem or '威吓' in problem and key == 'anti-jerk-leadership':
            score += 3
        
        if score > 0:
            matches.append((key, sol, score, matched_keywords))
    
    if not matches:
        print("⚠️  未找到完全匹配的解决方案")
        print("\n建议:")
        print("  1. 尝试使用更具体的关键词（领导力/效率/离职/执行/浑蛋等）")
        print("  2. 使用 'python3 script.py list' 查看所有方案")
        return {"status": "no_match"}
    
    # 按匹配度排序
    matches.sort(key=lambda x: x[2], reverse=True)
    
    print("✅ 匹配结果:\n")
    for i, (key, sol, score, keywords) in enumerate(matches, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
        print(f"{medal} {i}. {sol['name']} (匹配度：{score})")
        print(f"   匹配关键词：{', '.join(keywords)}")
        print(f"   核心框架：{sol['framework']}")
        print(f"   条目数：{sol['item_count']}条")
        print()
    
    # 推荐最佳匹配
    best_match = matches[0]
    print(f"\n💡 建议:")
    print(f"   使用 'python3 script.py show {best_match[0]}' 查看详细方案")
    print(f"   使用 'python3 script.py plan --goal \"你的具体目标\"' 获取实施路径")
    
    print("="*80 + "\n")
    
    return {"status": "success", "matches": [m[0] for m in matches]}


def plan_goal(args):
    """根据目标规划实施路径"""
    goal = args.goal.lower()
    
    print(f"\n🎯 分析目标：'{args.goal}'\n")
    
    # 简单关键词匹配
    if any(kw in goal for kw in ["领导", "影响力", "团队领导"]):
        recommended = "leadership-21-laws"
        reason = "你的目标涉及领导力提升"
    elif any(kw in goal for kw in ["效率", "时间", "工作", "生产力"]):
        recommended = "productivity-26-rules"
        reason = "你的目标涉及工作效率提升"
    elif any(kw in goal for kw in ["离职", "留任", "员工"]):
        recommended = "employee-retention"
        reason = "你的目标涉及员工留任"
    elif any(kw in goal for kw in ["执行", "制度", "规范"]):
        recommended = "execution-system"
        reason = "你的目标涉及执行力建设"
    elif any(kw in goal for kw in ["浑蛋", "威吓", "健康", "文化"]):
        recommended = "anti-jerk-leadership"
        reason = "你的目标涉及组织健康文化"
    else:
        print("⚠️  无法确定最佳方案，请尝试使用更具体的关键词")
        return {"status": "unclear"}
    
    sol = SOLUTIONS[recommended]
    
    print(f"✅ 推荐方案：{sol['name']}")
    print(f"   理由：{reason}")
    print(f"   来源：{sol['source']}")
    print(f"\n核心框架:")
    print(f"   {sol['framework']}")
    print(f"\n完整{sol['item_count']}条:")
    for i, item in enumerate(sol['items'][:5], 1):  # 只显示前 5 条
        print(f"   {i}. {item['name']}")
    if sol['item_count'] > 5:
        print(f"   ... 还有{sol['item_count']-5}条，请使用 'show' 命令查看完整列表")
    
    print(f"\n💡 下一步:")
    print(f"   使用 'python3 script.py show {recommended}' 查看详细方案")
    print(f"   查看框架文档获取完整实施路线图")
    
    print("="*80 + "\n")
    
    return {"status": "success", "recommended": recommended}


def diagnose(args):
    """领导力诊断"""
    diag_type = args.type
    
    print(f"\n📊 {diag_type}诊断\n")
    
    if diag_type == "leadership":
        print("领导力 21 法则自我评估:\n")
        print("请对以下法则进行自我评分（1-10 分）:\n")
        for i, item in enumerate(SOLUTIONS['leadership-21-laws']['items'][:10], 1):
            print(f"{i:2d}. {item['name']:10s} ___分  ({item['desc'][:30]}...)")
        print("\n💡 建议:")
        print("   1. 找出得分最低的 3 个法则")
        print("   2. 制定改进计划")
        print("   3. 定期（每季度）重新评估")
    
    elif diag_type == "retention":
        print("员工留任风险评估:\n")
        print("请评估以下风险因素（1-10 分，10 分最高风险）:\n")
        for i, item in enumerate(SOLUTIONS['employee-retention']['items'], 1):
            print(f"{i}. {item['name']:15s} ___分  ({item['desc'][:30]}...)")
        print("\n💡 建议:")
        print("   1. 找出风险最高的 3 个因素")
        print("   2. 优先解决高风险因素")
        print("   3. 定期进行员工满意度调查")
    
    elif diag_type == "execution":
        print("执行力系统评估:\n")
        print("请评估以下维度（1-10 分，10 分最好）:\n")
        for i, item in enumerate(SOLUTIONS['execution-system']['items'], 1):
            print(f"{i}. {item['name']:15s} ___分  ({item['desc'][:30]}...)")
        print("\n💡 建议:")
        print("   1. 找出得分最低的维度")
        print("   2. 建立相应的制度和流程")
        print("   3. 定期检查和优化")
    
    else:
        print(f"❌ 错误：未知的诊断类型 '{diag_type}'")
        print("可用类型：leadership, retention, execution")
        return {"status": "error"}
    
    print("="*80 + "\n")
    
    return {"status": "success", "type": diag_type}


def main():
    parser = argparse.ArgumentParser(
        description="leadership-coach v1.0 - 领导力教练",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python3 script.py list
  python3 script.py show leadership-21-laws
  python3 script.py solve --problem "团队执行力差"
  python3 script.py plan --goal "成为更好的领导者"
  python3 script.py diagnose --type leadership
        """
    )
    
    parser.add_argument(
        "action",
        type=str,
        choices=["list", "show", "solve", "plan", "diagnose"],
        help="执行动作"
    )
    
    parser.add_argument(
        "--solution", "-s",
        type=str,
        help="解决方案名称（用于 show 动作）"
    )
    
    parser.add_argument(
        "--problem", "-p",
        type=str,
        help="问题描述（用于 solve 动作）"
    )
    
    parser.add_argument(
        "--goal", "-g",
        type=str,
        help="目标描述（用于 plan 动作）"
    )
    
    parser.add_argument(
        "--type", "-t",
        type=str,
        help="诊断类型（用于 diagnose 动作）"
    )
    
    args = parser.parse_args()
    
    # 执行对应动作
    actions = {
        "list": list_solutions,
        "show": show_solution,
        "solve": solve_problem,
        "plan": plan_goal,
        "diagnose": diagnose
    }
    
    if args.action in actions:
        # 参数验证
        if args.action == "show" and not args.solution:
            print("❌ 错误：show 动作需要 --solution 参数")
            print("示例：python3 script.py show leadership-21-laws")
            sys.exit(1)
        
        if args.action == "solve" and not args.problem:
            print("❌ 错误：solve 动作需要 --problem 参数")
            print("示例：python3 script.py solve --problem '团队执行力差'")
            sys.exit(1)
        
        if args.action == "plan" and not args.goal:
            print("❌ 错误：plan 动作需要 --goal 参数")
            print("示例：python3 script.py plan --goal '成为更好的领导者'")
            sys.exit(1)
        
        if args.action == "diagnose" and not args.type:
            print("❌ 错误：diagnose 动作需要 --type 参数")
            print("示例：python3 script.py diagnose --type leadership")
            sys.exit(1)
        
        result = actions[args.action](args)
        return result
    else:
        print(f"❌ 错误：未知的动作：{args.action}")
        sys.exit(1)


if __name__ == "__main__":
    main()
