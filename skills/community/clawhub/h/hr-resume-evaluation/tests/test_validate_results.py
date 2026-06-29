from copy import deepcopy

import pytest

from scripts.validate_results import ValidationError, validate_evaluation


def valid_result():
    return {
        "candidate_id": "alice-resume",
        "inferred_profile": {
            "role_family": "engineering",
            "seniority": "mid",
            "domain_context": "backend services",
            "confidence": 0.8,
        },
        "scores": {
            "score_basis": "resume_plus_jd_company",
            "overall": 82,
            "resume_quality": 50,
            "jd_company_match": 32,
            "dimensions": [
                {
                    "name": "backend experience",
                    "score": 24,
                    "max_score": 30,
                    "evidence": ["Built production API services."],
                    "deductions": [],
                }
            ],
        },
        "evidence": ["Python and API delivery experience."],
        "deductions": ["Limited explicit cloud ownership evidence."],
        "strengths": ["Clear backend implementation history."],
        "concerns": ["Needs validation on distributed systems depth."],
        "interview_validation_points": ["Probe API reliability ownership."],
        "compliance": {
            "sensitive_or_irrelevant_information": [],
            "must_not_use_for_screening": [],
            "manual_review_required": [],
            "no_auto_reject_reasons": ["Recommendation is a review aid only."],
        },
        "recommendation": {
            "screening_bucket": "review",
            "summary": "Relevant experience with some areas to validate.",
            "next_steps": ["Recruiter review"],
        },
    }


def test_valid_result_passes():
    assert validate_evaluation(valid_result())["scores"]["overall"] == 82


def test_invalid_bucket_fails():
    result = deepcopy(valid_result())
    result["recommendation"]["screening_bucket"] = "reject"

    with pytest.raises(ValidationError, match="screening_bucket"):
        validate_evaluation(result)


def test_missing_profile_role_family_fails():
    result = deepcopy(valid_result())
    del result["inferred_profile"]["role_family"]

    with pytest.raises(ValidationError, match="role_family|missing required key"):
        validate_evaluation(result)


def test_missing_recommendation_summary_fails():
    result = deepcopy(valid_result())
    del result["recommendation"]["summary"]

    with pytest.raises(ValidationError, match="summary|missing required key"):
        validate_evaluation(result)


def test_recommendation_next_steps_must_be_list():
    result = deepcopy(valid_result())
    result["recommendation"]["next_steps"] = "Recruiter review"

    with pytest.raises(ValidationError, match="next_steps"):
        validate_evaluation(result)


def test_recommendation_summary_rejects_final_decision_label():
    result = deepcopy(valid_result())
    result["recommendation"]["summary"] = "Hire this candidate based on the resume."

    with pytest.raises(ValidationError, match="final decision label"):
        validate_evaluation(result)


def test_recommendation_next_steps_reject_final_decision_label():
    result = deepcopy(valid_result())
    result["recommendation"]["next_steps"] = ["通知候选人通过筛选"]

    with pytest.raises(ValidationError, match="final decision label"):
        validate_evaluation(result)


def test_compliance_warning_labels_do_not_trigger_recommendation_label_check():
    result = deepcopy(valid_result())
    result["compliance"]["no_auto_reject_reasons"] = [
        "Do not reject or eliminate automatically."
    ]
    result["compliance"]["manual_review_required"] = ["不得自动淘汰，需要人工复核。"]

    assert validate_evaluation(result)["recommendation"]["screening_bucket"] == "review"


def weighted_config():
    return {
        "weights": {
            "resume_quality": {
                "information_completeness": 6,
                "structure_readability": 5,
                "experience_credibility": 9,
                "project_delivery_impact": 18,
                "technical_depth_and_feasibility": 10,
                "education_research_competition_signal": 7,
                "risk_review_signals": 5,
            },
            "jd_company_match": {
                "hard_requirement_match": 8,
                "core_capability_match": 10,
                "jd_relevant_project_match": 14,
                "domain_industry_relevance": 4,
                "seniority_match": 3,
                "interview_validation_value": 1,
            },
        }
    }


def weighted_result():
    result = deepcopy(valid_result())
    result["scores"]["resume_quality"] = 50
    result["scores"]["jd_company_match"] = 32
    result["scores"]["overall"] = 82
    result["scores"]["dimensions"] = [
        {
            "name": "information_completeness",
            "score": 5,
            "max_score": 6,
            "evidence": ["Education and experience are visible."],
            "deductions": [],
        },
        {
            "name": "structure_readability",
            "score": 4,
            "max_score": 5,
            "evidence": ["Resume structure is clear."],
            "deductions": [],
        },
        {
            "name": "experience_credibility",
            "score": 8,
            "max_score": 9,
            "evidence": ["Timeline and ownership are coherent."],
            "deductions": [],
        },
        {
            "name": "project_delivery_impact",
            "score": 15,
            "max_score": 18,
            "evidence": ["Production project delivery and impact metrics are visible."],
            "deductions": [],
        },
        {
            "name": "technical_depth_and_feasibility",
            "score": 9,
            "max_score": 10,
            "evidence": ["Technical approach and responsibilities are concrete."],
            "deductions": [],
        },
        {
            "name": "education_research_competition_signal",
            "score": 4,
            "max_score": 7,
            "evidence": ["Education and research signals support technical depth."],
            "deductions": [],
        },
        {
            "name": "risk_review_signals",
            "score": 5,
            "max_score": 5,
            "evidence": ["No major risk signals."],
            "deductions": [],
        },
        {
            "name": "hard_requirement_match",
            "score": 7,
            "max_score": 8,
            "evidence": ["Hard requirements visibly match."],
            "deductions": [],
        },
        {
            "name": "core_capability_match",
            "score": 8,
            "max_score": 10,
            "evidence": ["Core capability evidence is relevant."],
            "deductions": [],
        },
        {
            "name": "jd_relevant_project_match",
            "score": 12,
            "max_score": 14,
            "evidence": ["Delivered projects align with the JD."],
            "deductions": [],
        },
        {
            "name": "domain_industry_relevance",
            "score": 3,
            "max_score": 4,
            "evidence": ["Domain context is relevant."],
            "deductions": [],
        },
        {
            "name": "seniority_match",
            "score": 2,
            "max_score": 3,
            "evidence": ["Ownership matches seniority."],
            "deductions": [],
        },
        {
            "name": "interview_validation_value",
            "score": 0,
            "max_score": 1,
            "evidence": ["Interview validation points are useful."],
            "deductions": [],
        },
    ]
    return result


def test_configured_weight_dimensions_pass():
    assert validate_evaluation(weighted_result(), weighted_config())["scores"]["overall"] == 82


def test_configured_weight_dimensions_reject_unexpected_dimension():
    result = weighted_result()
    result["scores"]["dimensions"][0]["name"] = "arbitrary_dimension"

    with pytest.raises(ValidationError, match="unexpected dimension"):
        validate_evaluation(result, weighted_config())


def test_configured_weight_dimensions_reject_wrong_max_score():
    result = weighted_result()
    result["scores"]["dimensions"][0]["max_score"] = 11

    with pytest.raises(ValidationError, match="configured weight"):
        validate_evaluation(result, weighted_config())


def test_configured_weight_dimensions_reject_sum_mismatch():
    result = weighted_result()
    result["scores"]["dimensions"][0]["score"] = 4

    with pytest.raises(ValidationError, match="resume_quality"):
        validate_evaluation(result, weighted_config())


def test_top_level_evidence_must_be_list():
    result = deepcopy(valid_result())
    result["evidence"] = "not a list"

    with pytest.raises(ValidationError, match="evidence"):
        validate_evaluation(result)


def test_top_level_strengths_must_be_list():
    result = deepcopy(valid_result())
    result["strengths"] = "not a list"

    with pytest.raises(ValidationError, match="strengths"):
        validate_evaluation(result)


def test_compliance_manual_review_required_must_be_list():
    result = deepcopy(valid_result())
    result["compliance"]["manual_review_required"] = "not a list"

    with pytest.raises(ValidationError, match="manual_review_required"):
        validate_evaluation(result)


def test_missing_dimension_score_fails():
    result = deepcopy(valid_result())
    del result["scores"]["dimensions"][0]["score"]

    with pytest.raises(ValidationError, match="score|missing required key"):
        validate_evaluation(result)


def test_dimension_score_above_max_fails():
    result = deepcopy(valid_result())
    result["scores"]["dimensions"][0]["score"] = 999
    result["scores"]["dimensions"][0]["max_score"] = 10

    with pytest.raises(ValidationError, match="dimension|score"):
        validate_evaluation(result)


def test_dimension_max_score_must_be_positive():
    result = deepcopy(valid_result())
    result["scores"]["dimensions"][0]["max_score"] = 0

    with pytest.raises(ValidationError, match="max_score"):
        validate_evaluation(result)


def test_dimension_without_evidence_or_deduction_fails():
    result = deepcopy(valid_result())
    result["scores"]["dimensions"][0]["evidence"] = []
    result["scores"]["dimensions"][0]["deductions"] = []

    with pytest.raises(ValidationError, match="dimension evidence"):
        validate_evaluation(result)


def test_dimension_evidence_must_be_list():
    result = deepcopy(valid_result())
    result["scores"]["dimensions"][0]["evidence"] = "Built production API services."

    with pytest.raises(ValidationError, match="evidence"):
        validate_evaluation(result)


def test_dimension_deductions_must_be_list():
    result = deepcopy(valid_result())
    result["scores"]["dimensions"][0]["deductions"] = "No deduction."

    with pytest.raises(ValidationError, match="deductions"):
        validate_evaluation(result)


def test_resume_plus_jd_score_must_add_up():
    result = deepcopy(valid_result())
    result["scores"]["overall"] = 90

    with pytest.raises(ValidationError, match="overall"):
        validate_evaluation(result)


def test_nan_score_fails():
    result = deepcopy(valid_result())
    result["scores"]["score_basis"] = "resume_quality_only"
    result["scores"]["jd_company_match"] = None
    result["scores"]["overall"] = float("nan")

    with pytest.raises(ValidationError, match="overall|number|range"):
        validate_evaluation(result)


def test_infinite_score_fails():
    result = deepcopy(valid_result())
    result["scores"]["overall"] = float("inf")

    with pytest.raises(ValidationError, match="overall|finite|number"):
        validate_evaluation(result)


def test_nan_confidence_fails():
    result = deepcopy(valid_result())
    result["inferred_profile"]["confidence"] = float("nan")

    with pytest.raises(ValidationError, match="confidence"):
        validate_evaluation(result)


def test_resume_quality_only_score_requires_null_match():
    result = deepcopy(valid_result())
    result["scores"]["score_basis"] = "resume_quality_only"
    result["scores"]["resume_quality"] = 48
    result["scores"]["overall"] = 80
    result["scores"]["jd_company_match"] = 10

    with pytest.raises(ValidationError, match="jd_company_match"):
        validate_evaluation(result)


def test_resume_quality_only_with_null_match_passes():
    result = deepcopy(valid_result())
    result["scores"]["score_basis"] = "resume_quality_only"
    result["scores"]["resume_quality"] = 48
    result["scores"]["overall"] = 80
    result["scores"]["jd_company_match"] = None

    assert validate_evaluation(result)["scores"]["jd_company_match"] is None


def test_resume_quality_only_overall_must_be_normalized():
    result = deepcopy(valid_result())
    result["scores"]["score_basis"] = "resume_quality_only"
    result["scores"]["resume_quality"] = 48
    result["scores"]["overall"] = 81
    result["scores"]["jd_company_match"] = None

    with pytest.raises(ValidationError, match="overall"):
        validate_evaluation(result)


def test_sensitive_information_can_only_live_in_compliance_fields():
    data = valid_result()
    data["compliance"]["sensitive_or_irrelevant_information"] = ["年龄: 28"]
    data["compliance"]["must_not_use_for_screening"] = ["年龄"]

    assert validate_evaluation(data)["compliance"]["must_not_use_for_screening"] == ["年龄"]
