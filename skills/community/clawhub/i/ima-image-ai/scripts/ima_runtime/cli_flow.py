from __future__ import annotations

import json
import os
import sys

from ima_runtime.adapters.cli_presenter import print_model_summary
from ima_runtime.capabilities.image.executor import execute_image_task
from ima_runtime.capabilities.image.models import build_image_model_binding
from ima_runtime.capabilities.image.params import infer_prompt_controls
from ima_runtime.capabilities.image.routes import build_image_task_spec
from ima_runtime.shared.catalog import apply_virtual_param_specs, extract_model_params, list_all_models
from ima_runtime.shared.client import get_product_list
from ima_runtime.shared.config import DEFAULT_MODEL_BY_TASK_TYPE, DEFAULT_MODEL_LABEL_BY_TASK_TYPE
from ima_runtime.shared.errors import build_contextual_diagnosis, extract_error_info, format_user_failure_message
from ima_runtime.shared.inputs import flatten_input_images_args, prepare_image_url
from ima_runtime.shared.output_validation import OutputValidationError
from ima_runtime.shared.prefs import get_preferred_model_id, save_pref
from ima_runtime.shared.types import ClarificationRequest, GatewayRequest


def _log(logger, level: str, message: str, *args) -> None:
    method = getattr(logger, level, None)
    if callable(method):
        method(message, *args)


def _fail(message: str) -> int:
    print(f"❌ {message}", file=sys.stderr)
    return 1


def _print_model_list(task_type: str, models: list[dict]) -> None:
    print(f"\nAvailable models for '{task_type}':")
    print(f"{'Name':<28} {'model_id':<34} {'version_id':<44} {'pts':>4}  attr_id")
    print("─" * 120)
    for model in models:
        print(f"{model['name']:<28} {model['model_id']:<34} {model['version_id']:<44} {model['credit']:>4}  {model['attr_id']}")


def _print_generation_result(result) -> None:
    print("\n✅ Generation complete!")
    print(f"   URL:   {result.url}")
    if result.cover_url:
        print(f"   Cover: {result.cover_url}")


def _normalize_control_value(value: object) -> str | None:
    if value is None:
        return None
    return str(value).strip().upper()


def _iter_model_leaf_nodes(nodes: list[dict]) -> list[dict]:
    leaves: list[dict] = []
    for node in nodes:
        if node.get("type") == "3":
            leaves.append(node)
        leaves.extend(_iter_model_leaf_nodes(node.get("children") or []))
    return leaves


MODEL_CONSTRAINT_KEYS = ("size", "aspect_ratio", "n", "quality")


def _extract_model_constraints(extra_params: dict[str, object]) -> dict[str, str]:
    constraints: dict[str, str] = {}
    for key in MODEL_CONSTRAINT_KEYS:
        normalized = _normalize_control_value(extra_params.get(key))
        if normalized is not None:
            constraints[key] = normalized
    return constraints


def _credit_for_constraint_candidate(node: dict, constraints: dict[str, str]) -> int | None:
    try:
        resolved = extract_model_params(node)
    except RuntimeError:
        return None

    try:
        effective_constraints, applied_virtual = apply_virtual_param_specs(constraints, resolved.get("virtual_param_specs") or [])
    except ValueError:
        return None

    normalized_defaults = {key.lower().strip(): _normalize_control_value(value) for key, value in resolved["form_params"].items()}
    field_option_specs = {
        key.lower().strip(): tuple(value for value in values)
        for key, values in (resolved.get("field_option_specs") or {}).items()
    }
    normalized_rules = [
        {
            "points": int(rule.get("points", 0)),
            "attributes": {
                key.lower().strip(): _normalize_control_value(value)
                for key, value in (rule.get("attributes") or {}).items()
                if not (key == "default" and value == "enabled")
            },
        }
        for rule in (node.get("credit_rules") or [])
    ]
    mentioned_keys = set(normalized_defaults)
    for rule in normalized_rules:
        mentioned_keys.update(rule["attributes"])

    best_points: int | None = None

    for rule in normalized_rules:
        attrs = rule["attributes"]
        compatible = True
        for key, value in effective_constraints.items():
            if key in field_option_specs:
                if value not in field_option_specs[key]:
                    compatible = False
                    break
                continue

            if key not in mentioned_keys:
                continue

            if key in applied_virtual:
                continue

            effective_value = attrs[key] if key in attrs else normalized_defaults.get(key)
            if effective_value != value:
                compatible = False
                break

        if not compatible:
            continue

        points = rule["points"]
        if best_points is None or points < best_points:
            best_points = points

    return best_points


def _node_mentions_any_constraint(node: dict, constraints: dict[str, str]) -> bool:
    try:
        resolved = extract_model_params(node)
    except RuntimeError:
        return False

    mentioned_keys = {key.lower().strip() for key in resolved["form_params"]}
    mentioned_keys.update(key.lower().strip() for key in (resolved.get("field_option_specs") or {}))
    for spec in resolved.get("virtual_param_specs") or []:
        mentioned_keys.update(spec.get("source_params") or ())
        target_param = spec.get("target_param")
        if target_param:
            mentioned_keys.add(target_param)
    for rule in node.get("credit_rules") or []:
        mentioned_keys.update(
            key.lower().strip()
            for key, value in (rule.get("attributes") or {}).items()
            if not (key == "default" and value == "enabled")
        )
    return any(key in mentioned_keys for key in constraints)


def _select_live_model_id_by_constraints(
    product_tree: list[dict],
    task_type: str,
    extra_params: dict[str, object],
    preferred_model_id: str | None,
) -> tuple[str | None, dict[str, str], bool]:
    if task_type not in {"text_to_image", "image_to_image"}:
        return None, {}, False

    constraints = _extract_model_constraints(extra_params)
    if not constraints:
        return None, {}, False

    candidates: list[tuple[int, str]] = []
    catalog_mentions_constraints = False
    for node in _iter_model_leaf_nodes(product_tree):
        model_id = str(node.get("model_id") or "").strip()
        if not model_id:
            continue
        if _node_mentions_any_constraint(node, constraints):
            catalog_mentions_constraints = True
        points = _credit_for_constraint_candidate(node, constraints=constraints)
        if points is None:
            continue
        candidates.append((points, model_id))

    if not candidates:
        if not catalog_mentions_constraints:
            return None, constraints, False
        return None, constraints, True

    compatible_model_ids = {model_id for _, model_id in candidates}
    if preferred_model_id and preferred_model_id in compatible_model_ids:
        return preferred_model_id, constraints, True

    candidates.sort(key=lambda item: (item[0], item[1]))
    return candidates[0][1], constraints, True


def _model_supports_constraints(product_tree: list[dict], model_id: str, constraints: dict[str, str]) -> bool:
    if not constraints:
        return True

    for node in _iter_model_leaf_nodes(product_tree):
        node_model_id = str(node.get("model_id") or "").strip()
        if node_model_id != model_id:
            continue
        return _credit_for_constraint_candidate(node, constraints=constraints) is not None
    return False


def _compatible_model_ids(product_tree: list[dict], constraints: dict[str, str]) -> list[str]:
    if not constraints:
        return []

    best_points_by_model: dict[str, int] = {}
    for node in _iter_model_leaf_nodes(product_tree):
        model_id = str(node.get("model_id") or "").strip()
        if not model_id:
            continue
        points = _credit_for_constraint_candidate(node, constraints=constraints)
        if points is None:
            continue
        current = best_points_by_model.get(model_id)
        if current is None or points < current:
            best_points_by_model[model_id] = points

    return [
        model_id
        for model_id, _ in sorted(best_points_by_model.items(), key=lambda item: (item[1], item[0]))
    ]


def run_cli(args, logger) -> int:
    api_key = args.api_key or os.getenv("IMA_API_KEY")
    if not api_key:
        return _fail("API key is required. Use --api-key or set IMA_API_KEY.")
    if not args.list_models and not args.prompt:
        return _fail("--prompt is required")

    extra_params: dict[str, object] = {}
    if args.size:
        extra_params["size"] = args.size
    if args.extra_params:
        try:
            decoded = json.loads(args.extra_params)
        except json.JSONDecodeError as exc:
            return _fail(f"Invalid --extra-params JSON: {exc}")
        if not isinstance(decoded, dict):
            return _fail("--extra-params must decode to a JSON object")
        extra_params.update(decoded)

    inferred_prompt_controls = infer_prompt_controls(args.prompt or "")
    inferred_model_id = inferred_prompt_controls.pop("__model_id__", None)
    for key, value in inferred_prompt_controls.items():
        extra_params.setdefault(key, value)

    if args.list_models:
        try:
            tree = get_product_list(args.base_url, api_key, args.task_type, language=args.language)
        except Exception as exc:
            return _fail(str(exc))
        payload = list_all_models(tree)
        if args.output_json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0
        _print_model_list(args.task_type, payload)
        return 0

    raw_inputs = flatten_input_images_args(args.input_images)
    try:
        resolved_inputs = [value if value.startswith("https://") else prepare_image_url(value, api_key) for value in raw_inputs]
    except Exception as exc:
        _log(logger, "error", "Input preparation failed: %s", exc)
        return _fail(str(exc))

    request = GatewayRequest(
        prompt=args.prompt,
        media_targets=("image",),
        input_images=tuple(resolved_inputs),
        intent_hints={"task_type": args.task_type},
        extra_params=extra_params,
    )
    try:
        spec = build_image_task_spec(request)
    except ValueError as exc:
        return _fail(str(exc))
    if isinstance(spec, ClarificationRequest):
        return _fail(spec.question)

    try:
        tree = get_product_list(args.base_url, api_key, spec.task_type, language=args.language)
    except Exception as exc:
        return _fail(str(exc))

    explicit_model_id = args.model_id
    preferred_model_id = get_preferred_model_id(args.user_id, spec.task_type)
    auto_selected_model = False
    selected_by_constraints, constraints, had_constraints = _select_live_model_id_by_constraints(
        tree,
        spec.task_type,
        dict(spec.extra_params),
        preferred_model_id,
    )

    if explicit_model_id:
        model_id = explicit_model_id
        if had_constraints and not _model_supports_constraints(tree, model_id, constraints):
            requested = ", ".join(f"{key}={value}" for key, value in constraints.items())
            return _fail(
                "Selected model does not support the requested parameters from the live catalog: "
                f"{requested}. Use --list-models to inspect compatible models or adjust the prompt/params."
            )
    elif inferred_model_id:
        model_id = inferred_model_id
        if had_constraints and not _model_supports_constraints(tree, model_id, constraints):
            requested = ", ".join(f"{key}={value}" for key, value in constraints.items())
            return _fail(
                "Prompt-inferred model does not support the requested parameters from the live catalog: "
                f"{requested}. Adjust the prompt, remove the conflicting model hint, or inspect --list-models."
            )
    else:
        if had_constraints:
            if selected_by_constraints is None:
                requested = ", ".join(f"{key}={value}" for key, value in constraints.items())
                return _fail(
                    "No live model supports the requested parameters: "
                    f"{requested}. Inspect --list-models and adjust the prompt/params."
                )
            model_id = selected_by_constraints
            auto_selected_model = True
            if not args.output_json:
                print(f"ℹ️ Using live catalog compatible model: {model_id}")
        elif preferred_model_id:
            model_id = preferred_model_id
        else:
            model_id = DEFAULT_MODEL_BY_TASK_TYPE[spec.task_type]
            auto_selected_model = True
            if not args.output_json:
                print(
                    "ℹ️ Using recommended default model: "
                    f"{DEFAULT_MODEL_LABEL_BY_TASK_TYPE[spec.task_type]} ({model_id})"
                )

    candidate_model_ids = [model_id]
    if had_constraints and explicit_model_id is None:
        for compatible_model_id in _compatible_model_ids(tree, constraints):
            if compatible_model_id not in candidate_model_ids:
                candidate_model_ids.append(compatible_model_id)

    result = None
    binding = None
    last_exc: Exception | None = None
    tried_validation_models: list[str] = []

    for index, candidate_model_id in enumerate(candidate_model_ids):
        try:
            binding = build_image_model_binding(tree, candidate_model_id, args.version_id)
        except Exception as exc:
            return _fail(str(exc))

        if not args.output_json:
            print_model_summary(binding.resolved_params)
        try:
            result = execute_image_task(args.base_url, api_key, spec, binding)
            model_id = candidate_model_id
            break
        except OutputValidationError as exc:
            last_exc = exc
            tried_validation_models.append(candidate_model_id)
            can_retry = index < len(candidate_model_ids) - 1
            if can_retry:
                auto_selected_model = True
                if not args.output_json:
                    print(
                        "⚠️ Output validation failed for "
                        f"{candidate_model_id}; retrying with compatible model {candidate_model_ids[index + 1]}."
                    )
                continue
            break
        except Exception as exc:
            last_exc = exc
            break

    if result is None:
        assert last_exc is not None
        diagnosis = build_contextual_diagnosis(
            error_info=extract_error_info(last_exc),
            task_type=spec.task_type,
            model_params=dict(binding.resolved_params) if binding is not None else {},
            current_params=dict(spec.extra_params),
            input_images=list(spec.input_images),
            credit_rules=list(binding.resolved_params.get("all_credit_rules") or []) if binding is not None else [],
        )
        if tried_validation_models:
            diagnosis["actions"].insert(0, f"Compatible models tried: {', '.join(tried_validation_models)}")
        attempts_used = getattr(last_exc, "attempts_used", 1)
        max_attempts = getattr(last_exc, "max_attempts", attempts_used)
        if tried_validation_models:
            attempts_used = max(attempts_used, len(tried_validation_models))
            max_attempts = max(max_attempts, len(candidate_model_ids))
        return _fail(format_user_failure_message(diagnosis, attempts_used, max_attempts))

    if not auto_selected_model:
        save_pref(
            args.user_id,
            spec.task_type,
            {"model_id": result.model_id, "model_name": result.model_name, "credit": result.credit},
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
    return 0
