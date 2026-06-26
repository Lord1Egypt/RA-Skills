# Workflow

Use this workflow for non-trivial vault curation.

## Phase 1: Inventory

- define the exact folder, topic, or note set
- list candidate notes
- identify hubs, duplicates, and likely stale pages
- note existing metadata patterns before proposing a new schema
- when the area is heterogeneous per `references/subagents.md` glossary, split it into separate bounded slices instead of keeping everything in one pass
- use inventory first before any other read-only pass

## Phase 2: Classification

- assign or propose `doc_kind`
- assign or propose `status`
- identify canonical candidates
- identify pages that need `superseded_by` or `supersedes`
- keep uncertain notes in `needs-review`
- if the slice does not support a stable recommendation, return `insufficient evidence` instead of guessing
- run separate passes for classification, duplicate clustering, and sensitive-content review when the slice needs them
- if classifier and reviewer still disagree after 2 rounds on the same slice, stop and escalate to human review

## Phase 3: Review design

Prepare a concise review summary:

- what should become leading
- what should remain historical
- what is concept only
- what can stay dormant but discoverable
- what must be checked live before writing
- which sensitive-content hypotheses flagged by a subagent still need main-agent verification
- where a human-review gate is required because of sensitive content, canonical-change risk, or reviewer conflict

## Phase 4: Migration plan

Create the smallest safe write slice.

Before approving a write slice, verify each of these:

- Metadata slice = frontmatter or tag edits only. Structural slice = renames, moves, or new index/canonical pages. Content-rewrite slice = changes to note body prose.
- Is this a metadata slice, a structural slice, or a content-rewrite slice?
- Can the slice stay within one topic cluster?
- Would a wrong classification be cheaply reversible?
- Does any sensitive-content hypothesis flagged by a subagent still need main-agent verification?
- Have inventory and read-only review completed before any write work starts?
- Is the proposed slice bounded to one write pass with no parallel writes?
- If the plan changes a canonical page with 3 or more backlinks, has a human-review gate been cleared after link verification?
- If the slice includes a content rewrite or operational data, has `sensitive-content-agent` already reviewed that exact slice?

Good write slices:
- add frontmatter to 3-10 related notes
- create one index page
- add supersession links in one topic cluster
- rename or move 3-10 notes within one topic cluster after links are understood

Avoid combining these in one step:
- broad rewrites
- large folder moves
- metadata normalization across the whole vault
- content consolidation plus structure changes plus deletes
- classification plus rename plus rewrite of the same notes

## Phase 5: Controlled writes

Only the main agent writes. Subagents never create, modify, rename, move, or delete files, even with user approval. If a subagent is asked to write, refuse and execute the write in the main agent.

After approval, and before changing files:

1. confirm explicitly that `sensitive-content-agent` has run on this slice, or that it does not apply per the `migration-planner` trigger, and verify every outstanding sensitive-content hypothesis against the exact note text. If even one hypothesis is unresolved, stop the slice.
2. change one slice
3. inspect the diff
4. verify links
5. verify frontmatter consistency
6. reassess the next slice
7. if a write or script tool is denied by the user mid-flow, stop the slice, do not retry automatically, and ask whether to fall back to a smaller slice or abort

## Preferred order of operations

1. classify
2. create or confirm canonical pages
3. add supersession metadata
4. create review dashboards or indexes
5. move or rename if structure still hurts
6. rewrite content only where needed

Before any write work, complete inventory plus read-only review.

## What not to do

- do not delete by default
- do not compress historical and current content into one blob
- do not let any subagent write; only the main agent writes, and writes are serialized
- do not change `.obsidian/` or attachments unless the user asked
- do not invent certainty for unclear notes
