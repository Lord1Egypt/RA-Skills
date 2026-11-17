# Plan Phase — Detailed Methodology

Step-by-step process for the PLAN phase. PLAN MUST NOT begin until RESEARCH is complete and all output files exist in `migration-plan/research/`. Every decision must trace back to RESEARCH evidence — if you cannot cite it, go back.

## Step 5: Define Migration Direction and Target Topology

### 5.1 — Direction Assessment

The direction is determined by evidence, not preference:

| Direction | Evidence that points here |
| --- | --- |
| **Decomposition** (monolith → ASP.NET Core services) | High coupling across domains, deployment bottlenecks in CI/CD config, scaling constraints, team autonomy requirements stated by user |
| **Consolidation** (services → ASP.NET Core modular monolith or ABP module set) | Excessive inter-service calls in the integration catalog, ops overhead, data consistency issues, small team |
| **Cross-stack** (any source → chosen target: .NET default, or user-selected) | EOL/deprecated stack in dependency inventory, user-specified target, ecosystem gaps in stack research |
| **In-place modernization** (.NET Framework → .NET, same topology) | Stack is EOL but architecture is sound; low coupling already |
| **UI-only migration** (backend stays, UI → Blazor WASM/MAUI) | Backend is healthy and API-ready; UI stack is dead/expensive (WebForms, Silverlight, AngularJS) |
| **Hybrid** | Different directions per domain — document which applies where |

### 5.2 — UI Target Decision

Applies when the target is .NET (the default). For a user-chosen non-.NET target, derive the UI decision from `stack-research.md` and confirm with the user in pt-BR.

Default and evidence rules — verify versions via web search:

| Legacy UI | Preferred target | Evidence required to deviate |
| --- | --- | --- |
| WebForms, MVC/Razor, AngularJS, jQuery SPA, Silverlight | **Blazor WebAssembly** | Public SEO-critical site (consider SSR/Blazor Web App); realtime-first app (Blazor Server); existing Angular team mandate |
| WinForms, WPF, UWP, Xamarin.Forms | **.NET MAUI** | Windows-only kiosk (WinUI 3 acceptable); web-first requirement |
| Both web + desktop/mobile | **MAUI Blazor Hybrid** sharing Razor class libraries with the WASM app | — |

Record the decision in `00-roadmap.md` with cited evidence.

### 5.3 — Direction Documentation

```markdown
## Migration Direction: {Direction}

**Target stack**: {e.g., ASP.NET Core API + Blazor WebAssembly + EF Core + SQL Server}
**Rationale** — RESEARCH findings:
- {Finding — ref to research/file.md}
**User-confirmed constraints**:
- {Constraints provided by the user}
```

If the direction is ambiguous, ASK THE USER in pt-BR — present evidence per option and let them decide.

## Step 6: Design Seams and Facades

Load `references/strangler-fig-patterns.md` for the .NET seam catalog (YARP routes, DI seams, Blazor islands, EF Core data seams, event interception).

### 6.1 — Seam Identification

Per domain, identify where behavior can be intercepted without changing legacy code:

- **API seams** — route groups (`RouteConfig`, `[Route]` attributes, OWIN/ASP.NET Core endpoints). `file:line`.
- **Event seams** — message producers/consumers, `DomainEvents`, webhooks. `file:line`.
- **Data seams** — `DbContext`/`IDbConnection` call sites, repository interfaces already in place. `file:line`.
- **UI seams** — route-level page boundaries, component mount points, menu entries. `file:line`.

### 6.2 — Facade Layer Design

```markdown
## Seam: {Name}
**Type**: API | Event | Data | UI
**Location**: `file:line`
**Current behavior**: {what it does — referenced}
**Facade approach**: {pattern from strangler-fig-patterns.md — e.g., YARP route + feature flag}
**Routing mechanism**: YARP | FeatureManagement flag | DI selector | Event interceptor
**Rollback mechanism**: {how to instantly revert — e.g., flip flag, revert YARP transform}
```

### 6.3 — Dependency Order

1. Domains with **zero incoming dependencies** migrate first (leaf nodes).
2. Domains **many others depend on** migrate last (core/shared).
3. Shared tables need a documented strategy — dual-write, owner-service + API reads, or expand-contract.

Produce a dependency graph showing migration order.

## Step 7: Per-Domain Migration Plans

One file per bounded context: `migration-plan/domains/XX-domain-{name}.md`. Each file is designed to become the evidence packet for a `write-specs` run (see `references/spec-handoff.md`) — so it must already carry the facts a SPEC needs.

### Domain File Template

```markdown
# Domain: {Name}

## Current State
**Modules**: {list with file:line refs}
**Responsibility**: {one sentence}
**Depends on / depended on by**: {domains, with file:line refs}
**Data stores**: {tables/collections/SPs with refs}
**External integrations**: {APIs, queues, file shares — with refs}
**Parity surface**: {endpoints/screens/jobs that must behave identically — from research §1.5}

## Target State (.NET)
**Architecture**: {e.g., ASP.NET Core minimal API slice + Blazor WASM pages, or MAUI module}
**Projects**: {proposed .csproj layout — e.g., Domain, Application, Infrastructure, Api, UI}
**Key changes**: {what moves where}
**Security redesigns**: {items pulled from research/security-debt.md that touch this domain}

## Migration Steps
### Step 1: {action}
**Pattern**: {ref to strangler-fig-patterns.md}
**Seam**: {ref to Step 6}
**What changes**: {specific description}
**Files affected**: {file:line list}
**Testing / parity**: {strategy from testing-safety-nets.md — which suite type}
**Rollback**: {how to revert this step}
**Success criteria**: {measurable}

## Risks Specific to This Domain
| Risk | Impact | Mitigation | Evidence |

## Dependencies on Other Domains
**Must complete before**: {domain + reason}
**Blocks**: {domain + reason}

## SPEC Handoff Summary
**Proposed SPEC slug**: `{kebab-slug}`
**Proposed type**: `Feature | Refactor | Infra | API | Frontend`
**Scope statement**: {one paragraph, in-scope/out-of-scope seeds for write-specs}
```

### Writing Guidelines

- Self-contained enough that `write-specs` + an executing agent can work the domain without reading every other domain file.
- Keep each file under ~300 lines; split oversized domains.
- Every `file:line` must have been actually read during RESEARCH.
- Known-bug behaviors go in "parity surface" with an explicit `BUG — decide` marker, never silently ported.

## Step 8: Consolidated Roadmap

Write `migration-plan/00-roadmap.md` **in the target repo** (or the current directory in analysis-only mode):

```markdown
# Migration Roadmap

## Executive Summary
**Current state**: {1-2 sentences, with refs}
**Target state**: {1-2 sentences}
**Direction**: {Step 5} | **UI target**: {Step 5.2}
**Domains**: {count} | **Critical risks**: {top 3}

## Phase Sequence

### Phase 0: Safety Net + Baseline
**Goal**: characterization/parity tests + observability (`migration_path` tags) + security-debt prerequisites — before any migration.
**Details**: `testing-safety-nets.md`
**Success criteria**: {measurable — e.g., parity suite covering top 80% of critical endpoints}

### Phase N: {domain(s)}
**Domains**: {leaf nodes first}
**Why this order**: {dependency evidence}
**Plan files**: `domains/XX-domain-*.md`
**SPEC files**: `.specs/SPEC-*-{slug}.md` (filled during Phase 3 of the skill)
**Issue links**: {#refs after create-issues}
**Success criteria**: {measurable}

### Final Phase: Legacy Decommission
**Goal**: remove legacy paths after all domains run at 100% for ≥30 days.
**Rollback**: flags/routes preserved ≥60 days post-decommission.

## Cross-Domain Concerns
| Concern | Strategy | Reference |
| Shared DB tables | owner + API reads / dual-write | {domain file} |
| Auth/session bridge | OIDC bridge, shared cookie scheme, token translation | {research ref} |
| Observability | `migration_path: legacy|new` tagging, old-vs-new dashboards | {research ref} |

## Risk Summary
{top risks with cross-refs to domain mitigations}

## Open Questions
{unresolved items needing user input before execution}
```

## Step 9–12: Delivery (delegated)

PLAN ends at the roadmap. The next phases are **not** executed inline:

- **Phase 3 — SPECs**: invoke `write-specs` per domain using `references/spec-handoff.md`.
- **Phase 4 — GATE**: pt-BR summary + explicit `sim`.
- **Phase 5 — Issues**: `create-issues` Epic `migration-{YYYYMMDD}` + slice Issues ordered by roadmap phases.
- **Phase 6 — Handoff**: `orchestrator` executes the approved SPECs.

## Plan Completion Checklist

- [ ] Direction + UI target documented with evidence (or explicitly escalated to the user)
- [ ] Every seam identified with `file:line`; facade designed per seam
- [ ] Domain order derived from dependency analysis
- [ ] Every domain file complete: current state, target .NET state, steps, testing, rollback, success criteria, SPEC handoff summary
- [ ] Roadmap sequences all domains; cross-cutting concerns addressed (shared DB, auth bridge, observability)
- [ ] Security-debt items assigned to phases (never silently ported)
- [ ] Parity coverage exists for every item on the parity surface
- [ ] No unreferenced claims; open questions listed
- [ ] All technology recommendations verified via web search / Microsoft docs
