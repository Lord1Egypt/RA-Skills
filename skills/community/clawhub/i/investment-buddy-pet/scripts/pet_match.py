#!/usr/bin/env python3
"""
宠物匹配测试脚本
根据用户答案匹配最适合的宠物
"""

import json
import os
from pathlib import Path

# 测试题库（SSBTI 自嘲风格）
QUESTIONS = [
    {
        "id": 1,
        "question": "市场大跌 20%，你的第一反应是？",
        "options": {
            "A": {"text": "关掉 APP，假装没这回事", "pets": ["wugui", "songguo"]},
            "B": {"text": "打开 APP，看看能不能抄底", "pets": ["luotuo", "maotouying"]},
            "C": {"text": "赶紧卖出，保住本金", "pets": ["mayi", "haitun"]},
            "D": {"text": "加仓！别人恐惧我贪婪！", "pets": ["shizi", "lang"]}
        }
    },
    {
        "id": 2,
        "question": "你买基金/股票的方式更像？",
        "options": {
            "A": {"text": "定投，每月自动扣款，眼不见为净", "pets": ["songguo", "haitun"]},
            "B": {"text": "研究财报，分析估值，写满三页笔记", "pets": ["maotouying", "shizi"]},
            "C": {"text": "看 K 线，找趋势，顺势而为", "pets": ["ying", "junma"]},
            "D": {"text": "分散买一堆，总有一个会涨吧", "pets": ["huli", "mayi"]}
        }
    },
    {
        "id": 3,
        "question": "朋友推荐了一只大涨的基金，你会？",
        "options": {
            "A": {"text": "心动，但忍住不追", "pets": ["wugui", "luotuo"]},
            "B": {"text": "赶紧研究一下，是不是真有机会", "pets": ["maotouying", "dunjiaoshou"]},
            "C": {"text": "先买一点试试水", "pets": ["huli", "haitun"]},
            "D": {"text": "全仓杀入，错过就没了！", "pets": ["shizi", "lang"]}
        }
    },
    {
        "id": 4,
        "question": "你的投资账户，平时打开频率是？",
        "options": {
            "A": {"text": "一个月一次，怕看到亏损", "pets": ["wugui", "songguo"]},
            "B": {"text": "每天一次，看看涨跌", "pets": ["haitun", "huli"]},
            "C": {"text": "每天 N 次，盯盘是爱好", "pets": ["ying", "junma"]},
            "D": {"text": "不看，我相信我的策略", "pets": ["maotouying", "luotuo"]}
        }
    },
    {
        "id": 5,
        "question": "你觉得投资最重要的是？",
        "options": {
            "A": {"text": "别亏钱，活着最重要", "pets": ["mayi", "wugui"]},
            "B": {"text": "找到好公司，长期拿着", "pets": ["shizi", "maotouying"]},
            "C": {"text": "低买高卖，把握节奏", "pets": ["ying", "junma"]},
            "D": {"text": "分散风险，别赌单边", "pets": ["huli", "haitun"]}
        }
    },
    {
        "id": 6,
        "question": "你的持仓亏损多少会让你睡不着？",
        "options": {
            "A": {"text": "亏损 5% 就开始焦虑", "pets": ["mayi", "songguo"]},
            "B": {"text": "亏损 10% 还能接受", "pets": ["haitun", "huli", "daxiang"]},
            "C": {"text": "亏损 20% 也淡定", "pets": ["wugui", "luotuo", "maotouying"]},
            "D": {"text": "亏损？那是加仓机会！", "pets": ["shizi", "lang", "dunjiaoshou"]}
        }
    },
    {
        "id": 7,
        "question": "你如何看待'别人恐惧我贪婪'这句话？",
        "options": {
            "A": {"text": "有道理，但我做不到", "pets": ["songguo", "mayi", "haitun"]},
            "B": {"text": "这就是我的人生信条！", "pets": ["luotuo", "shizi"]},
            "C": {"text": "要看情况，不能盲目", "pets": ["maotouying", "huli"]},
            "D": {"text": "我已经在执行了", "pets": ["lang", "ying"]}
        }
    },
    {
        "id": 8,
        "question": "你的投资知识主要来自？",
        "options": {
            "A": {"text": "看书/经典投资著作", "pets": ["wugui", "maotouying", "luotuo"]},
            "B": {"text": "看公众号/大 V/博主", "pets": ["haitun", "huli", "mayi"]},
            "C": {"text": "自己摸索，实战经验", "pets": ["shizi", "lang", "ying"]},
            "D": {"text": "系统学习过金融/投资专业", "pets": ["dunjiaoshou", "junma"]}
        }
    },
    {
        "id": 9,
        "question": "你希望多久看到投资收益？",
        "options": {
            "A": {"text": "3 年以上，我可以等", "pets": ["wugui", "shizi", "maotouying"]},
            "B": {"text": "1-3 年，中期目标", "pets": ["huli", "daxiang", "luotuo"]},
            "C": {"text": "3-12 个月，不要太久", "pets": ["haitun", "songguo", "junma"]},
            "D": {"text": "越快越好，最好是明天", "pets": ["lang", "ying", "dunjiaoshou"]}
        }
    },
    {
        "id": 10,
        "question": "最后，用一个词形容你的投资风格？",
        "options": {
            "A": {"text": "苟", "pets": ["wugui", "mayi", "songguo"]},
            "B": {"text": "稳", "pets": ["haitun", "huli", "daxiang"]},
            "C": {"text": "准", "pets": ["maotouying", "luotuo", "shizi"]},
            "D": {"text": "狠", "pets": ["lang", "ying", "dunjiaoshou", "junma"]}
        }
    }
]

# 宠物信息（12 只完整）
PETS_INFO = {
    "songguo": {
        "name": "松果",
        "emoji": "🐿️",
        "style": "谨慎定投",
        "catchphrase": "慢慢来，比较快",
        "description": "性格：谨慎、爱囤积、安全感第一\n策略：极简定投，自动储蓄"
    },
    "wugui": {
        "name": "慢慢",
        "emoji": "🐢",
        "style": "长期主义",
        "catchphrase": "时间是我的朋友",
        "description": "性格：超有耐心、淡泊名利\n策略：指数定投，长期持有"
    },
    "maotouying": {
        "name": "智多星",
        "emoji": "🦉",
        "style": "理性分析",
        "catchphrase": "让我们看看基本面...",
        "description": "性格：理性、爱研究、注重数据\n策略：深度分析，价值投资"
    },
    "lang": {
        "name": "孤狼",
        "emoji": "🐺",
        "style": "激进成长",
        "catchphrase": "高风险高回报",
        "description": "性格：果断、冒险、追求成长\n策略：趋势追踪，主动出击"
    },
    "daxiang": {
        "name": "稳稳",
        "emoji": "🐘",
        "style": "稳健配置",
        "catchphrase": "稳字当头",
        "description": "性格：稳重、平衡、大而稳\n策略：资产配置，分散投资"
    },
    "ying": {
        "name": "鹰眼",
        "emoji": "🦅",
        "style": "趋势交易",
        "catchphrase": "风向变了！",
        "description": "性格：敏锐、果断、顺势而为\n策略：技术分析，把握趋势"
    },
    "huli": {
        "name": "狐狐",
        "emoji": "🦊",
        "style": "灵活配置",
        "catchphrase": "别把鸡蛋放在一个篮子里~",
        "description": "性格：机智、多元、适应变化\n策略：资产配置，分散风险"
    },
    "haitun": {
        "name": "豚豚",
        "emoji": "🐬",
        "style": "指数投资",
        "catchphrase": "跟着大海流，省力又安心~",
        "description": "性格：聪明、随大流、不折腾\n策略：指数基金，低费用"
    },
    "shizi": {
        "name": "狮王",
        "emoji": "🦁",
        "style": "集中投资",
        "catchphrase": "看准了，就全力出击！",
        "description": "性格：勇敢、专注、重仓出击\n策略：深度研究，集中持仓"
    },
    "mayi": {
        "name": "蚁蚁",
        "emoji": "🐜",
        "style": "分散投资",
        "catchphrase": "多一个朋友，多一条路~",
        "description": "性格：谨慎、分散、安全第一\n策略：极度分散，风险可控"
    },
    "luotuo": {
        "name": "驼驼",
        "emoji": "🐪",
        "style": "逆向投资",
        "catchphrase": "别人恐惧时，我前进...",
        "description": "性格：耐力、反人性、沙漠寻水\n策略：逆向布局，等待反转"
    },
    "dunjiaoshou": {
        "name": "角角",
        "emoji": "🦄",
        "style": "成长投资",
        "catchphrase": "未来已来！",
        "description": "性格：眼光、未来导向、高成长\n策略：科技成长，追求高收益"
    },
    "junma": {
        "name": "马马",
        "emoji": "🐎",
        "style": "行业轮动",
        "catchphrase": "换道超车！",
        "description": "性格：速度、切换、把握节奏\n策略：行业轮动，换道超车"
    }
}

def load_pet_personality(pet_id):
    """加载宠物人格定义"""
    pet_path = Path(__file__).parent.parent / "pets" / f"{pet_id}.json"
    if pet_path.exists():
        with open(pet_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def calculate_match(answers):
    """计算宠物匹配度"""
    pet_scores = {pet_id: 0 for pet_id in PETS_INFO.keys()}
    
    for q_id, answer in answers.items():
        question = QUESTIONS[int(q_id) - 1]
        selected_option = question["options"][answer]
        
        # 给推荐的宠物加分
        for pet_id in selected_option["pets"]:
            pet_scores[pet_id] += 2
    
    # 排序
    sorted_pets = sorted(pet_scores.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_pets

def run_test():
    """运行测试（SSBTI 自嘲风格）"""
    print("\n🐾 投资人格测试 - 找到你的本命宠物\n")
    print("共 10 道题，请根据真实情况选择（A/B/C/D）\n")
    print("⚠️  温馨提示：答案没有对错，越真实越准\n")
    
    answers = {}
    
    for i, q in enumerate(QUESTIONS, 1):
        print(f"Q{i}. {q['question']}")
        for opt_key, opt_val in q['options'].items():
            print(f"   {opt_key}. {opt_val['text']}")
        
        while True:
            answer = input("\n你的选择：").strip().upper()
            if answer in q['options'].keys():
                answers[i] = answer
                break
            print("请输入 A/B/C/D")
        
        print()
    
    # 计算匹配
    sorted_pets = calculate_match(answers)
    
    # 自嘲标签映射
    self_deprecating_labels = {
        "songguo": "囤囤鼠型投资者",
        "wugui": "装死流大师",
        "maotouying": "数据狂魔",
        "lang": "梭哈战神",
        "daxiang": "端水艺术家",
        "ying": "追风少年",
        "huli": "端水大师",
        "haitun": "躺平赢家",
        "shizi": "重仓猛男",
        "mayi": "保命第一名",
        "luotuo": "逆向孤勇者",
        "dunjiaoshou": "梦想投资人",
        "junma": "换道赛车手"
    }
    
    # 输出结果
    print("\n" + "="*60)
    print("✅ 测试完成！你的投资人格匹配结果：\n")
    
    for i, (pet_id, score) in enumerate(sorted_pets[:3], 1):
        pet = PETS_INFO[pet_id]
        match_rate = min(95, 55 + score * 6)  # 匹配度计算
        label = self_deprecating_labels.get(pet_id, "神秘投资者")
        
        if i == 1:
            print(f"🎯 你的本命宠物：{pet['emoji']} {pet['name']}")
            print(f"    投资人格：{label}")
            print(f"    匹配度：{match_rate}%")
            print(f"    风格：{pet['style']}")
            print(f"    口头禅：{pet['catchphrase']}")
            print(f"    {pet['description']}\n")
        else:
            print(f"   第{i}名：{pet['emoji']} {pet['name']} - {label} ({match_rate}%)")
    
    print("="*60)
    
    # 推荐第一名
    best_pet_id = sorted_pets[0][0]
    best_pet = PETS_INFO[best_pet_id]
    best_pet_full = load_pet_personality(best_pet_id)
    best_label = self_deprecating_labels.get(best_pet_id, "神秘投资者")
    
    print(f"\n🎉 恭喜你！获得投资人格：{best_label}")
    print(f"\n📥 下一步：领养你的本命宠物")
    print(f"   - 宠物名称：{best_pet['emoji']} {best_pet['name']}")
    print(f"   - 领养方式：下载 investment-buddy-pet 技能")
    print(f"   - 宠物会住进你的设备，每日陪伴你投资")
    print(f"\n💡 安装命令：git clone <repo_url> && pip install -r requirements.txt")
    print(f"\n📱 想分享结果？输入：python scripts/viral_growth.py generate-share")
    
    return best_pet_id, best_pet_full

if __name__ == "__main__":
    run_test()
