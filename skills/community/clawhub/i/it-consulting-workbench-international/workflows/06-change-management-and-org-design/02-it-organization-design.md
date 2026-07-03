# IT Organization Design

## Objectives

Design a high-performance IT organization aligned with IT strategy and digitalization goals, including organizational structure, role definitions, capability models, headcount sizing, and transition plan.

---

## Prerequisites
- IT strategic direction confirmed
- Current IT organization assessed (from diagnostic phase)
- Understanding of the enterprise's organizational culture and talent market conditions

## Inputs
- IT strategic plan (from workflow 03-01)
- IT current-state diagnostic report — Organization dimension (from workflow 02-03)
- Current IT organization chart + personnel roster
- Enterprise-wide organization chart (to understand IT's positioning within the enterprise)

---

## Operation Steps

### Step 1: Define IT's organizational positioning

#### 1.1 Three roles of IT within the enterprise

| Role | Definition | IT's Positioning | Typical Org Form |
|------|------|---------|------------|
| **Utility** | IT = cost center; goal is "stable + cost-efficient" | CIO reports to CFO | Centralized, operations-heavy |
| **Partner** | IT = business enabler; goal is "empower business growth" | CIO reports to CEO | BU Partners + shared platform |
| **Driver** | IT = core competitiveness; goal is "create new business with technology" | CIO/CTO = core leadership | Productized / Platform-based, technology embedded in business |

**Key Decision:** What role should the client's IT organization play? This determines not only org design but also the CIO profile and compensation level.

#### 1.2 IT organization evolution direction

```
Traditional IT Organization:          Modern IT Organization:

CIO                                   CIO/CDO/CTO
├── Application Development           ├── Product & Platform
├── Infrastructure                    │   ├── Product Line A (business-aligned)
├── Operations                        │   ├── Product Line B
├── Security                          │   └── Platform Engineering (shared)
├── Data (if exists)                  ├── Enterprise Architecture & Security
└── PMO                               ├── Data & AI
                                      ├── Infrastructure & Cloud
                                      └── Operations & Support

"Order Taker"                         "Value Creation Partner"
```

---

### Step 2: Organizational structure design

#### 2.1 IT organization model selection

| Model | Description | Strengths | Weaknesses | Best For |
|------|------|------|------|------|
| **Centralized** | All IT resources under unified management | Standardization + efficiency + cost control | Slow to respond to business | Small-to-medium enterprises |
| **Federated** | HQ IT + BU IT | Balances standards with flexibility | Redundancy + high coordination cost | Diversified large enterprise groups |
| **Productized** | IT organized by product line / value stream | Good business alignment + fast | Potential duplication | Digital-native enterprises |
| **Platform + Product** | Shared platform (infrastructure/data) + product teams (business-facing) | Balances efficiency with flexibility | Requires strong governance and collaboration | Mid-to-large enterprises undergoing digital transformation |

**Recommended evolution path:**

```
Most traditional enterprises:
Centralized → Platform + Product → (once mature) can choose further productization or maintain Platform + Product
```

#### 2.2 Platform + Product model detailed design

```
┌─────────────────────────────────────────────────┐
│                  CIO / CTO                       │
├─────────────────────────────────────────────────┤
│                                                   │
│  ┌──────────── Product Lines ──────────┐          │
│  │                                     │          │
│  │ Product VP (business-aligned)       │          │
│  │  ├── Product Team: Customer Domain  │          │
│  │  │   └── PM + Dev + UX + Data      │          │
│  │  ├── Product Team: Transaction      │          │
│  │  │       Domain                     │          │
│  │  ├── Product Team: Risk Domain      │          │
│  │  └── Product Team: Data Intelligence│          │
│  │                                     │          │
│  └─────────────────────────────────────┘          │
│                                                   │
│  ┌──────────── Platform Layer ──────────┐         │
│  │                                     │          │
│  │ Platform VP (shared capabilities)   │          │
│  │  ├── Cloud & Infrastructure Platform│          │
│  │  ├── Data Platform                  │          │
│  │  ├── Security & Compliance Platform │          │
│  │  ├── DevOps / Toolchain Platform    │          │
│  │  └── Enterprise Architecture        │          │
│  │                                     │          │
│  └─────────────────────────────────────┘          │
│                                                   │
│  ┌──────────── Centers of Excellence ──┐          │
│  │  AI CoE | Agile CoE | Architecture  │          │
│  │                    CoE              │          │
│  └─────────────────────────────────────┘          │
│                                                   │
└─────────────────────────────────────────────────┘

Product Teams: "We own what to build + how to build it" (What + How for Business)
Platform Teams: "We provide reusable capabilities so product teams don't reinvent the wheel"
CoE: "We provide best practices / tools / methodologies so no one repeats the same mistakes"
```

#### 2.3 Key role definitions

| Role | Reports To | Core Responsibilities | Required Capabilities |
|------|--------|---------|----------|
| **CIO** | CEO / CFO | IT strategy + IT-business alignment + major investment decisions | Strategic thinking + business acumen + leadership |
| **CTO** | CIO / CEO | Technology strategy + architecture + technology foresight | Deep technical expertise + innovation + engineering culture |
| **CDO / CDAO** | CIO / CEO | Data strategy + data governance + AI implementation | Data + AI + business acumen |
| **Product VP** | CIO | Product line P&L (if applicable) + product strategy | Product management + business + technology |
| **Platform VP** | CIO | Platform capability building + SLA + efficiency | Architecture + engineering + DevOps |
| **CISO** | CIO / Board | Security strategy + risk + compliance | Security + risk + business communication |
| **Product Manager** | Product VP | Product vision + roadmap + requirement prioritization | Product + user research + data analysis |
| **Engineering Manager** | Product VP / Platform VP | Team + delivery + engineering quality | Technical + management + agile |
| **Site Reliability Engineer** | Platform VP | Availability + performance + automated operations | Deep technical + systems thinking + coding |
| **Data Engineer** | Data Platform | Data pipelines + data quality + data platform | Data engineering + distributed systems |

---

### Step 3: Team sizing and capability planning

#### 3.1 Headcount benchmarks

| IT Staff as % of Total Employees | Industry |
|-----------------|------|
| 2–4% | Manufacturing / Traditional Retail |
| 4–7% | Financial Services / Insurance |
| 7–12% | Enterprises undergoing digitalization |
| 20–50% | Technology / Software / SaaS enterprises |

#### 3.2 Staff composition ratios

World-class IT organization staff distribution:

| Category | Share | Notes |
|------|------|------|
| Product / Business-aligned roles (PM / BA / Product Designer) | 20–25% | Ensure technology builds what the business needs |
| Platform / Engineering roles (Engineers / Architects / SRE) | 45–55% | The real "builders" |
| Operations / Support roles | 10–15% | Gradually decreases with automation |
| Security / Compliance | 5–8% | |
| Management / PMO | 5–7% | |

**Warning:** If Ops/Support > 25%, automation level is too low; if Management/PMO > 10%, management layer is bloated.

#### 3.3 Skill gap matrix

| Key Skill | Current Headcount | Needed Headcount | Gap | Fill Method (Hire / Train / Outsource) |
|---------|---------|---------|------|---------------------|
| Cloud Architecture (AWS/Azure) | 2 | 8 | +6 | Hire 3 + Internal train 3 |
| AI/ML Engineering | 0 | 5 | +5 | Hire 2 (Lead) + Train 3 |
| Product Management | 1 | 6 | +5 | Hire 3 (external) + Transition 2 (internal BAs) |
| DevOps / SRE | 3 | 10 | +7 | Train 5 + Hire 2 |
| Data Engineering | 1 | 8 | +7 | Hire 4 + Train 3 |
| Legacy Systems (COBOL...) | 3 (near retirement) | 2 (transitional) | -1 | External vendor |---

### Step 4: Talent strategy

#### 4.1 Build-Buy-Rent decisions

| Role Type | Strategy | Rationale |
|---------|------|------|
| Core architecture / tech decisions | **Build** (train/hire) | Core capability cannot be outsourced |
| General development / testing | **Rent** (outsource) | Flexible scaling, predictable cost |
| Scarce high-end talent (AI / Security) | **Buy** (hire at premium) | Compete in the talent market |
| Legacy system maintenance | **Rent** (outsource) | Transitional strategy |
| Business Analysts | **Build** (internal transition) | Business knowledge > technical knowledge |
| Operations (non-core) | **Rent** (managed services) | Automate + outsource |

#### 4.2 Key retention strategies

IT staff turnover is typically 15–25%, higher than the enterprise average. Retention strategies:

| Factor | Why It Matters | Recommendation |
|------|----------|------|
| Technical growth | IT staff fear "skill erosion" most | Training budget ≥ $3K/person/year; quarterly learning days |
| Meaningful work | No one wants to only fix bugs / write reports forever | Include engineers in business discussions so they understand "why we're building this" |
| Modern tooling | Using antiquated tools = driving away your best people | Even if core systems are old, at minimum DevOps/toolchain should be modern |
| Compensation | Talent market pricing is transparent | At least 50th percentile; key talent at 75th+ percentile |
| Autonomy | Engineers hate being micro-managed | Grant technical decision autonomy (within architecture framework) |
| Dual career track | Not everyone wants / is suited for management | Management track + Expert track (Principal → Distinguished → Fellow) |

---

### Step 5: Transition plan

#### 5.1 Transition from old to new organization

```
Phase 1: Lay the Foundation (0–3 months)
├── Finalize new org structure
├── Appoint key leaders (CIO direct reports)
├── Communicate org changes: who goes where
├── Identify "affected" people: roles disappearing/changing — one-on-one conversations
└── Establish the first product team (pilot)

Phase 2: Core Transition (3–9 months)
├── Expand product teams to 2–3
├── Platform team transitions from infrastructure team
├── First batch of training / role transitions completed
├── Agile / DevOps practices proven in pilot teams
└── Identify "change blockers" and address them

Phase 3: Scale (9–18 months)
├── Entire organization operating under new structure
├── CoE operations normalized
├── Talent market strategy ongoing
└── Organizational health review + adjustments
```

#### 5.2 The human dimension of organizational change

```
Who is most affected?
├── Middle IT managers: From "people management" → "leading teams to build products" — capability requirements completely different
├── Senior technical experts: Tech stack changed; from "the most knowledgeable" → "must learn" — identity crisis
├── Operations staff: From "manual operations" → "writing code to automate" — core skills changed
└── Business liaisons (BAs): From "message passers" → "product managers" — core role changed

Everyone needs:
- Clear communication: "What your new role is, why, and how to transition"
- Training / transition period: Not "starting tomorrow you're a DevOps engineer"
- Choice: "You have these options: learn new skills / transfer roles / take severance and leave (with respect)"
```

---

## Outputs
1. **IT Organization Positioning Statement**: Role + reporting line + evolution direction
2. **Target Organization Chart**: Including key roles and headcount
3. **Role & Responsibility Descriptions**: Key role R&R
4. **Headcount & Structure Plan**: Headcount + composition + skill gaps
5. **Talent Strategy**: Build-Buy-Rent + retention strategy
6. **Transition Plan**: Three-phase transition + affected personnel placement

---

## Quality Check
- [ ] Organization design supports IT strategy (not a generic template)
- [ ] Key roles have clear responsibilities and required capabilities
- [ ] Skill gaps have concrete fill plans (not just "need to hire")
- [ ] Transition plan addresses "affected people" (not just the org chart)
- [ ] Staff composition ratios are reasonable (Ops < 15%, Management < 10%)
- [ ] CIO's positioning and reporting line are clearly defined

---

## Common Pitfalls

| Pitfall | Why It's Wrong | Correct Approach |
|------|---------|---------|
| Redrawing the org chart = org design | Drawing lines is easy, but changing people's behavior / capabilities / culture is the real org design | The org chart is only 10% of the work; 90% is transition + capability building + culture |
| Copying internet companies | "Let's do flat structure + product + agile too" — but management isn't ready to delegate, culture doesn't match | Design transition approach based on the enterprise's actual culture; sometimes "evolution" is more viable than "revolution" |
| CIO positioned too low | If CIO reports to CFO, IT will always be seen as a cost center — impossible to drive digitalization | Advocate for CIO reporting to CEO (at minimum a dotted line) |
| Ignoring middle managers | Middle managers are the most critical and hardest layer in org change — they lose the most power and need to change the most | Spend the most time on middle management: training / coaching / 1-on-1s / giving them new positioning |
| Mass layoffs instead of transformation | "Get rid of the old, hire new" — loses business knowledge, destroys morale, and new hires may not be better | Prioritize training / transition opportunities for existing staff; layoffs are a last resort |