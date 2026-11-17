<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Element Comparators — Per-Type Drift Detection Strategies

## Purpose

Defines HOW AI-GCE measures each **governed-element type** against reality. Every element type declared in the DWG baseline has a specific detection strategy: where to look, what to compare, and what counts as divergence. This is the step-2 body of the detection algorithm (`drift/drift-detection-engine.md`).

**Grounding:** Implements `MIDFLIGHT_DRIFT_GOVERNANCE_DESIGN.md` §15.

---

## MANDATORY: Stage Sub-Role — Audit Specialist + Systems Engineer

Audit Specialist (evidence) + Systems Engineer (structural comparison). ADDS a dimension.

### Anti-Patterns
- Do NOT report style preferences as divergence unless the element declares them
- Do NOT guess when the reality artifact is missing — flag "artifact not found" as evidence, not silent pass
- Do NOT hardcode source paths — resolve via `element.source` + manifest `paths`

---

## Comparator Table

Each governed element carries a `type`. The comparator maps type → detection strategy.

| Element Type | Locate (reality artifact) | Compare | Divergence = |
|-------------|---------------------------|---------|--------------|
| `component-boundary` | `paths.src` directory tree + import graph | Declared modules/dirs exist? Imports respect boundaries? | Missing module, or cross-boundary import |
| `technology-choice` | `package.json` / `pom.xml` / `pyproject.toml` / `Cargo.toml` / `go.mod` | Declared language/framework/runtime present? | Undeclared tech present, or declared tech absent |
| `api-contract` | Route defs / OpenAPI spec / handler signatures | Endpoints match declared contract? Versioning scheme? | Contract mismatch (e.g., header vs URI versioning) |
| `data-model` | Schema files / migrations / ORM entities | Schema matches declared model? | Undeclared tables/fields, or missing declared ones |
| `design-token` | CSS/SCSS vars / design-token JSON / theme files | Token names/values match declared taxonomy? | Off-taxonomy tokens, missing tokens |
| `acceptance-criteria` | Spec/story status + implementation evidence + tests | AC claims match test results? Implementation covers AC? | AC marked done but test fails; behavior missing |
| `naming-convention` | AST/grep scan of source | Identifiers follow declared convention? | Convention violations (advisory by default) |
| `security-pattern` | Auth middleware / token handling / RBAC config | Implementation matches declared strategy? | Missing auth, wrong token strategy, weak crypto |
| `infrastructure` | CI/CD config / IaC / container defs | Infra matches declared architecture? | Undeclared infra, missing declared pipeline stage |
| `nfr-threshold` | Perf configs / load-test results / SLA defs | Thresholds respect declared NFR bounds? | Measured value breaches declared threshold |

---

## Comparator Detail (Per Type)

### component-boundary
- **Locate:** scan `paths.src` for module folders declared in `architecture/` (C4 L3).
- **Compare:** (a) each declared module folder exists; (b) build the import graph — no import crosses a declared boundary illegally.
- **Evidence on drift:** "`src/payments/` imports from `src/orders/internal/` — crosses declared boundary (ARCH-001)."

### technology-choice
- **Locate:** the manifest/lockfile for the declared stack.
- **Compare:** declared deps present; no undeclared framework introduced (e.g., baseline says REST/Express, reality adds GraphQL/Apollo).
- **Evidence:** "`package.json` adds `@apollo/server`; baseline ARCH-002 declares REST/Express. Undeclared tech."

### api-contract
- **Locate:** route files, OpenAPI/Swagger, or handler signatures.
- **Compare:** endpoint shape, versioning scheme, error format vs declared contract.
- **Evidence:** "`src/api/routes.ts` uses header-based versioning; baseline ARCH-003 declares URI-path versioning."

### data-model
- **Locate:** schema/migration/ORM files.
- **Compare:** tables/fields/relationships vs declared model.
- **Evidence:** "Migration adds `users.ssn` column; not in declared data model DATA-001 (also a security concern)."

### design-token
- **Locate:** token files / CSS vars / theme config.
- **Compare:** token names + values vs declared taxonomy.
- **Evidence:** "`theme.css` defines `--color-brand-hot-pink`; not in design-token taxonomy UX-001."

### acceptance-criteria
- **Locate:** story/spec status (from `paths.backlog`) + implementation + test results (TGE correlation if available).
- **Compare:** does implementation cover the AC? Does test evidence support a "done" claim? Uses `storyStyle` (EARS/G-W-T) to parse ACs.
- **Evidence:** "PROD-001 AC-003 requires 2FA; `src/auth/login.ts` has no 2FA path. AC unmet."

### security-pattern
- **Locate:** auth middleware, token handling, RBAC/ABAC config.
- **Compare:** implementation vs declared security strategy.
- **Evidence:** "Endpoint `/admin/*` lacks authorization check; baseline SEC-001 requires RBAC on admin routes."

### infrastructure
- **Locate:** CI/CD config, IaC, container defs.
- **Compare:** infra vs declared architecture (deployment method, pipeline stages).
- **Evidence:** "CI pipeline missing the security-scan stage declared in INFRA-002."

### nfr-threshold
- **Locate:** perf configs, load-test results, SLA definitions.
- **Compare:** measured/configured values vs declared NFR bounds.
- **Evidence:** "Load test p95 = 480ms; baseline NFR-001 declares p95 < 200ms. Breach."

### naming-convention (advisory by default)
- **Locate:** AST/grep of source.
- **Compare:** identifier casing/patterns vs declared convention.
- **Evidence:** "3 functions in `helpers.ts` use snake_case; ADV-001 declares camelCase." (advisory — informs, never blocks)

---

## Comparator Rules

1. **Evidence is mandatory.** Every reported drift carries concrete evidence (file + what diverged). No evidence → no drift entry.
2. **Artifact-not-found is evidence, not a pass.** If the reality artifact for a governed element is missing, that's a HARD divergence ("expected artifact absent"), not a silent skip.
3. **Tech-stack-derived, not generic.** Locate strategies use the actual stack from the manifest — never assume file patterns.
4. **Advisory types never block.** `naming-convention` and other `locked: false` elements inform only.
5. **TGE correlation (when available).** For `acceptance-criteria`, cross-reference TGE test results as additional evidence (see Phase P8 correlation).

---

## Extensibility

New element types (from future ADLC extensions or custom governed elements) add a row here + a locate/compare strategy. The engine (`drift-detection-engine.md`) calls the comparator generically by `element.type`.

---

## Interaction with Other Files

| Related | Relationship |
|---------|--------------|
| `drift/drift-detection-engine.md` | Calls these comparators in step 2 of the algorithm |
| `drift/drift-register.md` | Evidence strings populate the register `evidence` field |
| (DWG `baseline/baseline-generation.md`) | Declares the element types + sources these comparators consume |

---

## Output Validation

- [ ] Every baseline element type has a comparator strategy
- [ ] Locate strategies resolve via `element.source` + manifest `paths` (no hardcoding)
- [ ] Every reported drift carries concrete evidence
- [ ] Artifact-not-found treated as HARD divergence, not silent pass
- [ ] Advisory types produce informational entries only
- [ ] `acceptance-criteria` uses `storyStyle` to parse ACs; correlates TGE results when available
