"""
BehaviorEngine - Child Behavior Analysis and Positive Discipline
"""
from typing import Dict, List

BEHAVIOR_PATTERNS = {
    'attention-seeking': {
        'description': '通过不当行为获取关注',
        'triggers': ['家长忙碌时', '有客人来访时', '兄弟姐妹获得关注时'],
        'typical_behaviors': ['故意捣乱', '大声喊叫', '重复提问'],
        'positive_response': [
            '主动给予关注：每天安排专属的“特别时光”',
            '捕捉好行为：及时表扬安静、专注的时刻',
            '教替代行为：教孩子如何礼貌地请求关注'
        ],
        'mistakes_to_avoid': ['只在孩子捣乱时才关注', '过度反应强化行为', '忽视所有行为']
    },
    'power-struggle': {
        'description': '通过反抗建立控制感',
        'triggers': ['被命令时', '感觉被控制时', '自主权被侵犯时'],
        'typical_behaviors': ['说“不”', '拖延', '故意做相反的事'],
        'positive_response': [
            '提供有限选择：给予2-3个可接受的选择',
            '避免权力斗争：用“我注意到...”代替命令',
            '赋予责任：让孩子承担适当的责任'
        ],
        'mistakes_to_avoid': ['陷入争吵', '威胁惩罚', '情绪化反应']
    },
    'avoidance': {
        'description': '逃避不喜欢的任务或情境',
        'triggers': ['困难任务', '新环境', '社交压力'],
        'typical_behaviors': ['拖延', '抱怨身体不适', '发脾气'],
        'positive_response': [
            '分解任务：将大任务拆分成小步骤',
            '提供支持：陪伴孩子一起开始任务',
            '使用计时器：明确任务时间和休息时间'
        ],
        'mistakes_to_avoid': ['强迫立即完成', '批评拖延', '代替孩子完成任务']
    },
    'sensory-seeking': {
        'description': '通过行为满足感官需求',
        'triggers': ['无聊时', '需要刺激时', '过度兴奋时'],
        'typical_behaviors': ['不停动来动去', '制造噪音', '触摸一切物品'],
        'positive_response': [
            '提供感官活动：如捏橡皮泥、玩沙、荡秋千',
            '建立感官角：准备安全的感官玩具',
            '安排充足活动：确保每天有足够的户外时间'
        ],
        'mistakes_to_avoid': ['惩罚正常感官需求', '限制所有活动', '忽视孩子的需求']
    }
}

POSITIVE_DISCIPLINE_TECHNIQUES = [
    {
        'name': '自然结果法',
        'description': '让孩子体验行为的自然结果',
        'when_to_use': '行为有明确、安全的自然结果时',
        'steps': [
            '提前告知可能的自然结果',
            '允许孩子体验结果（在安全范围内）',
            '事后温和讨论学到了什么'
        ],
        'example': '“如果不穿外套，可能会觉得冷。”'
    },
    {
        'name': '逻辑结果法',
        'description': '设计与行为相关的合理结果',
        'when_to_use': '行为没有明显自然结果时',
        'steps': [
            '结果必须与行为相关',
            '提前告知结果',
            '温和坚定地执行'
        ],
        'example': '“玩具乱扔不收拾，明天就不能玩这些玩具。”'
    },
    {
        'name': '积极暂停',
        'description': '帮助孩子平静情绪，不是惩罚',
        'when_to_use': '孩子情绪失控时',
        'steps': [
            '创建舒适的“冷静角”',
            '教孩子情绪平静技巧',
            '情绪平复后讨论解决方案'
        ],
        'example': '“你需要去冷静角平静一下吗？我们可以一起深呼吸。”'
    },
    {
        'name': '问题解决会议',
        'description': '与孩子共同寻找解决方案',
        'when_to_use': '重复出现的行为问题',
        'steps': [
            '选择平静的时间',
            '轮流表达感受和需求',
            '共同头脑风暴解决方案',
            '选择并试行一个方案'
        ],
        'example': '“我们都有点困扰睡前拖延，一起想想有什么办法能让睡前更顺利？”'
    }
]

class BehaviorEngine:
    def __init__(self):
        self.name = 'BehaviorEngine'

    def analyze_behavior(self, behavior_description, frequency, context):
        """分析行为背后的可能原因"""
        possible_patterns = []
        
        for pattern_name, pattern in BEHAVIOR_PATTERNS.items():
            # Check if behavior matches typical behaviors
            behavior_match = any(b in behavior_description for b in pattern['typical_behaviors'])
            context_match = any(c in context for c in pattern['triggers'])
            
            if behavior_match or context_match:
                confidence = 'high' if behavior_match and context_match else 'medium'
                possible_patterns.append({
                    'pattern': pattern_name,
                    'description': pattern['description'],
                    'confidence': confidence,
                    'triggers': pattern['triggers'],
                    'suggested_response': pattern['positive_response'][:2]
                })
        
        return {
            'behavior_analysis': {
                'description': behavior_description,
                'frequency': frequency,
                'context': context
            },
            'possible_patterns': possible_patterns,
            'recommended_techniques': POSITIVE_DISCIPLINE_TECHNIQUES[:2]
        }

    def get_positive_discipline_plan(self, pattern_name, child_age_months):
        """生成正向管教计划"""
        pattern = BEHAVIOR_PATTERNS.get(pattern_name)
        if not pattern:
            return {'error': 'Pattern not found'}
        
        # Age-appropriate adaptations
        adaptations = []
        if child_age_months < 24:
            adaptations = ['使用更简单的语言', '更多示范和引导', '保持一致性']
        elif child_age_months < 48:
            adaptations = ['加入简单解释', '使用视觉提示', '提供有限选择']
        else:
            adaptations = ['可以讨论感受', '共同制定规则', '赋予更多责任']
        
        return {
            'pattern': pattern_name,
            'description': pattern['description'],
            'age_adaptations': adaptations,
            'prevention_strategies': pattern.get('prevention_strategies', []),
            'positive_responses': pattern['positive_response'],
            'techniques_to_try': POSITIVE_DISCIPLINE_TECHNIQUES[:3],
            'mistakes_to_avoid': pattern['mistakes_to_avoid']
        }
