from __future__ import annotations

import hashlib
import logging
import time
import uuid

import requests

from ima_runtime.shared.catalog import select_credit_rule_by_params
from ima_runtime.shared.catalog import apply_virtual_param_overrides
from ima_runtime.shared.config import (
    APP_ID,
    APP_KEY,
    DEFAULT_IM_BASE_URL,
    VIDEO_MAX_WAIT_SECONDS,
    VIDEO_RECORDS_URL,
)
from ima_runtime.shared.media_utils import assert_public_https_url


logger = logging.getLogger("ima_skills")


def make_headers(api_key: str, language: str = "en") -> dict:
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "x-app-source": "ima_skills",
        "x_app_language": language,
    }


def _gen_sign() -> tuple[str, str, str]:
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

        if data.get("code") not in (0, 200):
            raise RuntimeError(f"Get upload token failed: {data.get('message')}")

        token_data = data.get("data", {})
        ful = token_data.get("ful")
        fdl = token_data.get("fdl")
        if not ful or not fdl:
            raise RuntimeError("Get upload token failed: missing ful/fdl in response")
        assert_public_https_url(ful)
        assert_public_https_url(fdl)
        return token_data
    except requests.RequestException as e:
        logger.error(f"Failed to get upload token: {e}")
        raise RuntimeError(f"Failed to get upload token: {e}")


def upload_to_oss(image_bytes: bytes, content_type: str, ful: str) -> None:
    """Step 2: PUT image bytes to the presigned OSS URL."""
    assert_public_https_url(ful)
    logger.info(f"Uploading {len(image_bytes)} bytes to OSS...")

    try:
        resp = requests.put(ful, data=image_bytes,
                           headers={"Content-Type": content_type}, timeout=60)
        resp.raise_for_status()
        logger.info("Upload successful")
    except requests.RequestException as e:
        logger.error(f"Upload failed: {e}")
        raise RuntimeError(f"Upload failed: {e}")


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


def create_task(base_url: str, api_key: str,
                task_type: str, model_params: dict,
                prompt: str,
                input_images: list[str] | None = None,
                extra_params: dict | None = None,
                src_image: list[dict] | None = None,
                src_video: list[dict] | None = None,
                src_audio: list[dict] | None = None) -> str:
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
        remapped_extra_params = apply_virtual_param_overrides(
            model_params.get("virtual_fields", []),
            extra_params or {},
        )
        merged_params = {**model_params.get('form_params', {}), **remapped_extra_params}
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
    remapped_extra_params = apply_virtual_param_overrides(
        model_params.get("virtual_fields", []),
        extra_params or {},
    )
    if remapped_extra_params:
        for key, value in remapped_extra_params.items():
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
    if remapped_extra_params and "model" in remapped_extra_params:
        # Allow user to explicitly override the version
        inner["model"] = remapped_extra_params["model"]

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
        "parameters": [{
            "attribute_id":  attribute_id,
            # Use raw model_id from product list when available to match backend expectations.
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
    if src_image:
        payload["src_image"] = src_image
        payload["src_img_url"] = [item["url"] for item in src_image if item.get("url")]
    else:
        payload["src_img_url"] = input_images

    url     = f"{base_url}/open/v1/tasks/create"
    headers = make_headers(api_key)

    if src_video:
        payload["src_video"] = src_video
    if src_audio:
        payload["src_audio"] = src_audio

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
                f"model={model_params['model_name']} "
                f"task_type={task_type} "
                f"attribute_id={attribute_id} "
                f"credit={credit}"
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


def poll_task(base_url: str, api_key: str, task_id: str,
              estimated_max: int = 120,
              poll_interval: int = 5,
              max_wait: int = VIDEO_MAX_WAIT_SECONDS,
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
                f"Task {task_id} timed out after {max_wait}s without explicit backend errors. "
                f"Please check your creation record at {VIDEO_RECORDS_URL}."
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
