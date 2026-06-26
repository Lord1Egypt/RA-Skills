import pytest

from business_blueprint.diff_patcher import (
    DiffPatchError,
    apply_diff,
    filter_diff,
    parse_path,
)


def test_parse_path_simple_keys():
    assert parse_path("library.knowledge.painPoints") == [
        "library", "knowledge", "painPoints"
    ]


def test_parse_path_with_index():
    assert parse_path("library.knowledge.painPoints[0].name") == [
        "library", "knowledge", "painPoints", 0, "name"
    ]


def test_parse_path_append_marker():
    assert parse_path("library.knowledge.painPoints[]") == [
        "library", "knowledge", "painPoints", -1
    ]


def test_modify_field():
    bp = {
        "library": {
            "knowledge": {
                "painPoints": [{"id": "pain-001", "name": "ROI 不稳"}]
            }
        }
    }
    diff = {
        "operations": [
            {
                "op": "modify",
                "path": "library.knowledge.painPoints[0].name",
                "old": "ROI 不稳",
                "new": "ROAS 波动",
            }
        ]
    }
    result = apply_diff(bp, diff)
    assert result["library"]["knowledge"]["painPoints"][0]["name"] == "ROAS 波动"
    # Original is not mutated
    assert bp["library"]["knowledge"]["painPoints"][0]["name"] == "ROI 不稳"


def test_add_via_append():
    bp = {"library": {"knowledge": {"painPoints": []}}}
    diff = {
        "operations": [
            {
                "op": "add",
                "path": "library.knowledge.painPoints[]",
                "value": {"id": "pain-002", "name": "新痛点", "entityType": "painPoint"},
            }
        ]
    }
    result = apply_diff(bp, diff)
    pain_points = result["library"]["knowledge"]["painPoints"]
    assert len(pain_points) == 1
    assert pain_points[0]["id"] == "pain-002"


def test_add_to_missing_array_creates_it():
    bp = {"library": {"knowledge": {}}}
    diff = {
        "operations": [
            {
                "op": "add",
                "path": "library.knowledge.strategies[]",
                "value": {"id": "str-001", "name": "X", "entityType": "strategy"},
            }
        ]
    }
    result = apply_diff(bp, diff)
    assert len(result["library"]["knowledge"]["strategies"]) == 1


def test_delete_indexed_entry():
    bp = {
        "library": {
            "knowledge": {
                "pitfalls": [
                    {"id": "pit-001", "name": "A"},
                    {"id": "pit-002", "name": "B"},
                    {"id": "pit-003", "name": "C"},
                ]
            }
        }
    }
    diff = {"operations": [{"op": "delete", "path": "library.knowledge.pitfalls[1]"}]}
    result = apply_diff(bp, diff)
    pitfalls = result["library"]["knowledge"]["pitfalls"]
    assert [p["id"] for p in pitfalls] == ["pit-001", "pit-003"]


def test_multiple_ops_in_order():
    bp = {
        "library": {
            "knowledge": {"painPoints": [{"id": "pain-001", "name": "X"}]}
        }
    }
    diff = {
        "operations": [
            {
                "op": "modify",
                "path": "library.knowledge.painPoints[0].name",
                "new": "Y",
            },
            {
                "op": "add",
                "path": "library.knowledge.painPoints[]",
                "value": {"id": "pain-002", "name": "Z", "entityType": "painPoint"},
            },
        ]
    }
    result = apply_diff(bp, diff)
    pain_points = result["library"]["knowledge"]["painPoints"]
    assert pain_points[0]["name"] == "Y"
    assert pain_points[1]["name"] == "Z"


def test_unknown_op_raises():
    bp = {"library": {}}
    diff = {"operations": [{"op": "totally-made-up", "path": "library"}]}
    with pytest.raises(DiffPatchError):
        apply_diff(bp, diff)


def test_filter_diff_rejects_some():
    diff = {
        "operations": [
            {"op": "modify", "path": "x", "new": "a"},
            {"op": "modify", "path": "y", "new": "b"},
            {"op": "modify", "path": "z", "new": "c"},
        ]
    }
    decisions = {0: "accept", 1: "reject", 2: "accept"}
    filtered = filter_diff(diff, decisions)
    assert len(filtered["operations"]) == 2
    assert filtered["operations"][0]["path"] == "x"
    assert filtered["operations"][1]["path"] == "z"


def test_empty_operations_is_noop():
    bp = {"library": {"knowledge": {"painPoints": []}}}
    result = apply_diff(bp, {"operations": []})
    assert result == bp


def test_modify_missing_index_raises():
    bp = {"library": {"knowledge": {"painPoints": []}}}
    diff = {
        "operations": [
            {
                "op": "modify",
                "path": "library.knowledge.painPoints[5].name",
                "new": "X",
            }
        ]
    }
    with pytest.raises(DiffPatchError):
        apply_diff(bp, diff)
