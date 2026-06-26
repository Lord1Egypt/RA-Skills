"""多模态视觉模型客户端：唯一的"理解"入口。

设计要点：
  - 用 OpenAI 兼容协议，可对接火山方舟 (ARK)、OpenAI、阿里 DashScope、本地 Ollama 等
  - 单页一次调用：图片 + Prompt → 结构化 JSON（schema 见 prompts.py）
  - 指数退避重试，失败抛 VLMError；不在本地做任何 fallback/规则修复
  - 所有日志走 stderr，调用结果返回结构化 dict（不打到 stdout）
"""
from __future__ import annotations

import base64
import json
import os
import re
import sys
import time
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Tuple


# ---------------------------------------------------------------------------
# 配置
# ---------------------------------------------------------------------------

# 各 provider 的默认 base_url
_PROVIDER_DEFAULTS: Dict[str, Tuple[str, str]] = {
    # provider: (default_base_url, default_model)
    "ark":     ("https://ark.cn-beijing.volces.com/api/v3", "doubao-1.5-vision-pro"),
    "openai":  ("",                                          "gpt-4o-mini"),
    "dashscope": ("https://dashscope.aliyuncs.com/compatible-mode/v1", "qwen-vl-max"),
    "ollama":  ("http://localhost:11434/v1",                 "qwen2.5-vl:7b"),
}


@dataclass
class VLMConfig:
    provider: str = "ark"
    model: str = "doubao-1.5-vision-pro"
    base_url: str = ""
    api_key: str = ""
    max_retries: int = 3
    retry_backoff_seconds: Tuple[int, ...] = (1, 2, 4, 8)
    timeout_seconds: int = 90
    response_format_json: bool = True
    temperature: float = 0.0
    # 单页输出 token 上限：财报密集表格 JSON 容易撑爆默认 4k；缺省抬到 32k
    # (建设银行季报实测：合并资产负债表单页 ~110 cells → JSON ~12k chars，16k 仍偶发截断)
    max_output_tokens: int = 32768


def vlm_config_from_env() -> Optional[VLMConfig]:
    """从环境变量构造 VLMConfig；密钥缺失返回 None。

    解析优先级（决定 provider 和默认 base_url/model）：
      1) VLM_PROVIDER 显式指定
      2) ARK_API_KEY 存在 → ark
      3) DASHSCOPE_API_KEY 存在 → dashscope
      4) OPENAI_API_KEY 存在 → openai
      5) 都缺 → None
    """
    explicit_provider = os.environ.get("VLM_PROVIDER", "").strip().lower() or None
    api_key = ""
    provider = "openai"

    if explicit_provider and explicit_provider in _PROVIDER_DEFAULTS:
        provider = explicit_provider
        key_env = {
            "ark": "ARK_API_KEY",
            "openai": "OPENAI_API_KEY",
            "dashscope": "DASHSCOPE_API_KEY",
            "ollama": "OLLAMA_API_KEY",  # 通常 ollama 不需要 key
        }[provider]
        api_key = os.environ.get(key_env, "")
        # ollama 允许无 key
        if provider == "ollama" and not api_key:
            api_key = "ollama"
    elif os.environ.get("ARK_API_KEY"):
        provider, api_key = "ark", os.environ["ARK_API_KEY"]
    elif os.environ.get("DASHSCOPE_API_KEY"):
        provider, api_key = "dashscope", os.environ["DASHSCOPE_API_KEY"]
    elif os.environ.get("OPENAI_API_KEY"):
        provider, api_key = "openai", os.environ["OPENAI_API_KEY"]

    if not api_key:
        return None

    default_base, default_model = _PROVIDER_DEFAULTS[provider]
    base_url = (
        os.environ.get("VLM_BASE_URL")
        or os.environ.get(f"{provider.upper()}_BASE_URL")
        or default_base
    )
    model = os.environ.get("VLM_MODEL") or default_model
    return VLMConfig(
        provider=provider,
        model=model,
        base_url=base_url,
        api_key=api_key,
        max_retries=int(os.environ.get("VLM_MAX_RETRIES", "3")),
        timeout_seconds=int(os.environ.get("VLM_TIMEOUT_SECONDS", "90")),
        max_output_tokens=int(os.environ.get("VLM_MAX_OUTPUT_TOKENS", "32768")),
    )


class VLMError(RuntimeError):
    """所有 VLM 调用失败的统一异常。"""


# ---------------------------------------------------------------------------
# JSON 响应解析
# ---------------------------------------------------------------------------

_CODE_FENCE = re.compile(r"```(?:json)?\s*(.*?)```\s*$", re.DOTALL)


def _strip_code_fence(s: str) -> str:
    s = s.strip()
    m = _CODE_FENCE.match(s)
    return m.group(1).strip() if m else s


def _try_extract_json(s: str) -> Any:
    """尽力把模型返回拆成 JSON。失败抛 VLMError。"""
    s = _strip_code_fence(s)
    try:
        return json.loads(s)
    except json.JSONDecodeError:
        # 兜底：从首个 { 到最后一个 } 之间取片段
        l, r = s.find("{"), s.rfind("}")
        if l >= 0 and r > l:
            try:
                return json.loads(s[l:r + 1])
            except json.JSONDecodeError:
                pass
    raise VLMError(f"模型返回非 JSON，head={s[:200]!r}")


# ---------------------------------------------------------------------------
# 调用
# ---------------------------------------------------------------------------

def _log(msg: str) -> None:
    print(msg, file=sys.stderr)


def _build_messages(image_bytes: bytes, prompt: str) -> list[dict]:
    b64 = base64.b64encode(image_bytes).decode("ascii")
    return [{
        "role": "user",
        "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {
                "url": f"data:image/png;base64,{b64}"
            }},
        ],
    }]


def _call_chat_completions(cfg: VLMConfig, messages: list[dict]) -> str:
    """走 OpenAI 兼容 chat/completions；返回 message.content。

    若启用 response_format=json_object 但模型不支持（首次调用收到 400 含
    'response_format'），自动剥掉该参数重试一次，并 in-place 关闭 cfg 上的
    `response_format_json`，避免同一会话后续每页都踩同一坑。
    """
    try:
        from openai import OpenAI, BadRequestError
    except ImportError as e:
        raise VLMError(f"openai SDK 未安装: {e}")

    client = OpenAI(
        api_key=cfg.api_key,
        base_url=cfg.base_url or None,
        timeout=cfg.timeout_seconds,
    )
    kwargs: Dict[str, Any] = {
        "model": cfg.model,
        "messages": messages,
        "temperature": cfg.temperature,
        "max_tokens": cfg.max_output_tokens,
    }
    if cfg.response_format_json:
        kwargs["response_format"] = {"type": "json_object"}

    try:
        resp = client.chat.completions.create(**kwargs)
    except BadRequestError as e:
        # 模型不支持 response_format=json_object → 剥掉再试一次并永久关闭
        msg = str(e)
        if "response_format" in msg and "response_format" in kwargs:
            _log(f"[vlm] 模型 {cfg.model} 不支持 response_format=json_object，"
                 f"剥掉后重试并关闭该选项")
            cfg.response_format_json = False
            kwargs.pop("response_format", None)
            resp = client.chat.completions.create(**kwargs)
        else:
            raise

    choice = resp.choices[0]
    finish = getattr(choice, "finish_reason", None)
    if finish == "length":
        # 截断了——后续 JSON 解析必然失败。提前抛带提示的错，便于上层决策（升 max_tokens / 拆页）
        raise VLMError(
            f"响应被截断（finish_reason=length，max_tokens={cfg.max_output_tokens}）"
            f"——该页内容超过当前输出上限，请提高 VLM_MAX_OUTPUT_TOKENS 或减小单页范围"
        )
    return choice.message.content or ""


def _is_retryable(e: Exception) -> bool:
    """只对网络/超时/限流/5xx 重试；4xx（鉴权失败、参数错误）和"已截断" 立即抛。"""
    # 截断错误是确定性的，重试也是浪费——立即冒上去让用户提高 max_tokens
    if isinstance(e, VLMError) and "finish_reason=length" in str(e):
        return False
    try:
        from openai import (
            APIConnectionError, APITimeoutError, RateLimitError,
            InternalServerError,
        )
    except ImportError:
        return False
    if isinstance(e, (APIConnectionError, APITimeoutError, RateLimitError,
                      InternalServerError)):
        return True
    # 兜底：未明确分类的 APIStatusError → 看 status_code
    status = getattr(e, "status_code", None) or getattr(
        getattr(e, "response", None), "status_code", None)
    if status is None:
        return False
    return status in (408, 425, 429, 500, 502, 503, 504)


def _call_with_retry(cfg: VLMConfig, messages: list[dict]) -> str:
    last_err: Optional[Exception] = None
    for attempt in range(cfg.max_retries):
        try:
            return _call_chat_completions(cfg, messages)
        except Exception as e:
            last_err = e
            if not _is_retryable(e):
                # 4xx / 参数错误 / 鉴权失败 → 快速失败
                raise VLMError(
                    f"VLM 调用失败（不可重试 {type(e).__name__}）: {e}"
                ) from e
            if attempt < cfg.max_retries - 1:
                delay = cfg.retry_backoff_seconds[
                    min(attempt, len(cfg.retry_backoff_seconds) - 1)
                ]
                _log(f"[vlm] 调用失败({type(e).__name__}: {e}), {delay}s 后重试 "
                     f"({attempt + 1}/{cfg.max_retries})")
                time.sleep(delay)
    raise VLMError(f"VLM 调用失败({cfg.max_retries} 次): {last_err}")


# ---------------------------------------------------------------------------
# 对外：单页解析
# ---------------------------------------------------------------------------

_REPAIR_PROMPT = """你是一个金融数值规整器。我会给你一份 JSON 数组，每个元素是表格中的一个单元格，包含其位置和原文：

[{"id": <int>, "text": "原文"}, ...]

请仅依据 text 字段判断该单元格的数值与单位，输出严格 JSON 对象：
{"<id>": {"value": <number> 或 null, "unit": <"yuan"|"wan_yuan"|"yi_yuan"|"million_yuan"|"percent"|"usd"|null>}, ...}

规则：
1. 千分位分隔符去掉："1,234,567.89" → 1234567.89
2. 括号代表负数："(1,234)" → -1234
3. 百分比："12.5%" → value=12.5, unit="percent"
4. **中文方向词决定正负**（关键）：
   - 含"下降/减少/降低/亏损/下滑/缩减"等 → 取负值。如"下降0.57个百分点" → value=-0.57, unit="percent"
   - 含"增长/上升/提高/上涨/扩大/盈利"等 → 取正值。如"增长3.29%" → value=3.29, unit="percent"
   - 仅数字无方向词时按字面值（数字本身可能已含负号或括号）
5. 纯标签/日期/描述文本（无数字 或 数字仅作年月日的一部分）→ value=null
6. 单位以下游已知上下文为准；若无法判断 → unit=null（重要：不要乱猜）
7. "-"、"—"、"不适用"、空白 → value=null

只输出 JSON 对象，不要任何代码块、解释或多余文字。"""


def repair_cells_via_vlm(
    *,
    cells: list[Dict[str, Any]],
    cfg: VLMConfig,
) -> Dict[int, Dict[str, Any]]:
    """二次精修：纯文本调用，把 (id, text) 批量映射为 (value, unit)。

    Args:
        cells: list of {"id": int, "text": str}
        cfg: 复用主调用的配置（同模型同 key）

    Returns:
        {id: {"value": ..., "unit": ...}}；模型未返回某 id 时缺省为 {"value": None, "unit": None}
    """
    if not cells:
        return {}
    payload = json.dumps(cells, ensure_ascii=False)
    user_msg = [{
        "role": "user",
        "content": [
            {"type": "text", "text": _REPAIR_PROMPT + "\n\n输入：\n" + payload},
        ],
    }]
    raw = _call_with_retry(cfg, user_msg)
    try:
        obj = _try_extract_json(raw)
    except VLMError as e:
        _log(f"[repair] 解析失败，跳过：{e}")
        return {}
    if not isinstance(obj, dict):
        return {}
    out: Dict[int, Dict[str, Any]] = {}
    for k, v in obj.items():
        try:
            cid = int(k)
        except (TypeError, ValueError):
            continue
        if isinstance(v, dict):
            out[cid] = {
                "value": v.get("value"),
                "unit": v.get("unit"),
            }
    return out


def parse_page_via_vlm(
    *,
    image_bytes: bytes,
    prompt: str,
    cfg: VLMConfig,
    page_no: int,
) -> Dict[str, Any]:
    """单页 → 调模型 → 解析结构化 JSON。

    返回的 dict 至少包含：
      - page_no: int
      - markdown: str                 该页的 Markdown
      - blocks: list[dict]            (可选) 文本块
      - tables: list[dict]            (可选) 表格 (rows 二维数组形式)
      - engine: str                   "vlm-{provider}-{mode 隐含在 prompt 里}"
      - confidence: float | None      模型自评（若 prompt 要求）
      - raw: str                      原始响应内容（便于排查）
    """
    messages = _build_messages(image_bytes, prompt)
    raw = _call_with_retry(cfg, messages)
    try:
        data = _try_extract_json(raw)
    except VLMError:
        raise

    if not isinstance(data, dict):
        raise VLMError(f"模型返回顶层不是 object: {type(data).__name__}")

    # 把 page_no 强制覆盖（模型有时会瞎填）
    data["page_no"] = page_no
    data.setdefault("markdown", "")
    data.setdefault("blocks", [])
    data.setdefault("tables", [])
    data.setdefault("engine", f"vlm-{cfg.provider}")
    data.setdefault("confidence", None)
    data["_raw_head"] = raw[:500]  # 截断保留便于排查
    return data
