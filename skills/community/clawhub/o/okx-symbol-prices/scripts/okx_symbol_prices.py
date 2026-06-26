import argparse
import datetime as _dt
import json
import sys
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional, Tuple

import requests


OKX_API_BASE = "https://www.okx.com"


@dataclass(frozen=True)
class Ticker:
    inst_id: str
    base: str
    quote: str
    last: float
    change_pct_24h: float


def _now_local_str() -> str:
    return _dt.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S%z")


def _get_json(session: requests.Session, url: str, timeout_s: float) -> Dict[str, Any]:
    r = session.get(
        url,
        timeout=timeout_s,
        headers={
            "User-Agent": "okx-symbol-prices/1.0",
            "Accept": "application/json, text/plain, */*",
        },
    )
    r.raise_for_status()
    return r.json()


def _parse_inst_id_spot(inst_id: str) -> Optional[Tuple[str, str]]:
    parts = inst_id.split("-")
    if len(parts) != 2:
        return None
    return parts[0], parts[1]


def _safe_float(v: Any, default: float = 0.0) -> float:
    try:
        return float(v)
    except Exception:
        return default


def fetch_spot_ticker(session: requests.Session, inst_id: str, timeout_s: float) -> Optional[Ticker]:
    url = f"{OKX_API_BASE}/api/v5/market/ticker?instId={inst_id}"
    j = _get_json(session, url, timeout_s=timeout_s)
    if str(j.get("code", "")) not in ("0", "00000", ""):
        raise RuntimeError(f"OKX error: code={j.get('code')} msg={j.get('msg')}")
    data = j.get("data") or []
    if not data:
        return None
    row = data[0]
    got_inst_id = str(row.get("instId", inst_id))
    parsed = _parse_inst_id_spot(got_inst_id)
    if not parsed:
        return None
    base, quote = parsed
    last = _safe_float(row.get("last"))
    open_24h = _safe_float(row.get("open24h"))
    change_pct_24h = ((last - open_24h) / open_24h * 100.0) if open_24h > 0 else 0.0
    if last <= 0:
        return None
    return Ticker(
        inst_id=got_inst_id,
        base=base,
        quote=quote,
        last=last,
        change_pct_24h=change_pct_24h,
    )


def _fmt_price_usd(price: float) -> str:
    decimals = 2
    if price < 1:
        decimals = 8
    if price < 0.01:
        decimals = 10
    if price < 0.0001:
        decimals = 12
    s = f"{price:,.{decimals}f}".rstrip("0").rstrip(".")
    return f"${s}"


def main() -> int:
    ap = argparse.ArgumentParser(description="One-shot OKX spot prices for specified symbols (USD display).")
    ap.add_argument("--symbols", type=str, required=True, help="Comma-separated base symbols, e.g. BTC,ETH,SOL")
    ap.add_argument("--timeout", type=float, default=10.0, help="HTTP timeout seconds (default: 10)")
    ap.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    args = ap.parse_args()

    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    if not symbols:
        print("symbols is empty", file=sys.stderr)
        return 2

    with requests.Session() as s:
        results: List[Tuple[str, Optional[Ticker]]] = []
        for base in symbols:
            picked: Optional[Ticker] = None
            for quote in ("USDT", "USDC", "USD"):
                inst_id = f"{base}-{quote}"
                try:
                    t = fetch_spot_ticker(s, inst_id=inst_id, timeout_s=args.timeout)
                except Exception:
                    t = None
                if t is not None:
                    picked = t
                    break
            results.append((base, picked))

        if args.format == "json":
            payload: List[Dict[str, Any]] = []
            for base, t in results:
                if t is None:
                    payload.append(
                        {
                            "symbol": base,
                            "okx": None,
                            "price_usd_display": None,
                            "chg24h_pct": None,
                            "timestamp": _now_local_str(),
                        }
                    )
                else:
                    payload.append(
                        {
                            "symbol": base,
                            "okx": asdict(t),
                            "price_usd_display": _fmt_price_usd(t.last),
                            "chg24h_pct": t.change_pct_24h,
                            "timestamp": _now_local_str(),
                        }
                    )
            print(json.dumps(payload, ensure_ascii=False))
            return 0

        print(f"[{_now_local_str()}] OKX prices (USD display)")
        for base, t in results:
            if t is None:
                print(f"- {base}: N/A (no USDT/USDC/USD spot ticker found on OKX)")
            else:
                print(f"- {t.base}/{t.quote}: {_fmt_price_usd(t.last)} (instId={t.inst_id}, chg24h={t.change_pct_24h:+.2f}%)")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())

