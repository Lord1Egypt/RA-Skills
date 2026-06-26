"""
验证外部 Sub-Agent Persona 的本地 normalize 逻辑
"""
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.persona_extractor import normalize_subagent_persona


def test_normalize_subagent_persona_fills_defaults():
    """Sub-Agent 返回不完整的 Persona 时，应填充默认值"""
    raw = {
        "identity": {
            "name": "测试主持人"
        }
    }

    result = normalize_subagent_persona(raw, gender="female")

    assert result["identity"]["name"] == "测试主持人"
    assert result["identity"]["archetype"] == "观察者"
    assert result["identity"]["core_drive"] == ""
    assert result["identity"]["chemistry"] == ""
    assert result["expression"]["pace"] == "normal"
    assert result["expression"]["sentence_length"] == "mixed"
    assert result["expression"]["attitude"] == "curious"
    assert isinstance(result["expression"]["voice_id"], str)
    assert len(result["expression"]["voice_id"]) > 0
    assert result["memory_seed"] == []


def test_normalize_subagent_persona_truncates_phrases():
    """signature_phrases 超过 3 个时应截断"""
    raw = {
        "identity": {"name": "测试"},
        "expression": {
            "signature_phrases": [" phrase1", " phrase2", " phrase3", " phrase4"]
        }
    }

    result = normalize_subagent_persona(raw)
    assert len(result["expression"]["signature_phrases"]) == 3
    assert result["expression"]["signature_phrases"][0] == " phrase1"


def test_normalize_subagent_persona_keeps_existing_voice_id():
    """若 Sub-Agent 已提供 voice_id，不应被覆盖"""
    raw = {
        "identity": {"name": "测试"},
        "expression": {
            "voice_id": "zh_female_vv_uranus_bigtts"
        }
    }

    result = normalize_subagent_persona(raw)
    assert result["expression"]["voice_id"] == "zh_female_vv_uranus_bigtts"


def test_normalize_subagent_persona_suggests_voice_by_gender():
    """根据 gender 推荐不同默认音色"""
    raw = {
        "identity": {"name": "测试", "archetype": "观察者"},
        "expression": {"attitude": "curious"}
    }

    female = normalize_subagent_persona(raw, gender="female")
    male = normalize_subagent_persona(raw, gender="male")

    assert female["expression"]["voice_id"] != male["expression"]["voice_id"]
    assert "female" in female["expression"]["voice_id"] or "_" in female["expression"]["voice_id"]
    assert "male" in male["expression"]["voice_id"]
