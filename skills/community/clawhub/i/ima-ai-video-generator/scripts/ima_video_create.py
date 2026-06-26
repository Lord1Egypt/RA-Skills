#!/usr/bin/env python3
"""
IMA Video Creation Script — ima_video_create.py
Version: 1.0.8

Video generation via IMA Open API.
Flow: product list → virtual param resolution → task create → poll status.

- Task types: text_to_video | image_to_video | first_last_frame_to_video | reference_image_to_video
- --input-images: accepts HTTPS URLs or local file paths (local files auto-uploaded to IMA CDN).

Usage:
  python3 ima_video_create.py --api-key ima_xxx --task-type text_to_video \\
    --model-id wan2.6-t2v --prompt "a cute puppy"

Logs: ~/.openclaw/logs/ima_skills/ima_create_YYYYMMDD.log
"""

import argparse
import hashlib
import json
import mimetypes
import os
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("requests not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)

# Import logger module
try:
    from ima_logger import setup_logger, cleanup_old_logs
    logger = setup_logger("ima_skills")
    cleanup_old_logs(days=7)
except ImportError:
    # Fallback: create basic logger if ima_logger not available
    import logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)-5s | %(funcName)-20s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logger = logging.getLogger("ima_skills")

# ─── Constants ────────────────────────────────────────────────────────────────

# Primary API endpoint (owned by IMA Studio)
DEFAULT_BASE_URL = "https://api.imastudio.com"

# Image upload endpoint (owned by IMA Studio)
# Used for: image_to_video, first_last_frame_to_video, reference_image_to_video
# Purpose: Upload images to OSS to obtain CDN URLs for video generation
# See SECURITY.md for full domain disclosure and privacy implications
DEFAULT_IM_BASE_URL = "https://imapi.liveme.com"

PREFS_PATH = os.path.expanduser("~/.openclaw/memory/ima_prefs.json")

# Poll interval (seconds) and max wait (seconds) per task type
POLL_CONFIG = {
    "text_to_video":             {"interval": 8,  "max_wait": 600},
    "image_to_video":            {"interval": 8,  "max_wait": 600},
    "first_last_frame_to_video": {"interval": 8,  "max_wait": 600},
    "reference_image_to_video":  {"interval": 8,  "max_wait": 600},
}

# App Key configuration (for OSS upload authentication)
# These are shared keys used by all IMA skill-based uploads
# NOT a secret - visible in public source code
# Used to generate request signatures for imapi.liveme.com upload API
# See SECURITY.md § "Credentials" for security implications
APP_ID = "webAgent"
APP_KEY = "32jdskjdk320eew"


# ─── HTTP helpers ─────────────────────────────────────────────────────────────

def make_headers(api_key: str, language: str = "en") -> dict:
    return {
        "Authorization":  f"Bearer {api_key}",
        "Content-Type":   "application/json",
        "x-app-source":   "ima_skills",
        "x_app_language": language,
    }


# ─── Image Upload (OSS) ───────────────────────────────────────────────────────

def _gen_sign() -> tuple[str, str, str]:
    """Generate per-request (sign, timestamp, nonce) for IM authentication."""
    nonce = uuid.uuid4().hex[:21]
    ts = str(int(time.time()))
    raw = f"{APP_ID}|{APP_KEY}|{ts}|{nonce}"
    sign = hashlib.sha1(raw.encode()).hexdigest().upper()
    return sign, ts, nonce


def get_upload_token(api_key: str, suffix: str, 
                     content_type: str, im_base_url: str = DEFAULT_IM_BASE_URL) -> dict:
    """
    Step 1: Get presigned upload URL from IM platform (imapi.liveme.com).
    
    **Security Note**: This function sends your IMA API key to imapi.liveme.com,
    which is IMA Studio's dedicated image upload service (separate from the main API).
    
    Why the API key is sent here:
    - imapi.liveme.com is owned and operated by IMA Studio
    - The upload service authenticates requests using the same IMA API key
    - This allows secure, authenticated image uploads without separate credentials
    - Images are stored in IMA's OSS infrastructure and returned as CDN URLs
    
    The two-domain architecture separates concerns:
    - api.imastudio.com: Video generation API (task orchestration)
    - imapi.liveme.com: Media storage API (large file uploads)
    
    See SECURITY.md § "Network Endpoints Used" for full disclosure.
    
    Args:
        api_key: IMA API key (used as both appUid and cmimToken for authentication)
        suffix: File extension (e.g., "jpg", "png")
        content_type: MIME type (e.g., "image/jpeg")
        im_base_url: IM upload service URL (default: https://imapi.liveme.com)
    
    Returns: 
        dict with keys:
        - "ful": Presigned PUT URL for uploading raw bytes
        - "fdl": CDN download URL for the uploaded file
    
    Raises:
        RuntimeError: If upload token request fails
    """
    sign, ts, nonce = _gen_sign()
    
    url = f"{im_base_url}/api/rest/oss/getuploadtoken"
    params = {
        "appUid": api_key,
        "appId": APP_ID,
        "appKey": APP_KEY,
        "cmimToken": api_key,
        "sign": sign,
        "timestamp": ts,
        "nonce": nonce,
        "fService": "privite",
        "fType": "picture",
        "fSuffix": suffix,
        "fContentType": content_type,
    }
    
    logger.info(f"Getting upload token: suffix={suffix}")
    
    try:
        resp = requests.get(url, params=params, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        if data.get("code") != 0:
            raise RuntimeError(f"Get upload token failed: {data.get('message')}")
        
        return data.get("data", {})
    except requests.RequestException as e:
        logger.error(f"Failed to get upload token: {e}")
        raise RuntimeError(f"Failed to get upload token: {e}")


def upload_to_oss(image_bytes: bytes, content_type: str, ful: str) -> None:
    """Step 2: PUT image bytes to the presigned OSS URL."""
    logger.info(f"Uploading {len(image_bytes)} bytes to OSS...")
    
    try:
        resp = requests.put(ful, data=image_bytes, 
                           headers={"Content-Type": content_type}, timeout=60)
        resp.raise_for_status()
        logger.info("Upload successful")
    except requests.RequestException as e:
        logger.error(f"Upload failed: {e}")
        raise RuntimeError(f"Upload failed: {e}")


def prepare_image_url(source: str | bytes, api_key: str,
                      im_base_url: str = DEFAULT_IM_BASE_URL) -> str:
    """
    Convert any image source to a public HTTPS CDN URL.
    
    - If source is already HTTPS URL → return as-is
    - If source is local file/bytes → upload to OSS first
    """
    # Already a public URL
    if isinstance(source, str) and source.startswith("https://"):
        logger.info(f"Using URL directly: {source[:50]}...")
        return source
    
    # Need to upload
    if not api_key:
        raise RuntimeError("Local image upload requires IMA API key (--api-key)")
    
    # Read file bytes
    if isinstance(source, str):
        if not os.path.isfile(source):
            raise RuntimeError(f"Image file not found: {source}")
        
        ext = Path(source).suffix.lstrip(".").lower() or "jpeg"
        with open(source, "rb") as f:
            image_bytes = f.read()
        content_type = mimetypes.guess_type(source)[0] or "image/jpeg"
        logger.info(f"Read local file: {source} ({len(image_bytes)} bytes)")
    else:
        image_bytes = source
        ext = "jpeg"
        content_type = "image/jpeg"
        logger.info(f"Using raw bytes ({len(image_bytes)} bytes)")
    
    # Upload workflow
    token_data = get_upload_token(api_key, ext, content_type, im_base_url)
    ful = token_data.get("ful")
    fdl = token_data.get("fdl")
    
    if not ful or not fdl:
        raise RuntimeError("Upload token missing 'ful' or 'fdl' field")
    
    upload_to_oss(image_bytes, content_type, ful)
    logger.info(f"Image uploaded: {fdl[:50]}...")
    return fdl


# ─── Step 1: Product List ─────────────────────────────────────────────────────

def get_product_list(base_url: str, api_key: str, category: str,
                     app: str = "ima", platform: str = "web",
                     language: str = "en") -> list:
    """
    GET /open/v1/product/list
    Returns the V2 tree: type=2 are model groups, type=3 are versions (leaves).
    Only type=3 nodes have credit_rules and form_config.
    """
    url     = f"{base_url}/open/v1/product/list"
    params  = {"app": app, "platform": platform, "category": category}
    headers = make_headers(api_key, language)

    logger.info(f"Query product list: category={category}, app={app}, platform={platform}")
    
    try:
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        code = data.get("code")
        if code not in (0, 200):
            error_msg = f"Product list API error: code={code}, msg={data.get('message')}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

        products_count = len(data.get("data") or [])
        logger.info(f"Product list retrieved successfully: {products_count} groups found")
        return data.get("data") or []
        
    except requests.RequestException as e:
        logger.error(f"Product list request failed: {str(e)}")
        raise


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

    def walk(nodes: list):
        for node in nodes:
            if node.get("type") == "3":
                mid = node.get("model_id", "")
                vid = node.get("id", "")
                if mid == target_model_id:
                    if target_version_id is None or vid == target_version_id:
                        candidates.append(node)
            children = node.get("children") or []
            walk(children)

    walk(product_tree)

    if not candidates:
        logger.error(f"Model not found: model_id={target_model_id}, version_id={target_version_id}")
        return None
    
    # Return last match — product list is ordered oldest→newest, last = newest
    selected = candidates[-1]
    logger.info(f"Model found: {selected.get('name')} (model_id={target_model_id}, version_id={selected.get('id')})")
    return selected


def list_all_models(product_tree: list) -> list[dict]:
    """Flatten tree to a list of {name, model_id, version_id, credit} dicts."""
    result = []

    def walk(nodes):
        for node in nodes:
            if node.get("type") == "3":
                cr = (node.get("credit_rules") or [{}])[0]
                result.append({
                    "name":       node.get("name", ""),
                    "model_id":   node.get("model_id", ""),
                    "version_id": node.get("id", ""),
                    "credit":     cr.get("points", 0),
                    "attr_id":    cr.get("attribute_id", 0),
                })
            walk(node.get("children") or [])

    walk(product_tree)
    return result


# ─── Step 2: Extract Parameters (including virtual param resolution) ──────────

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

    logger.info(f"Params extracted: model={node.get('model_id')}, attribute_id={attribute_id}, "
                f"credit={credit}, rule_attrs={len(rule_attributes)} fields")

    return {
        "attribute_id":     attribute_id,
        "credit":           credit,
        "model_id":         node.get("model_id", ""),
        "model_name":       node.get("name", ""),
        "model_version":    node.get("id", ""),   # ← version_id from product list
        "form_params":      form_params,
        "rule_attributes":  rule_attributes,  # ✅ NEW: required params from attributes
        "all_credit_rules": credit_rules,     # For smart selection
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
    
    # Normalize user params (handle bool → lowercase string for JSON compatibility)
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


# ─── Step 3: Create Task ──────────────────────────────────────────────────────

def create_task(base_url: str, api_key: str,
                task_type: str, model_params: dict,
                prompt: str,
                input_images: list[str] | None = None,
                extra_params: dict | None = None) -> str:
    """
    POST /open/v1/tasks/create

    Constructs the full request body as the imagent.bot frontend does:
      parameters[i].model_version = modelItem.key = node["id"] (version_id)
      parameters[i].attribute_id  = creditInfo.attributeId
      parameters[i].credit        = creditInfo.credits
      parameters[i].parameters    = { ...form_config_defaults,
                                       prompt, input_images, cast, n }
    
    NEW: Supports smart credit_rule selection based on user params (e.g., size: "4K").
    """
    if input_images is None:
        input_images = []

    # Smart credit_rule selection based on user params
    all_rules = model_params.get("all_credit_rules", [])
    normalized_rule_params = {}  # 🆕 Store normalized params from matched rule
    
    if all_rules:  # ← FIX: Always try smart selection
        # Extract params that might be in attributes
        # CRITICAL: ONLY include keys that actually appear in credit_rules.attributes
        # EXCLUDE form_config defaults like aspect_ratio, shot_type (not in attributes!)
        # 
        # Video credit_rules.attributes typically use:
        #   - duration, resolution, generate_audio (common)
        #   - sound, mode (Kling-specific)
        #   - fast_pretreatment, prompt_optimizer (Hailuo-specific)
        #
        # Image credit_rules.attributes typically use:
        #   - size, quality, n
        # Merge form_params and extra_params for matching
        merged_params = {**model_params.get('form_params', {}), **(extra_params or {})}
        candidate_params = {k: v for k, v in merged_params.items() 
                          if k in ["size", "quality", "resolution", "n",
                                   "duration", "generate_audio",
                                   "sound", "mode",
                                   "fast_pretreatment", "prompt_optimizer"]}
        # ⚠️ REMOVED: aspect_ratio, shot_type, compression_quality, sample_image_size
        #    These are form_config defaults, NOT used in credit_rules matching!
        if candidate_params:
            selected_rule = select_credit_rule_by_params(all_rules, candidate_params)
            if selected_rule:
                attribute_id = selected_rule.get("attribute_id", model_params["attribute_id"])
                credit = selected_rule.get("points", model_params["credit"])
                
                # 🆕 CRITICAL FIX: Use normalized values from the matched rule's attributes
                # This ensures API gets "1080P" (from rule) instead of "1080p" (from user)
                rule_attrs = selected_rule.get("attributes", {})
                valid_keys = ["size", "quality", "resolution", "n",
                             "duration", "generate_audio", "sound", "mode",
                             "fast_pretreatment", "prompt_optimizer"]
                for key in valid_keys:
                    if key in rule_attrs:
                        normalized_rule_params[key] = rule_attrs[key]
                
                print(f"🎯 Smart credit_rule selection: {candidate_params} → attribute_id={attribute_id}, credit={credit} pts", flush=True)
                if normalized_rule_params:
                    print(f"   📝 Normalized params from rule: {normalized_rule_params}", flush=True)
            else:
                attribute_id = model_params["attribute_id"]
                credit = model_params["credit"]
        else:
            attribute_id = model_params["attribute_id"]
            credit = model_params["credit"]
    else:
        attribute_id = model_params["attribute_id"]
        credit = model_params["credit"]

    # ✅ FIX for error 6009: Merge parameters in correct priority order
    # Priority (low → high): rule_attributes < form_params < normalized_rule_params < extra_params (non-rule keys)
    # This ensures backend validation always gets required fields from attributes
    inner: dict = {}
    
    # 1. First merge rule_attributes (required fields from credit_rules, lowest priority)
    rule_attrs = model_params.get("rule_attributes", {})
    if rule_attrs:
        inner.update(rule_attrs)
    
    # 2. Then merge form_config defaults (optional fields, medium priority)
    inner.update(model_params["form_params"])
    
    # 3. Merge normalized params from matched rule (higher priority - these are canonical values)
    # 🆕 CRITICAL: This overwrites user's "1080p" with rule's "1080P" to match attribute_id
    if normalized_rule_params:
        inner.update(normalized_rule_params)
    
    # 4. Finally merge user overrides for non-rule keys (highest priority for non-canonical fields)
    # Only merge keys that are NOT in normalized_rule_params to preserve canonical values
    if extra_params:
        for key, value in extra_params.items():
            if key not in normalized_rule_params:  # Don't override canonical rule values
                inner[key] = value

    # Required inner fields (always set these)
    inner["prompt"]       = prompt
    inner["n"]            = int(inner.get("n", 1))
    inner["input_images"] = input_images
    inner["cast"]         = {"points": credit, "attribute_id": attribute_id}
    
    # 🆕 CRITICAL: Preserve model parameter from form_config if present
    # Some models (e.g. Pixverse) use the same model_id but distinguish versions via this parameter
    # Example: model_id="pixverse" with model="v5.5" | "v5" | "v4.5" | "v4" | "v3.5"
    # Priority: form_config default < user override (if provided)
    if "model" in model_params.get("form_params", {}):
        # Use default from form_config (e.g. "v5.5")
        inner["model"] = model_params["form_params"]["model"]
    if extra_params and "model" in extra_params:
        # Allow user to explicitly override the version
        inner["model"] = extra_params["model"]
    
    # 🆕 CRITICAL: Auto-infer model parameter for Pixverse if missing
    # Pixverse V5.5/V5/V4 don't have model in form_config, but backend requires it
    # Error: "Invalid value for model" or "The Fusion feature is supported in model v4.5, v5, v5.5 and v5.6 only"
    if model_params.get("model_id") == "pixverse" and "model" not in inner:
        # Extract version from model_name: "Pixverse V5.5" → "v5.5"
        model_name = model_params.get("model_name", "")
        import re
        version_match = re.search(r'V(\d+(?:\.\d+)?)', model_name, re.IGNORECASE)
        if version_match:
            version = version_match.group(1)  # "5.5", "5", "4.5", "4", "3.5"
            inner["model"] = f"v{version}"
            print(f"🔧 Auto-inferred Pixverse model parameter: model=\"v{version}\" (from model_name=\"{model_name}\")", flush=True)

    payload = {
        "task_type":          task_type,
        "enable_multi_model": False,
        "src_img_url":        input_images,
        "parameters": [{
            "attribute_id":  attribute_id,
            "model_id":      model_params["model_id"],
            "model_name":    model_params["model_name"],
            "model_version": model_params["model_version"],   # ← version_id (NOT model_id!)
            "app":           "ima",
            "platform":      "web",
            "category":      task_type,
            "credit":        credit,
            "parameters":    inner,
        }],
    }

    url     = f"{base_url}/open/v1/tasks/create"
    headers = make_headers(api_key)

    logger.info(f"Create task: model={model_params['model_name']}, task_type={task_type}, "
                f"credit={credit}, attribute_id={attribute_id}")

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        code = data.get("code")
        if code not in (0, 200):
            logger.error(f"Task create failed: code={code}, msg={data.get('message')}, "
                        f"attribute_id={attribute_id}, credit={credit}")
            raise RuntimeError(
                f"Create task failed — code={code} "
                f"message={data.get('message')} "
                f"request={json.dumps(payload, ensure_ascii=False)}"
            )

        task_id = (data.get("data") or {}).get("id")
        if not task_id:
            logger.error("Task create failed: no task_id in response")
            raise RuntimeError(f"No task_id in response: {data}")

        logger.info(f"Task created: task_id={task_id}")
        return task_id
        
    except requests.RequestException as e:
        logger.error(f"Task create request failed: {str(e)}")
        raise


# ─── Step 4: Poll Task Status ─────────────────────────────────────────────────

def poll_task(base_url: str, api_key: str, task_id: str,
              estimated_max: int = 120,
              poll_interval: int = 5,
              max_wait: int = 600,
              on_progress=None) -> dict:
    """
    POST /open/v1/tasks/detail — poll until completion.

    - resource_status (int or null): 0=processing, 1=done, 2=failed, 3=deleted.
      null is treated as 0.
    - status (string): "pending" | "processing" | "success" | "failed".
      When resource_status==1, treat status=="failed" as failure; "success" (or "completed") as success.
    - Stop only when ALL medias have resource_status == 1 and no status == "failed".
    - Returns the first completed media dict (with url) when all are done.
    """
    url     = f"{base_url}/open/v1/tasks/detail"
    headers = make_headers(api_key)
    start   = time.time()

    logger.info(f"Poll task started: task_id={task_id}, max_wait={max_wait}s")

    last_progress_report = 0
    progress_interval    = 15 if poll_interval <= 5 else 30

    while True:
        elapsed = time.time() - start
        if elapsed > max_wait:
            logger.error(f"Task timeout: task_id={task_id}, elapsed={int(elapsed)}s, max_wait={max_wait}s")
            raise TimeoutError(
                f"Task {task_id} timed out after {max_wait}s. "
                "Check the IMA dashboard for status."
            )

        resp = requests.post(url, json={"task_id": task_id},
                             headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        code = data.get("code")
        if code not in (0, 200):
            raise RuntimeError(f"Poll error — code={code} msg={data.get('message')}")

        task   = data.get("data") or {}
        medias = task.get("medias") or []

        # Normalize resource_status: API may return null (Go *int); treat as 0 (processing)
        def _rs(m):
            v = m.get("resource_status")
            return 0 if (v is None or v == "") else int(v)

        # 1. Fail fast: any media failed or deleted → raise
        for media in medias:
            rs = _rs(media)
            if rs == 2:
                err = media.get("error_msg") or media.get("remark") or "unknown"
                logger.error(f"Task failed: task_id={task_id}, resource_status=2, error={err}")
                raise RuntimeError(f"Generation failed (resource_status=2): {err}")
            if rs == 3:
                logger.error(f"Task deleted: task_id={task_id}")
                raise RuntimeError("Task was deleted")

        # 2. Success only when ALL medias have resource_status == 1 (and none failed)
        # status is one of: "pending", "processing", "success", "failed"
        if medias and all(_rs(m) == 1 for m in medias):
            for media in medias:
                if (media.get("status") or "").strip().lower() == "failed":
                    err = media.get("error_msg") or media.get("remark") or "unknown"
                    logger.error(f"Task failed: task_id={task_id}, status=failed, error={err}")
                    raise RuntimeError(f"Generation failed: {err}")
            # All done and no failure → also wait for URL to be populated
            first_media = medias[0]
            result_url = first_media.get("url") or first_media.get("watermark_url")
            if result_url:
                elapsed_time = int(time.time() - start)
                logger.info(f"Task completed: task_id={task_id}, elapsed={elapsed_time}s, url={result_url[:80]}")
                return first_media
            # else: URL not ready yet, keep polling

        # Report progress periodically
        if elapsed - last_progress_report >= progress_interval:
            pct = min(95, int(elapsed / estimated_max * 100))
            msg = f"⏳ {int(elapsed)}s elapsed … {pct}%"
            if elapsed > estimated_max:
                msg += "  (taking longer than expected, please wait…)"
            if on_progress:
                on_progress(pct, int(elapsed), msg)
            else:
                print(msg, flush=True)
            last_progress_report = elapsed

        time.sleep(poll_interval)


# ─── Reflection Mechanism (v1.0.5) ────────────────────────────────────────────

def extract_error_info(exception: Exception) -> dict:
    """
    Extract error code and message from exception.
    
    Handles:
    - RuntimeError from create_task with code in message
    - requests.HTTPError (500, 400, etc.)
    - TimeoutError from poll_task
    
    Returns: {"code": int|str, "message": str, "type": str}
    """
    error_str = str(exception)
    
    # Check for HTTP status codes (500, 400, etc.)
    if isinstance(exception, requests.HTTPError):
        status_code = exception.response.status_code
        try:
            response_data = exception.response.json()
            api_code = response_data.get("code")
            api_msg = response_data.get("message", "")
            return {
                "code": api_code if api_code else status_code,
                "message": api_msg or error_str,
                "type": f"http_{status_code}",
                "raw_response": response_data
            }
        except:
            return {
                "code": status_code,
                "message": error_str,
                "type": f"http_{status_code}"
            }
    
    # Check for API error codes in RuntimeError message (6009, 6010, etc.)
    import re
    code_match = re.search(r'code[=:]?\s*(\d+)', error_str, re.IGNORECASE)
    if code_match:
        code = int(code_match.group(1))
        return {
            "code": code,
            "message": error_str,
            "type": f"api_{code}"
        }
    
    # Timeout error
    if isinstance(exception, TimeoutError):
        return {
            "code": "timeout",
            "message": error_str,
            "type": "timeout"
        }
    
    # Generic error
    return {
        "code": "unknown",
        "message": error_str,
        "type": "unknown"
    }


def get_param_degradation_strategy(param_key: str, current_value: str) -> list:
    """
    Get degradation sequence for a parameter when error occurs.
    
    Returns list of fallback values to try, from high-quality to low-quality.
    Empty list means no degradation available.
    """
    # Resolution degradation (1080p → 720p → 480p) for video
    if param_key.lower() == "resolution":
        res_map = {
            "1080p": ["720p", "480p"],
            "720p": ["480p"],
            "480p": []
        }
        return res_map.get(current_value.lower(), [])
    
    # Duration degradation (10s → 5s) for video
    if param_key.lower() == "duration":
        dur_map = {
            "10s": ["5s"],
            "5s": []
        }
        return dur_map.get(current_value.lower(), [])
    
    # Mode degradation for video models
    if param_key.lower() == "mode":
        mode_map = {
            "professional": ["standard"],
            "standard": []
        }
        return mode_map.get(current_value.lower(), [])
    
    # Quality degradation
    if param_key.lower() == "quality":
        quality_map = {
            "高清": ["标清"],
            "high": ["standard", "low"],
            "standard": ["low"],
            "low": []
        }
        return quality_map.get(current_value.lower(), [])
    
    return []


def reflect_on_failure(error_info: dict, 
                      attempt: int,
                      current_params: dict,
                      credit_rules: list,
                      model_params: dict) -> dict:
    """
    Analyze failure and determine corrective action.
    
    Args:
        error_info: Output from extract_error_info()
        attempt: Current attempt number (1, 2, or 3)
        current_params: Parameters used in failed attempt
        credit_rules: All available credit_rules for this model
        model_params: Model metadata (name, id, form_params, etc.)
    
    Returns:
        {
            "action": "retry" | "give_up",
            "new_params": dict (if action=="retry"),
            "reason": str (explanation of what changed),
            "suggestion": str (user-facing suggestion if give_up)
        }
    """
    code = error_info.get("code")
    error_type = error_info.get("type", "")
    
    logger.info(f"🔍 Reflection Attempt {attempt}: analyzing error code={code}, type={error_type}")
    
    # Strategy 1: 500 Internal Server Error → Degrade parameters
    if code == 500 or "http_500" in error_type:
        logger.info("Strategy: Degrade parameters due to 500 error")
        
        # Try to degrade a parameter (prioritize video-specific params)
        for key in ["resolution", "duration", "mode", "quality"]:
            if key in current_params:
                current_val = current_params[key]
                fallbacks = get_param_degradation_strategy(key, current_val)
                
                if fallbacks:
                    new_val = fallbacks[0]
                    new_params = current_params.copy()
                    new_params[key] = new_val
                    
                    logger.info(f"  → Degrading {key}: {current_val} → {new_val}")
                    
                    return {
                        "action": "retry",
                        "new_params": new_params,
                        "reason": f"500 error with {key}='{current_val}', degrading to '{new_val}'"
                    }
        
        return {
            "action": "give_up",
            "suggestion": f"Model '{model_params['model_name']}' returned 500 Internal Server Error. "
                         f"This may indicate a backend issue or unsupported parameter combination. "
                         f"Try a different model or contact IMA support."
        }
    
    # Strategy 2: 6009 (No matching rule) → Extract required params from first rule
    if code == 6009:
        logger.info("Strategy: Add missing parameters from credit_rules (6009)")
        
        if credit_rules and len(credit_rules) > 0:
            min_rule = min(credit_rules, key=lambda r: r.get("points", 9999))
            rule_attrs = min_rule.get("attributes", {})
            
            if rule_attrs:
                new_params = current_params.copy()
                added = []
                
                for key, val in rule_attrs.items():
                    if key not in new_params:
                        new_params[key] = val
                        added.append(f"{key}={val}")
                
                if added:
                    logger.info(f"  → Adding missing params: {', '.join(added)}")
                    return {
                        "action": "retry",
                        "new_params": new_params,
                        "reason": f"6009 error: added missing parameters {', '.join(added)} from credit_rules"
                    }
        
        return {
            "action": "give_up",
            "suggestion": f"No matching credit rule found for parameters: {current_params}. "
                         f"Model '{model_params['model_name']}' may not support this parameter combination. "
                         f"Try using default parameters or a different model."
        }
    
    # Strategy 3: 6010 (attribute_id mismatch) → Reselect credit_rule
    if code == 6010:
        logger.info("Strategy: Reselect credit_rule based on current params (6010)")
        
        if credit_rules:
            selected = select_credit_rule_by_params(credit_rules, current_params)
            
            if selected:
                new_attr_id = selected.get("attribute_id")
                new_points = selected.get("points")
                rule_attrs = selected.get("attributes", {})
                
                new_params = current_params.copy()
                new_params.update(rule_attrs)
                
                logger.info(f"  → Reselected rule: attribute_id={new_attr_id}, points={new_points}, attrs={rule_attrs}")
                
                return {
                    "action": "retry",
                    "new_params": new_params,
                    "reason": f"6010 error: reselected credit_rule (attribute_id={new_attr_id}, {new_points} pts)",
                    "new_attribute_id": new_attr_id,
                    "new_credit": new_points
                }
        
        return {
            "action": "give_up",
            "suggestion": f"Parameter mismatch (error 6010) for model '{model_params['model_name']}'. "
                         f"Could not find compatible credit_rule. Try refreshing the model list or using default parameters."
        }
    
    # Strategy 4: Timeout → Can't retry, but give helpful info
    if code == "timeout":
        return {
            "action": "give_up",
            "suggestion": f"Task generation timed out for model '{model_params['model_name']}'. "
                         f"The task may still be processing in the background. "
                         f"Check the IMA Studio dashboard (https://imagent.bot) for your task status. "
                         f"If this model is consistently slow, consider using a faster model."
        }
    
    # Default: Unknown error
    return {
        "action": "give_up",
        "suggestion": f"Unexpected error (code={code}): {error_info.get('message')}. "
                     f"If this persists, please report to IMA support with error code {code}."
    }


def create_task_with_reflection(base_url: str, api_key: str,
                                task_type: str, model_params: dict,
                                prompt: str,
                                input_images: list[str] | None = None,
                                extra_params: dict | None = None,
                                max_attempts: int = 3) -> str:
    """
    Create task with automatic error reflection and retry.
    
    Attempts up to max_attempts times, using reflection to adjust parameters
    between attempts based on error codes (500, 6009, 6010, timeout).
    
    Returns task_id on success, raises exception after max_attempts with helpful suggestion.
    """
    current_params = extra_params.copy() if extra_params else {}
    attempt_log = []
    
    credit_rules = model_params.get("all_credit_rules", [])
    
    for attempt in range(1, max_attempts + 1):
        try:
            logger.info(f"{'='*60}")
            logger.info(f"Attempt {attempt}/{max_attempts}: Creating task with params={current_params}")
            logger.info(f"{'='*60}")
            
            # Special handling: if reflection provided new attribute_id/credit, update model_params
            if attempt > 1 and "last_reflection" in locals():
                reflection = locals()["last_reflection"]
                if "new_attribute_id" in reflection:
                    model_params["attribute_id"] = reflection["new_attribute_id"]
                    model_params["credit"] = reflection["new_credit"]
                    logger.info(f"  Using reflected attribute_id={reflection['new_attribute_id']}, "
                              f"credit={reflection['new_credit']} pts")
            
            task_id = create_task(
                base_url=base_url,
                api_key=api_key,
                task_type=task_type,
                model_params=model_params,
                prompt=prompt,
                input_images=input_images,
                extra_params=current_params
            )
            
            # Success!
            if attempt > 1:
                logger.info(f"✅ Task created successfully after {attempt} attempts (auto-recovery)")
            
            attempt_log.append({
                "attempt": attempt,
                "result": "success",
                "params": current_params.copy()
            })
            
            return task_id
            
        except Exception as e:
            error_info = extract_error_info(e)
            
            attempt_log.append({
                "attempt": attempt,
                "result": "failed",
                "params": current_params.copy(),
                "error": error_info
            })
            
            logger.error(f"❌ Attempt {attempt} failed: {error_info['type']} - {error_info['message']}")
            
            if attempt < max_attempts:
                reflection = reflect_on_failure(
                    error_info=error_info,
                    attempt=attempt,
                    current_params=current_params,
                    credit_rules=credit_rules,
                    model_params=model_params
                )
                
                last_reflection = reflection
                
                if reflection["action"] == "retry":
                    current_params = reflection["new_params"]
                    logger.info(f"🔄 Reflection decision: {reflection['reason']}")
                    logger.info(f"   Retrying with new params: {current_params}")
                    continue
                else:
                    logger.error(f"💡 Reflection suggests giving up: {reflection.get('suggestion')}")
                    raise RuntimeError(
                        f"Task creation failed after {attempt} attempt(s).\n\n"
                        f"💡 Suggestion: {reflection.get('suggestion')}\n\n"
                        f"Attempt log:\n" + json.dumps(attempt_log, indent=2, ensure_ascii=False)
                    ) from e
            else:
                logger.error(f"❌ All {max_attempts} attempts failed")
                
                last_error = attempt_log[-1]["error"]
                suggestion = f"All {max_attempts} attempts failed. Last error: {last_error['message']}"
                
                if last_error['code'] in [401, 500, 4008, 6009, 6010]:
                    suggestion += f"\n\n💡 This may indicate:\n"
                    if last_error['code'] == 401:
                        suggestion += "  - API key is invalid or unauthorized\n"
                        suggestion += "  - 🔗 Generate API Key: https://www.imaclaw.ai/imaclaw/apikey\n"
                    elif last_error['code'] == 4008:
                        suggestion += "  - Insufficient points to create this task\n"
                        suggestion += "  - 🔗 Buy Credits: https://www.imaclaw.ai/imaclaw/subscription\n"
                    elif last_error['code'] == 500:
                        suggestion += "  - Backend server issue or unsupported parameter\n"
                        suggestion += "  - Try a different model or simpler parameters\n"
                    elif last_error['code'] == 6009:
                        suggestion += "  - No matching pricing rule for your parameters\n"
                        suggestion += "  - Try using default parameters or check available options\n"
                    elif last_error['code'] == 6010:
                        suggestion += "  - Parameter/pricing rule mismatch\n"
                        suggestion += "  - Refresh the model list or use recommended parameters\n"
                
                raise RuntimeError(
                    f"Task creation failed after {max_attempts} attempts.\n\n"
                    f"{suggestion}\n\n"
                    f"Full attempt log:\n" + json.dumps(attempt_log, indent=2, ensure_ascii=False)
                ) from e


# ─── User Preference Memory ───────────────────────────────────────────────────

def load_prefs() -> dict:
    try:
        with open(PREFS_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_pref(user_id: str, task_type: str, model_params: dict):
    os.makedirs(os.path.dirname(PREFS_PATH), exist_ok=True)
    prefs = load_prefs()
    key   = f"user_{user_id}"
    prefs.setdefault(key, {})[task_type] = {
        "model_id":    model_params["model_id"],
        "model_name":  model_params["model_name"],
        "credit":      model_params["credit"],
        "last_used":   datetime.now(timezone.utc).isoformat(),
    }
    with open(PREFS_PATH, "w", encoding="utf-8") as f:
        json.dump(prefs, f, ensure_ascii=False, indent=2)


def get_preferred_model_id(user_id: str, task_type: str) -> str | None:
    prefs = load_prefs()
    entry = (prefs.get(f"user_{user_id}") or {}).get(task_type)
    return entry.get("model_id") if entry else None


# ─── CLI Entry Point ──────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="IMA AI Creation Script — reliable task creation via Open API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text to video (Wan 2.6 — most popular default)
  python3 ima_video_create.py \\
    --api-key ima_xxx --task-type text_to_video \\
    --model-id wan2.6-t2v --prompt "a cute puppy running on grass"

  # Text to video with premium model
  python3 ima_video_create.py \\
    --api-key ima_xxx --task-type text_to_video \\
    --model-id MiniMax-Hailuo-2.3 --prompt "cinematic city skyline at sunset"

  # Image to video (Wan 2.6)
  python3 ima_video_create.py \\
    --api-key ima_xxx --task-type image_to_video \\
    --model-id wan2.6-i2v --prompt "camera slowly zooms in" \\
    --input-images https://example.com/photo.jpg

  # Text to music (Suno sonic-v5)
  python3 ima_video_create.py \\
    --api-key ima_xxx --task-type text_to_music \\
    --model-id sonic --prompt "upbeat lo-fi hip hop, 90 BPM"

  # List all models for a category
  python3 ima_video_create.py \\
    --api-key ima_xxx --task-type text_to_video --list-models
""",
    )

    p.add_argument("--api-key",  required=False,
                   help="IMA Open API key (starts with ima_). Can also use IMA_API_KEY env var")
    p.add_argument("--task-type", required=True,
                   choices=list(POLL_CONFIG.keys()),
                   help="Task type to create")
    p.add_argument("--model-id",
                   help="Model ID from product list (e.g. doubao-seedream-4.5)")
    p.add_argument("--version-id",
                   help="Specific version ID — overrides auto-select of latest")
    p.add_argument("--prompt",
                   help="Generation prompt (required unless --list-models)")
    p.add_argument("--input-images", nargs="*", default=[],
                   help="Input image URLs or local file paths (for image_to_video, first_last_frame_to_video, etc.). "
                        "Local files will be automatically uploaded using the API key.")
    p.add_argument("--size",
                   help="Override size parameter (e.g. 4k, 2k, 1024x1024)")
    p.add_argument("--extra-params",
                   help='JSON string of extra inner parameters, e.g. \'{"n":2}\'')
    p.add_argument("--language", default="en",
                   help="Language for product labels (en/zh)")
    p.add_argument("--base-url", default=DEFAULT_BASE_URL,
                   help="API base URL")
    p.add_argument("--user-id", default="default",
                   help="User ID for preference memory")
    p.add_argument("--list-models", action="store_true",
                   help="List all available models for --task-type and exit")
    p.add_argument("--output-json", action="store_true",
                   help="Output final result as JSON (for agent parsing)")

    return p


def main():
    args   = build_parser().parse_args()
    base   = args.base_url
    
    # Get API key from args or environment variable
    apikey = args.api_key or os.getenv("IMA_API_KEY")
    if not apikey:
        logger.error("API key is required. Use --api-key or set IMA_API_KEY environment variable")
        sys.exit(1)

    start_time = time.time()
    masked_key = f"{apikey[:10]}..." if len(apikey) > 10 else "***"
    logger.info(f"Script started: task_type={args.task_type}, model_id={args.model_id or 'auto'}, "
                f"api_key={masked_key}")

    # ── 1. Query product list ──────────────────────────────────────────────────
    print(f"🔍 Querying product list: category={args.task_type}", flush=True)
    try:
        tree = get_product_list(base, apikey, args.task_type,
                                language=args.language)
    except Exception as e:
        logger.error(f"Product list failed: {str(e)}")
        print(f"❌ Product list failed: {e}", file=sys.stderr)
        sys.exit(1)

    # ── List models mode ───────────────────────────────────────────────────────
    if args.list_models:
        models = list_all_models(tree)
        print(f"\nAvailable models for '{args.task_type}':")
        print(f"{'Name':<28} {'model_id':<34} {'version_id':<44} {'pts':>4}  attr_id")
        print("─" * 120)
        for m in models:
            print(f"{m['name']:<28} {m['model_id']:<34} {m['version_id']:<44} "
                  f"{m['credit']:>4}  {m['attr_id']}")
        sys.exit(0)

    # ── Resolve model_id ───────────────────────────────────────────────────────
    if not args.model_id:
        # Check user preference
        pref_model = get_preferred_model_id(args.user_id, args.task_type)
        if pref_model:
            args.model_id = pref_model
            print(f"💡 Using your preferred model: {pref_model}", flush=True)
        else:
            print("❌ --model-id is required (no saved preference found)", file=sys.stderr)
            print("   Run with --list-models to see available models", file=sys.stderr)
            sys.exit(1)

    if not args.prompt:
        print("❌ --prompt is required", file=sys.stderr)
        sys.exit(1)

    # ── 2. Find model version in tree ─────────────────────────────────────────
    node = find_model_version(tree, args.model_id, args.version_id)
    if not node:
        logger.error(f"Model not found: model_id={args.model_id}, task_type={args.task_type}")
        available = [f"  {m['model_id']}" for m in list_all_models(tree)]
        print(f"❌ model_id='{args.model_id}' not found for task_type='{args.task_type}'.",
              file=sys.stderr)
        print("   Available model_ids:\n" + "\n".join(available), file=sys.stderr)
        sys.exit(1)

    # ── 3. Extract params (including virtual param resolution) ────────────────
    try:
        mp = extract_model_params(node)
    except RuntimeError as e:
        logger.error(f"Param extraction failed: {str(e)}")
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Model found:")
    print(f"   name          = {mp['model_name']}")
    print(f"   model_id      = {mp['model_id']}")
    print(f"   model_version = {mp['model_version']}   ← version_id from product list")
    print(f"   attribute_id  = {mp['attribute_id']}")
    print(f"   credit        = {mp['credit']} pts")
    print(f"   form_params   = {json.dumps(mp['form_params'], ensure_ascii=False)}")

    # Apply overrides
    extra: dict = {}
    if args.size:
        extra["size"] = args.size
    if args.extra_params:
        try:
            extra.update(json.loads(args.extra_params))
        except json.JSONDecodeError as e:
            print(f"❌ Invalid --extra-params JSON: {e}", file=sys.stderr)
            sys.exit(1)

    # ── 4. Process input images (upload if needed) ────────────────────────────
    processed_images: list[str] = []
    if args.input_images:
        im_base = os.getenv("IMA_IM_BASE_URL", DEFAULT_IM_BASE_URL)
        
        print(f"\n📤 Processing {len(args.input_images)} input image(s)…", flush=True)
        for i, img_source in enumerate(args.input_images, 1):
            try:
                img_url = prepare_image_url(img_source, apikey, im_base)
                processed_images.append(img_url)
                
                if img_source.startswith("https://"):
                    print(f"   [{i}] Using URL: {img_url[:60]}...")
                else:
                    print(f"   [{i}] Uploaded: {os.path.basename(img_source) if isinstance(img_source, str) else 'bytes'} → {img_url[:60]}...")
            
            except RuntimeError as e:
                logger.error(f"Failed to process image {i}: {e}")
                print(f"❌ Failed to process image [{i}]: {e}", file=sys.stderr)
                sys.exit(1)
        
        print(f"✅ All {len(processed_images)} image(s) ready")

    # ── 5. Create task (with Reflection) ──────────────────────────────────────
    print(f"\n🚀 Creating task…", flush=True)
    try:
        task_id = create_task_with_reflection(
            base_url=base,
            api_key=apikey,
            task_type=args.task_type,
            model_params=mp,
            prompt=args.prompt,
            input_images=processed_images,
            extra_params=extra if extra else None,
            max_attempts=3  # Up to 3 automatic retries with reflection
        )
    except RuntimeError as e:
        logger.error(f"Task creation failed after reflection: {str(e)}")
        print(f"❌ Create task failed:\n{e}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Task created: {task_id}", flush=True)

    # ── 6. Poll for result ─────────────────────────────────────────────────────
    cfg        = POLL_CONFIG.get(args.task_type, {"interval": 5, "max_wait": 300})
    est_max    = cfg["max_wait"] // 2   # optimistic estimate = half of max_wait
    print(f"\n⏳ Polling… (interval={cfg['interval']}s, max={cfg['max_wait']}s)",
          flush=True)

    try:
        media = poll_task(base, apikey, task_id,
                          estimated_max=est_max,
                          poll_interval=cfg["interval"],
                          max_wait=cfg["max_wait"])
    except (TimeoutError, RuntimeError) as e:
        logger.error(f"Task polling failed: {str(e)}")
        print(f"\n❌ {e}", file=sys.stderr)
        sys.exit(1)

    # ── 6. Save preference ────────────────────────────────────────────────────
    save_pref(args.user_id, args.task_type, mp)

    # ── 7. Output result ───────────────────────────────────────────────────────
    result_url = media.get("url") or media.get("preview_url") or ""
    cover_url  = media.get("cover_url") or ""

    print(f"\n✅ Generation complete!")
    print(f"   URL:   {result_url}")
    if cover_url:
        print(f"   Cover: {cover_url}")

    if args.output_json:
        out = {
            "task_id":    task_id,
            "url":        result_url,
            "cover_url":  cover_url,
            "model_id":   mp["model_id"],
            "model_name": mp["model_name"],
            "credit":     mp["credit"],
        }
        print("\n" + json.dumps(out, ensure_ascii=False, indent=2))

    total_time = int(time.time() - start_time)
    logger.info(f"Script completed: total_time={total_time}s, task_id={task_id}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
