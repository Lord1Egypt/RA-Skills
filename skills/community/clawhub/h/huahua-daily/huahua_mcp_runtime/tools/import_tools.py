"""import_tools MCP tool implementations."""

import asyncio  # noqa: F401
import os  # noqa: F401
import re  # noqa: F401
from typing import Optional  # noqa: F401

from .binding import bind_runtime
from ..import_contract import (
    ImportReviewItem,
    ImportType,
    SourceKind,
    derive_time_mode,
    normalize_import_review_items,
)

_RUNTIME_DEPENDENCIES = ("_normalize_upload_files", "_post", "_post_files", "_require_token", "_summarize_import_items")
_MISSING = object()

if False:  # pragma: no cover - populated by bind() before tool registration
    _normalize_upload_files = None
    _post = None
    _post_files = None
    _require_token = None
    _summarize_import_items = None


def bind(runtime_globals: dict) -> None:
    bind_runtime(globals(), runtime_globals, _RUNTIME_DEPENDENCIES)


def _normalize_transaction_review_item(
    raw_item: dict,
    *,
    infer_missing_match: bool,
) -> dict:
    if not isinstance(raw_item, dict):
        raise ValueError("交易导入 items 的每一项都必须是对象")
    item = dict(raw_item)
    code = str(item.get("fund_code") or item.get("code") or "").strip()
    if not re.fullmatch(r"\d{6}", code) or code == "000000":
        code = "000000"
    fund_name = str(item.get("fund_name") or item.get("name") or "").strip()
    fund_real_name = str(
        item.get("fund_real_name") or item.get("name") or fund_name
    ).strip()
    raw_matched = item.get("matched", _MISSING)
    if raw_matched is True:
        matched = True
    elif raw_matched is False:
        matched = False
    elif raw_matched is _MISSING and infer_missing_match:
        raise ValueError("交易导入 matched 必须是明确的布尔值")
    else:
        matched = False

    tx_type = str(item.get("type") or "").strip().upper()
    if tx_type not in {"BUY", "SELL"}:
        raise ValueError("交易导入 type 必须是 BUY 或 SELL")
    time_value = str(item.get("time") or "09:00").strip() or "09:00"
    time_mode = derive_time_mode(time_value)

    item.update({
        "type": tx_type,
        "fund_name": fund_name or fund_real_name,
        "fund_code": code,
        "fund_real_name": fund_real_name,
        "matched": bool(matched),
        "date": str(item.get("date") or "").strip(),
        "time": time_value,
        "time_mode": time_mode,
        "amount": item.get("amount"),
        "shares": item.get("shares"),
        "skip": item.get("skip") is True,
        "skip_reason": item.get("skip_reason"),
    })
    return item


async def import_holding_screenshots(
    image_paths: Optional[list[str]] = None,
    images_base64: Optional[list[dict]] = None,
    import_type: str = "HOLDINGS",
) -> dict:
    """
    [已弃用] 识别持仓/自选截图，只为 full profile 旧调用兼容。

    新调用不得把图片转为 Base64；请使用配套 huahua CLI 直接上传用户明确提供的文件。

    Agent 可先对 unmatched / ambiguous 条目做轻确认，然后调用 request_import_review
    把结果发送到 App 现有导入确认页。

    Args:
        image_paths: 已禁用（安全限制），必须改用 images_base64。
        images_base64: 图片对象列表，格式 {filename, mime, base64}。
        import_type: "HOLDINGS"（持仓，默认）或 "WATCHLIST"（自选）。
            自选截图通常显示 6 位基金代码，传 "WATCHLIST" 后端会用专门 prompt
            提取代码并精确匹配，避免名称模糊匹配的误配。
    """
    _require_token()
    normalized_import_type = (import_type or "").strip().upper()
    if normalized_import_type not in {"HOLDINGS", "WATCHLIST"}:
        raise ValueError("import_type 必须是 HOLDINGS 或 WATCHLIST")
    files = _normalize_upload_files(image_paths, images_base64)
    mode = "watchlist" if normalized_import_type == "WATCHLIST" else "holdings"
    raw = await _post_files("/api/import_screenshot", files, form_data={"mode": mode})
    items = raw if isinstance(raw, list) else []
    normalized = []
    for item in items:
        if not isinstance(item, dict):
            continue
        code = item.get("code") or "000000"
        match_quality = item.get("match_quality") or ("exact" if code != "000000" else "none")
        normalized.append({
            **item,
            "match_status": "unmatched" if code == "000000" else match_quality,
            "resolution_required": code == "000000" or match_quality in {"none", "ambiguous"},
            "resolution_reason": "未匹配到基金代码" if code == "000000" else "",
        })
    return {
        "items": normalized,
        "summary": _summarize_import_items(normalized),
        "next_step": "如有未匹配或歧义项，先在对话中轻确认；确认后调用 request_import_review 发送到 App。",
    }


async def import_transaction_screenshots(
    image_paths: Optional[list[str]] = None,
    images_base64: Optional[list[dict]] = None,
) -> dict:
    """
    [已弃用] 识别交易记录截图，只为 full profile 旧调用兼容。

    新调用不得把图片转为 Base64；请使用配套 huahua CLI 直接上传用户明确提供的文件。

    Args:
        image_paths: 已禁用（安全限制），必须改用 images_base64。
        images_base64: 图片对象列表，格式 {filename, mime, base64}。
    """
    _require_token()
    files = _normalize_upload_files(image_paths, images_base64)
    raw = await _post_files("/api/import_transactions", files)
    items = raw if isinstance(raw, list) else []
    normalized = []
    for item in items:
        if not isinstance(item, dict):
            continue
        normalized_item = _normalize_transaction_review_item(
            item,
            infer_missing_match=False,
        )
        matched = normalized_item["matched"]
        reason = ""
        if not matched:
            reason = "未匹配到基金代码"
        elif not normalized_item.get("date"):
            reason = "交易日期缺失"
        elif normalized_item.get("type") == "BUY" and normalized_item.get("amount") is None:
            reason = "买入金额缺失"
        elif normalized_item.get("type") == "SELL" and normalized_item.get("shares") is None:
            reason = "卖出份额缺失"
        normalized.append({
            **normalized_item,
            "match_status": "exact" if matched else "unmatched",
            "resolution_required": bool(reason),
            "resolution_reason": reason,
        })
    return {
        "items": normalized,
        "summary": _summarize_import_items(normalized),
        "next_step": "如有未匹配或日期/金额歧义，先在对话中轻确认；确认后调用 request_import_review 发送到 App。",
    }


async def request_import_review(
    import_type: ImportType,
    items: list[ImportReviewItem],
    source_note: str = "Agent 整理的批量导入",
    client_request_id: str = "",
    source_kind: SourceKind = "text",
) -> dict:
    """
    将 Agent 整理好的结构化结果发送到 App，复用 App 现有批量导入确认页。

    items 可直接来自用户提供的文字、表格或 JSON。本工具不接收图片；本地
    截图应使用 ``huahua import screenshots`` CLI，禁止把 Base64 传入 MCP。

    Args:
        import_type: "HOLDINGS"、"WATCHLIST" 或 "TRANSACTIONS"。
        items: 识别结果数组，最多 300 条。
        source_note: 展示给用户的来源说明。
        client_request_id: 当前用户内幂等 ID；同一导入请求重试时必须复用。
        source_kind: 输入来源，支持 text/table/json/screenshot/file。
    """
    _require_token()
    normalized_type, normalized_items = normalize_import_review_items(import_type, items)
    normalized_source_kind = str(source_kind or "").strip().lower()
    if normalized_source_kind not in {"text", "table", "json", "screenshot", "file"}:
        raise ValueError("source_kind 必须是 text、table、json、screenshot 或 file")
    normalized_source_note = str(source_note or "").strip()
    if not normalized_source_note:
        raise ValueError("source_note 不能为空")
    if len(normalized_source_note) > 500:
        raise ValueError("source_note 不能超过 500 字符")
    normalized_client_request_id = str(client_request_id or "").strip()
    if normalized_client_request_id and not re.fullmatch(r"[A-Za-z0-9:_-]{1,120}", normalized_client_request_id):
        raise ValueError("client_request_id 仅支持 1-120 位字母、数字、冒号、下划线或连字符")
    if normalized_type == "TRANSACTIONS":
        normalized_items = [
            _normalize_transaction_review_item(item, infer_missing_match=True)
            for item in normalized_items
        ]
    request_body = {
        "import_type": normalized_type,
        "source_kind": normalized_source_kind,
        "source_note": normalized_source_note,
        "items": normalized_items,
    }
    if normalized_client_request_id:
        request_body["client_request_id"] = normalized_client_request_id
    result = await _post("/api/agent/import-reviews", request_body)
    return {
        **(result if isinstance(result, dict) else {}),
        "import_type": normalized_type,
        "source_kind": normalized_source_kind,
        "item_count": len(normalized_items),
        "next_step": "请在花花日记 App 中检查并确认；当前尚未写入持仓或交易。",
    }
