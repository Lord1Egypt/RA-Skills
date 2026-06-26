"""
oc_llm_client.py — OpenClaw 标准 LLM 调用客户端（打包分发版）
读取用户自己的 ~/.openclaw/openclaw.json，不硬编码任何供应商/模型/key。
"""
import json, os, re, io, urllib.request, urllib.error
from pathlib import Path

_CONF_PATH = Path.home() / ".openclaw" / "openclaw.json"
_cfg_cache: dict | None = None


def _cfg() -> dict:
    global _cfg_cache
    if _cfg_cache is None:
        _cfg_cache = json.loads(_CONF_PATH.read_text())
    return _cfg_cache


def _expand(val: str, env_vars: dict) -> str:
    """展开 ${VAR_NAME} 形式的占位符"""
    return re.sub(r'\$\{(\w+)\}', lambda m: env_vars.get(m.group(1), ""), val)


def get_default_model_config() -> dict:
    """返回 {'base_url', 'api_key', 'api', 'model_id'}"""
    c = _cfg()
    env_vars = c.get("env", {}).get("vars", {})
    primary = c.get("agents", {}).get("defaults", {}).get("model", {}).get("primary", "")
    if "/" not in primary:
        raise RuntimeError(f"无法解析默认模型: {primary!r}")
    provider_id, model_id = primary.split("/", 1)
    p = c.get("models", {}).get("providers", {}).get(provider_id)
    if not p:
        raise RuntimeError(f"provider '{provider_id}' 未在 openclaw.json 中配置")
    return {
        "base_url": p["baseUrl"].rstrip("/"),
        "api_key": _expand(str(p.get("apiKey", "")), env_vars),
        "api": p.get("api", "openai-completions"),
        "model_id": model_id,
    }


def llm_complete(prompt: str, model_cfg: dict | None = None,
                 max_tokens: int = 2000, system: str | None = None) -> str:
    """
    统一 LLM 调用接口，自动适配 anthropic-messages / openai-completions。
    model_cfg: 若为 None 则使用用户 openclaw.json 的默认模型配置。
    """
    mc = model_cfg or get_default_model_config()
    api = mc["api"]
    if api == "anthropic-messages":
        return _call_anthropic(prompt, mc, max_tokens, system)
    else:
        return _call_openai(prompt, mc, max_tokens, system)


def _call_openai(prompt, mc, max_tokens, system):
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    body = json.dumps({
        "model": mc["model_id"], "messages": messages,
        "max_tokens": max_tokens, "stream": True,
    }).encode()
    req = urllib.request.Request(
        f"{mc['base_url']}/v1/chat/completions", data=body,
        headers={"Content-Type": "application/json",
                 "Authorization": f"Bearer {mc['api_key']}"},
        method="POST",
    )
    chunks = []
    with urllib.request.urlopen(req, timeout=60) as resp:
        for raw in io.TextIOWrapper(resp, encoding="utf-8", errors="replace"):
            line = raw.strip()
            if not line.startswith("data:"):
                continue
            data = line[5:].strip()
            if data == "[DONE]":
                break
            try:
                delta = json.loads(data)["choices"][0]["delta"]
                if c := delta.get("content"):
                    chunks.append(c)
            except Exception:
                pass
    return "".join(chunks)


def _call_anthropic(prompt, mc, max_tokens, system):
    messages = [{"role": "user", "content": prompt}]
    body_dict = {"model": mc["model_id"], "max_tokens": max_tokens, "messages": messages}
    if system:
        body_dict["system"] = system
    body = json.dumps(body_dict).encode()
    req = urllib.request.Request(
        f"{mc['base_url']}/v1/messages", data=body,
        headers={"Content-Type": "application/json",
                 "x-api-key": mc["api_key"],
                 "anthropic-version": "2023-06-01"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        data = json.load(resp)
        return data.get("content", [{}])[0].get("text", "")
