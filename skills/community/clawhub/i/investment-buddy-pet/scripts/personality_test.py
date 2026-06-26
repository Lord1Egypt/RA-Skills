#!/usr/bin/env python3
"""
投资性格测试 - 20 题评估五维投资性格
"""

import json
from typing import Dict, List

# 测试题目（每个维度 4 题）
QUESTIONS = [
    # 风险承受力 (0-3)
    {
        "id": 1,
        "dimension": "risk_tolerance",
        "question": "你的投资一个月内下跌 20%，你会？",
        "options": [
            {"text": "立即卖出", "score": 0},
            {"text": "部分卖出", "score": 25},
            {"text": "持有不动", "score": 50},
            {"text": "加仓买入", "score": 75},
            {"text": "借钱加仓", "score": 100}
        ]
    },
    {
        "id": 2,
        "dimension": "risk_tolerance",
        "question": "你愿意为潜在的高收益承担多大损失？",
        "options": [
            {"text": "不能接受损失", "score": 0},
            {"text": "最多 5%", "score": 25},
            {"text": "最多 15%", "score": 50},
            {"text": "最多 30%", "score": 75},
            {"text": "超过 30%", "score": 100}
        ]
    },
    {
        "id": 3,
        "dimension": "risk_tolerance",
        "question": "市场大跌 5% 时，你的第一反应是？",
        "options": [
            {"text": "恐慌卖出", "score": 0},
            {"text": "很焦虑", "score": 25},
            {"text": "有点担心", "score": 50},
            {"text": "冷静观察", "score": 75},
            {"text": "寻找机会", "score": 100}
        ]
    },
    {
        "id": 4,
        "dimension": "risk_tolerance",
        "question": "你是否有过'后悔交易'（情绪化交易后后悔）？",
        "options": [
            {"text": "经常", "score": 0},
            {"text": "有时", "score": 25},
            {"text": "偶尔", "score": 50},
            {"text": "很少", "score": 75},
            {"text": "从未", "score": 100}
        ]
    },
    # 知识水平 (5-8)
    {
        "id": 5,
        "dimension": "knowledge_level",
        "question": "你知道以下哪些估值指标？（多选）",
        "options": [
            {"text": "PE", "score": 10},
            {"text": "PB", "score": 10},
            {"text": "DCF", "score": 20},
            {"text": "EV/EBITDA", "score": 20},
            {"text": "PEG", "score": 20},
            {"text": "以上都不知道", "score": 0}
        ],
        "multi": True
    },
    {
        "id": 6,
        "dimension": "knowledge_level",
        "question": "你能否独立阅读和理解上市公司财报？",
        "options": [
            {"text": "完全不能", "score": 0},
            {"text": "能看懂部分", "score": 25},
            {"text": "能看懂大部分", "score": 50},
            {"text": "能深入分析", "score": 75},
            {"text": "能发现财务问题", "score": 100}
        ]
    },
    {
        "id": 7,
        "dimension": "knowledge_level",
        "question": "你有多少年投资经验？",
        "options": [
            {"text": "少于 1 年", "score": 20},
            {"text": "1-3 年", "score": 40},
            {"text": "3-5 年", "score": 60},
            {"text": "5-10 年", "score": 80},
            {"text": "10 年以上", "score": 100}
        ]
    },
    {
        "id": 8,
        "dimension": "knowledge_level",
        "question": "你有书面的投资计划吗？",
        "options": [
            {"text": "从来没有", "score": 0},
            {"text": "想过但没写", "score": 25},
            {"text": "有简单计划", "score": 50},
            {"text": "有详细计划", "score": 75},
            {"text": "严格执行计划", "score": 100}
        ]
    },
    # 决策风格 (9-12)
    {
        "id": 9,
        "dimension": "decision_style",
        "question": "你通常如何决定买入一只股票？",
        "options": [
            {"text": "听消息/感觉", "score": 0},
            {"text": "看别人推荐", "score": 25},
            {"text": "简单分析", "score": 50},
            {"text": "深入调研", "score": 75},
            {"text": "模型信号", "score": 100}
        ]
    },
    {
        "id": 10,
        "dimension": "decision_style",
        "question": "你投资时主要依赖什么？",
        "options": [
            {"text": "直觉", "score": 0},
            {"text": "经验", "score": 25},
            {"text": "技术分析", "score": 50},
            {"text": "基本面分析", "score": 75},
            {"text": "量化模型", "score": 100}
        ]
    },
    {
        "id": 11,
        "dimension": "decision_style",
        "question": "你做决策的速度如何？",
        "options": [
            {"text": "很快，凭直觉", "score": 0},
            {"text": "较快，简单分析", "score": 25},
            {"text": "中等，权衡利弊", "score": 50},
            {"text": "较慢，深入分析", "score": 75},
            {"text": "很慢，反复验证", "score": 100}
        ]
    },
    {
        "id": 12,
        "dimension": "decision_style",
        "question": "你如何对待不同意见？",
        "options": [
            {"text": "完全不听", "score": 0},
            {"text": "听听但不信", "score": 25},
            {"text": "选择性接受", "score": 50},
            {"text": "认真考虑", "score": 75},
            {"text": "主动寻找反对意见", "score": 100}
        ]
    },
    # 情绪稳定性 (13-16)
    {
        "id": 13,
        "dimension": "emotional_stability",
        "question": "市场大跌 5% 时，你会？",
        "options": [
            {"text": "恐慌卖出", "score": 0},
            {"text": "很焦虑但持有", "score": 25},
            {"text": "有点担心", "score": 50},
            {"text": "冷静观察", "score": 75},
            {"text": "兴奋加仓", "score": 100}
        ]
    },
    {
        "id": 14,
        "dimension": "emotional_stability",
        "question": "你多久查看一次持仓？",
        "options": [
            {"text": "每天多次", "score": 0},
            {"text": "每天一次", "score": 25},
            {"text": "每周几次", "score": 50},
            {"text": "每周一次", "score": 75},
            {"text": "每月一次", "score": 100}
        ]
    },
    {
        "id": 15,
        "dimension": "emotional_stability",
        "question": "投资盈利时，你会？",
        "options": [
            {"text": "很兴奋，想加仓", "score": 0},
            {"text": "开心，但保持谨慎", "score": 25},
            {"text": "平静，按计划执行", "score": 50},
            {"text": "冷静，考虑止盈", "score": 75},
            {"text": "完全不受影响", "score": 100}
        ]
    },
    {
        "id": 16,
        "dimension": "emotional_stability",
        "question": "你如何管理投资压力？",
        "options": [
            {"text": "无法管理，很痛苦", "score": 0},
            {"text": "偶尔运动缓解", "score": 25},
            {"text": "有固定缓解方式", "score": 50},
            {"text": "压力很小", "score": 75},
            {"text": "几乎没压力", "score": 100}
        ]
    },
    # 时间偏好 (17-20)
    {
        "id": 17,
        "dimension": "time_preference",
        "question": "你理想的持股周期是？",
        "options": [
            {"text": "几天", "score": 0},
            {"text": "几周", "score": 25},
            {"text": "几个月", "score": 50},
            {"text": "几年", "score": 75},
            {"text": "十年以上", "score": 100}
        ]
    },
    {
        "id": 18,
        "dimension": "time_preference",
        "question": "你如何看待'慢慢变富'？",
        "options": [
            {"text": "太慢，我要快速致富", "score": 0},
            {"text": "可以接受，但希望快点", "score": 25},
            {"text": "认同，但做不到", "score": 50},
            {"text": "认同，并践行", "score": 75},
            {"text": "坚信，只赚慢钱", "score": 100}
        ]
    },
    {
        "id": 19,
        "dimension": "time_preference",
        "question": "你愿意等待一个好机会多久？",
        "options": [
            {"text": "几天都等不了", "score": 0},
            {"text": "几周", "score": 25},
            {"text": "几个月", "score": 50},
            {"text": "几年", "score": 75},
            {"text": "十年以上", "score": 100}
        ]
    },
    {
        "id": 20,
        "dimension": "time_preference",
        "question": "你的投资目标是？",
        "options": [
            {"text": "短期暴利", "score": 0},
            {"text": "1 年内翻倍", "score": 25},
            {"text": "3-5 年稳健增值", "score": 50},
            {"text": "10 年以上财务自由", "score": 75},
            {"text": "世代传承", "score": 100}
        ]
    }
]

# 宠物匹配规则
PET_PROFILES = {
    "songguo": {"name": "🐿️ 松果", "risk": 25, "knowledge": 50, "decision": 50, "emotional": 70, "time": 80},
    "manman": {"name": "🐢 慢慢", "risk": 50, "knowledge": 60, "decision": 60, "emotional": 80, "time": 90},
    "boshi": {"name": "🦉 博士", "risk": 50, "knowledge": 90, "decision": 80, "emotional": 70, "time": 60},
    "lieshou": {"name": "🐺 猎手", "risk": 80, "knowledge": 60, "decision": 70, "emotional": 60, "time": 30},
    "paopao": {"name": "🐬 泡泡", "risk": 50, "knowledge": 50, "decision": 50, "emotional": 90, "time": 50},
    "ashou": {"name": "🐻 阿守", "risk": 30, "knowledge": 60, "decision": 70, "emotional": 70, "time": 70},
    "tianyan": {"name": "🦅 天眼", "risk": 70, "knowledge": 80, "decision": 80, "emotional": 70, "time": 70},
    "dashan": {"name": "🐘 大山", "risk": 50, "knowledge": 60, "decision": 60, "emotional": 70, "time": 70},
    "huli": {"name": "🦊 狐狸", "risk": 60, "knowledge": 50, "decision": 60, "emotional": 60, "time": 40},
    "junma": {"name": "🐎 骏马", "risk": 70, "knowledge": 70, "decision": 70, "emotional": 60, "time": 50},
    "luotuo": {"name": "🐪 骆驼", "risk": 70, "knowledge": 80, "decision": 80, "emotional": 80, "time": 70},
    "xingxing": {"name": "🦄 星星", "risk": 80, "knowledge": 60, "decision": 60, "emotional": 70, "time": 40}
}

def run_test():
    """运行测试"""
    print("=" * 60)
    print("投资性格测试 - 找到你的专属投资宠物")
    print("=" * 60)
    print()
    print("共 20 题，预计 5 分钟完成。")
    print("请根据真实情况作答，没有对错之分。")
    print()
    
    scores = {
        "risk_tolerance": 0,
        "knowledge_level": 0,
        "decision_style": 0,
        "emotional_stability": 0,
        "time_preference": 0
    }
    
    max_scores = {dim: 0 for dim in scores}
    
    for q in QUESTIONS:
        print(f"[{q['id']}/20] {q['question']}")
        for i, opt in enumerate(q['options']):
            print(f"  {chr(65+i)}. {opt['text']}")
        
        while True:
            answer = input("你的选择 (A-E): ").strip().upper()
            if answer in ['A', 'B', 'C', 'D', 'E'] and len(answer) == 1:
                idx = ord(answer) - 65
                if idx < len(q['options']):
                    score = q['options'][idx]['score']
                    scores[q['dimension']] += score
                    max_scores[q['dimension']] += 100
                    break
        
        print()
    
    # 计算百分比
    results = {}
    for dim in scores:
        results[dim] = round(scores[dim] / max_scores[dim] * 100) if max_scores[dim] > 0 else 50
    
    return results

def match_pet(results):
    """匹配宠物"""
    compatibilities = []
    
    for pet_id, profile in PET_PROFILES.items():
        # 计算兼容度
        risk_match = 100 - abs(results['risk_tolerance'] - profile['risk'])
        knowledge_match = 100 - abs(results['knowledge_level'] - profile['knowledge'])
        decision_match = 100 - abs(results['decision_style'] - profile['decision'])
        emotional_match = 100 - abs(results['emotional_stability'] - profile['emotional'])
        time_match = 100 - abs(results['time_preference'] - profile['time'])
        
        compatibility = (
            risk_match * 0.25 +
            knowledge_match * 0.20 +
            decision_match * 0.20 +
            emotional_match * 0.20 +
            time_match * 0.15
        )
        
        compatibilities.append({
            "pet_id": pet_id,
            "name": profile['name'],
            "compatibility": round(compatibility)
        })
    
    # 排序
    compatibilities.sort(key=lambda x: x['compatibility'], reverse=True)
    
    return compatibilities[:3]

def print_results(results, matches):
    """打印结果"""
    print()
    print("=" * 60)
    print("测试结果")
    print("=" * 60)
    print()
    print("你的五维评分：")
    print(f"  风险承受力：{results['risk_tolerance']}/100")
    print(f"  知识水平：{results['knowledge_level']}/100")
    print(f"  决策风格：{results['decision_style']}/100")
    print(f"  情绪稳定性：{results['emotional_stability']}/100")
    print(f"  时间偏好：{results['time_preference']}/100")
    print()
    print("推荐宠物：")
    for i, match in enumerate(matches):
        medal = ["🥇", "🥈", "🥉"][i]
        print(f"  {medal} {match['name']}（兼容度 {match['compatibility']}%）")
    print()
    print("选择一只宠物激活（输入序号 1-3）：")
    
    while True:
        choice = input("你的选择：").strip()
        if choice in ['1', '2', '3']:
            selected = matches[int(choice) - 1]
            print()
            print(f"🎉 你选择了 {selected['name']}！")
            print("正在激活宠物配置...")
            return selected['pet_id']

if __name__ == "__main__":
    results = run_test()
    matches = match_pet(results)
    pet_id = print_results(results, matches)
    
    # 保存结果
    output = {
        "results": results,
        "selected_pet": pet_id,
        "timestamp": __import__('datetime').datetime.now().isoformat()
    }
    
    with open("test_result.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"结果已保存到 test_result.json")
