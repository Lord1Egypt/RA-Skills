from pathlib import Path

from scripts.evaluate_resumes import run_batch


JD_TEXT = "# JD\n\nNeed product launch ownership."
COMPANY_TEXT = "# Company\n\nB2B SaaS."


def model_result(parsed, jd, company, evaluation_config, model_config):
    assert jd == JD_TEXT
    assert company == COMPANY_TEXT

    score_basis = "resume_plus_jd_company" if jd or company else "resume_quality_only"

    return {
        "candidate_id": parsed.candidate_id,
        "inferred_profile": {
            "role_family": "Product and Project",
            "seniority": "mid",
            "domain_context": "B2B SaaS",
            "confidence": 0.75,
        },
        "scores": {
            "score_basis": score_basis,
            "overall": 78 if score_basis == "resume_plus_jd_company" else 80,
            "resume_quality": 48,
            "jd_company_match": 30 if score_basis == "resume_plus_jd_company" else None,
            "dimensions": [
                {
                    "name": "capability_clarity",
                    "score": 8,
                    "max_score": 10,
                    "evidence": ["owns launch work"],
                    "deductions": [],
                }
            ],
        },
        "evidence": ["owns launch work"],
        "deductions": [],
        "strengths": ["Owns launch work."],
        "concerns": ["Needs metric verification."],
        "interview_validation_points": ["Verify launch metrics and ownership."],
        "compliance": {
            "sensitive_or_irrelevant_information": [],
            "must_not_use_for_screening": [],
            "manual_review_required": ["needs metric verification"],
            "no_auto_reject_reasons": ["Use only as recruiter review support."],
        },
        "recommendation": {
            "screening_bucket": "review",
            "summary": "Review recommended with metric verification.",
            "next_steps": ["Recruiter validates launch metrics."],
        },
    }


def test_end_to_end_outputs_with_jd_and_company(tmp_path):
    resumes_dir = tmp_path / "resumes"
    output_dir = tmp_path / "output"
    config_path = Path(tmp_path) / "evaluation.yaml"
    jd_path = tmp_path / "jd.md"
    company_path = tmp_path / "company.md"

    resumes_dir.mkdir()
    (resumes_dir / "candidate.md").write_text(
        "Candidate owns B2B SaaS launch work across product and project delivery.",
        encoding="utf-8",
    )
    jd_path.write_text(JD_TEXT, encoding="utf-8")
    company_path.write_text(COMPANY_TEXT, encoding="utf-8")
    config_path.write_text("output_language: zh-CN\n", encoding="utf-8")

    summary = run_batch(
        resumes_dir=resumes_dir,
        output_dir=output_dir,
        evaluation_config_path=config_path,
        evaluator=model_result,
        jd_path=jd_path,
        company_path=company_path,
    )

    assert summary == {"successful": 1, "failed": 0}
    assert "resume_plus_jd_company" in (output_dir / "summary.csv").read_text(
        encoding="utf-8-sig"
    )
    assert "人工复核" in (output_dir / "candidate.md").read_text(encoding="utf-8")
