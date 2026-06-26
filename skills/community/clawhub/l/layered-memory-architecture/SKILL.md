---
name: layered-memory-architecture
description: Build cheap, truthful long-term memory for agents with a layered architecture instead of a memory blob. Design, explain, audit, or improve a system that separates hot canon, durable topic doctrine, project-scoped working memory, episodic logs, and generated live summaries. Use when creating token-efficient agent memory, reducing memory bloat and context cost, comparing layered memory against generic persistent-memory systems, defining memory boundaries, improving retrieval trust, or migrating from blob memory to a layered model.
---

# Memory Architecture

Design memory as a system, not a bucket.

## Core stance
Optimize for:
1. truthful retrieval
2. low token cost
3. clear boundaries
4. maintainable long-horizon continuity
5. project isolation where needed

Do not default to "store more and search later." First decide what kind of memory something is.

## The five-layer model
Use these layers consistently:

1. **Hot canon**
   - Small, frequently loaded, cross-session truths.
   - Identity, preferences, standing doctrine, current priorities, compact cross-project lessons.
   - Keep it aggressively bounded.

2. **Durable topic doctrine**
   - Stable architecture notes, decisions, playbooks, operating rules, and domain context.
   - More detailed than hot canon, but still curated.

3. **Project-scoped working memory**
   - Raw or evolving material tied to one initiative.
   - Research notes, migration plans, transcripts, experiment outputs, snapshots.
   - Promote only distilled lessons upward.

4. **Episodic logs**
   - What happened today or in a specific work session.
   - Events, observations, intermediate findings, next steps.
   - Default landing zone for fresh information.

5. **Generated live summaries**
   - Rebuildable operator read models for current state.
   - Queue views, alerts, health snapshots, status summaries, compact log digests.
   - Treat as derived state, not durable canon.

## Memory classification rule
Before writing memory, classify the item:

- **Cross-cutting durable truth** → hot canon
- **Durable but detailed rule / doctrine / architecture** → topic doc
- **Project-bound raw or changing context** → project memory
- **Fresh event or observation** → episodic log
- **Current operational snapshot** → generated summary only

If uncertain, bias downward:
- daily/project first
- promote later
- avoid prematurely canonizing noise

## Promotion / demotion flow
Use this ladder:

- fresh event → episodic log or project artifact
- repeated / stable lesson → topic doc
- hottest compact cross-cutting truth → hot canon
- volatile state → generated summary
- stale bulky detail → keep in project/archive, not hot canon

## Truthfulness rules
Never let memory blur these categories:
- durable truth
- project-specific context
- current live status
- historical event log
- derived summary

Do not promote temporary red/yellow/green conditions, queue counts, disk snapshots, or stale alerts into canon unless they reveal a durable rule.

## Retrieval policy
Retrieve in this order:
1. hot canon
2. compact index/selector
3. relevant topic docs
4. project memory only if the task is project-specific
5. generated summaries before raw logs for live-state questions
6. raw logs only when summary is insufficient or needs verification
7. episodic logs only when recent event history matters

The goal is not maximum recall. The goal is the right recall.

## Comparison frame
When comparing layered memory against generic persistent-memory tools, use this lens:

### Generic persistent-memory systems usually optimize for:
- saving more facts
- retrieving facts later
- one-store convenience
- simple demo value

### Layered memory systems optimize for:
- memory boundaries
- retrieval trust
- token hygiene
- long-term maintainability
- project isolation
- separation of canon vs live state

Use this summary line:
- **"Persistent memory is a feature. Memory architecture is a system."**

If needed, read `references/scorecard.md` for a compact comparison rubric.

## Anti-patterns
Flag these quickly:
- one giant memory blob with weak boundaries
- logs and durable truths mixed together
- live status stored as long-term canon
- duplicated facts across layers without summary/detail distinction
- always-append workflows with no dedupe or demotion
- semantic search over stale and current facts without authority separation
- project details contaminating global memory

## Output patterns
For comparisons or teaching material, prefer one of these structures:
- **scorecard**: category-by-category ratings and winners
- **analogy**: bucket/backpack vs compartments/ship
- **thesis**: "remember more" vs "remember the right things in the right places"
- **migration plan**: how to move from blob memory to layered memory

## Use bundled references only when needed
- Read `references/scorecard.md` when preparing a digestible comparison, talk track, or publishable rubric.
- Read `references/migration-pattern.md` when helping someone convert an existing persistent-memory setup into a layered one.
- Read `references/layout-template.md` when the user wants a concrete starter structure for implementing layered memory in a workspace.
- Read `references/audit-checklist.md` when the user wants a repeatable audit of an existing memory setup instead of a high-level philosophy discussion.
- Read `references/classifier-pattern.md` when the user wants a lightweight routing rule for deciding where fresh information belongs.
- Read `references/promotion-trigger-pattern.md` when the user wants a safe promotion model for moving notes upward over time.
- Read `references/summary-generator-pattern.md` when the user wants live-state summaries that remain derived and rebuildable rather than polluting canon.

## Reliability rules
- Prefer the smallest useful memory change over a total rewrite.
- Do not invent hidden automation or magical persistence claims.
- Keep implementation recommendations explicit about which layer is authoritative.
- If offering migration advice, separate immediate low-risk fixes from optional later refinements.
- If the user wants operational memory, keep generated summaries distinct from canon.
- Treat lightweight automations as helpers that nominate or summarize, not as silent canon-writing authorities.

Keep the explanation compact unless the user explicitly wants a deep comparison.
