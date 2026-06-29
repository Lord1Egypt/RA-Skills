#!/usr/bin/env python3
"""
Polymarket World Cup Group-Favorites Repricing

Thesis (from @airdrops_io post):
- Before tournament start, group-stage favorites can be underpriced to win outright.
- As favorites top groups, outright prices can reprice upward.
- Capture repricing into/through group stage; optional exit around knockout start.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Dict, List, Optional

from simmer_sdk.skill import get_config_path, load_config, update_config

sys.stdout.reconfigure(line_buffering=True)

VENUE_CHOICES = ["sim", "polymarket", "kalshi"]

CONFIG_SCHEMA = {
    "scan_limit": {"env": "SIMMER_WCGFR_SCAN_LIMIT", "default": 600, "type": int, "help": "Markets to scan"},
    "import_source": {"env": "SIMMER_WCGFR_IMPORT_SOURCE", "default": "polymarket", "type": str, "help": "Market source"},
    "tournament_start_utc": {"env": "SIMMER_WCGFR_TOURNAMENT_START", "default": "2026-06-11T00:00:00Z", "type": str, "help": "Entry window closes at tournament start"},
    "knockout_start_utc": {"env": "SIMMER_WCGFR_KNOCKOUT_START", "default": "2026-06-27T00:00:00Z", "type": str, "help": "Optional exit trigger"},
    "manage_exits": {"env": "SIMMER_WCGFR_MANAGE_EXITS", "default": True, "type": bool, "help": "Sell YES positions around knockout start"},
    "min_yes_price": {"env": "SIMMER_WCGFR_MIN_YES", "default": 0.05, "type": float, "help": "Ignore very long-shot outrights"},
    "max_yes_price": {"env": "SIMMER_WCGFR_MAX_YES", "default": 0.35, "type": float, "help": "Ignore already-rich outrights"},
    "base_group_boost": {"env": "SIMMER_WCGFR_BASE_BOOST", "default": 0.04, "type": float, "help": "Expected group-stage repricing boost"},
    "tier1_boost": {"env": "SIMMER_WCGFR_T1_BOOST", "default": 0.08, "type": float, "help": "Boost for top favorites"},
    "tier2_boost": {"env": "SIMMER_WCGFR_T2_BOOST", "default": 0.06, "type": float, "help": "Boost for secondary favorites"},
    "min_edge": {"env": "SIMMER_WCGFR_MIN_EDGE", "default": 0.03, "type": float, "help": "Minimum repricing edge to enter"},
    "max_spread": {"env": "SIMMER_WCGFR_MAX_SPREAD", "default": 0.05, "type": float, "help": "Skip if spread wider"},
    "max_slippage_pct": {"env": "SIMMER_WCGFR_MAX_SLIPPAGE", "default": 0.08, "type": float, "help": "Skip if slippage worse"},
    "max_position_usd": {"env": "SIMMER_WCGFR_MAX_POSITION", "default": 8.0, "type": float, "help": "Max per market"},
    "daily_budget_usd": {"env": "SIMMER_WCGFR_DAILY_BUDGET", "default": 30.0, "type": float, "help": "Daily budget"},
    "max_trades_per_run": {"env": "SIMMER_WCGFR_MAX_TRADES", "default": 3, "type": int, "help": "Max entries per run"},
    "cooldown_hours": {"env": "SIMMER_WCGFR_COOLDOWN_H", "default": 24, "type": int, "help": "Per-market cooldown"},
    "favorite_tier1": {"env": "SIMMER_WCGFR_FAVORITE_T1", "default": "Brazil,France,England,Argentina,Spain", "type": str, "help": "Top favorites"},
    "favorite_tier2": {"env": "SIMMER_WCGFR_FAVORITE_T2", "default": "Portugal,Germany,Netherlands", "type": str, "help": "Secondary favorites"},
}

cfg = load_config(CONFIG_SCHEMA, __file__, slug="polymarket-world-cup-group-favorites-repricing-clean")

SKILL_SLUG = "polymarket-world-cup-group-favorites-repricing-clean"
TRADE_SOURCE = "sdk:world-cup-group-favorites-repricing"
BASE = Path(__file__).parent
SPEND_FILE = BASE / "daily_spend.json"
COOLDOWN_FILE = BASE / "cooldown_state.json"

_client = None


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def parse_ts(s: str) -> datetime:
    return datetime.fromisoformat(str(s).replace("Z", "+00:00"))


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2))


def load_daily_spend() -> dict:
    d = now_utc().strftime("%Y-%m-%d")
    data = load_json(SPEND_FILE, {"date": d, "spent": 0.0, "trades": 0})
    if data.get("date") != d:
        data = {"date": d, "spent": 0.0, "trades": 0}
    return data


def get_client(live: bool, venue: str):
    global _client
    if _client is None:
        from simmer_sdk import SimmerClient

        key = os.environ.get("SIMMER_API_KEY")
        if not key:
            print("Error: SIMMER_API_KEY not set")
            sys.exit(1)
        _client = SimmerClient(api_key=key, venue=venue, live=live)
    return _client


def get_positions(client, venue: str) -> List[dict]:
    try:
        from dataclasses import asdict

        positions = client.get_positions(venue=venue)
        return [asdict(p) for p in positions]
    except Exception as e:
        print(f"Error fetching positions: {e}")
        return []


def api_market_search(query: str, limit: int) -> List[SimpleNamespace]:
    """Direct API search for outrights absent from snapshot feed."""
    key = os.environ.get("SIMMER_API_KEY")
    if not key:
        return []

    params = urllib.parse.urlencode(
        {
            "q": query,
            "status": "active",
            "venue": "polymarket",
            "limit": max(1, min(limit, 1000)),
        }
    )
    url = f"https://api.simmer.markets/api/sdk/markets?{params}"
    req = urllib.request.Request(
        url,
        headers={"Authorization": f"Bearer {key}", "Accept": "application/json"},
    )

    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            data = json.loads(r.read().decode())
    except Exception:
        return []

    out: List[SimpleNamespace] = []
    for m in (data.get("markets") or []):
        if not isinstance(m, dict):
            continue
        out.append(
            SimpleNamespace(
                id=m.get("id"),
                question=m.get("question", ""),
                spread=m.get("spread"),
                current_probability=m.get("current_probability"),
            )
        )
    return out


def discover_markets(client) -> List:
    base = client.get_markets(
        status="active",
        import_source=str(cfg["import_source"]),
        limit=int(cfg["scan_limit"]),
    )

    queries = [
        "win the 2026 FIFA World Cup",
        "2026 FIFA World Cup Winner",
        "World Cup winner",
    ]

    for team in parse_list_csv(cfg["favorite_tier1"]):
        queries.append(f"Will {team.title()} win the 2026 FIFA World Cup")

    extra: List[SimpleNamespace] = []
    for q in queries:
        extra.extend(api_market_search(q, limit=int(cfg["scan_limit"])))

    merged = []
    seen = set()
    for m in list(base) + extra:
        mid = getattr(m, "id", None)
        q = getattr(m, "question", "")
        if not mid or not q or mid in seen:
            continue
        seen.add(mid)
        merged.append(m)
    return merged


def check_context_safeguards(context: dict):
    if not context:
        return True, []

    reasons = []
    warnings = context.get("warnings", [])
    discipline = context.get("discipline", {})

    for warning in warnings:
        if "MARKET RESOLVED" in str(warning).upper():
            return False, ["Market already resolved"]

    warning_level = discipline.get("warning_level", "none")
    if warning_level == "severe":
        return False, [f"Severe flip-flop warning: {discipline.get('flip_flop_warning', '')}"]
    if warning_level == "mild":
        reasons.append("Mild flip-flop warning (proceed with caution)")

    return True, reasons


def is_world_cup_outright(question: str) -> bool:
    q = question.lower()
    has_wc = ("world cup" in q or "fifa" in q) and "2026" in q
    has_outright = (
        "win the world cup" in q
        or "to win the world cup" in q
        or "wins the world cup" in q
        or "win the 2026 fifa world cup" in q
        or "wins the 2026 fifa world cup" in q
        or "to win the 2026 fifa world cup" in q
        or "winner" in q
    )
    return has_wc and has_outright


def extract_team(question: str) -> Optional[str]:
    patterns = [
        r"will\s+(.+?)\s+win\s+the\s+2026\s+fifa\s+world\s+cup",
        r"will\s+(.+?)\s+win\s+the\s+world\s+cup",
        r"(.+?)\s+to\s+win\s+the\s+2026\s+fifa\s+world\s+cup",
    ]
    q = question.strip().lower()
    for p in patterns:
        m = re.search(p, q)
        if m:
            t = m.group(1).strip(" ?!.,")
            if t:
                return " ".join(w.capitalize() for w in t.split())
    return None


def parse_list_csv(s: str) -> List[str]:
    return [x.strip().lower() for x in str(s).split(",") if x.strip()]


def team_boost(team: str) -> float:
    t = team.lower()
    tier1 = set(parse_list_csv(cfg["favorite_tier1"]))
    tier2 = set(parse_list_csv(cfg["favorite_tier2"]))
    if t in tier1:
        return float(cfg["tier1_boost"])
    if t in tier2:
        return float(cfg["tier2_boost"])
    return float(cfg["base_group_boost"])


def safe_spread(ctx: dict, market_obj) -> Optional[float]:
    m = (ctx or {}).get("market") or {}
    try:
        if m.get("spread") is not None:
            return float(m.get("spread"))
    except Exception:
        pass
    try:
        s = getattr(market_obj, "spread", None)
        if s is not None:
            return float(s)
    except Exception:
        pass
    return None


def max_slippage_pct(ctx: dict) -> float:
    est = (ctx.get("slippage") or {}).get("estimates") or []
    vals = []
    for e in est:
        try:
            vals.append(float(e.get("slippage_pct", 0.0)))
        except Exception:
            pass
    return max(vals) if vals else 0.0


def get_yes_price(market_obj) -> Optional[float]:
    try:
        p = float(getattr(market_obj, "current_probability", None))
        if 0.0 < p < 1.0:
            return p
    except Exception:
        pass
    return None


def run(live: bool, venue: str, quiet: bool = False, positions_only: bool = False, use_safeguards: bool = True) -> int:
    client = get_client(live, venue)

    if positions_only:
        print(json.dumps(get_positions(client, venue), indent=2))
        return 0

    spend = load_daily_spend()
    cooldown = load_json(COOLDOWN_FILE, {})
    tnow = now_utc().timestamp()

    tournament_start = parse_ts(str(cfg["tournament_start_utc"]))
    knockout_start = parse_ts(str(cfg["knockout_start_utc"]))

    markets = discover_markets(client)
    cands = [m for m in markets if is_world_cup_outright(m.question)]

    if not quiet:
        print("🏆 World Cup Group-Favorites Repricing")
        print(f"scanned={len(markets)} candidates={len(cands)}")

    # Exit phase: close YES positions around knockout start
    if bool(cfg.get("manage_exits", True)) and now_utc() >= knockout_start:
        positions = get_positions(client, venue)
        exited = 0
        for p in positions:
            q = str(p.get("question", ""))
            if not is_world_cup_outright(q):
                continue
            shares_yes = float(p.get("shares_yes") or 0.0)
            if shares_yes <= 0:
                continue
            mid = p.get("market_id")
            if not mid:
                continue
            note = "WCGFR knockout-exit: close pre-tournament repricing position"
            if live:
                res = client.trade(
                    market_id=mid,
                    side="yes",
                    action="sell",
                    shares=shares_yes,
                    venue=venue,
                    reasoning=note,
                    source=TRADE_SOURCE,
                    skill_slug=SKILL_SLUG,
                )
                ok = bool(getattr(res, "success", False))
            else:
                ok = True
            if ok:
                exited += 1
        if not quiet:
            print(f"knockout-exit processed={exited}")
        if exited > 0:
            return 0

    # Entry phase only pre-tournament
    if now_utc() >= tournament_start:
        if not quiet:
            print("entry-window-closed: tournament has started")
        return 0

    ranked = []
    for m in cands:
        yes = get_yes_price(m)
        if yes is None:
            continue
        if yes < float(cfg["min_yes_price"]) or yes > float(cfg["max_yes_price"]):
            continue

        team = extract_team(m.question)
        if not team:
            continue

        boost = team_boost(team)
        fair = min(0.95, yes + boost)
        edge = fair - yes
        ranked.append((edge, team, yes, fair, boost, m))

    ranked.sort(key=lambda x: x[0], reverse=True)

    placed = []
    run_spent = 0.0

    for edge, team, yes, fair, boost, m in ranked:
        if len(placed) >= int(cfg["max_trades_per_run"]):
            break
        if edge < float(cfg["min_edge"]):
            continue

        mid = m.id
        last = float(cooldown.get(mid, 0))
        if tnow - last < float(cfg["cooldown_hours"]) * 3600:
            continue

        if spend["spent"] + run_spent >= float(cfg["daily_budget_usd"]):
            break

        ctx = client.get_market_context(mid, venue=venue) or {}

        if use_safeguards:
            ok_guard, reasons = check_context_safeguards(ctx)
            if not ok_guard:
                continue
            if reasons and not quiet:
                print(f"safeguard: {m.question[:64]}... -> {'; '.join(reasons)}")

        spread = safe_spread(ctx, m)
        slip = max_slippage_pct(ctx)
        if spread is not None and spread > float(cfg["max_spread"]):
            continue
        if slip > float(cfg["max_slippage_pct"]):
            continue

        amt = float(cfg["max_position_usd"])
        if spend["spent"] + run_spent + amt > float(cfg["daily_budget_usd"]):
            continue

        note = f"WCGFR pre-tournament repricing edge={edge:.3f} team={team} yes={yes:.3f} fair={fair:.3f} boost={boost:.3f}"

        if live:
            res = client.trade(
                market_id=mid,
                side="yes",
                amount=amt,
                action="buy",
                venue=venue,
                reasoning=note,
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                allow_rebuy=False,
                signal_data={
                    "team": team,
                    "yes_price": round(yes, 5),
                    "fair_yes": round(fair, 5),
                    "boost": round(boost, 5),
                    "edge": round(edge, 5),
                    "spread": None if spread is None else round(spread, 5),
                    "slippage_pct": round(slip, 5),
                    "entry_window": "pre-tournament",
                },
            )
            ok = bool(getattr(res, "success", False))
            oid = getattr(res, "order_id", None)
        else:
            ok = True
            oid = "dry-run"

        if ok:
            run_spent += amt
            cooldown[mid] = tnow
            placed.append({
                "team": team,
                "question": m.question,
                "yes": round(yes, 3),
                "fair": round(fair, 3),
                "boost": round(boost, 3),
                "edge": round(edge, 3),
                "amount": amt,
                "order_id": oid,
            })

    if live:
        spend["spent"] = round(float(spend["spent"]) + run_spent, 2)
        spend["trades"] = int(spend.get("trades", 0)) + len(placed)
        save_json(SPEND_FILE, spend)
        save_json(COOLDOWN_FILE, cooldown)

    if placed:
        print(f"Placed {len(placed)} entries")
        for p in placed:
            print(
                f"- {p['team']} | ${p['amount']:.2f} | yes={p['yes']:.3f} fair={p['fair']:.3f} "
                f"edge={p['edge']:.3f} boost={p['boost']:.3f} | {p['order_id']}"
            )
    else:
        print("No eligible entries this run.")

    print(f"Daily spent: ${spend['spent']:.2f} / ${float(cfg['daily_budget_usd']):.2f}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="World Cup group-favorites repricing trader")
    ap.add_argument("--live", action="store_true", help="Place real orders")
    ap.add_argument("--venue", choices=VENUE_CHOICES, default="polymarket", help="Trading venue")
    ap.add_argument("--positions", action="store_true", help="Show current positions and exit")
    ap.add_argument("--no-safeguards", action="store_true", help="Disable context safeguards")
    ap.add_argument("--quiet", action="store_true", help="Quiet output")
    ap.add_argument("--config", action="store_true", help="Print current config")
    ap.add_argument("--set", action="append", default=[], help="Update config key=value")
    args = ap.parse_args()

    if args.set:
        updates = {}
        for item in args.set:
            if "=" not in item:
                print(f"Invalid --set: {item}")
                return 2
            k, v = item.split("=", 1)
            k = k.strip()
            if k not in CONFIG_SCHEMA:
                print(f"Unknown config key: {k}")
                return 2
            t = CONFIG_SCHEMA[k]["type"]
            try:
                updates[k] = t(v)
            except Exception as e:
                print(f"Failed parse {k}: {e}")
                return 2
        update_config(updates, __file__)
        print(f"Updated config at {get_config_path(__file__)}")
        return 0

    if args.config:
        print(json.dumps(cfg, indent=2))
        return 0

    return run(
        live=(args.live or args.positions),
        venue=args.venue,
        quiet=args.quiet,
        positions_only=args.positions,
        use_safeguards=not args.no_safeguards,
    )


if __name__ == "__main__":
    raise SystemExit(main())
