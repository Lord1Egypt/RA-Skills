"""Portfolio report and mutation-request MCP tools."""

import json
import math
import re

from .binding import bind_runtime

_RUNTIME_DEPENDENCIES = ("_get", "_post", "_put", "_require_token", "_validate_amount", "_validate_date", "_validate_fund_code")

if False:  # pragma: no cover - populated by bind() before tool registration
    _get = None
    _post = None
    _put = None
    _require_token = None
    _validate_amount = None
    _validate_date = None
    _validate_fund_code = None


def bind(runtime_globals: dict) -> None:
    bind_runtime(globals(), runtime_globals, _RUNTIME_DEPENDENCIES)


async def request_transaction(
    item_code: str,
    item_name: str,
    record_type: str,
    amount: float = 0,
    date: str = "",
    note: str = "",
    group_name: str = "",
    group_id: str = "",
    sell_mode: str = "AMOUNT",
    shares: float = 0,
    client_request_id: str = "",
) -> str:
    """
    向用户的 App 发送一条交易请求信号。
    用户会在 App 中收到提示，点击后打开预填好的交易表单，确认后执行。
    交易逻辑（净值日计算、手续费、PENDING/CONFIRMED 状态）由 App 处理，不会产生数据冲突。

    重要：调用前须向用户确认基金名称和代码无误，尤其是通过搜索推断出来的代码。
    发送后须告知用户"需在 App 中确认才会生效"，不要让用户误以为已执行。

    如用户指定分组，请优先从 get_records 获取稳定的 group_id，同时可填写 group_name 供展示。
    App 只会精确匹配目标分组；匹配失败时弹出分组选择器，不会静默路由到其他持仓。
    重试同一请求时复用 client_request_id，服务端会返回同一条待确认请求，避免重复 Banner。
    已确认的纯场内标的只支持自选和参考估算；服务端会以
    exchange_instrument_watchlist_only 拒绝其买卖请求。

    Args:
        item_code: 项目编号，如 "110022"
        item_name: 项目名称，如 "易方达消费行业"
        record_type: "BUY"（买入）或 "SELL"（卖出）
        amount: 买入金额，或 sell_mode="AMOUNT" 时的卖出总价值；按份额卖出时可为 0
        date: 操作日期 YYYY-MM-DD，留空则由 App 使用今日
        note: 备注说明（可选）
        group_name: 目标分组名称（可选），如 "沪深宽基"
        group_id: get_records 返回的稳定目标分组 ID（推荐）
        sell_mode: 卖出输入模式，"AMOUNT"（金额）或 "SHARES"（份额）；买入时忽略
        shares: sell_mode="SHARES" 时的卖出份额
        client_request_id: 当前用户内幂等 ID；同一逻辑请求重试时必须复用

    Returns:
        str: 发送结果提示
    """
    _require_token()
    tx_type = record_type.upper()
    if tx_type not in ("BUY", "SELL"):
        raise ValueError("record_type 必须是 BUY 或 SELL")

    validated_code = _validate_fund_code(item_code)
    normalized_name = str(item_name or "").strip()
    if not normalized_name:
        raise ValueError("item_name 不能为空")
    if len(normalized_name) > 200:
        raise ValueError("item_name 不能超过 200 字符")
    normalized_note = str(note or "").strip()
    if len(normalized_note) > 1000:
        raise ValueError("note 不能超过 1000 字符")
    validated_date = _validate_date(date)
    normalized_group_name = str(group_name or "").strip()
    normalized_group_id = str(group_id or "").strip()
    if len(normalized_group_name) > 120 or len(normalized_group_id) > 120:
        raise ValueError("group_name 或 group_id 不能超过 120 字符")
    normalized_client_request_id = str(client_request_id or "").strip()
    if normalized_client_request_id and not re.fullmatch(r"[A-Za-z0-9:_-]{1,120}", normalized_client_request_id):
        raise ValueError("client_request_id 仅支持 1-120 位字母、数字、冒号、下划线或连字符")

    payload_dict: dict = {
        "code": validated_code,
        "name": normalized_name,
        "date": validated_date,
        "note": normalized_note,
    }
    if tx_type == "BUY":
        validated_amount = _validate_amount(amount)
        payload_dict["amount"] = validated_amount
    else:
        normalized_sell_mode = str(sell_mode or "AMOUNT").strip().upper()
        if normalized_sell_mode not in {"AMOUNT", "SHARES"}:
            raise ValueError("sell_mode 必须是 AMOUNT 或 SHARES")
        payload_dict["sell_mode"] = normalized_sell_mode
        if normalized_sell_mode == "AMOUNT":
            validated_amount = _validate_amount(amount)
            payload_dict["amount"] = validated_amount
        else:
            if (
                isinstance(shares, bool)
                or not isinstance(shares, (int, float))
                or not math.isfinite(float(shares))
                or float(shares) <= 0
            ):
                raise ValueError("按份额卖出时 shares 必须是大于 0 的数字")
            validated_shares = round(float(shares), 6)
            if validated_shares <= 0:
                raise ValueError("卖出份额精确到 6 位小数后必须至少为 0.000001")
            if validated_shares > 1_000_000_000:
                raise ValueError("卖出份额过大，请确认是否正确")
            payload_dict["shares"] = validated_shares
    if normalized_group_name:
        payload_dict["group_name"] = normalized_group_name
    if normalized_group_id:
        payload_dict["group_id"] = normalized_group_id
    if normalized_client_request_id:
        payload_dict["client_request_id"] = normalized_client_request_id

    payload = json.dumps(payload_dict, ensure_ascii=False)

    request_body = {"action_type": tx_type, "payload": payload}
    if normalized_client_request_id:
        request_body["client_request_id"] = normalized_client_request_id
    await _post("/api/agent/request", request_body)
    action = "买入" if tx_type == "BUY" else "卖出"
    group_label = normalized_group_name or normalized_group_id
    group_hint = f"（分组：{group_label}）" if group_label else ""
    value_hint = (
        f"{payload_dict['shares']:,.6f} 份"
        if tx_type == "SELL" and payload_dict.get("sell_mode") == "SHARES"
        else f"¥{payload_dict['amount']:,.2f}"
    )
    return f"✅ {action}请求已发送：{item_name}（{validated_code}）{value_hint}{group_hint}，请打开 App 确认后生效。"


async def get_agent_requests() -> list:
    """
    获取当前账号仍待处理的 Agent 交易请求。
    主要用于 Agent 自检是否已经重复发送请求；App 端仍是最终确认入口。
    """
    _require_token()
    data = await _get("/api/agent/request")
    return data if isinstance(data, list) else []


async def update_agent_request(request_id: str, status: str) -> dict:
    """
    更新 Agent 交易请求状态。通常由 App 调用；Agent 只应在用户明确要求撤销/忽略时使用。

    Args:
        request_id: get_agent_requests 返回的 id。
        status: 仅支持 "DISMISSED"；"PROCESSED" 必须由 App 在用户确认后设置。
    """
    _require_token()
    normalized_request_id = str(request_id or "").strip()
    if not re.fullmatch(r"[A-Za-z0-9_-]{1,120}", normalized_request_id):
        raise ValueError("request_id 仅支持 1-120 位字母、数字、下划线或连字符")
    normalized = (status or "").strip().upper()
    if normalized != "DISMISSED":
        raise ValueError("MCP 仅支持 DISMISSED；PROCESSED 必须由 App 在用户确认后设置")
    return await _put(f"/api/agent/request/{normalized_request_id}", {"status": normalized})
