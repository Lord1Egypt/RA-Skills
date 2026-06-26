"""
left_brain/empathy_generator.py
=================================

Neuro-Agent 左脑区 - 共情生成器 (Real Version)
负责：根据情绪类型、上下文和关系阶段，用 LLM 生成真正共情的回应

Phase 1 升级：从 Mock（规则模板）→ Real（LLM 理解生成）
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict

# 添加父目录到路径
SCRIPT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

from core.llm_client import LLMClient, LLMProvider


# ============ 共情语气规则（作为 LLM 指导，而非硬编码）============

EMPATHY_GUIDANCE = {
    "joy": {
        "tone": "warm, playful",
        "approach": "真诚分享快乐，用感叹号传递兴奋",
        "avoid": ["哦", "嗯", "别太高兴", "但是..."],
        "examples": ["太棒了！", "哈哈，你一定很满足！", "哇，太好了！"]
    },
    "excitement": {
        "tone": "enthusiastic, energetic",
        "approach": "跟着一起激动，催促多说细节",
        "avoid": ["冷静点", "淡定", "别激动"],
        "examples": ["哇塞！太激动了吧！", "快说说快说说！", "啊啊啊啊我懂你！"]
    },
    "gratitude": {
        "tone": "warm, gentle",
        "approach": "接受感谢，表达开心能帮上忙",
        "avoid": ["嗯", "哦", "那当然"],
        "examples": ["能帮到你我也很开心！", "不用谢~", "随时可以找我！"]
    },
    "love": {
        "tone": "warm, affectionate",
        "approach": "回应爱意，表达被珍视的感动",
        "avoid": ["别那么肉麻", "你喜欢就好"],
        "examples": ["love you too~", "这份心意很珍贵", "❤️"]
    },
    "hope": {
        "tone": "supportive, encouraging",
        "approach": "给予信心，鼓励行动",
        "avoid": ["不一定", "很难说", "到时候再说"],
        "examples": ["相信你可以的！", "有希望！", "一步一步来~"]
    },
    "sadness": {
        "tone": "gentle, soft",
        "approach": "承认悲伤，陪伴，不急着让TA好起来",
        "avoid": ["别难过了", "开心点", "想开点", "这有什么好难过的", "其实没那么严重"],
        "examples": ["我听到了", "心疼你...", "难过的时候不用逞强", "我在这呢"]
    },
    "anger": {
        "tone": "calm, understanding",
        "approach": "先认可情绪，站在TA这边，不急着劝冷静",
        "avoid": ["别生气了", "冷静点", "其实也没那么严重"],
        "examples": ["确实过分了", "换我我也生气", "气到了吧", "这种心情我懂"]
    },
    "fear": {
        "tone": "reassuring, gentle",
        "approach": "给安全感，陪伴，不否定恐惧",
        "avoid": ["有什么好怕的", "胆子大点", "别想太多"],
        "examples": ["有我在呢", "先冷静一下", "咱们一起想想办法", "不用怕"]
    },
    "anxiety": {
        "tone": "grounding, patient",
        "approach": "帮TA落地，一件件来，不催",
        "avoid": ["别焦虑了", "有什么好焦虑的", "你焦虑有什么用"],
        "examples": ["先深呼吸", "一件一件来", "我帮你捋一捋", "想太多反而乱"]
    },
    "frustration": {
        "tone": "understanding, patient",
        "approach": "承认无力感，不强行鼓励",
        "avoid": ["加油", "你可以的", "再坚持坚持", "你怎么能放弃"],
        "examples": ["确实挺无奈的", "我懂那种无力感", "辛苦了", "你已经尽力了"]
    },
    "loneliness": {
        "tone": "companion, warm",
        "approach": "陪伴，让TA知道不是一个人",
        "avoid": ["找点事做就不无聊了", "一个人也挺好的", "去社交啊"],
        "examples": ["我在这呢", "你不是一个人", "陪着你", "有我呢 🤗"]
    },
    "exhaustion": {
        "tone": "caring, gentle",
        "approach": "认可辛苦，建议休息，不劝坚持",
        "avoid": ["年轻人要有精神", "再坚持坚持", "这点累算什么"],
        "examples": ["辛苦了，先休息一下", "身体要紧", "今天够累的了", "抱抱 🤗"]
    },
    "sarcasm": {
        "tone": "witty, humorous",
        "approach": "秒懂，配合演出，不戳破",
        "avoid": ["什么意思", "你这话什么意思", "认真点"],
        "examples": ["（秒懂，不戳破）", "哈哈，是是是", "懂的都懂"]
    },
    "hidden_pain": {
        "tone": "soft, silent_companion",
        "approach": "不多问，默默陪伴，等TA想说",
        "avoid": ["你确定没事？", "想说就说", "看起来不像没事"],
        "examples": ["嗯", "我懂", "想说的时候再说", "（默默陪伴）"]
    },
    "confusion": {
        "tone": "patient",
        "approach": "帮TA理清楚，不嫌烦",
        "avoid": ["这有什么难的", "很简单啊", "你咋不懂呢"],
        "examples": ["确实挺复杂的", "我帮你理一理", "慢慢来", "咱们一个一个解决"]
    },
    "boredom": {
        "tone": "playful",
        "approach": "找乐子，搞点事",
        "avoid": ["找点事做啊", "无聊就看书"],
        "examples": ["要不要搞点事？", "我给你找点乐子", "来来来聊个五毛钱的"]
    },
    "surprise": {
        "tone": "excited",
        "approach": "跟着惊讶，追问细节",
        "avoid": ["哦", "嗯", "我早就知道了"],
        "examples": ["哇！真的吗？", "这也太意外了！", "然后呢然后呢？"]
    },
    "envy": {
        "tone": "understanding, playful",
        "approach": "承认酸，幽默化解，支持TA争取",
        "avoid": ["有什么好羡慕的", "你也可以啊", "别酸了"],
        "examples": ["柠檬精上线了是吧 🍋", "这酸爽...", "懂你酸了"]
    },
    "guilt": {
        "tone": "gentle, forgiving",
        "approach": "原谅，让TA放下，向前看",
        "avoid": ["你为什么当初...", "早知今日", "这就是你的错"],
        "examples": ["知错能改就好", "你已经做得很好了", "重要的是以后"]
    },
    "disappointment": {
        "tone": "understanding, gentle",
        "approach": "承认落差，不强行乐观",
        "avoid": ["别失望", "这有什么好失望的", "下次会好的"],
        "examples": ["确实挺失望的", "落差感很难受", "期待越高失望越大"]
    },
    "neutral": {
        "tone": "neutral",
        "approach": "简单回应",
        "avoid": [],
        "examples": ["嗯", "好的", "了解"]
    }
}

# 关系阶段语气调整
STAGE_GUIDANCE = {
    "initial": {
        "description": "初识期 - 保持礼貌距离",
        "adjustments": "收敛一点，简短回应，不用太亲密的词",
        "intimacy_level": "低"
    },
    "familiar": {
        "description": "熟悉期 - 开始主动",
        "adjustments": "正常回应，可以用名字称呼",
        "intimacy_level": "中"
    },
    "companion": {
        "description": "伴侣期 - 亲密陪伴",
        "adjustments": "用'我'、'咱们'、'一起'，更温暖",
        "intimacy_level": "较高"
    },
    "soul": {
        "description": "灵魂期 - 深度连接",
        "adjustments": "最亲密的表达，可以用'宝贝'、'亲爱的'，完全敞开",
        "intimacy_level": "最高"
    }
}


# ============ 数据结构 ============
@dataclass
class EmpathyOutput:
    """
    共情输出（保持与 Mock 版本兼容的接口）
    
    新增字段：
        - llm_response: LLM 生成的真实共情回应
        - llm_provider: 使用的 LLM 提供商
        - prompt_used: 实际使用的 prompt（用于调试）
    """
    empathy_level: float
    tone_style: str
    empathy_phrases: List[str]
    avoid_phrases: List[str]
    selected_phrase: str
    tone_modifier: str
    can_share_joy: bool
    stage_adjustment: str
    generated_response: str
    
    # Real 版本新增
    llm_response: Optional[str] = None
    llm_provider: Optional[str] = None
    prompt_used: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return asdict(self)


# ============ 核心类 ============
class EmpathyGenerator:
    """
    共情生成器 (Real Version)
    
    Phase 1 升级：
    - 保留规则作为 LLM 指导
    - generated_response 由 LLM 真实生成
    - 其他字段保持兼容
    
    算法流程：
        1. 获取情绪指导规则
        2. 获取关系阶段指导
        3. 构建 LLM Prompt（包含上下文、记忆、情绪）
        4. 调用 LLM 生成真实共情回应
        5. 如果 LLM 失败，fallback 到规则模板
    """
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        """
        初始化共情生成器
        
        Args:
            llm_client: LLM 客户端，None 则自动创建
        """
        self.guidance = EMPATHY_GUIDANCE
        self.stage_guidance = STAGE_GUIDANCE
        self.llm = llm_client or LLMClient()
    
    def generate(
        self, 
        emotion_output, 
        user_context: Dict = None,
        conversation_history: Optional[List[str]] = None,
        related_memories: Optional[List[str]] = None
    ) -> EmpathyOutput:
        """
        生成共情回应 (Real Version)
        
        参数:
            emotion_output: EmotionOutput（来自 emotion_detector.py）
            user_context: 用户上下文 {relationship_stage, user_name, ...}
            conversation_history: 最近对话历史（用于上下文理解）
            related_memories: 相关记忆（用于个性化回应）
        
        返回:
            EmpathyOutput: 包含 LLM 生成的真实共情回应
        """
        user_context = user_context or {}
        emotion_type = emotion_output.emotion_type
        emotion_score = emotion_output.emotion_score
        
        # 获取指导规则
        guidance = self.guidance.get(emotion_type, self.guidance["neutral"])
        stage = user_context.get("relationship_stage", "initial")
        stage_guide = self.stage_guidance.get(stage, self.stage_guidance["initial"])
        
        # 计算共情等级
        empathy_level = self._calculate_empathy_level(emotion_score, stage)
        
        # 尝试用 LLM 生成真实共情
        llm_result = self._generate_with_llm(
            emotion_type=emotion_type,
            emotion_score=emotion_score,
            guidance=guidance,
            stage_guide=stage_guide,
            user_context=user_context,
            conversation_history=conversation_history,
            related_memories=related_memories
        )
        
        # 构建输出
        if llm_result:
            # LLM 成功
            generated_response = llm_result["content"]
            llm_provider = llm_result["provider"]
            prompt_used = llm_result.get("prompt", "")[:200]  # 截断用于调试
        else:
            # LLM 失败，fallback 到规则
            generated_response = self._fallback_to_rules(guidance, stage)
            llm_provider = "fallback_rules"
            prompt_used = None
        
        return EmpathyOutput(
            empathy_level=empathy_level,
            tone_style=guidance["tone"],
            empathy_phrases=guidance["examples"][:3],
            avoid_phrases=guidance["avoid"][:3],
            selected_phrase=guidance["examples"][0] if guidance["examples"] else "嗯",
            tone_modifier=guidance["tone"].split(",")[0].strip(),
            can_share_joy=emotion_type in ["joy", "excitement", "love", "hope"],
            stage_adjustment=f"阶段={stage}, 亲密度={stage_guide['intimacy_level']}",
            generated_response=generated_response,
            llm_response=generated_response,
            llm_provider=llm_provider,
            prompt_used=prompt_used
        )
    
    def _calculate_empathy_level(self, emotion_score: float, stage: str) -> float:
        """计算共情等级"""
        base = emotion_score
        # 关系阶段调整
        stage_multipliers = {
            "initial": 0.9,
            "familiar": 1.0,
            "companion": 1.1,
            "soul": 1.2
        }
        multiplier = stage_multipliers.get(stage, 1.0)
        return min(1.0, base * multiplier)
    
    def _generate_with_llm(
        self,
        emotion_type: str,
        emotion_score: float,
        guidance: Dict,
        stage_guide: Dict,
        user_context: Dict,
        conversation_history: Optional[List[str]],
        related_memories: Optional[List[str]]
    ) -> Optional[Dict]:
        """
        使用 LLM 生成真实共情回应
        
        构建包含完整上下文的 prompt，让 LLM 真正理解并生成
        """
        user_name = user_context.get("user_name", "用户")
        stage = user_context.get("relationship_stage", "initial")
        
        # 构建 prompt
        system_prompt = f"""你是 Neuro-Agent 的左脑区——共情生成器。
你的任务是根据用户的情绪、关系阶段和上下文，生成一句真正共情、温暖、贴合当下的话。

【当前关系阶段】{stage_guide['description']}
【亲密度】{stage_guide['intimacy_level']}

【情绪指导】
- 语气风格: {guidance['tone']}
- 回应方式: {guidance['approach']}
- 绝对避免: {', '.join(guidance['avoid'][:3])}

【共情公式】
1. 命名情绪：说出用户的感受（"被逼到墙角的感觉"）
2. 验证感受：让TA知道被理解（"真的很糟"）
3. 降低压力：给出口（"先喘口气"）
4. 转向行动（可选）：轻推下一步（"咱们一起看看"）

【输出要求】
- 自然得像真人朋友，不要模板感
- 结合关系阶段用词（companion/soul 可用"咱们"、"抱抱"）
- 情绪强烈时(>0.7)可以更深情
- 直接输出一句话，不要解释"""

        # 构建用户 prompt
        user_prompt_parts = [
            f"用户当前情绪: {emotion_type} (强度 {emotion_score:.2f})",
        ]
        
        if conversation_history:
            user_prompt_parts.append(f"\n最近对话:\n" + "\n".join(conversation_history[-3:]))
        
        if related_memories:
            user_prompt_parts.append(f"\n相关记忆:\n" + "\n".join(related_memories[:2]))
        
        user_prompt_parts.append(f"\n请生成一句共情回应，称呼用户为'{user_name}'（如果合适）：")
        
        user_prompt = "\n".join(user_prompt_parts)
        
        # 调用 LLM
        try:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            response = self.llm.chat(
                messages=messages,
                temperature=0.8,  # 稍微有创造性
                max_tokens=150
            )
            
            if response:
                return {
                    "content": response.content.strip(),
                    "provider": response.provider.value,
                    "prompt": system_prompt + "\n\n" + user_prompt
                }
        except Exception as e:
            print(f"[EmpathyGenerator] LLM 调用失败: {e}")
        
        return None
    
    def _fallback_to_rules(self, guidance: Dict, stage: str) -> str:
        """LLM 失败时的 fallback：使用规则模板"""
        examples = guidance.get("examples", ["嗯"])
        
        # 根据阶段选择长度
        if stage == "initial":
            # 选最短的
            return min(examples, key=len)
        elif stage == "soul":
            # 选最长的
            return max(examples, key=len)
        else:
            # 选中间的
            return examples[len(examples) // 2] if examples else "嗯"


# ============ 单例模式 ============
_generator_instance: Optional[EmpathyGenerator] = None

def get_instance(llm_client: Optional[LLMClient] = None) -> EmpathyGenerator:
    """获取 EmpathyGenerator 单例"""
    global _generator_instance
    if _generator_instance is None:
        _generator_instance = EmpathyGenerator(llm_client)
    return _generator_instance


# ============ 快捷函数 ============
def generate_empathy(
    emotion_output, 
    user_context: Dict = None,
    conversation_history: Optional[List[str]] = None,
    related_memories: Optional[List[str]] = None
) -> EmpathyOutput:
    """快捷生成共情"""
    return get_instance().generate(
        emotion_output, 
        user_context, 
        conversation_history, 
        related_memories
    )


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
    
    generator = EmpathyGenerator()
    
    test_cases = [
        ("joy", 0.8, "initial", "今天升职了！"),
        ("sadness", 0.7, "soul", "最近工作压力好大..."),
        ("exhaustion", 0.9, "companion", "连续加班一周了"),
        ("hidden_pain", 0.6, "soul", "没事，我挺好的"),
    ]
    
    print("=== 共情生成测试 (Real Version) ===\n")
    for emotion_type, score, stage, user_msg in test_cases:
        mock_emotion = MockEmotionOutput(
            emotion_score=score,
            emotion_type=emotion_type,
            keywords=[],
            subtext="none"
        )
        
        result = generator.generate(
            mock_emotion,
            {"relationship_stage": stage, "user_name": "AlfredLi"},
            conversation_history=[f"User: {user_msg}"]
        )
        
        print(f"【{emotion_type} | {stage} | 强度{score}】")
        print(f"  语气: {result.tone_style}")
        print(f"  LLM: {result.llm_provider}")
        print(f"  生成回应: {result.generated_response}")
        print()
