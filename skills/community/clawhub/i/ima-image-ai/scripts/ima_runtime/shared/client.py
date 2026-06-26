from __future__ import annotations

import hashlib
import json
import logging
import time
import uuid

import requests

from ima_runtime.shared.catalog import apply_virtual_param_specs, select_credit_rule_by_params
from ima_runtime.shared.config import APP_ID, APP_KEY, DEFAULT_IM_BASE_URL

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


def _decode_api_response(response, context: str) -> dict:
    try:
        data = response.json()
    except ValueError:
        response.raise_for_status()
        raise RuntimeError(f"{context} failed: response body is not valid JSON")

    code = data.get("code")
    if code in (0, 200):
        return data

    message = data.get("message") or data.get("msg") or data.get("error") or "unknown"
    raise RuntimeError(f"{context} failed: code={code} msg={message}")


def get_upload_token(api_key: str, suffix: str, content_type: str, im_base_url: str = DEFAULT_IM_BASE_URL) -> dict:
    sign, ts, nonce = _gen_sign()
    response = requests.get(
        f"{im_base_url}/api/rest/oss/getuploadtoken",
        params={
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
        },
        timeout=30,
    )
    data = _decode_api_response(response, "Get upload token")
    return data.get("data", {})


def upload_to_oss(image_bytes: bytes, content_type: str, ful: str) -> None:
    response = requests.put(ful, data=image_bytes, headers={"Content-Type": content_type}, timeout=60)
    response.raise_for_status()


def get_product_list(
    base_url: str,
    api_key: str,
    category: str,
    app: str = "ima",
    platform: str = "web",
    language: str = "en",
) -> list:
    response = requests.get(
        f"{base_url}/open/v1/product/list",
        params={"app": app, "platform": platform, "category": category},
        headers=make_headers(api_key, language),
        timeout=30,
    )
    data = _decode_api_response(response, "Product list API error")
    return data.get("data") or []


def create_task(
    base_url: str,
    api_key: str,
    task_type: str,
    model_params: dict,
    prompt: str,
    input_images: list[str] | None = None,
    extra_params: dict | None = None,
) -> str:
    input_images = input_images or []
    effective_extra_params = dict(extra_params or {})
    if model_params.get("virtual_param_specs"):
        effective_extra_params, _ = apply_virtual_param_specs(
            effective_extra_params,
            model_params.get("virtual_param_specs") or [],
        )
    all_rules = model_params.get("all_credit_rules", [])
    normalized_rule_params = {}
    attribute_id = model_params["attribute_id"]
    credit = model_params["credit"]

    if all_rules:
        merged_params = {**model_params.get("form_params", {}), **effective_extra_params}
        candidate_params = {k: v for k, v in merged_params.items() if k in ["size", "quality", "n"]}
        selected_rule = select_credit_rule_by_params(all_rules, candidate_params)
        if selected_rule:
            attribute_id = selected_rule.get("attribute_id", attribute_id)
            credit = selected_rule.get("points", credit)
            for key in ["size", "quality", "n"]:
                if key in (selected_rule.get("attributes") or {}):
                    normalized_rule_params[key] = selected_rule["attributes"][key]
        else:
            selected_rule = None
    else:
        selected_rule = None

    inner = {}
    inner.update(model_params.get("rule_attributes", {}))
    inner.update(model_params.get("form_params", {}))
    inner.update(normalized_rule_params)
    if effective_extra_params:
        for key, value in effective_extra_params.items():
            if key not in normalized_rule_params:
                inner[key] = value
    inner["prompt"] = prompt
    inner["n"] = int(inner.get("n", 1))
    inner["input_images"] = input_images
    inner["cast"] = {"points": credit, "attribute_id": attribute_id}

    payload = {
        "task_type": task_type,
        "enable_multi_model": False,
        "src_img_url": input_images,
        "parameters": [
            {
                "attribute_id": attribute_id,
                "model_id": model_params["model_id"],
                "model_name": model_params["model_name"],
                "model_version": model_params["model_version"],
                "app": "ima",
                "platform": "web",
                "category": task_type,
                "credit": credit,
                "parameters": inner,
            }
        ],
    }

    response = requests.post(
        f"{base_url}/open/v1/tasks/create",
        json=payload,
        headers=make_headers(api_key),
        timeout=30,
    )
    data = _decode_api_response(response, "Create task")
    task_id = (data.get("data") or {}).get("id")
    if not task_id:
        raise RuntimeError(f"No task_id in response: {data}")
    return task_id


def poll_task(
    base_url: str,
    api_key: str,
    task_id: str,
    estimated_max: int = 120,
    poll_interval: int = 5,
    max_wait: int = 600,
    on_progress=None,
) -> dict:
    del estimated_max, on_progress
    start = time.time()
    while True:
        if time.time() - start > max_wait:
            raise TimeoutError(f"Task {task_id} timed out after {max_wait}s. Check the IMA dashboard for status.")
        response = requests.post(
            f"{base_url}/open/v1/tasks/detail",
            json={"task_id": task_id},
            headers=make_headers(api_key),
            timeout=30,
        )
        data = _decode_api_response(response, "Poll task")
        medias = (data.get("data") or {}).get("medias") or []
        for media in medias:
            resource_status = 0 if media.get("resource_status") in (None, "") else int(media.get("resource_status"))
            if resource_status == 2:
                raise RuntimeError(
                    f"Generation failed (resource_status=2): {media.get('error_msg') or media.get('remark') or 'unknown'}"
                )
            if resource_status == 3:
                raise RuntimeError("Task was deleted")
        if medias and all(
            (0 if media.get("resource_status") in (None, "") else int(media.get("resource_status"))) == 1
            for media in medias
        ):
            first_media = medias[0]
            result_url = first_media.get("url") or first_media.get("watermark_url")
            if result_url:
                return first_media
        time.sleep(poll_interval)
