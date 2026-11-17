#!/usr/bin/env python3
"""A complete read on one asset, in one pass.

"What's going on with ETH" is four questions wearing one coat: where is price,
where are the levels, where is leverage stacked, and has this configuration
resolved before. Each is a separate endpoint and none depends on another, so
they go out together — the workup costs one round trip, not four.

    python 01_asset_workup.py ETHUSDT
    python 01_asset_workup.py AAPL
"""

from __future__ import annotations

import concurrent.futures
import sys
from collections.abc import Callable
from typing import Any

import httpx
from client import BASE_URL, DEFAULT_TIMEOUT, NotFound, OracleXError, get


def is_equity(symbol: str) -> bool:
    """Equities are plain tickers; crypto pairs carry a quote or a venue prefix.

    The backend makes the same judgement before choosing an upstream — an
    unprefixed ticker used to be forced down the crypto path and read off a
    tokenised-equity market instead of the exchange it actually trades on.
    """
    upper = symbol.upper()
    if ":" in upper:
        return False
    return not upper.endswith(("USDT", "USDC", "USD", "BTC", "ETH"))


def failed(view: Any) -> bool:
    """True when a view is an error record rather than data or a clean absence."""
    return isinstance(view, dict) and "__error__" in view


def workup(symbol: str) -> dict[str, Any]:
    """Fetch every independent view of one symbol concurrently."""
    calls: dict[str, Callable[[httpx.Client], Any]] = {
        "price": lambda c: get(f"/api/price/{symbol}", client=c),
        "technical": lambda c: get(f"/api/technical/{symbol}", client=c),
        "memory": lambda c: get(f"/api/rag/insights/{symbol}", client=c),
    }
    if is_equity(symbol):
        calls["ownership"] = lambda c: get(f"/api/ownership/assets/{symbol}", client=c)
        # `type` defaults to the crypto branch, which resolves through
        # CoinGecko and answers 404 for a ticker. An equity has to say so.
        calls["fundamentals"] = lambda c: get(
            f"/api/asset-detail/{symbol}", {"type": "stock"}, client=c
        )
    else:
        # `/levels/` is a histogram of liquidations that already happened and
        # requires an explicit price_min/price_max window; `/map/` is the
        # forward-looking estimate and needs neither, which is what a workup
        # wants.
        calls["liquidations"] = lambda c: get(
            f"/api/liquidations/map/{symbol}", client=c
        )

    results: dict[str, Any] = {}
    with (
        httpx.Client(base_url=BASE_URL, timeout=DEFAULT_TIMEOUT) as shared,
        concurrent.futures.ThreadPoolExecutor(max_workers=len(calls)) as pool,
    ):
        futures = {pool.submit(fn, shared): name for name, fn in calls.items()}
        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            try:
                results[name] = future.result()
            except NotFound:
                # A 404 is an answer: this instance holds nothing for that
                # view. Record the absence instead of dropping the key, so
                # the caller can say so rather than staying silent.
                results[name] = None
            except OracleXError as exc:
                results[name] = {"__error__": str(exc)}

    # If nothing came back, the instance is down rather than thin on data.
    # Returning the dict anyway would let the caller render a summary out of
    # four failures, which reads exactly like an answer and is the one outcome
    # a workup must never produce.
    if all(failed(view) for view in results.values()):
        raise OracleXError(
            f"No view of {symbol} could be fetched. "
            f"{next(iter(results.values()))['__error__']}"
        )
    return results


def summarize(symbol: str, data: dict[str, Any]) -> str:
    """Render the workup, keeping the three outcomes visibly distinct.

    Data, a clean absence (the endpoint answered 404), and a failure (the call
    never landed) have to read differently. Collapsing the last two into
    silence is how a report ends up implying the instance confirmed something
    it was never asked.
    """
    lines = [f"# {symbol}", ""]

    quote = data.get("price")
    if failed(quote):
        lines.append(f"Price: unavailable — {quote['__error__']}")
    elif isinstance(quote, dict):
        # The payload names its upstream. Carrying that through matters: two
        # venues disagree by a few basis points, and a user comparing this
        # answer against their own screen should be able to see which one
        # answered rather than assume the difference is an error.
        value = quote.get("price")
        source = quote.get("source")
        lines.append(f"Price: {value} ({source})" if value else "Price: n/a")
    else:
        lines.append("Price: the instance could not resolve this symbol.")

    technical = data.get("technical")
    lines.append("")
    lines.append("## Levels")
    if failed(technical):
        lines.append(f"Unavailable — {technical['__error__']}")
    elif technical is None:
        lines.append("The instance could not compute levels for this symbol.")
    else:
        lines.append(
            f"Price {technical.get('current_price')} · "
            f"trend {technical.get('trend')} · "
            f"RSI {technical.get('rsi_value')} ({technical.get('rsi_signal')})"
        )
        # `zones` is keyed by kind — support / resistance / inside — and each
        # zone carries the timeframes that confirmed it. That confluence list
        # is the point of the endpoint: a band agreed on by 1d+1w is a
        # different claim from one seen only on 4h, and dropping it would
        # flatten the answer back into a plain number.
        zones = technical.get("zones") or {}
        for kind in ("support", "resistance"):
            for zone in (zones.get(kind) or [])[:3]:
                confirmed = ", ".join(zone.get("timeframes") or []) or "?"
                lines.append(
                    f"- {kind}: {zone.get('low')}–{zone.get('high')} "
                    f"({zone.get('distance_percent')}% away, confirmed on "
                    f"{confirmed}, strength {zone.get('strength', '?')})"
                )
        if not zones:
            lines.append("No zones returned. Inspect the raw payload.")

    for key, heading, present in (
        ("liquidations", "Leverage", "Liquidation map retrieved."),
        ("ownership", "Holders", "Institutional positions retrieved."),
        ("fundamentals", "Fundamentals", "Company data retrieved."),
    ):
        if key not in data:
            continue
        view = data[key]
        lines += ["", f"## {heading}"]
        if failed(view):
            lines.append(f"Unavailable — {view['__error__']}")
        elif view:
            lines.append(f"{present} See the raw payload.")
        else:
            lines.append("Nothing recorded for this symbol.")

    memory = data.get("memory")
    lines += ["", "## Precedent"]
    if failed(memory):
        lines.append(f"Unavailable — {memory['__error__']}")
    elif memory:
        lines.append("The store holds prior context for this symbol.")
    else:
        lines.append("The memory has nothing on this symbol yet.")

    return "\n".join(lines)


def main() -> int:
    symbol = sys.argv[1] if len(sys.argv) > 1 else "BTCUSDT"
    try:
        data = workup(symbol)
    except OracleXError as exc:
        print(exc, file=sys.stderr)
        return 1
    print(summarize(symbol, data))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
