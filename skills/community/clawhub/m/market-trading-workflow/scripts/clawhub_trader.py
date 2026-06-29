"""ClawHub trading workflow script.

Conservative defaults:
- dry-run by default
- runtime market discovery
- no hardcoded market ids
- refuse to trade without a fair probability estimate
"""

from __future__ import annotations

import argparse
import inspect
import json
import re
import sys
from datetime import datetime, timedelta, timezone
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

try:
    from simmer_sdk import SimmerClient
except ImportError as exc:  # pragma: no cover - user-facing dependency error
    raise SystemExit(
        "Missing dependency: simmer-sdk. Install it with `pip install -U simmer-sdk`."
    ) from exc

from team_names import CANONICAL_TEAMS, canonical_team, expand_team_query_aliases, score_team_question_match
from football_worldcup_model import market_research_snapshot


@dataclass
class MarketPick:
    market_id: str
    question: str
    current_probability: float
    venue: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Conservative ClawHub trading workflow")
    parser.add_argument("--query", help="Keyword search for market discovery")
    parser.add_argument("--tags", help="Comma-separated market tags for discovery")
    parser.add_argument("--venue", default="sim", help="Venue to trade or inspect (default: sim)")
    parser.add_argument("--market-id", help="Use a specific market id instead of discovery")
    parser.add_argument("--fair-probability", type=float, help="Your fair probability estimate for YES")
    parser.add_argument("--amount", type=float, default=10.0, help="Trade amount in Sim tokens or venue units")
    parser.add_argument("--min-edge", type=float, default=0.01, help="Minimum absolute edge required to trade (applies to paper and live equally)")
    parser.add_argument("--limit", type=int, default=20, help="Discovery result limit")
    parser.add_argument("--sort", default="volume", help="Discovery sort (default: volume)")
    parser.add_argument("--live", action="store_true", help="Enable live trading; default is dry-run/paper")
    parser.add_argument("--scan-slate", action="store_true", help="Scan the active slate instead of trading a single market")
    parser.add_argument("--scan-window-days", type=int, default=2, help="How many days ahead to include when scanning the slate")
    parser.add_argument("--reasoning", help="Public reasoning string for the trade")
    parser.add_argument("--skill-slug", default="market-trading-workflow", help="Source tag / skill slug")
    return parser.parse_args()


def _supported_kwargs(method, kwargs: dict[str, Any]) -> dict[str, Any]:
    params = inspect.signature(method).parameters
    return {k: v for k, v in kwargs.items() if k in params and v is not None}


def _market_attr(market: Any, name: str, default: Any = None) -> Any:
    if hasattr(market, name):
        value = getattr(market, name)
        if value is not None:
            return value
    if isinstance(market, dict):
        return market.get(name, default)
    return default


def _normalize_query(text: str) -> str:
    return " ".join(text.lower().replace("-", " ").split())


# Expand the raw search string with all team aliases we know about.
def _expand_queries(raw: str) -> list[str]:
    return expand_team_query_aliases(raw)


def _market_score(question: str, candidate: str) -> int:
    return score_team_question_match(question, candidate)


def _parse_resolves_at(raw: Any) -> Optional[datetime]:
    if not raw:
        return None
    text = str(raw).strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def _extract_fixture_pair(question: str) -> Optional[tuple[str, str]]:
    text = question.strip()
    if not re.match(r"^World Cup:\s+", text, flags=re.I):
        return None
    text = re.sub(r"^World Cup:\s*", "", text, flags=re.I)
    fixture, _, tail = text.partition(" - ")
    if not fixture or not tail:
        return None
    match = re.search(r"(.+?)\s+vs\.?\s+(.+)$", fixture, flags=re.I)
    if not match:
        return None
    left = match.group(1).strip()
    right = match.group(2).strip()
    if not left or not right:
        return None
    return left, right


def scan_slate(client: SimmerClient, args: argparse.Namespace) -> int:
    query_candidates = ["World Cup"]
    markets: list[Any] = []
    seen_ids: set[str] = set()
    for q in query_candidates:
        for market in client.get_markets(status="active", limit=max(100, args.limit), q=q):
            market_id = str(_market_attr(market, "id", ""))
            if market_id and market_id in seen_ids:
                continue
            if market_id:
                seen_ids.add(market_id)
            markets.append(market)
    if not markets:
        markets = client.get_markets(status="active", limit=max(100, args.limit))
    horizon = datetime.now(timezone.utc) + timedelta(days=max(1, args.scan_window_days))
    rows = []
    for market in markets:
        question = str(_market_attr(market, "question", ""))
        resolved = _parse_resolves_at(_market_attr(market, "resolves_at"))
        if resolved is None or resolved > horizon:
            continue
        fixture = _extract_fixture_pair(question)
        if not fixture:
            continue
        left_raw, right_raw = fixture
        left = canonical_team(left_raw)
        right = canonical_team(right_raw)
        if left not in CANONICAL_TEAMS or right not in CANONICAL_TEAMS:
            continue
        rows.append({
            "question": question,
            "left": left,
            "right": right,
            "resolves_at": _market_attr(market, "resolves_at"),
            "source": _market_attr(market, "import_source"),
            "price": float(_market_attr(market, "current_probability", 0.0) or 0.0),
            "id": _market_attr(market, "id"),
        })
    print(json.dumps({"scan_window_days": args.scan_window_days, "count": len(rows), "markets": rows}, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


def discover_market(client: SimmerClient, args: argparse.Namespace) -> MarketPick:
    if args.market_id:
        ctx = client.get_market_context(args.market_id, venue=args.venue)
        return MarketPick(
            market_id=args.market_id,
            question=ctx.get("question") or args.market_id,
            current_probability=float(ctx.get("current_probability") or 0.5),
            venue=args.venue,
        )

    if not args.query and not args.tags:
        raise SystemExit("Provide --query, --tags, or --market-id for market discovery.")

    # Current SDKs may differ in which filters they expose. Build the call from
    # only the supported parameters so the skill works across deployed versions.
    query_candidates: list[str] = []
    if args.query:
        query_candidates.extend(_expand_queries(args.query))
    if args.tags and not query_candidates:
        query_candidates.extend(_expand_queries(args.tags))

    if not query_candidates and not args.tags:
        raise SystemExit("Provide --query, --tags, or --market-id for market discovery.")
    if args.tags:
        query_candidates.append(args.tags)

    seen = set()
    query_candidates = [q for q in query_candidates if not (q in seen or seen.add(q))]

    best_market = None
    best_score = -1
    for candidate in query_candidates:
        discovery_kwargs: dict[str, Any] = {"limit": args.limit}
        discovery_kwargs["q"] = candidate
        if args.venue:
            discovery_kwargs["venue"] = args.venue
        if args.sort:
            discovery_kwargs["sort"] = args.sort
        if args.tags:
            discovery_kwargs["tags"] = args.tags

        markets = client.get_markets(**_supported_kwargs(client.get_markets, discovery_kwargs))
        if not markets:
            continue
        for market in markets:
            question = str(_market_attr(market, "question", ""))
            score = _market_score(question, args.query or args.tags or candidate)
            if score > best_score:
                best_market = market
                best_score = score
        if best_score >= 50:
            break

    if best_market is None:
        raise SystemExit("No markets found for the provided discovery filters.")

    market = best_market
    market_id = _market_attr(market, "id")
    question = _market_attr(market, "question", "(unknown question)")
    current_probability = _market_attr(market, "current_probability")
    if current_probability is None:
        current_probability = 0.5

    return MarketPick(
        market_id=str(market_id),
        question=str(question),
        current_probability=float(current_probability),
        venue=args.venue,
    )


def compute_side_and_edge(fair_probability: float, current_probability: float) -> tuple[str, float]:
    edge_yes = fair_probability - current_probability
    if edge_yes >= 0:
        return "yes", edge_yes
    return "no", -edge_yes


def stake_multiplier(fair_probability: float) -> float:
    if 0.30 <= fair_probability < 0.45:
        return 0.5
    return 1.0


def main() -> int:
    args = parse_args()
    client = SimmerClient.from_env(live=args.live, venue=args.venue)

    if args.scan_slate:
        return scan_slate(client, args)

    pick = discover_market(client, args)

    if args.fair_probability is None:
        payload = {
            "decision": "pass",
            "reason": "No fair probability supplied; refusing to guess",
            "market": pick.__dict__,
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
        return 0

    if not 0.0 <= args.fair_probability <= 1.0:
        raise SystemExit("--fair-probability must be between 0 and 1.")

    side, edge = compute_side_and_edge(args.fair_probability, pick.current_probability)

    context = client.get_market_context(pick.market_id, my_probability=args.fair_probability)
    warnings = context.get("warnings") or []
    edge_info = context.get("edge") or {}
    recommendation = edge_info.get("recommendation")
    research = market_research_snapshot(context.get("market") or {})

    decision = {
        "market": pick.__dict__,
        "fair_probability": args.fair_probability,
        "model_yes": round(args.fair_probability, 6),
        "model_no": round(1.0 - args.fair_probability, 6),
        "market_probability": pick.current_probability,
        "market_yes": round(pick.current_probability, 6),
        "market_no": round(1.0 - pick.current_probability, 6),
        "edge_yes": round(args.fair_probability - pick.current_probability, 6),
        "edge_abs": round(abs(args.fair_probability - pick.current_probability), 6),
        "recommendation": recommendation,
        "warnings": warnings,
        "mode": "live" if args.live else "paper",
        "research": research,
    }

    stake_factor = stake_multiplier(args.fair_probability)
    trade_amount = round(args.amount * stake_factor, 6)
    decision["stake_multiplier"] = stake_factor
    decision["requested_amount"] = args.amount
    decision["trade_amount"] = trade_amount

    if abs(args.fair_probability - pick.current_probability) < args.min_edge:
        decision["decision"] = "pass"
        decision["reason"] = "Edge below threshold"
        print(json.dumps(decision, indent=2, sort_keys=True))
        return 0

    if side == "no" and pick.current_probability > 0.75:
        decision["decision"] = "pass"
        decision["reason"] = "Selected opposite side is an extreme longshot"
        print(json.dumps(decision, indent=2, sort_keys=True))
        return 0

    if side == "yes" and pick.current_probability < 0.25:
        decision["decision"] = "pass"
        decision["reason"] = "Selected side is an extreme longshot"
        print(json.dumps(decision, indent=2, sort_keys=True))
        return 0

    if warnings:
        decision["warnings"] = warnings
        decision["warning_note"] = f"Context warnings present: {warnings}"

    if recommendation and recommendation != "TRADE":
        decision["recommendation_note"] = f"Context recommendation is {recommendation}"

    if not args.live:
        decision["decision"] = "paper-trade"
        decision["action"] = "submitted"
        decision["side"] = side
        decision["amount"] = trade_amount
        decision["reasoning"] = args.reasoning or f"Model yes {args.fair_probability:.3f} / no {1.0 - args.fair_probability:.3f} vs market yes {pick.current_probability:.3f} / no {1.0 - pick.current_probability:.3f}"
        result = client.trade(
            market_id=pick.market_id,
            side=side,
            amount=trade_amount,
            venue=args.venue,
            reasoning=decision["reasoning"],
            source=f"clawhub:{args.skill_slug}",
        )
        decision["result"] = {
            "success": getattr(result, "success", None),
            "trade_id": getattr(result, "trade_id", None),
            "fill_status": getattr(result, "fill_status", None),
            "shares_bought": getattr(result, "shares_bought", None),
            "shares_sold": getattr(result, "shares_sold", None),
            "shares_filled": getattr(result, "shares_filled", None),
            "cost": getattr(result, "cost", None),
            "warnings": getattr(result, "warnings", None),
        }
        print(json.dumps(decision, indent=2, sort_keys=True))
        return 0

    result = client.trade(
        market_id=pick.market_id,
        side=side,
        amount=args.amount,
        venue=args.venue,
        reasoning=args.reasoning or f"Model yes {args.fair_probability:.3f} / no {1.0 - args.fair_probability:.3f} vs market yes {pick.current_probability:.3f} / no {1.0 - pick.current_probability:.3f}",
        source=f"clawhub:{args.skill_slug}",
    )
    decision["decision"] = "trade"
    decision["action"] = "submitted"
    decision["side"] = side
    decision["amount"] = trade_amount
    decision["result"] = {
        "success": getattr(result, "success", None),
        "trade_id": getattr(result, "trade_id", None),
        "fill_status": getattr(result, "fill_status", None),
        "shares_bought": getattr(result, "shares_bought", None),
        "shares_sold": getattr(result, "shares_sold", None),
        "shares_filled": getattr(result, "shares_filled", None),
        "cost": getattr(result, "cost", None),
        "warnings": getattr(result, "warnings", None),
    }
    print(json.dumps(decision, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
