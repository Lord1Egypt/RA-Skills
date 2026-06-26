"""
IMA API Client Module
Version: 1.0.0 (Production Environment Only)

Handles all HTTP API calls to api.imastudio.com:
- Product list queries
- Task creation
- Task status polling
"""

import json
import time

import requests

from ima_constants import (
    ALLOWED_MODEL_IDS,
    normalize_model_id,
    MAX_POLL_WAIT_SECONDS,
    VIDEO_RECORDS_URL,
)
from ima_logger import get_logger

logger = get_logger()


def redact_headers(headers: dict) -> dict:
    """Return a copy of headers with sensitive values masked for logging."""
    redacted = dict(headers)
    auth_value = redacted.get("Authorization")
    if auth_value:
        scheme, _, token = auth_value.partition(" ")
        if token:
            preview = token[:6] + "..." if len(token) > 6 else "***"
            redacted["Authorization"] = f"{scheme} {preview}".strip()
        else:
            redacted["Authorization"] = "***"
    return redacted

# ─── HTTP Helpers ─────────────────────────────────────────────────────────────

def make_headers(api_key: str, language: str = "en") -> dict:
    """Generate HTTP headers for IMA API requests."""
    return {
        "Authorization":  f"Bearer {api_key}",
        "Content-Type":   "application/json",
        "User-Agent":     "IMA-OpenAPI-Client/ima-seedance2-video-generator_1.0.0",
        "x-app-source":   "ima_skills",
        "x_app_language": language,
    }

# ─── Product List API ─────────────────────────────────────────────────────────

def get_product_list(base_url: str, api_key: str, category: str,
                     app: str = "ima", platform: str = "web",
                     language: str = "en", model_ids: list[str] | None = None) -> list:
    """
    GET /open/v1/product/list
    Returns the V2 tree: type=2 are model groups, type=3 are versions (leaves).
    Only type=3 nodes have credit_rules and form_config.
    
    Args:
        model_ids: Optional list of model IDs to filter. 
                   Defaults to ["ima-pro", "ima-pro-fast"] if not provided.
    """
    # Default to skill-supported models if not specified
    if model_ids is None:
        model_ids = ["ima-pro", "ima-pro-fast"]
    
    url     = f"{base_url}/open/v1/product/list"
    params  = {"app": app, "platform": platform, "category": category}
    
    # Always add model_ids filter (now guaranteed to have a value)
    if model_ids:
        params["model_ids"] = ",".join(model_ids)
    
    headers = make_headers(api_key, language)    
    try:
        # DEBUG: Log full request details
        logger.error(f"DEBUG REQUEST: URL={url}, params={params}, headers={redact_headers(headers)}")
        
        resp = requests.get(url, params=params, headers=headers, timeout=30)
        
        # DEBUG: Log response
        logger.error(f"DEBUG RESPONSE: HTTP {resp.status_code}, body={resp.text[:500]}")
        
        # Parse JSON response (don't check HTTP status first!)
        try:
            data = resp.json()
        except ValueError as json_err:
            # Non-JSON response indicates HTTP-level error
            logger.error(f"Product list API returned non-JSON response: "
                        f"HTTP {resp.status_code}, body={resp.text[:200]}")
            raise RuntimeError(
                f"Product list API returned non-JSON response (HTTP {resp.status_code})"
            ) from json_err
        
        # Check business code (0 or 200 = success)
        code = data.get("code")
        if code in (0, 200):
            return data.get("data") or []
        
        # Business errors - provide detailed error based on code
        message = data.get("message") or "Unknown error"
        
        if code == 401:
            error_msg = f"IMA API Key unauthorized (code=401): {message}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        elif code == 6009:
            error_msg = f"Invalid parameters (code=6009): {message}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        elif code == 6010:
            error_msg = f"Parameters violate model constraints (code=6010): {message}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        else:
            error_msg = f"Product list API error: code={code}, msg={message}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)
        
    except requests.RequestException as e:
        logger.error(f"Product list request failed: {str(e)}")
        raise

def find_model_version(product_tree: list, target_model_id: str,
                       target_version_id: str | None = None) -> dict | None:
    """
    Walk the V2 tree and find a type=3 leaf node matching target_model_id.
    If target_version_id is given, match exactly; otherwise return the last
    (usually newest) matching version.
    """
    canonical_target_model_id = normalize_model_id(target_model_id)
    if canonical_target_model_id not in ALLOWED_MODEL_IDS:
        logger.error(
            f"Model not allowed in ima-seedance2-video-generator: model_id={target_model_id}, "
            f"allowed={sorted(ALLOWED_MODEL_IDS)}"
        )
        return None

    candidates = []

    def walk(nodes: list):
        for node in nodes:
            if node.get("type") == "3":
                mid = normalize_model_id(node.get("model_id", ""))
                vid = node.get("id", "")
                if mid == canonical_target_model_id:
                    if target_version_id is None or vid == target_version_id:
                        candidates.append(node)
            children = node.get("children") or []
            walk(children)

    walk(product_tree)

    if not candidates:
        logger.error(f"Model not found: model_id={canonical_target_model_id}, version_id={target_version_id}")
        return None
    
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
                result.append({
                    "name":       node.get("name", ""),
                    "model_id":   normalize_model_id(raw_model_id) or raw_model_id,
                    "raw_model_id": raw_model_id,
                    "version_id": node.get("id", ""),
                    "credit":     cr.get("points", 0),
                    "attr_id":    cr.get("attribute_id", 0),
                })
            walk(node.get("children") or [])

    walk(product_tree)
    return result

def filter_allowed_models(models: list[dict]) -> list[dict]:
    """Keep only models exposed by ima-seedance2-video-generator."""
    filtered = []
    for model in models:
        canonical_model_id = normalize_model_id(model.get("model_id"))
        if canonical_model_id in ALLOWED_MODEL_IDS:
            patched = dict(model)
            patched["model_id"] = canonical_model_id
            filtered.append(patched)
    return filtered

# ─── Task Creation API ────────────────────────────────────────────────────────

def create_task(base_url: str, api_key: str,
                task_type: str, model_params: dict,
                prompt: str,
                input_urls: list[str] | None = None,
                extra_params: dict | None = None,
                src_image: list[dict] | None = None,
                src_video: list[dict] | None = None,
                src_audio: list[dict] | None = None) -> str:
    """
    POST /open/v1/tasks/create
    
    NOTE: This is the core task creation function. For automatic retry with
    reflection, use create_task_with_reflection() from ima_reflection module.
    
    Args:
        base_url: API base URL
        api_key: IMA API key
        task_type: Task type (text_to_video, image_to_video, etc.)
        model_params: Model parameters from extract_model_params()
        prompt: Generation prompt
        input_urls: List of uploaded/reference media URLs (mapped to API input_images/src_img_url)
        extra_params: User overrides for parameters
        src_image: List of image metadata dicts (V2 API): [{"url": str, "width": int, "height": int}]
        src_video: List of video metadata dicts (V2 API): [{"url": str, "duration": float, "width": int, "height": int, "cover": str}]
        src_audio: List of audio metadata dicts (V2 API): [{"url": str, "duration": float}]
    
    Returns:
        task_id: Created task ID
    
    Raises:
        RuntimeError: If task creation fails
    """
    if input_urls is None:
        input_urls = []

    model_id = normalize_model_id(model_params.get("model_id"))
    if model_id not in ALLOWED_MODEL_IDS:
        raise RuntimeError(
            f"model_id '{model_params.get('model_id')}' is not allowed in ima-seedance2-video-generator. "
            f"Allowed: {', '.join(sorted(ALLOWED_MODEL_IDS))}"
        )

    # ─── Smart Credit Rule Selection (error 6010 prevention) ─────────────────
    # Reference: ima-sevio-ai implementation for proper attribute_id matching
    
    all_rules = model_params.get("all_credit_rules", [])
    normalized_rule_params = {}  # Canonical values from matched rule
    attribute_id = model_params["attribute_id"]  # Default from extract_model_params
    credit = model_params["credit"]
    
    if all_rules:
        # Merge form_params and user overrides for matching
        merged_params = {**model_params.get('form_params', {}), **(extra_params or {})}
        
        # CRITICAL: Only include fields that determine credit cost
        # For Seedance 2.0, credit_rules only contain: duration, resolution
        # Exclude: audio (always true), aspect_ratio (doesn't affect cost)
        candidate_params = {k: v for k, v in merged_params.items() 
                           if k in ["resolution", "duration", "mode", "quality", "n"]}
        
        # DEBUG: Print all_credit_rules and candidate_params
        print("=" * 80)
        print("🔍 CREDIT RULE SELECTION DEBUG")
        print("=" * 80)
        print(f"all_credit_rules ({len(all_rules)} rules):")
        for i, rule in enumerate(all_rules):
            print(f"  Rule {i+1}: attribute_id={rule.get('attribute_id')}, points={rule.get('points')}, attributes={rule.get('attributes')}")
        print(f"\ncandidate_params (for matching):")
        print(f"  {candidate_params}")
        print("=" * 80)
        
        if candidate_params:
            from ima_param_resolver import select_credit_rule_by_params
            selected_rule = select_credit_rule_by_params(all_rules, candidate_params)
            
            # DEBUG: Print selected rule
            print("=" * 80)
            print("✅ SELECTED RULE")
            print("=" * 80)
            print(f"  attribute_id: {selected_rule.get('attribute_id')}")
            print(f"  points: {selected_rule.get('points')}")
            print(f"  attributes: {selected_rule.get('attributes')}")
            print("=" * 80)
            
            if selected_rule:
                attribute_id = selected_rule.get("attribute_id", attribute_id)
                credit = selected_rule.get("points", credit)
                
                # Extract normalized canonical values from matched rule's attributes
                # This ensures API gets "720P" (from rule) instead of "720p" (from user)
                rule_attrs = selected_rule.get("attributes", {})
                for key in candidate_params.keys():
                    if key in rule_attrs:
                        normalized_rule_params[key] = rule_attrs[key]
                
                # Smart selection successful
                pass
    
    # ─── Parameter Merge (4-layer priority) ──────────────────────────────────
    # Priority (low → high):
    #   1. rule_attributes (required fields from matched credit_rule)
    #   2. form_params (optional defaults from form_config)
    #   3. normalized_rule_params (canonical values from matched rule)
    #   4. extra_params (user overrides for non-canonical fields)
    
    inner: dict = {}
    
    # Layer 1: Required fields from credit_rule.attributes
    rule_attrs = model_params.get("rule_attributes", {})
    if rule_attrs:
        inner.update(rule_attrs)
    
    # Layer 2: Form config defaults
    inner.update(model_params.get("form_params", {}))
    
    # Layer 3: Canonical values from matched rule (overwrites user's case/format)
    if normalized_rule_params:
        inner.update(normalized_rule_params)
    
    # Layer 4: User overrides (only for non-canonical fields)
    if extra_params:
        for key, value in extra_params.items():
            if key not in normalized_rule_params:  # Don't override canonical values
                inner[key] = value
    
    # Required inner fields (always set these last)
    inner["prompt"] = prompt
    inner["n"] = int(inner.get("n", 1))
    inner["input_images"] = input_urls
    inner["cast"] = {"points": credit, "attribute_id": attribute_id}

    payload = {
        "task_type":          task_type,
        "enable_multi_model": False,
        "parameters": [{
            "attribute_id":  attribute_id,
            "model_id":      model_params.get("model_id_raw") or model_params["model_id"],
            "model_name":    model_params["model_name"],
            "model_version": model_params["model_version"],
            "app":           "ima",
            "platform":      "web",
            "category":      task_type,
            "credit":        credit,
            "parameters":    inner,
        }],
    }
    
    # Add new V2 API parameters (asset compliance verified)
    if src_image:
        payload["src_image"] = src_image
    if src_video:
        payload["src_video"] = src_video
    if src_audio:
        payload["src_audio"] = src_audio
    
    # IMA API field: src_img_url
    if src_image:
        payload["src_img_url"] = [item["url"] for item in src_image if item.get("url")]

    url     = f"{base_url}/open/v1/tasks/create"
    headers = make_headers(api_key)

    # DEBUG: Print complete request payload
    print("=" * 80)
    print("🔍 COMPLETE REQUEST PAYLOAD (create_task)")
    print("=" * 80)
    print(f"URL: {url}")
    print(f"Headers: {json.dumps({k: v if k != 'Authorization' else 'Bearer ima_***' for k, v in headers.items()}, indent=2)}")
    print(f"Payload (JSON):")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    print("=" * 80)

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        
        # DEBUG: Print complete response
        print("=" * 80)
        print("📥 COMPLETE RESPONSE")
        print("=" * 80)
        print(f"HTTP Status: {resp.status_code}")
        print(f"Headers: {json.dumps(dict(resp.headers), indent=2)}")
        print(f"Body:")
        try:
            print(json.dumps(resp.json(), indent=2, ensure_ascii=False))
        except:
            print(resp.text)
        print("=" * 80)
        
        # Parse JSON response (don't check HTTP status first!)
        try:
            data = resp.json()
        except ValueError as json_err:
            logger.error(f"Create task API returned non-JSON response: "
                        f"HTTP {resp.status_code}, body={resp.text[:200]}")
            raise RuntimeError(
                f"Create task API returned non-JSON response (HTTP {resp.status_code})"
            ) from json_err
        
        # Check business code (0 or 200 = success)
        code = data.get("code")
        if code in (0, 200):
            task_id = (data.get("data") or {}).get("id")
            if not task_id:
                logger.error("Task create failed: no task_id in response")
                raise RuntimeError(f"No task_id in response: {data}")
            return task_id
        
        # Business errors - provide detailed error based on code
        message = data.get("message") or "Unknown error"
        
        if code == 401:
            error_msg = f"IMA API Key unauthorized (code=401): {message}"
            logger.error(f"Task create failed: {error_msg}, attribute_id={attribute_id}, credit={credit}")
            raise RuntimeError(error_msg)
        elif code == 6009:
            error_msg = f"Invalid parameters (code=6009): {message}"
            logger.error(f"Task create failed: {error_msg}, attribute_id={attribute_id}, credit={credit}")
            raise RuntimeError(error_msg)
        elif code == 6010:
            error_msg = f"Parameters violate model constraints (code=6010): {message}"
            logger.error(f"Task create failed: {error_msg}, attribute_id={attribute_id}, credit={credit}")
            raise RuntimeError(error_msg)
        else:
            error_msg = f"Create task failed — code={code} message={message}"
            logger.error(f"Task create failed: code={code}, msg={message}, "
                        f"attribute_id={attribute_id}, credit={credit}")
            raise RuntimeError(error_msg)
        
    except requests.RequestException as e:
        logger.error(f"Task create request failed: {str(e)}")
        raise

# ─── Task Polling API ─────────────────────────────────────────────────────────

def poll_task(base_url: str, api_key: str, task_id: str,
              estimated_max: int = 120,
              poll_interval: int = 5,
              max_wait: int = MAX_POLL_WAIT_SECONDS,
              on_progress=None) -> dict:
    """
    POST /open/v1/tasks/detail — poll until completion.

    - resource_status (int or null): 0=processing, 1=done, 2=failed, 3=deleted.
      null is treated as 0.
    - status (string): "pending" | "processing" | "success" | "failed".
    - Stop only when ALL medias have resource_status == 1 and no status == "failed".
    - Returns the first completed media dict (with url) when all are done.
    """
    url     = f"{base_url}/open/v1/tasks/detail"
    headers = make_headers(api_key)
    start   = time.time()
    max_wait = min(max_wait, MAX_POLL_WAIT_SECONDS)

    last_progress_report = 0
    progress_interval    = 15 if poll_interval <= 5 else 30

    while True:
        elapsed = time.time() - start
        if elapsed > max_wait:
            logger.error(f"Task timeout: task_id={task_id}, elapsed={int(elapsed)}s, max_wait={max_wait}s")
            raise TimeoutError(
                f"Task {task_id} timed out after {max_wait}s without explicit backend errors. "
                f"Please check your creation record at {VIDEO_RECORDS_URL}."
            )

        resp = requests.post(url, json={"task_id": task_id},
                             headers=headers, timeout=30)
        
        # Parse JSON response (don't check HTTP status first!)
        try:
            data = resp.json()
        except ValueError as json_err:
            logger.error(f"Poll task API returned non-JSON response: "
                        f"HTTP {resp.status_code}, body={resp.text[:200]}")
            raise RuntimeError(
                f"Poll task API returned non-JSON response (HTTP {resp.status_code})"
            ) from json_err
        
        # Check business code (0 or 200 = success)
        code = data.get("code")
        if code not in (0, 200):
            message = data.get("message") or "Unknown error"
            
            if code == 401:
                error_msg = f"IMA API Key unauthorized (code=401): {message}"
                logger.error(error_msg)
                raise RuntimeError(error_msg)
            else:
                error_msg = f"Poll error — code={code} msg={message}"
                logger.error(error_msg)
                raise RuntimeError(error_msg)

        task   = data.get("data") or {}
        medias = task.get("medias") or []

        def _rs(m):
            v = m.get("resource_status")
            return 0 if (v is None or v == "") else int(v)

        for media in medias:
            rs = _rs(media)
            if rs == 2:
                err = media.get("error_msg") or media.get("remark") or "unknown"
                logger.error(f"Task failed: task_id={task_id}, resource_status=2, error={err}")
                raise RuntimeError(f"Generation failed (resource_status=2): {err}")
            if rs == 3:
                logger.error(f"Task deleted: task_id={task_id}")
                raise RuntimeError("Task was deleted")

        if medias and all(_rs(m) == 1 for m in medias):
            for media in medias:
                if (media.get("status") or "").strip().lower() == "failed":
                    err = media.get("error_msg") or media.get("remark") or "unknown"
                    logger.error(f"Task failed: task_id={task_id}, status=failed, error={err}")
                    raise RuntimeError(f"Generation failed: {err}")
            first_media = medias[0]
            result_url = first_media.get("url") or first_media.get("watermark_url")
            if result_url:
                return first_media

        if elapsed - last_progress_report >= progress_interval:
            pct = min(95, int(elapsed / estimated_max * 100))
            msg = f"⏳ {int(elapsed)}s elapsed … {pct}%"
            if elapsed > estimated_max:
                msg += "  (taking longer than expected, please wait…)"
            if on_progress:
                on_progress(pct, int(elapsed), msg)
            else:
                logger.info(msg)
            last_progress_report = elapsed

        time.sleep(poll_interval)
