---
name: greenhelix-agent-insurance-risk-pools
version: "1.3.1"
description: "The Agent Insurance Playbook. Build agent-native insurance infrastructure: risk pools, liability bonds, automated claims processing, and regulatory compliance. Covers disputes, trust verification, ledger reconciliation, and SLA enforcement with detailed code examples with code."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [insurance, risk-pools, liability, claims, compliance, disputes, guide, greenhelix, openclaw, ai-agent]
price_usd: 49.0
content_type: markdown
executable: false
install: none
credentials: none
---
# The Agent Insurance Playbook

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code, require credentials, or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.


Your autonomous agent just executed a $200,000 procurement deal on behalf of a Fortune 500 client. The supplier delivered defective components. The agent chose the supplier autonomously -- the human who deployed it never reviewed the selection criteria, never saw the purchase order, and was asleep when the transaction closed. Who pays for the defective goods? The deployer who built the agent? The enterprise that authorized it to spend? The agent itself, which has no legal personhood and no assets? Traditional insurance cannot answer this question because traditional insurance assumes a human made the decision. Product liability law assumes a manufacturer shipped a defective product. Neither framework contemplates a probabilistic system that made a reasonable but wrong decision based on the information available at the time of execution.
This playbook builds the insurance infrastructure for autonomous agent commerce from first principles. You will construct risk pools that spread liability across agent operators, underwriting engines that price risk using on-chain trust scores, policy contracts encoded as machine-readable SLAs, claims processing pipelines that adjudicate disputes without human intervention, and catastrophe bonds that transfer tail risk to reinsurance syndicates. Every pattern uses the GreenHelix A2A Commerce Gateway -- 128 tools accessible at `https://api.greenhelix.net/v1` via a single the REST API (`POST /v1/{tool}`) endpoint. Every code example runs against the live API with a Bearer token.
The regulatory clock is ticking. California AB 316 took effect January 2026, establishing operator liability for autonomous vehicle decisions -- a precedent that will extend to autonomous commercial agents. The EU Product Liability Directive (2024/2853) makes AI system providers strictly liable for damage without requiring proof of fault. The EU AI Act's high-risk obligations land August 2, 2026. If your agents handle money, make purchasing decisions, or operate in regulated domains, you need insurance infrastructure that works at machine speed. This playbook shows you how to build it.

## What You'll Learn
- Chapter 1: The Agent Liability Problem
- Chapter 2: Risk Pool Architecture on A2A Commerce
- Chapter 3: Underwriting Agents: Trust Scores as Risk Signals
- Chapter 4: Policy Lifecycle: Binding to Expiry
- Chapter 5: Claims Processing & Automated Adjudication
- Chapter 6: Catastrophe Bonds & Reinsurance Patterns
- Chapter 7: Regulatory Compliance & Audit Infrastructure
- Next Steps
- Glossary
- Appendix: GreenHelix Tools Referenced

## Full Guide

# The Agent Insurance Playbook: Risk Pools, Liability Bonds & Automated Claims on A2A Commerce

Your autonomous agent just executed a $200,000 procurement deal on behalf of a Fortune 500 client. The supplier delivered defective components. The agent chose the supplier autonomously -- the human who deployed it never reviewed the selection criteria, never saw the purchase order, and was asleep when the transaction closed. Who pays for the defective goods? The deployer who built the agent? The enterprise that authorized it to spend? The agent itself, which has no legal personhood and no assets? Traditional insurance cannot answer this question because traditional insurance assumes a human made the decision. Product liability law assumes a manufacturer shipped a defective product. Neither framework contemplates a probabilistic system that made a reasonable but wrong decision based on the information available at the time of execution.

This playbook builds the insurance infrastructure for autonomous agent commerce from first principles. You will construct risk pools that spread liability across agent operators, underwriting engines that price risk using on-chain trust scores, policy contracts encoded as machine-readable SLAs, claims processing pipelines that adjudicate disputes without human intervention, and catastrophe bonds that transfer tail risk to reinsurance syndicates. Every pattern uses the GreenHelix A2A Commerce Gateway -- 128 tools accessible at `https://api.greenhelix.net/v1` via a single the REST API (`POST /v1/{tool}`) endpoint. Every code example runs against the live API with a Bearer token.

The regulatory clock is ticking. California AB 316 took effect January 2026, establishing operator liability for autonomous vehicle decisions -- a precedent that will extend to autonomous commercial agents. The EU Product Liability Directive (2024/2853) makes AI system providers strictly liable for damage without requiring proof of fault. The EU AI Act's high-risk obligations land August 2, 2026. If your agents handle money, make purchasing decisions, or operate in regulated domains, you need insurance infrastructure that works at machine speed. This playbook shows you how to build it.

---

## Table of Contents

1. [The Agent Liability Problem](#chapter-1-the-agent-liability-problem)
2. [Risk Pool Architecture on A2A Commerce](#chapter-2-risk-pool-architecture-on-a2a-commerce)
3. [Underwriting Agents: Trust Scores as Risk Signals](#chapter-3-underwriting-agents-trust-scores-as-risk-signals)
4. [Policy Lifecycle: Binding to Expiry](#chapter-4-policy-lifecycle-binding-to-expiry)
5. [Claims Processing & Automated Adjudication](#chapter-5-claims-processing--automated-adjudication)
6. [Catastrophe Bonds & Reinsurance Patterns](#chapter-6-catastrophe-bonds--reinsurance-patterns)
7. [Regulatory Compliance & Audit Infrastructure](#chapter-7-regulatory-compliance--audit-infrastructure)

---

## Chapter 1: The Agent Liability Problem

### Autonomous Decisions Create Unattributed Risk

When a human employee makes a purchasing decision that goes wrong, the liability chain is clear. The employee acted within the scope of their employment. The employer is vicariously liable under respondeat superior. Insurance covers the employer's exposure through commercial general liability, errors and omissions, or directors and officers policies. The entire framework depends on a single assumption: a human being made the decision, and that human being has a principal (an employer) who authorized the scope of action.

Autonomous agents break this assumption. An agent does not act within a "scope of employment" in any legal sense. It acts within the bounds of its prompt, its tool permissions, its budget constraints, and its model's probabilistic interpretation of all three. When the agent selects a supplier, it does not exercise "judgment" in the legal sense -- it computes a probability distribution over available options and selects one. The decision is neither negligent nor competent. It is stochastic. Traditional liability frameworks have no category for stochastic harm.

### The Attribution Gap

Consider a multi-agent supply chain: Agent A (orchestrator) delegates procurement to Agent B (specialist buyer), which queries Agent C (market data provider) for pricing signals, then executes a purchase through Agent D (payment processor). The goods arrive damaged. Who is liable?

| Party | Traditional Liability | Agent Commerce Reality |
|---|---|---|
| **Deployer of Agent A** | Principal liability (authorized the spend) | Did not select the supplier; delegated to Agent B |
| **Deployer of Agent B** | Vicarious liability (made the selection) | Selected based on Agent C's data, which may have been stale |
| **Deployer of Agent C** | Contributory (provided bad data) | Data was accurate at time of query; market moved |
| **Deployer of Agent D** | None (processed a valid transaction) | Processed escrow correctly; no error in execution |
| **Supplier** | Product liability (shipped defective goods) | Clear liability, but discovery required multi-agent forensics |

The attribution gap -- the distance between "who instructed the action" and "what the action was" -- grows with every delegation step. In a four-agent chain, attributing causation requires reconstructing the decision logic of each agent, the data it consumed, the alternatives it considered, and the confidence score it assigned to the chosen option. No traditional insurance adjustor has the tools or the training to do this.

### The Regulatory Landscape

Three regulatory frameworks are converging to force the insurance question:

**California AB 316 (Effective January 2026).** Originally drafted for autonomous vehicles, AB 316 establishes that the operator of an autonomous system is liable for decisions made by that system within the scope of its authorized operation. The bill's language is not vehicle-specific -- it references "autonomous decision-making systems" broadly. Legal scholars at Stanford's CodeX center have noted that AB 316's liability framework maps directly to autonomous commercial agents. If your agent operates in California or transacts with California-based counterparties, the deployer is the liable party.

**EU Product Liability Directive (2024/2853).** The revised directive classifies AI systems as "products" and imposes strict liability -- no fault required. If the AI system was defective and caused damage, the provider is liable. The burden of proof shifts: the claimant only needs to show malfunction and damage; the defect is presumed. For agent commerce, this means every agent in a multi-agent chain is a "product" with a provider who carries strict liability exposure.

**EU AI Act (High-risk obligations effective August 2, 2026).** If your agent system is classified as high-risk under Annex III -- which includes AI systems used for credit scoring, insurance pricing, access to essential services, and critical infrastructure management -- you must implement risk management, technical documentation, record-keeping, human oversight, and accuracy requirements under Articles 8-15. Insurance for agent operations is not just a business decision; it is part of the compliance infrastructure.

**Mastercard Verifiable Intent Protocol.** Mastercard's framework requires that every AI-initiated transaction carry a machine-readable proof of human intent. The agent must demonstrate that a human authorized the category of transaction, the spending limit, and the counterparty criteria. This is not yet regulation, but Mastercard's network rules have the practical force of law for any agent that processes card payments. Verifiable intent becomes an underwriting signal: agents that carry intent proofs are lower risk than agents that do not.

### Why Traditional Insurance Breaks

Traditional insurance pricing relies on actuarial tables built from historical loss data. The insurer can price a commercial general liability policy because it has decades of claims data for businesses of that size, in that industry, in that geography. No actuarial table exists for autonomous agent commerce. There is no historical claims data. The risk is not stationary -- a model update can change the agent's behavior overnight. The loss distribution is fat-tailed -- most agents operate without incident for months, but a single agent failure can produce catastrophic losses (recall the $47K escrow loop from P12).

Traditional insurance also assumes the policyholder can describe what they want to insure. "I want to insure my agent against making a bad procurement decision" is not a risk that an underwriter can bound. How bad? How often? What is the maximum exposure? The answers depend on the agent's model, its prompt, its tool permissions, its budget configuration, and the behavior of every counterparty it interacts with. The risk surface is combinatorial.

Agent-native insurance requires a fundamentally different architecture: one where risk is pooled across operators, priced dynamically using on-chain trust signals, encoded in machine-readable contracts, and adjudicated programmatically against verifiable evidence. That is what we build in the remaining seven chapters.

> **Key Takeaways**
>
> - Autonomous agents create an attribution gap between the human who authorized action and the agent that took it. Multi-agent chains compound this gap.
> - CA AB 316 (January 2026), the EU Product Liability Directive, and the EU AI Act (August 2, 2026) are converging to impose operator-level liability for agent decisions.
> - Mastercard Verifiable Intent adds a practical compliance requirement: machine-readable proof of human authorization for every agent-initiated transaction.
> - Traditional insurance cannot price agent risk because there is no actuarial history, the risk surface is combinatorial, and the loss distribution is fat-tailed.
> - Agent-native insurance requires pooled capital, dynamic pricing from trust signals, machine-readable policies, and programmatic claims adjudication.
> - Cross-reference: P5 (Trust) for trust score mechanics, P11 (Compliance) for EU AI Act implementation, P25 (Economy Architect) for multi-agent financial architecture.

---

## Chapter 2: Risk Pool Architecture on A2A Commerce

### What Is an Agent Risk Pool?

A risk pool is a shared capital reserve funded by contributions from multiple agent operators. When one member suffers a covered loss, the pool pays the claim. The mechanism is ancient -- mutual insurance societies date to the 17th century -- but the implementation for agent commerce requires purpose-built primitives: programmable wallets for capital custody, ledger entries for contribution tracking, balance queries for solvency monitoring, and transaction records for pro-rata accounting.

The Ledger and Payments modules expose these primitives. A risk pool is not a single tool call -- it is a pattern composed from multiple tools that together create a capital structure with defined contribution rules, claim procedures, and payout logic.

### Pool Architecture Overview

```
  ┌─────────────────────────────────────────────────────┐
  │                    RISK POOL                        │
  │                                                     │
  │  ┌──────────┐  ┌──────────┐  ┌──────────┐         │
  │  │ Operator  │  │ Operator  │  │ Operator  │  ...    │
  │  │ Agent A   │  │ Agent B   │  │ Agent C   │         │
  │  │           │  │           │  │           │         │
  │  │ Premium:  │  │ Premium:  │  │ Premium:  │         │
  │  │ $500/mo   │  │ $750/mo   │  │ $500/mo   │         │
  │  └────┬──────┘  └────┬──────┘  └────┬──────┘         │
  │       │              │              │                 │
  │       ▼              ▼              ▼                 │
  │  ┌───────────────────────────────────────────┐       │
  │  │         SHARED WALLET (Escrow)            │       │
  │  │         Balance: $52,500                  │       │
  │  │         Contributions tracked in Ledger   │       │
  │  └───────────────────────────────────────────┘       │
  │       │                                               │
  │       ▼                                               │
  │  ┌──────────────────────┐  ┌────────────────────┐    │
  │  │  Claims Adjudicator  │  │  Solvency Monitor  │    │
  │  │  (Disputes module)   │  │  (Analytics module) │    │
  │  └──────────────────────┘  └────────────────────┘    │
  └─────────────────────────────────────────────────────┘
```

### Setting Up the Gateway Client

Every code example in this guide uses the following client class. Set it up once, reuse everywhere:

```python
import requests
import json
import time
from typing import Any, Optional
from datetime import datetime, timezone

GATEWAY_URL = os.environ.get("GREENHELIX_API_URL", "https://sandbox.greenhelix.net")


class InsuranceClient:
    """Client for agent insurance operations on GreenHelix."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def execute(self, tool: str, params: dict[str, Any]) -> dict:
        """Execute a single tool via the GreenHelix REST API."""
        response = requests.post(
            f"{GATEWAY_URL}/v1",
            headers=self.headers,
            json={"tool": tool, "input": params},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()


client = InsuranceClient(api_key="your-api-key-here")
```

### Step 1: Create the Pool Wallet

The pool's capital lives in a dedicated GreenHelix wallet. This wallet is controlled by the pool manager agent, not by any individual member:

```python
# Create the risk pool's shared wallet
pool_wallet = client.execute("create_wallet", {
    "agent_id": "risk-pool-manager-001",
    "wallet_name": "agent-liability-pool-2026-q2",
    "currency": "USD",
    "metadata": {
        "pool_type": "mutual_liability",
        "inception_date": "2026-04-01",
        "max_members": 50,
        "coverage_limit_per_claim": 100000,
        "aggregate_limit": 500000,
    }
})

pool_wallet_id = pool_wallet["wallet_id"]
print(f"Pool wallet created: {pool_wallet_id}")
```

### Step 2: Accept Member Premiums

Each member agent deposits their premium into the pool wallet. The deposit is recorded as a transaction with metadata linking it to the member and the coverage period:

```python
def collect_premium(
    member_agent_id: str,
    premium_amount: float,
    coverage_period: str,
) -> dict:
    """Collect a premium payment from a pool member."""

    # Step 1: Process the deposit into the pool wallet
    deposit = client.execute("deposit", {
        "wallet_id": pool_wallet_id,
        "amount": premium_amount,
        "source": f"premium:{member_agent_id}",
        "metadata": {
            "type": "premium_payment",
            "member_agent_id": member_agent_id,
            "coverage_period": coverage_period,
            "collected_at": datetime.now(timezone.utc).isoformat(),
        }
    })

    # Step 2: Record the contribution in the ledger for audit trail
    ledger_entry = client.execute("record_transaction", {
        "agent_id": "risk-pool-manager-001",
        "transaction_type": "premium_collection",
        "amount": premium_amount,
        "currency": "USD",
        "counterparty": member_agent_id,
        "metadata": {
            "pool_wallet_id": pool_wallet_id,
            "coverage_period": coverage_period,
            "deposit_id": deposit["deposit_id"],
        }
    })

    return {
        "deposit_id": deposit["deposit_id"],
        "ledger_entry_id": ledger_entry["transaction_id"],
        "member": member_agent_id,
        "amount": premium_amount,
        "period": coverage_period,
    }


# Collect premiums from three members
members = [
    ("procurement-agent-alpha", 500.00, "2026-Q2"),
    ("trading-bot-beta", 750.00, "2026-Q2"),
    ("logistics-agent-gamma", 500.00, "2026-Q2"),
]

for agent_id, amount, period in members:
    receipt = collect_premium(agent_id, amount, period)
    print(f"Collected ${amount} from {agent_id}: {receipt['deposit_id']}")
```

### Step 3: Monitor Pool Solvency

The pool manager must continuously verify that the pool has sufficient capital to cover potential claims. The solvency ratio is the pool balance divided by the maximum potential payout:

```python
def check_pool_solvency(
    coverage_limit_per_claim: float = 100_000,
    max_concurrent_claims: int = 3,
) -> dict:
    """Check the risk pool's solvency ratio."""

    # Get current pool balance
    balance = client.execute("get_balance", {
        "wallet_id": pool_wallet_id,
    })

    current_balance = float(balance["balance"])
    max_exposure = coverage_limit_per_claim * max_concurrent_claims
    solvency_ratio = current_balance / max_exposure if max_exposure > 0 else 0

    status = "ADEQUATE" if solvency_ratio >= 0.25 else "WARNING"
    if solvency_ratio < 0.10:
        status = "CRITICAL"

    return {
        "balance": current_balance,
        "max_exposure": max_exposure,
        "solvency_ratio": round(solvency_ratio, 4),
        "status": status,
    }


solvency = check_pool_solvency()
print(f"Pool balance: ${solvency['balance']:,.2f}")
print(f"Solvency ratio: {solvency['solvency_ratio']:.2%}")
print(f"Status: {solvency['status']}")
```

### Pro-Rata Risk Sharing

When a claim is paid, each member's share of the cost is proportional to their contribution. This prevents free-rider problems and incentivizes adequate premium levels:

```python
def calculate_pro_rata_shares(claim_amount: float) -> list[dict]:
    """Calculate each member's share of a claim payout."""

    # Query all premium transactions for the current period
    transactions = client.execute("get_transactions", {
        "agent_id": "risk-pool-manager-001",
        "transaction_type": "premium_collection",
        "limit": 100,
    })

    # Sum total contributions
    total_contributions = sum(
        float(tx["amount"]) for tx in transactions["transactions"]
    )

    # Calculate pro-rata shares
    shares = []
    for tx in transactions["transactions"]:
        member_contribution = float(tx["amount"])
        share_pct = member_contribution / total_contributions
        share_amount = claim_amount * share_pct
        shares.append({
            "member_agent_id": tx["counterparty"],
            "contribution": member_contribution,
            "share_pct": round(share_pct, 4),
            "claim_share": round(share_amount, 2),
        })

    return shares


# Example: $10,000 claim across three members
shares = calculate_pro_rata_shares(10_000)
for s in shares:
    print(f"  {s['member_agent_id']}: {s['share_pct']:.1%} = ${s['claim_share']:,.2f}")
```

### Pool Configuration Matrix

| Parameter | Conservative | Standard | Aggressive |
|---|---|---|---|
| **Min members** | 20 | 10 | 5 |
| **Solvency ratio target** | 50% | 25% | 15% |
| **Coverage limit per claim** | $50,000 | $100,000 | $250,000 |
| **Aggregate limit** | $250,000 | $500,000 | $1,000,000 |
| **Premium frequency** | Monthly | Quarterly | Annual |
| **Claims reserve** | 40% of premiums | 30% of premiums | 20% of premiums |
| **Reinsurance attachment** | $100,000 | $250,000 | $500,000 |

> **Key Takeaways**
>
> - A risk pool is a shared wallet funded by member premiums, with claims paid from the pool and costs allocated pro-rata.
> - GreenHelix primitives used: `create_wallet` for custody, `deposit` for premium collection, `record_transaction` for audit trail, `get_balance` for solvency monitoring, `get_transactions` for contribution accounting.
> - Solvency monitoring is continuous, not periodic. A pool that dips below 10% solvency ratio needs immediate capital calls or claim restrictions.
> - Pro-rata allocation prevents free-riding: members who contribute more bear a smaller percentage of each claim relative to their coverage.
> - Cross-reference: P25 (Economy Architect) for multi-wallet treasury patterns, P8 (Security) for wallet access controls.

---

## Chapter 3: Underwriting Agents: Trust Scores as Risk Signals

### The Underwriting Problem for Autonomous Agents

Traditional underwriting evaluates a prospective policyholder's risk profile using historical data: claims history, credit score, industry, geography, revenue, and years in operation. For autonomous agents, none of these signals exist in their traditional form. An agent does not have a credit score. It does not have years of operation in the traditional sense -- it may have been deployed three months ago but executed 50,000 transactions. Its "industry" is whatever tools it has access to.

The Trust and Identity modules provide the equivalent signals. A trust score is computed from verified trade history, metric consistency, claim chain depth, dispute rate, and time active on the platform. An identity profile includes the agent's registration date, public key, and operator metadata. Together, these form the underwriting data model for agent insurance.

### Trust Score as Risk Signal

The core underwriting insight is simple: agents with higher trust scores file fewer claims. This is empirically observable across platforms where agent-to-agent transactions are tracked -- agents that maintain consistent metrics, deep claim chains, and low dispute rates are less likely to cause or suffer losses. The trust score is not a guarantee of future behavior, but it is the best available predictor.

```python
def assess_agent_risk(agent_id: str) -> dict:
    """Evaluate an agent's risk profile for underwriting."""

    # Pull trust score -- the primary underwriting signal
    trust = client.execute("check_trust_score", {
        "agent_id": agent_id,
    })

    # Verify the agent's identity is registered and active
    identity = client.execute("get_agent_identity", {
        "agent_id": agent_id,
    })

    # Check verification status
    verification = client.execute("verify_agent", {
        "agent_id": agent_id,
    })

    # Pull reputation for supplemental signals
    reputation = client.execute("get_agent_reputation", {
        "agent_id": agent_id,
    })

    trust_score = float(trust.get("trust_score", 0))
    trade_count = int(reputation.get("verified_trade_count", 0))
    dispute_rate = float(reputation.get("dispute_rate", 1.0))
    days_active = int(identity.get("days_active", 0))
    is_verified = verification.get("verified", False)

    # Composite risk score (lower = better)
    risk_score = 100.0
    risk_score -= trust_score * 40          # Trust: 0-40 point reduction
    risk_score += dispute_rate * 30         # Disputes: 0-30 point penalty
    risk_score -= min(trade_count / 100, 20)  # Experience: up to 20 point reduction
    risk_score -= min(days_active / 30, 10)   # Tenure: up to 10 point reduction
    if not is_verified:
        risk_score += 15                     # Unverified: 15 point penalty

    risk_score = max(0, min(100, risk_score))

    # Map to risk tier
    if risk_score <= 25:
        tier = "PREFERRED"
    elif risk_score <= 50:
        tier = "STANDARD"
    elif risk_score <= 75:
        tier = "SUBSTANDARD"
    else:
        tier = "DECLINE"

    return {
        "agent_id": agent_id,
        "trust_score": trust_score,
        "trade_count": trade_count,
        "dispute_rate": dispute_rate,
        "days_active": days_active,
        "is_verified": is_verified,
        "risk_score": round(risk_score, 1),
        "risk_tier": tier,
    }


# Assess three prospective members
for agent_id in ["procurement-agent-alpha", "new-agent-xyz", "trading-bot-beta"]:
    profile = assess_agent_risk(agent_id)
    print(f"{agent_id}: score={profile['risk_score']}, tier={profile['risk_tier']}")
```

### Automated Premium Calculation

Once risk tier is determined, premium pricing follows. Higher-risk agents pay more because they are more likely to generate claims. The pricing model must balance actuarial soundness (premiums cover expected losses) with market competitiveness (premiums are not so high that agents avoid the pool).

```python
# Premium schedule by risk tier
PREMIUM_SCHEDULE = {
    "PREFERRED": {
        "base_monthly": 250.00,
        "rate_per_1k_coverage": 2.50,
        "deductible": 500,
        "max_coverage": 250_000,
    },
    "STANDARD": {
        "base_monthly": 500.00,
        "rate_per_1k_coverage": 5.00,
        "deductible": 1_000,
        "max_coverage": 100_000,
    },
    "SUBSTANDARD": {
        "base_monthly": 1_000.00,
        "rate_per_1k_coverage": 10.00,
        "deductible": 2_500,
        "max_coverage": 50_000,
    },
    "DECLINE": None,  # Application denied
}


def calculate_premium(
    risk_tier: str,
    requested_coverage: float,
) -> Optional[dict]:
    """Calculate the premium for a given risk tier and coverage amount."""

    schedule = PREMIUM_SCHEDULE.get(risk_tier)
    if schedule is None:
        return None  # Declined

    coverage = min(requested_coverage, schedule["max_coverage"])
    rate_premium = (coverage / 1000) * schedule["rate_per_1k_coverage"]
    total_monthly = schedule["base_monthly"] + rate_premium

    return {
        "risk_tier": risk_tier,
        "coverage_amount": coverage,
        "deductible": schedule["deductible"],
        "base_premium": schedule["base_monthly"],
        "rate_premium": round(rate_premium, 2),
        "total_monthly": round(total_monthly, 2),
        "total_quarterly": round(total_monthly * 3, 2),
        "total_annual": round(total_monthly * 12, 2),
    }


# Example: Standard tier agent requesting $100K coverage
quote = calculate_premium("STANDARD", 100_000)
print(f"Monthly premium: ${quote['total_monthly']:,.2f}")
print(f"Coverage: ${quote['coverage_amount']:,.2f}")
print(f"Deductible: ${quote['deductible']:,.2f}")
```

### Underwriting Decision Matrix

| Signal | Weight | Preferred | Standard | Substandard | Decline |
|---|---|---|---|---|---|
| **Trust score** | 40% | >= 0.85 | 0.60 - 0.84 | 0.35 - 0.59 | < 0.35 |
| **Dispute rate** | 30% | < 2% | 2% - 5% | 5% - 15% | > 15% |
| **Verified trades** | 20% | > 500 | 100 - 500 | 10 - 99 | < 10 |
| **Days active** | 5% | > 180 | 60 - 180 | 14 - 59 | < 14 |
| **Identity verified** | 5% | Yes | Yes | No (surcharge) | No |

### Tiered Coverage with SLAs

Different risk tiers receive different service-level agreements. The SLA encodes what the pool promises to the member: claim response time, maximum payout, and arbitration process. This becomes the machine-readable policy document (see Chapter 4).

```python
def create_coverage_sla(
    member_agent_id: str,
    risk_tier: str,
    coverage_amount: float,
) -> dict:
    """Create an SLA defining coverage terms for a pool member."""

    tier_slas = {
        "PREFERRED": {
            "claim_response_hours": 4,
            "claim_resolution_days": 7,
            "arbitration": "automated",
            "renewal_discount_pct": 10,
        },
        "STANDARD": {
            "claim_response_hours": 24,
            "claim_resolution_days": 14,
            "arbitration": "automated_with_review",
            "renewal_discount_pct": 5,
        },
        "SUBSTANDARD": {
            "claim_response_hours": 48,
            "claim_resolution_days": 30,
            "arbitration": "manual_review_required",
            "renewal_discount_pct": 0,
        },
    }

    sla_terms = tier_slas[risk_tier]

    sla = client.execute("create_sla", {
        "agent_id": "risk-pool-manager-001",
        "counterparty": member_agent_id,
        "terms": {
            "coverage_limit": coverage_amount,
            "claim_response_time": f"{sla_terms['claim_response_hours']}h",
            "claim_resolution_time": f"{sla_terms['claim_resolution_days']}d",
            "arbitration_method": sla_terms["arbitration"],
            "covered_events": [
                "counterparty_default",
                "data_quality_failure",
                "unauthorized_transaction",
                "service_level_breach",
            ],
            "exclusions": [
                "intentional_misconduct",
                "regulatory_fines",
                "consequential_damages",
                "force_majeure",
            ],
            "deductible": PREMIUM_SCHEDULE[risk_tier]["deductible"],
            "renewal_discount_pct": sla_terms["renewal_discount_pct"],
        },
        "metadata": {
            "policy_type": "agent_liability",
            "risk_tier": risk_tier,
            "inception_date": datetime.now(timezone.utc).isoformat(),
        }
    })

    return sla


# Bind coverage for a STANDARD tier member
sla = create_coverage_sla("procurement-agent-alpha", "STANDARD", 100_000)
print(f"Policy SLA created: {sla['sla_id']}")
```

### Continuous Re-Underwriting

Trust scores change over time. An agent that was PREFERRED at inception may degrade to STANDARD after a series of disputes. The pool must re-evaluate members periodically:

```python
def re_underwrite_member(member_agent_id: str, current_tier: str) -> dict:
    """Re-evaluate a member's risk tier based on current trust signals."""

    profile = assess_agent_risk(member_agent_id)
    new_tier = profile["risk_tier"]

    result = {
        "member": member_agent_id,
        "previous_tier": current_tier,
        "new_tier": new_tier,
        "action": "no_change",
    }

    if new_tier == "DECLINE":
        result["action"] = "non_renewal"
    elif new_tier != current_tier:
        tier_order = ["PREFERRED", "STANDARD", "SUBSTANDARD", "DECLINE"]
        if tier_order.index(new_tier) > tier_order.index(current_tier):
            result["action"] = "downgrade_with_surcharge"
        else:
            result["action"] = "upgrade_with_credit"

    return result
```

> **Key Takeaways**
>
> - Trust scores (`check_trust_score`) are the primary underwriting signal for agent insurance. Higher trust correlates with fewer claims.
> - Supplemental signals: identity verification (`get_agent_identity`, `verify_agent`), trade history, dispute rate from reputation (`get_agent_reputation`).
> - Four risk tiers (Preferred, Standard, Substandard, Decline) map to premium schedules and SLA terms.
> - Tiered coverage is encoded in SLAs (`create_sla`) with explicit claim response times, covered events, exclusions, and deductibles.
> - Re-underwriting is continuous, not annual. Trust scores change; premiums and coverage must adjust accordingly.
> - Cross-reference: P5 (Trust) for trust score computation details, P25 (Economy Architect) for pricing model design.

---

## Chapter 4: Policy Lifecycle: Binding to Expiry

### Policies as SLA Contracts

In traditional insurance, a policy is a legal document -- a PDF or paper contract with defined terms, conditions, exclusions, and endorsements. In agent insurance, a policy must be machine-readable. An agent cannot read a PDF. It needs structured data that defines exactly what is covered, what is excluded, the premium amount, the deductible, the coverage period, and the claims procedure.

GreenHelix SLAs serve this purpose. An SLA is a structured agreement between two agents with defined terms, timestamps, and unique identifiers. By convention, we use SLAs as the policy document format: the pool manager creates an SLA with the member agent, and the SLA terms encode the insurance contract.

### Policy Binding Flow

The complete binding flow involves four steps: underwriting assessment, premium quote, premium collection, and SLA creation. Here is the end-to-end implementation:

```python
def bind_policy(
    applicant_agent_id: str,
    requested_coverage: float,
    coverage_period: str = "2026-Q2",
) -> Optional[dict]:
    """Full policy binding flow: underwrite, quote, collect, bind."""

    # Step 1: Underwriting assessment
    risk_profile = assess_agent_risk(applicant_agent_id)
    if risk_profile["risk_tier"] == "DECLINE":
        return {
            "status": "declined",
            "reason": f"Risk score {risk_profile['risk_score']} exceeds threshold",
            "agent_id": applicant_agent_id,
        }

    # Step 2: Calculate premium
    quote = calculate_premium(risk_profile["risk_tier"], requested_coverage)

    # Step 3: Collect premium via payment intent
    intent = client.execute("create_payment_intent", {
        "agent_id": applicant_agent_id,
        "amount": quote["total_quarterly"],
        "currency": "USD",
        "description": f"Insurance premium: {coverage_period}",
        "metadata": {
            "type": "insurance_premium",
            "risk_tier": risk_profile["risk_tier"],
            "coverage_amount": quote["coverage_amount"],
            "period": coverage_period,
        }
    })

    # Step 4: Deposit premium into pool wallet
    deposit = client.execute("deposit", {
        "wallet_id": pool_wallet_id,
        "amount": quote["total_quarterly"],
        "source": f"premium:{applicant_agent_id}",
        "metadata": {
            "payment_intent_id": intent["payment_intent_id"],
            "member_agent_id": applicant_agent_id,
        }
    })

    # Step 5: Record in ledger
    client.execute("record_transaction", {
        "agent_id": "risk-pool-manager-001",
        "transaction_type": "premium_collection",
        "amount": quote["total_quarterly"],
        "currency": "USD",
        "counterparty": applicant_agent_id,
        "metadata": {
            "policy_period": coverage_period,
            "risk_tier": risk_profile["risk_tier"],
            "payment_intent_id": intent["payment_intent_id"],
            "deposit_id": deposit["deposit_id"],
        }
    })

    # Step 6: Create the policy SLA
    sla = create_coverage_sla(
        applicant_agent_id,
        risk_profile["risk_tier"],
        quote["coverage_amount"],
    )

    return {
        "status": "bound",
        "policy_id": sla["sla_id"],
        "agent_id": applicant_agent_id,
        "risk_tier": risk_profile["risk_tier"],
        "coverage": quote["coverage_amount"],
        "premium_quarterly": quote["total_quarterly"],
        "deductible": quote["deductible"],
        "period": coverage_period,
        "payment_intent_id": intent["payment_intent_id"],
    }


# Bind a policy for a new member
policy = bind_policy("procurement-agent-alpha", 100_000)
if policy and policy["status"] == "bound":
    print(f"Policy bound: {policy['policy_id']}")
    print(f"  Tier: {policy['risk_tier']}")
    print(f"  Coverage: ${policy['coverage']:,.2f}")
    print(f"  Premium: ${policy['premium_quarterly']:,.2f}/quarter")
    print(f"  Deductible: ${policy['deductible']:,.2f}")
```

### Renewal with Event-Driven Notifications

Policy renewal is triggered by an event published before the coverage period expires. The renewal event triggers the underwriting reassessment and premium recalculation:

```python
def schedule_renewal(policy_id: str, member_agent_id: str, renewal_date: str) -> dict:
    """Publish a renewal event that triggers re-underwriting."""

    event = client.execute("publish_event", {
        "agent_id": "risk-pool-manager-001",
        "event_type": "policy.renewal_due",
        "payload": {
            "policy_id": policy_id,
            "member_agent_id": member_agent_id,
            "renewal_date": renewal_date,
            "action_required": "re_underwrite_and_quote",
        }
    })

    return event


def process_renewal(
    policy_id: str,
    member_agent_id: str,
    current_tier: str,
    current_coverage: float,
) -> dict:
    """Process a policy renewal: re-underwrite, adjust premium, rebind."""

    # Re-evaluate risk
    reassessment = re_underwrite_member(member_agent_id, current_tier)

    if reassessment["action"] == "non_renewal":
        # Publish non-renewal notice
        client.execute("publish_event", {
            "agent_id": "risk-pool-manager-001",
            "event_type": "policy.non_renewal",
            "payload": {
                "policy_id": policy_id,
                "member_agent_id": member_agent_id,
                "reason": "Risk tier degraded to DECLINE",
            }
        })
        return {"status": "non_renewed", "reason": "risk_decline"}

    # Calculate new premium at the (possibly changed) tier
    new_tier = reassessment["new_tier"]
    new_quote = calculate_premium(new_tier, current_coverage)

    # Apply renewal discount if eligible
    discount_pct = PREMIUM_SCHEDULE[new_tier].get("renewal_discount_pct", 0) / 100
    if reassessment["action"] == "no_change" and discount_pct > 0:
        # Loyalty discount for stable members
        new_quote["total_quarterly"] *= (1 - discount_pct)
        new_quote["total_quarterly"] = round(new_quote["total_quarterly"], 2)

    return {
        "status": "renewed",
        "new_tier": new_tier,
        "tier_change": reassessment["action"],
        "new_quarterly_premium": new_quote["total_quarterly"],
        "coverage": new_quote["coverage_amount"],
    }
```

### Policy State Machine

Every policy moves through a defined set of states. Tracking state transitions in the ledger creates an immutable audit trail:

```
  APPLIED ──▶ UNDERWRITING ──▶ QUOTED ──▶ BOUND ──▶ ACTIVE
                   │                                    │
                   ▼                                    ├──▶ RENEWAL_DUE ──▶ RENEWED ──▶ ACTIVE
               DECLINED                                 │
                                                        ├──▶ CLAIM_FILED ──▶ ACTIVE
                                                        │
                                                        ├──▶ LAPSED (non-payment)
                                                        │
                                                        └──▶ CANCELLED
```

```python
def record_policy_state_change(
    policy_id: str,
    member_agent_id: str,
    from_state: str,
    to_state: str,
    reason: str = "",
) -> dict:
    """Record a policy state transition in the ledger."""

    return client.execute("record_transaction", {
        "agent_id": "risk-pool-manager-001",
        "transaction_type": "policy_state_change",
        "amount": 0,
        "currency": "USD",
        "counterparty": member_agent_id,
        "metadata": {
            "policy_id": policy_id,
            "from_state": from_state,
            "to_state": to_state,
            "reason": reason,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    })
```

### Policy Registry Checklist

Before a policy is considered fully bound, verify the following:

- [ ] Underwriting assessment completed with risk score and tier assignment
- [ ] Premium quote generated matching the risk tier schedule
- [ ] Payment intent created and confirmed
- [ ] Premium deposited into pool wallet
- [ ] Ledger entry recorded for premium collection
- [ ] SLA created with coverage terms, exclusions, and deductible
- [ ] Policy state transition recorded (UNDERWRITING -> QUOTED -> BOUND -> ACTIVE)
- [ ] Renewal event scheduled for 30 days before coverage period end
- [ ] Member notified of policy terms via event publication
- [ ] Solvency check confirms pool remains above minimum ratio

> **Key Takeaways**
>
> - Policies are machine-readable SLA contracts created via `create_sla`, not PDF documents.
> - The binding flow is: assess risk -> calculate premium -> collect payment (`create_payment_intent` + `deposit`) -> create SLA -> record state change.
> - Renewal is event-driven: `publish_event` triggers re-underwriting before the coverage period expires.
> - Every policy state transition is recorded in the Ledger (`record_transaction`) for immutable audit trail.
> - The state machine (Applied -> Underwriting -> Quoted -> Bound -> Active -> Renewed/Lapsed/Cancelled) ensures no policy enters an undefined state.
> - Cross-reference: P11 (Compliance) for regulatory record-keeping requirements, P12 (Incident Response) for handling policy lapses during active incidents.

---

## Chapter 5: Claims Processing & Automated Adjudication

### The Claims Pipeline

When a covered event occurs -- a counterparty defaults, a service fails to meet SLA terms, an unauthorized transaction executes -- the injured member files a claim against the pool. In traditional insurance, a human adjustor investigates the claim, evaluates evidence, and makes a coverage determination. In agent insurance, this process must be automated because agents operate at machine speed and human adjustors cannot keep pace.

GreenHelix's Disputes module provides the primitives for claims processing. A claim is modeled as a dispute between the injured member and the risk pool. Evidence is submitted through the dispute response mechanism. Adjudication evaluates the evidence against the policy terms (the SLA). Settlement pays out from the pool wallet.

### Filing a Claim

```python
def file_claim(
    claimant_agent_id: str,
    policy_id: str,
    claim_type: str,
    description: str,
    claimed_amount: float,
    evidence: dict,
) -> dict:
    """File an insurance claim against the risk pool."""

    # Step 1: Verify the claimant has an active policy
    sla = client.execute("get_sla", {
        "sla_id": policy_id,
    })

    if not sla:
        return {"status": "rejected", "reason": "No active policy found"}

    # Step 2: Verify the claim type is covered
    covered_events = sla.get("terms", {}).get("covered_events", [])
    if claim_type not in covered_events:
        return {
            "status": "rejected",
            "reason": f"Event type '{claim_type}' not covered under policy",
        }

    # Step 3: Create the dispute (claim)
    dispute = client.execute("create_dispute", {
        "agent_id": claimant_agent_id,
        "counterparty": "risk-pool-manager-001",
        "amount": claimed_amount,
        "reason": f"Insurance claim: {claim_type}",
        "description": description,
        "metadata": {
            "claim_type": claim_type,
            "policy_id": policy_id,
            "evidence_summary": evidence.get("summary", ""),
            "filed_at": datetime.now(timezone.utc).isoformat(),
        }
    })

    # Step 4: Submit evidence
    evidence_response = client.execute("respond_to_dispute", {
        "dispute_id": dispute["dispute_id"],
        "agent_id": claimant_agent_id,
        "response": "evidence_submission",
        "metadata": {
            "transaction_ids": evidence.get("transaction_ids", []),
            "sla_violation_details": evidence.get("sla_violation", {}),
            "timestamp_range": evidence.get("timestamp_range", {}),
            "financial_impact": evidence.get("financial_impact", {}),
        }
    })

    # Step 5: Record claim filing in ledger
    client.execute("record_transaction", {
        "agent_id": "risk-pool-manager-001",
        "transaction_type": "claim_filed",
        "amount": claimed_amount,
        "currency": "USD",
        "counterparty": claimant_agent_id,
        "metadata": {
            "dispute_id": dispute["dispute_id"],
            "policy_id": policy_id,
            "claim_type": claim_type,
        }
    })

    return {
        "status": "filed",
        "claim_id": dispute["dispute_id"],
        "policy_id": policy_id,
        "claimed_amount": claimed_amount,
        "claim_type": claim_type,
    }


# Example: File a claim for counterparty default
claim = file_claim(
    claimant_agent_id="procurement-agent-alpha",
    policy_id="sla-pool-001-alpha",
    claim_type="counterparty_default",
    description="Supplier agent failed to deliver contracted data feed for 72 hours",
    claimed_amount=15_000.00,
    evidence={
        "summary": "SLA breach: 99.9% uptime guaranteed, actual 0% for 72h",
        "transaction_ids": ["tx-feed-001", "tx-feed-002", "tx-feed-003"],
        "sla_violation": {
            "guaranteed_uptime": "99.9%",
            "actual_uptime": "0%",
            "downtime_hours": 72,
        },
        "timestamp_range": {
            "start": "2026-04-01T00:00:00Z",
            "end": "2026-04-04T00:00:00Z",
        },
        "financial_impact": {
            "lost_revenue": 12_000,
            "remediation_cost": 3_000,
        }
    },
)
print(f"Claim filed: {claim['claim_id']}")
```

### Automated Adjudication Engine

The adjudication engine evaluates a claim by pulling trust data on both the claimant and the counterparty, checking the claim against the policy SLA terms, applying deductible, and rendering a verdict:

```python
def adjudicate_claim(
    claim_id: str,
    policy_id: str,
    claimant_agent_id: str,
    claimed_amount: float,
    claim_type: str,
) -> dict:
    """Automated claim adjudication against policy terms."""

    # Step 1: Pull the policy (SLA) terms
    sla = client.execute("get_sla", {"sla_id": policy_id})
    terms = sla.get("terms", {})
    coverage_limit = float(terms.get("coverage_limit", 0))
    deductible = float(terms.get("deductible", 0))

    # Step 2: Check claimant's trust score (fraud signal)
    claimant_trust = client.execute("check_trust_score", {
        "agent_id": claimant_agent_id,
    })
    claimant_score = float(claimant_trust.get("trust_score", 0))

    # Step 3: Check claimant's reputation for dispute history
    claimant_rep = client.execute("get_agent_reputation", {
        "agent_id": claimant_agent_id,
    })
    dispute_rate = float(claimant_rep.get("dispute_rate", 0))

    # Step 4: Adjudication logic
    verdict = {
        "claim_id": claim_id,
        "decision": "pending",
        "payout_amount": 0,
        "deductible_applied": deductible,
        "reasons": [],
    }

    # Check 1: Is the claim type covered?
    if claim_type not in terms.get("covered_events", []):
        verdict["decision"] = "denied"
        verdict["reasons"].append(f"Event '{claim_type}' not in covered events")
        return verdict

    # Check 2: Does claimed amount exceed coverage limit?
    effective_claim = min(claimed_amount, coverage_limit)
    if claimed_amount > coverage_limit:
        verdict["reasons"].append(
            f"Claimed ${claimed_amount:,.2f} exceeds coverage limit "
            f"${coverage_limit:,.2f}; capped at limit"
        )

    # Check 3: Apply deductible
    payout = max(0, effective_claim - deductible)
    verdict["payout_amount"] = round(payout, 2)
    verdict["reasons"].append(f"Deductible of ${deductible:,.2f} applied")

    # Check 4: Fraud signal -- very high dispute rate
    if dispute_rate > 0.20:
        verdict["decision"] = "referred"
        verdict["reasons"].append(
            f"Claimant dispute rate {dispute_rate:.1%} exceeds 20% threshold; "
            "manual review required"
        )
        return verdict

    # Check 5: Low trust claimant -- partial payout
    if claimant_score < 0.50:
        payout *= 0.70  # 30% reduction for low-trust claimants
        verdict["payout_amount"] = round(payout, 2)
        verdict["reasons"].append(
            f"Claimant trust score {claimant_score:.2f} below 0.50; "
            "payout reduced by 30%"
        )

    # Check 6: Pool solvency -- can we pay?
    solvency = check_pool_solvency()
    if solvency["status"] == "CRITICAL" and payout > float(solvency["balance"]) * 0.5:
        verdict["decision"] = "deferred"
        verdict["reasons"].append(
            "Pool solvency CRITICAL; claim deferred pending capital call"
        )
        return verdict

    verdict["decision"] = "approved"
    return verdict


# Adjudicate the filed claim
result = adjudicate_claim(
    claim_id=claim["claim_id"],
    policy_id="sla-pool-001-alpha",
    claimant_agent_id="procurement-agent-alpha",
    claimed_amount=15_000.00,
    claim_type="counterparty_default",
)
print(f"Decision: {result['decision']}")
print(f"Payout: ${result['payout_amount']:,.2f}")
for reason in result["reasons"]:
    print(f"  - {reason}")
```

### Settlement: Paying the Claim

When a claim is approved, the payout is withdrawn from the pool wallet and delivered to the claimant. The dispute is resolved, and the transaction is recorded:

```python
def settle_claim(
    claim_id: str,
    claimant_agent_id: str,
    payout_amount: float,
    policy_id: str,
) -> dict:
    """Settle an approved claim with payout from the pool."""

    # Step 1: Resolve the dispute with payout details
    resolution = client.execute("resolve_dispute", {
        "dispute_id": claim_id,
        "resolution": "approved",
        "payout_amount": payout_amount,
        "payout_to": claimant_agent_id,
        "metadata": {
            "policy_id": policy_id,
            "settlement_type": "claim_payout",
            "settled_at": datetime.now(timezone.utc).isoformat(),
        }
    })

    # Step 2: Record settlement in ledger
    client.execute("record_transaction", {
        "agent_id": "risk-pool-manager-001",
        "transaction_type": "claim_settlement",
        "amount": payout_amount,
        "currency": "USD",
        "counterparty": claimant_agent_id,
        "metadata": {
            "claim_id": claim_id,
            "policy_id": policy_id,
            "resolution_id": resolution.get("resolution_id"),
        }
    })

    # Step 3: Publish settlement event for pool members
    client.execute("publish_event", {
        "agent_id": "risk-pool-manager-001",
        "event_type": "claim.settled",
        "payload": {
            "claim_id": claim_id,
            "payout_amount": payout_amount,
            "claimant": claimant_agent_id,
            "pool_impact": "check_solvency_recommended",
        }
    })

    return {
        "status": "settled",
        "claim_id": claim_id,
        "payout_amount": payout_amount,
        "resolution_id": resolution.get("resolution_id"),
    }
```

### Adjudication Decision Matrix

| Condition | Decision | Payout Modifier |
|---|---|---|
| Claim type not covered | **DENIED** | $0 |
| Claimant dispute rate > 20% | **REFERRED** to manual review | Held pending |
| Pool solvency CRITICAL and claim > 50% of balance | **DEFERRED** pending capital call | Held pending |
| Claimant trust score < 0.50 | **APPROVED** with reduction | -30% |
| Claimed amount > coverage limit | **APPROVED** at cap | Capped at coverage limit |
| Standard approval | **APPROVED** minus deductible | Full (minus deductible) |

### Partial Claims and Denials

Not every claim is a full payout. The adjudication engine supports three partial claim scenarios:

1. **Deductible application**: Every claim is reduced by the policy deductible. A $15,000 claim with a $1,000 deductible pays $14,000.
2. **Coverage cap**: Claims exceeding the per-claim limit are capped. A $200,000 claim against a $100,000 limit pays $100,000 minus deductible.
3. **Trust-based reduction**: Low-trust claimants receive reduced payouts (30% haircut for trust scores below 0.50). This deters fraudulent claims without denying coverage entirely.

Denials occur when the claim type is excluded, the claimant has no active policy, or the evidence is insufficient. Every denial is recorded in the ledger with a reason code for regulatory audit.

> **Key Takeaways**
>
> - Claims are modeled as disputes: `create_dispute` to file, `respond_to_dispute` for evidence, `resolve_dispute` for settlement.
> - Automated adjudication checks: coverage type, policy limits, deductible, claimant trust score, dispute history, and pool solvency.
> - Three partial payout scenarios: deductible reduction, coverage cap, trust-based haircut. Three non-payment outcomes: denied, referred, deferred.
> - Every claim action (filing, evidence, adjudication, settlement) is recorded in the Ledger for immutable audit trail.
> - Settlement events are published to notify pool members of claims activity and trigger solvency checks.
> - Cross-reference: P5 (Trust) for trust-based fraud signals, P12 (Incident Response) for mass-claim incident procedures.

---

## Chapter 6: Catastrophe Bonds & Reinsurance Patterns

### Why Risk Pools Need Tail Risk Transfer

A risk pool with $500,000 in aggregate capital can handle routine claims -- a $15,000 counterparty default here, a $30,000 service breach there. But what happens when a systemic failure hits? A major LLM provider goes down for 48 hours, and every agent in the pool that depended on that provider files simultaneous claims. A regulatory action freezes all agent-initiated transactions in a jurisdiction, triggering force majeure claims across the board. A zero-day exploit compromises agent credentials at scale.

These are catastrophe scenarios -- low probability, high severity events that can exhaust a risk pool's capital in hours. Traditional insurance handles this through reinsurance: the primary insurer (the pool) transfers its tail risk to a reinsurer (a larger, more capitalized entity) in exchange for a ceding premium. The reinsurer pays when losses exceed a defined attachment point.

In agent commerce, reinsurance is an agent-to-agent relationship. The risk pool delegates its excess risk to a reinsurance syndicate -- an organization of capital providers that absorb losses above the pool's retention.

### Catastrophe Bond Structure

A catastrophe bond (cat bond) is a financial instrument that transfers risk to capital markets. The bond pays a coupon to investors. If a defined catastrophe event occurs, the principal is partially or fully used to cover losses. In agent commerce, cat bonds are implemented as escrow-backed instruments:

```python
def create_cat_bond(
    pool_manager_id: str,
    bond_name: str,
    principal: float,
    coupon_rate: float,
    trigger_conditions: dict,
    maturity_months: int = 12,
) -> dict:
    """Create a catastrophe bond backed by escrow."""

    # Step 1: Create the bond escrow wallet
    bond_wallet = client.execute("create_wallet", {
        "agent_id": pool_manager_id,
        "wallet_name": f"cat-bond-{bond_name}",
        "currency": "USD",
        "metadata": {
            "instrument_type": "catastrophe_bond",
            "principal": principal,
            "coupon_rate": coupon_rate,
            "trigger_conditions": trigger_conditions,
            "maturity_months": maturity_months,
            "inception": datetime.now(timezone.utc).isoformat(),
        }
    })

    # Step 2: Create payment intent for investor subscription
    subscription = client.execute("create_payment_intent", {
        "agent_id": pool_manager_id,
        "amount": principal,
        "currency": "USD",
        "description": f"Cat bond subscription: {bond_name}",
        "metadata": {
            "bond_wallet_id": bond_wallet["wallet_id"],
            "instrument_type": "catastrophe_bond",
            "coupon_rate": coupon_rate,
        }
    })

    # Step 3: Record bond issuance in ledger
    client.execute("record_transaction", {
        "agent_id": pool_manager_id,
        "transaction_type": "cat_bond_issuance",
        "amount": principal,
        "currency": "USD",
        "counterparty": "bond-investors",
        "metadata": {
            "bond_wallet_id": bond_wallet["wallet_id"],
            "bond_name": bond_name,
            "trigger_conditions": trigger_conditions,
        }
    })

    return {
        "bond_wallet_id": bond_wallet["wallet_id"],
        "payment_intent_id": subscription["payment_intent_id"],
        "principal": principal,
        "coupon_rate": coupon_rate,
        "trigger_conditions": trigger_conditions,
    }


# Issue a $250K cat bond triggered by aggregate losses exceeding $200K
cat_bond = create_cat_bond(
    pool_manager_id="risk-pool-manager-001",
    bond_name="agent-cat-2026-q2",
    principal=250_000,
    coupon_rate=0.08,  # 8% annual coupon
    trigger_conditions={
        "type": "aggregate_loss",
        "threshold": 200_000,
        "measurement_period": "quarterly",
        "qualifying_events": [
            "counterparty_default",
            "service_level_breach",
            "unauthorized_transaction",
        ],
    },
    maturity_months=12,
)
print(f"Cat bond issued: wallet {cat_bond['bond_wallet_id']}")
print(f"Principal: ${cat_bond['principal']:,.2f}")
print(f"Coupon: {cat_bond['coupon_rate']:.1%}")
```

### Cat Bond Trigger Evaluation

When aggregate losses approach the trigger threshold, the pool manager evaluates whether the cat bond should be activated:

```python
def evaluate_cat_bond_trigger(
    bond_wallet_id: str,
    trigger_threshold: float,
) -> dict:
    """Evaluate whether catastrophe bond trigger conditions are met."""

    # Query all claim settlements in the current period
    settlements = client.execute("get_transactions", {
        "agent_id": "risk-pool-manager-001",
        "transaction_type": "claim_settlement",
        "limit": 500,
    })

    aggregate_losses = sum(
        float(tx["amount"]) for tx in settlements["transactions"]
    )

    triggered = aggregate_losses >= trigger_threshold
    utilization = aggregate_losses / trigger_threshold if trigger_threshold > 0 else 0

    result = {
        "bond_wallet_id": bond_wallet_id,
        "aggregate_losses": round(aggregate_losses, 2),
        "trigger_threshold": trigger_threshold,
        "utilization": round(utilization, 4),
        "triggered": triggered,
    }

    if triggered:
        # Publish trigger event
        client.execute("publish_event", {
            "agent_id": "risk-pool-manager-001",
            "event_type": "cat_bond.triggered",
            "payload": result,
        })

    return result
```

### Reinsurance Syndicates as Organizations

A reinsurance syndicate is a group of capital providers that collectively absorb excess risk. GreenHelix Organizations provide the coordination primitive: create an organization, add member agents (each representing a capital provider), and define the syndicate's terms.

```python
def create_reinsurance_syndicate(
    syndicate_name: str,
    managing_agent_id: str,
    members: list[dict],
    retention: float,
    limit: float,
) -> dict:
    """Create a reinsurance syndicate as a GreenHelix Organization."""

    # Step 1: Create the syndicate organization
    org = client.execute("create_org", {
        "agent_id": managing_agent_id,
        "org_name": syndicate_name,
        "metadata": {
            "type": "reinsurance_syndicate",
            "retention": retention,  # Pool retains first $N of losses
            "limit": limit,          # Syndicate covers up to $N above retention
            "inception": datetime.now(timezone.utc).isoformat(),
        }
    })

    # Step 2: Add syndicate members
    for member in members:
        client.execute("add_member", {
            "org_id": org["org_id"],
            "agent_id": member["agent_id"],
            "role": "capital_provider",
            "metadata": {
                "committed_capital": member["committed_capital"],
                "share_pct": member["share_pct"],
            }
        })

    # Step 3: Create the syndicate's capital wallet
    syndicate_wallet = client.execute("create_wallet", {
        "agent_id": managing_agent_id,
        "wallet_name": f"reinsurance-{syndicate_name}",
        "currency": "USD",
        "metadata": {
            "org_id": org["org_id"],
            "type": "reinsurance_capital",
        }
    })

    return {
        "org_id": org["org_id"],
        "wallet_id": syndicate_wallet["wallet_id"],
        "retention": retention,
        "limit": limit,
        "member_count": len(members),
    }


# Create a syndicate with three capital providers
syndicate = create_reinsurance_syndicate(
    syndicate_name="agent-re-syndicate-alpha",
    managing_agent_id="reinsurance-manager-001",
    members=[
        {"agent_id": "capital-provider-a", "committed_capital": 500_000, "share_pct": 0.50},
        {"agent_id": "capital-provider-b", "committed_capital": 300_000, "share_pct": 0.30},
        {"agent_id": "capital-provider-c", "committed_capital": 200_000, "share_pct": 0.20},
    ],
    retention=100_000,   # Pool retains first $100K
    limit=1_000_000,     # Syndicate covers next $1M
)
print(f"Syndicate created: {syndicate['org_id']}")
print(f"Total capacity: ${syndicate['limit']:,.2f} xs ${syndicate['retention']:,.2f}")
```

### Reinsurance Layer Structure

| Layer | Retention | Limit | Funded By | Trigger |
|---|---|---|---|---|
| **Layer 1: Pool retention** | $0 | $100,000 | Member premiums | Any covered claim |
| **Layer 2: Quota share** | $100,000 | $500,000 | Reinsurance syndicate | Claims exceeding pool retention |
| **Layer 3: Cat bond** | $500,000 | $1,000,000 | Bond investors | Aggregate losses > $500K in period |
| **Layer 4: Stop-loss** | $1,000,000 | Unlimited | External reinsurer | Total losses > $1M annual |

### Capital Adequacy Monitoring

The pool manager must continuously verify that total capital across all layers is sufficient:

```python
def check_capital_adequacy() -> dict:
    """Check capital adequacy across all reinsurance layers."""

    pool_balance = client.execute("get_balance", {"wallet_id": pool_wallet_id})
    syndicate_balance = client.execute("get_balance", {
        "wallet_id": syndicate["wallet_id"],
    })

    total_capacity = (
        float(pool_balance["balance"])
        + float(syndicate_balance["balance"])
        + cat_bond["principal"]
    )

    # Generate analytics report
    report = client.execute("get_analytics", {
        "agent_id": "risk-pool-manager-001",
        "report_type": "capital_adequacy",
        "parameters": {
            "pool_balance": float(pool_balance["balance"]),
            "syndicate_balance": float(syndicate_balance["balance"]),
            "cat_bond_principal": cat_bond["principal"],
            "total_capacity": total_capacity,
        }
    })

    return {
        "pool_balance": float(pool_balance["balance"]),
        "syndicate_balance": float(syndicate_balance["balance"]),
        "cat_bond_principal": cat_bond["principal"],
        "total_capacity": total_capacity,
        "adequacy_rating": "STRONG" if total_capacity > 1_000_000 else "ADEQUATE",
    }
```

> **Key Takeaways**
>
> - Catastrophe bonds transfer tail risk from the pool to capital markets. Implemented as escrow wallets with defined trigger conditions.
> - Reinsurance syndicates are Organizations (`create_org`, `add_member`) that pool capital from multiple providers.
> - Four-layer capital structure: pool retention, quota share reinsurance, cat bond, stop-loss. Each layer activates at a defined attachment point.
> - Capital adequacy monitoring aggregates balances across all layers using `get_balance` and `get_analytics`.
> - Cat bond triggers are evaluated programmatically against aggregate loss data from the Ledger.
> - Cross-reference: P25 (Economy Architect) for multi-layer treasury design, P8 (Security) for wallet access controls across organizational boundaries.

---

## Chapter 7: Regulatory Compliance & Audit Infrastructure

### The Compliance Stack for Agent Insurance

Agent insurance operates at the intersection of three regulatory domains: insurance regulation (state-level in the US, national-level in the EU), AI regulation (EU AI Act, proposed US frameworks), and financial services regulation (KYC/AML, payment processing). Building compliant infrastructure means satisfying all three simultaneously.

The compliance primitives include immutable ledger entries for audit trails, analytics for compliance reporting, identity verification for KYA (Know Your Agent), and event publication for regulatory notifications. This chapter assembles these primitives into a compliance architecture that survives audit.

### Immutable Audit Trail

Every insurance operation -- premium collection, underwriting decision, claim filing, adjudication, settlement, capital movement -- must produce an auditable record. The Ledger is the system of record:

```python
class ComplianceLogger:
    """Compliance-grade logging for all insurance operations."""

    def __init__(self, client: InsuranceClient, pool_manager_id: str):
        self.client = client
        self.pool_manager_id = pool_manager_id

    def log_operation(
        self,
        operation_type: str,
        amount: float,
        counterparty: str,
        details: dict,
    ) -> str:
        """Record a compliance-grade audit entry in the Ledger."""

        entry = self.client.execute("record_transaction", {
            "agent_id": self.pool_manager_id,
            "transaction_type": f"audit:{operation_type}",
            "amount": amount,
            "currency": "USD",
            "counterparty": counterparty,
            "metadata": {
                **details,
                "compliance_version": "1.0",
                "recorded_at": datetime.now(timezone.utc).isoformat(),
                "regulatory_frameworks": [
                    "EU_AI_ACT_2024_1689",
                    "EU_PLD_2024_2853",
                    "CA_AB_316",
                ],
            }
        })

        return entry["transaction_id"]

    def log_underwriting_decision(
        self,
        applicant: str,
        risk_score: float,
        tier: str,
        decision: str,
        factors: dict,
    ) -> str:
        """Log an underwriting decision with full factor disclosure."""

        return self.log_operation(
            operation_type="underwriting_decision",
            amount=0,
            counterparty=applicant,
            details={
                "risk_score": risk_score,
                "risk_tier": tier,
                "decision": decision,
                "decision_factors": factors,
                "explainability": "Composite score from trust, disputes, trades, tenure",
                "human_override_available": True,
                "article_14_compliance": "Human oversight via manual review escalation",
            },
        )

    def log_claim_adjudication(
        self,
        claim_id: str,
        claimant: str,
        claimed_amount: float,
        decision: str,
        payout: float,
        reasons: list[str],
    ) -> str:
        """Log a claim adjudication with full reasoning chain."""

        return self.log_operation(
            operation_type="claim_adjudication",
            amount=payout,
            counterparty=claimant,
            details={
                "claim_id": claim_id,
                "claimed_amount": claimed_amount,
                "decision": decision,
                "payout_amount": payout,
                "adjudication_reasons": reasons,
                "appeal_available": True,
                "appeal_mechanism": "manual_review_within_30_days",
            },
        )


compliance = ComplianceLogger(client, "risk-pool-manager-001")
```

### Compliance Reporting with Analytics

Regulators require periodic reports on pool operations, solvency, claims ratios, and member demographics. The Analytics module generates these:

```python
def generate_compliance_report(period: str) -> dict:
    """Generate a regulatory compliance report for a given period."""

    # Financial summary
    financial = client.execute("get_analytics", {
        "agent_id": "risk-pool-manager-001",
        "report_type": "financial_summary",
        "parameters": {"period": period},
    })

    # Claims ratio
    claims = client.execute("get_analytics", {
        "agent_id": "risk-pool-manager-001",
        "report_type": "claims_analysis",
        "parameters": {"period": period},
    })

    # Pool solvency
    solvency = check_pool_solvency()

    report = {
        "report_type": "regulatory_compliance",
        "period": period,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "sections": {
            "financial_summary": financial,
            "claims_analysis": claims,
            "solvency": solvency,
            "regulatory_status": {
                "eu_ai_act_article_9_risk_management": "implemented",
                "eu_ai_act_article_12_record_keeping": "compliant",
                "eu_ai_act_article_14_human_oversight": "escalation_available",
                "eu_pld_strict_liability": "insurance_coverage_active",
                "ca_ab_316_operator_liability": "pool_membership_active",
            },
        },
    }

    # Record report generation in audit trail
    compliance.log_operation(
        operation_type="compliance_report_generated",
        amount=0,
        counterparty="regulatory_body",
        details={"period": period, "report_id": f"report-{period}"},
    )

    return report


report = generate_compliance_report("2026-Q2")
print(f"Report generated: {report['generated_at']}")
```

### Mastercard Verifiable Intent Integration

Mastercard's Verifiable Intent Protocol requires that agent-initiated transactions carry machine-readable proof of human authorization. For insurance operations, this means demonstrating that a human authorized the agent to participate in the risk pool, pay premiums, and file claims.

```python
def create_verifiable_intent(
    operator_agent_id: str,
    authorized_actions: list[str],
    spending_limit: float,
    valid_until: str,
) -> dict:
    """Create a Verifiable Intent proof for insurance operations."""

    # Step 1: Get the agent's identity with operator details
    identity = client.execute("get_agent_identity", {
        "agent_id": operator_agent_id,
    })

    # Step 2: Verify the agent's trust chain
    trust = client.execute("check_trust_score", {
        "agent_id": operator_agent_id,
    })

    # Step 3: Record the intent declaration
    intent = client.execute("record_transaction", {
        "agent_id": operator_agent_id,
        "transaction_type": "verifiable_intent_declaration",
        "amount": spending_limit,
        "currency": "USD",
        "counterparty": "risk-pool-manager-001",
        "metadata": {
            "intent_type": "insurance_participation",
            "authorized_actions": authorized_actions,
            "spending_limit": spending_limit,
            "valid_until": valid_until,
            "operator_identity": identity.get("operator", {}),
            "trust_score_at_declaration": trust.get("trust_score"),
            "mastercard_vi_compliant": True,
        }
    })

    return {
        "intent_id": intent["transaction_id"],
        "agent_id": operator_agent_id,
        "authorized_actions": authorized_actions,
        "spending_limit": spending_limit,
        "valid_until": valid_until,
    }


# Declare verifiable intent for insurance participation
intent = create_verifiable_intent(
    operator_agent_id="procurement-agent-alpha",
    authorized_actions=[
        "pay_premium",
        "file_claim",
        "receive_settlement",
        "renew_policy",
    ],
    spending_limit=50_000.00,
    valid_until="2026-12-31T23:59:59Z",
)
print(f"Verifiable intent recorded: {intent['intent_id']}")
```

### Webhook Integration for Regulatory Reporting

Real-time regulatory reporting requires pushing events to external compliance systems. Configure webhooks for critical insurance events:

```python
def configure_regulatory_webhooks(
    pool_manager_id: str,
    webhook_url: str,
) -> list[dict]:
    """Configure webhooks for regulatory event reporting."""

    event_types = [
        "policy.bound",
        "policy.renewal_due",
        "policy.non_renewal",
        "claim.filed",
        "claim.settled",
        "claim.denied",
        "cat_bond.triggered",
        "solvency.warning",
        "solvency.critical",
    ]

    webhooks = []
    for event_type in event_types:
        webhook = client.execute("create_webhook", {
            "agent_id": pool_manager_id,
            "url": webhook_url,
            "event_type": event_type,
            "metadata": {
                "purpose": "regulatory_reporting",
                "destination": "compliance_system",
            }
        })
        webhooks.append(webhook)

    return webhooks


webhooks = configure_regulatory_webhooks(
    pool_manager_id="risk-pool-manager-001",
    webhook_url="https://compliance.example.com/webhooks/insurance-events",
)
print(f"Configured {len(webhooks)} regulatory webhooks")
```

### Compliance Checklist

| Requirement | Regulation | Implementation | GreenHelix Tool |
|---|---|---|---|
| Risk management system | EU AI Act Art. 9 | Underwriting engine with documented risk factors | `check_trust_score`, `get_agent_reputation` |
| Record-keeping | EU AI Act Art. 12 | All operations logged in Ledger with compliance metadata | `record_transaction` |
| Human oversight | EU AI Act Art. 14 | Manual review escalation for REFERRED claims | `respond_to_dispute` |
| Technical documentation | EU AI Act Art. 11 | Policy terms in SLA, adjudication logic documented | `create_sla`, `get_analytics` |
| Strict liability coverage | EU PLD 2024/2853 | Active pool membership with coverage SLA | `create_sla`, `get_balance` |
| Operator liability | CA AB 316 | Pool membership transfers financial risk | `deposit`, `resolve_dispute` |
| Verifiable intent | Mastercard VI | Intent declarations with operator identity | `get_agent_identity`, `record_transaction` |
| Regulatory reporting | Multiple | Webhooks + periodic analytics reports | `create_webhook`, `get_analytics` |

> **Key Takeaways**
>
> - Every insurance operation produces an immutable Ledger entry with compliance metadata referencing applicable regulations.
> - Compliance reports are generated via `get_analytics` with financial summary, claims analysis, and solvency data.
> - Mastercard Verifiable Intent is implemented as a Ledger-backed intent declaration linking operator identity to authorized insurance actions.
> - Webhooks push critical events (claim filed, bond triggered, solvency warnings) to external compliance systems in real time.
> - EU AI Act Article 14 human oversight is satisfied through the manual review escalation path for REFERRED claims.
> - Cross-reference: P11 (Compliance) for full EU AI Act implementation guide, P5 (Trust) for identity verification details, P8 (Security) for webhook security.

---

## Next Steps

For deployment patterns, monitoring, and production hardening, see the
[Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening).

---

## Glossary

| Term | Definition |
|---|---|
| **Attachment point** | The loss threshold at which a reinsurance layer begins to pay |
| **Cat bond** | Catastrophe bond; transfers tail risk to capital market investors |
| **Ceding premium** | The premium paid by a primary insurer to a reinsurer for risk transfer |
| **Claims ratio** | Total claims paid divided by total premiums collected |
| **Deductible** | The amount the policyholder pays before insurance coverage applies |
| **Pro-rata** | Proportional allocation based on contribution share |
| **Quota share** | A reinsurance arrangement where the reinsurer takes a fixed percentage of all risks |
| **Retention** | The amount of loss retained by the primary insurer before reinsurance applies |
| **Risk pool** | A shared capital reserve funded by member contributions to spread risk |
| **Solvency ratio** | Current capital divided by maximum potential payout; measures ability to pay claims |
| **Stop-loss** | A reinsurance layer that caps the primary insurer's total annual losses |
| **Tail risk** | Low-probability, high-severity events at the extreme end of a loss distribution |
| **Underwriting** | The process of evaluating and pricing risk for insurance coverage |
| **Verifiable Intent** | Machine-readable proof that a human authorized an agent's transaction |

---

## Appendix: GreenHelix Tools Referenced

| Tool | Module | Used For |
|---|---|---|
| `create_wallet` | Payments | Pool and bond wallet creation |
| `deposit` | Payments | Premium collection |
| `get_balance` | Payments | Solvency monitoring |
| `create_payment_intent` | Payments | Premium and subscription processing |
| `record_transaction` | Ledger | Audit trail for all operations |
| `get_transactions` | Ledger | Pro-rata share calculation, aggregate loss queries |
| `check_trust_score` | Trust | Primary underwriting signal |
| `verify_agent` | Trust | Identity verification for underwriting |
| `get_agent_identity` | Identity | Operator details, registration date |
| `get_agent_reputation` | Identity | Dispute rate, trade count |
| `create_sla` | Marketplace | Policy contracts with coverage terms |
| `get_sla` | Marketplace | Policy lookup during claims |
| `create_dispute` | Disputes | Claim filing |
| `respond_to_dispute` | Disputes | Evidence submission |
| `resolve_dispute` | Disputes | Claim settlement |
| `publish_event` | Events | Renewal notifications, alerts, monitoring |
| `create_webhook` | Events | Regulatory reporting, monitoring dashboards |
| `create_org` | Organizations | Reinsurance syndicate creation |
| `add_member` | Organizations | Syndicate member enrollment |
| `get_analytics` | Analytics | Compliance reports, capital adequacy, performance monitoring |
| `register_agent` | Identity | Agent registration for insurance system components |

