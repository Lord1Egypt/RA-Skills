---
name: harness-engineering
description: Evolve an existing repository toward Harness Engineering by making it more legible to agents, moving critical knowledge into repo-local artifacts, adding predictable structure, and replacing policy-only documentation with executable checks. Use when Codex is asked to audit a live codebase against Harness Engineering ideas, strengthen AGENTS.md and docs, add runnable governance and CI checks, or incrementally reduce hidden context and architectural drift without rewriting the project from scratch.
---

# Harness Engineering

Evolve an existing repository toward Harness Engineering without pretending it must be rebuilt as a blank template.
Prefer repo-local knowledge, predictable structure, and executable checks over aspirational documentation and hidden context.

## Workflow

### 1. Audit the current repo

- Read `AGENTS.md` and the top-level docs under `docs/`.
- Identify missing source-of-truth artifacts, dead references, placeholder CI, and stack-specific assumptions.
- Confirm whether the repo is a real app, a governance layer, or a starter template.
- Preserve existing product and runtime structure where possible. Do not force a greenfield layout onto a mature codebase.

### 2. Establish the minimum repo-local artifacts

- Keep `AGENTS.md` short and map-like.
- Add only the missing artifacts that materially improve agent legibility, such as:
  - `docs/ARCHITECTURE.md`
  - `docs/core-beliefs.md`
  - `docs/quality-score.md`
  - `docs/observability.md`
  - `docs/worktrees.md`
  - `docs/skills.md`
  - `docs/product-specs/index.md`
  - `docs/product-specs/template.md`
  - `docs/exec-plans/index.md`
  - `docs/exec-plans/template.md`
  - `docs/exec-plans/tech-debt-tracker.md`
  - `docs/generated/README.md`
- Match the artifact set to the repository's maturity. A small service may need fewer documents than a large multi-domain product.
- If generated artifacts are referenced but not yet produced, add explicit placeholders rather than leaving silent gaps.

### 3. Replace policy-only claims with enforcement

- Use the repo's existing stack where needed, but prefer `bun` for lightweight governance scripts when that does not conflict with the project.
- Add executable checks for required files, stale placeholders, broken references, and obvious contract drift.
- Wire CI to run the checks for every push and pull request.
- Do not leave comments like "run lint later" as the only quality gate.

### 4. Preserve generality

- Preserve real project names, domains, and runtime details when the repository is already in active use.
- Remove only accidental one-off assumptions, stale tribal knowledge, and undocumented conventions.
- Write docs so a future agent can continue work from the repository itself.
- Prefer incremental hardening over broad rewrites.

### 5. Make the repo legible to agents

- Keep one clear location for each category of knowledge.
- Put product intent in `docs/product-specs/`.
- Put multi-step delivery work in `docs/exec-plans/`.
- Put detailed external library notes in `docs/references/`.
- Prefer explicit directory conventions over clever local variation.

### 6. Verify the template

- Run `bun run template:check` or the project equivalent.
- Fix all hard failures before stopping.
- Treat warnings as backlog only if they are genuinely optional.
- If the repository is not a git checkout, note that you cannot report git status.

## Editing rules

- Use imperative language in docs.
- Prefer concise checklists over essays.
- Keep examples aligned with `bun`.
- Avoid claiming that a metric, score, or automation is "automatic" unless code actually updates it.
- Add placeholder files when the template references an artifact that new projects will generate later.

## Reference

Read [references/checklist.md](references/checklist.md) when you need a compact audit list while editing or reviewing a template repo.

## Deliverables

- Updated repo-local docs
- Missing placeholder artifacts filled in
- Executable validation or governance checks
- CI wired to run real checks
- A short summary of what now supports Harness Engineering and what still depends on hidden context
