# AI-* Family — Artifact Ownership & Access Governance Model

> **Status:** Reference (as-is map + target model)
> **Scope:** Cross-cutting — the ownership-bearing chain (**AI-ADLC, AI-UXD, AI-POLC → AI-DWG → AI-GCE, AI-TGE**) plus upstream initiation (**AI-PILC**) and the **AI-DLC v1** runtime. The portfolio/edge packages (**AI-ILC, AI-PPM, AI-FLO**) carry provenance but do not define file ownership.
> **Created:** 2026-06-09
> **Author:** Maheri
> **Related:** `FAMILY_STRUCTURE.md`, `NAMING_AND_OWNERSHIP.md` (provenance keys + A-dominant naming convention), idea `005-lifecycle-change-propagation` (ownership dimension folded in), siblings `003`/`004`

---

## 1. Purpose

This document is the single source of truth for **how ownership of artifacts and files is established, generated, and enforced across the AI-* Family** — so that the wrong person (or the wrong AI session) cannot change a file they do not own.

It answers four questions end-to-end:

1. **What** can be owned (the ownable units at each layer of the chain)?
2. **Who/what** defines, generates, and enforces ownership at each stage?
3. **How** is "the wrong person can't change this file" actually guaranteed today — preventively or detectively?
4. **Where** are the gaps, and what is the target model that closes them?

It deliberately covers the complexity the family must handle: **DDD bounded contexts, microservice/data ownership, and team topology** — because those are the boundaries that ownership attaches to.

---

## 2. The ownership problem

The AI-* Family produces a chain of dependent artifacts and ultimately a living, operated system:

```
PIP (AI-PILC) → [ AP (AI-ADLC) ∥ UXP (AI-UXD) ∥ PBP (AI-POLC) — peer inputs, ≥1 ] → DW (AI-DWG) → enforcement layer (AI-GCE) + test governance (AI-TGE) → operated software (AI-DLC v1 sessions)
```

> **Peer-input note (OI-069):** AI-DWG composes the workspace from any non-empty subset of {AP, UXP, PBP}; none is mandatory-singular. File-ownership boundaries themselves still originate in **AI-ADLC** (DDD bounded contexts) — see Stage A — so the DEFINE→GENERATE→ENFORCE relay below remains ADLC→DWG→GCE.

Every layer creates files that *someone* must be accountable for and that *not everyone* should be allowed to change. Today, ownership is a real, well-developed concept — but it is **concentrated at the code/workspace layer and is largely detective rather than preventive**, and it does **not** govern the upstream artifacts or the package-development workspace itself.

---

## 3. Ownership planes

Ownership is not one thing. It exists on four distinct planes, each with a different owner type and a different enforcement maturity.

| Plane | Ownable unit | Owner type | Defined where | Enforced where | Maturity |
|-------|--------------|------------|---------------|----------------|:--------:|
| **P1 — Code / workspace files** | folders, modules, steering files | team / CODEOWNER | AI-DWG (`CODEOWNERS`) | AI-GCE (GOV-ROLE, GOV-TT) + Git platform | **Strong** |
| **P2 — Domain entities & data** | bounded-context entities, service data stores | owning bounded context / service team | AI-ADLC (DDD, MS-02) → AI-DWG (`domain-context.md`) | AI-GCE (entity-ownership, cross-service data rules) | **Strong** |
| **P3 — Upstream artifacts** | ADRs, charters, AP/PIP documents | author / accountable role (RACI) | AI-PILC (RACI), AI-ADLC (author convention) | — (convention only) | **Weak** |
| **P4 — Package-dev workspace** | the `*` source itself | persona (via steering fileMatch) | `.kiro/steering/*-rules.md` | — (convention only) | **Weak** |

The strength asymmetry is the central finding: **P1 and P2 are engineered; P3 and P4 rely on convention.**

---

## 4. As-is: the three-stage ownership relay (P1 + P2)

Ownership for code and domain artifacts is not a single feature — it is a relay handed across three packages.

```
   DEFINE                    GENERATE                      ENFORCE
   AI-ADLC          →        AI-DWG               →        AI-GCE
   ───────                   ──────                        ──────
   DDD bounded contexts      CODEOWNERS                    GOV-ROLE  (author ≠ approver)
   MS-01 one team/service    module-structure.md (Owner)   GOV-TT    (one context per team)
   MS-02 data ownership      role-isolation.md (SoD)       self-approval detection hook
   aggregate boundaries      domain-context.md (entity)    CODEOWNERS-based alert routing
```

### Stage A — AI-ADLC defines the boundaries (it never names a file owner)

| Source | Establishes |
|--------|-------------|
| `extensions/microservices/microservices.md` → **MS-01** | One service owns exactly one business capability / bounded context; one team per service |
| `extensions/microservices/microservices.md` → **MS-02** | Per-service data ownership — no other service reads/writes another's data store |
| `extensions/ddd-tactical/ddd-tactical.md` | Bounded contexts, aggregate boundaries, ubiquitous language |

### Stage B — AI-DWG generates the ownership artifacts

| Artifact (template) | What it owns | Generation source |
|---------------------|--------------|-------------------|
| `CODEOWNERS` (`templates/config/codeowners.md`) | folders → owners; steering & `CODEOWNERS` → architect/tech-lead; each `/src/{module}/` → module owner; `/src/shared/` → architect team | `mapping/components-to-structure.md` |
| `role-isolation.md` (`templates/steering/role-isolation.md`) | Segregation-of-Duties: who approves architecture vs. code vs. security vs. steering-file changes | `mapping/team-to-agreements.md` |
| `module-structure.md` | `\| Module \| Responsibility \| Bounded Context \| Owner \|` + dependency rules | `mapping/components-to-structure.md` |
| `domain-context.md` | **Entity ownership as a security boundary** — only the owning context may CREATE/UPDATE/DELETE; others reference by ID | `mapping/components-to-domain-context.md` |

### Stage C — AI-GCE enforces ownership at runtime

| Rule family | Derived from | Enforces |
|-------------|--------------|----------|
| **GOV-ROLE** | `role-isolation.md` + `CODEOWNERS` + `TEAM_AGREEMENTS.md` | Author ≠ approver (GOV-ROLE-004 "Session Owner ≠ Reviewer"); each module → exactly one team (GOV-ROLE-015/017); self-approval detection hook |
| **GOV-TT** (team topology) | `module-structure.md` + `CODEOWNERS` | One bounded context per team; cognitive-load limits; independent deployability; API-contract & steering-file ownership |
| **Alert routing** | `CODEOWNERS` | Routes each violation to the owner of the affected module |

> **Important:** No actual `CODEOWNERS` file exists in this package-dev workspace. It is a **generated runtime output** for downstream projects — only the template lives here.

---

## 5. How the guarantee actually works today

"The wrong person can't change this file" resolves to two enforcement modes, and the family is heavily weighted toward the second:

| Mode | Mechanism | Where | Effect |
|------|-----------|-------|--------|
| **Preventive** (blocks) | Git platform branch protection driven by `CODEOWNERS`; required CODEOWNER review | External Git platform (configured from generated `CODEOWNERS`) | A change *cannot merge* without owner approval |
| **Detective** (flags + logs) | GCE hooks (`fileEdited`, `agentStop`, `promptSubmit`) + JSONL compliance log | AI-GCE + AI-DLC v1 runtime | A wrong change is *detected, flagged, routed, and logged* — not hard-blocked in the editor |

Inside **AI-DLC v1 coding sessions**, enforcement is detective: `role-isolation.md` "AI MUST/MUST NOT" rules and GCE hooks fire, deviations are logged — but a determined wrong actor is flagged, not stopped. Hard prevention only exists at the Git-platform merge gate.

---

## 6. Gaps (the reason to build this)

| # | Gap | Plane | Impact |
|---|-----|-------|--------|
| G1 | **No ownership of upstream artifacts.** Nobody "owns" a specific ADR, charter, or AP doc beyond RACI/author convention. | P3 | A requirement or architecture decision can be changed with no segregation-of-duties check. |
| G2 | **Package-dev workspace ownership is convention-only.** Persona fileMatch + `workspace-rules.md` prohibitions are not enforceable. | P4 | Nothing blocks the wrong persona from editing another package's source. |
| G3 | **Runtime enforcement is detective, not preventive.** Hooks flag and log; they do not block. | P1/P2 | "Wrong person can't change" is true only at the Git merge gate, not in-session. |
| G4 | **Ownership-of-change across the lifecycle is unbuilt.** When a change lands, who owns re-synchronizing the now-stale artifacts is undefined. | all | Recognized in idea `005` but not yet built; ownership has no cross-chain dimension. |
| G5 | **No single ownership ledger.** Ownership facts are scattered across `CODEOWNERS`, `module-structure.md`, `domain-context.md`, RACI, and steering — no consolidated, queryable source. | all | "Who owns X?" requires reading 4+ files; drift between them is undetectable. |

---

## 7. Target model

The target is a **unified, plane-aware ownership model** with a single declarative source and graduated enforcement.

1. **One ownership ledger per scope.** A single declarative `OWNERS` manifest (or equivalent front-matter) that is the source of truth for all four planes; `CODEOWNERS`, `module-structure.md` Owner column, and RACI are *projections* of it, not independent records (closes G5).
2. **Extend the Owner concept up the chain.** AP and PIP artifacts carry an accountable owner and an approver-distinct-from-author rule, mirroring code-layer segregation of duties (closes G1).
3. **Enforceable package-dev ownership.** A `CODEOWNERS`-style mapping for `*` binding each package to its persona/owner, enforced by a pre-edit governance hook rather than convention alone (closes G2).
4. **Graduated preventive enforcement.** Promote the highest-risk ownership rules (steering files, security config, schema migrations, cross-context entity writes) from detective to preventive at the editor/session layer, not only at merge (closes G3).
5. **Change-ownership handoff.** Define who owns re-synchronization when a change crosses an ownership boundary — the connective tissue that ideas `003`/`004`/`005` orchestrate (closes G4).

---

## 8. Relationship to sibling ideas

The ownership model (the **noun** — *who owns what*) is carried inside idea **005** as a prerequisite layer; 003/004/005 are the **verbs** that act on owned things.

| Idea | Role relative to ownership |
|------|----------------------------|
| **003 — Version & Patch Manager** | The write-time *overwrite-protection* mechanic ownership uses when re-synchronizing files. |
| **004 — Change Request Management** | Governs the *decision* to change an owned artifact (who approves). |
| **005 — Lifecycle Change Propagation** | Orchestrates *who owns* re-synchronizing stale artifacts after a change — and now carries the ownership-definition layer itself (see the "Ownership Dimension" section of idea 005). |

---

*Document Version: 1.0 | Created: 2026-06-09 | Maintained by: Maheri*
