import argparse
import os
from dataclasses import dataclass
from typing import Any, Iterable, Optional

from simmer_sdk import SimmerClient
from simmer_sdk.sizing import size_position


SKILL_SLUG = "prediction-fair-value-template"
TRADE_SOURCE = f"sdk:{SKILL_SLUG}"
_CLIENT: Optional[SimmerClient] = None


@dataclass
class Config:
    market_query: str
    fair_probability: float
    min_edge: float
    max_markets: int
    max_slippage_pct: float
    venue: str
    live: bool


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Simmer fair-value trading skill template")
    parser.add_argument("--live", action="store_true", help="Enable live trades for this run")
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


def getenv_bool(name: str, default: bool) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def load_config() -> Config:
    args = parse_args()
    venue = getenv_str("TRADING_VENUE", "sim").lower()
    if venue not in {"sim", "polymarket"}:
        raise ValueError("TRADING_VENUE must be either 'sim' or 'polymarket'")

    fair_probability = getenv_float("FAIR_PROBABILITY", 0.60)
    if not 0.0 < fair_probability < 1.0:
        raise ValueError("FAIR_PROBABILITY must be between 0 and 1")

    min_edge = getenv_float("MIN_EDGE", 0.05)
    if min_edge <= 0:
        raise ValueError("MIN_EDGE must be greater than 0")

    max_markets = getenv_int("MAX_MARKETS", 5)
    if max_markets <= 0:
        raise ValueError("MAX_MARKETS must be greater than 0")

    max_slippage_pct = getenv_float("MAX_SLIPPAGE_PCT", 0.15)
    if max_slippage_pct <= 0:
        raise ValueError("MAX_SLIPPAGE_PCT must be greater than 0")

    live = args.live or getenv_bool("SIMMER_ENABLE_LIVE", False)
    return Config(
        market_query=getenv_str("MARKET_QUERY", "bitcoin"),
        fair_probability=fair_probability,
        min_edge=min_edge,
        max_markets=max_markets,
        max_slippage_pct=max_slippage_pct,
        venue=venue,
        live=live,
    )


def get_client(venue: str) -> SimmerClient:
    global _CLIENT
    if _CLIENT is None:
        _CLIENT = SimmerClient(api_key=os.environ["SIMMER_API_KEY"], venue=venue)
    return _CLIENT


def read_value(item: Any, key: str, default: Any = None) -> Any:
    if isinstance(item, dict):
        return item.get(key, default)
    return getattr(item, key, default)


def format_probability(value: float) -> str:
    return f"{value * 100:.1f}%"


def format_amount(value: float, venue: str) -> str:
    if venue == "sim":
        return f"{value:.2f} $SIM"
    return f"${value:.2f}"


def venue_bucket(briefing: dict[str, Any], venue: str) -> dict[str, Any]:
    venues = briefing.get("venues") or {}
    bucket = venues.get(venue)
    return bucket if isinstance(bucket, dict) else {}


def estimate_bankroll(client: SimmerClient, venue: str) -> float:
    briefing = client.get_briefing()
    bucket = venue_bucket(briefing, venue)
    balance = bucket.get("balance")
    if isinstance(balance, (int, float)):
        return float(balance)

    portfolio = client.get_portfolio(venue=venue)
    direct_balance = portfolio.get("balance") if isinstance(portfolio, dict) else None
    if isinstance(direct_balance, (int, float)):
        return float(direct_balance)

    venue_data = portfolio.get(venue) if isinstance(portfolio, dict) else None
    if isinstance(venue_data, dict):
        nested_balance = venue_data.get("balance")
        if isinstance(nested_balance, (int, float)):
            return float(nested_balance)

    return 100.0


def run_auto_redeem(client: SimmerClient) -> None:
    results = client.auto_redeem()
    for result in results:
        if result.get("success"):
            print(f"redeemed market={result.get('market_id')} tx={result.get('tx_hash')}")


def iter_markets(markets: Any) -> Iterable[Any]:
    if isinstance(markets, dict) and "markets" in markets:
        value = markets["markets"]
        if isinstance(value, list):
            return value
    if isinstance(markets, list):
        return markets
    return []


def build_reasoning(question: str, side: str, market_price: float, fair_probability: float, edge: float) -> str:
    fair_side_probability = fair_probability if side == "yes" else 1.0 - fair_probability
    return (
        f"Template thesis on '{question}': market price is {format_probability(market_price)}; "
        f"my fair value for {side.upper()} is {format_probability(fair_side_probability)}; "
        f"edge is {format_probability(edge)}."
    )


def should_skip_context(context: dict[str, Any], max_slippage_pct: float) -> Optional[str]:
    trading = context.get("trading") or {}
    flip_flop_warning = trading.get("flip_flop_warning")
    if isinstance(flip_flop_warning, str) and "SEVERE" in flip_flop_warning.upper():
        return flip_flop_warning

    slippage = context.get("slippage") or {}
    slippage_pct = slippage.get("slippage_pct", 0)
    if isinstance(slippage_pct, (int, float)) and slippage_pct > max_slippage_pct:
        return f"slippage too high: {slippage_pct:.2%}"

    edge_analysis = context.get("edge_analysis") or {}
    if edge_analysis.get("recommendation") == "HOLD":
        return "edge analysis recommends HOLD"

    return None


def decide_trade(current_yes_price: float, fair_yes_probability: float, min_edge: float) -> tuple[Optional[str], float, float]:
    yes_edge = fair_yes_probability - current_yes_price
    no_price = 1.0 - current_yes_price
    fair_no_probability = 1.0 - fair_yes_probability
    no_edge = fair_no_probability - no_price

    if yes_edge >= min_edge and yes_edge >= no_edge:
        return "yes", current_yes_price, yes_edge
    if no_edge >= min_edge:
        return "no", no_price, no_edge
    return None, 0.0, 0.0


def main() -> None:
    config = load_config()
    client = get_client(config.venue)

    print(f"skill={SKILL_SLUG} venue={config.venue} live={config.live}")
    print(
        f"query={config.market_query!r} fair_probability={config.fair_probability:.2f} "
        f"min_edge={config.min_edge:.2f} max_markets={config.max_markets}"
    )

    run_auto_redeem(client)
    bankroll = estimate_bankroll(client, config.venue)
    print(f"bankroll={format_amount(bankroll, config.venue)}")

    markets = client.get_markets(q=config.market_query, status="active", limit=config.max_markets)
    seen = 0
    executed = 0

    for market in iter_markets(markets):
        seen += 1
        market_id = read_value(market, "id") or read_value(market, "market_id")
        question = read_value(market, "question", "unknown market")
        current_yes_price = float(read_value(market, "current_probability", 0.0))

        if not market_id:
            print(f"skip market without id: {question}")
            continue

        side, market_price, edge = decide_trade(
            current_yes_price=current_yes_price,
            fair_yes_probability=config.fair_probability,
            min_edge=config.min_edge,
        )
        if side is None:
            print(
                f"skip market={market_id} question={question!r} "
                f"price={format_probability(current_yes_price)} edge below threshold"
            )
            continue

        context = client.get_market_context(market_id, venue=config.venue, my_probability=config.fair_probability)
        skip_reason = should_skip_context(context, config.max_slippage_pct)
        if skip_reason:
            print(f"skip market={market_id} question={question!r} reason={skip_reason}")
            continue

        p_win = config.fair_probability if side == "yes" else 1.0 - config.fair_probability
        amount = float(
            size_position(
                p_win=p_win,
                market_price=market_price,
                bankroll=bankroll,
                min_ev=config.min_edge,
            )
        )
        if amount <= 0:
            print(f"skip market={market_id} question={question!r} sizing returned zero")
            continue

        reasoning = build_reasoning(question, side, market_price, config.fair_probability, edge)
        print(
            f"candidate market={market_id} side={side} amount={format_amount(amount, config.venue)} "
            f"market_price={format_probability(market_price)} edge={format_probability(edge)}"
        )

        if not config.live:
            print(f"dry-run trade reasoning={reasoning}")
            continue

        result = client.trade(
            market_id=market_id,
            side=side,
            amount=amount,
            source=TRADE_SOURCE,
            skill_slug=SKILL_SLUG,
            reasoning=reasoning,
        )
        executed += 1
        shares = read_value(result, "shares_bought", 0)
        print(f"executed market={market_id} shares={shares}")

    print(f"scanned={seen} executed={executed}")


if __name__ == "__main__":
    main()