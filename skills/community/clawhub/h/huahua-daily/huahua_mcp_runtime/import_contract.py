"""Typed import-review contract shared by the MCP tool and artifact CLI."""

from __future__ import annotations

import math
import re
from datetime import datetime
from typing import Annotated, Any, Literal, cast

from pydantic import BaseModel, ConfigDict, Field, StrictBool


ImportType = Literal["HOLDINGS", "WATCHLIST", "TRANSACTIONS"]
SourceKind = Literal["text", "table", "json", "screenshot", "file"]
IMPORT_REVIEW_SCHEMA_VERSION = "huahua.import-review.v1"
MAX_AGENT_TRANSACTION_AMOUNT = 100_000_000
MAX_AGENT_TRANSACTION_SHARES = 1_000_000_000
StrictFiniteFloat = Annotated[
    float,
    Field(strict=True, allow_inf_nan=False),
]


class ImportReviewItem(BaseModel):
    """Superset schema; ``normalize_import_review_items`` enforces type rules."""

    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, allow_inf_nan=False)

    code: str | None = Field(default=None, pattern=r"^\d{6}$", description="持仓/自选基金代码，6 位数字")
    name: str | None = Field(default=None, max_length=200, description="持仓/自选基金名称")
    amount: StrictFiniteFloat | None = Field(default=None, description="持仓总金额或买入金额")
    total_return: StrictFiniteFloat | None = Field(default=None, description="持仓累计收益金额")
    match_quality: str | None = Field(default=None, max_length=30)
    reference_nav: StrictFiniteFloat | None = None
    reference_nav_date: str | None = Field(default=None, max_length=10)

    type: Literal["BUY", "SELL"] | None = Field(default=None, description="交易方向")
    fund_name: str | None = Field(default=None, max_length=200, description="交易原始基金名称")
    fund_code: str | None = Field(default=None, pattern=r"^\d{6}$", description="交易基金代码，6 位数字")
    fund_real_name: str | None = Field(default=None, max_length=200, description="交易标准基金名称")
    matched: StrictBool | None = Field(default=None, description="基金身份是否已明确匹配")
    date: str | None = Field(default=None, pattern=r"^\d{4}-\d{2}-\d{2}$", description="交易申请日，YYYY-MM-DD")
    time: str | None = Field(default="09:00", pattern=r"^\d{2}:\d{2}$", description="交易时间，HH:MM")
    time_mode: Literal["PRE_MARKET", "POST_MARKET"] | None = None
    shares: StrictFiniteFloat | None = Field(default=None, description="卖出份额")
    skip: StrictBool = False
    skip_reason: str | None = Field(default=None, max_length=500)
    match_status: str | None = Field(default=None, max_length=30)
    resolution_required: StrictBool | None = None
    resolution_reason: str | None = Field(default=None, max_length=500)


def _positive_number(value: Any, *, maximum: float) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(float(value))
        and float(value) > 0
        and float(value) <= maximum
    )


def _valid_code(value: Any) -> bool:
    return bool(re.fullmatch(r"\d{6}", str(value or "").strip())) and str(value).strip() != "000000"


def _valid_date(value: Any) -> bool:
    try:
        datetime.strptime(str(value or ""), "%Y-%m-%d")
        return True
    except ValueError:
        return False


def _valid_time(value: Any) -> bool:
    try:
        datetime.strptime(str(value or "09:00"), "%H:%M")
        return True
    except ValueError:
        return False


def derive_time_mode(time_value: str) -> str:
    try:
        hour = int(str(time_value or "09:00").split(":", 1)[0])
    except (TypeError, ValueError):
        hour = 9
    return "POST_MARKET" if hour >= 15 else "PRE_MARKET"


def _is_explicitly_unmatched(item: dict[str, Any]) -> bool:
    return str(item.get("match_quality") or "").strip().lower() in {
        "none", "unmatched", "ambiguous",
    }


def normalize_import_review_items(import_type: str, items: list[Any]) -> tuple[ImportType, list[dict[str, Any]]]:
    """Validate the public review shape before any HTTP request is sent."""

    normalized_type = str(import_type or "").strip().upper()
    if normalized_type not in {"HOLDINGS", "WATCHLIST", "TRANSACTIONS"}:
        raise ValueError("import_type 必须是 HOLDINGS、WATCHLIST 或 TRANSACTIONS")
    if not isinstance(items, list) or not items:
        raise ValueError("items 不能为空")
    if len(items) > 300:
        raise ValueError("单次导入请求最多 300 条")

    normalized: list[dict[str, Any]] = []
    for index, raw_item in enumerate(items, start=1):
        try:
            candidate = dict(raw_item) if isinstance(raw_item, dict) else raw_item
            if normalized_type == "TRANSACTIONS" and isinstance(candidate, dict):
                candidate.setdefault("fund_code", candidate.get("code"))
                candidate.setdefault("fund_name", candidate.get("name"))
                candidate.setdefault("fund_real_name", candidate.get("name") or candidate.get("fund_name"))
            item = ImportReviewItem.model_validate(candidate).model_dump(exclude_none=True, exclude_unset=True)
        except Exception as exc:
            raise ValueError(f"第 {index} 条导入记录格式无效：{exc}") from None

        if normalized_type == "HOLDINGS":
            if not _valid_code(item.get("code")):
                if str(item.get("code") or "") not in {"", "000000"} or not _is_explicitly_unmatched(item):
                    raise ValueError(f"第 {index} 条持仓缺少有效的 6 位基金代码或未匹配标记")
                item.update(code="000000", match_quality="none")
            if not _positive_number(
                item.get("amount"),
                maximum=MAX_AGENT_TRANSACTION_AMOUNT,
            ):
                raise ValueError(
                    f"第 {index} 条持仓 amount 必须大于 0 且不能超过 "
                    f"{MAX_AGENT_TRANSACTION_AMOUNT:g}"
                )
            total_return = item.get("total_return", 0)
            if not isinstance(total_return, (int, float)) or isinstance(total_return, bool) or not math.isfinite(float(total_return)):
                raise ValueError(f"第 {index} 条持仓 total_return 必须是有限数字")
            if abs(float(total_return)) > MAX_AGENT_TRANSACTION_AMOUNT:
                raise ValueError(
                    f"第 {index} 条持仓 total_return 绝对值不能超过 "
                    f"{MAX_AGENT_TRANSACTION_AMOUNT:g}"
                )
            if float(total_return) >= float(item["amount"]):
                raise ValueError(f"第 {index} 条持仓 total_return 必须小于 amount")
            item.setdefault("total_return", 0.0)
        elif normalized_type == "WATCHLIST":
            if not _valid_code(item.get("code")):
                if str(item.get("code") or "") not in {"", "000000"} or not _is_explicitly_unmatched(item):
                    raise ValueError(f"第 {index} 条自选缺少有效的 6 位基金代码或未匹配标记")
                item.update(code="000000", match_quality="none")
        else:
            if item.get("skip") is True:
                if not str(item.get("skip_reason") or "").strip():
                    raise ValueError(f"第 {index} 条跳过交易必须提供 skip_reason")
                normalized.append(item)
                continue
            if not isinstance(item.get("matched"), bool):
                raise ValueError(f"第 {index} 条交易 matched 必须是明确的布尔值")
            if not str(item.get("fund_name") or "").strip():
                raise ValueError(f"第 {index} 条交易缺少基金名称")
            if item["matched"] is True:
                if not _valid_code(item.get("fund_code")):
                    raise ValueError(f"第 {index} 条已匹配交易缺少有效的 6 位基金代码")
                if not str(item.get("fund_real_name") or "").strip():
                    raise ValueError(f"第 {index} 条已匹配交易缺少标准基金名称")
            elif not _valid_code(item.get("fund_code")):
                item["fund_code"] = "000000"
            if item.get("type") not in {"BUY", "SELL"}:
                raise ValueError(f"第 {index} 条交易 type 必须是 BUY 或 SELL")
            if not _valid_date(item.get("date")):
                raise ValueError(f"第 {index} 条交易 date 必须是有效的 YYYY-MM-DD")
            if not _valid_time(item.get("time")):
                raise ValueError(f"第 {index} 条交易 time 必须是有效的 HH:MM")
            item["time_mode"] = derive_time_mode(str(item.get("time") or "09:00"))
            if item["type"] == "BUY" and not _positive_number(
                item.get("amount"),
                maximum=MAX_AGENT_TRANSACTION_AMOUNT,
            ):
                raise ValueError(
                    f"第 {index} 条买入 amount 必须大于 0 且不能超过 "
                    f"{MAX_AGENT_TRANSACTION_AMOUNT:g}"
                )
            if item["type"] == "SELL" and not _positive_number(
                item.get("shares"),
                maximum=MAX_AGENT_TRANSACTION_SHARES,
            ):
                raise ValueError(
                    f"第 {index} 条卖出 shares 必须大于 0 且不能超过 "
                    f"{MAX_AGENT_TRANSACTION_SHARES:g}"
                )
        normalized.append(item)
    return cast(ImportType, normalized_type), normalized
