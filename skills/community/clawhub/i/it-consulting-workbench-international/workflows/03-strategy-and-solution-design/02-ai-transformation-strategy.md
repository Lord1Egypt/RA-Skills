# 02 — AI Transformation Strategy

## Objectives
Help clients develop an overall AI transformation strategy — from assessing the current state, to identifying high-value use cases, to planning the technology platform and talent system, ultimately forming an actionable phased AI Roadmap.

## Prerequisites
- IT current state diagnosis (especially data dimension) completed
- Client business strategy understood
- Client AI-related investments and project information collected

## Inputs
- Diagnostic Report (especially data and technology dimensions)
- Client AI initiative inventory (completed/ongoing/planned)
- Industry AI use case benchmarking

---

## Operation Steps

### Step 0: AI Macro Positioning — McKinsey Three Waves of AI Assessment

Before assessing maturity, help the client position which wave of AI value creation they are currently in:

| Wave | If the client... | Consulting Recommendation |
|------|-----------|---------|
| Wave 1 (Efficiency Boost) | Just starting AI, focused on single-point efficiency use cases | Strengthen data + tech foundation, 2-3 lighthouse projects |
| Wave 2 (Process Reinvention) | Already has AI success stories, ready to expand | End-to-end process refactoring, Agentic AI pilot |
| Wave 3 (Model Innovation) | High AI maturity, pursuing differentiation | AI-native products, ecosystem platform, external output |

> ⚠️ GenAI Adoption Gap: 46% of enterprises deploy GenAI at scale, but only 9% achieve significant business value. Avoid the trap of "Deployed a model = Transformation complete."

### Step 1: AI Maturity Assessment (AIM² Model) — Take the Temperature First

Before giving any AI recommendations, you must first assess the client's current stage:

```
Dimension            L1 (Point Experiment)   L2 (Dept. Rollout)   L3 (Enterprise Ops)   L4 (AI Native)   L5 (AI Ecosystem)
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
1. Strategy & Leadership    ⬤                                              ○ Target
2. Organization & Talent        ⬤                                          ○ Target
3. Data Foundation          ⬤                                              ○ Target
4. Technology Capability        ⬤                                          ○ Target
5. Application Scenarios    ⬤                                              ○ Target
6. Business Value               ⬤                                          ○ Target

● = Current State  ○ = 12-Month Target  ☆ = 24-Month Target
```

**Key benchmarks when scoring each dimension:**

```
Strategy & Leadership:
  L1: AI is an IT department spontaneous activity, no executive involvement → 1 point
  L2: CIO supports AI, has budget but no company-level strategy → 2 points
  L3: CEO/Board clearly defines AI strategic positioning, enterprise-level budget → 3 points
  L4: Every business decision considers AI capability, CDO/CAIO reports directly to CEO → 4 points
  L5: AI becomes core competitiveness, externally exporting AI capabilities → 5 points

Organization & Talent:
  L1: 0-2 people doing AI part-time → 1 point
  L2: 3-10 person small team, dependent on external → 2 points
  L3: 30+ person AI CoE, each BU has AI liaison → 3 points
  L4: AI engineers embedded in every product/business team → 4 points
  L5: Organization-wide AI literacy, AI-Native hiring standards → 5 points

Data Foundation: (This is the dimension that most often gets stuck)
  L1: Data silos, manual consolidation → 1 point
  L2: Partial data centralization, has BI → 2 points
  L3: Enterprise data platform, data governance framework, basic tagging system → 3 points
  L4: Data Products + federated governance, real-time data pipelines → 4 points
  L5: AI-ready data ecosystem, automated governance → 5 points
```

**Key Insight: Most traditional enterprises are between L1-L2. Jumping directly from L1 to L3 is almost doomed to fail — you must first strengthen the data foundation.**

### Step 2: AI Opportunity Identification Workshop

**Workshop Design (half-day, 15-25 people):**

```
Participants: Business VP ×3-5 + IT ×3-5 + Data/AI ×2-3 + Product/Innovation ×2-3

Agenda:
09:00-09:30  AI Capability Overview (not deep tech, but a case collection of "what AI can do now")
09:30-10:30  Group Brainstorming: "If AI could help us solve our 3 biggest business problems,
             what would those problems be?" (each group from a different department perspective)
10:30-11:00  Consolidation + Voting: each person gets 3 votes for the most valuable ideas
11:00-12:00  Top 10 initial expansion using the AI Opportunity Canvas
12:00-12:30  Preliminary prioritization + next steps

AI Opportunity Canvas (fill one per idea):
┌────────────────────────────────────────────────┐
│ AI Opportunity Canvas                           │
├────────────────────────────────────────────────┤
│ Business Problem: [The business problem to solve (not a tech problem)] │
│ Current Approach: [Manual method / existing system / ...]              │
│ AI Approach: [How AI intervenes: predict/classify/generate/...]        │
│ Data Source: [What data is needed, is it available now?]               │
│ Success Criteria: [Quantified KPI]                                     │
│ Expected Challenges: [Biggest obstacles]                               │
│ Relevant Use Case References: [Similar cases inside/outside industry]  │
└────────────────────────────────────────────────┘
```

### Step 3: Use Case Prioritization

**RICE+ Extended Model Scoring:**

```
Use Case Scoring Sheet:

Use Case Name: [Description]

Dimension               Weight   Score (1-10)   Weighted   Notes
─────────────────────────────────────────────────────────────────────────
Reach                     ×1        [__]          [__]     Affected users/transaction volume
Impact (Business Impact)  ×2        [__]          [__]     Magnitude of impact on revenue/cost/experience
Confidence                ×1.5      [__]          [__]     Technically feasible? Enough data?
Effort (Implementation ↓) ×1        [__]          [__]     Person-month estimate + tech complexity
Time-to-Value (↓)         ×1.5      [__]          [__]     How soon to see first version results?
Data Readiness            ×2        [__]          [__]     Does required data exist / quality / accessibility
Risk (↓)                  ×1        [__]          [__]     Compliance/ethics/model risk
─────────────────────────────────────────────────────────────────────────
Weighted Total Score: [___]

Priority: ▢ Act Now (>60)  ▢ Next (45-60)  ▢ Wait for Timing (30-45)  ▢ Defer (<30)
```

**Don't spread effort evenly. Recommendations:**
- Select 2-3 high-priority use cases as "Lighthouse Projects"
- Each lighthouse project should produce measurable business results within 3-6 months
- Pick one "almost guaranteed to succeed" (build confidence) + one "game-changing if successful" (breakthrough)

### Step 4: AI Technology Architecture Decisions

See `references/ai-and-business-transformation-framework.md` for the complete technology decision tree.

Core Principles:
1. **Use off-the-shelf whenever possible**: ChatGPT/Claude Enterprise > self-built LLM (unless data absolutely cannot leave premises)
2. **RAG before fine-tuning**: 80% of enterprise AI needs can be met with RAG
3. **Small models first**: In latency/cost-sensitive scenarios, small model + fine-tuning > large model
4. **Agent is the next step, not the first step**: First get single-step AI use cases working, then do Agents

### Step 5: AI Implementation Roadmap

```
Phase 1: Foundation (0-6 months)
  □ AI maturity baseline assessment completed
  □ 2-3 lighthouse projects launched (pick Quick Wins)
  □ Foundational data platform (Data Lakehouse/Catalog) MVP
  □ AI governance framework 1.0 (ethics/bias/security/compliance)
  □ Core team assembled: 3-5 ML engineers + 1 AI product manager
  □ First AI use case Go live + preliminary ROI verification

Phase 2: Scale (6-12 months)
  □ Lighthouse projects produce measurable ROI
  □ Expand from 2-3 use cases to 8-12
  □ MLOps platform deployed (train → deploy → monitor → iterate closed loop)
  □ Data labeling + feature engineering infrastructure
  □ AI CoE expanded to 15-20 people
  □ Business unit AI training (Citizen Data Scientist program)

Phase 3: Transform (12-24 months)
  □ AI embedded in core business processes and products
  □ Agentic AI pilot (starting with simple task automation)
  □ AI ROI accounts for 1-3% of revenue (depending on industry)
  □ Self-developed models surpass general-purpose models in specific domains
  □ AI capabilities externally exported (ecosystem/partners)
  □ Organization transforms to AI-Native (L4)
```

---

## Outputs

- AI Maturity Assessment Report (with 6-dimension radar chart)
- AI Opportunity Map (use case priority matrix)
- AI Technology Architecture Blueprint
- AI Implementation Roadmap (Q1-Q12+)
- Investment estimate and 5-year ROI forecast

## Quality Check

- [ ] All 6 AI assessment dimensions have scores and evidence
- [ ] Each priority use case has a quantified ROI estimate (at least order of magnitude)
- [ ] Data readiness is treated as a key constraint (not an afterthought)
- [ ] Roadmap Phase 1 includes "infrastructure + data + governance + use cases" all four tracks
- [ ] AI ethics/compliance/risk management considered
- [ ] Not only "doing AI" investment, but also "using AI" change management

## Common Pitfalls

| Pitfall | Correct Approach |
|------|---------|
| "We need to build an AI platform" — building the platform first | Platform is step 2; first verify value with concrete use cases |
| AI team built in a corner of IT, no interaction with business | AI team must be embedded in or closely aligned with business teams |
| Thinking "having ChatGPT Enterprise = AI transformation" | General AI tools = 10% efficiency ↑, industry-specific AI = 100% competitiveness ↑ |
| Blindly chasing large models, ignoring data quality | Models determine the ceiling, data determines the floor. Garbage data → Garbage AI |
| AI strategy without an Exit Plan | Every AI project needs Go/No-Go criteria; dare to stop what isn't working |