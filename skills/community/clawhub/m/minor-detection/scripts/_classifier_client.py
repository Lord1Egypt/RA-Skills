'''
模块说明：模型调用适配层
负责：
拼接聊天接口 URL
调外部聊天模型
处理重试
从模型返回文本里提取 JSON
把 request 异常包装成 ClassifierAPIError
'''

from __future__ import annotations

import json
import re
import time
from typing import Any, Dict, List

import requests


class ClassifierAPIError(RuntimeError):
    pass


def _chat_url(base_url: str) -> str:
    normalized = (base_url or "").rstrip("/")
    if normalized.endswith("/chat/completions"):
        return normalized
    return f"{normalized}/chat/completions"


def extract_json_object(text: str) -> Dict[str, Any]:
    cleaned = (text or "").strip()
    if not cleaned:
        raise ClassifierAPIError("classifier returned empty content")
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", cleaned, flags=re.DOTALL | re.IGNORECASE)
    if fenced:
        cleaned = fenced.group(1).strip()
    if cleaned.startswith("{") and cleaned.endswith("}"):
        return json.loads(cleaned)
    match = re.search(r"(\{.*\})", cleaned, flags=re.DOTALL)
    if match:
        return json.loads(match.group(1))
    raise ClassifierAPIError("classifier did not return a JSON object")


def _is_retryable_request_error(exc: requests.RequestException) -> bool:
    if isinstance(exc, (requests.Timeout, requests.ConnectionError)):
        return True
    if isinstance(exc, requests.HTTPError):
        status_code = getattr(exc.response, "status_code", None)
        if status_code in {408, 409, 429}:
            return True
        if status_code is not None and 500 <= int(status_code) < 600:
            return True
    return False


def _format_request_error(exc: requests.RequestException, attempts: int) -> str:
    suffix = f" after {attempts} attempts" if attempts > 1 else ""
    detail = str(exc).strip() or exc.__class__.__name__
    return f"classifier request failed{suffix}: {detail}"


def call_chat_completion(
    *,
    base_url: str,
    api_key: str,
    model: str,
    timeout_sec: int,
    messages: List[Dict[str, str]],
    temperature: float = 0.0,
    max_retries: int = 0,
    retry_backoff_sec: float = 0.0,
) -> tuple[Dict[str, Any], str]:
    if not api_key:
        raise ClassifierAPIError("missing classifier api key")

    total_attempts = max(1, int(max_retries) + 1)
    for attempt in range(total_attempts):
        try:
            response = requests.post(
                _chat_url(base_url),
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "response_format": {"type": "json_object"},
                },
                timeout=timeout_sec,
            )
            response.raise_for_status()
            payload = response.json()
            choices = payload.get("choices") or []
            if not choices:
                raise ClassifierAPIError("classifier returned no choices")
            message = choices[0].get("message") or {}
            content = message.get("content")
            if isinstance(content, list):
                content = "".join(str(item.get("text", "")) for item in content if isinstance(item, dict))
            content_text = str(content or "").strip()
            return extract_json_object(content_text), content_text
        except requests.RequestException as exc:
            attempts_used = attempt + 1
            if attempts_used >= total_attempts or not _is_retryable_request_error(exc):
                raise ClassifierAPIError(_format_request_error(exc, attempts_used)) from exc
            if retry_backoff_sec > 0:
                time.sleep(retry_backoff_sec * (2**attempt))
        except ValueError as exc:
            raise ClassifierAPIError(f"classifier returned invalid API payload: {exc}") from exc