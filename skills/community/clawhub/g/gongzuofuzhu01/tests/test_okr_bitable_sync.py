"""Tests for OKR Bitable Sync bridge."""

import sys
from pathlib import Path

_skill_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_skill_root))

from scripts.okr_sync_bitable import parse_bitable_rows, FIELD_MAP, BITABLE_CONFIG


def test_parse_empty():
    assert parse_bitable_rows([]) == []


def test_parse_single_o_no_kr():
    """Objective row with no KR."""
    records = [{
        "fields": {
            "YOUR_FIELD_ID_OBJECTIVE": "提升系统稳定性",
            "YOUR_FIELD_ID_KR": None,
            "YOUR_FIELD_ID_COMPLETION": 60.0,
            "YOUR_FIELD_ID_STATUS": "进行中",
            "YOUR_FIELD_ID_DEPT": "技术中心",
        }
    }]
    result = parse_bitable_rows(records)
    assert len(result) == 1
    assert result[0]["title"] == "提升系统稳定性"
    assert result[0]["obj_type"] == "objective"
    assert result[0]["progress"] == 60.0
    assert result[0]["status"] == "active"
    assert result[0]["extra"]["department"] == "技术中心"
    assert result[0]["key_results"] == []


def test_parse_o_with_krs():
    """O with 2 KRs, grouping by objective field."""
    records = [
        {"fields": {"YOUR_FIELD_ID_OBJECTIVE": "提升稳定性", "YOUR_FIELD_ID_KR": None, "YOUR_FIELD_ID_COMPLETION": 50.0}},
        {"fields": {"YOUR_FIELD_ID_OBJECTIVE": "提升稳定性", "YOUR_FIELD_ID_KR": "P99<200ms", "YOUR_FIELD_ID_COMPLETION": 80.0, "YOUR_FIELD_ID_KR_WEIGHT": 30.0}},
        {"fields": {"YOUR_FIELD_ID_OBJECTIVE": "提升稳定性", "YOUR_FIELD_ID_KR": "可用性99.95%", "YOUR_FIELD_ID_COMPLETION": 40.0, "YOUR_FIELD_ID_KR_WEIGHT": 70.0}},
    ]
    result = parse_bitable_rows(records)
    assert len(result) == 1
    o = result[0]
    assert o["title"] == "提升稳定性"
    assert len(o["key_results"]) == 2
    assert o["key_results"][0]["title"] == "P99<200ms"
    assert o["key_results"][0]["weight"] == 30.0
    assert o["key_results"][1]["title"] == "可用性99.95%"


def test_parse_multiple_os():
    """2 O's with KRs."""
    records = [
        {"fields": {"YOUR_FIELD_ID_OBJECTIVE": "提升稳定性", "YOUR_FIELD_ID_KR": None}},
        {"fields": {"YOUR_FIELD_ID_OBJECTIVE": "提升稳定性", "YOUR_FIELD_ID_KR": "P99<200ms"}},
        {"fields": {"YOUR_FIELD_ID_OBJECTIVE": "加速交付", "YOUR_FIELD_ID_KR": None}},
        {"fields": {"YOUR_FIELD_ID_OBJECTIVE": "加速交付", "YOUR_FIELD_ID_KR": "每日部署"}},
    ]
    result = parse_bitable_rows(records)
    assert len(result) == 2
    assert result[0]["title"] == "提升稳定性"
    assert result[1]["title"] == "加速交付"
    assert len(result[0]["key_results"]) == 1
    assert len(result[1]["key_results"]) == 1


def test_parse_missing_fields():
    """Missing fields get defaults."""
    records = [{"fields": {"YOUR_FIELD_ID_OBJECTIVE": "仅标题"}}]
    result = parse_bitable_rows(records)
    assert result[0]["progress"] == 0
    assert result[0]["status"] == "active"
    assert result[0]["extra"] == {}


def test_parse_status_mapping():
    """Status mapping: 进行中→active, 已完成→completed."""
    records = [{"fields": {"YOUR_FIELD_ID_OBJECTIVE": "测试", "YOUR_FIELD_ID_KR": None, "YOUR_FIELD_ID_STATUS": "已完成"}}]
    result = parse_bitable_rows(records)
    assert result[0]["status"] == "completed"


def test_config_exists():
    """Configuration is present and valid."""
    assert "app_token" in BITABLE_CONFIG
    assert "table_id" in BITABLE_CONFIG
    assert len(FIELD_MAP) >= 10


def test_kr_defaults():
    """KR with minimal fields gets sensible defaults."""
    records = [{"fields": {"YOUR_FIELD_ID_OBJECTIVE": "O", "YOUR_FIELD_ID_KR": "KR1"}}]
    result = parse_bitable_rows(records)
    kr = result[0]["key_results"][0]
    assert kr["progress"] == 0
    assert kr["weight"] == 0
    assert kr["status"] == "active"
