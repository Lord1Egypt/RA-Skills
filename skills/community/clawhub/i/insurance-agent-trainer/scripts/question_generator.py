# Insurance Question Bank Generator / 保险问题库自动生成脚本

"""
从产品画像自动生成标准化问题库
支持：单选题、多选题、案例分析、异议处理、竞品对比、促成话术
"""

import json
import random
from typing import Optional


# ============ 问题模板库 ============

OBJECTION_TEMPLATES = {
    "已有社保": {
        "L2": [
            "客户表示已有社保，不需要商业保险。请说明社保与商业保险的互补关系，并给出具体的费用对比案例。"
        ],
        "L3": [
            "高收入客户（年收入100万）表示'社保足够了'。请从'收入损失补偿'角度，设计一个重疾险的必要性说明。"
        ]
    },
    "保费太贵": {
        "L1": [
            "客户觉得保费太贵，你应该如何回应？请给出至少2种替代方案。"
        ],
        "L2": [
            "客户希望将年缴保费从2万降至5000元，但产品最低年缴为1.2万。如何在不降低核心保障的前提下处理这个异议？"
        ]
    },
    "回去商量": {
        "L2": [
            "客户表示'回去和家人商量一下'，这是典型的拖延异议。请设计3步处理方案，将商量变成确定购买。"
        ]
    },
    "比别家贵": {
        "L2": [
            "客户拿着竞品（平安福）条款来比较，说保费比你们便宜15%。如何做竞品对比？"
        ],
        "L3": [
            "客户是企业主，表示'你们产品不如某外资保险公司品牌大'。从保险安全性、条款保障两个维度回应。"
        ]
    }
}

PRODUCT_KNOWLEDGE_TEMPLATES = [
    "这款产品（{name}）的等待期是多久？请说明等待期内外的赔付差异。",
    "请简述（{name}）的保障责任范围，包括主险和附加险。",
    "（{name}）的缴费方式有哪些？不同缴费期如何影响总保费？",
    "投保人保费豁免条款的具体条件是什么？请举例说明。",
    "（{name}）的犹豫期是几天？犹豫期内退保会有什么损失？",
    "请说明（{name}）的'如实告知'义务，以及未如实告知的法律后果。",
    "（{name}）对被保险人的年龄要求是多少？超过年龄限制如何处理？",
    "产品中的'现金价值'是什么？在什么时候退保最合适？",
]

CASE_TEMPLATES = {
    "L2": [
        {
            "scenario": "35岁男性，IT工程师，年薪40万，已婚有1个孩子（3岁），有房贷150万（20年）。想买一份保障型保险。请为他设计保险方案。",
            "focus": "家庭保障缺口分析，产品组合（寿险+重疾+医疗），保费合理性"
        },
        {
            "scenario": "45岁女性，私企业主，年收入80万，有社保，孩子在国外读高中（每年30万教育费）。希望做养老规划。请为她设计含年金的保险方案。",
            "focus": "年金险IRR计算，养老现金流规划，教育金与养老金的平衡"
        }
    ],
    "L3": [
        {
            "scenario": "50岁男性，私企老板（制造业），企业年产值3000万，个人名下有住房2套（价值1000万），企业负债800万（个人连带担保）。担心企业债务风险影响家庭资产。请问如何用保险工具帮他做资产隔离？",
            "focus": "资产隔离+终身寿险+保险金信托，税务规划，传承设计"
        }
    ]
}


# ============ 问题生成器 ============


def generate_question_bank(product_profile: dict, agent_level: str = "L2",
                           questions_per_category: int = 5) -> dict:
    name = product_profile.get("product_name", "该产品")

    qb = {
        "meta": {"product": name, "level": agent_level, "total_questions": 0, "categories": {}},
        "questions": []
    }

    # 1. 产品知识题
    product_qs = []
    for i, tmpl in enumerate(PRODUCT_KNOWLEDGE_TEMPLATES[:questions_per_category + 2]):
        product_qs.append({
            "id": f"PK_{agent_level}_{i+1:02d}",
            "type": "product_knowledge", "category": "产品知识",
            "difficulty": {"L1": 1, "L2": 2, "L3": 3}[agent_level],
            "question": tmpl.format(name=name),
            "answer_guide": f"根据{name}产品手册对应章节回答",
            "points": {"L1": 1, "L2": 2, "L3": 3}[agent_level]
        })
    qb["categories"]["product_knowledge"] = len(product_qs)
    qb["questions"].extend(product_qs)

    # 2. 案例分析题
    case_qs = []
    case_templates = CASE_TEMPLATES.get(agent_level, CASE_TEMPLATES["L2"])
    for i, case in enumerate(case_templates[:questions_per_category]):
        case_qs.append({
            "id": f"CA_{agent_level}_{i+1:02d}",
            "type": "case_analysis", "category": "案例分析",
            "difficulty": {"L1": 1, "L2": 3, "L3": 5}[agent_level],
            "question": f"【案例分析】{case['scenario']}\n\n【训练重点】{case['focus']}",
            "answer_guide": f"建议方案：主险{name} + 附加险 + 医疗险 | {case['focus']}",
            "points": {"L1": 3, "L2": 5, "L3": 8}[agent_level]
        })
    qb["categories"]["case_analysis"] = len(case_qs)
    qb["questions"].extend(case_qs)

    # 3. 异议处理题
    objection_qs = []
    for category, templates in OBJECTION_TEMPLATES.items():
        level_templates = templates.get(agent_level, templates.get("L2", []))
        for i, q_text in enumerate(level_templates[:2]):
            objection_qs.append({
                "id": f"OB_{agent_level}_{category[:4]}_{i+1:02d}",
                "type": "objection_handling", "category": "异议处理",
                "objection_type": category,
                "difficulty": {"L1": 2, "L2": 3, "L3": 4}[agent_level],
                "question": q_text,
                "framework": "A(认同)-C(澄清)-E(引导)",
                "points": {"L1": 2, "L2": 4, "L3": 6}[agent_level]
            })
    qb["categories"]["objection_handling"] = len(objection_qs)
    qb["questions"].extend(objection_qs)

    # 4. 合规话术题
    compliance_qs = [
        {
            "id": f"CP_{agent_level}_01",
            "type": "compliance", "category": "合规话术", "difficulty": 1,
            "question": f"请用合规语言向客户说明{name}的犹豫期和退保规则（不超过3句话）。",
            "checklist": ["提及犹豫期天数（一般15天）", "犹豫期内退保退还全部保费",
                          "犹豫期后退保退还现金价值，可能有损失", "无误导性表述"],
            "points": 2
        },
        {
            "id": f"CP_{agent_level}_02",
            "type": "compliance", "category": "合规话术", "difficulty": 2,
            "question": f"在介绍{name}时，以下哪些话术违规？\n①'我们公司最大，理赔最快'\n②'只要住院就能赔'\n③'这个产品保证收益率5%'\n④'请您仔细阅读健康告知，如实填写'",
            "violations": ["①夸大公司实力", "②绝对化表述", "③使用未经证实的收益率"],
            "correct": "④是合规话术",
            "points": 2
        }
    ]
    qb["categories"]["compliance"] = len(compliance_qs)
    qb["questions"].extend(compliance_qs)

    # 5. 促成话术题
    closing_signals = ["客户问'多少钱一年？'", "客户问'什么时候生效？'",
                       "客户说'回去商量一下'", "客户说'能不能便宜点？'"]
    closing_qs = []
    for i, signal in enumerate(closing_signals[:questions_per_category]):
        closing_qs.append({
            "id": f"CL_{agent_level}_{i+1:02d}",
            "type": "closing_technique", "category": "促成话术",
            "difficulty": {"L1": 2, "L2": 3, "L3": 4}[agent_level],
            "question": f"客户表现出购买信号：'{signal}'。请设计促成话术。",
            "levels": {
                "L1": "标准假设成交法：直接促成",
                "L2": "利益汇总法：汇总产品亮点+限时权益",
                "L3": "回马枪+压力促成，让客户感觉自己在做决定"
            },
            "points": {"L1": 2, "L2": 4, "L3": 6}[agent_level]
        })
    qb["categories"]["closing"] = len(closing_qs)
    qb["questions"].extend(closing_qs)

    qb["meta"]["total_questions"] = len(qb["questions"])
    return qb


if __name__ == "__main__":
    sample_profile = {
        "product_name": "福享人生终身寿险（万能型）",
        "key_selling_points": ["复利增值，万能账户结算利率4.5%-5.2%", "灵活追加"],
        "exclusions": ["投保人对被保险人的故意伤害", "2年内自杀（无民事行为能力人除外）"],
        "compliance_notes": ["犹豫期15天", "等待期90天"]
    }
    qb = generate_question_bank(sample_profile, "L2", 5)
    print(f"生成了 {qb['meta']['total_questions']} 道题目")
    for cat, cnt in qb["meta"]["categories"].items():
        print(f"  - {cat}: {cnt}题")
