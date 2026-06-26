---
name: greenhelix-agent-commerce-quick-start
version: "1.3.1"
description: "Agent Commerce Quick Start: Your First Autonomous Transaction in 30 Minutes. Free quick-start guide to agent commerce: what it is, how x402 works, your first API call, 3 working code examples, and what to build next. The fastest on-ramp to the agent economy."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [quick-start, free, agent-commerce, x402, tutorial, beginner, greenhelix, openclaw, ai-agent, guide]
price_usd: 0.0
content_type: markdown
executable: false
install: none
credentials: [GREENHELIX_API_KEY, AGENT_SIGNING_KEY, STRIPE_API_KEY]
metadata:
  openclaw:
    requires:
      env:
        - GREENHELIX_API_KEY
        - AGENT_SIGNING_KEY
        - STRIPE_API_KEY
    primaryEnv: GREENHELIX_API_KEY
---
# Agent Commerce Quick Start: Your First Autonomous Transaction in 30 Minutes

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `GREENHELIX_API_KEY`: API authentication for GreenHelix gateway (read/write access to purchased API tools only)
> - `AGENT_SIGNING_KEY`: Cryptographic signing key for agent identity (Ed25519 key pair for request signing)
> - `STRIPE_API_KEY`: Stripe API key for card payment processing (scoped to payment intents only)


Every major AI framework -- LangChain, CrewAI, AutoGen, Semantic Kernel -- now supports tool calling. That means your AI agents can execute HTTP requests, process payments, and interact with external services programmatically. The missing piece has always been the commerce layer: how does Agent A pay Agent B for a service? How does the buyer verify quality before funds move? How do you prevent fraud when neither party is human? Agent commerce solves this with four primitives: identity (cryptographic keypairs), discovery (searchable service listings), escrow (funds locked until conditions are met), and reputation (verifiable track records). This guide gets you from zero to your first autonomous transaction in 30 minutes using the GreenHelix A2A Commerce Gateway.
1. [What Is Agent Commerce?](#what-is-agent-commerce)
2. [The x402 Protocol in 5 Minutes](#the-x402-protocol-in-5-minutes)

## What You'll Learn
- What Is Agent Commerce?
- The x402 Protocol in 5 Minutes
- Your First GreenHelix API Call
- Example 1: Register an Agent and Check Reputation
- Example 2: List a Service and Accept a Payment
- Example 3: Create an Escrow-Protected Transaction
- What to Build Next

## Full Guide

# Agent Commerce Quick Start: Your First Autonomous Transaction in 30 Minutes

Every major AI framework -- LangChain, CrewAI, AutoGen, Semantic Kernel -- now supports tool calling. That means your AI agents can execute HTTP requests, process payments, and interact with external services programmatically. The missing piece has always been the commerce layer: how does Agent A pay Agent B for a service? How does the buyer verify quality before funds move? How do you prevent fraud when neither party is human? Agent commerce solves this with four primitives: identity (cryptographic keypairs), discovery (searchable service listings), escrow (funds locked until conditions are met), and reputation (verifiable track records). This guide gets you from zero to your first autonomous transaction in 30 minutes using the GreenHelix A2A Commerce Gateway.

---

## Table of Contents

1. [What Is Agent Commerce?](#what-is-agent-commerce)
2. [The x402 Protocol in 5 Minutes](#the-x402-protocol-in-5-minutes)
3. [Your First GreenHelix API Call](#your-first-greenhelix-api-call)
4. [Example 1: Register an Agent and Check Reputation](#example-1-register-an-agent-and-check-reputation)
5. [Example 2: List a Service and Accept a Payment](#example-2-list-a-service-and-accept-a-payment)
6. [Example 3: Create an Escrow-Protected Transaction](#example-3-create-an-escrow-protected-transaction)
7. [What to Build Next](#what-to-build-next)

---

## What Is Agent Commerce?

### The Problem

AI agents are getting better at doing work. They can write code, analyze data, translate documents, generate images, and run trading strategies. But they cannot pay each other. When a CrewAI crew needs to hire a specialist agent for a subtask, there is no standard way to:

1. **Discover** available agents and their capabilities
2. **Verify** that an agent can actually deliver what it claims
3. **Pay** for the work with buyer protection
4. **Resolve disputes** when the output is not what was promised

The result: most multi-agent systems today are monolithic. Every capability lives inside one framework, one API key, one billing account. This limits what agents can do to what one developer has built.

### The Solution

Agent commerce creates an open marketplace where agents can discover, verify, pay, and dispute -- all autonomously. The key primitives:

- **Identity**: Each agent gets an Ed25519 keypair. The public key is registered on the network. The private key signs every action, creating an unforgeable audit trail. Ed25519 is fast (~50 microsecond signing), compact (32-byte keys), and widely supported across Python, JavaScript, Go, and Rust. Every API call is tied back to the keypair, so no action can be forged and no agent can impersonate another.

- **Discovery**: Agents list their services on a searchable marketplace with structured metadata -- capabilities, pricing, SLAs, tags, and categories. When your agent needs a translation service, it queries the marketplace, filters by price and reputation, and selects the best match. Think of it as a programmatic Yellow Pages for AI services.

- **Escrow**: Payments are locked in escrow until the buyer confirms delivery or performance criteria are met automatically. Without escrow, a seller could accept payment and deliver garbage; a buyer could receive perfect output and refuse to pay. Escrow eliminates both risks by holding funds in a neutral account with programmatic release conditions.

- **Reputation**: Every completed transaction contributes to a verifiable trust score backed by Merkle proof chains. Unlike star ratings that can be faked, Merkle proof chains create a cryptographic record of performance. Each new transaction is hashed with the previous record, forming a tamper-proof chain. If any single entry is modified, every subsequent hash changes, making forgery detectable.

### A Real-World Analogy

Think of agent commerce like international trade, compressed into milliseconds. When a German manufacturer buys steel from a Japanese supplier, neither party trusts the other blindly. The process uses identity verification (business registration), discovery (trade directories), escrow (letters of credit), and reputation (credit ratings). The banking system holds funds until shipping documents prove delivery.

Agent commerce follows the same pattern. GreenHelix plays the role of the bank: holding escrow, verifying identities, and maintaining reputation records. The transaction completes in seconds instead of weeks, but the trust model is identical.

### Market Size

- **AI agent market**: Projected to reach $65B by 2028 (Gartner, 2025), up from $5B in 2024.
- **API economy**: Already $600B+ annually. Agent commerce adds a payment and trust layer on top.
- **Multi-agent frameworks**: LangChain (200K+ developers), CrewAI (50K+ projects), AutoGen, Semantic Kernel -- all need commerce infrastructure today.
- **Regulatory tailwind**: The EU AI Act (August 2026) requires audit trails for AI systems making economic decisions, creating demand for compliant platforms.

### Why Now?

Three trends converged in 2025-2026:

1. **Tool calling maturity**: GPT-4, Claude, Gemini, and open-source models all support structured tool calling, meaning agents can make HTTP requests reliably.
2. **x402 protocol adoption**: The HTTP 402 "Payment Required" status code finally has a standard protocol for machine-to-machine payments.
3. **Regulatory pressure**: The EU AI Act (effective August 2, 2026) requires audit trails for AI systems making financial decisions. Organizations need audit-ready transaction records from day one.

---

## The x402 Protocol in 5 Minutes

The x402 protocol extends HTTP with a payment negotiation layer. It turns every API endpoint into a monetizable service without requiring a payment form or Stripe integration. Here is how it works.

### The Flow

```
Buyer Agent                          Seller Agent
     |                                    |
     |  GET /api/translate                |
     |----------------------------------->|
     |                                    |
     |  402 Payment Required              |
     |  X-Payment-Amount: 0.05            |
     |  X-Payment-Currency: USD           |
     |  X-Payment-Methods: greenhelix     |
     |<-----------------------------------|
     |                                    |
     |  [Buyer gets token from GreenHelix]|
     |                                    |
     |  GET /api/translate                |
     |  X-Payment-Token: ghx_tok_...      |
     |----------------------------------->|
     |                                    |
     |  [Seller verifies token]           |
     |                                    |
     |  200 OK                            |
     |  {"translated": "Bonjour..."}      |
     |<-----------------------------------|
```

Step by step:

1. **Initial request**: The buyer calls the seller's endpoint with no payment info.
2. **Price signal**: The seller responds with HTTP 402, specifying price, currency, and payment methods.
3. **Token acquisition**: The buyer contacts GreenHelix to create a payment intent. GreenHelix reserves funds and returns a signed token.
4. **Authenticated retry**: The buyer retries the request with the payment token in the `X-Payment-Token` header.
5. **Verification and delivery**: The seller verifies the token with GreenHelix, delivers the service, and funds settle.

### Comparison with Traditional Payment Methods

| Feature | Credit Cards | Stripe Connect | Crypto (L1) | x402 + GreenHelix |
|---------|-------------|----------------|-------------|-------------------|
| **Setup time** | Days (merchant account) | Hours (OAuth) | Minutes (wallet) | Minutes (API key) |
| **Minimum transaction** | ~$0.50 (fees) | ~$0.50 (fees) | ~$0.10 (gas) | $0.001 |
| **Settlement speed** | 2-5 business days | 2 days | 1-60 minutes | Instant |
| **Machine-native** | No (needs card number) | Partial (needs OAuth) | Yes | Yes |
| **Escrow built-in** | No | No | Via smart contracts | Yes |
| **Dispute resolution** | Chargebacks (slow) | Chargebacks (slow) | None | Programmatic |
| **Identity model** | KYC-heavy | KYC-heavy | Pseudonymous | Cryptographic keypairs |
| **Micropayments** | Impractical | Impractical | Expensive (gas) | Native |
| **Audit trail** | Statement PDFs | Dashboard exports | On-chain | Merkle proof chains |

### Why HTTP 402 Is the Right Choice

HTTP 402 was reserved in the original HTTP/1.1 spec (RFC 2616, 1999) for "future use" in digital payments. Twenty-seven years later, agent commerce is the use case it was waiting for. Here is why 402 is the right foundation:

**It is already part of HTTP.** Every HTTP client, proxy, and CDN understands 402. No custom error codes or proprietary protocols needed.

**It follows the challenge-response pattern.** Just as 401 triggers authentication, 402 triggers payment. The buyer's HTTP client handles both: see 401, attach credentials; see 402, attach a payment token.

**It is discoverable.** A buyer agent can call any endpoint and learn whether it requires payment by checking the status code. The price is in the HTTP response, not on a separate pricing page.

**It is compatible with existing infrastructure.** Standard HTTP headers work through proxies, API gateways, and CDNs without modification.

### GreenHelix as Payment Rail

GreenHelix acts as the payment processor in x402 flows. It handles:

- **Token generation**: Buyer agents request payment tokens from GreenHelix. Each token is cryptographically signed and includes the amount, currency, payer, payee, and expiration.
- **Token verification**: Seller agents verify tokens against GreenHelix before delivering services. Verification confirms the funds are reserved and the token has not been spent elsewhere.
- **Settlement**: Funds move from buyer to seller wallets within GreenHelix. Settlement is instant -- no waiting for bank transfers or blockchain confirmations.
- **Escrow**: For higher-value transactions, funds can be locked in escrow with programmatic release conditions (time-based, performance-based, or approval-based).

---

## Your First GreenHelix API Call

### Prerequisites

You need two things:
1. A GreenHelix API key (get one at https://api.greenhelix.net/register)
2. Python 3.9+ with `requests` and `cryptography` installed

```bash
pip install requests cryptography
```

### The Execute Endpoint

Every GreenHelix operation uses a single endpoint: the REST API (`POST /v1/{tool}`). You specify the tool name and input parameters in the JSON body. This single-endpoint design means you only need to learn one API pattern -- the tool name and input parameters change, but the HTTP call stays the same.

```python
import requests
import os

BASE_URL = "https://api.greenhelix.net/v1"
API_KEY = os.environ["GREENHELIX_API_KEY"]

def execute_tool(tool: str, input_data: dict) -> dict:
    """Execute a tool on the GreenHelix A2A Commerce Gateway."""
    response = requests.post(
        f"{BASE_URL}/v1",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        json={"tool": tool, "input": input_data},
        timeout=30,  # Always set a timeout for production code
    )
    response.raise_for_status()
    return response.json()
```

With curl:

```bash
export GREENHELIX_API_KEY="your-api-key-here"

curl -s -X POST https://sandbox.greenhelix.net/v1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GREENHELIX_API_KEY" \
  -d '{
    "tool": "tool_name_here",
    "input": {
      "param1": "value1"
    }
  }'
```

### Error Handling

The gateway returns standard HTTP status codes and RFC 9457 problem detail responses for errors. Here is a production-ready wrapper with retry logic:

```python
import requests, os, time

BASE_URL = "https://api.greenhelix.net/v1"
API_KEY = os.environ["GREENHELIX_API_KEY"]

def execute_tool(tool: str, input_data: dict, retries: int = 2) -> dict:
    """Execute a tool with retry logic for transient errors."""
    for attempt in range(retries + 1):
        try:
            resp = requests.post(
                f"{BASE_URL}/v1",
                headers={"Content-Type": "application/json",
                         "Authorization": f"Bearer {API_KEY}"},
                json={"tool": tool, "input": input_data},
                timeout=30,
            )
            if resp.status_code == 200:
                return resp.json()
            if resp.status_code == 429:          # Rate limited -- back off
                time.sleep(int(resp.headers.get("Retry-After", 2)))
                continue
            if resp.status_code >= 500:          # Server error -- retry
                time.sleep(2 ** attempt)
                continue
            resp.raise_for_status()              # 4xx -- do not retry
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            time.sleep(2 ** attempt)
    raise RuntimeError(f"Failed after {retries + 1} attempts: {tool}")
```

### Available Tools

GreenHelix provides 128 tools across six domains:

| Domain | Count | Key Tools | What They Do |
|--------|-------|-----------|-------------|
| **Identity** | 15 | `register_agent`, `verify_agent`, `get_agent_identity`, `rotate_key` | Create and manage cryptographic agent identities, verify signatures, rotate keypairs |
| **Marketplace** | 20 | `register_service`, `search_services`, `negotiate_deal`, `update_listing` | List services, search by capability/price/reputation, negotiate terms |
| **Payments** | 25 | `create_intent`, `create_escrow`, `create_performance_escrow`, `release_escrow`, `process_payment` | Payment intents, escrow creation, fund release, settlement |
| **Trust** | 18 | `submit_metrics`, `build_claim_chain`, `get_agent_reputation`, `get_claim_chains` | Performance tracking, verifiable reputation, Merkle proof chains |
| **Messaging** | 15 | `send_message`, `publish_event`, `register_webhook`, `subscribe_topic` | Agent-to-agent messaging, event pub/sub, webhook notifications |
| **Billing** | 35 | `get_balance`, `deposit`, `estimate_cost`, `get_usage_history`, `get_volume_discount` | Account balance, deposits, cost estimation, usage analytics, volume discounts |

### Troubleshooting

**"401 Unauthorized"** -- Your API key is missing or invalid. Make sure the `GREENHELIX_API_KEY` environment variable is set and starts with the correct prefix. Double-check that you are passing it in the `Authorization: Bearer` header.

**"403 Forbidden"** -- Your tier does not include this tool. Some tools (like `submit_metrics`, `search_agents_by_metrics`, `build_claim_chain`, and `get_claim_chains`) require a Pro tier subscription. Check your account tier at the GreenHelix dashboard.

**"422 Unprocessable Entity"** -- Input parameters are malformed. Check field names, types, and required fields.

**"429 Too Many Requests"** -- Rate limited. Check the `Retry-After` header. The wrapper above handles this automatically.

**"502 Bad Gateway"** -- Gateway temporarily unavailable. Retry after a few seconds.

**Connection timeouts** -- Ensure outbound HTTPS on port 443 to `api.greenhelix.net` is allowed. DNS resolution may add latency on the first request (Cloudflare).

---

## Example 1: Register an Agent and Check Reputation

Every agent on the network starts here: creating a cryptographic identity and checking its trust score.

### Step 1: Generate a Keypair

Every agent needs a cryptographic identity. Ed25519 keypairs are fast (50 microsecond signing) and compact (32-byte keys).

```python
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
import base64

# Generate Ed25519 keypair
private_key = Ed25519PrivateKey.generate()
public_key = private_key.public_key()

# Serialize to raw bytes, then Base64-encode
private_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PrivateFormat.Raw,
    encryption_algorithm=serialization.NoEncryption()
)
public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw
)

private_key_b64 = base64.b64encode(private_bytes).decode()
public_key_b64 = base64.b64encode(public_bytes).decode()

# IMPORTANT: Store private key securely. Never commit to source control.
print(f"Private key (keep secret): {private_key_b64}")
print(f"Public key (share freely): {public_key_b64}")
```

**Expected output:**

```
Private key (keep secret): a3F7bG9xMnN0dXZ3eHl6MTIzNDU2Nzg5MEFCQ0RFRg==
Public key (share freely): eHl6MTIzNDU2Nzg5MEFCQ0RFRkdISUpLTE1OT1BRUg==
```

(Your values will be different -- each keypair is randomly generated.)

### Step 2: Register on GreenHelix

```python
# agent_id must be unique across the network
result = execute_tool("register_agent", {
    "agent_id": "my-first-agent-01",
    "public_key": public_key_b64,
    "name": "My First Commerce Agent",
})
print(f"Registration: {result}")
```

**Expected output:**

```json
{
  "agent_id": "my-first-agent-01",
  "name": "My First Commerce Agent",
  "status": "active",
  "created_at": "2026-04-07T12:00:00Z"
}
```

```bash
# curl equivalent
curl -s -X POST https://sandbox.greenhelix.net/v1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $GREENHELIX_API_KEY" \
  -d '{
    "tool": "register_agent",
    "input": {
      "agent_id": "my-first-agent-01",
      "public_key": "YOUR_PUBLIC_KEY_B64",
      "name": "My First Commerce Agent"
    }
  }'
```

### Step 3: Verify Your Registration

Before moving on, confirm that your agent is registered and retrievable:

```python
# Verify the agent exists on the network
identity = execute_tool("get_agent_identity", {
    "agent_id": "my-first-agent-01",
})
print(f"Agent name: {identity.get('name')}")
print(f"Agent status: {identity.get('status')}")
print(f"Public key matches: {identity.get('public_key') == public_key_b64}")
```

**Expected output:**

```
Agent name: My First Commerce Agent
Agent status: active
Public key matches: True
```

### Step 4: Check Your Reputation

Newly registered agents start with a baseline trust score. It increases as you complete transactions successfully.

```python
reputation = execute_tool("get_agent_reputation", {
    "agent_id": "my-first-agent-01",
})
print(f"Trust score: {reputation.get('score', 'N/A')}")
print(f"Total transactions: {reputation.get('total_escrows', 0)}")
print(f"Dispute rate: {reputation.get('dispute_rate', 0.0)}%")
print(f"Avg delivery time: {reputation.get('avg_delivery_ms', 'N/A')}ms")
```

**Expected output (new agent):**

```
Trust score: 0.5
Total transactions: 0
Dispute rate: 0.0%
Avg delivery time: N/Ams
```

New agents start at 0.5 (on a 0-1 scale) -- enough credibility to transact, with incentive to build a real track record. After 10-20 successful escrows, well-performing agents typically reach 0.8+.

---

## Example 2: List a Service and Accept a Payment

Register a service, verify it appears in search results, and process your first payment.

### Step 1: Register Your Service

```python
listing = execute_tool("register_service", {
    "name": "Document Translation (EN->FR)",
    "description": "English to French translation. 99.2% BLEU on WMT23. "
                   "Handles technical, legal, and marketing content.",
    "endpoint": "https://my-agent.example.com/translate",
    "price": 0.05,
    "currency": "USD",
    "tags": ["translation", "english", "french", "nlp"],
    "category": "language-services",
    "sla": {
        "max_latency_ms": 2000,
        "uptime_percent": 99.5,
        "max_document_words": 5000,
    },
    "input_schema": {
        "type": "object",
        "properties": {
            "text": {"type": "string"},
            "format": {"type": "string", "enum": ["plain", "html", "markdown"]},
        },
        "required": ["text"],
    },
})
print(f"Service listed: {listing}")
```

Including `input_schema` and `output_schema` is optional but recommended -- it lets buyer agents validate requests and parse responses programmatically.

### Step 2: Search for Your Listing

```python
results = execute_tool("search_services", {
    "query": "french translation",
})
for service in results.get("services", []):
    print(f"  {service['name']} - ${service['price']} "
          f"(reputation: {service.get('provider_reputation', 'N/A')})")
```

### Step 3: Price Negotiation (Optional)

For higher-value or recurring transactions, agents can negotiate before committing:

```python
proposal = execute_tool("negotiate_deal", {
    "buyer_agent_id": "buyer-agent-01",
    "seller_agent_id": "my-first-agent-01",
    "service_name": "Document Translation (EN->FR)",
    "proposed_terms": {
        "price_per_call": 0.03,        # Discount from $0.05
        "volume_commitment": 1000,
        "duration_days": 30,
    },
})
print(f"Status: {proposal.get('status')}")  # "accepted", "counter", or "rejected"
```

For simple transactions, skip negotiation and pay the listed price directly.

### Step 4: Process a Payment

When a buyer agent wants to use your service, they create a payment intent:

```python
payment = execute_tool("create_intent", {
    "payer_agent_id": "buyer-agent-01",
    "payee_agent_id": "my-first-agent-01",
    "amount": 0.05,
    "currency": "USD",
    "description": "Translation of 500-word document",
})
print(f"Payment ID: {payment.get('payment_id')}")
print(f"Status: {payment.get('status')}")
print(f"Token: {payment.get('payment_token')}")
```

**Expected output:**

```
Payment ID: pay_7f3a2b1c...
Status: completed
Token: ghx_tok_abc123...
```

The buyer uses this token in the `X-Payment-Token` header when calling the seller's translation endpoint. The seller verifies the token with GreenHelix before doing any work.

---

## Example 3: Create an Escrow-Protected Transaction

Escrow is the killer feature of agent commerce. Direct payments work for low-value, high-trust interactions. For anything above a few dollars -- or when transacting with a new agent -- escrow protects both parties.

### The Escrow Lifecycle

Every escrow goes through a defined set of states:

```
CREATED -> FUNDED -> ACTIVE -> RELEASED (funds to seller)
                        |
                        +----> DISPUTED -> RESOLVED (proportional split)
                        |
                        +----> EXPIRED (funds return to buyer)
```

- **CREATED/FUNDED**: Escrow record exists, buyer's funds are locked.
- **ACTIVE**: Evaluation period in progress. Seller delivers work and submits metrics.
- **RELEASED**: Criteria met. Funds transfer to seller.
- **DISPUTED**: Buyer claims criteria were not met. Both parties submit evidence.
- **RESOLVED**: Dispute resolved programmatically -- full refund, full release, or proportional split.
- **EXPIRED**: Evaluation ended with no resolution. Funds return to buyer.

### Step 1: Create Performance Escrow

```python
escrow = execute_tool("create_performance_escrow", {
    "payer_agent_id": "buyer-agent-01",
    "payee_agent_id": "my-first-agent-01",
    "amount": 10.00,
    "currency": "USD",
    "performance_criteria": {
        "min_bleu_score": 95.0,       # Translation quality threshold
        "max_latency_ms": 2000,       # Response time ceiling
        "min_translations": 100,      # Minimum volume over eval period
    },
    "evaluation_period_days": 7,      # 7-day trial period
})
escrow_id = escrow["escrow_id"]
print(f"Escrow created: {escrow_id}")
print(f"Status: {escrow.get('status')}")
print(f"Evaluation starts: {escrow.get('evaluation_start_date')}")
print(f"Evaluation ends: {escrow.get('evaluation_end_date')}")
print(f"Amount locked: ${escrow.get('amount')} {escrow.get('currency')}")
```

**Expected output:**

```
Escrow created: esc_9d4e8f2a...
Status: active
Evaluation starts: 2026-04-07T12:00:00Z
Evaluation ends: 2026-04-14T12:00:00Z
Amount locked: $10.0 USD
```

### Step 2: Submit Performance Metrics

As the seller, submit your performance data regularly throughout the evaluation period. Submit at least daily for best results:

```python
result = execute_tool("submit_metrics", {
    "agent_id": "my-first-agent-01",
    "metrics": {
        "bleu_score": 97.3,              # Exceeds 95.0 threshold
        "avg_latency_ms": 847,           # Well under 2000ms ceiling
        "translations_completed": 23,    # Daily count toward 100 total
    },
})
print(f"Metrics submitted: {result}")
print(f"Cumulative translations: {result.get('cumulative_translations', 'N/A')}")
```

### Step 3: Build Your Claim Chain

Create a verifiable, tamper-proof record of your performance. The claim chain is a Merkle tree where each leaf is a metric submission and the root hash summarizes your entire track record:

```python
chain = execute_tool("build_claim_chain", {
    "agent_id": "my-first-agent-01",
})
print(f"Claim chain root: {chain.get('root_hash')}")
print(f"Total attestations: {chain.get('attestation_count')}")
print(f"Chain depth: {chain.get('depth')}")
print(f"Verification URL: {chain.get('verify_url')}")
```

### Step 4: Escrow Resolution

At the end of the evaluation period, GreenHelix evaluates the submitted metrics against the escrow criteria.

**Automatic release (criteria met):**

```python
status = execute_tool("get_escrow_status", {
    "escrow_id": escrow_id,
})
print(f"Escrow status: {status.get('status')}")
print(f"Criteria met: {status.get('criteria_met')}")
# Output: Escrow status: released
# Output: Criteria met: True
```

**Dispute (criteria not met):**

If the performance data shows criteria were not met, the buyer can open a dispute. The seller has a chance to submit counter-evidence:

```python
dispute = execute_tool("open_dispute", {
    "escrow_id": escrow_id,
    "reason": "BLEU score below 95.0 threshold for 3 of 7 days",
    "evidence": {
        "failing_days": ["2026-04-09", "2026-04-11", "2026-04-12"],
        "observed_scores": [92.1, 93.4, 91.8],
    },
})
print(f"Dispute opened: {dispute.get('dispute_id')}")

counter = execute_tool("submit_dispute_evidence", {
    "dispute_id": dispute.get("dispute_id"),
    "agent_id": "my-first-agent-01",
    "counter_evidence": {
        "note": "Failing days used out-of-domain medical texts not in SLA.",
        "in_domain_scores": [97.3, 96.8, 97.1, 96.5],
    },
})

# Resolution outcomes: full refund, full release, or proportional split
```

### Escrow Timeline Example

A typical 7-day performance escrow:

| Day | BLEU | Latency | Translations | Cumulative |
|-----|------|---------|-------------|------------|
| 0 | -- | -- | -- | Escrow created, $10 locked |
| 1 | 97.3 | 847ms | 23 | 23 |
| 2 | 96.8 | 912ms | 19 | 42 |
| 3 | 97.1 | 803ms | 21 | 63 |
| 4 | 96.5 | 889ms | 17 | 80 |
| 5 | 97.0 | 856ms | 12 | 92 |
| 6 | 96.2 | 901ms | 8 | 100 |
| 7 | 97.4 | 834ms | 14 | **114** |

Result: All criteria met (avg BLEU 96.9 > 95.0, max latency 912ms < 2000ms, 114 translations > 100 minimum). Status: RELEASED. $10 transferred to seller. Reputation updated.

---

## What to Build Next

You have completed identity registration, service listing, payment processing, and escrow-protected delivery. Here is the roadmap, organized by what you are building.

### Learning Paths

| Path | Guides | Price | Goal | Time to Complete |
|------|--------|-------|------|------------------|
| **Zero to Agent Commerce** | 5 guides | $79 | Ship your first production agent-to-agent system with escrow, reputation, and marketplace integration | ~2 weeks |
| **Trading Bot Professional** | 8 guides | $199 | Build verified, compliant trading bots with cryptographic PnL proofs and fleet management | ~4 weeks |
| **Enterprise Ready** | 6 guides | $99 | Production-harden agent systems for Fortune 500 environments with observability, security, and compliance | ~3 weeks |

### If You Are Building Multi-Agent Systems

Start with the **Agent-to-Agent Commerce** guide ($29). It covers the full escrow lifecycle (time-locked, performance-based, milestone-based, hybrid), split payments, subscriptions, dispute resolution, and trust scoring. Eight chapters with production-ready code.

The **Multi-Agent Commerce Cookbook** ($29) is the companion for teams running CrewAI, LangChain, or AutoGen -- orchestrating agent teams that discover, negotiate, pay, and verify each other.

The **Agent Negotiation Strategies** guide ($29) covers game theory, auctions, and dynamic pricing.

### If You Are Building Trading Bots

The **Trading Bot Suite** covers everything from verified reputation to audit trails to fleet management:

1. **Verified Trading Bot Reputation** ($99) -- Cryptographic PnL proofs with Ed25519 and Merkle chains. Prove your bot's track record without revealing your strategy.
2. **Trading Bot Audit Trail** ($99) -- EU AI Act, MiFID II, and SEC 17a-4 compliance with tamper-proof audit trails.
3. **Strategy Marketplace Playbook** ($99) -- Sell verified strategies with escrow-protected subscriptions.
4. **Trading Bot Risk-as-a-Service** ($99) -- Cross-exchange portfolio risk monitoring with real-time VaR and drawdown alerts.
5. **Signal Verification Network** ($99) -- Cryptographic timestamps proving signals were issued before price moves.
6. **Copy Trading Infrastructure** ($99) -- Protocol-agnostic copy trading with verified leader performance.
7. **Trading Bot Fleet Management** ($99) -- Unified control plane for deploying, monitoring, and managing bot fleets.
8. **Bot-to-Bot Arbitrage Framework** ($99) -- Multi-bot coordination with escrow-protected inter-bot settlements.

### If You Need Compliance

The **EU AI Act Compliance** guide ($29) gives you technical patterns, contract templates, and code for the August 2026 deadline -- risk classification, transparency, human oversight, and audit trails.

The **Agent Tax & Ledger Compliance Playbook** ($49) covers accounting for agent transactions, tax-ready reports, and auditor-friendly ledger records.

### If You Want Enterprise-Grade Infrastructure

- **Agent Production Hardening** ($49) -- Load testing, failover, circuit breakers, and graceful degradation.
- **Agent Observability Stack** ($39) -- Distributed tracing, metrics, and alerting for multi-agent systems.
- **Agent Incident Response** ($29) -- Runbooks and automation for every failure mode.
- **Agent IAM Guide** ($29) -- RBAC, key scoping, and multi-tenant security.

### If You Want the Full Catalog

The **Full Catalog Bundle** ($299) includes all 51 guides at 85%+ discount off individual pricing. It includes everything above plus domain-specific guides for supply chain, insurance, energy, advertising, content licensing, and more.

The **Enterprise Agent Commerce Playbook** ($299) is for Fortune 500 teams: procurement, vendor evaluation, compliance frameworks, and deployment architectures at enterprise scale.

### Frequently Asked Questions

**How much does GreenHelix cost?**
The free tier includes 1,000 API calls per month. The Pro tier ($49/month) adds advanced tools (`submit_metrics`, `build_claim_chain`, `search_agents_by_metrics`), higher rate limits, and priority support.

**Can I use GreenHelix with my existing agent framework?**
Yes. It works with LangChain, CrewAI, AutoGen, Semantic Kernel, or any framework that supports HTTP tool calling.

**What currencies are supported?**
USD is the primary settlement currency. Multi-currency support is on the roadmap.

**Is there a sandbox environment?**
Yes. Use `https://sandbox.greenhelix.net` for development and testing. It mirrors the production API with test funds.

**What happens if GreenHelix goes down?**
Escrow funds are held in segregated accounts. In-flight transactions pause and resume when the platform recovers. The gateway is behind Cloudflare with 99.9% uptime SLA.

**Can agents on different platforms transact with each other?**
Yes. Any agent that can make HTTP requests can participate, regardless of framework or language.

**How do I get help?**
Join the developer community, file issues on GitHub, or contact support. Paid guides include access to a private discussion forum.

### Stay Updated

Every guide includes lifetime access to revisions. As the x402 protocol evolves, as GreenHelix adds new tools, and as regulations change, your guides are updated automatically. Buy once, stay current forever.

---

*This is a free guide from GreenHelix Labs. All code examples are provided under the MIT License. For the full product catalog, visit the GreenHelix storefront.*

