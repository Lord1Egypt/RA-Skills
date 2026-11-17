from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SKILL_DIR = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = SKILL_DIR / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from common import (  # noqa: E402
    DEFAULT_CV_LIMITS,
    OUTPUT_DIR,
    SKILL_DIR as COMMON_SKILL_DIR,
    ValidationError,
    load_application_content,
    load_json,
    validate_cv_selection,
)
from generate_cv_selection import build_selection  # noqa: E402
from validate_application import PdfInspection, PdfInspectionError, validate_application  # noqa: E402

PROFILE_DIR = SKILL_DIR / "assets" / "profile"
EXAMPLES_DIR = SKILL_DIR / "examples"


def run_script(name: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / name), *args],
        cwd=SKILL_DIR,
        text=True,
        capture_output=True,
        check=False,
    )


def base_selection() -> dict:
    return {
        "schema_version": 2,
        "target_title": "Basisrolle",
        "language": "de",
        "about_me": "Basistext.",
        "limits": dict(DEFAULT_CV_LIMITS),
        "skills": ["delivery"],
        "experience": ["brightworks-analyst"],
        "education": ["bsc-business-informatics"],
        "projects": ["cloud-automation-dashboard"],
        "languages": ["fr"],
    }


def fake_inspector(*, cv_pages: int = 1, cv_text: str = "Mira Hoffmann", cv_words=None,
                   cover_text: str = "Bewerbung"):
    words = cv_words or [(30.0, 100.0, 80.0, 700.0, "Mira")]

    def inspect(path: Path) -> PdfInspection:
        if path.name == "CV.pdf":
            return PdfInspection(path, cv_pages, cv_text, 595.0, 800.0, words)
        return PdfInspection(path, 1, cover_text, 595.0, 800.0, [(30.0, 100.0, 80.0, 300.0, "Cover")])

    return inspect


def make_pdf_placeholders(app_dir: Path) -> None:
    (app_dir / "CV.pdf").write_bytes(b"%PDF-test")
    (app_dir / "cover_letter.pdf").write_bytes(b"%PDF-test")


def test_selection_limits_and_v1_defaults() -> None:
    job = load_json(EXAMPLES_DIR / "job.json")
    expanded = build_selection(job, PROFILE_DIR, {**DEFAULT_CV_LIMITS, "skills": 6}, None, "adaptive", None)
    assert expanded["schema_version"] == 2
    assert len(expanded["skills"]) == 6
    assert expanded["limits"]["skills"] == 6
    v1 = dict(expanded)
    v1.pop("schema_version")
    v1.pop("limits")
    assert validate_cv_selection(v1, PROFILE_DIR)["limits"] == DEFAULT_CV_LIMITS
    with pytest.raises(ValidationError, match="Unknown IDs"):
        validate_cv_selection({**expanded, "skills": ["not-a-profile-id"]}, PROFILE_DIR)
    with pytest.raises(ValidationError, match="non-negative"):
        validate_cv_selection({**expanded, "limits": {"skills": -1}}, PROFILE_DIR)


def test_default_output_directory_is_outside_the_installed_skill() -> None:
    assert COMMON_SKILL_DIR not in OUTPUT_DIR.parents


def test_selector_cli_records_supplied_limits(tmp_path: Path) -> None:
    limits = tmp_path / "limits.json"
    output = tmp_path / "cv_selection.json"
    limits.write_text(json.dumps({"limits": {"skills": 6}}), encoding="utf-8")
    completed = run_script(
        "generate_cv_selection.py", "--job", str(EXAMPLES_DIR / "job.json"), "--limits", str(limits),
        "--output", str(output), "--profile-dir", str(PROFILE_DIR),
    )
    assert completed.returncode == 0, completed.stderr
    assert load_json(output)["limits"]["skills"] == 6


def test_base_selection_strict_and_adaptive(tmp_path: Path) -> None:
    base_path = tmp_path / "base-cv_selection.json"
    base_path.write_text(json.dumps(base_selection()), encoding="utf-8")
    job = {"role": "Python Consultant", "language": "de", "description": "Python automation"}
    base = validate_cv_selection(load_json(base_path), PROFILE_DIR)
    strict = build_selection(job, PROFILE_DIR, base["limits"], base, "strict", base_path)
    assert strict["skills"] == ["delivery"]
    assert strict["target_title"] == "Python Consultant"
    assert strict["derived_from"]["path"] == str(base_path.resolve())
    adaptive = build_selection(job, PROFILE_DIR, base["limits"], base, "adaptive", base_path)
    assert adaptive["skills"][0] == "python"
    assert "delivery" in adaptive["skills"]


def test_prepare_rejects_invalid_base_without_new_folder(tmp_path: Path) -> None:
    broken = tmp_path / "broken-base"
    broken.mkdir()
    (broken / "cv_selection.json").write_text("{}", encoding="utf-8")
    output_root = tmp_path / "applications"
    completed = run_script(
        "prepare_application.py", "--slug", "2026-10-example-role", "--output-root", str(output_root),
        "--base-application", str(broken), "--profile-dir", str(PROFILE_DIR),
    )
    assert completed.returncode != 0
    assert not (output_root / "2026-10-example-role").exists()


def test_canonical_content_and_legacy_adapters_generate_sources(tmp_path: Path) -> None:
    canonical = EXAMPLES_DIR / "application_content.json"
    cover_tex, plain_text = tmp_path / "cover_letter.tex", tmp_path / "indeed_text.txt"
    cover = run_script("generate_cover_letter.py", "--content", str(canonical), "--output", str(cover_tex),
                       "--profile", str(PROFILE_DIR / "master_profile.json"))
    plain = run_script("generate_plain_text.py", "--content", str(canonical), "--output", str(plain_text),
                       "--profile", str(PROFILE_DIR / "master_profile.json"))
    assert cover.returncode == 0, cover.stderr
    assert plain.returncode == 0, plain.stderr
    assert "__" not in cover_tex.read_text(encoding="utf-8")
    assert "Mit freundlichen Grüßen" in plain_text.read_text(encoding="utf-8")

    legacy_cover = run_script(
        "generate_cover_letter.py", "--content", str(EXAMPLES_DIR / "cover_letter.json"),
        "--output", str(tmp_path / "legacy-cover.tex"), "--profile", str(PROFILE_DIR / "master_profile.json"),
    )
    legacy_plain = run_script(
        "generate_plain_text.py", "--content", str(EXAMPLES_DIR / "indeed_text.json"),
        "--output", str(tmp_path / "legacy-plain.txt"), "--profile", str(PROFILE_DIR / "master_profile.json"),
    )
    assert legacy_cover.returncode == 0, legacy_cover.stderr
    assert legacy_plain.returncode == 0, legacy_plain.stderr

    legacy = run_script(
        "convert_application_content.py", "--cover-letter", str(EXAMPLES_DIR / "cover_letter.json"),
        "--indeed-text", str(EXAMPLES_DIR / "indeed_text.json"), "--job", str(EXAMPLES_DIR / "job.json"),
        "--profile", str(PROFILE_DIR / "master_profile.json"), "--output", str(tmp_path / "application_content.json"),
    )
    assert legacy.returncode == 0, legacy.stderr
    converted = load_application_content(tmp_path / "application_content.json", load_json(PROFILE_DIR / "master_profile.json"))
    assert converted["schema_version"] == 2


def test_cover_generator_refuses_bundled_profile_for_external_content(tmp_path: Path) -> None:
    content = tmp_path / "application_content.json"
    shutil.copyfile(EXAMPLES_DIR / "application_content.json", content)
    completed = run_script(
        "generate_cover_letter.py", "--content", str(content),
        "--output", str(tmp_path / "cover_letter.tex"),
    )
    assert completed.returncode != 0
    assert "bundled example profile" in completed.stderr


def test_validator_detects_cover_letter_header_profile_mismatch(tmp_path: Path) -> None:
    make_pdf_placeholders(tmp_path)
    shutil.copyfile(EXAMPLES_DIR / "application_content.json", tmp_path / "application_content.json")
    subject = load_json(EXAMPLES_DIR / "application_content.json")["cover_letter"]["subject"]
    matching_header = (
        "Mira Hoffmann mira.hoffmann@example.com +49 30 00000000 "
        f"Berlin, Deutschland {subject}"
    )
    matching = validate_application(
        tmp_path, PROFILE_DIR,
        inspector=fake_inspector(cv_text="Mira Hoffmann", cover_text=matching_header),
    )
    assert matching.ok
    mismatching_header = f"Example Candidate example@example.com +49 1 234 Berlin {subject}"
    mismatching = validate_application(
        tmp_path, PROFILE_DIR,
        inspector=fake_inspector(cv_text="Mira Hoffmann", cover_text=mismatching_header),
    )
    assert any("cover-letter header" in error for error in mismatching.errors)


def test_canonical_content_rejects_repeated_company_in_address_block(tmp_path: Path) -> None:
    content = load_json(EXAMPLES_DIR / "application_content.json")
    content["job"]["company"] = "Example Co"
    content["cover_letter"]["recipient"] = "Example Co Hiring Team"
    content_path = tmp_path / "duplicate-recipient.json"
    content_path.write_text(json.dumps(content), encoding="utf-8")
    with pytest.raises(ValidationError, match="recipient must not repeat"):
        load_application_content(content_path, load_json(PROFILE_DIR / "master_profile.json"))

    content["cover_letter"]["recipient"] = "Hiring Team"
    content["cover_letter"]["company_address"] = ["Example Co", "Remote"]
    content_path.write_text(json.dumps(content), encoding="utf-8")
    with pytest.raises(ValidationError, match="company_address must not repeat"):
        load_application_content(content_path, load_json(PROFILE_DIR / "master_profile.json"))


def test_invalid_canonical_content_fails_with_a_specific_error(tmp_path: Path) -> None:
    invalid = {"schema_version": 2, "job": {}, "cover_letter": {}, "plain_text": {}}
    path = tmp_path / "invalid.json"
    path.write_text(json.dumps(invalid), encoding="utf-8")
    completed = run_script("generate_plain_text.py", "--content", str(path), "--output", str(tmp_path / "out.txt"),
                           "--profile", str(PROFILE_DIR / "master_profile.json"))
    assert completed.returncode != 0
    assert "job.company" in completed.stderr


def test_validator_success_and_each_failure_class(tmp_path: Path) -> None:
    make_pdf_placeholders(tmp_path)
    success = validate_application(tmp_path, PROFILE_DIR, inspector=fake_inspector())
    assert success.ok

    multiple_pages = validate_application(tmp_path, PROFILE_DIR, inspector=fake_inspector(cv_pages=2))
    assert any("exactly one page" in error for error in multiple_pages.errors)

    placeholders = validate_application(tmp_path, PROFILE_DIR, inspector=fake_inspector(cv_text="TODO replace me"))
    assert any("placeholder" in error for error in placeholders.errors)

    overflow = validate_application(
        tmp_path, PROFILE_DIR,
        inspector=fake_inspector(cv_words=[(20.0, 100.0, 80.0, 900.0, "overflow")]),
    )
    assert any("outside the page bounds" in error for error in overflow.errors)

    sparse = validate_application(
        tmp_path, PROFILE_DIR,
        strict_fill=True,
        inspector=fake_inspector(cv_words=[(20.0, 100.0, 80.0, 200.0, "sparse")]),
    )
    assert any("below" in error for error in sparse.errors)

    (tmp_path / "cv_selection.json").write_text(json.dumps({"schema_version": 2}), encoding="utf-8")
    invalid_schema = validate_application(tmp_path, PROFILE_DIR, inspector=fake_inspector())
    assert any("Input validation failed" in error for error in invalid_schema.errors)


def test_validator_detects_missing_pdfs(tmp_path: Path) -> None:
    report = validate_application(tmp_path, PROFILE_DIR)
    assert "Expected PDF is missing: CV.pdf" in report.errors
    assert "Expected PDF is missing: cover_letter.pdf" in report.errors


def test_validator_reports_missing_pdf_tools_without_success(tmp_path: Path) -> None:
    make_pdf_placeholders(tmp_path)

    def unavailable(_: Path) -> PdfInspection:
        raise PdfInspectionError("PDF validation requires Poppler tools on PATH: pdftotext")

    report = validate_application(tmp_path, PROFILE_DIR, inspector=unavailable)
    assert not report.ok
    assert any("Poppler" in error for error in report.errors)


def test_bundled_pdf_regression_when_poppler_is_available(tmp_path: Path) -> None:
    if not shutil.which("pdfinfo") or not shutil.which("pdftotext"):
        pytest.skip("Poppler is not installed")
    shutil.copyfile(EXAMPLES_DIR / "generated" / "CV-example.pdf", tmp_path / "CV.pdf")
    shutil.copyfile(EXAMPLES_DIR / "generated" / "cover-letter-example.pdf", tmp_path / "cover_letter.pdf")
    report = validate_application(tmp_path, PROFILE_DIR)
    assert report.ok, report.errors
