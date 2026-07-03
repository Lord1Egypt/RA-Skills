# IT Consulting Core Methodology Library

> This document is a deep reference, not meant to be read in one sitting. Refer back here when using specific methodologies in relevant workflows.

---

## 1. MECE Principle (Mutually Exclusive, Collectively Exhaustive)

### Core Concept
MECE is the cornerstone of structured thinking. Any problem decomposition must satisfy:
- **Mutually Exclusive**: Parts do not overlap with each other
- **Collectively Exhaustive**: Parts together cover everything

### Classic MECE Decompositions in IT Consulting

**IT Capability Five-Dimensional Decomposition** (Most Common):
```
IT Capability = Technology + Process + Organization + Data + Finance
```

**IT Investment Tripartite:**
```
Total IT Spend = Run (Operations) + Grow (Growth) + Transform (Transformation)
```

**Application System Tripartite (Pace-Layered):**
```
Application Portfolio = SoR (Systems of Record) + SoD (Systems of Differentiation) + SoI (Systems of Innovation)
```

**Technology Stack Layering:**
```
Technology Stack = Infrastructure Layer + Platform Layer + Application Layer + Channel/Access Layer + Security Layer
```

**IT Problem Diagnosis Five Dimensions:**
```
Problem Root Cause ∈ {Technical Cause, Process Cause, Organizational Cause, Data Cause, External Cause}
```

### MECE Self-Check Checklist
Ask yourself after each decomposition:
1. ME Check: "Do any two branches describe the same thing?"
2. CE Check: "Is any possibility omitted?"
3. Same-Level Check: "Are all branches at the same level of abstraction?"

---

## 2. Hypothesis-Driven Approach

### Traditional vs Hypothesis-Driven

| | Traditional Approach | Hypothesis-Driven |
|------|---------|---------|
| Starting Point | Data | Hypothesis |
| Path | Collect → Analyze → Discover → Conclude | Hypothesize → Validate → Iterate |
| Efficiency | Analyze 100%, 80% is wasted effort | Only analyze the critical 20% |
| Typical Problem | Analysis paralysis | Confirmation bias (requires vigilance) |

### Hypothesis-Driven Core Process
1. **Day 1 Propose Hypothesis**: Based on experience and preliminary information
2. **Design Validation Plan**: "If X is true, we should observe Y"
3. **Rapid Validation**: Falsify or confirm within 48 hours
4. **Iterative Refinement**: Keep what is confirmed, correct what is falsified
5. **Form Preliminary Judgment by Day 3-4**

### Hypothesis Formulation Standards
- Bad: "System performance is poor"
- Good (Verifiable): "If the core transaction system performance is the bottleneck, we should observe P99 response time >500ms, and peak CPU utilization >85%"

---

## 3. Pyramid Principle

### Structure
```
         ┌──────────────┐
         │ Core Conclusion│  ← Answer first
         └──────┬───────┘
    ┌───────────┼───────────┐
┌───┴───┐   ┌───┴───┐   ┌───┴───┐
│Argument 1│ │Argument 2│ │Argument 3│  ← Key arguments supporting conclusion
└───┬───┘   └───┬───┘   └───┬───┘
 Data/Facts   Data/Facts   Data/Facts    ← Evidence supporting arguments
```

### Four Iron Rules
1. Arguments at any level must be summaries of sub-level arguments (Summary)
2. Same-level arguments must follow MECE
3. Same-level arguments must be arranged in logical order (Deductive / Temporal / Structural / Degree)
4. Each argument must have at least 2 supports, at most 7 (2-7 Rule)

### SCQA Narrative Framework (for Executive Summaries and Presentation Openings)
- **S**ituation: "What environment are we in?" — Current state, consensus, non-controversial
- **C**omplication: "What has changed?" — Problem, challenge, opportunity
- **Q**uestion: "What core question needs to be answered?"
- **A**nswer: "What is my recommendation?" (Give directly)

---

## 4. 80/20 Rule (Pareto Principle)

### Applications in Consulting
- **Problem Discovery**: 20% of systems may cause 80% of failures, focus on these 20%
- **Problem Analysis**: 20% of analysis dimensions may contribute 80% of insights, do these first
- **Problem Solving**: 20% of initiatives may produce 80% of benefits, prioritize into Wave 1

### Practical: How to Find the 20%
1. List all possible factors / findings / recommendations
2. Score each (Impact Level 1-5)
3. Keep only those scoring 4-5
4. Ask yourself: "If we could only do 3 things, which would we regret NOT doing?"

---

## 5. Issue Tree vs Hypothesis Tree vs Driver Tree

| Type | Structure | Data Needs | When to Use | Output |
|------|------|---------|---------|------|
| Issue Tree | Decompose by logic/category | No data needed | Problem definition phase — "Where might the problem be?" | All possible causes |
| Hypothesis Tree | Decompose by hypothesis, each branch verifiable | Small amount of data | Exploration phase — "What is the most likely cause?" | Verified / disproven hypotheses |
| Driver Tree | Decompose by mathematical relationships | Data needed | Quantification phase — "How large is each factor's impact?" | Quantified impact ranking |

### Usage Sequence
Issue Tree (Broad exploration) → Hypothesis Tree (Focused validation) → Driver Tree (Quantify impact)

---

## 6. Root Cause Analysis

### 5-Why Technique
Ask "Why" 5 consecutive times until reaching the true systemic issue:

```
Symptom: New feature launches too slow (4 months)
Why 1: Because post-development testing takes 3 weeks
Why 2: Because full regression testing is done every time
Why 3: Because automated test coverage is only 15%
Why 4: Because the team has never been required to write tests in the past 3 years
Why 5: Because performance evaluation only measures "number of features launched", not "quality and technical debt"

Surface Cause: Testing is too slow
Root Cause: Performance evaluation system incentivizes short-term delivery, penalizes long-term quality investment
```

### Fishbone Diagram (Ishikawa Diagram)
Place the problem at the "fish head", expand possible causes from 4-6 dimensions:
```
                   People          Process
                      \           /
                       \         /
                        \       /
              Technology —— Problem —— Data
                        /       \
                       /         \
                      /           \
                   Systems       External
```

---

## 7. Common Strategy Framework Quick Reference

### McKinsey 3 Horizons
| Horizon | Timeframe | Focus | IT Focus |
|---------|------|------|--------|
| H1 | 0-12 months | Defend and extend existing business | Efficiency improvement / cost optimization / stable operations |
| H2 | 12-36 months | Build emerging business | New platform construction / digital capabilities / data-driven |
| H3 | 36 months+ | Create future options | Frontier technology experimentation / AI innovation / ecosystem building |

### McKinsey 7S
Hard Elements: **S**trategy → **S**tructure → **S**ystems
Soft Elements: **S**hared Values → **S**tyle → **S**taff → **S**kills

### Porter 5 Forces (for Industry Competition Analysis)
1. Threat of New Entrants
2. Bargaining Power of Suppliers
3. Bargaining Power of Buyers
4. Threat of Substitutes
5. Intensity of Rivalry Among Existing Competitors

### PESTEL (Macro Environment Analysis)
**P**olitical → **E**conomic → **S**ocial → **T**echnological → **E**nvironmental → **L**egal

### SWOT (Internal + External Integrated Analysis)
Internal: **S**trengths + **W**eaknesses
External: **O**pportunities + **T**hreats
→ Cross Analysis: SO Strategy (use strengths to seize opportunities) / WT Strategy (remedy weaknesses to defend against threats)

---

## 8. IT-Specific Framework Quick Reference

### TOGAF ADM (Architecture Development Method)
10 phases, requirements management throughout:
Preliminary → A.Vision → B.Business Architecture → C.IS Architecture (Data+App) → D.Technology Architecture → E.Opportunities & Solutions → F.Migration Planning → G.Implementation Governance → H.Architecture Change Management

### Well-Architected Framework (Cloud Architecture Best Practices)
Five Pillars: Operational Excellence / Security / Reliability / Performance Efficiency / Cost Optimization

### ITIL 4 (IT Service Management)
Service Value Chain: Plan → Improve → Engage → Design & Transition → Obtain/Build → Deliver & Support

### 6R Cloud Migration
Retire → Retain → Rehost → Replatform → Refactor → Reimagine
(Arranged from lowest to highest disruption)

### NIST CSF 2.0 (Cybersecurity Framework)
Six Functions: GOVERN → IDENTIFY → PROTECT → DETECT → RESPOND → RECOVER

### FinOps Maturity
Three Phases: Inform → Optimize → Operate

---

## 9. Framework Selection Decision Tree

```
What problem are you facing?
│
├── Problem unclear, need to define the problem itself → Issue Tree + MECE
├── Problem clear, need to find root cause → 5-Why + Fishbone Diagram
├── Need to develop strategy → McKinsey 3 Horizons + SWOT + PESTEL
├── Need organizational design → McKinsey 7S
├── Need to assess industry position → Porter 5 Forces
├── Need to make investment decisions → NPV/IRR + Decision Tree + Sensitivity Analysis
├── Need to manage change → Kotter 8-Step + ADKAR
├── Need to design IT architecture → TOGAF ADM
├── Need to migrate to cloud → 6R + Well-Architected
├── Need to conduct security assessment → NIST CSF 2.0
├── Need to do AI planning → AIM² + RICE+ + 5D Framework
└── Need to optimize costs → FinOps + TCO + TBM
```


---
## 10. McKinsey AI Value Creation Three Waves

### Three Waves Overview
| Wave | Timeframe | Core Characteristics | Value Creation |
|------|------|---------|---------|
| Wave 1: Technology Enablement | 2022-2024 | AI as efficiency tool embedded in existing processes | Efficiency improvement 10-30% |
| Wave 2: Process Reinvention | 2024-2027 | AI redesigns end-to-end business processes | Process efficiency 50-200% improvement |
| Wave 3: Business Model Innovation | 2027+ | AI becomes core product/service/business model | New revenue streams, industry rules rewritten |

### GenAI Implementation Gap
- 46% of enterprises deploy GenAI at scale, but only 9% achieve significant business value
- Three root causes: Insufficient data readiness (62%), Talent shortage (55%), Governance gap (48%)

### AI High Performer Six Profiles
| Dimension | High Performers | Laggards |
|------|---------|--------|
| Strategy | CEO-level AI agenda, AI budget >15% | AI = IT department spontaneous activity |
| Organization | AI team embedded in business units | Isolated lab, disconnected from business |
| Data | Enterprise data platform + data product mindset | Data silos, manual ETL |
| Technology | MLOps L3+, experiment→production <90 days | Single-machine training, manual deployment |
| Culture | Fail Fast, Learn Faster | Fear of failure or blind hype chasing |

---
## 11. Digital Transformation Five-Force Diagnostic Model

| Dimension | Diagnostic Question | Maturity Signal |
|------|---------|----------|
| Strategy Force | Is digital strategy clear? Aligned with business? | Board-level digital agenda |
| Organization Force | Digital leadership and talent? | CDO appointed, digital talent >15% |
| Process Force | Are core processes digitized? | End-to-end coverage >60% |
| Technology Force | Does IT architecture support rapid innovation? | Cloud adoption >60%, API-fication >50% |
| Data Force | Is data the foundation for decision-making? | Data-driven decision coverage >50% |

Eight-Step Advancement Method: Assess current state → Define vision → Identify gaps → Prioritize → Design roadmap → Establish transformation office → Lighthouse projects → Scale promotion

---
## 12. FinOps Cloud Financial Management Deep Framework (AISMM Four-Stage Evolution)

| Stage | Capability | Enterprise Share | Core Output |
|------|------|---------|---------|
| Stage 1: Observable | Visualization + Tags >90% | 100% | "Where is money spent" |
| Stage 2: Attributable | Showback + Chargeback | 85% | "Who spent the money" |
| Stage 3: Optimizable | Automated Rightsizing | 40% | "Waste auto-eliminated" |
| Stage 4: Evolvable | AI prediction + Self-optimization | <5% | "Costs adapt with business" |

Key Data (Flexera 2024): 84% of enterprises cite cloud cost as top challenge, 67% exceed budget, 82% have at least 10% waste

---
## 13. Zero Trust Security Architecture (NIST SP 800-207)

Three Core Principles: ① Never trust, always verify ② Least privilege (JIT+JEA) ③ Assume breach

Three Technical Paths: SASE (Cloud-native security + SD-WAN) / ZTNA (Application-level tunnel replacing VPN) / Micro-segmentation (Fine-grained between workloads)

2026 Trends: AI adaptive policies, ITDR becoming independent category, OT/IoT zero trust framework maturing

---
## 14. Technology Due Diligence Five-Dimension Framework (Bain Methodology)

| Dimension | Weight | Checklist Items | Common Red Flags |
|------|------|--------|---------|
| Architecture Quality | 25% | 20+ | Circular dependencies, no documentation |
| Engineering Practices | 20% | 25+ | Test coverage <30% |
| Security Posture | 20% | 20+ | Known vulnerabilities >90 days unpatched |
| Data Quality | 15% | 15+ | No data dictionary |
| Team Capability | 20% | 20+ | Key person dependency (Bus Factor=1) |

Valuation Impact Quantification: Technical debt quantified in $, directly affecting valuation model

---
## 15. Digital China Construction 2025 Action Plan

- "Data Element ×" Three-Year Action Plan: Data as production factor, promoting asset recognition on balance sheets
- Xinchuang Domestic Substitution: Full-stack localization of CPU/OS/DB/Middleware/Applications (2027 target for Party & government + central SOEs)
- Digital Government: One-stop government services, unified urban governance, integrated government collaboration
- Digital Infrastructure: 5G / Gigabit optical network / Computing power network / Data exchanges