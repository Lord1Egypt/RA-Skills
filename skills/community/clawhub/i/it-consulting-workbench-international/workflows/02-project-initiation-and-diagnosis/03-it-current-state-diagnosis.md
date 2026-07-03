# 03 — IT Current-State Diagnosis

## Objectives
Conduct a systematic and structured comprehensive diagnosis of the client's IT current state, covering five dimensions: Technology / Process / Organization / Data / Finance. Produce a scorable, comparable, and trackable current-state baseline.

## Prerequisites
- Kickoff meeting completed, team formed
- System/document access permissions obtained
- Stakeholder interviews scheduled (see this phase's 02-Stakeholder Interviews)

## Inputs
- Technical documentation provided by the client (architecture diagrams / system inventory / operations data, etc.)
- Stakeholder interview records
- Industry benchmark data (see `references/benchmark-data-and-industry-metrics.md`)

---

## Operation Steps

### Step 1: Technology Dimension Diagnosis — System / Architecture / Quality Full Scan

**1.1 Application Portfolio Assessment**

For each major system, evaluate using the following matrix:

```
System Name    Type    Business Criticality  Technical Health  Business Fit  Recommended Action
               SoR/    (1-5)                 (1-5)             (1-5)         Keep/Modernize/
               SoD/SoI                                                       Replace/Retire
──────────────────────────────────────────────────────────────────────────────────────────────
Core ERP       SoR     5                     2                 3             Modernize
CRM            SoD     4                     4                 3             Keep
Legacy Reporting SoI   2                     1                 1             Retire
E-commerce Platform SoD 5                    3                 4             Modernize
```

Scoring Criteria:
- Technical Health: 1=Severe technical debt, 5=Modern cloud-native architecture
- Business Fit: 1=Completely unable to meet current business needs, 5=Perfect fit with headroom

**1.2 Technical Architecture Assessment Checklist**

```
□ Architecture Style (Monolithic/Microservices/SOA/Event-driven/Hybrid)
□ Programming Language & Framework Versions (any EOL risks?)
□ Database Type & Version (RDBMS/NoSQL/Graph/TSDB)
□ Middleware/Integration Layer (ESB/API Gateway/Message Queue/ETL)
□ Infrastructure (On-premise DC/Colocation/Public Cloud/Hybrid)
□ Containerization/Orchestration Level (Bare Metal/VM/Container/K8s)
□ CI/CD Maturity (Manual → Automated → Continuous Deployment)
□ Observability (Logging/Metrics/Tracing coverage and tooling)
□ Disaster Recovery & High Availability (RPO/RTO/Cross-AZ/Cross-Region)
□ Tech Stack Consistency (Unified vs. each team chooses their own)
```

**1.3 Technical Debt Rapid Assessment**

```
Dimension              Score (1-10)   Evidence
Code Quality                         [Sonar score/Test coverage/...]
Architecture Complexity              [Coupling degree/Circular dependencies/...]
Documentation Completeness           [Architecture docs/API docs/...]
Operations Maturity                  [Automation rate/Alert effectiveness/...]
Security Baseline Deviation          [Known vulnerability count/Patch latency/...]

Technical Debt Total Score: ___/50
Industry Reference: Top-tier <10, Good 10-20, Watch 20-30, Severe >30
```

### Step 2: Process Dimension Diagnosis — IT Value Stream Efficiency

**2.1 IT Core Process Maturity Assessment**

For each core process, score using CMM/CMMI 5-level scale:

```
IT Core Process          Maturity (1-5)  Key Pain Point                  Industry Benchmark
Requirements Management                  Requirement change rate >30%      Industry target <15%
Architecture Review                      No formal review process
Development Management                   Requirement-to-Go-Live avg ___ days  Top-tier <7 days
Testing Management                       Automated Testing coverage ___%     >80%
Change Management                        Change failure rate ___%           <5%
Release Management                       Release frequency ___/week          Top-tier: on-demand
Incident Management                      MTTR ___ hours                     <1h
Problem Management                       Temporary fix ratio ___%           <20%
Capacity Management                      Resource utilization ___%          60-80%
Vendor Management                        Vendor SLA achievement rate ___%   >95%
```

**2.2 End-to-End Process Efficiency — Deep Dive into 3 Core Value Streams**

Select the 3 most important IT value streams (e.g., "New Feature from Requirement to Go-Live", "Incident from Discovery to Restoration", "New Vendor from Selection to Onboarding") and draw swimlane timing diagrams:

```
Value Stream: New Feature from Requirement to Go-Live
────────────────────────────────────────────────────────────────
Step                    Duration    Wait Time    Bottleneck?
Requirement Proposal & Review  2 days      5 days       ⚠️ Waiting for business confirmation
Technical Solution Design      3 days      2 days
Development                    5 days      1 day
Code Review                    1 day       2 days       ⚠️ Waiting for CR resources
Testing                        3 days      3 days       ⚠️ Environment instability
Release Approval               0.5 days    4 days       ⚠️ Approval chain too long
Go-Live                        0.5 days    0

Total Duration: 32 days | Actual Work Time: 15 days | Wait Waste: 17 days (53%)
Industry Top-Tier: Total duration <7 days, Wait waste <20%
```

### Step 3: Organization Dimension Diagnosis — IT Team and People

**3.1 Organization Structure Analysis**

```
□ Who does IT report to? (CEO vs CFO vs COO — determines IT's strategic positioning)
□ Total IT headcount: ___ people (___% of total company headcount)
□ IT support ratio: ___ employees per IT staff (Industry reference: High-tech 1:20, Manufacturing 1:50, Finance 1:30)
□ In-house vs. Outsourcing ratio: ___ : ___
□ Team geographic distribution: (Same city/Cross-city/Cross-country)
□ Organization structure type: (Centralized/Federated/Product-oriented/Platform+Team)
```

**3.2 IT Talent Skills Matrix**

```
Role/Capability Domain    Required    Current    Gap        Importance
                          Headcount   Headcount
EA/Architect              [x]         [y]        [z]        🔴 Critical
Product Manager           [x]         [y]        [z]        🟡 Important
Agile Coach/Scrum Master  [x]         [y]        [z]        🟢 General
DevOps/SRE                [x]         [y]        [z]        🔴 Critical
Data Engineer             [x]         [y]        [z]        🔴 Critical
AI/ML Engineer            [x]         [y]        [z]        🟡 Important
Security Engineer         [x]         [y]        [z]        🔴 Critical
```

**3.3 Culture and Capability Diagnostic Questions**
- "How long did it take for the last idea to go from proposal to implementation?" → Measures innovation velocity
- "How was the most recent system failure handled?" → Measures engineering culture and operations maturity
- "How does the business team describe IT?" → Measures IT's business partner positioning
- "Why does your best engineer choose to stay here?" → Measures talent attractiveness

### Step 4: Data Dimension Diagnosis — Fuel for AI/Analytics

```
Data Dimension           Current State Score (1-5)   Key Findings
Data Asset Inventory                                  □ Complete data catalog? (Yes/No)
Data Quality Standards                                 □ Key data entity quality: Completeness __% Accuracy __% Timeliness __%
Master Data Management                                 □ Customer/Product/Vendor master data: Unified/Fragmented/Nonexistent
Data Governance                                        □ Data Owners clearly defined? Policies enforced?
Data Accessibility                                     □ Average time for analysts to obtain data: ___ days
Data Security & Privacy                                □ Classification tiers? Masking mechanisms?
BI/Analytics Maturity                                  □ Reporting/Self-service analytics/AI-driven insights/Automated decisions (which level?)
AI Readiness                                           □ Data labeling? Feature engineering infrastructure? Model governance?
```

### Step 5: Finance Dimension Diagnosis — Where Is the Money Going

```
□ Total IT spend: $___M/year (___% of revenue)
□ IT spend per employee: $___/employee/year (Industry benchmark: Finance $15-25K, Manufacturing $5-10K)
□ Run/Grow/Transform: ___%/___%/___% (Target: 50/30/20)
□ Outsourcing spend ratio: ___%
□ Vendor concentration: Top 3 vendors account for ___% of IT spend
□ Cloud spend: $___M/year, estimated waste rate ___% (Industry average: 30-35%)
□ IT budget growth rate over past 3 years: ___%/year
□ Major IT project ROI tracking rate: ___% (how many projects had post-completion ROI evaluation)
```

---

## Outputs

After completing the five-dimension diagnosis, consolidate results into the report used in this phase's `04-diagnostic-report-writing.md`.

Intermediate artifacts:
- Application Portfolio Assessment Matrix
- Technical Debt Scorecard
- IT Process Maturity Radar Chart
- Value Stream Analysis Diagrams (3 streams)
- Organization Skills Gap Matrix
- Data Readiness Score
- IT Spend Structure Pie Chart

---

## Quality Checklist

- [ ] All five dimensions covered (Technology/Process/Organization/Data/Finance)
- [ ] Key metrics for each dimension collected and scored
- [ ] Scores are evidence-backed, not based on "gut feeling"
- [ ] Benchmarked against industry standards
- [ ] Top 3 pain points identified for each dimension
- [ ] Diagnostic findings preliminarily verified with stakeholders (to avoid bias)

## Common Pitfalls

| Pitfall | Correct Approach |
|---------|------------------|
| Only looking at systems, not people | Spend 2 days on technology diagnosis, and at least 1 day each on process/organization diagnosis |
| Subjective scoring ("I feel the technical debt is a 3") | Break down to specific metrics: code duplication rate / test coverage / architecture dependency count / known vulnerability count |
| Diagnosis = Criticism session | Diagnosis is about finding the "improvement starting point," not "proving you're bad." Start with what's being done well |
| Giving up when data is unavailable | Always have a Plan B: estimate based on interviews + annotate confidence level |
