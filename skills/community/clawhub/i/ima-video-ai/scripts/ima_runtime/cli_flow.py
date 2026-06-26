from __future__ import annotations

import json
import os
import sys

from ima_runtime.adapters.cli_presenter import print_model_summary
from ima_runtime.capabilities.video.executor import execute_video_task
from ima_runtime.capabilities.video.models import build_video_model_binding, normalize_model_id
from ima_runtime.capabilities.video.routes import build_video_task_spec
from ima_runtime.shared.catalog import list_all_models
from ima_runtime.shared.client import get_product_list
from ima_runtime.shared.errors import (
    build_contextual_diagnosis,
    extract_error_info,
    format_preflight_failure_message,
    format_user_failure_message,
    to_user_facing_model_name,
)
from ima_runtime.shared.inputs import (
    build_cli_media_assets,
    flatten_input_images_args,
)
from ima_runtime.shared.media_payloads import (
    build_media_payload_bundle,
    filter_models_for_media_support,
    prepare_media_assets,
    validate_model_media_support,
)
from ima_runtime.shared.reference_validation import (
    ReferenceInputValidationError,
    validate_seedance_image_assets,
    validate_seedance_reference_assets,
)
from ima_runtime.shared.compliance import AssetVerificationError, ensure_assets_verified
from ima_runtime.shared.prefs import get_preferred_model_id, save_pref
from ima_runtime.shared.recommendations import build_recommendation_lines, resolve_suggested_model
from ima_runtime.shared.seedance_capabilities import is_seedance_model
from ima_runtime.shared.types import ClarificationRequest, GatewayRequest


def _log(logger, level: str, message: str, *args) -> None:
    log_method = getattr(logger, level, None)
    if callable(log_method):
        log_method(message, *args)


def _print_model_list(task_type: str, models: list[dict]) -> None:
    print(f"\nAvailable models for '{task_type}':")
    print(f"{'Name':<28} {'model_id':<34} {'version_id':<44} {'pts':>4}  attr_id")
    print("─" * 120)
    for model in models:
        print(
            f"{model['name']:<28} {model['model_id']:<34} {model['version_id']:<44} "
            f"{model['credit']:>4}  {model['attr_id']}"
        )


def _print_generation_result(result) -> None:
    print("\n✅ Generation complete!")
    print(f"   URL:   {result.url}")
    if result.cover_url:
        print(f"   Cover: {result.cover_url}")


def _fail(message: str) -> int:
    print(f"❌ {message}", file=sys.stderr)
    return 1


def _build_missing_model_message(task_type: str, models: list[dict]) -> str:
    lines = [
        "--model-id is required (no saved preference found).",
        "Run --list-models to inspect available options.",
        *build_recommendation_lines(task_type, models),
    ]

    lines.append("Select a model explicitly with --model-id.")
    return "\n".join(lines)


def _is_interactive_terminal() -> bool:
    isatty = getattr(sys.stdin, "isatty", None)
    return bool(callable(isatty) and isatty())


def _prompt_for_model_choice(task_type: str, models: list[dict], media_assets=()) -> str:
    compatible_models = filter_models_for_media_support(task_type, models, media_assets)
    if not compatible_models:
        raise ValueError(f"No live catalog models currently support the requested {task_type} media constraints.")

    suggestion = resolve_suggested_model(task_type, compatible_models)
    if not suggestion.model:
        raise ValueError(f"No models were returned for {task_type}.")

    print(f"No saved preference found for {task_type}.")
    print("\n".join(build_recommendation_lines(task_type, models)))
    if media_assets:
        print(f"Compatible live catalog candidates for current inputs: {len(compatible_models)}")
    if suggestion.is_catalog_recommended:
        print("Press Enter to use the recommended model, choose a number below, or type a model_id.")
    else:
        print(f"No catalog recommendation is currently available for {task_type}.")
        print("Press Enter to use the first available model, choose a number below, or type a model_id.")

    choices: list[dict] = []
    seen_model_ids: set[str] = set()
    suggested_id = normalize_model_id(suggestion.model.get("model_id")) or suggestion.model.get("model_id")

    def add_choice(model: dict) -> None:
        model_id = normalize_model_id(model.get("model_id")) or model.get("model_id")
        if not model_id or model_id in seen_model_ids:
            return
        seen_model_ids.add(model_id)
        choices.append(model)

    add_choice(suggestion.model)
    for model in compatible_models:
        add_choice(model)
        if len(choices) >= 3:
            break

    for index, model in enumerate(choices, start=1):
        model_id = normalize_model_id(model.get("model_id")) or model.get("model_id")
        display_name = to_user_facing_model_name(model.get("name"), model_id)
        print(f"{index}. {display_name} ({model_id})")

    try:
        selection = input(f"Model selection [{suggested_id}]: ").strip()
    except (EOFError, KeyboardInterrupt) as exc:
        raise ValueError(
            "First-run model selection cancelled. Re-run with --model-id, "
            "--list-models, or scripts/ima_runtime_setup.py."
        ) from exc
    if not selection:
        return suggested_id

    if selection.isdigit():
        selected_index = int(selection)
        if 1 <= selected_index <= len(choices):
            selected_model = choices[selected_index - 1]
            return normalize_model_id(selected_model.get("model_id")) or selected_model.get("model_id")

    normalized_selection = normalize_model_id(selection) or selection
    available_model_ids = {
        normalize_model_id(model.get("model_id")) or model.get("model_id")
        for model in compatible_models
        if model.get("model_id")
    }
    if normalized_selection in available_model_ids:
        return normalized_selection

    raise ValueError(
        "Unknown model selection. Use a listed number, an available model_id, or rerun with --list-models."
    )


def run_cli(args, logger) -> int:
    api_key = args.api_key or os.getenv("IMA_API_KEY")
    if not api_key:
        return _fail(
            "API key is required. Use --api-key or set IMA_API_KEY. "
            "Get one at https://www.imaclaw.ai/imaclaw/apikey"
        )

    if not args.list_models and not args.prompt:
        return _fail("--prompt is required")

    extra_params: dict[str, object] = {}
    if args.size:
        extra_params["size"] = args.size
    if args.extra_params:
        try:
            decoded_extra_params = json.loads(args.extra_params)
        except json.JSONDecodeError as exc:
            return _fail(f"Invalid --extra-params JSON: {exc}")
        if not isinstance(decoded_extra_params, dict):
            return _fail("--extra-params must decode to a JSON object")
        extra_params.update(decoded_extra_params)

    _log(
        logger,
        "info",
        "CLI start: task_type=%s model_id=%s list_models=%s",
        args.task_type,
        args.model_id,
        args.list_models,
    )
    try:
        tree = get_product_list(args.base_url, api_key, args.task_type, language=args.language)
    except Exception as exc:
        _log(logger, "error", "Product list failed: %s", exc)
        diagnosis = build_contextual_diagnosis(
            error_info=extract_error_info(exc),
            task_type=args.task_type,
            model_params={"model_name": "IMA Model", "model_id": None, "form_params": {}},
            current_params=None,
            input_images=[],
            credit_rules=None,
        )
        if diagnosis.get("headline") == "API key is missing, invalid, or unauthorized":
            return _fail(
                format_preflight_failure_message(
                    operation_name="product list",
                    diagnosis=diagnosis,
                )
            )
        return _fail(f"Product list failed: {exc}")

    if args.list_models:
        payload = list_all_models(tree)
        if args.output_json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0
        _print_model_list(args.task_type, payload)
        print()
        print("\n".join(build_recommendation_lines(args.task_type, payload)))
        return 0

    try:
        request = GatewayRequest(
            prompt=args.prompt,
            media_targets=("video",),
            input_images=tuple(flatten_input_images_args(args.input_images)),
            media_assets=build_cli_media_assets(
                args.task_type,
                input_images=args.input_images,
                reference_images=getattr(args, "reference_images", []),
                reference_videos=getattr(args, "reference_videos", []),
                reference_audios=getattr(args, "reference_audios", []),
            ),
            intent_hints={"task_type": args.task_type},
            extra_params=extra_params,
        )
        spec = build_video_task_spec(request)
    except ValueError as exc:
        _log(logger, "error", "Input preparation failed: %s", exc)
        return _fail(str(exc))
    if isinstance(spec, ClarificationRequest):
        return _fail(spec.question)

    model_id = normalize_model_id(args.model_id) if args.model_id else get_preferred_model_id(
        args.user_id,
        args.task_type,
    )
    if not model_id:
        available_models = list_all_models(tree)
        if _is_interactive_terminal() and not args.output_json:
            try:
                model_id = _prompt_for_model_choice(args.task_type, available_models, spec.media_assets)
            except ValueError as exc:
                return _fail(str(exc))
        if not model_id:
            return _fail(_build_missing_model_message(args.task_type, available_models))

    try:
        binding = build_video_model_binding(tree, model_id, args.version_id)
    except Exception as exc:
        _log(logger, "error", "Model lookup failed: %s", exc)
        available_model_ids = sorted({model["model_id"] for model in list_all_models(tree) if model.get("model_id")})
        guidance = " Run --list-models to inspect available options."
        if available_model_ids:
            guidance += " Available model IDs: " + ", ".join(available_model_ids[:8])
            if len(available_model_ids) > 8:
                guidance += ", ..."
        return _fail(f"{exc}.{guidance}")

    try:
        validate_model_media_support(spec.task_type, dict(binding.resolved_params), spec.media_assets)
        prepared_assets = prepare_media_assets(spec.media_assets, api_key)
        if is_seedance_model(binding.candidate.model_id):
            if spec.task_type == "reference_image_to_video":
                validate_seedance_reference_assets(prepared_assets)
            elif spec.task_type in {"image_to_video", "first_last_frame_to_video"}:
                validate_seedance_image_assets(spec.task_type, prepared_assets)
        ensure_assets_verified(
            args.base_url,
            api_key,
            spec.task_type,
            binding.candidate.model_id,
            prepared_assets,
        )
        media_bundle = build_media_payload_bundle(spec.task_type, binding.candidate.model_id, prepared_assets)
    except (ValueError, RuntimeError, ReferenceInputValidationError, AssetVerificationError) as exc:
        _log(logger, "error", "Media preparation failed: %s", exc)
        return _fail(str(exc))

    print_model_summary(binding.resolved_params)
    try:
        result = execute_video_task(args.base_url, api_key, spec, binding, media_bundle=media_bundle)
    except Exception as exc:
        _log(logger, "error", "Task execution failed: %s", exc)
        attempts_used = getattr(exc, "attempts_used", 1)
        max_attempts = getattr(exc, "max_attempts", attempts_used)
        diagnosis = build_contextual_diagnosis(
            error_info=extract_error_info(exc),
            task_type=spec.task_type,
            model_params=dict(binding.resolved_params),
            current_params=dict(spec.extra_params),
            input_images=list(media_bundle.input_images),
            credit_rules=list(binding.resolved_params.get("all_credit_rules") or []),
        )
        return _fail(
            format_user_failure_message(
                diagnosis=diagnosis,
                attempts_used=attempts_used,
                max_attempts=max_attempts,
            )
        )

    save_pref(
        args.user_id,
        spec.task_type,
        {
            "model_id": result.model_id,
            "model_name": result.model_name,
            "credit": result.credit,
        },
    )

    if args.output_json:
        print(
            json.dumps(
                {
                    "task_id": result.task_id,
                    "url": result.url,
                    "cover_url": result.cover_url,
                    "model_id": result.model_id,
                    "model_name": result.model_name,
                    "credit": result.credit,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        _print_generation_result(result)
    _log(logger, "info", "CLI completed: task_id=%s", result.task_id)
    return 0
