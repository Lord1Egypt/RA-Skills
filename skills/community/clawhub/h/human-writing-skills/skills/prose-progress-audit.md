# Prose Progress Audit

## Aim

Catch polished but static drafts whose paragraphs restate a premise, emotion, or
argument without material change.

## Paragraph Progress Test

For each paragraph or scene beat, record:

- What became newly true?
- What did the reader learn that was not already inferable?
- What action, evidence, decision, cost, or contradiction moved?
- What pressure is carried into the next paragraph?

If two neighboring paragraphs reduce to the same summary, cut or merge one.

## Narrative Progress Types

- Position changes: someone moves, reaches, blocks, exits, crosses a barrier.
- Knowledge changes: someone learns, suspects, hides, misreads, or reveals.
- Relationship changes: trust, leverage, debt, shame, desire, or boundary shifts.
- Material changes: object, clothing, injury, money, evidence, time, or resource changes.
- Emotional changes: feeling becomes action, contradiction, or bodily signal.
- Promise changes: a hook opens, advances, complicates, or closes.

## Expository Progress Types

- Claim narrows or sharpens.
- Evidence appears and is attributed.
- Counterexample complicates the claim.
- Definition becomes more precise.
- Practical consequence becomes clear.
- The writer admits uncertainty or limit.

## Interaction Progress Test

When a line, gesture, decision, or discovery pressures another present character,
look for speech, action, bodily response, legible silence, interruption, or explicit
deferral before the passage shifts. Otherwise flag an orphaned interaction beat.

Require uptake only when a stimulus requests, challenges, reveals, touches a boundary,
alters terms, or changes available choices. Delayed uptake is valid when the text
carries the debt into the next relevant beat.
Include ordinary actions awaiting cooperation. Delegate bidirectional and partially
answered speech/action checks to `dialogue-voice-audit`.

## Audit Steps

1. Create a paragraph summary list.
2. Mark duplicate/decorative summaries, absent state change, and abandoned interaction.
3. For each weak paragraph, decide:
   - cut
   - merge
   - replace with evidence
   - convert explanation into action
   - add a complication
4. Preserve stillness only when it creates tension, voice, or changed observation.
5. In long drafts, flag non-neighboring echoes that repeat a fact or feeling without
   changing its evidence, owner, consequence, or interpretation.
6. If the passage is an expansion, compare added attention with added state change.
   Route scene-level word-allocation problems to `attention-budget-audit`.
7. Mark zero-progress terminal reflection or scenery as a candidate for the optional
   `ending` profile; do not duplicate that profile's full tail classification here.

## Output Check

```text
Prose Progress Audit
- Paragraph summary map:
- Duplicate or static paragraphs:
- Missing state change:
- Orphaned interaction beat or deferred interaction debt:
- Zero-progress terminal tail:
- Minimal repair:
```

A paragraph may be quiet. It may not be ornamental unless the genre explicitly
wants ornament and the surrounding text can carry it.
