#!/usr/bin/env python3
"""
Polymarket Paper Trading Platform

Practice prediction market trading with virtual money.

Usage:
    python paper_trading.py create-account --name "MyPortfolio"
    python paper_trading.py markets --limit 20
    python paper_trading.py trade --market "bitcoin-100k" --side YES --amount 500
    python paper_trading.py portfolio
    python paper_trading.py leaderboard --weekly
"""

import os
import sys
import json
import time
import hashlib
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum


class TradeSide(Enum):
    YES = "YES"
    NO = "NO"


class AccountTier(Enum):
    FREE = "free"
    PRO = "pro"
    TEAM = "team"


@dataclass
class Position:
    """Represents a position in a market."""
    
    market_id: str
    market_question: str
    side: TradeSide
    shares: float
    avg_price: float
    current_price: float
    opened_at: float
    closed_at: Optional[float] = None
    pnl: float = 0.0


@dataclass
class Trade:
    """Represents a trade execution."""
    
    trade_id: str
    market_id: str
    market_question: str
    side: TradeSide
    amount: float
    price: float
    shares: float
    fee: float
    timestamp: float
    resolved: bool = False
    outcome: Optional[str] = None


@dataclass
class Account:
    """Represents a paper trading account."""
    
    account_id: str
    name: str
    tier: AccountTier
    cash: float
    initial_cash: float
    positions: List[Position] = field(default_factory=list)
    trades: List[Trade] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)


class PolymarketPaperTrading:
    """Paper trading platform for Polymarket."""
    
    TIER_LIMITS = {
        AccountTier.FREE: {"cash": 10000, "markets_per_day": 5},
        AccountTier.PRO: {"cash": 100000, "markets_per_day": -1},
        AccountTier.TEAM: {"cash": 100000, "markets_per_day": -1},
    }
    
    TRADING_FEE = 0.0001  # 0.01% (Polymarket US fee)
    
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = Path(data_dir or Path.home() / ".polymarket-paper")
        self.accounts_dir = self.data_dir / "accounts"
        self.leaderboard_file = self.data_dir / "leaderboard.json"
        
        self._ensure_dirs()
        
        # Sample market data for testing
        self.sample_markets = [
            {
                "id": "bitcoin-100k",
                "question": "Will Bitcoin reach $100,000 by end of 2026?",
                "yes_price": 0.45,
                "no_price": 0.52,
                "volume": 5000000,
                "category": "crypto",
                "expires": "2026-12-31T23:59:59Z"
            },
            {
                "id": "trump-war-iran",
                "question": "Will Trump declare war on Iran by March 31, 2026?",
                "yes_price": 0.35,
                "no_price": 0.60,
                "volume": 2500000,
                "category": "politics",
                "expires": "2026-03-31T23:59:59Z"
            },
            {
                "id": "israel-lebanon",
                "question": "Will Israel strike Lebanon by March 31, 2026?",
                "yes_price": 0.85,
                "no_price": 0.12,
                "volume": 3000000,
                "category": "geopolitics",
                "expires": "2026-03-31T23:59:59Z"
            },
            {
                "id": "sp500-5000",
                "question": "Will S&P 500 reach 5000 by June 2026?",
                "yes_price": 0.72,
                "no_price": 0.25,
                "volume": 1500000,
                "category": "finance",
                "expires": "2026-06-30T23:59:59Z"
            },
            {
                "id": "eth-flip-btc",
                "question": "Will Ethereum flip Bitcoin market cap by 2027?",
                "yes_price": 0.18,
                "no_price": 0.78,
                "volume": 800000,
                "category": "crypto",
                "expires": "2027-12-31T23:59:59Z"
            }
        ]
    
    def _ensure_dirs(self):
        """Create necessary directories."""
        self.accounts_dir.mkdir(parents=True, exist_ok=True)
    
    def create_account(self, name: str, tier: str = "free", initial_cash: float = None) -> Account:
        """Create a new paper trading account."""
        
        tier_enum = AccountTier(tier.lower())
        
        if initial_cash is None:
            initial_cash = self.TIER_LIMITS[tier_enum]["cash"]
        
        account_id = hashlib.md5(f"{name}-{time.time()}".encode()).hexdigest()[:12]
        
        account = Account(
            account_id=account_id,
            name=name,
            tier=tier_enum,
            cash=initial_cash,
            initial_cash=initial_cash,
        )
        
        self._save_account(account)
        
        return account
    
    def _save_account(self, account: Account):
        """Save account to file."""
        
        account_file = self.accounts_dir / f"{account.account_id}.json"
        
        data = {
            "account_id": account.account_id,
            "name": account.name,
            "tier": account.tier.value,
            "cash": account.cash,
            "initial_cash": account.initial_cash,
            "positions": [
                {
                    "market_id": p.market_id,
                    "market_question": p.market_question,
                    "side": p.side.value,
                    "shares": p.shares,
                    "avg_price": p.avg_price,
                    "current_price": p.current_price,
                    "opened_at": p.opened_at,
                }
                for p in account.positions
            ],
            "trades": [
                {
                    "trade_id": t.trade_id,
                    "market_id": t.market_id,
                    "market_question": t.market_question,
                    "side": t.side.value,
                    "amount": t.amount,
                    "price": t.price,
                    "shares": t.shares,
                    "fee": t.fee,
                    "timestamp": t.timestamp,
                }
                for t in account.trades
            ],
            "created_at": account.created_at,
        }
        
        account_file.write_text(json.dumps(data, indent=2))
    
    def _load_account(self, account_id: str) -> Optional[Account]:
        """Load account from file."""
        
        account_file = self.accounts_dir / f"{account_id}.json"
        
        if not account_file.exists():
            return None
        
        data = json.loads(account_file.read_text())
        
        account = Account(
            account_id=data["account_id"],
            name=data["name"],
            tier=AccountTier(data["tier"]),
            cash=data["cash"],
            initial_cash=data["initial_cash"],
            positions=[
                Position(
                    market_id=p["market_id"],
                    market_question=p["market_question"],
                    side=TradeSide(p["side"]),
                    shares=p["shares"],
                    avg_price=p["avg_price"],
                    current_price=p["current_price"],
                    opened_at=p["opened_at"],
                )
                for p in data.get("positions", [])
            ],
            trades=[
                Trade(
                    trade_id=t["trade_id"],
                    market_id=t["market_id"],
                    market_question=t["market_question"],
                    side=TradeSide(t["side"]),
                    amount=t["amount"],
                    price=t["price"],
                    shares=t["shares"],
                    fee=t["fee"],
                    timestamp=t["timestamp"],
                )
                for t in data.get("trades", [])
            ],
            created_at=data.get("created_at", time.time()),
        )
        
        return account
    
    def get_markets(self, category: str = None, search: str = None, limit: int = 20) -> List[Dict]:
        """Get available markets."""
        
        # In production, this would fetch from Polymarket API
        # For now, use sample data
        
        markets = self.sample_markets.copy()
        
        if category:
            markets = [m for m in markets if m.get("category") == category]
        
        if search:
            search_lower = search.lower()
            markets = [m for m in markets if search_lower in m["question"].lower()]
        
        return markets[:limit]
    
    def get_market_prices(self, market_id: str) -> Dict:
        """Get current prices for a market."""
        
        # Find market
        for market in self.sample_markets:
            if market["id"] == market_id:
                return {
                    "yes_price": market["yes_price"],
                    "no_price": market["no_price"],
                }
        
        return {"yes_price": 0.5, "no_price": 0.5}
    
    def place_trade(self, account_id: str, market_id: str, side: str, amount: float) -> Trade:
        """Place a paper trade."""
        
        account = self._load_account(account_id)
        if not account:
            raise ValueError(f"Account not found: {account_id}")
        
        # Check cash
        if account.cash < amount:
            raise ValueError(f"Insufficient cash. Have ${account.cash:.2f}, need ${amount:.2f}")
        
        # Get market
        market = None
        for m in self.sample_markets:
            if m["id"] == market_id:
                market = m
                break
        
        if not market:
            raise ValueError(f"Market not found: {market_id}")
        
        # Get price
        prices = self.get_market_prices(market_id)
        price = prices["yes_price"] if side.upper() == "YES" else prices["no_price"]
        
        # Calculate shares
        shares = amount / price
        
        # Calculate fee
        fee = amount * self.TRADING_FEE
        
        # Execute trade
        trade_id = hashlib.md5(f"{account_id}-{market_id}-{time.time()}".encode()).hexdigest()[:12]
        
        trade = Trade(
            trade_id=trade_id,
            market_id=market_id,
            market_question=market["question"],
            side=TradeSide(side.upper()),
            amount=amount,
            price=price,
            shares=shares,
            fee=fee,
            timestamp=time.time(),
        )
        
        # Update account
        account.cash -= amount
        account.trades.append(trade)
        
        # Add position
        position = Position(
            market_id=market_id,
            market_question=market["question"],
            side=TradeSide(side.upper()),
            shares=shares,
            avg_price=price,
            current_price=price,
            opened_at=time.time(),
        )
        account.positions.append(position)
        
        self._save_account(account)
        
        return trade
    
    def get_portfolio(self, account_id: str) -> Dict:
        """Get account portfolio."""
        
        account = self._load_account(account_id)
        if not account:
            raise ValueError(f"Account not found: {account_id}")
        
        # Update positions with current prices
        total_position_value = 0.0
        
        for position in account.positions:
            prices = self.get_market_prices(position.market_id)
            position.current_price = prices["yes_price"] if position.side == TradeSide.YES else prices["no_price"]
            total_position_value += position.shares * position.current_price
        
        total_value = account.cash + total_position_value
        pnl = total_value - account.initial_cash
        pnl_pct = (pnl / account.initial_cash) * 100 if account.initial_cash > 0 else 0
        
        return {
            "account_id": account.account_id,
            "name": account.name,
            "tier": account.tier.value,
            "cash": account.cash,
            "position_value": total_position_value,
            "total_value": total_value,
            "initial_cash": account.initial_cash,
            "pnl": pnl,
            "pnl_pct": pnl_pct,
            "positions": [
                {
                    "market_id": p.market_id,
                    "market_question": p.market_question,
                    "side": p.side.value,
                    "shares": p.shares,
                    "avg_price": p.avg_price,
                    "current_price": p.current_price,
                    "value": p.shares * p.current_price,
                    "pnl": (p.current_price - p.avg_price) * p.shares,
                }
                for p in account.positions
            ],
            "trades_count": len(account.trades),
        }
    
    def get_leaderboard(self, period: str = "all-time") -> List[Dict]:
        """Get leaderboard."""
        
        leaderboard = []
        
        for account_file in self.accounts_dir.glob("*.json"):
            try:
                data = json.loads(account_file.read_text())
                
                total_value = data["cash"]
                for p in data.get("positions", []):
                    prices = self.get_market_prices(p["market_id"])
                    price = prices["yes_price"] if p["side"] == "YES" else prices["no_price"]
                    total_value += p["shares"] * price
                
                pnl = total_value - data["initial_cash"]
                pnl_pct = (pnl / data["initial_cash"]) * 100 if data["initial_cash"] > 0 else 0
                
                leaderboard.append({
                    "account_id": data["account_id"],
                    "name": data["name"],
                    "tier": data["tier"],
                    "total_value": total_value,
                    "pnl": pnl,
                    "pnl_pct": pnl_pct,
                    "trades_count": len(data.get("trades", [])),
                })
            except:
                continue
        
        # Sort by PnL percentage
        leaderboard.sort(key=lambda x: x["pnl_pct"], reverse=True)
        
        # Add rank
        for i, entry in enumerate(leaderboard):
            entry["rank"] = i + 1
        
        return leaderboard[:100]
    
    def resolve_market(self, account_id: str, market_id: str, outcome: str) -> Dict:
        """Manually resolve a market for practice."""
        
        account = self._load_account(account_id)
        if not account:
            raise ValueError(f"Account not found: {account_id}")
        
        # Find positions for this market
        resolved_positions = []
        total_payout = 0.0
        
        for i, position in enumerate(account.positions):
            if position.market_id == market_id:
                # Calculate payout
                if position.side.value == outcome.upper():
                    # Winning position
                    payout = position.shares * 1.0  # Each share worth $1
                    total_payout += payout
                    resolved_positions.append({
                        "market_id": market_id,
                        "side": position.side.value,
                        "shares": position.shares,
                        "payout": payout,
                        "won": True,
                    })
                else:
                    # Losing position
                    resolved_positions.append({
                        "market_id": market_id,
                        "side": position.side.value,
                        "shares": position.shares,
                        "payout": 0.0,
                        "won": False,
                    })
        
        # Remove resolved positions
        account.positions = [p for p in account.positions if p.market_id != market_id]
        
        # Add payout to cash
        account.cash += total_payout
        
        self._save_account(account)
        
        return {
            "market_id": market_id,
            "outcome": outcome,
            "resolved_positions": resolved_positions,
            "total_payout": total_payout,
            "new_cash": account.cash,
        }


def main():
    """CLI entry point."""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Polymarket Paper Trading")
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # create-account
    create_parser = subparsers.add_parser('create-account', help='Create account')
    create_parser.add_argument('--name', required=True, help='Account name')
    create_parser.add_argument('--tier', default='free', choices=['free', 'pro', 'team'])
    create_parser.add_argument('--initial', type=float, help='Initial cash')
    
    # markets
    markets_parser = subparsers.add_parser('markets', help='View markets')
    markets_parser.add_argument('--limit', type=int, default=20)
    markets_parser.add_argument('--category', help='Filter by category')
    markets_parser.add_argument('--search', help='Search keyword')
    
    # trade
    trade_parser = subparsers.add_parser('trade', help='Place trade')
    trade_parser.add_argument('--account', required=True, help='Account ID')
    trade_parser.add_argument('--market', required=True, help='Market ID')
    trade_parser.add_argument('--side', required=True, choices=['YES', 'NO'])
    trade_parser.add_argument('--amount', type=float, required=True)
    
    # portfolio
    portfolio_parser = subparsers.add_parser('portfolio', help='View portfolio')
    portfolio_parser.add_argument('--account', required=True, help='Account ID')
    
    # leaderboard
    leaderboard_parser = subparsers.add_parser('leaderboard', help='View leaderboard')
    leaderboard_parser.add_argument('--period', default='all-time', choices=['weekly', 'monthly', 'all-time'])
    
    # resolve
    resolve_parser = subparsers.add_parser('resolve', help='Resolve market')
    resolve_parser.add_argument('--account', required=True, help='Account ID')
    resolve_parser.add_argument('--market', required=True, help='Market ID')
    resolve_parser.add_argument('--outcome', required=True, choices=['YES', 'NO'])
    
    args = parser.parse_args()
    
    platform = PolymarketPaperTrading()
    
    if args.command == 'create-account':
        account = platform.create_account(args.name, args.tier, args.initial)
        print(f"✓ Created account: {account.name}")
        print(f"  Account ID: {account.account_id}")
        print(f"  Tier: {account.tier.value}")
        print(f"  Virtual cash: ${account.cash:,.2f}")
    
    elif args.command == 'markets':
        markets = platform.get_markets(
            category=args.category,
            search=args.search,
            limit=args.limit
        )
        
        print(f"\nFound {len(markets)} markets:\n")
        for i, m in enumerate(markets, 1):
            print(f"{i}. {m['question'][:60]}...")
            print(f"   YES: ${m['yes_price']:.2f}  NO: ${m['no_price']:.2f}  Vol: ${m['volume']:,.0f}")
            print()
    
    elif args.command == 'trade':
        trade = platform.place_trade(args.account, args.market, args.side, args.amount)
        print(f"✓ Trade executed")
        print(f"  Market: {trade.market_question[:50]}...")
        print(f"  Side: {trade.side.value}")
        print(f"  Amount: ${trade.amount:.2f}")
        print(f"  Price: ${trade.price:.4f}")
        print(f"  Shares: {trade.shares:,.2f}")
        print(f"  Fee: ${trade.fee:.4f}")
    
    elif args.command == 'portfolio':
        portfolio = platform.get_portfolio(args.account)
        print(f"\nPortfolio: {portfolio['name']}")
        print(f"Account ID: {portfolio['account_id']}")
        print(f"Tier: {portfolio['tier']}")
        print(f"\nCash: ${portfolio['cash']:,.2f}")
        print(f"Position Value: ${portfolio['position_value']:,.2f}")
        print(f"Total Value: ${portfolio['total_value']:,.2f}")
        print(f"\nPnL: ${portfolio['pnl']:,.2f} ({portfolio['pnl_pct']:+.2f}%)")
        print(f"Trades: {portfolio['trades_count']}")
        
        if portfolio['positions']:
            print(f"\nPositions:")
            for p in portfolio['positions']:
                print(f"  {p['side']} {p['shares']:,.0f} {p['market_question'][:30]}...")
                print(f"    Value: ${p['value']:,.2f}  PnL: ${p['pnl']:,.2f}")
    
    elif args.command == 'leaderboard':
        leaderboard = platform.get_leaderboard(period=args.period)
        
        print(f"\nLeaderboard ({args.period}):\n")
        for entry in leaderboard[:20]:
            print(f"{entry['rank']:2}. {entry['name'][:20]:<20} {entry['pnl_pct']:>+6.2f}%  ${entry['pnl']:>10,.2f}")
    
    elif args.command == 'resolve':
        result = platform.resolve_market(args.account, args.market, args.outcome)
        print(f"✓ Market resolved")
        print(f"  Market: {args.market}")
        print(f"  Outcome: {args.outcome}")
        print(f"  Positions resolved: {len(result['resolved_positions'])}")
        print(f"  Total payout: ${result['total_payout']:,.2f}")
        print(f"  New cash balance: ${result['new_cash']:,.2f}")
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()