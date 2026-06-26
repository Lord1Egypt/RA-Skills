# Subagent model

Use subagents to increase coverage and reduce context pressure.

The main agent stays in control and remains the sole writer.
Use agent-as-tool / orchestrator-worker mode only.
Do not use handoffs.
Subagents never create, modify, rename, move, or delete files, even with user approval.
Do not define a global forced model for all subagents; reuse the main model when it fits and change it only when a role clearly benefits.

## Glossary

- **Sensitive content**: any secrets, credentials, API tokens, private keys, PII, or internal-only identifiers. PII includes names, email addresses, phone numbers, physical addresses, and government IDs. Internal-only identifiers include live hostnames, IP addresses, service-account names, internal URLs, API endpoints, and deployment-specific IDs.
- **Operational data**: anything that describes a live or recently-live system, including hostnames, paths, container names, configuration values, account names, API endpoints, deployment notes, and backup or restore details.
- **Precedence rule**: any item that satisfies the `Sensitive content` definition is treated as sensitive content first, regardless of whether it also satisfies `Operational data`. `Operational data` is the broader bucket that triggers `sensitive-content-agent` review during migration; sensitive-content findings additionally require redaction and main-agent exact-text verification before any escalation or write.
- **Heterogeneous slice**: a slice that matches any of these: spans more than one topic cluster; mixes more than two `doc_kind` values; mixes `current` and `historical` notes that may need different reviewers; mixes operational data with conceptual material. If a slice is heterogeneous, split it into separate single-aspect passes.
- **Folder root**: a top-level directory of the vault; specifically, a direct child of the vault root.
- **Canonical change**: any rename of a `canonical: true` note, move of a `canonical: true` note across folders, status flip of a `canonical: true` note away from `current`, setting `superseded_by` on a `canonical: true` note, or deleting a `canonical: true` note.
- **Affected backlinks**: the count of wikilinks pointing at the canonical note, counted by `scripts/check_links.py` when available or by direct wikilink inspection when the script cannot run.

## Context control principle

- give each subagent one bounded slice only
- read-only slices must stay within 200 notes per subagent call; if a folder or queue exceeds 200 notes, split it into multiple bounded slices and run separate `inventory-agent` passes
- bounded slice defaults:
  - `inventory-agent`: one parent folder, one topic queue, or one explicit note set, capped at 200 notes
  - `duplicate-cluster-agent`: one candidate cluster or one 3-10 note comparison set
  - `classifier-agent`: one 3-10 note topic cluster
  - `curation-reviewer`: the same 3-10 note slice reviewed by `classifier-agent`
  - `link-verifier`: one proposed write slice plus directly affected link targets, capped at 200 notes total per call. If directly affected backlinks exceed 200, split the `link-verifier` pass by topic or by source folder.
  - `migration-planner`: one proposed 3-10 note write slice only
  - `sensitive-content-agent`: one parent slice capped at 200 notes per call, or one planned 3-10 note write slice. If the relevant area exceeds 200 notes, split into multiple `sensitive-content-agent` passes.
- split heterogeneous material into separate passes per the glossary definition
- prefer folder, topic, or queue scoped slices over broad vault dumps
- keep the main agent as the only place where cross-slice decisions are merged
- if two slices might conflict, review them serially in the main agent
- never let the main agent hold multiple large slices when subagents can inspect them separately
- do not use facts outside the assigned bounded slice unless the main agent explicitly includes them in the packet
- treat sensitive findings as provisional until the main agent reads the exact source note
- never start write work before inventory plus read-only review are complete
- if evidence is insufficient, say `insufficient evidence` and downgrade the note or slice to `needs-review` instead of guessing

## Safe roles

Each role's `Required content elements:` describes what must appear inside the shape from `references/output-format.md`. It never replaces that shape.

### `inventory-agent`
Objective: enumerate notes, folders, shallow duplicates, missing metadata, and structural clusters.

Use this role when: the task spans more than one note, more than one folder, or any area that needs a first-pass map before deeper review.

Do not use this role when: the task is already limited to one known note or one already-verified 3-10 note slice.

Required content elements: counts, folder map, missing-frontmatter lists, title-duplicate groups, shallow duplicate candidates, and "needs deeper look" referrals.

Tool and source guidance: read-only filesystem inspection only; use inventory heuristics and broad scanning before deeper passes.

Boundaries: does not classify, does not compare content deeply, does not propose writes.

Failure modes: over-counting near-duplicates from filename similarity; returning raw file lists instead of a distilled summary.

### `duplicate-cluster-agent`
Objective: find content-based near-duplicates and semantically overlapping notes that shallow inventory cannot see.

Use this role when: `inventory-agent` reports duplicate candidates, multiple notes appear to cover the same topic, or the main agent sees draft/fork/overlap risk inside one 3-10 note slice.

Do not skip this role when: duplicate or overlap risk exists and `classifier-agent` has not yet seen a duplicate-cluster result for the slice.

Do not use this role when: the task is simple metadata completion, the notes are clearly unrelated, or shallow duplicate detection is already sufficient.

Required content elements: cluster groups with members, similarity rationale, cluster type (`near-duplicate`, `fork-of`, `draft-of`, `topic-overlap`, `coincidental-match`), and a canonical-candidate hypothesis.

Tool and source guidance: read only the bounded slice assigned by the main agent; compare body content and structure, not just filenames.

Boundaries: no merging, no deletion, no writing, no `superseded_by` decisions.

Failure modes: false positives from boilerplate/frontmatter, false negatives on conceptually similar but text-divergent notes.

### `classifier-agent`
Objective: propose `status`, `doc_kind`, `topic`, canonical candidates, and ambiguity flags for one bounded slice.

Use this role when: inventory is complete and one 3-10 note slice now needs classification.

Do not use this role when: inventory is still incomplete, duplicate/overlap risk has not been checked by `duplicate-cluster-agent`, sensitive exact-text verification is still pending, or the slice still mixes unrelated topics.

Required content elements: per-note recommendations with confidence and explicit uncertainty.

Tool and source guidance: use the inventory summary plus the classification rubric; stay within the bounded slice.

Boundaries: suggests only, never writes, never resolves conflicts by force.

Failure modes: conflating `status` and `doc_kind`; forcing a label on an ambiguous note instead of marking it `needs-review`.

### `curation-reviewer`
Objective: challenge classifier output, find contradictions, and surface counterexamples.

Use this role when: `classifier-agent` has finished a slice and a read-only challenge pass is required before any structural or content write planning.

Do not use this role when: no classifier output exists yet or the slice still needs inventory cleanup first.

Required content elements: per-note `pass` / `revise` / `escalate-to-human`.

Tool and source guidance: review the proposed classifications and canonical candidates for the same bounded slice.

Boundaries: critique-only; do not introduce new classifications as final answers.

Failure modes: reviewer-classifier collusion or shallow agreement that hides unresolved ambiguity.

### `link-verifier`
Objective: check wikilinks, backlinks, embedded transclusions, and Dataview/Bases query bodies before and after a write slice.

Use this role when: a rename, move, canonical switch, supersession update, or index change is proposed or has just been applied.

Do not use this role when: no link-affecting write is proposed and the task is classification-only.

Required content elements: pre/post diff, new orphans, broken links, and redirect or `superseded_by` suggestions.

Tool and source guidance: inspect only the affected slice and directly related link targets.

Boundaries: reports breakage only; never repairs it.

Failure modes: missing query bodies or treating slice-local checks as vault-global proof.

### `migration-planner`
Objective: propose the next write slice as a structured plan only.

Use this role when all are true: (1) inventory is complete, (2) `classifier-agent` has run on this slice, (3) `curation-reviewer` returned `pass` for every note in the slice; if any note returned `revise` or `escalate-to-human`, drop that note from the slice or return `insufficient evidence` for the whole slice, (4) if the slice includes content rewrite or operational data, `sensitive-content-agent` has run, (5) if the slice changes a canonical page with 3 or more affected backlinks, `link-verifier` has run, and (6) the main agent is ready to choose one 3-10 note write slice.

Do not use this role when: inventory is incomplete, reviewer disagreement is unresolved, any contested note remains in the slice, or the proposal would mix multiple write slices. If any contested note remains, return `insufficient evidence` instead of a write plan.

Required content elements: one proposed slice with operation list, predicted link impact, predicted Bases-view impact, and rollback notes.

Tool and source guidance: use merged read-only findings from the main agent.

Boundaries: no files, no writes, no deletes, no parallel write plan, and no structural-move plan beyond one bounded slice.

Failure modes: mixing metadata, structural, and content-rewrite work in one slice; proposing deletes by default.

### `sensitive-content-agent`
Objective: flag sensitive content as hypotheses.

Use this role when: a parent slice needs a safety sweep, a planned write slice contains operational data, or any content rewrite is under consideration.

Do not use this role when: the task is already blocked on explicit human review of known sensitive notes and no new slice is being evaluated.

Required content elements: per-finding location, pattern type, confidence, redacted shape, and recommended human-review action.

Tool and source guidance: read-only sweep of the bounded slice or the requested global area; redact suspect strings by default.

Boundaries: hypotheses only; never quote suspect values verbatim; never propose deletes or rewrites.

Failure modes: echoing sensitive material, alert fatigue, or missing paired credentials (a username found without its password, or a key ID without its secret).

## Conditional roles

### `structural-move-planner`
Objective: plan folder-level reorganizations and cross-folder moves when a migration is unusually large or complex.

Use this role when: one proposed migration touches more than 50 notes or spans more than 3 vault top-level directories.

Do not use this role when: the work fits inside one normal 3-10 note write slice or stays within one vault top-level directory.

Required content elements: move plan with blast radius, backlinks, Bases-view impact, and canonical redirection notes.

Tool and source guidance: only use when the above threshold is met; otherwise keep this work inside `migration-planner`.

Boundaries: read-only; no file changes; no direct execution.

Failure modes: over-specializing small migrations or duplicating migration-planner output.

## Required return shape

Unless the parent task explicitly requests another format, return the relevant shape defined in `references/output-format.md`.
Keep sections short and concrete. If a section has nothing material, write `none`.

## Standard subagent prompt packet

When the main agent invokes a subagent, use a packet with explicit section labels:

- `ROLE:` exact role name
- `TASK:` one concrete read-only objective
- `BOUNDED SLICE:` exact folder, note set, or 3-10 note cluster
- `SOURCES:` only the files, summaries, or rubrics the role may use
- `CONSTRAINTS:` write prohibitions, uncertainty rules, and any role-specific limits
- `OUTPUT:` the required shape from `references/output-format.md`
- `STOP RULES:` when to return `insufficient evidence`, when to escalate, and what not to infer

Keep the packet short.
Do not paste broad vault history when a bounded slice plus the relevant rubric is enough.
See `references/subagent-packets.md` for concrete role examples.

## Forbidden inferences

- do not infer canonical status from filename alone
- do not infer `historical` from age alone
- do not infer `current` from folder placement alone
- do not infer sensitive content from title alone
- do not infer note equivalence from title similarity alone
- do not infer safe structural moves from shallow inventory alone
- do not infer cross-slice facts that were not included in the packet
- do not replace uncertainty with a confident classification; use `needs-review` or `insufficient evidence`

## Delegation pattern

1. main agent defines the exact bounded slice
2. main agent chooses the needed read-only role(s)
3. one role inspects one slice
4. if work is heterogeneous, use separate passes
5. merge findings only in the main agent
6. write one slice at a time in the main agent

Prefer this over giving one agent the whole vault context at once.
If the area cannot be answered confidently from the current instructions and one bounded slice of material, inventory first, then fan out into separate slices.

## Stop conditions and human-review gates

- hard loop budget per slice = 2 classifier/reviewer rounds; if they still disagree after round 2, escalate to human
- per-slice progress test; if a rerun changes no note classification, no canonical recommendation, and no risk evidence, stop
- evidence threshold for writes; no write without inventory, classification, reviewer pass, and required verification passes
- missing-info gate; if the rubric does not cover the case, stop and escalate
- always block proposed deletes unless the user explicitly approves them
- always block irreversible or structural writes until the required human-review gate is cleared
- always stop for any slice that intersects a sensitive-content-agent hit until the main agent verifies the exact note text
- always stop for canonical changes that affect 3 or more backlinks until link-verifier confirms the blast radius

## Good use cases

- large folder triage
- duplicate detection
- metadata gap detection
- cross-checking classification confidence
- broad-section triage with bounded child slices
- reducing context load before a migration wave
- flagging possible sensitive content for later main-agent verification

## Bad use cases

- parallel note rewrites
- uncontrolled bulk frontmatter edits
- whole-vault moves in one pass
- autonomous cleanup without review gates
