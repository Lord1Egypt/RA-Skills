#!/usr/bin/env python3
"""
MBTI Guru - 职场人际与情侣匹配数据
包含16种MBTI类型的职场建议和关系匹配
"""

WORKPLACE_DATA = {
    "INTJ": {
        "best_environment": "独立工作、有明确目标、能发挥战略思维的环境",
        "worst_environment": "需要频繁社交、缺乏自主性、强调服从的环境",
        "team_role": "战略规划者、问题解决者、创新推动者",
        "leadership_style": "理性领导，注重效率和结果",
        "collaboration_tips": [
            "给他们足够的独立空间和时间",
            "用数据和逻辑说服他们",
            "避免情绪化的讨论",
            "欣赏他们的战略眼光"
        ],
        "stress_response": "退缩到内心世界，需要独处时间来恢复"
    },
    "INTP": {
        "best_environment": "允许深入研究、有弹性工作时间、重视智识的环境",
        "worst_environment": "高压销售环境、过度社交、缺乏自主性的环境",
        "team_role": "分析师、研究者、技术专家",
        "leadership_style": "民主型领导，鼓励独立思考",
        "collaboration_tips": [
            "不要期望他们热情洋溢",
            "给他们时间思考和提出问题",
            "提供清晰的逻辑框架",
            "欣赏他们的创新想法"
        ],
        "stress_response": "过度分析，需要休息大脑"
    },
    "ENTJ": {
        "best_environment": "竞争性环境、有明确晋升通道、能发挥领导才能的环境",
        "worst_environment": "官僚主义严重、缺乏挑战、死气沉沉的环境",
        "team_role": "领导者、决策者、组织者",
        "leadership_style": "命令式领导，目标导向",
        "collaboration_tips": [
            "尊重他们的能力和权威",
            "直接坦诚地沟通",
            "不要浪费他们的时间",
            "提供有挑战性的任务"
        ],
        "stress_response": "更加咄咄逼人，需要掌控局面"
    },
    "ENTP": {
        "best_environment": "创新型企业、多元文化、充满辩论机会的环境",
        "worst_environment": "重复性工作、过度规范、死板的环境",
        "team_role": "创新者、谈判者、问题解决者",
        "leadership_style": "魅力型领导，善于激励团队",
        "collaboration_tips": [
            "欢迎他们的新想法",
            "不要限制他们的讨论",
            "提供智力刺激",
            "欣赏他们的多才多艺"
        ],
        "stress_response": "更加活跃，可能过度承诺"
    },
    "INFJ": {
        "best_environment": "有使命感、能帮助他人、创意与理想并存的非营利或教育机构",
        "worst_environment": "冷漠功利、缺乏价值观、勾心斗角的环境",
        "team_role": "理想主义者、激励者、价值观守护者",
        "leadership_style": "服务型领导，关注成员成长",
        "collaboration_tips": [
            "欣赏他们的理想主义",
            "给他们意义和目标",
            "不要强迫他们做不喜欢的事",
            "保护他们的隐私"
        ],
        "stress_response": "退缩独处，可能对人性失望"
    },
    "INFP": {
        "best_environment": "创意行业、教育、心理咨询、有自我表达空间的非营利组织",
        "worst_environment": "高压销售、过度竞争、扼杀创意的大型企业",
        "team_role": "理想主义者、调解者、创意提供者",
        "leadership_style": "民主型领导，注重价值观",
        "collaboration_tips": [
            "尊重他们的价值观",
            "允许他们按自己的方式工作",
            "给他们创造性的空间",
            "欣赏他们的同理心"
        ],
        "stress_response": "自我怀疑，可能逃避现实"
    },
    "ENFJ": {
        "best_environment": "教育、培训、咨询、团队领导、人力资源管理",
        "worst_environment": "需要独立工作、缺乏人际互动、技术性过强的环境",
        "team_role": "激励者、团队建设者、导师",
        "leadership_style": "魅力型领导，善于激励人心",
        "collaboration_tips": [
            "真诚地认可他们的贡献",
            "给他们带领团队的机会",
            "不要忽视他们的情感需求",
            "提供社交互动的机会"
        ],
        "stress_response": "过度承担责任，可能忽视自己"
    },
    "ENFP": {
        "best_environment": "创意行业、营销、咨询、有灵活性和刺激性的创业环境",
        "worst_environment": "重复性工作、过度规范、缺乏变化的环境",
        "team_role": "激励者、创新者、项目推动者",
        "leadership_style": "魅力型领导，充满热情",
        "collaboration_tips": [
            "给他们表达想法的平台",
            "欢迎他们的热情和创意",
            "不要限制可能性",
            "欣赏他们的正能量"
        ],
        "stress_response": "更加活跃健谈，可能逃避问题"
    },
    "ISTJ": {
        "best_environment": "金融、政府、医疗、传统企业、需要秩序和系统的环境",
        "worst_environment": "高度不确定、经常变化、缺乏结构的创新型创业公司",
        "team_role": "执行者、守护者、质量控制者",
        "leadership_style": "命令型领导，注重责任和传统",
        "collaboration_tips": [
            "尊重他们的专业知识和经验",
            "提供清晰的期望和截止日期",
            "不要指望他们灵活变通",
            "欣赏他们的可靠和稳定"
        ],
        "stress_response": "更加沉默和固执，需要秩序"
    },
    "ISFJ": {
        "best_environment": "医疗、护理、教育、行政、支持性的人际互动环境",
        "worst_environment": "高压销售、竞争激烈、缺乏认可的环境",
        "team_role": "支持者、照顾者、后勤保障",
        "leadership_style": "服务型领导，关注他人需求",
        "collaboration_tips": [
            "真诚感谢他们的付出",
            "给他们安静的工作环境",
            "不要强迫他们在公众场合表现",
            "保护他们不被利用"
        ],
        "stress_response": "过度工作来证明自己价值"
    },
    "ESTJ": {
        "best_environment": "企业管理、法律、执法、政府、传统行业管理岗位",
        "worst_environment": "缺乏结构、需要创意、情绪敏感的工作环境",
        "team_role": "管理者、组织者、质量控制者",
        "leadership_style": "命令型领导，注重效率和结果",
        "collaboration_tips": [
            "尊重他们的经验和能力",
            "直接坦诚地沟通",
            "不要质疑他们的权威",
            "欣赏他们的组织能力"
        ],
        "stress_response": "更加控制欲，可能对他人苛刻"
    },
    "ESFJ": {
        "best_environment": "客户服务、销售、医疗、教育、人际密集型服务行业",
        "worst_environment": "需要独立工作、缺乏认可、技术冷冰冰的环境",
        "team_role": "协调者、激励者、关系维护者",
        "leadership_style": "服务型领导，营造和谐氛围",
        "collaboration_tips": [
            "真诚感谢他们的帮助",
            "给他们社交互动的机会",
            "不要忽视他们的情感需求",
            "认可他们的努力和付出"
        ],
        "stress_response": "过度在意他人看法，可能迎合他人"
    },
    "ISTP": {
        "best_environment": "工程、技术、机械、军事、户外、动手操作的环境",
        "worst_environment": "需要频繁社交、过度规范、创意表演的环境",
        "team_role": "技术专家、问题解决者、实用主义者",
        "leadership_style": "放任型领导，尊重个人能力",
        "collaboration_tips": [
            "给他们动手操作的机会",
            "用事实和逻辑沟通",
            "不要过度干预他们的工作方式",
            "欣赏他们的技术能力"
        ],
        "stress_response": "退缩到内心，需要独处"
    },
    "ISFP": {
        "best_environment": "艺术、设计、手工艺、时尚、医疗保健支持",
        "worst_environment": "高压竞争、过度规范、缺乏美感的机械环境",
        "team_role": "艺术家、创作者、调解者",
        "leadership_style": "服务型领导，注重个人价值",
        "collaboration_tips": [
            "欣赏他们的审美和独特视角",
            "给他们创造性的空间",
            "不要给他们太大压力",
            "认可他们的艺术贡献"
        ],
        "stress_response": "逃避冲突，可能消极怠工"
    },
    "ESTP": {
        "best_environment": "销售、商务、体育、创业、危机管理、行动导向",
        "worst_environment": "长期规划、理论研究、缺乏刺激的环境",
        "team_role": "推动者、冒险家、危机处理者",
        "leadership_style": "命令型领导，注重即时结果",
        "collaboration_tips": [
            "给他们行动的机会",
            "直接简洁地沟通",
            "不要过度规划或理论化",
            "欣赏他们的活力和务实"
        ],
        "stress_response": "更加冲动，可能冒险"
    },
    "ESFP": {
        "best_environment": "娱乐、旅游、销售、表演艺术、公共关系",
        "worst_environment": "长期规划、重复性工作、缺乏变化的机械环境",
        "team_role": "激励者、氛围制造者、团队粘合剂",
        "leadership_style": "魅力型领导，营造愉快氛围",
        "collaboration_tips": [
            "给他们展示自己的舞台",
            "欢迎他们的热情和活力",
            "不要限制他们的社交",
            "认可他们的表现力"
        ],
        "stress_response": "更加活跃健谈，可能冲动"
    },
}

# 情侣匹配数据
ROMANTIC_COMPATIBILITY = {
    "INTJ": {
        "best_match": ["INFJ", "ENFJ", "INTP"],
        "challenging": ["ESFP", "ISFP", "ESTP"],
        "relationship_tips": [
            "学习表达情感，而不只是分析",
            "给伴侣足够的个人空间",
            "不要总是追求完美",
            "学会欣赏伴侣的感受"
        ],
        "communication": "直接但温柔，表达想法时加入情感元素"
    },
    "INTP": {
        "best_match": ["INFJ", "ENFJ", "INTJ"],
        "challenging": ["ESFJ", "ESTJ", "ISFP"],
        "relationship_tips": [
            "主动表达欣赏和爱意",
            "不要过度分析伴侣的意图",
            "多花时间陪伴而不只是思考",
            "学会处理冲突"
        ],
        "communication": "开放讨论，但注意伴侣需要情感支持"
    },
    "ENTJ": {
        "best_match": ["INTJ", "INFJ", "INFP"],
        "challenging": ["ISFP", "ESFP", "ISTP"],
        "relationship_tips": [
            "倾听而不只是指挥",
            "学会欣赏伴侣的付出",
            "不要总是争强好胜",
            "给伴侣表达意见的空间"
        ],
        "communication": "直接沟通，但注意语气不要太过命令式"
    },
    "ENTP": {
        "best_match": ["INFJ", "INTJ", "ENFJ"],
        "challenging": ["ISFJ", "ISTJ", "ESFJ"],
        "relationship_tips": [
            "专注而不要三心二意",
            "学会承诺并坚持",
            "不要只用智力吸引伴侣",
            "多关注伴侣的情感需求"
        ],
        "communication": "保持辩论的乐趣，但学会妥协"
    },
    "INFJ": {
        "best_match": ["INTJ", "ENFP", "INFP", "ENTJ"],
        "challenging": ["ESTP", "ESFP"],
        "relationship_tips": [
            "不要为了和谐而牺牲自己需求",
            "学会接受冲突",
            "表达自己的真实感受",
            "相信自己的直觉"
        ],
        "communication": "温柔但坦诚，表达深层感受"
    },
    "INFP": {
        "best_match": ["ENFJ", "INFJ", "INTJ"],
        "challenging": ["ESTJ", "ISTJ", "ESFJ"],
        "relationship_tips": [
            "坚持自己的价值观但保持灵活",
            "学会说“不”",
            "不要过度自我批评",
            "行动比完美主义更重要"
        ],
        "communication": "真诚表达，但也学会处理现实问题"
    },
    "ENFJ": {
        "best_match": ["INFP", "ISFP", "INTJ"],
        "challenging": ["ISTP", "ESTP", "INTP"],
        "relationship_tips": [
            "不要为他人牺牲自己",
            "学会独处而不感到内疚",
            "接受不是所有人都会喜欢你",
            "给自己空间满足自己的需求"
        ],
        "communication": "热情关怀，但学会倾听自己"
    },
    "ENFP": {
        "best_match": ["INFJ", "ENFJ", "INTJ"],
        "challenging": ["ISTJ", "ESTJ", "ISFJ"],
        "relationship_tips": [
            "学会承诺并坚持",
            "不要逃避困难的话题",
            "练习专注而不只是跳跃性思维",
            "给伴侣安全感"
        ],
        "communication": "保持热情和创意，但学会深度对话"
    },
    "ISTJ": {
        "best_match": ["ESFJ", "ESTJ", "ISFJ"],
        "challenging": ["ENFP", "ENTP", "INFP"],
        "relationship_tips": [
            "接受变化和新想法",
            "学会表达感情",
            "不要过于批评伴侣",
            "理解伴侣有不同的做事方式"
        ],
        "communication": "可靠稳定，但加入情感表达"
    },
    "ISFJ": {
        "best_match": ["ESFP", "ESTP", "ISFP"],
        "challenging": ["ENTP", "INTP", "ENTJ"],
        "relationship_tips": [
            "为自己站出来说话",
            "学会接受赞美",
            "不要把伴侣的问题都揽过来",
            "培养自己的兴趣和社交"
        ],
        "communication": "关怀体贴，但也表达自己的需求"
    },
    "ESTJ": {
        "best_match": ["ISTP", "ISFP", "ESTP"],
        "challenging": ["NF", "INFP", "ENFP"],
        "relationship_tips": [
            "倾听而不只是命令",
            "学会欣赏不同的做事方式",
            "注意伴侣的感受",
            "不要过于挑剔"
        ],
        "communication": "直接明了，但加入柔和语气"
    },
    "ESFJ": {
        "best_match": ["ISFP", "ISTP", "ESFP"],
        "challenging": ["INTP", "ENTP", "INTJ"],
        "relationship_tips": [
            "不要太在意他人的看法",
            "学会拒绝过分的要求",
            "给伴侣个人空间",
            "不要总是照顾他人而忽视自己"
        ],
        "communication": "温暖热情，但也表达自己的界限"
    },
    "ISTP": {
        "best_match": ["ESTJ", "ESFJ", "ESTP"],
        "challenging": ["NF", "ENFJ", "INFJ"],
        "relationship_tips": [
            "表达情感而不只是分析",
            "学会承诺和投入",
            "不要回避冲突",
            "多花时间陪伴伴侣"
        ],
        "communication": "实际直接，但也表达内心感受"
    },
    "ISFP": {
        "best_match": ["ESFJ", "ENFJ", "ESFP"],
        "challenging": ["ENTJ", "INTJ", "ENTP"],
        "relationship_tips": [
            "勇敢表达自己的立场",
            "学会坚持而不只是退让",
            "不要过度自我怀疑",
            "培养自信"
        ],
        "communication": "温和但真诚，表达独特视角"
    },
    "ESTP": {
        "best_match": ["ISTJ", "ISFJ", "ESTJ"],
        "challenging": ["INFJ", "INFP", "INTJ"],
        "relationship_tips": [
            "学会考虑后果",
            "练习倾听而不是只是说话",
            "不要只用刺激来维持关系",
            "培养深度对话的能力"
        ],
        "communication": "活泼直接，但也学会深度交流"
    },
    "ESFP": {
        "best_match": ["ISFJ", "ISTJ", "ESTJ"],
        "challenging": ["INTJ", "INFJ", "INTP"],
        "relationship_tips": [
            "学会承诺并坚持",
            "不要太在意他人目光",
            "发展深度而非只是广度",
            "练习在安静中享受相处"
        ],
        "communication": "活泼热情，但也学会倾听"
    },
}

def get_workplace_info(type_code: str) -> dict:
    """获取类型的职场信息"""
    return WORKPLACE_DATA.get(type_code, {})

def get_romantic_info(type_code: str) -> dict:
    """获取类型的情侣匹配信息"""
    return ROMANTIC_COMPATIBILITY.get(type_code, {})

def get_relationship_data(type_code: str) -> dict:
    """获取完整的关系数据"""
    return {
        "workplace": get_workplace_info(type_code),
        "romantic": get_romantic_info(type_code)
    }
