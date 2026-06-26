# Output and merge format

Use one compact format so subagent findings are mergeable.
This file is the single source of truth for output shapes.

## Context router

| Context | Use this shape |
|---|---|
| Subagent reply | `Required five-section shape` |
| Single-pass main-agent reply with no subagents | `Required five-section shape` |
| Main-agent merged reply from two or more subagent slices | `Final main-agent summary shape` |

## Required five-section shape

Return these sections in this order:

1. `Current state`
2. `Classification recommendations`
3. `Risks and contradictions`
4. `Next write slice`
5. `Verification`

Keep each section short and concrete.
If a section has nothing material, write `none`.

## Preferred note-level fields

When naming important notes, prefer this shape:

- `Path or note name`
- `doc_kind`
- `status`
- `canonical` yes/no when relevant
- short reason
- optional `confidence: low|medium|high`

If the bounded slice does not support a recommendation, write `insufficient evidence` and prefer `needs-review` over guessing.

## Sensitive findings

If a subagent suspects sensitive content (see `references/subagents.md` glossary):

- treat it as a hypothesis, not a confirmed finding
- reference only the note path, field or section, pattern type, and redacted shape
- do not quote the sensitive value
- do not recommend edits as if the finding were confirmed
- place the finding under `Risks and contradictions`
- require main-agent verification against exact note text before escalation or editing

## Merge rules for the main agent

When merging child-slice results:

1. prefer compact summaries over repeating every detail, but keep disagreements visible
2. surface disagreements explicitly
3. downgrade contested notes to `needs-review`
4. separate confirmed facts from hypotheses
5. separate structural actions from content rewrite actions
6. keep unsupported claims out of the merged summary; use `insufficient evidence` where needed

## Human-review gates

Escalate to explicit human review before:

- deleting notes
- moves or renames affecting more than 10 notes or more than 1 vault top-level directory
- editing notes after only inferred classification
- acting on sensitive-content hypotheses
- collapsing multiple competing pages into one canonical page without clear evidence
- changing a canonical page with 3 or more affected backlinks

## Final main-agent summary shape

When reporting merged results back after a multi-slice pass, use the required five-section shape.
