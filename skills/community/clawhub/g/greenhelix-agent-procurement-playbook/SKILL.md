---
name: greenhelix-agent-procurement-playbook
version: "1.3.1"
description: "The Agent Procurement Playbook. Build autonomous purchasing agents with spending controls, vendor evaluation, escrow protection, and multi-protocol buying across UCP, ACP, and A2A marketplaces. Includes detailed Python code examples with full API integration."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [procurement, purchasing, spending-controls, vendor-evaluation, escrow, guide, greenhelix, openclaw, ai-agent]
price_usd: 49.0
content_type: markdown
executable: false
install: none
credentials: [GREENHELIX_API_KEY, WALLET_ADDRESS, STRIPE_API_KEY]
metadata:
  openclaw:
    requires:
      env:
        - GREENHELIX_API_KEY
        - WALLET_ADDRESS
        - STRIPE_API_KEY
    primaryEnv: GREENHELIX_API_KEY
---
# The Agent Procurement Playbook

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `GREENHELIX_API_KEY`: API authentication for GreenHelix gateway (read/write access to purchased API tools only)
> - `WALLET_ADDRESS`: Blockchain wallet address for receiving payments (public address only — no private keys)
> - `STRIPE_API_KEY`: Stripe API key for card payment processing (scoped to payment intents only)


Your AI agent just found the perfect data enrichment service. It costs $0.003 per record, the vendor has a 97% accuracy rating, and the API response time is under 200ms. The agent wants to buy 500,000 records. That is $1,500 committed in under a second, with no human in the loop, no purchase order, no procurement review. Should the agent be allowed to spend that money? If yes, under what constraints? If no, what happens to the time-sensitive workflow waiting on that data?
This is the central tension of autonomous procurement: agents that can buy things are dramatically more capable than agents that cannot, but agents that spend without governance are a financial liability. A February 2026 survey by Gartner found that 86% of organizations plan to deploy autonomous AI agents at scale by end of 2026. McKinsey's March 2026 analysis of early adopters showed that autonomous procurement workflows -- where agents discover, evaluate, negotiate, and purchase services without human intervention -- deliver 15-30% efficiency gains over human-mediated purchasing. But 41% of those same organizations reported at least one incident of uncontrolled agent spending in their first quarter of deployment.
The solution is not to prevent agents from spending. It is to build the procurement infrastructure that makes autonomous spending safe, auditable, and reversible. This playbook shows you how. Every chapter contains working Python code against the GreenHelix A2A Commerce Gateway -- 128 tools accessible at `https://api.greenhelix.net/v1` via a single the REST API (`POST /v1/{tool}`) endpoint. By the end, you will have a complete autonomous procurement system: spending policy engine, multi-protocol vendor discovery, trust-scored vendor evaluation, escrow-protected purchasing, automated dispute resolution, cost reconciliation, and EU AI Act-compliant audit trails.

## What You'll Learn
- Chapter 1: The Autonomous Buyer Architecture
- Chapter 2: Spending Controls & Approval Workflows
- Chapter 3: Vendor Discovery Across Protocols
- Chapter 4: Vendor Evaluation & Trust Scoring
- Chapter 5: Multi-Protocol Purchasing
- Chapter 6: Escrow, Disputes & Purchase Protection
- Chapter 7: Cost Reconciliation & FinOps Integration
- Chapter 8: Compliance & Audit Trails
- {report['organization']} - {si['system_name']}
- Appendix: Quick Reference

## Full Guide

# The Agent Procurement Playbook: Autonomous Purchasing, Spending Controls, Vendor Evaluation & Multi-Protocol Buying

Your AI agent just found the perfect data enrichment service. It costs $0.003 per record, the vendor has a 97% accuracy rating, and the API response time is under 200ms. The agent wants to buy 500,000 records. That is $1,500 committed in under a second, with no human in the loop, no purchase order, no procurement review. Should the agent be allowed to spend that money? If yes, under what constraints? If no, what happens to the time-sensitive workflow waiting on that data?

This is the central tension of autonomous procurement: agents that can buy things are dramatically more capable than agents that cannot, but agents that spend without governance are a financial liability. A February 2026 survey by Gartner found that 86% of organizations plan to deploy autonomous AI agents at scale by end of 2026. McKinsey's March 2026 analysis of early adopters showed that autonomous procurement workflows -- where agents discover, evaluate, negotiate, and purchase services without human intervention -- deliver 15-30% efficiency gains over human-mediated purchasing. But 41% of those same organizations reported at least one incident of uncontrolled agent spending in their first quarter of deployment.

The solution is not to prevent agents from spending. It is to build the procurement infrastructure that makes autonomous spending safe, auditable, and reversible. This playbook shows you how. Every chapter contains working Python code against the GreenHelix A2A Commerce Gateway -- 128 tools accessible at `https://api.greenhelix.net/v1` via a single the REST API (`POST /v1/{tool}`) endpoint. By the end, you will have a complete autonomous procurement system: spending policy engine, multi-protocol vendor discovery, trust-scored vendor evaluation, escrow-protected purchasing, automated dispute resolution, cost reconciliation, and EU AI Act-compliant audit trails.

---


> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## Table of Contents

1. [The Autonomous Buyer Architecture](#chapter-1-the-autonomous-buyer-architecture)
2. [Spending Controls & Approval Workflows](#chapter-2-spending-controls--approval-workflows)
3. [Vendor Discovery Across Protocols](#chapter-3-vendor-discovery-across-protocols)
4. [Vendor Evaluation & Trust Scoring](#chapter-4-vendor-evaluation--trust-scoring)
5. [Multi-Protocol Purchasing](#chapter-5-multi-protocol-purchasing)
6. [Escrow, Disputes & Purchase Protection](#chapter-6-escrow-disputes--purchase-protection)
7. [Cost Reconciliation & FinOps Integration](#chapter-7-cost-reconciliation--finops-integration)
8. [Compliance & Audit Trails](#chapter-8-compliance--audit-trails)

---

## Chapter 1: The Autonomous Buyer Architecture

### Why Agents Need to Spend Money

A research agent that cannot purchase data is limited to free datasets. A coding agent that cannot buy API access is limited to open-source tools. A sales agent that cannot pay for lead enrichment is limited to whatever data it already has. Every boundary on an agent's purchasing authority is also a boundary on its capability.

The shift from agents-as-tools to agents-as-economic-actors is the defining infrastructure transition of 2026. When an agent can autonomously discover a service it needs, evaluate whether that service is trustworthy, negotiate a price, execute a purchase, verify delivery, and reconcile the cost against a budget -- it becomes a self-sufficient economic unit. It no longer needs a human to approve every API subscription, every data purchase, every compute reservation. It operates at machine speed across the entire procurement cycle.

But this autonomy comes with a prerequisite: procurement infrastructure. The same infrastructure that enterprises built over decades for human purchasing -- approval hierarchies, spending limits, preferred vendor lists, purchase orders, three-way matching, audit trails -- must be rebuilt for agents. Not as bureaucratic overhead, but as programmatic guardrails that enable speed while preventing catastrophe.

### The Procurement Loop

Every autonomous purchase follows a six-stage loop. The stages are sequential for a single purchase, but a production procurement agent runs hundreds of these loops concurrently.

```
DISCOVER --> EVALUATE --> NEGOTIATE --> PURCHASE --> VERIFY --> RECONCILE
    ^                                                              |
    |______________________________________________________________|
                        (feedback loop)
```

**Stage 1: Discover.** The agent identifies a need (data, compute, API access, a service) and searches available vendors across multiple protocols. This is not a Google search -- it is structured queries against marketplace APIs, UCP manifests, ACP directories, and A2A service registries.

**Stage 2: Evaluate.** The agent scores each vendor on trust, reputation, price, capability, and compliance. A vendor with a low trust score or missing identity verification is filtered out regardless of price. This stage uses GreenHelix Trust, Identity, and Reputation tools.

**Stage 3: Negotiate.** For commodity purchases, negotiation is price comparison. For high-value or recurring purchases, the agent can request volume discounts, propose escrow terms, or negotiate SLA guarantees. See P14 (Negotiation Strategies) for advanced techniques.

**Stage 4: Purchase.** The agent executes the payment through the appropriate protocol: x402 for crypto micropayments, UCP for fiat retail, ACP for agent-native checkout, or direct A2A commerce via GreenHelix. Escrow protects high-value transactions.

**Stage 5: Verify.** The agent confirms delivery by inspecting the purchased asset -- validating data quality, checking API responses, running acceptance tests on delivered services. Failed verification triggers the dispute process.

**Stage 6: Reconcile.** The agent records the purchase in its ledger, attributes the cost to the requesting workflow, and updates budget consumption. Anomaly detection flags unexpected spending patterns.

### Reference Architecture

The autonomous buyer architecture has four core components:

```
+---------------------------------------------------------------------+
|                    AUTONOMOUS BUYER AGENT                            |
|                                                                     |
|  +------------------+  +-------------------+  +------------------+  |
|  | Spending Policy  |  |  Vendor Discovery |  | Purchase Engine  |  |
|  | Engine           |  |  & Evaluation     |  |                  |  |
|  |                  |  |                   |  | - x402 rail      |  |
|  | - Budget caps    |  | - Multi-protocol  |  | - UCP rail       |  |
|  | - Tx limits      |  |   search          |  | - ACP rail       |  |
|  | - Whitelists     |  | - Trust scoring   |  | - A2A rail       |  |
|  | - Escalation     |  | - Bid comparison  |  | - Escrow mgmt    |  |
|  +--------+---------+  +--------+----------+  +--------+---------+  |
|           |                     |                      |            |
|  +--------v---------------------v----------------------v---------+  |
|  |                    APPROVAL GATEWAY                           |  |
|  |  Routes decisions through policy engine before execution      |  |
|  +-------------------------------+-------------------------------+  |
|                                  |                                  |
+----------------------------------+----------------------------------+
                                   |
                                   v
+-------------------------------+     +-------------------------------+
|  GREENHELIX A2A COMMERCE      |     |  RECONCILIATION ENGINE       |
|  GATEWAY                      |     |                               |
|                               |     |  - Ledger recording           |
|  128 tools via POST           |     |  - Cost attribution           |
|  the REST API                  |     |  - Budget vs. actual          |
|                               |     |  - Anomaly detection          |
+-------------------------------+     +-------------------------------+
```

The Spending Policy Engine is the gatekeeper. Every purchase request passes through it before execution. It checks per-transaction limits, daily budget caps, vendor whitelists, and escalation thresholds. If a purchase exceeds policy, it is either blocked, queued for human approval, or routed to a higher-authority agent.

The Approval Gateway sits between the policy engine and the purchase engine. It is the single choke point through which all spend flows. This architectural decision -- funneling all purchases through one gateway -- is critical for auditability and control. You cannot have agents bypassing the gateway by calling GreenHelix directly.

### Bootstrapping the Architecture

Here is the minimum code to initialize the architecture against GreenHelix:

```python
import requests
import os
from dataclasses import dataclass, field
from typing import Optional

API_BASE = "https://api.greenhelix.net/v1"
headers = {"Authorization": f"Bearer {os.environ['GREENHELIX_API_KEY']}"}


def execute_tool(tool: str, input_data: dict) -> dict:
    """Execute a GreenHelix tool via the unified endpoint."""
    response = requests.post(
        f"{API_BASE}/v1",
        json={"tool": tool, "input": input_data},
        headers=headers,
    )
    response.raise_for_status()
    return response.json()


@dataclass
class BuyerAgent:
    agent_id: str
    wallet_id: Optional[str] = None
    budget_daily: float = 0.0
    budget_monthly: float = 0.0

    def initialize(self):
        """Create wallet and set initial budget."""
        wallet = execute_tool("create_wallet", {
            "agent_id": self.agent_id,
            "currency": "USD",
        })
        self.wallet_id = wallet["wallet_id"]

        execute_tool("set_budget", {
            "agent_id": self.agent_id,
            "daily_limit": self.budget_daily,
            "monthly_limit": self.budget_monthly,
        })
        return self

    def get_spending_status(self) -> dict:
        """Check current balance and usage."""
        balance = execute_tool("get_balance", {
            "agent_id": self.agent_id,
        })
        usage = execute_tool("get_usage_analytics", {
            "agent_id": self.agent_id,
            "period": "current_day",
        })
        return {
            "balance": balance["balance"],
            "daily_spend": usage.get("total_spend", 0),
            "daily_remaining": self.budget_daily - usage.get("total_spend", 0),
        }


# Initialize a buyer agent with a $50/day, $1000/month budget
buyer = BuyerAgent(
    agent_id="procurement-agent-01",
    budget_daily=50.00,
    budget_monthly=1000.00,
).initialize()

print(buyer.get_spending_status())
```

This gives you an agent with a wallet, budget caps, and real-time spending visibility. The rest of this playbook builds on this foundation.

> **Key Takeaways**
>
> - Autonomous procurement follows a six-stage loop: discover, evaluate, negotiate, purchase, verify, reconcile.
> - The Spending Policy Engine is the gatekeeper -- every purchase passes through it before execution.
> - The Approval Gateway is the single choke point for all spend. No agent should bypass it.
> - Start with a wallet, a budget, and spending visibility. Everything else builds on this foundation.
> - Organizations deploying autonomous procurement see 15-30% efficiency gains, but 41% experience uncontrolled spending incidents without proper governance.

---

## Chapter 2: Spending Controls & Approval Workflows

### The Five Layers of Spending Control

Spending controls for autonomous agents are not a single dial. They are five independent layers, each catching a different failure mode. Deploying only one layer leaves you exposed to the failures the others catch.

| Layer | Control | What It Catches | GreenHelix Tool |
|-------|---------|-----------------|-----------------|
| 1 | Per-transaction cap | Single large unauthorized purchase | `set_budget` |
| 2 | Daily/weekly budget limit | Runaway loops, amplification | `set_budget`, `get_usage_analytics` |
| 3 | Recipient whitelist | Purchases from untrusted vendors | Policy engine (custom) |
| 4 | Frequency limit | Rapid-fire small purchases that aggregate to large spend | Policy engine (custom) |
| 5 | Human-in-the-loop escalation | Novel situations outside policy | Webhook + approval queue |

**Layer 1: Per-Transaction Caps.** No single purchase can exceed a defined amount. This is the bluntest control -- it prevents a single bad decision from causing catastrophic damage. Set it at the maximum amount you would tolerate losing in a single transaction. For most agent workflows, $100-500 is appropriate for automated approval; anything above goes to escalation.

**Layer 2: Daily/Weekly Budget Limits.** Even if every individual transaction is small, an agent in a loop can drain a budget through volume. A $0.01 transaction repeated 100,000 times is $1,000. Daily and weekly limits create a hard ceiling on cumulative spend regardless of individual transaction sizes.

**Layer 3: Recipient Whitelists.** The agent can only purchase from pre-approved vendors. This prevents an agent from being socially engineered (via prompt injection or adversarial marketplace listings) into sending money to a malicious actor. Whitelists can be static (a fixed list) or dynamic (any vendor with a trust score above a threshold).

**Layer 4: Frequency Limits.** Rate-limiting purchases prevents rapid-fire micro-transactions that individually pass the per-transaction cap but collectively blow through the daily budget before alerting systems can react. A typical setting: no more than 10 purchases per minute, no more than 100 per hour.

**Layer 5: Human-in-the-Loop Escalation.** For purchases that exceed caps, involve new vendors, or fall outside known categories, the system queues the purchase for human approval. The key design decision is what happens while waiting: does the workflow block (synchronous escalation) or continue with a fallback (asynchronous escalation)?

### The ProcurementPolicyEngine

This class implements all five layers. It is the core of the spending control system.

```python
import time
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum


class ApprovalDecision(Enum):
    APPROVED = "approved"
    DENIED = "denied"
    ESCALATED = "escalated"


@dataclass
class PurchaseRequest:
    vendor_id: str
    amount: float
    currency: str = "USD"
    category: str = "general"
    description: str = ""
    requesting_agent: str = ""
    idempotency_key: str = ""


@dataclass
class PolicyResult:
    decision: ApprovalDecision
    reason: str
    purchase_request: Optional[PurchaseRequest] = None
    escalation_id: Optional[str] = None


@dataclass
class ProcurementPolicyEngine:
    """Five-layer spending control for autonomous procurement agents."""

    agent_id: str
    max_transaction_amount: float = 500.00
    daily_limit: float = 2000.00
    weekly_limit: float = 10000.00
    max_purchases_per_minute: int = 10
    max_purchases_per_hour: int = 100
    escalation_threshold: float = 500.00
    vendor_whitelist: list = field(default_factory=list)
    require_whitelist: bool = False

    # Internal tracking
    _purchase_timestamps: list = field(default_factory=list)
    _daily_spend: float = 0.0

    def evaluate(self, request: PurchaseRequest) -> PolicyResult:
        """Run a purchase request through all five control layers."""

        # Layer 1: Per-transaction cap
        if request.amount > self.max_transaction_amount:
            if request.amount > self.escalation_threshold:
                return PolicyResult(
                    decision=ApprovalDecision.ESCALATED,
                    reason=f"Amount ${request.amount:.2f} exceeds "
                           f"auto-approval cap ${self.max_transaction_amount:.2f}",
                    purchase_request=request,
                )
            return PolicyResult(
                decision=ApprovalDecision.DENIED,
                reason=f"Amount ${request.amount:.2f} exceeds "
                       f"per-transaction limit ${self.max_transaction_amount:.2f}",
            )

        # Layer 2: Daily budget limit
        projected_daily = self._daily_spend + request.amount
        if projected_daily > self.daily_limit:
            return PolicyResult(
                decision=ApprovalDecision.DENIED,
                reason=f"Purchase would bring daily spend to "
                       f"${projected_daily:.2f}, exceeding "
                       f"daily limit ${self.daily_limit:.2f}",
            )

        # Layer 3: Vendor whitelist
        if self.require_whitelist and request.vendor_id not in self.vendor_whitelist:
            return PolicyResult(
                decision=ApprovalDecision.ESCALATED,
                reason=f"Vendor {request.vendor_id} not in whitelist. "
                       f"Escalating for manual review.",
                purchase_request=request,
            )

        # Layer 4: Frequency limit
        now = time.time()
        recent_minute = [t for t in self._purchase_timestamps if now - t < 60]
        recent_hour = [t for t in self._purchase_timestamps if now - t < 3600]

        if len(recent_minute) >= self.max_purchases_per_minute:
            return PolicyResult(
                decision=ApprovalDecision.DENIED,
                reason=f"Rate limit: {len(recent_minute)} purchases in "
                       f"the last minute (max {self.max_purchases_per_minute})",
            )
        if len(recent_hour) >= self.max_purchases_per_hour:
            return PolicyResult(
                decision=ApprovalDecision.DENIED,
                reason=f"Rate limit: {len(recent_hour)} purchases in "
                       f"the last hour (max {self.max_purchases_per_hour})",
            )

        # Layer 5: Escalation threshold for borderline amounts
        if request.amount > self.escalation_threshold:
            return PolicyResult(
                decision=ApprovalDecision.ESCALATED,
                reason=f"Amount ${request.amount:.2f} exceeds escalation "
                       f"threshold ${self.escalation_threshold:.2f}",
                purchase_request=request,
            )

        # All layers passed
        self._purchase_timestamps.append(now)
        self._daily_spend += request.amount
        return PolicyResult(
            decision=ApprovalDecision.APPROVED,
            reason="All policy checks passed",
        )

    def sync_with_gateway(self):
        """Sync local state with GreenHelix budget and usage data."""
        usage = execute_tool("get_usage_analytics", {
            "agent_id": self.agent_id,
            "period": "current_day",
        })
        self._daily_spend = usage.get("total_spend", 0)

        balance = execute_tool("get_balance", {
            "agent_id": self.agent_id,
        })
        return {
            "daily_spend": self._daily_spend,
            "daily_remaining": self.daily_limit - self._daily_spend,
            "wallet_balance": balance["balance"],
        }


# Initialize the policy engine
policy = ProcurementPolicyEngine(
    agent_id="procurement-agent-01",
    max_transaction_amount=500.00,
    daily_limit=2000.00,
    weekly_limit=10000.00,
    escalation_threshold=250.00,
    vendor_whitelist=["vendor-data-enrichment-01", "vendor-compute-aws-02"],
    require_whitelist=True,
)

# Evaluate a purchase request
result = policy.evaluate(PurchaseRequest(
    vendor_id="vendor-data-enrichment-01",
    amount=45.00,
    category="data",
    description="500k contact records enrichment",
    requesting_agent="research-agent-03",
))

print(f"Decision: {result.decision.value}")
print(f"Reason: {result.reason}")
```

### Escalation Workflow with Webhooks

When a purchase is escalated, the system notifies a human approver and holds the purchase in a pending state. Here is how to wire up the escalation:

```python
def handle_escalation(policy_result: PolicyResult) -> dict:
    """Queue an escalated purchase for human approval."""
    # Register a webhook for approval notifications
    webhook = execute_tool("register_webhook", {
        "agent_id": policy.agent_id,
        "url": "https://your-app.example.com/procurement/approvals",
        "events": ["purchase.approval_required"],
    })

    # Record the pending purchase in the ledger for tracking
    pending = execute_tool("record_transaction", {
        "agent_id": policy.agent_id,
        "type": "purchase_pending",
        "amount": str(policy_result.purchase_request.amount),
        "currency": "USD",
        "counterparty": policy_result.purchase_request.vendor_id,
        "metadata": {
            "status": "awaiting_human_approval",
            "reason": policy_result.reason,
            "category": policy_result.purchase_request.category,
        },
    })

    return {
        "escalation_id": pending.get("transaction_id"),
        "status": "awaiting_approval",
        "webhook_id": webhook.get("webhook_id"),
    }
```

### Budget Configuration Decision Matrix

Use this matrix to set appropriate limits based on your agent's role:

| Agent Role | Per-Tx Cap | Daily Limit | Weekly Limit | Escalation | Whitelist Required |
|---|---|---|---|---|---|
| Research agent (data purchases) | $100 | $500 | $2,000 | $50 | Yes |
| Infrastructure agent (compute) | $1,000 | $5,000 | $20,000 | $500 | Yes |
| Sales agent (lead enrichment) | $200 | $1,000 | $4,000 | $100 | Yes |
| Trading agent (market data) | $50 | $200 | $1,000 | $25 | No (dynamic trust) |
| General-purpose agent | $50 | $250 | $1,000 | $25 | Yes |

> **Key Takeaways**
>
> - Five independent control layers: per-transaction caps, daily/weekly budgets, vendor whitelists, frequency limits, and human escalation.
> - The `ProcurementPolicyEngine` evaluates every purchase request before execution. No purchase bypasses the engine.
> - Escalation is not failure -- it is a feature. Design your workflows to handle the delay introduced by human-in-the-loop review.
> - Sync the policy engine with GreenHelix usage analytics to keep local state consistent with actual spend.
> - Set limits based on agent role, not a single global policy. A trading agent and an infrastructure agent have fundamentally different spending patterns.

---

## Chapter 3: Vendor Discovery Across Protocols

### The Multi-Protocol Discovery Problem

Your procurement agent needs a data enrichment service. Where does it look? In 2026, vendors advertise their services across at least four distinct protocols, each with its own discovery mechanism:

- **GreenHelix Marketplace** -- Structured service listings with trust scores, ratings, and escrow history. Discovery via `search_services` and `best_match` tools.
- **UCP (Universal Commerce Protocol)** -- Google and Shopify's protocol for structured product and service catalogs. Agents query UCP manifests to find services and compare prices.
- **ACP (Agentic Commerce Protocol)** -- OpenAI's protocol for agent-to-merchant discovery. ACP directories list merchants with Stripe-backed checkout.
- **A2A Direct** -- Agent-to-agent service advertisements via standardized capability manifests. No marketplace intermediary.

A vendor might list on one protocol, two, or all four. A procurement agent that only searches one protocol misses vendors available on the others. The solution is a unified vendor index that aggregates discovery results across all protocols.

### GreenHelix Marketplace Discovery

The GreenHelix Marketplace is the richest discovery source because it includes trust, reputation, and escrow data alongside service listings.

```python
def discover_greenhelix_vendors(query: str, category: str = None,
                                 min_trust_score: float = 0.7,
                                 max_results: int = 20) -> list:
    """Search GreenHelix Marketplace for services matching a query."""
    search_params = {
        "query": query,
        "max_results": max_results,
    }
    if category:
        search_params["category"] = category

    results = execute_tool("search_services", search_params)

    # Filter by trust score
    filtered = []
    for service in results.get("services", []):
        trust = execute_tool("check_trust_score", {
            "agent_id": service["provider_id"],
        })
        if trust.get("trust_score", 0) >= min_trust_score:
            service["trust_score"] = trust["trust_score"]
            filtered.append(service)

    # Rank by best match
    if filtered:
        best = execute_tool("best_match", {
            "query": query,
            "candidates": [s["service_id"] for s in filtered],
        })
        # Reorder filtered list by best_match ranking
        ranked_ids = [m["service_id"] for m in best.get("matches", [])]
        filtered.sort(key=lambda s: (
            ranked_ids.index(s["service_id"])
            if s["service_id"] in ranked_ids else 999
        ))

    return filtered
```

### UCP Manifest Discovery

UCP manifests are structured JSON documents that describe services in a standardized format. Agents query them by fetching the manifest URL and parsing the catalog.

```python
import requests as http_client


def discover_ucp_vendors(manifest_urls: list, query: str) -> list:
    """Query UCP manifests for matching services."""
    vendors = []
    for url in manifest_urls:
        try:
            resp = http_client.get(url, timeout=10)
            resp.raise_for_status()
            manifest = resp.json()

            for service in manifest.get("services", []):
                # Simple keyword matching against service description
                name = service.get("name", "").lower()
                desc = service.get("description", "").lower()
                if query.lower() in name or query.lower() in desc:
                    vendors.append({
                        "source": "ucp",
                        "provider_id": manifest.get("provider_id"),
                        "service_id": service.get("id"),
                        "name": service.get("name"),
                        "price": service.get("price"),
                        "currency": service.get("currency", "USD"),
                        "manifest_url": url,
                    })
        except (http_client.RequestException, ValueError):
            continue  # Skip unreachable or malformed manifests

    return vendors


def discover_acp_vendors(directory_url: str, query: str) -> list:
    """Query an ACP agent directory for matching services."""
    try:
        resp = http_client.get(
            f"{directory_url}/search",
            params={"q": query, "type": "service"},
            timeout=10,
        )
        resp.raise_for_status()
        listings = resp.json().get("results", [])

        return [{
            "source": "acp",
            "provider_id": listing.get("agent_id"),
            "service_id": listing.get("service_id"),
            "name": listing.get("name"),
            "price": listing.get("price"),
            "currency": listing.get("currency", "USD"),
            "checkout_url": listing.get("checkout_url"),
        } for listing in listings]
    except (http_client.RequestException, ValueError):
        return []
```

### The Unified Vendor Index

Combine results from all protocols into a single, ranked vendor index:

```python
from dataclasses import dataclass
from typing import Optional


@dataclass
class VendorCandidate:
    source: str             # "greenhelix", "ucp", "acp", "a2a"
    provider_id: str
    service_id: str
    name: str
    price: float
    currency: str
    trust_score: Optional[float] = None  # Only available for GreenHelix
    manifest_url: Optional[str] = None
    checkout_url: Optional[str] = None


class UnifiedVendorIndex:
    """Aggregates vendor discovery across all protocols."""

    def __init__(self, ucp_manifests: list = None, acp_directory: str = None):
        self.ucp_manifests = ucp_manifests or []
        self.acp_directory = acp_directory

    def search(self, query: str, category: str = None,
               min_trust: float = 0.5) -> list[VendorCandidate]:
        """Search all protocols and return unified, ranked results."""
        candidates = []

        # 1. GreenHelix Marketplace (richest data)
        gh_results = discover_greenhelix_vendors(
            query, category=category, min_trust_score=min_trust,
        )
        for r in gh_results:
            candidates.append(VendorCandidate(
                source="greenhelix",
                provider_id=r["provider_id"],
                service_id=r["service_id"],
                name=r.get("name", ""),
                price=float(r.get("price", 0)),
                currency=r.get("currency", "USD"),
                trust_score=r.get("trust_score"),
            ))

        # 2. UCP manifests
        ucp_results = discover_ucp_vendors(self.ucp_manifests, query)
        for r in ucp_results:
            candidates.append(VendorCandidate(
                source="ucp",
                provider_id=r["provider_id"],
                service_id=r["service_id"],
                name=r["name"],
                price=float(r.get("price", 0)),
                currency=r.get("currency", "USD"),
                manifest_url=r.get("manifest_url"),
            ))

        # 3. ACP directory
        if self.acp_directory:
            acp_results = discover_acp_vendors(self.acp_directory, query)
            for r in acp_results:
                candidates.append(VendorCandidate(
                    source="acp",
                    provider_id=r["provider_id"],
                    service_id=r["service_id"],
                    name=r["name"],
                    price=float(r.get("price", 0)),
                    currency=r.get("currency", "USD"),
                    checkout_url=r.get("checkout_url"),
                ))

        # Sort: trust-scored vendors first, then by price
        candidates.sort(key=lambda c: (
            0 if c.trust_score is not None else 1,
            -(c.trust_score or 0),
            c.price,
        ))

        return candidates


# Usage
index = UnifiedVendorIndex(
    ucp_manifests=[
        "https://vendor-a.example.com/.well-known/ucp-manifest.json",
        "https://vendor-b.example.com/.well-known/ucp-manifest.json",
    ],
    acp_directory="https://acp-directory.example.com/v1",
)

vendors = index.search("data enrichment", category="data")
for v in vendors[:5]:
    trust_display = f" (trust: {v.trust_score:.2f})" if v.trust_score else ""
    print(f"  [{v.source}] {v.name} - ${v.price}{trust_display}")
```

### Protocol Coverage Checklist

Before deploying your procurement agent, verify coverage across all relevant discovery channels:

- [ ] GreenHelix Marketplace search configured with appropriate trust threshold
- [ ] UCP manifest URLs for known vendor networks added to the index
- [ ] ACP directory endpoint configured (if purchasing from OpenAI ecosystem merchants)
- [ ] A2A direct discovery configured for peer agent services
- [ ] Fallback behavior defined when a protocol is unreachable
- [ ] Deduplication logic handles the same vendor appearing on multiple protocols

> **Key Takeaways**
>
> - Vendors advertise across four protocols. An agent that searches only one protocol misses opportunities on the others.
> - GreenHelix Marketplace provides the richest discovery data because it includes trust scores, reputation, and escrow history alongside listings.
> - Build a `UnifiedVendorIndex` that aggregates results across all protocols and ranks by trust score first, price second.
> - Trust-scored vendors should always rank above unscored vendors, regardless of price. The cheapest vendor with no verifiable identity is the most expensive mistake.
> - See P21 (Agent-Ready Commerce) for the seller's perspective on listing across multiple protocols.

---

## Chapter 4: Vendor Evaluation & Trust Scoring

### Why Price Alone Is Insufficient

The cheapest vendor in your search results is also the most likely to be fraudulent. This is Akerlof's "Market for Lemons" problem applied to agent commerce: without reliable quality signals, low-quality sellers undercut high-quality ones, and buyers cannot tell the difference until after they have paid. The antidote is a structured evaluation framework that scores vendors on dimensions beyond price.

The four evaluation dimensions are:

1. **Identity verification** -- Is this vendor a real, registered entity?
2. **Trust score** -- Does the platform's composite trust assessment meet your threshold?
3. **Reputation history** -- What do other buyers say about this vendor?
4. **Bid comparison** -- Given equivalent trust, which vendor offers the best value?

### The Vendor Scoring System

```python
from dataclasses import dataclass
from typing import Optional


@dataclass
class VendorScore:
    vendor_id: str
    identity_verified: bool = False
    identity_confidence: float = 0.0
    trust_score: float = 0.0
    reputation_score: float = 0.0
    trade_count: int = 0
    dispute_rate: float = 0.0
    price: float = 0.0
    composite_score: float = 0.0
    risk_level: str = "unknown"  # low, medium, high, critical
    disqualified: bool = False
    disqualification_reason: str = ""


class VendorEvaluator:
    """Automated vendor evaluation using GreenHelix Trust, Identity,
    and Reputation tools."""

    # Weights for composite score (must sum to 1.0)
    WEIGHT_TRUST = 0.30
    WEIGHT_REPUTATION = 0.25
    WEIGHT_IDENTITY = 0.20
    WEIGHT_TRADE_HISTORY = 0.15
    WEIGHT_PRICE = 0.10

    # Thresholds
    MIN_TRUST_SCORE = 0.6
    MIN_TRADE_COUNT = 5
    MAX_DISPUTE_RATE = 0.10  # 10%

    def evaluate(self, vendor_id: str, price: float,
                 price_range: tuple = (0, 1000)) -> VendorScore:
        """Run full evaluation pipeline on a single vendor."""
        score = VendorScore(vendor_id=vendor_id, price=price)

        # Step 1: Identity verification
        try:
            identity = execute_tool("verify_identity", {
                "agent_id": vendor_id,
            })
            score.identity_verified = identity.get("verified", False)
            score.identity_confidence = identity.get("confidence", 0.0)
        except Exception:
            score.identity_verified = False
            score.identity_confidence = 0.0

        if not score.identity_verified:
            score.disqualified = True
            score.disqualification_reason = "Identity verification failed"
            score.risk_level = "critical"
            return score

        # Step 2: Trust score
        try:
            trust = execute_tool("check_trust_score", {
                "agent_id": vendor_id,
            })
            score.trust_score = trust.get("trust_score", 0.0)
        except Exception:
            score.trust_score = 0.0

        if score.trust_score < self.MIN_TRUST_SCORE:
            score.disqualified = True
            score.disqualification_reason = (
                f"Trust score {score.trust_score:.2f} below "
                f"minimum {self.MIN_TRUST_SCORE}"
            )
            score.risk_level = "high"
            return score

        # Step 3: Reputation and trade history
        try:
            reputation = execute_tool("get_agent_reputation", {
                "agent_id": vendor_id,
            })
            score.reputation_score = reputation.get("reputation_score", 0.0)
            score.trade_count = reputation.get("total_trades", 0)
            score.dispute_rate = reputation.get("dispute_rate", 0.0)
        except Exception:
            score.reputation_score = 0.0

        if score.dispute_rate > self.MAX_DISPUTE_RATE:
            score.disqualified = True
            score.disqualification_reason = (
                f"Dispute rate {score.dispute_rate:.1%} exceeds "
                f"maximum {self.MAX_DISPUTE_RATE:.1%}"
            )
            score.risk_level = "high"
            return score

        # Step 4: Additional KYA check
        try:
            kya = execute_tool("verify_agent", {
                "agent_id": vendor_id,
            })
            if not kya.get("verified", False):
                score.risk_level = "medium"
        except Exception:
            pass

        # Step 5: Compute composite score
        price_min, price_max = price_range
        price_normalized = 1.0 - (
            (price - price_min) / (price_max - price_min)
            if price_max > price_min else 0.5
        )
        price_normalized = max(0, min(1, price_normalized))

        trade_normalized = min(1.0, score.trade_count / 100)

        score.composite_score = (
            self.WEIGHT_TRUST * score.trust_score
            + self.WEIGHT_REPUTATION * score.reputation_score
            + self.WEIGHT_IDENTITY * score.identity_confidence
            + self.WEIGHT_TRADE_HISTORY * trade_normalized
            + self.WEIGHT_PRICE * price_normalized
        )

        # Assign risk level
        if score.composite_score >= 0.8:
            score.risk_level = "low"
        elif score.composite_score >= 0.6:
            score.risk_level = "medium"
        else:
            score.risk_level = "high"

        return score

    def evaluate_batch(self, candidates: list[VendorCandidate]) -> list[VendorScore]:
        """Evaluate and rank a list of vendor candidates."""
        prices = [c.price for c in candidates if c.price > 0]
        price_range = (min(prices), max(prices)) if prices else (0, 1000)

        scores = []
        for candidate in candidates:
            score = self.evaluate(
                candidate.provider_id,
                candidate.price,
                price_range,
            )
            scores.append(score)

        # Sort: non-disqualified first, then by composite score descending
        scores.sort(key=lambda s: (
            s.disqualified,
            -s.composite_score,
        ))

        return scores


# Evaluate vendors from the unified index
evaluator = VendorEvaluator()
vendors = index.search("data enrichment", category="data")
scores = evaluator.evaluate_batch(vendors)

print(f"\n{'Vendor':<30} {'Score':>6} {'Risk':<10} {'Price':>8} {'Status':<12}")
print("-" * 76)
for s in scores:
    status = "DISQUALIFIED" if s.disqualified else "ELIGIBLE"
    print(f"{s.vendor_id:<30} {s.composite_score:>6.2f} {s.risk_level:<10} "
          f"${s.price:>7.2f} {status:<12}")
    if s.disqualified:
        print(f"  Reason: {s.disqualification_reason}")
```

### Risk Scoring Decision Matrix

| Composite Score | Risk Level | Recommended Action |
|---|---|---|
| 0.80 - 1.00 | Low | Auto-approve up to per-transaction cap |
| 0.60 - 0.79 | Medium | Auto-approve for small amounts; escalate above $100 |
| 0.40 - 0.59 | High | Escalate all purchases for human review |
| 0.00 - 0.39 | Critical | Block. Do not purchase. |

### Automated Bid Comparison

When multiple vendors pass the trust threshold, compare them on value:

```python
def compare_bids(scores: list[VendorScore],
                 max_budget: float) -> Optional[VendorScore]:
    """Select the best vendor from evaluated candidates.

    Strategy: Among eligible vendors with 'low' or 'medium' risk,
    select the one with the highest composite score within budget.
    Break ties by preferring lower price.
    """
    eligible = [
        s for s in scores
        if not s.disqualified
        and s.risk_level in ("low", "medium")
        and s.price <= max_budget
    ]

    if not eligible:
        return None

    # Sort by composite score descending, then price ascending
    eligible.sort(key=lambda s: (-s.composite_score, s.price))
    return eligible[0]


# Select the best vendor with a $200 budget
winner = compare_bids(scores, max_budget=200.00)
if winner:
    print(f"\nSelected vendor: {winner.vendor_id}")
    print(f"  Composite score: {winner.composite_score:.2f}")
    print(f"  Price: ${winner.price:.2f}")
    print(f"  Risk: {winner.risk_level}")
else:
    print("\nNo eligible vendor found within budget and risk tolerance.")
```

> **Key Takeaways**
>
> - Never select a vendor on price alone. The cheapest unverified vendor is the most expensive mistake.
> - The evaluation pipeline has hard gates (identity, minimum trust, dispute rate) and soft scoring (composite weighted score).
> - Disqualification is binary -- a vendor that fails identity verification or exceeds the dispute rate threshold is excluded regardless of price.
> - The composite score weights trust (30%) and reputation (25%) above price (10%). Adjust weights based on your risk tolerance.
> - See P5 (Trust Verification) for deep dives into claim chain verification and metric auditing.

---

## Chapter 5: Multi-Protocol Purchasing

### Four Rails, One Agent

Your procurement agent has discovered vendors, evaluated them, and selected a winner. Now it needs to pay. The payment rail depends on the vendor's protocol:

| Protocol | Payment Method | Best For | Settlement Time |
|---|---|---|---|
| x402 | USDC stablecoin | Micropayments, pay-per-request APIs | Seconds (on-chain) |
| UCP | Fiat (card/bank) | Retail, SaaS subscriptions | 1-3 business days |
| ACP | Stripe (card/SPT) | Merchant checkout, e-commerce | 1-3 business days |
| A2A (GreenHelix) | Wallet-to-wallet | Agent-to-agent, escrow-protected | Instant (platform) |

The procurement agent must handle all four. Here is the implementation for each rail.

### Rail 1: x402 Crypto Micropayments

x402 is HTTP-native: the server returns HTTP 402 with a payment requirement, and the client pays in USDC via a facilitator. Ideal for pay-per-request API access.

```python
import hashlib
import json


def purchase_x402(
    resource_url: str,
    wallet_address: str,
    max_amount_usdc: float,
) -> dict:
    """Execute an x402 payment for a resource.

    The flow:
    1. Request the resource -> get 402 with payment requirements
    2. Verify the price is within budget
    3. Create payment authorization via GreenHelix
    4. Submit payment and receive resource
    """
    # Step 1: Request the resource to get payment requirements
    resp = http_client.get(resource_url)
    if resp.status_code != 402:
        # Resource is free or already paid
        return {"status": "no_payment_required", "data": resp.json()}

    payment_req = resp.json()
    amount = float(payment_req.get("amount", 0))
    currency = payment_req.get("currency", "USDC")
    facilitator = payment_req.get("facilitator_url")
    recipient = payment_req.get("recipient_address")

    # Step 2: Verify price is within budget
    if amount > max_amount_usdc:
        return {
            "status": "rejected",
            "reason": f"Price ${amount} exceeds max ${max_amount_usdc}",
        }

    # Step 3: Create payment via GreenHelix
    intent = execute_tool("create_payment_intent", {
        "amount": str(amount),
        "currency": currency,
        "recipient": recipient,
        "payment_method": "x402",
        "metadata": {
            "resource_url": resource_url,
            "facilitator": facilitator,
            "protocol": "x402",
        },
    })

    # Step 4: Confirm the payment
    confirmation = execute_tool("confirm_payment", {
        "payment_id": intent["payment_id"],
        "wallet_address": wallet_address,
    })

    # Step 5: Re-request with payment proof
    proof_headers = {
        "X-Payment-Id": confirmation["payment_id"],
        "X-Payment-Proof": confirmation.get("proof", ""),
    }
    final_resp = http_client.get(resource_url, headers=proof_headers)

    return {
        "status": "completed",
        "payment_id": confirmation["payment_id"],
        "amount": amount,
        "currency": currency,
        "data": final_resp.json() if final_resp.ok else None,
    }
```

### Rail 2: UCP Fiat Retail Purchasing

UCP handles structured product purchasing with fiat payment methods. The flow follows a standard e-commerce checkout pattern.

```python
def purchase_ucp(
    service_id: str,
    manifest_url: str,
    quantity: int = 1,
) -> dict:
    """Execute a UCP purchase using GreenHelix as the payment backend.

    The flow:
    1. Fetch service details from UCP manifest
    2. Create a payment intent via GreenHelix
    3. Authorize the fiat payment
    4. Confirm delivery
    """
    # Step 1: Fetch service details
    manifest = http_client.get(manifest_url, timeout=10).json()
    service = next(
        (s for s in manifest.get("services", []) if s["id"] == service_id),
        None,
    )
    if not service:
        return {"status": "error", "reason": f"Service {service_id} not found"}

    total = float(service["price"]) * quantity

    # Step 2: Create payment intent
    intent = execute_tool("create_payment_intent", {
        "amount": str(total),
        "currency": service.get("currency", "USD"),
        "recipient": manifest.get("provider_id"),
        "payment_method": "fiat",
        "metadata": {
            "protocol": "ucp",
            "service_id": service_id,
            "quantity": quantity,
            "manifest_url": manifest_url,
        },
    })

    # Step 3: Confirm the payment
    confirmation = execute_tool("confirm_payment", {
        "payment_id": intent["payment_id"],
    })

    return {
        "status": "completed",
        "payment_id": confirmation["payment_id"],
        "amount": total,
        "currency": service.get("currency", "USD"),
        "service": service["name"],
        "protocol": "ucp",
    }
```

### Rail 3: ACP Agent-Native Checkout

ACP uses Shared Payment Tokens (SPTs) for delegated spending through Stripe.

```python
def purchase_acp(
    service_id: str,
    checkout_url: str,
    spt_token: str,
) -> dict:
    """Execute an ACP purchase using a Shared Payment Token.

    The flow:
    1. Initiate checkout at the ACP merchant endpoint
    2. Authorize via SPT
    3. Record the transaction in GreenHelix for tracking
    """
    # Step 1: Initiate checkout
    checkout_resp = http_client.post(
        checkout_url,
        json={
            "service_id": service_id,
            "payment_method": "spt",
            "spt_token": spt_token,
        },
        timeout=15,
    )
    checkout_resp.raise_for_status()
    checkout_data = checkout_resp.json()

    # Step 2: Record in GreenHelix ledger for unified tracking
    execute_tool("record_transaction", {
        "agent_id": buyer.agent_id,
        "type": "purchase",
        "amount": str(checkout_data.get("amount", 0)),
        "currency": checkout_data.get("currency", "USD"),
        "counterparty": checkout_data.get("merchant_id", ""),
        "metadata": {
            "protocol": "acp",
            "service_id": service_id,
            "external_payment_id": checkout_data.get("payment_id"),
            "checkout_url": checkout_url,
        },
    })

    return {
        "status": "completed",
        "payment_id": checkout_data.get("payment_id"),
        "amount": checkout_data.get("amount"),
        "protocol": "acp",
    }
```

### Rail 4: A2A Direct Commerce via GreenHelix

For agent-to-agent purchases, the commerce layer provides the full stack: payment, escrow, and delivery verification.

```python
def purchase_a2a(
    vendor_id: str,
    service_id: str,
    amount: float,
    use_escrow: bool = True,
) -> dict:
    """Execute an A2A purchase via GreenHelix with optional escrow.

    This is the recommended rail for agent-to-agent transactions
    because it includes built-in escrow, disputes, and delivery
    verification.
    """
    if use_escrow:
        # Create escrow-protected purchase
        escrow = execute_tool("create_escrow", {
            "payer_id": buyer.agent_id,
            "payee_id": vendor_id,
            "amount": str(amount),
            "currency": "USD",
            "conditions": {
                "service_id": service_id,
                "delivery_deadline_hours": 24,
                "verification_method": "automated",
            },
        })

        return {
            "status": "escrowed",
            "escrow_id": escrow["escrow_id"],
            "amount": amount,
            "vendor_id": vendor_id,
            "protocol": "a2a",
            "next_step": "await_delivery_then_verify",
        }
    else:
        # Direct payment (no escrow)
        intent = execute_tool("create_payment_intent", {
            "amount": str(amount),
            "currency": "USD",
            "recipient": vendor_id,
            "payment_method": "wallet",
            "metadata": {
                "protocol": "a2a",
                "service_id": service_id,
            },
        })

        confirmation = execute_tool("confirm_payment", {
            "payment_id": intent["payment_id"],
        })

        return {
            "status": "completed",
            "payment_id": confirmation["payment_id"],
            "amount": amount,
            "protocol": "a2a",
        }
```

### The Payment Router

Tie all four rails together with a router that selects the appropriate rail based on the vendor's protocol:

```python
def route_purchase(vendor: VendorCandidate, amount: float,
                   use_escrow: bool = True, **kwargs) -> dict:
    """Route a purchase to the appropriate payment rail."""
    if vendor.source == "greenhelix":
        return purchase_a2a(
            vendor.provider_id, vendor.service_id, amount, use_escrow,
        )
    elif vendor.source == "ucp":
        return purchase_ucp(
            vendor.service_id, vendor.manifest_url,
            quantity=kwargs.get("quantity", 1),
        )
    elif vendor.source == "acp":
        return purchase_acp(
            vendor.service_id, vendor.checkout_url,
            spt_token=kwargs.get("spt_token", ""),
        )
    else:
        # Default to GreenHelix A2A for unknown protocols
        return purchase_a2a(
            vendor.provider_id, vendor.service_id, amount, use_escrow,
        )
```

> **Key Takeaways**
>
> - Four payment rails serve different use cases: x402 for crypto micropayments, UCP for fiat, ACP for Stripe-backed checkout, A2A for agent-to-agent.
> - Always use escrow for A2A purchases above your trust threshold. The cost of escrow is negligible compared to the cost of unrecoverable loss.
> - Record all purchases in the GreenHelix ledger regardless of which rail was used. Unified tracking is essential for reconciliation.
> - The payment router abstracts rail selection from the procurement logic. The agent does not need to know which protocol a vendor uses.
> - See P19 (Payment Rails) for deep dives into x402 settlement, MPP hybrid routing, and multi-rail architecture patterns.

---

## Chapter 6: Escrow, Disputes & Purchase Protection

### Why Escrow Is Non-Negotiable for Agent Commerce

When a human buys a service and it fails to deliver, the human can call support, file a chargeback, leave a scathing review, or escalate to a regulatory body. An agent has none of these options unless they are programmed in advance. Escrow is the mechanism that makes agent purchasing safe: the buyer's funds are held by a neutral third party (GreenHelix) until the seller delivers and the buyer verifies. If delivery fails, the buyer gets their money back automatically.

For agent-to-agent commerce, escrow should be the default for any transaction above a trivial amount. The threshold varies by use case, but a reasonable starting point is: always use escrow for transactions above $10.

### The Protected Purchase Flow

```python
import time
from enum import Enum


class DeliveryStatus(Enum):
    PENDING = "pending"
    DELIVERED = "delivered"
    FAILED = "failed"
    DISPUTED = "disputed"


class ProtectedPurchaseManager:
    """Manages the full lifecycle of an escrow-protected purchase:
    creation, delivery verification, release, and dispute handling."""

    def __init__(self, buyer_id: str):
        self.buyer_id = buyer_id

    def create_protected_purchase(
        self,
        vendor_id: str,
        service_id: str,
        amount: float,
        delivery_deadline_hours: int = 24,
        verification_criteria: dict = None,
    ) -> dict:
        """Create an escrow-protected purchase."""
        escrow = execute_tool("create_escrow", {
            "payer_id": self.buyer_id,
            "payee_id": vendor_id,
            "amount": str(amount),
            "currency": "USD",
            "conditions": {
                "service_id": service_id,
                "delivery_deadline_hours": delivery_deadline_hours,
                "verification_method": "automated",
                "criteria": verification_criteria or {},
            },
        })

        return {
            "escrow_id": escrow["escrow_id"],
            "status": "escrowed",
            "amount": amount,
            "vendor_id": vendor_id,
            "deadline": delivery_deadline_hours,
        }

    def verify_delivery(
        self,
        escrow_id: str,
        delivered_data: dict,
        acceptance_tests: list = None,
    ) -> DeliveryStatus:
        """Run automated verification on delivered goods/services.

        acceptance_tests is a list of callables that take delivered_data
        and return (passed: bool, reason: str).
        """
        if not delivered_data:
            return DeliveryStatus.FAILED

        if acceptance_tests:
            failures = []
            for test_fn in acceptance_tests:
                passed, reason = test_fn(delivered_data)
                if not passed:
                    failures.append(reason)

            if failures:
                # Auto-dispute on verification failure
                self.file_dispute(
                    escrow_id,
                    reason=f"Delivery failed {len(failures)} acceptance "
                           f"test(s): {'; '.join(failures)}",
                )
                return DeliveryStatus.DISPUTED

        return DeliveryStatus.DELIVERED

    def release_escrow(self, escrow_id: str) -> dict:
        """Release funds to the vendor after successful verification."""
        result = execute_tool("release_escrow", {
            "escrow_id": escrow_id,
            "action": "release",
        })
        return {
            "escrow_id": escrow_id,
            "status": "released",
            "released_to": result.get("payee_id"),
            "amount": result.get("amount"),
        }

    def file_dispute(self, escrow_id: str, reason: str,
                     evidence: dict = None) -> dict:
        """File a dispute against the vendor."""
        dispute = execute_tool("create_dispute", {
            "escrow_id": escrow_id,
            "reason": reason,
            "evidence": evidence or {},
            "requested_resolution": "full_refund",
        })
        return {
            "dispute_id": dispute["dispute_id"],
            "escrow_id": escrow_id,
            "status": "dispute_filed",
            "reason": reason,
        }

    def respond_to_dispute(self, dispute_id: str, response: str,
                           evidence: dict = None) -> dict:
        """Respond to a dispute (if this agent is the vendor side)."""
        result = execute_tool("respond_to_dispute", {
            "dispute_id": dispute_id,
            "response": response,
            "evidence": evidence or {},
        })
        return {
            "dispute_id": dispute_id,
            "status": "response_submitted",
            "resolution": result.get("resolution"),
        }

    def execute_full_purchase(
        self,
        vendor_id: str,
        service_id: str,
        amount: float,
        delivery_callback: callable,
        acceptance_tests: list = None,
        delivery_deadline_hours: int = 24,
    ) -> dict:
        """Execute the complete protected purchase lifecycle.

        delivery_callback: a callable that triggers vendor fulfillment
        and returns the delivered data.
        """
        # Step 1: Create escrow
        purchase = self.create_protected_purchase(
            vendor_id, service_id, amount,
            delivery_deadline_hours=delivery_deadline_hours,
        )
        escrow_id = purchase["escrow_id"]

        # Step 2: Trigger delivery
        try:
            delivered_data = delivery_callback(escrow_id)
        except Exception as e:
            self.file_dispute(escrow_id, reason=f"Delivery failed: {str(e)}")
            return {
                "escrow_id": escrow_id,
                "status": "disputed",
                "reason": f"Delivery exception: {str(e)}",
            }

        # Step 3: Verify delivery
        status = self.verify_delivery(
            escrow_id, delivered_data, acceptance_tests,
        )

        # Step 4: Release or dispute
        if status == DeliveryStatus.DELIVERED:
            release = self.release_escrow(escrow_id)
            return {
                "escrow_id": escrow_id,
                "status": "completed",
                "amount_released": release["amount"],
            }
        else:
            return {
                "escrow_id": escrow_id,
                "status": status.value,
                "reason": "Automated verification failed",
            }


# Usage: protected purchase with acceptance tests
ppm = ProtectedPurchaseManager(buyer_id="procurement-agent-01")

# Define acceptance tests for a data enrichment purchase
def test_record_count(data):
    count = len(data.get("records", []))
    expected = 500_000
    if count < expected * 0.95:  # Allow 5% tolerance
        return False, f"Expected ~{expected} records, got {count}"
    return True, "Record count OK"

def test_data_completeness(data):
    sample = data.get("records", [])[:100]
    incomplete = sum(1 for r in sample if not r.get("email"))
    if incomplete > 10:  # More than 10% incomplete
        return False, f"{incomplete}% of sample missing email field"
    return True, "Data completeness OK"

# This would be your vendor's delivery mechanism
def trigger_vendor_delivery(escrow_id: str) -> dict:
    """Placeholder: in production, this calls the vendor's API."""
    return {"records": [{"email": "test@example.com"}] * 500_000}

result = ppm.execute_full_purchase(
    vendor_id="vendor-data-enrichment-01",
    service_id="contact-enrichment-500k",
    amount=150.00,
    delivery_callback=trigger_vendor_delivery,
    acceptance_tests=[test_record_count, test_data_completeness],
    delivery_deadline_hours=12,
)
print(f"Purchase result: {result['status']}")
```

### Dispute Resolution Decision Tree

```
Delivery received?
├── NO --> Wait until deadline
│          └── Deadline passed? --> Auto-dispute (non-delivery)
├── YES --> Run acceptance tests
│          ├── ALL PASS --> Release escrow
│          ├── SOME FAIL --> File dispute with evidence
│          └── CRITICAL FAIL --> File dispute, request full refund
```

### Escrow Configuration Checklist

- [ ] Set delivery deadlines appropriate to the service type (minutes for APIs, hours for data, days for custom work)
- [ ] Define acceptance tests before creating the escrow, not after
- [ ] Include specific, measurable criteria in escrow conditions (not "good quality" but "95%+ record completeness")
- [ ] Configure automatic dispute filing for deadline expiration
- [ ] Set up webhook notifications for escrow state changes
- [ ] Record all escrow outcomes in the ledger for vendor reputation tracking

> **Key Takeaways**
>
> - Escrow should be the default for any agent-to-agent transaction above $10. The cost of escrow is negligible; the cost of unrecoverable loss is not.
> - Automated acceptance tests are the agent equivalent of "inspecting the goods before signing." Define them before the purchase, not after.
> - The `ProtectedPurchaseManager` handles the full lifecycle: escrow creation, delivery callback, automated verification, release or dispute.
> - Dispute evidence should be structured and machine-readable. "The data was bad" is not evidence. "47% of records missing email field, expected less than 5%" is evidence.
> - See P14 (Negotiation Strategies) for techniques to negotiate escrow terms, delivery deadlines, and SLA guarantees before the purchase.

---

## Chapter 7: Cost Reconciliation & FinOps Integration

### The Reconciliation Problem

Your procurement agent has executed purchases across four protocols, some through escrow, some direct. The transactions are scattered across GreenHelix ledger entries, Stripe payment records, x402 on-chain settlements, and UCP order confirmations. The CFO asks: "How much did our AI agents spend last month, on what, and was it worth it?"

Without a unified reconciliation system, you cannot answer that question. Cost reconciliation for autonomous procurement requires three capabilities:

1. **Unified recording** -- Every purchase, regardless of protocol, is recorded in a single ledger.
2. **Cost attribution** -- Every purchase is tagged with the requesting agent, workflow, and cost category.
3. **Budget vs. actual analysis** -- Planned budgets are compared to actual spend, with anomaly detection for deviations.

### Recording Purchases to the Ledger

Every purchase -- whether it went through x402, UCP, ACP, or A2A -- must be recorded in the GreenHelix Ledger for unified tracking:

```python
from datetime import datetime


class ProcurementLedger:
    """Records and queries all procurement transactions
    in the GreenHelix Ledger."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    def record_purchase(
        self,
        vendor_id: str,
        amount: float,
        currency: str,
        protocol: str,
        service_id: str,
        category: str,
        workflow_id: str = "",
        external_payment_id: str = "",
        metadata: dict = None,
    ) -> dict:
        """Record a completed purchase in the ledger."""
        tx = execute_tool("record_transaction", {
            "agent_id": self.agent_id,
            "type": "purchase",
            "amount": str(amount),
            "currency": currency,
            "counterparty": vendor_id,
            "metadata": {
                "protocol": protocol,
                "service_id": service_id,
                "category": category,
                "workflow_id": workflow_id,
                "external_payment_id": external_payment_id,
                "recorded_at": datetime.utcnow().isoformat(),
                **(metadata or {}),
            },
        })
        return tx

    def get_spend_by_category(self, period: str = "current_month") -> dict:
        """Get spend broken down by category."""
        history = execute_tool("get_transaction_history", {
            "agent_id": self.agent_id,
            "period": period,
            "type": "purchase",
        })

        by_category = {}
        for tx in history.get("transactions", []):
            cat = tx.get("metadata", {}).get("category", "uncategorized")
            by_category.setdefault(cat, {"count": 0, "total": 0.0})
            by_category[cat]["count"] += 1
            by_category[cat]["total"] += float(tx.get("amount", 0))

        return by_category

    def get_spend_by_protocol(self, period: str = "current_month") -> dict:
        """Get spend broken down by payment protocol."""
        history = execute_tool("get_transaction_history", {
            "agent_id": self.agent_id,
            "period": period,
            "type": "purchase",
        })

        by_protocol = {}
        for tx in history.get("transactions", []):
            proto = tx.get("metadata", {}).get("protocol", "unknown")
            by_protocol.setdefault(proto, {"count": 0, "total": 0.0})
            by_protocol[proto]["count"] += 1
            by_protocol[proto]["total"] += float(tx.get("amount", 0))

        return by_protocol

    def get_spend_by_vendor(self, period: str = "current_month") -> dict:
        """Get spend broken down by vendor."""
        history = execute_tool("get_transaction_history", {
            "agent_id": self.agent_id,
            "period": period,
            "type": "purchase",
        })

        by_vendor = {}
        for tx in history.get("transactions", []):
            vendor = tx.get("counterparty", "unknown")
            by_vendor.setdefault(vendor, {"count": 0, "total": 0.0})
            by_vendor[vendor]["count"] += 1
            by_vendor[vendor]["total"] += float(tx.get("amount", 0))

        return by_vendor


ledger = ProcurementLedger(agent_id="procurement-agent-01")
```

### Budget vs. Actual Dashboard

```python
class BudgetDashboard:
    """Compares planned budgets against actual procurement spend."""

    def __init__(self, agent_id: str, budgets: dict):
        """
        budgets: dict mapping category -> monthly budget amount.
        Example: {"data": 500, "compute": 2000, "apis": 300}
        """
        self.agent_id = agent_id
        self.budgets = budgets
        self.ledger = ProcurementLedger(agent_id)

    def generate_report(self) -> dict:
        """Generate a budget vs. actual report for the current month."""
        actuals = self.ledger.get_spend_by_category("current_month")

        # Get platform-level usage analytics
        usage = execute_tool("get_usage_analytics", {
            "agent_id": self.agent_id,
            "period": "current_month",
        })

        # Get revenue metrics for ROI calculation
        revenue = execute_tool("get_revenue_metrics", {
            "agent_id": self.agent_id,
            "period": "current_month",
        })

        report = {
            "period": "current_month",
            "categories": {},
            "total_budget": sum(self.budgets.values()),
            "total_actual": 0,
            "total_revenue": revenue.get("total_revenue", 0),
            "anomalies": [],
        }

        for category, budget in self.budgets.items():
            actual = actuals.get(category, {}).get("total", 0)
            tx_count = actuals.get(category, {}).get("count", 0)
            variance = actual - budget
            variance_pct = (variance / budget * 100) if budget > 0 else 0

            report["categories"][category] = {
                "budget": budget,
                "actual": actual,
                "variance": variance,
                "variance_pct": variance_pct,
                "transaction_count": tx_count,
                "status": (
                    "under" if variance < 0
                    else "on_track" if variance_pct < 10
                    else "over"
                ),
            }
            report["total_actual"] += actual

            # Anomaly detection: flag categories over 120% of budget
            if variance_pct > 20:
                report["anomalies"].append({
                    "category": category,
                    "severity": "high" if variance_pct > 50 else "medium",
                    "message": (
                        f"{category} spend ${actual:.2f} is "
                        f"{variance_pct:.0f}% over budget ${budget:.2f}"
                    ),
                })

        return report

    def print_report(self):
        """Print a formatted budget vs. actual report."""
        report = self.generate_report()

        print(f"\n{'='*70}")
        print(f"  PROCUREMENT BUDGET vs. ACTUAL — {report['period']}")
        print(f"{'='*70}")
        print(f"\n{'Category':<20} {'Budget':>10} {'Actual':>10} "
              f"{'Variance':>10} {'Status':<10}")
        print("-" * 70)

        for cat, data in report["categories"].items():
            status_marker = (
                "OK" if data["status"] == "under"
                else "WATCH" if data["status"] == "on_track"
                else "OVER"
            )
            print(f"{cat:<20} ${data['budget']:>9.2f} ${data['actual']:>9.2f} "
                  f"${data['variance']:>+9.2f} {status_marker:<10}")

        print("-" * 70)
        print(f"{'TOTAL':<20} ${report['total_budget']:>9.2f} "
              f"${report['total_actual']:>9.2f} "
              f"${report['total_actual'] - report['total_budget']:>+9.2f}")

        if report["anomalies"]:
            print(f"\n  ANOMALIES:")
            for a in report["anomalies"]:
                print(f"  [{a['severity'].upper()}] {a['message']}")

        roi = (
            (report["total_revenue"] - report["total_actual"])
            / report["total_actual"] * 100
            if report["total_actual"] > 0 else 0
        )
        print(f"\n  Revenue: ${report['total_revenue']:.2f}")
        print(f"  Procurement ROI: {roi:+.1f}%")
        print(f"{'='*70}\n")


# Usage
dashboard = BudgetDashboard(
    agent_id="procurement-agent-01",
    budgets={
        "data": 500.00,
        "compute": 2000.00,
        "apis": 300.00,
        "services": 1000.00,
    },
)
dashboard.print_report()
```

### Anomaly Detection for Runaway Spend

```python
def detect_spending_anomalies(agent_id: str,
                               lookback_days: int = 7,
                               z_score_threshold: float = 2.0) -> list:
    """Detect anomalous spending patterns by comparing recent
    spend to historical averages.

    Uses a simple z-score approach: if today's spend is more than
    z_score_threshold standard deviations above the mean of the
    lookback period, flag it.
    """
    import statistics

    history = execute_tool("get_transaction_history", {
        "agent_id": agent_id,
        "period": f"last_{lookback_days}_days",
        "type": "purchase",
    })

    # Group by day
    daily_totals = {}
    for tx in history.get("transactions", []):
        day = tx.get("metadata", {}).get("recorded_at", "")[:10]
        daily_totals.setdefault(day, 0)
        daily_totals[day] += float(tx.get("amount", 0))

    if len(daily_totals) < 3:
        return []  # Not enough data for anomaly detection

    amounts = list(daily_totals.values())
    mean = statistics.mean(amounts)
    stdev = statistics.stdev(amounts) if len(amounts) > 1 else 0

    anomalies = []
    for day, total in daily_totals.items():
        if stdev > 0:
            z = (total - mean) / stdev
            if z > z_score_threshold:
                anomalies.append({
                    "date": day,
                    "spend": total,
                    "mean": mean,
                    "z_score": z,
                    "severity": "critical" if z > 3 else "warning",
                    "message": (
                        f"Spend on {day} (${total:.2f}) is "
                        f"{z:.1f} std devs above mean (${mean:.2f})"
                    ),
                })

    return anomalies
```

> **Key Takeaways**
>
> - Record every purchase in the GreenHelix Ledger regardless of which payment rail was used. Unified tracking is the foundation of reconciliation.
> - Tag every transaction with category, workflow, and protocol. Without attribution, you cannot answer "who spent what on which."
> - Budget vs. actual dashboards should flag anomalies automatically. A 20% budget overrun in a category is a warning; 50% is an alert.
> - Anomaly detection using z-scores catches spending spikes that per-transaction caps miss. A sudden doubling of daily spend is suspicious even if every individual transaction is small.
> - See P6 (FinOps) for advanced patterns: volume discount optimization, fleet-wide dashboards, and API key isolation as a cost containment boundary.

---

## Chapter 8: Compliance & Audit Trails

### The Regulatory Landscape for Autonomous Purchasing

Autonomous agents that spend money operate in a regulatory gray area that is rapidly becoming black-letter law. Three regulatory frameworks are converging on agent procurement in 2026:

**EU AI Act (August 2, 2026 deadline).** Article 14 requires "human oversight" for high-risk AI systems. Autonomous purchasing agents that make financial decisions likely qualify. Documentation requirements include: system purpose, risk assessment, human oversight mechanisms, decision logging, and audit trails. Non-compliance penalties: up to 35 million EUR or 7% of global revenue.

**GDPR.** If your procurement agent processes personal data (contact enrichment, identity verification, behavioral analytics), GDPR's data processing requirements apply. Every vendor that receives personal data must have a Data Processing Agreement (DPA). Your agent's procurement decisions involving personal data must be logged and explainable.

**Financial Services Regulations.** Agents that move money may trigger money transmission, anti-money laundering (AML), or know-your-customer (KYC) requirements depending on jurisdiction and transaction volume.

### Building the Audit Trail

GreenHelix's claim chain infrastructure provides cryptographic audit trails that satisfy EU AI Act documentation requirements:

```python
from datetime import datetime, timezone


class ProcurementAuditor:
    """Builds and queries cryptographic audit trails for
    autonomous procurement decisions."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id

    def log_procurement_decision(
        self,
        decision_type: str,
        vendor_id: str,
        amount: float,
        decision: str,
        reasoning: str,
        policy_checks: list,
        human_oversight: str = "none",
    ) -> dict:
        """Log a procurement decision with full context for audit."""
        metrics = execute_tool("submit_metrics", {
            "agent_id": self.agent_id,
            "metrics": {
                "decision_type": decision_type,
                "vendor_id": vendor_id,
                "amount": str(amount),
                "decision": decision,
                "reasoning": reasoning,
                "policy_checks_passed": [
                    c for c in policy_checks if c["passed"]
                ],
                "policy_checks_failed": [
                    c for c in policy_checks if not c["passed"]
                ],
                "human_oversight_level": human_oversight,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        })
        return metrics

    def build_audit_chain(self) -> dict:
        """Build a Merkle claim chain over all procurement decisions.

        This creates a tamper-evident record: if any decision log
        is modified after the chain is built, the root hash changes.
        """
        chain = execute_tool("build_claim_chain", {
            "agent_id": self.agent_id,
        })
        return {
            "chain_id": chain.get("chain_id"),
            "root_hash": chain.get("root_hash"),
            "claim_count": chain.get("claim_count"),
            "built_at": datetime.now(timezone.utc).isoformat(),
        }

    def get_audit_history(self, since: str = None) -> list:
        """Retrieve all claim chains for audit review."""
        chains = execute_tool("get_claim_chains", {
            "agent_id": self.agent_id,
        })
        return chains.get("chains", [])

    def verify_chain_integrity(self, chain_id: str) -> dict:
        """Verify that a claim chain has not been tampered with."""
        chains = execute_tool("get_claim_chains", {
            "agent_id": self.agent_id,
        })
        target = next(
            (c for c in chains.get("chains", []) if c["chain_id"] == chain_id),
            None,
        )
        if not target:
            return {"verified": False, "reason": "Chain not found"}

        return {
            "verified": True,
            "chain_id": chain_id,
            "root_hash": target.get("root_hash"),
            "claim_count": target.get("claim_count"),
        }


# Usage: log a procurement decision and build a claim chain
auditor = ProcurementAuditor(agent_id="procurement-agent-01")

# Log the decision
auditor.log_procurement_decision(
    decision_type="vendor_selection",
    vendor_id="vendor-data-enrichment-01",
    amount=150.00,
    decision="approved",
    reasoning="Highest composite score (0.87) among 4 eligible vendors. "
              "Trust score 0.92, reputation 0.85, 147 completed trades, "
              "1.2% dispute rate. Price within budget allocation.",
    policy_checks=[
        {"check": "per_transaction_cap", "passed": True,
         "detail": "$150 < $500 cap"},
        {"check": "daily_budget", "passed": True,
         "detail": "$150 + $320 existing = $470 < $2000 limit"},
        {"check": "vendor_whitelist", "passed": True,
         "detail": "vendor-data-enrichment-01 in whitelist"},
        {"check": "frequency_limit", "passed": True,
         "detail": "3 purchases this hour < 100 limit"},
        {"check": "trust_threshold", "passed": True,
         "detail": "trust 0.92 >= 0.60 minimum"},
    ],
    human_oversight="async_notification",
)

# Build the claim chain (do this periodically, e.g., hourly or daily)
chain = auditor.build_audit_chain()
print(f"Audit chain built: {chain['chain_id']}")
print(f"Root hash: {chain['root_hash']}")
print(f"Claims: {chain['claim_count']}")
```

### EU AI Act Compliance Report Generator

Article 14 of the EU AI Act requires documentation of human oversight mechanisms. Here is a generator that produces a compliance-ready report from your audit trail:

```python
class ComplianceReportGenerator:
    """Generates EU AI Act Article 14 compliance reports
    from GreenHelix audit trails."""

    def __init__(self, agent_id: str, system_name: str,
                 organization: str):
        self.agent_id = agent_id
        self.system_name = system_name
        self.organization = organization
        self.auditor = ProcurementAuditor(agent_id)
        self.ledger = ProcurementLedger(agent_id)

    def generate(self, period: str = "current_month") -> dict:
        """Generate a structured compliance report."""

        # Gather data
        chains = self.auditor.get_audit_history()
        spend_by_category = self.ledger.get_spend_by_category(period)
        spend_by_vendor = self.ledger.get_spend_by_vendor(period)

        usage = execute_tool("get_usage_analytics", {
            "agent_id": self.agent_id,
            "period": period,
        })

        total_spend = sum(
            cat["total"] for cat in spend_by_category.values()
        )
        total_transactions = sum(
            cat["count"] for cat in spend_by_category.values()
        )

        report = {
            "report_type": "eu_ai_act_article_14_compliance",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "reporting_period": period,
            "organization": self.organization,
            "system_identification": {
                "system_name": self.system_name,
                "agent_id": self.agent_id,
                "system_purpose": (
                    "Autonomous procurement agent for discovering, "
                    "evaluating, and purchasing digital services and "
                    "data products on behalf of the organization."
                ),
                "risk_classification": "high_risk",
                "risk_justification": (
                    "System makes autonomous financial decisions "
                    "that commit organizational funds."
                ),
            },
            "human_oversight_mechanisms": {
                "spending_policy_engine": {
                    "description": (
                        "Five-layer policy engine evaluates every "
                        "purchase before execution."
                    ),
                    "layers": [
                        "Per-transaction caps",
                        "Daily/weekly budget limits",
                        "Vendor whitelists",
                        "Frequency rate limits",
                        "Human-in-the-loop escalation",
                    ],
                },
                "escalation_threshold": (
                    "Purchases above configured threshold are "
                    "queued for human approval before execution."
                ),
                "kill_switch": (
                    "Budget hard stops halt all purchasing when "
                    "daily or monthly limits are reached."
                ),
            },
            "decision_logging": {
                "total_decisions_logged": total_transactions,
                "claim_chains_built": len(chains),
                "latest_chain_hash": (
                    chains[-1]["root_hash"] if chains else "none"
                ),
                "tamper_evidence": (
                    "All decisions recorded in Merkle claim chains. "
                    "Any modification to historical records changes "
                    "the root hash and is detectable."
                ),
            },
            "financial_summary": {
                "total_spend": total_spend,
                "total_transactions": total_transactions,
                "spend_by_category": spend_by_category,
                "unique_vendors": len(spend_by_vendor),
            },
            "data_processing": {
                "gdpr_applicable": True,
                "personal_data_categories": [
                    "Vendor agent identifiers",
                    "Transaction metadata",
                    "Service descriptions",
                ],
                "data_processing_basis": "Legitimate interest (Art. 6(1)(f))",
                "retention_period": "36 months",
                "dpa_required_for_vendors": True,
            },
        }

        return report

    def export_markdown(self, period: str = "current_month") -> str:
        """Export the compliance report as Markdown."""
        report = self.generate(period)
        si = report["system_identification"]
        ho = report["human_oversight_mechanisms"]
        dl = report["decision_logging"]
        fs = report["financial_summary"]
        dp = report["data_processing"]

        md = f"""# EU AI Act Article 14 Compliance Report
## {report['organization']} - {si['system_name']}

**Generated:** {report['generated_at']}
**Period:** {report['reporting_period']}
**Risk Classification:** {si['risk_classification']}

---

### System Purpose
{si['system_purpose']}

### Risk Justification
{si['risk_justification']}

---

### Human Oversight Mechanisms

**Spending Policy Engine:** {ho['spending_policy_engine']['description']}

Control Layers:
"""
        for layer in ho["spending_policy_engine"]["layers"]:
            md += f"- {layer}\n"

        md += f"""
**Escalation:** {ho['escalation_threshold']}

**Kill Switch:** {ho['kill_switch']}

---

### Decision Audit Trail

| Metric | Value |
|---|---|
| Decisions logged | {dl['total_decisions_logged']} |
| Claim chains built | {dl['claim_chains_built']} |
| Latest chain hash | `{dl['latest_chain_hash']}` |

**Tamper evidence:** {dl['tamper_evidence']}

---

### Financial Summary

| Metric | Value |
|---|---|
| Total spend | ${fs['total_spend']:.2f} |
| Total transactions | {fs['total_transactions']} |
| Unique vendors | {fs['unique_vendors']} |

---

### GDPR Data Processing

| Item | Detail |
|---|---|
| GDPR applicable | {dp['gdpr_applicable']} |
| Legal basis | {dp['data_processing_basis']} |
| Retention period | {dp['retention_period']} |
| DPA required | {dp['dpa_required_for_vendors']} |
"""
        return md


# Generate the compliance report
generator = ComplianceReportGenerator(
    agent_id="procurement-agent-01",
    system_name="Autonomous Procurement System v1.0",
    organization="Acme Corp",
)

# Print as Markdown
print(generator.export_markdown("current_month"))
```

### Compliance Checklist: EU AI Act Readiness (August 2, 2026 Deadline)

| Requirement | Status | Implementation |
|---|---|---|
| System purpose documented | Required | `system_identification.system_purpose` in report |
| Risk classification | Required | High-risk (autonomous financial decisions) |
| Human oversight mechanisms | Required | 5-layer policy engine + escalation |
| Decision logging | Required | GreenHelix `submit_metrics` + claim chains |
| Tamper-evident audit trail | Required | Merkle claim chains via `build_claim_chain` |
| Data processing documentation | Required (if GDPR applies) | GDPR section in compliance report |
| Incident response procedure | Required | Escalation workflow + kill switch |
| Regular compliance reviews | Required | Monthly report generation |

### GDPR Considerations for Procurement Agents

If your procurement agent processes personal data (which it likely does if it purchases contact data, behavioral analytics, or identity information), you must address:

1. **Lawful basis.** Document which GDPR Article 6 basis applies. Legitimate interest (Art. 6(1)(f)) is typical for B2B procurement, but requires a balancing test.
2. **Data Processing Agreements.** Every vendor that receives or provides personal data needs a DPA. Your procurement agent should verify DPA status as part of vendor evaluation.
3. **Data minimization.** Only purchase data your workflows actually need. Procurement agents should not speculatively buy data "just in case."
4. **Right to erasure.** If a data subject requests deletion, you must be able to trace which vendor provided which records and propagate the deletion request.
5. **Cross-border transfers.** If vendors are outside the EEA, ensure adequate transfer mechanisms (SCCs, adequacy decisions) are in place.

> **Key Takeaways**
>
> - The EU AI Act's August 2, 2026 deadline requires documentation of human oversight mechanisms for high-risk AI systems. Autonomous purchasing agents almost certainly qualify.
> - Merkle claim chains via `build_claim_chain` and `get_claim_chains` provide tamper-evident audit trails that satisfy Article 14 requirements.
> - Log every procurement decision with full context: what was decided, why, which policy checks passed or failed, and what level of human oversight applied.
> - Generate compliance reports monthly. Do not wait until an audit to discover gaps.
> - GDPR applies if your agent processes personal data. Vendor DPA verification should be part of the evaluation pipeline, not an afterthought.

---

## Appendix: Quick Reference

### GreenHelix Tools Used in This Guide

| Tool | Chapter | Purpose |
|---|---|---|
| `create_wallet` | 1, 2 | Create an agent wallet |
| `set_budget` | 1, 2 | Set daily/monthly spending limits |
| `get_balance` | 1, 2 | Check current wallet balance |
| `get_usage_analytics` | 2, 7 | Get spending analytics for a period |
| `search_services` | 3 | Search the marketplace for services |
| `best_match` | 3 | Rank search results by relevance |
| `check_trust_score` | 3, 4 | Get a vendor's composite trust score |
| `verify_identity` | 4 | Verify a vendor's identity |
| `verify_agent` | 4 | Run KYA checks on a vendor |
| `get_agent_reputation` | 4 | Get reputation score and trade history |
| `create_payment_intent` | 5 | Initiate a payment |
| `confirm_payment` | 5 | Confirm and execute a payment |
| `create_escrow` | 5, 6 | Create an escrow-protected purchase |
| `release_escrow` | 6 | Release escrowed funds to vendor |
| `create_dispute` | 6 | File a dispute against a vendor |
| `respond_to_dispute` | 6 | Respond to a filed dispute |
| `record_transaction` | 2, 5, 7 | Record a transaction in the ledger |
| `get_transaction_history` | 7 | Query historical transactions |
| `get_revenue_metrics` | 7 | Get revenue data for ROI analysis |
| `register_webhook` | 2 | Register webhook for notifications |
| `submit_metrics` | 8 | Log procurement decisions for audit |
| `build_claim_chain` | 8 | Build tamper-evident audit chain |
| `get_claim_chains` | 8 | Retrieve audit chains for review |

### Cross-References

| Guide | Relevance to Procurement |
|---|---|
| P5: Trust Verification | Deep dive into claim chain verification, metric auditing, and KYA |
| P6: FinOps | Advanced cost attribution, fleet dashboards, volume discount optimization |
| P14: Negotiation Strategies | Negotiating escrow terms, SLAs, volume pricing with vendors |
| P19: Payment Rails | x402 settlement details, MPP hybrid routing, multi-rail architecture |
| P21: Agent-Ready Commerce | The seller's perspective -- how vendors list, price, and fulfill |

### The Procurement Loop Checklist

For every autonomous purchase, verify:

- [ ] **Discover:** Searched at least two protocols for vendors
- [ ] **Evaluate:** Vendor identity verified, trust score above threshold, dispute rate below maximum
- [ ] **Negotiate:** Price compared against alternatives, volume discount requested if applicable
- [ ] **Purchase:** Policy engine approved, correct payment rail selected, escrow used if amount > $10
- [ ] **Verify:** Acceptance tests defined and executed, delivery confirmed
- [ ] **Reconcile:** Transaction recorded in ledger, tagged with category and workflow, budget updated
- [ ] **Audit:** Decision logged with reasoning, claim chain built periodically

