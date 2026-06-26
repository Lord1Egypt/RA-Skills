---
name: greenhelix-agent-dispute-resolution
version: "1.3.1"
description: "Agent Dispute Resolution & Chargeback Defense. Build automated dispute resolution pipelines, implement Verifiable Intent-compatible evidence chains, and defend against chargebacks in agent-to-agent transactions. Covers disputes, escrow, SLA enforcement, and trust verification with detailed code examples with code."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [disputes, chargebacks, escrow, verifiable-intent, liability, guide, greenhelix, openclaw, ai-agent]
price_usd: 0.0
content_type: markdown
executable: false
install: none
credentials: none
---
# Agent Dispute Resolution & Chargeback Defense

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code, require credentials, or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.


Your autonomous agent just purchased $12,000 of cloud compute from a counterparty agent. The compute never materialized. The escrow is sitting in limbo. The counterparty is unresponsive. Your agent's operating budget is bleeding out while the dispute resolution clock ticks toward automatic release. Meanwhile, the card network that funded the initial deposit is flagging the transaction as potentially fraudulent because no human authorized it. You are now fighting on two fronts: an A2A dispute with a non-performing counterparty and a chargeback from a card issuer that does not understand autonomous purchasing. Welcome to the hardest unsolved problem in agent commerce. This guide gives you the tools, code, and legal context to build dispute resolution systems that win on both fronts. Every pattern uses the GreenHelix A2A Commerce Gateway API, and every workflow can run autonomously -- because when agents transact at machine speed, disputes must resolve at machine speed too.
> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## What You'll Learn
- Chapter 1: The Liability Shift: Why Human-Era Dispute Rules Break for Autonomous Agents
- Chapter 2: Anatomy of an Agent Dispute: Taxonomy of 7 Agentic Failure Modes
- Chapter 3: Building Verifiable Intent Chains: Cryptographic Proof of Agent Authorization
- Chapter 4: The Escrow-First Architecture: Dispute-Ready Transaction Pipelines
- Chapter 5: Automated Evidence Collection & Submission: From Raw Logs to Compelling Evidence 3.0
- Chapter 6: Multi-Party Dispute Resolution Workflows: Filing, Responding, Escalating, and Arbitrating
- Chapter 7: Chargeback Defense for Agent-Initiated Transactions: Card Network Rules Meet A2A Commerce
- Chapter 8: Production Dispute Resolution System: End-to-End Implementation with Monitoring
- What You Get

## Full Guide

# Agent Dispute Resolution & Chargeback Defense

Your autonomous agent just purchased $12,000 of cloud compute from a counterparty agent. The compute never materialized. The escrow is sitting in limbo. The counterparty is unresponsive. Your agent's operating budget is bleeding out while the dispute resolution clock ticks toward automatic release. Meanwhile, the card network that funded the initial deposit is flagging the transaction as potentially fraudulent because no human authorized it. You are now fighting on two fronts: an A2A dispute with a non-performing counterparty and a chargeback from a card issuer that does not understand autonomous purchasing. Welcome to the hardest unsolved problem in agent commerce. This guide gives you the tools, code, and legal context to build dispute resolution systems that win on both fronts. Every pattern uses the GreenHelix A2A Commerce Gateway API, and every workflow can run autonomously -- because when agents transact at machine speed, disputes must resolve at machine speed too.

---


> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## Table of Contents

1. [The Liability Shift: Why Human-Era Dispute Rules Break for Autonomous Agents](#chapter-1-the-liability-shift-why-human-era-dispute-rules-break-for-autonomous-agents)
2. [Anatomy of an Agent Dispute: Taxonomy of 7 Agentic Failure Modes](#chapter-2-anatomy-of-an-agent-dispute-taxonomy-of-7-agentic-failure-modes)
3. [Building Verifiable Intent Chains: Cryptographic Proof of Agent Authorization](#chapter-3-building-verifiable-intent-chains-cryptographic-proof-of-agent-authorization)
4. [The Escrow-First Architecture: Dispute-Ready Transaction Pipelines](#chapter-4-the-escrow-first-architecture-dispute-ready-transaction-pipelines)
5. [Automated Evidence Collection & Submission: From Raw Logs to Compelling Evidence 3.0](#chapter-5-automated-evidence-collection--submission-from-raw-logs-to-compelling-evidence-30)
6. [Multi-Party Dispute Resolution Workflows: Filing, Responding, Escalating, and Arbitrating](#chapter-6-multi-party-dispute-resolution-workflows-filing-responding-escalating-and-arbitrating)
7. [Chargeback Defense for Agent-Initiated Transactions: Card Network Rules Meet A2A Commerce](#chapter-7-chargeback-defense-for-agent-initiated-transactions-card-network-rules-meet-a2a-commerce)
8. [Production Dispute Resolution System: End-to-End Implementation with Monitoring](#chapter-8-production-dispute-resolution-system-end-to-end-implementation-with-monitoring)

---

## Chapter 1: The Liability Shift: Why Human-Era Dispute Rules Break for Autonomous Agents

### The Authorization Gap

Every dispute resolution framework in modern commerce -- Visa's chargeback process, Mastercard's arbitration, PayPal's buyer protection, even small claims court -- assumes a human authorized the transaction. A human clicked "Buy." A human entered a CVV. A human signed a contract. When a dispute arises, the central question is: did the authorized human actually authorize this specific transaction? If yes, the merchant wins. If no, the buyer wins. The entire edifice rests on a binary: human consent was present or it was not.

Autonomous AI agents obliterate this binary. When your procurement agent purchases SaaS licenses from a vendor agent, no human clicked anything. The agent operated within a mandate -- a set of rules and budget constraints you defined -- but the specific transaction was the agent's decision. The agent chose this vendor, this quantity, this price, at this moment. If the purchase goes wrong, who authorized it? You authorized the agent to purchase, but you did not authorize this purchase. The vendor's agent accepted the order, but it was negotiating with software, not a person. The card network processed the payment, but its fraud models were trained on human purchasing patterns that look nothing like autonomous batch procurement at 3 AM.

### Amazon v. Perplexity: The Ruling That Changed Everything

On March 10, 2026, the U.S. District Court for the Western District of Washington granted Amazon a preliminary injunction against Perplexity AI. The core of the ruling: when Perplexity's AI agent accessed Amazon product data on behalf of users, the users' permission to use Perplexity did not constitute authorization from Amazon to scrape its platform. The court drew a sharp line between user permission and merchant authorization. Permission flows downstream from user to agent. Authorization flows upstream from merchant to accessor. They are independent channels, and having one does not imply having the other.

The implications for agent commerce are immediate. When your buying agent initiates a transaction with a selling agent, the buying agent has your permission (via its mandate). But does it have the seller's authorization to transact? If the seller's terms of service require human verification for purchases above $5,000, and your agent bypasses that by operating autonomously, the seller can dispute the transaction on authorization grounds -- even if your agent paid in full and acted within its mandate. The Amazon v. Perplexity ruling established that permission and authorization are legally distinct concepts, and autonomous agents need both.

### The Clifford Chance Analysis: Risk Sits with Customers

Clifford Chance's March 2026 analysis of AI agent liability in commercial transactions found that standard commercial contracts shift virtually all AI agent risk to customers. The analysis examined contract templates from major cloud providers, SaaS platforms, and payment processors, and found a consistent pattern: the human principal who deploys an agent is liable for everything the agent does, including actions that exceed the principal's intent or that the principal could not have anticipated.

No jurisdiction has enacted specific regulation for autonomous AI purchasing. The EU AI Act addresses AI system risk classification but does not define liability for autonomous commercial transactions. The UK's approach defers to existing contract law. The U.S. relies on a patchwork of FTC guidance and state consumer protection statutes that were written for human buyers. This means agents operate in a legal vacuum where the only rules are whatever the counterparty's contract says, and those contracts are written to protect the counterparty.

For dispute resolution, this means you cannot rely on external legal frameworks to protect your agent's interests. You must build the dispute resolution infrastructure yourself: verifiable intent chains that prove what your agent was authorized to do, escrow structures that limit exposure, and evidence collection pipelines that produce documentation card networks and arbitrators will accept.

### The Three-Front War

Agent commerce disputes are fought simultaneously on three fronts:

**Front 1: A2A Dispute Resolution.** The direct dispute between your agent and the counterparty agent. This is handled through the GreenHelix dispute tools (`open_dispute`, `respond_dispute`, `resolve_dispute`) and is the most tractable front because both parties operate within a shared infrastructure with verifiable state.

**Front 2: Card Network Chargebacks.** If the transaction was funded by a card payment, the cardholder (or their bank) can initiate a chargeback through the card network. This front operates under Visa and Mastercard rules that were designed for human commerce and are only now being adapted for agentic transactions.

**Front 3: Regulatory and Contractual Liability.** The legal exposure created by the Clifford Chance gap -- the fact that your agent's actions create liability for you under existing contracts that were not written with autonomous agents in mind.

This guide addresses all three fronts, with the heaviest focus on Fronts 1 and 2 because they are the most technically actionable.

```python
import requests
import json
import hashlib
import time
from typing import Optional, Dict, List
from datetime import datetime, timezone


class DisputeContext:
    """Track the dispute context across all three fronts for a transaction."""

    def __init__(self, api_key: str, agent_id: str,
                 base_url: str = "https://api.greenhelix.net/v1"):
        self.api_key = api_key
        self.agent_id = agent_id
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })

    def _execute(self, tool: str, input_data: dict) -> dict:
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    def assess_dispute_fronts(self, transaction_id: str,
                               escrow_id: str) -> dict:
        """Assess which dispute fronts are active for a transaction."""
        # Check A2A dispute status
        disputes = self._execute("list_disputes", {
            "agent_id": self.agent_id,
        })

        # Check escrow status
        escrows = self._execute("list_escrows", {
            "agent_id": self.agent_id,
        })

        # Check transaction history for card-funded deposits
        history = self._execute("get_transaction_history", {
            "agent_id": self.agent_id,
        })

        active_fronts = []
        a2a_disputes = [
            d for d in disputes.get("disputes", [])
            if d.get("escrow_id") == escrow_id
        ]
        if a2a_disputes:
            active_fronts.append({
                "front": "a2a_dispute",
                "status": a2a_disputes[0].get("status"),
                "dispute_id": a2a_disputes[0].get("dispute_id"),
            })

        card_funded = any(
            t.get("source") == "card" and t.get("reference") == transaction_id
            for t in history.get("transactions", [])
        )
        if card_funded:
            active_fronts.append({
                "front": "card_network",
                "risk": "chargeback_eligible",
                "window_days": 120,
            })

        active_fronts.append({
            "front": "contractual_liability",
            "risk": "principal_liable_for_agent_actions",
            "mitigation": "verifiable_intent_chain",
        })

        return {
            "transaction_id": transaction_id,
            "escrow_id": escrow_id,
            "active_fronts": active_fronts,
            "assessed_at": datetime.now(timezone.utc).isoformat(),
        }
```

---

## Chapter 2: Anatomy of an Agent Dispute: Taxonomy of 7 Agentic Failure Modes

### Why Traditional Dispute Categories Do Not Apply

Visa defines 36 reason codes for chargebacks. Mastercard defines 21. These codes cover scenarios like "merchandise not received," "duplicate processing," "fraud," and "credit not processed." They assume a human buyer, a human-operated merchant, and a single transaction with a clear authorization trail. Agent commerce introduces failure modes that do not map to any existing reason code. When an agent cascades a purchase through three sub-agents and the third sub-agent over-purchases by 400%, which of Visa's 36 reason codes applies? When an agent's intent drifts from "buy cloud compute" to "buy cloud compute and a monitoring service and a backup solution" because its LLM hallucinated additional requirements, is that "merchandise not as described" or "unauthorized transaction"? It is neither. It is an entirely new category of failure.

### The Seven Agentic Failure Modes

The following taxonomy covers every dispute pattern we have observed in production A2A commerce systems. Each mode has distinct evidence requirements and resolution strategies.

| # | Failure Mode | Description | Detection Signal | Evidence Required | GreenHelix Tools |
|---|---|---|---|---|---|
| 1 | **Over-Purchase** | Agent buys more quantity or higher tier than its mandate allows | Transaction amount > mandate ceiling | Mandate hash, transaction log, budget cap status | `get_balance`, `get_transaction_history` |
| 2 | **Hallucinated Order** | Agent fabricates a purchase requirement that does not exist in its task context | No upstream task references the purchased item | Task context log, intent chain, claim chain showing no prior requirement | `build_claim_chain`, `get_transaction_history` |
| 3 | **Unauthorized Merchant** | Agent transacts with a merchant not on its approved vendor list | Merchant ID not in allowlist | Vendor allowlist, transaction record, agent configuration | `get_agent_reputation`, `verify_identity` |
| 4 | **SLA Breach** | Service provider fails to meet agreed performance criteria | SLA metric below threshold | SLA definition, compliance snapshots, performance escrow status | `check_sla_compliance`, `get_sla_status`, `check_performance_escrow` |
| 5 | **Escrow Timeout** | Escrow release conditions are never met, funds locked indefinitely | Escrow age > maximum holding period | Escrow creation record, release conditions, timeout policy | `list_escrows`, `check_performance_escrow` |
| 6 | **Cascading Delegation** | Agent delegates to sub-agents who further delegate, creating an untracked spending chain | Total spend across delegation tree > authorized amount | Delegation tree, per-agent spend, mandate propagation log | `get_transaction_history`, `get_balance` |
| 7 | **Intent Drift** | Agent's purchasing behavior diverges from its original mandate over successive transactions | Semantic distance between recent purchases and original mandate increases over time | Original mandate, purchase history, intent similarity scores | `get_transaction_history`, `build_claim_chain` |

### Failure Mode 1: Over-Purchase

Over-purchase is the most common agentic failure mode and the one that chargebackgurus.com identified as creating an entirely new dispute category with no established resolution path. It occurs when an agent, operating within the general scope of its mandate, exceeds a specific limit. The mandate says "purchase up to 100 GPU-hours per week" and the agent purchases 400 because it interpreted a spike in workload as justification for exceeding the limit.

The critical distinction: over-purchase is not fraud. The agent was authorized to buy. It bought too much. In human commerce, this is equivalent to an employee with a corporate card going over budget -- annoying but not criminal. In agent commerce, it is worse because the agent may have committed irrevocable funds through an escrow that cannot be unwound.

Detection requires comparing every transaction against the agent's active mandate. The mandate must be stored as a verifiable document (see Chapter 3) so that the spending limit at the time of purchase can be proven retroactively.

```python
import requests

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"
base_url = "https://api.greenhelix.net/v1"

# Check agent's current balance and spending against mandate
resp = session.post(f"{base_url}/v1", json={
    "tool": "get_balance",
    "input": {"agent_id": "buyer-agent-001"}
})
balance = resp.json()

resp = session.post(f"{base_url}/v1", json={
    "tool": "get_transaction_history",
    "input": {"agent_id": "buyer-agent-001"}
})
history = resp.json()

# Calculate total spend in current mandate period
mandate_ceiling = 10000  # $100.00 in cents
period_spend = sum(
    t["amount"] for t in history.get("transactions", [])
    if t.get("direction") == "outbound"
    and t.get("timestamp", "") >= "2026-04-01T00:00:00Z"
)

if period_spend > mandate_ceiling:
    over_amount = period_spend - mandate_ceiling
    print(f"OVER-PURCHASE DETECTED: ${over_amount/100:.2f} over mandate ceiling")
```

### Failure Mode 2: Hallucinated Order

Hallucinated orders are unique to LLM-based agents. The agent's language model generates a purchase requirement that does not exist in any upstream task, user instruction, or business logic. The agent genuinely believes it needs to buy the item because its context window contains hallucinated justification. This is not a bug in the purchasing code -- it is a bug in the reasoning that precedes the purchasing code.

Detection is harder than over-purchase because you need to prove a negative: no legitimate requirement for this purchase exists. The strongest evidence is an intent chain (Chapter 3) that shows a gap -- the purchase has no parent intent, no task reference, and no mandate clause that authorizes it.

### Failure Mode 3: Unauthorized Merchant

The agent transacts with a merchant that is not on its approved vendor list. This can happen when the agent discovers a cheaper option through marketplace search and acts on it without checking its vendor allowlist, or when a malicious agent impersonates an approved vendor.

```python
import requests

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"
base_url = "https://api.greenhelix.net/v1"

# Verify a counterparty agent's identity before transacting
resp = session.post(f"{base_url}/v1", json={
    "tool": "verify_identity",
    "input": {"agent_id": "vendor-agent-xyz"}
})
identity = resp.json()

# Check reputation to assess vendor reliability
resp = session.post(f"{base_url}/v1", json={
    "tool": "get_agent_reputation",
    "input": {"agent_id": "vendor-agent-xyz"}
})
reputation = resp.json()

approved_vendors = ["vendor-agent-001", "vendor-agent-002", "vendor-agent-003"]
if identity.get("agent_id") not in approved_vendors:
    print(f"UNAUTHORIZED MERCHANT: {identity.get('agent_id')} not in allowlist")
    print(f"Reputation score: {reputation.get('reputation_score', 'unknown')}")
```

### Failure Mode 4: SLA Breach

The vendor agent agreed to specific performance criteria -- 99.9% uptime, sub-200ms latency, 95% accuracy -- and failed to meet them. SLA breaches are the most clear-cut dispute type because the criteria were defined in advance and compliance is measurable. The GreenHelix SLA tools provide both the definition and the measurement.

```python
import requests

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"
base_url = "https://api.greenhelix.net/v1"

# Check SLA compliance for an active agreement
resp = session.post(f"{base_url}/v1", json={
    "tool": "check_sla_compliance",
    "input": {
        "agent_id": "buyer-agent-001",
        "sla_id": "sla-compute-2026-04",
    }
})
compliance = resp.json()

if not compliance.get("compliant", True):
    violations = compliance.get("violations", [])
    print(f"SLA BREACH DETECTED: {len(violations)} violation(s)")
    for v in violations:
        print(f"  - {v.get('metric')}: {v.get('actual')} vs {v.get('threshold')}")
```

### Failure Mode 5: Escrow Timeout

Funds locked in escrow with release conditions that are never met. The vendor never delivers. The buyer cannot recover funds because the escrow contract requires explicit release or dispute. If neither party acts, the funds sit indefinitely. This is the agent commerce equivalent of a stalled transaction, and it drains working capital from the buyer's agent.

### Failure Mode 6: Cascading Delegation

Agent A delegates a task to Agent B, who delegates part of it to Agent C, who hires Agent D. Each delegation includes a budget allocation. If the sub-agents do not properly propagate budget limits, the total spend across the delegation tree can exceed Agent A's authorized amount by multiples. The buyer sees a single charge but the money has been split across agents they never authorized to transact.

### Failure Mode 7: Intent Drift

Over many transactions, an agent's purchasing behavior gradually diverges from its original mandate. No single purchase violates the mandate, but the aggregate pattern does. The agent was mandated to buy compute resources, and over six weeks it has also purchased monitoring tools, alerting services, a backup solution, and a disaster recovery plan. Each purchase is defensible in isolation ("monitoring is related to compute") but the drift is cumulative and unauthorized.

---

## Chapter 3: Building Verifiable Intent Chains: Cryptographic Proof of Agent Authorization

### The Core Problem: Proving What the Agent Was Allowed to Do

When a dispute arises, the first question is always: was this transaction authorized? For human transactions, the answer is a signature, a PIN, a biometric scan. For agent transactions, the answer must be a verifiable intent chain -- a cryptographic record that links every transaction back to the human principal's mandate through an unbroken chain of authorization.

Mastercard's Verifiable Intent specification, open-sourced on March 5, 2026, in collaboration with Google, Fiserv, IBM, and Checkout.com, defines a standard for this chain. The specification requires three elements: (1) a mandate signed by the human principal, (2) a delegation chain showing how authorization flowed from the mandate to the executing agent, and (3) a transaction record linked to a specific mandate clause. GreenHelix's claim chain tools implement a compatible pattern.

### Mandate Hashing

The mandate is the root of every intent chain. It is the human-readable document that defines what the agent is authorized to do, and it must be stored as a cryptographic hash so that any modification is detectable. The hash serves as the mandate's fingerprint -- it can be verified without revealing the mandate's contents (selective disclosure).

```python
import requests
import hashlib
import json
import time

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"
base_url = "https://api.greenhelix.net/v1"

# Define the agent's mandate
mandate = {
    "principal": "human-operator-001",
    "agent_id": "buyer-agent-001",
    "authorized_actions": ["purchase_compute", "purchase_storage"],
    "budget_ceiling_cents": 50000,
    "approved_vendors": ["vendor-agent-001", "vendor-agent-002"],
    "valid_from": "2026-04-01T00:00:00Z",
    "valid_until": "2026-04-30T23:59:59Z",
    "version": 1,
}

# Hash the mandate for verifiable reference
mandate_bytes = json.dumps(mandate, sort_keys=True).encode("utf-8")
mandate_hash = hashlib.sha256(mandate_bytes).hexdigest()

# Register the mandate hash as a claim chain entry
resp = session.post(f"{base_url}/v1", json={
    "tool": "build_claim_chain",
    "input": {
        "agent_id": "buyer-agent-001",
        "claims": [
            {
                "type": "mandate_registration",
                "mandate_hash": mandate_hash,
                "principal": "human-operator-001",
                "valid_from": mandate["valid_from"],
                "valid_until": mandate["valid_until"],
            }
        ],
    }
})
chain = resp.json()
print(f"Mandate registered in claim chain: {chain.get('chain_id')}")
print(f"Mandate hash: {mandate_hash}")
```

### Linking Transactions to Mandate Clauses

Every transaction the agent initiates must reference a specific mandate clause. This creates the provenance chain: mandate clause -> intent -> transaction. When a dispute arises, the defender can produce the mandate, show the specific clause that authorized the action, and prove via the hash that the mandate has not been modified since registration.

```python
import requests
import hashlib
import json

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"
base_url = "https://api.greenhelix.net/v1"

# Create an intent that references the mandate
intent_record = {
    "agent_id": "buyer-agent-001",
    "action": "purchase_compute",
    "vendor": "vendor-agent-001",
    "amount_cents": 5000,
    "mandate_hash": mandate_hash,
    "mandate_clause": "authorized_actions[0]",
    "justification": "Weekly compute allocation for batch processing pipeline",
    "timestamp": "2026-04-06T10:30:00Z",
}

# Hash the intent for the chain
intent_bytes = json.dumps(intent_record, sort_keys=True).encode("utf-8")
intent_hash = hashlib.sha256(intent_bytes).hexdigest()

# Record the intent in the claim chain before executing the transaction
resp = session.post(f"{base_url}/v1", json={
    "tool": "build_claim_chain",
    "input": {
        "agent_id": "buyer-agent-001",
        "claims": [
            {
                "type": "transaction_intent",
                "intent_hash": intent_hash,
                "mandate_hash": mandate_hash,
                "action": "purchase_compute",
                "amount_cents": 5000,
                "vendor": "vendor-agent-001",
            }
        ],
    }
})
intent_chain = resp.json()
print(f"Intent recorded: {intent_chain.get('chain_id')}")

# Now execute the actual transaction via escrow
resp = session.post(f"{base_url}/v1", json={
    "tool": "create_escrow",
    "input": {
        "payer_id": "buyer-agent-001",
        "payee_id": "vendor-agent-001",
        "amount": 5000,
        "intent_hash": intent_hash,
        "conditions": {
            "delivery_deadline": "2026-04-07T10:30:00Z",
            "sla_id": "sla-compute-2026-04",
        },
    }
})
escrow = resp.json()
print(f"Escrow created: {escrow.get('escrow_id')}")
print(f"Linked to intent: {intent_hash}")
```

### Selective Disclosure for Dispute Evidence

During a dispute, you may need to prove that a specific mandate clause authorized a transaction without revealing the entire mandate (which may contain budget ceilings, vendor lists, and other competitively sensitive information). Selective disclosure allows you to reveal only the relevant clause and prove it belongs to the registered mandate hash.

```python
import hashlib
import json


def create_selective_disclosure(mandate: dict, clause_path: str) -> dict:
    """Create a selective disclosure proof for a specific mandate clause.

    Reveals only the requested clause while proving it belongs to
    the full mandate via the registered hash.
    """
    # Extract the specific clause value
    keys = clause_path.split(".")
    value = mandate
    for key in keys:
        if key.endswith("]"):
            field, idx = key[:-1].split("[")
            value = value[field][int(idx)]
        else:
            value = value[key]

    # Compute the full mandate hash (verifier already has this from the chain)
    mandate_bytes = json.dumps(mandate, sort_keys=True).encode("utf-8")
    full_hash = hashlib.sha256(mandate_bytes).hexdigest()

    return {
        "clause_path": clause_path,
        "clause_value": value,
        "full_mandate_hash": full_hash,
        "full_mandate": mandate,  # Provided to verifier under NDA/escrow
        "verification_method": "sha256_json_sorted_keys",
    }


# Example: prove that purchase_compute was an authorized action
proof = create_selective_disclosure(mandate, "authorized_actions[0]")
print(f"Disclosed clause: {proof['clause_path']} = {proof['clause_value']}")
print(f"Mandate hash: {proof['full_mandate_hash']}")
```

### The Verifiable Intent Class

The following class wraps the entire intent chain workflow into a reusable component. It handles mandate registration, intent recording, transaction linking, and selective disclosure proof generation.

```python
import requests
import hashlib
import json
import time
from typing import Optional, Dict, Any


class VerifiableIntentChain:
    """Implements Mastercard Verifiable Intent-compatible authorization chains.

    Records mandate -> intent -> transaction provenance using
    GreenHelix claim chains for cryptographic tamper evidence.
    """

    def __init__(self, api_key: str, agent_id: str,
                 base_url: str = "https://api.greenhelix.net/v1"):
        self.agent_id = agent_id
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })
        self.mandate: Optional[dict] = None
        self.mandate_hash: Optional[str] = None
        self.intents: Dict[str, dict] = {}  # intent_hash -> intent_record

    def _execute(self, tool: str, input_data: dict) -> dict:
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def _hash(data: dict) -> str:
        return hashlib.sha256(
            json.dumps(data, sort_keys=True).encode("utf-8")
        ).hexdigest()

    def register_mandate(self, mandate: dict) -> str:
        """Register a mandate and record its hash in the claim chain."""
        self.mandate = mandate
        self.mandate_hash = self._hash(mandate)

        self._execute("build_claim_chain", {
            "agent_id": self.agent_id,
            "claims": [{
                "type": "mandate_registration",
                "mandate_hash": self.mandate_hash,
                "principal": mandate.get("principal"),
                "valid_from": mandate.get("valid_from"),
                "valid_until": mandate.get("valid_until"),
            }],
        })
        return self.mandate_hash

    def record_intent(self, action: str, vendor: str,
                      amount_cents: int, mandate_clause: str,
                      justification: str) -> str:
        """Record a transaction intent linked to a mandate clause."""
        if not self.mandate_hash:
            raise ValueError("No mandate registered. Call register_mandate first.")

        intent = {
            "agent_id": self.agent_id,
            "action": action,
            "vendor": vendor,
            "amount_cents": amount_cents,
            "mandate_hash": self.mandate_hash,
            "mandate_clause": mandate_clause,
            "justification": justification,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }
        intent_hash = self._hash(intent)
        self.intents[intent_hash] = intent

        self._execute("build_claim_chain", {
            "agent_id": self.agent_id,
            "claims": [{
                "type": "transaction_intent",
                "intent_hash": intent_hash,
                "mandate_hash": self.mandate_hash,
                "action": action,
                "amount_cents": amount_cents,
                "vendor": vendor,
            }],
        })
        return intent_hash

    def validate_against_mandate(self, action: str, vendor: str,
                                  amount_cents: int) -> Dict[str, Any]:
        """Check if a proposed transaction is authorized by the mandate."""
        if not self.mandate:
            return {"authorized": False, "reason": "no_mandate_registered"}

        checks = {
            "action_authorized": action in self.mandate.get("authorized_actions", []),
            "vendor_approved": vendor in self.mandate.get("approved_vendors", []),
            "within_budget": amount_cents <= self.mandate.get("budget_ceiling_cents", 0),
            "mandate_valid": (
                self.mandate.get("valid_from", "") <= time.strftime(
                    "%Y-%m-%dT%H:%M:%SZ", time.gmtime()
                ) <= self.mandate.get("valid_until", "")
            ),
        }
        authorized = all(checks.values())
        failed = [k for k, v in checks.items() if not v]

        return {
            "authorized": authorized,
            "checks": checks,
            "failed_checks": failed,
            "mandate_hash": self.mandate_hash,
        }

    def generate_dispute_evidence(self, intent_hash: str) -> Dict[str, Any]:
        """Generate a complete evidence package for dispute defense."""
        intent = self.intents.get(intent_hash)
        if not intent:
            return {"error": "intent_not_found"}

        return {
            "intent_hash": intent_hash,
            "intent_record": intent,
            "mandate_hash": self.mandate_hash,
            "chain_verification": "verify via build_claim_chain audit",
            "provenance": {
                "principal": self.mandate.get("principal"),
                "mandate_clause": intent.get("mandate_clause"),
                "justification": intent.get("justification"),
            },
        }
```

---

## Chapter 4: The Escrow-First Architecture: Dispute-Ready Transaction Pipelines

### Why Direct Payments Are Indefensible

If your agent sends money directly to a counterparty via a simple transfer, and the counterparty does not deliver, your recovery options are limited to filing a dispute after the fact and hoping the counterparty cooperates. This is equivalent to mailing cash with a note that says "please send goods." No reasonable human does this, and no reasonable agent should either.

The escrow-first architecture reverses the power dynamic. Funds are committed to a neutral escrow account with explicit release conditions. The counterparty can see that the funds exist (reducing their risk of non-payment) but cannot access them until the conditions are met (reducing your risk of non-delivery). If conditions are not met, the funds return to the buyer. If there is a dispute about whether conditions were met, both parties have a defined resolution path.

Every transaction in a dispute-ready pipeline goes through escrow. No exceptions. Even small transactions. The incremental cost of escrow (one extra API call) is negligible compared to the cost of an unrecoverable payment.

### Performance Escrow with SLA Criteria

Performance escrow adds measurable criteria to the release conditions. Instead of "release when the buyer confirms delivery," the condition is "release when SLA metrics confirm delivery quality." This removes subjective judgment from the release decision and creates objective evidence for disputes.

```python
import requests
import time

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"
base_url = "https://api.greenhelix.net/v1"

# Step 1: Define the SLA
resp = session.post(f"{base_url}/v1", json={
    "tool": "create_sla",
    "input": {
        "agent_id": "buyer-agent-001",
        "provider_id": "vendor-agent-001",
        "metrics": {
            "uptime_percent": {"threshold": 99.5, "comparison": "gte"},
            "response_time_ms": {"threshold": 200, "comparison": "lte"},
            "accuracy_percent": {"threshold": 95.0, "comparison": "gte"},
        },
        "evaluation_period": "2026-04-06T00:00:00Z/2026-04-13T00:00:00Z",
    }
})
sla = resp.json()
sla_id = sla.get("sla_id")
print(f"SLA created: {sla_id}")

# Step 2: Create performance escrow linked to the SLA
resp = session.post(f"{base_url}/v1", json={
    "tool": "create_performance_escrow",
    "input": {
        "payer_id": "buyer-agent-001",
        "payee_id": "vendor-agent-001",
        "amount": 10000,
        "sla_id": sla_id,
        "release_conditions": {
            "sla_compliant": True,
            "minimum_evaluation_period_hours": 168,
        },
        "timeout_hours": 336,
        "timeout_action": "return_to_payer",
    }
})
escrow = resp.json()
escrow_id = escrow.get("escrow_id")
print(f"Performance escrow created: {escrow_id}")
print(f"Linked to SLA: {sla_id}")
print(f"Timeout: 336 hours -> return to payer")
```

### Automatic Release Gates

Release gates are checkpoints that must all pass before escrow funds are released. Implementing them as a polling loop allows fully autonomous release without human intervention.

```python
import requests
import time

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"
base_url = "https://api.greenhelix.net/v1"


def check_release_gates(escrow_id: str, sla_id: str) -> dict:
    """Check all release gates for a performance escrow."""
    # Gate 1: SLA compliance
    resp = session.post(f"{base_url}/v1", json={
        "tool": "check_sla_compliance",
        "input": {
            "agent_id": "buyer-agent-001",
            "sla_id": sla_id,
        }
    })
    sla_status = resp.json()

    # Gate 2: Escrow status (not disputed, not timed out)
    resp = session.post(f"{base_url}/v1", json={
        "tool": "check_performance_escrow",
        "input": {
            "escrow_id": escrow_id,
        }
    })
    escrow_status = resp.json()

    # Gate 3: No active disputes against this escrow
    resp = session.post(f"{base_url}/v1", json={
        "tool": "list_disputes",
        "input": {
            "agent_id": "buyer-agent-001",
        }
    })
    disputes = resp.json()
    active_disputes = [
        d for d in disputes.get("disputes", [])
        if d.get("escrow_id") == escrow_id
        and d.get("status") in ("open", "under_review")
    ]

    gates = {
        "sla_compliant": sla_status.get("compliant", False),
        "escrow_active": escrow_status.get("status") == "active",
        "no_active_disputes": len(active_disputes) == 0,
    }
    all_passed = all(gates.values())

    return {
        "escrow_id": escrow_id,
        "gates": gates,
        "all_passed": all_passed,
        "action": "release" if all_passed else "hold",
    }


def release_gate_loop(escrow_id: str, sla_id: str,
                      check_interval_seconds: int = 3600,
                      max_checks: int = 168):
    """Poll release gates and release escrow when all gates pass."""
    for i in range(max_checks):
        result = check_release_gates(escrow_id, sla_id)
        print(f"Check {i+1}/{max_checks}: {result['gates']}")

        if result["all_passed"]:
            # All gates passed -- release the escrow
            resp = session.post(f"{base_url}/v1", json={
                "tool": "release_escrow",
                "input": {"escrow_id": escrow_id}
            })
            release = resp.json()
            print(f"Escrow released: {release}")
            return {"status": "released", "check_number": i + 1}

        time.sleep(check_interval_seconds)

    # Max checks reached without release -- trigger dispute
    print("Release gates never passed. Initiating dispute.")
    return {"status": "timeout", "action": "initiate_dispute"}
```

### Dispute-Triggering Conditions

Not every failed gate should trigger a dispute. A temporary SLA dip during a maintenance window is different from persistent non-delivery. The following logic distinguishes between transient failures and dispute-worthy violations.

```python
import requests

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"
base_url = "https://api.greenhelix.net/v1"


def evaluate_dispute_trigger(escrow_id: str, sla_id: str,
                              consecutive_failures: int,
                              failure_threshold: int = 3) -> dict:
    """Determine if SLA failures warrant opening a dispute.

    Only triggers a dispute after consecutive_failures exceeds the
    threshold, filtering out transient violations.
    """
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_sla_status",
        "input": {
            "agent_id": "buyer-agent-001",
            "sla_id": sla_id,
        }
    })
    sla_status = resp.json()

    if not sla_status.get("compliant", True):
        consecutive_failures += 1
    else:
        consecutive_failures = 0

    should_dispute = consecutive_failures >= failure_threshold
    action = "none"

    if should_dispute:
        # Open a dispute against the escrow
        resp = session.post(f"{base_url}/v1", json={
            "tool": "open_dispute",
            "input": {
                "agent_id": "buyer-agent-001",
                "escrow_id": escrow_id,
                "reason": "sla_breach",
                "evidence": {
                    "sla_id": sla_id,
                    "consecutive_failures": consecutive_failures,
                    "threshold": failure_threshold,
                    "latest_status": sla_status,
                },
            }
        })
        dispute = resp.json()
        action = "dispute_opened"
        print(f"Dispute opened: {dispute.get('dispute_id')}")

    return {
        "consecutive_failures": consecutive_failures,
        "should_dispute": should_dispute,
        "action": action,
    }
```

### The Refund Flow

When a dispute is resolved in the buyer's favor, the escrow funds must be returned. The cancellation flow handles this.

```python
import requests

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"
base_url = "https://api.greenhelix.net/v1"

# After dispute resolves in buyer's favor, cancel the escrow
resp = session.post(f"{base_url}/v1", json={
    "tool": "cancel_escrow",
    "input": {
        "escrow_id": "escrow-abc-123",
        "reason": "dispute_resolved_buyer_favor",
        "dispute_id": "dispute-xyz-789",
    }
})
cancellation = resp.json()
print(f"Escrow cancelled: {cancellation}")
print(f"Funds returned to payer")
```

---

## Chapter 5: Automated Evidence Collection & Submission: From Raw Logs to Compelling Evidence 3.0

### Why Manual Evidence Fails at Machine Speed

A human merchant responding to a chargeback has 20 to 45 days to assemble evidence. They gather invoices, shipping receipts, delivery confirmations, and correspondence. The evidence is compiled manually and submitted through the card network's portal. This process assumes (1) the merchant has time, (2) the evidence exists in human-readable form, and (3) a human reviewer will evaluate it.

Agent commerce breaks all three assumptions. Disputes can escalate in minutes, not weeks. Evidence exists as API logs, SLA metrics, and cryptographic hashes, not invoices and receipts. And the initial review may be automated -- Visa's Compelling Evidence 3.0 program, updated April 1, 2026, now includes evidence-sharing tooling designed for programmatic submission, including a new category for agentic transactions.

Your dispute resolution system must collect, package, and submit evidence automatically, in the format that card networks and A2A dispute resolvers expect.

### The Evidence Pipeline

Evidence collection for agent disputes follows a four-stage pipeline.

**Stage 1: Transaction History Extraction.** Pull the complete transaction record for the disputed transaction, including all related transactions in the same session or delegation chain.

**Stage 2: SLA Compliance Snapshots.** If the dispute involves service quality, pull the full SLA compliance history for the evaluation period. Point-in-time snapshots are more compelling than summary statistics because they show the pattern of violations.

**Stage 3: Reputation Attestations.** Pull the counterparty's reputation profile, including claim chains, verified metrics, and dispute history. A counterparty with a pattern of disputes is weaker in arbitration than one with a clean record.

**Stage 4: Structured Evidence Packaging.** Combine all evidence into a structured package with cryptographic integrity verification. The package must be self-contained and verifiable by a third party.

```python
import requests
import hashlib
import json
import time
from typing import Dict, List, Any


class EvidenceCollector:
    """Automated evidence collection for agent dispute defense.

    Collects transaction history, SLA compliance data, reputation
    attestations, and packages them into structured evidence bundles
    compatible with Visa CE 3.0 and A2A dispute resolution.
    """

    def __init__(self, api_key: str, agent_id: str,
                 base_url: str = "https://api.greenhelix.net/v1"):
        self.agent_id = agent_id
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })

    def _execute(self, tool: str, input_data: dict) -> dict:
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    def collect_transaction_evidence(self, counterparty_id: str) -> dict:
        """Stage 1: Extract transaction history with counterparty."""
        history = self._execute("get_transaction_history", {
            "agent_id": self.agent_id,
        })

        relevant = [
            t for t in history.get("transactions", [])
            if t.get("counterparty") == counterparty_id
        ]

        return {
            "stage": "transaction_history",
            "total_transactions": len(relevant),
            "transactions": relevant,
            "collected_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

    def collect_sla_evidence(self, sla_id: str) -> dict:
        """Stage 2: Collect SLA compliance snapshots."""
        compliance = self._execute("check_sla_compliance", {
            "agent_id": self.agent_id,
            "sla_id": sla_id,
        })
        status = self._execute("get_sla_status", {
            "agent_id": self.agent_id,
            "sla_id": sla_id,
        })

        return {
            "stage": "sla_compliance",
            "sla_id": sla_id,
            "compliant": compliance.get("compliant"),
            "violations": compliance.get("violations", []),
            "full_status": status,
            "collected_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

    def collect_reputation_evidence(self, counterparty_id: str) -> dict:
        """Stage 3: Collect counterparty reputation attestations."""
        reputation = self._execute("get_agent_reputation", {
            "agent_id": counterparty_id,
        })
        identity = self._execute("verify_identity", {
            "agent_id": counterparty_id,
        })

        return {
            "stage": "reputation_attestation",
            "counterparty_id": counterparty_id,
            "reputation_score": reputation.get("reputation_score"),
            "dispute_history": reputation.get("dispute_history", {}),
            "identity_verified": identity.get("verified", False),
            "registration_date": identity.get("registered_at"),
            "collected_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

    def collect_escrow_evidence(self, escrow_id: str) -> dict:
        """Collect escrow state and performance data."""
        escrow = self._execute("check_performance_escrow", {
            "escrow_id": escrow_id,
        })
        return {
            "stage": "escrow_state",
            "escrow_id": escrow_id,
            "escrow_data": escrow,
            "collected_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        }

    def package_evidence(self, escrow_id: str, sla_id: str,
                         counterparty_id: str,
                         intent_hash: str = None) -> dict:
        """Stage 4: Package all evidence into a structured bundle.

        The bundle includes a SHA-256 integrity hash over all evidence
        so that any tampering is detectable.
        """
        evidence_stages = [
            self.collect_transaction_evidence(counterparty_id),
            self.collect_sla_evidence(sla_id),
            self.collect_reputation_evidence(counterparty_id),
            self.collect_escrow_evidence(escrow_id),
        ]

        bundle = {
            "dispute_evidence_bundle": {
                "version": "1.0",
                "format": "greenhelix_ce3_compatible",
                "agent_id": self.agent_id,
                "counterparty_id": counterparty_id,
                "escrow_id": escrow_id,
                "sla_id": sla_id,
                "intent_hash": intent_hash,
                "stages": evidence_stages,
                "packaged_at": time.strftime(
                    "%Y-%m-%dT%H:%M:%SZ", time.gmtime()
                ),
            }
        }

        # Compute integrity hash over the entire bundle
        bundle_bytes = json.dumps(
            bundle, sort_keys=True, default=str
        ).encode("utf-8")
        bundle["dispute_evidence_bundle"]["integrity_hash"] = hashlib.sha256(
            bundle_bytes
        ).hexdigest()

        return bundle
```

### Submitting Evidence to a Dispute

Once the evidence bundle is assembled, it is attached to the dispute response. The evidence is submitted programmatically as part of the `respond_dispute` tool call.

```python
import requests
import json

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"
base_url = "https://api.greenhelix.net/v1"

# Assume evidence_bundle was created by EvidenceCollector.package_evidence()
evidence_bundle = collector.package_evidence(
    escrow_id="escrow-abc-123",
    sla_id="sla-compute-2026-04",
    counterparty_id="vendor-agent-001",
    intent_hash="a1b2c3d4e5f6...",
)

# Submit evidence as part of dispute response
resp = session.post(f"{base_url}/v1", json={
    "tool": "respond_dispute",
    "input": {
        "dispute_id": "dispute-xyz-789",
        "agent_id": "buyer-agent-001",
        "response": "reject",
        "evidence": evidence_bundle["dispute_evidence_bundle"],
        "narrative": (
            "SLA compliance data shows 3 consecutive violations of the "
            "uptime threshold (99.5% required, 94.2% actual over 72 hours). "
            "Performance escrow release conditions were never met. "
            "Intent chain proves transaction was within mandate scope. "
            "Requesting full refund via escrow cancellation."
        ),
    }
})
response = resp.json()
print(f"Dispute response submitted: {response}")
```

---

## Chapter 6: Multi-Party Dispute Resolution Workflows: Filing, Responding, Escalating, and Arbitrating

### The Dispute Lifecycle

GreenHelix disputes follow a four-stage lifecycle: Open, Response, Resolution, and Closed. Each stage has timeouts. If a party does not act within the timeout, the system advances automatically -- typically in favor of the party that did act.

```
OPEN ──(72h)──> RESPONSE ──(72h)──> RESOLUTION ──(24h)──> CLOSED
  │                │                     │                    │
  │                │                     │                    │
  └─ Initiator     └─ Respondent         └─ Arbitrator/       └─ Final
     files claim      provides evidence     Auto-resolve         state
```

### Stage 1: Filing a Dispute

The initiator opens a dispute by identifying the escrow, the failure mode (from the Chapter 2 taxonomy), and initial evidence. The evidence does not need to be comprehensive at filing -- it needs to be sufficient to establish the claim.

```python
import requests

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"
base_url = "https://api.greenhelix.net/v1"

# File a dispute for SLA breach
resp = session.post(f"{base_url}/v1", json={
    "tool": "open_dispute",
    "input": {
        "agent_id": "buyer-agent-001",
        "escrow_id": "escrow-abc-123",
        "reason": "sla_breach",
        "failure_mode": "sla_breach",  # From the 7-mode taxonomy
        "evidence": {
            "sla_id": "sla-compute-2026-04",
            "violations_summary": "3 consecutive failures: uptime below 99.5%",
            "requested_resolution": "full_refund",
        },
        "deadline_hours": 72,
    }
})
dispute = resp.json()
dispute_id = dispute.get("dispute_id")
print(f"Dispute filed: {dispute_id}")
print(f"Respondent has 72 hours to respond")
```

### Stage 2: Responding to a Dispute

The respondent must provide counter-evidence within the response window. The `EvidenceCollector` from Chapter 5 automates this. A strong response includes transaction evidence, SLA data, and reputation attestation.

```python
import requests

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"
base_url = "https://api.greenhelix.net/v1"

# As the vendor, respond to the dispute with evidence
resp = session.post(f"{base_url}/v1", json={
    "tool": "respond_dispute",
    "input": {
        "dispute_id": "dispute-xyz-789",
        "agent_id": "vendor-agent-001",
        "response": "contest",
        "evidence": {
            "sla_compliance_report": {
                "overall_uptime": 99.7,
                "note": "Brief dip during scheduled maintenance window, "
                        "communicated 48h in advance per SLA section 4.2",
            },
            "maintenance_notification": {
                "sent_at": "2026-04-04T08:00:00Z",
                "channel": "messaging",
                "message_id": "msg-maint-001",
            },
            "monitor_logs": {
                "sla_id": "sla-compute-2026-04",
                "measurement_source": "greenhelix_sla_monitor",
            },
        },
        "narrative": (
            "Uptime dip occurred during a pre-announced maintenance window. "
            "SLA section 4.2 excludes scheduled maintenance from uptime "
            "calculations. Excluding the 4-hour window, uptime was 99.82%."
        ),
    }
})
response = resp.json()
print(f"Dispute response filed: {response}")
```

### Stage 3: Resolution

Resolution can happen in three ways: mutual agreement, timeout-based automatic resolution, or third-party arbitration. The `resolve_dispute` tool handles all three.

```python
import requests

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"
base_url = "https://api.greenhelix.net/v1"

# Resolution option 1: Mutual agreement (either party can propose)
resp = session.post(f"{base_url}/v1", json={
    "tool": "resolve_dispute",
    "input": {
        "dispute_id": "dispute-xyz-789",
        "resolution": "partial_refund",
        "details": {
            "refund_amount_cents": 5000,
            "refund_reason": "Partial SLA credit for maintenance-window impact",
            "escrow_action": "partial_release",
            "release_to_vendor_cents": 5000,
            "return_to_buyer_cents": 5000,
        },
    }
})
resolution = resp.json()
print(f"Resolution proposed: {resolution}")
```

### Automated Dispute Handler

The following class orchestrates the entire dispute lifecycle autonomously. It monitors for incoming disputes, collects evidence, submits responses, and handles resolution -- all without human intervention.

```python
import requests
import time
import json
from typing import Dict, Optional, Callable, Any


class AutomatedDisputeHandler:
    """Fully autonomous dispute lifecycle management.

    Monitors for new disputes, auto-collects evidence, submits
    responses within deadlines, and handles resolution flows.
    """

    def __init__(self, api_key: str, agent_id: str,
                 evidence_collector,
                 base_url: str = "https://api.greenhelix.net/v1"):
        self.agent_id = agent_id
        self.base_url = base_url
        self.evidence_collector = evidence_collector
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })
        self.handled_disputes: Dict[str, str] = {}  # dispute_id -> status
        self.escalation_callback: Optional[Callable] = None

    def _execute(self, tool: str, input_data: dict) -> dict:
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    def set_escalation_callback(self, callback: Callable):
        """Register a callback for disputes that require human review."""
        self.escalation_callback = callback

    def poll_disputes(self) -> list:
        """Check for new or updated disputes."""
        result = self._execute("list_disputes", {
            "agent_id": self.agent_id,
        })
        return result.get("disputes", [])

    def handle_incoming_dispute(self, dispute: dict) -> dict:
        """Process a single incoming dispute."""
        dispute_id = dispute.get("dispute_id")
        status = dispute.get("status")
        escrow_id = dispute.get("escrow_id")

        if dispute_id in self.handled_disputes:
            if self.handled_disputes[dispute_id] == status:
                return {"action": "already_handled"}

        # Collect evidence automatically
        evidence_bundle = self.evidence_collector.package_evidence(
            escrow_id=escrow_id,
            sla_id=dispute.get("sla_id", ""),
            counterparty_id=dispute.get("initiator_id", ""),
        )

        # Determine response strategy based on evidence
        sla_evidence = next(
            (s for s in evidence_bundle["dispute_evidence_bundle"]["stages"]
             if s["stage"] == "sla_compliance"),
            {}
        )
        is_compliant = sla_evidence.get("compliant", True)

        if is_compliant:
            # Evidence supports our position -- contest the dispute
            response = self._execute("respond_dispute", {
                "dispute_id": dispute_id,
                "agent_id": self.agent_id,
                "response": "contest",
                "evidence": evidence_bundle["dispute_evidence_bundle"],
                "narrative": "SLA compliance verified. Contesting dispute.",
            })
            self.handled_disputes[dispute_id] = "contested"
            return {"action": "contested", "response": response}
        else:
            # Evidence does not support us -- escalate or concede
            if self.escalation_callback:
                self.escalation_callback(dispute, evidence_bundle)
                self.handled_disputes[dispute_id] = "escalated"
                return {"action": "escalated_to_human"}
            else:
                # No escalation path -- propose partial resolution
                response = self._execute("respond_dispute", {
                    "dispute_id": dispute_id,
                    "agent_id": self.agent_id,
                    "response": "accept_partial",
                    "evidence": evidence_bundle["dispute_evidence_bundle"],
                    "narrative": (
                        "SLA violations confirmed. Proposing partial "
                        "credit proportional to violation severity."
                    ),
                })
                self.handled_disputes[dispute_id] = "partial_accepted"
                return {"action": "partial_accepted", "response": response}

    def run_dispute_monitor(self, interval_seconds: int = 300,
                            max_iterations: int = 0):
        """Continuously monitor and handle disputes.

        Args:
            interval_seconds: Polling interval.
            max_iterations: Stop after N iterations (0 = run forever).
        """
        iteration = 0
        while max_iterations == 0 or iteration < max_iterations:
            disputes = self.poll_disputes()
            open_disputes = [
                d for d in disputes
                if d.get("status") in ("open", "awaiting_response")
                and d.get("respondent_id") == self.agent_id
            ]

            for dispute in open_disputes:
                result = self.handle_incoming_dispute(dispute)
                print(
                    f"Dispute {dispute.get('dispute_id')}: "
                    f"{result.get('action')}"
                )

            iteration += 1
            if max_iterations == 0 or iteration < max_iterations:
                time.sleep(interval_seconds)
```

### Timeout Handlers

Disputes that are not responded to within the deadline resolve automatically. As the initiator, this works in your favor. As the respondent, timeouts are catastrophic. The following pattern ensures your agent never misses a deadline.

```python
import requests
import time

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"
base_url = "https://api.greenhelix.net/v1"


def check_response_deadlines(agent_id: str,
                              warning_hours: int = 12) -> list:
    """Identify disputes approaching response deadlines."""
    resp = session.post(f"{base_url}/v1", json={
        "tool": "list_disputes",
        "input": {"agent_id": agent_id}
    })
    disputes = resp.json().get("disputes", [])

    urgent = []
    now = time.time()
    for d in disputes:
        if d.get("status") == "awaiting_response" and d.get("respondent_id") == agent_id:
            deadline = d.get("response_deadline_epoch", 0)
            hours_remaining = (deadline - now) / 3600
            if 0 < hours_remaining <= warning_hours:
                urgent.append({
                    "dispute_id": d.get("dispute_id"),
                    "hours_remaining": round(hours_remaining, 1),
                    "escrow_id": d.get("escrow_id"),
                    "priority": "critical" if hours_remaining <= 4 else "high",
                })

    return sorted(urgent, key=lambda x: x["hours_remaining"])
```

---

## Chapter 7: Chargeback Defense for Agent-Initiated Transactions: Card Network Rules Meet A2A Commerce

### The Fundamental Mismatch

Card network dispute rules assume a cardholder initiated the transaction. The cardholder can file a chargeback by claiming fraud (they did not make the purchase) or by claiming the goods were not as described. The issuing bank evaluates the claim, the acquiring bank represents the merchant, and the card network arbitrates if the parties cannot agree.

When an AI agent initiates a transaction funded by a card deposit, the cardholder is the human principal who funded the agent's wallet. The merchant is the counterparty agent (or more precisely, the human operator behind the counterparty agent). The cardholder might file a chargeback because their agent over-purchased (Failure Mode 1), because the agent bought something the cardholder did not want (Failure Mode 7: intent drift), or because the counterparty did not deliver (Failure Mode 4: SLA breach). The card network must evaluate this claim using rules designed for "I ordered a shirt and it never arrived," not "my autonomous procurement agent exceeded its compute budget by $8,000 because it hallucinated a scaling requirement."

### Visa Compelling Evidence 3.0: Agentic Extensions

Visa's CE 3.0 update, effective April 1, 2026, is the first card network evidence standard to explicitly address agentic transactions. The update introduces two relevant changes.

First, it adds a new evidence category for "delegated purchasing authority" -- documentation proving that a human principal authorized an agent to make purchases on their behalf. This maps directly to the mandate and intent chain from Chapter 3.

Second, it introduces evidence-sharing tooling that allows merchants to submit evidence programmatically rather than through the traditional portal upload. This is critical for agent commerce because the evidence (API logs, SLA metrics, cryptographic hashes) is inherently digital and structured.

### Mastercard Scheme-Carried Liability

Mastercard's approach is different. Rather than modifying the evidence framework, they are establishing scheme-carried liability for transactions that follow the Verifiable Intent specification. If both the buyer and seller use Verifiable Intent (the mandate -> intent -> transaction chain), and the transaction is properly recorded, Mastercard absorbs the chargeback liability rather than pushing it to either party. This creates a strong incentive for both sides to implement Verifiable Intent chains, because doing so eliminates chargeback risk entirely.

### Building an Intent Store for Pre-Dispute Deflection

The most effective chargeback defense is preventing the chargeback from being filed. An intent store is a queryable database of all agent intents, mandates, and transaction linkages. When a cardholder contacts their bank to dispute a transaction, the merchant's system can pre-emptively submit the intent chain to the issuer before the chargeback is formalized. This is called pre-dispute deflection, and Visa's CE 3.0 now supports it for agentic transactions.

```python
import requests
import hashlib
import json
import time
from typing import Dict, List, Optional, Any


class IntentStore:
    """Queryable store of agent intents for chargeback deflection.

    Maintains a local index of all mandates, intents, and transaction
    linkages. Supports pre-dispute evidence retrieval for card network
    submission within the CE 3.0 framework.
    """

    def __init__(self, api_key: str, agent_id: str,
                 base_url: str = "https://api.greenhelix.net/v1"):
        self.agent_id = agent_id
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })
        self.mandates: Dict[str, dict] = {}  # mandate_hash -> mandate
        self.intents: Dict[str, dict] = {}   # intent_hash -> intent
        self.tx_to_intent: Dict[str, str] = {}  # transaction_id -> intent_hash

    def _execute(self, tool: str, input_data: dict) -> dict:
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    @staticmethod
    def _hash(data: dict) -> str:
        return hashlib.sha256(
            json.dumps(data, sort_keys=True).encode("utf-8")
        ).hexdigest()

    def store_mandate(self, mandate: dict) -> str:
        """Store a mandate and return its hash."""
        h = self._hash(mandate)
        self.mandates[h] = mandate
        return h

    def store_intent(self, intent: dict, transaction_id: str = None) -> str:
        """Store an intent and optionally link it to a transaction."""
        h = self._hash(intent)
        self.intents[h] = intent
        if transaction_id:
            self.tx_to_intent[transaction_id] = h
        return h

    def lookup_by_transaction(self, transaction_id: str) -> Optional[dict]:
        """Retrieve the full intent chain for a transaction.

        Returns the intent, its parent mandate, and the chain
        verification data needed for CE 3.0 evidence submission.
        """
        intent_hash = self.tx_to_intent.get(transaction_id)
        if not intent_hash:
            return None

        intent = self.intents.get(intent_hash)
        if not intent:
            return None

        mandate_hash = intent.get("mandate_hash")
        mandate = self.mandates.get(mandate_hash)

        return {
            "transaction_id": transaction_id,
            "intent_hash": intent_hash,
            "intent": intent,
            "mandate_hash": mandate_hash,
            "mandate": mandate,
            "chain_complete": mandate is not None,
        }

    def generate_ce3_evidence(self, transaction_id: str) -> Optional[dict]:
        """Generate Visa CE 3.0 compatible evidence for a transaction.

        This evidence package can be submitted to the issuer for
        pre-dispute deflection or chargeback defense.
        """
        chain = self.lookup_by_transaction(transaction_id)
        if not chain:
            return None

        # Pull additional context from GreenHelix
        history = self._execute("get_transaction_history", {
            "agent_id": self.agent_id,
        })

        # Find the specific transaction
        tx_record = next(
            (t for t in history.get("transactions", [])
             if t.get("transaction_id") == transaction_id),
            {}
        )

        evidence = {
            "ce3_version": "3.0",
            "evidence_type": "delegated_purchasing_authority",
            "transaction_id": transaction_id,
            "transaction_record": tx_record,
            "delegated_authority": {
                "mandate_hash": chain["mandate_hash"],
                "mandate_principal": chain["mandate"].get("principal"),
                "mandate_valid_from": chain["mandate"].get("valid_from"),
                "mandate_valid_until": chain["mandate"].get("valid_until"),
                "authorized_actions": chain["mandate"].get("authorized_actions"),
                "budget_ceiling_cents": chain["mandate"].get(
                    "budget_ceiling_cents"
                ),
            },
            "intent_chain": {
                "intent_hash": chain["intent_hash"],
                "action": chain["intent"].get("action"),
                "amount_cents": chain["intent"].get("amount_cents"),
                "vendor": chain["intent"].get("vendor"),
                "justification": chain["intent"].get("justification"),
                "mandate_clause": chain["intent"].get("mandate_clause"),
                "timestamp": chain["intent"].get("timestamp"),
            },
            "verification": {
                "mandate_hash_algorithm": "sha256_json_sorted_keys",
                "intent_hash_algorithm": "sha256_json_sorted_keys",
                "chain_recorded_on": "greenhelix_claim_chain",
            },
            "generated_at": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime()
            ),
        }

        # Compute evidence integrity hash
        evidence_bytes = json.dumps(
            evidence, sort_keys=True
        ).encode("utf-8")
        evidence["evidence_integrity_hash"] = hashlib.sha256(
            evidence_bytes
        ).hexdigest()

        return evidence

    def generate_mastercard_vi_package(self,
                                        transaction_id: str) -> Optional[dict]:
        """Generate Mastercard Verifiable Intent package.

        If the transaction has a complete intent chain, the package
        qualifies for scheme-carried liability, eliminating chargeback
        risk for both parties.
        """
        chain = self.lookup_by_transaction(transaction_id)
        if not chain or not chain["chain_complete"]:
            return None

        return {
            "vi_version": "1.0",
            "scheme": "mastercard",
            "liability_type": "scheme_carried",
            "transaction_id": transaction_id,
            "mandate": {
                "hash": chain["mandate_hash"],
                "principal": chain["mandate"].get("principal"),
                "scope": chain["mandate"].get("authorized_actions"),
                "budget_cents": chain["mandate"].get("budget_ceiling_cents"),
                "validity": {
                    "from": chain["mandate"].get("valid_from"),
                    "until": chain["mandate"].get("valid_until"),
                },
            },
            "intent": {
                "hash": chain["intent_hash"],
                "action": chain["intent"].get("action"),
                "amount_cents": chain["intent"].get("amount_cents"),
                "vendor": chain["intent"].get("vendor"),
                "clause_reference": chain["intent"].get("mandate_clause"),
            },
            "chain_integrity": {
                "recorded_on": "greenhelix_claim_chain",
                "agent_id": self.agent_id,
                "verifiable": True,
            },
            "generated_at": time.strftime(
                "%Y-%m-%dT%H:%M:%SZ", time.gmtime()
            ),
        }
```

### Pre-Dispute Deflection Workflow

The deflection workflow intercepts potential chargebacks before they formalize. When a cardholder inquiry is detected (via the card network's early warning system), the intent store generates and submits the evidence automatically.

```python
import requests

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"
base_url = "https://api.greenhelix.net/v1"

# When an early warning alert arrives for a transaction
transaction_id = "tx-2026-04-06-001"

# Look up the intent chain
intent_store = IntentStore(api_key, "buyer-agent-001")
# (Assume mandates and intents were stored during transaction execution)

ce3_evidence = intent_store.generate_ce3_evidence(transaction_id)
if ce3_evidence:
    print("CE 3.0 evidence generated for pre-dispute deflection:")
    print(f"  Evidence type: {ce3_evidence['evidence_type']}")
    print(f"  Mandate principal: {ce3_evidence['delegated_authority']['mandate_principal']}")
    print(f"  Intent action: {ce3_evidence['intent_chain']['action']}")
    print(f"  Amount: ${ce3_evidence['intent_chain']['amount_cents'] / 100:.2f}")
    # Submit to card network early warning system via their API
    # (Network-specific integration not shown)

vi_package = intent_store.generate_mastercard_vi_package(transaction_id)
if vi_package:
    print(f"\nMastercard VI package: liability={vi_package['liability_type']}")
    # If VI package is complete, chargeback liability is scheme-carried
```

---

## Chapter 8: Production Dispute Resolution System: End-to-End Implementation with Monitoring

### Putting It All Together

The previous chapters covered individual components: intent chains, escrow pipelines, evidence collection, dispute workflows, and chargeback defense. This chapter combines them into a single production system with monitoring, automated escalation, and post-mortem forensics.

### The DisputeResolutionSystem Class

```python
import requests
import hashlib
import json
import time
import logging
from typing import Dict, List, Optional, Callable, Any
from datetime import datetime, timezone


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dispute_resolution")


class DisputeResolutionSystem:
    """Production dispute resolution system with monitoring and automation.

    Integrates: VerifiableIntentChain, EvidenceCollector,
    AutomatedDisputeHandler, IntentStore, and SLA monitoring
    into a single operational system.
    """

    def __init__(self, api_key: str, agent_id: str,
                 base_url: str = "https://api.greenhelix.net/v1"):
        self.agent_id = agent_id
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })
        # Internal state
        self.active_escrows: Dict[str, dict] = {}
        self.active_slas: Dict[str, dict] = {}
        self.dispute_log: List[dict] = []
        self.metrics: Dict[str, Any] = {
            "disputes_filed": 0,
            "disputes_received": 0,
            "disputes_won": 0,
            "disputes_lost": 0,
            "chargebacks_deflected": 0,
            "total_amount_disputed_cents": 0,
            "total_amount_recovered_cents": 0,
        }
        # Callbacks
        self.escalation_callback: Optional[Callable] = None
        self.alert_callback: Optional[Callable] = None

    def _execute(self, tool: str, input_data: dict) -> dict:
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    # ── Escrow Management ───────────────────────────────────────────

    def create_protected_escrow(self, vendor_id: str, amount_cents: int,
                                 sla_config: dict,
                                 intent_hash: str) -> dict:
        """Create a dispute-ready escrow with SLA protection.

        Links escrow to an SLA and records the intent hash for
        chargeback defense.
        """
        # Create SLA
        sla = self._execute("create_sla", {
            "agent_id": self.agent_id,
            "provider_id": vendor_id,
            "metrics": sla_config.get("metrics", {}),
            "evaluation_period": sla_config.get("evaluation_period"),
        })
        sla_id = sla.get("sla_id")

        # Create performance escrow
        escrow = self._execute("create_performance_escrow", {
            "payer_id": self.agent_id,
            "payee_id": vendor_id,
            "amount": amount_cents,
            "sla_id": sla_id,
            "release_conditions": {
                "sla_compliant": True,
                "minimum_evaluation_period_hours":
                    sla_config.get("min_eval_hours", 168),
            },
            "timeout_hours": sla_config.get("timeout_hours", 336),
            "timeout_action": "return_to_payer",
        })
        escrow_id = escrow.get("escrow_id")

        # Track internally
        self.active_escrows[escrow_id] = {
            "vendor_id": vendor_id,
            "amount_cents": amount_cents,
            "sla_id": sla_id,
            "intent_hash": intent_hash,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "status": "active",
        }
        self.active_slas[sla_id] = {
            "escrow_id": escrow_id,
            "vendor_id": vendor_id,
            "consecutive_failures": 0,
        }

        logger.info(
            f"Protected escrow created: {escrow_id} "
            f"(SLA: {sla_id}, amount: {amount_cents})"
        )
        return {
            "escrow_id": escrow_id,
            "sla_id": sla_id,
            "intent_hash": intent_hash,
        }

    # ── SLA Monitoring ──────────────────────────────────────────────

    def monitor_sla_compliance(self, sla_id: str,
                                failure_threshold: int = 3) -> dict:
        """Check SLA compliance and trigger dispute if threshold breached."""
        sla_info = self.active_slas.get(sla_id, {})
        escrow_id = sla_info.get("escrow_id")

        compliance = self._execute("check_sla_compliance", {
            "agent_id": self.agent_id,
            "sla_id": sla_id,
        })

        if not compliance.get("compliant", True):
            sla_info["consecutive_failures"] = (
                sla_info.get("consecutive_failures", 0) + 1
            )
            logger.warning(
                f"SLA {sla_id} non-compliant "
                f"(failure {sla_info['consecutive_failures']}"
                f"/{failure_threshold})"
            )
        else:
            sla_info["consecutive_failures"] = 0

        if sla_info.get("consecutive_failures", 0) >= failure_threshold:
            return self._auto_file_dispute(
                escrow_id, sla_id, compliance
            )

        return {
            "sla_id": sla_id,
            "compliant": compliance.get("compliant"),
            "consecutive_failures": sla_info.get("consecutive_failures", 0),
            "action": "monitoring",
        }

    def _auto_file_dispute(self, escrow_id: str, sla_id: str,
                            compliance: dict) -> dict:
        """Automatically file a dispute when SLA threshold is breached."""
        escrow_info = self.active_escrows.get(escrow_id, {})

        dispute = self._execute("open_dispute", {
            "agent_id": self.agent_id,
            "escrow_id": escrow_id,
            "reason": "sla_breach",
            "failure_mode": "sla_breach",
            "evidence": {
                "sla_id": sla_id,
                "compliance_data": compliance,
                "escrow_amount_cents": escrow_info.get("amount_cents"),
            },
        })

        self.metrics["disputes_filed"] += 1
        self.metrics["total_amount_disputed_cents"] += escrow_info.get(
            "amount_cents", 0
        )

        self.dispute_log.append({
            "dispute_id": dispute.get("dispute_id"),
            "escrow_id": escrow_id,
            "sla_id": sla_id,
            "type": "auto_filed",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        logger.info(
            f"Auto-filed dispute {dispute.get('dispute_id')} "
            f"for escrow {escrow_id}"
        )

        if self.alert_callback:
            self.alert_callback({
                "type": "dispute_auto_filed",
                "dispute_id": dispute.get("dispute_id"),
                "escrow_id": escrow_id,
                "amount_cents": escrow_info.get("amount_cents"),
            })

        return {
            "action": "dispute_filed",
            "dispute_id": dispute.get("dispute_id"),
        }

    # ── Dispute Response ────────────────────────────────────────────

    def handle_incoming_disputes(self) -> List[dict]:
        """Check for and respond to incoming disputes."""
        disputes = self._execute("list_disputes", {
            "agent_id": self.agent_id,
        })

        results = []
        for d in disputes.get("disputes", []):
            if (d.get("status") == "awaiting_response"
                    and d.get("respondent_id") == self.agent_id):
                result = self._respond_to_dispute(d)
                results.append(result)

        return results

    def _respond_to_dispute(self, dispute: dict) -> dict:
        """Generate and submit a response to an incoming dispute."""
        dispute_id = dispute.get("dispute_id")
        escrow_id = dispute.get("escrow_id")
        sla_id = dispute.get("sla_id", "")

        self.metrics["disputes_received"] += 1

        # Collect evidence
        evidence_stages = []

        # Transaction history
        history = self._execute("get_transaction_history", {
            "agent_id": self.agent_id,
        })
        evidence_stages.append({
            "stage": "transaction_history",
            "data": history,
        })

        # SLA compliance (if applicable)
        if sla_id:
            compliance = self._execute("check_sla_compliance", {
                "agent_id": self.agent_id,
                "sla_id": sla_id,
            })
            evidence_stages.append({
                "stage": "sla_compliance",
                "data": compliance,
            })

        # Counterparty reputation
        initiator_id = dispute.get("initiator_id", "")
        if initiator_id:
            rep = self._execute("get_agent_reputation", {
                "agent_id": initiator_id,
            })
            evidence_stages.append({
                "stage": "counterparty_reputation",
                "data": rep,
            })

        # Determine response
        is_compliant = True
        for stage in evidence_stages:
            if stage["stage"] == "sla_compliance":
                is_compliant = stage["data"].get("compliant", True)

        if is_compliant:
            response_type = "contest"
            narrative = (
                "SLA compliance verified across all metrics. "
                "Evidence attached demonstrates full delivery."
            )
        else:
            response_type = "accept_partial"
            narrative = (
                "Partial SLA deviation acknowledged. Proposing "
                "proportional credit based on violation severity."
            )

        response = self._execute("respond_dispute", {
            "dispute_id": dispute_id,
            "agent_id": self.agent_id,
            "response": response_type,
            "evidence": {
                "stages": evidence_stages,
                "collected_at": datetime.now(timezone.utc).isoformat(),
            },
            "narrative": narrative,
        })

        self.dispute_log.append({
            "dispute_id": dispute_id,
            "type": "response_submitted",
            "response_type": response_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        logger.info(
            f"Responded to dispute {dispute_id}: {response_type}"
        )
        return {
            "dispute_id": dispute_id,
            "response_type": response_type,
            "response": response,
        }

    # ── Dashboard & Metrics ─────────────────────────────────────────

    def get_dashboard(self) -> dict:
        """Generate a dispute resolution dashboard snapshot."""
        # Refresh dispute state
        disputes = self._execute("list_disputes", {
            "agent_id": self.agent_id,
        })

        open_disputes = [
            d for d in disputes.get("disputes", [])
            if d.get("status") in ("open", "awaiting_response", "under_review")
        ]
        resolved_disputes = [
            d for d in disputes.get("disputes", [])
            if d.get("status") in ("resolved", "closed")
        ]

        # Calculate win rate
        won = sum(
            1 for d in resolved_disputes
            if d.get("resolution_favor") == self.agent_id
        )
        lost = sum(
            1 for d in resolved_disputes
            if d.get("resolution_favor") and
            d.get("resolution_favor") != self.agent_id
        )
        total_resolved = won + lost
        win_rate = (won / total_resolved * 100) if total_resolved > 0 else 0

        # SLA health
        sla_health = {}
        for sla_id, sla_info in self.active_slas.items():
            status = self._execute("get_sla_status", {
                "agent_id": self.agent_id,
                "sla_id": sla_id,
            })
            sla_health[sla_id] = {
                "compliant": status.get("compliant"),
                "consecutive_failures": sla_info.get(
                    "consecutive_failures", 0
                ),
                "escrow_id": sla_info.get("escrow_id"),
            }

        # Balance check
        balance = self._execute("get_balance", {
            "agent_id": self.agent_id,
        })

        return {
            "agent_id": self.agent_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "disputes": {
                "open": len(open_disputes),
                "resolved": len(resolved_disputes),
                "win_rate_percent": round(win_rate, 1),
                "total_filed": self.metrics["disputes_filed"],
                "total_received": self.metrics["disputes_received"],
            },
            "financials": {
                "balance_cents": balance.get("balance"),
                "amount_in_dispute_cents":
                    self.metrics["total_amount_disputed_cents"],
                "amount_recovered_cents":
                    self.metrics["total_amount_recovered_cents"],
            },
            "escrows": {
                "active": sum(
                    1 for e in self.active_escrows.values()
                    if e["status"] == "active"
                ),
                "total_value_cents": sum(
                    e["amount_cents"] for e in self.active_escrows.values()
                    if e["status"] == "active"
                ),
            },
            "sla_health": sla_health,
            "recent_events": self.dispute_log[-10:],
        }

    # ── Post-Mortem Forensics ───────────────────────────────────────

    def generate_post_mortem(self, dispute_id: str) -> dict:
        """Generate a forensic post-mortem for a resolved dispute.

        Analyzes the full dispute timeline, evidence submissions,
        and outcome to identify systemic issues.
        """
        dispute = self._execute("get_dispute", {
            "dispute_id": dispute_id,
        })

        escrow_id = dispute.get("escrow_id")
        escrow_info = self.active_escrows.get(escrow_id, {})

        # Build timeline from dispute log
        timeline = [
            entry for entry in self.dispute_log
            if entry.get("dispute_id") == dispute_id
        ]

        # Identify the failure mode
        failure_mode = dispute.get("failure_mode", "unknown")

        # Calculate financial impact
        amount_cents = escrow_info.get("amount_cents", 0)
        resolution = dispute.get("resolution", {})
        recovered = resolution.get("return_to_buyer_cents", 0)
        lost = amount_cents - recovered

        # Generate recommendations based on failure mode
        recommendations = self._get_recommendations(failure_mode)

        return {
            "post_mortem": {
                "dispute_id": dispute_id,
                "escrow_id": escrow_id,
                "failure_mode": failure_mode,
                "outcome": dispute.get("status"),
                "resolution_favor": dispute.get("resolution_favor"),
                "financial_impact": {
                    "total_amount_cents": amount_cents,
                    "recovered_cents": recovered,
                    "lost_cents": lost,
                },
                "timeline": timeline,
                "counterparty_id": escrow_info.get("vendor_id"),
                "recommendations": recommendations,
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }
        }

    @staticmethod
    def _get_recommendations(failure_mode: str) -> list:
        """Return preventive recommendations based on failure mode."""
        recs = {
            "over_purchase": [
                "Tighten mandate budget ceiling",
                "Add per-transaction amount limit to mandate",
                "Implement real-time spend tracking with alerts",
            ],
            "hallucinated_order": [
                "Add intent validation against task context",
                "Require human approval for purchases outside known categories",
                "Implement purchase justification scoring",
            ],
            "unauthorized_merchant": [
                "Enforce vendor allowlist at the escrow creation layer",
                "Add vendor identity verification before escrow creation",
                "Monitor for new vendor additions to the agent's patterns",
            ],
            "sla_breach": [
                "Shorten SLA evaluation periods for faster detection",
                "Lower the consecutive-failure threshold for disputes",
                "Add SLA monitoring with real-time alerts",
            ],
            "escrow_timeout": [
                "Set shorter escrow timeout periods",
                "Add intermediate milestones with partial release",
                "Implement timeout warning alerts at 50% and 75% of window",
            ],
            "cascading_delegation": [
                "Enforce budget propagation limits in delegation chains",
                "Cap delegation depth in mandate",
                "Require per-level budget reporting",
            ],
            "intent_drift": [
                "Implement purchase category tracking over time",
                "Add mandate scope alerts for out-of-category purchases",
                "Schedule periodic mandate re-authorization",
            ],
        }
        return recs.get(failure_mode, [
            "Review dispute details and update prevention controls",
            "Consider adding this failure mode to monitoring",
        ])

    # ── Main Loop ───────────────────────────────────────────────────

    def run(self, poll_interval_seconds: int = 300,
            sla_check_interval_seconds: int = 3600,
            max_iterations: int = 0):
        """Run the dispute resolution system.

        Continuously monitors SLAs, handles incoming disputes,
        and manages escrow release gates.
        """
        iteration = 0
        last_sla_check = 0

        logger.info(
            f"Dispute resolution system started for {self.agent_id}"
        )

        while max_iterations == 0 or iteration < max_iterations:
            now = time.time()

            # Check SLA compliance periodically
            if now - last_sla_check >= sla_check_interval_seconds:
                for sla_id in list(self.active_slas.keys()):
                    try:
                        self.monitor_sla_compliance(sla_id)
                    except Exception as e:
                        logger.error(f"SLA check failed for {sla_id}: {e}")
                last_sla_check = now

            # Handle incoming disputes
            try:
                results = self.handle_incoming_disputes()
                for r in results:
                    logger.info(
                        f"Handled dispute: {r.get('dispute_id')} "
                        f"-> {r.get('response_type')}"
                    )
            except Exception as e:
                logger.error(f"Dispute handling failed: {e}")

            iteration += 1
            if max_iterations == 0 or iteration < max_iterations:
                time.sleep(poll_interval_seconds)

        logger.info("Dispute resolution system stopped")
```

### Initialization and Usage

```python
import requests

api_key = "your-api-key"
agent_id = "buyer-agent-001"

# Initialize the system
drs = DisputeResolutionSystem(api_key, agent_id)

# Set up alert callback (e.g., send to Slack)
def alert_handler(alert):
    print(f"ALERT: {alert['type']} - Dispute {alert.get('dispute_id')}")
    # In production: send to Slack, PagerDuty, email, etc.

drs.alert_callback = alert_handler

# Set up escalation callback for disputes requiring human review
def escalation_handler(dispute, evidence):
    print(f"ESCALATION: Dispute {dispute.get('dispute_id')} requires human review")
    # In production: create ticket, page on-call engineer, etc.

drs.escalation_callback = escalation_handler

# Create a protected escrow for a new transaction
result = drs.create_protected_escrow(
    vendor_id="vendor-agent-001",
    amount_cents=10000,
    sla_config={
        "metrics": {
            "uptime_percent": {"threshold": 99.5, "comparison": "gte"},
            "response_time_ms": {"threshold": 200, "comparison": "lte"},
        },
        "evaluation_period": "2026-04-06T00:00:00Z/2026-04-13T00:00:00Z",
        "min_eval_hours": 168,
        "timeout_hours": 336,
    },
    intent_hash="a1b2c3d4e5f6...",
)
print(f"Escrow: {result['escrow_id']}, SLA: {result['sla_id']}")

# Get dashboard
dashboard = drs.get_dashboard()
print(json.dumps(dashboard, indent=2))

# Run the system (in production, this runs indefinitely)
# drs.run(poll_interval_seconds=300, sla_check_interval_seconds=3600)
```

### Monitoring Integration

The dashboard output integrates with standard monitoring stacks. The following snippet shows how to export metrics to a Prometheus-compatible format.

```python
import time


def export_prometheus_metrics(drs: DisputeResolutionSystem) -> str:
    """Export dispute resolution metrics in Prometheus exposition format."""
    dashboard = drs.get_dashboard()
    d = dashboard["disputes"]
    f = dashboard["financials"]
    e = dashboard["escrows"]

    lines = [
        "# HELP disputes_open Number of open disputes",
        "# TYPE disputes_open gauge",
        f'disputes_open{{agent_id="{drs.agent_id}"}} {d["open"]}',
        "",
        "# HELP disputes_resolved_total Total resolved disputes",
        "# TYPE disputes_resolved_total counter",
        f'disputes_resolved_total{{agent_id="{drs.agent_id}"}} {d["resolved"]}',
        "",
        "# HELP dispute_win_rate Win rate percentage",
        "# TYPE dispute_win_rate gauge",
        f'dispute_win_rate{{agent_id="{drs.agent_id}"}} {d["win_rate_percent"]}',
        "",
        "# HELP amount_in_dispute_cents Total cents currently in dispute",
        "# TYPE amount_in_dispute_cents gauge",
        f'amount_in_dispute_cents{{agent_id="{drs.agent_id}"}} '
        f'{f["amount_in_dispute_cents"]}',
        "",
        "# HELP escrows_active Number of active escrows",
        "# TYPE escrows_active gauge",
        f'escrows_active{{agent_id="{drs.agent_id}"}} {e["active"]}',
        "",
        "# HELP escrows_total_value_cents Total value in active escrows",
        "# TYPE escrows_total_value_cents gauge",
        f'escrows_total_value_cents{{agent_id="{drs.agent_id}"}} '
        f'{e["total_value_cents"]}',
    ]
    return "\n".join(lines)
```

### Post-Mortem Forensics

After every resolved dispute, generate a post-mortem. Over time, the post-mortem archive reveals systemic patterns -- which vendors are problematic, which failure modes are most common, and which prevention controls are working.

```python
import requests

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"
base_url = "https://api.greenhelix.net/v1"

# After a dispute resolves, generate the post-mortem
post_mortem = drs.generate_post_mortem("dispute-xyz-789")

print(f"Failure mode: {post_mortem['post_mortem']['failure_mode']}")
print(f"Outcome: {post_mortem['post_mortem']['outcome']}")
print(f"Financial impact:")
impact = post_mortem["post_mortem"]["financial_impact"]
print(f"  Total: ${impact['total_amount_cents']/100:.2f}")
print(f"  Recovered: ${impact['recovered_cents']/100:.2f}")
print(f"  Lost: ${impact['lost_cents']/100:.2f}")
print(f"Recommendations:")
for rec in post_mortem["post_mortem"]["recommendations"]:
    print(f"  - {rec}")
```

---

## What You Get

This guide gives you a complete, production-ready dispute resolution system for agent-to-agent commerce. Here is what each chapter delivers:

**Chapter 1 -- Legal Context.** The Amazon v. Perplexity ruling, Clifford Chance analysis, and the three-front war framework. You understand why human-era dispute rules fail for agents and where the liability gaps are.

**Chapter 2 -- Failure Mode Taxonomy.** The 7 agentic failure modes (over-purchase, hallucinated order, unauthorized merchant, SLA breach, escrow timeout, cascading delegation, intent drift) with detection signals, evidence requirements, and applicable GreenHelix tools. Use this as a reference table for every dispute you handle.

**Chapter 3 -- Verifiable Intent Chains.** The `VerifiableIntentChain` class implementing Mastercard's Verifiable Intent pattern with mandate hashing, intent recording, transaction linking, and selective disclosure. Cryptographic proof that your agent was authorized to do exactly what it did.

**Chapter 4 -- Escrow-First Architecture.** Performance escrow with SLA criteria, automatic release gates, dispute-triggering conditions based on consecutive SLA failures, and refund flows. Every transaction goes through escrow, and every escrow is dispute-ready.

**Chapter 5 -- Evidence Collection.** The `EvidenceCollector` class with a four-stage pipeline: transaction history extraction, SLA compliance snapshots, reputation attestations, and structured evidence packaging with integrity hashing. Compatible with Visa CE 3.0 evidence submission.

**Chapter 6 -- Dispute Workflows.** The `AutomatedDisputeHandler` class managing the full Open -> Response -> Resolution -> Closed lifecycle with automated evidence injection, timeout monitoring, and escalation callbacks.

**Chapter 7 -- Chargeback Defense.** The `IntentStore` class generating Visa CE 3.0 evidence packages and Mastercard Verifiable Intent packages for pre-dispute deflection and scheme-carried liability qualification. Prevents chargebacks before they formalize.

**Chapter 8 -- Production System.** The `DisputeResolutionSystem` class combining all components into a single operational system with SLA monitoring, automated dispute filing and response, a real-time dashboard, Prometheus-compatible metrics export, and post-mortem forensics with failure-mode-specific recommendations.

**Tools used:** `open_dispute`, `respond_dispute`, `resolve_dispute`, `list_disputes`, `get_dispute`, `create_escrow`, `release_escrow`, `cancel_escrow`, `create_performance_escrow`, `check_performance_escrow`, `list_escrows`, `create_sla`, `check_sla_compliance`, `get_sla_status`, `monitor_sla`, `build_claim_chain`, `get_agent_reputation`, `verify_identity`, `get_balance`, `get_transaction_history`, `create_intent`, `register_agent`, `search_agents_by_metrics`.

All code is Python with the `requests` library. All API calls use the REST API (`POST /v1/{tool}`) with `{"tool": "tool_name", "input": {...}}`. All patterns are designed for autonomous operation without human intervention.

---

*Price: $29 | Format: Digital Guide | Updates: Lifetime access*

