#!/usr/bin/env python3
import json
import os
import re

# English name mapping
english_names = {
    "第一性原理": "First Principles",
    "机会成本": "Opportunity Cost",
    "复利效应": "Compound Effect",
    "临界质量": "Critical Mass",
    "准备启动": "Preparation & Launch",
    "能力圈": "Circle of Competence",
    "逆向思维": "Inversion",
    "多元思维模型": "Mental Models Lattice",
    "护城河": "Moat",
    "安全边际": "Margin of Safety",
    "Lollapalooza 效应": "Lollapalooza Effect",
    "确认偏误": "Confirmation Bias",
    "锚定效应": "Anchoring Effect",
    "损失厌恶": "Loss Aversion",
    "社会认同": "Social Proof",
    "稀缺性": "Scarcity",
    "权威影响": "Authority Influence",
    "承诺一致": "Commitment & Consistency",
    "喜好原理": "Liking Principle",
    "对比原理": "Contrast Principle",
    "可得性启发": "Availability Heuristic",
    "代表性启发": "Representativeness Heuristic",
    "沉没成本": "Sunk Cost",
    "框架效应": "Framing Effect",
    "后见之明": "Hindsight Bias",
    "过度自信偏差": "Overconfidence Bias",
    "禀赋效应": "Endowment Effect",
    "现状偏误": "Status Quo Bias",
    "赌徒谬误": "Gambler's Fallacy",
    "光环效应": "Halo Effect",
    "均值回归": "Regression to the Mean",
    "激励机制": "Incentive Mechanism",
    "二阶思维": "Second-Order Thinking",
    "地图不是疆域": "Map is Not Territory",
    "奥卡姆剃刀": "Occam's Razor",
    "汉隆剃刀": "Hanlon's Razor",
    "博弈论": "Game Theory",
    "幂律分布": "Power Law Distribution",
    "反脆弱": "Antifragility",
    "黑天鹅": "Black Swan",
    "幸存者偏差": "Survivorship Bias",
    "达克效应": "Dunning-Kruger Effect",
    "市场先生": "Mr. Market",
    "回归均值": "Mean Reversion",
    "规模效应": "Scale Effect",
    "供需关系": "Supply & Demand",
    "杠杆": "Leverage",
    "非对称风险": "Asymmetric Risk",
    "比较优势": "Comparative Advantage",
    "叙事谬误": "Narrative Fallacy",
    "边际递减": "Diminishing Returns",
    "近因效应": "Recency Effect",
    "弹性": "Elasticity",
    "从众效应": "Bandwagon Effect",
    "创造性破坏": "Creative Destruction",
    "峰终定律": "Peak-End Rule",
    "利益攸关": "Skin in the Game",
    "遍历性": "Ergodicity",
    "冗余": "Redundancy",
    "压力影响": "Stress Influence",
    "被剥夺超级反应": "Deprival Super-Reaction",
    "嫉妒倾向": "Envy Tendency",
    "巴甫洛夫联想": "Pavlovian Association",
    "简单痛苦规避": "Simple Pain Avoidance",
    "好奇心倾向": "Curiosity Tendency",
    "互惠倾向": "Reciprocation Tendency",
    "尊重理由倾向": "Reason-Respecting Tendency",
    "格栅理论": "Lattice Theory",
    "系统思维": "Systems Thinking",
    "熵增定律": "Entropy",
    "影响圈/关注圈": "Circle of Influence",
    "帕累托原则": "Pareto Principle",
    "知识复利": "Knowledge Compounding",
    "权威错误影响": "Authority Misjudgment",
    "废话倾向": "Twaddle Tendency",
    "康德式公平倾向": "Kantian Fairness",
    "容错设计": "Fault Tolerance",
    "耐心": "Patience",
    "知识谦逊": "Intellectual Humility",
    "延迟满足": "Delayed Gratification",
    "什么都不做": "Do Nothing"
}

# Read models.json
with open('data/models.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

updated = 0
for model in data['models']:
    ref_file = model['referenceFile']
    chinese_name = model['name']
    english_name = english_names.get(chinese_name, "")
    
    if not os.path.exists(ref_file):
        print(f"⚠️  文件不存在: {ref_file}")
        continue
    
    # Read file
    with open(ref_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    if not lines:
        continue
    
    # Create new title
    new_title = f"# {chinese_name} ({english_name})\n"
    
    # Check if first line needs update
    if lines[0].strip().startswith('#'):
        old_title = lines[0].strip()
        if old_title != new_title.strip():
            lines[0] = new_title
            
            # Write back
            with open(ref_file, 'w', encoding='utf-8') as f:
                f.writelines(lines)
            
            updated += 1
            print(f"✓ {model['id']:>2}: {chinese_name}")

print(f"\n✅ 更新完成：{updated} 个文档标题已标准化")
