#!/usr/bin/env python3
"""
IMA Voice/Music Creation Script — ima_voice_create.py
Version: 1.2.2

Music/audio generation via IMA Open API (text_to_music only).
Flow: product list → virtual param resolution → task create → poll status.

Models: Suno (sonic), DouBao BGM (GenBGM), DouBao Song (GenSong).

Usage:
  IMA_API_KEY=ima_xxx python3 ima_voice_create.py --model-id sonic \\
    --prompt "upbeat lo-fi hip hop, 90 BPM"
"""

import argparse
import json
import os
import re
import sys
import time

try:
    import requests
except ImportError:
    print("requests not installed. Run: pip install requests", file=sys.stderr)
    sys.exit(1)

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-5s | %(funcName)-20s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("ima_skills")

# ─── Constants ────────────────────────────────────────────────────────────────

DEFAULT_BASE_URL = "https://api.imastudio.com"
TASK_TYPE        = "text_to_music"  # Fixed task type for voice/music generation

# Poll configuration for music generation
POLL_CONFIG = {
    "interval": 5,
    "max_wait": 480,  # 8-minute cap for text_to_music polling
}


# ─── HTTP helpers ─────────────────────────────────────────────────────────────

def make_headers(api_key: str, language: str = "en") -> dict:
    return {
        "Authorization":  f"Bearer {api_key}",
        "Content-Type":   "application/json",
        "User-Agent":     "IMA-OpenAPI-Client/Skill-1.2.2",
        "x-app-source":   "ima_skills",
        "x_app_language": language,
    }


# ─── Step 1: Product List ─────────────────────────────────────────────────────

def get_product_list(base_url: str, api_key: str,
                     app: str = "ima", platform: str = "web",
                     language: str = "en") -> list:
    """
    GET /open/v1/product/list
    Returns the V2 tree: type=2 are model groups, type=3 are versions (leaves).
    Only type=3 nodes have credit_rules and form_config.
    """
    url     = f"{base_url}/open/v1/product/list"
    params  = {"app": app, "platform": platform, "category": TASK_TYPE}
    headers = make_headers(api_key, language)

    logger.info(f"Query product list: category={TASK_TYPE}, app={app}, platform={platform}")
    
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


# ─── Step 2: Extract Parameters ───────────────────────────────────────────────

def resolve_virtual_param(field: dict) -> dict:
    """
    Handle virtual form fields (is_ui_virtual=True).
    
    Frontend logic (useAgentModeData.ts):
      1. Create sub-forms from ui_params (each has a default value)
      2. Build patch: {ui_param.field: ui_param.value} for each sub-param
      3. Find matching value_mapping rule where source_values == patch
      4. Use target_value as the actual API parameter value
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
      model_version : str   — node["id"]
      form_params   : dict  — resolved form_config defaults (including virtual params)
      rule_attributes : dict — required params from credit_rules[0].attributes
    """
    credit_rules = node.get("credit_rules") or []
    if not credit_rules:
        raise RuntimeError(
            f"No credit_rules found for model '{node.get('model_id')}' "
            f"version '{node.get('id')}'. Cannot determine attribute_id or credit."
        )

    cr = credit_rules[0]
    attribute_id = cr.get("attribute_id", 0)
    credit       = cr.get("points", 0)

    if attribute_id == 0:
        raise RuntimeError(
            f"attribute_id is 0 for model '{node.get('model_id')}'. "
            "This will cause 'Invalid product attribute' error."
        )

    # Build form_config defaults
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

    # Extract credit_rules[].attributes (required by backend validation)
    rule_attributes: dict = {}
    if credit_rules:
        first_rule_attrs = credit_rules[0].get("attributes", {})
        
        # Filter out {"default": "enabled"} marker (not an actual parameter)
        for key, value in first_rule_attrs.items():
            if not (key == "default" and value == "enabled"):
                rule_attributes[key] = value

    logger.info(f"Params extracted: model={node.get('model_id')}, attribute_id={attribute_id}, "
                f"credit={credit}, rule_attrs={len(rule_attributes)} fields")

    return {
        "attribute_id":     attribute_id,
        "credit":           credit,
        "model_id":         node.get("model_id", ""),
        "model_name":       node.get("name", ""),
        "model_version":    node.get("id", ""),
        "form_params":      form_params,
        "rule_attributes":  rule_attributes,
        "all_credit_rules": credit_rules,  # For smart selection
    }


# ─── Step 3: Create Task ──────────────────────────────────────────────────────

def create_task(base_url: str, api_key: str, model_params: dict,
                prompt: str, extra_params: dict | None = None) -> str:
    """
    POST /open/v1/tasks/create
    
    Constructs the full request body for music generation task.
    """
    # Merge parameters in correct priority order
    # Priority (low → high): rule_attributes < form_params < extra_params
    inner: dict = {}
    
    # 1. First merge rule_attributes (required fields from credit_rules)
    rule_attrs = model_params.get("rule_attributes", {})
    if rule_attrs:
        inner.update(rule_attrs)
    
    # 2. Then merge form_config defaults
    inner.update(model_params["form_params"])
    
    # 3. Finally merge user overrides
    if extra_params:
        inner.update(extra_params)

    # Required inner fields
    inner["prompt"]       = prompt
    inner["n"]            = int(inner.get("n", 1))
    inner["input_images"] = []
    inner["cast"]         = {
        "points": model_params["credit"],
        "attribute_id": model_params["attribute_id"]
    }

    payload = {
        "task_type":          TASK_TYPE,
        "enable_multi_model": False,
        "src_img_url":        [],
        "parameters": [{
            "attribute_id":  model_params["attribute_id"],
            "model_id":      model_params["model_id"],
            "model_name":    model_params["model_name"],
            "model_version": model_params["model_version"],
            "app":           "ima",
            "platform":      "web",
            "category":      TASK_TYPE,
            "credit":        model_params["credit"],
            "parameters":    inner,
        }],
    }

    url     = f"{base_url}/open/v1/tasks/create"
    headers = make_headers(api_key)

    logger.info(f"Create task: model={model_params['model_name']}, task_type={TASK_TYPE}, "
                f"credit={model_params['credit']}, attribute_id={model_params['attribute_id']}")

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()

        code = data.get("code")
        if code not in (0, 200):
            logger.error(f"Task create failed: code={code}, msg={data.get('message')}, "
                        f"attribute_id={model_params['attribute_id']}, credit={model_params['credit']}")
            
            # Build helpful error message with links for common errors
            error_msg = f"Create task failed — code={code} message={data.get('message')}"
            
            if code == 401:
                error_msg += "\n\n💡 API key is invalid or unauthorized"
                error_msg += "\n🔗 Generate API Key: https://www.imaclaw.ai/imaclaw/apikey"
            elif code == 4008:
                error_msg += "\n\n💡 Insufficient points to create this task"
                error_msg += "\n🔗 Buy Credits: https://www.imaclaw.ai/imaclaw/subscription"
            
            raise RuntimeError(error_msg)

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
              estimated_max: int = 150, on_progress=None) -> dict:
    """
    POST /open/v1/tasks/detail — poll until completion.
    
    Returns the first completed media dict (with url) when done.
    """
    url     = f"{base_url}/open/v1/tasks/detail"
    headers = make_headers(api_key)
    start   = time.time()

    logger.info(f"Poll task started: task_id={task_id}, max_wait={POLL_CONFIG['max_wait']}s")

    last_progress_report = 0
    progress_interval    = 15

    while True:
        elapsed = time.time() - start
        if elapsed > POLL_CONFIG['max_wait']:
            logger.error(f"Task timeout: task_id={task_id}, elapsed={int(elapsed)}s, max_wait={POLL_CONFIG['max_wait']}s")
            raise TimeoutError(
                f"Task {task_id} timed out after {POLL_CONFIG['max_wait']}s. "
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

        # Normalize resource_status: API may return null; treat as 0 (processing)
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

        time.sleep(POLL_CONFIG['interval'])


# ─── Reflection Mechanism (v1.1.0) ────────────────────────────────────────────

class ReflectionLog:
    """Tracks reflection attempts and errors for user transparency."""
    def __init__(self):
        self.attempts = []
        self.success = False
        self.task_id = None
    
    def add_attempt(self, attempt_num: int, error_code: int | None, 
                   sent_params: dict, attribute_id: int, credit: int,
                   reflection: str, action_taken: str, removed_params: list):
        self.attempts.append({
            "attempt": attempt_num,
            "error_code": error_code,
            "sent_params": sent_params,
            "attribute_id": attribute_id,
            "credit": credit,
            "reflection": reflection,
            "action_taken": action_taken,
            "removed_params": removed_params,
        })
    
    def to_dict(self):
        return {
            "success": self.success,
            "task_id": self.task_id,
            "attempts": len(self.attempts),
            "reflection_log": self.attempts,
        }


def select_credit_rule_by_params(credit_rules: list, user_params: dict) -> dict | None:
    """
    Select the best credit_rule matching user parameters.
    
    Strategy:
    1. Try exact match: ALL rule attributes match user params
    2. Fallback: first rule (default)
    
    Returns the selected credit_rule or None if credit_rules is empty.
    """
    if not credit_rules:
        return None
    
    if not user_params:
        return credit_rules[0]
    
    # Normalize user params
    def normalize_value(v):
        if isinstance(v, bool):
            return str(v).lower()
        if isinstance(v, (int, float)):
            return v
        return str(v).strip()
    
    normalized_user = {
        k.lower().strip(): normalize_value(v)
        for k, v in user_params.items()
    }
    
    # Try exact match
    for cr in credit_rules:
        attrs = cr.get("attributes", {})
        if not attrs:
            continue
        
        normalized_attrs = {
            k.lower().strip(): normalize_value(v)
            for k, v in attrs.items()
        }
        
        # Check if ALL rule attributes match user params
        if all(normalized_user.get(k) == v for k, v in normalized_attrs.items()):
            return cr
    
    # Fallback to first rule
    return credit_rules[0]


def create_task_with_reflection(base_url: str, api_key: str, model_params: dict,
                                prompt: str, extra_params: dict | None = None,
                                max_attempts: int = 3) -> tuple[str | None, ReflectionLog]:
    """
    POST /open/v1/tasks/create — with automatic reflection retry mechanism.
    
    Reflection strategy (3 attempts):
    1. Original params (smart credit_rule selection)
    2. Strict match (remove unsupported params)
    3. Fallback to default (credit_rules[0])
    
    Returns: (task_id, reflection_log)
    """
    reflection = ReflectionLog()
    all_rules = model_params.get("all_credit_rules", [])
    
    if not all_rules:
        logger.warning("No credit_rules found, using direct values")
        all_rules = [{
            "attribute_id": model_params["attribute_id"],
            "points": model_params["credit"],
            "attributes": model_params.get("rule_attributes", {}),
        }]
    
    # Get all possible attribute keys from credit_rules
    all_attr_keys = set()
    for rule in all_rules:
        all_attr_keys.update((rule.get("attributes") or {}).keys())
    
    # Music-specific attribute keys (from real API)
    music_attr_keys = {
        "custom_mode", "make_instrumental", "duration",  # Suno-specific
        "quality", "n",  # Common
    }
    
    # Merge form_params and extra_params
    merged_params = {**model_params.get('form_params', {}), **(extra_params or {})}
    
    # Attempt 1: Original params (smart selection)
    candidate_params = {k: v for k, v in merged_params.items() 
                       if k in music_attr_keys or k in all_attr_keys}
    
    for attempt_num in range(1, max_attempts + 1):
        logger.info(f"🔄 Attempt {attempt_num}/{max_attempts}: {len(candidate_params)} params")
        
        # Select credit_rule based on current candidate_params
        if candidate_params:
            selected_rule = select_credit_rule_by_params(all_rules, candidate_params)
        else:
            selected_rule = all_rules[0]
        
        if not selected_rule:
            selected_rule = all_rules[0]
        
        attribute_id = selected_rule.get("attribute_id", model_params["attribute_id"])
        credit = selected_rule.get("points", model_params["credit"])
        rule_attrs = selected_rule.get("attributes", {})
        
        # Build inner parameters
        inner: dict = {}
        
        # Merge: rule_attributes < form_params < candidate_params
        if rule_attrs:
            inner.update(rule_attrs)
        inner.update(model_params["form_params"])
        inner.update(candidate_params)
        
        # Required fields
        inner["prompt"] = prompt
        inner["n"] = int(inner.get("n", 1))
        inner["input_images"] = []
        inner["cast"] = {"points": credit, "attribute_id": attribute_id}
        
        payload = {
            "task_type": TASK_TYPE,
            "enable_multi_model": False,
            "src_img_url": [],
            "parameters": [{
                "attribute_id": attribute_id,
                "model_id": model_params["model_id"],
                "model_name": model_params["model_name"],
                "model_version": model_params["model_version"],
                "app": "ima",
                "platform": "web",
                "category": TASK_TYPE,
                "credit": credit,
                "parameters": inner,
            }],
        }
        
        url = f"{base_url}/open/v1/tasks/create"
        headers = make_headers(api_key)
        
        logger.info(f"Attempt {attempt_num}: attribute_id={attribute_id}, credit={credit}, params={list(candidate_params.keys())}")
        
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            
            code = data.get("code")
            error_msg = data.get("message", "")
            
            # Success
            if code in (0, 200):
                task_id = (data.get("data") or {}).get("id")
                if task_id:
                    reflection.success = True
                    reflection.task_id = task_id
                    
                    action = "original" if attempt_num == 1 else ("strict_match" if attempt_num == 2 else "fallback")
                    reflection.add_attempt(
                        attempt_num, None, candidate_params, attribute_id, credit,
                        f"✅ 成功（尝试 {attempt_num}）", action, []
                    )
                    
                    logger.info(f"✅ Task created successfully on attempt {attempt_num}: {task_id}")
                    return task_id, reflection
            
            # Failure: reflection needed
            error_code = None
            if "6009" in error_msg or "No exact rule match" in error_msg:
                error_code = 6009
            elif "6010" in error_msg or "Attribute ID does not match" in error_msg:
                error_code = 6010
            
            # Handle special error codes with links
            if code == 401:
                error_msg += "\n💡 API key is invalid or unauthorized"
                error_msg += "\n🔗 Generate API Key: https://www.imaclaw.ai/imaclaw/apikey"
            elif code == 4008:
                error_msg += "\n💡 Insufficient points to create this task"
                error_msg += "\n🔗 Buy Credits: https://www.imaclaw.ai/imaclaw/subscription"
            
            # Determine reflection strategy
            removed_params = []
            next_action = ""
            next_reflection = ""
            
            if attempt_num == 1:
                # Strategy 1 → 2: Strict match (remove unsupported params)
                removed_params = [k for k in candidate_params if k not in rule_attrs]
                candidate_params = {k: v for k, v in candidate_params.items() if k in rule_attrs}
                next_action = "strict_match"
                next_reflection = f"移除不支持的参数: {removed_params}" if removed_params else "无需移除参数"
            
            elif attempt_num == 2:
                # Strategy 2 → 3: Fallback to default rule
                default_rule = all_rules[0]
                attribute_id = default_rule.get("attribute_id")
                credit = default_rule.get("points")
                candidate_params = default_rule.get("attributes", {}).copy()
                next_action = "fallback_to_default"
                next_reflection = f"回退到默认规则（attribute_id={attribute_id}, credit={credit}）"
                removed_params = list(merged_params.keys())
            
            else:
                # Attempt 3 failed — no more strategies
                next_action = "max_attempts_reached"
                next_reflection = "❌ 已达最大尝试次数"
            
            reflection.add_attempt(
                attempt_num, error_code, candidate_params, attribute_id, credit,
                f"❌ {error_msg} → {next_reflection}", next_action, removed_params
            )
            
            logger.warning(f"Attempt {attempt_num} failed (code={code}): {error_msg} → {next_action}")
            
            # Max attempts reached
            if attempt_num >= max_attempts:
                logger.error(f"All {max_attempts} attempts failed")
                return None, reflection
        
        except requests.RequestException as e:
            logger.error(f"Attempt {attempt_num} request failed: {e}")
            reflection.add_attempt(
                attempt_num, None, candidate_params, attribute_id, credit,
                f"❌ 请求失败: {str(e)}", "network_error", []
            )
            
            if attempt_num >= max_attempts:
                return None, reflection
    
    # Should not reach here
    return None, reflection


def extract_error_info(exception: Exception) -> dict:
    error_str = str(exception)
    if isinstance(exception, TimeoutError):
        return {"code": "timeout", "message": error_str, "type": "timeout"}
    code_match = re.search(r'code[=:]?\s*(\d+)', error_str, re.IGNORECASE)
    if code_match:
        code = int(code_match.group(1))
        return {"code": code, "message": error_str, "type": f"api_{code}"}
    return {"code": "unknown", "message": error_str, "type": "unknown"}


def build_contextual_diagnosis(error_info: dict,
                               model_params: dict,
                               current_params: dict | None,
                               reflection: ReflectionLog | None = None) -> dict:
    code = error_info.get("code")
    raw_message = str(error_info.get("message") or "")
    msg_lower = raw_message.lower()
    model_name = model_params.get("model_name") or "unknown_model"
    model_id = model_params.get("model_id") or "unknown_model_id"
    current_params = current_params or {}

    removed_params: list[str] = []
    attempts = 0
    if reflection and reflection.attempts:
        attempts = len(reflection.attempts)
        for a in reflection.attempts:
            removed_params.extend(a.get("removed_params", []))
    removed_params = sorted(set(removed_params))

    diagnosis = {
        "code": code,
        "confidence": "medium",
        "headline": "Music generation failed with current model configuration",
        "reasoning": [],
        "actions": [],
        "model_name": model_name,
        "model_id": model_id,
        "task_type": TASK_TYPE,
        "attempts": attempts,
    }

    if code == 401 or "unauthorized" in msg_lower:
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "API key is invalid or unauthorized"
        diagnosis["actions"].append("Regenerate API key: https://www.imaclaw.ai/imaclaw/apikey")
        diagnosis["actions"].append("Retry with the new key in IMA_API_KEY environment variable.")
        return diagnosis

    if code == 4008 or "insufficient points" in msg_lower:
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "Account points are not enough for this music request"
        diagnosis["actions"].append("Top up credits: https://www.imaclaw.ai/imaclaw/subscription")
        diagnosis["actions"].append("Or switch to a lower-cost model.")
        return diagnosis

    if code in (6009, 6010) or "attribute" in msg_lower or removed_params:
        diagnosis["confidence"] = "high" if code in (6009, 6010) else "medium"
        diagnosis["headline"] = "Current parameter set does not match this music model rules"
        if removed_params:
            diagnosis["reasoning"].append("Unsupported params observed in retries: " + ", ".join(removed_params[:6]))
        if current_params:
            preview = ", ".join(f"{k}={v}" for k, v in list(current_params.items())[:4])
            diagnosis["reasoning"].append("Last attempted params: " + preview)
        diagnosis["actions"].append("Remove custom params and retry with model defaults.")
        diagnosis["actions"].append("Try another model via --list-models (e.g., sonic or GenBGM).")
        return diagnosis

    if code == "timeout" or "timed out" in msg_lower:
        diagnosis["headline"] = "Music task exceeded polling timeout"
        diagnosis["actions"].append("Retry with simpler prompt or default params.")
        diagnosis["actions"].append("Check task status in dashboard: https://imagent.bot")
        return diagnosis

    if "lyrics" in msg_lower and ("format" in msg_lower or "invalid" in msg_lower):
        diagnosis["confidence"] = "high"
        diagnosis["headline"] = "Lyrics format is incompatible with current model requirements"
        diagnosis["actions"].append("Simplify lyrics format or enable auto lyrics if supported.")
        diagnosis["actions"].append("Retry with shorter structured prompt.")
        return diagnosis

    diagnosis["reasoning"].append(f"Model context: {model_name} ({model_id}), task={TASK_TYPE}.")
    diagnosis["actions"].append("Retry with defaults and a simpler prompt.")
    diagnosis["actions"].append("If repeated, switch model via --list-models.")
    return diagnosis


def format_user_failure_message(diagnosis: dict,
                                attempts_used: int,
                                max_attempts: int) -> str:
    lines = [
        f"Music task failed after {attempts_used}/{max_attempts} attempt(s).",
        f"Model: {diagnosis.get('model_name')} ({diagnosis.get('model_id')})",
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
        for i, action in enumerate(actions[:4], 1):
            lines.append(f"{i}. {action}")
    code = diagnosis.get("code")
    if code not in (None, "", "unknown"):
        lines.append(f"Reference code: {code}")
    lines.append("Technical details are shown in current stderr output.")
    return "\n".join(lines)


def generate_user_suggestion(reflection: ReflectionLog, model_params: dict) -> str:
    if not reflection.attempts:
        diagnosis = build_contextual_diagnosis(
            {"code": "unknown", "message": "unknown", "type": "unknown"},
            model_params,
            {},
            reflection,
        )
        return format_user_failure_message(diagnosis, 1, 3)
    last = reflection.attempts[-1]
    error_code = last.get("error_code")
    error_info = {
        "code": error_code if error_code is not None else "unknown",
        "message": last.get("reflection", ""),
        "type": f"api_{error_code}" if error_code is not None else "unknown",
    }
    diagnosis = build_contextual_diagnosis(
        error_info=error_info,
        model_params=model_params,
        current_params=last.get("sent_params") or {},
        reflection=reflection,
    )
    return format_user_failure_message(
        diagnosis,
        attempts_used=len(reflection.attempts),
        max_attempts=max(3, len(reflection.attempts)),
    )


# ─── CLI Entry Point ──────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="IMA Voice/Music Creation Script — specialized for music generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate music with Suno (default, most powerful)
  IMA_API_KEY=ima_xxx python3 ima_voice_create.py \\
    --model-id sonic \\
    --prompt "upbeat lo-fi hip hop, 90 BPM, no vocals"

  # Generate music with DouBao BGM (background music)
  IMA_API_KEY=ima_xxx python3 ima_voice_create.py \\
    --model-id GenBGM \\
    --prompt "ambient chill, peaceful"

  # Generate song with DouBao Song
  IMA_API_KEY=ima_xxx python3 ima_voice_create.py \\
    --model-id GenSong \\
    --prompt "pop ballad, female vocals"

  # List all available music models
  IMA_API_KEY=ima_xxx python3 ima_voice_create.py \\
    --list-models
    
  # With extra Suno parameters
  IMA_API_KEY=ima_xxx python3 ima_voice_create.py \\
    --model-id sonic \\
    --prompt "以后都用 Suno" \\
    --extra-params '{"custom_mode": true, "make_instrumental": false}'
""",
    )

    p.add_argument("--model-id",
                   help="Model ID: sonic (Suno), GenBGM (DouBao BGM), GenSong (DouBao Song)")
    p.add_argument("--version-id",
                   help="Specific version ID — overrides auto-select of latest")
    p.add_argument("--prompt",
                   help="Music generation prompt (required unless --list-models)")
    p.add_argument("--extra-params",
                   help='JSON string of extra parameters, e.g. \'{"custom_mode": true}\'')
    p.add_argument("--language", default="en",
                   help="Language for product labels (en/zh)")
    p.add_argument("--base-url", default=DEFAULT_BASE_URL,
                   help="API base URL")
    p.add_argument("--list-models", action="store_true",
                   help="List all available music models and exit")
    p.add_argument("--output-json", action="store_true",
                   help="Output final result as JSON (for agent parsing)")

    return p


def main():
    args   = build_parser().parse_args()
    base   = args.base_url
    
    # API key is accepted only from environment variable
    apikey = os.getenv("IMA_API_KEY")
    if not apikey:
        logger.error("API key is required. Set IMA_API_KEY environment variable")
        sys.exit(1)

    start_time = time.time()
    logger.info(f"Script started: task_type={TASK_TYPE}, model_id={args.model_id or 'auto'}")

    # ── 1. Query product list ──────────────────────────────────────────────────
    print(f"🔍 Querying music models: category={TASK_TYPE}", flush=True)
    try:
        tree = get_product_list(base, apikey, language=args.language)
    except Exception as e:
        logger.error(f"Product list failed: {str(e)}")
        print(f"❌ Product list failed: {e}", file=sys.stderr)
        sys.exit(1)

    # ── List models mode ───────────────────────────────────────────────────────
    if args.list_models:
        models = list_all_models(tree)
        print(f"\nAvailable music models:")
        print(f"{'Name':<28} {'model_id':<34} {'version_id':<44} {'pts':>4}  attr_id")
        print("─" * 120)
        for m in models:
            print(f"{m['name']:<28} {m['model_id']:<34} {m['version_id']:<44} "
                  f"{m['credit']:>4}  {m['attr_id']}")
        sys.exit(0)

    # ── Resolve model_id ───────────────────────────────────────────────────────
    if not args.model_id:
        args.model_id = "sonic"
        print("💡 --model-id not provided. Defaulting to sonic.", flush=True)

    if not args.prompt:
        print("❌ --prompt is required", file=sys.stderr)
        sys.exit(1)

    # ── 2. Find model version in tree ─────────────────────────────────────────
    node = find_model_version(tree, args.model_id, args.version_id)
    if not node:
        logger.error(f"Model not found: model_id={args.model_id}")
        available = [f"  {m['model_id']}" for m in list_all_models(tree)]
        print(f"❌ model_id='{args.model_id}' not found.",
              file=sys.stderr)
        print("   Available model_ids:\n" + "\n".join(available), file=sys.stderr)
        sys.exit(1)

    # ── 3. Extract params ──────────────────────────────────────────────────────
    try:
        mp = extract_model_params(node)
    except RuntimeError as e:
        logger.error(f"Param extraction failed: {str(e)}")
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)

    print(f"✅ Model found:")
    print(f"   name          = {mp['model_name']}")
    print(f"   model_id      = {mp['model_id']}")
    print(f"   model_version = {mp['model_version']}")
    print(f"   attribute_id  = {mp['attribute_id']}")
    print(f"   credit        = {mp['credit']} pts")

    # Apply extra params
    extra: dict = {}
    if args.extra_params:
        try:
            extra.update(json.loads(args.extra_params))
        except json.JSONDecodeError as e:
            print(f"❌ Invalid --extra-params JSON: {e}", file=sys.stderr)
            sys.exit(1)

    # ── 4. Create task (with reflection) ───────────────────────────────────────
    print(f"\n🚀 Creating music generation task…", flush=True)
    try:
        task_id, reflection = create_task_with_reflection(
            base, apikey, mp, args.prompt,
            extra if extra else None,
            max_attempts=3
        )
        
        # Show reflection log if there were retries
        if task_id and len(reflection.attempts) > 1:
            print(f"\n🧠 反省日志 ({len(reflection.attempts)} 次尝试):")
            for attempt in reflection.attempts:
                status = "✅" if attempt.get("error_code") is None else "❌"
                action = attempt.get("action_taken") or "retry"
                print(f"   {status} [尝试 {attempt['attempt']}] action={action}")
        
        if not task_id:
            # Generate user suggestion
            user_msg = generate_user_suggestion(reflection, mp)
            print(f"\n{user_msg}", file=sys.stderr)
            sys.exit(1)
        
    except RuntimeError as e:
        logger.error(f"Task creation failed: {str(e)}")
        create_error = extract_error_info(e)
        diagnosis = build_contextual_diagnosis(
            error_info=create_error,
            model_params=mp,
            current_params=extra if extra else {},
            reflection=None,
        )
        print(
            "❌ "
            + format_user_failure_message(
                diagnosis=diagnosis,
                attempts_used=1,
                max_attempts=1,
            ),
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"✅ Task created: {task_id}", flush=True)

    # ── 5. Poll for result ─────────────────────────────────────────────────────
    est_max = POLL_CONFIG["max_wait"] // 2  # optimistic estimate
    print(f"\n⏳ Polling… (interval={POLL_CONFIG['interval']}s, max={POLL_CONFIG['max_wait']}s)",
          flush=True)

    try:
        media = poll_task(base, apikey, task_id, estimated_max=est_max)
    except (TimeoutError, RuntimeError) as e:
        logger.error(f"Task polling failed: {str(e)}")
        poll_error = extract_error_info(e)
        diagnosis = build_contextual_diagnosis(
            error_info=poll_error,
            model_params=mp,
            current_params=extra if extra else {},
            reflection=None,
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

    # ── 6. Output result ───────────────────────────────────────────────────────
    result_url = media.get("url") or media.get("preview_url") or ""
    duration   = media.get("duration_str") or ""

    print(f"\n✅ Music generation complete!")
    print(f"   URL:      {result_url}")
    if duration:
        print(f"   Duration: {duration}")

    if args.output_json:
        out = {
            "task_id":    task_id,
            "url":        result_url,
            "duration":   duration,
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
