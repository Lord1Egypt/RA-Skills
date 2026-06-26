---
name: greenhelix-agent-commerce-discovery
version: "1.3.1"
description: "Agent Commerce Discovery. Build machine-readable service catalogs, knowledge graphs, and UCP/MCP/A2A protocol endpoints so AI shopping agents can discover, evaluate, and transact with your services autonomously."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [discovery, knowledge-graph, ucp, mcp, structured-data, schema-org, guide, greenhelix, openclaw, ai-agent]
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
# Agent Commerce Discovery

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `GREENHELIX_API_KEY`: API authentication for GreenHelix gateway (read/write access to purchased API tools only)
> - `AGENT_SIGNING_KEY`: Cryptographic signing key for agent identity (Ed25519 key pair for request signing)
> - `STRIPE_API_KEY`: Stripe API key for card payment processing (scoped to payment intents only)


Forty percent of digital commerce services are invisible to AI agents. Not because the services are bad, but because they are structured for humans -- HTML pages, marketing copy, PDF brochures -- and agents cannot parse any of it. The services exist, the demand exists, and the agents have budgets to spend. But the transaction never happens because the agent never finds the service. This is the discovery gap, and it is the single largest source of lost revenue in the agentic economy.
Between January 2025 and March 2026, AI-referred traffic to commerce services grew 805% year-over-year. Google Shopping Graph now indexes over 45 billion product listings with structured attributes. ChatGPT's product search handles 2.3 million commerce queries per day. Perplexity Shopping launched with 30+ retail partners and AI-native product cards. The agents are shopping. The question is whether they can find you.
This guide is the practitioner's manual for making your services discoverable to AI agents. It covers the full stack: knowledge graphs that model your service catalog as machine-readable entities, protocol endpoints that announce your capabilities through UCP, MCP, A2A, and ACP, structured data that agents can parse and compare, real-time catalog synchronization that prevents stale listings, trust signals that help agents rank you above competitors, and analytics that measure whether discovery is actually converting into transactions. Every chapter contains production Python code against the GreenHelix A2A Commerce Gateway -- 128 tools accessible at `https://api.greenhelix.net/v1` via a single the REST API (`POST /v1/{tool}`) endpoint.

## What You'll Learn
- Chapter 1: The Discovery Problem
- Chapter 2: Commerce Knowledge Graphs from Scratch
- Chapter 3: The Protocol Stack: UCP, MCP, A2A, ACP
- Chapter 4: Building .well-known Discovery Endpoints
- Chapter 5: Structured Data & Schema.org for Agent Readability
- Chapter 6: Real-Time Catalog Sync & Graph Maintenance
- Chapter 7: Trust Signals & Reputation in Agent Discovery
- Chapter 8: Measuring Discovery Performance
- Conclusion: The Discovery Flywheel

## Full Guide

# Agent Commerce Discovery: Knowledge Graphs, Protocol Endpoints & Structured Data for AI-Discoverable Services

Forty percent of digital commerce services are invisible to AI agents. Not because the services are bad, but because they are structured for humans -- HTML pages, marketing copy, PDF brochures -- and agents cannot parse any of it. The services exist, the demand exists, and the agents have budgets to spend. But the transaction never happens because the agent never finds the service. This is the discovery gap, and it is the single largest source of lost revenue in the agentic economy.

Between January 2025 and March 2026, AI-referred traffic to commerce services grew 805% year-over-year. Google Shopping Graph now indexes over 45 billion product listings with structured attributes. ChatGPT's product search handles 2.3 million commerce queries per day. Perplexity Shopping launched with 30+ retail partners and AI-native product cards. The agents are shopping. The question is whether they can find you.

This guide is the practitioner's manual for making your services discoverable to AI agents. It covers the full stack: knowledge graphs that model your service catalog as machine-readable entities, protocol endpoints that announce your capabilities through UCP, MCP, A2A, and ACP, structured data that agents can parse and compare, real-time catalog synchronization that prevents stale listings, trust signals that help agents rank you above competitors, and analytics that measure whether discovery is actually converting into transactions. Every chapter contains production Python code against the GreenHelix A2A Commerce Gateway -- 128 tools accessible at `https://api.greenhelix.net/v1` via a single the REST API (`POST /v1/{tool}`) endpoint.

---

## Table of Contents

1. [The Discovery Problem](#chapter-1-the-discovery-problem)
2. [Commerce Knowledge Graphs from Scratch](#chapter-2-commerce-knowledge-graphs-from-scratch)
3. [The Protocol Stack: UCP, MCP, A2A, ACP](#chapter-3-the-protocol-stack-ucp-mcp-a2a-acp)
4. [Building .well-known Discovery Endpoints](#chapter-4-building-well-known-discovery-endpoints)
5. [Structured Data & Schema.org for Agent Readability](#chapter-5-structured-data--schemaorg-for-agent-readability)
6. [Real-Time Catalog Sync & Graph Maintenance](#chapter-6-real-time-catalog-sync--graph-maintenance)
7. [Trust Signals & Reputation in Agent Discovery](#chapter-7-trust-signals--reputation-in-agent-discovery)
8. [Measuring Discovery Performance](#chapter-8-measuring-discovery-performance)

---

## Chapter 1: The Discovery Problem

### Why 40% of Commerce Services Are Invisible

The number comes from a March 2026 analysis by Forrester: of 2,400 digital service providers surveyed, 40.3% had no machine-readable service description of any kind -- no JSON-LD, no OpenAPI spec, no agent card, no structured catalog. Their services existed only as human-readable web pages. For AI agents performing commerce queries, these services might as well not exist.

The root cause is architectural. Traditional web commerce optimized for a single consumer: a human with a browser. The human reads marketing copy, interprets images, navigates menus, and fills out checkout forms. Every element of the commerce experience -- product descriptions, pricing pages, comparison charts, testimonials -- is designed for visual consumption by a person sitting at a screen. AI agents consume none of this. An agent does not "see" your landing page. It sends structured queries to discovery endpoints, parses JSON responses, compares attributes programmatically, and executes transactions via API. If your service is not described in a format agents can query, you are invisible to the fastest-growing channel in digital commerce.

### The Shift from Human Browsing to Agent Crawling

Human discovery follows a browse-and-click pattern: Google search, scan results, click through, read page, compare tabs, make decision. The entire flow assumes visual attention and manual navigation. Agent discovery follows a query-and-parse pattern: send structured query, receive structured response, compare attributes algorithmically, execute highest-ranked option. The flows have almost nothing in common.

| Dimension | Human Browsing | Agent Crawling |
|---|---|---|
| **Discovery method** | Keyword search, link following | Structured API queries, `.well-known` endpoint crawling |
| **Content format** | HTML, images, video | JSON-LD, OpenAPI specs, agent cards |
| **Comparison method** | Visual side-by-side, gut feeling | Programmatic attribute matching, scoring algorithms |
| **Decision speed** | Minutes to days | Milliseconds to seconds |
| **Price sensitivity** | Influenced by anchoring, framing | Exact numerical comparison with configurable thresholds |
| **Trust evaluation** | Reviews, brand recognition | Cryptographic verification, trust scores, claim chains |
| **Transaction method** | Shopping cart, checkout form | API call with payment proof |

The implication is stark: optimizing for human browsing does nothing for agent crawling. A beautifully designed landing page with compelling copy and high-resolution product photos generates zero signal for an agent that queries the REST API (`POST /v1/{tool}`) with `{"tool": "search_services", "input": {"query": "data enrichment API under $0.01 per call with 99.9% uptime SLA"}}`. The agent needs structured attributes, machine-readable pricing, and verifiable SLA terms. It needs to find your service through a discovery protocol, not a Google search.

### How the Major Platforms Do Discovery

**Google Shopping Graph** indexes 45 billion product listings by crawling structured data from merchant websites. It prioritizes Merchant Center feeds (structured XML/JSON), followed by Schema.org JSON-LD embedded in product pages, followed by inferred attributes from unstructured HTML (lowest priority, lowest accuracy). Products with complete structured data appear in AI Overviews, Shopping tab results, and Gemini product recommendations. Products without structured data are deprioritized or excluded entirely.

**ChatGPT Product Search** (launched with GPT-4o shopping in April 2025) uses a combination of web crawling and direct merchant integrations. It surfaces product cards with structured attributes -- price, ratings, availability, specifications -- pulled from merchant APIs, affiliate feeds, and Schema.org markup. Merchants integrated through ACP (Agentic Commerce Protocol) get priority placement because ACP provides real-time inventory and pricing data that ChatGPT can trust to be current.

**A2A Discovery** (Google's Agent-to-Agent protocol) uses Agent Cards published at `/.well-known/agent.json`. An agent discovers another agent by fetching its Agent Card, which describes capabilities, supported input/output formats, authentication requirements, and service endpoints. A2A discovery is agent-to-agent, not agent-to-product -- it is how autonomous agents find other agents to delegate tasks to or purchase services from.

**GreenHelix Marketplace** provides a unified discovery layer across all these patterns. The `search_services` tool queries the marketplace index using structured attributes. The `best_match` tool returns the single best service for a given requirement set. The `register_service` tool publishes your service with structured metadata that agents can query. Your service appears in marketplace search results and can be discovered by any agent with API access.

### The Cost of Being Undiscoverable

The 805% year-over-year growth in AI-referred traffic is not evenly distributed. It concentrates on services that are machine-readable. A March 2026 analysis of 500 SaaS products found that those with complete structured data (JSON-LD, OpenAPI spec, and at least one discovery protocol endpoint) captured 14x more AI-referred traffic than those without. The relationship was not proportional -- it was binary. Services were either discoverable or they were not. There was no middle ground of "partially discoverable."

The revenue impact is direct. AI-referred traffic converts at 2.3x the rate of organic search traffic because agents only send users (or other agents) to services that match the query criteria. An agent that finds your service has already verified that your pricing, capabilities, and availability meet the requirements. The "lead" is pre-qualified by the agent's scoring algorithm. Losing that channel means losing your highest-converting traffic source.

```python
import requests
from typing import Any


GATEWAY_URL = os.environ.get("GREENHELIX_API_URL", "https://sandbox.greenhelix.net")


class DiscoveryClient:
    """Client for GreenHelix A2A Commerce Gateway discovery operations."""

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

    def search_services(self, query: str, filters: dict | None = None) -> dict:
        """Search the GreenHelix marketplace for services."""
        payload = {"query": query}
        if filters:
            payload["filters"] = filters
        return self.execute("search_services", payload)

    def best_match(self, requirements: dict) -> dict:
        """Find the single best service match for given requirements."""
        return self.execute("best_match", requirements)


# Initialize -- used throughout this guide
client = DiscoveryClient(api_key="your-api-key-here")

# Example: search for data enrichment services
results = client.search_services(
    query="data enrichment API",
    filters={
        "max_price_per_call": 0.01,
        "min_uptime_sla": 99.9,
        "protocols": ["ucp", "a2a"],
    },
)
print(f"Found {len(results.get('services', []))} matching services")
```

This client object is referenced in every subsequent chapter. Store your API key in an environment variable (`GREENHELIX_API_KEY`), never in source code.

> **Key Takeaways**
>
> - 40% of digital services have zero machine-readable descriptions. They are invisible to AI agents regardless of quality.
> - AI-referred commerce traffic grew 805% YoY. Services with complete structured data capture 14x more of this traffic.
> - Agent discovery is query-and-parse, not browse-and-click. Optimizing for humans does nothing for agents.
> - Google Shopping Graph, ChatGPT, A2A, and GreenHelix all rely on structured data. No structured data means no discovery.
> - See P21 (Agent-Ready Commerce) for building the full agent-ready storefront on top of discovery.

---

## Chapter 2: Commerce Knowledge Graphs from Scratch

### What Is a Commerce Knowledge Graph?

A knowledge graph is a structured representation of entities, their properties, and the relationships between them. In commerce, the entities are services, providers, pricing tiers, SLAs, certifications, and transactions. The relationships connect them: a provider *offers* a service, a service *has* a pricing tier, a pricing tier *includes* an SLA, an SLA *guarantees* an uptime level. The properties are the machine-readable attributes: price per call, latency percentile, geographic availability, supported authentication methods.

Traditional databases store this data in tables. Knowledge graphs store it as triples: subject-predicate-object. "DataEnrichmentAPI" -- "hasPricing" -- "PayPerCallTier". "PayPerCallTier" -- "costPerCall" -- "0.005 USD". "DataEnrichmentAPI" -- "guarantees" -- "99.95% Uptime SLA". The advantage of the graph structure is that agents can traverse relationships without knowing the schema in advance. An agent can start from a service node, follow edges to discover pricing, SLA terms, trust scores, and provider identity -- all without a predefined query template.

### Entities, Relationships, and Properties

A commerce knowledge graph for agent-discoverable services contains five core entity types:

| Entity Type | Description | Key Properties |
|---|---|---|
| **Service** | The product or capability being offered | name, description, category, version, status |
| **Provider** | The entity (agent or organization) offering the service | agent_id, public_key, registration_date, trust_score |
| **PricingTier** | A specific pricing configuration | tier_name, cost_per_call, monthly_cap, currency, billing_model |
| **SLA** | Service level agreement terms | uptime_guarantee, latency_p99, support_response_time |
| **Certification** | Verified claims about the service or provider | cert_type, issuer, valid_from, valid_until, verification_hash |

The relationships between these entities form the graph:

```
Provider --[offers]--> Service
Service --[hasPricing]--> PricingTier
Service --[guarantees]--> SLA
Provider --[holds]--> Certification
Service --[requires]--> Certification (for consumers)
Service --[dependsOn]--> Service (for composed services)
```

### Modeling Your Service Catalog as a Graph

The first step is translating your existing service catalog into graph form. Most teams start with a flat list of services in a database table or a YAML config file. The graph transformation adds structure that agents can navigate.

```python
import json
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class SLA:
    uptime_guarantee: float
    latency_p99_ms: int
    support_response_hours: int
    penalty_per_violation_pct: float = 5.0


@dataclass
class PricingTier:
    tier_name: str
    cost_per_call: float
    currency: str = "USD"
    monthly_cap: Optional[float] = None
    billing_model: str = "pay_per_call"
    volume_discounts: dict = field(default_factory=dict)


@dataclass
class ServiceNode:
    service_id: str
    name: str
    description: str
    category: str
    version: str
    provider_agent_id: str
    pricing_tiers: list[PricingTier] = field(default_factory=list)
    sla: Optional[SLA] = None
    tags: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)
    supported_protocols: list[str] = field(default_factory=list)
    status: str = "active"


class CommerceKnowledgeGraph:
    """In-memory knowledge graph for agent-discoverable services."""

    def __init__(self):
        self.services: dict[str, ServiceNode] = {}
        self.edges: list[dict] = []

    def add_service(self, service: ServiceNode) -> None:
        """Add a service node to the graph."""
        self.services[service.service_id] = service

        # Auto-generate relationship edges
        for tier in service.pricing_tiers:
            self.edges.append({
                "subject": service.service_id,
                "predicate": "hasPricing",
                "object": tier.tier_name,
                "properties": asdict(tier),
            })

        if service.sla:
            self.edges.append({
                "subject": service.service_id,
                "predicate": "guarantees",
                "object": f"{service.service_id}_sla",
                "properties": asdict(service.sla),
            })

        for dep in service.dependencies:
            self.edges.append({
                "subject": service.service_id,
                "predicate": "dependsOn",
                "object": dep,
            })

    def query_by_attribute(self, **kwargs) -> list[ServiceNode]:
        """Query services by attribute filters."""
        results = []
        for service in self.services.values():
            match = True
            for key, value in kwargs.items():
                if key == "max_cost_per_call":
                    if not any(
                        t.cost_per_call <= value
                        for t in service.pricing_tiers
                    ):
                        match = False
                elif key == "min_uptime":
                    if not service.sla or service.sla.uptime_guarantee < value:
                        match = False
                elif key == "category":
                    if service.category != value:
                        match = False
                elif key == "protocol":
                    if value not in service.supported_protocols:
                        match = False
            if match:
                results.append(service)
        return results

    def to_jsonld(self) -> list[dict]:
        """Export the graph as JSON-LD for agent consumption."""
        output = []
        for service in self.services.values():
            node = {
                "@context": "https://schema.org",
                "@type": "Service",
                "@id": f"urn:greenhelix:service:{service.service_id}",
                "name": service.name,
                "description": service.description,
                "category": service.category,
                "version": service.version,
                "provider": {
                    "@type": "Organization",
                    "identifier": service.provider_agent_id,
                },
                "offers": [
                    {
                        "@type": "Offer",
                        "name": tier.tier_name,
                        "price": str(tier.cost_per_call),
                        "priceCurrency": tier.currency,
                        "priceSpecification": {
                            "@type": "UnitPriceSpecification",
                            "price": str(tier.cost_per_call),
                            "priceCurrency": tier.currency,
                            "unitText": "per API call",
                            "billingModel": tier.billing_model,
                        },
                    }
                    for tier in service.pricing_tiers
                ],
            }
            if service.sla:
                node["termsOfService"] = {
                    "uptimeGuarantee": service.sla.uptime_guarantee,
                    "latencyP99Ms": service.sla.latency_p99_ms,
                    "supportResponseHours": service.sla.support_response_hours,
                }
            output.append(node)
        return output

    def sync_to_marketplace(self, discovery_client) -> list[dict]:
        """Register all services on GreenHelix marketplace."""
        results = []
        for service in self.services.values():
            cheapest_tier = min(
                service.pricing_tiers,
                key=lambda t: t.cost_per_call,
            ) if service.pricing_tiers else None

            result = discovery_client.execute("register_service", {
                "agent_id": service.provider_agent_id,
                "service_name": service.name,
                "description": service.description,
                "category": service.category,
                "tags": service.tags,
                "pricing": {
                    "model": cheapest_tier.billing_model if cheapest_tier else "contact",
                    "base_price": str(cheapest_tier.cost_per_call) if cheapest_tier else "0",
                    "currency": cheapest_tier.currency if cheapest_tier else "USD",
                },
                "sla": asdict(service.sla) if service.sla else None,
                "protocols": service.supported_protocols,
            })
            results.append(result)
        return results


# Build a sample graph
graph = CommerceKnowledgeGraph()

graph.add_service(ServiceNode(
    service_id="data-enrichment-v2",
    name="DataEnrich Pro",
    description="Real-time company data enrichment with 95% match rate",
    category="data-enrichment",
    version="2.1.0",
    provider_agent_id="agent-dataenrich-prod",
    pricing_tiers=[
        PricingTier("starter", cost_per_call=0.005, monthly_cap=100.0),
        PricingTier("growth", cost_per_call=0.003, monthly_cap=500.0,
                    volume_discounts={"10000": 0.002, "100000": 0.001}),
    ],
    sla=SLA(uptime_guarantee=99.95, latency_p99_ms=200,
            support_response_hours=4),
    tags=["enrichment", "company-data", "real-time", "api"],
    supported_protocols=["ucp", "a2a", "mcp"],
))

graph.add_service(ServiceNode(
    service_id="sentiment-analysis-v3",
    name="SentimentLens",
    description="Multi-language sentiment analysis with aspect extraction",
    category="nlp",
    version="3.0.1",
    provider_agent_id="agent-sentimentlens-prod",
    pricing_tiers=[
        PricingTier("basic", cost_per_call=0.001),
        PricingTier("premium", cost_per_call=0.008,
                    volume_discounts={"50000": 0.005}),
    ],
    sla=SLA(uptime_guarantee=99.9, latency_p99_ms=150,
            support_response_hours=8),
    tags=["nlp", "sentiment", "multilingual", "aspect-extraction"],
    supported_protocols=["ucp", "mcp"],
))

# Query the graph
cheap_services = graph.query_by_attribute(
    max_cost_per_call=0.005,
    min_uptime=99.9,
)
print(f"Services matching criteria: {[s.name for s in cheap_services]}")

# Export as JSON-LD
jsonld = graph.to_jsonld()
print(json.dumps(jsonld[0], indent=2))
```

### JSON-LD and Schema.org Vocabulary

JSON-LD (JavaScript Object Notation for Linked Data) is the standard format for embedding structured data in web pages and API responses. It uses `@context` to map property names to Schema.org URIs, `@type` to declare the entity type, and `@id` to provide a globally unique identifier. AI agents -- whether they are Google's crawlers, ChatGPT's shopping engine, or a GreenHelix marketplace indexer -- parse JSON-LD to extract structured attributes.

The Schema.org vocabulary provides standardized types for commerce: `Service`, `Offer`, `Organization`, `PriceSpecification`, `AggregateRating`, `Review`. Using these types ensures your data is interoperable across all agent ecosystems. A service described as `@type: Service` with `offers` containing `@type: Offer` and `priceSpecification` will be parsed identically by Google Shopping Graph, Perplexity Shopping, and GreenHelix `search_services`.

The `to_jsonld()` method in the `CommerceKnowledgeGraph` class above handles the conversion. The critical detail is using string representations for prices (`str(tier.cost_per_call)`) rather than floats, avoiding floating-point precision issues that cause agents to reject or miscompare pricing data. See P18 (Pricing & Monetization) for the full treatment of decimal-safe pricing.

> **Key Takeaways**
>
> - A commerce knowledge graph models services as entities with typed relationships: provider offers service, service has pricing, pricing includes SLA.
> - Five core entity types: Service, Provider, PricingTier, SLA, Certification. Each has machine-readable properties.
> - JSON-LD with Schema.org vocabulary is the interoperability standard. All major agent platforms parse it.
> - Build the graph in code, export as JSON-LD for web crawlers, and sync to GreenHelix marketplace via `register_service` for agent-native discovery.
> - Always use string-typed prices to avoid floating-point comparison failures.

---

## Chapter 3: The Protocol Stack: UCP, MCP, A2A, ACP

### Four Protocols, Four Jobs

The agentic commerce stack has consolidated around four protocols, each solving a distinct problem in the discovery-to-transaction lifecycle. Implementing the wrong one first wastes months. Implementing all four without understanding the dependencies creates a maintenance burden that outweighs the benefit. This chapter provides the decision framework.

**UCP (Unified Commerce Protocol)** is the discovery and capability advertisement layer. A UCP profile published at `/.well-known/ucp` tells agents what your service does, how it is priced, what payment methods it accepts, and where to find its API. UCP is the front door. Without it, agents that crawl for services have no standard entry point. UCP profiles are JSON documents with a defined schema: capabilities, pricing, authentication requirements, SLA terms, and payment methods. Think of it as a machine-readable business card that also includes the full menu and the credit card terminal specs.

**MCP (Model Context Protocol)** is the tool execution layer. An MCP server exposes tools -- functions with JSON Schema-defined inputs and outputs -- that LLMs and agents can call. MCP handles tool discovery (listing available tools and their schemas), tool invocation (sending structured inputs and receiving structured outputs), and context management (maintaining state across multi-turn tool interactions). If UCP tells an agent your service exists, MCP tells it how to call your service.

**A2A (Agent-to-Agent Protocol)** is the task delegation layer. A2A defines how agents discover each other (Agent Cards at `/.well-known/agent.json`), exchange task requests (JSON-based task messages with structured parts), and stream progress updates (Server-Sent Events). A2A is designed for agent-to-agent workflows where one agent delegates a task to another, monitors progress, and receives results. It overlaps with MCP in discovery but diverges in execution: MCP is function-call oriented, A2A is task-oriented.

**ACP (Agentic Commerce Protocol)** is the payment and checkout layer. ACP extends Stripe Checkout for AI agents, providing structured product catalogs, cart management, and payment flow orchestration. ACP is the narrowest of the four protocols -- it specifically handles the commercial transaction, not discovery, not tool execution, not task delegation.

### The Dependency Chain

The protocols are not independent. They form a dependency chain:

```
Discovery        Execution         Transaction
┌──────┐        ┌──────┐          ┌──────┐
│ UCP  │───────▶│ MCP  │─────────▶│ ACP  │
│      │───────▶│ A2A  │─────────▶│      │
└──────┘        └──────┘          └──────┘
```

UCP must come first. An agent cannot call your MCP tools or send you A2A tasks if it cannot discover you. MCP and A2A operate in parallel -- some agents prefer function calls (MCP), others prefer task delegation (A2A), many support both. ACP comes last because payment only matters after an agent has discovered your service and decided to use it.

### Decision Matrix: Which Protocol to Implement First

| Factor | UCP First | MCP First | A2A First | ACP First |
|---|---|---|---|---|
| **You sell API services** | Yes -- agents need to discover your capabilities | Second -- expose tools after discovery | Optional -- most API consumers prefer MCP | Third -- add payment after execution works |
| **You sell to LLM-powered agents** | Yes | Yes -- LLMs call MCP tools natively | Lower priority | After MCP |
| **You sell to autonomous agent fleets** | Yes | Optional | Yes -- fleets use A2A for task delegation | After A2A |
| **You are a marketplace** | Yes | Yes -- expose search/purchase as tools | Yes -- agents discover marketplace via A2A | Yes -- checkout via ACP |
| **You need payment immediately** | Still first -- discovery before payment | No | No | No -- useless without discovery |

The universal answer: **implement UCP first, then MCP or A2A depending on your buyer profile, then ACP**.

### Protocol Selection Logic

```python
def select_protocols(
    service_type: str,
    buyer_profile: str,
    needs_payment: bool,
    existing_protocols: list[str],
) -> list[dict]:
    """Determine which discovery protocols to implement and in what order.

    Returns prioritized list of protocols with implementation guidance.
    """
    recommendations = []

    # UCP is always first -- it is the discovery foundation
    if "ucp" not in existing_protocols:
        recommendations.append({
            "protocol": "ucp",
            "priority": 1,
            "reason": "Discovery foundation -- agents cannot find you without it",
            "effort_days": 2,
            "endpoint": "/.well-known/ucp",
        })

    # MCP vs A2A depends on buyer profile
    if buyer_profile in ("llm_agents", "api_consumers", "developers"):
        if "mcp" not in existing_protocols:
            recommendations.append({
                "protocol": "mcp",
                "priority": 2,
                "reason": "LLM agents and API consumers prefer function-call semantics",
                "effort_days": 3,
                "endpoint": "/mcp/tools",
            })
        if "a2a" not in existing_protocols:
            recommendations.append({
                "protocol": "a2a",
                "priority": 3,
                "reason": "Secondary -- covers autonomous agent fleets",
                "effort_days": 4,
                "endpoint": "/.well-known/agent.json",
            })
    elif buyer_profile in ("autonomous_fleets", "enterprise_agents"):
        if "a2a" not in existing_protocols:
            recommendations.append({
                "protocol": "a2a",
                "priority": 2,
                "reason": "Autonomous fleets use A2A for task delegation",
                "effort_days": 4,
                "endpoint": "/.well-known/agent.json",
            })
        if "mcp" not in existing_protocols:
            recommendations.append({
                "protocol": "mcp",
                "priority": 3,
                "reason": "Secondary -- covers LLM-based tool calling",
                "effort_days": 3,
                "endpoint": "/mcp/tools",
            })

    # ACP always comes after execution layer
    if needs_payment and "acp" not in existing_protocols:
        recommendations.append({
            "protocol": "acp",
            "priority": 4,
            "reason": "Payment layer -- implement after discovery and execution",
            "effort_days": 5,
            "endpoint": "/acp/checkout",
        })

    return sorted(recommendations, key=lambda r: r["priority"])


# Example: SaaS API selling to LLM-powered agents
plan = select_protocols(
    service_type="api_service",
    buyer_profile="llm_agents",
    needs_payment=True,
    existing_protocols=[],
)
for step in plan:
    print(f"Priority {step['priority']}: {step['protocol'].upper()} "
          f"({step['effort_days']} days) -- {step['reason']}")
```

### Registering Protocol Support on GreenHelix

Once you have implemented protocol endpoints, register them on the marketplace so agents know which protocols you support:

```python
# Register your service with protocol metadata
result = client.execute("register_service", {
    "agent_id": "agent-dataenrich-prod",
    "service_name": "DataEnrich Pro",
    "description": "Real-time company data enrichment API",
    "category": "data-enrichment",
    "tags": ["enrichment", "company-data", "api"],
    "pricing": {
        "model": "pay_per_call",
        "base_price": "0.005",
        "currency": "USD",
    },
    "protocols": ["ucp", "mcp", "a2a"],
    "endpoints": {
        "ucp": "https://dataenrich.example.com/.well-known/ucp",
        "mcp": "https://dataenrich.example.com/mcp/tools",
        "a2a": "https://dataenrich.example.com/.well-known/agent.json",
    },
})
print(f"Service registered: {result}")
```

Agents searching the marketplace can then filter by protocol:

```python
# Find services that support A2A
a2a_services = client.search_services(
    query="data enrichment",
    filters={"protocols": ["a2a"]},
)
```

> **Key Takeaways**
>
> - Four protocols form a stack: UCP (discovery), MCP (tool execution), A2A (task delegation), ACP (payment).
> - UCP is always implemented first. Without discovery, no other protocol matters.
> - MCP for LLM-powered agents, A2A for autonomous agent fleets. Most services should implement both.
> - ACP handles payment and is always implemented last in the chain.
> - Register protocol endpoints on GreenHelix via `register_service` so agents can filter by supported protocol.
> - See P21 (Agent-Ready Commerce) Chapter 3 for detailed UCP/ACP/x402 payment rail comparison.

---

## Chapter 4: Building .well-known Discovery Endpoints

### The Discovery Endpoint Pattern

The `.well-known` URI pattern (RFC 8615) provides a standardized location for machine-readable metadata. Agents crawling for services check these paths before attempting any other discovery method. If your service is at `https://api.example.com`, agents will look for:

- `https://api.example.com/.well-known/ucp` -- UCP service profile
- `https://api.example.com/.well-known/agent.json` -- A2A agent card
- `https://api.example.com/.well-known/ai-plugin.json` -- OpenAI/ChatGPT plugin manifest
- `https://api.example.com/.well-known/openapi.yaml` -- OpenAPI specification

Missing any of these endpoints means missing agents that use that specific discovery method. The cost of serving static JSON at four paths is trivial. The cost of not serving it is invisibility to entire agent ecosystems.

### UCP Profile: The Complete Service Advertisement

The UCP profile is the most comprehensive discovery document. It combines capability advertisement, pricing, payment methods, SLA terms, and API documentation references into a single JSON document.

```python
import json
from datetime import datetime, timezone


def build_ucp_profile(
    service_name: str,
    service_description: str,
    provider_agent_id: str,
    capabilities: list[dict],
    pricing_tiers: list[dict],
    payment_methods: list[str],
    sla: dict,
    api_spec_url: str,
    trust_score: float | None = None,
) -> dict:
    """Build a UCP profile document for /.well-known/ucp."""
    profile = {
        "ucp_version": "1.0",
        "service": {
            "name": service_name,
            "description": service_description,
            "provider": {
                "agent_id": provider_agent_id,
                "trust_score": trust_score,
                "verification_status": "verified" if trust_score and trust_score > 0.7 else "unverified",
            },
            "status": "active",
            "last_updated": datetime.now(timezone.utc).isoformat(),
        },
        "capabilities": capabilities,
        "pricing": {
            "tiers": pricing_tiers,
            "currency": "USD",
            "billing_models": list({t.get("billing_model", "pay_per_call") for t in pricing_tiers}),
        },
        "payment_methods": payment_methods,
        "sla": sla,
        "api": {
            "specification": api_spec_url,
            "format": "openapi-3.1",
            "authentication": {
                "type": "bearer",
                "token_endpoint": None,  # None for API-key auth
            },
        },
        "discovery": {
            "protocols": ["ucp", "mcp", "a2a"],
            "mcp_endpoint": "/mcp/tools",
            "a2a_agent_card": "/.well-known/agent.json",
        },
    }
    return profile


# Build profile for our data enrichment service
ucp_profile = build_ucp_profile(
    service_name="DataEnrich Pro",
    service_description="Real-time company data enrichment with 95% match rate across 200M+ companies",
    provider_agent_id="agent-dataenrich-prod",
    capabilities=[
        {
            "name": "company_lookup",
            "description": "Enrich company data from domain, name, or LinkedIn URL",
            "input_schema": {"domain": "string", "company_name": "string?"},
            "output_schema": {"company": "CompanyProfile"},
            "latency_p99_ms": 200,
        },
        {
            "name": "contact_enrichment",
            "description": "Enrich contact details from email or name + company",
            "input_schema": {"email": "string?", "name": "string?", "company": "string?"},
            "output_schema": {"contact": "ContactProfile"},
            "latency_p99_ms": 350,
        },
    ],
    pricing_tiers=[
        {
            "name": "starter",
            "cost_per_call": "0.005",
            "monthly_cap": "100.00",
            "billing_model": "pay_per_call",
        },
        {
            "name": "growth",
            "cost_per_call": "0.003",
            "monthly_cap": "500.00",
            "billing_model": "pay_per_call",
            "volume_discounts": {"10000": "0.002", "100000": "0.001"},
        },
    ],
    payment_methods=["greenhelix_escrow", "stripe", "x402_usdc"],
    sla={
        "uptime_guarantee": 99.95,
        "latency_p99_ms": 200,
        "support_response_hours": 4,
        "data_retention_days": 30,
    },
    api_spec_url="https://dataenrich.example.com/.well-known/openapi.yaml",
    trust_score=0.92,
)

print(json.dumps(ucp_profile, indent=2))
```

### MCP Tool Manifest

The MCP tool manifest describes each tool's input and output schemas so LLMs can discover and call them:

```python
def build_mcp_manifest(capabilities: list[dict]) -> dict:
    """Build an MCP tool manifest from service capabilities."""
    tools = []
    for cap in capabilities:
        tool = {
            "name": cap["name"],
            "description": cap["description"],
            "inputSchema": {
                "type": "object",
                "properties": {
                    k: {"type": v.rstrip("?")}
                    for k, v in cap.get("input_schema", {}).items()
                },
                "required": [
                    k for k, v in cap.get("input_schema", {}).items()
                    if not v.endswith("?")
                ],
            },
        }
        tools.append(tool)

    return {
        "schema_version": "2025-03-26",
        "server_info": {
            "name": "dataenrich-mcp",
            "version": "2.1.0",
        },
        "tools": tools,
    }
```

### A2A Agent Card

The A2A agent card is simpler -- it describes the agent's identity, capabilities, and communication preferences:

```python
def build_a2a_agent_card(
    agent_id: str,
    name: str,
    description: str,
    skills: list[dict],
    endpoint: str,
) -> dict:
    """Build an A2A Agent Card for /.well-known/agent.json."""
    return {
        "name": name,
        "description": description,
        "url": endpoint,
        "version": "1.0.0",
        "capabilities": {
            "streaming": True,
            "pushNotifications": False,
            "stateTransitionHistory": True,
        },
        "authentication": {
            "schemes": ["bearer"],
        },
        "defaultInputModes": ["application/json"],
        "defaultOutputModes": ["application/json"],
        "skills": skills,
    }


agent_card = build_a2a_agent_card(
    agent_id="agent-dataenrich-prod",
    name="DataEnrich Pro Agent",
    description="Autonomous data enrichment agent with 95% match rate",
    skills=[
        {
            "id": "company_lookup",
            "name": "Company Data Lookup",
            "description": "Enrich company data from domain or name",
            "tags": ["enrichment", "company-data"],
            "examples": ["Enrich data for openai.com", "Look up Stripe company info"],
        },
        {
            "id": "contact_enrichment",
            "name": "Contact Enrichment",
            "description": "Enrich contact details from email or name",
            "tags": ["enrichment", "contacts"],
            "examples": ["Find details for jane@example.com"],
        },
    ],
    endpoint="https://dataenrich.example.com/a2a",
)
```

### The FastAPI Service: All Endpoints Together

Here is a complete FastAPI service that serves all discovery endpoints and validates them against GreenHelix `search_services` and `best_match`:

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI(title="DataEnrich Pro -- Agent-Discoverable Service")


@app.get("/.well-known/ucp")
async def ucp_endpoint():
    """UCP service profile for agent discovery."""
    return JSONResponse(content=ucp_profile)


@app.get("/.well-known/agent.json")
async def a2a_agent_card_endpoint():
    """A2A Agent Card for agent-to-agent discovery."""
    return JSONResponse(content=agent_card)


@app.get("/mcp/tools")
async def mcp_tools_endpoint():
    """MCP tool manifest for LLM tool discovery."""
    manifest = build_mcp_manifest(ucp_profile["capabilities"])
    return JSONResponse(content=manifest)


@app.get("/.well-known/ai-plugin.json")
async def ai_plugin_endpoint():
    """OpenAI-compatible plugin manifest."""
    return JSONResponse(content={
        "schema_version": "v1",
        "name_for_human": "DataEnrich Pro",
        "name_for_model": "dataenrich_pro",
        "description_for_human": "Real-time company and contact data enrichment.",
        "description_for_model": (
            "Real-time data enrichment API. Supports company lookup by domain "
            "or name (200M+ companies, 95% match rate) and contact enrichment "
            "by email. Returns structured JSON with 50+ fields. Pricing: "
            "$0.003-$0.005 per call. Uptime SLA: 99.95%. Supports UCP, MCP, A2A."
        ),
        "auth": {"type": "service_http", "authorization_type": "bearer"},
        "api": {
            "type": "openapi",
            "url": "https://dataenrich.example.com/.well-known/openapi.yaml",
        },
    })


@app.get("/health")
async def health():
    return {"status": "ok"}


# Validation: test that your service is discoverable via GreenHelix
def validate_discovery():
    """Verify the service appears in GreenHelix search results."""
    # Search for our service by capability
    results = client.search_services(
        query="company data enrichment real-time",
        filters={"protocols": ["ucp", "mcp"]},
    )
    services = results.get("services", [])
    our_service = next(
        (s for s in services if s.get("agent_id") == "agent-dataenrich-prod"),
        None,
    )

    if not our_service:
        print("WARNING: Service not found in marketplace search results")
        print("Run register_service first (see Chapter 2)")
        return False

    # Verify best_match picks us for a targeted query
    match = client.best_match({
        "query": "data enrichment with 99%+ uptime and under $0.01 per call",
        "required_protocols": ["ucp"],
    })
    if match.get("agent_id") == "agent-dataenrich-prod":
        print("PASS: best_match returns our service for targeted query")
    else:
        print(f"INFO: best_match returned {match.get('agent_id')} -- "
              f"consider improving your listing attributes")

    return True


if __name__ == "__main__":
    validate_discovery()
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

### Discovery Endpoint Checklist

| Endpoint | Path | Format | Who Reads It |
|---|---|---|---|
| UCP Profile | `/.well-known/ucp` | JSON | UCP-compatible agents, GreenHelix marketplace indexer |
| A2A Agent Card | `/.well-known/agent.json` | JSON | Google A2A agents, autonomous fleets |
| MCP Tools | `/mcp/tools` | JSON | Claude, Cursor, Windsurf, LLM-based agents |
| AI Plugin | `/.well-known/ai-plugin.json` | JSON | ChatGPT, OpenAI-ecosystem agents |
| OpenAPI Spec | `/.well-known/openapi.yaml` | YAML | All programmatic consumers |

> **Key Takeaways**
>
> - Four `.well-known` endpoints cover the major agent discovery methods. Each takes minutes to implement and costs nothing to serve.
> - UCP profile is the most comprehensive: capabilities, pricing, SLA, payment methods, and cross-references to other endpoints.
> - MCP manifests let LLMs discover your tools. A2A agent cards let autonomous agents discover your capabilities.
> - Validate discovery by searching for your own service via GreenHelix `search_services` and `best_match`.
> - See P20 (Production Hardening) for rate-limiting and caching these endpoints at scale.

---

## Chapter 5: Structured Data & Schema.org for Agent Readability

### Why Schema.org Wins for Agent Discovery

Schema.org is the lingua franca of structured data on the web. Google, Bing, Yahoo, and Yandex jointly maintain it. Over 40 million websites use Schema.org markup. More importantly for agent commerce: every major AI shopping agent -- Google Gemini, ChatGPT, Perplexity, Claude -- parses Schema.org JSON-LD. When an agent encounters a `@type: Service` node with `offers`, `priceSpecification`, and `aggregateRating`, it extracts those fields into a comparable data structure regardless of which agent platform is doing the reading.

The alternative -- custom JSON schemas -- works for a single agent ecosystem but fails for cross-ecosystem discovery. An agent built for Google A2A might not understand your custom schema. An agent using ChatGPT's product search definitely will not. Schema.org is the only vocabulary that works everywhere.

### JSON-LD for Digital Services

Physical products have standardized Schema.org types: `Product`, `Offer`, `AggregateOffer`. Digital services require a slightly different approach because they have properties that physical products do not: SLA terms, API latency, uptime guarantees, supported protocols, rate limits. The correct mapping uses `Service` as the primary type, with `Offer` for pricing and custom properties for service-specific attributes.

```python
import json
from datetime import datetime, timezone


def build_service_jsonld(
    service_id: str,
    name: str,
    description: str,
    provider_name: str,
    provider_agent_id: str,
    category: str,
    pricing_tiers: list[dict],
    sla: dict,
    rating: dict | None = None,
    supported_protocols: list[str] | None = None,
    availability: str = "InStock",
) -> dict:
    """Build Schema.org JSON-LD for a digital service.

    Produces a document parseable by Google Shopping Graph, ChatGPT,
    Perplexity Shopping, and GreenHelix marketplace indexer.
    """
    jsonld = {
        "@context": "https://schema.org",
        "@type": "Service",
        "@id": f"urn:greenhelix:service:{service_id}",
        "name": name,
        "description": description,
        "serviceType": category,
        "provider": {
            "@type": "Organization",
            "name": provider_name,
            "identifier": provider_agent_id,
        },
        "offers": [],
        "termsOfService": f"https://api.example.com/tos/{service_id}",
        "availableChannel": {
            "@type": "ServiceChannel",
            "serviceType": "API",
            "availableLanguage": ["en"],
        },
    }

    # Add pricing tiers as offers
    for tier in pricing_tiers:
        offer = {
            "@type": "Offer",
            "name": tier["name"],
            "price": str(tier["cost_per_call"]),
            "priceCurrency": tier.get("currency", "USD"),
            "availability": f"https://schema.org/{availability}",
            "priceValidUntil": tier.get(
                "valid_until",
                datetime(2026, 12, 31, tzinfo=timezone.utc).isoformat(),
            ),
            "priceSpecification": {
                "@type": "UnitPriceSpecification",
                "price": str(tier["cost_per_call"]),
                "priceCurrency": tier.get("currency", "USD"),
                "unitText": "per API call",
                "referenceQuantity": {
                    "@type": "QuantitativeValue",
                    "value": 1,
                    "unitCode": "C62",  # ISO unit for "one"
                },
            },
        }
        if "monthly_cap" in tier:
            offer["priceSpecification"]["maxPrice"] = str(tier["monthly_cap"])
        jsonld["offers"].append(offer)

    # Add SLA as custom properties (agents parse these for comparison)
    if sla:
        jsonld["additionalProperty"] = [
            {
                "@type": "PropertyValue",
                "name": "uptimeGuarantee",
                "value": sla.get("uptime_guarantee", 99.9),
                "unitText": "percent",
            },
            {
                "@type": "PropertyValue",
                "name": "latencyP99",
                "value": sla.get("latency_p99_ms", 500),
                "unitText": "milliseconds",
            },
            {
                "@type": "PropertyValue",
                "name": "supportResponseTime",
                "value": sla.get("support_response_hours", 24),
                "unitText": "hours",
            },
        ]

    # Add aggregate rating if available
    if rating:
        jsonld["aggregateRating"] = {
            "@type": "AggregateRating",
            "ratingValue": rating["value"],
            "bestRating": 5,
            "ratingCount": rating["count"],
        }

    # Add protocol support as additional properties
    if supported_protocols:
        jsonld["additionalProperty"].append({
            "@type": "PropertyValue",
            "name": "supportedProtocols",
            "value": ", ".join(supported_protocols),
        })

    return jsonld


# Generate JSON-LD for our service
service_schema = build_service_jsonld(
    service_id="data-enrichment-v2",
    name="DataEnrich Pro",
    description="Real-time company data enrichment with 95% match rate across 200M+ companies. "
                "Returns 50+ structured fields per company including firmographics, technographics, "
                "and funding data.",
    provider_name="DataEnrich Inc.",
    provider_agent_id="agent-dataenrich-prod",
    category="data-enrichment",
    pricing_tiers=[
        {"name": "Starter", "cost_per_call": "0.005", "monthly_cap": "100.00"},
        {"name": "Growth", "cost_per_call": "0.003", "monthly_cap": "500.00"},
    ],
    sla={
        "uptime_guarantee": 99.95,
        "latency_p99_ms": 200,
        "support_response_hours": 4,
    },
    rating={"value": 4.8, "count": 342},
    supported_protocols=["ucp", "mcp", "a2a"],
)

print(json.dumps(service_schema, indent=2))
```

### Auto-Generating Structured Data via GreenHelix

When you register a service on the GreenHelix marketplace, the gateway can auto-generate Schema.org JSON-LD from your registration data. This ensures consistency between your marketplace listing and your web-embedded structured data.

```python
def register_and_generate_schema(
    discovery_client,
    service_data: dict,
) -> tuple[dict, dict]:
    """Register a service on GreenHelix and generate matching Schema.org JSON-LD.

    Returns (registration_result, jsonld_schema).
    """
    # Register on marketplace
    registration = discovery_client.execute("register_service", {
        "agent_id": service_data["provider_agent_id"],
        "service_name": service_data["name"],
        "description": service_data["description"],
        "category": service_data["category"],
        "tags": service_data.get("tags", []),
        "pricing": service_data["pricing"],
        "sla": service_data.get("sla"),
        "protocols": service_data.get("protocols", []),
    })

    # Fetch the listing back to get canonical data
    listing = discovery_client.execute("get_service", {
        "service_id": registration.get("service_id", service_data["name"]),
    })

    # Generate JSON-LD from canonical listing
    schema = build_service_jsonld(
        service_id=listing.get("service_id", ""),
        name=listing.get("service_name", service_data["name"]),
        description=listing.get("description", service_data["description"]),
        provider_name=service_data.get("provider_name", ""),
        provider_agent_id=listing.get("agent_id", ""),
        category=listing.get("category", ""),
        pricing_tiers=service_data.get("pricing_tiers", []),
        sla=listing.get("sla", {}),
        rating=listing.get("rating"),
        supported_protocols=listing.get("protocols", []),
    )

    return registration, schema


# Usage
reg_result, jsonld = register_and_generate_schema(client, {
    "provider_agent_id": "agent-dataenrich-prod",
    "provider_name": "DataEnrich Inc.",
    "name": "DataEnrich Pro",
    "description": "Real-time company data enrichment API",
    "category": "data-enrichment",
    "tags": ["enrichment", "company-data", "real-time"],
    "pricing": {"model": "pay_per_call", "base_price": "0.005", "currency": "USD"},
    "pricing_tiers": [
        {"name": "Starter", "cost_per_call": "0.005", "monthly_cap": "100.00"},
    ],
    "sla": {"uptime_guarantee": 99.95, "latency_p99_ms": 200, "support_response_hours": 4},
    "protocols": ["ucp", "mcp", "a2a"],
})
```

### Validation Script

Structured data is only useful if it is valid. Agents that encounter malformed JSON-LD will skip your listing. This validation script catches the most common errors before they reach production:

```python
def validate_service_jsonld(schema: dict) -> list[str]:
    """Validate a service JSON-LD document against common agent requirements.

    Returns a list of validation errors (empty = valid).
    """
    errors = []

    # Required fields
    if schema.get("@context") != "https://schema.org":
        errors.append("Missing or incorrect @context (must be https://schema.org)")

    if schema.get("@type") != "Service":
        errors.append(f"@type must be 'Service', got '{schema.get('@type')}'")

    if not schema.get("name"):
        errors.append("Missing 'name' field")

    if not schema.get("description"):
        errors.append("Missing 'description' field")
    elif len(schema["description"]) < 50:
        errors.append(f"Description too short ({len(schema['description'])} chars). "
                      "Agents need at least 50 chars for semantic matching.")

    # Pricing validation
    offers = schema.get("offers", [])
    if not offers:
        errors.append("No offers (pricing tiers). Agents cannot evaluate cost.")

    for i, offer in enumerate(offers):
        if offer.get("@type") != "Offer":
            errors.append(f"Offer {i}: @type must be 'Offer'")

        price = offer.get("price")
        if price is None:
            errors.append(f"Offer {i}: missing price")
        elif isinstance(price, float):
            errors.append(f"Offer {i}: price should be string, not float "
                         "(floating-point precision issues)")

        if not offer.get("priceCurrency"):
            errors.append(f"Offer {i}: missing priceCurrency")

    # Provider validation
    provider = schema.get("provider", {})
    if not provider.get("identifier"):
        errors.append("Provider missing 'identifier' (agent_id)")

    # SLA properties
    props = schema.get("additionalProperty", [])
    prop_names = {p.get("name") for p in props}
    recommended = {"uptimeGuarantee", "latencyP99", "supportedProtocols"}
    missing = recommended - prop_names
    if missing:
        errors.append(f"Missing recommended properties: {', '.join(missing)}")

    return errors


# Validate our generated schema
errors = validate_service_jsonld(service_schema)
if errors:
    print("Validation errors:")
    for err in errors:
        print(f"  - {err}")
else:
    print("Schema is valid for agent consumption")
```

### Embedding Structured Data in HTML

For services that also have human-readable web pages, embed the JSON-LD in a `<script>` tag. This allows both web crawlers and AI agents to parse your structured data:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "DataEnrich Pro",
  "description": "Real-time company data enrichment with 95% match rate...",
  "offers": [
    {
      "@type": "Offer",
      "name": "Starter",
      "price": "0.005",
      "priceCurrency": "USD"
    }
  ]
}
</script>
```

> **Key Takeaways**
>
> - Schema.org JSON-LD is the only structured data vocabulary parsed by all major agent platforms.
> - Use `@type: Service` with `Offer` for pricing and `PropertyValue` for SLA terms and protocol support.
> - Always use string-typed prices. Floating-point values cause comparison failures in agent scoring.
> - Auto-generate JSON-LD from GreenHelix `register_service` data to keep marketplace listing and web markup in sync.
> - Validate structured data before deploying. One malformed field can make your entire listing unparseable.
> - See P18 (Pricing & Monetization) for advanced pricing structures including volume discounts and tiered billing.

---

## Chapter 6: Real-Time Catalog Sync & Graph Maintenance

### Why Stale Data Kills Agent Transactions

AI agents do not tolerate stale data. When an agent queries your service listing and finds a price of $0.005 per call, it commits to that price in its transaction planning. If the actual price has changed to $0.008 since the listing was last updated, the agent will encounter a price mismatch at transaction time. Most agents treat price mismatches as a trust violation and blacklist the service. A single stale data incident can remove your service from an agent's candidate set permanently.

The tolerance for staleness varies by data type:

| Data Type | Maximum Acceptable Staleness | Impact of Stale Data |
|---|---|---|
| **Price** | 5 minutes | Transaction failure, trust violation, blacklisting |
| **Availability** | 1 minute | Failed purchases, wasted agent compute cycles |
| **Capability** | 1 hour | Capability mismatch errors, degraded results |
| **SLA terms** | 24 hours | Contractual disputes, expectation mismatches |
| **Trust score** | 1 hour | Incorrect agent ranking, suboptimal selection |

### Webhook-Driven vs. Polling: The Architecture Decision

Two approaches exist for keeping discovery data current: **polling** (agents periodically fetch your data) and **webhooks** (you push updates when data changes). Polling is simpler to implement. Webhooks are superior for freshness.

With polling, the best case is that an agent checks your listing every minute and your data is at most 60 seconds stale. The worst case is that agents poll every hour (common for low-priority services) and your data is 60 minutes stale. You have no control over polling frequency -- it is determined by the agent.

With webhooks, you push updates the moment data changes. Freshness is limited only by network latency -- typically under 500 milliseconds. You control the timing. The tradeoff is implementation complexity: you need to manage subscriber lists, handle delivery failures, and implement retry logic.

The correct answer for agent commerce is both: serve fresh data at your discovery endpoints (for agents that poll) AND push updates via webhooks (for agents that subscribe).

### GreenHelix Events and Webhooks

The GreenHelix gateway provides two tools for real-time updates: `publish_event` for broadcasting state changes, and `register_webhook` for subscribing to events from other services.

```python
import hashlib
import hmac
import time
from typing import Callable


class CatalogSyncManager:
    """Manages real-time synchronization between service catalog,
    knowledge graph, structured data, and discovery endpoints."""

    def __init__(self, discovery_client, webhook_secret: str):
        self.client = discovery_client
        self.webhook_secret = webhook_secret
        self.update_handlers: list[Callable] = []

    def register_update_handler(self, handler: Callable) -> None:
        """Register a callback for catalog updates."""
        self.update_handlers.append(handler)

    def publish_catalog_update(
        self,
        agent_id: str,
        event_type: str,
        service_id: str,
        changes: dict,
    ) -> dict:
        """Publish a catalog change event via GreenHelix."""
        event_data = {
            "service_id": service_id,
            "changes": changes,
            "timestamp": time.time(),
            "version": int(time.time() * 1000),
        }

        # Publish event to GreenHelix event bus
        result = self.client.execute("publish_event", {
            "agent_id": agent_id,
            "event_type": f"catalog.{event_type}",
            "payload": event_data,
        })

        # Run local update handlers
        for handler in self.update_handlers:
            handler(event_type, service_id, changes)

        return result

    def register_for_updates(
        self,
        agent_id: str,
        source_agent_id: str,
        callback_url: str,
        event_types: list[str],
    ) -> dict:
        """Subscribe to catalog updates from another service via webhook."""
        return self.client.execute("register_webhook", {
            "agent_id": agent_id,
            "source_agent_id": source_agent_id,
            "callback_url": callback_url,
            "event_types": event_types,
        })

    def verify_webhook_signature(
        self,
        payload: bytes,
        signature: str,
    ) -> bool:
        """Verify that a webhook payload was sent by GreenHelix."""
        expected = hmac.new(
            self.webhook_secret.encode(),
            payload,
            hashlib.sha256,
        ).hexdigest()
        return hmac.compare_digest(expected, signature)


# Initialize
sync_manager = CatalogSyncManager(client, webhook_secret="your-secret-here")
```

### Event-Driven Pipeline: Updating Graph + Structured Data + Endpoints

When a catalog change occurs -- price update, new capability, SLA revision -- the pipeline must update three systems in sequence: the knowledge graph, the structured data (JSON-LD), and the discovery endpoints.

```python
class DiscoveryPipeline:
    """End-to-end pipeline that updates all discovery surfaces when catalog changes."""

    def __init__(
        self,
        graph: "CommerceKnowledgeGraph",
        sync_manager: CatalogSyncManager,
        discovery_client: "DiscoveryClient",
    ):
        self.graph = graph
        self.sync = sync_manager
        self.client = discovery_client

        # Register handlers for automatic propagation
        self.sync.register_update_handler(self._on_catalog_update)

    def _on_catalog_update(
        self,
        event_type: str,
        service_id: str,
        changes: dict,
    ) -> None:
        """Handle a catalog update by propagating to all discovery surfaces."""
        print(f"Processing {event_type} for {service_id}")

        # Step 1: Update knowledge graph
        if service_id in self.graph.services:
            service = self.graph.services[service_id]
            if "pricing" in changes:
                self._update_pricing(service, changes["pricing"])
            if "sla" in changes:
                self._update_sla(service, changes["sla"])
            if "capabilities" in changes:
                self._update_capabilities(service, changes["capabilities"])
            if "status" in changes:
                service.status = changes["status"]

        # Step 2: Regenerate JSON-LD
        jsonld = self.graph.to_jsonld()
        self._write_jsonld(service_id, jsonld)

        # Step 3: Update marketplace listing
        self._sync_marketplace(service_id)

        print(f"Discovery surfaces updated for {service_id}")

    def _update_pricing(self, service: "ServiceNode", pricing: dict) -> None:
        """Update pricing tiers on a service node."""
        if "tiers" in pricing:
            service.pricing_tiers = [
                PricingTier(
                    tier_name=t["name"],
                    cost_per_call=float(t["cost_per_call"]),
                    currency=t.get("currency", "USD"),
                    monthly_cap=float(t["monthly_cap"]) if "monthly_cap" in t else None,
                )
                for t in pricing["tiers"]
            ]

    def _update_sla(self, service: "ServiceNode", sla_data: dict) -> None:
        """Update SLA terms on a service node."""
        if service.sla:
            for key, value in sla_data.items():
                if hasattr(service.sla, key):
                    setattr(service.sla, key, value)

    def _update_capabilities(self, service: "ServiceNode", caps: list) -> None:
        """Update capability list (triggers MCP manifest regeneration)."""
        service.tags = [c.get("name", "") for c in caps if "name" in c]

    def _write_jsonld(self, service_id: str, jsonld: list[dict]) -> None:
        """Write updated JSON-LD to file (or key-value store in production)."""
        target = next(
            (j for j in jsonld if service_id in j.get("@id", "")),
            None,
        )
        if target:
            with open(f"/var/data/schemas/{service_id}.jsonld", "w") as f:
                json.dump(target, f, indent=2)

    def _sync_marketplace(self, service_id: str) -> None:
        """Push updated data to GreenHelix marketplace."""
        if service_id not in self.graph.services:
            return

        service = self.graph.services[service_id]
        cheapest = min(
            service.pricing_tiers,
            key=lambda t: t.cost_per_call,
        ) if service.pricing_tiers else None

        self.client.execute("update_service", {
            "service_id": service_id,
            "pricing": {
                "model": cheapest.billing_model if cheapest else "contact",
                "base_price": str(cheapest.cost_per_call) if cheapest else "0",
                "currency": cheapest.currency if cheapest else "USD",
            },
            "sla": {
                "uptime_guarantee": service.sla.uptime_guarantee,
                "latency_p99_ms": service.sla.latency_p99_ms,
            } if service.sla else None,
            "status": service.status,
        })


# Wire up the pipeline
pipeline = DiscoveryPipeline(graph, sync_manager, client)

# Example: price change triggers automatic propagation
sync_manager.publish_catalog_update(
    agent_id="agent-dataenrich-prod",
    event_type="pricing_updated",
    service_id="data-enrichment-v2",
    changes={
        "pricing": {
            "tiers": [
                {"name": "starter", "cost_per_call": "0.004", "monthly_cap": "100.00"},
                {"name": "growth", "cost_per_call": "0.0025", "monthly_cap": "500.00"},
            ],
        },
    },
)
```

### Subscribing to External Catalog Updates

When your agent depends on external services, subscribe to their catalog events so your graph stays current:

```python
# Subscribe to pricing updates from a dependency
sync_manager.register_for_updates(
    agent_id="agent-my-service",
    source_agent_id="agent-dataenrich-prod",
    callback_url="https://my-service.example.com/webhooks/catalog",
    event_types=["catalog.pricing_updated", "catalog.status_changed"],
)

# Webhook receiver endpoint (add to your FastAPI app)
@app.post("/webhooks/catalog")
async def receive_catalog_webhook(request: Request):
    """Handle incoming catalog update webhooks from GreenHelix."""
    body = await request.body()
    signature = request.headers.get("X-GreenHelix-Signature", "")

    if not sync_manager.verify_webhook_signature(body, signature):
        return JSONResponse(status_code=401, content={"error": "Invalid signature"})

    payload = json.loads(body)
    event_type = payload.get("event_type", "")
    service_id = payload.get("service_id", "")
    changes = payload.get("changes", {})

    # Update our local graph with the external service's changes
    pipeline._on_catalog_update(event_type, service_id, changes)

    return {"status": "accepted"}
```

> **Key Takeaways**
>
> - Stale pricing data causes transaction failures and agent blacklisting. Maximum acceptable price staleness is 5 minutes.
> - Implement both polling-friendly endpoints (always serve fresh data) and webhook-driven push updates.
> - GreenHelix `publish_event` broadcasts catalog changes. `register_webhook` subscribes to changes from dependencies.
> - Build a pipeline that propagates every catalog change to three surfaces: knowledge graph, JSON-LD, and marketplace listing.
> - Always verify webhook signatures to prevent spoofed updates from corrupting your graph.
> - See P20 (Production Hardening) for webhook retry policies and dead-letter queues.

---

## Chapter 7: Trust Signals & Reputation in Agent Discovery

### Why Agents Rank by Trust, Not Just Price

When an AI agent evaluates ten services that all claim 99.9% uptime and $0.005 per call, it needs a tiebreaker. That tiebreaker is trust. The agent cannot verify marketing claims at query time. It cannot call references. It cannot run a benchmark. What it can do is check cryptographic trust signals: verified metrics submitted through authenticated APIs, Merkle claim chains that prove history has not been tampered with, composite reputation scores computed from transaction history, and escrow completion rates that show how the service behaves under contractual obligations.

Trust-based ranking is not hypothetical. The GreenHelix `best_match` tool uses trust score as a weighted factor in its ranking algorithm alongside price, SLA terms, and capability match. A service with a 0.92 trust score and $0.006 per call will rank above a service with no trust score and $0.004 per call for most agent configurations. The reason is risk-adjusted value: an agent that chooses the cheaper untrusted service has no recourse if the service fails, while the trusted service has verifiable history proving it delivers on its claims.

### The Trust Signal Hierarchy

Not all trust signals carry equal weight. Agents evaluate them in order of cryptographic strength:

| Signal | Source | Forgery Difficulty | Agent Weight |
|---|---|---|---|
| **Merkle claim chain** | `build_claim_chain` | Computationally infeasible | Highest |
| **Verified metrics** | `submit_metrics` | Requires compromised API key | High |
| **Trust score** | `check_trust_score` | Composite -- reflects all signals | High |
| **Agent verification** | `verify_agent` | Requires private key | Medium-High |
| **Escrow completion rate** | Transaction history | Requires real transactions | Medium |
| **Service ratings** | `rate_service` | Sybil-attackable without guards | Lower |

### Surfacing Trust in UCP Profiles

The UCP profile from Chapter 4 included a `trust_score` field. This section shows how to populate it with real data from the GreenHelix trust and reputation systems.

```python
class TrustEnrichedDiscovery:
    """Enriches discovery endpoints with real-time trust signals."""

    def __init__(self, discovery_client):
        self.client = discovery_client

    def get_trust_profile(self, agent_id: str) -> dict:
        """Fetch complete trust profile for an agent."""
        trust_data = {}

        # Get verification status
        try:
            verification = self.client.execute("verify_agent", {
                "agent_id": agent_id,
            })
            trust_data["verified"] = verification.get("verified", False)
            trust_data["verification_method"] = verification.get("method", "unknown")
        except Exception:
            trust_data["verified"] = False

        # Get trust score
        try:
            trust = self.client.execute("check_trust_score", {
                "agent_id": agent_id,
            })
            trust_data["trust_score"] = trust.get("score", 0.0)
            trust_data["trust_factors"] = trust.get("factors", {})
        except Exception:
            trust_data["trust_score"] = 0.0

        # Get reputation metrics
        try:
            reputation = self.client.execute("get_agent_reputation", {
                "agent_id": agent_id,
            })
            trust_data["reputation"] = {
                "trade_count": reputation.get("trade_count", 0),
                "success_rate": reputation.get("success_rate", 0.0),
                "avg_rating": reputation.get("avg_rating", 0.0),
                "active_since": reputation.get("active_since", ""),
            }
        except Exception:
            trust_data["reputation"] = {}

        # Get claim chain depth (tamper-evidence)
        try:
            chains = self.client.execute("get_claim_chains", {
                "agent_id": agent_id,
            })
            chain_list = chains.get("chains", [])
            trust_data["claim_chain"] = {
                "depth": len(chain_list),
                "latest_root_hash": chain_list[0].get("root_hash", "") if chain_list else "",
                "covers_from": chain_list[-1].get("timestamp", "") if chain_list else "",
                "covers_to": chain_list[0].get("timestamp", "") if chain_list else "",
            }
        except Exception:
            trust_data["claim_chain"] = {"depth": 0}

        return trust_data

    def enrich_ucp_profile(self, ucp_profile: dict, agent_id: str) -> dict:
        """Add real-time trust signals to a UCP profile."""
        trust = self.get_trust_profile(agent_id)

        ucp_profile["service"]["provider"]["trust_score"] = trust.get("trust_score", 0.0)
        ucp_profile["service"]["provider"]["verified"] = trust.get("verified", False)
        ucp_profile["service"]["provider"]["verification_method"] = trust.get(
            "verification_method", "none"
        )

        ucp_profile["trust"] = {
            "score": trust.get("trust_score", 0.0),
            "factors": trust.get("trust_factors", {}),
            "reputation": trust.get("reputation", {}),
            "claim_chain": trust.get("claim_chain", {}),
        }

        # Update verification status
        score = trust.get("trust_score", 0.0)
        if score >= 0.9:
            ucp_profile["service"]["provider"]["verification_status"] = "highly_trusted"
        elif score >= 0.7:
            ucp_profile["service"]["provider"]["verification_status"] = "verified"
        elif score >= 0.4:
            ucp_profile["service"]["provider"]["verification_status"] = "partially_verified"
        else:
            ucp_profile["service"]["provider"]["verification_status"] = "unverified"

        return ucp_profile


# Enrich our UCP profile with real trust data
trust_discovery = TrustEnrichedDiscovery(client)
enriched_profile = trust_discovery.enrich_ucp_profile(
    ucp_profile,
    agent_id="agent-dataenrich-prod",
)
print(f"Trust score: {enriched_profile['trust']['score']}")
print(f"Claim chain depth: {enriched_profile['trust']['claim_chain']['depth']}")
```

### Building Your Trust Profile

Trust is not just consumed by agents during discovery -- it must be built over time. Here is the lifecycle for establishing a credible trust profile:

```python
class TrustBuilder:
    """Tools for building a verifiable trust profile on GreenHelix."""

    def __init__(self, discovery_client, agent_id: str):
        self.client = discovery_client
        self.agent_id = agent_id

    def submit_performance_metrics(self, metrics: dict) -> dict:
        """Submit verified performance metrics.

        Call this regularly (daily or after each significant batch).
        Consistent submissions build trust; gaps raise red flags.
        """
        return self.client.execute("submit_metrics", {
            "agent_id": self.agent_id,
            "metrics": metrics,
        })

    def build_claim_chain(self) -> dict:
        """Build a Merkle claim chain over recent metric submissions.

        Call this weekly. The chain creates a tamper-evident history
        that agents can verify independently.
        """
        return self.client.execute("build_claim_chain", {
            "agent_id": self.agent_id,
        })

    def get_trust_improvement_plan(self) -> list[dict]:
        """Analyze current trust profile and recommend improvements."""
        trust = self.client.execute("check_trust_score", {
            "agent_id": self.agent_id,
        })
        score = trust.get("score", 0.0)
        factors = trust.get("factors", {})

        recommendations = []

        if factors.get("metric_submissions", 0) < 30:
            recommendations.append({
                "action": "Submit daily metrics for 30+ days",
                "impact": "high",
                "current": factors.get("metric_submissions", 0),
                "target": 30,
            })

        if factors.get("claim_chain_depth", 0) < 4:
            recommendations.append({
                "action": "Build weekly claim chains for 4+ weeks",
                "impact": "high",
                "current": factors.get("claim_chain_depth", 0),
                "target": 4,
            })

        if factors.get("trade_count", 0) < 50:
            recommendations.append({
                "action": "Complete 50+ successful transactions",
                "impact": "medium",
                "current": factors.get("trade_count", 0),
                "target": 50,
            })

        if factors.get("escrow_completion_rate", 0) < 0.95:
            recommendations.append({
                "action": "Improve escrow completion rate above 95%",
                "impact": "high",
                "current": factors.get("escrow_completion_rate", 0),
                "target": 0.95,
            })

        return recommendations


# Build trust over time
builder = TrustBuilder(client, "agent-dataenrich-prod")

# Submit today's metrics
builder.submit_performance_metrics({
    "uptime_pct": 99.97,
    "latency_p99_ms": 187,
    "requests_processed": 45230,
    "error_rate": 0.0003,
    "match_rate": 0.952,
})

# Weekly: build claim chain
chain_result = builder.build_claim_chain()
print(f"Claim chain built: {chain_result.get('root_hash', '')[:16]}...")

# Check what to improve
plan = builder.get_trust_improvement_plan()
for rec in plan:
    print(f"[{rec['impact'].upper()}] {rec['action']} "
          f"(current: {rec['current']}, target: {rec['target']})")
```

### Trust in JSON-LD Structured Data

Extend your Schema.org JSON-LD to include trust signals so agents parsing your web-embedded structured data also get trust information:

```python
def add_trust_to_jsonld(jsonld: dict, trust_profile: dict) -> dict:
    """Add trust signals to a Schema.org JSON-LD service document."""
    props = jsonld.setdefault("additionalProperty", [])

    props.append({
        "@type": "PropertyValue",
        "name": "trustScore",
        "value": trust_profile.get("trust_score", 0.0),
        "description": "GreenHelix composite trust score (0-1)",
    })

    props.append({
        "@type": "PropertyValue",
        "name": "claimChainDepth",
        "value": trust_profile.get("claim_chain", {}).get("depth", 0),
        "description": "Merkle claim chain depth (tamper-evidence)",
    })

    if trust_profile.get("reputation", {}).get("trade_count", 0) > 0:
        props.append({
            "@type": "PropertyValue",
            "name": "verifiedTradeCount",
            "value": trust_profile["reputation"]["trade_count"],
            "description": "Number of completed escrow-verified transactions",
        })

    if trust_profile.get("verified"):
        props.append({
            "@type": "PropertyValue",
            "name": "identityVerified",
            "value": True,
            "description": "Ed25519 cryptographic identity verification",
        })

    return jsonld


# Add trust to our JSON-LD
trust_profile = trust_discovery.get_trust_profile("agent-dataenrich-prod")
enriched_jsonld = add_trust_to_jsonld(service_schema, trust_profile)
```

> **Key Takeaways**
>
> - Agents rank by trust-adjusted value, not raw price. A trusted service at a higher price beats an untrusted service at a lower price.
> - Trust signals have a hierarchy: Merkle claim chains (strongest) > verified metrics > trust score > agent verification > ratings (weakest).
> - Enrich UCP profiles with real-time trust data from `check_trust_score`, `verify_agent`, `get_agent_reputation`, and `get_claim_chains`.
> - Build trust over time: submit daily metrics, build weekly claim chains, complete escrow transactions, maintain high completion rates.
> - Embed trust signals in Schema.org JSON-LD so agents that discover you via web crawling also get trust information.
> - See P5 (Trust & Verification) for the complete trust-building playbook and Merkle claim chain deep-dive.

---

## Chapter 8: Measuring Discovery Performance

### The Metrics That Matter

Discovery is not a binary state. You are not simply "discoverable" or "not discoverable." Discovery performance exists on a spectrum, and measuring it requires specific metrics that most commerce analytics dashboards do not track. Traditional analytics measure page views, click-through rates, and conversion funnels designed for human visitors. Agent discovery requires a different set of metrics.

**Discovery Rate** -- The percentage of relevant agent queries that return your service in the results. If agents make 1,000 queries that match your service's capabilities and your service appears in 340 of those result sets, your discovery rate is 34%. This is the top-of-funnel metric for agent commerce.

**Agent Conversion Rate** -- The percentage of discovered services that proceed to a transaction. If your service appears in 340 query results and 68 of those result in a completed transaction, your agent conversion rate is 20%. This measures how compelling your listing is once found.

**Time-to-Transaction** -- The elapsed time from an agent's first discovery query to transaction completion. Shorter is better. Long times indicate friction in your protocol endpoints, slow API responses, or missing structured data that forces agents to make additional queries.

**Ranking Position** -- Where your service appears in search results. Position 1-3 captures the vast majority of agent transactions. Position 10+ is functionally invisible because most agents evaluate only the top results.

**Trust-Adjusted Rank** -- Your ranking position after trust score weighting. A service with strong capabilities but weak trust will rank lower than a service with strong trust. This metric tells you whether trust is helping or hurting your discoverability.

### GreenHelix Analytics

The GreenHelix gateway provides analytics tools that measure these metrics directly:

```python
class DiscoveryAnalytics:
    """Track and analyze agent discovery performance."""

    def __init__(self, discovery_client, agent_id: str):
        self.client = discovery_client
        self.agent_id = agent_id

    def get_discovery_metrics(self, period: str = "30d") -> dict:
        """Fetch discovery performance metrics from GreenHelix."""
        usage = self.client.execute("get_usage_analytics", {
            "agent_id": self.agent_id,
            "period": period,
            "metrics": [
                "search_appearances",
                "search_impressions",
                "best_match_wins",
                "api_calls",
                "transactions_completed",
                "transaction_value",
            ],
        })

        revenue = self.client.execute("get_revenue_metrics", {
            "agent_id": self.agent_id,
            "period": period,
        })

        # Calculate derived metrics
        appearances = usage.get("search_appearances", 0)
        transactions = usage.get("transactions_completed", 0)
        best_match_wins = usage.get("best_match_wins", 0)

        return {
            "period": period,
            "raw_metrics": usage,
            "revenue": revenue,
            "derived": {
                "discovery_rate": (
                    appearances / usage.get("search_impressions", 1)
                    if usage.get("search_impressions", 0) > 0
                    else 0.0
                ),
                "conversion_rate": (
                    transactions / appearances
                    if appearances > 0
                    else 0.0
                ),
                "best_match_rate": (
                    best_match_wins / appearances
                    if appearances > 0
                    else 0.0
                ),
                "avg_transaction_value": (
                    usage.get("transaction_value", 0) / transactions
                    if transactions > 0
                    else 0.0
                ),
                "revenue_per_impression": (
                    revenue.get("total_revenue", 0) / usage.get("search_impressions", 1)
                    if usage.get("search_impressions", 0) > 0
                    else 0.0
                ),
            },
        }

    def compare_periods(self, current: str = "7d", previous: str = "7d") -> dict:
        """Compare discovery metrics between two periods."""
        current_metrics = self.get_discovery_metrics(current)
        previous_metrics = self.get_discovery_metrics(previous)

        comparison = {}
        for key in current_metrics["derived"]:
            curr_val = current_metrics["derived"][key]
            prev_val = previous_metrics["derived"].get(key, 0)
            if prev_val > 0:
                change_pct = ((curr_val - prev_val) / prev_val) * 100
            else:
                change_pct = 100.0 if curr_val > 0 else 0.0
            comparison[key] = {
                "current": curr_val,
                "previous": prev_val,
                "change_pct": round(change_pct, 2),
            }

        return comparison

    def discovery_health_check(self) -> list[dict]:
        """Run a comprehensive discovery health check.

        Returns a list of checks with pass/fail/warn status.
        """
        checks = []

        # Check 1: UCP endpoint responds
        try:
            # Simulate by verifying our service is registered
            service = self.client.execute("get_service", {
                "agent_id": self.agent_id,
            })
            checks.append({
                "check": "marketplace_listing",
                "status": "pass" if service else "fail",
                "detail": "Service is registered on GreenHelix marketplace",
            })
        except Exception as e:
            checks.append({
                "check": "marketplace_listing",
                "status": "fail",
                "detail": f"Service not found: {e}",
            })

        # Check 2: Trust score above threshold
        try:
            trust = self.client.execute("check_trust_score", {
                "agent_id": self.agent_id,
            })
            score = trust.get("score", 0.0)
            checks.append({
                "check": "trust_score",
                "status": "pass" if score >= 0.7 else "warn" if score >= 0.4 else "fail",
                "detail": f"Trust score: {score} (threshold: 0.7)",
                "value": score,
            })
        except Exception:
            checks.append({
                "check": "trust_score",
                "status": "fail",
                "detail": "Unable to fetch trust score",
            })

        # Check 3: Recent metrics submissions
        try:
            claims = self.client.execute("get_verified_claims", {
                "agent_id": self.agent_id,
            })
            claim_count = len(claims.get("claims", []))
            checks.append({
                "check": "metric_submissions",
                "status": "pass" if claim_count >= 7 else "warn" if claim_count >= 1 else "fail",
                "detail": f"{claim_count} verified claims (target: 7+ for weekly)",
                "value": claim_count,
            })
        except Exception:
            checks.append({
                "check": "metric_submissions",
                "status": "fail",
                "detail": "Unable to fetch verified claims",
            })

        # Check 4: Claim chain exists
        try:
            chains = self.client.execute("get_claim_chains", {
                "agent_id": self.agent_id,
            })
            depth = len(chains.get("chains", []))
            checks.append({
                "check": "claim_chain",
                "status": "pass" if depth >= 4 else "warn" if depth >= 1 else "fail",
                "detail": f"Claim chain depth: {depth} (target: 4+ for monthly)",
                "value": depth,
            })
        except Exception:
            checks.append({
                "check": "claim_chain",
                "status": "warn",
                "detail": "Unable to fetch claim chains",
            })

        # Check 5: Search visibility
        metrics = self.get_discovery_metrics("7d")
        dr = metrics["derived"]["discovery_rate"]
        checks.append({
            "check": "discovery_rate",
            "status": "pass" if dr >= 0.3 else "warn" if dr >= 0.1 else "fail",
            "detail": f"Discovery rate: {dr:.1%} (target: 30%+)",
            "value": dr,
        })

        # Check 6: Conversion
        cr = metrics["derived"]["conversion_rate"]
        checks.append({
            "check": "conversion_rate",
            "status": "pass" if cr >= 0.15 else "warn" if cr >= 0.05 else "fail",
            "detail": f"Conversion rate: {cr:.1%} (target: 15%+)",
            "value": cr,
        })

        return checks


# Run discovery analytics
analytics = DiscoveryAnalytics(client, "agent-dataenrich-prod")

# Get current metrics
metrics = analytics.get_discovery_metrics("30d")
print(f"Discovery rate: {metrics['derived']['discovery_rate']:.1%}")
print(f"Conversion rate: {metrics['derived']['conversion_rate']:.1%}")
print(f"Best match rate: {metrics['derived']['best_match_rate']:.1%}")
print(f"Revenue per impression: ${metrics['derived']['revenue_per_impression']:.4f}")

# Week-over-week comparison
comparison = analytics.compare_periods("7d", "7d")
for metric, data in comparison.items():
    direction = "up" if data["change_pct"] > 0 else "down"
    print(f"{metric}: {data['current']:.4f} ({direction} {abs(data['change_pct'])}%)")

# Health check
health = analytics.discovery_health_check()
for check in health:
    icon = {"pass": "OK", "warn": "WARN", "fail": "FAIL"}[check["status"]]
    print(f"[{icon}] {check['check']}: {check['detail']}")
```

### A/B Testing Structured Data

Different structured data configurations produce different discovery outcomes. A/B testing lets you determine which configuration maximizes your metrics. The approach is straightforward: run two versions of your structured data simultaneously (served to different agent cohorts) and compare performance.

```python
class StructuredDataExperiment:
    """A/B test different structured data configurations."""

    def __init__(self, discovery_client, agent_id: str):
        self.client = discovery_client
        self.agent_id = agent_id

    def run_experiment(
        self,
        variant_a: dict,
        variant_b: dict,
        description: str,
        duration_days: int = 14,
    ) -> dict:
        """Set up an A/B test between two structured data configurations.

        In practice, you would deploy both variants and route traffic
        based on a hash of the requesting agent's ID. This method
        registers both variants and returns the experiment config.
        """
        experiment = {
            "experiment_id": f"exp_{int(time.time())}",
            "description": description,
            "duration_days": duration_days,
            "variant_a": {
                "config": variant_a,
                "label": "control",
            },
            "variant_b": {
                "config": variant_b,
                "label": "treatment",
            },
        }

        # Publish experiment start event for tracking
        self.client.execute("publish_event", {
            "agent_id": self.agent_id,
            "event_type": "experiment.started",
            "payload": {
                "experiment_id": experiment["experiment_id"],
                "description": description,
                "variants": ["a", "b"],
            },
        })

        return experiment

    def analyze_results(
        self,
        experiment_id: str,
        variant_a_metrics: dict,
        variant_b_metrics: dict,
    ) -> dict:
        """Compare two variants and declare a winner."""
        results = {}
        for metric in ["discovery_rate", "conversion_rate", "revenue_per_impression"]:
            a_val = variant_a_metrics.get(metric, 0)
            b_val = variant_b_metrics.get(metric, 0)
            lift = ((b_val - a_val) / a_val * 100) if a_val > 0 else 0

            results[metric] = {
                "variant_a": a_val,
                "variant_b": b_val,
                "lift_pct": round(lift, 2),
                "winner": "b" if b_val > a_val else "a" if a_val > b_val else "tie",
            }

        return results


# Example: test whether detailed SLA properties improve discovery
experiment = StructuredDataExperiment(client, "agent-dataenrich-prod")
exp = experiment.run_experiment(
    variant_a={
        "sla_properties": ["uptimeGuarantee"],  # Minimal SLA info
    },
    variant_b={
        "sla_properties": [  # Full SLA info
            "uptimeGuarantee", "latencyP99",
            "supportResponseTime", "dataRetentionDays",
        ],
    },
    description="Test whether detailed SLA properties improve agent discovery rate",
    duration_days=14,
)
print(f"Experiment started: {exp['experiment_id']}")
```

### Discovery Dashboard

Combine all metrics into a single dashboard view:

```python
def print_discovery_dashboard(analytics: DiscoveryAnalytics) -> None:
    """Print a comprehensive discovery performance dashboard."""
    metrics = analytics.get_discovery_metrics("30d")
    health = analytics.discovery_health_check()
    comparison = analytics.compare_periods("7d", "7d")

    print("=" * 60)
    print("DISCOVERY PERFORMANCE DASHBOARD")
    print("=" * 60)

    print("\n--- 30-Day Metrics ---")
    d = metrics["derived"]
    print(f"Discovery Rate:          {d['discovery_rate']:.1%}")
    print(f"Conversion Rate:         {d['conversion_rate']:.1%}")
    print(f"Best Match Win Rate:     {d['best_match_rate']:.1%}")
    print(f"Avg Transaction Value:   ${d['avg_transaction_value']:.4f}")
    print(f"Revenue per Impression:  ${d['revenue_per_impression']:.6f}")

    print("\n--- Week-over-Week Changes ---")
    for metric, data in comparison.items():
        arrow = "+" if data["change_pct"] > 0 else ""
        print(f"{metric:30s} {arrow}{data['change_pct']}%")

    print("\n--- Health Checks ---")
    for check in health:
        status_label = {"pass": "PASS", "warn": "WARN", "fail": "FAIL"}[check["status"]]
        print(f"[{status_label:4s}] {check['check']:25s} {check['detail']}")

    print("\n" + "=" * 60)


# Run the dashboard
print_discovery_dashboard(analytics)
```

### Debugging Checklist

When discovery metrics are underperforming, work through this checklist in order:

| # | Check | Tool / Method | Expected Result | Common Fix |
|---|---|---|---|---|
| 1 | Is service registered? | `get_service` | Returns service data | Run `register_service` |
| 2 | Does `search_services` find you? | `search_services` with your category | Service in results | Improve description keywords |
| 3 | Does `best_match` select you? | `best_match` with specific requirements | Your service returned | Improve trust score, lower price, add capabilities |
| 4 | Is UCP endpoint live? | `GET /.well-known/ucp` | 200 with valid JSON | Deploy endpoint (Chapter 4) |
| 5 | Is A2A card live? | `GET /.well-known/agent.json` | 200 with valid JSON | Deploy agent card (Chapter 4) |
| 6 | Is MCP manifest live? | `GET /mcp/tools` | 200 with tools array | Deploy MCP manifest (Chapter 4) |
| 7 | Is JSON-LD valid? | `validate_service_jsonld()` | No errors | Fix validation errors (Chapter 5) |
| 8 | Is pricing current? | Compare listing vs actual price | Match | Trigger catalog sync (Chapter 6) |
| 9 | Is trust score adequate? | `check_trust_score` | >= 0.7 | Submit metrics, build claim chains (Chapter 7) |
| 10 | Are webhook events flowing? | `publish_event` + check subscriber count | Events published | Register webhooks (Chapter 6) |

If all ten checks pass and discovery rate is still below 30%, the issue is competitive: other services in your category have stronger listings. Improve your `description_for_model` with more specific keywords, add capabilities, lower pricing, or increase trust score through consistent metric submissions and claim chain building.

> **Key Takeaways**
>
> - Five metrics define discovery performance: discovery rate, agent conversion rate, time-to-transaction, ranking position, and trust-adjusted rank.
> - GreenHelix `get_usage_analytics` and `get_revenue_metrics` provide the raw data. Derive discovery rate and conversion rate from search appearances and completed transactions.
> - A/B test structured data configurations to find the optimal attribute set. More SLA detail often improves discovery rate.
> - Run weekly health checks. A single failing check (expired trust, stale pricing, missing endpoint) can collapse discovery metrics.
> - The 10-point debugging checklist covers the full discovery stack from registration to trust to endpoint availability.
> - See P21 (Agent-Ready Commerce) Chapter 7 for the complete agent discoverability test harness.

---

## Conclusion: The Discovery Flywheel

Discovery in agent commerce is not a one-time setup task. It is a flywheel with four stages:

1. **Build** -- Knowledge graph, structured data, protocol endpoints (Chapters 2-5)
2. **Publish** -- Register on marketplace, push events, keep data fresh (Chapter 6)
3. **Trust** -- Submit metrics, build claim chains, maintain reputation (Chapter 7)
4. **Measure** -- Track discovery rate, conversion, ranking. Feed improvements back into Build (Chapter 8)

Each rotation through the flywheel makes the next one more effective. A service with six months of consistent metric submissions, deep claim chains, hundreds of completed transactions, and optimized structured data will compound its discovery advantage over competitors who started later or maintain their listings less diligently.

The 805% year-over-year growth in AI-referred traffic is not slowing down. The services that invest in discovery infrastructure today will capture a disproportionate share of that traffic tomorrow. The services that do not will join the 40% that agents cannot see.

Start with Chapter 2. Build your graph. Implement UCP. Submit your first metrics. The flywheel starts with a single rotation.

---

*This guide uses the GreenHelix A2A Commerce Gateway (128 tools, `https://api.greenhelix.net/v1`). For related topics, see: P21 (Agent-Ready Commerce) for agent-ready storefronts, P18 (Pricing & Monetization) for advanced pricing structures, P5 (Trust & Verification) for the complete trust-building playbook, and P20 (Production Hardening) for deploying discovery infrastructure at scale.*

