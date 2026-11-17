---
name: product-ux-audit
description: Read-only, multi-phase audit of product logic, UX heuristics, user journeys, edge cases, and architecture modularity. Use this skill when the user invokes /product-ux-audit, asks for a "product audit", "UX audit", "product logic audit", "usability check", a heuristic evaluation, a user-journey review, or an edge-case / happy-path-vs-exception-path analysis. Complements `forensic-audit` (security/architecture) — this skill focuses on product logic, UX quality, and user-facing flow consistency, not vulnerabilities. MANDATORY: never run on an entire repo in a single pass — scope each invocation to one user flow / module (use a task list to split large codebases).
---

# Skill: product-ux-audit

## Trigger

Use this skill when the user asks for:
- a product logic audit ("product logic audit", "business logic audit")
- a UX/heuristic evaluation ("UX audit", "usability review")
- user journey mapping or happy-path vs exception-path analysis
- edge-case / boundary-condition discovery for a flow or feature
- a codebase modularization / separation-of-concerns review (product-driven, not security)
- a lightweight "is this feature production-ready from a product POV" check

**STRICT READ-ONLY**: Never modify, refactor, or create files inside the project repository. Only write reports to the `_Reports` output folder. Do not run mutating commands, migrations, or scripts.

For security/auth/crypto/data-integrity audits, use `forensic-audit` instead. For pure code-quality/refactor reviews, use `code-review` or `simplify`.

---

## Mission

Produce a structured, evidence-based audit of how a product (or a specific feature/flow) behaves from the user's and business's perspective — independent of whether the code is "secure" or "clean". Goals:

- Map the actual user flow(s) as implemented (not as documented).
- Find business-logic gaps, contradictions, and missing rules.
- Evaluate UX against Nielsen's heuristics.
- Find dead ends, friction points, and missing recovery/error paths.
- Enumerate edge cases and boundary conditions per flow.
- Compare happy path vs exception paths for completeness.
- Check architecture for product-feature modularity (each feature owns its slice).
- Optionally benchmark against competitors/industry standards if the user supplies that context.

---

## Pre-flight

1. **Scope**: Ask (or infer from the request) which feature/flow/area is in scope. If unscoped and the user says "audit the product", scope to the most user-facing flows (auth, onboarding, core feature loop, billing/queue if present) — don't try to cover the entire app in one pass.
   For this monorepo, also record **which app(s)** each in-scope flow belongs to (`apps/web` client-facing, `apps/desktop` client, `apps/desktop-operator`, `apps/desktop-admin`). Carry this per-flow app/persona label through every phase — e.g. don't apply Phase 2's elderly-client accessibility lens (#11) to an `apps/desktop-operator`/`apps/desktop-admin` screen unless evidence suggests the same users use it.
2. **Resolve output path**: `$outDir = "$env:USERPROFILE\Desktop\_Reports\product-audit_$(Get-Date -Format 'yyyy-MM-dd_HHmm')"`. Create it; abort if it fails.
3. **Repo context** (embed in every report header): `git rev-parse --short HEAD`, `git branch --show-current`, `git status --short`.
4. **Directory/route snapshot** for the in-scope area — orient before opining:
   ```bash
   # Next.js 14 App Router pages/routes + Fastify API routes
   rg --files apps/web/src/app apps/api/src --glob "page.tsx" --glob "route.ts" --glob "*.ts"
   rg "app\.(get|post|put|delete|patch)|fastify\.(get|post|put|delete|patch)|export default function" --type ts --type tsx -l

   # Electron IPC bridges & SSE streams (apps/desktop*, apps/api)
   rg "ipcMain\.handle|ipcRenderer\.invoke|reply\.raw\.write|text/event-stream" --type ts -l
   ```
   Adjust globs to the project's actual structure (check `apps/*/src` layout first if unfamiliar).
   Use `Glob` to check whether each in-scope `page.tsx` has sibling `loading.tsx`/`error.tsx`/`not-found.tsx` (App Router convention for loading/error UI) — note absences for Phase 3.
5. **Quick signal scan** — fast candidates for Phases 1/3 before deep reading:
   ```bash
   # Stubs / unfinished logic
   rg "TODO|FIXME|not implemented|HACK" --type ts --type tsx

   # Silent failure / swallowed errors
   rg "catch\s*\(.*\)\s*\{\s*\}" --type ts --type tsx

   # Where error/loading states exist (and by omission, where they don't)
   rg "isLoading|isPending|isError|skeleton|Spinner" --type tsx -l
   rg "catch|onError|throw new Error" --type ts --type tsx -l

   # Duplicated validation (cross-check FE vs BE in Phase 5)
   rg "\.min\(|\.max\(|\.required\(|z\.string\(\)" --type ts --type tsx -l
   ```
6. **Read before writing**: read the relevant routes/pages/components/services for the scoped flow(s) before forming any opinion. Don't audit from memory or assumptions.

---

## Report Header Template

```md
# [Phase Title]
**Date**: YYYY-MM-DD HH:MM
**Repo**: [repo root path]
**Git HEAD**: [short hash] ([branch])
**Scope**: [feature/flow(s) under audit]
---
```

## Finding Format (Phases 1-3, 5)

```
[file:line or screen/step] SEVERITY — short title

**Observed**: what the code/UI actually does (cite file:line)
**Expected/Standard**: what product logic, heuristic, or convention implies
**User impact**: confusion, data loss, dead end, inconsistent state, etc.
**Fix direction**: concrete next step (no code unless trivial)
```

Severity: CRITICAL / HIGH / MEDIUM / LOW / NOTE. Severity reflects **user/business impact**, not exploitability.

### Actionable vs Not Actionable

A finding is **actionable** only if it has a concrete file:line / screen reference AND a specific, real consequence for a user or the business. Generic UX best-practice statements without a concrete anchor in this codebase are not findings — drop them or fold them into context for an actionable one.

- Actionable: `[CheckoutForm.tsx:142] MEDIUM — submit button stays enabled during pending request, allowing duplicate charges on double-click`
- Not actionable: "Consider adding more whitespace for better visual hierarchy" (no file:line, no concrete user consequence)

### Avoid

- Do not propose a redesign, new design system, or new framework/library — that's out of scope for an audit.
- Do not invent personas, competitors, or KPIs not evidenced by the code, copy, or supplied by the user.
- Do not pad phases with generic UX textbook statements ("ensure consistency", "improve feedback") — every claim needs a concrete anchor.
- Do not re-score a heuristic based on assumed intent ("they probably meant to add a spinner") — score what's actually there.

---

## Phase Discipline

- **Fresh pass per phase** — don't rely on prior-phase memory; re-read relevant files for each phase's specific lens.
- **Cross-phase dedup** — Phase 1 (logic) and Phase 3 (edge cases) often surface the same spot (e.g. "empty input not validated"). Ownership:
  - **Phase 1** owns findings about *missing/contradictory business rules* (what should happen, per spec/business sense).
  - **Phase 3** owns findings about *unhandled input/state permutations* (what happens when it's not handled, regardless of whether a rule exists).
  - If a finding fits both, record it fully in its owning phase and reference it by file:line from the other ("see Phase 1 finding at X — not re-litigated here").
- **Sequential phases** — Phase N+1 starts only after Phase N's deliverable is written and verified (see below).
- **Verify write**: after each phase, confirm the deliverable file exists and contains at least one substantive finding/table row (not just the header template). If a phase genuinely has zero findings, write an explicit "No findings — checked: [what was checked]" line rather than leaving a near-empty file.

---

## Phase 0 — Flow Map & Scope

**Role**: Senior Product Strategist + Solution Architect.

- Enumerate the screens/routes/API endpoints that make up each in-scope flow, end to end (entry → completion → all exits).
- Note personas/roles involved (e.g. CLIENT, OPERATOR, ADMIN) and which steps each can reach.
- Note external systems touched (payment, queue, notifications, telephony, etc.) per flow.

**Deliverable**: `$outDir\audit_0_flow-map.md` — table of flows, steps, files, roles, external deps.

---

## Phase 1 — Product Logic Audit

**Role**: Senior Product Strategist (prompt source: "Product Logic Audit").

For each in-scope flow, check:
- **Business logic gaps**: rules implied by the UI/copy but not enforced in code (or vice versa).
- **Contradictory rules**: two code paths or screens that disagree on the same rule (e.g. a limit enforced on one endpoint but not another, a status that two places compute differently).
- **User flow inconsistencies**: same action behaves differently depending on entry point.
- **Missing edge cases**: see Phase 3 for the dedicated pass, but flag any glaring ones here.

**Deliverable**: `$outDir\audit_1_product-logic.md` — findings in standard format, severity = Critical/High/Medium/Low.

---

## Phase 2 — Heuristic Evaluation (Nielsen's 10 + Accessibility)

**Role**: UX Expert.

For each in-scope screen/flow, score 1-10 against each heuristic and give 1-2 concrete improvements where score < 8:

1. Visibility of system status
2. Match between system and real world
3. User control and freedom
4. Consistency and standards
5. Error prevention
6. Recognition rather than recall
7. Flexibility and efficiency of use
8. Aesthetic and minimalist design
9. Help users recognize, diagnose, and recover from errors
10. Help and documentation
11. **Accessibility & cognitive load for the actual user base** — when the in-scope flow is client/family-facing (lower tech literacy, older users): are tap/click targets large enough, is contrast/font size sufficient (check Tailwind classes like `text-xs`, arbitrary `text-[Npx]`), and are destructive/irreversible actions (cancel session, delete account, end call) clearly confirmed rather than a single accidental tap? Skip this heuristic for operator/admin-only screens unless evidence suggests the same concern applies.

Base scores on actual component code/markup (loading states, error messages, confirmation dialogs, copy, Tailwind classes), not assumptions.

**Deliverable**: `$outDir\audit_2_heuristics.md` — per-screen table (heuristic × score × note) + summary of weakest 3 heuristics across the product.

---

## Phase 3 — Friction, Dead Ends & Edge Cases

**Role**: UX Forensic Analyst + QA Edge-Case Hunter.

For each in-scope flow:
- **Dead ends**: states with no visible next action (e.g. error screen with no retry/back, empty list with no CTA).
- **Friction points**: steps with unnecessary required fields, re-authentication, redundant confirmations, or unclear copy.
- **Missing recovery paths**: what happens on network failure, validation failure, partial completion, session expiry mid-flow?
- **Offline & reconnection UX (SSE/Electron-specific)**: for flows backed by SSE (e.g. `queue-sse.ts`), does the UI show a reconnecting/stale state when the connection drops, or does it silently show outdated data? For Electron apps, what happens when the app wakes from OS sleep — does it refetch/reconnect, or sit on a dead connection? Check whether the SSE handler registers `reply.raw.on('close', ...)` (or equivalent) to detect client disconnects, and whether the client's `EventSource`/SSE consumer has an `onerror`/reconnect path.
- **IPC failure handling (Electron-specific)**: when an `ipcRenderer.invoke` call fails or times out (e.g. RustDesk launch failure), does the renderer surface an error state, or does the UI hang in `isLoading`/spinner indefinitely? Also check the relevant `BrowserWindow`'s `webPreferences` for `contextIsolation: true` — if it's missing or `false`, flag it (note in summary that depth coverage belongs to `forensic-audit`, but a flow-breaking IPC bridge issue is in scope here).
- **Edge cases / boundary conditions**: empty inputs, max-length inputs, zero/negative/huge numbers, concurrent submissions, duplicate actions (double-click submit), timezone/locale edges, permission changes mid-session.
- **Happy path vs exception paths**: for each flow, list the happy path steps, then for each step list the exception paths and whether the UI/code handles them (cite file:line) or not.

**Deliverable**: `$outDir\audit_3_friction-edgecases.md` — pain-point map (prioritized) + edge-case matrix (scenario | handled? | file:line | severity) + happy/unhappy path table.

---

## Phase 4 — User Journey Map (optional, on request or for the primary flow)

**Role**: UX Researcher.

For the primary persona/goal in scope, produce:
1. **Journey overview**: persona, goal, timeline/stages.
2. **Stage breakdown**: actions, touchpoints (UI/API), thoughts/feelings (inferred from friction found in Phase 3), pain points, opportunities.
3. **Touchpoint analysis**: channels (web/desktop/email/push), effectiveness, gaps.
4. **Metrics**: what KPIs/events would reveal whether this journey works (note if instrumentation exists or is missing).

**Deliverable**: `$outDir\audit_4_journey-map.md`.

---

## Phase 5 — Architecture & Modularization (product-driven)

**Role**: Solution Architect (prompt source: "Architecture Review" + "Modularization").

This is **not** a security pass (see `forensic-audit` for that). Focus on whether the codebase structure matches product structure:

- Does each in-scope feature live in a cohesive module/folder, or is its logic scattered across unrelated directories?
- Cross-feature dependencies: does feature A reach directly into feature B's internals (services, types, DB models) instead of a shared/owned interface?
- **Monorepo boundaries**: are shared types, Prisma schema, and utilities isolated in `@imma-help/db` / `@imma-help/desktop-shared` and consumed via those packages — or does `apps/web`, `apps/api`, or an `apps/desktop*` app reach into another app's `src` directly, or duplicate DB/schema logic locally instead of importing the shared package?
- UI/logic/data separation: are business rules duplicated between frontend validation and backend validation (and do they agree — cross-check with Phase 1)?
- Single points of failure for the in-scope flow (one service/util that, if it fails, breaks multiple unrelated features)?
- Scalability/perf notes only as they affect **product behavior** (e.g. "list grows unbounded → UI will eventually paginate badly") — defer deep perf/security findings to `forensic-audit`.

**Deliverable**: `$outDir\audit_5_architecture.md` — module map (table: feature → primary files → cross-deps) + refactoring suggestions with rationale. Optional Mermaid diagram of flow/module boundaries.

---

## Phase 6 — Competitive / Industry Benchmark (optional)

Only run if the user provides competitor names, target industry, or specific standards to check against — do not invent competitors or fetch external data without being asked.

- Map in-scope features to the named competitors' known capabilities (as supplied by the user).
- Identify gaps and differentiators.
- If the user asks for positioning copy, write a short (3-paragraph) draft.

**Deliverable**: `$outDir\audit_6_benchmark.md`.

---

## Challenge Pass (before Final Deliverable)

Before writing the master summary, validate every CRITICAL/HIGH finding from Phases 1, 2, 3, and 5.

- If subagents are available: spawn one fresh `Agent` (subagent_type "claude", no shared context, read-only) per batch of findings. Give it only the finding text + repo path — not your reasoning. Ask it to verify each finding against the actual code/UI and answer for each: **Confirmed / Overstated (downgrade severity) / Not an issue (drop)**, with a one-line reason.
- If subagents are not available: re-read the cited file:line yourself with fresh eyes and apply the same three-way verdict.

For Phase 2 (heuristic scores) specifically, challenge any score that seems to assume unverified intent — re-derive the score strictly from what's in the code/markup.

Apply the verdicts (drop/downgrade/keep) before building the rollup table. Note in the master summary how many findings were dropped/downgraded and why — this is a signal of audit quality, not a failure.

---

## Final Deliverable

Write `$outDir\audit_master_summary.md`:

- Severity rollup table across Phases 1, 3, 5 (Critical/High/Medium/Low/Note counts)
- Top 5 product-logic issues (Phase 1)
- Weakest heuristics + worst screens (Phase 2)
- Top 5 friction/dead-end fixes (Phase 3)
- Architecture/modularity highlights (Phase 5)
- Recommended fix order (quick wins first, then structural)

```
| Phase                | CRITICAL | HIGH | MEDIUM | LOW | NOTE |
|----------------------|----------|------|--------|-----|------|
| 1 Product Logic      |        N |    N |      N |   N |    N |
| 3 Friction/Edgecases |        N |    N |      N |   N |    N |
| 5 Architecture       |        N |    N |      N |   N |    N |
| TOTAL                |        N |    N |      N |   N |    N |
```

### Consolidated FINAL report

After all phase files and the master summary are written, concatenate everything into one combined file: `$outDir\FINAL_product-audit_$(Get-Date -Format 'yyyy-MM-dd_HHmm').md`.

Order: `audit_master_summary.md` first, then `audit_0_flow-map.md`, `audit_1_product-logic.md`, `audit_2_heuristics.md`, `audit_3_friction-edgecases.md`, `audit_4_journey-map.md` (if produced), `audit_5_architecture.md`, `audit_6_benchmark.md` (if produced) — separate each section with a `---` and a `# <original filename>` heading so the source phase stays traceable. This single file is the primary artifact to hand to the user; the per-phase files remain for traceability/reference.

---

## Constraints

- **READ-ONLY** on project source. Zero writes inside the repository — reports only go to `$outDir` under `_Reports`.
- **Evidence-only**: every finding cites a file:line, screen name, or concrete code excerpt. No speculation framed as fact.
- **Timestamped output** — never overwrite previous runs.
- **Scope discipline**: don't silently expand scope to the whole app; if you think broader scope is warranted, say so in the summary instead of just doing it.
- **No overlap duplication with forensic-audit**: if a security/data-integrity issue surfaces, note it briefly with a pointer ("see forensic-audit for security depth") rather than producing a full security finding here.
- **Severity = user/business impact**, not exploitability or code elegance.
