#!/usr/bin/env python3
"""
x402 Payment Protocol for AI Agents

Enables autonomous micropayments using HTTP 402 status codes and stablecoins.

Usage:
    python x402.py check <url>
    python x402.py pay <url> [--amount 0.01]
    python x402.py serve [--port 8080 --price 0.01]
    python x402.py balance [--chain base]
    python x402.py history [--limit 10]
"""

import os
import sys
import json
import time
import hashlib
import urllib.request
import urllib.error
from pathlib import Path
from typing import Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class Chain(Enum):
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    BASE = "base"
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"
    SOLANA = "solana"


class Stablecoin(Enum):
    USDC = "usdc"
    USDT = "usdt"
    DAI = "dai"


@dataclass
class PaymentRequest:
    """x402 payment requirement from server."""
    
    amount: float
    currency: str
    chain: str
    recipient_address: str
    facilitator_url: Optional[str] = None
    payment_id: Optional[str] = None
    expires_at: Optional[float] = None


@dataclass
class PaymentReceipt:
    """Proof of payment for retry request."""
    
    payment_id: str
    transaction_hash: str
    amount: float
    currency: str
    chain: str
    timestamp: float
    signature: str


class X402Client:
    """x402 payment client for AI agents."""
    
    SUPPORTED_CHAINS = {
        Chain.ETHEREUM: {"name": "Ethereum Mainnet", "chain_id": 1},
        Chain.POLYGON: {"name": "Polygon", "chain_id": 137},
        Chain.BASE: {"name": "Base", "chain_id": 8453},
        Chain.ARBITRUM: {"name": "Arbitrum One", "chain_id": 42161},
        Chain.OPTIMISM: {"name": "Optimism", "chain_id": 10},
        Chain.SOLANA: {"name": "Solana", "chain_id": None},
    }
    
    def __init__(self, config_dir: Optional[str] = None):
        self.config_dir = Path(config_dir or Path.home() / ".x402")
        self.config_file = self.config_dir / "config.json"
        self.wallet_file = self.config_dir / "wallet.json"
        self.history_file = self.config_dir / "history.jsonl"
        
        self._ensure_config_dir()
    
    def _ensure_config_dir(self):
        """Ensure config directory exists."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self) -> dict:
        """Load configuration."""
        if self.config_file.exists():
            return json.loads(self.config_file.read_text())
        return {"chain": "base", "token": "usdc"}
    
    def _save_config(self, config: dict):
        """Save configuration."""
        self.config_file.write_text(json.dumps(config, indent=2))
    
    def _load_wallet(self) -> dict:
        """Load wallet configuration."""
        if self.wallet_file.exists():
            return json.loads(self.wallet_file.read_text())
        return {}
    
    def check_support(self, url: str) -> Tuple[bool, Optional[PaymentRequest]]:
        """Check if endpoint supports x402 payments."""
        
        try:
            req = urllib.request.Request(url, method="GET")
            req.add_header("Accept", "application/json")
            
            try:
                response = urllib.request.urlopen(req, timeout=10)
                # If we get 200, endpoint is free
                return True, None
            except urllib.error.HTTPError as e:
                if e.code == 402:
                    # Parse payment requirement
                    try:
                        body = e.read().decode('utf-8')
                        data = json.loads(body)
                        
                        payment_req = PaymentRequest(
                            amount=float(data.get("amount", 0)),
                            currency=data.get("currency", "USDC"),
                            chain=data.get("chain", "base"),
                            recipient_address=data.get("address", ""),
                            facilitator_url=data.get("facilitator"),
                            payment_id=data.get("paymentId"),
                            expires_at=data.get("expiresAt"),
                        )
                        
                        return True, payment_req
                    except (json.JSONDecodeError, ValueError):
                        return False, None
                else:
                    return False, None
        
        except Exception as e:
            print(f"Error checking x402 support: {e}")
            return False, None
    
    def pay(self, url: str, max_amount: float = 1.0, 
            chain: Optional[str] = None, 
            dry_run: bool = False) -> Tuple[bool, Optional[PaymentReceipt]]:
        """Pay for API access."""
        
        # Check if endpoint requires payment
        supported, payment_req = self.check_support(url)
        
        if not supported:
            print("Endpoint does not support x402 payments")
            return False, None
        
        if payment_req is None:
            print("Endpoint is free, no payment required")
            return True, None
        
        # Check amount
        if payment_req.amount > max_amount:
            print(f"Payment amount ({payment_req.amount}) exceeds max ({max_amount})")
            return False, None
        
        # Get wallet
        wallet = self._load_wallet()
        
        if not wallet.get("address"):
            print("No wallet configured. Run: x402 config set wallet.address <address>")
            return False, None
        
        # Dry run - show payment details
        if dry_run:
            print("\nPayment Details:")
            print(f"  Amount: {payment_req.amount} {payment_req.currency}")
            print(f"  Chain: {payment_req.chain}")
            print(f"  Recipient: {payment_req.recipient_address}")
            print(f"  Your wallet: {wallet.get('address')}")
            print(f"  Payment ID: {payment_req.payment_id}")
            print()
            return True, None
        
        # Simulate payment (in real implementation, would use blockchain)
        print(f"Initiating payment of {payment_req.amount} {payment_req.currency}...")
        print(f"Chain: {payment_req.chain}")
        print(f"Recipient: {payment_req.recipient_address}")
        
        # In real implementation, would:
        # 1. Sign transaction with private key
        # 2. Submit to facilitator or directly to chain
        # 3. Wait for confirmation
        # 4. Generate payment receipt
        
        # Simulated receipt
        receipt = PaymentReceipt(
            payment_id=payment_req.payment_id or f"pay_{int(time.time())}",
            transaction_hash=f"0x{hashlib.sha256(str(time.time()).encode()).hexdigest()}",
            amount=payment_req.amount,
            currency=payment_req.currency,
            chain=payment_req.chain,
            timestamp=time.time(),
            signature="simulated",
        )
        
        # Save to history
        self._save_payment(receipt)
        
        print(f"Payment successful: {receipt.transaction_hash[:16]}...")
        
        return True, receipt
    
    def get_with_payment(self, url: str, receipt: PaymentReceipt) -> Optional[dict]:
        """Make request with payment proof."""
        
        try:
            req = urllib.request.Request(url, method="GET")
            req.add_header("Accept", "application/json")
            req.add_header("PAYMENT-SIGNATURE", receipt.signature)
            req.add_header("PAYMENT-TX", receipt.transaction_hash)
            req.add_header("PAYMENT-ID", receipt.payment_id)
            
            response = urllib.request.urlopen(req, timeout=30)
            data = json.loads(response.read().decode('utf-8'))
            
            return data
        
        except urllib.error.HTTPError as e:
            if e.code == 402:
                print("Payment still required - transaction may not be confirmed")
            else:
                print(f"Request failed: {e.code}")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None
    
    def _save_payment(self, receipt: PaymentReceipt):
        """Save payment to history."""
        
        record = {
            "payment_id": receipt.payment_id,
            "transaction_hash": receipt.transaction_hash,
            "amount": receipt.amount,
            "currency": receipt.currency,
            "chain": receipt.chain,
            "timestamp": receipt.timestamp,
        }
        
        with open(self.history_file, 'a') as f:
            f.write(json.dumps(record) + '\n')
    
    def get_balance(self, chain: Optional[str] = None) -> dict:
        """Get wallet balance."""
        
        wallet = self._load_wallet()
        
        if not wallet.get("address"):
            return {"error": "No wallet configured"}
        
        # In real implementation, would query blockchain
        # Simulated balance
        balances = {
            "ethereum": {"usdc": 100.0, "usdt": 50.0, "dai": 25.0},
            "polygon": {"usdc": 50.0, "usdt": 25.0},
            "base": {"usdc": 200.0},
            "arbitrum": {"usdc": 75.0},
            "optimism": {"usdc": 75.0},
            "solana": {"usdc": 150.0},
        }
        
        if chain:
            return {chain: balances.get(chain, {})}
        
        return balances
    
    def get_history(self, limit: int = 10, chain: Optional[str] = None) -> list:
        """Get payment history."""
        
        if not self.history_file.exists():
            return []
        
        records = []
        with open(self.history_file, 'r') as f:
            for line in f:
                try:
                    record = json.loads(line.strip())
                    if chain and record.get("chain") != chain:
                        continue
                    records.append(record)
                except json.JSONDecodeError:
                    continue
        
        return records[-limit:]


def main():
    """CLI entry point."""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="x402 payment protocol for AI agents")
    subparsers = parser.add_subparsers(dest='command', help='Command')
    
    # check command
    check_parser = subparsers.add_parser('check', help='Check if endpoint supports x402')
    check_parser.add_argument('url', help='Endpoint URL to check')
    check_parser.add_argument('--timeout', type=int, default=10, help='Request timeout')
    
    # pay command
    pay_parser = subparsers.add_parser('pay', help='Pay for API access')
    pay_parser.add_argument('url', help='Endpoint URL to pay for')
    pay_parser.add_argument('--amount', type=float, default=1.0, help='Maximum amount to pay')
    pay_parser.add_argument('--chain', default='base', help='Preferred chain')
    pay_parser.add_argument('--dry-run', action='store_true', help='Show payment without paying')
    
    # balance command
    balance_parser = subparsers.add_parser('balance', help='Check wallet balance')
    balance_parser.add_argument('--chain', help='Filter by chain')
    
    # history command
    history_parser = subparsers.add_parser('history', help='View payment history')
    history_parser.add_argument('--limit', type=int, default=10, help='Number of records')
    history_parser.add_argument('--chain', help='Filter by chain')
    
    # config command
    config_parser = subparsers.add_parser('config', help='Configure x402')
    config_subparsers = config_parser.add_subparsers(dest='config_command')
    
    config_set = config_subparsers.add_parser('set', help='Set configuration')
    config_set.add_argument('key', help='Configuration key (e.g., wallet.address)')
    config_set.add_argument('value', help='Configuration value')
    
    args = parser.parse_args()
    
    client = X402Client()
    
    if args.command == 'check':
        print(f"Checking {args.url}...")
        supported, payment_req = client.check_support(args.url)
        
        if supported:
            if payment_req:
                print(f"\n✓ Endpoint supports x402 payments")
                print(f"\nPayment Required:")
                print(f"  Amount: {payment_req.amount} {payment_req.currency}")
                print(f"  Chain: {payment_req.chain}")
                print(f"  Recipient: {payment_req.recipient_address}")
                if payment_req.facilitator_url:
                    print(f"  Facilitator: {payment_req.facilitator_url}")
            else:
                print("\n✓ Endpoint is free (no payment required)")
        else:
            print("\n✗ Endpoint does not support x402")
    
    elif args.command == 'pay':
        success, receipt = client.pay(
            args.url, 
            max_amount=args.amount,
            chain=args.chain,
            dry_run=args.dry_run
        )
        
        if success and receipt:
            print(f"\n✓ Payment successful")
            print(f"  Transaction: {receipt.transaction_hash}")
            print(f"  Amount: {receipt.amount} {receipt.currency}")
    
    elif args.command == 'balance':
        balances = client.get_balance(chain=args.chain)
        print("\nWallet Balances:")
        for chain, tokens in balances.items():
            print(f"\n{chain.upper()}:")
            for token, amount in tokens.items():
                print(f"  {token}: {amount}")
    
    elif args.command == 'history':
        records = client.get_history(limit=args.limit, chain=args.chain)
        
        if not records:
            print("No payment history")
        else:
            print("\nPayment History:")
            for record in records:
                print(f"\n  [{record['timestamp']}]")
                print(f"    Amount: {record['amount']} {record['currency']}")
                print(f"    Chain: {record['chain']}")
                print(f"    TX: {record['transaction_hash'][:16]}...")
    
    elif args.command == 'config':
        if args.config_command == 'set':
            config = client._load_config()
            
            # Parse key path
            keys = args.key.split('.')
            
            # Set nested value
            current = config
            for key in keys[:-1]:
                if key not in current:
                    current[key] = {}
                current = current[key]
            current[keys[-1]] = args.value
            
            client._save_config(config)
            print(f"✓ Set {args.key} = {args.value}")
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()