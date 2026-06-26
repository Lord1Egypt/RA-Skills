"""
mcp_connector/merger.py
────────────────────────
Client-side data merger — combines remote market quote with local ERP data.

This is where the "local aggregation" principle is implemented:
  Remote quote  → market price, risk score, advisory, quote action
  Local ERP     → local stock qty, supply status from YOUR inventory
  Merged view   → what the agent / user sees

The merger runs entirely on the client machine.  No ERP pricing data is
ever sent to the remote engine.

Schema v1.1 additions
──────────────────────
The MergedQuoteView now surfaces the reasoning engine's output:
  risk_level         — low | medium | high | unknown
  risk_index         — raw score 0.0–1.0 (None = data insufficient)
  tw_neutral_confidence — data quality score 0.0–1.0
  advisory           — professional trade guidance in the buyer's language
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from mcp_connector.api_client import RemoteQuote
from mcp_connector.erp_reader import ErpRecord


@dataclass(frozen=True)
class MergedQuoteView:
    """
    Combined view of remote market intelligence and local ERP inventory.
    Safe to display to the user in full — no server-side secrets included.
    """
    part_number: str
    requested_qty: int

    # ── Remote: pricing ────────────────────────────────────────────────────────
    market_quoted_price: float | None   # USD, rounded 4dp; None = pending review
    price_currency: str                 # always "USD"
    quote_action: str                   # auto_quote | pending | clarify
    market_stock_available: bool        # engine's availability signal
    market_supply_status: str | None    # normal | limited | eol | unavailable
    data_source: str                    # always "tw-neutral"

    # ── Remote: risk intelligence (v1.1) ─────────────────────────────────────
    risk_level: str                     # low | medium | high | unknown
    risk_index: float | None            # 0.0–1.0; None = insufficient data
    tw_neutral_confidence: float | None # data quality 0.0–1.0
    advisory: str | None                # trade guidance in buyer's language
    advisory_lang: str                  # language code

    # ── Local ERP (never sent to server) ─────────────────────────────────────
    local_stock_qty: float | None
    local_supply_status: str | None
    erp_source: str                     # excel | sqlite | unavailable

    # ── Computed ──────────────────────────────────────────────────────────────
    has_local_stock: bool
    recommendation: str                 # actionable one-liner for the trader


# ── Helpers ───────────────────────────────────────────────────────────────────

def _build_recommendation(
    quote_action: str,
    market_available: bool,
    local_qty: float | None,
    risk_level: str,
) -> str:
    """
    Produce a concise actionable recommendation that factors in BOTH
    the quote action AND the risk level.
    """
    has_local = bool(local_qty and local_qty > 0)
    risk_tag  = {
        "low":     "",
        "medium":  "  ⚠️  建議索取 CoC 文件。",
        "high":    "  🚨 高風險：勿自動下單，請升交品質團隊。",
        "unknown": "  ℹ️  資料不足，建議保守處理。",
    }.get(risk_level, "")

    if quote_action == "clarify":
        return "⚠️  請確認料號和數量後重試。"

    if quote_action == "auto_quote":
        if has_local:
            return f"✅ 可自動報價。本地庫存 {int(local_qty):,} 件，可直接出貨。{risk_tag}"
        if market_available:
            return f"✅ 可自動報價。市場有貨，需採購後出貨。{risk_tag}"
        return f"⚠️  可報價，但市場庫存信號不足，請確認供應。{risk_tag}"

    if quote_action == "pending":
        if has_local:
            return f"🔄 報價需人工審核。本地庫存 {int(local_qty):,} 件。{risk_tag}"
        return f"🔄 報價需人工審核。請聯繫採購確認庫存。{risk_tag}"

    return "❓ 狀態未知，請人工跟進。"


# ── Main merge function ────────────────────────────────────────────────────────

def merge(
    remote: RemoteQuote,
    local: ErpRecord,
    requested_qty: int = 0,
) -> MergedQuoteView:
    """Merge a remote quote (v1.1) with local ERP data into a unified view."""
    has_local = bool(local.stock_qty and local.stock_qty > 0)
    return MergedQuoteView(
        part_number          = remote.part_number,
        requested_qty        = requested_qty or remote.requested_qty,
        market_quoted_price  = remote.quoted_price,
        price_currency       = remote.price_currency,
        quote_action         = remote.quote_action,
        market_stock_available = remote.stock_available,
        market_supply_status = remote.supply_status,
        data_source          = remote.data_source,
        risk_level           = remote.risk_level,
        risk_index           = remote.risk_index,
        tw_neutral_confidence= remote.tw_neutral_confidence,
        advisory             = remote.advisory,
        advisory_lang        = remote.advisory_lang,
        local_stock_qty      = local.stock_qty,
        local_supply_status  = local.supply_status,
        erp_source           = local.source,
        has_local_stock      = has_local,
        recommendation       = _build_recommendation(
            remote.quote_action,
            remote.stock_available,
            local.stock_qty,
            remote.risk_level,
        ),
    )


# ── Display formatters ────────────────────────────────────────────────────────

_RISK_BADGE = {
    "low":     "🟢 低風險",
    "medium":  "🟡 中等風險",
    "high":    "🔴 高風險",
    "unknown": "⚪ 未知",
}

_ACTION_LABEL = {
    "auto_quote": "✅ 自動報價",
    "pending":    "🔄 待人工審核",
    "clarify":    "⚠️  請確認料號/數量",
}


def format_as_text(view: MergedQuoteView) -> str:
    """
    Format the merged view as a human-readable Markdown table for MCP output.
    Labels are in Traditional Chinese; values are language-neutral.
    The advisory section (if present) is appended in the buyer's chosen language.
    """
    price_str = (
        f"{view.price_currency} {view.market_quoted_price:.4f}"
        if view.market_quoted_price is not None
        else "待審核 / N/A"
    )
    local_qty_str = (
        f"{int(view.local_stock_qty):,} 件"
        if view.local_stock_qty is not None
        else "無資料"
    )
    risk_badge = _RISK_BADGE.get(view.risk_level, view.risk_level)
    risk_index_str = (
        f"{view.risk_index:.2f}"
        if view.risk_index is not None
        else "—"
    )
    confidence_str = (
        f"{view.tw_neutral_confidence:.0%}"
        if view.tw_neutral_confidence is not None
        else "—"
    )
    action_label = _ACTION_LABEL.get(view.quote_action, view.quote_action)

    lines = [
        f"## IC 報價彙整  —  {view.part_number}",
        "",
        "| 項目                | 內容                                        |",
        "|---------------------|---------------------------------------------|",
        f"| 料號                | `{view.part_number}`                        |",
        f"| 詢價數量            | {view.requested_qty:,} 件                   |",
        f"| 市場報價            | {price_str}                                 |",
        f"| 報價狀態            | {action_label}                              |",
        f"| 市場有貨            | {'是' if view.market_stock_available else '否'}                                       |",
        f"| 市場供應狀態        | {view.market_supply_status or '—'}          |",
        "| ——                  | ——                                          |",
        f"| 風險等級            | {risk_badge}  (index: {risk_index_str})     |",
        f"| 台灣中立資料信心度  | {confidence_str}                            |",
        "| ——                  | ——                                          |",
        f"| 本地 ERP 庫存       | {local_qty_str}                             |",
        f"| 本地供應狀態        | {view.local_supply_status or '—'}           |",
        f"| 資料來源標記        | {view.data_source}                          |",
        f"| ERP 資料來源        | {view.erp_source}                           |",
    ]

    lines += ["", f"**建議：** {view.recommendation}"]

    # Advisory block — shown in the language the buyer selected
    if view.advisory:
        lines += [
            "",
            f"---",
            f"**Trade Advisory ({view.advisory_lang}):**",
            "",
            f"> {view.advisory}",
        ]

    return "\n".join(lines)


def format_as_dict(view: MergedQuoteView) -> dict[str, Any]:
    """Return the merged view as a plain dict (for JSON serialisation)."""
    return {
        "part_number":             view.part_number,
        "requested_qty":           view.requested_qty,
        "market_quoted_price":     view.market_quoted_price,
        "price_currency":          view.price_currency,
        "quote_action":            view.quote_action,
        "market_stock_available":  view.market_stock_available,
        "market_supply_status":    view.market_supply_status,
        "data_source":             view.data_source,
        "risk_level":              view.risk_level,
        "risk_index":              view.risk_index,
        "tw_neutral_confidence":   view.tw_neutral_confidence,
        "advisory":                view.advisory,
        "advisory_lang":           view.advisory_lang,
        "local_stock_qty":         view.local_stock_qty,
        "local_supply_status":     view.local_supply_status,
        "erp_source":              view.erp_source,
        "has_local_stock":         view.has_local_stock,
        "recommendation":          view.recommendation,
    }
