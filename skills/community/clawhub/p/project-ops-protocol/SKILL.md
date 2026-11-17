---
name: project-ops-protocol
description: >-
  A lightweight operating protocol for running serious projects across multiple
  AI sessions/agents and humans: layered battle map, three ledgers of record,
  an append-only alignment board with milestone heartbeats, a relay note for
  cross-session handover, plus quality-judge gates before any external publish.
  Triggers: start a new project, multi-session collaboration, project ops,
  mechanism/handbook, alignment, wrap-up, retrospective, operating model.
version: 1.0.1
license: CC BY-4.0
author: Zhao Xinghua (Steven Zhao)
homepage: https://github.com/zhaoxinghua09-cell/project-ops-protocol
keywords: [ai-agents, multi-agent, project-management, llm, workflow, governance, operating-procedure]
x-theory: LGD (Lifecycle Governance Doctrine) — registry/evidence/gates; concept DOI https://doi.org/10.5281/zenodo.22456647
---

![lgd-powered-en](https://raw.githubusercontent.com/zhaoxinghua09-cell/lgd-theory/main/assets/badges/powered/lgd-powered-en.svg)

# Project Ops Protocol (POP)

Proven on a long-running multi-session project: 100+ docs, 50+ tools, several
parallel AI sessions and one human decision-maker — without losing state,
duplicating work, or colliding. Everything below is copy-paste-able into any
new project. It is a method, not a company secret.

## When to use
- You are starting a real project that will span many sessions/agents/days.
- Several AI sessions (or people) work the same project in parallel.
- Someone asks "how do we organize / what's the mechanism / do a retrospective".
- Skip it for one-off questions and single-tool jobs.

## Core idea: four layers
```
Plan     layered battle map: Stand → Build → Distribute; each layer closes
         before the next opens; an honest "watchlist" for what we deliberately
         do NOT do now (with a review cadence).
Execute  measure first, reuse before build, converge over duplicate;
         statuses change only after they actually happen.
Sync     one append-only alignment board + milestone heartbeats + @channel tags.
Memory   one relay note (read first by any new session) + a living handbook
         where process changes land BEFORE they are announced.
```

## Standard artifacts (build once, reuse always)
| Artifact | Job | Write rule |
|---|---|---|
| Battle map | layers, milestones, watchlist | close a layer before opening the next |
| Release ledger | channel/publish status = source of truth | change only on real events; URLs clickable |
| Domain/topic ledger | stable IDs per deliverable | create once, never renumber |
| Alignment board | cross-session heartbeat | append-only; one line per completed deliverable |
| Relay note | cross-session memory | update at every wrap-up |
| Retrospective | facts + mechanism + traps + take-aways | mandatory at project close |
| Handbook | rules live here | change the handbook FIRST, then announce |

## Hard rules (the cards that prevent the common failure modes)
1. Heartbeat: within 5 minutes of finishing a deliverable, +1 line on the
   alignment board (`time | line | did what | path/url`). No polling loops;
   to request something from another line, tag it on the board.
2. No-collision: before starting work, read the division of labour + the tail
   of the alignment board. Reuse before rebuild: scan existing assets first.
3. Unique anchors: when editing shared files, match on a unique string and
   re-check neighbouring lines after saving (prevents silent overwrites).
4. Measure first: plan conclusions come from actual inventory (counts/APIs),
   never from vibes.
5. Honest watchlist: what we are NOT doing goes on the watchlist with a review
   date — it never becomes a zombie todo.
6. Secrets: a local encrypted credential store only; secrets never in chat,
   commands, screenshots, or shared plaintext folders. Inject into processes
   via environment, echo nothing.
7. Gate before external publish: desensitize scan → quality judge (5 dims,
   ≥0.80 pass, any 0.0 vetoes) → safe packaging → owner approval.
8. Process changes land in the handbook before being announced anywhere else.

## Quality judge (LLM-as-judge rubric)
Score each deliverable 0.0–1.0 per dimension; pass ≥0.80; any 0.0 = veto:
1. Factual accuracy — every claim traces to a source?
2. Citation accuracy — sources actually support the claims?
3. Completeness — conclusions, boundaries, attribution, license all present?
4. Source quality — primary/official preferred over secondary retells?
5. Discipline — no internal names, secrets, local paths, or private strategy
   words in anything going outside?
Quick 30-second self-check: (a) can each claim be pointed to a source?
(b) am I citing the primary source, not a retell? (c) would this leak anything
internal if it went public?

## New-project checklist (day 1)
- [ ] battle map v0.1 (layers + milestones + watchlist)
- [ ] three ledgers identified/created
- [ ] alignment board created + heartbeat rule announced (multi-session only)
- [ ] existing assets scanned (no rebuilding what exists)
- [ ] roles/boundaries written down where everyone can see

## Wrap-up checklist (project or big day ends)
- [ ] layer close-out checked, including watchlist explanation
- [ ] retrospective written (data / mechanism / traps / take-aways)
- [ ] relay note updated (single place every new session reads first)
- [ ] open items listed explicitly (≠ failure — honesty is the standard)

## Boundaries & philosophy
- Markdown + filesystem is enough until retrieval actually degrades; do not
  front-load vector DBs / knowledge graphs / event buses (benchmarks show plain
  files beat specialised memory tools when retrieval is reliable).
- Handbook-first (borrowed from GitLab), orchestrator-worker + compressed
  reports back (borrowed from Anthropic multi-agent research), judge-gated
  publishing. All ideas are credited to their sources — copy what works.

© 2026 Zhao Xinghua (Steven Zhao) — CC BY 4.0 · MedXpert × SynomosAI
