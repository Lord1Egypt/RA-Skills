#!/usr/bin/env python3
"""
IBKR Gateway Client — read-only queries via ib_async
Usage: python3 ibkr_client.py <command> [--port 4001]
Commands: summary, positions, quote <symbol>
"""

import sys
import argparse
from ib_async import IB, Stock, Index, Future

def connect(port=4001, client_id=99):
    ib = IB()
    ib.connect('127.0.0.1', port, clientId=client_id, readonly=True)
    return ib

def cmd_summary(ib):
    """Account summary — key metrics only."""
    acct = ib.accountValues()
    keys = {
        'NetLiquidation': 'NAV',
        'TotalCashValue': 'Cash',
        'StockMarketValue': 'Stocks',
        'OptionMarketValue': 'Options',
        'FuturesPNL': 'Futures P&L',
        'UnrealizedPnL': 'Unrealized',
        'RealizedPnL': 'Realized',
        'BuyingPower': 'Buying Power',
        'MaintMarginReq': 'Maintenance Margin',
        'GrossPositionValue': 'Gross Position Value',
    }
    print(f"Account: {ib.managedAccounts()}")
    print("-" * 40)
    for av in acct:
        if av.tag in keys and av.currency == 'BASE':
            val = float(av.value)
            print(f"{keys[av.tag]:.<25s} {val:>15,.2f}")

def cmd_positions(ib):
    """Current positions."""
    positions = ib.positions()
    if not positions:
        print("No positions found")
        return
    
    print(f"{'Symbol':<20} {'Exchange':<8} {'Qty':>10} {'Avg Cost':>12} {'Value':>14}")
    print("-" * 66)
    
    total_value = 0
    for pos in positions:
        c = pos.contract
        symbol = c.localSymbol or c.symbol
        qty = pos.position
        avg = pos.avgCost
        # Approximate value (we'd need market data for exact)
        value = qty * avg if avg else 0
        total_value += value
        print(f"{symbol:<20} {c.exchange or '':<8} {qty:>10,.0f} {avg:>12,.2f} {value:>14,.2f}")
    
    print("-" * 66)
    print(f"{'Total (cost basis)':<20} {'':<8} {'':>10} {'':>12} {total_value:>14,.2f}")

def cmd_quote(ib, symbol, exchange='SEHK', currency='HKD'):
    """Get a quote for a stock."""
    contract = Stock(symbol, exchange, currency)
    ib.reqMarketDataType(3)  # Delayed frozen data
    ticker = ib.reqMktData(contract, '', False, False)
    ib.sleep(3)
    
    print(f"\n{symbol} ({exchange})")
    print(f"  Last:    {ticker.last}")
    print(f"  Bid:     {ticker.bid} x {ticker.bidSize}")
    print(f"  Ask:     {ticker.ask} x {ticker.askSize}")
    print(f"  Close:   {ticker.close}")
    print(f"  Volume:  {ticker.volume}")
    print(f"  High:    {ticker.high}")
    print(f"  Low:     {ticker.low}")
    
    ib.cancelMktData(contract)

def cmd_nav(ib):
    """Quick NAV check."""
    acct = ib.accountValues()
    for av in acct:
        if av.tag == 'NetLiquidation' and av.currency == 'BASE':
            print(f"NAV: ${float(av.value):,.2f}")
            return
    print("NAV not available")

def main():
    parser = argparse.ArgumentParser(description='IBKR Gateway Client')
    parser.add_argument('command', help='summary|positions|quote|nav')
    parser.add_argument('symbol', nargs='?', help='Symbol for quote')
    parser.add_argument('--port', type=int, default=4001, help='API port')
    parser.add_argument('--exchange', default='SEHK', help='Exchange')
    parser.add_argument('--currency', default='HKD', help='Currency')
    args = parser.parse_args()
    
    ib = connect(port=args.port)
    try:
        if args.command == 'summary':
            cmd_summary(ib)
        elif args.command == 'positions':
            cmd_positions(ib)
        elif args.command == 'quote':
            if not args.symbol:
                print("Usage: ibkr_client.py quote <symbol>")
                sys.exit(1)
            cmd_quote(ib, args.symbol, args.exchange, args.currency)
        elif args.command == 'nav':
            cmd_nav(ib)
        else:
            print(f"Unknown command: {args.command}")
            sys.exit(1)
    finally:
        ib.disconnect()

if __name__ == '__main__':
    main()
