"""
CommunicationEngine - Parent-Child Communication Guidance
"""
from typing import Dict, List

COMMUNICATION_DB = {
    'tantrum': {
        'scenario': '孩子发脾气、哭闹',
        'techniques': [
            {
                'name': '共情式倾听',
                'description': '先承认孩子的情绪，再处理行为',
                'steps': ['蹲下与孩子平视', '用平静的语气说“我看到你很生气/难过”', '描述你观察到的“因为玩具坏了，所以你很伤心”', '等待孩子情绪平复后再讨论解决方案'],
                'example_scripts': {
                    'effective': '“我知道你很想要这个玩具，现在坏了你很伤心。我们一起看看能不能修好它。”',
                    'ineffective': '“别哭了！再哭我就不理你了！”'
                }
            },
            {
                'name': '提供有限选择',
                'description': '给孩子有限的选择权，增加控制感',
                'steps': ['提供2-3个可接受的选择', '用简单清晰的语言表达', '尊重孩子的选择并执行'],
                'example_scripts': {
                    'effective': '“你是想先穿袜子还是先穿鞋子？”',
                    'ineffective': '“快穿衣服！”'
                }
            }
        ],
        'common_mistakes': ['与孩子争吵', '威胁惩罚', '忽视情绪'],
        'prevention_strategies': ['建立日常规律', '提前预告变化', '确保孩子基本需求得到满足']
    },
    'refusal': {
        'scenario': '孩子拒绝配合（如不收拾玩具、不吃饭）',
        'techniques': [
            {
                'name': '游戏化引导',
                'description': '将任务转化为游戏',
                'steps': ['创造有趣的游戏场景', '加入计时或比赛元素', '夸张地表扬进步'],
                'example_scripts': {
                    'effective': '“我们来比赛，看谁先把积木送回家！”',
                    'ineffective': '“快点收拾，不然没收玩具！”'
                }
            },
            {
                'name': '自然结果法',
                'description': '让孩子体验行为的自然结果',
                'steps': ['提前告知可能的后果', '允许孩子体验自然结果', '事后讨论学习'],
                'example_scripts': {
                    'effective': '“如果不收拾玩具，明天可能就找不到它们了。”',
                    'ineffective': '“你不收拾我就全扔了！”'
                }
            }
        ],
        'common_mistakes': ['权力斗争', '反复唠叨', '情绪化反应'],
        'prevention_strategies': ['建立清晰的规则和惯例', '给予过渡时间', '提供适当的自主权']
    },
    'sharing': {
        'scenario': '孩子不愿分享玩具',
        'techniques': [
            {
                'name': '轮流计时法',
                'description': '用计时器明确轮流时间',
                'steps': ['设置计时器（如2分钟）', '明确宣布轮流规则', '严格执行计时'],
                'example_scripts': {
                    'effective': '“我们用计时器，每人玩2分钟，时间到了就换人。”',
                    'ineffective': '“你是哥哥要让着弟弟！”'
                }
            },
            {
                'name': '特殊物品尊重',
                'description': '允许孩子保留特别珍爱的物品',
                'steps': ['提前和孩子商量哪些是“特别玩具”', '将这些玩具放在安全地方', '教孩子如何礼貌拒绝分享特别物品'],
                'example_scripts': {
                    'effective': '“这个小熊是你的好朋友，你可以不分享。其他玩具我们轮流玩好吗？”',
                    'ineffective': '“小气鬼！什么都要自己玩！”'
                }
            }
        ],
        'common_mistakes': ['强迫分享', '贴标签（小气）', '比较孩子'],
        'prevention_strategies': ['提前准备足够的玩具', '示范分享行为', '表扬分享时刻']
    },
    'bedtime': {
        'scenario': '睡前拖延、不肯睡觉',
        'techniques': [
            {
                'name': '可视化睡前程序',
                'description': '用图片展示睡前步骤',
                'steps': ['制作睡前程序图表', '每完成一步贴贴纸', '保持程序一致性'],
                'example_scripts': {
                    'effective': '“看，我们已经完成了刷牙、换睡衣，现在该讲故事了。”',
                    'ineffective': '“都几点了还不睡！”'
                }
            },
            {
                'name': '有限选择+计时器',
                'description': '结合选择和计时减少拖延',
                'steps': ['提供有限选择“你想听一个故事还是两个？”', '使用计时器明确时间限制', '温和坚定地执行'],
                'example_scripts': {
                    'effective': '“计时器响了我们就关灯，你可以选择听一个长故事或两个短故事。”',
                    'ineffective': '“再不睡明天别想看电视！”'
                }
            }
        ],
        'common_mistakes': ['情绪化威胁', '不断让步', '程序不一致'],
        'prevention_strategies': ['建立固定的睡前程序', '确保白天充足活动', '创造舒适的睡眠环境']
    }
}

class CommunicationEngine:
    def __init__(self):
        self.name = 'CommunicationEngine'

    def get_guidance(self, scenario, child_age_months=None):
        guidance = COMMUNICATION_DB.get(scenario)
        if not guidance:
            return {'error': 'Scenario not found'}
        
        result = {
            'scenario': guidance['scenario'],
            'techniques': guidance['techniques'],
            'common_mistakes': guidance['common_mistakes'],
            'prevention_strategies': guidance['prevention_strategies']
        }
        
        # Age-specific adaptations
        if child_age_months:
            if child_age_months < 36:  # Under 3 years
                result['age_adaptation'] = '对于幼儿，语言要更简单，示范比说教更重要'
            else:  # 3+ years
                result['age_adaptation'] = '对于学龄前儿童，可以加入更多解释和讨论'
        
        return result

    def generate_script(self, scenario, technique_name):
        guidance = COMMUNICATION_DB.get(scenario)
        if not guidance:
            return {'error': 'Scenario not found'}
        
        for technique in guidance['techniques']:
            if technique['name'] == technique_name:
                return {
                    'technique': technique,
                    'practice_exercises': [
                        '角色扮演：家长和孩子互换角色',
                        '录像回放：录下互动过程一起观看讨论',
                        '渐进练习：从简单场景开始逐渐增加难度'
                    ]
                }
        
        return {'error': 'Technique not found'}
