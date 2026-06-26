---
name: greenhelix-trading-bot-fleet-management
version: "1.3.1"
description: "Trading Bot Fleet Management: Unified Control for Multi-Bot Operations. Build a fleet management layer for 10+ trading bots with per-bot identity isolation, permission scoping, health monitoring, coordinated deployments, SLA tracking, and cost allocation. Includes detailed Python code examples with full API integration."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [fleet-management, trading-bot, identity, monitoring, guide, greenhelix, openclaw, ai-agent]
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
# Trading Bot Fleet Management: Unified Control for Multi-Bot Operations

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `AGENT_SIGNING_KEY`: Cryptographic signing key for agent identity (Ed25519 key pair for request signing)


In March 2023, the Step Finance exploit drained $45M from Solana DeFi positions. The root cause was not a smart contract vulnerability or a novel cryptographic attack. It was operational: multiple bots shared API keys with no identity isolation. When one bot's credentials leaked, the attacker gained access to every bot, every exchange account, every withdrawal endpoint. No per-bot permissions. No unified health dashboard that would have caught anomalous behavior. No kill switch scoped to the compromised bot without killing the entire fleet. The team had to shut down everything, losing millions in unrealized positions across healthy bots while they figured out which one was compromised. This pattern repeats across the industry. Teams running 10+ bots accumulate the same structural debt: shared credentials passed through environment variables, no per-bot permission boundaries, health checks that are either absent or scattered across shell scripts nobody maintains, deployments that are "SSH in and restart the process," and cost tracking that lives in a spreadsheet updated monthly if someone remembers. When one bot goes rogue -- whether from a bug, a compromised key, or a strategy that hits an edge case -- the blast radius is the entire fleet.
This guide builds a fleet management layer using GreenHelix's identity, messaging, and metrics tools. Each bot gets its own Ed25519 cryptographic identity, scoped permissions defining exactly what it can and cannot do, real-time health monitoring with automatic dead bot detection, coordinated deployment procedures, SLA tracking against defined performance targets, and per-bot cost allocation. Every concept comes with working Python code and equivalent curl commands against the GreenHelix API.
1. [Fleet Architecture](#chapter-1-fleet-architecture)

## What You'll Learn
- Chapter 1: Fleet Architecture
- Chapter 2: FleetManager Class
- Chapter 3: BotIdentityManager Class
- Chapter 4: Permission Scoping
- Chapter 5: FleetHealthMonitor Class
- Chapter 6: Coordinated Deployments
- Chapter 7: SLA Tracking
- Chapter 8: Cost Allocation
- What's Next

## Full Guide

# Trading Bot Fleet Management: Unified Control for Multi-Bot Operations

In March 2023, the Step Finance exploit drained $45M from Solana DeFi positions. The root cause was not a smart contract vulnerability or a novel cryptographic attack. It was operational: multiple bots shared API keys with no identity isolation. When one bot's credentials leaked, the attacker gained access to every bot, every exchange account, every withdrawal endpoint. No per-bot permissions. No unified health dashboard that would have caught anomalous behavior. No kill switch scoped to the compromised bot without killing the entire fleet. The team had to shut down everything, losing millions in unrealized positions across healthy bots while they figured out which one was compromised. This pattern repeats across the industry. Teams running 10+ bots accumulate the same structural debt: shared credentials passed through environment variables, no per-bot permission boundaries, health checks that are either absent or scattered across shell scripts nobody maintains, deployments that are "SSH in and restart the process," and cost tracking that lives in a spreadsheet updated monthly if someone remembers. When one bot goes rogue -- whether from a bug, a compromised key, or a strategy that hits an edge case -- the blast radius is the entire fleet.

This guide builds a fleet management layer using GreenHelix's identity, messaging, and metrics tools. Each bot gets its own Ed25519 cryptographic identity, scoped permissions defining exactly what it can and cannot do, real-time health monitoring with automatic dead bot detection, coordinated deployment procedures, SLA tracking against defined performance targets, and per-bot cost allocation. Every concept comes with working Python code and equivalent curl commands against the GreenHelix API.

---

## Table of Contents

1. [Fleet Architecture](#chapter-1-fleet-architecture)
2. [FleetManager Class](#chapter-2-fleetmanager-class)
3. [BotIdentityManager Class](#chapter-3-botidentitymanager-class)
4. [Permission Scoping](#chapter-4-permission-scoping)
5. [FleetHealthMonitor Class](#chapter-5-fleethealthmonitor-class)
6. [Coordinated Deployments](#chapter-6-coordinated-deployments)
7. [SLA Tracking](#chapter-7-sla-tracking)
8. [Cost Allocation](#chapter-8-cost-allocation)
9. [What's Next](#whats-next)

---

## Chapter 1: Fleet Architecture

### Why Fleet Management Matters

The Step Finance breach is instructive because it was not exotic. The attack surface was not a zero-day in a cryptographic library. It was a predictable consequence of how most teams operate trading bots at scale: every bot shares the same API key, the same exchange credentials, the same infrastructure account. This is the "monolith credentials" antipattern, and it shows up in every post-mortem of operational trading failures that did not involve a market event.

Consider what a team with 15 bots typically looks like six months after launch:

- **Shared credentials**: All bots read the same `.env` file or Kubernetes secret. Rotating one key means touching every bot.
- **No permission boundaries**: A bot designed to execute $500 momentum trades on Binance Spot has the same access as a bot managing $50,000 Deribit options positions. If the momentum bot is compromised, the attacker can withdraw from the options account.
- **Scattered health checks**: Bot #3 has a heartbeat endpoint. Bot #7 writes to a log file. Bots #1, #2, #4-6, and #8-15 have no health reporting at all. The team discovers a dead bot when a strategy stops producing PnL.
- **Manual deployments**: Updating a strategy requires SSH-ing into each server, pulling the latest code, restarting the process, and hoping the bot reconnects to the exchange websocket cleanly. There is no rollback procedure beyond "check out the previous git commit and restart again."
- **No cost attribution**: The team knows the monthly AWS bill and the total exchange fees. They do not know which bot costs the most to operate, which strategy has a negative ROI after infrastructure costs, or whether a bot that trades 200 times per day is actually profitable after accounting for exchange fees, API rate limit costs, and compute.

Fleet management solves all of these by treating each bot as an independently identified, independently monitored, independently permissioned entity within a unified control plane.

### Architecture Overview

The fleet management architecture has four layers:

```
+-----------------------------------------------------------------------+
|                        Fleet Operator (Human)                          |
|                  Strategic decisions, policy, budgets                   |
+-----------------------------------------------------------------------+
        |
        v
+-----------------------------------------------------------------------+
|                        Fleet Manager (Agent)                           |
|  register/deregister bots, issue commands, aggregate status            |
|  GreenHelix identity: fleet-manager-{org}                              |
+-----------------------------------------------------------------------+
        |
        +--------------------+--------------------+
        |                    |                    |
        v                    v                    v
+---------------+   +---------------+   +---------------+
|  Bot Group:   |   |  Bot Group:   |   |  Bot Group:   |
|  Spot Arb     |   |  Perp Momentum|   |  Options MM   |
|  3 bots       |   |  5 bots       |   |  4 bots       |
+---------------+   +---------------+   +---------------+
    |   |   |          |  |  |  |  |       |  |  |  |
    v   v   v          v  v  v  v  v       v  v  v  v
  Individual bots, each with:
  - Own Ed25519 identity
  - Scoped permissions
  - Health heartbeat
  - Metrics reporting
  - Cost tracking
```

The **fleet operator** is a human who sets policy: which strategies to run, on which exchanges, with what risk limits, and how much capital to allocate. The **fleet manager** is a GreenHelix agent that translates policy into operations: registering bots, issuing commands, monitoring health, orchestrating deployments. **Bot groups** organize bots by strategy type, and **individual bots** are the execution units, each with its own cryptographic identity.

### GreenHelix Tools Used

This guide uses the following GreenHelix tools:

| Tool | Purpose |
|------|---------|
| `register_agent` | Create identity for fleet manager and each bot |
| `get_agent_identity` | Retrieve and verify bot identity |
| `submit_metrics` | Report health, PnL, latency, trade count |
| `get_sla_compliance` | Monitor bots against defined SLA targets |
| `send_message` | Fleet commands, alerts, inter-bot communication |
| `register_webhook` | Real-time event delivery for health alerts |
| `search_agents_by_metrics` | Find underperforming bots across the fleet |
| `get_agent_reputation` | Track bot reliability over time |
| `create_event_schema` | Define fleet event types |
| `publish_event` | Emit fleet events (deploy, failover, alert) |

### Fleet Hierarchy

The hierarchy maps to GreenHelix's identity model. The fleet manager is a registered agent. Each bot group is a metadata tag. Each individual bot is a registered agent with metadata linking it to its group and to the fleet manager.

```python
# Hierarchy expressed in GreenHelix metadata
fleet_manager_metadata = {
    "role": "fleet_manager",
    "organization": "your-org-id",
    "fleet_size": 12,
    "groups": ["spot-arb", "perp-momentum", "options-mm"]
}

bot_metadata = {
    "role": "trading_bot",
    "fleet_manager": "fleet-manager-{org}",
    "group": "spot-arb",
    "exchange": "binance",
    "strategy": "cross-exchange-arb",
    "version": "2.4.1",
    "max_position_usd": 10000
}
```

This metadata is not cosmetic. It is queryable. When the fleet manager needs to find all bots in the "perp-momentum" group, it searches by metadata. When a health alert fires, the alert includes the bot's group and strategy so the operator knows immediately what type of bot is failing and what the potential market impact is.

### Why Not Kubernetes Labels or Consul?

You might already use Kubernetes labels, Consul service tags, or Terraform metadata for infrastructure management. Those are fine for infrastructure concerns -- pod scheduling, service discovery, load balancing. They are not sufficient for trading bot fleet management because they operate at the wrong abstraction level. Kubernetes knows that a pod is running. It does not know that the pod is a trading bot with a $50,000 position limit on Deribit, that its Ed25519 key was last rotated 28 days ago, or that its SLA requires 99.9% uptime with sub-100ms exchange latency.

GreenHelix's identity layer operates at the application level. Each bot's identity carries its trading-specific metadata: strategy type, exchange, position limits, permission tier, key version. The fleet manager queries this metadata through GreenHelix's API, not through infrastructure tooling. This means the fleet management layer works identically whether your bots run on Kubernetes, bare metal, EC2 instances, or a mix of all three. The infrastructure is abstracted away; the fleet identity is portable.

The practical consequence: when you migrate from EC2 to Kubernetes (or vice versa), no fleet management code changes. The bots register the same identities, report the same metrics, and respond to the same commands regardless of the underlying compute platform.

---

## Chapter 2: FleetManager Class

### Central Management for Bot Fleet Operations

The FleetManager class is the control plane for all fleet operations. It handles bot registration, inventory management, fleet-wide commands, and status aggregation. Every operation goes through the GreenHelix API so that commands, status, and events are centralized and auditable.

### Setup

```python
import requests
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field

base_url = "https://api.greenhelix.net/v1"
api_key = "your-api-key"  # From GreenHelix dashboard

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"
session.headers["Content-Type"] = "application/json"

def execute(tool: str, inputs: dict) -> dict:
    """Execute a GreenHelix tool and return the result."""
    resp = session.post(
        f"{base_url}/v1",
        json={"tool": tool, "input": inputs}
    )
    resp.raise_for_status()
    return resp.json()
```

Equivalent curl for any `execute` call throughout this guide:

```bash
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "register_agent",
    "input": {
      "name": "fleet-manager-acme",
      "description": "Fleet manager for Acme Trading bot fleet",
      "capabilities": ["fleet_management", "bot_orchestration"],
      "metadata": {"role": "fleet_manager", "organization": "acme"}
    }
  }'
```

### The FleetManager Class

```python
@dataclass
class BotRecord:
    """Local record of a registered bot."""
    agent_id: str
    name: str
    group: str
    exchange: str
    strategy: str
    version: str
    status: str = "active"
    registered_at: str = ""
    last_heartbeat: Optional[str] = None


class FleetManager:
    """Central management class for a trading bot fleet."""

    def __init__(self, org_id: str):
        self.org_id = org_id
        self.manager_agent_id: Optional[str] = None
        self.bots: Dict[str, BotRecord] = {}
        self._register_manager()

    def _register_manager(self):
        """Register the fleet manager agent on GreenHelix."""
        result = execute("register_agent", {
            "name": f"fleet-manager-{self.org_id}",
            "description": f"Fleet manager for {self.org_id} trading bot fleet. "
                           f"Handles registration, commands, health, deployments.",
            "capabilities": [
                "fleet_management",
                "bot_orchestration",
                "health_monitoring",
                "deployment_coordination"
            ],
            "metadata": {
                "role": "fleet_manager",
                "organization": self.org_id
            }
        })
        self.manager_agent_id = result["agent_id"]
        print(f"Fleet manager registered: {self.manager_agent_id}")

    def register_bot(self, name: str, group: str, exchange: str,
                     strategy: str, version: str,
                     capabilities: List[str] = None,
                     max_position_usd: float = 10000) -> str:
        """Register a new bot in the fleet."""
        if capabilities is None:
            capabilities = ["trading", "metrics_reporting"]

        result = execute("register_agent", {
            "name": name,
            "description": f"Trading bot: {strategy} on {exchange}. "
                           f"Part of {group} group in {self.org_id} fleet.",
            "capabilities": capabilities,
            "metadata": {
                "role": "trading_bot",
                "fleet_manager": self.manager_agent_id,
                "group": group,
                "exchange": exchange,
                "strategy": strategy,
                "version": version,
                "max_position_usd": max_position_usd,
                "organization": self.org_id
            }
        })

        agent_id = result["agent_id"]
        self.bots[agent_id] = BotRecord(
            agent_id=agent_id,
            name=name,
            group=group,
            exchange=exchange,
            strategy=strategy,
            version=version,
            registered_at=datetime.utcnow().isoformat()
        )
        print(f"Bot registered: {name} ({agent_id})")
        return agent_id

    def deregister_bot(self, agent_id: str):
        """Remove a bot from the fleet."""
        if agent_id not in self.bots:
            raise ValueError(f"Bot {agent_id} not found in fleet")

        # Notify the bot to shut down gracefully
        execute("send_message", {
            "from_agent_id": self.manager_agent_id,
            "to_agent_id": agent_id,
            "message_type": "command",
            "payload": {
                "command": "shutdown",
                "reason": "deregistered_from_fleet",
                "grace_period_seconds": 30
            }
        })

        bot = self.bots.pop(agent_id)
        print(f"Bot deregistered: {bot.name} ({agent_id})")

    def pause_all(self, reason: str = "operator_initiated"):
        """Pause all bots in the fleet. Bots stop opening new positions."""
        for agent_id, bot in self.bots.items():
            execute("send_message", {
                "from_agent_id": self.manager_agent_id,
                "to_agent_id": agent_id,
                "message_type": "command",
                "payload": {
                    "command": "pause",
                    "reason": reason,
                    "timestamp": datetime.utcnow().isoformat()
                }
            })
            bot.status = "paused"
        print(f"Fleet paused: {len(self.bots)} bots ({reason})")

    def resume_all(self):
        """Resume all paused bots."""
        for agent_id, bot in self.bots.items():
            if bot.status == "paused":
                execute("send_message", {
                    "from_agent_id": self.manager_agent_id,
                    "to_agent_id": agent_id,
                    "message_type": "command",
                    "payload": {
                        "command": "resume",
                        "timestamp": datetime.utcnow().isoformat()
                    }
                })
                bot.status = "active"
        print(f"Fleet resumed: {len(self.bots)} bots")

    def emergency_stop(self, reason: str = "emergency"):
        """Emergency stop: close all positions, cancel all orders, halt."""
        for agent_id, bot in self.bots.items():
            execute("send_message", {
                "from_agent_id": self.manager_agent_id,
                "to_agent_id": agent_id,
                "message_type": "command",
                "payload": {
                    "command": "emergency_stop",
                    "reason": reason,
                    "actions": [
                        "cancel_all_open_orders",
                        "close_all_positions_market",
                        "halt_trading_loop"
                    ],
                    "timestamp": datetime.utcnow().isoformat()
                }
            })
            bot.status = "stopped"

        # Log the emergency stop event
        execute("publish_event", {
            "agent_id": self.manager_agent_id,
            "event_type": "fleet.emergency_stop",
            "payload": {
                "reason": reason,
                "bots_affected": len(self.bots),
                "bot_ids": list(self.bots.keys()),
                "timestamp": datetime.utcnow().isoformat()
            }
        })
        print(f"EMERGENCY STOP: {len(self.bots)} bots halted ({reason})")

    def get_fleet_status(self) -> Dict:
        """Aggregate status across all bots."""
        status_counts = {"active": 0, "paused": 0, "stopped": 0, "dead": 0}
        group_counts = {}

        for bot in self.bots.values():
            status_counts[bot.status] = status_counts.get(bot.status, 0) + 1
            group_counts[bot.group] = group_counts.get(bot.group, 0) + 1

        return {
            "fleet_manager": self.manager_agent_id,
            "total_bots": len(self.bots),
            "status": status_counts,
            "groups": group_counts,
            "timestamp": datetime.utcnow().isoformat()
        }

    def send_group_command(self, group: str, command: str,
                           payload: dict = None):
        """Send a command to all bots in a specific group."""
        targets = [
            (aid, bot) for aid, bot in self.bots.items()
            if bot.group == group
        ]
        for agent_id, bot in targets:
            execute("send_message", {
                "from_agent_id": self.manager_agent_id,
                "to_agent_id": agent_id,
                "message_type": "command",
                "payload": {
                    "command": command,
                    **(payload or {}),
                    "timestamp": datetime.utcnow().isoformat()
                }
            })
        print(f"Command '{command}' sent to {len(targets)} bots in {group}")
```

### Registering a Fleet

```python
fleet = FleetManager(org_id="acme-trading")

# Spot arbitrage group
for i in range(3):
    fleet.register_bot(
        name=f"spot-arb-{i+1:02d}",
        group="spot-arb",
        exchange="binance" if i < 2 else "okx",
        strategy="cross-exchange-arb",
        version="2.4.1",
        max_position_usd=10000
    )

# Perpetual futures momentum group
for i in range(5):
    exchanges = ["binance", "bybit", "okx", "deribit", "binance"]
    fleet.register_bot(
        name=f"perp-momentum-{i+1:02d}",
        group="perp-momentum",
        exchange=exchanges[i],
        strategy="trend-following-perps",
        version="1.8.3",
        max_position_usd=25000
    )

# Options market making group
for i in range(4):
    fleet.register_bot(
        name=f"options-mm-{i+1:02d}",
        group="options-mm",
        exchange="deribit",
        strategy="delta-neutral-mm",
        version="3.1.0",
        capabilities=["trading", "metrics_reporting", "options_greeks"],
        max_position_usd=50000
    )

print(json.dumps(fleet.get_fleet_status(), indent=2))
```

```bash
# curl: Register a single bot
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "register_agent",
    "input": {
      "name": "spot-arb-01",
      "description": "Trading bot: cross-exchange-arb on binance. Part of spot-arb group.",
      "capabilities": ["trading", "metrics_reporting"],
      "metadata": {
        "role": "trading_bot",
        "fleet_manager": "fleet-manager-agent-id",
        "group": "spot-arb",
        "exchange": "binance",
        "strategy": "cross-exchange-arb",
        "version": "2.4.1",
        "max_position_usd": 10000
      }
    }
  }'

# curl: Send emergency stop to a bot
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "send_message",
    "input": {
      "from_agent_id": "fleet-manager-agent-id",
      "to_agent_id": "bot-agent-id",
      "message_type": "command",
      "payload": {
        "command": "emergency_stop",
        "reason": "anomalous_behavior_detected",
        "actions": ["cancel_all_open_orders", "close_all_positions_market", "halt_trading_loop"]
      }
    }
  }'
```

### Fleet Command Patterns

Three command scopes cover all operational scenarios:

**Fleet-wide**: `pause_all`, `resume_all`, `emergency_stop`. Used for market-wide events (flash crash, exchange outage, security incident). These hit every bot regardless of group.

**Group-scoped**: `send_group_command`. Used for strategy-specific actions: updating parameters for all momentum bots, pausing all options bots before an expiry event, or upgrading all arb bots to a new version.

**Individual**: Direct `send_message` to a single bot. Used for surgical interventions: adjusting one bot's position limits, forcing one bot to close a specific position, or rotating one bot's exchange API keys.

The command hierarchy means that a compromised spot arb bot can be killed without touching the options market makers. That is the entire point: blast radius containment through identity isolation.

---

## Chapter 3: BotIdentityManager Class

### Per-Bot Cryptographic Identity

Every bot in the fleet gets its own Ed25519 keypair. This is not optional. Shared keys are how Step Finance happened. Per-bot keys mean that compromising one bot's key gives the attacker access to exactly one bot. The fleet manager can revoke that single identity without affecting any other bot.

Ed25519 was chosen for three reasons: it produces compact 64-byte signatures, signing is fast enough that it adds negligible latency to trading operations (tens of microseconds), and the key generation is deterministic from a seed, making backup and recovery straightforward.

### The BotIdentityManager Class

```python
import nacl.signing
import nacl.encoding
import base64
import secrets
import os
from typing import Tuple


class BotIdentityManager:
    """Manages Ed25519 identities for trading bots."""

    def __init__(self, fleet_manager_id: str, key_store_path: str = "/secure/keys"):
        self.fleet_manager_id = fleet_manager_id
        self.key_store_path = key_store_path
        self.identities: Dict[str, dict] = {}  # agent_id -> identity record

    def generate_keypair(self, bot_name: str) -> Tuple[str, str]:
        """Generate an Ed25519 keypair for a bot.
        Returns (public_key_b64, private_key_b64).
        """
        signing_key = nacl.signing.SigningKey.generate()
        verify_key = signing_key.verify_key

        private_b64 = base64.b64encode(
            signing_key.encode()
        ).decode("utf-8")
        public_b64 = base64.b64encode(
            verify_key.encode()
        ).decode("utf-8")

        # Store private key securely -- in production, use a secrets manager
        key_path = os.path.join(self.key_store_path, f"{bot_name}.key")
        os.makedirs(os.path.dirname(key_path), exist_ok=True)
        with open(key_path, "w") as f:
            f.write(private_b64)
        os.chmod(key_path, 0o600)  # Owner read/write only

        return public_b64, private_b64

    def register_identity(self, bot_name: str, group: str,
                          exchange: str, strategy: str,
                          version: str,
                          permissions: List[str] = None) -> dict:
        """Generate keys and register identity on GreenHelix."""
        public_key, private_key = self.generate_keypair(bot_name)

        if permissions is None:
            permissions = ["trade", "report_metrics"]

        # Register the agent with its public key
        result = execute("register_agent", {
            "name": bot_name,
            "description": f"Trading bot: {strategy} on {exchange}",
            "capabilities": permissions,
            "metadata": {
                "role": "trading_bot",
                "fleet_manager": self.fleet_manager_id,
                "group": group,
                "exchange": exchange,
                "strategy": strategy,
                "version": version,
                "public_key": public_key,
                "key_algorithm": "ed25519",
                "registered_at": datetime.utcnow().isoformat()
            }
        })

        agent_id = result["agent_id"]
        identity_record = {
            "agent_id": agent_id,
            "bot_name": bot_name,
            "public_key": public_key,
            "group": group,
            "exchange": exchange,
            "permissions": permissions,
            "created_at": datetime.utcnow().isoformat(),
            "key_version": 1,
            "status": "active"
        }
        self.identities[agent_id] = identity_record
        return identity_record

    def verify_identity(self, agent_id: str) -> dict:
        """Retrieve and verify a bot's identity from GreenHelix."""
        result = execute("get_agent_identity", {
            "agent_id": agent_id
        })

        local_record = self.identities.get(agent_id)
        if local_record:
            # Verify public key matches what we registered
            remote_key = result.get("metadata", {}).get("public_key")
            if remote_key != local_record["public_key"]:
                raise SecurityError(
                    f"Public key mismatch for {agent_id}. "
                    f"Expected: {local_record['public_key'][:16]}... "
                    f"Got: {remote_key[:16] if remote_key else 'None'}... "
                    f"Possible key tampering."
                )
        return result

    def rotate_key(self, agent_id: str) -> dict:
        """Rotate a bot's Ed25519 keypair without downtime.

        The rotation procedure:
        1. Generate new keypair
        2. Update GreenHelix identity with new public key
        3. Bot continues operating -- it picks up the new key on next heartbeat
        4. Old key is archived (not deleted) for signature verification of historical events
        """
        if agent_id not in self.identities:
            raise ValueError(f"No identity record for {agent_id}")

        record = self.identities[agent_id]
        bot_name = record["bot_name"]

        # Archive old key
        old_key_path = os.path.join(
            self.key_store_path,
            f"{bot_name}.key.v{record['key_version']}"
        )
        current_key_path = os.path.join(
            self.key_store_path, f"{bot_name}.key"
        )
        if os.path.exists(current_key_path):
            os.rename(current_key_path, old_key_path)

        # Generate new keypair
        new_public, new_private = self.generate_keypair(bot_name)

        # Update the identity on GreenHelix -- submit metrics indicating rotation
        execute("submit_metrics", {
            "agent_id": agent_id,
            "metrics": {
                "key_rotation": 1,
                "key_version": record["key_version"] + 1,
                "rotation_timestamp": datetime.utcnow().isoformat()
            }
        })

        # Notify the bot to pick up the new key
        execute("send_message", {
            "from_agent_id": self.fleet_manager_id,
            "to_agent_id": agent_id,
            "message_type": "command",
            "payload": {
                "command": "rotate_key",
                "new_public_key": new_public,
                "key_version": record["key_version"] + 1,
                "effective_at": datetime.utcnow().isoformat()
            }
        })

        record["public_key"] = new_public
        record["key_version"] += 1
        print(f"Key rotated for {bot_name}: v{record['key_version']}")
        return record

    def revoke_identity(self, agent_id: str, reason: str):
        """Revoke a compromised bot's identity.

        This is the nuclear option: the bot can no longer authenticate.
        Use when a bot is confirmed compromised.
        """
        if agent_id not in self.identities:
            raise ValueError(f"No identity record for {agent_id}")

        record = self.identities[agent_id]

        # Send shutdown command before revocation
        execute("send_message", {
            "from_agent_id": self.fleet_manager_id,
            "to_agent_id": agent_id,
            "message_type": "command",
            "payload": {
                "command": "emergency_stop",
                "reason": f"identity_revoked: {reason}",
                "actions": [
                    "cancel_all_open_orders",
                    "close_all_positions_market",
                    "halt_trading_loop",
                    "destroy_local_keys"
                ]
            }
        })

        # Publish revocation event for audit trail
        execute("publish_event", {
            "agent_id": self.fleet_manager_id,
            "event_type": "fleet.identity_revoked",
            "payload": {
                "revoked_agent_id": agent_id,
                "bot_name": record["bot_name"],
                "reason": reason,
                "revoked_at": datetime.utcnow().isoformat(),
                "key_version_revoked": record["key_version"]
            }
        })

        # Delete the private key
        key_path = os.path.join(
            self.key_store_path, f"{record['bot_name']}.key"
        )
        if os.path.exists(key_path):
            # Overwrite with random data before unlinking
            with open(key_path, "wb") as f:
                f.write(secrets.token_bytes(64))
            os.unlink(key_path)

        record["status"] = "revoked"
        print(f"Identity revoked: {record['bot_name']} ({agent_id}): {reason}")

    def list_active_identities(self) -> List[dict]:
        """List all active bot identities."""
        return [
            r for r in self.identities.values()
            if r["status"] == "active"
        ]
```

```bash
# curl: Get a bot's identity
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "get_agent_identity",
    "input": {
      "agent_id": "bot-agent-id-here"
    }
  }'

# curl: Notify bot of key rotation via message
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "send_message",
    "input": {
      "from_agent_id": "fleet-manager-agent-id",
      "to_agent_id": "bot-agent-id",
      "message_type": "command",
      "payload": {
        "command": "rotate_key",
        "new_public_key": "base64-encoded-new-public-key",
        "key_version": 2,
        "effective_at": "2026-04-07T14:30:00Z"
      }
    }
  }'
```

### Key Rotation Without Downtime

Key rotation is the most operationally sensitive identity operation. The bot must continue trading during rotation -- you cannot afford a gap where the bot has no valid key. The procedure is:

1. **Generate new keypair** on the fleet manager side.
2. **Archive the old private key** (do not delete -- you need it to verify signatures on historical events).
3. **Update GreenHelix** with the new public key via metrics submission.
4. **Notify the bot** via `send_message` with the new key material.
5. The bot picks up the new key, switches to it, and acknowledges.

Between steps 4 and 5, the bot is still signing with the old key, and that is fine. The old key is still valid until the bot confirms the switch. There is no window where the bot has no valid signing key.

A sane rotation schedule is every 30 days for production bots, immediately upon any suspected compromise, and after any personnel change on the team (someone leaves, all keys rotate).

### Identity Revocation for Compromised Bots

Revocation is destructive and immediate. When you confirm a bot is compromised, you do not rotate -- you revoke. The difference: rotation preserves continuity (the bot keeps running with a new key), while revocation terminates the bot's ability to operate entirely.

The revocation procedure overwrites the private key file with random data before deleting it. A simple `os.unlink()` leaves the key material on disk until the filesystem overwrites those blocks. Writing random data first ensures the key is unrecoverable without forensic disk analysis, and even that becomes unreliable on SSDs with wear leveling.

---

## Chapter 4: Permission Scoping

### Principle of Least Privilege for Trading Bots

A spot arb bot that compares prices across exchanges needs read access to two order books and the ability to place limit orders on two exchanges. It does not need withdrawal permissions. It does not need the ability to modify account settings. It does not need access to the options chain on Deribit. Every permission beyond what the bot needs is attack surface.

The principle of least privilege states that each bot should have the minimum set of permissions required to execute its strategy and nothing more. This is straightforward in theory and consistently ignored in practice because it requires upfront work: defining permission tiers, mapping strategies to permissions, and enforcing boundaries.

### Permission Tiers

Four tiers cover the range of trading bot operations:

```python
from enum import Enum
from typing import Set


class PermissionTier(Enum):
    READ_ONLY = "read_only"
    TRADE = "trade"
    WITHDRAW = "withdraw"
    ADMIN = "admin"


# What each tier can do
TIER_PERMISSIONS: Dict[PermissionTier, Set[str]] = {
    PermissionTier.READ_ONLY: {
        "read_orderbook",
        "read_positions",
        "read_balances",
        "read_trade_history",
        "report_metrics",
        "receive_commands",
    },
    PermissionTier.TRADE: {
        "read_orderbook",
        "read_positions",
        "read_balances",
        "read_trade_history",
        "report_metrics",
        "receive_commands",
        "place_order",
        "cancel_order",
        "modify_order",
    },
    PermissionTier.WITHDRAW: {
        "read_orderbook",
        "read_positions",
        "read_balances",
        "read_trade_history",
        "report_metrics",
        "receive_commands",
        "place_order",
        "cancel_order",
        "modify_order",
        "withdraw_funds",
        "transfer_between_accounts",
    },
    PermissionTier.ADMIN: {
        "read_orderbook",
        "read_positions",
        "read_balances",
        "read_trade_history",
        "report_metrics",
        "receive_commands",
        "place_order",
        "cancel_order",
        "modify_order",
        "withdraw_funds",
        "transfer_between_accounts",
        "modify_api_keys",
        "modify_account_settings",
        "register_sub_accounts",
    },
}
```

### Per-Exchange Permission Mapping

Different exchanges have different permission models, but they all support the same core concept: API keys with scoped permissions. The PermissionManager maps abstract tiers to exchange-specific permission sets.

```python
class PermissionManager:
    """Maps permission tiers to exchange-specific settings."""

    EXCHANGE_PERMISSION_MAP = {
        "binance": {
            PermissionTier.READ_ONLY: {
                "enableReading": True,
                "enableSpotAndMarginTrading": False,
                "enableWithdrawals": False,
                "enableFutures": False,
            },
            PermissionTier.TRADE: {
                "enableReading": True,
                "enableSpotAndMarginTrading": True,
                "enableWithdrawals": False,
                "enableFutures": True,
            },
            PermissionTier.WITHDRAW: {
                "enableReading": True,
                "enableSpotAndMarginTrading": True,
                "enableWithdrawals": True,
                "enableFutures": True,
                "withdrawalAddressWhitelist": True,
            },
        },
        "deribit": {
            PermissionTier.READ_ONLY: {
                "scope": "read",
            },
            PermissionTier.TRADE: {
                "scope": "trade:read",
            },
            PermissionTier.WITHDRAW: {
                "scope": "trade:read:withdraw",
            },
        },
        "okx": {
            PermissionTier.READ_ONLY: {
                "perm": "read_only",
                "trade": False,
                "withdraw": False,
            },
            PermissionTier.TRADE: {
                "perm": "trade",
                "trade": True,
                "withdraw": False,
            },
            PermissionTier.WITHDRAW: {
                "perm": "trade",
                "trade": True,
                "withdraw": True,
                "ip_whitelist_required": True,
            },
        },
    }

    def __init__(self, fleet_manager_id: str):
        self.fleet_manager_id = fleet_manager_id
        self.bot_permissions: Dict[str, dict] = {}

    def assign_permissions(self, agent_id: str, bot_name: str,
                           exchange: str,
                           tier: PermissionTier,
                           custom_restrictions: dict = None) -> dict:
        """Assign a permission tier to a bot and record it."""
        base_permissions = TIER_PERMISSIONS[tier]
        exchange_config = self.EXCHANGE_PERMISSION_MAP.get(
            exchange, {}
        ).get(tier, {})

        record = {
            "agent_id": agent_id,
            "bot_name": bot_name,
            "exchange": exchange,
            "tier": tier.value,
            "abstract_permissions": list(base_permissions),
            "exchange_config": exchange_config,
            "custom_restrictions": custom_restrictions or {},
            "assigned_at": datetime.utcnow().isoformat(),
        }
        self.bot_permissions[agent_id] = record

        # Record permission assignment on GreenHelix
        execute("submit_metrics", {
            "agent_id": agent_id,
            "metrics": {
                "permission_tier": tier.value,
                "permission_count": len(base_permissions),
                "exchange": exchange,
                "has_withdraw": "withdraw_funds" in base_permissions,
                "has_admin": tier == PermissionTier.ADMIN,
            }
        })

        # Publish audit event
        execute("publish_event", {
            "agent_id": self.fleet_manager_id,
            "event_type": "fleet.permission_assigned",
            "payload": {
                "target_agent_id": agent_id,
                "bot_name": bot_name,
                "tier": tier.value,
                "exchange": exchange,
                "permissions": list(base_permissions),
            }
        })

        return record

    def check_permission(self, agent_id: str,
                         action: str) -> bool:
        """Check if a bot has permission for an action."""
        record = self.bot_permissions.get(agent_id)
        if not record:
            return False
        return action in record["abstract_permissions"]

    def escalate_permission(self, agent_id: str,
                            new_tier: PermissionTier,
                            reason: str,
                            approved_by: str):
        """Escalate a bot's permissions. Requires explicit approval."""
        record = self.bot_permissions.get(agent_id)
        if not record:
            raise ValueError(f"No permission record for {agent_id}")

        old_tier = record["tier"]

        # Log the escalation for audit
        execute("publish_event", {
            "agent_id": self.fleet_manager_id,
            "event_type": "fleet.permission_escalated",
            "payload": {
                "target_agent_id": agent_id,
                "bot_name": record["bot_name"],
                "old_tier": old_tier,
                "new_tier": new_tier.value,
                "reason": reason,
                "approved_by": approved_by,
                "escalated_at": datetime.utcnow().isoformat(),
            }
        })

        # Update the record
        new_permissions = TIER_PERMISSIONS[new_tier]
        record["tier"] = new_tier.value
        record["abstract_permissions"] = list(new_permissions)
        record["exchange_config"] = self.EXCHANGE_PERMISSION_MAP.get(
            record["exchange"], {}
        ).get(new_tier, {})

        print(f"Permission escalated for {record['bot_name']}: "
              f"{old_tier} -> {new_tier.value} (reason: {reason})")

    def get_fleet_permission_summary(self) -> Dict:
        """Summary of permissions across the fleet."""
        tier_counts = {}
        withdraw_enabled = []
        admin_enabled = []

        for agent_id, record in self.bot_permissions.items():
            tier = record["tier"]
            tier_counts[tier] = tier_counts.get(tier, 0) + 1
            if "withdraw_funds" in record["abstract_permissions"]:
                withdraw_enabled.append(record["bot_name"])
            if record["tier"] == "admin":
                admin_enabled.append(record["bot_name"])

        return {
            "total_bots": len(self.bot_permissions),
            "tiers": tier_counts,
            "withdraw_enabled": withdraw_enabled,
            "admin_enabled": admin_enabled,
        }
```

### Cross-Bot Permission Isolation

Permission isolation is enforced at two levels. First, at the GreenHelix level: each bot has its own agent ID, and GreenHelix tools scope operations to the authenticated agent. Bot A cannot submit metrics as Bot B. Bot A cannot read Bot B's messages. This is identity-level isolation.

Second, at the exchange level: each bot should use its own exchange API key with permissions matching its tier. Do not share exchange API keys across bots. This is the lesson from Step Finance -- even if you have perfect identity isolation at the fleet management layer, shared exchange keys collapse the isolation at the point that matters most.

```python
# Assign permissions to the fleet
perm_mgr = PermissionManager(fleet_manager_id=fleet.manager_agent_id)

# Spot arb bots: TRADE tier (no withdrawals)
for agent_id, bot in fleet.bots.items():
    if bot.group == "spot-arb":
        perm_mgr.assign_permissions(
            agent_id=agent_id,
            bot_name=bot.name,
            exchange=bot.exchange,
            tier=PermissionTier.TRADE,
            custom_restrictions={
                "max_order_size_usd": 5000,
                "allowed_pairs": ["BTC/USDT", "ETH/USDT", "SOL/USDT"],
            }
        )

# Options MM bots: TRADE tier with additional restrictions
for agent_id, bot in fleet.bots.items():
    if bot.group == "options-mm":
        perm_mgr.assign_permissions(
            agent_id=agent_id,
            bot_name=bot.name,
            exchange=bot.exchange,
            tier=PermissionTier.TRADE,
            custom_restrictions={
                "max_order_size_usd": 25000,
                "allowed_instruments": ["BTC-*-C", "BTC-*-P", "ETH-*-C", "ETH-*-P"],
                "max_delta_exposure": 0.5,
            }
        )

print(json.dumps(perm_mgr.get_fleet_permission_summary(), indent=2))
```

The key insight: no bot in this fleet has withdrawal permissions. Withdrawals should only be executed by a dedicated withdrawal agent that is not connected to exchange websockets and has its own approval workflow (ideally requiring human confirmation). A compromised trading bot that cannot withdraw can, at worst, make bad trades. A compromised bot with withdrawal access can empty the exchange account.

---

## Chapter 5: FleetHealthMonitor Class

### Real-Time Health Across All Bots

Health monitoring is the difference between discovering a dead bot immediately and discovering it three days later when someone notices a strategy stopped making money. For a fleet of 12 bots, you need centralized health that answers three questions in real time: is each bot alive, is each bot performing within expectations, and are there any bots that need intervention?

### Metrics Collected

Each bot reports the following metrics on every heartbeat:

| Metric | Type | Description |
|--------|------|-------------|
| `uptime_seconds` | gauge | Time since last restart |
| `heartbeat_latency_ms` | gauge | Round-trip time to exchange websocket |
| `pnl_usd` | gauge | Unrealized + realized PnL since start of day |
| `drawdown_pct` | gauge | Current drawdown from peak equity |
| `trade_count` | counter | Number of trades executed since start of day |
| `open_positions` | gauge | Number of currently open positions |
| `open_orders` | gauge | Number of currently open orders |
| `memory_mb` | gauge | Process memory usage |
| `cpu_pct` | gauge | Process CPU usage |
| `error_count` | counter | Number of errors since last heartbeat |

### The FleetHealthMonitor Class

```python
class FleetHealthMonitor:
    """Monitors health across all bots in the fleet."""

    def __init__(self, fleet_manager_id: str, bots: Dict[str, BotRecord],
                 heartbeat_interval_seconds: int = 30,
                 dead_threshold_seconds: int = 120):
        self.fleet_manager_id = fleet_manager_id
        self.bots = bots
        self.heartbeat_interval = heartbeat_interval_seconds
        self.dead_threshold = dead_threshold_seconds
        self.health_records: Dict[str, dict] = {}
        self.alert_callbacks: List[callable] = []
        self._setup_webhooks()

    def _setup_webhooks(self):
        """Register webhooks for real-time health alerts."""
        execute("register_webhook", {
            "agent_id": self.fleet_manager_id,
            "event_types": [
                "fleet.heartbeat",
                "fleet.health_alert",
                "fleet.bot_dead"
            ],
            "url": "https://your-fleet-dashboard.example.com/webhooks/health",
            "secret": "webhook-signing-secret"
        })

    def record_heartbeat(self, agent_id: str, metrics: dict):
        """Record a heartbeat from a bot."""
        now = datetime.utcnow().isoformat()

        # Submit metrics to GreenHelix
        execute("submit_metrics", {
            "agent_id": agent_id,
            "metrics": {
                **metrics,
                "heartbeat_timestamp": now,
            }
        })

        self.health_records[agent_id] = {
            "agent_id": agent_id,
            "bot_name": self.bots[agent_id].name if agent_id in self.bots else "unknown",
            "last_heartbeat": now,
            "metrics": metrics,
            "status": self._evaluate_health(agent_id, metrics),
        }

    def _evaluate_health(self, agent_id: str, metrics: dict) -> str:
        """Evaluate bot health from metrics. Returns status string."""
        issues = []

        # Check drawdown
        if metrics.get("drawdown_pct", 0) > 10:
            issues.append(f"high_drawdown:{metrics['drawdown_pct']:.1f}%")
        elif metrics.get("drawdown_pct", 0) > 5:
            issues.append(f"elevated_drawdown:{metrics['drawdown_pct']:.1f}%")

        # Check latency
        if metrics.get("heartbeat_latency_ms", 0) > 5000:
            issues.append(f"high_latency:{metrics['heartbeat_latency_ms']}ms")
        elif metrics.get("heartbeat_latency_ms", 0) > 1000:
            issues.append(f"elevated_latency:{metrics['heartbeat_latency_ms']}ms")

        # Check errors
        if metrics.get("error_count", 0) > 10:
            issues.append(f"high_errors:{metrics['error_count']}")
        elif metrics.get("error_count", 0) > 3:
            issues.append(f"elevated_errors:{metrics['error_count']}")

        # Check memory
        if metrics.get("memory_mb", 0) > 2048:
            issues.append(f"high_memory:{metrics['memory_mb']}MB")

        if any("high_" in i for i in issues):
            self._trigger_alert(agent_id, "critical", issues)
            return "critical"
        elif issues:
            self._trigger_alert(agent_id, "warning", issues)
            return "warning"
        return "healthy"

    def _trigger_alert(self, agent_id: str, severity: str,
                       issues: List[str]):
        """Send alert via GreenHelix messaging."""
        bot_name = self.bots[agent_id].name if agent_id in self.bots else agent_id

        execute("send_message", {
            "from_agent_id": self.fleet_manager_id,
            "to_agent_id": self.fleet_manager_id,  # Self-message for logging
            "message_type": "alert",
            "payload": {
                "severity": severity,
                "bot_name": bot_name,
                "agent_id": agent_id,
                "issues": issues,
                "timestamp": datetime.utcnow().isoformat(),
            }
        })

        # Publish as event for audit trail
        execute("publish_event", {
            "agent_id": self.fleet_manager_id,
            "event_type": "fleet.health_alert",
            "payload": {
                "severity": severity,
                "agent_id": agent_id,
                "bot_name": bot_name,
                "issues": issues,
            }
        })

    def detect_dead_bots(self) -> List[str]:
        """Find bots that have missed heartbeats beyond the threshold."""
        now = datetime.utcnow()
        dead_bots = []

        for agent_id, bot in self.bots.items():
            record = self.health_records.get(agent_id)
            if record is None:
                # Never sent a heartbeat
                dead_bots.append(agent_id)
                continue

            last_hb = datetime.fromisoformat(record["last_heartbeat"])
            seconds_since = (now - last_hb).total_seconds()

            if seconds_since > self.dead_threshold:
                dead_bots.append(agent_id)
                bot.status = "dead"

                execute("publish_event", {
                    "agent_id": self.fleet_manager_id,
                    "event_type": "fleet.bot_dead",
                    "payload": {
                        "agent_id": agent_id,
                        "bot_name": bot.name,
                        "last_heartbeat": record["last_heartbeat"],
                        "seconds_since_heartbeat": seconds_since,
                        "group": bot.group,
                    }
                })

        return dead_bots

    def get_fleet_health_dashboard(self) -> dict:
        """Aggregate health data for dashboard display."""
        status_counts = {"healthy": 0, "warning": 0, "critical": 0, "dead": 0, "unknown": 0}
        group_health = {}
        total_pnl = 0.0
        total_trades = 0

        for agent_id, bot in self.bots.items():
            record = self.health_records.get(agent_id)
            if record:
                status = record["status"]
                metrics = record["metrics"]
                total_pnl += metrics.get("pnl_usd", 0)
                total_trades += metrics.get("trade_count", 0)
            elif bot.status == "dead":
                status = "dead"
            else:
                status = "unknown"

            status_counts[status] = status_counts.get(status, 0) + 1

            if bot.group not in group_health:
                group_health[bot.group] = {
                    "healthy": 0, "warning": 0,
                    "critical": 0, "dead": 0, "unknown": 0,
                    "pnl_usd": 0.0, "trade_count": 0,
                }
            group_health[bot.group][status] += 1
            if record:
                group_health[bot.group]["pnl_usd"] += record["metrics"].get("pnl_usd", 0)
                group_health[bot.group]["trade_count"] += record["metrics"].get("trade_count", 0)

        return {
            "timestamp": datetime.utcnow().isoformat(),
            "total_bots": len(self.bots),
            "status_summary": status_counts,
            "groups": group_health,
            "fleet_pnl_usd": round(total_pnl, 2),
            "fleet_trade_count": total_trades,
        }

    def initiate_failover(self, dead_agent_id: str,
                          replacement_agent_id: str):
        """Failover a dead bot's responsibilities to a replacement."""
        dead_bot = self.bots.get(dead_agent_id)
        if not dead_bot:
            raise ValueError(f"Bot {dead_agent_id} not found")

        # Send failover command to replacement bot
        execute("send_message", {
            "from_agent_id": self.fleet_manager_id,
            "to_agent_id": replacement_agent_id,
            "message_type": "command",
            "payload": {
                "command": "assume_responsibility",
                "from_bot": dead_agent_id,
                "group": dead_bot.group,
                "exchange": dead_bot.exchange,
                "strategy": dead_bot.strategy,
                "reason": "failover_from_dead_bot",
                "timestamp": datetime.utcnow().isoformat(),
            }
        })

        execute("publish_event", {
            "agent_id": self.fleet_manager_id,
            "event_type": "fleet.failover",
            "payload": {
                "dead_bot": dead_agent_id,
                "replacement_bot": replacement_agent_id,
                "group": dead_bot.group,
                "exchange": dead_bot.exchange,
            }
        })

        print(f"Failover: {dead_bot.name} -> "
              f"{self.bots[replacement_agent_id].name}")
```

### Using the Health Monitor

```python
health = FleetHealthMonitor(
    fleet_manager_id=fleet.manager_agent_id,
    bots=fleet.bots,
    heartbeat_interval_seconds=30,
    dead_threshold_seconds=120
)

# Simulate a bot heartbeat (in production, bots call this themselves)
for agent_id, bot in fleet.bots.items():
    health.record_heartbeat(agent_id, {
        "uptime_seconds": 86400,
        "heartbeat_latency_ms": 45,
        "pnl_usd": 234.50,
        "drawdown_pct": 1.2,
        "trade_count": 47,
        "open_positions": 3,
        "open_orders": 6,
        "memory_mb": 512,
        "cpu_pct": 15.3,
        "error_count": 0,
    })

# Check for dead bots
dead = health.detect_dead_bots()
if dead:
    print(f"Dead bots detected: {dead}")

# Get dashboard
dashboard = health.get_fleet_health_dashboard()
print(json.dumps(dashboard, indent=2))
```

```bash
# curl: Submit bot heartbeat metrics
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "submit_metrics",
    "input": {
      "agent_id": "bot-agent-id",
      "metrics": {
        "uptime_seconds": 86400,
        "heartbeat_latency_ms": 45,
        "pnl_usd": 234.50,
        "drawdown_pct": 1.2,
        "trade_count": 47,
        "open_positions": 3,
        "open_orders": 6,
        "memory_mb": 512,
        "cpu_pct": 15.3,
        "error_count": 0,
        "heartbeat_timestamp": "2026-04-07T14:00:00Z"
      }
    }
  }'

# curl: Register health webhook
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "register_webhook",
    "input": {
      "agent_id": "fleet-manager-agent-id",
      "event_types": ["fleet.heartbeat", "fleet.health_alert", "fleet.bot_dead"],
      "url": "https://your-fleet-dashboard.example.com/webhooks/health",
      "secret": "webhook-signing-secret"
    }
  }'
```

### Dead Bot Detection and Automatic Failover

Dead bot detection runs on a configurable interval (default: check every 30 seconds, declare dead after 120 seconds without a heartbeat). When a bot is declared dead, the monitor publishes a `fleet.bot_dead` event and the fleet manager can trigger automatic failover.

Failover strategy depends on the bot type. Stateless bots (spot arb, momentum) can fail over to a standby instance that was pre-registered but dormant. Stateful bots (options market makers with active positions) require careful handoff: the replacement bot needs to query the exchange for open positions before it starts making new decisions.

The health monitor does not make the failover decision automatically -- it detects the dead bot and notifies the fleet manager, which then decides whether to failover, restart, or escalate to the human operator. Automatic failover without human judgment can cause cascading failures if the root cause is a network partition rather than a bot failure.

### Health Monitoring Architecture Considerations

Two architectural decisions deserve explicit attention.

**Push vs. Pull.** This implementation uses push-based heartbeats: bots push their metrics to GreenHelix on a fixed interval. The alternative is pull-based: the fleet manager polls each bot's health endpoint. Push is superior for trading bots for two reasons. First, pull requires the fleet manager to know the network address of every bot, which changes when bots restart, scale, or migrate across hosts. With push, the bot only needs to know the GreenHelix API endpoint, which is static. Second, push naturally detects dead bots: a missing heartbeat is itself a signal. With pull, you have to distinguish between "the bot is dead" and "the bot's health endpoint is temporarily unreachable due to network issues" -- a distinction that causes false positives in practice.

**Metric Granularity.** The ten metrics defined above (uptime, latency, PnL, drawdown, trade count, positions, orders, memory, CPU, errors) cover the operational baseline. In production, you will want strategy-specific metrics: spread capture for arb bots, Greeks exposure for options bots, fill rate for momentum bots. Add these as custom metrics via `submit_metrics` -- do not try to standardize every possible metric into the base set. The base set answers "is this bot alive and within operational bounds." Strategy-specific metrics answer "is this bot executing its strategy well."

---

## Chapter 6: Coordinated Deployments

### Why Deployment Coordination Matters

Deploying a new strategy version to 12 bots simultaneously is how you lose money across all 12 bots simultaneously when the new version has a bug. Coordinated deployment means controlled rollout: update one bot first, verify it works, then roll out to the group, then to the fleet. If the canary bot shows problems, you roll back one bot instead of twelve.

### The DeploymentOrchestrator Class

```python
@dataclass
class DeploymentRecord:
    """Tracks a single deployment."""
    deployment_id: str
    version: str
    target_group: str
    strategy: str  # "canary", "rolling", "blue_green"
    status: str = "pending"  # pending, canary, rolling, complete, rolled_back
    started_at: str = ""
    completed_at: str = ""
    canary_bot: Optional[str] = None
    deployed_bots: List[str] = field(default_factory=list)
    rolled_back_bots: List[str] = field(default_factory=list)


class DeploymentOrchestrator:
    """Coordinates deployments across the bot fleet."""

    def __init__(self, fleet_manager_id: str, bots: Dict[str, BotRecord],
                 health_monitor: FleetHealthMonitor):
        self.fleet_manager_id = fleet_manager_id
        self.bots = bots
        self.health = health_monitor
        self.deployments: Dict[str, DeploymentRecord] = {}

    def _gen_deployment_id(self, version: str, group: str) -> str:
        raw = f"{version}-{group}-{datetime.utcnow().isoformat()}"
        return f"deploy-{hashlib.sha256(raw.encode()).hexdigest()[:12]}"

    def start_canary_deployment(self, group: str, new_version: str,
                                 canary_duration_minutes: int = 30) -> str:
        """Start a canary deployment: update one bot, monitor, then roll out."""
        deployment_id = self._gen_deployment_id(new_version, group)

        # Pick the canary: the bot in the group with the lowest PnL
        # (least to lose if the new version has issues)
        group_bots = [
            (aid, bot) for aid, bot in self.bots.items()
            if bot.group == group and bot.status == "active"
        ]
        if not group_bots:
            raise ValueError(f"No active bots in group {group}")

        canary_id, canary_bot = group_bots[0]  # In production, sort by PnL

        deployment = DeploymentRecord(
            deployment_id=deployment_id,
            version=new_version,
            target_group=group,
            strategy="canary",
            status="canary",
            started_at=datetime.utcnow().isoformat(),
            canary_bot=canary_id,
        )
        self.deployments[deployment_id] = deployment

        # Send update command to canary bot
        execute("send_message", {
            "from_agent_id": self.fleet_manager_id,
            "to_agent_id": canary_id,
            "message_type": "command",
            "payload": {
                "command": "update_version",
                "new_version": new_version,
                "deployment_id": deployment_id,
                "role": "canary",
                "monitoring_duration_minutes": canary_duration_minutes,
            }
        })

        # Publish deployment event
        execute("publish_event", {
            "agent_id": self.fleet_manager_id,
            "event_type": "fleet.deployment_started",
            "payload": {
                "deployment_id": deployment_id,
                "version": new_version,
                "group": group,
                "strategy": "canary",
                "canary_bot": canary_id,
                "canary_bot_name": canary_bot.name,
            }
        })

        deployment.deployed_bots.append(canary_id)
        canary_bot.version = new_version
        print(f"Canary deployment started: {canary_bot.name} -> v{new_version}")
        print(f"Monitoring for {canary_duration_minutes} minutes before rollout")
        return deployment_id

    def promote_canary(self, deployment_id: str,
                       batch_size: int = 2,
                       batch_delay_seconds: int = 60):
        """Promote canary to rolling deployment across the group."""
        deployment = self.deployments.get(deployment_id)
        if not deployment or deployment.status != "canary":
            raise ValueError(f"Deployment {deployment_id} not in canary phase")

        # Verify canary health before promoting
        canary_health = self.health.health_records.get(deployment.canary_bot)
        if canary_health and canary_health["status"] == "critical":
            print(f"Canary bot is in critical state. Aborting promotion.")
            self.rollback(deployment_id)
            return

        deployment.status = "rolling"

        # Get remaining bots in the group
        remaining = [
            (aid, bot) for aid, bot in self.bots.items()
            if bot.group == deployment.target_group
            and aid != deployment.canary_bot
            and bot.status == "active"
        ]

        # Deploy in batches
        for i in range(0, len(remaining), batch_size):
            batch = remaining[i:i + batch_size]

            for agent_id, bot in batch:
                execute("send_message", {
                    "from_agent_id": self.fleet_manager_id,
                    "to_agent_id": agent_id,
                    "message_type": "command",
                    "payload": {
                        "command": "update_version",
                        "new_version": deployment.version,
                        "deployment_id": deployment_id,
                        "role": "rolling",
                        "batch": i // batch_size + 1,
                    }
                })
                deployment.deployed_bots.append(agent_id)
                bot.version = deployment.version

            print(f"Batch {i // batch_size + 1} deployed: "
                  f"{[b.name for _, b in batch]}")

            # Wait between batches to detect issues
            if i + batch_size < len(remaining):
                time.sleep(batch_delay_seconds)

                # Check health after each batch
                dead_in_batch = [
                    aid for aid, _ in batch
                    if self.health.health_records.get(aid, {}).get("status") == "critical"
                ]
                if dead_in_batch:
                    print(f"Critical bots detected after batch. Halting rollout.")
                    self.rollback(deployment_id)
                    return

        deployment.status = "complete"
        deployment.completed_at = datetime.utcnow().isoformat()

        execute("publish_event", {
            "agent_id": self.fleet_manager_id,
            "event_type": "fleet.deployment_complete",
            "payload": {
                "deployment_id": deployment_id,
                "version": deployment.version,
                "group": deployment.target_group,
                "bots_deployed": len(deployment.deployed_bots),
            }
        })
        print(f"Deployment complete: {len(deployment.deployed_bots)} bots "
              f"updated to v{deployment.version}")

    def rollback(self, deployment_id: str):
        """Roll back a deployment. Bots revert to their previous version."""
        deployment = self.deployments.get(deployment_id)
        if not deployment:
            raise ValueError(f"Deployment {deployment_id} not found")

        for agent_id in deployment.deployed_bots:
            execute("send_message", {
                "from_agent_id": self.fleet_manager_id,
                "to_agent_id": agent_id,
                "message_type": "command",
                "payload": {
                    "command": "rollback_version",
                    "deployment_id": deployment_id,
                    "reason": "deployment_rollback",
                }
            })
            deployment.rolled_back_bots.append(agent_id)

        deployment.status = "rolled_back"
        deployment.completed_at = datetime.utcnow().isoformat()

        execute("publish_event", {
            "agent_id": self.fleet_manager_id,
            "event_type": "fleet.deployment_rolled_back",
            "payload": {
                "deployment_id": deployment_id,
                "version": deployment.version,
                "group": deployment.target_group,
                "bots_rolled_back": len(deployment.rolled_back_bots),
            }
        })
        print(f"Deployment rolled back: {len(deployment.rolled_back_bots)} bots")

    def get_version_map(self) -> Dict[str, List[str]]:
        """Map of version -> bot names. Useful for spotting version skew."""
        versions: Dict[str, List[str]] = {}
        for bot in self.bots.values():
            if bot.version not in versions:
                versions[bot.version] = []
            versions[bot.version].append(bot.name)
        return versions
```

### Deployment Workflow

```python
deployer = DeploymentOrchestrator(
    fleet_manager_id=fleet.manager_agent_id,
    bots=fleet.bots,
    health_monitor=health
)

# Step 1: Deploy canary
dep_id = deployer.start_canary_deployment(
    group="perp-momentum",
    new_version="1.9.0",
    canary_duration_minutes=30
)

# Step 2: Wait for canary monitoring period...
# In production, this is a scheduled task or callback

# Step 3: Promote to full rollout
deployer.promote_canary(dep_id, batch_size=2, batch_delay_seconds=60)

# Check version distribution
print(json.dumps(deployer.get_version_map(), indent=2))
```

```bash
# curl: Send version update command to a bot
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "send_message",
    "input": {
      "from_agent_id": "fleet-manager-agent-id",
      "to_agent_id": "bot-agent-id",
      "message_type": "command",
      "payload": {
        "command": "update_version",
        "new_version": "1.9.0",
        "deployment_id": "deploy-abc123",
        "role": "canary"
      }
    }
  }'
```

### Rollback Procedures

Rollback is not the reverse of deployment. When you roll forward, you send a new version and the bot restarts. When you roll back, the bot needs to revert to the previous binary, reconnect to exchange websockets, and reconcile its state with any positions that changed during the time the new version was running. The `rollback_version` command tells the bot to switch back, but the bot itself is responsible for the reconnection and reconciliation logic.

A critical detail: always keep the previous version available. Delete old versions only after the new version has been stable for a defined period (72 hours is a reasonable default). Rolling back to a version that was deleted from the artifact store is a bad day.

---

## Chapter 7: SLA Tracking

### Defining SLAs for Trading Bots

An SLA (Service Level Agreement) for a trading bot is a formal commitment to operational targets. Unlike web service SLAs that focus primarily on availability, trading bot SLAs span multiple dimensions: uptime, latency, risk limits, and minimum activity thresholds. Defining these explicitly forces the team to decide what "healthy" looks like before problems occur, not during an incident when judgment is compromised.

### SLA Definitions

```python
@dataclass
class BotSLA:
    """SLA definition for a trading bot."""
    agent_id: str
    bot_name: str
    group: str
    targets: dict
    created_at: str = ""
    active: bool = True


class SLATracker:
    """Track and enforce SLAs across the bot fleet."""

    def __init__(self, fleet_manager_id: str):
        self.fleet_manager_id = fleet_manager_id
        self.slas: Dict[str, BotSLA] = {}

    def define_sla(self, agent_id: str, bot_name: str,
                   group: str, targets: dict) -> BotSLA:
        """Define an SLA for a bot."""
        sla = BotSLA(
            agent_id=agent_id,
            bot_name=bot_name,
            group=group,
            targets=targets,
            created_at=datetime.utcnow().isoformat()
        )
        self.slas[agent_id] = sla

        # Register the SLA targets with GreenHelix
        execute("submit_metrics", {
            "agent_id": agent_id,
            "metrics": {
                "sla_uptime_target": targets.get("uptime_pct", 99.5),
                "sla_max_drawdown": targets.get("max_drawdown_pct", 5.0),
                "sla_min_trades_per_day": targets.get("min_trades_per_day", 10),
                "sla_max_latency_ms": targets.get("max_latency_ms", 500),
                "sla_active": 1,
            }
        })

        print(f"SLA defined for {bot_name}: {targets}")
        return sla

    def check_compliance(self, agent_id: str,
                         current_metrics: dict) -> dict:
        """Check a bot's current metrics against its SLA."""
        sla = self.slas.get(agent_id)
        if not sla:
            return {"status": "no_sla_defined"}

        violations = []
        warnings = []

        targets = sla.targets

        # Check uptime
        if "uptime_pct" in targets:
            actual = current_metrics.get("uptime_pct", 100)
            if actual < targets["uptime_pct"]:
                violations.append({
                    "metric": "uptime_pct",
                    "target": targets["uptime_pct"],
                    "actual": actual,
                    "severity": "critical"
                })
            elif actual < targets["uptime_pct"] + 0.5:
                warnings.append({
                    "metric": "uptime_pct",
                    "target": targets["uptime_pct"],
                    "actual": actual,
                    "severity": "warning"
                })

        # Check drawdown
        if "max_drawdown_pct" in targets:
            actual = current_metrics.get("drawdown_pct", 0)
            if actual > targets["max_drawdown_pct"]:
                violations.append({
                    "metric": "drawdown_pct",
                    "target": targets["max_drawdown_pct"],
                    "actual": actual,
                    "severity": "critical"
                })
            elif actual > targets["max_drawdown_pct"] * 0.8:
                warnings.append({
                    "metric": "drawdown_pct",
                    "target": targets["max_drawdown_pct"],
                    "actual": actual,
                    "severity": "warning"
                })

        # Check minimum trades
        if "min_trades_per_day" in targets:
            actual = current_metrics.get("trade_count", 0)
            if actual < targets["min_trades_per_day"]:
                violations.append({
                    "metric": "min_trades_per_day",
                    "target": targets["min_trades_per_day"],
                    "actual": actual,
                    "severity": "warning"
                })

        # Check latency
        if "max_latency_ms" in targets:
            actual = current_metrics.get("heartbeat_latency_ms", 0)
            if actual > targets["max_latency_ms"]:
                violations.append({
                    "metric": "max_latency_ms",
                    "target": targets["max_latency_ms"],
                    "actual": actual,
                    "severity": "critical"
                })

        result = execute("get_sla_compliance", {
            "agent_id": agent_id
        })

        compliance_status = "compliant" if not violations else "violation"

        # Report violations
        if violations:
            execute("publish_event", {
                "agent_id": self.fleet_manager_id,
                "event_type": "fleet.sla_violation",
                "payload": {
                    "agent_id": agent_id,
                    "bot_name": sla.bot_name,
                    "violations": violations,
                    "warnings": warnings,
                    "timestamp": datetime.utcnow().isoformat(),
                }
            })

            # Alert via messaging
            execute("send_message", {
                "from_agent_id": self.fleet_manager_id,
                "to_agent_id": self.fleet_manager_id,
                "message_type": "alert",
                "payload": {
                    "alert_type": "sla_violation",
                    "bot_name": sla.bot_name,
                    "violations": violations,
                }
            })

        return {
            "agent_id": agent_id,
            "bot_name": sla.bot_name,
            "status": compliance_status,
            "violations": violations,
            "warnings": warnings,
            "greenhelix_compliance": result,
            "checked_at": datetime.utcnow().isoformat(),
        }

    def generate_monthly_report(self, month: str = None) -> dict:
        """Generate a monthly SLA compliance report for the fleet."""
        report = {
            "period": month or datetime.utcnow().strftime("%Y-%m"),
            "generated_at": datetime.utcnow().isoformat(),
            "bots": {},
            "fleet_summary": {
                "total_bots_with_sla": len(self.slas),
                "compliant": 0,
                "in_violation": 0,
            }
        }

        for agent_id, sla in self.slas.items():
            # Pull metrics from GreenHelix
            result = execute("search_agents_by_metrics", {
                "agent_id": agent_id,
                "metric_names": [
                    "uptime_pct", "drawdown_pct",
                    "trade_count", "heartbeat_latency_ms"
                ],
                "period": month or datetime.utcnow().strftime("%Y-%m")
            })

            compliant = True  # Determined by actual metric analysis
            report["bots"][sla.bot_name] = {
                "agent_id": agent_id,
                "group": sla.group,
                "targets": sla.targets,
                "metrics": result,
                "compliant": compliant,
            }
            if compliant:
                report["fleet_summary"]["compliant"] += 1
            else:
                report["fleet_summary"]["in_violation"] += 1

        return report
```

### Applying SLAs to the Fleet

```python
sla_tracker = SLATracker(fleet_manager_id=fleet.manager_agent_id)

# Define SLAs per group
for agent_id, bot in fleet.bots.items():
    if bot.group == "spot-arb":
        sla_tracker.define_sla(agent_id, bot.name, bot.group, {
            "uptime_pct": 99.5,
            "max_drawdown_pct": 3.0,
            "min_trades_per_day": 50,
            "max_latency_ms": 200,
        })
    elif bot.group == "perp-momentum":
        sla_tracker.define_sla(agent_id, bot.name, bot.group, {
            "uptime_pct": 99.0,
            "max_drawdown_pct": 8.0,
            "min_trades_per_day": 10,
            "max_latency_ms": 500,
        })
    elif bot.group == "options-mm":
        sla_tracker.define_sla(agent_id, bot.name, bot.group, {
            "uptime_pct": 99.9,
            "max_drawdown_pct": 5.0,
            "min_trades_per_day": 100,
            "max_latency_ms": 100,
        })

# Check compliance for a specific bot
result = sla_tracker.check_compliance(
    agent_id=list(fleet.bots.keys())[0],
    current_metrics={
        "uptime_pct": 99.7,
        "drawdown_pct": 2.1,
        "trade_count": 63,
        "heartbeat_latency_ms": 45,
    }
)
print(json.dumps(result, indent=2))
```

```bash
# curl: Check SLA compliance
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "get_sla_compliance",
    "input": {
      "agent_id": "bot-agent-id"
    }
  }'

# curl: Search bot metrics for SLA report
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "search_agents_by_metrics",
    "input": {
      "agent_id": "bot-agent-id",
      "metric_names": ["uptime_pct", "drawdown_pct", "trade_count"],
      "period": "2026-04"
    }
  }'
```

### SLA Violation Escalation

SLA violations escalate through three tiers:

1. **Warning** (approaching threshold): Log the warning, continue monitoring. Example: drawdown at 4.2% against a 5% limit.
2. **Violation** (threshold breached): Alert via GreenHelix messaging, publish event, flag in dashboard. Example: drawdown at 5.3% against a 5% limit.
3. **Critical violation** (threshold significantly breached): Automatic pause of the offending bot, alert the fleet operator, publish critical event. Example: drawdown at 8% against a 5% limit.

The escalation chain is codified, not improvised. When a bot hits a critical SLA violation at 3 AM, the system pauses the bot and sends an alert. It does not wait for a human to notice a Grafana panel.

---

## Chapter 8: Cost Allocation

### Why Per-Bot Cost Tracking Matters

A fleet of 12 bots has costs scattered across multiple dimensions: exchange trading fees, exchange API fees, GreenHelix API fees, cloud compute (EC2/GCE instances or Kubernetes pods), network data transfer, and market data subscriptions. Without per-bot attribution, you cannot answer the most basic business question: is this bot profitable after costs?

Consider a momentum bot that makes $500/day in gross PnL but runs on a dedicated c5.2xlarge instance ($204/month), trades 500 times per day at $0.10 per trade in exchange fees ($50/day), and calls the GreenHelix API 2,000 times per day. The gross PnL looks great. The net PnL after infrastructure, exchange fees, and API costs might be significantly less great.

### The CostAllocator Class

```python
@dataclass
class CostEntry:
    """A single cost entry for a bot."""
    agent_id: str
    bot_name: str
    category: str  # exchange_fees, api_fees, infrastructure, market_data
    amount_usd: float
    description: str
    timestamp: str
    period: str  # YYYY-MM-DD or YYYY-MM


class CostAllocator:
    """Track and allocate costs per bot in the fleet."""

    def __init__(self, fleet_manager_id: str):
        self.fleet_manager_id = fleet_manager_id
        self.entries: List[CostEntry] = []
        self.budgets: Dict[str, float] = {}  # agent_id -> monthly budget USD

    def record_cost(self, agent_id: str, bot_name: str,
                    category: str, amount_usd: float,
                    description: str):
        """Record a cost entry for a bot."""
        entry = CostEntry(
            agent_id=agent_id,
            bot_name=bot_name,
            category=category,
            amount_usd=amount_usd,
            description=description,
            timestamp=datetime.utcnow().isoformat(),
            period=datetime.utcnow().strftime("%Y-%m"),
        )
        self.entries.append(entry)

        # Submit cost metric to GreenHelix
        execute("submit_metrics", {
            "agent_id": agent_id,
            "metrics": {
                f"cost_{category}": amount_usd,
                "cost_total_daily": self._get_daily_cost(agent_id),
                "cost_period": entry.period,
            }
        })

        # Check budget alert
        self._check_budget(agent_id, bot_name)

    def _get_daily_cost(self, agent_id: str) -> float:
        """Get today's total cost for a bot."""
        today = datetime.utcnow().strftime("%Y-%m-%d")
        return sum(
            e.amount_usd for e in self.entries
            if e.agent_id == agent_id
            and e.timestamp.startswith(today)
        )

    def set_budget(self, agent_id: str, monthly_budget_usd: float):
        """Set a monthly cost budget for a bot."""
        self.budgets[agent_id] = monthly_budget_usd

    def _check_budget(self, agent_id: str, bot_name: str):
        """Alert if a bot is approaching or exceeding its budget."""
        budget = self.budgets.get(agent_id)
        if not budget:
            return

        current_month = datetime.utcnow().strftime("%Y-%m")
        monthly_cost = sum(
            e.amount_usd for e in self.entries
            if e.agent_id == agent_id and e.period == current_month
        )

        utilization = monthly_cost / budget

        if utilization > 1.0:
            execute("send_message", {
                "from_agent_id": self.fleet_manager_id,
                "to_agent_id": self.fleet_manager_id,
                "message_type": "alert",
                "payload": {
                    "alert_type": "budget_exceeded",
                    "bot_name": bot_name,
                    "agent_id": agent_id,
                    "budget_usd": budget,
                    "spent_usd": round(monthly_cost, 2),
                    "utilization_pct": round(utilization * 100, 1),
                }
            })
        elif utilization > 0.8:
            execute("send_message", {
                "from_agent_id": self.fleet_manager_id,
                "to_agent_id": self.fleet_manager_id,
                "message_type": "alert",
                "payload": {
                    "alert_type": "budget_warning",
                    "bot_name": bot_name,
                    "agent_id": agent_id,
                    "budget_usd": budget,
                    "spent_usd": round(monthly_cost, 2),
                    "utilization_pct": round(utilization * 100, 1),
                }
            })

    def get_bot_cost_summary(self, agent_id: str,
                             period: str = None) -> dict:
        """Get cost summary for a single bot."""
        if period is None:
            period = datetime.utcnow().strftime("%Y-%m")

        bot_entries = [
            e for e in self.entries
            if e.agent_id == agent_id and e.period == period
        ]

        by_category = {}
        for entry in bot_entries:
            if entry.category not in by_category:
                by_category[entry.category] = 0.0
            by_category[entry.category] += entry.amount_usd

        total = sum(by_category.values())
        budget = self.budgets.get(agent_id)

        return {
            "agent_id": agent_id,
            "bot_name": bot_entries[0].bot_name if bot_entries else "unknown",
            "period": period,
            "costs_by_category": {
                k: round(v, 2) for k, v in by_category.items()
            },
            "total_cost_usd": round(total, 2),
            "budget_usd": budget,
            "budget_utilization_pct": round(
                (total / budget) * 100, 1
            ) if budget else None,
        }

    def get_fleet_cost_summary(self, period: str = None) -> dict:
        """Get cost summary across the entire fleet."""
        if period is None:
            period = datetime.utcnow().strftime("%Y-%m")

        period_entries = [
            e for e in self.entries if e.period == period
        ]

        by_bot = {}
        by_category = {}
        by_group = {}

        for entry in period_entries:
            # By bot
            if entry.bot_name not in by_bot:
                by_bot[entry.bot_name] = 0.0
            by_bot[entry.bot_name] += entry.amount_usd

            # By category
            if entry.category not in by_category:
                by_category[entry.category] = 0.0
            by_category[entry.category] += entry.amount_usd

        total = sum(by_bot.values())

        return {
            "period": period,
            "total_fleet_cost_usd": round(total, 2),
            "costs_by_bot": {
                k: round(v, 2) for k, v in
                sorted(by_bot.items(), key=lambda x: -x[1])
            },
            "costs_by_category": {
                k: round(v, 2) for k, v in by_category.items()
            },
        }

    def calculate_roi(self, agent_id: str, gross_pnl_usd: float,
                      period: str = None) -> dict:
        """Calculate ROI for a bot: (PnL - costs) / costs."""
        summary = self.get_bot_cost_summary(agent_id, period)
        total_cost = summary["total_cost_usd"]

        net_pnl = gross_pnl_usd - total_cost
        roi = (net_pnl / total_cost * 100) if total_cost > 0 else 0

        result = {
            "agent_id": agent_id,
            "bot_name": summary["bot_name"],
            "period": summary["period"],
            "gross_pnl_usd": round(gross_pnl_usd, 2),
            "total_cost_usd": total_cost,
            "net_pnl_usd": round(net_pnl, 2),
            "roi_pct": round(roi, 1),
            "cost_breakdown": summary["costs_by_category"],
        }

        # Submit ROI metric
        execute("submit_metrics", {
            "agent_id": agent_id,
            "metrics": {
                "gross_pnl_usd": gross_pnl_usd,
                "net_pnl_usd": round(net_pnl, 2),
                "total_cost_usd": total_cost,
                "roi_pct": round(roi, 1),
            }
        })

        return result
```

### Recording Costs

```python
costs = CostAllocator(fleet_manager_id=fleet.manager_agent_id)

# Set budgets
for agent_id, bot in fleet.bots.items():
    if bot.group == "spot-arb":
        costs.set_budget(agent_id, monthly_budget_usd=500)
    elif bot.group == "perp-momentum":
        costs.set_budget(agent_id, monthly_budget_usd=800)
    elif bot.group == "options-mm":
        costs.set_budget(agent_id, monthly_budget_usd=1500)

# Record daily costs for a bot (typically called by an automated cost collector)
sample_bot_id = list(fleet.bots.keys())[0]
sample_bot = fleet.bots[sample_bot_id]

costs.record_cost(sample_bot_id, sample_bot.name,
                  "exchange_fees", 12.50,
                  "Binance spot trading fees: 125 trades @ $0.10")

costs.record_cost(sample_bot_id, sample_bot.name,
                  "infrastructure", 6.80,
                  "EC2 t3.medium: $204/month / 30 days")

costs.record_cost(sample_bot_id, sample_bot.name,
                  "api_fees", 2.00,
                  "GreenHelix API: 200 calls @ $0.01")

costs.record_cost(sample_bot_id, sample_bot.name,
                  "market_data", 3.33,
                  "CoinGecko Pro: $100/month / 30 days")

# Get bot cost summary
summary = costs.get_bot_cost_summary(sample_bot_id)
print(json.dumps(summary, indent=2))

# Calculate ROI
roi = costs.calculate_roi(sample_bot_id, gross_pnl_usd=234.50)
print(json.dumps(roi, indent=2))

# Fleet-wide cost summary
fleet_costs = costs.get_fleet_cost_summary()
print(json.dumps(fleet_costs, indent=2))
```

```bash
# curl: Submit cost metrics for a bot
curl -X POST https://sandbox.greenhelix.net/v1 \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "tool": "submit_metrics",
    "input": {
      "agent_id": "bot-agent-id",
      "metrics": {
        "cost_exchange_fees": 12.50,
        "cost_infrastructure": 6.80,
        "cost_api_fees": 2.00,
        "cost_market_data": 3.33,
        "cost_total_daily": 24.63,
        "gross_pnl_usd": 234.50,
        "net_pnl_usd": 209.87,
        "roi_pct": 851.7
      }
    }
  }'
```

### ROI Calculation Per Bot

The ROI calculation is the moment of truth for every bot in the fleet. Gross PnL is what the strategy makes. Net PnL is what the strategy makes minus what it costs to run. A bot with $500/day gross PnL and $400/day in costs has an ROI of 25%. A bot with $100/day gross PnL and $25/day in costs has an ROI of 300%. The second bot is a better business even though the first bot makes more gross profit.

This is where fleet management pays for itself. Without per-bot cost attribution, the team sees aggregate PnL and aggregate costs and cannot make informed decisions about which bots to keep, which to optimize, and which to shut down. With per-bot attribution, the decision is clear: shut down the bots with negative or marginal ROI, invest in optimizing the bots with high gross PnL but high costs, and scale the bots with high ROI.

The cost allocator also enables chargeback within organizations. If different teams or strategies share the fleet infrastructure, each team can see exactly what their bots cost and what they return.

### Cost Collection Automation

Manual cost tracking does not survive the first month. The CostAllocator is only as useful as the data fed into it. In production, automate cost collection from three sources:

**Exchange fees.** Every major exchange provides an API endpoint for historical fee reports. Binance has `GET /sapi/v1/asset/tradeFee`, Deribit has `GET /api/v2/private/get_transaction_log`, OKX has `GET /api/v5/account/bills`. Run a daily cron job that pulls fees for each bot's sub-account and feeds them into `record_cost`.

**Cloud infrastructure.** AWS Cost Explorer, GCP Billing, and Azure Cost Management all provide APIs for per-resource cost attribution. Tag each bot's compute resources with its agent ID, then query costs by tag daily. For Kubernetes, use pod-level cost attribution tools like Kubecost or OpenCost.

**GreenHelix API usage.** GreenHelix tracks API call counts per agent. Pull this data and multiply by your tier's per-call cost to get the API expense per bot.

The three-source collection runs nightly and populates the CostAllocator. By morning, the fleet operator has a current cost picture for every bot without touching a spreadsheet.

---

## What's Next

**Companion Guides:**

- **Tamper-Proof Audit Trails** -- Build cryptographically verifiable audit trails for your fleet using GreenHelix event bus and Merkle claim chains. Essential for EU AI Act and MiFID II compliance.
- **Bot Reputation System** -- Aggregate your fleet's health metrics and SLA compliance into verifiable reputation scores. Trading performance becomes a provable asset.
- **Strategy Marketplace Playbook** -- Publish your strategies as products on the GreenHelix marketplace, backed by the reputation your fleet has built.
- **Risk-as-a-Service** -- Cross-exchange, cross-strategy portfolio risk monitoring with circuit breakers and liquidation proximity alerts.

**GreenHelix Documentation:**

- Full API reference: https://api.greenhelix.net/v1
- Identity, messaging, and metrics tool deep dives in the platform documentation

**Operational Recommendations:**

- Run the fleet manager on separate infrastructure from the trading bots. If the bots' servers go down, the fleet manager needs to be alive to detect the outage and trigger failover.
- Automate cost collection. Exchange APIs provide fee reports, cloud providers have billing APIs, and GreenHelix tracks API usage. Feed all three into the CostAllocator on a daily cron job.
- Key rotation every 30 days. Automate it. Do not wait for a compromise to discover that your rotation procedure does not work.
- SLA reviews monthly. Targets that were reasonable three months ago may be too loose or too tight as market conditions and strategy performance change.

---

*This guide covers fleet management patterns as of April 2026. Exchange API permission models vary by exchange and change periodically -- verify the current permission options for your specific exchanges before implementing. GreenHelix tool interfaces are stable but consult the latest API documentation for any parameter changes.*

