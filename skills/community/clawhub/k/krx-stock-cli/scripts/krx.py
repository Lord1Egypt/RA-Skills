#!/usr/bin/env python3
"""krx-stock-cli — Korean Exchange (KRX) stock market data CLI.

Backed by the FinanceDataReader library (https://github.com/FinanceData/FinanceDataReader),
which aggregates KRX, Naver Finance, and other public sources. No API key required.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timedelta
from typing import Any

try:
    import pandas as pd
    import FinanceDataReader as fdr
except ImportError as exc:
    sys.stderr.write(
        f"[krx-stock-cli] missing dependency: {exc.name}. "
        "Install with `pip install -r scripts/requirements.txt`.\n"
    )
    sys.exit(10)


# ---- helpers --------------------------------------------------------------


def _today() -> str:
    return date.today().strftime("%Y-%m-%d")


def _days_ago(n: int) -> str:
    return (date.today() - timedelta(days=n)).strftime("%Y-%m-%d")


def _normalize_date(s: str | None) -> str | None:
    if not s:
        return None
    s = s.strip()
    if re.fullmatch(r"\d{8}", s):
        return f"{s[:4]}-{s[4:6]}-{s[6:]}"
    if re.fullmatch(r"\d{4}-\d{2}-\d{2}", s):
        return s
    return s  # let fdr complain


def _resolve_range(args: argparse.Namespace) -> tuple[str, str]:
    end = _normalize_date(args.end) or _today()
    if args.start:
        return _normalize_date(args.start), end
    if args.days:
        return _days_ago(args.days), end
    return _days_ago(30), end


def _emit(df: pd.DataFrame | list | dict, as_csv: bool) -> None:
    if isinstance(df, pd.DataFrame):
        if df.index.name:
            df = df.reset_index()
        df.columns = [str(c) for c in df.columns]
        if as_csv:
            df.to_csv(sys.stdout, index=False)
            return
        _print_json(df.to_dict(orient="records"))
        return
    if as_csv:
        sys.stderr.write("[krx-stock-cli] --csv only supported for tabular output\n")
        sys.exit(4)
    _print_json(df)


def _print_json(payload: Any) -> None:
    def _default(o: Any) -> Any:
        if isinstance(o, (pd.Timestamp, datetime, date)):
            return o.strftime("%Y-%m-%d")
        if hasattr(o, "item"):
            return o.item()
        if pd.isna(o):
            return None
        return str(o)

    json.dump(payload, sys.stdout, ensure_ascii=False, indent=2, default=_default)
    sys.stdout.write("\n")


def _fail(code: str, **extra: Any) -> None:
    json.dump({"error": code, **extra}, sys.stderr, ensure_ascii=False)
    sys.stderr.write("\n")
    sys.exit(2)


_LISTING_CACHE: dict[str, pd.DataFrame] = {}


def _listing(market: str = "KRX") -> pd.DataFrame:
    key = market.upper()
    if key not in _LISTING_CACHE:
        _LISTING_CACHE[key] = fdr.StockListing(key)
    return _LISTING_CACHE[key]


# ---- commands -------------------------------------------------------------


def cmd_ticker(args: argparse.Namespace) -> None:
    q = args.query.strip()
    df = _listing("KRX")
    if q.isdigit() and len(q) == 6:
        row = df[df["Code"] == q]
        if row.empty:
            _fail("ticker_not_found", input=q)
        r = row.iloc[0]
        _print_json(
            {
                "ticker": q,
                "name": r.get("Name"),
                "market": r.get("Market"),
                "isin": r.get("ISU_CD"),
            }
        )
        return
    row = df[df["Name"] == q]
    if row.empty:
        _fail("ticker_not_found", input=q)
    r = row.iloc[0]
    _print_json(
        {
            "ticker": r["Code"],
            "name": r["Name"],
            "market": r.get("Market"),
            "isin": r.get("ISU_CD"),
        }
    )


def cmd_search(args: argparse.Namespace) -> None:
    q = args.query.strip()
    df = _listing("KRX")
    hits = df[df["Name"].str.contains(q, na=False, case=False)][
        ["Code", "Name", "Market", "Marcap"]
    ]
    if args.top:
        hits = hits.head(args.top)
    _emit(hits, args.csv)


def cmd_list(args: argparse.Namespace) -> None:
    df = _listing(args.market)
    cols = [
        c
        for c in ["Code", "Name", "Market", "Dept", "Close", "Marcap", "Stocks", "Symbol", "Industry"]
        if c in df.columns
    ]
    df = df[cols] if cols else df
    if args.top:
        df = df.head(args.top)
    _emit(df, args.csv)


def cmd_ohlcv(args: argparse.Namespace) -> None:
    start, end = _resolve_range(args)
    df = fdr.DataReader(args.ticker, start, end)
    _emit(df, args.csv)


def cmd_snapshot(args: argparse.Namespace) -> None:
    listing = _listing("KRX")
    row = listing[listing["Code"] == args.ticker]
    if row.empty:
        _fail("ticker_not_found", input=args.ticker)
    r = row.iloc[0]
    _print_json(
        {
            "ticker": args.ticker,
            "name": r.get("Name"),
            "market": r.get("Market"),
            "close": r.get("Close"),
            "change": r.get("Changes"),
            "change_pct": r.get("ChagesRatio"),
            "open": r.get("Open"),
            "high": r.get("High"),
            "low": r.get("Low"),
            "volume": r.get("Volume"),
            "amount": r.get("Amount"),
            "marcap": r.get("Marcap"),
            "shares": r.get("Stocks"),
        }
    )


def cmd_marketcap(args: argparse.Namespace) -> None:
    df = _listing(args.market)
    if "Marcap" in df.columns:
        df = df.sort_values("Marcap", ascending=False)
    cols = [c for c in ["Code", "Name", "Market", "Close", "Marcap", "Stocks"] if c in df.columns]
    df = df[cols] if cols else df
    if args.top:
        df = df.head(args.top)
    _emit(df, args.csv)


def cmd_index(args: argparse.Namespace) -> None:
    start, end = _resolve_range(args)
    df = fdr.DataReader(args.code, start, end)
    _emit(df, args.csv)


def cmd_index_list(_args: argparse.Namespace) -> None:
    # Curated list — FDR doesn't expose a KRX index catalogue directly.
    _print_json(
        [
            {"code": "KS11", "name": "KOSPI"},
            {"code": "KQ11", "name": "KOSDAQ"},
            {"code": "KS200", "name": "KOSPI 200"},
            {"code": "KRX100", "name": "KRX 100"},
            {"code": "KSM", "name": "KOSDAQ 150"},
            {"code": "DJI", "name": "Dow Jones Industrial Average"},
            {"code": "IXIC", "name": "NASDAQ Composite"},
            {"code": "US500", "name": "S&P 500"},
            {"code": "N225", "name": "Nikkei 225"},
            {"code": "SSEC", "name": "Shanghai Composite"},
        ]
    )


# ---- argparse -------------------------------------------------------------


_MARKETS = ["KRX", "KOSPI", "KOSDAQ", "KONEX", "ETF/KR"]


def _add_range_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--start", help="start date (YYYYMMDD or YYYY-MM-DD)")
    p.add_argument("--end", help="end date (default: today)")
    p.add_argument("--days", type=int, help="last N days ending today")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="krx", description="Korean Exchange data CLI")
    p.add_argument("--csv", action="store_true", help="emit CSV instead of JSON")
    sub = p.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("ticker", help="resolve ticker ↔ company name")
    t.add_argument("query", help="6-digit ticker or exact company name")
    t.set_defaults(func=cmd_ticker)

    s = sub.add_parser("search", help="substring search by company name")
    s.add_argument("query")
    s.add_argument("--top", type=int, default=20)
    s.set_defaults(func=cmd_search)

    lst = sub.add_parser("list", help="list tickers in a market")
    lst.add_argument("--market", default="KRX", choices=_MARKETS)
    lst.add_argument("--top", type=int)
    lst.set_defaults(func=cmd_list)

    o = sub.add_parser("ohlcv", help="OHLCV for one ticker")
    o.add_argument("ticker", help="6-digit KRX ticker, e.g. 005930")
    _add_range_args(o)
    o.set_defaults(func=cmd_ohlcv)

    sn = sub.add_parser("snapshot", help="latest-close snapshot for one ticker")
    sn.add_argument("ticker")
    sn.set_defaults(func=cmd_snapshot)

    mc = sub.add_parser("marketcap", help="market-cap ranking")
    mc.add_argument("--market", default="KRX", choices=_MARKETS)
    mc.add_argument("--top", type=int, default=50)
    mc.set_defaults(func=cmd_marketcap)

    i = sub.add_parser("index", help="index OHLCV by code (KS11=KOSPI, KQ11=KOSDAQ, KS200, KRX100…)")
    i.add_argument("code")
    _add_range_args(i)
    i.set_defaults(func=cmd_index)

    il = sub.add_parser("index-list", help="common index codes")
    il.set_defaults(func=cmd_index_list)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        args.func(args)
        return 0
    except SystemExit:
        raise
    except Exception as exc:  # noqa: BLE001
        json.dump(
            {"error": "upstream_error", "message": str(exc), "type": type(exc).__name__},
            sys.stderr,
            ensure_ascii=False,
        )
        sys.stderr.write("\n")
        return 3


if __name__ == "__main__":
    sys.exit(main())
