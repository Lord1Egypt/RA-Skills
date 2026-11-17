"""JSON-only command-line entry point for position JD creation."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hr_recruitment_onboarding_skill.app.config import Settings
from hr_recruitment_onboarding_skill.app.exceptions import HRSkillError
from hr_recruitment_onboarding_skill.app.file_repository import FileRepository
from hr_recruitment_onboarding_skill.app.result import error_response, success_response
from hr_recruitment_onboarding_skill.app.validation import (
    validate_generate_jd_request,
)
from hr_recruitment_onboarding_skill.app.workspace import WorkspaceManager
from hr_recruitment_onboarding_skill.services.jd_service import JDService
from hr_recruitment_onboarding_skill.services.llm_service import LLMService
from hr_recruitment_onboarding_skill.services.rule_based_extractor import (
    RuleBasedExtractor,
)


PROJECT_ROOT = Path(__file__).resolve().parent


class _JSONArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise HRSkillError("INVALID_ARGUMENT", "命令行参数无效。")


def build_service(project_root: Path) -> JDService:
    """Build the production service from environment-backed settings."""
    repository = FileRepository()
    workspace = WorkspaceManager(
        Settings.from_environment(project_root),
        repository,
    )
    return JDService(
        project_root=project_root,
        workspace=workspace,
        repository=repository,
        llm_service=LLMService.from_environment(),
        extractor=RuleBasedExtractor(),
    )


def _parse_arguments(argv: list[str] | None) -> argparse.Namespace:
    parser = _JSONArgumentParser(add_help=False)
    inputs = parser.add_mutually_exclusive_group()
    inputs.add_argument("--request", metavar="FILE")
    inputs.add_argument("--json", dest="json_text", metavar="STRING")
    return parser.parse_args(argv)


def _read_request(arguments: argparse.Namespace) -> dict:
    if arguments.request:
        try:
            raw = Path(arguments.request).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise HRSkillError(
                "REQUEST_READ_ERROR",
                f"无法读取请求文件：{arguments.request}",
            ) from error
    elif arguments.json_text is not None:
        raw = arguments.json_text
    else:
        raw = sys.stdin.read()

    try:
        payload = json.loads(raw)
    except (json.JSONDecodeError, UnicodeError) as error:
        raise HRSkillError(
            "INVALID_JSON",
            "请求必须是有效的 JSON 对象。",
        ) from error

    if not isinstance(payload, dict):
        raise HRSkillError("INVALID_REQUEST", "请求必须是 JSON 对象。")
    return payload


def _request_mode(payload: object) -> str:
    if isinstance(payload, dict) and isinstance(payload.get("mode"), str):
        return payload["mode"]
    return "generate_jd"


def main(argv: list[str] | None = None) -> int:
    """Handle one request and write exactly one JSON object to stdout."""
    mode = "generate_jd"
    try:
        arguments = _parse_arguments(argv)
        payload = _read_request(arguments)
        mode = _request_mode(payload)
        request = validate_generate_jd_request(payload)
        result = build_service(PROJECT_ROOT).create_position(request)
        response = success_response(
            mode=mode,
            message="职位已创建。",
            data=result["position"],
            generated_files=result["generated_files"],
            warnings=result["warnings"],
        )
        exit_code = 0
    except HRSkillError as error:
        response = error_response(error, mode)
        exit_code = 1
    except Exception:
        response = error_response(
            HRSkillError("INTERNAL_ERROR", "处理请求时发生内部错误，请稍后重试。"),
            mode,
        )
        exit_code = 1

    sys.stdout.write(json.dumps(response, ensure_ascii=False) + "\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
