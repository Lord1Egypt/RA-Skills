#!/usr/bin/env python3
"""
Solana Meme Token Analyzer
Analyzes token holder distribution to detect insider wallets and concentration risk.
"""

import requests
import time
import os
import sys
import json
from colorama import Fore, Style, init
from tabulate import tabulate

init(autoreset=True)


class MemeAnalyzerPro:
    def __init__(self, token_address):
        self.token = token_address
        helius_key = os.environ.get("HELIUS_API_KEY", "")

        self.rpc_endpoints = []
        if helius_key:
            self.rpc_endpoints.append(
                f"https://mainnet.helius-rpc.com/?api-key={helius_key}"
            )
        self.rpc_endpoints += [
            "https://api.mainnet-beta.solana.com",
            "https://solana-mainnet.rpc.extrnode.com",
            "https://solana-api.projectserum.com",
        ]

        self.dex_url = f"https://api.dexscreener.com/latest/dex/tokens/{self.token}"
        self.headers = {"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}

    def log(self, msg, color=Fore.WHITE):
        print(f"{color}[System] {msg}{Style.RESET_ALL}")

    def rpc_call(self, method, params):
        payload = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": method,
            "params": params
        }

        for rpc_url in self.rpc_endpoints:
            try:
                response = requests.post(rpc_url, json=payload, headers=self.headers, timeout=8)

                if response.status_code == 200:
                    data = response.json()
                    if "error" in data:
                        continue
                    return data.get("result")
                elif response.status_code == 429:
                    self.log(f"节点 {rpc_url[:40]}... 限流 (429)，自动切换...", Fore.YELLOW)
                    time.sleep(1)
                    continue
                else:
                    continue
            except Exception:
                continue

        self.log("❌ 所有节点均请求失败！建议设置 HELIUS_API_KEY 环境变量。", Fore.RED)
        return None

    def get_token_info_dex(self):
        try:
            r = requests.get(self.dex_url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                if data.get('pairs'):
                    return max(data['pairs'], key=lambda x: x.get('liquidity', {}).get('usd', 0))
        except Exception:
            pass
        return None

    def get_token_supply(self):
        res = self.rpc_call("getTokenSupply", [self.token])
        if res and 'value' in res:
            return float(res['value']['uiAmountString'])
        return 0

    def get_largest_accounts(self):
        self.log("正在扫描持仓分布 (自动寻找可用节点)...", Fore.CYAN)
        res = self.rpc_call("getTokenLargestAccounts", [self.token])
        if res and 'value' in res:
            return res['value']
        return []

    def get_sol_balance(self, address):
        res = self.rpc_call("getBalance", [address])
        if res and 'value' in res:
            return res['value'] / 10 ** 9
        return -1

    def run(self, output_json=False):
        print(f"\n{Fore.GREEN}=== Solana Meme Token Analyzer ==={Style.RESET_ALL}")

        dex_info = self.get_token_info_dex()
        if not dex_info:
            self.log("DexScreener 未找到数据 (无效CA或新币)", Fore.RED)
            if output_json:
                print(json.dumps({"error": "Token not found on DexScreener"}))
            return

        symbol = dex_info['baseToken']['symbol']
        price = dex_info.get('priceUsd', '0')
        lp_address = dex_info.get('pairAddress')
        liquidity_usd = dex_info.get('liquidity', {}).get('usd', 0)

        print(f"Token: {Fore.CYAN}${symbol}{Style.RESET_ALL} | Price: ${price} | Liquidity: ${liquidity_usd:,.0f}")
        print(f"LP Address: {lp_address}")

        total_supply = self.get_token_supply()
        if not total_supply:
            return

        holders = self.get_largest_accounts()
        if not holders:
            self.log("⚠️ 无法获取持仓。公共节点拒绝服务，建议设置 HELIUS_API_KEY。", Fore.YELLOW)
            return

        table_data = []
        suspicious_count = 0
        top10_insider_share = 0
        result_holders = []

        print(f"\n正在分析前 {len(holders)} 大户 (检测老鼠仓)...")

        for i, h in enumerate(holders):
            addr = h['address']
            amount = float(h['uiAmountString'])
            percent = (amount / total_supply) * 100

            tag = "普通大户"
            color = Fore.WHITE
            sol_balance = None

            if addr == lp_address:
                tag = "LP 池子"
                color = Fore.BLUE
            else:
                if i < 12:
                    sol_bal = self.get_sol_balance(addr)
                    sol_balance = sol_bal if sol_bal != -1 else None

                    if i < 10:
                        top10_insider_share += percent

                    if sol_bal != -1:
                        if sol_bal < 0.05:
                            tag = f"⚠️ 疑似老鼠仓 (SOL:{sol_bal:.3f})"
                            color = Fore.RED
                            suspicious_count += 1
                        elif sol_bal > 500:
                            tag = f"🐋 巨鲸/交易所 (SOL:{sol_bal:.0f})"
                            color = Fore.MAGENTA
                        else:
                            tag = f"SOL: {sol_bal:.2f}"

            table_data.append([
                i + 1,
                f"{addr[:4]}...{addr[-4:]}",
                f"{percent:.2f}%",
                f"{color}{tag}{Style.RESET_ALL}"
            ])
            result_holders.append({
                "rank": i + 1,
                "address": addr,
                "percent": round(percent, 2),
                "tag": tag.replace("⚠️ ", "").replace("🐋 ", ""),
                "sol_balance": sol_balance
            })
            time.sleep(0.1)

        print(tabulate(table_data, headers=["排名", "地址", "占比", "分析结果"], tablefmt="grid"))

        risk_level = "LOW"
        warnings = []

        if suspicious_count > 0:
            warnings.append(f"发现 {suspicious_count} 个疑似老鼠仓 (持币多但没钱)")
            risk_level = "HIGH"
            print(f"\n{Fore.RED}⚠️ {warnings[-1]}{Style.RESET_ALL}")

        print(f"\n📊 {symbol} 风险简报:")
        print(f"前10名潜在控盘率: {top10_insider_share:.2f}%")

        if top10_insider_share > 50:
            risk_level = "EXTREME"
            warnings.append(f"极度控盘！前10名持有 {top10_insider_share:.1f}%，随时可能砸盘")
            print(f"{Fore.RED}🚨 极度控盘预警！{Style.RESET_ALL}")
        elif top10_insider_share > 30:
            if risk_level == "LOW":
                risk_level = "MEDIUM"
            warnings.append(f"高度控盘！前10名持有 {top10_insider_share:.1f}%")
            print(f"{Fore.RED}🚨 高度控盘预警！庄家随时可能砸盘。{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}✅ 筹码分布相对健康。{Style.RESET_ALL}")

        if output_json:
            result = {
                "token": {"symbol": symbol, "price_usd": price, "liquidity_usd": liquidity_usd},
                "risk_level": risk_level,
                "top10_concentration": round(top10_insider_share, 2),
                "suspicious_insider_count": suspicious_count,
                "warnings": warnings,
                "holders": result_holders
            }
            print("\n--- JSON OUTPUT ---")
            print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1].strip()
        use_json = "--json" in sys.argv
    else:
        target = input("请输入 Token CA: ").strip()
        use_json = False

    if target:
        MemeAnalyzerPro(target).run(output_json=use_json)
    else:
        print("用法: python3 psdm.py <TOKEN_CA> [--json]")
        sys.exit(1)
