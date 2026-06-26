#!/usr/bin/env python3
"""
IMA Voice/Music Creation Script — ima_voice_create.py
(version tracked in SKILL.md frontmatter)

Specialized script for music/audio generation via IMA Open API.
Handles: product list query → virtual param resolution → task create → poll status

🆕 v1.1.0 Features:
  - ✨ Reflection mechanism: Automatic error recovery with 3-layer retry strategy
  - ✨ Smart parameter adjustment for Error 6009/6010
  - ✨ User-friendly error messages with model suggestions
  - ✨ Transparent logging of all retry attempts

🆕 v1.0.8 Features:
  - Enhanced error handling for 401 (Unauthorized) and 4008 (Insufficient points)
  - Clickable links to API key generation and credit purchase pages

Usage:
  python3 ima_voice_create.py \\
    --api-key  ima_xxx \\
    --model-id  sonic \\
    --prompt   "upbeat lo-fi hip hop, 90 BPM"

Supports text_to_music task type only.
Models: Suno (sonic), DouBao BGM (GenBGM), DouBao Song (GenSong)

Logs: ~/.openclaw/logs/ima_skills/ima_create_YYYYMMDD.log
"""

import argparse
import json
import os
import sys
import time
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
TASK_TYPE        = "text_to_music"  # Fixed task type for voice/music generation

# Poll configuration for music generation
POLL_CONFIG = {
    "interval": 5,
    "max_wait": 300,  # Increased for Suno (slow generation, 120-180s typical)
}


# ─── HTTP helpers ─────────────────────────────────────────────────────────────

def make_headers(api_key: str, language: str = "en") -> dict:
    return {
        "Authorization":  f"Bearer {api_key}",
        "Content-Type":   "application/json",
        "User-Agent":     "IMA-OpenAPI-Client/Skill-1.0.2",
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
            else:
                error_msg += f"\nrequest={json.dumps(payload, ensure_ascii=False)}"
            
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


def generate_user_suggestion(reflection: ReflectionLog, model_params: dict) -> str:
    """
    Generate user-friendly error message from reflection log.
    
    Shows what went wrong and suggests alternative models/parameters.
    """
    if not reflection.attempts:
        return "❌ 音频生成失败：未知错误"
    
    last_attempt = reflection.attempts[-1]
    error_code = last_attempt.get("error_code")
    removed_params = []
    
    # Collect all removed params across attempts
    for attempt in reflection.attempts:
        removed_params.extend(attempt.get("removed_params", []))
    
    removed_params = list(set(removed_params))  # Deduplicate
    
    msg_parts = ["❌ 音频生成失败"]
    msg_parts.append(f"\n• 尝试次数: {len(reflection.attempts)}")
    msg_parts.append(f"\n• 模型: {model_params['model_name']}")
    
    if removed_params:
        msg_parts.append(f"\n• 不支持的参数: {', '.join(removed_params)}")
    
    if error_code == 6009:
        msg_parts.append("\n\n❓ 原因: 模型不支持当前参数组合")
        msg_parts.append("\n💡 建议:")
        msg_parts.append("\n  1. 尝试其他模型（推荐: Suno sonic, DouBao GenBGM）")
        msg_parts.append("\n  2. 移除不支持的参数")
    elif error_code == 6010:
        msg_parts.append("\n\n❓ 原因: 参数配置与模型不匹配")
        msg_parts.append("\n💡 建议:")
        msg_parts.append("\n  1. 使用模型的默认参数")
        msg_parts.append("\n  2. 尝试其他模型")
    else:
        msg_parts.append("\n\n❓ 原因: 生成参数配置异常")
        msg_parts.append("\n💡 建议: 换个模型试试（推荐: Suno sonic）")
    
    # Add reflection log (condensed)
    msg_parts.append("\n\n📝 反省日志:")
    for attempt in reflection.attempts:
        msg_parts.append(f"\n  [{attempt['attempt']}] {attempt['reflection']}")
    
    return "".join(msg_parts)


# ─── Step 3: Create Task (Legacy Wrapper) ─────────────────────────────────────

def load_prefs() -> dict:
    try:
        with open(PREFS_PATH, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_pref(user_id: str, model_params: dict):
    os.makedirs(os.path.dirname(PREFS_PATH), exist_ok=True)
    prefs = load_prefs()
    key   = f"user_{user_id}"
    prefs.setdefault(key, {})[TASK_TYPE] = {
        "model_id":    model_params["model_id"],
        "model_name":  model_params["model_name"],
        "credit":      model_params["credit"],
        "last_used":   datetime.now(timezone.utc).isoformat(),
    }
    with open(PREFS_PATH, "w", encoding="utf-8") as f:
        json.dump(prefs, f, ensure_ascii=False, indent=2)


def get_preferred_model_id(user_id: str) -> str | None:
    prefs = load_prefs()
    entry = (prefs.get(f"user_{user_id}") or {}).get(TASK_TYPE)
    return entry.get("model_id") if entry else None


# ─── CLI Entry Point ──────────────────────────────────────────────────────────

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="IMA Voice/Music Creation Script — specialized for music generation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate music with Suno (default, most powerful)
  python3 ima_voice_create.py \\
    --api-key ima_xxx \\
    --model-id sonic \\
    --prompt "upbeat lo-fi hip hop, 90 BPM, no vocals"

  # Generate music with DouBao BGM (background music)
  python3 ima_voice_create.py \\
    --api-key ima_xxx \\
    --model-id GenBGM \\
    --prompt "ambient chill, peaceful"

  # Generate song with DouBao Song
  python3 ima_voice_create.py \\
    --api-key ima_xxx \\
    --model-id GenSong \\
    --prompt "pop ballad, female vocals"

  # List all available music models
  python3 ima_voice_create.py \\
    --api-key ima_xxx \\
    --list-models
    
  # With extra Suno parameters
  python3 ima_voice_create.py \\
    --api-key ima_xxx \\
    --model-id sonic \\
    --prompt "以后都用 Suno" \\
    --extra-params '{"custom_mode": true, "make_instrumental": false}'
""",
    )

    p.add_argument("--api-key",  required=False,
                   help="IMA Open API key (starts with ima_). Can also use IMA_API_KEY env var")
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
    p.add_argument("--user-id", default="default",
                   help="User ID for preference memory")
    p.add_argument("--list-models", action="store_true",
                   help="List all available music models and exit")
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
    logger.info(f"Script started: task_type={TASK_TYPE}, model_id={args.model_id or 'auto'}, "
                f"api_key={masked_key}")

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
        # Check user preference
        pref_model = get_preferred_model_id(args.user_id)
        if pref_model:
            args.model_id = pref_model
            print(f"💡 Using your preferred model: {pref_model}", flush=True)
        else:
            print("❌ --model-id is required (no saved preference found)", file=sys.stderr)
            print("   Run with --list-models to see available models", file=sys.stderr)
            print("   Recommended: sonic (Suno), GenBGM (DouBao BGM), GenSong (DouBao Song)", file=sys.stderr)
            sys.exit(1)

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
        if len(reflection.attempts) > 1:
            print(f"\n🧠 反省日志 ({len(reflection.attempts)} 次尝试):")
            for attempt in reflection.attempts:
                status = "✅" if attempt.get("error_code") is None else "❌"
                print(f"   {status} [尝试 {attempt['attempt']}] {attempt['reflection']}")
        
        if not task_id:
            # Generate user suggestion
            user_msg = generate_user_suggestion(reflection, mp)
            print(f"\n{user_msg}", file=sys.stderr)
            sys.exit(1)
        
    except RuntimeError as e:
        logger.error(f"Task creation failed: {str(e)}")
        print(f"❌ Create task failed: {e}", file=sys.stderr)
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
        print(f"\n❌ {e}", file=sys.stderr)
        sys.exit(1)

    # ── 6. Save preference ────────────────────────────────────────────────────
    save_pref(args.user_id, mp)

    # ── 7. Output result ───────────────────────────────────────────────────────
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
