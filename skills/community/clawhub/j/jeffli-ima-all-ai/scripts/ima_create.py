#!/usr/bin/env python3
"""
IMA AI Creation Script — ima_create.py
Version: 1.4.0

Reliable task creation via IMA Open API.
Flow: product list → virtual param resolution → task create → poll status.

**Image generation uses KIE API** (nano-banana-2 model).
**Video/Music/TTS use IMA API.**

- --input-images: accepts HTTPS URLs or local file paths (local files auto-uploaded to IMA CDN).
- Task types: text_to_image | image_to_image | text_to_video | image_to_video |
  first_last_frame_to_video | reference_image_to_video | text_to_music | text_to_speech

Usage:
  # Image (uses KIE API):
  python3 ima_create.py --kie-key YOUR_KIE_KEY --task-type text_to_image \\
    --prompt "a cute puppy"

  # Video/Music/TTS (uses IMA API):
  python3 ima_create.py --api-key ima_xxx --task-type text_to_video \\
    --model-id ima-pro --prompt "a cat playing piano"

Logs: ~/.openclaw/logs/ima_skills/ima_create_YYYYMMDD.log
"""

import argparse
import hashlib
import json
import math
import mimetypes
import os
import re
import sys
import time
import uuid
from datetime import datetime, timezone

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

DEFAULT_BASE_URL = "https://api.imastudio.com"
PREFS_PATH       = os.path.expanduser("~/.openclaw/memory/ima_prefs.json")
VIDEO_MAX_WAIT_SECONDS = 40 * 60
VIDEO_RECORDS_URL = "https://www.imastudio.com/ai-creation/text-to-video"
VIDEO_TASK_TYPES = {
    "text_to_video",
    "image_to_video",
    "first_last_frame_to_video",
    "reference_image_to_video",
}

# Upload service (IMA image/video CDN upload). See SKILL.md "Network Endpoints Used".
IMA_IM_BASE = "https://imapi.liveme.com"
APP_ID      = "webAgent"
APP_KEY     = "32jdskjdk320eew"   # public shared client-id, not a secret

# ─── KIE API (Image Generation) ──────────────────────────────────────────────
KIE_API_BASE = "https://api.kie.ai/api/v1"
IMAGE_TASK_TYPES = {"text_to_image", "image_to_image"}

# Poll interval (seconds) and max wait (seconds) per task type
POLL_CONFIG = {
    "text_to_image":             {"interval": 5,  "max_wait": 600},
    "image_to_image":            {"interval": 5,  "max_wait": 600},
    "text_to_video":             {"interval": 8,  "max_wait": VIDEO_MAX_WAIT_SECONDS},
    "image_to_video":            {"interval": 8,  "max_wait": VIDEO_MAX_WAIT_SECONDS},
    "first_last_frame_to_video": {"interval": 8,  "max_wait": VIDEO_MAX_WAIT_SECONDS},
    "reference_image_to_video":  {"interval": 8,  "max_wait": VIDEO_MAX_WAIT_SECONDS},
    "text_to_music":             {"interval": 5,  "max_wait": 480},
    "text_to_speech":            {"interval": 3,  "max_wait": 300},
}

# Model alias normalization (user-facing input -> canonical model_id).
# Keep this minimal: dynamic product list remains the source of truth.
MODEL_ID_ALIASES = {
    "ima sevio 1.0": "ima-pro",
    "ima sevio 1.0-fast": "ima-pro-fast",
    "ima sevio 1.0 fast": "ima-pro-fast",
}


def normalize_model_id(model_id: str | None) -> str | None:
    """Normalize known aliases; return original model_id when no alias applies."""
    if not model_id:
        return None
    normalized_key = re.sub(r"\s+", " ", model_id.strip().lower())
    return MODEL_ID_ALIASES.get(normalized_key, model_id.strip())


def to_user_facing_model_name(model_name: str | None, model_id: str | None) -> str:
    """Return user-facing Sevio branding when model_id belongs to Sevio family."""
    canonical = normalize_model_id(model_id)
    if canonical == "ima-pro":
        return "Ima Sevio 1.0 (IMA Video Pro)"
    if canonical == "ima-pro-fast":
        return "Ima Sevio 1.0-Fast (IMA Video Pro Fast)"
    return model_name or "IMA Model"


# ─── HTTP helpers ─────────────────────────────────────────────────────────────

def make_headers(api_key: str, language: str = "en") -> dict:
    return {
        "Authorization":  f"Bearer {api_key}",
        "Content-Type":   "application/json",
        "x-app-source":   "ima_skills",
        "x_app_language": language,
    }


# ─── Image upload helpers ─────────────────────────────────────────────────────

def _gen_sign() -> tuple:
    """Generate per-request (sign, timestamp, nonce) for upload token."""
    nonce = uuid.uuid4().hex[:21]
    ts    = str(int(time.time()))
    raw   = f"{APP_ID}|{APP_KEY}|{ts}|{nonce}"
    sign  = hashlib.sha1(raw.encode()).hexdigest().upper()
    return sign, ts, nonce


def _get_upload_token(api_key: str, suffix: str, content_type: str) -> dict:
    """Step 1: Get presigned upload URL from IMA upload service."""
    sign, ts, nonce = _gen_sign()
    r = requests.get(
        f"{IMA_IM_BASE}/api/rest/oss/getuploadtoken",
        params={
            "appUid":       api_key,
            "appId":        APP_ID,
            "appKey":       APP_KEY,
            "cmimToken":    api_key,
            "sign":         sign,
            "timestamp":    ts,
            "nonce":        nonce,
            "fService":     "privite",
            "fType":        "picture",
            "fSuffix":      suffix,
            "fContentType": content_type,
        },
        timeout=15,
    )
    r.raise_for_status()
    return r.json()["data"]


def prepare_image_url(source: str, api_key: str) -> str:
    """Upload a local image file to IMA CDN and return its public URL.

    If `source` is already an HTTPS URL it is returned as-is.
    Otherwise the file is uploaded via the two-step presigned URL flow and
    the resulting CDN URL (fdl) is returned.
    """
    if source.startswith("https://") or source.startswith("http://"):
        return source

    if not os.path.isfile(source):
        raise FileNotFoundError(f"Input image not found: {source}")

    content_type = mimetypes.guess_type(source)[0] or "image/jpeg"
    suffix = source.rsplit(".", 1)[-1].lower() if "." in source else "jpeg"

    logger.info(f"Uploading local image: {source} ({content_type})")
    token_data = _get_upload_token(api_key, suffix, content_type)
    ful = token_data["ful"]
    fdl = token_data["fdl"]

    with open(source, "rb") as f:
        image_bytes = f.read()
    resp = requests.put(ful, data=image_bytes, headers={"Content-Type": content_type}, timeout=60)
    resp.raise_for_status()

    logger.info(f"Upload complete: {fdl}")
    return fdl


# ─── KIE Image Generation ─────────────────────────────────────────────────

def get_kie_callback_url() -> str | None:
    """Get the KIE callback URL from the running callback server."""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 8787))
    sock.close()
    if result != 0:
        return None
    # Callback server is running, return the callback URL
    # User should provide this via --callback-url or env var
    return os.environ.get("KIE_CALLBACK_URL")


def create_kie_image_task(api_key: str, prompt: str,
                          model: str = "nano-banana-2",
                          resolution: str = "1K",
                          aspect_ratio: str = "16:9",
                          input_image: str | None = None,
                          callback_url: str | None = None) -> dict:
    """
    Create a KIE image generation task.

    Returns: {"task_id": "xxx", "status": "created"}
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": model,
        "input": {
            "prompt": prompt,
            "resolution": resolution,
            "aspect_ratio": aspect_ratio,
        }
    }

    if input_image:
        payload["input"]["input_image"] = input_image

    if callback_url:
        payload["callBackUrl"] = callback_url

    url = f"{KIE_API_BASE}/jobs/createTask"
    logger.info(f"Creating KIE image task: model={model}, prompt={prompt[:50]}...")

    resp = requests.post(url, json=payload, headers=headers, timeout=30)
    resp.raise_for_status()
    result = resp.json()

    if result.get("code") != 0 and result.get("code") != 200:
        raise RuntimeError(f"KIE API error: {result.get('msg', result)}")

    data = result.get("data", {})
    task_id = data.get("task_id") or data.get("job_id")
    logger.info(f"KIE task created: {task_id}")
    return {"task_id": task_id, "status": "created", "data": data}


def poll_kie_task(api_key: str, task_id: str, interval: int = 5,
                  max_wait: int = 600) -> dict:
    """
    Poll KIE task status until completion.

    Returns: final task result dict
    """
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    start = time.time()
    url = f"{KIE_API_BASE}/jobs/getTaskDetails"
    params = {"task_id": task_id}

    while time.time() - start < max_wait:
        resp = requests.get(url, params=params, headers=headers, timeout=15)
        resp.raise_for_status()
        result = resp.json()

        data = result.get("data", {})
        status = data.get("status", "")

        if status in ("completed", "success", "finish"):
            logger.info(f"KIE task completed: {task_id}")
            return data
        elif status in ("failed", "error"):
            raise RuntimeError(f"KIE task failed: {data.get('error', status)}")

        logger.info(f"KIE task status: {status} — waiting {interval}s...")
        time.sleep(interval)

    raise RuntimeError(f"KIE task timeout after {max_wait}s")


def get_kie_image_url(api_key: str, task_id: str) -> str:
    """Get the generated image URL from KIE task."""
    headers = {
        "Authorization": f"Bearer {api_key}",
    }
    url = f"{KIE_API_BASE}/jobs/getTaskDetails"
    params = {"task_id": task_id}

    resp = requests.get(url, params=params, headers=headers, timeout=15)
    resp.raise_for_status()
    result = resp.json()

    data = result.get("data", {})
    images = data.get("result", {}).get("images", [])
    if images:
        return images[0].get("url") or images[0]
    raise RuntimeError(f"No image in KIE result: {data}")


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
    
    # 🆕 CRITICAL FIX: For TTS tasks, keep "default": "enabled" parameter
    # It's not just a marker - it's a required parameter for the API
    # Simply copy all attributes from the selected rule
    rule_attributes = rule_attrs.copy()

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
        # CRITICAL FIX: Case-insensitive matching for size/resolution/duration values
        # User may pass "1k" but rules define "1K", or "1080p" vs "1080P"
        return str(v).strip().upper()  # "1k" → "1K", "1080p" → "1080P"
    
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


def get_valid_attribute_keys(credit_rules: list, task_type: str = None) -> set:
    """
    Extract all valid attribute keys from credit_rules dynamically.
    
    This avoids hardcoding parameter lists that may become outdated.
    Scans all credit_rules[].attributes and collects keys (excluding special markers).
    
    Args:
        credit_rules: List of credit rules from product API
        task_type: Optional task type for special handling (e.g., "text_to_speech")
    
    Returns: set of attribute keys that can be used for credit_rule matching
    """
    valid_keys = set()
    
    for rule in credit_rules:
        attrs = rule.get("attributes", {})
        for key, value in attrs.items():
            # Special case for TTS: keep all attributes including "default": "enabled"
            # This fixes the issue where TTS tasks fail because the required parameter is skipped
            if task_type == "text_to_speech":
                valid_keys.add(key)
            # For other task types: skip special markers like {"default": "enabled"}
            elif not (key == "default" and value == "enabled"):
                valid_keys.add(key)
    
    return valid_keys


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

    # Smart credit_rule selection based on merged params (form defaults + user overrides)
    # 🔧 FIX: Always try to match credit_rule based on actual parameters (not just user params)
    # This fixes error 6010 when backend recalculates rule based on complete params
    all_rules = model_params.get("all_credit_rules", [])
    normalized_rule_params = {}  # 🆕 Store normalized params from matched rule
    
    if all_rules:
        # Merge form_config defaults + user overrides (user params take priority)
        merged_params = {**model_params["form_params"], **(extra_params or {})}
        
        # ✅ DYNAMIC: Extract valid attribute keys from credit_rules
        # This replaces the hardcoded list and stays in sync with backend
        # Pass task_type to handle TTS special case (keep "default": "enabled")
        valid_keys = get_valid_attribute_keys(all_rules, task_type)
        
        # Filter merged params to only include keys that appear in credit_rules.attributes
        candidate_params = {k: v for k, v in merged_params.items() if k in valid_keys}
        
        # Common attribute keys (for reference, but not used for filtering):
        # Image: size, quality, n
        # Video: duration, resolution, generate_audio, sound, mode,
        #        fast_pretreatment, prompt_optimizer
        # Music: (typically no attributes in credit_rules)
        
        if candidate_params:
            selected_rule = select_credit_rule_by_params(all_rules, candidate_params)
            if selected_rule:
                attribute_id = selected_rule.get("attribute_id", model_params["attribute_id"])
                credit = selected_rule.get("points", model_params["credit"])
                
                # 🆕 CRITICAL FIX: Use normalized values from the matched rule's attributes
                # This ensures API gets "1K" (from rule) instead of "1k" (from user)
                rule_attrs = selected_rule.get("attributes", {})
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

    # ✅ FIX for error 6010: Merge parameters in correct priority order
    # Priority (low → high): form_params < rule_attributes < normalized_rule_params < extra_params
    # CRITICAL: rule_attributes MUST override form_params to match attribute_id
    inner: dict = {}
    
    # 1. First merge form_config defaults (UI defaults, lowest priority)
    inner.update(model_params["form_params"])
    
    # 2. Then merge rule_attributes (required fields from credit_rules, MUST override form_params)
    # ⚠️ This fixes error 6010: rule_attributes define the params required by attribute_id
    rule_attrs = model_params.get("rule_attributes", {})
    if rule_attrs:
        inner.update(rule_attrs)
    
    # 3. Merge normalized params from matched rule (higher priority - these are canonical values)
    # 🆕 CRITICAL: This overwrites user's "1k" with rule's "1K" to match attribute_id
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
            # Use raw model_id from product list when available for backend compatibility.
            "model_id":      model_params.get("model_id_raw") or model_params["model_id"],
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
              task_type: str | None = None,
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
            if task_type in VIDEO_TASK_TYPES:
                raise TimeoutError(
                    f"Task {task_id} timed out after {max_wait}s without explicit backend errors. "
                    f"Please check your creation record at {VIDEO_RECORDS_URL}."
                )
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


def _normalize_compare_value(value) -> str:
    if isinstance(value, bool):
        return str(value).lower()
    return str(value).strip().upper()


def _parse_min_pixels(text: str) -> int | None:
    match = re.search(
        r"(?:at\s+least\s+(\d+)\s+pixels|pixels?\s+should\s+be\s+at\s+least\s+(\d+))",
        text,
        re.IGNORECASE,
    )
    if not match:
        return None
    return int(match.group(1) or match.group(2))


def _parse_size_dims(value) -> tuple[int, int] | None:
    if not isinstance(value, str):
        return None
    match = re.search(r"(\d{2,5})\s*[xX×]\s*(\d{2,5})", value)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2))


def _format_rule_attributes(rule: dict, task_type: str, max_items: int = 4) -> str:
    attrs = rule.get("attributes") or {}
    parts: list[str] = []
    for key, value in attrs.items():
        if task_type != "text_to_speech" and key == "default" and value == "enabled":
            continue
        parts.append(f"{key}={value}")
    if not parts:
        return "<default rule>"
    return ", ".join(parts[:max_items])


def _best_rule_mismatch(credit_rules: list, merged_params: dict, task_type: str) -> dict | None:
    if not credit_rules:
        return None

    best: dict | None = None
    normalized_params = {
        str(k).strip().lower(): _normalize_compare_value(v)
        for k, v in merged_params.items()
    }

    for rule in credit_rules:
        attrs = rule.get("attributes") or {}
        if not attrs:
            continue

        missing: list[str] = []
        conflicts: list[tuple[str, str, str]] = []
        matched = 0

        for key, expected in attrs.items():
            if task_type != "text_to_speech" and key == "default" and expected == "enabled":
                continue
            k = str(key).strip().lower()
            expected_norm = _normalize_compare_value(expected)
            actual_norm = normalized_params.get(k)
            if actual_norm is None:
                missing.append(str(key))
            elif actual_norm == expected_norm:
                matched += 1
            else:
                actual_raw = merged_params.get(key, merged_params.get(k, ""))
                conflicts.append((str(key), str(actual_raw), str(expected)))

        score = matched * 3 - len(missing) * 2 - len(conflicts) * 3
        candidate = {
            "rule": rule,
            "missing": missing,
            "conflicts": conflicts,
            "matched": matched,
            "score": score,
        }
        if best is None or candidate["score"] > best["score"]:
            best = candidate

    return best


def build_contextual_diagnosis(error_info: dict,
                               task_type: str,
                               model_params: dict,
                               current_params: dict | None,
                               input_images: list[str] | None,
                               credit_rules: list | None) -> dict:
    """
    Diagnose failure using model context + effective params + raw error.
    """
    code = error_info.get("code")
    raw_message = str(error_info.get("message") or "")
    msg_lower = raw_message.lower()

    merged_params = dict(model_params.get("form_params") or {})
    merged_params.update(current_params or {})
    media_inputs = input_images or []
    model_name = model_params.get("model_name") or "unknown_model"
    model_id = model_params.get("model_id") or "unknown_model_id"

    diagnosis = {
        "code": code,
        "confidence": "medium",
        "headline": "Model task failed with current configuration",
        "reasoning": [],
        "actions": [],
        "model_name": model_name,
        "model_id": model_id,
        "task_type": task_type,
    }

    input_required = {
        "image_to_image",
        "image_to_video",
        "first_last_frame_to_video",
        "reference_image_to_video",
    }
    if task_type in input_required and not media_inputs:
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "Missing required reference media for this task type"
        diagnosis["reasoning"].append(
            f"{task_type} requires input media, but input_images is empty."
        )
        diagnosis["actions"].append("Provide at least one URL/path via --input-images.")
        if task_type == "first_last_frame_to_video":
            diagnosis["actions"].append("Provide at least 2 frames: first and last.")
        return diagnosis

    if task_type == "first_last_frame_to_video" and 0 < len(media_inputs) < 2:
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "Insufficient frames for first_last_frame_to_video"
        diagnosis["reasoning"].append(
            f"Received {len(media_inputs)} media item(s); this mode typically needs first+last frames."
        )
        diagnosis["actions"].append("Pass two frame URLs in --input-images.")
        return diagnosis

    if code == 401 or "unauthorized" in msg_lower:
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "API key is invalid or unauthorized"
        diagnosis["actions"].append("Regenerate API key: https://www.imaclaw.ai/imaclaw/apikey")
        diagnosis["actions"].append("Retry with the new key in --api-key.")
        return diagnosis

    if code == 4008 or "insufficient points" in msg_lower:
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "Account points are not enough for this model request"
        diagnosis["reasoning"].append(
            f"Model {model_name} ({model_id}) charges by attribute/profile."
        )
        diagnosis["actions"].append("Top up credits: https://www.imaclaw.ai/imaclaw/subscription")
        diagnosis["actions"].append("Or switch to a lower-cost model/parameter profile.")
        return diagnosis

    min_pixels = _parse_min_pixels(raw_message)
    requested_dims = _parse_size_dims(str(merged_params.get("size") or ""))
    fallback_dims = _parse_size_dims(raw_message)
    dims = requested_dims or fallback_dims
    if min_pixels is not None and dims is not None:
        requested_pixels = dims[0] * dims[1]
        if requested_pixels < min_pixels:
            diagnosis["confidence"] = "high"
            diagnosis["headline"] = "Output size is below this model's minimum pixel requirement"
            diagnosis["reasoning"].append(
                f"Requested size {dims[0]}x{dims[1]} ({requested_pixels} px) is below required {min_pixels} px."
            )
            target = int(math.ceil(math.sqrt(min_pixels)))
            diagnosis["actions"].append(f"Increase --size to at least around {target}x{target}.")
            diagnosis["actions"].append("Then retry with the same model.")
            return diagnosis

    credit_rules = credit_rules or []
    rule_mismatch = _best_rule_mismatch(credit_rules, merged_params, task_type)
    if (
        code in (6009, 6010)
        or "invalid product attribute" in msg_lower
        or "no matching" in msg_lower
        or "attribute" in msg_lower
    ):
        diagnosis["headline"] = "Current parameter combination does not fit this model rule set"
        diagnosis["confidence"] = "high" if code in (6009, 6010) else "medium"
        diagnosis["reasoning"].append(
            f"Model {model_name} uses attribute-based rules; current overrides conflict with matched rule."
        )
        if rule_mismatch:
            if rule_mismatch["missing"]:
                diagnosis["reasoning"].append(
                    "Missing parameters for best-matching rule: "
                    + ", ".join(rule_mismatch["missing"][:4])
                )
            if rule_mismatch["conflicts"]:
                compact = ", ".join(
                    f"{k}={got} (expected {expected})"
                    for k, got, expected in rule_mismatch["conflicts"][:3]
                )
                diagnosis["reasoning"].append(f"Conflicting values: {compact}")
            diagnosis["actions"].append(
                "Use a rule-compatible profile: "
                + _format_rule_attributes(rule_mismatch["rule"], task_type)
            )
        diagnosis["actions"].append("Remove custom --extra-params and retry with defaults.")
        return diagnosis

    if code == "timeout" or "timed out" in msg_lower:
        diagnosis["confidence"] = "medium"
        diagnosis["headline"] = "Task exceeded polling timeout for current model settings"
        max_wait = (POLL_CONFIG.get(task_type) or {}).get("max_wait")
        if max_wait:
            diagnosis["reasoning"].append(f"Polling waited {max_wait}s without a ready result.")
        diagnosis["actions"].append("Retry with lower complexity (size/resolution/duration).")
        diagnosis["actions"].append("Use --list-models and choose a faster model variant.")
        if task_type in VIDEO_TASK_TYPES:
            diagnosis["actions"].append(f"Check your creation record: {VIDEO_RECORDS_URL}")
        else:
            diagnosis["actions"].append("Check task status in dashboard: https://imagent.bot")
        return diagnosis

    if code == 500 or "internal server error" in msg_lower:
        diagnosis["confidence"] = "medium"
        diagnosis["headline"] = "Backend rejected current parameter complexity"
        for key in ("size", "resolution", "duration", "quality"):
            if key in merged_params:
                fallback = get_param_degradation_strategy(key, str(merged_params[key]))
                if fallback:
                    diagnosis["actions"].append(
                        f"Try {key}={fallback[0]} (current {merged_params[key]})."
                    )
                    break
        diagnosis["actions"].append("Retry after simplifying parameters.")
        return diagnosis

    diagnosis["reasoning"].append(
        f"Model context: {to_user_facing_model_name(model_name, model_id)}, "
        f"task={task_type}, media_count={len(media_inputs)}."
    )
    if merged_params:
        focus_keys = ["size", "resolution", "duration", "quality", "mode"]
        hints = [f"{k}={merged_params[k]}" for k in focus_keys if k in merged_params]
        if hints:
            diagnosis["reasoning"].append("Active key parameters: " + ", ".join(hints))
    diagnosis["actions"].append("Retry with defaults (remove --extra-params).")
    diagnosis["actions"].append("Use --list-models to verify model and supported settings.")
    return diagnosis


def format_user_failure_message(diagnosis: dict,
                                attempts_used: int,
                                max_attempts: int) -> str:
    """Render a user-facing failure summary without exposing raw backend errors."""
    display_model = to_user_facing_model_name(
        diagnosis.get("model_name"),
        diagnosis.get("model_id"),
    )
    lines = [
        f"Task failed after {attempts_used}/{max_attempts} attempt(s).",
        (
            f"Model: {display_model} | "
            f"Task: {diagnosis.get('task_type')}"
        ),
        f"Likely cause ({diagnosis.get('confidence', 'medium')} confidence): {diagnosis.get('headline')}",
    ]

    reasoning = diagnosis.get("reasoning") or []
    if reasoning:
        lines.append("Why this diagnosis:")
        for item in reasoning[:3]:
            lines.append(f"- {item}")

    actions = diagnosis.get("actions") or []
    if actions:
        lines.append("What to do next:")
        for index, action in enumerate(actions[:4], 1):
            lines.append(f"{index}. {action}")

    code = diagnosis.get("code")
    if code not in (None, "", "unknown"):
        lines.append(f"Reference code: {code}")
    lines.append("Technical details were recorded in local logs.")
    return "\n".join(lines)


def get_param_degradation_strategy(param_key: str, current_value: str) -> list:
    """
    Get degradation sequence for a parameter when error occurs.
    
    Returns list of fallback values to try, from high-quality to low-quality.
    Empty list means no degradation available.
    """
    # Size degradation (4K → 2K → 1K → 512px) for image
    if param_key.lower() == "size":
        size_map = {
            "4k": ["2k", "1k", "512px"],
            "2k": ["1k", "512px"],
            "1k": ["512px"],
            "512px": []
        }
        return size_map.get(current_value.lower(), [])
    
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
        
        # Try to degrade a parameter (prioritize based on task type)
        for key in ["size", "resolution", "duration", "quality"]:
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
                         f"The task may still be processing in the background without explicit backend errors. "
                         f"Please check your creation record at {VIDEO_RECORDS_URL}. "
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
                    diagnosis = build_contextual_diagnosis(
                        error_info=error_info,
                        task_type=task_type,
                        model_params=model_params,
                        current_params=current_params,
                        input_images=input_images,
                        credit_rules=credit_rules,
                    )
                    logger.error(
                        "Contextual diagnosis (early give-up): %s",
                        json.dumps(diagnosis, ensure_ascii=False),
                    )
                    raise RuntimeError(
                        format_user_failure_message(
                            diagnosis=diagnosis,
                            attempts_used=attempt,
                            max_attempts=max_attempts,
                        )
                    ) from e
            else:
                logger.error(f"❌ All {max_attempts} attempts failed")

                last_error = attempt_log[-1]["error"]
                diagnosis = build_contextual_diagnosis(
                    error_info=last_error,
                    task_type=task_type,
                    model_params=model_params,
                    current_params=current_params,
                    input_images=input_images,
                    credit_rules=credit_rules,
                )
                logger.error(
                    "Contextual diagnosis (max attempts): %s",
                    json.dumps(diagnosis, ensure_ascii=False),
                )
                logger.error(
                    "Attempt log (debug only): %s",
                    json.dumps(attempt_log, ensure_ascii=False),
                )
                raise RuntimeError(
                    format_user_failure_message(
                        diagnosis=diagnosis,
                        attempts_used=max_attempts,
                        max_attempts=max_attempts,
                    )
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
    canonical_model_id = normalize_model_id(model_params.get("model_id")) or model_params.get("model_id")
    prefs.setdefault(key, {})[task_type] = {
        "model_id":    canonical_model_id,
        "model_name":  model_params["model_name"],
        "credit":      model_params["credit"],
        "last_used":   datetime.now(timezone.utc).isoformat(),
    }
    with open(PREFS_PATH, "w", encoding="utf-8") as f:
        json.dump(prefs, f, ensure_ascii=False, indent=2)


def get_preferred_model_id(user_id: str, task_type: str) -> str | None:
    prefs = load_prefs()
    entry = (prefs.get(f"user_{user_id}") or {}).get(task_type)
    if not entry:
        return None
    return normalize_model_id(entry.get("model_id"))


# ─── CLI Entry Point ──────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="IMA AI Creation Script — reliable task creation via Open API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text to image (SeeDream 4.5 — newest default)
  python3 ima_create.py \\
    --api-key ima_xxx --task-type text_to_image \\
    --model-id doubao-seedream-4.5 --prompt "a cute puppy"

  # Text to image with size override
  python3 ima_create.py \\
    --api-key ima_xxx --task-type text_to_image \\
    --model-id doubao-seedream-4.5 --prompt "city skyline" --size 2k

  # Text to video (Wan 2.6 — most popular default)
  python3 ima_create.py \\
    --api-key ima_xxx --task-type text_to_video \\
    --model-id wan2.6-t2v --prompt "a puppy running on grass, cinematic"

  # Image to video (Wan 2.6)
  python3 ima_create.py \\
    --api-key ima_xxx --task-type image_to_video \\
    --model-id wan2.6-i2v --prompt "camera slowly zooms in" \\
    --input-images https://example.com/photo.jpg

  # Text to music (Suno sonic-v5)
  python3 ima_create.py \\
    --api-key ima_xxx --task-type text_to_music \\
    --model-id sonic --prompt "upbeat lo-fi hip hop, 90 BPM"

  # Text to speech (TTS) — use model_id from --list-models for category text_to_speech
  python3 ima_create.py \\
    --api-key ima_xxx --task-type text_to_speech \\
    --model-id <from list-models> --prompt "Text to be spoken"

  # List all models for a category
  python3 ima_create.py \\
    --api-key ima_xxx --task-type text_to_video --list-models
""",
    )

    p.add_argument("--api-key",
                   help="IMA Open API key (starts with ima_). Required for video/music/TTS tasks, "
                        "optional for image tasks (use --kie-key instead).")
    p.add_argument("--kie-key",
                   help="KIE API key for image generation (text_to_image, image_to_image). "
                        "Takes precedence over --api-key for image tasks.")
    p.add_argument("--callback-url",
                   help="KIE callback URL (required for KIE image tasks). "
                        "e.g. https://xxx.trycloudflare.com/kie-callback")
    p.add_argument("--task-type", required=True,
                   choices=list(POLL_CONFIG.keys()),
                   help="Task type to create")
    p.add_argument("--model-id",
                   help="Model ID from product list (e.g. doubao-seedream-4.5)")
    p.add_argument("--version-id",
                   help="Specific version ID — overrides auto-select of latest")
    p.add_argument("--prompt",
                   help="Generation prompt (required unless --list-models)")
    p.add_argument("--input-images", nargs="*", action="append", default=[],
                   help="Input image URLs or local file paths (for image_to_image, image_to_video, etc.). "
                        "Can be repeated multiple times; values are merged. "
                        "Local files are automatically uploaded using the API key.")
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


def flatten_input_images_args(raw_groups) -> list[str]:
    """Merge repeated --input-images groups into one flat list."""
    flattened: list[str] = []
    for group in raw_groups or []:
        if isinstance(group, list):
            flattened.extend([str(v) for v in group if str(v).strip()])
        elif group is not None and str(group).strip():
            flattened.append(str(group))
    return flattened


def main():
    args   = build_parser().parse_args()
    base   = args.base_url
    apikey = args.api_key or args.kie_key  # Use kie_key for images
    if args.model_id:
        args.model_id = normalize_model_id(args.model_id) or args.model_id

    start_time = time.time()
    masked_key = f"{apikey[:10]}..." if len(apikey) > 10 else "***"
    logger.info(f"Script started: task_type={args.task_type}, model_id={args.model_id or 'auto'}, "
                f"api_key={masked_key}")

    # ── Image tasks: use KIE API ──────────────────────────────────────────────
    if args.task_type in IMAGE_TASK_TYPES:
        kie_key = args.kie_key or os.environ.get("KIE_API_KEY")
        if not kie_key:
            # Try to load from credentials file
            cred_path = os.path.expanduser("~/.openclaw/credentials/kie.json")
            if os.path.exists(cred_path):
                try:
                    with open(cred_path) as f:
                        kie_key = json.load(f).get("api_key")
                except Exception:
                    pass
            if not kie_key:
                print("❌ --kie-key required for image tasks (or set KIE_API_KEY env var)", file=sys.stderr)
                sys.exit(1)

        if not args.callback_url:
            callback_url = os.environ.get("KIE_CALLBACK_URL")
        else:
            callback_url = args.callback_url

        print(f"🖼️  Using KIE API for image generation", flush=True)
        print(f"   Model: nano-banana-2, Resolution: 1K, Aspect: 16:9")

        # Create KIE task
        task_result = create_kie_image_task(
            api_key=kie_key,
            prompt=args.prompt or "",
            model="nano-banana-2",
            resolution="1K",
            aspect_ratio="16:9",
            callback_url=callback_url
        )

        task_id = task_result.get("task_id")
        if not task_id:
            print(f"❌ KIE task creation failed: {task_result}", file=sys.stderr)
            sys.exit(1)

        print(f"✅ KIE Task created: {task_id}", flush=True)

        # Poll for completion
        print(f"⏳ Polling KIE task...", flush=True)
        try:
            result = poll_kie_task(kie_key, task_id,
                                 interval=POLL_CONFIG["text_to_image"]["interval"],
                                 max_wait=POLL_CONFIG["text_to_image"]["max_wait"])
            image_url = get_kie_image_url(kie_key, task_id)
            elapsed = time.time() - start_time
            print(f"\n✅ KIE Image generated successfully!", flush=True)
            print(f"   Image URL: {image_url}", flush=True)
            print(f"   Time: {elapsed:.1f}s", flush=True)
            sys.exit(0)
        except RuntimeError as e:
            print(f"❌ KIE task failed: {e}", file=sys.stderr)
            sys.exit(1)

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

    # ── 3b. Resolve local image paths → CDN URLs ─────────────────────────────
    raw_inputs = flatten_input_images_args(args.input_images)
    resolved_inputs: list[str] = []
    for src in raw_inputs:
        if src.startswith("https://") or src.startswith("http://"):
            resolved_inputs.append(src)
        else:
            print(f"📤 Uploading local image: {os.path.basename(src)}", flush=True)
            try:
                cdn_url = prepare_image_url(src, apikey)
                resolved_inputs.append(cdn_url)
                print(f"   ✅ Uploaded → {cdn_url}", flush=True)
            except Exception as e:
                logger.error(f"Image upload failed: {src} — {e}")
                print(f"❌ Failed to upload image {src}: {e}", file=sys.stderr)
                sys.exit(1)

    # ── 4. Create task (with Reflection) ──────────────────────────────────────
    print(f"\n🚀 Creating task…", flush=True)
    try:
        task_id = create_task_with_reflection(
            base_url=base,
            api_key=apikey,
            task_type=args.task_type,
            model_params=mp,
            prompt=args.prompt,
            input_images=resolved_inputs,
            extra_params=extra if extra else None,
            max_attempts=3  # Up to 3 automatic retries with reflection
        )
    except RuntimeError as e:
        logger.error(f"Task creation failed after reflection: {str(e)}")
        print(f"❌ Create task failed:\n{e}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Task created: {task_id}", flush=True)

    # ── 5. Poll for result ─────────────────────────────────────────────────────
    cfg        = POLL_CONFIG.get(args.task_type, {"interval": 5, "max_wait": 300})
    est_max    = cfg["max_wait"] // 2   # optimistic estimate = half of max_wait
    print(f"\n⏳ Polling… (interval={cfg['interval']}s, max={cfg['max_wait']}s)",
          flush=True)

    try:
        media = poll_task(base, apikey, task_id,
                          task_type=args.task_type,
                          estimated_max=est_max,
                          poll_interval=cfg["interval"],
                          max_wait=cfg["max_wait"])
    except (TimeoutError, RuntimeError) as e:
        logger.error(f"Task polling failed: {str(e)}")
        poll_error = extract_error_info(e)
        diagnosis = build_contextual_diagnosis(
            error_info=poll_error,
            task_type=args.task_type,
            model_params=mp,
            current_params=extra if extra else {},
            input_images=resolved_inputs,
            credit_rules=mp.get("all_credit_rules", []),
        )
        logger.error(
            "Polling contextual diagnosis: %s",
            json.dumps(diagnosis, ensure_ascii=False),
        )
        print(
            "\n❌ "
            + format_user_failure_message(
                diagnosis=diagnosis,
                attempts_used=1,
                max_attempts=1,
            ),
            file=sys.stderr,
        )
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
