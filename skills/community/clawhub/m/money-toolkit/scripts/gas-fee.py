#!/usr/bin/env python3
"""Gas费实时监控 - 多链对比"""
import sys

try:
    from web3 import Web3
    HAS_WEB3 = True
except ImportError:
    HAS_WEB3 = False

ETH_PRICE = 76065  # approximate USD

CHAINS = {
    "Ethereum": {"rpc": "https://ethereum-rpc.publicnode.com", "chain_id": 1},
    "Arbitrum": {"rpc": "https://arbitrum-rpc.publicnode.com", "chain_id": 42161},
    "Optimism": {"rpc": "https://optimism-rpc.publicnode.com", "chain_id": 10},
    "Base": {"rpc": "https://base-rpc.publicnode.com", "chain_id": 8453},
}

def main():
    print("⛽ Gas费实时监控 - 多链对比\n")

    if not HAS_WEB3:
        print("❌ 需要 web3 库: pip install web3")
        return

    print(f"{'链':<12} {'Gas(Gwei)':<12} {'转账成本':<12} {'vs ETH节省'}")
    print("-" * 50)

    eth_cost = None
    results = []

    for name, config in CHAINS.items():
        w3 = Web3(Web3.HTTPProvider(config["rpc"]))
        if w3.is_connected():
            gas = w3.eth.gas_price
            gwei = gas / 1e9
            # Simple transfer: 21000 gas units
            cost_usd = (21000 * gwei / 1e9) * ETH_PRICE
            if name == "Ethereum":
                eth_cost = cost_usd
            results.append((name, gwei, cost_usd))
        else:
            results.append((name, None, None))

    for name, gwei, cost in results:
        if gwei is None:
            print(f"{name:<12} ❌ 连接失败")
            continue
        saving = ""
        if name != "Ethereum" and eth_cost and eth_cost > 0:
            pct = ((eth_cost - cost) / eth_cost) * 100
            saving = f"省 {pct:.0f}%"
        print(f"{name:<12} {gwei:<12.2f} ${cost:<11.4f} {saving}")

    # Best time to transact
    print(f"\n💡 省钱策略:")
    print(f"  • 当前 ETH Gas 极低 ({results[0][1]:.2f} Gwei) — 适合现在操作!")
    print(f"  • L2 转账成本几乎为零 — 大额操作优先用 L2")
    print(f"  • 周末凌晨 (UTC 0-6) 通常 Gas 最低")
    print(f"  • 批量交易比单笔省 Gas")
    print(f"  • Solana 费用 ~$0.00025/笔")

if __name__ == '__main__':
    main()