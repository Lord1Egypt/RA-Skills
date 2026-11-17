from .exceptions import HRSkillError


def success_response(
    mode: str,
    message: str,
    data: object,
    generated_files: list[str],
    warnings: list[str],
) -> dict:
    """Build the JSON contract for a successful skill request."""
    return {
        "success": True,
        "mode": mode,
        "message": message,
        "data": data,
        "generated_files": generated_files,
        "warnings": warnings,
    }


def error_response(error: HRSkillError, mode: str) -> dict:
    """Build the JSON contract for an expected skill error."""
    return {
        "success": False,
        "mode": mode,
        "error_code": error.code,
        "message": error.message,
        "details": error.details,
    }
