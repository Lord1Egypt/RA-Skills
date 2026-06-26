"""
验证 ResearchPackage 数据契约的严格性
"""
import pytest
from src.schema import ResearchPackage, ResearchSegment, ResearchMaterial


def test_valid_research_package():
    """合法的 ResearchPackage 应该被正确解析"""
    pkg = {
        "schema_version": "2.1",
        "source": "人工智能的发展趋势",
        "source_type": "topic",
        "style_selected": "深度对谈",
        "hook": "AI 离我们有多远？",
        "central_insight": "AI 正在重塑工作的基本单元",
        "content_outline": "全篇采用渐进式揭露结构。seg_01 从日常办公切入建立共鸣；seg_02 抛出核心冲突并给出数据支撑。深度对谈风格，语气沉稳。",
        "segments": [
            {
                "segment_id": "seg_01",
                "narrative_function": "setup",
                "dramatic_goal": "建立代入感",
                "content_focus": "AI 在办公场景中的渗透",
                "estimated_length": 600,
                "materials_to_use": ["mat_001"],
                "persona_dynamics": {
                    "who_initiates": "A",
                    "dynamic_mode": "storytelling",
                    "emotional_tone": "curious"
                },
                "outline": "本段弧线：从日常观察到建立共鸣。关键转折点在中段，用36氪案例打破听众对AI办公的遥远感。推进计划：A以身边变化发问，B起初不以为然，A用数据说服，B产生共鸣。深度对谈风格，情绪平稳。"
            },
            {
                "segment_id": "seg_02",
                "narrative_function": "confrontation",
                "dramatic_goal": "抛出核心冲突",
                "content_focus": "AI 替代人类工作的边界",
                "estimated_length": 800,
                "materials_to_use": ["mat_002"],
                "persona_dynamics": {
                    "who_initiates": "B",
                    "dynamic_mode": "challenge",
                    "emotional_tone": "tense"
                }
            }
        ],
        "enriched_materials": [
            {
                "material_id": "mat_001",
                "material_type": "案例故事",
                "content": "某团队使用 ChatGPT 后效率提升 40%",
                "source": "36氪",
                "related_topic": "AI 办公",
                "usage_hint": "开场共鸣"
            },
            {
                "material_id": "mat_002",
                "material_type": "专家观点",
                "content": "MIT 教授认为短期冲击被高估",
                "source": "MIT Technology Review",
                "related_topic": "AI 与就业",
                "usage_hint": "用于挑战恐慌叙事"
            }
        ]
    }

    result = ResearchPackage.model_validate(pkg)
    assert result.schema_version == "2.1"
    assert result.source == "人工智能的发展趋势"
    assert result.style_selected == "深度对谈"
    assert len(result.segments) == 2
    assert len(result.enriched_materials) == 2
    assert result.segments[0].segment_id == "seg_01"
    assert result.enriched_materials[0].material_id == "mat_001"
    assert result.segments[0].outline is not None
    assert "建立共鸣" in result.segments[0].outline


def test_missing_segments_should_fail():
    """缺少 segments 时必须验证失败"""
    pkg = {
        "schema_version": "2.0",
        "source": "测试主题",
        "source_type": "topic",
        "style_selected": "深度对谈",
    }

    with pytest.raises(Exception):
        ResearchPackage.model_validate(pkg)


def test_empty_segments_should_fail():
    """segments 为空列表时必须验证失败"""
    pkg = {
        "schema_version": "2.0",
        "source": "测试主题",
        "source_type": "topic",
        "style_selected": "深度对谈",
        "segments": []
    }

    with pytest.raises(Exception):
        ResearchPackage.model_validate(pkg)


def test_invalid_segment_id_should_fail():
    """segment_id 不符合 seg_XX 格式时必须失败"""
    pkg = {
        "schema_version": "2.0",
        "source": "测试主题",
        "source_type": "topic",
        "style_selected": "深度对谈",
        "segments": [
            {
                "segment_id": "segment_1",
                "narrative_function": "setup",
                "dramatic_goal": "目标",
                "content_focus": "焦点",
                "estimated_length": 600,
            }
        ]
    }

    with pytest.raises(Exception):
        ResearchPackage.model_validate(pkg)


def test_invalid_material_id_should_fail():
    """material_id 不符合 mat_XXX 格式时必须失败"""
    pkg = {
        "schema_version": "2.0",
        "source": "测试主题",
        "source_type": "topic",
        "style_selected": "深度对谈",
        "segments": [
            {
                "segment_id": "seg_01",
                "narrative_function": "setup",
                "dramatic_goal": "目标",
                "content_focus": "焦点",
                "estimated_length": 600,
            }
        ],
        "enriched_materials": [
            {
                "material_id": "m001",
                "material_type": "数据事实",
                "content": "内容",
                "source": "来源",
                "related_topic": "主题",
                "usage_hint": "用法"
            }
        ]
    }

    with pytest.raises(Exception):
        ResearchPackage.model_validate(pkg)


def test_invalid_narrative_function_should_fail():
    """narrative_function 不在枚举值中时必须失败"""
    pkg = {
        "schema_version": "2.0",
        "source": "测试主题",
        "source_type": "topic",
        "style_selected": "深度对谈",
        "segments": [
            {
                "segment_id": "seg_01",
                "narrative_function": "intro",
                "dramatic_goal": "目标",
                "content_focus": "焦点",
                "estimated_length": 600,
            }
        ]
    }

    with pytest.raises(Exception):
        ResearchPackage.model_validate(pkg)


def test_invalid_material_type_should_fail():
    """material_type 不在枚举值中时必须失败"""
    pkg = {
        "schema_version": "2.0",
        "source": "测试主题",
        "source_type": "topic",
        "style_selected": "深度对谈",
        "segments": [
            {
                "segment_id": "seg_01",
                "narrative_function": "setup",
                "dramatic_goal": "目标",
                "content_focus": "焦点",
                "estimated_length": 600,
            }
        ],
        "enriched_materials": [
            {
                "material_id": "mat_001",
                "material_type": "未知类型",
                "content": "内容",
                "source": "来源",
                "related_topic": "主题",
                "usage_hint": "用法"
            }
        ]
    }

    with pytest.raises(Exception):
        ResearchPackage.model_validate(pkg)


def test_model_dump_returns_dict():
    """model_dump() 应返回可被下游使用的纯 dict"""
    pkg = {
        "schema_version": "2.0",
        "source": "测试主题",
        "source_type": "topic",
        "style_selected": "深度对谈",
        "segments": [
            {
                "segment_id": "seg_01",
                "narrative_function": "setup",
                "dramatic_goal": "目标",
                "content_focus": "焦点",
                "estimated_length": 600,
            }
        ]
    }

    result = ResearchPackage.model_validate(pkg)
    d = result.model_dump()
    assert isinstance(d, dict)
    assert d["schema_version"] == "2.0"
    assert d["segments"][0]["segment_id"] == "seg_01"


def test_backward_compatibility_without_outline():
    """不含 outline 和 content_outline 的旧 schema 2.0 数据应仍能验证通过"""
    pkg = {
        "schema_version": "2.0",
        "source": "测试主题",
        "source_type": "topic",
        "style_selected": "深度对谈",
        "segments": [
            {
                "segment_id": "seg_01",
                "narrative_function": "setup",
                "dramatic_goal": "目标",
                "content_focus": "焦点",
                "estimated_length": 600,
            }
        ]
    }

    result = ResearchPackage.model_validate(pkg)
    assert result.schema_version == "2.0"
    assert result.content_outline is None
    assert result.segments[0].outline is None
