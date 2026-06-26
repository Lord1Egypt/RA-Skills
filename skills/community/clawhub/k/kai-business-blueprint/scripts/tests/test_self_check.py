from business_blueprint.knowledge_self_check import (
    SELF_CHECK_QUESTIONS,
    derive_questions,
    has_unresolved_questions,
    populate_self_check,
)


def test_has_unresolved_questions_true():
    entity = {"_selfCheck": {"questions": ["?"]}}
    assert has_unresolved_questions(entity) is True


def test_has_unresolved_questions_false_when_empty():
    entity = {"_selfCheck": {"questions": []}}
    assert has_unresolved_questions(entity) is False


def test_has_unresolved_questions_false_when_missing():
    entity = {"id": "pain-001"}
    assert has_unresolved_questions(entity) is False


def test_derive_questions_painpoint_always_keeps_root_cause():
    entity = {
        "id": "pain-001",
        "name": "X",
        "entityType": "painPoint",
        "severity": "high",
        "description": "stable description",
    }
    questions = derive_questions(entity, [])
    # painPoint always keeps the symptom-vs-root-cause question
    assert any("根因" in q for q in questions)


def test_derive_questions_strategy_without_solves_flagged():
    entity = {"id": "str-001", "name": "X", "entityType": "strategy"}
    questions = derive_questions(entity, [])
    assert any("solves" in q or "痛点" in q for q in questions)


def test_derive_questions_strategy_with_solves_skips_pain_question():
    entity = {"id": "str-001", "name": "X", "entityType": "strategy"}
    relations = [
        {"from": "str-001", "to": "pain-001", "type": "solves"},
    ]
    questions = derive_questions(entity, relations)
    # Should NOT include the "对应哪个痛点" question
    assert not any(q.startswith("对应哪个具体痛点") for q in questions)


def test_derive_questions_unknown_type_returns_empty():
    entity = {"id": "x-001", "name": "Y", "entityType": "unknownThing"}
    assert derive_questions(entity, []) == []


def test_populate_self_check_does_not_overwrite_existing():
    bp = {
        "library": {
            "knowledge": {
                "painPoints": [
                    {
                        "id": "pain-001",
                        "name": "X",
                        "entityType": "painPoint",
                        "_selfCheck": {"passed": ["A"], "questions": ["B"]},
                    }
                ]
            }
        },
        "relations": [],
    }
    populate_self_check(bp)
    sc = bp["library"]["knowledge"]["painPoints"][0]["_selfCheck"]
    assert sc["passed"] == ["A"]
    assert sc["questions"] == ["B"]


def test_populate_self_check_fills_missing():
    bp = {
        "library": {
            "knowledge": {
                "painPoints": [
                    {"id": "pain-001", "name": "X", "entityType": "painPoint"}
                ],
                "strategies": [
                    {"id": "str-001", "name": "Y", "entityType": "strategy"}
                ],
            }
        },
        "relations": [],
    }
    populate_self_check(bp)
    pain_check = bp["library"]["knowledge"]["painPoints"][0]["_selfCheck"]
    str_check = bp["library"]["knowledge"]["strategies"][0]["_selfCheck"]
    assert "questions" in pain_check
    assert "questions" in str_check
    assert isinstance(pain_check["questions"], list)
    assert isinstance(str_check["questions"], list)


def test_self_check_questions_cover_all_six_types():
    expected = {"painPoint", "strategy", "rule", "metric", "practice", "pitfall"}
    assert expected == set(SELF_CHECK_QUESTIONS.keys())
    for entity_type, questions in SELF_CHECK_QUESTIONS.items():
        assert isinstance(questions, list) and len(questions) >= 3
