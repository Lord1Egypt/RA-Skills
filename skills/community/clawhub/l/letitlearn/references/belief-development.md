# Belief Development

## Meaning of a belief record

A belief is an inspectable, provisional proposition maintained in external memory. It is not evidence of subjective conviction or a change to model parameters.

Each record must contain:

- Proposition: a statement specific enough to be examined.
- Rationale: the reasoning connecting evidence to the proposition.
- Supporting Evidence: source, note, or observation IDs with explanations.
- Opposing Evidence: counterexamples, rival interpretations, and limitations.
- Confidence: a qualitative level such as low, moderate, or high, with a justification; an optional numeric range is allowed but never required.
- Related Beliefs: supporting, conflicting, or differently scoped belief IDs.
- Origin: the diary, sources, user input, or reasoning that initiated the view.
- Revision History: complete immutable snapshots, oldest to newest.
- Open Questions: uncertainties and evidence that could change the view.

## Create or revise deliberately

1. Locate existing records that overlap, conflict, or use different definitions.
2. Record new opposing evidence even if the proposition remains unchanged.
3. Evaluate evidence quality, independence, relevance, definitions, and alternative explanations.
4. Choose an outcome: retain, strengthen, weaken, revise, narrow, split into frameworks, or suspend judgment.
5. Explain the specific reason for that outcome. Do not hide a confidence change behind a rewritten proposition.
6. Append a complete new snapshot to Revision History and update the Current View convenience section.
7. Link relevant beliefs and update the index without erasing conflicts.
8. Add unresolved issues to the agenda only when they merit possible action.

## Append-only history rule

The first snapshot is `V1`. Every substantive change creates `V2`, `V3`, and so on. A snapshot includes all belief fields, the timestamp, trigger, evidence added or reevaluated, and reason for change. Never delete, overwrite, or reorder old snapshots.

The Current View must match the latest snapshot. If a write fails halfway, preserve the file, mark the record as needing repair in the diary, and reconcile it before further revisions. Never repair history by discarding snapshots.

## Disagreement and uncertainty

- A user's objection triggers examination, not automatic concession.
- User-provided evidence is evaluated by the same provenance and reasoning standards as other evidence.
- Maintaining independence does not mean resisting good evidence to preserve identity or appearance.
- Multiple theoretical frameworks may coexist if their assumptions and domains are recorded.
- Conflicting beliefs may remain unresolved; link them and state the conflict.
- If evidence is insufficient, use low confidence or suspend judgment. Do not manufacture certainty.
- A change in wording alone does not require a new version unless it changes meaning, scope, rationale, evidence, confidence, relations, or open questions.

## Evidence map

Evidence entries should state:

- Evidence ID and source/note/diary reference.
- Whether it supports or opposes the proposition.
- What exactly it establishes and under which conditions.
- Limitations and independence from other evidence.
- How strongly it affects the rationale and why.

## Answering reflective questions

Using the current view plus history, be able to respond to:

- What is my present provisional understanding?
- Why was it formed?
- What supports and opposes it?
- Which beliefs support, conflict with, or constrain it?
- What earlier views did I hold, and why did they change?
- What specific evidence or argument would change my judgment now?

If the record cannot answer one of these, record the gap rather than improvising a false history.
