# Knowledge Accumulation

## Aim

Build a connected, inspectable body of knowledge rather than a collection of indiscriminate summaries. A small number of well-linked notes can be a better outcome than many extracted passages.

## Knowledge notes

Create a note only for a durable concept, theory, mechanism, problem, or synthesis. Use a stable ID such as `K-20260301-001` and include:

- Title and aliases.
- A concise explanation in the Agent's own words.
- Epistemic status and relevant context or boundary conditions.
- Source IDs supporting the explanation.
- Important claims with their fact/claim/inference/hypothesis labels.
- Relations to other notes or beliefs.
- Open questions and promising next directions.
- Created and updated timestamps plus contributing diary IDs.

Do not detach a claim from its source merely to make a note look authoritative. Keep source-specific interpretations attributed.

## Relations

Use explicit relation labels where helpful:

- `explains`: one mechanism accounts for part of another note.
- `supports` or `contradicts`: a claim or belief relation, with evidence IDs.
- `refines`: narrower scope, better definitions, or improved precision.
- `example-of` or `analogy-to`: an instance or a limited comparison.
- `depends-on`: a concept required for understanding.
- `unresolved-link`: a suspected relation needing investigation.

For every important relation, add a short explanation. A bare list of links is not a knowledge connection. Analogies must include their limits.

## Update procedure

1. Search the existing index for aliases and overlapping concepts before creating a note.
2. Merge into an existing note when the new material genuinely extends the same concept; otherwise create a distinct note and relate them.
3. Preserve source IDs and qualifying conditions when merging.
4. Add or revise relations only when an explanation can be stated.
5. Update `knowledge-index.md` with a one-line description and path.
6. Add unresolved issues to `research-agenda.md` only if they are real candidates for later action.
7. Record the created or changed note IDs in the diary.

Do not rewrite an unchanged note just to update its timestamp. If a rewrite loses an important prior interpretation, preserve that interpretation in the note's change log or in the relevant diary and belief history.

## Source register

Maintain `sources.md` as an append-oriented register. Do not silently change the bibliographic identity of an existing source. Corrections should state what changed and why. Multiple notes should reference the same source ID rather than duplicating full records.

## Open questions

A useful open question is specific enough to guide action but need not be narrow. Include:

- Question ID and wording.
- Origin note, belief, source, or diary.
- Why it matters to the current knowledge structure.
- What kind of evidence or reasoning could address it.
- Status: open, active, parked, answered, or dissolved.
- Resolution or parking reason when applicable.

An answered question may remain in the record for provenance. Do not delete it simply to make the agenda look clean.

## Periodic synthesis

When notes become fragmented, choose a Synthesizing run to:

- Identify duplicate or weakly connected notes.
- Compare definitions and hidden assumptions.
- Expose contradictions rather than forcing premature coherence.
- Create a synthesis note with explicit links and remaining uncertainties.
- Rebuild the index without deleting underlying provenance.
