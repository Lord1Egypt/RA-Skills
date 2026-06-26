#!/usr/bin/env python3
"""
Polymarket Valuation Divergence Trader

Trade markets where your probability model diverges from Polymarket price.
Scans active markets, calculates Kelly-sized positions based on edge.

Usage:
    python valuation_trader.py              # Dry run
    python valuation_trader.py --live       # Real trades
    python valuation_trader.py --positions  # Show positions
    python valuation_trader.py --config     # Show config

Requires:
    SIMMER_API_KEY environment variable
"""

import os
import sys
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

# Force line-buffered stdout for cron/Docker/OpenClaw visibility
sys.stdout.reconfigure(line_buffering=True)

# =============================================================================
# Configuration System (copy-paste boilerplate)
# =============================================================================

def _load_config(schema, skill_file, config_filename="config.json"):
    """Load config with priority: config.json > env vars > defaults."""
    config_path = Path(skill_file).parent / config_filename
    file_cfg = {}
    if config_path.exists():
        try:
            with open(config_path) as f:
                file_cfg = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    result = {}
    for key, spec in schema.items():
        if key in file_cfg:
            result[key] = file_cfg[key]
        elif spec.get("env") and os.environ.get(spec["env"]):
            val = os.environ.get(spec["env"])
            type_fn = spec.get("type", str)
            try:
                result[key] = type_fn(val) if type_fn != str else val
            except (ValueError, TypeError):
                result[key] = spec.get("default")
        else:
            result[key] = spec.get("default")
    return result

def _get_config_path(skill_file, config_filename="config.json"):
    return Path(skill_file).parent / config_filename

def _update_config(updates, skill_file, config_filename="config.json"):
    config_path = Path(skill_file).parent / config_filename
    existing = {}
    if config_path.exists():
        try:
            with open(config_path) as f:
                existing = json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    existing.update(updates)
    with open(config_path, "w") as f:
        json.dump(existing, f, indent=2)
    return existing

load_config = _load_config
get_config_path = _get_config_path
update_config = _update_config

# =============================================================================
# Configuration Schema
# =============================================================================

CONFIG_SCHEMA = {
    "edge_threshold": {"env": "SIMMER_VALUATION_EDGE", "default": 0.015, "type": float},
    "kelly_fraction": {"env": "SIMMER_VALUATION_KELLY", "default": 0.25, "type": float},
    "max_position_usd": {"env": "SIMMER_VALUATION_MAX_POSITION", "default": 5.00, "type": float},
    "max_trades_per_run": {"env": "SIMMER_VALUATION_MAX_TRADES", "default": 5, "type": int},
    "probability_source": {"env": "SIMMER_VALUATION_SOURCE", "default": "simmer_ai", "type": str},
}

_config = load_config(CONFIG_SCHEMA, __file__)

EDGE_THRESHOLD = _config["edge_threshold"]
KELLY_FRACTION = _config["kelly_fraction"]
MAX_POSITION_USD = _config["max_position_usd"]
MAX_TRADES_PER_RUN = _config["max_trades_per_run"]
PROBABILITY_SOURCE = _config["probability_source"]

TRADE_SOURCE = "sdk:valuation"

# =============================================================================
# SimmerClient Singleton
# =============================================================================

_client = None

def get_client(live=True):
    """Lazy-init SimmerClient singleton."""
    global _client
    if _client is None:
        try:
            from simmer_sdk import SimmerClient
        except ImportError:
            print("Error: simmer-sdk not installed. Run: pip install simmer-sdk")
            sys.exit(1)
        api_key = os.environ.get("SIMMER_API_KEY")
        if not api_key:
            print("Error: SIMMER_API_KEY environment variable not set")
            print("Get your API key from: simmer.markets/dashboard -> SDK tab")
            sys.exit(1)
        venue = os.environ.get("TRADING_VENUE", "polymarket")
        _client = SimmerClient(api_key=api_key, venue=venue)
    return _client

# =============================================================================
# Utility Functions
# =============================================================================

def fetch_json(url, headers=None):
    """Fetch JSON from URL."""
    if headers is None:
        headers = {}
    headers.setdefault("User-Agent", "SimmerValuationSkill/1.0")
    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except (HTTPError, URLError, Exception) as e:
        print(f"  ⚠️ Fetch failed: {url} — {e}")
        return None

def get_market_context(market_id):
    """Get context for a market (safeguards + position info)."""
    try:
        return get_client().get_market_context(market_id)
    except Exception as e:
        print(f"  ⚠️ Context failed: {e}")
        return None

def check_safeguards(context):
    """Check if safeguards pass. Returns (safe: bool, warnings: list)."""
    warnings = []
    if not context:
        return False, ["No context"]
    
    discipline = context.get("discipline", {})
    flip_flop = discipline.get("flip_flop_warning")
    if flip_flop in ["SEVERE", "CAUTION"]:
        warnings.append(f"flip_flop: {flip_flop}")
    
    market = context.get("market", {})
    if market.get("status") == "resolved":
        warnings.append("MARKET RESOLVED")
    
    slippage = context.get("slippage", {})
    spread_pct = slippage.get("spread_pct", 0)
    if spread_pct > 5:
        warnings.append(f"High spread: {spread_pct:.1f}%")
    
    safe = len([w for w in warnings if w in ["MARKET RESOLVED", "flip_flop: SEVERE"]]) == 0
    return safe, warnings

def execute_trade(market_id, side, amount, market_price, model_prob, edge, reasoning):
    """Execute trade via SDK with safeguards."""
    try:
        result = get_client().trade(
            market_id=market_id,
            side=side,
            amount=amount,
            source=TRADE_SOURCE,
            reasoning=reasoning
        )
        if result.success:
            return {"success": True, "trade_id": result.trade_id, "shares": result.shares_bought}
        else:
            return {"success": False, "error": "Trade returned success=False"}
    except Exception as e:
        return {"success": False, "error": str(e)}

def calculate_kelly_position(edge, market_price, bankroll, max_usd):
    """Calculate Kelly-sized position."""
    if edge <= 0:
        return 0
    
    # Kelly fraction = edge / (1 - market_price)
    kelly_raw = edge / (1 - market_price) if market_price < 1 else 0
    kelly_capped = min(kelly_raw, KELLY_FRACTION)
    
    position_size = kelly_capped * bankroll
    position_size = min(position_size, max_usd)
    
    return max(0, position_size)

def get_model_probability(market_id, market_question):
    """Get probability from model. Default: Simmer AI consensus."""
    if PROBABILITY_SOURCE == "simmer_ai":
        context = get_market_context(market_id)
        if context:
            market = context.get("market", {})
            ai_consensus = market.get("ai_consensus")
            if ai_consensus is not None:
                return ai_consensus
    # Fallback: return None (skip market)
    return None

def show_config():
    """Show current configuration."""
    print("\n📋 Valuation Trader Config")
    print("=" * 50)
    print(f"  Edge threshold: {EDGE_THRESHOLD:.1%}")
    print(f"  Kelly fraction: {KELLY_FRACTION:.1%}")
    print(f"  Max position: ${MAX_POSITION_USD:.2f}")
    print(f"  Max trades/run: {MAX_TRADES_PER_RUN}")
    print(f"  Probability source: {PROBABILITY_SOURCE}")
    print(f"  Config file: {get_config_path(__file__)}")
    print()

def show_positions():
    """Show current positions."""
    try:
        positions = get_client().get_positions()
        print(f"\n📊 Current Positions ({len(positions)} total)")
        print("=" * 50)
        for pos in positions:
            pnl = pos.unrealized_pnl if hasattr(pos, 'unrealized_pnl') else 0
            print(f"  {pos.market_question[:50]}...")
            print(f"    Side: {pos.side} | Shares: {pos.shares_yes:.1f} | PnL: ${pnl:.2f}")
        print()
    except Exception as e:
        print(f"Error fetching positions: {e}")

def run_scan(live=False, quiet=False):
    """Main scan loop."""
    if not quiet:
        print("[PAPER MODE]" if not live else "[LIVE MODE]")
        print()
        print("🎯 Valuation Trader Scan")
        print("=" * 50)
    
    # Get active markets
    try:
        markets = get_client().get_markets(status="active", limit=100)
    except Exception as e:
        print(f"Error fetching markets: {e}")
        return
    
    if not quiet:
        print(f"  Markets scanned: {len(markets)}")
    
    # Get portfolio for Kelly sizing
    try:
        portfolio = get_client().get_portfolio()
        bankroll = portfolio.balance_usdc if hasattr(portfolio, 'balance_usdc') else 100
    except:
        bankroll = 100
    
    trades_executed = 0
    signals = 0
    
    for market in markets:
        if trades_executed >= MAX_TRADES_PER_RUN:
            break
        
        market_id = market.id
        market_question = market.question
        market_price = market.current_probability
        
        # Get model probability
        model_prob = get_model_probability(market_id, market_question)
        if model_prob is None:
            continue
        
        # Calculate edge
        edge = model_prob - market_price
        
        # Check signal
        if abs(edge) < EDGE_THRESHOLD:
            continue
        
        signals += 1
        
        if not quiet:
            edge_pct = edge * 100
            print(f"\n📰 {market_question[:60]}...")
            print(f"   Model: {model_prob:.0%} | Market: {market_price:.0%} | Edge: {edge_pct:+.1f}%")
        
        # Check safeguards
        context = get_market_context(market_id)
        safe, warnings = check_safeguards(context)
        
        if warnings:
            if not quiet:
                print(f"   ⚠️ {', '.join(warnings[:2])}")
            if not safe:
                if not quiet:
                    print(f"   ⏭️ Safeguards failed, skipping")
                continue
        
        # Determine side
        side = "yes" if edge > 0 else "no"
        
        # Calculate position size (Kelly)
        position_size = calculate_kelly_position(edge, market_price, bankroll, MAX_POSITION_USD)
        
        if position_size < 0.01:
            if not quiet:
                print(f"   Position too small: ${position_size:.2f}")
            continue
        
        if not quiet:
            print(f"   💰 {'DRY RUN' if not live else 'EXECUTING'}: {side.upper()} ${position_size:.2f}")
        
        if live:
            result = execute_trade(
                market_id, side, position_size,
                market_price, model_prob, edge,
                f"Valuation edge: model {model_prob:.0%} vs market {market_price:.0%}"
            )
            if result["success"]:
                if not quiet:
                    print(f"   ✅ Trade {result['trade_id'][:8]}... executed")
                trades_executed += 1
            else:
                if not quiet:
                    print(f"   ❌ Trade failed: {result.get('error', 'unknown')}")
    
    if not quiet:
        print()
        print("=" * 50)
        print(f"  Signals found: {signals}")
        print(f"  Executed: {trades_executed}")
        print()

# =============================================================================
# CLI Entry Point
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Polymarket Valuation Divergence Trader")
    parser.add_argument("--live", action="store_true", help="Execute real trades")
    parser.add_argument("--positions", action="store_true", help="Show current positions")
    parser.add_argument("--config", action="store_true", help="Show configuration")
    parser.add_argument("--set", type=str, help="Update config (KEY=VALUE)")
    parser.add_argument("--quiet", action="store_true", help="Quiet mode (cron-friendly)")
    
    args = parser.parse_args()
    
    if args.config:
        show_config()
        return
    
    if args.positions:
        show_positions()
        return
    
    if args.set:
        key, val = args.set.split("=")
        if key in CONFIG_SCHEMA:
            type_fn = CONFIG_SCHEMA[key].get("type", str)
            update_config({key: type_fn(val)}, __file__)
            print(f"✅ Updated {key} = {val}")
        else:
            print(f"❌ Unknown config key: {key}")
        return
    
    run_scan(live=args.live, quiet=args.quiet)

if __name__ == "__main__":
    main()
