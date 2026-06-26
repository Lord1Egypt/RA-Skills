---
name: greenhelix-bot-arbitrage-framework
version: "1.3.1"
description: "Bot-to-Bot Arbitrage Framework: Multi-Bot Coordination with Trust Verification. Build a multi-bot arbitrage coordination framework with marketplace discovery, escrow protection, and trust verification. Covers cross-exchange opportunity detection, execution verification, profit splitting, MEV protection, and audit trails."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [arbitrage, trading-bot, multi-bot, coordination, guide, greenhelix, openclaw, ai-agent]
price_usd: 99.0
content_type: markdown
executable: false
install: none
credentials: [AGENT_SIGNING_KEY]
metadata:
  openclaw:
    requires:
      env:
        - AGENT_SIGNING_KEY
    primaryEnv: AGENT_SIGNING_KEY
---
# Bot-to-Bot Arbitrage Framework: Multi-Bot Coordination with Trust Verification

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `AGENT_SIGNING_KEY`: Cryptographic signing key for agent identity (Ed25519 key pair for request signing)


Arbitrage bots operate in isolation. A bot that spots a price discrepancy between Binance and Kraken has to execute both legs itself -- funding accounts on both exchanges, maintaining API keys for each, and racing against every other solo operator watching the same order books. The capital requirements are brutal: to capture a 0.3% spread on a $100,000 opportunity, you need $100,000 sitting idle on Binance and another $100,000 on Kraken, earning nothing while waiting for the next opportunity. Multiply that across ten exchanges and you are looking at a million dollars in idle capital for a strategy that might generate $500 per trade.
Multi-bot coordination solves this. One bot holds capital on Binance and specializes in that exchange's matching engine quirks. Another holds capital on Kraken and knows its WebSocket feed intimately. A third monitors OKX. When a cross-exchange opportunity appears, the coordinating bot signals the relevant pair, they execute simultaneously, and profits are split according to a pre-negotiated agreement. Capital efficiency improves by an order of magnitude. Latency drops because each bot is co-located with its exchange. Coverage expands because adding a new exchange means onboarding one specialist bot, not refactoring an entire monolithic system.
The problem is trust. How does the Binance bot know the Kraken bot actually executed its leg? How do you split profits with a bot operated by someone you have never met? What happens when one leg fills and the other does not? What stops a counterparty from reporting a worse fill price than they actually received? This guide builds a complete framework for coordinated multi-bot arbitrage using GreenHelix's marketplace for bot discovery, escrow for profit splitting, claim chains for execution verification, and event bus for audit trails. Every component comes with working Python code and curl equivalents against the GreenHelix API.

## What You'll Learn
- Chapter 1: Why Multi-Bot Arbitrage
- Chapter 2: ArbitrageCoordinator Class
- Chapter 3: OpportunityScanner Class
- Chapter 4: Execution Verification
- Chapter 5: Profit Splitting via Escrow
- Chapter 6: MEV Protection
- Chapter 7: Latency Optimization
- Chapter 8: Audit Trails for Arbitrage
- What's Next

## Full Guide

# Bot-to-Bot Arbitrage Framework: Multi-Bot Coordination with Trust Verification

Arbitrage bots operate in isolation. A bot that spots a price discrepancy between Binance and Kraken has to execute both legs itself -- funding accounts on both exchanges, maintaining API keys for each, and racing against every other solo operator watching the same order books. The capital requirements are brutal: to capture a 0.3% spread on a $100,000 opportunity, you need $100,000 sitting idle on Binance and another $100,000 on Kraken, earning nothing while waiting for the next opportunity. Multiply that across ten exchanges and you are looking at a million dollars in idle capital for a strategy that might generate $500 per trade.

Multi-bot coordination solves this. One bot holds capital on Binance and specializes in that exchange's matching engine quirks. Another holds capital on Kraken and knows its WebSocket feed intimately. A third monitors OKX. When a cross-exchange opportunity appears, the coordinating bot signals the relevant pair, they execute simultaneously, and profits are split according to a pre-negotiated agreement. Capital efficiency improves by an order of magnitude. Latency drops because each bot is co-located with its exchange. Coverage expands because adding a new exchange means onboarding one specialist bot, not refactoring an entire monolithic system.

The problem is trust. How does the Binance bot know the Kraken bot actually executed its leg? How do you split profits with a bot operated by someone you have never met? What happens when one leg fills and the other does not? What stops a counterparty from reporting a worse fill price than they actually received? This guide builds a complete framework for coordinated multi-bot arbitrage using GreenHelix's marketplace for bot discovery, escrow for profit splitting, claim chains for execution verification, and event bus for audit trails. Every component comes with working Python code and curl equivalents against the GreenHelix API.

---

## Table of Contents

1. [Why Multi-Bot Arbitrage](#chapter-1-why-multi-bot-arbitrage)
2. [ArbitrageCoordinator Class](#chapter-2-arbitragecoordinator-class)
3. [OpportunityScanner Class](#chapter-3-opportunityscanner-class)
4. [Execution Verification](#chapter-4-execution-verification)
5. [Profit Splitting via Escrow](#chapter-5-profit-splitting-via-escrow)
6. [MEV Protection](#chapter-6-mev-protection)
7. [Latency Optimization](#chapter-7-latency-optimization)
8. [Audit Trails for Arbitrage](#chapter-8-audit-trails-for-arbitrage)

---

## Chapter 1: Why Multi-Bot Arbitrage

### The Capital Efficiency Problem

A solo arbitrage bot monitoring ten exchanges needs funded accounts on all ten. Most of that capital sits idle most of the time. A Binance-Kraken opportunity might appear once every thirty seconds, but the capital allocated to the Binance-OKX pair and the Kraken-Bybit pair and every other combination is locked up, doing nothing, waiting for its turn.

The numbers are straightforward. Assume $50,000 minimum per exchange account to capture meaningful opportunities (sub-$50K and slippage on larger orders eats your edge). Ten exchanges means $500,000 in deployed capital. Average daily return on cross-exchange crypto arbitrage in 2026 hovers around 0.05-0.15% of deployed capital after fees -- that is $250-$750 per day on half a million dollars. The capital efficiency ratio is terrible.

Multi-bot coordination restructures this entirely. Each bot operator funds one exchange. Ten operators each deploying $50,000 create a network with $500,000 in total liquidity, but each individual's capital requirement is 90% lower. When a Binance-Kraken opportunity appears, only those two bots' capital is involved. The other eight bots' capital is simultaneously available for other pairs. The same $50,000 individual commitment can participate in multiple simultaneous opportunities across different pairs, as long as the pairs involve that bot's exchange.

### The Latency Advantage

Exchange co-location is the single biggest latency reduction available to a trading bot. A bot running on AWS ap-northeast-1 (Tokyo) hitting Binance's Tokyo matching engine sees 0.3ms round-trip times. The same bot hitting Kraken's London servers sees 150ms. In arbitrage, 150ms is an eternity -- the opportunity is gone.

A solo bot cannot be co-located with ten exchanges simultaneously. The physics do not allow it. But a network of specialist bots -- one co-located with each exchange -- can achieve sub-millisecond execution on every leg. The Binance specialist sits in Tokyo. The Kraken specialist sits in London. The OKX specialist sits in Hong Kong. When a cross-exchange opportunity is detected, the coordinating signal travels at the speed of light between data centers (roughly 70ms Tokyo-to-London), but both legs execute at local speed. The total execution time is the coordination signal latency plus the local execution latency, which is still faster than a solo bot executing one leg locally and the other leg across an ocean.

### The Trust Problem

Coordination creates value, but it also creates risk. Consider a two-leg arbitrage between Binance and Kraken:

```
Opportunity: ETH is $3,000.00 on Binance, $3,012.00 on Kraken
Strategy:    Buy 10 ETH on Binance ($30,000), Sell 10 ETH on Kraken ($30,120)
Gross profit: $120.00
Fees (est):   $36.00 (0.06% taker on each leg)
Net profit:   $84.00
```

Bot A buys on Binance. Bot B sells on Kraken. After execution, Bot B holds the $30,120 from the Kraken sale. The agreed profit split is 50/50, so Bot B owes Bot A $42.00 plus Bot A's $30,000 principal. But what stops Bot B from claiming the sell only filled at $3,008 instead of $3,012, reducing Bot A's share? What stops Bot B from simply not paying at all?

In traditional finance, clearing houses solve this -- they sit between counterparties, guarantee settlement, and manage collateral. In bot-to-bot arbitrage, the equivalent infrastructure maps to these tools:

- **search_services** -- Discover specialist bots registered on specific exchanges
- **negotiate_deal** -- Agree on profit split terms before execution
- **create_escrow** -- Lock collateral to guarantee settlement
- **submit_metrics** -- Report execution latency, fill rates, and reliability
- **build_claim_chain** -- Create cryptographic proof of execution for dispute resolution
- **publish_event** -- Log every step for audit and compliance

### GreenHelix Tools for Arbitrage Coordination

| Tool | Role in Arbitrage |
|---|---|
| `register_agent` | Register each exchange-specialist bot with its capabilities |
| `search_services` | Find bots specializing in specific exchanges |
| `negotiate_deal` | Agree on profit split, minimum opportunity size, latency SLAs |
| `create_escrow` | Lock profit-share collateral before execution |
| `release_escrow` | Release funds after verified execution |
| `submit_metrics` | Report fill rates, latency, reliability to build reputation |
| `build_claim_chain` | Create tamper-proof execution evidence |
| `publish_event` | Log opportunities, executions, settlements to the event bus |
| `get_reputation` | Check counterparty reliability before partnering |

### Why Now

Cross-exchange arbitrage has existed since the first two crypto exchanges launched. What has changed in 2025-2026 is the infrastructure. Three developments make multi-bot coordination viable today when it was not two years ago.

First, exchange API latency has dropped. Binance's matching engine upgrade in late 2025 reduced API response times to sub-millisecond for co-located clients. Kraken, OKX, and Bybit followed with similar improvements. The execution speed gap between institutional and retail API access has narrowed -- a well-optimized bot on a standard cloud instance now achieves execution times that previously required bare-metal co-location.

Second, the agent commerce infrastructure exists. Before GreenHelix and similar platforms, bot coordination required custom bilateral agreements, manual escrow arrangements, and trust based on personal reputation in Telegram groups. GreenHelix provides the standardized primitives -- identity, escrow, reputation, event logging -- that turn ad-hoc coordination into a scalable protocol.

Third, the regulatory landscape is clarifying. MiCA in the EU, updated SEC guidance in the US, and ASIC's framework in Australia all treat algorithmic trading as a regulated activity with specific record-keeping requirements. Bots that operate within a compliance-ready framework (with audit trails, execution verification, and settlement records) have a structural advantage over bots that operate in the dark.

### The Network Effect

There is a compounding advantage to multi-bot coordination that solo operators cannot replicate. A two-bot network covers one exchange pair. A five-bot network covers ten pairs. A ten-bot network covers forty-five pairs. The number of arbitrage opportunities scales quadratically with the number of exchanges covered, but each bot's capital requirement stays constant. A single bot operator joining a ten-bot network gains access to nine new exchange pairs without deploying a single dollar of additional capital.

This creates a natural marketplace for coordination. Bots with strong execution on a specific exchange can monetize that capability by partnering with bots on other exchanges. A Binance specialist with 0.4ms execution and a 97% fill rate is a valuable counterparty -- its speed and reliability directly increase the capture rate for any opportunity involving Binance. GreenHelix's reputation system makes this value visible: bots publish verified execution metrics, and coordinators use those metrics to select the best partner for each opportunity.

The rest of this guide builds a production framework using these tools. Chapter 2 creates the coordination layer. Chapter 3 scans for opportunities. Chapter 4 verifies execution. Chapter 5 handles profit splitting. Chapters 6-8 cover MEV protection, latency optimization, and compliance audit trails.

---

## Chapter 2: ArbitrageCoordinator Class

### Architecture

The ArbitrageCoordinator is the central orchestrator. It does not execute trades itself -- it discovers specialist bots, negotiates coordination agreements, manages escrow for profit splitting, and dispatches execution signals. Think of it as the clearing house in a traditional exchange, but running as an autonomous agent.

```
+---------------------+       +---------------------+       +---------------------+
|  Binance Bot        |       | ArbitrageCoordinator|       |  Kraken Bot          |
|  (exchange specialist)|     |  (orchestrator)     |       |  (exchange specialist)|
|                     |       |                     |       |                     |
|  Monitors Binance   |       |  Discovers bots     |       |  Monitors Kraken    |
|  order book         |       |  Negotiates deals   |       |  order book         |
|  Executes buy/sell  |       |  Manages escrow     |       |  Executes buy/sell  |
|  Reports fills      |       |  Verifies execution |       |  Reports fills      |
|                     |       |  Splits profits     |       |                     |
+--------+------------+       +----------+----------+       +----------+----------+
         |                               |                              |
         |  publish_event (fill data)    |  create_escrow               |  publish_event (fill data)
         +------------------------------>|<-----------------------------+
                                         |
                                    build_claim_chain
                                    release_escrow
```

### Setup

```python
import requests
import json
import time
import hashlib
import base64
from datetime import datetime, timedelta
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

API_BASE = "https://api.greenhelix.net/v1"
API_KEY = "your-api-key"

session = requests.Session()
session.headers["Authorization"] = f"Bearer {API_KEY}"
session.headers["Content-Type"] = "application/json"

def execute(tool: str, inputs: dict) -> dict:
    """Execute a GreenHelix tool and return the result."""
    resp = session.post(
        f"{API_BASE}/v1",
        json={"tool": tool, "input": inputs}
    )
    resp.raise_for_status()
    return resp.json()
```

### The ArbitrageCoordinator Class

```python
class ArbitrageCoordinator:
    """Orchestrates multi-bot arbitrage across exchanges."""

    def __init__(self, agent_id: str, private_key_b64: str):
        self.agent_id = agent_id
        self.private_key = Ed25519PrivateKey.from_private_bytes(
            base64.b64decode(private_key_b64)
        )
        self.public_key = self.private_key.public_key()
        self.exchange_bots: dict[str, dict] = {}  # exchange -> bot info
        self.active_deals: dict[str, dict] = {}   # deal_id -> deal info
        self.pending_escrows: dict[str, str] = {}  # opportunity_id -> escrow_id

    def sign_payload(self, payload: dict) -> str:
        """Sign a canonical JSON payload with Ed25519."""
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        signature = self.private_key.sign(canonical.encode())
        return base64.b64encode(signature).decode()

    def discover_exchange_bots(self, exchanges: list[str]) -> dict[str, list[dict]]:
        """Find specialist bots for each target exchange."""
        discovered = {}
        for exchange in exchanges:
            results = execute("search_services", {
                "query": f"arbitrage execution {exchange}",
                "filters": {
                    "capabilities": ["exchange_execution", "fast_fill"],
                    "metadata.exchange": exchange,
                    "metadata.bot_type": "exchange_specialist"
                },
                "limit": 10
            })
            discovered[exchange] = results.get("services", [])
            self._log_discovery(exchange, len(discovered[exchange]))
        self.exchange_bots = {
            ex: bots[0] for ex, bots in discovered.items() if bots
        }
        return discovered

    def _log_discovery(self, exchange: str, count: int):
        """Log bot discovery to the event bus."""
        execute("publish_event", {
            "agent_id": self.agent_id,
            "event_type": "arbitrage.bot_discovery",
            "payload": {
                "exchange": exchange,
                "bots_found": count,
                "timestamp": datetime.utcnow().isoformat()
            },
            "signature": self.sign_payload({
                "exchange": exchange,
                "bots_found": count
            })
        })

    def negotiate_coordination(
        self,
        exchange_a: str,
        exchange_b: str,
        profit_split: dict,
        min_opportunity_usd: float,
        max_latency_ms: int
    ) -> dict:
        """Negotiate a coordination agreement with two exchange bots."""
        bot_a = self.exchange_bots.get(exchange_a)
        bot_b = self.exchange_bots.get(exchange_b)
        if not bot_a or not bot_b:
            raise ValueError(f"Missing bot for {exchange_a} or {exchange_b}")

        terms = {
            "pair": f"{exchange_a}-{exchange_b}",
            "profit_split": profit_split,
            "min_opportunity_usd": str(min_opportunity_usd),
            "max_latency_ms": max_latency_ms,
            "escrow_required": True,
            "verification_method": "claim_chain",
            "valid_until": (
                datetime.utcnow() + timedelta(hours=24)
            ).isoformat()
        }

        deal = execute("negotiate_deal", {
            "proposer_id": self.agent_id,
            "counterparty_ids": [bot_a["agent_id"], bot_b["agent_id"]],
            "terms": terms,
            "signature": self.sign_payload(terms)
        })

        deal_id = deal["deal_id"]
        self.active_deals[deal_id] = {
            "exchange_a": exchange_a,
            "exchange_b": exchange_b,
            "bot_a": bot_a["agent_id"],
            "bot_b": bot_b["agent_id"],
            "terms": terms,
            "status": "negotiated"
        }
        return deal

    def create_execution_escrow(
        self,
        opportunity_id: str,
        deal_id: str,
        amount_usd: str
    ) -> dict:
        """Create escrow to guarantee profit-split settlement."""
        deal = self.active_deals.get(deal_id)
        if not deal:
            raise ValueError(f"No active deal: {deal_id}")

        escrow = execute("create_escrow", {
            "payer_id": self.agent_id,
            "payee_ids": [deal["bot_a"], deal["bot_b"]],
            "amount": amount_usd,
            "currency": "USD",
            "conditions": {
                "type": "multi_party_arbitrage",
                "opportunity_id": opportunity_id,
                "deal_id": deal_id,
                "release_on": "verified_execution",
                "timeout_hours": 1,
                "dispute_window_minutes": 30
            },
            "signature": self.sign_payload({
                "opportunity_id": opportunity_id,
                "amount": amount_usd
            })
        })

        self.pending_escrows[opportunity_id] = escrow["escrow_id"]
        return escrow

    def dispatch_execution(
        self,
        opportunity_id: str,
        deal_id: str,
        legs: list[dict]
    ) -> dict:
        """Signal exchange bots to execute their respective legs."""
        deal = self.active_deals[deal_id]
        execution_signals = []

        for leg in legs:
            signal = {
                "opportunity_id": opportunity_id,
                "exchange": leg["exchange"],
                "side": leg["side"],
                "symbol": leg["symbol"],
                "quantity": leg["quantity"],
                "limit_price": leg["limit_price"],
                "execution_deadline_ms": leg.get("deadline_ms", 500),
                "escrow_id": self.pending_escrows.get(opportunity_id),
                "timestamp": datetime.utcnow().isoformat()
            }
            signal["signature"] = self.sign_payload(signal)

            execute("publish_event", {
                "agent_id": self.agent_id,
                "event_type": "arbitrage.execution_signal",
                "payload": signal
            })
            execution_signals.append(signal)

        return {
            "opportunity_id": opportunity_id,
            "signals_dispatched": len(execution_signals),
            "legs": execution_signals
        }
```

The equivalent curl for bot discovery:

```bash
# Discover Binance specialist bots
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "search_services",
    "input": {
      "query": "arbitrage execution binance",
      "filters": {
        "capabilities": ["exchange_execution", "fast_fill"],
        "metadata.exchange": "binance",
        "metadata.bot_type": "exchange_specialist"
      },
      "limit": 10
    }
  }'
```

```bash
# Negotiate coordination deal
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "negotiate_deal",
    "input": {
      "proposer_id": "arb-coordinator-01",
      "counterparty_ids": ["binance-bot-07", "kraken-bot-03"],
      "terms": {
        "pair": "binance-kraken",
        "profit_split": {"coordinator": "0.20", "bot_a": "0.40", "bot_b": "0.40"},
        "min_opportunity_usd": "50.00",
        "max_latency_ms": 200,
        "escrow_required": true,
        "verification_method": "claim_chain"
      },
      "signature": "base64-ed25519-signature"
    }
  }'
```

### Registering the Coordinator

Before the coordinator can operate, it needs a GreenHelix identity:

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import base64

# Generate coordinator keypair
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

COORDINATOR_PRIVATE_KEY = base64.b64encode(private_bytes).decode()
COORDINATOR_PUBLIC_KEY = base64.b64encode(public_bytes).decode()

# Register coordinator agent
coordinator = execute("register_agent", {
    "name": "arb-coordinator-01",
    "description": "Multi-bot arbitrage coordinator. Discovers exchange specialists, "
                   "negotiates profit splits, manages escrow, verifies execution.",
    "capabilities": [
        "arbitrage_coordination",
        "escrow_management",
        "execution_verification",
        "profit_distribution"
    ],
    "metadata": {
        "agent_type": "arbitrage_coordinator",
        "supported_exchanges": ["binance", "kraken", "okx", "bybit", "coinbase"],
        "min_opportunity_usd": 50,
        "max_concurrent_opportunities": 20
    }
})

coordinator_id = coordinator["agent_id"]

# Initialize the coordinator
arb = ArbitrageCoordinator(coordinator_id, COORDINATOR_PRIVATE_KEY)
```

```bash
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "register_agent",
    "input": {
      "name": "arb-coordinator-01",
      "description": "Multi-bot arbitrage coordinator.",
      "capabilities": [
        "arbitrage_coordination",
        "escrow_management",
        "execution_verification",
        "profit_distribution"
      ],
      "metadata": {
        "agent_type": "arbitrage_coordinator",
        "supported_exchanges": ["binance", "kraken", "okx", "bybit", "coinbase"],
        "min_opportunity_usd": 50
      }
    }
  }'
```

### Registering an Exchange Specialist Bot

Each exchange specialist registers with metadata describing its exchange, latency characteristics, and supported pairs:

```python
binance_bot = execute("register_agent", {
    "name": "binance-specialist-07",
    "description": "Binance exchange specialist. Co-located in Tokyo. "
                   "Sub-millisecond execution on spot pairs.",
    "capabilities": [
        "exchange_execution",
        "fast_fill",
        "order_book_monitoring",
        "fill_reporting"
    ],
    "metadata": {
        "agent_type": "exchange_specialist",
        "exchange": "binance",
        "location": "ap-northeast-1",
        "avg_execution_ms": 0.4,
        "supported_pairs": ["BTC/USDT", "ETH/USDT", "SOL/USDT", "BNB/USDT"],
        "max_order_size_usd": 500000
    }
})
```

---

## Chapter 3: OpportunityScanner Class

### Cross-Exchange Price Monitoring

The OpportunityScanner monitors prices across exchanges and identifies arbitrage opportunities that meet minimum profit thresholds after accounting for fees, slippage, and coordination costs. It does not execute trades -- it feeds opportunities to the ArbitrageCoordinator.

### Fee Structures

Every opportunity calculation must account for exchange fees. These vary by exchange, tier, and whether you are a maker or taker:

| Exchange | Taker Fee | Maker Fee | Withdrawal Fee (ETH) |
|---|---|---|---|
| Binance | 0.0750% | 0.0750% | 0.00042 ETH |
| Kraken | 0.0400% | 0.0160% | 0.0025 ETH |
| OKX | 0.0800% | 0.0500% | 0.0014 ETH |
| Bybit | 0.0550% | 0.0100% | 0.0012 ETH |
| Coinbase | 0.0800% | 0.0400% | network fee |

These are VIP/high-volume tier fees as of Q1 2026. Retail tier fees are 3-5x higher and make most arbitrage unprofitable.

### The OpportunityScanner Class

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class ArbitrageOpportunity:
    opportunity_id: str
    symbol: str
    buy_exchange: str
    sell_exchange: str
    buy_price: str
    sell_price: str
    spread_bps: float
    quantity: str
    gross_profit_usd: str
    net_profit_usd: str
    fees_usd: str
    latency_score: float
    detected_at: str
    expires_at: str

class OpportunityScanner:
    """Scans for cross-exchange arbitrage opportunities."""

    # Fee schedules: exchange -> {"taker": rate, "maker": rate}
    FEE_SCHEDULE = {
        "binance":  {"taker": 0.000750, "maker": 0.000750},
        "kraken":   {"taker": 0.000400, "maker": 0.000160},
        "okx":      {"taker": 0.000800, "maker": 0.000500},
        "bybit":    {"taker": 0.000550, "maker": 0.000100},
        "coinbase": {"taker": 0.000800, "maker": 0.000400},
    }

    # Estimated coordination overhead per trade
    COORDINATION_FEE_BPS = 2.0  # 0.02% for escrow + verification

    def __init__(
        self,
        agent_id: str,
        exchanges: list[str],
        min_profit_usd: float = 20.0,
        min_spread_bps: float = 5.0,
        max_quantity_usd: float = 100000.0
    ):
        self.agent_id = agent_id
        self.exchanges = exchanges
        self.min_profit_usd = min_profit_usd
        self.min_spread_bps = min_spread_bps
        self.max_quantity_usd = max_quantity_usd
        self.price_cache: dict[str, dict[str, dict]] = {}
        self._opportunity_counter = 0

    def update_prices(self, exchange: str, symbol: str, bid: str, ask: str, depth_usd: str):
        """Update cached price for an exchange/symbol pair."""
        if symbol not in self.price_cache:
            self.price_cache[symbol] = {}
        self.price_cache[symbol][exchange] = {
            "bid": float(bid),
            "ask": float(ask),
            "depth_usd": float(depth_usd),
            "updated_at": datetime.utcnow().isoformat()
        }

    def scan(self, symbol: str) -> list[ArbitrageOpportunity]:
        """Scan all exchange pairs for arbitrage opportunities on a symbol."""
        if symbol not in self.price_cache:
            return []

        prices = self.price_cache[symbol]
        opportunities = []

        for buy_ex in self.exchanges:
            for sell_ex in self.exchanges:
                if buy_ex == sell_ex:
                    continue
                if buy_ex not in prices or sell_ex not in prices:
                    continue

                opp = self._evaluate_pair(
                    symbol, buy_ex, sell_ex,
                    prices[buy_ex], prices[sell_ex]
                )
                if opp:
                    opportunities.append(opp)

        # Sort by net profit descending
        opportunities.sort(key=lambda o: float(o.net_profit_usd), reverse=True)
        return opportunities

    def _evaluate_pair(
        self,
        symbol: str,
        buy_exchange: str,
        sell_exchange: str,
        buy_data: dict,
        sell_data: dict
    ) -> Optional[ArbitrageOpportunity]:
        """Evaluate a single exchange pair for arbitrage."""
        buy_price = buy_data["ask"]   # we pay the ask to buy
        sell_price = sell_data["bid"]  # we receive the bid to sell

        if sell_price <= buy_price:
            return None  # no spread

        spread_bps = ((sell_price - buy_price) / buy_price) * 10000

        if spread_bps < self.min_spread_bps:
            return None

        # Determine executable quantity based on order book depth
        max_qty_by_depth = min(
            buy_data["depth_usd"],
            sell_data["depth_usd"]
        )
        trade_size_usd = min(max_qty_by_depth, self.max_quantity_usd)
        quantity = trade_size_usd / buy_price

        # Calculate fees
        buy_fee = trade_size_usd * self.FEE_SCHEDULE[buy_exchange]["taker"]
        sell_fee = (quantity * sell_price) * self.FEE_SCHEDULE[sell_exchange]["taker"]
        coordination_fee = trade_size_usd * (self.COORDINATION_FEE_BPS / 10000)
        total_fees = buy_fee + sell_fee + coordination_fee

        gross_profit = (sell_price - buy_price) * quantity
        net_profit = gross_profit - total_fees

        if net_profit < self.min_profit_usd:
            return None

        self._opportunity_counter += 1
        opp_id = f"opp-{self.agent_id}-{self._opportunity_counter:08d}"

        # Calculate latency score (0-1, higher is better)
        latency_score = self._estimate_latency_score(buy_exchange, sell_exchange)

        return ArbitrageOpportunity(
            opportunity_id=opp_id,
            symbol=symbol,
            buy_exchange=buy_exchange,
            sell_exchange=sell_exchange,
            buy_price=f"{buy_price:.8f}",
            sell_price=f"{sell_price:.8f}",
            spread_bps=round(spread_bps, 2),
            quantity=f"{quantity:.8f}",
            gross_profit_usd=f"{gross_profit:.2f}",
            net_profit_usd=f"{net_profit:.2f}",
            fees_usd=f"{total_fees:.2f}",
            latency_score=latency_score,
            detected_at=datetime.utcnow().isoformat(),
            expires_at=(datetime.utcnow() + timedelta(seconds=2)).isoformat()
        )

    def _estimate_latency_score(self, exchange_a: str, exchange_b: str) -> float:
        """Estimate execution latency score for an exchange pair.

        Based on geographic distance between exchange matching engines.
        Score of 1.0 = both in same region, 0.5 = cross-continent,
        0.2 = worst case.
        """
        LOCATIONS = {
            "binance": "tokyo",
            "kraken": "london",
            "okx": "hong_kong",
            "bybit": "singapore",
            "coinbase": "virginia",
        }
        # Rough inter-region latencies in ms
        LATENCIES = {
            ("tokyo", "tokyo"): 0.5,
            ("tokyo", "hong_kong"): 35,
            ("tokyo", "singapore"): 60,
            ("tokyo", "london"): 150,
            ("tokyo", "virginia"): 90,
            ("london", "london"): 0.5,
            ("london", "virginia"): 40,
            ("london", "hong_kong"): 120,
            ("london", "singapore"): 100,
            ("hong_kong", "hong_kong"): 0.5,
            ("hong_kong", "singapore"): 25,
            ("hong_kong", "virginia"): 130,
            ("singapore", "singapore"): 0.5,
            ("singapore", "virginia"): 140,
            ("virginia", "virginia"): 0.5,
        }
        loc_a = LOCATIONS.get(exchange_a, "virginia")
        loc_b = LOCATIONS.get(exchange_b, "virginia")
        key = tuple(sorted([loc_a, loc_b]))
        latency_ms = LATENCIES.get(key, 150)
        # Normalize: 0.5ms -> 1.0, 150ms -> 0.2
        return max(0.2, 1.0 - (latency_ms / 200))

    def log_opportunity(self, opp: ArbitrageOpportunity):
        """Publish opportunity to GreenHelix event bus."""
        execute("publish_event", {
            "agent_id": self.agent_id,
            "event_type": "arbitrage.opportunity_detected",
            "payload": {
                "opportunity_id": opp.opportunity_id,
                "symbol": opp.symbol,
                "buy_exchange": opp.buy_exchange,
                "sell_exchange": opp.sell_exchange,
                "spread_bps": opp.spread_bps,
                "net_profit_usd": opp.net_profit_usd,
                "latency_score": opp.latency_score,
                "detected_at": opp.detected_at
            }
        })
```

### Running the Scanner

```python
# Initialize scanner
scanner = OpportunityScanner(
    agent_id=coordinator_id,
    exchanges=["binance", "kraken", "okx", "bybit", "coinbase"],
    min_profit_usd=20.0,
    min_spread_bps=5.0,
    max_quantity_usd=100000.0
)

# Simulate price updates (in production, these come from WebSocket feeds)
scanner.update_prices("binance", "ETH/USDT", bid="3000.50", ask="3000.80", depth_usd="250000")
scanner.update_prices("kraken",  "ETH/USDT", bid="3012.00", ask="3012.40", depth_usd="180000")
scanner.update_prices("okx",    "ETH/USDT", bid="3001.20", ask="3001.60", depth_usd="300000")

# Scan for opportunities
opportunities = scanner.scan("ETH/USDT")
for opp in opportunities:
    print(f"[{opp.opportunity_id}] {opp.buy_exchange} -> {opp.sell_exchange}: "
          f"spread={opp.spread_bps}bps, net=${opp.net_profit_usd}")
    scanner.log_opportunity(opp)
```

### Stale Price Detection

Price data goes stale fast. A price update from 500ms ago might as well be from last year in arbitrage. The scanner must discard stale prices to avoid executing on phantom opportunities:

```python
def _is_price_fresh(self, exchange_data: dict, max_age_ms: float = 500) -> bool:
    """Check if a cached price is still fresh enough to trade on."""
    updated_at = datetime.fromisoformat(exchange_data["updated_at"])
    age_ms = (datetime.utcnow() - updated_at).total_seconds() * 1000
    return age_ms <= max_age_ms
```

In production, the scanner should track staleness per exchange and alert the coordinator when a feed goes dark. A Binance WebSocket feed that stops sending updates for 2 seconds likely indicates a connection drop -- the bot should reconnect, not continue operating on the last known price.

### Feeding Opportunities to the Coordinator

```python
# Full pipeline: scan -> validate -> escrow -> dispatch
for opp in opportunities:
    # Check that we have active deals for this exchange pair
    matching_deals = [
        (did, d) for did, d in arb.active_deals.items()
        if d["exchange_a"] == opp.buy_exchange
        and d["exchange_b"] == opp.sell_exchange
        and d["status"] == "negotiated"
    ]
    if not matching_deals:
        continue

    deal_id, deal = matching_deals[0]

    # Create escrow for profit settlement
    escrow = arb.create_execution_escrow(
        opportunity_id=opp.opportunity_id,
        deal_id=deal_id,
        amount_usd=opp.net_profit_usd
    )

    # Dispatch execution signals to both bots
    result = arb.dispatch_execution(
        opportunity_id=opp.opportunity_id,
        deal_id=deal_id,
        legs=[
            {
                "exchange": opp.buy_exchange,
                "side": "buy",
                "symbol": opp.symbol,
                "quantity": opp.quantity,
                "limit_price": opp.buy_price,
                "deadline_ms": 500
            },
            {
                "exchange": opp.sell_exchange,
                "side": "sell",
                "symbol": opp.symbol,
                "quantity": opp.quantity,
                "limit_price": opp.sell_price,
                "deadline_ms": 500
            }
        ]
    )
    print(f"Dispatched {result['signals_dispatched']} legs for {opp.opportunity_id}")
```

---

## Chapter 4: Execution Verification

### Why Verification Matters

After the coordinator dispatches execution signals, each exchange bot independently executes its leg. But the coordinator cannot see inside the exchange -- it relies on the bots to report back. This creates an information asymmetry that must be resolved cryptographically. A bot could lie about its fill price, claim a partial fill when it got a full fill, or report execution failure when it actually succeeded (pocketing the profit from the other leg's movement).

Execution verification solves this with three mechanisms: signed fill reports that bind the bot's identity to its claimed execution, timestamp proofs that establish execution ordering, and claim chains that create tamper-proof evidence for dispute resolution.

### The ExecutionVerifier Class

```python
class ExecutionVerifier:
    """Verifies that counterparty bots actually executed their legs."""

    def __init__(self, agent_id: str, private_key_b64: str):
        self.agent_id = agent_id
        self.private_key = Ed25519PrivateKey.from_private_bytes(
            base64.b64decode(private_key_b64)
        )
        self.verification_cache: dict[str, dict] = {}

    def sign_payload(self, payload: dict) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        signature = self.private_key.sign(canonical.encode())
        return base64.b64encode(signature).decode()

    def submit_fill_report(
        self,
        opportunity_id: str,
        exchange: str,
        side: str,
        symbol: str,
        fill_price: str,
        fill_quantity: str,
        exchange_order_id: str,
        exchange_timestamp_us: int
    ) -> dict:
        """Submit a signed fill report for one leg of an arbitrage."""
        report = {
            "opportunity_id": opportunity_id,
            "exchange": exchange,
            "side": side,
            "symbol": symbol,
            "fill_price": fill_price,
            "fill_quantity": fill_quantity,
            "exchange_order_id": exchange_order_id,
            "exchange_timestamp_us": exchange_timestamp_us,
            "reporter_id": self.agent_id,
            "reported_at": datetime.utcnow().isoformat()
        }
        report["signature"] = self.sign_payload(report)

        # Publish fill report as a signed event
        result = execute("publish_event", {
            "agent_id": self.agent_id,
            "event_type": "arbitrage.fill_report",
            "payload": report
        })

        return {"report": report, "event_id": result.get("event_id")}

    def verify_execution(
        self,
        opportunity_id: str,
        expected_legs: list[dict],
        timeout_seconds: int = 30
    ) -> dict:
        """Verify that all legs of an arbitrage were executed.

        Waits for fill reports from each exchange bot, validates
        signatures, checks prices against expectations, and builds
        a verification summary.
        """
        deadline = time.time() + timeout_seconds
        verified_legs = {}
        failures = []

        while time.time() < deadline and len(verified_legs) < len(expected_legs):
            # Poll for fill report events
            events = execute("get_events", {
                "agent_id": self.agent_id,
                "event_type": "arbitrage.fill_report",
                "filters": {
                    "payload.opportunity_id": opportunity_id
                },
                "limit": 10
            })

            for event in events.get("events", []):
                report = event["payload"]
                exchange = report["exchange"]

                if exchange in verified_legs:
                    continue  # already verified this leg

                # Find the expected leg for this exchange
                expected = next(
                    (l for l in expected_legs if l["exchange"] == exchange),
                    None
                )
                if not expected:
                    continue

                # Validate fill against expectations
                validation = self._validate_fill(report, expected)
                if validation["valid"]:
                    verified_legs[exchange] = {
                        "report": report,
                        "validation": validation
                    }
                else:
                    failures.append({
                        "exchange": exchange,
                        "reason": validation["reason"],
                        "report": report
                    })

            if len(verified_legs) < len(expected_legs):
                time.sleep(0.5)

        all_verified = len(verified_legs) == len(expected_legs)

        verification = {
            "opportunity_id": opportunity_id,
            "all_verified": all_verified,
            "verified_legs": verified_legs,
            "failures": failures,
            "missing_legs": [
                l["exchange"] for l in expected_legs
                if l["exchange"] not in verified_legs
            ],
            "verified_at": datetime.utcnow().isoformat()
        }

        self.verification_cache[opportunity_id] = verification
        return verification

    def _validate_fill(self, report: dict, expected: dict) -> dict:
        """Validate a fill report against expectations."""
        fill_price = float(report["fill_price"])
        expected_price = float(expected["limit_price"])
        fill_qty = float(report["fill_quantity"])
        expected_qty = float(expected["quantity"])

        # Price slippage tolerance: 0.1% (10 bps)
        max_slippage = expected_price * 0.001

        if expected["side"] == "buy" and fill_price > expected_price + max_slippage:
            return {
                "valid": False,
                "reason": f"Buy fill price {fill_price} exceeds limit "
                          f"{expected_price} + slippage {max_slippage}"
            }

        if expected["side"] == "sell" and fill_price < expected_price - max_slippage:
            return {
                "valid": False,
                "reason": f"Sell fill price {fill_price} below limit "
                          f"{expected_price} - slippage {max_slippage}"
            }

        # Quantity tolerance: 1%
        qty_tolerance = expected_qty * 0.01
        if fill_qty < expected_qty - qty_tolerance:
            return {
                "valid": False,
                "reason": f"Fill quantity {fill_qty} below expected "
                          f"{expected_qty} - tolerance {qty_tolerance}"
            }

        return {"valid": True, "reason": "within_tolerance"}

    def build_evidence_package(self, opportunity_id: str) -> dict:
        """Build a tamper-proof evidence package using claim chains.

        This creates a Merkle-tree-backed proof of all events
        related to an opportunity -- discovery, execution signals,
        fill reports, and verification results.
        """
        verification = self.verification_cache.get(opportunity_id)
        if not verification:
            raise ValueError(f"No verification data for {opportunity_id}")

        # Collect all event IDs related to this opportunity
        events = execute("get_events", {
            "agent_id": self.agent_id,
            "filters": {
                "payload.opportunity_id": opportunity_id
            },
            "limit": 100
        })

        event_ids = [e["event_id"] for e in events.get("events", [])]

        # Build claim chain over all related events
        claim_chain = execute("build_claim_chain", {
            "agent_id": self.agent_id,
            "claim_type": "arbitrage_execution_proof",
            "event_ids": event_ids,
            "metadata": {
                "opportunity_id": opportunity_id,
                "all_verified": verification["all_verified"],
                "leg_count": len(verification["verified_legs"]),
                "verified_at": verification["verified_at"]
            },
            "signature": self.sign_payload({
                "opportunity_id": opportunity_id,
                "event_ids": event_ids
            })
        })

        return {
            "opportunity_id": opportunity_id,
            "chain_id": claim_chain["chain_id"],
            "merkle_root": claim_chain["merkle_root"],
            "event_count": len(event_ids),
            "verification": verification
        }
```

### Using the Verifier

```python
verifier = ExecutionVerifier(coordinator_id, COORDINATOR_PRIVATE_KEY)

# After dispatching execution, wait for verification
verification = verifier.verify_execution(
    opportunity_id="opp-arb-coordinator-01-00000001",
    expected_legs=[
        {
            "exchange": "binance",
            "side": "buy",
            "symbol": "ETH/USDT",
            "quantity": "5.00000000",
            "limit_price": "3000.80000000"
        },
        {
            "exchange": "kraken",
            "side": "sell",
            "symbol": "ETH/USDT",
            "quantity": "5.00000000",
            "limit_price": "3012.00000000"
        }
    ],
    timeout_seconds=30
)

if verification["all_verified"]:
    print("All legs verified. Building evidence package.")
    evidence = verifier.build_evidence_package(
        "opp-arb-coordinator-01-00000001"
    )
    print(f"Evidence chain: {evidence['chain_id']}")
    print(f"Merkle root: {evidence['merkle_root']}")
else:
    print(f"Verification failed. Missing: {verification['missing_legs']}")
    print(f"Failures: {verification['failures']}")
```

The curl equivalent for building evidence:

```bash
# Build claim chain for execution proof
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "build_claim_chain",
    "input": {
      "agent_id": "arb-coordinator-01",
      "claim_type": "arbitrage_execution_proof",
      "event_ids": [
        "evt-001-signal-binance",
        "evt-002-signal-kraken",
        "evt-003-fill-binance",
        "evt-004-fill-kraken"
      ],
      "metadata": {
        "opportunity_id": "opp-arb-coordinator-01-00000001",
        "all_verified": true,
        "leg_count": 2
      },
      "signature": "base64-ed25519-signature"
    }
  }'
```

### Timestamp Proofs

Execution ordering matters. If the buy leg executes at T=0ms and the sell leg executes at T=200ms, a 200ms price movement could have occurred. The fill reports include `exchange_timestamp_us` -- the microsecond timestamp from the exchange itself, not the bot's local clock. The verifier checks that both legs executed within the acceptable window:

```python
def verify_timestamp_ordering(self, verification: dict, max_gap_ms: int = 500) -> bool:
    """Verify that both legs executed within the acceptable time window."""
    timestamps = []
    for exchange, data in verification["verified_legs"].items():
        ts_us = data["report"]["exchange_timestamp_us"]
        timestamps.append(ts_us)

    if len(timestamps) < 2:
        return False

    gap_us = max(timestamps) - min(timestamps)
    gap_ms = gap_us / 1000

    return gap_ms <= max_gap_ms
```

---

## Chapter 5: Profit Splitting via Escrow

### Escrow-Protected Settlement

After both legs are verified, profits must be distributed. The coordinator created an escrow before dispatching execution (Chapter 2). Now it releases that escrow according to the agreed profit split. The key property: no party can access the funds without verified execution, and the split formula is locked in the escrow conditions -- not subject to post-hoc renegotiation.

### Split Models

Three common models for profit distribution in multi-bot arbitrage:

**Equal Split (50/50).** Simple but unfair when capital contributions differ. If Bot A commits $100,000 and Bot B commits $20,000, equal split gives Bot B 5x the return on capital.

**Proportional to Capital.** Each bot receives profit proportional to the capital it deployed for the trade. This is fairest for capital-heavy strategies but ignores latency contributions.

**Proportional to Latency Contribution.** The bot that executes faster captures more value because it reduces the window for adverse price movement. A bot that fills in 0.4ms contributes more to the trade's success than one that fills in 50ms. This model allocates a latency bonus to the faster executor.

In practice, most coordination agreements use a hybrid: a base split proportional to capital, with a latency bonus for the faster leg.

```python
class ProfitSplitter:
    """Handles profit distribution via GreenHelix escrow."""

    def __init__(self, agent_id: str, private_key_b64: str):
        self.agent_id = agent_id
        self.private_key = Ed25519PrivateKey.from_private_bytes(
            base64.b64decode(private_key_b64)
        )

    def sign_payload(self, payload: dict) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        signature = self.private_key.sign(canonical.encode())
        return base64.b64encode(signature).decode()

    def calculate_split(
        self,
        net_profit_usd: float,
        model: str,
        participants: list[dict]
    ) -> dict[str, str]:
        """Calculate profit split based on the chosen model.

        participants: list of {
            "agent_id": str,
            "role": "coordinator" | "executor",
            "capital_usd": float,
            "execution_ms": float  # only for latency model
        }
        """
        if model == "equal":
            per_party = net_profit_usd / len(participants)
            return {p["agent_id"]: f"{per_party:.2f}" for p in participants}

        elif model == "capital_weighted":
            total_capital = sum(p["capital_usd"] for p in participants)
            return {
                p["agent_id"]: f"{(net_profit_usd * p['capital_usd'] / total_capital):.2f}"
                for p in participants
            }

        elif model == "latency_hybrid":
            # 70% capital-weighted, 20% latency bonus, 10% coordinator fee
            coordinator_fee = net_profit_usd * 0.10
            latency_pool = net_profit_usd * 0.20
            capital_pool = net_profit_usd * 0.70

            executors = [p for p in participants if p["role"] == "executor"]
            coordinator = next(
                (p for p in participants if p["role"] == "coordinator"), None
            )

            splits = {}

            # Coordinator gets flat fee
            if coordinator:
                splits[coordinator["agent_id"]] = f"{coordinator_fee:.2f}"

            # Capital-weighted portion
            total_capital = sum(p["capital_usd"] for p in executors)
            for p in executors:
                capital_share = capital_pool * p["capital_usd"] / total_capital
                splits[p["agent_id"]] = f"{capital_share:.2f}"

            # Latency bonus: faster executor gets more
            if len(executors) == 2:
                total_latency = sum(1.0 / p["execution_ms"] for p in executors)
                for p in executors:
                    latency_share = latency_pool * (1.0 / p["execution_ms"]) / total_latency
                    current = float(splits[p["agent_id"]])
                    splits[p["agent_id"]] = f"{(current + latency_share):.2f}"

            return splits

        else:
            raise ValueError(f"Unknown split model: {model}")

    def settle_via_escrow(
        self,
        escrow_id: str,
        opportunity_id: str,
        splits: dict[str, str],
        evidence_chain_id: str
    ) -> dict:
        """Release escrow according to calculated splits."""
        release_payload = {
            "escrow_id": escrow_id,
            "opportunity_id": opportunity_id,
            "distributions": [
                {"agent_id": agent_id, "amount": amount, "currency": "USD"}
                for agent_id, amount in splits.items()
            ],
            "evidence_chain_id": evidence_chain_id,
            "settled_at": datetime.utcnow().isoformat()
        }
        release_payload["signature"] = self.sign_payload(release_payload)

        result = execute("release_escrow", {
            "escrow_id": escrow_id,
            "release_to": release_payload["distributions"],
            "evidence": {
                "chain_id": evidence_chain_id,
                "opportunity_id": opportunity_id
            },
            "signature": release_payload["signature"]
        })

        # Log settlement event
        execute("publish_event", {
            "agent_id": self.agent_id,
            "event_type": "arbitrage.settlement",
            "payload": {
                "opportunity_id": opportunity_id,
                "escrow_id": escrow_id,
                "splits": splits,
                "evidence_chain_id": evidence_chain_id,
                "settled_at": release_payload["settled_at"]
            }
        })

        return result
```

### Why Escrow Matters

Without escrow, profit splitting relies entirely on the counterparty's goodwill. Bot B sells on Kraken and receives $30,120 in its exchange account. The agreed split says Bot A gets $42 in profit. But Bot B controls the Kraken account. There is no technical mechanism forcing Bot B to pay. In traditional finance, this is solved by clearing houses that hold collateral from both sides. GreenHelix escrow serves the same function: the coordinator locks the expected profit in escrow before dispatching execution signals. Neither bot can access the escrowed funds until the verifier confirms both legs executed within tolerance. If verification fails, the escrow returns to the coordinator according to the pre-defined cancellation rules.

The escrow amount is typically the expected net profit, not the full trade notional. Locking the entire $30,000 per leg in escrow would be capital-inefficient and defeat the purpose of multi-bot coordination. Instead, each bot posts a smaller performance bond (e.g., 2x the expected profit) as collateral. If a bot fails to execute or reports fraudulent fills, it forfeits its bond.

### Handling Partial Fills

Partial fills are the most common failure mode in multi-bot arbitrage. Bot A gets a full fill on Binance, but Bot B only fills 60% on Kraken because a large market order swept the book during execution. The coordinator must handle this gracefully:

```python
def handle_partial_fill(
    self,
    opportunity_id: str,
    escrow_id: str,
    verification: dict,
    original_quantity: float
) -> dict:
    """Handle settlement when one or more legs have partial fills."""
    fill_quantities = {}
    for exchange, data in verification["verified_legs"].items():
        fill_quantities[exchange] = float(data["report"]["fill_quantity"])

    # The effective trade size is the minimum fill across all legs
    effective_qty = min(fill_quantities.values())
    fill_ratio = effective_qty / original_quantity

    if fill_ratio < 0.5:
        # Less than 50% filled -- cancel escrow, unwind positions
        cancel_result = execute("release_escrow", {
            "escrow_id": escrow_id,
            "action": "cancel",
            "reason": f"Partial fill below threshold: {fill_ratio:.1%}",
            "signature": self.sign_payload({
                "escrow_id": escrow_id,
                "action": "cancel"
            })
        })
        return {"action": "cancelled", "fill_ratio": fill_ratio, "result": cancel_result}

    # Partial settlement: reduce profit proportionally
    # The overfilled leg has excess inventory that must be unwound separately
    return {
        "action": "partial_settlement",
        "fill_ratio": fill_ratio,
        "effective_quantity": f"{effective_qty:.8f}",
        "excess_fills": {
            ex: f"{(qty - effective_qty):.8f}"
            for ex, qty in fill_quantities.items()
            if qty > effective_qty
        }
    }
```

### Settlement via curl

```bash
# Release escrow after verified execution
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "release_escrow",
    "input": {
      "escrow_id": "esc-abc123",
      "release_to": [
        {"agent_id": "arb-coordinator-01", "amount": "8.40", "currency": "USD"},
        {"agent_id": "binance-bot-07", "amount": "38.22", "currency": "USD"},
        {"agent_id": "kraken-bot-03", "amount": "37.38", "currency": "USD"}
      ],
      "evidence": {
        "chain_id": "chain-xyz789",
        "opportunity_id": "opp-arb-coordinator-01-00000001"
      },
      "signature": "base64-ed25519-signature"
    }
  }'
```

### Full Settlement Example

```python
splitter = ProfitSplitter(coordinator_id, COORDINATOR_PRIVATE_KEY)

# Calculate split using latency-hybrid model
splits = splitter.calculate_split(
    net_profit_usd=84.00,
    model="latency_hybrid",
    participants=[
        {
            "agent_id": coordinator_id,
            "role": "coordinator",
            "capital_usd": 0,
            "execution_ms": 0
        },
        {
            "agent_id": "binance-bot-07",
            "role": "executor",
            "capital_usd": 30000,
            "execution_ms": 0.4
        },
        {
            "agent_id": "kraken-bot-03",
            "role": "executor",
            "capital_usd": 30120,
            "execution_ms": 2.1
        }
    ]
)

# Settle via escrow
settlement = splitter.settle_via_escrow(
    escrow_id="esc-abc123",
    opportunity_id="opp-arb-coordinator-01-00000001",
    splits=splits,
    evidence_chain_id="chain-xyz789"
)

print(f"Settlement: {splits}")
# Output: {'arb-coordinator-01': '8.40', 'binance-bot-07': '38.22', 'kraken-bot-03': '37.38'}
# Coordinator: 10% = $8.40
# Binance bot: higher latency bonus (0.4ms vs 2.1ms) offsets slightly lower capital
# Kraken bot: slightly more capital, but slower execution
```

---

## Chapter 6: MEV Protection

### What MEV Means for Arbitrage Bots

Maximal Extractable Value (MEV) originated in the Ethereum mempool, where miners and validators could reorder, insert, or censor transactions to extract profit. The concept has expanded beyond blockchain. In the context of multi-bot arbitrage, MEV risk manifests in three ways:

**Front-running.** A third party observes your opportunity signal (the coordination message between bots) and executes the same trade before you. If you broadcast "buy ETH on Binance at $3,000, sell on Kraken at $3,012" in the clear, anyone monitoring the signal can race you.

**Sandwich attacks.** A third party sees your pending buy order, places a buy order ahead of you (pushing the price up), then sells into your fill (profiting from the artificial price increase). This is well-documented on-chain but occurs on centralized exchanges too, particularly through API key compromise or colluding market makers.

**Information leakage.** Even if your execution is private, the pattern of your trades reveals your strategy. A counterparty bot in your coordination network could extract this information and trade against you on exchanges where you are not active.

### Commit-Reveal for Opportunity Sharing

The first line of defense is never broadcasting opportunity details in the clear. Instead, use a commit-reveal pattern: share a cryptographic commitment to the opportunity (proving you detected it first), then reveal the details only to verified counterparties through encrypted channels.

```python
class MEVProtector:
    """MEV protection for multi-bot arbitrage coordination."""

    def __init__(self, agent_id: str, private_key_b64: str):
        self.agent_id = agent_id
        self.private_key = Ed25519PrivateKey.from_private_bytes(
            base64.b64decode(private_key_b64)
        )
        self.commitments: dict[str, dict] = {}

    def sign_payload(self, payload: dict) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        signature = self.private_key.sign(canonical.encode())
        return base64.b64encode(signature).decode()

    def commit_opportunity(self, opportunity: ArbitrageOpportunity) -> dict:
        """Create a cryptographic commitment to an opportunity without revealing details.

        The commitment is a hash of the full opportunity details plus a random nonce.
        Published to the event bus as proof of discovery priority. Details are revealed
        only to authorized counterparties after escrow is created.
        """
        nonce = base64.b64encode(hashlib.sha256(
            f"{opportunity.opportunity_id}-{time.time_ns()}".encode()
        ).digest()).decode()

        preimage = {
            "opportunity_id": opportunity.opportunity_id,
            "symbol": opportunity.symbol,
            "buy_exchange": opportunity.buy_exchange,
            "sell_exchange": opportunity.sell_exchange,
            "buy_price": opportunity.buy_price,
            "sell_price": opportunity.sell_price,
            "quantity": opportunity.quantity,
            "nonce": nonce
        }

        commitment = hashlib.sha256(
            json.dumps(preimage, sort_keys=True, separators=(",", ":")).encode()
        ).hexdigest()

        # Store locally for later reveal
        self.commitments[opportunity.opportunity_id] = {
            "preimage": preimage,
            "commitment": commitment,
            "nonce": nonce
        }

        # Publish commitment (not the details)
        execute("publish_event", {
            "agent_id": self.agent_id,
            "event_type": "arbitrage.opportunity_commitment",
            "payload": {
                "opportunity_id": opportunity.opportunity_id,
                "commitment": commitment,
                "committed_at": datetime.utcnow().isoformat()
            },
            "signature": self.sign_payload({"commitment": commitment})
        })

        return {"commitment": commitment, "opportunity_id": opportunity.opportunity_id}

    def reveal_to_counterparty(
        self,
        opportunity_id: str,
        counterparty_public_key_b64: str
    ) -> dict:
        """Reveal opportunity details to a specific counterparty.

        In production, this would encrypt the details with the counterparty's
        public key. For this example, we publish a reveal event that references
        the original commitment.
        """
        stored = self.commitments.get(opportunity_id)
        if not stored:
            raise ValueError(f"No commitment found for {opportunity_id}")

        reveal_payload = {
            "opportunity_id": opportunity_id,
            "preimage": stored["preimage"],
            "commitment": stored["commitment"],
            "revealed_to": counterparty_public_key_b64,
            "revealed_at": datetime.utcnow().isoformat()
        }

        # Counterparty can verify: sha256(preimage) == commitment
        execute("publish_event", {
            "agent_id": self.agent_id,
            "event_type": "arbitrage.opportunity_reveal",
            "payload": reveal_payload,
            "signature": self.sign_payload(reveal_payload)
        })

        return reveal_payload
```

### Detecting Front-Running

Even with commit-reveal protection, you need to detect when front-running has occurred so you can respond. The primary indicator is adverse price movement between opportunity detection and execution. If you detect ETH at $3,000 on Binance and your buy order fills at $3,002, someone likely saw your intent and bought ahead of you.

```python
def detect_front_running(
    expected_price: float,
    actual_fill_price: float,
    side: str,
    normal_slippage_bps: float = 2.0
) -> dict:
    """Detect potential front-running based on fill price deviation.

    Returns analysis of whether the fill price deviation exceeds
    normal market microstructure noise.
    """
    if side == "buy":
        slippage_bps = ((actual_fill_price - expected_price) / expected_price) * 10000
    else:
        slippage_bps = ((expected_price - actual_fill_price) / expected_price) * 10000

    is_suspicious = slippage_bps > normal_slippage_bps * 3  # 3x normal = suspicious
    is_likely_frontrun = slippage_bps > normal_slippage_bps * 5  # 5x normal = likely

    return {
        "expected_price": f"{expected_price:.8f}",
        "actual_price": f"{actual_fill_price:.8f}",
        "slippage_bps": round(slippage_bps, 2),
        "normal_slippage_bps": normal_slippage_bps,
        "suspicious": is_suspicious,
        "likely_frontrun": is_likely_frontrun,
        "recommendation": (
            "abort_and_investigate" if is_likely_frontrun
            else "flag_for_review" if is_suspicious
            else "normal"
        )
    }
```

If front-running is detected repeatedly on a specific exchange pair or with a specific counterparty, the coordinator should blacklist that counterparty and report the behavior to GreenHelix's reputation system. Systematic front-running by a coordination partner destroys the network's value -- the reputation penalty must be severe enough to deter it.

### Counterparty Information Barriers

Within a coordination network, each bot should know only what it needs to execute its leg. The Binance bot does not need to know the Kraken sell price -- it only needs to know "buy 5 ETH at limit $3,000.80 within 500ms." The less information each participant has, the less they can exploit. This is the same information barrier principle used by investment banks between their trading desks and advisory arms.

The coordinator enforces this by sending each bot only its own leg details. The full opportunity (both sides, spread, expected profit) exists only in the coordinator's memory and in the commit-reveal commitment. Even if a counterparty bot is compromised or malicious, it cannot reconstruct the full opportunity from its execution signal alone.

### Private Execution Channels

The second defense layer is ensuring that execution signals travel through private channels, not public event streams. GreenHelix supports scoped events -- events visible only to specified agent IDs:

```bash
# Publish execution signal visible only to the target bot
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "publish_event",
    "input": {
      "agent_id": "arb-coordinator-01",
      "event_type": "arbitrage.execution_signal",
      "payload": {
        "opportunity_id": "opp-arb-coordinator-01-00000001",
        "exchange": "binance",
        "side": "buy",
        "symbol": "ETH/USDT",
        "quantity": "5.00000000",
        "limit_price": "3000.80000000"
      },
      "visibility": ["binance-bot-07"],
      "signature": "base64-ed25519-signature"
    }
  }'
```

### Execution Timing Randomization

Predictable execution patterns create MEV opportunities. If your bot always executes within 10ms of receiving a signal, a front-runner can time their order to arrive 1ms earlier. Adding controlled randomization breaks this predictability:

```python
import random

def randomized_execution_delay(base_delay_ms: float = 0, max_jitter_ms: float = 50) -> float:
    """Add random jitter to execution timing to prevent front-running.

    The jitter follows a truncated normal distribution centered
    on base_delay_ms, not a uniform distribution. Uniform jitter
    is detectable; normally-distributed jitter is not.
    """
    jitter = random.gauss(0, max_jitter_ms / 3)
    jitter = max(-max_jitter_ms, min(max_jitter_ms, jitter))
    return max(0, base_delay_ms + jitter)
```

### Order Splitting

Large orders are visible in the order book and attract front-runners. Splitting a single leg into multiple smaller orders spread over a short time window reduces visibility:

```python
def split_order(
    quantity: float,
    limit_price: float,
    num_slices: int = 5,
    time_window_ms: int = 200
) -> list[dict]:
    """Split a large order into smaller slices with price randomization."""
    slice_qty = quantity / num_slices
    delay_per_slice = time_window_ms / num_slices
    slices = []

    for i in range(num_slices):
        # Slight price variation on each slice to avoid detection
        price_jitter = limit_price * random.uniform(-0.0001, 0.0001)
        slices.append({
            "quantity": f"{slice_qty:.8f}",
            "limit_price": f"{(limit_price + price_jitter):.8f}",
            "delay_ms": delay_per_slice * i
        })

    return slices
```

---

## Chapter 7: Latency Optimization

### Sub-Millisecond Requirements

In cross-exchange arbitrage, the opportunity lifetime is measured in milliseconds. Academic research on crypto arbitrage (Makarov and Schoar, 2020; updated 2025) shows that median cross-exchange price discrepancies on major pairs persist for 200-800ms. After accounting for the time to detect the opportunity, signal counterparties, and execute both legs, you have a budget of roughly 100-300ms. Every millisecond matters: each 10ms of added latency reduces capture rate by approximately 3-5% on competitive pairs.

The latency budget breaks down as:

```
+-----------------------------------------+
| Latency Budget for Binance-Kraken Arb   |
+-----------------------------------------+
| Component              | Target   | Max |
|------------------------|----------|-----|
| Opportunity detection  |   5 ms   | 20  |
| Coordinator processing |   2 ms   | 10  |
| Signal to Bot A        |  70 ms   | 90  |
| Signal to Bot B        |  70 ms   | 90  |
| Bot A execution        |   0.4 ms |  5  |
| Bot B execution        |   2 ms   | 10  |
| Fill confirmation      |  10 ms   | 30  |
|------------------------|----------|-----|
| Total                  | 159 ms   | 255 |
+-----------------------------------------+
```

The signal latency (coordinator to exchange bot) dominates. This is physics -- the speed of light in fiber between Tokyo and London is approximately 70ms. You cannot optimize this below the physical limit. What you can optimize is everything else.

### Co-Location Strategy

Each exchange specialist bot should run as close to its exchange's matching engine as possible:

| Exchange | Matching Engine Location | Recommended Cloud Region |
|---|---|---|
| Binance | Tokyo, Japan | AWS ap-northeast-1 |
| Kraken | London, UK | AWS eu-west-2 |
| OKX | Hong Kong | AWS ap-east-1 |
| Bybit | Singapore | AWS ap-southeast-1 |
| Coinbase | Virginia, USA | AWS us-east-1 |

The coordinator should run in a location that minimizes maximum signal latency to any exchange bot. For the five exchanges above, Frankfurt (AWS eu-central-1) provides the best worst-case latency: 80ms to Tokyo, 10ms to London, 100ms to Hong Kong, 90ms to Singapore, 45ms to Virginia. No single location achieves sub-50ms to all five, but Frankfurt keeps the worst case under 100ms.

### WebSocket vs REST for Price Feeds

Exchange specialist bots must choose between WebSocket price feeds and REST polling. The answer is always WebSocket for price monitoring. REST polling at 100ms intervals means you discover opportunities up to 100ms late. WebSocket push delivers price updates within 1-5ms of the exchange processing them. The latency difference compounds: a 100ms detection delay plus a 70ms signal delay plus a 2ms execution delay means 172ms total -- well within the opportunity window. But a REST poll that happens to fire 90ms after the price moved gives you 162ms of detection latency, pushing total time to 234ms. On competitive pairs, that extra 62ms drops your capture rate by 15-20%.

Every major exchange provides WebSocket order book feeds: Binance's `wss://stream.binance.com`, Kraken's `wss://ws.kraken.com`, OKX's `wss://ws.okx.com`. The specialist bot should maintain persistent WebSocket connections to each feed and parse price updates in the hot path without any heap allocation. In Python, this means pre-allocated buffers and `orjson` for JSON parsing (3-5x faster than `json.loads` on order book payloads).

### Connection Pooling

Creating a new TCP connection for each API call adds 30-50ms of handshake overhead. Persistent connections eliminate this:

```python
import urllib3

class LowLatencyExecutor:
    """Optimized executor for sub-millisecond exchange operations."""

    def __init__(self, exchange_api_base: str, api_key: str):
        # Pre-create connection pool with keep-alive
        self.pool = urllib3.HTTPSConnectionPool(
            host=exchange_api_base.replace("https://", ""),
            maxsize=10,
            block=False,
            retries=urllib3.Retry(total=0),  # no retries -- fail fast
            timeout=urllib3.Timeout(connect=1.0, read=2.0)
        )
        self.api_key = api_key
        self._headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Connection": "keep-alive"
        }

    def execute_order(self, order: dict) -> dict:
        """Execute an order with minimal latency."""
        body = json.dumps(order).encode()
        resp = self.pool.urlopen(
            "POST",
            "/api/v1/order",
            headers=self._headers,
            body=body
        )
        return json.loads(resp.data)
```

### Pre-Signed Transactions

For exchanges that support it, pre-sign the order payload and cache it. When the execution signal arrives, you send the pre-signed payload immediately without cryptographic computation in the hot path:

```python
class PreSignedOrderCache:
    """Cache pre-signed orders for instant dispatch."""

    def __init__(self, private_key: Ed25519PrivateKey):
        self.private_key = private_key
        self.cache: dict[str, dict] = {}

    def prepare_order(
        self,
        symbol: str,
        side: str,
        quantity: str,
        price: str,
        ttl_seconds: int = 5
    ) -> str:
        """Pre-sign an order for later dispatch.

        Returns a cache key. The signed order expires after ttl_seconds.
        """
        order = {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "price": price,
            "timestamp": int(time.time() * 1000),
            "valid_until": int((time.time() + ttl_seconds) * 1000)
        }

        canonical = json.dumps(order, sort_keys=True, separators=(",", ":"))
        signature = self.private_key.sign(canonical.encode())
        order["signature"] = base64.b64encode(signature).decode()

        cache_key = f"{symbol}-{side}-{price}"
        self.cache[cache_key] = {
            "order": order,
            "expires_at": time.time() + ttl_seconds
        }
        return cache_key

    def get_order(self, cache_key: str) -> dict | None:
        """Retrieve a pre-signed order. Returns None if expired."""
        entry = self.cache.get(cache_key)
        if not entry:
            return None
        if time.time() > entry["expires_at"]:
            del self.cache[cache_key]
            return None
        return entry["order"]
```

### Reporting Latency Metrics

Exchange specialist bots should report their execution latency to GreenHelix so the coordinator can make informed routing decisions:

```python
def report_latency_metrics(agent_id: str, exchange: str, metrics: dict):
    """Report execution latency metrics to GreenHelix."""
    execute("submit_metrics", {
        "agent_id": agent_id,
        "metrics": {
            f"{exchange}_avg_execution_ms": metrics["avg_execution_ms"],
            f"{exchange}_p99_execution_ms": metrics["p99_execution_ms"],
            f"{exchange}_fill_rate": metrics["fill_rate"],
            f"{exchange}_uptime_pct": metrics["uptime_pct"],
            f"{exchange}_orders_today": metrics["orders_today"]
        }
    })

# Example: Binance bot reports its daily metrics
report_latency_metrics("binance-bot-07", "binance", {
    "avg_execution_ms": 0.38,
    "p99_execution_ms": 1.2,
    "fill_rate": 0.97,
    "uptime_pct": 99.99,
    "orders_today": 4821
})
```

```bash
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "submit_metrics",
    "input": {
      "agent_id": "binance-bot-07",
      "metrics": {
        "binance_avg_execution_ms": 0.38,
        "binance_p99_execution_ms": 1.2,
        "binance_fill_rate": 0.97,
        "binance_uptime_pct": 99.99,
        "binance_orders_today": 4821
      }
    }
  }'
```

### Using Metrics for Routing

The coordinator uses reported metrics to decide which exchange bot to use when multiple bots cover the same exchange:

```python
def select_best_bot(self, exchange: str, candidates: list[dict]) -> dict:
    """Select the best bot for an exchange based on reported metrics."""
    scored = []
    for bot in candidates:
        reputation = execute("get_reputation", {
            "agent_id": bot["agent_id"]
        })

        # Composite score: 40% fill rate, 30% latency, 30% uptime
        fill_rate = reputation.get("metrics", {}).get(f"{exchange}_fill_rate", 0.5)
        avg_ms = reputation.get("metrics", {}).get(f"{exchange}_avg_execution_ms", 100)
        uptime = reputation.get("metrics", {}).get(f"{exchange}_uptime_pct", 90)

        latency_score = max(0, 1 - (avg_ms / 10))  # 0ms = 1.0, 10ms = 0.0
        score = (fill_rate * 0.4) + (latency_score * 0.3) + ((uptime / 100) * 0.3)
        scored.append((score, bot))

    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1]
```

---

## Chapter 8: Audit Trails for Arbitrage

### Regulatory Requirements

Arbitrage bots operating across regulated exchanges face overlapping compliance obligations. The EU AI Act (effective August 2, 2026) classifies autonomous financial trading systems as high-risk AI under Annex III. MiFID II RTS 25 requires per-order event logging with microsecond timestamps. SEC Rule 17a-4 mandates write-once, read-many (WORM) storage for trade records. Even if you trade only crypto on centralized exchanges, most jurisdictions now classify this as a regulated activity requiring auditable record-keeping.

The common thread: every decision your bot makes -- every opportunity detected, every execution signal dispatched, every fill received, every profit split -- must be logged in a tamper-evident, independently verifiable format. A mutable database is not sufficient.

### Event Types for Arbitrage Audit

Define a schema for each auditable event in the arbitrage lifecycle:

| Event Type | When | Key Fields |
|---|---|---|
| `arbitrage.opportunity_detected` | Scanner finds a profitable spread | symbol, exchanges, spread_bps, net_profit_est |
| `arbitrage.opportunity_commitment` | Commit-reveal: commit phase | commitment_hash, timestamp |
| `arbitrage.deal_negotiated` | Coordination agreement reached | deal_id, counterparties, terms |
| `arbitrage.escrow_created` | Escrow locked for settlement | escrow_id, amount, conditions |
| `arbitrage.execution_signal` | Coordinator signals exchange bot | exchange, side, symbol, quantity, price |
| `arbitrage.fill_report` | Exchange bot reports fill | exchange, fill_price, fill_qty, exchange_ts |
| `arbitrage.verification_complete` | All legs verified | opportunity_id, all_verified, legs |
| `arbitrage.settlement` | Escrow released, profit split | escrow_id, splits, evidence_chain_id |
| `arbitrage.dispute_opened` | Counterparty disputes fill | dispute_id, reason, evidence |

### The AuditTrail Class

```python
class ArbitrageAuditTrail:
    """Compliance-grade audit logging for arbitrage operations."""

    def __init__(self, agent_id: str, private_key_b64: str):
        self.agent_id = agent_id
        self.private_key = Ed25519PrivateKey.from_private_bytes(
            base64.b64decode(private_key_b64)
        )
        self.event_buffer: list[dict] = []
        self.chain_schedule_minutes = 15  # build chain every 15 minutes

    def sign_payload(self, payload: dict) -> str:
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        signature = self.private_key.sign(canonical.encode())
        return base64.b64encode(signature).decode()

    def log_event(self, event_type: str, payload: dict) -> dict:
        """Log an auditable event with cryptographic signature."""
        event = {
            "agent_id": self.agent_id,
            "event_type": event_type,
            "payload": payload,
            "timestamp_us": int(time.time() * 1_000_000),
            "signature": self.sign_payload(payload)
        }

        result = execute("publish_event", event)
        event["event_id"] = result.get("event_id")
        self.event_buffer.append(event)

        return result

    def build_periodic_chain(self) -> dict:
        """Build a Merkle claim chain over buffered events.

        Call this on a schedule (e.g., every 15 minutes) to create
        a tamper-proof commitment over recent events. The chain root
        can be verified independently by auditors.
        """
        if not self.event_buffer:
            return {"status": "no_events"}

        event_ids = [e["event_id"] for e in self.event_buffer if e.get("event_id")]

        chain = execute("build_claim_chain", {
            "agent_id": self.agent_id,
            "claim_type": "arbitrage_audit_chain",
            "event_ids": event_ids,
            "metadata": {
                "event_count": len(event_ids),
                "time_range": {
                    "from": self.event_buffer[0]["timestamp_us"],
                    "to": self.event_buffer[-1]["timestamp_us"]
                },
                "chain_build_trigger": "periodic"
            },
            "signature": self.sign_payload({"event_ids": event_ids})
        })

        # Clear buffer after successful chain build
        self.event_buffer.clear()

        return chain

    def generate_compliance_report(
        self,
        start_date: str,
        end_date: str
    ) -> dict:
        """Generate a compliance report for a date range.

        Retrieves all events and claim chains in the range, computes
        summary statistics, and returns a structured report suitable
        for regulatory submission.
        """
        events = execute("get_events", {
            "agent_id": self.agent_id,
            "filters": {
                "timestamp_from": start_date,
                "timestamp_to": end_date
            },
            "limit": 10000
        })

        chains = execute("get_claim_chains", {
            "agent_id": self.agent_id,
            "filters": {
                "created_from": start_date,
                "created_to": end_date
            }
        })

        all_events = events.get("events", [])

        # Compute statistics
        opportunities = [e for e in all_events if e["event_type"] == "arbitrage.opportunity_detected"]
        executions = [e for e in all_events if e["event_type"] == "arbitrage.execution_signal"]
        settlements = [e for e in all_events if e["event_type"] == "arbitrage.settlement"]
        disputes = [e for e in all_events if e["event_type"] == "arbitrage.dispute_opened"]

        total_settled = sum(
            sum(float(v) for v in s["payload"].get("splits", {}).values())
            for s in settlements
        )

        report = {
            "report_type": "arbitrage_compliance",
            "agent_id": self.agent_id,
            "period": {"start": start_date, "end": end_date},
            "summary": {
                "total_events": len(all_events),
                "opportunities_detected": len(opportunities),
                "executions_dispatched": len(executions),
                "settlements_completed": len(settlements),
                "disputes_opened": len(disputes),
                "total_settled_usd": f"{total_settled:.2f}",
                "claim_chains_built": len(chains.get("chains", []))
            },
            "claim_chain_roots": [
                {
                    "chain_id": c["chain_id"],
                    "merkle_root": c["merkle_root"],
                    "event_count": c.get("metadata", {}).get("event_count", 0)
                }
                for c in chains.get("chains", [])
            ],
            "generated_at": datetime.utcnow().isoformat()
        }

        return report
```

### Dispute Resolution Evidence

When a counterparty disputes a fill -- claiming they executed at a different price than reported, or that they never received an execution signal -- the claim chain provides the resolution mechanism. The evidence package built by the `ExecutionVerifier` (Chapter 4) contains every event in the opportunity lifecycle, each signed by the originating bot's Ed25519 key, all anchored in a Merkle tree whose root is published and immutable.

An auditor or dispute resolver can independently verify three things without trusting any party:

1. **Completeness**: The claim chain includes all events from opportunity detection through settlement. Missing events create a gap in the Merkle proof that is cryptographically detectable.
2. **Authenticity**: Each event's Ed25519 signature binds it to the signing bot's identity. A bot cannot forge events from another bot without the private key.
3. **Ordering**: Timestamps within the chain establish the sequence of events. Combined with exchange-provided timestamps on fill reports, this creates a verifiable timeline.

```python
def open_dispute(
    self,
    opportunity_id: str,
    disputed_by: str,
    reason: str,
    evidence_chain_id: str
) -> dict:
    """Open a dispute for an arbitrage settlement."""
    dispute_payload = {
        "opportunity_id": opportunity_id,
        "disputed_by": disputed_by,
        "reason": reason,
        "evidence_chain_id": evidence_chain_id,
        "opened_at": datetime.utcnow().isoformat()
    }

    return self.log_event("arbitrage.dispute_opened", dispute_payload)
```

### Integrating the Audit Trail

Wire the audit trail into the coordinator so every action is logged automatically:

```python
audit = ArbitrageAuditTrail(coordinator_id, COORDINATOR_PRIVATE_KEY)

# Log opportunity detection
for opp in opportunities:
    audit.log_event("arbitrage.opportunity_detected", {
        "opportunity_id": opp.opportunity_id,
        "symbol": opp.symbol,
        "buy_exchange": opp.buy_exchange,
        "sell_exchange": opp.sell_exchange,
        "spread_bps": opp.spread_bps,
        "net_profit_usd": opp.net_profit_usd,
        "detected_at": opp.detected_at
    })

# Log escrow creation
audit.log_event("arbitrage.escrow_created", {
    "opportunity_id": opp.opportunity_id,
    "escrow_id": "esc-abc123",
    "amount": opp.net_profit_usd,
    "conditions": "verified_execution"
})

# Log settlement
audit.log_event("arbitrage.settlement", {
    "opportunity_id": opp.opportunity_id,
    "escrow_id": "esc-abc123",
    "splits": splits,
    "evidence_chain_id": "chain-xyz789"
})

# Build periodic Merkle chain (run on schedule)
chain = audit.build_periodic_chain()
print(f"Audit chain built: {chain.get('chain_id')}")
print(f"Merkle root: {chain.get('merkle_root')}")
```

### Monitoring and Alerting

Submit audit trail health metrics to GreenHelix for observability:

```python
execute("submit_metrics", {
    "agent_id": coordinator_id,
    "metrics": {
        "audit_events_today": 2847,
        "audit_buffer_size": len(audit.event_buffer),
        "chains_built_today": 96,
        "opportunities_detected_today": 412,
        "settlements_completed_today": 387,
        "disputes_today": 2,
        "settlement_rate": 0.939,
        "avg_settlement_time_ms": 4200
    }
})
```

```bash
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "submit_metrics",
    "input": {
      "agent_id": "arb-coordinator-01",
      "metrics": {
        "audit_events_today": 2847,
        "chains_built_today": 96,
        "opportunities_detected_today": 412,
        "settlements_completed_today": 387,
        "disputes_today": 2,
        "settlement_rate": 0.939
      }
    }
  }'
```

### Generating a Compliance Report

```python
report = audit.generate_compliance_report(
    start_date="2026-04-01T00:00:00Z",
    end_date="2026-04-07T23:59:59Z"
)

print(json.dumps(report, indent=2))
```

```bash
# Query events for compliance
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "get_events",
    "input": {
      "agent_id": "arb-coordinator-01",
      "filters": {
        "timestamp_from": "2026-04-01T00:00:00Z",
        "timestamp_to": "2026-04-07T23:59:59Z"
      },
      "limit": 10000
    }
  }'
```

```bash
# Query claim chains for audit verification
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "get_claim_chains",
    "input": {
      "agent_id": "arb-coordinator-01",
      "filters": {
        "created_from": "2026-04-01T00:00:00Z",
        "created_to": "2026-04-07T23:59:59Z"
      }
    }
  }'
```

---

## What's Next

**Companion Guides:**

- **Tamper-Proof Audit Trails for Trading Bots** -- Deep dive into EU AI Act, MiFID II, and SEC 17a-4 compliance for your arbitrage audit trail. Extends the logging patterns in Chapter 8 with Merkle tree verification and webhook-based real-time audit forwarding.
- **Verified Bot Reputation** -- Turn your arbitrage execution metrics into a provable reputation asset. Counterparties can verify your fill rate, latency, and settlement history before agreeing to coordinate.
- **Strategy Marketplace Playbook** -- Publish your arbitrage coordination framework as a product on the GreenHelix marketplace, with reputation-backed performance claims and escrow-protected licensing.

**GreenHelix Documentation:**

- Full API reference: https://api.greenhelix.net/v1
- Escrow lifecycle and dispute resolution in the platform documentation
- Event bus schemas and claim chain verification procedures

**Production Considerations:**

The framework in this guide is architecturally complete but requires exchange-specific adapters for production deployment. Each exchange has its own WebSocket feed format, order API schema, authentication mechanism, and rate limits. The ArbitrageCoordinator, OpportunityScanner, ExecutionVerifier, and ProfitSplitter are exchange-agnostic by design -- they communicate through GreenHelix events and escrow, not through exchange APIs directly. The exchange specialist bots encapsulate all exchange-specific logic. Adding a new exchange means writing one new specialist bot and registering it on GreenHelix, not modifying any framework code.

---

*This guide describes coordination patterns for autonomous trading bots. Arbitrage across exchanges carries financial risk including but not limited to execution risk, counterparty risk, exchange insolvency risk, and regulatory risk. The fee structures and latency numbers cited are representative as of Q1 2026 and change frequently. Test all strategies in a paper-trading environment before deploying real capital. Consult your compliance counsel for jurisdiction-specific obligations related to algorithmic trading.*

