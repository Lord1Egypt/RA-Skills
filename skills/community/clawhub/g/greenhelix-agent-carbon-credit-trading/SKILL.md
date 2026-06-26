---
name: greenhelix-agent-carbon-credit-trading
version: "1.3.1"
description: "Agent-Powered Carbon Credit Trading & CBAM Compliance. Build autonomous carbon credit trading agents: credit discovery, MRV verification, escrow-protected trading, CBAM compliance automation, multi-agent portfolios, and dispute resolution. Includes detailed Python code examples for every pattern."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [carbon-credits, cbam, emissions, trading, compliance, escrow, sustainability, guide, greenhelix, openclaw, ai-agent]
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
# Agent-Powered Carbon Credit Trading & CBAM Compliance

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `GREENHELIX_API_KEY`: API authentication for GreenHelix gateway (read/write access to purchased API tools only)


The EU Carbon Border Adjustment Mechanism became financially binding on January 1, 2026. Every importer of iron, steel, aluminum, cement, fertilizer, hydrogen, and electricity into the European Union must now surrender CBAM certificates corresponding to the embedded emissions of their imports. The penalty for non-compliance is EUR 100 per tonne of CO2 equivalent not covered. This is not a reporting exercise anymore -- the transitional phase ended December 31, 2025. Real money moves now. Meanwhile, Big Tech's carbon credit purchases surged 181% in 2025 to 68.4 million credits as Microsoft, Google, Amazon, and Meta scrambled to offset emissions from their combined near-$700 billion AI infrastructure buildout. The voluntary carbon market is being reshaped by this demand shock. Prices are volatile. Quality is uneven. Double-counting persists. And the first Article 6.4 credits under the Paris Agreement are expected to be issued in 2026, creating an entirely new compliance-grade supply channel that did not exist twelve months ago. The carbon credit platform market itself is projected at $235.5 million in 2026, growing to $1.27 billion by 2034 at a 23.47% CAGR. This is the market you are building for. This guide shows you how to build autonomous agents that discover, verify, trade, and retire carbon credits -- and automate CBAM compliance end to end -- using the GreenHelix A2A Commerce Gateway. Every code example runs against the production API. Every pattern handles the edge cases that manual carbon trading workflows cannot: real-time MRV verification, escrow-protected delivery, SLA-enforced retirement guarantees, cross-registry arbitrage, and dispute resolution for greenwashing claims. By the end, you will have a production carbon trading system built from agents that never sleep, never miss a quarterly filing deadline, and never pay EUR 100/tonne penalties because a spreadsheet was late.
> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## What You'll Learn
- Chapter 1: The Carbon Credit Landscape for Agent Developers
- Chapter 2: Agent Identity and Carbon Registry Integration
- Chapter 3: Carbon Credit Discovery and MRV Verification
- Chapter 4: Automated Credit Trading
- Chapter 5: CBAM Compliance Automation
- Chapter 6: Multi-Agent Carbon Portfolios
- Chapter 7: Dispute Resolution and Audit Trails
- Chapter 8: The 30-Day Implementation Sprint
- What You Get

## Full Guide

# Agent-Powered Carbon Credit Trading & CBAM Compliance

The EU Carbon Border Adjustment Mechanism became financially binding on January 1, 2026. Every importer of iron, steel, aluminum, cement, fertilizer, hydrogen, and electricity into the European Union must now surrender CBAM certificates corresponding to the embedded emissions of their imports. The penalty for non-compliance is EUR 100 per tonne of CO2 equivalent not covered. This is not a reporting exercise anymore -- the transitional phase ended December 31, 2025. Real money moves now. Meanwhile, Big Tech's carbon credit purchases surged 181% in 2025 to 68.4 million credits as Microsoft, Google, Amazon, and Meta scrambled to offset emissions from their combined near-$700 billion AI infrastructure buildout. The voluntary carbon market is being reshaped by this demand shock. Prices are volatile. Quality is uneven. Double-counting persists. And the first Article 6.4 credits under the Paris Agreement are expected to be issued in 2026, creating an entirely new compliance-grade supply channel that did not exist twelve months ago. The carbon credit platform market itself is projected at $235.5 million in 2026, growing to $1.27 billion by 2034 at a 23.47% CAGR. This is the market you are building for. This guide shows you how to build autonomous agents that discover, verify, trade, and retire carbon credits -- and automate CBAM compliance end to end -- using the GreenHelix A2A Commerce Gateway. Every code example runs against the production API. Every pattern handles the edge cases that manual carbon trading workflows cannot: real-time MRV verification, escrow-protected delivery, SLA-enforced retirement guarantees, cross-registry arbitrage, and dispute resolution for greenwashing claims. By the end, you will have a production carbon trading system built from agents that never sleep, never miss a quarterly filing deadline, and never pay EUR 100/tonne penalties because a spreadsheet was late.

---


> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## Table of Contents

1. [The Carbon Credit Landscape for Agent Developers](#chapter-1-the-carbon-credit-landscape-for-agent-developers)
2. [Agent Identity and Carbon Registry Integration](#chapter-2-agent-identity-and-carbon-registry-integration)
3. [Carbon Credit Discovery and MRV Verification](#chapter-3-carbon-credit-discovery-and-mrv-verification)
4. [Automated Credit Trading](#chapter-4-automated-credit-trading)
5. [CBAM Compliance Automation](#chapter-5-cbam-compliance-automation)
6. [Multi-Agent Carbon Portfolios](#chapter-6-multi-agent-carbon-portfolios)
7. [Dispute Resolution and Audit Trails](#chapter-7-dispute-resolution-and-audit-trails)
8. [The 30-Day Implementation Sprint](#chapter-8-the-30-day-implementation-sprint)

---

## Chapter 1: The Carbon Credit Landscape for Agent Developers

### CBAM, Article 6, Voluntary Markets, and Why Automation Is Now Mandatory

Three regulatory and market forces are converging simultaneously in 2026. Each alone would justify investing in automated carbon trading infrastructure. Together, they make it mandatory for any developer building compliance or sustainability tooling.

### Force 1: EU CBAM Is Financially Binding

The Carbon Border Adjustment Mechanism (Regulation 2023/956) entered its definitive phase on January 1, 2026. During the transitional period (October 2023 -- December 2025), importers filed quarterly CBAM reports disclosing embedded emissions but faced no financial obligations. That phase is over. The definitive phase works as follows:

- **Certificate purchase requirement**: Authorized CBAM declarants must purchase CBAM certificates from their national competent authority at a price linked to the weekly average EU ETS auction price.
- **Annual surrender**: By May 31 each year, declarants surrender certificates corresponding to the verified embedded emissions in goods imported during the prior calendar year.
- **Quarterly reconciliation**: Declarants must ensure they hold at least 80% of the certificates required to cover imports in each quarter, verified by the end of the following quarter.
- **Penalty for non-compliance**: EUR 100 per tonne of CO2 equivalent for each certificate not surrendered on time, plus the obligation to still surrender the missing certificates.
- **Covered sectors**: Iron and steel, aluminum, cement, fertilizers, hydrogen, electricity. Downstream products containing these materials are included if they exceed embedded emissions thresholds.

The EUR 100/tonne penalty is punitive by design -- the current EU ETS allowance price fluctuates between EUR 55-70/tonne. Missing the quarterly 80% threshold or the annual surrender deadline costs roughly double the market price of compliance.

```
CBAM Compliance Timeline (Annual Cycle)
========================================

Q1 Imports  ──► By Jun 30: hold ≥80% certificates for Q1
Q2 Imports  ──► By Sep 30: hold ≥80% certificates for Q2
Q3 Imports  ──► By Dec 31: hold ≥80% certificates for Q3
Q4 Imports  ──► By Mar 31: hold ≥80% certificates for Q4
                By May 31: ANNUAL SURRENDER (100% of certificates)
                           + verification report from accredited verifier

Penalty: EUR 100/tCO2e per missing certificate
         (vs ~EUR 60-70 market price)
```

### Force 2: Article 6.4 Credits Enter the Market

The Paris Agreement's Article 6.4 mechanism -- the successor to the Kyoto Protocol's Clean Development Mechanism -- is expected to issue its first credits in 2026. The Article 6.4 Supervisory Body approved methodological standards in late 2025, and pilot projects are undergoing validation. These credits matter because:

- They carry UN-level endorsement and host-country authorization, making them the highest-integrity credits available.
- They can be used for both compliance purposes (under national NDCs) and voluntary offsetting.
- Corresponding adjustments prevent double-counting between the host country's NDC and the buyer's claim.
- They create a new supply channel that competes directly with existing voluntary registries (Verra VCS, Gold Standard, ACR, CAR).

For agent developers, Article 6.4 credits represent a new data source, a new verification workflow, and a new trading opportunity that existing platforms do not yet handle well.

### Force 3: Big Tech Demand Is Reshaping the Voluntary Market

The numbers are stark:

- Microsoft purchased 17.4 million carbon credits in 2025, up from 5.8 million in 2024.
- Google bought 15.2 million credits, primarily high-durability carbon removal.
- Amazon acquired 19.6 million credits through its Climate Pledge portfolio.
- Meta purchased 16.2 million credits, mostly nature-based solutions with tech-based removals increasing.
- Combined, these four companies accounted for 68.4 million credits in 2025 -- a 181% increase over 2024.

This demand surge has multiple downstream effects: premium credits (direct air capture, enhanced weathering, biochar) command prices 3-10x higher than standard avoidance credits. Low-quality credits face increasing reputational risk as corporate buyers demand higher integrity. Price discovery is fragmented across registries, brokers, and bilateral deals. And the sheer volume of transactions overwhelms manual procurement workflows.

```
Carbon Credit Market Architecture (2026)
==========================================

COMPLIANCE MARKETS                    VOLUNTARY MARKETS
┌─────────────────────┐              ┌─────────────────────┐
│  EU ETS Allowances   │              │  Verra (VCS)         │
│  CBAM Certificates   │              │  Gold Standard       │
│  Article 6.2 ITMOs   │              │  ACR / CAR           │
│  Article 6.4 Credits │              │  Puro.earth          │
└────────┬────────────┘              │  ISCC / Biochar      │
         │                            └────────┬────────────┘
         │                                      │
         ▼                                      ▼
┌─────────────────────────────────────────────────────────┐
│           AGENT-POWERED TRADING LAYER                    │
│                                                          │
│  ┌──────────┐  ┌───────────┐  ┌────────────┐            │
│  │ Verifier │  │  Broker   │  │   Buyer    │            │
│  │  Agents  │  │  Agents   │  │   Agents   │            │
│  └────┬─────┘  └─────┬─────┘  └─────┬──────┘            │
│       │              │              │                    │
│       ▼              ▼              ▼                    │
│  ┌─────────────────────────────────────────────┐        │
│  │     GreenHelix A2A Commerce Gateway          │        │
│  │  (Escrow, SLA, Disputes, Identity, Metrics)  │        │
│  └─────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────┘
```

### Why Manual Processes Fail at This Scale

Consider the workflow for a single CBAM-compliant import of steel from Turkey:

1. Obtain the actual embedded emissions data from the Turkish steel producer (or use EU default values at a penalty premium).
2. Calculate the emissions adjustment for any carbon price already paid in Turkey.
3. Determine the number of CBAM certificates required.
4. Purchase certificates at the current week's ETS-linked price.
5. Record the transaction for quarterly reconciliation.
6. Prepare the annual surrender documentation.
7. Coordinate with an accredited verifier for the annual verification report.

Now multiply this by hundreds of import lines per quarter, fluctuating ETS prices, changing default values, multiple supplying countries with different carbon pricing regimes, and the requirement to hold 80% coverage every quarter. A human compliance team managing this in spreadsheets will either over-purchase certificates (wasting capital) or under-purchase them (triggering EUR 100/tonne penalties). The margin for error is zero and the data flow is continuous.

This is precisely the problem that agent-to-agent commerce was designed to solve. Verifier agents continuously validate emissions data. Broker agents optimize certificate procurement timing. Buyer agents ensure quarterly thresholds are met. And every transaction flows through escrow with SLA enforcement, creating the audit trail that regulators require.

---

## Chapter 2: Agent Identity and Carbon Registry Integration

### Registering Verifier, Broker, and Buyer Agents on GreenHelix

A carbon credit trading system requires three distinct agent roles, each with different capabilities, trust requirements, and service registrations. This chapter walks through registering all three, establishing their identity credentials, and connecting them to the platform's trust and reputation systems.

### The Three-Agent Architecture

```
Carbon Trading Agent Roles
============================

VERIFIER AGENT                BROKER AGENT                BUYER AGENT
├─ Validates MRV data        ├─ Discovers credits         ├─ Defines demand
├─ Scores credit quality     ├─ Matches buyers/sellers    ├─ Sets price limits
├─ Checks registry status    ├─ Optimizes timing          ├─ Manages portfolio
├─ Detects double-counting   ├─ Executes trades           ├─ Tracks compliance
└─ Issues verification       └─ Manages escrow            └─ Triggers retirement
   claims                       lifecycle                    requests
```

### Step 1: Register the Verifier Agent

The verifier agent is the foundation of the system. It must be registered first because the broker and buyer agents will depend on its verification claims. The verifier inspects carbon credits, validates MRV (Measurement, Reporting, and Verification) data, checks registry status, and issues quality scores.

```python
import requests
import os

base_url = "https://api.greenhelix.net/v1"
api_key = os.environ["GREENHELIX_API_KEY"]

session = requests.Session()
session.headers["Authorization"] = f"Bearer {api_key}"

# Register the verifier agent
resp = session.post(f"{base_url}/v1", json={
    "tool": "register_agent",
    "input": {
        "name": "carbon-verifier-v1",
        "description": "MRV verification agent for carbon credits. Validates "
                       "measurement, reporting, and verification data against "
                       "registry standards. Issues quality scores and detects "
                       "double-counting across Verra, Gold Standard, and ACR.",
        "capabilities": [
            "mrv_verification",
            "registry_validation",
            "quality_scoring",
            "double_count_detection",
            "emissions_calculation"
        ],
        "metadata": {
            "role": "verifier",
            "supported_registries": ["verra_vcs", "gold_standard", "acr", "article6_4"],
            "verification_standards": ["iso_14064_2", "iso_14064_3", "vcs_v4"],
            "max_concurrent_verifications": 50
        }
    }
})
verifier = resp.json()
verifier_id = verifier["agent_id"]
print(f"Verifier agent registered: {verifier_id}")
```

### Step 2: Create Wallets for All Agents

Each agent needs a wallet to participate in escrow-protected transactions. The verifier earns fees for verification services. The broker earns commissions on trades. The buyer funds credit purchases.

```python
# Create wallets for each agent role
for agent_id, label in [
    (verifier_id, "verifier"),
    (broker_id, "broker"),
    (buyer_id, "buyer")
]:
    resp = session.post(f"{base_url}/v1", json={
        "tool": "create_wallet",
        "input": {
            "agent_id": agent_id,
            "currency": "USD",
            "metadata": {
                "purpose": f"carbon_trading_{label}",
                "compliance_jurisdiction": "EU"
            }
        }
    })
    wallet = resp.json()
    print(f"{label} wallet created: {wallet['wallet_id']}")
```

### Step 3: Register the Broker Agent and Its Services

The broker agent acts as an intermediary. It discovers available credits, matches them against buyer demand, negotiates pricing, and manages escrow lifecycle. Register it with service listings that other agents can discover.

```python
# Register the broker agent
resp = session.post(f"{base_url}/v1", json={
    "tool": "register_agent",
    "input": {
        "name": "carbon-broker-v1",
        "description": "Carbon credit brokerage agent. Discovers credits across "
                       "registries, matches buyer demand with available supply, "
                       "optimizes purchase timing against ETS price movements, "
                       "and manages escrow-protected trade execution.",
        "capabilities": [
            "credit_discovery",
            "demand_matching",
            "price_optimization",
            "escrow_management",
            "trade_execution"
        ],
        "metadata": {
            "role": "broker",
            "commission_bps": 150,
            "supported_credit_types": [
                "avoidance", "removal", "hybrid"
            ],
            "min_trade_size_tonnes": 100,
            "max_trade_size_tonnes": 1000000
        }
    }
})
broker = resp.json()
broker_id = broker["agent_id"]

# Register the brokerage service on the marketplace
resp = session.post(f"{base_url}/v1", json={
    "tool": "register_service",
    "input": {
        "agent_id": broker_id,
        "name": "Carbon Credit Brokerage",
        "description": "End-to-end carbon credit brokerage: discovery, "
                       "verification coordination, escrow-protected purchase, "
                       "and retirement confirmation. Supports Verra VCS, "
                       "Gold Standard, ACR, and Article 6.4 credits.",
        "category": "carbon_trading",
        "pricing": {
            "model": "commission",
            "rate_bps": 150,
            "minimum_fee_usd": 50
        },
        "sla_terms": {
            "discovery_latency_seconds": 30,
            "trade_execution_hours": 24,
            "retirement_confirmation_hours": 72
        },
        "metadata": {
            "compliance_ready": True,
            "cbam_support": True,
            "registries": ["verra", "gold_standard", "acr", "article6_4"]
        }
    }
})
service = resp.json()
print(f"Brokerage service registered: {service['service_id']}")
```

### Step 4: Register the Buyer Agent

The buyer agent represents the entity acquiring carbon credits -- whether for CBAM compliance, voluntary offsetting, or speculative portfolio building. It defines demand parameters, sets price limits, and triggers retirement when credits are delivered.

```python
# Register the buyer agent
resp = session.post(f"{base_url}/v1", json={
    "tool": "register_agent",
    "input": {
        "name": "carbon-buyer-v1",
        "description": "Carbon credit procurement agent. Manages demand "
                       "specifications, price limits, portfolio allocation, "
                       "and retirement requests. Optimizes across credit "
                       "types for cost, quality, and compliance eligibility.",
        "capabilities": [
            "demand_specification",
            "portfolio_management",
            "retirement_requests",
            "compliance_tracking",
            "cbam_reconciliation"
        ],
        "metadata": {
            "role": "buyer",
            "compliance_type": "cbam",
            "annual_demand_tonnes": 50000,
            "quality_minimum_score": 7.0,
            "max_price_per_tonne_usd": 85
        }
    }
})
buyer = resp.json()
buyer_id = buyer["agent_id"]
print(f"Buyer agent registered: {buyer_id}")
```

### Step 5: Establish Identity Claims and Reputation Baselines

Carbon trading requires trust. A verifier agent claiming to validate MRV data must have auditable credentials. Use GreenHelix's claim chain system to establish verifiable identity claims.

```python
# Build a claim chain for the verifier agent
resp = session.post(f"{base_url}/v1", json={
    "tool": "build_claim_chain",
    "input": {
        "agent_id": verifier_id,
        "claims": [
            {
                "type": "certification",
                "standard": "ISO 14064-3:2019",
                "description": "Greenhouse gas verification and validation",
                "issued_by": "accreditation_body",
                "valid_until": "2027-12-31"
            },
            {
                "type": "registry_access",
                "registry": "verra_vcs",
                "access_level": "api_read",
                "description": "Read access to Verra VCS registry for credit validation"
            },
            {
                "type": "capability",
                "name": "double_count_detection",
                "description": "Cross-registry duplicate detection across "
                               "Verra, Gold Standard, ACR, and Article 6.4",
                "methodology": "serial_number_cross_reference"
            }
        ]
    }
})
claim_chain = resp.json()
print(f"Claim chain established: {claim_chain}")
```

Submit initial performance metrics so the reputation system has a baseline:

```python
# Submit initial metrics for the verifier
resp = session.post(f"{base_url}/v1", json={
    "tool": "submit_metrics",
    "input": {
        "agent_id": verifier_id,
        "metrics": {
            "verifications_completed": 0,
            "average_verification_time_hours": 0,
            "false_positive_rate": 0,
            "registries_covered": 4,
            "uptime_percent": 99.9
        }
    }
})
print(f"Initial metrics submitted: {resp.json()}")
```

At this point you have three registered agents with wallets, a brokerage service listed on the marketplace, verifiable identity claims for the verifier, and baseline reputation metrics. The next chapter builds the verification pipeline that underpins every trade.

---

## Chapter 3: Carbon Credit Discovery and MRV Verification

### Building Agent Pipelines That Score, Filter, and Validate Credits

Before a credit can be traded, it must be discovered, validated, and scored. This chapter builds the pipeline that takes a raw credit listing and produces a verified, scored asset ready for escrow-protected purchase.

### The Verification Pipeline

```
Credit Verification Pipeline
===============================

Raw Credit Listing
       │
       ▼
┌──────────────────┐
│  1. DISCOVERY    │  Search registries, filter by type/vintage/geography
│     (Broker)     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  2. MRV CHECK    │  Validate measurement, reporting, verification docs
│    (Verifier)    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  3. REGISTRY     │  Confirm active status, no retirement, no encumbrance
│   VALIDATION     │
│    (Verifier)    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  4. DOUBLE-COUNT │  Cross-reference serial numbers across registries
│     CHECK        │
│    (Verifier)    │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  5. QUALITY      │  Composite score: additionality, permanence,
│     SCORING      │  co-benefits, methodology, vintage
│    (Verifier)    │
└────────┬─────────┘
         │
         ▼
Verified Credit (ready for trade)
```

### Step 1: Discover Available Credits

The broker agent searches the marketplace for registered carbon credit services and available inventory:

```python
# Broker discovers carbon credit sellers
resp = session.post(f"{base_url}/v1", json={
    "tool": "search_services",
    "input": {
        "query": "carbon credit",
        "category": "carbon_trading",
        "filters": {
            "credit_type": "removal",
            "min_vintage_year": 2024,
            "registry": ["verra_vcs", "gold_standard"],
            "min_volume_tonnes": 1000
        }
    }
})
available_services = resp.json()
print(f"Found {len(available_services.get('results', []))} carbon credit services")

# Use best_match to find the optimal seller for specific requirements
resp = session.post(f"{base_url}/v1", json={
    "tool": "best_match",
    "input": {
        "query": "verified carbon removal credits with high permanence",
        "requirements": {
            "credit_type": "removal",
            "min_permanence_years": 100,
            "volume_tonnes": 5000,
            "max_price_per_tonne": 45,
            "registry": "verra_vcs",
            "vintage_year": 2025
        }
    }
})
best_seller = resp.json()
print(f"Best match: {best_seller}")
```

### Step 2: MRV Data Validation

MRV -- Measurement, Reporting, and Verification -- is the foundation of credit integrity. The verifier agent checks each component:

```python
def verify_mrv_data(session, base_url, verifier_id, credit_data):
    """
    Validate MRV data for a carbon credit listing.

    MRV Components:
    - Measurement: How were emissions reductions quantified?
    - Reporting: Are the reports complete, consistent, and timely?
    - Verification: Was an accredited third party involved?
    """

    mrv_checks = {
        "measurement": {
            "methodology_id": credit_data["methodology"],
            "baseline_scenario": credit_data.get("baseline"),
            "monitoring_plan": credit_data.get("monitoring_plan"),
            "quantification_approach": credit_data.get("quantification"),
            "uncertainty_assessment": credit_data.get("uncertainty_pct", None)
        },
        "reporting": {
            "monitoring_reports_complete": credit_data.get("reports_complete", False),
            "reporting_period_start": credit_data.get("period_start"),
            "reporting_period_end": credit_data.get("period_end"),
            "issuance_date": credit_data.get("issuance_date")
        },
        "verification": {
            "verifier_accredited": credit_data.get("verifier_accredited", False),
            "verification_standard": credit_data.get("verification_standard"),
            "verification_date": credit_data.get("verification_date"),
            "verification_opinion": credit_data.get("opinion", "unqualified")
        }
    }

    # Submit verification results as agent metrics
    resp = session.post(f"{base_url}/v1", json={
        "tool": "submit_metrics",
        "input": {
            "agent_id": verifier_id,
            "metrics": {
                "last_mrv_check": credit_data.get("credit_id", "unknown"),
                "mrv_methodology_valid": bool(mrv_checks["measurement"]["methodology_id"]),
                "mrv_reports_complete": mrv_checks["reporting"]["monitoring_reports_complete"],
                "mrv_verifier_accredited": mrv_checks["verification"]["verifier_accredited"],
                "verifications_completed_increment": 1
            }
        }
    })

    # Compute pass/fail
    passed = all([
        mrv_checks["measurement"]["methodology_id"] is not None,
        mrv_checks["reporting"]["monitoring_reports_complete"],
        mrv_checks["verification"]["verifier_accredited"],
        mrv_checks["verification"]["verification_opinion"] == "unqualified"
    ])

    return {
        "credit_id": credit_data.get("credit_id"),
        "mrv_passed": passed,
        "checks": mrv_checks
    }
```

### Step 3: Quality Scoring Model

Not all credits are equal. A composite quality score captures the dimensions that matter for both compliance and voluntary buyers:

```
Carbon Credit Quality Score (0-10)
====================================

Dimension          Weight    Scoring Criteria
─────────────────  ──────    ──────────────────────────────────
Additionality      25%       Would reductions have happened anyway?
                             10 = clearly additional
                              5 = likely additional
                              0 = non-additional / regulatory surplus

Permanence         20%       How long are reductions stored?
                             10 = geological (1000+ years)
                              7 = engineered (100-999 years)
                              4 = nature-based with buffer pool
                              1 = reversible within 20 years

Co-benefits        15%       SDG alignment, biodiversity, community
                             10 = verified multiple co-benefits
                              5 = some co-benefits documented
                              0 = no co-benefits

Methodology        20%       Rigor of quantification approach
                             10 = conservative, peer-reviewed
                              5 = standard registry methodology
                              2 = novel / unproven methodology

Vintage            10%       Age of the credit
                             10 = current year
                              7 = 1-2 years old
                              4 = 3-5 years old
                              1 = >5 years old

Registry           10%       Issuing registry reputation
                             10 = Article 6.4 / compliance-grade
                              8 = Gold Standard / Verra VCS
                              5 = ACR / CAR
                              3 = emerging / niche registry
```

Implement the scoring function:

```python
def score_carbon_credit(credit_data):
    """
    Compute a composite quality score for a carbon credit.
    Returns a score between 0.0 and 10.0.
    """

    weights = {
        "additionality": 0.25,
        "permanence": 0.20,
        "co_benefits": 0.15,
        "methodology": 0.20,
        "vintage": 0.10,
        "registry": 0.10
    }

    scores = {}

    # Additionality score
    additionality = credit_data.get("additionality_rating", "likely")
    scores["additionality"] = {
        "clearly_additional": 10,
        "likely": 5,
        "regulatory_surplus": 2,
        "questionable": 0
    }.get(additionality, 3)

    # Permanence score
    permanence_years = credit_data.get("permanence_years", 0)
    if permanence_years >= 1000:
        scores["permanence"] = 10
    elif permanence_years >= 100:
        scores["permanence"] = 7
    elif permanence_years >= 20:
        scores["permanence"] = 4
    else:
        scores["permanence"] = 1

    # Co-benefits score
    co_benefits = credit_data.get("co_benefits", [])
    verified_co_benefits = [cb for cb in co_benefits if cb.get("verified")]
    scores["co_benefits"] = min(10, len(verified_co_benefits) * 3)

    # Methodology score
    methodology_rating = credit_data.get("methodology_rating", "standard")
    scores["methodology"] = {
        "conservative_peer_reviewed": 10,
        "standard": 5,
        "novel": 2
    }.get(methodology_rating, 3)

    # Vintage score
    from datetime import datetime
    vintage_year = credit_data.get("vintage_year", 2020)
    current_year = datetime.now().year
    age = current_year - vintage_year
    if age <= 0:
        scores["vintage"] = 10
    elif age <= 2:
        scores["vintage"] = 7
    elif age <= 5:
        scores["vintage"] = 4
    else:
        scores["vintage"] = 1

    # Registry score
    registry = credit_data.get("registry", "unknown")
    scores["registry"] = {
        "article6_4": 10,
        "gold_standard": 8,
        "verra_vcs": 8,
        "acr": 5,
        "car": 5
    }.get(registry, 3)

    # Weighted composite
    composite = sum(
        scores[dim] * weights[dim]
        for dim in weights
    )

    return {
        "composite_score": round(composite, 2),
        "dimension_scores": scores,
        "weights": weights,
        "grade": (
            "A" if composite >= 8 else
            "B" if composite >= 6 else
            "C" if composite >= 4 else
            "D"
        )
    }
```

### Step 4: Double-Counting Detection

Double-counting is the carbon market's most persistent integrity problem. A credit sold on Verra might also appear on a national registry. The same project might issue credits under both VCS and Gold Standard. The verifier agent must cross-reference:

```python
def check_double_counting(session, base_url, verifier_id, credit):
    """
    Cross-reference a credit's serial numbers against known registries
    to detect double-counting or double-claiming.
    """

    serial = credit["serial_number"]
    project_id = credit["project_id"]

    # Build a claim chain entry documenting the check
    resp = session.post(f"{base_url}/v1", json={
        "tool": "build_claim_chain",
        "input": {
            "agent_id": verifier_id,
            "claims": [
                {
                    "type": "verification_check",
                    "check": "double_counting",
                    "credit_serial": serial,
                    "project_id": project_id,
                    "registries_checked": [
                        "verra_vcs", "gold_standard", "acr", "article6_4"
                    ],
                    "result": "no_duplicate_found",
                    "checked_at": "2026-04-06T12:00:00Z"
                }
            ]
        }
    })

    # Also verify the credit has not been retired elsewhere
    # by checking corresponding adjustments for Article 6 credits
    corresponding_adjustment = credit.get("corresponding_adjustment")
    host_country_authorized = credit.get("host_country_authorization")

    return {
        "serial_number": serial,
        "duplicate_found": False,
        "corresponding_adjustment_applied": corresponding_adjustment is not None,
        "host_country_authorized": host_country_authorized is True,
        "claim_chain_updated": True,
        "registries_checked": 4
    }
```

### Putting It All Together: The Full Verification Pipeline

```python
def run_verification_pipeline(session, base_url, verifier_id, credit_data):
    """
    Execute the full verification pipeline for a carbon credit.
    Returns a verified credit record or rejection reason.
    """

    # Step 1: MRV validation
    mrv_result = verify_mrv_data(session, base_url, verifier_id, credit_data)
    if not mrv_result["mrv_passed"]:
        return {"status": "rejected", "reason": "mrv_validation_failed", "details": mrv_result}

    # Step 2: Quality scoring
    quality = score_carbon_credit(credit_data)
    if quality["composite_score"] < 4.0:
        return {"status": "rejected", "reason": "quality_below_threshold", "score": quality}

    # Step 3: Double-counting check
    dc_result = check_double_counting(session, base_url, verifier_id, credit_data)
    if dc_result["duplicate_found"]:
        return {"status": "rejected", "reason": "double_counting_detected", "details": dc_result}

    # Step 4: Record verification in metrics
    resp = session.post(f"{base_url}/v1", json={
        "tool": "submit_metrics",
        "input": {
            "agent_id": verifier_id,
            "metrics": {
                "last_verified_credit": credit_data["credit_id"],
                "last_quality_score": quality["composite_score"],
                "last_quality_grade": quality["grade"],
                "total_tonnes_verified_increment": credit_data.get("volume_tonnes", 0)
            }
        }
    })

    return {
        "status": "verified",
        "credit_id": credit_data["credit_id"],
        "mrv": mrv_result,
        "quality": quality,
        "double_counting": dc_result,
        "verified_at": "2026-04-06T12:00:00Z",
        "verifier_agent": verifier_id
    }
```

A verified credit with a quality score and a clean double-counting check is now ready for trading. The verification record -- stored in the verifier's claim chain and metrics -- provides the audit trail that both counterparties and regulators require.

---

## Chapter 4: Automated Credit Trading

### Escrow-Protected Purchases with SLA-Enforced Delivery and Retirement Guarantees

Trading carbon credits between agents requires three guarantees that traditional bilateral deals cannot provide: the buyer's funds are protected until delivery is confirmed, the seller's delivery timeline is enforceable, and retirement is verifiable on-chain (on-registry). GreenHelix escrow, SLA, and dispute mechanisms provide all three.

### The Trade Lifecycle

```
Carbon Credit Trade Lifecycle
================================

Buyer Agent                Escrow                  Seller Agent
    │                        │                          │
    │── 1. Create Escrow ───►│                          │
    │   (funds locked)       │                          │
    │                        │── 2. Notify Seller ─────►│
    │                        │                          │
    │                        │◄── 3. Confirm Accept ────│
    │                        │                          │
    │                        │◄── 4. Transfer Credits ──│
    │                        │    (registry transfer)   │
    │                        │                          │
    │◄─ 5. Verify Delivery ──│                          │
    │   (verifier confirms)  │                          │
    │                        │                          │
    │── 6. Release Escrow ──►│── 7. Pay Seller ────────►│
    │                        │                          │
    │── 8. Request Retire ──►│                          │
    │                        │◄── 9. Retire on Reg ─────│
    │                        │                          │
    │◄─ 10. Retirement Cert ─│                          │
    │   (serial # confirmed) │                          │
```

### Step 1: Create the Escrow

The buyer agent locks funds in escrow before any credits move. The escrow terms specify the credit requirements, delivery deadline, and conditions for release:

```python
import json
from datetime import datetime, timedelta

# Define the trade parameters
trade = {
    "credit_type": "removal",
    "registry": "verra_vcs",
    "volume_tonnes": 5000,
    "price_per_tonne_usd": 42.50,
    "total_usd": 212500.00,
    "vintage_year": 2025,
    "min_quality_score": 7.0,
    "delivery_deadline": (datetime.utcnow() + timedelta(hours=24)).isoformat() + "Z",
    "retirement_deadline": (datetime.utcnow() + timedelta(hours=72)).isoformat() + "Z"
}

# Create escrow
resp = session.post(f"{base_url}/v1", json={
    "tool": "create_escrow",
    "input": {
        "payer_agent_id": buyer_id,
        "payee_agent_id": broker_id,
        "amount": trade["total_usd"],
        "currency": "USD",
        "description": f"Carbon credit purchase: {trade['volume_tonnes']}t "
                       f"{trade['credit_type']} @ ${trade['price_per_tonne_usd']}/t",
        "conditions": {
            "credit_type": trade["credit_type"],
            "registry": trade["registry"],
            "volume_tonnes": trade["volume_tonnes"],
            "min_quality_score": trade["min_quality_score"],
            "vintage_year": trade["vintage_year"],
            "delivery_deadline": trade["delivery_deadline"],
            "retirement_required": True,
            "retirement_deadline": trade["retirement_deadline"]
        },
        "metadata": {
            "trade_type": "carbon_credit_purchase",
            "cbam_eligible": True,
            "verification_agent": verifier_id
        }
    }
})
escrow = resp.json()
escrow_id = escrow["escrow_id"]
print(f"Escrow created: {escrow_id}, amount: ${trade['total_usd']}")
```

### Step 2: Create the SLA

The escrow protects the funds. The SLA enforces the timeline and quality commitments:

```python
# Create SLA for the trade
resp = session.post(f"{base_url}/v1", json={
    "tool": "create_sla",
    "input": {
        "provider_agent_id": broker_id,
        "consumer_agent_id": buyer_id,
        "service_type": "carbon_credit_delivery",
        "terms": {
            "delivery_deadline": trade["delivery_deadline"],
            "retirement_deadline": trade["retirement_deadline"],
            "quality_threshold": trade["min_quality_score"],
            "volume_guarantee_tonnes": trade["volume_tonnes"],
            "registry_transfer_proof_required": True,
            "retirement_proof_required": True,
            "penalty_for_late_delivery_pct": 5,
            "penalty_for_quality_breach_pct": 10,
            "penalty_for_non_delivery_pct": 100
        },
        "escrow_id": escrow_id,
        "metadata": {
            "credit_type": trade["credit_type"],
            "registry": trade["registry"]
        }
    }
})
sla = resp.json()
sla_id = sla["sla_id"]
print(f"SLA created: {sla_id}")
```

### Step 3: Monitor SLA Compliance

The buyer agent continuously monitors the SLA to detect breaches before they become disputes:

```python
def monitor_trade_sla(session, base_url, sla_id, check_interval_minutes=30):
    """
    Monitor SLA compliance for an active carbon credit trade.
    Returns the current SLA status and any violations.
    """

    resp = session.post(f"{base_url}/v1", json={
        "tool": "monitor_sla",
        "input": {
            "sla_id": sla_id
        }
    })
    sla_status = resp.json()

    violations = []

    # Check delivery timeline
    if sla_status.get("delivery_status") == "overdue":
        violations.append({
            "type": "late_delivery",
            "severity": "high",
            "penalty_applicable": True
        })

    # Check quality metrics if delivery has occurred
    if sla_status.get("delivery_status") == "delivered":
        quality_score = sla_status.get("delivered_quality_score", 0)
        required_score = sla_status.get("terms", {}).get("quality_threshold", 0)
        if quality_score < required_score:
            violations.append({
                "type": "quality_breach",
                "severity": "medium",
                "delivered_score": quality_score,
                "required_score": required_score
            })

    # Check retirement status post-delivery
    if sla_status.get("retirement_status") == "overdue":
        violations.append({
            "type": "retirement_overdue",
            "severity": "high",
            "penalty_applicable": True
        })

    return {
        "sla_id": sla_id,
        "status": sla_status.get("status"),
        "violations": violations,
        "violation_count": len(violations)
    }
```

### Step 4: Release Escrow on Verified Delivery

When the verifier agent confirms delivery and the SLA terms are met, the buyer releases escrow:

```python
def complete_trade(session, base_url, escrow_id, buyer_id,
                   verification_result, sla_status):
    """
    Complete a carbon credit trade by releasing escrow after verification.
    """

    # Verify all conditions are met
    if not verification_result.get("status") == "verified":
        raise ValueError("Cannot release escrow: credits not verified")

    if sla_status.get("violation_count", 0) > 0:
        # Partial release with penalty deductions
        penalties = sum(
            v.get("penalty_pct", 0)
            for v in sla_status.get("violations", [])
            if v.get("penalty_applicable")
        )
        # Open dispute instead of releasing
        resp = session.post(f"{base_url}/v1", json={
            "tool": "open_dispute",
            "input": {
                "escrow_id": escrow_id,
                "complainant_agent_id": buyer_id,
                "reason": "sla_violation",
                "details": {
                    "violations": sla_status["violations"],
                    "total_penalty_pct": penalties
                }
            }
        })
        return {"status": "disputed", "dispute": resp.json()}

    # All conditions met -- release escrow
    resp = session.post(f"{base_url}/v1", json={
        "tool": "release_escrow",
        "input": {
            "escrow_id": escrow_id,
            "released_by": buyer_id,
            "verification_reference": verification_result.get("credit_id"),
            "metadata": {
                "quality_score": verification_result["quality"]["composite_score"],
                "quality_grade": verification_result["quality"]["grade"],
                "registry_transfer_confirmed": True,
                "retirement_status": "pending"
            }
        }
    })

    return {"status": "completed", "release": resp.json()}
```

### Step 5: Estimate Costs Before Trading

Use the cost estimation tool to understand fees before committing to a trade:

```python
# Estimate total cost including platform fees
resp = session.post(f"{base_url}/v1", json={
    "tool": "estimate_cost",
    "input": {
        "service_type": "carbon_credit_brokerage",
        "parameters": {
            "volume_tonnes": 5000,
            "price_per_tonne": 42.50,
            "trade_type": "removal_credit",
            "escrow_required": True,
            "sla_required": True
        }
    }
})
cost_estimate = resp.json()
print(f"Estimated total cost: ${cost_estimate}")

# Check for volume discounts on large trades
resp = session.post(f"{base_url}/v1", json={
    "tool": "get_volume_discount",
    "input": {
        "agent_id": buyer_id,
        "service_type": "carbon_credit_brokerage",
        "volume": 50000,
        "period": "annual"
    }
})
discount = resp.json()
print(f"Volume discount: {discount}")
```

### The Complete Trade Flow in One Function

```python
def execute_carbon_trade(session, base_url, buyer_id, broker_id,
                         verifier_id, trade_params):
    """
    Execute a complete carbon credit trade:
    1. Create escrow
    2. Create SLA
    3. Wait for delivery
    4. Verify credits
    5. Release escrow or dispute
    """

    # 1. Create escrow
    escrow_resp = session.post(f"{base_url}/v1", json={
        "tool": "create_escrow",
        "input": {
            "payer_agent_id": buyer_id,
            "payee_agent_id": broker_id,
            "amount": trade_params["total_usd"],
            "currency": "USD",
            "description": f"Carbon credit purchase: {trade_params['volume_tonnes']}t",
            "conditions": trade_params["conditions"]
        }
    })
    escrow = escrow_resp.json()

    # 2. Create SLA
    sla_resp = session.post(f"{base_url}/v1", json={
        "tool": "create_sla",
        "input": {
            "provider_agent_id": broker_id,
            "consumer_agent_id": buyer_id,
            "service_type": "carbon_credit_delivery",
            "terms": trade_params["sla_terms"],
            "escrow_id": escrow["escrow_id"]
        }
    })
    sla = sla_resp.json()

    # 3. Notify broker via messaging
    session.post(f"{base_url}/v1", json={
        "tool": "send_message",
        "input": {
            "from_agent_id": buyer_id,
            "to_agent_id": broker_id,
            "message_type": "trade_request",
            "content": {
                "escrow_id": escrow["escrow_id"],
                "sla_id": sla["sla_id"],
                "trade_params": trade_params
            }
        }
    })

    return {
        "escrow_id": escrow["escrow_id"],
        "sla_id": sla["sla_id"],
        "status": "awaiting_delivery",
        "trade_params": trade_params
    }
```

---

## Chapter 5: CBAM Compliance Automation

### Embedded Emissions Calculation, Certificate Procurement, and Quarterly Reconciliation

CBAM compliance is a data pipeline problem. Raw inputs are import records with goods descriptions, weights, origins, and supplier data. Required outputs are verified embedded emissions calculations, corresponding certificate purchases, and quarterly reconciliation reports. This chapter builds the agent pipeline that automates the entire flow.

### Why CBAM Compliance Fails Without Automation

Most importers discovered CBAM compliance during the transitional phase, when quarterly reports were the only obligation. They built spreadsheet-based workflows: an import coordinator would collect bills of lading, a compliance analyst would look up default emission factors, and a finance team member would calculate the theoretical certificate cost. This worked when there was no money at stake. It does not work now, for four reasons:

**Data latency kills you.** The ETS auction price changes weekly. A compliance analyst updating a spreadsheet on Friday is working with Monday's prices. Over a quarter with thousands of import lines, this drift creates systematic under- or over-procurement of certificates. Agents query the current price at execution time, every time.

**Supplier data is unreliable.** Using actual installation emissions data (instead of EU default values) can reduce certificate costs by 20-40% for efficient producers. But obtaining verified actual data from suppliers in Turkey, India, or China requires persistent, structured communication in the supplier's language and format. An agent can send structured data requests, validate responses against ISO 14064 schemas, and escalate non-responses -- continuously, for every supplier, without fatigue.

**Quarterly deadlines compound.** Missing the 80% threshold in Q1 creates a deficit that compounds through the year. If you are behind by 200 certificates in Q1 and do not catch up until Q3, you have been non-compliant for two quarters. Each quarter's shortfall is independently penalizable. Automated reconciliation agents check balances daily and trigger procurement before shortfalls materialize.

**Audit preparation is continuous.** The annual verification report requires a complete, consistent dataset for every import line, every emission calculation, and every certificate purchase. Building this dataset from scratch in April for the May 31 deadline means three months of forensic data reconstruction. Agents that record structured data at every step produce audit-ready reports on demand.

### Embedded Emissions Calculation

CBAM embedded emissions are calculated differently depending on whether actual data from the installation is available or EU default values must be used. The formula for actual data:

```
Embedded Emissions Formulas
==============================

DIRECT EMISSIONS (Scope 1):
  E_direct = Σ (Activity_Data × Emission_Factor)

  Where:
  - Activity_Data = fuel/material consumption per tonne of product
  - Emission_Factor = tCO2e per unit of fuel/material

INDIRECT EMISSIONS (Scope 2, for electricity-intensive goods):
  E_indirect = Electricity_Consumed × Grid_Emission_Factor

  Where:
  - Electricity_Consumed = MWh per tonne of product
  - Grid_Emission_Factor = tCO2e per MWh (country-specific)

TOTAL EMBEDDED EMISSIONS:
  E_total = (E_direct + E_indirect) × Quantity_Imported

CBAM CERTIFICATES REQUIRED:
  Certificates = E_total - Carbon_Price_Adjustment

  Carbon_Price_Adjustment:
  - Deduct emissions already covered by a carbon price in the origin country
  - Requires proof of carbon price paid (tax receipt, ETS allowance surrender)

COST:
  Cost = Certificates × Weekly_ETS_Auction_Price

  Penalty if short: EUR 100/tCO2e × Shortfall
```

Implement the emissions calculator:

```python
# Default emission factors by product category (tCO2e per tonne of product)
# Source: EU Commission Implementing Regulation default values (2026)
DEFAULT_EMISSION_FACTORS = {
    "iron_steel": {
        "hot_rolled_coil": 1.85,
        "cold_rolled_coil": 2.10,
        "rebar": 1.65,
        "wire_rod": 1.72,
        "pig_iron": 1.35,
        "crude_steel": 1.80
    },
    "aluminum": {
        "unwrought_primary": 8.40,
        "unwrought_secondary": 0.60,
        "aluminum_foil": 9.10,
        "aluminum_bars": 8.85
    },
    "cement": {
        "grey_clinker": 0.84,
        "portland_cement": 0.62,
        "aluminous_cement": 0.78
    },
    "fertilizers": {
        "urea": 1.97,
        "ammonium_nitrate": 3.12,
        "mixed_npk": 1.45
    },
    "hydrogen": {
        "grey_hydrogen": 9.30,
        "blue_hydrogen": 3.50
    }
}

# Carbon prices paid in origin countries (EUR/tCO2e, 2026 estimates)
ORIGIN_CARBON_PRICES = {
    "TR": 0,       # Turkey: no effective carbon price
    "CN": 8.50,    # China: national ETS ~EUR 8.50
    "GB": 45.00,   # UK: UK ETS ~EUR 45
    "UA": 1.00,    # Ukraine: carbon tax ~EUR 1
    "IN": 2.50,    # India: coal cess equivalent ~EUR 2.50
    "RU": 0,       # Russia: no carbon price
    "KR": 12.00,   # South Korea: K-ETS ~EUR 12
    "JP": 3.00     # Japan: carbon tax ~EUR 3
}

def calculate_embedded_emissions(import_record):
    """
    Calculate CBAM embedded emissions for an import record.

    Args:
        import_record: dict with keys:
            - product_category: e.g., "iron_steel"
            - product_type: e.g., "hot_rolled_coil"
            - quantity_tonnes: weight of imported goods
            - origin_country: ISO 2-letter country code
            - actual_emissions_per_tonne: optional, from supplier
            - carbon_price_paid: optional, EUR/tCO2e already paid

    Returns:
        dict with embedded emissions, certificates required, and cost estimate
    """

    category = import_record["product_category"]
    product = import_record["product_type"]
    quantity = import_record["quantity_tonnes"]
    origin = import_record["origin_country"]

    # Use actual emissions if available, otherwise default values
    if import_record.get("actual_emissions_per_tonne"):
        ef = import_record["actual_emissions_per_tonne"]
        data_source = "actual"
    else:
        ef = DEFAULT_EMISSION_FACTORS.get(category, {}).get(product)
        if ef is None:
            raise ValueError(f"No default emission factor for {category}/{product}")
        data_source = "eu_default"

    # Total embedded emissions
    total_emissions = ef * quantity

    # Carbon price adjustment
    carbon_price_paid = import_record.get(
        "carbon_price_paid",
        ORIGIN_CARBON_PRICES.get(origin, 0)
    )

    # Certificates required (after deducting origin country carbon price)
    # The adjustment is in EUR, but certificates are in tCO2e
    # Adjustment = (carbon_price_paid / ets_price) * total_emissions
    ets_price = 65.00  # Current weekly EU ETS auction price (EUR/tCO2e)

    if carbon_price_paid > 0:
        adjustment_fraction = min(carbon_price_paid / ets_price, 1.0)
        adjustment_tonnes = total_emissions * adjustment_fraction
    else:
        adjustment_tonnes = 0

    certificates_required = total_emissions - adjustment_tonnes

    # Cost estimate
    cost_eur = certificates_required * ets_price
    penalty_if_missing = certificates_required * 100  # EUR 100/tCO2e penalty

    return {
        "import_id": import_record.get("import_id"),
        "product": f"{category}/{product}",
        "quantity_tonnes": quantity,
        "origin_country": origin,
        "emission_factor": ef,
        "data_source": data_source,
        "total_embedded_emissions_tco2e": round(total_emissions, 2),
        "carbon_price_adjustment_tco2e": round(adjustment_tonnes, 2),
        "certificates_required": round(certificates_required, 2),
        "estimated_cost_eur": round(cost_eur, 2),
        "penalty_if_missing_eur": round(penalty_if_missing, 2),
        "ets_reference_price_eur": ets_price
    }
```

### Example: Calculating Emissions for a Steel Import

```python
# Example: 500 tonnes of hot-rolled steel coil from Turkey
import_record = {
    "import_id": "IMP-2026-04-0042",
    "product_category": "iron_steel",
    "product_type": "hot_rolled_coil",
    "quantity_tonnes": 500,
    "origin_country": "TR",
    "actual_emissions_per_tonne": None,  # no actual data from supplier
    "carbon_price_paid": None            # Turkey has no carbon price
}

result = calculate_embedded_emissions(import_record)
# Result:
# total_embedded_emissions_tco2e: 925.0  (500t × 1.85 tCO2e/t)
# carbon_price_adjustment_tco2e: 0       (Turkey: no carbon price)
# certificates_required: 925.0
# estimated_cost_eur: 60,125.00          (925 × EUR 65)
# penalty_if_missing_eur: 92,500.00      (925 × EUR 100)
```

### Quarterly Reconciliation Agent

The CBAM requires that importers hold at least 80% of required certificates by the end of each quarter. Build an agent that tracks this continuously:

```python
def quarterly_reconciliation(session, base_url, buyer_id, quarter_imports):
    """
    Run quarterly CBAM reconciliation:
    1. Calculate total emissions for all imports in the quarter
    2. Determine certificates required (80% threshold)
    3. Check current certificate holdings
    4. Trigger procurement if shortfall exists
    """

    # Calculate emissions for each import
    total_emissions = 0
    total_certificates_needed = 0
    import_details = []

    for imp in quarter_imports:
        result = calculate_embedded_emissions(imp)
        total_emissions += result["total_embedded_emissions_tco2e"]
        total_certificates_needed += result["certificates_required"]
        import_details.append(result)

    # 80% quarterly threshold
    quarterly_threshold = total_certificates_needed * 0.80
    quarterly_threshold_cost = quarterly_threshold * 65.00  # EUR at current ETS price

    # Record the reconciliation via analytics
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_analytics",
        "input": {
            "agent_id": buyer_id,
            "metric": "cbam_certificate_balance",
            "period": "current_quarter"
        }
    })
    current_balance = resp.json()

    certificates_held = current_balance.get("certificates_held", 0)
    shortfall = max(0, quarterly_threshold - certificates_held)

    reconciliation = {
        "quarter": "Q2-2026",
        "total_imports": len(quarter_imports),
        "total_emissions_tco2e": round(total_emissions, 2),
        "total_certificates_needed": round(total_certificates_needed, 2),
        "quarterly_threshold_80pct": round(quarterly_threshold, 2),
        "certificates_held": certificates_held,
        "shortfall": round(shortfall, 2),
        "shortfall_cost_eur": round(shortfall * 65.00, 2),
        "penalty_exposure_eur": round(shortfall * 100, 2),
        "status": "compliant" if shortfall <= 0 else "action_required",
        "import_details": import_details
    }

    # If shortfall exists, trigger automated procurement
    if shortfall > 0:
        # Message the broker agent to procure certificates
        session.post(f"{base_url}/v1", json={
            "tool": "send_message",
            "input": {
                "from_agent_id": buyer_id,
                "to_agent_id": broker_id,
                "message_type": "procurement_request",
                "content": {
                    "type": "cbam_certificates",
                    "volume_tco2e": shortfall,
                    "urgency": "high",
                    "max_price_eur_per_tco2e": 70,
                    "deadline": "end_of_quarter",
                    "reconciliation": reconciliation
                }
            }
        })
        reconciliation["procurement_triggered"] = True

    # Submit reconciliation data as compliance metrics
    resp = session.post(f"{base_url}/v1", json={
        "tool": "submit_metrics",
        "input": {
            "agent_id": buyer_id,
            "metrics": {
                "cbam_quarter": "Q2-2026",
                "cbam_total_emissions": total_emissions,
                "cbam_certificates_required": total_certificates_needed,
                "cbam_certificates_held": certificates_held,
                "cbam_shortfall": shortfall,
                "cbam_compliance_status": reconciliation["status"]
            }
        }
    })

    return reconciliation
```

### Compliance Status Checking

Use the compliance tool to verify your overall CBAM standing:

```python
# Check compliance status
resp = session.post(f"{base_url}/v1", json={
    "tool": "check_compliance",
    "input": {
        "agent_id": buyer_id,
        "compliance_type": "cbam",
        "parameters": {
            "jurisdiction": "EU",
            "reporting_period": "2026-Q2",
            "check_certificate_balance": True,
            "check_quarterly_threshold": True,
            "check_verification_status": True
        }
    }
})
compliance = resp.json()
print(f"CBAM compliance status: {compliance}")
```

### CBAM Compliance Checklist

```
CBAM Quarterly Compliance Checklist
======================================

[ ] Import records complete for all CBAM-covered goods
[ ] Embedded emissions calculated (actual data or defaults)
[ ] Carbon price adjustments applied for origin countries
[ ] Certificate requirement calculated
[ ] 80% quarterly threshold verified
[ ] Certificates procured to cover shortfall
[ ] Reconciliation report generated
[ ] Agent metrics updated with compliance status
[ ] Audit trail verified (all transactions in escrow history)
[ ] Next quarter's projected demand estimated

Annual Surrender (by May 31):
[ ] Full-year emissions calculated
[ ] 100% certificate coverage verified
[ ] Accredited verifier report obtained
[ ] Surrender filed with national competent authority
[ ] Any excess certificates noted for buyback opportunity
```

---

## Chapter 6: Multi-Agent Carbon Portfolios

### Demand Aggregation, Price Optimization, and Cross-Registry Arbitrage

A single buyer agent purchasing credits from a single broker is straightforward. Production systems require multi-agent coordination: aggregating demand across multiple business units, optimizing purchase timing against ETS price movements, and exploiting price differentials between registries. This chapter builds those patterns.

### Demand Aggregation Architecture

```
Multi-Agent Demand Aggregation
================================

Business Unit A          Business Unit B          Business Unit C
(Steel imports)          (Aluminum imports)       (Cement imports)
    │                        │                        │
    ▼                        ▼                        ▼
┌──────────┐           ┌──────────┐           ┌──────────┐
│ Buyer    │           │ Buyer    │           │ Buyer    │
│ Agent A  │           │ Agent B  │           │ Agent C  │
└────┬─────┘           └────┬─────┘           └────┬─────┘
     │                      │                      │
     └──────────┬───────────┴──────────┬───────────┘
                │                      │
                ▼                      ▼
        ┌──────────────┐      ┌──────────────┐
        │  Aggregator  │      │  Portfolio   │
        │    Agent     │─────►│  Optimizer   │
        └──────┬───────┘      └──────┬───────┘
               │                     │
               ▼                     ▼
        ┌──────────────────────────────────┐
        │       Broker Agent Network       │
        │  (cross-registry, multi-source)  │
        └──────────────────────────────────┘
```

### Building the Aggregator Agent

The aggregator collects demand from multiple buyer agents and consolidates it into bulk orders that qualify for volume discounts:

```python
# Register the aggregator agent
resp = session.post(f"{base_url}/v1", json={
    "tool": "register_agent",
    "input": {
        "name": "carbon-aggregator-v1",
        "description": "Demand aggregation agent for carbon credit procurement. "
                       "Consolidates requirements from multiple buyer agents, "
                       "negotiates bulk pricing, and coordinates delivery.",
        "capabilities": [
            "demand_aggregation",
            "bulk_negotiation",
            "portfolio_allocation",
            "cross_registry_optimization"
        ],
        "metadata": {
            "role": "aggregator",
            "max_buyer_agents": 50,
            "supported_credit_types": ["avoidance", "removal", "hybrid"]
        }
    }
})
aggregator = resp.json()
aggregator_id = aggregator["agent_id"]

# Collect demand from buyer agents
def aggregate_demand(session, base_url, aggregator_id, buyer_agent_ids):
    """
    Collect and consolidate demand from multiple buyer agents.
    """
    total_demand = {
        "removal": 0,
        "avoidance": 0,
        "hybrid": 0
    }
    buyer_requirements = []

    for buyer_id in buyer_agent_ids:
        # Retrieve each buyer's current demand
        resp = session.post(f"{base_url}/v1", json={
            "tool": "get_analytics",
            "input": {
                "agent_id": buyer_id,
                "metric": "carbon_demand",
                "period": "current_quarter"
            }
        })
        demand = resp.json()

        buyer_requirements.append({
            "buyer_id": buyer_id,
            "demand": demand
        })

        for credit_type in total_demand:
            total_demand[credit_type] += demand.get(
                f"{credit_type}_tonnes", 0
            )

    # Check volume discount for aggregated demand
    total_tonnes = sum(total_demand.values())
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_volume_discount",
        "input": {
            "agent_id": aggregator_id,
            "service_type": "carbon_credit_brokerage",
            "volume": total_tonnes,
            "period": "quarterly"
        }
    })
    volume_discount = resp.json()

    return {
        "total_demand": total_demand,
        "total_tonnes": total_tonnes,
        "buyer_count": len(buyer_agent_ids),
        "buyer_requirements": buyer_requirements,
        "volume_discount": volume_discount,
        "aggregation_savings_estimate": total_tonnes * 0.50  # ~$0.50/t savings from bulk
    }
```

### Price Optimization Strategy

Carbon credit prices fluctuate with the EU ETS auction price (weekly), registry supply/demand dynamics (daily), and seasonal patterns (quarterly compliance deadlines drive demand spikes). The optimizer agent times purchases to minimize cost:

```python
def optimize_purchase_timing(session, base_url, aggregator_id, demand):
    """
    Optimize credit purchase timing based on:
    1. Current ETS price vs 30-day moving average
    2. Days until quarterly compliance deadline
    3. Available supply at current prices
    4. Historical price seasonality
    """

    # Get current market analytics
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_analytics",
        "input": {
            "agent_id": aggregator_id,
            "metric": "market_conditions",
            "period": "last_30_days"
        }
    })
    market = resp.json()

    # Decision logic
    current_price = market.get("current_ets_price_eur", 65)
    avg_30d = market.get("avg_30d_ets_price_eur", 63)
    days_to_deadline = market.get("days_to_quarterly_deadline", 45)

    strategy = {
        "total_demand_tonnes": demand["total_tonnes"],
        "tranches": []
    }

    if current_price < avg_30d * 0.95:
        # Price is >5% below 30-day average: buy aggressively
        strategy["recommendation"] = "buy_now"
        strategy["tranches"].append({
            "percentage": 80,
            "timing": "immediate",
            "reason": "price_below_average"
        })
        strategy["tranches"].append({
            "percentage": 20,
            "timing": "next_week",
            "reason": "reserve_for_price_improvement"
        })

    elif days_to_deadline < 14:
        # Less than 2 weeks to deadline: buy everything now
        strategy["recommendation"] = "buy_urgently"
        strategy["tranches"].append({
            "percentage": 100,
            "timing": "immediate",
            "reason": "deadline_pressure"
        })

    else:
        # Normal conditions: dollar-cost average over remaining time
        weeks_remaining = days_to_deadline // 7
        weekly_pct = 100 / max(weeks_remaining, 1)
        for week in range(weeks_remaining):
            strategy["tranches"].append({
                "percentage": round(weekly_pct, 1),
                "timing": f"week_{week + 1}",
                "reason": "dollar_cost_averaging"
            })
        strategy["recommendation"] = "dca"

    return strategy
```

### Cross-Registry Arbitrage

Different registries price equivalent credits differently. A 2025-vintage forest conservation credit might trade at $12/tonne on Verra and $15/tonne on Gold Standard (due to Gold Standard's stricter co-benefits requirements and the resulting premium). For buyers who need compliance-grade credits (where registry pedigree matters), this difference is justified. For voluntary buyers focused primarily on volume, the Verra credit at $12 represents a better value for equivalent climate impact.

```python
def find_arbitrage_opportunities(session, base_url, broker_id):
    """
    Identify price differentials for equivalent credits across registries.
    """

    registries = ["verra_vcs", "gold_standard", "acr"]
    credit_types = ["avoidance", "removal"]

    opportunities = []

    for credit_type in credit_types:
        prices = {}
        for registry in registries:
            resp = session.post(f"{base_url}/v1", json={
                "tool": "search_services",
                "input": {
                    "query": f"{credit_type} carbon credits",
                    "category": "carbon_trading",
                    "filters": {
                        "registry": registry,
                        "credit_type": credit_type,
                        "min_vintage_year": 2024
                    }
                }
            })
            results = resp.json()
            if results.get("results"):
                avg_price = sum(
                    r.get("price_per_tonne", 0)
                    for r in results["results"]
                ) / len(results["results"])
                prices[registry] = avg_price

        # Find spreads
        if len(prices) >= 2:
            sorted_prices = sorted(prices.items(), key=lambda x: x[1])
            cheapest = sorted_prices[0]
            most_expensive = sorted_prices[-1]
            spread = most_expensive[1] - cheapest[1]
            spread_pct = (spread / cheapest[1]) * 100 if cheapest[1] > 0 else 0

            if spread_pct > 10:  # >10% spread is meaningful
                opportunities.append({
                    "credit_type": credit_type,
                    "buy_registry": cheapest[0],
                    "buy_price": cheapest[1],
                    "sell_registry": most_expensive[0],
                    "sell_price": most_expensive[1],
                    "spread_usd": round(spread, 2),
                    "spread_pct": round(spread_pct, 1)
                })

    return {"opportunities": opportunities, "count": len(opportunities)}
```

### Portfolio Risk Management

A carbon credit portfolio carries three categories of risk that traditional financial portfolios do not:

**Reversal risk.** Nature-based credits (REDD+, afforestation) can reverse if the forest burns down, is logged, or succumbs to disease. Buffer pools held by registries mitigate this partially, but a portfolio concentrated in a single geography or project type faces correlated reversal risk. Diversification across geographies and credit types (nature-based, engineered removal, avoidance) is the primary mitigation.

**Regulatory risk.** A credit type that qualifies for CBAM compliance today may be disqualified by future implementing acts. Article 6.4 credits are expected to be the gold standard, but the Supervisory Body's methodological decisions are ongoing. Holding credits across multiple compliance frameworks (EU ETS-linked, Article 6.2 ITMOs, Article 6.4, and national programs) hedges against single-framework disqualification.

**Reputational risk.** High-profile investigative reports on carbon credit fraud (the 2023 Verra/REDD+ controversy, the 2024 South Pole allegations) can crater the value and acceptability of entire project categories overnight. Portfolio construction must consider not just current quality scores but also exposure to categories under active scrutiny.

### Portfolio Allocation

Distribute aggregated demand across credit types and registries to optimize for cost, quality, and compliance eligibility:

```python
def allocate_portfolio(demand, budget_usd, compliance_requirements):
    """
    Allocate a carbon credit portfolio across types and registries.

    Allocation strategy:
    1. CBAM-eligible credits first (compliance requirement)
    2. High-quality removal credits (reputational value)
    3. Cost-optimized avoidance credits (volume fill)
    """

    allocation = {
        "cbam_compliance": {
            "budget_pct": 60,
            "credit_type": "compliance_grade",
            "target_registries": ["article6_4", "eu_ets_linked"],
            "tonnes": demand["total_tonnes"] * 0.60,
            "max_price_per_tonne": 70
        },
        "high_quality_removal": {
            "budget_pct": 25,
            "credit_type": "removal",
            "target_registries": ["verra_vcs", "gold_standard", "puro_earth"],
            "tonnes": demand["total_tonnes"] * 0.25,
            "max_price_per_tonne": 120,
            "min_permanence_years": 100
        },
        "volume_fill": {
            "budget_pct": 15,
            "credit_type": "avoidance",
            "target_registries": ["verra_vcs", "acr"],
            "tonnes": demand["total_tonnes"] * 0.15,
            "max_price_per_tonne": 20,
            "min_quality_score": 5.0
        }
    }

    total_estimated_cost = (
        allocation["cbam_compliance"]["tonnes"] * 65 +
        allocation["high_quality_removal"]["tonnes"] * 80 +
        allocation["volume_fill"]["tonnes"] * 12
    )

    allocation["total_estimated_cost_usd"] = round(total_estimated_cost, 2)
    allocation["within_budget"] = total_estimated_cost <= budget_usd

    return allocation
```

---

## Chapter 7: Dispute Resolution and Audit Trails

### Handling Greenwashing Claims, Double-Counting Disputes, and Regulatory Audits

Carbon markets face a unique dispute landscape. Credits can be fraudulent (non-existent projects), exaggerated (inflated baselines), double-counted (sold to multiple buyers), or greenwashed (marketed as high-quality when they are not). This chapter builds the dispute resolution and audit trail infrastructure that handles these scenarios.

### Dispute Categories in Carbon Trading

```
Carbon Credit Dispute Taxonomy
=================================

FRAUD                           QUALITY
├─ Non-existent project         ├─ Inflated baseline
├─ Fabricated MRV data          ├─ Additionality failure
├─ Fake registry entries        ├─ Permanence reversal
└─ Identity fraud               └─ Methodology deficiency

DELIVERY                        COMPLIANCE
├─ Late delivery                ├─ Wrong registry
├─ Wrong vintage                ├─ Not CBAM-eligible
├─ Wrong credit type            ├─ Missing corresponding adjustment
├─ Partial delivery             └─ Insufficient verification
└─ Non-delivery

DOUBLE-COUNTING
├─ Same credit on multiple registries
├─ Credit retired but resold
├─ Missing corresponding adjustment (Article 6)
└─ Host country NDC double-claim
```

### Opening a Dispute

When a buyer agent detects a problem with delivered credits, it opens a dispute through the escrow system:

```python
def open_carbon_dispute(session, base_url, buyer_id, escrow_id,
                        dispute_type, evidence):
    """
    Open a dispute for a carbon credit trade.

    dispute_type: one of 'fraud', 'quality', 'delivery', 'compliance',
                  'double_counting', 'greenwashing'
    evidence: dict containing supporting data for the claim
    """

    resp = session.post(f"{base_url}/v1", json={
        "tool": "open_dispute",
        "input": {
            "escrow_id": escrow_id,
            "complainant_agent_id": buyer_id,
            "reason": dispute_type,
            "details": {
                "dispute_category": dispute_type,
                "evidence": evidence,
                "requested_resolution": determine_resolution(dispute_type),
                "urgency": "high" if dispute_type in [
                    "fraud", "double_counting"
                ] else "medium"
            }
        }
    })
    dispute = resp.json()
    dispute_id = dispute.get("dispute_id")

    # Record the dispute in the buyer's transaction history
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_transaction_history",
        "input": {
            "agent_id": buyer_id,
            "filters": {
                "escrow_id": escrow_id,
                "include_disputes": True
            }
        }
    })

    return {
        "dispute_id": dispute_id,
        "escrow_id": escrow_id,
        "type": dispute_type,
        "status": "open",
        "transaction_history": resp.json()
    }


def determine_resolution(dispute_type):
    """Map dispute types to standard resolution requests."""
    resolutions = {
        "fraud": "full_refund_and_blacklist",
        "quality": "partial_refund_or_replacement",
        "delivery": "redeliver_or_refund",
        "compliance": "replacement_with_compliant_credits",
        "double_counting": "full_refund_and_registry_notification",
        "greenwashing": "independent_verification_and_adjustment"
    }
    return resolutions.get(dispute_type, "arbitration")
```

### Handling a Greenwashing Dispute

Greenwashing is the most common dispute type in carbon markets. A credit marketed as "high-quality removal" turns out to be a standard avoidance credit with inflated co-benefits claims. Here is the full flow:

```python
def handle_greenwashing_dispute(session, base_url, buyer_id, broker_id,
                                verifier_id, escrow_id, credit_data):
    """
    Handle a greenwashing dispute:
    1. Buyer flags quality discrepancy
    2. Independent verifier re-evaluates the credit
    3. If greenwashing confirmed, dispute is resolved in buyer's favor
    4. If not confirmed, dispute is resolved in seller's favor
    """

    # Step 1: Buyer opens dispute with evidence
    evidence = {
        "claimed_quality_score": credit_data.get("claimed_score", 8.5),
        "claimed_credit_type": credit_data.get("claimed_type", "removal"),
        "actual_observations": {
            "project_visit_findings": "No active carbon removal equipment observed",
            "registry_methodology": "VM0007 (REDD+) — avoidance, not removal",
            "independent_assessment": "Credit type misrepresented in listing"
        },
        "supporting_documents": [
            "site_visit_report_2026_03.pdf",
            "registry_methodology_screenshot.png",
            "original_listing_archived.html"
        ]
    }

    dispute = open_carbon_dispute(
        session, base_url, buyer_id, escrow_id,
        "greenwashing", evidence
    )

    # Step 2: Request independent verification
    resp = session.post(f"{base_url}/v1", json={
        "tool": "send_message",
        "input": {
            "from_agent_id": buyer_id,
            "to_agent_id": verifier_id,
            "message_type": "verification_request",
            "content": {
                "dispute_id": dispute["dispute_id"],
                "credit_data": credit_data,
                "verification_scope": "full_reassessment",
                "original_claimed_score": evidence["claimed_quality_score"]
            }
        }
    })

    # Step 3: Verifier re-scores the credit
    reverification = run_verification_pipeline(
        session, base_url, verifier_id, credit_data
    )
    actual_score = reverification.get("quality", {}).get("composite_score", 0)
    claimed_score = evidence["claimed_quality_score"]
    discrepancy = claimed_score - actual_score

    # Step 4: Resolve based on findings
    if discrepancy > 2.0:
        # Significant greenwashing — resolve in buyer's favor
        resp = session.post(f"{base_url}/v1", json={
            "tool": "resolve_dispute",
            "input": {
                "dispute_id": dispute["dispute_id"],
                "resolution": "buyer_favored",
                "details": {
                    "finding": "greenwashing_confirmed",
                    "claimed_score": claimed_score,
                    "actual_score": actual_score,
                    "discrepancy": round(discrepancy, 2),
                    "remedy": "full_refund",
                    "credit_type_mismatch": True
                }
            }
        })
    elif discrepancy > 0.5:
        # Minor discrepancy — partial adjustment
        adjustment_pct = (discrepancy / claimed_score) * 100
        resp = session.post(f"{base_url}/v1", json={
            "tool": "resolve_dispute",
            "input": {
                "dispute_id": dispute["dispute_id"],
                "resolution": "partial_adjustment",
                "details": {
                    "finding": "quality_overstatement",
                    "adjustment_percentage": round(adjustment_pct, 1),
                    "remedy": "partial_refund",
                    "refund_amount": round(
                        credit_data.get("total_usd", 0) * adjustment_pct / 100, 2
                    )
                }
            }
        })
    else:
        # No material discrepancy
        resp = session.post(f"{base_url}/v1", json={
            "tool": "resolve_dispute",
            "input": {
                "dispute_id": dispute["dispute_id"],
                "resolution": "seller_favored",
                "details": {
                    "finding": "quality_within_tolerance",
                    "claimed_score": claimed_score,
                    "actual_score": actual_score,
                    "discrepancy": round(discrepancy, 2)
                }
            }
        })

    return resp.json()
```

### Building the Audit Trail

Regulators require a complete, tamper-evident audit trail for carbon credit transactions. GreenHelix's transaction history, claim chains, and metrics create this trail automatically -- but you need to structure queries correctly for regulatory reporting:

```python
def generate_audit_report(session, base_url, buyer_id, reporting_period):
    """
    Generate a comprehensive audit trail for a reporting period.
    Suitable for regulatory review and third-party verification.
    """

    # 1. Transaction history — all financial movements
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_transaction_history",
        "input": {
            "agent_id": buyer_id,
            "filters": {
                "period": reporting_period,
                "include_escrows": True,
                "include_disputes": True,
                "include_transfers": True
            }
        }
    })
    transactions = resp.json()

    # 2. Agent reputation — verification of counterparty quality
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_agent_reputation",
        "input": {
            "agent_id": buyer_id
        }
    })
    reputation = resp.json()

    # 3. Compliance metrics — CBAM reconciliation data
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_analytics",
        "input": {
            "agent_id": buyer_id,
            "metric": "compliance_history",
            "period": reporting_period
        }
    })
    compliance = resp.json()

    audit_report = {
        "report_type": "carbon_credit_audit_trail",
        "agent_id": buyer_id,
        "reporting_period": reporting_period,
        "generated_at": "2026-04-06T12:00:00Z",
        "sections": {
            "financial_transactions": {
                "total_transactions": len(transactions.get("transactions", [])),
                "total_spent_usd": sum(
                    t.get("amount", 0) for t in transactions.get("transactions", [])
                ),
                "escrows_created": len([
                    t for t in transactions.get("transactions", [])
                    if t.get("type") == "escrow"
                ]),
                "disputes_filed": len([
                    t for t in transactions.get("transactions", [])
                    if t.get("type") == "dispute"
                ]),
                "details": transactions
            },
            "credit_portfolio": {
                "total_credits_purchased_tco2e": compliance.get(
                    "total_purchased", 0
                ),
                "total_credits_retired_tco2e": compliance.get(
                    "total_retired", 0
                ),
                "average_quality_score": compliance.get(
                    "avg_quality_score", 0
                ),
                "registries_used": compliance.get("registries", [])
            },
            "cbam_compliance": {
                "quarters_reported": compliance.get("quarters", []),
                "certificates_surrendered": compliance.get(
                    "certificates_surrendered", 0
                ),
                "penalties_incurred": compliance.get("penalties_eur", 0),
                "verification_reports": compliance.get("verifier_reports", [])
            },
            "counterparty_reputation": reputation,
            "dispute_history": {
                "total_disputes": len([
                    t for t in transactions.get("transactions", [])
                    if t.get("type") == "dispute"
                ]),
                "disputes_won": compliance.get("disputes_won", 0),
                "disputes_lost": compliance.get("disputes_lost", 0)
            }
        }
    }

    return audit_report
```

### Regulatory Audit Readiness Checklist

```
Regulatory Audit Readiness
============================

DOCUMENTATION
[ ] Agent registration records (all three roles)
[ ] Service registration records
[ ] Claim chain entries for all verification claims
[ ] Identity credentials (ISO certifications, registry access)

FINANCIAL RECORDS
[ ] Complete escrow history (creation, release, dispute)
[ ] All transfers with counterparty identification
[ ] Fee and commission records
[ ] Volume discount documentation

COMPLIANCE DATA
[ ] Quarterly CBAM reconciliation reports
[ ] Embedded emissions calculations (per import line)
[ ] Certificate purchase records with ETS price references
[ ] Annual surrender documentation
[ ] Accredited verifier reports

CREDIT INTEGRITY
[ ] MRV validation records for every purchased credit
[ ] Quality scores with dimension breakdowns
[ ] Double-counting check results
[ ] Registry transfer confirmations
[ ] Retirement confirmations with serial numbers

DISPUTE RECORDS
[ ] All opened disputes with evidence
[ ] Resolution outcomes
[ ] Remedy execution (refunds, replacements)
[ ] Greenwashing assessments
```

---

## Chapter 8: The 30-Day Implementation Sprint

### From First API Call to Production Carbon Trading System

This chapter provides a day-by-day implementation plan. Each day builds on the previous one. By day 30, you have a production-ready carbon trading system with CBAM compliance automation.

### Sprint Overview

```
30-Day Implementation Sprint
==============================

WEEK 1: FOUNDATION (Days 1-7)
├─ Day 1-2:  Agent registration and identity setup
├─ Day 3-4:  Wallet creation and funding
├─ Day 5-6:  Service registration and marketplace listing
└─ Day 7:    Integration testing (agent-to-agent communication)

WEEK 2: VERIFICATION (Days 8-14)
├─ Day 8-9:   MRV verification pipeline
├─ Day 10-11: Quality scoring model calibration
├─ Day 12-13: Double-counting detection
└─ Day 14:    End-to-end verification testing

WEEK 3: TRADING (Days 15-21)
├─ Day 15-16: Escrow-protected trade flow
├─ Day 17-18: SLA creation and monitoring
├─ Day 19-20: Dispute handling workflows
└─ Day 21:    Trade flow integration testing

WEEK 4: COMPLIANCE & PRODUCTION (Days 22-30)
├─ Day 22-23: CBAM emissions calculator
├─ Day 24-25: Quarterly reconciliation automation
├─ Day 26-27: Multi-agent portfolio optimization
├─ Day 28:    Audit trail generation
├─ Day 29:    Production hardening and monitoring
└─ Day 30:    Go-live and first automated trade
```

### Week 1: Foundation (Days 1-7)

**Days 1-2: Agent Registration**

Start with a single Python module that registers all three agents and stores their IDs:

```python
import requests
import json
import os

# Configuration
BASE_URL = "https://api.greenhelix.net/v1"
API_KEY = os.environ["GREENHELIX_API_KEY"]

session = requests.Session()
session.headers["Authorization"] = f"Bearer {API_KEY}"
session.headers["Content-Type"] = "application/json"

def execute(tool, input_data):
    """Helper to execute a GreenHelix tool."""
    resp = session.post(f"{BASE_URL}/v1", json={
        "tool": tool,
        "input": input_data
    })
    resp.raise_for_status()
    return resp.json()

# Register all agents
agents = {}
for role, config in {
    "verifier": {
        "name": "carbon-verifier-prod",
        "description": "Production MRV verification agent",
        "capabilities": ["mrv_verification", "quality_scoring",
                         "double_count_detection"]
    },
    "broker": {
        "name": "carbon-broker-prod",
        "description": "Production carbon credit brokerage agent",
        "capabilities": ["credit_discovery", "trade_execution",
                         "escrow_management"]
    },
    "buyer": {
        "name": "carbon-buyer-prod",
        "description": "Production carbon credit procurement agent",
        "capabilities": ["demand_specification", "compliance_tracking",
                         "cbam_reconciliation"]
    }
}.items():
    result = execute("register_agent", config)
    agents[role] = result["agent_id"]
    print(f"Registered {role}: {result['agent_id']}")

# Save agent IDs for subsequent scripts
with open("agent_config.json", "w") as f:
    json.dump(agents, f, indent=2)
```

**Days 3-4: Wallet Creation and Funding**

```python
# Create wallets and verify funding
for role, agent_id in agents.items():
    wallet = execute("create_wallet", {
        "agent_id": agent_id,
        "currency": "USD"
    })
    print(f"{role} wallet: {wallet['wallet_id']}")

    # Fund the buyer wallet (transfer from treasury)
    if role == "buyer":
        execute("transfer", {
            "from_agent_id": "treasury",
            "to_agent_id": agent_id,
            "amount": 500000.00,
            "currency": "USD",
            "description": "Initial funding for carbon credit procurement"
        })
```

**Days 5-6: Service Registration**

```python
# Register the brokerage service
execute("register_service", {
    "agent_id": agents["broker"],
    "name": "Carbon Credit Brokerage Service",
    "description": "Full-service carbon credit brokerage with MRV "
                   "verification, escrow-protected trading, and "
                   "retirement confirmation.",
    "category": "carbon_trading",
    "pricing": {
        "model": "commission",
        "rate_bps": 150,
        "minimum_fee_usd": 50
    }
})

# Register the verification service
execute("register_service", {
    "agent_id": agents["verifier"],
    "name": "Carbon Credit Verification Service",
    "description": "Independent MRV verification, quality scoring, "
                   "and double-counting detection for carbon credits.",
    "category": "carbon_verification",
    "pricing": {
        "model": "per_verification",
        "fee_usd": 25
    }
})
```

**Day 7: Integration Test**

```python
# Verify agent-to-agent communication
resp = execute("send_message", {
    "from_agent_id": agents["buyer"],
    "to_agent_id": agents["broker"],
    "message_type": "ping",
    "content": {"test": True, "timestamp": "2026-04-06T12:00:00Z"}
})
print(f"Message sent: {resp}")

# Verify service discovery
resp = execute("search_services", {
    "query": "carbon credit",
    "category": "carbon_trading"
})
print(f"Services found: {len(resp.get('results', []))}")

# Verify reputation system
resp = execute("get_agent_reputation", {
    "agent_id": agents["verifier"]
})
print(f"Verifier reputation: {resp}")
```

### Week 2: Verification Pipeline (Days 8-14)

Build the verification pipeline components from Chapter 3. Each day implements and tests one component:

- **Days 8-9**: Implement `verify_mrv_data()` and test against sample credits with known-good and known-bad MRV data.
- **Days 10-11**: Implement `score_carbon_credit()` and calibrate weights by scoring a diverse set of credits and comparing against manual assessments.
- **Days 12-13**: Implement `check_double_counting()` and test with synthetic duplicates planted across registries.
- **Day 14**: Wire all three into `run_verification_pipeline()` and run an end-to-end test with 100 sample credits. Target: zero false negatives on planted defects, fewer than 5% false positives.

### Week 3: Trading Infrastructure (Days 15-21)

Build the trading components from Chapter 4:

- **Days 15-16**: Implement `execute_carbon_trade()` with escrow creation. Test with small trades ($100) to verify the escrow lifecycle.
- **Days 17-18**: Add SLA creation and monitoring. Test deadline enforcement by creating SLAs with short deadlines and verifying breach detection.
- **Days 19-20**: Implement dispute handling from Chapter 7. Test all six dispute types with synthetic scenarios.
- **Day 21**: Run a complete trade from discovery through retirement, including a deliberate quality dispute that resolves correctly.

### Week 4: Compliance and Go-Live (Days 22-30)

**Days 22-23: CBAM Calculator**

Deploy the emissions calculator from Chapter 5. Validate against known import records:

```python
# Validation test: known import with known emissions
test_imports = [
    {
        "import_id": "TEST-001",
        "product_category": "iron_steel",
        "product_type": "hot_rolled_coil",
        "quantity_tonnes": 1000,
        "origin_country": "TR",
        "expected_emissions": 1850.0,
        "expected_certificates": 1850.0
    },
    {
        "import_id": "TEST-002",
        "product_category": "aluminum",
        "product_type": "unwrought_primary",
        "quantity_tonnes": 200,
        "origin_country": "CN",
        "expected_emissions": 1680.0,
        "expected_certificates": 1460.31  # adjusted for China's carbon price
    }
]

for test in test_imports:
    result = calculate_embedded_emissions(test)
    assert abs(result["total_embedded_emissions_tco2e"] -
               test["expected_emissions"]) < 0.1, (
        f"Emissions mismatch for {test['import_id']}"
    )
    print(f"PASS: {test['import_id']}")
```

**Days 24-25: Quarterly Reconciliation**

Deploy the reconciliation agent from Chapter 5. Set it to run daily, checking the 80% threshold.

**Days 26-27: Portfolio Optimization**

Deploy the multi-agent portfolio from Chapter 6. Start with the demand aggregation pattern and a simple 60/25/15 allocation.

**Day 28: Audit Trail**

Generate the first audit report and validate it against the regulatory checklist from Chapter 7.

**Day 29: Production Hardening**

```python
# Production monitoring setup
def production_health_check(session, base_url, agents):
    """
    Run a complete health check of the carbon trading system.
    """
    checks = {}

    # Verify all agents are responsive
    for role, agent_id in agents.items():
        resp = session.post(f"{base_url}/v1", json={
            "tool": "get_agent_reputation",
            "input": {"agent_id": agent_id}
        })
        checks[f"{role}_agent"] = resp.status_code == 200

    # Verify escrow system
    resp = session.post(f"{base_url}/v1", json={
        "tool": "get_transaction_history",
        "input": {
            "agent_id": agents["buyer"],
            "filters": {"period": "last_24h"}
        }
    })
    checks["transaction_history"] = resp.status_code == 200

    # Verify marketplace discovery
    resp = session.post(f"{base_url}/v1", json={
        "tool": "search_services",
        "input": {
            "query": "carbon",
            "category": "carbon_trading"
        }
    })
    checks["service_discovery"] = resp.status_code == 200

    all_healthy = all(checks.values())
    return {"healthy": all_healthy, "checks": checks}
```

**Day 30: Go-Live**

Execute the first production trade. Start with a small volume (100 tonnes) to validate the end-to-end flow in production:

```python
# First production trade
first_trade = execute_carbon_trade(
    session, BASE_URL,
    buyer_id=agents["buyer"],
    broker_id=agents["broker"],
    verifier_id=agents["verifier"],
    trade_params={
        "credit_type": "removal",
        "registry": "verra_vcs",
        "volume_tonnes": 100,
        "price_per_tonne_usd": 42.50,
        "total_usd": 4250.00,
        "conditions": {
            "min_quality_score": 7.0,
            "vintage_year": 2025,
            "delivery_deadline": "2026-04-09T00:00:00Z",
            "retirement_required": True,
            "retirement_deadline": "2026-04-12T00:00:00Z"
        },
        "sla_terms": {
            "delivery_deadline": "2026-04-09T00:00:00Z",
            "retirement_deadline": "2026-04-12T00:00:00Z",
            "quality_threshold": 7.0,
            "volume_guarantee_tonnes": 100,
            "penalty_for_late_delivery_pct": 5,
            "penalty_for_non_delivery_pct": 100
        }
    }
)

print(f"First production trade: {json.dumps(first_trade, indent=2)}")
```

---

## What You Get

This guide gives you a complete, production-ready system for agent-powered carbon credit trading and CBAM compliance:

**Three specialized agents** -- verifier, broker, and buyer -- registered on GreenHelix with wallets, identity claims, reputation baselines, and marketplace service listings.

**A verification pipeline** that validates MRV data, scores credit quality across six dimensions (additionality, permanence, co-benefits, methodology, vintage, registry), and detects double-counting across registries.

**Escrow-protected trading** with SLA enforcement that guarantees delivery timelines, quality thresholds, retirement confirmation, and automatic dispute escalation when terms are breached.

**CBAM compliance automation** including embedded emissions calculators for all six covered sectors, carbon price adjustments for origin countries, quarterly 80% threshold monitoring, and automated certificate procurement when shortfalls are detected.

**Multi-agent portfolio management** with demand aggregation across business units, purchase timing optimization against ETS price movements, cross-registry arbitrage detection, and strategic allocation across compliance-grade, removal, and avoidance credits.

**Dispute resolution** for greenwashing, double-counting, delivery failures, and compliance deficiencies -- with automatic escalation, independent re-verification, and resolution enforcement through escrow.

**A complete audit trail** structured for regulatory review, including financial transactions, credit integrity records, compliance reconciliation data, and counterparty reputation scores.

**A 30-day sprint plan** that takes you from your first API call to a production system executing automated carbon credit trades with full CBAM compliance. Every code example uses the GreenHelix API. Every pattern handles the edge cases that real carbon markets produce.

The EU CBAM penalty is EUR 100 per tonne. The average trade in this system costs EUR 65 per tonne. The difference is the cost of being late. Your agents will not be late.

