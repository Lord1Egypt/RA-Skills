# AI-* Family — Subject-Matter Glossary

**Version:** 1.0.0
**Created:** 2026-06-11
**Updated:** 2026-06-11
**Purpose:** Single-source definition of every subject-matter concept used across the AI-* family packages. Helps new users, contributors, and AI agents understand the domain language without guessing.

---

## How to Use This Glossary

- Terms are grouped by **domain** (the package that primarily introduces them)
- Many terms are used across multiple packages — they're listed where they originate
- Terms marked with `→` reference another glossary entry
- Keep this file updated when new concepts are introduced in any package

---

## A. Project Management & Initiation (AI-PILC)

| Term | Definition |
|------|-----------|
| **Project Initiation Package (PIP)** | The complete governance foundation for a project — all initiation artifacts assembled and approved, ready for execution handoff. AI-PILC's final output that feeds the Project layer (→AI-POLC → AI-UXD → AI-ADLC). |
| **Project Charter** | Formal document that authorizes a project's existence. Defines authority, objectives, boundaries, high-level scope, success criteria, and governance mandate. The formal "go" decision. |
| **Business Case** | Investment justification document containing: problem statement, proposed solution, options analysis, benefits (tangible + intangible), cost estimate, →ROI analysis, timeline, risk summary, and recommendation. |
| **Feasibility Assessment** | Evaluation of project viability across four dimensions: Technical (can we build it?), Operational (can we run it?), Financial (can we afford it?), Schedule (can we deliver on time?). Each dimension is scored and weighted into an overall feasibility rating. |
| **Stakeholder Register** | Catalog of all project stakeholders with classification (→Power/Interest Matrix), engagement strategy, communication preferences, and influence assessment. |
| **RACI Matrix** | Governance tool assigning exactly one of four roles to each person per deliverable/activity: **R**esponsible (does the work), **A**ccountable (owns the outcome), **C**onsulted (provides input), **I**nformed (kept aware). |
| **Risk Register** | Structured catalog of identified risks. Each entry includes: description, probability (1-5), impact (1-5), risk score (P×I), mitigation strategy, contingency plan, owner, and status. |
| **MoSCoW Prioritization** | Requirements classification framework: **M**ust have (non-negotiable), **S**hould have (important but not critical), **C**ould have (desirable if resources allow), **W**on't have (explicitly deferred). |
| **Scope Statement** | Formal definition of project boundaries: in-scope / out-of-scope table, deliverable list, →WBS summary, acceptance criteria, assumptions, constraints, and scope change control process. |
| **Work Breakdown Structure (WBS)** | Hierarchical decomposition of total project scope into manageable work packages. Deliverable-oriented (not activity-oriented). Typically 2-3 levels deep depending on →Adaptive Depth. |
| **Resource Plan** | Team composition, skill requirements, capacity allocation, budget breakdown (CAPEX/OPEX), timeline mapping, and procurement needs. |
| **Requirement Intake Form** | Structured template capturing: requestor details, business need, functional requirements, non-functional requirements, constraints, assumptions, dependencies, priority, and stakeholders. |
| **Stage Gate** | Mandatory approval checkpoint between workflow stages. User must explicitly approve before proceeding. Non-negotiable in all AI-* packages — the workflow never auto-progresses. |
| **Phase Gate (initiation lifecycle — AI-PILC)** | Higher-level milestone boundary between major workflow phases (e.g., Inception → Assessment → Justification → Authorization → Planning → Mobilization). Scoped to the project-initiation lifecycle. Distinct from →Phase Gates (PG-*) in the build lifecycle. |
| **ROM (Rough Order of Magnitude)** | Early-stage cost estimate with accepted variance of -25% to +75%. Produced during Business Case when detailed costing is premature. |
| **ROI (Return on Investment)** | Financial metric: (Net Benefits / Total Investment) × 100%. Used alongside →NPV and →Payback Period in business case analysis. |
| **NPV (Net Present Value)** | Present value of future cash flows minus initial investment, accounting for time value of money. Positive NPV = financially justified. |
| **Payback Period** | Time required to recover the initial investment. Shorter = lower risk. Used alongside →ROI and →NPV. |
| **Power/Interest Matrix** | Stakeholder classification grid: high-power/high-interest (manage closely), high-power/low-interest (keep satisfied), low-power/high-interest (keep informed), low-power/low-interest (monitor). |
| **Kickoff Agenda** | Structured meeting plan for formal project start: introductions, project overview, governance structure, communication plan, immediate next steps, Q&A. |
| **Decision Log** | Register tracking significant decisions with: date, context, options considered, decision made, rationale, decision-maker, and impact. |
| **Change Log** | Register of approved scope, approach, or timeline changes: date, change description, reason, impact assessment, approver. |
| **Issue Log** | Register of blockers and problems: date, description, severity (H/M/L), area affected, status (Open/Closed), resolution, resolved date. |
| **Action Items** | Tracked follow-up tasks: description, owner, due date, status (Open/Done), source (which meeting/stage generated it). |
| **Assumptions & Dependencies** | Register of project assumptions (things believed true but not proven) and dependencies (things needed from external parties): type (A/D), impact if invalid, validation status. |
| **Lessons Learned** | Insights captured during project execution about what worked, what didn't, and what to do differently. Shared across phases for continuous improvement. |
| **PMBOK (Project Management Body of Knowledge)** | PMI's standard methodology framework. AI-PILC aligns terminology and process structure with PMBOK 7th Edition principles. |
| **PRINCE2 (Projects IN Controlled Environments)** | Process-based project management methodology emphasizing business justification, defined organization, staged delivery, and management by exception. |
| **ITIL (IT Infrastructure Library)** | Framework of best practices for IT service management — referenced for service-oriented project governance. |
| **Steering Committee** | Executive governance body that reviews progress, resolves escalations, and provides formal sign-off at →Phase Gates. |
| **Adaptive Depth** | Three-tier workflow calibration applied across all AI-* packages: **Minimal** (clear/small scope), **Standard** (normal complexity), **Comprehensive** (high complexity, many unknowns). Each stage behaves differently per level. |
| **Project ID** | Immutable family-wide correlation key (format: `PRJ-{ABBREV}-{YYYY}-{NNN}`). Minted at AI-PILC Stage 1, carried through every downstream package for traceability and portfolio roll-up. |

---

## B. Architecture Design (AI-ADLC)

| Term | Definition |
|------|-----------|
| **Architecture Package (AP)** | Complete technical design foundation for a project — all architecture artifacts assembled, validated, and ready for AI-DWG to transform into a development workspace. AI-ADLC's final output. |
| **C4 Model** | Architecture visualization framework (Simon Brown) with 4 levels of progressive decomposition: Context (L1), Container (L2), Component (L3), Code (L4). AI-ADLC uses L1-L3. |
| **System Context (C4 Level 1)** | Highest abstraction. Shows: the system as a single box, external actors (people/roles who use it), external systems (integrations). Defines the trust boundary — what's "inside" vs. "outside." |
| **Container Diagram (C4 Level 2)** | Decomposes the system into deployable units: applications, databases, message brokers, file stores, CDNs. Each container has a technology assignment and defined communication with others. |
| **Component Design (C4 Level 3)** | Internal structure within each container: modules, bounded contexts, services, interfaces, and dependency rules. This level drives folder structure and module boundaries. |
| **ADR (Architecture Decision Record)** | Formal record of a significant design choice. Structure: Title, Status, Context, Decision Drivers, Considered Options, Decision, Rationale, Consequences. Produced when 2+ viable options exist and the choice has lasting impact. |
| **Architecture Vision** | Opening statement defining what the architecture optimizes for (e.g., "scalability over cost efficiency") plus guiding principles that constrain all subsequent decisions. |
| **Quality Attributes** | Non-functional characteristics the system must exhibit: performance, security, scalability, availability, reliability, maintainability, accessibility. Prioritized as Critical / High / Medium / Low. |
| **Technology Stack** | Complete inventory of technology choices per container: language, framework, database engine, caching layer, search engine, messaging system, deployment platform, monitoring tools, UI framework. |
| **Multi-Tenancy** | Architecture for serving multiple customers (tenants) from shared infrastructure with data isolation. Models: database-per-tenant, schema-per-tenant, row-level isolation. Includes tenant context propagation and cross-tenant security. |
| **Security & Identity Architecture** | Authentication methods (OAuth2, OIDC, SAML), authorization model (→RBAC, ABAC), token strategy (JWT, opaque), encryption (at rest, in transit), secrets management, audit logging, OWASP Top 10 mitigations. |
| **RBAC (Role-Based Access Control)** | Authorization model where permissions are assigned to roles, and users are assigned to roles. Simpler than ABAC but less granular. |
| **Data Architecture** | Entity-relationship design, schema management (migrations), storage patterns (structured/unstructured/cached/indexed), data lifecycle (retention, archival, backup), and consistency model. |
| **API Architecture** | API style and standards: REST conventions, pagination strategy, filtering/sorting, error response format, versioning strategy, authentication mechanism, rate limiting, documentation approach (OpenAPI/Swagger). |
| **Integration Architecture** | Patterns for connecting to external systems: synchronous (REST/gRPC), asynchronous (events/queues), file transfer, polling. Adapter/connector design, failure handling, →Dead Letter Queue. |
| **Infrastructure & Deployment** | Deployment topology (containers, orchestration, networking), high availability design, scaling approach (horizontal/vertical/auto), observability (metrics, logging, tracing, alerting), backup/DR strategy. |
| **Architecture Workbook** | Living document tracking the thinking process throughout design: decision backlog, open questions, discussion notes, resolved items, option analyses. Maintained across all stages. |
| **Bounded Context** | →DDD concept: explicit boundary around a domain model where terms and rules are internally consistent. Each bounded context has its own →Ubiquitous Language and can be implemented independently. |
| **DDD (Domain-Driven Design)** | Software design approach centering the domain model as the primary driver of architecture. AI-ADLC's DDD Tactical extension adds →Aggregates, →Domain Events, →Anti-Corruption Layers, →Value Objects. |
| **Aggregate** | DDD tactical pattern: cluster of domain objects (entities + value objects) treated as a single unit for data changes. Has a root entity and a defined consistency boundary. Changes within one aggregate are transactional. |
| **Domain Event** | DDD concept: notification that something significant happened in the domain. Used for decoupled communication between →Bounded Contexts (e.g., "OrderPlaced", "PaymentReceived"). |
| **Value Object** | DDD concept: immutable object defined by its attributes rather than identity. Two value objects with the same attributes are equal (e.g., Money(100, "USD"), Address, DateRange). |
| **Anti-Corruption Layer (ACL)** | DDD pattern: translation boundary that prevents one system's model from polluting another. Adapts, translates, and shields — particularly important between legacy and new systems. |
| **Ubiquitous Language** | DDD concept: shared vocabulary between developers and domain experts, used consistently in code, documentation, and conversation within a →Bounded Context. |
| **CQRS (Command Query Responsibility Segregation)** | Architecture pattern separating the write model (commands that change state) from the read model (queries that return data). Each side can be optimized independently. Often combined with →Event Sourcing. |
| **Event Sourcing** | Data pattern: instead of storing current state, store the complete sequence of state-changing events. Current state is reconstructed by replaying events. Includes projections, read models, and snapshots for performance. |
| **BFF Pattern (Backend for Frontend)** | Architecture pattern where each frontend channel (web, mobile, TV, etc.) has its own dedicated backend API layer that aggregates and shapes data specifically for that client's needs. |
| **Circuit Breaker** | Resilience pattern: monitors calls to a service. After N consecutive failures, "opens" the circuit — immediately returning errors without attempting the call. After a timeout, allows a test call through. Prevents →Cascading Failure. |
| **Bulkhead** | Resilience pattern: isolates components into pools so that failure in one pool doesn't exhaust resources shared with others. Named after ship compartments that prevent total flooding. |
| **Retry with Backoff** | Resilience pattern: automatically retries failed operations with increasing delay between attempts (exponential backoff + jitter). Prevents thundering herd on recovery. |
| **Graceful Degradation** | Resilience principle: system continues operating with reduced functionality when components fail, rather than failing entirely. Example: show cached data when database is slow. |
| **Cascading Failure** | Failure mode where one component's failure causes dependent components to fail, which causes their dependents to fail, spreading through the system. →Circuit Breaker prevents this. |
| **Dead Letter Queue (DLQ)** | Message queue where failed/unprocessable messages are sent after exhausting retry attempts. Enables manual inspection and replay without blocking the main processing flow. |
| **Feature Flags** | Progressive delivery mechanism: runtime switches controlling feature visibility without code deployment. Lifecycle: create → percentage rollout → full rollout → permanent → flag removal. |
| **Strangler Fig Pattern** | Legacy migration strategy: incrementally replace functionality by routing requests to a new system piece by piece, while the old system handles everything not yet migrated. |
| **Microservices** | Architecture style: system decomposed into independently deployable services, each owning one business capability, with its own data store. Communicates via APIs or events. |
| **Service Mesh** | Infrastructure layer handling service-to-service communication: routing, load balancing, observability, mutual TLS, retries, circuit breaking — without application code changes. |
| **Saga Pattern** | Distributed transaction pattern: coordinates multi-service operations through a sequence of local transactions. If one fails, compensating transactions undo previous steps. Choreography (event-driven) or Orchestration (coordinator). |
| **Shared Kernel** | DDD integration pattern: explicitly shared code or model between two →Bounded Contexts, maintained jointly by both teams. Minimized to reduce coupling. |
| **Mermaid** | Text-based diagramming syntax used for architecture diagrams in AI-ADLC. Renders to visual diagrams in Markdown viewers. Standard styling conventions in `diagram-standards.md`. |
| **Extension (AI-ADLC)** | Optional advanced architecture pattern that adds mandatory rules when activated. Opt-in only. Once active, its rules become blocking constraints. Six extensions: DDD, Microservices, BFF, Event Sourcing, Resilience, Feature Flags. |

---

## C. Workspace Generation & DevOps (AI-DWG)

| Term | Definition |
|------|-----------|
| **Development Workspace (DW)** | Ready-to-code project environment: →Steering Files, folder structure, configuration files, operational documents, planning templates. AI-DWG's output — what AI-DLC v1 builds within. |
| **Steering File** | Prescriptive rule file in `.kiro/steering/` that governs AI assistant and developer behavior. Uses MUST/MUST NOT/NEVER language (binary compliance). Each traces back to a specific →AP artifact. |
| **Provenance Tracking** | Mechanism marking every generated file with its architecture source via metadata comment: `<!-- Generated by AI-DWG | Source: {doc} → "{section}" -->`. Enables traceability audits and targeted →Reconciliation. |
| **Provenance Front-Matter** | YAML metadata block on generated `.md` files: `generatedBy`, `generatedVersion`, `source`, `generatedOn`, `ownership`. Standard across all AI-* packages per `NAMING_AND_OWNERSHIP.md`. |
| **Delta Reconciliation** | AI-DWG Mode 2: detect what changed in the →AP since last generation, update only affected workspace files, preserve team customizations marked with →Custom Markers. |
| **Greenfield** | New project starting from scratch — no existing codebase. AI-DWG applies Mode 1 (full generation) to produce the complete workspace. |
| **Brownfield** | Existing project with existing code that needs governance overlay. AI-DWG applies Mode 3: adds steering files non-destructively, acknowledges existing structure, baselines current state. |
| **Conditional Generation** | Principle: files are generated ONLY when the →AP justifies them. No multi-tenancy in AP = no tenancy steering file. Prevents bloat. |
| **Mapping File** | Transformation contract in AI-DWG defining the explicit rule: "given this AP input section → produce this workspace output file." The mapping IS the API. 23 mappings total. |
| **Downstream Signaling** | Notification from AI-DWG to →AI-GCE indicating workspace files were generated or updated, triggering compliance re-derivation. Implemented via marker file presence/timestamps. |
| **Marker File** | Detection anchor whose presence signals a package's output exists (e.g., `pilc-state.md`, `adlc-state.md`, `workspace-rules.md`). File names are non-negotiable — renaming breaks detection. |
| **Custom Markers (`<!-- custom -->`)** | HTML comments protecting team-added content from being overwritten during →Delta Reconciliation. Content between markers survives re-generation. |
| **Technology-Adaptive Output** | Generated files vary based on detected tech stack. Node.js gets `package.json` + ESLint; Python gets `pyproject.toml` + Ruff; .NET gets `.csproj` + Roslyn analyzers. |
| **CODEOWNERS** | Git platform file mapping code paths to responsible teams/individuals. Generated from →C4 Level 3 component ownership. Enforced on pull requests. |
| **Definition of Done (DoD)** | Quality criteria document defining when a work item is "done" (code, tests, docs, review, deployment). Generated from →AP quality attributes. Enforced by →AI-GCE as a gate. |
| **Day-1 Productivity** | Design principle: a developer joining after workspace generation needs ZERO additional setup guidance beyond what's in the generated files. Everything needed is present. |
| **EditorConfig** | Cross-editor configuration file (`.editorconfig`) standardizing indent style, line endings, trailing whitespace rules. Tech-stack-appropriate defaults generated by AI-DWG. |
| **Docker Compose** | Container orchestration configuration for local development. Generated based on tech stack and infrastructure requirements from the →AP. |

---

## D. Governance & Compliance (AI-GCE)

| Term | Definition |
|------|-----------|
| **Compliance Enforcement Layer** | Complete governance infrastructure produced by AI-GCE: →Compliance Hooks, →Compliance Rules, →Governance Agents, and →Compliance Log. Tailored to the specific project's architecture and methodology. |
| **Compliance Hook** | Automated check triggered by IDE events (file edit, agent stop, prompt submit, tool use) that enforces a governance rule in real-time. Produces zero output when rules pass (→Silent When Compliant). |
| **Hook Debounce** | Classification of WHEN hooks fire: **Tier A** = immediate on `fileEdited` (security-critical — secrets, data leakage, destructive ops); **Tier B** = batch on `agentStop` (advisory — naming, boundaries, coverage). |
| **Three-Tier Progressive Compliance** | Enforcement adoption model: **Tier 1** (Day 0, essential rules, 60-70% coverage) → **Tier 2** (Sprint 2+, expanded enforcement, 80-90%) → **Tier 3** (Pre-Release, full compliance, 92%+). Never big-bang. |
| **Two-Source Derivation** | AI-GCE generates rules from two combined sources: (1) →Steering Files (project-specific, from workspace) + (2) →Built-In Baseline (universal methodology minimums). Steering wins on conflict. |
| **Built-In Baseline** | Universal governance rules that apply to ANY project regardless of steering file content. Examples: "spec before code", "author ≠ approver", "no direct push to main", "session discipline." |
| **Brownfield Baseline** | Document acknowledging existing violations as technical debt with remediation SLAs. Enforcement applies ONLY to new/changed code from Day 1. Existing violations get a timeline. |
| **Compliance Score** | Percentage metric: (passing rules / total applicable rules) × 100%. Target varies by →Tier. Tracked over time in `.compliance-state.json`. |
| **Re-Derivation** | AI-GCE Mode 2: selectively re-generating only the rules/hooks affected by upstream steering file changes. Preserves →Custom Markers and team additions. |
| **Phase-Aware Enforcement** | Rules only fire when applicable to the current project phase. Sprint governance doesn't fire during initial setup. Phase tracked in `.compliance-state.json`. |
| **Compliance Log (JSONL)** | Append-only audit trail. Every hook execution writes: `{timestamp, rule_id, result (pass/fail/skip), evidence, file, agent}`. Non-negotiable audit requirement. |
| **Exception Workflow** | Process for legitimately bypassing a compliance rule: justification required, different-person approval for Critical severity, expiration date mandatory, logged in compliance log. |
| **Remediation Workflow** | Process for fixing violations: Detection → Assignment → Fix → Verification → Closure. Tracked until resolved. |
| **Silent When Compliant** | Design principle: hooks produce ZERO output when all rules pass. Only surface violations. Noise kills adoption. |
| **Role Isolation / Separation of Duties** | Governance principle: author ≠ approver, no self-merge, each module has exactly one owning team. Prevents conflicts of interest. See →`WHY_SEPARATION_OF_DUTIES_MATTERS.md`. |
| **Team Topology** | Organizational structure mapped to code ownership: one →Bounded Context per team, cognitive load limits, independent deployability. Governance enforces the declared boundaries. |
| **Session Governance** | AI-DLC v1 methodology rules: spec-before-code, never →Vibe Code, one task at a time, correction escalation protocol. Enforced on every prompt submission. |
| **Vibe Coding** | Anti-pattern: AI writing code without following specifications, steering rules, or structured methodology. Session governance exists specifically to prevent this. |
| **Correction Escalation Protocol** | 4-level response to AI mistakes: (1) Point correction → (2) Pattern correction → (3) Design correction → (4) Session restart. Severity increases if corrections don't stick. |
| **Sprint Governance** | Rules for sprint health: sprint plan must exist, sprint goal defined, retrospective actions tracked, velocity measured. |
| **Phase Gates (PG-*) — build lifecycle (AI-GCE/AI-DLC v1)** | Milestone gates with specific pass criteria: Setup→Foundation, Foundation→Construction, Construction→Integration, Integration→Go-Live. Distinct from →Phase Gate (initiation lifecycle — AI-PILC). |
| **CI/CD Gates** | Pipeline quality thresholds that must pass before merge/deploy: tests green, security scan clear, coverage targets met, architecture violations = 0. |
| **PR Governance** | Pull request process rules: conventional commit messages, maximum PR size, required approvals count, reviewer diversity, no self-approval. |
| **Change Management** | Release governance: sign-off requirements, rollback criteria, deployment windows, impact assessment, communication plan. |
| **Compliance Dashboard** | Visual summary: tier progress, overall score, rules/hooks inventory, active exceptions, top recurring violations, trend over time. |
| **Governance Agent** | AI-triggered governance checkpoint invoked at process milestones via shortcut command (e.g., `SDC__`, `SGV__`). Three types: Infrastructure, Process, Audit. |
| **Agent Registry** | Single-source lookup file (`.governance/AGENT_REGISTRY.md`) for all active agents in a workspace: ID, name, type, trigger, tier, producer, status. |
| **Context Budget** | Maximum allowed size for always-included steering files (≤300 lines). Prevents context window overflow for AI assistants. Enforced by steering governance. |
| **Five Qualities Test** | Steering file meta-governance criteria: (1) Prescriptive language, (2) Enforceable (binary pass/fail), (3) Specific (not vague), (4) Non-contradictory, (5) Fresh (up-to-date). |
| **Tier Activation** | AI-GCE Mode 4: upgrading compliance tier when readiness criteria are met (minimum score threshold + all prerequisites satisfied). |

---

## E. Test Governance (AI-TGE)

| Term | Definition |
|------|-----------|
| **Test Register** | Master list mapping every →Architecture Commitment to required tests. Columns: ID, commitment source, test level, test type, technique, description, status (Required/Exists/Missing/Deprecated/Overridden). |
| **Test Strategy** | Document defining: test pyramid ratios, test types needed per architecture layer, tools/frameworks, coverage goals, test data strategy, automation approach, entry/exit criteria per environment. |
| **Debt Scorecard** | Prioritized list of missing tests ranked by composite risk score. Presented as top-N actionable items with specific instructions on what to test and why. |
| **Architecture Commitment** | A testable promise the architecture makes. Examples: "API validates input per schema", "tenant data is isolated", "circuit breaker opens after 5 failures." The unit of test coverage tracking. |
| **Test Pyramid** | Recommended distribution of test investment: many fast unit tests (base), fewer integration tests (middle), fewest slow system/acceptance tests (top). Ratios vary by architecture. |
| **ISTQB Classification** | Standard taxonomy for test requirements. Three dimensions: **Level** (Unit/Integration/System/Acceptance) × **Type** (Functional/Non-Functional/Structural) × **Technique** (Architecture-Derived/Baseline/Story-Derived/Manual). |
| **Risk-Based Test Prioritization** | Scoring missing tests on 4 factors (1-5 each): Architectural Risk (how critical is this component?), Blast Radius (what fails if it fails?), Logic Complexity (how tricky is the implementation?), Change Frequency (how often is it modified?). Composite range: 1-625. |
| **Characterization Test** | Test documenting EXISTING behavior of legacy code BEFORE modification. Mandatory in →Brownfield scenarios. Captures current behavior as baseline regardless of whether it's "correct." |
| **Coverage Report** | Multi-view analysis: by commitment, by component, by test type, by risk level. Answers "did we test what we designed?" — not just lines-of-code coverage. |
| **Architecture Reconciliation (Test)** | Detecting →AP changes since last strategy run and updating the test register: new commitments → new Required entries, removed → Deprecated, changed → flagged for review. |
| **Defect Log** | Structured defect tracking: ID, severity (Critical/High/Medium/Low), category, description, linked test/component/story, root cause, status lifecycle (Open→Assigned→Fixed→Verified→Closed). |
| **Observation Phase** | AI-TGE's continuous mode: watching AI-DLC v1 build execution, tracking what gets tested, updating register status and coverage reports. Non-blocking — informs, doesn't gate. |
| **Strategy Phase** | AI-TGE's derivation mode with gates: determining WHAT must be tested and WHY. Stages: workspace detection, architecture reading, requirement derivation, brownfield assessment, strategy generation, risk scoring. |
| **Orphaned Test** | A test that exists in the codebase but has no matching →Architecture Commitment in the test register. May indicate obsolete or undocumented behavior. |
| **Test Debt** | Gap between what should be tested (per register) and what actually is tested. Scored and prioritized by →Risk-Based Test Prioritization. |
| **Two-Source Coverage** | AI-TGE derives test requirements from TWO sources: (1) Architecture-derived (from →AP commitments) + (2) Built-in baseline (universal minimums like "auth endpoints must have security tests"). Even thin APs get minimum governance. |

---

## F. Cross-Package & Chain Concepts

| Term | Definition |
|------|-----------|
| **AI-* Family** | The complete suite of injectable workflow packages: AI-ILC, AI-PILC, AI-PPM (Portfolio layer) + AI-ADLC, AI-UXD, AI-POLC, AI-DWG, AI-GCE, AI-TGE (Project layer) + AI-FLO (Edge router). |
| **Portfolio Layer** | AI-* Family scope covering MANY projects simultaneously: AI-ILC (idea filtering), AI-PILC (project initiation), AI-PPM (portfolio governance and prioritization). |
| **Project Layer** | AI-* Family scope covering ONE project end-to-end: AI-POLC (product ownership), AI-UXD (UX), AI-ADLC (design), AI-DWG (workspace), AI-GCE (compliance), AI-TGE (test governance), AI-DLC v1 (build). Runs sequentially: POLC→UXD→ADLC→DWG. |
| **Edge Layer / AI-FLO** | Router/orchestration engine between Portfolio and Project layers. Carries handoff decisions, routes outputs to the correct next package. |
| **Chain Contract** | Each package's formal interface: what it reads (predecessor output), what it produces (successor input), detection strategy, →Marker Files, guaranteed outputs. |
| **Management Framework (Shared Spine)** | Consolidated governance trail per project: Decision Log, Change Log, Issue Log, Lessons Learned, Action Items, Assumptions & Dependencies. Phase-prefixed IDs prevent collision. |
| **Phase-Prefixed ID** | Entry numbering for shared registers: `{PHASE}-{TYPE}-{NNN}` (e.g., `PILC-D-001` = AI-PILC Decision #001, `ADLC-C-002` = AI-ADLC Change #002). Prevents cross-package ID collision. |
| **Detection by Marker** | Architectural principle: packages find predecessor outputs by →Marker File presence, never by hardcoded path. Enables flexibility in folder placement. |
| **Graceful Degradation (OR-Input)** | Package principle: optional inputs enrich output when present but NEVER block when absent. Every package works standalone. Missing predecessors = reduced output, not failure. |
| **Ownership Model** | Three values for generated files: `generated` (tool manages, may overwrite), `hybrid` (tool-seeded, team-edited, →Custom Markers preserved), `user` (team-owned, tool treats as read-only). |
| **Append-if-Exists / Create-if-Absent** | Shared file contribution behavior: when a package encounters a shared artifact (e.g., AGENT_REGISTRY), it appends its content. If the file doesn't exist yet, it creates it with headers + its entries. |
| **Territory Rule** | Each package owns governance for its domain ONLY. AI-PILC checks PIP quality — never code. AI-GCE checks code/process — never PIP documents. No overlap permitted. |
| **Agent Governance Contract** | Cross-package standard for agent naming (`{domain}-{function}-agent.md`), anatomy (required sections), shortcut triggers (`{3-LETTER}__`), territory ownership, lifecycle, tier alignment. |
| **Shortcut Trigger** | Pattern `{3-LETTER-UPPERCASE}__` (three capitals + double underscore) to invoke →Governance Agents. Examples: `SDC__`, `SGV__`, `IQA__`, `BLH__`. Globally unique per workspace. |
| **RAG Status** | Red / Amber / Green health indicator used in dashboards. Red = blocked/critical, Amber = at risk, Green = on track. |
| **Injectable Workflow Package** | The core product type of the AI-* family: a set of steering files and rule details that, when installed into a Kiro workspace, guide an AI assistant through a structured professional process. |
| **AI-DLC v1 (AI-Driven Development Life Cycle)** | Amazon's open-source build lifecycle ([awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)). NOT part of the AI-* Family — but the AI-* chain produces the workspace AI-DLC v1 consumes and builds within. |

---

## G. Planned Package Concepts (AI-ILC, AI-POLC, AI-UXD, AI-PPM)

| Term | Definition |
|------|-----------|
| **Idea Brief / Feature Brief** | AI-ILC output: structured evaluation of a raw idea — shaped, scored against criteria, and routed (to project initiation as PIP input, or to feature backlog). |
| **Product Backlog Package (PBP)** | AI-POLC output: product ownership artifacts including user stories, Definition of Ready, release slicing, acceptance criteria standard, value-based prioritization (→WSJF). |
| **WSJF (Weighted Shortest Job First)** | Value-based prioritization model from SAFe: (Business Value + Time Criticality + Risk Reduction) / Job Size. Used in AI-POLC for ordering decisions. |
| **UX Design Package (UXP)** | AI-UXD output: user personas, journey maps, information architecture, user flows, design system + →Design Tokens, accessibility baseline. |
| **Design Tokens** | Named values representing visual design decisions (colors, typography, spacing, motion, breakpoints). Platform-agnostic format that can be compiled to CSS variables, Swift constants, etc. |
| **Information Architecture (IA)** | Content organization discipline: navigation structure, labeling systems, categorization schemes, search systems. Defines HOW users find things. |
| **Accessibility Baseline** | WCAG target level (A/AA/AAA) and compliance checklist. Part of UXP; enforced by →AI-GCE once installed. |
| **Portfolio Register** | AI-PPM output: cross-project inventory with prioritization scores, resource allocation, health status, dependency mapping, and strategic alignment assessment. |
| **User Persona** | Fictional character representing a user segment. Includes: demographics, goals, frustrations, behaviors, scenarios. Drives UX decisions and acceptance criteria. |
| **User Journey Map** | Visual representation of the steps a →User Persona takes to accomplish a goal. Includes touchpoints, emotions, pain points, and opportunities at each stage. |
| **Definition of Ready (DoR)** | Criteria a backlog item must meet BEFORE it can be pulled into a sprint. Ensures work items are actionable. Counterpart to →Definition of Done. |

---

## H. Methodology & Platform Concepts

| Term | Definition |
|------|-----------|
| **Kiro** | AI-powered development environment that this family of packages targets. Provides: steering files, hooks, agents, specs, and MCP integration. |
| **Kiro Steering** | File-based rule system in `.kiro/steering/` that instructs the AI assistant how to behave. Always-included, fileMatch (conditional), or manual (user-invoked via `#`). |
| **Kiro Hook** | Event-triggered automation in `.kiro/hooks/`. Fires on IDE events (fileEdited, promptSubmit, agentStop, etc.) and performs an action (askAgent or runCommand). |
| **Kiro Agent** | Specialized AI task executor in `.kiro/agents/`. Has defined purpose, tools, and trigger. Invoked by shortcut or manually. |
| **MCP (Model Context Protocol)** | Standard protocol for connecting AI assistants to external tools/services. Configured via `mcp.json`. |
| **Human-in-the-Loop** | Interaction model where the AI proposes and the human approves at →Stage Gates. No autonomous progression past checkpoints. Core principle of all lifecycle packages. |
| **Persona (AI-* System)** | Role definition that makes AI output read like domain-expert writing. Primary persona = whole-package voice. Sub-role persona = specialist lens layered during specific stages. |
| **Sub-Role** | Specialist lens ADDED on top of the primary →Persona during a stage requiring different thinking (e.g., Financial Analyst sub-role during Business Case stage). Additive, never replacing. Maximum two per stage. |
| **Core-Workflow / Core-Generator / Core-Engine** | The master orchestration file in each package. Defines the complete execution logic: phases, stages, transitions, gates, loading instructions. Always loaded first. |
| **Rule Details** | Folder containing detailed instructions for each stage/mapping/generator. Referenced from the core file but loaded on demand to conserve context. |
| **Session Continuity** | Mechanism for resuming interrupted workflows. State file captures: current phase, current stage, completed stages, pending decisions, depth level, active extensions. Enough to resume cold. |
| **State File** | Per-package progress tracker (e.g., `pilc-state.md`, `adlc-state.md`, `tge-state.md`). Records workflow position, decisions made, and configuration. →Marker File. |

---

## Maintenance

This glossary is updated when:
- A new package is built (add its domain terms)
- A new concept is introduced in any package file
- A term definition needs clarification based on user feedback
- Terms are deprecated or renamed

**Owner:** `` (shared across all packages)
**Sync trigger:** a governance review verifies no new unglossaried terms were introduced whenever a package is built or updated.

*Knowledge Document | Created: 2026-06-11 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
