#!/usr/bin/env python3
"""
Show portfolio status and trading performance.
"""

import sys
sys.path.insert(0, str(__file__).rsplit('/', 2)[0])

from valuation_trader import get_client

def main():
    try:
        portfolio = get_client().get_portfolio()
        positions = get_client().get_positions()
        
        print(f"\n📊 Portfolio Status")
        print("=" * 50)
        print(f"  Balance: ${portfolio.balance_usdc:.2f}" if hasattr(portfolio, 'balance_usdc') else "  Balance: Unknown")
        print(f"  Total PnL: ${getattr(portfolio, 'pnl_total', 0):.2f}")
        print(f"  Positions: {len(positions)}")
        print()
        
        if positions:
            print(f"📋 Positions ({len(positions)})")
            print("=" * 50)
            for pos in positions:
                pnl = pos.unrealized_pnl if hasattr(pos, 'unrealized_pnl') else 0
                shares = pos.shares_yes if hasattr(pos, 'shares_yes') else 0
                print(f"  {pos.market_question[:50]}...")
                print(f"    Shares: {shares:.1f} | PnL: ${pnl:.2f}")
            print()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
