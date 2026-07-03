# AI & Business Transformation Deep Framework

> This document provides deep methodologies needed for AI transformation, referenced by relevant workflows.
> **v1.1.0 New**: McKinsey AI Three Waves, GenAI Gap, AI High Performer Profile, Digital Transformation Three Stages Deepening.

---

## 1. AIM² Maturity Model Detailed Scoring Criteria

### L1: Experimental — Composite Score 1.0-1.9
- **Strategy**: AI is a spontaneous IT department activity, no company-level strategy or budget
- **Organization**: 0-2 people part-time on AI, highly dependent on external vendors
- **Data**: Data silos, manual data preparation, no data governance
- **Technology**: No ML platform, single-machine training, manual deployment
- **Applications**: 1-2 PoC-level projects, no production-grade use cases
- **Value**: ROI unclear, unable to quantify AI input-output

### L2: Departmental — Composite Score 2.0-2.9
- **Strategy**: CIO-driven, departmental budget exists, but not elevated to corporate strategy
- **Organization**: 3-10 person AI team, beginning collaboration with some business units
- **Data**: Partial data centralization, basic BI platform and data warehouse
- **Technology**: Basic ML platform or cloud AI services (GPU/ML PaaS)
- **Applications**: 1-3 production-grade AI use cases, ROI partially quantifiable
- **Value**: Some use cases produce measurable business results

### L3: Enterprise — Composite Score 3.0-3.9
- **Strategy**: CEO/Board explicitly defines AI strategy, enterprise-level AI budget, CDO/CAIO appointed
- **Organization**: AI CoE 30+ people, AI liaisons in each BU, MLOps engineers
- **Data**: Enterprise data platform (Lakehouse), data governance framework, feature engineering platform
- **Technology**: Complete MLOps platform, model factory, AI service catalog
- **Applications**: 10+ production-grade use cases covering multiple business domains, each with clear ROI
- **Value**: AI ROI as percentage of revenue quantifiable, quarterly AI value reports

### L4: AI-Native — Composite Score 4.0-4.9
- **Strategy**: AI drives core business decisions and product innovation, AI capability = core competitiveness
- **Organization**: AI engineers embedded in every product/business team, organization-wide AI literacy assessment
- **Data**: Data Products + Federated Governance, real-time data pipelines, semantic layer
- **Technology**: Agentic AI platform, automated ML/LLMOps, autonomous governance
- **Applications**: AI embedded in >50% of core business processes, Agentic AI enters operational layer
- **Value**: AI revenue share >10% of total revenue (varies by industry)

### L5: AI-Ecosystem — Composite Score 5.0
- **Strategy**: AI capabilities externally exported, building industry/ecosystem platform
- **Organization**: AI-Native hiring standards, AI culture = corporate DNA
- **Data**: Data/AI capabilities as a service (DaaS/AIaaS), data flywheel effect
- **Technology**: Multi-Agent autonomous collaboration network, AI self-optimizing infrastructure
- **Applications**: AI creates new business models / new revenue streams / new product lines
- **Value**: Industry AI standard-setter, AI ecosystem revenue > core business revenue (for some enterprises)

---



---
## 1.5 McKinsey AI Value Creation Three Waves

| Wave | Timeframe | Characteristics | Value |
|------|------|------|------|
| Wave 1: Technology Enablement | 2022-2024 | AI as efficiency tool | Efficiency ↑10-30% |
| Wave 2: Process Reinvention | 2024-2027 | AI redesigns processes | Process efficiency ↑50-200% |
| Wave 3: Business Model Innovation | 2027+ | AI becomes core product | New revenue streams |

### GenAI Implementation Gap
46% of enterprises deploy GenAI at scale → only 9% achieve significant business value. Gap of 37pp.
Three root causes: Data Readiness (62%) > Talent Shortage (55%) > Governance Gap (48%)

### AI High Performer Six Profiles
| Dimension | High Performers | Laggards |
|------|---------|--------|
| Strategy | CEO-level AI agenda | IT department spontaneous activity |
| Investment | AI budget >15% of total IT spend | AI budget <5% |
| Organization | AI embedded in BUs | Isolated lab |
| Data | Data products + real-time pipelines | Data silos |
| Technology | MLOps L3+ | Manual deployment |
| Culture | Fail Fast | Fear of failure / Blind hype chasing |

---
## 1.6 Digital Transformation Three Stages Deepening

| Stage | Characteristics | Typical Work | Key Metrics |
|------|------|---------|---------|
| 1.0 Informatization | Paper→Electronic | ERP/OA/CRM rollout | System coverage >80% |
| 2.0 Digitalization | Data-driven | Data middle platform / AI / Omnichannel | Data-driven decisions >50% |
| 3.0 Intelligentization | AI-native | Agentic AI / Autonomous decision-making | AI contribution to revenue >10% |

Transition Traps: Jumping from 1.0 to 3.0 (skipping data foundation), thinking "buying a system = transformation complete", ignoring organizational culture change


## 2. 5D AI Implementation Framework (Thoughtworks)

Any AI project requires simultaneous effort across five dimensions:

### D1: AI Literacy
- **All Staff**: Understand what AI can/cannot do / how to formulate requirements
- **Managers**: Understand AI investment logic, avoid "AI tourism"
- **Technical Staff**: Continuous learning, avoid being replaced by tools
- ⚠️ Only 20% of developers can consistently and effectively use AI programming tools

### D2: Strong Engineering
- Code quality, testing, architecture discipline must not degrade due to AI
- MLOps/LLMOps maturity is prerequisite for scaling
- Observability / Rollback capability / Auditability

### D3: Internal Champions
- Cultivate cross-level AI advocates
- Bottom-up innovation + Top-down support
- Celebrate small wins, build positive flywheel

### D4: Sound Governance
- Lab → Radar → Structured oversight
- Model risk management (bias / hallucination / safety)
- AI regulation alignment (EU AI Act / China Generative AI Management Measures)

### D5: Focused Experimentation
- Use case-driven (not technology-driven)
- Minimum Viable Model (MVM)
- Each experiment has clear Go/No-Go criteria

---

## 3. Agentic AI Enterprise Implementation Framework

### Three-Tier Architecture (Accenture Hive Model)

```
L3 — Orchestrator Agents
  ├── Cross-department complex decision coordination
  ├── Multi-Agent task orchestration & conflict resolution
  └── Human approval node integration

L2 — Super Agents
  ├── Domain process supervision & goal achievement
  ├── Anomaly detection & human escalation
  └── KPI: Process completion rate / accuracy / human escalation rate

L1 — Utility Agents
  ├── Single clear task automation
  └── KPI: Task completion rate / processing time / error rate
```

### Implementation Roadmap
- **M1-3**: Select 3-5 L1 high-value low-risk scenarios, establish Agent governance framework
- **M4-6**: L1 go-live + iteration, select 1-2 L2 scenario PoCs
- **M7-12**: L2 scaling, Agent operations dashboard
- **M13-18**: Evaluate L3 orchestration layer feasibility

### Agent Governance Core
- **Identity**: Each Agent has unique identity identifier, bound permissions
- **Boundaries**: Explicit rules on "what Agent can do / absolutely cannot do"
- **Audit**: All Agent decisions traceable
- **Metrics**: Decision throughput / decision acceptance rate / human intervention rate / error rate

---

## 4. AI Technology Architecture Decision Tree

```
Requirement: I want to use AI to solve [business problem]
│
├── Is the problem standardized (customer service / translation / code / writing)?
│   └── Use general model API directly (ChatGPT/Claude/Gemini)
│       ├── Need enterprise security? → Enterprise version
│       └── Need to reference internal knowledge? → + RAG
│
├── Does the problem require referencing large amounts of internal enterprise knowledge?
│   └── RAG Architecture (LangChain/LlamaIndex/Dify)
│       ├── Knowledge volume <10K documents → Simple RAG (Embedding + Vector Search)
│       ├── Knowledge volume >10K documents + structured queries → Agentic RAG
│       └── Extremely high accuracy requirements → + Fine-tuning
│
├── Does the problem require learning specific style/domain language?
│   └── Fine-tuning
│       ├── Data <1000 samples → Not recommended (insufficient samples)
│       ├── Data 1000-10K samples → LoRA/QLoRA
│       └── Data >100K samples + proprietary needs → Full Fine-tuning
│
├── Does the problem require multi-step autonomous execution?
│   └── Agent Framework (LangGraph/CrewAI/AutoGen)
│
└── Does the problem involve core IP / absolute privacy?
    └── Proprietary model / Private deployment of open-source model
        ├── Cost-sensitive → Small models (Llama/Mistral/Qwen) + LoRA
        └── Cost-insensitive → Large models + Full Fine-tuning
```

---

## 5. AI Use Case Priority Scoring (RICE+ Extended)

```
Use Case: [Name]

Dimension           Weight   Score(1-10)   Notes
────────────────────────────────────────────
Reach                ×1       [__]         Affected users / transaction volume / revenue share
Impact               ×2       [__]         Impact on revenue / cost / experience / risk
Confidence           ×1.5     [__]         Technically feasible? Data sufficient? Similar cases exist?
Effort (↓ difficulty) ×1      [__]         Person-months + infrastructure cost
Time-to-Value        ×1.5     [__]         Time to first measurable result?
Data Readiness       ×2       [__]         Availability / quality / compliance of required data
Risk Level (↓)       ×1       [__]         Compliance / ethics / model risk / organizational resistance

Weighted Total Score: [___]

>60:  Act Now (Lighthouse Project)
45-60: Next Up (Q2-Q3 Launch)
30-45: Wait (Dependent on other conditions)
<30:  Park
```

---

## 6. AI Implementation Anti-Patterns

| Anti-Pattern | Why It's Wrong | Correct Approach |
|--------|---------|---------|
| "Build AI platform first" | Platform without use cases = mall without customers | First run 1-2 use cases end-to-end, then abstract into platform |
| "Hire 10 data scientists" | Data scientists without data engineers and data = cooks without ingredients | Data Engineer : ML Engineer : Data Scientist = 3:2:1 |
| "Build a ChatGPT enterprise edition" | General AI = ~10% efficiency gain, industry-specific AI = ~100% competitiveness gain | Put 80% effort into scenarios + data + integration |
| "Bigger models are better" | GPT-4 inference cost is 20x GPT-3.5, but many scenarios only need GPT-3.5 | Model routing: simple problems → small models, complex problems → large models |
| Neglecting model monitoring | Model going live = beginning of the story, not the end | Day 1: Data drift / model decay / bias / cost monitoring go live |