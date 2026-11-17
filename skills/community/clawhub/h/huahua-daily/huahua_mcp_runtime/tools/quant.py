"""quant MCP tool implementations."""

import asyncio  # noqa: F401
import json  # noqa: F401
import math
import os  # noqa: F401
import re  # noqa: F401
import time  # noqa: F401
from typing import Literal, Optional  # noqa: F401

from pydantic import BaseModel, ConfigDict, Field

from .binding import bind_runtime

_RUNTIME_DEPENDENCIES = ("_beijing_date_string", "_get", "_post", "_require_token", "_validate_data_cutoff", "_validate_date", "_validate_fund_code")

QuantBenchmarkCode = Literal[
    "000001", "399001", "399006", "000016", "000300",
    "000688", "000852", "000905", "000510", "899050",
]

if False:  # pragma: no cover - populated by bind() before tool registration
    _beijing_date_string = None
    _get = None
    _post = None
    _require_token = None
    _validate_data_cutoff = None
    _validate_date = None
    _validate_fund_code = None


def bind(runtime_globals: dict) -> None:
    bind_runtime(globals(), runtime_globals, _RUNTIME_DEPENDENCIES)


def _validated_range(start_date: str, end_date: str) -> tuple[str, str]:
    start = _validate_date(start_date)
    end = _validate_date(end_date)
    if start and end and start > end:
        raise ValueError("start_date 不能晚于 end_date")
    return start, end


def _bounded_text(value, name: str, max_length: int, *, required: bool = False) -> str:
    normalized = str(value or "").strip()
    if required and not normalized:
        raise ValueError(f"{name} 不能为空")
    if len(normalized) > max_length:
        raise ValueError(f"{name} 不能超过 {max_length} 字符")
    return normalized


def _positive_id(value, name: str) -> int:
    if isinstance(value, bool):
        raise ValueError(f"{name} 必须是正整数")
    try:
        normalized = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} 必须是正整数") from None
    if normalized <= 0:
        raise ValueError(f"{name} 必须是正整数")
    return normalized


def _rate(value, name: str) -> float:
    if isinstance(value, bool):
        raise ValueError(f"{name} 必须在 0 到 1 之间")
    try:
        normalized = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{name} 必须在 0 到 1 之间") from None
    if not math.isfinite(normalized) or not 0 < normalized <= 1:
        raise ValueError(f"{name} 必须在 0 到 1 之间")
    return normalized


class QuantSnapshotRiskVeto(BaseModel):
    """Risk veto contract exposed in the MCP tool schema."""

    model_config = ConfigDict(extra="allow")
    blocked: bool
    reasons: list[str] = Field(default_factory=list)


class QuantSnapshotFundSignal(BaseModel):
    """Per-fund observation contract exposed in the MCP tool schema."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)
    code: str
    observation: Literal["ADD", "HOLD", "REDUCE", "WATCH", "EXIT"]
    triggers: list[str]
    risk_veto: QuantSnapshotRiskVeto = Field(alias="riskVeto")


async def get_transaction_ledger(
    start_date: str = "",
    end_date: str = "",
    codes: Optional[list[str]] = None,
    transaction_types: Optional[list[str]] = None,
    statuses: Optional[list[str]] = None,
    group_id: str = "",
    cursor: str = "",
    limit: int = 100,
    order: str = "desc",
) -> dict:
    """获取完整交易账本，含金额、份额、费用、净值日与确认日，可分页。永久删除的基金不会出现。"""
    _require_token()
    start_date, end_date = _validated_range(start_date, end_date)
    normalized_group_id = _bounded_text(group_id, "group_id", 120)
    params = {
        "start_date": _validate_date(start_date) or None,
        "end_date": _validate_date(end_date) or None,
        "codes": [_validate_fund_code(code) for code in (codes or [])],
        "types": [str(value) for value in (transaction_types or [])],
        "statuses": [str(value) for value in (statuses or [])],
        "group_ids": [normalized_group_id] if normalized_group_id else [],
        "cursor": cursor or None,
        "limit": min(500, max(1, int(limit))),
        "order": order if order in {"asc", "desc"} else "desc",
    }
    return await _get("/api/portfolio/ledger", params={key: value for key, value in params.items() if value not in (None, [], "")})


async def get_batch_fund_nav_history(
    codes: list[str],
    start_date: str = "",
    end_date: str = "",
    order: str = "asc",
) -> dict:
    """一次获取最多 20 只基金的官方 D 日净值数据库快照。

    freshnessMode=unchecked_db_snapshot 表示未核验当前公布进度；complete 只表示
    请求区间的边界覆盖，不得用它证明“已经更新到最新”。当前量化分析应使用
    get_batch_fund_quant_metrics，由后端核验新鲜度并按需补数。
    """
    _require_token()
    validated = list(dict.fromkeys(_validate_fund_code(code) for code in codes))
    if not validated or len(validated) > 20:
        raise ValueError("codes 需要包含 1-20 个有效基金代码")
    start_date, end_date = _validated_range(start_date, end_date)
    return await _post("/api/funds/nav-history/batch", {
        "codes": validated,
        "start_date": start_date or None,
        "end_date": end_date or None,
        "order": order if order in {"asc", "desc"} else "asc",
    })


async def get_portfolio_nav_history(
    start_date: str = "",
    end_date: str = "",
    benchmark_code: Optional[QuantBenchmarkCode] = "000300",
    group_id: str = "",
) -> dict:
    """获取真实组合的每日收益、单位净值、累计收益和回撤曲线。

    当前区间必须检查 complete 与 navFreshness；navFreshness.retryAfterMs 存在时
    按该间隔有界重试，最多 3 次，仍不完整则不得给出当前量化结论。
    """
    _require_token()
    if not end_date:
        end_date = _beijing_date_string()
    end_date = _validate_date(end_date)
    if not start_date:
        from datetime import datetime, timedelta
        start_date = (datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=365)).strftime("%Y-%m-%d")
    start_date, end_date = _validated_range(start_date, end_date)
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "benchmark_code": _validate_fund_code(benchmark_code) if benchmark_code else None,
        "group_id": _bounded_text(group_id, "group_id", 120) or None,
        "methodology_version": "linked_daily_return_v1",
    }
    return await _get("/api/portfolio/performance", params={key: value for key, value in params.items() if value})


async def get_portfolio_trade_review(
    start_date: str,
    end_date: str,
    benchmark_code: Optional[QuantBenchmarkCode] = "000300",
    group_id: str = "",
) -> dict:
    """获取与 App 策略实验室一致的加减仓复盘和 T1/T7/T20/T60 后续表现。"""
    _require_token()
    start_date, end_date = _validated_range(start_date, end_date)
    params = {
        "start_date": start_date,
        "end_date": end_date,
        "benchmark_code": _validate_fund_code(benchmark_code) if benchmark_code else None,
        "group_id": _bounded_text(group_id, "group_id", 120) or None,
    }
    return await _get("/api/portfolio/trade-review", params={key: value for key, value in params.items() if value})


async def get_quant_strategy_context(
    as_of_date: str = "",
    group_id: str = "",
    mode: Literal["live", "historical"] = "live",
    history_window: str = "1y",
    benchmark_code: QuantBenchmarkCode = "000300",
    view: Literal["compact", "full"] = "compact",
) -> dict:
    """综合投资分析的首选单调用。

    compact 一次返回持仓、市场、基金指标、执行窗口、数据质量与分析就绪状态；
    不要再串行重复取数。若 dataQuality.fundOfficialNavFreshness.retryAfterMs 存在，
    按该间隔有界重试，最多 3 次。
    """
    _require_token()
    if not as_of_date:
        as_of_date = _beijing_date_string()
    if mode not in {"live", "historical"}:
        raise ValueError("mode 仅支持 live/historical")
    if history_window != "1y":
        raise ValueError("history_window 当前统一使用 1y")
    if view not in {"compact", "full"}:
        raise ValueError("view 仅支持 compact/full")
    params = {
        "asOfDate": _validate_date(as_of_date),
        "groupId": _bounded_text(group_id, "group_id", 120) or None,
        "mode": mode,
        "historyWindow": history_window,
        "benchmarkCode": _validate_fund_code(benchmark_code),
        "view": view,
    }
    return await _get(
        "/api/quant/strategy-context",
        params={key: value for key, value in params.items() if value is not None},
    )


async def run_portfolio_backtest(
    funds: list[dict],
    start_date: str,
    end_date: str,
    initial_capital: float = 100000,
    strategy_type: str = "target_rebalance",
    rebalance_frequency: str = "monthly",
    take_profit_rate: float = 0.15,
    stop_loss_rate: float = 0.10,
    reentry_rate: float = 0.05,
    benchmark_code: Optional[QuantBenchmarkCode] = "000300",
    name: str = "Agent 回测",
    client_run_id: str = "",
    group_id: str = "",
    max_series_points: int = 300,
) -> dict:
    """运行固定比例或止盈止损历史回测；不接受代码表达式，重试可复用 client_run_id。"""
    _require_token()
    if not 1 <= len(funds) <= 20:
        raise ValueError("funds 数量必须为 1-20")
    normalized = []
    for fund in funds:
        if not isinstance(fund, dict):
            raise ValueError("funds 每项必须是 {code, weight}")
        raw_weight = fund.get("weight")
        try:
            weight = float(raw_weight)
        except (TypeError, ValueError):
            raise ValueError("funds 每项的 weight 必须在 0 到 1 之间") from None
        if isinstance(raw_weight, bool) or not math.isfinite(weight) or not 0 < weight <= 1:
            raise ValueError("funds 每项的 weight 必须在 0 到 1 之间")
        normalized_fund = {
            "code": _validate_fund_code(fund.get("code")),
            "weight": weight,
        }
        fund_name = str(fund.get("name") or "").strip()
        if fund_name:
            normalized_fund["name"] = fund_name[:120]
        normalized.append(normalized_fund)
    if abs(sum(item["weight"] for item in normalized) - 1) > 0.0001:
        raise ValueError("目标权重之和必须等于 1")
    if rebalance_frequency not in {"none", "daily", "weekly", "monthly", "quarterly"}:
        raise ValueError("rebalance_frequency 仅支持 none/daily/weekly/monthly/quarterly")
    if strategy_type not in {"target_rebalance", "threshold_reentry"}:
        raise ValueError("strategy_type 仅支持 target_rebalance/threshold_reentry")
    raw_initial_capital = initial_capital
    try:
        initial_capital = float(raw_initial_capital)
    except (TypeError, ValueError):
        raise ValueError("initial_capital 必须大于 0 且不超过 10 亿元") from None
    if isinstance(raw_initial_capital, bool) or not math.isfinite(initial_capital) or not 0 < initial_capital <= 1_000_000_000:
        raise ValueError("initial_capital 必须大于 0 且不超过 10 亿元")
    take_profit_rate = _rate(take_profit_rate, "take_profit_rate")
    stop_loss_rate = _rate(stop_loss_rate, "stop_loss_rate")
    reentry_rate = _rate(reentry_rate, "reentry_rate")
    start_date, end_date = _validated_range(start_date, end_date)
    normalized_name = _bounded_text(name, "name", 120, required=True)
    normalized_group_id = _bounded_text(group_id, "group_id", 120)
    if not client_run_id:
        client_run_id = f"mcp-{int(time.time() * 1000)}-{os.urandom(4).hex()}"
    elif not re.fullmatch(r"[A-Za-z0-9:_-]{1,120}", str(client_run_id).strip()):
        raise ValueError("client_run_id 仅支持 1-120 位字母、数字、冒号、下划线或连字符")
    client_run_id = str(client_run_id).strip()
    result = await _post("/api/quant/backtests/run", {
        "client_run_id": client_run_id,
        "name": normalized_name,
        "start_date": start_date,
        "end_date": end_date,
        "initial_capital": initial_capital,
        "funds": normalized,
        "strategy_type": strategy_type,
        "rebalance_frequency": rebalance_frequency,
        "take_profit_rate": take_profit_rate,
        "stop_loss_rate": stop_loss_rate,
        "reentry_rate": reentry_rate,
        "benchmark_code": _validate_fund_code(benchmark_code) if benchmark_code else None,
        "source_group_id": normalized_group_id or None,
        "source_group_name": None,
    })
    series = result.get("series") if isinstance(result, dict) else None
    if isinstance(series, list):
        requested = min(500, max(2, int(max_series_points)))
        original_count = len(series)
        if original_count > requested:
            indexes = sorted({round(index * (original_count - 1) / (requested - 1)) for index in range(requested)})
            result["series"] = [series[index] for index in indexes]
        result["seriesPointCount"] = original_count
        result["seriesTruncated"] = original_count > len(result["series"])
    trades = result.get("trades") if isinstance(result, dict) else None
    if isinstance(trades, list):
        result["tradeCount"] = len(trades)
        result["trades"] = trades[:200]
        result["tradesTruncated"] = len(trades) > 200
    return result


async def get_portfolio_backtest(
    run_id: int,
    trade_offset: int = 0,
    trade_limit: int = 100,
    max_series_points: int = 300,
) -> dict:
    """分页读取已保存回测的走势和交易，供 Agent 审计长周期试算结果。"""
    _require_token()
    result = await _get(f"/api/quant/backtests/{_positive_id(run_id, 'run_id')}")
    if not isinstance(result, dict):
        return result
    series = result.get("series")
    if isinstance(series, list):
        requested = min(500, max(2, int(max_series_points)))
        original_count = len(series)
        if original_count > requested:
            indexes = sorted({round(index * (original_count - 1) / (requested - 1)) for index in range(requested)})
            result["series"] = [series[index] for index in indexes]
        result["seriesPointCount"] = original_count
        result["seriesTruncated"] = original_count > len(result["series"])
    trades = result.get("trades")
    if isinstance(trades, list):
        offset = max(0, int(trade_offset))
        limit = min(200, max(1, int(trade_limit)))
        result["tradeCount"] = len(trades)
        result["trades"] = trades[offset:offset + limit]
        result["tradeOffset"] = offset
        result["nextTradeOffset"] = offset + limit if offset + limit < len(trades) else None
    return result


async def save_quant_snapshot(
    snapshot_key: str,
    snapshot_date: str,
    strategy_id: str,
    data_cutoff_at: str,
    strategy_version: str = "",
    fund_signals: Optional[list[QuantSnapshotFundSignal]] = None,
    market_mode: Optional[dict] = None,
    features: Optional[dict] = None,
    risk: Optional[dict] = None,
    data_quality: Optional[dict] = None,
    group_id: str = "",
) -> dict:
    """幂等归档当天策略观察；每条观察需要 code、observation、triggers 和 riskVeto；不保存建议金额，不创建虚拟账户，也不会交易。"""
    _require_token()
    normalized_snapshot_key = _bounded_text(snapshot_key, "snapshot_key", 160, required=True)
    normalized_strategy_id = _bounded_text(strategy_id, "strategy_id", 120, required=True)
    normalized_strategy_version = _bounded_text(strategy_version, "strategy_version", 80)
    normalized_group_id = _bounded_text(group_id, "group_id", 120)
    if len(fund_signals or []) > 100:
        raise ValueError("fund_signals 单次最多 100 条")
    signals = []
    for signal in fund_signals or []:
        normalized_signal = QuantSnapshotFundSignal.model_validate(signal).model_dump(by_alias=True)
        normalized_signal["code"] = _validate_fund_code(normalized_signal.get("code"))
        signals.append(normalized_signal)
    body = {
        "snapshot_key": normalized_snapshot_key,
        "snapshot_date": _validate_date(snapshot_date),
        "strategy_id": normalized_strategy_id,
        "strategy_version": normalized_strategy_version or None,
        "data_cutoff_at": _validate_data_cutoff(data_cutoff_at),
        "group_id": normalized_group_id or None,
        "signals": signals,
        "market_mode": market_mode or {},
        "features": features or {},
        "risk": risk or {},
        "data_quality": data_quality or {},
        "provenance": {"writer": "huahuadaily_mcp"},
    }
    return await _post("/api/quant/snapshots", body)


async def get_quant_snapshots(
    strategy_id: str = "",
    latest_only: bool = False,
    limit: int = 50,
    cursor: str = "",
    start_date: str = "",
    end_date: str = "",
    snapshot_id: int = 0,
    group_id: str = "",
) -> dict:
    """分页读取不可变信号档案；列表返回摘要，传 snapshot_id 读取完整内容。"""
    _require_token()
    if snapshot_id:
        return await _get(f"/api/quant/snapshots/{_positive_id(snapshot_id, 'snapshot_id')}")
    start_date, end_date = _validated_range(start_date, end_date)
    params = {
        "strategy_id": _bounded_text(strategy_id, "strategy_id", 120) or None,
        "portfolio_type": "actual",
        "cursor": cursor or None,
        "start_date": start_date or None,
        "end_date": end_date or None,
        "group_id": _bounded_text(group_id, "group_id", 120) or None,
    }
    if latest_only:
        if cursor:
            raise ValueError("latest_only=true 时不能同时传 cursor")
        latest_params = {
            key: value for key, value in params.items()
            if key != "cursor" and value is not None
        }
        latest_params["limit"] = 1
        page = await _get("/api/quant/snapshots", params=latest_params)
        items = page.get("items") if isinstance(page, dict) else None
        if not isinstance(items, list) or not items:
            raise ValueError("指定条件下暂无量化信号档案")
        snapshot_id = items[0].get("id") if isinstance(items[0], dict) else None
        if not snapshot_id:
            raise ValueError("最新量化信号档案缺少 id")
        return await _get(f"/api/quant/snapshots/{_positive_id(snapshot_id, 'snapshot_id')}")
    params["limit"] = min(100, max(1, int(limit)))
    return await _get("/api/quant/snapshots", params={key: value for key, value in params.items() if value is not None})


async def get_quant_snapshot_review(
    snapshot_id: int,
    benchmark_code: Optional[QuantBenchmarkCode] = "000300",
) -> dict:
    """读取与 App 一致的不可变信号快照 T1/T7/T20/T60 权威复盘。"""
    _require_token()
    params = {
        "benchmark_code": _validate_fund_code(benchmark_code) if benchmark_code else None,
    }
    return await _get(
        f"/api/quant/snapshots/{_positive_id(snapshot_id, 'snapshot_id')}/review",
        params={key: value for key, value in params.items() if value},
    )
