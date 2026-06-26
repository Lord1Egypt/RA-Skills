from __future__ import annotations

import logging
import re
from typing import Any

logger = logging.getLogger("ima_skills")

MODEL_ID_ALIASES = {
    "gpt image 2": "gpt-image-2",
    "gpt-image-2": "gpt-image-2",
    "gptimage2": "gpt-image-2",
    "seedream": "doubao-seedream-4.5",
    "seedream 4.5": "doubao-seedream-4.5",
    "see dream": "doubao-seedream-4.5",
    "可梦": "doubao-seedream-4.5",
    "nano banana": "gemini-3.1-flash-image",
    "nano banana 2": "gemini-3.1-flash-image",
    "nano banana2": "gemini-3.1-flash-image",
    "banana": "gemini-3.1-flash-image",
    "香蕉": "gemini-3.1-flash-image",
    "banana pro": "gemini-3-pro-image",
    "nano banana pro": "gemini-3-pro-image",
    "香蕉pro": "gemini-3-pro-image",
    "香蕉 pro": "gemini-3-pro-image",
    "mj": "midjourney",
}


def canonicalize_model_id(model_id: str | None) -> str | None:
    if not model_id:
        return None
    normalized_key = re.sub(r"\s+", " ", model_id.strip().lower())
    return MODEL_ID_ALIASES.get(normalized_key, model_id.strip())


def _normalize_value(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value).strip().upper()


def find_model_version(product_tree: list, target_model_id: str, target_version_id: str | None = None) -> dict | None:
    candidates: list[dict] = []
    canonical_target_model_id = canonicalize_model_id(target_model_id) or target_model_id

    def walk(nodes: list) -> None:
        for node in nodes:
            if node.get("type") == "3":
                mid = node.get("model_id", "")
                normalized_mid = canonicalize_model_id(mid) or mid
                vid = node.get("id", "")
                if normalized_mid == canonical_target_model_id and (target_version_id is None or vid == target_version_id):
                    candidates.append(node)
            walk(node.get("children") or [])

    walk(product_tree)
    if not candidates:
        logger.error("Model not found: model_id=%s, version_id=%s", canonical_target_model_id, target_version_id)
        return None
    return candidates[-1]


def list_all_models(product_tree: list) -> list[dict]:
    result: list[dict] = []

    def walk(nodes: list) -> None:
        for node in nodes:
            if node.get("type") == "3":
                try:
                    resolved = extract_model_params(node)
                    model_id = resolved["model_id"]
                    credit = resolved["credit"]
                    attr_id = resolved["attribute_id"]
                except RuntimeError:
                    credit_rule = (node.get("credit_rules") or [{}])[0]
                    model_id = canonicalize_model_id(node.get("model_id", "")) or node.get("model_id", "")
                    credit = credit_rule.get("points", 0)
                    attr_id = credit_rule.get("attribute_id", 0)
                result.append(
                    {
                        "name": node.get("name", ""),
                        "model_id": model_id,
                        "version_id": node.get("id", ""),
                        "credit": credit,
                        "attr_id": attr_id,
                    }
                )
            walk(node.get("children") or [])

    walk(product_tree)
    return result


def resolve_virtual_param(field: dict) -> dict:
    field_name = field.get("field")
    ui_params = field.get("ui_params") or []
    mapping_rules = (field.get("value_mapping") or {}).get("mapping_rules") or []
    default_value = field.get("value")
    if not field_name:
        return {}

    if ui_params and mapping_rules:
        patch = {}
        for ui in ui_params:
            ui_field = ui.get("field") or ui.get("id", "")
            patch[ui_field] = ui.get("value")
        for rule in mapping_rules:
            source = rule.get("source_values") or {}
            if all(patch.get(k) == v for k, v in source.items()):
                return {field_name: rule.get("target_value")}

    if default_value is not None:
        return {field_name: default_value}
    return {}


def extract_virtual_param_specs(field: dict) -> list[dict]:
    field_name = field.get("field")
    mapping = field.get("value_mapping") or {}
    mapping_rules = mapping.get("mapping_rules") or []
    source_params = tuple(mapping.get("source_params") or [])
    target_param = mapping.get("target_param") or field_name
    if not field_name or not mapping_rules or not source_params or not target_param:
        return []

    normalized_rules = []
    for rule in mapping_rules:
        source_values = {
            key.lower().strip(): _normalize_value(value)
            for key, value in (rule.get("source_values") or {}).items()
        }
        if not source_values:
            continue
        normalized_rules.append(
            {
                "source_values": source_values,
                "target_value": rule.get("target_value"),
                "normalized_target_value": _normalize_value(rule.get("target_value")),
            }
        )

    if not normalized_rules:
        return []

    return [
        {
            "field": field_name,
            "target_param": str(target_param).lower().strip(),
            "source_params": tuple(str(param).lower().strip() for param in source_params),
            "mapping_rules": tuple(normalized_rules),
        }
    ]


def apply_virtual_param_specs(user_params: dict[str, Any], virtual_param_specs: list[dict]) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    effective = dict(user_params)
    applied: dict[str, dict[str, Any]] = {}

    for spec in virtual_param_specs or []:
        source_params = tuple(spec.get("source_params") or ())
        if not source_params:
            continue
        if not any(param in effective for param in source_params):
            continue

        normalized_user = {key.lower().strip(): _normalize_value(value) for key, value in effective.items()}
        matched_rule = None
        for rule in spec.get("mapping_rules") or ():
            source_values = rule.get("source_values") or {}
            if all(normalized_user.get(key) == value for key, value in source_values.items()):
                matched_rule = rule
                break

        if matched_rule is None:
            provided = ", ".join(
                f"{param}={effective[param]}"
                for param in source_params
                if param in effective
            )
            raise ValueError(f"Unsupported virtual parameter combination for {spec.get('target_param')}: {provided}")

        target_param = spec["target_param"]
        target_value = matched_rule["target_value"]
        normalized_target_value = matched_rule["normalized_target_value"]
        if target_param in effective and _normalize_value(effective[target_param]) != normalized_target_value:
            raise ValueError(
                f"Conflicting values for {target_param}: explicit={effective[target_param]} mapped={target_value}"
            )

        effective[target_param] = target_value
        for param in source_params:
            effective.pop(param, None)

        applied[target_param] = {
            "target_value": target_value,
            "source_values": dict(matched_rule["source_values"]),
            "source_params": source_params,
        }

    return effective, applied


def extract_model_params(node: dict) -> dict:
    credit_rules = node.get("credit_rules") or []
    if not credit_rules:
        raise RuntimeError(
            f"No credit_rules found for model '{node.get('model_id')}' version '{node.get('id')}'."
        )

    form_params: dict[str, Any] = {}
    virtual_param_specs: list[dict] = []
    field_option_specs: dict[str, tuple[str, ...]] = {}
    for field in node.get("form_config") or []:
        field_name = field.get("field")
        if not field_name:
            continue
        normalized_field_name = field_name.lower().strip()
        option_values = tuple(
            _normalize_value(option.get("value"))
            for option in (field.get("options") or [])
            if option.get("value") is not None
        )
        if option_values:
            field_option_specs[normalized_field_name] = option_values
        if field.get("is_ui_virtual", False):
            form_params.update(resolve_virtual_param(field))
            virtual_param_specs.extend(extract_virtual_param_specs(field))
        elif field.get("value") is not None:
            form_params[field_name] = field.get("value")

    normalized_form = {k.lower().strip(): _normalize_value(v) for k, v in form_params.items()}

    selected_rule = None
    for rule in credit_rules:
        attrs = {
            k.lower().strip(): _normalize_value(v)
            for k, v in (rule.get("attributes") or {}).items()
            if not (k == "default" and v == "enabled")
        }
        if all(normalized_form.get(k) == v for k, v in attrs.items()):
            selected_rule = rule
            break

    if not selected_rule:
        selected_rule = credit_rules[0]

    rule_attributes = {}
    for key, value in (selected_rule.get("attributes") or {}).items():
        if not (key == "default" and value == "enabled"):
            rule_attributes[key] = value

    return {
        "attribute_id": selected_rule.get("attribute_id", 0),
        "credit": selected_rule.get("points", 0),
        "model_id": canonicalize_model_id(node.get("model_id", "")) or node.get("model_id", ""),
        "model_name": node.get("name", ""),
        "model_version": node.get("id", ""),
        "form_params": form_params,
        "rule_attributes": rule_attributes,
        "all_credit_rules": credit_rules,
        "virtual_param_specs": virtual_param_specs,
        "field_option_specs": field_option_specs,
    }


def select_credit_rule_by_params(credit_rules: list, user_params: dict) -> dict | None:
    if not credit_rules:
        return None
    if not user_params:
        return credit_rules[0]

    normalized_user = {k.lower().strip(): _normalize_value(v) for k, v in user_params.items()}
    for rule in credit_rules:
        attrs = {k.lower().strip(): _normalize_value(v) for k, v in (rule.get("attributes") or {}).items()}
        if all(normalized_user.get(k) == v for k, v in attrs.items()):
            return rule

    return credit_rules[0]
