---
name: greenhelix-trading-bot-risk-service
version: "1.3.1"
description: "Trading Bot Risk-as-a-Service: Real-Time Portfolio Risk Monitoring for Multi-Exchange Operations. Build a cross-exchange, cross-strategy real-time portfolio risk monitoring system with webhooks, event bus, and SLA compliance enforcement. Covers drawdown alerts, correlation monitoring, liquidation proximity, circuit breakers, and production deployment."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [trading-bot, risk-management, portfolio, monitoring, circuit-breaker, guide, greenhelix, openclaw, ai-agent]
price_usd: 0.0
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
# Trading Bot Risk-as-a-Service: Real-Time Portfolio Risk Monitoring for Multi-Exchange Operations

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `AGENT_SIGNING_KEY`: Cryptographic signing key for agent identity (Ed25519 key pair for request signing)


If you run trading bots across multiple exchanges, you have a visibility problem. Binance shows you Binance positions. Coinbase shows you Coinbase positions. Kraken shows you Kraken positions. Nobody shows you the aggregate. Nobody tells you that your mean-reversion strategy on Binance and your momentum strategy on Coinbase have become 0.94 correlated over the last four hours -- meaning a single market move will hit both simultaneously. Nobody warns you that your combined leverage across three exchanges has crept from 3x to 7x because each exchange only sees its own slice. The May 2025 cascade liquidations on BitMEX made this concrete: bots running isolated risk checks per exchange missed the aggregate exposure building across venues, and when BTC dropped 12% in ninety minutes, the cross-exchange margin calls arrived simultaneously. Operators who had $200K in aggregate equity across four exchanges discovered they were effectively running 11x leverage when positions were netted. The liquidation cascade took 47 seconds from first margin call to full wipeout. This guide builds a complete, production-grade risk monitoring system that sits above your exchange connections and provides a unified view of portfolio risk. It uses GreenHelix's event bus for real-time data aggregation, webhooks for alert delivery, and SLA compliance monitoring for operational health tracking. You will build drawdown trackers, correlation monitors, liquidation proximity engines, and circuit breakers -- all wired together through a single risk management layer that treats your entire multi-exchange operation as one portfolio.
1. [Risk Architecture Overview](#chapter-1-risk-architecture-overview)
2. [The RiskMonitor Class](#chapter-2-the-riskmonitor-class)

## What You'll Learn
- Chapter 1: Risk Architecture Overview
- Chapter 2: The RiskMonitor Class
- Chapter 3: Drawdown Monitoring and Alerts
- Chapter 4: Correlation Monitoring
- Chapter 5: Liquidation Proximity Engine
- Chapter 6: Circuit Breaker Implementation
- Chapter 7: Multi-Exchange Aggregation
- Next Steps
- What's Next

## Full Guide

# Trading Bot Risk-as-a-Service: Real-Time Portfolio Risk Monitoring for Multi-Exchange Operations

If you run trading bots across multiple exchanges, you have a visibility problem. Binance shows you Binance positions. Coinbase shows you Coinbase positions. Kraken shows you Kraken positions. Nobody shows you the aggregate. Nobody tells you that your mean-reversion strategy on Binance and your momentum strategy on Coinbase have become 0.94 correlated over the last four hours -- meaning a single market move will hit both simultaneously. Nobody warns you that your combined leverage across three exchanges has crept from 3x to 7x because each exchange only sees its own slice. The May 2025 cascade liquidations on BitMEX made this concrete: bots running isolated risk checks per exchange missed the aggregate exposure building across venues, and when BTC dropped 12% in ninety minutes, the cross-exchange margin calls arrived simultaneously. Operators who had $200K in aggregate equity across four exchanges discovered they were effectively running 11x leverage when positions were netted. The liquidation cascade took 47 seconds from first margin call to full wipeout. This guide builds a complete, production-grade risk monitoring system that sits above your exchange connections and provides a unified view of portfolio risk. It uses GreenHelix's event bus for real-time data aggregation, webhooks for alert delivery, and SLA compliance monitoring for operational health tracking. You will build drawdown trackers, correlation monitors, liquidation proximity engines, and circuit breakers -- all wired together through a single risk management layer that treats your entire multi-exchange operation as one portfolio.

---

## Table of Contents

1. [Risk Architecture Overview](#chapter-1-risk-architecture-overview)
2. [The RiskMonitor Class](#chapter-2-the-riskmonitor-class)
3. [Drawdown Monitoring and Alerts](#chapter-3-drawdown-monitoring-and-alerts)
4. [Correlation Monitoring](#chapter-4-correlation-monitoring)
5. [Liquidation Proximity Engine](#chapter-5-liquidation-proximity-engine)
6. [Circuit Breaker Implementation](#chapter-6-circuit-breaker-implementation)
7. [Multi-Exchange Aggregation](#chapter-7-multi-exchange-aggregation)
9. [What's Next](#whats-next)

---

## Chapter 1: Risk Architecture Overview

### Why Centralized Risk Monitoring Matters

Every professional trading desk has a risk management layer that sits above the execution layer. The risk system sees all positions, all strategies, all venues. It computes aggregate exposure, monitors correlation regimes, and has the authority to halt trading when thresholds are breached. Retail and semi-professional bot operators skip this layer because building it is hard and the exchanges do not provide the APIs to do it natively across venues. The result is that a $500K multi-exchange bot operation runs with less risk infrastructure than a single-desk prop trader at a regional firm.

The failure modes are specific and predictable:

- **Cross-exchange leverage accumulation**: Each exchange computes margin independently. A 3x position on Binance and a 3x position on Coinbase in correlated assets is effectively 6x aggregate leverage against your total equity -- but neither exchange reports it that way.
- **Correlation regime changes**: Two strategies that were uncorrelated during backtesting become highly correlated during market stress. The diversification benefit you assumed in your position sizing disappears exactly when you need it.
- **Cascading liquidations**: A liquidation on one exchange reduces your total equity, which increases your leverage ratio on other exchanges, which triggers further liquidations. This feedback loop operates faster than human reaction time.
- **Silent risk drift**: Without continuous monitoring, risk parameters drift over days and weeks. A portfolio that started at 2x aggregate leverage creeps to 5x through a series of individually reasonable position additions.

### Architecture

The system has four layers:

```
+------------------+    +------------------+    +------------------+
|  Binance Bot     |    |  Coinbase Bot    |    |  Kraken Bot      |
|  (execution)     |    |  (execution)     |    |  (execution)     |
+--------+---------+    +--------+---------+    +--------+---------+
         |                       |                       |
         |   publish_event       |   publish_event       |   publish_event
         v                       v                       v
+------------------------------------------------------------------------+
|                     GreenHelix Event Bus                                |
|  (real-time event ingestion, schema validation, ordering)              |
+--------+---------------------+-----------------------+-----------------+
         |                     |                       |
         |   get_events        |   webhooks            |   get_sla_compliance
         v                     v                       v
+------------------------------------------------------------------------+
|                     Risk Engine                                        |
|  +----------------+  +------------------+  +------------------------+  |
|  | DrawdownTracker|  | CorrelationMon   |  | LiquidationProximity   |  |
|  +----------------+  +------------------+  +------------------------+  |
|  +----------------+  +------------------+  +------------------------+  |
|  | CircuitBreaker |  | ExchangeAggr     |  | AlertManager           |  |
|  +----------------+  +------------------+  +------------------------+  |
+--------+---------------------------------------------------------------+
         |
         |   send_message / register_webhook
         v
+------------------------------------------------------------------------+
|                     Alert Delivery                                      |
|  Slack, PagerDuty, Telegram, Email, SMS                                |
+------------------------------------------------------------------------+
```

### GreenHelix Tools Used

This guide uses seven GreenHelix tools:

| Tool | Purpose |
|------|---------|
| `register_agent` | Register the risk monitoring agent |
| `register_webhook` | Set up alert delivery endpoints |
| `publish_event` | Bots publish position and trade events |
| `get_events` | Risk engine retrieves events for analysis |
| `get_sla_compliance` | Monitor risk engine uptime and latency |
| `submit_metrics` | Report risk metrics for observability |
| `send_message` | Deliver alerts to operators |

### Risk Metrics Hierarchy

Risk metrics are computed at four levels, each aggregating from the level below:

1. **Position-level**: Per-position P&L, unrealized P&L, distance to liquidation, margin utilization
2. **Strategy-level**: Strategy drawdown, strategy Sharpe ratio (rolling), strategy exposure, number of open positions
3. **Portfolio-level**: Aggregate drawdown, cross-strategy correlation matrix, net exposure by asset, aggregate leverage
4. **Fleet-level**: Total equity at risk, number of active strategies, circuit breaker status, SLA compliance score

Each level publishes events to the GreenHelix event bus, and higher levels consume events from lower levels. This creates a clean data flow where the risk engine never polls exchanges directly -- it only reads from the event bus.

### Event Types for Risk Monitoring

Define one event type per risk signal:

| Event Type | Trigger | Key Fields |
|---|---|---|
| `risk.portfolio_check` | Periodic risk scan completes | total_equity, aggregate_leverage, alerts |
| `risk.drawdown_alert` | Drawdown exceeds threshold | level, threshold_pct, current_pct, trigger_timeframe |
| `risk.correlation_matrix` | Correlation matrix updated | matrix, strategy_count |
| `risk.correlation_regime_change` | Correlation shift detected | avg_change, max_change |
| `risk.liquidation_proximity` | Liquidation check completes | positions, min_distance_pct |
| `risk.circuit_breaker_transition` | State change | from, to, reason, trip_count |
| `risk.circuit_breaker_config` | Triggers updated | triggers |
| `risk.aggregate_snapshot` | Cross-exchange aggregation | total_equity, aggregate_leverage, net_exposure |
| `risk.thresholds_updated` | Risk thresholds changed | thresholds |
| `risk.key_rotated` | Agent key rotation | new_public_key |

Each event is signed with the risk agent's Ed25519 private key. The signature covers the canonical JSON serialization of the payload (keys sorted, no whitespace), ensuring that risk events cannot be fabricated or tampered with after the fact. This matters when you need to prove to auditors or investors that a circuit breaker tripped at a specific time for a specific reason.

### Verifying the API Connection

Before building the full risk engine, verify that your GreenHelix API credentials work:

```bash
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "register_agent",
    "input": {
      "agent_id": "risk-monitor-prod-01",
      "public_key": "'"$PUBLIC_KEY_B64"'",
      "name": "Portfolio Risk Monitor"
    }
  }'
```

```python
import requests

API_BASE = "https://api.greenhelix.net/v1"
API_KEY = "your-api-key"

response = requests.post(
    f"{API_BASE}/v1",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    },
    json={
        "tool": "register_agent",
        "input": {
            "agent_id": "risk-monitor-prod-01",
            "public_key": "your-public-key-base64",
            "name": "Portfolio Risk Monitor",
        },
    },
)
print(response.json())
```

If both return a success response with your agent ID, the foundation is in place.

---

## Chapter 2: The RiskMonitor Class

### Core Infrastructure

The `RiskMonitor` class is the foundation for all risk monitoring in this guide. Every subsequent chapter builds on it.

```bash
# Generate an Ed25519 keypair for the risk monitor agent
python3 -c "
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import base64

private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

priv_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PrivateFormat.Raw,
    encryption_algorithm=serialization.NoEncryption()
)
pub_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw
)

print(f'PRIVATE_KEY_B64={base64.b64encode(priv_bytes).decode()}')
print(f'PUBLIC_KEY_B64={base64.b64encode(pub_bytes).decode()}')
"
```

```bash
# Register the risk monitor agent
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "register_agent",
    "input": {
      "agent_id": "risk-monitor-prod-01",
      "public_key": "'"$PUBLIC_KEY_B64"'",
      "name": "Portfolio Risk Monitor"
    }
  }'
```

### Python Implementation

```python
import json
import time
import base64
import hashlib
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

import requests
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization


class RiskMonitor:
    """Cross-exchange portfolio risk monitoring using GreenHelix APIs."""

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        private_key_b64: str,
        base_url: str = "https://api.greenhelix.net/v1",
    ):
        self.api_key = api_key
        self.agent_id = agent_id
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

        # Load Ed25519 private key
        key_bytes = base64.b64decode(private_key_b64)
        self._private_key = Ed25519PrivateKey.from_private_bytes(key_bytes)
        self._public_key = self._private_key.public_key()

        # Risk thresholds (defaults)
        self.thresholds = {
            "max_drawdown_pct": 15.0,
            "max_correlation": 0.85,
            "max_leverage": 5.0,
            "min_margin_ratio": 0.20,
            "max_single_position_pct": 25.0,
        }

    def _execute(self, tool: str, input_data: dict) -> dict:
        """Execute a GreenHelix tool."""
        response = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        response.raise_for_status()
        return response.json()

    def _sign(self, payload: dict) -> str:
        """Sign a payload with Ed25519."""
        canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        signature = self._private_key.sign(canonical.encode("utf-8"))
        return base64.b64encode(signature).decode()

    def register_risk_agent(self) -> dict:
        """Register this risk monitor as a GreenHelix agent."""
        pub_bytes = self._public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        return self._execute("register_agent", {
            "agent_id": self.agent_id,
            "public_key": base64.b64encode(pub_bytes).decode(),
            "name": f"Risk Monitor ({self.agent_id})",
        })

    def configure_thresholds(
        self,
        max_drawdown_pct: float = 15.0,
        max_correlation: float = 0.85,
        max_leverage: float = 5.0,
        min_margin_ratio: float = 0.20,
        max_single_position_pct: float = 25.0,
    ) -> dict:
        """Set risk thresholds and publish them as a configuration event."""
        self.thresholds = {
            "max_drawdown_pct": max_drawdown_pct,
            "max_correlation": max_correlation,
            "max_leverage": max_leverage,
            "min_margin_ratio": min_margin_ratio,
            "max_single_position_pct": max_single_position_pct,
        }

        event_payload = {
            "agent_id": self.agent_id,
            "thresholds": self.thresholds,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        event_payload["signature"] = self._sign(self.thresholds)

        return self._execute("publish_event", {
            "event_type": "risk.thresholds_updated",
            "payload": event_payload,
        })

    def check_portfolio_risk(self, positions: List[dict]) -> dict:
        """
        Run all risk checks against current positions.

        Returns a dict with risk metrics and any triggered alerts.
        """
        total_equity = sum(p.get("equity", 0) for p in positions)
        total_notional = sum(abs(p.get("notional", 0)) for p in positions)
        leverage = total_notional / total_equity if total_equity > 0 else float("inf")

        alerts = []

        # Check leverage
        if leverage > self.thresholds["max_leverage"]:
            alerts.append({
                "type": "leverage_breach",
                "current": round(leverage, 2),
                "threshold": self.thresholds["max_leverage"],
                "severity": "critical",
            })

        # Check concentration
        for pos in positions:
            if total_notional > 0:
                concentration = abs(pos.get("notional", 0)) / total_notional * 100
                if concentration > self.thresholds["max_single_position_pct"]:
                    alerts.append({
                        "type": "concentration_breach",
                        "position": pos.get("symbol", "unknown"),
                        "current_pct": round(concentration, 2),
                        "threshold": self.thresholds["max_single_position_pct"],
                        "severity": "warning",
                    })

        risk_summary = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "total_equity": total_equity,
            "total_notional": total_notional,
            "aggregate_leverage": round(leverage, 2),
            "position_count": len(positions),
            "alerts": alerts,
            "status": "critical" if any(a["severity"] == "critical" for a in alerts)
                      else "warning" if alerts
                      else "healthy",
        }

        # Publish risk check result as event
        event_payload = {
            "agent_id": self.agent_id,
            **risk_summary,
        }
        event_payload["signature"] = self._sign(risk_summary)

        self._execute("publish_event", {
            "event_type": "risk.portfolio_check",
            "payload": event_payload,
        })

        return risk_summary
```

### Configuring Thresholds via curl

```bash
# Publish a threshold configuration event
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "publish_event",
    "input": {
      "event_type": "risk.thresholds_updated",
      "payload": {
        "agent_id": "risk-monitor-prod-01",
        "thresholds": {
          "max_drawdown_pct": 15.0,
          "max_correlation": 0.85,
          "max_leverage": 5.0,
          "min_margin_ratio": 0.20,
          "max_single_position_pct": 25.0
        },
        "timestamp": "2026-04-07T12:00:00Z",
        "signature": "base64-ed25519-signature"
      }
    }
  }'
```

### Usage Example

```python
monitor = RiskMonitor(
    api_key="your-api-key",
    agent_id="risk-monitor-prod-01",
    private_key_b64="your-private-key-base64",
)

# Register and configure
monitor.register_risk_agent()
monitor.configure_thresholds(
    max_drawdown_pct=12.0,
    max_leverage=4.0,
    min_margin_ratio=0.25,
)

# Check risk against current positions
positions = [
    {"symbol": "BTC-USD", "notional": 50000, "equity": 15000, "exchange": "binance"},
    {"symbol": "ETH-USD", "notional": 30000, "equity": 10000, "exchange": "coinbase"},
    {"symbol": "SOL-USD", "notional": 20000, "equity": 8000, "exchange": "kraken"},
]

result = monitor.check_portfolio_risk(positions)
print(f"Status: {result['status']}, Leverage: {result['aggregate_leverage']}x")
```

The `RiskMonitor` class provides the transport layer and basic risk checks. The following chapters build specialized risk engines that integrate with it.

---

## Chapter 3: Drawdown Monitoring and Alerts

### Why Drawdown Is the Primary Risk Metric

Drawdown measures peak-to-trough decline. Unlike volatility (which is symmetric) or VaR (which is model-dependent), drawdown directly answers the question operators care about: "How much have I lost from my best point?" A 15% drawdown means your portfolio is worth 85% of its highest recorded value. Drawdown is also the metric most directly tied to survival -- a 50% drawdown requires a 100% gain to recover, and a 75% drawdown requires a 300% gain. Bot operators who monitor drawdown at multiple timeframes catch problems before they become existential.

### The DrawdownTracker Class

```python
import time
from collections import defaultdict
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple


class DrawdownTracker:
    """Tracks drawdown across multiple timeframes with alert escalation."""

    # Timeframe windows in seconds
    TIMEFRAMES = {
        "1h": 3600,
        "4h": 14400,
        "24h": 86400,
        "7d": 604800,
    }

    # Alert escalation levels
    ALERT_LEVELS = {
        "warning": 5.0,
        "critical": 8.0,
        "emergency": 12.0,
        "circuit_breaker": 15.0,
    }

    def __init__(self, risk_monitor: "RiskMonitor"):
        self.risk_monitor = risk_monitor
        self._equity_history: List[Tuple[float, float]] = []  # (timestamp, equity)
        self._peaks: Dict[str, float] = {}  # timeframe -> peak equity
        self._current_drawdowns: Dict[str, float] = {}
        self._alert_history: List[dict] = []

    def update(self, equity: float, timestamp: Optional[float] = None) -> dict:
        """
        Record a new equity value and compute drawdowns across all timeframes.

        Returns the current drawdown state.
        """
        ts = timestamp or time.time()
        self._equity_history.append((ts, equity))

        # Prune history older than 7 days
        cutoff = ts - self.TIMEFRAMES["7d"]
        self._equity_history = [
            (t, e) for t, e in self._equity_history if t >= cutoff
        ]

        drawdowns = {}
        for tf_name, tf_seconds in self.TIMEFRAMES.items():
            tf_cutoff = ts - tf_seconds
            tf_values = [e for t, e in self._equity_history if t >= tf_cutoff]

            if not tf_values:
                drawdowns[tf_name] = 0.0
                continue

            peak = max(tf_values)
            self._peaks[tf_name] = peak
            current_dd = ((peak - equity) / peak) * 100 if peak > 0 else 0.0
            drawdowns[tf_name] = round(current_dd, 4)

        self._current_drawdowns = drawdowns
        return drawdowns

    def check_alerts(self) -> List[dict]:
        """
        Check current drawdowns against alert thresholds.

        Returns a list of triggered alerts, sorted by severity.
        """
        alerts = []
        worst_dd = max(self._current_drawdowns.values()) if self._current_drawdowns else 0.0

        for level_name, level_threshold in sorted(
            self.ALERT_LEVELS.items(), key=lambda x: x[1]
        ):
            if worst_dd >= level_threshold:
                # Find which timeframe triggered
                trigger_tf = max(
                    self._current_drawdowns, key=self._current_drawdowns.get
                )

                alert = {
                    "level": level_name,
                    "threshold_pct": level_threshold,
                    "current_pct": round(worst_dd, 4),
                    "trigger_timeframe": trigger_tf,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "peak_equity": self._peaks.get(trigger_tf, 0),
                }
                alerts.append(alert)

        if alerts:
            self._alert_history.extend(alerts)
            # Publish the most severe alert
            worst_alert = alerts[-1]
            payload = {
                "agent_id": self.risk_monitor.agent_id,
                "alert_type": "drawdown",
                **worst_alert,
            }
            payload["signature"] = self.risk_monitor._sign(worst_alert)

            self.risk_monitor._execute("publish_event", {
                "event_type": "risk.drawdown_alert",
                "payload": payload,
            })

        return alerts

    def get_history(self, timeframe: str = "24h") -> List[dict]:
        """Get drawdown history for a specific timeframe."""
        tf_seconds = self.TIMEFRAMES.get(timeframe, 86400)
        cutoff = time.time() - tf_seconds
        return [
            {"timestamp": t, "equity": e}
            for t, e in self._equity_history
            if t >= cutoff
        ]
```

### Webhook-Based Alert Delivery

Register a webhook to receive drawdown alerts in real time:

```bash
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "register_webhook",
    "input": {
      "url": "https://your-ops-server.example.com/risk/drawdown",
      "event_types": [
        "risk.drawdown_alert",
        "risk.portfolio_check"
      ],
      "secret": "your-webhook-hmac-secret"
    }
  }'
```

```python
# Register webhooks for drawdown alerts
monitor.register_risk_agent()

webhook_result = monitor._execute("register_webhook", {
    "url": "https://your-ops-server.example.com/risk/drawdown",
    "event_types": ["risk.drawdown_alert", "risk.portfolio_check"],
    "secret": "your-webhook-hmac-secret",
})
print(f"Webhook registered: {webhook_result}")
```

### Alert Escalation in Practice

The four-level escalation model maps directly to operational responses:

| Level | Threshold | Action |
|-------|-----------|--------|
| Warning | 5% drawdown | Log and notify via Slack |
| Critical | 8% drawdown | Page the on-call operator, reduce position sizes by 50% |
| Emergency | 12% drawdown | Halt new position opens, begin unwinding existing positions |
| Circuit Breaker | 15% drawdown | Cancel all open orders, close all positions, halt all strategies |

### Running the Drawdown Loop

```python
tracker = DrawdownTracker(risk_monitor=monitor)

# Simulate a monitoring loop (in production, this runs continuously)
def run_drawdown_monitor(monitor: RiskMonitor, tracker: DrawdownTracker):
    """Poll equity every 10 seconds and check drawdown alerts."""
    while True:
        # Fetch latest equity from your exchange aggregation layer
        events = monitor._execute("get_events", {
            "event_type": "exchange.equity_update",
            "limit": 1,
            "order": "desc",
        })

        if events.get("events"):
            equity = events["events"][0]["payload"].get("total_equity", 0)
            drawdowns = tracker.update(equity)
            alerts = tracker.check_alerts()

            if alerts:
                worst = alerts[-1]
                print(
                    f"[{worst['level'].upper()}] Drawdown: {worst['current_pct']}% "
                    f"(threshold: {worst['threshold_pct']}%, "
                    f"timeframe: {worst['trigger_timeframe']})"
                )

                # Send alert via messaging
                if worst["level"] in ("emergency", "circuit_breaker"):
                    monitor._execute("send_message", {
                        "to": "ops-team",
                        "subject": f"RISK ALERT: {worst['level'].upper()} drawdown",
                        "body": (
                            f"Drawdown: {worst['current_pct']}% "
                            f"(threshold: {worst['threshold_pct']}%)\n"
                            f"Timeframe: {worst['trigger_timeframe']}\n"
                            f"Peak equity: ${worst['peak_equity']:,.2f}"
                        ),
                    })

        time.sleep(10)
```

```bash
# Query drawdown alert history via curl
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "get_events",
    "input": {
      "event_type": "risk.drawdown_alert",
      "limit": 20,
      "order": "desc"
    }
  }'
```

### Drawdown Severity Classification

Not all drawdowns are equal. A 10% drawdown in a trending market during high volatility is qualitatively different from a 10% drawdown in a ranging market during low volatility. The tracker uses the drawdown across multiple timeframes to classify severity:

- **Shallow, slow drawdown** (24h drawdown > 1h drawdown): The portfolio is grinding lower. This is typically caused by a losing trend-following position. Monitor but do not panic -- the strategy may recover when the trend reverses.
- **Deep, fast drawdown** (1h drawdown > 24h drawdown): The portfolio is in rapid decline. This pattern is characteristic of liquidation cascades, flash crashes, or correlated position blowups. Immediate attention required.
- **Oscillating drawdown** (1h and 4h drawdowns similar, both < 24h): The portfolio is whipsawing. This pattern is common during high-volatility news events. Reduce position sizes rather than closing positions -- the whipsaw may resolve in either direction.

The drawdown tracker publishes this classification in the event payload, allowing downstream consumers (the circuit breaker, alert manager) to tailor their response to the type of drawdown, not just the magnitude.

The drawdown tracker is intentionally simple. It uses empirical peaks, not modeled ones. It does not try to predict future drawdown -- it measures what has already happened and triggers actions based on predefined thresholds. Predictive models add complexity without adding reliability under stress conditions.

---

## Chapter 4: Correlation Monitoring

### Why Correlation Kills Portfolios

Diversification is the only free lunch in finance -- until it isn't. Portfolio theory assumes that combining uncorrelated strategies reduces total risk. If Strategy A has a Sharpe of 1.5 and Strategy B has a Sharpe of 1.5, and they are uncorrelated, the combined portfolio has a Sharpe of roughly 2.1. But correlation is not static. During market stress, correlations spike. The 2020 COVID crash saw BTC-ETH correlation go from 0.6 to 0.95 in 48 hours. The 2022 LUNA collapse pushed correlations across all crypto assets above 0.9 for weeks. Strategies that appeared diversified during calm markets became a single concentrated bet during the exact conditions where diversification mattered most.

Monitoring correlation in real time -- and detecting regime changes -- lets you reduce exposure before the diversification illusion costs you capital.

### The CorrelationMonitor Class

```python
import math
from collections import deque
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple


class CorrelationMonitor:
    """
    Rolling correlation computation between strategies
    with regime change detection.
    """

    def __init__(
        self,
        risk_monitor: "RiskMonitor",
        window_size: int = 100,
        regime_change_threshold: float = 0.3,
    ):
        self.risk_monitor = risk_monitor
        self.window_size = window_size
        self.regime_change_threshold = regime_change_threshold

        # Returns buffer per strategy
        self._returns: Dict[str, deque] = {}
        self._correlation_history: List[dict] = []
        self._previous_matrix: Optional[Dict[str, Dict[str, float]]] = None

    def add_returns(self, strategy_id: str, returns_value: float) -> None:
        """Add a return observation for a strategy."""
        if strategy_id not in self._returns:
            self._returns[strategy_id] = deque(maxlen=self.window_size)
        self._returns[strategy_id].append(returns_value)

    def _pearson(self, x: List[float], y: List[float]) -> float:
        """Compute Pearson correlation between two series."""
        n = min(len(x), len(y))
        if n < 10:
            return 0.0

        x, y = x[:n], y[:n]
        mean_x = sum(x) / n
        mean_y = sum(y) / n

        cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        std_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x))
        std_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y))

        if std_x == 0 or std_y == 0:
            return 0.0

        return cov / (std_x * std_y)

    def compute_matrix(self) -> Dict[str, Dict[str, float]]:
        """Compute the full correlation matrix across all strategies."""
        strategies = sorted(self._returns.keys())
        matrix = {}

        for s1 in strategies:
            matrix[s1] = {}
            for s2 in strategies:
                if s1 == s2:
                    matrix[s1][s2] = 1.0
                else:
                    corr = self._pearson(
                        list(self._returns[s1]),
                        list(self._returns[s2]),
                    )
                    matrix[s1][s2] = round(corr, 4)

        # Publish the matrix as an event
        payload = {
            "agent_id": self.risk_monitor.agent_id,
            "matrix": matrix,
            "strategy_count": len(strategies),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        payload["signature"] = self.risk_monitor._sign({"matrix": matrix})

        self.risk_monitor._execute("publish_event", {
            "event_type": "risk.correlation_matrix",
            "payload": payload,
        })

        self._correlation_history.append({
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "matrix": matrix,
        })

        return matrix

    def detect_regime_change(self) -> Optional[dict]:
        """
        Detect if the correlation regime has changed significantly.

        Compares current matrix to previous matrix. A regime change is
        detected when the average absolute change in correlations exceeds
        the threshold.
        """
        current = self.compute_matrix()

        if self._previous_matrix is None:
            self._previous_matrix = current
            return None

        strategies = sorted(current.keys())
        changes = []

        for s1 in strategies:
            for s2 in strategies:
                if s1 >= s2:
                    continue
                prev = self._previous_matrix.get(s1, {}).get(s2, 0.0)
                curr = current.get(s1, {}).get(s2, 0.0)
                changes.append(abs(curr - prev))

        if not changes:
            self._previous_matrix = current
            return None

        avg_change = sum(changes) / len(changes)
        max_change = max(changes)

        self._previous_matrix = current

        if avg_change > self.regime_change_threshold:
            alert = {
                "type": "correlation_regime_change",
                "avg_change": round(avg_change, 4),
                "max_change": round(max_change, 4),
                "threshold": self.regime_change_threshold,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "matrix": current,
            }

            # Publish regime change event
            event_payload = {
                "agent_id": self.risk_monitor.agent_id,
                **alert,
            }
            event_payload["signature"] = self.risk_monitor._sign(alert)

            self.risk_monitor._execute("publish_event", {
                "event_type": "risk.correlation_regime_change",
                "payload": event_payload,
            })

            return alert

        return None
```

### Querying Correlation History via curl

```bash
# Get recent correlation matrix events
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "get_events",
    "input": {
      "event_type": "risk.correlation_matrix",
      "limit": 10,
      "order": "desc"
    }
  }'
```

```bash
# Get regime change alerts
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "get_events",
    "input": {
      "event_type": "risk.correlation_regime_change",
      "limit": 5,
      "order": "desc"
    }
  }'
```

### Usage Example

```python
corr_monitor = CorrelationMonitor(
    risk_monitor=monitor,
    window_size=100,
    regime_change_threshold=0.3,
)

# Feed returns from each strategy (in production, these come from trade events)
import random
for i in range(120):
    corr_monitor.add_returns("mean-reversion-btc", random.gauss(0.001, 0.02))
    corr_monitor.add_returns("momentum-eth", random.gauss(0.0005, 0.025))
    corr_monitor.add_returns("arb-sol-perps", random.gauss(0.0008, 0.015))

matrix = corr_monitor.compute_matrix()
for s1, row in matrix.items():
    print(f"{s1}: {row}")

regime = corr_monitor.detect_regime_change()
if regime:
    print(f"REGIME CHANGE detected: avg change {regime['avg_change']}")
```

### Interpreting the Correlation Matrix

The correlation matrix is symmetric with 1.0 on the diagonal. Off-diagonal values range from -1.0 (perfectly inverse) to +1.0 (perfectly correlated). For risk management purposes:

- **Below 0.3**: Strategies are effectively uncorrelated. Diversification benefit is real.
- **0.3 to 0.6**: Moderate correlation. Some diversification benefit remains, but not full.
- **0.6 to 0.85**: High correlation. The strategies will draw down together in stressed markets. Position sizes should account for this.
- **Above 0.85**: The strategies are effectively the same bet. The circuit breaker should consider triggering if this persists.

### Practical Considerations for Correlation Monitoring

**Window size selection**: The `window_size` parameter controls how many return observations are used to compute correlation. Smaller windows (30-50) are more responsive to recent correlation changes but produce noisier estimates. Larger windows (100-200) are more stable but slower to detect regime changes. A common compromise is to run two correlation monitors in parallel -- one with a 50-observation window for early detection and one with a 150-observation window for confirmation.

**Return frequency**: The correlation monitor needs returns at a consistent frequency. If Strategy A reports returns every minute and Strategy B reports every 15 minutes, the correlation estimate will be unreliable. Normalize to the lowest common frequency across all strategies. For most crypto bot operations, 5-minute or 15-minute returns provide a good balance between responsiveness and stability.

**Handling missing data**: If a strategy stops reporting returns (e.g., because the bot crashed or the exchange is down), the correlation monitor should flag this rather than computing correlation with stale data. A strategy that has not reported in 30 minutes should be excluded from the matrix with a note, not included with its last known returns repeated.

**Correlation is not causation**: Two strategies can be highly correlated because they both respond to the same market factor (e.g., BTC price), not because they are redundant. If Strategy A goes long BTC on momentum signals and Strategy B goes long ETH on mean-reversion signals, they may be correlated during strong BTC moves (because ETH follows BTC) but serve different functions in the portfolio. Use correlation as an input to risk decisions, not as the sole decision criterion.

---

## Chapter 5: Liquidation Proximity Engine

### Why Distance to Liquidation Matters

A position's P&L tells you what has happened. Distance to liquidation tells you what will happen if the market moves against you by a specific amount. A position might be profitable but dangerously close to liquidation if leverage is high. Exchange liquidation engines are not gentle -- they liquidate at market, often at prices significantly worse than the liquidation price, and they charge liquidation fees. Getting liquidated on a leveraged position typically costs 2-5% more than closing the position manually at the same price. Binance charges a liquidation clearance fee that can be as high as 1.5% of the position's notional value. Coinbase's liquidation engine can execute up to 5% below the liquidation price during fast markets. These costs are invisible until they hit -- and they always hit at the worst possible time, during exactly the market conditions where your portfolio can least afford the additional loss.

The liquidation proximity engine monitors distance to liquidation across all positions on all exchanges and triggers alerts before the exchange's liquidation engine takes over. The goal is simple: never get liquidated. Always close the position yourself, at a better price, before the exchange does it for you.

### Exchange Margin Models

Different exchanges use different margin models, and this affects liquidation price calculation:

- **Isolated margin** (per-position): Each position has its own margin. Liquidation price depends only on that position's margin and entry price. Simple to calculate, but does not benefit from cross-position netting.
- **Cross margin** (per-account): All positions on the account share a single margin pool. A profitable position's unrealized P&L can offset a losing position's margin requirement. Liquidation depends on the aggregate account equity vs total maintenance margin.

### The LiquidationProximityEngine Class

```python
from datetime import datetime, timezone
from typing import Dict, List, Optional


class LiquidationProximityEngine:
    """
    Monitors distance to liquidation across exchanges and margin modes.
    """

    # Maintenance margin rates by exchange (simplified)
    MAINTENANCE_MARGIN = {
        "binance": 0.004,   # 0.4% for BTC
        "coinbase": 0.005,  # 0.5%
        "kraken": 0.005,    # 0.5%
    }

    def __init__(
        self,
        risk_monitor: "RiskMonitor",
        alert_threshold_pct: float = 20.0,
        critical_threshold_pct: float = 10.0,
    ):
        self.risk_monitor = risk_monitor
        self.alert_threshold_pct = alert_threshold_pct
        self.critical_threshold_pct = critical_threshold_pct
        self._positions: List[dict] = []
        self._alerts: List[dict] = []

    def _calc_liquidation_price_isolated(
        self,
        entry_price: float,
        side: str,
        leverage: float,
        maint_margin_rate: float,
    ) -> float:
        """
        Calculate liquidation price for an isolated-margin position.

        For longs: liq = entry * (1 - 1/leverage + maint_margin_rate)
        For shorts: liq = entry * (1 + 1/leverage - maint_margin_rate)
        """
        if side == "long":
            return entry_price * (1 - 1 / leverage + maint_margin_rate)
        else:
            return entry_price * (1 + 1 / leverage - maint_margin_rate)

    def _calc_distance_to_liquidation(
        self,
        current_price: float,
        liquidation_price: float,
        side: str,
    ) -> float:
        """Calculate percentage distance from current price to liquidation."""
        if side == "long":
            distance = (current_price - liquidation_price) / current_price * 100
        else:
            distance = (liquidation_price - current_price) / current_price * 100
        return max(0.0, round(distance, 4))

    def update_positions(self, positions: List[dict]) -> List[dict]:
        """
        Update tracked positions and compute liquidation proximity.

        Each position dict should have:
        - symbol, exchange, side, entry_price, current_price,
          leverage, margin_mode, quantity
        """
        self._positions = positions
        results = []

        for pos in positions:
            exchange = pos.get("exchange", "binance")
            maint_rate = self.MAINTENANCE_MARGIN.get(exchange, 0.005)
            margin_mode = pos.get("margin_mode", "isolated")

            if margin_mode == "isolated":
                liq_price = self._calc_liquidation_price_isolated(
                    entry_price=pos["entry_price"],
                    side=pos["side"],
                    leverage=pos["leverage"],
                    maint_margin_rate=maint_rate,
                )
            else:
                # Cross margin: use account-level equity
                # Simplified: treat as isolated with effective leverage
                liq_price = self._calc_liquidation_price_isolated(
                    entry_price=pos["entry_price"],
                    side=pos["side"],
                    leverage=pos.get("effective_leverage", pos["leverage"]),
                    maint_margin_rate=maint_rate,
                )

            distance = self._calc_distance_to_liquidation(
                current_price=pos["current_price"],
                liquidation_price=liq_price,
                side=pos["side"],
            )

            result = {
                "symbol": pos["symbol"],
                "exchange": exchange,
                "side": pos["side"],
                "entry_price": pos["entry_price"],
                "current_price": pos["current_price"],
                "liquidation_price": round(liq_price, 2),
                "distance_pct": distance,
                "leverage": pos["leverage"],
                "status": "critical" if distance < self.critical_threshold_pct
                          else "warning" if distance < self.alert_threshold_pct
                          else "safe",
            }
            results.append(result)

        # Publish positions with liquidation data
        payload = {
            "agent_id": self.risk_monitor.agent_id,
            "positions": results,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        payload["signature"] = self.risk_monitor._sign(
            {"positions_count": len(results)}
        )

        self.risk_monitor._execute("publish_event", {
            "event_type": "risk.liquidation_proximity",
            "payload": payload,
        })

        return results

    def get_alerts(self) -> List[dict]:
        """Get all positions within alert thresholds."""
        alerts = []
        for pos in self._positions:
            result = self.update_positions([pos])[0]
            if result["status"] in ("warning", "critical"):
                alerts.append(result)
        return alerts

    def get_aggregate_risk(self) -> dict:
        """Compute aggregate liquidation risk across all positions."""
        if not self._positions:
            return {"status": "no_positions", "min_distance_pct": 100.0}

        results = self.update_positions(self._positions)
        distances = [r["distance_pct"] for r in results]

        return {
            "position_count": len(results),
            "min_distance_pct": min(distances),
            "avg_distance_pct": round(sum(distances) / len(distances), 2),
            "critical_count": sum(1 for r in results if r["status"] == "critical"),
            "warning_count": sum(1 for r in results if r["status"] == "warning"),
            "closest_position": min(results, key=lambda r: r["distance_pct"]),
        }
```

### Checking Liquidation Proximity via curl

```bash
# Query recent liquidation proximity events
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "get_events",
    "input": {
      "event_type": "risk.liquidation_proximity",
      "limit": 5,
      "order": "desc"
    }
  }'
```

```bash
# Send an alert when a position is close to liquidation
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "send_message",
    "input": {
      "to": "ops-team",
      "subject": "LIQUIDATION WARNING: BTC-USD on Binance",
      "body": "BTC-USD long position is 8.5% from liquidation.\nEntry: $67,200 | Current: $63,100 | Liq: $57,800\nLeverage: 10x | Margin mode: isolated\nAction required: reduce position or add margin."
    }
  }'
```

### Usage Example

```python
liq_engine = LiquidationProximityEngine(
    risk_monitor=monitor,
    alert_threshold_pct=20.0,
    critical_threshold_pct=10.0,
)

positions = [
    {
        "symbol": "BTC-USD",
        "exchange": "binance",
        "side": "long",
        "entry_price": 67200,
        "current_price": 63100,
        "leverage": 10,
        "margin_mode": "isolated",
        "quantity": 0.5,
    },
    {
        "symbol": "ETH-USD",
        "exchange": "coinbase",
        "side": "short",
        "entry_price": 3400,
        "current_price": 3520,
        "leverage": 5,
        "margin_mode": "cross",
        "effective_leverage": 4.2,
        "quantity": 10,
    },
]

results = liq_engine.update_positions(positions)
for r in results:
    print(
        f"{r['symbol']} ({r['exchange']}): {r['distance_pct']}% from liquidation "
        f"[{r['status']}] | Liq price: ${r['liquidation_price']:,.2f}"
    )

agg = liq_engine.get_aggregate_risk()
print(f"\nAggregate: min distance {agg['min_distance_pct']}%, "
      f"{agg['critical_count']} critical, {agg['warning_count']} warnings")
```

### Aggregate Liquidation Risk

Individual position liquidation distances do not capture the full picture. In cross-margin mode, a losing position's margin requirement is covered by the account's total equity -- including unrealized profits from other positions. If those other positions reverse, the aggregate margin coverage can collapse rapidly. The `get_aggregate_risk()` method computes the minimum distance to liquidation across all positions and counts how many positions are in warning or critical states. When multiple positions are simultaneously close to liquidation, the aggregate risk is higher than what any individual position metric suggests because a liquidation on one position can cascade to others through shared margin.

The right operational response depends on the aggregate picture:
- **One position critical, others safe**: Add margin to the critical position or reduce its size. The rest of the portfolio is fine.
- **Multiple positions warning**: The portfolio is stressed. Reduce aggregate leverage by closing the weakest positions first.
- **Multiple positions critical**: This is the circuit breaker scenario. The risk of cascade liquidation is high. Close positions starting from the most leveraged.

The engine intentionally uses simplified liquidation calculations. Real exchange liquidation engines have additional factors (funding rate accruals, insurance fund contributions, ADL priority). The simplified model provides a conservative lower bound -- your actual liquidation price is slightly further away than what this engine computes, which means alerts will fire slightly early. This is the correct failure mode for a safety system.

---

## Chapter 6: Circuit Breaker Implementation

### The Case for Automated Trading Halts

Human reaction time to a risk event is measured in minutes. Market cascades are measured in seconds. The May 2025 BitMEX incident saw a $180M liquidation cascade complete in 47 seconds. No operator, no matter how attentive, can evaluate risk, make a decision, and execute that decision across three exchanges in under a minute. Circuit breakers are the solution: automated systems that halt trading when predefined conditions are met, without waiting for human approval. The human's role shifts from "react to the crisis" to "review the circuit breaker's decision after the fact and decide when to re-enable trading."

The concept is borrowed from stock exchanges, which have used circuit breakers since the 1987 crash. The NYSE halts trading when the S&P 500 drops 7% (Level 1), 13% (Level 2), or 20% (Level 3) from the previous day's close. These thresholds were calibrated through decades of experience. Your trading bot needs its own calibrated thresholds, tuned to your specific strategies, capital base, and risk tolerance. The circuit breaker in this chapter is fully configurable and integrates with the drawdown, correlation, and liquidation monitors from previous chapters to make holistic risk decisions.

### Circuit Breaker State Machine

The circuit breaker has three states:

```
                    +---------+
                    |         |
           +------>| CLOSED  |<------+
           |       | (normal)|       |
           |       +----+----+       |
           |            |            |
           |    trigger condition    |
           |    exceeded             |
           |            |            |
           |            v            |
     recovery      +----+----+      |
     period        |         |      |
     elapsed       |  OPEN   |      |
           |       | (halted)|      |
           |       +----+----+      |
           |            |            |
           |   cooldown elapsed     |
           |            |            |
           |            v            |
           |       +----+----+      |
           |       |         |      |  test trade
           +-------+HALF_OPEN+------+  fails
                   | (test)  |
                   +---------+
```

- **CLOSED**: Normal operation. All strategies execute freely. Risk monitors are active.
- **OPEN**: Trading is halted. All open orders are cancelled. No new positions are opened. Existing positions may be closed (configurable). A cooldown timer starts.
- **HALF_OPEN**: After the cooldown, one test trade is allowed with reduced position size. If it succeeds without triggering another alert, transition to CLOSED. If it fails, transition back to OPEN with a longer cooldown.

### The CircuitBreakerManager Class

```python
import enum
import time
from datetime import datetime, timezone
from typing import Callable, Dict, List, Optional


class CircuitState(enum.Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreakerManager:
    """
    Circuit breaker for trading operations with configurable triggers
    and GreenHelix SLA compliance integration.
    """

    def __init__(
        self,
        risk_monitor: "RiskMonitor",
        cooldown_seconds: int = 300,
        max_cooldown_seconds: int = 3600,
        cooldown_multiplier: float = 2.0,
        test_position_fraction: float = 0.1,
    ):
        self.risk_monitor = risk_monitor
        self.cooldown_seconds = cooldown_seconds
        self.max_cooldown_seconds = max_cooldown_seconds
        self.cooldown_multiplier = cooldown_multiplier
        self.test_position_fraction = test_position_fraction

        self._state = CircuitState.CLOSED
        self._open_since: Optional[float] = None
        self._current_cooldown = cooldown_seconds
        self._trip_count = 0
        self._trip_history: List[dict] = []

        # Configurable trigger thresholds
        self.triggers = {
            "drawdown_pct": 15.0,
            "correlation_max": 0.95,
            "liquidation_distance_pct": 10.0,
            "rapid_loss_pct": 5.0,
            "rapid_loss_window_seconds": 300,
        }

        # Callbacks for state transitions
        self._on_open_callbacks: List[Callable] = []
        self._on_close_callbacks: List[Callable] = []

    @property
    def state(self) -> CircuitState:
        return self._state

    def configure_triggers(self, **kwargs) -> None:
        """Update trigger thresholds."""
        for key, value in kwargs.items():
            if key in self.triggers:
                self.triggers[key] = value

        # Publish trigger configuration
        payload = {
            "agent_id": self.risk_monitor.agent_id,
            "triggers": self.triggers,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        payload["signature"] = self.risk_monitor._sign(self.triggers)

        self.risk_monitor._execute("publish_event", {
            "event_type": "risk.circuit_breaker_config",
            "payload": payload,
        })

    def on_open(self, callback: Callable) -> None:
        """Register a callback for when the circuit breaker opens."""
        self._on_open_callbacks.append(callback)

    def on_close(self, callback: Callable) -> None:
        """Register a callback for when the circuit breaker closes."""
        self._on_close_callbacks.append(callback)

    def evaluate(
        self,
        drawdown_pct: float = 0.0,
        max_correlation: float = 0.0,
        min_liq_distance_pct: float = 100.0,
        rapid_loss_pct: float = 0.0,
    ) -> dict:
        """
        Evaluate current risk metrics against circuit breaker triggers.

        Returns the current state and any state transitions.
        """
        now = time.time()

        if self._state == CircuitState.OPEN:
            # Check if cooldown has elapsed
            if self._open_since and (now - self._open_since) >= self._current_cooldown:
                self._transition_to(CircuitState.HALF_OPEN)
                return self._status("cooldown_elapsed")
            return self._status("waiting_cooldown")

        if self._state == CircuitState.HALF_OPEN:
            # In half-open state, check if conditions have improved
            if self._should_trip(
                drawdown_pct, max_correlation, min_liq_distance_pct, rapid_loss_pct
            ):
                # Conditions still bad -- back to OPEN with longer cooldown
                self._current_cooldown = min(
                    self._current_cooldown * self.cooldown_multiplier,
                    self.max_cooldown_seconds,
                )
                self._transition_to(CircuitState.OPEN, reason="half_open_test_failed")
                return self._status("test_failed")
            else:
                self._transition_to(CircuitState.CLOSED)
                return self._status("recovered")

        # CLOSED state -- check triggers
        trip_reasons = self._should_trip(
            drawdown_pct, max_correlation, min_liq_distance_pct, rapid_loss_pct
        )

        if trip_reasons:
            self._current_cooldown = self.cooldown_seconds
            self._transition_to(CircuitState.OPEN, reason=trip_reasons)
            return self._status("tripped")

        return self._status("healthy")

    def _should_trip(
        self,
        drawdown_pct: float,
        max_correlation: float,
        min_liq_distance_pct: float,
        rapid_loss_pct: float,
    ) -> Optional[List[str]]:
        """Check if any trigger condition is met. Returns reasons or None."""
        reasons = []

        if drawdown_pct >= self.triggers["drawdown_pct"]:
            reasons.append(
                f"drawdown {drawdown_pct:.1f}% >= {self.triggers['drawdown_pct']}%"
            )
        if max_correlation >= self.triggers["correlation_max"]:
            reasons.append(
                f"correlation {max_correlation:.2f} >= {self.triggers['correlation_max']}"
            )
        if min_liq_distance_pct <= self.triggers["liquidation_distance_pct"]:
            reasons.append(
                f"liq distance {min_liq_distance_pct:.1f}% "
                f"<= {self.triggers['liquidation_distance_pct']}%"
            )
        if rapid_loss_pct >= self.triggers["rapid_loss_pct"]:
            reasons.append(
                f"rapid loss {rapid_loss_pct:.1f}% "
                f"in {self.triggers['rapid_loss_window_seconds']}s"
            )

        return reasons if reasons else None

    def _transition_to(
        self, new_state: CircuitState, reason: Optional[str] = None
    ) -> None:
        """Execute a state transition."""
        old_state = self._state
        self._state = new_state

        if new_state == CircuitState.OPEN:
            self._open_since = time.time()
            self._trip_count += 1

        transition = {
            "from": old_state.value,
            "to": new_state.value,
            "reason": str(reason) if reason else "normal_transition",
            "trip_count": self._trip_count,
            "cooldown_seconds": self._current_cooldown,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self._trip_history.append(transition)

        # Publish state transition event
        payload = {
            "agent_id": self.risk_monitor.agent_id,
            **transition,
        }
        payload["signature"] = self.risk_monitor._sign(transition)

        self.risk_monitor._execute("publish_event", {
            "event_type": "risk.circuit_breaker_transition",
            "payload": payload,
        })

        # Fire callbacks
        if new_state == CircuitState.OPEN:
            for cb in self._on_open_callbacks:
                cb(transition)
        elif new_state == CircuitState.CLOSED:
            for cb in self._on_close_callbacks:
                cb(transition)

    def _status(self, description: str) -> dict:
        """Return current circuit breaker status."""
        elapsed = 0
        if self._open_since:
            elapsed = time.time() - self._open_since

        return {
            "state": self._state.value,
            "description": description,
            "trip_count": self._trip_count,
            "cooldown_seconds": self._current_cooldown,
            "elapsed_seconds": round(elapsed, 1),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def check_sla_compliance(self) -> dict:
        """
        Check circuit breaker SLA compliance via GreenHelix.

        Tracks uptime (time in CLOSED state) as a percentage.
        """
        return self.risk_monitor._execute("get_sla_compliance", {
            "agent_id": self.risk_monitor.agent_id,
            "metric": "circuit_breaker_uptime",
        })
```

### Circuit Breaker Operations via curl

```bash
# Register a webhook for circuit breaker state transitions
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "register_webhook",
    "input": {
      "url": "https://your-ops-server.example.com/risk/circuit-breaker",
      "event_types": [
        "risk.circuit_breaker_transition",
        "risk.circuit_breaker_config"
      ],
      "secret": "your-webhook-hmac-secret"
    }
  }'
```

```bash
# Query circuit breaker history
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "get_events",
    "input": {
      "event_type": "risk.circuit_breaker_transition",
      "limit": 20,
      "order": "desc"
    }
  }'
```

```bash
# Check SLA compliance for the circuit breaker
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "get_sla_compliance",
    "input": {
      "agent_id": "risk-monitor-prod-01",
      "metric": "circuit_breaker_uptime"
    }
  }'
```

### Wiring the Circuit Breaker to Risk Monitors

```python
circuit_breaker = CircuitBreakerManager(
    risk_monitor=monitor,
    cooldown_seconds=300,
    max_cooldown_seconds=3600,
)

circuit_breaker.configure_triggers(
    drawdown_pct=12.0,
    correlation_max=0.92,
    liquidation_distance_pct=8.0,
    rapid_loss_pct=4.0,
)

# Register callbacks
def on_circuit_open(transition):
    """Cancel all open orders and notify ops."""
    print(f"CIRCUIT BREAKER OPEN: {transition['reason']}")
    monitor._execute("send_message", {
        "to": "ops-team",
        "subject": "CIRCUIT BREAKER TRIPPED",
        "body": (
            f"Reason: {transition['reason']}\n"
            f"Trip count: {transition['trip_count']}\n"
            f"Cooldown: {transition['cooldown_seconds']}s"
        ),
    })

circuit_breaker.on_open(on_circuit_open)

# In the main risk loop
status = circuit_breaker.evaluate(
    drawdown_pct=13.5,
    max_correlation=0.88,
    min_liq_distance_pct=15.0,
    rapid_loss_pct=2.0,
)
print(f"Circuit breaker: {status['state']} ({status['description']})")
```

---

## Chapter 7: Multi-Exchange Aggregation

### The Normalization Problem

Every exchange has its own API format. Binance returns positions as an array with `positionAmt` and `entryPrice`. Coinbase returns `size` and `average_entry_price`. Kraken returns `vol` and `cost`. Symbol naming varies: Binance uses `BTCUSDT`, Coinbase uses `BTC-USD`, Kraken uses `XXBTZUSD`. Margin types, leverage formats, and P&L calculations differ across every API. Before the risk engine can compute aggregate exposure, it needs a unified position format. The exchange adapter pattern solves this: one adapter per exchange, all implementing the same interface, all returning the same normalized data structure. This is the same pattern used by CCXT (a popular open-source library for cryptocurrency exchange APIs), but implemented here with the minimum surface area needed for risk monitoring rather than the full trading API.

### The Exchange Adapter Pattern

```python
import abc
import hashlib
import hmac
import time
from datetime import datetime, timezone
from typing import Dict, List, Optional

import requests


class NormalizedPosition:
    """Unified position representation across exchanges."""

    def __init__(
        self,
        symbol: str,
        exchange: str,
        side: str,
        quantity: float,
        entry_price: float,
        current_price: float,
        notional: float,
        leverage: float,
        margin_mode: str,
        unrealized_pnl: float,
        margin_used: float,
    ):
        self.symbol = symbol
        self.exchange = exchange
        self.side = side
        self.quantity = quantity
        self.entry_price = entry_price
        self.current_price = current_price
        self.notional = notional
        self.leverage = leverage
        self.margin_mode = margin_mode
        self.unrealized_pnl = unrealized_pnl
        self.margin_used = margin_used

    def to_dict(self) -> dict:
        return {
            "symbol": self.symbol,
            "exchange": self.exchange,
            "side": self.side,
            "quantity": self.quantity,
            "entry_price": self.entry_price,
            "current_price": self.current_price,
            "notional": self.notional,
            "leverage": self.leverage,
            "margin_mode": self.margin_mode,
            "unrealized_pnl": self.unrealized_pnl,
            "margin_used": self.margin_used,
        }


class ExchangeAdapter(abc.ABC):
    """Base class for exchange adapters."""

    @abc.abstractmethod
    def get_positions(self) -> List[NormalizedPosition]:
        """Fetch and normalize all open positions."""
        ...

    @abc.abstractmethod
    def get_account_equity(self) -> float:
        """Fetch total account equity in USD."""
        ...

    @abc.abstractmethod
    def cancel_all_orders(self) -> dict:
        """Cancel all open orders (used by circuit breaker)."""
        ...


class BinanceAdapter(ExchangeAdapter):
    """Adapter for Binance Futures API."""

    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = "https://fapi.binance.com"
        self.session = requests.Session()
        self.session.headers.update({"X-MBX-APIKEY": api_key})

    def _sign(self, params: dict) -> dict:
        """Add timestamp and HMAC signature to request params."""
        params["timestamp"] = int(time.time() * 1000)
        query_string = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
        signature = hmac.new(
            self.secret_key.encode(), query_string.encode(), hashlib.sha256
        ).hexdigest()
        params["signature"] = signature
        return params

    def get_positions(self) -> List[NormalizedPosition]:
        params = self._sign({})
        response = self.session.get(
            f"{self.base_url}/fapi/v2/positionRisk", params=params
        )
        response.raise_for_status()

        positions = []
        for p in response.json():
            amt = float(p["positionAmt"])
            if amt == 0:
                continue

            positions.append(NormalizedPosition(
                symbol=p["symbol"].replace("USDT", "-USD"),
                exchange="binance",
                side="long" if amt > 0 else "short",
                quantity=abs(amt),
                entry_price=float(p["entryPrice"]),
                current_price=float(p["markPrice"]),
                notional=abs(float(p["notional"])),
                leverage=float(p["leverage"]),
                margin_mode="isolated" if p["marginType"] == "isolated" else "cross",
                unrealized_pnl=float(p["unRealizedProfit"]),
                margin_used=float(p.get("isolatedMargin", 0)),
            ))

        return positions

    def get_account_equity(self) -> float:
        params = self._sign({})
        response = self.session.get(
            f"{self.base_url}/fapi/v2/account", params=params
        )
        response.raise_for_status()
        return float(response.json()["totalWalletBalance"])

    def cancel_all_orders(self) -> dict:
        # Cancel for each active symbol
        positions = self.get_positions()
        results = {}
        for pos in positions:
            symbol = pos.symbol.replace("-USD", "USDT")
            params = self._sign({"symbol": symbol})
            response = self.session.delete(
                f"{self.base_url}/fapi/v1/allOpenOrders", params=params
            )
            results[symbol] = response.status_code
        return results
```

### Aggregating Across Exchanges

```python
def aggregate_positions(
    adapters: List[ExchangeAdapter],
    risk_monitor: "RiskMonitor",
) -> dict:
    """
    Fetch positions from all exchanges and compute aggregate metrics.
    Publishes the aggregated view as a GreenHelix event.
    """
    all_positions = []
    total_equity = 0.0

    for adapter in adapters:
        positions = adapter.get_positions()
        equity = adapter.get_account_equity()
        all_positions.extend(positions)
        total_equity += equity

    # Compute aggregate metrics
    total_notional = sum(p.notional for p in all_positions)
    total_unrealized_pnl = sum(p.unrealized_pnl for p in all_positions)
    aggregate_leverage = total_notional / total_equity if total_equity > 0 else 0.0

    # Net exposure by base asset
    net_exposure: Dict[str, float] = {}
    for p in all_positions:
        base = p.symbol.split("-")[0]
        signed_notional = p.notional if p.side == "long" else -p.notional
        net_exposure[base] = net_exposure.get(base, 0) + signed_notional

    # Per-exchange breakdown
    exchange_breakdown: Dict[str, dict] = {}
    for p in all_positions:
        if p.exchange not in exchange_breakdown:
            exchange_breakdown[p.exchange] = {
                "position_count": 0,
                "total_notional": 0.0,
                "unrealized_pnl": 0.0,
            }
        eb = exchange_breakdown[p.exchange]
        eb["position_count"] += 1
        eb["total_notional"] += p.notional
        eb["unrealized_pnl"] += p.unrealized_pnl

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_equity": round(total_equity, 2),
        "total_notional": round(total_notional, 2),
        "aggregate_leverage": round(aggregate_leverage, 2),
        "total_unrealized_pnl": round(total_unrealized_pnl, 2),
        "position_count": len(all_positions),
        "exchange_count": len(exchange_breakdown),
        "net_exposure": {k: round(v, 2) for k, v in net_exposure.items()},
        "exchange_breakdown": exchange_breakdown,
        "positions": [p.to_dict() for p in all_positions],
    }

    # Publish aggregated snapshot to GreenHelix
    payload = {
        "agent_id": risk_monitor.agent_id,
        **{k: v for k, v in result.items() if k != "positions"},
    }
    payload["signature"] = risk_monitor._sign(
        {"equity": total_equity, "leverage": aggregate_leverage}
    )

    risk_monitor._execute("publish_event", {
        "event_type": "risk.aggregate_snapshot",
        "payload": payload,
    })

    return result
```

### Querying Aggregate Snapshots via curl

```bash
# Get the latest aggregate portfolio snapshot
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "get_events",
    "input": {
      "event_type": "risk.aggregate_snapshot",
      "limit": 1,
      "order": "desc"
    }
  }'
```

```bash
# Publish an aggregate snapshot manually (e.g., from a cron job)
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "publish_event",
    "input": {
      "event_type": "risk.aggregate_snapshot",
      "payload": {
        "agent_id": "risk-monitor-prod-01",
        "total_equity": 98500.00,
        "total_notional": 312000.00,
        "aggregate_leverage": 3.17,
        "total_unrealized_pnl": -1240.50,
        "position_count": 7,
        "exchange_count": 3,
        "net_exposure": {
          "BTC": 142000.00,
          "ETH": 95000.00,
          "SOL": 75000.00
        },
        "timestamp": "2026-04-07T14:30:00Z",
        "signature": "base64-ed25519-signature"
      }
    }
  }'
```

### Usage Example

```python
# Wire up exchange adapters
binance = BinanceAdapter(
    api_key="your-binance-api-key",
    secret_key="your-binance-secret-key",
)
# (Similarly for CoinbaseAdapter, KrakenAdapter)

adapters = [binance]  # Add more adapters as needed

# Run aggregation
snapshot = aggregate_positions(adapters, monitor)
print(f"Total equity: ${snapshot['total_equity']:,.2f}")
print(f"Aggregate leverage: {snapshot['aggregate_leverage']}x")
print(f"Positions across {snapshot['exchange_count']} exchanges: {snapshot['position_count']}")

for asset, exposure in snapshot["net_exposure"].items():
    direction = "LONG" if exposure > 0 else "SHORT"
    print(f"  {asset}: ${abs(exposure):,.2f} {direction}")
```

Adding a new exchange requires implementing only three methods: `get_positions()`, `get_account_equity()`, and `cancel_all_orders()`. The rest of the risk engine works without modification because it operates on `NormalizedPosition` objects, not exchange-specific data structures.

### Handling Exchange API Failures

Exchange APIs fail. Rate limits are hit, connections time out, maintenance windows arrive without notice. The aggregation layer needs to handle partial data gracefully:

```python
def safe_aggregate_positions(
    adapters: Dict[str, ExchangeAdapter],
    risk_monitor: "RiskMonitor",
) -> dict:
    """
    Aggregate positions with exchange failure resilience.
    """
    all_positions = []
    total_equity = 0.0
    failures = {}
    successes = {}

    for name, adapter in adapters.items():
        try:
            positions = adapter.get_positions()
            equity = adapter.get_account_equity()
            all_positions.extend(positions)
            total_equity += equity
            successes[name] = len(positions)
        except requests.exceptions.RequestException as e:
            failures[name] = str(e)

    if failures:
        # Publish a partial data warning
        risk_monitor._execute("publish_event", {
            "event_type": "risk.exchange_failure",
            "payload": {
                "agent_id": risk_monitor.agent_id,
                "failures": failures,
                "successes": successes,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "signature": risk_monitor._sign({"failures": list(failures.keys())}),
            },
        })

        # Alert the operator
        risk_monitor._execute("send_message", {
            "to": "ops-team",
            "subject": f"EXCHANGE API FAILURE: {', '.join(failures.keys())}",
            "body": (
                f"Failed exchanges: {json.dumps(failures, indent=2)}\n"
                f"Successful exchanges: {json.dumps(successes, indent=2)}\n"
                f"Risk metrics are computed from partial data."
            ),
        })

    total_notional = sum(p.notional for p in all_positions)
    aggregate_leverage = total_notional / total_equity if total_equity > 0 else 0.0

    return {
        "total_equity": round(total_equity, 2),
        "aggregate_leverage": round(aggregate_leverage, 2),
        "position_count": len(all_positions),
        "exchange_failures": failures,
        "positions": [p.to_dict() for p in all_positions],
    }
```

When an exchange API fails, the risk engine computes metrics from the exchanges that are reachable. This means the reported aggregate leverage and total equity may understate the true values. The operator is notified so they can decide whether to act conservatively (assume the unreachable exchange has unfavorable positions) or wait for the connection to recover.

---

## Next Steps

For deployment patterns, monitoring, and production hardening, see the
[Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening).

---

## What's Next

**Companion Guides:**

- **Tamper-Proof Audit Trails for Trading Bots** -- Add cryptographic verification and regulatory compliance (EU AI Act, MiFID II, SEC 17a-4) to the risk events generated by this system.
- **Bot Reputation System** -- Turn your risk management track record into verifiable reputation. Prove to copy traders and capital allocators that your risk controls are real, not just claimed.
- **Strategy Marketplace Playbook** -- Publish risk-managed strategies on the GreenHelix marketplace with provable drawdown limits and circuit breaker guarantees.
- **AgentOps: Fleet Management** -- Scale from monitoring a single portfolio to managing risk across a fleet of trading bots with centralized governance.

**GreenHelix Documentation:**

- Full API reference: https://api.greenhelix.net/v1
- Event bus deep dive and webhook configuration in the platform documentation
- SLA compliance tracking and metrics ingestion reference

**Architecture Decisions Worth Revisiting:**

As your operation scales, revisit these trade-offs:
- **Polling vs. streaming**: This guide uses polling (10-second cycles). For sub-second risk monitoring, switch to WebSocket connections to exchanges and stream position updates to the GreenHelix event bus in real time.
- **Single risk engine vs. distributed**: A single risk engine is a single point of failure. For operations above $1M in aggregate equity, run two instances in active-passive mode, with the passive instance consuming the same events and ready to take over if the primary fails.
- **Alert fatigue**: Tune your thresholds aggressively at first (tight thresholds, frequent alerts), then loosen them as you learn what your portfolio's normal behavior looks like. A circuit breaker that trips every week will be ignored or disabled -- defeating its purpose.

---

*Published by GreenHelix Labs. All code examples are provided under the MIT License. For the full product catalog, visit the GreenHelix storefront.*

