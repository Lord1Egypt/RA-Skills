<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Technology Stack Selection

## Stage: 6 of 13
## Phase: 🟡 DECISIONS
## Execution: ALWAYS

---

## Purpose

Select the concrete technology for every container identified in Stage 5. Each selection is justified against architecture principles, constraints, team context, and decision drivers. Major selections produce formal ADRs.

**CTO Mindset:** "These choices live with us for 5+ years. I need to balance proven reliability, team productivity, ecosystem maturity, and constraint compliance."

---

## Depth Adaptation

| Depth | Stack Selection Behavior |
|-------|------------------------|
| **Minimal** | 2 options per major choice. Brief rationale. ADRs only for top 2-3 decisions (backend language, database, framework). |
| **Standard** | 3-4 options per choice with pros/cons table. ADR per major technology category. Full Technology Stack document with rationale per selection. |
| **Comprehensive** | 4-5 options with deep comparison (ecosystem maturity, performance benchmarks, license audit, community health). ADR per decision. Extended evaluation against all constraints and principles. Version-specific recommendations. |

---

## Step-by-Step Execution

### Step 1: Load Context

1. Container list (Stage 5) — what needs technology assigned
2. Architecture Principles (Stage 3) — especially technology-related principles
3. Constraints (Stage 3) — hard limits on technology choices
4. Team Context (Stage 2) — skills, size, maturity
5. Scale Targets (Stage 2) — performance and capacity requirements
6. Quality Attributes (Stage 3) — priorities that influence tech selection

---

### Step 2: Organize Decisions by Category

Group technology decisions into logical categories. Present and decide one category at a time:

| Category | Decisions Involved | ADR? |
|----------|-------------------|:----:|
| **Backend Runtime & Framework** | Language, runtime version, application framework, ORM/data access | ✅ Yes |
| **Frontend & UI** | SPA framework, component library, state management, build tooling | ✅ Yes |
| **Database** | Primary RDBMS, connection pooling, replication strategy | ✅ Yes |
| **Caching** | Cache engine, use cases (session, config, query), eviction strategy | ✅ if multiple options viable |
| **Search** | Full-text search engine (if required) | ✅ if not built-in DB |
| **Message Queue / Job System** | Queue technology, job scheduling, retry/DLQ strategy | ✅ Yes |
| **File/Object Storage** | Attachment storage approach | ⚠️ Only if non-trivial choice |
| **Real-Time** | WebSocket/SSE technology, pub-sub for live updates | ✅ if core feature |
| **Deployment & Containerization** | Container runtime, orchestration, CI/CD tooling | ✅ Yes |
| **Observability** | Metrics, logging, tracing, alerting stack | ✅ if multiple viable stacks |
| **Additional** (project-specific) | AI integration approach, email engine, PDF generation, i18n, etc. | ⚠️ Per decision |

---

### Step 3: Evaluate Options Per Category

For EACH category, produce a structured evaluation:

```markdown
## {Category Name}

### Container(s) Affected: {which containers from Stage 5}

### Decision Drivers (for this category)
- {Driver 1 — from principles/constraints/team context}
- {Driver 2}
- {Driver 3}
- {Driver 4}

### Options Evaluated

| Option | Description | Pros | Cons | Constraint Compliance |
|--------|-------------|------|------|:---------------------:|
| **(a) {Name + Version}** | {1-sentence description} | {Key advantages — 3-5 bullets} | {Key disadvantages — 2-4 bullets} | {✅ All / ⚠️ Partial / ❌ Violates C{n}} |
| **(b) {Name + Version}** | {description} | {pros} | {cons} | {compliance} |
| **(c) {Name + Version}** | {description} | {pros} | {cons} | {compliance} |

### Recommended: Option ({x}) — {Name}

**Rationale:** {3-5 sentences. Reference decision drivers. Explain why this wins given the specific context — not just "it's popular." Address why alternatives were not chosen.}

### Consequences
- **Enables:** {what this choice makes possible}
- **Constrains:** {what downstream decisions this locks}
- **Risk:** {what could go wrong with this choice}

→ _This decision generates ADR-{nnn}_

**Your Decision:** _[awaiting input]_
```

---

### Step 4: Constraint Compliance Gate

CRITICAL: Before recommending ANY technology, verify:

```
For each technology option:
  □ Does it comply with deployment constraint? (on-prem capable?)
  □ Does it comply with licensing constraint? (open-source? free?)
  □ Does the team have or can acquire skills for it?
  □ Does it meet performance requirements?
  □ Does it support required features? (RTL, i18n, accessibility, etc.)
  □ Is it actively maintained? (last release < 12 months)
  □ Does it have production track record at similar scale?
```

**If an option violates ANY constraint → mark it ❌ and do NOT recommend it.** Note the violation in the Cons column.

---

### Step 5: Decision Interaction Model

Present decisions to user in batches by category:

**Batch 1: Core Stack (Backend + Database)**
- These are the most impactful; decide first
- Other decisions depend on these

**Batch 2: Frontend & UI**
- Often influenced by backend choice (shared language benefits)

**Batch 3: Infrastructure & Supporting Services**
- Cache, queue, search, storage, monitoring
- Lower risk; more interchangeable

**Within each batch:**
- Present the evaluation table
- State the recommendation with rationale
- Wait for user decision
- Produce ADR immediately upon decision
- Move to next category

**Shortcut:** If user says "accept all recommendations" → produce all ADRs in batch; summarize choices.

---

### Step 6: Technology Compatibility Check

After all selections are made, verify the stack works together:

| Check | What to Verify |
|-------|---------------|
| Language ecosystem | Selected libraries/frameworks available in chosen language |
| Protocol compatibility | Selected tools can communicate (e.g., DB driver exists for language) |
| Deployment compatibility | All components can run in chosen deployment model |
| License compatibility | No license conflicts between components (e.g., AGPL + proprietary) |
| Version compatibility | Selected versions are mutually compatible |
| Operational coherence | All components manageable by stated team size |

If conflict found → flag to user and propose resolution.

---

### Step 7: Produce Technology Stack Summary

```markdown
## Technology Stack Summary

### Core Stack

| Layer | Technology | Version | License | Rationale (1-line) | ADR |
|-------|-----------|:-------:|:-------:|-------------------|:---:|
| Backend Runtime | {tech} | {ver} | {license} | {why} | ADR-{nnn} |
| Backend Framework | {tech} | {ver} | {license} | {why} | ADR-{nnn} |
| Frontend Framework | {tech} | {ver} | {license} | {why} | ADR-{nnn} |
| UI Component Library | {tech} | {ver} | {license} | {why} | — |
| Primary Database | {tech} | {ver} | {license} | {why} | ADR-{nnn} |
| ORM / Data Access | {tech} | {ver} | {license} | {why} | — |

### Supporting Services

| Service | Technology | Version | License | Purpose | ADR |
|---------|-----------|:-------:|:-------:|---------|:---:|
| Cache | {tech} | {ver} | {license} | {purpose} | — |
| Search | {tech} | {ver} | {license} | {purpose} | ADR-{nnn} |
| Message Queue | {tech} | {ver} | {license} | {purpose} | ADR-{nnn} |
| File Storage | {tech} | {ver} | {license} | {purpose} | — |
| Real-Time | {tech} | {ver} | {license} | {purpose} | — |

### Deployment & Operations

| Concern | Technology | Version | License | Purpose | ADR |
|---------|-----------|:-------:|:-------:|---------|:---:|
| Containerization | {tech} | {ver} | {license} | {purpose} | — |
| Orchestration | {tech} | {ver} | {license} | {purpose} | ADR-{nnn} |
| CI/CD | {tech} | {ver} | {license} | {purpose} | — |
| Metrics | {tech} | {ver} | {license} | {purpose} | — |
| Logging | {tech} | {ver} | {license} | {purpose} | — |
| Alerting | {tech} | {ver} | {license} | {purpose} | — |

### Build & Development Tools

| Tool | Technology | Purpose |
|------|-----------|---------|
| Package Manager | {tech} | {purpose} |
| Linting | {tech} | {purpose} |
| Testing | {tech} | {purpose} |
| API Documentation | {tech} | {purpose} |
```

---

### Step 8: Update Container Diagram

Now that technologies are selected, update the C4 L2 diagram with actual technology labels (replacing "TBD"):

- Update the Container Diagram document (Stage 5 output)
- Replace technology placeholders with selected technologies
- Note in state file that C4 L2 is now technology-annotated

---

### Step 9: Produce ADRs

For each major decision, produce a standalone ADR file in `{output_root}/ADR/`:

**ADR file naming:** `ADR-{NNN}_{Decision_Title_Slug}.md`

**Minimum ADRs for a Standard-depth workflow:**
- Backend language/framework selection
- Database selection
- Frontend framework selection (if UI exists)
- Deployment/orchestration approach

**Content per ADR:** Use template `templates/adr-template.md` — populated with the evaluation data from Step 3.

---

### Step 10: Present for Review

```markdown
## Review: Technology Stack — {system_name}

I've selected technology for all {n} containers.

**Core decisions:**
- Backend: {tech + framework}
- Frontend: {tech + library}
- Database: {tech}
- Cache: {tech}
- Queue: {tech}
- Deployment: {tech}

**Stack characteristics:**
- Language consistency: {mono-language or polyglot}
- License compliance: {all open-source / mixed / issues}
- Team alignment: {matches skills / some learning needed / major reskilling}
- Ecosystem maturity: {all mature / some emerging}

**ADRs produced:** {n} (ADR-{first} through ADR-{last})

**Full document:** Saved to `{file_path}`

---

**Your response:**
- (a) **Approve** — Technology stack is locked; proceed
- (b) **Challenge a choice** — I disagree with {specific selection}; let's discuss
- (c) **Add technology** — Missing a component I need
- (d) **Reconsider approach** — The overall stack direction needs rethinking
```

---

### Step 11: Log and Transition

1. Update state: Stage 6 = ✅ Done; Current Stage = 7 (or 8 if Stage 7 is skipped)
2. Update state: ADR register with all new ADRs
3. Update Architecture Workbook: session log + resolved decision backlog items
4. Determine Stage 7 applicability: Does the system need multi-tenancy? If no → skip to Stage 8

Display:

```
✅ Stage 6: Technology Stack Selection — Complete

🔧 Stack: {backend} + {frontend} + {database} + {n} supporting services
📐 ADRs: {n} produced (ADR-{first} to ADR-{last})
📄 Saved to: {file_path}

{If Stage 7 applicable:}
Next → Stage 7: Multi-Tenancy & Data Isolation Strategy

{If Stage 7 skipped:}
Next → Stage 8: Security & Identity Architecture (Stage 7 skipped — single-tenant system)

Proceeding...
```

---

## Output File

Save to:
- Numbered: `{output_root}/04_Technology_Stack.md`
- Phase folders: `{output_root}/decisions/Technology_Stack.md`

---

## Technology Selection Anti-Patterns

| Anti-Pattern | Why It's Wrong | Do Instead |
|-------------|---------------|-----------|
| Choosing what's "hot" / trending | Hype ≠ production readiness | Evaluate maturity, community, maintenance |
| Choosing what CTO personally likes | Personal preference ≠ team fit | Consider team skills and hiring pool |
| Over-engineering for scale you don't have | Complexity without benefit | Design for current + 2-3x; re-evaluate when exceeded |
| Ignoring operational burden | Dev-friendly ≠ ops-friendly | Consider: who maintains this at 2 AM? |
| Single-source evaluation | Cherry-picked pros | Always evaluate 2+ alternatives fairly |
| Vendor lock-in | Future flexibility sacrificed | Prefer standard protocols and abstractions |
| Decision without ADR | Future team won't understand why | Document every non-obvious choice |
