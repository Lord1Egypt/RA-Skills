> **Copyright (c) 2026 IDC. All Rights Reserved. Licensed under CC-BY-SA-4.0.** See `IDCcopyright.md` for details.

# COMPASS Dimensions — Detailed Reference

Seven dimensions organized across three constraint layers. Use this reference during Step 4 to validate specific dimensions with user-provided business evidence.

---

## Layer 1: Information Input

### Perception (感知与理解)

**Core question:** Can external inputs be efficiently and accurately converted into system-usable structured data?

**Judgment signals:**
- Heavy manual data entry workload
- Diverse and non-standard information formats
- Low efficiency processing multi-modal inputs (images, voice, documents)

**Typical scenarios:**
- Invoice/receipt recognition and data entry
- Contract information extraction from scanned PDFs
- Multi-channel order aggregation (email attachments, chat files, web portals)
- Voice-to-text intent recognition for customer calls
- Product specification extraction from supplier documents

**Agent capabilities in this dimension:**
- Multi-format document parsing (PDF, images, handwriting, tables)
- Multi-language email and attachment understanding
- Intent classification from unstructured customer communications
- Cross-format data normalization and validation

---

## Layer 2: Information Processing

### Analysis (分析与决策)

**Core question:** Can multi-source data be rapidly aggregated, compared, and synthesized into actionable decision recommendations?

**Judgment signals:**
- Decisions depend on pulling data from multiple systems manually
- Excel-based analysis consumes significant time
- High-frequency decision scenarios where human cognitive bandwidth is the bottleneck

**Typical scenarios:**
- Multi-supplier price comparison and selection
- Customer credit risk assessment
- Dynamic inventory allocation across warehouses
- Marketing attribution and campaign optimization
- Financial statement analysis and anomaly detection
- Procurement spend analysis and vendor evaluation

**Agent capabilities in this dimension:**
- Cross-system data retrieval and synthesis
- Multi-dimensional analysis with weighted scoring
- Scenario simulation and what-if analysis
- Decision recommendation with confidence levels and supporting evidence

### Orchestration (流程编排)

**Core question:** Can tasks automatically connect and dynamically route across multiple systems?

**Judgment signals:**
- Cross-system processes rely on manual triggers
- Process breaks on exceptions requiring human intervention
- API connections are hard-coded, lacking flexibility
- Status updates require manual propagation across systems

**Typical scenarios:**
- End-to-end order processing (order → inventory check → production scheduling → logistics → settlement)
- Procurement coordination (requisition → approval → PO → receiving → payment)
- Contract approval workflow across legal, finance, and business units
- Employee onboarding across HR, IT, and facilities systems
- Claims processing in insurance (intake → validation → assessment → payment)

**Agent capabilities in this dimension:**
- Dynamic workflow routing based on context and business rules
- Exception handling with escalation logic
- Cross-system API orchestration with fallback strategies
- State management across distributed systems

### Monitoring (监控与主动响应)

**Core question:** Can anomalies and deviations be detected promptly and trigger automated responses?

**Judgment signals:**
- Reliance on periodic manual inspections or on-call staff
- Alert rules are simple threshold-based, missing complex patterns
- Long latency from anomaly detection to response
- Reactive rather than proactive incident management

**Typical scenarios:**
- Financial transaction anomaly detection
- Industrial equipment predictive maintenance alerts
- Supply chain disruption early warning
- Regulatory compliance deviation monitoring
- SLA breach detection and escalation

**Agent capabilities in this dimension:**
- Pattern-based anomaly detection beyond simple thresholds
- Proactive alert generation with root cause hypotheses
- Automated first-response actions (isolate, escalate, notify)
- Continuous monitoring with learning from feedback

### Collaboration (协调沟通)

**Core question:** Is cross-department, cross-role information alignment and status synchronization efficient?

**Judgment signals:**
- Significant time spent chasing progress, aligning information, and coordination meetings
- Project delays frequently trace back to information asymmetry
- Status updates require manual broadcasting across stakeholders
- Decision-making stalls waiting for input from multiple parties

**Typical scenarios:**
- Cross-department project coordination (sales ↔ production ↔ logistics)
- Customer communication and after-sales response coordination
- Vendor and supplier relationship management
- Internal approval chain acceleration
- Multi-stakeholder decision alignment

**Agent capabilities in this dimension:**
- Automated status aggregation and broadcast
- Intelligent meeting scheduling and preparation
- Action item tracking and deadline management
- Cross-team context bridging and translation

---

## Layer 3: Information Assetization

### Sedimentation (知识沉淀)

**Core question:** Can individual experience and tacit knowledge be solidified into organizational digital assets?

**Judgment signals:**
- Key personnel departure significantly impacts operations
- New employee onboarding cycles are excessively long
- Best practices are scattered across personal notes and individual experience
- Successful pilot projects cannot be replicated across teams

**Typical scenarios:**
- Expert decision logic capture and codification
- Knowledge base construction from fragmented sources
- Best practice documentation and maintenance
- Training material generation from operational data
- Post-mortem analysis and lesson-learned capture

**Agent capabilities in this dimension:**
- Decision trace logging with rationale capture
- Knowledge graph construction from operational records
- Automated documentation generation
- Experience pattern extraction and recommendation

### Scalability (规模弹性)

**Core question:** Can execution capacity scale beyond the physical limits of headcount?

**Judgment signals:**
- Peak periods heavily depend on overtime and temporary staff
- Linear headcount growth cannot keep pace with business growth
- Adding people does not proportionally increase throughput
- Quality degrades during high-volume periods

**Typical scenarios:**
- E-commerce peak season customer service scaling
- Month-end / quarter-end financial closing
- Regulatory reporting surge periods
- Product launch support scaling
- Batch processing of high-volume repetitive tasks

**Agent capabilities in this dimension:**
- Elastic capacity adjustment without proportional cost increase
- Parallel processing of independent tasks
- Quality-consistent execution at any volume
- Rapid onboarding of new task types through configuration

---

## Quick Reference: Dimension Selection Guide

| If user says... | Primary dimension | Secondary dimension |
|-----------------|-------------------|-------------------|
| "We spend all day entering data from emails and PDFs" | Perception | — |
| "We manually pull data from 5 systems to make decisions" | Analysis | Orchestration |
| "Every time something goes wrong, the whole process stops" | Orchestration | Monitoring |
| "We only find out about problems when customers complain" | Monitoring | Collaboration |
| "Half our time is spent in meetings chasing status" | Collaboration | Orchestration |
| "When our best person leaves, everything falls apart" | Sedimentation | Scalability |
| "We can't handle double the volume without doubling staff" | Scalability | Sedimentation |
| "Orders come from everywhere in every format" | Perception | Orchestration |
| "Sales, production, and logistics are always misaligned" | Collaboration | Monitoring |
