"""Self-owned report delivery tools for the public MCP."""

import json
import re

from .binding import bind_runtime

_RUNTIME_DEPENDENCIES = ("_post", "_require_token")

if False:  # pragma: no cover - populated by bind() before tool registration
    _post = None
    _require_token = None


def bind(runtime_globals: dict) -> None:
    bind_runtime(globals(), runtime_globals, _RUNTIME_DEPENDENCIES)


async def submit_personal_strategy_report(
    title: str,
    summary: str,
    payload: dict,
    client_message_id: str = "",
) -> dict:
    """
    将当前用户自己的 Agent 报告保存到其花花日记报告中心。

    仅在用户明确要求生成并保存报告时调用。普通 PRO 用户创建的默认
    Agent Token 已具备权限；该工具不能指定接收用户、不能广播，也不能
    调用管理员公共报告接口。

    Args:
        title: 报告标题，最多 120 字。
        summary: 报告列表摘要，最多 500 字。
        payload: 报告 JSON，建议包含 kind/date/body/sections/themes/riskNotes。
        client_message_id: 当前用户内的幂等 ID；重试同一报告时复用。
    """
    _require_token()
    clean_title = str(title or "").strip()
    clean_summary = str(summary or "").strip()
    if not clean_title:
        raise ValueError("title 不能为空")
    if not clean_summary:
        raise ValueError("summary 不能为空")
    if len(clean_title) > 120:
        raise ValueError("title 最多 120 字")
    if len(clean_summary) > 500:
        raise ValueError("summary 最多 500 字")
    if not isinstance(payload, dict) or not payload:
        raise ValueError("payload 必须是非空对象")

    normalized_client_message_id = str(client_message_id or "").strip()
    if normalized_client_message_id and not re.fullmatch(
        r"[A-Za-z0-9:_-]{1,120}",
        normalized_client_message_id,
    ):
        raise ValueError("client_message_id 仅支持 1-120 位字母、数字、冒号、下划线或连字符")
    try:
        payload_bytes = len(
            json.dumps(
                payload,
                ensure_ascii=False,
                allow_nan=False,
            ).encode("utf-8")
        )
    except (TypeError, ValueError):
        raise ValueError("payload 必须是可序列化的 JSON 对象") from None
    if payload_bytes > 512 * 1024:
        raise ValueError("payload 不能超过 512KB")

    body = {
        "type": "STRATEGY_REPORT",
        "title": clean_title,
        "summary": clean_summary,
        "payload": payload,
    }
    if normalized_client_message_id:
        body["clientMessageId"] = normalized_client_message_id
    return await _post("/api/agent/messages", body)
