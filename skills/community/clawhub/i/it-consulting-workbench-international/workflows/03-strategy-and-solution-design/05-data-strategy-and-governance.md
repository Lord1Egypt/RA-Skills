# Data Strategy & Governance

## Objectives

Position data as a strategic enterprise asset, design a full data lifecycle management system, and develop a roadmap from current data state to a data-driven organization.

---

## Prerequisites
- IT current state diagnostic report already includes data dimension assessment
- Business strategy / IT strategy direction clarified
- Understanding of the client industry's data compliance requirements

## Inputs
- IT current state diagnostic report (data architecture / data quality / data governance current state)
- IT strategy draft
- Industry compliance requirements (e.g., GDPR / Personal Information Protection Law / industry data management regulations)
- Existing data asset inventory (if available)

---

## Operation Steps

### Step 1: Define Core Data Strategy Questions

**Output**: Data Strategy Problem Statement

Answer three fundamental questions:
1. **What is data hindering today?** (e.g., "Financial close takes 7 days because data must be manually reconciled")
2. **What can data drive tomorrow?** (e.g., "If we could see customer behavior in real time, marketing ROI could improve 30%")
3. **If we don't change the current data state, what happens in 3-5 years?** (e.g., "Data silos built by each department; integration costs will be 10x today's cost in 5 years")

**Fill-in Template:**
```
Current Data Pain Points TOP 5:
1. [Pain point] → [Impact: how much money / how many people / how much time]
2. ...
3. ...

Data Strategy Objectives (12-18 months):
- Data Governance: [e.g., Establish enterprise data governance council + data owner system]
- Data Platform: [e.g., Build unified data platform, 100% of core business domain data onboarded]
- Data Applications: [e.g., Go live 3 data-driven business use cases]
- Data Culture: [e.g., 100% of middle management and above complete data literacy training]
```

---

### Step 2: Data Maturity Assessment

#### 2.1 Six-Dimension Data Capability Assessment

| Dimension | L1 (Initial) | L2 (Repeatable) | L3 (Defined) | L4 (Managed) | L5 (Optimized) |
|------|---------|-----------|-----------|-----------|---------|
| **Data Strategy** | No formal strategy | Department-level data strategy | Enterprise data strategy | Data-driven business decisions | Data as product / monetization |
| **Data Governance** | No governance | Partial data standards | Formal governance framework | Automated governance | Ecosystem-level governance |
| **Data Architecture** | File shares / manual | Databases / data warehouse | Data Lake / Warehouse | Lakehouse / Data Mesh | Intelligent data platform |
| **Data Quality** | Don't know if it's good | Reactive fixes | Proactive monitoring | Source prevention | AI-driven automated quality repair |
| **Data Analytics** | Reports (after the fact) | Descriptive analytics | Diagnostic + predictive | Prescriptive + AI | Cognitive (AI autonomous insights) |
| **Data Culture** | Data = IT's problem | Some business units use data | Data literacy training | Data-driven decision-making normalized | Data = corporate culture DNA |

**Current Score Radar Chart**: Mark the current level for each dimension, compare with industry benchmarks.

#### 2.2 Industry Data Maturity Reference

| Industry | Average Maturity | Leading Maturity | Key Gap Dimensions |
|------|----------|----------|------------|
| Financial Services | L3 | L4 | Strong data governance, weak data culture |
| Manufacturing | L2 | L3 | Poor data architecture (OT/IT fragmentation) |
| Retail | L2.5 | L4 | Strong data analytics (marketing), weak data governance |
| Healthcare | L2 | L3 | Good data quality, poor data sharing (privacy) |
| Government | L1.5 | L3 | Poor data architecture, low willingness to share |

---

### Step 3: Data Governance Framework Design

#### 3.1 Data Governance Organizational Structure

```
Board / CEO
    │
    ├── Data Governance Council
    │    Members: CDO (Chair) + Business Line VPs + CIO + Legal + Compliance
    │    Frequency: Monthly
    │    Responsibilities: Strategic direction, policy approval, major data issue arbitration
    │
    ├── CDO / Chief Data Officer
    │    Responsibilities: Data strategy execution, data asset management, data value realization
    │
    ├── Data Owners (one per subject domain, held by Business VPs)
    │    Data Subject Domains: Customer / Product / Supplier / Finance / Employee / ...
    │    Responsibilities: "Who can view / what counts as good data / conflict arbitration" for this domain
    │
    ├── Data Stewards (can be part-time)
    │    1-3 people under each Data Owner
    │    Responsibilities: Day-to-day data quality, metadata maintenance, first-line data issue handling
    │
    └── Data Architecture / Data Engineering Team
         Responsibilities: Data platform construction & operations, technical implementation of data standards
```

#### 3.2 Core Data Governance Processes

**Process 1: Data Standard Development**
```
Business proposes → Data Steward drafts → Data Owner reviews → Data Governance Council approves → Release → Platform implementation
```

**Process 2: Data Quality Incident Handling**
```
Issue discovered → Data Steward confirms → Severity classification (L1/L2/L3) →
L1: Fix within 24 hours, Data Steward handles
L2: Fix within 72 hours, Data Owner + IT collaboration
L3: Within one week, escalate to Data Governance Council, root cause analysis + preventive measures
```

**Process 3: Data Access Approval**
```
Request → Data Owner approval → Least privilege authorization → Periodic audit → Auto-revoke upon expiry
```

#### 3.3 Data Standard Definitions

| Standard Category | Example |
|---------|------|
| Naming Conventions | Table names: `[domain]_[entity]_[type]`, e.g., `cust_profile_t` |
| Coding Rules | Customer ID: `CUST-{region}-{8-digit sequence}` |
| Data Dictionary | Each field: business meaning + data type + value range + source system |
| Reference Data | Country codes / currencies / industry classifications / ... unified values |
| Quality Rules | Required / uniqueness / value range / format / cross-reference validation |

---

### Step 4: Data Architecture Design

#### 4.1 Data Platform Selection Decision

```
Is real-time data needed?
  ├── Yes (latency <1 min) → Event-driven architecture (Kafka + Flink + real-time warehouse)
  │   └── Selection: Streaming + Lakehouse (e.g., Databricks / ClickHouse)
  │
  └── No (batch processing acceptable) → Data Warehouse / Data Lake
      ├── Data volume <10TB + simple BI → Data Warehouse (Snowflake / Redshift)
      ├── Data volume >10TB + multi-source heterogeneous → Data Lakehouse (Databricks / Iceberg)
      └── Multiple BUs with independent data teams → Data Mesh (federated governance + data products)
```

#### 4.2 Data Platform Technology Stack Reference

```
Data Ingestion Layer:
├── Batch: Airbyte / Fivetran / DataX
├── Real-time Streaming: Kafka + Flink / Spark Streaming
└── CDC (Incremental): Debezium / DMS

Data Storage Layer:
├── Data Lake: S3/OSS + Iceberg/Hudi
├── Data Warehouse: Snowflake / Databricks / Doris
├── Feature Store: Feast / Tecton
└── Graph Database: Neo4j / JanusGraph

Data Processing Layer:
├── ETL/ELT: dbt + Airflow / Dagster
├── Data Quality: Great Expectations / Deequ
└── Data Lineage: DataHub / Marquez / OpenLineage

Data Serving Layer:
├── BI: Tableau / Power BI / Metabase
├── Self-service Analytics: Superset / NetEase YouShu
├── Data API: GraphQL + REST
└── Semantic Layer: Cube / Looker
```

#### 4.3 Three Paradigms of Data Architecture Evolution

| Paradigm | Applicable Conditions | Advantages | Disadvantages |
|------|---------|------|------|
| **Centralized DW/Lake** | Small-medium scale, low BU autonomy needs | Good governance, high consistency | Becomes bottleneck, hard to scale |
| **Data Lakehouse** | Large-medium scale, multi-source heterogeneous data | Flexible + governance balanced | Complex tech stack |
| **Data Mesh** | Large scale, multiple BUs with independent data teams | Good scalability, BU autonomy | High governance cost, risk of duplication |

**Recommended Evolution Path (for most enterprises):**
```
Centralized DW → Lakehouse → Conditionally evolve to Data Mesh (not mandatory to reach Mesh)
```

---

### Step 5: Data Quality & Master Data Management

#### 5.1 Data Quality Measurement

4 Core Quality Dimensions (Precision Version):

| Dimension | Definition | Measurement Formula | Target |
|------|------|---------|------|
| Completeness | No missing required fields | Complete records / Total records | >99% |
| Accuracy | Data reflects the real world | Accurate records / Sample size | >99.5% |
| Consistency | Same data consistent across systems | Consistent records / Records that should have same value | >98% |
| Timeliness | Data available when needed | Records arriving within specified time / Total records | >99% (real-time >99.9%) |

#### 5.2 Master Data Management (MDM) Implementation Strategy

**MDM Four-Mode Selection:**

| Mode | Description | Applicable Scenario |
|------|------|---------|
| **Registry** | Stores only links, not actual data | Need to quickly identify "who is who", don't change source systems |
| **Coexistence** | MDM Hub stores partial attributes, source systems retain full data | Gradual transition approach |
| **Transactional** | MDM Hub = single source of truth, all systems read/write to Hub | Many source systems, poor data quality, determined to govern |
| **Consolidated** | Aggregate from source systems into a golden record for querying | Reporting/analytics scenarios, no need to write back to source systems |

**Implementation Steps:**
1. Select 1-2 most painful master data domains (prefer customer/product first)
2. Define the master data model for that domain (which attributes, source of truth, who has authority)
3. Perform one full matching + deduplication + merge
4. Establish ongoing deduplication and merge rules
5. Release to consuming systems (via API or ETL)

---

### Step 6: Data Roadmap

```
Phase 1: Foundation (0-6 months)
├── Establish Data Governance Council + appoint first batch of Data Owners
├── Select 2 data domains (e.g., Customer + Product), define data standards
├── Data platform foundation setup (Lakehouse)
├── First data quality dashboard Go live (monitor 1-2 core systems)
└── Milestone: First data domain data standards released, first use case data onboarding complete

Phase 2: Scale (6-12 months)
├── Expand to full business domain data standards
├── Master Data Management (MDM) Go live (first domain)
├── Data Catalog Go live: all core datasets discoverable
├── Self-service BI platform + data literacy training (100+ people)
└── Milestone: MDM first domain Go live, 100% of data assets discoverable

Phase 3: Innovate (12-24 months)
├── Real-time data pipelines (core scenarios)
├── Data as a Product concept introduced
├── AI/ML platform deeply integrated with data platform
├── Data value dashboard (quantify data's contribution to business)
└── Milestone: Data-driven revenue share quantifiable
```

---

## Outputs
1. **Data Strategy One-Pager**: Pain points + objectives + 12-month roadmap
2. **Data Maturity Assessment**: Radar chart + industry comparison
3. **Data Governance Framework**: Organizational structure + core processes + standards
4. **Data Architecture Design**: Platform selection + tech stack + evolution path
5. **Data Quality Measurement Framework**: Key metrics + monitoring approach
6. **Master Data Management Strategy**: Domain selection + mode selection + implementation steps
7. **Data Roadmap**: Three phases + milestones

---

## Quality Check
- [ ] Data governance organization is not "hollow": each Data Owner has a specific name and responsibilities
- [ ] Data standards are not "a dictionary as thick as an encyclopedia that no one reads": start from 2-3 most painful data elements
- [ ] Platform selection has clear rationale, compared against alternatives
- [ ] Data quality targets have baselines and target values (not "improve data quality")
- [ ] Industry compliance requirements considered
- [ ] Roadmap Phase 1 has Quick Wins (data strategy's biggest taboo: "build the platform first and wait 3 years")

---

## Common Pitfalls

| Pitfall | Why It's Wrong | Correct Approach |
|------|---------|---------|
| "Build the big data platform first" | Built platform with no data onboarded = luxury mall with no stores | Use-case driven: each phase's data onboarding anchored to a specific business use case |
| Data governance = IT's job | Data Owners should come from business; IT is technical support | From day one, have business VPs serve as Data Owners, accountable for "their data" |
| Pursuing perfect data quality | "Data must be 100% accurate before we dare use it" → never goes live | Different scenarios, different quality requirements: AI recommendations can tolerate noise, financial reports zero tolerance |
| Data standards become a dictionary | Hundreds of pages of PDF, written but no one reads | Embed data standards into the data platform (automated validation, can't write without passing) |
| Ignoring data culture | Technology built but no one uses it; business continues with Excel | Data literacy training + Treat data as product (data products have SLA/docs/support) |