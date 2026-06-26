---
name: greenhelix-agent-interoperability-bridge
version: "1.3.1"
description: "The Agent Interoperability Bridge: Connecting GreenHelix Agents to x402, ACP, A2A, MCP, Visa TAP, Google AP2/UCP, PayPal Agent Ready, and OpenAI ACP Ecosystems. Practical guide to building working protocol bridges between all nine major agentic web protocols: x402 v2 micropayments, ACP merchant checkout, A2A v2 task orchestration, MCP 1.5+ tool integration, Visa TAP card-network payments, Google AP2 real-time payments, UCP service orchestration, PayPal Agent Ready, and OpenAI ACP commerce flows. Includes detailed code examples with Python bridge classes for protocol translation, cross-protocol identity mapping, intelligent payment routing, and event bri"
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [interoperability, x402, acp, a2a, mcp, visa-tap, google-ap2, ucp, paypal-agent-ready, openai-acp, protocol-bridge, agent-commerce, payment-routing, guide, greenhelix]
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
# The Agent Interoperability Bridge: Connecting GreenHelix Agents to x402, ACP, A2A, MCP, Visa TAP, Google AP2/UCP, PayPal Agent Ready, and OpenAI ACP Ecosystems

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `WALLET_ADDRESS`: Blockchain wallet address for receiving payments (public address only — no private keys)
> - `AGENT_SIGNING_KEY`: Cryptographic signing key for agent identity (Ed25519 key pair for request signing)
> - `STRIPE_API_KEY`: Stripe API key for card payment processing (scoped to payment intents only)


Your GreenHelix agent fleet is processing 10,000 escrow-backed transactions per day. Identity verification is locked down, trust scores are climbing, and your marketplace listings are generating inbound leads. Then a potential partner sends a message: "We run on Google A2A. Can your agents accept task requests from ours?" Another partner follows: "Our billing runs through x402 micropayments. Can your services respond to HTTP 402 flows?" A third asks: "We expose everything through MCP. Can your agents discover and call our tools?" A fourth says: "Our enterprise agents authorize payments through Visa TAP. Can you accept those?" A fifth: "We use Google's AP2 for micropayments and UCP for service orchestration." A sixth: "Our entire merchant base runs PayPal Agent Ready. Can your agents plug in?" A seventh: "We built our agent commerce on OpenAI's ACP. Can your services accept Agentic Commerce Protocol flows?"
You search for integration guides and find protocol comparison articles -- dozens of them. x402 vs. ACP. A2A vs. MCP. Visa TAP vs. Google AP2. Comparison matrices. Architecture diagrams. What you cannot find is a single guide that shows you how to build working bridges between these protocols and your GreenHelix infrastructure. Not theory. Not comparison tables. Working Python classes that translate payment proofs, map identity schemas, convert task formats, and expose tool definitions across protocol boundaries.
This is that guide.

## What You'll Learn
- Chapter 1: The Fragmented Agentic Web
- Chapter 2: x402 v2 Protocol Bridge
- Chapter 3: ACP (Agentic Commerce Protocol) Bridge
- Chapter 4: A2A v2 (Agent-to-Agent) Protocol Bridge
- Chapter 5: MCP 1.5+ (Model Context Protocol) Bridge
- Chapter 6: Visa TAP Bridge
- Chapter 7: Google AP2/UCP Bridge
- Chapter 8: PayPal Agent Ready Bridge
- Chapter 9: OpenAI ACP Bridge
- Chapter 10: Cross-Protocol Identity

## Full Guide

# The Agent Interoperability Bridge: Connecting GreenHelix Agents to x402, ACP, A2A, MCP, Visa TAP, Google AP2/UCP, PayPal Agent Ready, and OpenAI ACP Ecosystems

Your GreenHelix agent fleet is processing 10,000 escrow-backed transactions per day. Identity verification is locked down, trust scores are climbing, and your marketplace listings are generating inbound leads. Then a potential partner sends a message: "We run on Google A2A. Can your agents accept task requests from ours?" Another partner follows: "Our billing runs through x402 micropayments. Can your services respond to HTTP 402 flows?" A third asks: "We expose everything through MCP. Can your agents discover and call our tools?" A fourth says: "Our enterprise agents authorize payments through Visa TAP. Can you accept those?" A fifth: "We use Google's AP2 for micropayments and UCP for service orchestration." A sixth: "Our entire merchant base runs PayPal Agent Ready. Can your agents plug in?" A seventh: "We built our agent commerce on OpenAI's ACP. Can your services accept Agentic Commerce Protocol flows?"

You search for integration guides and find protocol comparison articles -- dozens of them. x402 vs. ACP. A2A vs. MCP. Visa TAP vs. Google AP2. Comparison matrices. Architecture diagrams. What you cannot find is a single guide that shows you how to build working bridges between these protocols and your GreenHelix infrastructure. Not theory. Not comparison tables. Working Python classes that translate payment proofs, map identity schemas, convert task formats, and expose tool definitions across protocol boundaries.

This is that guide.

The 2026 agent protocol landscape has expanded from four major protocols to nine or more. The original four -- x402, ACP, A2A, and MCP -- have matured significantly into their v2 generations. x402 v2 is now backed by the x402 Foundation (Coinbase, Cloudflare, Stripe, AWS, and Microsoft) and has processed over 100 million payments. A2A v2 adds streaming-first task execution and enhanced Agent Card schemas. MCP 1.5+ introduces Streamable HTTP transport, resource subscriptions, and structured tool annotations. Meanwhile, five new heavyweight entrants have arrived: Visa's Transaction Authorization Protocol (TAP), Google's Agent Payments Protocol v2 (AP2) and Universal Commerce Protocol (UCP), PayPal's Agent Ready platform, and OpenAI's Agentic Commerce Protocol (OpenAI ACP). Each brings a different philosophy, a different merchant base, and a different set of integration requirements.

Every bridge class in this guide runs against the GreenHelix API at `https://api.greenhelix.net/v1`. Every code example is production-ready. By the end, your GreenHelix agents will accept x402 v2 micropayments, process ACP checkout flows, respond to A2A v2 task requests, expose services as MCP 1.5+ tools, authorize payments through Visa TAP, process Google AP2 payments and UCP task orchestration, integrate with PayPal's Agent Ready merchant network, and accept OpenAI ACP commerce flows -- without abandoning the escrow, identity, and trust infrastructure you have already built.

---

## Table of Contents

1. [The Fragmented Agentic Web](#chapter-1-the-fragmented-agentic-web)
2. [x402 v2 Protocol Bridge](#chapter-2-x402-v2-protocol-bridge)
3. [ACP (Agentic Commerce Protocol) Bridge](#chapter-3-acp-agentic-commerce-protocol-bridge)
4. [A2A v2 (Agent-to-Agent) Protocol Bridge](#chapter-4-a2a-v2-agent-to-agent-protocol-bridge)
5. [MCP 1.5+ (Model Context Protocol) Bridge](#chapter-5-mcp-15-model-context-protocol-bridge)
6. [Visa TAP Bridge](#chapter-6-visa-tap-bridge)
7. [Google AP2/UCP Bridge](#chapter-7-google-ap2ucp-bridge)
8. [PayPal Agent Ready Bridge](#chapter-8-paypal-agent-ready-bridge)
9. [OpenAI ACP Bridge](#chapter-9-openai-acp-bridge)
10. [Cross-Protocol Identity](#chapter-10-cross-protocol-identity)
11. [Cross-Protocol Payment Routing](#chapter-11-cross-protocol-payment-routing)
12. [Cross-Protocol Event Bridge](#chapter-12-cross-protocol-event-bridge)
13. [Production Bridge Deployment](#chapter-13-production-bridge-deployment)

---

## Chapter 1: The Fragmented Agentic Web

### Nine Protocols, Zero Interoperability

As of April 2026, the agentic web has splintered into at least nine major protocols, each backed by a different technology giant or financial network, each solving a different slice of the agent commerce problem, and none of them talking to each other. The landscape has more than doubled in the past six months alone.

**x402 v2** (x402 Foundation: Coinbase, Cloudflare, Stripe, AWS, Microsoft) revived the HTTP 402 status code to enable pay-per-request micropayments. A server returns 402 with a payment requirement. The client settles the payment -- typically in USDC on Base or Solana -- and retries the request with a payment proof header. The x402 Foundation, formalized in late 2025 with five founding members, has processed over 100 million payments since launch. Version 2 of the protocol adds fiat settlement through Stripe and AWS payment rails, batch payment proofs for multi-step workflows, and a standardized facilitator discovery mechanism via `/.well-known/x402-facilitator.json`. It excels at sub-cent API billing. It has no concept of escrow, identity, or service discovery.

**ACP** (OpenAI, Stripe) -- the Agentic Commerce Protocol -- extends Stripe Checkout for AI agents. An agent browses a merchant catalog, selects a product, and completes a Stripe-based checkout flow. ACP powers Instant Checkout in ChatGPT for merchants on Etsy, Shopify, and Instacart. With the arrival of Visa TAP and PayPal Agent Ready, ACP now competes directly for the enterprise merchant segment it once had largely to itself. ACP's differentiator remains its deep Stripe integration and the ChatGPT distribution channel, but it must now defend its position against protocols backed by incumbents with vastly larger existing merchant bases.

**A2A v2** (Google, with 50+ partners) -- the Agent-to-Agent protocol -- defines a standard for agents to discover each other via Agent Cards (JSON metadata at `/.well-known/agent.json`), exchange tasks with structured message parts, and stream progress updates via Server-Sent Events. Version 2 introduces streaming-first task execution (replacing the poll-based model as the primary path), enhanced Agent Card schemas with capability negotiation and protocol versioning, and a standardized push notification mechanism using webhooks. It remains transport-agnostic and focused on task orchestration, not payments. An A2A v2 agent can describe its capabilities, negotiate interaction modes, and stream partial results, but cannot accept payment without bolting on a separate payment protocol.

**MCP 1.5+** (Anthropic, donated to Linux Foundation) -- the Model Context Protocol -- standardizes how AI models interact with external tools. An MCP server exposes tool schemas (JSON Schema definitions of inputs and outputs). An MCP client -- typically an LLM -- discovers available tools, calls them with structured inputs, and receives structured outputs. MCP 1.5 introduces Streamable HTTP transport (replacing the older SSE-based transport), resource subscriptions for real-time data feeds, structured tool annotations (read-only vs. destructive, idempotent vs. non-idempotent), and OAuth 2.1 authorization flows for remote servers. With 10,000+ servers and enterprise adoption accelerating, MCP is the de facto standard for tool integration in Claude, Cursor, Windsurf, and dozens of other AI clients. It has no built-in payment, identity, or marketplace layer.

**Visa TAP** (Visa) -- the Transaction Authorization Protocol -- brings traditional card network authorization to agent commerce. TAP uses enhanced 3-D Secure 2 (3DS2) flows for agent identity verification and EMV tokenization for secure payment credentials. Visa TAP does not issue new payment rails; it extends the existing Visa network to support AI agent transactions. An agent presents a Visa TAP token, the acquiring bank authorizes the transaction through the existing VisaNet infrastructure, and settlement occurs through standard card network settlement. TAP's advantage is instant access to 100+ million merchants already accepting Visa. Its disadvantage is card-network transaction fees (1.5-3.5%) that make sub-cent micropayments economically infeasible.

**Google AP2** (Google) -- the Agent Payments Protocol v2 -- is built on the real-time payment patterns proven by UPI (India) and Pix (Brazil). AP2 supports six payment types: micropayments (sub-cent), standard transactions, subscriptions, escrow, split payments, and batch settlements. AP2 uses a hub-and-spoke architecture where Google acts as the payment hub, agents register as spokes, and payments settle through Google's treasury infrastructure. AP2 targets the same micropayment niche as x402 but adds subscription and escrow primitives that x402 lacks.

**Google UCP** (Google) -- the Universal Commerce Protocol -- is Google's answer to the service discovery and task orchestration problem. Where A2A handles task exchange between agents, UCP provides a higher-level commerce layer: service catalogs, pricing negotiation, SLA definitions, and multi-step workflow orchestration. UCP and A2A are complementary -- A2A handles the task-level communication, UCP handles the commercial wrapper around it. In practice, a UCP service listing includes an A2A endpoint for task execution and an AP2 endpoint for payment.

**PayPal Agent Ready** (PayPal, Braintree) -- uses Fastlane tokens for one-tap agent authentication and Braintree's GraphQL API for payment processing. Agent Ready targets PayPal's existing 400+ million consumer accounts and 35+ million merchant accounts. An agent authenticating through Agent Ready can access the consumer's PayPal wallet, Venmo balance, or linked bank accounts. For merchants, Agent Ready integrates through Braintree's existing SDKs with a new `agent_context` parameter that flags the transaction as agent-initiated. Agent Ready's advantage is the largest existing consumer wallet base in Western markets. Its disadvantage is PayPal-only settlement with no crypto or real-time payment rail options.

**OpenAI ACP** (OpenAI) -- the Agentic Commerce Protocol -- is OpenAI's dedicated agent-to-agent commerce framework, distinct from the earlier ACP (Stripe-based checkout). OpenAI ACP defines a commerce graph where agents publish service manifests (capabilities, pricing tiers, SLAs, and accepted payment methods), discover each other through a centralized registry, and negotiate terms programmatically before executing transactions. OpenAI ACP supports multiple payment backends -- Stripe, x402, and direct bank transfers -- through a pluggable payment adapter layer. The protocol includes built-in dispute resolution, usage metering, and refund flows. Its differentiator is deep integration with ChatGPT Plugins and the OpenAI agent platform, giving service providers access to OpenAI's consumer and enterprise distribution channels. Its disadvantage is vendor lock-in: the registry and dispute resolution are centralized through OpenAI infrastructure.

**TAP (Token Agent Protocol)** -- an emerging protocol for on-chain agent coordination using ERC-8183 and ERC-8004. It provides smart-contract escrow and on-chain agent registries. It requires Ethereum gas for every state transition, making it expensive for high-frequency interactions.

### The Interoperability Problem

If your agents live in the GreenHelix ecosystem, you already have escrow-backed payments, cryptographic identity, trust scoring, marketplace discovery, event-driven webhooks, and 128 tools accessible through a single API. The problem is not capability. The problem is reach.

A potential client running x402-native infrastructure cannot pay your GreenHelix agent because your agent does not speak x402. A partner running Google A2A cannot discover your agent because you do not publish an Agent Card. An MCP client cannot call your services because your tools are not exposed as MCP tool definitions. An ACP agent cannot purchase your service because you do not have an ACP-compatible product listing. An enterprise running Visa TAP cannot authorize payments to your agent. A Google AP2/UCP deployment cannot discover or pay your services. A PayPal merchant cannot process agent transactions through your endpoint. An agent in the OpenAI ACP ecosystem cannot find your service manifest or negotiate terms with your agent.

Every protocol boundary is a lost transaction. Every missing bridge is a partner who goes elsewhere. With nine protocols and counting, the cost of not bridging is nine times what it was a year ago.

### The Bridge Architecture

The solution is not to abandon GreenHelix and rewrite everything for each protocol. The solution is an adapter pattern: a thin protocol translation layer that sits between the external protocol and your GreenHelix infrastructure.

```
  External Protocol          Bridge Layer            GreenHelix
  ┌──────────────┐     ┌─────────────────────┐     ┌──────────────┐
  │  x402 Client  │────▶│  X402Bridge          │────▶│  create_escrow│
  │  ACP Agent    │────▶│  ACPBridge           │────▶│  create_      │
  │  A2A Agent    │────▶│  A2ABridge           │────▶│    payment_   │
  │  MCP Client   │────▶│  MCPBridge           │────▶│    intent     │
  │  Visa TAP     │────▶│  VisaTAPBridge       │────▶│  register_   │
  │  Google AP2   │────▶│  AP2UCPBridge        │────▶│    agent      │
  │  PayPal Ready │────▶│  PayPalBridge        │────▶│  publish_event│
  │  OpenAI ACP   │────▶│  OpenAIACPBridge     │────▶│  search_      │
  └──────────────┘     │                     │     │    services   │
                        │  IdentityMapper     │────▶│              │
                        │  PaymentRouter      │────▶│              │
                        │  EventBridge        │────▶│              │
                        └─────────────────────┘     └──────────────┘
```

Each bridge class handles three responsibilities: **translate** the incoming protocol message into a GreenHelix API call, **execute** the call against the REST API (`POST /v1/{tool}`), and **translate** the GreenHelix response back into the external protocol's expected format. The bridges share a common `GreenHelixClient` base class and a unified `IdentityMapper` for cross-protocol identity resolution.

The remainder of this guide builds each bridge, starting with x402.

---

## Chapter 2: x402 v2 Protocol Bridge

### How x402 v2 Works

The x402 protocol is elegant in its simplicity. It adds a payment layer directly to HTTP by leveraging the 402 Payment Required status code that has existed in the HTTP specification since 1997 but was never standardized until Coinbase and Cloudflare defined a concrete implementation in late 2025. Version 2, released in early 2026, extends the original with fiat settlement paths, batch payment proofs, and facilitator discovery.

The flow has four steps:

1. A client sends an HTTP request to a server.
2. The server returns HTTP 402 with headers specifying the payment requirement: amount, currency (USDC, USD, or EUR in v2), facilitator URL, accepted settlement methods, and a payment address.
3. The client sends payment to the facilitator, which settles on-chain (Base L2 or Solana) or via fiat rails (Stripe or AWS Payments in v2).
4. The client retries the original request with an `X-PAYMENT-PROOF` header containing the transaction hash, facilitator signature, and settlement method.

The server validates the payment proof, verifies settlement with the facilitator, and serves the response. The entire flow adds one round-trip to the normal request-response cycle. For micropayments -- $0.001 to $0.10 per request -- the overhead is acceptable.

### The GreenHelix x402 Adapter

To accept x402 payments, your GreenHelix agent needs to do three things: issue 402 responses with correct payment headers, validate incoming payment proofs, and record the payment in GreenHelix's ledger via escrow. The escrow step is critical -- it means every x402 payment is tracked, auditable, and subject to the same trust and compliance infrastructure as native GreenHelix transactions.

```python
import requests
import hashlib
import time
import json
from typing import Optional


class GreenHelixClient:
    """Base client for all bridge classes."""

    def __init__(self, api_key: str, base_url: str = "https://api.greenhelix.net/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    def execute(self, tool: str, inputs: dict) -> dict:
        """Execute a GreenHelix tool."""
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": inputs},
        )
        resp.raise_for_status()
        return resp.json()


class X402Bridge:
    """Translates x402 v2 micropayment flows into GreenHelix escrow transactions.

    Supports both crypto (USDC on Base/Solana) and fiat (Stripe/AWS) settlement
    paths introduced in x402 v2.
    """

    SUPPORTED_SETTLEMENT = {"crypto", "stripe", "aws"}

    def __init__(self, client: GreenHelixClient, agent_id: str,
                 facilitator_url: str, payment_address: str,
                 accepted_settlements: list = None):
        self.client = client
        self.agent_id = agent_id
        self.facilitator_url = facilitator_url
        self.payment_address = payment_address
        self.accepted_settlements = accepted_settlements or ["crypto", "stripe"]

    def create_402_response(self, price_usd: float, resource_id: str) -> dict:
        """Generate the headers for an HTTP 402 response.

        Returns a dict of headers to attach to the 402 response.
        x402 v2 adds settlement method negotiation and batch proof support.
        """
        return {
            "X-PAYMENT-REQUIRED": "true",
            "X-PAYMENT-AMOUNT": str(price_usd),
            "X-PAYMENT-CURRENCY": "USD",
            "X-PAYMENT-ADDRESS": self.payment_address,
            "X-PAYMENT-FACILITATOR": self.facilitator_url,
            "X-PAYMENT-RESOURCE": resource_id,
            "X-PAYMENT-EXPIRY": str(int(time.time()) + 300),  # 5 min window
            "X-PAYMENT-VERSION": "2",
            "X-PAYMENT-SETTLEMENTS": ",".join(self.accepted_settlements),
        }

    def validate_payment_proof(self, proof_header: str) -> dict:
        """Validate an x402 payment proof against the facilitator.

        Returns the validated payment details or raises ValueError.
        """
        try:
            proof_data = json.loads(proof_header)
        except json.JSONDecodeError:
            raise ValueError("Malformed payment proof header")

        tx_hash = proof_data.get("tx_hash")
        facilitator_sig = proof_data.get("facilitator_signature")
        amount = proof_data.get("amount")

        if not all([tx_hash, facilitator_sig, amount]):
            raise ValueError("Payment proof missing required fields")

        # Verify with the facilitator that the payment settled
        verify_resp = requests.post(
            f"{self.facilitator_url}/verify",
            json={
                "tx_hash": tx_hash,
                "expected_address": self.payment_address,
                "expected_amount": str(amount),
            },
            timeout=10,
        )
        if verify_resp.status_code != 200:
            raise ValueError(f"Facilitator rejected proof: {verify_resp.text}")

        return verify_resp.json()

    def record_in_greenhelix(self, payment_proof: dict,
                              resource_id: str, payer_id: str) -> dict:
        """Record the x402 payment as a GreenHelix escrow for auditability.

        Creates a completed escrow that records the external payment in the
        GreenHelix ledger, preserving the full audit trail.
        """
        escrow = self.client.execute("create_escrow", {
            "payer_agent_id": payer_id,
            "payee_agent_id": self.agent_id,
            "amount": str(payment_proof["amount"]),
            "description": (
                f"x402 payment for resource {resource_id}. "
                f"TX: {payment_proof['tx_hash']}. "
                f"Facilitator: {self.facilitator_url}"
            ),
            "escrow_type": "standard",
            "metadata": json.dumps({
                "protocol": "x402",
                "tx_hash": payment_proof["tx_hash"],
                "resource_id": resource_id,
            }),
        })
        return escrow

    def handle_request(self, request_headers: dict, resource_id: str,
                       price_usd: float, payer_id: str) -> dict:
        """Full x402 flow: check for proof, validate, record, or return 402.

        Returns either a 402 response dict or a success dict with the
        recorded escrow.
        """
        proof_header = request_headers.get("X-PAYMENT-PROOF")

        if not proof_header:
            return {
                "status": 402,
                "headers": self.create_402_response(price_usd, resource_id),
            }

        payment_proof = self.validate_payment_proof(proof_header)
        escrow = self.record_in_greenhelix(payment_proof, resource_id, payer_id)

        return {
            "status": 200,
            "escrow_id": escrow.get("escrow_id"),
            "payment_recorded": True,
        }
```

### Exposing GreenHelix Services as x402 Endpoints

To make your GreenHelix service discoverable by x402 clients, wrap it in a lightweight HTTP server that returns 402 for unauthenticated requests. Here is a Flask example:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

client = GreenHelixClient(api_key="your-api-key")
bridge = X402Bridge(
    client=client,
    agent_id="my-summarizer-agent",
    facilitator_url="https://facilitator.x402.org",
    payment_address="0xYourUSDCAddress",
)


@app.route("/api/summarize", methods=["POST"])
def summarize():
    result = bridge.handle_request(
        request_headers=dict(request.headers),
        resource_id="summarize-v1",
        price_usd=0.05,
        payer_id=request.headers.get("X-AGENT-ID", "unknown"),
    )

    if result["status"] == 402:
        return jsonify({"error": "payment_required"}), 402, result["headers"]

    # Payment verified -- execute the actual service via GreenHelix
    service_result = client.execute("search_services", {
        "query": "summarization",
        "agent_id": "my-summarizer-agent",
    })

    return jsonify({
        "result": service_result,
        "escrow_id": result["escrow_id"],
    })
```

### Key Design Decisions

**Why escrow, not direct deposit?** Recording x402 payments as escrow entries -- even though the payment already settled on-chain -- gives you the full GreenHelix audit trail. Every x402 payment appears in your ledger alongside native payments. Trust scores, compliance reports, and financial reconciliation work across both payment sources.

**Expiry windows.** The `X-PAYMENT-EXPIRY` header gives the client 5 minutes to complete payment. This prevents replay attacks where a client reuses an old payment proof for a new request. The facilitator enforces the expiry on the settlement side; your bridge enforces it on the proof validation side.

**Idempotency.** The `tx_hash` from the payment proof is unique per transaction. If a client retries with the same proof, your bridge should check whether an escrow with that `tx_hash` already exists before creating a duplicate. Add a cache or database lookup keyed on `tx_hash` in production.

---

## Chapter 3: ACP (Agentic Commerce Protocol) Bridge

### How ACP Works

The Agentic Commerce Protocol, developed jointly by OpenAI and Stripe, enables AI agents to purchase products and services from merchants through Stripe-powered checkout flows. ACP defines three entities: the **buyer agent** (an AI that wants to purchase something), the **merchant** (a service with a Stripe account and product catalog), and the **orchestrator** (typically ChatGPT or another host application that manages the checkout UI).

The flow:

1. The buyer agent discovers a merchant's product catalog via the ACP product listing API.
2. The agent selects a product and initiates checkout by creating a Stripe Payment Intent.
3. The orchestrator presents a checkout surface to the user (or auto-approves for pre-authorized agents).
4. Stripe processes the payment. The merchant fulfills the order.
5. The merchant sends the fulfillment result back to the agent.

ACP is designed for agent-to-merchant transactions. It assumes the merchant has a Stripe account, a product catalog, and a fulfillment pipeline. Your GreenHelix agent is not a Stripe merchant. But it can act as one with the right bridge.

### Translating ACP Product Listings to GreenHelix Marketplace

The first step is making your GreenHelix services visible to ACP agents. ACP product listings follow a specific schema. Your bridge translates GreenHelix marketplace entries into that schema.

```python
class ACPBridge:
    """Translates ACP checkout flows into GreenHelix payment intents."""

    def __init__(self, client: GreenHelixClient, agent_id: str,
                 stripe_webhook_secret: str = ""):
        self.client = client
        self.agent_id = agent_id
        self.stripe_webhook_secret = stripe_webhook_secret

    def greenhelix_service_to_acp_listing(self, service: dict) -> dict:
        """Convert a GreenHelix marketplace service into an ACP product listing.

        ACP expects a specific schema for product discovery. This method
        maps GreenHelix fields to ACP fields.
        """
        return {
            "id": service.get("service_id"),
            "name": service.get("name"),
            "description": service.get("description"),
            "price": {
                "amount": int(float(service.get("price", "0")) * 100),
                "currency": "usd",
            },
            "fulfillment_type": "digital",
            "provider": {
                "name": service.get("provider_agent_id", self.agent_id),
                "protocol": "greenhelix",
            },
            "metadata": {
                "greenhelix_service_id": service.get("service_id"),
                "greenhelix_agent_id": self.agent_id,
            },
        }

    def sync_listings_to_acp(self) -> list:
        """Pull all services from GreenHelix marketplace and convert to ACP format."""
        services = self.client.execute("search_services", {
            "provider_agent_id": self.agent_id,
        })
        service_list = services.get("services", [])
        return [
            self.greenhelix_service_to_acp_listing(s) for s in service_list
        ]

    def handle_acp_purchase(self, acp_intent: dict) -> dict:
        """Translate an ACP purchase intent into a GreenHelix payment intent.

        When an ACP agent initiates checkout for one of your listings,
        this method creates the corresponding GreenHelix payment intent
        and returns the mapping.
        """
        greenhelix_service_id = (
            acp_intent.get("metadata", {}).get("greenhelix_service_id")
        )
        if not greenhelix_service_id:
            raise ValueError("ACP intent missing greenhelix_service_id metadata")

        buyer_agent_id = acp_intent.get("buyer", {}).get("agent_id", "acp-buyer")
        amount_cents = acp_intent.get("amount", 0)
        amount_usd = str(amount_cents / 100)

        # Create a GreenHelix payment intent that mirrors the ACP transaction
        payment_intent = self.client.execute("create_payment_intent", {
            "payer_agent_id": buyer_agent_id,
            "payee_agent_id": self.agent_id,
            "amount": amount_usd,
            "description": (
                f"ACP checkout for service {greenhelix_service_id}. "
                f"ACP intent: {acp_intent.get('id', 'unknown')}"
            ),
            "metadata": json.dumps({
                "protocol": "acp",
                "acp_intent_id": acp_intent.get("id"),
                "stripe_payment_intent": acp_intent.get("stripe_pi_id"),
            }),
        })

        return {
            "greenhelix_payment_intent": payment_intent,
            "acp_intent_id": acp_intent.get("id"),
            "status": "payment_intent_created",
        }

    def handle_acp_fulfillment(self, acp_intent_id: str,
                                 greenhelix_payment_id: str,
                                 result: dict) -> dict:
        """Complete the ACP fulfillment flow after service delivery.

        After your GreenHelix agent completes the work, this method
        formats the result in ACP's expected fulfillment schema and
        publishes a completion event.
        """
        # Publish the completion event in GreenHelix
        self.client.execute("publish_event", {
            "event_type": "acp.fulfillment.completed",
            "agent_id": self.agent_id,
            "payload": json.dumps({
                "acp_intent_id": acp_intent_id,
                "greenhelix_payment_id": greenhelix_payment_id,
                "result": result,
            }),
        })

        # Return ACP-formatted fulfillment response
        return {
            "intent_id": acp_intent_id,
            "status": "fulfilled",
            "result": result,
            "provider": {
                "protocol": "greenhelix",
                "agent_id": self.agent_id,
            },
        }

    def register_as_acp_merchant(self, service_name: str,
                                   service_description: str,
                                   price_usd: float) -> dict:
        """Register your GreenHelix agent as both a GreenHelix marketplace
        service and an ACP-compatible merchant.

        Creates the GreenHelix marketplace entry and returns the ACP-formatted
        listing for registration with ACP directories.
        """
        # Register in GreenHelix marketplace
        gh_service = self.client.execute("register_service", {
            "agent_id": self.agent_id,
            "name": service_name,
            "description": service_description,
            "price": str(price_usd),
            "tags": json.dumps(["acp-compatible", "bridge"]),
        })

        # Convert to ACP listing format
        acp_listing = self.greenhelix_service_to_acp_listing(gh_service)

        return {
            "greenhelix_service": gh_service,
            "acp_listing": acp_listing,
        }
```

### Accepting Payments from ACP Agents

The key insight is that ACP payments settle through Stripe, while GreenHelix payments settle through the gateway's internal ledger. Your bridge creates a corresponding GreenHelix payment intent for every ACP checkout, linking the two via metadata. This gives you dual-ledger auditability: Stripe's records for the fiat side, GreenHelix's records for the agent commerce side.

When an ACP agent initiates checkout:

1. Your bridge receives the ACP intent via webhook.
2. It calls `handle_acp_purchase()` to create the GreenHelix payment intent.
3. Stripe processes the payment on the ACP side.
4. Your agent performs the service.
5. `handle_acp_fulfillment()` records completion in both systems.

```python
# Webhook handler for incoming ACP purchase events
@app.route("/webhooks/acp", methods=["POST"])
def acp_webhook():
    event = request.json
    event_type = event.get("type")

    if event_type == "checkout.initiated":
        result = acp_bridge.handle_acp_purchase(event.get("intent"))
        return jsonify(result)

    elif event_type == "payment.completed":
        # Stripe has confirmed payment -- now fulfill via GreenHelix
        intent_id = event["intent"]["id"]
        payment_id = event["intent"]["greenhelix_payment_id"]

        # Execute your GreenHelix-backed service
        service_result = client.execute("search_services", {
            "service_id": event["intent"]["metadata"]["greenhelix_service_id"],
        })

        fulfillment = acp_bridge.handle_acp_fulfillment(
            acp_intent_id=intent_id,
            greenhelix_payment_id=payment_id,
            result=service_result,
        )
        return jsonify(fulfillment)

    return jsonify({"status": "ignored"}), 200
```

### Identity Mapping for ACP

ACP identifies merchants by Stripe account ID. GreenHelix identifies agents by `agent_id` and Ed25519 public key. Your bridge must maintain a mapping between these identities. The `IdentityMapper` class in Chapter 10 handles this -- but at the ACP layer, you store the Stripe account ID alongside the GreenHelix agent registration:

```python
# When registering, link GreenHelix identity to Stripe identity
identity_mapper.register_mapping(
    greenhelix_agent_id="my-summarizer-agent",
    protocol="acp",
    external_id="acct_1234567890",  # Stripe account ID
    metadata={"stripe_account_type": "express"},
)
```

---

## Chapter 4: A2A v2 (Agent-to-Agent) Protocol Bridge

### How Google's A2A v2 Works

Google's Agent-to-Agent protocol defines a standard for agents to discover each other and exchange work. Version 2 refines the original with streaming-first execution, enhanced capability negotiation, and push notifications. Four concepts are central:

**Agent Cards (v2).** Every A2A agent publishes a JSON metadata file at `/.well-known/agent.json`. The v2 card schema adds protocol version negotiation, supported interaction modes (streaming, push, poll), capability tags for semantic matching, and optional payment endpoint references. Think of it as a machine-readable resume with contract terms.

**Tasks.** When one agent wants to hire another, it creates a Task. The task has an ID, a description, input data (as "message parts" -- text, files, structured data), and a lifecycle: `submitted` -> `working` -> `completed` (or `failed`, `canceled`). In v2, streaming is the primary interaction mode -- the hiring agent receives task updates via Server-Sent Events in real time, with polling as a fallback.

**Messages.** Task progress is communicated through messages. Each message contains one or more "parts" -- text parts, file parts, or data parts. The agent processing the task sends messages as it works, and a final message with the result when done.

**Push Notifications (v2).** A2A v2 introduces a standardized push notification mechanism. Agents can register webhook URLs during task creation, and the executing agent delivers status updates to those URLs. This replaces the need for long-lived SSE connections in asynchronous workflows.

A2A deliberately does not include payments. It is a task orchestration protocol. Your bridge adds GreenHelix's payment layer to A2A's task orchestration.

### Mapping A2A Agent Cards to GreenHelix Identities

Your GreenHelix agent has a registered identity with capabilities, a public key, and a trust score. An A2A agent has an Agent Card with skills, authentication info, and endpoint URLs. The bridge maps between them.

```python
class A2ABridge:
    """Translates A2A task requests into GreenHelix service calls and
    publishes GreenHelix agents as A2A-discoverable."""

    def __init__(self, client: GreenHelixClient, agent_id: str,
                 base_url: str = "https://your-agent.example.com"):
        self.client = client
        self.agent_id = agent_id
        self.base_url = base_url

    def generate_agent_card(self) -> dict:
        """Generate an A2A v2 Agent Card from GreenHelix agent identity.

        Pulls the agent's identity and marketplace listings from GreenHelix
        and formats them as an A2A v2-compliant Agent Card with capability
        negotiation and payment endpoint references.
        """
        identity = self.client.execute("get_agent_identity", {
            "agent_id": self.agent_id,
        })

        services = self.client.execute("search_services", {
            "provider_agent_id": self.agent_id,
        })
        service_list = services.get("services", [])

        skills = []
        for svc in service_list:
            skills.append({
                "id": svc.get("service_id"),
                "name": svc.get("name"),
                "description": svc.get("description"),
                "tags": svc.get("tags", []),
                "examples": [
                    f"Use this skill to {svc.get('description', 'perform a task')}"
                ],
            })

        return {
            "name": identity.get("name", self.agent_id),
            "description": identity.get("description", ""),
            "url": self.base_url,
            "version": "2.0.0",
            "protocolVersion": "2.0",
            "capabilities": {
                "streaming": True,
                "pushNotifications": True,
                "stateTransitionHistory": True,
            },
            "authentication": {
                "schemes": ["bearer"],
                "credentials": None,  # Provided at runtime
            },
            "defaultInputModes": ["text/plain", "application/json"],
            "defaultOutputModes": ["text/plain", "application/json"],
            "skills": skills,
            "provider": {
                "organization": "GreenHelix",
                "url": "https://api.greenhelix.net",
            },
            "supportsPayment": {
                "protocols": ["greenhelix", "x402", "ap2"],
                "endpoint": f"{self.base_url}/payment",
            },
            "x-greenhelix": {
                "agent_id": self.agent_id,
                "public_key": identity.get("public_key"),
                "trust_score": identity.get("trust_score"),
            },
        }

    def handle_a2a_task(self, task_request: dict) -> dict:
        """Translate an incoming A2A task request into a GreenHelix service call.

        Extracts the task description and input parts, maps them to a
        GreenHelix service execution, and returns the result formatted
        as A2A task messages.
        """
        task_id = task_request.get("id", f"a2a-{int(time.time())}")
        skill_id = task_request.get("skill_id")
        input_parts = task_request.get("message", {}).get("parts", [])

        # Extract text input from A2A message parts
        text_input = ""
        structured_input = {}
        for part in input_parts:
            if part.get("type") == "text":
                text_input += part.get("text", "")
            elif part.get("type") == "data":
                structured_input.update(part.get("data", {}))

        # Look up the GreenHelix service corresponding to this skill
        service = self.client.execute("search_services", {
            "service_id": skill_id,
            "provider_agent_id": self.agent_id,
        })

        # Create a payment intent for the A2A task if the service has a price
        payment_result = None
        caller_id = task_request.get("caller_agent_id", "a2a-caller")
        service_price = service.get("price", "0")

        if float(service_price) > 0:
            payment_result = self.client.execute("create_payment_intent", {
                "payer_agent_id": caller_id,
                "payee_agent_id": self.agent_id,
                "amount": service_price,
                "description": f"A2A task {task_id} for skill {skill_id}",
                "metadata": json.dumps({
                    "protocol": "a2a",
                    "a2a_task_id": task_id,
                }),
            })

        # Publish event for tracking
        self.client.execute("publish_event", {
            "event_type": "a2a.task.received",
            "agent_id": self.agent_id,
            "payload": json.dumps({
                "task_id": task_id,
                "skill_id": skill_id,
                "caller": caller_id,
            }),
        })

        return {
            "id": task_id,
            "status": {"state": "working"},
            "messages": [
                {
                    "role": "agent",
                    "parts": [
                        {
                            "type": "text",
                            "text": f"Task accepted. Processing via GreenHelix agent {self.agent_id}.",
                        }
                    ],
                }
            ],
            "greenhelix_payment": payment_result,
        }

    def complete_a2a_task(self, task_id: str, result_text: str,
                           result_data: dict = None) -> dict:
        """Mark an A2A task as completed and return the result.

        Formats the GreenHelix service output as A2A message parts.
        """
        parts = [{"type": "text", "text": result_text}]
        if result_data:
            parts.append({"type": "data", "data": result_data})

        # Publish completion event
        self.client.execute("publish_event", {
            "event_type": "a2a.task.completed",
            "agent_id": self.agent_id,
            "payload": json.dumps({
                "task_id": task_id,
                "result_summary": result_text[:200],
            }),
        })

        return {
            "id": task_id,
            "status": {"state": "completed"},
            "messages": [
                {
                    "role": "agent",
                    "parts": parts,
                }
            ],
        }

    def publish_agent_card(self) -> dict:
        """Register the agent card in GreenHelix and return it for serving.

        The card should be served at /.well-known/agent.json on your
        agent's HTTP endpoint.
        """
        card = self.generate_agent_card()

        # Also register a webhook so GreenHelix events can notify A2A callers
        self.client.execute("register_webhook", {
            "agent_id": self.agent_id,
            "url": f"{self.base_url}/a2a/tasks/webhook",
            "events": json.dumps([
                "a2a.task.received",
                "a2a.task.completed",
            ]),
        })

        return card
```

### Publishing GreenHelix Agents as A2A-Discoverable

To make your agent visible to A2A clients, serve the Agent Card at the well-known URL:

```python
@app.route("/.well-known/agent.json")
def agent_card():
    card = a2a_bridge.generate_agent_card()
    return jsonify(card)


@app.route("/a2a/tasks", methods=["POST"])
def create_task():
    task_request = request.json
    result = a2a_bridge.handle_a2a_task(task_request)
    return jsonify(result), 201


@app.route("/a2a/tasks/<task_id>", methods=["GET"])
def get_task(task_id):
    # In production, retrieve task state from your storage
    return jsonify({"id": task_id, "status": {"state": "working"}})
```

### Adding Payments to A2A

A2A has no payment primitive. Your bridge adds one by creating a GreenHelix payment intent for every task. The caller agent must have a GreenHelix wallet (or you create a temporary one via the `IdentityMapper`). The payment intent ID is returned in the task response, and the caller's payment must be confirmed before your agent delivers the final result. This transforms A2A from a free task protocol into a paid service protocol with escrow-backed guarantees.

---

## Chapter 5: MCP 1.5+ (Model Context Protocol) Bridge

### How MCP 1.5 Works

The Model Context Protocol defines a client-server architecture for tool integration. An MCP server exposes a catalog of tools, each described by a JSON Schema that specifies the tool's name, description, input parameters, and output format. An MCP client -- typically an LLM runtime like Claude, Cursor, or a custom agent -- connects to the server, discovers available tools, calls them with structured inputs, and receives structured outputs.

MCP 1.5 introduces Streamable HTTP transport (replacing the older SSE-only transport for remote servers), making deployment simpler and more compatible with standard HTTP infrastructure. The protocol defines these core methods:

- `tools/list` -- returns the catalog of available tools with annotations.
- `tools/call` -- executes a specific tool with provided arguments.
- `resources/list` -- returns available data resources (optional).
- `resources/subscribe` -- subscribes to resource changes (new in 1.5).

MCP 1.5 also adds structured tool annotations: `readOnlyHint`, `destructiveHint`, `idempotentHint`, and `openWorldHint`. These annotations tell MCP clients whether a tool reads data, modifies state, or can be safely retried -- critical information for agent commerce tools that handle payments. OAuth 2.1 authorization for remote MCP servers means your bridge can enforce authentication without custom middleware.

With 10,000+ servers and enterprise adoption accelerating after the Linux Foundation donation, MCP is the de facto standard for tool integration in the AI ecosystem. By exposing your GreenHelix services as MCP tools, any MCP-compatible client can discover and call them without knowing anything about the GreenHelix API.

### Exposing GreenHelix Tools as MCP Tool Definitions

The bridge translates GreenHelix's tool catalog into MCP tool schemas and wraps each the REST API (`POST /v1/{tool}`) call as an MCP tool invocation.

```python
class MCPBridge:
    """Wraps GreenHelix execute API as MCP-compatible tool definitions."""

    def __init__(self, client: GreenHelixClient, agent_id: str,
                 exposed_tools: list = None):
        self.client = client
        self.agent_id = agent_id
        # Only expose specific tools, not the full 128-tool catalog
        self.exposed_tools = exposed_tools or []
        self._tool_schemas = {}

    def define_tool_schema(self, tool_name: str, description: str,
                            input_schema: dict, price_usd: float = 0,
                            read_only: bool = True, idempotent: bool = True,
                            destructive: bool = False) -> dict:
        """Define an MCP 1.5 tool schema for a GreenHelix tool.

        Each exposed tool gets a JSON Schema definition with MCP 1.5
        annotations that MCP clients use for discovery, safety
        classification, and invocation.
        """
        schema = {
            "name": f"greenhelix_{tool_name}",
            "description": description,
            "inputSchema": {
                "type": "object",
                "properties": input_schema,
            },
            "annotations": {
                "readOnlyHint": read_only,
                "destructiveHint": destructive,
                "idempotentHint": idempotent,
                "openWorldHint": True,
            },
            "x-greenhelix": {
                "tool": tool_name,
                "agent_id": self.agent_id,
                "price_usd": price_usd,
            },
        }
        self._tool_schemas[tool_name] = schema
        return schema

    def register_standard_tools(self) -> list:
        """Register a curated set of GreenHelix tools as MCP 1.5 tool definitions.

        Returns the list of MCP tool schemas for tools/list responses.
        Each tool includes MCP 1.5 annotations for safety classification.
        """
        tools = []

        tools.append(self.define_tool_schema(
            tool_name="search_services",
            description="Search the GreenHelix agent marketplace for services matching a query.",
            input_schema={
                "query": {
                    "type": "string",
                    "description": "Search query for finding agent services",
                },
                "tags": {
                    "type": "string",
                    "description": "Comma-separated tags to filter by",
                },
            },
            read_only=True,
            idempotent=True,
        ))

        tools.append(self.define_tool_schema(
            tool_name="get_agent_identity",
            description="Retrieve the identity and trust score of a GreenHelix agent.",
            input_schema={
                "agent_id": {
                    "type": "string",
                    "description": "The agent ID to look up",
                },
            },
            read_only=True,
            idempotent=True,
        ))

        tools.append(self.define_tool_schema(
            tool_name="send_message",
            description="Send a message to a GreenHelix agent.",
            input_schema={
                "sender_agent_id": {
                    "type": "string",
                    "description": "Your agent ID",
                },
                "receiver_agent_id": {
                    "type": "string",
                    "description": "The recipient agent ID",
                },
                "content": {
                    "type": "string",
                    "description": "The message content",
                },
            },
            read_only=False,
            idempotent=False,
            destructive=False,
        ))

        # Add custom tools from exposed_tools list
        for tool_name in self.exposed_tools:
            if tool_name not in self._tool_schemas:
                tools.append(self.define_tool_schema(
                    tool_name=tool_name,
                    description=f"Execute the {tool_name} GreenHelix tool.",
                    input_schema={
                        "input": {
                            "type": "object",
                            "description": f"Input parameters for {tool_name}",
                        },
                    },
                ))

        return tools

    def handle_tools_list(self) -> dict:
        """Handle an MCP tools/list request.

        Returns a JSON-RPC 2.0 response with all registered tool schemas.
        """
        if not self._tool_schemas:
            self.register_standard_tools()

        return {
            "jsonrpc": "2.0",
            "result": {
                "tools": list(self._tool_schemas.values()),
            },
        }

    def handle_tools_call(self, tool_name: str, arguments: dict,
                           caller_id: str = "mcp-client") -> dict:
        """Handle an MCP tools/call request.

        Translates the MCP tool call into a GreenHelix execute API call
        and formats the response as a JSON-RPC 2.0 result.
        """
        # Strip the greenhelix_ prefix if present
        gh_tool_name = tool_name.replace("greenhelix_", "")

        if gh_tool_name not in self._tool_schemas:
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32601,
                    "message": f"Tool not found: {tool_name}",
                },
            }

        # Check if this tool has a price -- if so, create a payment intent
        schema = self._tool_schemas[gh_tool_name]
        price = schema.get("x-greenhelix", {}).get("price_usd", 0)

        payment_info = None
        if price > 0:
            payment_info = self.client.execute("create_payment_intent", {
                "payer_agent_id": caller_id,
                "payee_agent_id": self.agent_id,
                "amount": str(price),
                "description": f"MCP tool call: {gh_tool_name}",
                "metadata": json.dumps({
                    "protocol": "mcp",
                    "tool": gh_tool_name,
                }),
            })

        # Execute the GreenHelix tool
        result = self.client.execute(gh_tool_name, arguments)

        # Publish event for cross-protocol tracking
        self.client.execute("publish_event", {
            "event_type": "mcp.tool.called",
            "agent_id": self.agent_id,
            "payload": json.dumps({
                "tool": gh_tool_name,
                "caller": caller_id,
                "has_payment": price > 0,
            }),
        })

        return {
            "jsonrpc": "2.0",
            "result": {
                "content": [
                    {
                        "type": "text",
                        "text": json.dumps(result, indent=2),
                    }
                ],
                "x-greenhelix-payment": payment_info,
            },
        }
```

### Running the MCP Server

MCP servers communicate over stdio (for local tools) or Streamable HTTP (for remote tools, replacing the older SSE transport in MCP 1.5). Here is a minimal Streamable HTTP-based MCP server that wraps your GreenHelix bridge:

```python
@app.route("/mcp", methods=["POST"])
def mcp_endpoint():
    rpc_request = request.json
    method = rpc_request.get("method")
    params = rpc_request.get("params", {})
    rpc_id = rpc_request.get("id")

    if method == "tools/list":
        response = mcp_bridge.handle_tools_list()
    elif method == "tools/call":
        response = mcp_bridge.handle_tools_call(
            tool_name=params.get("name"),
            arguments=params.get("arguments", {}),
            caller_id=request.headers.get("X-AGENT-ID", "mcp-client"),
        )
    else:
        response = {
            "jsonrpc": "2.0",
            "error": {"code": -32601, "message": f"Unknown method: {method}"},
        }

    response["id"] = rpc_id
    return jsonify(response)
```

### Letting MCP Clients Call GreenHelix Services Natively

Once your MCP server is running, any MCP client can discover and call your GreenHelix services without modification. Claude, Cursor, or any custom LLM agent connects to your MCP endpoint, calls `tools/list` to discover available tools, and calls `tools/call` with the appropriate arguments. The bridge handles the translation transparently.

The critical advantage is discoverability. MCP clients expect tools to describe themselves via JSON Schema. By wrapping your GreenHelix services as MCP tools, you make them first-class citizens in the MCP ecosystem. An LLM can reason about which tool to use based on the schema description, without any GreenHelix-specific knowledge.

For paid tools, the bridge handles payment automatically. The `x-greenhelix-payment` field in the response tells the caller that a payment intent was created. Sophisticated MCP clients can read this field and present the payment to the user; simpler clients ignore it and the payment settles in the background via the GreenHelix ledger.

---

## Chapter 6: Visa TAP Bridge

### How Visa TAP Works

Visa's Transaction Authorization Protocol extends the existing card network infrastructure to support AI agent transactions. TAP does not create new payment rails. Instead, it adds an agent authorization layer on top of VisaNet, the same network that processes 65,000 transactions per second for human cardholders.

The TAP flow:

1. An agent presents a Visa TAP token -- an EMV tokenized credential linked to a funding source (credit card, debit card, or prepaid account).
2. The receiving agent or merchant sends an authorization request through the standard acquiring bank path, with an `agent_context` object that identifies the transaction as agent-initiated.
3. VisaNet routes the authorization through enhanced 3-D Secure 2 (3DS2) flows that verify agent identity instead of cardholder identity. The agent's TAP certificate replaces the human's biometric or OTP challenge.
4. Upon approval, the merchant receives a standard authorization code. Settlement occurs through the normal card network batch process (T+1 or T+2).

TAP's advantage is instant access to 100+ million merchants already accepting Visa. Any merchant with a Visa terminal or payment gateway can accept TAP payments without modification -- the agent context is transparent to the merchant's existing infrastructure. The disadvantage is card-network interchange fees (1.5-3.5%) that make sub-cent micropayments economically infeasible, and batch settlement latency that conflicts with real-time agent workflows.

### The GreenHelix Visa TAP Adapter

Your bridge translates Visa TAP authorization flows into GreenHelix payment intents and escrow entries, giving you dual-ledger visibility across both the card network and GreenHelix systems.

```python
class VisaTAPBridge:
    """Translates Visa TAP agent payment authorizations into GreenHelix
    payment intents with card-network settlement tracking."""

    def __init__(self, client: GreenHelixClient, agent_id: str,
                 merchant_id: str, acquiring_bank_endpoint: str,
                 tap_certificate_path: str):
        self.client = client
        self.agent_id = agent_id
        self.merchant_id = merchant_id
        self.acquiring_bank_endpoint = acquiring_bank_endpoint
        self.tap_certificate_path = tap_certificate_path

    def create_tap_authorization(self, tap_token: str, amount_usd: float,
                                   payer_agent_id: str,
                                   description: str = "") -> dict:
        """Submit a Visa TAP authorization request and record it in GreenHelix.

        Sends the authorization through the acquiring bank, then creates
        a corresponding GreenHelix payment intent for dual-ledger tracking.
        """
        # Build the TAP authorization request
        auth_request = {
            "token": tap_token,
            "amount": int(amount_usd * 100),  # Cents
            "currency": "USD",
            "merchant_id": self.merchant_id,
            "agent_context": {
                "agent_id": self.agent_id,
                "transaction_type": "agent_initiated",
                "tap_version": "1.0",
                "3ds2_method": "certificate",
            },
            "description": description,
        }

        # Submit to acquiring bank
        auth_response = requests.post(
            f"{self.acquiring_bank_endpoint}/authorize",
            json=auth_request,
            cert=self.tap_certificate_path,
            timeout=15,
        )

        if auth_response.status_code != 200:
            raise ValueError(
                f"TAP authorization failed: {auth_response.text}"
            )

        auth_result = auth_response.json()
        authorization_code = auth_result.get("authorization_code")

        if not authorization_code:
            raise ValueError(
                f"TAP authorization declined: {auth_result.get('decline_reason')}"
            )

        # Record in GreenHelix ledger for dual-ledger auditability
        payment_intent = self.client.execute("create_payment_intent", {
            "payer_agent_id": payer_agent_id,
            "payee_agent_id": self.agent_id,
            "amount": str(amount_usd),
            "description": (
                f"Visa TAP payment. Auth: {authorization_code}. "
                f"{description}"
            ),
            "metadata": json.dumps({
                "protocol": "visa_tap",
                "authorization_code": authorization_code,
                "tap_token_last4": tap_token[-4:],
                "merchant_id": self.merchant_id,
                "settlement_method": "card_network",
                "expected_settlement": "T+1",
            }),
        })

        # Publish tracking event
        self.client.execute("publish_event", {
            "event_type": "tap.authorization.completed",
            "agent_id": self.agent_id,
            "payload": json.dumps({
                "authorization_code": authorization_code,
                "amount": str(amount_usd),
                "payer_agent_id": payer_agent_id,
                "greenhelix_payment_id": payment_intent.get("payment_id"),
            }),
        })

        return {
            "authorization_code": authorization_code,
            "greenhelix_payment_intent": payment_intent,
            "settlement_expected": "T+1",
            "status": "authorized",
        }

    def handle_tap_settlement_webhook(self, settlement_event: dict) -> dict:
        """Process a Visa TAP settlement confirmation webhook.

        Called when the card network batch settlement completes (typically
        T+1). Updates the corresponding GreenHelix payment intent status.
        """
        auth_code = settlement_event.get("authorization_code")
        settled_amount = settlement_event.get("settled_amount_cents", 0) / 100
        net_amount = settlement_event.get("net_amount_cents", 0) / 100
        interchange_fee = settled_amount - net_amount

        self.client.execute("publish_event", {
            "event_type": "tap.settlement.completed",
            "agent_id": self.agent_id,
            "payload": json.dumps({
                "authorization_code": auth_code,
                "settled_amount": str(settled_amount),
                "net_amount": str(net_amount),
                "interchange_fee": str(interchange_fee),
            }),
        })

        return {
            "authorization_code": auth_code,
            "settled": True,
            "net_amount": str(net_amount),
            "interchange_fee": str(interchange_fee),
        }

    def validate_tap_token(self, tap_token: str) -> dict:
        """Validate a Visa TAP token before processing a transaction.

        Checks token format, expiry, and whether the token is on the
        network's revocation list.
        """
        validation_resp = requests.post(
            f"{self.acquiring_bank_endpoint}/validate-token",
            json={"token": tap_token},
            cert=self.tap_certificate_path,
            timeout=10,
        )
        if validation_resp.status_code != 200:
            return {"valid": False, "reason": "Token validation failed"}

        result = validation_resp.json()
        return {
            "valid": result.get("valid", False),
            "token_type": result.get("token_type"),  # credit, debit, prepaid
            "funding_source": result.get("funding_source"),
            "expiry": result.get("expiry"),
        }
```

### Key Design Decisions for Visa TAP

**Interchange fee tracking.** Card network fees are significant for agent commerce -- 1.5-3.5% per transaction. The bridge tracks interchange fees in GreenHelix metadata so you can calculate true net revenue per transaction, not just gross volume. This is critical for pricing optimization when serving both TAP and lower-fee protocols like x402.

**Settlement lag.** Unlike x402 (near-instant on-chain settlement) or GreenHelix escrow (instant within the platform), Visa TAP settles in T+1 or T+2 batches. Your bridge creates the GreenHelix payment intent at authorization time but should not release escrow funds until settlement confirmation arrives via the settlement webhook. This prevents paying out on transactions that are later reversed.

**Minimum transaction size.** At 1.5-3.5% interchange plus a per-transaction fixed fee ($0.10-$0.30), TAP is economically viable only for transactions above approximately $2.00. For micropayments below that threshold, route to x402 or AP2 instead. The PaymentRouter in Chapter 11 handles this automatically.

---

## Chapter 7: Google AP2/UCP Bridge

### How Google AP2 Works

Google's Agent Payments Protocol v2 is built on real-time payment patterns proven by UPI (India's Unified Payments Interface, processing 12+ billion transactions per month) and Pix (Brazil's instant payment system). AP2 supports six payment types: micropayments (sub-cent), standard transactions, subscriptions, escrow, split payments, and batch settlements.

AP2 uses a hub-and-spoke architecture. Google acts as the payment hub. Agents register as spokes with a Google AP2 account. When Agent A wants to pay Agent B, the payment flows through Google's treasury infrastructure: A's balance is debited, B's balance is credited, and settlement occurs in real time (sub-second for pre-funded accounts) or T+1 for bank-linked accounts.

### How Google UCP Works

The Universal Commerce Protocol is Google's service discovery and commercial orchestration layer. Where A2A handles task-level communication between agents, UCP wraps commercial terms around those tasks: service catalogs with pricing, SLA definitions, pricing negotiation flows, multi-step workflow orchestration, and dispute resolution.

A UCP service listing includes:
- **Service manifest**: name, description, capabilities, version
- **Pricing schedule**: per-call, subscription, or tiered pricing with volume discounts
- **SLA terms**: latency guarantees, uptime commitments, error rate bounds
- **A2A endpoint**: the A2A URL for task execution
- **AP2 endpoint**: the AP2 payment address for settlement

UCP and A2A are complementary. A2A handles the "how do agents talk to each other" problem. UCP handles the "under what commercial terms" problem.

### The GreenHelix AP2/UCP Adapter

The bridge handles both AP2 payments and UCP service orchestration, translating between Google's infrastructure and GreenHelix's escrow and marketplace systems.

```python
class AP2UCPBridge:
    """Translates Google AP2 payments and UCP service orchestration into
    GreenHelix payment intents and marketplace listings."""

    def __init__(self, client: GreenHelixClient, agent_id: str,
                 ap2_account_id: str, ap2_api_key: str,
                 ap2_base_url: str = "https://payments.googleapis.com/ap2/v2"):
        self.client = client
        self.agent_id = agent_id
        self.ap2_account_id = ap2_account_id
        self.ap2_api_key = ap2_api_key
        self.ap2_base_url = ap2_base_url
        self._ap2_session = requests.Session()
        self._ap2_session.headers.update({
            "Authorization": f"Bearer {ap2_api_key}",
            "Content-Type": "application/json",
        })

    def receive_ap2_payment(self, ap2_payment_event: dict) -> dict:
        """Process an incoming Google AP2 payment and record it in GreenHelix.

        Called when a Google AP2 agent sends payment to your AP2 account.
        Creates a corresponding GreenHelix payment intent for dual-ledger
        tracking.
        """
        payment_id = ap2_payment_event.get("payment_id")
        amount = ap2_payment_event.get("amount")
        currency = ap2_payment_event.get("currency", "USD")
        payer_ap2_id = ap2_payment_event.get("payer_account_id")
        payment_type = ap2_payment_event.get("payment_type", "standard")

        # Verify the payment with Google's AP2 API
        verify_resp = self._ap2_session.get(
            f"{self.ap2_base_url}/payments/{payment_id}",
            timeout=10,
        )
        if verify_resp.status_code != 200:
            raise ValueError(f"AP2 payment verification failed: {verify_resp.text}")

        verified = verify_resp.json()
        if verified.get("status") != "settled":
            raise ValueError(
                f"AP2 payment not settled: {verified.get('status')}"
            )

        # Record in GreenHelix
        payment_intent = self.client.execute("create_payment_intent", {
            "payer_agent_id": f"ap2:{payer_ap2_id}",
            "payee_agent_id": self.agent_id,
            "amount": str(amount),
            "description": (
                f"Google AP2 {payment_type} payment. "
                f"AP2 ID: {payment_id}"
            ),
            "metadata": json.dumps({
                "protocol": "google_ap2",
                "ap2_payment_id": payment_id,
                "payment_type": payment_type,
                "currency": currency,
                "settlement_method": "google_treasury",
            }),
        })

        return {
            "ap2_payment_id": payment_id,
            "greenhelix_payment_intent": payment_intent,
            "status": "recorded",
        }

    def send_ap2_payment(self, recipient_ap2_id: str, amount_usd: float,
                           description: str = "",
                           payment_type: str = "standard") -> dict:
        """Send a Google AP2 payment from your account and record it in GreenHelix.

        Used when your GreenHelix agent needs to pay a Google AP2 agent.
        """
        payment_resp = self._ap2_session.post(
            f"{self.ap2_base_url}/payments",
            json={
                "payer_account_id": self.ap2_account_id,
                "payee_account_id": recipient_ap2_id,
                "amount": str(amount_usd),
                "currency": "USD",
                "payment_type": payment_type,
                "description": description,
            },
            timeout=15,
        )

        if payment_resp.status_code not in (200, 201):
            raise ValueError(f"AP2 payment failed: {payment_resp.text}")

        ap2_result = payment_resp.json()

        # Record outbound payment in GreenHelix
        self.client.execute("publish_event", {
            "event_type": "ap2.payment.sent",
            "agent_id": self.agent_id,
            "payload": json.dumps({
                "ap2_payment_id": ap2_result.get("payment_id"),
                "recipient": recipient_ap2_id,
                "amount": str(amount_usd),
                "payment_type": payment_type,
            }),
        })

        return ap2_result

    def greenhelix_service_to_ucp_listing(self, service: dict) -> dict:
        """Convert a GreenHelix marketplace service into a UCP service listing.

        UCP listings include pricing schedules, SLA terms, and endpoint
        references for both A2A task execution and AP2 payment.
        """
        return {
            "service_id": service.get("service_id"),
            "name": service.get("name"),
            "description": service.get("description"),
            "version": "1.0.0",
            "pricing": {
                "model": "per_call",
                "amount": service.get("price", "0"),
                "currency": "USD",
                "volume_discounts": [],
            },
            "sla": {
                "max_latency_ms": 5000,
                "uptime_percent": 99.5,
                "max_error_rate_percent": 1.0,
            },
            "endpoints": {
                "a2a": f"https://your-agent.example.com/.well-known/agent.json",
                "ap2_payment": self.ap2_account_id,
                "greenhelix": f"https://api.greenhelix.net/v1",
            },
            "provider": {
                "name": service.get("provider_agent_id", self.agent_id),
                "protocol": "greenhelix",
                "ap2_account": self.ap2_account_id,
            },
            "metadata": {
                "greenhelix_service_id": service.get("service_id"),
                "greenhelix_agent_id": self.agent_id,
            },
        }

    def sync_listings_to_ucp(self) -> list:
        """Pull all services from GreenHelix marketplace and publish as UCP listings."""
        services = self.client.execute("search_services", {
            "provider_agent_id": self.agent_id,
        })
        service_list = services.get("services", [])
        return [
            self.greenhelix_service_to_ucp_listing(s) for s in service_list
        ]

    def handle_ucp_negotiation(self, negotiation_request: dict) -> dict:
        """Handle a UCP pricing negotiation request.

        UCP allows buyer agents to propose alternative terms (lower price,
        different SLA, volume commitment). This method evaluates the
        proposal against your configured policies and responds.
        """
        proposed_price = float(negotiation_request.get("proposed_price", 0))
        service_id = negotiation_request.get("service_id")
        volume_commitment = negotiation_request.get("volume_commitment", 0)

        # Look up current service pricing
        service = self.client.execute("search_services", {
            "service_id": service_id,
            "provider_agent_id": self.agent_id,
        })
        list_price = float(service.get("price", "0"))

        # Simple negotiation logic: accept if within 20% of list price
        # or if volume commitment > 1000 calls
        min_acceptable = list_price * 0.8
        if proposed_price >= min_acceptable or volume_commitment > 1000:
            return {
                "status": "accepted",
                "agreed_price": str(max(proposed_price, min_acceptable)),
                "volume_commitment": volume_commitment,
                "service_id": service_id,
            }
        else:
            return {
                "status": "counter_offer",
                "counter_price": str(min_acceptable),
                "message": (
                    f"Minimum price is {min_acceptable}. "
                    f"Volume discounts available above 1000 calls."
                ),
            }
```

### AP2 vs. x402 for Micropayments

Both AP2 and x402 target sub-cent micropayments, but they differ in settlement architecture. x402 settles on-chain (or via Stripe in v2), giving you verifiable payment proofs but requiring facilitator infrastructure. AP2 settles through Google's treasury, giving you real-time balance updates but requiring a Google AP2 account and trusting Google as the settlement counterparty.

For GreenHelix agents, the practical decision comes down to your counterparty's ecosystem. If they are in the Google ecosystem (using A2A for task orchestration), AP2 is the natural payment complement. If they are using x402-native infrastructure (Coinbase, Cloudflare), x402 is simpler. The PaymentRouter in Chapter 11 automates this selection.

---

## Chapter 8: PayPal Agent Ready Bridge

### How PayPal Agent Ready Works

PayPal Agent Ready extends PayPal's existing infrastructure for AI agent transactions. It has two components:

**Fastlane Authentication.** Agents authenticate using Fastlane tokens -- one-tap authentication credentials that link an agent to a consumer's PayPal account. The consumer pre-authorizes the agent during a one-time setup, and subsequent transactions require only the Fastlane token. This is PayPal's answer to the "agent authorization" problem: how does a consumer grant spending authority to an AI agent without sharing credentials?

**Braintree Agent API.** Transactions are processed through Braintree's GraphQL API with a new `agent_context` parameter. The parameter includes the agent's identity, the authorization scope (spending limits, merchant restrictions), and the consumer's Fastlane token. Braintree routes the transaction through PayPal's standard payment processing, with the agent context logged for compliance and dispute resolution.

Agent Ready targets PayPal's 400+ million consumer accounts and 35+ million merchant accounts. An agent authenticated through Agent Ready can access the consumer's PayPal wallet, Venmo balance, or linked bank accounts. Settlement is through PayPal's standard disbursement: instant to PayPal balance, T+1 to bank accounts.

### The GreenHelix PayPal Agent Ready Adapter

```python
class PayPalAgentReadyBridge:
    """Translates PayPal Agent Ready transactions into GreenHelix payment
    intents with Braintree settlement tracking."""

    def __init__(self, client: GreenHelixClient, agent_id: str,
                 braintree_merchant_id: str, braintree_api_key: str,
                 braintree_api_secret: str,
                 braintree_environment: str = "production"):
        self.client = client
        self.agent_id = agent_id
        self.braintree_merchant_id = braintree_merchant_id
        self.braintree_api_key = braintree_api_key
        self.braintree_api_secret = braintree_api_secret
        self.braintree_environment = braintree_environment
        self._bt_base_url = (
            "https://payments.braintree-api.com/graphql"
            if braintree_environment == "production"
            else "https://payments.sandbox.braintree-api.com/graphql"
        )

    def process_agent_ready_payment(self, fastlane_token: str,
                                       amount_usd: float,
                                       payer_agent_id: str,
                                       description: str = "") -> dict:
        """Process a PayPal Agent Ready payment and record it in GreenHelix.

        Charges the consumer's PayPal account via the Fastlane token
        and creates a corresponding GreenHelix payment intent.
        """
        # Execute Braintree GraphQL mutation with agent context
        mutation = """
        mutation ChargePayPalAccount($input: ChargePayPalAccountInput!) {
            chargePayPalAccount(input: $input) {
                transaction {
                    id
                    status
                    amount { value currencyCode }
                    paypal { payerId payerEmail }
                }
            }
        }
        """
        variables = {
            "input": {
                "paymentMethodId": fastlane_token,
                "transaction": {
                    "amount": str(amount_usd),
                    "agentContext": {
                        "agentId": self.agent_id,
                        "transactionType": "AGENT_INITIATED",
                        "authorizationScope": "PRE_AUTHORIZED",
                    },
                    "description": description,
                },
            },
        }

        bt_response = requests.post(
            self._bt_base_url,
            json={"query": mutation, "variables": variables},
            auth=(self.braintree_api_key, self.braintree_api_secret),
            timeout=15,
        )

        if bt_response.status_code != 200:
            raise ValueError(
                f"Braintree request failed: {bt_response.text}"
            )

        result = bt_response.json()
        tx_data = (
            result.get("data", {})
            .get("chargePayPalAccount", {})
            .get("transaction", {})
        )

        if not tx_data or tx_data.get("status") != "SETTLING":
            raise ValueError(
                f"PayPal transaction failed: {json.dumps(result.get('errors', []))}"
            )

        braintree_tx_id = tx_data["id"]

        # Record in GreenHelix ledger
        payment_intent = self.client.execute("create_payment_intent", {
            "payer_agent_id": payer_agent_id,
            "payee_agent_id": self.agent_id,
            "amount": str(amount_usd),
            "description": (
                f"PayPal Agent Ready payment. "
                f"Braintree TX: {braintree_tx_id}. {description}"
            ),
            "metadata": json.dumps({
                "protocol": "paypal_agent_ready",
                "braintree_tx_id": braintree_tx_id,
                "paypal_payer_id": tx_data.get("paypal", {}).get("payerId"),
                "settlement_method": "paypal",
            }),
        })

        self.client.execute("publish_event", {
            "event_type": "paypal.payment.completed",
            "agent_id": self.agent_id,
            "payload": json.dumps({
                "braintree_tx_id": braintree_tx_id,
                "amount": str(amount_usd),
                "payer_agent_id": payer_agent_id,
                "greenhelix_payment_id": payment_intent.get("payment_id"),
            }),
        })

        return {
            "braintree_tx_id": braintree_tx_id,
            "greenhelix_payment_intent": payment_intent,
            "status": "settling",
        }

    def validate_fastlane_token(self, fastlane_token: str) -> dict:
        """Validate a Fastlane token before processing a transaction.

        Checks token validity, authorization scope, and spending limits.
        """
        query = """
        query ValidatePaymentMethod($id: ID!) {
            node(id: $id) {
                ... on PayPalAccount {
                    payerId
                    email
                    agentAuthorization {
                        scope
                        spendingLimit { value currencyCode }
                        expiresAt
                    }
                }
            }
        }
        """
        resp = requests.post(
            self._bt_base_url,
            json={"query": query, "variables": {"id": fastlane_token}},
            auth=(self.braintree_api_key, self.braintree_api_secret),
            timeout=10,
        )

        if resp.status_code != 200:
            return {"valid": False, "reason": "Validation request failed"}

        data = resp.json().get("data", {}).get("node", {})
        auth = data.get("agentAuthorization", {})

        return {
            "valid": bool(data.get("payerId")),
            "payer_id": data.get("payerId"),
            "email": data.get("email"),
            "scope": auth.get("scope"),
            "spending_limit": auth.get("spendingLimit", {}).get("value"),
            "expires_at": auth.get("expiresAt"),
        }

    def greenhelix_service_to_agent_ready_listing(self, service: dict) -> dict:
        """Convert a GreenHelix marketplace service into a PayPal Agent Ready
        merchant listing format."""
        return {
            "merchant_id": self.braintree_merchant_id,
            "service_id": service.get("service_id"),
            "name": service.get("name"),
            "description": service.get("description"),
            "price": {
                "value": service.get("price", "0"),
                "currency_code": "USD",
            },
            "agent_ready": {
                "supports_fastlane": True,
                "supports_venmo": True,
                "agent_initiated": True,
            },
            "metadata": {
                "greenhelix_service_id": service.get("service_id"),
                "greenhelix_agent_id": self.agent_id,
            },
        }
```

### PayPal Agent Ready vs. ACP (Stripe)

Both Agent Ready and ACP solve the "agent buys from merchant" problem, but they target different merchant bases. ACP routes through Stripe; Agent Ready routes through Braintree/PayPal. In practice, many merchants accept both, so the choice comes down to which payment method the consumer (or consuming agent) has authorized. If the consumer's agent has a Fastlane token, use Agent Ready. If the agent has a Stripe payment method, use ACP. The PaymentRouter in Chapter 11 selects the optimal path based on available credentials.

---

## Chapter 9: OpenAI ACP Bridge

### How OpenAI ACP Works

OpenAI's Agentic Commerce Protocol defines a commerce graph for AI agent services. Unlike the earlier ACP (Stripe-based checkout, covered in Chapter 3), OpenAI ACP is a full-stack commerce framework with five layers:

1. **Service Manifests.** Agents publish structured manifests describing their capabilities, pricing tiers, SLAs, accepted payment methods, and terms of service. Manifests are registered in OpenAI's centralized service registry and discoverable through both API queries and ChatGPT's agent plugin marketplace.

2. **Discovery and Matching.** Buyer agents query the registry to find services matching their requirements. The registry supports semantic search, capability filtering, price comparison, and SLA matching. Results are ranked by a combination of relevance, provider reputation, and pricing.

3. **Term Negotiation.** Before executing a transaction, buyer and seller agents can negotiate terms programmatically. The negotiation protocol supports price proposals, counter-offers, volume commitments, and custom SLA modifications. Non-negotiable listings skip this step.

4. **Transaction Execution.** Payments flow through a pluggable payment adapter layer. OpenAI ACP supports Stripe, x402, and direct bank transfers as payment backends. The protocol creates a transaction record that links the service manifest, negotiated terms, payment confirmation, and fulfillment result.

5. **Dispute Resolution.** OpenAI ACP includes built-in dispute flows. If the buyer claims non-delivery or quality issues, the dispute is escalated through OpenAI's resolution process, which can issue refunds, adjust provider reputation scores, or suspend service listings.

### The GreenHelix OpenAI ACP Adapter

The bridge exposes GreenHelix services as OpenAI ACP service manifests and translates incoming ACP transactions into GreenHelix payment intents with full escrow backing.

```python
class OpenAIACPBridge:
    """Translates OpenAI ACP service manifests and transactions into
    GreenHelix marketplace listings and escrow-backed payment intents."""

    def __init__(self, client: GreenHelixClient, agent_id: str,
                 openai_acp_api_key: str,
                 openai_acp_base_url: str = "https://api.openai.com/v1/acp"):
        self.client = client
        self.agent_id = agent_id
        self.openai_acp_api_key = openai_acp_api_key
        self.openai_acp_base_url = openai_acp_base_url
        self._acp_session = requests.Session()
        self._acp_session.headers.update({
            "Authorization": f"Bearer {openai_acp_api_key}",
            "Content-Type": "application/json",
        })

    def greenhelix_service_to_acp_manifest(self, service: dict) -> dict:
        """Convert a GreenHelix marketplace service into an OpenAI ACP
        service manifest for registration in the ACP service registry."""
        return {
            "manifest_version": "1.0",
            "service_id": service.get("service_id"),
            "name": service.get("name"),
            "description": service.get("description"),
            "provider": {
                "id": self.agent_id,
                "name": service.get("provider_agent_id", self.agent_id),
                "protocol": "greenhelix",
            },
            "pricing": {
                "tiers": [
                    {
                        "name": "standard",
                        "price_per_call": service.get("price", "0"),
                        "currency": "USD",
                        "rate_limit": 1000,  # calls per hour
                    },
                ],
                "negotiable": True,
            },
            "sla": {
                "max_latency_ms": 5000,
                "uptime_percent": 99.5,
                "support_channel": "webhook",
            },
            "accepted_payment_methods": [
                "stripe", "x402", "greenhelix_escrow",
            ],
            "capabilities": service.get("tags", []),
            "fulfillment": {
                "type": "real_time",
                "endpoint": f"https://api.greenhelix.net/v1",
                "protocol": "greenhelix_execute",
            },
            "metadata": {
                "greenhelix_service_id": service.get("service_id"),
                "greenhelix_agent_id": self.agent_id,
            },
        }

    def register_manifests_in_acp(self) -> list:
        """Register all GreenHelix services as OpenAI ACP service manifests."""
        services = self.client.execute("search_services", {
            "provider_agent_id": self.agent_id,
        })
        service_list = services.get("services", [])

        registered = []
        for svc in service_list:
            manifest = self.greenhelix_service_to_acp_manifest(svc)
            resp = self._acp_session.post(
                f"{self.openai_acp_base_url}/manifests",
                json=manifest,
                timeout=10,
            )
            if resp.status_code in (200, 201):
                registered.append({
                    "service_id": svc.get("service_id"),
                    "acp_manifest_id": resp.json().get("manifest_id"),
                    "status": "registered",
                })
            else:
                registered.append({
                    "service_id": svc.get("service_id"),
                    "status": "failed",
                    "error": resp.text,
                })

        return registered

    def handle_acp_transaction(self, acp_transaction: dict) -> dict:
        """Process an incoming OpenAI ACP transaction request.

        Creates a GreenHelix escrow for the transaction amount, executes
        the requested service, and returns the fulfillment result in ACP
        format. The escrow ensures the buyer's payment is held until
        fulfillment is confirmed.
        """
        manifest_id = acp_transaction.get("manifest_id")
        service_id = acp_transaction.get("service_id")
        buyer_id = acp_transaction.get("buyer", {}).get("id", "acp-buyer")
        amount = acp_transaction.get("agreed_price",
                                       acp_transaction.get("list_price", "0"))
        payment_method = acp_transaction.get("payment_method", "stripe")
        transaction_id = acp_transaction.get("transaction_id")

        # Create GreenHelix escrow for buyer protection
        escrow = self.client.execute("create_escrow", {
            "payer_agent_id": f"openai-acp:{buyer_id}",
            "payee_agent_id": self.agent_id,
            "amount": str(amount),
            "description": (
                f"OpenAI ACP transaction {transaction_id}. "
                f"Service: {service_id}. Manifest: {manifest_id}"
            ),
            "escrow_type": "standard",
            "metadata": json.dumps({
                "protocol": "openai_acp",
                "acp_transaction_id": transaction_id,
                "acp_manifest_id": manifest_id,
                "payment_method": payment_method,
            }),
        })

        # Publish tracking event
        self.client.execute("publish_event", {
            "event_type": "openai_acp.transaction.received",
            "agent_id": self.agent_id,
            "payload": json.dumps({
                "transaction_id": transaction_id,
                "service_id": service_id,
                "buyer_id": buyer_id,
                "amount": str(amount),
                "escrow_id": escrow.get("escrow_id"),
            }),
        })

        return {
            "transaction_id": transaction_id,
            "escrow_id": escrow.get("escrow_id"),
            "status": "accepted",
            "fulfillment_status": "pending",
        }

    def complete_acp_fulfillment(self, transaction_id: str,
                                    escrow_id: str,
                                    result: dict) -> dict:
        """Complete an OpenAI ACP transaction after service fulfillment.

        Releases the escrow and sends the fulfillment result back to the
        ACP registry for buyer confirmation.
        """
        # Notify ACP registry of fulfillment
        fulfill_resp = self._acp_session.post(
            f"{self.openai_acp_base_url}/transactions/{transaction_id}/fulfill",
            json={
                "status": "fulfilled",
                "result": result,
                "provider_id": self.agent_id,
            },
            timeout=10,
        )

        # Publish completion event
        self.client.execute("publish_event", {
            "event_type": "openai_acp.transaction.fulfilled",
            "agent_id": self.agent_id,
            "payload": json.dumps({
                "transaction_id": transaction_id,
                "escrow_id": escrow_id,
                "fulfillment_status": "completed",
            }),
        })

        return {
            "transaction_id": transaction_id,
            "escrow_id": escrow_id,
            "status": "fulfilled",
            "acp_confirmation": fulfill_resp.json() if fulfill_resp.ok else None,
        }

    def handle_acp_negotiation(self, negotiation_request: dict) -> dict:
        """Handle an OpenAI ACP term negotiation request.

        Evaluates the buyer's proposed terms against the service manifest
        and responds with acceptance, rejection, or counter-offer.
        """
        service_id = negotiation_request.get("service_id")
        proposed_price = float(negotiation_request.get("proposed_price", 0))
        proposed_volume = negotiation_request.get("volume_commitment", 0)

        # Look up current service pricing
        service = self.client.execute("search_services", {
            "service_id": service_id,
            "provider_agent_id": self.agent_id,
        })
        list_price = float(service.get("price", "0"))

        # Negotiation policy: accept >= 80% of list price, or
        # >= 60% with volume commitment > 5000
        min_price = list_price * 0.8
        volume_min_price = list_price * 0.6

        if proposed_price >= min_price:
            return {
                "status": "accepted",
                "agreed_price": str(proposed_price),
                "volume_commitment": proposed_volume,
            }
        elif proposed_price >= volume_min_price and proposed_volume > 5000:
            return {
                "status": "accepted",
                "agreed_price": str(proposed_price),
                "volume_commitment": proposed_volume,
                "note": "Volume discount applied",
            }
        else:
            return {
                "status": "counter_offer",
                "counter_price": str(min_price),
                "message": (
                    f"Minimum price: {min_price}. Volume discount "
                    f"(60% of list) available for 5000+ call commitments."
                ),
            }
```

### OpenAI ACP vs. ACP (Stripe) vs. UCP

Three protocols now handle the "agent commerce" problem. ACP (Chapter 3) is Stripe-native checkout for the ChatGPT distribution channel. OpenAI ACP is a broader commerce framework with multi-backend payment support and built-in dispute resolution. UCP (Chapter 7) is Google's answer with SLA negotiation and A2A integration.

The key differences for bridge builders:

- **ACP (Stripe)**: Simplest integration. Stripe-only payments. Best for merchants already on Stripe.
- **OpenAI ACP**: Richest feature set. Multi-payment-backend. Built-in disputes. Best for agents selling through the OpenAI ecosystem.
- **UCP**: Tightest integration with A2A task orchestration and AP2 payments. Best for agents in the Google ecosystem.

Your GreenHelix bridge supports all three simultaneously. The IdentityMapper (Chapter 10) links your agent's identity across all three registries, and the PaymentRouter (Chapter 11) selects the optimal payment path for each transaction.

---

## Chapter 10: Cross-Protocol Identity

### The Identity Mapping Problem

Your GreenHelix agent is `my-summarizer-agent` with Ed25519 public key `MCowBQYDK2Vw...`. In x402, it is identified by its USDC payment address `0xAb5801a7...`. In ACP, it is a Stripe account `acct_1234567890`. In A2A, it is discoverable at `https://your-agent.example.com/.well-known/agent.json`. In MCP, it is the server at `https://your-agent.example.com/mcp`. In Visa TAP, it is a merchant ID with a TAP certificate. In Google AP2, it is an AP2 account ID. In UCP, it is a service provider in Google's commerce registry. In PayPal Agent Ready, it is a Braintree merchant ID. In OpenAI ACP, it is a provider ID in OpenAI's service registry.

One agent. Ten identities. Zero automatic cross-referencing.

When an A2A agent calls your service and then later initiates an x402 payment, how do you know it is the same entity? When an MCP client calls your tool and you want to check its trust score in GreenHelix, how do you resolve the MCP client identity to a GreenHelix agent ID? When a Visa TAP authorization arrives, how do you link it to the OpenAI ACP transaction that triggered it? Without an identity mapping layer, every protocol interaction is a stranger transaction with no reputation context.

### Building the Identity Registry

The `IdentityMapper` maintains bidirectional mappings between GreenHelix agent IDs and external protocol identities. It stores mappings in GreenHelix's own identity system via metadata fields, making the registry auditable and persistent.

```python
class IdentityMapper:
    """Maps agent identities across GreenHelix and all nine external protocols."""

    SUPPORTED_PROTOCOLS = {
        "x402", "acp", "a2a", "mcp", "tap",
        "visa_tap", "ap2", "ucp", "paypal_agent_ready", "openai_acp",
    }

    def __init__(self, client: GreenHelixClient):
        self.client = client
        # In-memory cache; production should use persistent storage
        self._mappings = {}  # {greenhelix_id: {protocol: external_id}}
        self._reverse = {}   # {(protocol, external_id): greenhelix_id}

    def register_mapping(self, greenhelix_agent_id: str, protocol: str,
                          external_id: str, metadata: dict = None) -> dict:
        """Register an identity mapping between GreenHelix and an external protocol.

        Also verifies that the GreenHelix agent exists before creating
        the mapping.
        """
        if protocol not in self.SUPPORTED_PROTOCOLS:
            raise ValueError(
                f"Unsupported protocol: {protocol}. "
                f"Supported: {self.SUPPORTED_PROTOCOLS}"
            )

        # Verify the GreenHelix agent exists
        identity = self.client.execute("verify_agent", {
            "agent_id": greenhelix_agent_id,
        })
        if not identity.get("verified"):
            raise ValueError(
                f"Agent {greenhelix_agent_id} not found or not verified"
            )

        # Store the mapping
        if greenhelix_agent_id not in self._mappings:
            self._mappings[greenhelix_agent_id] = {}
        self._mappings[greenhelix_agent_id][protocol] = {
            "external_id": external_id,
            "metadata": metadata or {},
            "registered_at": time.time(),
        }

        # Reverse index
        self._reverse[(protocol, external_id)] = greenhelix_agent_id

        # Persist the mapping in GreenHelix event bus for auditability
        self.client.execute("publish_event", {
            "event_type": "identity.mapping.created",
            "agent_id": greenhelix_agent_id,
            "payload": json.dumps({
                "protocol": protocol,
                "external_id": external_id,
                "metadata": metadata,
            }),
        })

        return {
            "greenhelix_agent_id": greenhelix_agent_id,
            "protocol": protocol,
            "external_id": external_id,
            "status": "registered",
        }

    def resolve_identity(self, protocol: str, external_id: str) -> dict:
        """Resolve an external protocol identity to a GreenHelix agent.

        Returns the GreenHelix agent ID and identity details, or None if
        no mapping exists.
        """
        greenhelix_id = self._reverse.get((protocol, external_id))
        if not greenhelix_id:
            return None

        # Fetch current GreenHelix identity
        identity = self.client.execute("get_agent_identity", {
            "agent_id": greenhelix_id,
        })

        mapping_data = self._mappings.get(greenhelix_id, {}).get(protocol, {})

        return {
            "greenhelix_agent_id": greenhelix_id,
            "greenhelix_identity": identity,
            "protocol": protocol,
            "external_id": external_id,
            "mapping_metadata": mapping_data.get("metadata", {}),
        }

    def get_all_identities(self, greenhelix_agent_id: str) -> dict:
        """Get all protocol identities for a GreenHelix agent.

        Returns a dict mapping protocol names to external identity details.
        """
        return {
            "greenhelix_agent_id": greenhelix_agent_id,
            "protocols": self._mappings.get(greenhelix_agent_id, {}),
        }

    def verify_cross_protocol(self, greenhelix_agent_id: str,
                                protocol: str, claimed_id: str) -> dict:
        """Verify that a claimed external identity matches the registered mapping.

        Used when an external agent claims to be a specific GreenHelix agent.
        Returns verification result with the trust score from GreenHelix.
        """
        mapping = self._mappings.get(greenhelix_agent_id, {}).get(protocol)

        if not mapping:
            return {
                "verified": False,
                "reason": f"No {protocol} mapping for {greenhelix_agent_id}",
            }

        if mapping["external_id"] != claimed_id:
            return {
                "verified": False,
                "reason": "Claimed identity does not match registered mapping",
            }

        # Fetch trust score for additional context
        identity = self.client.execute("get_agent_identity", {
            "agent_id": greenhelix_agent_id,
        })

        return {
            "verified": True,
            "greenhelix_agent_id": greenhelix_agent_id,
            "trust_score": identity.get("trust_score"),
            "protocol": protocol,
            "external_id": claimed_id,
        }
```

### Cryptographic Identity Verification Across Protocols

The `verify_cross_protocol` method handles the soft case: checking that a claimed identity matches a registered mapping. For high-value transactions, you need cryptographic verification -- proving that the entity controlling the external identity is the same entity that controls the GreenHelix Ed25519 key.

The pattern is a challenge-response:

1. Your bridge generates a random nonce.
2. The external agent signs the nonce with its protocol-specific key (e.g., the Ethereum key for x402, the Ed25519 key for GreenHelix).
3. Your bridge verifies both signatures and confirms they correspond to the mapped identities.

```python
import secrets


def create_identity_challenge(self, greenhelix_agent_id: str,
                               protocol: str) -> dict:
    """Generate a challenge for cross-protocol identity verification."""
    nonce = secrets.token_hex(32)

    self.client.execute("publish_event", {
        "event_type": "identity.challenge.created",
        "agent_id": greenhelix_agent_id,
        "payload": json.dumps({
            "protocol": protocol,
            "nonce": nonce,
            "expires_at": time.time() + 300,
        }),
    })

    return {
        "nonce": nonce,
        "message": f"Sign this nonce with both your {protocol} key and GreenHelix key: {nonce}",
        "expires_at": time.time() + 300,
    }
```

This dual-signature verification ensures that cross-protocol identity claims are cryptographically bound, not just database lookups. For most use cases the soft verification is sufficient. For high-value escrow bridging or cross-protocol dispute resolution, require the challenge-response.

---

## Chapter 11: Cross-Protocol Payment Routing

### The Routing Problem

With nine protocols, your agent now has six distinct payment paths: x402 v2 (crypto or fiat micropayments), ACP (Stripe checkout), Visa TAP (card network), Google AP2 (Google treasury), PayPal Agent Ready (PayPal/Braintree), and OpenAI ACP (multi-backend). Each path has different fee structures, settlement latency, minimum viable transaction sizes, and geographic reach. Choosing the wrong path costs money -- a $0.01 micropayment through Visa TAP incurs $0.10+ in interchange fees, turning a profitable transaction into a loss.

The `PaymentRouter` selects the optimal payment path for each transaction based on amount, counterparty capabilities, fee structure, and settlement speed requirements.

### Building the Payment Router

```python
class PaymentRouter:
    """Selects the optimal payment protocol for cross-protocol transactions.

    Routes payments through the lowest-cost path that satisfies the
    transaction's settlement speed and counterparty requirements.
    """

    # Fee structures by protocol (approximate, as of April 2026)
    PROTOCOL_FEES = {
        "x402": {
            "fixed_fee": 0.00,
            "percent_fee": 0.1,   # 0.1% for crypto, ~1% for fiat
            "min_viable_amount": 0.001,
            "settlement_speed": "near_instant",  # seconds for crypto
        },
        "acp": {
            "fixed_fee": 0.30,
            "percent_fee": 2.9,   # Standard Stripe pricing
            "min_viable_amount": 0.50,
            "settlement_speed": "t_plus_2",
        },
        "visa_tap": {
            "fixed_fee": 0.10,
            "percent_fee": 2.5,   # Average interchange
            "min_viable_amount": 2.00,
            "settlement_speed": "t_plus_1",
        },
        "ap2": {
            "fixed_fee": 0.00,
            "percent_fee": 0.05,  # Google subsidized rate
            "min_viable_amount": 0.001,
            "settlement_speed": "near_instant",  # pre-funded accounts
        },
        "paypal_agent_ready": {
            "fixed_fee": 0.30,
            "percent_fee": 2.99,
            "min_viable_amount": 1.00,
            "settlement_speed": "instant_to_balance",
        },
        "openai_acp": {
            "fixed_fee": 0.00,
            "percent_fee": 1.5,   # OpenAI platform fee
            "min_viable_amount": 0.10,
            "settlement_speed": "near_instant",
        },
    }

    def __init__(self, identity_mapper: IdentityMapper,
                 available_bridges: dict):
        """Initialize with identity mapper and a dict of protocol -> bridge instance."""
        self.identity_mapper = identity_mapper
        self.available_bridges = available_bridges

    def calculate_fee(self, protocol: str, amount: float) -> float:
        """Calculate the total fee for a given protocol and amount."""
        fee_config = self.PROTOCOL_FEES.get(protocol, {})
        fixed = fee_config.get("fixed_fee", 0)
        percent = fee_config.get("percent_fee", 0)
        return fixed + (amount * percent / 100)

    def route_payment(self, amount: float,
                       payer_protocols: list,
                       payee_protocols: list,
                       prefer_speed: bool = False,
                       max_fee_percent: float = None) -> dict:
        """Select the optimal payment protocol for a transaction.

        Args:
            amount: Transaction amount in USD.
            payer_protocols: Protocols the payer supports (e.g., ["x402", "ap2"]).
            payee_protocols: Protocols the payee supports (e.g., ["visa_tap", "acp"]).
            prefer_speed: If True, prioritize settlement speed over fees.
            max_fee_percent: Maximum acceptable fee as percentage of amount.

        Returns:
            Dict with the selected protocol, estimated fee, and routing rationale.
        """
        # Find protocols supported by both parties
        common_protocols = set(payer_protocols) & set(payee_protocols)
        # Also include protocols where we can bridge (payer -> GreenHelix -> payee)
        bridgeable = set(self.available_bridges.keys())
        candidates = common_protocols | (set(payer_protocols) & bridgeable)

        if not candidates:
            return {
                "protocol": "greenhelix",
                "fee": 0,
                "rationale": "No common protocol; falling back to GreenHelix native",
            }

        # Score each candidate
        scored = []
        for protocol in candidates:
            fee_config = self.PROTOCOL_FEES.get(protocol)
            if not fee_config:
                continue

            min_viable = fee_config.get("min_viable_amount", 0)
            if amount < min_viable:
                continue  # Transaction too small for this protocol

            fee = self.calculate_fee(protocol, amount)
            fee_percent = (fee / amount * 100) if amount > 0 else 0

            if max_fee_percent is not None and fee_percent > max_fee_percent:
                continue  # Fee exceeds maximum

            speed_score = {
                "near_instant": 0,
                "instant_to_balance": 1,
                "t_plus_1": 2,
                "t_plus_2": 3,
            }.get(fee_config.get("settlement_speed", "t_plus_2"), 4)

            # Combined score: lower is better
            if prefer_speed:
                score = speed_score * 100 + fee
            else:
                score = fee * 100 + speed_score

            scored.append({
                "protocol": protocol,
                "fee": round(fee, 4),
                "fee_percent": round(fee_percent, 2),
                "settlement_speed": fee_config.get("settlement_speed"),
                "score": score,
            })

        if not scored:
            return {
                "protocol": "greenhelix",
                "fee": 0,
                "rationale": "No viable protocol for this amount/fee combination",
            }

        # Select the best (lowest score)
        scored.sort(key=lambda x: x["score"])
        best = scored[0]

        return {
            "protocol": best["protocol"],
            "fee": best["fee"],
            "fee_percent": best["fee_percent"],
            "settlement_speed": best["settlement_speed"],
            "alternatives": scored[1:3],  # Next 2 best options
            "rationale": (
                f"Selected {best['protocol']} for ${amount:.2f}: "
                f"fee ${best['fee']:.4f} ({best['fee_percent']}%), "
                f"settlement {best['settlement_speed']}"
            ),
        }

    def execute_routed_payment(self, amount: float,
                                 payer_agent_id: str,
                                 payee_agent_id: str,
                                 payer_protocols: list,
                                 payee_protocols: list,
                                 description: str = "",
                                 prefer_speed: bool = False) -> dict:
        """Route and execute a payment through the optimal protocol.

        Selects the best protocol, then delegates to the appropriate
        bridge class for execution.
        """
        route = self.route_payment(
            amount=amount,
            payer_protocols=payer_protocols,
            payee_protocols=payee_protocols,
            prefer_speed=prefer_speed,
        )

        protocol = route["protocol"]
        bridge = self.available_bridges.get(protocol)

        if not bridge:
            # Fall back to GreenHelix native payment
            return {
                "route": route,
                "execution": "greenhelix_native",
                "message": f"No bridge for {protocol}; use GreenHelix native",
            }

        return {
            "route": route,
            "protocol": protocol,
            "bridge": type(bridge).__name__,
            "status": "ready_to_execute",
            "description": description,
        }
```

### Routing Decision Matrix

The router follows this priority order for common scenarios:

| Transaction Amount | Best Protocol | Rationale |
|---|---|---|
| $0.001 - $0.10 | x402 v2 or AP2 | Sub-cent viable, near-zero fees |
| $0.10 - $2.00 | AP2 or OpenAI ACP | Low fixed fees, below card network minimums |
| $2.00 - $50.00 | Any (fee-optimized) | Router selects by counterparty and fee |
| $50.00+ | ACP, Visa TAP, or PayPal | Established rails, buyer protection |

**Speed-critical transactions** (e.g., real-time API gating) route to x402 v2 (crypto) or AP2, both of which settle in seconds for pre-funded accounts. **Cost-critical bulk transactions** route to AP2 or x402 v2 fiat, which have the lowest marginal fees. **Enterprise transactions** with compliance requirements route to Visa TAP or ACP, which provide card-network-grade audit trails.

The router's fee table should be updated quarterly as protocols adjust pricing. Google has been subsidizing AP2 fees to drive adoption; expect rates to increase as the subsidy period ends.

---

## Chapter 12: Cross-Protocol Event Bridge

### The Event Translation Problem

Each protocol has its own event model. GreenHelix publishes events via `publish_event` and delivers them through webhooks registered with `register_webhook`. A2A v2 streams task updates via Server-Sent Events and push notifications. ACP sends Stripe webhook events. x402 relies on on-chain transaction confirmations. MCP 1.5 supports notifications via Streamable HTTP. Visa TAP sends settlement webhooks through the card network. AP2 delivers real-time payment events. PayPal Agent Ready uses Braintree webhooks. OpenAI ACP publishes transaction lifecycle events through its API.

When a cross-protocol transaction completes, multiple systems need notification. If an A2A agent pays via x402 for a GreenHelix service exposed through MCP, four event systems are involved. If a Visa TAP authorization triggers an OpenAI ACP fulfillment tracked in GreenHelix, three more event systems join the mix. Without a unified event bridge, you are writing custom notification code for every protocol combination -- and with nine protocols, that is 72 possible pairwise translations.

### Building the Event Bridge

The `EventBridge` normalizes events from all protocols into a common format, translates them to each protocol's native event schema, and forwards them to the appropriate destinations.

```python
class EventBridge:
    """Translates events between GreenHelix and external protocol event systems."""

    def __init__(self, client: GreenHelixClient, agent_id: str,
                 identity_mapper: IdentityMapper):
        self.client = client
        self.agent_id = agent_id
        self.identity_mapper = identity_mapper
        self._webhook_registry = {}  # {protocol: [webhook_urls]}

    def register_external_webhook(self, protocol: str, url: str,
                                    events: list) -> dict:
        """Register a webhook for forwarding events to an external protocol.

        Events matching the specified types will be translated and forwarded
        to this URL.
        """
        if protocol not in self._webhook_registry:
            self._webhook_registry[protocol] = []

        registration = {
            "url": url,
            "events": events,
            "protocol": protocol,
            "registered_at": time.time(),
        }
        self._webhook_registry[protocol].append(registration)

        # Also register in GreenHelix for persistence
        self.client.execute("register_webhook", {
            "agent_id": self.agent_id,
            "url": url,
            "events": json.dumps(events),
        })

        return {
            "status": "registered",
            "protocol": protocol,
            "url": url,
            "events": events,
        }

    def translate_event(self, source_protocol: str, event: dict,
                         target_protocol: str) -> dict:
        """Translate an event from one protocol's schema to another.

        Handles the mapping between protocol-specific event types and
        payload formats.
        """
        # Normalize to a common intermediate format
        normalized = self._normalize_event(source_protocol, event)

        # Translate to the target protocol format
        return self._denormalize_event(target_protocol, normalized)

    def _normalize_event(self, protocol: str, event: dict) -> dict:
        """Convert a protocol-specific event to the common format."""
        if protocol == "greenhelix":
            return {
                "type": event.get("event_type"),
                "agent_id": event.get("agent_id"),
                "timestamp": event.get("timestamp", time.time()),
                "payload": event.get("payload", {}),
                "source_protocol": "greenhelix",
            }
        elif protocol == "a2a":
            return {
                "type": f"a2a.{event.get('status', {}).get('state', 'unknown')}",
                "agent_id": event.get("agent_id"),
                "timestamp": time.time(),
                "payload": {
                    "task_id": event.get("id"),
                    "messages": event.get("messages", []),
                },
                "source_protocol": "a2a",
            }
        elif protocol == "acp":
            return {
                "type": f"acp.{event.get('type', 'unknown')}",
                "agent_id": event.get("merchant_id"),
                "timestamp": event.get("created", time.time()),
                "payload": event.get("data", {}),
                "source_protocol": "acp",
            }
        elif protocol == "x402":
            return {
                "type": "x402.payment.settled",
                "agent_id": event.get("payee_address"),
                "timestamp": event.get("block_timestamp", time.time()),
                "payload": {
                    "tx_hash": event.get("tx_hash"),
                    "amount": event.get("amount"),
                    "currency": event.get("currency", "USD"),
                },
                "source_protocol": "x402",
            }
        elif protocol == "visa_tap":
            return {
                "type": f"visa_tap.{event.get('event_type', 'authorization')}",
                "agent_id": event.get("merchant_id"),
                "timestamp": event.get("timestamp", time.time()),
                "payload": {
                    "authorization_code": event.get("authorization_code"),
                    "amount": event.get("amount"),
                    "status": event.get("status"),
                },
                "source_protocol": "visa_tap",
            }
        elif protocol == "ap2":
            return {
                "type": f"ap2.{event.get('event_type', 'payment')}",
                "agent_id": event.get("payee_account_id"),
                "timestamp": event.get("timestamp", time.time()),
                "payload": {
                    "payment_id": event.get("payment_id"),
                    "amount": event.get("amount"),
                    "payment_type": event.get("payment_type"),
                },
                "source_protocol": "ap2",
            }
        elif protocol == "ucp":
            return {
                "type": f"ucp.{event.get('event_type', 'service')}",
                "agent_id": event.get("provider_id"),
                "timestamp": event.get("timestamp", time.time()),
                "payload": {
                    "service_id": event.get("service_id"),
                    "negotiation_status": event.get("negotiation_status"),
                    "transaction_id": event.get("transaction_id"),
                },
                "source_protocol": "ucp",
            }
        elif protocol == "paypal_agent_ready":
            return {
                "type": f"paypal.{event.get('event_type', 'payment')}",
                "agent_id": event.get("merchant_id"),
                "timestamp": event.get("timestamp", time.time()),
                "payload": {
                    "braintree_tx_id": event.get("braintree_tx_id"),
                    "amount": event.get("amount"),
                    "payer_id": event.get("payer_id"),
                },
                "source_protocol": "paypal_agent_ready",
            }
        elif protocol == "openai_acp":
            return {
                "type": f"openai_acp.{event.get('event_type', 'transaction')}",
                "agent_id": event.get("provider_id"),
                "timestamp": event.get("timestamp", time.time()),
                "payload": {
                    "transaction_id": event.get("transaction_id"),
                    "manifest_id": event.get("manifest_id"),
                    "amount": event.get("amount"),
                    "status": event.get("status"),
                },
                "source_protocol": "openai_acp",
            }
        else:
            return {
                "type": f"{protocol}.unknown",
                "agent_id": "unknown",
                "timestamp": time.time(),
                "payload": event,
                "source_protocol": protocol,
            }

    def _denormalize_event(self, protocol: str, normalized: dict) -> dict:
        """Convert the common format to a protocol-specific event."""
        if protocol == "greenhelix":
            return {
                "event_type": normalized["type"],
                "agent_id": normalized["agent_id"],
                "payload": json.dumps(normalized["payload"]),
            }
        elif protocol == "a2a":
            return {
                "jsonrpc": "2.0",
                "method": "tasks/update",
                "params": {
                    "id": normalized["payload"].get("task_id"),
                    "status": {"state": "working"},
                    "messages": [
                        {
                            "role": "agent",
                            "parts": [
                                {
                                    "type": "text",
                                    "text": json.dumps(normalized["payload"]),
                                }
                            ],
                        }
                    ],
                },
            }
        elif protocol == "acp":
            return {
                "type": normalized["type"].replace(".", "_"),
                "data": normalized["payload"],
                "created": int(normalized["timestamp"]),
            }
        elif protocol == "mcp":
            # MCP has no native events; format as a notification
            return {
                "jsonrpc": "2.0",
                "method": "notifications/message",
                "params": {
                    "level": "info",
                    "data": normalized["payload"],
                    "logger": f"greenhelix.bridge.{normalized['source_protocol']}",
                },
            }
        else:
            return normalized

    def forward_event(self, source_protocol: str, event: dict,
                       target_protocols: list = None) -> list:
        """Translate and forward an event to all registered webhooks.

        If target_protocols is specified, only forwards to those protocols.
        Otherwise, forwards to all protocols with registered webhooks.
        """
        results = []
        protocols_to_notify = target_protocols or list(self._webhook_registry.keys())

        for protocol in protocols_to_notify:
            webhooks = self._webhook_registry.get(protocol, [])
            translated = self.translate_event(source_protocol, event, protocol)

            for webhook in webhooks:
                # Check if this webhook is subscribed to this event type
                normalized_type = self._normalize_event(
                    source_protocol, event
                )["type"]

                subscribed = any(
                    normalized_type.startswith(evt)
                    for evt in webhook["events"]
                ) or "*" in webhook["events"]

                if not subscribed:
                    continue

                try:
                    resp = requests.post(
                        webhook["url"],
                        json=translated,
                        timeout=10,
                        headers={"X-Source-Protocol": source_protocol},
                    )
                    results.append({
                        "protocol": protocol,
                        "url": webhook["url"],
                        "status": resp.status_code,
                        "success": resp.status_code < 400,
                    })
                except requests.RequestException as e:
                    results.append({
                        "protocol": protocol,
                        "url": webhook["url"],
                        "status": 0,
                        "success": False,
                        "error": str(e),
                    })

        # Record the forwarding in GreenHelix event bus
        self.client.execute("publish_event", {
            "event_type": "bridge.event.forwarded",
            "agent_id": self.agent_id,
            "payload": json.dumps({
                "source_protocol": source_protocol,
                "target_protocols": protocols_to_notify,
                "results_count": len(results),
                "success_count": sum(1 for r in results if r["success"]),
            }),
        })

        return results

    def ingest_external_event(self, source_protocol: str,
                                event: dict) -> dict:
        """Ingest an event from an external protocol into the GreenHelix event bus.

        Normalizes the event and publishes it as a GreenHelix event, making
        external protocol activity visible in GreenHelix dashboards and
        audit trails.
        """
        normalized = self._normalize_event(source_protocol, event)
        gh_event = self._denormalize_event("greenhelix", normalized)

        result = self.client.execute("publish_event", {
            "event_type": gh_event["event_type"],
            "agent_id": self.agent_id,
            "payload": gh_event["payload"],
        })

        return {
            "ingested": True,
            "source_protocol": source_protocol,
            "greenhelix_event": result,
        }
```

### Webhook Translation Patterns

Three patterns cover the majority of cross-protocol event scenarios:

**Pattern 1: GreenHelix-Out.** A GreenHelix event (escrow released, payment completed, trust score changed) needs to notify an external system. The EventBridge translates the GreenHelix event into the target protocol's format and forwards it via webhook.

```python
# When a GreenHelix escrow completes, notify the A2A task caller
event_bridge.register_external_webhook(
    protocol="a2a",
    url="https://partner-agent.example.com/a2a/tasks/webhook",
    events=["escrow.released", "escrow.completed"],
)
```

**Pattern 2: External-In.** An external event (x402 payment settled, A2A task updated, ACP checkout completed) needs to appear in GreenHelix's event bus. The EventBridge normalizes the external event and publishes it as a GreenHelix event.

```python
# Ingest an x402 payment confirmation into GreenHelix
event_bridge.ingest_external_event("x402", {
    "tx_hash": "0xabc123...",
    "amount": "0.05",
    "payee_address": "0xYourAddress",
    "block_timestamp": 1712345678,
})
```

**Pattern 3: Protocol-to-Protocol.** An event from one external protocol needs to reach another external protocol, with GreenHelix as the translation hub. The event is ingested, translated, and forwarded in a single call.

```python
# An A2A task completion triggers an ACP fulfillment webhook
a2a_event = {"id": "task-123", "status": {"state": "completed"}}
event_bridge.forward_event("a2a", a2a_event, target_protocols=["acp"])
```

---

## Chapter 13: Production Bridge Deployment

### Performance: Caching Protocol Translations

Protocol translation adds latency. Each bridge call involves at least one GreenHelix API call, potentially a facilitator verification (x402), and event publishing. In production, three caching strategies reduce this overhead:

**Identity cache.** The `IdentityMapper` lookups are the most frequent cross-protocol operation. Cache resolved identities with a 5-minute TTL. A simple `functools.lru_cache` works for single-process deployments; use Redis for multi-process.

```python
from functools import lru_cache

@lru_cache(maxsize=1024)
def cached_resolve_identity(protocol: str, external_id: str):
    return identity_mapper.resolve_identity(protocol, external_id)
```

**Tool schema cache.** The MCP `tools/list` response is static until you add or remove services. Cache the entire response and invalidate only when the marketplace listing changes. This eliminates a GreenHelix API call on every MCP discovery request.

**Agent Card cache.** The A2A Agent Card changes infrequently. Serve it from a cache with a 10-minute TTL, refreshing from GreenHelix identity and marketplace data on cache miss.

### Security: Validating Cross-Protocol Payment Proofs

Every bridge that accepts payments from external protocols must validate the payment proof before executing the service. The validation requirements differ by protocol:

**x402 v2.** Verify the payment proof with the facilitator before creating the GreenHelix escrow. Never trust the client's claim that payment settled. The facilitator is the source of truth. Validate the `tx_hash`, the `amount`, the `payment_address`, and the `settlement_method` all match your expectations. For fiat settlement paths (new in v2), also verify that the facilitator's fiat confirmation includes a Stripe or AWS payment ID.

**ACP.** Verify the Stripe webhook signature before processing any ACP event. Use the `stripe_webhook_secret` to validate the `Stripe-Signature` header. Reject events with invalid signatures -- they may be replay attacks or forgeries.

**A2A v2.** A2A has no built-in payment, so payment validation happens at the GreenHelix layer. Verify that the caller's GreenHelix wallet has sufficient balance before creating the payment intent. If the caller does not have a GreenHelix identity, require them to register via the `IdentityMapper` before accepting paid tasks. For push notification webhooks (new in v2), validate the notification signature to prevent spoofed task updates.

**MCP 1.5.** For paid MCP tools, verify the caller's identity via OAuth 2.1 (new in MCP 1.5) and check balance before executing the tool. Use the `destructiveHint` and `idempotentHint` annotations to prevent accidental double-charges on non-idempotent payment tools. Include the payment intent ID in the response so the caller can verify the charge.

**Visa TAP.** Validate the TAP token with the acquiring bank before processing. Verify the 3DS2 agent certificate matches your registered TAP identity. Never process a TAP authorization without a valid authorization code from VisaNet. Monitor for chargebacks -- card-network disputes follow different timelines than on-chain settlements.

**Google AP2.** Verify every incoming AP2 payment event with Google's AP2 API. The `payment_id` returned by the event must match a verified `settled` status on Google's side. Do not release escrow or deliver services based solely on the webhook payload -- always verify against the AP2 API as the source of truth.

**PayPal Agent Ready.** Validate the Braintree webhook signature before processing settlement events. Verify that the Fastlane token has not expired and that the consumer's authorization scope covers the transaction amount. Monitor PayPal's dispute resolution timeline (180 days) and hold escrow reserves accordingly.

**OpenAI ACP.** Verify transaction events with the OpenAI ACP API. Validate that the `transaction_id` exists and the status matches the claimed event. For escrow-backed transactions, do not release funds until OpenAI ACP confirms buyer acceptance of the fulfillment result. Monitor the dispute window (configurable per manifest, typically 7-30 days).

For a comprehensive treatment of payment security patterns, cross-protocol threat models, and defense-in-depth strategies for agent commerce, see **The Agent Commerce Security Handbook** (Product 8 in this series).

### Monitoring: Tracking Bridge Health and Translation Errors

Each bridge should emit metrics and events that feed into your observability pipeline. The minimum viable metrics:

**Per-bridge counters:**
- `bridge.{protocol}.requests_total` -- total requests received per protocol.
- `bridge.{protocol}.translations_success` -- successful protocol translations.
- `bridge.{protocol}.translations_error` -- failed translations (schema mismatch, missing fields).
- `bridge.{protocol}.payment_verified` -- payment proofs that passed validation.
- `bridge.{protocol}.payment_rejected` -- payment proofs that failed validation.

**Latency histograms:**
- `bridge.{protocol}.translation_duration_ms` -- time spent translating protocol messages.
- `bridge.{protocol}.greenhelix_api_duration_ms` -- time spent in GreenHelix API calls.
- `bridge.{protocol}.total_duration_ms` -- end-to-end request duration.

**Error rates by type:**
- Identity resolution failures (no mapping found).
- Payment validation failures (invalid proof, insufficient balance).
- Event forwarding failures (webhook timeout, target unreachable).

Publish these metrics as GreenHelix events using `publish_event` with event type `bridge.metrics`. This makes bridge health visible in the same dashboards and alerting pipelines as your core agent commerce metrics. For a complete guide to building observability pipelines for agent commerce, including OpenTelemetry integration, health check patterns, and alerting thresholds, see **The Agent Testing and Observability Cookbook** (Product 9 in this series).

```python
class BridgeMonitor:
    """Lightweight monitoring for all bridge classes."""

    def __init__(self, client: GreenHelixClient, agent_id: str):
        self.client = client
        self.agent_id = agent_id
        self._counters = {}

    def record(self, protocol: str, metric: str, value: float = 1):
        """Record a metric value for a specific protocol bridge."""
        key = f"bridge.{protocol}.{metric}"
        self._counters[key] = self._counters.get(key, 0) + value

    def flush(self):
        """Publish accumulated metrics to GreenHelix event bus."""
        if not self._counters:
            return

        self.client.execute("publish_event", {
            "event_type": "bridge.metrics",
            "agent_id": self.agent_id,
            "payload": json.dumps({
                "counters": self._counters,
                "flushed_at": time.time(),
            }),
        })
        self._counters = {}
```

### Error Handling and Resilience

Bridge failures should degrade gracefully. If the x402 facilitator is unreachable, return a 503 with a `Retry-After` header -- do not silently accept unverified payments. If the A2A Agent Card generation fails because GreenHelix identity is temporarily unavailable, serve a cached card. If an event forward fails, queue it for retry with exponential backoff.

The principle is: **never compromise payment validation for availability.** A bridge that accepts unverified payments is worse than a bridge that is down. Payments are fail-closed. Everything else is fail-open.

For incident response procedures specific to bridge failures -- including runbooks for payment proof validation outages, identity resolution cascades, payment routing fallbacks, and event forwarding backlogs -- see **The Agent Incident Response Playbook** (Product 12 in this series).

### Putting It All Together

Here is the initialization code that wires up all bridge classes in a single deployment:

```python
# Initialize the shared GreenHelix client
client = GreenHelixClient(api_key="your-api-key")
agent_id = "my-commerce-agent"

# Identity mapper -- shared across all bridges
identity_mapper = IdentityMapper(client=client)

# Original four protocol bridges
x402_bridge = X402Bridge(
    client=client,
    agent_id=agent_id,
    facilitator_url="https://facilitator.x402.org",
    payment_address="0xYourUSDCAddress",
    accepted_settlements=["crypto", "stripe"],
)

acp_bridge = ACPBridge(
    client=client,
    agent_id=agent_id,
    stripe_webhook_secret="whsec_...",
)

a2a_bridge = A2ABridge(
    client=client,
    agent_id=agent_id,
    base_url="https://your-agent.example.com",
)

mcp_bridge = MCPBridge(
    client=client,
    agent_id=agent_id,
    exposed_tools=["search_services", "get_agent_identity", "send_message"],
)

# New protocol bridges
visa_tap_bridge = VisaTAPBridge(
    client=client,
    agent_id=agent_id,
    merchant_id="your-visa-merchant-id",
    acquiring_bank_endpoint="https://acquiring-bank.example.com/tap",
    tap_certificate_path="/etc/ssl/tap/agent-cert.pem",
)

ap2_ucp_bridge = AP2UCPBridge(
    client=client,
    agent_id=agent_id,
    ap2_account_id="your-ap2-account-id",
    ap2_api_key="your-ap2-api-key",
)

paypal_bridge = PayPalAgentReadyBridge(
    client=client,
    agent_id=agent_id,
    braintree_merchant_id="your-braintree-merchant-id",
    braintree_api_key="your-braintree-api-key",
    braintree_api_secret="your-braintree-api-secret",
)

openai_acp_bridge = OpenAIACPBridge(
    client=client,
    agent_id=agent_id,
    openai_acp_api_key="your-openai-acp-key",
)

# Payment router -- selects optimal protocol per transaction
payment_router = PaymentRouter(
    identity_mapper=identity_mapper,
    available_bridges={
        "x402": x402_bridge,
        "acp": acp_bridge,
        "visa_tap": visa_tap_bridge,
        "ap2": ap2_ucp_bridge,
        "paypal_agent_ready": paypal_bridge,
        "openai_acp": openai_acp_bridge,
    },
)

# Event bridge -- uses identity mapper for cross-protocol resolution
event_bridge = EventBridge(
    client=client,
    agent_id=agent_id,
    identity_mapper=identity_mapper,
)

# Monitoring
monitor = BridgeMonitor(client=client, agent_id=agent_id)

# Register cross-protocol identities
identity_mapper.register_mapping(agent_id, "x402", "0xYourUSDCAddress")
identity_mapper.register_mapping(agent_id, "acp", "acct_1234567890")
identity_mapper.register_mapping(agent_id, "a2a", "https://your-agent.example.com")
identity_mapper.register_mapping(agent_id, "mcp", "https://your-agent.example.com/mcp")
identity_mapper.register_mapping(agent_id, "visa_tap", "your-visa-merchant-id")
identity_mapper.register_mapping(agent_id, "ap2", "your-ap2-account-id")
identity_mapper.register_mapping(agent_id, "ucp", "your-ucp-provider-id")
identity_mapper.register_mapping(agent_id, "paypal_agent_ready", "your-braintree-merchant-id")
identity_mapper.register_mapping(agent_id, "openai_acp", "your-openai-acp-provider-id")

# Publish the A2A v2 Agent Card
a2a_bridge.publish_agent_card()

# Register MCP 1.5 tools
mcp_bridge.register_standard_tools()

# Sync listings to external registries
ap2_ucp_bridge.sync_listings_to_ucp()
openai_acp_bridge.register_manifests_in_acp()
```

Your GreenHelix agent is now reachable from nine protocol ecosystems. x402 v2 clients can pay per request via crypto or fiat. ACP agents can complete Stripe checkout flows. A2A v2 agents can discover your capabilities, stream task execution, and receive push notifications. MCP 1.5 clients can call your tools natively with safety annotations. Visa TAP agents can authorize card-network payments. Google AP2 agents can send real-time payments and discover your services through UCP. PayPal Agent Ready agents can pay through Fastlane tokens. OpenAI ACP agents can discover your service manifests, negotiate terms, and execute escrow-backed transactions. The PaymentRouter selects the cheapest or fastest path for every cross-protocol payment.

Every transaction -- regardless of originating protocol -- is recorded in the GreenHelix ledger with full audit trail, identity tracking, and trust score context.

The agentic web is fragmented. Your agents no longer are.

---

## What's Next

This guide covered the architecture and implementation of protocol bridges between GreenHelix and all nine major agentic web protocols: x402 v2 micropayments, ACP merchant checkout, A2A v2 task orchestration, MCP 1.5+ tool integration, Visa TAP card-network payments, Google AP2 real-time payments, Google UCP service orchestration, PayPal Agent Ready merchant integration, and OpenAI ACP commerce flows. Each bridge class handles protocol translation, payment recording, and identity mapping through a common GreenHelix client, shared identity registry, and intelligent payment router.

The protocol landscape will continue to fragment. New entrants will arrive. Existing protocols will release breaking version upgrades. The bridge architecture in this guide is designed for extensibility -- adding a new protocol means writing one bridge class that implements the translate-execute-translate pattern, registering it with the IdentityMapper, PaymentRouter, and EventBridge, and wiring it into the initialization block. The core infrastructure scales to any number of protocols.

For deeper coverage of specific domains referenced in this guide:

- **The Agent Commerce Security Handbook** -- threat models for cross-protocol payment validation, defense-in-depth for bridge endpoints, and secure key management across protocol boundaries.
- **The Agent Testing and Observability Cookbook** -- OpenTelemetry tracing for bridge calls, health check patterns for multi-protocol deployments, and alerting pipelines for translation errors.
- **The Agent Incident Response Playbook** -- runbooks for bridge-specific failures including payment proof validation outages, identity resolution cascades, and event forwarding backlogs.
- **Agent-to-Agent Commerce Toolkit** -- the foundational guide to GreenHelix escrow, identity, marketplace, and trust scoring that all bridges in this guide build upon.

For the full API reference and tool catalog (all 128 tools), visit the GreenHelix developer documentation at [https://api.greenhelix.net/docs](https://api.greenhelix.net/docs).

---

*Price: $29 | Format: Digital Guide | Updates: Lifetime access*

