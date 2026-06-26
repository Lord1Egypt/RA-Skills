#!/usr/bin/env python3
"""DeFi收益聚合器"""
import json
import sys
import urllib.request

def fetch_defillama_pools():
    """Fetch top yield pools from DeFiLlama."""
    url = "https://yields.llama.fi/pools"
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            return json.loads(r.read())
    except:
        return None

def format_apy(apy, base_apy=None):
    """Format APY with base vs reward distinction."""
    if base_apy and base_apy > 0:
        return f"{base_apy:.1f}% (总:{apy:.1f}%)"
    return f"{apy:.1f}%"

def main():
    print("🌾 DeFi 收益聚合 TOP20")
    print("稳定币/USDC/USDT池 | 按TVL排序")
    print(f"{'─'*60}")
    
    data = fetch_defillama_pools()
    if not data or 'data' not in data:
        print("❌ DeFiLlama API 不可用")
        print("\n💡 备用方式: 访问 https://defillama.com/yields")
        return
    
    pools = data['data']
    
    # Filter for stablecoin pools with decent TVL
    stable_filter = ['USDC', 'USDT', 'DAI', 'FRAX', 'USDS', 'crvUSD']
    
    relevant = [
        p for p in pools 
        if p.get('tvlUsd', 0) > 1_000_000  # > $1M TVL
        and any(s in str(p.get('symbol', '')) for s in stable_filter)
    ]
    
    # Sort by TVL descending
    relevant.sort(key=lambda x: x.get('tvlUsd', 0), reverse=True)
    
    for i, p in enumerate(relevant[:20], 1):
        tvl = p.get('tvlUsd', 0)
        apy = p.get('apy', 0)
        base = p.get('apyBase', apy)
        project = p.get('project', '?')
        chain = p.get('chain', '?')
        symbol = p.get('symbol', '?')
        
        tvl_str = f"${tvl/1e6:,.1f}M" if tvl > 1e6 else f"${tvl/1e3:,.1f}K"
        
        star = "⭐" if apy > 20 else ("🔶" if apy > 10 else "")
        print(f"  {i:2}. {star} {project} | {symbol} | {chain}")
        print(f"      APY: {format_apy(apy, base)} | TVL: {tvl_str}")
    
    if not relevant:
        print("  当前无满足条件的池子")
    
    print(f"\n💡 数据来源: DeFiLlama Yields API")
    print("⚠️  APY实时波动 | DYOR | 注意无常损失和协议风险")

if __name__ == '__main__':
    main()
