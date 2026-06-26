"""
AI Podcast Dual-Host Schema Definitions
数据契约：所有 SubAgent 间通信的 Pydantic 模型
"""

from datetime import datetime
from typing import Literal, List, Optional
from pydantic import BaseModel, Field, field_validator


class TokenUsage(BaseModel):
    """Token 使用统计"""
    input: int = Field(ge=0, description="输入token数")
    output: int = Field(ge=0, description="输出token数")
    total: int = Field(ge=0)


class ResearchTopic(BaseModel):
    """研究主题"""
    title: str = Field(max_length=100)
    key_points: List[str] = Field(max_length=5, description="每个topic最多5个要点")
    signals: List[Literal["争议", "重要性", "时效性", "专业性"]] = Field(default_factory=list)


class TopicAbstraction(BaseModel):
    """主题抽象/切入角度"""
    angle: str = Field(max_length=200, description="切入角度")
    talkability: Literal["高", "中", "低"] = Field(description="可讨论性评级")
    conflict_potential: Optional[str] = Field(None, max_length=100, description="潜在冲突点")


class DetailedMaterial(BaseModel):
    """详细材料条目 - 供Stage 2按需引用"""
    material_id: str = Field(pattern=r'^mat_[0-9]{3}$', description="材料编号 mat_001, mat_002...")
    material_type: Literal["数据事实", "案例故事", "专家观点", "反面论点", "背景信息"]
    content: str = Field(max_length=500, description="材料内容原文或摘要")
    source: Optional[str] = Field(None, max_length=100, description="来源说明")
    related_topic: str = Field(description="关联的topic标题")
    usage_hint: str = Field(max_length=100, description="使用建议，如'用于支撑效率提升观点'")


class ResearchMaterials(BaseModel):
    """Research Agent生成的详细材料库 - 渐进式披露给Stage 2"""
    schema_version: Literal["1.0"] = "1.0"
    session_id: str = Field(pattern=r'^[a-z0-9]{12}$')
    materials: List[DetailedMaterial] = Field(max_length=20, description="详细材料列表，最多20条")
    statistics_summary: Optional[str] = Field(None, max_length=500, description="关键统计数据汇总")
    quotes_collection: Optional[str] = Field(None, max_length=800, description="关键引用合集")


class ResearchSummary(BaseModel):
    """Research Agent输出，Orchestrator与Content Generator输入"""
    schema_version: Literal["1.0"] = "1.0"
    session_id: str = Field(pattern=r'^[a-z0-9]{12}$')
    topics: List[ResearchTopic] = Field(min_length=1, max_length=5)
    topic_abstraction: List[TopicAbstraction] = Field(min_length=1, max_length=3)
    materials: List[DetailedMaterial] = Field(default_factory=list, max_length=20, description="详细材料库供Stage 2引用")
    token_usage: TokenUsage
    confidence: float = Field(ge=0.0, le=1.0)

    @field_validator('confidence')
    @classmethod
    def check_confidence(cls, v: float) -> float:
        if v < 0.6:
            raise ValueError(f"Research confidence {v} below threshold 0.6")
        return v


class OutlineSegment(BaseModel):
    """大纲段落定义"""
    segment_id: str = Field(pattern=r'^seg_[0-9]{2}$')
    goal: str = Field(max_length=200, description="本段目标")
    content_focus: str = Field(max_length=100, description="内容焦点")
    interaction_hint: Literal["debate", "casual", "deep", "comedy", "news"]
    estimated_length: int = Field(ge=50, le=2500, description="预估字数")


class Outline(BaseModel):
    """Content Generator Stage 1输出"""
    schema_version: Literal["1.0"] = "1.0"
    session_id: str
    segments: List[OutlineSegment] = Field(min_length=3, max_length=6)  # 3-6个段落
    persona_applied: List[str] = Field(description="应用的Persona特质")
    style_template: Literal["高效传达", "发散漫谈", "深度对谈", "观点交锋", "喜剧风格"]
    total_estimated_length: int = Field(ge=300, le=12000)


class DialogueLine(BaseModel):
    """单句对话 - 简化版，只保留核心字段"""
    speaker: Literal["A", "B"]
    text: str = Field(max_length=500, min_length=2, description="单句2-500字符，口语化")


class ScriptVersion(BaseModel):
    """Content Generator Stage 2输出 - 简化版"""
    schema_version: Literal["1.0"] = "1.0"
    session_id: str
    outline_checksum: str = Field(description="源outline的hash")
    lines: List[DialogueLine] = Field(max_length=600)
    word_count: int = Field(ge=300, le=15000)
    estimated_duration_sec: int = Field(ge=60, le=2400, description="预估音频秒数")
    token_usage: TokenUsage

    @classmethod
    def create_for_test(
        cls,
        lines: List[DialogueLine],
        session_id: str = "test_session",
        word_count: Optional[int] = None,
        estimated_duration_sec: Optional[int] = None,
    ) -> "ScriptVersion":
        """
        创建用于测试的 ScriptVersion 实例

        自动计算 word_count 和 estimated_duration_sec，填充必需的占位符字段

        Args:
            lines: 对话行列表
            session_id: 会话ID
            word_count: 字数（自动计算）
            estimated_duration_sec: 预估时长（自动计算）

        Returns:
            ScriptVersion 实例
        """
        # 自动计算字数
        if word_count is None:
            word_count = sum(len(line.text) for line in lines)

        # 自动计算时长（假设每分钟250字）
        if estimated_duration_sec is None:
            estimated_duration_sec = max(120, min(1500, int(word_count / 250 * 60)))

        return cls(
            session_id=session_id,
            outline_checksum="test_checksum_" + session_id,
            lines=lines,
            word_count=word_count,
            estimated_duration_sec=estimated_duration_sec,
            token_usage=TokenUsage(input=1000, output=word_count, total=1000 + word_count),
        )


class ResearchSegment(BaseModel):
    """Research Sub-Agent输出：单个 segment"""
    segment_id: str = Field(pattern=r'^seg_[0-9]{2}$')
    narrative_function: Literal["setup", "confrontation", "resolution"]
    dramatic_goal: str = Field(max_length=300)
    content_focus: str = Field(max_length=200)
    estimated_length: int = Field(ge=50, le=2500)
    materials_to_use: List[str] = Field(default_factory=list)
    persona_dynamics: dict = Field(default_factory=dict)
    outline: Optional[str] = Field(None, max_length=1000)
    # 自然语言大纲，描述本段的内容节奏、情绪弧线、关键转折、与上下段的衔接方式


class ResearchMaterial(BaseModel):
    """Research Sub-Agent输出：单条材料"""
    material_id: str = Field(pattern=r'^mat_[0-9]{3}$')
    material_type: Literal["数据事实", "案例故事", "专家观点", "反面论点", "背景信息"]
    content: str = Field(max_length=1500)
    source: Optional[str] = Field(None, max_length=200)
    related_topic: str = Field(max_length=200)
    usage_hint: str = Field(max_length=200)


class ResearchPackage(BaseModel):
    """Research Sub-Agent必须返回的严格数据包"""
    schema_version: Literal["2.0", "2.1"] = "2.1"
    session_id: Optional[str] = None
    source: str
    source_type: Literal["topic", "url", "pdf"]
    style_selected: str
    style_reasoning: Optional[str] = None
    hook: Optional[str] = None
    central_insight: Optional[str] = None
    content_outline: Optional[str] = Field(None, max_length=1500)
    # 整体内容大纲，描述全篇在不同风格下的表达节奏设计
    segments: List[ResearchSegment] = Field(min_length=1)
    enriched_materials: List[ResearchMaterial] = Field(default_factory=list)


class PodcastOutput(BaseModel):
    """最终产物"""
    session_id: str
    outline: Outline
    script: ScriptVersion
    audio_path: str
    research_summary: ResearchSummary
    cost_report: dict
    generated_at: datetime
