from pathlib import Path

import json
import pytest

from business_blueprint.refine import (
    build_refine_prompt,
    generate_diff,
    parse_refine_response,
    refine_blueprint,
)


def _sample_blueprint() -> dict:
    return {
        "meta": {
            "blueprintType": "domain-knowledge",
            "detectedIntent": "test",
            "revisionId": "rev-base",
        },
        "context": {"clarifications": []},
        "library": {
            "knowledge": {
                "painPoints": [
                    {"id": "pain-001", "name": "ROI 不稳", "entityType": "painPoint"}
                ]
            }
        },
        "relations": [],
    }


def test_build_refine_prompt_contains_blueprint_and_feedback():
    bp = _sample_blueprint()
    prompt = build_refine_prompt(bp, "拆细痛点")
    assert "ROI 不稳" in prompt
    assert "拆细痛点" in prompt
    assert "rev-base" in prompt


def test_parse_refine_response_pure_json():
    raw = json.dumps({
        "diffId": "diff-x",
        "operations": [],
        "rationale": "no changes",
    })
    parsed = parse_refine_response(raw)
    assert parsed["diffId"] == "diff-x"
    assert parsed["operations"] == []


def test_parse_refine_response_handles_fenced_block():
    raw = '```json\n{"diffId": "diff-y", "operations": []}\n```'
    parsed = parse_refine_response(raw)
    assert parsed["diffId"] == "diff-y"


def test_parse_refine_response_handles_generic_fence():
    raw = '```\n{"diffId": "diff-z", "operations": []}\n```'
    parsed = parse_refine_response(raw)
    assert parsed["diffId"] == "diff-z"


def test_generate_diff_uses_injected_llm_call():
    bp = _sample_blueprint()
    fake_response = json.dumps({
        "diffId": "diff-1",
        "operations": [
            {
                "op": "modify",
                "path": "library.knowledge.painPoints[0].name",
                "old": "ROI 不稳",
                "new": "ROAS 波动",
            }
        ],
        "rationale": "拆分粒度",
    })
    diff = generate_diff(bp, "feedback", lambda prompt: fake_response)
    assert diff["operations"][0]["new"] == "ROAS 波动"


def test_refine_blueprint_applies_diff_and_writes(tmp_path: Path):
    bp_path = tmp_path / "bp.json"
    out_path = tmp_path / "out.json"
    bp_path.write_text(
        json.dumps(_sample_blueprint(), ensure_ascii=False), encoding="utf-8"
    )

    fake_response = json.dumps({
        "diffId": "diff-1",
        "operations": [
            {
                "op": "modify",
                "path": "library.knowledge.painPoints[0].name",
                "old": "ROI 不稳",
                "new": "ROAS 波动",
            }
        ],
        "rationale": "test",
    })

    diff = refine_blueprint(
        blueprint_path=bp_path,
        feedback="test feedback",
        output_path=out_path,
        llm_call=lambda prompt: fake_response,
    )

    assert diff["diffId"] == "diff-1"

    new_bp = json.loads(out_path.read_text(encoding="utf-8"))
    assert new_bp["library"]["knowledge"]["painPoints"][0]["name"] == "ROAS 波动"
    # revision metadata is bumped
    assert new_bp["meta"]["revisionId"] != "rev-base"
    assert new_bp["meta"]["parentRevisionId"] == "rev-base"
    assert new_bp["meta"]["lastModifiedBy"] == "ai-refine"

    # diff sidecar is written
    diff_path = out_path.with_suffix(".diff.json")
    assert diff_path.exists()


def test_refine_blueprint_no_apply_writes_only_diff(tmp_path: Path):
    bp_path = tmp_path / "bp.json"
    out_path = tmp_path / "out.json"
    bp_path.write_text(json.dumps(_sample_blueprint()), encoding="utf-8")

    fake = json.dumps({"diffId": "d", "operations": [], "rationale": ""})
    refine_blueprint(
        blueprint_path=bp_path,
        feedback="x",
        output_path=out_path,
        llm_call=lambda prompt: fake,
        auto_apply=False,
    )

    assert not out_path.exists()
    assert out_path.with_suffix(".diff.json").exists()


def test_parse_refine_response_empty_raises():
    with pytest.raises(ValueError):
        parse_refine_response("")
