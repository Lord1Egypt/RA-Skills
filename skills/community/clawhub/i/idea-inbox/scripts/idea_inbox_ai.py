#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import sys
import time
import tomllib
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

WORKSPACE = Path(os.environ.get("OPENCLAW_WORKSPACE", "/Users/hanxiaolin/.openclaw/workspace"))
CODEX_CONFIG = Path(os.environ.get("CODEX_CONFIG", str(Path.home() / ".codex" / "config.toml")))
CODEX_AUTH = Path(os.environ.get("CODEX_AUTH", str(Path.home() / ".codex" / "auth.json")))
OPENCLAW_CONFIG = Path(os.environ.get("OPENCLAW_CONFIG", str(Path.home() / ".openclaw" / "openclaw.json")))

DEFAULT_PROMPT = Path(__file__).resolve().parent.parent / "prompts" / "classify.json"
DEFAULT_MODEL = os.environ.get("IDEA_INBOX_MODEL", "").strip() or "gpt-5.2"
TIMEOUT = int(os.environ.get("IDEA_INBOX_TIMEOUT", "60"))
RETRIES = max(1, int(os.environ.get("IDEA_INBOX_RETRIES", "3")))

CATEGORY_ENUM = ["产品", "技术", "商业", "管理", "内容", "生活", "其他"]


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_prompt(path: Path | None) -> tuple[str, str]:
    p = path or DEFAULT_PROMPT
    payload = json.loads(p.read_text(encoding="utf-8"))
    return str(payload.get("instructions") or "").strip(), str(payload.get("prompt") or "").strip()


def _normalize_model_id(model_id: str) -> str:
    return model_id[:-6] if model_id.endswith("-codex") else model_id


def _load_codex_config() -> dict[str, Any] | None:
    if not CODEX_CONFIG.exists():
        return None
    return tomllib.loads(CODEX_CONFIG.read_text(encoding="utf-8"))


def _load_codex_auth() -> dict[str, Any] | None:
    if not CODEX_AUTH.exists():
        return None
    return json.loads(CODEX_AUTH.read_text(encoding="utf-8"))


def _load_openclaw_config() -> dict[str, Any] | None:
    if not OPENCLAW_CONFIG.exists():
        return None
    return json.loads(OPENCLAW_CONFIG.read_text(encoding="utf-8"))


def _pick_provider(model_override: str | None) -> tuple[dict[str, Any], str, str] | None:
    # Prefer Codex provider config; read API key from ~/.codex/auth.json (NOT env).
    try:
        codex = _load_codex_config()
    except Exception:
        codex = None

    if codex:
        providers = codex.get("model_providers") or {}
        if isinstance(providers, dict) and providers:
            provider_name = codex.get("model_provider") or ""
            if provider_name not in providers:
                provider_name = next(iter(providers.keys()))
            provider = providers.get(provider_name) or {}
            base_url = provider.get("base_url") or provider.get("baseUrl")
            wire_api = provider.get("wire_api") or provider.get("wireApi") or "responses"

            auth = _load_codex_auth() or {}
            api_key = auth.get("OPENAI_API_KEY") or auth.get("openai_api_key")

            if base_url and api_key:
                model = _normalize_model_id(model_override or DEFAULT_MODEL or codex.get("model") or "")
                api_type = "openai-responses" if str(wire_api).lower() == "responses" else "openai-completions"

                headers: dict[str, str] = {}
                auth_header = True
                try:
                    openclaw = _load_openclaw_config() or {}
                    oc_provider = (openclaw.get("models") or {}).get("providers", {}).get(provider_name)
                    if isinstance(oc_provider, dict):
                        headers = oc_provider.get("headers") or {}
                        if "authHeader" in oc_provider:
                            auth_header = bool(oc_provider.get("authHeader"))
                except Exception:
                    pass

                return ({"baseUrl": base_url, "apiKey": api_key, "api": api_type, "headers": headers, "authHeader": auth_header}, model, api_type)

    # Fallback: OpenClaw provider config (still do NOT read env keys)
    try:
        oc = _load_openclaw_config()
    except Exception:
        oc = None
    if not oc:
        return None

    providers = (oc.get("models") or {}).get("providers") or {}
    if not isinstance(providers, dict) or not providers:
        return None

    provider_name = next(iter(providers.keys()))
    provider = providers.get(provider_name) or {}
    base_url = provider.get("baseUrl") or provider.get("base_url")
    api_key = provider.get("apiKey") or provider.get("api_key")
    api_type = provider.get("api") or provider.get("wire_api") or "openai-completions"
    model = _normalize_model_id(model_override or DEFAULT_MODEL)

    if base_url and api_key:
        headers = provider.get("headers") or {}
        auth_header = bool(provider.get("authHeader", True))
        return ({"baseUrl": base_url, "apiKey": api_key, "api": str(api_type), "headers": headers, "authHeader": auth_header}, model, str(api_type))

    return None


def _openai_endpoint(base_url: str, path: str) -> str:
    base = (base_url or "").rstrip("/")
    if base.endswith("/v1"):
        return f"{base}{path}"
    return f"{base}/v1{path}"


def _http_post_json(url: str, headers: dict[str, str], payload: dict[str, Any], timeout: int) -> dict[str, Any]:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/json")
    for k, v in headers.items():
        if v is None:
            continue
        req.add_header(k, str(v))
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read().decode("utf-8", errors="replace")
        return json.loads(raw)


def _extract_text(api_type: str, obj: dict[str, Any]) -> str:
    if api_type == "openai-responses":
        if isinstance(obj.get("output_text"), str):
            return obj["output_text"].strip()
        out = obj.get("output")
        if isinstance(out, list):
            chunks: list[str] = []
            for item in out:
                if not isinstance(item, dict):
                    continue
                content = item.get("content")
                if isinstance(content, list):
                    for c in content:
                        if isinstance(c, dict) and c.get("type") in ("output_text", "text") and isinstance(c.get("text"), str):
                            chunks.append(c["text"])
            txt = "".join(chunks).strip()
            if txt:
                return txt
        return ""

    # openai-completions/chat.completions
    try:
        return (obj.get("choices") or [{}])[0].get("message", {}).get("content", "").strip()
    except Exception:
        return ""


def _clean_json_text(text: str) -> str:
    # Remove code fences if any; then trim.
    t = text.strip()
    t = re.sub(r"^```[a-zA-Z0-9_-]*\n", "", t)
    t = re.sub(r"\n```$", "", t)
    return t.strip()


def _validate_payload(obj: dict[str, Any]) -> dict[str, Any]:
    category = str(obj.get("category") or "").strip()
    tags = obj.get("tags") or []
    summary = str(obj.get("summary") or "").strip()

    if category not in CATEGORY_ENUM:
        category = "其他"

    if not isinstance(tags, list):
        tags = []
    tags2: list[str] = []
    for x in tags:
        s = str(x).strip()
        if not s:
            continue
        s = s.lstrip("#").strip()
        if len(s) > 24:
            s = s[:24]
        tags2.append(s)
    if not tags2:
        tags2 = ["其他"]
    tags2 = tags2[:5]

    if not summary:
        summary = "（无）"
    if len(summary) > 500:
        summary = summary[:500]

    return {"category": category, "tags": tags2, "summary": summary}


def classify(text: str, prompt_path: str | None = None, model: str | None = None) -> dict[str, Any]:
    provider_pick = _pick_provider(model)
    if not provider_pick:
        raise RuntimeError("No model provider found. Check ~/.codex/config.toml and ~/.codex/auth.json")

    provider, model_id, api_type = provider_pick
    instructions, prompt_tpl = _load_prompt(Path(prompt_path) if prompt_path else None)
    prompt = (prompt_tpl or "").replace("{{TEXT}}", text.strip())

    headers = dict(provider.get("headers") or {})
    if provider.get("authHeader", True):
        headers["Authorization"] = f"Bearer {provider['apiKey']}"
    else:
        headers["x-api-key"] = str(provider["apiKey"])

    last_err: Exception | None = None
    for attempt in range(1, RETRIES + 1):
        try:
            if api_type == "openai-responses":
                url = _openai_endpoint(provider["baseUrl"], "/responses")
                payload = {
                    "model": model_id,
                    "input": (
                        f"{instructions}\n\n" +
                        f"{prompt}\n\n" +
                        "请只输出严格JSON。"
                    ),
                    "temperature": 0.2,
                }
                obj = _http_post_json(url, headers, payload, timeout=TIMEOUT)
            else:
                url = _openai_endpoint(provider["baseUrl"], "/chat/completions")
                payload = {
                    "model": model_id,
                    "messages": [
                        {"role": "system", "content": instructions},
                        {"role": "user", "content": prompt + "\n\n请只输出严格JSON。"},
                    ],
                    "temperature": 0.2,
                }
                obj = _http_post_json(url, headers, payload, timeout=TIMEOUT)

            raw = _extract_text(api_type, obj)
            raw = _clean_json_text(raw)
            data = json.loads(raw)
            if not isinstance(data, dict):
                raise ValueError("Model output is not a JSON object")
            return _validate_payload(data)
        except Exception as e:
            last_err = e
            time.sleep(0.4 * attempt)

    raise RuntimeError(f"Model classify failed: {last_err}")


def main() -> None:
    text = sys.stdin.read().strip()
    if not text:
        print(json.dumps({"error": "empty input"}, ensure_ascii=False))
        sys.exit(2)
    try:
        out = classify(text)
        print(json.dumps(out, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
