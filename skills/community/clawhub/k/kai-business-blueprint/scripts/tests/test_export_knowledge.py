from pathlib import Path

from business_blueprint.export_knowledge import (
    export_knowledge_svg,
    is_knowledge_blueprint,
    render_knowledge_svg,
)


def _sample_blueprint() -> dict:
    return {
        "meta": {
            "blueprintType": "domain-knowledge",
            "title": "Test KG",
            "detectedIntent": "test intent",
        },
        "library": {
            "knowledge": {
                "painPoints": [
                    {
                        "id": "pain-001",
                        "name": "ROI 不稳",
                        "entityType": "painPoint",
                        "severity": "high",
                        "_selfCheck": {
                            "passed": [],
                            "questions": ["是症状还是根因？"],
                        },
                    }
                ],
                "strategies": [
                    {
                        "id": "str-001",
                        "name": "测款节奏策略",
                        "entityType": "strategy",
                    }
                ],
                "metrics": [
                    {
                        "id": "met-001",
                        "name": "ROAS 基准",
                        "entityType": "metric",
                    }
                ],
            }
        },
        "relations": [
            {"id": "rel-001", "type": "solves", "from": "str-001", "to": "pain-001"},
            {"id": "rel-002", "type": "measures", "from": "met-001", "to": "str-001"},
        ],
    }


def test_render_produces_svg_root():
    svg = render_knowledge_svg(_sample_blueprint())
    assert svg.startswith("<svg")
    assert svg.rstrip().endswith("</svg>")


def test_render_includes_all_entity_names():
    svg = render_knowledge_svg(_sample_blueprint())
    assert "ROI 不稳" in svg
    assert "测款节奏策略" in svg
    assert "ROAS 基准" in svg


def test_render_emits_self_check_badge():
    svg = render_knowledge_svg(_sample_blueprint())
    # The badge text and tooltip should appear when questions != []
    assert "kg-selfcheck-badge" in svg
    assert "未确认的自检项" in svg


def test_render_no_badge_when_questions_empty():
    bp = _sample_blueprint()
    bp["library"]["knowledge"]["painPoints"][0]["_selfCheck"]["questions"] = []
    svg = render_knowledge_svg(bp)
    assert "kg-selfcheck-badge" not in svg


def test_render_includes_relation_arrows():
    svg = render_knowledge_svg(_sample_blueprint())
    # Each relation type uses a unique marker id
    assert 'marker-end="url(#kg-arrow-solves)"' in svg
    assert 'marker-end="url(#kg-arrow-measures)"' in svg


def test_render_skips_relations_referencing_unknown_entities():
    bp = _sample_blueprint()
    bp["relations"].append(
        {"id": "rel-bogus", "type": "solves", "from": "ghost", "to": "pain-001"}
    )
    svg = render_knowledge_svg(bp)
    # Should not crash and should still include valid relations
    assert "ROI 不稳" in svg


def test_export_writes_file(tmp_path: Path):
    target = tmp_path / "out.svg"
    export_knowledge_svg(_sample_blueprint(), target)
    text = target.read_text(encoding="utf-8")
    assert text.startswith("<svg")
    assert "测款节奏策略" in text


def test_is_knowledge_blueprint_via_meta():
    bp = {"meta": {"blueprintType": "domain-knowledge"}, "library": {}}
    assert is_knowledge_blueprint(bp) is True


def test_is_knowledge_blueprint_via_non_empty_knowledge():
    bp = {
        "meta": {},
        "library": {
            "knowledge": {
                "painPoints": [
                    {"id": "pain-001", "name": "X", "entityType": "painPoint"}
                ]
            }
        },
    }
    assert is_knowledge_blueprint(bp) is True


def test_is_not_knowledge_blueprint_for_pure_architecture():
    bp = {
        "meta": {"blueprintType": "architecture"},
        "library": {"capabilities": [{"id": "cap-001", "name": "X"}]},
    }
    assert is_knowledge_blueprint(bp) is False


def test_render_handles_empty_knowledge_gracefully():
    bp = {
        "meta": {"blueprintType": "domain-knowledge", "title": "Empty"},
        "library": {"knowledge": {"painPoints": [], "strategies": []}},
        "relations": [],
    }
    svg = render_knowledge_svg(bp)
    assert svg.startswith("<svg")


def test_render_unknown_entity_type_uses_default_style():
    bp = {
        "meta": {"blueprintType": "domain-knowledge"},
        "library": {
            "knowledge": {
                "caseStudies": [
                    {"id": "cs-001", "name": "案例 A", "entityType": "caseStudy"}
                ]
            }
        },
        "relations": [],
    }
    svg = render_knowledge_svg(bp)
    assert "案例 A" in svg
