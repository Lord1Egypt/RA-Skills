# 01 — IT Strategy Planning

## Objectives
Based on diagnostic findings and the client's business strategy, design a complete IT strategic plan — defining the 3-5 year IT development direction, investment priorities, and implementation roadmap, positioning IT as a strategic asset for business growth.

## Prerequisites
- Diagnostic report completed and confirmed by the client
- Client business strategy / annual plan obtained
- Client IT budget range understood

## Inputs
- IT Current-State Diagnostic Report
- Client business strategy documents / CEO interview records
- Industry trend research + competitive IT capability benchmarking

---

## Operation Steps

### Step 0: Strategic Context Analysis — Digital China & Xinchuang Policy Impact

Before starting strategy decoding, assess three key policy dimensions:

| Policy Dimension | Key Question | Impact Level |
|---------|---------|---------|
| Xinchuang Requirements | Is the client within the scope of Xinchuang substitution? | State-owned enterprises: High / Private enterprises: Medium |
| Data as a Factor of Production (Data Element ×) | Can client data become an asset? | Data-intensive: High |
| Digital Transformation KPIs | Does the client's superior/SASAC have assessment requirements? | State-owned enterprises: High |
| Cross-border Data Compliance | Does the client operate cross-border? | Multinational: High |

#### Five-Force Diagnostic Quick Assessment (See details in `references/Core Methodology Library.md §11`)
Before strategy decoding, use the Five-Force model to quickly assess the client's digital baseline:
- Strategy Force [1-5]: Degree of alignment between digital strategy and business strategy
- Organization Force [1-5]: CDO/Digital leadership and talent density
- Process Force [1-5]: End-to-end process digitalization coverage
- Technology Force [1-5]: Cloud adoption rate + APIfication rate
- Data Force [1-5]: Data-driven decision coverage

→ Five-Force Radar Chart → Identify the weakest link → Strategic focus

---

### Step 1: Business Strategy Decoding — Translating from Business Language to IT Language

First, translate the client's business strategy into IT's required responses:

```
Business Strategic Intent              →     IT Strategic Implication                   →      IT Initiative
────────────────────────────────────────────────────────────────────────────────────────────────────────────────
"3-year revenue doubling, enter 5 new markets"  →  Systems need to support multi-country/multi-language/multi-currency/   →  Core system internationalization overhaul +
                               multi-regulation, with rapid replication deployment           Global ERP template + Cloud infrastructure global deployment

"Non-organic growth via M&A"     →  Speed and cost of IT integration for acquired companies       →  M&A IT Playbook +
                              is key to M&A value realization                 Integration architecture standardization + Data migration tools

"Transition from selling products to selling services/subscriptions"  →  Requires IoT/remote monitoring/subscription billing/         →  IoT platform + Subscription billing system +
                              customer self-service portal/data-driven operations            Customer portal + Data analytics platform

"AI-driven business innovation"          →  Data is fuel for AI — data governance/quality/     →  Data platform + MLOps + AI use case
                              labeling are prerequisites, not AI itself          Pipeline + AI Center of Excellence

'Xinchuang domestic substitution'            →  Technology stack security + supply chain autonomy +        →  Full-stack domestic adaptation roadmap +
                      reducing redundant systems                         Vendor optimization
                     CPU/OS/DB/Middleware layer-by-layer replacement
                      Future compliance risk

"Cost reduction 20%, improve operational efficiency"     →  Automation/process reengineering/system integration/          →  RPA+AI automation + Application integration +
                              reducing redundant systems                         Vendor optimization

"Improve customer experience and NPS"         →  Omni-channel experience/personalization/real-time/           →  CRM+CDP + Omni-channel platform +
                              Data-driven customer insights                  Customer data platform
```

### Step 2: Design Target Capability Blueprint — Business Capability Heatmap

**2.1 Identify Core Business Capabilities (15-25 items)**

```
Strategic Capabilities (Competitive Differentiators):
  ├── Product Innovation & R&D
  ├── Customer Insight & Personalization
  ├── Supply Chain Agility
  └── Data-driven Decision Making

Core Operational Capabilities (Core Operations):
  ├── Procurement & Vendor Management
  ├── Production/Service Delivery
  ├── Sales & Channel Management
  ├── Order Management
  ├── Finance & Accounting
  ├── Human Resources
  └── IT & Digitalization

Supporting Capabilities:
  ├── Compliance & Risk Management
  ├── Legal & Intellectual Property
  └── Corporate Communications
```

**2.2 Capability Heatmap (Current Support Level vs. Business Importance)**

```
Capability              Business Importance   IT Current Support    Gap     Priority
                        (1-5)                 (1-5)
─────────────────────────────────────────────────────────────────────────
Product Innovation      5                     2                     -3      🔴 P0 Immediate Action
Customer Insight & Personalization  5          3                     -2      🔴 P0 Immediate Action
Supply Chain Agility    4                     3                     -1      🟡 P1 Within 6 Months
Order Management        4                     4                     0       🟢 Maintain
Finance & Accounting    3                     3                     0       🟢 Maintain
HR                      2                     4                     +2      📌 Over-invested, can reduce cost appropriately
```

### Step 3: Design Target Architecture Blueprint

**3.1 Application Architecture Target State**

Plan by SoR/SoD/SoI three-layer classification:

```
SoR Layer (Systems of Record — pursue stability/standardization/low TCO):
  Target: Core ERP/HR/Finance — SAP S/4HANA or Oracle Fusion Cloud
  Strategy: Standardize → Integrate → Move to Cloud → Process Automation

SoD Layer (Differentiating Systems — pursue business fit/agility):
  Target: CRM/CDP/E-commerce/Supply Chain Decisions — Salesforce + Custom-built
  Strategy: Best-of-Breed → API-First → Microservice-based

SoI Layer (Innovation Systems — pursue speed/experimentation):
  Target: AI Recommendations/Predictions/Agents — Cloud-native + Data Platform
  Strategy: Rapid Experimentation → Data-driven → Rapid Scaling or Rapid Termination
```

**3.2 Application Rationalization Matrix**

```
Current System   Health   Business Fit   Strategic Alignment   Recommended Action   Target State
Core ERP         2/5      3/5            4/5                   Modernize             → Upgrade to cloud version + APIfication
Legacy CRM       3/5      2/5            2/5                   Replace               → Migrate to Salesforce
BI Reporting     4/5      3/5            3/5                   Keep                  → Maintain, supplement with self-service analytics
Phone Support    2/5      1/5            1/5                   Retire                → Merge functionality into omni-channel service platform
E-commerce       3/5      4/5            5/5                   Modernize             → Re-platform + Microservices
```

### Step 4: Investment Portfolio Design — Run/Grow/Transform

```
Total IT Investment: $XXM/year (X.X% of revenue)

Current Allocation:
  Run (Operations):     $XXM (65%)  
  Grow (Growth):        $XXM (22%)  
  Transform:            $XXM (13%)  

Target Allocation (3 years later):
  Run (Operations):     $XXM (48%)  ← Reduce 17pp through automation
  Grow (Growth):        $XXM (30%)  ← More investment toward business growth support  
  Transform:            $XXM (22%)  ← AI/Data/Modernization

Transformation Path:
  Year 1: Focus on Run Optimization (Automation/System Integration/Cloud Migration → Free up funds)
  Year 2: More toward Grow (Business Empowerment/Data-driven/Agile Delivery)
  Year 3: Transform reaches 20%+ (AI Innovation/New Business Models/Ecosystem Platform)
```

**Investment Initiative Prioritization (IPA Matrix: Impact × Feasibility × Alignment):**

```
Initiative                         Strategic Alignment  Business Impact  Implementation Feasibility  Total Priority  Timeline
ERP Core Modernization             5                    4                3                           60              Year 1-2
Omni-channel Customer Platform     5                    5                4                           100             Year 1
AI Customer Insight Engine         4                    4                3                           48              Year 2
IT Operations Automation (ChatOps/AIOps)  3              3                5                           45              Year 1
Data Analytics & Self-service BI Platform  4            4                4                           64              Year 1-2
Cloud Migration (Non-core Systems) 3                    3                5                           45              Year 1
Microservices Architecture Overhaul 3                   3                2                           18              Year 2-3
```

### Step 5: Roadmap Wave Design

```
Wave 1: Quick Wins (0-6 months)
  ┌─────────────────────────────────────────────────┐
  │ 1. Omni-channel Customer Platform — Business-led, IT-supported             │
  │ 2. IT Operations Automation — Reduce Run cost, free up resources          │
  │ 3. Data Analytics Platform MVP — Let business quickly see data value      │
  │                                                  │
  │ Investment: $X.XM | Expected Annual Return: $X.XM | Payback: X months   │
  └─────────────────────────────────────────────────┘

Wave 2: Core Transformation (6-18 months)
  ┌─────────────────────────────────────────────────┐
  │ 4. ERP Core Modernization — Modular, finance first then supply chain       │
  │ 5. AI Customer Insight — Based on Wave 1 data platform              │
  │ 6. Application Integration & Retirement — Clean up redundant systems                │
  │                                                  │
  │ Investment: $X.XM | Expected Annual Return: $X.XM                  │
  └─────────────────────────────────────────────────┘

Wave 3: Innovation & Scale (18-36 months)
  ┌─────────────────────────────────────────────────┐
  │ 7. AI-driven Business Innovation — Expand from verified use cases          │
  │ 8. Microservices Architecture Full Overhaul                             │
  │ 9. Data Productization & Ecosystem Opening                          │
  │                                                  │
  │ Investment: $X.XM | Expected Annual Return: $X.XM                  │
  └─────────────────────────────────────────────────┘
```

### Step 6: Governance Mechanism Design

```
IT Governance Three-Tier Structure:

L1: IT Investment Board — Quarterly
   Members: CEO/CIO/CFO/BU Heads
   Responsibilities: IT strategic direction approval / Major investment decisions (>$X00K) / Investment portfolio rebalancing

L2: Architecture Review Board — Monthly
   Members: CIO/EA/Security Lead/Key Architects
   Responsibilities: Architecture standards setting / Major technology decisions / Architecture exception approvals

L3: Program/Project Governance — Per Project
   Members: Sponsor/PM/Key Stakeholders
   Responsibilities: Daily progress/Risks/Change decisions
```

---

## Outputs

- IT Strategic Planning Report (using `templates/it-strategy-planning-report-template.md`)
- Capability Heatmap
- Application Rationalization Matrix
- 3-Year Investment Roadmap
- IT Governance Design

## Quality Checklist

- [ ] Every IT initiative can be traced back to business strategy
- [ ] Each application rationalization recommendation (Retire/Maintain/Modernize/Replace) has a rationale and timing
- [ ] Roadmap accounts for organizational absorption capacity (more projects is not always better)
- [ ] Run/Grow/Transform ratios have clear year-by-year targets
- [ ] Financial model includes a "do nothing" comparison
- [ ] Governance design clarifies decision rights ownership

## Common Pitfalls

| Pitfall | Correct Approach |
|---------|------------------|
| IT strategy = IT department wish list | Start from business strategy, not from what IT wants to do |
| Roadmap stuffed too full (20+ projects) | 3-5 core initiatives per wave, focus > comprehensiveness. Finish one before starting another |
| Target architecture is "Li Auto Utopia" (perfect but unattainable) | Transition architecture is more important than target architecture — the client needs to know "how to get there step by step" |
| Copying a peer's strategy | Companies with the same annual revenue may need completely different IT strategies — context determines everything |
