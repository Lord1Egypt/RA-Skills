#!/usr/bin/env python3
"""
AI算力销售 - 发现阶段话术与框架工具
Discovery Playbook for AI Infrastructure Sales

Usage:
    python3 discovery.py --scenario first_call --industry technology --format markdown
    python3 discovery.py --scenario poc --industry healthcare --format json --output result.json
"""

import argparse
import json
import sys
from typing import Any, Dict, List

# ─────────────────────────────────────────────
# 场景定义
# ─────────────────────────────────────────────

SCENARIOS = {
    "first_call": {
        "name": "首次电话沟通",
        "description": "冷启动/初次接触，快速建立信任并挖掘初步需求",
        "duration_hint": "15-20分钟",
        "goals": [
            "确认客户身份与职位",
            "了解其AI/ML业务方向",
            "识别算力瓶颈信号",
            "约定下一步深度沟通",
        ],
    },
    "intro_call": {
        "name": "需求介绍会议",
        "description": "客户已有初步意向，深入了解其业务场景与技术架构",
        "duration_hint": "30-60分钟",
        "goals": [
            "深度了解AI工作负载类型",
            "了解现有基础设施与痛点",
            "评估预算与决策链",
            "识别技术决策人",
        ],
    },
    "poc": {
        "name": "POC阶段访谈",
        "description": "验证阶段，收集技术细节与评估标准",
        "duration_hint": "45-90分钟",
        "goals": [
            "明确POC目标与成功标准",
            "了解数据规模与模型复杂度",
            "确认技术对接需求",
            "识别潜在风险点",
        ],
    },
    "renewal": {
        "name": "续约/增购沟通",
        "description": "现有客户的价值回顾与增购机会挖掘",
        "duration_hint": "20-30分钟",
        "goals": [
            "回顾使用效果与ROI",
            "发现新增需求",
            "识别扩张场景",
            "锁定续约条件",
        ],
    },
}

# ─────────────────────────────────────────────
# 行业定义
# ─────────────────────────────────────────────

INDUSTRIES = {
    "technology": {
        "name": "科技/互联网",
        "pain_points": [
            "模型训练成本高，GPU利用率低",
            "推理集群扩缩容不灵活",
            "多租户安全隔离",
            "与内部ML平台集成",
        ],
        "typical_workloads": ["大模型预训练", "RLHF微调", "推理服务", "RAG应用"],
        "key_contacts": ["CTO", "VP Engineering", "ML平台负责人", "Infra负责人"],
    },
    "finance": {
        "name": "金融",
        "pain_points": [
            "数据合规与安全要求极高",
            "低延迟推理要求",
            "模型可解释性",
            "灾备与多地域部署",
        ],
        "typical_workloads": ["量化策略训练", "风控模型", "智能投顾", "反欺诈"],
        "key_contacts": ["CIO", "量化团队负责人", "风控负责人", "合规负责人"],
    },
    "healthcare": {
        "name": "医疗健康",
        "pain_points": [
            "数据隐私（HIPAA等）",
            "长周期临床验证",
            "小样本学习需求",
            "多模态数据处理",
        ],
        "typical_workloads": ["医学影像分析", "药物发现", "病历NLP", "基因测序分析"],
        "key_contacts": ["CIO", "CDO", "临床AI负责人", "研发负责人"],
    },
    "autonomous": {
        "name": "自动驾驶/机器人",
        "pain_points": [
            "超大规模数据标注与训练",
            "仿真计算",
            "极端案例覆盖率",
            "车端-云端协同",
        ],
        "typical_workloads": [
            "感知模型训练",
            "仿真渲染",
            "数据闭环处理",
            "多传感器融合",
        ],
        "key_contacts": ["VP AI", "数据平台负责人", "仿真负责人", "CTO"],
    },
    "media": {
        "name": "内容/娱乐",
        "pain_points": [
            "生成式内容生产成本",
            "实时推理延迟",
            "内容安全审核",
            "多语言AIGC",
        ],
        "typical_workloads": ["文生图/视频", "数字人", "语音合成", "内容推荐"],
        "key_contacts": ["技术VP", "AI Lab负责人", "产品负责人"],
    },
    "manufacturing": {
        "name": "制造业",
        "pain_points": [
            "边缘-云端协同",
            "质检自动化",
            "预测性维护",
            "工厂网络安全",
        ],
        "typical_workloads": ["视觉质检", "数字孪生", "工艺优化", "缺陷检测"],
        "key_contacts": ["IT负责人", "智能化负责人", "工厂厂长", "CTO"],
    },
    "academic": {
        "name": "学术/研究机构",
        "pain_points": [
            "科研经费限制",
            "算力申请周期长",
            "多用户共享调度",
            "数据版权与开放性",
        ],
        "typical_workloads": ["基础研究训练", "论文复现", "开放模型微调", "HPC融合"],
        "key_contacts": ["PI/实验室负责人", "信息中心负责人", "研究生"],
    },
    "government": {
        "name": "政府/央企",
        "pain_points": [
            "信创合规要求",
            "私有化部署",
            "数据不出域",
            "等保/分保认证",
        ],
        "typical_workloads": ["政务知识库", "智能问答", "公文处理", "城市大脑"],
        "key_contacts": ["信息中心主任", "科技处长", "CIO", "项目经理"],
    },
}

# ─────────────────────────────────────────────
# 通用访谈问题模板
# ─────────────────────────────────────────────

DISCOVERY_QUESTIONS = {
    "situation": {
        "title": "现状了解",
        "questions": [
            {
                "id": "S1",
                "question": "能介绍一下您目前团队规模和AI/ML的业务方向吗？",
                "purpose": "了解业务背景，判断算力需求规模",
                "skill_tip": "用开放式问题开场，避免一上来就问技术细节",
            },
            {
                "id": "S2",
                "question": "目前使用的是什么云厂商或自建算力？规模如何？",
                "purpose": "了解现有资源配置，识别替换或补充机会",
                "skill_tip": "避免批评客户现有方案，以了解为主",
            },
            {
                "id": "S3",
                "question": "现有的GPU集群利用率大概是什么水平？",
                "purpose": "挖掘效率优化空间",
                "skill_tip": "客户通常不清楚具体数字，可引导估算",
            },
            {
                "id": "S4",
                "question": "近期有哪些新项目或业务场景需要算力支持？",
                "purpose": "发现新需求信号",
                "skill_tip": "关注客户提到的'计划中'项目",
            },
        ],
    },
    "pain": {
        "title": "痛点挖掘",
        "questions": [
            {
                "id": "P1",
                "question": "在模型训练或推理过程中，遇到最大的瓶颈是什么？",
                "purpose": "识别核心痛点，对症下药",
                "skill_tip": "引导客户描述具体场景而非抽象抱怨",
            },
            {
                "id": "P2",
                "question": "算力采购的审批流程是怎样的？预算周期是多久？",
                "purpose": "了解采购决策链",
                "skill_tip": "提前了解决策链可避免后期卡单",
            },
            {
                "id": "P3",
                "question": "如果算力问题解决了，对业务会有什么直接影响？",
                "purpose": "量化痛点价值",
                "skill_tip": "帮助客户把算力问题与业务KPI挂钩",
            },
            {
                "id": "P4",
                "question": "目前最耗时的环节是哪个——申请算力、排队等待、还是训练本身？",
                "purpose": "细分痛点类型",
                "skill_tip": "不同痛点对应不同的解决方案",
            },
        ],
    },
    "power": {
        "title": "权力确认",
        "questions": [
            {
                "id": "W1",
                "question": "在算力采购这件事上，最终拍板的是哪位？您是决策人还是影响者？",
                "purpose": "确认关键决策人",
                "skill_tip": "直接询问身份，避免绕弯子",
            },
            {
                "id": "W2",
                "question": "技术选型主要由哪个团队负责？他们最关注什么指标？",
                "purpose": "识别技术评估维度",
                "skill_tip": "技术人的关注点通常与采购不同",
            },
            {
                "id": "W3",
                "question": "有没有已经接触过的其他算力供应商？为什么没有合作？",
                "purpose": "了解竞争态势",
                "skill_tip": "了解竞品短板可帮助我们定位优势",
            },
        ],
    },
    "money": {
        "title": "预算探索",
        "questions": [
            {
                "id": "M1",
                "question": "目前每年在算力上的投入大概是什么量级？",
                "purpose": "评估客户购买力",
                "skill_tip": "如客户不愿透露，可问相对增长预期",
            },
            {
                "id": "M2",
                "question": "如果有一个方案能降低30%成本，您有预算空间接受吗？",
                "purpose": "测试价格弹性",
                "skill_tip": "用具体数字而非抽象提问",
            },
        ],
    },
    "timeline": {
        "title": "时间线确认",
        "questions": [
            {
                "id": "T1",
                "question": "这个需求希望什么时候落地？有什么关键时间节点吗？",
                "purpose": "确认紧迫度与决策节奏",
                "skill_tip": "时间越紧，决策越快，但也意味着风险越高",
            },
            {
                "id": "T2",
                "question": "在正式采购前，需要先做POC吗？POC的成功标准是什么？",
                "purpose": "了解验证路径",
                "skill_tip": "POC标准要具体、可量化、可验证",
            },
        ],
    },
}


# ─────────────────────────────────────────────
# 话术建议库
# ─────────────────────────────────────────────

TALKING_POINTS = {
    "opening": [
        "感谢您抽出时间，今天我想先了解一下您这边的实际情况，然后看看我们能怎么帮到您。",
        "我们服务过很多和您情况类似的团队，大多数在聊完之后都能找到明确的优化方向。",
        "您看我是直接问问题，还是先给您简单介绍一下我们的方案再讨论？",
    ],
    "probing": [
        "这个很有趣，能展开说说吗？具体是哪个环节卡住了？",
        "如果时间、成本、效果这三个只能优先满足两个，您会怎么选？",
        "您刚才提到的这个挑战，现在有什么临时方案吗？",
        "在您看来，这个问题最理想的解决状态是什么样的？",
    ],
    "objection_handling": {
        "too_expensive": [
            "完全理解成本是重要考量。我想先确认一下，您比较的是哪些方案？",
            "其实很多客户一开始也觉得贵，但算完ROI之后就发现是划算的。",
            "我们可以先从一个小规模的试点开始，成本可控，也好验证效果。",
        ],
        "already_satisfied": [
            "太好了！能问一下现在用的是什么方案吗？有什么是我们可以做得更好的？",
            "即使现有方案OK，我们也可以作为备选供应商，谈谈长期合作的可能。",
            "很多客户在业务扩张时才发现原有方案的瓶颈，我们可以提前帮您规划。",
        ],
        "no_urgency": [
            "完全理解。那您预计什么时候会重新评估算力需求？",
            "我们不需要您现在就做决定，但可以先帮您了解行业趋势，避免错过好时机。",
        ],
        "need_to_check_with_team": [
            "完全正常，这么大的决策肯定需要团队讨论。您觉得哪些同事的意见最重要？",
            "我可以准备一份针对性的对比材料，方便您内部沟通。",
        ],
    },
    "closing": [
        "今天聊得很有价值，我整理一下我们的发现和建议，回头发给您。",
        "根据刚才的沟通，我建议下一步先做一个小规模的POC验证，您看这周方便安排吗？",
        "我们有几个合作案例和您的场景很接近，我可以安排一次技术交流。",
    ],
}

# ─────────────────────────────────────────────
# 关键发现记录模板
# ─────────────────────────────────────────────

DISCOVERY_TEMPLATE = {
    "metadata": {
        "company_name": "",
        "contact_name": "",
        "contact_role": "",
        "contact_email": "",
        "interview_date": "",
        "interviewer": "",
        "scenario": "",
        "industry": "",
    },
    "situation": {
        "team_size": "",
        "ai_focus_areas": [],
        "current_infrastructure": "",
        "gpu_cluster_scale": "",
        "gpu_utilization": "",
        "new_projects_planned": [],
    },
    "pain_points": {
        "primary_pain": "",
        "pain_urgency": "",  # High / Medium / Low
        "current_workaround": "",
        "business_impact": "",
    },
    "power_map": {
        "decision_maker": "",
        "technical_eval_team": [],
        "budget_holder": "",
        "influencers": [],
    },
    "money": {
        "current_annual_spend": "",
        "budget_approval_process": "",
        "price_sensitivity": "",  # High / Medium / Low
        "cost_reduction_expectation": "",
    },
    "timeline": {
        "desired_go_live": "",
        "key_deadlines": [],
        "poc_needed": True,
        "poc_success_criteria": [],
        "decision_timeline": "",
    },
    "competitive": {
        "existing_providers": [],
        "why_not_selected": "",
        "our_advantages": [],
    },
    "next_steps": {
        "action_items": [],
        "follow_up_date": "",
        "next_meeting_type": "",
        "materials_to_prepare": [],
    },
    "notes": "",
}


# ─────────────────────────────────────────────
# 辅助函数
# ─────────────────────────────────────────────

def get_scenario(scenario_key: str) -> Dict[str, Any]:
    if scenario_key not in SCENARIOS:
        available = ", ".join(SCENARIOS.keys())
        sys.exit(f"错误：未知场景 '{scenario_key}'，可用场景：{available}")
    return SCENARIOS[scenario_key]


def get_industry(industry_key: str) -> Dict[str, Any]:
    if industry_key not in INDUSTRIES:
        available = ", ".join(INDUSTRIES.keys())
        sys.exit(f"错误：未知行业 '{industry_key}'，可用行业：{available}")
    return INDUSTRIES[industry_key]


def build_questions_list(scenario: Dict, industry: Dict) -> List[Dict]:
    """构建特定场景+行业的访谈问题列表"""
    all_qs = []
    for section_key, section in DISCOVERY_QUESTIONS.items():
        for q in section["questions"]:
            all_qs.append({**q, "category": section_key, "category_name": section["title"]})
    return all_qs


def render_markdown(scenario_key: str, industry_key: str) -> str:
    scenario = get_scenario(scenario_key)
    industry = get_industry(industry_key)
    questions = build_questions_list(scenario, industry)

    lines = [
        f"# AI算力销售发现阶段指南",
        f"",
        f"**场景：** {scenario['name']}  \n",
        f"**行业：** {industry['name']}  \n",
        f"**会议时长参考：** {scenario['duration_hint']}",
        f"",
        f"---",
        f"",
        f"## 🎯 本阶段目标",
        f"",
    ]
    for i, goal in enumerate(scenario["goals"], 1):
        lines.append(f"{i}. {goal}")

    lines += ["", f"## 🏭 {industry['name']} 行业背景", ""]

    lines.append("**典型痛点：**")
    for p in industry["pain_points"]:
        lines.append(f"- {p}")

    lines += ["", "**典型工作负载：**"]
    for w in industry["typical_workloads"]:
        lines.append(f"- {w}")

    lines += ["", "**关键决策人：**"]
    for c in industry["key_contacts"]:
        lines.append(f"- {c}")

    lines += ["", "---", "", "## ❓ 访谈问题清单", ""]

    current_cat = None
    for q in questions:
        if q["category"] != current_cat:
            lines += ["", f"### {q['category_name']}", ""]
            current_cat = q["category"]
        lines.append(f"**[{q['id']}] {q['question']}**")
        lines.append(f"- 目的：{q['purpose']}")
        lines.append(f"- 技巧：{q['skill_tip']}")
        lines.append("")

    lines += ["", "---", "", "## 💬 话术建议", ""]

    lines += ["", "### 开场白"]
    for t in TALKING_POINTS["opening"]:
        lines.append(f"- {t}")

    lines += ["", "### 深入追问"]
    for t in TALKING_POINTS["probing"]:
        lines.append(f"- {t}")

    lines += ["", "### 异议处理"]
    for obj, tips in TALKING_POINTS["objection_handling"].items():
        lines.append(f"**{obj}：**")
        for t in tips:
            lines.append(f"- {t}")
        lines.append("")

    lines += ["", "### 收尾话术"]
    for t in TALKING_POINTS["closing"]:
        lines.append(f"- {t}")

    lines += ["", "---", "", "## 📋 关键发现记录模板", "", "```"]
    lines.append(json.dumps(DISCOVERY_TEMPLATE, ensure_ascii=False, indent=2))
    lines.append("```")

    return "\n".join(lines)


def render_json(scenario_key: str, industry_key: str) -> str:
    scenario = get_scenario(scenario_key)
    industry = get_industry(industry_key)
    questions = build_questions_list(scenario, industry)

    output = {
        "metadata": {
            "scenario_key": scenario_key,
            "scenario_name": scenario["name"],
            "scenario_description": scenario["description"],
            "scenario_duration": scenario["duration_hint"],
            "industry_key": industry_key,
            "industry_name": industry["name"],
            "generated_by": "pans-discovery-playbook",
        },
        "goals": scenario["goals"],
        "industry_context": {
            "pain_points": industry["pain_points"],
            "typical_workloads": industry["typical_workloads"],
            "key_contacts": industry["key_contacts"],
        },
        "discovery_questions": questions,
        "talking_points": TALKING_POINTS,
        "discovery_template": DISCOVERY_TEMPLATE,
    }
    return json.dumps(output, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="discovery.py",
        description="AI算力销售发现阶段话术与框架工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python3 discovery.py --scenario first_call --industry technology --format markdown
  python3 discovery.py --scenario poc --industry finance --format json --output result.json
  python3 discovery.py --scenario renewal --industry healthcare

可用场景：first_call, intro_call, poc, renewal
可用行业：technology, finance, healthcare, autonomous, media, manufacturing, academic, government
        """,
    )
    parser.add_argument(
        "--scenario",
        "-s",
        type=str,
        default="intro_call",
        choices=list(SCENARIOS.keys()),
        help="沟通场景 (默认: intro_call)",
    )
    parser.add_argument(
        "--industry",
        "-i",
        type=str,
        default="technology",
        choices=list(INDUSTRIES.keys()),
        help="目标行业 (默认: technology)",
    )
    parser.add_argument(
        "--format",
        "-f",
        type=str,
        default="markdown",
        choices=["json", "markdown"],
        help="输出格式 (默认: markdown)",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="输出文件路径 (不指定则打印到标准输出)",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if args.format == "markdown":
        content = render_markdown(args.scenario, args.industry)
    else:
        content = render_json(args.scenario, args.industry)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ 已保存到: {args.output}")
    else:
        print(content)


if __name__ == "__main__":
    main()
