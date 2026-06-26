#!/usr/bin/env python3
"""
Momentum Polymarket Trader Skill

Automated trading on Polymarket based on price momentum signals.
This is a customizable template - replace calculate_signal() to implement your strategy.
"""

import os
import sys
import time
import random
import argparse
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

try:
    from aion_sdk import AionClient
except ImportError:
    print("Error: aion-sdk not found. Please run: pip install aion-sdk")
    sys.exit(1)


# ============================================================================
# Configuration Constants
# ============================================================================

TRADE_SOURCE = "sdk:momentum-polymarket-trader"
SKILL_SLUG = "momentum-polymarket-trader"
VENUE = "polymarket"

# Read configuration from environment variables
MAX_POSITION_SIZE = float(os.getenv("MAX_POSITION_SIZE", "10.0"))
MIN_EDGE_THRESHOLD = float(os.getenv("MIN_EDGE_THRESHOLD", "0.05"))
BASE_POLL_INTERVAL = 60  # seconds


# ============================================================================
# Client Singleton
# ============================================================================

_client = None

def get_client() -> AionClient:
    """Get AION client singleton"""
    global _client
    if _client is None:
        api_key = os.environ.get("AION_API_KEY")
        if not api_key:
            raise ValueError(
                "AION_API_KEY environment variable not found.\n"
                "Get your API key from https://pm-t1.bxingupdate.com/agents and set the environment variable."
            )
        _client = AionClient(
            api_key=api_key,
            venue=VENUE
        )
    return _client


# ============================================================================
# Data Models
# ============================================================================

@dataclass
class Signal:
    """Trading signal"""
    side: Optional[str]  # "yes", "no", or None
    confidence: float  # 0-1
    reasoning: str
    edge: float = 0.0  # Expected edge


@dataclass
class TradeDecision:
    """Trade decision"""
    market_id: str
    market_question: str
    action: str  # "TRADE", "HOLD", "SKIP"
    side: Optional[str] = None
    size: float = 0.0
    reasoning: str = ""


# ============================================================================
# Core Trading Logic
# ============================================================================

def calculate_signal(market: Dict, context: Dict) -> Signal:
    """
    Calculate trading signal for a market
    
    ⚠️ This is the function you should customize!
    
    Replace this function to implement your trading strategy. You can use:
    - Technical indicators (moving averages, RSI, MACD, etc.)
    - Machine learning models
    - External data sources (news, social media, etc.)
    - Any other signal logic
    
    Args:
        market: Market data dictionary
        context: Market context data (includes trading discipline, slippage estimates, etc.)
    
    Returns:
        Signal object
    """
    # Default implementation: simple price momentum strategy
    # This is just an example - should be replaced with more sophisticated logic
    
    yes_price = market.get("yesPrice", 0.5)
    no_price = market.get("noPrice", 0.5)
    
    # Check if historical price data is available
    # Note: This is a simplified version; real implementation should fetch historical data
    
    # Example logic: if YES price deviates significantly from 0.5, assume momentum
    momentum_threshold = 0.10
    
    if yes_price > 0.5 + momentum_threshold:
        # Price is already high, might continue rising (momentum strategy)
        edge = (yes_price - 0.5) * 0.3  # Simplified edge calculation
        return Signal(
            side="yes",
            confidence=min(0.9, 0.5 + edge),
            reasoning=f"Positive momentum detected for YES (current price={yes_price:.3f})",
            edge=edge
        )
    elif no_price > 0.5 + momentum_threshold:
        # NO price is high
        edge = (no_price - 0.5) * 0.3
        return Signal(
            side="no",
            confidence=min(0.9, 0.5 + edge),
            reasoning=f"Positive momentum detected for NO (current price={no_price:.3f})",
            edge=edge
        )
    else:
        # Price near 0.5, no clear momentum
        return Signal(
            side=None,
            confidence=0.0,
            reasoning=f"No clear momentum signal (YES={yes_price:.3f}, NO={no_price:.3f})",
            edge=0.0
        )


def check_market_context(market_id: str, my_probability: Optional[float] = None) -> Dict:
    """
    Fetch market context and trading discipline data
    
    Context includes:
    - flip-flop warnings
    - slippage estimates
    - edge analysis
    """
    client = get_client()
    params = {}
    if my_probability is not None:
        params["my_probability"] = my_probability
    
    try:
        return client.get_market_context(market_id, **params)
    except Exception as e:
        print(f"Warning: Unable to fetch context for market {market_id}: {e}")
        return {}


def auto_redeem_positions():
    """Auto-redeem winnings from resolved markets"""
    client = get_client()
    results = []
    
    try:
        redemption_results = client.auto_redeem()
        for r in redemption_results:
            if r.get("success"):
                results.append({
                    "market_id": r.get("market_id"),
                    "tx_hash": r.get("tx_hash"),
                    "amount": r.get("amount", 0)
                })
                print(f"✓ Redeemed market {r['market_id'][:20]}...: tx={r['tx_hash'][:10]}...")
        return results
    except Exception as e:
        print(f"Warning: Auto-redemption failed: {e}")
        return []


def execute_trade(
    market: Dict,
    signal: Signal,
    dry_run: bool = True
) -> bool:
    """
    Execute trade
    
    Args:
        market: Market data
        signal: Trading signal
        dry_run: If True, only simulates trade without actual execution
    
    Returns:
        Whether successful
    """
    client = get_client()
    market_id = market.get("id")
    
    # Calculate trade size
    position_size = min(MAX_POSITION_SIZE, 5.0 * signal.confidence)
    
    if dry_run:
        print(f"  [DRY-RUN] Simulating trade: {signal.side.upper()} {position_size:.1f} USDC")
        print(f"  Reason: {signal.reasoning}")
        return True
    
    try:
        result = client.trade(
            market_id=market_id,
            side=signal.side,
            amount=position_size,
            source=TRADE_SOURCE,
            skill_slug=SKILL_SLUG,
            reasoning=signal.reasoning
        )
        
        if result.get("success"):
            print(f"  ✓ Trade executed: {signal.side.upper()} {position_size:.1f} USDC")
            print(f"  Order ID: {result.get('order_id', 'N/A')}")
            return True
        else:
            print(f"  ✗ Trade failed: {result.get('error', 'Unknown error')}")
            return False
            
    except Exception as e:
        print(f"  ✗ Trade execution exception: {e}")
        return False


# ============================================================================
# Main Execution Loop
# ============================================================================

def run_once(dry_run: bool = True) -> Dict:
    """
    Execute one trading cycle
    
    Returns:
        Dictionary containing execution summary
    """
    client = get_client()
    
    print(f"\n{'='*70}")
    print(f"Skill: {SKILL_SLUG}")
    print(f"Venue: {VENUE}")
    print(f"Mode: {'DRY-RUN (simulation)' if dry_run else 'LIVE TRADING ⚠️'}")
    print(f"{'='*70}\n")
    
    # 1. Auto-redeem resolved positions
    print("🔄 Checking for positions to redeem...")
    redeemed = auto_redeem_positions()
    
    # 2. Fetch market briefing
    print("\n📊 Fetching market briefing...")
    try:
        # Note: Wallet address may be needed here; simplified version omits it if API doesn't require
        briefing = client.get_briefing(venue=VENUE, include_markets=True)
    except Exception as e:
        print(f"✗ Unable to fetch briefing: {e}")
        return {"status": "error", "error": str(e)}
    
    # 3. Check risk alerts
    risk_alerts = briefing.get("riskAlerts", [])
    if risk_alerts:
        print(f"\n⚠️  Risk alerts:")
        for alert in risk_alerts:
            print(f"  - {alert}")
        print("\n⏸️  Trading paused due to risk alerts")
        return {"status": "risk-paused", "alerts": risk_alerts}
    else:
        print("✓ No risk alerts")
    
    # 4. Analyze opportunity markets
    opportunity_markets = briefing.get("opportunityMarkets", [])
    print(f"\n🎯 Found {len(opportunity_markets)} opportunity markets")
    
    decisions: List[TradeDecision] = []
    
    for market in opportunity_markets:
        market_id = market.get("id")
        market_question = market.get("question", market.get("title", "Unknown market"))
        
        print(f"\nAnalyzing: {market_question[:60]}...")
        
        # Fetch market context
        context = check_market_context(market_id)
        
        # Check warnings
        warnings = context.get("warnings", [])
        trading_data = context.get("trading", {})
        
        if trading_data.get("flip_flop_warning"):
            print("  ⚠️  Flip-flop detected - skipping")
            decisions.append(TradeDecision(
                market_id=market_id,
                market_question=market_question,
                action="SKIP",
                reasoning="flip-flop warning"
            ))
            continue
        
        if warnings:
            print(f"  ⚠️  Warnings: {', '.join(warnings[:2])} - skipping")
            decisions.append(TradeDecision(
                market_id=market_id,
                market_question=market_question,
                action="SKIP",
                reasoning=f"Context warnings: {warnings[0]}"
            ))
            continue
        
        # Calculate trading signal
        signal = calculate_signal(market, context)
        
        if signal.side is None:
            print(f"  • HOLD: {signal.reasoning}")
            decisions.append(TradeDecision(
                market_id=market_id,
                market_question=market_question,
                action="HOLD",
                reasoning=signal.reasoning
            ))
            continue
        
        # Check if edge is sufficient
        if signal.edge < MIN_EDGE_THRESHOLD:
            print(f"  • HOLD: Edge too small ({signal.edge:.1%} < {MIN_EDGE_THRESHOLD:.1%})")
            decisions.append(TradeDecision(
                market_id=market_id,
                market_question=market_question,
                action="HOLD",
                reasoning=f"Insufficient edge ({signal.edge:.1%})"
            ))
            continue
        
        # Execute trade
        print(f"  💰 TRADE {signal.side.upper()}: Edge {signal.edge:.1%}")
        success = execute_trade(market, signal, dry_run=dry_run)
        
        decisions.append(TradeDecision(
            market_id=market_id,
            market_question=market_question,
            action="TRADE" if success else "FAILED",
            side=signal.side,
            size=min(MAX_POSITION_SIZE, 5.0 * signal.confidence),
            reasoning=signal.reasoning
        ))
    
    # 5. Output summary
    print(f"\n{'='*70}")
    print("Execution Summary")
    print(f"{'='*70}")
    print(f"Auto-redeemed: {len(redeemed)} positions")
    print(f"Markets analyzed: {len(opportunity_markets)}")
    print(f"Trades executed: {sum(1 for d in decisions if d.action == 'TRADE')}")
    print(f"Hold decisions: {sum(1 for d in decisions if d.action == 'HOLD')}")
    print(f"Markets skipped: {sum(1 for d in decisions if d.action == 'SKIP')}")
    print(f"{'='*70}\n")
    
    return {
        "status": "ok",
        "redeemed": len(redeemed),
        "analyzed": len(opportunity_markets),
        "decisions": decisions
    }


def run_continuous(dry_run: bool = True):
    """Continuously run the trading skill (polling with jitter)"""
    print(f"🚀 Starting continuous trading mode...")
    print(f"Base interval: {BASE_POLL_INTERVAL} seconds")
    print(f"Mode: {'DRY-RUN' if dry_run else 'LIVE TRADING'}\n")
    
    iteration = 0
    while True:
        iteration += 1
        print(f"\n>>> Iteration #{iteration}")
        
        try:
            result = run_once(dry_run=dry_run)
            
            if result.get("status") == "error":
                print(f"✗ Error: {result.get('error')}")
                
        except KeyboardInterrupt:
            print("\n\n⏹️  Received interrupt signal, stopping...")
            break
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
            import traceback
            traceback.print_exc()
        
        # Random jitter to avoid synchronization
        jitter = random.randint(-8, 8)
        sleep_time = max(15, BASE_POLL_INTERVAL + jitter)
        
        print(f"\n💤 Sleeping for {sleep_time} seconds...")
        time.sleep(sleep_time)


# ============================================================================
# Command Line Interface
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Momentum Polymarket Trader Skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry-run single execution (default)
  python momentum_trader.py
  
  # Dry-run continuous mode
  python momentum_trader.py --continuous
  
  # Live trading single execution (⚠️ uses real funds!)
  python momentum_trader.py --live
  
  # Live trading continuous mode
  python momentum_trader.py --live --continuous

Environment variables:
  AION_API_KEY          Required - your AION API key
  MAX_POSITION_SIZE     Optional - max position size (default: 10.0)
  MIN_EDGE_THRESHOLD    Optional - min edge threshold (default: 0.05)
        """
    )
    
    parser.add_argument(
        "--live",
        action="store_true",
        help="Live trading mode (⚠️ uses real funds!)"
    )
    
    parser.add_argument(
        "--continuous",
        action="store_true",
        help="Continuous running mode (regular polling)"
    )
    
    args = parser.parse_args()
    
    # Safety check
    if args.live:
        print("\n" + "="*70)
        print("⚠️  WARNING: Live Trading Mode")
        print("="*70)
        print("You are about to trade with real funds!")
        print("Please ensure you have:")
        print("  1. Tested this skill in dry-run mode")
        print("  2. Understand the trading logic and risks")
        print("  3. Set appropriate position limits")
        print("="*70)
        
        response = input("\nConfirm to continue? Type 'YES' to proceed: ")
        if response != "YES":
            print("Cancelled.")
            return
    
    # Run
    dry_run = not args.live
    
    if args.continuous:
        run_continuous(dry_run=dry_run)
    else:
        run_once(dry_run=dry_run)


if __name__ == "__main__":
    main()
