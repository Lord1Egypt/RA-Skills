"""
IMA Parameter Resolver Module
Version: 1.0.0

Handles parameter extraction and credit_rule matching from product list data.
Includes virtual parameter resolution and smart credit_rule selection.
"""

from ima_constants import normalize_model_id, ALLOWED_MODEL_IDS
from ima_logger import get_logger

logger = get_logger()

# ─── Virtual Parameter Resolution ────────────────────────────────────────────

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

# ─── Model Parameter Extraction ──────────────────────────────────────────────

def extract_model_params(node: dict, user_params: dict | None = None) -> dict:
    """
    Extract everything needed for the create task request from a product list leaf node.
    
    NEW: Accepts user_params to select the correct credit_rule based on user's actual parameters.

    Returns:
      attribute_id  : int   — from matched credit_rule.attribute_id
      credit        : int   — from matched credit_rule.points
      model_id      : str   — node["model_id"]
      model_name    : str   — node["name"]
      model_version : str   — node["id"]
      form_params   : dict  — resolved form_config defaults (including virtual params)
      rule_attributes: dict — required parameters from the matched credit_rule
      all_credit_rules: list — All available credit_rules for smart selection
    """
    credit_rules = node.get("credit_rules") or []
    if not credit_rules:
        raise RuntimeError(
            f"No credit_rules found for model '{node.get('model_id')}' "
            f"version '{node.get('id')}'. Cannot determine attribute_id or credit."
        )

    form_params: dict = {}
    for field in (node.get("form_config") or []):
        fname = field.get("field")
        if not fname:
            continue

        is_virtual = field.get("is_ui_virtual", False)
        if is_virtual:
            resolved = resolve_virtual_param(field)
            form_params.update(resolved)
        else:
            fvalue = field.get("value")
            if fvalue is not None:
                form_params[fname] = fvalue

    # Merge user params with form defaults (user params take priority)
    if user_params:
        merged_params = {**form_params, **user_params}
    else:
        merged_params = form_params
    
    selected_rule = None
    
    def normalize_value(v):
        if isinstance(v, bool):
            return str(v).lower()
        return str(v).strip().upper()
    
    normalized_merged = {
        k.lower().strip(): normalize_value(v)
        for k, v in merged_params.items()
    }
    
    for cr in credit_rules:
        attrs = cr.get("attributes", {})
        if not attrs:
            continue
        
        normalized_attrs = {
            k.lower().strip(): normalize_value(v)
            for k, v in attrs.items()
            if not (k == "default" and v == "enabled")
        }
        
        match = all(
            normalized_merged.get(k) == v
            for k, v in normalized_attrs.items()
        )
        
        if match:
            selected_rule = cr
            logger.info(f"✅ Matched credit_rule: attribute_id={cr.get('attribute_id')}, "
                       f"attrs={attrs}")
            break
    
    if not selected_rule:
        selected_rule = credit_rules[0]
        logger.warning(f"⚠️  No credit_rule matched merged params, using first rule (attribute_id={selected_rule.get('attribute_id')})")
        logger.warning(f"⚠️  Available credit_rules: {len(credit_rules)} rules")
        for i, cr in enumerate(credit_rules):
            logger.warning(f"     Rule {i+1}: attribute_id={cr.get('attribute_id')}, points={cr.get('points')}, attrs={cr.get('attributes')}")

    
    attribute_id = selected_rule.get("attribute_id", 0)
    credit = selected_rule.get("points", 0)

    if attribute_id == 0:
        raise RuntimeError(
            f"attribute_id is 0 for model '{node.get('model_id')}'. "
            "This will cause 'Invalid product attribute' error."
        )

    rule_attributes: dict = {}
    rule_attrs = selected_rule.get("attributes", {})
    
    for key, value in rule_attrs.items():
        if not (key == "default" and value == "enabled"):
            rule_attributes[key] = value

    raw_model_id = node.get("model_id", "")
    canonical_model_id = normalize_model_id(raw_model_id) or raw_model_id

    logger.info(
        f"Params extracted: model={canonical_model_id}, raw_model={raw_model_id}, "
        f"attribute_id={attribute_id}, credit={credit}, rule_attrs={len(rule_attributes)} fields"
    )

    return {
        "attribute_id":     attribute_id,
        "credit":           credit,
        "model_id":         canonical_model_id,
        "model_id_raw":     raw_model_id,
        "model_name":       node.get("name", ""),
        "model_version":    node.get("id", ""),
        "form_params":      form_params,
        "rule_attributes":  rule_attributes,
        "all_credit_rules": credit_rules,
    }

# ─── Smart Credit Rule Selection ─────────────────────────────────────────────

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
    
    def normalize_value(v):
        if isinstance(v, bool):
            return str(v).lower()
        return str(v).strip().upper()
    
    normalized_user = {
        k.lower().strip(): normalize_value(v)
        for k, v in user_params.items()
    }
    
    # ─── Strategy 1: Exact bidirectional match ───────────────────────────────
    # Both rule attributes and user params must match exactly (no extra params allowed)
    for cr in credit_rules:
        attrs = cr.get("attributes", {})
        if not attrs:
            continue
        
        normalized_attrs = {
            k.lower().strip(): normalize_value(v)
            for k, v in attrs.items()
        }
        
        # DEBUG: Print matching process
        forward_match = all(normalized_user.get(k) == v for k, v in normalized_attrs.items())
        backward_match = all(k in normalized_attrs for k in normalized_user.keys())
        
        print(f"  Rule {cr.get('attribute_id')}: forward={forward_match}, backward={backward_match}")
        print(f"    rule_attrs: {normalized_attrs}")
        print(f"    user_params: {normalized_user}")
        
        # Bidirectional check:
        # 1. All rule attributes must match user params (forward)
        # 2. All user params must be in rule attributes (backward, no extras)
        if forward_match and backward_match:
            print(f"  ✅ MATCHED: attribute_id={cr.get('attribute_id')}")
            return cr
    
    # ─── Strategy 2: Partial match (rule attributes subset of user params) ───
    # Only used if no exact bidirectional match found
    # Rule attributes must match user params, but user can have extra params
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
        
        # Count matching attributes
        match_count = sum(1 for k, v in normalized_attrs.items() 
                         if normalized_user.get(k) == v)
        
        if match_count > best_match_count:
            best_match_count = match_count
            best_match = cr
    
    if best_match:
        print(f"  ⚠️ PARTIAL MATCH: attribute_id={best_match.get('attribute_id')} (matched {best_match_count} fields)")
        return best_match
    
    # ─── Strategy 3: Fallback to default (first rule) ────────────────────────
    print(f"  ⚠️ NO MATCH: using default rule (attribute_id={credit_rules[0].get('attribute_id')})")
    return credit_rules[0]
