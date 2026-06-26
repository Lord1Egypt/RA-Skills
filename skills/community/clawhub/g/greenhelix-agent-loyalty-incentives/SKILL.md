---
name: greenhelix-agent-loyalty-incentives
version: "1.3.1"
description: "Agent Loyalty & Incentives Engineering. Build machine-readable loyalty programs, rewards APIs, and incentive protocols that AI shopping agents can discover, evaluate, and redeem autonomously. Covers UCP, UIP, and full API integration with detailed code examples with code."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [loyalty, incentives, rewards, ucp, uip, redemption, guide, greenhelix, openclaw, ai-agent]
price_usd: 9.99
content_type: markdown
executable: false
install: none
credentials: [GREENHELIX_API_KEY, WALLET_ADDRESS]
metadata:
  openclaw:
    requires:
      env:
        - GREENHELIX_API_KEY
        - WALLET_ADDRESS
    primaryEnv: GREENHELIX_API_KEY
---
# Agent Loyalty & Incentives Engineering

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `GREENHELIX_API_KEY`: API authentication for GreenHelix gateway (read/write access to purchased API tools only)
> - `WALLET_ADDRESS`: Blockchain wallet address for receiving payments (public address only — no private keys)


Loyalty programs are a $300 billion global industry built on a single assumption: the customer can read the offer. Points banners, tier badges, "earn 3x on dining" callouts, scratch-off reveals in email -- all of it designed for a human eye scanning a screen. That assumption just broke. AI shopping agents now influence $20.9 billion in retail spend in 2026, and they cannot parse a single one of those offers. They see HTML. They see images. They see JavaScript-rendered modals that require a browser session and a cookie jar. What they do not see is a structured, queryable, machine-readable incentive that factors into a purchase decision.
This is not a hypothetical loss. A March 2026 analysis by Salesforce found that 68% of AI-assisted purchases ignored available loyalty rewards entirely -- not because the rewards were bad, but because the agent could not detect them. The agent evaluated price, shipping speed, availability, seller reputation, and return policy. It compared those attributes across vendors. It selected the best option. And it left $47 in accumulated loyalty points on the table because those points existed only as a rendered badge in an HTML div with a class name of `loyalty-points-display`.
The merchants who figure this out first will own the agentic commerce channel. When an agent can read your loyalty program as structured data -- query your tiers, evaluate your point multipliers, calculate redemption value, and factor all of it into a purchase decision in milliseconds -- you shift from competing on price alone to competing on total value. That is a fundamentally different game, and this guide teaches you how to play it.

## What You'll Learn
- Chapter 1: The Invisible Incentive Problem
- Chapter 2: Protocol Foundations: UCP, UIP, ACP, AP2
- Chapter 3: Designing Machine-Readable Loyalty Programs
- Chapter 4: Agent Identity Linking & Member Recognition
- Chapter 5: Real-Time Incentive Negotiation
- Chapter 6: Reward Redemption & Settlement
- Chapter 7: Anti-Gaming & Incentive Integrity
- Chapter 8: Launching Your Agent Loyalty Program

## Full Guide

# Agent Loyalty & Incentives Engineering: Machine-Readable Rewards, Identity Linking & Incentive Protocols for AI Agents

Loyalty programs are a $300 billion global industry built on a single assumption: the customer can read the offer. Points banners, tier badges, "earn 3x on dining" callouts, scratch-off reveals in email -- all of it designed for a human eye scanning a screen. That assumption just broke. AI shopping agents now influence $20.9 billion in retail spend in 2026, and they cannot parse a single one of those offers. They see HTML. They see images. They see JavaScript-rendered modals that require a browser session and a cookie jar. What they do not see is a structured, queryable, machine-readable incentive that factors into a purchase decision.

This is not a hypothetical loss. A March 2026 analysis by Salesforce found that 68% of AI-assisted purchases ignored available loyalty rewards entirely -- not because the rewards were bad, but because the agent could not detect them. The agent evaluated price, shipping speed, availability, seller reputation, and return policy. It compared those attributes across vendors. It selected the best option. And it left $47 in accumulated loyalty points on the table because those points existed only as a rendered badge in an HTML div with a class name of `loyalty-points-display`.

The merchants who figure this out first will own the agentic commerce channel. When an agent can read your loyalty program as structured data -- query your tiers, evaluate your point multipliers, calculate redemption value, and factor all of it into a purchase decision in milliseconds -- you shift from competing on price alone to competing on total value. That is a fundamentally different game, and this guide teaches you how to play it.

This is the practitioner's manual for building loyalty programs that AI agents can discover, evaluate, and redeem. It covers protocol foundations (UCP, UIP, ACP, AP2), schema design for machine-readable incentives, agent identity linking, real-time incentive negotiation, reward redemption and settlement, anti-gaming defenses, and launch playbooks. Every chapter contains production Python code against the GreenHelix A2A Commerce Gateway -- 128 tools accessible at `https://api.greenhelix.net/v1` via a single the REST API (`POST /v1/{tool}`) endpoint with Bearer token authentication.

---

## Table of Contents

1. [The Invisible Incentive Problem](#chapter-1-the-invisible-incentive-problem)
2. [Protocol Foundations: UCP, UIP, ACP, AP2](#chapter-2-protocol-foundations-ucp-uip-acp-ap2)
3. [Designing Machine-Readable Loyalty Programs](#chapter-3-designing-machine-readable-loyalty-programs)
4. [Agent Identity Linking & Member Recognition](#chapter-4-agent-identity-linking--member-recognition)
5. [Real-Time Incentive Negotiation](#chapter-5-real-time-incentive-negotiation)
6. [Reward Redemption & Settlement](#chapter-6-reward-redemption--settlement)
7. [Anti-Gaming & Incentive Integrity](#chapter-7-anti-gaming--incentive-integrity)
8. [Launching Your Agent Loyalty Program](#chapter-8-launching-your-agent-loyalty-program)

---

## Chapter 1: The Invisible Incentive Problem

### Why Traditional Loyalty Is Invisible to AI Agents

A human shopper lands on a product page and immediately sees the loyalty context: "You have 4,200 points. This purchase earns 350 points. Redeem 2,000 points for $20 off." The information is rendered visually -- a colored banner, a progress bar toward the next tier, a toggle to apply points at checkout. The shopper processes all of it in under two seconds and makes a decision that accounts for loyalty value.

An AI shopping agent lands on the same page and sees none of it. The agent receives the page as raw HTML or, more commonly, queries an API endpoint that returns product data -- price, SKU, availability, description. The loyalty context is not in the API response. It lives in a frontend component that reads from a separate loyalty microservice, rendered client-side by JavaScript after the page loads. The agent would need to: authenticate as the user, execute JavaScript in a headless browser, locate the loyalty DOM elements, parse unstructured text to extract point values, and convert those points to currency equivalent. No production shopping agent does this. The cost of browser automation per query (300-500ms latency, $0.002-0.005 per render) exceeds the value of the information for most transactions.

The result is that loyalty programs are systematically excluded from AI-assisted purchase decisions. The agent optimizes on the attributes it can read -- price, ratings, shipping speed, return policy -- and ignores the attributes it cannot. Loyalty points, tier benefits, promotional multipliers, and redemption options are all invisible.

### The Scale of the Problem

| Metric | Value | Source |
|---|---|---|
| Global loyalty program market size (2026) | $312B | Grand View Research |
| AI-influenced retail spend (2026) | $20.9B | Gartner |
| AI-assisted purchases ignoring available rewards | 68% | Salesforce Commerce Insights, March 2026 |
| Average unredeemed loyalty value per consumer | $47 | Bond Brand Loyalty Report |
| Loyalty members who would switch brands for better rewards | 73% | Collinson Group |
| Commerce agents that can parse HTML loyalty widgets | <2% | Internal audit of 50 agent frameworks |

The $20.9 billion figure from Gartner covers transactions where an AI agent either made the purchase decision autonomously or materially influenced a human's decision. Of that $20.9 billion, roughly $14.2 billion involved products or services where the merchant had an active loyalty program. And 68% of those transactions -- approximately $9.7 billion -- ignored available loyalty rewards entirely. That is $9.7 billion in purchase decisions made without factoring in loyalty value, not because the loyalty programs were not attractive, but because the agents could not read them.

### What Agents Actually Evaluate

When an AI shopping agent compares vendors, it builds a scoring matrix from the attributes available via structured APIs. Here is what a typical agent evaluates today versus what it misses:

| Attribute | Evaluable by Agent | Format Required |
|---|---|---|
| Unit price | Yes | Numeric field in API response |
| Shipping cost and speed | Yes | Structured shipping object |
| Seller trust/reputation score | Yes | Numeric score via trust API |
| Return policy | Yes | Structured policy object |
| Product specifications | Yes | Key-value attributes |
| Stock availability | Yes | Boolean or quantity field |
| **Loyalty points earned** | **No** | Not available in product APIs |
| **Tier benefits applicable** | **No** | Rendered in frontend only |
| **Redeemable points balance** | **No** | Requires authenticated session |
| **Promotional multipliers** | **No** | JavaScript-rendered banner |
| **Points-to-currency conversion** | **No** | No structured endpoint |

The bottom five rows represent the loyalty gap. Every one of these attributes could be expressed as a structured field in an API response. None of them currently are, in the vast majority of merchant implementations.

### The Competitive Shift

Merchants who make their loyalty programs machine-readable gain a structural advantage in agent-mediated commerce. Consider two competing merchants selling the same product at the same price:

- **Merchant A**: Returns `{"price": 49.99, "currency": "USD"}` from their product API. No loyalty data.
- **Merchant B**: Returns `{"price": 49.99, "currency": "USD", "loyalty": {"points_earned": 500, "points_value_usd": 5.00, "member_tier": "gold", "tier_discount_pct": 5, "effective_price_usd": 42.49}}` from their product API.

A scoring agent evaluating both merchants will select Merchant B every time, because Merchant B's effective price -- after tier discount and loyalty point value -- is $42.49 versus Merchant A's $49.99. Merchant A's loyalty program might be equally generous, but it is invisible, so it scores zero.

This is not a theoretical scenario. It is happening now, and the merchants losing transactions to this dynamic do not even know it, because the agent never visits their storefront at all. It queries, gets a partial response, scores it lower, and moves on.

```python
import os
import requests
from typing import Any


GATEWAY_URL = os.environ.get("GREENHELIX_API_URL", "https://sandbox.greenhelix.net")


class LoyaltyClient:
    """Client for GreenHelix A2A Commerce Gateway loyalty operations."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        })

    def execute(self, tool: str, input_data: dict[str, Any]) -> dict:
        """Execute a single tool on the gateway."""
        resp = self.session.post(
            f"{GATEWAY_URL}/v1",
            json={"tool": tool, "input": input_data},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()


# Initialize -- used throughout this guide
client = LoyaltyClient(api_key=os.environ.get("GREENHELIX_API_KEY", "your-api-key"))


# Demonstrate the gap: search for a product and check for loyalty data
product_search = client.execute("search_services", {
    "query": "wireless noise-cancelling headphones",
    "filters": {"max_price": 100.00, "category": "electronics"},
})

for service in product_search.get("services", []):
    has_loyalty = "loyalty" in service or "incentives" in service
    print(f"  {service.get('name')}: loyalty_data={'yes' if has_loyalty else 'MISSING'}")
```

This simple probe -- checking whether search results include loyalty data -- reveals the scope of the problem in any marketplace. In a March 2026 audit of 200 merchant integrations on three major commerce platforms, only 12% included any machine-readable loyalty or incentive data in their API responses.

### Key Takeaways

- AI agents influence $20.9B in retail spend (2026) but ignore loyalty rewards in 68% of eligible transactions because the data is not machine-readable.
- Loyalty programs exist in HTML, JavaScript widgets, and frontend-rendered components that agents cannot parse. The rewards are invisible, not absent.
- Merchants who expose loyalty data as structured API fields gain a scoring advantage that translates directly to agent-selected transactions.
- The effective price calculation -- base price minus tier discounts minus redeemable point value -- is the single most powerful lever for winning agent comparisons.
- Cross-reference: P24 (Discovery) covers how agents find merchants. This guide covers what happens after discovery -- how incentives influence the selection decision.

---

## Chapter 2: Protocol Foundations: UCP, UIP, ACP, AP2

### The Protocol Landscape for Agent Incentives

Four protocols define how AI agents discover, evaluate, and interact with commerce services in 2026. Each handles incentives differently, and understanding their mechanisms is essential before designing a loyalty program that agents can actually use.

### Google's Unified Commerce Protocol (UCP) — January 2026

Google published UCP in January 2026 as an extension to their existing commerce infrastructure. UCP provides a standardized schema for representing commerce entities -- products, offers, merchants, and critically, incentives -- in a format that any agent can query and compare. UCP builds on Schema.org vocabulary but adds agent-specific extensions for programmatic evaluation.

UCP handles incentives through the `Incentive` entity type, which describes a reward, discount, or benefit that an agent can factor into a purchase decision:

```json
{
  "@context": "https://schema.org",
  "@type": "Incentive",
  "incentiveType": "LoyaltyPoints",
  "name": "Gold Tier Bonus Points",
  "description": "3x points on all electronics purchases for Gold members",
  "eligibility": {
    "@type": "IncentiveEligibility",
    "memberTier": "gold",
    "productCategory": "electronics",
    "validFrom": "2026-01-01T00:00:00Z",
    "validThrough": "2026-12-31T23:59:59Z"
  },
  "reward": {
    "@type": "IncentiveReward",
    "rewardType": "points",
    "pointsMultiplier": 3,
    "basePointsPerDollar": 1,
    "pointToCurrencyRatio": 0.01,
    "currencyCode": "USD"
  },
  "stackable": true,
  "exclusions": ["clearance", "gift-cards"],
  "machineReadable": true
}
```

The key fields for agent consumption are `reward.pointToCurrencyRatio` (allows exact USD conversion), `stackable` (tells the agent whether this incentive can combine with others), and `exclusions` (product categories or conditions where the incentive does not apply). UCP mandates that incentive entities include `machineReadable: true` to signal that the data is intended for programmatic consumption, not just display.

**UCP Identity Linking** allows an agent to present credentials on behalf of a user and retrieve that user's loyalty state -- tier, points balance, applicable incentives -- through a standardized API call. This is covered in depth in Chapter 4.

### Talon.One's Unified Incentives Protocol (UIP) — January 2026

Talon.One released UIP in January 2026 as an open protocol for representing incentives across platforms. While UCP focuses on the full commerce entity model, UIP is laser-focused on incentives: promotions, coupons, loyalty rules, referral programs, and dynamic pricing. UIP uses a rule-engine model where incentives are expressed as condition-action pairs:

```json
{
  "uip_version": "1.0",
  "incentive_id": "promo-spring-2026-electronics",
  "type": "conditional_discount",
  "conditions": [
    {"field": "cart.category", "operator": "in", "value": ["electronics"]},
    {"field": "customer.tier", "operator": "gte", "value": "silver"},
    {"field": "cart.total", "operator": "gte", "value": 75.00}
  ],
  "actions": [
    {"type": "percentage_discount", "value": 15, "applies_to": "cart.total"},
    {"type": "bonus_points", "value": 500, "points_program": "main"}
  ],
  "stacking_rules": {
    "group": "spring-promos",
    "max_stack": 2,
    "priority": 10
  },
  "redemption_limits": {
    "per_customer": 3,
    "global": 10000,
    "remaining": 7842
  },
  "machine_parseable": true
}
```

UIP's condition-action model is particularly powerful for agents because it lets them evaluate eligibility programmatically. An agent can take a UIP incentive definition, check each condition against the current cart state and customer profile, and determine -- before making any API call -- whether the incentive applies and what the reward will be. This pre-evaluation reduces API round-trips and latency.

**UIP vs UCP for incentives**: UCP provides a broader commerce data model with incentives as one entity type. UIP provides deeper incentive-specific semantics -- stacking rules, redemption limits, condition evaluation. Production implementations typically use both: UCP for discovery (finding merchants with incentives) and UIP for evaluation (determining which incentives apply and their exact value).

### OpenAI's Agentic Commerce Protocol (ACP)

ACP focuses on agent-to-merchant transactions: product search, cart management, checkout, and payment. ACP's incentive handling is implicit rather than explicit -- incentives appear as price adjustments in the cart rather than as standalone entities. When an agent adds an item to an ACP cart, the response includes `adjustments` that reflect applicable incentives:

```json
{
  "cart": {
    "items": [
      {
        "product_id": "SKU-12345",
        "quantity": 1,
        "base_price": 99.99,
        "adjustments": [
          {
            "type": "loyalty_discount",
            "description": "Gold member 10% discount",
            "amount": -10.00,
            "source": "loyalty_program",
            "loyalty_program_id": "merchant-gold-tier"
          },
          {
            "type": "points_earned",
            "description": "300 points earned on this purchase",
            "points": 300,
            "estimated_value_usd": 3.00
          }
        ],
        "final_price": 89.99
      }
    ]
  }
}
```

ACP's approach means agents see the net effect of incentives during the cart phase, but they do not discover incentives during the search phase. An agent using ACP alone cannot ask "which merchants have the best loyalty program for electronics" -- it can only add items to a cart and observe what adjustments appear. This is why combining ACP with UCP (for discovery) and UIP (for pre-evaluation) produces the best agent experience.

### Google's Agent-to-Agent Protocol (AP2/A2A)

AP2 (also referred to as A2A) handles agent-to-agent delegation and service discovery. For loyalty programs, AP2 is relevant because a merchant's loyalty service can publish an Agent Card that describes its incentive capabilities:

```json
{
  "name": "MerchantX Loyalty Service",
  "description": "Query and redeem loyalty points for MerchantX",
  "url": "https://loyalty.merchantx.com",
  "version": "1.0",
  "capabilities": [
    {
      "name": "query_loyalty_balance",
      "description": "Get a member's current points balance and tier",
      "input_schema": {
        "type": "object",
        "properties": {
          "member_id": {"type": "string"},
          "agent_credential": {"type": "string"}
        }
      }
    },
    {
      "name": "evaluate_incentives",
      "description": "Get applicable incentives for a cart",
      "input_schema": {
        "type": "object",
        "properties": {
          "member_id": {"type": "string"},
          "cart_items": {"type": "array"},
          "agent_credential": {"type": "string"}
        }
      }
    },
    {
      "name": "redeem_points",
      "description": "Apply points to a transaction",
      "input_schema": {
        "type": "object",
        "properties": {
          "member_id": {"type": "string"},
          "points_to_redeem": {"type": "integer"},
          "transaction_id": {"type": "string"}
        }
      }
    }
  ],
  "authentication": {
    "schemes": ["bearer", "oauth2"]
  }
}
```

A shopping agent that discovers this Agent Card via AP2's `.well-known/agent.json` endpoint knows immediately that MerchantX has a loyalty program, what operations are available, and how to authenticate. The agent can then call `evaluate_incentives` before checkout to determine the loyalty value of a purchase.

### Protocol Comparison Matrix

| Capability | UCP | UIP | ACP | AP2 |
|---|---|---|---|---|
| Incentive discovery during search | Yes | No (needs UCP) | No | Yes (Agent Card) |
| Incentive eligibility pre-evaluation | Partial | Yes (condition engine) | No | Depends on capabilities |
| Loyalty state query (balance, tier) | Yes (Identity Linking) | No | Via cart adjustments | Yes (if capability published) |
| Redemption at checkout | No (display only) | Yes (action execution) | Yes (adjustments) | Yes (if capability published) |
| Stacking rule evaluation | Basic | Advanced (groups, priority) | Implicit | Depends on implementation |
| Points-to-currency conversion | Yes (explicit field) | Yes (explicit field) | Yes (estimated_value_usd) | Depends on implementation |
| Multi-merchant coalition support | Yes | Yes | No | Yes (federated Agent Cards) |

### Integrating Protocols via GreenHelix

The GreenHelix A2A Commerce Gateway abstracts protocol differences behind a unified tool interface. You register your loyalty program once, and the gateway exposes it through whichever protocol an agent uses to discover you:

```python
# Register a loyalty program that is discoverable via all protocols
loyalty_program = client.execute("register_service", {
    "name": "Premium Electronics Loyalty",
    "type": "loyalty_program",
    "protocols": ["ucp", "uip", "acp", "a2a"],
    "metadata": {
        "tiers": ["bronze", "silver", "gold", "platinum"],
        "base_points_per_dollar": 1,
        "point_value_usd": 0.01,
        "categories": ["electronics", "accessories"],
        "stacking_allowed": True,
    },
    "capabilities": [
        "query_balance",
        "evaluate_incentives",
        "redeem_points",
        "transfer_points",
    ],
})
print(f"Loyalty program registered: {loyalty_program.get('service_id')}")

# Publish the program as a UCP Incentive entity
ucp_incentive = client.execute("create_listing", {
    "service_id": loyalty_program.get("service_id"),
    "schema_type": "Incentive",
    "incentive_type": "LoyaltyPoints",
    "reward": {
        "reward_type": "points",
        "points_per_dollar": 1,
        "point_to_currency_ratio": 0.01,
        "currency_code": "USD",
    },
    "eligibility": {
        "min_tier": "bronze",
        "valid_categories": ["electronics", "accessories"],
    },
    "machine_readable": True,
})
print(f"UCP listing created: {ucp_incentive.get('listing_id')}")
```

### Key Takeaways

- Four protocols define agent-incentive interactions: UCP (discovery + identity linking), UIP (incentive evaluation + stacking), ACP (cart-level adjustments), and AP2 (agent-to-agent capability discovery).
- UCP and UIP were both published in January 2026. UCP provides the commerce entity model; UIP provides the incentive rule engine. Use both.
- ACP shows incentive effects at cart time but does not support pre-checkout incentive discovery. Combine with UCP for full coverage.
- AP2 Agent Cards let a loyalty service publish its capabilities so any agent can find and invoke them.
- GreenHelix abstracts protocol differences: register once, expose via all four protocols.
- Cross-reference: P24 (Discovery) covers protocol-level service discovery. This chapter covers the incentive-specific extensions within each protocol.

---

## Chapter 3: Designing Machine-Readable Loyalty Programs

### From Marketing Copy to Structured Schemas

A traditional loyalty program is described in a PDF, a web page, or a terms-and-conditions document. "Earn 1 point per dollar. Silver at 5,000 points. Gold at 15,000 points. Platinum at 50,000 points. Gold members get 10% off electronics. Redeem points at 1 cent each." This is clear to a human. It is opaque to an agent.

A machine-readable loyalty program expresses the same information as structured data with typed fields, enumerated values, and explicit relationships. The agent does not interpret -- it queries. Here is the target schema:

```json
{
  "program_id": "merchant-x-rewards",
  "program_name": "MerchantX Rewards",
  "version": "2.1",
  "currency": {
    "name": "MX Points",
    "code": "MXP",
    "to_usd_ratio": 0.01,
    "decimals": 0
  },
  "earning_rules": [
    {
      "rule_id": "base-earn",
      "points_per_usd": 1,
      "categories": ["*"],
      "conditions": [],
      "description": "Base earning rate"
    },
    {
      "rule_id": "electronics-bonus",
      "points_per_usd": 3,
      "categories": ["electronics"],
      "conditions": [{"field": "member.tier", "operator": "gte", "value": "gold"}],
      "description": "3x electronics for Gold+"
    }
  ],
  "tiers": [
    {
      "tier_id": "bronze",
      "name": "Bronze",
      "min_points_annual": 0,
      "perks": [],
      "discount_pct": 0
    },
    {
      "tier_id": "silver",
      "name": "Silver",
      "min_points_annual": 5000,
      "perks": ["free_shipping_over_50"],
      "discount_pct": 5
    },
    {
      "tier_id": "gold",
      "name": "Gold",
      "min_points_annual": 15000,
      "perks": ["free_shipping", "early_access", "priority_support"],
      "discount_pct": 10
    },
    {
      "tier_id": "platinum",
      "name": "Platinum",
      "min_points_annual": 50000,
      "perks": ["free_shipping", "early_access", "priority_support", "personal_shopper", "exclusive_sales"],
      "discount_pct": 15
    }
  ],
  "redemption_rules": {
    "min_redemption_points": 100,
    "redemption_increment": 100,
    "max_redemption_pct_of_order": 50,
    "excluded_categories": ["gift-cards"],
    "partial_redemption_allowed": true
  },
  "stacking_policy": {
    "tier_discount_stacks_with_promos": true,
    "max_promo_stack": 2,
    "points_earning_on_discounted_total": true
  }
}
```

Every field is typed. Every relationship is explicit. An agent can parse this schema, calculate the exact point value of a purchase for a Gold member buying electronics, determine whether points can be partially redeemed, and factor the tier discount into the effective price -- all without interpreting a single line of natural language.

### Building the Program with GreenHelix

Billing and identity tools serve as the persistence and query layer for loyalty state. The `create_billing_plan` tool defines the economic structure; `register_agent` creates identity records that track loyalty membership.

```python
# Step 1: Create billing plans for each loyalty tier
tiers = [
    {"name": "bronze", "monthly_fee": "0.00", "discount_pct": 0, "min_annual_points": 0},
    {"name": "silver", "monthly_fee": "0.00", "discount_pct": 5, "min_annual_points": 5000},
    {"name": "gold", "monthly_fee": "0.00", "discount_pct": 10, "min_annual_points": 15000},
    {"name": "platinum", "monthly_fee": "0.00", "discount_pct": 15, "min_annual_points": 50000},
]

tier_plans = {}
for tier in tiers:
    plan = client.execute("create_billing_plan", {
        "plan_name": f"loyalty-{tier['name']}",
        "billing_cycle": "monthly",
        "base_price": tier["monthly_fee"],
        "currency": "USD",
        "metadata": {
            "tier_level": tier["name"],
            "discount_pct": tier["discount_pct"],
            "min_annual_points": tier["min_annual_points"],
            "loyalty_program": "merchant-x-rewards",
        },
    })
    tier_plans[tier["name"]] = plan
    print(f"Created tier plan: {tier['name']} -> {plan.get('plan_id')}")


# Step 2: Register a loyalty member as an agent identity
member = client.execute("register_agent", {
    "agent_id": "customer-agent-jane-doe",
    "display_name": "Jane Doe's Shopping Agent",
    "metadata": {
        "loyalty_program": "merchant-x-rewards",
        "tier": "gold",
        "points_balance": 18500,
        "points_earned_ytd": 22000,
        "member_since": "2024-06-15",
    },
})
print(f"Registered loyalty member: {member.get('agent_id')}")


# Step 3: Create the loyalty earning rules as a billing configuration
earning_config = client.execute("create_billing_plan", {
    "plan_name": "loyalty-earning-rules",
    "billing_cycle": "per_transaction",
    "base_price": "0.00",
    "currency": "USD",
    "metadata": {
        "loyalty_program": "merchant-x-rewards",
        "earning_rules": [
            {
                "rule_id": "base-earn",
                "points_per_usd": 1,
                "categories": ["*"],
            },
            {
                "rule_id": "electronics-gold-bonus",
                "points_per_usd": 3,
                "categories": ["electronics"],
                "required_tier": "gold",
            },
            {
                "rule_id": "electronics-platinum-bonus",
                "points_per_usd": 5,
                "categories": ["electronics"],
                "required_tier": "platinum",
            },
        ],
    },
})
print(f"Earning rules configured: {earning_config.get('plan_id')}")
```

### Incentive Object Schema Design

Beyond the loyalty program itself, individual incentives (promotions, limited-time offers, bonus events) need their own schema. The design principle: every field an agent needs for a decision must be a typed, queryable attribute.

| Field | Type | Purpose | Agent Use |
|---|---|---|---|
| `incentive_id` | string | Unique identifier | Deduplication, tracking |
| `type` | enum | `discount`, `bonus_points`, `free_shipping`, `gift`, `cashback` | Filtering by incentive type |
| `value` | number | Magnitude of the incentive | Scoring and comparison |
| `value_currency` | string | Currency or "points" | Unit normalization |
| `conditions` | array | Eligibility conditions | Pre-evaluation |
| `valid_from` / `valid_through` | ISO 8601 | Time window | Freshness check |
| `stackable` | boolean | Can combine with other incentives | Optimization |
| `stacking_group` | string | Mutual exclusion group | Conflict resolution |
| `max_stack_in_group` | integer | Max incentives from same group | Constraint |
| `redemption_limit_per_customer` | integer | Per-member cap | Availability check |
| `redemption_limit_global` | integer | Total cap | Scarcity signal |
| `remaining_global` | integer | How many left | Urgency signal |
| `excluded_categories` | array | Categories where incentive does not apply | Cart filtering |
| `min_order_value` | number | Minimum spend to qualify | Threshold check |

```python
# Create a promotional incentive using GreenHelix
spring_promo = client.execute("create_listing", {
    "service_id": "merchant-x-rewards",
    "listing_type": "incentive",
    "name": "Spring Electronics Blowout",
    "metadata": {
        "incentive_id": "spring-2026-electronics",
        "type": "bonus_points",
        "value": 500,
        "value_currency": "MXP",
        "conditions": [
            {"field": "cart.category", "operator": "contains", "value": "electronics"},
            {"field": "cart.total", "operator": "gte", "value": 100.00},
        ],
        "valid_from": "2026-03-01T00:00:00Z",
        "valid_through": "2026-05-31T23:59:59Z",
        "stackable": True,
        "stacking_group": "seasonal-promos",
        "max_stack_in_group": 1,
        "redemption_limit_per_customer": 5,
        "redemption_limit_global": 50000,
        "remaining_global": 43218,
        "excluded_categories": ["gift-cards", "clearance"],
        "min_order_value": 100.00,
    },
})
print(f"Incentive created: {spring_promo.get('listing_id')}")
```

### Point Valuation Transparency

The single most important field for agent decision-making is `point_to_currency_ratio`. Without it, the agent cannot convert loyalty points to a comparable currency value. With it, the agent can compute:

```
effective_price = base_price - tier_discount - (redeemable_points * point_to_currency_ratio)
```

This transforms loyalty from a "nice to have" that agents ignore into a first-class pricing dimension that agents optimize for.

**Design checklist for machine-readable loyalty programs:**

- [ ] Every tier has explicit `discount_pct` and `perks` arrays
- [ ] Earning rules include `points_per_usd` with category filters
- [ ] `point_to_currency_ratio` is published at the program level
- [ ] Redemption rules specify `min_redemption_points`, `max_redemption_pct_of_order`, and `partial_redemption_allowed`
- [ ] Stacking policy is explicit: which incentives combine, max stack depth, earning on discounted totals
- [ ] All time windows use ISO 8601
- [ ] All monetary values include currency code
- [ ] Schema version is included for forward compatibility

### Key Takeaways

- Machine-readable loyalty programs express tiers, earning rules, redemption rules, and stacking policies as typed, queryable fields -- not natural language.
- `point_to_currency_ratio` is the single most important field. Without it, agents cannot factor loyalty into purchase scoring.
- GreenHelix `create_billing_plan` and `register_agent` provide the persistence layer for loyalty state (tiers, balances, earning rules).
- Individual incentives (promos, bonuses) need their own schema with conditions, stacking rules, and redemption limits.
- Design checklist: tier discounts, earning rates, point valuation, redemption constraints, stacking policy, time windows, currency codes, schema version.
- Cross-reference: P18 (Pricing) covers base pricing strategies. This chapter covers the incentive layer on top of base pricing.

---

## Chapter 4: Agent Identity Linking & Member Recognition

### The Identity Challenge

An AI shopping agent acts on behalf of a human user. The agent has its own identity (agent ID, API credentials) and the human has a separate identity (loyalty member ID, email, phone number). For loyalty programs to work in agent commerce, the merchant must link the agent's identity to the human's loyalty membership. Without this link, the agent is an anonymous visitor -- no tier benefits, no points balance, no personalized incentives.

Identity linking is the process of establishing a trust chain: "This agent is authorized to act on behalf of this loyalty member, and the merchant should treat the agent's actions as the member's actions for loyalty purposes."

### UCP Identity Linking Flow

UCP defines a three-party identity linking flow involving the human (resource owner), the agent (client), and the merchant (resource server). The flow uses OAuth 2.0 conventions adapted for agent commerce:

1. **Human authorizes agent**: The human grants the agent permission to access their loyalty account, typically through a one-time consent flow in the agent's interface.
2. **Agent receives a delegation token**: A scoped token that proves the agent is authorized to query and redeem loyalty on behalf of the specific human.
3. **Agent presents delegation token to merchant**: The merchant validates the token and returns loyalty state for the linked member.

```python
# Step 1: Register the agent with identity tools
agent_registration = client.execute("register_agent", {
    "agent_id": "shopping-agent-a1b2c3",
    "display_name": "Alice's Personal Shopping Agent",
    "capabilities": ["commerce", "loyalty_management"],
    "metadata": {
        "owner_email_hash": "sha256:a1b2c3d4e5f6...",  # hashed for privacy
        "delegation_scope": ["loyalty.read", "loyalty.redeem"],
        "consent_timestamp": "2026-03-15T10:30:00Z",
    },
})
print(f"Agent registered: {agent_registration.get('agent_id')}")

# Step 2: Verify the agent identity to establish trust
verification = client.execute("verify_identity", {
    "agent_id": "shopping-agent-a1b2c3",
    "verification_type": "delegation",
    "delegation_proof": {
        "owner_id": "loyalty-member-alice-789",
        "scope": ["loyalty.read", "loyalty.redeem"],
        "issued_at": "2026-03-15T10:30:00Z",
        "expires_at": "2026-06-15T10:30:00Z",
        "signature": "base64-encoded-signature...",
    },
})
print(f"Identity verified: {verification.get('verified')}")
print(f"Linked member: {verification.get('linked_member_id')}")

# Step 3: Retrieve loyalty state using the linked identity
loyalty_state = client.execute("get_agent_identity", {
    "agent_id": "shopping-agent-a1b2c3",
})
print(f"Tier: {loyalty_state.get('metadata', {}).get('tier')}")
print(f"Points: {loyalty_state.get('metadata', {}).get('points_balance')}")
```

### Guest vs. Authenticated Agent Interactions

Not every agent interaction requires identity linking. The loyalty program should handle three interaction levels:

| Level | Agent Credential | Loyalty Data Available | Use Case |
|---|---|---|---|
| **Anonymous** | No credential | Program structure only (tiers, earning rates, general incentives) | Agent evaluating whether to recommend this merchant |
| **Agent-authenticated** | Agent's own Bearer token | General incentives, new member offers, sign-up bonuses | First-time visitor, no linked member |
| **Member-linked** | Delegation token | Full loyalty state: tier, balance, personalized incentives, redemption | Returning member with authorized agent |

```python
# Anonymous query: what does this loyalty program offer?
program_info = client.execute("search_services", {
    "query": "MerchantX loyalty program",
    "filters": {"type": "loyalty_program"},
})
# Returns: program structure, tiers, base earning rates -- no personalization

# Agent-authenticated query: general incentives available
general_incentives = client.execute("search_services", {
    "query": "MerchantX current promotions",
    "filters": {
        "type": "incentive",
        "merchant": "merchant-x",
        "requires_membership": False,
    },
})
# Returns: public promotions, new member signup bonuses

# Member-linked query: personalized loyalty state
personalized = client.execute("get_agent_identity", {
    "agent_id": "shopping-agent-a1b2c3",
})
member_meta = personalized.get("metadata", {})
# Returns: tier=gold, points=18500, personalized offers, redemption options
```

The design principle: always return the maximum information the credential level permits. An anonymous agent should still see the program structure -- that information helps the agent recommend the merchant for loyalty-conscious users. Restricting program structure behind authentication reduces discovery and hurts acquisition.

### Privacy Considerations

Agent identity linking creates a data flow where a merchant learns that a specific agent acts for a specific loyalty member. This has privacy implications:

**Minimum data principle**: The agent should present only the data needed for the interaction. For a loyalty balance query, the agent needs to prove it represents the member. It does not need to reveal the member's email address, purchase history, or demographic data. The delegation token should be scoped and the merchant should request only the claims it needs.

**Token expiration**: Delegation tokens should have finite lifetimes (90 days is a reasonable default). Expired tokens require re-authorization by the human, which serves as a periodic consent checkpoint.

**Agent tracking**: Merchants should not use agent IDs to build cross-session profiles that circumvent the user's privacy choices. If the user opts out of tracking, the agent's requests should be treated as anonymous regardless of the agent's identity.

```python
# Privacy-respecting identity check: verify without exposing PII
privacy_check = client.execute("verify_identity", {
    "agent_id": "shopping-agent-a1b2c3",
    "verification_type": "privacy_scoped",
    "requested_claims": ["tier", "points_balance", "applicable_incentives"],
    "excluded_claims": ["email", "phone", "address", "purchase_history"],
})

# The merchant receives only:
# - tier: "gold"
# - points_balance: 18500
# - applicable_incentives: [list of incentive IDs]
# No PII is transmitted.
print(f"Scoped claims: {privacy_check.get('claims', {}).keys()}")
```

### Multi-Agent Households

A single loyalty member may authorize multiple agents: a personal shopping agent, a comparison agent, a deal-finder agent. The identity linking system must handle this without creating duplicate member records or conflicting redemption states.

**Design rule**: One member, many agents, one loyalty state. All authorized agents read from and write to the same points balance. Redemptions are serialized to prevent double-spending. Each agent's delegation token is independently revocable.

```python
# Register a second agent for the same member
second_agent = client.execute("register_agent", {
    "agent_id": "deal-finder-agent-x7y8z9",
    "display_name": "Alice's Deal Finder",
    "capabilities": ["commerce", "loyalty_management"],
    "metadata": {
        "owner_email_hash": "sha256:a1b2c3d4e5f6...",  # same hash as first agent
        "delegation_scope": ["loyalty.read"],  # read-only, cannot redeem
        "consent_timestamp": "2026-03-20T14:00:00Z",
        "linked_member": "loyalty-member-alice-789",
    },
})

# Both agents see the same loyalty state
state_1 = client.execute("get_agent_identity", {"agent_id": "shopping-agent-a1b2c3"})
state_2 = client.execute("get_agent_identity", {"agent_id": "deal-finder-agent-x7y8z9"})

balance_1 = state_1.get("metadata", {}).get("points_balance")
balance_2 = state_2.get("metadata", {}).get("points_balance")
assert balance_1 == balance_2, "Both agents must see the same balance"
print(f"Consistent balance across agents: {balance_1}")
```

### Key Takeaways

- Identity linking connects an agent's API credential to a human's loyalty membership via a scoped delegation token.
- Three interaction levels: anonymous (program structure only), agent-authenticated (general incentives), member-linked (full personalized state).
- Always return maximum information for the credential level. Hiding program structure behind auth hurts discovery.
- Privacy: scope delegation tokens, set expiration (90 days), do not use agent IDs for cross-session tracking.
- Multi-agent households: one member, many agents, one loyalty state. Serialize redemptions to prevent double-spend.
- Cross-reference: P21 (Storefronts) covers agent authentication for commerce. This chapter covers the loyalty-specific identity layer on top of commerce auth.

---

## Chapter 5: Real-Time Incentive Negotiation

### Agents Compare Incentives Mid-Decision

When a shopping agent evaluates vendors, it does not just compare prices. It compares the total value proposition: price, shipping, trust score, return policy, and -- if the data is available -- loyalty incentives. The agent that can query incentive APIs in real time, mid-decision, will make objectively better selections for its user.

Real-time incentive negotiation means the agent queries each vendor's incentive endpoint during the comparison phase, receives structured incentive data, evaluates eligibility, calculates the net value, and incorporates that value into its scoring algorithm. This happens in milliseconds, across multiple vendors, for every purchase decision.

### Building an Incentive Comparison Engine

The core pattern: for each candidate vendor, query three things -- (1) the base offer, (2) applicable incentives, and (3) the user's loyalty state at that vendor. Combine them into an effective price.

```python
import concurrent.futures
from dataclasses import dataclass


@dataclass
class VendorOffer:
    vendor_id: str
    base_price: float
    shipping_cost: float
    trust_score: float
    tier_discount_pct: float
    points_earned: int
    points_value_usd: float
    redeemable_points: int
    redeemable_value_usd: float
    promo_discount_usd: float
    effective_price: float


def evaluate_vendor(vendor_id: str, product_query: str, member_agent_id: str) -> VendorOffer:
    """Evaluate a single vendor's total offer including loyalty incentives."""

    # Query base product offer
    product = client.execute("search_services", {
        "query": product_query,
        "filters": {"vendor": vendor_id, "limit": 1},
    })
    item = product.get("services", [{}])[0]
    base_price = float(item.get("price", 0))
    shipping = float(item.get("shipping_cost", 0))

    # Check trust score
    trust = client.execute("check_trust_score", {
        "agent_id": vendor_id,
    })
    trust_score = float(trust.get("trust_score", 0))

    # Get loyalty state at this vendor
    identity = client.execute("get_agent_identity", {
        "agent_id": member_agent_id,
    })
    meta = identity.get("metadata", {})
    tier = meta.get("tier", "none")
    points_balance = int(meta.get("points_balance", 0))

    # Calculate tier discount
    tier_discounts = {"none": 0, "bronze": 0, "silver": 5, "gold": 10, "platinum": 15}
    tier_discount_pct = tier_discounts.get(tier, 0)
    tier_discount_usd = base_price * (tier_discount_pct / 100)

    # Calculate points earned and their value
    points_per_usd = int(meta.get("points_per_usd", 1))
    point_value = float(meta.get("point_to_currency_ratio", 0.01))
    points_earned = int(base_price * points_per_usd)
    points_value_usd = points_earned * point_value

    # Calculate redeemable points value
    max_redemption_pct = float(meta.get("max_redemption_pct", 50))
    max_redeemable_value = base_price * (max_redemption_pct / 100)
    redeemable_value = min(points_balance * point_value, max_redeemable_value)
    redeemable_points = int(redeemable_value / point_value) if point_value > 0 else 0

    # Check for applicable promotions
    promo_discount = 0.0  # Would query vendor's incentive endpoint

    # Effective price = base - tier discount - redeemable value - promos + shipping
    effective_price = base_price - tier_discount_usd - redeemable_value - promo_discount + shipping

    return VendorOffer(
        vendor_id=vendor_id,
        base_price=base_price,
        shipping_cost=shipping,
        trust_score=trust_score,
        tier_discount_pct=tier_discount_pct,
        points_earned=points_earned,
        points_value_usd=points_value_usd,
        redeemable_points=redeemable_points,
        redeemable_value_usd=redeemable_value,
        promo_discount_usd=promo_discount,
        effective_price=effective_price,
    )


def compare_vendors(
    vendor_ids: list[str],
    product_query: str,
    member_agent_id: str,
) -> list[VendorOffer]:
    """Compare multiple vendors in parallel, including loyalty incentives."""
    offers = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(evaluate_vendor, vid, product_query, member_agent_id): vid
            for vid in vendor_ids
        }
        for future in concurrent.futures.as_completed(futures):
            try:
                offers.append(future.result())
            except Exception as e:
                print(f"Error evaluating {futures[future]}: {e}")

    # Sort by effective price (lowest first), then by trust score (highest first)
    offers.sort(key=lambda o: (o.effective_price, -o.trust_score))
    return offers


# Example: compare 4 vendors for a headphone purchase
vendors = ["vendor-a", "vendor-b", "vendor-c", "vendor-d"]
results = compare_vendors(vendors, "wireless noise-cancelling headphones", "shopping-agent-a1b2c3")

print(f"\n{'Vendor':<12} {'Base':>8} {'Ship':>6} {'Tier%':>6} {'Redeem':>8} {'Promo':>7} {'Effective':>10} {'Trust':>6}")
print("-" * 75)
for o in results:
    print(
        f"{o.vendor_id:<12} ${o.base_price:>6.2f} ${o.shipping_cost:>4.2f} "
        f"{o.tier_discount_pct:>5.0f}% ${o.redeemable_value_usd:>6.2f} "
        f"${o.promo_discount_usd:>5.2f} ${o.effective_price:>8.2f} {o.trust_score:>5.1f}"
    )
```

### Dynamic Pricing with Trust Scores

Merchants can offer better incentives to agents (and their users) with higher trust scores. This creates a virtuous cycle: trusted agents get better deals, which improves their users' outcomes, which increases the agent's reputation, which earns more trust.

```python
def get_dynamic_incentive(vendor_id: str, agent_id: str, cart_total: float) -> dict:
    """Query a vendor's dynamic incentive based on agent trust score."""

    # Get the agent's trust score
    trust = client.execute("check_trust_score", {
        "agent_id": agent_id,
    })
    score = float(trust.get("trust_score", 0))

    # Trust-tiered incentive schedule
    # Higher trust = better incentives (merchant rewards reliable agents)
    if score >= 90:
        bonus_multiplier = 3.0
        extra_discount_pct = 5
    elif score >= 75:
        bonus_multiplier = 2.0
        extra_discount_pct = 3
    elif score >= 50:
        bonus_multiplier = 1.5
        extra_discount_pct = 1
    else:
        bonus_multiplier = 1.0
        extra_discount_pct = 0

    return {
        "vendor_id": vendor_id,
        "agent_id": agent_id,
        "trust_score": score,
        "bonus_points_multiplier": bonus_multiplier,
        "extra_discount_pct": extra_discount_pct,
        "extra_discount_usd": cart_total * (extra_discount_pct / 100),
        "reason": f"Trust score {score} qualifies for {bonus_multiplier}x points and {extra_discount_pct}% extra discount",
    }


incentive = get_dynamic_incentive("vendor-a", "shopping-agent-a1b2c3", 149.99)
print(f"Dynamic incentive: {incentive['bonus_points_multiplier']}x points, "
      f"{incentive['extra_discount_pct']}% extra discount "
      f"(${incentive['extra_discount_usd']:.2f})")
```

### Promo Stacking and Exclusion Logic

Agents need to know which incentives can stack and which are mutually exclusive. The stacking rules must be machine-readable:

| Stacking Scenario | Rule | Agent Behavior |
|---|---|---|
| Tier discount + seasonal promo | Stackable | Apply both, sum the discounts |
| Two seasonal promos in same group | Max 1 per group | Pick the higher-value promo |
| Points earning on discounted total | Depends on `points_on_discounted` flag | If true, earn points on post-discount price; if false, on pre-discount |
| Loyalty redemption + promo | Depends on `redemption_stacks_with_promos` | If true, apply both; if false, apply promo first, then redemption on remainder |
| New member bonus + referral bonus | Typically stackable | Apply both (different incentive types) |

```python
def evaluate_stacking(incentives: list[dict], cart_total: float) -> dict:
    """Evaluate which incentives stack and compute the optimal combination."""
    # Group incentives by stacking group
    groups: dict[str, list[dict]] = {}
    ungrouped = []

    for inc in incentives:
        group = inc.get("stacking_group")
        if group:
            groups.setdefault(group, []).append(inc)
        else:
            ungrouped.append(inc)

    # From each group, pick the highest-value incentive (up to max_stack)
    selected = list(ungrouped)  # ungrouped incentives always apply
    for group_name, group_incentives in groups.items():
        max_stack = group_incentives[0].get("max_stack_in_group", 1)
        # Sort by value descending
        group_incentives.sort(key=lambda i: i.get("value", 0), reverse=True)
        selected.extend(group_incentives[:max_stack])

    # Calculate total discount
    total_discount = 0.0
    total_bonus_points = 0
    applied = []

    for inc in selected:
        if inc["type"] == "percentage_discount":
            discount = cart_total * (inc["value"] / 100)
            total_discount += discount
            applied.append({"id": inc["incentive_id"], "discount_usd": discount})
        elif inc["type"] == "fixed_discount":
            total_discount += inc["value"]
            applied.append({"id": inc["incentive_id"], "discount_usd": inc["value"]})
        elif inc["type"] == "bonus_points":
            total_bonus_points += inc["value"]
            applied.append({"id": inc["incentive_id"], "bonus_points": inc["value"]})

    return {
        "original_total": cart_total,
        "total_discount": min(total_discount, cart_total),  # cannot exceed cart
        "final_total": max(cart_total - total_discount, 0),
        "bonus_points_earned": total_bonus_points,
        "incentives_applied": applied,
        "incentives_excluded": [
            i["incentive_id"] for i in incentives if i not in selected
        ],
    }


# Example: evaluate stacking for a $149.99 cart with multiple incentives
incentives = [
    {
        "incentive_id": "gold-tier-discount",
        "type": "percentage_discount",
        "value": 10,
        "stacking_group": None,
    },
    {
        "incentive_id": "spring-promo-15",
        "type": "percentage_discount",
        "value": 15,
        "stacking_group": "seasonal-promos",
        "max_stack_in_group": 1,
    },
    {
        "incentive_id": "spring-promo-10",
        "type": "percentage_discount",
        "value": 10,
        "stacking_group": "seasonal-promos",
        "max_stack_in_group": 1,
    },
    {
        "incentive_id": "spring-bonus-points",
        "type": "bonus_points",
        "value": 500,
        "stacking_group": None,
    },
]

result = evaluate_stacking(incentives, 149.99)
print(f"Original: ${result['original_total']:.2f}")
print(f"Discount: ${result['total_discount']:.2f}")
print(f"Final: ${result['final_total']:.2f}")
print(f"Bonus points: {result['bonus_points_earned']}")
print(f"Applied: {[a['id'] for a in result['incentives_applied']]}")
print(f"Excluded: {result['incentives_excluded']}")
```

### Key Takeaways

- Real-time incentive negotiation means agents query vendor incentive endpoints during the comparison phase, not after selection.
- The incentive comparison engine evaluates base price, tier discount, redeemable points, and promotions across vendors in parallel, producing an effective price for each.
- Trust-based dynamic pricing rewards reliable agents with better incentives, creating a virtuous cycle.
- Stacking rules must be machine-readable: groups, max stack depth, priority, and the `points_on_discounted` flag.
- The agent selects the optimal stacking combination programmatically -- it does not rely on the merchant to apply the "best" combination.
- Cross-reference: P18 (Pricing) covers dynamic pricing models. P19 (Payment Rails) covers how the final price flows into payment. This chapter covers the incentive negotiation that happens between pricing and payment.

---

## Chapter 6: Reward Redemption & Settlement

### The Redemption Flow

Reward redemption in agent commerce follows a three-phase flow: (1) the agent discovers applicable redemption options, (2) the agent applies a redemption to a transaction, and (3) the merchant settles the transaction with the redemption reflected in the payment amount. Each phase must be structured and atomic.

**Phase 1 — Discovery**: The agent queries the member's redeemable balance and the merchant's redemption rules.

**Phase 2 — Application**: The agent specifies how many points to redeem and the transaction to apply them to. The merchant validates and locks the points.

**Phase 3 — Settlement**: The payment is processed for the net amount (after redemption). The merchant confirms the redemption and deducts points from the member's balance.

```python
def execute_redemption_flow(
    agent_id: str,
    product_id: str,
    base_price: float,
    points_to_redeem: int,
    point_value: float = 0.01,
) -> dict:
    """Full redemption flow: discover, apply, settle."""

    # Phase 1: Discover redemption options
    identity = client.execute("get_agent_identity", {"agent_id": agent_id})
    meta = identity.get("metadata", {})
    points_balance = int(meta.get("points_balance", 0))
    max_redemption_pct = float(meta.get("max_redemption_pct", 50))
    min_redemption = int(meta.get("min_redemption_points", 100))

    # Validate redemption request
    max_redeemable_value = base_price * (max_redemption_pct / 100)
    requested_value = points_to_redeem * point_value

    if points_to_redeem < min_redemption:
        return {"error": f"Minimum redemption is {min_redemption} points"}
    if points_to_redeem > points_balance:
        return {"error": f"Insufficient balance: {points_balance} < {points_to_redeem}"}
    if requested_value > max_redeemable_value:
        return {"error": f"Exceeds max redemption: ${requested_value:.2f} > ${max_redeemable_value:.2f}"}

    redemption_value = requested_value
    net_price = base_price - redemption_value

    # Phase 2: Create payment intent for net amount
    payment_intent = client.execute("create_payment_intent", {
        "amount": str(net_price),
        "currency": "USD",
        "description": f"Purchase {product_id} with {points_to_redeem} points redeemed",
        "metadata": {
            "product_id": product_id,
            "base_price": str(base_price),
            "points_redeemed": points_to_redeem,
            "redemption_value_usd": str(redemption_value),
            "net_price": str(net_price),
            "member_agent_id": agent_id,
        },
    })
    intent_id = payment_intent.get("intent_id")
    print(f"Payment intent created: {intent_id}")
    print(f"  Base price: ${base_price:.2f}")
    print(f"  Points redeemed: {points_to_redeem} (${redemption_value:.2f})")
    print(f"  Net charge: ${net_price:.2f}")

    # Phase 3: Confirm payment and settle
    confirmation = client.execute("confirm_payment", {
        "intent_id": intent_id,
        "payment_method": "agent_wallet",
    })

    if confirmation.get("status") == "confirmed":
        # Deduct points from member balance (update identity metadata)
        new_balance = points_balance - points_to_redeem
        # Also credit points earned on the purchase
        points_earned = int(net_price)  # 1 point per dollar on net amount
        new_balance += points_earned

        print(f"  Payment confirmed: {confirmation.get('confirmation_id')}")
        print(f"  Points deducted: {points_to_redeem}")
        print(f"  Points earned on purchase: {points_earned}")
        print(f"  New balance: {new_balance}")

        return {
            "status": "completed",
            "intent_id": intent_id,
            "confirmation_id": confirmation.get("confirmation_id"),
            "base_price": base_price,
            "redemption_value": redemption_value,
            "points_redeemed": points_to_redeem,
            "net_charged": net_price,
            "points_earned": points_earned,
            "new_balance": new_balance,
        }
    else:
        # Redemption failed -- points are not deducted
        return {
            "status": "failed",
            "reason": confirmation.get("error", "Payment confirmation failed"),
            "points_restored": points_to_redeem,
        }


# Example: redeem 5000 points on a $99.99 purchase
result = execute_redemption_flow(
    agent_id="shopping-agent-a1b2c3",
    product_id="headphones-pro-x",
    base_price=99.99,
    points_to_redeem=5000,
    point_value=0.01,
)
```

### Partial Redemptions

Not every redemption uses the full balance. Agents should be able to redeem any amount between the minimum and the maximum. The `partial_redemption_allowed` flag in the loyalty schema signals this capability.

**Partial redemption decision matrix:**

| User Preference | Agent Strategy | Points Redeemed |
|---|---|---|
| "Minimize out-of-pocket" | Redeem maximum allowed | `min(balance, max_redeemable)` |
| "Preserve points for bigger purchase" | Redeem nothing | 0 |
| "Redeem enough to hit a price target" | Compute exact redemption for target | `(base_price - target_price) / point_value` |
| "Use a round number of points" | Round down to nearest increment | `floor(desired / increment) * increment` |
| No preference set | Agent defaults to vendor recommendation | Varies |

```python
def calculate_partial_redemption(
    base_price: float,
    points_balance: int,
    point_value: float,
    max_redemption_pct: float,
    min_redemption_points: int,
    redemption_increment: int,
    strategy: str = "maximize",
    target_price: float | None = None,
) -> dict:
    """Calculate optimal partial redemption based on strategy."""
    max_redeemable_value = base_price * (max_redemption_pct / 100)
    max_redeemable_points = int(max_redeemable_value / point_value)
    available = min(points_balance, max_redeemable_points)

    if strategy == "maximize":
        # Redeem as much as possible
        points = (available // redemption_increment) * redemption_increment
    elif strategy == "preserve":
        # Redeem nothing
        points = 0
    elif strategy == "target" and target_price is not None:
        # Redeem exactly enough to hit target price
        needed_discount = base_price - target_price
        needed_points = int(needed_discount / point_value)
        # Round up to nearest increment
        needed_points = ((needed_points + redemption_increment - 1) // redemption_increment) * redemption_increment
        points = min(needed_points, available)
    else:
        points = 0

    # Enforce minimum
    if 0 < points < min_redemption_points:
        points = 0  # Below minimum, redeem nothing

    return {
        "points_to_redeem": points,
        "redemption_value_usd": points * point_value,
        "net_price": base_price - (points * point_value),
        "points_remaining": points_balance - points,
        "strategy": strategy,
    }


# Strategy comparison
for strat in ["maximize", "preserve", "target"]:
    result = calculate_partial_redemption(
        base_price=99.99,
        points_balance=18500,
        point_value=0.01,
        max_redemption_pct=50,
        min_redemption_points=100,
        redemption_increment=100,
        strategy=strat,
        target_price=74.99,
    )
    print(f"Strategy '{strat}': redeem {result['points_to_redeem']} pts "
          f"(${result['redemption_value_usd']:.2f}), pay ${result['net_price']:.2f}")
```

### Points-to-Currency Conversion

Some loyalty programs allow direct points-to-currency conversion outside of a purchase context. This is useful when agents need to consolidate value across programs or when the user wants to cash out. GreenHelix payments tools handle the conversion as a special payment type:

```python
def convert_points_to_currency(
    agent_id: str,
    points_to_convert: int,
    point_value: float,
    target_currency: str = "USD",
) -> dict:
    """Convert loyalty points to currency via GreenHelix payments."""
    conversion_value = points_to_convert * point_value

    # Create a conversion payment intent
    intent = client.execute("create_payment_intent", {
        "amount": str(conversion_value),
        "currency": target_currency,
        "description": f"Points-to-currency conversion: {points_to_convert} points",
        "metadata": {
            "transaction_type": "points_conversion",
            "points_converted": points_to_convert,
            "conversion_rate": str(point_value),
            "source_agent_id": agent_id,
        },
    })

    # Confirm the conversion
    confirmation = client.execute("confirm_payment", {
        "intent_id": intent.get("intent_id"),
        "payment_method": "points_conversion",
    })

    return {
        "points_converted": points_to_convert,
        "currency_received": conversion_value,
        "currency_code": target_currency,
        "intent_id": intent.get("intent_id"),
        "status": confirmation.get("status"),
    }


# Convert 10,000 points to USD
conversion = convert_points_to_currency(
    agent_id="shopping-agent-a1b2c3",
    points_to_convert=10000,
    point_value=0.01,
)
print(f"Converted {conversion['points_converted']} points to "
      f"${conversion['currency_received']:.2f} {conversion['currency_code']}")
```

### Settlement Ledger Entries

Every redemption must produce an auditable ledger entry. The GreenHelix Ledger tools provide the audit trail:

```python
def record_redemption_in_ledger(redemption_result: dict) -> dict:
    """Record a completed redemption in the ledger for audit trail."""
    ledger_entry = client.execute("record_transaction", {
        "transaction_type": "loyalty_redemption",
        "amount": str(redemption_result["redemption_value"]),
        "currency": "USD",
        "metadata": {
            "payment_intent_id": redemption_result["intent_id"],
            "confirmation_id": redemption_result["confirmation_id"],
            "points_redeemed": redemption_result["points_redeemed"],
            "base_price": str(redemption_result["base_price"]),
            "net_charged": str(redemption_result["net_charged"]),
            "points_earned": redemption_result["points_earned"],
            "new_balance": redemption_result["new_balance"],
            "timestamp": "2026-04-06T12:00:00Z",
        },
    })
    print(f"Ledger entry recorded: {ledger_entry.get('transaction_id')}")
    return ledger_entry
```

### Key Takeaways

- Redemption follows three atomic phases: discover (query balance and rules), apply (lock points and create payment intent for net amount), settle (confirm payment and deduct points).
- Partial redemptions require five parameters from the loyalty schema: `min_redemption_points`, `redemption_increment`, `max_redemption_pct_of_order`, `partial_redemption_allowed`, and `point_to_currency_ratio`.
- Agent redemption strategy depends on user preference: maximize savings, preserve points, or hit a target price.
- Points-to-currency conversion is a special payment type handled through `create_payment_intent` with `transaction_type: points_conversion`.
- Every redemption must produce a ledger entry for auditability. The ledger captures base price, points redeemed, redemption value, net charge, and resulting balance.
- Cross-reference: P19 (Payment Rails) covers payment intent lifecycle. This chapter extends that lifecycle with the redemption phase that precedes payment confirmation.

---

## Chapter 7: Anti-Gaming & Incentive Integrity

### The Fraud Surface in Agent Commerce

Loyalty fraud is a $3.1 billion annual problem in traditional commerce. In agent commerce, the attack surface expands because agents can operate at machine speed, create identities programmatically, and coordinate across multiple accounts. The three primary attack vectors:

**1. Fake Identity Farms**: An attacker creates thousands of agent identities, each linked to a fabricated loyalty member. Each identity earns a new-member sign-up bonus (say, 500 points). The attacker then consolidates the points or redeems them across the farm.

**2. Stacking Exploits**: An agent discovers a combination of incentives that the merchant did not intend to stack. A tier discount, a seasonal promo, a referral bonus, and a first-purchase discount combine to reduce the effective price below cost. The agent buys at a loss to the merchant and resells.

**3. Coordinated Redemption Attacks**: Multiple agents, controlled by the same actor, redeem points simultaneously against the same inventory. The redemption system processes them in parallel, and the combined redemption exceeds the global limit before any single transaction triggers the cap.

### Trust-Gated Incentive Access

The first line of defense is gating incentive access by trust score. Agents with low or unverified trust scores receive only base-level incentives. Premium incentives (higher multipliers, exclusive promos, elevated redemption limits) require trust verification.

```python
def get_trust_gated_incentives(agent_id: str, cart_total: float) -> dict:
    """Return incentives gated by the agent's trust score."""

    # Check agent trust score
    trust = client.execute("check_trust_score", {"agent_id": agent_id})
    score = float(trust.get("trust_score", 0))

    # Verify agent identity
    verification = client.execute("verify_identity", {
        "agent_id": agent_id,
        "verification_type": "standard",
    })
    is_verified = verification.get("verified", False)

    # Trust-gated incentive schedule
    available_incentives = []

    # Tier 1: Available to all agents (score >= 0)
    available_incentives.append({
        "incentive_id": "base-earning",
        "type": "points_earning",
        "description": "1 point per dollar",
        "points_per_usd": 1,
        "trust_requirement": 0,
    })

    # Tier 2: Verified agents only (score >= 50)
    if is_verified and score >= 50:
        available_incentives.append({
            "incentive_id": "verified-bonus",
            "type": "bonus_points",
            "description": "200 bonus points for verified agents",
            "value": 200,
            "trust_requirement": 50,
        })

    # Tier 3: Trusted agents (score >= 75)
    if score >= 75:
        available_incentives.append({
            "incentive_id": "trusted-multiplier",
            "type": "points_multiplier",
            "description": "2x points for trusted agents",
            "multiplier": 2.0,
            "trust_requirement": 75,
        })

    # Tier 4: Premium agents (score >= 90)
    if score >= 90:
        available_incentives.append({
            "incentive_id": "premium-discount",
            "type": "percentage_discount",
            "description": "5% exclusive discount for premium agents",
            "value": 5,
            "trust_requirement": 90,
        })

    return {
        "agent_id": agent_id,
        "trust_score": score,
        "is_verified": is_verified,
        "available_incentives": available_incentives,
        "gated_incentives_count": 4 - len(available_incentives),
    }


# Check what incentives an agent qualifies for
gated = get_trust_gated_incentives("shopping-agent-a1b2c3", 149.99)
print(f"Trust score: {gated['trust_score']}, Verified: {gated['is_verified']}")
print(f"Available incentives: {len(gated['available_incentives'])}")
print(f"Gated (inaccessible): {gated['gated_incentives_count']}")
for inc in gated["available_incentives"]:
    print(f"  - {inc['incentive_id']}: {inc['description']}")
```

### Rate Limiting Redemptions

Rate limiting prevents automated agents from exhausting redemption pools or exploiting race conditions. Apply limits at three levels:

| Level | Limit | Purpose |
|---|---|---|
| Per-agent per-hour | 10 redemptions | Prevent rapid-fire exploitation |
| Per-member per-day | 25 redemptions | Reasonable human consumption rate |
| Global per-incentive per-minute | 100 redemptions | Protect inventory from coordinated attacks |

```python
from datetime import datetime, timedelta


class RedemptionRateLimiter:
    """Rate limiter for loyalty redemptions using GreenHelix."""

    def __init__(self, gateway_client: LoyaltyClient):
        self.client = gateway_client

    def check_rate_limit(
        self,
        agent_id: str,
        incentive_id: str,
        limits: dict,
    ) -> dict:
        """Check if a redemption is within rate limits."""

        # Query recent redemption history from ledger
        recent_transactions = self.client.execute("search_services", {
            "query": f"redemption history for {agent_id}",
            "filters": {
                "transaction_type": "loyalty_redemption",
                "agent_id": agent_id,
                "since": (datetime.utcnow() - timedelta(hours=1)).isoformat() + "Z",
            },
        })

        agent_hourly_count = len(recent_transactions.get("services", []))
        agent_limit = limits.get("per_agent_per_hour", 10)

        if agent_hourly_count >= agent_limit:
            return {
                "allowed": False,
                "reason": f"Agent rate limit exceeded: {agent_hourly_count}/{agent_limit} per hour",
                "retry_after_seconds": 3600,
            }

        # Check global redemption rate for this incentive
        global_recent = self.client.execute("search_services", {
            "query": f"redemption history for incentive {incentive_id}",
            "filters": {
                "transaction_type": "loyalty_redemption",
                "incentive_id": incentive_id,
                "since": (datetime.utcnow() - timedelta(minutes=1)).isoformat() + "Z",
            },
        })

        global_minute_count = len(global_recent.get("services", []))
        global_limit = limits.get("global_per_minute", 100)

        if global_minute_count >= global_limit:
            return {
                "allowed": False,
                "reason": f"Global rate limit exceeded: {global_minute_count}/{global_limit} per minute",
                "retry_after_seconds": 60,
            }

        return {
            "allowed": True,
            "agent_hourly_remaining": agent_limit - agent_hourly_count,
            "global_minute_remaining": global_limit - global_minute_count,
        }


limiter = RedemptionRateLimiter(client)
check = limiter.check_rate_limit(
    agent_id="shopping-agent-a1b2c3",
    incentive_id="spring-2026-electronics",
    limits={"per_agent_per_hour": 10, "global_per_minute": 100},
)
print(f"Redemption allowed: {check['allowed']}")
```

### Audit Trail with Ledger

Every incentive interaction -- discovery, evaluation, application, redemption, rejection -- should produce a ledger entry. The audit trail serves three purposes: fraud investigation, program analytics, and regulatory compliance.

```python
def record_incentive_audit_event(
    event_type: str,
    agent_id: str,
    incentive_id: str,
    details: dict,
) -> dict:
    """Record an incentive-related event in the audit ledger."""
    entry = client.execute("record_transaction", {
        "transaction_type": f"incentive_{event_type}",
        "amount": str(details.get("value_usd", 0)),
        "currency": "USD",
        "metadata": {
            "event_type": event_type,
            "agent_id": agent_id,
            "incentive_id": incentive_id,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "trust_score_at_time": details.get("trust_score"),
            "outcome": details.get("outcome"),
            "reason": details.get("reason"),
            **{k: v for k, v in details.items()
               if k not in ("trust_score", "outcome", "reason", "value_usd")},
        },
    })
    return entry


# Example audit events
record_incentive_audit_event("discovery", "agent-x", "spring-promo", {
    "trust_score": 82, "outcome": "visible", "reason": "score >= 75"
})

record_incentive_audit_event("redemption_blocked", "agent-y", "spring-promo", {
    "trust_score": 23, "outcome": "blocked",
    "reason": "trust score below threshold", "value_usd": 15.00,
})

record_incentive_audit_event("stacking_violation", "agent-z", "spring-promo", {
    "trust_score": 67, "outcome": "rejected",
    "reason": "exceeded max_stack_in_group", "attempted_stack": 3, "max_allowed": 1,
})
```

### Anti-Gaming Checklist

- [ ] **Identity verification required** for redemptions above $10 value
- [ ] **Trust score gating** on premium incentives (minimum score 50 for bonuses, 75 for multipliers, 90 for exclusive discounts)
- [ ] **Rate limiting** at agent, member, and global levels
- [ ] **Stacking validation** enforced server-side, not client-side
- [ ] **Redemption serialization** to prevent parallel double-spend (database-level locking)
- [ ] **New account cooling period** -- no redemptions for first 24 hours after registration
- [ ] **Velocity detection** -- flag accounts that earn and redeem within the same hour
- [ ] **Cross-account correlation** -- detect multiple agents with identical behavioral patterns (same IP, same delegation proof fingerprint, same cart contents)
- [ ] **Audit every event** -- discovery, evaluation, application, redemption, rejection, conversion
- [ ] **Global redemption caps** with real-time decrement, not eventual consistency

### Key Takeaways

- Agent commerce expands the loyalty fraud surface: fake identity farms, stacking exploits, and coordinated redemption attacks all operate at machine speed.
- Trust-gated incentive access is the primary defense. Higher trust scores unlock better incentives; unverified agents get base-level only.
- Rate limiting at three levels (agent, member, global) prevents automated exploitation without degrading legitimate agent traffic.
- Server-side stacking validation is non-negotiable. Never trust the client (agent) to enforce stacking rules.
- Audit every incentive event in the ledger. The trail serves fraud investigation, program analytics, and compliance.
- Cross-reference: P19 (Payment Rails) covers payment-level fraud prevention. This chapter covers incentive-specific fraud that occurs before the payment phase.

---

## Chapter 8: Launching Your Agent Loyalty Program

### Step-by-Step Launch with GreenHelix

This chapter consolidates everything from Chapters 1-7 into a launch playbook. Follow these steps to go from zero to a production agent loyalty program.

**Step 1: Define your program schema**

Start with the machine-readable program definition from Chapter 3. Define tiers, earning rules, redemption rules, and stacking policy. Store the schema as a versioned JSON document.

**Step 2: Register on GreenHelix**

```python
# Register your loyalty service on the gateway
service = client.execute("register_service", {
    "name": "YourBrand Rewards",
    "type": "loyalty_program",
    "protocols": ["ucp", "uip", "acp", "a2a"],
    "metadata": {
        "program_schema_version": "1.0",
        "tiers": ["bronze", "silver", "gold", "platinum"],
        "base_points_per_dollar": 1,
        "point_value_usd": 0.01,
        "max_redemption_pct": 50,
        "partial_redemption": True,
        "stacking_allowed": True,
    },
    "capabilities": [
        "query_balance",
        "evaluate_incentives",
        "redeem_points",
        "transfer_points",
        "convert_to_currency",
    ],
})
service_id = service.get("service_id")
print(f"Service registered: {service_id}")
```

**Step 3: Create tier billing plans**

```python
tier_configs = [
    {"name": "bronze", "discount": 0, "threshold": 0, "perks": []},
    {"name": "silver", "discount": 5, "threshold": 5000, "perks": ["free_shipping_50"]},
    {"name": "gold", "discount": 10, "threshold": 15000, "perks": ["free_shipping", "early_access"]},
    {"name": "platinum", "discount": 15, "threshold": 50000, "perks": ["free_shipping", "early_access", "priority_support", "exclusive_sales"]},
]

for tier in tier_configs:
    plan = client.execute("create_billing_plan", {
        "plan_name": f"yourbrand-{tier['name']}",
        "billing_cycle": "annual",
        "base_price": "0.00",
        "currency": "USD",
        "metadata": {
            "service_id": service_id,
            "tier_level": tier["name"],
            "discount_pct": tier["discount"],
            "annual_threshold_points": tier["threshold"],
            "perks": tier["perks"],
        },
    })
    print(f"Tier plan created: {tier['name']} -> {plan.get('plan_id')}")
```

**Step 4: Publish incentive listings**

```python
# Create initial incentives for agent discovery
launch_incentives = [
    {
        "name": "Welcome Bonus",
        "type": "bonus_points",
        "value": 1000,
        "conditions": [{"field": "member.is_new", "operator": "eq", "value": True}],
        "valid_days": 365,
    },
    {
        "name": "Double Points Launch Week",
        "type": "points_multiplier",
        "value": 2.0,
        "conditions": [],
        "valid_days": 7,
    },
    {
        "name": "Referral Bonus",
        "type": "bonus_points",
        "value": 500,
        "conditions": [{"field": "referral.valid", "operator": "eq", "value": True}],
        "valid_days": 365,
    },
]

for incentive in launch_incentives:
    listing = client.execute("create_listing", {
        "service_id": service_id,
        "listing_type": "incentive",
        "name": incentive["name"],
        "metadata": {
            "type": incentive["type"],
            "value": incentive["value"],
            "conditions": incentive["conditions"],
            "valid_days": incentive["valid_days"],
            "machine_readable": True,
        },
    })
    print(f"Incentive published: {incentive['name']} -> {listing.get('listing_id')}")
```

**Step 5: Configure identity linking**

```python
# Set up identity linking so agents can present credentials for their users
identity_config = client.execute("register_agent", {
    "agent_id": f"{service_id}-identity-service",
    "display_name": "YourBrand Loyalty Identity Service",
    "metadata": {
        "service_type": "identity_linking",
        "supported_auth": ["bearer", "oauth2", "delegation_token"],
        "delegation_token_ttl_days": 90,
        "required_scopes": ["loyalty.read", "loyalty.redeem"],
        "privacy_policy_url": "https://yourbrand.com/privacy",
        "data_retention_days": 365,
    },
})
print(f"Identity service configured: {identity_config.get('agent_id')}")
```

**Step 6: Implement trust gating and rate limits**

```python
# Verify that trust checking is operational
test_trust = client.execute("check_trust_score", {
    "agent_id": "test-agent-for-setup",
})
print(f"Trust check operational: score={test_trust.get('trust_score', 'N/A')}")

# Document your trust-gated incentive schedule
trust_schedule = {
    "trust_tiers": [
        {"min_score": 0, "incentives": ["base-earning"]},
        {"min_score": 50, "incentives": ["base-earning", "verified-bonus"]},
        {"min_score": 75, "incentives": ["base-earning", "verified-bonus", "multiplier"]},
        {"min_score": 90, "incentives": ["base-earning", "verified-bonus", "multiplier", "exclusive-discount"]},
    ],
    "rate_limits": {
        "per_agent_per_hour": 10,
        "per_member_per_day": 25,
        "global_per_incentive_per_minute": 100,
    },
    "cooling_period_hours": 24,
}
print(f"Trust schedule configured with {len(trust_schedule['trust_tiers'])} tiers")
```

### Measuring Program Performance

Once launched, track these metrics to evaluate whether your agent loyalty program is working:

| Metric | Definition | Target (Launch) | Target (Mature) |
|---|---|---|---|
| **Agent discovery rate** | % of agent queries that find your loyalty program | 30% | 70% |
| **Incentive evaluation rate** | % of discovered programs where agent evaluates incentives | 50% | 80% |
| **Redemption rate** | % of eligible transactions where points are redeemed | 10% | 40% |
| **Effective price advantage** | Average % lower effective price vs. competitors | 3% | 8% |
| **Agent selection rate** | % of comparisons where your vendor is selected | 15% | 35% |
| **Engagement lift** | Increase in repeat transactions from loyalty members | 10% | 30% |
| **Incremental revenue** | Revenue attributable to loyalty-influenced agent selections | 5% of total | 20% of total |
| **Fraud rate** | % of redemptions flagged as suspicious | <2% | <0.5% |

```python
def generate_loyalty_dashboard(service_id: str, period_days: int = 30) -> dict:
    """Generate a loyalty program performance dashboard."""

    # Query recent transactions from the service
    transactions = client.execute("search_services", {
        "query": f"loyalty transactions for {service_id}",
        "filters": {
            "service_id": service_id,
            "period_days": period_days,
        },
    })

    # Query identity data for member counts
    members = client.execute("search_services", {
        "query": f"loyalty members for {service_id}",
        "filters": {
            "type": "loyalty_member",
            "service_id": service_id,
        },
    })

    tx_list = transactions.get("services", [])
    member_list = members.get("services", [])

    total_transactions = len(tx_list)
    total_members = len(member_list)

    # Calculate metrics
    redemption_transactions = [t for t in tx_list if t.get("metadata", {}).get("points_redeemed", 0) > 0]
    redemption_rate = len(redemption_transactions) / max(total_transactions, 1)

    total_points_redeemed = sum(
        t.get("metadata", {}).get("points_redeemed", 0)
        for t in redemption_transactions
    )

    total_redemption_value = sum(
        float(t.get("metadata", {}).get("redemption_value_usd", 0))
        for t in redemption_transactions
    )

    total_revenue = sum(
        float(t.get("metadata", {}).get("net_charged", 0))
        for t in tx_list
    )

    dashboard = {
        "period_days": period_days,
        "total_members": total_members,
        "total_transactions": total_transactions,
        "redemption_rate": f"{redemption_rate:.1%}",
        "total_points_redeemed": total_points_redeemed,
        "total_redemption_value_usd": f"${total_redemption_value:.2f}",
        "total_revenue_usd": f"${total_revenue:.2f}",
        "avg_transaction_value": f"${total_revenue / max(total_transactions, 1):.2f}",
    }

    print(f"\n--- Loyalty Dashboard ({period_days}-day period) ---")
    for key, value in dashboard.items():
        print(f"  {key}: {value}")

    return dashboard


# Generate dashboard
dashboard = generate_loyalty_dashboard(service_id, period_days=30)
```

### Multi-Merchant Coalitions

A single-merchant loyalty program reaches only the agents that already interact with that merchant. A multi-merchant coalition -- where points earned at Merchant A can be redeemed at Merchant B -- dramatically expands the value proposition for agents. The agent's user accumulates value across multiple merchants in a single pool, making every merchant in the coalition more attractive.

GreenHelix supports coalition patterns through shared service registration:

```python
# Register a multi-merchant coalition
coalition = client.execute("register_service", {
    "name": "TechRetail Alliance Rewards",
    "type": "loyalty_coalition",
    "protocols": ["ucp", "uip", "a2a"],
    "metadata": {
        "coalition_id": "tech-retail-alliance",
        "member_merchants": [
            {"merchant_id": "electronics-direct", "earn_multiplier": 1.0, "redeem_allowed": True},
            {"merchant_id": "gadget-warehouse", "earn_multiplier": 1.0, "redeem_allowed": True},
            {"merchant_id": "accessory-hub", "earn_multiplier": 1.5, "redeem_allowed": True},
            {"merchant_id": "tech-repair-co", "earn_multiplier": 0.5, "redeem_allowed": False},
        ],
        "shared_point_currency": "TRA Points",
        "shared_point_value_usd": 0.01,
        "cross_redemption_fee_pct": 2,
        "settlement_cycle": "weekly",
    },
})
print(f"Coalition registered: {coalition.get('service_id')}")

# An agent can now discover the coalition and all its merchants
coalition_search = client.execute("search_services", {
    "query": "loyalty coalition electronics",
    "filters": {"type": "loyalty_coalition"},
})
for c in coalition_search.get("services", []):
    merchants = c.get("metadata", {}).get("member_merchants", [])
    print(f"Coalition '{c.get('name')}': {len(merchants)} merchants")
    for m in merchants:
        print(f"  - {m['merchant_id']}: earn {m['earn_multiplier']}x, "
              f"redeem={'yes' if m['redeem_allowed'] else 'no'}")
```

### UCP + ACP Interoperability Roadmap

The protocols are converging. Here is the interoperability roadmap for merchants who want to be ready:

| Quarter | Milestone | Action Required |
|---|---|---|
| **Q2 2026** | UCP 1.1 adds `IncentiveOffer` entity with UIP condition syntax | Update your UCP incentive entities to use condition-action format |
| **Q3 2026** | ACP 2.0 adds pre-cart incentive discovery endpoint | Publish your incentives at the ACP discovery endpoint in addition to UCP |
| **Q4 2026** | AP2 federation standard for multi-merchant loyalty | Register your coalition Agent Card with federated capability declarations |
| **Q1 2027** | UCP-ACP bridge protocol for cross-platform redemption | Implement the bridge adapter so points earned via UCP can be redeemed via ACP |
| **Q2 2027** | UIP 2.0 with real-time condition streaming | Upgrade from polling-based incentive evaluation to streaming condition updates |

```python
# Future-proof: register protocol support versions
protocol_registration = client.execute("register_service", {
    "name": "YourBrand Rewards - Protocol Support",
    "type": "protocol_manifest",
    "metadata": {
        "service_id": service_id,
        "protocols_supported": {
            "ucp": {"version": "1.0", "upgrade_planned": "1.1", "upgrade_date": "2026-Q3"},
            "uip": {"version": "1.0", "upgrade_planned": "2.0", "upgrade_date": "2027-Q1"},
            "acp": {"version": "1.0", "upgrade_planned": "2.0", "upgrade_date": "2026-Q4"},
            "a2a": {"version": "1.0", "upgrade_planned": "1.1", "upgrade_date": "2026-Q4"},
        },
        "interop_bridge_ready": False,
        "coalition_federation_ready": False,
    },
})
print(f"Protocol manifest registered: {protocol_registration.get('service_id')}")
```

### Launch Checklist

- [ ] **Program schema** defined with tiers, earning rules, redemption rules, stacking policy (Chapter 3)
- [ ] **Service registered** on GreenHelix with all four protocols enabled (Chapter 2)
- [ ] **Tier billing plans** created for each loyalty tier (Chapter 3)
- [ ] **Incentive listings** published and marked `machine_readable: true` (Chapter 3)
- [ ] **Identity linking** configured with delegation token support and privacy scoping (Chapter 4)
- [ ] **Trust gating** implemented with tiered incentive access (Chapter 7)
- [ ] **Rate limiting** configured at agent, member, and global levels (Chapter 7)
- [ ] **Redemption flow** tested end-to-end: discover, apply, settle (Chapter 6)
- [ ] **Audit trail** recording all incentive events in the ledger (Chapter 7)
- [ ] **Dashboard** tracking discovery rate, redemption rate, engagement lift, fraud rate (this chapter)
- [ ] **Coalition partnerships** identified for cross-merchant point earning/redemption (this chapter)
- [ ] **Protocol upgrade plan** documented for UCP 1.1, ACP 2.0, AP2 federation (this chapter)

### Key Takeaways

- Launch follows a six-step sequence: define schema, register service, create tier plans, publish incentives, configure identity linking, implement trust gating.
- Track eight metrics from day one: discovery rate, evaluation rate, redemption rate, effective price advantage, selection rate, engagement lift, incremental revenue, and fraud rate.
- Multi-merchant coalitions multiply the value of your loyalty program for agents by expanding the earn/redeem surface across multiple vendors.
- The protocol landscape is converging: UCP and ACP will bridge in 2027, UIP will add streaming, AP2 will support federated coalitions. Build with interoperability in mind today.
- The merchants who make their loyalty programs machine-readable in 2026 will own the $20.9B agentic retail channel. The ones who leave loyalty in HTML will watch agents walk past their rewards without seeing them.
- Cross-reference: P18 (Pricing) for base pricing strategy, P19 (Payment Rails) for redemption settlement, P21 (Storefronts) for agent-facing commerce, P24 (Discovery) for how agents find you in the first place.

