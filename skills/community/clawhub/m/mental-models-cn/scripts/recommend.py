#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
思维模型推荐引擎 v2.1
根据用户输入的问题自动推荐最佳思维模型组合
支持 73 个核心思维模型

使用方法:
    python recommend.py "我要分析一个行业是否值得进入"
    python recommend.py "如何评估这个投资机会"
    python recommend.py "分析 Tesla 的竞争优势"
    python recommend.py "如何提升学习效率" --json
"""

import json
import sys
import re
import argparse
from typing import List, Dict, Tuple, Optional

# ============================================================================
# 模型知识库 v2.1 - 73 个核心思维模型
# ============================================================================
MODELS_DB = {
    # ========== 基础分析（6 个）==========
    "PESTEL": {
        "name": "PESTEL 分析",
        "file": "pestel-analysis.md",
        "series": "基础分析",
        "keywords": ["宏观", "环境", "政策", "经济", "社会", "技术", "法律", "政治"],
        "scenarios": ["宏观环境分析", "市场进入", "政策影响", "行业研究"],
        "description": "宏观环境扫描工具"
    },
    "SWOT": {
        "name": "SWOT 分析",
        "file": "swot-analysis.md",
        "series": "基础分析",
        "keywords": ["优势", "劣势", "机会", "威胁", "内外部"],
        "scenarios": ["综合分析", "战略制定", "竞争分析", "自我评估"],
        "description": "内外部综合分析工具"
    },
    "Porter5": {
        "name": "波特五力",
        "file": "porters-five-forces.md",
        "series": "基础分析",
        "keywords": ["行业", "竞争", "供应商", "购买者", "进入壁垒", "替代品"],
        "scenarios": ["行业分析", "竞争策略", "市场进入", "投资评估"],
        "description": "行业竞争分析框架"
    },
    "MECE": {
        "name": "MECE 原则",
        "file": "mece-principle.md",
        "series": "基础分析",
        "keywords": ["结构化", "分类", "不重不漏", "拆解", "逻辑"],
        "scenarios": ["问题分析", "结构化思考", "团队协作", "报告撰写"],
        "description": "结构化思考原则"
    },
    "Systems": {
        "name": "系统思维",
        "file": "systems-thinking.md",
        "series": "基础分析",
        "keywords": ["系统", "整体", "相互作用", "反馈", "循环", "关联"],
        "scenarios": ["复杂问题", "组织分析", "生态分析", "动态分析"],
        "description": "整体性分析框架"
    },
    "FirstPrinciples": {
        "name": "第一性原理",
        "file": "first-principles.md",
        "series": "基础分析",
        "keywords": ["本质", "拆解", "基本原理", "回归", "物理", "创新"],
        "scenarios": ["创新", "本质分析", "产品定位", "问题解决"],
        "description": "本质拆解思维"
    },
    
    # ========== 决策思维（8 个）==========
    "SecondOrder": {
        "name": "二阶效应",
        "file": "second-order-effects.md",
        "series": "决策思维",
        "keywords": ["连锁", "后果", "长期", "推演", "间接"],
        "scenarios": ["风险评估", "决策分析", "政策影响", "战略规划"],
        "description": "连锁反应推演"
    },
    "Occam": {
        "name": "奥卡姆剃刀",
        "file": "occams-razor.md",
        "series": "决策思维",
        "keywords": ["简化", "简单", "假设", "精简"],
        "scenarios": ["问题简化", "决策优化", "理论选择"],
        "description": "简化原则"
    },
    "Hanlon": {
        "name": "汉隆剃刀",
        "file": "hans-razor.md",
        "series": "决策思维",
        "keywords": ["归因", "恶意", "愚蠢", "误解"],
        "scenarios": ["人际分析", "组织行为", "冲突理解"],
        "description": "归因简化原则"
    },
    "Inversion": {
        "name": "逆向思维",
        "file": "inversion.md",
        "series": "决策思维",
        "keywords": ["反向", "失败", "避免", "倒推"],
        "scenarios": ["风险评估", "竞争策略", "创新", "问题预防"],
        "description": "反向思考方法"
    },
    "GameTheory": {
        "name": "博弈论",
        "file": "game-theory.md",
        "series": "决策思维",
        "keywords": ["策略", "互动", "纳什均衡", "定价", "竞争", "合作"],
        "scenarios": ["竞争策略", "定价策略", "谈判", "合作决策"],
        "description": "策略互动分析"
    },
    "Comparative": {
        "name": "比较优势",
        "file": "comparative-advantage.md",
        "series": "决策思维",
        "keywords": ["分工", "专业化", "贸易", "优势"],
        "scenarios": ["职业选择", "团队合作", "国际贸易"],
        "description": "专业化分工原理"
    },
    "Opportunity": {
        "name": "机会成本",
        "file": "opportunity-cost.md",
        "series": "决策思维",
        "keywords": ["选择", "代价", "放弃", "成本"],
        "scenarios": ["投资决策", "时间管理", "资源分配"],
        "description": "选择的真实代价"
    },
    "Lean": {
        "name": "精益创业",
        "file": "lean-startup.md",
        "series": "决策思维",
        "keywords": ["MVP", "验证", "迭代", "快速", "反馈"],
        "scenarios": ["创业", "产品开发", "创新项目"],
        "description": "快速验证方法"
    },
    
    # ========== 趋势分析（5 个）==========
    "Cycle": {
        "name": "周期理论",
        "file": "cycle-theory.md",
        "series": "趋势分析",
        "keywords": ["周期", "经济", "波动", "循环", "时机"],
        "scenarios": ["投资时机", "市场判断", "经济分析"],
        "description": "经济周期分析"
    },
    "PowerLaw": {
        "name": "幂律分布",
        "file": "power-law.md",
        "series": "趋势分析",
        "keywords": ["80/20", "二八", "分布", "头部", "长尾"],
        "scenarios": ["资源分配", "投资选择", "市场分析"],
        "description": "80/20 法则"
    },
    "Antifragile": {
        "name": "反脆弱",
        "file": "antifragile.md",
        "series": "趋势分析",
        "keywords": ["风险", "波动", "收益", "不确定性", "成长"],
        "scenarios": ["风险管理", "投资策略", "职业规划"],
        "description": "从波动中受益"
    },
    "CriticalMass": {
        "name": "临界质量",
        "file": "critical-mass.md",
        "series": "趋势分析",
        "keywords": ["量变", "质变", "引爆点", "阈值"],
        "scenarios": ["市场启动", "产品发布", "变革管理"],
        "description": "量变到质变"
    },
    "LongTerm": {
        "name": "长期主义",
        "file": "long-term-thinking.md",
        "series": "趋势分析",
        "keywords": ["复利", "长期", "耐心", "持续"],
        "scenarios": ["投资决策", "职业发展", "能力建设"],
        "description": "复利思维"
    },
    
    # ========== 概率思维（3 个）==========
    "Probabilistic": {
        "name": "概率思维",
        "file": "probabilistic-thinking.md",
        "series": "概率思维",
        "keywords": ["概率", "不确定性", "期望值", "风险"],
        "scenarios": ["投资决策", "风险评估", "战略规划"],
        "description": "不确定性决策"
    },
    "Bayes": {
        "name": "贝叶斯定理",
        "file": "bayes-theorem.md",
        "series": "概率思维",
        "keywords": ["信念", "更新", "证据", "概率"],
        "scenarios": ["医学诊断", "投资判断", "科学推理"],
        "description": "信念更新方法"
    },
    "Survivorship": {
        "name": "幸存者偏差",
        "file": "survivorship-bias.md",
        "series": "概率思维",
        "keywords": ["沉默", "证据", "选择", "偏差"],
        "scenarios": ["投资分析", "成功学", "历史研究"],
        "description": "沉默的证据"
    },
    
    # ========== 商业战略（3 个）==========
    "Network": {
        "name": "网络效应",
        "file": "network-effects.md",
        "series": "商业战略",
        "keywords": ["平台", "用户", "价值", "规模", "垄断"],
        "scenarios": ["平台战略", "产品定价", "市场竞争"],
        "description": "平台经济原理"
    },
    "BlueOcean": {
        "name": "蓝海战略",
        "file": "blue-ocean.md",
        "series": "商业战略",
        "keywords": ["无竞争", "创新", "价值", "差异化"],
        "scenarios": ["创业方向", "产品定位", "市场策略"],
        "description": "无竞争市场策略"
    },
    
    # ========== 心理实验（6 个）==========
    "StanfordPrison": {
        "name": "斯坦福监狱实验",
        "file": "psychology-experiments.md",
        "series": "心理实验",
        "keywords": ["环境", "角色", "权力", "服从", "行为"],
        "scenarios": ["组织管理", "权力分析", "制度设计"],
        "description": "环境影响行为"
    },
    "Milgram": {
        "name": "米尔格拉姆服从实验",
        "file": "psychology-experiments.md",
        "series": "心理实验",
        "keywords": ["权威", "服从", "道德", "责任"],
        "scenarios": ["组织行为", "道德决策", "权威分析"],
        "description": "权威服从心理"
    },
    "Asch": {
        "name": "阿希从众实验",
        "file": "psychology-experiments.md",
        "series": "心理实验",
        "keywords": ["从众", "群体", "压力", "独立"],
        "scenarios": ["群体决策", "会议管理", "独立思考"],
        "description": "群体压力影响"
    },
    "CognitiveDissonance": {
        "name": "认知失调实验",
        "file": "psychology-experiments.md",
        "series": "心理实验",
        "keywords": ["信念", "调整", "合理化", "冲突"],
        "scenarios": ["决策后行为", "说服策略", "自我反思"],
        "description": "信念调整机制"
    },
    "Marshmallow": {
        "name": "棉花糖实验",
        "file": "psychology-experiments.md",
        "series": "心理实验",
        "keywords": ["延迟", "满足", "自控", "耐心"],
        "scenarios": ["教育", "习惯养成", "自我管理"],
        "description": "延迟满足能力"
    },
    "InvisibleGorilla": {
        "name": "看不见的大猩猩",
        "file": "psychology-experiments.md",
        "series": "心理实验",
        "keywords": ["注意力", "盲区", "忽视", "专注"],
        "scenarios": ["安全设计", "决策验证", "自我觉察"],
        "description": "注意力盲区"
    },
    
    # ========== 群体心理（8 个）==========
    "GroupPolarization": {
        "name": "群体极化",
        "file": "group-psychology.md",
        "series": "群体心理",
        "keywords": ["极端", "讨论", "决策", "放大"],
        "scenarios": ["董事会决策", "社交媒体", "陪审团"],
        "description": "观点趋向极端"
    },
    "InformationCascade": {
        "name": "信息级联",
        "file": "group-psychology.md",
        "series": "群体心理",
        "keywords": ["跟随", "模仿", "传播", "连锁"],
        "scenarios": ["市场趋势", "投资决策", "消费行为"],
        "description": "跟随他人行为"
    },
    "Herding": {
        "name": "羊群效应",
        "file": "group-psychology.md",
        "series": "群体心理",
        "keywords": ["从众", "跟风", "模仿", "群体"],
        "scenarios": ["股市", "房市", "加密货币", "流行趋势"],
        "description": "群体模仿行为"
    },
    "SocialIdentity": {
        "name": "社会认同理论",
        "file": "group-psychology.md",
        "series": "群体心理",
        "keywords": ["归属", "群体", "身份", "认同"],
        "scenarios": ["品牌建设", "组织文化", "营销"],
        "description": "群体归属心理"
    },
    "WisdomCrowds": {
        "name": "集体智慧",
        "file": "group-psychology.md",
        "series": "群体心理",
        "keywords": ["群体", "判断", "预测", "平均"],
        "scenarios": ["预测市场", "开源软件", "众包"],
        "description": "群体判断优势"
    },
    "SpiralSilence": {
        "name": "沉默的螺旋",
        "file": "group-psychology.md",
        "series": "群体心理",
        "keywords": ["沉默", "舆论", "少数", "孤立"],
        "scenarios": ["舆论分析", "会议决策", "组织文化"],
        "description": "少数派沉默现象"
    },
    "BrokenWindows": {
        "name": "破窗理论",
        "file": "group-psychology.md",
        "series": "群体心理",
        "keywords": ["失序", "小问题", "恶化", "规范"],
        "scenarios": ["社区管理", "企业文化", "质量管理"],
        "description": "小问题引发大问题"
    },
    "Bystander": {
        "name": "旁观者效应",
        "file": "group-psychology.md",
        "series": "群体心理",
        "keywords": ["责任", "分散", "帮助", "干预"],
        "scenarios": ["紧急响应", "举报制度", "社会干预"],
        "description": "责任分散效应"
    },
    
    # ========== 经济心理（10 个）==========
    "Scarcity": {
        "name": "稀缺心态",
        "file": "depression-psychology.md",
        "series": "经济心理",
        "keywords": ["稀缺", "短视", "认知", "带宽"],
        "scenarios": ["萧条期决策", "资源管理", "时间管理"],
        "description": "资源稀缺影响认知"
    },
    "LossAversion": {
        "name": "损失厌恶",
        "file": "depression-psychology.md",
        "series": "经济心理",
        "keywords": ["损失", "痛苦", "风险", "保守"],
        "scenarios": ["投资决策", "风险管理", "谈判"],
        "description": "损失痛苦大于收益快乐"
    },
    "Anchoring": {
        "name": "锚定效应",
        "file": "depression-psychology.md",
        "series": "经济心理",
        "keywords": ["锚点", "首个", "依赖", "参考"],
        "scenarios": ["价格谈判", "估算", "目标设定"],
        "description": "过度依赖首个信息"
    },
    "Availability": {
        "name": "可得性启发",
        "file": "depression-psychology.md",
        "series": "经济心理",
        "keywords": ["易想起", "高估", "媒体", "概率"],
        "scenarios": ["风险评估", "投资判断", "媒体影响"],
        "description": "高估易想起事件"
    },
    "SocialComparison": {
        "name": "社会比较",
        "file": "depression-psychology.md",
        "series": "经济心理",
        "keywords": ["比较", "他人", "评估", "攀比"],
        "scenarios": ["消费决策", "职业选择", "社交媒体"],
        "description": "通过他人评估自己"
    },
    "IllusionControl": {
        "name": "控制错觉",
        "file": "depression-psychology.md",
        "series": "经济心理",
        "keywords": ["控制", "高估", "自信", "预测"],
        "scenarios": ["投资决策", "创业", "风险管理"],
        "description": "高估自己控制能力"
    },
    "HerdingBehavior": {
        "name": "从众行为",
        "file": "depression-psychology.md",
        "series": "经济心理",
        "keywords": ["跟随", "大众", "放弃", "判断"],
        "scenarios": ["股市", "银行挤兑", "恐慌"],
        "description": "跟随大众放弃判断"
    },
    "MentalAccounting": {
        "name": "心理账户",
        "file": "depression-psychology.md",
        "series": "经济心理",
        "keywords": ["账户", "区别", "资金", "分类"],
        "scenarios": ["消费决策", "投资", "理财"],
        "description": "区别对待不同资金"
    },
    "StatusQuo": {
        "name": "现状偏见",
        "file": "depression-psychology.md",
        "series": "经济心理",
        "keywords": ["现状", "维持", "改变", "惯性"],
        "scenarios": ["职业选择", "投资调整", "变革管理"],
        "description": "倾向维持现状"
    },
    "Pessimism": {
        "name": "悲观偏差",
        "file": "depression-psychology.md",
        "series": "经济心理",
        "keywords": ["悲观", "萧条", "过度", "负面"],
        "scenarios": ["经济判断", "投资决策", "风险评估"],
        "description": "萧条期过度悲观"
    },
    
    # ========== 认知科学（8 个）==========
    "DualProcess": {
        "name": "双系统思维",
        "file": "cognitive-science.md",
        "series": "认知科学",
        "keywords": ["快思考", "慢思考", "直觉", "理性", "系统"],
        "scenarios": ["重要决策", "日常习惯", "避免错误"],
        "description": "系统 1 与系统 2"
    },
    "Metacognition": {
        "name": "元认知",
        "file": "cognitive-science.md",
        "series": "认知科学",
        "keywords": ["思考", "监控", "反思", "自我"],
        "scenarios": ["学习", "决策", "问题解决"],
        "description": "思考自己的思考"
    },
    "Attention": {
        "name": "注意力管理",
        "file": "cognitive-science.md",
        "series": "认知科学",
        "keywords": ["注意力", "专注", "干扰", "资源"],
        "scenarios": ["工作效率", "学习", "时间管理"],
        "description": "注意力是稀缺资源"
    },
    "ConfirmationBias": {
        "name": "确认偏误",
        "file": "cognitive-science.md",
        "series": "认知科学",
        "keywords": ["确认", "支持", "证据", "偏见"],
        "scenarios": ["决策", "研究", "投资"],
        "description": "寻找支持自己观点的证据"
    },
    "Framing": {
        "name": "框架效应",
        "file": "cognitive-science.md",
        "series": "认知科学",
        "keywords": ["框架", "表述", "决策", "影响"],
        "scenarios": ["沟通", "谈判", "决策"],
        "description": "表述方式影响决策"
    },
    "CognitiveLoad": {
        "name": "认知负荷",
        "file": "cognitive-science.md",
        "series": "认知科学",
        "keywords": ["负荷", "记忆", "工作", "限制"],
        "scenarios": ["教学设计", "界面设计", "文档写作"],
        "description": "工作记忆有限"
    },
    "Hindsight": {
        "name": "后见之明",
        "file": "cognitive-science.md",
        "series": "认知科学",
        "keywords": ["事后", "早知道", "预测", "复盘"],
        "scenarios": ["复盘", "学习", "预测"],
        "description": "\"我早就知道\"偏误"
    },
    
    # ========== 学习成长（8 个）==========
    "DeliberatePractice": {
        "name": "刻意练习",
        "file": "learning-growth.md",
        "series": "学习成长",
        "keywords": ["练习", "专注", "反馈", "目标", "专家"],
        "scenarios": ["技能学习", "专业精进", "能力提升"],
        "description": "有目的的专项训练"
    },
    "Feynman": {
        "name": "费曼技巧",
        "file": "learning-growth.md",
        "series": "学习成长",
        "keywords": ["教学", "简化", "理解", "学习"],
        "scenarios": ["学习新知", "理解概念", "准备考试"],
        "description": "以教为学"
    },
    "GrowthMindset": {
        "name": "成长型思维",
        "file": "learning-growth.md",
        "series": "学习成长",
        "keywords": ["成长", "培养", "努力", "能力"],
        "scenarios": ["学习", "职业发展", "教育孩子"],
        "description": "能力可以培养"
    },
    "LearningPyramid": {
        "name": "学习金字塔",
        "file": "learning-growth.md",
        "series": "学习成长",
        "keywords": ["学习", "留存", "主动", "被动"],
        "scenarios": ["学习设计", "培训", "教学"],
        "description": "主动学习效果更好"
    },
    "SpacedRepetition": {
        "name": "间隔重复",
        "file": "learning-growth.md",
        "series": "学习成长",
        "keywords": ["间隔", "重复", "记忆", "复习"],
        "scenarios": ["语言学习", "考试复习", "技能培训"],
        "description": "分散学习记忆更牢"
    },
    "KnowledgeCompound": {
        "name": "知识复利",
        "file": "learning-growth.md",
        "series": "学习成长",
        "keywords": ["复利", "积累", "连接", "网络"],
        "scenarios": ["长期学习", "知识管理", "能力建设"],
        "description": "知识积累产生复利"
    },
    "TShaped": {
        "name": "T 型人才",
        "file": "learning-growth.md",
        "series": "学习成长",
        "keywords": ["深度", "广度", "专业", "跨界"],
        "scenarios": ["职业规划", "能力构建", "技能发展"],
        "description": "深度 + 广度"
    },
    "Flow": {
        "name": "心流理论",
        "file": "learning-growth.md",
        "series": "学习成长",
        "keywords": ["心流", "专注", "状态", "最佳"],
        "scenarios": ["工作效率", "创意设计", "运动表现"],
        "description": "全神贯注的最佳状态"
    },
    
    # ========== 人际沟通（8 个）==========
    "NVC": {
        "name": "非暴力沟通",
        "file": "communication-relationships.md",
        "series": "人际沟通",
        "keywords": ["沟通", "观察", "感受", "需要", "请求"],
        "scenarios": ["亲密关系", "亲子沟通", "职场沟通", "冲突调解"],
        "description": "观察 - 感受 - 需要 - 请求"
    },
    "EmotionalBank": {
        "name": "情感账户",
        "file": "communication-relationships.md",
        "series": "人际沟通",
        "keywords": ["关系", "信任", "存款", "取款"],
        "scenarios": ["关系维护", "团队建设", "客户服务"],
        "description": "关系如银行账户"
    },
    "SixDegrees": {
        "name": "六度分隔",
        "file": "communication-relationships.md",
        "series": "人际沟通",
        "keywords": ["人脉", "连接", "社交", "网络"],
        "scenarios": ["人脉拓展", "求职招聘", "信息传播"],
        "description": "任何两人最多隔 5 人"
    },
    "Dunbar": {
        "name": "邓巴数字",
        "file": "communication-relationships.md",
        "series": "人际沟通",
        "keywords": ["社交", "上限", "150", "圈层"],
        "scenarios": ["社交管理", "团队建设", "社区运营"],
        "description": "稳定社交上限 150 人"
    },
    "Reciprocity": {
        "name": "互惠原则",
        "file": "communication-relationships.md",
        "series": "人际沟通",
        "keywords": ["互惠", "回报", "给予", "交换"],
        "scenarios": ["影响力", "合作", "销售"],
        "description": "回报他人善意"
    },
    "Commitment": {
        "name": "承诺一致",
        "file": "communication-relationships.md",
        "series": "人际沟通",
        "keywords": ["承诺", "一致", "言行", "压力"],
        "scenarios": ["说服", "习惯养成", "目标达成"],
        "description": "言行一致的压力"
    },
    "SocialProof": {
        "name": "社会证明",
        "file": "communication-relationships.md",
        "series": "人际沟通",
        "keywords": ["证明", "跟随", "评价", "销量"],
        "scenarios": ["营销", "影响力", "产品设计"],
        "description": "跟随他人行为"
    },
    "Liking": {
        "name": "喜好原理",
        "file": "communication-relationships.md",
        "series": "人际沟通",
        "keywords": ["喜好", "喜欢", "说服", "魅力"],
        "scenarios": ["销售", "人际关系", "影响力"],
        "description": "喜欢更容易被说服"
    },
}

# ============================================================================
# 场景 - 模型映射（快速匹配）
# ============================================================================
SCENARIO_MAP = {
    "行业分析": ["Porter5", "PESTEL", "Cycle", "SWOT"],
    "投资决策": ["Probabilistic", "Bayes", "Antifragile", "PowerLaw", "LossAversion"],
    "职业规划": ["Comparative", "Opportunity", "LongTerm", "TShaped", "GrowthMindset"],
    "创业方向": ["BlueOcean", "Lean", "Network", "FirstPrinciples"],
    "竞争策略": ["Porter5", "GameTheory", "BlueOcean", "Comparative"],
    "风险评估": ["SecondOrder", "Inversion", "Antifragile", "Probabilistic"],
    "人际沟通": ["NVC", "EmotionalBank", "Reciprocity", "Liking"],
    "学习成长": ["DeliberatePractice", "Feynman", "GrowthMindset", "SpacedRepetition", "Flow"],
    "团队管理": ["Systems", "MECE", "EmotionalBank", "BrokenWindows"],
    "产品定价": ["GameTheory", "Network", "PowerLaw"],
    "市场进入": ["PESTEL", "Porter5", "BlueOcean", "Cycle"],
    "创新方向": ["FirstPrinciples", "BlueOcean", "Inversion", "DualProcess"],
    "会议决策": ["MECE", "GroupPolarization", "Asch", "SpiralSilence"],
    "自我提升": ["Metacognition", "DeliberatePractice", "GrowthMindset", "Flow"],
    "萧条期决策": ["Scarcity", "LossAversion", "HerdingBehavior", "Pessimism"],
    # 周期分析场景（新增）
    "周期分析": ["Cycle", "SecondOrder", "Antifragile", "PowerLaw", "LongTerm"],
    "经济周期": ["Cycle", "PESTEL", "SecondOrder", "Probabilistic"],
    "市场周期": ["Cycle", "Probabilistic", "Antifragile", "PowerLaw"],
    "行业周期": ["Cycle", "Porter5", "SecondOrder", "LongTerm"],
    "拐点判断": ["Cycle", "SecondOrder", "Probabilistic", "Inversion"],
}

# ============================================================================
# 推荐引擎核心函数
# ============================================================================

def calculate_match_score(model_data: Dict, query: str) -> int:
    """计算模型与查询的匹配度分数"""
    score = 0
    query_lower = query.lower()
    
    # 关键词匹配（权重最高）
    for keyword in model_data.get("keywords", []):
        if keyword.lower() in query_lower:
            score += 10
    
    # 场景匹配
    for scenario in model_data.get("scenarios", []):
        if scenario.lower() in query_lower:
            score += 8
    
    # 名称匹配
    if model_data.get("name", "").lower() in query_lower:
        score += 15
    
    # 描述匹配
    if model_data.get("description", "").lower() in query_lower:
        score += 5
    
    return score

def recommend_models(query: str, top_n: int = 5) -> List[Tuple[str, Dict, int]]:
    """推荐最匹配的模型"""
    scores = []
    
    for model_id, model_data in MODELS_DB.items():
        score = calculate_match_score(model_data, query)
        if score > 0:
            scores.append((model_id, model_data, score))
    
    # 按分数排序
    scores.sort(key=lambda x: x[2], reverse=True)
    
    return scores[:top_n]

def get_scenario_recommendations(scenario: str) -> List[str]:
    """根据预设场景推荐模型"""
    return SCENARIO_MAP.get(scenario, [])

def generate_analysis_framework(query: str, recommendations: List[Tuple]) -> str:
    """生成分析框架"""
    output = []
    output.append("\n# 📋 {} 分析框架\n".format(query))
    output.append("## 推荐模型组合\n")
    
    for i, (model_id, model_data, score) in enumerate(recommendations, 1):
        stars = "⭐" * min(5, max(1, score // 15))
        output.append("{}. **{}** - {}".format(i, model_data["name"], model_data["description"]))
        output.append("   - 匹配度：{} {}".format(stars, score))
        output.append("   - 文档：`{}`".format(model_data["file"]))
        output.append("")
    
    output.append("## 分析步骤\n")
    output.append("### 第一步：数据收集")
    output.append("- [ ] 收集相关数据和信息")
    output.append("- [ ] 识别关键因素")
    output.append("- [ ] 确定分析范围\n")
    
    output.append("### 第二步：模型应用\n")
    for model_id, model_data, score in recommendations:
        output.append("- [ ] 应用 **{}**: {}".format(model_data["name"], model_data["description"]))
    
    output.append("\n### 第三步：综合分析")
    output.append("- [ ] 整合各模型分析结果")
    output.append("- [ ] 识别关键发现")
    output.append("- [ ] 形成结论和建议\n")
    
    return "\n".join(output)

def detect_scenario(query: str) -> Optional[str]:
    """检测查询属于哪个预设场景"""
    query_lower = query.lower()
    for scenario in SCENARIO_MAP.keys():
        if scenario.lower() in query_lower:
            return scenario
    return None

# ============================================================================
# 主函数
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="思维模型推荐引擎 v2.1")
    parser.add_argument("query", nargs="?", help="要分析的问题或场景")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    parser.add_argument("--top", type=int, default=5, help="推荐模型数量（默认：5）")
    parser.add_argument("--list", action="store_true", help="列出所有可用模型")
    parser.add_argument("--stats", action="store_true", help="显示统计信息")
    
    args = parser.parse_args()
    
    # 列出所有模型
    if args.list:
        print("📚 思维模型库 v2.1 - 共 {} 个模型\n".format(len(MODELS_DB)))
        series_count = {}
        for model_id, model_data in MODELS_DB.items():
            series = model_data.get("series", "其他")
            if series not in series_count:
                series_count[series] = []
            series_count[series].append(model_data["name"])
        
        for series, models in sorted(series_count.items()):
            print("### {}（{}个）".format(series, len(models)))
            for model in models:
                print("  - {}".format(model))
            print("")
        return
    
    # 显示统计
    if args.stats:
        series_count = {}
        for model_data in MODELS_DB.values():
            series = model_data.get("series", "其他")
            series_count[series] = series_count.get(series, 0) + 1
        
        print("📊 思维模型库统计")
        print("=" * 50)
        print("总模型数：{}".format(len(MODELS_DB)))
        print("预设场景：{}".format(len(SCENARIO_MAP)))
        print("\n系列分布:")
        for series, count in sorted(series_count.items(), key=lambda x: x[1], reverse=True):
            print("  {}: {} 个".format(series, count))
        return
    
    # 检查查询
    if not args.query:
        print("🧠 思维模型推荐引擎 v2.1")
        print("\n使用方法:")
        print("  python recommend.py \"你的问题\"")
        print("  python recommend.py \"我要分析新能源汽车行业\"")
        print("  python recommend.py \"如何评估投资机会\" --json")
        print("\n选项:")
        print("  --list    列出所有可用模型")
        print("  --stats   显示统计信息")
        print("  --json    输出 JSON 格式")
        print("  --top N   推荐 N 个模型（默认：5）")
        print("\n示例:")
        print("  python recommend.py \"我要分析一个行业是否值得进入\"")
        print("  python recommend.py \"如何提升学习效率\"")
        print("  python recommend.py \"分析 Tesla 的竞争优势\"")
        return
    
    query = args.query
    print("🔍 分析问题：{}\n".format(query))
    
    # 检测预设场景
    scenario = detect_scenario(query)
    if scenario:
        print("📌 识别场景：{}\n".format(scenario))
        scenario_models = get_scenario_recommendations(scenario)
        # 获取场景模型的详细信息
        scenario_recommendations = []
        for model_id in scenario_models:
            if model_id in MODELS_DB:
                score = calculate_match_score(MODELS_DB[model_id], query)
                scenario_recommendations.append((model_id, MODELS_DB[model_id], score + 20))  # 场景匹配加分
    
    # 获取推荐
    recommendations = recommend_models(query, args.top)
    
    # 合并场景推荐和关键词推荐
    if scenario and scenario_recommendations:
        all_recs = {r[0]: r for r in recommendations}
        for r in scenario_recommendations:
            if r[0] not in all_recs:
                all_recs[r[0]] = r
        recommendations = sorted(all_recs.values(), key=lambda x: x[2], reverse=True)[:args.top]
    
    if not recommendations:
        print("⚠️  未找到匹配的模型，请尝试其他关键词")
        print("\n可用场景:")
        for s in list(SCENARIO_MAP.keys())[:10]:
            print("  - {}".format(s))
        print("\n使用 --list 查看所有模型")
        return
    
    # 输出结果
    if args.json:
        result = {
            "query": query,
            "scenario": scenario,
            "recommendations": [
                {
                    "id": model_id,
                    "name": data["name"],
                    "file": data["file"],
                    "series": data.get("series", ""),
                    "description": data["description"],
                    "score": score
                }
                for model_id, data, score in recommendations
            ]
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("## 📊 推荐模型组合\n")
        for i, (model_id, model_data, score) in enumerate(recommendations, 1):
            stars = "⭐" * min(5, max(1, score // 15))
            print("{}. **{}**".format(i, model_data["name"]))
            print("   - 描述：{}".format(model_data["description"]))
            print("   - 系列：{}".format(model_data.get("series", "其他")))
            print("   - 文档：`{}`".format(model_data["file"]))
            print("   - 匹配度：{} {}".format(stars, score))
            print("")
        
        print("=" * 60)
        print(generate_analysis_framework(query, recommendations))

if __name__ == "__main__":
    main()
