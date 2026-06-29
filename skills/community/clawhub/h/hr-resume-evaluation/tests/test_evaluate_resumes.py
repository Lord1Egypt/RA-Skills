import csv
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from scripts.evaluate_resumes import _parser
from scripts.evaluate_resumes import run_batch


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def fake_model_result(candidate_id):
    return {
        "candidate_id": candidate_id,
        "inferred_profile": {
            "role_family": "Sales and Business",
            "seniority": "mid",
            "domain_context": "enterprise sales",
            "confidence": 0.85,
        },
        "scores": {
            "score_basis": "resume_quality_only",
            "overall": 80,
            "resume_quality": 48,
            "jd_company_match": None,
            "dimensions": [
                {
                    "name": "achievement_impact",
                    "score": 12,
                    "max_score": 15,
                    "evidence": ["delivered revenue growth"],
                    "deductions": [],
                }
            ],
        },
        "evidence": ["delivered revenue growth"],
        "deductions": [],
        "strengths": ["Clear evidence of revenue impact."],
        "concerns": ["Validate sales cycle ownership."],
        "interview_validation_points": ["Ask for quota attainment details."],
        "compliance": {
            "sensitive_or_irrelevant_information": [],
            "must_not_use_for_screening": [],
            "manual_review_required": [],
            "no_auto_reject_reasons": ["Use only as recruiter review support."],
        },
        "recommendation": {
            "screening_bucket": "review",
            "summary": "Review recommended based on resume evidence.",
            "next_steps": ["Recruiter review"],
        },
    }


def test_run_batch_generates_reports_without_jd(tmp_path):
    resumes_dir = tmp_path / "resumes"
    output_dir = tmp_path / "reports"
    config_path = tmp_path / "evaluation.yaml"
    resumes_dir.mkdir()
    (resumes_dir / "alice.md").write_text("Alice delivered revenue growth.", encoding="utf-8")
    config_path.write_text("output_language: en\n", encoding="utf-8")

    def fake_evaluator(parsed, jd_text, company_text, evaluation_config, model_config):
        assert jd_text is None
        assert company_text is None
        assert evaluation_config == {"output_language": "en"}
        assert model_config is None
        return fake_model_result(parsed.candidate_id)

    summary = run_batch(
        resumes_dir=resumes_dir,
        output_dir=output_dir,
        evaluation_config_path=config_path,
        evaluator=fake_evaluator,
    )

    assert summary == {"successful": 1, "failed": 0}
    assert (output_dir / "alice.md").exists()
    assert (output_dir / "summary.md").exists()
    assert (output_dir / "summary.csv").exists()


def test_run_batch_retries_validation_failure_and_succeeds(tmp_path):
    resumes_dir = tmp_path / "resumes"
    output_dir = tmp_path / "reports"
    config_path = tmp_path / "evaluation.yaml"
    resumes_dir.mkdir()
    (resumes_dir / "alice.md").write_text("Alice delivered revenue growth.", encoding="utf-8")
    config_path.write_text("max_model_retries: 1\n", encoding="utf-8")
    calls = []

    def fake_evaluator(parsed, jd_text, company_text, evaluation_config, model_config):
        calls.append(parsed.candidate_id)
        result = fake_model_result(parsed.candidate_id)
        if len(calls) == 1:
            result["scores"]["overall"] = 81
        return result

    summary = run_batch(
        resumes_dir=resumes_dir,
        output_dir=output_dir,
        evaluation_config_path=config_path,
        evaluator=fake_evaluator,
    )

    assert summary == {"successful": 1, "failed": 0}
    assert calls == ["alice", "alice"]
    assert (output_dir / "alice.md").exists()


def test_run_batch_applies_recruiter_overrides_before_rendering(tmp_path):
    resumes_dir = tmp_path / "resumes"
    output_dir = tmp_path / "reports"
    config_path = tmp_path / "evaluation.yaml"
    resumes_dir.mkdir()
    (resumes_dir / "alice.md").write_text("Alice delivered revenue growth.", encoding="utf-8")
    config_path.write_text(
        "role_family_override: Technical and Engineering\n"
        "seniority_override: senior\n",
        encoding="utf-8",
    )

    def fake_evaluator(parsed, jd_text, company_text, evaluation_config, model_config):
        result = fake_model_result(parsed.candidate_id)
        result["inferred_profile"]["role_family"] = "Sales and Business"
        result["inferred_profile"]["seniority"] = "junior"
        return result

    summary = run_batch(
        resumes_dir=resumes_dir,
        output_dir=output_dir,
        evaluation_config_path=config_path,
        evaluator=fake_evaluator,
    )

    report_text = (output_dir / "alice.md").read_text(encoding="utf-8")
    with (output_dir / "summary.csv").open(encoding="utf-8-sig", newline="") as handle:
        row = next(csv.DictReader(handle))

    assert summary == {"successful": 1, "failed": 0}
    assert "Technical and Engineering" in report_text
    assert "senior" in report_text
    assert "Sales and Business" not in report_text
    assert "junior" not in report_text
    assert row["role_family"] == "Technical and Engineering"
    assert row["seniority"] == "senior"


def test_run_batch_enforces_configured_dimension_weights(tmp_path):
    resumes_dir = tmp_path / "resumes"
    output_dir = tmp_path / "reports"
    config_path = tmp_path / "evaluation.yaml"
    resumes_dir.mkdir()
    (resumes_dir / "alice.md").write_text("Alice delivered revenue growth.", encoding="utf-8")
    config_path.write_text(
        "\n".join(
            [
                "weights:",
                "  resume_quality:",
                "    information_completeness: 6",
                "    structure_readability: 5",
                "    experience_credibility: 9",
                "    project_delivery_impact: 18",
                "    technical_depth_and_feasibility: 10",
                "    education_research_competition_signal: 7",
                "    risk_review_signals: 5",
                "  jd_company_match:",
                "    hard_requirement_match: 8",
                "    core_capability_match: 10",
                "    jd_relevant_project_match: 14",
                "    domain_industry_relevance: 4",
                "    seniority_match: 3",
                "    interview_validation_value: 1",
            ]
        ),
        encoding="utf-8",
    )

    def fake_evaluator(parsed, jd_text, company_text, evaluation_config, model_config):
        return fake_model_result(parsed.candidate_id)

    summary = run_batch(
        resumes_dir=resumes_dir,
        output_dir=output_dir,
        evaluation_config_path=config_path,
        evaluator=fake_evaluator,
    )

    summary_text = (output_dir / "summary.md").read_text(encoding="utf-8")
    assert summary == {"successful": 0, "failed": 1}
    assert "evaluation_error:ValidationError" in summary_text


def test_run_batch_retries_non_object_model_output_and_succeeds(tmp_path):
    resumes_dir = tmp_path / "resumes"
    output_dir = tmp_path / "reports"
    config_path = tmp_path / "evaluation.yaml"
    resumes_dir.mkdir()
    (resumes_dir / "alice.md").write_text("Alice delivered revenue growth.", encoding="utf-8")
    config_path.write_text("max_model_retries: 1\n", encoding="utf-8")
    calls = []

    def fake_evaluator(parsed, jd_text, company_text, evaluation_config, model_config):
        calls.append(parsed.candidate_id)
        if len(calls) == 1:
            return []
        return fake_model_result(parsed.candidate_id)

    summary = run_batch(
        resumes_dir=resumes_dir,
        output_dir=output_dir,
        evaluation_config_path=config_path,
        evaluator=fake_evaluator,
    )

    assert summary == {"successful": 1, "failed": 0}
    assert calls == ["alice", "alice"]
    assert (output_dir / "alice.md").exists()


def test_run_batch_writes_sanitized_raw_json_when_enabled(tmp_path):
    resumes_dir = tmp_path / "resumes"
    output_dir = tmp_path / "reports"
    config_path = tmp_path / "evaluation.yaml"
    jd_path = tmp_path / "jd.md"
    company_path = tmp_path / "company.md"
    resumes_dir.mkdir()
    (resumes_dir / "alice.md").write_text("Alice delivered revenue growth.", encoding="utf-8")
    jd_path.write_text("Need sales growth ownership.", encoding="utf-8")
    company_path.write_text("Enterprise SaaS company.", encoding="utf-8")
    config_path.write_text("include_raw_json: true\n", encoding="utf-8")

    def fake_evaluator(parsed, jd_text, company_text, evaluation_config, model_config):
        result = fake_model_result(parsed.candidate_id)
        result["api_secret"] = "must not be trusted"
        result["scores"]["score_basis"] = "resume_plus_jd_company"
        result["scores"]["overall"] = 78
        result["scores"]["resume_quality"] = 48
        result["scores"]["jd_company_match"] = 30
        return result

    summary = run_batch(
        resumes_dir=resumes_dir,
        output_dir=output_dir,
        evaluation_config_path=config_path,
        evaluator=fake_evaluator,
        jd_path=jd_path,
        company_path=company_path,
    )

    json_path = output_dir / "alice.json"
    raw_result = json.loads(json_path.read_text(encoding="utf-8"))
    report_text = (output_dir / "alice.md").read_text(encoding="utf-8")

    assert summary == {"successful": 1, "failed": 0}
    assert raw_result["candidate_id"] == "alice"
    assert raw_result["file_name"] == "alice.md"
    assert "api_secret" not in raw_result
    assert raw_result["audit"]["jd_company_context_used"] is True
    datetime.fromisoformat(raw_result["audit"]["evaluation_time"])
    assert "评估时间" in report_text
    assert "是否使用 JD/公司背景：是" in report_text


def test_run_batch_skips_raw_json_when_disabled(tmp_path):
    resumes_dir = tmp_path / "resumes"
    output_dir = tmp_path / "reports"
    config_path = tmp_path / "evaluation.yaml"
    resumes_dir.mkdir()
    (resumes_dir / "alice.md").write_text("Alice delivered revenue growth.", encoding="utf-8")
    config_path.write_text("include_raw_json: false\n", encoding="utf-8")

    def fake_evaluator(parsed, jd_text, company_text, evaluation_config, model_config):
        return fake_model_result(parsed.candidate_id)

    summary = run_batch(
        resumes_dir=resumes_dir,
        output_dir=output_dir,
        evaluation_config_path=config_path,
        evaluator=fake_evaluator,
    )

    assert summary == {"successful": 1, "failed": 0}
    assert (output_dir / "alice.md").exists()
    assert not (output_dir / "alice.json").exists()


def test_run_batch_repeated_validation_failure_is_sanitized(tmp_path):
    resumes_dir = tmp_path / "resumes"
    output_dir = tmp_path / "reports"
    config_path = tmp_path / "evaluation.yaml"
    resumes_dir.mkdir()
    (resumes_dir / "alice.md").write_text("Alice delivered revenue growth.", encoding="utf-8")
    config_path.write_text("max_model_retries: 1\n", encoding="utf-8")
    calls = []

    def fake_evaluator(parsed, jd_text, company_text, evaluation_config, model_config):
        calls.append(parsed.candidate_id)
        result = fake_model_result(parsed.candidate_id)
        result["scores"]["overall"] = 81
        result["evidence"] = ["secret-token resume text"]
        return result

    summary = run_batch(
        resumes_dir=resumes_dir,
        output_dir=output_dir,
        evaluation_config_path=config_path,
        evaluator=fake_evaluator,
    )

    summary_text = (output_dir / "summary.md").read_text(encoding="utf-8")
    assert summary == {"successful": 0, "failed": 1}
    assert calls == ["alice", "alice"]
    assert "evaluation_error:ValidationError" in summary_text
    assert "secret-token" not in summary_text
    assert "resume text" not in summary_text


def test_run_batch_writes_distinct_reports_for_chinese_filenames(tmp_path):
    resumes_dir = tmp_path / "resumes"
    output_dir = tmp_path / "reports"
    config_path = tmp_path / "evaluation.yaml"
    resumes_dir.mkdir()
    (resumes_dir / "张三.md").write_text("Backend API delivery.", encoding="utf-8")
    (resumes_dir / "李四.md").write_text("Sales growth ownership.", encoding="utf-8")
    config_path.write_text("{}\n", encoding="utf-8")

    def fake_evaluator(parsed, jd_text, company_text, evaluation_config, model_config):
        return fake_model_result(parsed.candidate_id)

    summary = run_batch(
        resumes_dir=resumes_dir,
        output_dir=output_dir,
        evaluation_config_path=config_path,
        evaluator=fake_evaluator,
    )

    with (output_dir / "summary.csv").open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    candidate_ids = {row["candidate_id"] for row in rows}
    report_paths = {row["report_path"] for row in rows}
    assert summary == {"successful": 2, "failed": 0}
    assert len(candidate_ids) == 2
    assert len(report_paths) == 2
    assert all((output_dir / report_path).exists() for report_path in report_paths)


def test_run_batch_records_parse_failure(tmp_path):
    resumes_dir = tmp_path / "resumes"
    output_dir = tmp_path / "reports"
    config_path = tmp_path / "evaluation.yaml"
    resumes_dir.mkdir()
    (resumes_dir / "empty.txt").write_text(" \n\t\n", encoding="utf-8")
    config_path.write_text("{}\n", encoding="utf-8")

    def fake_evaluator(parsed, jd_text, company_text, evaluation_config, model_config):
        raise AssertionError("evaluator should not be called for parse failures")

    summary = run_batch(
        resumes_dir=resumes_dir,
        output_dir=output_dir,
        evaluation_config_path=config_path,
        evaluator=fake_evaluator,
    )

    assert summary == {"successful": 0, "failed": 1}
    assert "empty_text" in (output_dir / "summary.md").read_text(encoding="utf-8")


def test_run_batch_sanitizes_parser_exception_details(tmp_path, monkeypatch):
    from scripts import evaluate_resumes
    from scripts.parse_documents import ParsedDocument

    resumes_dir = tmp_path / "resumes"
    output_dir = tmp_path / "reports"
    config_path = tmp_path / "evaluation.yaml"
    resumes_dir.mkdir()
    resume_path = resumes_dir / "broken.pdf"
    resume_path.write_bytes(b"not a real pdf")
    config_path.write_text("{}\n", encoding="utf-8")

    monkeypatch.setattr(evaluate_resumes, "discover_resumes", lambda folder: [resume_path])
    monkeypatch.setattr(
        evaluate_resumes,
        "parse_document",
        lambda path: ParsedDocument(
            path=path,
            file_name="broken.pdf",
            candidate_id="broken",
            text="",
            ok=False,
            error="parse_error: secret-token resume text",
        ),
    )

    def fake_evaluator(parsed, jd_text, company_text, evaluation_config, model_config):
        raise AssertionError("evaluator should not be called for parse failures")

    summary = evaluate_resumes.run_batch(
        resumes_dir=resumes_dir,
        output_dir=output_dir,
        evaluation_config_path=config_path,
        evaluator=fake_evaluator,
    )

    summary_text = (output_dir / "summary.md").read_text(encoding="utf-8")
    assert summary == {"successful": 0, "failed": 1}
    assert "secret-token" not in summary_text
    assert "resume text" not in summary_text
    assert "parse_error" in summary_text
    assert "broken.pdf" in summary_text


def test_run_batch_sanitizes_evaluator_exception(tmp_path):
    resumes_dir = tmp_path / "resumes"
    output_dir = tmp_path / "reports"
    config_path = tmp_path / "evaluation.yaml"
    resumes_dir.mkdir()
    (resumes_dir / "alice.md").write_text("Alice delivered revenue growth.", encoding="utf-8")
    config_path.write_text("{}\n", encoding="utf-8")

    def fake_evaluator(parsed, jd_text, company_text, evaluation_config, model_config):
        raise RuntimeError("secret-token resume text")

    summary = run_batch(
        resumes_dir=resumes_dir,
        output_dir=output_dir,
        evaluation_config_path=config_path,
        evaluator=fake_evaluator,
    )

    summary_text = (output_dir / "summary.md").read_text(encoding="utf-8")
    assert summary == {"successful": 0, "failed": 1}
    assert "secret-token" not in summary_text
    assert "resume text" not in summary_text
    assert "evaluation_error" in summary_text
    assert "RuntimeError" in summary_text


def test_run_batch_mixed_success_failure_counts_and_summary_lists_file(tmp_path):
    resumes_dir = tmp_path / "resumes"
    output_dir = tmp_path / "reports"
    config_path = tmp_path / "evaluation.yaml"
    resumes_dir.mkdir()
    (resumes_dir / "alice.md").write_text("Alice delivered revenue growth.", encoding="utf-8")
    (resumes_dir / "empty.txt").write_text(" \n\t\n", encoding="utf-8")
    config_path.write_text("{}\n", encoding="utf-8")

    def fake_evaluator(parsed, jd_text, company_text, evaluation_config, model_config):
        return fake_model_result(parsed.candidate_id)

    summary = run_batch(
        resumes_dir=resumes_dir,
        output_dir=output_dir,
        evaluation_config_path=config_path,
        evaluator=fake_evaluator,
    )

    assert summary == {"successful": 1, "failed": 1}
    assert "empty.txt" in (output_dir / "summary.md").read_text(encoding="utf-8")


def test_main_returns_nonzero_when_any_failures():
    from scripts.evaluate_resumes import _exit_code

    assert _exit_code({"successful": 1, "failed": 1}) == 1
    assert _exit_code({"successful": 1, "failed": 0}) == 0
    assert _exit_code({"successful": 0, "failed": 0}) == 0


def test_parser_accepts_documented_options():
    args = _parser().parse_args(
        [
            "--resumes",
            "input/resumes",
            "--output",
            "reports",
            "--config",
            "config/evaluation.yaml",
            "--model-config",
            "config/model.yaml",
            "--jd",
            "input/jd.md",
            "--company",
            "input/company.md",
        ]
    )

    assert args.resumes.name == "resumes"
    assert args.output.name == "reports"
    assert args.config.name == "evaluation.yaml"


def test_direct_script_help_runs():
    result = subprocess.run(
        [sys.executable, "scripts/evaluate_resumes.py", "--help"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert "--resumes" in result.stdout
    assert "--output" in result.stdout


def test_role_family_fixtures_exist():
    fixture_dir = Path(__file__).parent / "fixtures" / "role_families"
    expected = {
        "technical.md",
        "sales.md",
        "operations.md",
        "product.md",
        "finance_hr_admin.md",
        "management.md",
    }

    assert {path.name for path in fixture_dir.glob("*.md") if path.name != "资料索引.md"} == expected
