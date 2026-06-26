# Subagent packet examples

Use these examples when the main agent prepares a read-only subagent call.

Keep the packet short.
Pass only the bounded slice, the minimum relevant rubric, and the exact constraints.
Use the output shapes from `references/output-format.md`.

## Packet template

```text
ROLE:
<exact role name>

TASK:
<one concrete read-only objective>

BOUNDED SLICE:
<exact folder, note set, or 3-10 note cluster>

SOURCES:
- <allowed file, summary, or rubric>

CONSTRAINTS:
- read-only
- use only the bounded slice and listed sources
- if evidence is insufficient, write `insufficient evidence`
- prefer `needs-review` over guessing

OUTPUT:
Return the required five-section shape from `references/output-format.md`.

STOP RULES:
- do not infer outside the bounded slice
- do not propose writes
- do not quote sensitive values
- stop when the bounded slice does not support a stable recommendation
```

## Example: `inventory-agent`

```text
ROLE:
inventory-agent

TASK:
Map the current state of this vault area before any deeper pass.

BOUNDED SLICE:
Folder `40 Skills & Automatisierung/Obsidian Curator`, capped at 200 notes.

SOURCES:
- note files inside the bounded slice
- `references/status-schema.md`

CONSTRAINTS:
- read-only
- do not classify note status beyond obvious missing metadata flags
- do not compare content deeply; shallow duplicate detection only
- do not propose writes
- if evidence is insufficient, write `insufficient evidence`

OUTPUT:
Return the required five-section shape from `references/output-format.md`.

STOP RULES:
- use only the bounded slice
- if a duplicate needs content comparison, route it as a candidate for `duplicate-cluster-agent`
- if a note may contain sensitive content, flag it under `Risks and contradictions` as a sensitive-content hypothesis and prefer `status: needs-review`
```

## Example: `duplicate-cluster-agent`

```text
ROLE:
duplicate-cluster-agent

TASK:
Check whether these 4 notes are near-duplicates, forks, drafts, or only topic-overlapping.

BOUNDED SLICE:
These 4 notes only:
- `X.md`
- `Y.md`
- `Z.md`
- `W.md`

SOURCES:
- note bodies for the 4 notes
- inventory summary that flagged them as duplicate candidates

CONSTRAINTS:
- read-only
- compare content and structure, not filename alone
- do not merge notes
- do not propose `superseded_by`
- if evidence is insufficient, write `insufficient evidence`

OUTPUT:
Return the required five-section shape from `references/output-format.md`.

STOP RULES:
- do not call notes duplicates from title similarity alone
- do not infer one canonical note from path prestige alone
- if overlap is weak, report `topic-overlap` or `coincidental-match`
```

## Example: `classifier-agent`

```text
ROLE:
classifier-agent

TASK:
Classify this 5-note topic cluster and propose canonical candidates.

BOUNDED SLICE:
These 5 notes only:
- `A.md`
- `B.md`
- `C.md`
- `D.md`
- `E.md`

SOURCES:
- inventory summary for this slice
- duplicate-cluster result if duplicate or overlap risk exists
- `references/status-schema.md`
- `references/classification-rubric.md`

CONSTRAINTS:
- read-only
- use only these 5 notes plus the listed source files and summaries
- do not rely on folder history outside the packet
- if a note stays ambiguous, prefer `needs-review`
- if evidence is insufficient, write `insufficient evidence`

OUTPUT:
Return the required five-section shape from `references/output-format.md`.

STOP RULES:
- do not propose deletions
- do not force a canonical page when the slice does not support one
- do not infer `historical` from age alone
```

## Example: `curation-reviewer`

```text
ROLE:
curation-reviewer

TASK:
Challenge the classifier output for this same 5-note slice before any write planning.

BOUNDED SLICE:
The same 5 notes reviewed by `classifier-agent`:
- `A.md`
- `B.md`
- `C.md`
- `D.md`
- `E.md`

SOURCES:
- classifier-agent output for this exact slice
- inventory summary for this exact slice
- `references/status-schema.md`
- `references/classification-rubric.md`

CONSTRAINTS:
- read-only
- critique only
- do not introduce final classifications as new truth
- return per-note `pass`, `revise`, or `escalate-to-human`
- if evidence is insufficient, write `insufficient evidence`

OUTPUT:
Return the required five-section shape from `references/output-format.md`.

STOP RULES:
- if classifier and reviewer still disagree after round 2, escalate to human review
- if a contested note remains, keep it `needs-review`
- do not propose writes
```

## Example: `link-verifier`

```text
ROLE:
link-verifier

TASK:
Check link and backlink risk for this proposed canonical-page update.

BOUNDED SLICE:
Proposed write slice plus directly affected link targets:
- `Canonical Page.md`
- `Old Supporting Note.md`
- `Topic Index.md`

SOURCES:
- proposed rename, move, canonical switch, supersession update, or index change
- affected note paths
- `scripts/check_links.py` output if available

CONSTRAINTS:
- read-only
- report breakage only; never repair it
- inspect wikilinks, backlinks, embedded transclusions, and Dataview/Bases query bodies
- cap the bounded slice at 200 notes; if directly affected backlinks exceed 200, split the link-verifier pass by topic or by source folder
- treat slice-local checks as slice-local, not vault-global proof
- if affected backlinks are outside the inspected slice, return `insufficient evidence` and request a wider slice

OUTPUT:
Return the required five-section shape from `references/output-format.md`.

STOP RULES:
- do not modify links
- do not approve a canonical change with 3 or more affected backlinks unless blast radius is clear
- do not infer safe moves from shallow inventory alone
```

## Example: `migration-planner`

```text
ROLE:
migration-planner

TASK:
Propose exactly one 3-10 note write slice based on completed read-only findings.

BOUNDED SLICE:
One proposed write slice only:
- `Note 1.md`
- `Note 2.md`
- `Note 3.md`

SOURCES:
- merged main-agent findings
- inventory-agent output
- classifier-agent output
- curation-reviewer output with `pass`
- sensitive-content-agent output when the slice includes content rewrite or operational data
- link-verifier output when the slice changes a canonical page with 3 or more affected backlinks

CONSTRAINTS:
- read-only
- plan only; do not create or modify files
- no deletes
- no parallel write plan
- do not mix metadata, structural, and content-rewrite work in one slice
- if any contested note remains, return `insufficient evidence` instead of a write plan

OUTPUT:
Return the required five-section shape from `references/output-format.md`.

STOP RULES:
- do not propose a write slice before inventory, classification, reviewer pass, and required verification passes are complete
- do not propose a write slice unless curation-reviewer returned `pass` for every note in the slice
- do not propose structural moves beyond one bounded slice
- block deletion proposals unless the user explicitly approved deletion planning
```

## Example: `sensitive-content-agent`

```text
ROLE:
sensitive-content-agent

TASK:
Review this planned write slice for sensitive content.

BOUNDED SLICE:
These 3 notes only:
- `Ops Note 1.md`
- `Ops Note 2.md`
- `Migration Draft.md`

SOURCES:
- note files in the bounded slice
- sensitive-content definition from `references/subagents.md` glossary

CONSTRAINTS:
- read-only
- hypotheses only
- cap the bounded slice at 200 notes; if the relevant area exceeds 200 notes, split into multiple sensitive-content-agent passes
- redact suspect strings by default
- never quote sensitive values verbatim
- if evidence is insufficient, write `insufficient evidence`

OUTPUT:
Return the required five-section shape from `references/output-format.md`.

STOP RULES:
- do not recommend edits as if a finding were confirmed
- place findings under `Risks and contradictions` as sensitive-content hypotheses
- point only to note path, field or section, pattern type, and redacted shape
```

## Example: `structural-move-planner`

```text
ROLE:
structural-move-planner

TASK:
Plan folder-level reorganization risk for a migration that crosses the structural threshold.

BOUNDED SLICE:
One proposed structural migration that touches more than 50 notes or spans more than 3 vault top-level directories.

SOURCES:
- merged main-agent findings
- inventory summaries for each affected folder root
- link-verifier output or planned link-verifier scope
- current folder-root map

CONSTRAINTS:
- read-only
- plan only; do not create, rename, move, or delete files
- do not replace `migration-planner` for normal 3-10 note write slices
- compute blast radius for backlinks, Bases views, Dataview queries, embeds, and canonical redirections
- if evidence is insufficient, write `insufficient evidence`

OUTPUT:
Return the required five-section shape from `references/output-format.md`.

STOP RULES:
- do not approve execution
- do not propose parallel writes
- if the migration is below threshold, return that `migration-planner` should handle it instead
- block deletion proposals unless the user explicitly approved deletion planning
```
