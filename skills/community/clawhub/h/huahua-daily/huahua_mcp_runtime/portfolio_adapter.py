"""Pure adapters for canonical PowerSync v3 portfolio responses."""

import json
import math
import re
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

from .portfolio_math import EFFECTIVE_ZERO_SHARES

CONFIRMED_EMPTY_PORTFOLIO_KEYS = {
    "funds", "archivedLedger", "deletedFundsMeta", "dismissedDividendKeys",
    "userPreferences", "groups", "watchlistGroups", "globalTags", "tagDisplayCount",
    "fieldConfigs", "watchlistFieldConfigs", "nightWatchCodes", "purchaseLimitWatchItems",
    "purchaseLimitWatchNightDefaultsMigrated", "marketIndexSelection", "emptyPortfolioConfirmed",
    "clearedAt", "timestamp", "version",
}


def is_valid_fund_code_value(value) -> bool:
    return bool(re.fullmatch(r"\d{6}", str(value or "").strip()))


def is_restorable_fund(fund) -> bool:
    return isinstance(fund, dict) and is_valid_fund_code_value(fund.get("code"))


def is_empty_plain_object(value) -> bool:
    return isinstance(value, dict) and len(value) == 0


def summarize_sync_payload(parsed: dict) -> dict:
    funds = parsed.get("funds")
    has_funds_array = isinstance(funds, list)
    fund_items = funds if has_funds_array else []
    restorable = [fund for fund in fund_items if is_restorable_fund(fund)]
    empty_portfolio_confirmed = parsed.get("emptyPortfolioConfirmed") is True
    is_confirmed_empty = (
        bool(parsed)
        and not any(key not in CONFIRMED_EMPTY_PORTFOLIO_KEYS for key in parsed)
        and has_funds_array
        and len(fund_items) == 0
        and empty_portfolio_confirmed
        and ("archivedLedger" not in parsed or is_empty_plain_object(parsed.get("archivedLedger")))
        and ("deletedFundsMeta" not in parsed or is_empty_plain_object(parsed.get("deletedFundsMeta")))
    )
    return {
        "has_payload": bool(parsed),
        "has_funds_array": has_funds_array,
        "fund_count": len(fund_items),
        "restorable_fund_count": len(restorable),
        "portfolio_fund_count": sum(1 for fund in restorable if fund.get("isWatchlist") is not True),
        "watchlist_fund_count": sum(1 for fund in restorable if fund.get("isWatchlist") is True),
        "empty_portfolio_confirmed": empty_portfolio_confirmed,
        "is_confirmed_empty_portfolio_snapshot": is_confirmed_empty,
        "has_restorable_sync_payload": len(restorable) > 0 or is_confirmed_empty,
    }


def portfolio_payload_source(raw: dict, fallback: str = "") -> str:
    del fallback
    if raw.get("protocolVersion") != 3:
        raise RuntimeError("云同步服务协议不是 PowerSync v3，请先更新服务端")
    return "portfolio_v3"


def _active(items: object) -> list[dict]:
    if not isinstance(items, list):
        return []
    return [
        item for item in items
        if isinstance(item, dict) and item.get("deletedAt") in {None, ""}
    ]


def _json_value(value: object) -> object:
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except (TypeError, ValueError):
        return None


def _finite(value: object, default: float = 0.0) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return default
    return parsed if math.isfinite(parsed) else default


def _round(value: float, digits: int) -> float:
    try:
        quantum = Decimal(1).scaleb(-digits)
        return float(Decimal(str(value)).quantize(quantum, rounding=ROUND_HALF_UP))
    except (InvalidOperation, ValueError):
        return 0.0


_TX_TYPE_ORDER = {
    "CORRECTION": 0,
    "SELL": 1,
    "BUY": 2,
    "DIVIDEND_CASH": 3,
    "DIVIDEND_REINVEST": 3,
}


def _transaction_sort_key(indexed: tuple[int, dict]) -> tuple:
    index, transaction = indexed
    transaction_type = str(transaction.get("type") or "")
    effective_date = str(
        transaction.get("confirmDate") or transaction.get("date") or ""
    )[:10]
    cash_rank = 1 if transaction_type == "DIVIDEND_CASH" else 0
    day_order = transaction.get("dayOrder")
    day_order_rank = _finite(day_order, float("inf")) \
        if day_order is not None else float("inf")
    return (
        effective_date,
        cash_rank,
        day_order_rank,
        _TX_TYPE_ORDER.get(transaction_type, 9),
        index,
    )


def _recalculate_fund_state(transactions: list[dict]) -> dict[str, float]:
    """Mirror the App's authoritative transaction replay for MCP projections."""

    holding_shares = 0.0
    total_input_principal = 0.0
    realized_profit = 0.0
    confirmed = [
        item for item in transactions
        if str(item.get("status") or "") == "CONFIRMED"
    ]
    ordered = [
        item for _, item in sorted(enumerate(confirmed), key=_transaction_sort_key)
    ]
    for transaction in ordered:
        transaction_type = str(transaction.get("type") or "")
        amount = _finite(transaction.get("amount"))
        shares = _finite(transaction.get("shares"))
        nav = _finite(transaction.get("nav"))
        fee = _finite(transaction.get("fee"))
        if transaction_type == "BUY":
            buy_shares = _round(shares, 6) if shares > 0 else 0.0
            if buy_shares <= 0:
                net_amount = _round(max(0.0, amount - fee), 2)
                buy_shares = _round(net_amount / nav, 6) if nav > 0 and net_amount > 0 else 0.0
            buy_amount = amount
            if buy_amount <= 0 and buy_shares > 0 and nav > 0:
                buy_amount = _round(buy_shares * nav, 2)
            if buy_shares > 0 and buy_amount > 0:
                holding_shares = _round(holding_shares + buy_shares, 6)
                total_input_principal = _round(total_input_principal + buy_amount, 2)
        elif transaction_type == "CORRECTION":
            if shares < 0 or nav <= 0:
                continue
            holding_shares = _round(shares, 6)
            total_input_principal = _round(shares * nav, 2)
        elif transaction_type == "SELL":
            sell_shares = shares
            if sell_shares <= 0 and nav > 0:
                sell_shares = _round(amount / nav, 6)
            sell_amount = amount
            if sell_amount <= 0 and sell_shares > 0 and nav > 0:
                sell_amount = _round(sell_shares * nav, 2)
            if sell_shares > 0 and sell_amount > 0:
                sold_principal = _round(
                    total_input_principal * min(sell_shares, holding_shares) / holding_shares,
                    2,
                ) if holding_shares > 0 else 0.0
                transaction_profit = _round((sell_amount - fee) - sold_principal, 2)
                realized_profit = _round(realized_profit + transaction_profit, 2)
                holding_shares = _round(holding_shares - sell_shares, 6)
                total_input_principal = _round(total_input_principal - sold_principal, 2)
                if holding_shares <= EFFECTIVE_ZERO_SHARES:
                    holding_shares = 0.0
                    total_input_principal = 0.0
        elif transaction_type == "DIVIDEND_CASH":
            realized_profit = _round(realized_profit + amount, 2)
        elif transaction_type == "DIVIDEND_REINVEST":
            reinvest_shares = shares
            if reinvest_shares <= 0 and nav > 0 and amount > 0:
                reinvest_shares = _round(amount / nav, 6)
            if reinvest_shares > 0:
                holding_shares = _round(holding_shares + reinvest_shares, 6)
    return {
        "holdingShares": holding_shares,
        "holdingCost": (
            _round(total_input_principal / holding_shares, 4)
            if holding_shares > 0 else 0.0
        ),
        "holdingCostTotal": _round(total_input_principal, 2),
        "realizedProfit": realized_profit,
    }


def _decode_membership_value(item: dict) -> tuple[int, object]:
    parsed = _json_value(item.get("valueJson"))
    if (
        isinstance(parsed, dict)
        and isinstance(parsed.get("__huahuaOrder"), int)
        and "value" in parsed
    ):
        return int(parsed["__huahuaOrder"]), parsed["value"]
    return 2**53 - 1, parsed


def _project_v3_preferences(raw: dict, tags: list[dict]) -> dict:
    result: dict = {}
    domains = {
        "user_preferences": "userPreferences",
        "field_config": "fieldConfigs",
        "watchlist_field_config": "watchlistFieldConfigs",
    }
    for item in _active(raw.get("settings")):
        domain = str(item.get("domain") or "")
        key = str(item.get("key") or "")
        value = _json_value(item.get("valueJson"))
        if domain == "tag" and key == "display_count":
            result["tagDisplayCount"] = value
            continue
        if domain == "purchase_limit" and key == "night_defaults_migrated":
            result["purchaseLimitWatchNightDefaultsMigrated"] = value is True
            continue
        target = domains.get(domain)
        if target and key:
            result.setdefault(target, {})[key] = value

    collection_names = {
        "night_watch_codes": "nightWatchCodes",
        "market_index_selection": "marketIndexSelection",
        "purchase_limit_watch_items": "purchaseLimitWatchItems",
        "archived_ledger": "archivedLedger",
        "deleted_funds_meta": "deletedFundsMeta",
        "dismissed_dividend_keys": "dismissedDividendKeys",
    }
    grouped: dict[str, list[dict]] = {}
    all_memberships = raw.get("settingMemberships")
    if isinstance(all_memberships, list):
        for item in all_memberships:
            if not isinstance(item, dict):
                continue
            collection = str(item.get("collection") or "")
            if collection in collection_names:
                grouped.setdefault(collection, []).append(item)
    for collection, all_items in grouped.items():
        target = collection_names[collection]
        decoded = [
            (item, *_decode_membership_value(item))
            for item in all_items
            if item.get("deletedAt") in {None, ""}
        ]
        decoded.sort(key=lambda value: (value[1], str(value[0].get("memberKey") or "")))
        if target in {"archivedLedger", "deletedFundsMeta"}:
            result[target] = {
                str(item.get("memberKey") or ""): value
                for item, _order, value in decoded
            }
        else:
            result[target] = [value for _item, _order, value in decoded]
    result["globalTags"] = [
        {"text": item.get("name", ""), "color": item.get("color") or "red"}
        for item in tags
    ]
    return result


def adapt_portfolio_v3_state(raw: dict) -> dict:
    """Project normalized v3 rows into the stable MCP portfolio tool model."""

    groups = sorted(_active(raw.get("groups")), key=lambda item: str(item.get("sortRank") or ""))
    positions = sorted(_active(raw.get("positions")), key=lambda item: str(item.get("sortRank") or ""))
    transactions = _active(raw.get("transactions"))
    plans = _active(raw.get("autoInvestPlans"))
    disciplines = _active(raw.get("disciplines"))
    triggers = [item for item in raw.get("disciplineTriggers", []) if isinstance(item, dict)] \
        if isinstance(raw.get("disciplineTriggers"), list) else []
    tags = sorted(_active(raw.get("tags")), key=lambda item: str(item.get("sortRank") or ""))
    position_tags = [
        item for item in raw.get("positionTags", [])
        if isinstance(item, dict) and item.get("active") is True
    ] if isinstance(raw.get("positionTags"), list) else []

    transactions_by_position: dict[str, list[dict]] = {}
    for item in transactions:
        transaction = {
            "id": item.get("id"),
            "type": item.get("type"),
            "status": item.get("status"),
            "date": item.get("tradeDate"),
            "confirmDate": item.get("confirmDate"),
            "navDate": item.get("navDate"),
            "amount": item.get("amount", "0"),
            "shares": item.get("shares", "0"),
            "nav": item.get("nav", "0"),
            "fee": item.get("fee", "0"),
            "dayOrder": item.get("dayOrder"),
            "timeMode": item.get("timeMode"),
            "feeMode": item.get("feeMode"),
            "feeValue": item.get("feeValue"),
            "origin": item.get("origin"),
            "createdAt": item.get("createdAt"),
        }
        transactions_by_position.setdefault(str(item.get("positionId") or ""), []).append(transaction)

    plans_by_position: dict[str, list[dict]] = {}
    for item in plans:
        plan = {
            "id": item.get("id"),
            "enabled": item.get("enabled") is True,
            "amount": item.get("amount", "0"),
            "feeRate": item.get("feeRate"),
            "cycle": item.get("cycle"),
            "nextRunDate": item.get("nextRunDate"),
            "timeMode": item.get("timeMode"),
            "weekDay": item.get("weekDay"),
            "monthDay": item.get("monthDay"),
        }
        plans_by_position.setdefault(str(item.get("positionId") or ""), []).append(plan)

    latest_trigger_by_discipline: dict[str, dict] = {}
    for item in triggers:
        discipline_id = str(item.get("disciplineId") or "")
        current = latest_trigger_by_discipline.get(discipline_id)
        if current is None or str(item.get("createdAt") or "") >= str(current.get("createdAt") or ""):
            latest_trigger_by_discipline[discipline_id] = item
    disciplines_by_position: dict[str, list[dict]] = {}
    for item in disciplines:
        if item.get("enabled") is not True:
            continue
        trigger = latest_trigger_by_discipline.get(str(item.get("id") or ""))
        discipline = {
            "id": item.get("id"),
            "conditionType": item.get("conditionType"),
            "threshold": item.get("threshold"),
            "note": item.get("note") or None,
            "triggered": item.get("breachActive") is True,
            "triggeredAt": trigger.get("createdAt") if trigger else None,
            "dismissed": bool(trigger and trigger.get("dismissedAt")),
        }
        disciplines_by_position.setdefault(str(item.get("positionId") or ""), []).append(discipline)

    tags_by_id = {str(item.get("id") or ""): item for item in tags}
    memberships_by_position: dict[str, list[dict]] = {}
    for item in position_tags:
        memberships_by_position.setdefault(str(item.get("positionId") or ""), []).append(item)

    funds: list[dict] = []
    for position in positions:
        position_id = str(position.get("id") or "")
        transactions_for_position = transactions_by_position.get(position_id, [])
        holding = _recalculate_fund_state(transactions_for_position)
        memberships = memberships_by_position.get(position_id, [])
        tag_names = [
            tags_by_id[tag_id].get("name", "")
            for tag_id in [str(item.get("tagId") or "") for item in memberships]
            if tag_id in tags_by_id
        ]
        visible_tag_names = [
            tags_by_id[tag_id].get("name", "")
            for tag_id in [
                str(item.get("tagId") or "")
                for item in memberships if item.get("visible") is True
            ]
            if tag_id in tags_by_id
        ]
        asset_key = str(position.get("assetKey") or "")
        code = asset_key.split(":", 1)[1] if asset_key.lower().startswith("fund:") else asset_key
        is_watchlist = position.get("kind") == "watchlist"
        fund = {
            "id": position_id,
            "code": code,
            "name": position.get("name") or code,
            "groupId": "" if is_watchlist else position.get("groupId", ""),
            "watchlistGroupId": position.get("watchlistGroupId") or (
                position.get("groupId", "") if is_watchlist else None
            ),
            "pinned": position.get("pinned") is True,
            "isWatchlist": is_watchlist,
            "clearedHideFromWatchlist": position.get("hiddenFromWatchlist") is True,
            "dataSourceMode": position.get("dataSourcePreference"),
            "defaultBuyRate": position.get("defaultBuyFeeRate"),
            "defaultSellRate": position.get("defaultSellFeeRate"),
            "transactions": transactions_for_position,
            "tags": tag_names,
            "visibleTags": visible_tag_names,
            **({
                "holdingShares": 0.0,
                "holdingCost": 0.0,
                "holdingCostTotal": 0.0,
                "realizedProfit": 0.0,
            } if is_watchlist else holding),
        }
        position_plans = plans_by_position.get(position_id, [])
        if len(position_plans) == 1:
            fund["autoInvestConfig"] = position_plans[0]
        elif position_plans:
            fund["autoInvestConfigs"] = position_plans
        position_disciplines = disciplines_by_position.get(position_id, [])
        if position_disciplines:
            fund["disciplines"] = position_disciplines
        funds.append(fund)

    projected = {
        "version": "portfolio-v3",
        "timestamp": raw.get("updatedAt"),
        "funds": funds,
        "groups": [
            {"id": item.get("id"), "name": item.get("name", ""), "isDefault": item.get("isDefault") is True}
            for item in groups if item.get("scope") == "portfolio"
        ],
        "watchlistGroups": [
            {"id": item.get("id"), "name": item.get("name", ""), "isDefault": item.get("isDefault") is True}
            for item in groups if item.get("scope") == "watchlist"
        ],
        "emptyPortfolioConfirmed": len(funds) == 0,
        **_project_v3_preferences(raw, tags),
    }
    return projected


def unwrap_sync_payload(raw: dict, source: str = "") -> dict:
    portfolio_payload_source(raw, source)
    parsed = adapt_portfolio_v3_state(raw)
    summary = summarize_sync_payload(parsed)
    parsed["_meta_summary"] = summary
    parsed["_meta_updated_at"] = raw.get("updatedAt", "")
    parsed["_meta_etag"] = f'v3:{raw.get("syncEpoch", 1)}:{raw.get("changeVersion", 0)}'
    parsed["_meta_data_source"] = "portfolio_v3"
    parsed["_meta_size_bytes"] = len(
        json.dumps(raw, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    )
    parsed["_meta_protocol_version"] = 3
    parsed["_meta_sync_epoch"] = raw.get("syncEpoch", 1)
    parsed["_meta_change_version"] = raw.get("changeVersion", 0)
    for key, value in summary.items():
        parsed[f"_meta_{key}"] = value
    return parsed
