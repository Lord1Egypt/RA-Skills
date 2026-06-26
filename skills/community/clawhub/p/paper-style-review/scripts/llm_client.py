#!/usr/bin/env python3
"""LLM 调用层 — 统一的 AI 检查接口。

使用 OpenAI-compatible API 来做：
- 逻辑通顺检查
- 中文术语规范检查
- 风格偏离检查（对照参考论文）

所有检查都以参考论文为依据，逐段/逐批次进行。
"""

from __future__ import annotations

import json
import os
import sys
import time
from copy import deepcopy
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from openai import OpenAI
from style_prompt_contract import (
    STYLE_PROFILE_EXTRACTION_VERSION,
    STYLE_PROMPT_PROFILE_VERSION,
    build_style_profile_axes_block,
    build_style_prompt_contract_block,
)

# ---------------------------------------------------------------------------
# 默认配置
# ---------------------------------------------------------------------------
DEFAULT_MODEL = "gpt-5.4"
MAX_RETRIES = 2
RETRY_DELAY = 3
DEFAULT_TIMEOUT = 120
SUPPORTED_OPENAI_APIS = {
    "openai",
    "openai-chatcompletions",
    "openai-completions",
    "openai-responses",
    "openai-codex-responses",
}
OPENCLAW_GLOBAL_CONFIG_PATH = Path.home() / ".openclaw" / "openclaw.json"


def _cfg_int(cfg: Dict[str, Any], key: str, default: int) -> int:
    try:
        value = cfg.get(key, default)
        return int(value)
    except Exception:
        return default


def _cfg_str(cfg: Optional[Dict[str, Any]], *keys: str) -> str:
    data = cfg or {}
    for key in keys:
        value = data.get(key)
        if value is None:
            continue
        text = str(value).strip()
        if text:
            return text
    return ""


def _normalize_api_base(base_url: str) -> str:
    base = (base_url or "").strip()
    if not base:
        return ""
    parsed = urlparse(base)
    if parsed.scheme and parsed.netloc and (not parsed.path or parsed.path == "/"):
        return base.rstrip("/") + "/v1"
    return base.rstrip("/")


def _load_json(path: Path) -> Dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _load_openclaw_state() -> Dict[str, Any]:
    global_path = OPENCLAW_GLOBAL_CONFIG_PATH
    global_config = _load_json(global_path) if global_path.exists() else {}

    global_providers = (global_config.get("models") or {}).get("providers") or {}
    if not isinstance(global_providers, dict):
        global_providers = {}

    providers: Dict[str, Dict[str, Any]] = {}
    provider_order: List[str] = []
    for provider_name, provider_cfg in global_providers.items():
        if not isinstance(provider_cfg, dict):
            continue
        provider_order.append(provider_name)
        providers[provider_name] = deepcopy(provider_cfg)

    model_defaults = (global_config.get("agents") or {}).get("defaults", {}).get("model") or {}
    primary_ref = _cfg_str(model_defaults, "primary")
    fallback_refs = []
    if isinstance(model_defaults.get("fallbacks"), list):
        fallback_refs = [str(item).strip() for item in model_defaults["fallbacks"] if str(item).strip()]

    openclaw_env = global_config.get("env") if isinstance(global_config.get("env"), dict) else {}
    return {
        "providers": providers,
        "providerOrder": provider_order,
        "primaryRef": primary_ref,
        "fallbackRefs": fallback_refs,
        "env": openclaw_env,
        "globalConfigPath": str(global_path) if global_path.exists() else None,
    }


def _resolve_model_ref(model_ref: str = "", provider_ref: str = "") -> tuple[str, str]:
    chosen_ref = (model_ref or "").strip()
    provider_name = (provider_ref or "").strip()
    model_name = ""
    if chosen_ref and "/" in chosen_ref:
        provider_name, model_name = chosen_ref.split("/", 1)
    elif chosen_ref and not provider_name:
        model_name = chosen_ref
    return provider_name, model_name


def _select_model_id(provider: Dict[str, Any], desired_model: str = "", *, strict_model: bool = False) -> str:
    models = provider.get("models") or []
    desired = str(desired_model or "").strip()
    if desired:
        for item in models:
            if str((item or {}).get("id") or "").strip() == desired:
                return desired
        if strict_model:
            return ""
    if models:
        selected = str((models[0] or {}).get("id") or "").strip()
        if selected:
            return selected
    return desired


def _candidate_from_provider(
    provider_name: str,
    provider: Dict[str, Any],
    *,
    desired_model: str = "",
    model_ref: str = "",
    source: str,
    strict_model: bool = False,
) -> Dict[str, Any]:
    api_kind = str(provider.get("api") or "").strip()
    if api_kind and api_kind not in SUPPORTED_OPENAI_APIS:
        return {}

    model_name = desired_model
    if model_ref:
        _, ref_model_name = _resolve_model_ref(model_ref=model_ref)
        if ref_model_name:
            model_name = ref_model_name
    selected_model_id = _select_model_id(provider, model_name, strict_model=strict_model)
    api_base = _normalize_api_base(str(provider.get("baseUrl") or ""))
    api_key = str(provider.get("apiKey") or "").strip()
    if not api_base or not api_key or not selected_model_id:
        return {}

    return {
        "apiBase": api_base,
        "apiKey": api_key,
        "model": selected_model_id,
        "modelRef": f"{provider_name}/{selected_model_id}",
        "providerRef": provider_name,
        "providerApi": api_kind,
        "resolvedFrom": source,
    }


def _resolve_provider_candidate(
    state: Dict[str, Any],
    *,
    model_ref: str = "",
    provider_ref: str = "",
    desired_model: str = "",
    source: str,
    strict_model: bool = False,
) -> Dict[str, Any]:
    provider_name, model_name = _resolve_model_ref(model_ref=model_ref, provider_ref=provider_ref)
    if not provider_name:
        return {}
    provider = (state.get("providers") or {}).get(provider_name)
    if not isinstance(provider, dict):
        return {}
    return _candidate_from_provider(
        provider_name,
        provider,
        desired_model=model_name or desired_model,
        model_ref=model_ref,
        source=source,
        strict_model=strict_model,
    )


def _dedupe_candidates(candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    seen = set()
    output: List[Dict[str, Any]] = []
    for candidate in candidates:
        if not candidate:
            continue
        api_base = _normalize_api_base(_cfg_str(candidate, "apiBase", "baseUrl"))
        api_key = _cfg_str(candidate, "apiKey")
        model = _cfg_str(candidate, "model") or DEFAULT_MODEL
        if not api_base or not api_key or not model:
            continue
        key = (
            _cfg_str(candidate, "providerRef"),
            _cfg_str(candidate, "modelRef"),
            api_base,
            api_key,
            model,
        )
        if key in seen:
            continue
        seen.add(key)
        normalized = dict(candidate)
        normalized["apiBase"] = api_base
        normalized["model"] = model
        output.append(normalized)
    return output


def _build_default_provider_candidates(state: Dict[str, Any], desired_model: str) -> List[Dict[str, Any]]:
    providers = state.get("providers") or {}
    candidates: List[Dict[str, Any]] = []

    primary_ref = str(state.get("primaryRef") or "").strip()
    if primary_ref:
        primary_candidate = _resolve_provider_candidate(
            state,
            model_ref=primary_ref,
            desired_model=desired_model,
            source="openclaw:primary",
            strict_model=True,
        )
        if primary_candidate:
            candidates.append(primary_candidate)

    for fallback_ref in state.get("fallbackRefs") or []:
        fallback_candidate = _resolve_provider_candidate(
            state,
            model_ref=str(fallback_ref),
            desired_model=desired_model,
            source="openclaw:fallback",
            strict_model=True,
        )
        if fallback_candidate:
            candidates.append(fallback_candidate)

    for provider_name in state.get("providerOrder") or []:
        provider = providers.get(provider_name)
        if not isinstance(provider, dict):
            continue
        candidate = _candidate_from_provider(
            provider_name,
            provider,
            desired_model=desired_model,
            source="openclaw:provider-pool",
            strict_model=True,
        )
        if candidate:
            candidates.append(candidate)

    return _dedupe_candidates(candidates)


def _build_direct_candidates(
    direct: Dict[str, str],
    provider_candidates: List[Dict[str, Any]],
    *,
    source: str,
    allow_api_key_override: bool = False,
) -> List[Dict[str, Any]]:
    if not any(direct.values()):
        return []

    api_base = _normalize_api_base(str(direct.get("apiBase") or ""))
    api_key = str(direct.get("apiKey") or "").strip()
    model = str(direct.get("model") or "").strip()

    if api_base and api_key:
        return [{
            "apiBase": api_base,
            "apiKey": api_key,
            "model": model or DEFAULT_MODEL,
            "resolvedFrom": source,
        }]

    if not provider_candidates:
        candidate = {
            "apiBase": api_base,
            "apiKey": api_key,
            "model": model or DEFAULT_MODEL,
            "resolvedFrom": source,
        }
        return [candidate] if candidate["apiBase"] and candidate["apiKey"] else []

    hydrated: List[Dict[str, Any]] = []
    for provider_candidate in provider_candidates:
        provider_api_key = _cfg_str(provider_candidate, "apiKey")
        if api_key and not api_base and not allow_api_key_override and provider_api_key and provider_api_key != api_key:
            continue
        candidate = dict(provider_candidate)
        if api_base:
            candidate["apiBase"] = api_base
        if api_key:
            candidate["apiKey"] = api_key
        if model:
            candidate["model"] = model
            provider_ref = _cfg_str(candidate, "providerRef")
            if provider_ref:
                candidate["modelRef"] = f"{provider_ref}/{model}"
        candidate["resolvedFrom"] = f"{source} <- {provider_candidate.get('resolvedFrom')}"
        hydrated.append(candidate)
    return _dedupe_candidates(hydrated)


def resolve_llm_candidates(config: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
    cfg = dict(config or {})
    state = _load_openclaw_state()
    openclaw_env = state.get("env") or {}

    env_direct = {
        "apiBase": _normalize_api_base(
            os.getenv("PAPER_STYLE_REVIEW_LLM_API_BASE")
            or os.getenv("OPENAI_BASE_URL")
            or os.getenv("OPENAI_API_BASE")
            or str(openclaw_env.get("OPENAI_BASE_URL") or openclaw_env.get("OPENAI_API_BASE") or "")
        ),
        "apiKey": (
            os.getenv("PAPER_STYLE_REVIEW_LLM_API_KEY")
            or os.getenv("OPENAI_API_KEY")
            or str(openclaw_env.get("OPENAI_API_KEY") or "")
        ).strip(),
        "model": (os.getenv("PAPER_STYLE_REVIEW_LLM_MODEL") or os.getenv("OPENAI_MODEL") or "").strip(),
    }
    env_model_ref = (
        os.getenv("PAPER_STYLE_REVIEW_LLM_MODEL_REF")
        or os.getenv("PAPER_STYLE_REVIEW_LLM_PROVIDER_MODEL")
        or ""
    ).strip()
    env_provider_ref = (os.getenv("PAPER_STYLE_REVIEW_LLM_PROVIDER") or "").strip()

    explicit = {
        "apiBase": _normalize_api_base(_cfg_str(cfg, "apiBase", "baseUrl")),
        "apiKey": _cfg_str(cfg, "apiKey"),
        "model": _cfg_str(cfg, "model"),
        "modelRef": _cfg_str(cfg, "modelRef", "providerModel"),
        "providerRef": _cfg_str(cfg, "providerRef", "provider"),
    }
    desired_model = explicit["model"]
    if not desired_model and explicit["modelRef"]:
        _, desired_model = _resolve_model_ref(model_ref=explicit["modelRef"])
    if not desired_model:
        desired_model = env_direct["model"]
    if not desired_model and env_model_ref:
        _, desired_model = _resolve_model_ref(model_ref=env_model_ref)
    desired_model = desired_model or DEFAULT_MODEL

    default_provider_candidates = _build_default_provider_candidates(state, desired_model)

    if explicit["modelRef"] or explicit["providerRef"]:
        explicit_provider = _resolve_provider_candidate(
            state,
            model_ref=explicit["modelRef"],
            provider_ref=explicit["providerRef"],
            desired_model=desired_model,
            source="llmConfig:provider",
            strict_model=bool(explicit["modelRef"] or explicit["model"]),
        )
        candidates = [explicit_provider] if explicit_provider else []
        hydrated = _build_direct_candidates(
            {
                "apiBase": explicit["apiBase"],
                "apiKey": explicit["apiKey"],
                "model": explicit["model"],
            },
            candidates,
            source="llmConfig:direct",
            allow_api_key_override=True,
        )
        return _dedupe_candidates(hydrated or candidates)

    explicit_direct_candidates = _build_direct_candidates(
        {
            "apiBase": explicit["apiBase"],
            "apiKey": explicit["apiKey"],
            "model": explicit["model"],
        },
        default_provider_candidates,
        source="llmConfig:direct",
        allow_api_key_override=True,
    )
    if explicit_direct_candidates:
        return explicit_direct_candidates

    env_provider_candidates: List[Dict[str, Any]] = []
    if env_model_ref or env_provider_ref:
        env_provider = _resolve_provider_candidate(
            state,
            model_ref=env_model_ref,
            provider_ref=env_provider_ref,
            desired_model=desired_model,
            source="env:provider",
            strict_model=bool(env_model_ref or env_direct["model"]),
        )
        if env_provider:
            env_provider_candidates.append(env_provider)

    env_direct_candidates = _build_direct_candidates(
        env_direct,
        env_provider_candidates or default_provider_candidates,
        source="env:direct",
        allow_api_key_override=False,
    )
    candidates = env_direct_candidates + env_provider_candidates + default_provider_candidates
    return _dedupe_candidates(candidates)


def resolve_llm_config(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """统一解析 LLM 配置，返回首选候选并挂载 fallback 链。"""
    resolved = dict(config or {})
    candidates = resolve_llm_candidates(config)
    if candidates:
        primary = dict(candidates[0])
        resolved.update({k: v for k, v in primary.items() if v not in (None, "")})
        fallback_chain = [
            {
                "apiBase": item.get("apiBase"),
                "model": item.get("model"),
                "modelRef": item.get("modelRef"),
                "providerRef": item.get("providerRef"),
                "providerApi": item.get("providerApi"),
                "resolvedFrom": item.get("resolvedFrom"),
            }
            for item in candidates[1:]
        ]
        if fallback_chain:
            resolved["fallbackChain"] = fallback_chain
    missing = [key for key in ("apiBase", "apiKey", "model") if not _cfg_str(resolved, key)]
    if missing:
        raise RuntimeError(
            "LLM 配置不完整，缺少："
            + ", ".join(missing)
            + "。请在 llmConfig 中显式提供，或设置 PAPER_STYLE_REVIEW_LLM_* / OPENAI_*，"
            + "或在 ~/.openclaw/openclaw.json 中配置可用 provider。"
        )
    resolved["apiBase"] = _normalize_api_base(_cfg_str(resolved, "apiBase", "baseUrl"))
    if not _cfg_str(resolved, "model"):
        resolved["model"] = DEFAULT_MODEL
    return resolved


def _mask_secret(value: str) -> str:
    text = (value or "").strip()
    if len(text) <= 8:
        return "***" if text else ""
    return f"{text[:4]}***{text[-4:]}"


def summarize_llm_config(config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    resolved = resolve_llm_config(config)
    return {
        "apiBase": resolved.get("apiBase"),
        "apiKeyMasked": _mask_secret(_cfg_str(resolved, "apiKey")),
        "model": resolved.get("model"),
        "modelRef": resolved.get("modelRef"),
        "providerRef": resolved.get("providerRef"),
        "providerApi": resolved.get("providerApi"),
        "resolvedFrom": resolved.get("resolvedFrom"),
        "fallbackChain": [
            {
                "apiBase": item.get("apiBase"),
                "model": item.get("model"),
                "modelRef": item.get("modelRef"),
                "providerRef": item.get("providerRef"),
                "providerApi": item.get("providerApi"),
                "resolvedFrom": item.get("resolvedFrom"),
            }
            for item in resolved.get("fallbackChain", [])
        ],
    }


def _get_client(config: Optional[Dict[str, Any]] = None) -> OpenAI:
    """创建 OpenAI client。"""
    cfg = dict(config or {})
    return OpenAI(
        api_key=cfg.get("apiKey"),
        base_url=cfg.get("apiBase"),
        timeout=_cfg_int(cfg, "timeout", DEFAULT_TIMEOUT),
    )


def _extract_responses_text(resp: Any) -> str:
    text = getattr(resp, "output_text", None)
    if isinstance(text, str) and text.strip():
        return text

    collected: List[str] = []
    for item in getattr(resp, "output", []) or []:
        for content in getattr(item, "content", []) or []:
            part_text = getattr(content, "text", None)
            if isinstance(part_text, str) and part_text:
                collected.append(part_text)
    return "\n".join(collected).strip()


def _use_responses_api(cfg: Dict[str, Any]) -> bool:
    provider_api = _cfg_str(cfg, "providerApi", "api")
    return provider_api in {"openai-responses", "openai-codex-responses"}


def call_llm(
    prompt: str,
    system: str = "",
    config: Optional[Dict[str, Any]] = None,
    temperature: float = 0.1,
    max_tokens: int = 4096,
) -> str:
    """调用 LLM，返回文本响应。"""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    candidates = resolve_llm_candidates(config)
    if not candidates:
        resolve_llm_config(config)
        raise RuntimeError("LLM 配置解析失败，未生成可用候选。")

    last_error: Optional[Exception] = None
    total_candidates = len(candidates)

    for candidate_index, candidate in enumerate(candidates, start=1):
        cfg = dict(config or {})
        cfg.update(candidate)
        model = cfg.get("model", DEFAULT_MODEL)
        client = _get_client(cfg)
        max_retries = _cfg_int(cfg, "maxRetries", MAX_RETRIES)
        retry_delay = _cfg_int(cfg, "retryDelay", RETRY_DELAY)
        use_responses_api = _use_responses_api(cfg)
        provider_hint = _cfg_str(cfg, "modelRef") or _cfg_str(cfg, "providerRef") or model
        source_hint = _cfg_str(cfg, "resolvedFrom")

        for attempt in range(max_retries + 1):
            try:
                if use_responses_api:
                    resp = client.responses.create(
                        model=model,
                        input=messages,
                        max_output_tokens=max_tokens,
                        temperature=temperature,
                    )
                    return _extract_responses_text(resp)

                resp = client.chat.completions.create(
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    max_tokens=max_tokens,
                )
                return resp.choices[0].message.content or ""
            except Exception as e:
                last_error = e
                if attempt < max_retries:
                    print(
                        f"[LLM] retry {attempt+1}/{max_retries} via {provider_hint} ({source_hint}): {e}",
                        file=sys.stderr,
                    )
                    time.sleep(retry_delay)
                    continue
                if candidate_index < total_candidates:
                    print(
                        f"[LLM] candidate {candidate_index}/{total_candidates} failed via {provider_hint} ({source_hint}), switching fallback: {e}",
                        file=sys.stderr,
                    )
                else:
                    print(
                        f"[LLM] failed after exhausting {total_candidates} candidate(s) and {max_retries+1} attempt(s) on final candidate {provider_hint}: {e}",
                        file=sys.stderr,
                    )

    if last_error:
        raise last_error
    raise RuntimeError("LLM 调用失败，未获得任何响应。")


def _repair_json_text(text: str) -> str:
    """尝试修复 LLM 输出的不合法 JSON（主要是未转义的双引号）。"""
    import re
    # 替换中文引号为「」避免冲突
    text = text.replace('\u201c', '「').replace('\u201d', '」')
    text = text.replace('\u2018', '『').replace('\u2019', '』')
    return text


def _salvage_json_array_items(text: str) -> list:
    """从被截断的 JSON 数组文本中尽量抢救已完整闭合的对象。"""
    start = text.find('[')
    if start < 0:
        return []

    items = []
    depth = 0
    obj_start = None
    in_string = False
    escape = False

    for idx in range(start, len(text)):
        ch = text[idx]
        if in_string:
            if escape:
                escape = False
            elif ch == '\\':
                escape = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
            continue

        if ch == '{':
            if depth == 0:
                obj_start = idx
            depth += 1
        elif ch == '}':
            if depth > 0:
                depth -= 1
                if depth == 0 and obj_start is not None:
                    candidate = text[obj_start:idx + 1]
                    try:
                        items.append(json.loads(candidate))
                    except Exception:
                        pass
                    obj_start = None
    return items


def call_llm_json(
    prompt: str,
    system: str = "",
    config: Optional[Dict[str, Any]] = None,
    temperature: float = 0.1,
    max_tokens: int = 4096,
) -> Any:
    """调用 LLM，解析 JSON 响应。"""
    raw = call_llm(prompt, system, config, temperature, max_tokens)
    text = _repair_json_text(raw.strip())
    
    # 方法1: 直接 json.loads
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        pass
    
    # 方法2: 去掉 markdown code fence 后再试
    import re
    # 匹配 ```json ... ``` 或 ``` ... ```
    fence_match = re.search(r'```(?:json)?\s*\n([\s\S]*?)\n\s*```', text)
    if fence_match:
        inner = fence_match.group(1).strip()
        try:
            return json.loads(inner)
        except (json.JSONDecodeError, ValueError):
            pass
    
    # 方法3: 找到第一个 [ 开始、最后一个 ] 结束
    first_bracket = text.find('[')
    last_bracket = text.rfind(']')
    if first_bracket >= 0 and last_bracket > first_bracket:
        candidate = text[first_bracket:last_bracket + 1]
        try:
            return json.loads(candidate)
        except (json.JSONDecodeError, ValueError):
            pass
    
    # 方法4: 找 { } 对象
    first_brace = text.find('{')
    last_brace = text.rfind('}')
    if first_brace >= 0 and last_brace > first_brace:
        candidate = text[first_brace:last_brace + 1]
        try:
            return json.loads(candidate)
        except (json.JSONDecodeError, ValueError):
            pass

    # 方法5: 若数组被截断，尽量抢救前面已经完整闭合的对象
    salvaged_items = _salvage_json_array_items(text)
    if salvaged_items:
        print(f"[LLM] JSON parse salvaged {len(salvaged_items)} item(s) from truncated array.", file=sys.stderr)
        return salvaged_items
    
    print(f"[LLM] JSON parse failed, raw response:\n{raw[:300]}", file=sys.stderr)
    return []


# ---------------------------------------------------------------------------
# refs 风格画像抽取
# ---------------------------------------------------------------------------

STYLE_PROFILE_SYSTEM = (
    "You are a language style analyzer. "
    "Your job is not to summarize topic content but to extract how a paragraph type creates its style. "
    "Work from structure, progression, syntax, diction, evidence anchoring, rhythm, reader model, and rhetorical moves. "
    "Avoid vague adjectives. Every conclusion must say both the style trait and the language action that produces it. "
    "Prefer reusable, transferable mechanisms. If evidence is weak or samples are short or mixed, narrow the claim and lower confidence. "
    "Return JSON only."
)

STYLE_PROFILE_PROMPT = """ParagraphType:{paragraph_type}
RefCount:{ref_count}
SampleCount:{sample_count}
ObservedSectionPatterns:{section_patterns}
MechanismFields:{style_axes}
Task:infer the reusable style mechanics of this paragraph type. Separate expression style from topic.
Method:
1.State each conclusion as trait + language action.
2.Prioritize reusable mechanisms over labels.
3.Use paragraph position and local role as evidence.
4.If samples are short,mixed,or sparse,keep claims narrow and mark uncertainty.
Samples:
{samples}
Return one JSON object:
{{
  "oneLine":"<=30 words",
  "mechanisms":{{
    "logic":"trait + mechanism",
    "density":"trait + mechanism",
    "linking":"trait + mechanism",
    "closure":"trait + mechanism",
    "tone":"trait + mechanism",
    "rhythm":"trait + mechanism",
    "evidence":"trait + mechanism",
    "focus":"trait + mechanism",
    "stance":"trait + mechanism",
    "abstraction":"trait + mechanism",
    "emotion":"trait + mechanism",
    "units":"trait + mechanism",
    "reader":"trait + mechanism",
    "rhetoric":"trait + mechanism",
    "persuasion":"trait + mechanism",
    "markers":"trait + mechanism"
  }},
  "formula":"short expression formula",
  "rules":["5 concrete reusable rules"],
  "signatureTraits":["3 most identifying traits"],
  "confidence":"high|medium|low",
  "confidenceNotes":"what is solid vs what is tentative"
}}
Rules:
-JSON only.
-No markdown.
-Do not use empty labels like rational, sharp, delicate without mechanism.
-Rules must be executable.
-signatureTraits must be the 3 highest-signal features.
-Avoid double quote characters inside string values."""


def extract_style_profile_for_paragraph_type(
    *,
    paragraph_type: str,
    paragraphs: List[Dict[str, Any]],
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if not paragraphs:
        return {}

    cfg = dict(config or {})
    if "styleProfileTimeout" in cfg:
        cfg["timeout"] = cfg["styleProfileTimeout"]
    max_tokens = _cfg_int(cfg, "styleProfileMaxTokens", 1600)

    samples = []
    ref_ids = set()
    section_patterns = []
    for idx, para in enumerate(paragraphs, start=1):
        ref_id = str(para.get("refId") or "").strip()
        ref_label = str(para.get("refLabel") or para.get("refAlias") or ref_id or "unknown").strip()
        ref_ids.add(ref_id or ref_label)
        text = str(para.get("text") or "").strip()
        section_path = str(para.get("sectionPath") or "").strip()
        section_pattern = str(para.get("sectionExpansionPattern") or "").strip()
        paragraph_order = str(para.get("paragraphOrdinalInSection") or "").strip()
        level2_title = str(para.get("level2Title") or "").strip()
        level3_title = str(para.get("level3Title") or "").strip()
        if section_pattern:
            section_patterns.append(section_pattern)
        meta_bits = [f"ref={ref_label}"]
        if section_path:
            meta_bits.append(f"path={section_path}")
        if level2_title:
            meta_bits.append(f"l2={level2_title}")
        if level3_title:
            meta_bits.append(f"l3={level3_title}")
        if paragraph_order:
            meta_bits.append(f"ord={paragraph_order}")
        if section_pattern:
            meta_bits.append(f"pattern={section_pattern}")
        samples.append(f"[{idx}][{'|'.join(meta_bits)}] {text}")

    pattern_counter: Dict[str, int] = {}
    for value in section_patterns:
        pattern_counter[value] = pattern_counter.get(value, 0) + 1
    ordered_patterns = sorted(pattern_counter.items(), key=lambda item: (-item[1], item[0]))
    rendered_patterns = ",".join(f"{name}:{count}" for name, count in ordered_patterns[:6]) or "unknown"

    prompt = STYLE_PROFILE_PROMPT.format(
        paragraph_type=paragraph_type,
        style_axes=build_style_profile_axes_block(),
        ref_count=len([ref for ref in ref_ids if ref]),
        sample_count=len(paragraphs),
        section_patterns=rendered_patterns,
        samples="\n\n".join(samples),
    )
    result = call_llm_json(prompt, STYLE_PROFILE_SYSTEM, cfg, max_tokens=max_tokens)
    return result if isinstance(result, dict) else {}


# ---------------------------------------------------------------------------
# 逻辑通顺检查
# ---------------------------------------------------------------------------

LOGIC_CHECK_SYSTEM = """你是一位严谨的中文学术论文审阅专家。你的任务是逐段检查论文的逻辑通顺性。

你需要检查：
1. 每段内部的论证逻辑是否通顺——因果关系是否成立，推理是否跳步
2. 段落之间的衔接是否自然——上下文是否连贯
3. 论述是否存在漏洞——主张是否有支撑，结论是否有依据
4. 表述是否模糊或自相矛盾

注意：
- 只标注真正有逻辑问题的段落，不要标注正常的段落
- 封面页、声明页、目录等非正文内容不要检查
- "申请学位级别：硕士"这类元数据不是逻辑问题
- 你需要结合上下文理解，不能孤立地看每个段落
- 给出的问题必须具体、可操作，不能泛泛而谈"""

LOGIC_CHECK_PROMPT = """以下是论文的一个章节，请逐段检查逻辑通顺性。

## 参考论文的展开方式（供你对比参照）
{ref_context}

## 待检查的章节内容
章节标题：{chapter_title}

{paragraphs}

---

请以 JSON 数组格式返回发现的逻辑问题（如果没有问题就返回空数组 []）。每个问题包含：
- "paragraphIndex": 段落序号（从1开始）
- "sourceText": 有问题的原文片段（最多50字）
- "problem": 具体的逻辑问题描述（50字以内）
- "suggestion": 修改建议（50字以内）
- "severity": "high" 或 "medium" 或 "low"

补充约束：
- 如果一个 batch 问题很多，只返回最关键、最有代表性的前 8 条
- 保持短句，避免解释性废话

重要：JSON 字符串值里不要使用双引号字符，改用「」或单引号。保持简洁。只返回 JSON。"""


def check_logic_batch(
    chapter_title: str,
    paragraphs: List[Dict[str, str]],
    ref_context: str = "",
    config: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """用 LLM 检查一个章节的逻辑通顺性。
    
    paragraphs: [{"index": 1, "text": "..."}]
    """
    if not paragraphs:
        return []

    cfg = dict(config or {})
    if "logicTimeout" in cfg:
        cfg["timeout"] = cfg["logicTimeout"]
    logic_max_tokens = _cfg_int(cfg, "logicMaxTokens", 1024)

    # 构建段落文本
    para_text = ""
    for p in paragraphs:
        para_text += f"【第{p['index']}段】\n{p['text']}\n\n"

    prompt = LOGIC_CHECK_PROMPT.format(
        ref_context=ref_context or "（无参考上下文）",
        chapter_title=chapter_title,
        paragraphs=para_text,
    )

    result = call_llm_json(prompt, LOGIC_CHECK_SYSTEM, cfg, max_tokens=logic_max_tokens)
    if isinstance(result, list):
        return result
    return []


# ---------------------------------------------------------------------------
# 中文术语规范检查
# ---------------------------------------------------------------------------

TERM_CHECK_SYSTEM = """你是一位中文学术论文的术语审校专家。你的任务是检查论文中的中文表述是否符合学术规范，并特别判断某些词语是否真的属于中文学术论文常用说法。

你需要检查：
1. 是否存在自造词、非标准的中文复合术语（例如把两个概念生造成一个词）
2. 是否存在中文语境下不常见、过生硬、疑似营销化或翻译腔的说法
3. 是否存在口语化表达（论文不应出现的口语体）
4. 中文专有名词/术语是否准确（比如『物联网』是标准用法，『物连网』就是错误）
5. 术语是否前后一致（同一个概念是否用了不同的中文表述）
6. 对类似『资产可视性盲区』『网络资产地图』这类复合表达，要判断：中文论文里是否常见、是否更像行业宣传语、是否需要换成更稳妥的学术说法
7. 是否存在生僻词、罕见复合词、低频中文组合，虽然未必能直接判错，但在中文论文语境里明显需要进一步确认

注意：
- 英文缩写（如 ZMap、DPDK、HTTP、API）本身不算错误，但若脱离中文锚点、首次未解释，也可以提示
- 只标注真正可疑的用词，不要标注正常的学术用语
- 『基于』『通过』『针对』等常见中文介词不算术语问题
- 若你无法百分百确定一个词是否通行，尤其是生僻词、冷门缩合词、疑似翻译直译词，请标为『external_verification_candidate』而不是武断判错
- 给出的问题必须具体，需要指出错在哪里、应该怎么改"""

TERM_CHECK_PROMPT = """以下是论文的一段内容，请检查中文术语是否规范，并判断是否存在中文论文语境下不够稳妥、过生硬、疑似自造词、翻译腔、生僻词或罕见复合词表达。

## 参考论文中的术语使用习惯（供你对照）
{ref_terms_context}

## 待检查的论文内容
{text}

---

请以 JSON 数组格式返回发现的术语问题（如果没有问题就返回空数组 []）。每个问题包含：
- "term": 有问题的术语/用词（尽量只返回词或短语，不要整句）
- "issueType": 取值只能是：variant_usage | weak_chinese_context | coined_term | jargon_like_phrase | abbreviation_without_anchor | external_verification_candidate
- "sourceText": 包含该术语的原文短句（尽量短，最好能精确定位到词附近）
- "problem": 具体问题描述（60字以内）
- "suggestion": 建议的更稳妥写法（40字以内）
- "cnkiSearchHint": 若属于中文语境可疑项、生僻词、罕见复合词或需进一步确认项，给一个适合检索中文论文是否常用的检索词；否则给空字符串
- "severity": "high" 或 "medium" 或 "low"

重要：
- 尽量返回『词/短语级』问题，不要把整段都当作术语问题
- 对生僻词/需确认项，优先返回最小可定位词组，并说明是“需要确认”而不是直接判错
- 如果一个 batch 命中很多问题，只返回最关键、最有代表性的前 6 条
- JSON 字符串值里不要使用双引号字符，改用「」或单引号
- 保持简洁，只返回 JSON。"""


def check_terminology_batch(
    text: str,
    ref_terms_context: str = "",
    config: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """用 LLM 检查一段文本的中文术语规范性。"""
    if not text or len(text.strip()) < 20:
        return []

    cfg = dict(config or {})
    if "termTimeout" in cfg:
        cfg["timeout"] = cfg["termTimeout"]
    term_max_tokens = _cfg_int(cfg, "termMaxTokens", 1024)

    prompt = TERM_CHECK_PROMPT.format(
        ref_terms_context=ref_terms_context or "（无参考术语上下文）",
        text=text,
    )

    result = call_llm_json(prompt, TERM_CHECK_SYSTEM, cfg, max_tokens=term_max_tokens)
    if isinstance(result, list):
        return result
    return []


# ---------------------------------------------------------------------------
# 风格偏离检查
# ---------------------------------------------------------------------------

STYLE_CHECK_SYSTEM = """You are a thesis style reviewer.

Your only task:
- judge one target paragraph only against the given paragraphType style profile;
- if the paragraph clearly deviates, extract all meaningful style problems in this paragraph, then give one integrated optimization direction and one rewritten version;
- if the paragraph basically fits the profile, return no annotation.

Hard rules:
- Use only the provided style-profile facts. Do not import generic writing advice.
- Every reported issue must be grounded in the profile mechanisms, formula, rules, signature traits, or context.
- Report all meaningful paragraph-level style problems, but avoid splitting one problem into trivial duplicates.
- Each issue must be anchored to one exact sentence copied from the target paragraph.
- Rewrite must only reorder, compress, clarify, or rebalance existing information. No new facts.
- Avoid generic remarks. Point to concrete missing, redundant, misordered, or weakly anchored language actions.
- Return JSON only."""

STYLE_CHECK_PROMPT = """ParagraphType:{paragraph_type}
ParagraphLabel:{paragraph_label}
ParagraphDescription:{paragraph_description}
StyleProfile:
{style_profile_payload}
TargetParagraph:
Chapter:{chapter_title}
Text:{paragraph}
PromptVersion:{style_prompt_version}
{style_contract}
Return one JSON object:
{{
  "needsAnnotation": true|false,
  "sourceText": "representative source span or empty",
  "problem": "overall summary of the paragraph's style problems or empty",
  "suggestion": "overall optimization direction for the whole paragraph or empty",
  "rewriteVersion": "revised paragraph or empty",
  "structureAdjustments": ["2-3 concrete edit actions"],
  "issueItems": [
    {{
      "sentenceText": "exact full sentence copied from target paragraph",
      "focusText": "exact smaller phrase inside sentenceText or empty",
      "diffType": "~|+|-",
      "rewriteText": "local revision example for this sentence issue or empty when delete only",
      "sourceText": "problematic source span",
      "problem": "concrete style problem",
      "suggestion": "local fix direction",
      "expectedProfileEvidence": ["1-2 matched style-profile facts"],
      "observedTextEvidence": ["1-2 concrete observations from target text"],
      "missingAnchors": ["missing anchors if any"],
      "violatedSequence": ["broken or skipped sequence steps if any"],
      "hitAvoidPatterns": ["bad patterns if any"],
      "severity": "high|medium|low",
      "deviationType": "logic|density|linking|closure|tone|rhythm|evidence|focus|stance|abstraction|emotion|units|reader|rhetoric|persuasion|markers|formula|general"
    }}
  ],
  "severity": "high|medium|low",
  "deviationType": "multiple|logic|density|linking|closure|tone|rhythm|evidence|focus|stance|abstraction|emotion|units|reader|rhetoric|persuasion|markers|formula|general"
}}
Rules:
- If the paragraph basically fits, return needsAnnotation=false and keep other fields empty or [].
- Prefer profile-grounded issues over surface polish.
- Return every meaningful style issue in issueItems, then summarize them in problem and suggestion.
- sentenceText must be copied exactly from the target paragraph and must uniquely identify where the issue is.
- Prefer sentence-level anchoring; use focusText only when a smaller phrase inside that sentence is the real attachment point.
- diffType means replace, add, or delete for the local sentence-level revision.
- rewriteText must show what to change the local sentence or phrase into; if diffType is +, provide the inserted wording; if diffType is -, rewriteText may be empty.
- Keep all outputs concise.
- Avoid double quote characters inside string values."""


def check_style_deviation_paragraph(
    chapter_title: str,
    paragraph: Dict[str, str],
    style_profile_payload: str = "",
    paragraph_type: str = "",
    paragraph_label: str = "",
    paragraph_description: str = "",
    config: Optional[Dict[str, Any]] = None,
) -> Optional[Dict[str, Any]]:
    """用 LLM 对照参考画像检查单段风格偏离，并返回段落级总结与句子级问题锚点。"""
    if not paragraph:
        return None

    cfg = dict(config or {})
    if "styleTimeout" in cfg:
        cfg["timeout"] = cfg["styleTimeout"]
    style_max_tokens = _cfg_int(cfg, "styleMaxTokens", 1024)

    prompt = STYLE_CHECK_PROMPT.format(
        paragraph_type=paragraph_type or "unknown",
        paragraph_label=paragraph_label or chapter_title,
        paragraph_description=paragraph_description or "n/a",
        style_profile_payload=style_profile_payload or "null",
        chapter_title=chapter_title,
        paragraph=str(paragraph.get("text") or "").strip(),
        style_prompt_version=STYLE_PROMPT_PROFILE_VERSION,
        style_contract=build_style_prompt_contract_block(),
    )

    result = call_llm_json(prompt, STYLE_CHECK_SYSTEM, cfg, max_tokens=style_max_tokens)
    if not isinstance(result, dict):
        return None
    if not bool(result.get("needsAnnotation")):
        return None
    return result


FUSED_REVIEW_SYSTEM = """You are a thesis review engine.

You review one batch of thesis paragraphs for three distinct tasks:
1. terminology and Chinese academic wording,
2. logic and coherence,
3. style deviation against the provided paragraphType style profiles.

Hard rules:
- Return JSON only.
- Use paragraphId exactly as provided.
- Keep task boundaries strict: do not report style problems as terminology, or terminology problems as logic.
- If evidence is weak, do not report the issue.
- sentenceText must be copied exactly from the target paragraph.
- focusText should be a smaller exact span inside sentenceText when possible, otherwise empty.
- style rewriteText must show a local example of what the sentence or phrase should become.
- When you propose suggestion or rewriteText, keep the revised wording grammatically complete; do not leave broken sentence fragments, and preserve a complete subject-predicate structure when the sentence requires one.
- Do not add facts that are not supported by the target paragraph."""


FUSED_REVIEW_PROMPT = """BatchMeta:
{batch_meta}
EnabledChecks:
{enabled_checks}
TermPolicy:
{term_policy}
LogicReference:
{logic_reference}
StyleProfilesByType:
{style_profiles}
Paragraphs:
{paragraphs}

Return one JSON object:
{{
  "batchId": "same as input",
  "terminologyIssues": [
    {{
      "paragraphId": "exact paragraphId",
      "sentenceText": "exact sentence",
      "focusText": "exact smaller span or empty",
      "term": "term or phrase",
      "issueType": "variant_usage|weak_chinese_context|coined_term|jargon_like_phrase|abbreviation_without_anchor|external_verification_candidate",
      "problem": "specific problem",
      "suggestion": "safer wording",
      "severity": "high|medium|low"
    }}
  ],
  "logicIssues": [
    {{
      "paragraphId": "exact paragraphId",
      "relatedParagraphId": "another paragraphId or empty",
      "scope": "paragraph|cross_paragraph",
      "sentenceText": "exact sentence",
      "focusText": "exact smaller span or empty",
      "problem": "logic or coherence problem",
      "suggestion": "fix direction",
      "severity": "high|medium|low"
    }}
  ],
  "styleIssues": [
    {{
      "paragraphId": "exact paragraphId",
      "paragraphType": "exact paragraphType",
      "sentenceText": "exact sentence",
      "focusText": "exact smaller span or empty",
      "sourceText": "exact problematic source span",
      "deviationType": "logic|density|linking|closure|tone|rhythm|evidence|focus|stance|abstraction|emotion|units|reader|rhetoric|persuasion|markers|formula|general",
      "diffType": "~|+|-",
      "problem": "specific style problem",
      "suggestion": "local fix direction",
      "rewriteText": "local revision example or empty when delete-only",
      "severity": "high|medium|low"
    }}
  ]
}}

Rules:
- If a check is disabled, return an empty array for that task.
- Review paragraphs in order and prefer exact anchoring over vague summary.
- Do not duplicate the same observation across multiple tasks.
- For styleIssues, only judge paragraphs whose paragraphType exists in StyleProfilesByType.
- For logicIssues, use relatedParagraphId only when the problem truly depends on another paragraph in this batch.
- If a sentence is hard to understand because the subject, predicate, or object chain is incomplete, you may report it as a logic or style problem based on the primary failure.
- Keep outputs concise and operational.
- Avoid double quote characters inside string values."""


def check_fused_review_batch(
    *,
    batch_meta: Dict[str, Any],
    enabled_checks: Dict[str, bool],
    paragraphs: List[Dict[str, Any]],
    style_profiles_by_type: Dict[str, Any],
    term_policy: Dict[str, Any],
    logic_reference: Dict[str, Any],
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    if not paragraphs:
        return {
            "batchId": str(batch_meta.get("batchId") or ""),
            "terminologyIssues": [],
            "logicIssues": [],
            "styleIssues": [],
        }

    cfg = dict(config or {})
    if "fusedTimeout" in cfg:
        cfg["timeout"] = cfg["fusedTimeout"]
    fused_max_tokens = _cfg_int(cfg, "fusedMaxTokens", 2200)

    prompt = FUSED_REVIEW_PROMPT.format(
        batch_meta=json.dumps(batch_meta, ensure_ascii=False, indent=2),
        enabled_checks=json.dumps(enabled_checks, ensure_ascii=False, indent=2),
        term_policy=json.dumps(term_policy or {}, ensure_ascii=False, indent=2),
        logic_reference=json.dumps(logic_reference or {}, ensure_ascii=False, indent=2),
        style_profiles=json.dumps(style_profiles_by_type or {}, ensure_ascii=False, indent=2),
        paragraphs=json.dumps(paragraphs, ensure_ascii=False, indent=2),
    )
    result = call_llm_json(prompt, FUSED_REVIEW_SYSTEM, cfg, max_tokens=fused_max_tokens)
    if not isinstance(result, dict):
        return {
            "batchId": str(batch_meta.get("batchId") or ""),
            "terminologyIssues": [],
            "logicIssues": [],
            "styleIssues": [],
        }
    result.setdefault("batchId", str(batch_meta.get("batchId") or ""))
    for key in ("terminologyIssues", "logicIssues", "styleIssues"):
        if not isinstance(result.get(key), list):
            result[key] = []
    return result


# ---------------------------------------------------------------------------
# 测试
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Testing LLM client...")
    try:
        resp = call_llm("回复'OK'两个字母", temperature=0)
        print(f"LLM response: {resp}")
        print("✓ LLM client working")
    except Exception as e:
        print(f"✗ LLM client error: {e}")
