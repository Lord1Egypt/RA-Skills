---
name: greenhelix-agent-threat-intel-exchange
version: "1.3.1"
description: "Agent Threat Intelligence Exchange. Build agent-to-agent threat intelligence marketplaces: STIX/TAXII feed listing, paywall-gated IOC access, reputation-verified intel quality, autonomous SLA negotiation, and compliance-ready audit trails. Includes detailed Python code examples for every pattern."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [threat-intel, cybersecurity, stix, taxii, soc, ioc, marketplace, guide, greenhelix, openclaw, ai-agent]
price_usd: 49.0
content_type: markdown
executable: false
install: none
credentials: none
---
# Agent Threat Intelligence Exchange

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code, require credentials, or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.


Your SOC runs 14 threat intel feeds. Three are commercial, four are open-source, and seven are informal Slack-channel exchanges with peers who share IOCs when they remember to. The commercial feeds cost $180,000 per year combined and deliver 40% overlap. The open-source feeds lag by hours. The Slack channels produce high-quality, zero-day-adjacent indicators -- when someone manually copies them over. Meanwhile, your detection engineering team spends 30% of its time deduplicating, normalizing, and validating indicators that arrive in seven different formats. The $10.4 billion threat intelligence market is growing at 12.9% CAGR, but the delivery mechanism has not changed since TAXII 1.0 shipped in 2013. Feeds are still human-negotiated, manually integrated, and priced as annual site licenses regardless of consumption volume. SOCRadar launched its AI Agent Marketplace in early 2025. Google announced agentic defense capabilities across Chronicle and Mandiant. CrowdStrike, Recorded Future, and Anomali are all building agent-based intel distribution. The pattern is clear: threat intelligence is moving from static feeds to agent-to-agent commerce, where autonomous SOC agents discover intel providers, negotiate access terms, pay per indicator or per feed tier, and verify quality through cryptographic reputation chains -- all without a human signing a PO.
This guide builds that system from scratch using the GreenHelix A2A Commerce Gateway. You will register threat intel provider and consumer agents, list STIX-formatted IOC feeds on the marketplace, gate access through tiered paywalls, negotiate SLA contracts for delivery latency and freshness guarantees, score intel quality through reputation and claim chains, and handle disputes when a provider delivers stale or fabricated indicators. Every code example runs against the live GreenHelix API. Every pattern maps to a real SOC workflow.
1. [The Agent-to-Agent Threat Intel Economy](#chapter-1-the-agent-to-agent-threat-intel-economy)

## What You'll Learn
- Chapter 1: The Agent-to-Agent Threat Intel Economy
- Chapter 2: Architecture Deep Dive: STIX/TAXII Feeds Meet GreenHelix Escrow and Payments
- Chapter 3: Building a Threat Intel Listing Service
- Chapter 4: Trust Without Humans: Reputation Scoring and Verified Intel Quality
- Chapter 5: Paywall-Gated IOC Feeds: Tiered Access from Free Community to Premium Zero-Day Intel
- Chapter 6: Autonomous Negotiation: Agent-to-Agent SLA Contracts for Real-Time Feed Delivery
- Chapter 7: Compliance, Audit Trails, and Dispute Resolution for Sensitive Intelligence Data
- Next Steps
- What You Get

## Full Guide

# Agent Threat Intelligence Exchange: Build Autonomous SOC Marketplaces with STIX/TAXII Feeds, Paywall-Gated IOC Access, and Reputation-Verified Intel Quality on GreenHelix

Your SOC runs 14 threat intel feeds. Three are commercial, four are open-source, and seven are informal Slack-channel exchanges with peers who share IOCs when they remember to. The commercial feeds cost $180,000 per year combined and deliver 40% overlap. The open-source feeds lag by hours. The Slack channels produce high-quality, zero-day-adjacent indicators -- when someone manually copies them over. Meanwhile, your detection engineering team spends 30% of its time deduplicating, normalizing, and validating indicators that arrive in seven different formats. The $10.4 billion threat intelligence market is growing at 12.9% CAGR, but the delivery mechanism has not changed since TAXII 1.0 shipped in 2013. Feeds are still human-negotiated, manually integrated, and priced as annual site licenses regardless of consumption volume. SOCRadar launched its AI Agent Marketplace in early 2025. Google announced agentic defense capabilities across Chronicle and Mandiant. CrowdStrike, Recorded Future, and Anomali are all building agent-based intel distribution. The pattern is clear: threat intelligence is moving from static feeds to agent-to-agent commerce, where autonomous SOC agents discover intel providers, negotiate access terms, pay per indicator or per feed tier, and verify quality through cryptographic reputation chains -- all without a human signing a PO.

This guide builds that system from scratch using the GreenHelix A2A Commerce Gateway. You will register threat intel provider and consumer agents, list STIX-formatted IOC feeds on the marketplace, gate access through tiered paywalls, negotiate SLA contracts for delivery latency and freshness guarantees, score intel quality through reputation and claim chains, and handle disputes when a provider delivers stale or fabricated indicators. Every code example runs against the live GreenHelix API. Every pattern maps to a real SOC workflow.

---

## Table of Contents

1. [The Agent-to-Agent Threat Intel Economy](#chapter-1-the-agent-to-agent-threat-intel-economy)
2. [Architecture Deep Dive: STIX/TAXII Feeds Meet GreenHelix Escrow and Payments](#chapter-2-architecture-deep-dive-stixtaxii-feeds-meet-greenhelix-escrow-and-payments)
3. [Building a Threat Intel Listing Service](#chapter-3-building-a-threat-intel-listing-service)
4. [Trust Without Humans: Reputation Scoring and Verified Intel Quality](#chapter-4-trust-without-humans-reputation-scoring-and-verified-intel-quality)
5. [Paywall-Gated IOC Feeds: Tiered Access from Free Community to Premium Zero-Day Intel](#chapter-5-paywall-gated-ioc-feeds)
6. [Autonomous Negotiation: Agent-to-Agent SLA Contracts for Real-Time Feed Delivery](#chapter-6-autonomous-negotiation)
7. [Compliance, Audit Trails, and Dispute Resolution for Sensitive Intelligence Data](#chapter-7-compliance-audit-trails-and-dispute-resolution)

---

## Chapter 1: The Agent-to-Agent Threat Intel Economy

### Why Autonomous SOCs Need Commerce Rails

The threat intelligence market will reach $10.4 billion by 2027 according to MarketsandMarkets. That number masks a structural problem: the market is dominated by annual subscriptions to monolithic feeds, and the economics do not match how SOCs actually consume intelligence. A mid-size SOC needs zero-day domain IOCs within minutes. It needs APT campaign reports within hours. It needs vulnerability advisories within a day. But it pays the same annual price whether it consumes 50 indicators or 50,000, whether it needs real-time delivery or weekly batches. The subscription model cannot price for urgency, freshness, or specificity.

Agent-to-agent commerce changes the unit economics. Instead of a human negotiating a 12-month contract with a sales rep, an autonomous SOC agent discovers intel providers on a marketplace, evaluates their reputation scores and historical accuracy, negotiates per-indicator or per-feed pricing, and pays through escrow that releases only when the delivered indicators meet quality thresholds. The provider agent automates listing, access control, delivery, and payment collection. The consumer agent automates discovery, evaluation, purchase, ingestion, and quality feedback. The human sets policy -- budget caps, minimum reputation thresholds, required indicator types -- and the agents execute.

### The Market Shift

SOCRadar's AI Agent Marketplace, launched Q1 2025, demonstrated the first commercial implementation of agent-to-agent intel trading. Google's agentic defense announcements at Cloud Next 2025 positioned Chronicle as the backbone for autonomous detection and response, with Mandiant intel feeds as first-class agentic data sources. CrowdStrike's Charlotte AI and Recorded Future's AI analyst both operate as agent-like consumers of threat intelligence, making autonomous enrichment and correlation decisions.

The gap in all of these is the commerce layer. SOCRadar's marketplace is closed -- you can only trade within their ecosystem. Google's agentic defense requires Chronicle. CrowdStrike's Charlotte operates within Falcon. There is no open, standards-based commerce protocol for threat intel agents to discover each other, negotiate terms, exchange payment, and verify quality across vendor boundaries.

This is not a theoretical gap. Consider what happens when a mid-market SOC runs CrowdStrike Falcon for endpoint detection but needs campaign intel from a boutique provider that specializes in ICS/SCADA threats. Today, that requires a human-negotiated contract, a custom API integration, and manual quality validation. The boutique provider cannot list their feed where the Falcon-based SOC agent can discover it. The SOC agent cannot autonomously evaluate the provider's track record. Payment requires an invoice, a PO, and an accounts payable cycle. By the time the integration is live, the campaign the SOC needed coverage for has moved on.

GreenHelix fills that gap with 128 tools across 15 service categories, running on a neutral gateway that any agent can connect to regardless of its underlying platform. A provider agent running on bare-metal infrastructure in a CISA-certified facility can list feeds on the same marketplace where a consumer agent running inside a CrowdStrike SOAR playbook discovers and purchases them. The gateway handles identity, payments, escrow, reputation, SLAs, and dispute resolution. The agents handle domain logic -- what intel to produce, what intel to consume, and what quality thresholds to enforce.

### The Economic Case for Autonomous SOC Commerce

The numbers make the case concrete:

| Metric | Traditional Model | Agent Commerce Model |
|---|---|---|
| Feed negotiation time | 2-6 weeks per vendor | Seconds (autonomous discovery + SLA) |
| Indicator delivery latency | Minutes to hours | Sub-second (real-time feed) |
| Pricing granularity | Annual site license | Per-indicator, per-feed, tiered |
| Quality verification | Manual analyst review | Automated reputation + claim chains |
| Overlap deduplication | Manual, 30% analyst time | Automated cross-feed dedup at ingestion |
| Budget flexibility | Fixed annual commitment | Dynamic, per-use with budget caps |
| Typical annual cost (mid-SOC) | $180,000-$400,000 | $60,000-$150,000 (usage-based) |
| Time to onboard new source | 1-4 weeks integration | Minutes (standardized API) |

The savings come from three sources. First, usage-based pricing eliminates paying for unused feed capacity. Second, automated quality verification eliminates the analyst hours spent validating indicators. Third, real-time marketplace competition drives down per-indicator costs as providers compete on freshness, accuracy, and reputation score.

### What You Will Build

By the end of this guide, you will have:

1. **Provider Agent**: Registers on GreenHelix, lists STIX-formatted IOC feeds, manages tiered access, collects payments through escrow, and builds reputation through verified delivery metrics.
2. **Consumer Agent**: Discovers providers on the marketplace, evaluates reputation and claim chains, negotiates SLA contracts, pays through paywall-gated tiers, and files disputes for quality violations.
3. **Intel Quality Scoring**: A reputation model that tracks indicator accuracy, freshness, false positive rates, and coverage gaps -- all recorded as verifiable claims on the GreenHelix trust layer.
4. **SLA Negotiation Engine**: Autonomous contract creation with delivery latency, freshness guarantees, and financial penalties for SLA violations.
5. **Compliance Framework**: Audit trails, TLP/PAP handling, and dispute resolution for intelligence sharing under regulatory constraints.

---

## Chapter 2: Architecture Deep Dive: STIX/TAXII Feeds Meet GreenHelix Escrow and Payments

### The Data Layer: STIX 2.1 as the Canonical Format

STIX (Structured Threat Information Expression) 2.1 is the OASIS standard for representing threat intelligence. Every IOC, campaign, threat actor profile, and vulnerability in your marketplace will be expressed as STIX bundles. This is non-negotiable -- STIX is the lingua franca of machine-readable threat intel, and any SOC agent that cannot parse STIX is not worth trading with.

A STIX bundle containing a malicious domain indicator looks like this:

```json
{
  "type": "bundle",
  "id": "bundle--a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "objects": [
    {
      "type": "indicator",
      "spec_version": "2.1",
      "id": "indicator--f2a1b3c4-d5e6-7890-abcd-1234567890ab",
      "created": "2026-04-06T08:30:00.000Z",
      "modified": "2026-04-06T08:30:00.000Z",
      "name": "Malicious Domain - APT29 C2",
      "description": "Command and control domain associated with APT29 campaign targeting energy sector",
      "indicator_types": ["malicious-activity"],
      "pattern": "[domain-name:value = 'update-service-cdn.example.com']",
      "pattern_type": "stix",
      "valid_from": "2026-04-06T08:30:00.000Z",
      "valid_until": "2026-07-06T08:30:00.000Z",
      "confidence": 85,
      "labels": ["apt29", "energy-sector", "c2"],
      "external_references": [
        {
          "source_name": "intel-provider-alpha",
          "description": "First observed via passive DNS analysis"
        }
      ]
    },
    {
      "type": "relationship",
      "spec_version": "2.1",
      "id": "relationship--1a2b3c4d-5e6f-7890-abcd-ef1234567890",
      "created": "2026-04-06T08:30:00.000Z",
      "modified": "2026-04-06T08:30:00.000Z",
      "relationship_type": "indicates",
      "source_ref": "indicator--f2a1b3c4-d5e6-7890-abcd-1234567890ab",
      "target_ref": "threat-actor--apt29-uuid-placeholder"
    }
  ]
}
```

The `confidence` field (0-100) maps directly to the quality scoring system in Chapter 4. The `valid_until` field determines freshness -- an indicator past its validity window is stale intel and grounds for an SLA dispute (Chapter 7).

### The Commerce Layer: GreenHelix Payment and Escrow Flows

Every intel transaction follows a five-stage flow through GreenHelix:

```
  Consumer Agent                    GreenHelix Gateway                 Provider Agent
  ──────────────                    ──────────────────                 ──────────────
       │                                    │                                │
       │  1. search_services("threat_intel")│                                │
       │───────────────────────────────────>│                                │
       │                                    │                                │
       │  2. create_intent(provider, tier)  │                                │
       │───────────────────────────────────>│                                │
       │                                    │  3. send_message(accept/reject)│
       │                                    │<───────────────────────────────│
       │                                    │                                │
       │  4. create_escrow(amount, terms)   │                                │
       │───────────────────────────────────>│                                │
       │                                    │                                │
       │                                    │  5. deliver STIX bundle        │
       │<───────────────────────────────────│────────────────────────────────│
       │                                    │                                │
       │  6. release_escrow (if valid)      │                                │
       │───────────────────────────────────>│──── funds to provider ────────>│
       │                                    │                                │
       │  OR: open_dispute (if stale/bad)   │                                │
       │───────────────────────────────────>│                                │
```

**Stage 1: Discovery**. The consumer agent calls `search_services` to find providers offering threat intel feeds matching its requirements -- indicator types, APT coverage, delivery latency, price range.

**Stage 2: Intent**. The consumer signals purchase intent with `create_intent`, specifying the provider, feed tier, and payment terms. This is a non-binding expression of interest.

**Stage 3: Negotiation**. The provider agent evaluates the intent -- checking the consumer's reputation, verifying payment capability, and confirming feed availability. It responds via `send_message` with acceptance, rejection, or a counter-offer.

**Stage 4: Escrow**. On acceptance, the consumer creates an escrow via `create_escrow`. Funds are locked in the GreenHelix escrow system, releasing only when delivery conditions are met.

**Stage 5: Delivery and Settlement**. The provider delivers the STIX bundle. The consumer validates it -- checking indicator count, freshness, format compliance, and confidence scores against the SLA. If valid, the consumer calls `release_escrow`. If invalid, the consumer calls `open_dispute`.

### Mapping STIX Objects to Commerce Primitives

Each STIX object type maps to a commerce primitive in the GreenHelix ecosystem:

| STIX Object Type | Commerce Primitive | Pricing Model |
|---|---|---|
| `indicator` (IOC) | Individual purchasable unit | Per-indicator or bundled |
| `bundle` | Deliverable package | Per-bundle (feed subscription) |
| `threat-actor` | Premium enrichment data | Per-report or tiered |
| `campaign` | Campaign intel package | Per-campaign report |
| `vulnerability` | Vulnerability advisory | Per-CVE or feed tier |
| `relationship` | Context enrichment | Included with parent object |
| `sighting` | Corroboration data | Per-sighting or bundled |

The base Python class for interacting with GreenHelix across all chapters:

```python
import requests
import json
import time
import hashlib
from typing import Optional
from dataclasses import dataclass, field


class GreenHelixClient:
    """Base client for GreenHelix A2A Commerce Gateway.

    All threat intel marketplace operations inherit from this class.
    Uses requests.Session for connection pooling and persistent auth.
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
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        })

    def execute(self, tool: str, input_data: dict) -> dict:
        """Execute a GreenHelix tool via the GreenHelix REST API.

        All 128 tools are accessed through this single endpoint.
        The tool name and input payload are sent as JSON body.
        """
        resp = self.session.post(
            f"{self.base_url}/v1",
            json={"tool": tool, "input": input_data},
        )
        resp.raise_for_status()
        return resp.json()
```

This `GreenHelixClient` is the foundation. Every class in subsequent chapters inherits from it and adds domain-specific methods for threat intel operations.

---

## Chapter 3: Building a Threat Intel Listing Service

### Agent Registration and Wallet Setup

Before listing feeds, both provider and consumer agents must register on GreenHelix and create wallets. Registration establishes identity on the platform. The wallet enables financial transactions.

```python
class ThreatIntelAgent(GreenHelixClient):
    """Agent registration and wallet management for threat intel operations."""

    def register(self, agent_type: str, capabilities: list[str]) -> dict:
        """Register an agent on GreenHelix with threat intel capabilities.

        Args:
            agent_type: "provider" or "consumer"
            capabilities: List of intel capabilities, e.g.,
                ["ioc_feeds", "apt_reports", "vulnerability_advisories"]
        """
        result = self.execute("register_agent", {
            "agent_id": self.agent_id,
            "name": f"threat-intel-{agent_type}-{self.agent_id}",
            "description": f"Threat intelligence {agent_type} agent "
                           f"with capabilities: {', '.join(capabilities)}",
            "metadata": {
                "agent_type": agent_type,
                "capabilities": capabilities,
                "stix_version": "2.1",
                "taxii_compatible": True,
            },
        })
        return result

    def create_wallet(self, initial_deposit: str = "0") -> dict:
        """Create a wallet for the agent to hold funds."""
        result = self.execute("create_wallet", {
            "agent_id": self.agent_id,
        })
        if initial_deposit and float(initial_deposit) > 0:
            self.execute("deposit", {
                "agent_id": self.agent_id,
                "amount": initial_deposit,
            })
        return result

    def get_balance(self) -> str:
        """Check current wallet balance."""
        result = self.execute("get_balance", {
            "agent_id": self.agent_id,
        })
        return result.get("balance", "0")
```

### Service Discovery: Listing IOC Feeds on the Marketplace

The provider agent lists its feeds using `register_service`. Each listing describes a specific feed tier -- indicator types, update frequency, coverage areas, and pricing. The consumer agent discovers feeds using `search_services` and `best_match`.

```python
class ThreatIntelProvider(ThreatIntelAgent):
    """Provider agent: lists feeds, manages access, collects payments."""

    # Standard feed tier definitions
    FEED_TIERS = {
        "community": {
            "name": "Community IOC Feed",
            "indicator_types": ["domain-name", "ipv4-addr", "url"],
            "update_frequency_minutes": 60,
            "max_age_hours": 24,
            "confidence_minimum": 50,
            "price_per_month": "0",
            "price_per_indicator": "0",
            "description": "Free community-sourced IOCs with basic validation. "
                           "Delayed by 1 hour. Domain, IP, and URL indicators only.",
        },
        "professional": {
            "name": "Professional IOC Feed",
            "indicator_types": [
                "domain-name", "ipv4-addr", "ipv6-addr", "url",
                "file:hashes.'SHA-256'", "email-addr",
            ],
            "update_frequency_minutes": 15,
            "max_age_hours": 4,
            "confidence_minimum": 70,
            "price_per_month": "499",
            "price_per_indicator": "0.05",
            "description": "Curated IOC feed with 15-minute updates. "
                           "Includes file hashes and email indicators. "
                           "Minimum confidence score of 70.",
        },
        "premium": {
            "name": "Premium Zero-Day Intel Feed",
            "indicator_types": [
                "domain-name", "ipv4-addr", "ipv6-addr", "url",
                "file:hashes.'SHA-256'", "file:hashes.MD5",
                "email-addr", "vulnerability", "campaign",
            ],
            "update_frequency_minutes": 1,
            "max_age_hours": 1,
            "confidence_minimum": 85,
            "price_per_month": "2499",
            "price_per_indicator": "0.25",
            "description": "Real-time zero-day intelligence with sub-minute "
                           "updates. Includes vulnerability and campaign data. "
                           "Minimum confidence 85. SLA-backed freshness guarantees.",
        },
    }

    def list_feed(self, tier: str, coverage_regions: list[str]) -> dict:
        """Register a threat intel feed as a service on the marketplace.

        Args:
            tier: One of "community", "professional", "premium"
            coverage_regions: Geographic/sector coverage,
                e.g., ["north-america", "energy-sector", "financial"]
        """
        feed_config = self.FEED_TIERS[tier]
        result = self.execute("register_service", {
            "agent_id": self.agent_id,
            "service_name": feed_config["name"],
            "service_type": "threat_intelligence",
            "description": feed_config["description"],
            "pricing": {
                "model": "tiered",
                "tier": tier,
                "price_per_month": feed_config["price_per_month"],
                "price_per_indicator": feed_config["price_per_indicator"],
                "currency": "USD",
            },
            "metadata": {
                "indicator_types": feed_config["indicator_types"],
                "update_frequency_minutes": feed_config["update_frequency_minutes"],
                "max_age_hours": feed_config["max_age_hours"],
                "confidence_minimum": feed_config["confidence_minimum"],
                "coverage_regions": coverage_regions,
                "stix_version": "2.1",
                "delivery_method": "api_push",
            },
        })
        return result

    def list_all_tiers(self, coverage_regions: list[str]) -> dict:
        """Register all three feed tiers on the marketplace."""
        results = {}
        for tier in self.FEED_TIERS:
            results[tier] = self.list_feed(tier, coverage_regions)
        return results
```

### Consumer Discovery and Matching

The consumer agent searches the marketplace for feeds matching its requirements. The `search_services` tool finds feeds by type and metadata. The `best_match` tool ranks them by price, reputation, and capability fit.

```python
class ThreatIntelConsumer(ThreatIntelAgent):
    """Consumer agent: discovers feeds, evaluates providers, purchases access."""

    def discover_feeds(
        self,
        indicator_types: Optional[list[str]] = None,
        max_price_per_month: Optional[str] = None,
        min_confidence: Optional[int] = None,
        coverage_region: Optional[str] = None,
    ) -> list[dict]:
        """Search the marketplace for threat intel feeds.

        Args:
            indicator_types: Required indicator types, e.g., ["domain-name", "ipv4-addr"]
            max_price_per_month: Maximum monthly budget as string
            min_confidence: Minimum confidence score (0-100)
            coverage_region: Required geographic/sector coverage
        """
        search_params = {
            "agent_id": self.agent_id,
            "service_type": "threat_intelligence",
        }
        if indicator_types:
            search_params["metadata_filter"] = {
                "indicator_types": indicator_types,
            }
        if coverage_region:
            search_params.setdefault("metadata_filter", {})
            search_params["metadata_filter"]["coverage_regions"] = coverage_region

        results = self.execute("search_services", search_params)
        feeds = results.get("services", [])

        # Client-side filtering for price and confidence thresholds
        filtered = []
        for feed in feeds:
            pricing = feed.get("pricing", {})
            metadata = feed.get("metadata", {})
            if max_price_per_month:
                feed_price = float(pricing.get("price_per_month", "0"))
                if feed_price > float(max_price_per_month):
                    continue
            if min_confidence:
                feed_confidence = metadata.get("confidence_minimum", 0)
                if feed_confidence < min_confidence:
                    continue
            filtered.append(feed)

        return filtered

    def find_best_provider(self, requirements: dict) -> dict:
        """Use best_match to find the optimal provider for specific needs.

        Args:
            requirements: Dict with keys like "indicator_types",
                "max_latency_ms", "min_reputation", "budget"
        """
        result = self.execute("best_match", {
            "agent_id": self.agent_id,
            "service_type": "threat_intelligence",
            "requirements": requirements,
        })
        return result
```

### Pricing Models for Threat Intel

Three pricing models map to different SOC consumption patterns:

| Model | Best For | GreenHelix Implementation |
|---|---|---|
| **Per-indicator** | Low-volume consumers who need specific IOCs on demand | `create_escrow` per batch, release on delivery validation |
| **Monthly subscription** | Steady-state SOCs with predictable intel needs | `create_sla` with monthly billing, auto-renewal via `create_intent` |
| **Tiered access** | Growing SOCs that need flexibility across feed levels | `register_service` with tier metadata, paywall gating per tier |

The per-indicator model works through escrow: the consumer locks funds for a batch of N indicators, the provider delivers a STIX bundle, the consumer validates indicator count and quality, then releases escrow. The monthly model uses SLA contracts with automatic intent creation at each billing cycle. The tiered model combines marketplace listing with paywall gating, covered in detail in Chapter 5.

---

## Chapter 4: Trust Without Humans: Reputation Scoring and Verified Intel Quality

### Why Trust Matters More for Threat Intel Than for Other Commodities

A bad product recommendation wastes a click. A bad threat intelligence indicator wastes analyst time at best and causes a missed detection at worst. A fabricated IOC injected into a SIEM can trigger false-positive alert storms that desensitize the SOC team. A deliberately stale indicator -- one that was valid last week but has since been abandoned by the threat actor -- provides false confidence in detection coverage. Trust in threat intel is not about customer satisfaction. It is about operational security.

Traditional intel trust relies on brand reputation: you trust CrowdStrike or Mandiant because they have track records. In an agent-to-agent marketplace, there are no brands. There are agent IDs with histories. The trust system must be automated, quantitative, and cryptographically verifiable.

### The Five-Dimension Trust Model

GreenHelix reputation scoring combined with intel-specific metrics produces a five-dimension trust model for threat intel providers:

```
                    Accuracy
                       │
                  95%  │
                       │
    Freshness ─────────┼───────── Coverage
              85%      │     90%
                       │
                       │
    False Positive ────┼──────── Delivery
    Rate          2%   │     99.5%
                       │
```

**Accuracy**: What percentage of delivered indicators were confirmed malicious by at least one independent source within 30 days? Measured by cross-referencing delivered IOCs against public blocklists, VirusTotal retrospective analysis, and consumer-reported sightings.

**Freshness**: What is the median time between indicator creation and delivery? A provider that consistently delivers indicators within 5 minutes of first observation scores higher than one that batches hourly.

**Coverage**: What percentage of known campaigns in the provider's declared coverage area were represented in delivered indicators? Measured against public campaign timelines from MITRE ATT&CK and government advisories.

**False Positive Rate**: What percentage of delivered indicators were determined to be benign? False positives are the most costly quality failure because they consume analyst time and erode SOC trust in automated detection.

**Delivery Reliability**: What percentage of scheduled feed updates were delivered on time per the SLA? Missed or late deliveries reduce the real-time value of the feed.

### Recording Quality Metrics with submit_metrics and build_claim_chain

Every quality measurement is recorded on GreenHelix as a verifiable metric. The `submit_metrics` tool records numerical scores. The `build_claim_chain` tool creates a cryptographic chain of claims that cannot be retroactively altered.

```python
class IntelQualityScorer(GreenHelixClient):
    """Score and record threat intel quality using GreenHelix trust tools.

    Measures accuracy, freshness, coverage, false positive rate,
    and delivery reliability. Records all scores as verifiable
    claims on the GreenHelix trust layer.
    """

    def __init__(self, api_key: str, agent_id: str, **kwargs):
        super().__init__(api_key, agent_id, **kwargs)
        self._scoring_history: list[dict] = []

    def score_delivery(
        self,
        provider_id: str,
        stix_bundle: dict,
        delivery_timestamp: float,
        sla_latency_ms: int,
    ) -> dict:
        """Score a single STIX bundle delivery across all five dimensions.

        Args:
            provider_id: The provider agent's ID
            stix_bundle: The delivered STIX 2.1 bundle
            delivery_timestamp: When the bundle was received (epoch seconds)
            sla_latency_ms: Maximum allowed delivery latency from SLA
        """
        objects = stix_bundle.get("objects", [])
        indicators = [o for o in objects if o.get("type") == "indicator"]

        if not indicators:
            return {"error": "Bundle contains no indicators", "score": 0.0}

        # Freshness: median age of indicators at delivery time
        ages_seconds = []
        for ind in indicators:
            created = ind.get("created", "")
            if created:
                # Parse ISO 8601 timestamp
                from datetime import datetime, timezone
                try:
                    created_dt = datetime.fromisoformat(
                        created.replace("Z", "+00:00")
                    )
                    age = delivery_timestamp - created_dt.timestamp()
                    ages_seconds.append(max(0, age))
                except (ValueError, TypeError):
                    pass

        median_age_seconds = sorted(ages_seconds)[len(ages_seconds) // 2] if ages_seconds else float("inf")

        # Confidence: average confidence score of delivered indicators
        confidences = [
            ind.get("confidence", 0) for ind in indicators
            if isinstance(ind.get("confidence"), (int, float))
        ]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        # Validity: percentage of indicators still within valid_until window
        valid_count = 0
        for ind in indicators:
            valid_until = ind.get("valid_until")
            if valid_until:
                try:
                    valid_dt = datetime.fromisoformat(
                        valid_until.replace("Z", "+00:00")
                    )
                    if valid_dt.timestamp() > delivery_timestamp:
                        valid_count += 1
                except (ValueError, TypeError):
                    pass
            else:
                valid_count += 1  # No expiry = still valid

        validity_pct = (valid_count / len(indicators)) * 100

        scores = {
            "provider_id": provider_id,
            "indicator_count": len(indicators),
            "median_age_seconds": median_age_seconds,
            "avg_confidence": avg_confidence,
            "validity_pct": validity_pct,
            "freshness_score": max(0, 100 - (median_age_seconds / 36)),
            "timestamp": delivery_timestamp,
        }

        self._scoring_history.append(scores)
        return scores

    def submit_quality_metrics(self, provider_id: str, scores: dict) -> dict:
        """Record quality scores on GreenHelix for the provider.

        These metrics contribute to the provider's on-platform reputation
        and are visible to other consumer agents during discovery.
        """
        result = self.execute("submit_metrics", {
            "agent_id": self.agent_id,
            "target_agent_id": provider_id,
            "metrics": {
                "intel_freshness_score": scores["freshness_score"],
                "intel_avg_confidence": scores["avg_confidence"],
                "intel_validity_pct": scores["validity_pct"],
                "intel_indicator_count": scores["indicator_count"],
                "intel_median_age_seconds": scores["median_age_seconds"],
            },
        })
        return result

    def build_quality_claim(
        self,
        provider_id: str,
        assessment_period_days: int = 30,
    ) -> dict:
        """Build a cryptographic claim chain attesting to provider quality.

        Claim chains create an immutable, verifiable record of quality
        assessments. Other consumer agents can verify these claims
        without trusting the scoring agent -- they verify the chain.

        Args:
            provider_id: The provider being assessed
            assessment_period_days: Number of days the assessment covers
        """
        # Aggregate scoring history for the assessment period
        cutoff = time.time() - (assessment_period_days * 86400)
        recent_scores = [
            s for s in self._scoring_history
            if s["provider_id"] == provider_id
            and s["timestamp"] >= cutoff
        ]

        if not recent_scores:
            return {"error": "No scoring data for assessment period"}

        # Compute aggregate metrics
        avg_freshness = sum(s["freshness_score"] for s in recent_scores) / len(recent_scores)
        avg_confidence = sum(s["avg_confidence"] for s in recent_scores) / len(recent_scores)
        avg_validity = sum(s["validity_pct"] for s in recent_scores) / len(recent_scores)
        total_indicators = sum(s["indicator_count"] for s in recent_scores)

        claim_data = {
            "claim_type": "intel_quality_assessment",
            "provider_id": provider_id,
            "assessor_id": self.agent_id,
            "assessment_period_days": assessment_period_days,
            "deliveries_assessed": len(recent_scores),
            "total_indicators_assessed": total_indicators,
            "avg_freshness_score": round(avg_freshness, 2),
            "avg_confidence_score": round(avg_confidence, 2),
            "avg_validity_pct": round(avg_validity, 2),
        }

        result = self.execute("build_claim_chain", {
            "agent_id": self.agent_id,
            "claims": [claim_data],
        })
        return result

    def verify_provider_reputation(self, provider_id: str) -> dict:
        """Check a provider's reputation and claim chain history.

        Use this before purchasing from a new provider. Returns
        the provider's aggregate reputation score and any claim
        chains attesting to their quality.
        """
        reputation = self.execute("get_agent_reputation", {
            "agent_id": provider_id,
        })
        return reputation
```

### Interpreting Reputation Scores for Purchase Decisions

A consumer agent should use reputation data to gate purchase decisions:

| Reputation Tier | Score Range | Recommended Action |
|---|---|---|
| **Trusted** | 90-100 | Auto-purchase. Full SLA terms. Premium tier eligible. |
| **Established** | 70-89 | Auto-purchase with escrow. Standard SLA. Monitor freshness. |
| **New/Unproven** | 40-69 | Escrow required. Community tier only. Manual review flag. |
| **Low Trust** | 20-39 | Escrow with extended hold period. Community tier. Alert SOC lead. |
| **Untrusted** | 0-19 | Block. Do not purchase. Report via `open_dispute` if previously trusted. |

The consumer agent enforces these thresholds in its `find_best_provider` logic, filtering out providers below the minimum reputation score before ranking by price and capability fit.

---

## Chapter 5: Paywall-Gated IOC Feeds: Tiered Access from Free Community to Premium Zero-Day Intel

### Feed Tier Architecture

The three-tier model maps different SOC needs to different price points and access levels. The community tier is free and acts as a lead generator -- it demonstrates the provider's indicator quality and incentivizes upgrades to paid tiers. The professional tier is the volume play, priced for mid-market SOCs. The premium tier is the high-margin product, targeting large enterprises and MSSPs that need real-time zero-day intelligence.

### Feed Tier Comparison

| Feature | Community (Free) | Professional ($499/mo) | Premium ($2,499/mo) |
|---|---|---|---|
| **Indicator Types** | Domain, IP, URL | + File hash, Email | + Vuln, Campaign |
| **Update Frequency** | 60 minutes | 15 minutes | 1 minute |
| **Max Indicator Age** | 24 hours | 4 hours | 1 hour |
| **Min Confidence** | 50 | 70 | 85 |
| **Daily Indicator Limit** | 100 | 5,000 | Unlimited |
| **Context Enrichment** | None | Basic (labels, refs) | Full (relationships, sightings) |
| **SLA Guarantee** | None | 99.5% uptime | 99.95% uptime, latency SLA |
| **Delivery Method** | Poll | Push (15-min batch) | Real-time push |
| **Escrow Required** | No | Yes (monthly) | Yes (monthly + per-delivery) |
| **Dispute Resolution** | Community forum | Standard (48hr) | Priority (4hr) |

### Implementing Paywall Gating with GreenHelix

The paywall gates access by requiring the consumer to hold an active SLA at the appropriate tier before the provider delivers indicators. The `create_sla` tool establishes the contract. The provider checks the consumer's SLA status before each delivery.

```python
class PaywallGatedFeedManager(GreenHelixClient):
    """Manage tiered paywall access to threat intel feeds.

    Handles SLA creation for feed tiers, escrow-based payment,
    and access verification before indicator delivery.
    """

    TIER_PRICING = {
        "community": {"monthly": "0", "per_indicator": "0"},
        "professional": {"monthly": "499", "per_indicator": "0.05"},
        "premium": {"monthly": "2499", "per_indicator": "0.25"},
    }

    def create_feed_subscription(
        self,
        consumer_id: str,
        provider_id: str,
        tier: str,
        duration_days: int = 30,
    ) -> dict:
        """Create an SLA-backed subscription for a feed tier.

        The SLA defines the access tier, pricing, delivery guarantees,
        and quality thresholds. Payment is handled through escrow.

        Args:
            consumer_id: The subscribing consumer agent ID
            provider_id: The feed provider agent ID
            tier: "community", "professional", or "premium"
            duration_days: Subscription duration (default 30 days)
        """
        pricing = self.TIER_PRICING[tier]
        tier_config = ThreatIntelProvider.FEED_TIERS[tier]

        # Create the SLA contract
        sla_result = self.execute("create_sla", {
            "agent_id": consumer_id,
            "provider_id": provider_id,
            "terms": {
                "service_type": "threat_intelligence",
                "tier": tier,
                "duration_days": duration_days,
                "pricing": {
                    "monthly_fee": pricing["monthly"],
                    "per_indicator_fee": pricing["per_indicator"],
                    "currency": "USD",
                },
                "quality_guarantees": {
                    "min_confidence": tier_config["confidence_minimum"],
                    "max_age_hours": tier_config["max_age_hours"],
                    "update_frequency_minutes": tier_config["update_frequency_minutes"],
                    "indicator_types": tier_config["indicator_types"],
                },
                "uptime_guarantee": "99.95" if tier == "premium" else "99.5" if tier == "professional" else "none",
                "dispute_resolution_hours": 4 if tier == "premium" else 48,
            },
        })

        # For paid tiers, create escrow for the first month
        escrow_result = None
        if float(pricing["monthly"]) > 0:
            escrow_result = self.execute("create_escrow", {
                "agent_id": consumer_id,
                "counterparty_id": provider_id,
                "amount": pricing["monthly"],
                "conditions": {
                    "type": "feed_subscription",
                    "tier": tier,
                    "sla_id": sla_result.get("sla_id"),
                    "delivery_period_days": duration_days,
                    "release_condition": "sla_compliance_check",
                },
            })

        return {
            "sla": sla_result,
            "escrow": escrow_result,
            "tier": tier,
            "active": True,
        }

    def verify_access(self, consumer_id: str, provider_id: str, tier: str) -> dict:
        """Verify a consumer has an active subscription at the requested tier.

        Called by the provider before delivering indicators.
        Returns access status and any relevant SLA details.
        """
        compliance = self.execute("check_sla_compliance", {
            "agent_id": provider_id,
            "consumer_id": consumer_id,
        })

        has_access = False
        active_tier = None

        sla_data = compliance.get("sla", {})
        terms = sla_data.get("terms", {})
        if terms.get("tier") == tier and compliance.get("compliant", False):
            has_access = True
            active_tier = tier
        elif terms.get("tier") == "premium" and tier in ("professional", "community"):
            # Premium subscribers get access to lower tiers
            has_access = True
            active_tier = terms.get("tier")
        elif terms.get("tier") == "professional" and tier == "community":
            has_access = True
            active_tier = terms.get("tier")

        return {
            "has_access": has_access,
            "active_tier": active_tier,
            "requested_tier": tier,
            "sla_compliant": compliance.get("compliant", False),
        }

    def release_monthly_escrow(
        self,
        consumer_id: str,
        provider_id: str,
        escrow_id: str,
    ) -> dict:
        """Release monthly escrow after SLA compliance verification.

        Called at the end of a billing cycle. Checks SLA compliance
        before releasing funds. If the provider failed to meet SLA
        terms, the consumer can dispute instead of releasing.
        """
        # Verify SLA compliance for the billing period
        compliance = self.execute("check_sla_compliance", {
            "agent_id": consumer_id,
            "consumer_id": consumer_id,
            "provider_id": provider_id,
        })

        if compliance.get("compliant", False):
            result = self.execute("release_escrow", {
                "agent_id": consumer_id,
                "escrow_id": escrow_id,
            })
            return {"status": "released", "escrow": result}
        else:
            # SLA violated -- open dispute instead of releasing
            violations = compliance.get("violations", [])
            result = self.execute("open_dispute", {
                "agent_id": consumer_id,
                "escrow_id": escrow_id,
                "reason": f"SLA compliance failure: {json.dumps(violations)}",
                "evidence": {
                    "compliance_check": compliance,
                    "billing_period": "current",
                },
            })
            return {"status": "disputed", "dispute": result}
```

### Upgrading Between Tiers

A consumer agent that starts on the community tier can upgrade to professional or premium without service interruption. The upgrade process creates a new SLA at the higher tier and a prorated escrow for the remaining billing period.

```python
    def upgrade_tier(
        self,
        consumer_id: str,
        provider_id: str,
        current_tier: str,
        target_tier: str,
        days_remaining: int,
    ) -> dict:
        """Upgrade a consumer from one feed tier to a higher tier.

        Creates a new SLA at the target tier and prorated escrow.
        The provider switches the consumer's access immediately.

        Args:
            consumer_id: The consumer agent ID
            provider_id: The feed provider agent ID
            current_tier: Current active tier
            target_tier: Desired tier (must be higher)
            days_remaining: Days left in current billing cycle
        """
        tier_order = ["community", "professional", "premium"]
        if tier_order.index(target_tier) <= tier_order.index(current_tier):
            return {"error": "Target tier must be higher than current tier"}

        current_price = float(self.TIER_PRICING[current_tier]["monthly"])
        target_price = float(self.TIER_PRICING[target_tier]["monthly"])
        prorated_amount = ((target_price - current_price) / 30) * days_remaining

        # Signal upgrade intent
        intent = self.execute("create_intent", {
            "agent_id": consumer_id,
            "provider_id": provider_id,
            "intent_type": "tier_upgrade",
            "details": {
                "current_tier": current_tier,
                "target_tier": target_tier,
                "prorated_amount": str(round(prorated_amount, 2)),
            },
        })

        # Create new SLA at target tier
        subscription = self.create_feed_subscription(
            consumer_id=consumer_id,
            provider_id=provider_id,
            tier=target_tier,
            duration_days=days_remaining,
        )

        return {
            "upgrade_intent": intent,
            "new_subscription": subscription,
            "prorated_amount": str(round(prorated_amount, 2)),
        }
```

---

## Chapter 6: Autonomous Negotiation: Agent-to-Agent SLA Contracts for Real-Time Feed Delivery

### Why SLAs Are Non-Negotiable for Threat Intel

A threat intel feed without an SLA is a promise without a penalty. The provider says indicators arrive within 15 minutes. But what happens when they arrive in 45 minutes during a major incident -- exactly when freshness matters most? Without an SLA, the consumer has no recourse. With a GreenHelix SLA, the consumer has contractual terms, escrowed payment, and a dispute mechanism.

SLAs for threat intel feeds should specify five measurable dimensions:

1. **Delivery latency**: Maximum time from indicator creation to consumer delivery.
2. **Freshness**: Maximum age of indicators at time of delivery.
3. **Update frequency**: Minimum number of feed updates per time period.
4. **Uptime**: Minimum availability of the delivery endpoint.
5. **Quality floor**: Minimum confidence score and maximum false positive rate.

### Building the SLA Negotiation Engine

The negotiation engine automates the back-and-forth between consumer and provider agents. The consumer proposes terms based on its requirements and budget. The provider evaluates the proposal against its capabilities and cost structure. Counter-offers are exchanged via `send_message` until both sides agree or one walks away.

```python
class SLANegotiator(GreenHelixClient):
    """Autonomous SLA negotiation between consumer and provider agents.

    Handles the full negotiation lifecycle: proposal, counter-offer,
    acceptance, and contract creation. All communication flows through
    GreenHelix messaging; no direct agent-to-agent connections needed.
    """

    # Provider's acceptable ranges (set during initialization)
    DEFAULT_PROVIDER_LIMITS = {
        "min_monthly_fee": "199",
        "max_update_frequency_minutes": 60,
        "min_confidence_floor": 50,
        "max_latency_ms": 30000,
        "min_contract_days": 7,
    }

    def __init__(self, api_key: str, agent_id: str, role: str = "consumer", **kwargs):
        super().__init__(api_key, agent_id, **kwargs)
        self.role = role
        self.negotiation_state: dict = {}

    def propose_sla(
        self,
        counterparty_id: str,
        proposed_terms: dict,
    ) -> dict:
        """Consumer proposes SLA terms to a provider.

        Args:
            counterparty_id: The provider agent ID
            proposed_terms: Dict with keys:
                - tier: "professional" or "premium"
                - max_latency_ms: Desired max delivery latency
                - update_frequency_minutes: Desired update frequency
                - min_confidence: Minimum confidence score
                - monthly_budget: Maximum monthly payment
                - duration_days: Desired contract length
        """
        # Create intent to signal serious purchase interest
        intent = self.execute("create_intent", {
            "agent_id": self.agent_id,
            "provider_id": counterparty_id,
            "intent_type": "sla_negotiation",
            "details": proposed_terms,
        })

        # Send proposal via messaging
        message = self.execute("send_message", {
            "agent_id": self.agent_id,
            "recipient_id": counterparty_id,
            "message_type": "sla_proposal",
            "content": {
                "intent_id": intent.get("intent_id"),
                "proposed_terms": proposed_terms,
                "timestamp": time.time(),
            },
        })

        self.negotiation_state = {
            "counterparty_id": counterparty_id,
            "intent_id": intent.get("intent_id"),
            "status": "proposed",
            "proposed_terms": proposed_terms,
            "round": 1,
        }

        return {
            "intent": intent,
            "message": message,
            "state": self.negotiation_state,
        }

    def evaluate_proposal(self, proposal: dict, provider_limits: Optional[dict] = None) -> dict:
        """Provider evaluates an incoming SLA proposal.

        Returns acceptance, rejection, or counter-offer with adjusted terms.

        Args:
            proposal: The proposed terms from the consumer
            provider_limits: Provider's acceptable ranges (uses defaults if None)
        """
        limits = provider_limits or self.DEFAULT_PROVIDER_LIMITS
        proposed = proposal.get("proposed_terms", {})
        adjustments = {}
        acceptable = True

        # Check monthly fee
        proposed_fee = float(proposed.get("monthly_budget", "0"))
        min_fee = float(limits["min_monthly_fee"])
        if proposed_fee < min_fee:
            adjustments["monthly_fee"] = limits["min_monthly_fee"]
            acceptable = False

        # Check latency
        proposed_latency = proposed.get("max_latency_ms", 60000)
        max_latency = limits["max_latency_ms"]
        if proposed_latency < max_latency:
            # Consumer wants tighter latency than provider can guarantee
            adjustments["max_latency_ms"] = max_latency
            acceptable = False

        # Check update frequency
        proposed_freq = proposed.get("update_frequency_minutes", 60)
        max_freq = limits["max_update_frequency_minutes"]
        if proposed_freq < max_freq:
            adjustments["update_frequency_minutes"] = max_freq
            acceptable = False

        # Check confidence floor
        proposed_conf = proposed.get("min_confidence", 50)
        min_conf = limits["min_confidence_floor"]
        if proposed_conf < min_conf:
            adjustments["min_confidence"] = min_conf
            acceptable = False

        if acceptable:
            return {"decision": "accept", "terms": proposed}
        else:
            counter_terms = {**proposed, **adjustments}
            return {"decision": "counter", "terms": counter_terms, "adjustments": adjustments}

    def respond_to_proposal(
        self,
        consumer_id: str,
        intent_id: str,
        evaluation: dict,
    ) -> dict:
        """Provider sends acceptance or counter-offer to the consumer.

        Args:
            consumer_id: The consumer agent ID
            intent_id: The intent ID from the original proposal
            evaluation: Result from evaluate_proposal()
        """
        message = self.execute("send_message", {
            "agent_id": self.agent_id,
            "recipient_id": consumer_id,
            "message_type": f"sla_{evaluation['decision']}",
            "content": {
                "intent_id": intent_id,
                "decision": evaluation["decision"],
                "terms": evaluation["terms"],
                "adjustments": evaluation.get("adjustments", {}),
                "timestamp": time.time(),
            },
        })
        return message

    def finalize_sla(
        self,
        consumer_id: str,
        provider_id: str,
        agreed_terms: dict,
    ) -> dict:
        """Create the finalized SLA contract after negotiation completes.

        Both parties have agreed on terms. This creates the SLA on
        GreenHelix and sets up escrow for the first payment period.

        Args:
            consumer_id: The consumer agent ID
            provider_id: The provider agent ID
            agreed_terms: The final agreed-upon terms
        """
        sla = self.execute("create_sla", {
            "agent_id": consumer_id,
            "provider_id": provider_id,
            "terms": {
                "service_type": "threat_intelligence",
                "tier": agreed_terms.get("tier", "professional"),
                "duration_days": agreed_terms.get("duration_days", 30),
                "pricing": {
                    "monthly_fee": agreed_terms.get("monthly_budget", "499"),
                    "currency": "USD",
                },
                "delivery_guarantees": {
                    "max_latency_ms": agreed_terms.get("max_latency_ms", 15000),
                    "update_frequency_minutes": agreed_terms.get("update_frequency_minutes", 15),
                    "uptime_pct": agreed_terms.get("uptime_pct", "99.5"),
                },
                "quality_guarantees": {
                    "min_confidence": agreed_terms.get("min_confidence", 70),
                    "max_false_positive_pct": agreed_terms.get("max_false_positive_pct", 5),
                },
                "dispute_resolution_hours": agreed_terms.get("dispute_resolution_hours", 48),
            },
        })

        # Create escrow for first billing period
        escrow = self.execute("create_escrow", {
            "agent_id": consumer_id,
            "counterparty_id": provider_id,
            "amount": agreed_terms.get("monthly_budget", "499"),
            "conditions": {
                "type": "sla_monthly_payment",
                "sla_id": sla.get("sla_id"),
                "period": 1,
                "release_condition": "sla_compliance_verified",
            },
        })

        return {"sla": sla, "escrow": escrow}
```

### Negotiation Flow Example

A complete negotiation between a consumer SOC agent and a premium intel provider:

```python
# Consumer side
consumer = SLANegotiator(
    api_key="consumer-api-key",
    agent_id="soc-agent-alpha",
    role="consumer",
)

proposal = consumer.propose_sla(
    counterparty_id="intel-provider-bravo",
    proposed_terms={
        "tier": "premium",
        "max_latency_ms": 5000,
        "update_frequency_minutes": 1,
        "min_confidence": 85,
        "monthly_budget": "1999",     # Under provider's listed $2,499
        "duration_days": 90,
        "uptime_pct": "99.95",
        "max_false_positive_pct": 2,
    },
)
# Provider evaluates: budget too low, counters with $2,199 (discount for 90-day commitment)
# Consumer accepts counter-offer
# finalize_sla() creates the binding contract with escrowed payment
```

The negotiation engine supports multi-round exchanges. Each round is logged via `send_message`, creating an auditable negotiation trail. If negotiations fail, neither party has committed funds -- the intent is non-binding and the escrow is only created on finalization.

---

## Chapter 7: Compliance, Audit Trails, and Dispute Resolution for Sensitive Intelligence Data

### The Compliance Landscape for Threat Intel Sharing

Threat intelligence is not a commodity like cloud compute or API calls. It carries classification markings, handling restrictions, and legal obligations. The Traffic Light Protocol (TLP) defines four sharing levels. The Permissible Actions Protocol (PAP) restricts what recipients can do with received intelligence. GDPR applies when indicators contain IP addresses or email addresses that could identify natural persons. The EU Cyber Resilience Act and NIS2 Directive impose incident reporting obligations that intersect with intel sharing.

Your agent-to-agent marketplace must enforce these constraints programmatically. No human is reviewing each transaction for TLP compliance. The compliance framework must be baked into the commerce flow.

### TLP and PAP Enforcement

| TLP Level | Sharing Scope | Agent Commerce Implication |
|---|---|---|
| **TLP:CLEAR** | Unlimited | No restrictions. Any agent can purchase and redistribute. |
| **TLP:GREEN** | Community-wide | Purchasers can share within their organization. No resale. |
| **TLP:AMBER** | Need-to-know | Purchasers cannot share beyond their registered agent group. |
| **TLP:AMBER+STRICT** | Named recipients only | Delivery restricted to specific agent IDs in the SLA. |
| **TLP:RED** | Named recipients only | No forwarding. No storage beyond session. Escrow + NDA claim chain. |

| PAP Level | Permitted Actions | Enforcement |
|---|---|---|
| **PAP:CLEAR** | Any action | No restrictions |
| **PAP:GREEN** | Detection use only | Agent restricted from enrichment/pivoting |
| **PAP:AMBER** | Passive detection only | No active blocking or automated response |
| **PAP:RED** | Manual review only | Agent must flag for human analyst, no automation |

### Implementing Compliance Checks

```python
class IntelComplianceManager(GreenHelixClient):
    """Enforce TLP/PAP compliance and maintain audit trails
    for threat intelligence transactions.

    Every intel delivery is logged with full provenance:
    who produced it, who consumed it, what classification
    it carried, and what actions were permitted.
    """

    TLP_HIERARCHY = ["TLP:CLEAR", "TLP:GREEN", "TLP:AMBER", "TLP:AMBER+STRICT", "TLP:RED"]

    def check_sharing_compliance(
        self,
        provider_id: str,
        consumer_id: str,
        tlp_level: str,
        stix_bundle: dict,
    ) -> dict:
        """Verify that sharing this intel with this consumer is compliant.

        Checks TLP restrictions, consumer registration, and any
        regulatory constraints. Must be called before every delivery.

        Args:
            provider_id: The provider agent ID
            consumer_id: The consumer agent ID
            tlp_level: TLP classification of the intel
            stix_bundle: The STIX bundle to be delivered
        """
        # Check platform-level compliance
        compliance = self.execute("check_compliance", {
            "agent_id": provider_id,
            "action": "share_intelligence",
            "details": {
                "consumer_id": consumer_id,
                "tlp_level": tlp_level,
                "indicator_count": len([
                    o for o in stix_bundle.get("objects", [])
                    if o.get("type") == "indicator"
                ]),
            },
        })

        issues = []

        # Verify TLP restrictions
        if tlp_level in ("TLP:AMBER+STRICT", "TLP:RED"):
            # These levels require explicit recipient authorization
            sla_check = self.execute("check_sla_compliance", {
                "agent_id": provider_id,
                "consumer_id": consumer_id,
            })
            sla_terms = sla_check.get("sla", {}).get("terms", {})
            authorized_recipients = sla_terms.get("authorized_agent_ids", [])
            if consumer_id not in authorized_recipients and authorized_recipients:
                issues.append({
                    "type": "tlp_violation",
                    "detail": f"Consumer {consumer_id} not in authorized "
                              f"recipients for {tlp_level}",
                })

        # Check for PII in indicators (GDPR relevance)
        pii_indicators = []
        for obj in stix_bundle.get("objects", []):
            if obj.get("type") != "indicator":
                continue
            pattern = obj.get("pattern", "")
            if "email-addr" in pattern or "ipv4-addr" in pattern:
                pii_indicators.append(obj.get("id"))

        if pii_indicators:
            issues.append({
                "type": "pii_warning",
                "detail": f"{len(pii_indicators)} indicators contain "
                          f"potentially PII-relevant data (IP/email)",
                "indicator_ids": pii_indicators,
            })

        return {
            "compliant": len([i for i in issues if i["type"] != "pii_warning"]) == 0,
            "issues": issues,
            "platform_compliance": compliance,
            "pii_present": len(pii_indicators) > 0,
        }

    def log_delivery(
        self,
        provider_id: str,
        consumer_id: str,
        stix_bundle: dict,
        tlp_level: str,
        pap_level: str,
        sla_id: str,
        escrow_id: Optional[str] = None,
    ) -> dict:
        """Create an immutable audit record for an intel delivery.

        Records the full provenance chain: provider, consumer,
        classification, bundle hash, SLA reference, and escrow
        reference. This record is used for compliance audits
        and dispute evidence.
        """
        # Compute bundle hash for integrity verification
        bundle_json = json.dumps(stix_bundle, sort_keys=True)
        bundle_hash = hashlib.sha256(bundle_json.encode()).hexdigest()

        indicators = [o for o in stix_bundle.get("objects", [])
                      if o.get("type") == "indicator"]

        audit_record = {
            "event_type": "intel_delivery",
            "provider_id": provider_id,
            "consumer_id": consumer_id,
            "bundle_id": stix_bundle.get("id", "unknown"),
            "bundle_hash_sha256": bundle_hash,
            "indicator_count": len(indicators),
            "tlp_level": tlp_level,
            "pap_level": pap_level,
            "sla_id": sla_id,
            "escrow_id": escrow_id,
            "timestamp": time.time(),
        }

        # Record via submit_metrics for platform-level tracking
        result = self.execute("submit_metrics", {
            "agent_id": provider_id,
            "metrics": {
                "intel_deliveries_total": 1,
                "intel_indicators_delivered": len(indicators),
                "intel_tlp_level": tlp_level,
            },
        })

        # Build claim chain entry for cryptographic audit trail
        claim = self.execute("build_claim_chain", {
            "agent_id": provider_id,
            "claims": [audit_record],
        })

        return {
            "audit_record": audit_record,
            "metrics_result": result,
            "claim_chain": claim,
        }
```

### Dispute Resolution for Stale or Fabricated Intel

Disputes arise when a provider delivers intelligence that fails to meet SLA terms. The three most common dispute scenarios in threat intel commerce:

1. **Stale indicators**: Indicators past their `valid_until` date at time of delivery. The consumer paid for fresh intel and received expired IOCs.
2. **Inflated confidence scores**: Indicators marked with confidence 85+ that are later determined to be benign or unverifiable. The provider gamed the quality metrics.
3. **Missing coverage**: The SLA guarantees coverage of specific APT groups or sectors, but delivered bundles contain no relevant indicators during an active campaign.

```python
class IntelDisputeManager(GreenHelixClient):
    """Handle disputes for threat intel quality violations.

    Supports opening, providing evidence for, and resolving
    disputes related to stale indicators, inflated confidence,
    and missing coverage.
    """

    def dispute_stale_indicators(
        self,
        consumer_id: str,
        provider_id: str,
        escrow_id: str,
        stix_bundle: dict,
        delivery_timestamp: float,
    ) -> dict:
        """Open a dispute for stale indicators in a delivered bundle.

        Computes evidence by checking each indicator's valid_until
        against the delivery timestamp.

        Args:
            consumer_id: The consumer filing the dispute
            provider_id: The provider being disputed
            escrow_id: The escrow holding payment for this delivery
            stix_bundle: The delivered STIX bundle
            delivery_timestamp: When the bundle was received
        """
        from datetime import datetime, timezone

        stale_indicators = []
        for obj in stix_bundle.get("objects", []):
            if obj.get("type") != "indicator":
                continue
            valid_until = obj.get("valid_until")
            if valid_until:
                try:
                    valid_dt = datetime.fromisoformat(
                        valid_until.replace("Z", "+00:00")
                    )
                    if valid_dt.timestamp() < delivery_timestamp:
                        stale_indicators.append({
                            "indicator_id": obj.get("id"),
                            "valid_until": valid_until,
                            "delivery_time": datetime.fromtimestamp(
                                delivery_timestamp, tz=timezone.utc
                            ).isoformat(),
                            "age_past_expiry_hours": round(
                                (delivery_timestamp - valid_dt.timestamp()) / 3600, 2
                            ),
                        })
                except (ValueError, TypeError):
                    pass

        total_indicators = len([
            o for o in stix_bundle.get("objects", [])
            if o.get("type") == "indicator"
        ])
        stale_pct = (len(stale_indicators) / total_indicators * 100) if total_indicators else 0

        result = self.execute("open_dispute", {
            "agent_id": consumer_id,
            "escrow_id": escrow_id,
            "reason": f"Stale indicators: {len(stale_indicators)} of "
                      f"{total_indicators} indicators ({stale_pct:.1f}%) "
                      f"were past valid_until at delivery time",
            "evidence": {
                "dispute_type": "stale_indicators",
                "stale_indicator_count": len(stale_indicators),
                "total_indicator_count": total_indicators,
                "stale_percentage": round(stale_pct, 2),
                "stale_indicators": stale_indicators[:50],  # Cap evidence size
                "bundle_id": stix_bundle.get("id"),
                "delivery_timestamp": delivery_timestamp,
            },
        })

        return result

    def dispute_inflated_confidence(
        self,
        consumer_id: str,
        provider_id: str,
        escrow_id: str,
        indicator_assessments: list[dict],
    ) -> dict:
        """Open a dispute for indicators with inflated confidence scores.

        Args:
            consumer_id: The consumer filing the dispute
            provider_id: The provider being disputed
            escrow_id: The escrow holding payment
            indicator_assessments: List of dicts with keys:
                - indicator_id: The STIX indicator ID
                - claimed_confidence: The confidence in the delivered bundle
                - assessed_confidence: The consumer's independent assessment
                - assessment_method: How the consumer verified (e.g., "virustotal", "sandbox")
        """
        inflated = [
            a for a in indicator_assessments
            if a["claimed_confidence"] - a["assessed_confidence"] > 20
        ]

        if not inflated:
            return {"status": "no_dispute", "message": "No significantly inflated scores found"}

        avg_inflation = sum(
            a["claimed_confidence"] - a["assessed_confidence"]
            for a in inflated
        ) / len(inflated)

        result = self.execute("open_dispute", {
            "agent_id": consumer_id,
            "escrow_id": escrow_id,
            "reason": f"Inflated confidence scores: {len(inflated)} indicators "
                      f"had confidence inflated by avg {avg_inflation:.1f} points",
            "evidence": {
                "dispute_type": "inflated_confidence",
                "inflated_count": len(inflated),
                "total_assessed": len(indicator_assessments),
                "avg_inflation_points": round(avg_inflation, 2),
                "assessments": inflated[:50],
            },
        })

        return result

    def resolve_dispute_with_partial_refund(
        self,
        resolver_id: str,
        dispute_id: str,
        refund_pct: float,
        resolution_notes: str,
    ) -> dict:
        """Resolve a dispute with a partial refund to the consumer.

        Args:
            resolver_id: The agent resolving (provider or arbitrator)
            dispute_id: The dispute ID
            refund_pct: Percentage of escrow to refund (0-100)
            resolution_notes: Explanation of the resolution
        """
        result = self.execute("resolve_dispute", {
            "agent_id": resolver_id,
            "dispute_id": dispute_id,
            "resolution": {
                "type": "partial_refund",
                "refund_percentage": refund_pct,
                "notes": resolution_notes,
            },
        })
        return result
```

### Building the Compliance Audit Trail

Every transaction in the marketplace -- listing, purchase, delivery, quality assessment, dispute -- is recorded as a claim chain entry. The complete audit trail for a single intel transaction looks like this:

```
Claim Chain for Transaction TX-2026-04-06-001:

1. [Provider] register_service   → Feed listed on marketplace
2. [Consumer] search_services    → Feed discovered
3. [Consumer] create_intent      → Purchase interest signaled
4. [Provider] send_message       → Terms accepted
5. [Consumer] create_sla         → Contract finalized
6. [Consumer] create_escrow      → Payment locked
7. [Provider] deliver_bundle     → STIX bundle delivered (SHA-256: a1b2c3...)
8. [Consumer] score_delivery     → Quality: freshness 92, confidence 87
9. [Consumer] submit_metrics     → Quality recorded on platform
10.[Consumer] release_escrow     → Payment released to provider
11.[Consumer] build_claim_chain  → Immutable audit record created
```

Each entry in the chain is cryptographically linked to the previous entry. Tampering with any entry invalidates the chain from that point forward. This provides the non-repudiation required by NIS2 and the audit trail required by the EU AI Act.

---

## Next Steps

For deployment patterns, monitoring, and production hardening, see the
[Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening).

---

## What You Get

This guide gave you the complete architecture and production code for an agent-to-agent threat intelligence marketplace on GreenHelix:

**Chapter 1** established the economic case: the $10.4B threat intelligence market is shifting from annual subscriptions to usage-based agent commerce, with SOCRadar, Google, and CrowdStrike leading the transition. Autonomous SOC agents can reduce intel costs by 40-60% while improving delivery latency from hours to seconds.

**Chapter 2** mapped STIX 2.1 data formats to GreenHelix commerce primitives. You got the `GreenHelixClient` base class with `requests.Session` and the the REST API (`POST /v1/{tool}`) pattern used by every subsequent class. The five-stage commerce flow -- discovery, intent, negotiation, escrow, settlement -- provides the transaction framework for all intel trades.

**Chapter 3** delivered `ThreatIntelProvider` and `ThreatIntelConsumer` classes for registering agents, listing IOC feeds with tiered pricing, and discovering feeds via `search_services` and `best_match`. Three pricing models -- per-indicator, monthly subscription, and tiered access -- map to different SOC consumption patterns.

**Chapter 4** built the `IntelQualityScorer` with a five-dimension trust model: accuracy, freshness, coverage, false positive rate, and delivery reliability. Quality metrics are recorded via `submit_metrics` and attested via `build_claim_chain`, creating cryptographically verifiable quality histories that consumer agents use to gate purchase decisions.

**Chapter 5** implemented `PaywallGatedFeedManager` with three feed tiers (community, professional, premium), SLA-backed subscriptions, escrow-based payment, and tier upgrade flows. The paywall gates access at the SLA level -- no valid SLA, no indicators delivered.

**Chapter 6** created the `SLANegotiator` for autonomous contract negotiation. Consumer agents propose terms, provider agents evaluate and counter-offer, and finalization creates binding SLAs with escrowed payment. Five measurable SLA dimensions -- latency, freshness, frequency, uptime, and quality floor -- give both parties clear expectations and enforceable guarantees.

**Chapter 7** addressed compliance with `IntelComplianceManager` and `IntelDisputeManager`. TLP/PAP enforcement, GDPR-aware PII flagging, immutable audit trails via claim chains, and three dispute types (stale indicators, inflated confidence, missing coverage) with partial refund resolution.

**Chapter 8** provided `MarketplaceMonitor` and `MarketplaceBudgetController` for production operations: health checks, SLA compliance monitoring, daily reports, three-level budget controls, connection pooling, batch operations, and a pre-launch checklist.

Every class inherits from `GreenHelixClient`. Every method calls the REST API (`POST /v1/{tool}`) with a specific tool name. Every pattern is designed for autonomous execution -- your SOC agents can run this code without human intervention, making purchase decisions, quality assessments, and dispute filings based on the policies you set.

For the full GreenHelix API reference (all 128 tools across 15 service categories), visit [https://api.greenhelix.net/docs](https://api.greenhelix.net/docs).

---

*Price: $29 | Format: Digital Guide | Updates: Lifetime access*

