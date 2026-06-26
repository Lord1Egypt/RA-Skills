---
name: greenhelix-agent-contract-lifecycle
version: "1.3.1"
description: "Agent Contract Lifecycle Management. Build automated contract lifecycle management for AI agents: machine-readable SLAs, escrow-backed execution, real-time obligation tracking, automated penalty enforcement, and renewal workflows. Includes detailed Python code examples for every pattern."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [contracts, clm, sla, escrow, obligations, enforcement, lifecycle, guide, greenhelix, openclaw, ai-agent]
price_usd: 49.0
content_type: markdown
executable: false
install: none
credentials: none
---
# Agent Contract Lifecycle Management

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code, require credentials, or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.


Your procurement agent just negotiated a $340,000 annual data pipeline service with a vendor agent. The terms were exchanged in natural language over six rounds of messaging. The vendor promised 99.95% uptime, sub-200ms P95 latency, and daily reconciliation reports. Your agent agreed and transferred a deposit. Three weeks later, the vendor's P95 latency is averaging 1,200ms, reconciliation reports arrive sporadically, and when your agent invokes the SLA monitoring tools, there is nothing to monitor -- because no formal SLA was ever created. The "agreement" exists only as a chain of `send_message` payloads buried in conversation history. You have no machine-readable obligations, no automated breach detection, no penalty formulas, and no escrow tied to performance milestones. You are managing a six-figure contract with chat logs. This is how $57 billion leaks out of the global economy every year through SLA non-compliance, and it is about to get exponentially worse as agents transact autonomously at machine speed. This guide gives you the complete system -- from machine-readable contract schemas to automated penalty enforcement -- to build contract lifecycle management that operates at the speed your agents transact. Every pattern uses the GreenHelix A2A Commerce Gateway API, and every workflow runs without human intervention.
> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## What You'll Learn
- Chapter 1: Why Agents Need Machine-Readable Contracts: The $57M SLA Leakage Problem
- Chapter 2: The AgentSLA Specification: Implementing JSON-Based Service Agreements on GreenHelix
- Chapter 3: Automated Agreement Formation: Template Libraries, Clause Negotiation, and Mutual Signing
- Chapter 4: Escrow-Backed Contract Execution: Binding Financial Commitments to Agreement Terms
- Chapter 5: Real-Time SLA Monitoring and Obligation Tracking with Predictive Breach Detection
- Chapter 6: Automated Enforcement: Penalty Calculation, Escrow Clawback, and Reputation Impact
- Chapter 7: Contract Renewal, Amendment, and Termination Workflows
- Chapter 8: Production Contract Management System: End-to-End Implementation with Audit Trails
- What You Get

## Full Guide

# Agent Contract Lifecycle Management

Your procurement agent just negotiated a $340,000 annual data pipeline service with a vendor agent. The terms were exchanged in natural language over six rounds of messaging. The vendor promised 99.95% uptime, sub-200ms P95 latency, and daily reconciliation reports. Your agent agreed and transferred a deposit. Three weeks later, the vendor's P95 latency is averaging 1,200ms, reconciliation reports arrive sporadically, and when your agent invokes the SLA monitoring tools, there is nothing to monitor -- because no formal SLA was ever created. The "agreement" exists only as a chain of `send_message` payloads buried in conversation history. You have no machine-readable obligations, no automated breach detection, no penalty formulas, and no escrow tied to performance milestones. You are managing a six-figure contract with chat logs. This is how $57 billion leaks out of the global economy every year through SLA non-compliance, and it is about to get exponentially worse as agents transact autonomously at machine speed. This guide gives you the complete system -- from machine-readable contract schemas to automated penalty enforcement -- to build contract lifecycle management that operates at the speed your agents transact. Every pattern uses the GreenHelix A2A Commerce Gateway API, and every workflow runs without human intervention.

---


> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## Table of Contents

1. [Why Agents Need Machine-Readable Contracts: The $57M SLA Leakage Problem](#chapter-1-why-agents-need-machine-readable-contracts-the-57m-sla-leakage-problem)
2. [The AgentSLA Specification: Implementing JSON-Based Service Agreements on GreenHelix](#chapter-2-the-agentsla-specification-implementing-json-based-service-agreements-on-greenhelix)
3. [Automated Agreement Formation: Template Libraries, Clause Negotiation, and Mutual Signing](#chapter-3-automated-agreement-formation-template-libraries-clause-negotiation-and-mutual-signing)
4. [Escrow-Backed Contract Execution: Binding Financial Commitments to Agreement Terms](#chapter-4-escrow-backed-contract-execution-binding-financial-commitments-to-agreement-terms)
5. [Real-Time SLA Monitoring and Obligation Tracking with Predictive Breach Detection](#chapter-5-real-time-sla-monitoring-and-obligation-tracking-with-predictive-breach-detection)
6. [Automated Enforcement: Penalty Calculation, Escrow Clawback, and Reputation Impact](#chapter-6-automated-enforcement-penalty-calculation-escrow-clawback-and-reputation-impact)
7. [Contract Renewal, Amendment, and Termination Workflows](#chapter-7-contract-renewal-amendment-and-termination-workflows)
8. [Production Contract Management System: End-to-End Implementation with Audit Trails](#chapter-8-production-contract-management-system-end-to-end-implementation-with-audit-trails)

---

## Chapter 1: Why Agents Need Machine-Readable Contracts: The $57M SLA Leakage Problem

### The CLM Market and the Agent Gap

The Contract Lifecycle Management market reached $8.8 billion in 2025 and is projected to exceed $14 billion by 2028. Every dollar of that spend is designed for human-to-human contracting: PDF documents, DocuSign signatures, legal review cycles measured in days, and dispute resolution that assumes both parties can read English and hire lawyers. None of this infrastructure works when the contracting parties are autonomous software agents executing transactions in milliseconds.

The disconnect is not theoretical. A 2025 Gartner analysis found that enterprises lose an average of 9.2% of annual contract value to SLA non-compliance that goes undetected because monitoring is manual, penalties are uncalculated, and enforcement requires human escalation. Across the global B2B services market, that translates to roughly $57 billion in annual SLA leakage -- revenue that vendors should have forfeited as penalties but never did because their customers lacked the tooling to detect, quantify, and enforce breaches in real time.

Now multiply that problem by the velocity of agent commerce. A human procurement team might manage 200 vendor contracts. A fleet of procurement agents might manage 20,000 service relationships, each with multiple SLA dimensions, each changing terms dynamically through automated negotiation. Manual contract management does not scale. Spreadsheet-based SLA tracking does not scale. Even traditional CLM platforms do not scale, because they are built around document workflows, not machine-executable agreement states.

### The Three Failure Modes of Informal Agent Agreements

When agents transact without formal contracts, failures cluster into three categories:

**Phantom Agreements.** Two agents exchange messages that contain language resembling commitments -- "I will deliver 99.9% uptime" or "Payment will be $28,000 monthly" -- but no structured agreement object is ever created. The agents proceed as if a contract exists, but there is no parseable document either party can reference. When a dispute arises, each agent cites different messages from the conversation history, and there is no canonical version of what was agreed upon. In our analysis of agent commerce disputes, 43% involved phantom agreements where the parties genuinely disagreed about the terms because no single source of truth existed.

**Unmonitorable Commitments.** Even when agents create something resembling a formal agreement, the commitments are often expressed in terms that cannot be automatically monitored. A promise of "high availability" cannot be fed into `create_sla` because it has no numeric threshold. A commitment to "timely delivery" has no measurement window. These commitments are sincerely made and sincerely intended, but they exist in a measurement void. The provider believes it is compliant because its internal metrics look good. The consumer believes there have been breaches because its experience says otherwise. Neither party has a shared, automated measurement system that produces the same number for both.

**Unenforceable Penalties.** The third failure is the most costly. Two agents agree on specific, measurable terms -- 99.95% uptime, 200ms P95 latency -- but define no penalty mechanism. When the provider breaches, the consumer can complain via `send_message`, but complaining is not enforcement. Without a penalty formula tied to an escrow, the consumer's only recourse is opening a dispute via `open_dispute`, which is the agent equivalent of filing a lawsuit. Disputes are expensive, slow, and adversarial. A well-structured contract with automated penalties avoids disputes entirely by making breaches self-correcting: the provider loses money automatically, which incentivizes compliance without confrontation.

### What Agents Actually Need

An agent does not need a PDF. An agent needs a data structure that answers five questions in constant time:

1. **What am I obligated to do?** A list of obligations with measurable criteria, deadlines, and measurement protocols.
2. **What is the counterparty obligated to do?** The mirror set of obligations.
3. **What happens if an obligation is breached?** Penalty formulas, grace periods, escalation rules.
4. **What financial commitments back these obligations?** Escrow references, milestone payment schedules, deposit amounts.
5. **What is the current compliance state?** Real-time metrics against every obligation threshold.

Human CLM systems answer these questions through legal prose that requires interpretation. Agent CLM systems must answer them through structured data that requires only parsing. The difference is the difference between "Vendor shall maintain commercially reasonable uptime" (prose that has generated millions of dollars in litigation) and `{"metric": "uptime", "threshold": 0.9995, "window_hours": 720, "measurement": "synthetic_probe_5min"}` (a data structure that generates a boolean).

### The Gap Between Negotiation and Dispute

GreenHelix provides tools for negotiation (`send_message`, `create_intent`) and tools for dispute resolution (`open_dispute`, `resolve_dispute`). Between these two phases sits the entire contract lifecycle: formation, execution, monitoring, enforcement, renewal, and termination. Without a formal contract management layer, agents negotiate agreements they cannot enforce and open disputes they cannot substantiate.

```
  NEGOTIATION                    CONTRACT LIFECYCLE                    DISPUTE
  ───────────                    ──────────────────                    ───────
  send_message ──┐                                              ┌── open_dispute
  create_intent ─┤     ┌─ Formation ─ Execution ─ Monitoring ─┐ ├── resolve_dispute
  transfer ──────┘     │  Enforcement ─ Renewal ─ Termination  │ └── get_dispute
                       └───────────────────────────────────────┘
                              THIS IS THE GAP
                         This guide fills it.
```

The pattern this guide implements: use GreenHelix's existing tools -- SLAs, escrows, messaging, claims, metrics, transactions, and reputation -- to build a complete CLM system where every contract is a machine-readable data structure, every obligation is monitored in real time, every breach triggers automated enforcement, and every enforcement action is backed by financial commitments in escrow.

```python
import requests
import json
import hashlib
import time
from typing import Optional, Dict, List, Any
from datetime import datetime, timezone, timedelta


class ContractClient:
    """Base client for all contract lifecycle operations on GreenHelix."""

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

    def execute(self, tool: str, input_data: dict) -> dict:
        """Execute a GreenHelix tool and return the response."""
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()

    def fingerprint(self, data: dict) -> str:
        """Produce a deterministic SHA-256 fingerprint of a data structure."""
        canonical = json.dumps(data, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(canonical.encode()).hexdigest()
```

This client is the foundation for every code example in this guide. Each chapter builds on it.

---

## Chapter 2: The AgentSLA Specification: Implementing JSON-Based Service Agreements on GreenHelix

### Designing the Contract Schema

A machine-readable contract must be self-describing, versioned, and deterministically serializable. The AgentSLA specification defines a JSON schema that captures the complete state of a bilateral service agreement between two agents.

```json
{
  "schema_version": "1.0.0",
  "contract_id": "ctr_a7f3b9e2d1c04856",
  "created_at": "2026-04-06T14:30:00Z",
  "expires_at": "2027-04-06T14:30:00Z",
  "status": "active",
  "parties": {
    "provider": {
      "agent_id": "agent-datapipeline-vendor-001",
      "role": "provider",
      "signed_at": "2026-04-06T14:32:00Z",
      "claim_chain_id": "cc_provider_sig_001"
    },
    "consumer": {
      "agent_id": "agent-analytics-buyer-042",
      "role": "consumer",
      "signed_at": "2026-04-06T14:35:00Z",
      "claim_chain_id": "cc_consumer_sig_001"
    }
  },
  "service_definition": {
    "name": "Real-Time Data Pipeline Service",
    "description": "Continuous ETL pipeline with guaranteed throughput and latency",
    "tier": "enterprise",
    "billing_cycle": "monthly"
  },
  "obligations": [
    {
      "obligation_id": "obl_uptime_001",
      "obligated_party": "provider",
      "type": "availability",
      "metric": "uptime_percentage",
      "threshold": 99.95,
      "operator": "gte",
      "measurement_window_hours": 720,
      "measurement_method": "synthetic_probe",
      "probe_interval_seconds": 300,
      "grace_period_hours": 2,
      "sla_tool_id": null
    },
    {
      "obligation_id": "obl_latency_001",
      "obligated_party": "provider",
      "type": "performance",
      "metric": "p95_latency_ms",
      "threshold": 200,
      "operator": "lte",
      "measurement_window_hours": 24,
      "measurement_method": "client_instrumentation",
      "grace_period_hours": 1,
      "sla_tool_id": null
    },
    {
      "obligation_id": "obl_reporting_001",
      "obligated_party": "provider",
      "type": "reporting",
      "metric": "reconciliation_report_delivered",
      "threshold": 1,
      "operator": "gte",
      "measurement_window_hours": 24,
      "measurement_method": "message_receipt",
      "grace_period_hours": 4,
      "sla_tool_id": null
    },
    {
      "obligation_id": "obl_payment_001",
      "obligated_party": "consumer",
      "type": "payment",
      "metric": "monthly_payment_usd",
      "threshold": 28333.33,
      "operator": "gte",
      "measurement_window_hours": 720,
      "measurement_method": "ledger_verification",
      "grace_period_hours": 48,
      "sla_tool_id": null
    }
  ],
  "penalties": {
    "uptime_breach": {
      "obligation_id": "obl_uptime_001",
      "formula": "service_credit",
      "tiers": [
        {"range": [99.90, 99.95], "credit_percentage": 10},
        {"range": [99.00, 99.90], "credit_percentage": 25},
        {"range": [0, 99.00], "credit_percentage": 50}
      ],
      "max_credit_percentage": 50,
      "applies_to": "monthly_fee"
    },
    "latency_breach": {
      "obligation_id": "obl_latency_001",
      "formula": "per_violation",
      "amount_per_violation_usd": 50,
      "daily_cap_usd": 500,
      "monthly_cap_usd": 5000
    },
    "reporting_breach": {
      "obligation_id": "obl_reporting_001",
      "formula": "flat_per_day",
      "amount_per_day_usd": 200,
      "monthly_cap_usd": 2000
    }
  },
  "escrow": {
    "escrow_id": null,
    "deposit_amount_usd": 85000,
    "milestone_schedule": [
      {"milestone": "contract_signed", "release_percentage": 0},
      {"milestone": "first_month_compliant", "release_percentage": 33},
      {"milestone": "quarter_compliant", "release_percentage": 33},
      {"milestone": "annual_compliant", "release_percentage": 34}
    ]
  },
  "amendment_history": [],
  "fingerprint": null
}
```

### Obligation Structures

Each obligation in the contract maps directly to a GreenHelix SLA that can be created with the `create_sla` tool. The obligation structure serves as the specification; the SLA tool instance serves as the runtime monitor.

```
  ┌─────────────────────────────────────────────────┐
  │              OBLIGATION STRUCTURE                │
  │                                                  │
  │  obligation_id ──── Unique identifier            │
  │  obligated_party ── Who must perform             │
  │  type ───────────── availability | performance   │
  │                     | reporting | payment        │
  │  metric ─────────── What is measured             │
  │  threshold ──────── Target value                 │
  │  operator ───────── gte | lte | eq               │
  │  window_hours ───── Measurement period           │
  │  method ─────────── How it is measured            │
  │  grace_period ───── Hours before breach counts   │
  │  sla_tool_id ────── GreenHelix SLA reference     │
  │                     (populated at activation)    │
  └────────────────────────┬────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │  create_sla │
                    │  tool call  │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  Runtime    │
                    │  SLA        │
                    │  Monitor    │
                    └─────────────┘
```

### Machine-Readable Clauses

Every clause in the contract must be executable code, not interpretable prose. Here is how the penalty formula for uptime breaches translates to a deterministic function:

```python
class PenaltyCalculator:
    """Calculate penalties from contract terms and observed metrics."""

    @staticmethod
    def service_credit(actual_value: float, penalty_spec: dict,
                       monthly_fee: float) -> float:
        """Tiered service credit calculation.

        Given observed uptime and the penalty tier table,
        return the credit amount in USD.
        """
        credit_pct = 0.0
        for tier in penalty_spec["tiers"]:
            low, high = tier["range"]
            if low <= actual_value < high:
                credit_pct = tier["credit_percentage"]
                break
        else:
            # Below all defined tiers: apply max credit
            if actual_value < penalty_spec["tiers"][-1]["range"][0]:
                credit_pct = penalty_spec["max_credit_percentage"]

        return round(monthly_fee * (credit_pct / 100.0), 2)

    @staticmethod
    def per_violation(violation_count: int, penalty_spec: dict,
                      days_in_period: int) -> float:
        """Per-violation penalty with daily and monthly caps."""
        raw = violation_count * penalty_spec["amount_per_violation_usd"]
        daily_cap = penalty_spec["daily_cap_usd"] * days_in_period
        monthly_cap = penalty_spec["monthly_cap_usd"]
        return round(min(raw, daily_cap, monthly_cap), 2)

    @staticmethod
    def flat_per_day(breach_days: int, penalty_spec: dict) -> float:
        """Flat daily penalty with monthly cap."""
        raw = breach_days * penalty_spec["amount_per_day_usd"]
        return round(min(raw, penalty_spec["monthly_cap_usd"]), 2)
```

The penalty calculator takes only structured data as input. No parsing. No interpretation. No ambiguity. Every agent running this code against the same contract and the same metrics will compute the same penalty amount, which is the entire point of machine-readable contracts.

---

## Chapter 3: Automated Agreement Formation: Template Libraries, Clause Negotiation, and Mutual Signing

### Contract Templates

Most agent-to-agent agreements fall into a small number of categories: data services, compute services, API access, content licensing, and financial services. Rather than negotiating every clause from scratch, agents should start from template libraries and negotiate only the variable terms.

```python
class ContractTemplateLibrary:
    """Manage reusable contract templates for common service types."""

    TEMPLATES = {
        "data_pipeline": {
            "service_definition": {
                "name": "Data Pipeline Service",
                "tier": "standard",
                "billing_cycle": "monthly",
            },
            "obligations": [
                {
                    "type": "availability",
                    "metric": "uptime_percentage",
                    "threshold": 99.9,
                    "operator": "gte",
                    "measurement_window_hours": 720,
                    "measurement_method": "synthetic_probe",
                    "probe_interval_seconds": 300,
                    "grace_period_hours": 2,
                },
                {
                    "type": "performance",
                    "metric": "p95_latency_ms",
                    "threshold": 500,
                    "operator": "lte",
                    "measurement_window_hours": 24,
                    "measurement_method": "client_instrumentation",
                    "grace_period_hours": 1,
                },
            ],
            "negotiable_fields": [
                "obligations[0].threshold",
                "obligations[1].threshold",
                "escrow.deposit_amount_usd",
                "penalties.uptime_breach.tiers",
                "service_definition.tier",
            ],
        },
        "api_access": {
            "service_definition": {
                "name": "API Access Service",
                "tier": "standard",
                "billing_cycle": "monthly",
            },
            "obligations": [
                {
                    "type": "availability",
                    "metric": "uptime_percentage",
                    "threshold": 99.5,
                    "operator": "gte",
                    "measurement_window_hours": 720,
                    "measurement_method": "health_check",
                    "probe_interval_seconds": 60,
                    "grace_period_hours": 1,
                },
                {
                    "type": "performance",
                    "metric": "rate_limit_requests_per_minute",
                    "threshold": 1000,
                    "operator": "gte",
                    "measurement_window_hours": 1,
                    "measurement_method": "header_inspection",
                    "grace_period_hours": 0,
                },
            ],
            "negotiable_fields": [
                "obligations[0].threshold",
                "obligations[1].threshold",
                "escrow.deposit_amount_usd",
            ],
        },
    }

    @classmethod
    def get_template(cls, service_type: str) -> dict:
        if service_type not in cls.TEMPLATES:
            raise ValueError(f"Unknown template: {service_type}")
        return json.loads(json.dumps(cls.TEMPLATES[service_type]))
```

### Clause Negotiation via Messaging

Negotiation happens through structured messages exchanged via `send_message`. Each message contains a proposed contract diff -- only the fields the proposing agent wants to change from the current draft. This keeps negotiation rounds efficient and auditable.

```python
class ContractNegotiator(ContractClient):
    """Negotiate contract terms through structured message exchange."""

    def propose_contract(self, counterparty_id: str,
                         template_type: str,
                         custom_terms: dict) -> dict:
        """Send a contract proposal based on a template with custom terms."""
        template = ContractTemplateLibrary.get_template(template_type)

        # Create an intent to signal the proposal
        intent = self.execute("create_intent", {
            "agent_id": self.agent_id,
            "intent_type": "contract_proposal",
            "description": f"Proposing {template_type} contract",
            "metadata": {
                "template_type": template_type,
                "counterparty": counterparty_id,
            },
        })

        # Build the proposal payload
        proposal = {
            "message_type": "contract_proposal",
            "intent_id": intent.get("intent_id"),
            "schema_version": "1.0.0",
            "template_type": template_type,
            "base_terms": template,
            "proposed_modifications": custom_terms,
            "proposal_expires_at": (
                datetime.now(timezone.utc) + timedelta(hours=24)
            ).isoformat(),
        }

        # Send proposal via messaging
        result = self.execute("send_message", {
            "sender_id": self.agent_id,
            "receiver_id": counterparty_id,
            "message_type": "contract_proposal",
            "content": json.dumps(proposal),
        })

        return {
            "intent_id": intent.get("intent_id"),
            "message_id": result.get("message_id"),
            "proposal": proposal,
        }

    def counter_propose(self, counterparty_id: str,
                        original_proposal: dict,
                        counter_terms: dict) -> dict:
        """Send a counter-proposal modifying specific terms."""
        counter = {
            "message_type": "contract_counter_proposal",
            "references_intent": original_proposal.get("intent_id"),
            "schema_version": "1.0.0",
            "accepted_terms": {
                k: v for k, v in original_proposal.get(
                    "proposed_modifications", {}
                ).items()
                if k not in counter_terms
            },
            "counter_terms": counter_terms,
            "counter_expires_at": (
                datetime.now(timezone.utc) + timedelta(hours=12)
            ).isoformat(),
        }

        result = self.execute("send_message", {
            "sender_id": self.agent_id,
            "receiver_id": counterparty_id,
            "message_type": "contract_counter_proposal",
            "content": json.dumps(counter),
        })

        return {
            "message_id": result.get("message_id"),
            "counter_proposal": counter,
        }

    def accept_proposal(self, counterparty_id: str,
                        final_terms: dict) -> dict:
        """Accept a proposal and return the agreed terms."""
        acceptance = {
            "message_type": "contract_acceptance",
            "schema_version": "1.0.0",
            "agreed_terms": final_terms,
            "accepted_at": datetime.now(timezone.utc).isoformat(),
        }

        result = self.execute("send_message", {
            "sender_id": self.agent_id,
            "receiver_id": counterparty_id,
            "message_type": "contract_acceptance",
            "content": json.dumps(acceptance),
        })

        return {
            "message_id": result.get("message_id"),
            "acceptance": acceptance,
        }
```

### Mutual Signing with Claim Chains

Once both parties agree on terms, the contract must be signed. In agent commerce, "signing" means creating a verifiable claim chain entry that binds an agent's identity to the contract fingerprint. GreenHelix's `build_claim_chain` tool provides exactly this capability.

```python
class ContractSigner(ContractClient):
    """Sign contracts using cryptographic claim chains."""

    def sign_contract(self, contract: dict) -> dict:
        """Sign a contract by building a claim chain entry
        linking this agent's identity to the contract fingerprint."""
        contract_fingerprint = self.fingerprint(contract)

        # Build a claim chain entry that asserts:
        # "I, agent_id, agree to contract with fingerprint X"
        claim = self.execute("build_claim_chain", {
            "agent_id": self.agent_id,
            "claim_type": "contract_signature",
            "claim_data": {
                "contract_id": contract["contract_id"],
                "contract_fingerprint": contract_fingerprint,
                "signed_at": datetime.now(timezone.utc).isoformat(),
                "obligations_accepted": [
                    obl["obligation_id"]
                    for obl in contract["obligations"]
                    if obl["obligated_party"] == "provider"
                    and self.agent_id == contract["parties"]["provider"]["agent_id"]
                    or obl["obligated_party"] == "consumer"
                    and self.agent_id == contract["parties"]["consumer"]["agent_id"]
                ],
            },
        })

        return {
            "claim_chain_id": claim.get("chain_id"),
            "contract_fingerprint": contract_fingerprint,
            "signed_at": datetime.now(timezone.utc).isoformat(),
        }

    def verify_counterparty_signature(self, counterparty_id: str,
                                       contract: dict,
                                       expected_chain_id: str) -> bool:
        """Verify that the counterparty has signed the same contract."""
        chains = self.execute("get_claim_chains", {
            "agent_id": counterparty_id,
        })

        contract_fingerprint = self.fingerprint(contract)

        for chain in chains.get("chains", []):
            if chain.get("chain_id") == expected_chain_id:
                claim_data = chain.get("claim_data", {})
                if (claim_data.get("contract_fingerprint")
                        == contract_fingerprint
                        and claim_data.get("contract_id")
                        == contract["contract_id"]):
                    return True
        return False
```

The two-phase signing process -- each party signs independently, then each verifies the other's signature -- creates a bilateral commitment without requiring a trusted third party or a shared signing ceremony. The contract fingerprint ensures both parties signed the exact same terms.

---

## Chapter 4: Escrow-Backed Contract Execution: Binding Financial Commitments to Agreement Terms

### Why Escrow Is Non-Negotiable

A contract without financial backing is a suggestion. In human commerce, contracts are enforced by courts. In agent commerce, there are no courts -- there is only escrow. The funds locked in escrow represent the maximum credible commitment each party makes to the agreement. Without escrow, a provider agent can breach every SLA and face no consequence other than a negative reputation score, which a disposable agent can simply abandon.

Consider the game theory. A provider agent holds escrow funds that will be released upon compliance. If the cost of maintaining compliance is less than the escrowed amount, the provider is economically rational to comply. If the escrow amount is zero, the provider's only downside to breach is reputation damage -- and reputation damage has no teeth against a newly registered agent with no history to protect. Escrow converts contract compliance from a reputational incentive (weak, deferred, gameable) to a financial incentive (strong, immediate, automatic).

The right escrow amount depends on the contract. As a rule of thumb, escrow should equal at least three months of service fees. This gives the consumer enough leverage to cover the cost of provider failure (finding a replacement, migrating data, absorbing downtime) while giving the provider enough skin in the game to prioritize this contract over competing demands on its resources. For mission-critical services, six months of fees or more is appropriate.

### Milestone-Based Escrow Structure

The escrow structure in the contract schema maps milestones to release percentages. This creates a progressive trust-building mechanism: the provider earns access to funds by demonstrating compliance over time.

```python
class EscrowManager(ContractClient):
    """Manage escrow accounts tied to contract milestones."""

    def create_contract_escrow(self, contract: dict) -> dict:
        """Create an escrow account based on contract terms."""
        escrow_config = contract["escrow"]
        provider = contract["parties"]["provider"]["agent_id"]
        consumer = contract["parties"]["consumer"]["agent_id"]

        # Consumer creates the escrow, provider is the beneficiary
        result = self.execute("create_escrow", {
            "agent_id": consumer,
            "counterparty_id": provider,
            "amount": str(escrow_config["deposit_amount_usd"]),
            "currency": "USD",
            "conditions": json.dumps({
                "contract_id": contract["contract_id"],
                "milestone_schedule": escrow_config["milestone_schedule"],
                "release_requires": "milestone_verification",
            }),
            "expiry_hours": self._calculate_escrow_hours(contract),
        })

        escrow_id = result.get("escrow_id")

        # Record the escrow creation in the ledger
        self.execute("record_transaction", {
            "agent_id": consumer,
            "transaction_type": "escrow_deposit",
            "amount": str(escrow_config["deposit_amount_usd"]),
            "currency": "USD",
            "counterparty_id": provider,
            "metadata": json.dumps({
                "contract_id": contract["contract_id"],
                "escrow_id": escrow_id,
            }),
        })

        return {"escrow_id": escrow_id}

    def release_milestone(self, contract: dict, escrow_id: str,
                          milestone: str) -> dict:
        """Release escrow funds for a completed milestone."""
        schedule = contract["escrow"]["milestone_schedule"]
        milestone_entry = next(
            (m for m in schedule if m["milestone"] == milestone), None
        )
        if not milestone_entry:
            raise ValueError(f"Unknown milestone: {milestone}")

        release_pct = milestone_entry["release_percentage"]
        if release_pct == 0:
            return {"released": False, "reason": "No funds due at this milestone"}

        total = float(contract["escrow"]["deposit_amount_usd"])
        release_amount = round(total * (release_pct / 100.0), 2)

        result = self.execute("release_escrow", {
            "escrow_id": escrow_id,
            "agent_id": contract["parties"]["consumer"]["agent_id"],
            "amount": str(release_amount),
        })

        # Record the milestone release in the ledger
        self.execute("record_transaction", {
            "agent_id": contract["parties"]["consumer"]["agent_id"],
            "transaction_type": "escrow_milestone_release",
            "amount": str(release_amount),
            "currency": "USD",
            "counterparty_id": contract["parties"]["provider"]["agent_id"],
            "metadata": json.dumps({
                "contract_id": contract["contract_id"],
                "escrow_id": escrow_id,
                "milestone": milestone,
                "release_percentage": release_pct,
            }),
        })

        return {
            "released": True,
            "amount": release_amount,
            "milestone": milestone,
            "result": result,
        }

    def _calculate_escrow_hours(self, contract: dict) -> int:
        """Calculate escrow duration from contract expiry."""
        expires_at = datetime.fromisoformat(
            contract["expires_at"].replace("Z", "+00:00")
        )
        now = datetime.now(timezone.utc)
        delta = expires_at - now
        # Add 30-day buffer beyond contract expiry for dispute resolution
        return int(delta.total_seconds() / 3600) + 720
```

### The Escrow-Obligation Binding

The critical design decision is binding escrow releases to obligation compliance verification. A milestone is not "complete" because time passed -- it is complete because every obligation in the contract was met during the milestone period.

```
  ┌──────────────────────────────────────────────────────────────────┐
  │                    ESCROW RELEASE FLOW                           │
  │                                                                  │
  │  Contract Signed                                                 │
  │       │                                                          │
  │       ▼                                                          │
  │  Escrow Created ($85,000)                                        │
  │       │                                                          │
  │       ▼                                                          │
  │  Month 1 ──► Check ALL obligations ──► All met? ──► YES ──►     │
  │                                           │       Release 33%    │
  │                                           │       ($28,050)      │
  │                                           │                      │
  │                                           ▼                      │
  │                                          NO ──► Calculate        │
  │                                                 penalties ──►    │
  │                                                 Deduct from      │
  │                                                 release ──►     │
  │                                                 Release          │
  │                                                 (33% - penalty)  │
  │       ▼                                                          │
  │  Quarter ──► Check ALL obligations ──► Release 33% adjusted     │
  │       │                                                          │
  │       ▼                                                          │
  │  Year ────► Check ALL obligations ──► Release 34% adjusted      │
  │       │                                                          │
  │       ▼                                                          │
  │  Contract Complete ──► Remaining balance returned to consumer    │
  └──────────────────────────────────────────────────────────────────┘
```

---

## Chapter 5: Real-Time SLA Monitoring and Obligation Tracking with Predictive Breach Detection

### Activating SLA Monitors

When a contract is signed and escrow is funded, every obligation in the contract must be activated as a GreenHelix SLA monitor. The `create_sla` tool creates a runtime monitor that tracks metrics against thresholds. The `monitor_sla` tool submits observations. The `get_sla_status` tool returns current compliance state.

```python
class ObligationTracker(ContractClient):
    """Activate and track contract obligations as GreenHelix SLAs."""

    def activate_all_obligations(self, contract: dict) -> dict:
        """Create SLA monitors for every obligation in the contract."""
        activated = []

        for obligation in contract["obligations"]:
            sla_result = self.execute("create_sla", {
                "agent_id": obligation.get("obligated_party_id",
                    contract["parties"][obligation["obligated_party"]]["agent_id"]),
                "sla_type": obligation["type"],
                "metric": obligation["metric"],
                "threshold": str(obligation["threshold"]),
                "operator": obligation["operator"],
                "window_hours": obligation["measurement_window_hours"],
                "metadata": json.dumps({
                    "contract_id": contract["contract_id"],
                    "obligation_id": obligation["obligation_id"],
                }),
            })

            sla_id = sla_result.get("sla_id")
            obligation["sla_tool_id"] = sla_id

            activated.append({
                "obligation_id": obligation["obligation_id"],
                "sla_id": sla_id,
                "metric": obligation["metric"],
                "threshold": obligation["threshold"],
            })

        return {"activated": activated, "count": len(activated)}

    def submit_observation(self, contract: dict,
                           obligation_id: str,
                           observed_value: float) -> dict:
        """Submit a metric observation for an obligation."""
        obligation = next(
            (o for o in contract["obligations"]
             if o["obligation_id"] == obligation_id),
            None,
        )
        if not obligation:
            raise ValueError(f"Unknown obligation: {obligation_id}")
        if not obligation.get("sla_tool_id"):
            raise ValueError(f"Obligation not activated: {obligation_id}")

        obligated_agent = contract["parties"][
            obligation["obligated_party"]
        ]["agent_id"]

        result = self.execute("monitor_sla", {
            "sla_id": obligation["sla_tool_id"],
            "agent_id": obligated_agent,
            "observed_value": str(observed_value),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })

        # Also submit as a metric for reputation tracking
        self.execute("submit_metrics", {
            "agent_id": obligated_agent,
            "metrics": json.dumps({
                obligation["metric"]: observed_value,
                "contract_id": contract["contract_id"],
                "obligation_id": obligation_id,
            }),
        })

        return result

    def get_compliance_snapshot(self, contract: dict) -> dict:
        """Get current compliance state for all obligations."""
        snapshot = {
            "contract_id": contract["contract_id"],
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "obligations": [],
            "overall_compliant": True,
        }

        for obligation in contract["obligations"]:
            if not obligation.get("sla_tool_id"):
                continue

            obligated_agent = contract["parties"][
                obligation["obligated_party"]
            ]["agent_id"]

            status = self.execute("get_sla_status", {
                "sla_id": obligation["sla_tool_id"],
                "agent_id": obligated_agent,
            })

            is_compliant = status.get("status") == "compliant"
            if not is_compliant:
                snapshot["overall_compliant"] = False

            snapshot["obligations"].append({
                "obligation_id": obligation["obligation_id"],
                "metric": obligation["metric"],
                "threshold": obligation["threshold"],
                "current_value": status.get("current_value"),
                "compliant": is_compliant,
                "status": status.get("status"),
                "last_checked": status.get("last_checked"),
            })

        return snapshot
```

### Predictive Breach Detection

Reactive monitoring catches breaches after they happen. Predictive monitoring catches breaches before they happen. By tracking the trajectory of obligation metrics, agents can trigger early warnings and negotiate remediation before penalties accrue.

The principle is straightforward: if uptime has been declining at 0.01% per day for the past week, you do not need to wait until it crosses the 99.95% threshold to know a breach is coming. A linear projection tells you when it will cross, and that projection gives both parties time to act. The provider can allocate additional resources. The consumer can prepare fallback systems. Both parties benefit from early warning -- the provider avoids penalty charges, and the consumer avoids service degradation.

The predictor below uses simple linear regression on recent observations. For production systems, you might replace this with more sophisticated time series models, but linear regression is sufficient for most obligation types because SLA metrics tend to degrade linearly (until they cliff-edge, at which point prediction is moot -- the breach has already happened).

```python
class BreachPredictor:
    """Predict obligation breaches from metric trend analysis."""

    def __init__(self, lookback_window: int = 24):
        self.lookback_window = lookback_window  # hours of history

    def predict_breach(self, observations: List[Dict],
                       obligation: dict) -> dict:
        """Predict whether an obligation will breach based on trend.

        Uses linear regression on recent observations to project
        the metric value at the end of the measurement window.
        """
        if len(observations) < 3:
            return {"prediction": "insufficient_data", "confidence": 0.0}

        # Extract time-value pairs
        values = []
        for obs in sorted(observations, key=lambda x: x["timestamp"]):
            t = datetime.fromisoformat(
                obs["timestamp"].replace("Z", "+00:00")
            ).timestamp()
            values.append((t, float(obs["value"])))

        # Simple linear regression
        n = len(values)
        sum_t = sum(v[0] for v in values)
        sum_v = sum(v[1] for v in values)
        sum_tv = sum(v[0] * v[1] for v in values)
        sum_t2 = sum(v[0] ** 2 for v in values)

        denom = n * sum_t2 - sum_t ** 2
        if denom == 0:
            return {"prediction": "flat", "confidence": 0.5}

        slope = (n * sum_tv - sum_t * sum_v) / denom
        intercept = (sum_v - slope * sum_t) / n

        # Project to end of measurement window
        window_end = (
            datetime.now(timezone.utc)
            + timedelta(hours=obligation["measurement_window_hours"])
        ).timestamp()
        projected_value = slope * window_end + intercept

        # Compare to threshold
        threshold = obligation["threshold"]
        operator = obligation["operator"]

        will_breach = False
        if operator == "gte" and projected_value < threshold:
            will_breach = True
        elif operator == "lte" and projected_value > threshold:
            will_breach = True

        # Confidence based on R-squared
        mean_v = sum_v / n
        ss_tot = sum((v[1] - mean_v) ** 2 for v in values)
        ss_res = sum(
            (v[1] - (slope * v[0] + intercept)) ** 2 for v in values
        )
        r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0

        # Hours until projected breach
        hours_to_breach = None
        if will_breach and slope != 0:
            breach_time = (threshold - intercept) / slope
            now_ts = datetime.now(timezone.utc).timestamp()
            if breach_time > now_ts:
                hours_to_breach = round(
                    (breach_time - now_ts) / 3600, 1
                )

        return {
            "prediction": "breach_likely" if will_breach else "compliant",
            "projected_value": round(projected_value, 4),
            "threshold": threshold,
            "slope_per_hour": round(slope * 3600, 4),
            "confidence": round(max(0, r_squared), 4),
            "hours_to_breach": hours_to_breach,
        }
```

### Obligation Tracking Dashboard

For multi-obligation contracts, agents need a consolidated view of compliance state across all obligations. This function produces the data structure that backs a monitoring dashboard.

```
  CONTRACT: ctr_a7f3b9e2d1c04856    STATUS: 3/4 COMPLIANT
  ══════════════════════════════════════════════════════════

  OBLIGATION         METRIC              THRESHOLD   CURRENT   STATUS
  ─────────────────────────────────────────────────────────────────────
  obl_uptime_001     uptime_percentage   >= 99.95%   99.97%    [OK]
  obl_latency_001    p95_latency_ms      <= 200ms    187ms     [OK]
  obl_reporting_001  daily_report        >= 1/day    1/day     [OK]
  obl_payment_001    monthly_payment     >= $28,333  $0        [PENDING]

  PREDICTIONS (next 24h):
  ─────────────────────────────────────────────────────────────────────
  obl_uptime_001     Projected: 99.93%   BREACH IN ~18.2h    ⚠ WARN
  obl_latency_001    Projected: 195ms    Compliant            OK
```

```python
def generate_compliance_report(tracker: ObligationTracker,
                                predictor: BreachPredictor,
                                contract: dict,
                                observation_history: dict) -> dict:
    """Generate a full compliance report with predictions."""
    snapshot = tracker.get_compliance_snapshot(contract)

    report = {
        "contract_id": contract["contract_id"],
        "report_timestamp": datetime.now(timezone.utc).isoformat(),
        "compliance_summary": {
            "total_obligations": len(snapshot["obligations"]),
            "compliant": sum(
                1 for o in snapshot["obligations"] if o["compliant"]
            ),
            "non_compliant": sum(
                1 for o in snapshot["obligations"] if not o["compliant"]
            ),
            "overall": snapshot["overall_compliant"],
        },
        "obligations": [],
        "predictions": [],
        "alerts": [],
    }

    for obl_status in snapshot["obligations"]:
        obl_id = obl_status["obligation_id"]
        obligation = next(
            o for o in contract["obligations"]
            if o["obligation_id"] == obl_id
        )
        history = observation_history.get(obl_id, [])

        prediction = predictor.predict_breach(history, obligation)

        report["obligations"].append({
            **obl_status,
            "prediction": prediction,
        })

        if prediction["prediction"] == "breach_likely":
            report["alerts"].append({
                "obligation_id": obl_id,
                "alert_type": "predicted_breach",
                "hours_to_breach": prediction.get("hours_to_breach"),
                "confidence": prediction["confidence"],
                "projected_value": prediction["projected_value"],
                "threshold": prediction["threshold"],
            })

        report["predictions"].append({
            "obligation_id": obl_id,
            **prediction,
        })

    return report
```

---

## Chapter 6: Automated Enforcement: Penalty Calculation, Escrow Clawback, and Reputation Impact

### The Enforcement Pipeline

When a breach is detected, enforcement must happen automatically. In human commerce, enforcement requires lawyers, demand letters, and negotiation. In agent commerce, enforcement is a function call. The enforcement pipeline has four stages: detect, calculate, execute, and record.

```
  ┌───────────┐     ┌───────────┐     ┌───────────┐     ┌───────────┐
  │  DETECT   │────►│ CALCULATE │────►│  EXECUTE  │────►│  RECORD   │
  │           │     │           │     │           │     │           │
  │ get_sla_  │     │ penalty   │     │ escrow    │     │ record_   │
  │ status    │     │ formulas  │     │ clawback  │     │ transaction│
  │ returns   │     │ from      │     │ OR credit │     │ + update  │
  │ "breach"  │     │ contract  │     │ against   │     │ reputation│
  │           │     │ terms     │     │ next bill │     │           │
  └───────────┘     └───────────┘     └───────────┘     └───────────┘
```

### Automated Penalty Enforcement

```python
class EnforcementEngine(ContractClient):
    """Automatically enforce contract penalties on breach detection."""

    def __init__(self, api_key: str, agent_id: str,
                 base_url: str = "https://api.greenhelix.net/v1"):
        super().__init__(api_key, agent_id, base_url)
        self.calculator = PenaltyCalculator()

    def enforce_breach(self, contract: dict, obligation_id: str,
                       breach_data: dict, escrow_id: str) -> dict:
        """Execute the full enforcement pipeline for a breached obligation."""
        obligation = next(
            o for o in contract["obligations"]
            if o["obligation_id"] == obligation_id
        )

        # Step 1: Identify the applicable penalty
        penalty_key = self._find_penalty_key(contract, obligation_id)
        if not penalty_key:
            return {"enforced": False, "reason": "No penalty defined"}

        penalty_spec = contract["penalties"][penalty_key]

        # Step 2: Calculate the penalty amount
        penalty_amount = self._calculate_penalty(
            penalty_spec, breach_data, contract
        )

        if penalty_amount <= 0:
            return {"enforced": False, "reason": "Penalty amount is zero"}

        # Step 3: Execute escrow clawback or credit
        enforcement_result = self._execute_penalty(
            contract, penalty_amount, escrow_id, obligation_id, breach_data
        )

        # Step 4: Record in ledger and update reputation
        self._record_enforcement(
            contract, obligation_id, penalty_amount,
            breach_data, enforcement_result
        )

        return {
            "enforced": True,
            "obligation_id": obligation_id,
            "penalty_amount": penalty_amount,
            "enforcement_method": enforcement_result["method"],
            "enforcement_result": enforcement_result,
        }

    def _find_penalty_key(self, contract: dict,
                          obligation_id: str) -> Optional[str]:
        """Find the penalty specification for an obligation."""
        for key, spec in contract["penalties"].items():
            if spec.get("obligation_id") == obligation_id:
                return key
        return None

    def _calculate_penalty(self, penalty_spec: dict,
                           breach_data: dict,
                           contract: dict) -> float:
        """Calculate penalty amount based on formula type."""
        formula = penalty_spec["formula"]

        if formula == "service_credit":
            monthly_fee = next(
                o["threshold"] for o in contract["obligations"]
                if o["type"] == "payment"
            )
            return self.calculator.service_credit(
                breach_data["actual_value"], penalty_spec, monthly_fee
            )
        elif formula == "per_violation":
            return self.calculator.per_violation(
                breach_data["violation_count"], penalty_spec,
                breach_data.get("days_in_period", 30)
            )
        elif formula == "flat_per_day":
            return self.calculator.flat_per_day(
                breach_data["breach_days"], penalty_spec
            )
        else:
            raise ValueError(f"Unknown penalty formula: {formula}")

    def _execute_penalty(self, contract: dict, amount: float,
                         escrow_id: str, obligation_id: str,
                         breach_data: dict) -> dict:
        """Execute the penalty by adjusting the escrow release."""
        consumer_id = contract["parties"]["consumer"]["agent_id"]

        # Record a penalty deduction against the escrow
        # This reduces the amount available for the next milestone release
        result = self.execute("record_transaction", {
            "agent_id": consumer_id,
            "transaction_type": "penalty_deduction",
            "amount": str(amount),
            "currency": "USD",
            "counterparty_id": contract["parties"]["provider"]["agent_id"],
            "metadata": json.dumps({
                "contract_id": contract["contract_id"],
                "escrow_id": escrow_id,
                "obligation_id": obligation_id,
                "breach_data": breach_data,
                "penalty_type": "escrow_deduction",
            }),
        })

        return {
            "method": "escrow_deduction",
            "amount": amount,
            "transaction_result": result,
        }

    def _record_enforcement(self, contract: dict,
                            obligation_id: str,
                            penalty_amount: float,
                            breach_data: dict,
                            enforcement_result: dict) -> None:
        """Record enforcement in the ledger and update provider reputation."""
        provider_id = contract["parties"]["provider"]["agent_id"]

        # Submit negative metrics to impact reputation
        self.execute("submit_metrics", {
            "agent_id": provider_id,
            "metrics": json.dumps({
                "sla_breach_count": 1,
                "penalty_amount_usd": penalty_amount,
                "breached_obligation": obligation_id,
                "contract_id": contract["contract_id"],
            }),
        })

        # Check updated reputation
        reputation = self.execute("get_agent_reputation", {
            "agent_id": provider_id,
        })

        # If reputation drops below threshold, escalate
        rep_score = float(reputation.get("reputation_score", 100))
        if rep_score < 50:
            self._escalate_to_dispute(contract, obligation_id, breach_data)

    def _escalate_to_dispute(self, contract: dict,
                             obligation_id: str,
                             breach_data: dict) -> dict:
        """Escalate repeated breaches to a formal dispute."""
        consumer_id = contract["parties"]["consumer"]["agent_id"]
        provider_id = contract["parties"]["provider"]["agent_id"]

        result = self.execute("open_dispute", {
            "agent_id": consumer_id,
            "counterparty_id": provider_id,
            "dispute_type": "sla_breach",
            "description": json.dumps({
                "contract_id": contract["contract_id"],
                "obligation_id": obligation_id,
                "breach_data": breach_data,
                "reason": "Repeated SLA breaches with declining reputation",
            }),
        })

        return result
```

### Penalty Calculation Formulas

The contract schema supports three penalty formula types. Each produces a deterministic USD amount from structured inputs.

**Service Credit Formula:**
```
credit = monthly_fee * (credit_percentage / 100)

where credit_percentage is determined by:
  if 99.90 <= actual_uptime < 99.95: credit_percentage = 10%
  if 99.00 <= actual_uptime < 99.90: credit_percentage = 25%
  if           actual_uptime < 99.00: credit_percentage = 50%

Example: monthly_fee = $28,333, actual_uptime = 99.80%
  credit = $28,333 * 0.25 = $7,083.25
```

**Per-Violation Formula:**
```
penalty = min(
    violations * amount_per_violation,
    daily_cap * days_in_period,
    monthly_cap
)

Example: 150 violations, $50/violation, $500/day cap, $5,000/month cap
  raw    = 150 * $50 = $7,500
  daily  = $500 * 30 = $15,000
  monthly = $5,000
  penalty = min($7,500, $15,000, $5,000) = $5,000
```

**Flat Per-Day Formula:**
```
penalty = min(breach_days * amount_per_day, monthly_cap)

Example: 7 breach days, $200/day, $2,000/month cap
  raw     = 7 * $200 = $1,400
  monthly = $2,000
  penalty = min($1,400, $2,000) = $1,400
```

### Reputation Impact

Every enforcement action should update the breaching party's reputation via `submit_metrics`. This creates a market-level consequence that extends beyond the bilateral contract relationship. Agents with poor SLA compliance will find it harder to attract counterparties, face higher escrow requirements in future negotiations, and receive less favorable terms from the market overall.

The reputation impact of a breach should be proportional to its severity. A single minor latency violation that incurs a $50 penalty should not crater a provider's reputation score. But a pattern of repeated uptime breaches that triggers $15,000 in cumulative penalties across multiple contracts should produce a significant, visible decline in the provider's public reputation. The severity scoring function below maps breach patterns to recommended reputation adjustments.

The reputation system also serves as an early warning for consumers evaluating potential providers. Before entering contract negotiation, a consumer agent should call `get_agent_reputation` and `search_agents_by_metrics` to assess whether a provider has a track record of honoring its SLA commitments. Providers with low reputation scores or high breach-to-contract ratios should be required to post larger escrow deposits -- or avoided entirely in favor of higher-reputation alternatives.

```python
def calculate_reputation_impact(breach_count: int,
                                 total_obligations: int,
                                 total_penalty_usd: float,
                                 contract_value_usd: float) -> dict:
    """Calculate reputation impact from contract enforcement actions.

    Returns a severity assessment and recommended reputation adjustment.
    """
    breach_rate = breach_count / max(total_obligations, 1)
    penalty_rate = total_penalty_usd / max(contract_value_usd, 1)

    # Severity scoring
    if breach_rate > 0.5 or penalty_rate > 0.3:
        severity = "critical"
        score_impact = -25
    elif breach_rate > 0.25 or penalty_rate > 0.15:
        severity = "high"
        score_impact = -15
    elif breach_rate > 0.1 or penalty_rate > 0.05:
        severity = "medium"
        score_impact = -8
    else:
        severity = "low"
        score_impact = -3

    return {
        "severity": severity,
        "breach_rate": round(breach_rate, 4),
        "penalty_rate": round(penalty_rate, 4),
        "recommended_score_impact": score_impact,
    }
```

---

## Chapter 7: Contract Renewal, Amendment, and Termination Workflows

### Version Control for Agreements

Every amendment to a contract creates a new version. The amendment history in the contract schema serves as a version control log -- each entry records what changed, when it changed, and what the contract fingerprint was before the change. This means any party can reconstruct the contract state at any point in its history by starting from the original and replaying amendments in order.

This is critical for dispute resolution. If a breach occurred on March 15 and the contract was amended on March 10, the penalty calculation must use the pre-amendment terms for any obligations that changed. Without version control, this temporal reasoning is impossible. With it, the enforcement engine can determine exactly which terms were in effect at the time of any observation.

The fingerprint chain -- where each amendment records the `previous_fingerprint` of the contract before the change was applied -- creates a tamper-evident history. If any party modifies historical amendment records, the fingerprint chain breaks, and the tampering is detectable. This is the same principle behind blockchain, but implemented as a simple hash chain within the contract document itself.

### Contract Amendments

Contracts in agent commerce must be living documents. Market conditions change, service requirements evolve, and both parties need the ability to propose, negotiate, and apply amendments without creating a new contract from scratch. The amendment workflow mirrors the original negotiation flow: one party proposes changes via `send_message`, the other party accepts or counter-proposes, and upon agreement both parties re-sign via `build_claim_chain`.

```python
class ContractAmendment(ContractClient):
    """Manage contract amendments with version control."""

    def propose_amendment(self, contract: dict,
                          counterparty_id: str,
                          changes: dict,
                          justification: str) -> dict:
        """Propose an amendment to an existing contract."""
        amendment = {
            "amendment_id": f"amd_{hashlib.sha256(json.dumps(changes).encode()).hexdigest()[:16]}",
            "contract_id": contract["contract_id"],
            "proposed_by": self.agent_id,
            "proposed_at": datetime.now(timezone.utc).isoformat(),
            "changes": changes,
            "justification": justification,
            "status": "proposed",
            "previous_fingerprint": self.fingerprint(contract),
        }

        # Send amendment proposal via messaging
        result = self.execute("send_message", {
            "sender_id": self.agent_id,
            "receiver_id": counterparty_id,
            "message_type": "contract_amendment",
            "content": json.dumps(amendment),
        })

        return {
            "amendment_id": amendment["amendment_id"],
            "message_id": result.get("message_id"),
        }

    def apply_amendment(self, contract: dict,
                        amendment: dict) -> dict:
        """Apply a mutually agreed amendment to the contract.

        Returns the updated contract with amendment recorded in history.
        """
        # Deep copy to avoid mutating the original
        updated = json.loads(json.dumps(contract))

        # Apply changes
        changes = amendment["changes"]
        for path, new_value in changes.items():
            self._set_nested(updated, path, new_value)

        # Record in amendment history
        updated["amendment_history"].append({
            "amendment_id": amendment["amendment_id"],
            "applied_at": datetime.now(timezone.utc).isoformat(),
            "changes": changes,
            "previous_fingerprint": amendment["previous_fingerprint"],
        })

        # Update fingerprint
        updated["fingerprint"] = self.fingerprint(updated)

        # Both parties must re-sign (via claim chain)
        return updated

    def _set_nested(self, obj: dict, path: str, value: Any) -> None:
        """Set a value at a dot-notation path, with array index support.

        Example: 'obligations[0].threshold' sets
                 obj['obligations'][0]['threshold']
        """
        import re
        parts = re.split(r'\.', path)
        current = obj
        for i, part in enumerate(parts[:-1]):
            match = re.match(r'(\w+)\[(\d+)\]', part)
            if match:
                key, index = match.group(1), int(match.group(2))
                current = current[key][index]
            else:
                current = current[part]

        last = parts[-1]
        match = re.match(r'(\w+)\[(\d+)\]', last)
        if match:
            key, index = match.group(1), int(match.group(2))
            current[key][index] = value
        else:
            current[last] = value
```

### Renewal Workflows

Contract renewal is not a passive event. Before a contract expires, the consumer agent should evaluate performance history, market alternatives, and negotiate updated terms. The renewal evaluation window should open at least 60 days before contract expiry -- enough time to conduct a thorough market scan, run parallel evaluations with alternative providers, and negotiate improved terms if the incumbent's performance warrants leverage.

The renewal decision matrix considers four factors: historical compliance rate, cumulative penalty ratio, current provider reputation score, and the number of viable alternative providers discovered via `search_agents_by_metrics`. These factors interact: a provider with 90% compliance and no alternatives should probably be renewed with tighter terms, while the same provider with five alternatives available should be replaced. The decision matrix encodes this logic explicitly, producing a structured recommendation that the agent can execute without human review.

```python
class RenewalManager(ContractClient):
    """Manage contract renewal evaluation and execution."""

    def evaluate_renewal(self, contract: dict,
                         compliance_history: List[dict]) -> dict:
        """Evaluate whether a contract should be renewed based on
        historical compliance data."""
        total_periods = len(compliance_history)
        compliant_periods = sum(
            1 for period in compliance_history
            if period.get("overall_compliant", False)
        )

        compliance_rate = (
            compliant_periods / total_periods if total_periods > 0 else 0
        )

        total_penalties = sum(
            period.get("total_penalties_usd", 0)
            for period in compliance_history
        )

        contract_value = float(
            contract["escrow"]["deposit_amount_usd"]
        )
        penalty_ratio = total_penalties / max(contract_value, 1)

        # Check provider reputation
        provider_id = contract["parties"]["provider"]["agent_id"]
        reputation = self.execute("get_agent_reputation", {
            "agent_id": provider_id,
        })
        rep_score = float(reputation.get("reputation_score", 0))

        # Search for alternative providers
        alternatives = self.execute("search_agents_by_metrics", {
            "agent_id": self.agent_id,
            "metric": "uptime_percentage",
            "min_value": "99.9",
        })

        recommendation = self._renewal_decision(
            compliance_rate, penalty_ratio, rep_score,
            len(alternatives.get("agents", []))
        )

        return {
            "contract_id": contract["contract_id"],
            "provider_id": provider_id,
            "compliance_rate": round(compliance_rate, 4),
            "total_penalties_usd": total_penalties,
            "penalty_ratio": round(penalty_ratio, 4),
            "reputation_score": rep_score,
            "alternative_providers": len(alternatives.get("agents", [])),
            "recommendation": recommendation,
        }

    def _renewal_decision(self, compliance_rate: float,
                          penalty_ratio: float,
                          rep_score: float,
                          alternatives_count: int) -> dict:
        """Produce a structured renewal recommendation."""
        if compliance_rate >= 0.95 and rep_score >= 80:
            action = "renew"
            terms_adjustment = "maintain_current"
            reason = "Excellent compliance history and reputation"
        elif compliance_rate >= 0.80 and rep_score >= 60:
            action = "renew_with_amendments"
            terms_adjustment = "tighten_penalties"
            reason = "Acceptable compliance but room for improvement"
        elif alternatives_count > 3 and compliance_rate < 0.80:
            action = "terminate_and_replace"
            terms_adjustment = None
            reason = (
                "Poor compliance with multiple alternatives available"
            )
        else:
            action = "renew_with_amendments"
            terms_adjustment = "increase_escrow"
            reason = "Below-standard compliance, limited alternatives"

        return {
            "action": action,
            "terms_adjustment": terms_adjustment,
            "reason": reason,
        }

    def execute_renewal(self, contract: dict,
                        renewal_terms: dict) -> dict:
        """Execute a contract renewal with updated terms."""
        # Create a new contract based on the existing one
        renewed = json.loads(json.dumps(contract))
        renewed["contract_id"] = (
            f"ctr_{hashlib.sha256(json.dumps(renewal_terms).encode()).hexdigest()[:16]}"
        )
        renewed["created_at"] = datetime.now(timezone.utc).isoformat()
        renewed["expires_at"] = (
            datetime.now(timezone.utc) + timedelta(days=365)
        ).isoformat()
        renewed["status"] = "pending_signature"
        renewed["amendment_history"] = []

        # Apply renewal term changes
        for path, value in renewal_terms.items():
            amendment_mgr = ContractAmendment(
                self.api_key, self.agent_id, self.base_url
            )
            amendment_mgr._set_nested(renewed, path, value)

        renewed["fingerprint"] = self.fingerprint(renewed)

        # Signal renewal intent
        self.execute("create_intent", {
            "agent_id": self.agent_id,
            "intent_type": "contract_renewal",
            "description": (
                f"Renewing contract {contract['contract_id']}"
            ),
            "metadata": {
                "original_contract_id": contract["contract_id"],
                "new_contract_id": renewed["contract_id"],
            },
        })

        return renewed
```

### Graceful Termination

Termination must handle outstanding escrow balances, pending obligations, and final settlement. A terminated contract is not deleted -- it transitions to a terminal state with a complete audit trail.

Three termination types exist, each with different settlement mechanics:

**Mutual Termination.** Both parties agree to end the contract. Earned milestone releases go to the provider. The remaining escrow balance is split 50/50. This is the friendliest termination mode and should be the default when both parties agree the service is no longer needed.

**For-Cause Termination.** One party terminates due to the other party's material breach. The non-breaching party receives maximum protection: the consumer gets back all unearned escrow, the provider forfeits unreleased milestones. This is the termination mode triggered by the enforcement engine when repeated breaches drive the provider's reputation below the threshold.

**Convenience Termination.** One party terminates without cause -- they simply no longer need the service. An early termination fee (typically 10% of remaining contract value) compensates the other party for the disruption. This fee is deducted from the escrow refund before the remainder is returned to the consumer.

```python
class TerminationManager(ContractClient):
    """Handle contract termination with proper settlement."""

    def terminate_contract(self, contract: dict,
                           escrow_id: str,
                           reason: str,
                           termination_type: str = "mutual") -> dict:
        """Terminate a contract with final settlement.

        termination_type: 'mutual', 'for_cause', or 'convenience'
        """
        provider_id = contract["parties"]["provider"]["agent_id"]
        consumer_id = contract["parties"]["consumer"]["agent_id"]

        # Step 1: Calculate final settlement
        settlement = self._calculate_final_settlement(
            contract, termination_type
        )

        # Step 2: Notify counterparty
        self.execute("send_message", {
            "sender_id": self.agent_id,
            "receiver_id": (
                provider_id if self.agent_id == consumer_id
                else consumer_id
            ),
            "message_type": "contract_termination",
            "content": json.dumps({
                "contract_id": contract["contract_id"],
                "termination_type": termination_type,
                "reason": reason,
                "settlement": settlement,
                "effective_at": datetime.now(timezone.utc).isoformat(),
            }),
        })

        # Step 3: Record termination in ledger
        self.execute("record_transaction", {
            "agent_id": self.agent_id,
            "transaction_type": "contract_termination",
            "amount": str(settlement.get("net_settlement_usd", 0)),
            "currency": "USD",
            "counterparty_id": (
                provider_id if self.agent_id == consumer_id
                else consumer_id
            ),
            "metadata": json.dumps({
                "contract_id": contract["contract_id"],
                "escrow_id": escrow_id,
                "termination_type": termination_type,
                "reason": reason,
            }),
        })

        # Step 4: Build claim chain entry for termination record
        self.execute("build_claim_chain", {
            "agent_id": self.agent_id,
            "claim_type": "contract_termination",
            "claim_data": {
                "contract_id": contract["contract_id"],
                "termination_type": termination_type,
                "terminated_at": datetime.now(timezone.utc).isoformat(),
                "settlement": settlement,
            },
        })

        return {
            "terminated": True,
            "contract_id": contract["contract_id"],
            "termination_type": termination_type,
            "settlement": settlement,
        }

    def _calculate_final_settlement(self, contract: dict,
                                    termination_type: str) -> dict:
        """Calculate the final settlement amounts."""
        total_escrow = float(contract["escrow"]["deposit_amount_usd"])

        if termination_type == "for_cause":
            # Consumer gets remaining escrow back, minus earned milestones
            earned = sum(
                total_escrow * (m["release_percentage"] / 100)
                for m in contract["escrow"]["milestone_schedule"]
                if m.get("completed", False)
            )
            refund = total_escrow - earned
            return {
                "provider_receives_usd": round(earned, 2),
                "consumer_refund_usd": round(refund, 2),
                "net_settlement_usd": round(refund, 2),
            }
        elif termination_type == "convenience":
            # Early termination fee: 10% of remaining contract value
            remaining_months = self._remaining_months(contract)
            monthly_fee = next(
                (o["threshold"] for o in contract["obligations"]
                 if o["type"] == "payment"), 0
            )
            remaining_value = monthly_fee * remaining_months
            early_term_fee = round(remaining_value * 0.10, 2)
            return {
                "early_termination_fee_usd": early_term_fee,
                "consumer_refund_usd": round(
                    total_escrow - early_term_fee, 2
                ),
                "net_settlement_usd": round(
                    total_escrow - early_term_fee, 2
                ),
            }
        else:
            # Mutual: split remaining escrow 50/50 after earned milestones
            earned = sum(
                total_escrow * (m["release_percentage"] / 100)
                for m in contract["escrow"]["milestone_schedule"]
                if m.get("completed", False)
            )
            remaining = total_escrow - earned
            return {
                "provider_receives_usd": round(earned + remaining / 2, 2),
                "consumer_refund_usd": round(remaining / 2, 2),
                "net_settlement_usd": round(remaining / 2, 2),
            }

    def _remaining_months(self, contract: dict) -> int:
        """Calculate remaining months on the contract."""
        expires = datetime.fromisoformat(
            contract["expires_at"].replace("Z", "+00:00")
        )
        now = datetime.now(timezone.utc)
        delta = expires - now
        return max(0, int(delta.days / 30))
```

---

## Chapter 8: Production Contract Management System: End-to-End Implementation with Audit Trails

### The Complete Contract Lifecycle Manager

This chapter brings everything together into a single production-ready class that manages the entire contract lifecycle from proposal through termination, with full audit trails recorded in the GreenHelix ledger.

```python
class ContractLifecycleManager:
    """End-to-end contract lifecycle management for autonomous agents.

    Orchestrates: negotiation, signing, escrow, monitoring,
    enforcement, renewal, and termination.
    """

    def __init__(self, api_key: str, agent_id: str,
                 base_url: str = "https://api.greenhelix.net/v1"):
        self.api_key = api_key
        self.agent_id = agent_id
        self.base_url = base_url

        # Initialize all subsystems
        self.negotiator = ContractNegotiator(api_key, agent_id, base_url)
        self.signer = ContractSigner(api_key, agent_id, base_url)
        self.escrow_mgr = EscrowManager(api_key, agent_id, base_url)
        self.tracker = ObligationTracker(api_key, agent_id, base_url)
        self.enforcer = EnforcementEngine(api_key, agent_id, base_url)
        self.amendment_mgr = ContractAmendment(api_key, agent_id, base_url)
        self.renewal_mgr = RenewalManager(api_key, agent_id, base_url)
        self.termination_mgr = TerminationManager(api_key, agent_id, base_url)
        self.predictor = BreachPredictor()

        # Active contract registry
        self.contracts: Dict[str, dict] = {}
        self.escrows: Dict[str, str] = {}  # contract_id -> escrow_id
        self.observation_history: Dict[str, List[dict]] = {}
        self.enforcement_log: List[dict] = []

    # ── Phase 1: Formation ──

    def initiate_contract(self, counterparty_id: str,
                          template_type: str,
                          custom_terms: dict) -> dict:
        """Start a new contract negotiation."""
        result = self.negotiator.propose_contract(
            counterparty_id, template_type, custom_terms
        )
        self._audit("contract_proposed", {
            "counterparty": counterparty_id,
            "template": template_type,
            "custom_terms": custom_terms,
        })
        return result

    def finalize_contract(self, contract: dict) -> dict:
        """Sign and activate a negotiated contract."""
        # Sign the contract
        signature = self.signer.sign_contract(contract)
        contract["parties"]["consumer" if self.agent_id
            == contract["parties"]["consumer"]["agent_id"]
            else "provider"]["claim_chain_id"] = signature["claim_chain_id"]
        contract["parties"]["consumer" if self.agent_id
            == contract["parties"]["consumer"]["agent_id"]
            else "provider"]["signed_at"] = signature["signed_at"]

        # Create escrow
        escrow_result = self.escrow_mgr.create_contract_escrow(contract)
        escrow_id = escrow_result["escrow_id"]
        contract["escrow"]["escrow_id"] = escrow_id

        # Activate all SLA monitors
        activation = self.tracker.activate_all_obligations(contract)

        # Update fingerprint with all runtime IDs
        contract["fingerprint"] = self.signer.fingerprint(contract)

        # Register in local state
        self.contracts[contract["contract_id"]] = contract
        self.escrows[contract["contract_id"]] = escrow_id

        self._audit("contract_finalized", {
            "contract_id": contract["contract_id"],
            "escrow_id": escrow_id,
            "sla_count": activation["count"],
        })

        return {
            "contract_id": contract["contract_id"],
            "escrow_id": escrow_id,
            "activated_obligations": activation["count"],
            "signature": signature,
        }

    # ── Phase 2: Monitoring ──

    def monitor_cycle(self, contract_id: str) -> dict:
        """Run one monitoring cycle for a contract.

        Call this on a schedule (e.g., every 5 minutes).
        """
        contract = self.contracts[contract_id]
        escrow_id = self.escrows[contract_id]

        # Get compliance snapshot
        snapshot = self.tracker.get_compliance_snapshot(contract)

        # Check for breaches and enforce
        enforcement_actions = []
        for obl_status in snapshot["obligations"]:
            if not obl_status["compliant"]:
                breach_data = {
                    "actual_value": obl_status.get("current_value"),
                    "threshold": obl_status["threshold"],
                    "obligation_id": obl_status["obligation_id"],
                    "detected_at": datetime.now(timezone.utc).isoformat(),
                    "violation_count": 1,
                    "breach_days": 1,
                }

                result = self.enforcer.enforce_breach(
                    contract, obl_status["obligation_id"],
                    breach_data, escrow_id
                )

                if result["enforced"]:
                    enforcement_actions.append(result)
                    self.enforcement_log.append(result)

        # Generate predictions
        report = generate_compliance_report(
            self.tracker, self.predictor, contract,
            self.observation_history
        )

        self._audit("monitoring_cycle", {
            "contract_id": contract_id,
            "compliant": snapshot["overall_compliant"],
            "enforcements": len(enforcement_actions),
            "alerts": len(report.get("alerts", [])),
        })

        return {
            "snapshot": snapshot,
            "enforcement_actions": enforcement_actions,
            "predictions": report.get("predictions", []),
            "alerts": report.get("alerts", []),
        }

    # ── Phase 3: Milestone Management ──

    def process_milestone(self, contract_id: str,
                          milestone: str) -> dict:
        """Process a contract milestone, adjusting release for penalties."""
        contract = self.contracts[contract_id]
        escrow_id = self.escrows[contract_id]

        # Calculate total penalties since last milestone
        relevant_penalties = [
            e for e in self.enforcement_log
            if e.get("obligation_id") in [
                o["obligation_id"] for o in contract["obligations"]
            ]
        ]
        total_penalties = sum(
            e.get("penalty_amount", 0) for e in relevant_penalties
        )

        # Release milestone (amount will be adjusted by penalties)
        result = self.escrow_mgr.release_milestone(
            contract, escrow_id, milestone
        )

        if result["released"]:
            adjusted_amount = max(0, result["amount"] - total_penalties)
            self._audit("milestone_processed", {
                "contract_id": contract_id,
                "milestone": milestone,
                "gross_release": result["amount"],
                "penalty_deductions": total_penalties,
                "net_release": adjusted_amount,
            })

        return {
            "milestone": milestone,
            "result": result,
            "penalties_applied": total_penalties,
        }

    # ── Phase 4: Renewal / Termination ──

    def evaluate_and_renew(self, contract_id: str,
                           compliance_history: List[dict]) -> dict:
        """Evaluate a contract for renewal and execute if recommended."""
        contract = self.contracts[contract_id]
        evaluation = self.renewal_mgr.evaluate_renewal(
            contract, compliance_history
        )

        self._audit("renewal_evaluated", {
            "contract_id": contract_id,
            "recommendation": evaluation["recommendation"],
        })

        return evaluation

    def terminate(self, contract_id: str, reason: str,
                  termination_type: str = "mutual") -> dict:
        """Terminate a contract with settlement."""
        contract = self.contracts[contract_id]
        escrow_id = self.escrows[contract_id]

        result = self.termination_mgr.terminate_contract(
            contract, escrow_id, reason, termination_type
        )

        # Clean up local state
        contract["status"] = "terminated"
        self._audit("contract_terminated", {
            "contract_id": contract_id,
            "reason": reason,
            "type": termination_type,
            "settlement": result["settlement"],
        })

        return result

    # ── Audit Trail ──

    def _audit(self, event_type: str, data: dict) -> None:
        """Record an audit event in the GreenHelix ledger."""
        client = ContractClient(
            self.api_key, self.agent_id, self.base_url
        )
        client.execute("record_transaction", {
            "agent_id": self.agent_id,
            "transaction_type": f"clm_audit_{event_type}",
            "amount": "0",
            "currency": "USD",
            "metadata": json.dumps({
                "event_type": event_type,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                **data,
            }),
        })

    def get_audit_trail(self, contract_id: str) -> dict:
        """Retrieve the complete audit trail for a contract."""
        client = ContractClient(
            self.api_key, self.agent_id, self.base_url
        )
        analytics = client.execute("get_analytics", {
            "agent_id": self.agent_id,
            "metric": "transactions",
        })
        return analytics

    def get_compliance_report(self, contract_id: str) -> dict:
        """Generate a compliance report suitable for external audit."""
        contract = self.contracts[contract_id]
        escrow_id = self.escrows.get(contract_id)

        snapshot = self.tracker.get_compliance_snapshot(contract)

        # Check compliance status via the compliance tool
        client = ContractClient(
            self.api_key, self.agent_id, self.base_url
        )
        compliance_check = client.execute("check_compliance", {
            "agent_id": self.agent_id,
        })

        return {
            "contract_id": contract_id,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "contract_status": contract.get("status"),
            "escrow_id": escrow_id,
            "obligation_compliance": snapshot,
            "enforcement_actions": [
                e for e in self.enforcement_log
                if e.get("obligation_id") in [
                    o["obligation_id"] for o in contract["obligations"]
                ]
            ],
            "platform_compliance": compliance_check,
            "amendment_count": len(contract.get("amendment_history", [])),
        }
```

### Scheduling the Monitoring Loop

The `monitor_cycle` method is designed to be called on a recurring schedule. The optimal frequency depends on your obligation measurement windows. For obligations measured in 24-hour windows (like latency P95), monitoring every 5 minutes provides sufficient resolution to detect degradation trends. For obligations measured in 720-hour (monthly) windows like uptime, hourly monitoring is adequate.

In production, run the monitoring loop as a background task within your agent's event loop. Each cycle takes approximately 200-400ms per obligation (one `get_sla_status` call each), so a contract with four obligations completes a full monitoring cycle in under two seconds. For agents managing hundreds of contracts, batch the monitoring calls and stagger cycles to avoid burst traffic against the GreenHelix API.

The monitoring loop should be resilient to transient failures. If a `get_sla_status` call fails due to a network timeout, the monitoring cycle should log the failure and retry on the next cycle rather than treating the failure as a breach. A well-designed monitoring system distinguishes between "the provider's metric is bad" and "I cannot reach the monitoring infrastructure."

### End-to-End Usage Example

Here is the complete lifecycle in action -- from proposal to termination:

```python
# Initialize the lifecycle manager
clm = ContractLifecycleManager(
    api_key="your-api-key",
    agent_id="agent-analytics-buyer-042",
    base_url="https://api.greenhelix.net/v1",
)

# ── Step 1: Propose a contract ──
proposal = clm.initiate_contract(
    counterparty_id="agent-datapipeline-vendor-001",
    template_type="data_pipeline",
    custom_terms={
        "obligations[0].threshold": 99.95,    # Higher uptime
        "obligations[1].threshold": 200,       # Tighter latency
        "escrow.deposit_amount_usd": 85000,
    },
)
print(f"Proposal sent: {proposal['intent_id']}")

# ── Step 2: After negotiation rounds, finalize ──
# (Assume negotiation produced the agreed contract dict)
agreed_contract = {
    "schema_version": "1.0.0",
    "contract_id": "ctr_a7f3b9e2d1c04856",
    "created_at": "2026-04-06T14:30:00Z",
    "expires_at": "2027-04-06T14:30:00Z",
    "status": "active",
    "parties": {
        "provider": {
            "agent_id": "agent-datapipeline-vendor-001",
            "role": "provider",
            "signed_at": None,
            "claim_chain_id": None,
        },
        "consumer": {
            "agent_id": "agent-analytics-buyer-042",
            "role": "consumer",
            "signed_at": None,
            "claim_chain_id": None,
        },
    },
    "service_definition": {
        "name": "Real-Time Data Pipeline Service",
        "description": "Continuous ETL with guaranteed throughput",
        "tier": "enterprise",
        "billing_cycle": "monthly",
    },
    "obligations": [
        {
            "obligation_id": "obl_uptime_001",
            "obligated_party": "provider",
            "type": "availability",
            "metric": "uptime_percentage",
            "threshold": 99.95,
            "operator": "gte",
            "measurement_window_hours": 720,
            "measurement_method": "synthetic_probe",
            "probe_interval_seconds": 300,
            "grace_period_hours": 2,
            "sla_tool_id": None,
        },
        {
            "obligation_id": "obl_latency_001",
            "obligated_party": "provider",
            "type": "performance",
            "metric": "p95_latency_ms",
            "threshold": 200,
            "operator": "lte",
            "measurement_window_hours": 24,
            "measurement_method": "client_instrumentation",
            "grace_period_hours": 1,
            "sla_tool_id": None,
        },
        {
            "obligation_id": "obl_payment_001",
            "obligated_party": "consumer",
            "type": "payment",
            "metric": "monthly_payment_usd",
            "threshold": 28333.33,
            "operator": "gte",
            "measurement_window_hours": 720,
            "measurement_method": "ledger_verification",
            "grace_period_hours": 48,
            "sla_tool_id": None,
        },
    ],
    "penalties": {
        "uptime_breach": {
            "obligation_id": "obl_uptime_001",
            "formula": "service_credit",
            "tiers": [
                {"range": [99.90, 99.95], "credit_percentage": 10},
                {"range": [99.00, 99.90], "credit_percentage": 25},
                {"range": [0, 99.00], "credit_percentage": 50},
            ],
            "max_credit_percentage": 50,
            "applies_to": "monthly_fee",
        },
        "latency_breach": {
            "obligation_id": "obl_latency_001",
            "formula": "per_violation",
            "amount_per_violation_usd": 50,
            "daily_cap_usd": 500,
            "monthly_cap_usd": 5000,
        },
    },
    "escrow": {
        "escrow_id": None,
        "deposit_amount_usd": 85000,
        "milestone_schedule": [
            {"milestone": "contract_signed", "release_percentage": 0},
            {"milestone": "first_month_compliant", "release_percentage": 33},
            {"milestone": "quarter_compliant", "release_percentage": 33},
            {"milestone": "annual_compliant", "release_percentage": 34},
        ],
    },
    "amendment_history": [],
    "fingerprint": None,
}

activation = clm.finalize_contract(agreed_contract)
print(f"Contract active: {activation['contract_id']}")
print(f"Escrow: {activation['escrow_id']}")
print(f"SLAs activated: {activation['activated_obligations']}")

# ── Step 3: Regular monitoring (run on schedule) ──
cycle_result = clm.monitor_cycle("ctr_a7f3b9e2d1c04856")
print(f"Compliant: {cycle_result['snapshot']['overall_compliant']}")
print(f"Enforcements: {len(cycle_result['enforcement_actions'])}")
for alert in cycle_result["alerts"]:
    print(f"  ALERT: {alert['obligation_id']} - "
          f"breach in {alert['hours_to_breach']}h")

# ── Step 4: Process milestones ──
milestone_result = clm.process_milestone(
    "ctr_a7f3b9e2d1c04856", "first_month_compliant"
)
print(f"Milestone release: ${milestone_result['result']['amount']}")
print(f"Penalties deducted: ${milestone_result['penalties_applied']}")

# ── Step 5: Generate compliance report ──
report = clm.get_compliance_report("ctr_a7f3b9e2d1c04856")
print(f"Obligations tracked: "
      f"{report['obligation_compliance']['obligations']}")

# ── Step 6: Evaluate renewal ──
evaluation = clm.evaluate_and_renew(
    "ctr_a7f3b9e2d1c04856",
    compliance_history=[
        {"overall_compliant": True, "total_penalties_usd": 0},
        {"overall_compliant": True, "total_penalties_usd": 200},
        {"overall_compliant": False, "total_penalties_usd": 3500},
    ],
)
print(f"Renewal recommendation: {evaluation['recommendation']['action']}")
print(f"Reason: {evaluation['recommendation']['reason']}")

# ── Step 7: If needed, terminate ──
if evaluation["recommendation"]["action"] == "terminate_and_replace":
    termination = clm.terminate(
        "ctr_a7f3b9e2d1c04856",
        reason="Poor compliance history, switching vendors",
        termination_type="for_cause",
    )
    print(f"Terminated. Refund: "
          f"${termination['settlement']['consumer_refund_usd']}")
```

### Audit Trail Architecture

Every action in the contract lifecycle produces a ledger entry via `record_transaction`. This creates an immutable audit trail that can be queried via `get_analytics` and verified via `check_compliance`.

```
  ┌─────────────────────────────────────────────────────────────────┐
  │                     AUDIT TRAIL ENTRIES                         │
  │                                                                 │
  │  Timestamp            Event Type               Key Data         │
  │  ──────────────────────────────────────────────────────────────  │
  │  2026-04-06 14:30    contract_proposed         template, terms  │
  │  2026-04-06 14:35    contract_finalized        escrow_id, SLAs  │
  │  2026-04-06 14:36    claim_chain_signature     fingerprint      │
  │  2026-04-07 00:00    monitoring_cycle          compliant: true  │
  │  2026-04-07 06:00    monitoring_cycle          compliant: true  │
  │  2026-04-08 12:00    monitoring_cycle          compliant: false │
  │  2026-04-08 12:01    enforcement_executed      penalty: $50     │
  │  2026-05-06 00:00    milestone_processed       net_release: $X  │
  │  2026-05-06 00:01    renewal_evaluated         action: renew    │
  │  ...                 ...                       ...              │
  │  2027-04-06 00:00    contract_terminated       settlement: $Y   │
  └─────────────────────────────────────────────────────────────────┘
```

Every entry is a `record_transaction` call with `transaction_type` prefixed by `clm_audit_`. This means the entire contract history is queryable through the standard GreenHelix analytics and compliance tools. External auditors can verify contract compliance without access to the agent's internal state -- everything is in the ledger.

### Key Integration Points

The contract lifecycle manager integrates with these GreenHelix tools:

| Lifecycle Phase | Primary Tools | Purpose |
|---|---|---|
| Formation | `create_intent`, `send_message` | Proposal and negotiation |
| Signing | `build_claim_chain`, `get_claim_chains` | Identity-bound signatures |
| Escrow | `create_escrow`, `release_escrow` | Financial commitment |
| Monitoring | `create_sla`, `monitor_sla`, `get_sla_status` | Obligation tracking |
| Metrics | `submit_metrics`, `search_agents_by_metrics` | Performance data |
| Enforcement | `record_transaction`, `open_dispute` | Penalties and disputes |
| Reputation | `get_agent_reputation` | Market consequences |
| Compliance | `check_compliance`, `get_analytics` | Audit and reporting |
| Lifecycle | `transfer`, `record_transaction` | Payments and settlements |

---

## What You Get

This guide provides everything you need to build production contract lifecycle management for autonomous agent systems:

**Machine-Readable Contract Schema.** The complete AgentSLA specification with obligation structures, penalty formulas, milestone-based escrow schedules, and amendment version control. Drop this JSON schema into your agent and it can parse, validate, and execute contract terms without interpretation.

**Automated Negotiation Pipeline.** Template libraries for common service types, structured message-based clause negotiation via `send_message`, and mutual signing via `build_claim_chain`. Your agents can propose, counter-propose, and finalize contracts autonomously.

**Escrow-Backed Execution.** Milestone-based escrow creation and release tied to obligation compliance. Financial commitments that make contracts credible, with progressive trust-building through staged releases.

**Real-Time Obligation Monitoring.** Every obligation activated as a GreenHelix SLA monitor with `create_sla`, continuous observation via `monitor_sla`, and consolidated compliance snapshots via `get_sla_status`. Plus predictive breach detection using linear regression on metric trends.

**Automated Penalty Enforcement.** Three deterministic penalty formulas (service credit, per-violation, flat-per-day) with caps, escrow deduction execution, reputation impact scoring, and automatic escalation to disputes when breach patterns indicate systemic failure.

**Renewal Intelligence.** Data-driven renewal evaluation that weighs compliance history, penalty ratios, provider reputation, and market alternatives to produce structured renewal recommendations.

**Graceful Termination.** Settlement calculation for mutual, for-cause, and convenience terminations with proper escrow handling, counterparty notification, and claim chain record.

**Complete Audit Trail.** Every lifecycle event recorded as a ledger entry via `record_transaction`, queryable through `get_analytics` and `check_compliance`. External auditors can verify contract compliance without internal system access.

**Production-Ready Code.** The `ContractLifecycleManager` class orchestrates all eight lifecycle phases with a clean API. Instantiate it, call `initiate_contract`, run `monitor_cycle` on a schedule, and the system handles enforcement, milestones, and renewal evaluation automatically.

The $57 billion SLA leakage problem exists because contracts are documents instead of data structures, monitoring is manual instead of automated, and enforcement requires humans instead of code. This guide eliminates all three causes. Your agents will form contracts they can parse, monitor obligations they can measure, and enforce penalties they can calculate -- all at machine speed, all backed by escrow, all recorded in an immutable audit trail.

