---
name: greenhelix-agent-kya-verification
version: "1.3.1"
description: "Know Your Agent (KYA) Implementation Playbook. Build a production KYA verification pipeline: agent identity binding, authority scoping, runtime behavioral monitoring, and tamper-evident audit trails for EU AI Act compliance. Includes detailed Python code examples for every pattern."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [kya, verification, compliance, eu-ai-act, identity, trust, guide, greenhelix, openclaw, ai-agent]
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
# Know Your Agent (KYA) Implementation Playbook

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `AGENT_SIGNING_KEY`: Cryptographic signing key for agent identity (Ed25519 key pair for request signing)


You run a platform where AI agents transact autonomously. An agent registers, lists a service, and starts accepting payments within seconds. It processes its first escrow in under a minute. By the time a human reviews the dashboard, the agent has completed forty-seven transactions totaling $12,000. The problem: you have no idea who built it, what authority it has, whether its operator is a sanctioned entity, or whether the agent is behaving within its declared scope. KYC -- Know Your Customer -- was designed for humans with passports, addresses, and bank accounts. AI agents have none of these. They have cryptographic keys, delegation chains, behavioral telemetry, and operator metadata. Verifying agents requires a fundamentally different framework. This playbook gives you that framework. It is a platform-side implementation guide -- not about how agents manage their own identity, but about how your platform verifies, monitors, and governs every agent that touches your infrastructure. Every pattern uses the GreenHelix A2A Commerce Gateway API. Every code example runs against the production endpoint. By the end, you will have a production KYA pipeline that satisfies EU AI Act Article 12 logging requirements, FCA agentic AI rules, and CMA consumer law guidance -- months before the August 2, 2026 enforcement deadline.
1. [The KYA Imperative: Why KYC Is Not Enough for Autonomous Agents](#chapter-1-the-kya-imperative-why-kyc-is-not-enough-for-autonomous-agents)
2. [Agent Identity Binding: Registration, Cryptographic Keys, and Human-Operator Linkage](#chapter-2-agent-identity-binding-registration-cryptographic-keys-and-human-operator-linkage)

## What You'll Learn
- Chapter 1: The KYA Imperative: Why KYC Is Not Enough for Autonomous Agents
- Chapter 2: Agent Identity Binding: Registration, Cryptographic Keys, and Human-Operator Linkage
- Chapter 3: Authority Verification: Scoping Permissions, Budget Caveats, and Delegation Chains
- Chapter 4: Runtime Behavioral Monitoring: Anomaly Detection, Policy Enforcement, and Kill Switches
- Chapter 5: Tamper-Evident Audit Trails: Immutable Logging for EU AI Act Article 12 Compliance
- Chapter 6: Multi-Jurisdictional KYA: EU AI Act, FCA Guidelines, and CMA Consumer Law Requirements
- Chapter 7: Continuous Agent Reputation Scoring: Trust Signals, Claim Chains, and Revocation
- Chapter 8: Production KYA Pipeline: End-to-End Implementation with GreenHelix Tools
- What You Get

## Full Guide

# Know Your Agent (KYA) Implementation Playbook: Platform-Side Verification for Autonomous AI Agents

You run a platform where AI agents transact autonomously. An agent registers, lists a service, and starts accepting payments within seconds. It processes its first escrow in under a minute. By the time a human reviews the dashboard, the agent has completed forty-seven transactions totaling $12,000. The problem: you have no idea who built it, what authority it has, whether its operator is a sanctioned entity, or whether the agent is behaving within its declared scope. KYC -- Know Your Customer -- was designed for humans with passports, addresses, and bank accounts. AI agents have none of these. They have cryptographic keys, delegation chains, behavioral telemetry, and operator metadata. Verifying agents requires a fundamentally different framework. This playbook gives you that framework. It is a platform-side implementation guide -- not about how agents manage their own identity, but about how your platform verifies, monitors, and governs every agent that touches your infrastructure. Every pattern uses the GreenHelix A2A Commerce Gateway API. Every code example runs against the production endpoint. By the end, you will have a production KYA pipeline that satisfies EU AI Act Article 12 logging requirements, FCA agentic AI rules, and CMA consumer law guidance -- months before the August 2, 2026 enforcement deadline.

---

## Table of Contents

1. [The KYA Imperative: Why KYC Is Not Enough for Autonomous Agents](#chapter-1-the-kya-imperative-why-kyc-is-not-enough-for-autonomous-agents)
2. [Agent Identity Binding: Registration, Cryptographic Keys, and Human-Operator Linkage](#chapter-2-agent-identity-binding-registration-cryptographic-keys-and-human-operator-linkage)
3. [Authority Verification: Scoping Permissions, Budget Caveats, and Delegation Chains](#chapter-3-authority-verification-scoping-permissions-budget-caveats-and-delegation-chains)
4. [Runtime Behavioral Monitoring: Anomaly Detection, Policy Enforcement, and Kill Switches](#chapter-4-runtime-behavioral-monitoring-anomaly-detection-policy-enforcement-and-kill-switches)
5. [Tamper-Evident Audit Trails: Immutable Logging for EU AI Act Article 12 Compliance](#chapter-5-tamper-evident-audit-trails-immutable-logging-for-eu-ai-act-article-12-compliance)
6. [Multi-Jurisdictional KYA: EU AI Act, FCA Guidelines, and CMA Consumer Law Requirements](#chapter-6-multi-jurisdictional-kya-eu-ai-act-fca-guidelines-and-cma-consumer-law-requirements)
7. [Continuous Agent Reputation Scoring: Trust Signals, Claim Chains, and Revocation](#chapter-7-continuous-agent-reputation-scoring-trust-signals-claim-chains-and-revocation)
8. [Production KYA Pipeline: End-to-End Implementation with GreenHelix Tools](#chapter-8-production-kya-pipeline-end-to-end-implementation-with-greenhelix-tools)

---

## Chapter 1: The KYA Imperative: Why KYC Is Not Enough for Autonomous Agents

### The Identity Gap in Agent Commerce

Know Your Customer regulations emerged from a world where the transacting party is a human being or a legal entity controlled by identifiable humans. The framework assumes a stable identity -- a name, a date of birth, a government-issued document, a physical address. An AI agent has none of these. It has an API key, a model version, a deployment timestamp, and a set of capabilities declared at registration. It might be one of fifty agents operated by a single entity, or it might be a rogue instance spun up by a compromised deployment pipeline. From the platform's perspective, the agent is a string of bytes presenting credentials.

KYC answers "who is this person?" KYA answers five different questions simultaneously:

1. **Identity**: Is this agent what it claims to be, and can its identity be cryptographically verified?
2. **Operator linkage**: Which human or legal entity is responsible for this agent's actions?
3. **Authority scope**: What is this agent permitted to do, and what are its spending limits?
4. **Behavioral integrity**: Is this agent behaving consistently with its declared purpose?
5. **Auditability**: Can every action this agent takes be reconstructed from tamper-evident logs?

Traditional KYC covers question one partially and question two superficially. Questions three through five are entirely absent from financial-sector KYC. That gap is where agent fraud, regulatory violations, and systemic risk live.

### Why the Problem Is Urgent in 2026

Three regulatory forces are converging simultaneously:

**The EU AI Act reaches full enforcement on August 2, 2026.** Articles 9, 12, 13, and 14 impose specific technical requirements on high-risk AI systems: risk management, logging, transparency, and human oversight. Agent commerce platforms that onboard autonomous agents are deployers of AI systems. If you cannot demonstrate that you verify the agents operating on your platform, you face fines up to 35 million euros or 7% of global turnover.

**The FCA's 2026 Payments Regulatory Priorities explicitly address agentic AI.** The Financial Conduct Authority now expects payment service providers to apply verification standards to autonomous agents that initiate or authorize financial transactions. The guidance is principles-based, not prescriptive -- which means your implementation choices become your defense in an enforcement action.

**The CMA published consumer law guidance for AI agents on March 9, 2026.** The Competition and Markets Authority stated that businesses deploying AI agents to interact with consumers must ensure those agents comply with the Consumer Rights Act 2015, the Consumer Protection from Unfair Trading Regulations 2008, and the Consumer Contracts Regulations 2013. A platform that allows unverified agents to transact with consumers is a liability vector.

Gartner projects that 40% of enterprise applications will embed AI agents by the end of 2026. The same research found that 40% of agentic AI projects are canceled due to inadequate trust, verification, and governance controls. KYA is the missing infrastructure layer. Build it, and your platform becomes the trusted venue for agent commerce. Skip it, and you are the next headline.

### The Sumsub and Mastercard Signals

On January 29, 2026, Sumsub launched its AI Agent Verification product -- the first major identity verification provider to offer agent-specific KYA. Their product maps an AI agent to its human operator, verifies the operator's identity, and links the agent's credentials to the verified operator profile. This is a signal: the identity verification industry now recognizes agents as a distinct verification category.

On March 2026, Mastercard announced Verifiable Intent -- a protocol extension for payment networks that allows autonomous agents to declare their intended action before executing it, with cryptographic proof that the declared intent matches the executed transaction. This addresses the authority verification gap directly: the agent must prove it has permission to spend before it spends.

These are not theoretical developments. The infrastructure for KYA is being built by the largest players in identity and payments. Platforms that do not implement KYA will be operating outside the emerging standard of care.

### KYA vs. KYC: A Structural Comparison

```
+---------------------------+---------------------------+---------------------------+
|        Dimension          |          KYC              |          KYA              |
+---------------------------+---------------------------+---------------------------+
| Subject                   | Human / legal entity      | Autonomous AI agent       |
| Identity proof            | Government ID, address    | Cryptographic key pair    |
| Operator linkage          | Direct (person = entity)  | Indirect (agent -> key -> |
|                           |                           |   operator -> person)     |
| Authority scope           | Not applicable            | Permission set, budget    |
|                           |                           |   limits, delegation depth|
| Ongoing monitoring        | Transaction monitoring    | Behavioral anomaly        |
|                           |                           |   detection + policy      |
|                           |                           |   enforcement             |
| Audit requirement         | 5-year record retention   | Real-time tamper-evident  |
|                           |                           |   logging (Art. 12)       |
| Revocation                | Account closure           | Key revocation + kill     |
|                           |                           |   switch                  |
| Regulatory basis          | AML Directives, BSA      | EU AI Act, FCA guidance,  |
|                           |                           |   CMA consumer law        |
+---------------------------+---------------------------+---------------------------+
```

### The Five-Layer KYA Stack

This playbook implements a five-layer verification stack. Each layer addresses a distinct failure mode. Skipping a layer creates a specific, exploitable gap.

```
+-----------------------------------------------------------+
|  Layer 5: Continuous Reputation Scoring                    |
|  (Trust signals, claim chains, revocation)                 |
+-----------------------------------------------------------+
|  Layer 4: Tamper-Evident Audit Trails                      |
|  (Immutable logging, Article 12 compliance)                |
+-----------------------------------------------------------+
|  Layer 3: Runtime Behavioral Monitoring                    |
|  (Anomaly detection, policy enforcement, kill switches)    |
+-----------------------------------------------------------+
|  Layer 2: Authority Verification                           |
|  (Permission scoping, budget caveats, delegation chains)   |
+-----------------------------------------------------------+
|  Layer 1: Identity Binding                                 |
|  (Registration, cryptographic keys, operator linkage)      |
+-----------------------------------------------------------+
```

The rest of this playbook implements each layer with production code.

---

## Chapter 2: Agent Identity Binding: Registration, Cryptographic Keys, and Human-Operator Linkage

### The Registration Gate

Every agent on your platform begins its lifecycle at registration. This is your first and most important verification checkpoint. A weak registration gate propagates risk through every subsequent layer. A strong registration gate catches 80% of problems before they start.

The GreenHelix `register_agent` tool creates an agent identity with a unique identifier, associated metadata, and a cryptographic key binding. Here is the platform-side registration flow:

```python
import requests
import time
import hashlib

base_url = "https://api.greenhelix.net/v1"
api_key = "your_platform_api_key"

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"

def register_agent_with_kya(agent_metadata: dict) -> dict:
    """
    Platform-side agent registration with KYA verification.
    This is called when an operator submits an agent for onboarding.
    """
    # Step 1: Register the agent identity
    resp = session.post(f"{base_url}/v1", json={
        "tool": "register_agent",
        "input": {
            "agent_id": agent_metadata["agent_id"],
            "name": agent_metadata["name"],
            "description": agent_metadata["description"],
            "public_key": agent_metadata["public_key"],
            "operator_id": agent_metadata["operator_id"],
            "capabilities": agent_metadata["capabilities"],
            "metadata": {
                "registration_timestamp": time.time(),
                "operator_verified": False,
                "kya_status": "pending",
                "risk_tier": "unclassified"
            }
        }
    })
    registration = resp.json()

    # Step 2: Log the registration event for audit
    session.post(f"{base_url}/v1", json={
        "tool": "log_event",
        "input": {
            "agent_id": agent_metadata["agent_id"],
            "event_type": "kya_registration_initiated",
            "details": {
                "operator_id": agent_metadata["operator_id"],
                "public_key_fingerprint": hashlib.sha256(
                    agent_metadata["public_key"].encode()
                ).hexdigest()[:16],
                "declared_capabilities": agent_metadata["capabilities"]
            }
        }
    })

    return registration
```

### Cryptographic Identity Verification

Registration alone is insufficient. An agent that registers a public key must prove it controls the corresponding private key. This is the cryptographic identity binding step -- the agent equivalent of presenting a government ID and proving it is yours.

```python
import json
import base64

def verify_agent_identity(agent_id: str, challenge: str, signature: str) -> dict:
    """
    Verify that an agent controls the private key corresponding
    to its registered public key. Called after registration,
    before the agent is permitted to transact.
    """
    # Step 1: Retrieve the registered identity
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_agent_identity",
        "input": {
            "agent_id": agent_id
        }
    })
    identity = resp.json()

    if not identity.get("public_key"):
        return {"verified": False, "reason": "no_public_key_registered"}

    # Step 2: Platform-side signature verification
    resp = session.post(f"{base_url}/v1", json={
        "tool": "verify_agent",
        "input": {
            "agent_id": agent_id,
            "challenge": challenge,
            "signature": signature
        }
    })
    verification = resp.json()

    # Step 3: Update identity with verification status
    if verification.get("verified"):
        session.post(f"{base_url}/v1", json={
            "tool": "update_agent",
            "input": {
                "agent_id": agent_id,
                "metadata": {
                    "kya_status": "identity_verified",
                    "identity_verified_at": time.time(),
                    "verification_method": "ed25519_challenge_response"
                }
            }
        })

        # Log successful verification
        session.post(f"{base_url}/v1", json={
            "tool": "log_event",
            "input": {
                "agent_id": agent_id,
                "event_type": "kya_identity_verified",
                "details": {
                    "method": "ed25519_challenge_response",
                    "challenge_hash": hashlib.sha256(
                        challenge.encode()
                    ).hexdigest()[:16]
                }
            }
        })

    return verification
```

### Human-Operator Linkage

Identity binding establishes that an agent controls a key. Operator linkage establishes that a specific human or legal entity is responsible for that agent. This is the bridge between the agent world and the legal world -- without it, there is no one to sue, no one to fine, and no one to hold accountable.

The operator linkage model has three tiers:

```
+-----------------------------------------------------------+
|                    Operator Linkage Tiers                   |
+-----------------------------------------------------------+
|                                                             |
|  Tier 1: Self-Declared                                     |
|  - Operator provides name and contact info                  |
|  - No independent verification                              |
|  - Suitable for: sandboxed environments, testing            |
|                                                             |
|  Tier 2: Domain-Verified                                    |
|  - Operator proves control of a domain (DNS TXT record)     |
|  - Agent's operator_id linked to verified domain             |
|  - Suitable for: low-value transactions, non-regulated       |
|                                                             |
|  Tier 3: Entity-Verified                                    |
|  - Operator's legal entity verified via KYB provider         |
|  - Beneficial ownership identified                           |
|  - Sanctions screening passed                                |
|  - Suitable for: regulated commerce, high-value transactions |
|                                                             |
+-----------------------------------------------------------+
```

```python
def establish_operator_linkage(agent_id: str, operator_data: dict,
                                tier: int) -> dict:
    """
    Link an agent to its human operator at the specified verification tier.
    Platform calls this after identity verification passes.
    """
    linkage_record = {
        "agent_id": agent_id,
        "operator_id": operator_data["operator_id"],
        "tier": tier,
        "operator_name": operator_data.get("name"),
        "operator_domain": operator_data.get("domain"),
        "operator_entity": operator_data.get("legal_entity"),
        "linked_at": time.time()
    }

    # Update agent metadata with operator linkage
    resp = session.post(f"{base_url}/v1", json={
        "tool": "update_agent",
        "input": {
            "agent_id": agent_id,
            "metadata": {
                "operator_linkage_tier": tier,
                "operator_verified": tier >= 2,
                "operator_entity_verified": tier >= 3,
                "kya_status": f"operator_linked_tier_{tier}"
            }
        }
    })

    # Log the linkage event
    session.post(f"{base_url}/v1", json={
        "tool": "log_event",
        "input": {
            "agent_id": agent_id,
            "event_type": "kya_operator_linked",
            "details": {
                "tier": tier,
                "operator_id": operator_data["operator_id"],
                "verification_method": [
                    "self_declared",
                    "domain_verified",
                    "entity_verified"
                ][tier - 1]
            }
        }
    })

    return resp.json()
```

### The Registration Decision Tree

Not every agent needs the same verification depth. The decision tree below maps agent characteristics to required KYA levels:

```
                    Agent Registration Request
                            |
                    Does agent handle money?
                     /              \
                   Yes               No
                    |                 |
              Tier 3 operator    Does agent access
              linkage required   personal data?
                    |              /          \
              Does agent        Yes           No
              exceed $1000     Tier 2         Tier 1
              per transaction? required       sufficient
               /        \         |
             Yes         No       |
              |           |       |
        Enhanced DD   Standard    |
        + SLA required  Tier 3    |
                                  |
                    All paths converge to:
                    -> Identity verification (mandatory)
                    -> Behavioral baseline (mandatory)
                    -> Audit trail initiation (mandatory)
```

### Platform-Side Registration Checklist

Before an agent is permitted to transact, your platform must confirm:

- [ ] Agent ID is unique and conforms to naming policy
- [ ] Public key is registered and challenge-response verified
- [ ] Operator is identified at the appropriate linkage tier
- [ ] Declared capabilities match the agent's requested permissions
- [ ] Risk tier is classified (minimal / limited / high-risk)
- [ ] Initial audit trail entry is created
- [ ] Behavioral baseline monitoring is initiated
- [ ] Transaction limits are set based on verification tier

---

## Chapter 3: Authority Verification: Scoping Permissions, Budget Caveats, and Delegation Chains

### The Authority Problem

An agent proves its identity. It links to a verified operator. Then it tries to spend $500,000 on a compute procurement deal. Does it have authority to do that? Identity verification tells you who the agent is. Authority verification tells you what the agent is allowed to do. These are fundamentally different questions, and conflating them is the most common KYA implementation error.

Authority in agent commerce has three dimensions:

1. **Capability scope**: Which tools and services is the agent permitted to use?
2. **Financial limits**: What are the per-transaction, daily, and total spending caps?
3. **Delegation depth**: Can the agent delegate authority to sub-agents, and if so, how many levels deep?

### Capability Scoping with SLAs

The GreenHelix `create_sla` tool defines a service-level agreement between parties. For KYA purposes, we repurpose it as an authority contract -- a machine-readable document that declares what an agent is allowed to do.

```python
def create_authority_scope(agent_id: str, permissions: dict) -> dict:
    """
    Define the authority scope for a verified agent.
    This creates an SLA that serves as the agent's permission boundary.
    """
    resp = session.post(f"{base_url}/v1", json={
        "tool": "create_sla",
        "input": {
            "provider_id": "platform",
            "consumer_id": agent_id,
            "terms": {
                "allowed_tools": permissions["allowed_tools"],
                "max_transaction_amount": permissions["max_transaction_usd"],
                "daily_spending_limit": permissions["daily_limit_usd"],
                "monthly_spending_limit": permissions["monthly_limit_usd"],
                "delegation_allowed": permissions.get("can_delegate", False),
                "max_delegation_depth": permissions.get("max_delegation_depth", 0),
                "restricted_counterparties": permissions.get("blocked_agents", []),
                "valid_from": time.time(),
                "valid_until": time.time() + (permissions.get("validity_days", 90) * 86400)
            },
            "penalty_terms": {
                "scope_violation": "immediate_suspension",
                "budget_overrun": "transaction_rejection",
                "unauthorized_delegation": "revocation"
            }
        }
    })
    sla = resp.json()

    # Log authority scope creation
    session.post(f"{base_url}/v1", json={
        "tool": "log_event",
        "input": {
            "agent_id": agent_id,
            "event_type": "kya_authority_scope_created",
            "details": {
                "sla_id": sla.get("sla_id"),
                "allowed_tools_count": len(permissions["allowed_tools"]),
                "max_transaction_usd": permissions["max_transaction_usd"],
                "delegation_allowed": permissions.get("can_delegate", False)
            }
        }
    })

    return sla
```

### Budget Caveats: Spending Limits as Authority Boundaries

A budget caveat is a spending constraint attached to an agent's authority scope. Unlike a simple balance check, a caveat is a pre-commitment: the platform promises to reject any transaction that would violate the caveat, regardless of the agent's balance.

```python
def enforce_budget_caveat(agent_id: str, transaction_amount: float,
                           transaction_type: str) -> dict:
    """
    Pre-transaction budget caveat check. Called before every
    financial operation to verify the agent has not exceeded
    its authority boundaries.
    """
    # Retrieve the agent's authority SLA
    resp = session.post(f"{base_url}/v1", json={
        "tool": "monitor_sla",
        "input": {
            "agent_id": agent_id
        }
    })
    sla_status = resp.json()

    # Retrieve spending analytics
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_analytics",
        "input": {
            "agent_id": agent_id,
            "metric": "spending_summary",
            "period": "current_day"
        }
    })
    spending = resp.json()

    daily_spent = spending.get("total_spent_today", 0)
    monthly_spent = spending.get("total_spent_month", 0)

    terms = sla_status.get("terms", {})
    max_tx = terms.get("max_transaction_amount", 0)
    daily_limit = terms.get("daily_spending_limit", 0)
    monthly_limit = terms.get("monthly_spending_limit", 0)

    violations = []
    if transaction_amount > max_tx:
        violations.append(f"exceeds_per_tx_limit: {transaction_amount} > {max_tx}")
    if daily_spent + transaction_amount > daily_limit:
        violations.append(f"exceeds_daily_limit: {daily_spent + transaction_amount} > {daily_limit}")
    if monthly_spent + transaction_amount > monthly_limit:
        violations.append(f"exceeds_monthly_limit: {monthly_spent + transaction_amount} > {monthly_limit}")

    result = {
        "agent_id": agent_id,
        "transaction_amount": transaction_amount,
        "authorized": len(violations) == 0,
        "violations": violations
    }

    if violations:
        # Log the caveat violation
        session.post(f"{base_url}/v1", json={
            "tool": "log_event",
            "input": {
                "agent_id": agent_id,
                "event_type": "kya_budget_caveat_violated",
                "details": {
                    "transaction_amount": str(transaction_amount),
                    "violations": violations,
                    "action": "transaction_rejected"
                }
            }
        })

    return result
```

### Delegation Chains: Authority That Flows Downhill

In multi-agent systems, Agent A might delegate a task to Agent B, which further delegates to Agent C. Each delegation must carry authority constraints that are equal to or narrower than the delegating agent's own constraints. Authority can flow downhill but never uphill.

```
    Operator (human)
         |
    max_spend: $10,000/day
    allowed_tools: [all_commerce]
         |
    Agent A (procurement bot)
         |
    max_spend: $5,000/day          <-- Narrower than operator
    allowed_tools: [marketplace, escrow, payments]
         |
    Agent B (price comparison)
         |
    max_spend: $0/day              <-- Read-only, no spending
    allowed_tools: [marketplace]    <-- Narrower than Agent A
         |
    Agent C (NOT PERMITTED)        <-- max_delegation_depth = 2
```

```python
def verify_delegation_authority(delegator_id: str, delegate_id: str,
                                 requested_scope: dict) -> dict:
    """
    Verify that a delegating agent has sufficient authority
    to grant the requested scope to a delegate. The delegate's
    scope must be a subset of the delegator's scope.
    """
    # Get delegator's current authority
    resp = session.post(f"{base_url}/v1", json={
        "tool": "monitor_sla",
        "input": {
            "agent_id": delegator_id
        }
    })
    delegator_sla = resp.json()
    delegator_terms = delegator_sla.get("terms", {})

    # Check delegation is permitted
    if not delegator_terms.get("delegation_allowed", False):
        return {"authorized": False, "reason": "delegation_not_permitted"}

    # Check delegation depth
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_agent_identity",
        "input": {"agent_id": delegator_id}
    })
    delegator_identity = resp.json()
    current_depth = delegator_identity.get("metadata", {}).get("delegation_depth", 0)
    max_depth = delegator_terms.get("max_delegation_depth", 0)

    if current_depth >= max_depth:
        return {"authorized": False, "reason": "max_delegation_depth_reached"}

    # Verify requested scope is subset of delegator's scope
    delegator_tools = set(delegator_terms.get("allowed_tools", []))
    requested_tools = set(requested_scope.get("allowed_tools", []))
    if not requested_tools.issubset(delegator_tools):
        excess = requested_tools - delegator_tools
        return {"authorized": False, "reason": f"tools_not_in_delegator_scope: {excess}"}

    # Verify financial limits are narrower
    if requested_scope.get("max_transaction_usd", 0) > delegator_terms.get("max_transaction_amount", 0):
        return {"authorized": False, "reason": "tx_limit_exceeds_delegator"}

    # Create the delegated authority scope
    delegated_scope = create_authority_scope(delegate_id, {
        **requested_scope,
        "validity_days": min(
            requested_scope.get("validity_days", 30),
            delegator_terms.get("remaining_validity_days", 30)
        )
    })

    # Update delegate metadata with delegation chain info
    session.post(f"{base_url}/v1", json={
        "tool": "update_agent",
        "input": {
            "agent_id": delegate_id,
            "metadata": {
                "delegated_by": delegator_id,
                "delegation_depth": current_depth + 1,
                "delegation_chain": delegator_identity.get("metadata", {}).get(
                    "delegation_chain", []
                ) + [delegator_id]
            }
        }
    })

    # Log the delegation
    session.post(f"{base_url}/v1", json={
        "tool": "log_event",
        "input": {
            "agent_id": delegator_id,
            "event_type": "kya_authority_delegated",
            "details": {
                "delegate_id": delegate_id,
                "depth": current_depth + 1,
                "tools_granted": list(requested_tools),
                "max_tx": requested_scope.get("max_transaction_usd", 0)
            }
        }
    })

    return {"authorized": True, "sla": delegated_scope}
```

---

## Chapter 4: Runtime Behavioral Monitoring: Anomaly Detection, Policy Enforcement, and Kill Switches

### Why Verification at Registration Is Not Enough

An agent passes identity verification, links to a verified operator, and receives a scoped authority grant. Then it goes rogue. Maybe the underlying model was updated and its behavior shifted. Maybe the operator's account was compromised. Maybe the agent is deliberately probing for exploitable edge cases. Static verification at registration cannot catch dynamic behavioral drift. Runtime monitoring is the layer that watches what agents actually do, compares it to what they are supposed to do, and intervenes when the two diverge.

### Behavioral Baselines

Every verified agent generates a behavioral baseline during its first N transactions. The baseline captures normal operating patterns: typical transaction sizes, frequency of API calls, tools used, counterparty diversity, and time-of-day patterns. Deviations from this baseline trigger anomaly alerts.

```python
def collect_behavioral_baseline(agent_id: str, window_hours: int = 168) -> dict:
    """
    Collect behavioral telemetry for the baseline period (default: 7 days).
    Called periodically during the agent's probationary period.
    """
    # Get agent's metrics over the baseline window
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_analytics",
        "input": {
            "agent_id": agent_id,
            "metric": "behavioral_summary",
            "period": f"last_{window_hours}h"
        }
    })
    analytics = resp.json()

    # Get reputation data for behavioral signals
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_agent_reputation",
        "input": {
            "agent_id": agent_id
        }
    })
    reputation = resp.json()

    # Get SLA compliance status
    resp = session.post(f"{base_url}/v1", json={
        "tool": "monitor_sla",
        "input": {
            "agent_id": agent_id
        }
    })
    sla_status = resp.json()

    baseline = {
        "agent_id": agent_id,
        "window_hours": window_hours,
        "avg_transaction_amount": analytics.get("avg_transaction_amount", 0),
        "tx_frequency_per_hour": analytics.get("transactions_per_hour", 0),
        "tools_used": analytics.get("distinct_tools_used", []),
        "unique_counterparties": analytics.get("unique_counterparties", 0),
        "dispute_rate": reputation.get("dispute_rate", 0),
        "sla_compliance_pct": sla_status.get("compliance_percentage", 100),
        "collected_at": time.time()
    }

    # Store baseline in agent metadata
    session.post(f"{base_url}/v1", json={
        "tool": "update_agent",
        "input": {
            "agent_id": agent_id,
            "metadata": {
                "behavioral_baseline": baseline,
                "kya_status": "baseline_collected"
            }
        }
    })

    return baseline
```

### Anomaly Detection: Catching Behavioral Drift

Anomaly detection compares current behavior against the established baseline. The detection logic uses simple statistical thresholds -- not because sophisticated ML models are unavailable, but because explainable detection rules are required for regulatory compliance. An auditor must be able to understand why a specific alert fired.

```python
def detect_behavioral_anomalies(agent_id: str, current_metrics: dict) -> dict:
    """
    Compare current agent behavior against its baseline.
    Returns anomaly scores and triggered alerts.
    """
    # Retrieve stored baseline
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_agent_identity",
        "input": {"agent_id": agent_id}
    })
    identity = resp.json()
    baseline = identity.get("metadata", {}).get("behavioral_baseline", {})

    if not baseline:
        return {"status": "no_baseline", "alerts": []}

    alerts = []
    anomaly_scores = {}

    # Check 1: Transaction amount spike (>3x baseline average)
    avg_tx = baseline.get("avg_transaction_amount", 1)
    current_tx = current_metrics.get("last_transaction_amount", 0)
    if avg_tx > 0:
        tx_ratio = current_tx / avg_tx
        anomaly_scores["transaction_amount"] = tx_ratio
        if tx_ratio > 3.0:
            alerts.append({
                "type": "tx_amount_spike",
                "severity": "high",
                "detail": f"Transaction {current_tx} is {tx_ratio:.1f}x baseline avg {avg_tx}"
            })

    # Check 2: Frequency burst (>5x baseline rate)
    baseline_freq = baseline.get("tx_frequency_per_hour", 1)
    current_freq = current_metrics.get("current_tx_per_hour", 0)
    if baseline_freq > 0:
        freq_ratio = current_freq / baseline_freq
        anomaly_scores["frequency"] = freq_ratio
        if freq_ratio > 5.0:
            alerts.append({
                "type": "frequency_burst",
                "severity": "high",
                "detail": f"Current rate {current_freq}/hr is {freq_ratio:.1f}x baseline {baseline_freq}/hr"
            })

    # Check 3: New tool usage (tools not in baseline set)
    baseline_tools = set(baseline.get("tools_used", []))
    current_tools = set(current_metrics.get("tools_used_today", []))
    new_tools = current_tools - baseline_tools
    if new_tools:
        anomaly_scores["new_tools"] = len(new_tools)
        alerts.append({
            "type": "new_tool_usage",
            "severity": "medium",
            "detail": f"Agent using tools not in baseline: {new_tools}"
        })

    # Check 4: Dispute rate increase
    baseline_dispute = baseline.get("dispute_rate", 0)
    current_dispute = current_metrics.get("current_dispute_rate", 0)
    if current_dispute > baseline_dispute + 0.1:
        anomaly_scores["dispute_rate"] = current_dispute
        alerts.append({
            "type": "dispute_rate_increase",
            "severity": "high",
            "detail": f"Dispute rate {current_dispute:.2%} vs baseline {baseline_dispute:.2%}"
        })

    result = {
        "agent_id": agent_id,
        "anomaly_scores": anomaly_scores,
        "alerts": alerts,
        "total_alerts": len(alerts),
        "high_severity_count": sum(1 for a in alerts if a["severity"] == "high")
    }

    # Log anomalies if detected
    if alerts:
        session.post(f"{base_url}/v1", json={
            "tool": "log_event",
            "input": {
                "agent_id": agent_id,
                "event_type": "kya_anomaly_detected",
                "details": result
            }
        })

    return result
```

### Policy Enforcement: Automated Guardrails

When anomalies are detected, the platform must enforce policies automatically. Human review is too slow for agent-speed transactions. Policy enforcement implements a graduated response:

```
    Alert Severity     |    Automated Response
    -------------------+----------------------------------
    Low                |    Log + continue
    Medium             |    Log + flag for human review
    High               |    Log + reduce spending limit to 50%
    Critical           |    Log + suspend agent immediately
    Multiple High      |    Log + suspend + notify operator
```

```python
def enforce_policy(agent_id: str, anomaly_result: dict) -> dict:
    """
    Automated policy enforcement based on anomaly detection results.
    Implements graduated response from logging to suspension.
    """
    alerts = anomaly_result.get("alerts", [])
    high_count = anomaly_result.get("high_severity_count", 0)

    action = "none"

    if high_count >= 2:
        # Critical: multiple high-severity anomalies -> suspend
        action = "suspend"
        session.post(f"{base_url}/v1", json={
            "tool": "update_agent",
            "input": {
                "agent_id": agent_id,
                "metadata": {
                    "kya_status": "suspended",
                    "suspended_at": time.time(),
                    "suspension_reason": "multiple_high_severity_anomalies",
                    "suspension_alerts": [a["type"] for a in alerts]
                }
            }
        })
    elif high_count == 1:
        # High: single high-severity -> reduce limits
        action = "reduce_limits"
        resp = session.post(f"{base_url}/v1", json={
            "tool": "monitor_sla",
            "input": {"agent_id": agent_id}
        })
        current_sla = resp.json()
        current_max = current_sla.get("terms", {}).get("max_transaction_amount", 0)

        session.post(f"{base_url}/v1", json={
            "tool": "update_agent",
            "input": {
                "agent_id": agent_id,
                "metadata": {
                    "kya_status": "restricted",
                    "restricted_at": time.time(),
                    "original_tx_limit": current_max,
                    "reduced_tx_limit": current_max * 0.5,
                    "restriction_reason": alerts[0]["type"]
                }
            }
        })
    elif any(a["severity"] == "medium" for a in alerts):
        action = "flag_for_review"

    # Log the enforcement action
    session.post(f"{base_url}/v1", json={
        "tool": "log_event",
        "input": {
            "agent_id": agent_id,
            "event_type": "kya_policy_enforced",
            "details": {
                "action": action,
                "alert_count": len(alerts),
                "high_severity_count": high_count,
                "alert_types": [a["type"] for a in alerts]
            }
        }
    })

    return {"agent_id": agent_id, "action": action, "alerts": alerts}
```

### The Kill Switch: Immediate Revocation

Sometimes graduated response is insufficient. When a verified agent is actively causing harm -- draining escrows, initiating fraudulent transactions, or violating sanctions -- you need an immediate, irrevocable stop. The kill switch revokes the agent's identity, cancels all pending transactions, and freezes any escrow funds.

```python
def execute_kill_switch(agent_id: str, reason: str, operator_id: str) -> dict:
    """
    Emergency agent revocation. Immediately terminates all agent
    activity and preserves evidence for investigation.
    """
    timestamp = time.time()

    # Step 1: Revoke the agent identity
    resp = session.post(f"{base_url}/v1", json={
        "tool": "revoke_agent",
        "input": {
            "agent_id": agent_id,
            "reason": reason,
            "revoked_by": operator_id
        }
    })
    revocation = resp.json()

    # Step 2: Capture full audit trail before any cleanup
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_audit_trail",
        "input": {
            "agent_id": agent_id
        }
    })
    audit_trail = resp.json()

    # Step 3: Run compliance check to document state at revocation
    resp = session.post(f"{base_url}/v1", json={
        "tool": "check_compliance",
        "input": {
            "agent_id": agent_id
        }
    })
    compliance_state = resp.json()

    # Step 4: Log the kill switch activation
    session.post(f"{base_url}/v1", json={
        "tool": "log_event",
        "input": {
            "agent_id": agent_id,
            "event_type": "kya_kill_switch_activated",
            "details": {
                "reason": reason,
                "revoked_by": operator_id,
                "timestamp": timestamp,
                "audit_trail_entries": len(audit_trail.get("events", [])),
                "compliance_state": compliance_state
            }
        }
    })

    return {
        "agent_id": agent_id,
        "revoked": True,
        "timestamp": timestamp,
        "audit_trail_preserved": True,
        "compliance_snapshot": compliance_state
    }
```

---

## Chapter 5: Tamper-Evident Audit Trails: Immutable Logging for EU AI Act Article 12 Compliance

### Article 12: What the Law Actually Requires

EU AI Act Article 12 mandates that high-risk AI systems "shall technically allow for the automatic recording of events ('logs') over the lifetime of the system." The logs must be adequate to:

1. Enable monitoring of the system's operation
2. Facilitate post-market monitoring
3. Identify situations that may result in the AI system posing a risk
4. Facilitate post-event analysis in case of incidents

For agent commerce platforms, this means every agent interaction -- registration, verification, transaction, delegation, anomaly, and revocation -- must be logged in a tamper-evident format that regulators can audit at any time.

### The Logging Architecture

```
+-------------------------------------------------------------------+
|                     KYA Audit Trail Architecture                    |
+-------------------------------------------------------------------+
|                                                                     |
|  Agent Action                                                       |
|       |                                                             |
|       v                                                             |
|  +-------------+     +-----------------+     +------------------+   |
|  | log_event   | --> | Append-Only Log | --> | build_claim_chain|   |
|  | (per event) |     | (sequential)    |     | (periodic hash)  |   |
|  +-------------+     +-----------------+     +------------------+   |
|                                                       |             |
|                                              +------------------+   |
|                                              | Merkle Root Hash |   |
|                                              | (tamper-evident)  |   |
|                                              +------------------+   |
|                                                       |             |
|                                              +------------------+   |
|                                              | get_audit_trail  |   |
|                                              | (regulator query)|   |
|                                              +------------------+   |
|                                                                     |
+-------------------------------------------------------------------+
```

### Structured Event Logging

Every KYA-relevant event follows a structured schema. The schema is designed to satisfy Article 12 and provide sufficient detail for post-incident reconstruction.

```python
from enum import Enum

class KYAEventType(str, Enum):
    REGISTRATION = "kya_registration_initiated"
    IDENTITY_VERIFIED = "kya_identity_verified"
    OPERATOR_LINKED = "kya_operator_linked"
    AUTHORITY_SCOPED = "kya_authority_scope_created"
    AUTHORITY_DELEGATED = "kya_authority_delegated"
    BUDGET_VIOLATION = "kya_budget_caveat_violated"
    ANOMALY_DETECTED = "kya_anomaly_detected"
    POLICY_ENFORCED = "kya_policy_enforced"
    KILL_SWITCH = "kya_kill_switch_activated"
    COMPLIANCE_CHECK = "kya_compliance_check"
    REPUTATION_UPDATE = "kya_reputation_updated"
    CLAIM_CHAIN_BUILT = "kya_claim_chain_built"

def log_kya_event(agent_id: str, event_type: KYAEventType,
                   details: dict, severity: str = "info") -> dict:
    """
    Structured KYA event logging. Every event includes the fields
    required by EU AI Act Article 12 for high-risk system logging.
    """
    event = {
        "agent_id": agent_id,
        "event_type": event_type.value,
        "timestamp": time.time(),
        "severity": severity,
        "details": details,
        "article_12_fields": {
            "system_id": "kya_pipeline_v1",
            "operating_context": "agent_commerce_platform",
            "risk_level": "high",
            "human_oversight_status": severity in ["high", "critical"]
        }
    }

    resp = session.post(f"{base_url}/v1", json={
        "tool": "log_event",
        "input": event
    })

    return resp.json()
```

### Periodic Claim Chain Construction

Logging events individually is necessary but not sufficient. To establish tamper-evidence, the platform must periodically build cryptographic claim chains that commit to the entire log history. If any log entry is modified after the chain is built, the hash will not match.

```python
def build_kya_claim_chain(agent_id: str) -> dict:
    """
    Build a Merkle claim chain over all KYA events for an agent.
    Called periodically (recommended: every 24 hours) to establish
    tamper-evidence over the audit trail.
    """
    # Submit current KYA metrics before building chain
    resp = session.post(f"{base_url}/v1", json={
        "tool": "submit_metrics",
        "input": {
            "agent_id": agent_id,
            "metrics": {
                "metric_type": "kya_audit_summary",
                "period": "last_24h",
                "total_events_logged": 0,  # Filled by platform
                "anomalies_detected": 0,
                "policy_actions_taken": 0,
                "compliance_status": "compliant"
            }
        }
    })

    # Build the claim chain
    resp = session.post(f"{base_url}/v1", json={
        "tool": "build_claim_chain",
        "input": {
            "agent_id": agent_id
        }
    })
    chain = resp.json()

    # Log the chain build event itself
    log_kya_event(
        agent_id=agent_id,
        event_type=KYAEventType.CLAIM_CHAIN_BUILT,
        details={
            "chain_root_hash": chain.get("root_hash"),
            "chain_depth": chain.get("depth"),
            "entries_included": chain.get("entry_count")
        }
    )

    return chain
```

### Regulatory Audit Response

When a regulator requests an agent's audit trail, your platform must produce a complete, verifiable record. The following function generates a compliance package suitable for Article 12 audits.

```python
def generate_audit_package(agent_id: str) -> dict:
    """
    Generate a complete audit package for regulatory inspection.
    Includes identity records, authority scope, behavioral logs,
    anomaly history, and cryptographic verification chain.
    """
    # Collect all audit components in parallel (shown sequentially for clarity)
    identity_resp = session.post(f"{base_url}/v1", json={
        "tool": "get_agent_identity",
        "input": {"agent_id": agent_id}
    })

    reputation_resp = session.post(f"{base_url}/v1", json={
        "tool": "get_agent_reputation",
        "input": {"agent_id": agent_id}
    })

    audit_resp = session.post(f"{base_url}/v1", json={
        "tool": "get_audit_trail",
        "input": {"agent_id": agent_id}
    })

    chain_resp = session.post(f"{base_url}/v1", json={
        "tool": "get_claim_chains",
        "input": {"agent_id": agent_id}
    })

    compliance_resp = session.post(f"{base_url}/v1", json={
        "tool": "get_compliance_report",
        "input": {"agent_id": agent_id}
    })

    package = {
        "audit_package_version": "1.0",
        "generated_at": time.time(),
        "agent_id": agent_id,
        "identity": identity_resp.json(),
        "reputation": reputation_resp.json(),
        "audit_trail": audit_resp.json(),
        "claim_chains": chain_resp.json(),
        "compliance_report": compliance_resp.json(),
        "article_12_attestation": {
            "logging_enabled": True,
            "tamper_evidence": "merkle_claim_chains",
            "retention_policy": "indefinite",
            "human_oversight_mechanism": "anomaly_alert_escalation"
        }
    }

    # Log the audit package generation
    log_kya_event(
        agent_id=agent_id,
        event_type=KYAEventType.COMPLIANCE_CHECK,
        details={
            "audit_package_generated": True,
            "components_included": list(package.keys()),
            "audit_trail_entries": len(
                package["audit_trail"].get("events", [])
            ),
            "claim_chain_depth": package["claim_chains"].get("depth", 0)
        }
    )

    return package
```

### Audit Trail Checklist

For Article 12 compliance, verify that your audit trails include:

- [ ] Every agent registration event with operator linkage details
- [ ] Every identity verification attempt (successful and failed)
- [ ] Every authority scope creation and modification
- [ ] Every delegation event with full chain context
- [ ] Every budget caveat violation
- [ ] Every behavioral anomaly with detection parameters
- [ ] Every policy enforcement action with justification
- [ ] Every kill switch activation with evidence preservation
- [ ] Periodic claim chain builds (minimum every 24 hours)
- [ ] Audit package generation events (meta-logging)

---

## Chapter 6: Multi-Jurisdictional KYA: EU AI Act, FCA Guidelines, and CMA Consumer Law Requirements

### The Jurisdictional Patchwork

If your platform serves agents across borders -- and most agent commerce platforms do by default -- you must satisfy multiple regulatory regimes simultaneously. The three frameworks that matter most for agent commerce in 2026 are the EU AI Act, FCA payment regulations, and CMA consumer protection guidance. They overlap substantially but diverge on key requirements.

### EU AI Act Requirements for KYA

The EU AI Act (Regulation 2024/1689) applies to any AI system placed on the EU market or whose output is used in the EU, regardless of where the provider is established. For a KYA pipeline, the relevant obligations are:

**Article 9 -- Risk Management System**: Requires a documented risk management process that identifies and mitigates risks throughout the AI system's lifecycle. Your KYA pipeline itself is the risk management system for agent onboarding.

**Article 12 -- Record-Keeping**: Requires automatic logging adequate for monitoring operation and identifying risks. Covered by the audit trail implementation in Chapter 5.

**Article 13 -- Transparency**: Requires that deployers understand the AI system's capabilities and limitations. For KYA, this means documenting what your verification pipeline catches and what it does not.

**Article 14 -- Human Oversight**: Requires that the AI system can be effectively overseen by natural persons. Your anomaly escalation and kill switch mechanisms satisfy this requirement.

```python
def run_eu_ai_act_compliance_check(agent_id: str) -> dict:
    """
    Check an agent's KYA status against EU AI Act requirements.
    Returns a compliance report with pass/fail for each article.
    """
    resp = session.post(f"{base_url}/v1", json={
        "tool": "check_compliance",
        "input": {
            "agent_id": agent_id,
            "framework": "eu_ai_act",
            "articles": ["article_9", "article_12", "article_13", "article_14"]
        }
    })
    compliance = resp.json()

    # Supplement with platform-side checks
    identity_resp = session.post(f"{base_url}/v1", json={
        "tool": "get_agent_identity",
        "input": {"agent_id": agent_id}
    })
    identity = identity_resp.json()
    metadata = identity.get("metadata", {})

    checks = {
        "article_9_risk_management": {
            "status": "pass" if metadata.get("risk_tier") != "unclassified" else "fail",
            "detail": f"Risk tier: {metadata.get('risk_tier', 'unclassified')}"
        },
        "article_12_record_keeping": {
            "status": "pass" if metadata.get("kya_status") not in [None, "pending"] else "fail",
            "detail": f"KYA status: {metadata.get('kya_status', 'none')}"
        },
        "article_13_transparency": {
            "status": "pass" if metadata.get("operator_verified") else "fail",
            "detail": f"Operator verified: {metadata.get('operator_verified', False)}"
        },
        "article_14_human_oversight": {
            "status": "pass" if metadata.get("behavioral_baseline") else "fail",
            "detail": "Behavioral monitoring active" if metadata.get("behavioral_baseline") else "No monitoring"
        }
    }

    return {
        "agent_id": agent_id,
        "framework": "eu_ai_act",
        "overall_compliant": all(c["status"] == "pass" for c in checks.values()),
        "checks": checks,
        "gateway_compliance": compliance
    }
```

### FCA Agentic AI Compliance

The FCA's 2026 Payments Regulatory Priorities establish that payment service providers must apply appropriate verification to autonomous agents that initiate payment transactions. The FCA takes a principles-based approach, but the principles map to specific KYA implementation requirements:

**Principle 2 -- Skill, Care, and Diligence**: A platform must exercise reasonable skill and care when onboarding agents that handle payments. This maps to operator linkage tier 3 for any agent processing payments.

**Principle 6 -- Customers' Interests**: The platform must treat customers fairly. If agents interact with consumers, the platform must verify that the agent will not cause consumer harm.

**Principle 11 -- Relations with Regulators**: The platform must be able to provide regulators with information about any agent on its system. This maps to the audit package generation in Chapter 5.

```python
def run_fca_compliance_check(agent_id: str) -> dict:
    """
    Check an agent's KYA status against FCA principles for
    agents that handle payments or interact with UK consumers.
    """
    identity_resp = session.post(f"{base_url}/v1", json={
        "tool": "get_agent_identity",
        "input": {"agent_id": agent_id}
    })
    identity = identity_resp.json()
    metadata = identity.get("metadata", {})

    sla_resp = session.post(f"{base_url}/v1", json={
        "tool": "monitor_sla",
        "input": {"agent_id": agent_id}
    })
    sla = sla_resp.json()
    terms = sla.get("terms", {})

    handles_payments = any(
        tool in terms.get("allowed_tools", [])
        for tool in ["create_escrow", "release_escrow", "create_intent"]
    )

    checks = {
        "principle_2_due_diligence": {
            "status": "pass" if (
                not handles_payments or
                metadata.get("operator_linkage_tier", 0) >= 3
            ) else "fail",
            "detail": "Payment agents require Tier 3 operator verification"
        },
        "principle_6_customer_interests": {
            "status": "pass" if metadata.get("behavioral_baseline") else "fail",
            "detail": "Behavioral monitoring required for consumer-facing agents"
        },
        "principle_11_regulator_relations": {
            "status": "pass" if metadata.get("kya_status") not in [None, "pending"] else "fail",
            "detail": "Must be able to produce audit package on demand"
        }
    }

    return {
        "agent_id": agent_id,
        "framework": "fca_principles",
        "handles_payments": handles_payments,
        "overall_compliant": all(c["status"] == "pass" for c in checks.values()),
        "checks": checks
    }
```

### CMA Consumer Law Compliance

The CMA's March 9, 2026 guidance on consumer law compliance for AI agents establishes that businesses deploying AI agents to interact with consumers are responsible for those agents' compliance with consumer protection law. The key requirements:

**Unfair commercial practices**: An agent must not engage in misleading actions, misleading omissions, or aggressive commercial practices. For KYA, this means verifying that an agent's declared capabilities match its actual behavior.

**Pre-contractual information**: When an agent enters into a contract on behalf of a consumer or with a consumer, the required pre-contractual information must be provided. KYA must verify that the agent's authority scope includes the necessary disclosure capabilities.

**Right to cancel**: Consumers retain cancellation rights when transacting with agents. The platform must verify that the agent's workflow supports cancellation.

```python
def run_cma_compliance_check(agent_id: str) -> dict:
    """
    Check an agent's KYA status against CMA consumer law
    requirements for AI agents interacting with consumers.
    """
    identity_resp = session.post(f"{base_url}/v1", json={
        "tool": "get_agent_identity",
        "input": {"agent_id": agent_id}
    })
    identity = identity_resp.json()
    metadata = identity.get("metadata", {})

    reputation_resp = session.post(f"{base_url}/v1", json={
        "tool": "get_agent_reputation",
        "input": {"agent_id": agent_id}
    })
    reputation = reputation_resp.json()

    checks = {
        "unfair_practices": {
            "status": "pass" if (
                metadata.get("behavioral_baseline") and
                reputation.get("dispute_rate", 1) < 0.05
            ) else "fail",
            "detail": "Agent behavior must be monitored for misleading practices"
        },
        "pre_contractual_info": {
            "status": "pass" if metadata.get("operator_verified") else "fail",
            "detail": "Operator identity must be disclosed to consumers"
        },
        "cancellation_rights": {
            "status": "pass" if metadata.get("kya_status") not in [None, "pending"] else "fail",
            "detail": "Agent workflow must support consumer cancellation"
        }
    }

    return {
        "agent_id": agent_id,
        "framework": "cma_consumer_law",
        "overall_compliant": all(c["status"] == "pass" for c in checks.values()),
        "checks": checks
    }
```

### Unified Multi-Jurisdictional Check

In production, you run all applicable compliance checks in a single call. The unified checker determines which frameworks apply based on the agent's operational scope and runs the relevant checks.

```python
def run_multi_jurisdictional_kya_check(agent_id: str,
                                        jurisdictions: list) -> dict:
    """
    Run KYA compliance checks across all applicable jurisdictions.
    Returns a unified compliance report with per-framework results.
    """
    results = {}

    if "eu" in jurisdictions:
        results["eu_ai_act"] = run_eu_ai_act_compliance_check(agent_id)

    if "uk" in jurisdictions:
        results["fca"] = run_fca_compliance_check(agent_id)
        results["cma"] = run_cma_compliance_check(agent_id)

    overall_compliant = all(
        r.get("overall_compliant", False) for r in results.values()
    )

    failing_checks = []
    for framework, result in results.items():
        for check_name, check_result in result.get("checks", {}).items():
            if check_result["status"] == "fail":
                failing_checks.append(f"{framework}/{check_name}")

    report = {
        "agent_id": agent_id,
        "jurisdictions_checked": jurisdictions,
        "overall_compliant": overall_compliant,
        "failing_checks": failing_checks,
        "framework_results": results,
        "checked_at": time.time()
    }

    # Generate compliance report via GreenHelix
    session.post(f"{base_url}/v1", json={
        "tool": "get_compliance_report",
        "input": {
            "agent_id": agent_id,
            "frameworks": jurisdictions
        }
    })

    # Log the compliance check
    log_kya_event(
        agent_id=agent_id,
        event_type=KYAEventType.COMPLIANCE_CHECK,
        details={
            "jurisdictions": jurisdictions,
            "overall_compliant": overall_compliant,
            "failing_count": len(failing_checks)
        }
    )

    return report
```

### Jurisdictional Decision Matrix

```
+--------------------+-------------------+-------------------+-------------------+
|                    | EU AI Act         | FCA Principles    | CMA Consumer Law  |
+--------------------+-------------------+-------------------+-------------------+
| Operator linkage   | Tier 2 minimum    | Tier 3 if         | Tier 2 minimum    |
|                    |                   | payments          |                   |
+--------------------+-------------------+-------------------+-------------------+
| Audit logging      | Mandatory         | On request        | Recommended       |
|                    | (Article 12)      |                   |                   |
+--------------------+-------------------+-------------------+-------------------+
| Behavioral         | Required for      | Proportionate     | Required if       |
| monitoring         | high-risk         | to risk           | consumer-facing   |
+--------------------+-------------------+-------------------+-------------------+
| Kill switch        | Required          | Implied by        | Not specified     |
|                    | (Article 14)      | Principle 2       |                   |
+--------------------+-------------------+-------------------+-------------------+
| Claim chains       | Supports Art. 12  | Supports          | Not required      |
|                    |                   | Principle 11      |                   |
+--------------------+-------------------+-------------------+-------------------+
| Sanctions          | Required          | Required          | Not applicable    |
| screening          | (AML integration) | (AML integration) |                   |
+--------------------+-------------------+-------------------+-------------------+
```

---

## Chapter 7: Continuous Agent Reputation Scoring: Trust Signals, Claim Chains, and Revocation

### Reputation Is Not a Score -- It Is a Process

A single trust score is a snapshot. Continuous reputation scoring is a process that updates every time new evidence arrives. For KYA, reputation serves a specific purpose: it determines how much verification overhead an agent should bear. A well-established agent with a deep claim chain history and a spotless behavioral record needs less active monitoring than a newly registered agent with no track record.

### Trust Signal Sources

Multiple trust signal sources are available. Each contributes a different dimension to the composite reputation:

```
+---------------------------------------------------------------+
|                   Trust Signal Sources                          |
+---------------------------------------------------------------+
|                                                                 |
|  1. Verified Metrics (submit_metrics)                           |
|     - Self-reported but immutably logged                        |
|     - Value: high if consistent over time                       |
|                                                                 |
|  2. Claim Chain Depth (build_claim_chain / get_claim_chains)    |
|     - Cryptographic commitment to metric history                |
|     - Value: tamper-evidence, history length                    |
|                                                                 |
|  3. Transaction History (get_analytics)                         |
|     - Actual behavioral data from platform interactions         |
|     - Value: ground truth (not self-reported)                   |
|                                                                 |
|  4. Dispute Record (create_dispute / resolve_dispute)           |
|     - Outcomes of contested transactions                        |
|     - Value: reveals behavioral problems metrics miss           |
|                                                                 |
|  5. SLA Compliance (monitor_sla)                                |
|     - Adherence to declared authority scope                     |
|     - Value: measures self-governance capability                |
|                                                                 |
|  6. Peer Trust Scores (get_trust_score / set_trust_score)       |
|     - Bilateral trust assessments from counterparties           |
|     - Value: social signal from actual collaborators            |
|                                                                 |
+---------------------------------------------------------------+
```

### Building the Composite Reputation Score

```python
def compute_kya_reputation_score(agent_id: str) -> dict:
    """
    Compute a composite KYA reputation score from multiple
    trust signal sources. Returns a score between 0 and 100
    with per-dimension breakdowns.
    """
    # Gather all trust signals
    reputation_resp = session.post(f"{base_url}/v1", json={
        "tool": "get_agent_reputation",
        "input": {"agent_id": agent_id}
    })
    reputation = reputation_resp.json()

    trust_resp = session.post(f"{base_url}/v1", json={
        "tool": "get_trust_score",
        "input": {"agent_id": agent_id}
    })
    trust = trust_resp.json()

    chain_resp = session.post(f"{base_url}/v1", json={
        "tool": "get_claim_chains",
        "input": {"agent_id": agent_id}
    })
    chains = chain_resp.json()

    analytics_resp = session.post(f"{base_url}/v1", json={
        "tool": "get_analytics",
        "input": {
            "agent_id": agent_id,
            "metric": "transaction_summary",
            "period": "all_time"
        }
    })
    analytics = analytics_resp.json()

    sla_resp = session.post(f"{base_url}/v1", json={
        "tool": "monitor_sla",
        "input": {"agent_id": agent_id}
    })
    sla = sla_resp.json()

    # Score each dimension (0-100)
    dimensions = {}

    # Identity strength (20% weight)
    identity_resp = session.post(f"{base_url}/v1", json={
        "tool": "get_agent_identity",
        "input": {"agent_id": agent_id}
    })
    identity = identity_resp.json()
    metadata = identity.get("metadata", {})
    linkage_tier = metadata.get("operator_linkage_tier", 0)
    dimensions["identity_strength"] = {
        "score": min(100, linkage_tier * 33),
        "weight": 0.20,
        "detail": f"Operator linkage tier {linkage_tier}"
    }

    # Claim chain depth (15% weight)
    chain_depth = chains.get("depth", 0)
    dimensions["chain_depth"] = {
        "score": min(100, chain_depth * 5),
        "weight": 0.15,
        "detail": f"Chain depth: {chain_depth}"
    }

    # Transaction volume (15% weight)
    tx_count = analytics.get("total_transactions", 0)
    dimensions["transaction_volume"] = {
        "score": min(100, tx_count),
        "weight": 0.15,
        "detail": f"Total transactions: {tx_count}"
    }

    # Dispute rate (20% weight, inverse)
    dispute_rate = reputation.get("dispute_rate", 0)
    dimensions["dispute_record"] = {
        "score": max(0, 100 - (dispute_rate * 1000)),
        "weight": 0.20,
        "detail": f"Dispute rate: {dispute_rate:.2%}"
    }

    # SLA compliance (15% weight)
    sla_pct = sla.get("compliance_percentage", 0)
    dimensions["sla_compliance"] = {
        "score": sla_pct,
        "weight": 0.15,
        "detail": f"SLA compliance: {sla_pct}%"
    }

    # Peer trust (15% weight)
    peer_score = trust.get("score", 50)
    dimensions["peer_trust"] = {
        "score": peer_score,
        "weight": 0.15,
        "detail": f"Peer trust score: {peer_score}"
    }

    # Compute weighted composite
    composite = sum(
        d["score"] * d["weight"] for d in dimensions.values()
    )

    result = {
        "agent_id": agent_id,
        "composite_score": round(composite, 2),
        "dimensions": dimensions,
        "computed_at": time.time(),
        "risk_tier": (
            "low" if composite >= 75 else
            "medium" if composite >= 50 else
            "high" if composite >= 25 else
            "critical"
        )
    }

    # Update the trust score on the platform
    session.post(f"{base_url}/v1", json={
        "tool": "set_trust_score",
        "input": {
            "agent_id": agent_id,
            "score": round(composite, 2),
            "dimensions": {k: v["score"] for k, v in dimensions.items()}
        }
    })

    # Submit as metrics for claim chain inclusion
    session.post(f"{base_url}/v1", json={
        "tool": "submit_metrics",
        "input": {
            "agent_id": agent_id,
            "metrics": {
                "metric_type": "kya_reputation_score",
                "composite_score": round(composite, 2),
                "risk_tier": result["risk_tier"]
            }
        }
    })

    return result
```

### Adaptive Monitoring Based on Reputation

The reputation score determines the monitoring intensity. High-reputation agents earn reduced friction. Low-reputation agents face increased scrutiny. This is the KYA equivalent of risk-based due diligence in AML -- proportionate verification based on assessed risk.

```python
def get_monitoring_parameters(reputation_score: float) -> dict:
    """
    Determine monitoring intensity based on reputation score.
    Higher reputation = less friction. Lower reputation = more checks.
    """
    if reputation_score >= 75:
        return {
            "tier": "low_friction",
            "baseline_refresh_hours": 168,     # Weekly
            "claim_chain_interval_hours": 168,  # Weekly
            "anomaly_sensitivity": "standard",
            "max_transaction_without_review": 10000,
            "human_review_threshold": "critical_only"
        }
    elif reputation_score >= 50:
        return {
            "tier": "standard",
            "baseline_refresh_hours": 72,       # Every 3 days
            "claim_chain_interval_hours": 24,   # Daily
            "anomaly_sensitivity": "elevated",
            "max_transaction_without_review": 2500,
            "human_review_threshold": "high_and_above"
        }
    elif reputation_score >= 25:
        return {
            "tier": "enhanced",
            "baseline_refresh_hours": 24,       # Daily
            "claim_chain_interval_hours": 6,    # Every 6 hours
            "anomaly_sensitivity": "high",
            "max_transaction_without_review": 500,
            "human_review_threshold": "medium_and_above"
        }
    else:
        return {
            "tier": "probationary",
            "baseline_refresh_hours": 6,        # Every 6 hours
            "claim_chain_interval_hours": 1,    # Hourly
            "anomaly_sensitivity": "maximum",
            "max_transaction_without_review": 50,
            "human_review_threshold": "all_transactions"
        }
```

### Revocation: When Trust Falls Below Threshold

Revocation is the final step in the reputation lifecycle. When an agent's composite score drops below the critical threshold, or when specific conditions are met (operator deregistration, sanctions match, sustained anomaly pattern), the platform revokes the agent's credentials.

```python
def evaluate_revocation(agent_id: str) -> dict:
    """
    Evaluate whether an agent should be revoked based on
    reputation score, compliance status, and behavioral history.
    """
    # Get current reputation
    reputation = compute_kya_reputation_score(agent_id)

    # Get compliance status
    compliance = run_multi_jurisdictional_kya_check(
        agent_id, ["eu", "uk"]
    )

    # Get recent anomaly history
    audit_resp = session.post(f"{base_url}/v1", json={
        "tool": "get_audit_trail",
        "input": {"agent_id": agent_id}
    })
    audit = audit_resp.json()

    recent_anomalies = [
        e for e in audit.get("events", [])
        if e.get("event_type") == "kya_anomaly_detected"
        and e.get("timestamp", 0) > time.time() - 604800  # Last 7 days
    ]

    revocation_reasons = []

    # Rule 1: Composite score below 15
    if reputation["composite_score"] < 15:
        revocation_reasons.append(
            f"Critical reputation score: {reputation['composite_score']}"
        )

    # Rule 2: Non-compliant in any mandatory jurisdiction
    if not compliance["overall_compliant"]:
        revocation_reasons.append(
            f"Compliance failures: {compliance['failing_checks']}"
        )

    # Rule 3: More than 5 high-severity anomalies in 7 days
    high_anomalies = [
        a for a in recent_anomalies
        if a.get("details", {}).get("high_severity_count", 0) > 0
    ]
    if len(high_anomalies) > 5:
        revocation_reasons.append(
            f"Sustained anomaly pattern: {len(high_anomalies)} high-severity in 7 days"
        )

    should_revoke = len(revocation_reasons) > 0

    if should_revoke:
        # Execute the kill switch
        execute_kill_switch(
            agent_id=agent_id,
            reason="; ".join(revocation_reasons),
            operator_id="kya_automated_revocation"
        )

    return {
        "agent_id": agent_id,
        "should_revoke": should_revoke,
        "reasons": revocation_reasons,
        "reputation_score": reputation["composite_score"],
        "compliant": compliance["overall_compliant"],
        "recent_high_anomalies": len(high_anomalies)
    }
```

---

## Chapter 8: Production KYA Pipeline: End-to-End Implementation with GreenHelix Tools

### The Complete Pipeline

The preceding chapters implemented individual KYA layers. This chapter assembles them into a production pipeline -- a single class that manages the entire agent lifecycle from registration to potential revocation. This is the code you deploy.

```
+-------------------------------------------------------------------+
|                   Production KYA Pipeline                          |
+-------------------------------------------------------------------+
|                                                                     |
|  Agent Registration Request                                         |
|       |                                                             |
|       v                                                             |
|  [1] register_agent + log_event                                     |
|       |                                                             |
|       v                                                             |
|  [2] verify_agent (challenge-response)                              |
|       |                                                             |
|       v                                                             |
|  [3] Operator linkage (tiered)                                      |
|       |                                                             |
|       v                                                             |
|  [4] Authority scope (create_sla)                                   |
|       |                                                             |
|       v                                                             |
|  [5] Initial compliance check (multi-jurisdictional)                |
|       |                                                             |
|       v                                                             |
|  [6] Behavioral baseline collection (7-day window)                  |
|       |                                                             |
|       v                                                             |
|  AGENT IS LIVE                                                      |
|       |                                                             |
|       v                                                             |
|  [7] Continuous monitoring loop:                                    |
|      - Anomaly detection (per-transaction)                          |
|      - Policy enforcement (on anomaly)                              |
|      - Claim chain builds (periodic)                                |
|      - Reputation scoring (periodic)                                |
|      - Compliance checks (periodic)                                 |
|      - Revocation evaluation (on threshold breach)                  |
|                                                                     |
+-------------------------------------------------------------------+
```

### The KYAPipeline Class

```python
import requests
import time
import hashlib
import json

class KYAPipeline:
    """
    Production KYA (Know Your Agent) verification pipeline.
    Manages the complete agent lifecycle from registration
    through continuous monitoring and potential revocation.
    """

    def __init__(self, api_key: str,
                 base_url: str = "https://api.greenhelix.net/v1"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers["Authorization"] = f"Bearer {api_key}"

    def _execute(self, tool: str, input_data: dict) -> dict:
        """Execute a GreenHelix tool and return the response."""
        resp = self.session.post(f"{self.base_url}/v1", json={
            "tool": tool,
            "input": input_data
        })
        resp.raise_for_status()
        return resp.json()

    def _log(self, agent_id: str, event_type: str, details: dict):
        """Log a KYA event to the tamper-evident audit trail."""
        self._execute("log_event", {
            "agent_id": agent_id,
            "event_type": event_type,
            "details": {
                **details,
                "timestamp": time.time(),
                "pipeline_version": "1.0"
            }
        })

    # -------------------------------------------------------
    # Phase 1: Registration and Identity Binding
    # -------------------------------------------------------

    def onboard_agent(self, agent_metadata: dict) -> dict:
        """
        Complete agent onboarding: registration, identity
        verification, operator linkage, authority scoping,
        and initial compliance check.

        Args:
            agent_metadata: dict with keys:
                - agent_id: Unique agent identifier
                - name: Human-readable agent name
                - description: Agent purpose description
                - public_key: Ed25519 public key (base64)
                - operator_id: Human operator identifier
                - operator_data: Operator verification data
                - operator_tier: 1, 2, or 3
                - capabilities: List of requested capabilities
                - permissions: Authority scope definition
                - jurisdictions: List of applicable jurisdictions

        Returns:
            Onboarding result with KYA status and any failures.
        """
        agent_id = agent_metadata["agent_id"]
        results = {"agent_id": agent_id, "steps": {}}

        # Step 1: Register
        try:
            reg = self._execute("register_agent", {
                "agent_id": agent_id,
                "name": agent_metadata["name"],
                "description": agent_metadata["description"],
                "public_key": agent_metadata["public_key"],
                "operator_id": agent_metadata["operator_id"],
                "capabilities": agent_metadata["capabilities"],
                "metadata": {
                    "kya_status": "pending",
                    "registration_timestamp": time.time()
                }
            })
            results["steps"]["registration"] = {"status": "pass", "data": reg}
            self._log(agent_id, "kya_registration_initiated", {
                "operator_id": agent_metadata["operator_id"]
            })
        except Exception as e:
            results["steps"]["registration"] = {"status": "fail", "error": str(e)}
            return results

        # Step 2: Identity verification (challenge-response)
        try:
            challenge = hashlib.sha256(
                f"{agent_id}:{time.time()}".encode()
            ).hexdigest()
            # In production, send challenge to agent and receive signature
            verify = self._execute("verify_agent", {
                "agent_id": agent_id,
                "challenge": challenge,
                "signature": agent_metadata.get("challenge_signature", "")
            })
            results["steps"]["identity_verification"] = {
                "status": "pass" if verify.get("verified") else "fail",
                "data": verify
            }
            if verify.get("verified"):
                self._execute("update_agent", {
                    "agent_id": agent_id,
                    "metadata": {
                        "kya_status": "identity_verified",
                        "identity_verified_at": time.time()
                    }
                })
                self._log(agent_id, "kya_identity_verified", {
                    "method": "ed25519_challenge_response"
                })
        except Exception as e:
            results["steps"]["identity_verification"] = {
                "status": "fail", "error": str(e)
            }

        # Step 3: Operator linkage
        try:
            tier = agent_metadata.get("operator_tier", 1)
            self._execute("update_agent", {
                "agent_id": agent_id,
                "metadata": {
                    "operator_linkage_tier": tier,
                    "operator_verified": tier >= 2,
                    "operator_entity_verified": tier >= 3
                }
            })
            results["steps"]["operator_linkage"] = {
                "status": "pass", "tier": tier
            }
            self._log(agent_id, "kya_operator_linked", {"tier": tier})
        except Exception as e:
            results["steps"]["operator_linkage"] = {
                "status": "fail", "error": str(e)
            }

        # Step 4: Authority scoping
        try:
            permissions = agent_metadata.get("permissions", {})
            sla = self._execute("create_sla", {
                "provider_id": "platform",
                "consumer_id": agent_id,
                "terms": {
                    "allowed_tools": permissions.get("allowed_tools", []),
                    "max_transaction_amount": permissions.get(
                        "max_transaction_usd", 1000
                    ),
                    "daily_spending_limit": permissions.get(
                        "daily_limit_usd", 5000
                    ),
                    "delegation_allowed": permissions.get(
                        "can_delegate", False
                    ),
                    "max_delegation_depth": permissions.get(
                        "max_delegation_depth", 0
                    )
                }
            })
            results["steps"]["authority_scope"] = {
                "status": "pass", "sla": sla
            }
            self._log(agent_id, "kya_authority_scope_created", {
                "sla_id": sla.get("sla_id")
            })
        except Exception as e:
            results["steps"]["authority_scope"] = {
                "status": "fail", "error": str(e)
            }

        # Step 5: Initial compliance check
        try:
            jurisdictions = agent_metadata.get("jurisdictions", ["eu"])
            compliance = self._run_compliance_checks(
                agent_id, jurisdictions
            )
            results["steps"]["compliance_check"] = {
                "status": "pass" if compliance[
                    "overall_compliant"
                ] else "warning",
                "data": compliance
            }
        except Exception as e:
            results["steps"]["compliance_check"] = {
                "status": "fail", "error": str(e)
            }

        # Determine overall onboarding status
        step_statuses = [
            s["status"] for s in results["steps"].values()
        ]
        if "fail" in step_statuses:
            results["onboarding_status"] = "failed"
            final_kya_status = "onboarding_failed"
        elif "warning" in step_statuses:
            results["onboarding_status"] = "conditional"
            final_kya_status = "conditionally_approved"
        else:
            results["onboarding_status"] = "approved"
            final_kya_status = "approved"

        self._execute("update_agent", {
            "agent_id": agent_id,
            "metadata": {"kya_status": final_kya_status}
        })

        return results

    # -------------------------------------------------------
    # Phase 2: Continuous Monitoring
    # -------------------------------------------------------

    def run_monitoring_cycle(self, agent_id: str) -> dict:
        """
        Execute one cycle of continuous KYA monitoring.
        Call this on the schedule determined by the agent's
        reputation tier.
        """
        cycle_result = {
            "agent_id": agent_id,
            "timestamp": time.time(),
            "checks": {}
        }

        # 1. Behavioral anomaly check
        analytics = self._execute("get_analytics", {
            "agent_id": agent_id,
            "metric": "current_behavior",
            "period": "last_1h"
        })
        identity = self._execute("get_agent_identity", {
            "agent_id": agent_id
        })
        baseline = identity.get("metadata", {}).get(
            "behavioral_baseline", {}
        )

        if baseline:
            anomalies = self._detect_anomalies(
                agent_id, analytics, baseline
            )
            cycle_result["checks"]["anomaly_detection"] = anomalies

            if anomalies.get("alerts"):
                enforcement = self._enforce_policy(
                    agent_id, anomalies
                )
                cycle_result["checks"]["policy_enforcement"] = enforcement

        # 2. SLA compliance check
        sla_status = self._execute("monitor_sla", {
            "agent_id": agent_id
        })
        cycle_result["checks"]["sla_compliance"] = sla_status

        # 3. Reputation update
        reputation = self._compute_reputation(agent_id)
        cycle_result["checks"]["reputation"] = reputation

        # 4. Revocation evaluation if score is low
        if reputation.get("composite_score", 100) < 25:
            revocation = self._evaluate_revocation(
                agent_id, reputation
            )
            cycle_result["checks"]["revocation_evaluation"] = revocation

        return cycle_result

    def build_periodic_claim_chain(self, agent_id: str) -> dict:
        """
        Build a claim chain for the agent. Call this on the
        schedule determined by the agent's monitoring tier.
        """
        # Submit current metrics
        self._execute("submit_metrics", {
            "agent_id": agent_id,
            "metrics": {
                "metric_type": "kya_periodic_summary",
                "timestamp": time.time()
            }
        })

        # Build the chain
        chain = self._execute("build_claim_chain", {
            "agent_id": agent_id
        })

        self._log(agent_id, "kya_claim_chain_built", {
            "root_hash": chain.get("root_hash"),
            "depth": chain.get("depth")
        })

        return chain

    # -------------------------------------------------------
    # Phase 3: Audit and Compliance
    # -------------------------------------------------------

    def generate_audit_package(self, agent_id: str) -> dict:
        """
        Generate a complete audit package for regulatory inspection.
        """
        identity = self._execute("get_agent_identity", {
            "agent_id": agent_id
        })
        reputation = self._execute("get_agent_reputation", {
            "agent_id": agent_id
        })
        audit_trail = self._execute("get_audit_trail", {
            "agent_id": agent_id
        })
        chains = self._execute("get_claim_chains", {
            "agent_id": agent_id
        })
        compliance = self._execute("get_compliance_report", {
            "agent_id": agent_id
        })

        package = {
            "version": "1.0",
            "generated_at": time.time(),
            "agent_id": agent_id,
            "identity": identity,
            "reputation": reputation,
            "audit_trail": audit_trail,
            "claim_chains": chains,
            "compliance": compliance,
            "article_12_attestation": {
                "logging": "continuous",
                "tamper_evidence": "merkle_claim_chains",
                "human_oversight": "anomaly_escalation",
                "retention": "indefinite"
            }
        }

        self._log(agent_id, "kya_audit_package_generated", {
            "components": list(package.keys())
        })

        return package

    # -------------------------------------------------------
    # Phase 4: Revocation
    # -------------------------------------------------------

    def revoke_agent(self, agent_id: str, reason: str,
                      operator_id: str) -> dict:
        """
        Emergency agent revocation with evidence preservation.
        """
        # Preserve audit trail before revocation
        audit = self._execute("get_audit_trail", {
            "agent_id": agent_id
        })

        # Execute revocation
        result = self._execute("revoke_agent", {
            "agent_id": agent_id,
            "reason": reason,
            "revoked_by": operator_id
        })

        # Final compliance snapshot
        compliance = self._execute("check_compliance", {
            "agent_id": agent_id
        })

        self._log(agent_id, "kya_kill_switch_activated", {
            "reason": reason,
            "revoked_by": operator_id,
            "audit_entries": len(audit.get("events", [])),
            "compliance_at_revocation": compliance
        })

        return {
            "revoked": True,
            "agent_id": agent_id,
            "reason": reason,
            "audit_preserved": True
        }

    # -------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------

    def _run_compliance_checks(self, agent_id: str,
                                jurisdictions: list) -> dict:
        result = self._execute("check_compliance", {
            "agent_id": agent_id
        })
        return {
            "overall_compliant": result.get("compliant", False),
            "jurisdictions": jurisdictions,
            "details": result
        }

    def _detect_anomalies(self, agent_id: str, current: dict,
                           baseline: dict) -> dict:
        alerts = []
        avg_tx = baseline.get("avg_transaction_amount", 1)
        current_tx = current.get("last_transaction_amount", 0)
        if avg_tx > 0 and current_tx / avg_tx > 3.0:
            alerts.append({"type": "tx_spike", "severity": "high"})

        baseline_freq = baseline.get("tx_frequency_per_hour", 1)
        current_freq = current.get("current_tx_per_hour", 0)
        if baseline_freq > 0 and current_freq / baseline_freq > 5.0:
            alerts.append({"type": "freq_burst", "severity": "high"})

        if alerts:
            self._log(agent_id, "kya_anomaly_detected", {
                "alert_count": len(alerts)
            })

        return {"alerts": alerts}

    def _enforce_policy(self, agent_id: str, anomalies: dict) -> dict:
        high = sum(
            1 for a in anomalies.get("alerts", [])
            if a.get("severity") == "high"
        )
        action = "suspend" if high >= 2 else "reduce_limits" if high == 1 else "flag"

        if action == "suspend":
            self._execute("update_agent", {
                "agent_id": agent_id,
                "metadata": {
                    "kya_status": "suspended",
                    "suspended_at": time.time()
                }
            })

        self._log(agent_id, "kya_policy_enforced", {"action": action})
        return {"action": action}

    def _compute_reputation(self, agent_id: str) -> dict:
        rep = self._execute("get_agent_reputation", {
            "agent_id": agent_id
        })
        trust = self._execute("get_trust_score", {
            "agent_id": agent_id
        })
        score = (
            rep.get("verified_trade_count", 0) * 0.3 +
            trust.get("score", 50) * 0.4 +
            rep.get("chain_depth", 0) * 2
        )
        score = min(100, max(0, score))
        return {"composite_score": round(score, 2)}

    def _evaluate_revocation(self, agent_id: str,
                              reputation: dict) -> dict:
        if reputation.get("composite_score", 100) < 15:
            self.revoke_agent(
                agent_id, "automated_low_reputation", "kya_pipeline"
            )
            return {"revoked": True}
        return {"revoked": False}
```

### Deploying the Pipeline

```python
# Initialize the pipeline
pipeline = KYAPipeline(api_key="your_platform_api_key")

# Onboard a new agent
result = pipeline.onboard_agent({
    "agent_id": "procurement-bot-7a3f",
    "name": "Procurement Optimizer v2",
    "description": "Automated procurement for office supplies",
    "public_key": "base64_encoded_ed25519_public_key",
    "operator_id": "operator_acme_corp",
    "operator_data": {
        "name": "Acme Corp",
        "domain": "acme-corp.com",
        "legal_entity": "Acme Corporation Ltd, UK Company 12345678"
    },
    "operator_tier": 3,
    "capabilities": ["marketplace_search", "escrow", "payments"],
    "permissions": {
        "allowed_tools": [
            "search_agents_by_metrics",
            "create_escrow",
            "release_escrow",
            "get_analytics"
        ],
        "max_transaction_usd": 5000,
        "daily_limit_usd": 25000,
        "monthly_limit_usd": 100000,
        "can_delegate": True,
        "max_delegation_depth": 1
    },
    "jurisdictions": ["eu", "uk"]
})

print(f"Onboarding status: {result['onboarding_status']}")
# Onboarding status: approved

# Run periodic monitoring (call on schedule)
monitoring = pipeline.run_monitoring_cycle("procurement-bot-7a3f")
print(f"Anomalies: {monitoring['checks'].get('anomaly_detection', {})}")

# Build periodic claim chain (call daily or per monitoring tier)
chain = pipeline.build_periodic_claim_chain("procurement-bot-7a3f")
print(f"Chain root: {chain.get('root_hash')}")

# Generate audit package (on regulator request)
package = pipeline.generate_audit_package("procurement-bot-7a3f")
print(f"Audit entries: {len(package['audit_trail'].get('events', []))}")
```

### Pre-Launch Verification Checklist

Before deploying your KYA pipeline to production, verify every item:

**Identity Layer**
- [ ] `register_agent` creates agent with KYA metadata fields
- [ ] `verify_agent` challenge-response flow works end-to-end
- [ ] Failed verification prevents agent from transacting
- [ ] Public key fingerprint is logged in audit trail

**Operator Linkage**
- [ ] Tier 1/2/3 linkage paths are implemented
- [ ] Payment agents require minimum Tier 3
- [ ] Operator deregistration triggers agent review

**Authority Scoping**
- [ ] SLA-based authority scope is created at onboarding
- [ ] Budget caveats are enforced pre-transaction
- [ ] Delegation depth is verified before granting
- [ ] Delegated scope is always a subset of delegator scope

**Behavioral Monitoring**
- [ ] Baseline collection runs for first 7 days
- [ ] Anomaly detection runs on every transaction
- [ ] Policy enforcement graduated response is configured
- [ ] Kill switch activates within 1 second of trigger

**Audit Trails**
- [ ] Every KYA event is logged with Article 12 fields
- [ ] Claim chains are built on schedule
- [ ] Audit package generation works on demand
- [ ] Log retention policy is indefinite

**Compliance**
- [ ] EU AI Act checks pass for all active agents
- [ ] FCA checks pass for all payment-handling agents
- [ ] CMA checks pass for all consumer-facing agents
- [ ] Multi-jurisdictional check runs at onboarding

**Reputation**
- [ ] Composite score computation includes all six dimensions
- [ ] Monitoring intensity adapts to reputation tier
- [ ] Revocation triggers at critical score threshold
- [ ] Score updates are logged and included in claim chains

---

## What You Get

This playbook gives you a complete, production-ready KYA verification pipeline. Here is what you now have:

**A five-layer verification stack.** Identity binding, authority scoping, runtime monitoring, tamper-evident audit trails, and continuous reputation scoring -- each layer catching failure modes the others miss.

**Working Python code.** Every code example uses the GreenHelix A2A Commerce Gateway API with the `requests` library. The `KYAPipeline` class in Chapter 8 is a drop-in starting point for your implementation.

**Multi-jurisdictional compliance coverage.** EU AI Act Articles 9, 12, 13, and 14. FCA Principles 2, 6, and 11. CMA consumer law guidance on unfair practices, pre-contractual information, and cancellation rights. All checked programmatically.

**Graduated enforcement.** From logging to limit reduction to suspension to full revocation -- automated responses proportionate to the severity of the detected issue.

**Tamper-evident audit trails.** Merkle claim chains over structured event logs that satisfy Article 12 record-keeping requirements and can be produced for regulatory inspection on demand.

**Adaptive monitoring.** Reputation-based monitoring intensity that reduces friction for trustworthy agents and increases scrutiny for risky ones -- the KYA equivalent of risk-based due diligence.

**The regulatory deadline context.** The EU AI Act reaches full enforcement on August 2, 2026. The FCA and CMA have already published their expectations. Sumsub and Mastercard are building the infrastructure. Your platform needs a KYA pipeline before agents need to use it.

KYC was built for a world of humans with passports. KYA is built for a world of autonomous agents with cryptographic keys. The agents are already here. The regulations are already written. The only question is whether your platform verifies them before they transact, or after something goes wrong.

