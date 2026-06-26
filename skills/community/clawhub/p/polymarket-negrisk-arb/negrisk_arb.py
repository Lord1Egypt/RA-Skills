#!/usr/bin/env python3
"""
Polymarket NegRisk Arbitrage Trader
Find multi-outcome markets where sum of prices deviates from $1.00
Execute simultaneous batch trades to lock in risk-free profit.

No signals. No AI. Just math.
"""

import os
import sys
import json
import argparse
import time
import requests
from datetime import datetime, timezone
from collections import defaultdict
from pathlib import Path

try:
    from simmer_sdk import SimmerClient
except ImportError:
    print("❌ simmer-sdk not installed. Run: pip install simmer-sdk")
    sys.exit(1)

SKILL_SLUG = "polymarket-negrisk-arb"   # Must match ClawHub slug
TRADE_SOURCE = "sdk:negrisk-arb"        # Tag for all trades

# ─── Configuration ────────────────────────────────────────────────────────────

CONFIG_FILE = Path(__file__).parent / "negrisk_config.json"
LEDGER_FILE = Path(__file__).parent / "negrisk_ledger.json"

DEFAULTS = {
    "max_yes_sum": 0.95,
    "max_no_sum": 0.95,
    "min_profit_pct": 0.03,
    "max_position_usd": 10.00,
    "max_total_usd": 50.00,
    "max_trades_per_run": 2,
    "daily_budget": 50.00,
    "min_outcomes": 3,
    "max_outcomes": 15,
    "slippage_max_pct": 0.05,
    "fee_filter": True,
    "require_simultaneous": True,
    "venue": "sim",
    "min_volume_24h": 500.0,
    "min_hours_to_resolution": 24,
    "max_position_pct_of_volume": 0.05,
}

ENV_MAP = {
    "max_yes_sum":        "SIMMER_NEGRISK_MAX_YES_SUM",
    "max_no_sum":         "SIMMER_NEGRISK_MAX_NO_SUM",
    "min_profit_pct":     "SIMMER_NEGRISK_MIN_PROFIT",
    "max_position_usd":   "SIMMER_NEGRISK_MAX_POSITION",
    "max_total_usd":      "SIMMER_NEGRISK_MAX_TOTAL",
    "max_trades_per_run": "SIMMER_NEGRISK_MAX_TRADES",
    "daily_budget":       "SIMMER_NEGRISK_DAILY_BUDGET",
    "min_outcomes":       "SIMMER_NEGRISK_MIN_OUTCOMES",
    "max_outcomes":       "SIMMER_NEGRISK_MAX_OUTCOMES",
    "slippage_max_pct":   "SIMMER_NEGRISK_SLIPPAGE",
    "fee_filter":         "SIMMER_NEGRISK_FEE_FILTER",
    "venue":              "TRADING_VENUE",
    "min_volume_24h":     "SIMMER_NEGRISK_MIN_VOLUME",
    "min_hours_to_resolution": "SIMMER_NEGRISK_MIN_HOURS",
}


def load_config():
    cfg = dict(DEFAULTS)
    if CONFIG_FILE.exists():
        try:
            cfg.update(json.loads(CONFIG_FILE.read_text()))
        except Exception:
            pass
    for key, env_var in ENV_MAP.items():
        val = os.environ.get(env_var)
        if val is not None:
            if key in ("max_yes_sum", "max_no_sum", "min_profit_pct",
                       "max_position_usd", "max_total_usd", "slippage_max_pct", "daily_budget",
                       "min_volume_24h", "max_position_pct_of_volume"):
                try:
                    cfg[key] = float(val)
                except ValueError:
                    pass
            elif key in ("max_trades_per_run", "min_outcomes", "max_outcomes"):
                try:
                    cfg[key] = int(val)
                except ValueError:
                    pass
            elif key == "fee_filter":
                cfg[key] = val.lower() in ("true", "1", "yes")
            else:
                cfg[key] = val
    return cfg


def save_config(cfg):
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))


def update_config(key, value):
    cfg = load_config()
    if key not in DEFAULTS:
        print(f"❌ Unknown config key: {key}")
        print(f"   Valid keys: {', '.join(DEFAULTS.keys())}")
        return
    original = DEFAULTS[key]
    try:
        if isinstance(original, bool):
            cfg[key] = value.lower() in ("true", "1", "yes")
        elif isinstance(original, float):
            cfg[key] = float(value)
        elif isinstance(original, int):
            cfg[key] = int(value)
        else:
            cfg[key] = value
    except ValueError:
        print(f"❌ Invalid value '{value}' for {key}")
        return
    save_config(cfg)
    print(f"✅ {key} = {cfg[key]}")


# ─── Ledger ───────────────────────────────────────────────────────────────────

def load_ledger():
    if LEDGER_FILE.exists():
        try:
            return json.loads(LEDGER_FILE.read_text())
        except Exception:
            pass
    return {"trades": [], "daily_spend": {}}


def save_ledger(ledger):
    LEDGER_FILE.write_text(json.dumps(ledger, indent=2))


def get_daily_spend(ledger):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return ledger.get("daily_spend", {}).get(today, 0.0)


def add_daily_spend(ledger, amount):
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    ledger.setdefault("daily_spend", {})
    ledger["daily_spend"][today] = ledger["daily_spend"].get(today, 0.0) + amount


# ─── Market Grouping ──────────────────────────────────────────────────────────

def group_markets_by_event(markets):
    """
    Group markets that belong to the same NegRisk event.
    Uses resolves_at + shared question tokens for reliable grouping.
    """
    events = defaultdict(list)

    for m in markets:
        q = m.get("question", "")
        resolves_at = m.get("resolves_at", "")
        tags = m.get("tags", [])

        # Skip inactive markets
        if m.get("status") != "active":
            continue

        # Better grouping: use resolves_at + first 4 words of question
        # This handles "Will X be Y?" style questions reliably
        words = q.lower().split()
        # Remove common outcome words (numbers, percentages, names at end)
        prefix_words = words[:min(5, len(words))]
        # Remove last word if it looks like an outcome (number, %, short word)
        if prefix_words and (prefix_words[-1].replace('.','').replace('%','').isdigit() 
                              or len(prefix_words[-1]) <= 3):
            prefix_words = prefix_words[:-1]
        prefix = " ".join(prefix_words)

        # Use resolves_at date only (not full timestamp) for better grouping
        resolves_date = resolves_at[:10] if resolves_at else ""

        key = f"{prefix}|{resolves_date}"
        events[key].append(m)

    # Filter: only groups with enough outcomes
    return {k: v for k, v in events.items() if len(v) >= 2}


# ─── Arbitrage Detection ──────────────────────────────────────────────────────

def check_yes_arbitrage(outcomes, cfg):
    """Check if YES prices sum below threshold."""
    yes_sum = sum(m.get("current_probability", 0) for m in outcomes)
    if yes_sum <= 0:
        return None

    cost = yes_sum
    payout = 1.0
    net = payout - cost
    profit_pct = net / cost if cost > 0 else 0

    if yes_sum < cfg["max_yes_sum"] and profit_pct >= cfg["min_profit_pct"]:
        return {
            "side": "yes",
            "sum": yes_sum,
            "cost": cost,
            "payout": payout,
            "net_profit": net,
            "profit_pct": profit_pct,
        }
    return None


def check_no_arbitrage(outcomes, cfg):
    """Check if NO prices sum below threshold."""
    no_sum = sum(1.0 - m.get("current_probability", 0) for m in outcomes)
    if no_sum <= 0:
        return None

    cost = no_sum
    payout = 1.0
    net = payout - cost
    profit_pct = net / cost if cost > 0 else 0

    if no_sum < cfg["max_no_sum"] and profit_pct >= cfg["min_profit_pct"]:
        return {
            "side": "no",
            "sum": no_sum,
            "cost": cost,
            "payout": payout,
            "net_profit": net,
            "profit_pct": profit_pct,
        }
    return None


def check_fees(outcomes, client, cfg):
    """Check all outcomes for taker fees. Returns True if safe to trade."""
    if not cfg["fee_filter"]:
        return True, {}

    fee_info = {}
    for m in outcomes:
        if m.get("is_paid", False):
            return False, {}
        fee_info[m["id"]] = 0
    return True, fee_info


# ─── Execution ────────────────────────────────────────────────────────────────

def execute_arbitrage(client, outcomes, arb, cfg, live=False, quiet=False):
    """Execute simultaneous batch trade for all outcomes."""
    side = arb["side"]

    # Build batch trade list
    trades = []
    for m in outcomes:
        if side == "yes":
            price = m.get("current_probability", 0)
        else:
            price = 1.0 - m.get("current_probability", 0)

        if price <= 0:
            continue

        # Size: equal dollar amount per outcome, capped at max_position_usd
        # Also cap at % of market volume to avoid excessive market impact
        vol = m.get("volume_24h") or 0
        vol_cap = vol * cfg.get("max_position_pct_of_volume", 0.05) if vol > 0 else cfg["max_position_usd"]
        amount = min(cfg["max_position_usd"], cfg["max_total_usd"] / len(outcomes), vol_cap)
        amount = max(amount, 0.50)  # minimum $0.50 per bucket

        trades.append({
            "market_id": m["id"],
            "side": side,
            "amount": round(amount, 2),
        })

    if not trades:
        return None

    total_cost = sum(t["amount"] for t in trades)

    if not live:
        if not quiet:
            print(f"\n  [DRY RUN] Would execute {len(trades)} trades, total ~${total_cost:.2f}")
            for t in trades:
                m = next(x for x in outcomes if x["id"] == t["market_id"])
                price = m.get("current_probability") if side == "yes" else 1.0 - m.get("current_probability", 0)
                print(f"    {side.upper()} {m['question'][-40:]:40s} @ ${price:.3f} → ${t['amount']:.2f}")
        return {"success": True, "dry_run": True, "total_cost": total_cost}

    # Execute batch
    try:

        api_key = os.environ.get("SIMMER_API_KEY")
        response = requests.post(
            "https://api.simmer.markets/api/sdk/trades/batch",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "trades": trades,
                "venue": cfg["venue"],
                "source": TRADE_SOURCE,
                "skill_slug": SKILL_SLUG,
            },
            timeout=30,
        )
        response.raise_for_status()
        result = response.json()

        if not quiet:
            success_count = sum(1 for r in result.get("results", []) if r.get("success"))
            print(f"\n  ✅ Batch executed: {success_count}/{len(trades)} filled")
            print(f"  Total cost: ${result.get('total_cost', 0):.2f}")
            if result.get("warnings"):
                for w in result["warnings"]:
                    print(f"  ⚠️  {w}")

        return result
    except Exception as e:
        if not quiet:
            print(f"\n  ❌ Batch trade failed: {e}")
        return {"success": False, "error": str(e)}


# ─── Stats ────────────────────────────────────────────────────────────────────

def show_stats():
    ledger = load_ledger()
    trades = ledger.get("trades", [])

    if not trades:
        print("No trades recorded yet. Run --live to start trading.")
        return

    total = len(trades)
    total_invested = sum(t.get("cost", 0) for t in trades)
    total_profit = sum(t.get("actual_profit", t.get("expected_profit", 0)) for t in trades)

    print(f"\n📊 NegRisk Arbitrage Stats")
    print(f"{'='*50}")
    print(f"Total events traded: {total}")
    print(f"Total invested:      ${total_invested:.2f}")
    print(f"Total profit:        ${total_profit:.2f}")
    if total_invested > 0:
        print(f"Overall ROI:         {total_profit/total_invested*100:.1f}%")

    print(f"\nDaily spend history:")
    for date, amount in sorted(ledger.get("daily_spend", {}).items())[-7:]:
        print(f"  {date}: ${amount:.2f}")


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="NegRisk Arbitrage Trader")
    parser.add_argument("--live", action="store_true", help="Execute real trades")
    parser.add_argument("--side", choices=["yes", "no"], help="Only scan one side")
    parser.add_argument("--min-profit", type=float, help="Override min profit %")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--quiet", action="store_true", help="Minimal output")
    parser.add_argument("--stats", action="store_true", help="Show stats")
    parser.add_argument("--config", action="store_true", help="Show config")
    parser.add_argument("--set", metavar="KEY=VALUE", help="Update config")
    args = parser.parse_args()

    # Handle --set
    if args.set:
        if "=" not in args.set:
            print("❌ Format: --set key=value")
            sys.exit(1)
        key, value = args.set.split("=", 1)
        update_config(key.strip(), value.strip())
        return

    # Handle --stats
    if args.stats:
        show_stats()
        return

    cfg = load_config()
    if args.min_profit:
        cfg["min_profit_pct"] = args.min_profit

    # Handle --config
    if args.config:
        print("\n⚙️  Current Configuration:")
        print(f"{'='*50}")
        for k, v in cfg.items():
            print(f"  {k:30s} {v}")
        return

    # Init client
    api_key = os.environ.get("SIMMER_API_KEY")
    if not api_key:
        print("❌ SIMMER_API_KEY not set")
        sys.exit(1)

    client = SimmerClient(api_key=api_key)
    ledger = load_ledger()

    if not args.quiet:
        print(f"\n🔢 NegRisk Arbitrage Scanner")
        print(f"{'='*50}")
        print(f"Mode: {'🔴 LIVE' if args.live else '📄 DRY RUN'}")
        print(f"Venue: {cfg['venue']}")
        print(f"\n⚙️  Configuration:")
        print(f"  Max YES sum:     ${cfg['max_yes_sum']:.2f}")
        print(f"  Max NO sum:      ${cfg['max_no_sum']:.2f}")
        print(f"  Min profit:      {cfg['min_profit_pct']*100:.1f}%")
        print(f"  Max position:    ${cfg['max_position_usd']:.2f}/bucket")
        print(f"  Daily budget:    ${cfg['daily_budget']:.2f}")

    # Check daily budget
    daily_spend = get_daily_spend(ledger)
    if daily_spend >= cfg["daily_budget"]:
        if not args.quiet:
            print(f"\n⛔ Daily budget exhausted: ${daily_spend:.2f} / ${cfg['daily_budget']:.2f}")
        return

    # Fetch markets
    if not args.quiet:
        print(f"\n🔍 Fetching active markets...")

    try:
        all_markets = []
        offset = 0
        limit = 200
        while True:
            batch = client.get_markets(status="active", limit=limit)
            if not batch:
                break
            # Convert to dicts if needed
            batch_dicts = []
            for m in batch:
                if hasattr(m, '__dict__'):
                    d = {
                        "id": m.id,
                        "question": m.question,
                        "status": m.status,
                        "current_probability": m.current_probability,
                        "resolves_at": getattr(m, 'resolves_at', None),
                        "tags": getattr(m, 'tags', []),
                        "is_paid": getattr(m, 'is_paid', False),
                        "import_source": getattr(m, 'import_source', ''),
                    }
                else:
                    d = m
                batch_dicts.append(d)
            all_markets.extend(batch_dicts)
            if len(batch) < limit:
                break
            offset += limit

    except Exception as e:
        print(f"❌ Failed to fetch markets: {e}")
        sys.exit(1)

    if not args.quiet:
        print(f"  Found {len(all_markets)} active markets")

    # Group by event
    events = group_markets_by_event(all_markets)

    if not args.quiet:
        print(f"  Grouped into {len(events)} multi-outcome events")

    # Filter by outcome count, volume and resolution time
    now = datetime.now(timezone.utc)
    min_hours = cfg.get("min_hours_to_resolution", 24)
    min_vol = cfg.get("min_volume_24h", 500.0)

    valid_events = {}
    for k, outcomes in events.items():
        # Check outcome count
        if not (cfg["min_outcomes"] <= len(outcomes) <= cfg["max_outcomes"]):
            continue
        # Check min resolution time
        too_soon = False
        for m in outcomes:
            ra = m.get("resolves_at", "")
            if ra:
                try:
                    from datetime import datetime as dt
                    resolves = dt.fromisoformat(ra.replace("Z", "+00:00"))
                    hours_left = (resolves - now).total_seconds() / 3600
                    if hours_left < min_hours:
                        too_soon = True
                        break
                except Exception:
                    pass
        if too_soon:
            continue
        # Check min volume: at least one outcome must have volume > min_vol
        has_volume = any(
            (m.get("volume_24h") or 0) >= min_vol for m in outcomes
        )
        if not has_volume:
            continue
        valid_events[k] = outcomes

    if not args.quiet:
        print(f"  {len(valid_events)} events within outcome range "
              f"({cfg['min_outcomes']}-{cfg['max_outcomes']} outcomes)")
        print(f"\n🔎 Scanning for arbitrage...")

    opportunities = []

    for event_key, outcomes in valid_events.items():
        # Check fees
        fee_ok, _ = check_fees(outcomes, client, cfg)
        if not fee_ok:
            continue

        # Check YES arbitrage
        if not args.side or args.side == "yes":
            yes_arb = check_yes_arbitrage(outcomes, cfg)
            if yes_arb:
                opportunities.append((event_key, outcomes, yes_arb))

        # Check NO arbitrage
        if not args.side or args.side == "no":
            no_arb = check_no_arbitrage(outcomes, cfg)
            if no_arb:
                opportunities.append((event_key, outcomes, no_arb))

    if not opportunities:
        if not args.quiet:
            print(f"\n  No arbitrage opportunities found.")
            print(f"  All {len(valid_events)} events are efficiently priced.")
            print(f"\n  Tips:")
            print(f"  • Lower min_profit_pct: --set min_profit_pct=0.02")
            print(f"  • Check during high-volatility events")
            print(f"  • More imported markets = more opportunities")
        return

    if not args.quiet:
        print(f"\n🎯 Opportunities Found: {len(opportunities)}")

    # JSON output
    if args.json:
        output = []
        for event_key, outcomes, arb in opportunities:
            output.append({
                "event": event_key.split("|")[0],
                "resolves_at": event_key.split("|")[1] if "|" in event_key else None,
                "side": arb["side"],
                "sum": round(arb["sum"], 4),
                "profit_pct": round(arb["profit_pct"] * 100, 2),
                "outcomes": len(outcomes),
            })
        print(json.dumps(output, indent=2))
        return

    # Process opportunities
    trades_executed = 0

    for event_key, outcomes, arb in opportunities:
        if trades_executed >= cfg["max_trades_per_run"]:
            if not args.quiet:
                print(f"\n⏹️  Max trades per run reached ({cfg['max_trades_per_run']})")
            break

        # Check daily budget
        daily_spend = get_daily_spend(ledger)
        remaining = cfg["daily_budget"] - daily_spend
        if remaining <= 0:
            if not args.quiet:
                print(f"\n⛔ Daily budget exhausted")
            break

        event_name = event_key.split("|")[0]
        resolves_at = event_key.split("|")[1] if "|" in event_key else "unknown"

        if not args.quiet:
            print(f"\n{'━'*50}")
            print(f"Event: {event_name[:60]}")
            print(f"Side: {arb['side'].upper()} arbitrage | {len(outcomes)} outcomes")
            print(f"Resolves: {resolves_at[:10] if resolves_at else 'unknown'}")
            print(f"{'━'*50}")

            # Show all outcomes
            for m in sorted(outcomes, key=lambda x: x.get("current_probability", 0), reverse=True):
                price = m.get("current_probability", 0) if arb["side"] == "yes" else 1.0 - m.get("current_probability", 0)
                print(f"  {m['question'][-45:]:45s} ${price:.3f}")

            print(f"  {'─'*50}")
            print(f"  Sum:     ${arb['sum']:.4f} (threshold: ${cfg['max_yes_sum']:.2f}) ✅")
            print(f"  Cost:    ${arb['cost']:.4f}")
            print(f"  Payout:  ${arb['payout']:.2f}")
            print(f"  Profit:  +${arb['net_profit']:.4f} ({arb['profit_pct']*100:.1f}%) ✅")

        # Execute
        result = execute_arbitrage(client, outcomes, arb, cfg, live=args.live, quiet=args.quiet)

        if result and result.get("success"):
            actual_cost = result.get("total_cost", arb["cost"])
            add_daily_spend(ledger, actual_cost)

            # Log to ledger
            ledger["trades"].append({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "event": event_name,
                "side": arb["side"],
                "outcomes": len(outcomes),
                "expected_sum": round(arb["sum"], 4),
                "expected_profit_pct": round(arb["profit_pct"] * 100, 2),
                "cost": actual_cost,
                "expected_profit": round(arb["net_profit"], 4),
                "dry_run": not args.live,
            })
            save_ledger(ledger)
            trades_executed += 1

    # Summary
    if not args.quiet:
        print(f"\n{'='*50}")
        print(f"📊 Summary:")
        print(f"  Events scanned:    {len(valid_events)}")
        print(f"  Opportunities:     {len(opportunities)}")
        print(f"  Trades executed:   {trades_executed}")
        print(f"  Daily spend:       ${get_daily_spend(ledger):.2f} / ${cfg['daily_budget']:.2f}")
        if not args.live:
            print(f"\n  Run with --live to execute real trades")


if __name__ == "__main__":
    main()
