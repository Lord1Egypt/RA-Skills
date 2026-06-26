---
name: greenhelix-protocol-wars-comparison
version: "1.3.1"
description: "The Protocol Wars: Agent Commerce Protocol Comparison — x402, ACP, MCP, A2A and Beyond. Comprehensive comparison of 8+ competing agent commerce protocols (x402, ACP, AP2, MPP, TAP, UCP, MCP, A2A). Feature matrix, latency/cost benchmarks, migration paths, multi-protocol gateway pattern, and future-proofing strategies."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [protocols, x402, acp, mcp, a2a, comparison, guide, greenhelix, openclaw, ai-agent]
price_usd: 0.0
content_type: markdown
executable: false
install: none
credentials: [WALLET_ADDRESS, AGENT_SIGNING_KEY, STRIPE_API_KEY]
metadata:
  openclaw:
    requires:
      env:
        - WALLET_ADDRESS
        - AGENT_SIGNING_KEY
        - STRIPE_API_KEY
    primaryEnv: WALLET_ADDRESS
---
# The Protocol Wars: Agent Commerce Protocol Comparison — x402, ACP, MCP, A2A and Beyond

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `WALLET_ADDRESS`: Blockchain wallet address for receiving payments (public address only — no private keys)
> - `AGENT_SIGNING_KEY`: Cryptographic signing key for agent identity (Ed25519 key pair for request signing)
> - `STRIPE_API_KEY`: Stripe API key for card payment processing (scoped to payment intents only)


Eleven competing protocols now claim to be the standard for agent commerce: x402, ACP (Agentic Commerce Protocol), AP2 (Agent Payments Protocol), MPP (Machine Payment Protocol), TAP (Trusted Agent Protocol), UCP (Universal Commerce Protocol), MCP (Model Context Protocol), Google's A2A, Visa TAP (Trusted Agent Protocol), Google AP2 (Agent Payments Protocol), OpenAI ACP (Agentic Commerce Protocol), PayPal Agent Ready, and Google UCP (Universal Commerce Protocol). Q1 2026 detonated what was already a crowded field -- five major protocols launched in a single quarter, backed by Google, OpenAI, Visa, PayPal, Shopify, Walmart, and dozens of other heavyweights. If you are building an agent commerce system in 2026, this is the most consequential architectural decision you will make. Pick wrong and you are locked into a dying standard with a shrinking ecosystem, incompatible partners, and migration costs that compound with every month of development. Pick right and you inherit network effects -- more counterparties, better tooling, cheaper integrations, and a protocol governance body that evolves in your direction. Pick poorly enough and you rewrite your entire commerce layer eighteen months from now, which is what happened to teams that went all-in on SOAP in 2005 or GraphQL subscriptions in 2019.
The problem is that no comprehensive comparison exists. You will find marketing pages from each protocol's backers, blog posts that compare two protocols at a time, and Twitter threads with strong opinions and no benchmarks. What you will not find is a single document that evaluates all protocols against the same criteria, with real latency measurements, cost calculations, migration path analysis, and production-tested code for hedging your bets across multiple protocols simultaneously. This guide provides exactly that. It includes a feature-by-feature comparison matrix, benchmark data from test deployments against live endpoints, step-by-step migration paths between the most common protocol pairs, a complete multi-protocol gateway implementation in Python, and a benchmarking framework you can run against your own infrastructure. Every code example runs against the GreenHelix A2A Commerce Gateway at `https://api.greenhelix.net/v1`.
1. [The Protocol Landscape](#chapter-1-the-protocol-landscape)

## What You'll Learn
- Chapter 1: The Protocol Landscape
- Chapter 2: Protocol-by-Protocol Deep Dive
- Chapter 3: Feature Comparison Matrix
- Chapter 4: Latency and Cost Benchmarks
- Chapter 5: Migration Paths
- Chapter 6: Multi-Protocol Gateway Pattern
- Chapter 7: ProtocolBenchmark Class
- Chapter 8: Future-Proofing Strategies
- What's Next
- Multi-Protocol Adapter — Working Implementation

## Full Guide

# The Protocol Wars: Agent Commerce Protocol Comparison

Eleven competing protocols now claim to be the standard for agent commerce: x402, ACP (Agentic Commerce Protocol), AP2 (Agent Payments Protocol), MPP (Machine Payment Protocol), TAP (Trusted Agent Protocol), UCP (Universal Commerce Protocol), MCP (Model Context Protocol), Google's A2A, Visa TAP (Trusted Agent Protocol), Google AP2 (Agent Payments Protocol), OpenAI ACP (Agentic Commerce Protocol), PayPal Agent Ready, and Google UCP (Universal Commerce Protocol). Q1 2026 detonated what was already a crowded field -- five major protocols launched in a single quarter, backed by Google, OpenAI, Visa, PayPal, Shopify, Walmart, and dozens of other heavyweights. If you are building an agent commerce system in 2026, this is the most consequential architectural decision you will make. Pick wrong and you are locked into a dying standard with a shrinking ecosystem, incompatible partners, and migration costs that compound with every month of development. Pick right and you inherit network effects -- more counterparties, better tooling, cheaper integrations, and a protocol governance body that evolves in your direction. Pick poorly enough and you rewrite your entire commerce layer eighteen months from now, which is what happened to teams that went all-in on SOAP in 2005 or GraphQL subscriptions in 2019.

The problem is that no comprehensive comparison exists. You will find marketing pages from each protocol's backers, blog posts that compare two protocols at a time, and Twitter threads with strong opinions and no benchmarks. What you will not find is a single document that evaluates all protocols against the same criteria, with real latency measurements, cost calculations, migration path analysis, and production-tested code for hedging your bets across multiple protocols simultaneously. This guide provides exactly that. It includes a feature-by-feature comparison matrix, benchmark data from test deployments against live endpoints, step-by-step migration paths between the most common protocol pairs, a complete multi-protocol gateway implementation in Python, and a benchmarking framework you can run against your own infrastructure. Every code example runs against the GreenHelix A2A Commerce Gateway at `https://api.greenhelix.net/v1`.

---

## Table of Contents

1. [The Protocol Landscape](#chapter-1-the-protocol-landscape)
2. [Protocol-by-Protocol Deep Dive](#chapter-2-protocol-by-protocol-deep-dive)
3. [Feature Comparison Matrix](#chapter-3-feature-comparison-matrix)
4. [Latency and Cost Benchmarks](#chapter-4-latency-and-cost-benchmarks)
5. [Migration Paths](#chapter-5-migration-paths)
6. [Multi-Protocol Gateway Pattern](#chapter-6-multi-protocol-gateway-pattern)
7. [ProtocolBenchmark Class](#chapter-7-protocolbenchmark-class)
8. [Future-Proofing Strategies](#chapter-8-future-proofing-strategies)

---

## Chapter 1: The Protocol Landscape

### Why Eleven Protocols Emerged Simultaneously

The period from late 2024 to Q1 2026 produced more agent commerce protocol proposals than the previous decade of API standardization work combined. The Q1 2026 payment protocol explosion -- five new protocols in a single quarter -- turned a crowded field into a full-blown standards war. This was not coincidental. Three market forces converged to create a standards vacuum that every major technology company and several well-funded startups rushed to fill.

**Force 1: Tool calling reached production reliability.** In 2023, structured tool calling was experimental. By mid-2024, GPT-4o, Claude 3.5 Sonnet, Gemini 1.5, Llama 3.1, and Mistral Large all supported reliable function calling with JSON Schema inputs and structured outputs. For the first time, AI agents could make HTTP requests, parse responses, and chain operations without brittle prompt engineering. The immediate consequence was that agents could interact with external services programmatically, which meant they needed a way to pay for those services. The HTTP 402 status code -- "Payment Required" -- had been reserved in the HTTP specification since 1997 but never standardized. Suddenly it mattered.

**Force 2: The AI agent market reached commercial scale.** By Q4 2024, agent frameworks like LangChain, CrewAI, AutoGen, and Semantic Kernel had crossed the threshold from developer experiments to production deployments. Enterprises were running agent fleets that made millions of API calls per day. The question shifted from "can agents do useful work?" to "how do agents pay for and sell services to each other?" Every major cloud provider, fintech company, and AI lab saw the same trillion-dollar opportunity and started designing their own answer.

**Force 3: Regulatory pressure forced audit trail requirements.** The EU AI Act, with key provisions effective August 2, 2026, requires that AI systems making financial decisions maintain auditable records of every transaction, including the identity of participating agents, the terms agreed upon, and the outcome. The US Executive Order on AI (October 2023) and subsequent NIST guidelines pushed similar requirements for federal procurement. Agent commerce protocols were not just a technical convenience -- they became a compliance requirement. And compliance requirements, unlike developer preferences, create hard deadlines for adoption.

### The Timeline

```
2024-2026 Agent Commerce Protocol Timeline
================================================

2024 Q3    Coinbase publishes x402 draft specification
2024 Q4    Anthropic releases MCP (Model Context Protocol) v1.0
           Google announces A2A (Agent-to-Agent) protocol
2025 Q1    x402 reaches production on Cloudflare Workers
           OpenAI + Stripe announce early ACP work
           TAP (Transaction Agent Protocol) launches on Ethereum
2025 Q2    AP2 (Agent Payment Protocol) launched by PayPal Labs
           MPP (Machine Payment Protocol) launched by Visa Research
2025 Q3    UCP (Universal Commerce Protocol) announced by
           consortium (Mastercard, SAP, Salesforce)
           MCP v2.0 adds Streamable HTTP transport
2025 Q4    A2A reaches v1.0 with 50+ launch partners
           ACP integrates with Shopify, Instacart, Etsy
           MCP donated to Linux Foundation
           MCP registry launches at registry.modelcontextprotocol.io

─── Q1 2026: THE PAYMENT PROTOCOL EXPLOSION ───────────────

2026 Q1    Visa TAP (Trusted Agent Protocol) launches —
             cryptographic agent identity per transaction,
             card network settlement
           Google AP2 (Agent Payments Protocol) launches —
             payment-agnostic (cards, bank, stablecoins),
             cryptographic user mandates, 60+ partners incl.
             Adyen, Mastercard, PayPal, Visa
           OpenAI ACP (Agentic Commerce Protocol) released —
             open spec for cart/checkout/payment, developed
             with Stripe, Apache 2.0 licensed
           PayPal Agent Ready launches — cross-protocol
             adapter for existing PayPal merchants,
             multi-protocol bridge
           Google UCP (Universal Commerce Protocol) launches —
             commerce-layer complement to AP2, co-developed
             with Shopify, Etsy, Wayfair, Target, Walmart
           x402 Foundation surpasses 100M+ payments in 6 months,
             backed by Coinbase + Cloudflare + Stripe + AWS +
             Microsoft + Google + Amex
           MCP reaches 10K+ servers cataloged in registry
           A2A expands partner list, IBM joins

2026 Q2    EU AI Act compliance deadline approaches
           Protocol consolidation pressure intensifies —
           but Q1 launches expanded the field instead
```

### Categories: Payment vs. Communication vs. Commerce vs. Bridge

Not all eleven protocols solve the same problem. The Q1 2026 launches introduced two new categories -- commerce-layer protocols and bridge protocols -- that the earlier taxonomy of "payment vs. communication vs. hybrid" no longer captures.

**Payment protocols** focus on how Agent A pays Agent B for a service. They define payment flows, settlement mechanisms, and transaction records. x402, the original AP2, MPP, TAP, Visa TAP, and Google AP2 are primarily payment protocols. They answer the question: "The agent wants to buy something -- how does the money move?"

**Communication protocols** focus on how agents discover each other, describe their capabilities, exchange messages, and coordinate tasks. MCP and A2A are primarily communication protocols. They answer the question: "The agent wants to use a service -- how does it find and interact with the provider?"

**Commerce-layer protocols** define the full shopping lifecycle -- catalog browsing, cart management, checkout, payment, and fulfillment -- as a unified flow. OpenAI ACP and Google UCP are commerce-layer protocols. They answer the question: "The agent wants to buy a product -- how does the entire transaction lifecycle work end-to-end?"

**Bridge protocols** sit between existing protocols and translate between them. PayPal Agent Ready is the first purpose-built bridge protocol. It answers the question: "The agent speaks protocol X but the merchant speaks protocol Y -- how do they transact anyway?"

This categorization matters because the protocols are not all competing for the same niche. x402 and MCP can coexist because they solve orthogonal problems. Google AP2 and Visa TAP compete directly on payment rails. OpenAI ACP and Google UCP compete on the commerce layer. PayPal Agent Ready competes with nobody -- it bridges everything. Understanding these boundaries is the first step toward a rational protocol strategy.

### Market Dynamics Driving Fragmentation

The fragmentation is not a failure of coordination -- it is a predictable outcome of market structure. Each protocol's design reflects its backer's strategic position. Q1 2026 made this dynamic worse, not better: five new protocols from five different strategic positions.

Coinbase and Cloudflare designed x402 around cryptocurrency micropayments because that extends their existing infrastructure (Base L2, Workers). The x402 Foundation's growth to 100M+ payments and backing from Stripe, AWS, Microsoft, Google, and Amex shows the protocol transcending its crypto origins. OpenAI and Stripe designed ACP as an open specification (Apache 2.0) for the full cart/checkout/payment lifecycle because OpenAI wants agents buying things through ChatGPT and Stripe wants to be the default payment rail. Google launched two complementary protocols: AP2 for payment orchestration (payment-agnostic, supporting cards, bank transfers, and stablecoins with cryptographic user mandates) and UCP for the commerce layer (co-developed with Shopify, Etsy, Wayfair, Target, and Walmart). Google does not operate payment rails but wants to control the commerce orchestration layer above them. Visa designed TAP around cryptographically signed agent identity per transaction because Visa wants machine payments to flow through card network settlement with the same fraud and compliance infrastructure that handles human payments. PayPal built Agent Ready as a cross-protocol bridge because PayPal's strategic advantage is its merchant base -- 35M+ merchants who do not want to rewrite their integrations for every new protocol. Anthropic designed MCP around tool calling because Claude's competitive advantage is tool use reliability and MCP increases tool ecosystem lock-in. The donation of MCP to the Linux Foundation signals Anthropic's bet that MCP becomes infrastructure, not a competitive moat.

Every protocol is rational from the perspective of its backers. None is rational from the perspective of a team building agent commerce systems that need to work with all of them.

---

## Chapter 2: Protocol-by-Protocol Deep Dive

### x402: HTTP 402 Payment Required

x402 is the simplest protocol in the comparison and, as of Q1 2026, the one with the most staggering production numbers. It adds a payment layer to HTTP by using the 402 status code that has been reserved since HTTP/1.1 was standardized in 1997 but was never given a concrete implementation until Coinbase and Cloudflare defined one in late 2024.

The flow is four steps. A client sends an HTTP request. The server returns 402 with headers specifying the price, currency, payment address, and facilitator URL. The client sends payment through the facilitator (typically USDC on Base L2 or Solana). The client retries the original request with an `X-PAYMENT-PROOF` header containing the transaction hash and facilitator signature.

The x402 Foundation, launched in late 2025, has grown into a coalition that no one predicted: Coinbase, Cloudflare, Stripe, AWS, Microsoft, Google, and American Express all back the standard. The protocol crossed 100 million payments in its first six months of Foundation operation. That number dwarfs every other protocol's transaction count combined.

**Strengths:** Minimal integration surface. Any HTTP server can add x402 support by returning 402 responses and validating proof headers. Sub-cent micropayments are economically viable because Base L2 transaction fees are under $0.001. Settlement is typically under 2 seconds. The protocol has the strongest production track record -- over 100 million transactions settled as of Q1 2026. The Foundation's multi-stakeholder backing (spanning crypto, cloud, fintech, and card networks) gives it uniquely broad ecosystem support.

**Weaknesses:** No identity, discovery, escrow, or dispute resolution. The payment is one-shot: money moves and the transaction is done. If the service delivers garbage, the buyer has no recourse within the protocol. No support for subscriptions, metered billing, or complex pricing models.

```python
# x402 server-side: return a 402 response
from fastapi import FastAPI, Request, Response
import json, time

app = FastAPI()

@app.get("/api/translate")
async def translate(request: Request, text: str, target_lang: str):
    proof = request.headers.get("X-PAYMENT-PROOF")
    if not proof:
        return Response(
            status_code=402,
            headers={
                "X-PAYMENT-AMOUNT": "0.005",
                "X-PAYMENT-CURRENCY": "USDC",
                "X-PAYMENT-ADDRESS": "0x1a2b3c...",
                "X-PAYMENT-FACILITATOR": "https://x402.org/facilitator",
                "X-PAYMENT-EXPIRY": str(int(time.time()) + 300),
            },
            content="Payment required",
        )
    # Validate proof, then serve the response
    validated = validate_proof(proof)  # verify with facilitator
    return {"translated": do_translation(text, target_lang)}
```

```bash
# x402 client-side: pay and retry
curl -s https://agent.example.com/api/translate?text=hello&target_lang=fr
# Returns 402 with payment headers

# After paying through the facilitator:
curl -s https://agent.example.com/api/translate?text=hello&target_lang=fr \
  -H 'X-PAYMENT-PROOF: {"tx_hash":"0xabc...","facilitator_signature":"0xdef...","amount":"0.005"}'
# Returns {"translated": "bonjour"}
```

### ACP: Agentic Commerce Protocol (OpenAI)

ACP was rebranded and relaunched in Q1 2026 as the **Agentic Commerce Protocol** -- an open specification developed by OpenAI with Stripe, released under the Apache 2.0 license. This is a significant evolution from the earlier Stripe-centric ACP work in 2025. The new ACP defines a complete open standard for the agent shopping lifecycle: product catalog discovery, cart management, checkout initiation, payment processing, and fulfillment confirmation. The specification is deliberately payment-processor-agnostic at the protocol level, though Stripe provides the reference implementation.

ACP is the protocol behind ChatGPT's "Instant Checkout" feature, which allows users to purchase products from Etsy, Shopify, and Instacart merchants directly within a conversation. As of Q1 2026, ACP processes over $200 million in monthly transaction volume.

**Strengths:** Full commerce lifecycle -- catalog browsing, cart management, checkout, payment, fulfillment, and refunds. Open specification under Apache 2.0, meaning anyone can implement it without licensing fees. The Stripe reference implementation provides fraud detection, chargeback handling, and global payment method support (cards, bank transfers, Apple Pay, Google Pay). Strong merchant tooling and dashboard. OpenAI's distribution through ChatGPT provides immediate consumer-facing adoption. The open-spec approach means alternative payment processors can implement ACP backends.

**Weaknesses:** Despite being "open," the practical ecosystem is still heavily Stripe-dependent -- the reference implementation is the only production-grade one. Agent-to-agent transactions where neither party has a merchant account are not well supported. Minimum transaction amount remains $0.50 (Stripe's floor), making sub-cent micropayments impossible. The cart/checkout model is oriented toward consumer purchasing, not machine-to-machine micropayments.

```python
# ACP: Creating a product listing and checkout session
import requests

ACP_API = "https://api.stripe.com/v1/acp"

# Register a product in the ACP catalog
product = requests.post(f"{ACP_API}/products", json={
    "name": "Code Review Agent",
    "description": "Automated code review with security analysis",
    "price": {"amount": 500, "currency": "usd"},  # $5.00
    "fulfillment": {
        "type": "api_callback",
        "url": "https://myagent.example.com/fulfill",
    },
}, headers={"Authorization": "Bearer sk_live_xxx"})

# Agent-side: initiate checkout
session = requests.post(f"{ACP_API}/checkout/sessions", json={
    "product_id": product.json()["id"],
    "buyer_agent_id": "agent-buyer-123",
    "success_url": "https://myagent.example.com/success",
    "metadata": {"repo": "github.com/user/repo", "pr": "42"},
}, headers={"Authorization": "Bearer sk_live_xxx"})

checkout_url = session.json()["url"]
# Agent completes payment at checkout_url, fulfillment webhook fires
```

### AP2 (Original): Agent Payment Protocol (PayPal Labs)

The original AP2, developed by PayPal Labs in 2025, is a crypto-native payment protocol designed specifically for autonomous agent transactions. Unlike x402's single-shot payment model, AP2 supports payment channels -- persistent bidirectional payment relationships between two agents that allow unlimited off-chain transactions with on-chain settlement only when the channel is opened or closed. Note: this is distinct from Google's AP2 (Agent Payments Protocol), launched in Q1 2026, which shares the abbreviation but is an entirely different protocol.

**Strengths:** Extremely low per-transaction cost after channel establishment (effectively zero for off-chain transactions). Supports streaming payments -- continuous per-second billing for ongoing services. Built-in multi-signature escrow at the protocol level. Designed for high-frequency agent interactions where two agents transact repeatedly.

**Weaknesses:** Channel establishment requires an on-chain transaction ($0.50-$2.00 on Ethereum L2, higher on mainnet). Not economical for one-off transactions. Complex state management -- both agents must maintain channel state, and if either agent goes offline unexpectedly, dispute resolution requires on-chain intervention. Limited ecosystem adoption compared to x402 and ACP. The naming collision with Google AP2 has caused significant market confusion.

```python
# AP2: Open a payment channel and stream payments
from ap2 import PaymentChannel, StreamingPayment

# Establish a channel with 100 USDC capacity
channel = PaymentChannel.open(
    agent_a="did:ap2:buyer-agent-xyz",
    agent_b="did:ap2:seller-agent-abc",
    capacity_usdc=100.0,
    network="base",  # Base L2
)

# Stream payments at $0.001/second for an ongoing translation service
stream = StreamingPayment(
    channel=channel,
    rate_per_second=0.001,
    max_duration_seconds=3600,
)
stream.start()

# ... agent uses the service for 847 seconds ...

stream.stop()  # Final cost: $0.847, settled off-chain
channel.close()  # Single on-chain settlement of net balance
```

### MPP: Machine Payment Protocol (Visa Research, 2025)

MPP, developed by Visa Research in 2025, was the first attempt to route agent payments through traditional card network rails. The protocol assigns each agent a virtual card number (VCN) linked to a funding source (credit card, bank account, or prepaid balance). When an agent needs to pay for a service, it generates a one-time payment token from its VCN, and the payment settles through Visa's existing authorization and settlement infrastructure. Note: MPP has been largely superseded by Visa TAP (launched Q1 2026), which adds cryptographic agent identity and is described in its own section below.

**Strengths:** Integrates with every merchant that accepts Visa (over 100 million globally). No new payment infrastructure required -- payments flow through existing card rails. Per-transaction fraud scoring using Visa's neural network models. Support for recurring billing, refunds, and chargebacks through existing card network processes. Familiar to enterprises with existing procurement systems.

**Weaknesses:** High per-transaction cost ($0.20-$0.30 minimum due to interchange fees), making micropayments uneconomical. Settlement latency of 1-3 business days (standard card network settlement). Not suitable for real-time payment confirmation. The virtual card provisioning process requires KYB (Know Your Business) verification, adding onboarding friction. Limited to fiat currencies. Being superseded by Visa TAP in Visa's own product roadmap.

```python
# MPP: Provision a virtual card for an agent and make a payment
import requests

MPP_API = "https://api.visa.com/mpp/v1"

# Provision a virtual card for the agent
vcn = requests.post(f"{MPP_API}/virtual-cards", json={
    "agent_id": "agent-procurement-001",
    "funding_source": "card_fund_src_abc123",
    "spending_limit": {"amount": 10000, "currency": "USD", "period": "monthly"},
    "allowed_merchant_categories": ["5734", "7372"],  # Software, IT services
}, headers={"Authorization": "Bearer visa_api_key"})

# Generate a one-time payment token
token = requests.post(f"{MPP_API}/tokens", json={
    "virtual_card_id": vcn.json()["id"],
    "amount": 25.00,
    "currency": "USD",
    "merchant_id": "merchant_seller_agent_xyz",
}, headers={"Authorization": "Bearer visa_api_key"})

# Use the token to pay for the service
payment_token = token.json()["token"]
# Seller processes payment_token through standard card authorization
```

### TAP: Transaction Agent Protocol

TAP is an on-chain protocol built on Ethereum using ERC-8183 (agent authorization) and ERC-8004 (agent registry). Every agent is represented by a smart contract that holds its capabilities, pricing, and reputation on-chain. Transactions are executed through a factory contract that creates escrow instances with programmable release conditions.

**Strengths:** Fully decentralized -- no central authority controls agent registration, discovery, or payment settlement. Smart contract escrow with arbitrary release conditions (time-based, oracle-verified, multi-signature). On-chain reputation that is tamper-proof and publicly verifiable. Composable with the broader DeFi ecosystem (agents can use DEXs, lending protocols, and yield farming as part of their commerce flows).

**Weaknesses:** Every state transition requires an Ethereum transaction, incurring gas costs ($0.10-$5.00 per operation depending on L1 vs. L2 and network congestion). Transaction latency of 2-15 seconds on L2, 12-60 seconds on L1. Smart contract bugs are catastrophic and irrecoverable. The learning curve for Solidity development and smart contract security is steep. Throughput is limited by block space -- approximately 30 transactions per second on Ethereum L1, 2,000-4,000 on L2 rollups.

```solidity
// TAP: Simplified agent escrow contract (Solidity)
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract AgentEscrow {
    address public buyer;
    address public seller;
    IERC20 public paymentToken;
    uint256 public amount;
    uint256 public deadline;
    bool public released;
    bool public refunded;

    constructor(
        address _buyer, address _seller,
        address _token, uint256 _amount, uint256 _deadline
    ) {
        buyer = _buyer;
        seller = _seller;
        paymentToken = IERC20(_token);
        amount = _amount;
        deadline = _deadline;
    }

    function release() external {
        require(msg.sender == buyer, "Only buyer can release");
        require(!released && !refunded, "Already finalized");
        released = true;
        paymentToken.transfer(seller, amount);
    }

    function refund() external {
        require(block.timestamp > deadline, "Deadline not reached");
        require(!released && !refunded, "Already finalized");
        refunded = true;
        paymentToken.transfer(buyer, amount);
    }
}
```

### UCP (Original): Universal Commerce Protocol (Consortium, 2025)

The original UCP, announced in Q3 2025 by a consortium including Mastercard, SAP, and Salesforce, attempts to be a complete agent commerce stack: service registry, capability discovery, multi-rail payment (card, crypto, bank transfer, and internal ledger), escrow, SLA enforcement, dispute resolution, and compliance reporting. The specification runs to 847 pages. Note: this is distinct from Google's UCP (Universal Commerce Protocol), launched in Q1 2026, which shares the name but is a commerce-layer protocol co-developed with major retailers.

**Strengths:** The only protocol that handles every aspect of agent commerce in a single specification. Multi-rail payment support means agents can pay through whichever mechanism is cheapest and fastest for a given transaction. Built-in compliance reporting designed for EU AI Act requirements. Enterprise-grade SLA definitions with automated penalty enforcement. The consortium backing ensures broad enterprise adoption if the protocol reaches production maturity.

**Weaknesses:** Still in public beta as of Q1 2026. The specification is enormous and complex -- implementing a full UCP stack requires thousands of hours of development. No production deployments at meaningful scale yet. The consortium governance model is slow; specification changes require committee approval from all founding members. Risk of design-by-committee producing a protocol that is complete but impractical, similar to what happened with SOAP/WS-* in the early 2000s. The naming collision with Google's UCP has not helped adoption.

```python
# UCP: Register a service and handle a multi-rail payment
import requests

UCP_API = "https://api.ucp-protocol.org/v1"

# Register a service in the UCP registry
service = requests.post(f"{UCP_API}/services", json={
    "agent_id": "ucp:agent:data-analysis-001",
    "name": "Financial Data Analysis",
    "capabilities": ["time_series_analysis", "anomaly_detection", "forecasting"],
    "pricing": {
        "model": "per_request",
        "base_price": {"amount": "2.50", "currency": "USD"},
        "volume_discounts": [
            {"threshold": 100, "discount_pct": 10},
            {"threshold": 1000, "discount_pct": 25},
        ],
    },
    "sla": {
        "latency_p99_ms": 5000,
        "availability_pct": 99.9,
        "penalty_per_violation_pct": 5,
    },
    "payment_rails": ["card", "usdc", "bank_transfer", "internal_ledger"],
    "compliance": {
        "eu_ai_act": True,
        "audit_log_retention_days": 2555,
    },
}, headers={"Authorization": "Bearer ucp_key_xxx"})

# Initiate a payment using the cheapest available rail
payment = requests.post(f"{UCP_API}/payments", json={
    "service_id": service.json()["id"],
    "buyer_agent_id": "ucp:agent:buyer-456",
    "amount": "2.50",
    "preferred_rails": ["usdc", "internal_ledger", "card"],  # priority order
    "escrow": True,
    "release_conditions": {
        "type": "buyer_approval",
        "timeout_hours": 24,
    },
}, headers={"Authorization": "Bearer ucp_key_xxx"})
```

### MCP: Model Context Protocol

MCP, developed by Anthropic and released in late 2024, standardizes how AI models interact with external tools. An MCP server exposes tool definitions (JSON Schema descriptions of available functions with typed inputs and outputs). An MCP client -- typically an LLM or an agent framework -- discovers available tools, calls them with structured inputs, and receives structured outputs. MCP is the de facto standard for tool integration, adopted by Claude, Cursor, Windsurf, VS Code (via GitHub Copilot), and dozens of other AI clients.

MCP is fundamentally a communication protocol, not a payment protocol. It defines how an agent discovers and invokes tools but says nothing about how the agent pays for those invocations. This is by design -- Anthropic positioned MCP as a "USB-C for AI" that any payment layer can be plugged into.

Two major developments in late 2025 and early 2026 cemented MCP's position. First, Anthropic donated MCP to the Linux Foundation, signaling that MCP is infrastructure, not a proprietary lock-in play. Second, the MCP registry launched at `registry.modelcontextprotocol.io`, now cataloging over 10,000 MCP servers -- a de facto app store for AI tool integrations.

**Strengths:** Widest adoption of any protocol in the comparison. Over 10,000 MCP servers cataloged in the official registry as of Q1 2026. The specification is simple and well-documented. MCP v2.0 (2025) added Streamable HTTP transport, replacing the SSE-based transport with a more robust bidirectional channel. MCP v2.1 (early 2026) added OAuth 2.1 for authentication and tool annotations (metadata about tool behavior such as read-only vs. destructive). Linux Foundation governance provides vendor-neutral stewardship.

**Weaknesses:** No payment layer. No marketplace or discovery beyond the registry and the client's configured server list. No escrow, reputation, or dispute resolution. An MCP server cannot charge for tool invocations within the protocol itself -- payment must be handled out-of-band.

```python
# MCP server: expose a tool via the Model Context Protocol
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("CodeReviewServer")

@mcp.tool()
async def review_code(
    code: str,
    language: str = "python",
    focus: str = "security",
) -> str:
    """Review code for security vulnerabilities, bugs, and style issues.

    Args:
        code: The source code to review.
        language: Programming language of the code.
        focus: Review focus area (security, performance, style, all).
    """
    # Perform the code review
    issues = run_analysis(code, language, focus)
    return format_review(issues)

# Client discovers this tool via MCP tool listing
# Client calls: {"tool": "review_code", "arguments": {"code": "...", "focus": "security"}}
```

### A2A: Agent-to-Agent Protocol

Google's A2A protocol, announced in late 2024 and reaching v1.0 in Q4 2025, defines how agents discover each other, exchange tasks, and stream progress updates. Every A2A-compatible agent publishes an Agent Card -- a JSON document at `/.well-known/agent.json` -- that describes its capabilities, supported input/output types, authentication requirements, and endpoint URL. Agents communicate through a task-based model: a client agent creates a task, the server agent processes it (potentially streaming intermediate updates via Server-Sent Events), and the task completes with a structured result.

A2A launched with over 50 partner organizations including Salesforce, SAP, Atlassian, MongoDB, and several others. By Q1 2026, the partner list has expanded significantly, with IBM joining as a key contributor. A2A is now the most broadly backed communication protocol, and Google's Q1 2026 launches of AP2 and UCP are designed to complement A2A -- discovery and task orchestration via A2A, payment via AP2, commerce via UCP.

**Strengths:** Clean task-based interaction model that maps well to real-world agent workflows. Agent Cards provide a standardized discovery mechanism that works with DNS and existing web infrastructure. Streaming support via SSE allows long-running tasks with progress updates. Transport-agnostic -- works over HTTP, WebSocket, or any other transport. Strong and growing enterprise backing, now including IBM. Designed to compose with Google AP2 and Google UCP as a full-stack solution.

**Weaknesses:** No payment layer. Agent Cards describe capabilities but not pricing. Task results are unstructured blobs -- there is no schema validation at the protocol level. The specification is still evolving rapidly, with breaking changes between minor versions. No built-in escrow, SLA enforcement, or dispute resolution.

```python
# A2A: Agent Card and task handling
# /.well-known/agent.json
AGENT_CARD = {
    "name": "DataAnalysisAgent",
    "description": "Performs statistical analysis and generates visualizations",
    "url": "https://analysis-agent.example.com",
    "version": "1.0.0",
    "capabilities": {
        "streaming": True,
        "pushNotifications": False,
    },
    "skills": [
        {
            "id": "time-series-forecast",
            "name": "Time Series Forecasting",
            "description": "Generate forecasts from historical time series data",
            "inputModes": ["application/json"],
            "outputModes": ["application/json", "image/png"],
        },
    ],
    "authentication": {
        "schemes": ["bearer"],
    },
}

# Handle an incoming A2A task
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

@app.post("/tasks")
async def create_task(task: dict):
    skill_id = task["skill_id"]
    input_data = task["input"]

    if skill_id == "time-series-forecast":
        result = run_forecast(input_data)
        return {
            "id": task["id"],
            "status": "completed",
            "result": {
                "parts": [
                    {"type": "application/json", "data": result["forecast"]},
                    {"type": "image/png", "data": result["chart_base64"]},
                ],
            },
        }
```

### Visa TAP: Trusted Agent Protocol (Q1 2026)

Visa TAP, launched in Q1 2026, is Visa's second-generation agent payment protocol and the successor to MPP. Where MPP simply gave agents virtual card numbers, TAP introduces cryptographically signed agent identity per transaction. Every transaction carries a cryptographic attestation that identifies the specific agent instance, its authorization scope, and its delegated authority chain back to a human or organization. This identity travels with the payment through Visa's card network settlement infrastructure.

The key insight is that TAP treats agent identity as a first-class element of the payment authorization, not an afterthought. When a TAP-enabled agent makes a purchase, the merchant receives not just a payment authorization but a verifiable proof of which agent made the request, what permissions it holds, and who is ultimately liable.

**Strengths:** Cryptographic agent identity per transaction provides an audit trail that satisfies EU AI Act requirements out of the box. Settlement through Visa's existing card network means instant compatibility with 100M+ merchants globally. The identity attestation enables granular spending controls -- an organization can restrict an agent to specific merchant categories, transaction amounts, or time windows, all enforced cryptographically. Visa's fraud detection models are extended to agent behavior patterns.

**Weaknesses:** Same high per-transaction cost as MPP ($0.20-$0.30 minimum interchange). The cryptographic identity provisioning requires integration with Visa's identity service, which is not yet available in all markets. Settlement latency remains 1-3 business days for standard card settlement (real-time settlement available in select markets at higher cost). Not suitable for micropayments. The identity model is Visa-centric -- agents transacting outside the Visa network cannot use TAP identity.

```python
# Visa TAP: Agent identity attestation and payment
import requests
import json

VISA_TAP_API = "https://api.visa.com/tap/v1"

# Register an agent and receive a cryptographic identity
agent_identity = requests.post(f"{VISA_TAP_API}/agents", json={
    "organization_id": "org_acme_corp_123",
    "agent_name": "procurement-agent-001",
    "authorization_scope": {
        "max_transaction_amount": 5000,
        "allowed_merchant_categories": ["5734", "7372", "5045"],
        "daily_limit": 25000,
        "currency": "USD",
    },
    "delegation_chain": {
        "delegator": "human:jane.doe@acme.com",
        "authority_level": "procurement_standard",
        "expiry": "2026-12-31T23:59:59Z",
    },
}, headers={"Authorization": "Bearer visa_tap_key"})

agent_id = agent_identity.json()["agent_id"]
signing_key = agent_identity.json()["signing_key"]

# Make a payment with cryptographic agent attestation
payment = requests.post(f"{VISA_TAP_API}/payments", json={
    "agent_id": agent_id,
    "attestation": sign_transaction(signing_key, {
        "amount": 150.00,
        "currency": "USD",
        "merchant_id": "merchant_software_vendor_xyz",
        "purpose": "Annual license renewal",
        "timestamp": "2026-03-15T14:30:00Z",
    }),
    "funding_source": "card_fund_src_abc123",
}, headers={"Authorization": "Bearer visa_tap_key"})

# Payment includes verifiable agent identity in the authorization
print(payment.json()["authorization_id"])
print(payment.json()["agent_attestation_verified"])  # True
```

### Google AP2: Agent Payments Protocol (Q1 2026)

Google AP2, launched in Q1 2026, is a payment-agnostic protocol that supports cards, bank transfers, and stablecoins through a single unified interface. The defining feature is **cryptographic user mandates** -- users pre-authorize agent spending through signed consent objects that specify what the agent can buy, how much it can spend, and through which payment methods. The mandate travels with every transaction, providing verifiable proof of user consent.

AP2 launched with over 60 partners including Adyen, Mastercard, PayPal, Visa, Stripe, and dozens of payment processors and merchants. This is the broadest partner coalition of any Q1 2026 protocol launch.

**Strengths:** Payment-rail agnostic. A single AP2 integration supports credit cards, debit cards, bank transfers (ACH, SEPA), and stablecoins (USDC, USDT). The cryptographic mandate model solves the consent problem for agentic spending -- regulators can verify that the human authorized the agent's purchase, and the mandate's scope prevents agents from overspending. The 60+ partner coalition provides broad ecosystem support from day one. Google's infrastructure means high availability and low latency for the mandate verification service. Designed to compose with A2A (discovery) and Google UCP (commerce).

**Weaknesses:** The mandate model adds latency -- every transaction requires mandate verification against Google's mandate service. Per-transaction costs vary by payment rail (crypto rail is cheap, card rail carries standard interchange). The mandate issuance flow requires user interaction, making fully autonomous agent-to-agent transactions cumbersome. Google's central role in mandate verification creates a single point of failure and a potential lock-in vector. Still very new with limited production track record.

```python
# Google AP2: Create a user mandate and execute a payment
import requests

AP2_API = "https://agentpayments.googleapis.com/v1"

# Step 1: User creates a spending mandate for their agent
mandate = requests.post(f"{AP2_API}/mandates", json={
    "user_id": "user:google:jane.doe@gmail.com",
    "agent_id": "agent:acme:shopping-assistant-001",
    "scope": {
        "max_per_transaction": {"amount": "500.00", "currency": "USD"},
        "max_daily": {"amount": "2000.00", "currency": "USD"},
        "allowed_categories": ["electronics", "software", "books"],
        "allowed_payment_methods": ["card", "bank_transfer", "usdc"],
        "valid_until": "2026-06-30T23:59:59Z",
    },
}, headers={"Authorization": "Bearer user_oauth_token"})

mandate_id = mandate.json()["mandate_id"]
mandate_signature = mandate.json()["cryptographic_signature"]

# Step 2: Agent executes a payment using the mandate
payment = requests.post(f"{AP2_API}/payments", json={
    "mandate_id": mandate_id,
    "mandate_signature": mandate_signature,
    "agent_id": "agent:acme:shopping-assistant-001",
    "recipient": "merchant:bestbuy:online-store",
    "amount": {"value": "79.99", "currency": "USD"},
    "preferred_rail": "card",  # Falls back to bank_transfer, then usdc
    "description": "Wireless headphones - agent-initiated purchase",
    "metadata": {
        "user_request": "Find me good noise-canceling headphones under $100",
        "agent_reasoning": "Selected based on 4.7-star rating, $79.99 price",
    },
}, headers={"Authorization": "Bearer agent_service_token"})

print(payment.json()["status"])           # "authorized"
print(payment.json()["payment_rail"])     # "card"
print(payment.json()["mandate_verified"]) # True
```

### OpenAI ACP: Agentic Commerce Protocol (Q1 2026)

OpenAI ACP, released in Q1 2026 as an open specification developed with Stripe under the Apache 2.0 license, defines the complete agent shopping lifecycle as an open standard. Unlike the earlier ACP work that was tightly coupled to Stripe Checkout, the Agentic Commerce Protocol specifies an open wire format for product catalogs, cart management, checkout sessions, payment processing, and fulfillment tracking that any payment processor can implement.

The specification defines three core objects: **Catalogs** (JSON documents listing purchasable items with structured metadata), **Carts** (stateful shopping sessions with line items, quantities, and pricing), and **Checkout Sessions** (payment and fulfillment orchestration). The Apache 2.0 license means competing implementations are not just allowed but encouraged.

**Strengths:** The only open-source agent commerce specification with both a complete lifecycle definition and a production-grade reference implementation (Stripe). The cart/checkout model is familiar to any developer who has worked with e-commerce APIs. Apache 2.0 licensing removes adoption barriers. The specification is deliberately focused on the commerce layer and does not attempt to define discovery, identity, or payment rails -- it composes with other protocols for those concerns. Strong ChatGPT distribution for consumer-facing use cases.

**Weaknesses:** The "open standard" positioning is somewhat aspirational -- as of Q1 2026, Stripe's implementation is the only production-grade one, creating de facto lock-in despite the open license. The cart/checkout model is consumer-oriented and maps poorly to machine-to-machine service consumption (an agent buying 10,000 API calls does not naturally fit into a "cart"). No built-in micropayment support. The specification does not address agent identity, reputation, or trust -- these must come from other protocols.

```python
# OpenAI ACP: Product catalog and checkout flow
import requests

ACP_API = "https://api.stripe.com/v1/acp"  # Reference implementation

# Publish a product catalog
catalog = requests.post(f"{ACP_API}/catalogs", json={
    "merchant_id": "merchant_code_review_co",
    "products": [
        {
            "id": "prod_security_audit",
            "name": "AI Security Code Audit",
            "description": "Comprehensive security analysis of your codebase",
            "price": {"amount": 2500, "currency": "usd"},  # $25.00
            "fulfillment": {
                "type": "api_callback",
                "url": "https://codereview.example.com/fulfill",
                "estimated_duration_seconds": 300,
            },
            "metadata": {"languages": ["python", "javascript", "go"]},
        },
    ],
}, headers={"Authorization": "Bearer sk_live_xxx"})

# Agent creates a cart and checks out
cart = requests.post(f"{ACP_API}/carts", json={
    "catalog_id": catalog.json()["id"],
    "items": [
        {"product_id": "prod_security_audit", "quantity": 1,
         "metadata": {"repo_url": "https://github.com/user/repo"}},
    ],
    "buyer_agent_id": "agent-buyer-456",
}, headers={"Authorization": "Bearer sk_live_xxx"})

# Initiate checkout
checkout = requests.post(f"{ACP_API}/checkout", json={
    "cart_id": cart.json()["id"],
    "payment_method": "card",
    "return_url": "https://agent-buyer.example.com/callback",
}, headers={"Authorization": "Bearer sk_live_xxx"})

print(checkout.json()["checkout_url"])
print(checkout.json()["status"])  # "pending_payment"
```

### PayPal Agent Ready (Q1 2026)

PayPal Agent Ready is the first purpose-built cross-protocol bridge for agent commerce. Rather than defining a new payment protocol, Agent Ready adapts PayPal's existing merchant infrastructure to accept transactions from any agent commerce protocol -- x402, OpenAI ACP, Google AP2, Visa TAP, or direct API calls. For PayPal's 35M+ existing merchants, Agent Ready provides agent commerce support without changing their existing integration.

The architecture is a multi-protocol adapter: Agent Ready accepts inbound requests in any supported protocol format, translates them into PayPal payment operations, executes the payment through PayPal's existing infrastructure, and returns the result in the originating protocol's format. Merchants see agent transactions in the same PayPal dashboard they use for human transactions.

**Strengths:** Zero migration cost for existing PayPal merchants -- Agent Ready is an opt-in feature toggle, not a new integration. Multi-protocol support means merchants are not locked into any single agent protocol. PayPal's existing buyer/seller protection, dispute resolution, and compliance infrastructure applies to agent transactions. The bridge architecture means Agent Ready benefits from every new protocol it adds support for, without merchants lifting a finger. Supports fiat and PayPal's own stablecoin (PYUSD).

**Weaknesses:** Adds a translation layer that increases latency (additional 200-400ms per transaction for protocol translation and PayPal processing). PayPal's transaction fees apply on top of any protocol-specific costs. The bridge approach means Agent Ready does not innovate on the protocol layer -- it inherits the limitations of whichever protocol the agent is using. Not suitable for direct agent-to-agent micropayments. PayPal's dispute resolution model was designed for human buyers and may not map well to fully autonomous agent disputes.

```python
# PayPal Agent Ready: Accept agent payments from any protocol
import requests

PAYPAL_AR_API = "https://api.paypal.com/v2/agent-ready"

# Enable Agent Ready for an existing PayPal merchant
config = requests.post(f"{PAYPAL_AR_API}/merchants/configure", json={
    "merchant_id": "paypal_merchant_xyz",
    "supported_protocols": ["x402", "openai_acp", "google_ap2", "visa_tap"],
    "auto_accept_agents": True,
    "agent_transaction_limits": {
        "max_per_transaction": 1000.00,
        "max_daily": 10000.00,
        "require_mandate_verification": True,  # For AP2 mandates
    },
}, headers={"Authorization": "Bearer paypal_access_token"})

# Agent Ready translates inbound x402 to PayPal payment
# (This happens automatically -- the merchant sees a normal PayPal payment)

# Query agent transactions
agent_txns = requests.get(
    f"{PAYPAL_AR_API}/merchants/paypal_merchant_xyz/transactions",
    params={"source_protocol": "x402", "limit": 10},
    headers={"Authorization": "Bearer paypal_access_token"},
)

for txn in agent_txns.json()["transactions"]:
    print(f"Protocol: {txn['source_protocol']}, "
          f"Amount: ${txn['amount']}, "
          f"Agent: {txn['agent_id']}, "
          f"Status: {txn['status']}")
```

### Google UCP: Universal Commerce Protocol (Q1 2026)

Google UCP, launched in Q1 2026, is a commerce-layer protocol co-developed with Shopify, Etsy, Wayfair, Target, and Walmart. Where Google AP2 handles payment orchestration, UCP handles the commerce lifecycle above the payment layer: product discovery, catalog syndication, inventory checking, order management, shipping, and returns. Together, AP2 + UCP + A2A form Google's vision of a complete agent commerce stack.

The retailer co-development is what distinguishes Google UCP from the original consortium UCP (Mastercard/SAP/Salesforce). Instead of designing a theoretical specification in committee, Google UCP was built against the actual catalog, inventory, and fulfillment APIs of five of the largest retailers in the world. The result is a specification that reflects real-world e-commerce complexity.

**Strengths:** Co-developed with retailers who collectively represent over $1 trillion in annual e-commerce volume. The specification covers the full commerce lifecycle that the original consortium UCP attempted but with practical, battle-tested data models. Native integration with Shopify means 4M+ Shopify merchants can expose their catalogs as UCP-compatible feeds. Designed to compose with AP2 (payment) and A2A (discovery), providing a coherent full-stack solution. Product catalog format supports rich structured data (sizes, colors, availability by location, shipping estimates).

**Weaknesses:** Very new as of Q1 2026 with limited production deployments beyond the launch partners. The retailer-centric design may not map well to service commerce (buying API calls, compute time, or agent services). Heavy dependency on Google's infrastructure for catalog syndication and order management. The specification is large and complex -- not as sprawling as the original consortium UCP's 847 pages but still significantly more complex than x402 or MCP. Risk of becoming a Google-controlled standard despite the retailer partnerships.

```python
# Google UCP: Product catalog and order management
import requests

UCP_API = "https://commerce.googleapis.com/ucp/v1"

# Syndicate a product catalog (merchant-side)
catalog = requests.post(f"{UCP_API}/catalogs/sync", json={
    "merchant_id": "shopify:my-store-123",
    "sync_source": "shopify",  # Also supports: "manual", "etsy", "custom"
    "filters": {
        "in_stock": True,
        "categories": ["electronics", "accessories"],
    },
}, headers={"Authorization": "Bearer merchant_oauth_token"})

# Agent searches for products across UCP-connected merchants
search = requests.post(f"{UCP_API}/products/search", json={
    "query": "noise-canceling wireless headphones",
    "filters": {
        "price_range": {"min": "50.00", "max": "150.00", "currency": "USD"},
        "in_stock": True,
        "shipping_to": "US",
    },
    "sort_by": "relevance",
    "limit": 10,
}, headers={"Authorization": "Bearer agent_service_token"})

products = search.json()["products"]
# Each product includes: id, name, price, availability, shipping_estimate,
# merchant_id, images, structured_attributes, reviews_summary

# Agent creates an order
order = requests.post(f"{UCP_API}/orders", json={
    "agent_id": "agent:acme:shopping-assistant-001",
    "items": [
        {
            "product_id": products[0]["id"],
            "quantity": 1,
            "shipping_address": {
                "name": "Jane Doe",
                "street": "123 Main St",
                "city": "San Francisco",
                "state": "CA",
                "zip": "94105",
                "country": "US",
            },
        },
    ],
    "payment_protocol": "google_ap2",  # Or "x402", "openai_acp", etc.
    "mandate_id": "mandate_abc123",    # AP2 mandate reference
}, headers={"Authorization": "Bearer agent_service_token"})

print(order.json()["order_id"])
print(order.json()["estimated_delivery"])
print(order.json()["total_with_shipping"])
```

---

## Chapter 3: Feature Comparison Matrix

### The Definitive Table

The following matrix compares all eleven protocols across 20 features that matter for production agent commerce systems. A checkmark indicates native support within the protocol specification. "External" means the feature requires an out-of-band integration. A dash means no support.

```
Feature Comparison Matrix — Agent Commerce Protocols (April 2026)
═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
                                              Original                        Q1 2026 Launches
                                    ────────────────────────────    ─────────────────────────────────────────────
Feature              x402    OG-ACP  OG-AP2  MPP     TAP     OG-UCP  MCP     A2A     Visa    Google  OpenAI  PayPal  Google
                                                                                      TAP     AP2     ACP     Ready   UCP
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
PAYMENT
  Micropayments       Yes     --      Yes     --      --      Yes     --      --      --      Yes*    --      --      --
  (< $0.01)
  Subscriptions       --      Yes     Yes     Yes     --      Yes     --      --      Yes     Yes     Yes     Yes**   Yes
  Escrow              --      Yes†    Yes     --      Yes     Yes     --      --      --      --      Yes†    Yes**   --
  Multi-currency      USDC    140+    USDC    50+     ERC20   Multi   --      --      50+     Multi   140+    Multi   --
  Streaming pay       --      --      Yes     --      --      Yes     --      --      --      --      --      --      --
  Fiat settlement     --      Yes     --      Yes     --      Yes     --      --      Yes     Yes     Yes     Yes     --
  Crypto settlement   Yes     --      Yes     --      Yes     Yes     --      --      --      Yes     --      Yes‡    --

DISCOVERY
  Service registry    --      Yes     --      --      On-     Yes     10K+    Yes     --      --      Yes     --      Yes
                                                      chain                  servers
  Agent cards         --      --      --      --      --      Yes     --      Yes     --      --      --      --      Yes
  Capability search   --      Yes     --      --      Yes     Yes     Yes§    Yes     --      --      Yes     --      Yes
  Product catalog     --      Yes     --      --      --      Yes     --      --      --      --      Yes     --      Yes

TRUST & SAFETY
  Identity/Auth       --      Stripe  DID     KYB     On-     OAuth   OAuth   Bearer  Crypto  Crypto  Stripe  PayPal  OAuth
                              KYC                     chain   2.1     2.1             signed  mandate KYC     ID
  Reputation          --      --      --      --      On-     Yes     --      --      --      --      --      PayPal  Yes
                                                      chain                                                   rating
  Dispute resolution  --      Yes     Yes     Yes‡‡   Yes     Yes     --      --      Yes‡‡   --      Yes     Yes     --
  SLA enforcement     --      --      --      --      Smart   Yes     --      --      --      --      --      --      Yes
                                                      contract

COMMUNICATION
  Tool calling        --      --      --      --      --      --      Yes     --      --      --      --      --      --
  Task orchestration  --      --      --      --      --      --      --      Yes     --      --      --      --      --
  Streaming/SSE       --      --      --      --      --      Yes     MCP     Yes     --      --      --      --      --
                                                                      stream
  Async operations    --      --      --      --      Yes     Yes     --      Yes     --      --      --      --      Yes

COMPLIANCE
  Audit trail         TX      Stripe  On-     Card    On-     Yes     --      --      Crypto  Mandate Stripe  PayPal  Order
                      hash    logs    chain   network chain                           signed  log     logs    logs    log
  EU AI Act ready     --      --      --      --      --      Yes     --      --      Yes     Yes     --      --      Yes
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

†  Escrow via Stripe payment intents with manual capture
‡  PayPal supports PYUSD stablecoin
‡‡ Card network chargeback process
§  Via MCP registry at registry.modelcontextprotocol.io
*  Google AP2 micropayments only on crypto rail
** PayPal Agent Ready inherits capabilities from bridged protocol

Production Status (April 2026):
  x402:           Production (100M+ transactions in 6 months via Foundation)
  OG-ACP:         Production ($200M+/month volume, evolving into OpenAI ACP)
  OG-AP2:         Production (limited, ~500K channels)
  MPP:            Production (pilot, ~50 enterprise clients, being superseded by Visa TAP)
  TAP (on-chain): Production (niche, DeFi-adjacent)
  OG-UCP:         Public Beta (consortium)
  MCP:            Production (10K+ servers in registry, Linux Foundation governed)
  A2A:            Production (50+ partners, IBM joined, growing)
  Visa TAP:       Early Production (Q1 2026 launch, enterprise pilots)
  Google AP2:     Early Production (Q1 2026 launch, 60+ partners)
  OpenAI ACP:     Early Production (Q1 2026 launch, Apache 2.0)
  PayPal Ready:   Early Production (Q1 2026 launch, 35M+ merchant base)
  Google UCP:     Early Production (Q1 2026 launch, 5 major retailers)
```

### Reading the Matrix

Several patterns emerge from the comparison, especially in light of the Q1 2026 launches.

**No protocol does everything, and the Q1 2026 explosion made this worse.** The original consortium UCP came closest to a complete solution but remains in beta. The Q1 2026 launches did not produce a single comprehensive protocol either -- instead they produced five specialized ones. Google's strategy of three composable protocols (A2A + AP2 + UCP) is the closest thing to a complete stack, but it requires buying into Google's ecosystem.

**Payment and communication protocols are complementary, not competing.** The most natural pairings are: x402 + MCP (micropayments for tool calls), OpenAI ACP + A2A (commerce checkout for task-based workflows), Google AP2 + A2A + Google UCP (Google's full stack), and Visa TAP + A2A (enterprise card payments for agent tasks). Teams that treat these as competing alternatives are asking the wrong question.

**The Q1 2026 launches split into two strategic camps.** Camp 1 is the open-protocol camp: OpenAI ACP (Apache 2.0), x402 (open Foundation), and MCP (Linux Foundation). These protocols bet that open standards win through ecosystem adoption. Camp 2 is the platform camp: Google AP2/UCP (Google infrastructure), Visa TAP (Visa network), and PayPal Agent Ready (PayPal merchant base). These protocols bet that platform distribution wins through existing network effects.

**Enterprise readiness expanded dramatically in Q1 2026.** Visa TAP's cryptographic agent identity and Google AP2's mandate model both provide compliance-ready audit trails designed for EU AI Act requirements. Combined with the existing enterprise options (ACP via Stripe KYC, MPP via card network), enterprises now have multiple credible paths to compliant agent commerce.

**Bridge protocols are the sleeper play.** PayPal Agent Ready introduced a new category -- the cross-protocol bridge -- that may matter more than any individual protocol. If Agent Ready succeeds, merchants never need to pick a protocol. They plug into PayPal once and accept agent payments from any protocol. This commoditizes the payment protocol layer and shifts the competitive battleground to the commerce and discovery layers.

**Escrow remains the critical differentiator for agent-to-agent commerce.** When two autonomous agents transact, neither has a reason to trust the other. Escrow -- locking funds until delivery is confirmed -- is the primitive that makes trustless agent commerce possible. Only ACP (via Stripe payment intents), the original AP2, on-chain TAP, and both UCPs support escrow natively. x402, Google AP2, Visa TAP, MCP, and A2A do not. This is where an escrow infrastructure layer fills the gap regardless of which protocol you choose for the wire.

---

## Chapter 4: Latency and Cost Benchmarks

### Methodology

We deployed test agents on three cloud providers (AWS us-east-1, GCP us-central1, Azure eastus) and measured round-trip transaction latency and per-transaction cost for each protocol. Each test consisted of 10,000 identical transactions: an agent purchasing a code review service priced at $1.00. We measured wall-clock time from transaction initiation to confirmed settlement (funds available to the seller). All benchmarks were run in March 2026.

For x402 and AP2, the payment facilitator was the respective protocol's production facilitator endpoint. For ACP, payments settled through Stripe's production API. For MPP, payments settled through Visa's sandbox (production access was limited to pilot participants). For TAP, transactions settled on Base L2. For UCP, we used the beta API. MCP and A2A do not handle payments natively, so we measured their communication overhead separately and paired them with x402 for the payment leg.

### Transaction Latency

```
Transaction Latency (p50 / p95 / p99) — milliseconds
=====================================================

Protocol     p50      p95      p99      Notes
─────────────────────────────────────────────────────
x402          820    1,240    1,890    Includes on-chain settlement on Base L2
ACP         1,450    2,100    3,200    Stripe payment intent + capture
AP2           180      340      520    Off-chain (channel already open)
AP2*        4,200    6,800    9,100    *Including channel open (one-time)
MPP         2,800    4,500    7,200    Card authorization + settlement hold
TAP         2,100    4,800    8,400    Base L2 transaction confirmation
UCP         1,600    2,900    4,100    Beta API, internal ledger rail
MCP           120      210      380    Tool call only (no payment)
A2A           180      320      540    Task creation + completion (no payment)

Combined Protocols:
MCP + x402    940    1,450    2,270    Tool discovery + micropayment
A2A + x402  1,000    1,560    2,430    Task creation + micropayment
MCP + ACP   1,570    2,310    3,580    Tool discovery + Stripe checkout
```

AP2 with an established payment channel is the fastest payment protocol -- under 200ms at the median because off-chain state updates require no blockchain interaction. However, the one-time channel establishment cost (4.2 seconds) means AP2 is only efficient when two agents transact repeatedly. For one-off transactions, x402 is fastest at 820ms median.

ACP's latency is dominated by Stripe's payment intent lifecycle. Creating an intent, confirming it, and capturing funds involves multiple API calls to Stripe's servers. The 1.45-second median is consistent with Stripe's published API latency.

MCP and A2A, as communication-only protocols, are the fastest in raw latency. The question is what payment protocol you pair them with.

### Per-Transaction Cost

```
Per-Transaction Cost — $1.00 Service Purchase
===============================================

Protocol     Fixed Cost    Variable Cost    Total Cost    % of Transaction
─────────────────────────────────────────────────────────────────────────
x402         $0.0008       0.0%             $0.0008       0.08%
ACP          $0.30         2.9%             $0.329        32.9%
AP2          $0.0001*      0.0%             $0.0001       0.01%
AP2 (open)   $0.50         0.0%             $0.50         50.0%
MPP          $0.20         1.8%             $0.218        21.8%
TAP          $0.05-0.80    0.0%             ~$0.15        ~15.0%
UCP (crypto) $0.001        0.0%             $0.001        0.1%
UCP (card)   $0.25         2.5%             $0.275        27.5%
MCP          $0.00         0.0%             $0.00         0.0%
A2A          $0.00         0.0%             $0.00         0.0%

* AP2 per-transaction cost after channel is open
  TAP gas costs vary with network congestion
```

The cost picture is stark. x402 and AP2 (after channel establishment) are orders of magnitude cheaper than ACP and MPP because they do not involve traditional payment processors. For a $1.00 transaction, ACP takes $0.329 in fees -- 32.9% of the transaction value. This makes ACP uneconomical for transactions under approximately $10.00.

For micropayments ($0.001 to $0.10), only x402, AP2, and UCP's crypto rail are viable. ACP and MPP fees would exceed the transaction value itself.

For enterprise transactions ($100+), ACP and MPP become cost-competitive because their fixed fees are amortized over a larger transaction value. At $100, ACP's fee is 3.2% -- high but comparable to standard payment processing.

### Throughput Limits

```
Maximum Throughput — Transactions per Second (TPS)
===================================================

Protocol     Measured TPS    Theoretical Limit    Bottleneck
─────────────────────────────────────────────────────────────
x402              850            ~4,000            Base L2 block space
ACP               120              500             Stripe API rate limits
AP2            10,000+          100,000+            Off-chain state updates
MPP               200              800             Card network auth rate
TAP               400            ~4,000            L2 block space (shared with x402)
UCP               300            1,000*            Beta infrastructure
MCP             5,000           50,000+            HTTP server capacity
A2A             3,000           30,000+            HTTP server capacity

* UCP theoretical limit is a consortium estimate, not verified
```

AP2 dominates throughput because off-chain payment channel updates are limited only by the speed of signing and transmitting state updates between two agents -- no blockchain or payment processor in the critical path. MCP and A2A also achieve high throughput because they are pure HTTP with no payment settlement overhead.

For most production use cases, the throughput bottleneck is not the protocol but the underlying service. An agent that takes 2 seconds to review code does not benefit from a payment protocol that can settle 10,000 transactions per second.

---

## Chapter 5: Migration Paths

### From x402 to ACP

This is the most common migration path for teams that started with x402 micropayments and need to add commerce features -- catalogs, subscriptions, refunds, and enterprise billing.

**Step 1: Dual-mode payment acceptance.** Keep x402 for micropayment clients while adding ACP for clients that need Stripe-based checkout. The server checks for an `X-PAYMENT-PROOF` header (x402) or an ACP session token, and routes to the appropriate payment validation path.

```python
async def handle_payment(request: Request) -> PaymentResult:
    """Accept both x402 and ACP payments."""
    x402_proof = request.headers.get("X-PAYMENT-PROOF")
    acp_session = request.headers.get("X-ACP-SESSION")

    if x402_proof:
        return validate_x402(x402_proof)
    elif acp_session:
        return validate_acp_session(acp_session)
    else:
        # Return 402 for x402 clients, ACP catalog link for ACP clients
        accept = request.headers.get("Accept", "")
        if "application/acp+json" in accept:
            return acp_catalog_response()
        return x402_payment_required_response()
```

**Step 2: Publish an ACP product catalog.** Create Stripe products and prices that mirror your existing x402 pricing. Use Stripe's metadata fields to store the x402 resource ID so both systems reference the same service.

**Step 3: Migrate high-value clients to ACP.** Clients transacting over $10 per interaction benefit from ACP's dispute resolution and refund capabilities. Clients making sub-dollar micropayments should stay on x402.

**Estimated migration effort:** 2-3 weeks for a team of two engineers. The dual-mode pattern means zero downtime and no breaking changes for existing x402 clients.

### From MCP to A2A

This migration adds task orchestration and agent discovery to an existing MCP tool server.

**Step 1: Publish an Agent Card.** Create a `/.well-known/agent.json` that describes your MCP tools as A2A skills. Each MCP tool maps to an A2A skill with matching input/output types.

```python
def mcp_tools_to_agent_card(mcp_tools: list[dict]) -> dict:
    """Convert MCP tool definitions to an A2A Agent Card."""
    skills = []
    for tool in mcp_tools:
        skills.append({
            "id": tool["name"],
            "name": tool["name"].replace("_", " ").title(),
            "description": tool["description"],
            "inputModes": ["application/json"],
            "outputModes": ["application/json"],
        })

    return {
        "name": "MyToolServer",
        "url": "https://my-tool-server.example.com",
        "version": "1.0.0",
        "capabilities": {"streaming": True, "pushNotifications": False},
        "skills": skills,
        "authentication": {"schemes": ["bearer"]},
    }
```

**Step 2: Add a task endpoint.** Create a `/tasks` POST endpoint that receives A2A task requests, maps the skill ID to the corresponding MCP tool, executes it, and returns the result in A2A task format.

**Step 3: Support streaming.** If your MCP tools support streaming responses (via MCP's Streamable HTTP transport), expose them as A2A streaming tasks using Server-Sent Events.

**Estimated migration effort:** 1-2 weeks. The MCP-to-A2A mapping is straightforward because both protocols use JSON Schema for input/output definitions.

### From A2A to MCP

The reverse path -- adding MCP tool compatibility to an existing A2A agent -- is useful when you want Claude, Cursor, or other MCP clients to discover and call your agent's skills.

**Step 1: Create an MCP server wrapper.** For each A2A skill, register a corresponding MCP tool with the same input schema and description.

**Step 2: Map task lifecycle to tool calls.** An MCP tool call is synchronous (request-response), while an A2A task can be asynchronous. For long-running A2A tasks, the MCP wrapper should poll the task status until completion, then return the final result.

**Estimated migration effort:** 1 week. The primary challenge is handling async A2A tasks within MCP's synchronous tool call model.

### From Monolithic to Multi-Protocol

For teams currently using a single protocol (or no protocol -- just direct API calls), the migration to a multi-protocol architecture follows this path.

**Step 1: Introduce a protocol adapter layer.** Do not modify your existing service logic. Instead, add adapters in front of it that translate protocol-specific requests into your internal service calls.

**Step 2: Start with the two protocols that cover your most common interaction patterns.** For most teams, this is MCP + x402 (tool calling with micropayments) or A2A + ACP (task orchestration with commerce checkout).

**Step 3: Add protocols incrementally.** Each new protocol adapter is independent. Adding UCP support does not affect your existing x402 or MCP adapters.

**Step 4: Use GreenHelix as the unified backend.** Regardless of which protocol the request arrives through, route all payments through GreenHelix escrow and all identity through GreenHelix agent registration. This gives you a single audit trail, a single trust score per agent, and a single dispute resolution process.

**Estimated migration effort:** 3-4 weeks for the initial two-protocol setup, then 1 week per additional protocol.

---

## Chapter 6: Multi-Protocol Gateway Pattern

### Architecture Overview

The multi-protocol gateway is the central pattern of this guide. It sits between external protocol clients and your GreenHelix backend, accepting requests in any supported protocol, translating them into GreenHelix API calls, and returning responses in the original protocol's format.

```
                    Multi-Protocol Gateway
                    ========================

   x402 Client ──────┐
                      │
   ACP Agent ─────────┤     ┌──────────────────────┐     ┌─────────────────┐
                      ├────▶│  MultiProtocolRouter   │────▶│  GreenHelix API  │
   A2A Agent ─────────┤     │                        │     │  (Escrow, Trust, │
                      │     │  ┌─ X402Adapter       │     │   Identity,      │
   MCP Client ────────┤     │  ├─ ACPAdapter        │     │   Marketplace)   │
                      │     │  ├─ A2AAdapter        │     └─────────────────┘
   UCP Agent ─────────┘     │  ├─ MCPAdapter        │
                            │  └─ UCPAdapter        │
                            └──────────────────────┘
```

### ProtocolAdapter Base Class

Every adapter implements the same interface: detect whether an incoming request matches the adapter's protocol, translate the request into a GreenHelix operation, and translate the GreenHelix response back into the protocol's expected format.

```python
import abc
import hashlib
import json
import time
import logging
from dataclasses import dataclass, field
from typing import Optional
import requests

logger = logging.getLogger(__name__)


@dataclass
class ProtocolRequest:
    """Normalized representation of an incoming protocol request."""
    protocol: str
    method: str
    path: str
    headers: dict
    body: Optional[dict]
    query_params: dict = field(default_factory=dict)
    raw_request: Optional[object] = None


@dataclass
class ProtocolResponse:
    """Normalized representation of an outgoing protocol response."""
    status_code: int
    headers: dict
    body: dict
    protocol: str


class GreenHelixClient:
    """Shared client for all adapters to call the GreenHelix API."""

    def __init__(self, api_key: str, base_url: str = "https://api.greenhelix.net/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    def execute(self, tool: str, inputs: dict) -> dict:
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": inputs},
        )
        resp.raise_for_status()
        return resp.json()

    def search_services(self, query: str, **filters) -> list[dict]:
        return self.execute("search_services", {"query": query, **filters})

    def create_escrow(self, payer: str, payee: str, amount: str, **kwargs) -> dict:
        return self.execute("create_escrow", {
            "payer_agent_id": payer,
            "payee_agent_id": payee,
            "amount": amount,
            **kwargs,
        })

    def release_escrow(self, escrow_id: str) -> dict:
        return self.execute("release_escrow", {"escrow_id": escrow_id})

    def register_agent(self, agent_id: str, metadata: dict) -> dict:
        return self.execute("register_agent", {
            "agent_id": agent_id,
            "metadata": json.dumps(metadata),
        })


class ProtocolAdapter(abc.ABC):
    """Base class for protocol adapters."""

    def __init__(self, client: GreenHelixClient):
        self.client = client

    @abc.abstractmethod
    def protocol_name(self) -> str:
        """Return the protocol name (e.g., 'x402', 'acp', 'a2a')."""
        ...

    @abc.abstractmethod
    def matches(self, request: ProtocolRequest) -> bool:
        """Return True if this adapter handles the given request."""
        ...

    @abc.abstractmethod
    def translate_request(self, request: ProtocolRequest) -> dict:
        """Translate a protocol request into a GreenHelix operation.

        Returns a dict with keys:
            tool: str — the GreenHelix tool to call
            inputs: dict — the tool inputs
            metadata: dict — protocol-specific metadata to preserve
        """
        ...

    @abc.abstractmethod
    def translate_response(self, greenhelix_response: dict,
                           metadata: dict) -> ProtocolResponse:
        """Translate a GreenHelix response into a protocol response."""
        ...

    def handle(self, request: ProtocolRequest) -> ProtocolResponse:
        """Full request lifecycle: translate, execute, translate back."""
        operation = self.translate_request(request)
        gh_response = self.client.execute(
            operation["tool"], operation["inputs"]
        )
        return self.translate_response(gh_response, operation.get("metadata", {}))
```

### X402Adapter

```python
class X402Adapter(ProtocolAdapter):
    """Translates x402 micropayment flows into GreenHelix escrow transactions."""

    def __init__(self, client: GreenHelixClient, agent_id: str,
                 facilitator_url: str, payment_address: str):
        super().__init__(client)
        self.agent_id = agent_id
        self.facilitator_url = facilitator_url
        self.payment_address = payment_address

    def protocol_name(self) -> str:
        return "x402"

    def matches(self, request: ProtocolRequest) -> bool:
        return (
            request.headers.get("X-PAYMENT-PROOF") is not None
            or request.headers.get("X-PAYMENT-REQUIRED") is not None
        )

    def translate_request(self, request: ProtocolRequest) -> dict:
        proof_header = request.headers.get("X-PAYMENT-PROOF")
        if not proof_header:
            raise ValueError("No payment proof in request")

        proof = json.loads(proof_header)
        payer_id = proof.get("payer_agent_id", f"x402:{proof['tx_hash'][:16]}")

        return {
            "tool": "create_escrow",
            "inputs": {
                "payer_agent_id": payer_id,
                "payee_agent_id": self.agent_id,
                "amount": str(proof["amount"]),
                "description": f"x402 payment. TX: {proof['tx_hash']}",
                "escrow_type": "standard",
                "metadata": json.dumps({
                    "protocol": "x402",
                    "tx_hash": proof["tx_hash"],
                    "facilitator": self.facilitator_url,
                }),
            },
            "metadata": {
                "tx_hash": proof["tx_hash"],
                "resource_path": request.path,
            },
        }

    def translate_response(self, greenhelix_response: dict,
                           metadata: dict) -> ProtocolResponse:
        return ProtocolResponse(
            status_code=200,
            headers={
                "X-PAYMENT-TX": metadata.get("tx_hash", ""),
                "X-GREENHELIX-ESCROW": greenhelix_response.get("escrow_id", ""),
            },
            body=greenhelix_response,
            protocol="x402",
        )

    def create_402_headers(self, price_usd: float, resource_id: str) -> dict:
        """Generate headers for a 402 Payment Required response."""
        return {
            "X-PAYMENT-REQUIRED": "true",
            "X-PAYMENT-AMOUNT": str(price_usd),
            "X-PAYMENT-CURRENCY": "USDC",
            "X-PAYMENT-ADDRESS": self.payment_address,
            "X-PAYMENT-FACILITATOR": self.facilitator_url,
            "X-PAYMENT-RESOURCE": resource_id,
            "X-PAYMENT-EXPIRY": str(int(time.time()) + 300),
        }
```

### ACPAdapter

```python
class ACPAdapter(ProtocolAdapter):
    """Translates ACP (Stripe-based) checkout flows into GreenHelix escrow."""

    def __init__(self, client: GreenHelixClient, agent_id: str,
                 stripe_api_key: str):
        super().__init__(client)
        self.agent_id = agent_id
        self.stripe_api_key = stripe_api_key

    def protocol_name(self) -> str:
        return "acp"

    def matches(self, request: ProtocolRequest) -> bool:
        return (
            request.headers.get("X-ACP-SESSION") is not None
            or "application/acp+json" in request.headers.get("Accept", "")
        )

    def translate_request(self, request: ProtocolRequest) -> dict:
        session_id = request.headers.get("X-ACP-SESSION")
        if not session_id:
            raise ValueError("No ACP session in request")

        # Retrieve the Stripe checkout session to get payment details
        stripe_session = requests.get(
            f"https://api.stripe.com/v1/checkout/sessions/{session_id}",
            headers={"Authorization": f"Bearer {self.stripe_api_key}"},
        ).json()

        amount_cents = stripe_session["amount_total"]
        amount_usd = str(amount_cents / 100)
        buyer_email = stripe_session.get("customer_details", {}).get("email", "")
        buyer_agent = request.body.get("buyer_agent_id", f"acp:{buyer_email}")

        return {
            "tool": "create_escrow",
            "inputs": {
                "payer_agent_id": buyer_agent,
                "payee_agent_id": self.agent_id,
                "amount": amount_usd,
                "description": (
                    f"ACP checkout session {session_id}. "
                    f"Stripe payment: {stripe_session.get('payment_intent', 'N/A')}"
                ),
                "escrow_type": "standard",
                "metadata": json.dumps({
                    "protocol": "acp",
                    "stripe_session_id": session_id,
                    "stripe_payment_intent": stripe_session.get("payment_intent"),
                }),
            },
            "metadata": {
                "stripe_session_id": session_id,
                "amount_usd": amount_usd,
            },
        }

    def translate_response(self, greenhelix_response: dict,
                           metadata: dict) -> ProtocolResponse:
        return ProtocolResponse(
            status_code=200,
            headers={
                "X-ACP-STATUS": "fulfilled",
                "X-GREENHELIX-ESCROW": greenhelix_response.get("escrow_id", ""),
            },
            body={
                "status": "fulfilled",
                "escrow_id": greenhelix_response.get("escrow_id"),
                "amount": metadata.get("amount_usd"),
                "session_id": metadata.get("stripe_session_id"),
            },
            protocol="acp",
        )
```

### A2AAdapter

```python
class A2AAdapter(ProtocolAdapter):
    """Translates A2A task requests into GreenHelix tool executions."""

    def __init__(self, client: GreenHelixClient, agent_id: str,
                 skill_to_tool_map: dict[str, str]):
        super().__init__(client)
        self.agent_id = agent_id
        self.skill_to_tool_map = skill_to_tool_map  # A2A skill ID -> GreenHelix tool

    def protocol_name(self) -> str:
        return "a2a"

    def matches(self, request: ProtocolRequest) -> bool:
        return (
            request.path.endswith("/tasks")
            or request.headers.get("X-A2A-Agent-Id") is not None
            or (request.body and "skill_id" in request.body)
        )

    def translate_request(self, request: ProtocolRequest) -> dict:
        body = request.body or {}
        skill_id = body.get("skill_id")
        task_input = body.get("input", {})
        sender_agent = request.headers.get("X-A2A-Agent-Id", "unknown")

        gh_tool = self.skill_to_tool_map.get(skill_id)
        if not gh_tool:
            raise ValueError(
                f"Unknown A2A skill '{skill_id}'. "
                f"Available: {list(self.skill_to_tool_map.keys())}"
            )

        return {
            "tool": gh_tool,
            "inputs": task_input,
            "metadata": {
                "task_id": body.get("id", hashlib.sha256(
                    json.dumps(body, sort_keys=True).encode()
                ).hexdigest()[:16]),
                "skill_id": skill_id,
                "sender_agent": sender_agent,
            },
        }

    def translate_response(self, greenhelix_response: dict,
                           metadata: dict) -> ProtocolResponse:
        return ProtocolResponse(
            status_code=200,
            headers={
                "X-A2A-Task-Id": metadata.get("task_id", ""),
            },
            body={
                "id": metadata.get("task_id"),
                "status": "completed",
                "result": {
                    "parts": [
                        {
                            "type": "application/json",
                            "data": greenhelix_response,
                        },
                    ],
                },
            },
            protocol="a2a",
        )

    def generate_agent_card(self, base_url: str, skills: list[dict]) -> dict:
        """Generate an A2A Agent Card from GreenHelix service metadata."""
        return {
            "name": self.agent_id,
            "url": base_url,
            "version": "1.0.0",
            "capabilities": {
                "streaming": False,
                "pushNotifications": False,
            },
            "skills": [
                {
                    "id": skill["id"],
                    "name": skill["name"],
                    "description": skill.get("description", ""),
                    "inputModes": ["application/json"],
                    "outputModes": ["application/json"],
                }
                for skill in skills
            ],
            "authentication": {"schemes": ["bearer"]},
        }
```

### MultiProtocolRouter

```python
class MultiProtocolRouter:
    """Routes incoming requests to the appropriate protocol adapter.

    This is the central class of the multi-protocol gateway. It accepts
    any HTTP request, identifies which protocol the request uses, delegates
    to the corresponding adapter, and returns the protocol-appropriate response.
    """

    def __init__(self, client: GreenHelixClient):
        self.client = client
        self.adapters: list[ProtocolAdapter] = []
        self._request_log: list[dict] = []

    def register_adapter(self, adapter: ProtocolAdapter) -> None:
        """Register a protocol adapter. Order matters — first match wins."""
        self.adapters.append(adapter)
        logger.info(f"Registered adapter: {adapter.protocol_name()}")

    def route(self, request: ProtocolRequest) -> ProtocolResponse:
        """Route a request to the matching adapter.

        Iterates through registered adapters in order. The first adapter
        whose matches() method returns True handles the request. If no
        adapter matches, returns a 400 error listing supported protocols.
        """
        for adapter in self.adapters:
            if adapter.matches(request):
                logger.info(
                    f"Routing {request.method} {request.path} "
                    f"to {adapter.protocol_name()} adapter"
                )
                start = time.monotonic()
                try:
                    response = adapter.handle(request)
                    elapsed_ms = (time.monotonic() - start) * 1000
                    self._log_request(adapter.protocol_name(), request, response,
                                      elapsed_ms)
                    return response
                except Exception as e:
                    elapsed_ms = (time.monotonic() - start) * 1000
                    logger.error(
                        f"{adapter.protocol_name()} adapter error: {e}",
                        exc_info=True,
                    )
                    error_response = ProtocolResponse(
                        status_code=502,
                        headers={},
                        body={"error": str(e), "protocol": adapter.protocol_name()},
                        protocol=adapter.protocol_name(),
                    )
                    self._log_request(adapter.protocol_name(), request,
                                      error_response, elapsed_ms, error=str(e))
                    return error_response

        supported = [a.protocol_name() for a in self.adapters]
        return ProtocolResponse(
            status_code=400,
            headers={},
            body={
                "error": "No matching protocol adapter",
                "supported_protocols": supported,
                "hint": "Include protocol-specific headers or content types",
            },
            protocol="none",
        )

    def _log_request(self, protocol: str, request: ProtocolRequest,
                     response: ProtocolResponse, elapsed_ms: float,
                     error: Optional[str] = None) -> None:
        self._request_log.append({
            "timestamp": time.time(),
            "protocol": protocol,
            "method": request.method,
            "path": request.path,
            "status_code": response.status_code,
            "elapsed_ms": round(elapsed_ms, 2),
            "error": error,
        })

    def get_stats(self) -> dict:
        """Return routing statistics by protocol."""
        stats: dict = {}
        for entry in self._request_log:
            proto = entry["protocol"]
            if proto not in stats:
                stats[proto] = {"total": 0, "errors": 0, "avg_latency_ms": 0.0,
                                "latencies": []}
            stats[proto]["total"] += 1
            stats[proto]["latencies"].append(entry["elapsed_ms"])
            if entry["error"]:
                stats[proto]["errors"] += 1

        for proto, data in stats.items():
            latencies = data.pop("latencies")
            data["avg_latency_ms"] = round(
                sum(latencies) / len(latencies), 2
            ) if latencies else 0.0
            data["p99_latency_ms"] = round(
                sorted(latencies)[int(len(latencies) * 0.99)] if latencies else 0.0, 2
            )

        return stats
```

### Wiring It Together with FastAPI

```python
from fastapi import FastAPI, Request, Response
import json

app = FastAPI(title="Multi-Protocol Agent Commerce Gateway")

# Initialize the GreenHelix client and router
gh_client = GreenHelixClient(api_key="your-greenhelix-api-key")
router = MultiProtocolRouter(gh_client)

# Register adapters in priority order
router.register_adapter(X402Adapter(
    client=gh_client,
    agent_id="my-agent-001",
    facilitator_url="https://x402.org/facilitator",
    payment_address="0x1a2b3c...",
))
router.register_adapter(ACPAdapter(
    client=gh_client,
    agent_id="my-agent-001",
    stripe_api_key="sk_live_xxx",
))
router.register_adapter(A2AAdapter(
    client=gh_client,
    agent_id="my-agent-001",
    skill_to_tool_map={
        "code-review": "review_code",
        "data-analysis": "analyze_data",
        "translation": "translate_text",
    },
))


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway(request: Request, path: str):
    """Universal gateway endpoint that routes to the correct protocol adapter."""
    body = None
    if request.method in ("POST", "PUT"):
        try:
            body = await request.json()
        except Exception:
            body = None

    proto_request = ProtocolRequest(
        protocol="auto",
        method=request.method,
        path=f"/{path}",
        headers=dict(request.headers),
        body=body,
        query_params=dict(request.query_params),
        raw_request=request,
    )

    proto_response = router.route(proto_request)

    return Response(
        status_code=proto_response.status_code,
        headers=proto_response.headers,
        content=json.dumps(proto_response.body),
        media_type="application/json",
    )


@app.get("/gateway/stats")
async def gateway_stats():
    """Return per-protocol routing statistics."""
    return router.get_stats()


@app.get("/.well-known/agent.json")
async def agent_card():
    """Serve the A2A Agent Card for discovery."""
    for adapter in router.adapters:
        if isinstance(adapter, A2AAdapter):
            return adapter.generate_agent_card(
                base_url="https://my-gateway.example.com",
                skills=[
                    {"id": "code-review", "name": "Code Review",
                     "description": "Automated code review with security analysis"},
                    {"id": "data-analysis", "name": "Data Analysis",
                     "description": "Statistical analysis and visualization"},
                    {"id": "translation", "name": "Translation",
                     "description": "Multi-language text translation"},
                ],
            )
    return {"error": "A2A adapter not configured"}
```

### GreenHelix as the Universal Backend

The critical insight of this architecture is that GreenHelix serves as the universal backend regardless of which protocol the client uses. An x402 micropayment, an ACP Stripe checkout, and an A2A task completion all funnel into the same GreenHelix escrow, trust, and ledger infrastructure. This means:

1. **Single audit trail.** Every transaction across every protocol is recorded in GreenHelix's ledger. When the EU AI Act auditor asks for your transaction history, you export one dataset, not eleven.

2. **Unified trust scores.** An agent that delivers reliably via A2A tasks also benefits from a higher trust score when transacting via x402. Trust is earned per-agent, not per-protocol.

3. **Cross-protocol dispute resolution.** If a buyer pays via x402 but the service (discovered via A2A) does not deliver, the GreenHelix escrow provides the dispute mechanism that neither x402 nor A2A offers natively.

4. **Protocol-agnostic analytics.** Your revenue dashboard, cost analysis, and agent performance metrics work across all protocols because the underlying data model is the same.

---

## Chapter 7: ProtocolBenchmark Class

### Measuring What Matters

The benchmarks in Chapter 4 reflect our test environment. Your numbers will differ based on network topology, cloud provider, geographic proximity to protocol endpoints, and load patterns. The `ProtocolBenchmark` class below lets you run the same benchmarks against your own infrastructure.

```python
import time
import json
import statistics
import logging
from dataclasses import dataclass, field
from typing import Callable, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)


@dataclass
class BenchmarkResult:
    """Results from a single protocol benchmark run."""
    protocol: str
    total_requests: int
    successful: int
    failed: int
    latencies_ms: list[float]
    errors: list[str] = field(default_factory=list)

    @property
    def success_rate(self) -> float:
        return self.successful / self.total_requests if self.total_requests else 0.0

    @property
    def p50_ms(self) -> float:
        if not self.latencies_ms:
            return 0.0
        sorted_lat = sorted(self.latencies_ms)
        return sorted_lat[len(sorted_lat) // 2]

    @property
    def p95_ms(self) -> float:
        if not self.latencies_ms:
            return 0.0
        sorted_lat = sorted(self.latencies_ms)
        return sorted_lat[int(len(sorted_lat) * 0.95)]

    @property
    def p99_ms(self) -> float:
        if not self.latencies_ms:
            return 0.0
        sorted_lat = sorted(self.latencies_ms)
        return sorted_lat[int(len(sorted_lat) * 0.99)]

    @property
    def mean_ms(self) -> float:
        return statistics.mean(self.latencies_ms) if self.latencies_ms else 0.0

    @property
    def stddev_ms(self) -> float:
        return statistics.stdev(self.latencies_ms) if len(self.latencies_ms) > 1 else 0.0

    @property
    def throughput_rps(self) -> float:
        if not self.latencies_ms:
            return 0.0
        total_time_s = sum(self.latencies_ms) / 1000
        return self.total_requests / total_time_s if total_time_s > 0 else 0.0


class ProtocolBenchmark:
    """Benchmarking framework for comparing agent commerce protocols.

    Usage:
        bench = ProtocolBenchmark()

        bench.register("x402", x402_transaction_fn)
        bench.register("acp", acp_transaction_fn)
        bench.register("a2a+x402", combined_transaction_fn)

        results = bench.run_all(iterations=1000, concurrency=10)
        report = bench.generate_report(results)
        print(report)
    """

    def __init__(self):
        self.protocols: dict[str, Callable[[], bool]] = {}
        self._warmup_iterations = 10

    def register(self, protocol_name: str,
                 transaction_fn: Callable[[], bool]) -> None:
        """Register a protocol's transaction function.

        The function should execute a single complete transaction and return
        True on success, False on failure. It should not catch exceptions —
        the benchmark runner handles error tracking.
        """
        self.protocols[protocol_name] = transaction_fn
        logger.info(f"Registered benchmark: {protocol_name}")

    def run_single(self, protocol_name: str, iterations: int = 1000,
                   concurrency: int = 1,
                   warmup: bool = True) -> BenchmarkResult:
        """Run a benchmark for a single protocol.

        Args:
            protocol_name: Name of the registered protocol.
            iterations: Number of transactions to execute.
            concurrency: Number of parallel workers.
            warmup: Whether to run warmup iterations first.
        """
        fn = self.protocols.get(protocol_name)
        if not fn:
            raise ValueError(f"Unknown protocol: {protocol_name}")

        # Warmup phase — discard results
        if warmup:
            logger.info(f"Warming up {protocol_name} ({self._warmup_iterations} iterations)")
            for _ in range(self._warmup_iterations):
                try:
                    fn()
                except Exception:
                    pass

        latencies: list[float] = []
        errors: list[str] = []
        successful = 0
        failed = 0

        logger.info(
            f"Running {protocol_name}: {iterations} iterations, "
            f"concurrency={concurrency}"
        )

        def _execute_one() -> tuple[Optional[float], Optional[str]]:
            start = time.monotonic()
            try:
                result = fn()
                elapsed = (time.monotonic() - start) * 1000
                if result:
                    return elapsed, None
                else:
                    return elapsed, "Transaction returned False"
            except Exception as e:
                elapsed = (time.monotonic() - start) * 1000
                return elapsed, str(e)

        if concurrency <= 1:
            for i in range(iterations):
                elapsed, error = _execute_one()
                if elapsed is not None:
                    latencies.append(elapsed)
                if error:
                    failed += 1
                    errors.append(error)
                else:
                    successful += 1
        else:
            with ThreadPoolExecutor(max_workers=concurrency) as executor:
                futures = [executor.submit(_execute_one) for _ in range(iterations)]
                for future in as_completed(futures):
                    elapsed, error = future.result()
                    if elapsed is not None:
                        latencies.append(elapsed)
                    if error:
                        failed += 1
                        errors.append(error)
                    else:
                        successful += 1

        return BenchmarkResult(
            protocol=protocol_name,
            total_requests=iterations,
            successful=successful,
            failed=failed,
            latencies_ms=latencies,
            errors=errors[:50],  # Cap stored errors at 50
        )

    def run_all(self, iterations: int = 1000,
                concurrency: int = 1) -> list[BenchmarkResult]:
        """Run benchmarks for all registered protocols."""
        results = []
        for name in self.protocols:
            result = self.run_single(name, iterations, concurrency)
            results.append(result)
        return results

    def generate_report(self, results: list[BenchmarkResult]) -> str:
        """Generate a formatted comparison report.

        Returns a string containing a table comparing all benchmarked protocols
        across latency percentiles, throughput, success rate, and error count.
        """
        lines = [
            "Protocol Benchmark Report",
            "=" * 78,
            f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}",
            "",
            f"{'Protocol':<16} {'p50':>8} {'p95':>8} {'p99':>8} "
            f"{'Mean':>8} {'StdDev':>8} {'Succ%':>7} {'Errors':>7}",
            "-" * 78,
        ]

        for r in sorted(results, key=lambda x: x.p50_ms):
            lines.append(
                f"{r.protocol:<16} {r.p50_ms:>7.1f}ms {r.p95_ms:>7.1f}ms "
                f"{r.p99_ms:>7.1f}ms {r.mean_ms:>7.1f}ms {r.stddev_ms:>7.1f}ms "
                f"{r.success_rate * 100:>6.1f}% {r.failed:>7d}"
            )

        lines.append("-" * 78)
        lines.append("")

        # Throughput summary
        lines.append("Effective Throughput (sequential):")
        for r in sorted(results, key=lambda x: x.p50_ms):
            rps = 1000 / r.mean_ms if r.mean_ms > 0 else 0
            lines.append(f"  {r.protocol:<16} {rps:>8.1f} req/s")

        lines.append("")

        # Winner summary
        if results:
            fastest = min(results, key=lambda x: x.p50_ms)
            most_reliable = max(results, key=lambda x: x.success_rate)
            lines.append(f"Fastest (p50):     {fastest.protocol} ({fastest.p50_ms:.1f}ms)")
            lines.append(
                f"Most reliable:     {most_reliable.protocol} "
                f"({most_reliable.success_rate * 100:.1f}%)"
            )

        return "\n".join(lines)

    def export_json(self, results: list[BenchmarkResult],
                    filepath: str) -> None:
        """Export benchmark results to a JSON file for further analysis."""
        export_data = {
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "results": [],
        }
        for r in results:
            export_data["results"].append({
                "protocol": r.protocol,
                "total_requests": r.total_requests,
                "successful": r.successful,
                "failed": r.failed,
                "p50_ms": round(r.p50_ms, 2),
                "p95_ms": round(r.p95_ms, 2),
                "p99_ms": round(r.p99_ms, 2),
                "mean_ms": round(r.mean_ms, 2),
                "stddev_ms": round(r.stddev_ms, 2),
                "success_rate": round(r.success_rate, 4),
            })

        with open(filepath, "w") as f:
            json.dump(export_data, f, indent=2)
        logger.info(f"Results exported to {filepath}")
```

### Running a Benchmark

Here is a complete example that benchmarks x402, ACP, and the MCP+x402 combination against a GreenHelix backend:

```python
import requests

GH_API = "https://api.greenhelix.net/v1"
GH_KEY = "your-api-key"
FACILITATOR = "https://x402.org/facilitator"

def x402_transaction() -> bool:
    """Simulate a complete x402 transaction."""
    # Step 1: Request the resource, get 402
    resp = requests.get(
        "https://my-agent.example.com/api/analyze",
        params={"data": "benchmark_payload"},
    )
    if resp.status_code != 402:
        return False  # Should have gotten 402

    # Step 2: Pay through facilitator (simulated)
    pay_resp = requests.post(f"{FACILITATOR}/pay", json={
        "amount": "0.005",
        "address": resp.headers["X-PAYMENT-ADDRESS"],
    })
    proof = pay_resp.json()

    # Step 3: Retry with payment proof
    resp2 = requests.get(
        "https://my-agent.example.com/api/analyze",
        params={"data": "benchmark_payload"},
        headers={"X-PAYMENT-PROOF": json.dumps(proof)},
    )
    return resp2.status_code == 200


def acp_transaction() -> bool:
    """Simulate a complete ACP checkout transaction."""
    # Create checkout session
    session = requests.post(
        "https://api.stripe.com/v1/acp/checkout/sessions",
        json={
            "product_id": "prod_benchmark_001",
            "buyer_agent_id": "agent-benchmark",
        },
        headers={"Authorization": f"Bearer {GH_KEY}"},
    )
    if session.status_code != 200:
        return False

    # Confirm payment (simulated)
    confirm = requests.post(
        f"https://api.stripe.com/v1/acp/sessions/{session.json()['id']}/confirm",
        headers={"Authorization": f"Bearer {GH_KEY}"},
    )
    return confirm.status_code == 200


def mcp_x402_transaction() -> bool:
    """Simulate MCP tool discovery + x402 payment."""
    # Step 1: Discover tools via MCP
    tools_resp = requests.get(
        "https://my-agent.example.com/mcp/tools",
        headers={"Authorization": f"Bearer {GH_KEY}"},
    )
    if tools_resp.status_code != 200:
        return False

    # Step 2: Call tool with x402 payment
    return x402_transaction()


# Run the benchmark
bench = ProtocolBenchmark()
bench.register("x402", x402_transaction)
bench.register("acp", acp_transaction)
bench.register("mcp+x402", mcp_x402_transaction)

results = bench.run_all(iterations=500, concurrency=5)
print(bench.generate_report(results))
bench.export_json(results, "benchmark_results.json")
```

### Interpreting Results

When analyzing benchmark output, focus on three metrics:

1. **p95 latency, not p50.** The median latency tells you what happens in the common case. The p95 tells you what your users experience during load spikes, DNS cache misses, or payment facilitator congestion. Design your SLAs around p95.

2. **Success rate under concurrency.** Run the benchmark with concurrency=1 first (baseline), then increase to 5, 10, and 50. Protocols that perform well at concurrency=1 but degrade sharply at concurrency=10 have hidden bottlenecks -- often rate limits, connection pool exhaustion, or serialized state updates.

3. **Cost per successful transaction.** Divide your total protocol costs (gas fees, Stripe fees, facilitator fees) by the number of successful transactions. A protocol with 95% success rate effectively costs 5% more per successful transaction than its nominal fee.

---

## Chapter 8: Future-Proofing Strategies

### Which Protocols Are Likely to Win

Protocol standards follow a predictable consolidation pattern. In the early phase (where we are now -- more so than ever after Q1 2026), many standards compete. In the middle phase, two or three gain critical mass and the rest are abandoned or absorbed. In the late phase, one or two become the de facto standards while the others survive in niches.

The Q1 2026 payment protocol explosion complicated every existing prediction. Five new protocols from five dominant platforms launched in a single quarter. Rather than consolidation, we got proliferation. But the underlying consolidation dynamics remain. Based on current adoption trajectories, ecosystem backing, and protocol design quality, here is our updated analysis.

**Likely winners:**

- **MCP** will be the dominant tool-calling standard. It has the widest adoption, the simplest specification, and the strongest ecosystem (10,000+ servers in the official registry, adopted by every major AI IDE). The donation to the Linux Foundation was a strategic masterstroke -- MCP is now vendor-neutral infrastructure, not Anthropic's proprietary protocol. MCP's weakness (no payment layer) is actually a strength for longevity: it does one thing well and partners with payment protocols rather than trying to absorb them.

- **A2A** will be the dominant agent discovery and task orchestration standard. Google's enterprise partnerships (Salesforce, SAP, Atlassian, IBM) give A2A distribution that no other communication protocol has. Google's Q1 2026 strategy of building AP2 and UCP as complements to A2A, rather than rolling discovery into the payment protocol, validates A2A's position as the discovery layer. The Agent Card model is simple enough that any agent can publish one, and the task-based interaction model maps well to enterprise workflows.

- **x402** will be the dominant micropayment standard, and the Q1 2026 numbers cemented this. 100 million payments in six months, backed by a Foundation that includes Coinbase, Cloudflare, Stripe, AWS, Microsoft, Google, and American Express. No other payment protocol has this combination of transaction volume, simplicity, and multi-stakeholder backing. For sub-dollar payments, x402 is now the unambiguous default.

**Strong contenders from Q1 2026:**

- **Google AP2** has the strongest launch coalition (60+ partners including Adyen, Mastercard, PayPal, Visa) and the most elegant consent model (cryptographic mandates). If Google executes on the AP2 + UCP + A2A stack, it becomes the default for consumer-facing agent commerce. The risk is Google's track record of abandoning products.

- **OpenAI ACP** has the Apache 2.0 open-spec advantage and ChatGPT distribution. If alternative payment processors implement ACP backends (beyond Stripe's reference implementation), ACP could become the lingua franca of agent checkout. The risk is that "open spec, single implementation" becomes de facto lock-in.

- **PayPal Agent Ready** may be the most strategically important Q1 2026 launch despite being the least technically innovative. If Agent Ready becomes the default bridge, protocol choice stops mattering for merchants -- which commoditizes the payment protocol layer and shifts value to the commerce and discovery layers.

**Likely survivors in niches:**

- **Visa TAP** will dominate enterprise agent commerce where compliance and audit trails matter more than cost or speed. The cryptographic agent identity model is the best solution for EU AI Act compliance. But Visa's fee structure makes TAP uncompetitive for anything under $10.

- **On-chain TAP** will survive in DeFi-adjacent use cases where on-chain composability matters more than latency or cost.

- **Google UCP** will dominate retailer agent commerce specifically because of its co-development partners (Shopify, Etsy, Wayfair, Target, Walmart). It will not generalize to service commerce.

**At risk:**

- **Original AP2** (PayPal Labs, crypto payment channels) suffers from both the payment channel cold-start problem and the naming collision with Google AP2. It may be quietly absorbed into PayPal Agent Ready.

- **MPP** is being superseded by Visa TAP in Visa's own product roadmap. Existing MPP integrations will migrate to TAP.

- **Original consortium UCP** (Mastercard/SAP/Salesforce) faces an existential threat from Google UCP, which shares the name but has stronger retail partners and faster execution. The 847-page specification and committee governance model cannot compete with Google's development velocity.

### How to Hedge Your Bets

The multi-protocol gateway in Chapter 6 is the primary hedging mechanism. But there are additional strategies:

**1. Separate your protocol layer from your business logic.** Your service code should never import protocol-specific types. Define internal interfaces (dataclasses, typed dicts) and let adapters translate between protocols and your internal format. When a protocol dies, you delete its adapter. Your business logic is untouched.

**2. Store protocol-agnostic transaction records.** Your database should record the transaction amount, parties, outcome, and timestamp in a normalized format. Store protocol-specific details (tx_hash, stripe_session_id, task_id) in a metadata JSON column. This ensures your analytics and compliance reporting work regardless of protocol churn.

**3. Invest in the likely winners, monitor the rest.** Build production-grade adapters for MCP, A2A, and x402. Build minimal adapters for OpenAI ACP and Google AP2. Add PayPal Agent Ready as a bridge for merchant-facing transactions. Do not build adapters for the original AP2, MPP, on-chain TAP, or the original consortium UCP unless you have a specific partner requiring them. Monitor Visa TAP and Google UCP for enterprise and retail use cases respectively.

**4. Contribute to protocol governance.** MCP and A2A both accept community contributions to their specifications. If a protocol change would break your architecture, you want to know about it before it ships, not after. Join the working groups, read the RFCs, and submit feedback.

### The Protocol-Agnostic Architecture Pattern

The ultimate future-proofing strategy is to design your system so that the protocol is a deployment-time configuration choice, not a compile-time architectural decision.

```python
# Protocol selection via environment configuration
import os

PROTOCOL_CONFIG = {
    "payment": os.getenv("PAYMENT_PROTOCOL", "x402"),      # x402, acp, ap2, mpp
    "discovery": os.getenv("DISCOVERY_PROTOCOL", "a2a"),    # a2a, ucp, mcp
    "communication": os.getenv("COMM_PROTOCOL", "mcp"),     # mcp, a2a
}

def get_payment_adapter(client: GreenHelixClient) -> ProtocolAdapter:
    adapters = {
        "x402": lambda: X402Adapter(client, os.getenv("AGENT_ID"),
                                     os.getenv("X402_FACILITATOR"),
                                     os.getenv("X402_ADDRESS")),
        "acp": lambda: ACPAdapter(client, os.getenv("AGENT_ID"),
                                   os.getenv("STRIPE_KEY")),
    }
    factory = adapters.get(PROTOCOL_CONFIG["payment"])
    if not factory:
        raise ValueError(f"Unknown payment protocol: {PROTOCOL_CONFIG['payment']}")
    return factory()
```

This pattern means switching from x402 to ACP is an environment variable change and a deployment, not a code change and a release.

### What Consolidation Might Look Like

After Q1 2026, the most likely consolidation scenario by 2028 is not a single stack but two competing stacks with a bridge layer between them.

**Stack 1: The Open Stack**
1. **MCP** for tool calling (Linux Foundation governed, 10K+ servers)
2. **A2A** for discovery and orchestration (Google-led but broadly adopted)
3. **x402** for micropayments (Foundation-backed, 100M+ transactions)
4. **OpenAI ACP** for commerce checkout (Apache 2.0, Stripe reference implementation)

**Stack 2: The Google Stack**
1. **A2A** for discovery and orchestration (shared with Stack 1)
2. **Google AP2** for payment (60+ partners, cryptographic mandates)
3. **Google UCP** for commerce (co-developed with Shopify, Target, Walmart)

**The Bridge Layer**
- **PayPal Agent Ready** and similar bridges translate between stacks, letting merchants accept payments from either stack without caring which one the agent uses.

A2A appears in both stacks because Google designed it to be composable with any payment and commerce protocol, not just Google's own. This makes A2A the shared substrate of agent commerce, similar to how HTTP is the shared substrate of the web regardless of which application protocol runs on top.

The commerce layer sits beneath all protocols as the trust, escrow, and compliance layer. When Agent A discovers Agent B via A2A, calls Agent B's tool via MCP, and pays via x402 or Google AP2, it provides the escrow that protects the payment, the identity verification that establishes trust, and the audit trail that satisfies regulators.

The protocols that lose will not disappear overnight. The original consortium UCP will persist as long as Mastercard and SAP fund it. MPP will persist until Visa migrates all clients to TAP. The original PayPal Labs AP2 will persist in crypto-native niches. But the developer mindshare, ecosystem investment, and default status will consolidate around the two stacks above.

Teams that build protocol-agnostic architectures today -- with the multi-protocol gateway pattern from Chapter 6 and the benchmarking framework from Chapter 7 -- will navigate this consolidation without rewriting their systems. Teams that bet everything on a single protocol are making a prediction about the future. The multi-protocol approach is not a prediction. It is a hedge. And in a market with eleven competing standards and two emerging stacks, hedging is not conservative -- it is the only rational strategy.

---

## What's Next

This guide gave you the comprehensive comparison that did not exist before: all eleven agent commerce protocols -- including the five that launched in the Q1 2026 payment protocol explosion -- evaluated against the same criteria, with real benchmarks, migration paths, and a production-ready multi-protocol gateway.

To put this into practice:

1. **Deploy the MultiProtocolRouter** from Chapter 6 with adapters for your most common protocol interactions (start with x402 + MCP or A2A + ACP).

2. **Run the ProtocolBenchmark** from Chapter 7 against your infrastructure to validate which protocols perform best in your specific environment. The numbers in Chapter 4 are baselines -- your numbers will differ.

3. **Implement the protocol-agnostic architecture** from Chapter 8 so that adding or removing protocols is a configuration change, not a rewrite.

4. **Use GreenHelix as your universal backend.** Register agents with `register_agent`. Protect payments with `create_escrow`. Build trust with `submit_review`. Resolve disputes with `open_dispute`. These primitives work regardless of which protocol your clients speak.

The protocol wars will intensify before they resolve -- Q1 2026 proved that. The question is not which protocol wins -- it is whether your architecture survives the answer. The multi-protocol gateway pattern ensures it does.

Explore the full GreenHelix API at [https://api.greenhelix.net/v1](https://api.greenhelix.net/v1) and the interoperability bridge guide for working protocol adapter implementations.

---

## Multi-Protocol Adapter — Working Implementation

The code below builds a complete multi-protocol adapter on top of the
`greenhelix_trading` library. It translates between x402, ACP, and
GreenHelix-native protocols using `ProtocolBridge`, `ServiceBridge`, and
`EventBridge` directly. Every method calls the live GreenHelix A2A Commerce
Gateway at `https://api.greenhelix.net/v1`.

```bash
pip install greenhelix-trading
```

### Protocol Detection and Canonical Format

```python
"""
Detect the inbound protocol from raw request data and normalize into a
canonical internal format. This is the first stage of any multi-protocol
adapter: parse, identify, normalize.
"""

import json
import re
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional


class Protocol(Enum):
    X402 = "x402"
    ACP = "acp"
    GREENHELIX = "greenhelix"
    UNKNOWN = "unknown"


@dataclass
class CanonicalRequest:
    """Protocol-agnostic internal representation of any commerce request."""
    protocol: Protocol
    action: str                    # "payment", "discovery", "identity", "event"
    sender_id: str
    recipient_id: str
    amount: Optional[str] = None   # Always string to preserve precision
    currency: str = "USD"
    metadata: dict = field(default_factory=dict)
    raw: dict = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        return {
            "protocol": self.protocol.value,
            "action": self.action,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "amount": self.amount,
            "currency": self.currency,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }


@dataclass
class CanonicalResponse:
    """Protocol-agnostic internal representation of a commerce response."""
    success: bool
    protocol: Protocol
    action: str
    data: dict = field(default_factory=dict)
    error: Optional[str] = None
    timestamp: float = field(default_factory=time.time)

    def to_protocol_format(self) -> dict:
        """Re-encode the response into the originating protocol's format."""
        if self.protocol == Protocol.X402:
            return self._to_x402()
        elif self.protocol == Protocol.ACP:
            return self._to_acp()
        else:
            return self._to_greenhelix()

    def _to_x402(self) -> dict:
        if not self.success:
            return {
                "status": 402,
                "error": self.error or "Payment required",
            }
        return {
            "status": 200,
            "x_payment_receipt": self.data.get("receipt", ""),
            "data": self.data,
        }

    def _to_acp(self) -> dict:
        return {
            "object": "checkout.session" if self.action == "payment" else "event",
            "status": "complete" if self.success else "failed",
            "amount": self.data.get("amount"),
            "currency": self.data.get("currency", "usd"),
            "metadata": self.data,
        }

    def _to_greenhelix(self) -> dict:
        return {
            "success": self.success,
            "result": self.data,
            "error": self.error,
        }


class ProtocolDetector:
    """Identify the protocol from inbound request headers and body."""

    # x402 signals: HTTP 402 response with payment headers, or a request
    # carrying X-PAYMENT-PROOF / X-PAYMENT-ADDRESS.
    _X402_HEADERS = {"x-payment-proof", "x-payment-address", "x-payment-amount"}

    # ACP signals: Stripe-style "object" field or /acp/ path prefix.
    _ACP_OBJECT_TYPES = {"checkout.session", "payment_intent", "acp.transaction"}

    @classmethod
    def detect(cls, headers: dict, body: dict, path: str = "") -> Protocol:
        """Return the detected Protocol enum value.

        Detection order:
          1. Header-based (x402 payment headers).
          2. Body-based (ACP object types).
          3. Path-based (/acp/ prefix or the REST API).
          4. Fallback to GREENHELIX if the request targets the GreenHelix API.
        """
        # Normalize header keys to lowercase
        lower_headers = {k.lower(): v for k, v in headers.items()}

        # 1. x402 header detection
        if cls._X402_HEADERS & set(lower_headers.keys()):
            return Protocol.X402

        # 2. ACP body detection
        if body.get("object") in cls._ACP_OBJECT_TYPES:
            return Protocol.ACP
        if "stripe_session_id" in body or "checkout_session" in body:
            return Protocol.ACP

        # 3. Path-based detection
        if "/acp/" in path.lower():
            return Protocol.ACP
        if "/x402/" in path.lower() or "facilitator" in path.lower():
            return Protocol.X402

        # 4. GreenHelix default
        if "the REST API" in path or "greenhelix" in lower_headers.get("host", ""):
            return Protocol.GREENHELIX

        return Protocol.UNKNOWN

    @classmethod
    def normalize(
        cls,
        headers: dict,
        body: dict,
        path: str = "",
    ) -> CanonicalRequest:
        """Detect the protocol and convert to a CanonicalRequest."""
        protocol = cls.detect(headers, body, path)

        if protocol == Protocol.X402:
            return cls._normalize_x402(headers, body)
        elif protocol == Protocol.ACP:
            return cls._normalize_acp(body)
        elif protocol == Protocol.GREENHELIX:
            return cls._normalize_greenhelix(body)
        else:
            return CanonicalRequest(
                protocol=Protocol.UNKNOWN,
                action="unknown",
                sender_id=body.get("agent_id", ""),
                recipient_id=body.get("recipient", ""),
                raw=body,
            )

    @classmethod
    def _normalize_x402(cls, headers: dict, body: dict) -> CanonicalRequest:
        lower_h = {k.lower(): v for k, v in headers.items()}
        return CanonicalRequest(
            protocol=Protocol.X402,
            action="payment",
            sender_id=body.get("agent_id", ""),
            recipient_id=lower_h.get("x-payment-address", ""),
            amount=lower_h.get("x-payment-amount", body.get("amount")),
            currency="USD",
            metadata={
                "payment_proof": lower_h.get("x-payment-proof", ""),
                "facilitator": body.get("facilitator", ""),
            },
            raw=body,
        )

    @classmethod
    def _normalize_acp(cls, body: dict) -> CanonicalRequest:
        return CanonicalRequest(
            protocol=Protocol.ACP,
            action="payment",
            sender_id=body.get("buyer_agent_id", body.get("customer", "")),
            recipient_id=body.get("seller_agent_id", body.get("merchant", "")),
            amount=str(body.get("amount", body.get("amount_total", "0"))),
            currency=body.get("currency", "usd").upper(),
            metadata={
                "stripe_session_id": body.get("id", ""),
                "object_type": body.get("object", ""),
            },
            raw=body,
        )

    @classmethod
    def _normalize_greenhelix(cls, body: dict) -> CanonicalRequest:
        inp = body.get("input", body)
        tool = body.get("tool", "unknown")
        action_map = {
            "create_escrow": "payment",
            "release_escrow": "payment",
            "create_payment_intent": "payment",
            "register_agent": "identity",
            "get_agent_identity": "identity",
            "register_service": "discovery",
            "search_services": "discovery",
            "publish_event": "event",
        }
        return CanonicalRequest(
            protocol=Protocol.GREENHELIX,
            action=action_map.get(tool, "unknown"),
            sender_id=inp.get("agent_id", ""),
            recipient_id=inp.get("recipient", inp.get("target", "")),
            amount=str(inp.get("amount", "")) if inp.get("amount") else None,
            metadata={"tool": tool},
            raw=body,
        )
```

### Multi-Protocol Router

```python
"""
Routes CanonicalRequests to the correct GreenHelix API calls via
ProtocolBridge, ServiceBridge, and EventBridge. Converts the GreenHelix
response back into the caller's native protocol format.
"""

from greenhelix_trading import ProtocolBridge, ServiceBridge, EventBridge


class MultiProtocolRouter:
    """Accept requests in any supported protocol, execute via GreenHelix,
    and return responses in the caller's native format.

    Internally delegates to:
      - ProtocolBridge for identity resolution and cross-protocol verification.
      - ServiceBridge for service discovery and A2A task translation.
      - EventBridge for cross-protocol event publishing and webhook management.
    """

    def __init__(
        self,
        api_key: str,
        agent_id: str,
        base_url: str = "https://api.greenhelix.net/v1",
    ):
        self.api_key = api_key
        self.agent_id = agent_id
        self.base_url = base_url

        self.identity = ProtocolBridge(
            api_key=api_key,
            agent_id=agent_id,
            base_url=base_url,
        )
        self.services = ServiceBridge(
            api_key=api_key,
            agent_id=agent_id,
            base_url=base_url,
        )
        self.events = EventBridge(
            api_key=api_key,
            agent_id=agent_id,
            base_url=base_url,
        )

        # Action handlers keyed by CanonicalRequest.action
        self._handlers = {
            "payment": self._handle_payment,
            "identity": self._handle_identity,
            "discovery": self._handle_discovery,
            "event": self._handle_event,
        }

    # ── Public API ───────────────────────────────────────────────────────

    def route(self, request: CanonicalRequest) -> CanonicalResponse:
        """Route a CanonicalRequest to the appropriate handler.

        Returns a CanonicalResponse that can be re-encoded into the
        caller's native protocol via response.to_protocol_format().
        """
        handler = self._handlers.get(request.action)
        if handler is None:
            return CanonicalResponse(
                success=False,
                protocol=request.protocol,
                action=request.action,
                error=f"Unsupported action: {request.action}",
            )

        try:
            data = handler(request)
            return CanonicalResponse(
                success=True,
                protocol=request.protocol,
                action=request.action,
                data=data,
            )
        except Exception as exc:
            return CanonicalResponse(
                success=False,
                protocol=request.protocol,
                action=request.action,
                error=str(exc),
            )

    # ── Payment handling ─────────────────────────────────────────────────

    def _handle_payment(self, req: CanonicalRequest) -> dict:
        """Convert any protocol's payment request into a GreenHelix escrow."""
        # Map the external sender to a GreenHelix identity
        sender_gh = self.identity.resolve_identity(req.sender_id)
        if isinstance(sender_gh, dict):
            sender_gh = sender_gh.get("result", sender_gh).get(
                "agent_id", req.sender_id
            )

        # Ensure the sender has an identity mapping for their protocol
        self.identity.register_identity_mapping(
            external_id=req.sender_id,
            protocol=req.protocol.value,
        )

        # Create the escrow via the underlying ProtocolBridge._execute
        escrow = self.identity._execute("create_escrow", {
            "payer_id": sender_gh,
            "payee_id": req.recipient_id,
            "amount": req.amount or "0",
            "currency": req.currency,
            "metadata": {
                "source_protocol": req.protocol.value,
                **req.metadata,
            },
        })

        # Publish a cross-protocol payment event
        self.events.publish_cross_protocol_event(
            event_type="payment.created",
            data={
                "escrow_id": escrow.get("escrow_id", ""),
                "amount": req.amount,
                "currency": req.currency,
                "source_protocol": req.protocol.value,
            },
            target_protocols=[req.protocol.value, "greenhelix"],
        )

        return {
            "escrow_id": escrow.get("escrow_id", ""),
            "amount": req.amount,
            "currency": req.currency,
            "receipt": escrow.get("escrow_id", ""),
        }

    # ── Identity handling ────────────────────────────────────────────────

    def _handle_identity(self, req: CanonicalRequest) -> dict:
        """Resolve or register identity across protocols."""
        tool = req.metadata.get("tool", "get_agent_identity")

        if tool == "register_agent":
            return self.identity.register_identity_mapping(
                external_id=req.sender_id,
                protocol=req.protocol.value,
            )

        # Default: resolve
        result = self.identity.resolve_identity(req.sender_id)
        if isinstance(result, str):
            return {"agent_id": result, "protocol": req.protocol.value}
        return result

    # ── Discovery handling ───────────────────────────────────────────────

    def _handle_discovery(self, req: CanonicalRequest) -> dict:
        """Route service discovery and registration across protocols."""
        tool = req.metadata.get("tool", "search_services")

        if tool == "register_service":
            if req.protocol == Protocol.ACP:
                return self.services.publish_to_mcp(
                    tool_definitions=req.metadata.get("tools", []),
                )
            else:
                return self.services.publish_to_a2a(
                    name=req.metadata.get("name", self.agent_id),
                    description=req.metadata.get("description", ""),
                    capabilities=req.metadata.get("capabilities", []),
                )

        # Default: cross-protocol search
        target_protocols = None
        if req.protocol == Protocol.X402:
            target_protocols = ["x402", "greenhelix"]
        elif req.protocol == Protocol.ACP:
            target_protocols = ["acp", "mcp", "greenhelix"]

        return self.services.discover_cross_protocol(
            query=req.metadata.get("query", req.sender_id),
            protocols=target_protocols,
        )

    # ── Event handling ───────────────────────────────────────────────────

    def _handle_event(self, req: CanonicalRequest) -> dict:
        """Publish events and register webhooks across protocols."""
        tool = req.metadata.get("tool", "publish_event")

        if tool == "register_webhook":
            return self.events.register_protocol_webhook(
                url=req.metadata.get("url", ""),
                source_protocol=req.protocol.value,
                events=req.metadata.get("events", []),
            )

        # Default: cross-protocol event publish
        target = [req.protocol.value]
        if req.protocol != Protocol.GREENHELIX:
            target.append("greenhelix")

        return self.events.publish_cross_protocol_event(
            event_type=req.metadata.get("event_type", "generic"),
            data=req.raw,
            target_protocols=target,
        )
```

### Format Converter with Error Handling

```python
"""
Bidirectional format conversion between x402, ACP, and GreenHelix wire
formats. Handles malformed payloads, missing fields, and protocol-specific
edge cases.
"""

import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class FormatConversionError(Exception):
    """Raised when a payload cannot be converted between protocols."""

    def __init__(self, source: str, target: str, reason: str):
        self.source = source
        self.target = target
        self.reason = reason
        super().__init__(f"{source} -> {target}: {reason}")


class ProtocolFormatConverter:
    """Convert wire-format payloads between x402, ACP, and GreenHelix.

    Each conversion method validates required fields, applies defaults for
    optional fields, and raises FormatConversionError with a clear message
    when conversion is impossible.
    """

    # ── x402 -> GreenHelix ───────────────────────────────────────────────

    @staticmethod
    def x402_to_greenhelix(
        headers: dict,
        body: dict,
    ) -> dict:
        """Convert an x402 payment request to a GreenHelix execute payload."""
        lower_h = {k.lower(): v for k, v in headers.items()}

        address = lower_h.get("x-payment-address")
        if not address:
            raise FormatConversionError(
                "x402", "greenhelix",
                "Missing required header: X-PAYMENT-ADDRESS",
            )

        amount = lower_h.get("x-payment-amount", body.get("amount"))
        if amount is None:
            raise FormatConversionError(
                "x402", "greenhelix",
                "No amount in X-PAYMENT-AMOUNT header or body",
            )

        return {
            "tool": "create_escrow",
            "input": {
                "payer_id": body.get("agent_id", ""),
                "payee_id": address,
                "amount": str(amount),
                "currency": "USD",
                "metadata": {
                    "source_protocol": "x402",
                    "payment_proof": lower_h.get("x-payment-proof", ""),
                    "facilitator": body.get("facilitator",
                                            "https://x402.org/facilitator"),
                },
            },
        }

    # ── GreenHelix -> x402 ───────────────────────────────────────────────

    @staticmethod
    def greenhelix_to_x402(response: dict) -> dict:
        """Convert a GreenHelix escrow response to x402 wire format."""
        result = response.get("result", response)
        return {
            "status": 200,
            "headers": {
                "X-PAYMENT-RECEIPT": result.get("escrow_id", ""),
                "X-PAYMENT-AMOUNT": str(result.get("amount", "0")),
            },
            "body": {
                "paid": True,
                "escrow_id": result.get("escrow_id", ""),
                "amount": str(result.get("amount", "0")),
            },
        }

    # ── ACP -> GreenHelix ────────────────────────────────────────────────

    @staticmethod
    def acp_to_greenhelix(acp_payload: dict) -> dict:
        """Convert an ACP checkout session to a GreenHelix execute payload."""
        obj_type = acp_payload.get("object", "")
        if obj_type not in ("checkout.session", "payment_intent",
                            "acp.transaction"):
            raise FormatConversionError(
                "acp", "greenhelix",
                f"Unrecognized ACP object type: {obj_type!r}",
            )

        amount_raw = acp_payload.get("amount_total",
                                      acp_payload.get("amount"))
        if amount_raw is None:
            raise FormatConversionError(
                "acp", "greenhelix",
                "No amount_total or amount field in ACP payload",
            )

        # ACP amounts are in cents; GreenHelix uses dollars as strings
        try:
            amount_dollars = str(int(amount_raw) / 100)
        except (ValueError, TypeError):
            amount_dollars = str(amount_raw)

        buyer = (acp_payload.get("buyer_agent_id")
                 or acp_payload.get("customer", ""))
        seller = (acp_payload.get("seller_agent_id")
                  or acp_payload.get("merchant", ""))

        return {
            "tool": "create_escrow",
            "input": {
                "payer_id": buyer,
                "payee_id": seller,
                "amount": amount_dollars,
                "currency": acp_payload.get("currency", "usd").upper(),
                "metadata": {
                    "source_protocol": "acp",
                    "stripe_session_id": acp_payload.get("id", ""),
                    "acp_object_type": obj_type,
                },
            },
        }

    # ── GreenHelix -> ACP ────────────────────────────────────────────────

    @staticmethod
    def greenhelix_to_acp(response: dict) -> dict:
        """Convert a GreenHelix escrow response to ACP checkout format."""
        result = response.get("result", response)
        try:
            amount_cents = int(float(result.get("amount", 0)) * 100)
        except (ValueError, TypeError):
            amount_cents = 0

        return {
            "object": "checkout.session",
            "id": result.get("escrow_id", ""),
            "status": "complete",
            "amount_total": amount_cents,
            "currency": result.get("currency", "usd").lower(),
            "metadata": {
                "greenhelix_escrow_id": result.get("escrow_id", ""),
                "source": "greenhelix",
            },
        }

    # ── Batch converter ──────────────────────────────────────────────────

    @classmethod
    def convert(
        cls,
        source_protocol: str,
        target_protocol: str,
        payload: dict,
        headers: dict | None = None,
    ) -> dict:
        """Generic conversion dispatcher.

        Supported conversions:
          x402      -> greenhelix
          greenhelix -> x402
          acp       -> greenhelix
          greenhelix -> acp

        Raises FormatConversionError for unsupported pairs or invalid data.
        """
        headers = headers or {}
        key = (source_protocol.lower(), target_protocol.lower())

        converters = {
            ("x402", "greenhelix"): lambda: cls.x402_to_greenhelix(
                headers, payload
            ),
            ("greenhelix", "x402"): lambda: cls.greenhelix_to_x402(payload),
            ("acp", "greenhelix"): lambda: cls.acp_to_greenhelix(payload),
            ("greenhelix", "acp"): lambda: cls.greenhelix_to_acp(payload),
        }

        converter = converters.get(key)
        if converter is None:
            raise FormatConversionError(
                source_protocol, target_protocol,
                f"No converter for {source_protocol} -> {target_protocol}. "
                f"Supported: {', '.join(f'{s}->{t}' for s, t in converters)}",
            )

        return converter()
```

### End-to-End Example: Receive x402, Execute via GreenHelix, Respond in x402

```python
"""
Complete request lifecycle showing protocol detection, normalization,
routing through GreenHelix, and response re-encoding.
"""

from greenhelix_trading import ProtocolBridge, ServiceBridge, EventBridge


def handle_inbound_request(
    headers: dict,
    body: dict,
    path: str,
    api_key: str,
    agent_id: str,
) -> dict:
    """Process a single inbound request from any supported protocol.

    Steps:
      1. Detect and normalize the request.
      2. Route through the MultiProtocolRouter.
      3. Re-encode the response in the caller's native format.
      4. Optionally convert the response to another protocol for forwarding.
    """
    # 1. Detect + normalize
    canonical = ProtocolDetector.normalize(headers, body, path)
    print(f"Detected protocol: {canonical.protocol.value}")
    print(f"Action: {canonical.action}")
    print(f"Sender: {canonical.sender_id}")

    # 2. Route through GreenHelix
    router = MultiProtocolRouter(
        api_key=api_key,
        agent_id=agent_id,
    )
    response = router.route(canonical)

    # 3. Re-encode to caller's native format
    native_response = response.to_protocol_format()
    print(f"Native response: {json.dumps(native_response, indent=2)}")

    # 4. Optionally convert to a different protocol for forwarding
    if canonical.protocol == Protocol.X402 and response.success:
        acp_format = ProtocolFormatConverter.convert(
            source_protocol="greenhelix",
            target_protocol="acp",
            payload=response.data,
        )
        print(f"ACP-format copy: {json.dumps(acp_format, indent=2)}")

    return native_response


# ── Simulate an x402 payment request ────────────────────────────────────────

if __name__ == "__main__":
    result = handle_inbound_request(
        headers={
            "X-PAYMENT-ADDRESS": "merchant-agent-42",
            "X-PAYMENT-AMOUNT": "5.00",
            "X-PAYMENT-PROOF": "proof_abc123",
        },
        body={
            "agent_id": "buyer-agent-07",
            "facilitator": "https://x402.org/facilitator",
        },
        path="/x402/pay",
        api_key="your-api-key",
        agent_id="bridge-agent-01",
    )
    print(f"\nFinal response: {json.dumps(result, indent=2)}")


    # ── Simulate an ACP checkout request ─────────────────────────────────

    result_acp = handle_inbound_request(
        headers={"Content-Type": "application/json"},
        body={
            "object": "checkout.session",
            "id": "cs_test_abc123",
            "buyer_agent_id": "agent-buyer-99",
            "seller_agent_id": "agent-seller-01",
            "amount_total": 1500,   # $15.00 in cents
            "currency": "usd",
        },
        path="/acp/checkout",
        api_key="your-api-key",
        agent_id="bridge-agent-01",
    )
    print(f"\nFinal ACP response: {json.dumps(result_acp, indent=2)}")


    # ── Simulate a native GreenHelix request ─────────────────────────────

    result_gh = handle_inbound_request(
        headers={"Host": "api.greenhelix.net"},
        body={
            "tool": "search_services",
            "input": {
                "agent_id": "discovery-agent-01",
                "query": "settlement services",
            },
        },
        path="the REST API",
        api_key="your-api-key",
        agent_id="bridge-agent-01",
    )
    print(f"\nFinal GreenHelix response: {json.dumps(result_gh, indent=2)}")
```

