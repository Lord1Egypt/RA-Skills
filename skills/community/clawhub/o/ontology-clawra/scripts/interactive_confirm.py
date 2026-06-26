#!/usr/bin/env python3
"""
ontology-clawra 渐进式交互确认模块
每次只问1-2个核心问题，根据回答动态调整
"""

from typical_scenarios import TYPICAL_SCENARIOS, generate_confirmation_questions


class InteractiveConfirm:
    """渐进式交互确认器"""
    
    def __init__(self, category):
        self.category = category
        self.user_answers = {}
        self.questions_asked = 0
        self.max_questions = 3  # 每次最多问3个问题
        
        # 获取该类别的确认问题
        self.all_questions = generate_confirmation_questions(category, {})
    
    def get_next_question(self):
        """获取下一个问题"""
        if self.questions_asked >= len(self.all_questions):
            return None
        
        q, options, default = self.all_questions[self.questions_asked]
        return {
            "question": q,
            "options": options,
            "default": default,
            "question_num": self.questions_asked + 1,
            "total_questions": len(self.all_questions)
        }
    
    def submit_answer(self, answer):
        """提交回答"""
        if self.questions_asked < len(self.all_questions):
            q, _, default = self.all_questions[self.questions_asked]
            # 处理用户可能回答了简化答案
            self.user_answers[q] = answer if answer else default
            self.questions_asked += 1
            return True
        return False
    
    def is_complete(self):
        """是否完成所有问题"""
        return self.questions_asked >= len(self.all_questions)
    
    def get_current_scenario(self):
        """获取当前匹配的典型场景"""
        # 转换用户回答格式
        answer_map = {}
        for q, a in self.user_answers.items():
            if "地区" in q:
                answer_map["region"] = "南方" if "南方" in a else "北方"
            elif "供暖" in q:
                answer_map["has_heating"] = "是" in a
            elif "类型" in q:
                if "多层" in a:
                    answer_map["building_type"] = "多层"
                elif "高层" in a:
                    answer_map["building_type"] = "高层"
                else:
                    answer_map["building_type"] = "超高层"
            elif "设备" in q:
                answer_map["gas_devices"] = a
        
        # 尝试匹配场景
        from typical_scenarios import match_scenario
        return match_scenario(self.category, answer_map)
    
    def generate_intro_message(self):
        """生成引导消息"""
        intros = {
            "gas_regulator": """🏠 **调压箱选型确认**

为了给出准确的选型结果，需要确认几个关键问题：
（每次只需回答1-2个问题）""",
            "restaurant": """🍽️ **餐厅用气确认**

需要确认以下信息："""
        }
        return intros.get(self.category, "需要确认以下信息：")


def quick_confirm(category, question):
    """
    快速确认 - 用于单个问题
    返回: (问题文本, 选项列表, 默认值)
    """
    questions = generate_confirmation_questions(category, {})
    for q, options, default in questions:
        if any(keyword in q for keyword in question.split()):
            return q, options, default
    return None, None, None


def generate_scenario_options(category):
    """生成场景选项（用于选择而非问答）"""
    if category not in TYPICAL_SCENARIOS:
        return []
    
    scenarios = TYPICAL_SCENARIOS[category]["scenarios"]
    options = []
    for key, scenario in scenarios.items():
        options.append({
            "key": key,
            "name": scenario["name"],
            "description": scenario["description"],
            "result": scenario.get("calculation", {}).get("example_result", "")
        })
    
    return options


def main():
    """测试"""
    print("=" * 50)
    print("渐进式交互确认测试")
    print("=" * 50)
    
    # 初始化
    confirm = InteractiveConfirm("gas_regulator")
    
    # 引导消息
    print("\n" + confirm.generate_intro_message())
    
    # 逐个提问
    while not confirm.is_complete():
        q = confirm.get_next_question()
        if not q:
            break
        
        print(f"\n❓ 问题 {q['question_num']}/{q['total_questions']}: {q['question']}")
        print(f"   选项: {q['options']}")
        print(f"   默认: {q['default']}")
        
        # 模拟用户回答
        confirm.submit_answer(q['default'])
    
    # 输出结果
    print("\n" + "=" * 50)
    print("📊 用户回答汇总:")
    for k, v in confirm.user_answers.items():
        print(f"  • {k}: {v}")
    
    # 匹配场景
    scenario = confirm.get_current_scenario()
    if scenario:
        print(f"\n🎯 匹配场景: {scenario['name']}")
        print(f"   计算结果: {scenario['calculation']['example_result']}")
    else:
        print("\n⚠️ 未能匹配到典型场景")


if __name__ == "__main__":
    main()
