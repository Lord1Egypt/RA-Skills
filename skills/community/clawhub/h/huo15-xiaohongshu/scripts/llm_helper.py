"""火一五小红书 — Anthropic SDK 统一封装。

设计目标
========
1. **Prompt Caching** — Allen 教学体系（allen_method.md / ai_speak_patterns.json /
   seasonal_themes.md 共 19KB）作为缓存内容块，5min TTL，命中后 0.1x 成本。
2. **统一模型选择** — 默认 Sonnet 4.6（成本/质量平衡），关键诊断用 Opus 4.7。
3. **Streaming 支持** — critique --watch 实时反馈。
4. **Tool Use** — coach 让 Claude 自主调本地函数。
5. **失败优雅退化** — 没装 anthropic SDK / 没设 API key / 网络故障时静默回退到规则模式。

环境变量
========
- `XHS_LLM_PROVIDER=anthropic` — 启用 LLM 增强
- `ANTHROPIC_API_KEY=...`     — 必填
- `XHS_LLM_MODEL=...`         — 覆盖默认模型
- `XHS_LLM_DEBUG=1`            — 打印 token 用量

只在 LLM 真正需要时延迟 import anthropic — 没装也能跑（脚本回退到规则模式）。
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional


_DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# 统一的默认模型（按场景）
DEFAULT_MODELS = {
    "fast":     "claude-haiku-4-5-20251001",   # 简单分类、批量评分
    "balanced": "claude-sonnet-4-6",           # 教练、诊断、生成
    "deep":     "claude-opus-4-7",             # 关键决策、extended thinking
}


def is_enabled() -> bool:
    """LLM 增强是否被启用。"""
    return os.environ.get("XHS_LLM_PROVIDER", "").lower() == "anthropic" \
        and bool(os.environ.get("ANTHROPIC_API_KEY"))


def _model(tier: str) -> str:
    return os.environ.get("XHS_LLM_MODEL") or DEFAULT_MODELS.get(tier, DEFAULT_MODELS["balanced"])


def _client():
    """延迟 import — 只在调用时尝试。"""
    try:
        from anthropic import Anthropic
        return Anthropic()
    except ImportError:
        return None
    except Exception:
        return None


# =====================================================================
# 缓存内容块构建器
# =====================================================================


_CACHE_FILES = [
    ("allen_method", "data/allen_method.md"),
    ("ai_speak", "data/ai_speak_patterns.json"),
    ("seasonal", "data/seasonal_themes.md"),
    ("title_templates", "data/title_templates.md"),
    ("content_structures", "data/content_structures.md"),
]


def build_allen_system_blocks(include: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """构建带 cache_control 的 system 块列表。

    每次都用同样的内容时，Anthropic 会缓存 5 分钟，下一次命中只付 10% token 成本。

    Args:
        include: 想包含的资产 key 列表；空 = 全部。

    Returns:
        [{"type": "text", "text": "你是...", "cache_control": ...}, ...] — 喂给 system 字段
    """
    blocks: List[Dict[str, Any]] = [{
        "type": "text",
        "text": (
            "你是 huo15-xiaohongshu 创作助手。"
            "你深谙司志远（Allen）的小红书文案体系（三课 + 五技法 + 11 案例 + 范本对照）。"
            "你写文案时遵循：留白 / 不教读者要带读者 / 用人话不用 AI 腔 / 共同记忆而非冷知识 / "
            "用邀请语而非任务指令 / 展示在做的人而非教读者怎么做。"
        ),
    }]

    keep = set(include) if include else None

    for key, rel in _CACHE_FILES:
        if keep is not None and key not in keep:
            continue
        path = _DATA_DIR.parent / rel
        if not path.exists():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        blocks.append({
            "type": "text",
            "text": f"# 资源：{key}\n\n{text}",
        })

    # 最后一块加 cache_control（对前面所有块都生效）
    if len(blocks) > 1:
        blocks[-1]["cache_control"] = {"type": "ephemeral"}

    return blocks


# =====================================================================
# 通用 messages.create 包装
# =====================================================================


def call(
    user_prompt: str,
    *,
    tier: str = "balanced",
    cached_assets: Optional[List[str]] = None,
    extra_system: str = "",
    max_tokens: int = 1500,
    temperature: float = 0.7,
    response_format: str = "text",   # "text" or "json"
) -> Optional[str]:
    """单次 messages.create — 带 prompt caching。失败返回 None。"""
    if not is_enabled():
        return None
    client = _client()
    if client is None:
        return None

    system_blocks = build_allen_system_blocks(cached_assets)
    if extra_system:
        # extra_system 不缓存 — 因为它通常是任务专属
        system_blocks.append({"type": "text", "text": extra_system})

    user = user_prompt
    if response_format == "json":
        user += "\n\n请以 JSON 格式输出（顶层是 object 或 array），不要包裹 markdown 代码块。"

    try:
        resp = client.messages.create(
            model=_model(tier),
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_blocks,
            messages=[{"role": "user", "content": user}],
        )
    except Exception as e:
        if os.environ.get("XHS_LLM_DEBUG"):
            print(f"[llm_helper] call failed: {e}", file=sys.stderr)
        return None

    text = ""
    if resp.content:
        for block in resp.content:
            if getattr(block, "type", None) == "text":
                text += block.text

    if os.environ.get("XHS_LLM_DEBUG"):
        usage = getattr(resp, "usage", None)
        if usage:
            print(f"[llm_helper] tier={tier} "
                  f"input={usage.input_tokens} "
                  f"cache_read={getattr(usage, 'cache_read_input_tokens', 0)} "
                  f"cache_create={getattr(usage, 'cache_creation_input_tokens', 0)} "
                  f"output={usage.output_tokens}",
                  file=sys.stderr)

    return text.strip() if text else None


def call_json(user_prompt: str, **kwargs) -> Optional[Any]:
    """同 call() 但解析为 JSON。"""
    raw = call(user_prompt, response_format="json", **kwargs)
    if not raw:
        return None
    # 容错：去掉 ```json 包裹
    raw = raw.strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw
        if raw.endswith("```"):
            raw = raw[:-3]
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return None


# =====================================================================
# Streaming
# =====================================================================


def stream(
    user_prompt: str,
    *,
    tier: str = "balanced",
    cached_assets: Optional[List[str]] = None,
    extra_system: str = "",
    max_tokens: int = 2000,
    temperature: float = 0.7,
) -> Optional[Iterable[str]]:
    """流式输出。yield 每一段文本片段。失败返回 None。"""
    if not is_enabled():
        return None
    client = _client()
    if client is None:
        return None

    system_blocks = build_allen_system_blocks(cached_assets)
    if extra_system:
        system_blocks.append({"type": "text", "text": extra_system})

    def _gen():
        try:
            with client.messages.stream(
                model=_model(tier),
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_blocks,
                messages=[{"role": "user", "content": user_prompt}],
            ) as s:
                for chunk in s.text_stream:
                    yield chunk
        except Exception as e:
            if os.environ.get("XHS_LLM_DEBUG"):
                print(f"[llm_helper] stream failed: {e}", file=sys.stderr)
            return

    return _gen()


# =====================================================================
# Tool use
# =====================================================================


def call_with_tools(
    user_prompt: str,
    tools: List[Dict[str, Any]],
    tool_handlers: Dict[str, Callable[[Dict[str, Any]], Any]],
    *,
    tier: str = "balanced",
    cached_assets: Optional[List[str]] = None,
    extra_system: str = "",
    max_tokens: int = 2000,
    max_iter: int = 4,
) -> Optional[str]:
    """让 Claude 自主调本地函数。tool_handlers 是 {tool_name: callable(input_dict)}。"""
    if not is_enabled():
        return None
    client = _client()
    if client is None:
        return None

    system_blocks = build_allen_system_blocks(cached_assets)
    if extra_system:
        system_blocks.append({"type": "text", "text": extra_system})

    messages = [{"role": "user", "content": user_prompt}]

    for _ in range(max_iter):
        try:
            resp = client.messages.create(
                model=_model(tier),
                max_tokens=max_tokens,
                system=system_blocks,
                tools=tools,
                messages=messages,
            )
        except Exception as e:
            if os.environ.get("XHS_LLM_DEBUG"):
                print(f"[llm_helper] tool call failed: {e}", file=sys.stderr)
            return None

        if resp.stop_reason != "tool_use":
            # 收尾文本
            text = ""
            for block in resp.content:
                if getattr(block, "type", None) == "text":
                    text += block.text
            return text.strip() if text else None

        # 处理 tool calls
        messages.append({"role": "assistant", "content": resp.content})
        tool_results = []
        for block in resp.content:
            if getattr(block, "type", None) == "tool_use":
                handler = tool_handlers.get(block.name)
                if handler:
                    try:
                        result = handler(block.input)
                    except Exception as e:
                        result = f"Error: {e}"
                else:
                    result = f"Unknown tool: {block.name}"
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": str(result),
                })
        messages.append({"role": "user", "content": tool_results})

    return None
