"""
ActivityEngine - Age-Appropriate Activity Recommendation Engine
"""
from typing import Dict, List

ACTIVITY_DB = {
    (0, 3): [
        {'id': 'act_0_3_1', 'name': '追视练习', 'domains': ['cognitive', 'gross-motor'],
         'difficulty': 'easy', 'duration_minutes': 5,
         'materials': ['黑白卡', '红球'],
         'steps': ['将黑白卡放在宝宝视线前20-30cm', '缓慢左右移动卡片，观察宝宝眼睛跟随', '每天2-3次，每次3-5分钟'],
         'safety_notes': ['确保卡片边缘光滑', '不要在宝宝哭闹时进行']},
        {'id': 'act_0_3_2', 'name': '俯趴抬头', 'domains': ['gross-motor'],
         'difficulty': 'easy', 'duration_minutes': 10,
         'materials': ['软垫', '彩色玩具'],
         'steps': ['在软垫上让宝宝俯卧', '用彩色玩具在前方吸引注意力', '逐渐延长时间'],
         'safety_notes': ['选择宝宝清醒时进行', '注意观察是否疲劳']}
    ],
    (3, 6): [
        {'id': 'act_3_6_1', 'name': '抓握游戏', 'domains': ['fine-motor', 'cognitive'],
         'difficulty': 'easy', 'duration_minutes': 10,
         'materials': ['摇铃', '布书', '软积木'],
         'steps': ['选择不同材质的玩具让宝宝抓握', '描述玩具的颜色、材质', '鼓励换手传递'],
         'safety_notes': ['玩具需无毒、大件（防止误吞）']},
        {'id': 'act_3_6_2', 'name': '翻身练习', 'domains': ['gross-motor'],
         'difficulty': 'medium', 'duration_minutes': 15,
         'materials': ['软垫', '吸引注意力的玩具'],
         'steps': ['宝宝仰卧，在侧面用玩具引导', '轻轻推送宝宝侧身', '逐渐减少辅助直至独立翻身'],
         'safety_notes': ['选择柔软地面', '不要在刚吃完奶后进行']}
    ],
    (6, 12): [
        {'id': 'act_6_12_1', 'name': '爬行隧道', 'domains': ['gross-motor', 'cognitive'],
         'difficulty': 'medium', 'duration_minutes': 20,
         'materials': ['纸箱', '毯子', '玩具'],
         'steps': ['用纸箱和毯子搭建小隧道', '在另一端放玩具吸引爬行', '家庭成员轮流在隧道另一端呼唤'],
         'safety_notes': ['确保纸箱边缘光滑无刺', '全程看护']},
        {'id': 'act_6_12_2', 'name': '敲击乐器', 'domains': ['fine-motor', 'cognitive', 'language'],
         'difficulty': 'easy', 'duration_minutes': 15,
         'materials': ['塑料碗', '木勺', '空奶粉罐'],
         'steps': ['示范敲击不同物体发出不同声音', '让宝宝自由探索敲击', '配合简单节拍念唱'],
         'safety_notes': ['确保容器无尖锐边缘', '防止敲击到手指']},
        {'id': 'act_6_12_3', 'name': '躲猫猫', 'domains': ['cognitive', 'social-emotional'],
         'difficulty': 'easy', 'duration_minutes': 10,
         'materials': ['毯子', '毛绒玩具'],
         'steps': ['用毯子遮住脸问宝宝在哪', '掀开毯子说找到啦', '用玩具重复此游戏'],
         'safety_notes': ['确保毯子透气轻薄']}
    ],
    (12, 24): [
        {'id': 'act_12_24_1', 'name': '积木叠叠乐', 'domains': ['fine-motor', 'cognitive'],
         'difficulty': 'medium', 'duration_minutes': 20,
         'materials': ['软积木', '套圈玩具'],
         'steps': ['示范叠高2-3块积木', '鼓励宝宝模仿', '数数：一块、两块、三块'],
         'safety_notes': ['选择轻质软积木防止砸脚']},
        {'id': 'act_12_24_2', 'name': '假想过家家', 'domains': ['cognitive', 'language', 'social-emotional'],
         'difficulty': 'easy', 'duration_minutes': 15,
         'materials': ['玩具厨房', '塑料食物', '餐具'],
         'steps': ['设置假想场景如做饭', '引导宝宝给玩偶喂饭', '描述正在进行的动作'],
         'safety_notes': ['玩具食材需足够大防止误吞']},
        {'id': 'act_12_24_3', 'name': '户外感官探索', 'domains': ['gross-motor', 'cognitive'],
         'difficulty': 'easy', 'duration_minutes': 30,
         'materials': ['沙坑', '草地'],
         'steps': ['带宝宝在安全环境中自由探索', '描述触感和感受：沙子是细细的、草是软软的', '注意安全，不让宝宝将异物放入口中'],
         'safety_notes': ['户外需全程看护', '注意防晒防蚊']}
    ],
    (24, 36): [
        {'id': 'act_24_36_1', 'name': '角色扮演游戏', 'domains': ['cognitive', 'language', 'social-emotional'],
         'difficulty': 'medium', 'duration_minutes': 25,
         'materials': ['道具服装', '玩偶', '玩具家具'],
         'steps': ['确定一个场景如医生看病', '家长示范如何与玩偶互动', '让宝宝主导游戏过程'],
         'safety_notes': ['道具需安全无小零件']},
        {'id': 'act_24_36_2', 'name': '简单粘贴画', 'domains': ['fine-motor', 'cognitive', 'creative'],
         'difficulty': 'easy', 'duration_minutes': 20,
         'materials': ['彩纸', '胶水', '画笔'],
         'steps': ['示范撕纸动作', '让宝宝自由撕扯彩纸', '一起将撕下的纸片贴在另一张纸上组成图案'],
         'safety_notes': ['使用儿童安全剪刀，需在成人指导下使用']},
        {'id': 'act_24_36_3', 'name': '球类互动', 'domains': ['gross-motor', 'social-emotional'],
         'difficulty': 'easy', 'duration_minutes': 20,
         'materials': ['不同大小的球'],
         'steps': ['示范踢球、抛球、接球', '从近距离开始逐渐增加距离', '鼓励与同伴一起玩'],
         'safety_notes': ['选择柔软的球', '注意周围无尖锐物']}
    ],
    (36, 60): [
        {'id': 'act_36_60_1', 'name': '合作搭建', 'domains': ['cognitive', 'social-emotional', 'fine-motor'],
         'difficulty': 'hard', 'duration_minutes': 40,
         'materials': ['积木', '磁力片', '纸箱'],
         'steps': ['设定搭建目标如建一座桥', '分工合作完成搭建', '讨论遇到的问题和解决方法'],
         'safety_notes': ['积木需稳固防止倒塌砸伤']},
        {'id': 'act_36_60_2', 'name': '棋盘游戏', 'domains': ['cognitive', 'social-emotional'],
         'difficulty': 'medium', 'duration_minutes': 30,
         'materials': ['简单桌游', '飞行棋', '记忆卡牌'],
         'steps': ['选择适合年龄的桌游', '讲解规则并示范', '鼓励轮流进行，正确对待输赢'],
         'safety_notes': ['游戏配件需适合年龄，防止误吞']},
        {'id': 'act_36_60_3', 'name': '科学小实验', 'domains': ['cognitive', 'science', 'fine-motor'],
         'difficulty': 'medium', 'duration_minutes': 30,
         'materials': ['白醋', '小苏打', '食用色素', '杯子'],
         'steps': ['往杯中加入小苏打', '滴入几滴食用色素', '倒入白醋观察反应', '解释火山爆发的原理'],
         'safety_notes': ['材料需安全无毒', '在成人监督下进行']}
    ]
}

class ActivityEngine:
    def __init__(self):
        self.name = 'ActivityEngine'

    def get_age_range(self, age_months):
        ranges = [(0, 3), (3, 6), (6, 12), (12, 24), (24, 36), (36, 60)]
        for r in ranges:
            if r[0] <= age_months < r[1]:
                return r
        return (36, 60)

    def recommend_activities(self, age_months, available_time=30, preferred_domains=None):
        age_range = self.get_age_range(age_months)
        activities = ACTIVITY_DB.get(age_range, ACTIVITY_DB[(36, 60)])
        suitable = []
        for a in activities:
            if a['duration_minutes'] <= available_time:
                if preferred_domains is None or any(d in a['domains'] for d in preferred_domains):
                    suitable.append(a)
        return {
            'age_range': str(age_range[0]) + '-' + str(age_range[1]) + '个月',
            'recommended_activities': suitable,
            'summary': {'total_available': len(suitable), 'most_relevant': [a['name'] for a in suitable[:3]]}
        }

    def get_activity_detail(self, activity_id):
        for activities in ACTIVITY_DB.values():
            for a in activities:
                if a['id'] == activity_id:
                    return a
        return {}
