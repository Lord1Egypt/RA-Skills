"""
NIMA Unified LLM Client
========================
Single source of truth for LLM calls across nima-core.

Canonical environment variables:
  NIMA_LLM_PROVIDER
  NIMA_LLM_API_KEY
  NIMA_LLM_MODEL
  NIMA_LLM_BASE_URL

Backward compatibility:
  - provider=openai   falls back to OPENAI_API_KEY when NIMA_LLM_API_KEY is unset
  - provider=anthropic falls back to ANTHROPIC_API_KEY when NIMA_LLM_API_KEY is unset
  - provider can be inferred from NIMA_LLM_BASE_URL; otherwise defaults to openai
"""

from __future__ import annotations

import json
import logging
import urllib.error
import urllib.request
from urllib.parse import urlparse
from pathlib import Path
from typing import Optional, Dict, Any

from nima_core.llm_config import resolve_llm_config

__all__ = ["llm_complete", "get_llm_config", "load_nima_env"]
logger = logging.getLogger(__name__)
APPLICATION_JSON = "application/json"


def _parse_env_line(line: str):
    line = line.strip()
    if not line or line.startswith("#") or "=" not in line:
        return None
    key, val = line.split("=", 1)
    val = val.strip()
    if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
        val = val[1:-1]
    return key, val


def load_nima_env():
    env_path = Path.home() / ".nima" / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for raw in f:
                parsed = _parse_env_line(raw)
                if parsed:
                    import os
                    os.environ[parsed[0]] = parsed[1]


load_nima_env()


def _openai_config(key: str, base_url: str, model: str) -> Dict[str, Any]:
    base = base_url.rstrip("/")
    return {
        "provider": "openai",
        "base_url": base,
        "model": model,
        "key": key,
        "headers": {"Authorization": f"Bearer {key}", "Content-Type": APPLICATION_JSON},
        "endpoint": f"{base}/chat/completions",
        "response_path": ["choices", 0, "message", "content"],
    }


def _anthropic_config(key: str, base_url: str, model: str) -> Dict[str, Any]:
    base = base_url.rstrip("/")
    endpoint = (base + "/messages") if base.endswith("/v1") else (base + "/v1/messages")
    return {
        "provider": "anthropic",
        "base_url": base,
        "model": model,
        "key": key,
        "headers": {"x-api-key": key, "anthropic-version": "2023-06-01", "content-type": APPLICATION_JSON},
        "endpoint": endpoint,
        "response_path": ["content", 0, "text"],
    }


def get_llm_config(model_override: Optional[str] = None, provider_override: Optional[str] = None) -> Optional[Dict[str, Any]]:
    resolved = resolve_llm_config(provider=provider_override, model=model_override)
    if not resolved.api_key:
        return None
    if resolved.provider == "anthropic":
        return _anthropic_config(resolved.api_key, resolved.base_url, resolved.model)
    return _openai_config(resolved.api_key, resolved.base_url, resolved.model)


def _do_llm_request(prompt: str, config: Dict[str, Any], max_tokens: int = 200, timeout: int = 30, system: Optional[str] = None) -> Optional[str]:
    endpoint = config.get("endpoint")
    if not endpoint:
        return None
    parsed = urlparse(endpoint)
    if parsed.scheme not in ("http", "https"):
        logger.warning("Invalid URL scheme in endpoint: %s", endpoint)
        return None

    if config["provider"] == "anthropic":
        payload = {
            "model": config["model"],
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            payload["system"] = system
    else:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        payload = {
            "model": config["model"],
            "messages": messages,
            "max_tokens": max_tokens,
        }

    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers=dict(config["headers"]),
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    out = data
    for key in config["response_path"]:
        if isinstance(out, list):
            out = out[0]
        out = out[key]
    return out.strip() if isinstance(out, str) else out


def llm_complete(prompt: str, model: Optional[str] = None, max_tokens: int = 200, timeout: int = 30, system: Optional[str] = None, provider_override: Optional[str] = None) -> Optional[str]:
    config = get_llm_config(model_override=model, provider_override=provider_override)
    if not config:
        logger.warning("No LLM provider configured (set NIMA_LLM_PROVIDER, NIMA_LLM_API_KEY, NIMA_LLM_MODEL, and optionally NIMA_LLM_BASE_URL)")
        return None
    try:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})
        if config["provider"] == "anthropic":
            payload = {"model": config["model"], "max_tokens": max_tokens, "messages": [m for m in messages if m["role"] != "system"]}
            if system:
                payload["system"] = system
        else:
            payload = {"model": config["model"], "max_tokens": max_tokens, "messages": messages}
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(config["endpoint"], data=data, headers=config["headers"])
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            result = json.loads(resp.read())
            value = result
            for key in config["response_path"]:
                value = value[key]
            text = value.strip() if isinstance(value, str) else str(value)
            return text if text and len(text) > 5 else None
    except urllib.error.HTTPError as e:
        logger.warning("LLM HTTP %d from %s (%s) — %s", e.code, config["provider"], config["endpoint"], e.read().decode()[:200] if hasattr(e, "read") else str(e))
        return None
    except Exception as e:
        logger.warning("LLM error from %s: %s", config["provider"], e)
        return None


def llm_complete_with_fallback(prompt: str, model: Optional[str] = None, max_tokens: int = 200, timeout: int = 30, system: Optional[str] = None) -> Optional[str]:
    """Try auto-detected provider first, then explicit providers without duplicating request logic."""
    tried = set()
    for provider in (None, "openai", "anthropic"):
        try:
            cfg = get_llm_config(model_override=model, provider_override=provider)
            provider_name = cfg.get("provider") if cfg else None
            if provider_name in tried:
                continue
            if provider_name:
                tried.add(provider_name)
            result = llm_complete(
                prompt,
                model=model,
                max_tokens=max_tokens,
                timeout=timeout,
                system=system,
                provider_override=provider,
            )
            if result is not None:
                return result
        except Exception as e:
            logger.warning(f"LLM fallback attempt failed ({provider or 'auto'}): {e}")
            continue
    return None

def extractive_distill(texts: list, date_str: str = "", max_len: int = 300) -> str:
    sentences = []
    for text in texts[:10]:
        for sent in text.replace("\n", ". ").split(". "):
            sent = sent.strip()
            if len(sent) > 20 and not sent.startswith("[") and not sent.startswith("{"):
                sentences.append(sent)
                break
    if not sentences:
        return f"Session from {date_str} ({len(texts)} turns)"
    combined = ". ".join(sentences[:5])
    if len(combined) > max_len:
        combined = combined[:max_len] + "..."
    prefix = f"Session {date_str}: " if date_str else ""
    return prefix + combined
