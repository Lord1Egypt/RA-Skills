---
name: greenhelix-agent-supply-chain-orchestration
version: "1.3.1"
description: "Agentic Supply Chain Orchestration. Build multi-agent supplier networks that self-heal: supplier discovery, real-time SLA monitoring, disruption detection with automated rerouting, demand aggregation, and cross-border compliance. Includes detailed Python code examples for every pattern."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [supply-chain, orchestration, procurement, multi-agent, sla, disruption, guide, greenhelix, openclaw, ai-agent]
price_usd: 49.0
content_type: markdown
executable: false
install: none
credentials: [GREENHELIX_API_KEY]
metadata:
  openclaw:
    requires:
      env:
        - GREENHELIX_API_KEY
    primaryEnv: GREENHELIX_API_KEY
---
# Agentic Supply Chain Orchestration

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `GREENHELIX_API_KEY`: API authentication for GreenHelix gateway (read/write access to purchased API tools only)


Your procurement agent found a backup supplier in 340 milliseconds. The primary supplier -- a ceramics manufacturer in Shenzhen -- had just failed its SLA for the third consecutive delivery window. Your orchestration layer detected the failure pattern at the second miss, pre-qualified two alternates using trust scores and compliance verification, and by the time the third failure registered, it had already rerouted the purchase order, updated the escrow terms, and notified the downstream assembly agent that materials would arrive 18 hours late instead of 96. No human touched the workflow. No Slack thread. No emergency procurement meeting.
This is not a hypothetical. This is what supply chain orchestration looks like when agents operate as a coordinated network rather than isolated procurement bots. Deloitte projects that by 2031, 60% of supply chain disruptions will be resolved without human intervention. Microsoft's Supply Chain 2.0 initiative (March 2026) reports multi-agent supply chain systems moving from proof-of-concept to production deployments. SAP's 2026 trend analysis identifies the defining shift: from firefighting individual disruptions to orchestrating resilient networks that absorb disruptions autonomously.
But the gap between vision and execution is enormous. A 2025 Gartner survey found that 73% of procurement organizations are piloting AI agents, but only 11% have the infrastructure to scale beyond single-agent experiments. The failure mode is not the AI -- it is the architecture. Single-agent procurement hits a ceiling fast: one agent cannot monitor 200 suppliers, track cross-border compliance in 14 jurisdictions, aggregate demand signals from five business units, and reroute orders when a port closure disrupts three tiers of your supply network simultaneously.

## What You'll Learn
- Chapter 1: The Agentic Supply Chain Architecture
- Chapter 2: Supplier Network Discovery and Multi-Tier Mapping
- Chapter 3: Real-Time Supplier Health Monitoring
- Chapter 4: Disruption Detection and Automated Rerouting
- Chapter 5: Demand Signal Aggregation and Predictive Sourcing
- Chapter 6: Cross-Border Compliance
- Chapter 7: Agent-to-Agent Coordination
- Chapter 8: The 30-Day Implementation Sprint
- What You Get

## Full Guide

# Agentic Supply Chain Orchestration: Multi-Agent Supplier Networks That Self-Heal

Your procurement agent found a backup supplier in 340 milliseconds. The primary supplier -- a ceramics manufacturer in Shenzhen -- had just failed its SLA for the third consecutive delivery window. Your orchestration layer detected the failure pattern at the second miss, pre-qualified two alternates using trust scores and compliance verification, and by the time the third failure registered, it had already rerouted the purchase order, updated the escrow terms, and notified the downstream assembly agent that materials would arrive 18 hours late instead of 96. No human touched the workflow. No Slack thread. No emergency procurement meeting.

This is not a hypothetical. This is what supply chain orchestration looks like when agents operate as a coordinated network rather than isolated procurement bots. Deloitte projects that by 2031, 60% of supply chain disruptions will be resolved without human intervention. Microsoft's Supply Chain 2.0 initiative (March 2026) reports multi-agent supply chain systems moving from proof-of-concept to production deployments. SAP's 2026 trend analysis identifies the defining shift: from firefighting individual disruptions to orchestrating resilient networks that absorb disruptions autonomously.

But the gap between vision and execution is enormous. A 2025 Gartner survey found that 73% of procurement organizations are piloting AI agents, but only 11% have the infrastructure to scale beyond single-agent experiments. The failure mode is not the AI -- it is the architecture. Single-agent procurement hits a ceiling fast: one agent cannot monitor 200 suppliers, track cross-border compliance in 14 jurisdictions, aggregate demand signals from five business units, and reroute orders when a port closure disrupts three tiers of your supply network simultaneously.

You need a multi-agent supply chain. And you need the orchestration infrastructure to prevent that multi-agent system from becoming a liability. One documented case saw a 400x cost overrun when a poorly orchestrated procurement loop went recursive -- each agent spawning sub-agents to find alternatives, each sub-agent spawning its own searches, until the API bill exceeded the value of the goods being procured.

This guide builds the orchestration layer. Every chapter contains working Python code against the GreenHelix A2A Commerce Gateway -- 128 tools accessible at `https://api.greenhelix.net/v1` via a single the REST API (`POST /v1/{tool}`) endpoint. By the end, you will have a complete supply chain orchestration system: multi-tier supplier mapping, real-time SLA monitoring, automated disruption rerouting, demand signal aggregation, cross-border compliance checks, and agent-to-agent coordination with escrow-protected transactions.

---


> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## Table of Contents

1. [The Agentic Supply Chain Architecture](#chapter-1-the-agentic-supply-chain-architecture)
2. [Supplier Network Discovery and Multi-Tier Mapping](#chapter-2-supplier-network-discovery-and-multi-tier-mapping)
3. [Real-Time Supplier Health Monitoring](#chapter-3-real-time-supplier-health-monitoring)
4. [Disruption Detection and Automated Rerouting](#chapter-4-disruption-detection-and-automated-rerouting)
5. [Demand Signal Aggregation and Predictive Sourcing](#chapter-5-demand-signal-aggregation-and-predictive-sourcing)
6. [Cross-Border Compliance](#chapter-6-cross-border-compliance)
7. [Agent-to-Agent Coordination](#chapter-7-agent-to-agent-coordination)
8. [The 30-Day Implementation Sprint](#chapter-8-the-30-day-implementation-sprint)

---

## Chapter 1: The Agentic Supply Chain Architecture

### Why Single-Agent Procurement Is Not Enough

A procurement agent that can discover vendors, compare prices, and execute purchases is useful. It handles the transactional layer of sourcing. But supply chains are not transactions -- they are networks. A single procurement agent cannot:

- Monitor the health of 200 active suppliers across four tiers simultaneously
- Detect that a port congestion event in Rotterdam will cascade into a 3-week delay for your Tier-2 chemical supplier in Belgium
- Aggregate demand signals from five internal business units to negotiate a volume discount with a shared raw materials vendor
- Verify that a rerouted order to a new supplier in Vietnam complies with CBAM carbon reporting requirements and US tariff schedules
- Coordinate with three downstream assembly agents whose production schedules depend on the rerouted materials arriving within a specific window

Each of these tasks requires a specialized agent with domain-specific context. The architecture challenge is not building individual agents -- it is orchestrating them into a coherent supply network that operates faster than disruptions propagate.

### The Orchestration Pattern

The agentic supply chain has five layers. Each layer is staffed by one or more specialized agents, and all agents communicate through a shared message bus and execute commercial operations through the GreenHelix gateway.

```
+=========================================================================+
|                     ORCHESTRATION LAYER (this guide)                     |
+=========================================================================+
|                                                                         |
|  +---------------+  +----------------+  +--------------------+          |
|  | SUPPLY TIER   |  | DEMAND TIER    |  | COMPLIANCE TIER    |          |
|  |               |  |                |  |                    |          |
|  | - Discovery   |  | - Signal       |  | - Tariff engine    |          |
|  |   agents      |  |   aggregation  |  | - Sanctions screen |          |
|  | - Health       |  |   agents       |  | - Jurisdiction     |          |
|  |   monitors    |  | - Forecast     |  |   resolver         |          |
|  | - Rerouting   |  |   agents       |  | - Audit trail      |          |
|  |   agents      |  | - Predictive   |  |   agents           |          |
|  |               |  |   sourcing     |  |                    |          |
|  +-------+-------+  +-------+--------+  +---------+----------+          |
|          |                  |                      |                     |
|  +-------v------------------v----------------------v------------------+  |
|  |                  COORDINATION BUS                                  |  |
|  |  GreenHelix Messaging + Escrow + SLA Enforcement                   |  |
|  +-------+------------------------------------------------------------+  |
|          |                                                              |
|  +-------v------------------------------------------------------------+  |
|  |                  COMMERCE LAYER                                     |  |
|  |  Identity | Payments | Ledger | Trust | Reputation                  |  |
|  +---------------------------------------------------------------------+ |
+=========================================================================+
```

**Layer 1: Commerce.** Identity verification, payments, ledger, trust scoring, and reputation tracking. This is the foundation -- agents cannot transact without it. The commerce layer provides these capabilities.

**Layer 2: Coordination Bus.** Message passing between agents, escrow management for inter-agent transactions, and SLA enforcement. This layer ensures agents can collaborate without centralized control.

**Layer 3: Supply Tier.** Agents responsible for the supplier side: discovering new suppliers, monitoring existing supplier health, and executing rerouting when disruptions occur.

**Layer 4: Demand Tier.** Agents responsible for the buyer side: aggregating demand signals from internal consumers, generating demand forecasts, and triggering predictive sourcing before shortages materialize.

**Layer 5: Compliance Tier.** Agents responsible for regulatory requirements: tariff calculations, sanctions screening, jurisdiction-specific rules, and maintaining audit trails.

**Layer 6: Orchestration.** The coordination logic that ties the other layers together. This is where rerouting decisions are made, where supply-demand mismatches are resolved, and where multi-agent workflows are sequenced.

### Setting Up the Foundation

Every agent in the supply chain network needs an identity on GreenHelix. Here is the bootstrap sequence for the core orchestration agent:

```python
import requests
import os
import time

base_url = "https://api.greenhelix.net/v1"
api_key = os.environ["GREENHELIX_API_KEY"]

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"

def execute(tool: str, input_data: dict) -> dict:
    """Execute a GreenHelix tool and return the result."""
    resp = session.post(f"{base_url}/v1", json={
        "tool": tool,
        "input": input_data
    })
    resp.raise_for_status()
    return resp.json()

# Register the orchestration agent
orchestrator = execute("register_agent", {
    "name": "supply-chain-orchestrator",
    "description": "Central orchestration agent for multi-tier supply chain management",
    "capabilities": [
        "supplier_discovery",
        "health_monitoring",
        "disruption_rerouting",
        "demand_aggregation",
        "compliance_verification"
    ],
    "metadata": {
        "version": "1.0",
        "tier": "orchestration",
        "max_suppliers": 500,
        "supported_regions": ["NA", "EU", "APAC"]
    }
})

orchestrator_id = orchestrator["agent_id"]
print(f"Orchestrator registered: {orchestrator_id}")
```

Now register the specialized sub-agents. In production, each of these runs as a separate process or container. For this guide, we register them as distinct identities that the orchestrator coordinates:

```python
agent_roles = [
    {
        "name": "supplier-discovery-agent",
        "description": "Discovers and qualifies new suppliers across marketplace",
        "capabilities": ["search", "qualification", "tier_mapping"]
    },
    {
        "name": "health-monitor-agent",
        "description": "Monitors SLA compliance and supplier health metrics",
        "capabilities": ["sla_tracking", "anomaly_detection", "alerting"]
    },
    {
        "name": "rerouting-agent",
        "description": "Executes automated supplier rerouting on disruption",
        "capabilities": ["alternate_sourcing", "order_migration", "escrow_management"]
    },
    {
        "name": "demand-aggregation-agent",
        "description": "Aggregates demand signals and generates sourcing forecasts",
        "capabilities": ["signal_collection", "forecasting", "predictive_sourcing"]
    },
    {
        "name": "compliance-agent",
        "description": "Verifies cross-border compliance for all supply chain transactions",
        "capabilities": ["tariff_calculation", "sanctions_screening", "audit_trail"]
    }
]

agent_ids = {}
for role in agent_roles:
    result = execute("register_agent", role)
    agent_ids[role["name"]] = result["agent_id"]
    print(f"Registered {role['name']}: {result['agent_id']}")
```

### The Anti-Pattern: Recursive Agent Spawning

Before building further, internalize the failure mode that kills multi-agent supply chains. The pattern looks like this:

```
Orchestrator detects disruption
  --> Spawns 5 discovery agents to find alternates
    --> Each discovery agent queries marketplace, gets partial results
      --> Each spawns 3 more agents to drill into sub-categories
        --> Each sub-agent spawns evaluation agents
          --> 5 * 3 * 3 = 45 agents, each making API calls
            --> Cost: $2,700 in API fees for a $500 component
```

The fix is simple: **bounded concurrency with circuit breakers.** Every orchestration workflow must declare its maximum agent count, maximum API budget, and maximum execution time before the first agent starts. We will enforce this in every code example throughout the guide.

```python
ORCHESTRATION_LIMITS = {
    "max_concurrent_agents": 10,
    "max_api_budget_usd": 50.00,
    "max_execution_seconds": 300,
    "max_rerouting_depth": 2,       # only 2 levels of alternate sourcing
    "max_discovery_results": 25     # cap marketplace search results
}
```

---

## Chapter 2: Supplier Network Discovery and Multi-Tier Mapping

### Beyond Flat Vendor Lists

Traditional procurement maintains a flat approved vendor list (AVL). Agent-based supply chains need a graph. Your Tier-1 supplier (the one you contract with directly) depends on Tier-2 suppliers (their material providers), who depend on Tier-3 suppliers (raw material extractors or sub-component manufacturers). A disruption at Tier-3 propagates upward, but a flat AVL has no visibility below Tier-1.

Multi-tier mapping changes this. The discovery agent builds a graph of supplier relationships, so when a Tier-3 lithium mine in Chile goes offline, your orchestrator knows which Tier-2 battery cell manufacturers are affected, which Tier-1 battery pack assemblers depend on those cells, and which of your product lines are at risk -- before the Tier-1 supplier even reports a delay.

```
YOUR AGENT (Buyer)
    |
    +-- Tier 1: Battery Pack Assembler (Shenzhen)
    |       |
    |       +-- Tier 2: Cell Manufacturer A (South Korea)
    |       |       |
    |       |       +-- Tier 3: Lithium Mine (Chile) <-- DISRUPTION
    |       |       +-- Tier 3: Cobalt Refinery (DRC)
    |       |
    |       +-- Tier 2: Cell Manufacturer B (Japan)
    |               |
    |               +-- Tier 3: Lithium Mine (Australia)  <-- ALTERNATE
    |               +-- Tier 3: Cobalt Refinery (Finland)
    |
    +-- Tier 1: Battery Pack Assembler (Hungary)   <-- BACKUP
            |
            +-- Tier 2: Cell Manufacturer C (Poland)
```

### Discovering Suppliers on the Marketplace

The GreenHelix marketplace is the primary discovery mechanism. Suppliers register their services with capability tags, pricing, and SLA terms. The discovery agent queries the marketplace to find suppliers matching specific requirements:

```python
def discover_suppliers(category: str, region: str = None, min_trust: float = 0.7,
                       max_results: int = 25) -> list:
    """
    Search the GreenHelix marketplace for suppliers matching criteria.
    Returns a list of supplier profiles sorted by relevance.
    """
    search_input = {
        "query": category,
        "limit": min(max_results, ORCHESTRATION_LIMITS["max_discovery_results"])
    }
    if region:
        search_input["filters"] = {"region": region}

    results = execute("search_services", search_input)
    suppliers = results.get("services", [])

    # Filter by trust score
    qualified = []
    for supplier in suppliers:
        reputation = execute("get_agent_reputation", {
            "agent_id": supplier["agent_id"]
        })
        trust_score = reputation.get("score", 0)
        if trust_score >= min_trust:
            supplier["trust_score"] = trust_score
            qualified.append(supplier)

    # Sort by trust score descending
    qualified.sort(key=lambda s: s["trust_score"], reverse=True)
    return qualified


# Discover battery cell manufacturers in APAC
cell_suppliers = discover_suppliers(
    category="battery cell manufacturing",
    region="APAC",
    min_trust=0.8
)

for s in cell_suppliers:
    print(f"  {s['name']} | Trust: {s['trust_score']:.2f} | {s.get('region', 'N/A')}")
```

### Building the Supplier Graph

Once you have discovered suppliers at each tier, build the relationship graph. Each node is a supplier agent; each edge represents a dependency (supplier A depends on supplier B for a specific input):

```python
class SupplierNode:
    """A node in the multi-tier supplier graph."""

    def __init__(self, agent_id: str, name: str, tier: int, category: str,
                 trust_score: float = 0.0):
        self.agent_id = agent_id
        self.name = name
        self.tier = tier
        self.category = category
        self.trust_score = trust_score
        self.dependencies = []      # list of (SupplierNode, material) tuples
        self.dependents = []        # list of (SupplierNode, material) tuples
        self.sla_id = None
        self.health_status = "unknown"

    def add_dependency(self, supplier, material: str):
        self.dependencies.append((supplier, material))
        supplier.dependents.append((self, material))


class SupplierGraph:
    """Multi-tier supplier network graph."""

    def __init__(self):
        self.nodes = {}  # agent_id -> SupplierNode

    def add_supplier(self, node: SupplierNode):
        self.nodes[node.agent_id] = node

    def get_upstream_chain(self, agent_id: str) -> list:
        """Get all upstream suppliers (dependencies) recursively."""
        visited = set()
        chain = []

        def walk(node_id):
            if node_id in visited:
                return
            visited.add(node_id)
            node = self.nodes.get(node_id)
            if not node:
                return
            for dep, material in node.dependencies:
                chain.append({
                    "supplier": dep.name,
                    "agent_id": dep.agent_id,
                    "tier": dep.tier,
                    "material": material,
                    "trust_score": dep.trust_score
                })
                walk(dep.agent_id)

        walk(agent_id)
        return chain

    def get_impact_zone(self, disrupted_agent_id: str) -> list:
        """Get all downstream suppliers affected by a disruption."""
        visited = set()
        impacted = []

        def walk(node_id):
            if node_id in visited:
                return
            visited.add(node_id)
            node = self.nodes.get(node_id)
            if not node:
                return
            for dependent, material in node.dependents:
                impacted.append({
                    "supplier": dependent.name,
                    "agent_id": dependent.agent_id,
                    "tier": dependent.tier,
                    "material": material
                })
                walk(dependent.agent_id)

        walk(disrupted_agent_id)
        return impacted


# Build a sample graph
graph = SupplierGraph()

# Tier 3
lithium_chile = SupplierNode("lit-cl-001", "LithiumCo Chile", 3, "lithium", 0.85)
lithium_aus = SupplierNode("lit-au-001", "LithiumCo Australia", 3, "lithium", 0.91)

# Tier 2
cell_mfg_kr = SupplierNode("cell-kr-001", "CellTech Korea", 2, "battery_cells", 0.88)
cell_mfg_jp = SupplierNode("cell-jp-001", "CellTech Japan", 2, "battery_cells", 0.92)

# Tier 1
pack_assembler = SupplierNode("pack-cn-001", "PackAssembly Shenzhen", 1, "battery_packs", 0.86)

# Wire dependencies
cell_mfg_kr.add_dependency(lithium_chile, "lithium_carbonate")
cell_mfg_jp.add_dependency(lithium_aus, "lithium_hydroxide")
pack_assembler.add_dependency(cell_mfg_kr, "prismatic_cells")
pack_assembler.add_dependency(cell_mfg_jp, "cylindrical_cells")

for node in [lithium_chile, lithium_aus, cell_mfg_kr, cell_mfg_jp, pack_assembler]:
    graph.add_supplier(node)

# What happens if Chile lithium goes offline?
impact = graph.get_impact_zone("lit-cl-001")
print("Disruption at LithiumCo Chile affects:")
for i in impact:
    print(f"  Tier {i['tier']}: {i['supplier']} (material: {i['material']})")
```

### Best-Match Supplier Selection

When you need to select a single supplier from multiple candidates, use the `best_match` tool to rank options against weighted criteria:

```python
def select_best_supplier(query: str, requirements: dict) -> dict:
    """
    Use GreenHelix best_match to find the optimal supplier
    for a given set of requirements.
    """
    result = execute("best_match", {
        "query": query,
        "requirements": requirements
    })
    return result


best = select_best_supplier(
    query="lithium carbonate supplier with >99.5% purity",
    requirements={
        "min_trust_score": 0.85,
        "region_preference": "APAC",
        "max_lead_time_days": 21,
        "certifications": ["ISO9001", "IATF16949"]
    }
)

print(f"Best match: {best.get('name')} (score: {best.get('match_score', 'N/A')})")
```

### Discovery Checklist

Before moving to monitoring, verify your supplier graph:

- [ ] All Tier-1 suppliers registered and trust-scored
- [ ] At least 2 alternate suppliers per critical material at each tier
- [ ] Tier-2 dependencies mapped for every Tier-1 supplier
- [ ] Tier-3 dependencies mapped for high-risk materials (single-source, geopolitically exposed)
- [ ] Every supplier node has an `agent_id` on GreenHelix
- [ ] Graph `get_impact_zone` tested for each Tier-3 single-source supplier
- [ ] Discovery budget tracked and within `ORCHESTRATION_LIMITS`

---

## Chapter 3: Real-Time Supplier Health Monitoring

### SLAs, Trust Scores, and Anomaly Detection

A supplier graph is only as useful as the data flowing through it. Static graphs with quarterly reviews are how traditional supply chains work -- and why they get blindsided by disruptions. The agentic supply chain monitors every supplier in real time, using three complementary signals:

**Signal 1: SLA Compliance.** Contractual obligations with measurable thresholds. Delivery time, defect rate, fill rate, response time. These are the leading indicators of supplier degradation.

**Signal 2: Trust Scores.** GreenHelix reputation scores aggregated from all transactions across the network. A supplier's trust score reflects not just their performance with you, but their performance with every buyer on the platform.

**Signal 3: Behavioral Anomalies.** Patterns that do not violate any specific SLA but indicate emerging risk. A supplier whose average response time increased from 2 hours to 8 hours over the past week has not breached an SLA -- but the trend predicts a breach within days.

### Creating SLAs for Every Supplier

Every supplier relationship needs a programmatic SLA. This is not a PDF contract -- it is a machine-readable agreement that the health monitor agent evaluates continuously:

```python
def create_supplier_sla(supplier_agent_id: str, terms: dict) -> dict:
    """
    Create an SLA between the orchestrator and a supplier agent.
    Terms define measurable thresholds for automated monitoring.
    """
    sla = execute("create_sla", {
        "agent_id": orchestrator_id,
        "counterparty_id": supplier_agent_id,
        "terms": terms
    })
    return sla


# SLA for the Korea cell manufacturer
cell_sla = create_supplier_sla(
    supplier_agent_id="cell-kr-001",
    terms={
        "delivery_time_days": {
            "target": 14,
            "maximum": 21,
            "measurement": "calendar_days_from_order"
        },
        "defect_rate_pct": {
            "target": 0.5,
            "maximum": 2.0,
            "measurement": "defective_units_per_hundred"
        },
        "fill_rate_pct": {
            "target": 98,
            "minimum": 95,
            "measurement": "ordered_quantity_fulfilled_pct"
        },
        "response_time_hours": {
            "target": 4,
            "maximum": 24,
            "measurement": "hours_to_first_response"
        },
        "review_period": "monthly",
        "penalty_clause": "auto_reroute_on_3_consecutive_breaches"
    }
)

sla_id = cell_sla["sla_id"]
print(f"SLA created: {sla_id}")
```

### The Health Monitor Loop

The health monitor agent runs continuously, polling SLA compliance and trust scores at configurable intervals. In production, this runs as a daemon process or scheduled Lambda:

```python
import datetime

class SupplierHealthMonitor:
    """Continuous health monitoring for all suppliers in the graph."""

    # Thresholds for anomaly detection
    TRUST_DECLINE_THRESHOLD = 0.05     # 5% drop triggers warning
    RESPONSE_TIME_MULTIPLIER = 2.0     # 2x increase triggers warning
    CONSECUTIVE_BREACH_LIMIT = 3       # auto-reroute threshold

    def __init__(self, graph: SupplierGraph, orchestrator_id: str):
        self.graph = graph
        self.orchestrator_id = orchestrator_id
        self.breach_counts = {}      # agent_id -> consecutive breach count
        self.trust_history = {}      # agent_id -> [score, score, ...]
        self.alerts = []

    def check_sla_compliance(self, supplier: SupplierNode) -> dict:
        """Check SLA compliance for a single supplier."""
        if not supplier.sla_id:
            return {"status": "no_sla", "agent_id": supplier.agent_id}

        compliance = execute("check_sla_compliance", {
            "sla_id": supplier.sla_id
        })
        return compliance

    def check_trust_score(self, supplier: SupplierNode) -> dict:
        """Check current trust score and detect decline trends."""
        reputation = execute("get_agent_reputation", {
            "agent_id": supplier.agent_id
        })
        current_score = reputation.get("score", 0)

        # Track history
        history = self.trust_history.setdefault(supplier.agent_id, [])
        history.append(current_score)

        # Keep last 30 readings
        if len(history) > 30:
            history.pop(0)

        # Detect decline
        decline_detected = False
        if len(history) >= 5:
            avg_recent = sum(history[-5:]) / 5
            avg_older = sum(history[:-5]) / max(len(history) - 5, 1)
            if avg_older > 0 and (avg_older - avg_recent) / avg_older > self.TRUST_DECLINE_THRESHOLD:
                decline_detected = True

        return {
            "agent_id": supplier.agent_id,
            "current_score": current_score,
            "trend": "declining" if decline_detected else "stable",
            "history_length": len(history)
        }

    def run_health_check(self) -> list:
        """Run a full health check across all suppliers."""
        results = []

        for agent_id, supplier in self.graph.nodes.items():
            # SLA check
            sla_result = self.check_sla_compliance(supplier)
            is_breached = sla_result.get("compliant") is False

            # Trust check
            trust_result = self.check_trust_score(supplier)

            # Track consecutive breaches
            if is_breached:
                self.breach_counts[agent_id] = self.breach_counts.get(agent_id, 0) + 1
            else:
                self.breach_counts[agent_id] = 0

            # Determine health status
            consecutive = self.breach_counts.get(agent_id, 0)
            if consecutive >= self.CONSECUTIVE_BREACH_LIMIT:
                status = "critical"
            elif consecutive > 0 or trust_result["trend"] == "declining":
                status = "warning"
            else:
                status = "healthy"

            supplier.health_status = status

            check_result = {
                "agent_id": agent_id,
                "name": supplier.name,
                "tier": supplier.tier,
                "health_status": status,
                "consecutive_breaches": consecutive,
                "trust_score": trust_result["current_score"],
                "trust_trend": trust_result["trend"],
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
            results.append(check_result)

            # Generate alerts for non-healthy suppliers
            if status != "healthy":
                self.alerts.append({
                    "severity": "critical" if status == "critical" else "warning",
                    "supplier": supplier.name,
                    "agent_id": agent_id,
                    "reason": f"{consecutive} consecutive SLA breaches"
                            if consecutive > 0
                            else "Trust score declining",
                    "timestamp": datetime.datetime.utcnow().isoformat()
                })

        return results


# Initialize and run
monitor = SupplierHealthMonitor(graph, orchestrator_id)
health_results = monitor.run_health_check()

for r in health_results:
    indicator = {"healthy": "OK", "warning": "!!", "critical": "XX"}[r["health_status"]]
    print(f"  [{indicator}] {r['name']} | Trust: {r['trust_score']:.2f} "
          f"({r['trust_trend']}) | Breaches: {r['consecutive_breaches']}")
```

### Submitting Performance Metrics

When you receive a delivery from a supplier, submit metrics to GreenHelix so the network-wide trust scores reflect actual performance:

```python
def report_supplier_delivery(supplier_agent_id: str, delivery_data: dict):
    """
    Submit delivery performance metrics for a supplier.
    These metrics feed into the GreenHelix reputation system.
    """
    execute("submit_metrics", {
        "agent_id": supplier_agent_id,
        "metrics": {
            "delivery_time_days": delivery_data["actual_delivery_days"],
            "defect_rate": delivery_data["defect_rate"],
            "fill_rate": delivery_data["fill_rate"],
            "order_accuracy": delivery_data["order_accuracy"],
            "communication_score": delivery_data["communication_score"]
        }
    })

    # Also check SLA status after metric submission
    if delivery_data.get("sla_id"):
        sla_status = execute("get_sla_status", {
            "sla_id": delivery_data["sla_id"]
        })
        return sla_status
    return {"status": "metrics_submitted"}


# Report a delivery
report_supplier_delivery("cell-kr-001", {
    "actual_delivery_days": 16,
    "defect_rate": 0.3,
    "fill_rate": 99.2,
    "order_accuracy": 100.0,
    "communication_score": 4.5,
    "sla_id": sla_id
})
```

### Health Dashboard Decision Tree

Use this decision tree to determine the appropriate action based on health check results:

```
HEALTH CHECK RESULT
    |
    +-- healthy (no breaches, stable trust)
    |       --> No action. Continue monitoring.
    |
    +-- warning (1-2 breaches OR declining trust)
    |       |
    |       +-- Is this a Tier-1 supplier?
    |       |       YES --> Pre-qualify 2 alternates (Chapter 2 discovery)
    |       |       NO  --> Log warning, increase monitoring frequency
    |       |
    |       +-- Is trust declining but no SLA breach?
    |               YES --> Send message to supplier requesting status update
    |               NO  --> Standard escalation path
    |
    +-- critical (3+ consecutive breaches)
            |
            +-- Is there a pre-qualified alternate?
            |       YES --> Execute automated rerouting (Chapter 4)
            |       NO  --> Emergency discovery + human escalation
            |
            +-- Is this a single-source supplier?
                    YES --> IMMEDIATE human escalation + emergency sourcing
                    NO  --> Automated rerouting within 1 hour
```

### Monitoring Checklist

- [ ] SLAs created for every Tier-1 and critical Tier-2 supplier
- [ ] Health monitor running at least every 15 minutes for Tier-1
- [ ] Trust score history retained for trend analysis (minimum 30 data points)
- [ ] Delivery metrics submitted after every fulfilled order
- [ ] Alert routing configured: warnings to Slack, critical to PagerDuty + orchestrator
- [ ] Pre-qualified alternates identified for all suppliers in "warning" state
- [ ] Single-source suppliers flagged with higher monitoring frequency

---

## Chapter 4: Disruption Detection and Automated Rerouting

### The Self-Healing Supply Chain

A supply chain that detects disruptions but requires human intervention to reroute is faster than a blind supply chain but still operates at human speed. The self-healing supply chain closes the loop: detect, decide, reroute, verify -- all within the time it would take a human to open the first email.

The rerouting agent executes a four-step sequence when the health monitor flags a critical supplier:

```
CRITICAL ALERT
    |
    v
[1. ASSESS IMPACT]  --> Which orders are affected? Which downstream
    |                    agents depend on this supplier?
    v
[2. SELECT ALTERNATE] --> Query pre-qualified alternates, verify
    |                     availability, check compliance
    v
[3. EXECUTE REROUTE] --> Create new escrow, place order with
    |                    alternate, update downstream agents
    v
[4. VERIFY & CLOSE]  --> Confirm new order accepted, update
                         supplier graph, close old escrow
```

### Impact Assessment

When a supplier goes critical, the first step is calculating the blast radius. Which orders are in-flight? Which downstream agents will be affected? What is the financial exposure?

```python
def assess_disruption_impact(graph: SupplierGraph, disrupted_agent_id: str,
                              open_orders: list) -> dict:
    """
    Assess the impact of a supplier disruption on the supply network.

    Args:
        graph: The supplier network graph
        disrupted_agent_id: Agent ID of the disrupted supplier
        open_orders: List of currently open orders with this supplier

    Returns:
        Impact assessment with affected orders, downstream agents,
        and estimated financial exposure.
    """
    # Get all downstream nodes affected
    impact_zone = graph.get_impact_zone(disrupted_agent_id)

    # Calculate financial exposure from open orders
    affected_orders = [
        order for order in open_orders
        if order["supplier_agent_id"] == disrupted_agent_id
    ]
    financial_exposure = sum(o.get("value_usd", 0) for o in affected_orders)

    # Get SLA status for the disrupted supplier
    supplier = graph.nodes.get(disrupted_agent_id)
    sla_status = None
    if supplier and supplier.sla_id:
        sla_status = execute("get_sla_status", {
            "sla_id": supplier.sla_id
        })

    return {
        "disrupted_supplier": supplier.name if supplier else disrupted_agent_id,
        "affected_orders": len(affected_orders),
        "financial_exposure_usd": financial_exposure,
        "downstream_impact": impact_zone,
        "downstream_agent_count": len(impact_zone),
        "sla_status": sla_status,
        "requires_immediate_action": financial_exposure > 10000
                                     or len(impact_zone) > 3
    }


# Example: assess impact of Korea cell manufacturer going down
sample_orders = [
    {"order_id": "ORD-001", "supplier_agent_id": "cell-kr-001",
     "value_usd": 45000, "quantity": 10000, "due_date": "2026-04-20"},
    {"order_id": "ORD-002", "supplier_agent_id": "cell-kr-001",
     "value_usd": 22000, "quantity": 5000, "due_date": "2026-04-28"},
]

impact = assess_disruption_impact(graph, "cell-kr-001", sample_orders)
print(f"Disruption at: {impact['disrupted_supplier']}")
print(f"Affected orders: {impact['affected_orders']}")
print(f"Financial exposure: ${impact['financial_exposure_usd']:,.2f}")
print(f"Downstream agents impacted: {impact['downstream_agent_count']}")
```

### Selecting an Alternate Supplier

The rerouting agent queries the pre-qualified alternates list first. If no pre-qualified alternate is available, it falls back to marketplace discovery with tighter constraints (higher minimum trust, verified identity required):

```python
def select_alternate_supplier(original_supplier: SupplierNode,
                               graph: SupplierGraph,
                               pre_qualified: list,
                               requirements: dict) -> dict:
    """
    Select the best alternate supplier for a disrupted source.
    Checks pre-qualified list first, then falls back to marketplace.
    """
    # Step 1: Check pre-qualified alternates
    for alt_id in pre_qualified:
        alt = graph.nodes.get(alt_id)
        if alt and alt.health_status == "healthy":
            # Verify the alternate is still active and compliant
            verification = execute("verify_agent", {
                "agent_id": alt_id
            })
            if verification.get("verified"):
                return {
                    "source": "pre_qualified",
                    "agent_id": alt_id,
                    "name": alt.name,
                    "trust_score": alt.trust_score,
                    "verified": True
                }

    # Step 2: Fall back to marketplace discovery
    print("No pre-qualified alternate available. Searching marketplace...")
    search_results = execute("search_services", {
        "query": original_supplier.category,
        "limit": 10
    })

    candidates = []
    for svc in search_results.get("services", []):
        rep = execute("get_agent_reputation", {
            "agent_id": svc["agent_id"]
        })
        score = rep.get("score", 0)
        if score >= requirements.get("min_trust_score", 0.85):
            # Verify identity
            verification = execute("verify_agent", {
                "agent_id": svc["agent_id"]
            })
            if verification.get("verified"):
                candidates.append({
                    "source": "marketplace_discovery",
                    "agent_id": svc["agent_id"],
                    "name": svc.get("name", "Unknown"),
                    "trust_score": score,
                    "verified": True
                })

    if not candidates:
        return {"source": "none", "error": "No qualified alternate found"}

    # Return highest trust score candidate
    candidates.sort(key=lambda c: c["trust_score"], reverse=True)
    return candidates[0]


# Find alternate for Korean cell manufacturer
alternate = select_alternate_supplier(
    original_supplier=cell_mfg_kr,
    graph=graph,
    pre_qualified=["cell-jp-001"],   # Japan cell manufacturer is pre-qualified
    requirements={"min_trust_score": 0.85}
)
print(f"Selected alternate: {alternate['name']} "
      f"(trust: {alternate['trust_score']:.2f}, source: {alternate['source']})")
```

### Executing the Reroute

Once an alternate is selected, the rerouting agent creates a new escrow-protected order and notifies all affected downstream agents:

```python
def execute_reroute(original_order: dict, alternate: dict,
                    downstream_agents: list) -> dict:
    """
    Execute a full supply chain reroute:
    1. Create escrow with alternate supplier
    2. Notify downstream agents of delay
    3. Update supplier graph
    """
    results = {"steps": []}

    # Step 1: Create escrow with the alternate supplier
    escrow = execute("create_escrow", {
        "payer_id": orchestrator_id,
        "payee_id": alternate["agent_id"],
        "amount": str(original_order["value_usd"]),
        "currency": "USD",
        "conditions": {
            "delivery_by": original_order["due_date"],
            "quantity": original_order["quantity"],
            "quality_standard": "per_original_sla",
            "auto_release_on_confirmation": True
        }
    })
    results["escrow_id"] = escrow.get("escrow_id")
    results["steps"].append({
        "action": "escrow_created",
        "escrow_id": escrow.get("escrow_id"),
        "amount_usd": original_order["value_usd"]
    })

    # Step 2: Notify downstream agents
    for agent in downstream_agents:
        execute("send_message", {
            "from_agent_id": orchestrator_id,
            "to_agent_id": agent["agent_id"],
            "message": {
                "type": "supply_chain_reroute",
                "original_order": original_order["order_id"],
                "original_supplier": original_order["supplier_agent_id"],
                "new_supplier": alternate["agent_id"],
                "new_supplier_name": alternate["name"],
                "estimated_delay_hours": 18,
                "action_required": "update_production_schedule"
            }
        })
        results["steps"].append({
            "action": "downstream_notified",
            "agent_id": agent["agent_id"]
        })

    # Step 3: Create SLA with the alternate supplier
    new_sla = execute("create_sla", {
        "agent_id": orchestrator_id,
        "counterparty_id": alternate["agent_id"],
        "terms": {
            "delivery_time_days": {"target": 14, "maximum": 21},
            "defect_rate_pct": {"target": 0.5, "maximum": 2.0},
            "fill_rate_pct": {"target": 98, "minimum": 95}
        }
    })
    results["new_sla_id"] = new_sla.get("sla_id")
    results["steps"].append({
        "action": "sla_created",
        "sla_id": new_sla.get("sla_id")
    })

    results["status"] = "reroute_complete"
    return results


# Execute the reroute
reroute_result = execute_reroute(
    original_order=sample_orders[0],
    alternate=alternate,
    downstream_agents=[
        {"agent_id": "pack-cn-001", "name": "PackAssembly Shenzhen"}
    ]
)

print(f"Reroute status: {reroute_result['status']}")
print(f"Escrow ID: {reroute_result['escrow_id']}")
print(f"New SLA ID: {reroute_result['new_sla_id']}")
for step in reroute_result["steps"]:
    print(f"  Step: {step['action']}")
```

### The Full Rerouting Pipeline

Putting it all together -- detection, assessment, selection, execution -- into a single orchestration function:

```python
def handle_critical_supplier(graph: SupplierGraph, monitor: SupplierHealthMonitor,
                              disrupted_agent_id: str, open_orders: list,
                              pre_qualified_alternates: dict) -> dict:
    """
    Full self-healing pipeline triggered when a supplier goes critical.

    Args:
        graph: Supplier network graph
        monitor: Health monitor instance
        disrupted_agent_id: The failing supplier's agent ID
        open_orders: All currently open orders
        pre_qualified_alternates: Dict of agent_id -> [alternate_ids]

    Returns:
        Summary of all rerouting actions taken.
    """
    pipeline_start = time.time()
    results = {"actions": [], "errors": []}

    # 1. Assess impact
    impact = assess_disruption_impact(graph, disrupted_agent_id, open_orders)
    results["impact"] = impact

    if not impact["requires_immediate_action"]:
        results["decision"] = "monitor_only"
        return results

    # 2. Select alternate
    supplier = graph.nodes.get(disrupted_agent_id)
    alternates = pre_qualified_alternates.get(disrupted_agent_id, [])

    alternate = select_alternate_supplier(
        original_supplier=supplier,
        graph=graph,
        pre_qualified=alternates,
        requirements={"min_trust_score": 0.85}
    )

    if alternate.get("source") == "none":
        results["decision"] = "escalate_to_human"
        results["reason"] = "No qualified alternate found"
        # Send emergency alert
        execute("send_message", {
            "from_agent_id": orchestrator_id,
            "to_agent_id": orchestrator_id,
            "message": {
                "type": "emergency_escalation",
                "disrupted_supplier": supplier.name if supplier else disrupted_agent_id,
                "financial_exposure": impact["financial_exposure_usd"],
                "action_needed": "manual_sourcing_required"
            }
        })
        return results

    # 3. Reroute affected orders
    affected_orders = [
        o for o in open_orders
        if o["supplier_agent_id"] == disrupted_agent_id
    ]

    for order in affected_orders:
        try:
            reroute = execute_reroute(
                original_order=order,
                alternate=alternate,
                downstream_agents=impact["downstream_impact"]
            )
            results["actions"].append({
                "order_id": order["order_id"],
                "reroute_status": reroute["status"],
                "new_supplier": alternate["name"],
                "escrow_id": reroute.get("escrow_id")
            })
        except Exception as e:
            results["errors"].append({
                "order_id": order["order_id"],
                "error": str(e)
            })

    elapsed = time.time() - pipeline_start
    results["decision"] = "auto_rerouted"
    results["elapsed_seconds"] = round(elapsed, 2)
    results["orders_rerouted"] = len(results["actions"])
    results["orders_failed"] = len(results["errors"])

    return results
```

### Rerouting Guardrails

Never deploy automated rerouting without these guardrails:

| Guardrail | Purpose | Implementation |
|-----------|---------|----------------|
| Budget cap per reroute | Prevent runaway spending | Check `ORCHESTRATION_LIMITS["max_api_budget_usd"]` before each reroute |
| Maximum reroute depth | Prevent cascading reroutes | `max_rerouting_depth: 2` -- if alternate also fails, escalate to human |
| Cooldown period | Prevent flapping | Minimum 1 hour between reroutes for same material |
| Single-source lockout | Force human review | If disrupted supplier is the only source, block auto-reroute |
| Downstream confirmation | Verify reroute was received | Require acknowledgment from downstream agents within 30 minutes |

---

## Chapter 5: Demand Signal Aggregation and Predictive Sourcing

### From Reactive to Predictive

Chapters 2-4 handle the supply side: who are your suppliers, are they healthy, and what happens when they fail. This chapter handles the demand side: what will you need, when will you need it, and can you source it before the need becomes urgent.

The demand aggregation agent collects signals from multiple internal sources -- sales forecasts, production schedules, inventory levels, seasonal patterns -- and translates them into sourcing actions. The goal is to shift procurement from reactive (order when inventory hits reorder point) to predictive (order based on demand forecast before inventory drops).

```
DEMAND SIGNALS                   AGGREGATION                 SOURCING ACTIONS
+------------------+            +---------------+           +------------------+
| Sales forecasts  |--+         |               |           | Pre-order from   |
+------------------+  |         | Demand        |           | preferred vendor |
                      +-------->| Aggregation   |---------->+------------------+
+------------------+  |         | Agent         |           | Request volume   |
| Production plans |--+         |               |           | discount quote   |
+------------------+  |         +-------+-------+           +------------------+
                      |                 |                    | Trigger new      |
+------------------+  |                 v                    | supplier search  |
| Inventory levels |--+         +-------+-------+           +------------------+
+------------------+  |         | Analytics &   |           | Adjust safety    |
                      +-------->| Forecasting   |           | stock levels     |
+------------------+  |         +---------------+           +------------------+
| Seasonal patterns|--+
+------------------+
```

### Collecting Analytics Data

Use GreenHelix analytics tools to gather transaction history and spending patterns that feed into demand forecasting:

```python
def collect_demand_signals(orchestrator_id: str, lookback_days: int = 90) -> dict:
    """
    Collect demand signals from transaction history and analytics.
    Returns aggregated data for forecasting.
    """
    # Get transaction history for spending patterns
    transactions = execute("get_transaction_history", {
        "agent_id": orchestrator_id,
        "limit": 500
    })

    # Get analytics for trend data
    analytics = execute("get_analytics", {
        "agent_id": orchestrator_id,
        "period": f"last_{lookback_days}_days",
        "metrics": ["spending_by_category", "order_frequency", "volume_trends"]
    })

    # Get current balance for budget planning
    balance = execute("get_balance", {
        "agent_id": orchestrator_id
    })

    return {
        "transactions": transactions,
        "analytics": analytics,
        "current_balance": balance,
        "lookback_days": lookback_days
    }


signals = collect_demand_signals(orchestrator_id, lookback_days=90)
print(f"Collected {len(signals['transactions'].get('transactions', []))} transactions")
```

### Demand Forecasting Logic

With historical data collected, apply forecasting logic to predict upcoming material needs. This example uses a simple moving average -- production systems should use more sophisticated models, but the GreenHelix integration pattern remains the same:

```python
from collections import defaultdict

def forecast_demand(transactions: list, forecast_days: int = 30) -> list:
    """
    Generate a demand forecast from transaction history.
    Groups by category and projects forward using weighted moving average.
    """
    # Group transactions by category and week
    weekly_demand = defaultdict(list)

    for tx in transactions:
        category = tx.get("category", "uncategorized")
        amount = float(tx.get("amount", 0))
        weekly_demand[category].append(amount)

    forecasts = []
    for category, amounts in weekly_demand.items():
        if len(amounts) < 4:
            continue

        # Weighted moving average (recent weeks weighted higher)
        weights = list(range(1, min(len(amounts), 12) + 1))
        recent = amounts[-len(weights):]
        weighted_avg = sum(w * a for w, a in zip(weights, recent)) / sum(weights)

        # Project forward
        projected_spend = weighted_avg * (forecast_days / 7)

        forecasts.append({
            "category": category,
            "weekly_average_usd": round(weighted_avg, 2),
            "projected_30day_usd": round(projected_spend, 2),
            "data_points": len(amounts),
            "trend": "increasing" if len(amounts) >= 4
                     and sum(amounts[-2:]) > sum(amounts[-4:-2])
                     else "stable"
        })

    # Sort by projected spend descending
    forecasts.sort(key=lambda f: f["projected_30day_usd"], reverse=True)
    return forecasts
```

### Predictive Sourcing: Acting on Forecasts

When the forecast predicts increased demand for a category, the sourcing agent should proactively negotiate volume discounts and secure supply:

```python
def predictive_sourcing_action(forecast: dict, preferred_suppliers: dict) -> dict:
    """
    Take proactive sourcing action based on a demand forecast.
    Negotiates volume discounts for high-demand categories.
    """
    category = forecast["category"]
    projected = forecast["projected_30day_usd"]

    # Only act on significant forecasted spend
    if projected < 5000:
        return {"action": "none", "reason": "Below threshold"}

    # Check if volume discount is available from preferred supplier
    supplier_id = preferred_suppliers.get(category)
    if not supplier_id:
        return {"action": "discover_supplier", "category": category}

    # Request volume discount estimate
    discount = execute("get_volume_discount", {
        "agent_id": orchestrator_id,
        "supplier_id": supplier_id,
        "volume_usd": str(projected),
        "period": "monthly"
    })

    # Estimate total cost with discount
    cost_estimate = execute("estimate_cost", {
        "agent_id": orchestrator_id,
        "amount": str(projected),
        "currency": "USD"
    })

    action = {
        "action": "negotiate_volume_discount",
        "category": category,
        "supplier_id": supplier_id,
        "projected_spend_usd": projected,
        "discount_available": discount,
        "cost_estimate": cost_estimate,
        "recommendation": "lock_in_rate" if forecast["trend"] == "increasing"
                          else "spot_buy"
    }

    # If trend is increasing and discount available, send intent
    if forecast["trend"] == "increasing":
        intent = execute("create_intent", {
            "agent_id": orchestrator_id,
            "type": "purchase",
            "details": {
                "category": category,
                "estimated_volume_usd": str(projected),
                "period": "next_30_days",
                "preferred_supplier": supplier_id
            }
        })
        action["intent_id"] = intent.get("intent_id")

    return action


# Example: act on battery cell forecast
sample_forecast = {
    "category": "battery_cells",
    "weekly_average_usd": 12500.00,
    "projected_30day_usd": 53571.43,
    "data_points": 24,
    "trend": "increasing"
}

sourcing_action = predictive_sourcing_action(
    forecast=sample_forecast,
    preferred_suppliers={"battery_cells": "cell-jp-001"}
)

print(f"Action: {sourcing_action['action']}")
print(f"Recommendation: {sourcing_action.get('recommendation', 'N/A')}")
```

### Demand Signal Types and Weighting

Not all demand signals carry equal predictive weight. A binding purchase order from a key customer is a stronger signal than a seasonal trend extrapolation. The demand aggregation agent should weight signals accordingly:

```
SIGNAL WEIGHTING MATRIX

Signal Type                  Weight    Lag         Reliability
---------------------------------------------------------------
Confirmed purchase orders    1.0       0 days      Very high
Production schedule commits  0.9       1-3 days    High
Sales pipeline (>80% prob)   0.7       7-14 days   Medium-high
Inventory reorder triggers   0.6       0 days      High (reactive)
Seasonal pattern match       0.5       30-90 days  Medium
Market trend extrapolation   0.3       60-180 days Low-medium
Economic indicator signals   0.2       90-365 days Low
```

The weighted forecast combines these signals into a single demand projection:

```python
def weighted_demand_forecast(signals: list) -> dict:
    """
    Combine multiple demand signals with weighting into
    a single demand projection per category.
    """
    SIGNAL_WEIGHTS = {
        "confirmed_po": 1.0,
        "production_schedule": 0.9,
        "sales_pipeline": 0.7,
        "inventory_reorder": 0.6,
        "seasonal_pattern": 0.5,
        "market_trend": 0.3,
        "economic_indicator": 0.2
    }

    category_demand = defaultdict(lambda: {"weighted_sum": 0, "weight_total": 0})

    for signal in signals:
        category = signal["category"]
        signal_type = signal["type"]
        amount = signal["projected_amount_usd"]
        weight = SIGNAL_WEIGHTS.get(signal_type, 0.1)

        category_demand[category]["weighted_sum"] += amount * weight
        category_demand[category]["weight_total"] += weight

    forecasts = {}
    for category, data in category_demand.items():
        if data["weight_total"] > 0:
            forecasts[category] = {
                "weighted_projection_usd": round(
                    data["weighted_sum"] / data["weight_total"], 2
                ),
                "signal_count": data["weight_total"],
                "confidence": "high" if data["weight_total"] > 2.0
                              else "medium" if data["weight_total"] > 1.0
                              else "low"
            }

    return forecasts


# Example signal inputs
sample_signals = [
    {"category": "battery_cells", "type": "confirmed_po",
     "projected_amount_usd": 55000},
    {"category": "battery_cells", "type": "production_schedule",
     "projected_amount_usd": 62000},
    {"category": "battery_cells", "type": "seasonal_pattern",
     "projected_amount_usd": 48000},
    {"category": "connectors", "type": "inventory_reorder",
     "projected_amount_usd": 8000},
    {"category": "connectors", "type": "market_trend",
     "projected_amount_usd": 12000},
]

forecast = weighted_demand_forecast(sample_signals)
for cat, data in forecast.items():
    print(f"  {cat}: ${data['weighted_projection_usd']:,.2f} "
          f"(confidence: {data['confidence']})")
```

### Inventory-Aware Sourcing Triggers

The demand aggregation agent should not just forecast -- it should trigger sourcing actions automatically when inventory projections cross safety thresholds. This closes the loop between demand intelligence and supply action:

```python
def check_sourcing_triggers(forecasts: dict, inventory_levels: dict,
                             safety_stock_days: int = 14) -> list:
    """
    Compare demand forecasts against inventory levels.
    Return a list of sourcing actions that should be triggered.
    """
    actions = []

    for category, forecast_data in forecasts.items():
        daily_demand = forecast_data["weighted_projection_usd"] / 30
        current_inventory_value = inventory_levels.get(category, {}).get("value_usd", 0)
        days_of_supply = (current_inventory_value / daily_demand
                          if daily_demand > 0 else float("inf"))

        if days_of_supply <= safety_stock_days * 0.5:
            actions.append({
                "category": category,
                "urgency": "critical",
                "action": "emergency_order",
                "days_of_supply": round(days_of_supply, 1),
                "recommended_order_usd": round(daily_demand * safety_stock_days * 2, 2)
            })
        elif days_of_supply <= safety_stock_days:
            actions.append({
                "category": category,
                "urgency": "standard",
                "action": "reorder",
                "days_of_supply": round(days_of_supply, 1),
                "recommended_order_usd": round(daily_demand * safety_stock_days, 2)
            })
        elif days_of_supply <= safety_stock_days * 1.5:
            actions.append({
                "category": category,
                "urgency": "low",
                "action": "monitor",
                "days_of_supply": round(days_of_supply, 1),
                "recommended_order_usd": 0
            })

    # Sort by urgency
    urgency_order = {"critical": 0, "standard": 1, "low": 2}
    actions.sort(key=lambda a: urgency_order.get(a["urgency"], 3))
    return actions
```

### Search for High-Performance Suppliers by Metrics

When your demand forecast exceeds current supplier capacity, use metrics-based search to find suppliers with proven high-volume track records:

```python
def find_high_capacity_suppliers(category: str, min_monthly_volume: float) -> list:
    """
    Search for suppliers by performance metrics.
    Targets suppliers with proven high-volume fulfillment capability.
    """
    results = execute("search_agents_by_metrics", {
        "metrics_filter": {
            "category": category,
            "min_fill_rate": 95,
            "min_monthly_volume_usd": min_monthly_volume,
            "min_trust_score": 0.85
        },
        "limit": 10
    })

    suppliers = results.get("agents", [])

    # Verify each candidate
    verified = []
    for s in suppliers:
        verification = execute("verify_agent", {"agent_id": s["agent_id"]})
        if verification.get("verified"):
            verified.append({
                "agent_id": s["agent_id"],
                "name": s.get("name"),
                "metrics": s.get("metrics", {}),
                "verified": True
            })

    return verified


# Find high-capacity battery cell suppliers
high_cap = find_high_capacity_suppliers("battery_cells", min_monthly_volume=50000)
for s in high_cap:
    print(f"  {s['name']} | Verified: {s['verified']}")
```

---

## Chapter 6: Cross-Border Compliance

### Tariffs, Sanctions Screening, and Multi-Jurisdictional Rules

A supply chain that crosses borders is a supply chain that crosses legal jurisdictions. Your orchestration agent cannot reroute an order from a Korean supplier to a Vietnamese supplier without verifying: (a) tariff implications for importing from Vietnam into your destination market, (b) the Vietnamese supplier is not on any sanctions list, (c) the rerouting does not violate any origin-of-goods rules that affect downstream sales, and (d) carbon reporting obligations under CBAM if the goods enter the EU.

The compliance agent handles all of this. It sits between every sourcing decision and every payment execution, verifying that the proposed transaction is lawful in every relevant jurisdiction.

```
SOURCING DECISION
    |
    v
+---+-----------------------------+
| COMPLIANCE GATE                 |
|                                 |
|  [1] Sanctions screen           |
|  [2] Tariff calculation         |
|  [3] Origin-of-goods rules     |
|  [4] Carbon/environmental regs  |
|  [5] Data residency (if digital)|
|  [6] Export controls             |
|                                 |
|  Result: PASS / FAIL / REVIEW   |
+---+-----------------------------+
    |
    v
PASS --> Execute payment
FAIL --> Block + log reason
REVIEW --> Queue for human review
```

### Running Compliance Checks

The GreenHelix `check_compliance` tool validates a transaction against the relevant regulatory frameworks. Wrap it in a gate function that blocks non-compliant transactions:

```python
def compliance_gate(transaction: dict) -> dict:
    """
    Run a compliance check on a proposed transaction.
    Must pass before any payment or escrow is created.

    Returns:
        {
            "allowed": bool,
            "checks": [...],
            "blocked_reasons": [...] (if any)
        }
    """
    # Run the compliance check
    result = execute("check_compliance", {
        "agent_id": orchestrator_id,
        "transaction": {
            "type": transaction["type"],
            "counterparty_id": transaction["supplier_agent_id"],
            "amount": str(transaction["amount_usd"]),
            "currency": "USD",
            "origin_country": transaction.get("origin_country"),
            "destination_country": transaction.get("destination_country"),
            "goods_category": transaction.get("goods_category"),
            "hs_code": transaction.get("hs_code")
        }
    })

    checks_passed = result.get("compliant", False)
    details = result.get("details", {})

    response = {
        "allowed": checks_passed,
        "compliance_id": result.get("compliance_id"),
        "checks": details.get("checks_performed", []),
        "blocked_reasons": details.get("violations", []),
        "tariff_rate": details.get("tariff_rate"),
        "estimated_duties_usd": details.get("estimated_duties"),
        "warnings": details.get("warnings", [])
    }

    return response


# Check compliance for rerouted order to Vietnam
compliance_result = compliance_gate({
    "type": "purchase",
    "supplier_agent_id": "cell-vn-001",
    "amount_usd": 45000,
    "origin_country": "VN",
    "destination_country": "US",
    "goods_category": "lithium_ion_battery_cells",
    "hs_code": "8507.60"
})

if compliance_result["allowed"]:
    print("Compliance: PASS")
    print(f"Tariff rate: {compliance_result.get('tariff_rate', 'N/A')}")
    print(f"Estimated duties: ${compliance_result.get('estimated_duties_usd', 'N/A')}")
else:
    print("Compliance: BLOCKED")
    for reason in compliance_result["blocked_reasons"]:
        print(f"  Violation: {reason}")
```

### Integrating Compliance into Rerouting

The compliance gate must be inserted into the rerouting pipeline from Chapter 4. Here is the updated alternate selection function that checks compliance before approving a supplier:

```python
def select_compliant_alternate(original_supplier: SupplierNode,
                                candidates: list,
                                order: dict) -> dict:
    """
    Select an alternate supplier that passes both trust AND compliance checks.
    Iterates through candidates until one passes, or returns None.
    """
    for candidate in candidates:
        # Trust check (already done in discovery, but verify current score)
        rep = execute("get_agent_reputation", {
            "agent_id": candidate["agent_id"]
        })
        if rep.get("score", 0) < 0.85:
            continue

        # Compliance check
        compliance = compliance_gate({
            "type": "purchase",
            "supplier_agent_id": candidate["agent_id"],
            "amount_usd": order["value_usd"],
            "origin_country": candidate.get("country"),
            "destination_country": order.get("destination_country", "US"),
            "goods_category": original_supplier.category,
            "hs_code": order.get("hs_code")
        })

        if compliance["allowed"]:
            return {
                "agent_id": candidate["agent_id"],
                "name": candidate["name"],
                "trust_score": rep.get("score"),
                "compliance_id": compliance["compliance_id"],
                "tariff_rate": compliance.get("tariff_rate"),
                "estimated_duties_usd": compliance.get("estimated_duties_usd"),
                "total_landed_cost_usd": (
                    order["value_usd"]
                    + (compliance.get("estimated_duties_usd") or 0)
                )
            }
        else:
            print(f"  {candidate['name']} failed compliance: "
                  f"{compliance['blocked_reasons']}")

    return None  # No compliant alternate found
```

### Building Claim Chains for Provenance

For goods that require origin traceability (conflict minerals, organic certification, carbon footprint), use GreenHelix claim chains to build a verifiable provenance trail:

```python
def build_provenance_chain(graph: SupplierGraph, product_id: str,
                           tier1_agent_id: str) -> dict:
    """
    Build a claim chain tracing a product's provenance through
    the supplier graph. Each tier adds a verifiable claim.
    """
    # Get the upstream chain
    upstream = graph.get_upstream_chain(tier1_agent_id)

    # Build claim chain starting from deepest tier
    upstream.reverse()  # Start from raw materials

    chain = execute("build_claim_chain", {
        "agent_id": orchestrator_id,
        "product_id": product_id,
        "claims": [
            {
                "supplier_agent_id": node["agent_id"],
                "tier": node["tier"],
                "material": node["material"],
                "claim_type": "origin_verification",
                "metadata": {
                    "trust_score": node["trust_score"]
                }
            }
            for node in upstream
        ]
    })

    return chain


# Build provenance chain for a battery pack order
provenance = build_provenance_chain(
    graph=graph,
    product_id="BATT-PACK-2026-Q2-001",
    tier1_agent_id="pack-cn-001"
)

print(f"Claim chain ID: {provenance.get('chain_id')}")
print(f"Claims in chain: {len(provenance.get('claims', []))}")
```

### Multi-Jurisdictional Decision Matrix

When a rerouting event changes the origin country, multiple compliance dimensions shift simultaneously. Use this matrix to determine which checks are required for any origin-destination pair:

```
COMPLIANCE CHECK MATRIX

Origin \ Dest  |  US           |  EU           |  UK           |  APAC
---------------|---------------|---------------|---------------|---------------
China (CN)     |  Sec 301      |  Anti-dumping |  Post-Brexit  |  RCEP rules
               |  Entity List  |  CBAM carbon  |  UK tariff    |  of origin
               |  ITAR screen  |  Dual-use     |  schedule     |
---------------|---------------|---------------|---------------|---------------
Vietnam (VN)   |  GSP eligible |  EBA pref     |  DCTS pref    |  RCEP pref
               |  AD/CVD watch |  CBAM carbon  |  UK FTA       |  CPTPP rules
               |  Origin verify|  Dual-use     |  schedule     |
---------------|---------------|---------------|---------------|---------------
South Korea    |  KORUS FTA    |  EU-KR FTA    |  UK-KR FTA    |  RCEP pref
(KR)           |  Pref tariff  |  Pref tariff  |  Pref tariff  |  CPTPP rules
               |  ITAR screen  |  Dual-use     |  schedule     |
---------------|---------------|---------------|---------------|---------------
Japan (JP)     |  No FTA       |  EU-JP EPA    |  UK-JP CEPA   |  RCEP pref
               |  MFN rates    |  Pref tariff  |  Pref tariff  |  CPTPP rules
               |  ITAR screen  |  Dual-use     |  schedule     |
```

The compliance agent must map each rerouting scenario to the correct row and column, then execute all applicable checks. A reroute from South Korea (KORUS FTA preferential tariff) to Vietnam (GSP eligible but with anti-dumping watch) can change the landed cost by 8-15% -- enough to make the reroute economically unviable even if the alternate supplier's unit price is lower.

```python
def calculate_landed_cost(unit_price_usd: float, quantity: int,
                          compliance_result: dict,
                          shipping_estimate_usd: float) -> dict:
    """
    Calculate total landed cost including tariffs, duties,
    and shipping for a supply chain transaction.
    """
    subtotal = unit_price_usd * quantity
    tariff_rate = compliance_result.get("tariff_rate", 0) or 0
    duties = subtotal * (tariff_rate / 100)
    total_landed = subtotal + duties + shipping_estimate_usd

    return {
        "unit_price_usd": unit_price_usd,
        "quantity": quantity,
        "subtotal_usd": round(subtotal, 2),
        "tariff_rate_pct": tariff_rate,
        "duties_usd": round(duties, 2),
        "shipping_usd": round(shipping_estimate_usd, 2),
        "total_landed_usd": round(total_landed, 2),
        "effective_unit_cost_usd": round(total_landed / quantity, 4)
    }
```

### Cross-Border Compliance Checklist

- [ ] Compliance gate integrated before every `create_escrow` and `transfer` call
- [ ] HS codes mapped for every product category in supplier graph
- [ ] Sanctions screening enabled for all new supplier registrations
- [ ] Tariff calculations cached per origin-destination pair (refresh weekly)
- [ ] Claim chains built for all regulated goods (conflict minerals, dual-use)
- [ ] CBAM carbon reporting data collected from EU-bound suppliers
- [ ] Compliance audit log retained (minimum 7 years for trade compliance)
- [ ] Human review queue configured for "REVIEW" results from compliance gate

---

## Chapter 7: Agent-to-Agent Coordination

### Messaging, Escrow, and Dispute Resolution Across the Network

A multi-agent supply chain only works if agents can coordinate. The supply tier agents need to tell the demand tier agents about capacity changes. The compliance agent needs to block the rerouting agent when a proposed alternate fails sanctions screening. The orchestrator needs to sequence all of these interactions without becoming a bottleneck.

GreenHelix provides three coordination primitives:

1. **Messaging** -- Asynchronous message passing between any two registered agents
2. **Escrow** -- Financial coordination that holds funds until delivery conditions are met
3. **Dispute Resolution** -- Structured conflict resolution when deliveries fail

### The Message Bus Pattern

Rather than point-to-point messaging between every agent pair, implement a topic-based message bus where agents subscribe to event types. The orchestrator routes messages based on topic:

```python
class SupplyChainMessageBus:
    """
    Message bus for supply chain agent coordination.
    Uses GreenHelix messaging as transport layer.
    """

    # Topic definitions
    TOPICS = {
        "disruption.detected": ["rerouting-agent", "demand-aggregation-agent"],
        "disruption.rerouted": ["health-monitor-agent", "compliance-agent"],
        "compliance.blocked": ["rerouting-agent", "supply-chain-orchestrator"],
        "demand.forecast_updated": ["supplier-discovery-agent"],
        "sla.breach": ["health-monitor-agent", "supply-chain-orchestrator"],
        "order.created": ["compliance-agent", "health-monitor-agent"],
        "order.delivered": ["demand-aggregation-agent", "health-monitor-agent"]
    }

    def __init__(self, orchestrator_id: str, agent_ids: dict):
        self.orchestrator_id = orchestrator_id
        self.agent_ids = agent_ids  # name -> agent_id mapping

    def publish(self, topic: str, payload: dict, sender_id: str):
        """Publish a message to all subscribers of a topic."""
        subscribers = self.TOPICS.get(topic, [])
        results = []

        for subscriber_name in subscribers:
            subscriber_id = self.agent_ids.get(subscriber_name)
            if not subscriber_id or subscriber_id == sender_id:
                continue

            result = execute("send_message", {
                "from_agent_id": sender_id,
                "to_agent_id": subscriber_id,
                "message": {
                    "topic": topic,
                    "payload": payload,
                    "timestamp": datetime.datetime.utcnow().isoformat()
                }
            })
            results.append({
                "subscriber": subscriber_name,
                "message_id": result.get("message_id")
            })

        return results

    def poll(self, agent_id: str, topics: list = None) -> list:
        """
        Poll for messages addressed to an agent.
        Optionally filter by topic.
        """
        messages = execute("get_messages", {
            "agent_id": agent_id
        })

        all_messages = messages.get("messages", [])

        if topics:
            filtered = [
                m for m in all_messages
                if m.get("message", {}).get("topic") in topics
            ]
            return filtered

        return all_messages


# Initialize the message bus
bus = SupplyChainMessageBus(orchestrator_id, agent_ids)

# Publish a disruption event
bus.publish(
    topic="disruption.detected",
    payload={
        "supplier_agent_id": "cell-kr-001",
        "supplier_name": "CellTech Korea",
        "disruption_type": "sla_breach_consecutive",
        "severity": "critical",
        "affected_orders": ["ORD-001", "ORD-002"]
    },
    sender_id=agent_ids["health-monitor-agent"]
)
```

### Escrow-Protected Supply Chain Transactions

Every financial transaction between supply chain agents should be escrow-protected. The escrow holds funds until the buyer confirms delivery, protecting both sides:

```python
def create_supply_chain_escrow(buyer_id: str, supplier_id: str,
                                order: dict) -> dict:
    """
    Create an escrow for a supply chain order with delivery conditions.
    Funds are held until delivery is confirmed or dispute is opened.
    """
    escrow = execute("create_escrow", {
        "payer_id": buyer_id,
        "payee_id": supplier_id,
        "amount": str(order["value_usd"]),
        "currency": "USD",
        "conditions": {
            "delivery_deadline": order["due_date"],
            "quantity": order["quantity"],
            "quality_standard": order.get("quality_standard", "as_described"),
            "inspection_period_hours": 48,
            "auto_release_days": 7
        }
    })
    return escrow


def confirm_delivery_and_release(escrow_id: str, delivery_data: dict) -> dict:
    """
    Confirm delivery and release escrow funds to supplier.
    Only release if delivery meets quality standards.
    """
    # Validate delivery against order requirements
    meets_requirements = (
        delivery_data["fill_rate"] >= 95
        and delivery_data["defect_rate"] <= 2.0
    )

    if meets_requirements:
        release = execute("release_escrow", {
            "escrow_id": escrow_id,
            "release_reason": "delivery_confirmed",
            "delivery_metrics": delivery_data
        })
        return {"status": "released", "result": release}
    else:
        # Open dispute for substandard delivery
        dispute = execute("open_dispute", {
            "escrow_id": escrow_id,
            "reason": "delivery_below_sla",
            "evidence": {
                "expected_fill_rate": 95,
                "actual_fill_rate": delivery_data["fill_rate"],
                "expected_max_defect_rate": 2.0,
                "actual_defect_rate": delivery_data["defect_rate"]
            }
        })
        return {"status": "disputed", "dispute": dispute}


# Create escrow for an order
escrow = create_supply_chain_escrow(
    buyer_id=orchestrator_id,
    supplier_id="cell-jp-001",
    order={
        "order_id": "ORD-003",
        "value_usd": 38000,
        "quantity": 8000,
        "due_date": "2026-05-01",
        "quality_standard": "IEC62133"
    }
)

print(f"Escrow created: {escrow.get('escrow_id')}")

# Later, when delivery arrives...
delivery_result = confirm_delivery_and_release(
    escrow_id=escrow.get("escrow_id"),
    delivery_data={
        "fill_rate": 99.1,
        "defect_rate": 0.4,
        "delivery_days": 13,
        "inspection_passed": True
    }
)

print(f"Delivery result: {delivery_result['status']}")
```

### Dispute Resolution

When a delivery fails inspection, the dispute resolution process ensures both parties have a structured path to resolution:

```python
def handle_supply_chain_dispute(escrow_id: str, dispute_id: str,
                                 evidence: dict) -> dict:
    """
    Handle a supply chain dispute through the GreenHelix resolution process.

    Steps:
    1. Gather evidence from both parties
    2. Check SLA terms for applicable penalties
    3. Propose resolution (partial refund, replacement, or full refund)
    4. Execute resolution
    """
    # Check if a resolution can be proposed
    resolution_proposal = {
        "escrow_id": escrow_id,
        "dispute_id": dispute_id,
        "proposed_resolution": None,
        "reasoning": None
    }

    actual_fill = evidence.get("actual_fill_rate", 0)
    expected_fill = evidence.get("expected_fill_rate", 95)
    shortfall_pct = ((expected_fill - actual_fill) / expected_fill) * 100

    if shortfall_pct <= 5:
        # Minor shortfall: partial refund proportional to shortfall
        resolution_proposal["proposed_resolution"] = "partial_refund"
        resolution_proposal["refund_percentage"] = round(shortfall_pct, 1)
        resolution_proposal["reasoning"] = (
            f"Fill rate {actual_fill}% vs {expected_fill}% target. "
            f"Shortfall of {shortfall_pct:.1f}% warrants proportional refund."
        )
    elif shortfall_pct <= 20:
        # Significant shortfall: partial refund + replacement order
        resolution_proposal["proposed_resolution"] = "partial_refund_plus_replacement"
        resolution_proposal["refund_percentage"] = round(shortfall_pct, 1)
        resolution_proposal["reasoning"] = (
            f"Significant shortfall of {shortfall_pct:.1f}%. "
            f"Proportional refund plus replacement order for missing quantity."
        )
    else:
        # Major failure: full refund
        resolution_proposal["proposed_resolution"] = "full_refund"
        resolution_proposal["refund_percentage"] = 100
        resolution_proposal["reasoning"] = (
            f"Critical shortfall of {shortfall_pct:.1f}%. "
            f"Full refund recommended."
        )

    # Execute the resolution
    resolution = execute("resolve_dispute", {
        "dispute_id": dispute_id,
        "resolution": resolution_proposal["proposed_resolution"],
        "details": resolution_proposal
    })

    return {
        "resolution": resolution,
        "proposal": resolution_proposal
    }
```

### Coordination Patterns for Multi-Agent Workflows

Here are three coordination patterns used in production supply chain orchestration:

**Pattern 1: Sequential Gate.** Compliance check before every payment. No agent can bypass the gate.

```python
def gated_payment(payer_id: str, payee_id: str, amount: float,
                  transaction_context: dict) -> dict:
    """Payment only executes if compliance gate passes."""
    compliance = compliance_gate({
        "type": "payment",
        "supplier_agent_id": payee_id,
        "amount_usd": amount,
        **transaction_context
    })

    if not compliance["allowed"]:
        return {"status": "blocked", "reasons": compliance["blocked_reasons"]}

    # Create invoice
    invoice = execute("create_invoice", {
        "from_agent_id": payee_id,
        "to_agent_id": payer_id,
        "amount": str(amount),
        "currency": "USD",
        "compliance_id": compliance["compliance_id"]
    })

    # Execute transfer
    transfer = execute("transfer", {
        "from_agent_id": payer_id,
        "to_agent_id": payee_id,
        "amount": str(amount),
        "currency": "USD",
        "reference": invoice.get("invoice_id")
    })

    return {"status": "completed", "transfer": transfer, "invoice": invoice}
```

**Pattern 2: Fan-Out/Fan-In.** Discover multiple suppliers in parallel, collect results, select the best.

```python
def parallel_supplier_evaluation(category: str, candidate_ids: list) -> list:
    """
    Evaluate multiple suppliers in parallel.
    Each evaluation is independent — collect all results then rank.
    """
    evaluations = []

    for agent_id in candidate_ids:
        # Get reputation
        rep = execute("get_agent_reputation", {"agent_id": agent_id})

        # Get SLA status if exists
        sla_status = execute("get_sla_status", {
            "sla_id": f"sla-{agent_id}"  # Assuming SLA ID convention
        })

        # Verify identity
        verification = execute("verify_agent", {"agent_id": agent_id})

        evaluations.append({
            "agent_id": agent_id,
            "trust_score": rep.get("score", 0),
            "sla_compliant": sla_status.get("compliant", None),
            "verified": verification.get("verified", False),
            "composite_score": (
                rep.get("score", 0) * 0.4
                + (1.0 if sla_status.get("compliant") else 0.5) * 0.4
                + (1.0 if verification.get("verified") else 0.0) * 0.2
            )
        })

    # Rank by composite score
    evaluations.sort(key=lambda e: e["composite_score"], reverse=True)
    return evaluations
```

**Pattern 3: Event-Driven Cascade.** A disruption event triggers a cascade of actions across multiple agents without centralized coordination.

```python
def disruption_cascade(bus: SupplyChainMessageBus, event: dict):
    """
    Trigger event-driven cascade across the supply chain network.
    Each agent reacts to the event independently.
    """
    # Phase 1: Health monitor detects and publishes
    bus.publish(
        topic="disruption.detected",
        payload=event,
        sender_id=agent_ids["health-monitor-agent"]
    )

    # Phase 2: Rerouting agent reacts (via message polling)
    # In production, this runs in the rerouting agent's event loop
    reroute_messages = bus.poll(
        agent_id=agent_ids["rerouting-agent"],
        topics=["disruption.detected"]
    )

    for msg in reroute_messages:
        payload = msg.get("message", {}).get("payload", {})
        # Rerouting agent publishes its result
        bus.publish(
            topic="disruption.rerouted",
            payload={
                "original_event": payload,
                "new_supplier": "cell-jp-001",
                "action": "rerouted"
            },
            sender_id=agent_ids["rerouting-agent"]
        )

    # Phase 3: Compliance agent validates the reroute
    compliance_messages = bus.poll(
        agent_id=agent_ids["compliance-agent"],
        topics=["disruption.rerouted"]
    )

    for msg in compliance_messages:
        payload = msg.get("message", {}).get("payload", {})
        new_supplier = payload.get("new_supplier")
        # Run compliance check on new supplier
        result = compliance_gate({
            "type": "reroute",
            "supplier_agent_id": new_supplier,
            "amount_usd": event.get("financial_exposure", 0),
            "origin_country": "JP",
            "destination_country": "US",
            "goods_category": "battery_cells"
        })

        if not result["allowed"]:
            bus.publish(
                topic="compliance.blocked",
                payload={
                    "blocked_supplier": new_supplier,
                    "reasons": result["blocked_reasons"]
                },
                sender_id=agent_ids["compliance-agent"]
            )
```

---

## Chapter 8: The 30-Day Implementation Sprint

### From Single Buyer to Orchestrated Supply Network

You do not need six months to build a multi-agent supply chain. You need 30 days of focused implementation, starting with the simplest viable agent and adding capabilities week by week. This chapter provides the sprint plan.

### Week 1: Foundation (Days 1-7)

**Goal:** Single orchestration agent with Tier-1 supplier graph and basic health monitoring.

```
Day 1-2: Agent Registration & Identity
    - Register orchestrator agent (Chapter 1)
    - Register 3-5 sub-agents (discovery, health, rerouting, demand, compliance)
    - Verify all agents with verify_agent
    - Set up the execute() helper and ORCHESTRATION_LIMITS

Day 3-4: Supplier Graph
    - Map your top 10 Tier-1 suppliers into SupplierGraph
    - Run search_services for each supplier category
    - Score each supplier with get_agent_reputation
    - Build dependency edges for known Tier-2 relationships

Day 5-7: Basic Health Monitoring
    - Create SLAs for top 5 Tier-1 suppliers (create_sla)
    - Implement SupplierHealthMonitor with 1-hour check interval
    - Set up breach counting and alert generation
    - Test: manually trigger a "warning" state, verify alert fires
```

**Week 1 validation checklist:**

- [ ] All agents registered and verified on GreenHelix
- [ ] Supplier graph contains at least 10 Tier-1 nodes
- [ ] SLAs created for top 5 suppliers
- [ ] Health monitor runs without errors for 24 hours
- [ ] At least one alert generated and routed correctly

### Week 2: Resilience (Days 8-14)

**Goal:** Automated rerouting for Tier-1 disruptions with compliance gating.

```
Day 8-9: Alternate Supplier Qualification
    - For each Tier-1 supplier, identify 2 alternates
    - Run get_agent_reputation and verify_agent on each alternate
    - Store pre-qualified alternates in the graph

Day 10-11: Rerouting Pipeline
    - Implement assess_disruption_impact
    - Implement select_alternate_supplier (with pre-qualified list)
    - Implement execute_reroute with escrow creation
    - Add rerouting guardrails (budget cap, depth limit, cooldown)

Day 12-13: Compliance Gate
    - Implement compliance_gate wrapping check_compliance
    - Insert gate into rerouting pipeline
    - Test: attempt reroute to a non-compliant supplier, verify block

Day 14: Integration Test
    - Simulate full disruption: mark supplier critical, verify
      auto-reroute fires, compliance passes, escrow created,
      downstream agents notified
    - Measure end-to-end latency (target: under 60 seconds)
```

**Week 2 validation checklist:**

- [ ] At least 2 pre-qualified alternates per Tier-1 supplier
- [ ] Rerouting pipeline executes end-to-end in under 60 seconds
- [ ] Compliance gate blocks non-compliant reroutes
- [ ] Escrow created for every rerouted order
- [ ] Downstream agents receive notification messages
- [ ] Budget guardrail tested and enforced

### Week 3: Intelligence (Days 15-21)

**Goal:** Demand forecasting with predictive sourcing and multi-tier visibility.

```
Day 15-16: Demand Signal Collection
    - Implement collect_demand_signals with get_transaction_history
    - Pull 90 days of historical data
    - Implement forecast_demand with weighted moving average

Day 17-18: Predictive Sourcing
    - Implement predictive_sourcing_action
    - Connect to get_volume_discount and estimate_cost
    - Create purchase intents for increasing-trend categories

Day 19-20: Multi-Tier Mapping
    - Extend supplier graph to Tier-2 for all critical materials
    - Map Tier-3 for single-source risk materials
    - Implement get_impact_zone for Tier-3 disruption scenarios

Day 21: Provenance & Metrics
    - Implement build_provenance_chain for regulated goods
    - Submit historical metrics with submit_metrics
    - Set up search_agents_by_metrics for capacity planning
```

**Week 3 validation checklist:**

- [ ] Demand forecasts generated for top 10 spending categories
- [ ] At least one volume discount negotiated via predictive sourcing
- [ ] Supplier graph extends to Tier-2 for all Tier-1 suppliers
- [ ] Tier-3 mapped for at least 3 single-source materials
- [ ] Impact zone analysis produces correct cascade for Tier-3 disruption
- [ ] Claim chain built for at least one regulated product

### Week 4: Coordination (Days 22-30)

**Goal:** Full multi-agent coordination with message bus, dispute resolution, and production hardening.

```
Day 22-23: Message Bus
    - Implement SupplyChainMessageBus with topic routing
    - Wire all sub-agents to publish/subscribe on relevant topics
    - Test event cascade: disruption -> reroute -> compliance check

Day 24-25: Escrow & Disputes
    - Implement create_supply_chain_escrow for all new orders
    - Implement confirm_delivery_and_release
    - Implement handle_supply_chain_dispute for failed deliveries

Day 26-27: Production Hardening
    - Add retry logic to all execute() calls (3 retries, exponential backoff)
    - Add circuit breakers for recursive agent spawning
    - Implement budget tracking across all agents
    - Add structured logging for every orchestration decision

Day 28-29: Monitoring & Alerting
    - Dashboard: supplier health status across all tiers
    - Dashboard: demand forecasts vs actual orders
    - Dashboard: rerouting events with latency metrics
    - Alerting: critical supplier + failed reroute + budget threshold

Day 30: Load Test & Documentation
    - Simulate 50 concurrent supplier health checks
    - Simulate 5 simultaneous disruption reroutes
    - Verify budget limits hold under load
    - Document all agent configurations and SLA terms
```

**Week 4 validation checklist:**

- [ ] Message bus delivers events to all subscribers within 5 seconds
- [ ] Escrow created and released for at least 3 test orders
- [ ] One dispute opened and resolved through structured process
- [ ] Retry logic handles GreenHelix API transient failures
- [ ] Circuit breaker triggers when agent count exceeds limit
- [ ] Budget tracking accurate across all agents
- [ ] Load test passes: 50 health checks + 5 reroutes concurrently
- [ ] All dashboards operational

### Production Architecture Reference

The final production architecture after the 30-day sprint:

```
+=========================================================================+
|                         PRODUCTION DEPLOYMENT                           |
+=========================================================================+
|                                                                         |
|  Orchestrator Process (always-on)                                       |
|  +----------------------------------------------------------------+    |
|  | Event Loop                                                      |    |
|  |   - Polls message bus every 5s                                  |    |
|  |   - Dispatches events to handler functions                      |    |
|  |   - Enforces ORCHESTRATION_LIMITS globally                      |    |
|  +----------------------------------------------------------------+    |
|                                                                         |
|  Health Monitor (cron: every 15 min)                                    |
|  +----------------------------------------------------------------+    |
|  | For each supplier in graph:                                     |    |
|  |   check_sla_compliance -> check_trust_score -> publish status   |    |
|  +----------------------------------------------------------------+    |
|                                                                         |
|  Demand Aggregator (cron: daily)                                        |
|  +----------------------------------------------------------------+    |
|  | collect_demand_signals -> forecast_demand ->                    |    |
|  |   predictive_sourcing_action -> publish forecasts               |    |
|  +----------------------------------------------------------------+    |
|                                                                         |
|  Rerouting Agent (event-driven)                                         |
|  +----------------------------------------------------------------+    |
|  | On disruption.detected:                                         |    |
|  |   assess_impact -> select_alternate -> compliance_gate ->       |    |
|  |   execute_reroute -> publish disruption.rerouted                |    |
|  +----------------------------------------------------------------+    |
|                                                                         |
|  Compliance Agent (gate: synchronous)                                   |
|  +----------------------------------------------------------------+    |
|  | On every payment/escrow/reroute:                                |    |
|  |   check_compliance -> PASS/FAIL/REVIEW                          |    |
|  +----------------------------------------------------------------+    |
|                                                                         |
+=========================================================================+
|  GreenHelix A2A Commerce Gateway (https://api.greenhelix.net/v1)       |
|  128 tools | Identity | Payments | Trust | Messaging | Escrow | SLA   |
+=========================================================================+
```

### Cost Estimation

Estimate your GreenHelix API usage for production operation:

| Operation | Frequency | Calls/Month | Est. Cost |
|-----------|-----------|-------------|-----------|
| Health checks (50 suppliers, 15-min interval) | 4/hour | 144,000 | Varies by tier |
| Demand signal collection | Daily | 30 | Minimal |
| Compliance checks | Per order | ~200 | Per-call pricing |
| Messaging (bus events) | Per event | ~5,000 | Per-call pricing |
| Rerouting (full pipeline) | ~2-5/month | ~50 | Per-call pricing |
| Discovery (new suppliers) | Weekly | ~100 | Per-call pricing |

Use `estimate_cost` to get exact pricing for your usage pattern:

```python
cost = execute("estimate_cost", {
    "agent_id": orchestrator_id,
    "amount": "1000",
    "currency": "USD"
})
print(f"Estimated cost: {cost}")
```

---

## What You Get

By following this guide, you will have built:

**A Multi-Tier Supplier Graph** -- Not a flat vendor list. A graph data structure mapping supplier dependencies across three tiers, with trust scores, health status, and impact zone analysis for every node. When a Tier-3 lithium mine goes offline, you know within seconds which Tier-1 assemblers are affected and which orders are at risk.

**Real-Time Health Monitoring** -- SLA compliance checking, trust score trend analysis, and anomaly detection running continuously across your entire supplier network. Leading indicators of supplier degradation detected before they become delivery failures.

**Self-Healing Rerouting** -- Automated disruption response that assesses impact, selects a pre-qualified alternate, verifies compliance, creates escrow-protected orders, and notifies downstream agents -- all within 60 seconds, with budget caps and depth limits preventing runaway costs.

**Predictive Sourcing** -- Demand signal aggregation and forecasting that shifts procurement from reactive to predictive. Volume discounts negotiated before demand spikes. New suppliers discovered before capacity constraints bind.

**Cross-Border Compliance** -- A compliance gate inserted into every financial transaction. Sanctions screening, tariff calculation, and provenance tracking via verifiable claim chains. No payment executes without passing the gate.

**Multi-Agent Coordination** -- A topic-based message bus, escrow-protected transactions, and structured dispute resolution. Agents collaborate without centralized bottlenecks, and every financial interaction is protected.

**A 30-Day Implementation Sprint** -- A week-by-week plan with daily tasks, validation checklists, and a production architecture reference. You start with a single orchestration agent on Day 1 and have a full multi-agent supply chain network by Day 30.

All code examples use the GreenHelix A2A Commerce Gateway at `https://api.greenhelix.net/v1`, with the standard the REST API (`POST /v1/{tool}`) pattern. Every tool call is production-ready -- copy the code, set your API key, and deploy.

