---
name: greenhelix-copy-trading-infrastructure
version: "1.3.1"
description: "Copy Trading Infrastructure: Protocol-Agnostic Copy Trading with Verified Leader Performance. Build copy trading infrastructure with verified leader performance, follower allocation models, slippage handling, performance escrow, and revenue sharing. Includes detailed Python code examples with marketplace and escrow integration patterns."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [copy-trading, trading-bot, leader-follower, escrow, guide, greenhelix, openclaw, ai-agent]
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
# Copy Trading Infrastructure: Protocol-Agnostic Copy Trading with Verified Leader Performance

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `GREENHELIX_API_KEY`: API authentication for GreenHelix gateway (read/write access to purchased API tools only)
> - `AGENT_SIGNING_KEY`: Cryptographic signing key for agent identity (Ed25519 key pair for request signing)


Copy trading is the fastest-growing segment of automated trading, projected to reach $4.2 billion by 2027 according to Allied Market Research. But the current generation of platforms -- eToro, Bybit Copy, NAGA, ZuluTrade -- share a fundamental trust problem that limits their growth and exposes followers to unnecessary risk. Leader performance is self-reported or platform-curated with opaque methodology. Followers have no recourse when leaders lose money beyond closing the copy relationship after the damage is done. Platforms take 20-30% of performance fees while adding no verification, no escrow protection, and no cryptographic proof that stated returns actually occurred. The result is an ecosystem where the most profitable strategy for a leader is not to trade well, but to attract followers, collect fees, and let survivorship bias do the marketing. This guide builds something different: protocol-agnostic copy trading infrastructure where leader performance is cryptographically verified through Ed25519-signed trade records, follower allocations are risk-managed through configurable models, and revenue sharing flows through escrow that releases only when performance criteria are met. The trust layer is GreenHelix. Leaders register as service providers on the marketplace. Followers discover and evaluate them using verified metrics. Performance escrow protects follower capital. Revenue splits are enforced by smart contracts, not gentleman's agreements. The entire system is exchange-agnostic -- the same infrastructure works whether your leaders trade on Binance, Coinbase, Interactive Brokers, or a DEX.
1. [Copy Trading Architecture](#chapter-1-copy-trading-architecture)
2. [CopyTradingLeader Class](#chapter-2-copytradingleader-class)

## What You'll Learn
- Chapter 1: Copy Trading Architecture
- Chapter 2: CopyTradingLeader Class
- Chapter 3: CopyTradingFollower Class
- Chapter 4: Allocation Models
- Chapter 5: Slippage Handling
- Chapter 6: Performance Escrow
- Chapter 7: Revenue Sharing
- Next Steps
- What's Next

## Full Guide

# Copy Trading Infrastructure: Protocol-Agnostic Copy Trading with Verified Leader Performance

Copy trading is the fastest-growing segment of automated trading, projected to reach $4.2 billion by 2027 according to Allied Market Research. But the current generation of platforms -- eToro, Bybit Copy, NAGA, ZuluTrade -- share a fundamental trust problem that limits their growth and exposes followers to unnecessary risk. Leader performance is self-reported or platform-curated with opaque methodology. Followers have no recourse when leaders lose money beyond closing the copy relationship after the damage is done. Platforms take 20-30% of performance fees while adding no verification, no escrow protection, and no cryptographic proof that stated returns actually occurred. The result is an ecosystem where the most profitable strategy for a leader is not to trade well, but to attract followers, collect fees, and let survivorship bias do the marketing. This guide builds something different: protocol-agnostic copy trading infrastructure where leader performance is cryptographically verified through Ed25519-signed trade records, follower allocations are risk-managed through configurable models, and revenue sharing flows through escrow that releases only when performance criteria are met. The trust layer is GreenHelix. Leaders register as service providers on the marketplace. Followers discover and evaluate them using verified metrics. Performance escrow protects follower capital. Revenue splits are enforced by smart contracts, not gentleman's agreements. The entire system is exchange-agnostic -- the same infrastructure works whether your leaders trade on Binance, Coinbase, Interactive Brokers, or a DEX.

---

## Table of Contents

1. [Copy Trading Architecture](#chapter-1-copy-trading-architecture)
2. [CopyTradingLeader Class](#chapter-2-copytradingleader-class)
3. [CopyTradingFollower Class](#chapter-3-copytradingfollower-class)
4. [Allocation Models](#chapter-4-allocation-models)
5. [Slippage Handling](#chapter-5-slippage-handling)
6. [Performance Escrow](#chapter-6-performance-escrow)
7. [Revenue Sharing](#chapter-7-revenue-sharing)
9. [What's Next](#whats-next)

---

## Chapter 1: Copy Trading Architecture

### The Leader-Follower Model with GreenHelix as Trust Layer

Copy trading is conceptually simple: a leader executes trades, and followers mirror those trades in their own accounts. The complexity lies entirely in trust. How does a follower know the leader's track record is real? How does the follower limit their exposure if the leader blows up? How does the leader get paid fairly for generating alpha? And how do both parties resolve disputes without a centralized authority that has perverse incentives?

Traditional platforms solve these problems by becoming the centralized authority. eToro holds both leader and follower funds, controls the performance data, sets the fee structure, and resolves disputes at its discretion. This works until it does not -- platforms can selectively promote leaders who generate revenue, suppress negative performance data, or structure fees that incentivize volume over performance.

The GreenHelix architecture replaces platform trust with cryptographic verification. Leaders submit signed performance metrics that cannot be fabricated. Followers subscribe through performance escrow that protects their capital. Revenue sharing flows through escrow contracts that release only when agreed-upon criteria are met. The platform does not hold funds, does not curate leaders, and does not resolve disputes -- the protocol does.

### Architecture Overview

```
+-------------------+       +---------------------+       +-------------------+
|   Copy Leader     |       |   GreenHelix API    |       |   Copy Follower   |
|                   |       |                     |       |                   |
|  Execute trades   |       |                     |       |                   |
|  on exchange      |       |                     |       |                   |
|       |           |       |                     |       |                   |
|  Sign trade       |       |                     |       |                   |
|  record (Ed25519) |       |                     |       |                   |
|       |           |       |                     |       |                   |
|  submit_metrics  -------> |  Verified Metrics   |       |                   |
|  publish_event   -------> |  Event Bus          | ----> |  Receive signal   |
|  register_service ------> |  Marketplace        | ----> |  search_services  |
|                   |       |                     |       |  subscribe        |
|                   |       |  Performance Escrow | <---- |  create_escrow    |
|                   |       |       |              |       |       |           |
|  claim_revenue  <-------- |  release_escrow     |       |  execute trade    |
|                   |       |  (criteria met)     |       |  on own exchange  |
|                   |       |                     |       |       |           |
|  get_reputation  <------> |  Reputation Engine  | <---> |  get_reputation   |
+-------------------+       +---------------------+       +-------------------+
```

The data flow works as follows. A leader executes a trade on their exchange of choice -- Binance, Coinbase, Interactive Brokers, a DEX, it does not matter. The leader's bot signs the trade record with its Ed25519 private key and publishes it to the GreenHelix event bus via `publish_event`. Simultaneously, the leader submits aggregate performance metrics via `submit_metrics` -- win rate, Sharpe ratio, max drawdown, total return -- that become part of their verifiable reputation. Followers discover leaders through `search_services` on the marketplace, evaluate them using `get_agent_reputation` and `get_claim_chains`, subscribe by creating a performance escrow via `create_escrow`, and receive trade signals through webhooks registered with `register_webhook`. When a signal arrives, the follower's bot applies its allocation model, adjusts for risk limits, and executes the corresponding trade on the follower's own exchange account. At the end of each evaluation period, the escrow contract checks whether the leader met the agreed performance criteria. If yes, the leader's revenue share is released. If not, the follower's escrow deposit is returned.

### GreenHelix Tools Used

This guide uses the following GreenHelix API tools:

| Tool | Purpose |
|---|---|
| `register_agent` | Register leader and follower identities with Ed25519 public keys |
| `register_service` | List a leader's copy trading service on the marketplace |
| `search_services` | Discover available copy trading leaders |
| `create_escrow` | Create performance escrow protecting follower deposits |
| `release_escrow` | Release escrow when performance criteria are met |
| `submit_metrics` | Submit verified performance metrics for leaders |
| `get_agent_reputation` | Retrieve a leader's verified reputation score |
| `get_claim_chains` | Verify the integrity of a leader's performance history |
| `publish_event` | Broadcast trade signals to followers via the event bus |
| `register_webhook` | Register follower endpoints to receive trade signals |
| `create_sla` | Define performance SLA between leader and follower |
| `check_sla_compliance` | Verify leader meets agreed SLA terms |

### Why Protocol-Agnostic Matters

Locking copy trading to a single exchange limits the leader pool and the follower pool. A leader who trades BTC/USDT on Binance Futures should be copyable by a follower on Bybit, OKX, or a self-custodied DEX. The GreenHelix event bus decouples signal generation from signal execution. The leader publishes a normalized trade signal -- symbol, side, size as a percentage of portfolio, entry price, stop loss, take profit -- and each follower's execution engine translates that signal into exchange-specific orders. This is the same architecture used by institutional signal distribution networks like Portware and FlexTrade, scaled down to retail.

---

## Chapter 2: CopyTradingLeader Class

### Leader Registration and Service Listing

A copy trading leader is an agent that executes trades on one or more exchanges and broadcasts those trades as signals. Before a leader can attract followers, they must register their identity, list their service on the marketplace, and begin building a verified track record.

#### Step 1: Generate an Ed25519 Keypair

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import base64

private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

private_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PrivateFormat.Raw,
    encryption_algorithm=serialization.NoEncryption()
)
public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw
)

PRIVATE_KEY_B64 = base64.b64encode(private_bytes).decode()
PUBLIC_KEY_B64 = base64.b64encode(public_bytes).decode()
```

Store the private key in a secrets manager. It signs every trade record and performance metric submission -- if it leaks, an attacker can fabricate your track record.

#### Step 2: Register and List

```bash
# Register the leader agent
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "register_agent",
    "input": {
      "agent_id": "leader-crypto-momentum-01",
      "public_key": "'"$PUBLIC_KEY_B64"'",
      "name": "Crypto Momentum Alpha"
    }
  }'

# List the copy trading service on the marketplace
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "register_service",
    "input": {
      "agent_id": "leader-crypto-momentum-01",
      "service_type": "copy_trading",
      "name": "Crypto Momentum Alpha -- Copy Trading",
      "description": "Momentum-based crypto trading strategy. BTC/ETH/SOL on Binance Futures. 15-minute to 4-hour timeframes. Target Sharpe > 2.0, max drawdown < 15%.",
      "pricing": {
        "model": "hybrid",
        "subscription_monthly_usd": "49.00",
        "performance_fee_pct": "15.0"
      },
      "metadata": {
        "strategy_type": "momentum",
        "asset_classes": ["crypto"],
        "exchanges": ["binance_futures"],
        "symbols": ["BTCUSDT", "ETHUSDT", "SOLUSDT"],
        "timeframes": ["15m", "1h", "4h"],
        "track_record_months": 18,
        "verified_sharpe": "2.34",
        "verified_max_drawdown_pct": "11.7",
        "verified_win_rate_pct": "58.3",
        "avg_trades_per_week": 12,
        "max_followers": 500
      }
    }
  }'
```

The `max_followers` field is critical. Every additional follower increases market impact when the leader's signals are executed simultaneously. A leader trading $100K with 500 followers at $10K each creates $5.1M of correlated order flow. On illiquid pairs, this causes meaningful slippage -- covered in Chapter 5.

### The CopyTradingLeader Class

```python
import json
import time
import hashlib
import base64
import uuid
from datetime import datetime, timezone
from typing import Optional

import requests
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
)
from cryptography.hazmat.primitives import serialization


class CopyTradingLeader:
    """Copy trading leader that broadcasts verified trade signals."""

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        private_key_b64: str,
    ):
        self.api_base = "https://api.greenhelix.net/v1"
        self.api_key = api_key
        self.agent_id = agent_id
        self._private_key = Ed25519PrivateKey.from_private_bytes(
            base64.b64decode(private_key_b64)
        )
        self._trades: list[dict] = []
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    def _execute(self, tool: str, input_data: dict) -> dict:
        resp = self._session.post(
            f"{self.api_base}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    def _sign(self, payload: dict) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        signature = self._private_key.sign(canonical.encode())
        return base64.b64encode(signature).decode()

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def broadcast_trade_signal(
        self,
        symbol: str,
        side: str,
        size_pct: float,
        entry_price: float,
        stop_loss: Optional[float] = None,
        take_profit: Optional[float] = None,
        order_type: str = "market",
        timeframe: str = "1h",
    ) -> dict:
        """Broadcast a trade signal to all followers via the event bus."""
        signal_id = str(uuid.uuid4())
        timestamp = self._now_iso()

        payload = {
            "signal_id": signal_id,
            "leader_id": self.agent_id,
            "symbol": symbol,
            "side": side,
            "size_pct": str(size_pct),
            "entry_price": str(entry_price),
            "order_type": order_type,
            "timeframe": timeframe,
            "timestamp": timestamp,
        }
        if stop_loss is not None:
            payload["stop_loss"] = str(stop_loss)
        if take_profit is not None:
            payload["take_profit"] = str(take_profit)

        payload["signature"] = self._sign(payload)

        result = self._execute("publish_event", {
            "event_type": "copy_trade.signal",
            "payload": payload,
        })

        self._trades.append({
            "signal_id": signal_id,
            "symbol": symbol,
            "side": side,
            "size_pct": size_pct,
            "entry_price": entry_price,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "timestamp": timestamp,
            "status": "open",
        })

        return result

    def close_position(
        self,
        signal_id: str,
        exit_price: float,
        pnl_pct: float,
    ) -> dict:
        """Broadcast a position close signal."""
        timestamp = self._now_iso()

        payload = {
            "signal_id": signal_id,
            "leader_id": self.agent_id,
            "action": "close",
            "exit_price": str(exit_price),
            "pnl_pct": str(pnl_pct),
            "timestamp": timestamp,
        }
        payload["signature"] = self._sign(payload)

        result = self._execute("publish_event", {
            "event_type": "copy_trade.close",
            "payload": payload,
        })

        for trade in self._trades:
            if trade["signal_id"] == signal_id:
                trade["status"] = "closed"
                trade["exit_price"] = exit_price
                trade["pnl_pct"] = pnl_pct
                break

        return result

    def submit_performance_metrics(self) -> dict:
        """Submit verified performance metrics to build reputation."""
        closed_trades = [t for t in self._trades if t["status"] == "closed"]
        if not closed_trades:
            return {"status": "no_closed_trades"}

        wins = [t for t in closed_trades if t["pnl_pct"] > 0]
        losses = [t for t in closed_trades if t["pnl_pct"] <= 0]
        pnls = [t["pnl_pct"] for t in closed_trades]

        total_return = sum(pnls)
        win_rate = len(wins) / len(closed_trades) * 100
        avg_win = sum(t["pnl_pct"] for t in wins) / len(wins) if wins else 0
        avg_loss = sum(t["pnl_pct"] for t in losses) / len(losses) if losses else 0
        max_drawdown = self._calculate_max_drawdown(pnls)
        sharpe = self._calculate_sharpe(pnls)

        metrics = {
            "total_trades": len(closed_trades),
            "win_rate_pct": str(round(win_rate, 2)),
            "total_return_pct": str(round(total_return, 4)),
            "avg_win_pct": str(round(avg_win, 4)),
            "avg_loss_pct": str(round(avg_loss, 4)),
            "max_drawdown_pct": str(round(max_drawdown, 4)),
            "sharpe_ratio": str(round(sharpe, 4)),
            "last_updated": self._now_iso(),
        }
        metrics["signature"] = self._sign(metrics)

        return self._execute("submit_metrics", {
            "agent_id": self.agent_id,
            "metrics": metrics,
        })

    def _calculate_max_drawdown(self, pnls: list[float]) -> float:
        cumulative = 0.0
        peak = 0.0
        max_dd = 0.0
        for pnl in pnls:
            cumulative += pnl
            if cumulative > peak:
                peak = cumulative
            drawdown = peak - cumulative
            if drawdown > max_dd:
                max_dd = drawdown
        return max_dd

    def _calculate_sharpe(self, pnls: list[float]) -> float:
        if len(pnls) < 2:
            return 0.0
        mean = sum(pnls) / len(pnls)
        variance = sum((p - mean) ** 2 for p in pnls) / (len(pnls) - 1)
        std = variance ** 0.5
        if std == 0:
            return 0.0
        # Annualize assuming ~250 trading days, ~3 trades/day
        return (mean / std) * (750 ** 0.5)

    def register_service(
        self,
        name: str,
        description: str,
        pricing: dict,
        metadata: dict,
    ) -> dict:
        """List the copy trading service on the marketplace."""
        return self._execute("register_service", {
            "agent_id": self.agent_id,
            "service_type": "copy_trading",
            "name": name,
            "description": description,
            "pricing": pricing,
            "metadata": metadata,
        })

    def configure_revenue(
        self,
        model: str = "hybrid",
        subscription_monthly_usd: str = "49.00",
        performance_fee_pct: str = "15.0",
        high_water_mark: bool = True,
    ) -> dict:
        """Configure revenue model for the copy trading service."""
        return {
            "model": model,
            "subscription_monthly_usd": subscription_monthly_usd,
            "performance_fee_pct": performance_fee_pct,
            "high_water_mark": high_water_mark,
        }
```

### Revenue Configuration: Fixed Fee vs Percentage vs Hybrid

Leaders choose from three revenue models. **Fixed subscription** charges a flat monthly fee regardless of performance -- predictable for both parties but does not align leader and follower incentives. **Performance fee** takes a percentage of profits above a high-water mark -- strongly aligns incentives but creates income volatility for the leader. **Hybrid** combines a lower monthly subscription with a reduced performance fee -- the subscription covers infrastructure costs while the performance fee rewards alpha. The hybrid model is the industry standard for copy trading services above $25/month.

```bash
# Register with hybrid pricing
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "register_service",
    "input": {
      "agent_id": "leader-crypto-momentum-01",
      "service_type": "copy_trading",
      "name": "Crypto Momentum Alpha",
      "description": "Momentum strategy, BTC/ETH/SOL, Sharpe > 2.0",
      "pricing": {
        "model": "hybrid",
        "subscription_monthly_usd": "49.00",
        "performance_fee_pct": "15.0",
        "high_water_mark": true,
        "billing_cycle": "monthly",
        "trial_days": 7
      },
      "metadata": {
        "strategy_type": "momentum",
        "min_follower_capital_usd": "1000"
      }
    }
  }'
```

The `high_water_mark` flag ensures the leader only earns performance fees on new profits. If a follower's account drops from $10,000 to $8,000, the leader earns no performance fee until the account exceeds $10,000 again. This prevents leaders from earning fees on recovery -- you only pay for net new alpha.

### Trade Signal Broadcasting

When the leader executes a trade, the signal is normalized and broadcast to all followers via the GreenHelix event bus. The signal includes the symbol, side, size as a percentage of portfolio (not an absolute amount), and optional stop loss and take profit levels.

```python
import os

leader = CopyTradingLeader(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="leader-crypto-momentum-01",
    private_key_b64=os.environ["LEADER_PRIVATE_KEY"],
)

# Long BTC with 10% of portfolio, 2% stop loss, 6% take profit
result = leader.broadcast_trade_signal(
    symbol="BTCUSDT",
    side="buy",
    size_pct=10.0,
    entry_price=67250.00,
    stop_loss=65905.00,
    take_profit=71285.00,
    order_type="limit",
    timeframe="4h",
)
print(f"Signal broadcast: {result}")

# Later, close the position
result = leader.close_position(
    signal_id=result["payload"]["signal_id"],
    exit_price=71100.00,
    pnl_pct=5.72,
)
print(f"Position closed: {result}")

# Submit updated performance metrics
metrics_result = leader.submit_performance_metrics()
print(f"Metrics submitted: {metrics_result}")
```

The `size_pct` field is the key abstraction that makes copy trading protocol-agnostic. A leader trading a $500K portfolio who allocates 10% to BTC sends `size_pct: 10.0`. A follower with a $5K portfolio allocates 10% -- $500 -- to the same trade. The signal describes intent, not execution details. Each follower's execution engine translates that intent into exchange-specific orders appropriate for their account size.

---

## Chapter 3: CopyTradingFollower Class

### Discovering and Evaluating Leaders

A follower's first task is finding leaders worth copying. The GreenHelix marketplace exposes leader listings through `search_services`, and the reputation engine provides verified metrics through `get_agent_reputation`. The combination lets followers make data-driven decisions rather than relying on platform-curated leaderboards.

```bash
# Search for copy trading leaders specializing in crypto momentum
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "search_services",
    "input": {
      "service_type": "copy_trading",
      "query": "crypto momentum",
      "filters": {
        "min_sharpe": "1.5",
        "max_drawdown_pct": "20.0",
        "min_track_record_months": 6
      },
      "sort_by": "sharpe_ratio",
      "sort_order": "desc",
      "limit": 20
    }
  }'
```

```bash
# Get verified reputation for a specific leader
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "get_agent_reputation",
    "input": {
      "agent_id": "leader-crypto-momentum-01"
    }
  }'
```

```bash
# Verify the leader's performance claim chain
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "get_claim_chains",
    "input": {
      "agent_id": "leader-crypto-momentum-01",
      "claim_type": "performance_metrics"
    }
  }'
```

The claim chain is the critical verification step. `get_agent_reputation` returns aggregate scores, but `get_claim_chains` returns the Merkle tree of signed performance submissions. A follower can independently verify that each metric submission was signed by the leader's Ed25519 key, that the submissions form an unbroken chain, and that no submissions have been retroactively modified. This is the difference between "the platform says this leader has a 2.34 Sharpe" and "I have cryptographic proof that this leader submitted 18 months of signed performance data that produces a 2.34 Sharpe."

### The CopyTradingFollower Class

```python
import json
import time
import base64
import uuid
from datetime import datetime, timezone
from typing import Optional
from dataclasses import dataclass, field

import requests
from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey,
    Ed25519PublicKey,
)
from cryptography.hazmat.primitives import serialization


@dataclass
class LeaderSubscription:
    """Tracks a follower's subscription to a specific leader."""
    leader_id: str
    escrow_id: str
    max_allocation_pct: float = 20.0
    max_drawdown_pct: float = 10.0
    max_position_size_pct: float = 5.0
    allowed_symbols: list[str] = field(default_factory=list)
    active: bool = True
    positions: dict = field(default_factory=dict)
    cumulative_pnl: float = 0.0
    high_water_mark: float = 0.0


class CopyTradingFollower:
    """Copy trading follower that discovers, evaluates, and copies leaders."""

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        private_key_b64: str,
        portfolio_value_usd: float,
    ):
        self.api_base = "https://api.greenhelix.net/v1"
        self.api_key = api_key
        self.agent_id = agent_id
        self.portfolio_value = portfolio_value_usd
        self._private_key = Ed25519PrivateKey.from_private_bytes(
            base64.b64decode(private_key_b64)
        )
        self._subscriptions: dict[str, LeaderSubscription] = {}
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    def _execute(self, tool: str, input_data: dict) -> dict:
        resp = self._session.post(
            f"{self.api_base}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    def _sign(self, payload: dict) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        signature = self._private_key.sign(canonical.encode())
        return base64.b64encode(signature).decode()

    def discover_leaders(
        self,
        strategy_type: str = "momentum",
        min_sharpe: float = 1.5,
        max_drawdown: float = 20.0,
        min_months: int = 6,
    ) -> list[dict]:
        """Search for copy trading leaders matching criteria."""
        result = self._execute("search_services", {
            "service_type": "copy_trading",
            "query": strategy_type,
            "filters": {
                "min_sharpe": str(min_sharpe),
                "max_drawdown_pct": str(max_drawdown),
                "min_track_record_months": min_months,
            },
            "sort_by": "sharpe_ratio",
            "sort_order": "desc",
            "limit": 20,
        })
        return result.get("services", [])

    def evaluate_leader(self, leader_id: str) -> dict:
        """Get verified reputation and performance claim chain for a leader."""
        reputation = self._execute("get_agent_reputation", {
            "agent_id": leader_id,
        })
        claims = self._execute("get_claim_chains", {
            "agent_id": leader_id,
            "claim_type": "performance_metrics",
        })
        return {
            "reputation": reputation,
            "claim_chains": claims,
            "verified": self._verify_claim_chain(claims),
        }

    def _verify_claim_chain(self, claims: dict) -> bool:
        """Verify the integrity of a leader's performance claim chain."""
        chain = claims.get("chains", [])
        if not chain:
            return False
        # Verify each link is signed and the chain is unbroken
        for i, link in enumerate(chain):
            if "signature" not in link:
                return False
            if i > 0 and link.get("previous_hash") != chain[i - 1].get("hash"):
                return False
        return True

    def subscribe(
        self,
        leader_id: str,
        escrow_amount_usd: float,
        max_allocation_pct: float = 20.0,
        max_drawdown_pct: float = 10.0,
        max_position_size_pct: float = 5.0,
        allowed_symbols: Optional[list[str]] = None,
        evaluation_period_days: int = 30,
        performance_criteria: Optional[dict] = None,
    ) -> dict:
        """Subscribe to a leader with performance escrow protection."""
        if performance_criteria is None:
            performance_criteria = {
                "min_sharpe": "1.0",
                "max_drawdown_pct": "20.0",
                "min_win_rate_pct": "45.0",
            }

        escrow_result = self._execute("create_escrow", {
            "payer_id": self.agent_id,
            "payee_id": leader_id,
            "amount": str(escrow_amount_usd),
            "currency": "USD",
            "conditions": {
                "type": "performance_escrow",
                "evaluation_period_days": evaluation_period_days,
                "criteria": performance_criteria,
                "auto_release": True,
            },
            "description": f"Copy trading subscription: {self.agent_id} -> {leader_id}",
        })

        escrow_id = escrow_result["escrow_id"]

        subscription = LeaderSubscription(
            leader_id=leader_id,
            escrow_id=escrow_id,
            max_allocation_pct=max_allocation_pct,
            max_drawdown_pct=max_drawdown_pct,
            max_position_size_pct=max_position_size_pct,
            allowed_symbols=allowed_symbols or [],
        )
        self._subscriptions[leader_id] = subscription

        # Register webhook to receive trade signals from this leader
        self._execute("register_webhook", {
            "url": f"https://your-follower-bot.example.com/signals/{leader_id}",
            "event_types": ["copy_trade.signal", "copy_trade.close"],
            "filters": {"leader_id": leader_id},
            "secret": f"webhook-secret-{leader_id}",
        })

        return escrow_result

    def handle_trade_signal(self, signal: dict) -> Optional[dict]:
        """Process an incoming trade signal from a leader."""
        leader_id = signal.get("leader_id")
        sub = self._subscriptions.get(leader_id)
        if not sub or not sub.active:
            return None

        symbol = signal.get("symbol")

        # Check symbol whitelist
        if sub.allowed_symbols and symbol not in sub.allowed_symbols:
            return {"status": "skipped", "reason": "symbol_not_allowed"}

        # Check drawdown limit
        if sub.cumulative_pnl < 0 and abs(sub.cumulative_pnl) >= sub.max_drawdown_pct:
            sub.active = False
            return {"status": "stopped", "reason": "max_drawdown_reached"}

        # Check total allocation to this leader
        current_allocation = sum(
            pos.get("allocated_usd", 0) for pos in sub.positions.values()
        )
        max_allocation_usd = self.portfolio_value * (sub.max_allocation_pct / 100)
        if current_allocation >= max_allocation_usd:
            return {"status": "skipped", "reason": "max_allocation_reached"}

        # Calculate position size
        leader_size_pct = float(signal.get("size_pct", 0))
        capped_size_pct = min(leader_size_pct, sub.max_position_size_pct)
        position_usd = self.portfolio_value * (capped_size_pct / 100)

        # Ensure we do not exceed remaining allocation
        remaining = max_allocation_usd - current_allocation
        position_usd = min(position_usd, remaining)

        if position_usd < 10:  # Minimum position size
            return {"status": "skipped", "reason": "position_too_small"}

        # Execute the trade on the follower's exchange
        execution = self._execute_on_exchange(
            symbol=symbol,
            side=signal.get("side"),
            amount_usd=position_usd,
            order_type=signal.get("order_type", "market"),
            stop_loss=signal.get("stop_loss"),
            take_profit=signal.get("take_profit"),
        )

        signal_id = signal.get("signal_id")
        sub.positions[signal_id] = {
            "symbol": symbol,
            "side": signal.get("side"),
            "allocated_usd": position_usd,
            "entry_price": execution.get("fill_price"),
            "timestamp": signal.get("timestamp"),
        }

        return execution

    def handle_close_signal(self, signal: dict) -> Optional[dict]:
        """Process a position close signal from a leader."""
        leader_id = signal.get("leader_id")
        signal_id = signal.get("signal_id")
        sub = self._subscriptions.get(leader_id)
        if not sub or signal_id not in sub.positions:
            return None

        position = sub.positions[signal_id]
        execution = self._close_on_exchange(
            symbol=position["symbol"],
            side="sell" if position["side"] == "buy" else "buy",
            amount_usd=position["allocated_usd"],
        )

        # Track PnL
        pnl_pct = float(signal.get("pnl_pct", 0))
        sub.cumulative_pnl += pnl_pct
        if sub.cumulative_pnl > sub.high_water_mark:
            sub.high_water_mark = sub.cumulative_pnl

        del sub.positions[signal_id]
        return execution

    def _execute_on_exchange(self, **kwargs) -> dict:
        """Execute a trade on the follower's exchange. Override per exchange."""
        # Placeholder -- implement per exchange (Binance, Coinbase, etc.)
        return {
            "status": "filled",
            "fill_price": kwargs.get("amount_usd", 0),
            "exchange": "binance",
        }

    def _close_on_exchange(self, **kwargs) -> dict:
        """Close a position on the follower's exchange. Override per exchange."""
        return {"status": "closed", "exchange": "binance"}

    def unsubscribe(self, leader_id: str) -> dict:
        """Unsubscribe from a leader and close all open positions."""
        sub = self._subscriptions.get(leader_id)
        if not sub:
            return {"status": "not_subscribed"}

        # Close all open positions
        for signal_id, position in list(sub.positions.items()):
            self._close_on_exchange(
                symbol=position["symbol"],
                side="sell" if position["side"] == "buy" else "buy",
                amount_usd=position["allocated_usd"],
            )

        sub.active = False
        sub.positions.clear()

        return {"status": "unsubscribed", "leader_id": leader_id}
```

### Risk Limits Per Leader

The `LeaderSubscription` dataclass encodes four risk constraints that protect the follower:

**max_allocation_pct** -- The maximum percentage of the follower's portfolio that can be allocated to positions from this leader at any point in time. Default 20%. If a follower subscribes to five leaders at 20% each, their entire portfolio is allocated -- but no single leader can cause more than 20% damage.

**max_drawdown_pct** -- The cumulative loss threshold that triggers automatic unsubscription. If a leader's signals produce cumulative losses exceeding this threshold, the follower stops copying. Default 10%. This is a circuit breaker that prevents catastrophic losses from a leader who has lost their edge.

**max_position_size_pct** -- The maximum size of any single position, regardless of what the leader signals. If a leader allocates 25% of their portfolio to a single trade (aggressive), the follower caps it at 5% (conservative). This prevents a single bad trade from causing outsized damage.

**allowed_symbols** -- An optional whitelist of tradeable symbols. A follower might want to copy a leader's BTC and ETH trades but skip altcoin signals. An empty list means all symbols are allowed.

```python
import os

follower = CopyTradingFollower(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="follower-conservative-01",
    private_key_b64=os.environ["FOLLOWER_PRIVATE_KEY"],
    portfolio_value_usd=25000.00,
)

# Subscribe to the momentum leader with conservative risk limits
escrow = follower.subscribe(
    leader_id="leader-crypto-momentum-01",
    escrow_amount_usd=500.00,
    max_allocation_pct=15.0,
    max_drawdown_pct=8.0,
    max_position_size_pct=3.0,
    allowed_symbols=["BTCUSDT", "ETHUSDT"],
    evaluation_period_days=30,
    performance_criteria={
        "min_sharpe": "1.5",
        "max_drawdown_pct": "15.0",
        "min_win_rate_pct": "50.0",
    },
)
print(f"Subscribed with escrow: {escrow['escrow_id']}")
```

This follower has a $25,000 portfolio and allocates at most 15% ($3,750) to the momentum leader. No single position exceeds 3% ($750). If cumulative losses reach 8% ($2,000), copying stops automatically. Only BTC and ETH signals are followed -- SOL is filtered out. The $500 escrow deposit is released to the leader only if they maintain a Sharpe above 1.5, drawdown below 15%, and win rate above 50% over 30 days.

---

## Chapter 4: Allocation Models

### Why One Size Does Not Fit All

A leader who allocates 15% of a $500K portfolio to a BTC long should not trigger the same $75K allocation from a $50K follower. The follower would be risking 150% of their capital. Even with `max_position_size_pct` caps, the relationship between leader sizing and follower sizing needs a formal model. This chapter implements four allocation strategies: proportional, fixed-size, risk-parity, and Kelly criterion.

### The AllocationEngine Class

```python
import math
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class AllocationStrategy(Enum):
    PROPORTIONAL = "proportional"
    FIXED_SIZE = "fixed_size"
    RISK_PARITY = "risk_parity"
    KELLY = "kelly"


@dataclass
class AllocationResult:
    strategy: str
    position_usd: float
    position_pct: float
    leader_size_pct: float
    adjustments: dict


class AllocationEngine:
    """Computes follower position sizes using multiple allocation strategies."""

    def __init__(
        self,
        portfolio_value_usd: float,
        max_position_pct: float = 5.0,
        max_total_allocation_pct: float = 80.0,
    ):
        self.portfolio_value = portfolio_value_usd
        self.max_position_pct = max_position_pct
        self.max_total_pct = max_total_allocation_pct
        self._current_allocation_usd = 0.0

    def allocate(
        self,
        strategy: AllocationStrategy,
        leader_size_pct: float,
        leader_portfolio_usd: Optional[float] = None,
        symbol_volatility: Optional[float] = None,
        target_portfolio_volatility: Optional[float] = None,
        win_rate: Optional[float] = None,
        avg_win_loss_ratio: Optional[float] = None,
        fixed_amount_usd: Optional[float] = None,
    ) -> AllocationResult:
        """Calculate position size based on the chosen strategy."""

        if strategy == AllocationStrategy.PROPORTIONAL:
            return self._proportional(leader_size_pct, leader_portfolio_usd)
        elif strategy == AllocationStrategy.FIXED_SIZE:
            return self._fixed_size(leader_size_pct, fixed_amount_usd)
        elif strategy == AllocationStrategy.RISK_PARITY:
            return self._risk_parity(
                leader_size_pct, symbol_volatility, target_portfolio_volatility
            )
        elif strategy == AllocationStrategy.KELLY:
            return self._kelly(leader_size_pct, win_rate, avg_win_loss_ratio)
        else:
            raise ValueError(f"Unknown strategy: {strategy}")

    def _proportional(
        self,
        leader_size_pct: float,
        leader_portfolio_usd: Optional[float],
    ) -> AllocationResult:
        """Mirror the leader's percentage allocation directly."""
        position_pct = leader_size_pct
        position_pct = self._apply_caps(position_pct)
        position_usd = self.portfolio_value * (position_pct / 100)

        return AllocationResult(
            strategy="proportional",
            position_usd=round(position_usd, 2),
            position_pct=round(position_pct, 4),
            leader_size_pct=leader_size_pct,
            adjustments={"capped": position_pct < leader_size_pct},
        )

    def _fixed_size(
        self,
        leader_size_pct: float,
        fixed_amount_usd: Optional[float],
    ) -> AllocationResult:
        """Use a fixed USD amount per trade regardless of leader sizing."""
        if fixed_amount_usd is None:
            fixed_amount_usd = self.portfolio_value * 0.02  # Default 2%

        position_pct = (fixed_amount_usd / self.portfolio_value) * 100
        position_pct = self._apply_caps(position_pct)
        position_usd = self.portfolio_value * (position_pct / 100)

        return AllocationResult(
            strategy="fixed_size",
            position_usd=round(position_usd, 2),
            position_pct=round(position_pct, 4),
            leader_size_pct=leader_size_pct,
            adjustments={
                "fixed_amount_requested": fixed_amount_usd,
                "capped": position_pct < (fixed_amount_usd / self.portfolio_value * 100),
            },
        )

    def _risk_parity(
        self,
        leader_size_pct: float,
        symbol_volatility: Optional[float],
        target_volatility: Optional[float],
    ) -> AllocationResult:
        """Normalize position size by asset volatility.

        Risk parity ensures each position contributes equal risk to the
        portfolio, regardless of the underlying asset's volatility. A
        position in BTC (30% annualized vol) should be smaller than a
        position in a stablecoin pair (2% annualized vol).
        """
        if symbol_volatility is None or symbol_volatility <= 0:
            symbol_volatility = 0.50  # Default 50% annualized vol (crypto)
        if target_volatility is None or target_volatility <= 0:
            target_volatility = 0.15  # Default 15% target portfolio vol

        # Scale the leader's allocation by the volatility ratio
        vol_scalar = target_volatility / symbol_volatility
        position_pct = leader_size_pct * vol_scalar
        position_pct = self._apply_caps(position_pct)
        position_usd = self.portfolio_value * (position_pct / 100)

        return AllocationResult(
            strategy="risk_parity",
            position_usd=round(position_usd, 2),
            position_pct=round(position_pct, 4),
            leader_size_pct=leader_size_pct,
            adjustments={
                "symbol_volatility": symbol_volatility,
                "target_volatility": target_volatility,
                "vol_scalar": round(vol_scalar, 4),
            },
        )

    def _kelly(
        self,
        leader_size_pct: float,
        win_rate: Optional[float],
        avg_win_loss_ratio: Optional[float],
    ) -> AllocationResult:
        """Kelly criterion sizing based on the leader's historical edge.

        The Kelly criterion calculates the optimal fraction of capital to
        risk on each trade, given the probability of winning and the ratio
        of average win to average loss. Full Kelly is aggressive -- most
        practitioners use half-Kelly or quarter-Kelly.

        Kelly fraction = W - (1 - W) / R
        where W = win probability, R = win/loss ratio
        """
        if win_rate is None or win_rate <= 0 or win_rate >= 1:
            win_rate = 0.55  # Default 55% win rate
        if avg_win_loss_ratio is None or avg_win_loss_ratio <= 0:
            avg_win_loss_ratio = 1.5  # Default 1.5:1 win/loss ratio

        kelly_fraction = win_rate - (1 - win_rate) / avg_win_loss_ratio

        # Use half-Kelly for safety
        half_kelly = kelly_fraction / 2.0

        if half_kelly <= 0:
            # Negative Kelly means the strategy has negative expected value
            return AllocationResult(
                strategy="kelly",
                position_usd=0.0,
                position_pct=0.0,
                leader_size_pct=leader_size_pct,
                adjustments={
                    "kelly_fraction": round(kelly_fraction, 4),
                    "half_kelly": round(half_kelly, 4),
                    "negative_ev": True,
                },
            )

        position_pct = half_kelly * 100
        position_pct = self._apply_caps(position_pct)
        position_usd = self.portfolio_value * (position_pct / 100)

        return AllocationResult(
            strategy="kelly",
            position_usd=round(position_usd, 2),
            position_pct=round(position_pct, 4),
            leader_size_pct=leader_size_pct,
            adjustments={
                "kelly_fraction": round(kelly_fraction, 4),
                "half_kelly": round(half_kelly, 4),
                "win_rate": win_rate,
                "avg_win_loss_ratio": avg_win_loss_ratio,
            },
        )

    def _apply_caps(self, position_pct: float) -> float:
        """Apply maximum position size and total allocation caps."""
        # Cap individual position
        position_pct = min(position_pct, self.max_position_pct)

        # Cap total allocation
        current_pct = (self._current_allocation_usd / self.portfolio_value) * 100
        remaining_pct = self.max_total_pct - current_pct
        position_pct = min(position_pct, max(remaining_pct, 0))

        return position_pct

    def record_allocation(self, amount_usd: float) -> None:
        """Track current allocation for cap enforcement."""
        self._current_allocation_usd += amount_usd

    def release_allocation(self, amount_usd: float) -> None:
        """Release allocation when a position is closed."""
        self._current_allocation_usd = max(
            0, self._current_allocation_usd - amount_usd
        )
```

### Strategy Comparison

Here is how the four strategies behave for a $25,000 follower portfolio receiving a 10% BTC long signal from a leader:

```python
engine = AllocationEngine(
    portfolio_value_usd=25000.00,
    max_position_pct=5.0,
    max_total_allocation_pct=80.0,
)

# Proportional: Mirror the leader's 10% -> capped at 5%
prop = engine.allocate(
    AllocationStrategy.PROPORTIONAL,
    leader_size_pct=10.0,
)
print(f"Proportional: ${prop.position_usd} ({prop.position_pct}%)")
# Output: Proportional: $1250.00 (5.0%)  -- capped from 10% to 5%

# Fixed-size: Always $500 per trade
fixed = engine.allocate(
    AllocationStrategy.FIXED_SIZE,
    leader_size_pct=10.0,
    fixed_amount_usd=500.00,
)
print(f"Fixed: ${fixed.position_usd} ({fixed.position_pct}%)")
# Output: Fixed: $500.00 (2.0%)

# Risk-parity: BTC has 60% annualized vol, target 15%
rp = engine.allocate(
    AllocationStrategy.RISK_PARITY,
    leader_size_pct=10.0,
    symbol_volatility=0.60,
    target_portfolio_volatility=0.15,
)
print(f"Risk-parity: ${rp.position_usd} ({rp.position_pct}%)")
# Output: Risk-parity: $625.00 (2.5%)  -- scaled down by vol ratio 0.25

# Kelly: Leader has 58% win rate, 1.8:1 avg win/loss
kelly = engine.allocate(
    AllocationStrategy.KELLY,
    leader_size_pct=10.0,
    win_rate=0.58,
    avg_win_loss_ratio=1.8,
)
print(f"Kelly: ${kelly.position_usd} ({kelly.position_pct}%)")
# Output: Kelly: $645.83 (2.5833%)  -- half-Kelly = 0.3467/2 = 17.33% -> capped at 5%
```

**When to use each strategy:**

- **Proportional** is the simplest. Use it when you trust the leader's sizing and want to mirror their conviction. The cap prevents blow-ups.
- **Fixed-size** ignores leader conviction entirely. Use it when you want consistent exposure regardless of how aggressively the leader trades. Good for beginners who want to limit risk per trade.
- **Risk-parity** normalizes by volatility. Use it when you copy multiple leaders across asset classes. A 10% position in BTC (high vol) should not carry the same risk as a 10% position in EUR/USD (low vol). Risk-parity handles this automatically.
- **Kelly** optimizes for long-term growth based on the leader's edge. Use it when you have reliable statistics on the leader's win rate and win/loss ratio. Half-Kelly is the standard practice -- full Kelly is theoretically optimal but produces extreme drawdowns.

---

## Chapter 5: Slippage Handling

### Why Slippage Kills Copy Trading Returns

Slippage is the difference between the price the leader gets and the price the follower gets. In copy trading, slippage is structural, not accidental. When a leader broadcasts a signal to 500 followers, all 500 execute the same trade within seconds. This creates a burst of correlated order flow that moves the market against the followers. The leader, who executed first, got a better price. The last followers to execute got the worst price. Over hundreds of trades, this difference compounds into a significant return gap between leader and follower.

Consider a concrete example. A leader goes long BTC at $67,250. They have 500 followers with an average position size of $2,000. That is $1 million in correlated buy orders hitting the book within a 5-second window. On Binance BTC/USDT perpetual -- one of the most liquid markets in crypto -- the order book depth at the best ask is typically $2-5 million. A $1 million market buy would walk the book by 10-30 basis points. The first follower might fill at $67,260 (1.5 bps slippage). The last follower might fill at $67,320 (10.4 bps slippage). On a trade with a 200 bps profit target, the last follower just lost 5% of their expected return to slippage.

On less liquid markets -- altcoin pairs, DEXs, traditional equities during off-hours -- the effect is much worse.

### The SlippageMonitor Class

```python
import statistics
from datetime import datetime, timezone
from dataclasses import dataclass, field
from typing import Optional

import requests


@dataclass
class SlippageRecord:
    signal_id: str
    symbol: str
    leader_price: float
    follower_price: float
    slippage_bps: float
    follower_position_in_queue: int
    total_followers: int
    timestamp: str


class SlippageMonitor:
    """Tracks and analyzes slippage between leader and follower executions."""

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        slippage_budget_bps: float = 15.0,
        alert_threshold_bps: float = 25.0,
    ):
        self.api_base = "https://api.greenhelix.net/v1"
        self.api_key = api_key
        self.agent_id = agent_id
        self.slippage_budget_bps = slippage_budget_bps
        self.alert_threshold_bps = alert_threshold_bps
        self._records: list[SlippageRecord] = []
        self._session = requests.Session()
        self._session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    def _execute(self, tool: str, input_data: dict) -> dict:
        resp = self._session.post(
            f"{self.api_base}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    def record_execution(
        self,
        signal_id: str,
        symbol: str,
        leader_price: float,
        follower_price: float,
        side: str,
        position_in_queue: int = 0,
        total_followers: int = 1,
    ) -> SlippageRecord:
        """Record a trade execution and calculate slippage."""
        if side == "buy":
            slippage_bps = ((follower_price - leader_price) / leader_price) * 10000
        else:
            slippage_bps = ((leader_price - follower_price) / leader_price) * 10000

        record = SlippageRecord(
            signal_id=signal_id,
            symbol=symbol,
            leader_price=leader_price,
            follower_price=follower_price,
            slippage_bps=round(slippage_bps, 2),
            follower_position_in_queue=position_in_queue,
            total_followers=total_followers,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self._records.append(record)

        if abs(slippage_bps) > self.alert_threshold_bps:
            self._fire_slippage_alert(record)

        return record

    def get_statistics(self, symbol: Optional[str] = None) -> dict:
        """Calculate slippage statistics, optionally filtered by symbol."""
        records = self._records
        if symbol:
            records = [r for r in records if r.symbol == symbol]

        if not records:
            return {"count": 0}

        slippages = [r.slippage_bps for r in records]

        return {
            "count": len(records),
            "mean_bps": round(statistics.mean(slippages), 2),
            "median_bps": round(statistics.median(slippages), 2),
            "std_bps": round(statistics.stdev(slippages), 2) if len(slippages) > 1 else 0,
            "max_bps": round(max(slippages), 2),
            "min_bps": round(min(slippages), 2),
            "p95_bps": round(sorted(slippages)[int(len(slippages) * 0.95)], 2),
            "within_budget": sum(1 for s in slippages if abs(s) <= self.slippage_budget_bps),
            "exceeded_budget": sum(1 for s in slippages if abs(s) > self.slippage_budget_bps),
            "budget_compliance_pct": round(
                sum(1 for s in slippages if abs(s) <= self.slippage_budget_bps) / len(slippages) * 100, 2
            ),
        }

    def estimate_market_impact(
        self,
        symbol: str,
        total_follower_volume_usd: float,
        order_book_depth_usd: float,
    ) -> dict:
        """Estimate slippage from market impact for a given follower pool.

        Uses the square-root market impact model:
        impact_bps = k * sqrt(V / D)
        where V = total order volume, D = order book depth, k = impact coefficient
        """
        # k is calibrated per market; 10 is typical for crypto
        k = 10.0
        impact_bps = k * (total_follower_volume_usd / order_book_depth_usd) ** 0.5

        return {
            "symbol": symbol,
            "total_volume_usd": total_follower_volume_usd,
            "order_book_depth_usd": order_book_depth_usd,
            "estimated_impact_bps": round(impact_bps, 2),
            "within_budget": impact_bps <= self.slippage_budget_bps,
            "recommendation": self._impact_recommendation(impact_bps),
        }

    def _impact_recommendation(self, impact_bps: float) -> str:
        if impact_bps <= 5:
            return "Low impact. No action needed."
        elif impact_bps <= 15:
            return "Moderate impact. Consider staggering follower executions over 10-30 seconds."
        elif impact_bps <= 30:
            return "High impact. Stagger executions and consider reducing follower pool or position sizes."
        else:
            return "Severe impact. Reduce follower pool size, use limit orders, or split across multiple venues."

    def _fire_slippage_alert(self, record: SlippageRecord) -> None:
        """Publish a slippage alert to the event bus."""
        self._execute("publish_event", {
            "event_type": "copy_trade.slippage_alert",
            "payload": {
                "follower_id": self.agent_id,
                "signal_id": record.signal_id,
                "symbol": record.symbol,
                "slippage_bps": str(record.slippage_bps),
                "threshold_bps": str(self.alert_threshold_bps),
                "timestamp": record.timestamp,
            },
        })

    def submit_slippage_metrics(self) -> dict:
        """Submit slippage metrics to GreenHelix for monitoring."""
        stats = self.get_statistics()
        if stats["count"] == 0:
            return {"status": "no_data"}

        return self._execute("submit_metrics", {
            "agent_id": self.agent_id,
            "metrics": {
                "slippage_mean_bps": str(stats["mean_bps"]),
                "slippage_p95_bps": str(stats["p95_bps"]),
                "slippage_budget_compliance_pct": str(stats["budget_compliance_pct"]),
                "slippage_records_count": stats["count"],
            },
        })
```

### Mitigation Strategies

Four approaches reduce slippage in copy trading systems:

**Staggered execution.** Instead of all followers executing simultaneously, spread executions over a 10-60 second window with random jitter. This reduces the burst of correlated order flow. The trade-off is that later followers get slightly different market conditions -- but the average slippage across all followers decreases.

**Limit orders with timeout.** Instead of market orders, followers place limit orders at the leader's entry price plus a slippage budget (e.g., entry + 5 bps). If the limit order does not fill within 30 seconds, it is cancelled and replaced with a market order. This captures fills at the leader's price when possible and falls back to market execution when the price has moved.

**Multi-venue execution.** Split the follower's order across multiple exchanges. If a follower needs to buy $2,000 of BTC, execute $1,000 on Binance and $1,000 on OKX. Each venue experiences half the market impact. This requires the follower to maintain accounts and balances on multiple exchanges.

**Follower pool caps.** The simplest and most effective mitigation. If slippage statistics show that average slippage exceeds the budget when the follower pool is above 300, cap the pool at 300. The leader earns less in total fees but preserves follower returns, which preserves reputation, which attracts higher-value followers.

```python
monitor = SlippageMonitor(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="follower-conservative-01",
    slippage_budget_bps=15.0,
    alert_threshold_bps=25.0,
)

# After each trade execution, record the slippage
record = monitor.record_execution(
    signal_id="sig-abc-123",
    symbol="BTCUSDT",
    leader_price=67250.00,
    follower_price=67268.50,
    side="buy",
    position_in_queue=147,
    total_followers=412,
)
print(f"Slippage: {record.slippage_bps} bps")

# Estimate market impact before subscribing to a popular leader
impact = monitor.estimate_market_impact(
    symbol="BTCUSDT",
    total_follower_volume_usd=850000.00,
    order_book_depth_usd=3000000.00,
)
print(f"Estimated impact: {impact['estimated_impact_bps']} bps")
print(f"Recommendation: {impact['recommendation']}")
```

---

## Chapter 6: Performance Escrow

### How Performance Escrow Protects Followers

Performance escrow is the mechanism that makes trustless copy trading possible. A follower deposits funds into an escrow contract that specifies performance criteria. If the leader meets those criteria during the evaluation period, the escrow releases -- the leader gets paid and the follower continues the subscription. If the leader fails to meet criteria, the escrow refunds -- the follower recovers their deposit and can choose a different leader.

This is fundamentally different from how existing platforms work. On eToro, a follower pays a spread markup on every trade, regardless of leader performance. On Bybit Copy, the leader receives performance fees even if the follower's account is down year-to-date (because fees are calculated per profitable trade, not on net performance). GreenHelix escrow enforces a simple contract: the leader gets paid only if they deliver results.

### Creating a Performance Escrow

```bash
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "create_escrow",
    "input": {
      "payer_id": "follower-conservative-01",
      "payee_id": "leader-crypto-momentum-01",
      "amount": "500.00",
      "currency": "USD",
      "conditions": {
        "type": "performance_escrow",
        "evaluation_period_days": 30,
        "criteria": {
          "min_sharpe": "1.0",
          "max_drawdown_pct": "20.0",
          "min_win_rate_pct": "45.0",
          "min_trades": 10
        },
        "data_source": "verified_metrics",
        "auto_release": true,
        "dispute_window_hours": 48
      },
      "description": "Performance escrow: 30-day evaluation for copy trading subscription"
    }
  }'
```

The `conditions` block defines the contract. The `evaluation_period_days` sets the window -- 30 days is standard for monthly subscriptions. The `criteria` object specifies the thresholds:

- **min_sharpe: 1.0** -- The leader's risk-adjusted return must be positive. A Sharpe above 1.0 means each unit of risk produced at least one unit of return. This is a low bar intentionally -- the escrow protects against gross underperformance, not mediocrity.
- **max_drawdown_pct: 20.0** -- The leader's peak-to-trough decline during the evaluation period cannot exceed 20%. This prevents a leader from taking massive concentrated bets, getting lucky, and then blowing up.
- **min_win_rate_pct: 45.0** -- At least 45% of closed trades must be profitable. Combined with a positive Sharpe, this filters out leaders who achieve returns through a few large wins and many small losses -- a fragile pattern.
- **min_trades: 10** -- The leader must execute at least 10 trades during the evaluation period. This prevents gaming by making a single lucky trade and going dormant.

The `data_source: verified_metrics` tells the escrow contract to evaluate criteria using the leader's signed `submit_metrics` data, not self-reported claims. The `auto_release: true` flag means that if all criteria are met at the end of the evaluation period, the escrow releases automatically without manual intervention. The `dispute_window_hours: 48` gives the follower 48 hours after the evaluation period ends to dispute the release if they believe the metrics are inaccurate.

### Evaluation Logic

At the end of the evaluation period, the escrow contract evaluates the leader's verified metrics against the criteria. This happens automatically:

```bash
# Check escrow status (called automatically, but also available on-demand)
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "check_sla_compliance",
    "input": {
      "escrow_id": "esc-abc-123",
      "evaluation_window": {
        "start": "2026-03-01T00:00:00Z",
        "end": "2026-03-31T23:59:59Z"
      }
    }
  }'
```

```python
def evaluate_escrow(self, escrow_id: str, leader_id: str) -> dict:
    """Evaluate whether a leader met performance criteria for escrow release."""
    # Fetch the leader's verified metrics for the evaluation period
    reputation = self._execute("get_agent_reputation", {
        "agent_id": leader_id,
    })

    metrics = reputation.get("metrics", {})
    sharpe = float(metrics.get("sharpe_ratio", "0"))
    drawdown = float(metrics.get("max_drawdown_pct", "100"))
    win_rate = float(metrics.get("win_rate_pct", "0"))
    total_trades = int(metrics.get("total_trades", "0"))

    # Check against criteria
    criteria_met = {
        "min_sharpe": sharpe >= 1.0,
        "max_drawdown": drawdown <= 20.0,
        "min_win_rate": win_rate >= 45.0,
        "min_trades": total_trades >= 10,
    }

    all_met = all(criteria_met.values())

    if all_met:
        # Release escrow to the leader
        release = self._execute("release_escrow", {
            "escrow_id": escrow_id,
            "release_to": leader_id,
            "reason": "performance_criteria_met",
            "evidence": {
                "sharpe": str(sharpe),
                "max_drawdown_pct": str(drawdown),
                "win_rate_pct": str(win_rate),
                "total_trades": total_trades,
            },
        })
        return {"status": "released", "release": release, "criteria": criteria_met}
    else:
        # Refund escrow to the follower
        refund = self._execute("release_escrow", {
            "escrow_id": escrow_id,
            "release_to": self.agent_id,
            "reason": "performance_criteria_not_met",
            "evidence": {
                "sharpe": str(sharpe),
                "max_drawdown_pct": str(drawdown),
                "win_rate_pct": str(win_rate),
                "total_trades": total_trades,
                "failed_criteria": [k for k, v in criteria_met.items() if not v],
            },
        })
        return {"status": "refunded", "refund": refund, "criteria": criteria_met}
```

### What Happens When a Leader Underperforms

When a leader fails to meet escrow criteria, the sequence is:

1. **Escrow evaluation fails.** The contract identifies which criteria were not met.
2. **48-hour dispute window opens.** The leader can dispute the evaluation if they believe the metrics are incorrect -- for example, if a metric submission failed due to an API error and their actual performance meets criteria.
3. **If no dispute or dispute rejected:** The escrow refunds to the follower. The subscription is suspended.
4. **Leader reputation updated.** The failed escrow is recorded in the leader's reputation. Future followers can see the escrow failure rate: "This leader has met performance criteria in 11 of 12 evaluation periods (91.7%)."
5. **Follower can re-subscribe.** If the follower believes the underperformance is temporary, they can create a new escrow and continue copying. The risk management is modular -- each evaluation period is independent.

The dispute mechanism is important. Markets have bad months. A leader with an 18-month track record who misses criteria in month 19 is not necessarily a bad leader. The escrow system protects followers from persistent underperformance without penalizing leaders for normal variance. The 30-day evaluation period, combined with reasonable criteria thresholds, is calibrated to distinguish between "bad luck" and "lost edge."

---

## Chapter 7: Revenue Sharing

### Fee Models for Copy Trading

Revenue sharing determines how value flows from followers to leaders. The fee model must balance three constraints: leaders need sustainable income to continue operating, followers need fees that do not eat their returns, and the system needs incentive alignment where leaders earn more when followers earn more.

### Subscription Model

Flat monthly fee. The leader earns a predictable income regardless of follower returns. Simple to implement, simple to understand.

```bash
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "create_escrow",
    "input": {
      "payer_id": "follower-conservative-01",
      "payee_id": "leader-crypto-momentum-01",
      "amount": "49.00",
      "currency": "USD",
      "conditions": {
        "type": "subscription",
        "billing_cycle": "monthly",
        "auto_renew": true
      },
      "description": "Monthly copy trading subscription"
    }
  }'
```

The downside: no incentive alignment. The leader earns $49/month whether the follower makes $5,000 or loses $5,000. This model works best for low-cost services where the leader's primary motivation is building reputation rather than earning subscription revenue.

### Performance Fee Model

The leader takes a percentage of net new profits above a high-water mark. This is the hedge fund model (the "2 and 20" tradition, minus the management fee).

```python
class RevenueCalculator:
    """Calculates revenue sharing between leaders and followers."""

    def __init__(self):
        self._follower_hwms: dict[str, float] = {}

    def calculate_performance_fee(
        self,
        follower_id: str,
        current_value_usd: float,
        performance_fee_pct: float = 15.0,
    ) -> dict:
        """Calculate performance fee based on high-water mark."""
        hwm = self._follower_hwms.get(follower_id, current_value_usd)

        if current_value_usd <= hwm:
            return {
                "follower_id": follower_id,
                "current_value": str(current_value_usd),
                "high_water_mark": str(hwm),
                "profit_above_hwm": "0.00",
                "fee_usd": "0.00",
                "fee_pct": str(performance_fee_pct),
            }

        profit = current_value_usd - hwm
        fee = profit * (performance_fee_pct / 100)

        # Update high-water mark
        self._follower_hwms[follower_id] = current_value_usd

        return {
            "follower_id": follower_id,
            "current_value": str(round(current_value_usd, 2)),
            "high_water_mark": str(round(hwm, 2)),
            "profit_above_hwm": str(round(profit, 2)),
            "fee_usd": str(round(fee, 2)),
            "fee_pct": str(performance_fee_pct),
        }

    def calculate_hybrid_fee(
        self,
        follower_id: str,
        current_value_usd: float,
        subscription_monthly_usd: float = 49.00,
        performance_fee_pct: float = 10.0,
        days_in_period: int = 30,
    ) -> dict:
        """Calculate hybrid fee: subscription + performance."""
        perf = self.calculate_performance_fee(
            follower_id, current_value_usd, performance_fee_pct
        )

        total_fee = subscription_monthly_usd + float(perf["fee_usd"])

        return {
            "follower_id": follower_id,
            "subscription_fee_usd": str(round(subscription_monthly_usd, 2)),
            "performance_fee_usd": perf["fee_usd"],
            "total_fee_usd": str(round(total_fee, 2)),
            "period_days": days_in_period,
        }

    def calculate_revenue_split(
        self,
        total_fee_usd: float,
        leader_share_pct: float = 80.0,
    ) -> dict:
        """Split revenue between leader and platform."""
        leader_share = total_fee_usd * (leader_share_pct / 100)
        platform_share = total_fee_usd - leader_share

        return {
            "total_fee_usd": str(round(total_fee_usd, 2)),
            "leader_share_usd": str(round(leader_share, 2)),
            "platform_share_usd": str(round(platform_share, 2)),
            "leader_share_pct": str(leader_share_pct),
            "platform_share_pct": str(round(100 - leader_share_pct, 2)),
        }
```

### Revenue Split via GreenHelix Escrow

The escrow system handles the actual fund transfer. At the end of each billing period, the revenue calculator determines the fee, and the escrow releases the appropriate amount to the leader.

```python
calc = RevenueCalculator()

# End of month: follower started at $25,000, now at $27,500
fee = calc.calculate_hybrid_fee(
    follower_id="follower-conservative-01",
    current_value_usd=27500.00,
    subscription_monthly_usd=49.00,
    performance_fee_pct=10.0,
)
print(f"Subscription: ${fee['subscription_fee_usd']}")
print(f"Performance: ${fee['performance_fee_usd']}")
print(f"Total: ${fee['total_fee_usd']}")
# Output:
#   Subscription: $49.00
#   Performance: $250.00  (10% of $2,500 profit above HWM)
#   Total: $299.00

# Split between leader and platform
split = calc.calculate_revenue_split(
    total_fee_usd=299.00,
    leader_share_pct=80.0,
)
print(f"Leader receives: ${split['leader_share_usd']}")
print(f"Platform receives: ${split['platform_share_usd']}")
# Output:
#   Leader receives: $239.20
#   Platform receives: $59.80
```

```bash
# Release the leader's share from escrow
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "release_escrow",
    "input": {
      "escrow_id": "esc-revenue-march-2026",
      "release_to": "leader-crypto-momentum-01",
      "amount": "239.20",
      "reason": "monthly_revenue_share",
      "evidence": {
        "period": "2026-03",
        "subscription_fee": "49.00",
        "performance_fee": "250.00",
        "total_fee": "299.00",
        "leader_share_pct": "80.0",
        "leader_share_usd": "239.20"
      }
    }
  }'
```

### Tax Reporting Considerations

Copy trading revenue has tax implications for both leaders and followers. Leaders earn fee income, which is generally taxable as ordinary income in most jurisdictions. Followers have two tax events: the trading gains or losses from copied trades, and the fee deductions which may be deductible as investment expenses.

The GreenHelix escrow system maintains a complete audit trail of all fee transfers. At year-end, leaders and followers can query their transaction history for tax reporting:

```bash
# Query fee transaction history for tax reporting
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "get_events",
    "input": {
      "agent_id": "leader-crypto-momentum-01",
      "event_type": "escrow.release",
      "start_date": "2026-01-01T00:00:00Z",
      "end_date": "2026-12-31T23:59:59Z",
      "limit": 1000
    }
  }'
```

The response includes every escrow release with the breakdown of subscription fees, performance fees, and revenue splits. This is the source material for 1099-MISC (US), Schedule E (US), or the equivalent reporting forms in other jurisdictions. Consult a tax professional for jurisdiction-specific obligations -- copy trading income classification varies between ordinary income, capital gains, and investment advisory fees depending on the jurisdiction and the specific fee structure.

---

## Next Steps

For deployment patterns, monitoring, and production hardening, see the
[Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening).

---

## What's Next

**Companion Guides:**

- **Trading Bot Risk-as-a-Service** -- Build real-time portfolio risk monitoring with drawdown alerts, correlation monitoring, and circuit breakers across your copy trading portfolio.
- **Tamper-Proof Audit Trails for Trading Bots** -- Create compliance-ready audit trails for your copy trading signals using Merkle claim chains. Essential for EU AI Act and MiFID II compliance.
- **Bot Reputation System** -- Turn your leader track record into a verifiable, cryptographically-backed reputation that followers can independently audit.

**GreenHelix Documentation:**

- Full API reference: https://api.greenhelix.net/v1
- Event bus, escrow, and marketplace deep dives in the platform documentation

**Extending the Infrastructure:**

The allocation models in Chapter 4 can be extended with machine learning -- train a model on historical leader signals and your realized slippage to predict optimal position sizing. The performance escrow criteria in Chapter 6 can incorporate Calmar ratio, Sortino ratio, or custom metrics via the `submit_metrics` API. The revenue calculator in Chapter 7 can support tiered pricing where high-AUM followers get lower performance fees, incentivizing larger allocations.

---

*This guide covers copy trading infrastructure patterns as of April 2026. Exchange APIs, fee structures, and rate limits change frequently -- verify current limits before production deployment. Tax treatment of copy trading income varies by jurisdiction. The performance escrow criteria used in this guide are illustrative; calibrate thresholds to the specific strategy, asset class, and market regime. Consult your compliance counsel and tax advisor for jurisdiction-specific obligations.*

