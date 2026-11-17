import re

from .exceptions import HRSkillError


JOB_ID_PATTERN = re.compile(r"^JOB-\d{4}-\d{3}$")
REQUIRED_FIELDS = ("mode", "job_id", "job_title", "department", "location", "description")


def validate_generate_jd_request(payload: dict) -> dict:
    """Validate and normalize a generate-JD request."""
    if not isinstance(payload, dict):
        raise HRSkillError("INVALID_REQUEST", "请求必须是 JSON 对象。")

    job_id = str(payload.get("job_id", "")).strip()
    if job_id and not JOB_ID_PATTERN.fullmatch(job_id):
        raise HRSkillError("INVALID_JOB_ID", "职位编号必须符合 JOB-YYYY-NNN 格式。")

    missing = [key for key in REQUIRED_FIELDS if not str(payload.get(key, "")).strip()]
    if missing:
        raise HRSkillError("MISSING_REQUIRED_FIELD", f"缺少必填字段：{', '.join(missing)}。")

    if payload["mode"] != "generate_jd":
        raise HRSkillError("UNSUPPORTED_MODE", "当前仅支持 generate_jd 模式。")

    return {key: str(payload[key]).strip() for key in REQUIRED_FIELDS}
