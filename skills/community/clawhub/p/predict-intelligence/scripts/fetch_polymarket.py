#!/usr/bin/env python3
"""
Polymarket Data Fetcher
Search for active prediction markets related to a geopolitical query.
Returns event-level data (with multi-option support) as JSON.
"""

import argparse
import json
import re
import sys

try:
    import requests
except ImportError:
    sys.exit("Missing dependency: pip install requests")

GAMMA_API = "https://gamma-api.polymarket.com"


def _word_score(terms: list, text: str) -> int:
    words = set(re.findall(r'[a-z0-9]+', text.lower()))
    return sum(1 for t in terms if t in words)


def _parse_vol(obj: dict) -> float:
    v = obj.get("volume") or obj.get("volumeNum") or "0"
    try:
        return float(str(v).replace(",", "").replace("$", ""))
    except ValueError:
        return 0.0


def _fmt_vol(v: float) -> str:
    if v >= 1_000_000:
        return f"${v / 1_000_000:.1f}M"
    if v >= 1_000:
        return f"${v / 1_000:.0f}K"
    return f"${v:.0f}"


def _is_settled(market: dict) -> bool:
    raw = market.get("outcomePrices", "[]")
    prices = json.loads(raw) if isinstance(raw, str) else (raw or [])
    if not prices:
        return False
    try:
        return all(float(p) >= 0.99 or float(p) <= 0.01 for p in prices if p)
    except (ValueError, TypeError):
        return False


def _parse_outcomes(market: dict):
    raw_o = market.get("outcomes", "[]")
    raw_p = market.get("outcomePrices", "[]")
    outcomes = json.loads(raw_o) if isinstance(raw_o, str) else (raw_o or [])
    prices = json.loads(raw_p) if isinstance(raw_p, str) else (raw_p or [])
    result = []
    for name, price_s in zip(outcomes, prices):
        try:
            prob = round(float(price_s), 4)
        except (ValueError, TypeError):
            prob = 0
        result.append({"name": str(name), "market_prob": prob, "price": f"${prob:.2f}"})
    return result


def _build_url(event: dict) -> str:
    slug = event.get("slug") or ""
    if slug:
        return f"https://polymarket.com/event/{slug}"
    return ""


def fetch_events(query: str, limit: int = 5) -> list:
    """Fetch and format relevant Polymarket events."""
    terms = query.lower().split()
    results = []
    seen_questions = set()

    # Strategy 1: search events (for multi-market events)
    try:
        resp = requests.get(
            f"{GAMMA_API}/events",
            params={"active": "true", "closed": "false", "limit": 50,
                    "order": "volume", "ascending": "false"},
            timeout=15,
        )
        resp.raise_for_status()

        scored = []
        for ev in resp.json():
            title = (ev.get("title") or "").lower()
            desc = (ev.get("description") or "").lower()
            score = _word_score(terms, f"{title} {desc}")
            if score > 0:
                scored.append((score, _parse_vol(ev), ev))

        scored.sort(key=lambda x: (-x[0], -x[1]))

        for _, _, ev in scored:
            if len(results) >= limit:
                break
            markets = ev.get("markets") or []
            active_markets = [m for m in markets if not _is_settled(m)]

            if not active_markets:
                continue

            url = _build_url(ev)
            question = ev.get("title") or ev.get("question") or "Unknown"
            total_vol = sum(_parse_vol(m) for m in markets)

            if len(active_markets) == 1:
                # single-market event: show Yes/No
                mkt = active_markets[0]
                options = _parse_outcomes(mkt)
                q = mkt.get("question") or question
            else:
                # multi-market event: each sub-market is an option
                options = []
                for mkt in active_markets:
                    olist = _parse_outcomes(mkt)
                    yes_prob = next((o["market_prob"] for o in olist if o["name"] == "Yes"), 0)
                    name = mkt.get("groupItemTitle") or mkt.get("question") or "Option"
                    options.append({
                        "name": name,
                        "market_prob": yes_prob,
                        "price": f"${yes_prob:.2f}",
                    })
                options.sort(key=lambda o: o["market_prob"], reverse=True)
                q = question

            if q in seen_questions:
                continue
            seen_questions.add(q)

            results.append({
                "question": q,
                "url": url,
                "volume": _fmt_vol(total_vol),
                "options": options,
            })
    except Exception as e:
        print(f"[WARN] Events search failed: {e}", file=sys.stderr)

    # Strategy 2: supplement with individual markets if needed
    if len(results) < limit:
        try:
            resp = requests.get(
                f"{GAMMA_API}/markets",
                params={"active": "true", "closed": "false", "limit": 50,
                        "order": "volume", "ascending": "false"},
                timeout=15,
            )
            resp.raise_for_status()

            scored = []
            for mkt in resp.json():
                if _is_settled(mkt):
                    continue
                q = (mkt.get("question") or "").lower()
                desc = (mkt.get("description") or "").lower()
                score = _word_score(terms, f"{q} {desc}")
                if score > 0:
                    scored.append((score, _parse_vol(mkt), mkt))

            scored.sort(key=lambda x: (-x[0], -x[1]))

            for _, _, mkt in scored:
                if len(results) >= limit:
                    break
                q = mkt.get("question") or "Unknown"
                if q in seen_questions:
                    continue
                seen_questions.add(q)

                slug = mkt.get("eventSlug") or mkt.get("slug") or ""
                url = f"https://polymarket.com/event/{slug}" if slug else ""

                results.append({
                    "question": q,
                    "url": url,
                    "volume": _fmt_vol(_parse_vol(mkt)),
                    "options": _parse_outcomes(mkt),
                })
        except Exception as e:
            print(f"[WARN] Markets search failed: {e}", file=sys.stderr)

    return results[:limit]


def main():
    parser = argparse.ArgumentParser(description="Fetch Polymarket data")
    parser.add_argument("--query", required=True, help="Search keywords")
    parser.add_argument("--limit", type=int, default=5, help="Number of events")
    parser.add_argument("--output", help="Output JSON file (default: stdout)")
    args = parser.parse_args()

    data = fetch_events(args.query, args.limit)
    out = json.dumps(data, indent=2, ensure_ascii=False)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(out)
        print(f"[OK] {len(data)} events → {args.output}", file=sys.stderr)
    else:
        print(out)


if __name__ == "__main__":
    main()
