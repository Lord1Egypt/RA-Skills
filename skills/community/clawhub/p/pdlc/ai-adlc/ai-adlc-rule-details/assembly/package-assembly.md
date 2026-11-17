<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Architecture Package Assembly

## Stage: 13 of 13
## Phase: 🚀 ASSEMBLY
## Execution: ALWAYS (Final Stage)

---

## Purpose

Consolidate all architecture deliverables into a complete, cross-referenced, quality-checked Architecture Package (AP). Verify consistency across all documents and ADRs, identify unresolved questions, and produce a package README that serves as the table of contents and reading guide.

---

## Depth Adaptation

| Depth | Assembly Behavior |
|-------|------------------|
| **Minimal** | Inventory check. Brief consistency scan. Package README with TOC and reading order. Quality score. |
| **Standard** | Full cross-reference integrity check (containers ↔ tech stack ↔ ADRs ↔ security). Completeness audit. Open questions summary. Package README with full narrative. Quality score with per-category breakdown. |
| **Comprehensive** | Deep consistency audit with explicit verification per document pair. Traceability matrix (requirement → principle → decision → ADR). Gap analysis against requirements. Executive architecture summary. Package README with detailed reading guide and decision map. Quality score with recommendations for future iterations. |

---

## Step-by-Step Execution

### Step 1: Inventory All Artifacts

Scan the output directory and compile a complete inventory:

```markdown
## Package Inventory

### Architecture Documents

| # | Document | Stage | File Path | Status |
|---|----------|:-----:|-----------|:------:|
| 1 | Architecture Vision & Principles | 3 | {path} | ✅ Complete |
| 2 | System Context (C4 L1) | 4 | {path} | ✅ Complete |
| 3 | Container Diagram (C4 L2) | 5 | {path} | ✅ Complete |
| 4 | Technology Stack | 6 | {path} | ✅ Complete |
| 5 | Multi-Tenancy Architecture | 7 | {path} | ✅ / ⏭️ Skipped |
| 6 | Security & Identity Architecture | 8 | {path} | ✅ Complete |
| 7 | Data Architecture | 9 | {path} | ✅ Complete |
| 8 | API Architecture | 10 | {path} | ✅ Complete |
| 9 | Integration Architecture | 11 | {path} | ✅ Complete |
| 10 | Infrastructure & Deployment | 11 | {path} | ✅ Complete |
| 11 | Component Design (C4 L3) | 12 | {path} | ✅ Complete |

### Architecture Decision Records

| ADR # | Title | Status | Stage |
|:-----:|-------|:------:|:-----:|
| ADR-001 | {title} | Accepted | {n} |
| ADR-002 | {title} | Accepted | {n} |
| ... | ... | ... | ... |

### Supporting Documents

| Document | Path | Purpose |
|----------|------|---------|
| Architecture Workbook | {path} | Decision backlog, open questions, discussion notes |
| adlc-state.md | {path} | Workflow state and progress |
| ADR-000 Template | {path} | Template for future ADRs |
```

---

### Step 2: Cross-Reference Integrity Check

Verify consistency across ALL documents:

| Check | Documents Involved | What to Verify |
|-------|-------------------|---------------|
| **System name** | All documents | Same name everywhere |
| **Container names** | C4 L2, Tech Stack, Component Design, Infrastructure | Exact name match |
| **Technology labels** | C4 L2, Tech Stack ADRs, Infrastructure, Component Design | Same tech in all references |
| **External systems** | C4 L1, Integration Architecture | Every L1 external has integration pattern defined |
| **Actors** | C4 L1, Security (auth methods), API (consumers) | All actors have auth path and API access defined |
| **Entities** | Data Architecture, Component Design | Every entity has owning module; every module has entities listed |
| **Modules** | Component Design, API Architecture | Every API endpoint maps to a module |
| **Principles** | Vision, all subsequent documents | No recommendation contradicts a principle |
| **Constraints** | Vision, all subsequent documents | No design choice violates a constraint |
| **ADR decisions** | ADR files, parent documents | ADR summary in parent matches full ADR content |
| **Security patterns** | Security doc, API doc, Multi-tenancy doc | Auth/authz consistently applied |
| **Tenant scoping** | Multi-tenancy, Data, API, Component Design | Consistent isolation at all layers |

**If inconsistency found:**
1. Identify which document is authoritative (latest stage's decision wins)
2. Flag to user: "Inconsistency: {doc A} says X, {doc B} says Y"
3. Update the incorrect document
4. Note correction in Architecture Workbook

---

### Step 3: Completeness Audit

```markdown
## Completeness Audit

### Document Coverage

| Check | Expected | Actual | Gap? |
|-------|:--------:|:------:|:----:|
| Architecture documents | {10-11} | {n} | {Any missing?} |
| ADRs for major decisions | {5-10 typical} | {n} | {Any undocumented decisions?} |
| C4 diagrams (L1 + L2 + L3) | 3 minimum | {n} | {Missing levels?} |
| All containers have technology | 100% | {%} | {Any still TBD?} |
| All externals have integration pattern | 100% | {%} | {Undesigned integrations?} |
| All modules have entity ownership | 100% | {%} | {Orphan entities?} |

### Principle Coverage

| Principle | Addressed In | Verified? |
|-----------|-------------|:---------:|
| P1: {name} | {Which documents apply it} | {✅ / ⚠️} |
| P2: {name} | {Documents} | {✅ / ⚠️} |

### Open Questions (from Workbook)

| # | Question | Status | Impact if Unresolved |
|---|----------|:------:|---------------------|
| 1 | {question} | {Resolved / Open / Deferred} | {What breaks or is unclear} |
```

---

### Step 4: ADR Register Validation

```markdown
## ADR Validation

| Check | Result |
|-------|--------|
| Sequential numbering (no gaps) | {✅ / ❌ — which missing?} |
| All have "Accepted" or "Proposed" status | {✅ / ❌ — which stuck?} |
| All cross-referenced in parent document | {✅ / ❌ — which orphaned?} |
| No conflicting ADRs | {✅ / ❌ — which conflict?} |
| Options actually evaluated (not rubber-stamp) | {✅ / ⚠️ — which lack alternatives?} |
| Consequences documented | {✅ / ❌ — which missing consequences?} |
```

---

### Step 5: Diagram Consistency

```markdown
## Diagram Integrity

| Check | Result |
|-------|--------|
| C4 L2 containers ⊆ C4 L1 system boundary | {✅ / ❌} |
| C4 L3 components ⊆ C4 L2 container | {✅ / ❌} |
| Technology labels on L2 match Tech Stack doc | {✅ / ❌} |
| External system names match across L1, Integration doc | {✅ / ❌} |
| Actor names match across L1, Security, API docs | {✅ / ❌} |
| All relationships labeled (verb + protocol) | {✅ / ❌} |
| No orphan nodes in any diagram | {✅ / ❌} |
```

---

### Step 6: Package Quality Score

| Dimension | Score (1-5) | Criteria |
|-----------|:-----------:|----------|
| **Completeness** | {n} | All expected documents present; all stages covered |
| **Consistency** | {n} | Cross-references match; no contradictions; terminology stable |
| **Clarity** | {n} | Documents readable by target audience (developers + tech leads) |
| **Actionability** | {n} | Development team can start building from these docs |
| **Traceability** | {n} | Requirements → principles → decisions → design traceable |

**Overall Package Quality: {sum}/25**

| Score | Rating |
|:-----:|--------|
| 22-25 | 🟢 Excellent — ready for development handoff |
| 18-21 | 🟡 Good — minor gaps; team can start with caveats |
| 13-17 | 🟠 Adequate — notable gaps; supplement with verbal guidance |
| 5-12 | 🔴 Incomplete — significant work needed |

---

### Step 7: Produce Architecture Package README

```markdown
# Architecture Package — {system_name}

## Overview

| Field | Value |
|-------|-------|
| System | {system_name} |
| Architecture Style | {Modular Monolith / Microservices / etc.} |
| Primary Technology | {Backend: X, Frontend: Y, DB: Z} |
| Deployment | {Docker Compose / K8s / etc.} on {cloud / on-prem} |
| Scale Target | {users, tenants, transactions} |
| Multi-Tenant | {Yes — model / No} |
| ADRs | {n} decisions recorded |
| Package Quality | {score}/25 — {rating} |
| Date Produced | {date} |
| Produced Via | AI-ADLC v1.0.0 |

---

## Reading Order (Recommended)

| Order | Document | What You'll Learn |
|:-----:|----------|------------------|
| 1 | Architecture Vision | Principles, constraints, quality priorities |
| 2 | System Context (C4 L1) | Who uses the system; what it connects to |
| 3 | Container Diagram (C4 L2) | Major deployable units and their relationships |
| 4 | Technology Stack | What technology was chosen for each container and why |
| 5 | Multi-Tenancy (if applicable) | How tenant isolation works at every layer |
| 6 | Security & Identity | How auth, authz, encryption, and audit work |
| 7 | Data Architecture | Schema strategy, entities, storage layers |
| 8 | API Architecture | API conventions, versioning, error handling |
| 9 | Integration & Infrastructure | External system connections; deployment topology |
| 10 | Component Design (C4 L3) | Internal module structure; dependency rules |
| — | ADRs | Deep-dive on specific decisions (reference as needed) |

---

## Architecture at a Glance

{2-3 paragraph executive summary of the architecture — what it is, how it's structured, what makes it distinctive}

---

## Key Architectural Decisions (Top {n})

| ADR | Decision | Impact |
|:---:|----------|--------|
| ADR-001 | {title} | {1-line impact} |
| ADR-002 | {title} | {1-line impact} |
| ... | ... | ... |

---

## Principles (Quick Reference)

| ID | Principle | One-Liner |
|:--:|-----------|-----------|
| P1 | {name} | {statement} |
| P2 | {name} | {statement} |
| ... | ... | ... |

---

## Constraints (Quick Reference)

| # | Constraint | Impact |
|---|-----------|--------|
| C1 | {constraint} | {impact} |
| ... | ... | ... |

---

## Open Items / Future Decisions

| # | Item | Context | When to Decide |
|---|------|---------|:--------------:|
| 1 | {open question or deferred decision} | {why it's open} | {Phase/milestone} |

---

## For Development Team

This package is the architectural blueprint. When starting development:
1. Read documents in the recommended order above
2. Reference ADRs when you encounter "why was X chosen?"
3. Follow the principles — they constrain your implementation choices
4. Respect the constraints — they are non-negotiable
5. Module boundaries (C4 L3) define code organization
6. API conventions (Stage 10) define your endpoint implementation

---

*Architecture Package produced: {date}*
*Methodology: AI-ADLC v1.0.0*
*Status: Ready for development team onboarding*
```

---

### Step 8: Finalize Workbook

Update Architecture Workbook:
- Mark all resolved questions as "✅ Resolved"
- List remaining open questions clearly
- Add final session log entry
- Close decision backlog (mark remaining items as "Deferred to development")

---

### Step 9: Update State File

```markdown
## Final State Update

- Stage 13: ✅ Done
- Status: Complete
- Last Updated: {timestamp}
- Package Quality: {score}/25
- Total ADRs: {n}
- Open Questions: {n} (carried into development)
```

---

### Step 9b: Emit Feasibility / Cost-Risk Signal to AI-POLC (Architecture→Product cost loop)

AI-POLC and AI-ADLC are same-layer peers, so this is a **direct downstream signal recorded in `adlc-state.md`** (no AI-FLO; AI-POLC reads it at its workspace-detection). This closes the real-world **Architecture → Product cost/risk re-prioritization loop**: architecture's feasibility verdict reshapes product prioritization ("that epic is 3× the cost — reorder the roadmap").

**Produce relative bands, NEVER dollar estimates.** The signal is advisory effort/complexity bands + technical-risk flags, mapped to the product's epics/areas where identifiable:

```markdown
## Downstream Signals

| Signal | Status |
|--------|--------|
| cost-risk-notes | available |

### Feasibility / Cost-Risk (for AI-POLC re-prioritization)

| Epic / Area | Effort Band | Technical Risk | Driver (why) |
|-------------|:-----------:|:--------------:|--------------|
| {epic or functional area} | {S / M / L / XL} | {🟢 low / 🟡 med / 🔴 high} | {e.g., "new integration + multi-tenant isolation", "depends on unproven pattern", "high coupling to legacy"} |

> Bands are **relative complexity/effort**, derived from component count, integration complexity, NFR difficulty, and pattern novelty — not cost figures. Advisory input to WSJF Job Duration / value-effort scoring. AI-POLC consumes via `adlc-state.md` and applies the "AP feasibility/cost-risk update" re-prioritization trigger.
```

Map bands to the product areas/epics when the AP can be aligned to them; otherwise emit per architecture area and let AI-POLC associate. **Standalone-safe:** if no AI-POLC is present, the signal is simply recorded and unused. If the architecture changes later (reconciliation), refresh this table so POLC can re-score.

---

### Step 10: Present Final Summary

```
🎉 AI-ADLC WORKFLOW COMPLETE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 Architecture Package for "{system_name}" is ready.

📊 Package Summary:
   • Documents produced: {n}
   • ADRs recorded: {n}
   • C4 diagrams: {n} (L1 + L2 + L3)
   • Stages completed: {n}/13
   • Principles defined: {n}
   • Constraints documented: {n}
   • Open questions: {n} (for development phase)
   • Package quality: {score}/25 — {rating}

📁 Package location: {output_root}/
📋 Package README: {readme_path}
📐 ADR folder: {adr_path}/ ({n} records)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📌 Next Steps:
   1. Review package with Technical Lead and senior developers
   2. Resolve {n} open questions during first design sprint
   3. Run AI-DWG to generate the development workspace from this Architecture Package
   4. Begin AI-DLC v1 construction phase using this architecture as input
   5. ADR register continues to grow during development (new decisions arise)

🔀 **Chain Navigation (what's next in the AI-* Family):**
   • Sequential next: **AI-DWG** (`_DWG_`) — Development Workspace Generation
   • Or ask AI-FLO: type `_FLO_` for routing guidance based on your project state
   • Dashboard data: type `DAT__ pdlc/adlc` to update the family dashboard

⚠️ **IMPORTANT: Start the next package (AI-DWG) in a NEW session.**
   Each AI-* package loads a full workflow into context;
   a fresh session keeps it fast and focused.

The architecture is ready for development team onboarding.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| Some stages were skipped | Note in README; explain why; assess if package is still viable |
| ADRs have "Proposed" status (not accepted) | Flag as open decisions; recommend resolving before development start |
| Contradictions found during assembly | Resolve with user before finalizing; never ship contradictory docs |
| User stopped early | Produce partial package; clearly state what's missing and impact |
| Architecture evolved during workflow (early decisions revised) | Verify all downstream docs updated; cross-reference check is critical |

---

## Output File

Save to:
- Numbered: `{output_root}/ARCHITECTURE_PACKAGE_README.md`
- Phase folders: `{output_root}/ARCHITECTURE_PACKAGE_README.md`

---

## Assembly Quality Checklist

| Check | Pass Criteria |
|-------|---------------|
| All documents present | Every stage produced its expected output |
| Cross-references valid | Names, technologies, entities consistent across docs |
| ADRs complete | All registered, properly formatted, cross-referenced |
| Diagrams consistent | C4 levels align; technology labels match |
| Principles respected | No document contradicts the Vision |
| Constraints honored | No design violates constraints |
| Open items tracked | Unresolved questions explicitly listed with context |
| README navigable | A new reader can find their way through the package |
| Actionable | A development team can start building from this package |
