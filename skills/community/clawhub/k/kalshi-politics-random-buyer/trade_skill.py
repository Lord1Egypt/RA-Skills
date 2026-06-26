import argparse
import json
import os
import random
from dataclasses import dataclass
from typing import Any, Optional

from simmer_sdk import SimmerClient
from simmer_sdk.sizing import size_position


SKILL_SLUG = "kalshi-politics-random-buyer"
TRADE_SOURCE = f"sdk:{SKILL_SLUG}"
DEFAULT_QUERIES = [
    "election",
    "president",
    "presidency",
    "senate",
    "house",
    "governor",
    "politics",
    "campaign",
    "ballot",
    "nominee",
    "party",
]
POLITICS_KEYWORDS = {
    "election",
    "president",
    "presidency",
    "presidential",
    "senate",
    "house",
    "congress",
    "governor",
    "mayor",
    "campaign",
    "vote",
    "voter",
    "ballot",
    "democrat",
    "democratic",
    "republican",
    "nominee",
    "party",
    "candidate",
    "white house",
    "parliament",
    "prime minister",
}
_CLIENT: Optional[SimmerClient] = None


@dataclass
class Config:
    queries: list[str]
    max_markets_per_query: int
    min_price: float
    max_price: float
    fair_probability: float
    min_edge: float
    max_slippage_pct: float
    random_seed: Optional[int]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dry-run Kalshi politics random buyer")
    parser.add_argument("--live", action="store_true", help="Rejected: this template is dry-run only")
    return parser.parse_args()


def getenv_str(name: str, default: str) -> str:
    value = os.getenv(name)
    return value.strip() if value is not None else default


def getenv_float(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None:
        return default
    return float(raw)


def getenv_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    return int(raw)


def maybe_int(name: str) -> Optional[int]:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        return None
    return int(raw)


def parse_queries(raw: str) -> list[str]:
    queries = [item.strip() for item in raw.split(",") if item.strip()]
    return queries or list(DEFAULT_QUERIES)


def load_config() -> Config:
    args = parse_args()
    if args.live:
        raise SystemExit("This template is dry-run only. Remove --live.")

    min_price = getenv_float("MIN_PRICE", 0.02)
    max_price = getenv_float("MAX_PRICE", 0.98)
    if not 0.0 < min_price < max_price < 1.0:
        raise ValueError("MIN_PRICE and MAX_PRICE must satisfy 0 < MIN_PRICE < MAX_PRICE < 1")

    fair_probability = getenv_float("FAIR_PROBABILITY", 0.55)
    if not 0.0 < fair_probability < 1.0:
        raise ValueError("FAIR_PROBABILITY must be between 0 and 1")

    min_edge = getenv_float("MIN_EDGE", 0.02)
    max_markets_per_query = getenv_int("MAX_MARKETS_PER_QUERY", 50)
    if max_markets_per_query <= 0:
        raise ValueError("MAX_MARKETS_PER_QUERY must be greater than 0")

    return Config(
        queries=parse_queries(getenv_str("SEARCH_QUERIES", ",".join(DEFAULT_QUERIES))),
        max_markets_per_query=max_markets_per_query,
        min_price=min_price,
        max_price=max_price,
        fair_probability=fair_probability,
        min_edge=min_edge,
        max_slippage_pct=getenv_float("MAX_SLIPPAGE_PCT", 0.15),
        random_seed=maybe_int("RANDOM_SEED"),
    )


def get_client() -> SimmerClient:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = SimmerClient(api_key=os.environ["SIMMER_API_KEY"], venue="kalshi")
    return _CLIENT


def read_value(item: Any, key: str, default: Any = None) -> Any:
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)


def format_probability(value: float) -> str:
    return f"{value * 100:.1f}%"


def format_amount(value: float) -> str:
    return f"${value:.2f}"


def estimate_bankroll(client: SimmerClient) -> float:
    briefing = client.get_briefing()
    venue_data = (briefing.get("venues") or {}).get("kalshi") or {}
    balance = venue_data.get("balance")
    if isinstance(balance, (int, float)):
        return float(balance)
    return 100.0


def is_politics_market(question: str) -> bool:
    haystack = question.lower()
    return any(keyword in haystack for keyword in POLITICS_KEYWORDS)


def unique_candidates(discovered: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for candidate in discovered:
        ticker = candidate.get("ticker")
        if not ticker or ticker in seen:
            continue
        seen.add(ticker)
        unique.append(candidate)
    return unique


def discover_candidates(client: SimmerClient, config: Config) -> list[dict[str, Any]]:
    discovered: list[dict[str, Any]] = []

    def collect(query: Optional[str], limit: int) -> None:
        nonlocal discovered
        markets = client.list_importable_markets(venue="kalshi", q=query, limit=limit)
        for market in markets:
            ticker = read_value(market, "ticker")
            question = str(read_value(market, "question", "unknown market"))
            url = read_value(market, "url")
            current_yes_price = float(read_value(market, "current_price", 0.0) or 0.0)
            if not ticker or not url:
                continue
            if not is_politics_market(question):
                continue
            if not (config.min_price <= current_yes_price <= config.max_price):
                continue
            discovered.append(
                {
                    "ticker": ticker,
                    "question": question,
                    "url": url,
                    "current_yes_price": current_yes_price,
                    "volume_value": float(read_value(market, "volume_24h", 0.0) or 0.0),
                }
            )

    for query in config.queries:
        collect(query, config.max_markets_per_query)

    if not discovered:
        collect(None, min(max(config.max_markets_per_query * 2, 50), 100))

    return unique_candidates(discovered)


def should_skip_context(context: dict[str, Any], max_slippage_pct: float) -> str | None:
    discipline = context.get("discipline") or {}
    flip_flop_warning = discipline.get("flip_flop_warning")
    if isinstance(flip_flop_warning, str) and discipline.get("warning_level") == "severe":
        return flip_flop_warning

    slippage = context.get("slippage") or {}
    spread_pct = slippage.get("spread_pct", 0) or 0
    estimates = slippage.get("estimates") or []
    worst_slippage = max((estimate.get("slippage_pct", 0) or 0) for estimate in estimates) if estimates else 0
    if spread_pct > max_slippage_pct:
        return f"spread too high: {spread_pct:.2%}"
    if worst_slippage > max_slippage_pct:
        return f"slippage too high: {worst_slippage:.2%}"

    edge = context.get("edge") or {}
    if edge.get("recommendation") in {"SKIP", "HOLD"}:
        return f"edge recommends {edge.get('recommendation')}"

    warnings = context.get("warnings") or []
    for warning in warnings:
        if "RESOLVED" in str(warning).upper():
            return str(warning)
    return None


def decide_trade(current_yes_price: float, fair_yes_probability: float, min_edge: float) -> tuple[str | None, float, float]:
    yes_edge = fair_yes_probability - current_yes_price
    no_price = 1.0 - current_yes_price
    fair_no_probability = 1.0 - fair_yes_probability
    no_edge = fair_no_probability - no_price
    if yes_edge >= min_edge and yes_edge >= no_edge:
        return "yes", current_yes_price, yes_edge
    if no_edge >= min_edge:
        return "no", no_price, no_edge
    return None, 0.0, 0.0


def ensure_market_indexed(client: SimmerClient, ticker: str, url: str, cache: dict[str, str]) -> tuple[str | None, str | None]:
    if ticker in cache:
        return cache[ticker], None

    check = client.check_market_exists(ticker=ticker)
    market_id = check.get("market_id")
    if market_id:
        cache[ticker] = market_id
        return market_id, None

    result = client.import_kalshi_market(url)
    if result.get("status") in {"imported", "already_exists"} and result.get("market_id"):
        market_id = result["market_id"]
        cache[ticker] = market_id
        return market_id, None

    return None, result.get("error") or f"import status={result.get('status')}"


def build_reasoning(question: str, side: str, market_price: float, fair_probability: float, edge: float, candidates: int) -> str:
    fair_side_probability = fair_probability if side == "yes" else 1.0 - fair_probability
    return (
        f"Random Kalshi politics template selected '{question}' from {candidates} candidate markets; "
        f"market price is {format_probability(market_price)}; fair value for {side.upper()} is "
        f"{format_probability(fair_side_probability)}; edge is {format_probability(edge)}."
    )


def build_execution_plan(
    *,
    ticker: str,
    question: str,
    market_id: str,
    side: str,
    amount: float,
    market_price: float,
    fair_probability: float,
    edge: float,
    bankroll: float,
    candidate_count: int,
    reasoning: str,
) -> dict[str, Any]:
    fair_side_probability = fair_probability if side == "yes" else 1.0 - fair_probability
    return {
        "mode": "manual-confirmation",
        "venue": "kalshi",
        "skill_slug": SKILL_SLUG,
        "ticker": ticker,
        "market_id": market_id,
        "question": question,
        "side": side,
        "max_notional_usd": round(amount, 2),
        "market_price": round(market_price, 6),
        "market_price_pct": round(market_price * 100.0, 2),
        "fair_probability": round(fair_side_probability, 6),
        "fair_probability_pct": round(fair_side_probability * 100.0, 2),
        "edge": round(edge, 6),
        "edge_pct": round(edge * 100.0, 2),
        "bankroll_usd": round(bankroll, 2),
        "candidate_count": candidate_count,
        "reasoning": reasoning,
        "manual_review_required": True,
        "checklist": [
            "Confirm the market is still active and unresolved.",
            "Confirm current price and spread still match the plan.",
            "Confirm this order does not exceed your current risk limit.",
            "Confirm you still want the proposed side and size before placing any live order manually.",
        ],
    }


def main() -> None:
    config = load_config()
    client = get_client()
    index_cache: dict[str, str] = {}
    bankroll = estimate_bankroll(client)

    print(f"skill={SKILL_SLUG} venue=kalshi live=False")
    print(f"queries={config.queries} fair_probability={config.fair_probability:.2f} min_edge={config.min_edge:.2f}")
    print(f"bankroll={format_amount(bankroll)}")

    candidates = discover_candidates(client, config)
    if not candidates:
        print("No politics market candidates matched the configured Kalshi filters.")
        return

    rng = random.Random(config.random_seed)
    shuffled = list(candidates)
    rng.shuffle(shuffled)
    print(f"candidate_pool={len(candidates)} random_seed={config.random_seed}")

    skipped: list[str] = []
    for rank, candidate in enumerate(shuffled, start=1):
        ticker = candidate["ticker"]
        question = candidate["question"]
        market_id, error = ensure_market_indexed(client, ticker, candidate["url"], index_cache)
        if not market_id:
            skipped.append(f"{ticker}: {error}")
            continue

        context = client.get_market_context(market_id, venue="kalshi", my_probability=config.fair_probability)
        skip_reason = should_skip_context(context, config.max_slippage_pct)
        if skip_reason:
            skipped.append(f"{ticker}: {skip_reason}")
            continue

        market = context.get("market") or {}
        live_yes_price = market.get("current_price")
        if live_yes_price is None:
            live_yes_price = market.get("current_probability")
        live_yes_price = float(live_yes_price if live_yes_price is not None else candidate["current_yes_price"])

        side, market_price, edge = decide_trade(live_yes_price, config.fair_probability, config.min_edge)
        if side is None:
            skipped.append(f"{ticker}: edge below threshold after context check")
            continue

        p_win = config.fair_probability if side == "yes" else 1.0 - config.fair_probability
        amount = round(float(size_position(p_win=p_win, market_price=market_price, bankroll=bankroll, min_ev=config.min_edge)), 2)
        if amount <= 0:
            skipped.append(f"{ticker}: sizing returned zero")
            continue

        reasoning = build_reasoning(question, side, market_price, config.fair_probability, edge, len(candidates))
        plan = build_execution_plan(
            ticker=ticker,
            question=question,
            market_id=market_id,
            side=side,
            amount=amount,
            market_price=market_price,
            fair_probability=config.fair_probability,
            edge=edge,
            bankroll=bankroll,
            candidate_count=len(candidates),
            reasoning=reasoning,
        )
        print(
            f"selected rank={rank} ticker={ticker} market={market_id} side={side} amount={format_amount(amount)} "
            f"price={format_probability(market_price)} edge={format_probability(edge)}"
        )
        print(f"manual-confirmation reasoning={reasoning}")
        print("execution_plan:")
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        if skipped:
            print("skipped_candidates:")
            for item in skipped[:10]:
                print(f"- {item}")
        return

    print("No randomized politics candidate passed Kalshi indexing and safeguard checks.")
    if skipped:
        print("skipped_candidates:")
        for item in skipped[:10]:
            print(f"- {item}")


if __name__ == "__main__":
    main()