from __future__ import annotations

import os
import sys

import requests

from ima_runtime.shared.catalog import list_all_models
from ima_runtime.shared.client import get_product_list
from ima_runtime.shared.errors import (
    build_contextual_diagnosis,
    extract_error_info,
    format_preflight_failure_message,
)
from ima_runtime.shared.recommendations import build_recommendation_lines


def _log(logger, level: str, message: str, *args) -> None:
    log_method = getattr(logger, level, None)
    if callable(log_method):
        log_method(message, *args)


def _fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def run_doctor(args, logger, env: dict[str, str] | None = None) -> int:
    env = dict(os.environ if env is None else env)
    api_key = args.api_key or env.get("IMA_API_KEY")

    print(f"Doctor checks for {args.task_type}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"requests: {requests.__version__}")

    if not api_key:
        return _fail(
            "IMA_API_KEY is missing.\n"
            "Set IMA_API_KEY or pass --api-key.\n"
            "Create one at https://www.imaclaw.ai/imaclaw/apikey"
        )

    print("API key: present")
    _log(logger, "info", "Doctor start: task_type=%s", args.task_type)
    try:
        tree = get_product_list(args.base_url, api_key, args.task_type, language=args.language)
    except Exception as exc:
        _log(logger, "error", "Doctor product list failed: %s", exc)
        diagnosis = build_contextual_diagnosis(
            error_info=extract_error_info(exc),
            task_type=args.task_type,
            model_params={"model_name": "IMA Model", "model_id": None, "form_params": {}},
            current_params=None,
            input_images=[],
            credit_rules=None,
        )
        return _fail(
            format_preflight_failure_message(
                operation_name="product list",
                diagnosis=diagnosis,
            )
        )

    models = list_all_models(tree)
    if not models:
        return _fail(
            f"Product list returned zero usable models for {args.task_type}. "
            "Verify account access or try again later."
        )
    print(f"Product list: reachable ({len(models)} model leaves)")
    print("\n".join(build_recommendation_lines(args.task_type, models)))
    print("No paid generation task was created.")
    _log(logger, "info", "Doctor completed: task_type=%s models=%s", args.task_type, len(models))
    return 0
