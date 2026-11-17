import io
import json
import sys
from pathlib import Path

import pytest

import hr_recruitment_onboarding_skill.main as cli


REQUEST = {
    "mode": "generate_jd",
    "job_id": "JOB-2026-001",
    "job_title": "Java开发工程师",
    "department": "研发部",
    "location": "青岛",
    "description": "本科以上，3年以上Java开发经验，熟悉Spring Boot、MySQL和Redis。",
}


def _assert_single_json_object(captured, expected_success: bool) -> dict:
    assert captured.err == ""
    assert captured.out.count("\n") == 1
    response = json.loads(captured.out)
    assert isinstance(response, dict)
    assert response["success"] is expected_success
    return response


def test_json_argument_prints_exactly_one_canonical_success_object(
    tmp_path, monkeypatch, capsys
):
    monkeypatch.setenv("OPIE_WORKSPACE", str(tmp_path))

    exit_code = cli.main(["--json", json.dumps(REQUEST, ensure_ascii=False)])

    response = _assert_single_json_object(capsys.readouterr(), True)
    assert exit_code == 0
    assert "Java开发工程师" in json.dumps(response, ensure_ascii=False)
    assert response["mode"] == "generate_jd"
    assert response["data"]["generation_source"] == "rules_fallback"
    assert response["generated_files"] == [
        "hr_recruitment_data/positions/JOB-2026-001/position.json",
        "hr_recruitment_data/positions/JOB-2026-001/jd.md",
        "hr_recruitment_data/positions/JOB-2026-001/talent_pool.json",
    ]


def test_request_file_input_prints_one_json_object(tmp_path, monkeypatch, capsys):
    workspace = tmp_path / "workspace"
    request_path = tmp_path / "request.json"
    request_path.write_text(json.dumps(REQUEST, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setenv("OPIE_WORKSPACE", str(workspace))

    exit_code = cli.main(["--request", str(request_path)])

    _assert_single_json_object(capsys.readouterr(), True)
    assert exit_code == 0


def test_stdin_input_prints_one_json_object(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("OPIE_WORKSPACE", str(tmp_path))
    monkeypatch.setattr(
        sys, "stdin", io.StringIO(json.dumps(REQUEST, ensure_ascii=False))
    )

    exit_code = cli.main([])

    _assert_single_json_object(capsys.readouterr(), True)
    assert exit_code == 0


def test_duplicate_is_one_chinese_json_error_and_does_not_change_files(
    tmp_path, monkeypatch, capsys
):
    monkeypatch.setenv("OPIE_WORKSPACE", str(tmp_path))
    arguments = ["--json", json.dumps(REQUEST, ensure_ascii=False)]
    assert cli.main(arguments) == 0
    _assert_single_json_object(capsys.readouterr(), True)
    data_root = tmp_path / "hr_recruitment_data"
    before = {
        path.relative_to(data_root).as_posix(): path.read_bytes()
        for path in data_root.rglob("*")
        if path.is_file()
    }

    exit_code = cli.main(arguments)

    response = _assert_single_json_object(capsys.readouterr(), False)
    after = {
        path.relative_to(data_root).as_posix(): path.read_bytes()
        for path in data_root.rglob("*")
        if path.is_file()
    }
    assert exit_code == 1
    assert response["error_code"] == "DUPLICATE_JOB_ID"
    assert response["message"] == "职位编号 JOB-2026-001 已存在。"
    assert after == before


@pytest.mark.parametrize(
    "arguments,input_text",
    [
        (["--json", "{bad json"], ""),
        (["--request", "missing.json"], ""),
        (["--json", "{}"], ""),
        (["--request", "one.json", "--json", "{}"], ""),
    ],
)
def test_expected_input_errors_are_one_json_object(
    tmp_path, monkeypatch, capsys, arguments, input_text
):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "stdin", io.StringIO(input_text))

    exit_code = cli.main(arguments)

    response = _assert_single_json_object(capsys.readouterr(), False)
    assert exit_code == 1
    assert response["error_code"] != "INTERNAL_ERROR"


def test_unexpected_exception_is_one_sanitized_json_object(
    monkeypatch, capsys
):
    def fail_to_build(project_root: Path):
        raise RuntimeError("top-secret internal detail")

    monkeypatch.setattr(cli, "build_service", fail_to_build)

    exit_code = cli.main(["--json", json.dumps(REQUEST, ensure_ascii=False)])

    captured = capsys.readouterr()
    response = _assert_single_json_object(captured, False)
    assert exit_code == 1
    assert response["error_code"] == "INTERNAL_ERROR"
    assert "top-secret" not in captured.out


def test_invalid_argument_error_message_is_chinese_only(capsys):
    exit_code = cli.main(["--request"])

    response = _assert_single_json_object(capsys.readouterr(), False)
    assert exit_code == 1
    assert response["error_code"] == "INVALID_ARGUMENT"
    assert response["message"] == "命令行参数无效。"
