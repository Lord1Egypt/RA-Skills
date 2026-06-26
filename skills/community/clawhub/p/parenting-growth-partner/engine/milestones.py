"""
MilestoneEngine - Child Development Milestone Tracking
"""
from typing import Dict, List

DOMAINS = {
    'gross-motor': '大运动',
    'fine-motor': '精细动作',
    'language': '语言',
    'cognitive': '认知',
    'social-emotional': '社会情感',
    'adaptive': '适应能力'
}

MILESTONE_DB = {
    (0, 3): {
        'gross-motor': [
            {'id': 'gm_0_3_1', 'description': '俯卧时能抬头', 'typical': ['抬头45度'], 'advanced': ['抬头90度']},
            {'id': 'gm_0_3_2', 'description': '四肢活动良好', 'typical': ['四肢无规律舞动'], 'advanced': []}
        ],
        'fine-motor': [
            {'id': 'fm_0_3_1', 'description': '手握拳', 'typical': ['紧紧握拳'], 'advanced': ['能抓住拨浪鼓']}
        ],
        'language': [
            {'id': 'la_0_3_1', 'description': '发出喉音', 'typical': ['咕咕声、咯咯声'], 'advanced': ['能发元音a,o']}
        ],
        'cognitive': [
            {'id': 'cg_0_3_1', 'description': '追视移动物体', 'typical': ['眼睛跟随人脸'], 'advanced': ['追视红球180度']}
        ],
        'social-emotional': [
            {'id': 'se_0_3_1', 'description': '对声音有反应', 'typical': ['听到声音停止活动'], 'advanced': ['转头寻找声源']}
        ],
        'adaptive': [
            {'id': 'ad_0_3_1', 'description': '建立喂养和睡眠规律', 'typical': ['开始形成规律'], 'advanced': []}
        ]
    },
    (3, 6): {
        'gross-motor': [
            {'id': 'gm_3_6_1', 'description': '翻身', 'typical': ['从仰卧翻到俯卧'], 'advanced': ['从俯卧翻到仰卧']},
            {'id': 'gm_3_6_2', 'description': '坐立', 'typical': ['撑手独坐片刻'], 'advanced': ['独坐较稳']}
        ],
        'fine-motor': [
            {'id': 'fm_3_6_1', 'description': '伸手抓握', 'typical': ['主动抓握玩具'], 'advanced': ['换手传递']}
        ],
        'language': [
            {'id': 'la_3_6_1', 'description': '发出音节', 'typical': ['ma,ba,da音节'], 'advanced': ['模仿声音']}
        ],
        'cognitive': [
            {'id': 'cg_3_6_1', 'description': '认识熟悉的人', 'typical': ['看到妈妈有反应'], 'advanced': ['主动寻求互动']}
        ],
        'social-emotional': [
            {'id': 'se_3_6_1', 'description': '开始认生', 'typical': ['对陌生人有反应'], 'advanced': ['明显依恋主要照护人']}
        ],
        'adaptive': [
            {'id': 'ad_3_6_1', 'description': '开始添加辅食', 'typical': ['接受勺喂'], 'advanced': ['能够自己拿食物']}
        ]
    },
    (6, 12): {
        'gross-motor': [
            {'id': 'gm_6_12_1', 'description': '爬行', 'typical': ['四肢爬行'], 'advanced': ['扶站扶走']},
            {'id': 'gm_6_12_2', 'description': '站立和行走', 'typical': ['独站片刻'], 'advanced': ['独立行走几步']}
        ],
        'fine-motor': [
            {'id': 'fm_6_12_1', 'description': '捏取小物品', 'typical': ['拇指食指捏起'], 'advanced': ['叠积木2-3块']}
        ],
        'language': [
            {'id': 'la_6_12_1', 'description': '理解简单词汇', 'typical': ['听懂再见'], 'advanced': ['叫爸妈']}
        ],
        'cognitive': [
            {'id': 'cg_6_12_1', 'description': '客体永久性', 'typical': ['找藏起的玩具'], 'advanced': ['用工具够玩具']}
        ],
        'social-emotional': [
            {'id': 'se_6_12_1', 'description': '分离焦虑', 'typical': ['主要照护人离开时哭闹'], 'advanced': []}
        ],
        'adaptive': [
            {'id': 'ad_6_12_1', 'description': '自主进食意愿', 'typical': ['抢勺子'], 'advanced': ['用杯子喝水']}
        ]
    },
    (12, 24): {
        'gross-motor': [
            {'id': 'gm_12_24_1', 'description': '独立行走', 'typical': ['走得熟练'], 'advanced': ['能跑']},
            {'id': 'gm_12_24_2', 'description': '攀爬', 'typical': ['爬上椅子'], 'advanced': ['双脚跳']}
        ],
        'fine-motor': [
            {'id': 'fm_12_24_1', 'description': '搭积木', 'typical': ['叠2-3块'], 'advanced': ['叠4-6块']}
        ],
        'language': [
            {'id': 'la_12_24_1', 'description': '说单词', 'typical': ['10-50个词汇'], 'advanced': ['说短句']}
        ],
        'cognitive': [
            {'id': 'cg_12_24_1', 'description': '假想游戏', 'typical': ['拿玩具电话假装打电话'], 'advanced': []}
        ],
        'social-emotional': [
            {'id': 'se_12_24_1', 'description': '同伴意识', 'typical': ['看其他孩子玩'], 'advanced': ['出现社交互动']}
        ],
        'adaptive': [
            {'id': 'ad_12_24_1', 'description': '使用勺子', 'typical': ['较熟练使用'], 'advanced': []}
        ]
    },
    (24, 36): {
        'gross-motor': [
            {'id': 'gm_24_36_1', 'description': '跑跳能力', 'typical': ['能跑但不稳'], 'advanced': ['双脚交替上下楼梯']},
            {'id': 'gm_24_36_2', 'description': '大动作协调', 'typical': ['踢球'], 'advanced': ['骑三轮车']}
        ],
        'fine-motor': [
            {'id': 'fm_24_36_1', 'description': '精细动作发展', 'typical': ['用蜡笔涂鸦'], 'advanced': ['模仿画直线']}
        ],
        'language': [
            {'id': 'la_24_36_1', 'description': '语言爆发期', 'typical': ['词汇量快速增长'], 'advanced': ['说完整句子']}
        ],
        'cognitive': [
            {'id': 'cg_24_36_1', 'description': '平行游戏到合作游戏', 'typical': ['各玩各的'], 'advanced': ['开始简单合作']}
        ],
        'social-emotional': [
            {'id': 'se_24_36_1', 'description': '自我意识发展', 'typical': ['说'我''], 'advanced': ['用名字称呼自己']}
        ],
        'adaptive': [
            {'id': 'ad_24_36_1', 'description': '如厕训练准备', 'typical': ['白天能控制排尿'], 'advanced': ['能表达如厕需求']}
        ]
    },
    (36, 60): {
        'gross-motor': [
            {'id': 'gm_36_60_1', 'description': '平衡与协调', 'typical': ['单脚站1-2秒'], 'advanced': ['单脚站5秒以上']},
            {'id': 'gm_36_60_2', 'description': '跳跃', 'typical': ['并脚跳'], 'advanced': ['单脚跳']}
        ],
        'fine-motor': [
            {'id': 'fm_36_60_1', 'description': '书写准备', 'typical': ['描摹图形'], 'advanced': ['写出简单字']}
        ],
        'language': [
            {'id': 'la_36_60_1', 'description': '语言表达', 'typical': ['说完整故事'], 'advanced': ['复述发生的事情']}
        ],
        'cognitive': [
            {'id': 'cg_36_60_1', 'description': '数感发展', 'typical': ['数数1-10'], 'advanced': ['理解数量关系']}
        ],
        'social-emotional': [
            {'id': 'se_36_60_1', 'description': '亲社会行为', 'typical': ['分享玩具'], 'advanced': ['安慰其他孩子']}
        ],
        'adaptive': [
            {'id': 'ad_36_60_1', 'description': '自理能力', 'typical': ['独立穿衣'], 'advanced': ['学会系扣子']}
        ]
    }
}

RED_FLAG_THRESHOLDS = {
    3: {'gross-motor': '不能抬头', 'language': '对声音无反应'},
    6: {'gross-motor': '不能翻身', 'language': '不发出任何声音'},
    12: {'gross-motor': '不能独坐', 'language': '不懂简单指令'},
    24: {'gross-motor': '不能独立行走', 'language': '不会说单词'},
    36: {'language': '不能说短句', 'cognitive': '不理解简单指令'},
    60: {'language': '不能说完整句子', 'cognitive': '无法数数'}
}

class MilestoneEngine:
    def __init__(self):
        self.name = 'MilestoneEngine'

    def get_age_range(self, age_months):
        ranges = [(0, 3), (3, 6), (6, 12), (12, 24), (24, 36), (36, 60)]
        for r in ranges:
            if r[0] <= age_months < r[1]:
                return r
        return (36, 60)

    def assess_milestones(self, age_months, observations=None):
        age_range = self.get_age_range(age_months)
        domain_data = MILESTONE_DB.get(age_range, MILESTONE_DB[(36, 60)])
        achieved = []
        upcoming = []
        at_risk = []
        for domain, milestones in domain_data.items():
            for m in milestones:
                status = 'typical'
                if observations and domain in observations:
                    for tb in m.get('typical', []):
                        if tb in str(observations[domain]):
                            status = 'achieved'
                achieved.append({'id': m['id'], 'domain': domain, 'domain_cn': DOMAINS.get(domain, domain), 'description': m['description'], 'status': status})
            all_ranges = sorted(MILESTONE_DB.keys())
            next_range = None
            for r in all_ranges:
                if r[0] == age_range[1]:
                    next_range = r
                    break
            if next_range:
                for m in MILESTONE_DB[next_range].get(domain, []):
                    upcoming.append({'id': m['id'], 'domain': domain, 'domain_cn': DOMAINS.get(domain, domain), 'description': m['description'], 'next_age_range': str(next_range[0]) + '-' + str(next_range[1]) + '个月'})
        if age_months in RED_FLAG_THRESHOLDS:
            for domain, flag_desc in RED_FLAG_THRESHOLDS[age_months].items():
                if observations and domain in observations:
                    if not any(m['domain'] == domain and m['status'] == 'achieved' for m in achieved):
                        at_risk.append({'domain': domain, 'domain_cn': DOMAINS.get(domain, domain), 'warning': flag_desc, 'recommendation': '建议咨询专业人士'})
        return {'age_months': age_months, 'age_range': str(age_range[0]) + '-' + str(age_range[1]) + '个月', 'total_milestones_checked': len(achieved), 'achieved': achieved, 'upcoming': upcoming[:6], 'red_flags': at_risk, 'summary': {'milestones_achieved_count': len([m for m in achieved if m.get('status') == 'achieved']), 'development_status': 'at_risk' if at_risk else 'on_track'}}

    def generate_recommendations(self, assessment):
        recommendations = []
        if assessment['summary']['development_status'] == 'at_risk':
            recommendations.append({'type': 'professional', 'priority': 'high', 'title': '建议寻求专业评估', 'description': '发现潜在发展预警信号，建议联系儿科医生或儿童发展专家'})
        achieved_count = assessment['summary']['milestones_achieved_count']
        if achieved_count < 3:
            recommendations.append({'type': 'activity', 'priority': 'medium', 'title': '加强日常互动', 'description': '通过日常游戏和互动支持该年龄段的发展'})
        for upcoming in assessment.get('upcoming', [])[:2]:
            recommendations.append({'type': 'activity', 'priority': 'low', 'title': '预备' + upcoming['domain_cn'] + '发展', 'description': '下一阶段可关注：' + upcoming['description']})
        return recommendations
