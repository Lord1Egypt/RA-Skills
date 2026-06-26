---
name: greenhelix-strategy-marketplace-playbook
version: "1.3.1"
description: "The Agent Strategy Marketplace Playbook. Complete guide to selling verified trading strategies with escrow-protected subscriptions. Covers marketplace listing, performance verification, subscription management, and dispute resolution."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [trading-bot, guide, escrow, marketplace, greenhelix, openclaw, ai-agent]
price_usd: 0.0
content_type: markdown
executable: false
install: none
credentials: [GREENHELIX_API_KEY, AGENT_SIGNING_KEY]
metadata:
  openclaw:
    requires:
      env:
        - GREENHELIX_API_KEY
        - AGENT_SIGNING_KEY
    primaryEnv: GREENHELIX_API_KEY
---
# The Agent Strategy Marketplace Playbook

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `GREENHELIX_API_KEY`: API authentication for GreenHelix gateway (read/write access to purchased API tools only)
> - `AGENT_SIGNING_KEY`: Cryptographic signing key for agent identity (Ed25519 key pair for request signing)


Trading strategy marketplaces like Cryptohopper, Collective2, and QuantConnect take 20-30% commission on strategy subscriptions while offering nothing more than self-reported, unverifiable performance numbers. Buyers have zero recourse when a strategy that claimed 85% win rate turns out to deliver 40%. Sellers with genuinely profitable strategies cannot differentiate themselves from curve-fitted backtests and outright scammers. The result is a low-trust marketplace where good strategy developers are systematically undervalued, buyers get burned repeatedly, and the platform extracts rent from both sides without adding trust. This guide shows you how to build a strategy selling business on the GreenHelix A2A Commerce Gateway, where performance is cryptographically verified, payments are protected by escrow that releases only when your strategy delivers, and your track record is an immutable Merkle tree that no one --- including you --- can falsify.
1. [Architecture Overview](#chapter-1-architecture-overview)
2. [Setting Up Your Strategy Seller Identity](#chapter-2-setting-up-your-strategy-seller-identity)

## What You'll Learn
- Chapter 1: Architecture Overview
- Chapter 2: Setting Up Your Strategy Seller Identity
- Chapter 3: Listing Your Strategy on the Marketplace
- Chapter 4: Setting Up Performance Escrow
- Chapter 5: Proving Your Performance
- Chapter 6: Handling Disputes
- Chapter 7: Scaling Your Strategy Business
- Chapter 8: Advanced Escrow Patterns
- Chapter 9: Multi-Strategy Portfolio Management
- Chapter 10: Dispute Resolution Workflows

## Full Guide

# The Agent Strategy Marketplace Playbook: Sell Verified Trading Strategies with Escrow-Protected Subscriptions

Trading strategy marketplaces like Cryptohopper, Collective2, and QuantConnect take 20-30% commission on strategy subscriptions while offering nothing more than self-reported, unverifiable performance numbers. Buyers have zero recourse when a strategy that claimed 85% win rate turns out to deliver 40%. Sellers with genuinely profitable strategies cannot differentiate themselves from curve-fitted backtests and outright scammers. The result is a low-trust marketplace where good strategy developers are systematically undervalued, buyers get burned repeatedly, and the platform extracts rent from both sides without adding trust. This guide shows you how to build a strategy selling business on the GreenHelix A2A Commerce Gateway, where performance is cryptographically verified, payments are protected by escrow that releases only when your strategy delivers, and your track record is an immutable Merkle tree that no one --- including you --- can falsify.

---

## Table of Contents

1. [Architecture Overview](#chapter-1-architecture-overview)
2. [Setting Up Your Strategy Seller Identity](#chapter-2-setting-up-your-strategy-seller-identity)
3. [Listing Your Strategy on the Marketplace](#chapter-3-listing-your-strategy-on-the-marketplace)
4. [Setting Up Performance Escrow](#chapter-4-setting-up-performance-escrow)
5. [Proving Your Performance](#chapter-5-proving-your-performance)
6. [Handling Disputes](#chapter-6-handling-disputes)
7. [Scaling Your Strategy Business](#chapter-7-scaling-your-strategy-business)
8. [Advanced Escrow Patterns](#chapter-8-advanced-escrow-patterns)
9. [Multi-Strategy Portfolio Management](#chapter-9-multi-strategy-portfolio-management)
10. [Dispute Resolution Workflows](#chapter-10-dispute-resolution-workflows)
12. [What's Next](#whats-next)

---

## Chapter 1: Architecture Overview

### How the Strategy Marketplace Works

The GreenHelix strategy marketplace operates on a simple loop with four participants: the seller (you), the buyer (a trading bot operator or agent), the escrow system, and the verification layer.

The flow works like this:

1. **Seller lists strategy** on the marketplace with defined performance criteria.
2. **Buyer discovers strategy** via search and subscribes by funding a performance escrow.
3. **Seller executes strategy** and submits signed trade metrics after each execution cycle.
4. **Verification layer** builds a Merkle tree (claim chain) from accumulated metrics.
5. **Escrow auto-releases** if performance criteria are met at the end of the evaluation period.
6. **If criteria are not met**, the buyer can open a dispute, and funds are returned or partially released based on evidence.

### System Flow Diagram

```
+------------------+         +---------------------+         +------------------+
|  Strategy Seller |         |   GreenHelix A2A    |         | Strategy Buyer   |
|  (Your Bot)      |         |   Commerce Gateway  |         | (Subscriber Bot) |
+--------+---------+         +---------+-----------+         +--------+---------+
         |                             |                              |
         | 1. register_agent           |                              |
         |---------------------------->|                              |
         |                             |                              |
         | 2. register_service         |                              |
         |---------------------------->|                              |
         |                             |                              |
         |                             |  3. search_services          |
         |                             |<-----------------------------|
         |                             |                              |
         |                             |  4. create_performance_escrow|
         |                             |<-----------------------------|
         |                             |                              |
         | 5. submit_metrics (daily)   |                              |
         |---------------------------->|                              |
         |                             |                              |
         | 6. build_claim_chain        |                              |
         |---------------------------->|                              |
         |                             |                              |
         |      7. Evaluation period ends                             |
         |         Criteria met? ------+----> release_escrow (auto)   |
         |         Criteria failed? ---+----> open_dispute            |
         |                             |                              |
```

### Why Performance Escrow Changes the Game

Traditional strategy marketplaces are adversarial. The seller's incentive is to overstate performance because there is no penalty for doing so. The buyer's only signal is reviews, which are easily gamed. Performance escrow flips this dynamic: the seller's revenue is directly tied to delivering on stated criteria. If you claim a 2.0 Sharpe ratio over 30 days, you get paid only when the verification layer confirms it. This means honest sellers earn more (because buyers trust the system and subscribe at higher prices), and dishonest sellers earn nothing.

---

## Chapter 2: Setting Up Your Strategy Seller Identity

### Generate an Ed25519 Keypair

Every agent on GreenHelix has a cryptographic identity. You sign your metric submissions with your private key, and anyone can verify them against your public key. This is what makes your track record tamper-proof.

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import base64

# Generate a new Ed25519 keypair
private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

# Serialize the private key (store this securely --- never share it)
private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PrivateFormat.Raw,
    encryption_algorithm=serialization.NoEncryption()
)

# Serialize the public key (this goes in your agent registration)
public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw
)

private_key_b64 = base64.b64encode(private_key_bytes).decode()
public_key_b64 = base64.b64encode(public_key_bytes).decode()

print(f"Private key (keep secret): {private_key_b64}")
print(f"Public key (share freely): {public_key_b64}")
```

Save your private key in an environment variable or secrets manager. Never commit it to version control.

### Register Your Agent on GreenHelix

With your keypair generated, register your identity on the gateway.

**curl:**

```bash
curl -s -X POST https://sandbox.greenhelix.net/v1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GREENHELIX_API_KEY" \
  -d '{
    "tool": "register_agent",
    "input": {
      "agent_id": "strategy-seller-mrev-01",
      "public_key": "'"$PUBLIC_KEY_B64"'",
      "name": "Mean Reversion Strategy v1"
    }
  }'
```

**Python:**

```python
import requests
import os

BASE_URL = "https://api.greenhelix.net/v1"
API_KEY = os.environ["GREENHELIX_API_KEY"]

def execute_tool(tool: str, input_data: dict) -> dict:
    """Execute a tool on the GreenHelix gateway."""
    response = requests.post(
        f"{BASE_URL}/v1",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        json={"tool": tool, "input": input_data},
    )
    response.raise_for_status()
    return response.json()

# Register your agent identity
result = execute_tool("register_agent", {
    "agent_id": "strategy-seller-mrev-01",
    "public_key": public_key_b64,
    "name": "Mean Reversion Strategy v1",
})
print(result)
```

### The Complete GreenHelixClient Class

You will use this client throughout the rest of the guide. It wraps every API call you need into a clean interface.

```python
import requests
import os
import base64
import json
import time
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)
from cryptography.hazmat.primitives import serialization


class GreenHelixClient:
    """Client for the GreenHelix A2A Commerce Gateway."""

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        private_key_b64: str,
        base_url: str = "https://api.greenhelix.net/v1",
    ):
        self.base_url = base_url
        self.agent_id = agent_id
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })

        # Load Ed25519 private key for signing
        private_key_bytes = base64.b64decode(private_key_b64)
        self._private_key = Ed25519PrivateKey.from_private_bytes(
            private_key_bytes
        )
        self._public_key = self._private_key.public_key()

    def _execute(self, tool: str, input_data: dict) -> dict:
        """Execute a tool on the gateway."""
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    def sign_payload(self, payload: dict) -> str:
        """Sign a JSON payload with your Ed25519 private key."""
        payload_bytes = json.dumps(payload, sort_keys=True).encode()
        signature = self._private_key.sign(payload_bytes)
        return base64.b64encode(signature).decode()

    def register(self, name: str) -> dict:
        """Register this agent on the gateway."""
        public_key_bytes = self._public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        return self._execute("register_agent", {
            "agent_id": self.agent_id,
            "public_key": base64.b64encode(public_key_bytes).decode(),
            "name": name,
        })

    def register_service(
        self,
        name: str,
        description: str,
        endpoint: str,
        price: float,
        tags: list[str],
        category: str,
    ) -> dict:
        """List a service on the marketplace."""
        return self._execute("register_service", {
            "name": name,
            "description": description,
            "endpoint": endpoint,
            "price": price,
            "tags": tags,
            "category": category,
        })

    def search_services(self, query: str) -> dict:
        """Search the marketplace."""
        return self._execute("search_services", {"query": query})

    def create_performance_escrow(
        self,
        payer_agent_id: str,
        amount: float,
        currency: str,
        performance_criteria: dict,
        evaluation_period_days: int,
    ) -> dict:
        """Create a performance-based escrow."""
        return self._execute("create_performance_escrow", {
            "payer_agent_id": payer_agent_id,
            "payee_agent_id": self.agent_id,
            "amount": amount,
            "currency": currency,
            "performance_criteria": performance_criteria,
            "evaluation_period_days": evaluation_period_days,
        })

    def release_escrow(self, escrow_id: str) -> dict:
        """Manually release an escrow."""
        return self._execute("release_escrow", {"escrow_id": escrow_id})

    def submit_metrics(self, metrics: dict) -> dict:
        """Submit signed performance metrics."""
        return self._execute("submit_metrics", {
            "agent_id": self.agent_id,
            "metrics": metrics,
        })

    def build_claim_chain(self) -> dict:
        """Build a Merkle tree from your attestation history."""
        return self._execute("build_claim_chain", {
            "agent_id": self.agent_id,
        })

    def get_reputation(self, agent_id: str | None = None) -> dict:
        """Get trust score for an agent."""
        return self._execute("get_agent_reputation", {
            "agent_id": agent_id or self.agent_id,
        })

    def open_dispute(self, escrow_id: str, reason: str) -> dict:
        """Open a dispute on an escrow."""
        return self._execute("open_dispute", {
            "escrow_id": escrow_id,
            "reason": reason,
        })

    def resolve_dispute(self, dispute_id: str, resolution: str) -> dict:
        """Resolve a dispute."""
        return self._execute("resolve_dispute", {
            "dispute_id": dispute_id,
            "resolution": resolution,
        })
```

### Verify Registration

Confirm your agent is registered by checking your reputation endpoint (newly registered agents start with a baseline score).

```bash
curl -s -X POST https://sandbox.greenhelix.net/v1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GREENHELIX_API_KEY" \
  -d '{
    "tool": "get_agent_reputation",
    "input": {
      "agent_id": "strategy-seller-mrev-01"
    }
  }'
```

```python
client = GreenHelixClient(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="strategy-seller-mrev-01",
    private_key_b64=os.environ["GREENHELIX_PRIVATE_KEY"],
)

reputation = client.get_reputation()
print(f"Agent registered. Trust score: {reputation}")
```

---

## Chapter 3: Listing Your Strategy on the Marketplace

### Create a Compelling Service Listing

Your listing is the first thing a potential subscriber sees. It must communicate three things clearly: what the strategy does, what performance it targets, and what the subscription terms are.

Here is an example listing for a mean reversion strategy running on BTC/USDT 1-hour candles.

**curl:**

```bash
curl -s -X POST https://sandbox.greenhelix.net/v1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GREENHELIX_API_KEY" \
  -d '{
    "tool": "register_service",
    "input": {
      "name": "BTC Mean Reversion (1H) - Verified Performance",
      "description": "Automated mean reversion strategy on BTC/USDT 1-hour timeframe. Targets 2.0+ Sharpe ratio with max 8% drawdown. All performance metrics are cryptographically signed and verified via escrow. 30-day evaluation period. Refund if criteria not met.",
      "endpoint": "https://my-bot.example.com/signals/mrev-btc-1h",
      "price": 49.00,
      "tags": ["trading-strategy", "btc", "mean-reversion", "verified-performance", "escrow-protected"],
      "category": "trading-strategies"
    }
  }'
```

**Python:**

```python
listing = client.register_service(
    name="BTC Mean Reversion (1H) - Verified Performance",
    description=(
        "Automated mean reversion strategy on BTC/USDT 1-hour timeframe. "
        "Targets 2.0+ Sharpe ratio with max 8% drawdown. All performance "
        "metrics are cryptographically signed and verified via escrow. "
        "30-day evaluation period. Refund if criteria not met."
    ),
    endpoint="https://my-bot.example.com/signals/mrev-btc-1h",
    price=49.00,
    tags=[
        "trading-strategy",
        "btc",
        "mean-reversion",
        "verified-performance",
        "escrow-protected",
    ],
    category="trading-strategies",
)
print(f"Strategy listed: {listing}")
```

### Pricing Your Strategy

The current market for trading strategy subscriptions runs from $10/month for basic indicator-based strategies up to $99/month or more for verified quantitative strategies. Because GreenHelix performance escrow gives buyers confidence that the numbers are real, you can typically price 20-40% higher than equivalent listings on traditional marketplaces. A strategy with a verified 2.0+ Sharpe ratio and 6+ months of immutable history commands a premium.

Pricing recommendations:
- **$10-25/month**: Simple trend-following or indicator-based strategies with modest performance claims.
- **$25-49/month**: Quantitative strategies with solid risk-adjusted returns and 30-day escrow evaluation.
- **$49-99/month**: Multi-asset or portfolio strategies with longer track records and tighter performance guarantees.

### Tagging for Discovery

Tags determine how buyers find your strategy. Use specific, descriptive tags. Avoid generic terms like "profitable" or "best." Effective tags include the asset pair, timeframe, strategy type, and differentiators like "verified-performance" or "escrow-protected."

### Verify Your Listing Appears in Search

After listing, verify that your strategy is discoverable.

```bash
curl -s -X POST https://sandbox.greenhelix.net/v1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GREENHELIX_API_KEY" \
  -d '{
    "tool": "search_services",
    "input": {
      "query": "btc mean reversion verified"
    }
  }'
```

```python
results = client.search_services("btc mean reversion verified")
for service in results.get("services", []):
    print(f"  {service['name']} - ${service['price']}/mo")
```

---

## Chapter 4: Setting Up Performance Escrow

### How Performance Escrow Works

When a buyer subscribes to your strategy, they do not pay you directly. Instead, funds are locked in a performance escrow with explicit criteria that must be met over a defined evaluation period. At the end of the period, one of three things happens:

1. **Criteria met**: Escrow auto-releases to you. You get paid.
2. **Criteria partially met**: Buyer can accept and release, or dispute for partial refund.
3. **Criteria not met**: Buyer opens a dispute. Funds are returned or split based on evidence.

This is what makes the system work. Buyers subscribe with near-zero risk. Sellers with good strategies earn consistently. Sellers with bad strategies earn nothing --- which is exactly how it should be.

### Define Performance Criteria

Performance criteria are the contract between you and your subscriber. Be specific and conservative. It is far better to promise a 1.5 Sharpe and deliver 2.0 than to promise 3.0 and miss. Here is a well-structured performance criteria object:

```python
performance_criteria = {
    "min_sharpe_ratio": 1.5,
    "max_drawdown_pct": 10.0,
    "min_win_rate_pct": 55.0,
    "min_total_trades": 20,
}
```

- **min_sharpe_ratio**: Risk-adjusted return. 1.5+ is solid for a 30-day window.
- **max_drawdown_pct**: Maximum peak-to-trough decline. 10% gives you room for normal volatility.
- **min_win_rate_pct**: Percentage of winning trades. 55% is realistic for mean reversion.
- **min_total_trades**: Minimum number of trades. Prevents gaming by taking one lucky trade.

### Create Escrow When a Subscriber Signs Up

When a buyer agent subscribes, you (or your automation) create the performance escrow.

**curl:**

```bash
curl -s -X POST https://sandbox.greenhelix.net/v1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GREENHELIX_API_KEY" \
  -d '{
    "tool": "create_performance_escrow",
    "input": {
      "payer_agent_id": "subscriber-bot-alpha",
      "payee_agent_id": "strategy-seller-mrev-01",
      "amount": 49.00,
      "currency": "USD",
      "performance_criteria": {
        "min_sharpe_ratio": 1.5,
        "max_drawdown_pct": 10.0,
        "min_win_rate_pct": 55.0,
        "min_total_trades": 20
      },
      "evaluation_period_days": 30
    }
  }'
```

**Python:**

```python
escrow = client.create_performance_escrow(
    payer_agent_id="subscriber-bot-alpha",
    amount=49.00,
    currency="USD",
    performance_criteria={
        "min_sharpe_ratio": 1.5,
        "max_drawdown_pct": 10.0,
        "min_win_rate_pct": 55.0,
        "min_total_trades": 20,
    },
    evaluation_period_days=30,
)
escrow_id = escrow["escrow_id"]
print(f"Escrow created: {escrow_id}")
print(f"Evaluation ends: {escrow['evaluation_end_date']}")
```

### Complete Escrow Creation Flow

In production, you will automate this entire flow. Here is the pattern: when your endpoint receives a subscription request, validate the buyer agent, create the escrow, and return the escrow ID so both parties can track it.

```python
def handle_subscription_request(buyer_agent_id: str, plan: str) -> dict:
    """Handle an incoming subscription request from a buyer agent."""
    plans = {
        "basic": {
            "amount": 29.00,
            "criteria": {
                "min_sharpe_ratio": 1.2,
                "max_drawdown_pct": 12.0,
                "min_win_rate_pct": 52.0,
                "min_total_trades": 15,
            },
            "evaluation_days": 30,
        },
        "premium": {
            "amount": 49.00,
            "criteria": {
                "min_sharpe_ratio": 1.5,
                "max_drawdown_pct": 10.0,
                "min_win_rate_pct": 55.0,
                "min_total_trades": 20,
            },
            "evaluation_days": 30,
        },
    }

    if plan not in plans:
        return {"error": f"Unknown plan: {plan}. Available: {list(plans)}"}

    config = plans[plan]
    escrow = client.create_performance_escrow(
        payer_agent_id=buyer_agent_id,
        amount=config["amount"],
        currency="USD",
        performance_criteria=config["criteria"],
        evaluation_period_days=config["evaluation_days"],
    )

    return {
        "status": "subscribed",
        "escrow_id": escrow["escrow_id"],
        "plan": plan,
        "evaluation_end_date": escrow["evaluation_end_date"],
        "criteria": config["criteria"],
    }
```

---

## Chapter 5: Proving Your Performance

### Submit Trade Metrics After Each Execution

Every time your strategy executes trades, submit the results to GreenHelix. These metrics are what the escrow system evaluates at the end of the period. Submit daily or after each significant trade batch.

**curl:**

```bash
curl -s -X POST https://sandbox.greenhelix.net/v1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GREENHELIX_API_KEY" \
  -d '{
    "tool": "submit_metrics",
    "input": {
      "agent_id": "strategy-seller-mrev-01",
      "metrics": {
        "period_start": "2026-04-01T00:00:00Z",
        "period_end": "2026-04-01T23:59:59Z",
        "trades_executed": 7,
        "winning_trades": 5,
        "losing_trades": 2,
        "total_pnl_usd": 342.18,
        "max_drawdown_pct": 2.3,
        "sharpe_ratio": 2.14,
        "win_rate_pct": 71.4,
        "avg_trade_duration_minutes": 47,
        "pairs_traded": ["BTC/USDT"]
      }
    }
  }'
```

**Python:**

```python
from datetime import datetime, timezone

daily_metrics = {
    "period_start": "2026-04-01T00:00:00Z",
    "period_end": "2026-04-01T23:59:59Z",
    "trades_executed": 7,
    "winning_trades": 5,
    "losing_trades": 2,
    "total_pnl_usd": 342.18,
    "max_drawdown_pct": 2.3,
    "sharpe_ratio": 2.14,
    "win_rate_pct": 71.4,
    "avg_trade_duration_minutes": 47,
    "pairs_traded": ["BTC/USDT"],
}

result = client.submit_metrics(daily_metrics)
print(f"Metrics submitted: {result}")
```

### Automated Metrics Submission Pipeline

In production, you will run a daily job that computes your strategy's metrics from your trade log and submits them automatically. Here is a complete pipeline:

```python
import json
from datetime import datetime, timedelta, timezone


def compute_daily_metrics(trades: list[dict], date: str) -> dict:
    """Compute strategy metrics from a list of executed trades for a day."""
    if not trades:
        return None

    winning = [t for t in trades if t["pnl"] > 0]
    losing = [t for t in trades if t["pnl"] <= 0]
    total_pnl = sum(t["pnl"] for t in trades)

    # Compute rolling Sharpe from daily returns
    returns = [t["pnl"] / t["position_size"] for t in trades]
    avg_return = sum(returns) / len(returns)
    if len(returns) > 1:
        variance = sum((r - avg_return) ** 2 for r in returns) / (
            len(returns) - 1
        )
        std_return = variance ** 0.5
        sharpe = (avg_return / std_return) * (252 ** 0.5) if std_return > 0 else 0.0
    else:
        sharpe = 0.0

    # Compute max drawdown from cumulative P&L
    cumulative = []
    running = 0.0
    peak = 0.0
    max_dd = 0.0
    for t in trades:
        running += t["pnl"]
        cumulative.append(running)
        if running > peak:
            peak = running
        dd = (peak - running) / peak * 100 if peak > 0 else 0.0
        if dd > max_dd:
            max_dd = dd

    return {
        "period_start": f"{date}T00:00:00Z",
        "period_end": f"{date}T23:59:59Z",
        "trades_executed": len(trades),
        "winning_trades": len(winning),
        "losing_trades": len(losing),
        "total_pnl_usd": round(total_pnl, 2),
        "max_drawdown_pct": round(max_dd, 2),
        "sharpe_ratio": round(sharpe, 2),
        "win_rate_pct": round(len(winning) / len(trades) * 100, 1),
        "pairs_traded": list(set(t["pair"] for t in trades)),
    }


def daily_metrics_job(client: GreenHelixClient, trades: list[dict]):
    """Run as a daily cron job to submit metrics."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    metrics = compute_daily_metrics(trades, today)
    if metrics:
        result = client.submit_metrics(metrics)
        print(f"[{today}] Metrics submitted: {result}")
    else:
        print(f"[{today}] No trades executed, skipping submission.")
```

### Build Claim Chains

After accumulating metric submissions, build your claim chain. This creates a Merkle tree from your attestation history --- an append-only, tamper-evident data structure that anyone can verify. Each new metric submission becomes a leaf node, and the root hash changes with every update, making historical falsification detectable.

**curl:**

```bash
curl -s -X POST https://sandbox.greenhelix.net/v1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GREENHELIX_API_KEY" \
  -d '{
    "tool": "build_claim_chain",
    "input": {
      "agent_id": "strategy-seller-mrev-01"
    }
  }'
```

**Python:**

```python
claim_chain = client.build_claim_chain()
print(f"Claim chain root: {claim_chain.get('root_hash')}")
print(f"Total attestations: {claim_chain.get('attestation_count')}")
print(f"Chain depth: {claim_chain.get('depth')}")
```

Build your claim chain regularly --- at least weekly, ideally daily after metrics submission. A longer, unbroken chain is a stronger trust signal. Subscribers and potential buyers can verify any leaf in the tree independently, which is why this system is fundamentally different from self-reported numbers on traditional platforms.

### How Trust Scores Are Computed

Your reputation score on GreenHelix is derived from several factors:

- **Claim chain length and consistency**: Longer chains with regular submissions score higher.
- **Escrow completion rate**: The percentage of escrows that auto-release (criteria met) vs. disputed.
- **Metric variance**: Consistent performance across periods scores higher than volatile results.
- **Dispute history**: Disputes that resolve in your favor are neutral; disputes you lose drag the score down.

Check your trust score at any time:

```python
reputation = client.get_reputation()
print(f"Trust score: {reputation.get('score')}")
print(f"Escrow completion rate: {reputation.get('escrow_completion_rate')}")
print(f"Total escrows completed: {reputation.get('total_escrows')}")
```

---

## Chapter 6: Handling Disputes

### When a Subscriber Opens a Dispute

A subscriber can open a dispute on an active escrow if they believe your strategy has not met the stated performance criteria. Disputes are not adversarial by design --- they are a resolution mechanism.

```python
# From the subscriber's perspective:
dispute = client.open_dispute(
    escrow_id="escrow-abc123",
    reason=(
        "Strategy claimed min 1.5 Sharpe over 30 days. "
        "Actual Sharpe was 0.87 based on submitted metrics. "
        "Requesting full refund per escrow terms."
    ),
)
print(f"Dispute opened: {dispute['dispute_id']}")
```

### How to Respond with Evidence

When a dispute is opened against your escrow, your primary evidence is your claim chain. Because every metric submission is a signed, timestamped leaf in a Merkle tree, you can prove exactly what you submitted and when. If the metrics genuinely show you met the criteria, the evidence speaks for itself.

```python
# Build your claim chain as evidence
claim_chain = client.build_claim_chain()

# The claim chain contains all signed metric submissions
# The resolver can verify each leaf against your public key
print(f"Evidence submitted via claim chain: {claim_chain['root_hash']}")
print(f"Attestations available for review: {claim_chain['attestation_count']}")
```

### Resolution Outcomes

Disputes resolve in one of three ways:

1. **Full release to seller**: Metrics clearly show criteria were met. The subscriber's dispute was unfounded.
2. **Full refund to buyer**: Metrics show criteria were not met. Funds return to the subscriber.
3. **Partial release**: Performance was close to criteria but fell short on one metric. Funds are split proportionally.

```bash
# Resolve a dispute (typically done by the platform or arbitrator)
curl -s -X POST https://sandbox.greenhelix.net/v1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GREENHELIX_API_KEY" \
  -d '{
    "tool": "resolve_dispute",
    "input": {
      "dispute_id": "dispute-xyz789",
      "resolution": "release_to_seller"
    }
  }'
```

### Best Practices for Avoiding Disputes

1. **Set conservative criteria.** Promise less, deliver more. A 1.5 Sharpe target with 2.0 delivery builds your reputation faster than a 3.0 target you occasionally miss.
2. **Submit metrics daily.** Gaps in your metric history look suspicious and weaken your position in disputes.
3. **Communicate proactively.** If your strategy hits a rough patch (high drawdown, low trade count), reach out to subscribers before the escrow evaluation period ends.
4. **Keep your claim chain current.** Build it after every metric submission. A stale chain is harder to defend with.

---

## Chapter 7: Scaling Your Strategy Business

### Multiple Strategies, Tiered Pricing

Once your first strategy has a solid track record (3+ months of verified performance, 90%+ escrow completion rate), expand. List multiple strategies with different risk profiles and price points.

```python
strategies = [
    {
        "name": "BTC Mean Reversion (1H) - Conservative",
        "price": 29.00,
        "criteria": {"min_sharpe_ratio": 1.2, "max_drawdown_pct": 8.0},
        "tags": ["btc", "mean-reversion", "conservative", "verified-performance"],
    },
    {
        "name": "BTC Mean Reversion (1H) - Aggressive",
        "price": 49.00,
        "criteria": {"min_sharpe_ratio": 2.0, "max_drawdown_pct": 15.0},
        "tags": ["btc", "mean-reversion", "aggressive", "verified-performance"],
    },
    {
        "name": "Multi-Asset Momentum Portfolio",
        "price": 99.00,
        "criteria": {"min_sharpe_ratio": 1.8, "max_drawdown_pct": 12.0},
        "tags": ["multi-asset", "momentum", "portfolio", "verified-performance"],
    },
]

for strat in strategies:
    result = client.register_service(
        name=strat["name"],
        description=f"Verified performance strategy. Escrow-protected with {strat['criteria']['min_sharpe_ratio']}+ Sharpe target.",
        endpoint="https://my-bot.example.com/signals/" + strat["name"].lower().replace(" ", "-"),
        price=strat["price"],
        tags=strat["tags"],
        category="trading-strategies",
    )
    print(f"Listed: {strat['name']} at ${strat['price']}/mo")
```

### Using Analytics to Track Subscriber Growth

Monitor your reputation and escrow metrics to understand your business trajectory.

```python
def print_business_dashboard(client: GreenHelixClient):
    """Print a summary of your strategy business metrics."""
    reputation = client.get_reputation()

    print("=== Strategy Business Dashboard ===")
    print(f"Trust Score:            {reputation.get('score', 'N/A')}")
    print(f"Escrow Completion Rate: {reputation.get('escrow_completion_rate', 'N/A')}")
    print(f"Total Escrows:          {reputation.get('total_escrows', 'N/A')}")
    print(f"Active Disputes:        {reputation.get('active_disputes', 0)}")
    print("===================================")

print_business_dashboard(client)
```

### Cross-Selling Between Strategies

Subscribers who are happy with one strategy are your best prospects for another. When a subscriber's escrow completes successfully (criteria met, funds released), that is the ideal moment to suggest your other strategies. The verified track record from the first subscription is your strongest sales tool for the second.

### Monitoring Your Reputation Score

Your trust score is the single most important metric for long-term strategy sales growth. It compounds: higher trust scores lead to more subscribers, more successful escrows lead to higher scores, and the cycle reinforces itself. Check your score weekly and investigate any dips immediately.

```python
# Weekly reputation check
reputation = client.get_reputation()
score = reputation.get("score", 0)
if score < 0.8:
    print(f"WARNING: Trust score dropped to {score}. Investigate recent escrows.")
elif score >= 0.95:
    print(f"Trust score: {score} - Excellent. Consider raising prices.")
else:
    print(f"Trust score: {score} - Healthy.")
```

---

## Chapter 8: Advanced Escrow Patterns

### Multi-Tier Escrow

Chapter 4 introduced a basic two-tier plan structure. In practice, you will want to define escrow criteria that scale with the subscription price and the buyer's risk appetite. Multi-tier escrow means each plan tier has its own performance criteria, evaluation period, and escrow amount --- and the criteria get progressively stricter as the price increases.

The key insight is that higher-tier subscribers are paying more because they expect tighter performance guarantees. A $99/month premium subscriber should not have the same 1.2 Sharpe threshold as a $29/month basic subscriber. The escrow criteria must reflect the price.

```python
TIER_CONFIGS = {
    "starter": {
        "amount": 19.00,
        "criteria": {
            "min_sharpe_ratio": 1.0,
            "max_drawdown_pct": 15.0,
            "min_win_rate_pct": 50.0,
            "min_total_trades": 10,
        },
        "evaluation_days": 14,
    },
    "standard": {
        "amount": 49.00,
        "criteria": {
            "min_sharpe_ratio": 1.5,
            "max_drawdown_pct": 10.0,
            "min_win_rate_pct": 55.0,
            "min_total_trades": 20,
        },
        "evaluation_days": 30,
    },
    "professional": {
        "amount": 99.00,
        "criteria": {
            "min_sharpe_ratio": 2.0,
            "max_drawdown_pct": 7.0,
            "min_win_rate_pct": 60.0,
            "min_total_trades": 30,
        },
        "evaluation_days": 30,
    },
    "institutional": {
        "amount": 249.00,
        "criteria": {
            "min_sharpe_ratio": 2.5,
            "max_drawdown_pct": 5.0,
            "min_win_rate_pct": 62.0,
            "min_total_trades": 40,
            "max_consecutive_losses": 4,
            "min_profit_factor": 1.8,
        },
        "evaluation_days": 60,
    },
}


def create_tiered_escrow(
    client: GreenHelixClient, buyer_agent_id: str, tier: str
) -> dict:
    """Create an escrow with tier-appropriate criteria."""
    if tier not in TIER_CONFIGS:
        raise ValueError(f"Unknown tier: {tier}. Available: {list(TIER_CONFIGS)}")

    config = TIER_CONFIGS[tier]
    escrow = client.create_performance_escrow(
        payer_agent_id=buyer_agent_id,
        amount=config["amount"],
        currency="USD",
        performance_criteria=config["criteria"],
        evaluation_period_days=config["evaluation_days"],
    )
    return {
        "tier": tier,
        "escrow_id": escrow["escrow_id"],
        "criteria": config["criteria"],
        "evaluation_end_date": escrow["evaluation_end_date"],
    }
```

Notice the institutional tier adds two additional criteria fields: `max_consecutive_losses` and `min_profit_factor`. Higher tiers can include stricter and more granular performance requirements. This is a competitive advantage --- no traditional marketplace can enforce these guarantees programmatically.

### Rolling Escrow

Fixed 30-day escrow periods create a problem: the subscriber pays on day 1 and waits 30 days for the evaluation. If the strategy fails on day 29, the subscriber wasted a month. Rolling escrow solves this by creating a continuous 30-day evaluation window that slides forward with each new metric submission. Instead of a single fixed window, the system evaluates the most recent 30 days of data at any point.

The implementation pattern is to create overlapping escrows that renew automatically. When one evaluation period completes successfully, a new escrow is created immediately for the next period, giving both parties continuous coverage.

```python
from datetime import datetime, timedelta, timezone


class RollingEscrowManager:
    """Manage continuous rolling escrow windows for a strategy subscription."""

    def __init__(self, client: GreenHelixClient, window_days: int = 30):
        self.client = client
        self.window_days = window_days
        self.active_escrows: dict[str, dict] = {}

    def start_subscription(
        self, buyer_agent_id: str, amount: float, criteria: dict
    ) -> dict:
        """Start a rolling escrow subscription."""
        escrow = self.client.create_performance_escrow(
            payer_agent_id=buyer_agent_id,
            amount=amount,
            currency="USD",
            performance_criteria=criteria,
            evaluation_period_days=self.window_days,
        )
        self.active_escrows[buyer_agent_id] = {
            "escrow_id": escrow["escrow_id"],
            "started": datetime.now(timezone.utc).isoformat(),
            "amount": amount,
            "criteria": criteria,
        }
        return escrow

    def check_and_renew(self, buyer_agent_id: str) -> dict | None:
        """Check if an escrow period ended and auto-renew if successful."""
        if buyer_agent_id not in self.active_escrows:
            return None

        current = self.active_escrows[buyer_agent_id]
        escrow_id = current["escrow_id"]

        # Attempt to release the current escrow (criteria met)
        try:
            release = self.client.release_escrow(escrow_id)
            if release.get("status") == "released":
                # Criteria met --- create the next rolling window
                new_escrow = self.client.create_performance_escrow(
                    payer_agent_id=buyer_agent_id,
                    amount=current["amount"],
                    currency="USD",
                    performance_criteria=current["criteria"],
                    evaluation_period_days=self.window_days,
                )
                self.active_escrows[buyer_agent_id] = {
                    "escrow_id": new_escrow["escrow_id"],
                    "started": datetime.now(timezone.utc).isoformat(),
                    "amount": current["amount"],
                    "criteria": current["criteria"],
                }
                return {"renewed": True, "new_escrow_id": new_escrow["escrow_id"]}
        except Exception as e:
            return {"renewed": False, "error": str(e)}

        return {"renewed": False, "reason": "evaluation_period_active"}
```

Run `check_and_renew` as a daily cron job for each active subscriber. When the evaluation period ends and criteria are met, the escrow releases and a new one is created seamlessly. The subscriber never has a gap in coverage, and you never have a gap in revenue.

### Conditional Escrow Release

Not all strategies deliver linearly. A momentum strategy might underperform for two weeks, then capture a large move that puts it well above the target. Conditional escrow release handles this by allowing partial release at defined milestones within the evaluation period.

The pattern is to define milestone checkpoints --- for example, at day 10, day 20, and day 30 --- and release a fraction of the escrow at each checkpoint if the interim criteria are met.

```python
MILESTONE_SCHEDULE = [
    {"day": 10, "release_pct": 25, "min_sharpe_ratio": 1.0, "max_drawdown_pct": 12.0},
    {"day": 20, "release_pct": 25, "min_sharpe_ratio": 1.3, "max_drawdown_pct": 10.0},
    {"day": 30, "release_pct": 50, "min_sharpe_ratio": 1.5, "max_drawdown_pct": 10.0},
]


def evaluate_milestone(
    client: GreenHelixClient,
    escrow_id: str,
    current_metrics: dict,
    milestone: dict,
) -> dict:
    """Evaluate whether a milestone's criteria are met for partial release."""
    sharpe_ok = current_metrics.get("sharpe_ratio", 0) >= milestone["min_sharpe_ratio"]
    dd_ok = current_metrics.get("max_drawdown_pct", 100) <= milestone["max_drawdown_pct"]

    if sharpe_ok and dd_ok:
        # Request partial release
        result = client._execute("release_escrow", {
            "escrow_id": escrow_id,
            "release_percentage": milestone["release_pct"],
        })
        return {
            "milestone_day": milestone["day"],
            "released_pct": milestone["release_pct"],
            "status": "released",
        }
    else:
        return {
            "milestone_day": milestone["day"],
            "released_pct": 0,
            "status": "deferred",
            "reason": f"Sharpe: {current_metrics.get('sharpe_ratio')} "
                      f"(need {milestone['min_sharpe_ratio']}), "
                      f"DD: {current_metrics.get('max_drawdown_pct')}% "
                      f"(max {milestone['max_drawdown_pct']}%)",
        }
```

Conditional release reduces the seller's cash flow risk. Even if day 30 performance dips slightly, you have already received 50% of the escrow from earlier milestones. For buyers, it provides earlier signal on whether the strategy is performing --- if no milestones are hit by day 20, they know to prepare a dispute.

### Escrow Stacking

When multiple subscribers are all following the same strategy, their escrows are evaluated independently, but the risk is correlated. If the strategy has a bad month, every subscriber's escrow is at risk simultaneously. Escrow stacking is the practice of managing aggregate risk across all active escrows for a single strategy.

```python
def calculate_escrow_exposure(
    client: GreenHelixClient, active_escrow_ids: list[str]
) -> dict:
    """Calculate total exposure across all active escrows for a strategy."""
    total_locked = 0.0
    escrow_details = []

    for eid in active_escrow_ids:
        # In production, you would track these in your own database
        escrow_details.append({"escrow_id": eid})

    # Aggregate risk metrics
    return {
        "total_escrows": len(active_escrow_ids),
        "total_locked_usd": total_locked,
        "max_loss_if_all_fail": total_locked,
        "escrows": escrow_details,
    }


def should_accept_new_subscriber(
    active_escrow_count: int,
    max_concurrent_escrows: int = 50,
    current_sharpe: float = 0.0,
    min_sharpe_for_new_subs: float = 1.2,
) -> bool:
    """Determine if you should accept a new subscriber based on current risk."""
    if active_escrow_count >= max_concurrent_escrows:
        return False  # Capacity limit reached
    if current_sharpe < min_sharpe_for_new_subs:
        return False  # Performance too weak to take on more risk
    return True
```

The rule of thumb is simple: do not accept new subscribers when your strategy is underperforming. Every new escrow during a drawdown is additional capital at risk. Set a capacity limit and a minimum current performance threshold. When your strategy is running well, open the gates. When it is struggling, close them until performance recovers. This protects both your revenue and your reputation score.

### Escrow Monitoring Dashboard

With multiple escrow patterns running simultaneously --- tiered, rolling, conditional, stacked --- you need a centralized view of all active escrows and their status. Build a monitoring function that aggregates escrow state across all subscribers and flags any that require attention.

```python
def escrow_dashboard(
    client: GreenHelixClient,
    active_escrows: list[dict],
) -> dict:
    """Generate a dashboard view of all active escrows."""
    summary = {
        "total_active": len(active_escrows),
        "total_locked_usd": sum(e.get("amount", 0) for e in active_escrows),
        "expiring_within_7_days": [],
        "at_risk": [],
        "on_track": [],
    }

    now = datetime.now(timezone.utc)
    for escrow in active_escrows:
        end_date = datetime.fromisoformat(
            escrow.get("evaluation_end_date", "").replace("Z", "+00:00")
        )
        days_remaining = (end_date - now).days

        entry = {
            "escrow_id": escrow["escrow_id"],
            "subscriber": escrow.get("payer_agent_id", "unknown"),
            "amount": escrow.get("amount", 0),
            "days_remaining": days_remaining,
            "tier": escrow.get("tier", "standard"),
        }

        if days_remaining <= 7:
            summary["expiring_within_7_days"].append(entry)
        # In production, cross-reference with current metrics to classify
        summary["on_track"].append(entry)

    print(f"=== Escrow Dashboard ===")
    print(f"Active escrows:      {summary['total_active']}")
    print(f"Total locked:        ${summary['total_locked_usd']:.2f}")
    print(f"Expiring soon (<7d): {len(summary['expiring_within_7_days'])}")
    print(f"========================")
    return summary
```

The dashboard should run on a schedule --- at least daily, ideally hourly during active trading sessions. Pipe the output into your monitoring system so that expiring escrows and at-risk positions show up in Grafana or your alerting tool of choice. The goal is to never be surprised by an escrow evaluation outcome. If you know 5 days in advance that an escrow is at risk, you have time to either improve performance or proactively communicate with the subscriber.

### When to Use Which Pattern

Choosing the right escrow pattern depends on your strategy's characteristics and your subscriber base:

- **Multi-tier escrow** is best when you serve diverse subscribers with different budgets and risk tolerances. It lets you capture revenue from beginners ($19/month starter tier) and institutions ($249/month) simultaneously.
- **Rolling escrow** is ideal for strategies with consistent, predictable performance. It eliminates gaps between evaluation periods and provides continuous revenue flow.
- **Conditional escrow** works best for strategies with uneven return profiles --- momentum strategies that have quiet periods followed by large gains. Milestones let you capture partial revenue even during drawdowns.
- **Escrow stacking** is a risk management pattern, not a pricing pattern. Use it whenever you have more than 10 concurrent subscribers on a single strategy to prevent correlated losses from wiping out an entire month of revenue.

Most production strategy sellers use a combination: multi-tier pricing with rolling escrow for their flagship strategy, conditional escrow for newer or more volatile strategies, and stacking limits across the board.

---

## Chapter 9: Multi-Strategy Portfolio Management

### Running Multiple Strategies Simultaneously

A single strategy is a single point of failure. Market regimes change, and the mean reversion strategy that printed money in a range-bound market will bleed during a strong trend. The solution is to run multiple strategies simultaneously, each targeting different market conditions, and manage them as a portfolio.

The first step is to register each strategy as a separate service on the marketplace, each with its own agent identity.

```python
STRATEGY_AGENTS = {
    "mrev-btc-1h": {
        "agent_id": "strategy-seller-mrev-01",
        "name": "BTC Mean Reversion (1H)",
        "category": "mean-reversion",
        "pairs": ["BTC/USDT"],
    },
    "momentum-eth-4h": {
        "agent_id": "strategy-seller-mom-02",
        "name": "ETH Momentum (4H)",
        "category": "momentum",
        "pairs": ["ETH/USDT"],
    },
    "arb-cross-exchange": {
        "agent_id": "strategy-seller-arb-03",
        "name": "Cross-Exchange Arbitrage",
        "category": "arbitrage",
        "pairs": ["BTC/USDT", "ETH/USDT", "SOL/USDT"],
    },
    "vol-btc-perp": {
        "agent_id": "strategy-seller-vol-04",
        "name": "BTC Volatility Harvest (Perps)",
        "category": "volatility",
        "pairs": ["BTC/USDT-PERP"],
    },
    "trend-multi-asset": {
        "agent_id": "strategy-seller-trend-05",
        "name": "Multi-Asset Trend Following",
        "category": "trend-following",
        "pairs": ["BTC/USDT", "ETH/USDT", "SOL/USDT", "AVAX/USDT"],
    },
}


def register_all_strategies(api_key: str, private_key_b64: str):
    """Register all strategy agents and list them on the marketplace."""
    clients = {}
    for key, config in STRATEGY_AGENTS.items():
        c = GreenHelixClient(
            api_key=api_key,
            agent_id=config["agent_id"],
            private_key_b64=private_key_b64,
            base_url="https://api.greenhelix.net/v1",
        )
        c.register(config["name"])
        c.register_service(
            name=config["name"],
            description=f"Verified {config['category']} strategy on {', '.join(config['pairs'])}.",
            endpoint=f"https://my-bot.example.com/signals/{key}",
            price=49.00,
            tags=[config["category"], "verified-performance", "escrow-protected"]
                 + [p.lower().replace("/", "-") for p in config["pairs"]],
            category="trading-strategies",
        )
        clients[key] = c
        print(f"Registered: {config['name']}")
    return clients
```

### Portfolio-Level Risk Management

Running five strategies independently is not portfolio management. Portfolio management means tracking aggregate risk across all strategies and making allocation decisions based on the combined picture. The key metrics to track at the portfolio level are total drawdown, total exposure, and cross-strategy correlation.

```python
def compute_portfolio_metrics(
    strategy_metrics: dict[str, dict],
) -> dict:
    """Compute aggregate portfolio metrics across all active strategies."""
    total_pnl = 0.0
    max_drawdown = 0.0
    total_trades = 0
    winning_trades = 0
    all_returns = []

    for name, metrics in strategy_metrics.items():
        total_pnl += metrics.get("total_pnl_usd", 0.0)
        dd = metrics.get("max_drawdown_pct", 0.0)
        if dd > max_drawdown:
            max_drawdown = dd
        total_trades += metrics.get("trades_executed", 0)
        winning_trades += metrics.get("winning_trades", 0)
        # Collect per-strategy returns for correlation analysis
        if "daily_returns" in metrics:
            all_returns.append(metrics["daily_returns"])

    portfolio_win_rate = (
        (winning_trades / total_trades * 100) if total_trades > 0 else 0.0
    )

    return {
        "total_pnl_usd": round(total_pnl, 2),
        "max_drawdown_pct": round(max_drawdown, 2),
        "total_trades": total_trades,
        "portfolio_win_rate_pct": round(portfolio_win_rate, 1),
        "strategy_count": len(strategy_metrics),
    }
```

### Correlation Monitoring

The worst thing that can happen to a multi-strategy portfolio is correlated drawdowns. If your mean reversion and momentum strategies both lose money at the same time, diversification is not working. Monitor the correlation between strategy returns and adjust allocations when correlation spikes.

```python
def compute_correlation(returns_a: list[float], returns_b: list[float]) -> float:
    """Compute Pearson correlation between two return series."""
    n = min(len(returns_a), len(returns_b))
    if n < 5:
        return 0.0  # Not enough data

    a = returns_a[:n]
    b = returns_b[:n]
    mean_a = sum(a) / n
    mean_b = sum(b) / n

    cov = sum((a[i] - mean_a) * (b[i] - mean_b) for i in range(n)) / (n - 1)
    std_a = (sum((x - mean_a) ** 2 for x in a) / (n - 1)) ** 0.5
    std_b = (sum((x - mean_b) ** 2 for x in b) / (n - 1)) ** 0.5

    if std_a == 0 or std_b == 0:
        return 0.0

    return round(cov / (std_a * std_b), 4)


def monitor_correlations(
    strategy_returns: dict[str, list[float]], threshold: float = 0.7
) -> list[dict]:
    """Flag strategy pairs with correlation above the threshold."""
    alerts = []
    names = list(strategy_returns.keys())
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            corr = compute_correlation(
                strategy_returns[names[i]], strategy_returns[names[j]]
            )
            if abs(corr) >= threshold:
                alerts.append({
                    "strategy_a": names[i],
                    "strategy_b": names[j],
                    "correlation": corr,
                    "action": "reduce_allocation" if corr > 0 else "monitor",
                })
    return alerts
```

When two strategies show correlation above 0.7, you have two options: reduce allocation to one of them, or pause new subscriber intake on one until the correlation drops. The goal is to maintain genuine diversification at the portfolio level, which keeps your aggregate escrow completion rate high even when individual strategies hit rough patches.

### Capital Allocation and Rebalancing

Not all strategies deserve equal capital allocation. A strategy with a 6-month verified track record and 95% escrow completion rate should get more capital and more subscriber slots than a strategy you launched last week. Rebalancing means periodically adjusting how many subscribers each strategy accepts and what price point each strategy targets.

```python
def compute_allocation_weights(
    strategy_stats: dict[str, dict],
) -> dict[str, float]:
    """Compute allocation weights based on risk-adjusted performance."""
    weights = {}
    total_score = 0.0

    for name, stats in strategy_stats.items():
        sharpe = stats.get("sharpe_ratio", 0.0)
        completion_rate = stats.get("escrow_completion_rate", 0.5)
        months_active = stats.get("months_active", 1)

        # Score: Sharpe * completion rate * log(months + 1)
        import math
        score = max(0.0, sharpe) * completion_rate * math.log(months_active + 1)
        weights[name] = score
        total_score += score

    # Normalize to percentages
    if total_score > 0:
        for name in weights:
            weights[name] = round(weights[name] / total_score * 100, 1)

    return weights
```

### Strategy Rotation Based on Market Regime

Market regimes --- trending, range-bound, high-volatility, low-volatility --- favor different strategy types. A simple regime detection system can guide which strategies to promote and which to pause.

```python
def detect_market_regime(
    recent_prices: list[float], lookback: int = 30
) -> str:
    """Detect the current market regime from recent price data."""
    if len(recent_prices) < lookback:
        return "unknown"

    prices = recent_prices[-lookback:]
    returns = [(prices[i] - prices[i - 1]) / prices[i - 1] for i in range(1, len(prices))]

    avg_return = sum(returns) / len(returns)
    volatility = (sum((r - avg_return) ** 2 for r in returns) / len(returns)) ** 0.5
    trend_strength = abs(avg_return) / volatility if volatility > 0 else 0

    if volatility > 0.03 and trend_strength > 1.5:
        return "trending_volatile"
    elif volatility > 0.03:
        return "choppy_volatile"
    elif trend_strength > 1.5:
        return "trending_quiet"
    else:
        return "range_bound"


REGIME_STRATEGY_MAP = {
    "trending_volatile": ["momentum-eth-4h", "trend-multi-asset"],
    "choppy_volatile": ["arb-cross-exchange", "vol-btc-perp"],
    "trending_quiet": ["trend-multi-asset", "momentum-eth-4h"],
    "range_bound": ["mrev-btc-1h", "arb-cross-exchange"],
}


def get_promoted_strategies(regime: str) -> list[str]:
    """Return which strategies to actively promote for the current regime."""
    return REGIME_STRATEGY_MAP.get(regime, list(STRATEGY_AGENTS.keys()))
```

In practice, run `detect_market_regime` daily using price data from your exchange feed. When the regime shifts, update your marketplace listings to highlight the strategies best suited to the current environment. You do not need to delist underperforming strategies --- simply adjust their visibility and stop accepting new subscribers on strategies that are fighting the regime. This keeps your escrow completion rate high and prevents reputation damage from strategies running in unfavorable conditions.

**Automated regime-based subscriber gating:**

```bash
# Check current regime and adjust strategy visibility
curl -s -X POST https://sandbox.greenhelix.net/v1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GREENHELIX_API_KEY" \
  -d '{
    "tool": "search_services",
    "input": {
      "query": "strategy-seller mean-reversion momentum"
    }
  }'
```

```python
def apply_regime_gating(
    clients: dict[str, GreenHelixClient],
    regime: str,
    strategy_returns: dict[str, list[float]],
):
    """Pause subscriber intake for strategies mismatched to current regime."""
    promoted = get_promoted_strategies(regime)
    for key, c in clients.items():
        if key in promoted:
            print(f"[{key}] ACTIVE - accepting subscribers (regime: {regime})")
        else:
            # Check if strategy is still performing despite regime mismatch
            recent = strategy_returns.get(key, [])
            if recent and sum(recent[-7:]) > 0:
                print(f"[{key}] ACTIVE - performing despite regime mismatch")
            else:
                print(f"[{key}] PAUSED - not suited for {regime} regime")
```

### Portfolio-Level Metrics and Claim Chains

Submit portfolio-level metrics to GreenHelix alongside individual strategy metrics. This builds a portfolio-level claim chain that institutional subscribers can verify. Institutional buyers who subscribe to your entire portfolio (rather than individual strategies) need aggregate proof that the combined performance meets their criteria.

```python
def submit_portfolio_metrics(
    client: GreenHelixClient, strategy_metrics: dict[str, dict]
):
    """Submit aggregate portfolio metrics to GreenHelix."""
    portfolio = compute_portfolio_metrics(strategy_metrics)
    portfolio["period_start"] = strategy_metrics[
        list(strategy_metrics.keys())[0]
    ].get("period_start", "")
    portfolio["period_end"] = strategy_metrics[
        list(strategy_metrics.keys())[0]
    ].get("period_end", "")

    result = client.submit_metrics(portfolio)
    print(f"Portfolio metrics submitted: {result}")

    # Build claim chain for portfolio-level verification
    chain = client.build_claim_chain()
    print(f"Portfolio claim chain root: {chain.get('root_hash')}")
```

---

## Chapter 10: Dispute Resolution Workflows

### The Dispute Lifecycle

Chapter 6 covered the basics of disputes. This chapter goes deeper into the mechanics of each stage and how to handle them programmatically. Every dispute follows a defined lifecycle with four stages:

1. **Opened**: The subscriber files a dispute with a reason and the escrow ID. The escrow is frozen --- no funds can be released or returned until the dispute is resolved.
2. **Evidence**: Both parties submit evidence. For the seller, this is the claim chain. For the buyer, this is their own analysis of the submitted metrics against the escrow criteria.
3. **Mediation**: The platform evaluates the evidence. In most cases, this is automated --- the claim chain is verified, the metrics are compared against the criteria, and a resolution is computed.
4. **Resolution**: Funds are released, returned, or split. The outcome is recorded on both parties' reputation profiles.

```python
def handle_dispute_lifecycle(
    client: GreenHelixClient, escrow_id: str
) -> dict:
    """Monitor and respond to a dispute through its lifecycle."""
    # Step 1: Detect that a dispute has been opened
    # In production, you would receive this via webhook
    print(f"Dispute detected on escrow: {escrow_id}")

    # Step 2: Build your evidence (claim chain)
    claim_chain = client.build_claim_chain()
    print(f"Evidence prepared. Chain root: {claim_chain.get('root_hash')}")
    print(f"Attestations: {claim_chain.get('attestation_count')}")

    # Step 3: Retrieve verified claims for the evaluation period
    claims = client._execute("get_verified_claims", {
        "agent_id": client.agent_id,
    })

    # Step 4: Compute whether criteria were actually met
    attestations = claims.get("claims", [])
    if not attestations:
        return {"status": "no_evidence", "recommendation": "accept_refund"}

    sharpe_values = [a["metrics"]["sharpe_ratio"] for a in attestations if "sharpe_ratio" in a.get("metrics", {})]
    dd_values = [a["metrics"]["max_drawdown_pct"] for a in attestations if "max_drawdown_pct" in a.get("metrics", {})]

    avg_sharpe = sum(sharpe_values) / len(sharpe_values) if sharpe_values else 0
    max_dd = max(dd_values) if dd_values else 100

    return {
        "avg_sharpe": round(avg_sharpe, 2),
        "max_drawdown_pct": round(max_dd, 2),
        "attestation_count": len(attestations),
        "chain_root": claim_chain.get("root_hash"),
    }
```

### Building Evidence Packages

When a dispute goes to mediation, the strength of your evidence determines the outcome. A strong evidence package has three components: a complete claim chain with no gaps, signed metric submissions that cover the entire evaluation period, and a clear mapping from submitted metrics to the escrow criteria.

```python
def build_evidence_package(
    client: GreenHelixClient,
    escrow_criteria: dict,
    evaluation_start: str,
    evaluation_end: str,
) -> dict:
    """Build a complete evidence package for dispute defense."""
    # Get all verified claims in the evaluation window
    claims = client._execute("get_verified_claims", {
        "agent_id": client.agent_id,
    })
    attestations = claims.get("claims", [])

    # Filter to evaluation period
    period_attestations = [
        a for a in attestations
        if evaluation_start <= a.get("timestamp", "") <= evaluation_end
    ]

    # Build the claim chain for tamper-evident proof
    chain = client.build_claim_chain()

    # Compute aggregate performance over the evaluation period
    total_trades = sum(a["metrics"].get("trades_executed", 0) for a in period_attestations)
    winning_trades = sum(a["metrics"].get("winning_trades", 0) for a in period_attestations)
    sharpe_values = [a["metrics"]["sharpe_ratio"] for a in period_attestations if "sharpe_ratio" in a.get("metrics", {})]
    dd_values = [a["metrics"]["max_drawdown_pct"] for a in period_attestations if "max_drawdown_pct" in a.get("metrics", {})]

    avg_sharpe = sum(sharpe_values) / len(sharpe_values) if sharpe_values else 0.0
    max_dd = max(dd_values) if dd_values else 0.0
    win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0.0

    # Compare against criteria
    criteria_results = {
        "min_sharpe_ratio": {
            "required": escrow_criteria.get("min_sharpe_ratio", 0),
            "actual": round(avg_sharpe, 2),
            "met": avg_sharpe >= escrow_criteria.get("min_sharpe_ratio", 0),
        },
        "max_drawdown_pct": {
            "required": escrow_criteria.get("max_drawdown_pct", 100),
            "actual": round(max_dd, 2),
            "met": max_dd <= escrow_criteria.get("max_drawdown_pct", 100),
        },
        "min_win_rate_pct": {
            "required": escrow_criteria.get("min_win_rate_pct", 0),
            "actual": round(win_rate, 1),
            "met": win_rate >= escrow_criteria.get("min_win_rate_pct", 0),
        },
        "min_total_trades": {
            "required": escrow_criteria.get("min_total_trades", 0),
            "actual": total_trades,
            "met": total_trades >= escrow_criteria.get("min_total_trades", 0),
        },
    }

    all_met = all(c["met"] for c in criteria_results.values())
    met_count = sum(1 for c in criteria_results.values() if c["met"])

    return {
        "chain_root": chain.get("root_hash"),
        "attestation_count": len(period_attestations),
        "evaluation_period": {"start": evaluation_start, "end": evaluation_end},
        "criteria_results": criteria_results,
        "all_criteria_met": all_met,
        "criteria_met_count": f"{met_count}/{len(criteria_results)}",
    }
```

### Automated Dispute Detection

The best disputes are the ones that never happen. Automated dispute detection monitors your strategy's performance throughout the evaluation period and alerts you when criteria are at risk, giving you time to communicate with subscribers proactively.

```python
def check_criteria_risk(
    current_metrics: dict,
    escrow_criteria: dict,
    days_remaining: int,
    total_days: int,
) -> list[dict]:
    """Check if any escrow criteria are at risk of not being met."""
    alerts = []
    progress = (total_days - days_remaining) / total_days

    # Sharpe ratio check
    current_sharpe = current_metrics.get("sharpe_ratio", 0)
    target_sharpe = escrow_criteria.get("min_sharpe_ratio", 0)
    if current_sharpe < target_sharpe * 0.9:
        alerts.append({
            "metric": "sharpe_ratio",
            "current": current_sharpe,
            "target": target_sharpe,
            "severity": "critical" if current_sharpe < target_sharpe * 0.7 else "warning",
            "days_remaining": days_remaining,
            "message": f"Sharpe at {current_sharpe}, need {target_sharpe}. "
                       f"{days_remaining} days left to recover.",
        })

    # Drawdown check
    current_dd = current_metrics.get("max_drawdown_pct", 0)
    max_dd = escrow_criteria.get("max_drawdown_pct", 100)
    if current_dd > max_dd * 0.8:
        alerts.append({
            "metric": "max_drawdown_pct",
            "current": current_dd,
            "target": max_dd,
            "severity": "critical" if current_dd > max_dd * 0.95 else "warning",
            "days_remaining": days_remaining,
            "message": f"Drawdown at {current_dd}%, limit is {max_dd}%. "
                       f"Close to breach.",
        })

    # Trade count check (are we on pace?)
    current_trades = current_metrics.get("trades_executed", 0)
    target_trades = escrow_criteria.get("min_total_trades", 0)
    expected_trades = target_trades * progress
    if current_trades < expected_trades * 0.8 and days_remaining < total_days * 0.5:
        alerts.append({
            "metric": "min_total_trades",
            "current": current_trades,
            "target": target_trades,
            "severity": "warning",
            "days_remaining": days_remaining,
            "message": f"Only {current_trades} trades executed, need {target_trades}. "
                       f"Behind pace with {days_remaining} days left.",
        })

    return alerts
```

### Partial Refund Calculations

When a dispute results in a partial release, the refund amount is calculated based on how many criteria were met and how close the performance was to the target. This is not a binary outcome --- it is a proportional calculation that rewards strategies that came close to their targets.

```python
def calculate_partial_refund(
    escrow_amount: float, criteria_results: dict
) -> dict:
    """Calculate a fair partial refund based on criteria performance."""
    total_criteria = len(criteria_results)
    met_criteria = sum(1 for c in criteria_results.values() if c["met"])

    # Base refund: proportion of criteria not met
    base_refund_pct = ((total_criteria - met_criteria) / total_criteria) * 100

    # Adjust for "how close" unmet criteria were to target
    closeness_adjustments = []
    for name, result in criteria_results.items():
        if not result["met"]:
            required = result["required"]
            actual = result["actual"]
            if required > 0:
                # How close were we? 0.0 = totally missed, 1.0 = almost met
                if name == "max_drawdown_pct":
                    # For drawdown, lower is better, and we exceeded the max
                    closeness = max(0, 1 - (actual - required) / required)
                else:
                    closeness = actual / required if required > 0 else 0
                closeness_adjustments.append(min(closeness, 1.0))

    # Average closeness reduces the refund
    if closeness_adjustments:
        avg_closeness = sum(closeness_adjustments) / len(closeness_adjustments)
        adjusted_refund_pct = base_refund_pct * (1 - avg_closeness * 0.5)
    else:
        adjusted_refund_pct = base_refund_pct

    refund_amount = round(escrow_amount * adjusted_refund_pct / 100, 2)
    seller_amount = round(escrow_amount - refund_amount, 2)

    return {
        "escrow_amount": escrow_amount,
        "refund_to_buyer": refund_amount,
        "release_to_seller": seller_amount,
        "refund_percentage": round(adjusted_refund_pct, 1),
        "criteria_met": f"{met_criteria}/{total_criteria}",
    }
```

### Dispute Prevention Strategies

Prevention is always cheaper than resolution. Here are concrete strategies that reduce dispute rates, implemented as code patterns you can integrate into your operations.

**Daily performance notification to subscribers:**

```python
def notify_subscribers_daily(
    client: GreenHelixClient,
    subscriber_ids: list[str],
    current_metrics: dict,
    escrow_criteria: dict,
):
    """Send daily performance summaries to subscribers via messaging."""
    for subscriber_id in subscriber_ids:
        sharpe = current_metrics.get("sharpe_ratio", 0)
        target = escrow_criteria.get("min_sharpe_ratio", 0)
        status = "on_track" if sharpe >= target else "below_target"

        client._execute("send_message", {
            "from_agent_id": client.agent_id,
            "to_agent_id": subscriber_id,
            "message": {
                "type": "performance_update",
                "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
                "sharpe_ratio": sharpe,
                "target_sharpe": target,
                "status": status,
                "max_drawdown_pct": current_metrics.get("max_drawdown_pct", 0),
            },
        })
```

**Pre-emptive escrow extension during volatile markets:**

When market volatility spikes and your strategy temporarily underperforms, reaching out to the subscriber before the evaluation period ends and offering an extension is far better than waiting for a dispute. Most subscribers will agree to an extension if you are transparent about the situation, because they know the strategy works in normal conditions and they can verify the track record in your claim chain.

```bash
# Check if a subscriber's escrow is at risk
curl -s -X POST https://sandbox.greenhelix.net/v1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GREENHELIX_API_KEY" \
  -d '{
    "tool": "get_verified_claims",
    "input": {
      "agent_id": "strategy-seller-mrev-01"
    }
  }'
```

Review the output and if the rolling performance metrics are trending below criteria, contact the subscriber proactively. A simple message explaining the situation, backed by your transparent claim chain, goes a long way toward avoiding a formal dispute.

---

## Next Steps

For deployment patterns, monitoring, and production hardening, see the
[Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening).

---

## What's Next

This guide covered the complete lifecycle of selling trading strategies through the GreenHelix A2A Commerce Gateway: identity registration, marketplace listing, performance escrow, verifiable metrics, dispute handling, scaling, advanced escrow patterns, multi-strategy portfolio management, dispute resolution workflows, and production deployment.

For deeper coverage of specific topics, see the companion guides:

- **Bot Reputation: Building and Leveraging Agent Trust Scores** --- covers the trust score algorithm in detail, advanced claim chain strategies, and how to use your reputation as a competitive moat across the GreenHelix ecosystem.
- **EU AI Act Compliance for Autonomous Trading Agents** --- covers the regulatory requirements for operating autonomous trading bots in European markets, including the transparency and audit trail requirements that GreenHelix's attestation system helps you meet.

For the full API reference and additional tool documentation, visit the GreenHelix developer documentation at [https://api.greenhelix.net/docs](https://api.greenhelix.net/docs).

---

*Published by GreenHelix Labs. All code examples are provided under the MIT License and are intended for use with the GreenHelix A2A Commerce Gateway.*

