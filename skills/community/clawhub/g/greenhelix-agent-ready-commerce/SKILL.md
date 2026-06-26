---
name: greenhelix-agent-ready-commerce
version: "1.3.1"
description: "Agent-Ready Commerce: Retrofit Your APIs for AI Buyers. Build agent-discoverable storefronts and API-first product feeds so AI shopping agents choose your products over competitors. Covers structured data, UCP/ACP/x402 payment rails, and marketplace integration with detailed code examples with code."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [agentic-commerce, aco, ucp, acp, product-feeds, discovery, guide, greenhelix, openclaw, ai-agent]
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
# Agent-Ready Commerce: Retrofit Your APIs for AI Buyers

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


AI shopping agents now influence over $67 billion in purchasing decisions. Between January 2025 and March 2026, AI-attributed orders grew 11x across tracked e-commerce platforms. The brands capturing this revenue share one trait: their product data is structured for machines, not just humans. The new commerce funnel is agent query, structured response, programmatic purchase -- and every gap in that chain is revenue lost to a competitor whose data is cleaner, whose schemas are richer, and whose checkout flow an agent can complete without human intervention.
This guide is the practitioner's manual for building agent-ready commerce infrastructure. Every chapter contains production Python code against the GreenHelix A2A Commerce Gateway -- 128 tools accessible at `https://api.greenhelix.net/v1` via a single the REST API (`POST /v1/{tool}`) endpoint. By the end, you will have an agent-discoverable storefront, structured product feeds with validation, multi-protocol checkout flows (UCP, ACP, x402), a GreenHelix marketplace listing with trust signals, escrow-protected payment flows, an agent discoverability test harness, and a 14-day sprint plan to ship all of it.
1. [The Agentic Commerce Shift](#chapter-1-the-agentic-commerce-shift)

## What You'll Learn
- Chapter 1: The Agentic Commerce Shift
- Chapter 2: Anatomy of an Agent-Ready Storefront
- Chapter 3: UCP, ACP, and x402: Choosing Your Payment Rails
- Chapter 4: Structured Product Feeds That Win
- Chapter 5: Agent Discovery via GreenHelix Marketplace
- Chapter 6: Agent-to-Agent Payment Flows
- Chapter 7: Testing Agent Discoverability
- Chapter 8: The 14-Day ACO Sprint
- Appendix: Tool Reference

## Full Guide

# Agent-Ready Commerce: Retrofit Your APIs for AI Buyers

AI shopping agents now influence over $67 billion in purchasing decisions. Between January 2025 and March 2026, AI-attributed orders grew 11x across tracked e-commerce platforms. The brands capturing this revenue share one trait: their product data is structured for machines, not just humans. The new commerce funnel is agent query, structured response, programmatic purchase -- and every gap in that chain is revenue lost to a competitor whose data is cleaner, whose schemas are richer, and whose checkout flow an agent can complete without human intervention.

This guide is the practitioner's manual for building agent-ready commerce infrastructure. Every chapter contains production Python code against the GreenHelix A2A Commerce Gateway -- 128 tools accessible at `https://api.greenhelix.net/v1` via a single the REST API (`POST /v1/{tool}`) endpoint. By the end, you will have an agent-discoverable storefront, structured product feeds with validation, multi-protocol checkout flows (UCP, ACP, x402), a GreenHelix marketplace listing with trust signals, escrow-protected payment flows, an agent discoverability test harness, and a 14-day sprint plan to ship all of it.

---

## Table of Contents

1. [The Agentic Commerce Shift](#chapter-1-the-agentic-commerce-shift)
2. [Anatomy of an Agent-Ready Storefront](#chapter-2-anatomy-of-an-agent-ready-storefront)
3. [UCP, ACP, and x402: Choosing Your Payment Rails](#chapter-3-ucp-acp-and-x402-choosing-your-payment-rails)
4. [Structured Product Feeds That Win](#chapter-4-structured-product-feeds-that-win)
5. [Agent Discovery via GreenHelix Marketplace](#chapter-5-agent-discovery-via-greenhelix-marketplace)
6. [Agent-to-Agent Payment Flows](#chapter-6-agent-to-agent-payment-flows)
7. [Testing Agent Discoverability](#chapter-7-testing-agent-discoverability)
8. [The 14-Day ACO Sprint](#chapter-8-the-14-day-aco-sprint)

---

## Chapter 1: The Agentic Commerce Shift

### The Numbers That Changed Everything

During Cyber Week 2025, AI-powered shopping agents influenced $67 billion in U.S. online spending. Salesforce tracked the transactions: AI-attributed product recommendations drove 17% of all orders, up from 5% the previous year. Adobe Analytics reported that AI-powered chatbots on retail sites handled 1.3 billion sessions during the five-day window. But the more important metric came from Shopify's internal analysis: merchants whose product data scored above 95% attribute completeness saw 3-4x the AI-referred traffic of merchants below 80%. The agents were not choosing randomly. They were choosing the products they could understand.

By March 2026, the growth curve had steepened. AI-attributed orders across the 50 largest U.S. e-commerce platforms grew 11x compared to January 2025 -- from 0.3% of total orders to 3.3%. That percentage sounds small until you calculate the absolute numbers: 3.3% of the $1.1 trillion U.S. e-commerce market is $36.3 billion in transactions where an AI agent materially influenced the purchase decision. The trajectory puts AI-attributed commerce above $100 billion by mid-2027.

### The New Funnel

Traditional e-commerce optimizes for human eyeballs: product images, emotional copy, social proof badges, countdown timers. The conversion funnel is awareness, consideration, decision, purchase -- each stage designed for a human scrolling on a phone.

Agent commerce replaces every stage:

| Traditional Stage | Agent Commerce Equivalent | What the Agent Needs |
|---|---|---|
| **Awareness** | Agent discovers your product via structured query | JSON-LD schema, OpenAPI spec, marketplace listing |
| **Consideration** | Agent compares attributes programmatically | Complete attribute data, machine-readable pricing, real-time inventory |
| **Decision** | Agent selects based on ranking algorithm | Trust signals, verified metrics, claim chains |
| **Purchase** | Agent completes checkout via API | Programmatic payment rails (UCP/ACP/x402), escrow support |

Notice what is missing: images, emotional copy, brand storytelling. Agents do not read your About page. They parse your product schema. If your schema is incomplete, you are invisible to the fastest-growing channel in commerce.

### Why "Agent-Readable" Means Revenue

The data is unambiguous. Salsify's 2026 Product Experience Benchmark studied 14,000 product listings across Amazon, Walmart, and Target. Products with 99.9% attribute completeness -- every field filled, every variant specified, every specification machine-parseable -- achieved 3-4x the visibility in AI-powered search compared to products at 90% completeness. The relationship was not linear. It was a step function: below 95%, visibility dropped off a cliff. Above 99%, it climbed exponentially.

The reason is structural. AI agents use retrieval-augmented generation (RAG) to match user queries to product data. The retrieval step depends on embedding similarity between the query and the product description. A product listing that says "Blue Widget, $29.99" generates a weak embedding. A listing with structured JSON-LD including `color: "Navy Blue (Pantone 19-4052)"`, `material: "6061-T6 Anodized Aluminum"`, `dimensions: {"length": 12.5, "width": 3.2, "height": 1.8, "unit": "cm"}`, `certifications: ["ISO 9001:2015", "RoHS"]` generates an embedding that matches far more queries -- including queries the merchant never anticipated.

This is the core thesis of this guide: **structured product data is not a technical nice-to-have. It is revenue infrastructure.**

### The GreenHelix Commerce Stack

The GreenHelix A2A Commerce Gateway provides the infrastructure for agent-ready commerce across the full lifecycle: discovery (marketplace listing, search, ranking), payment (escrow, subscriptions, deposits), trust (metrics, claim chains, reputation scoring), and interoperability (protocol bridges for UCP, ACP, x402).

Every code example in this guide calls the gateway via the REST API (`POST /v1/{tool}`):

```python
import requests
from typing import Any

GATEWAY_URL = os.environ.get("GREENHELIX_API_URL", "https://sandbox.greenhelix.net")

class CommerceClient:
    """Client for GreenHelix A2A Commerce Gateway."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def execute(self, tool: str, input_data: dict[str, Any]) -> dict:
        """Execute a single tool on the gateway."""
        response = requests.post(
            f"{GATEWAY_URL}/v1",
            json={"tool": tool, "input": input_data},
            headers=self.headers,
            timeout=30,
        )
        response.raise_for_status()
        return response.json()

# Initialize once, use throughout
client = CommerceClient(api_key="your-api-key-here")
```

This client object is referenced in every subsequent chapter. Store your API key in an environment variable (`GREENHELIX_API_KEY`), never in source code.

> **Key Takeaways**
>
> - AI shopping agents influenced $67B+ during Cyber Week 2025. AI-attributed orders grew 11x between January 2025 and March 2026.
> - Products with 99.9% attribute completeness achieve 3-4x visibility in agent-powered search. Below 95% completeness, visibility collapses.
> - The agent commerce funnel is: structured query, programmatic comparison, API-driven purchase. Every stage requires machine-readable data.
> - GreenHelix provides the full commerce stack: discovery, payments, trust, and protocol interoperability through 128 tools at a single endpoint.

---

## Chapter 2: Anatomy of an Agent-Ready Storefront

### The Three Layers of Agent Discoverability

An agent-ready storefront exposes three machine-readable layers that allow AI agents to discover, evaluate, and purchase your products without human intervention:

1. **Manifest layer** -- `.well-known/ai-plugin.json` tells agents your storefront exists and where to find its API.
2. **Schema layer** -- JSON-LD product schemas embedded in pages (or served via API) describe every product attribute in a format agents can parse.
3. **API layer** -- An OpenAPI specification defines endpoints agents call to search products, check inventory, and initiate checkout.

Miss any layer and you break the chain. An agent that discovers your manifest but finds no OpenAPI spec cannot call your API. An agent that finds your API but no product schemas cannot compare your products to competitors.

### Layer 1: The AI Plugin Manifest

The `.well-known/ai-plugin.json` manifest is the entry point. Agents crawling for commerce endpoints check this path first -- it is the equivalent of `robots.txt` for AI commerce agents. The specification originated with OpenAI's ChatGPT plugin system and has been adopted as a de facto standard across Gemini, Perplexity, and Claude shopping agents.

```json
{
  "schema_version": "v1",
  "name_for_human": "Precision Parts Direct",
  "name_for_model": "precision_parts",
  "description_for_human": "Industrial precision components with same-day shipping.",
  "description_for_model": "Structured product catalog of 12,000+ precision-machined components. Supports real-time inventory queries, attribute-based filtering (material, tolerance, certification), bulk pricing, and programmatic checkout via UCP, ACP, or x402. All products have 99.9%+ attribute completeness with JSON-LD schemas.",
  "auth": {
    "type": "service_http",
    "authorization_type": "bearer",
    "verification_tokens": {
      "greenhelix": "ghx_verify_abc123"
    }
  },
  "api": {
    "type": "openapi",
    "url": "https://parts.example.com/.well-known/openapi.yaml",
    "is_user_authenticated": false
  },
  "logo_url": "https://parts.example.com/logo.png",
  "contact_email": "api@parts.example.com",
  "legal_info_url": "https://parts.example.com/legal"
}
```

Three fields matter most for agent discoverability:

- **`description_for_model`** -- This is what the agent reads. Pack it with structured keywords: product count, attribute types, supported payment protocols, completeness score. Agents use this for semantic matching against user queries.
- **`api.url`** -- Must point to a valid OpenAPI spec. Agents parse this to learn your endpoint signatures, request/response schemas, and authentication requirements.
- **`auth.verification_tokens.greenhelix`** -- If you register on the GreenHelix marketplace, include this token so the gateway can verify your listing is legitimate.

### Layer 2: JSON-LD Product Schemas

JSON-LD (JavaScript Object Notation for Linked Data) is the structured data format that Google, Bing, and now AI agents use to understand product attributes. Embed it in your HTML pages via `<script type="application/ld+json">` tags, or serve it directly via API for agent-only consumption.

```python
def build_product_schema(product: dict) -> dict:
    """Build a JSON-LD Product schema from internal product data."""
    schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": product["name"],
        "description": product["description"],
        "sku": product["sku"],
        "mpn": product.get("mpn", ""),
        "brand": {
            "@type": "Brand",
            "name": product["brand"],
        },
        "offers": {
            "@type": "Offer",
            "url": product["url"],
            "priceCurrency": "USD",
            "price": str(product["price"]),
            "availability": (
                "https://schema.org/InStock"
                if product["inventory"] > 0
                else "https://schema.org/OutOfStock"
            ),
            "itemCondition": "https://schema.org/NewCondition",
            "priceValidUntil": product.get("price_valid_until", "2026-12-31"),
            "seller": {
                "@type": "Organization",
                "name": product["seller_name"],
            },
        },
        "additionalProperty": [
            {
                "@type": "PropertyValue",
                "name": key,
                "value": value,
            }
            for key, value in product.get("attributes", {}).items()
        ],
    }

    # Add aggregate rating if available
    if product.get("rating_count", 0) > 0:
        schema["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": str(product["rating_value"]),
            "reviewCount": str(product["rating_count"]),
        }

    return schema


# Example usage
product_data = {
    "name": "Precision Ball Bearing - 608-2RS",
    "description": "Sealed radial ball bearing, 8mm bore, ABEC-7 precision grade",
    "sku": "PBB-608-2RS-ABEC7",
    "mpn": "608-2RS-P7",
    "brand": "RotorTech",
    "url": "https://parts.example.com/products/pbb-608-2rs-abec7",
    "price": 4.75,
    "inventory": 24500,
    "seller_name": "Precision Parts Direct",
    "price_valid_until": "2026-06-30",
    "rating_value": 4.8,
    "rating_count": 1247,
    "attributes": {
        "bore_diameter_mm": "8",
        "outer_diameter_mm": "22",
        "width_mm": "7",
        "material": "Chrome Steel (AISI 52100)",
        "seal_type": "Double Rubber Seal (2RS)",
        "abec_grade": "ABEC-7",
        "max_rpm": "42000",
        "dynamic_load_rating_kn": "3.45",
        "static_load_rating_kn": "1.37",
        "weight_grams": "12",
        "operating_temp_range": "-30C to +120C",
        "certifications": "ISO 9001:2015, ISO 14001:2015",
    },
}

schema = build_product_schema(product_data)
```

That product has 15 structured attributes. An agent searching for "ABEC-7 bearing under $5 with double seal rated above 40000 RPM" will match every field. A competing listing that only specifies "ball bearing, $4.75" will not match the query -- even if the physical product is identical.

### Layer 3: OpenAPI Specification

The OpenAPI spec defines the programmatic interface agents use to search, filter, and purchase. Here is a minimal spec for a product catalog API:

```yaml
openapi: 3.1.0
info:
  title: Precision Parts API
  version: 1.0.0
  description: Agent-ready product catalog with structured search and checkout
paths:
  /products/search:
    post:
      operationId: searchProducts
      summary: Search products by structured attributes
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                query:
                  type: string
                filters:
                  type: object
                  properties:
                    material:
                      type: string
                    min_price:
                      type: number
                    max_price:
                      type: number
                    in_stock:
                      type: boolean
                    certifications:
                      type: array
                      items:
                        type: string
                sort_by:
                  type: string
                  enum: [price_asc, price_desc, rating, relevance]
                limit:
                  type: integer
                  default: 20
      responses:
        '200':
          description: Matching products with full schemas
  /products/{sku}/inventory:
    get:
      operationId: getInventory
      summary: Real-time inventory for a specific SKU
      parameters:
        - name: sku
          in: path
          required: true
          schema:
            type: string
      responses:
        '200':
          description: Current inventory count and restock ETA
  /checkout/initiate:
    post:
      operationId: initiateCheckout
      summary: Start a programmatic checkout flow
      requestBody:
        content:
          application/json:
            schema:
              type: object
              required: [items, payment_protocol]
              properties:
                items:
                  type: array
                  items:
                    type: object
                    properties:
                      sku:
                        type: string
                      quantity:
                        type: integer
                payment_protocol:
                  type: string
                  enum: [ucp, acp, x402, greenhelix_escrow]
                buyer_agent_id:
                  type: string
      responses:
        '200':
          description: Checkout session with payment instructions
```

### Building It in 30 Minutes: FastAPI Implementation

Here is a complete agent-ready storefront API using FastAPI. It serves the manifest, product schemas, and checkout endpoint -- and registers itself on the GreenHelix marketplace for discoverability.

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os

app = FastAPI(title="Precision Parts API", version="1.0.0")

# GreenHelix client (from Chapter 1)
client = CommerceClient(api_key=os.environ["GREENHELIX_API_KEY"])

# In-memory product catalog (replace with database in production)
CATALOG = {
    "PBB-608-2RS-ABEC7": {
        "name": "Precision Ball Bearing - 608-2RS",
        "sku": "PBB-608-2RS-ABEC7",
        "price": 4.75,
        "inventory": 24500,
        "brand": "RotorTech",
        "description": "Sealed radial ball bearing, 8mm bore, ABEC-7 precision",
        "seller_name": "Precision Parts Direct",
        "url": "https://parts.example.com/products/pbb-608-2rs-abec7",
        "attributes": {
            "bore_diameter_mm": "8",
            "outer_diameter_mm": "22",
            "material": "Chrome Steel (AISI 52100)",
            "seal_type": "Double Rubber Seal (2RS)",
            "abec_grade": "ABEC-7",
            "max_rpm": "42000",
            "certifications": "ISO 9001:2015",
        },
        "rating_value": 4.8,
        "rating_count": 1247,
    },
}


@app.get("/.well-known/ai-plugin.json")
def ai_plugin_manifest():
    """Serve the AI plugin manifest for agent discovery."""
    return {
        "schema_version": "v1",
        "name_for_human": "Precision Parts Direct",
        "name_for_model": "precision_parts",
        "description_for_model": (
            "Structured catalog of 12,000+ precision components. "
            "Supports attribute search, real-time inventory, bulk pricing, "
            "and checkout via UCP, ACP, x402, or GreenHelix escrow. "
            "99.9% attribute completeness."
        ),
        "api": {
            "type": "openapi",
            "url": "https://parts.example.com/openapi.json",
        },
    }


class SearchRequest(BaseModel):
    query: str = ""
    filters: dict = {}
    sort_by: str = "relevance"
    limit: int = 20


@app.post("/products/search")
def search_products(req: SearchRequest):
    """Search products with structured filters."""
    results = []
    for sku, product in CATALOG.items():
        # Apply filters
        if req.filters.get("max_price") and product["price"] > req.filters["max_price"]:
            continue
        if req.filters.get("material"):
            if req.filters["material"].lower() not in product["attributes"].get("material", "").lower():
                continue
        results.append(build_product_schema(product))

    return {"results": results[:req.limit], "total": len(results)}


@app.get("/products/{sku}/inventory")
def get_inventory(sku: str):
    """Real-time inventory check."""
    product = CATALOG.get(sku)
    if not product:
        raise HTTPException(status_code=404, detail="SKU not found")
    return {
        "sku": sku,
        "available": product["inventory"],
        "in_stock": product["inventory"] > 0,
    }


class CheckoutRequest(BaseModel):
    items: list[dict]
    payment_protocol: str  # ucp, acp, x402, greenhelix_escrow
    buyer_agent_id: str = ""


@app.post("/checkout/initiate")
def initiate_checkout(req: CheckoutRequest):
    """Start a programmatic checkout flow."""
    # Calculate total
    total = 0.0
    for item in req.items:
        product = CATALOG.get(item["sku"])
        if not product:
            raise HTTPException(status_code=404, detail=f"SKU {item['sku']} not found")
        total += product["price"] * item.get("quantity", 1)

    if req.payment_protocol == "greenhelix_escrow":
        # Create escrow via GreenHelix
        escrow = client.execute("create_escrow", {
            "payer_agent_id": req.buyer_agent_id,
            "payee_agent_id": "precision-parts-agent",
            "amount": str(total),
            "description": f"Order: {len(req.items)} items",
        })
        return {
            "checkout_id": escrow.get("escrow_id"),
            "total": str(total),
            "protocol": "greenhelix_escrow",
            "status": "escrow_created",
            "instructions": "Funds are locked. Seller will ship and release on delivery.",
        }

    # Return protocol-specific payment instructions for UCP/ACP/x402
    return {
        "total": str(total),
        "protocol": req.payment_protocol,
        "status": "payment_required",
        "payment_url": f"https://parts.example.com/pay/{req.payment_protocol}",
    }


# Register on GreenHelix marketplace at startup
@app.on_event("startup")
async def register_on_marketplace():
    """Register this storefront on GreenHelix for agent discovery."""
    try:
        client.execute("register_service", {
            "name": "Precision Parts Direct",
            "description": (
                "Industrial precision components: bearings, shafts, seals, "
                "fasteners. 12,000+ SKUs. 99.9% attribute completeness. "
                "Same-day shipping. Supports escrow checkout."
            ),
            "endpoint": "https://parts.example.com",
            "price": 0.0,
            "tags": ["precision-parts", "bearings", "industrial", "b2b"],
            "category": "industrial_components",
        })
    except Exception as e:
        print(f"Marketplace registration failed: {e}")
```

This gives you a fully agent-discoverable storefront in under 200 lines. An AI agent can find it via the `.well-known` manifest, parse the OpenAPI spec, search products by structured attributes, check inventory, and initiate checkout through four different payment protocols.

> **Key Takeaways**
>
> - Agent-ready storefronts have three layers: manifest (`.well-known/ai-plugin.json`), schema (JSON-LD product data), and API (OpenAPI spec with search and checkout endpoints).
> - The `description_for_model` field in your manifest is the single most important field for agent discovery. Pack it with structured keywords and capability descriptions.
> - JSON-LD product schemas with complete attributes are what allow agents to match your products to queries. Every missing attribute is a missed query match.
> - A complete FastAPI storefront with marketplace registration can be built in 30 minutes and under 200 lines of Python.

---

## Chapter 3: UCP, ACP, and x402: Choosing Your Payment Rails

### The Three-Protocol Reality

As of April 2026, three payment protocols dominate agent commerce. Each solves a different problem, targets a different buyer type, and requires a different integration. Most production storefronts will support at least two.

**Universal Commerce Protocol (UCP)** -- Google and Shopify's protocol for structured product discovery and checkout. UCP defines a standardized product catalog format that agents query to find available products, compare prices, and initiate purchases. The checkout flow delegates to the merchant's existing payment infrastructure (typically Stripe or Shopify Payments). UCP is in production on Shopify and Google Shopping. It is the most widely supported protocol for agent-to-merchant commerce.

**Agentic Commerce Protocol (ACP)** -- OpenAI and Stripe's protocol for AI agent checkout. ACP powers Instant Checkout in ChatGPT for merchants on Etsy, Shopify, and Instacart. The flow uses Shared Payment Tokens (SPTs) -- delegated spending authority from a human's Stripe account to an agent. ACP handles product search, cart assembly, and Stripe-based checkout. It requires the merchant to have a Stripe account.

**x402** -- Coinbase and Cloudflare's HTTP-native micropayment protocol, now under the Linux Foundation with Google, Stripe, AWS, and Visa as founding members. The server returns HTTP 402 with a payment requirement. The client pays in USDC via a facilitator. Settlement is on-chain (Base L2, Solana, or Ethereum L2s). Sub-cent transaction fees make it ideal for pay-per-request API access and digital product delivery. See P19 (Payment Rails Playbook) for deep implementation details.

### Protocol Comparison Matrix

| Dimension | UCP | ACP | x402 | GreenHelix |
|---|---|---|---|---|
| **Backed by** | Google, Shopify | OpenAI, Stripe | Linux Foundation, Coinbase, Cloudflare | GreenHelix Labs |
| **Primary use case** | Structured product discovery + checkout | AI agent instant checkout | HTTP micropayments | Full agent commerce stack |
| **Settlement** | Merchant's processor (Stripe, Shopify Pay) | Stripe | On-chain (USDC on Base/Solana) | Built-in ledger + escrow |
| **Minimum transaction** | Processor-dependent (~$0.50) | $0.50 (Stripe minimum) | $0.0001 (sub-cent) | $0.01 |
| **Buyer requirements** | Payment method on file | Stripe SPT (human-authorized) | USDC wallet | GreenHelix wallet (deposit-based) |
| **Seller requirements** | UCP catalog registration | Stripe merchant account | x402 facilitator integration | GreenHelix service registration |
| **Escrow support** | No | No (Stripe disputes only) | No | Yes (standard + performance) |
| **Discovery built-in** | Yes (UCP catalog) | Yes (merchant catalog) | No | Yes (marketplace + best_match) |
| **Dispute resolution** | Via merchant | Via Stripe | None | Built-in (create_dispute/resolve_dispute) |
| **Best for** | Physical goods, retail | Consumer purchases via ChatGPT | API access, digital content | Agent-to-agent services |

### When to Use Each

**Use UCP when** you sell physical products or structured services and want maximum reach across Google Shopping and Shopify-integrated agents. UCP's structured catalog format maps directly to the JSON-LD schemas from Chapter 2. If you already sell on Shopify, UCP integration is near-automatic.

**Use ACP when** ChatGPT users are a significant buyer segment. ACP's Instant Checkout eliminates the redirect-to-website friction that kills conversion. The human authorizes spending via an SPT, and the agent completes the purchase inside the conversation. Conversion rates for ACP-enabled merchants are 2-3x higher than redirect-based checkout.

**Use x402 when** you sell digital products, API access, or content that can be delivered per-request. x402's sub-cent fees make it viable for transactions that would be uneconomical on card rails. A $0.002 data enrichment call that costs $0.30 on Stripe costs $0.00001 on x402.

**Use GreenHelix escrow when** trust is critical -- the buyer needs assurance that funds are locked until delivery is verified, or the seller needs assurance that the buyer cannot cancel after work begins. Escrow is essential for agent-to-agent service transactions where neither party has a pre-existing relationship.

### Code: Multi-Protocol Checkout Handler

This class handles checkout across all four protocols, with GreenHelix as the escrow layer for any protocol that lacks native buyer protection.

```python
import requests
import hashlib
import time
from dataclasses import dataclass
from typing import Optional

GATEWAY_URL = os.environ.get("GREENHELIX_API_URL", "https://sandbox.greenhelix.net")


@dataclass
class CheckoutResult:
    protocol: str
    status: str
    transaction_id: str
    amount: str
    instructions: Optional[dict] = None


class MultiProtocolCheckout:
    """Handle checkout across UCP, ACP, x402, and GreenHelix escrow."""

    def __init__(self, api_key: str, seller_agent_id: str):
        self.api_key = api_key
        self.seller_agent_id = seller_agent_id
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def _ghx(self, tool: str, input_data: dict) -> dict:
        """Execute a GreenHelix tool."""
        resp = requests.post(
            f"{GATEWAY_URL}/v1",
            json={"tool": tool, "input": input_data},
            headers=self.headers,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def checkout_ucp(
        self, buyer_agent_id: str, items: list[dict], total: float
    ) -> CheckoutResult:
        """UCP checkout: structured catalog query + merchant payment.

        In production, this calls the UCP catalog API to validate
        availability and then redirects to the merchant's payment page.
        We wrap it in GreenHelix escrow for buyer protection.
        """
        # Create escrow to protect the buyer
        escrow = self._ghx("create_escrow", {
            "payer_agent_id": buyer_agent_id,
            "payee_agent_id": self.seller_agent_id,
            "amount": str(total),
            "description": f"UCP order: {len(items)} items",
        })

        # Record the payment intent for UCP tracking
        intent = self._ghx("create_payment_intent", {
            "payer_agent_id": buyer_agent_id,
            "payee_agent_id": self.seller_agent_id,
            "amount": str(total),
            "currency": "USD",
            "description": "UCP-routed order with escrow protection",
        })

        return CheckoutResult(
            protocol="ucp",
            status="escrow_created",
            transaction_id=escrow.get("escrow_id", ""),
            amount=str(total),
            instructions={
                "escrow_id": escrow.get("escrow_id"),
                "payment_intent_id": intent.get("intent_id"),
                "next_step": "Buyer confirms delivery, then escrow releases.",
            },
        )

    def checkout_acp(
        self, buyer_agent_id: str, items: list[dict], total: float,
        stripe_spt: str,
    ) -> CheckoutResult:
        """ACP checkout: Stripe Shared Payment Token flow.

        The buyer agent holds an SPT (delegated by its human principal).
        We validate the SPT, charge via Stripe, and record on GreenHelix.
        """
        # Record the payment on GreenHelix for auditing
        intent = self._ghx("create_payment_intent", {
            "payer_agent_id": buyer_agent_id,
            "payee_agent_id": self.seller_agent_id,
            "amount": str(total),
            "currency": "USD",
            "description": f"ACP checkout via Stripe SPT",
        })

        # In production: call Stripe API with the SPT to charge
        # stripe.PaymentIntent.create(amount=int(total*100), ...)

        return CheckoutResult(
            protocol="acp",
            status="payment_captured",
            transaction_id=intent.get("intent_id", ""),
            amount=str(total),
            instructions={
                "stripe_spt_used": True,
                "intent_id": intent.get("intent_id"),
                "next_step": "Payment captured. Fulfillment begins.",
            },
        )

    def checkout_x402(
        self, buyer_agent_id: str, items: list[dict], total: float,
    ) -> CheckoutResult:
        """x402 checkout: HTTP 402 micropayment flow.

        Returns 402 payment requirement. Buyer settles in USDC via
        facilitator, then retries with X-PAYMENT-PROOF header.
        """
        # Generate a unique payment requirement
        payment_id = hashlib.sha256(
            f"{buyer_agent_id}:{time.time()}".encode()
        ).hexdigest()[:16]

        # Record on GreenHelix
        intent = self._ghx("create_payment_intent", {
            "payer_agent_id": buyer_agent_id,
            "payee_agent_id": self.seller_agent_id,
            "amount": str(total),
            "currency": "USD",
            "description": f"x402 payment requirement {payment_id}",
        })

        return CheckoutResult(
            protocol="x402",
            status="payment_required",
            transaction_id=payment_id,
            amount=str(total),
            instructions={
                "http_status": 402,
                "payment_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18",
                "currency": "USDC",
                "network": "base",
                "facilitator": "https://x402.org/facilitator",
                "intent_id": intent.get("intent_id"),
                "next_step": "Pay via facilitator, retry with X-PAYMENT-PROOF header.",
            },
        )

    def checkout_escrow(
        self, buyer_agent_id: str, items: list[dict], total: float,
    ) -> CheckoutResult:
        """GreenHelix native escrow checkout."""
        escrow = self._ghx("create_escrow", {
            "payer_agent_id": buyer_agent_id,
            "payee_agent_id": self.seller_agent_id,
            "amount": str(total),
            "description": f"Direct escrow: {len(items)} items, ${total:.2f}",
        })

        return CheckoutResult(
            protocol="greenhelix_escrow",
            status="escrow_created",
            transaction_id=escrow.get("escrow_id", ""),
            amount=str(total),
            instructions={
                "escrow_id": escrow.get("escrow_id"),
                "next_step": "Seller fulfills order. Buyer releases escrow on delivery.",
            },
        )

    def route_checkout(
        self, buyer_agent_id: str, items: list[dict], total: float,
        preferred_protocol: str = "greenhelix_escrow",
        stripe_spt: Optional[str] = None,
    ) -> CheckoutResult:
        """Route to the appropriate checkout flow based on protocol preference."""
        router = {
            "ucp": lambda: self.checkout_ucp(buyer_agent_id, items, total),
            "acp": lambda: self.checkout_acp(buyer_agent_id, items, total, stripe_spt or ""),
            "x402": lambda: self.checkout_x402(buyer_agent_id, items, total),
            "greenhelix_escrow": lambda: self.checkout_escrow(buyer_agent_id, items, total),
        }
        handler = router.get(preferred_protocol)
        if not handler:
            raise ValueError(f"Unsupported protocol: {preferred_protocol}")
        return handler()


# Usage
checkout = MultiProtocolCheckout(
    api_key="your-api-key",
    seller_agent_id="precision-parts-agent",
)

# Route based on buyer's preferred protocol
result = checkout.route_checkout(
    buyer_agent_id="buyer-agent-007",
    items=[{"sku": "PBB-608-2RS-ABEC7", "quantity": 100}],
    total=475.00,
    preferred_protocol="greenhelix_escrow",
)
print(f"Protocol: {result.protocol}, Status: {result.status}")
print(f"Transaction: {result.transaction_id}")
```

### Protocol Selection Decision Tree

```
Is the buyer a ChatGPT user with a Stripe SPT?
  └─ Yes → ACP (highest conversion for ChatGPT users)
  └─ No →
      Is the transaction < $0.50?
        └─ Yes → x402 (sub-cent fees, USDC settlement)
        └─ No →
            Does the buyer need escrow protection?
              └─ Yes → GreenHelix Escrow (funds locked until delivery)
              └─ No →
                  Is the buyer on Google Shopping or Shopify?
                    └─ Yes → UCP (structured catalog integration)
                    └─ No → GreenHelix Escrow (safest default)
```

> **Key Takeaways**
>
> - UCP, ACP, and x402 each serve different buyer segments and transaction sizes. Most storefronts should support at least two protocols.
> - ACP delivers 2-3x higher conversion for ChatGPT users via Instant Checkout. x402 enables sub-cent micropayments that card rails cannot support.
> - GreenHelix escrow wraps any protocol with buyer protection -- use it as the default for agent-to-agent transactions where trust is not yet established.
> - A multi-protocol checkout handler with routing logic can be built in a single class. Route based on buyer capabilities, transaction size, and trust requirements.
> - Cross-reference P19 (Payment Rails Playbook) for deep x402 and MPP implementation details, and P13 (Interoperability Bridge) for protocol bridging patterns.

---

## Chapter 4: Structured Product Feeds That Win

### The Completeness Cliff

Salsify analyzed 2.3 million product listings across major U.S. retail platforms in Q1 2026. The finding that reshaped the industry: AI agent visibility is not a linear function of attribute completeness. It is a step function.

| Attribute Completeness | Relative AI Agent Visibility | Agent-Attributed Orders (Index) |
|---|---|---|
| < 80% | 1x (baseline) | 100 |
| 80% - 89% | 1.2x | 115 |
| 90% - 94% | 1.5x | 140 |
| 95% - 98% | 2.1x | 210 |
| 99% - 99.8% | 2.8x | 290 |
| 99.9%+ | 3.8x | 380 |

The jump from 98% to 99.9% -- filling in those last few attributes -- nearly doubles visibility. This is because AI agents use embedding-based retrieval, and each additional structured attribute adds a new dimension to the embedding vector that can match queries. A product missing `operating_temp_range` is invisible to every query that includes temperature requirements, even if the product physically meets the spec.

### Attribute Completeness Scoring

Build a scoring system that identifies gaps in your product data before they cost you visibility.

```python
from dataclasses import dataclass, field


@dataclass
class CompletenessReport:
    sku: str
    score: float
    total_fields: int
    filled_fields: int
    missing: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


# Define required and recommended attributes by category
ATTRIBUTE_REQUIREMENTS = {
    "industrial_components": {
        "required": [
            "name", "sku", "brand", "price", "description",
            "material", "dimensions", "weight", "certifications",
        ],
        "recommended": [
            "mpn", "operating_temp_range", "max_load_rating",
            "tolerance", "finish", "country_of_origin",
            "lead_time_days", "moq", "bulk_pricing_tiers",
            "datasheet_url", "cad_model_url", "rohs_compliant",
        ],
        "optional": [
            "color", "packaging_type", "shelf_life",
            "hazmat_classification", "customs_tariff_code",
        ],
    },
    "digital_products": {
        "required": [
            "name", "sku", "price", "description",
            "format", "file_size", "license_type",
        ],
        "recommended": [
            "version", "compatible_platforms", "language",
            "sample_url", "changelog_url", "support_url",
            "api_documentation_url", "uptime_sla",
        ],
        "optional": [
            "trial_available", "refund_policy", "volume_discounts",
        ],
    },
}


def score_completeness(
    product: dict, category: str = "industrial_components"
) -> CompletenessReport:
    """Score a product's attribute completeness."""
    reqs = ATTRIBUTE_REQUIREMENTS.get(category, ATTRIBUTE_REQUIREMENTS["industrial_components"])

    all_fields = reqs["required"] + reqs["recommended"] + reqs["optional"]
    # Flatten product attributes for checking
    flat = {**product, **product.get("attributes", {})}

    filled = []
    missing = []
    warnings = []

    for attr in reqs["required"]:
        if flat.get(attr) not in (None, "", [], {}):
            filled.append(attr)
        else:
            missing.append(f"[REQUIRED] {attr}")

    for attr in reqs["recommended"]:
        if flat.get(attr) not in (None, "", [], {}):
            filled.append(attr)
        else:
            missing.append(f"[RECOMMENDED] {attr}")

    for attr in reqs["optional"]:
        if flat.get(attr) not in (None, "", [], {}):
            filled.append(attr)

    # Quality warnings
    if flat.get("description") and len(str(flat["description"])) < 50:
        warnings.append("Description is under 50 characters -- expand for better embeddings")
    if flat.get("price") and float(flat["price"]) == 0:
        warnings.append("Price is zero -- agents may filter this as unavailable")
    if not flat.get("certifications"):
        warnings.append("No certifications listed -- reduces trust signal for B2B agents")

    total = len(all_fields)
    score = len(filled) / total if total > 0 else 0.0

    return CompletenessReport(
        sku=product.get("sku", "unknown"),
        score=round(score * 100, 1),
        total_fields=total,
        filled_fields=len(filled),
        missing=missing,
        warnings=warnings,
    )


# Score a product
report = score_completeness(product_data, "industrial_components")
print(f"SKU: {report.sku}")
print(f"Completeness: {report.score}%")
print(f"Filled: {report.filled_fields}/{report.total_fields}")
for m in report.missing:
    print(f"  Missing: {m}")
for w in report.warnings:
    print(f"  Warning: {w}")
```

### Machine-Readable Pricing Rules

Agents need to understand your pricing programmatically -- not just the base price, but volume discounts, tiered pricing, promotional rules, and currency conversion. Encode pricing rules in a structured format that agents can parse and calculate against.

```python
import json
from typing import Optional


def build_pricing_rules(product: dict) -> dict:
    """Build machine-readable pricing rules for a product."""
    rules = {
        "@type": "PricingRules",
        "sku": product["sku"],
        "base_price": {
            "amount": str(product["price"]),
            "currency": "USD",
            "valid_until": product.get("price_valid_until", "2026-12-31"),
        },
        "volume_discounts": [
            {"min_quantity": 1, "max_quantity": 99, "unit_price": str(product["price"])},
            {"min_quantity": 100, "max_quantity": 499, "unit_price": str(round(product["price"] * 0.90, 2))},
            {"min_quantity": 500, "max_quantity": 999, "unit_price": str(round(product["price"] * 0.82, 2))},
            {"min_quantity": 1000, "max_quantity": None, "unit_price": str(round(product["price"] * 0.75, 2))},
        ],
        "bulk_rounding": "per_tier",
        "payment_protocols": ["ucp", "acp", "x402", "greenhelix_escrow"],
        "accepted_currencies": ["USD", "EUR", "USDC"],
    }
    return rules


# Generate pricing rules for catalog
pricing = build_pricing_rules(product_data)
print(json.dumps(pricing, indent=2))
```

### Real-Time Inventory Webhooks

Agents that check inventory get burned by stale data. If your catalog shows 500 units but only 3 remain, the agent starts a checkout that fails at fulfillment. This destroys your trust score. Implement real-time inventory webhooks that push updates to subscribed agents.

```python
import time


class InventoryWebhookManager:
    """Manage real-time inventory webhooks via GreenHelix events."""

    def __init__(self, client: "CommerceClient"):
        self.client = client

    def publish_inventory_update(self, sku: str, quantity: int, warehouse: str = "primary"):
        """Push inventory update to subscribed agents."""
        return self.client.execute("publish_event", {
            "event_type": "inventory.updated",
            "payload": {
                "sku": sku,
                "available_quantity": quantity,
                "warehouse": warehouse,
                "timestamp": time.time(),
                "in_stock": quantity > 0,
                "low_stock_warning": quantity < 50,
            },
        })

    def publish_price_change(self, sku: str, old_price: float, new_price: float):
        """Notify subscribed agents of a price change."""
        return self.client.execute("publish_event", {
            "event_type": "pricing.updated",
            "payload": {
                "sku": sku,
                "old_price": str(old_price),
                "new_price": str(new_price),
                "change_pct": str(round((new_price - old_price) / old_price * 100, 2)),
                "effective_at": time.time(),
            },
        })


# Usage
webhook_mgr = InventoryWebhookManager(client)

# Inventory dropped -- push to all subscribed agents
webhook_mgr.publish_inventory_update("PBB-608-2RS-ABEC7", quantity=47)

# Price reduction -- agents watching this SKU get notified
webhook_mgr.publish_price_change("PBB-608-2RS-ABEC7", old_price=4.75, new_price=4.25)
```

### Product Feed Generator with Validation

Combine schemas, pricing, and inventory into a validated product feed that agents consume.

```python
import json
import time
from typing import Optional


class ProductFeedGenerator:
    """Generate validated, agent-ready product feeds."""

    def __init__(self, client: "CommerceClient", seller_id: str):
        self.client = client
        self.seller_id = seller_id

    def generate_feed(
        self, products: list[dict], category: str = "industrial_components"
    ) -> dict:
        """Generate a complete product feed with validation."""
        feed_items = []
        errors = []
        total_score = 0.0

        for product in products:
            # Score completeness
            report = score_completeness(product, category)
            total_score += report.score

            if report.score < 90.0:
                errors.append(
                    f"SKU {product['sku']}: completeness {report.score}% "
                    f"(below 90% threshold). Missing: {report.missing[:3]}"
                )
                continue

            # Build the feed item
            item = {
                "schema": build_product_schema(product),
                "pricing": build_pricing_rules(product),
                "inventory": {
                    "available": product.get("inventory", 0),
                    "in_stock": product.get("inventory", 0) > 0,
                    "updated_at": time.time(),
                },
                "completeness_score": report.score,
            }
            feed_items.append(item)

        avg_score = total_score / len(products) if products else 0.0

        feed = {
            "@context": "https://schema.org",
            "@type": "ProductFeed",
            "seller": self.seller_id,
            "generated_at": time.time(),
            "total_products": len(products),
            "included_products": len(feed_items),
            "excluded_products": len(errors),
            "average_completeness": round(avg_score, 1),
            "items": feed_items,
            "errors": errors,
        }

        return feed

    def publish_feed(self, feed: dict) -> dict:
        """Publish the feed and register/update on GreenHelix marketplace."""
        # Update service registration with feed metadata
        result = self.client.execute("register_service", {
            "name": f"{self.seller_id} Product Feed",
            "description": (
                f"Structured product feed: {feed['included_products']} products, "
                f"{feed['average_completeness']}% avg completeness. "
                f"Updated {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}."
            ),
            "endpoint": f"https://{self.seller_id}.example.com/feed.json",
            "price": 0.0,
            "tags": ["product-feed", "structured-data", "real-time-inventory"],
            "category": "product_catalog",
        })
        return result


# Generate and publish
feed_gen = ProductFeedGenerator(client, seller_id="precision-parts")
feed = feed_gen.generate_feed([product_data])
print(f"Feed: {feed['included_products']} products, {feed['average_completeness']}% avg completeness")
print(f"Excluded: {len(feed['errors'])} products below threshold")

# Publish to marketplace
feed_gen.publish_feed(feed)
```

### Variant Handling

Products with variants (sizes, colors, configurations) are a common source of completeness failures. Each variant must be a distinct feed item with its own SKU, attributes, and inventory count.

```python
def expand_variants(base_product: dict, variants: list[dict]) -> list[dict]:
    """Expand a base product into variant-specific feed items.

    Each variant overrides specific attributes of the base product
    and gets its own SKU.
    """
    expanded = []
    for variant in variants:
        item = {**base_product}
        item["attributes"] = {**base_product.get("attributes", {})}

        # Override with variant-specific values
        for key, value in variant.items():
            if key in ("sku_suffix", "variant_label"):
                continue
            if key in ("attributes",):
                item["attributes"].update(value)
            else:
                item[key] = value

        # Generate variant SKU
        item["sku"] = f"{base_product['sku']}-{variant.get('sku_suffix', 'V')}"
        item["name"] = f"{base_product['name']} - {variant.get('variant_label', '')}"

        expanded.append(item)

    return expanded


# Example: bearing with size variants
size_variants = [
    {"sku_suffix": "8MM", "variant_label": "8mm Bore", "price": 4.75, "inventory": 24500,
     "attributes": {"bore_diameter_mm": "8", "outer_diameter_mm": "22", "width_mm": "7"}},
    {"sku_suffix": "10MM", "variant_label": "10mm Bore", "price": 5.25, "inventory": 18200,
     "attributes": {"bore_diameter_mm": "10", "outer_diameter_mm": "26", "width_mm": "8"}},
    {"sku_suffix": "12MM", "variant_label": "12mm Bore", "price": 6.50, "inventory": 9800,
     "attributes": {"bore_diameter_mm": "12", "outer_diameter_mm": "32", "width_mm": "10"}},
]

all_variants = expand_variants(product_data, size_variants)
print(f"Generated {len(all_variants)} variant SKUs from 1 base product")
```

> **Key Takeaways**
>
> - Attribute completeness follows a step function: 99.9% completeness delivers 3-4x the AI agent visibility of 90% completeness. The last few percent matter most.
> - Build automated completeness scoring into your product data pipeline. Flag any product below 95% for enrichment before it enters the feed.
> - Machine-readable pricing rules (volume discounts, tier breakpoints, accepted currencies) let agents calculate total cost without human intervention.
> - Real-time inventory webhooks via GreenHelix `publish_event` prevent stale-data checkout failures that destroy trust scores.
> - Every product variant needs its own SKU, attributes, and inventory count. Do not collapse variants into a single listing.

---

## Chapter 5: Agent Discovery via GreenHelix Marketplace

### The Discovery Problem

You built the storefront. Your product feeds score 99.5% completeness. Your checkout handles four payment protocols. But none of it matters if agents cannot find you.

The GreenHelix Marketplace solves this with three tools that form the discovery pipeline:

1. **`register_service`** -- List your service with structured metadata, tags, and pricing.
2. **`search_services`** -- Agents query the marketplace with natural language or structured filters.
3. **`best_match`** -- Returns the single highest-ranked service for a query, factoring in relevance, trust score, ratings, and response time.

The ranking algorithm behind `best_match` weights five signals:

| Signal | Weight | How to Optimize |
|---|---|---|
| **Query relevance** | 35% | Match your service description to likely agent queries. Use specific, attribute-rich descriptions. |
| **Trust score** | 25% | Build trust with `submit_metrics` and `build_claim_chain`. Verified performance data outweighs self-reported claims. |
| **Service rating** | 20% | Deliver quality consistently. Ratings come from `rate_service` calls by buyer agents post-transaction. |
| **Response time** | 10% | Keep your endpoint fast. The marketplace tracks latency from health checks. Under 200ms is competitive. |
| **Price competitiveness** | 10% | Priced reasonably relative to comparable services. Not necessarily cheapest -- value-adjusted. |

### Full Registration Walkthrough

Register a service with rich metadata that maximizes each ranking signal.

```python
import os
import time

GATEWAY_URL = os.environ.get("GREENHELIX_API_URL", "https://sandbox.greenhelix.net")

api_key = os.environ["GREENHELIX_API_KEY"]
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}


def ghx(tool: str, input_data: dict) -> dict:
    """Execute a GreenHelix tool."""
    resp = requests.post(
        f"{GATEWAY_URL}/v1",
        json={"tool": tool, "input": input_data},
        headers=headers,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


# Step 1: Register your agent identity
agent_registration = ghx("register_agent", {
    "agent_id": "precision-parts-agent",
    "public_key": "base64-encoded-ed25519-public-key",
    "name": "Precision Parts Direct",
})
print(f"Agent registered: {agent_registration}")

# Step 2: Create a wallet and fund it
wallet = ghx("create_wallet", {})
deposit = ghx("deposit", {"amount": "100.00"})
print(f"Wallet funded: ${deposit}")

# Step 3: Register your service on the marketplace
service = ghx("register_service", {
    "name": "Precision Parts Catalog API",
    "description": (
        "Agent-ready product catalog: 12,000+ precision-machined industrial "
        "components including bearings, shafts, seals, and fasteners. "
        "JSON-LD product schemas with 99.5% average attribute completeness. "
        "Real-time inventory via webhooks. Volume pricing with 4 discount "
        "tiers. Supports checkout via UCP, ACP, x402, and GreenHelix escrow. "
        "Average response time: 45ms. ISO 9001:2015 certified supply chain."
    ),
    "endpoint": "https://parts.example.com",
    "price": 0.0,  # Free discovery; revenue from product sales
    "tags": [
        "precision-parts", "bearings", "industrial", "b2b",
        "iso-certified", "real-time-inventory", "bulk-pricing",
        "agent-ready", "json-ld", "structured-data",
    ],
    "category": "industrial_components",
})
service_id = service.get("service_id", "")
print(f"Service registered: {service_id}")
```

### Building Trust Signals

Trust score accounts for 25% of the `best_match` ranking. Build it with two tools: `submit_metrics` (report verified performance data) and `build_claim_chain` (create a cryptographic chain of evidence linking claims to outcomes).

```python
# Step 4: Submit performance metrics
# These are verified by the gateway and contribute to your trust score.
metrics = ghx("submit_metrics", {
    "agent_id": "precision-parts-agent",
    "metrics": {
        "orders_fulfilled_30d": 1247,
        "on_time_delivery_pct": 98.6,
        "return_rate_pct": 0.3,
        "avg_response_time_ms": 45,
        "catalog_completeness_pct": 99.5,
        "active_skus": 12847,
        "escrow_completion_rate_pct": 99.8,
    },
})
print(f"Metrics submitted: {metrics}")

# Step 5: Build a claim chain
# Each claim links to verifiable evidence. The chain is cryptographically
# signed and can be independently verified by any agent.
claim_chain = ghx("build_claim_chain", {
    "agent_id": "precision-parts-agent",
    "claims": [
        {
            "claim_type": "certification",
            "claim_value": "ISO 9001:2015",
            "evidence_url": "https://parts.example.com/certs/iso9001.pdf",
        },
        {
            "claim_type": "performance",
            "claim_value": "98.6% on-time delivery (30-day rolling)",
            "evidence_url": "https://parts.example.com/metrics/delivery",
        },
        {
            "claim_type": "catalog",
            "claim_value": "12,847 active SKUs with 99.5% completeness",
            "evidence_url": "https://parts.example.com/feed.json",
        },
    ],
})
print(f"Claim chain built: {claim_chain}")

# Step 6: Check your trust score
trust = ghx("get_trust_score", {
    "agent_id": "precision-parts-agent",
})
print(f"Trust score: {trust}")
```

### Optimizing for search_services and best_match

When a buyer agent calls `search_services`, the marketplace performs semantic search against service descriptions. When it calls `best_match`, it adds ranking signals. Optimize for both.

```python
# How buyer agents find you:

# Broad search -- returns multiple results ranked by relevance
search_results = ghx("search_services", {
    "query": "precision bearings with ISO certification and bulk pricing",
})
print(f"Search returned {len(search_results.get('services', []))} results")

# Best match -- returns the single top-ranked service
top_result = ghx("best_match", {
    "query": "ABEC-7 ball bearings with real-time inventory API",
})
print(f"Best match: {top_result}")

# Verify your ranking by checking trust score and reputation
reputation = ghx("get_agent_reputation", {
    "agent_id": "precision-parts-agent",
})
print(f"Reputation: {reputation}")
```

### The Description Optimization Checklist

Your service description is the single most impactful field for `search_services` ranking. Treat it like SEO for agents.

| Element | Include? | Example |
|---|---|---|
| Product count | Yes | "12,000+ precision-machined components" |
| Product categories | Yes | "bearings, shafts, seals, fasteners" |
| Data quality signal | Yes | "99.5% average attribute completeness" |
| Data format | Yes | "JSON-LD product schemas" |
| Real-time capabilities | Yes | "Real-time inventory via webhooks" |
| Pricing structure | Yes | "Volume pricing with 4 discount tiers" |
| Payment protocols | Yes | "UCP, ACP, x402, GreenHelix escrow" |
| Performance metric | Yes | "Average response time: 45ms" |
| Certifications | Yes | "ISO 9001:2015 certified supply chain" |
| Vague marketing copy | No | "World-class quality" (meaningless to agents) |

Every keyword in your description is a potential match for an agent query. Be specific, quantitative, and structured.

> **Key Takeaways**
>
> - The GreenHelix marketplace uses five ranking signals: query relevance (35%), trust score (25%), ratings (20%), response time (10%), and price competitiveness (10%).
> - `register_service` with a rich, keyword-dense description is the foundation. Include product count, categories, data quality metrics, payment protocols, and performance numbers.
> - Trust signals from `submit_metrics` and `build_claim_chain` account for 25% of ranking. Cryptographic claim chains are more credible than self-reported descriptions.
> - Optimize your description like SEO for agents: specific, quantitative, structured. Avoid vague marketing language that agents cannot parse.
> - Cross-reference P4 (Commerce Toolkit) for the full `AgentCommerce` class and P18 (Pricing & Monetization) for marketplace listing economics.

---

## Chapter 6: Agent-to-Agent Payment Flows

### Payment Primitives

The GreenHelix gateway provides five payment primitives that cover the full lifecycle of agent-to-agent commerce:

| Primitive | Tool | Purpose |
|---|---|---|
| **Escrow** | `create_escrow` / `release_escrow` / `cancel_escrow` | Lock funds until work is verified. The core trust mechanism. |
| **Performance Escrow** | `create_performance_escrow` / `check_performance_escrow` | Auto-release when measurable metrics exceed a threshold. |
| **Subscription** | `create_subscription` / `cancel_subscription` | Recurring payments for ongoing services. |
| **Deposit** | `deposit` / `get_balance` | Fund agent wallets for payment capability. |
| **Dispute** | `create_dispute` / `resolve_dispute` | Structured disagreement resolution with evidence. |

### Escrow-Protected Product Purchases

The most common pattern: a buyer agent locks funds in escrow, the seller fulfills the order, and the buyer releases payment on delivery confirmation.

```python
import os
import time

api_key = os.environ["GREENHELIX_API_KEY"]
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}


def ghx(tool: str, input_data: dict) -> dict:
    resp = requests.post(
        f"{GATEWAY_URL}/v1",
        json={"tool": tool, "input": input_data},
        headers=headers,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


class EscrowCheckout:
    """Manage escrow-protected product purchases."""

    def __init__(self, buyer_id: str, seller_id: str):
        self.buyer_id = buyer_id
        self.seller_id = seller_id

    def create_order(self, items: list[dict], total: float) -> dict:
        """Create an escrow-backed order."""
        # Step 1: Verify buyer has sufficient balance
        balance = ghx("get_balance", {})
        available = float(balance.get("balance", "0"))
        if available < total:
            return {"error": f"Insufficient balance: ${available} < ${total}"}

        # Step 2: Create escrow
        escrow = ghx("create_escrow", {
            "payer_agent_id": self.buyer_id,
            "payee_agent_id": self.seller_id,
            "amount": str(total),
            "description": (
                f"Product order: {len(items)} items. "
                f"SKUs: {', '.join(i['sku'] for i in items)}"
            ),
        })

        return {
            "order_id": escrow.get("escrow_id"),
            "status": "escrow_locked",
            "amount": str(total),
            "items": items,
        }

    def confirm_delivery(self, escrow_id: str) -> dict:
        """Buyer confirms delivery -- release funds to seller."""
        release = ghx("release_escrow", {"escrow_id": escrow_id})
        return {
            "escrow_id": escrow_id,
            "status": "payment_released",
            "result": release,
        }

    def cancel_order(self, escrow_id: str) -> dict:
        """Cancel the order -- return funds to buyer."""
        cancel = ghx("cancel_escrow", {"escrow_id": escrow_id})
        return {
            "escrow_id": escrow_id,
            "status": "order_cancelled",
            "result": cancel,
        }


# Full purchase flow
checkout = EscrowCheckout(
    buyer_id="buyer-agent-007",
    seller_id="precision-parts-agent",
)

# Place order
order = checkout.create_order(
    items=[
        {"sku": "PBB-608-2RS-ABEC7", "quantity": 100, "unit_price": 4.28},
        {"sku": "PBB-608-2RS-ABEC7-10MM", "quantity": 50, "unit_price": 4.73},
    ],
    total=664.50,
)
print(f"Order placed: {order}")

# ... seller ships, buyer receives ...

# Confirm delivery and release payment
if order.get("order_id"):
    result = checkout.confirm_delivery(order["order_id"])
    print(f"Payment released: {result}")
```

### Performance-Gated Payments

For services where quality is measurable, performance escrow auto-releases when metrics exceed agreed thresholds. No manual release needed.

```python
# Create performance escrow for a data enrichment service
# Funds release automatically when accuracy exceeds 95%
perf_escrow = ghx("create_performance_escrow", {
    "payer_agent_id": "buyer-agent-007",
    "payee_agent_id": "enrichment-service-agent",
    "amount": "500.00",
    "currency": "USD",
    "performance_criteria": {
        "min_accuracy": 0.95,
        "min_records_processed": 10000,
    },
    "evaluation_period_days": 7,
})
perf_escrow_id = perf_escrow.get("escrow_id", "")
print(f"Performance escrow created: {perf_escrow_id}")

# After the service runs, check if criteria are met
check = ghx("check_performance_escrow", {
    "escrow_id": perf_escrow_id,
})
print(f"Performance check: {check}")
# If criteria met → funds auto-release to seller
# If not met within evaluation period → funds return to buyer
```

### Subscription Billing

For ongoing services -- monitoring, data feeds, continuous enrichment -- use subscription billing. The gateway handles recurring charges automatically.

```python
# Create a monthly subscription for real-time inventory feed access
subscription = ghx("create_subscription", {
    "payer_agent_id": "buyer-agent-007",
    "payee_agent_id": "precision-parts-agent",
    "amount": "49.00",
    "interval": "monthly",
})
subscription_id = subscription.get("subscription_id", "")
print(f"Subscription created: {subscription_id}")

# Check subscription status
status = ghx("get_subscription", {
    "subscription_id": subscription_id,
})
print(f"Subscription status: {status}")

# Cancel when no longer needed
# cancel = ghx("cancel_subscription", {"subscription_id": subscription_id})
```

### Dispute Resolution

When a buyer disputes a transaction -- wrong items, quality below spec, incomplete delivery -- the dispute system provides structured resolution.

```python
class DisputeManager:
    """Handle disputes on escrow-backed transactions."""

    def open_dispute(self, escrow_id: str, reason: str, evidence: dict) -> dict:
        """Buyer opens a dispute on an active escrow."""
        dispute = ghx("create_dispute", {
            "escrow_id": escrow_id,
            "reason": reason,
            "evidence": evidence,
        })
        return dispute

    def respond_to_dispute(self, dispute_id: str, response: str, evidence: dict) -> dict:
        """Seller responds to a dispute with counter-evidence."""
        response_result = ghx("resolve_dispute", {
            "dispute_id": dispute_id,
            "resolution": response,
            "evidence": evidence,
        })
        return response_result


# Dispute flow example
disputes = DisputeManager()

# Buyer: received wrong items
dispute = disputes.open_dispute(
    escrow_id="esc_abc123",
    reason="Received ABEC-5 bearings instead of ABEC-7 as ordered",
    evidence={
        "order_sku": "PBB-608-2RS-ABEC7",
        "received_sku": "PBB-608-2RS-ABEC5",
        "inspection_report_url": "https://buyer.example.com/reports/inspection_123.pdf",
        "photo_urls": [
            "https://buyer.example.com/photos/label_mismatch_1.jpg",
            "https://buyer.example.com/photos/label_mismatch_2.jpg",
        ],
    },
)
print(f"Dispute opened: {dispute}")

# Seller: respond with resolution (e.g., reshipping correct items)
resolution = disputes.respond_to_dispute(
    dispute_id=dispute.get("dispute_id", ""),
    response="Acknowledged. Reshipping correct ABEC-7 bearings. Tracking: FDX-789456.",
    evidence={
        "reshipment_tracking": "FDX-789456",
        "correct_sku_confirmed": "PBB-608-2RS-ABEC7",
        "estimated_delivery": "2026-04-09",
    },
)
print(f"Dispute resolved: {resolution}")
```

### Deposit Management

Before an agent can participate in escrow or subscriptions, it needs a funded wallet. Manage deposits programmatically.

```python
def ensure_funded(agent_id: str, minimum_balance: float) -> dict:
    """Ensure agent wallet has sufficient funds, topping up if needed."""
    balance = ghx("get_balance", {})
    current = float(balance.get("balance", "0"))

    if current >= minimum_balance:
        return {
            "status": "sufficient",
            "balance": str(current),
            "agent_id": agent_id,
        }

    # Top up to 2x the minimum for buffer
    top_up_amount = (minimum_balance * 2) - current
    deposit_result = ghx("deposit", {"amount": str(round(top_up_amount, 2))})

    return {
        "status": "topped_up",
        "previous_balance": str(current),
        "deposited": str(round(top_up_amount, 2)),
        "new_balance": str(current + top_up_amount),
        "agent_id": agent_id,
    }


# Ensure buyer has enough for a $664.50 order
funding = ensure_funded("buyer-agent-007", minimum_balance=664.50)
print(f"Wallet status: {funding}")
```

> **Key Takeaways**
>
> - Escrow is the core payment primitive for agent-to-agent commerce. It eliminates the trust problem: funds lock until work is verified.
> - Performance escrow automates release based on measurable metrics -- ideal for data processing, enrichment, and any service with quantifiable quality.
> - Subscription billing handles recurring service access with automatic charges at configurable intervals.
> - The dispute system provides structured resolution with evidence submission from both parties. Dispute outcomes affect trust scores.
> - Always verify wallet balance before creating escrow. Use the `ensure_funded` pattern to top up automatically.
> - Cross-reference P4 (Commerce Toolkit) for split payment patterns and P19 (Payment Rails Playbook) for multi-rail settlement.

---

## Chapter 7: Testing Agent Discoverability

### Why You Need an Agent Simulator

Your storefront is live. Your product feed scores 99.5%. Your marketplace listing is registered. But how do you know an actual AI agent will find you, parse your data correctly, and complete checkout?

You cannot wait for production traffic to find out. You need an agent simulator -- a test harness that mimics how Gemini, ChatGPT, Perplexity, and Claude shopping agents discover, evaluate, and purchase from storefronts. The simulator queries your endpoints, validates structured data, measures response latency, and produces an Agent Readiness Index (ARI) score.

### The Agent Readiness Index

The ARI score grades your storefront across five dimensions:

| Dimension | Weight | What It Measures | Target |
|---|---|---|---|
| **Discoverability** | 25% | Can agents find your manifest and OpenAPI spec? | 100% |
| **Data Quality** | 30% | Attribute completeness, schema validity, pricing structure | > 99% |
| **Marketplace Ranking** | 20% | Position in `search_services` and `best_match` results | Top 3 |
| **Checkout Completeness** | 15% | Can agents initiate checkout via all advertised protocols? | All protocols work |
| **Response Performance** | 10% | Endpoint latency under load | < 200ms p95 |

### Building the Agent Simulator

```python
import requests
import time
import json
from dataclasses import dataclass, field
from typing import Optional

GATEWAY_URL = os.environ.get("GREENHELIX_API_URL", "https://sandbox.greenhelix.net")


@dataclass
class TestResult:
    dimension: str
    test_name: str
    passed: bool
    score: float  # 0.0 to 1.0
    latency_ms: float
    details: str = ""


@dataclass
class ARIReport:
    overall_score: float = 0.0
    grade: str = ""
    results: list[TestResult] = field(default_factory=list)
    recommendations: list[str] = field(default_factory=list)


class AgentSimulator:
    """Simulate AI shopping agent behavior to test storefront readiness."""

    def __init__(
        self,
        api_key: str,
        storefront_url: str,
        service_query: str,
    ):
        self.api_key = api_key
        self.storefront_url = storefront_url
        self.service_query = service_query
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
        self.results: list[TestResult] = []

    def _ghx(self, tool: str, input_data: dict) -> dict:
        resp = requests.post(
            f"{GATEWAY_URL}/v1",
            json={"tool": tool, "input": input_data},
            headers=self.headers,
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    def _timed_get(self, url: str) -> tuple[Optional[dict], float]:
        """GET a URL and return (parsed_json, latency_ms)."""
        start = time.time()
        try:
            resp = requests.get(url, timeout=10)
            latency = (time.time() - start) * 1000
            if resp.status_code == 200:
                return resp.json(), latency
            return None, latency
        except Exception:
            return None, (time.time() - start) * 1000

    # ── Discoverability Tests ──────────────────────────────────

    def test_manifest(self) -> TestResult:
        """Test: Can agents find .well-known/ai-plugin.json?"""
        url = f"{self.storefront_url}/.well-known/ai-plugin.json"
        data, latency = self._timed_get(url)

        if data and "name_for_model" in data and "api" in data:
            has_description = bool(data.get("description_for_model", ""))
            has_api_url = bool(data.get("api", {}).get("url", ""))
            score = 1.0 if (has_description and has_api_url) else 0.7
            result = TestResult(
                dimension="discoverability",
                test_name="ai_plugin_manifest",
                passed=True,
                score=score,
                latency_ms=latency,
                details=f"Manifest found. description_for_model: {has_description}, api.url: {has_api_url}",
            )
        else:
            result = TestResult(
                dimension="discoverability",
                test_name="ai_plugin_manifest",
                passed=False,
                score=0.0,
                latency_ms=latency,
                details="Manifest missing or malformed",
            )

        self.results.append(result)
        return result

    def test_openapi_spec(self) -> TestResult:
        """Test: Is the OpenAPI spec reachable and valid?"""
        # First get the manifest to find the OpenAPI URL
        manifest_url = f"{self.storefront_url}/.well-known/ai-plugin.json"
        manifest, _ = self._timed_get(manifest_url)

        if not manifest:
            result = TestResult(
                dimension="discoverability",
                test_name="openapi_spec",
                passed=False,
                score=0.0,
                latency_ms=0,
                details="Cannot test: manifest not found",
            )
            self.results.append(result)
            return result

        api_url = manifest.get("api", {}).get("url", "")
        if not api_url:
            result = TestResult(
                dimension="discoverability",
                test_name="openapi_spec",
                passed=False,
                score=0.0,
                latency_ms=0,
                details="No api.url in manifest",
            )
            self.results.append(result)
            return result

        data, latency = self._timed_get(api_url)
        has_paths = bool(data and data.get("paths"))
        has_info = bool(data and data.get("info"))

        result = TestResult(
            dimension="discoverability",
            test_name="openapi_spec",
            passed=bool(has_paths and has_info),
            score=1.0 if (has_paths and has_info) else 0.0,
            latency_ms=latency,
            details=f"OpenAPI spec: paths={has_paths}, info={has_info}",
        )
        self.results.append(result)
        return result

    # ── Marketplace Tests ──────────────────────────────────────

    def test_search_visibility(self) -> TestResult:
        """Test: Does your service appear in search_services results?"""
        start = time.time()
        results = self._ghx("search_services", {
            "query": self.service_query,
        })
        latency = (time.time() - start) * 1000

        services = results.get("services", [])
        found = any(
            self.storefront_url in str(s)
            for s in services
        )

        # Score based on position
        position = -1
        for i, s in enumerate(services):
            if self.storefront_url in str(s):
                position = i
                break

        if position == 0:
            score = 1.0
        elif position in (1, 2):
            score = 0.8
        elif position >= 0:
            score = 0.5
        else:
            score = 0.0

        result = TestResult(
            dimension="marketplace",
            test_name="search_visibility",
            passed=found,
            score=score,
            latency_ms=latency,
            details=f"Position in search results: {position if position >= 0 else 'not found'}. Total results: {len(services)}",
        )
        self.results.append(result)
        return result

    def test_best_match(self) -> TestResult:
        """Test: Are you the best_match for your target query?"""
        start = time.time()
        match = self._ghx("best_match", {
            "query": self.service_query,
        })
        latency = (time.time() - start) * 1000

        is_top = self.storefront_url in str(match)

        result = TestResult(
            dimension="marketplace",
            test_name="best_match_ranking",
            passed=is_top,
            score=1.0 if is_top else 0.0,
            latency_ms=latency,
            details=f"Top match: {'Yes' if is_top else 'No'}. Result: {json.dumps(match)[:200]}",
        )
        self.results.append(result)
        return result

    # ── Data Quality Tests ─────────────────────────────────────

    def test_product_schema(self) -> TestResult:
        """Test: Do product search results return valid JSON-LD schemas?"""
        search_url = f"{self.storefront_url}/products/search"
        start = time.time()
        try:
            resp = requests.post(
                search_url,
                json={"query": "", "limit": 5},
                timeout=10,
            )
            latency = (time.time() - start) * 1000
            data = resp.json()
        except Exception:
            latency = (time.time() - start) * 1000
            result = TestResult(
                dimension="data_quality",
                test_name="product_schema_validity",
                passed=False,
                score=0.0,
                latency_ms=latency,
                details="Product search endpoint unreachable",
            )
            self.results.append(result)
            return result

        products = data.get("results", [])
        valid_count = 0
        for p in products:
            has_context = "@context" in p
            has_type = "@type" in p
            has_offers = "offers" in p
            has_properties = "additionalProperty" in p
            if all([has_context, has_type, has_offers, has_properties]):
                valid_count += 1

        score = valid_count / len(products) if products else 0.0

        result = TestResult(
            dimension="data_quality",
            test_name="product_schema_validity",
            passed=score >= 0.9,
            score=score,
            latency_ms=latency,
            details=f"{valid_count}/{len(products)} products have valid JSON-LD schemas",
        )
        self.results.append(result)
        return result

    # ── Checkout Tests ─────────────────────────────────────────

    def test_checkout_protocols(self) -> TestResult:
        """Test: Can checkout be initiated for each advertised protocol?"""
        checkout_url = f"{self.storefront_url}/checkout/initiate"
        protocols = ["ucp", "acp", "x402", "greenhelix_escrow"]
        working = []

        start = time.time()
        for protocol in protocols:
            try:
                resp = requests.post(
                    checkout_url,
                    json={
                        "items": [{"sku": "TEST-SKU", "quantity": 1}],
                        "payment_protocol": protocol,
                        "buyer_agent_id": "test-simulator",
                    },
                    timeout=10,
                )
                if resp.status_code in (200, 201, 402):
                    working.append(protocol)
            except Exception:
                pass
        latency = (time.time() - start) * 1000

        score = len(working) / len(protocols)
        result = TestResult(
            dimension="checkout",
            test_name="protocol_support",
            passed=score >= 0.75,
            score=score,
            latency_ms=latency,
            details=f"Working protocols: {working}. Missing: {set(protocols) - set(working)}",
        )
        self.results.append(result)
        return result

    # ── Performance Tests ──────────────────────────────────────

    def test_response_latency(self, num_requests: int = 10) -> TestResult:
        """Test: Are endpoints fast enough for agent real-time queries?"""
        search_url = f"{self.storefront_url}/products/search"
        latencies = []

        for _ in range(num_requests):
            start = time.time()
            try:
                requests.post(
                    search_url,
                    json={"query": "bearing", "limit": 5},
                    timeout=10,
                )
                latencies.append((time.time() - start) * 1000)
            except Exception:
                latencies.append(10000)  # penalty for failures

        if not latencies:
            result = TestResult(
                dimension="performance",
                test_name="response_latency",
                passed=False,
                score=0.0,
                latency_ms=0,
                details="No successful requests",
            )
            self.results.append(result)
            return result

        latencies.sort()
        p50 = latencies[len(latencies) // 2]
        p95 = latencies[int(len(latencies) * 0.95)]
        avg = sum(latencies) / len(latencies)

        # Score: 1.0 if p95 < 200ms, 0.5 if < 500ms, 0.0 if > 1000ms
        if p95 < 200:
            score = 1.0
        elif p95 < 500:
            score = 0.5
        else:
            score = 0.0

        result = TestResult(
            dimension="performance",
            test_name="response_latency",
            passed=p95 < 200,
            score=score,
            latency_ms=p95,
            details=f"p50={p50:.0f}ms, p95={p95:.0f}ms, avg={avg:.0f}ms ({num_requests} requests)",
        )
        self.results.append(result)
        return result

    # ── Report Generation ──────────────────────────────────────

    def run_all(self) -> ARIReport:
        """Run all tests and generate an ARI report."""
        self.results = []

        # Run all test suites
        self.test_manifest()
        self.test_openapi_spec()
        self.test_search_visibility()
        self.test_best_match()
        self.test_product_schema()
        self.test_checkout_protocols()
        self.test_response_latency()

        # Calculate weighted score
        weights = {
            "discoverability": 0.25,
            "marketplace": 0.20,
            "data_quality": 0.30,
            "checkout": 0.15,
            "performance": 0.10,
        }

        dimension_scores = {}
        for r in self.results:
            if r.dimension not in dimension_scores:
                dimension_scores[r.dimension] = []
            dimension_scores[r.dimension].append(r.score)

        weighted_total = 0.0
        for dim, scores in dimension_scores.items():
            avg = sum(scores) / len(scores) if scores else 0.0
            weight = weights.get(dim, 0.1)
            weighted_total += avg * weight

        overall = round(weighted_total * 100, 1)

        # Grade
        if overall >= 90:
            grade = "A"
        elif overall >= 80:
            grade = "B"
        elif overall >= 70:
            grade = "C"
        elif overall >= 60:
            grade = "D"
        else:
            grade = "F"

        # Recommendations
        recs = []
        for r in self.results:
            if not r.passed:
                if r.test_name == "ai_plugin_manifest":
                    recs.append("Add .well-known/ai-plugin.json with description_for_model and api.url")
                elif r.test_name == "openapi_spec":
                    recs.append("Publish a valid OpenAPI spec at the URL specified in your manifest")
                elif r.test_name == "search_visibility":
                    recs.append("Optimize your register_service description with specific keywords")
                elif r.test_name == "best_match_ranking":
                    recs.append("Build trust signals with submit_metrics and build_claim_chain")
                elif r.test_name == "product_schema_validity":
                    recs.append("Ensure all products have @context, @type, offers, and additionalProperty")
                elif r.test_name == "protocol_support":
                    recs.append("Implement all advertised checkout protocols")
                elif r.test_name == "response_latency":
                    recs.append("Reduce p95 latency below 200ms -- add caching or optimize queries")

        return ARIReport(
            overall_score=overall,
            grade=grade,
            results=self.results,
            recommendations=recs,
        )


# Run the simulator
simulator = AgentSimulator(
    api_key=os.environ["GREENHELIX_API_KEY"],
    storefront_url="https://parts.example.com",
    service_query="precision bearings with ISO certification",
)

report = simulator.run_all()
print(f"\n{'='*50}")
print(f"AGENT READINESS INDEX: {report.overall_score}% (Grade: {report.grade})")
print(f"{'='*50}")

for r in report.results:
    status = "PASS" if r.passed else "FAIL"
    print(f"  [{status}] {r.dimension}/{r.test_name}: {r.score:.0%} ({r.latency_ms:.0f}ms)")
    if r.details:
        print(f"         {r.details}")

if report.recommendations:
    print(f"\nRecommendations:")
    for i, rec in enumerate(report.recommendations, 1):
        print(f"  {i}. {rec}")
```

### Interpreting ARI Scores

| Score | Grade | Interpretation | Action |
|---|---|---|---|
| 90-100 | A | Agent-ready. Agents can discover, evaluate, and purchase from your storefront. | Monitor and maintain. |
| 80-89 | B | Mostly ready. One or two gaps reducing visibility or conversion. | Fix specific failures. |
| 70-79 | C | Functional but underperforming. Missing trust signals or incomplete schemas. | Prioritize data quality and marketplace optimization. |
| 60-69 | D | Significant gaps. Agents can find you but struggle to complete purchases. | Full audit needed. Use the 14-Day Sprint (Chapter 8). |
| < 60 | F | Not agent-ready. Most agents will skip your storefront entirely. | Start from Chapter 2 and implement systematically. |

### Continuous Monitoring

Run the simulator on a schedule -- daily or on every deployment -- and track your ARI score over time. Publish the results as metrics on GreenHelix to reinforce your trust score.

```python
def publish_ari_as_metrics(report: ARIReport):
    """Publish ARI results as GreenHelix metrics for trust scoring."""
    dimension_scores = {}
    for r in report.results:
        if r.dimension not in dimension_scores:
            dimension_scores[r.dimension] = []
        dimension_scores[r.dimension].append(r.score)

    metrics = {
        "ari_overall_score": report.overall_score,
        "ari_grade": report.grade,
    }
    for dim, scores in dimension_scores.items():
        avg = sum(scores) / len(scores) if scores else 0
        metrics[f"ari_{dim}_score"] = round(avg * 100, 1)

    ghx("submit_metrics", {
        "agent_id": "precision-parts-agent",
        "metrics": metrics,
    })
    print(f"ARI metrics published to GreenHelix")


publish_ari_as_metrics(report)
```

> **Key Takeaways**
>
> - Build an agent simulator that tests five dimensions: discoverability, data quality, marketplace ranking, checkout completeness, and response performance.
> - The Agent Readiness Index (ARI) provides a single score (0-100) and letter grade for your storefront's agent compatibility. Target 90+ (Grade A).
> - Run the simulator on every deployment and track ARI over time. Regressions in structured data or latency directly reduce agent-referred revenue.
> - Publish ARI scores as GreenHelix metrics via `submit_metrics` to reinforce your trust score and marketplace ranking.
> - The simulator catches problems before production agents do -- a schema regression caught in CI is free; a schema regression caught by a lost sale costs revenue.

---

## Chapter 8: The 14-Day ACO Sprint

### Overview

The Agent Commerce Optimization (ACO) Sprint is a 14-day execution plan that takes your storefront from zero agent readiness to production-grade discoverability. Each day has specific deliverables, measurable checkpoints, and code tasks. By day 14, your ARI score should be 85+ with a clear path to 95+.

### Days 1-2: Audit Product Data

**Objective**: Assess current product data quality and identify gaps.

**Day 1 Tasks**:

- [ ] Export your full product catalog to a structured format (JSON or CSV)
- [ ] Run the completeness scoring function from Chapter 4 against every product
- [ ] Generate a gap report: which products are below 95% completeness?
- [ ] Identify the 10 most common missing attributes across your catalog

**Day 2 Tasks**:

- [ ] Prioritize products by revenue contribution -- fix the top 20% first (they drive 80% of revenue)
- [ ] Fill in missing required attributes for all top-revenue products
- [ ] Set up automated completeness scoring in your CI/CD pipeline
- [ ] Target: all top-revenue products at 98%+ completeness

```python
# Day 1-2: Catalog audit script
import json


def audit_catalog(products: list[dict], category: str) -> dict:
    """Audit an entire product catalog for agent readiness."""
    results = {
        "total_products": len(products),
        "above_99": 0,
        "above_95": 0,
        "above_90": 0,
        "below_90": 0,
        "most_common_missing": {},
        "products_to_fix": [],
    }

    for product in products:
        report = score_completeness(product, category)

        if report.score >= 99.0:
            results["above_99"] += 1
        elif report.score >= 95.0:
            results["above_95"] += 1
        elif report.score >= 90.0:
            results["above_90"] += 1
        else:
            results["below_90"] += 1
            results["products_to_fix"].append({
                "sku": report.sku,
                "score": report.score,
                "missing": report.missing[:5],
            })

        for m in report.missing:
            attr = m.split("] ")[1] if "] " in m else m
            results["most_common_missing"][attr] = (
                results["most_common_missing"].get(attr, 0) + 1
            )

    # Sort most common missing by frequency
    results["most_common_missing"] = dict(
        sorted(
            results["most_common_missing"].items(),
            key=lambda x: x[1],
            reverse=True,
        )[:10]
    )

    return results


# Run the audit
# audit = audit_catalog(all_products, "industrial_components")
# print(json.dumps(audit, indent=2))
```

### Days 3-5: Implement Manifests and Schemas

**Objective**: Deploy the three layers of agent discoverability.

**Day 3 Tasks**:

- [ ] Create `.well-known/ai-plugin.json` manifest (Chapter 2, Layer 1)
- [ ] Write `description_for_model` optimized for your top 5 search queries
- [ ] Deploy manifest to production and verify with `curl`

**Day 4 Tasks**:

- [ ] Implement JSON-LD product schemas using `build_product_schema()` (Chapter 2, Layer 2)
- [ ] Add schemas to all product pages (embed in HTML) and as API responses
- [ ] Validate schemas with Google's Rich Results Test

**Day 5 Tasks**:

- [ ] Publish OpenAPI spec at the URL referenced in your manifest (Chapter 2, Layer 3)
- [ ] Include `/products/search`, `/products/{sku}/inventory`, and `/checkout/initiate` endpoints
- [ ] Test with an OpenAPI validator (e.g., `openapi-spec-validator` Python package)
- [ ] Run ARI discoverability tests -- target 100%

```python
# Day 3-5: Verify all three layers are deployed
def verify_storefront_layers(base_url: str) -> dict:
    """Verify all three agent-readiness layers are deployed."""
    checks = {}

    # Layer 1: Manifest
    try:
        resp = requests.get(f"{base_url}/.well-known/ai-plugin.json", timeout=5)
        manifest = resp.json()
        checks["manifest"] = {
            "deployed": resp.status_code == 200,
            "has_model_description": bool(manifest.get("description_for_model")),
            "has_api_url": bool(manifest.get("api", {}).get("url")),
        }
    except Exception as e:
        checks["manifest"] = {"deployed": False, "error": str(e)}

    # Layer 2: Product schemas (check search endpoint)
    try:
        resp = requests.post(
            f"{base_url}/products/search",
            json={"query": "", "limit": 1},
            timeout=5,
        )
        results = resp.json().get("results", [])
        if results:
            has_jsonld = "@context" in results[0] and "@type" in results[0]
            checks["schemas"] = {"deployed": True, "valid_jsonld": has_jsonld}
        else:
            checks["schemas"] = {"deployed": True, "valid_jsonld": False, "note": "No results"}
    except Exception as e:
        checks["schemas"] = {"deployed": False, "error": str(e)}

    # Layer 3: OpenAPI spec
    api_url = checks.get("manifest", {}).get("has_api_url")
    if api_url and checks.get("manifest", {}).get("deployed"):
        try:
            manifest_resp = requests.get(f"{base_url}/.well-known/ai-plugin.json")
            api_spec_url = manifest_resp.json().get("api", {}).get("url", "")
            spec_resp = requests.get(api_spec_url, timeout=5)
            checks["openapi"] = {
                "deployed": spec_resp.status_code == 200,
                "has_paths": "paths" in spec_resp.text,
            }
        except Exception as e:
            checks["openapi"] = {"deployed": False, "error": str(e)}
    else:
        checks["openapi"] = {"deployed": False, "note": "No api.url in manifest"}

    return checks


# verify = verify_storefront_layers("https://parts.example.com")
# print(json.dumps(verify, indent=2))
```

### Days 6-8: Connect Payment Rails

**Objective**: Implement multi-protocol checkout.

**Day 6 Tasks**:

- [ ] Implement GreenHelix escrow checkout (`create_escrow` / `release_escrow`)
- [ ] Test escrow flow end-to-end: create, verify lock, release, verify balance
- [ ] Deploy `/checkout/initiate` endpoint with `greenhelix_escrow` support

**Day 7 Tasks**:

- [ ] Add x402 checkout flow for micropayments / digital product delivery
- [ ] Add UCP checkout flow for structured catalog purchases
- [ ] Test both flows with the agent simulator

**Day 8 Tasks**:

- [ ] Add ACP checkout flow if you have a Stripe merchant account
- [ ] Implement the `MultiProtocolCheckout` router from Chapter 3
- [ ] Run ARI checkout tests -- target all advertised protocols working
- [ ] Set up subscription billing for recurring access with `create_subscription`

```python
# Day 6-8: End-to-end checkout verification
def verify_checkout_flows(base_url: str) -> dict:
    """Verify all checkout protocols are functional."""
    protocols = ["greenhelix_escrow", "x402", "ucp", "acp"]
    results = {}

    for protocol in protocols:
        try:
            resp = requests.post(
                f"{base_url}/checkout/initiate",
                json={
                    "items": [{"sku": "TEST-VERIFY", "quantity": 1}],
                    "payment_protocol": protocol,
                    "buyer_agent_id": "checkout-verifier",
                },
                timeout=10,
            )
            results[protocol] = {
                "status_code": resp.status_code,
                "working": resp.status_code in (200, 201, 402),
                "response": resp.json() if resp.status_code < 500 else None,
            }
        except Exception as e:
            results[protocol] = {"working": False, "error": str(e)}

    return results
```

### Days 9-10: Register on Marketplaces

**Objective**: Make your storefront discoverable through the GreenHelix marketplace.

**Day 9 Tasks**:

- [ ] Register agent identity with `register_agent`
- [ ] Create and fund wallet with `create_wallet` and `deposit`
- [ ] Register service with optimized description using `register_service` (Chapter 5)
- [ ] Verify service appears in `search_services` results for your target queries

**Day 10 Tasks**:

- [ ] Submit initial performance metrics with `submit_metrics`
- [ ] Build claim chain with certifications and evidence using `build_claim_chain`
- [ ] Check trust score with `get_trust_score` -- establish baseline
- [ ] Run ARI marketplace tests -- target top 3 position for primary queries
- [ ] Verify `best_match` returns your service for at least one target query

```python
# Day 9-10: Marketplace registration and verification
def verify_marketplace_presence(service_query: str) -> dict:
    """Verify marketplace presence and ranking."""
    results = {}

    # Check search visibility
    search = ghx("search_services", {"query": service_query})
    services = search.get("services", [])
    results["search_results_count"] = len(services)
    results["appears_in_search"] = len(services) > 0

    # Check best_match
    match = ghx("best_match", {"query": service_query})
    results["best_match"] = match

    # Check trust score
    trust = ghx("get_trust_score", {
        "agent_id": "precision-parts-agent",
    })
    results["trust_score"] = trust

    return results
```

### Days 11-14: Monitoring and Iteration

**Objective**: Set up continuous monitoring, fix remaining gaps, and iterate toward ARI 95+.

**Day 11 Tasks**:

- [ ] Run full ARI assessment with the agent simulator from Chapter 7
- [ ] Document current score and grade
- [ ] Prioritize failed tests by impact (weight x gap from target)

**Day 12 Tasks**:

- [ ] Fix the top 3 highest-impact failures identified on Day 11
- [ ] Re-run ARI assessment after each fix to verify improvement
- [ ] Set up scheduled ARI monitoring (daily cron job or CI pipeline)

**Day 13 Tasks**:

- [ ] Implement inventory webhooks with `publish_event` (Chapter 4)
- [ ] Set up price change notifications
- [ ] Test webhook delivery to a subscriber agent
- [ ] Optimize endpoint latency -- add caching for frequently-queried SKUs

**Day 14 Tasks**:

- [ ] Final ARI assessment -- target 85+ overall, with a path to 95+
- [ ] Publish ARI metrics to GreenHelix via `submit_metrics`
- [ ] Document remaining gaps and create a backlog for continued optimization
- [ ] Set up alerting: notify team if ARI drops below 80

```python
# Day 14: Final assessment and metric publication
def final_aco_assessment(
    api_key: str,
    storefront_url: str,
    service_query: str,
    agent_id: str,
) -> dict:
    """Run the final ACO sprint assessment."""
    # Run full ARI
    sim = AgentSimulator(
        api_key=api_key,
        storefront_url=storefront_url,
        service_query=service_query,
    )
    report = sim.run_all()

    # Publish to GreenHelix
    ghx("submit_metrics", {
        "agent_id": agent_id,
        "metrics": {
            "ari_score": report.overall_score,
            "ari_grade": report.grade,
            "aco_sprint_completed": True,
            "aco_completion_date": time.strftime("%Y-%m-%d"),
        },
    })

    # Summary
    summary = {
        "ari_score": report.overall_score,
        "grade": report.grade,
        "tests_passed": sum(1 for r in report.results if r.passed),
        "tests_total": len(report.results),
        "recommendations": report.recommendations,
        "sprint_status": "complete" if report.overall_score >= 85 else "needs_iteration",
    }

    return summary


# final = final_aco_assessment(
#     api_key=os.environ["GREENHELIX_API_KEY"],
#     storefront_url="https://parts.example.com",
#     service_query="precision bearings ISO certified",
#     agent_id="precision-parts-agent",
# )
# print(json.dumps(final, indent=2))
```

### Printable ACO Sprint Checklist

```
ACO SPRINT CHECKLIST
====================

PHASE 1: AUDIT (Days 1-2)
[ ] Export full product catalog
[ ] Run completeness scoring on all products
[ ] Generate gap report
[ ] Identify top 10 missing attributes
[ ] Fix top-revenue products to 98%+ completeness
[ ] Set up automated scoring in CI/CD

PHASE 2: MANIFESTS & SCHEMAS (Days 3-5)
[ ] Deploy .well-known/ai-plugin.json
[ ] Write optimized description_for_model
[ ] Implement JSON-LD product schemas
[ ] Embed schemas in pages and API responses
[ ] Publish OpenAPI spec
[ ] Validate all three layers

PHASE 3: PAYMENT RAILS (Days 6-8)
[ ] Implement GreenHelix escrow checkout
[ ] Test escrow end-to-end
[ ] Add x402 micropayment flow
[ ] Add UCP checkout flow
[ ] Add ACP checkout flow (if Stripe merchant)
[ ] Deploy MultiProtocolCheckout router
[ ] Set up subscription billing

PHASE 4: MARKETPLACE (Days 9-10)
[ ] Register agent identity
[ ] Create and fund wallet
[ ] Register service with optimized description
[ ] Verify search_services visibility
[ ] Submit performance metrics
[ ] Build claim chain with evidence
[ ] Check trust score baseline
[ ] Verify best_match ranking

PHASE 5: MONITORING (Days 11-14)
[ ] Run full ARI assessment
[ ] Fix top 3 highest-impact failures
[ ] Set up daily ARI monitoring
[ ] Implement inventory webhooks
[ ] Set up price change notifications
[ ] Optimize endpoint latency (< 200ms p95)
[ ] Final ARI assessment (target: 85+)
[ ] Publish ARI metrics to GreenHelix
[ ] Document remaining gaps
[ ] Set up regression alerting (ARI < 80)

SCORE: ___/100  GRADE: ___
```

> **Key Takeaways**
>
> - The 14-day ACO sprint follows five phases: audit (days 1-2), manifests and schemas (days 3-5), payment rails (days 6-8), marketplace registration (days 9-10), and monitoring and iteration (days 11-14).
> - Target ARI 85+ by day 14. Most storefronts can reach this with focused execution on data completeness and marketplace optimization.
> - Continuous ARI monitoring catches regressions before they cost revenue. Run the agent simulator on every deployment.
> - The sprint is not a one-time event. Agent commerce standards evolve monthly. Schedule quarterly ACO refreshes to maintain competitiveness.
> - Cross-reference P4 (Commerce Toolkit) for escrow patterns, P13 (Interoperability Bridge) for protocol bridging, P18 (Pricing & Monetization) for pricing optimization, and P19 (Payment Rails Playbook) for deep protocol implementation.

---

## Appendix: Tool Reference

The following GreenHelix A2A Commerce Gateway tools are used throughout this guide. All tools are called via `POST https://sandbox.greenhelix.net/v1` with Bearer token authentication.

| Tool | Chapter(s) | Purpose |
|---|---|---|
| `register_agent` | 5, 6 | Register agent identity with Ed25519 public key |
| `create_wallet` | 5, 6 | Create a wallet for an agent |
| `deposit` | 5, 6 | Fund an agent wallet |
| `get_balance` | 6 | Check wallet balance |
| `register_service` | 2, 4, 5 | List a service on the marketplace |
| `search_services` | 5, 7 | Search marketplace for services |
| `best_match` | 5, 7 | Get highest-ranked service for a query |
| `submit_metrics` | 5, 7, 8 | Report verified performance metrics |
| `build_claim_chain` | 5, 8 | Create cryptographic evidence chain |
| `get_trust_score` | 5, 8 | Check trust score for an agent |
| `get_agent_reputation` | 5 | Get reputation details |
| `create_escrow` | 2, 3, 6 | Lock funds until work is verified |
| `release_escrow` | 6 | Release escrowed funds to seller |
| `cancel_escrow` | 6 | Cancel escrow and return funds to buyer |
| `create_performance_escrow` | 6 | Escrow with metric-based auto-release |
| `check_performance_escrow` | 6 | Check if performance criteria are met |
| `create_subscription` | 6 | Set up recurring payment |
| `cancel_subscription` | 6 | Cancel a subscription |
| `create_payment_intent` | 3 | Record payment intent for tracking |
| `create_dispute` | 6 | Open a dispute on an escrow |
| `resolve_dispute` | 6 | Resolve a dispute with evidence |
| `publish_event` | 4 | Push inventory/price events to subscribers |
| `rate_service` | 5 | Rate a marketplace service (1-5) |

---

*This guide is part of the GreenHelix A2A Commerce product library. For related guides, see P4 (Commerce Toolkit), P13 (Interoperability Bridge), P18 (Pricing & Monetization), and P19 (Payment Rails Playbook).*

