# Enterprise Architecture Design

## Objectives

Based on the TOGAF ADM framework, complete the current-state (As-Is) modeling and target-state (To-Be) design of the enterprise architecture, producing the Architecture Definition Document and gap analysis.

---

## Prerequisites
- IT Current-State Diagnostic Report completed
- IT strategic direction has received initial consensus
- Key stakeholders have been identified and can participate in architecture reviews

## Inputs
- IT Current-State Diagnostic Report (from workflow 02-04)
- IT Strategic Planning Draft (from workflow 03-01)
- Business Capability Model / Business Strategy Document
- Existing architecture documentation (if any)

---

## Operation Steps

### Step 1: Architecture Scope Definition

**Output**: Architecture Scope Statement

1. **Define the architecture scope**
   - Entire enterprise? A specific business domain? A specific product line?
   - Which departments / systems / processes are affected?
   - What is excluded?

2. **Determine architecture dimensions**
   - Business Architecture — Mandatory
   - Data Architecture — Mandatory
   - Application Architecture — Mandatory
   - Technology Architecture — Mandatory
   - Security Architecture — Depends on project scope

3. **Architecture Scope Statement template**
| Element | Content |
|---------|---------|
| Architecture Scope | [e.g.: China-region core business systems, excluding overseas subsidiaries] |
| Time Horizon | Current State (As-Is) → Target State (To-Be, 3 years later) |
| Business Domains | [e.g.: Trading / Risk Control / Customer Service / Finance] |
| Key Constraints | [e.g.: Core systems cannot be taken offline, data must not leave the country, budget cap] |
| Exclusions | [e.g.: Office network, non-core peripheral systems] |

---

### Step 2: Business Architecture Design

**Output**: Business Capability Map + Business Process Diagrams + Organization Mapping

#### 2.1 Business Capability Modeling

Build an L1→L2→L3 business capability map:

```
Level 1: Strategic Capabilities
  ├── Market Insight
  ├── Product Innovation
  └── Strategic Planning

Level 1: Core Capabilities
  ├── Marketing & Sales
  │   ├── L2: Marketing Management
  │   │   ├── L3: Campaign Planning
  │   │   ├── L3: Lead Management
  │   │   └── L3: ROI Analysis
  │   └── L2: Sales Management
  │       ├── L3: Opportunity Management
  │       ├── L3: Quotation Management
  │       └── L3: Contract Management
  ├── Product Delivery
  │   └── ...
  └── Customer Service
      └── ...

Level 1: Supporting Capabilities
  ├── Finance & Accounting
  ├── Human Resources
  ├── IT Management
  └── Legal & Compliance
```

**Capability Heatmap Assessment Dimensions:**
- Strategic Importance: 1 (Low) — 5 (Critical)
- Current Maturity: 1 (Manual) — 5 (World-Class)
- IT Coverage: 1 (No system support) — 5 (Fully Automated)
- Competitive Differentiation: Generic / Differentiating / Core Competency

**Heatmap Output Format:**
| Business Capability | Strategic Importance | Current Maturity | IT Coverage | Gap (Importance - Maturity) | Improvement Priority |
|--------------------|---------------------|------------------|-------------|-----------------------------|---------------------|
| Customer 360 View | 5 | 2 | 1 | 3 | High |
| Intelligent Pricing | 4 | 1 | 1 | 3 | High |
| Financial Reporting | 3 | 4 | 4 | -1 | Low |

#### 2.2 Value Stream Mapping

Select 1-3 core value streams and map end-to-end processes:

```
Value Stream: Order-to-Cash

[Customer Order] → [Credit Check] → [Order Confirmation] → [Warehouse Picking] → 
[Logistics Delivery] → [Customer Sign-off] → [Invoicing] → [Payment Reconciliation]

Annotate each node with:
- Current Pain Point: [e.g.: Manual credit check, takes 2 days]
- Current System: [e.g.: Excel + Email]
- Target State: [e.g.: Automated credit scoring, <5 minutes]
- Improvement Lever: [e.g.: Rules engine + external credit bureau API]
```

#### 2.3 Organization Mapping

Business Capability → Responsible Department → Supporting Applications → Key Roles:

| Business Capability | Responsible Dept | Supporting Application | Business Owner | IT Owner |
|--------------------|------------------|------------------------|----------------|----------|
| Customer 360 View | CRM Department | Salesforce | Mr. Zhang | IT Manager Li |
| ... | | | | |

---

### Step 3: Data Architecture Design

**Output**: Data Entity Relationship Diagram + Data Flow Diagram + Data Governance Requirements

#### 3.1 Subject Area Model

Identify data subject areas and establish high-level relationships:

```
Customer Domain    Product Domain    Transaction Domain    Risk Domain
  │                   │                   │                   │
  ├─ Customer MDM     ├─ Product Catalog  ├─ Orders           ├─ Credit Score
  ├─ Customer Profile ├─ Pricing          ├─ Payments         ├─ Fraud Flags
  ├─ Customer Preferences ├─ Inventory    ├─ Fulfillment      ├─ Compliance Audit
  └─ Customer Interactions                └─ Settlement       └─ Regulatory Reports

Cross-domain Data Flow: Customer → Transaction → Risk → Customer (Feedback Loop)
```

#### 3.2 Three Pillars of Data Architecture

| Dimension | As-Is Pain Points | To-Be Design | Migration Strategy |
|-----------|-------------------|--------------|-------------------|
| Master Data Management (MDM) | Customer data scattered across 5 systems, each with its own copy | Unified MDM, single entry with full-chain synchronization | Pilot with Customer and Product domains first, then expand |
| Data Integration Layer | Point-to-point interfaces, N*(N-1) explosion | ESB/API Gateway + Event-driven | Gradually migrate from point-to-point to bus routing |
| Data Analytics Layer | BI reports built in silos | Lakehouse + Semantic Layer + Unified BI | Build data warehouse foundation first, then migrate existing reports |

#### 3.3 Data Governance Brief Design

- Data Owner: Assign a business owner for each subject area
- Data Standards: Master data coding rules / Metadata standards / Data dictionary
- Data Quality: Measure across 5 dimensions — Completeness / Accuracy / Consistency / Timeliness / Uniqueness
- Data Security: Classification tiers (Public / Internal / Confidential / Top Secret)

---

### Step 4: Application Architecture Design

**Output**: Application Landscape Map + Application Interaction Matrix + Application Classification & Disposition Recommendations

#### 4.1 Application Classification (Gartner Pace-Layered)

| Layer | Definition | Characteristics | Lifecycle | Technology Strategy |
|-------|-----------|-----------------|-----------|---------------------|
| **SoR** (System of Record) | Systems of Record: ERP / Core Banking / HIS | Stable, strictly governed, long lifecycle | 10-20 years | Modernize / Wrap / Gradual replacement |
| **SoD** (System of Differentiation) | Differentiating Systems: CRM / Risk Control / Pricing Engine | Moderate change, supports competitiveness | 3-7 years | Refactor / Decouple into microservices |
| **SoI** (System of Innovation) | Innovation Systems: AI Recommendations / Digital Twin | Rapid iteration, experimental | 1-2 years | New build / Cloud-native / Fast experimentation |

#### 4.2 Application Rationalization

Annotate each application with a disposition recommendation:

```
Application: [Name]
├── Type: SoR / SoD / SoI
├── Business Fit: High / Medium / Low
├── Technical Health: High / Medium / Low
├── Disposition: Retain / Upgrade / Replace / Retire / Merge
├── Rationale: [1-2 sentences]
├── Estimated Investment: $[X]M
└── Time Window: [YYYY-QX] — [YYYY-QX]
```

Disposition Matrix:

| | High Business Fit | Medium Business Fit | Low Business Fit |
|---|---|---|---|
| **High Technical Health** | Retain + Continuously Optimize | Observe | Investigate Alternatives |
| **Medium Technical Health** | Upgrade / Refactor | Judge with other factors | Replace / Retire |
| **Low Technical Health** | Modernize / Wrap | Replace (Planned) | Retire Immediately |

#### 4.3 Application Integration Architecture

Map the main interaction relationships among applications:

```
Channel Layer: [Mobile App] [Web] [Mini Program] [Store Terminal] [API Partners]

        ↓ Unified API Gateway ↓

Business Middle Platform: [Order Center] [User Center] [Product Center] [Inventory Center] [Marketing Center]
                ↕ Event Bus ↕
Data Middle Platform: [Data Ingestion] → [Data Processing] → [Data Services] → [Data Applications]

        ↓ Integration Layer ↓

Backend Systems: [ERP] [Finance] [HR] [OA] [SCM]
```

---

### Step 5: Technology Architecture Design

**Output**: Technology Platform Blueprint + Technology Selection Recommendations + Technology Standards & Principles

#### 5.1 Technology Platform Blueprint

Define the logical layers of the target technology platform:

```
┌──────────────────────────────────────────────────┐
│          Security & Compliance Layer (Full-Stack) │
├──────────────────────────────────────────────────┤
│  User Experience Layer: Portal / Mobile / Web     │
├──────────────────────────────────────────────────┤
│  API & Integration Layer: API Gateway / ESB / Event Bus │
├──────────────────────────────────────────────────┤
│  Business Services Layer: Microservices (Containerized) / Serverless │
├──────────────────────────────────────────────────┤
│  Data Services Layer: Lakehouse / MDM / Feature Store │
├──────────────────────────────────────────────────┤
│  AI/ML Platform Layer: MLOps / LLMOps / Agent Framework │
├──────────────────────────────────────────────────┤
│  Infrastructure Layer: Multi-cloud / Hybrid Cloud / IaC / Observability │
├──────────────────────────────────────────────────┤
│  Governance & Operations Layer: CMDB / ITSM / FinOps / DevOps │
└──────────────────────────────────────────────────┘
```

#### 5.2 Key Technology Selection Decisions (not vendor selection — deferred to Phase 3)

| Technology Domain | Strategic Direction | Rationale | Constraints |
|-------------------|---------------------|-----------|-------------|
| Cloud Strategy | Hybrid Cloud (AWS + Private Cloud) | Core data retained on private cloud | Data export compliance |
| Container Orchestration | Kubernetes | Industry standard, ample talent supply | — |
| API Management | Kong / APISIX | Open-source + high performance | Requires in-house operations capability |
| Database | PostgreSQL + Redis + MongoDB | OLTP + Caching + Document | — |
| Message Middleware | Kafka | High throughput + event sourcing | High operations cost |
| CI/CD | GitHub Actions + ArgoCD | Cloud-native GitOps | — |
| Observability | Grafana + Prometheus + OpenTelemetry | Open-source standards | — |

#### 5.3 Architecture Principles

Format: `Principle Name: One-sentence principle → Rationale → Impact`

1. **Cloud First**: New applications default to cloud services (PaaS preferred over IaaS) → Reduces operational burden, elastic scaling → Requires cloud skills development
2. **API First**: All inter-system communication via APIs → Loose coupling, replaceability → Requires API governance
3. **Shift Left Security**: Security review begins at the architecture design phase → Reduces late-stage remediation cost → May slow initial development velocity
4. **Data as an Asset**: Data centrally managed, ownership resides with the business → Breaks down data silos → Requires data governance investment
5. **Automate Everything**: Automatable manual processes should not be done manually → Reduces human error → Higher initial investment

---

### Step 6: Target Architecture Consensus (Architecture Review)

#### 6.1 Architecture Review Board (ARB)

**Participants**: CIO + Business VP Representatives + IT Architecture Lead + Security Lead + Data Lead

**Agenda (90 minutes)**:
1. Architecture Scope & Principles Reaffirmation (5 min)
2. As-Is Architecture Key Findings (15 min)
3. To-Be Architecture Design (30 min): Business → Data → Application → Technology
4. Key Architecture Decision Points Discussion (20 min): 5-7 architecture issues requiring decisions
5. Gap Analysis & Migration Path (10 min)
6. Next Steps & Action Items (5 min)
7. Decision Records (5 min)

#### 6.2 Architecture Decision Record (ADR)

Complete one ADR for each key decision:

```
ADR-[Number]: [Title]

Background: [Why is this decision needed?]
Decision: [What specific decision was made?]
Alternatives: [What other options were considered? Why were they not chosen?]
Impact: [Positive impacts + negative consequences of this decision]
Status: Proposed / Approved / Implemented / Deprecated
Date: [YYYY-MM-DD]
Decision Maker: [Name / Role]
```

---

### Step 7: Gap Analysis & Migration Path

#### 7.1 Gap Matrix

| Architecture Domain | As-Is | To-Be | Gap Description | Remediation Approach | Priority | Estimated Investment |
|---------------------|-------|-------|-----------------|---------------------|----------|----------------------|
| Business: Intelligent Pricing | Manual Excel | AI Dynamic Pricing Engine | No data / No algorithm / No system | New Build | High | $2M |
| Data: Customer 360 | 5 customer tables, no linkage | Unified MDM + CDP | Data standards / Integration / Governance | Rework | High | $1.5M |
| Application: Legacy ERP | 15-year-old Oracle EBS | SaaS ERP | 10 years of technical debt | Replace | Medium | $5M |
| Technology: Containerization | VM-based Deployment | Kubernetes | Operations / Monitoring / Processes | Upgrade | Medium | $0.5M |

#### 7.2 Migration Roadmap

```
Wave 1 (0-6 months): Foundation Readiness
├── API Gateway Deployment
├── CI/CD Pipeline Setup
├── First microservice pilot (choose low-risk scenario)
└── Data platform foundation setup

Wave 2 (6-18 months): Core Migration
├── SoD system microservice-based transformation (2-3 systems)
├── Master Data Management (MDM) Phase 1 Go-Live
├── Containerized migration (30% of workloads)
└── Event-driven architecture pilot

Wave 3 (18-30 months): Scaling
├── SoR system wrapping
├── Full containerization (80%+ of workloads)
├── AI platform integration into architecture
└── Full-chain observability Go-Live

Wave 4 (30-36 months): Optimization & Innovation
├── Automated governance
├── Agentic AI integration
└── Continuous architecture evolution mechanism
```

---

## Outputs
1. **Architecture Definition Document (ADD)**: Contains all four architectures — Business / Data / Application / Technology
2. **Architecture Decision Records (ADR)** x N
3. **Gap Analysis Matrix**
4. **Migration Roadmap**

---

## Quality Checklist

- [ ] All four architecture layers (Business / Data / Application / Technology) are complete with no gaps
- [ ] Clear gap analysis exists between As-Is and To-Be
- [ ] Each gap has a specific remediation approach and timeline
- [ ] Architecture principles are explicit, with rationale and impact descriptions
- [ ] Key architecture decisions have ADR records
- [ ] Technology selections have clear rationale and constraints
- [ ] Migration Roadmap has clear Wave divisions
- [ ] Business capability heatmap covers all core business domains

---

## Common Pitfalls

| Pitfall | Why It's Wrong | Correct Approach |
|---------|---------------|------------------|
| "Paper Architecture" | Architecture design disconnected from actual implementation | Every To-Be design should annotate the name of the first system to implement it |
| Over-Engineering | "We need a middle platform supporting 10 billion concurrent users" — actual DAU is 2,000 | Design for 3-year business scale, reserve extension points, don't build prematurely |
| Architecture Review by Voting | 10 people review, each gives one suggestion, and in the end no one can explain why the architecture looks this way | Define a clear Architecture Owner; review is for "raising concerns / identifying risks," not "making decisions for the architect" |
| Ignoring Legacy System Personnel Dependencies | "This system is too old, replace it" — but only Old Li understands it, and Old Li is about to retire | Prioritize systems with key-person dependencies; tacit knowledge extraction must happen before retirement |
| Chasing the Newest Technology | "Use the latest, hottest tech" — no one on the team knows it, and you can't hire for it | Evaluate the triangle of "Team can master it + Active community + Stable vendor" |
