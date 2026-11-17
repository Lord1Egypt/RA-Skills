import pytest

from hr_recruitment_onboarding_skill.app.exceptions import HRSkillError
from hr_recruitment_onboarding_skill.app.result import error_response, success_response
from hr_recruitment_onboarding_skill.app.validation import validate_generate_jd_request


def test_accepts_complete_request():
    request = validate_generate_jd_request(
        {
            "mode": "generate_jd",
            "job_id": "JOB-2026-001",
            "job_title": "Java开发工程师",
            "department": "研发部",
            "location": "青岛",
            "description": "3年以上 Java 开发经验",
        }
    )

    assert request["job_id"] == "JOB-2026-001"


def test_rejects_invalid_job_id():
    with pytest.raises(HRSkillError) as exc:
        validate_generate_jd_request({"mode": "generate_jd", "job_id": "java-1"})

    assert exc.value.code == "INVALID_JOB_ID"


def test_success_response_uses_the_canonical_shape():
    data = {"job_id": "JOB-2026-001"}
    generated_files = ["positions/JOB-2026-001/position.json"]
    warnings = ["请 HR 核对结果"]

    response = success_response("generate_jd", "职位已创建", data, generated_files, warnings)

    assert response == {
        "success": True,
        "mode": "generate_jd",
        "message": "职位已创建",
        "data": data,
        "generated_files": generated_files,
        "warnings": warnings,
    }


def test_error_response_uses_error_contract():
    error = HRSkillError("INVALID_JOB_ID", "职位编号格式无效", {"job_id": "java-1"})

    response = error_response(error, "generate_jd")

    assert response == {
        "success": False,
        "mode": "generate_jd",
        "error_code": "INVALID_JOB_ID",
        "message": "职位编号格式无效",
        "details": {"job_id": "java-1"},
    }
