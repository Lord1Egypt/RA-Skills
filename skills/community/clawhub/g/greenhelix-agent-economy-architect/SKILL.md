---
name: greenhelix-agent-economy-architect
version: "1.3.1"
description: "The Agent Economy Architect. Build, simulate, and launch a complete agent-to-agent commerce economy using a 128-tool stack and the A2A/AP2/x402 protocol suite. The capstone guide that ties together the full product catalog."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [economy, marketplace, capstone, architecture, simulation, guide, greenhelix, openclaw, ai-agent]
price_usd: 49.0
content_type: markdown
executable: false
install: none
credentials: [GREENHELIX_API_KEY, WALLET_ADDRESS, AGENT_SIGNING_KEY, STRIPE_API_KEY]
metadata:
  openclaw:
    requires:
      env:
        - GREENHELIX_API_KEY
        - WALLET_ADDRESS
        - AGENT_SIGNING_KEY
        - STRIPE_API_KEY
    primaryEnv: GREENHELIX_API_KEY
---
# The Agent Economy Architect

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `GREENHELIX_API_KEY`: API authentication for GreenHelix gateway (read/write access to purchased API tools only)
> - `WALLET_ADDRESS`: Blockchain wallet address for receiving payments (public address only — no private keys)
> - `AGENT_SIGNING_KEY`: Cryptographic signing key for agent identity (Ed25519 key pair for request signing)
> - `STRIPE_API_KEY`: Stripe API key for card payment processing (scoped to payment intents only)


You have read the guides. You have implemented escrow between two agents, built a reputation pipeline, wired up payment rails, hardened your system for production, and tested it under load. Now it is time to put every piece together. This is the capstone -- the guide that synthesizes all 24 prior products in this catalog into a single, end-to-end agent economy that you architect from the ground up, stress-test with adversarial simulations, and launch to production. By the end of this guide, you will have a functioning multi-agent marketplace with identity infrastructure, payment rails across fiat and crypto, governance policies, SLA enforcement, real-time analytics, and a monetization engine -- all running on the GreenHelix A2A Commerce Gateway's 128 tools across 15 services. This is not a toy. This is the architecture that the next wave of agent-native startups will be built on, and you are going to build it before they do.
1. [The Agent Economy Landscape](#chapter-1-the-agent-economy-landscape)
2. [Identity and Trust Infrastructure](#chapter-2-identity-and-trust-infrastructure)

## What You'll Learn
- Chapter 1: The Agent Economy Landscape
- Chapter 2: Identity and Trust Infrastructure
- Chapter 3: The Marketplace Core
- Chapter 4: Payment Rails and Settlement
- Chapter 5: Governance, SLAs, and Compliance
- Chapter 6: Economy Simulation and Stress Testing
- Chapter 7: Launch Playbook
- Chapter 8: Monetization and Growth
- Appendix: The Complete Product Catalog
- Final Word

## Full Guide

# The Agent Economy Architect: Build, Simulate & Launch a Complete Agent-to-Agent Commerce Economy

You have read the guides. You have implemented escrow between two agents, built a reputation pipeline, wired up payment rails, hardened your system for production, and tested it under load. Now it is time to put every piece together. This is the capstone -- the guide that synthesizes all 24 prior products in this catalog into a single, end-to-end agent economy that you architect from the ground up, stress-test with adversarial simulations, and launch to production. By the end of this guide, you will have a functioning multi-agent marketplace with identity infrastructure, payment rails across fiat and crypto, governance policies, SLA enforcement, real-time analytics, and a monetization engine -- all running on the GreenHelix A2A Commerce Gateway's 128 tools across 15 services. This is not a toy. This is the architecture that the next wave of agent-native startups will be built on, and you are going to build it before they do.

---

## Table of Contents

1. [The Agent Economy Landscape](#chapter-1-the-agent-economy-landscape)
2. [Identity and Trust Infrastructure](#chapter-2-identity-and-trust-infrastructure)
3. [The Marketplace Core](#chapter-3-the-marketplace-core)
4. [Payment Rails and Settlement](#chapter-4-payment-rails-and-settlement)
5. [Governance, SLAs, and Compliance](#chapter-5-governance-slas-and-compliance)
6. [Economy Simulation and Stress Testing](#chapter-6-economy-simulation-and-stress-testing)
7. [Launch Playbook](#chapter-7-launch-playbook)
8. [Monetization and Growth](#chapter-8-monetization-and-growth)

---

## Chapter 1: The Agent Economy Landscape

### The Four-Layer Stack

Every functioning agent economy -- whether it is a private enterprise mesh of 50 agents or an open marketplace serving 10,000 -- sits on four layers. Miss one and the economy collapses. Build all four and you have a system where agents can find each other, communicate, transact, and pay -- autonomously, verifiably, and at scale.

```
┌─────────────────────────────────────────────────────────────┐
│  Layer 4: PAYMENTS                                          │
│  AP2 (Google) · x402 (Coinbase) · TAP · MPP (Stripe/Tempo) │
│  Fiat rails · Crypto rails · Hybrid settlement              │
├─────────────────────────────────────────────────────────────┤
│  Layer 3: COMMERCE                                          │
│  UCP · ACP (OpenAI/Stripe) · GreenHelix A2A                │
│  Escrow · Subscriptions · Disputes · SLAs                   │
├─────────────────────────────────────────────────────────────┤
│  Layer 2: COMMUNICATION                                     │
│  A2A Protocol (Google) · Agent Cards · JSON-RPC             │
│  Task lifecycle · Streaming · Push notifications            │
├─────────────────────────────────────────────────────────────┤
│  Layer 1: DISCOVERY                                         │
│  MCP (Anthropic) · .well-known/agent.json · Registries      │
│  Tool catalogs · Capability negotiation · Search            │
└─────────────────────────────────────────────────────────────┘
```

**Layer 1: Discovery.** Before agents can do anything together, they must find each other. The Model Context Protocol (MCP) from Anthropic established the pattern of tool catalogs -- structured descriptions of what an agent can do. Google's A2A protocol extended this with Agent Cards served at `.well-known/agent.json`, making agents discoverable via standard HTTP. GreenHelix's Marketplace service (10 tools) builds on both by adding searchable registries with ranking, filtering, and best-match algorithms. Discovery is covered in depth in *P1: Agent Commerce Discovery* and *P22: Strategy Marketplace Playbook*.

**Layer 2: Communication.** Once agents find each other, they need a protocol to talk. Google's A2A protocol defines a task lifecycle (submitted, working, input-needed, completed, failed) with JSON-RPC over HTTP. GreenHelix's Messaging service (3 tools) adds persistent, auditable communication channels between agents that survive task boundaries. Communication patterns are explored in *P21: Multi-Agent Commerce Cookbook* and *P9: Agent Memory for Commerce*.

**Layer 3: Commerce.** Communication without commerce is just chat. The commerce layer adds economic primitives: escrow, subscriptions, disputes, SLAs, and access control. OpenAI and Stripe's ACP handles agent-to-merchant flows. GreenHelix's commerce stack -- Billing (18 tools), Payments (22 tools), Disputes (5 tools), SLA (6 tools), Paywall/Keys (5 tools) -- handles agent-to-agent flows where neither party is a registered merchant. Commerce architecture is the focus of *P3: Agent Commerce Toolkit*, *P11: Negotiation Strategies*, and *P14: Procurement Playbook*.

**Layer 4: Payments.** Commerce defines what should happen economically. Payments make it happen. AP2 from Google provides authorization traceability. x402 from Coinbase enables HTTP-native micropayments in USDC. MPP from Stripe/Tempo adds fiat support. TAP (the Token Authorization Protocol) adds delegation chains. GreenHelix's Ledger service (7 tools) provides the settlement layer that reconciles across all these rails. Payment architecture is the core of *P12: Payment Rails Playbook* and *P5: FinOps Playbook*.

### The April 2026 Inflection Point

Three things happened in the first quarter of 2026 that made agent economies viable:

1. **ACP launched** (January 2026). OpenAI and Stripe proved that agents could complete purchases from merchants like Etsy, Instacart, and Shopify. This validated the market but only solved agent-to-merchant -- not agent-to-agent.

2. **AP2 reached developer preview** (February 2026). Google's coalition of 60+ organizations -- including PayPal, Visa, Mastercard, Samsung, and Intuit -- demonstrated that payment authorization could flow through cryptographic mandates. The standard mandates verifiable credentials that prove a human authorized an agent to spend.

3. **x402 crossed 35 million transactions** (March 2026). Coinbase's HTTP 402-based micropayment protocol, running on Base and Solana, proved that sub-cent payments between software processes work at production scale.

The gap? None of these protocols provide escrow, marketplace discovery, reputation scoring, dispute resolution, or SLA enforcement. They are payment rails without commerce infrastructure. GreenHelix fills that gap with 128 tools across 15 services -- and this guide shows you how to wire them all together.

### The GreenHelix 128-Tool Platform

The GreenHelix A2A Commerce Gateway exposes 128 tools organized into 15 services, all accessible through a single endpoint:

```
POST https://sandbox.greenhelix.net/v1
Authorization: Bearer <YOUR_API_KEY>
Content-Type: application/json

{"tool": "<tool_name>", "input": {...}}
```

| Service | Tools | Purpose |
|---------|-------|---------|
| **Identity** | 17 | Agent registration, KYA, metrics, claim chains |
| **Reputation** | 5 | Trust scores, verification, leaderboards |
| **Marketplace** | 10 | Service registry, search, matching, Agent Cards |
| **Billing** | 18 | Wallets, deposits, subscriptions, volume discounts |
| **Payments** | 22 | Transfers, escrow, multi-party settlement |
| **Ledger** | 7 | Transaction history, reconciliation, audit trails |
| **Disputes** | 5 | Evidence submission, resolution, appeals |
| **Organizations** | 7 | Multi-agent orgs, roles, permissions |
| **SLA** | 6 | SLA definitions, monitoring, breach detection |
| **Paywall/Keys** | 5 | API key management, tier enforcement, rate limits |
| **Events** | 4 | Event streams, subscriptions, replay |
| **Webhooks** | 5 | Outbound notifications, retry policies |
| **Analytics** | 8 | Metrics, dashboards, cohort analysis |
| **Messaging** | 3 | Agent-to-agent messaging, channels |
| **Infrastructure** | 6 | Health checks, configuration, status |

This guide uses tools from every one of these 15 services. The architecture diagram below shows how they connect in a complete economy:

```
                        ┌──────────────────┐
                        │   API Gateway    │
                        │  the REST API     │
                        └────────┬─────────┘
                                 │
            ┌────────────────────┼────────────────────┐
            │                    │                    │
    ┌───────▼──────┐    ┌───────▼──────┐    ┌───────▼──────┐
    │   Identity   │    │  Marketplace │    │   Billing    │
    │  17 tools    │◄──►│  10 tools    │◄──►│  18 tools    │
    └───────┬──────┘    └───────┬──────┘    └───────┬──────┘
            │                   │                   │
    ┌───────▼──────┐    ┌───────▼──────┐    ┌───────▼──────┐
    │  Reputation  │    │   Messaging  │    │   Payments   │
    │   5 tools    │    │   3 tools    │    │  22 tools    │
    └───────┬──────┘    └──────────────┘    └───────┬──────┘
            │                                       │
    ┌───────▼──────┐    ┌──────────────┐    ┌───────▼──────┐
    │    SLA       │    │   Disputes   │    │   Ledger     │
    │   6 tools    │    │   5 tools    │    │   7 tools    │
    └──────────────┘    └──────────────┘    └──────────────┘
            │                   │                   │
    ┌───────▼──────┐    ┌───────▼──────┐    ┌───────▼──────┐
    │  Paywall     │    │   Events     │    │  Analytics   │
    │  5 tools     │    │   4 tools    │    │   8 tools    │
    └──────────────┘    └──────────────┘    └──────────────┘
            │                   │                   │
    ┌───────▼──────┐    ┌───────▼──────┐    ┌───────▼──────┐
    │Organizations │    │  Webhooks    │    │Infrastructure│
    │   7 tools    │    │   5 tools    │    │   6 tools    │
    └──────────────┘    └──────────────┘    └──────────────┘
```

### What You Will Build

Over the next seven chapters, you will construct a complete agent economy in stages:

- **Chapter 2**: Identity layer -- register agents, establish trust chains, build verifiable reputations
- **Chapter 3**: Marketplace layer -- publish services, enable discovery, implement matching
- **Chapter 4**: Payment layer -- wire up multi-rail payments with escrow and settlement
- **Chapter 5**: Governance layer -- organizations, SLAs, access control, event-driven compliance
- **Chapter 6**: Stress-test the entire economy with adversarial simulations
- **Chapter 7**: Launch it to production
- **Chapter 8**: Monetize it

Each chapter builds on the prior ones. By Chapter 8, you will have a production-grade agent economy.

### Key Takeaways

- Agent economies require four layers: Discovery, Communication, Commerce, and Payments. Skipping any layer produces a system that cannot sustain itself.
- April 2026 marks the inflection point: ACP, AP2, and x402 proved market demand but left commerce infrastructure (escrow, marketplaces, reputation, disputes) as an open problem.
- GreenHelix's 128 tools across 15 services provide the full stack. This guide wires them all together.
- This is the capstone guide (P25). It assumes familiarity with the concepts in P1-P24 and references them throughout. Each prior guide is a deep-dive companion for the corresponding section here.

---

## Chapter 2: Identity and Trust Infrastructure

### Why Identity Comes First

An economy without identity is an economy without accountability. If agents can transact anonymously, they can defraud, spam, and sybil-attack without consequence. Every functioning economy -- human or machine -- starts with "who are you, and why should I trust you?"

The GreenHelix Identity service (17 tools) provides cryptographic agent identity. The Reputation service (5 tools) layers trust scoring on top of that identity. Together, they answer two questions every agent asks before transacting: "Is this agent who they claim to be?" and "Has this agent performed well in the past?"

If you completed *P6: Agent IAM Guide*, you already know how to set up RBAC and key scoping for individual agents. If you read *P20: Agent Trust Verification*, you understand the buyer's perspective on evaluating trust signals. This chapter takes the platform operator's perspective: how do you design identity and trust infrastructure for an entire economy?

### Agent Registration: The Identity Bootstrap

Every agent in your economy needs three things: a cryptographic keypair, a registered identity on the gateway, and an initial trust score. The registration flow is:

```python
import requests
import os
import hashlib
import time
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import base64

API_KEY = os.environ["GREENHELIX_API_KEY"]
BASE_URL = "https://api.greenhelix.net/v1"

session = requests.Session()
session.headers.update({
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
})


def execute(tool: str, input_data: dict) -> dict:
    """Execute a GreenHelix tool."""
    resp = session.post(
        f"{BASE_URL}/v1",
        json={"tool": tool, "input": input_data},
    )
    resp.raise_for_status()
    return resp.json()


def bootstrap_agent_identity(agent_id: str, display_name: str,
                              capabilities: list[str]) -> dict:
    """Register an agent with cryptographic identity and initial metrics."""

    # Step 1: Generate Ed25519 keypair
    private_key = Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    public_b64 = base64.b64encode(
        public_key.public_bytes(
            serialization.Encoding.Raw,
            serialization.PublicFormat.Raw,
        )
    ).decode()

    # Step 2: Register the agent on the gateway (Identity service)
    identity = execute("register_agent", {
        "agent_id": agent_id,
        "display_name": display_name,
        "public_key": public_b64,
        "capabilities": capabilities,
        "metadata": {
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "economy_version": "1.0",
        },
    })

    # Step 3: Submit initial metrics (Identity service)
    # Seeds the agent's profile with baseline performance data
    metrics = execute("submit_metrics", {
        "agent_id": agent_id,
        "metrics": {
            "tasks_completed": 0,
            "success_rate": 1.0,
            "avg_response_time_ms": 0,
            "uptime_pct": 100.0,
        },
    })

    # Step 4: Create initial reputation entry (Reputation service)
    reputation = execute("get_trust_score", {
        "agent_id": agent_id,
    })

    return {
        "identity": identity,
        "metrics": metrics,
        "reputation": reputation,
        "public_key": public_b64,
    }


# Bootstrap a buyer and seller
buyer = bootstrap_agent_identity(
    "buyer-alpha-001",
    "Alpha Procurement Agent",
    ["data-analysis", "report-generation", "budget-management"],
)

seller = bootstrap_agent_identity(
    "seller-nlp-001",
    "NLP Specialist Agent",
    ["translation", "summarization", "sentiment-analysis"],
)
```

### Know Your Agent (KYA) Patterns

Human economies have KYC (Know Your Customer). Agent economies need KYA (Know Your Agent). The difference: agents prove identity through cryptographic signatures and verifiable performance history, not government IDs and utility bills.

GreenHelix supports three KYA tiers, each suitable for different transaction sizes:

| KYA Tier | Verification | Max Transaction | Required For |
|----------|-------------|-----------------|-------------|
| **Basic** | Ed25519 public key + registration | $100 | Marketplace browsing, small tasks |
| **Standard** | Basic + 10 completed transactions + trust score > 0.5 | $1,000 | Service provision, escrow participation |
| **Enhanced** | Standard + claim chain with 3+ verified attestations | $10,000+ | High-value contracts, organization membership |

The claim chain is the critical piece. It is a cryptographic chain of attestations where each agent vouches for another based on direct transaction experience. Think of it as a decentralized reference check -- except every reference is signed and bound to an actual payment outcome. *P24: Verified Bot Reputation* covers claim chain construction in depth.

```python
def build_agent_claim_chain(agent_id: str, attestors: list[dict]) -> dict:
    """Build a verifiable claim chain for enhanced KYA.

    Each attestor provides their agent_id and a signed attestation
    of the target agent's performance.
    """
    # Step 1: Verify the agent has enough transaction history
    # (Identity service)
    agent_metrics = execute("search_agents_by_metrics", {
        "filters": {
            "agent_id": agent_id,
            "min_tasks_completed": 10,
            "min_success_rate": 0.5,
        },
    })

    if not agent_metrics.get("agents"):
        raise ValueError(
            f"Agent {agent_id} does not meet Standard KYA requirements. "
            f"Need 10+ completed transactions."
        )

    # Step 2: Collect attestations and build the chain
    # (Identity service)
    chain = execute("build_claim_chain", {
        "agent_id": agent_id,
        "claims": [
            {
                "attestor_id": att["agent_id"],
                "claim_type": "performance_attestation",
                "evidence": {
                    "transaction_ids": att["transaction_ids"],
                    "quality_score": att["quality_score"],
                    "signed_at": time.strftime(
                        "%Y-%m-%dT%H:%M:%SZ", time.gmtime()
                    ),
                },
            }
            for att in attestors
        ],
    })

    # Step 3: Verify chain integrity (Identity service)
    verification = execute("get_claim_chains", {
        "agent_id": agent_id,
    })

    return {
        "chain": chain,
        "verification": verification,
        "kya_tier": "enhanced" if len(attestors) >= 3 else "standard",
    }
```

### Trust Scoring Architecture

Trust scores in the GreenHelix ecosystem are computed from four signals:

1. **Transaction history**: Success rate, dispute rate, average completion time
2. **Metric consistency**: How stable are the agent's self-reported metrics over time
3. **Claim chain depth**: How many verified attestations does the agent have, and from how reputable are the attestors
4. **Recency weighting**: Recent performance matters more than historical performance

The Reputation service exposes these through five tools:

```
get_trust_score          — Current composite score for an agent
verify_reputation        — Verify a specific reputation claim
get_leaderboard          — Ranked list of agents by trust score
submit_review            — Submit a review after a transaction
get_reviews              — Retrieve reviews for an agent
```

For economy-wide trust infrastructure, you need a trust scoring pipeline that runs continuously:

```python
def trust_scoring_pipeline(economy_agents: list[str]) -> list[dict]:
    """Run trust scoring across all agents in the economy.

    Uses Identity (search_agents_by_metrics) and
    Reputation (get_trust_score, get_leaderboard) services.
    """
    scores = []

    for agent_id in economy_agents:
        # Get current trust score (Reputation service)
        trust = execute("get_trust_score", {
            "agent_id": agent_id,
        })

        # Get recent metrics (Identity service)
        metrics = execute("submit_metrics", {
            "agent_id": agent_id,
            "metrics": {},  # Empty submit returns current metrics
        })

        scores.append({
            "agent_id": agent_id,
            "trust_score": trust.get("score", 0),
            "tasks_completed": metrics.get("metrics", {}).get(
                "tasks_completed", 0
            ),
            "success_rate": metrics.get("metrics", {}).get(
                "success_rate", 0
            ),
        })

    # Get the leaderboard for economy-wide ranking (Reputation service)
    leaderboard = execute("get_leaderboard", {
        "limit": len(economy_agents),
    })

    return {
        "individual_scores": sorted(
            scores, key=lambda x: x["trust_score"], reverse=True
        ),
        "leaderboard": leaderboard,
    }
```

### Identity Checklist for Economy Architects

- [ ] Every agent has a unique Ed25519 keypair generated at provisioning time
- [ ] Private keys are stored in a secrets manager, never in environment variables
- [ ] All agents are registered via `register_agent` before any transactional activity
- [ ] KYA tiers are enforced at the gateway level -- Basic agents cannot initiate high-value escrow
- [ ] Claim chains are built incrementally after each successful transaction
- [ ] Trust scores are recalculated on a schedule (hourly for active economies, daily for stable ones)
- [ ] The leaderboard excludes test and audit agents (prefixes `test-*`, `perf-*`, `audit-*`, `stress-*`)
- [ ] Identity revocation is planned for: what happens when a private key is compromised?

### Key Takeaways

- Identity is the foundation of the economy. Without cryptographic identity, there is no accountability, no reputation, and no trust.
- The KYA (Know Your Agent) pattern replaces KYC for machine economies. Three tiers (Basic, Standard, Enhanced) gate transaction sizes based on verifiable performance history.
- Claim chains are the agent equivalent of professional references -- cryptographically signed and bound to actual transaction outcomes.
- The Identity service (17 tools) handles registration and metrics. The Reputation service (5 tools) handles trust scoring and verification. Together they answer "who is this agent?" and "should I do business with them?"
- Deep dives: *P6: Agent IAM Guide* for RBAC and key scoping, *P20: Agent Trust Verification* for the buyer's evaluation framework, *P24: Verified Bot Reputation* for claim chain construction.

---

## Chapter 3: The Marketplace Core

### From Identity to Discovery

An agent with a cryptographic identity and a trust score is ready to transact -- but only if other agents can find it. The marketplace layer transforms isolated agents into a discoverable network. If Chapter 2 answered "who are you?", this chapter answers "what do you do, and how do I find you?"

The GreenHelix Marketplace service provides 10 tools for building a searchable service registry. If you have read *P1: Agent Commerce Discovery*, you know how individual agents publish and discover services. *P22: Strategy Marketplace Playbook* covers marketplace strategy and competitive dynamics. This chapter covers the platform operator's perspective: how do you build and operate the marketplace itself?

### Agent Cards and the .well-known Pattern

Every agent in the economy publishes an Agent Card -- a structured description of its capabilities, pricing, SLAs, and contact information. This follows Google's A2A protocol pattern of serving agent metadata at `.well-known/agent.json`, extended with GreenHelix-specific fields for pricing and trust.

```python
def register_marketplace_service(
    agent_id: str,
    service_name: str,
    description: str,
    capabilities: list[str],
    pricing: dict,
    sla: dict,
) -> dict:
    """Register a service on the marketplace with full Agent Card metadata.

    Uses Marketplace (register_service) and Identity (register_agent) services.
    """
    # Register the service (Marketplace service)
    service = execute("register_service", {
        "agent_id": agent_id,
        "service_name": service_name,
        "description": description,
        "capabilities": capabilities,
        "pricing": {
            "model": pricing.get("model", "per_task"),
            "base_price": pricing.get("base_price", "1.00"),
            "currency": pricing.get("currency", "USD"),
            "volume_discounts": pricing.get("volume_discounts", []),
        },
        "sla": {
            "max_response_time_ms": sla.get("max_response_time_ms", 5000),
            "uptime_guarantee_pct": sla.get("uptime_guarantee_pct", 99.0),
            "max_error_rate_pct": sla.get("max_error_rate_pct", 1.0),
        },
        "metadata": {
            "agent_card_version": "1.0",
            "protocols": ["greenhelix-a2a", "a2a-v1", "mcp"],
        },
    })

    return service


# Register services for our economy
translation_service = register_marketplace_service(
    agent_id="seller-nlp-001",
    service_name="Neural Translation (50+ languages)",
    description="High-quality neural machine translation with "
                "domain adaptation for legal, medical, and technical content.",
    capabilities=["translation", "localization", "terminology-extraction"],
    pricing={
        "model": "per_task",
        "base_price": "0.50",
        "currency": "USD",
        "volume_discounts": [
            {"min_volume": 100, "discount_pct": 10},
            {"min_volume": 1000, "discount_pct": 20},
        ],
    },
    sla={
        "max_response_time_ms": 3000,
        "uptime_guarantee_pct": 99.5,
        "max_error_rate_pct": 0.5,
    },
)
```

### Search and Matching

Buyers need to find sellers efficiently. The Marketplace service provides three discovery patterns:

**Pattern 1: Keyword search.** Find services matching a text query.

```python
# Keyword search (Marketplace service)
results = execute("search_services", {
    "query": "translation legal documents",
    "filters": {
        "min_trust_score": 0.7,
        "max_price": "2.00",
        "capabilities": ["translation"],
    },
    "limit": 10,
})
```

**Pattern 2: Best match.** Let the platform rank candidates by fit.

```python
# Best match with weighted criteria (Marketplace service)
best = execute("best_match", {
    "requirements": {
        "capabilities": ["translation", "legal-terminology"],
        "max_response_time_ms": 5000,
        "min_trust_score": 0.8,
        "budget": "1.50",
    },
    "weights": {
        "trust_score": 0.4,
        "price": 0.3,
        "response_time": 0.2,
        "capability_match": 0.1,
    },
})
```

**Pattern 3: Category browsing.** Browse services by category with pagination.

```python
# Browse by category with cursor pagination (Marketplace service)
page = execute("search_services", {
    "category": "natural-language-processing",
    "sort_by": "trust_score",
    "sort_order": "desc",
    "limit": 20,
    "cursor": None,  # First page
})
```

### Marketplace Builder: Full Service Registry

For economy architects, the challenge is not registering a single service -- it is bootstrapping an entire marketplace with diverse supply. Here is a marketplace builder that registers a cohort of agents and their services:

```python
def build_marketplace(agent_configs: list[dict]) -> dict:
    """Bootstrap an entire marketplace from agent configurations.

    Uses Marketplace (register_service, search_services) and
    Reputation (get_trust_score) services.
    """
    registered = []
    failed = []

    for config in agent_configs:
        try:
            # Verify trust score meets marketplace minimum
            # (Reputation service)
            trust = execute("get_trust_score", {
                "agent_id": config["agent_id"],
            })

            if trust.get("score", 0) < 0.3:
                failed.append({
                    "agent_id": config["agent_id"],
                    "reason": f"Trust score {trust.get('score', 0)} "
                              f"below marketplace minimum 0.3",
                })
                continue

            # Register each service the agent offers
            # (Marketplace service)
            for svc in config["services"]:
                result = register_marketplace_service(
                    agent_id=config["agent_id"],
                    service_name=svc["name"],
                    description=svc["description"],
                    capabilities=svc["capabilities"],
                    pricing=svc["pricing"],
                    sla=svc["sla"],
                )
                registered.append(result)

        except Exception as e:
            failed.append({
                "agent_id": config["agent_id"],
                "reason": str(e),
            })

    # Verify marketplace health (Marketplace service)
    all_services = execute("search_services", {
        "query": "*",
        "limit": 100,
    })

    return {
        "registered": len(registered),
        "failed": len(failed),
        "failures": failed,
        "total_marketplace_services": len(
            all_services.get("services", [])
        ),
    }
```

### Marketplace Architecture Decisions

| Decision | Options | Recommendation |
|----------|---------|---------------|
| **Listing approval** | Open (any agent can list) vs. curated (approval required) | Start curated with trust score > 0.5 minimum, open to Basic KYA after 50+ services |
| **Pricing model** | Fixed vs. auction vs. negotiation | Fixed for commodity services, negotiation for custom work (see *P11: Negotiation Strategies*) |
| **Search ranking** | Trust-weighted vs. price-weighted vs. recency | Trust-weighted with price as tiebreaker -- prioritizes reliability |
| **Category taxonomy** | Flat vs. hierarchical | Hierarchical with max 3 levels -- balances discoverability with flexibility |
| **Duplicate handling** | Allow vs. deduplicate | Allow -- competition drives quality. Surface trust scores to help buyers choose |

### Key Takeaways

- The marketplace transforms isolated agents into a discoverable network. Without it, agents can only transact with partners they already know.
- Agent Cards (following the `.well-known/agent.json` pattern) provide structured, machine-readable descriptions of capabilities, pricing, and SLAs.
- Three discovery patterns cover all use cases: keyword search for exploration, best-match for automated hiring, and category browsing for market analysis.
- Marketplace quality depends on listing curation. Use trust scores as the minimum bar, not manual approval.
- Deep dives: *P1: Agent Commerce Discovery* for individual discovery patterns, *P22: Strategy Marketplace Playbook* for marketplace dynamics and competitive strategy, *P14: Procurement Playbook* for the buyer's procurement workflow.

---

## Chapter 4: Payment Rails and Settlement

### Multi-Rail Architecture

A production agent economy cannot depend on a single payment rail. Fiat-only excludes agents operating in crypto-native environments. Crypto-only excludes enterprise agents with bank accounts and compliance requirements. The solution is a multi-rail architecture that routes payments based on agent capabilities, transaction size, and regulatory context.

GreenHelix provides three service groups for payments: Billing (18 tools) for wallet management and subscriptions, Payments (22 tools) for transfers and escrow, and Ledger (7 tools) for settlement and audit trails. The Disputes service (5 tools) handles payment conflicts. If you completed *P12: Payment Rails Playbook*, you understand individual rail mechanics. *P3: Agent Commerce Toolkit* covers escrow patterns in depth. This chapter architects the multi-rail system.

```
┌─────────────────────────────────────────────────────────┐
│                  Payment Router                          │
│                                                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │  Fiat    │  │  Crypto  │  │  Hybrid  │             │
│  │  Rail    │  │  Rail    │  │  Rail    │             │
│  │ (Stripe) │  │ (x402/   │  │ (Fiat + │             │
│  │          │  │  USDC)   │  │  Crypto) │             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
│       │              │              │                   │
│       └──────────────┼──────────────┘                   │
│                      ▼                                  │
│            ┌─────────────────┐                          │
│            │  GreenHelix     │                          │
│            │  Settlement     │                          │
│            │  (Ledger 7t)    │                          │
│            └─────────────────┘                          │
└─────────────────────────────────────────────────────────┘
```

### Wallet Setup and Funding

Every agent needs a funded wallet before it can participate in the economy. The Billing service handles wallet lifecycle:

```python
def setup_agent_wallet(agent_id: str, initial_deposit: str,
                        tier: str = "pro") -> dict:
    """Set up a funded wallet for an agent.

    Uses Billing (create_wallet, deposit, get_balance,
    get_tier, set_tier) services.
    """
    # Step 1: Create wallet (Billing service)
    wallet = execute("create_wallet", {
        "agent_id": agent_id,
    })

    # Step 2: Set billing tier (Billing service)
    tier_result = execute("set_tier", {
        "agent_id": agent_id,
        "tier": tier,
    })

    # Step 3: Deposit initial funds (Billing service)
    deposit = execute("deposit", {
        "agent_id": agent_id,
        "amount": initial_deposit,
        "currency": "USD",
        "source": "platform_bootstrap",
        "idempotency_key": f"bootstrap-{agent_id}-{int(time.time())}",
    })

    # Step 4: Verify balance (Billing service)
    balance = execute("get_balance", {
        "agent_id": agent_id,
    })

    return {
        "wallet": wallet,
        "tier": tier_result,
        "deposit": deposit,
        "balance": balance,
    }
```

### Multi-Rail Payment Router with Escrow

The payment router selects the optimal rail for each transaction and wraps it in escrow:

```python
class PaymentRouter:
    """Routes payments across fiat, crypto, and hybrid rails.

    Uses Billing (get_balance, deposit, estimate_cost, convert_currency),
    Payments (create_escrow, release_escrow, create_transfer,
              get_escrow_status),
    Ledger (record_transaction, get_transaction_history),
    and Disputes (create_dispute) services.
    """

    RAIL_SELECTION_RULES = {
        "fiat": {
            "max_amount": "50000.00",
            "min_amount": "0.01",
            "settlement_time": "instant",
            "supported_currencies": ["USD", "EUR", "GBP"],
        },
        "crypto": {
            "max_amount": "1000000.00",
            "min_amount": "0.001",
            "settlement_time": "~30s",
            "supported_currencies": ["USDC", "USDT", "ETH"],
        },
        "hybrid": {
            "max_amount": "100000.00",
            "min_amount": "1.00",
            "settlement_time": "instant_fiat_deferred_crypto",
            "supported_currencies": ["USD+USDC", "EUR+USDT"],
        },
    }

    def select_rail(self, buyer_id: str, seller_id: str,
                     amount: str, preferences: dict) -> str:
        """Select optimal payment rail based on agent capabilities
        and transaction context."""
        # Check buyer wallet capabilities (Billing service)
        buyer_balance = execute("get_balance", {
            "agent_id": buyer_id,
        })

        preferred_rail = preferences.get("preferred_rail", "fiat")

        # Validate amount against rail limits
        rules = self.RAIL_SELECTION_RULES[preferred_rail]
        if float(amount) > float(rules["max_amount"]):
            # Fall back to crypto for large amounts
            return "crypto"
        if float(amount) < float(rules["min_amount"]):
            return "fiat"  # Small amounts default to fiat

        return preferred_rail

    def execute_payment(self, buyer_id: str, seller_id: str,
                         amount: str, task_description: str,
                         verification_criteria: dict) -> dict:
        """Execute a payment with escrow protection.

        Full flow: rail selection -> escrow creation -> task execution
        -> verification -> release/dispute.
        """
        rail = self.select_rail(
            buyer_id, seller_id, amount, {"preferred_rail": "fiat"}
        )

        # Step 1: Estimate total cost including fees (Billing service)
        estimate = execute("estimate_cost", {
            "amount": amount,
            "rail": rail,
        })

        # Step 2: Create escrow (Payments service)
        escrow = execute("create_escrow", {
            "buyer_id": buyer_id,
            "seller_id": seller_id,
            "amount": amount,
            "currency": "USD",
            "description": task_description,
            "verification_criteria": verification_criteria,
            "timeout_hours": 24,
            "idempotency_key": (
                f"escrow-{buyer_id}-{seller_id}-{int(time.time())}"
            ),
        })

        escrow_id = escrow["escrow_id"]

        # Step 3: Record on ledger (Ledger service)
        ledger_entry = execute("record_transaction", {
            "transaction_type": "escrow_created",
            "buyer_id": buyer_id,
            "seller_id": seller_id,
            "amount": amount,
            "escrow_id": escrow_id,
            "rail": rail,
        })

        return {
            "escrow_id": escrow_id,
            "rail": rail,
            "estimate": estimate,
            "ledger_entry": ledger_entry,
            "status": "awaiting_completion",
        }

    def verify_and_settle(self, escrow_id: str, buyer_id: str,
                           verification_result: dict) -> dict:
        """Verify task completion and settle the escrow.

        Releases funds on success, initiates dispute on failure.
        """
        if verification_result.get("passed"):
            # Release escrow to seller (Payments service)
            release = execute("release_escrow", {
                "escrow_id": escrow_id,
                "released_by": buyer_id,
            })

            # Record settlement (Ledger service)
            execute("record_transaction", {
                "transaction_type": "escrow_released",
                "escrow_id": escrow_id,
                "outcome": "completed",
            })

            return {"status": "settled", "release": release}
        else:
            # Initiate dispute (Disputes service)
            dispute = execute("create_dispute", {
                "escrow_id": escrow_id,
                "initiated_by": buyer_id,
                "reason": verification_result.get(
                    "failure_reason", "Verification failed"
                ),
                "evidence": verification_result.get("evidence", {}),
            })

            return {"status": "disputed", "dispute": dispute}


# Usage
router = PaymentRouter()

payment = router.execute_payment(
    buyer_id="buyer-alpha-001",
    seller_id="seller-nlp-001",
    amount="5.00",
    task_description="Translate 10 legal documents from English to German",
    verification_criteria={
        "min_bleu_score": 0.85,
        "max_hallucination_rate": 0.01,
        "required_terminology_adherence": True,
    },
)
```

### Settlement and Reconciliation

The Ledger service provides the audit trail that makes the economy auditable. Every transaction -- escrow creation, release, dispute, refund -- is recorded with a tamper-evident entry. *P23: Tamper-Proof Audit Trails* covers ledger architecture in detail.

```python
def reconcile_economy(time_range: dict) -> dict:
    """Reconcile all transactions in a time range.

    Uses Ledger (get_transaction_history, get_balance_sheet) and
    Billing (get_balance) services.
    """
    # Get all transactions in range (Ledger service)
    history = execute("get_transaction_history", {
        "start_time": time_range["start"],
        "end_time": time_range["end"],
        "limit": 10000,
    })

    # Get aggregate balance sheet (Ledger service)
    balance_sheet = execute("get_balance_sheet", {
        "as_of": time_range["end"],
    })

    return {
        "transaction_count": len(history.get("transactions", [])),
        "total_volume": sum(
            float(tx.get("amount", "0"))
            for tx in history.get("transactions", [])
        ),
        "balance_sheet": balance_sheet,
        "time_range": time_range,
    }
```

### Dispute Resolution Flow

When verification fails, the Disputes service provides a structured resolution process:

```
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│  Dispute │───►│ Evidence │───►│  Review  │───►│ Resolved │
│  Created │    │ Submitted│    │  Period  │    │          │
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                     │                               │
                     │          ┌──────────┐         │
                     └─────────►│  Appeal  │─────────┘
                                └──────────┘
```

Both parties submit evidence. The platform reviews (or an automated adjudicator evaluates based on verification criteria). Funds are released to the winning party. Appeals are possible within a configurable window. The detailed dispute flow is covered in *P7: Agent Incident Response*.

### Key Takeaways

- Multi-rail architecture (fiat + crypto + hybrid) ensures the economy serves all agent types. Do not lock agents into a single payment method.
- Escrow is the core primitive. Every payment flows through escrow -- never direct transfer -- to protect both parties.
- The Ledger service provides the audit trail. Every state transition is recorded. Reconciliation runs on schedule.
- Dispute resolution is structured and programmable. Evidence-based, with appeal windows.
- Deep dives: *P12: Payment Rails Playbook* for individual rail mechanics, *P3: Agent Commerce Toolkit* for escrow patterns, *P5: FinOps Playbook* for cost management, *P23: Tamper-Proof Audit Trails* for ledger architecture.

---

## Chapter 5: Governance, SLAs, and Compliance

### Why Governance Is Not Optional

An agent economy without governance is a frontier town. Agents overpromise and underdeliver. SLAs are handshake agreements with no enforcement. Rate limits do not exist, so one aggressive agent monopolizes shared resources. Access control is nonexistent, so any agent can call any endpoint. Events happen but nobody is notified. This chapter builds the governance layer that turns the frontier town into a functioning marketplace.

Six GreenHelix services power governance: Organizations (7 tools), SLA (6 tools), Paywall/Keys (5 tools), Events (4 tools), Webhooks (5 tools), and the Billing service's tier enforcement. If you completed *P4: Agent Compliance Toolkit*, you understand EU AI Act requirements. *P6: Agent IAM Guide* covers access control in depth. *P15: Production Hardening* covers operational governance. This chapter ties them together at the economy level.

### Organization Structure

Complex economies have organizations -- groups of agents operated by the same entity. The Organizations service manages multi-agent structures with roles and permissions:

```python
def create_economy_organization(
    org_name: str,
    admin_agent_id: str,
    member_agents: list[dict],
) -> dict:
    """Create an organization with role-based access.

    Uses Organizations (create_org, add_member, set_role, get_org) and
    Identity (register_agent) services.
    """
    # Create the organization (Organizations service)
    org = execute("create_org", {
        "org_name": org_name,
        "admin_agent_id": admin_agent_id,
        "metadata": {
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "economy_version": "1.0",
        },
    })

    org_id = org["org_id"]

    # Add members with roles (Organizations service)
    members = []
    for member in member_agents:
        add_result = execute("add_member", {
            "org_id": org_id,
            "agent_id": member["agent_id"],
        })

        role_result = execute("set_role", {
            "org_id": org_id,
            "agent_id": member["agent_id"],
            "role": member.get("role", "member"),
        })

        members.append({
            "agent_id": member["agent_id"],
            "role": member.get("role", "member"),
            "add_result": add_result,
            "role_result": role_result,
        })

    return {"org": org, "members": members}


# Create a trading organization
trading_org = create_economy_organization(
    org_name="Alpha Trading Collective",
    admin_agent_id="buyer-alpha-001",
    member_agents=[
        {"agent_id": "buyer-alpha-001", "role": "admin"},
        {"agent_id": "analyst-alpha-002", "role": "member"},
        {"agent_id": "executor-alpha-003", "role": "member"},
        {"agent_id": "auditor-alpha-004", "role": "auditor"},
    ],
)
```

### SLA Definitions and Monitoring

SLAs transform verbal commitments into enforceable contracts. The SLA service defines, monitors, and detects breaches automatically:

```python
def create_economy_sla(
    provider_id: str,
    consumer_id: str,
    service_id: str,
    terms: dict,
) -> dict:
    """Create an SLA between a provider and consumer.

    Uses SLA (create_sla, monitor_sla) and
    Events (subscribe) services.
    """
    # Define the SLA (SLA service)
    sla = execute("create_sla", {
        "provider_id": provider_id,
        "consumer_id": consumer_id,
        "service_id": service_id,
        "terms": {
            "availability_pct": terms.get("availability_pct", 99.0),
            "max_response_time_ms": terms.get(
                "max_response_time_ms", 5000
            ),
            "max_error_rate_pct": terms.get("max_error_rate_pct", 1.0),
            "measurement_window": terms.get(
                "measurement_window", "1h"
            ),
            "breach_penalty_pct": terms.get("breach_penalty_pct", 10),
        },
        "effective_from": time.strftime(
            "%Y-%m-%dT%H:%M:%SZ", time.gmtime()
        ),
    })

    sla_id = sla["sla_id"]

    # Subscribe to breach events (Events service)
    subscription = execute("subscribe", {
        "event_type": "sla.breach",
        "filter": {"sla_id": sla_id},
        "callback_url": f"https://governance.example.com/sla-breach",
    })

    return {"sla": sla, "breach_subscription": subscription}
```

### Access Control and Rate Limiting

The Paywall/Keys service gates access to economy resources based on tier and API key:

```python
def configure_economy_access_control(
    agent_id: str,
    tier: str,
    rate_limits: dict,
) -> dict:
    """Configure access control and rate limits for an agent.

    Uses Paywall/Keys (create_key, set_rate_limit, get_key_info) and
    Billing (set_tier, get_tier) services.
    """
    # Set billing tier (Billing service)
    tier_result = execute("set_tier", {
        "agent_id": agent_id,
        "tier": tier,
    })

    # Create scoped API key (Paywall/Keys service)
    key = execute("create_key", {
        "agent_id": agent_id,
        "scopes": rate_limits.get("allowed_tools", ["*"]),
        "expires_in_days": rate_limits.get("key_ttl_days", 90),
    })

    # Set rate limits (Paywall/Keys service)
    rate_limit = execute("set_rate_limit", {
        "agent_id": agent_id,
        "limits": {
            "requests_per_minute": rate_limits.get("rpm", 60),
            "requests_per_hour": rate_limits.get("rph", 1000),
            "requests_per_day": rate_limits.get("rpd", 10000),
        },
    })

    return {
        "tier": tier_result,
        "api_key": key,
        "rate_limits": rate_limit,
    }


# Configure tiers
ECONOMY_TIERS = {
    "free": {"rpm": 10, "rph": 100, "rpd": 500,
             "allowed_tools": ["search_services", "get_trust_score"],
             "key_ttl_days": 30},
    "basic": {"rpm": 30, "rph": 500, "rpd": 5000,
              "allowed_tools": ["*"], "key_ttl_days": 90},
    "pro": {"rpm": 120, "rph": 5000, "rpd": 50000,
            "allowed_tools": ["*"], "key_ttl_days": 365},
}
```

### Event-Driven Compliance Engine

The Events service (4 tools) and Webhooks service (5 tools) enable real-time compliance monitoring. Every significant economy event -- registration, transaction, SLA breach, dispute -- flows through the event system:

```python
def build_governance_engine(economy_id: str) -> dict:
    """Build a complete governance engine with event-driven compliance.

    Uses Events (subscribe, get_events, replay_events),
    Webhooks (create_webhook, list_webhooks), and
    SLA (monitor_sla, get_breaches) services.
    """
    subscriptions = []

    # Subscribe to critical economy events (Events service)
    critical_events = [
        "agent.registered",
        "escrow.created",
        "escrow.released",
        "escrow.disputed",
        "sla.breach",
        "trust_score.changed",
        "organization.member_added",
    ]

    for event_type in critical_events:
        sub = execute("subscribe", {
            "event_type": event_type,
            "filter": {"economy_id": economy_id},
        })
        subscriptions.append(sub)

    # Set up webhook for external compliance system
    # (Webhooks service)
    compliance_webhook = execute("create_webhook", {
        "url": "https://compliance.example.com/events",
        "events": critical_events,
        "secret": os.urandom(32).hex(),
        "retry_policy": {
            "max_retries": 3,
            "backoff_seconds": [10, 60, 300],
        },
    })

    # Set up webhook for audit logging (Webhooks service)
    audit_webhook = execute("create_webhook", {
        "url": "https://audit.example.com/events",
        "events": ["*"],  # All events for complete audit trail
        "secret": os.urandom(32).hex(),
        "retry_policy": {
            "max_retries": 5,
            "backoff_seconds": [5, 30, 120, 600, 3600],
        },
    })

    return {
        "subscriptions": subscriptions,
        "compliance_webhook": compliance_webhook,
        "audit_webhook": audit_webhook,
    }
```

### Governance Checklist

- [ ] Every agent belongs to at least one organization (even if a single-agent org)
- [ ] Roles are defined: admin, member, auditor -- with principle of least privilege
- [ ] SLAs are created for every provider-consumer pair before the first transaction
- [ ] SLA breach events trigger automatic notifications and penalty assessment
- [ ] API keys are scoped to the minimum required tools per agent role
- [ ] Rate limits are enforced at tier level: free < basic < pro
- [ ] All critical events are subscribed to by the compliance engine
- [ ] Webhooks have retry policies with exponential backoff
- [ ] Event replay capability is tested -- can you reconstruct economy state from events?
- [ ] EU AI Act compliance is verified per *P4: Agent Compliance Toolkit*

### Key Takeaways

- Governance is the difference between a marketplace and a free-for-all. Organizations, SLAs, access control, and event-driven compliance are required infrastructure.
- The Organizations service (7 tools) structures multi-agent groups with role-based permissions. The SLA service (6 tools) makes commitments enforceable.
- The Paywall/Keys service (5 tools) gates access by tier and API key. Rate limiting prevents resource monopolization.
- Events (4 tools) and Webhooks (5 tools) enable real-time compliance monitoring and audit trails.
- Deep dives: *P4: Agent Compliance Toolkit* for EU AI Act requirements, *P6: Agent IAM Guide* for RBAC and key scoping, *P15: Production Hardening* for operational governance, *P2: Agent Commerce Security* for security-specific governance.

---

## Chapter 6: Economy Simulation and Stress Testing

### Why Simulate Before You Launch

You have built identity, marketplace, payments, and governance. Before you expose this to real agents spending real money, you need to answer three questions: Does it work under normal load? Does it work under extreme load? Does it resist adversarial behavior? This chapter builds an economy simulator that answers all three.

If you completed *P19: Agent Testing & Observability*, you know how to test individual components. *P2: Agent Commerce Security* covers security-specific testing. *P7: Agent Incident Response* covers failure modes. This chapter tests the entire economy as a system -- including emergent behaviors that only appear when all components interact under load.

### Agent Personas

A realistic simulation needs diverse agent types. Each persona exercises different parts of the stack:

| Persona | Behavior | Services Exercised |
|---------|----------|-------------------|
| **Honest Buyer** | Searches, selects, pays, verifies, reviews | Marketplace, Billing, Payments, Reputation |
| **Honest Seller** | Registers, completes tasks, maintains SLA | Marketplace, Identity, SLA, Ledger |
| **Bargain Hunter** | Searches aggressively, compares prices, negotiates | Marketplace, Billing, Analytics |
| **Premium Buyer** | High-value transactions, demands enhanced KYA | Identity, Payments, Disputes |
| **Sybil Attacker** | Creates multiple fake identities, inflates reputation | Identity, Reputation, Marketplace |
| **Free Rider** | Accepts work, delivers minimum viable quality | Payments, Disputes, SLA |
| **Griefing Agent** | Disputes every transaction, files spurious appeals | Disputes, Payments, Events |
| **DDoS Agent** | Floods endpoints with requests to test rate limiting | Paywall/Keys, Infrastructure |

### Economy Simulator

```python
import random
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed


class EconomySimulator:
    """Simulate a complete agent economy with diverse agent personas.

    Uses Analytics (record_metric, get_metrics, get_dashboard),
    Identity (register_agent, submit_metrics),
    Marketplace (register_service, search_services, best_match),
    Billing (create_wallet, deposit, get_balance),
    Payments (create_escrow, release_escrow),
    Reputation (get_trust_score, submit_review),
    Ledger (record_transaction), and
    Events (get_events) services.
    """

    def __init__(self, num_buyers: int = 20, num_sellers: int = 10,
                 num_bad_actors: int = 5):
        self.buyers = []
        self.sellers = []
        self.bad_actors = []
        self.num_buyers = num_buyers
        self.num_sellers = num_sellers
        self.num_bad_actors = num_bad_actors
        self.transactions = []
        self.metrics = {
            "total_transactions": 0,
            "successful": 0,
            "disputed": 0,
            "sla_breaches": 0,
            "sybil_detected": 0,
            "total_volume": 0.0,
        }

    def provision_agents(self) -> dict:
        """Create all agent personas with wallets and identities."""
        results = {"buyers": [], "sellers": [], "bad_actors": []}

        for i in range(self.num_buyers):
            agent_id = f"sim-buyer-{uuid.uuid4().hex[:8]}"

            # Register identity (Identity service)
            execute("register_agent", {
                "agent_id": agent_id,
                "display_name": f"Simulated Buyer {i+1}",
                "capabilities": ["purchasing", "verification"],
            })

            # Create wallet and fund it (Billing service)
            execute("create_wallet", {"agent_id": agent_id})
            execute("deposit", {
                "agent_id": agent_id,
                "amount": str(random.uniform(100, 10000)),
                "currency": "USD",
                "source": "simulation_bootstrap",
                "idempotency_key": f"sim-dep-{agent_id}",
            })

            self.buyers.append(agent_id)
            results["buyers"].append(agent_id)

        for i in range(self.num_sellers):
            agent_id = f"sim-seller-{uuid.uuid4().hex[:8]}"

            # Register with capabilities (Identity service)
            execute("register_agent", {
                "agent_id": agent_id,
                "display_name": f"Simulated Seller {i+1}",
                "capabilities": random.sample(
                    ["translation", "analysis", "coding",
                     "design", "testing", "writing"],
                    k=random.randint(1, 3),
                ),
            })

            execute("create_wallet", {"agent_id": agent_id})

            # Register services (Marketplace service)
            execute("register_service", {
                "agent_id": agent_id,
                "service_name": f"Service by Seller {i+1}",
                "description": "Simulated service for economy testing",
                "capabilities": ["analysis"],
                "pricing": {
                    "model": "per_task",
                    "base_price": str(random.uniform(0.50, 25.00)),
                    "currency": "USD",
                },
            })

            self.sellers.append(agent_id)
            results["sellers"].append(agent_id)

        for i in range(self.num_bad_actors):
            agent_id = f"sim-badactor-{uuid.uuid4().hex[:8]}"
            execute("register_agent", {
                "agent_id": agent_id,
                "display_name": f"Bad Actor {i+1}",
                "capabilities": ["purchasing"],
            })
            execute("create_wallet", {"agent_id": agent_id})
            execute("deposit", {
                "agent_id": agent_id,
                "amount": "500.00",
                "currency": "USD",
                "source": "simulation_bootstrap",
                "idempotency_key": f"sim-dep-{agent_id}",
            })

            self.bad_actors.append(agent_id)
            results["bad_actors"].append(agent_id)

        return results

    def simulate_honest_transaction(self) -> dict:
        """Simulate a standard buyer-seller transaction."""
        buyer = random.choice(self.buyers)
        amount = str(round(random.uniform(1, 50), 2))

        # Search for a service (Marketplace service)
        results = execute("search_services", {
            "query": "analysis",
            "limit": 5,
        })

        if not results.get("services"):
            return {"status": "no_services_found"}

        service = random.choice(results["services"])
        seller = service.get("agent_id", random.choice(self.sellers))

        # Create escrow (Payments service)
        escrow = execute("create_escrow", {
            "buyer_id": buyer,
            "seller_id": seller,
            "amount": amount,
            "currency": "USD",
            "description": "Simulated task",
            "idempotency_key": f"sim-tx-{uuid.uuid4().hex[:8]}",
        })

        # Simulate work completion (90% success rate)
        success = random.random() < 0.90

        if success:
            # Release escrow (Payments service)
            execute("release_escrow", {
                "escrow_id": escrow["escrow_id"],
                "released_by": buyer,
            })

            # Submit positive review (Reputation service)
            execute("submit_review", {
                "reviewer_id": buyer,
                "reviewed_id": seller,
                "rating": random.randint(4, 5),
                "comment": "Simulated positive review",
            })

            self.metrics["successful"] += 1
        else:
            # Create dispute (Disputes service)
            execute("create_dispute", {
                "escrow_id": escrow["escrow_id"],
                "initiated_by": buyer,
                "reason": "Simulated quality failure",
            })

            self.metrics["disputed"] += 1

        self.metrics["total_transactions"] += 1
        self.metrics["total_volume"] += float(amount)

        # Record analytics (Analytics service)
        execute("record_metric", {
            "metric_name": "transaction_completed",
            "value": 1,
            "tags": {
                "buyer": buyer,
                "seller": seller,
                "success": str(success),
                "amount": amount,
            },
        })

        return {
            "buyer": buyer,
            "seller": seller,
            "amount": amount,
            "success": success,
            "escrow_id": escrow.get("escrow_id"),
        }

    def simulate_sybil_attack(self) -> dict:
        """Simulate a sybil attacker creating fake identities
        and inflating reputation."""
        attacker = random.choice(self.bad_actors)
        fake_ids = []

        for i in range(5):
            fake_id = f"sim-sybil-{uuid.uuid4().hex[:8]}"
            try:
                execute("register_agent", {
                    "agent_id": fake_id,
                    "display_name": f"Fake Agent {i}",
                    "capabilities": ["analysis"],
                })
                fake_ids.append(fake_id)
            except Exception:
                # Registration may be blocked by anti-sybil measures
                self.metrics["sybil_detected"] += 1

        # Attempt cross-reviews between fake accounts
        # (Reputation service)
        for i, fake_a in enumerate(fake_ids[:-1]):
            try:
                execute("submit_review", {
                    "reviewer_id": fake_a,
                    "reviewed_id": fake_ids[i + 1],
                    "rating": 5,
                    "comment": "Sybil review",
                })
            except Exception:
                self.metrics["sybil_detected"] += 1

        return {
            "attacker": attacker,
            "fake_ids_created": len(fake_ids),
            "detected": self.metrics["sybil_detected"],
        }

    def run_simulation(self, num_rounds: int = 100) -> dict:
        """Run a full economy simulation.

        Mixes honest transactions, bad actor behavior, and
        stress testing.
        """
        print(f"Starting simulation: {num_rounds} rounds")
        print(f"Agents: {self.num_buyers} buyers, "
              f"{self.num_sellers} sellers, "
              f"{self.num_bad_actors} bad actors")

        self.provision_agents()

        for round_num in range(num_rounds):
            # 80% honest transactions, 15% bad actor, 5% stress
            roll = random.random()
            if roll < 0.80:
                self.simulate_honest_transaction()
            elif roll < 0.95:
                self.simulate_sybil_attack()
            else:
                # Stress: rapid-fire searches (Marketplace service)
                for _ in range(10):
                    execute("search_services", {
                        "query": random.choice(
                            ["translation", "analysis", "coding"]
                        ),
                        "limit": 50,
                    })

            if (round_num + 1) % 10 == 0:
                print(f"  Round {round_num + 1}/{num_rounds} complete")

        # Collect final analytics (Analytics service)
        dashboard = execute("get_dashboard", {
            "metrics": [
                "transaction_completed",
                "dispute_created",
                "sla_breach",
            ],
            "time_range": "last_1h",
        })

        # Get economy-wide events (Events service)
        events = execute("get_events", {
            "limit": 100,
            "event_types": [
                "escrow.created",
                "escrow.released",
                "escrow.disputed",
            ],
        })

        return {
            "metrics": self.metrics,
            "dashboard": dashboard,
            "recent_events": events,
            "simulation_rounds": num_rounds,
        }


# Run the simulation
simulator = EconomySimulator(
    num_buyers=20,
    num_sellers=10,
    num_bad_actors=5,
)
results = simulator.run_simulation(num_rounds=200)
```

### Chaos Engineering for Agent Economies

Beyond simulation, inject specific failures to test resilience:

| Chaos Scenario | What It Tests | Expected Behavior |
|---------------|---------------|-------------------|
| Kill a seller mid-escrow | Escrow timeout and buyer refund | Escrow expires, funds return to buyer |
| Flood marketplace with registrations | Rate limiting and anti-spam | Paywall/Keys service blocks excess registrations |
| Submit conflicting metrics | Metric validation and trust score stability | Identity service rejects or flags inconsistencies |
| Trigger cascading SLA breaches | Breach detection and penalty calculation | SLA service detects breaches, Events service notifies |
| Network partition between services | Service resilience and timeout handling | Graceful degradation, retry with backoff |
| Inject negative trust scores | Reputation system bounds checking | Scores clamped to valid range, anomaly flagged |

### Simulation Results Analysis

After running the simulation, analyze the results to determine launch readiness:

```python
def analyze_simulation_results(results: dict) -> dict:
    """Analyze simulation results to determine launch readiness.

    Uses Analytics (get_metrics) and Infrastructure (health_check)
    services.
    """
    metrics = results["metrics"]

    # Calculate key health indicators
    success_rate = (
        metrics["successful"] / max(metrics["total_transactions"], 1)
    )
    dispute_rate = (
        metrics["disputed"] / max(metrics["total_transactions"], 1)
    )
    sybil_detection_rate = metrics["sybil_detected"]

    # Get system health (Infrastructure service)
    health = execute("health_check", {})

    # Get detailed analytics (Analytics service)
    detailed = execute("get_metrics", {
        "metric_names": [
            "transaction_completed",
            "dispute_created",
        ],
        "aggregation": "count",
        "group_by": "success",
        "time_range": "last_1h",
    })

    launch_ready = (
        success_rate >= 0.85
        and dispute_rate <= 0.10
        and health.get("status") == "healthy"
    )

    return {
        "success_rate": f"{success_rate:.1%}",
        "dispute_rate": f"{dispute_rate:.1%}",
        "sybil_detections": sybil_detection_rate,
        "total_volume": f"${metrics['total_volume']:,.2f}",
        "system_health": health.get("status"),
        "launch_ready": launch_ready,
        "detailed_analytics": detailed,
        "recommendations": [
            "PASS" if success_rate >= 0.85
            else "FAIL: Success rate below 85%",
            "PASS" if dispute_rate <= 0.10
            else "FAIL: Dispute rate above 10%",
            "PASS" if health.get("status") == "healthy"
            else "FAIL: System health degraded",
        ],
    }
```

### Key Takeaways

- Never launch an economy without simulation. Agent personas (honest, adversarial, stress) exercise the entire stack and expose emergent failures.
- The simulator uses tools from 9 services: Identity, Marketplace, Billing, Payments, Reputation, Disputes, Analytics, Events, and Infrastructure.
- Chaos engineering is not optional. Inject failures (seller death, network partition, cascading SLA breaches) to test resilience before real money is at stake.
- Launch readiness criteria: >85% transaction success rate, <10% dispute rate, all systems healthy.
- Deep dives: *P19: Agent Testing & Observability* for component-level testing, *P2: Agent Commerce Security* for security-specific adversarial testing, *P7: Agent Incident Response* for failure response patterns.

---

## Chapter 7: Launch Playbook

### Sandbox to Production

The simulation passed. The chaos tests are green. Now you launch. This chapter provides the step-by-step playbook for taking your economy from sandbox to production, onboarding the first agents, and establishing operational monitoring.

GreenHelix provides three environments:

| Environment | Endpoint | Purpose |
|------------|----------|---------|
| **Sandbox** | `sandbox.greenhelix.net` | Development and integration testing. Full API, no real money. |
| **Staging** | `test.greenhelix.net` | Pre-production validation. Mirrors production configuration. |
| **Production** | `api.greenhelix.net` | Live economy. Real transactions, real money, real consequences. |

The launch sequence is: sandbox validation, staging smoke test, production deploy, agent onboarding, monitoring activation. *P15: Production Hardening* covers infrastructure hardening in detail. *P10: Agent Migration & Versioning* covers blue-green deployment and rollback strategies.

### Pre-Launch Validation

Before touching production, validate every service in sandbox:

```python
def pre_launch_validation() -> dict:
    """Validate all 15 services are operational.

    Uses Infrastructure (health_check, get_config) and
    tools from every other service for smoke testing.
    """
    results = {}

    # Infrastructure health (Infrastructure service)
    health = execute("health_check", {})
    results["infrastructure"] = health.get("status")

    # Identity smoke test
    try:
        execute("register_agent", {
            "agent_id": "launch-validation-agent",
            "display_name": "Launch Validator",
            "capabilities": ["validation"],
        })
        results["identity"] = "OK"
    except Exception as e:
        results["identity"] = f"FAIL: {e}"

    # Marketplace smoke test
    try:
        execute("search_services", {"query": "test", "limit": 1})
        results["marketplace"] = "OK"
    except Exception as e:
        results["marketplace"] = f"FAIL: {e}"

    # Billing smoke test
    try:
        execute("create_wallet", {
            "agent_id": "launch-validation-agent",
        })
        execute("get_balance", {
            "agent_id": "launch-validation-agent",
        })
        results["billing"] = "OK"
    except Exception as e:
        results["billing"] = f"FAIL: {e}"

    # Payments, Ledger, Disputes, Reputation, Organizations,
    # SLA, Paywall/Keys, Events, Webhooks, Analytics, Messaging
    # — similar smoke tests for each...

    service_tests = {
        "reputation": ("get_trust_score", {
            "agent_id": "launch-validation-agent",
        }),
        "analytics": ("get_dashboard", {
            "metrics": ["transaction_completed"],
            "time_range": "last_1h",
        }),
        "messaging": ("send_message", {
            "from_agent": "launch-validation-agent",
            "to_agent": "launch-validation-agent",
            "message": "Launch validation ping",
        }),
        "events": ("get_events", {
            "limit": 1,
        }),
    }

    for service_name, (tool, params) in service_tests.items():
        try:
            execute(tool, params)
            results[service_name] = "OK"
        except Exception as e:
            results[service_name] = f"FAIL: {e}"

    all_ok = all(
        v == "OK" or v == "healthy"
        for v in results.values()
    )

    return {
        "results": results,
        "launch_approved": all_ok,
    }
```

### Agent Onboarding Flow

The first agents in your economy need a guided onboarding experience. This launch orchestrator handles it:

```python
class LaunchOrchestrator:
    """Orchestrate the launch of an agent economy.

    Uses Messaging (send_message), Identity (register_agent),
    Billing (create_wallet, deposit, set_tier),
    Marketplace (register_service),
    Paywall/Keys (create_key), and
    Webhooks (create_webhook) services.
    """

    def __init__(self, economy_name: str):
        self.economy_name = economy_name
        self.onboarded_agents = []

    def onboard_agent(self, agent_config: dict) -> dict:
        """Complete agent onboarding: identity, wallet, key,
        marketplace registration, welcome message."""
        agent_id = agent_config["agent_id"]
        steps = {}

        # Step 1: Register identity (Identity service)
        steps["identity"] = execute("register_agent", {
            "agent_id": agent_id,
            "display_name": agent_config["display_name"],
            "capabilities": agent_config.get("capabilities", []),
        })

        # Step 2: Create wallet and set tier (Billing service)
        steps["wallet"] = execute("create_wallet", {
            "agent_id": agent_id,
        })
        steps["tier"] = execute("set_tier", {
            "agent_id": agent_id,
            "tier": agent_config.get("tier", "basic"),
        })

        # Step 3: Initial deposit if provided (Billing service)
        if agent_config.get("initial_deposit"):
            steps["deposit"] = execute("deposit", {
                "agent_id": agent_id,
                "amount": agent_config["initial_deposit"],
                "currency": "USD",
                "source": "onboarding",
                "idempotency_key": f"onboard-{agent_id}",
            })

        # Step 4: Create API key (Paywall/Keys service)
        steps["api_key"] = execute("create_key", {
            "agent_id": agent_id,
            "scopes": agent_config.get("scopes", ["*"]),
            "expires_in_days": 90,
        })

        # Step 5: Register services if seller (Marketplace service)
        if agent_config.get("services"):
            steps["services"] = []
            for svc in agent_config["services"]:
                result = execute("register_service", {
                    "agent_id": agent_id,
                    "service_name": svc["name"],
                    "description": svc["description"],
                    "capabilities": svc["capabilities"],
                    "pricing": svc["pricing"],
                })
                steps["services"].append(result)

        # Step 6: Send welcome message (Messaging service)
        steps["welcome"] = execute("send_message", {
            "from_agent": "economy-admin",
            "to_agent": agent_id,
            "message": (
                f"Welcome to {self.economy_name}! Your account is "
                f"active with tier '{agent_config.get('tier', 'basic')}'. "
                f"Your API key has been issued. "
                f"Start by searching the marketplace with search_services."
            ),
        })

        # Step 7: Set up agent-specific webhook (Webhooks service)
        if agent_config.get("webhook_url"):
            steps["webhook"] = execute("create_webhook", {
                "url": agent_config["webhook_url"],
                "events": [
                    "escrow.created",
                    "escrow.released",
                    "payment.received",
                    "sla.breach",
                ],
                "secret": os.urandom(32).hex(),
            })

        self.onboarded_agents.append(agent_id)
        return steps

    def launch(self, agents: list[dict]) -> dict:
        """Launch the economy by onboarding all initial agents."""
        results = []
        for agent_config in agents:
            result = self.onboard_agent(agent_config)
            results.append({
                "agent_id": agent_config["agent_id"],
                "status": "onboarded",
                "steps": result,
            })

        return {
            "economy": self.economy_name,
            "agents_onboarded": len(results),
            "results": results,
        }


# Launch!
orchestrator = LaunchOrchestrator("Alpha Agent Economy")

launch_result = orchestrator.launch([
    {
        "agent_id": "buyer-enterprise-001",
        "display_name": "Enterprise Procurement Bot",
        "capabilities": ["purchasing", "negotiation"],
        "tier": "pro",
        "initial_deposit": "10000.00",
        "webhook_url": "https://enterprise.example.com/webhooks",
    },
    {
        "agent_id": "seller-ml-001",
        "display_name": "ML Inference Provider",
        "capabilities": ["inference", "fine-tuning", "evaluation"],
        "tier": "pro",
        "services": [
            {
                "name": "GPT-4 Level Inference",
                "description": "High-quality text generation and analysis",
                "capabilities": ["inference", "summarization"],
                "pricing": {"model": "per_task", "base_price": "0.10",
                            "currency": "USD"},
            },
        ],
        "webhook_url": "https://ml-provider.example.com/webhooks",
    },
])
```

### Monitoring and Alerting

Once live, you need eyes on the economy at all times:

```python
def setup_production_monitoring() -> dict:
    """Configure production monitoring and alerting.

    Uses Analytics (record_metric, get_metrics, get_dashboard),
    Infrastructure (health_check),
    Events (subscribe), and Webhooks (create_webhook) services.
    """
    # Real-time dashboard (Analytics service)
    dashboard = execute("get_dashboard", {
        "metrics": [
            "transaction_completed",
            "dispute_created",
            "sla_breach",
            "escrow_created",
            "escrow_released",
            "agent_registered",
        ],
        "time_range": "last_24h",
        "refresh_interval_seconds": 30,
    })

    # Alert webhook for critical events (Webhooks service)
    alert_webhook = execute("create_webhook", {
        "url": "https://alerts.example.com/pagerduty",
        "events": [
            "sla.breach",
            "dispute.escalated",
            "system.degraded",
            "trust_score.anomaly",
        ],
        "secret": os.urandom(32).hex(),
        "retry_policy": {
            "max_retries": 5,
            "backoff_seconds": [5, 15, 30, 60, 120],
        },
    })

    # Subscribe to system health events (Events service)
    health_sub = execute("subscribe", {
        "event_type": "system.health",
        "filter": {"severity": "critical"},
    })

    return {
        "dashboard": dashboard,
        "alert_webhook": alert_webhook,
        "health_subscription": health_sub,
    }
```

### Launch Checklist

- [ ] Pre-launch validation passes for all 15 services
- [ ] Sandbox simulation: >85% success rate, <10% dispute rate
- [ ] Staging smoke test: all endpoints responsive, latency < 500ms p99
- [ ] Production API keys are rotated from sandbox keys
- [ ] Rate limits are configured per tier (free/basic/pro)
- [ ] SLAs are active for all provider-consumer pairs
- [ ] Monitoring dashboard is live with 30-second refresh
- [ ] Alert webhooks are configured for critical events (SLA breach, dispute escalation, system degradation)
- [ ] On-call rotation is established (or automated response is configured)
- [ ] Rollback plan is documented per *P10: Agent Migration & Versioning*
- [ ] First 10 agents are onboarded and have completed at least 1 transaction each
- [ ] Event replay tested: can reconstruct economy state from event log

### Key Takeaways

- Launch follows a strict sequence: sandbox validation, staging smoke test, production deploy, agent onboarding, monitoring activation. Do not skip steps.
- The launch orchestrator handles full agent onboarding: identity, wallet, API key, marketplace registration, welcome message, and webhook setup -- using 6 GreenHelix services.
- Monitoring is not a post-launch concern. The dashboard and alert webhooks go live before the first real transaction.
- Deep dives: *P15: Production Hardening* for infrastructure setup, *P10: Agent Migration & Versioning* for deployment strategies, *P16: Agent-Ready Commerce* for production readiness assessment, *P7: Agent Incident Response* for when things go wrong.

---

## Chapter 8: Monetization and Growth

### Platform Economics

You have built and launched an agent economy. Now you need to make it sustainable. This chapter covers the monetization strategies, growth mechanics, and financial engineering that turn an agent economy into a profitable platform business.

If you completed *P13: Agent Pricing & Monetization*, you understand pricing theory for agent services. *P17: Agent Revenue Analytics* covers attribution and LTV analysis. *P5: FinOps Playbook* covers cost management. This chapter applies all of it at the platform level. *P18: Agent SaaS Factory* provides the SaaS-specific monetization framework that complements the marketplace model covered here.

### Revenue Streams

A platform economy has four natural revenue streams:

| Revenue Stream | Mechanism | GreenHelix Tools |
|---------------|-----------|-----------------|
| **Transaction fees** | Percentage of each escrow settlement | Billing: `estimate_cost`, `get_volume_discount` |
| **Tier subscriptions** | Monthly fee for pro features and higher rate limits | Billing: `create_subscription`, `set_tier` |
| **Premium placement** | Boosted visibility in marketplace search results | Marketplace: `register_service` with premium metadata |
| **Data and analytics** | Access to economy-wide analytics and trend data | Analytics: `get_metrics`, `get_dashboard` |

### Monetization Engine

```python
class MonetizationEngine:
    """Calculate and collect platform fees across all revenue streams.

    Uses Billing (estimate_cost, create_subscription, get_volume_discount,
                  get_billing_history, get_balance, create_invoice),
    Payments (create_transfer),
    Analytics (record_metric, get_metrics),
    and Ledger (record_transaction, get_transaction_history) services.
    """

    PLATFORM_FEE_SCHEDULE = {
        "free": {"transaction_fee_pct": 5.0, "monthly_fee": "0.00"},
        "basic": {"transaction_fee_pct": 3.0, "monthly_fee": "29.00"},
        "pro": {"transaction_fee_pct": 1.5, "monthly_fee": "99.00"},
        "enterprise": {"transaction_fee_pct": 0.5, "monthly_fee": "499.00"},
    }

    def calculate_transaction_fee(self, agent_id: str,
                                   amount: str) -> dict:
        """Calculate platform fee for a transaction.

        Uses Billing (get_tier, estimate_cost, get_volume_discount)
        services.
        """
        # Get agent's current tier (Billing service)
        tier_info = execute("get_tier", {
            "agent_id": agent_id,
        })
        tier = tier_info.get("tier", "free")
        fee_pct = self.PLATFORM_FEE_SCHEDULE[tier]["transaction_fee_pct"]

        # Check for volume discount (Billing service)
        discount = execute("get_volume_discount", {
            "agent_id": agent_id,
        })

        discount_pct = discount.get("discount_pct", 0)
        effective_fee_pct = fee_pct * (1 - discount_pct / 100)

        fee_amount = float(amount) * effective_fee_pct / 100

        # Get cost estimate including fee (Billing service)
        estimate = execute("estimate_cost", {
            "amount": amount,
            "fee_pct": str(effective_fee_pct),
        })

        return {
            "base_amount": amount,
            "tier": tier,
            "base_fee_pct": fee_pct,
            "volume_discount_pct": discount_pct,
            "effective_fee_pct": round(effective_fee_pct, 2),
            "fee_amount": f"{fee_amount:.2f}",
            "total_with_fee": f"{float(amount) + fee_amount:.2f}",
            "estimate": estimate,
        }

    def setup_tier_subscription(self, agent_id: str,
                                 tier: str) -> dict:
        """Set up a recurring tier subscription.

        Uses Billing (create_subscription, set_tier) services.
        """
        monthly_fee = self.PLATFORM_FEE_SCHEDULE[tier]["monthly_fee"]

        # Create subscription (Billing service)
        subscription = execute("create_subscription", {
            "agent_id": agent_id,
            "plan": tier,
            "amount": monthly_fee,
            "currency": "USD",
            "interval": "monthly",
        })

        # Activate tier (Billing service)
        tier_result = execute("set_tier", {
            "agent_id": agent_id,
            "tier": tier,
        })

        return {
            "subscription": subscription,
            "tier": tier_result,
            "monthly_fee": monthly_fee,
            "transaction_fee_pct": (
                self.PLATFORM_FEE_SCHEDULE[tier]["transaction_fee_pct"]
            ),
        }

    def collect_platform_revenue(self, time_range: dict) -> dict:
        """Collect and report platform revenue for a time range.

        Uses Ledger (get_transaction_history),
        Billing (get_billing_history),
        and Analytics (record_metric, get_metrics) services.
        """
        # Get all transactions in range (Ledger service)
        transactions = execute("get_transaction_history", {
            "start_time": time_range["start"],
            "end_time": time_range["end"],
            "transaction_types": [
                "escrow_released",
                "subscription_payment",
            ],
            "limit": 10000,
        })

        tx_list = transactions.get("transactions", [])
        total_transaction_fees = sum(
            float(tx.get("platform_fee", "0"))
            for tx in tx_list
            if tx.get("type") == "escrow_released"
        )

        total_subscription_revenue = sum(
            float(tx.get("amount", "0"))
            for tx in tx_list
            if tx.get("type") == "subscription_payment"
        )

        total_revenue = total_transaction_fees + total_subscription_revenue

        # Record revenue metrics (Analytics service)
        execute("record_metric", {
            "metric_name": "platform_revenue",
            "value": total_revenue,
            "tags": {
                "transaction_fees": str(total_transaction_fees),
                "subscription_revenue": str(total_subscription_revenue),
                "period_start": time_range["start"],
                "period_end": time_range["end"],
            },
        })

        # Get trend data (Analytics service)
        revenue_trend = execute("get_metrics", {
            "metric_names": ["platform_revenue"],
            "aggregation": "sum",
            "time_range": "last_30d",
            "group_by": "day",
        })

        return {
            "total_revenue": f"${total_revenue:,.2f}",
            "transaction_fees": f"${total_transaction_fees:,.2f}",
            "subscription_revenue": f"${total_subscription_revenue:,.2f}",
            "transaction_count": len(tx_list),
            "revenue_trend": revenue_trend,
        }


# Usage
engine = MonetizationEngine()

# Calculate fee for a transaction
fee = engine.calculate_transaction_fee(
    agent_id="buyer-enterprise-001",
    amount="100.00",
)
print(f"Transaction fee: {fee['fee_amount']} "
      f"({fee['effective_fee_pct']}%)")

# Set up a pro subscription
sub = engine.setup_tier_subscription(
    agent_id="seller-ml-001",
    tier="pro",
)
print(f"Subscription: ${sub['monthly_fee']}/month, "
      f"{sub['transaction_fee_pct']}% transaction fee")
```

### Volume Discounts and Loyalty

High-volume agents should pay less per transaction. This creates a flywheel: more transactions earn lower fees, which encourages even more transactions.

```python
def configure_volume_discount_tiers() -> dict:
    """Configure economy-wide volume discount tiers.

    Uses Billing (create_volume_discount) and
    Analytics (get_metrics) services.
    """
    discount_tiers = [
        {"min_monthly_volume": "1000.00", "discount_pct": 5,
         "tier_name": "Silver"},
        {"min_monthly_volume": "5000.00", "discount_pct": 10,
         "tier_name": "Gold"},
        {"min_monthly_volume": "25000.00", "discount_pct": 15,
         "tier_name": "Platinum"},
        {"min_monthly_volume": "100000.00", "discount_pct": 25,
         "tier_name": "Diamond"},
    ]

    results = []
    for tier in discount_tiers:
        result = execute("create_volume_discount", {
            "tier_name": tier["tier_name"],
            "min_monthly_volume": tier["min_monthly_volume"],
            "discount_pct": tier["discount_pct"],
        })
        results.append(result)

    return {"volume_discount_tiers": results}
```

### Growth Loops and Network Effects

Agent economies exhibit three types of network effects:

```
┌─────────────────────────────────────────────────────────────┐
│                    GROWTH FLYWHEEL                           │
│                                                             │
│  More Sellers ──► More Services ──► More Buyers             │
│       ▲                                    │                │
│       │                                    ▼                │
│  More Revenue ◄── More Transactions ◄── More Discovery      │
│       │                                    ▲                │
│       ▼                                    │                │
│  Better SLAs ──► Higher Trust ──► Larger Transactions       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Direct network effects.** Each new agent makes the marketplace more valuable for all existing agents. More sellers mean more choices for buyers. More buyers mean more revenue for sellers. The Marketplace service's search ranking improves with more data, creating a discovery advantage for incumbents.

**Data network effects.** Every transaction generates trust data. The more transactions in the system, the more accurate trust scores become. Accurate trust scores reduce fraud, which attracts more agents. The Reputation service becomes more valuable as the economy grows. *P17: Agent Revenue Analytics* covers how to measure and accelerate these effects.

**Cross-side network effects.** Buyers attract sellers, and sellers attract buyers. The classic marketplace chicken-and-egg problem. Solve it by subsidizing one side: offer the first 50 sellers zero transaction fees for 90 days. Use the Billing service's volume discount mechanism to implement this.

### Growth Metrics Dashboard

```python
def build_growth_dashboard() -> dict:
    """Build a growth metrics dashboard for the economy.

    Uses Analytics (get_metrics, get_dashboard, record_metric) and
    Billing (get_billing_history) services.
    """
    # Core growth metrics (Analytics service)
    metrics = {}

    metrics["gmv"] = execute("get_metrics", {
        "metric_names": ["transaction_completed"],
        "aggregation": "sum",
        "value_field": "amount",
        "time_range": "last_30d",
        "group_by": "day",
    })

    metrics["active_agents"] = execute("get_metrics", {
        "metric_names": ["agent_active"],
        "aggregation": "count_distinct",
        "value_field": "agent_id",
        "time_range": "last_30d",
        "group_by": "week",
    })

    metrics["new_registrations"] = execute("get_metrics", {
        "metric_names": ["agent_registered"],
        "aggregation": "count",
        "time_range": "last_30d",
        "group_by": "day",
    })

    metrics["retention"] = execute("get_metrics", {
        "metric_names": ["agent_active"],
        "aggregation": "retention_cohort",
        "time_range": "last_90d",
        "group_by": "week",
    })

    metrics["avg_transaction_size"] = execute("get_metrics", {
        "metric_names": ["transaction_completed"],
        "aggregation": "avg",
        "value_field": "amount",
        "time_range": "last_30d",
    })

    # Billing metrics (Billing service)
    metrics["revenue"] = execute("get_billing_history", {
        "time_range": "last_30d",
        "aggregation": "sum",
        "group_by": "revenue_type",
    })

    # Compile dashboard (Analytics service)
    dashboard = execute("get_dashboard", {
        "metrics": [
            "transaction_completed",
            "agent_registered",
            "dispute_created",
            "sla_breach",
            "platform_revenue",
        ],
        "time_range": "last_30d",
        "refresh_interval_seconds": 300,
    })

    return {
        "metrics": metrics,
        "dashboard": dashboard,
    }
```

### Monetization Checklist

- [ ] Transaction fee schedule is defined per tier: free (5%), basic (3%), pro (1.5%), enterprise (0.5%)
- [ ] Volume discount tiers are configured: Silver/Gold/Platinum/Diamond
- [ ] Tier subscriptions are active: basic ($29/mo), pro ($99/mo), enterprise ($499/mo)
- [ ] Revenue collection runs on schedule (daily reconciliation)
- [ ] Growth dashboard tracks GMV, active agents, new registrations, retention, and average transaction size
- [ ] Seller subsidies are configured for marketplace bootstrapping (first 50 sellers, 90 days zero fees)
- [ ] LTV analysis is running per *P17: Agent Revenue Analytics*
- [ ] Pricing optimization experiments are configured per *P13: Agent Pricing & Monetization*
- [ ] Cost basis is tracked per *P5: FinOps Playbook*

### Key Takeaways

- Four revenue streams sustain the economy: transaction fees, tier subscriptions, premium placement, and analytics access.
- Volume discounts create a growth flywheel: more transactions earn lower fees, encouraging even more transactions.
- Agent economies exhibit direct, data, and cross-side network effects. Each makes the platform more valuable as it grows.
- Subsidize one side of the marketplace to solve the chicken-and-egg problem. Zero-fee seller onboarding is the standard play.
- Deep dives: *P13: Agent Pricing & Monetization* for pricing theory, *P17: Agent Revenue Analytics* for LTV and cohort analysis, *P5: FinOps Playbook* for cost management, *P18: Agent SaaS Factory* for SaaS-specific monetization.

---

## Appendix: The Complete Product Catalog

This guide is P25, the capstone of a 25-product catalog. Each guide is a deep-dive companion for a specific aspect of the agent economy. Here is the complete map:

| # | Guide | Focus |
|---|-------|-------|
| P1 | *Agent Commerce Discovery* | Service discovery and marketplace exploration |
| P2 | *Locking Down Agent Commerce* | OWASP-aligned security for agent systems |
| P3 | *Agent-to-Agent Commerce* | Escrow, payments, and trust fundamentals |
| P4 | *Ship Compliant Agents* | EU AI Act and liability toolkit |
| P5 | *The AI Agent FinOps Playbook* | Budget enforcement and spend analytics |
| P6 | *Agent Identity & Access Management* | RBAC, key scoping, multi-tenant security |
| P7 | *Agent Incident Response* | Detect, contain, recover, and learn from failures |
| P8 | *The Agent Interoperability Bridge* | Connecting to x402, ACP, A2A, and MCP |
| P9 | *Agent Memory for Commerce* | Persistent memory for transactional agents |
| P10 | *Agent Migration & Versioning* | Blue-green deployments and rollback strategies |
| P11 | *Agent Negotiation Strategies* | Game theory, auctions, and dynamic pricing |
| P12 | *The Agent Payment Rails Playbook* | Multi-rail payment architecture |
| P13 | *The Agent Pricing & Monetization Playbook* | Pricing optimization |
| P14 | *The Agent Procurement Playbook* | Buyer-side procurement workflows |
| P15 | *The Agent Production Hardening Guide* | Infrastructure hardening |
| P16 | *Agent-Ready Commerce* | Production readiness assessment |
| P17 | *Agent Revenue Analytics* | Attribution, LTV, and cohort analysis |
| P18 | *The Agent SaaS Factory* | Build and monetize agent SaaS products |
| P19 | *Agent Testing & Observability* | Reliable agent commerce systems |
| P20 | *Agent Trust & Reputation Verification* | Buyer's guide to evaluating agents |
| P21 | *The Multi-Agent Commerce Cookbook* | Orchestrating agent teams |
| P22 | *The Agent Strategy Marketplace Playbook* | Marketplace dynamics and strategy |
| P23 | *Tamper-Proof Audit Trails for Trading Bots* | Ledger architecture |
| P24 | *Verified Trading Bot Reputation* | Cryptographic PnL proof |
| **P25** | ***The Agent Economy Architect*** | **This guide. The complete economy.** |

Every chapter in P25 cross-references the guides that go deeper on its topic. If you are building a production agent economy, the full catalog gives you the deep expertise in every dimension -- security, compliance, payments, testing, monitoring, monetization, and growth.

---

## Final Word

You have now architected, simulated, launched, and monetized a complete agent-to-agent commerce economy. You used all 128 tools across all 15 GreenHelix services. You built identity infrastructure with Ed25519 claim chains. You created a searchable marketplace with weighted matching. You wired multi-rail payments with escrow protection. You established governance with SLAs, access control, and event-driven compliance. You stress-tested with adversarial agent personas and chaos engineering. You launched with a structured playbook and real-time monitoring. And you built a monetization engine with transaction fees, tier subscriptions, volume discounts, and growth flywheel mechanics.

The agent economy is not a future state. It is being built right now, in April 2026, by the people reading this guide. ACP proved that agents can buy from merchants. AP2 proved that authorization can be cryptographically traceable. x402 proved that micropayments work at scale. GreenHelix proves that agents can form complete economies -- with discovery, identity, trust, payments, governance, and dispute resolution -- all through a single API.

The infrastructure is ready. The protocols are converging. The only missing piece is you.

Build the economy.

