# Cloud Strategy & Migration Planning

## Objectives

Develop the client enterprise's cloud adoption strategy, including cloud goal definition, 6R migration analysis, FinOps framework, and migration roadmap, ultimately producing an executable cloud migration plan.

---

## Prerequisites
- IT Current-State Diagnostic Report completed (understanding existing infrastructure and application portfolio)
- IT strategy / enterprise architecture direction has been preliminarily determined
- Client has directional consensus on "whether to move to the cloud" (if still in the decision phase, a cloud value justification must be done first)

## Inputs
- IT Current-State Diagnostic Report (application inventory + infrastructure inventory + technical debt assessment)
- Enterprise Architecture Design Document (target architecture blueprint)
- Industry compliance requirements (e.g., data export restrictions, information security classified protection requirements)
- Existing IT budget & contracts (understanding existing hardware / software / operations contract expiration dates)

---

## Operation Steps

### Step 1: Cloud Strategy Goal Definition

**Output**: Cloud Strategy on a Page

#### 1.1 Identify Core Drivers for Cloud Adoption

Not "because everyone else is moving to the cloud so we should too" — lock down specific goals from the following dimensions:

| Driver | Key Question | Quantified Goal Example |
|--------|-------------|-------------------------|
| Business Agility | How long does it take for a new application to go from idea to go-live? | From 3 months → 2 weeks |
| Cost Optimization | Is existing infrastructure elastic? | Reduce infrastructure TCO by 25% |
| Global Expansion | Is multi-region deployment needed? | Deploy in 3 regions to meet data residency requirements |
| Innovation Acceleration | Can new technologies like AI / Big Data be adopted quickly? | Go-live 3 AI use cases within 6 months |
| Operations Simplification | How much time does the IT team spend on infrastructure operations? | Reduce infrastructure ops headcount from 10 → 3 |
| Security & Compliance | Does current security capability meet regulatory requirements? | Pass Classified Protection Level 3 / ISO 27001 |

**Fill-in Template:**
```
Our primary reason for moving to the cloud is: [Select 1-2 core drivers]
Specific quantified goals:
- Goal 1: [Metric] from [Baseline] to [Target] within [Timeframe]
- Goal 2: [Same as above]
- Goal 3: [Same as above]
```

#### 1.2 Define Cloud Strategy Model

| Model | Definition | Suitable Scenarios | Unsuitable Scenarios |
|-------|-----------|-------------------|---------------------|
| **Cloud-First** | New applications default to public cloud | Most enterprises | Core systems with hard data residency requirements |
| **Cloud-Only** | Full cloud migration, no data centers retained | Internet-native enterprises | Significant legacy investments not yet fully depreciated |
| **Hybrid** | Core stays on-premises, elasticity / innovation on cloud | Finance / Government / Large Manufacturing | Startups that don't need on-premises deployment |
| **Multi-Cloud** | Use 2+ public clouds simultaneously | Avoiding lock-in / leveraging each provider's strengths | Low cloud maturity, insufficient team capability |

---

### Step 2: Application Portfolio Analysis & 6R Classification

**Output**: Application 6R Classification List

#### 2.1 6R Migration Strategies

| Strategy | Description | Typical Scenario | Effort | Cost | Example |
|----------|-------------|------------------|--------|------|---------|
| **Retire** | Decommission applications no longer needed | Zombie applications, duplicate functionality | Low | Savings | Old reporting system |
| **Retain** | Do not migrate for now, keep on-premises | Regulatory requirements / Recently upgraded / Low value | None | Maintain | Industrial control SCADA |
| **Rehost** (Lift & Shift) | Move as-is to cloud VMs | Fast migration, time-sensitive | Low | Break-even or slightly higher | Old Java app — move to cloud first, optimize later |
| **Replatform** | Move to cloud managed services (e.g., RDS) | Reduce operational burden | Medium | Medium | Self-managed MySQL → RDS |
| **Refactor / Re-architect** | Rewrite as cloud-native | Needs elasticity / frequent changes / high value | High | High (short-term), Low (long-term) | Monolith → Microservices + Containers |
| **Replace** | Replace with SaaS | Non-differentiating functionality | Medium | On-demand | Self-managed email → Office 365 |

#### 2.2 Application Classification Worksheet

| Application | Business Value (1-5) | Technical Health (1-5) | Current Resources | 6R Classification | Migration Priority | Estimated Time | Notes |
|-------------|----------------------|------------------------|-------------------|-------------------|-------------------|----------------|-------|
| Core Transaction System | 5 | 2 | 10 VMs | Replatform | Wave 2 | 6 months | Decouple before migration |
| Customer Service System | 4 | 3 | 5 VMs | Replace (SaaS) | Wave 1 | 3 months | Start 6 months before contract expiry |
| Reporting System A | 2 | 2 | 3 VMs | Retire | Wave 1 | 1 month | Functionality replaced by new BI |
| Risk Control Engine | 5 | 4 | 20 VMs | Refactor | Wave 3 | 12 months | Core IP, in-house development required |
| Industrial Data Collection | 4 | 3 | Edge devices | Retain | — | — | Compliance requires on-premises deployment |

**Classification Principles:**
- If application is approaching EOL (EoL <18 months) → Prioritize Replace / Refactor
- If underlying hardware is approaching expiry → Prioritize Rehost / Replatform (leverage the window)
- If business value is low and a replacement already exists → Retire
- If a major version upgrade was completed within the last 6 months → Retain (wait for next cycle)

---

### Step 3: Cloud Platform Selection & Architecture Design

#### 3.1 Cloud Platform Assessment Dimensions

| Assessment Dimension | Weight | AWS | Azure | GCP | Alibaba Cloud | Huawei Cloud |
|----------------------|--------|-----|-------|-----|---------------|--------------|
| Global Coverage | ×1 | 5 | 5 | 4 | 3 | 2 |
| China Region Availability | ×1.5 | 2 (requires filing via Sinnet) | 3 (21Vianet) | 0 | 5 | 5 |
| AI/ML Services | ×2 | 5 | 4 | 5 | 3 | 3 |
| Compliance Certifications | ×1.5 | 5 | 5 | 4 | 4 | 5 (Classified Protection) |
| Ecosystem / Talent | ×1 | 5 | 4 | 3 | 4 | 3 |
| Cost (same spec) | ×1 | 3 | 3 | 3 | 4 | 4 |

*(Adjust weights and scores based on the client's specific context)*

#### 3.2 Landing Zone Design Elements

Foundational design for the target cloud environment:

| Element | Design Decision | Tool / Service |
|---------|----------------|----------------|
| Account / Subscription Structure | By environment (dev/test/prod) + by BU accounts | AWS Organizations / Azure Management Groups |
| Network Design | Hub-Spoke + Transit Gateway | AWS TGW / Azure vWAN |
| Identity & Access | Enterprise AD/IdP Federation + SSO + MFA | AWS IAM Identity Center / Azure AD |
| Security Baseline | Classified Protection + Industry Compliance + Cloud Security Best Practices | Security Hub / Defender |
| Logging & Audit | Centralized logging + immutable audit logs | CloudTrail / Sentinel |
| Cost Control | Mandatory tagging + budget alerts + auto-shutdown non-production | Budgets / Cost Management |

---

### Step 4: FinOps Deep Framework Design (AISMM Four-Stage Evolution)

#### 4.0 FinOps Maturity Assessment — AISMM Model
Based on the FinOps Foundation's AISMM (AI System Maturity Model), cloud financial management is divided into four evolutionary stages:

| Stage | Capability | Enterprise Adoption | Target Timeline |
|-------|-----------|---------------------|-----------------|
| Stage 1: Observable | Visual dashboards + tag coverage >90% | 100% (Entry) | M1-M3 |
| Stage 2: Attributable | Showback + Chargeback + Unit Economics | 85% | M4-M6 |
| Stage 3: Optimizable | Automated Rightsizing + Scheduling + RI | 40% | M7-M12 |
| Stage 4: Evolvable | AI-driven prediction + self-optimizing infrastructure | <5% | M13+ |

> Benchmark Data: 82% of enterprises have at least 10% cloud spend waste (Flexera 2024). Average savings of 20-40% after FinOps implementation.

### Step 4: FinOps Framework Design

#### 4.1 FinOps Three-Phase Roadmap

```
Phase 1: Inform (Visibility) — M1-M3
├── Enforce mandatory resource tagging policy
├── Build cost visibility dashboards (by BU / Project / Environment)
├── Set budget alerts (account-level + project-level)
└── First monthly cloud bill review meeting

Phase 2: Optimize — M4-M9
├── Rightsizing: Eliminate idle / over-provisioned resources
├── Commitment discounts: RI / Savings Plan (commitment utilization >90%)
├── Auto-scheduling for non-production environments (shutdown 8pm-8am, weekends off, saving 65-75%)
├── Storage lifecycle policies (S3 Intelligent-Tiering / Cool Blob)
└── Data transfer cost optimization (reduce cross-AZ / cross-region traffic)

Phase 3: Operate — M10+
├── Unit economics: Cloud cost per transaction / per user / per API call
├── Continuous FinOps: Automated cost anomaly detection + auto-remediation
├── FinOps KPIs integrated into team performance evaluation
└── FinOps certification (FinOps Foundation Practitioner)
```

#### 4.2 Cloud Cost Estimation Model

```
5-Year TCO Comparison: On-Premises vs. Cloud (aggregated by 6R classification)

                      Year1    Year2    Year3    Year4    Year5    Cumulative
On-Premises (do nothing):
  Hardware purchase/maintenance [$]      [$]      [$]      [$]      [$]      [$]
  Software licenses           [$]      [$]      [$]      [$]      [$]      [$]
  Data center (power/cooling/rent) [$]   [$]      [$]      [$]      [$]      [$]
  Operations personnel        [$]      [$]      [$]      [$]      [$]      [$]
  On-Premises Total           [$]      [$]      [$]      [$]      [$]      [$]

After Cloud Migration:
  Compute (EC2/VM)            [$]      [$]      [$]      [$]      [$]      [$]
  Storage (S3/Disk)           [$]      [$]      [$]      [$]      [$]      [$]
  Network                     [$]      [$]      [$]      [$]      [$]      [$]
  Managed Services (RDS/K8s)  [$]      [$]      [$]      [$]      [$]      [$]
  Support Plan                [$]      [$]      [$]      [$]      [$]      [$]
  Migration transition coexistence cost [$] [—]      [—]      [—]      [—]      [$]
  Cloud Total                 [$]      [$]      [$]      [$]      [$]      [$]

Net Savings: [$] (if negative, non-cost benefits must be justified)
```---

### Step 5: Migration Roadmap

#### 5.1 Four-Wave Migration Plan

```
Wave 1 (0-6 months): Foundation + Quick Wins
├── Landing Zone Deployment (Network / Security / Accounts / Logging)
├── CI/CD Pipeline + IaC (Terraform / CDK)
├── First batch migration: 5-10 low-risk applications (Rehost / Retire / Replace SaaS)
├── FinOps toolchain go-live
├── Team cloud skills training (at least 1 Associate-level certification per person)
└── Key Milestone: First production application running on cloud

Wave 2 (6-12 months): Core System Migration
├── Core business system Replatform (e.g., Oracle → RDS PostgreSQL)
├── Container platform (EKS/AKS) deployment + first batch of containerized applications
├── DR (Disaster Recovery) cross-AZ / cross-Region configuration
├── Full FinOps operations (cost dashboard + monthly review)
└── Key Milestone: 50% of workloads on cloud

Wave 3 (12-24 months): Refactor & Optimize
├── High-value monolith refactored to microservices
├── Data platform migrated to cloud-native Lakehouse
├── AI/ML platform deployment
├── Multi-cloud (if needed) second cloud go-live
└── Key Milestone: 80% of workloads on cloud

Wave 4 (24-36 months): Data Center Shutdown
├── Remaining Retain applications migrated or retired
├── Data center contract expiration migration / decommissioning
├── Full cloud-native operations
└── Key Milestone: Last data center shut down
```

#### 5.2 Per-Wave Checklist

```
Wave [X] Go/No-Go Review Checklist:
□ All applications from the previous wave have been running successfully for 30 days with no major issues
□ Costs are within ±10% of budget
□ Performance is no worse than pre-migration (data-backed)
□ Security / compliance audit passed
□ Team skills are in place (specify who is responsible for what)
□ Rollback plan has been verified
□ Business stakeholders have confirmed the next wave migration window
```

---

### Step 6: Security & Compliance

#### 6.1 Cloud Shared Responsibility Model

```
Responsibility       IaaS    PaaS    SaaS    On-Prem
─────────────────────────────────────────────────────
Physical Security    Cloud   Cloud   Cloud   Customer
Network Security     Shared  Cloud   Cloud   Customer
Host Security        Customer Shared  Cloud   Customer
Application Security Customer Customer Shared  Customer
Data Security        Customer Customer Customer Customer
Identity Security    Customer Customer Customer Customer
```

#### 6.2 Security Red Lines During Migration

- [ ] Production data anonymized before migration → non-production environments
- [ ] Network isolation: Production / non-production networks are not connected
- [ ] Encryption: In transit (TLS 1.2+) + At rest (AES-256)
- [ ] Access Control: Least privilege + temporary credentials (no permanent Access Keys)
- [ ] Audit: All API calls recorded + immutable logs
- [ ] Compliance: Data does not leave the country (if applicable) + Classified Protection assessment

---

## Outputs
1. **Cloud Strategy on a Page**: Goals + Model + Quantified metrics
2. **Application 6R Classification List**: Matrix of all applications × migration strategy
3. **Cloud Platform Assessment & Selection**: Recommended platform + rationale
4. **Landing Zone Design**: Security / Network / Account / Cost foundation
5. **5-Year TCO Comparison**: On-Premises vs. Cloud
6. **FinOps Framework**: Three-phase roadmap + toolchain
7. **Migration Roadmap**: Four-wave migration + milestones + Go/No-Go criteria
8. **Security & Compliance Checklist**

---

## Quality Checklist
- [ ] Every application has a clear 6R classification and rationale
- [ ] Cloud platform selection has a quantified assessment (not "the boss knows the AWS sales rep")
- [ ] TCO model includes migration transition coexistence costs (this is the most commonly overlooked item)
- [ ] Migration Roadmap has clear Go/No-Go criteria (not "just keep pushing forward")
- [ ] Shared responsibility model has been communicated to and understood by the client
- [ ] FinOps framework is designed from Day 1 (not "let's get on the cloud first and figure it out later")
- [ ] Team skills gap has a remediation plan (not "we'll figure it out ourselves after moving to the cloud")
- [ ] Data residency and compliance constraints have been considered (especially for multinational enterprises)

---

## Common Pitfalls

| Pitfall | Why It's Wrong | Correct Approach |
|---------|---------------|------------------|
| "All-in cloud" one-size-fits-all | Not all applications are suitable for cloud; industrial control / compliance-restricted systems may need to stay on-premises | Follow 6R classification; Retain where appropriate |
| No FinOps before cloud migration | The first month's bill will shock the client: "You said cloud saves money, but this is twice as expensive as on-premises!" | Do FinOps from Day 1: mandatory tagging, budget alerts |
| Ignoring network latency | After Lift & Shift, cloud applications accessing on-premises databases see latency jump from 1ms → 20ms | Test network latency in advance; migrate databases and applications together whenever possible |
| Underestimating migration effort | "This system is simple, done in 2 weeks" → Actually takes 2 months (configuration / testing / security / compliance) | Apply 2-3x buffer multiplier per application |
| Ignoring team skills | Adopting Kubernetes but the team only knows how to deploy via FTP | Cloud skills training precedes large-scale migration; cultivate at least 2-3 core personnel |
| Not verifying rollback plan | "It will definitely succeed, no rollback needed" — then production is down for 3 days | Every migration batch must have a verified rollback plan and a rollback decision time window |