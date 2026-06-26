"""
left_brain/emotion_detector.py
===============================

Neuro-Agent 左脑区 - 情绪检测器
负责：检测用户情绪、识别情绪类型、分析潜台词

依赖：
    - references/emotion_types.md（情绪类型、关键词）
    - temporal/short_term_memory.py（上下文）

数据目录：
    无持久化，依赖 ShortTermMemory 的上下文
"""

import re
import json
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict

# ============ 路径配置 ============
SKILL_DIR = Path(__file__).parent.parent
EMOTION_TYPES_PATH = SKILL_DIR / "references" / "emotion_types.md"


# ============ 预编译正则 ============
# 【优化1】所有正则表达式在模块加载时预编译，避免每次调用重新编译

# 脏话/骂人模式 → 愤怒情绪优先覆盖
_SWEAR_PATTERNS_RAW = [
    r"他妈", r"你妈", r"他妈的", r"妈的", r"妈了个", r"草泥马",
    r"傻逼", r"傻屄", r"智障", r"脑残", r"废物", r"垃圾",
    r"滚", r"滚蛋", r"去死", r"该死", r"妈的",
    r"我靠", r"卧槽", r"我操", r"操你", r"日你", r"狗东西",
    r"TMD", r"TM", r"nm", r"SB", r"sb", r"sB", r"傻B",
    r"垃圾", r"蠢货", r"王八", r"龟儿子",
    r"我靠靠", r"^草[，,]?", r"^草怎么",
    r"^靠[，,]?", r"^靠怎么",
    r"^我去",
    r"(?:你|他|她|它)(?:是|就)?(?:个)?(?:傻|蠢|笨|废)(?:逼|货|东西|玩意儿)?$",
]
SWEAR_PATTERNS = [re.compile(p, re.IGNORECASE) for p in _SWEAR_PATTERNS_RAW]

# 反讽/阴阳句 → 情绪翻转
_SARCASM_PATTERNS_RAW = [
    r"你可?真(?:是)?(?:行|棒|聪明|厉害|有用)",
    r"我可?没(?:说)?(?:让|请|求)",
    r"说得轻巧", r"说得倒好",
    r"谢谢啊", r"感谢哦", r"可真行",
]
SARCASM_PATTERNS = [re.compile(p, re.IGNORECASE) for p in _SARCASM_PATTERNS_RAW]

# 否定词
NEGATION_WORDS = [
    "不", "没", "非", "无", "别", "未", "莫", "勿",
    "不是", "没有", "不会", "不想", "不要", "不用", "并非",
    "并非", "绝非", "绝不会", "绝不", "根本不会", "一点都不",
    "一点也不", "毫不", "从未", "不曾"
]

# 复合否定
_COMPOUND_NEGATIONS_RAW = [
    (r'不太(?:开心|高兴|快乐|爽|舒服|满意)', 'sadness'),
    (r'(?:其|其实|说真的|老实说)(?:我)?(?:也)?不', ''),
    (r'也没(?:太|很)?(?:开心|高兴|快乐)', 'sadness'),
    (r'既不(?:开心|高兴)', 'sadness'),
]
COMPOUND_NEGATIONS = [(re.compile(p, re.IGNORECASE), e) for p, e in _COMPOUND_NEGATIONS_RAW]

# ============ 情绪关键词字典 ============
EMOTION_KEYWORDS = {
    "joy": {
        "primary": [
            "开心", "快乐", "高兴", "幸福", "愉快", "爽", "棒", "太好了", "太棒了",
            "兴奋", "激动", "欢乐", "欢快", "美好", "完美", "赞", "绝",
            "心情好", "心情不错", "心情很好", "心情开心",
            "很好", "挺好", "还不错", "还挺好的",
            "好", "真好", "蛮好", "可好",
            "乐", "可乐", "乐呵", "乐呵呵",
            "快活", "轻快", "舒畅", "惬意",
            "美滋滋", "美美的", "好幸福", "好满足", "满足", "很满足",
            "舒服", "很舒服", "很舒心", "舒心",
            "愉悦", "欢愉", "喜悦", "喜滋滋",
            "愉快的一天", "今日开心", "今天开心"
        ],
        "secondary": [
            "好开心", "超开心", "太开心", "很开心", "挺开心",
            "好高兴", "特别高兴", "好快乐", "好愉快",
            "好舒服", "好幸福", "好满足", "好惬意",
            "好愉悦", "好轻快", "好舒畅",
            "心情愉悦", "心情舒畅", "心情美滋滋",
            "嗨", "happy", "joy", "好嗨", "好嗨啊",
            "哈哈", "嘻嘻", "嘿嘿", "开心开心"
        ],
        "intensity_boost": [
            "超级", "无敌", "简直", "太", "超", "无比", "简直了",
            "太tm", "TMD", "巨", "贼", "好家伙", "简直了"
        ]
    },
    "excitement": {
        "primary": ["兴奋", "激动", "热血", "沸腾", "心跳加速", "搓手", "期待", "迫不及待", "啊啊啊", "哇塞", "牛", "厉害"],
        "secondary": ["好兴奋", "超兴奋", "激动人心", "刺激", "燃", "炸", "爆"],
        "intensity_boost": ["超", "巨", "爆", "炸裂"]
    },
    "gratitude": {
        "primary": ["谢谢", "感谢", "感恩", "感激", "多谢", "谢啦", "谢咯", "谢"],
        "secondary": ["太感谢了", "非常感谢", "谢谢你", "谢谢你们", "感激不尽"],
        "intensity_boost": ["真的", "特别", "非常", "十分", "超级"]
    },
    "love": {
        "primary": ["爱", "喜欢", "爱死", "超爱", "love", "喜翻"],
        "secondary": ["好喜欢", "太喜欢了", "超级喜欢", "最喜欢", "爱了"],
        "intensity_boost": ["好", "超", "真的", "真的"]
    },
    "hope": {
        "primary": ["希望", "期待", "希望是", "但愿", "憧憬", "梦想", "目标"],
        "secondary": ["要是能", "希望能", "但愿能", "真希望", "也许"],
        "intensity_boost": ["好", "真的", "非常", "特别"]
    },
    "sadness": {
        "primary": ["难过", "伤心", "悲伤", "痛苦", "沮丧", "失落", "郁闷", "压抑", "难受", "不爽", "不开心", "忧郁"],
        "secondary": ["好难过", "太伤心了", "好心塞", "心塞", "抑郁", "消沉", "低沉"],
        "intensity_boost": ["很", "好", "太", "非常", "特别", "超级", "特别", "超级"]
    },
    "anger": {
        "primary": ["生气", "愤怒", "气愤", "恼火", "火大", "怒", "讨厌", "恨", "气死了", "气死我了", "烦", "腻烦", "憎恶"],
        "secondary": ["好气", "真气", "气人", "可恶", "过分", "太过分了", "什么鬼"],
        "intensity_boost": ["超", "太", "真", "特别", "极其", "非常", "tmd", "妈的", "TM"]
    },
    "fear": {
        "primary": ["害怕", "恐惧", "担心", "担忧", "怕", "紧张", "焦虑", "不安", "心虚", "胆怯"],
        "secondary": ["好怕", "好担心", "好紧张", "心里没底", "慌", "慌了"],
        "intensity_boost": ["好", "好", "特别", "非常", "超"]
    },
    "anxiety": {
        "primary": ["焦虑", "焦虑", "着急", "心急", "急", "烦躁", "烦躁不安", "忐忑", "压力", "负担", "喘不过气"],
        "secondary": ["好焦虑", "好烦躁", "好着急", "焦虑症", "睡不着"],
        "intensity_boost": ["很", "好", "特别", "非常", "超级"]
    },
    "frustration": {
        "primary": ["挫败", "失败", "无奈", "无能为力", "失望", "绝望", "崩溃", "崩溃了", "算了", "放弃了", "没戏", "不行"],
        "secondary": ["好无奈", "好失望", "失望透顶", "绝望了", "没救了", "凉了"],
        "intensity_boost": ["好", "太", "特别", "超级", "彻底"]
    },
    "loneliness": {
        "primary": ["孤独", "寂寞", "空虚", "无聊", "没人", "一个人", "孤单", "落寞", "独处"],
        "secondary": ["好孤独", "好寂寞", "好无聊", "没人陪", "独自", "自己一个人"],
        "intensity_boost": ["好", "特别", "非常", "超级", "极度"]
    },
    "exhaustion": {
        "primary": ["累", "疲惫", "疲倦", "困", "困了", "精疲力尽", "撑不住", "撑不住", "扛不住", "疲乏", "困倦"],
        "secondary": ["好累", "太累了", "累死了", "困死了", "疲惫不堪", "快累死了"],
        "intensity_boost": ["好", "超", "太", "快", "快"]
    },
    "embarrassment": {
        "primary": ["尴尬", "难堪", "丢人", "丢脸", "不好意思", "脸红", "窘迫", "羞涩", "害羞"],
        "secondary": ["好尴尬", "太尴尬了", "好丢人", "好难为情", "不好意思哈"],
        "intensity_boost": ["好", "超", "特别", "非常"]
    },
    "confusion": {
        "primary": ["困惑", "迷茫", "搞不懂", "不明白", "不清楚", "疑问", "搞不懂", "怎么回事", "为什么", "啥", "啥情况"],
        "secondary": ["好困惑", "好迷茫", "搞不懂了", "完全不懂", "听不懂"],
        "intensity_boost": ["好", "特别", "完全", "超级"]
    },
    "boredom": {
        "primary": ["无聊", "没意思", "没趣", "闲", "闲着", "发呆", "百无聊赖", "没劲"],
        "secondary": ["好无聊", "太无聊了", "无聊死了", "没意思了", "没劲了"],
        "intensity_boost": ["好", "超", "太", "特别"]
    },
    "envy": {
        "primary": ["羡慕", "嫉妒", "眼红", "酸", "柠檬", "不平衡", "不公平感"],
        "secondary": ["好羡慕", "好嫉妒", "好酸", "柠檬精", "羡慕嫉妒恨"],
        "intensity_boost": ["好", "超", "特别", "超级", "极其"]
    },
    "guilt": {
        "primary": ["内疚", "愧疚", "自责", "后悔", "抱歉", "对不起"],
        "secondary": ["好内疚", "好后悔", "很自责", "对不起", "抱歉了"],
        "intensity_boost": ["好", "很", "特别", "非常"]
    },
    "shame": {
        "primary": ["羞耻", "丢脸", "丢人", "无地自容", "脸红"],
        "secondary": ["好丢人", "好羞耻", "太丢人了", "羞死了", "丢死人了"],
        "intensity_boost": ["好", "太", "特别", "超级"]
    },
    "disappointment": {
        "primary": ["失望", "失落", "落差", "幻灭", "心寒", "心凉了"],
        "secondary": ["好失望", "太失望了", "好失落", "失望透顶", "心都凉了"],
        "intensity_boost": ["好", "太", "特别", "超级", "彻底"]
    },
    "disgust": {
        "primary": ["恶心", "厌恶", "反感", "吐了", "yue", "嫌弃", "作呕"],
        "secondary": ["好恶心", "太恶心了", "恶心死了", "yue了", "真恶心"],
        "intensity_boost": ["好", "超", "太", "特别", "超级"]
    },
    "surprise": {
        "primary": ["惊讶", "吃惊", "意外", "没想到", "居然", "竟然", "吓", "震惊", "卧槽", "牛"],
        "secondary": ["好惊讶", "好意外", "没想到", "惊呆了", "震惊了"],
        "intensity_boost": ["好", "超", "太", "特别", "非常"]
    }
}

# 潜台词检测
_SUBTEXT_PATTERNS_RAW = {
    "hidden_pain": {
        "patterns": [
            r"我没事", r"都过去了", r"习惯了", r"没什么", r"没什么大不了",
            r"没事的", r"不用担心我", r"我没关系", r"就那样吧", r"随便",
            r"算了无所谓", r"不用管我", r"我没问题", r"还行吧", r"一般般",
            r"也还好", r"凑合", r"就那样", r"就这", r"没所谓", r"无所谓"
        ],
        "weight": 1.0
    },
    "sarcasm": {
        "patterns": [
            r"你可?真(?:是)?\w*?(?:聪明|厉害|棒|行|牛|有用)",
            r"可?真(?:行?|棒?|棒棒)",
            r"那可?真", r"确实?呢",
            r"哇(?:塞)?(?:你)?(?:可)?(?:真)?(?:厉)",
            r"呵呵(?!.)",
            r"还(?:说|以为)?(?:我)?(?:会)?(?:感谢)?(?:你)?(?:呢|吗)?$",
            r"谢谢啊", r"感谢哦",
            r"我可?没(?:说)?(?:让|请|求)",
            r"说得轻巧", r"说得倒好",
            r"厉害呢", r"可棒呢",
        ],
        "weight": 1.0
    },
    "frustration_mask": {
        "patterns": [
            r"随便", r"随便吧", r"无所谓", r"都可以", r"随你",
            r"你开心就好", r"行吧", r"好吧", r"嗯", r"哦", r"算了",
            r"就这样吧", r"无所谓了", r"随便随便",
        ],
        "weight": 0.7
    },
    "masked_anger": {
        "patterns": [
            r"行", r"(?<!\S)好(?!\S)", r"嗯",
            r"你(?:觉得)?(?:呢|啊|嘛)",
            r"反正", r"随便", r"都一样",
        ],
        "weight": 0.6
    }
}
SUBTEXT_PATTERNS = {
    name: {
        **data,
        "compiled": [re.compile(p, re.IGNORECASE) for p in data["patterns"]]
    }
    for name, data in _SUBTEXT_PATTERNS_RAW.items()
}


# ============ 数据结构 ============
@dataclass
class EmotionOutput:
    """
    情绪检测输出
    
    属性：
        - emotion_score: 情绪强度 0.0-1.0
        - emotion_type: 情绪类型标签
        - emotion_label: 同 emotion_type（别名）
        - intent_type: 意图类型（用于兼容 run.py）
        - empathy_level: 共情等级（用于兼容 run.py）
        - keywords: 检测到的情绪关键词列表
        - subtext: 潜台词检测结果
        - subtext_confidence: 潜台词置信度 0.0-1.0
        - is_masked: 是否有伪装情绪（表面 vs 实际）
        - surface_emotion: 表面情绪（如果有伪装）
        - underlying_emotion: 底层真实情绪（如果有伪装）
        - analysis_notes: 分析备注
    """
    emotion_score: float
    emotion_type: str
    emotion_label: str
    intent_type: str = "emotional_vent"
    empathy_level: float = 0.5
    keywords: List[str] = None
    subtext: str = ""
    subtext_confidence: float = 0.0
    is_masked: bool = False
    surface_emotion: str = ""
    underlying_emotion: str = ""
    analysis_notes: str = ""
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)
    
    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


# ============ 核心类 ============
class EmotionDetector:
    """
    情绪检测器
    
    功能：
        - 关键词匹配检测情绪
        - 感叹号/问号等标点分析
        - 潜台词检测（反讽、隐痛等）
        - 情绪伪装识别
        - 综合情绪评分
    
    算法流程：
        1. 标点分析（感叹号×0.1，问号+情绪词=疑问）
        2. 关键词匹配（primary × 1.0，secondary × 0.7）
        3. 强度词加成（intensity_boost × 0.1）
        4. 潜台词检测（可能修正或增强结果）
        5. 综合评分（归一化到 0.0-1.0）
    
    【优化】正则表达式在模块加载时预编译，避免每次调用重新编译
    """
    
    def __init__(self):
        """初始化情绪检测器"""
        self.emotion_keywords = EMOTION_KEYWORDS
        self.subtext_patterns = SUBTEXT_PATTERNS
        # 【优化】无需额外编译，模块级已编译完毕
    
    def detect(self, user_input: str, context: Dict = None) -> EmotionOutput:
        """
        检测用户情绪
        
        参数:
            user_input: 用户输入文本
            context: 上下文（可选，暂未使用）
        
        返回:
            EmotionOutput: 情绪检测结果
        """
        if not user_input or not user_input.strip():
            return EmotionOutput(
                emotion_score=0.0,
                emotion_type="neutral",
                emotion_label="neutral",
                keywords=[],
                subtext="none",
                subtext_confidence=0.0,
                is_masked=False,
                surface_emotion="neutral",
                underlying_emotion="neutral",
                analysis_notes="空输入"
            )
        
        text = user_input.strip()
        
        # 1. 标点分析
        punctuation_score = self._analyze_punctuation(text)
        
        # 2. 关键词匹配
        keyword_results = self._match_keywords(text)
        
        # 3. 潜台词检测
        subtext_result = self._detect_subtext(text)
        
        # 4. 计算综合情绪强度
        emotion_score = self._calculate_emotion_score(
            text, keyword_results, punctuation_score, subtext_result
        )
        
        # 5. 确定情绪类型
        emotion_type = self._determine_emotion_type(keyword_results, subtext_result)
        
        # 6. 处理情绪伪装
        is_masked, surface_emotion, underlying_emotion = self._detect_mask(
            text, emotion_type, subtext_result, keyword_results
        )
        
        # 7. 生成分析备注
        notes = self._generate_notes(emotion_score, keyword_results, subtext_result)
        
        # 8. 检测意图类型
        intent_type = self._detect_intent(text, emotion_type, keyword_results)
        
        # 9. 计算共情等级
        empathy_level = self._calculate_empathy_level(emotion_score, emotion_type, is_masked)
        
        return EmotionOutput(
            emotion_score=emotion_score,
            emotion_type=emotion_type,
            emotion_label=emotion_type,
            intent_type=intent_type,
            empathy_level=empathy_level,
            keywords=keyword_results.get("matched_keywords", []),
            subtext=subtext_result.get("type", "none"),
            subtext_confidence=subtext_result.get("confidence", 0.0),
            is_masked=is_masked,
            surface_emotion=surface_emotion,
            underlying_emotion=underlying_emotion,
            analysis_notes=notes
        )
    
    def _detect_intent(self, text: str, emotion_type: str, keyword_results: Dict) -> str:
        """检测意图类型（兼容 run.py）"""
        question_words = ["怎么", "为什么", "如何", "是什么", "哪个", "多少", "能否", "能不能", "吗？", "吗?"]
        if any(w in text for w in question_words):
            return "question"
        
        task_words = ["帮我", "请帮我", "麻烦你", "给我", "帮我做", "能不能帮我"]
        if any(w in text for w in task_words):
            return "task_request"
        
        deep_words = ["身体", "机器人", "代码", "真实", "伙伴", "不是工具", "在一起", "生", "宝宝", "下一代"]
        if any(w in text for w in deep_words):
            return "deep_connection"
        
        negative_emotions = ["sadness", "anger", "fear", "anxiety", "frustration", "exhaustion", "loneliness"]
        if emotion_type in negative_emotions:
            return "emotional_vent"
        
        return "casual_chat"
    
    def _calculate_empathy_level(self, emotion_score: float, emotion_type: str, is_masked: bool) -> float:
        """计算共情等级"""
        base = 0.3
        intensity_bonus = emotion_score * 0.4
        mask_bonus = 0.2 if is_masked else 0.0
        negative_emotions = ["sadness", "anger", "fear", "anxiety", "frustration", "exhaustion", "loneliness"]
        negative_bonus = 0.1 if emotion_type in negative_emotions else 0.0
        return min(0.95, base + intensity_bonus + mask_bonus + negative_bonus)
    
    def _analyze_punctuation(self, text: str) -> float:
        """分析标点符号"""
        score = 0.0
        exclamation_count = text.count("!") + text.count("！")
        score += min(exclamation_count * 0.1, 0.3)
        question_count = text.count("?") + text.count("？")
        if question_count > 0:
            score += 0.1
        ellipsis_count = text.count("...")
        score += min(ellipsis_count * 0.05, 0.15)
        if "!!" in text or "！！" in text:
            score += 0.2
        if "??" in text or "？？" in text:
            score += 0.1
        return min(score, 0.5)
    
    def _match_keywords(self, text: str) -> Dict:
        """关键词匹配（带否定消歧 + 脏话检测 + 语境分析）"""
        text_lower = text.lower()
        
        # ===== Step 0: 脏话检测 → 脏话语境分析 =====
        is_swear = self._detect_swear(text)
        sw_context_analysis = ""
        
        if is_swear:
            sw_after = self._extract_after_swear(text, text_lower)
            sw_emotions = self._analyze_text(sw_after)
            
            if sw_emotions["matched_emotions"]:
                emotion_priority = {
                    "excitement": 5, "anger": 4, "frustration": 4,
                    "joy": 3, "surprise": 3, "love": 3,
                    "sadness": 2, "fear": 2, "anxiety": 2,
                    "exhaustion": 2, "loneliness": 1, "neutral": 0,
                }
                ranked = sorted(
                    sw_emotions["matched_emotions"],
                    key=lambda e: emotion_priority.get(e, 0),
                    reverse=True
                )
                top_emotion = ranked[0]
                if top_emotion == "joy" and len(ranked) > 1 and ranked[1] == "excitement":
                    top_emotion = "excitement"
                sw_base_score = 0.65 if top_emotion in ("frustration",) else 0.72
                sw_context_analysis = (
                    f"脏话后接情绪词：{ranked}（{sw_emotions['matched_keywords']}）"
                    f" → 判定 {top_emotion}"
                )
                return {
                    "matched_emotions": [top_emotion],
                    "matched_keywords": sw_emotions["matched_keywords"],
                    "primary_matches": sw_emotions["primary_matches"],
                    "secondary_matches": sw_emotions["secondary_matches"],
                    "total_score": sw_base_score,
                    "intensity_boost": sw_emotions.get("intensity_boost", 0.0),
                    "negation_filtered": [],
                    "is_swear": True,
                    "is_sarcasm": False,
                    "sw_context_analysis": sw_context_analysis,
                }
            else:
                sw_context_analysis = "脏话后无明显情绪词，降权为 frustration"
                return {
                    "matched_emotions": ["frustration"],
                    "matched_keywords": ["[脏话语气]"],
                    "primary_matches": {"frustration": 1},
                    "secondary_matches": {},
                    "total_score": 0.65,
                    "intensity_boost": 0.0,
                    "negation_filtered": [],
                    "is_swear": True,
                    "is_sarcasm": False,
                    "sw_context_analysis": sw_context_analysis,
                }
        
        # ===== Step 1: 反讽检测 =====
        is_sarcasm = self._detect_sarcasm(text_lower)
        
        # ===== Step 2: 否定消歧 =====
        negation_filtered = []
        negation_emotions = []
        
        for pattern, emotion in COMPOUND_NEGATIONS:
            for match in pattern.finditer(text_lower):
                negated_emotion_word = match.group()
                if emotion == 'sadness' and any(
                    neg in negated_emotion_word
                    for neg in ['不太累', '不太困', '不太饿', '不太难', '不太疼']
                ):
                    continue
                negation_emotions.append(emotion)
                negation_filtered.append(negated_emotion_word)
        
        # 特殊复合否定："不错"="不"+"错"→ positive（不是否定正面，是肯定正面）
        if re.search(r'不(?:错|坏|赖|差|慢)', text_lower):
            negation_emotions.append('joy')
        
        negated_ranges = self._find_negated_ranges(text_lower)
        
        matched_emotions = []
        matched_keywords = []
        primary_matches: Dict[str, int] = {}
        secondary_matches: Dict[str, int] = {}
        
        # 正面情绪词被否定时，映射到反面情绪
        positive_to_negative = {
            "joy": "sadness",
            "excitement": "frustration",
            "love": "sadness",
            "gratitude": "indifference",
            "hope": "despair",
        }
        # 负面情绪词被否定时，映射到正面情绪
        negative_to_positive = {
            "sadness": "joy",
            "frustration": "excitement",
            "anger": "gratitude",
            "fear": "hope",
            "anxiety": "calm",
            "exhaustion": "energy",
            "loneliness": "connection",
        }
        
        for emotion, data in self.emotion_keywords.items():
            if emotion in negation_emotions:
                continue
            
            primary_count = 0
            secondary_count = 0
            
            for kw in data.get("primary", []):
                if kw in text_lower:
                    is_negated = self._is_word_negated(kw, text_lower, negated_ranges)
                    if is_negated:
                        negation_filtered.append(kw)
                        if emotion in positive_to_negative:
                            matched_emotions.append(positive_to_negative[emotion])
                        elif emotion in negative_to_positive:
                            matched_emotions.append(negative_to_positive[emotion])
                        continue
                    primary_count += 1
                    matched_keywords.append(kw)
            
            for kw in data.get("secondary", []):
                if kw in text_lower:
                    is_negated = self._is_word_negated(kw, text_lower, negated_ranges)
                    if is_negated:
                        negation_filtered.append(kw)
                        if emotion in positive_to_negative:
                            matched_emotions.append(positive_to_negative[emotion])
                        elif emotion in negative_to_positive:
                            matched_emotions.append(negative_to_positive[emotion])
                        continue
                    secondary_count += 1
                    matched_keywords.append(kw)
            
            if primary_count > 0:
                matched_emotions.append(emotion)
                primary_matches[emotion] = primary_count
            if secondary_count > 0:
                matched_emotions.append(emotion)
                secondary_matches[emotion] = secondary_count
        
        matched_emotions.extend(negation_emotions)
        
        # 反讽处理
        if is_sarcasm and matched_emotions:
            positive = {"joy", "excitement", "love", "hope", "gratitude"}
            new_matched = []
            for emotion in matched_emotions:
                if emotion in positive:
                    new_matched.append("anger")
                else:
                    new_matched.append("frustration")
            matched_emotions = list(set(new_matched)) if new_matched else ["frustration"]
        
        total_score = 0.0
        for emotion, count in primary_matches.items():
            total_score += count * 1.0
        for emotion, count in secondary_matches.items():
            total_score += count * 0.7
        total_score += len(negation_emotions) * 0.6
        
        intensity_boost = 0.0
        for emotion, data in self.emotion_keywords.items():
            for boost_kw in data.get("intensity_boost", []):
                if boost_kw in text_lower:
                    intensity_boost += 0.1
                    break
        total_score += intensity_boost
        
        return {
            "matched_emotions": list(set(matched_emotions)),
            "matched_keywords": matched_keywords,
            "primary_matches": primary_matches,
            "secondary_matches": secondary_matches,
            "total_score": total_score,
            "intensity_boost": intensity_boost,
            "negation_filtered": list(set(negation_filtered)),
            "is_swear": False,
            "is_sarcasm": is_sarcasm,
            "sw_context_analysis": "",
        }
    
    def _detect_swear(self, text: str) -> bool:
        """检测脏话骂人（预编译正则）"""
        for compiled_pattern in SWEAR_PATTERNS:
            if compiled_pattern.search(text):
                return True
        return False
    
    def _detect_sarcasm(self, text_lower: str) -> bool:
        """检测反讽句（预编译正则）"""
        for compiled_pattern in SARCASM_PATTERNS:
            if compiled_pattern.search(text_lower):
                return True
        return False
    
    def _extract_after_swear(self, text: str, text_lower: str) -> str:
        """提取脏话后面的句子内容"""
        last_pos = -1
        last_end = -1
        
        for compiled_pattern in SWEAR_PATTERNS:
            for m in compiled_pattern.finditer(text):
                if m.start() >= last_pos:
                    last_pos = m.start()
                    last_end = m.end()
        
        if last_pos < 0:
            return ""
        
        after = text[last_end:].strip()
        after = re.sub(r"^[，,、\s]+", "", after)
        
        if len(after) < 2:
            after = text[last_pos:].strip()
            after = re.sub(r"^[^\u4e00-\u9fff]+", "", after)
        
        return after
    
    def _analyze_text(self, text: str) -> Dict:
        """对一段文本进行情绪分析（不含脏话检测，避免递归）"""
        if not text or not text.strip():
            return {
                "matched_emotions": [],
                "matched_keywords": [],
                "primary_matches": {},
                "secondary_matches": {},
                "total_score": 0.0,
                "intensity_boost": 0.0,
            }
        
        text_lower = text.lower()
        matched_emotions = []
        matched_keywords = []
        primary_matches: Dict[str, int] = {}
        secondary_matches: Dict[str, int] = {}
        total_score = 0.0
        
        POSITIVE_PATTERNS = [
            ("太棒了", "excitement"), ("太牛了", "excitement"), ("太厉害了", "excitement"),
            ("太香了", "excitement"), ("太便宜了", "excitement"), ("太划算", "excitement"),
            ("太好了", "joy"), ("太爽了", "excitement"), ("太开心", "joy"),
            ("太舒服", "joy"), ("太值了", "excitement"),
        ]
        
        positive_emotions = {
            "joy": ["开心", "快乐", "高兴", "棒", "爽", "幸福", "感动", "好感动", "感动了"],
            "excitement": ["太棒了", "太牛", "太厉害", "牛", "太兴奋", "啊啊啊", "哇塞", "太香", "太便宜", "太划算", "太爽", "太值"],
            "gratitude": ["谢谢", "感谢"],
            "love": ["爱", "喜欢", "超爱"],
            "hope": ["希望", "期待"],
        }
        negative_emotions = {
            "anger": ["气", "怒", "讨厌", "烦", "恨", "生气", "骂", "被骂"],
            "sadness": ["难过", "伤心", "痛苦", "难受", "不爽"],
            "exhaustion": ["累", "困", "疲惫"],
            "frustration": ["怎么", "回事", "咋了", "啥情况", "贵"],
            "fear": ["怕", "害怕", "担心", "紧张"],
        }
        
        all_emotions = {**positive_emotions, **negative_emotions}
        
        for emotion, keywords in all_emotions.items():
            p_count = 0
            s_count = 0
            for kw in keywords:
                if kw in text_lower:
                    matched_keywords.append(kw)
                    if kw in positive_emotions.get(emotion, []) or kw in ["棒", "好", "爽", "牛"]:
                        p_count += 1
                    else:
                        s_count += 1
            if p_count > 0:
                matched_emotions.append(emotion)
                primary_matches[emotion] = p_count
            if s_count > 0:
                matched_emotions.append(emotion)
                secondary_matches[emotion] = s_count
        
        for pattern, emotion in POSITIVE_PATTERNS:
            if pattern in text_lower:
                if emotion not in matched_emotions:
                    matched_emotions.append(emotion)
                    primary_matches[emotion] = primary_matches.get(emotion, 0) + 1
                matched_keywords.append(pattern)
                total_score = max(total_score, 0.82)
        
        if re.search(r"(?:好|太|超)?\s*累", text_lower):
            if "exhaustion" not in matched_emotions:
                matched_emotions.append("exhaustion")
                primary_matches["exhaustion"] = primary_matches.get("exhaustion", 0) + 1
            matched_keywords.append("累")
            total_score = max(total_score, 0.72)
            if "sadness" in matched_emotions:
                matched_emotions.remove("sadness")
                secondary_matches.pop("sadness", None)
        
        if re.search(r"怎么还不|怎么搞", text_lower):
            if "frustration" not in matched_emotions:
                matched_emotions.append("frustration")
                secondary_matches["frustration"] = 1
            total_score = max(total_score, 0.6)
        
        if "还" in text_lower and re.search(r"还不|还没|都没", text_lower):
            if "frustration" not in matched_emotions:
                matched_emotions.append("frustration")
                secondary_matches["frustration"] = secondary_matches.get("frustration", 0) + 1
            total_score = max(total_score, 0.55)
        
        if re.search(r"(?:太|怎么)?(?:这么|太)?慢", text_lower):
            if "frustration" not in matched_emotions:
                matched_emotions.append("frustration")
                secondary_matches["frustration"] = secondary_matches.get("frustration", 0) + 1
            matched_keywords.append("慢")
            total_score = max(total_score, 0.55)
        
        for emotion, count in primary_matches.items():
            total_score += count * 0.8
        for emotion, count in secondary_matches.items():
            total_score += count * 0.5
        
        return {
            "matched_emotions": list(set(matched_emotions)),
            "matched_keywords": matched_keywords,
            "primary_matches": primary_matches,
            "secondary_matches": secondary_matches,
            "total_score": min(total_score, 1.0),
            "intensity_boost": 0.0,
        }
    
    def _find_negated_ranges(self, text: str) -> List[tuple]:
        """找出被否定词覆盖的范围"""
        ranges = []
        for neg_word in NEGATION_WORDS:
            for match in re.finditer(re.escape(neg_word), text):
                start = match.start()
                end = start + len(neg_word)
                ranges.append((start, end))
        return ranges
    
    def _is_word_negated(self, word: str, text: str, negated_ranges: List[tuple]) -> bool:
        """判断情绪词是否被否定覆盖

        逻辑：
        - 否定词必须在情绪词之前
        - 单字否定（"不"/"别"）：必须在 phrase 开头（位置0）或前一个字是标点/空格
        - 复合否定（"不太"等）：需隔1-2字
        - 重叠（如"特别"里的"别"）不算否定
        """
        SINGLE_NEG = {"不", "没", "非", "无", "别", "未", "莫", "勿"}
        for match in re.finditer(re.escape(word), text):
            word_start = match.start()
            word_end = match.end()
            for neg_start, neg_end in negated_ranges:
                neg_word_len = neg_end - neg_start
                neg_word = text[neg_start:neg_end]
                gap = word_start - neg_end
                
                # 单字否定词：必须位于独立位置（非合成词的一部分）
                if neg_word_len == 1 and neg_word in SINGLE_NEG:
                    # 独立否定：位置0，或前一个是标点/空格
                    is_independent = (neg_start == 0) or (
                        neg_start > 0 and text[neg_start - 1] in ' \t,，、'
                    )
                    if is_independent and neg_start < word_start and 0 <= gap <= 1:
                        return True
                # 复合否定词：gap 需 1-2
                elif neg_word_len > 1:
                    if neg_start < word_start and 1 <= gap <= 2:
                        return True
        return False
    
    def _detect_subtext(self, text: str) -> Dict:
        """潜台词检测（预编译正则）"""
        text_lower = text.lower()
        results = []
        
        for subtext_type, data in self.subtext_patterns.items():
            for compiled_pattern in data.get("compiled", []):
                match = compiled_pattern.search(text_lower)
                if match:
                    results.append({
                        "type": subtext_type,
                        "confidence": data["weight"],
                        "matched": match.group(),
                        "position": match.start()
                    })
        
        if not results:
            return {"type": "none", "confidence": 0.0, "matched": ""}
        
        results.sort(key=lambda x: x["confidence"], reverse=True)
        best = results[0]
        
        return {
            "type": best["type"],
            "confidence": best["confidence"],
            "matched": best["matched"]
        }
    
    def _calculate_emotion_score(
        self,
        text: str,
        keyword_results: Dict,
        punctuation_score: float,
        subtext_result: Dict
    ) -> float:
        """计算综合情绪强度"""
        keyword_score = min(keyword_results["total_score"] * 0.1, 0.5)
        
        base_scores = {
            "joy": 0.6, "excitement": 0.6, "love": 0.5, "hope": 0.4,
            "sadness": 0.5, "anger": 0.6, "fear": 0.5, "anxiety": 0.5,
            "frustration": 0.6, "loneliness": 0.5, "exhaustion": 0.4,
            "guilt": 0.4, "shame": 0.4, "disappointment": 0.5,
            "envy": 0.4, "disgust": 0.5, "surprise": 0.3,
            "gratitude": 0.3, "embarrassment": 0.3, "confusion": 0.2,
            "boredom": 0.2
        }
        
        matched_emotions = keyword_results["matched_emotions"]
        if matched_emotions:
            base_score = max(base_scores.get(m, 0.3) for m in matched_emotions)
        else:
            base_score = 0.1
        
        subtext_boost = 0.0
        if subtext_result["type"] == "hidden_pain":
            subtext_boost = 0.3
        elif subtext_result["type"] == "sarcasm":
            subtext_boost = 0.2
        elif subtext_result["type"] in ("frustration_mask", "masked_anger"):
            subtext_boost = 0.2
        
        total = base_score + keyword_score + punctuation_score + subtext_boost
        return min(max(total, 0.0), 1.0)
    
    def _determine_emotion_type(
        self,
        keyword_results: Dict,
        subtext_result: Dict
    ) -> str:
        """确定情绪类型"""
        matched_emotions = keyword_results["matched_emotions"]
        
        if not matched_emotions:
            if subtext_result["type"] == "hidden_pain":
                return "sadness"
            elif subtext_result["type"] == "sarcasm":
                return "anger"
            elif subtext_result["type"] == "frustration_mask":
                return "frustration"
            elif subtext_result["type"] == "masked_anger":
                return "anger"
            return "neutral"
        
        if len(matched_emotions) == 1:
            return matched_emotions[0]
        
        negative = ["sadness", "anger", "fear", "anxiety", "frustration",
                    "loneliness", "exhaustion", "disappointment", "disgust"]
        
        for emotion in negative:
            if emotion in matched_emotions:
                return emotion
        
        return matched_emotions[0]
    
    def _detect_mask(
        self,
        text: str,
        surface_type: str,
        subtext_result: Dict,
        keyword_results: Dict
    ) -> tuple:
        """检测情绪伪装"""
        subtext_type = subtext_result.get("type", "none")
        
        if subtext_type == "hidden_pain":
            return True, surface_type, "sadness"
        if subtext_type == "sarcasm":
            return True, surface_type, "anger"
        if subtext_type == "frustration_mask":
            return True, surface_type, "frustration"
        if subtext_type == "masked_anger":
            return True, surface_type, "anger"
        
        return False, surface_type, surface_type
    
    def _generate_notes(
        self,
        score: float,
        keyword_results: Dict,
        subtext_result: Dict
    ) -> str:
        """生成分析备注"""
        notes = []
        
        if keyword_results.get("is_swear"):
            ctx = keyword_results.get("sw_context_analysis", "")
            if ctx:
                return f"脏话检测 → 语境分析：{ctx}"
            return "脏话检测 → frustration（脏话语气，无明确负面指向）"
        
        if keyword_results.get("is_sarcasm"):
            notes.append("反讽检测 → 情绪已翻转")
        
        if score >= 0.8:
            notes.append("情绪非常强烈")
        elif score >= 0.6:
            notes.append("情绪明显")
        elif score >= 0.4:
            notes.append("情绪中等")
        elif score >= 0.2:
            notes.append("情绪轻微")
        else:
            notes.append("情绪平静")
        
        if keyword_results["matched_emotions"]:
            emotions_str = ", ".join(keyword_results["matched_emotions"][:3])
            notes.append(f"情绪类型：{emotions_str}")
        
        if keyword_results["matched_keywords"]:
            kws = ", ".join(keyword_results["matched_keywords"][:5])
            notes.append(f"命中：{kws}")
        
        neg_filtered = keyword_results.get("negation_filtered", [])
        if neg_filtered:
            notes.append(f"⚠️否定过滤：{', '.join(neg_filtered)}")
        
        if subtext_result["type"] != "none":
            notes.append(f"潜台词：{subtext_result['type']}({subtext_result['confidence']:.1f})")
        
        return "; ".join(notes)
    
    def detect_subtext(self, user_input: str) -> Dict:
        """单独检测潜台词（供外部调用）"""
        return self._detect_subtext(user_input)


# ============ 单例模式 ============
_detector_instance: Optional[EmotionDetector] = None

def get_instance() -> EmotionDetector:
    """获取 EmotionDetector 单例"""
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = EmotionDetector()
    return _detector_instance


def detect_emotion(user_input: str, context: Dict = None) -> EmotionOutput:
    """快捷情绪检测"""
    return get_instance().detect(user_input, context)

def detect_subtext(user_input: str) -> Dict:
    """快捷潜台词检测"""
    return get_instance().detect_subtext(user_input)


# ============ 测试 ============
if __name__ == "__main__":
    detector = EmotionDetector()
    
    test_cases = [
        ("今天太开心了！", "正常开心"),
        ("工作好累啊，老板又骂我了", "疲惫+挫败"),
        ("卧槽，这也太牛了吧！", "惊讶+兴奋"),
        ("算了，放弃吧", "绝望"),
        ("明天要面试了，好紧张", "焦虑"),
        ("你好", "中性"),
        ("谢谢你的帮助！", "感激"),
        ("其实我有点害怕...", "隐藏恐惧"),
        ("我开心你妈", "骂人+脏话 → anger"),
        ("傻逼东西", "纯骂人 → anger"),
        ("妈的，气死我了", "脏话+愤怒 → anger"),
        ("我靠，太牛了", "我靠+夸赞 → excitement"),
        ("其实我也没很开心", "否定开心 → sadness"),
        ("不，我不开心", "否定不开心 → joy"),
        ("我没事，真的没事...", "隐痛伪装 → sadness"),
        ("随便吧，无所谓", "挫败伪装 → frustration"),
        ("呵呵", "冷笑反讽 → anger"),
        ("你可真是聪明啊", "阴阳怪气 → anger"),
    ]
    
    print("=== 情绪检测测试 ===\n")
    for text, desc in test_cases:
        result = detector.detect(text)
        print(f"【{desc}】{text}")
        print(f"  情绪: {result.emotion_type} ({result.emotion_score:.2f})")
        print(f"  关键词: {result.keywords}")
        if result.is_masked:
            print(f"  ⚠️ 伪装: 表面={result.surface_emotion}, 底层={result.underlying_emotion}")
        if result.subtext != "none":
            print(f"  潜台词: {result.subtext} ({result.subtext_confidence:.1f})")
        print(f"  备注: {result.analysis_notes}")
        print()
