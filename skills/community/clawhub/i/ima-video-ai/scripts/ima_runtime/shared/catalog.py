from __future__ import annotations

import logging
import re


logger = logging.getLogger("ima_skills")

MODEL_ID_ALIASES = {
    "ima sevio 1.0": "ima-pro",
    "ima sevio 1.0-fast": "ima-pro-fast",
    "ima sevio 1.0 fast": "ima-pro-fast",
    "seedance 2.0": "ima-pro",
    "seedance 2.0-fast": "ima-pro-fast",
    "seedance 2.0 fast": "ima-pro-fast",
}


def canonicalize_model_id(model_id: str | None) -> str | None:
    if not model_id:
        return None
    normalized_key = re.sub(r"\s+", " ", model_id.strip().lower())
    return MODEL_ID_ALIASES.get(normalized_key, model_id.strip())


normalize_model_id = canonicalize_model_id


def find_model_version(product_tree: list, target_model_id: str,
                       target_version_id: str | None = None) -> dict | None:
    """
    Walk the V2 tree and find a type=3 leaf node matching target_model_id.
    If target_version_id is given, match exactly; otherwise return the last
    (usually newest) matching version.

    Key insight from imagent.bot frontend:
      modelItem.key       → node["id"]          (= model_version in create request)
      modelItem.modelCodeId → node["model_id"]   (= model_id in create request)
      modelItem.name      → node["name"]         (= model_name in create request)
    """
    candidates = []
    canonical_target_model_id = normalize_model_id(target_model_id) or target_model_id

    def walk(nodes: list):
        for node in nodes:
            if node.get("type") == "3":
                mid = node.get("model_id", "")
                normalized_mid = normalize_model_id(mid) or mid
                vid = node.get("id", "")
                if normalized_mid == canonical_target_model_id:
                    if target_version_id is None or vid == target_version_id:
                        candidates.append(node)
            children = node.get("children") or []
            walk(children)

    walk(product_tree)

    if not candidates:
        logger.error(
            f"Model not found: model_id={canonical_target_model_id}, "
            f"version_id={target_version_id}"
        )
        return None

    # Return last match — product list is ordered oldest→newest, last = newest
    selected = candidates[-1]
    logger.info(
        f"Model found: {selected.get('name')} "
        f"(model_id={canonical_target_model_id}, version_id={selected.get('id')})"
    )
    return selected


def list_all_models(product_tree: list) -> list[dict]:
    """Flatten tree to a list of {name, model_id, version_id, credit} dicts."""
    result = []

    def walk(nodes):
        for node in nodes:
            if node.get("type") == "3":
                cr = (node.get("credit_rules") or [{}])[0]
                raw_model_id = node.get("model_id", "")
                canonical_model_id = normalize_model_id(raw_model_id) or raw_model_id
                result.append({
                    "name":       node.get("name", ""),
                    "model_id":   canonical_model_id,
                    "raw_model_id": raw_model_id,
                    "version_id": node.get("id", ""),
                    "credit":     cr.get("points", 0),
                    "attr_id":    cr.get("attribute_id", 0),
                    "model_types": list(node.get("model_types") or []),
                    "files_accept_types": list((node.get("files") or {}).get("acceptType") or []),
                    "form_fields": [field.get("field") for field in (node.get("form_config") or []) if field.get("field")],
                })
            walk(node.get("children") or [])

    walk(product_tree)
    return result


def resolve_virtual_param(field: dict) -> dict:
    """
    Handle virtual form fields (is_ui_virtual=True).

    Frontend logic (useAgentModeData.ts):
      1. Create sub-forms from ui_params (each has a default value)
      2. Build patch: {ui_param.field: ui_param.value} for each sub-param
      3. Find matching value_mapping rule where source_values == patch
      4. Use target_value as the actual API parameter value

    If is_ui_virtual is not exposed by Open API, fall through to default value.
    """
    field_name     = field.get("field")
    ui_params      = field.get("ui_params") or []
    value_mapping  = field.get("value_mapping") or {}
    mapping_rules  = value_mapping.get("mapping_rules") or []
    default_value  = field.get("value")

    if not field_name:
        return {}

    if ui_params and mapping_rules:
        # Build patch from ui_params default values
        patch = {}
        for ui in ui_params:
            ui_field = ui.get("field") or ui.get("id", "")
            patch[ui_field] = ui.get("value")

        # Find matching mapping rule
        for rule in mapping_rules:
            source = rule.get("source_values") or {}
            if all(patch.get(k) == v for k, v in source.items()):
                return {field_name: rule.get("target_value")}

    # Fallback: use the field's own default value
    if default_value is not None:
        return {field_name: default_value}
    return {}


def apply_virtual_param_overrides(virtual_fields: list[dict], params: dict) -> dict:
    """
    Apply ui_params -> target_value mapping for user-provided overrides.

    This complements resolve_virtual_param(), which only resolves default values
    from form_config. When users provide UI-facing sub-params such as
    {"quality":"1080p"}, this function remaps them to the backend-facing target
    param such as {"mode":"pro"} before rule matching and payload assembly.
    """
    resolved = dict(params)
    for field in virtual_fields or []:
        field_name = field.get("field")
        ui_params = field.get("ui_params") or []
        value_mapping = field.get("value_mapping") or {}
        mapping_rules = value_mapping.get("mapping_rules") or []
        if not field_name or not ui_params or not mapping_rules:
            continue

        ui_field_names = [ui.get("field") or ui.get("id", "") for ui in ui_params if ui.get("field") or ui.get("id")]
        if not any(name in resolved for name in ui_field_names):
            continue

        patch = {}
        for ui in ui_params:
            ui_field = ui.get("field") or ui.get("id", "")
            if not ui_field:
                continue
            if ui_field in resolved:
                patch[ui_field] = resolved[ui_field]
            else:
                patch[ui_field] = ui.get("value")

        matched_rule = None
        for rule in mapping_rules:
            source = rule.get("source_values") or {}
            if all(patch.get(k) == v for k, v in source.items()):
                matched_rule = rule
                break

        if matched_rule is None:
            raise ValueError(
                f"No value_mapping rule matched virtual field '{field_name}' for ui params {patch}"
            )

        mapped_target = matched_rule.get("target_value")
        if field_name in resolved and field_name not in ui_field_names and resolved[field_name] != mapped_target:
            raise ValueError(
                f"Conflicting values for virtual field '{field_name}': "
                f"explicit={resolved[field_name]!r} mapped={mapped_target!r}"
            )

        resolved[field_name] = mapped_target
        for ui_field_name in ui_field_names:
            if ui_field_name != field_name:
                resolved.pop(ui_field_name, None)

    return resolved


def extract_model_params(node: dict) -> dict:
    """
    Extract everything needed for the create task request from a product list leaf node.

    Returns:
      attribute_id  : int   — from credit_rules[0].attribute_id
      credit        : int   — from credit_rules[0].points
      model_id      : str   — node["model_id"]
      model_name    : str   — node["name"]
      model_version : str   — node["id"]  ← CRITICAL: this is what backend calls model_version_id
      form_params   : dict  — resolved form_config defaults (including virtual params)
    """
    credit_rules = node.get("credit_rules") or []
    if not credit_rules:
        raise RuntimeError(
            f"No credit_rules found for model '{node.get('model_id')}' "
            f"version '{node.get('id')}'. Cannot determine attribute_id or credit."
        )

    # Build form_config defaults FIRST (before selecting credit_rule)
    form_params: dict = {}
    for field in (node.get("form_config") or []):
        fname = field.get("field")
        if not fname:
            continue

        is_virtual = field.get("is_ui_virtual", False)
        if is_virtual:
            # Apply virtual param resolution (frontend logic)
            resolved = resolve_virtual_param(field)
            form_params.update(resolved)
        else:
            fvalue = field.get("value")
            if fvalue is not None:
                form_params[fname] = fvalue

    # 🆕 CRITICAL FIX: Select the correct credit_rule based on form_params
    # Don't always use credit_rules[0] - match form_params to rule.attributes
    selected_rule = None

    # Normalize form_params for matching
    def normalize_value(v):
        if isinstance(v, bool):
            return str(v).lower()
        return str(v).strip().upper()

    normalized_form = {
        k.lower().strip(): normalize_value(v)
        for k, v in form_params.items()
    }

    # Try to find a rule that matches form_params
    for cr in credit_rules:
        attrs = cr.get("attributes", {})
        if not attrs:
            continue

        normalized_attrs = {
            k.lower().strip(): normalize_value(v)
            for k, v in attrs.items()
            if not (k == "default" and v == "enabled")  # Skip markers
        }

        # Check if rule attributes match form_params
        match = all(
            normalized_form.get(k) == v
            for k, v in normalized_attrs.items()
        )

        if match:
            selected_rule = cr
            logger.info(f"🎯 Matched credit_rule by form_params: attribute_id={cr.get('attribute_id')}, "
                       f"attrs={attrs}")
            break

    # Fallback to first rule if no match
    if not selected_rule:
        selected_rule = credit_rules[0]
        logger.warning(f"⚠️  No credit_rule matched form_params, using first rule (attribute_id={selected_rule.get('attribute_id')})")

    attribute_id = selected_rule.get("attribute_id", 0)
    credit = selected_rule.get("points", 0)

    if attribute_id == 0:
        raise RuntimeError(
            f"attribute_id is 0 for model '{node.get('model_id')}'. "
            "This will cause 'Invalid product attribute' error."
        )

    # ✅ Extract rule_attributes from the SELECTED rule (not always credit_rules[0])
    rule_attributes: dict = {}
    rule_attrs = selected_rule.get("attributes", {})

    # Filter out {"default": "enabled"} marker (not an actual parameter)
    for key, value in rule_attrs.items():
        if not (key == "default" and value == "enabled"):
            rule_attributes[key] = value

    raw_model_id = node.get("model_id", "")
    canonical_model_id = normalize_model_id(raw_model_id) or raw_model_id

    logger.info(
        f"Params extracted: model={canonical_model_id}, raw_model={raw_model_id}, "
        f"attribute_id={attribute_id}, credit={credit}, "
        f"rule_attrs={len(rule_attributes)} fields"
    )

    return {
        "attribute_id":     attribute_id,
        "credit":           credit,
        "model_id":         canonical_model_id,
        "model_id_raw":     raw_model_id,
        "model_name":       node.get("name", ""),
        "model_version":    node.get("id", ""),   # ← version_id from product list
        "form_params":      form_params,
        "rule_attributes":  rule_attributes,  # ✅ NEW: required params from attributes
        "all_credit_rules": credit_rules,     # For smart selection
        "virtual_fields":   [field for field in (node.get("form_config") or []) if field.get("is_ui_virtual")],
        "model_types":      list(node.get("model_types") or []),
        "files_accept_types": list((node.get("files") or {}).get("acceptType") or []),
        "form_fields":      [field.get("field") for field in (node.get("form_config") or []) if field.get("field")],
    }


def select_credit_rule_by_params(credit_rules: list, user_params: dict) -> dict | None:
    """
    Select the best credit_rule matching user parameters.

    CRITICAL FIX (error 6010): Must match ALL attributes in credit_rule, not just user params.
    Backend validation checks if request params match the rule's attributes exactly.

    Strategy:
    1. Try exact match: ALL rule attributes match user params (bidirectional)
    2. Try partial match: rule attributes are subset of user params
    3. Fallback: first rule (default)

    Returns the selected credit_rule or None if credit_rules is empty.
    """
    if not credit_rules:
        return None

    if not user_params:
        return credit_rules[0]

    # Normalize user params (handle bool → lowercase string for JSON comparison consistency)
    def normalize_value(v):
        if isinstance(v, bool):
            return str(v).lower()  # False → "false", True → "true"
        # CRITICAL FIX: Case-insensitive matching for resolution/duration/size values
        # User may pass "1080p" but rules define "1080P", or "5s" vs "5S"
        return str(v).strip().upper()  # "1080p" → "1080P", "5s" → "5S"

    normalized_user = {
        k.lower().strip(): normalize_value(v)
        for k, v in user_params.items()
    }

    # Try exact match: ALL rule attributes must match user params
    # This ensures backend validation passes (error 6010 prevention)
    for cr in credit_rules:
        attrs = cr.get("attributes", {})
        if not attrs:
            continue

        normalized_attrs = {
            k.lower().strip(): normalize_value(v)
            for k, v in attrs.items()
        }

        # CRITICAL: Check if ALL rule attributes are in user params AND match
        # (Not just if user params are in rule attributes)
        if all(normalized_user.get(k) == v for k, v in normalized_attrs.items()):
            return cr

    # Try partial match (at least some attributes match)
    best_match = None
    best_match_count = 0

    for cr in credit_rules:
        attrs = cr.get("attributes", {})
        if not attrs:
            continue

        normalized_attrs = {
            k.lower().strip(): normalize_value(v)
            for k, v in attrs.items()
        }

        # Count how many attributes match
        match_count = sum(1 for k, v in normalized_attrs.items()
                         if normalized_user.get(k) == v)

        if match_count > best_match_count:
            best_match_count = match_count
            best_match = cr

    if best_match:
        return best_match

    # Fallback to first rule
    return credit_rules[0]
