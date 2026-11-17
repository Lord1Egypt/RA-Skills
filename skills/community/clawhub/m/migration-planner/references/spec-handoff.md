# SPEC Handoff — Domain Plan → SPECs → Issues → Orchestrator

The contract between `migration-planner` and the delivery pipeline. The planner stops at plans; this file defines how plans become executable work without bypassing each skill's own guardrails.

All delivery artifacts land in the **target repo**: `migration-plan/` outputs, `.specs/SPEC-*.md` files, and the GitHub Epic/slice Issues. The temp clone of the source repo is read-only evidence — it never receives artifacts. In analysis-only mode (no target repo yet), stop after PLAN and ask the user for the target repo before Phase 3.

## Phase 3 — One SPEC per Domain via write-specs

For each `migration-plan/domains/XX-domain-{name}.md`, invoke `write-specs` **per its own contract** — do not fill the SPEC template yourself. Hand it an evidence packet so its interview starts informed instead of blank:

```markdown
## Handoff Packet for write-specs
- Source plan: `migration-plan/domains/XX-domain-{name}.md`
- Proposed slug: `{kebab-slug}` (from the domain file's SPEC Handoff Summary)
- Proposed type: `Feature | Refactor | API | Infra | Frontend`
- Scope seed: in-scope/out-of-scope from the domain file
- Parity surface: behaviors that must be preserved (list)
- Testing strategy: safety-net selections (parity, contract, golden master)
- Rollback: per-step mechanism
- Risks/security-debt items touching this domain
- Dependencies: domains that must complete first (blocks → SPEC dependency notes)
```

`write-specs` runs its own pt-BR design-tree interview — answer from the domain file when possible and let it ask the user only what the plan did not settle. Output: `.specs/SPEC-{YYYYMMDD}-{slug}.md` in `Draft`, with the domain plan path referenced in metadata/context.

Rules:

- One SPEC per bounded context. If a domain file is too big for one SPEC, split the domain first — never merge domains into one SPEC.
- Do not weaken the domain file's evidence when translating: `file:line` refs and parity requirements must survive into the SPEC.
- `Status` stays `Draft` until the user approves (next phase).

## Phase 4 — Approval Gate

After all Draft SPECs exist, present the pt-BR summary and STOP:

```text
Plano de migração concluído.
- Domínios mapeados: [N] | SPECs Draft gerados: [lista]
- Roadmap: migration-plan/00-roadmap.md
- Principais riscos: [top 3]

Aprovar os SPECs e criar o Epic + Issues no GitHub? (sim/não)
```

No Issue, branch, commit, push, or spec execution before explicit `sim`. On `não`, keep everything as Draft and ask what to adjust.

## Phase 5 — Issues via create-issues

After approval (invoke `create-issues` per its contract and Label Contract):

1. **Epic Issue** `migration-{YYYYMMDD}` — labels `epic` + `todo` — summarizing direction, target stack, domain list, roadmap phases, and top risks; links to `migration-plan/00-roadmap.md`.
2. **Slice Issues** — one per approved domain SPEC — labels `slice` + `todo`; each links the Epic and its `.specs/` path; cross-dependencies via `Blocked by #<n>` reflecting the roadmap order (leaf domains unblocked, core/shared domains blocked by their prerequisites).
3. Existing equivalent Issue → link it, never duplicate. Sync `backlog`/`todo` per the Label Contract.
4. Update each SPEC's `Ticket` field and the roadmap's `Issue links` with real numbers/URLs.

If `gh` is unavailable/unauthenticated: report it, keep SPECs Approved locally, and skip to Phase 7 without blocking.

## Phase 6 — Handoff to orchestrator

Only when every approved SPEC has an Issue (or valid link):

1. Verify: clean working tree, branch policy allows work, every SPEC `Status: Approved`, dependency order matches the roadmap.
2. Invoke `orchestrator` per its contract — it runs its own Phase 4–5 loop (implementation via `execute-specs`/`tdd-spec`, tests, review, QA).
3. Remind the orchestrator that migration SPECs carry parity requirements: the safety-net tests in each SPEC are part of the DoD, not optional.

The orchestrator executes ALL approved SPECs — including any pre-existing ones — this is by design.

## Phase 7 — Run State

Write `.claude/memory/migration-planner-{YYYYMMDD}.md`:

```markdown
# Migration Planner Run — {YYYYMMDD}
- Repo / branch: {…}
- Direction: {…} | UI target: {…}
- Research: migration-plan/research/* (complete)
- Domains: [domain → spec path → issue #]
- Epic: #{n}
- Gate result: approved {date} | pending
- Open pendencies: {list}
```

Re-runs read this file first: a domain already mapped to a SPEC or Issue is `DUPLICADO` — link it, never replan or recreate.
