"""
mcp_connector/api_client.py
────────────────────────────
HTTP client that calls the remote api_engine (v1.1 schema).

Design decisions
─────────────────
- Uses httpx (sync) — keeps the connector single-threaded and simple.
- Sends ONLY part_number, qty, and lang to the engine.
  ERP pricing data NEVER leaves the client machine.
- Validates that the response schema matches the allowed key set before
  returning — guards against accidental leakage if the server returns extra.
- Raises QuoteApiError (not raw HTTPError) so callers get clean handling.

Schema v1.1 fields now surfaced to callers
───────────────────────────────────────────
  risk_index          — counterfeit/grey-market risk score 0.0–1.0
  risk_level          — "low" | "medium" | "high" | "unknown"
  tw_neutral_confidence — data quality / cross-source consistency 0.0–1.0
  advisory            — professional trade guidance (in requested language)
  advisory_lang       — language code the advisory was generated in
  schema_version      — "1.1" (for forward-compat checks)
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any

try:
    import httpx
except ImportError:
    httpx = None  # type: ignore[assignment]

from mcp_connector.config import config

log = logging.getLogger("mcp_connector.api_client")


class QuoteApiError(Exception):
    """Raised when the remote engine returns an error or is unreachable."""
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


# ── Response field policy ─────────────────────────────────────────────────────

# All fields from PublicQuoteResponse (schemas v1.1) that are safe to consume
_ALLOWED_RESPONSE_KEYS = frozenset({
    # Core response fields
    "ok", "schema_version", "part_number", "requested_qty",
    # Pricing
    "quoted_price", "price_currency", "quote_action",
    # Availability
    "stock_available", "supply_status",
    # Risk intelligence — new in v1.1
    "risk_index", "risk_level", "tw_neutral_confidence",
    # Advisory
    "advisory", "advisory_lang",
    # Metadata
    "data_source", "created_at",
    # Error
    "error",
})

# Fields that MUST NEVER appear in a server response (defence-in-depth check)
_FORBIDDEN_RESPONSE_KEYS = frozenset({
    "erp_floor_price", "erp_normal_price", "confidence",
    "auto_reply_allowed", "handoff_reason", "market_low_price",
    "market_quote_count", "stock_qty", "reasons", "source_mode",
    "source_platform", "evidence_json", "erp_inventory_found",
    "erp_inventory_stock_qty", "decision_stub", "erp_context",
})


# ── Result type ───────────────────────────────────────────────────────────────

@dataclass(frozen=True)
class RemoteQuote:
    """
    Parsed, sanitised remote quote response (schema v1.1).

    Risk fields
    ───────────
    risk_index           Counterfeit/grey-market risk score 0.0–1.0.
                         None = server could not compute (treat as medium).
    risk_level           Human-readable tier: low | medium | high | unknown.
                         AUTO-DERIVED by the server from risk_index thresholds.
    tw_neutral_confidence  Data quality indicator 0.0–1.0.
                          High = multiple independent sources agree.
                          Low  = single source or wide price spread.
    advisory             Professional trade guidance in the requested language.
                          None = server could not generate (network/data issue).
    """
    ok: bool
    schema_version: str
    part_number: str
    requested_qty: int

    # Pricing
    quoted_price: float | None
    price_currency: str
    quote_action: str               # auto_quote | pending | clarify

    # Availability
    stock_available: bool
    supply_status: str | None       # normal | limited | eol | unavailable | unknown

    # Risk intelligence (v1.1)
    risk_index: float | None        # 0.0–1.0
    risk_level: str                 # low | medium | high | unknown
    tw_neutral_confidence: float | None

    # Advisory (v1.1)
    advisory: str | None
    advisory_lang: str              # language code the advisory is in

    # Metadata
    data_source: str                # always "tw-neutral"
    created_at: str                 # UTC ISO 8601

    # Error
    error: str | None


# ── Internal helpers ──────────────────────────────────────────────────────────

def _sanitise_response(data: dict[str, Any]) -> dict[str, Any]:
    """
    Strip any keys not in the allowed set; raise a warning if forbidden keys appear.
    This is a client-side safety net — the server should already be sanitised,
    but defence in depth matters.
    """
    found_forbidden = _FORBIDDEN_RESPONSE_KEYS & data.keys()
    if found_forbidden:
        log.error(
            "SECURITY: server response contained forbidden keys: %s — dropping them.",
            sorted(found_forbidden),
        )
    return {k: v for k, v in data.items() if k in _ALLOWED_RESPONSE_KEYS}


def _parse_float(val: Any) -> float | None:
    if val is None:
        return None
    try:
        return float(val)
    except (TypeError, ValueError):
        return None


# ── Public API ────────────────────────────────────────────────────────────────

def fetch_quote(
    part_number: str,
    qty: int = 0,
    customer_id: str = "",
    lang: str = "en",
) -> RemoteQuote:
    """
    Call GET /v1/quote on the remote api_engine and return a RemoteQuote.

    Parameters
    ──────────
    part_number   Part number to query (will be normalised server-side).
    qty           Requested quantity.  0 = unspecified.
    customer_id   Optional opaque ID for server-side logging only.
    lang          Advisory language code: en | de | ja | zh-TW | fr | ko.
                  Defaults to "en".

    Raises
    ──────
    QuoteApiError — engine unreachable, non-200, or response fails validation.
    ImportError   — httpx is not installed.
    """
    if httpx is None:
        raise ImportError(
            "httpx is required for the MCP connector.  "
            "Install it with:  pip install httpx"
        )

    if not config.engine_url:
        raise QuoteApiError("QUOTE_ENGINE_URL is not configured.")
    if not config.engine_api_key:
        raise QuoteApiError("QUOTE_ENGINE_API_KEY is not configured.")

    # ── Build request ─────────────────────────────────────────────────────────
    url    = f"{config.engine_url}/v1/quote"
    params: dict[str, Any] = {
        "part_number": part_number,
        "qty":         qty,
        "lang":        lang,
    }
    if customer_id:
        params["customer_id"] = customer_id

    log.info("Fetching remote quote: part=%s qty=%d lang=%s", part_number, qty, lang)

    # ── HTTP call ─────────────────────────────────────────────────────────────
    try:
        resp = httpx.get(
            url,
            params=params,
            headers={"X-API-Key": config.engine_api_key},
            timeout=config.timeout,
        )
    except httpx.TimeoutException:
        raise QuoteApiError(
            f"Request to {url} timed out after {config.timeout}s."
        )
    except httpx.RequestError as exc:
        raise QuoteApiError(f"Network error reaching {url}: {exc}")

    # ── Status code handling ──────────────────────────────────────────────────
    if resp.status_code == 403:
        raise QuoteApiError("API key rejected by engine.", status_code=403)
    if resp.status_code == 404:
        raise QuoteApiError(
            f"Endpoint not found: {url}  (is the engine running /v1/?)",
            status_code=404,
        )
    if resp.status_code >= 500:
        raise QuoteApiError(
            f"Engine returned server error {resp.status_code}.",
            status_code=resp.status_code,
        )
    if resp.status_code != 200:
        raise QuoteApiError(
            f"Unexpected status {resp.status_code} from engine.",
            status_code=resp.status_code,
        )

    # ── Parse & sanitise ─────────────────────────────────────────────────────
    try:
        raw: dict[str, Any] = resp.json()
    except Exception:
        raise QuoteApiError("Engine returned non-JSON response.")

    safe = _sanitise_response(raw)

    return RemoteQuote(
        ok               = bool(safe.get("ok", False)),
        schema_version   = str(safe.get("schema_version", "1.1")),
        part_number      = str(safe.get("part_number", part_number)),
        requested_qty    = int(safe.get("requested_qty", qty)),
        quoted_price     = _parse_float(safe.get("quoted_price")),
        price_currency   = str(safe.get("price_currency", "USD")),
        quote_action     = str(safe.get("quote_action", "pending")),
        stock_available  = bool(safe.get("stock_available", False)),
        supply_status    = str(safe["supply_status"]) if safe.get("supply_status") else None,
        risk_index       = _parse_float(safe.get("risk_index")),
        risk_level       = str(safe.get("risk_level", "unknown")),
        tw_neutral_confidence = _parse_float(safe.get("tw_neutral_confidence")),
        advisory         = str(safe["advisory"]) if safe.get("advisory") else None,
        advisory_lang    = str(safe.get("advisory_lang", lang)),
        data_source      = str(safe.get("data_source", "tw-neutral")),
        created_at       = str(safe.get("created_at", "")),
        error            = str(safe["error"]) if safe.get("error") else None,
    )
