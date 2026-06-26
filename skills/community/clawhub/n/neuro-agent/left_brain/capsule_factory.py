"""
left_brain/capsule_factory.py
==============================

Neuro-Agent 左脑区 - 情绪胶囊工厂
负责：判断是否需要生成胶囊、创建胶囊、管理胶囊生命周期

依赖：
    - left_brain/emotion_detector.py
    - temporal/long_term_memory.py
    - temporal/short_term_memory.py
    - references/emotion_types.md
"""

import re
import hashlib
from datetime import datetime
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict

# ============ 胶囊类型判断规则 ============
CAPSULE_TYPE_PATTERNS = {
    "preference": {
        "keywords": [
            r"我喜欢", r"我喜欢吃", r"我爱", r"我偏好", r"我喜欢(\w+)",
            r"我比较喜欢", r"我比较(\w+)的", r"我想要", r"我想要(\w+)",
            r"我不喜欢", r"我不吃", r"我讨厌", r"我恨",
            r"我比较(喜欢|爱|想要|倾向)",
            r"一般般", r"凑合", r"都行", r"无所谓",
            r"最(喜欢|爱|想要|讨厌|恨|怕)",
        ],
        "weight": 1.0
    },
    "emotion": {
        "keywords": [
            r"我今天(很|好|太|特别)?(开心|高兴|快乐|难过|伤心|生气|愤怒|害怕|担心)",
            r"我(最近|现在|这会儿|此刻)(很|好|太|特别)?(开心|难过|焦虑|烦躁)",
            r"感觉(很|好|太)?(好|开心|难受|累|爽|激动)",
            r"我现在(开心|难过|兴奋|失落|激动|崩溃)",
            r"(\w+)死了",  # 累死了、开心死了
            r"好(开心|难过|激动|兴奋|难受|爽|嗨)",
        ],
        "weight": 0.9
    },
    "fact": {
        "keywords": [
            r"我住在", r"我在(北京|上海|深圳|广州|杭州)",
            r"我是(做)?(.+?)(的|工作|行业)", r"我在(.+?)(上班|工作)",
            r"我是(\w+)", r"我(\w+)了",  # 我毕业了、我跳槽了
            r"我(\w+)(年|岁)", r"我今年(\d+)",
            r"我有(.+?)年", r"我(.+?)年(.+?)经验",
            r"以前(做|是|在)", r"之前(.+?)工作",
            r"目前(.+?)工作", r"现在(.+?)做",
        ],
        "weight": 0.8
    },
    "secret": {
        "keywords": [
            r"其实我", r"其实(.+?)是", r"我其实",
            r"我不(想|好意思|敢)说",
            r"这事别", r"这个不要",
            r"我不想让", r"我没跟别人说",
            r"只有你知道", r"我只告诉你",
            r"我有个(.+?)秘密", r"秘密是",
            r"其实(.+?)有点", r"我有(.+?)点",
            r"坦白说", r"说真的",
        ],
        "weight": 0.9
    }
}

# 胶囊触发条件
CAPSULE_TRIGGER_PATTERNS = {
    "explicit_memory": {
        "keywords": [r"记住", r"记一下", r"帮我记", r"要记住", r"别忘了", r"这个很重要"],
        "score": 1.0
    },
    "explicit_forget": {
        "keywords": [r"忘了", r"忘掉", r"别记", r"不要记住", r"算了当我没说"],
        "score": -1.0  # 负分，不创建
    },
    "self_disclosure": {
        "keywords": [
            r"^我",  # 以"我"开头的句子
            r"跟你说", r"告诉你", r"跟你说个",
            r"我跟你说", r"悄悄告诉你",
            r"其实", r"坦白", r"说真的",
        ],
        "score": 0.7
    },
    "preference_explicit": {
        "keywords": [r"我喜欢", r"我想要", r"我不喜欢", r"我讨厌", r"我的"],
        "score": 0.8
    },
    "emotion_explicit": {
        "keywords": [
            r"我今天", r"我现在", r"我最近", r"我(很|好|太|特别)",
            r"感觉(很|好)", r"(\w+)死了", r"(\w+)透了"
        ],
        "score": 0.6
    },
    "milestone": {
        "keywords": [
            r"生日", r"纪念日", r"今天是我", r"今天是(.+?)的生日",
            r"(\d+)周年", r"认识(\d+)年", r"在一起(\d+)",
        ],
        "score": 1.0
    }
}

# 敏感度检测
SENSITIVITY_PATTERNS = {
    "critical": {
        "keywords": [
            r"秘密", r"不能说的", r"只有你知道", r"保密",
            r"这个秘密", r"我最大的", r"我的(.+?)秘密",
            r"我从来没跟别人说", r"这是我(.+?)秘密",
        ],
        "weight": 1.0
    },
    "high": {
        "keywords": [
            r"其实", r"不过", r"只是", r"我不(想|好意思|敢)",
            r"有点(难过|害怕|担心|不好意思|后悔|内疚)",
            r"我只是", r"我没跟别人说过",
            r"不想让别人知道", r"不想让人知道",
            r"我(.+?)不太好意思", r"有点(.+?)不(好意思|想说)",
        ],
        "weight": 0.8
    }
}


# ============ 数据结构 ============
@dataclass
class CapsuleOutput:
    """
    胶囊工厂输出
    
    属性：
        - should_capsule: 是否应该创建胶囊
        - capsules: 生成的胶囊列表
        - capsule_reasons: 每个胶囊的创建原因
        - skip_reason: 如果不创建，说明原因
        - confidence: 判断置信度
    """
    should_capsule: bool
    capsules: List[Any]  # List[EmotionCapsule]
    capsule_reasons: List[str]
    skip_reason: str
    confidence: float
    
    def to_dict(self) -> Dict:
        return asdict(self)


# ============ 核心类 ============
class CapsuleFactory:
    """
    情绪胶囊工厂
    
    功能：
        - 判断是否需要创建胶囊
        - 创建胶囊
        - 判断胶囊类型
        - 判断敏感度
        - 生成胶囊摘要
        - 管理胶囊生命周期
    
    创建条件（满足其一）：
        1. 高情绪强度：emotion_score >= 0.7
        2. 自我暴露：包含"我..."开头的重要陈述
        3. 偏好表达："我喜欢/讨厌/想要/不要..."
        4. 矛盾修正："我不吃辣了"、"其实..."
        5. 特殊指令："记住这个"、"忘了吧"
        6. 里程碑事件：生日/纪念日/重大事件
    """
    
    def __init__(self):
        """初始化胶囊工厂"""
        self.type_patterns = CAPSULE_TYPE_PATTERNS
        self.trigger_patterns = CAPSULE_TRIGGER_PATTERNS
        self.sensitivity_patterns = SENSITIVITY_PATTERNS
        self._compile_patterns()
    
    def _compile_patterns(self):
        """预编译正则表达式"""
        for category in [self.type_patterns, self.trigger_patterns, self.sensitivity_patterns]:
            for key, data in category.items():
                if isinstance(data, dict) and "keywords" in data:
                    data["compiled"] = [
                        re.compile(kw, re.IGNORECASE) 
                        for kw in data["keywords"]
                    ]
    
    def should_create_capsule(
        self, 
        user_input: str, 
        emotion_output
    ) -> tuple:
        """
        判断是否应该创建胶囊
        
        参数:
            user_input: 用户输入
            emotion_output: EmotionOutput
        
        返回:
            (should_create: bool, score: float, reasons: List[str])
        """
        if not user_input or not user_input.strip():
            return False, 0.0, ["空输入"]
        
        text = user_input.strip()
        score = 0.0
        reasons = []
        
        # 1. 情绪强度检查
        emotion_score = getattr(emotion_output, "emotion_score", 0.0)
        if emotion_score >= 0.8:
            score += 0.4
            reasons.append(f"情绪强度高({emotion_score:.1f})")
        elif emotion_score >= 0.7:
            score += 0.3
            reasons.append(f"情绪强度中高({emotion_score:.1f})")
        elif emotion_score >= 0.5:
            score += 0.1
            reasons.append(f"情绪强度中({emotion_score:.1f})")
        
        # 2. 明确指令检查
        for key, data in self.trigger_patterns.items():
            for compiled in data.get("compiled", []):
                if compiled.search(text):
                    score += data["score"]
                    if data["score"] > 0:
                        reasons.append(f"触发词: {key}")
                    else:
                        reasons.append(f"跳过原因: {key}")
                    break
        
        # 3. 自我暴露检查
        if text.startswith("我") or "我" in text[:10]:
            # 检查是否在谈论自己
            if any(kw in text for kw in ["喜欢", "讨厌", "想要", "觉得", "感觉", "是", "住在", "工作", "做"]):
                score += 0.3
                reasons.append("自我暴露")
        
        # 4. 矛盾修正检查
        if any(kw in text for kw in ["其实", "不过", "但是", "算了", "不是", "不再", "以后不", "改"]):
            if any(kw in text for kw in ["不", "别", "没", "不再"]):
                score += 0.2
                reasons.append("矛盾修正")
        
        # 5. 里程碑检查
        milestone_keywords = ["生日", "纪念日", "周年", "认识", "在一起"]
        if any(kw in text for kw in milestone_keywords):
            score += 0.5
            reasons.append("里程碑事件")
        
        # 最终判断
        should_create = score >= 0.5
        
        # 负面条件
        if "忘掉" in text or "别记" in text or "不要记住" in text:
            should_create = False
            reasons.append("明确要求遗忘")
        
        return should_create, score, reasons
    
    def create_capsule(
        self,
        user_input: str,
        emotion_output,
        context: Dict = None
    ) -> Any:
        """
        创建情绪胶囊
        
        参数:
            user_input: 用户输入
            emotion_output: EmotionOutput
            context: 额外上下文
        
        返回:
            EmotionCapsule 或 None
        """
        context = context or {}
        
        # 判断是否应该创建
        should_create, score, reasons = self.should_create_capsule(
            user_input, emotion_output
        )
        
        if not should_create:
            return None
        
        # 判断类型
        capsule_type = self.determine_type(user_input)
        
        # 判断敏感度
        sensitivity = self.determine_sensitivity(user_input, emotion_output)
        
        # 生成摘要
        summary = self.generate_summary(user_input, capsule_type, emotion_output)
        
        # 创建胶囊
        from temporal.long_term_memory import EmotionCapsule
        
        capsule_id = self._generate_id(user_input)
        now = datetime.now()
        
        capsule = EmotionCapsule(
            id=capsule_id,
            timestamp=now.isoformat(),
            type=capsule_type,
            content={
                "summary": summary,
                "original_trigger": user_input,
                "detail": self.extract_detail(user_input, capsule_type)
            },
            emotion={
                "label": emotion_output.emotion_type,
                "intensity": emotion_output.emotion_score
            },
            tags=self.extract_tags(user_input, emotion_output),
            decay_rate=0.0,  # 会在 long_term_memory 中计算
            access_count=0,
            memory_strength=1.0,
            is_dormant=False,
            sensitivity=sensitivity,
            last_accessed=now.isoformat()
        )
        
        return capsule
    
    def determine_type(self, user_input: str) -> str:
        """
        判断胶囊类型
        
        优先级：preference > emotion > fact > secret
        """
        text = user_input.strip()
        
        scores = {}
        
        for capsule_type, data in self.type_patterns.items():
            score = 0.0
            for compiled in data.get("compiled", []):
                if compiled.search(text):
                    score += data["weight"]
            
            if score > 0:
                scores[capsule_type] = score
        
        if not scores:
            return "fact"  # 默认类型
        
        # 返回得分最高的
        return max(scores.items(), key=lambda x: x[1])[0]
    
    def determine_sensitivity(
        self, 
        user_input: str, 
        emotion_output
    ) -> str:
        """
        判断敏感度
        
        规则：
            - normal：普通偏好、事实
            - high：个人伤痛、敏感话题
            - critical：核心秘密
        """
        text = user_input.strip()
        
        # 检查 critical 关键词
        for compiled in self.sensitivity_patterns["critical"].get("compiled", []):
            if compiled.search(text):
                return "critical"
        
        # 检查 high 关键词
        for compiled in self.sensitivity_patterns["high"].get("compiled", []):
            if compiled.search(text):
                return "high"
        
        # 情绪强度高但不是 critical
        emotion_score = getattr(emotion_output, "emotion_score", 0.0)
        if emotion_score >= 0.8:
            emotion_type = getattr(emotion_output, "emotion_type", "")
            if emotion_type in ["sadness", "fear", "guilt", "shame", "hidden_pain"]:
                return "high"
        
        return "normal"
    
    def generate_summary(
        self, 
        user_input: str, 
        capsule_type: str,
        emotion_output
    ) -> str:
        """
        生成胶囊摘要
        
        规则：
            - preference：提取偏好内容
            - emotion：提取情绪事件
            - fact：提取事实信息
            - secret：保持原意，模糊处理
        """
        text = user_input.strip()
        
        if capsule_type == "preference":
            # 提取偏好
            preference_kw = ["喜欢", "讨厌", "想要", "爱", "偏好", "倾向"]
            for kw in preference_kw:
                if kw in text:
                    # 找到关键词后的内容
                    idx = text.index(kw)
                    summary = text[idx:].strip()
                    if len(summary) > 2:
                        return summary[:50]  # 截断
            return f"偏好: {text[:30]}..."
        
        elif capsule_type == "emotion":
            # 提取情绪
            return f"情绪: {text[:40]}..."
        
        elif capsule_type == "secret":
            # 模糊处理，保护隐私
            return f"秘密: {text[:20]}..."
        
        else:
            return text[:50]
    
    def extract_detail(
        self, 
        user_input: str, 
        capsule_type: str
    ) -> str:
        """提取详细内容"""
        text = user_input.strip()
        
        # 简单处理：保留原始内容
        if len(text) <= 200:
            return text
        else:
            return text[:200] + "..."
    
    def extract_tags(
        self, 
        user_input: str, 
        emotion_output
    ) -> List[str]:
        """提取标签"""
        tags = []
        text = user_input.strip()
        
        # 基于情绪类型添加标签
        emotion_type = getattr(emotion_output, "emotion_type", "neutral")
        tags.append(emotion_type)
        
        # 基于内容添加标签
        tag_keywords = {
            "工作": ["工作", "上班", "老板", "同事", "公司", "面试", "求职"],
            "生活": ["生活", "日常", "家里", "家里", "做饭", "家务"],
            "情感": ["感情", "恋爱", "男/女", "朋友", "家人", "约会"],
            "健康": ["健康", "身体", "运动", "减肥", "生病"],
            "学习": ["学习", "考试", "读书", "课程"],
            "娱乐": ["电影", "游戏", "音乐", "旅游", "逛街"],
            "财务": ["钱", "理财", "投资", "买房"],
            "科技": ["手机", "电脑", "app", "ai", "技术"]
        }
        
        for tag, keywords in tag_keywords.items():
            if any(kw in text for kw in keywords):
                tags.append(tag)
                break
        
        # 基于情绪关键词添加标签
        if emotion_type == "joy":
            tags.append("正面情绪")
        elif emotion_type in ["sadness", "anger", "fear", "anxiety", "frustration"]:
            tags.append("负面情绪")
        
        return list(set(tags))[:5]  # 去重，最多5个
    
    def _generate_id(self, user_input: str) -> str:
        """生成胶囊ID"""
        timestamp = datetime.now().timestamp()
        content_hash = hashlib.md5(user_input.encode()).hexdigest()[:8]
        return f"capsule_{int(timestamp)}_{content_hash}"
    
    def create_multiple(
        self,
        user_input: str,
        emotion_output,
        context: Dict = None
    ) -> CapsuleOutput:
        """
        创建多个胶囊（如果有多个可提取的信息）
        
        返回:
            CapsuleOutput
        """
        capsule = self.create_capsule(user_input, emotion_output, context)
        
        if capsule:
            should_create, score, reasons = self.should_create_capsule(
                user_input, emotion_output
            )
            return CapsuleOutput(
                should_capsule=True,
                capsules=[capsule],
                capsule_reasons=reasons,
                skip_reason="",
                confidence=min(score, 1.0)
            )
        else:
            _, _, reasons = self.should_create_capsule(user_input, emotion_output)
            return CapsuleOutput(
                should_capsule=False,
                capsules=[],
                capsule_reasons=[],
                skip_reason="; ".join(reasons) if reasons else "未达到创建条件",
                confidence=0.0
            )


# ============ 单例模式 ============
_factory_instance: Optional[CapsuleFactory] = None

def get_instance() -> CapsuleFactory:
    """获取 CapsuleFactory 单例"""
    global _factory_instance
    if _factory_instance is None:
        _factory_instance = CapsuleFactory()
    return _factory_instance


# ============ 快捷函数 ============
def should_create_capsule(user_input: str, emotion_output) -> tuple:
    """快捷判断是否创建胶囊"""
    return get_instance().should_create_capsule(user_input, emotion_output)

def create_capsule(
    user_input: str,
    emotion_output,
    context: Dict = None
):
    """快捷创建胶囊"""
    return get_instance().create_capsule(user_input, emotion_output, context)


# ============ 测试 ============
if __name__ == "__main__":
    from dataclasses import dataclass
    from typing import List
    
    @dataclass
    class MockEmotionOutput:
        emotion_score: float
        emotion_type: str
        keywords: List[str]
        subtext: str
    
    factory = CapsuleFactory()
    
    test_cases = [
        ("我喜欢吃辣，越辣越开心！", MockEmotionOutput(0.6, "joy", ["喜欢", "辣"], "none")),
        ("其实我有点害怕一个人...", MockEmotionOutput(0.5, "fear", ["害怕"], "hidden_pain")),
        ("我住在上海，做电商运营", MockEmotionOutput(0.2, "neutral", [], "none")),
        ("记住，我最讨厌被放鸽子", MockEmotionOutput(0.4, "anger", ["讨厌"], "none")),
        ("今天工作好累啊，老板又骂我了", MockEmotionOutput(0.7, "sadness", ["累", "累"], "none")),
        ("算了忘了吧，当我没说", MockEmotionOutput(0.3, "neutral", [], "none")),
        ("其实我最近有点迷茫...", MockEmotionOutput(0.6, "anxiety", ["迷茫"], "hidden_pain")),
        ("我喜欢跑步，特别是早上", MockEmotionOutput(0.4, "joy", ["喜欢", "跑步"], "none")),
    ]
    
    print("=== 胶囊工厂测试 ===\n")
    for text, emotion in test_cases:
        should_create, score, reasons = factory.should_create_capsule(text, emotion)
        capsule_type = factory.determine_type(text)
        sensitivity = factory.determine_sensitivity(text, emotion)
        
        print(f"【{text}】")
        print(f"  情绪: {emotion.emotion_type} ({emotion.emotion_score:.1f})")
        print(f"  类型: {capsule_type}, 敏感度: {sensitivity}")
        print(f"  应创建: {should_create} (得分: {score:.2f})")
        print(f"  原因: {reasons}")
        
        if should_create:
            capsule = factory.create_capsule(text, emotion)
            if capsule:
                print(f"  胶囊ID: {capsule.id}")
                print(f"  摘要: {capsule.content['summary']}")
                print(f"  标签: {capsule.tags}")
        
        print()
