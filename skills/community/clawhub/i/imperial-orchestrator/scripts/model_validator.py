#!/usr/bin/env python3
"""Imperial Orchestrator · 模型验证器

真正探活每个模型——发送一个最小请求，验证模型是否可用。
不是光发现，而是确认能跑。

用法:
  python3 scripts/model_validator.py \
    --openclaw-config ~/.openclaw/openclaw.json \
    --state-file .imperial_state.json \
    --timeout 15

探活策略:
  1. 从 openclaw.json 读取 provider API 地址和认证信息
  2. 对每个模型发送一个极简 chat completion 请求 ("Hi", max_tokens=5)
  3. 根据响应更新 health 状态
  4. 401/403 → auth_dead, timeout → degraded, 200 → healthy
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from lib import (
    HealthInfo,
    Registry,
    build_initial_state,
    load_json,
    now_ts,
    read_openclaw_config,
    record_failure,
    record_success,
    refresh_group_summaries,
    save_json,
)

# ── Provider API 解析 ─────────────────────────────────────────────────

# 已知 provider 的 chat completion 端点模板
KNOWN_ENDPOINTS = {
    "openai": "/v1/chat/completions",
    "anthropic": "/v1/messages",
}

# OpenAI 兼容的 provider（用 /v1/chat/completions）
OPENAI_COMPATIBLE = {
    "openai", "deepseek", "modelstudio", "qwen", "moonshot", "kimi",
    "minimax", "groq", "together", "fireworks", "openrouter", "siliconflow",
    "ollama", "lmstudio", "localhost", "local", "volcengine", "baichuan",
    "zhipu", "yi", "stepfun",
}


def resolve_api_base(provider_key: str, provider_data: Dict[str, Any]) -> Optional[str]:
    """从 provider 配置中解析 API base URL。"""
    # 直接配置了 baseUrl
    base = provider_data.get("baseUrl") or provider_data.get("base_url") or ""
    if base:
        return base.rstrip("/")

    # 尝试从 api 字段推断
    api = provider_data.get("api", "").lower()
    key_lower = provider_key.lower()

    # 已知平台默认地址
    defaults = {
        "openai": "https://api.openai.com",
        "deepseek": "https://api.deepseek.com",
        "moonshot": "https://api.moonshot.cn",
        "kimi": "https://api.moonshot.cn",
        "minimax": "https://api.minimax.chat",
        "ollama": "http://localhost:11434",
        "lmstudio": "http://localhost:1234",
    }
    for name, url in defaults.items():
        if name in key_lower:
            return url

    return None


def resolve_api_key(provider_key: str, provider_data: Dict[str, Any]) -> Optional[str]:
    """从 provider 配置中解析 API Key。"""
    import os

    # 直接配置了 key
    key = provider_data.get("apiKey") or provider_data.get("api_key") or ""
    if key and not key.startswith("${"):
        return key

    # 环境变量引用格式: ${ENV_VAR} 或 $ENV_VAR
    if key.startswith("${") and key.endswith("}"):
        env_var = key[2:-1]
        return os.environ.get(env_var)
    if key.startswith("$"):
        return os.environ.get(key[1:])

    # 尝试常见环境变量名
    key_lower = provider_key.lower()
    env_candidates = [
        f"{provider_key.upper()}_API_KEY",
        f"{provider_key.upper()}_KEY",
        f"{key_lower.upper().replace('-', '_')}_API_KEY",
    ]
    # 特殊映射
    if "openai" in key_lower:
        env_candidates.insert(0, "OPENAI_API_KEY")
    if "anthropic" in key_lower:
        env_candidates.insert(0, "ANTHROPIC_API_KEY")
    if "deepseek" in key_lower:
        env_candidates.insert(0, "DEEPSEEK_API_KEY")

    for env in env_candidates:
        val = os.environ.get(env)
        if val:
            return val

    return None


def is_local_provider(provider_key: str) -> bool:
    lower = provider_key.lower()
    return any(p in lower for p in ("ollama", "lmstudio", "localhost", "local"))


# ── 探活请求 ──────────────────────────────────────────────────────────

def _http_probe(url: str, payload: bytes, headers: Dict[str, str], timeout: int) -> Tuple[str, Optional[str], float]:
    """通用 HTTP 探活。返回 (status, error, latency_ms)。"""
    req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
    start = time.monotonic()

    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            latency = (time.monotonic() - start) * 1000
            body = json.loads(resp.read())
            # OpenAI 格式: choices; Anthropic 格式: content; Ollama 格式: message
            if body.get("choices") or body.get("content") or body.get("message"):
                return "healthy", None, latency
            return "degraded", "Unexpected response format: no choices/content/message", latency
    except urllib.error.HTTPError as e:
        latency = (time.monotonic() - start) * 1000
        code = e.code
        try:
            raw = e.read()
            parsed = json.loads(raw)
            detail = parsed.get("error", {})
            if isinstance(detail, dict):
                detail = detail.get("message", str(e))
        except Exception:
            detail = str(e)
        if code in (401, 403):
            return "auth_dead", f"HTTP {code}: {detail}", latency
        if code == 429:
            return "rate_limited", f"HTTP 429: {detail}", latency
        return "down", f"HTTP {code}: {detail}", latency
    except urllib.error.URLError as e:
        latency = (time.monotonic() - start) * 1000
        return "down", f"Connection error: {e.reason}", latency
    except TimeoutError:
        latency = (time.monotonic() - start) * 1000
        return "timeout", f"Timeout after {timeout}s", latency
    except Exception as e:
        latency = (time.monotonic() - start) * 1000
        return "down", f"Unexpected: {e}", latency


def _build_endpoint(base_url: str, api_type: str) -> str:
    """根据 API 类型和 base_url 构建完整请求 URL，避免重复拼 /v1。"""
    base = base_url.rstrip("/")

    if api_type == "anthropic-messages":
        # Anthropic: base 通常是 https://api.anthropic.com 或代理
        if base.endswith("/v1"):
            return f"{base}/messages"
        return f"{base}/v1/messages"

    if api_type == "ollama":
        # Ollama 原生 API: http://host:11434/api/chat
        if "/api/" in base:
            return f"{base}/chat"
        return f"{base}/api/chat"

    # OpenAI 兼容格式
    if base.endswith("/v1"):
        return f"{base}/chat/completions"
    return f"{base}/v1/chat/completions"


def probe_model_openai(base_url: str, model_id: str, api_key: Optional[str], timeout: int) -> Tuple[str, Optional[str], float]:
    """OpenAI 兼容格式探活。"""
    url = _build_endpoint(base_url, "openai-completions")
    payload = json.dumps({
        "model": model_id,
        "messages": [{"role": "user", "content": "Hi"}],
        "max_tokens": 5,
        "temperature": 0,
    }).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    return _http_probe(url, payload, headers, timeout)


def probe_model_anthropic(base_url: str, model_id: str, api_key: Optional[str], timeout: int) -> Tuple[str, Optional[str], float]:
    """Anthropic Messages API 格式探活。"""
    url = _build_endpoint(base_url, "anthropic-messages")
    payload = json.dumps({
        "model": model_id,
        "messages": [{"role": "user", "content": "Hi"}],
        "max_tokens": 5,
    }).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }
    if api_key:
        headers["x-api-key"] = api_key
    return _http_probe(url, payload, headers, timeout)


def probe_model_ollama(base_url: str, model_id: str, timeout: int) -> Tuple[str, Optional[str], float]:
    """Ollama 原生 API 格式探活。"""
    url = _build_endpoint(base_url, "ollama")
    payload = json.dumps({
        "model": model_id,
        "messages": [{"role": "user", "content": "Hi"}],
        "stream": False,
        "options": {"num_predict": 5},
    }).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    return _http_probe(url, payload, headers, timeout)


def probe_model(
    provider_key: str,
    provider_data: Dict[str, Any],
    model_id: str,
    timeout: int,
    api_type: str = "",
) -> Tuple[str, Optional[str], float]:
    """根据 provider 的 api 类型选择正确的探活方式。"""
    base_url = resolve_api_base(provider_key, provider_data)
    if not base_url:
        return "down", f"Cannot resolve API base for provider '{provider_key}'", 0

    api_type = api_type or (provider_data.get("api") or "").lower()
    api_key = resolve_api_key(provider_key, provider_data)

    # 本地模型不需要 key
    if not api_key and not is_local_provider(provider_key):
        return "auth_dead", f"No API key found for provider '{provider_key}'", 0

    if api_type == "anthropic-messages":
        return probe_model_anthropic(base_url, model_id, api_key, timeout)
    elif api_type == "ollama":
        return probe_model_ollama(base_url, model_id, timeout)
    else:
        # 默认走 OpenAI 兼容
        return probe_model_openai(base_url, model_id, api_key, timeout)


# ── 主逻辑 ────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="验证所有模型的可用性。")
    p.add_argument("--openclaw-config", type=Path, default=None)
    p.add_argument("--state-file", type=Path, default=Path(".imperial_state.json"))
    p.add_argument("--timeout", type=int, default=15, help="每个模型的探活超时(秒)")
    p.add_argument("--skip-local", action="store_true", help="跳过本地模型探活")
    p.add_argument("--only-provider", type=str, default=None, help="只探活指定 provider")
    p.add_argument("--json", action="store_true", help="输出 JSON 格式")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    reg = Registry(root)

    # 加载或构建 state
    cfg = read_openclaw_config(args.openclaw_config)
    if not cfg:
        print("❌ 找不到 openclaw.json", file=sys.stderr)
        return 1

    if args.state_file.exists():
        state = load_json(args.state_file)
    else:
        state = build_initial_state(reg, cfg)

    providers_cfg = cfg.get("models", {}).get("providers", {})
    models_state = state.get("models", {})
    results: List[Dict[str, Any]] = []

    total = len(models_state)
    healthy = 0
    auth_dead = 0
    down = 0
    timeout_count = 0

    if not args.json:
        print(f"🔍 开始探活 {total} 个模型...\n")

    for model_ref, model_data in sorted(models_state.items()):
        provider_key = model_data.get("provider", "unknown")

        # 过滤
        if args.only_provider and provider_key != args.only_provider:
            continue
        if args.skip_local and model_data.get("local"):
            continue

        model_id = model_ref.split("/", 1)[1] if "/" in model_ref else model_ref
        provider_data = providers_cfg.get(provider_key, {})

        api_type = model_data.get("api_type", "openai-completions")
        status, error, latency = probe_model(provider_key, provider_data, model_id, args.timeout, api_type=api_type)

        # 更新 state
        if status == "healthy":
            record_success(state, model_ref)
            healthy += 1
        elif status == "auth_dead":
            cooldown = int(reg.fail_cfg.get("policies", {}).get("auth_errors", {}).get("cooldown_seconds", 1800))
            record_failure(state, model_ref, "auth", cooldown_seconds=cooldown)
            auth_dead += 1
        elif status == "timeout":
            record_failure(state, model_ref, "timeout")
            timeout_count += 1
        elif status == "rate_limited":
            record_failure(state, model_ref, "rate_limit", cooldown_seconds=120)
            down += 1
        else:
            record_failure(state, model_ref, "server_error", cooldown_seconds=60)
            down += 1

        # 记录延迟到 state
        model_data.setdefault("benchmark", {})["probe_latency_ms"] = round(latency, 1)

        result = {
            "model_ref": model_ref,
            "provider": provider_key,
            "status": status,
            "latency_ms": round(latency, 1),
            "error": error,
        }
        results.append(result)

        if not args.json:
            icon = {"healthy": "✅", "auth_dead": "🔴", "timeout": "⏱️", "rate_limited": "🟡", "down": "❌"}.get(status, "❓")
            lat_str = f"{latency:.0f}ms" if latency else "N/A"
            err_str = f" — {error}" if error else ""
            print(f"  {icon} {model_ref:45s} {status:12s} {lat_str:>8s}{err_str}")

    # 持久化
    refresh_group_summaries(state)
    save_json(args.state_file, state)

    if args.json:
        output = {
            "timestamp": now_ts(),
            "summary": {
                "total": total,
                "healthy": healthy,
                "auth_dead": auth_dead,
                "timeout": timeout_count,
                "down": down,
            },
            "results": results,
        }
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'─' * 60}")
        print(f"📊 探活完成: {healthy}✅  {auth_dead}🔴auth  {timeout_count}⏱️timeout  {down}❌down  / {total} 总计")
        print(f"📄 State 已更新: {args.state_file}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
