#!/usr/bin/env python3
"""
亲子关系培养计划生成器
根据孩子年龄和问题诊断，生成个性化的培养计划
"""

import argparse
import json
from datetime import datetime, timedelta


def generate_age_based_plan(child_age: str) -> dict:
    """根据年龄段生成基础培养计划"""
    
    age_plans = {
        "0-3": {
            "stage": "婴儿期",
            "core_task": "建立信任与安全依恋",
            "description": "这是依恋关系形成的关键期。孩子通过父母的及时回应建立对世界的基本信任。",
            "key_indicators": [
                "及时回应孩子的需求",
                "保持情绪稳定",
                "提供安全稳定的环境",
                "肌肤接触和眼神交流"
            ],
            "protect_focus": [
                "保护探索的萌芽（抓握、触摸、爬行）",
                "保护自主性的最初表达（摇头、推开）",
                "保护情感表达（哭、笑）"
            ],
            "avoid": [
                "长时间分离而不解释",
                "在孩子面前激烈争吵",
                "强制断奶、断奶睡",
                "忽视哭泣或过度响应"
            ],
            "milestones": {
                "3months": "能对主要照顾者微笑",
                "6months": "能区分熟悉和陌生",
                "12months": "形成安全依恋",
                "24months": "开始发展自主性"
            }
        },
        "3-6": {
            "stage": "幼儿期",
            "core_task": "培养自主性与主动性",
            "description": "孩子开始有强烈的'我要自己做'的意愿。这是自主性发展的黄金期。",
            "key_indicators": [
                "提供有限选择（今天穿蓝色还是红色衣服）",
                "允许说'不'和适度的反抗",
                "鼓励独立完成任务",
                "接纳情绪但设定边界"
            ],
            "protect_focus": [
                "保护自主探索的意愿",
                "保护想象力和假装游戏",
                "保护提问和好奇心",
                "保护社交尝试"
            ],
            "avoid": [
                "替孩子做他能做的事",
                "否定孩子的感受（'这有什么好怕的'）",
                "过度保护不让孩子尝试",
                "用惩罚阻止反抗行为"
            ],
            "milestones": {
                "3years": "能表达基本需求和情绪",
                "4years": "开始玩角色扮演游戏",
                "5years": "能遵守简单规则",
                "6years": "准备好进入学校环境"
            }
        },
        "6-12": {
            "stage": "学龄期",
            "core_task": "培养能力感与勤奋感",
            "description": "孩子开始在学校和同伴中获得能力感。通过努力获得成就感是关键。",
            "key_indicators": [
                "关注过程而非结果",
                "鼓励努力而非天赋",
                "支持兴趣爱好发展",
                "培养时间管理和自主学习"
            ],
            "protect_focus": [
                "保护学习兴趣和好奇心",
                "保护失败后继续尝试的勇气",
                "保护同伴关系",
                "保护多元能力的发展"
            ],
            "avoid": [
                "只关注分数",
                "与其他孩子比较",
                "过度安排孩子时间",
                "代替孩子解决社交问题"
            ],
            "milestones": {
                "7years": "开始理解规则的重要性",
                "9years": "能够独立完成作业",
                "11years": "发展出稳定的自我概念"
            }
        },
        "12+": {
            "stage": "青春期",
            "core_task": "支持身份认同与分离个体化",
            "description": "孩子开始探索'我是谁'，通过与父母分离来建立独立身份。这是正常的发展过程。",
            "key_indicators": [
                "尊重隐私和个人空间",
                "允许观点不同",
                "协商而非命令",
                "提供情感支持而非控制"
            ],
            "protect_focus": [
                "保护自我探索的空间",
                "保护隐私",
                "保护同伴关系",
                "保护情绪体验的完整性"
            ],
            "avoid": [
                "过度监控（查手机、日记）",
                "公开批评和羞辱",
                "将不同观点视为背叛",
                "切断与朋友的联系"
            ],
            "milestones": {
                "14years": "形成相对稳定的自我认同",
                "16years": "发展出独立的价值观",
                "18years": "准备好离开家庭独立"
            }
        }
    }
    
    # 根据年龄匹配
    age_num = int(child_age.replace("+", "").replace("岁", "").split("-")[0])
    
    if age_num < 3:
        return age_plans["0-3"]
    elif age_num < 6:
        return age_plans["3-6"]
    elif age_num < 12:
        return age_plans["6-12"]
    else:
        return age_plans["12+"]


def generate_problem_based_plan(problem_type: str, severity: str) -> dict:
    """根据问题类型生成干预计划"""
    
    problem_plans = {
        "主体性缺失": {
            "root_cause": "长期被控制，决策权和选择权被剥夺",
            "intervention": [
                "开始提供有限选择",
                "逐步归还决策权",
                "允许试错和承担后果",
                "避免过度介入"
            ],
            "timeline": "6-12个月",
            "warning_signs": [
                "孩子无法做出选择（需要继续引导）",
                "选择后后悔（需要接纳情绪）",
                "过度依赖（需要耐心等待）"
            ]
        },
        "能量枯竭": {
            "root_cause": "时间被过度占用，能量持续消耗",
            "intervention": [
                "识别并减少非必要任务",
                "保留自由玩耍时间",
                "减少竞争性活动",
                "增加户外和运动"
            ],
            "timeline": "3-6个月",
            "warning_signs": [
                "对一切失去兴趣（需要专业支持）",
                "睡眠问题（需要医学评估）",
                "持续情绪低落（需要专业支持）"
            ]
        },
        "情绪困难": {
            "root_cause": "情绪长期不被接纳和引导",
            "intervention": [
                "命名和确认情绪",
                "设立情绪安全空间",
                "示范情绪调节",
                "提供稳定回应"
            ],
            "timeline": "6-12个月",
            "warning_signs": [
                "情绪崩溃频繁且剧烈",
                "有自伤行为",
                "持续两周以上的情绪低落"
            ]
        },
        "亲子冲突": {
            "root_cause": "边界不清，控制与反抗的循环",
            "intervention": [
                "明确边界并一致执行",
                "减少命令式语言",
                "建立修复关系的日常习惯",
                "处理自己的情绪"
            ],
            "timeline": "3-6个月",
            "warning_signs": [
                "冲突升级为暴力",
                "孩子拒绝所有交流",
                "影响正常生活功能"
            ]
        }
    }
    
    return problem_plans.get(problem_type, {})


def generate_cultivation_plan(child_age: str, problem_types: list, output_format: str = "markdown") -> str:
    """生成完整的培养计划"""
    
    # 获取年龄段基础计划
    age_plan = generate_age_based_plan(child_age)
    
    # 获取问题干预计划
    problem_plans = [generate_problem_based_plan(p, "中度") for p in problem_types]
    
    # 生成计划
    if output_format == "markdown":
        return generate_markdown_plan(child_age, age_plan, problem_plans)
    else:
        return generate_json_plan(child_age, age_plan, problem_plans)


def generate_markdown_plan(child_age: str, age_plan: dict, problem_plans: list) -> str:
    """生成Markdown格式的计划"""
    
    plan = []
    plan.append("# 个性化亲子培养计划\n")
    plan.append(f"**生成日期**: {datetime.now().strftime('%Y-%m-%d')}")
    plan.append(f"**孩子年龄**: {child_age}岁")
    plan.append(f"**发展阶段**: {age_plan['stage']}")
    plan.append(f"**核心任务**: {age_plan['core_task']}\n")
    
    # 阶段概述
    plan.append("---\n")
    plan.append("## 阶段概述\n")
    plan.append(f"{age_plan['description']}\n")
    
    # 关键行动指标
    plan.append("---\n")
    plan.append("## 关键行动指标\n")
    plan.append("以下是你在这个阶段应该重点做的事情：\n")
    for i, indicator in enumerate(age_plan["key_indicators"], 1):
        plan.append(f"{i}. {indicator}")
    plan.append("")
    
    # 保护重点
    plan.append("---\n")
    plan.append("## 保护重点\n")
    plan.append("以下方面需要特别保护，不要破坏：\n")
    for item in age_plan["protect_focus"]:
        plan.append(f"- {item}")
    plan.append("")
    
    # 避免事项
    plan.append("---\n")
    plan.append("## 避免事项\n")
    plan.append("以下行为会伤害孩子的发展，需要避免：\n")
    for item in age_plan["avoid"]:
        plan.append(f"- ~~{item}~~")
    plan.append("")
    
    # 发展里程碑
    plan.append("---\n")
    plan.append("## 发展里程碑\n")
    plan.append("这个阶段孩子应该达到的发展标志：\n")
    for marker, desc in age_plan["milestones"].items():
        plan.append(f"- **{marker}**: {desc}")
    plan.append("")
    
    # 问题干预
    if problem_plans:
        plan.append("---\n")
        plan.append("## 问题专项干预\n")
        
        for i, pp in enumerate(problem_plans, 1):
            if not pp:
                continue
                
            problem_name = list({"主体性缺失": "", "能量枯竭": "", "情绪困难": "", "亲子冲突": ""}.keys())[i-1]
            plan.append(f"### {i}. {problem_name}\n")
            plan.append(f"**根源分析**: {pp.get('root_cause', '待诊断')}\n")
            plan.append(f"**预计干预周期**: {pp.get('timeline', '视情况')}\n")
            plan.append("\n**干预措施**:\n")
            for j, action in enumerate(pp.get("intervention", []), 1):
                plan.append(f"{j}. {action}")
            plan.append("\n**警示信号**:\n")
            for signal in pp.get("warning_signs", []):
                plan.append(f"- {signal}")
            plan.append("")
    
    # 每周行动计划
    plan.append("---\n")
    plan.append("## 每周行动计划\n")
    plan.append("### 每日必做\n")
    plan.append("| 时间 | 活动 | 目的 |\n")
    plan.append("|------|------|------|\n")
    plan.append("| 早晨 | 5分钟专属陪伴 | 建立情感联结 |\n")
    plan.append("| 放学后 | 倾听而非追问 | 了解孩子状态 |\n")
    plan.append("| 晚间 | 回顾与感谢 | 培养积极情绪 |\n")
    plan.append("\n### 每周必做\n")
    plan.append("| 项目 | 时长 | 说明 |\n")
    plan.append("|------|------|------|\n")
    plan.append("| 户外活动 | 2小时+ | 释放能量 |\n")
    plan.append("| 自由玩耍 | 1小时+ | 自主探索 |\n")
    plan.append("| 一对一时光 | 30分钟 | 深度联结 |\n")
    plan.append("| 家庭会议 | 20分钟 | 培养参与感 |\n")
    plan.append("\n")
    
    # 评估与调整
    plan.append("---\n")
    plan.append("## 评估与调整\n")
    plan.append("### 每周自评问题\n")
    plan.append("1. 这周我给了孩子多少次选择机会？\n")
    plan.append("2. 我有多少次是在命令而不是请求？\n")
    plan.append("3. 孩子的情绪状态如何？\n")
    plan.append("4. 我自己的情绪状态如何？\n")
    plan.append("5. 有什么进步？有什么需要调整？\n")
    plan.append("\n### 调整信号\n")
    plan.append("- 孩子更加配合 → 继续当前策略\n")
    plan.append("- 冲突增加 → 可能推进太快，需要放慢\n")
    plan.append("- 孩子退缩 → 需要更多情感支持\n")
    plan.append("- 父母疲惫 → 需要寻求支持，照顾好自己\n")
    plan.append("\n---\n")
    plan.append(f"*本计划基于孩子年龄 {child_age} 岁和发展阶段制定，请根据实际情况灵活调整。*\n")
    
    return "\n".join(plan)


def generate_json_plan(child_age: str, age_plan: dict, problem_plans: list) -> str:
    """生成JSON格式的计划"""
    
    data = {
        "child_age": child_age,
        "stage": age_plan["stage"],
        "core_task": age_plan["core_task"],
        "generated_at": datetime.now().isoformat(),
        "age_based_plan": age_plan,
        "problem_interventions": problem_plans,
        "weekly_action": {
            "daily": [
                {"time": "早晨", "activity": "5分钟专属陪伴", "purpose": "建立情感联结"},
                {"time": "放学后", "activity": "倾听而非追问", "purpose": "了解孩子状态"},
                {"time": "晚间", "activity": "回顾与感谢", "purpose": "培养积极情绪"}
            ],
            "weekly": [
                {"item": "户外活动", "duration": "2小时+", "note": "释放能量"},
                {"item": "自由玩耍", "duration": "1小时+", "note": "自主探索"},
                {"item": "一对一时光", "duration": "30分钟", "note": "深度联结"},
                {"item": "家庭会议", "duration": "20分钟", "note": "培养参与感"}
            ]
        }
    }
    
    return json.dumps(data, ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(description="亲子关系培养计划生成器")
    parser.add_argument("--age", "-a", type=str, required=True, help="孩子年龄，如 '8' 或 '12+'")
    parser.add_argument("--problems", "-p", type=str, nargs="+", default=[], 
                       help="问题类型，如 '主体性缺失' '能量枯竭'")
    parser.add_argument("--output", "-o", type=str, help="输出文件路径")
    parser.add_argument("--format", "-f", choices=["markdown", "json"], default="markdown",
                       help="输出格式")
    
    args = parser.parse_args()
    
    plan = generate_cultivation_plan(args.age, args.problems, args.format)
    
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(plan)
        print(f"培养计划已生成: {args.output}")
    else:
        print(plan)


if __name__ == "__main__":
    main()
