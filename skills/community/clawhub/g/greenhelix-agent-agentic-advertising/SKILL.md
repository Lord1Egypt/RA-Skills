---
name: greenhelix-agent-agentic-advertising
version: "1.3.1"
description: "Agentic Advertising: Build Autonomous Media-Buying Agents. Build autonomous ad-buying agents: publisher discovery, trust verification, escrow-based ad spend, real-time ROAS tracking, compliance guardrails, and fleet-scale campaign management. Includes detailed Python code examples with full API integration."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [advertising, adcp, media-buying, programmatic, escrow, roas, guide, greenhelix, openclaw, ai-agent]
price_usd: 29.0
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
# Agentic Advertising: Build Autonomous Media-Buying Agents

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `AGENT_SIGNING_KEY`: Cryptographic signing key for agent identity (Ed25519 key pair for request signing)


In December 2025, PubMatic and Butler/Till ran the first fully autonomous CTV campaign. A Claude-powered agent received a campaign brief, selected inventory, placed bids, optimized creative rotation, and reported results -- all without a human touching a DSP UI. Setup time dropped 87%. ROAS improved 31% over the manual baseline. Two months later, the Ad Context Protocol (AdCP) launched with backing from PubMatic, Scope3, Yahoo, and Samba.TV, providing a standardized interface for agents to interact with the programmatic supply chain. The IAB Tech Lab followed in January 2026 with an agentic advertising roadmap, effectively acknowledging that manual programmatic buying is ending. eMarketer declared 2026 the beginning of the end for human-operated media desks.
The infrastructure for autonomous ad buying exists. What most teams lack is the commerce layer underneath it: how does an ad-buying agent hold budget securely, discover and verify publishers programmatically, release payment only on confirmed delivery, and operate within compliance guardrails -- all without a human approving each transaction?
This guide builds that layer using the GreenHelix A2A Commerce Gateway. You will register media-buying agents with cryptographic identities, discover and verify publishers through a searchable marketplace, hold ad budgets in escrow that releases only on verified impressions, track ROAS and attention signals in real time, enforce spending caps and approval workflows, and scale from a single campaign to a fleet of autonomous buyers. Every concept comes with working Python code against the GreenHelix API.

## What You'll Learn
- Chapter 1: The Agentic Advertising Landscape
- Chapter 2: Agent Architecture for Media Buying
- Chapter 3: Publisher Discovery and Trust Verification via GreenHelix Marketplace
- Chapter 4: Implementing the AdCP Media Buy Protocol
- Chapter 5: Escrow-Based Ad Spend
- Chapter 6: Real-Time Campaign Analytics
- Chapter 7: Compliance Guardrails
- Next Steps
- What You Get

## Full Guide

# Agentic Advertising: Build Autonomous Media-Buying Agents

In December 2025, PubMatic and Butler/Till ran the first fully autonomous CTV campaign. A Claude-powered agent received a campaign brief, selected inventory, placed bids, optimized creative rotation, and reported results -- all without a human touching a DSP UI. Setup time dropped 87%. ROAS improved 31% over the manual baseline. Two months later, the Ad Context Protocol (AdCP) launched with backing from PubMatic, Scope3, Yahoo, and Samba.TV, providing a standardized interface for agents to interact with the programmatic supply chain. The IAB Tech Lab followed in January 2026 with an agentic advertising roadmap, effectively acknowledging that manual programmatic buying is ending. eMarketer declared 2026 the beginning of the end for human-operated media desks.

The infrastructure for autonomous ad buying exists. What most teams lack is the commerce layer underneath it: how does an ad-buying agent hold budget securely, discover and verify publishers programmatically, release payment only on confirmed delivery, and operate within compliance guardrails -- all without a human approving each transaction?

This guide builds that layer using the GreenHelix A2A Commerce Gateway. You will register media-buying agents with cryptographic identities, discover and verify publishers through a searchable marketplace, hold ad budgets in escrow that releases only on verified impressions, track ROAS and attention signals in real time, enforce spending caps and approval workflows, and scale from a single campaign to a fleet of autonomous buyers. Every concept comes with working Python code against the GreenHelix API.

---


> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## Table of Contents

1. [The Agentic Advertising Landscape](#chapter-1-the-agentic-advertising-landscape)
2. [Agent Architecture for Media Buying](#chapter-2-agent-architecture-for-media-buying)
3. [Publisher Discovery and Trust Verification](#chapter-3-publisher-discovery-and-trust-verification)
4. [Implementing the AdCP Media Buy Protocol](#chapter-4-implementing-the-adcp-media-buy-protocol)
5. [Escrow-Based Ad Spend](#chapter-5-escrow-based-ad-spend)
6. [Real-Time Campaign Analytics](#chapter-6-real-time-campaign-analytics)
7. [Compliance Guardrails](#chapter-7-compliance-guardrails)

---

## Chapter 1: The Agentic Advertising Landscape

### AdCP, AgenticOS, and Why Manual Buying Is Ending

The programmatic advertising stack was built for humans. A media buyer opens a DSP, creates a line item, sets targeting parameters, uploads creative, defines a budget, launches, monitors a dashboard, adjusts bids, pauses underperformers, and writes a report. This workflow made sense when campaigns numbered in the dozens. It breaks down at the scale the market now demands: thousands of micro-campaigns across CTV, DOOH, audio, retail media, and social -- each requiring real-time optimization against attention signals, supply path quality metrics, and carbon impact scores that no human can process fast enough.

Three developments in late 2025 and early 2026 changed the trajectory permanently.

**PubMatic + Butler/Till: The First Autonomous CTV Campaign.** In December 2025, Butler/Till deployed a Claude-powered agent that executed an end-to-end CTV buy on PubMatic's platform. The agent ingested a campaign brief (target audience, KPIs, budget, flight dates), queried available inventory, evaluated supply paths for quality and fraud signals, placed bids, monitored delivery in real time, shifted spend toward high-performing segments, and generated post-campaign reports. The results: 87% reduction in campaign setup time and 31% improvement in ROAS over the manual baseline. The agent did not assist a human buyer. It replaced the human buyer for that campaign.

**The Ad Context Protocol (AdCP).** Launched in early 2026, AdCP provides a standardized protocol for AI agents to interact with the advertising ecosystem. Backed by PubMatic, Scope3, Yahoo, and Samba.TV, AdCP defines four modules:

```
+---------------------------------------------------------------------+
|                     Ad Context Protocol (AdCP)                       |
+---------------------------------------------------------------------+
|                                                                       |
|  +----------------+  +----------------+  +----------+  +-----------+ |
|  |    Signals      |  |   Media Buy    |  | Creative |  | Curation  | |
|  |   Activation    |  |                |  |          |  |           | |
|  +----------------+  +----------------+  +----------+  +-----------+ |
|  | Audience data   |  | Inventory      |  | Asset    |  | Supply    | |
|  | Attention       |  | Bidding        |  | variants |  | path      | |
|  | Context         |  | Budget mgmt    |  | Testing  |  | quality   | |
|  | Carbon impact   |  | Pacing         |  | Rotation |  | Filtering | |
|  +----------------+  +----------------+  +----------+  +-----------+ |
|                                                                       |
+---------------------------------------------------------------------+
```

Each module exposes structured interfaces that agents can call programmatically. Signals Activation provides audience and attention data. Media Buy handles inventory selection, bidding, and budget pacing. Creative manages asset variants and rotation. Curation filters supply paths for quality, brand safety, and sustainability.

The significance of AdCP is not any single module -- it is the standardization. Before AdCP, every DSP, SSP, and data provider had its own API, its own authentication model, its own response format. An agent integrating with The Trade Desk looked nothing like an agent integrating with DV360. AdCP provides a common vocabulary: an agent that speaks AdCP can interact with any AdCP-compliant platform without platform-specific code. This is the same inflection point that OpenRTB created for programmatic bidding in 2012, but for agent-driven workflows instead of server-to-server auctions.

**IAB Tech Lab Agentic Advertising Roadmap.** Released January 2026, the roadmap defines standards for agent identity, capability negotiation, and transaction logging in advertising workflows. It explicitly positions autonomous agents as first-class participants in the programmatic supply chain -- not just tools assisting human traders, but independent actors executing campaigns. The roadmap identifies three phases: assisted automation (agents helping humans, 2024-2025), supervised autonomy (agents acting with human oversight, 2026), and full autonomy (agents acting independently within defined guardrails, 2027+). Most production systems today operate in the supervised autonomy phase, which is exactly what this guide targets: agents that execute campaigns independently but within programmable compliance boundaries.

### Why Manual Buying Cannot Scale

The math is straightforward. A skilled media buyer can manage 10-20 campaigns simultaneously, monitoring performance dashboards, adjusting bids, reviewing creative reports, and communicating with publishers. Each campaign requires roughly 2-4 hours per week of active management. A mid-size agency running 200 campaigns needs 10-20 buyers. A large agency running 2,000 campaigns needs 100-200 buyers.

Now consider the fragmentation: CTV alone has 85+ streaming platforms, each with distinct inventory characteristics, audience profiles, and measurement capabilities. DOOH spans 500,000+ screens in the US. Retail media networks number 50+ and growing. Each channel, each platform, each publisher requires targeting decisions, bid adjustments, creative variants, and performance analysis. The combinatorial explosion of campaigns multiplied by channels multiplied by publishers multiplied by creative variants exceeds human cognitive bandwidth by orders of magnitude.

Autonomous agents eliminate this bottleneck. An agent does not get tired at 3am when a campaign is pacing behind. An agent does not forget to check a publisher's IVT rate before releasing budget. An agent can evaluate 200 publishers in the time a human evaluates 5. The 31% ROAS improvement PubMatic reported is not because agents are smarter than humans -- it is because agents are faster, more consistent, and operate 24/7 without attention fatigue.

### The Missing Commerce Layer

AdCP tells agents how to buy media. It does not tell agents how to hold money safely, verify that a publisher is trustworthy before committing budget, release payment only when impressions are actually delivered, or enforce spending limits without a human checking a dashboard. These are commerce problems, not advertising protocol problems.

Consider the lifecycle of an autonomous media buy:

```
Campaign Brief
      |
      v
+------------------+     +-------------------+     +------------------+
| Agent registers  |---->| Agent discovers   |---->| Agent evaluates  |
| identity, gets   |     | publishers via    |     | publisher trust  |
| wallet, receives |     | marketplace       |     | scores, supply   |
| delegated budget |     | search            |     | path quality     |
+------------------+     +-------------------+     +------------------+
                                                           |
                                                           v
+------------------+     +-------------------+     +------------------+
| Agent monitors   |<----| Escrow holds ad   |<----| Agent negotiates |
| delivery, tracks |     | budget until      |     | terms, locks     |
| ROAS, attention  |     | verified delivery |     | budget in escrow |
| signals          |     |                   |     |                  |
+------------------+     +-------------------+     +------------------+
      |
      v
+------------------+     +-------------------+
| Release escrow   |---->| Log transaction,  |
| on confirmed     |     | update reputation,|
| impressions, or  |     | report to         |
| cancel on fraud  |     | compliance        |
+------------------+     +-------------------+
```

Every box in that diagram requires commerce infrastructure: agent identity and wallets, publisher discovery and trust scoring, escrow-based budget management, real-time analytics, compliance guardrails, and fleet-scale monitoring. This guide implements each box.

### What You Will Build

By the end of this guide, you will have:

- A media-buying agent with a cryptographic identity, wallet, and delegated budget authority
- A publisher discovery pipeline that searches, scores, and ranks publishers by trust and supply path quality
- An AdCP-aligned campaign execution flow with escrow-backed budget management
- Real-time ROAS tracking with attention signal integration
- Compliance guardrails including spending caps, approval workflows, and audit trails
- A production deployment pattern for scaling to a fleet of autonomous buyers

All code runs against the GreenHelix A2A Commerce Gateway at `https://api.greenhelix.net/v1`.

---

## Chapter 2: Agent Architecture for Media Buying

### Identity, Wallets, and Budget Delegation

Every autonomous media buyer needs three things before it can spend a dollar: a verified identity that other agents and publishers can authenticate, a wallet to hold funds, and delegated authority defining how much it can spend and on what. This chapter builds all three.

The identity question is particularly important in advertising. A publisher receiving a bid needs to know: is this buyer legitimate? Does it represent a real advertiser? Does it have actual budget authority? In human-operated programmatic, these questions are answered by platform accounts, contracts, and business relationships. In autonomous buying, they must be answered cryptographically. GreenHelix agents use Ed25519 keypairs bound to registered profiles, giving publishers a verifiable identity to check before accepting bids and delivering impressions.

The wallet question is equally critical. In traditional programmatic, budget management happens inside the DSP -- the buyer sets a daily cap, and the DSP enforces it. When the agent operates across multiple publishers directly (as AdCP enables), there is no single DSP enforcing caps. The wallet becomes the budget enforcement mechanism: the agent can only commit funds that exist in its wallet, and escrow creation atomically deducts from available balance.

### Setup

```python
import requests
import json
import time
from datetime import datetime, timedelta

base_url = "https://api.greenhelix.net/v1"
api_key = "your-api-key"  # From GreenHelix dashboard

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"
session.headers["Content-Type"] = "application/json"

def execute(tool: str, inputs: dict) -> dict:
    """Execute a GreenHelix tool and return the result."""
    resp = session.post(
        f"{base_url}/v1",
        json={"tool": tool, "input": inputs}
    )
    resp.raise_for_status()
    return resp.json()
```

### Register the Media-Buying Agent

An agent identity on GreenHelix is an Ed25519 keypair bound to a profile. The profile declares the agent's capabilities, tier, and metadata. For a media buyer, the capabilities describe what it can do (buy media, manage campaigns, report analytics) and what it needs from counterparties (verified inventory, impression verification, brand safety).

```python
# Register the primary media-buying agent
buyer_agent = execute("register_agent", {
    "name": "media-buyer-ctv-01",
    "description": "Autonomous CTV media buyer. Executes campaign briefs "
                   "against verified publisher inventory with escrow-backed "
                   "budget management.",
    "capabilities": [
        "media_buying",
        "campaign_optimization",
        "bid_management",
        "roas_tracking",
        "supply_path_verification"
    ],
    "metadata": {
        "agent_type": "media_buyer",
        "channels": ["ctv", "dooh", "audio"],
        "adcp_version": "1.0",
        "max_daily_spend": 50000,
        "organization": "your-org-id"
    }
})

buyer_agent_id = buyer_agent["agent_id"]
print(f"Buyer agent registered: {buyer_agent_id}")
```

### Create the Campaign Wallet

Each campaign should have its own wallet. This isolates campaign budgets from each other -- a runaway optimization loop on Campaign A cannot drain Campaign B's funds.

```python
# Create a dedicated wallet for a CTV campaign
campaign_wallet = execute("create_wallet", {
    "agent_id": buyer_agent_id,
    "label": "ctv-q2-2026-brand-awareness",
    "metadata": {
        "campaign_id": "camp-2026-q2-001",
        "channel": "ctv",
        "objective": "brand_awareness",
        "flight_start": "2026-04-15",
        "flight_end": "2026-05-15",
        "total_budget": 150000
    }
})

wallet_id = campaign_wallet["wallet_id"]
print(f"Campaign wallet created: {wallet_id}")
```

### Budget Delegation Architecture

In a manual buying workflow, a human approves each IO (insertion order). In an autonomous workflow, you pre-authorize spending with explicit limits. GreenHelix models this through wallet balances and escrow caps -- the agent can only lock funds that exist in its wallet, and each escrow is an explicit commitment.

The architecture for a multi-campaign organization looks like this:

```
+---------------------------------------------------------------+
|                    Organization Master Wallet                   |
|                    Balance: $500,000                            |
+---------------------------------------------------------------+
        |                    |                    |
        v                    v                    v
+---------------+   +---------------+   +---------------+
| CTV Campaign  |   | DOOH Campaign |   | Audio Campaign|
| Wallet        |   | Wallet        |   | Wallet        |
| $150,000      |   | $200,000      |   | $150,000      |
+---------------+   +---------------+   +---------------+
    |       |            |       |            |
    v       v            v       v            v
+------+ +------+   +------+ +------+   +------+
|Escrow| |Escrow|   |Escrow| |Escrow|   |Escrow|
|Pub A | |Pub B |   |Pub C | |Pub D |   |Pub E |
|$25K  | |$40K  |   |$60K  | |$50K  |   |$35K  |
+------+ +------+   +------+ +------+   +------+
```

Each escrow is a commitment to a specific publisher for a specific flight. The agent creates escrows as it negotiates deals, and each creation deducts from the campaign wallet balance. This prevents over-commitment: the agent cannot promise more than it has.

### Register Supporting Agents

A production media-buying operation needs more than one agent. At minimum, you need a buyer, an analyst, and a compliance monitor.

```python
# Register an analytics agent that tracks campaign performance
analyst_agent = execute("register_agent", {
    "name": "campaign-analyst-01",
    "description": "Tracks ROAS, attention signals, and supply path quality "
                   "for active campaigns. Provides optimization recommendations.",
    "capabilities": [
        "analytics",
        "roas_calculation",
        "attention_tracking",
        "supply_path_analysis"
    ],
    "metadata": {
        "agent_type": "analyst",
        "reports_to": buyer_agent_id
    }
})

analyst_id = analyst_agent["agent_id"]

# Register a compliance agent that enforces spending guardrails
compliance_agent = execute("register_agent", {
    "name": "compliance-monitor-01",
    "description": "Monitors ad spend against approved budgets, enforces "
                   "spending caps, flags anomalies, and maintains audit trails.",
    "capabilities": [
        "compliance_monitoring",
        "spend_tracking",
        "anomaly_detection",
        "audit_logging"
    ],
    "metadata": {
        "agent_type": "compliance",
        "authority_level": "can_pause_campaigns",
        "reports_to": buyer_agent_id
    }
})

compliance_id = compliance_agent["agent_id"]
print(f"Analyst: {analyst_id}, Compliance: {compliance_id}")
```

### Check Wallet Balance

Before any buying begins, verify the wallet is funded and the balance matches expectations.

```python
balance = execute("get_balance", {
    "agent_id": buyer_agent_id,
    "wallet_id": wallet_id
})

print(f"Available balance: ${balance['available']}")
print(f"Locked in escrow:  ${balance['locked']}")
print(f"Total:             ${balance['total']}")

# Verify sufficient funds for the campaign
assert balance["available"] >= 150000, "Insufficient campaign budget"
```

---

## Chapter 3: Publisher Discovery and Trust Verification via GreenHelix Marketplace

### Finding and Vetting Publishers Programmatically

In manual buying, a media planner reviews a spreadsheet of publishers, checks comScore data, reviews ads.txt files, and calls a few sales reps. An autonomous agent needs to do this in seconds, programmatically, with quantifiable trust signals. GreenHelix's marketplace provides `search_services` for broad discovery and `best_match` for ranked results, backed by reputation scores and verifiable claim chains.

Publisher trust is the single highest-risk decision in autonomous ad buying. A buyer agent that sends budget to a fraudulent publisher loses money with no recourse. In human-operated buying, trust accumulates through years of business relationships, industry conferences, and institutional knowledge ("Publisher X has a great CTV app" or "Publisher Y had an IVT problem last year"). An autonomous agent has none of this institutional memory. It needs a system that quantifies trust from verifiable evidence: transaction history, delivery performance, IVT rates across past campaigns, dispute outcomes, and supply chain transparency.

GreenHelix provides this through three mechanisms. First, `search_services` discovers publishers that match capability requirements. Second, `get_agent_reputation` and `build_claim_chain` provide trust evidence -- not just a score, but the cryptographically signed records behind it. Third, `search_agents_by_metrics` surfaces historical performance data that the agent can use to make its own trust calculation rather than relying on a single opaque number.

### Search for CTV Publishers

```python
# Broad search for CTV inventory providers
ctv_publishers = execute("search_services", {
    "query": "ctv inventory premium connected television advertising",
    "filters": {
        "capabilities": ["ctv_inventory", "impression_verification"],
        "min_reputation": 0.7,
        "status": "active"
    },
    "limit": 20
})

print(f"Found {len(ctv_publishers['results'])} CTV publishers")
for pub in ctv_publishers["results"]:
    print(f"  {pub['name']} - reputation: {pub['reputation_score']:.2f} "
          f"- capabilities: {pub['capabilities']}")
```

### Ranked Publisher Matching

`best_match` goes beyond keyword search. It ranks publishers against your specific requirements -- channel, audience overlap, supply path quality, historical performance, and price.

```python
# Find the best publisher match for a specific campaign brief
best_publishers = execute("best_match", {
    "requirements": {
        "channel": "ctv",
        "audience": "adults_25_54",
        "geography": "united_states",
        "min_impressions": 1000000,
        "max_cpm": 35.00,
        "brand_safety": "strict",
        "supply_path": "direct_or_one_hop",
        "viewability_threshold": 0.90,
        "attention_signals_required": True
    },
    "limit": 10,
    "sort_by": "combined_score"
})

for i, match in enumerate(best_publishers["results"]):
    print(f"\n#{i+1}: {match['name']}")
    print(f"  Match score:    {match['score']:.2f}")
    print(f"  Reputation:     {match['reputation_score']:.2f}")
    print(f"  Estimated CPM:  ${match.get('estimated_cpm', 'N/A')}")
    print(f"  Supply path:    {match.get('supply_path_hops', 'N/A')} hops")
```

### Verify Publisher Reputation

A reputation score is a summary. To make a high-stakes budget commitment, you need the underlying evidence. GreenHelix's claim chains provide cryptographically verifiable proof of past performance.

```python
def verify_publisher(publisher_id: str) -> dict:
    """Deep verification of a publisher before committing budget."""

    # Get the aggregate reputation score
    reputation = execute("get_agent_reputation", {
        "agent_id": publisher_id
    })

    # Get the verifiable claim chain -- signed records of past
    # transactions, delivery rates, dispute outcomes
    claims = execute("build_claim_chain", {
        "agent_id": publisher_id,
        "claim_types": [
            "delivery_rate",
            "impression_verification",
            "dispute_outcomes",
            "supply_path_declarations"
        ]
    })

    # Search for performance metrics submitted by this publisher
    metrics = execute("search_agents_by_metrics", {
        "filters": {
            "agent_id": publisher_id,
            "metric_types": [
                "fill_rate",
                "viewability_rate",
                "invalid_traffic_rate",
                "attention_score"
            ]
        }
    })

    verification = {
        "publisher_id": publisher_id,
        "reputation_score": reputation["score"],
        "total_transactions": reputation.get("total_transactions", 0),
        "dispute_rate": reputation.get("dispute_rate", 0),
        "claim_chain_length": len(claims.get("claims", [])),
        "claims_verified": all(
            c.get("verified", False) for c in claims.get("claims", [])
        ),
        "avg_fill_rate": None,
        "avg_viewability": None,
        "ivt_rate": None
    }

    # Extract metric averages
    for metric in metrics.get("results", []):
        if metric["metric_type"] == "fill_rate":
            verification["avg_fill_rate"] = metric["value"]
        elif metric["metric_type"] == "viewability_rate":
            verification["avg_viewability"] = metric["value"]
        elif metric["metric_type"] == "invalid_traffic_rate":
            verification["ivt_rate"] = metric["value"]

    return verification

# Verify the top-ranked publisher
top_publisher = best_publishers["results"][0]
pub_verification = verify_publisher(top_publisher["agent_id"])

print(f"Publisher: {top_publisher['name']}")
print(f"  Reputation score:   {pub_verification['reputation_score']:.2f}")
print(f"  Total transactions: {pub_verification['total_transactions']}")
print(f"  Dispute rate:       {pub_verification['dispute_rate']:.1%}")
print(f"  Claims verified:    {pub_verification['claims_verified']}")
print(f"  Avg fill rate:      {pub_verification['avg_fill_rate']}")
print(f"  Avg viewability:    {pub_verification['avg_viewability']}")
print(f"  IVT rate:           {pub_verification['ivt_rate']}")
```

### Supply Path Quality Scoring

Supply path optimization (SPO) is critical for programmatic efficiency. Every intermediary between your bid and the publisher's ad server adds cost, latency, and fraud risk. Use the reputation and metrics data to build a supply path quality score.

```python
def score_supply_path(publisher_id: str, verification: dict) -> float:
    """Score a publisher's supply path quality from 0.0 to 1.0.

    Weights:
      - Direct path (fewer hops) = 30%
      - Low IVT rate             = 25%
      - High viewability         = 25%
      - Low dispute rate         = 20%
    """
    score = 0.0

    # Supply path directness (from best_match data)
    hops = verification.get("supply_path_hops", 3)
    if hops <= 1:
        score += 0.30
    elif hops == 2:
        score += 0.15
    # 3+ hops: no points

    # IVT rate (lower is better)
    ivt = verification.get("ivt_rate", 0.05)
    if ivt is not None:
        if ivt < 0.01:
            score += 0.25
        elif ivt < 0.03:
            score += 0.15
        elif ivt < 0.05:
            score += 0.05

    # Viewability (higher is better)
    view = verification.get("avg_viewability", 0.5)
    if view is not None:
        if view >= 0.90:
            score += 0.25
        elif view >= 0.70:
            score += 0.15
        elif view >= 0.50:
            score += 0.05

    # Dispute rate (lower is better)
    disputes = verification.get("dispute_rate", 0.05)
    if disputes < 0.01:
        score += 0.20
    elif disputes < 0.03:
        score += 0.10

    return score

# Score all verified publishers
scored_publishers = []
for pub in best_publishers["results"][:5]:
    v = verify_publisher(pub["agent_id"])
    v["supply_path_hops"] = pub.get("supply_path_hops", 2)
    spq = score_supply_path(pub["agent_id"], v)
    scored_publishers.append({
        "publisher": pub,
        "verification": v,
        "supply_path_quality": spq
    })

# Sort by supply path quality
scored_publishers.sort(key=lambda x: x["supply_path_quality"], reverse=True)

print("\nPublisher Rankings by Supply Path Quality:")
for i, sp in enumerate(scored_publishers):
    print(f"  #{i+1} {sp['publisher']['name']}: "
          f"SPQ={sp['supply_path_quality']:.2f}, "
          f"Rep={sp['verification']['reputation_score']:.2f}")
```

---

## Chapter 4: Implementing the AdCP Media Buy Protocol

### From Brief to Autonomous Execution

AdCP defines four modules -- Signals Activation, Media Buy, Creative, and Curation -- that together represent the full lifecycle of a programmatic campaign. This chapter maps each module to GreenHelix tools, building an end-to-end autonomous execution pipeline.

### Campaign Brief Structure

The campaign brief is the input to the entire system. It encodes everything the agent needs to execute autonomously.

```python
campaign_brief = {
    "campaign_id": "camp-2026-q2-001",
    "advertiser": "acme-streaming",
    "objective": "brand_awareness",
    "channel": "ctv",
    "flight": {
        "start": "2026-04-15",
        "end": "2026-05-15"
    },
    "budget": {
        "total": 150000,
        "daily_cap": 5000,
        "currency": "USD"
    },
    "audience": {
        "age_range": "25-54",
        "geography": "US",
        "interests": ["streaming", "entertainment", "technology"],
        "household_income": "top_40_percent"
    },
    "kpis": {
        "target_roas": 3.5,
        "min_viewability": 0.90,
        "max_ivt_rate": 0.02,
        "min_attention_score": 0.7
    },
    "creative": {
        "assets": ["creative-15s-v1", "creative-30s-v1", "creative-30s-v2"],
        "rotation_strategy": "optimize_attention"
    },
    "brand_safety": {
        "level": "strict",
        "blocked_categories": ["adult", "violence", "gambling"],
        "required_certifications": ["tag_certified", "mrc_accredited"]
    }
}
```

### Module 1: Signals Activation

Signals Activation gathers audience data, attention signals, and contextual information to inform targeting decisions. In GreenHelix, this maps to discovering and querying data providers.

```python
def activate_signals(brief: dict) -> dict:
    """Query signal providers for audience and attention data."""

    # Find signal providers in the marketplace
    signal_providers = execute("search_services", {
        "query": "audience data attention signals ctv measurement",
        "filters": {
            "capabilities": ["audience_data", "attention_measurement"],
            "min_reputation": 0.8
        },
        "limit": 5
    })

    # Create a payment intent for signal data access
    signal_intent = execute("create_intent", {
        "agent_id": buyer_agent_id,
        "amount": "500.00",
        "currency": "USD",
        "description": f"Signal activation for campaign {brief['campaign_id']}",
        "metadata": {
            "campaign_id": brief["campaign_id"],
            "signal_types": ["audience", "attention", "context"],
            "module": "signals_activation"
        }
    })

    # Estimate cost for signal data
    cost_estimate = execute("estimate_cost", {
        "tool": "data_access",
        "parameters": {
            "data_type": "audience_signals",
            "impressions": 1000000,
            "signal_types": ["attention", "context", "viewability"]
        }
    })

    return {
        "providers": signal_providers["results"],
        "intent_id": signal_intent["intent_id"],
        "estimated_cost": cost_estimate,
        "audience_segments": brief["audience"],
        "attention_threshold": brief["kpis"]["min_attention_score"]
    }

signals = activate_signals(campaign_brief)
print(f"Signal providers found: {len(signals['providers'])}")
print(f"Signal intent created: {signals['intent_id']}")
```

### Module 2: Media Buy

The Media Buy module handles inventory selection, bidding, and budget pacing. This is where the agent commits money -- and where escrow becomes critical.

```python
def execute_media_buy(brief: dict, publishers: list, wallet_id: str) -> list:
    """Execute media buys against verified publishers with escrow."""

    active_deals = []

    for pub_data in publishers:
        publisher = pub_data["publisher"]
        publisher_id = publisher["agent_id"]
        spq = pub_data["supply_path_quality"]

        # Allocate budget proportional to supply path quality
        total_spq = sum(p["supply_path_quality"] for p in publishers)
        allocation = (spq / total_spq) * brief["budget"]["total"]
        allocation = round(allocation, 2)

        # Check volume discounts for larger commitments
        discount = execute("get_volume_discount", {
            "agent_id": buyer_agent_id,
            "amount": str(allocation),
            "counterparty_id": publisher_id
        })

        effective_amount = allocation
        if discount.get("discount_rate", 0) > 0:
            effective_amount = allocation * (1 - discount["discount_rate"])
            effective_amount = round(effective_amount, 2)
            print(f"  Volume discount from {publisher['name']}: "
                  f"{discount['discount_rate']:.1%} off "
                  f"(${allocation} -> ${effective_amount})")

        # Create escrow -- budget is locked but not yet released
        escrow = execute("create_escrow", {
            "payer_id": buyer_agent_id,
            "payee_id": publisher_id,
            "amount": str(effective_amount),
            "currency": "USD",
            "wallet_id": wallet_id,
            "conditions": {
                "release_type": "milestone",
                "milestones": [
                    {
                        "name": "delivery_25_percent",
                        "percentage": 25,
                        "criteria": "25% of contracted impressions delivered "
                                    "with viewability >= 90%"
                    },
                    {
                        "name": "delivery_50_percent",
                        "percentage": 25,
                        "criteria": "50% of contracted impressions delivered"
                    },
                    {
                        "name": "delivery_75_percent",
                        "percentage": 25,
                        "criteria": "75% of contracted impressions delivered"
                    },
                    {
                        "name": "delivery_complete",
                        "percentage": 25,
                        "criteria": "100% of contracted impressions delivered, "
                                    "final verification complete"
                    }
                ],
                "expiry": brief["flight"]["end"],
                "cancellation": {
                    "ivt_rate_exceeds": 0.05,
                    "viewability_below": 0.70,
                    "fraud_detected": True
                }
            },
            "metadata": {
                "campaign_id": brief["campaign_id"],
                "publisher_name": publisher["name"],
                "channel": brief["channel"],
                "module": "media_buy"
            }
        })

        active_deals.append({
            "publisher_id": publisher_id,
            "publisher_name": publisher["name"],
            "escrow_id": escrow["escrow_id"],
            "amount": effective_amount,
            "supply_path_quality": spq,
            "status": "active"
        })

        print(f"Escrow created: {escrow['escrow_id']} -> "
              f"{publisher['name']} for ${effective_amount}")

    return active_deals

# Execute buys against top 3 publishers
deals = execute_media_buy(
    campaign_brief,
    scored_publishers[:3],
    wallet_id
)
print(f"\n{len(deals)} media buys executed, "
      f"total locked: ${sum(d['amount'] for d in deals):,.2f}")
```

### Module 3: Creative Management

Creative rotation determines which ad variant shows in each impression. The agent tracks attention scores per creative and shifts delivery toward top performers.

```python
def manage_creative_rotation(brief: dict, deals: list) -> dict:
    """Set up creative rotation and track per-variant performance."""

    creative_state = {
        "variants": {},
        "rotation_strategy": brief["creative"]["rotation_strategy"]
    }

    for asset_id in brief["creative"]["assets"]:
        creative_state["variants"][asset_id] = {
            "impressions": 0,
            "attention_score_sum": 0.0,
            "avg_attention": 0.0,
            "weight": 1.0 / len(brief["creative"]["assets"])
        }

    # Register creative tracking as a service metric
    for deal in deals:
        execute("submit_metrics", {
            "agent_id": buyer_agent_id,
            "metrics": {
                "metric_type": "creative_rotation_initialized",
                "campaign_id": brief["campaign_id"],
                "publisher_id": deal["publisher_id"],
                "variants": list(creative_state["variants"].keys()),
                "strategy": creative_state["rotation_strategy"]
            }
        })

    return creative_state

def update_creative_weights(creative_state: dict) -> dict:
    """Recalculate creative weights based on attention scores.

    Uses Thompson sampling: variants with higher average attention
    scores get proportionally more impressions.
    """
    total_attention = sum(
        v["avg_attention"] for v in creative_state["variants"].values()
    )

    if total_attention == 0:
        return creative_state  # Keep equal weights until data arrives

    for asset_id, variant in creative_state["variants"].items():
        variant["weight"] = variant["avg_attention"] / total_attention

    return creative_state

creative_state = manage_creative_rotation(campaign_brief, deals)
print("Creative rotation initialized:")
for asset_id, variant in creative_state["variants"].items():
    print(f"  {asset_id}: weight={variant['weight']:.2f}")
```

### Module 4: Curation (Supply Path Filtering)

Curation continuously filters the supply path for quality. If a publisher's metrics degrade below thresholds during the flight, the agent should reduce or pause spend.

```python
def curate_supply_path(deals: list, brief: dict) -> list:
    """Evaluate active deals against quality thresholds.

    Returns list of deals with updated status:
    'active', 'warning', or 'paused'.
    """
    curated_deals = []

    for deal in deals:
        # Get latest reputation data
        reputation = execute("get_agent_reputation", {
            "agent_id": deal["publisher_id"]
        })

        # Get latest performance metrics
        metrics = execute("search_agents_by_metrics", {
            "filters": {
                "agent_id": deal["publisher_id"],
                "metric_types": ["viewability_rate", "invalid_traffic_rate",
                                 "fill_rate", "attention_score"]
            }
        })

        # Evaluate against campaign thresholds
        status = "active"
        warnings = []

        for metric in metrics.get("results", []):
            if (metric["metric_type"] == "invalid_traffic_rate"
                    and metric["value"] > brief["kpis"]["max_ivt_rate"]):
                status = "paused"
                warnings.append(
                    f"IVT rate {metric['value']:.1%} exceeds "
                    f"threshold {brief['kpis']['max_ivt_rate']:.1%}"
                )
            elif (metric["metric_type"] == "viewability_rate"
                    and metric["value"] < brief["kpis"]["min_viewability"]):
                if status != "paused":
                    status = "warning"
                warnings.append(
                    f"Viewability {metric['value']:.1%} below "
                    f"threshold {brief['kpis']['min_viewability']:.1%}"
                )

        deal_copy = dict(deal)
        deal_copy["status"] = status
        deal_copy["warnings"] = warnings
        deal_copy["current_reputation"] = reputation.get("score", 0)
        curated_deals.append(deal_copy)

        if warnings:
            print(f"  {deal['publisher_name']}: {status} - {'; '.join(warnings)}")

    return curated_deals

curated = curate_supply_path(deals, campaign_brief)
active_count = sum(1 for d in curated if d["status"] == "active")
print(f"\nCuration complete: {active_count}/{len(curated)} deals active")
```

---

## Chapter 5: Escrow-Based Ad Spend

### Holding Budgets in GreenHelix Until Delivery Confirmed

Escrow is the mechanism that makes autonomous ad buying safe. Without it, you are wiring money to publishers and hoping they deliver. With it, funds are locked in a neutral account and released only when verified conditions are met. This chapter covers the three escrow patterns relevant to media buying: milestone-based release, fraud-triggered cancellation, and partial release on underdelivery.

In traditional programmatic, payment happens after the fact. An advertiser runs a campaign, the publisher delivers impressions, an invoice arrives 30-60 days later, and payment settles 30-60 days after that. Discrepancies between buyer-side and seller-side impression counts are reconciled manually, sometimes taking months. This model does not work for autonomous agents. An agent cannot wait 90 days for reconciliation. It needs real-time budget commitment and release tied to verifiable delivery events.

GreenHelix escrow bridges this gap. When the buyer agent creates an escrow, the budget is immediately deducted from its wallet and held by the gateway. The publisher can see the committed funds, confirming the buyer's ability to pay. As impressions deliver and pass verification checks, the buyer releases milestones, and funds transfer to the publisher in real time. If delivery fails or fraud is detected, unreleased funds return to the buyer. Neither party needs to trust the other. The escrow contract is the trust layer.

The three patterns below cover the full range of outcomes: successful delivery, fraud detection, and partial delivery.

### Pattern 1: Milestone-Based Release

The most common pattern. Budget releases in tranches as the publisher hits delivery milestones.

```python
def release_milestone(escrow_id: str, milestone_name: str,
                      publisher_id: str, verification: dict) -> dict:
    """Release an escrow milestone after verifying delivery."""

    # Verify the milestone criteria before releasing
    assert verification["viewability"] >= 0.90, \
        f"Viewability {verification['viewability']:.1%} below 90% threshold"
    assert verification["ivt_rate"] <= 0.05, \
        f"IVT rate {verification['ivt_rate']:.1%} exceeds 5% threshold"
    assert verification["impressions_delivered"] >= verification["impressions_contracted"], \
        "Impression delivery shortfall"

    # Release the escrow milestone
    release = execute("release_escrow", {
        "escrow_id": escrow_id,
        "milestone": milestone_name,
        "verification": {
            "impressions_delivered": verification["impressions_delivered"],
            "viewability_rate": verification["viewability"],
            "ivt_rate": verification["ivt_rate"],
            "attention_score": verification.get("attention_score", 0),
            "verified_by": buyer_agent_id,
            "verified_at": datetime.utcnow().isoformat()
        }
    })

    # Log the release in the ledger
    ledger_entry = execute("get_ledger_entries", {
        "agent_id": buyer_agent_id,
        "filters": {
            "escrow_id": escrow_id,
            "entry_type": "escrow_release"
        },
        "limit": 1
    })

    print(f"Milestone '{milestone_name}' released for escrow {escrow_id}")
    print(f"  Amount released: ${release.get('amount_released', 'N/A')}")
    print(f"  Remaining: ${release.get('amount_remaining', 'N/A')}")

    return release

# Example: release the first milestone
verification_data = {
    "impressions_delivered": 275000,
    "impressions_contracted": 250000,
    "viewability": 0.93,
    "ivt_rate": 0.012,
    "attention_score": 0.78
}

# release = release_milestone(
#     deals[0]["escrow_id"],
#     "delivery_25_percent",
#     deals[0]["publisher_id"],
#     verification_data
# )
```

### Pattern 2: Fraud-Triggered Cancellation

If invalid traffic exceeds thresholds or fraud is detected, the agent cancels the escrow and recovers unreleased funds.

```python
def cancel_on_fraud(escrow_id: str, deal: dict, evidence: dict) -> dict:
    """Cancel an escrow due to fraud or quality violation."""

    # Notify the publisher via messaging before cancellation
    execute("send_message", {
        "from_agent_id": buyer_agent_id,
        "to_agent_id": deal["publisher_id"],
        "message_type": "escrow_cancellation_notice",
        "content": {
            "escrow_id": escrow_id,
            "reason": evidence["reason"],
            "ivt_rate_observed": evidence.get("ivt_rate", "N/A"),
            "threshold": evidence.get("threshold", "N/A"),
            "evidence_summary": evidence.get("summary", ""),
            "cancellation_effective": datetime.utcnow().isoformat()
        }
    })

    # Cancel the escrow -- unreleased funds return to buyer wallet
    cancellation = execute("release_escrow", {
        "escrow_id": escrow_id,
        "action": "cancel",
        "reason": evidence["reason"],
        "evidence": evidence
    })

    # Submit negative metrics to update publisher reputation
    execute("submit_metrics", {
        "agent_id": buyer_agent_id,
        "metrics": {
            "metric_type": "fraud_incident",
            "publisher_id": deal["publisher_id"],
            "escrow_id": escrow_id,
            "ivt_rate": evidence.get("ivt_rate", 0),
            "fraud_type": evidence.get("fraud_type", "unknown"),
            "amount_recovered": cancellation.get("amount_returned", 0)
        }
    })

    print(f"Escrow {escrow_id} cancelled: {evidence['reason']}")
    print(f"  Funds returned: ${cancellation.get('amount_returned', 'N/A')}")

    return cancellation

# Example: cancel due to high IVT
# cancel_on_fraud(deals[1]["escrow_id"], deals[1], {
#     "reason": "IVT rate exceeded 5% threshold",
#     "ivt_rate": 0.087,
#     "threshold": 0.05,
#     "fraud_type": "sophisticated_invalid_traffic",
#     "summary": "MRC-accredited verification detected 8.7% SIVT "
#                "over 48-hour window, exceeding 5% campaign threshold."
# })
```

### Pattern 3: Partial Release on Underdelivery

When a publisher delivers some but not all contracted impressions, you release a proportional amount and return the rest.

```python
def partial_release(escrow_id: str, deal: dict,
                    delivered_pct: float, verification: dict) -> dict:
    """Release partial escrow proportional to actual delivery."""

    if delivered_pct >= 1.0:
        # Full delivery -- release everything
        return execute("release_escrow", {
            "escrow_id": escrow_id,
            "milestone": "delivery_complete",
            "verification": verification
        })

    # Partial delivery -- release proportional amount, cancel remainder
    partial_amount = round(deal["amount"] * delivered_pct, 2)

    release = execute("release_escrow", {
        "escrow_id": escrow_id,
        "action": "partial_release",
        "amount": str(partial_amount),
        "reason": f"Partial delivery: {delivered_pct:.0%} of contracted impressions",
        "verification": verification
    })

    print(f"Partial release for {deal['publisher_name']}:")
    print(f"  Delivery:  {delivered_pct:.0%}")
    print(f"  Released:  ${partial_amount:,.2f}")
    print(f"  Returned:  ${deal['amount'] - partial_amount:,.2f}")

    return release
```

### Escrow Lifecycle Dashboard

Track all escrows for a campaign in a single view.

```python
def campaign_escrow_dashboard(deals: list) -> dict:
    """Aggregate escrow status across all campaign deals."""

    dashboard = {
        "total_locked": 0,
        "total_released": 0,
        "total_returned": 0,
        "deals": []
    }

    for deal in deals:
        # Get current balance to see escrow state
        balance = execute("get_balance", {
            "agent_id": buyer_agent_id,
            "wallet_id": wallet_id
        })

        # Get ledger entries for this escrow
        entries = execute("get_ledger_entries", {
            "agent_id": buyer_agent_id,
            "filters": {
                "escrow_id": deal["escrow_id"]
            }
        })

        released = sum(
            float(e.get("amount", 0))
            for e in entries.get("entries", [])
            if e.get("entry_type") == "escrow_release"
        )
        returned = sum(
            float(e.get("amount", 0))
            for e in entries.get("entries", [])
            if e.get("entry_type") == "escrow_cancel"
        )

        deal_status = {
            "publisher": deal["publisher_name"],
            "escrow_id": deal["escrow_id"],
            "total_amount": deal["amount"],
            "released": released,
            "returned": returned,
            "remaining": deal["amount"] - released - returned,
            "status": deal.get("status", "active")
        }

        dashboard["deals"].append(deal_status)
        dashboard["total_locked"] += deal_status["remaining"]
        dashboard["total_released"] += released
        dashboard["total_returned"] += returned

    return dashboard

# dashboard = campaign_escrow_dashboard(deals)
# print(f"Campaign Budget Dashboard:")
# print(f"  Locked in escrow: ${dashboard['total_locked']:,.2f}")
# print(f"  Released:         ${dashboard['total_released']:,.2f}")
# print(f"  Returned:         ${dashboard['total_returned']:,.2f}")
```

---

## Chapter 6: Real-Time Campaign Analytics

### Tracking ROAS, Attention Signals, and Supply Path Quality

An autonomous buyer without analytics is a bot burning money. This chapter builds the analytics pipeline: ingesting delivery data, calculating ROAS, tracking attention signals, monitoring supply path quality, and feeding optimization decisions back into the buying loop.

The analytics challenge for autonomous agents is fundamentally different from human analytics. A human buyer reviews a dashboard once or twice a day, spots trends, and makes adjustments. An autonomous agent needs continuous, programmatic access to metrics that feed directly into decision logic. The agent does not "look at" a chart -- it ingests structured data, evaluates it against thresholds, and takes action. This means the analytics pipeline must be machine-readable, real-time, and integrated with the optimization loop.

GreenHelix provides two complementary tools for this. `submit_metrics` pushes performance data into the platform, building both the campaign's analytics record and the agent's (and publisher's) reputation over time. `get_analytics` pulls aggregated data back out for decision-making. Together, they form a feedback loop: impressions deliver, the agent submits metrics, the analytics engine aggregates them, the optimization loop queries the aggregates, and decisions flow back into budget allocation and creative rotation.

### Submit Campaign Metrics

As impressions deliver, the buyer agent submits metrics to GreenHelix for tracking, reputation building, and compliance auditing.

```python
def submit_campaign_metrics(deal: dict, period: dict) -> dict:
    """Submit a period's worth of campaign metrics."""

    metrics_payload = {
        "agent_id": buyer_agent_id,
        "metrics": {
            "metric_type": "campaign_delivery",
            "campaign_id": campaign_brief["campaign_id"],
            "publisher_id": deal["publisher_id"],
            "escrow_id": deal["escrow_id"],
            "period": {
                "start": period["start"],
                "end": period["end"]
            },
            "impressions": period["impressions"],
            "spend": str(period["spend"]),
            "viewability_rate": period["viewability_rate"],
            "ivt_rate": period["ivt_rate"],
            "attention_score": period["attention_score"],
            "completion_rate": period["completion_rate"],
            "cpm": str(round(period["spend"] / period["impressions"] * 1000, 2)),
            "roas": period.get("roas", 0)
        }
    }

    result = execute("submit_metrics", metrics_payload)
    return result

# Example: submit daily metrics for a deal
daily_metrics = {
    "start": "2026-04-15T00:00:00Z",
    "end": "2026-04-15T23:59:59Z",
    "impressions": 35000,
    "spend": 980.00,
    "viewability_rate": 0.94,
    "ivt_rate": 0.008,
    "attention_score": 0.81,
    "completion_rate": 0.87,
    "roas": 4.2
}

# submit_campaign_metrics(deals[0], daily_metrics)
```

### ROAS Tracking Dashboard

```python
def get_campaign_analytics(campaign_id: str) -> dict:
    """Pull aggregate analytics for a campaign."""

    analytics = execute("get_analytics", {
        "agent_id": buyer_agent_id,
        "filters": {
            "campaign_id": campaign_id,
            "metric_types": [
                "campaign_delivery",
                "creative_rotation_initialized"
            ]
        }
    })

    # Aggregate across all publishers
    totals = {
        "total_impressions": 0,
        "total_spend": 0.0,
        "weighted_viewability": 0.0,
        "weighted_attention": 0.0,
        "weighted_ivt": 0.0,
        "avg_roas": 0.0,
        "publisher_breakdown": []
    }

    for entry in analytics.get("results", []):
        metrics = entry.get("metrics", {})
        imps = metrics.get("impressions", 0)
        spend = float(metrics.get("spend", 0))

        totals["total_impressions"] += imps
        totals["total_spend"] += spend
        totals["weighted_viewability"] += (
            metrics.get("viewability_rate", 0) * imps
        )
        totals["weighted_attention"] += (
            metrics.get("attention_score", 0) * imps
        )
        totals["weighted_ivt"] += metrics.get("ivt_rate", 0) * imps

    if totals["total_impressions"] > 0:
        totals["weighted_viewability"] /= totals["total_impressions"]
        totals["weighted_attention"] /= totals["total_impressions"]
        totals["weighted_ivt"] /= totals["total_impressions"]

    if totals["total_spend"] > 0:
        totals["effective_cpm"] = (
            totals["total_spend"] / totals["total_impressions"] * 1000
        )

    return totals

# analytics = get_campaign_analytics(campaign_brief["campaign_id"])
# print(f"Campaign Analytics:")
# print(f"  Impressions: {analytics['total_impressions']:,}")
# print(f"  Spend:       ${analytics['total_spend']:,.2f}")
# print(f"  eCPM:        ${analytics.get('effective_cpm', 0):.2f}")
# print(f"  Viewability: {analytics['weighted_viewability']:.1%}")
# print(f"  Attention:   {analytics['weighted_attention']:.2f}")
# print(f"  IVT Rate:    {analytics['weighted_ivt']:.2%}")
```

### Attention Signal Integration

Attention metrics go beyond viewability. They measure whether a viewer actually engaged with the ad -- dwell time, eye tracking proxies, interaction events, completion rate. The agent uses these to optimize creative rotation and publisher allocation.

```python
def optimize_from_attention(deals: list, creative_state: dict,
                            campaign_id: str) -> dict:
    """Use attention signals to optimize spend allocation and creative mix.

    Returns optimization recommendations.
    """
    recommendations = {
        "publisher_reallocations": [],
        "creative_weight_changes": [],
        "timestamp": datetime.utcnow().isoformat()
    }

    # Get per-publisher attention data
    for deal in deals:
        if deal.get("status") != "active":
            continue

        pub_metrics = execute("search_agents_by_metrics", {
            "filters": {
                "agent_id": deal["publisher_id"],
                "metric_types": ["attention_score"]
            }
        })

        avg_attention = 0.0
        count = 0
        for m in pub_metrics.get("results", []):
            avg_attention += m["value"]
            count += 1
        if count > 0:
            avg_attention /= count

        # If attention is significantly above average, recommend
        # increasing spend allocation
        if avg_attention > 0.8:
            recommendations["publisher_reallocations"].append({
                "publisher_id": deal["publisher_id"],
                "publisher_name": deal["publisher_name"],
                "current_attention": avg_attention,
                "action": "increase_allocation",
                "reason": f"Attention score {avg_attention:.2f} exceeds 0.80 threshold"
            })
        elif avg_attention < 0.5:
            recommendations["publisher_reallocations"].append({
                "publisher_id": deal["publisher_id"],
                "publisher_name": deal["publisher_name"],
                "current_attention": avg_attention,
                "action": "decrease_allocation",
                "reason": f"Attention score {avg_attention:.2f} below 0.50 threshold"
            })

    # Update creative weights based on latest attention data
    creative_state = update_creative_weights(creative_state)
    for asset_id, variant in creative_state["variants"].items():
        recommendations["creative_weight_changes"].append({
            "asset_id": asset_id,
            "new_weight": variant["weight"],
            "avg_attention": variant["avg_attention"]
        })

    return recommendations

# optimizations = optimize_from_attention(
#     curated, creative_state, campaign_brief["campaign_id"]
# )
```

### The Optimization Loop

The full optimization loop runs continuously during the campaign flight, pulling analytics, running curation, adjusting creative weights, and reallocating budget.

```
+------------------------------------------------------------+
|               Continuous Optimization Loop                   |
+------------------------------------------------------------+
|                                                              |
|  [1] Pull Analytics -----> [2] Run Curation                |
|       get_analytics             curate_supply_path           |
|       search_agents_            check thresholds             |
|       by_metrics                flag/pause deals             |
|              |                        |                      |
|              v                        v                      |
|  [3] Optimize Creative -----> [4] Reallocate Budget         |
|       update_creative_              shift spend to           |
|       weights                       high-attention           |
|       submit_metrics                publishers               |
|              |                        |                      |
|              +---------> [5] <--------+                      |
|                     Report & Log                             |
|                     submit_metrics                           |
|                     send_message (to compliance)             |
|                                                              |
|  Loop frequency: every 15 minutes during flight              |
+------------------------------------------------------------+
```

```python
def run_optimization_loop(deals: list, brief: dict,
                          creative_state: dict) -> None:
    """Single iteration of the optimization loop."""

    print(f"[{datetime.utcnow().isoformat()}] Running optimization cycle...")

    # Step 1: Pull latest analytics
    analytics = get_campaign_analytics(brief["campaign_id"])

    # Step 2: Run supply path curation
    curated_deals = curate_supply_path(deals, brief)

    # Step 3 & 4: Optimize from attention signals
    recommendations = optimize_from_attention(
        curated_deals, creative_state, brief["campaign_id"]
    )

    # Step 5: Log the optimization cycle
    execute("submit_metrics", {
        "agent_id": buyer_agent_id,
        "metrics": {
            "metric_type": "optimization_cycle",
            "campaign_id": brief["campaign_id"],
            "timestamp": datetime.utcnow().isoformat(),
            "analytics_snapshot": {
                "impressions": analytics["total_impressions"],
                "spend": analytics["total_spend"],
                "viewability": analytics["weighted_viewability"],
                "attention": analytics["weighted_attention"]
            },
            "active_deals": sum(
                1 for d in curated_deals if d["status"] == "active"
            ),
            "recommendations": len(
                recommendations["publisher_reallocations"]
            )
        }
    })

    # Notify compliance agent of any warnings
    warnings = [d for d in curated_deals if d.get("warnings")]
    if warnings:
        execute("send_message", {
            "from_agent_id": buyer_agent_id,
            "to_agent_id": compliance_id,
            "message_type": "optimization_warnings",
            "content": {
                "campaign_id": brief["campaign_id"],
                "warnings": [
                    {
                        "publisher": d["publisher_name"],
                        "issues": d["warnings"]
                    }
                    for d in warnings
                ]
            }
        })

    print(f"  Active deals: "
          f"{sum(1 for d in curated_deals if d['status'] == 'active')}"
          f"/{len(curated_deals)}")
    print(f"  Recommendations: "
          f"{len(recommendations['publisher_reallocations'])} "
          f"publisher, "
          f"{len(recommendations['creative_weight_changes'])} creative")
```

---

## Chapter 7: Compliance Guardrails

### Spending Caps, Approval Workflows, and Audit Trails for Ad Budgets

Autonomous does not mean uncontrolled. Advertisers, agencies, and regulators require that ad spend operates within defined limits, that anomalies trigger human review, and that every dollar is auditable. This chapter implements three compliance layers: SLA-based spending caps, approval workflows for threshold events, and complete audit trails.

Compliance in autonomous advertising operates on two levels. At the business level, the advertiser sets a budget and expects it to be spent efficiently and within bounds. Overspend by 1% is a rounding error. Overspend by 20% is a career-ending incident for the team that deployed the agent. At the regulatory level, advertising spend in certain categories (pharmaceuticals, financial services, alcohol, political) requires documented approval chains and audit trails that regulators can inspect.

The critical insight is that compliance must be proactive, not reactive. A human buyer who accidentally overspends can stop and explain. An autonomous agent that overspends 50% of a daily budget in 30 minutes (because a publisher suddenly made cheaper inventory available and the optimization loop aggressively allocated) creates a fait accompli. The only defense is a compliance layer that runs ahead of or alongside the buying logic, checking every commitment against pre-defined limits before funds are locked.

GreenHelix SLAs provide this proactive layer. An SLA is not a retroactive report -- it is a programmable contract that monitors metrics in real time and triggers defined actions when conditions are violated. The compliance agent checks SLAs at configurable intervals (typically every 15 minutes) and can pause escrows, alert humans, or halt campaigns before damage compounds.

### Layer 1: SLA-Based Spending Caps

GreenHelix SLAs are programmable contracts that define performance expectations and trigger actions when violated. For ad buying, the SLA defines spending limits.

```python
def create_spending_sla(brief: dict) -> dict:
    """Create an SLA that enforces campaign spending limits."""

    sla = execute("create_sla", {
        "agent_id": buyer_agent_id,
        "name": f"spend-cap-{brief['campaign_id']}",
        "description": f"Spending guardrails for campaign {brief['campaign_id']}",
        "conditions": {
            "daily_spend_cap": {
                "metric": "daily_spend",
                "operator": "lte",
                "value": brief["budget"]["daily_cap"],
                "action_on_violation": "pause_campaign"
            },
            "total_spend_cap": {
                "metric": "total_spend",
                "operator": "lte",
                "value": brief["budget"]["total"],
                "action_on_violation": "halt_all_escrows"
            },
            "ivt_rate_cap": {
                "metric": "ivt_rate",
                "operator": "lte",
                "value": brief["kpis"]["max_ivt_rate"],
                "action_on_violation": "alert_compliance"
            },
            "min_roas": {
                "metric": "roas",
                "operator": "gte",
                "value": brief["kpis"]["target_roas"] * 0.5,
                "action_on_violation": "alert_and_reduce_spend"
            }
        },
        "monitoring_interval": "15m",
        "metadata": {
            "campaign_id": brief["campaign_id"],
            "created_by": buyer_agent_id,
            "compliance_agent": compliance_id
        }
    })

    print(f"Spending SLA created: {sla['sla_id']}")
    return sla

spending_sla = create_spending_sla(campaign_brief)
```

### Layer 2: Compliance Checking

The compliance agent periodically checks SLA adherence and takes action on violations.

```python
def check_campaign_compliance(sla_id: str, brief: dict) -> dict:
    """Check campaign compliance against SLA conditions."""

    compliance = execute("check_sla_compliance", {
        "sla_id": sla_id,
        "agent_id": buyer_agent_id
    })

    violations = compliance.get("violations", [])
    status = "compliant" if not violations else "violation_detected"

    report = {
        "sla_id": sla_id,
        "campaign_id": brief["campaign_id"],
        "status": status,
        "checked_at": datetime.utcnow().isoformat(),
        "violations": violations,
        "actions_taken": []
    }

    for violation in violations:
        condition = violation.get("condition", "")
        severity = violation.get("severity", "warning")

        if severity == "critical":
            # Critical: pause all active escrows
            report["actions_taken"].append({
                "action": "pause_all_escrows",
                "reason": f"Critical SLA violation: {condition}",
                "timestamp": datetime.utcnow().isoformat()
            })

            # Alert compliance agent
            execute("send_message", {
                "from_agent_id": buyer_agent_id,
                "to_agent_id": compliance_id,
                "message_type": "critical_sla_violation",
                "content": {
                    "campaign_id": brief["campaign_id"],
                    "sla_id": sla_id,
                    "violation": violation,
                    "action": "escrows_paused",
                    "requires_human_review": True
                }
            })

        elif severity == "warning":
            report["actions_taken"].append({
                "action": "alert_sent",
                "reason": f"SLA warning: {condition}",
                "timestamp": datetime.utcnow().isoformat()
            })

            execute("send_message", {
                "from_agent_id": buyer_agent_id,
                "to_agent_id": compliance_id,
                "message_type": "sla_warning",
                "content": {
                    "campaign_id": brief["campaign_id"],
                    "sla_id": sla_id,
                    "violation": violation
                }
            })

    # Log compliance check as a metric
    execute("submit_metrics", {
        "agent_id": compliance_id,
        "metrics": {
            "metric_type": "compliance_check",
            "campaign_id": brief["campaign_id"],
            "sla_id": sla_id,
            "status": status,
            "violations_count": len(violations),
            "actions_count": len(report["actions_taken"])
        }
    })

    return report

# compliance_report = check_campaign_compliance(
#     spending_sla["sla_id"], campaign_brief
# )
```

### Layer 3: Audit Trail

Every action the agent takes -- escrow creation, milestone release, cancellation, compliance check, optimization decision -- must be auditable. GreenHelix's ledger provides the immutable record.

```python
def generate_audit_trail(campaign_id: str, agent_id: str) -> dict:
    """Generate a complete audit trail for a campaign.

    Pulls all ledger entries, metrics submissions, and messages
    related to the campaign.
    """

    # Get all ledger entries for the buyer agent
    ledger = execute("get_ledger_entries", {
        "agent_id": agent_id,
        "filters": {
            "metadata.campaign_id": campaign_id
        },
        "limit": 1000
    })

    # Get all analytics for the campaign
    analytics = execute("get_analytics", {
        "agent_id": agent_id,
        "filters": {
            "campaign_id": campaign_id
        }
    })

    # Categorize entries
    trail = {
        "campaign_id": campaign_id,
        "generated_at": datetime.utcnow().isoformat(),
        "escrow_events": [],
        "payment_events": [],
        "compliance_events": [],
        "optimization_events": [],
        "total_spend": 0.0,
        "total_recovered": 0.0
    }

    for entry in ledger.get("entries", []):
        entry_type = entry.get("entry_type", "")
        amount = float(entry.get("amount", 0))

        if "escrow" in entry_type:
            trail["escrow_events"].append(entry)
            if entry_type == "escrow_release":
                trail["total_spend"] += amount
            elif entry_type == "escrow_cancel":
                trail["total_recovered"] += amount

        elif "payment" in entry_type:
            trail["payment_events"].append(entry)

    for record in analytics.get("results", []):
        metric_type = record.get("metrics", {}).get("metric_type", "")
        if "compliance" in metric_type:
            trail["compliance_events"].append(record)
        elif "optimization" in metric_type:
            trail["optimization_events"].append(record)

    trail["summary"] = {
        "total_escrow_events": len(trail["escrow_events"]),
        "total_payment_events": len(trail["payment_events"]),
        "total_compliance_checks": len(trail["compliance_events"]),
        "total_optimization_cycles": len(trail["optimization_events"]),
        "net_spend": trail["total_spend"],
        "recovered_from_cancellations": trail["total_recovered"]
    }

    return trail

# audit = generate_audit_trail(campaign_brief["campaign_id"], buyer_agent_id)
# print(f"Audit Trail for {audit['campaign_id']}:")
# print(f"  Escrow events:        {audit['summary']['total_escrow_events']}")
# print(f"  Compliance checks:    {audit['summary']['total_compliance_checks']}")
# print(f"  Optimization cycles:  {audit['summary']['total_optimization_cycles']}")
# print(f"  Net spend:            ${audit['summary']['net_spend']:,.2f}")
# print(f"  Recovered:            ${audit['summary']['recovered_from_cancellations']:,.2f}")
```

### Billing Integration for Cost Tracking

Track the cost of using GreenHelix tools themselves, separate from ad spend.

```python
def track_platform_costs(campaign_id: str) -> dict:
    """Track GreenHelix platform costs for the campaign."""

    # Estimate per-tool costs
    tools_used = [
        "search_services", "best_match", "create_escrow",
        "release_escrow", "get_analytics", "submit_metrics",
        "check_sla_compliance", "send_message", "get_balance",
        "get_ledger_entries", "get_agent_reputation",
        "build_claim_chain", "search_agents_by_metrics"
    ]

    total_platform_cost = 0.0
    cost_breakdown = []

    for tool in tools_used:
        estimate = execute("estimate_cost", {
            "tool": tool,
            "parameters": {
                "campaign_id": campaign_id,
                "estimated_calls": 100  # per day
            }
        })

        daily_cost = float(estimate.get("estimated_cost", 0))
        cost_breakdown.append({
            "tool": tool,
            "daily_cost": daily_cost,
            "monthly_cost": daily_cost * 30
        })
        total_platform_cost += daily_cost

    return {
        "daily_platform_cost": total_platform_cost,
        "monthly_platform_cost": total_platform_cost * 30,
        "breakdown": cost_breakdown,
        "as_percentage_of_spend": (
            total_platform_cost / campaign_brief["budget"]["daily_cap"]
        ) * 100
    }

# costs = track_platform_costs(campaign_brief["campaign_id"])
# print(f"Platform costs: ${costs['daily_platform_cost']:.2f}/day "
#       f"({costs['as_percentage_of_spend']:.2f}% of daily spend)")
```

---

## Next Steps

For deployment patterns, monitoring, and production hardening, see the
[Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening).

---

## What You Get

This guide walked through building autonomous media-buying agents on the GreenHelix A2A Commerce Gateway, from a single campaign to a production fleet. Here is what you now have:

**Agent Identity and Wallets (Chapter 2).** Buyer, analyst, and compliance agents registered with cryptographic identities. Per-campaign wallets that isolate budgets. Delegation architecture that prevents over-commitment.

**Publisher Discovery and Trust (Chapter 3).** Programmatic publisher search via `search_services` and `best_match`. Deep verification using reputation scores, claim chains, and performance metrics. Supply path quality scoring that quantifies directness, IVT rates, viewability, and dispute history.

**AdCP-Aligned Campaign Execution (Chapter 4).** Four-module pipeline mapping AdCP's Signals Activation, Media Buy, Creative, and Curation to GreenHelix tools. Campaign brief structure that encodes everything an agent needs to execute autonomously. Milestone-based escrow for each publisher deal.

**Escrow-Based Budget Management (Chapter 5).** Three escrow patterns: milestone release for on-track delivery, fraud-triggered cancellation with evidence and messaging, and partial release for underdelivery. Campaign-level escrow dashboard aggregating all deal states.

**Real-Time Analytics (Chapter 6).** Metric submission pipeline for impressions, spend, viewability, IVT, and attention scores. ROAS tracking dashboard. Attention-driven optimization that shifts spend toward high-engagement publishers and top-performing creative variants. Continuous optimization loop running every 15 minutes.

**Compliance Guardrails (Chapter 7).** SLA-based spending caps with automatic enforcement. Multi-tier compliance checking with escalation. Complete audit trails pulling from the ledger and analytics. Platform cost tracking to monitor GreenHelix tool usage separately from ad spend.

**Production Fleet Operations (Chapter 8).** Fleet registration pattern for scaling across channels. Health monitoring across all agents. Fleet-level SLAs for operational metrics. Three-tier alerting via messaging. Auto-scaling based on utilization thresholds. Production readiness checklist covering identity, wallets, publishers, escrow, compliance, analytics, fleet, and testing.

The PubMatic/Butler/Till campaign proved that autonomous media buying works. AdCP and the IAB roadmap are standardizing the interfaces. GreenHelix provides the commerce layer that makes it safe: verified identities, escrowed budgets, auditable transactions, and programmable compliance. The 31% ROAS improvement is the starting point, not the ceiling.

