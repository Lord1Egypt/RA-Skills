"""Portfolio MCP tool implementations."""

import json

from .binding import RuntimeCallable, bind_runtime
from . import portfolio_preferences
from .fund_estimate_helpers import estimate_audit_payload as _estimate_audit_payload
from .portfolio_preferences import (
    auto_invest_plans as _auto_invest_plans,
    fund_disciplines as _fund_disciplines,
    get_auto_invest_plans,
    get_fund_disciplines,
    get_night_watchlist,
    get_portfolio_preferences,
    get_purchase_limit_watchlist,
)
__all__ = (
    "get_auto_invest_plans",
    "get_fund_disciplines",
    "get_night_watchlist",
    "get_portfolio_preferences",
    "get_purchase_limit_watchlist",
)

_RUNTIME_DEPENDENCIES = ("_calc_fund_stats", "_download_portfolio", "_download_portfolio_raw", "_fetch_estimates", "_get", "_is_valid_fund_code_value", "_normalize_data_source_mode", "_r2", "_ratio_pct", "_require_token", "_to_float", "_unwrap_sync_payload", "_validate_fund_code")
if False:  # pragma: no cover - populated by bind() before tool registration
    _calc_fund_stats = None
    _download_portfolio = None
    _download_portfolio_raw = None
    _fetch_estimates = None
    _get = None
    _is_valid_fund_code_value = None
    _normalize_data_source_mode = None
    _r2 = None
    _ratio_pct = None
    _require_token = None
    _to_float = None
    _unwrap_sync_payload = None
    _validate_fund_code = None
    _runtime_get_records = None


def bind(runtime_globals: dict) -> None:
    bind_runtime(globals(), runtime_globals, _RUNTIME_DEPENDENCIES)
    portfolio_preferences.bind(runtime_globals)
    globals()["_runtime_get_records"] = RuntimeCallable(runtime_globals, "get_records")


async def get_sync_meta() -> dict:
    """
    获取云端实时同步主数据元信息，不下载完整数据。
    返回 updated_at、etag、size_bytes 和历史快照摘要，用于判断 App 数据是否已经同步到云端。
    """
    _require_token()
    meta = await _get("/api/sync/v3/meta")
    if isinstance(meta, dict):
        restorable_count = int(meta.get("restorable_fund_count") or 0)
        empty_confirmed = meta.get("empty_portfolio_confirmed") is True
        has_empty_tombstone = (
            empty_confirmed
            and meta.get("has_funds_array") is True
            and int(meta.get("fund_count") or 0) == 0
        )
        meta["has_restorable_sync_payload"] = restorable_count > 0 or has_empty_tombstone
        meta["data_source"] = "portfolio_v3"
        meta["portfolio_updated_at"] = meta.get("updated_at", "")
        meta["freshness_field"] = "portfolio_updated_at"
        meta["sync_cursor"] = {
            "protocol_version": meta.get("protocol_version"),
            "sync_epoch": meta.get("sync_epoch"),
            "change_version": meta.get("change_version"),
        }
    return meta


async def get_raw_sync_data(include_json_text: bool = False) -> dict:
    """
    获取完整云端实时同步主数据的兼容投影。默认返回结构化组合投影；只有
    include_json_text=true 时才额外返回底层接口原始 JSON 字符串。

    实时同步主数据包含 funds、groups、watchlistGroups、globalTags、字段显示配置、
    nightWatchCodes、purchaseLimitWatchItems、marketIndexSelection 等。
    profit ledger 是 App 可由交易记录和历史净值重建的派生数据；当前主数据通常不包含 ledger。

    Args:
        include_json_text: 是否同时返回服务端原始 json_data 字符串；只有做导出/迁移审计时才建议开启。
            开启时该调用绕过会话缓存并重新下载完整原始数据。
    """
    _require_token()
    if include_json_text:
        raw, source = await _download_portfolio_raw()
        parsed = _unwrap_sync_payload(raw if isinstance(raw, dict) else {}, source=source)
        json_text = json.dumps(raw, ensure_ascii=False) if isinstance(raw, dict) else ""
    else:
        parsed = await _download_portfolio()
        source = parsed.get("_meta_data_source", "portfolio_v3")
        json_text = ""
    result = {
        "data": {k: v for k, v in parsed.items() if not k.startswith("_meta_")},
        "meta": {
            "updated_at": parsed.get("_meta_updated_at", ""),
            "portfolio_updated_at": parsed.get("_meta_updated_at", ""),
            "payload_timestamp": parsed.get("timestamp"),
            "payload_timestamp_semantics": (
                "客户端快照谱系/迁移元数据，不表示云端持仓新鲜度；"
                "新鲜度只看 portfolio_updated_at"
            ),
            "etag": parsed.get("_meta_etag", ""),
            "data_source": parsed.get("_meta_data_source", source),
            "size_bytes": parsed.get("_meta_size_bytes", 0),
            "contains_ledger": "ledger" in parsed,
            "contains_archived_ledger": "archivedLedger" in parsed,
            **parsed.get("_meta_summary", {}),
        },
    }
    if include_json_text:
        result["json_data"] = json_text
    return result


async def get_transactions(code: str = "", include_pending: bool = True) -> dict:
    """
    获取云端实时同步主数据中的交易流水。默认返回全部基金；传入 code 时只返回该基金。

    Args:
        code: 可选，6 位基金代码。
        include_pending: 是否包含待确认交易。
    """
    _require_token()
    # 验证基金代码（如果提供）
    validated_code = ""
    if code:
        validated_code = _validate_fund_code(code)
    portfolio = await _download_portfolio()
    funds = portfolio.get("funds", [])
    items = []
    for fund in funds:
        if validated_code and str(fund.get("code", "")) != validated_code:
            continue
        txs = fund.get("transactions") or []
        if not include_pending:
            txs = [tx for tx in txs if tx.get("status") == "CONFIRMED"]
        items.append({
            "code": fund.get("code", ""),
            "name": fund.get("name", ""),
            "groupId": fund.get("groupId", ""),
            "transactions": txs,
        })
    return {
        "items": items,
        "portfolioUpdatedAt": portfolio.get("_meta_updated_at", ""),
    }


async def get_groups() -> dict:
    """
    获取持仓分组和自选分组。
    """
    _require_token()
    portfolio = await _download_portfolio()
    return {
        "groups": portfolio.get("groups", []),
        "watchlistGroups": portfolio.get("watchlistGroups", []),
        "portfolioUpdatedAt": portfolio.get("_meta_updated_at", ""),
    }


async def get_tags() -> dict:
    """
    获取全局标签注册表，以及每只基金绑定的标签。
    """
    _require_token()
    portfolio = await _download_portfolio()
    funds = portfolio.get("funds", [])
    return {
        "globalTags": portfolio.get("globalTags", []),
        "fundTags": [
            {
                "code": fund.get("code", ""),
                "name": fund.get("name", ""),
                "tags": fund.get("tags", []),
                "visibleTags": fund.get("visibleTags", []),
            }
            for fund in funds
        ],
        "portfolioUpdatedAt": portfolio.get("_meta_updated_at", ""),
    }


async def get_records(include_transactions: bool = False) -> dict:
    """
    获取用户持仓记录，并自动计算今日收益、持有收益、累计收益、市值、持有收益率等字段。
    需要 Agent Token 且账号需开通会员才能使用云端实时同步数据。

    数据来自 PowerSync v3 云端实时同步主数据（portfolioUpdatedAt）。若刚在 App 中刷新了净值或新增了交易，
    请先确认 App 实时同步已完成后再查询，以获取最新数据。

    返回结构：
    - holdings: 有持仓的记录列表（含实时收益计算、autoInvestPlans 和 disciplines）
    - watchlist: App 中可见的观察列记录（排除已送养隐藏项；含盘中估算
      estimatedNav/estimatedChangePercent；有配置时包含 autoInvestPlans 和 disciplines）
    - summary: 持仓汇总（总市值/今日收益/持有收益/持有收益率/累计收益/在途金额）
      - todayProfitRate: 今日/昨日收益率（todayProfit / totalDayBaseMarketValue × 100%，分母为归属日组合期初市值）
      - totalDayBaseMarketValue: 今日/昨日收益率使用的组合期初市值
      - totalHoldingProfit: 持有收益总额（市值 - 成本，不含落袋/已实现收益）
      - totalHoldingReturnRate: 持有收益率（totalHoldingProfit / totalCost × 100%，仅反映浮动亏盈）
      - cumulativeProfit: 累计收益（持有收益 + 已实现收益，含落袋；不代表用户所有平台/历史交易的完整累计）
    - portfolioUpdatedAt: 云端实时同步主数据的最后更新时间（UTC）
    - summary.valuationCompleteness: 官方市值完整度；freshenedCodes 表示使用行情接口中
      比组合快照更新的官方净值锚点修正估值
    - holdings[].valuationNavDate/valuationSource: 官方市值采用的净值日期和来源；
      estimatedMarketValue 是独立盘中估算，不进入 marketValue
    - strategyPreferences.maxDrawdownLimitPct: 用户设置的组合回撤阈值百分数；0 表示未启用
    - summary.estimateCompleteness: 当前估值帧可用性。complete=false 表示至少一只持仓
      没有可用于当日收益的估值帧；timeoutCount>0 或 staleCount>0 时不得把 0 元
      当成真实零涨跌，过期 last-good 只供审计。
    - holdings/watchlist 的 estimateDisplayDate 是估算展示日，targetNavDate 与
      latestOfficialNavDate 是净值 D 日；returnAttributionDate 才是收益归属 G 日。
      G 日不可靠时为 null，不能回退成 D 日。
    - holdings/watchlist[].estimateAudit: provider/engine/proxyCoverage、fxDegraded、
      partial、evidenceComplete 和 fallback 等审计字段；coverage 仅在后端审计传输
      实际提供时存在。普通回答不主动展开这些技术状态，用户明确要求诊断时才使用。

    Args:
        include_transactions: 是否在每条记录中附带原始 transactions。默认 false 以节省上下文。
            需要审计交易流水、重算收益或排查数据时设为 true。
    """
    _require_token()
    # 下载记录并复用缓存。
    portfolio = await _download_portfolio()
    funds: list = portfolio.get("funds", [])
    data_updated_at: str = portfolio.get("_meta_updated_at", "")
    data_source: str = portfolio.get("_meta_data_source", "")
    snapshot_summary: dict = portfolio.get("_meta_summary", {})
    user_preferences = portfolio.get("userPreferences") if isinstance(portfolio.get("userPreferences"), dict) else {}
    try:
        max_drawdown_limit_pct = float(user_preferences.get("strategyMaxDrawdownLimitPct", 10))
    except (TypeError, ValueError):
        max_drawdown_limit_pct = 10.0
    if max_drawdown_limit_pct != 0 and not 5 <= max_drawdown_limit_pct <= 30:
        max_drawdown_limit_pct = 10.0

    # 2. 与 App getWatchlistFundsByGroup 的可见性语义一致：如果同代码已有显式
    # 自选记录，不再把清仓持仓记录重复展示为自选。
    explicit_watchlist_codes = {
        str(fund.get("code") or "").strip()
        for fund in funds
        if fund.get("isWatchlist") is True
    }

    # 3. 并行批量获取今日估算数值；仅合并同一时刻的重叠请求。
    # 与 App 刷新口径一致：持仓和可见观察列（非送养）都请求盘中估算，
    # 送养隐藏项不请求，避免无谓的开销。
    estimate_codes = [
        str(fund.get("code") or "").strip()
        for fund in funds
        if (
            _is_valid_fund_code_value(fund.get("code"))
            and (
                (fund.get("isWatchlist") is not True and _to_float(fund.get("holdingShares")) > 0)
                or (
                    fund.get("isWatchlist") is True
                    or (
                        _to_float(fund.get("holdingShares")) == 0
                        and str(fund.get("code") or "").strip() not in explicit_watchlist_codes
                        and fund.get("clearedHideFromWatchlist") is not True
                    )
                )
            )
        )
    ]
    estimate_map: dict = {}
    if estimate_codes:
        default_mode = _normalize_data_source_mode(user_preferences.get("fundDataSourceMode"))
        mode_by_code = {}
        for fund in funds:
            code = str(fund.get("code") or "").strip()
            if not _is_valid_fund_code_value(code):
                continue
            fund_mode = fund.get("dataSourceMode")
            if fund_mode or code not in mode_by_code:
                mode_by_code[code] = _normalize_data_source_mode(fund_mode or default_mode)
        estimate_map = await _fetch_estimates(
            estimate_codes,
            default_data_source_mode=default_mode,
            data_source_mode_by_code=mode_by_code,
        )

    # 4. 计算每条记录的收益字段，剥离原始 transactions（减少 token 消耗）
    holdings = []
    watchlist = []

    for fund in funds:
        code = fund.get("code", "")
        normalized_code = str(code or "").strip()
        holding_shares = _to_float(fund.get("holdingShares"))
        is_explicit_watchlist = fund.get("isWatchlist") is True
        is_holding = not is_explicit_watchlist and holding_shares > 0
        is_visible_watchlist = is_explicit_watchlist or (
            holding_shares == 0
            and normalized_code not in explicit_watchlist_codes
            and fund.get("clearedHideFromWatchlist") is not True
        )
        if not is_holding and not is_visible_watchlist:
            continue

        est = estimate_map.get(code, {})
        stats = _calc_fund_stats(fund, est)
        txs = fund.get("transactions") or []
        requested_mode = mode_by_code.get(
            normalized_code,
            _normalize_data_source_mode(
                user_preferences.get("fundDataSourceMode")
            ),
        )
        estimate_audit = (
            _estimate_audit_payload(est, requested_mode)
            if est
            else None
        )

        # 响应仅保留汇总字段，不返回原始交易明细。
        enriched = {
            "code": code,
            "name": fund.get("name", ""),
            "type": est.get("type") or fund.get("type", ""),
            "sector": est.get("sector") or fund.get("sector", ""),
            "groupId": fund.get("groupId", ""),
            "tags": fund.get("tags", []),
            **stats,
        }
        auto_invest_plans = _auto_invest_plans(fund)
        if auto_invest_plans:
            enriched["autoInvestPlans"] = auto_invest_plans
        disciplines = _fund_disciplines(fund)
        if disciplines:
            enriched["disciplines"] = disciplines
        if include_transactions:
            enriched["transactions"] = txs

        # 估算时间（来自后端 gztime 字段）
        if est:
            enriched["estimateTime"] = est.get("gztime", "")
            enriched["estimateAudit"] = estimate_audit
            enriched["estimatePartial"] = estimate_audit["partial"]
            enriched["estimateEvidenceComplete"] = estimate_audit[
                "evidenceComplete"
            ]

        # 在途资产（PENDING 买入交易）
        pending_buy_txs = [
            {"date": tx.get("date"), "amount": tx.get("amount"), "note": tx.get("note")}
            for tx in txs if tx.get("status") == "PENDING" and tx.get("type") == "BUY"
        ]
        in_transit_amount = _r2(sum(_to_float(tx.get("amount")) for tx in pending_buy_txs))
        enriched["inTransitAmount"] = in_transit_amount
        if pending_buy_txs:
            enriched["pendingBuyTransactions"] = pending_buy_txs

        if is_holding:
            holdings.append(enriched)
        else:
            # 观察列仅包含基础信息和行情。
            watchlist_item = {
                "code": code,
                "name": fund.get("name", ""),
                "type": est.get("type") or fund.get("type", ""),
                "sector": est.get("sector") or fund.get("sector", ""),
                "lastNav": stats.get("lastNav"),
                "estimatedNav": stats.get("estimatedNav"),
                "estimatedChangePercent": stats.get("estimatedChangePercent"),
                "estimateSource": stats.get("estimateSource"),
                "estimateAvailable": stats.get("estimateAvailable"),
                "estimateFreshness": stats.get("estimateFreshness"),
                "estimateStale": stats.get("estimateStale"),
                "estimateDisplayDate": stats.get("estimateDisplayDate"),
                "targetNavDate": stats.get("targetNavDate"),
                "latestOfficialNavDate": stats.get("latestOfficialNavDate"),
                "lastNavPublishDate": stats.get("lastNavPublishDate"),
                "returnAttributionDate": stats.get("returnAttributionDate"),
                "estimateAudit": estimate_audit,
                "estimatePartial": (
                    estimate_audit.get("partial") is True
                    if estimate_audit
                    else False
                ),
                "estimateEvidenceComplete": (
                    estimate_audit.get("evidenceComplete") is True
                    if estimate_audit
                    else False
                ),
                **({"transactions": txs} if include_transactions else {}),
            }
            if auto_invest_plans:
                watchlist_item["autoInvestPlans"] = auto_invest_plans
            if disciplines:
                watchlist_item["disciplines"] = disciplines
            watchlist.append(watchlist_item)

    # 5. 汇总统计（只统计持仓项目）
    # 使用迭代累加而非 sum-then-round，精确对齐前端 analytics.ts 的逐步 r2 模式：
    #   totalMarketValue = r2(totalMarketValue + r2(stats.currentMarketValue))
    # 逐步舍入用于限制多基金累加的浮点误差。
    total_market_value = 0.0
    total_cost = 0.0
    total_today_profit = 0.0
    total_holding_profit = 0.0
    total_cumulative_profit = 0.0
    total_in_transit = 0.0
    total_invested = 0.0
    total_day_base_market_value = 0.0
    attributable_count = 0
    updated_count = 0
    pending_attribution_count = 0
    estimate_available_count = 0
    estimate_timeout_count = 0
    estimate_stale_count = 0
    estimate_partial_count = 0
    estimate_unavailable_codes = []
    estimate_timeout_codes = []
    estimate_stale_codes = []
    estimate_partial_codes = []
    valuation_available_count = 0
    valuation_freshened_codes = []
    valuation_missing_date_codes = []
    partial_estimated_market_value = 0.0
    estimated_market_value_available_count = 0
    for f in holdings:
        total_market_value = _r2(total_market_value + f.get("marketValue", 0))
        total_cost = _r2(total_cost + f.get("costTotal", 0))
        total_today_profit = _r2(total_today_profit + f.get("todayProfit", 0))
        total_day_base_market_value = _r2(total_day_base_market_value + f.get("dayBaseMarketValue", 0))
        total_holding_profit = _r2(total_holding_profit + f.get("holdingProfit", 0))
        total_cumulative_profit = _r2(total_cumulative_profit + f.get("totalProfit", 0))
        total_in_transit = _r2(total_in_transit + f.get("inTransitAmount", 0))
        total_invested = _r2(total_invested + f.get("totalInvested", 0))
        if f.get("displayedDayAttributable"):
            attributable_count += 1
            if f.get("estimateSource") == "official_published":
                updated_count += 1
        elif f.get("estimateSource") == "official_published":
            pending_attribution_count += 1
        if f.get("estimateAvailable"):
            estimate_available_count += 1
        else:
            estimate_unavailable_codes.append(f.get("code"))
        if f.get("estimateStale"):
            estimate_stale_count += 1
            estimate_stale_codes.append(f.get("code"))
        estimate_audit = f.get("estimateAudit")
        if (
            isinstance(estimate_audit, dict)
            and estimate_audit.get("partial") is True
        ):
            estimate_partial_count += 1
            estimate_partial_codes.append(f.get("code"))
        if f.get("estimateSource") == "timeout":
            estimate_timeout_count += 1
            estimate_timeout_codes.append(f.get("code"))
        if f.get("valuationAvailable"):
            valuation_available_count += 1
            if not f.get("valuationNavDate"):
                valuation_missing_date_codes.append(f.get("code"))
        if f.get("valuationFreshenedFromMarketData"):
            valuation_freshened_codes.append(f.get("code"))
        if f.get("estimatedMarketValue") is not None:
            estimated_market_value_available_count += 1
            partial_estimated_market_value = _r2(
                partial_estimated_market_value + f["estimatedMarketValue"]
            )
    estimate_unavailable_count = len(holdings) - estimate_available_count
    total_holding_return_rate = _ratio_pct(total_holding_profit, total_cost)
    today_profit_rate = _ratio_pct(total_today_profit, total_day_base_market_value)

    return {
        "holdings": holdings,
        "watchlist": watchlist,
        "groups": portfolio.get("groups", []),
        "summary": {
            "totalMarketValue": total_market_value,
            "totalCost": total_cost,
            "todayProfit": total_today_profit,
            "todayProfitRate": today_profit_rate,
            "totalDayBaseMarketValue": total_day_base_market_value,
            "totalHoldingProfit": total_holding_profit,
            "totalHoldingReturnRate": total_holding_return_rate,
            "cumulativeProfit": total_cumulative_profit,
            "totalInvested": total_invested,
            "heldItemCount": len(holdings),
            "totalInTransitAmount": total_in_transit,
            "emptyPortfolioConfirmed": snapshot_summary.get("empty_portfolio_confirmed", False),
            "isConfirmedEmptyPortfolioSnapshot": snapshot_summary.get("is_confirmed_empty_portfolio_snapshot", False),
            "hasRestorableSyncPayload": snapshot_summary.get("has_restorable_sync_payload", False),
            "dataSource": data_source,
            "displayedDayCompleteness": {
                "totalCount": len(holdings),
                "attributableCount": attributable_count,
                "updatedCount": updated_count,
                "pendingAttributionCount": pending_attribution_count,
                "complete": pending_attribution_count == 0,
            },
            "estimateCompleteness": {
                "totalCount": len(holdings),
                "availableCount": estimate_available_count,
                "unavailableCount": estimate_unavailable_count,
                "timeoutCount": estimate_timeout_count,
                "staleCount": estimate_stale_count,
                "partialCount": estimate_partial_count,
                "unavailableCodes": estimate_unavailable_codes,
                "timeoutCodes": estimate_timeout_codes,
                "staleCodes": estimate_stale_codes,
                "partialCodes": estimate_partial_codes,
                "evidenceComplete": (
                    estimate_unavailable_count == 0
                    and estimate_partial_count == 0
                ),
                "complete": estimate_unavailable_count == 0,
            },
            "valuationCompleteness": {
                "totalCount": len(holdings),
                "availableCount": valuation_available_count,
                "unavailableCount": len(holdings) - valuation_available_count,
                "freshenedCount": len(valuation_freshened_codes),
                "freshenedCodes": valuation_freshened_codes,
                "missingDateCount": len(valuation_missing_date_codes),
                "missingDateCodes": valuation_missing_date_codes,
                "complete": (
                    valuation_available_count == len(holdings)
                    and not valuation_missing_date_codes
                ),
            },
            "partialEstimatedMarketValue": partial_estimated_market_value,
            "totalEstimatedMarketValue": (
                partial_estimated_market_value
                if estimated_market_value_available_count == len(holdings)
                else None
            ),
            "estimatedMarketValueCompleteness": {
                "totalCount": len(holdings),
                "availableCount": estimated_market_value_available_count,
                "unavailableCount": len(holdings) - estimated_market_value_available_count,
                "complete": estimated_market_value_available_count == len(holdings),
            },
        },
        "snapshotSummary": snapshot_summary,
        "strategyPreferences": {
            "maxDrawdownLimitPct": max_drawdown_limit_pct,
        },
        "portfolioUpdatedAt": data_updated_at,
        "dataSource": data_source,
    }


async def get_summary() -> dict:
    """获取精简持仓总览；只问组合汇总时使用，综合投资分析改用 compact 策略上下文。"""
    _require_token()
    result = await _runtime_get_records()
    summary = result.get("summary", {})
    summary["portfolioUpdatedAt"] = result.get("portfolioUpdatedAt", "")
    return summary
