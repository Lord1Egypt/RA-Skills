#!/usr/bin/env python3
"""
MBTI Guru - 认知功能数据
包含16种MBTI类型的8种认知功能栈
"""

COGNITIVE_FUNCTIONS = {
    # ============================================
    # NT 理性者 (Intuitive Thinking)
    # ============================================
    "INTJ": {
        "name": "建筑师 / Architect",
        "functions": {
            "dominant": {"name": "内向直觉 Ni", "description": "洞察未来可能性，善于看到事物发展的规律和趋势", "strength": "战略思维、预见性"},
            "auxiliary": {"name": "外向思考 Te", "description": "高效组织外部世界，制定逻辑性的计划和系统", "strength": "执行能力、系统构建"},
            "tertiary": {"name": "内向情感 Fi", "description": "建立个人价值观体系，关注内心情感体验", "strength": "价值判断、道德指南"},
            "inferior": {"name": "外向感觉 Se", "description": "对当下环境和具体细节的感知", "strength": "即时反应、现实感知"},
        },
        "shadow": {
            "critic": "外向直觉 Ne", "trickster": "内向思考 Ti",
            "demon": "外向情感 Fe", "devil": "内向感觉 Si"
        },
        "growth": [
            "发展Te的同时，不要忽视Fi——你的价值观同样重要",
            "学会放松，适时体验当下而非总是规划未来",
            "接受不确定性，明白不是所有事都需要逻辑解释",
            "多倾听他人的感受，而不只是逻辑分析"
        ]
    },
    "INTP": {
        "name": "逻辑学家 / Logician",
        "functions": {
            "dominant": {"name": "内向思考 Ti", "description": "深入分析内在逻辑，追求精确的理解和原理", "strength": "分析能力、逻辑严谨"},
            "auxiliary": {"name": "外向直觉 Ne", "description": "探索各种可能性，连接不同的想法和概念", "strength": "创意联想、可能性思维"},
            "tertiary": {"name": "内向感觉 Si", "description": "回顾过去的经验和细节，建立内部数据库", "strength": "经验积累、细节记忆"},
            "inferior": {"name": "外向情感 Fe", "description": "理解和适应他人的情感需求", "strength": "社交技巧、情感洞察"},
        },
        "shadow": {
            "critic": "内向直觉 Ni", "trickster": "外向思考 Te",
            "demon": "内向感觉 Si", "devil": "外向情感 Fe"
        },
        "growth": [
            "发展Fe功能，主动表达情感而非总是藏在心里",
            "学会在适当时机做决定，不过度分析",
            "珍惜人际关系，不只是把它们当作逻辑练习",
            "接受不完美，理解灰色地带的存在"
        ]
    },
    "ENTJ": {
        "name": "指挥官 / Commander",
        "functions": {
            "dominant": {"name": "外向思考 Te", "description": "高效组织外部资源，推动目标实现", "strength": "领导能力、决策效率"},
            "auxiliary": {"name": "内向直觉 Ni", "description": "形成长远的战略愿景，把握发展方向", "strength": "战略规划、直觉判断"},
            "tertiary": {"name": "外向感觉 Se", "description": "关注当下的具体现实和环境", "strength": "即时行动、细节把握"},
            "inferior": {"name": "内向情感 Fi", "description": "建立和维护个人价值观和内心感受", "strength": "自我认知、价值坚守"},
        },
        "shadow": {
            "critic": "内向思考 Ti", "trickster": "外向直觉 Ne",
            "demon": "外向感觉 Se", "devil": "内向直觉 Ni"
        },
        "growth": [
            "发展Fi，学会理解自己和他人的情感需求",
            "练习耐心倾听，不要总是急于给出解决方案",
            "接受自己也有软弱的时候，不需要一直强势",
            "注意他人的感受，而不只是效率和结果"
        ]
    },
    "ENTP": {
        "name": "辩论家 / Debater",
        "functions": {
            "dominant": {"name": "外向直觉 Ne", "description": "探索可能性，连接不同的想法和创新概念", "strength": "创意能力、可能性探索"},
            "auxiliary": {"name": "内向思考 Ti", "description": "分析内在逻辑，评估想法的合理性", "strength": "逻辑分析、客观评估"},
            "tertiary": {"name": "外向情感 Fe", "description": "关注他人的情感和需求", "strength": "人际洞察、情感共鸣"},
            "inferior": {"name": "内向感觉 Si", "description": "重视过去的经验和既有程序", "strength": "传统维护、细节执行"},
        },
        "shadow": {
            "critic": "外向思考 Te", "trickster": "内向直觉 Ni",
            "demon": "内向感觉 Si", "devil": "外向情感 Fe"
        },
        "growth": [
            "发展Si，学会坚持完成已经开始的项目",
            "练习专注，而不只是对新想法感到兴奋",
            "学习承担责任，而不只是逃避困难的决定",
            "在争论中多考虑他人的感受"
        ]
    },
    
    # ============================================
    # NF 理想主义者 (Intuitive Feeling)
    # ============================================
    "INFJ": {
        "name": "提倡者 / Advocate",
        "functions": {
            "dominant": {"name": "内向直觉 Ni", "description": "洞察本质和未来可能性，看到更深层的模式", "strength": "洞察力、预见性"},
            "auxiliary": {"name": "外向情感 Fe", "description": "理解和影响他人的情感需求", "strength": "共情能力、人际影响"},
            "tertiary": {"name": "内向思考 Ti", "description": "分析内在逻辑，确保决定的一致性", "strength": "批判思维、逻辑验证"},
            "inferior": {"name": "外向感觉 Se", "description": "感知当下的具体环境和细节", "strength": "现实适应、即时反应"},
        },
        "shadow": {
            "critic": "外向直觉 Ne", "trickster": "内向情感 Fi",
            "demon": "外向感觉 Se", "devil": "内向思考 Ti"
        },
        "growth": [
            "不要总是为了满足他人而牺牲自己",
            "学会接受冲突，不必害怕伤害他人感情",
            "发展Ti，勇于进行困难的对话",
            "多关注当下，享受此时此刻"
        ]
    },
    "INFP": {
        "name": "调停者 / Mediator",
        "functions": {
            "dominant": {"name": "内向情感 Fi", "description": "建立在个人价值观基础上的内心体验和判断", "strength": "价值观判断、情感深度"},
            "auxiliary": {"name": "外向直觉 Ne", "description": "探索外部世界的可能性和新的想法", "strength": "创意探索、可能性思维"},
            "tertiary": {"name": "内向感觉 Si", "description": "联系过去的经验和既有的做事方式", "strength": "传统维护、经验积累"},
            "inferior": {"name": "外向思考 Te", "description": "高效组织外部世界完成任务", "strength": "执行能力、效率提升"},
        },
        "shadow": {
            "critic": "内向直觉 Ni", "trickster": "外向情感 Fe",
            "demon": "内向感觉 Si", "devil": "外向思考 Te"
        },
        "growth": [
            "发展Te，不要让完美主义阻止你行动",
            "学会说“不”，保护自己的时间和精力",
            "接受现实有时与理想不同",
            "在坚持价值观和灵活变通之间找到平衡"
        ]
    },
    "ENFJ": {
        "name": "主人公 / Protagonist",
        "functions": {
            "dominant": {"name": "外向情感 Fe", "description": "真诚地关心他人，致力于共同成长", "strength": "激励能力、领导魅力"},
            "auxiliary": {"name": "内向直觉 Ni", "description": "看到更深层的意义和未来的可能性", "strength": "战略眼光、洞察本质"},
            "tertiary": {"name": "外向感觉 Se", "description": "享受当下的体验和周围的世界", "strength": "即时反应、现实感知"},
            "inferior": {"name": "内向思考 Ti", "description": "分析内在逻辑确保决定合理", "strength": "批判分析、逻辑思考"},
        },
        "shadow": {
            "critic": "内向情感 Fi", "trickster": "外向直觉 Ne",
            "demon": "外向感觉 Se", "devil": "内向直觉 Ni"
        },
        "growth": [
            "发展Ti，允许自己做出不受欢迎的决定",
            "不要过度在意他人的看法",
            "学会接受自己无法改变所有事",
            "给自己留些独处的时间充电"
        ]
    },
    "ENFP": {
        "name": "竞选者 / Campaigner",
        "functions": {
            "dominant": {"name": "外向直觉 Ne", "description": "充满热情地探索各种可能性和创新想法", "strength": "热情传染、创意激发"},
            "auxiliary": {"name": "内向情感 Fi", "description": "基于个人价值观做真实的决定", "strength": "真实自我、价值驱动"},
            "tertiary": {"name": "内向感觉 Si", "description": "联系过去的经验和熟悉的方式", "strength": "传统维护、经验运用"},
            "inferior": {"name": "外向思考 Te", "description": "高效组织和完成外部世界的任务", "strength": "执行能力、组织管理"},
        },
        "shadow": {
            "critic": "外向情感 Fe", "trickster": "内向直觉 Ni",
            "demon": "内向感觉 Si", "devil": "外向思考 Te"
        },
        "growth": [
            "发展Te，学会坚持完成而不是半途而废",
            "练习专注，不被太多可能性分散注意力",
            "学会面对困难的决定，而不只是拖延",
            "在热情和实际可行性之间找到平衡"
        ]
    },
    
    # ============================================
    # SJ 守护者 (Sensing Judging)
    # ============================================
    "ISTJ": {
        "name": "物流师 / Logistician",
        "functions": {
            "dominant": {"name": "内向感觉 Si", "description": "关注细节和过去的经验， 建立可靠的系统", "strength": "可靠性、细节把控"},
            "auxiliary": {"name": "外向思考 Te", "description": "高效组织外部世界，实现目标", "strength": "执行能力、组织效率"},
            "tertiary": {"name": "内向情感 Fi", "description": "发展个人价值观和内在标准", "strength": "道德指南、价值判断"},
            "inferior": {"name": "外向直觉 Ne", "description": "探索新的可能性和创新的想法", "strength": "可能性探索、创新思维"},
        },
        "shadow": {
            "critic": "外向感觉 Se", "trickster": "内向思考 Ti",
            "demon": "内向感觉 Si", "devil": "外向直觉 Ne"
        },
        "growth": [
            "发展Ne，适度接受变化和新想法",
            "不要过于僵化，学会灵活应变",
            "理解他人的做事方式可能与你不同",
            "允许自己尝试新的方法而不只是依赖经验"
        ]
    },
    "ISFJ": {
        "name": "守护者 / Defender",
        "functions": {
            "dominant": {"name": "内向感觉 Si", "description": "珍视传统和过去的经验，细心照顾他人的需求", "strength": "忠诚守护、细心照顾"},
            "auxiliary": {"name": "外向情感 Fe", "description": "真诚地帮助和服务他人", "strength": "服务精神、人文关怀"},
            "tertiary": {"name": "内向直觉 Ni", "description": "看到事物发展的趋势和可能性", "strength": "洞察趋势、预见发展"},
            "inferior": {"name": "外向思考 Te", "description": "完成任务和达成目标的能力", "strength": "执行能力、效率意识"},
        },
        "shadow": {
            "critic": "内向情感 Fi", "trickster": "外向感觉 Se",
            "demon": "内向直觉 Ni", "devil": "外向思考 Te"
        },
        "growth": [
            "发展Te，为自己的需求站出来说话",
            "学会接受赞美，而不只是默默付出",
            "不要把别人的问题都扛在自己身上",
            "适度放手，不必事必躬亲"
        ]
    },
    "ESTJ": {
        "name": "总经理 / Executive",
        "functions": {
            "dominant": {"name": "外向思考 Te", "description": "高效组织和管理外部事务", "strength": "管理能力、执行效率"},
            "auxiliary": {"name": "内向感觉 Si", "description": "利用过去的经验和传统确保稳定", "strength": "传统维护、系统建立"},
            "tertiary": {"name": "内向直觉 Ni", "description": "看到未来发展的可能性", "strength": "战略眼光、趋势把握"},
            "inferior": {"name": "外向情感 Fe", "description": "理解和关心他人的情感需求", "strength": "情感洞察、人文关怀"},
        },
        "shadow": {
            "critic": "外向感觉 Se", "trickster": "内向思考 Ti",
            "demon": "内向直觉 Ni", "devil": "外向情感 Fe"
        },
        "growth": [
            "发展Fe，多关注员工的情感而非只是业绩",
            "学会欣赏不同的观点和工作方式",
            "接受不是所有事都能用逻辑解决",
            "练习耐心，不只是追求效率"
        ]
    },
    "ESFJ": {
        "name": "执政官 / Consul",
        "functions": {
            "dominant": {"name": "外向情感 Fe", "description": "热情地照顾他人，营造和谐的人际关系", "strength": "社交能力、人际和谐"},
            "auxiliary": {"name": "内向感觉 Si", "description": "关注细节和既有的经验传统", "strength": "细心周到、传统维护"},
            "tertiary": {"name": "内向直觉 Ni", "description": "洞察未来的可能性和趋势", "strength": "战略思维、预见能力"},
            "inferior": {"name": "外向思考 Te", "description": "完成任务和组织外部事务", "strength": "执行能力、组织管理"},
        },
        "shadow": {
            "critic": "外向感觉 Se", "trickster": "内向情感 Fi",
            "demon": "内向直觉 Ni", "devil": "外向思考 Te"
        },
        "growth": [
            "发展Te，为自己的需求争取而不只是付出",
            "学会接受批评，不必追求每个人的认可",
            "不要过度在意社交礼仪而忽视自己的感受",
            "允许自己说“不”，不必讨好所有人"
        ]
    },
    
    # ============================================
    # SP 探险家 (Sensing Perceiving)
    # ============================================
    "ISTP": {
        "name": "鉴赏家 / Virtuoso",
        "functions": {
            "dominant": {"name": "内向思考 Ti", "description": "分析内在逻辑原理，追求精确的技术理解", "strength": "逻辑分析、技术专长"},
            "auxiliary": {"name": "外向感觉 Se", "description": "敏锐感知当下环境，擅长操作工具", "strength": "动手能力、即时反应"},
            "tertiary": {"name": "内向直觉 Ni", "description": "看到事物发展的长远趋势", "strength": "战略洞察、趋势把握"},
            "inferior": {"name": "外向情感 Fe", "description": "理解和适应他人的情感需求", "strength": "人际适应、情感洞察"},
        },
        "shadow": {
            "critic": "内向感觉 Si", "trickster": "外向思考 Te",
            "demon": "外向感觉 Se", "devil": "内向直觉 Ni"
        },
        "growth": [
            "发展Fe，表达自己的情感而不是藏起来",
            "学会承诺和坚持，而不只是保持灵活",
            "多关注他人的需求而不只是技术问题",
            "练习长期规划，而不只是即时反应"
        ]
    },
    "ISFP": {
        "name": "探险家 / Adventurer",
        "functions": {
            "dominant": {"name": "内向情感 Fi", "description": "基于个人价值观做出真实的决定", "strength": "艺术感受、价值坚守"},
            "auxiliary": {"name": "外向感觉 Se", "description": "享受当下的体验，灵活适应环境", "strength": "审美能力、灵活适应"},
            "tertiary": {"name": "内向直觉 Ni", "description": "洞察未来的可能性", "strength": "艺术洞察、直觉把握"},
            "inferior": {"name": "外向思考 Te", "description": "高效组织和完成任务", "strength": "执行能力、效率提升"},
        },
        "shadow": {
            "critic": "内向感觉 Si", "trickster": "外向情感 Fe",
            "demon": "内向直觉 Ni", "devil": "外向思考 Te"
        },
        "growth": [
            "发展Te，勇敢表达自己的需求和立场",
            "学会坚持完成任务而不只是半途而废",
            "不要过度自我批评，接受自己的不完美",
            "练习在团队中发挥领导作用"
        ]
    },
    "ESTP": {
        "name": "企业家 / Entrepreneur",
        "functions": {
            "dominant": {"name": "外向感觉 Se", "description": "敏锐感知当下环境，果断行动", "strength": "行动力、危机处理"},
            "auxiliary": {"name": "外向思考 Te", "description": "高效分析和解决问题", "strength": "分析能力、决策效率"},
            "tertiary": {"name": "内向直觉 Ni", "description": "形成对未来趋势的洞察", "strength": "趋势把握、战略眼光"},
            "inferior": {"name": "内向情感 Fi", "description": "建立和维护个人价值观", "strength": "价值坚守、道德指南"},
        },
        "shadow": {
            "critic": "外向直觉 Ne", "trickster": "内向感觉 Si",
            "demon": "外向思考 Te", "devil": "内向直觉 Ni"
        },
        "growth": [
            "发展Fi，关注自己的内心感受而非只看外在成就",
            "练习停下来思考，而不只是冲动行动",
            "学会尊重他人的感受而不只是追求刺激",
            "培养长期规划的能力"
        ]
    },
    "ESFP": {
        "name": "表演者 / Entertainer",
        "functions": {
            "dominant": {"name": "外向感觉 Se", "description": "享受当下的体验，充满活力和热情", "strength": "表现力、热情传染"},
            "auxiliary": {"name": "内向情感 Fi", "description": "基于个人价值观做真实的决定", "strength": "艺术表达、价值驱动"},
            "tertiary": {"name": "内向直觉 Ni", "description": "洞察未来的可能性", "strength": "趋势洞察、预见能力"},
            "inferior": {"name": "外向思考 Te", "description": "高效组织和分析外部世界", "strength": "组织能力、逻辑分析"},
        },
        "shadow": {
            "critic": "外向情感 Fe", "trickster": "内向感觉 Si",
            "demon": "内向直觉 Ni", "devil": "外向思考 Te"
        },
        "growth": [
            "发展Te，学会计划和组织而不只是活在当下",
            "接受批评，把它当作成长的机会",
            "不要过度追求认可，做真实的自己",
            "练习在决定前进行深思熟虑"
        ]
    },
}

def get_cognitive_functions(type_code: str) -> dict:
    """获取类型的认知功能数据"""
    return COGNITIVE_FUNCTIONS.get(type_code, {})

def get_all_functions() -> dict:
    """获取所有类型的认知功能数据"""
    return COGNITIVE_FUNCTIONS
