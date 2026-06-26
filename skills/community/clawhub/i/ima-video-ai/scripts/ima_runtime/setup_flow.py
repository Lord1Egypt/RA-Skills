from __future__ import annotations

import os
import sys

from ima_runtime.shared.catalog import list_all_models, normalize_model_id
from ima_runtime.shared.client import get_product_list
from ima_runtime.shared.config import VIDEO_TASK_TYPES
from ima_runtime.shared.errors import (
    build_contextual_diagnosis,
    extract_error_info,
    format_preflight_failure_message,
    to_user_facing_model_name,
)
from ima_runtime.shared.prefs import save_pref
from ima_runtime.shared.recommendations import build_recommendation_lines, resolve_suggested_model


def _log(logger, level: str, message: str, *args) -> None:
    log_method = getattr(logger, level, None)
    if callable(log_method):
        log_method(message, *args)


def _fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def _cancelled_error() -> ValueError:
    return ValueError(
        "Setup cancelled. Re-run scripts/ima_runtime_setup.py when you're ready, "
        "or use --model-id with scripts/ima_runtime_cli.py."
    )


def _prompt_api_key(input_fn, env: dict[str, str]) -> str | None:
    existing = env.get("IMA_API_KEY")
    if existing:
        return existing
    try:
        entered = input_fn("Enter IMA_API_KEY (leave blank to cancel): ").strip()
    except (EOFError, KeyboardInterrupt) as exc:
        raise _cancelled_error() from exc
    return entered or None


def _prompt_task_type(input_fn) -> str:
    print("Choose the first task type to configure:")
    for index, task_type in enumerate(VIDEO_TASK_TYPES, start=1):
        print(f"{index}. {task_type}")
    try:
        choice = input_fn("Task type [1]: ").strip()
    except (EOFError, KeyboardInterrupt) as exc:
        raise _cancelled_error() from exc
    if not choice:
        return VIDEO_TASK_TYPES[0]
    if choice.isdigit():
        selected_index = int(choice)
        if 1 <= selected_index <= len(VIDEO_TASK_TYPES):
            return VIDEO_TASK_TYPES[selected_index - 1]
    if choice in VIDEO_TASK_TYPES:
        return choice
    raise ValueError(f"Unsupported task type selection: {choice}")


def _select_model(task_type: str, models: list[dict], requested_model_id: str | None, input_fn) -> dict:
    models_by_id = {
        normalize_model_id(model.get("model_id")) or model.get("model_id"): model
        for model in models
        if model.get("model_id")
    }
    if requested_model_id:
        chosen = models_by_id.get(normalize_model_id(requested_model_id) or requested_model_id)
        if not chosen:
            raise ValueError(f"Unknown model_id for {task_type}: {requested_model_id}")
        return chosen

    suggestion = resolve_suggested_model(task_type, models)
    if suggestion.model is None:
        raise ValueError(f"No models available for {task_type}")

    if suggestion.is_catalog_recommended:
        print("Press Enter to use the recommended model shown below.")
    else:
        print(f"No catalog recommendation is currently available for {task_type}.")
        print("Press Enter to use the first available model shown below.")

    print("Available models:")
    for index, model in enumerate(models, start=1):
        display_name = to_user_facing_model_name(model.get("name"), model.get("model_id"))
        print(f"{index}. {display_name} ({model['model_id']}) - {model['credit']} pts")

    try:
        choice = input_fn(f"Model number or model_id [{suggestion.model['model_id']}]: ").strip()
    except (EOFError, KeyboardInterrupt) as exc:
        raise _cancelled_error() from exc
    if not choice:
        return suggestion.model
    if choice.isdigit():
        selected_index = int(choice)
        if 1 <= selected_index <= len(models):
            return models[selected_index - 1]
    chosen = models_by_id.get(normalize_model_id(choice) or choice)
    if chosen:
        return chosen
    raise ValueError(f"Unknown model selection: {choice}")


def _print_next_steps(task_type: str, user_id: str) -> None:
    prompt_example = "a paper airplane gliding through warm sunset light"
    cli_cmd = f'python3 scripts/ima_runtime_cli.py --task-type {task_type} --prompt "{prompt_example}"'
    if user_id != "default":
        cli_cmd += f" --user-id {user_id}"

    print("IMA_API_KEY is not persisted by this setup script.")
    print("Next steps:")
    print('1. export IMA_API_KEY="your-api-key"')
    print(f"2. {cli_cmd}")


def run_setup(args, logger, input_fn=input, env: dict[str, str] | None = None) -> int:
    env = dict(os.environ if env is None else env)
    try:
        api_key = args.api_key or _prompt_api_key(input_fn, env)
        if not api_key:
            return _fail(
                "API key is required for setup.\n"
                "Set IMA_API_KEY or rerun with --api-key after creating one at "
                "https://www.imaclaw.ai/imaclaw/apikey"
            )
        task_type = args.task_type or _prompt_task_type(input_fn)
    except ValueError as exc:
        return _fail(str(exc))

    _log(logger, "info", "Setup start: task_type=%s user_id=%s", task_type, args.user_id)
    try:
        tree = get_product_list(args.base_url, api_key, task_type, language=args.language)
    except Exception as exc:
        _log(logger, "error", "Setup product list failed: %s", exc)
        diagnosis = build_contextual_diagnosis(
            error_info=extract_error_info(exc),
            task_type=task_type,
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
        return _fail(f"No models were returned for {task_type}. Run again later.")

    print("\n".join(build_recommendation_lines(task_type, models)))

    try:
        selected_model = _select_model(task_type, models, args.model_id, input_fn)
    except ValueError as exc:
        return _fail(str(exc))

    save_pref(
        args.user_id,
        task_type,
        {
            "model_id": selected_model["model_id"],
            "model_name": selected_model["name"],
            "credit": selected_model["credit"],
        },
    )
    display_name = to_user_facing_model_name(selected_model["name"], selected_model["model_id"])
    print(f"Saved preference for user '{args.user_id}': {display_name} ({selected_model['model_id']})")
    _print_next_steps(task_type, args.user_id)
    _log(logger, "info", "Setup completed: task_type=%s model_id=%s", task_type, selected_model["model_id"])
    return 0
