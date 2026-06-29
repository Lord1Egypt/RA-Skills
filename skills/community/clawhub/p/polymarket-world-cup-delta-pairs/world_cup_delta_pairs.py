#!/usr/bin/env python3
"""
Polymarket World Cup Delta Pairs

Inspired by @zETHerka:
- Pair "NO team advances" with "YES team wins World Cup" on the same team.
- Structure seeks mispricing between related markets.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
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
    "scan_limit": {"env": "SIMMER_WCDP_SCAN_LIMIT", "default": 700, "type": int, "help": "Markets to scan"},
    "import_source": {"env": "SIMMER_WCDP_IMPORT_SOURCE", "default": "polymarket", "type": str, "help": "Market source"},
    "team_universe": {"env": "SIMMER_WCDP_TEAM_UNIVERSE", "default": "Brazil,France,England,Argentina,Spain,Germany,Portugal,Netherlands,Sweden,Mexico,USA,Japan,Morocco,Croatia,Uruguay", "type": str, "help": "Comma-separated teams to query for pairing"},
    "min_advance_yes": {"env": "SIMMER_WCDP_MIN_ADV_YES", "default": 0.20, "type": float, "help": "Min advance YES price"},
    "max_advance_yes": {"env": "SIMMER_WCDP_MAX_ADV_YES", "default": 0.75, "type": float, "help": "Max advance YES price"},
    "min_winner_yes": {"env": "SIMMER_WCDP_MIN_WIN_YES", "default": 0.002, "type": float, "help": "Min winner YES price"},
    "max_winner_yes": {"env": "SIMMER_WCDP_MAX_WIN_YES", "default": 0.35, "type": float, "help": "Max winner YES price"},
    "winner_reprice_boost": {"env": "SIMMER_WCDP_REPRICE_BOOST", "default": 0.10, "type": float, "help": "Expected winner repricing after group advance"},
    "min_settle_edge": {"env": "SIMMER_WCDP_MIN_SETTLE_EDGE", "default": 0.02, "type": float, "help": "Min fail-to-advance scenario edge"},
    "min_cross_gap": {"env": "SIMMER_WCDP_MIN_CROSS_GAP", "default": 0.20, "type": float, "help": "Require advance_yes - winner_yes to exceed this gap"},
    "min_reprice_edge": {"env": "SIMMER_WCDP_MIN_REPRICE_EDGE", "default": -0.35, "type": float, "help": "Min advance+reprice scenario edge"},
    "max_spread": {"env": "SIMMER_WCDP_MAX_SPREAD", "default": 0.06, "type": float, "help": "Max acceptable spread"},
    "max_slippage_pct": {"env": "SIMMER_WCDP_MAX_SLIPPAGE", "default": 0.10, "type": float, "help": "Max acceptable slippage"},
    "per_leg_usd": {"env": "SIMMER_WCDP_PER_LEG_USD", "default": 4.0, "type": float, "help": "USD per leg (pair uses 2x)"},
    "daily_budget_usd": {"env": "SIMMER_WCDP_DAILY_BUDGET", "default": 30.0, "type": float, "help": "Daily spend cap"},
    "max_pairs_per_run": {"env": "SIMMER_WCDP_MAX_PAIRS", "default": 2, "type": int, "help": "Max pair entries per run"},
    "cooldown_hours": {"env": "SIMMER_WCDP_COOLDOWN_H", "default": 24, "type": int, "help": "Per-team cooldown"},
}

cfg = load_config(CONFIG_SCHEMA, __file__, slug="polymarket-world-cup-delta-pairs")

SKILL_SLUG = "polymarket-world-cup-delta-pairs"
TRADE_SOURCE = "sdk:world-cup-delta-pairs"
BASE = Path(__file__).parent
SPEND_FILE = BASE / "daily_spend.json"
COOLDOWN_FILE = BASE / "cooldown_state.json"

_client = None


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


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
            raise SystemExit(1)
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
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}", "Accept": "application/json"})
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


def parse_list_csv(s: str) -> List[str]:
    return [x.strip() for x in str(s).split(",") if x.strip()]


def discover_markets(client) -> List:
    # Prefer explicit World Cup tag discovery so results are stable regardless of
    # default API sort order/caps for generic market scans.
    limit = max(1, min(int(cfg["scan_limit"]), 100))
    base: List = []
    try:
        base = client.get_markets(
            status="active",
            import_source=str(cfg["import_source"]),
            tags="world-cup",
            limit=limit,
        )
    except TypeError:
        # Older SDKs may not yet support tags=... on get_markets.
        base = client.get_markets(status="active", import_source=str(cfg["import_source"]), limit=limit)

    queries = [
        "World Cup winner",
        "2026 FIFA World Cup winner",
        "advance to knockout",
        "advance from group",
        "reach knockout stage",
    ]
    for team in parse_list_csv(cfg["team_universe"]):
        queries.append(f"Will {team} advance to the knockout stages at the 2026 FIFA World Cup")
        queries.append(f"Will {team} win the 2026 FIFA World Cup")

    extra: List[SimpleNamespace] = []
    for q in queries:
        extra.extend(api_market_search(q, int(cfg["scan_limit"])))

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


def norm_team(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = s.lower().strip()
    s = re.sub(r"\b(the|fc|national team)\b", "", s)
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def extract_winner_team(question: str) -> Optional[str]:
    q = question.lower()
    pats = [
        r"will\s+(.+?)\s+win\s+the\s+2026\s+fifa\s+world\s+cup",
        r"will\s+(.+?)\s+win\s+the\s+world\s+cup",
        r"(.+?)\s+to\s+win\s+the\s+2026\s+fifa\s+world\s+cup",
    ]
    for p in pats:
        m = re.search(p, q)
        if m:
            return m.group(1).strip(" ?!.,")
    return None


def extract_advance_team(question: str) -> Optional[str]:
    q = question.lower()
    pats = [
        r"will\s+(.+?)\s+advance\s+to\s+the\s+knockout",
        r"will\s+(.+?)\s+advance\s+from\s+group",
        r"will\s+(.+?)\s+reach\s+the\s+knockout",
    ]
    for p in pats:
        m = re.search(p, q)
        if m:
            return m.group(1).strip(" ?!.,")
    return None


def is_winner_market(question: str) -> bool:
    q = question.lower()
    return (("world cup" in q or "fifa" in q) and "2026" in q and ("winner" in q or "win the" in q))


def is_advance_market(question: str) -> bool:
    q = question.lower()
    return ("2026" in q and ("advance" in q or "knockout" in q) and ("world cup" in q or "fifa" in q))


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


def yes_price_from_context(ctx: dict, market_obj) -> Optional[float]:
    m = (ctx or {}).get("market") or {}
    for k in ("best_ask_yes", "ask_yes", "bestAskYes", "best_ask"):
        v = m.get(k)
        if v is not None:
            try:
                p = float(v)
                if 0.0 < p < 1.0:
                    return p
            except Exception:
                pass
    try:
        p = float(getattr(market_obj, "current_probability", 0.0) or 0.0)
        if 0.0 < p < 1.0:
            return p
    except Exception:
        pass
    return None


def safe_spread(ctx: dict, market_obj) -> Optional[float]:
    m = (ctx or {}).get("market") or {}
    try:
        if m.get("spread") is not None:
            return float(m.get("spread"))
    except Exception:
        pass
    try:
        s = float(getattr(market_obj, "spread", 0.0) or 0.0)
        if s > 0:
            return s
    except Exception:
        pass
    return None


def max_slippage_pct(ctx: dict) -> float:
    analysis = (ctx or {}).get("analysis") or {}
    slip = analysis.get("slippage")
    if not isinstance(slip, dict):
        return 0.0
    vals = []
    for k in ("buy_yes", "buy_no", "sell_yes", "sell_no"):
        v = slip.get(k)
        if isinstance(v, dict) and v.get("percent") is not None:
            try:
                vals.append(float(v.get("percent")))
            except Exception:
                pass
    return max(vals) if vals else 0.0


def build_pairs(markets: List) -> List[dict]:
    winners: Dict[str, SimpleNamespace] = {}
    advances: Dict[str, SimpleNamespace] = {}

    for m in markets:
        q = getattr(m, "question", "")
        if is_winner_market(q):
            t = extract_winner_team(q)
            if t:
                winners[norm_team(t)] = m
        if is_advance_market(q):
            t = extract_advance_team(q)
            if t:
                advances[norm_team(t)] = m

    pairs = []
    for tkey, w in winners.items():
        a = advances.get(tkey)
        if not a:
            continue
        pairs.append({"team": tkey.title(), "winner": w, "advance": a})
    return pairs


def discovery_debug(markets: List) -> dict:
    team_set = {norm_team(t) for t in parse_list_csv(cfg["team_universe"]) }
    winner_like = 0
    advance_like = 0
    winner_team_hits = set()
    advance_team_hits = set()

    for m in markets:
        q = getattr(m, "question", "")
        if is_winner_market(q):
            winner_like += 1
            wt = extract_winner_team(q)
            if wt:
                n = norm_team(wt)
                if n in team_set:
                    winner_team_hits.add(n)
        if is_advance_market(q):
            advance_like += 1
            at = extract_advance_team(q)
            if at:
                n = norm_team(at)
                if n in team_set:
                    advance_team_hits.add(n)

    return {
        "markets": len(markets),
        "winner_like": winner_like,
        "advance_like": advance_like,
        "winner_team_hits": len(winner_team_hits),
        "advance_team_hits": len(advance_team_hits),
        "winner_teams": sorted(t.title() for t in winner_team_hits)[:10],
        "advance_teams": sorted(t.title() for t in advance_team_hits)[:10],
    }


def run(live: bool, venue: str, quiet: bool, positions_only: bool, use_safeguards: bool) -> int:
    client = get_client(live=live, venue=venue)

    if positions_only:
        positions = get_positions(client, venue)
        tagged = [p for p in positions if TRADE_SOURCE in (p.get("sources") or [])]
        print(json.dumps(tagged, indent=2))
        return 0

    spend = load_daily_spend()
    cooldown = load_json(COOLDOWN_FILE, {})
    tnow = now_utc().timestamp()

    markets = discover_markets(client)
    pairs = build_pairs(markets)
    dbg = discovery_debug(markets)

    if not quiet:
        print("🧩 World Cup Delta Pairs")
        print(f"scanned={len(markets)} candidate_pairs={len(pairs)}")
        print(
            "discovery_debug: "
            f"markets={dbg['markets']} winner_like={dbg['winner_like']} advance_like={dbg['advance_like']} "
            f"winner_team_hits={dbg['winner_team_hits']} advance_team_hits={dbg['advance_team_hits']}"
        )
        if dbg["winner_teams"]:
            print(f"winner_team_samples={', '.join(dbg['winner_teams'])}")
        if dbg["advance_teams"]:
            print(f"advance_team_samples={', '.join(dbg['advance_teams'])}")

    ranked = []
    for pair in pairs:
        team = pair["team"]
        w = pair["winner"]
        a = pair["advance"]

        ctx_w = client.get_market_context(w.id, venue=venue) or {}
        ctx_a = client.get_market_context(a.id, venue=venue) or {}

        if use_safeguards:
            ok_w, _ = check_context_safeguards(ctx_w)
            ok_a, _ = check_context_safeguards(ctx_a)
            if not ok_w or not ok_a:
                continue

        spread_w = safe_spread(ctx_w, w)
        spread_a = safe_spread(ctx_a, a)
        slip = max(max_slippage_pct(ctx_w), max_slippage_pct(ctx_a))
        if spread_w is not None and spread_w > float(cfg["max_spread"]):
            continue
        if spread_a is not None and spread_a > float(cfg["max_spread"]):
            continue
        if slip > float(cfg["max_slippage_pct"]):
            continue

        winner_yes = yes_price_from_context(ctx_w, w)
        advance_yes = yes_price_from_context(ctx_a, a)
        if winner_yes is None or advance_yes is None:
            continue

        if not (float(cfg["min_winner_yes"]) <= winner_yes <= float(cfg["max_winner_yes"])):
            continue
        if not (float(cfg["min_advance_yes"]) <= advance_yes <= float(cfg["max_advance_yes"])):
            continue

        no_advance_price = 1.0 - advance_yes
        pair_cost = no_advance_price + winner_yes

        settle_edge = 1.0 - pair_cost
        repriced_winner = min(0.95, winner_yes + float(cfg["winner_reprice_boost"]))
        reprice_edge = repriced_winner - pair_cost
        cross_gap = advance_yes - winner_yes

        if settle_edge < float(cfg["min_settle_edge"]):
            continue
        if cross_gap < float(cfg["min_cross_gap"]):
            continue
        if reprice_edge < float(cfg["min_reprice_edge"]):
            continue

        score = min(settle_edge, max(reprice_edge, 0.0)) + (cross_gap * 0.25)
        ranked.append({
            "team": team,
            "winner": w,
            "advance": a,
            "winner_yes": winner_yes,
            "advance_yes": advance_yes,
            "pair_cost": pair_cost,
            "settle_edge": settle_edge,
            "reprice_edge": reprice_edge,
            "cross_gap": cross_gap,
            "score": score,
        })

    ranked.sort(key=lambda x: x["score"], reverse=True)

    placed = []
    run_spent = 0.0

    for item in ranked:
        if len(placed) >= int(cfg["max_pairs_per_run"]):
            break

        team_key = norm_team(item["team"])
        last = float(cooldown.get(team_key, 0))
        if tnow - last < float(cfg["cooldown_hours"]) * 3600:
            continue

        leg = float(cfg["per_leg_usd"])
        pair_spend = leg * 2
        if spend["spent"] + run_spent + pair_spend > float(cfg["daily_budget_usd"]):
            continue

        w = item["winner"]
        a = item["advance"]

        note_base = (
            f"WCDP pair team={item['team']} cost={item['pair_cost']:.3f} "
            f"settle_edge={item['settle_edge']:.3f} reprice_edge={item['reprice_edge']:.3f}"
        )

        if live:
            r1 = client.trade(
                market_id=a.id,
                side="no",
                amount=leg,
                action="buy",
                venue=venue,
                reasoning=note_base + " | leg=no-advance",
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                allow_rebuy=False,
                signal_data={
                    "team": item["team"],
                    "leg": "no_advance",
                    "advance_yes": round(item["advance_yes"], 5),
                },
            )
            ok1 = bool(getattr(r1, "success", False))
            oid1 = getattr(r1, "order_id", None)

            r2 = client.trade(
                market_id=w.id,
                side="yes",
                amount=leg,
                action="buy",
                venue=venue,
                reasoning=note_base + " | leg=yes-winner",
                source=TRADE_SOURCE,
                skill_slug=SKILL_SLUG,
                allow_rebuy=False,
                signal_data={
                    "team": item["team"],
                    "leg": "yes_winner",
                    "winner_yes": round(item["winner_yes"], 5),
                    "pair_cost": round(item["pair_cost"], 5),
                    "settle_edge": round(item["settle_edge"], 5),
                    "reprice_edge": round(item["reprice_edge"], 5),
                    "cross_gap": round(item["cross_gap"], 5),
                },
            )
            ok2 = bool(getattr(r2, "success", False))
            oid2 = getattr(r2, "order_id", None)

            ok = ok1 and ok2
        else:
            ok = True
            oid1 = "dry-run"
            oid2 = "dry-run"

        if ok:
            run_spent += pair_spend
            cooldown[team_key] = tnow
            placed.append(
                {
                    "team": item["team"],
                    "pair_cost": round(item["pair_cost"], 3),
                    "settle_edge": round(item["settle_edge"], 3),
                    "reprice_edge": round(item["reprice_edge"], 3),
                    "cross_gap": round(item["cross_gap"], 3),
                    "amount_per_leg": leg,
                    "order_no_advance": oid1,
                    "order_winner": oid2,
                }
            )

    if live:
        spend["spent"] = round(float(spend["spent"]) + run_spent, 2)
        spend["trades"] = int(spend.get("trades", 0)) + (len(placed) * 2)
        save_json(SPEND_FILE, spend)
        save_json(COOLDOWN_FILE, cooldown)

    if placed:
        print(f"Placed {len(placed)} pair entries")
        for p in placed:
            print(
                f"- {p['team']} | pair_cost={p['pair_cost']:.3f} settle_edge={p['settle_edge']:.3f} "
                f"reprice_edge={p['reprice_edge']:.3f} cross_gap={p['cross_gap']:.3f} | ${p['amount_per_leg']:.2f}/leg"
            )
    else:
        print("No eligible pair entries this run.")

    print(f"Daily spent: ${spend['spent']:.2f} / ${float(cfg['daily_budget_usd']):.2f}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="World Cup delta-neutral pair trader")
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
