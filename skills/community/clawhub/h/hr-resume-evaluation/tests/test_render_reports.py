import copy
import csv

from scripts.render_reports import (
    render_candidate_report,
    render_csv_summary,
    render_summary_report,
)


def sample_result(candidate_id="alice"):
    return {
        "candidate_id": candidate_id,
        "file_name": f"{candidate_id}.md",
        "report_path": "",
        "inferred_profile": {
            "role_family": "engineering",
            "seniority": "mid",
            "domain_context": "backend services",
            "confidence": 0.8,
        },
        "scores": {
            "score_basis": "resume_plus_jd_company",
            "overall": 80,
            "resume_quality": 50,
            "jd_company_match": 30,
            "dimensions": [
                {
                    "name": "工程交付",
                    "score": 20,
                    "max_score": 25,
                    "evidence": ["负责后端服务交付。"],
                    "deductions": ["缺少规模化指标。"],
                }
            ],
        },
        "evidence": ["简历体现 Python 和 API 项目经验。"],
        "deductions": ["云平台深度证据不足。"],
        "strengths": ["后端实现经验清晰。"],
        "concerns": ["需要验证分布式系统深度。"],
        "interview_validation_points": ["追问 API 稳定性 ownership。"],
        "compliance": {
            "sensitive_or_irrelevant_information": ["年龄：32"],
            "must_not_use_for_screening": ["年龄"],
            "manual_review_required": ["出现敏感或无关信息，需要人工复核。"],
            "no_auto_reject_reasons": ["报告仅作为人工复核参考。"],
        },
        "recommendation": {
            "screening_bucket": "review",
            "summary": "相关经验较匹配，建议复核。",
            "next_steps": ["招聘专员复核"],
        },
    }


def test_render_candidate_report_contains_scores_and_compliance(tmp_path):
    report_path = render_candidate_report(sample_result(), tmp_path)

    content = report_path.read_text(encoding="utf-8")

    assert "总分" in content
    assert "score_basis" in content
    assert "resume_plus_jd_company" in content
    assert "不得作为筛选依据" in content
    assert "年龄" in content


def test_render_summary_report_lists_candidate(tmp_path):
    report_path = render_summary_report([sample_result()], [], tmp_path)

    content = report_path.read_text(encoding="utf-8")

    assert "批量简历评估汇总" in content
    assert "alice" in content
    assert "review" in content


def test_render_summary_report_includes_batch_aggregations(tmp_path):
    alice = sample_result("alice")
    bob = sample_result("bob")
    bob["inferred_profile"]["role_family"] = "sales"
    bob["scores"]["overall"] = 72
    bob["scores"]["resume_quality"] = 42
    bob["scores"]["jd_company_match"] = 30
    bob["concerns"] = ["Needs metric verification."]
    alice["concerns"] = ["Needs metric verification.", "Clarify ownership scope."]

    report_path = render_summary_report([alice, bob], [], tmp_path)

    content = report_path.read_text(encoding="utf-8")

    assert "total_evaluated: 2" in content
    assert "jd_company_matching_count: 2" in content
    assert "80-89: 1" in content
    assert "70-79: 1" in content
    assert "engineering: 1" in content
    assert "sales: 1" in content
    assert "Needs metric verification.: 2" in content


def test_render_summary_report_counts_failures_in_total_evaluated(tmp_path):
    report_path = render_summary_report(
        [sample_result()],
        [{"candidate_id": "empty", "file_name": "empty.txt", "error": "empty_text"}],
        tmp_path,
    )

    content = report_path.read_text(encoding="utf-8")

    assert "total_evaluated: 2" in content
    assert "成功数量：1" in content
    assert "失败数量：1" in content


def test_render_csv_summary_has_expected_columns(tmp_path):
    report_path = render_csv_summary([sample_result()], tmp_path)

    content = report_path.read_text(encoding="utf-8-sig")

    assert "candidate_id,file_name,score_basis" in content
    assert "alice,alice.md,resume_plus_jd_company" in content


def test_candidate_report_uses_safe_filename_inside_output_dir(tmp_path):
    output_dir = tmp_path / "reports"
    outside_path = tmp_path / "outside.md"

    report_path = render_candidate_report(sample_result("../outside"), output_dir)

    assert report_path.resolve().parent == output_dir.resolve()
    assert not outside_path.exists()


def test_render_candidate_report_does_not_mutate_input(tmp_path):
    result = sample_result()
    original = copy.deepcopy(result)

    render_candidate_report(result, tmp_path)

    assert result == original


def test_summary_table_escapes_markdown_cells(tmp_path):
    result = sample_result()
    result["inferred_profile"]["role_family"] = "A|B\nC"

    report_path = render_summary_report([result], [], tmp_path)
    content = report_path.read_text(encoding="utf-8")

    assert "A|B\nC" not in content
    assert "A\\|B C" in content


def test_csv_escapes_formula_values_and_has_bom(tmp_path):
    result = sample_result()
    result["file_name"] = "@resume.md"
    result["strengths"] = ["=SUM(1,1)"]
    result["concerns"] = ["+cmd"]
    result["compliance"]["manual_review_required"] = ["-risk"]

    report_path = render_csv_summary([result], tmp_path)

    raw_content = report_path.read_bytes()
    content = report_path.read_text(encoding="utf-8-sig")

    assert raw_content.startswith(b"\xef\xbb\xbf")
    assert "'=SUM(1,1)" in content
    assert "'+cmd" in content
    assert "'-risk" in content
    assert "'@resume.md" in content


def test_csv_escapes_whitespace_prefixed_formula_values(tmp_path):
    result = sample_result()
    result["strengths"] = ["\t=SUM(1,1)"]
    result["concerns"] = [" =SUM(1,1)"]

    report_path = render_csv_summary([result], tmp_path)

    content = report_path.read_text(encoding="utf-8-sig")

    assert "'\t=SUM(1,1)" in content
    assert "' =SUM(1,1)" in content


def test_csv_escapes_control_prefixed_formula_values(tmp_path):
    result = sample_result()
    result["strengths"] = ["\x00=SUM(1,1)"]
    result["concerns"] = ['\x1b@HYPERLINK("x")']

    report_path = render_csv_summary([result], tmp_path)

    with report_path.open(encoding="utf-8-sig", newline="") as handle:
        row = next(csv.DictReader(handle))

    assert row["top_strengths"] == "'\x00=SUM(1,1)"
    assert row["top_concerns"] == "'\x1b@HYPERLINK(\"x\")"


def test_csv_escapes_del_and_c1_control_prefixed_formula_values(tmp_path):
    result = sample_result()
    result["strengths"] = ["\x7f=SUM(1,1)"]
    result["concerns"] = ["\x85+1"]

    report_path = render_csv_summary([result], tmp_path)

    with report_path.open(encoding="utf-8-sig", newline="") as handle:
        row = next(csv.DictReader(handle))

    assert row["top_strengths"] == "'\x7f=SUM(1,1)"
    assert row["top_concerns"] == "'\x85+1"


def test_csv_ignores_preexisting_report_path(tmp_path):
    result = sample_result("folder/evil")
    result["file_name"] = "source.md"
    result["report_path"] = "../bad.md"

    report_path = render_csv_summary([result], tmp_path)

    with report_path.open(encoding="utf-8-sig", newline="") as handle:
        row = next(csv.DictReader(handle))

    assert row["report_path"] == "folder-evil.md"
    assert row["report_path"] != "../bad.md"


def test_summary_report_ignores_preexisting_report_path(tmp_path):
    result = sample_result("folder/evil")
    result["file_name"] = "source.md"
    result["report_path"] = "../bad.md"

    report_path = render_summary_report([result], [], tmp_path)

    content = report_path.read_text(encoding="utf-8")

    assert "folder-evil.md" in content
    assert "../bad.md" not in content
