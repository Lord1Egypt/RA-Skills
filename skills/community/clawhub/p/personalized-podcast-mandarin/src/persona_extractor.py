# -*- coding: utf-8 -*-
"""
Persona提取器
从用户材料中提取三层Persona：Identity / Expression / Memory
"""

import json
from typing import Dict, Any, Optional, List
from pathlib import Path
from pydantic import BaseModel, Field

from src.volcano_client_requests import create_ark_client_requests
from src.voice_selector import VoiceSelector


class MemorySeed(BaseModel):
    """记忆种子结构"""
    title: str = Field(default="", description="记忆标题")
    content: str = Field(default="", description="记忆内容")
    tags: List[str] = Field(default_factory=list, description="标签")


class Identity(BaseModel):
    """身份层结构"""
    name: str = Field(default="", description="人物名称")
    archetype: str = Field(default="观察者", description="原型角色")
    core_drive: str = Field(default="", description="核心驱动力")
    chemistry: str = Field(default="", description="互动风格")


class Expression(BaseModel):
    """表达层结构"""
    pace: str = Field(default="normal", description="语速")
    sentence_length: str = Field(default="mixed", description="句子长度")
    signature_phrases: List[str] = Field(default_factory=list, description="标志性口头禅")
    attitude: str = Field(default="curious", description="态度")
    voice_id: str = Field(default="", description="音色ID")


class PersonaStructure(BaseModel):
    """完整Persona结构"""
    identity: Identity = Field(default_factory=Identity)
    expression: Expression = Field(default_factory=Expression)
    memory_seed: List[MemorySeed] = Field(default_factory=list, description="记忆种子列表")


class PersonaExtractor:
    """Persona提取器"""

    def __init__(self, api_key: Optional[str] = None, gender: str = "female", skip_client_init: bool = False):
        self.gender = gender
        if not skip_client_init:
            self.client = create_ark_client_requests(api_key=api_key)
        else:
            self.client = None
        self._load_prompt()

    def _load_prompt(self):
        """加载提取Prompt，并注入音色列表"""
        prompt_path = Path(__file__).parent.parent / "agents" / "persona-extractor.md"
        with open(prompt_path, "r", encoding="utf-8") as f:
            prompt_template = f.read()

        # 加载音色列表并生成选择指南
        voice_selector = VoiceSelector()
        voice_list_text = voice_selector.build_selection_prompt(
            gender=self.gender,
            max_voices=20
        )

        # 替换占位符
        self.extract_prompt = prompt_template.replace("{{VOICE_LIST}}", voice_list_text)

    def extract(self, text: str, user_hint: str = "", raise_on_error: bool = True, gender: Optional[str] = None) -> Dict[str, Any]:
        """
        从文本材料提取Persona

        Args:
            text: 用户提供的材料（文章/播客转录等）
            user_hint: 用户的补充说明（如"像李诞那样"）
            raise_on_error: 失败时是否抛出异常（默认True，测试时可设为False返回空结构）
            gender: 性别（"male"或"female"），用于选择合适音色，默认使用初始化时的gender

        Returns:
            三层Persona字典

        Raises:
            RuntimeError: 当API调用失败且 raise_on_error=True 时
            ValueError: 当返回结果格式异常时
        """
        # 如果指定了gender且与当前不同，需要重新加载prompt
        if gender and gender != self.gender:
            self.gender = gender
            self._load_prompt()
        # 截断文本避免超限
        text_truncated = text[:8000] if len(text) > 8000 else text

        # 构建输入
        input_content = f"""请从以下材料提取Persona：

【用户补充说明】
{user_hint if user_hint else "无"}

【材料内容】
{text_truncated}

请严格按照输出格式要求提取，只输出JSON，不要其他解释。"""

        # 调用LLM提取
        try:
            result, _ = self.client.chat_completion(
                system_prompt=self.extract_prompt,
                user_message=input_content,
                output_schema=PersonaStructure,
                temperature=0.5,  # 低温度确保稳定提取
                max_tokens=2048
            )

            # 解析结果 - 使用Pydantic模型
            if hasattr(result, 'model_dump'):
                persona = result.model_dump()
            elif isinstance(result, dict):
                persona = result
            elif isinstance(result, str):
                persona = json.loads(result)
            else:
                raise ValueError(f"Unexpected result type: {type(result)}")

            return self._validate_and_clean(persona)

        except Exception as e:
            # 记录详细错误信息
            import traceback
            error_msg = f"Persona提取失败: {type(e).__name__}: {e}"
            print(f"[ERROR] {error_msg}")
            print(f"[DEBUG] 详细堆栈:\n{traceback.format_exc()}")

            if raise_on_error:
                raise RuntimeError(error_msg) from e
            # 返回空结构（向后兼容模式）
            return self._empty_persona()

    def extract_from_preset(self, preset_name: str) -> Optional[Dict[str, Any]]:
        """
        从预设库获取Persona

        Args:
            preset_name: 预设名称（如"李诞"、"罗翔"）

        Returns:
            预设Persona或None
        """
        presets = self._load_presets()
        return presets.get(preset_name)

    @classmethod
    def get_preset(cls, preset_name: str) -> Optional[Dict[str, Any]]:
        """类方法：无需实例化获取预设Persona"""
        return cls._load_presets_static().get(preset_name)

    @classmethod
    def _load_presets_static(cls) -> Dict[str, Dict]:
        """静态方法加载预设，无需实例化"""
        return {
            "李诞": {
                "identity": {
                    "name": "李诞",
                    "archetype": "吐槽者",
                    "core_drive": "用幽默解构严肃，在荒诞中寻找真实",
                    "chemistry": "先认同后转折，用降维打击消解对方的严肃"
                },
                "expression": {
                    "pace": "slow",
                    "sentence_length": "short",
                    "signature_phrases": ["说白了", "这事儿逗不逗", "爱咋咋地"],
                    "attitude": "mournful"
                },
                "memory_seed": []
            },
            "罗翔": {
                "identity": {
                    "name": "罗翔",
                    "archetype": "追问者",
                    "core_drive": "用法治思维审视人性，在严肃中保持谦卑",
                    "chemistry": "用案例引导对方思考，不断追问本质"
                },
                "expression": {
                    "pace": "normal",
                    "sentence_length": "mixed",
                    "signature_phrases": ["各位同学", "我们必须思考", "法律是对人最低的道德要求"],
                    "attitude": "authoritative"
                },
                "memory_seed": []
            }
        }

    def _load_presets(self) -> Dict[str, Dict]:
        """加载预设Persona库"""
        return self._load_presets_static()

    def _validate_and_clean(self, persona: Dict) -> Dict[str, Any]:
        """验证并清理提取结果"""
        # 确保三层结构存在
        if "identity" not in persona:
            persona["identity"] = {}
        if "expression" not in persona:
            persona["expression"] = {}
        if "memory_seed" not in persona:
            persona["memory_seed"] = []

        # 清理identity字段
        identity = persona["identity"]
        identity.setdefault("name", "")
        identity.setdefault("archetype", "观察者")
        identity.setdefault("core_drive", "")
        identity.setdefault("chemistry", "")

        # 清理expression字段
        expression = persona["expression"]
        expression.setdefault("pace", "normal")
        expression.setdefault("sentence_length", "mixed")
        expression.setdefault("signature_phrases", [])
        expression.setdefault("attitude", "curious")

        # 限制signature_phrases最多3个
        if len(expression["signature_phrases"]) > 3:
            expression["signature_phrases"] = expression["signature_phrases"][:3]

        # 清理memory_seed
        if not isinstance(persona["memory_seed"], list):
            persona["memory_seed"] = []

        # 确保每条memory有完整字段
        for mem in persona["memory_seed"]:
            if isinstance(mem, dict):
                mem.setdefault("title", "")
                mem.setdefault("content", "")
                mem.setdefault("tags", [])

        return persona

    def _empty_persona(self) -> Dict[str, Any]:
        """返回空Persona结构"""
        return {
            "identity": {
                "name": "",
                "archetype": "观察者",
                "core_drive": "",
                "chemistry": ""
            },
            "expression": {
                "pace": "normal",
                "sentence_length": "mixed",
                "signature_phrases": [],
                "attitude": "curious"
            },
            "memory_seed": []
        }


# 便捷函数
def extract_persona(
    text: str,
    user_hint: str = "",
    api_key: Optional[str] = None,
    raise_on_error: bool = True,
    gender: str = "female"
) -> Dict[str, Any]:
    """
    便捷提取函数

    Args:
        text: 用户提供的材料
        user_hint: 风格提示
        api_key: API密钥
        raise_on_error: 失败时是否抛出异常（默认True）
        gender: 性别（"male"或"female"），用于选择合适音色
    """
    extractor = PersonaExtractor(api_key=api_key, gender=gender)
    return extractor.extract(text, user_hint, raise_on_error=raise_on_error, gender=gender)


def get_preset_persona(preset_name: str) -> Optional[Dict[str, Any]]:
    """获取预设Persona（无需API Key）"""
    return PersonaExtractor.get_preset(preset_name)


def normalize_subagent_persona(persona_dict: dict, gender: str = "female") -> Dict[str, Any]:
    """
    接收外部Sub-Agent返回的Persona，执行本地兜底处理：
    - 填充默认值
    - 语音映射（如果缺失voice_id）
    - 截断signature_phrases到3个

    Args:
        persona_dict: Sub-Agent返回的原始Persona字典
        gender: 性别（"male"或"female"），用于推荐音色

    Returns:
        验证并清理后的Persona字典
    """
    # 记录原始输入是否已包含voice_id（避免_validate_and_clean的副作用导致误判）
    original_voice_id = persona_dict.get("expression", {}).get("voice_id")

    extractor = PersonaExtractor(gender=gender, skip_client_init=True)
    cleaned = extractor._validate_and_clean(persona_dict)

    # 深拷贝，避免修改原始输入字典（防止多次调用时互相污染）
    import copy
    cleaned = copy.deepcopy(cleaned)

    # 如果原始输入缺失voice_id，使用本地VoiceSelector推荐
    if not original_voice_id:
        voice_selector = VoiceSelector()
        archetype = cleaned.get("identity", {}).get("archetype", "观察者")
        attitude = cleaned.get("expression", {}).get("attitude", "curious")
        suggested = voice_selector.suggest_voice(archetype=archetype, attitude=attitude, gender=gender)
        cleaned["expression"]["voice_id"] = suggested

    return cleaned
