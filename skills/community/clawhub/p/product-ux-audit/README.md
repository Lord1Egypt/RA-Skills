<p align="center">
  <img src="images/logo.png" alt="Product UX Audit Logo" width="200" />
</p>

# Product UX Audit Skill

A read-only, multi-phase audit protocol for AI coding assistants (Claude Code, Antigravity, and compatible agents). Performs a systematic, evidence-based audit of a product's business logic, user journeys, UX heuristics, edge cases, and feature modularity.

Developed against a Turborepo monorepo stack (Next.js App Router, Fastify, Electron, Prisma/PostgreSQL). Stack-specific patterns are marked and can be adapted for other architectures.

## What It Does

Seven sequential phases:

* **Phase 0: Flow Map & Scope** — Maps all screens, routes, APIs, user roles (personas), and external system dependencies.
* **Phase 1: Product Logic Audit** — Logic gaps, contradictory rules between endpoints/views, inconsistencies in user flows.
* **Phase 2: Heuristic Evaluation** — Nielsen's 10 usability heuristics + accessibility and cognitive load for non-technical users.
* **Phase 3: Friction, Dead Ends & Edge Cases** — Dead-end states, UX friction, network/SSE disconnection recovery, unhandled edge cases.
* **Phase 4: User Journey Map** — Primary user journey, touchpoints, feelings, pain points, and product metrics.
* **Phase 5: Architecture & Modularization** — Monorepo boundaries, feature encapsulation, type sharing, frontend/backend validation sync.
* **Phase 6: Competitive Benchmark** — Product evaluation against user-specified competitors.

---

## How to Use

1. **Install:** Save `SKILL.md` into `~/.claude/skills/product-ux-audit/SKILL.md`. Restart your agent session — the skill becomes available as `/product-ux-audit`.
2. **Invoke with a defined scope:** One user flow at a time — e.g. `/product-ux-audit. Scope: auth-onboarding. Files: src/app/(auth)/*, src/api/auth.ts`. See Scope Discipline in SKILL.md — never point it at an entire repository in one pass.
3. **Read the report:** Phase reports plus a final summary are written to `%USERPROFILE%\Desktop\_Reports\<timestamp>\` (Windows) or `~/Desktop/_Reports/<timestamp>/` (Linux/macOS) — never inside the project repository.
4. **Auditing a whole product?** See the pipeline section below — generate a task list first, then run it one scope at a time.

---

## Orchestrating a Large-Scale Audit (Multi-Agent Pipeline)

Passing an entire repository to a single agent session causes context overload, shallow findings, and high hallucination rates. The template in [tasks-pipeline-example.md](./tasks-pipeline-example.md) implements a multi-agent pipeline with dual independent runs per scope.

1. Ask the agent to scan the project and generate a task list partitioned by user flow or module boundary.
2. Launch all `runA`/`runB` subagents concurrently in a single batch.
3. Merge each scope pair yourself as they complete (no subagent for merge).
4. Consolidate to `AUDIT_FINAL.md` with cross-scope deduplication, sorted CRITICAL → LOW.

---

## Default Technology Stack

`SKILL.md` search patterns target:
* **Frontend:** Next.js (App Router/Vite), React, TailwindCSS.
* **Backend:** Fastify API, Server-Sent Events (SSE).
* **Database & ORM:** Prisma ORM, PostgreSQL.
* **Desktop Client:** Electron IPC bridges (`ipcMain`, `ipcRenderer`).

## Custom Stack Adaptation

Replace framework-specific patterns in `SKILL.md`:
1. **Search queries:** Update directory structures (e.g. `templates/` or `controllers/` instead of Next.js App Router).
2. **Framework rules:** Replace React hooks/state indicators (`isLoading`, `isPending`) with your frontend framework's equivalents.
3. **ORM queries:** Replace Prisma methods (`prisma.findMany()`) with Sequelize `.findAll()`, Django `.objects.all()`, etc.

## Known Limitations

- This is a code-level UX and product logic audit — it cannot observe actual user behavior, session recordings, or A/B test data. Pair with real user research for product decisions.
- Phase 6 (Competitive Benchmark) depends on the agent's training data knowledge of competitors — verify claims against current product state.
- Findings are scoped to one flow per invocation by design. Cross-flow inconsistencies are only caught if both flows are audited and compared manually.
- Severity reflects user impact and product risk, not security exploitability. For security depth, use `forensic-audit`.
- Stack-specific search patterns (Prisma, Fastify, Electron) may not match other architectures — adapt before running on a different stack.
