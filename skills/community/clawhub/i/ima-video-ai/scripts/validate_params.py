#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from types import SimpleNamespace
from typing import Any

from parse_user_request import parse_request

from ima_runtime.shared.catalog import apply_virtual_param_overrides, list_all_models, normalize_model_id
from ima_runtime.shared.client import get_product_list
from ima_runtime.shared.media_payloads import filter_models_for_media_support


def _flatten_media(values) -> list[str]:
    result: list[str] = []
    for value in values or []:
        if isinstance(value, list):
            result.extend(str(v) for v in value if str(v).strip())
        elif value is not None and str(value).strip():
            result.append(str(value))
    return result


def _flatten_model_nodes(product_tree: list) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []

    def walk(nodes):
        for node in nodes or []:
            if node.get("type") == "3":
                item = {
                    "name": node.get("name", ""),
                    "model_id": normalize_model_id(node.get("model_id")) or node.get("model_id"),
                    "raw_model_id": node.get("model_id"),
                    "version_id": node.get("id", ""),
                    "form_config": list(node.get("form_config") or []),
                    "credit_rules": list(node.get("credit_rules") or []),
                    "model_types": list(node.get("model_types") or []),
                    "files_accept_types": list((node.get("files") or {}).get("acceptType") or []),
                }
                result.append(item)
            walk(node.get("children") or [])

    walk(product_tree)
    return result


def _field_options(field: dict) -> set[str]:
    options = field.get("options") or []
    return {str(option.get("value")) for option in options if option.get("value") is not None}


def _normalize_value(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value).strip().upper()


def _constraint_alias_candidates(key: str) -> tuple[str, ...]:
    if key == "resolution":
        return ("resolution", "quality")
    if key == "quality":
        return ("quality", "resolution")
    return (key,)


def _remap_constraint_for_model(model: dict, key: str, value: Any) -> tuple[dict[str, Any] | None, bool]:
    form_config = model.get("form_config") or []
    direct_field = next((field for field in form_config if field.get("field") == key), None)
    if direct_field:
        options = _field_options(direct_field)
        if options and str(value) not in options:
            normalized_options = {_normalize_value(option) for option in options}
            if _normalize_value(value) not in normalized_options:
                return None, True
        return {key: value}, True

    virtual_fields = [field for field in form_config if field.get("is_ui_virtual")]
    for candidate_key in _constraint_alias_candidates(key):
        try:
            remapped = apply_virtual_param_overrides(virtual_fields, {candidate_key: value})
        except ValueError:
            continue
        if remapped != {candidate_key: value} or candidate_key in {field.get("field") for field in virtual_fields}:
            return remapped, True
        ui_field_names = {
            ui.get("field") or ui.get("id")
            for field in virtual_fields
            for ui in (field.get("ui_params") or [])
            if ui.get("field") or ui.get("id")
        }
        if candidate_key in ui_field_names:
            return remapped, True

    return None, False


def _credit_rule_supports_constraints(model: dict, constraints: dict[str, Any]) -> bool | None:
    credit_rules = model.get("credit_rules") or []
    if not credit_rules or not constraints:
        return None

    remapped: dict[str, Any] = {}
    any_remapped = False
    for key, value in constraints.items():
        mapped, handled = _remap_constraint_for_model(model, key, value)
        if handled:
            any_remapped = True
            if mapped is None:
                return False
            remapped.update(mapped)

    if not any_remapped:
        return None

    attrs_keys = {
        str(attr_key).strip().lower()
        for rule in credit_rules
        for attr_key in (rule.get("attributes") or {}).keys()
    }
    relevant = {
        key: value
        for key, value in remapped.items()
        if str(key).strip().lower() in attrs_keys
    }
    if not relevant:
        return None

    normalized_relevant = {str(k).strip().lower(): _normalize_value(v) for k, v in relevant.items()}
    for rule in credit_rules:
        attrs = rule.get("attributes") or {}
        normalized_attrs = {str(k).strip().lower(): _normalize_value(v) for k, v in attrs.items()}
        if all(normalized_attrs.get(k) == v for k, v in normalized_relevant.items()):
            return True
    return False


def _supports_constraint(model: dict, key: str, value: Any) -> bool | None:
    credit_rule_support = _credit_rule_supports_constraints(model, {key: value})
    if credit_rule_support is not None:
        return credit_rule_support

    form_config = model.get("form_config") or []
    direct_field = next((field for field in form_config if field.get("field") == key), None)
    if direct_field:
        options = _field_options(direct_field)
        if not options:
            return None
        normalized_options = {_normalize_value(option) for option in options}
        return _normalize_value(value) in normalized_options

    remapped, handled = _remap_constraint_for_model(model, key, value)
    if handled:
        if remapped is None:
            return False
        return True

    return None


def _compatible_with_constraints(models: list[dict], constraints: dict[str, Any]) -> tuple[list[dict], list[str]]:
    if not constraints:
        return models, []
    compatible: list[dict] = []
    unknown_constraints: list[str] = []
    for model in models:
        is_compatible = True
        unresolved_keys: list[str] = []
        for key, value in constraints.items():
            support = _supports_constraint(model, key, value)
            if support is False:
                is_compatible = False
                break
            if support is None:
                unresolved_keys.append(key)
        if is_compatible:
            compatible.append(model)
        unknown_constraints.extend(unresolved_keys)
    return compatible, sorted(set(unknown_constraints))


def _rank_models(models: list[dict], semantic_intent: dict[str, bool]) -> list[dict]:
    def score(model: dict) -> tuple:
        first_points = (model.get("credit_rules") or [{}])[0].get("points", 0)
        if semantic_intent.get("speed_priority") and not semantic_intent.get("quality_priority"):
            return (first_points, model.get("name", ""))
        if semantic_intent.get("quality_priority") and not semantic_intent.get("speed_priority"):
            return (-first_points, model.get("name", ""))
        return (model.get("name", ""), first_points)

    return sorted(models, key=score)


def validate_request(request: str, media: list[str], *, base_url: str, api_key: str, language: str = "en") -> dict[str, Any]:
    parsed = parse_request(request, media)
    if parsed.get("clarification"):
        return {"status": "clarification", **parsed}

    task_type = parsed["task_type"]
    tree = get_product_list(base_url, api_key, task_type, language=language)
    models = _flatten_model_nodes(tree)
    compatible_models = filter_models_for_media_support(
        task_type,
        models,
        tuple(
            SimpleNamespace(**asset)
            for asset in parsed["media_assets"]
        ),
    )
    compatible_models, unknown_constraints = _compatible_with_constraints(compatible_models, parsed["constraints"])

    explicit_model_id = parsed.get("explicit_model_id")
    if explicit_model_id:
        explicit_candidates = [model for model in compatible_models if model["model_id"] == explicit_model_id]
        if not explicit_candidates:
            return {
                "status": "error",
                "reason": "model_constraint_conflict",
                "message": f"Explicit model '{explicit_model_id}' conflicts with the current media or parameter constraints.",
                **parsed,
            }
        selected = _rank_models(explicit_candidates, parsed["semantic_intent"])[0]
        return {"status": "ok", "selected_model": selected, "compatible_models": explicit_candidates, "unknown_constraints": unknown_constraints, **parsed}

    if not compatible_models:
        return {
            "status": "error",
            "reason": "no_compatible_model",
            "message": f"No live catalog model currently supports task_type={task_type} with the current media and parameter constraints.",
            **parsed,
        }

    ranked = _rank_models(compatible_models, parsed["semantic_intent"])
    speed = parsed["semantic_intent"].get("speed_priority")
    quality = parsed["semantic_intent"].get("quality_priority")
    if len(ranked) == 1 or speed != quality:
        return {"status": "ok", "selected_model": ranked[0], "compatible_models": ranked, "unknown_constraints": unknown_constraints, **parsed}

    return {
        "status": "clarification",
        "reason": "multiple_compatible_models",
        "message": "Multiple live catalog models satisfy the request. Clarify whether you prefer speed, cost, or final quality.",
        "model_options": [
            {"model_id": model["model_id"], "version_id": model["version_id"], "name": model["name"]}
            for model in ranked[:3]
        ],
        "unknown_constraints": unknown_constraints,
        **parsed,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate parsed natural-language video parameters against the live catalog")
    parser.add_argument("--request", required=True, help="Free-form user request")
    parser.add_argument("--media", nargs="*", action="append", default=[], help="Optional media paths or URLs referenced by the request")
    parser.add_argument("--api-key", help="IMA API key; falls back to IMA_API_KEY")
    parser.add_argument("--base-url", default="https://api.imastudio.com", help="API base URL")
    parser.add_argument("--language", default="en", help="Catalog language")
    parser.add_argument("--output-json", action="store_true", help="Output validation result as JSON")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    api_key = args.api_key or os.getenv("IMA_API_KEY")
    if not api_key:
        print("IMA_API_KEY is required.", file=sys.stderr)
        return 1
    result = validate_request(args.request, _flatten_media(args.media), base_url=args.base_url, api_key=api_key, language=args.language)
    if args.output_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result)
    return 0 if result.get("status") == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
