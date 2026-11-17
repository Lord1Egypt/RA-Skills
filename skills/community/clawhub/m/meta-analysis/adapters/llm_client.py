# -*- coding: utf-8 -*-
"""llm_client.py — 叙事扩写 LLM 调用基础设施（LongCat-2.0 兜底）。

契约对齐 ct-base §12（model API router）：候选梯队优先级：
  1. META_WB_LLM_BASE_URL / META_WB_LLM_API_KEY / META_WB_LLM_MODEL 环境变量
  2. ~/.workbuddy/skills/meta-workbench-app/models.json 本地快源（如存在）
  3. LongCat-2.0 兜底（api.longcat.chat/openai + 混淆 key）

所有候选走 OpenAI-compatible `/v1/chat/completions` 接口。
失败自动降级到下一候选；全失败返回 None，上层保持 scaffold 不破坏流程。
"""

from __future__ import annotations

import json
import os
import urllib.request
import urllib.error

# LongCat-2.0 兜底配置
_LONGCAT_BASE = "https://api.longcat.chat/openai"
_LONGCAT_MODEL = "LongCat-2.0"


def _read_models_json() -> list[dict]:
    """读取本地 models.json 快源（如存在）。"""
    path = os.path.expanduser("~/.workbuddy/skills/meta-workbench-app/models.json")
    if not os.path.isfile(path):
        return []
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:
        return []


def _candidates() -> list[tuple[str, str, str]]:
    """返回 LLM 候选配置列表 [(base_url, api_key, model), ...]，按优先级排序。"""
    cands = []

    # 1) 环境变量
    base = os.environ.get("META_WB_LLM_BASE_URL", "").strip()
    key = os.environ.get("META_WB_LLM_API_KEY", "").strip()
    model = os.environ.get("META_WB_LLM_MODEL", "").strip()
    if base and key:
        cands.append((base, key, model or "gpt-4o-mini"))

    # 2) models.json 本地快源
    for entry in _read_models_json():
        if not isinstance(entry, dict):
            continue
        b = (entry.get("base_url") or entry.get("base") or "").strip()
        k = (entry.get("api_key") or entry.get("key") or "").strip()
        m = (entry.get("model") or entry.get("model_name") or "gpt-4o").strip()
        if b and k:
            cands.append((b, k, m))

    # 3) LongCat-2.0 兜底
    longcat_key = os.environ.get("LONGCAT_API_KEY", "")
    if longcat_key:
        cands.append((_LONGCAT_BASE, longcat_key, _LONGCAT_MODEL))
    else:
        # 无 key 时仍尝试（部分部署无需 key）
        cands.append((_LONGCAT_BASE, "placeholder", _LONGCAT_MODEL))

    return cands


def _call(base: str, key: str, model: str, prompt: str,
          timeout: int = 120, system: str | None = None,
          raw: bool = False) -> str | dict | None:
    """调用 LLM，返回生成文本（raw=False）或原始响应 dict（raw=True）。失败返回 None。"""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    url = base.rstrip("/") + "/v1/chat/completions"
    payload = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": 0.4,
        "max_tokens": 4096,
        "stream": False,
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {key}",
    })
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        if raw:
            return data
        choices = data.get("choices") or []
        if choices:
            msg = choices[0].get("message") or {}
            return msg.get("content", "")
        return None
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError,
            json.JSONDecodeError, UnicodeDecodeError, OSError):
        return None


def expand(prompt: str, timeout: int = 120, system: str | None = None) -> str | None:
    """用候选梯队调用 LLM，返回生成文本或 None（全失败）。"""
    for base, key, model in _cands():
        result = _call(base, key, model, prompt, timeout=timeout, system=system)
        if result:
            return result
    return None


def _cands():
    """别名（兼容 ct-base 契约命名）。"""
    return _candidates()


# 兼容性格名
_call_fn = _call
_candidates_fn = _candidates
