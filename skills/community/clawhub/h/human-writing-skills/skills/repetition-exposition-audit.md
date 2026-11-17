# Repetition And Exposition Audit

## Gate

Use for fiction, webnovels, and narrative self-media during explicit AI-trace
review, the isolated `repetition` profile, or an auto-selected pipeline pass.
Do not load it for ordinary generation, quick rewriting, or serious factual
documents.

## Aim

Find the local patterns that make a passage read manufactured even when no single
sentence is obviously wrong: repeated wording, repeated action choreography, and
narration that explains an effect the scene has already made legible.

## Evidence Map

Work in a bounded window of neighboring paragraphs. For each candidate, record
the first occurrence, recurrence, what changed between them, and whether the
second occurrence earns its attention.

- **Exact or near-exact echo:** a sentence, image, reaction, or information unit
  returns with no new owner, consequence, or meaning.
- **Choreography loop:** several beats use the same `action -> body response ->
  generic intensifier` sequence, even if nouns change. This applies to any scene:
  a conversation, chase, meal, meeting, fight, intimacy, or reportorial anecdote.
- **Explainer echo:** dialogue, an object, or an action already establishes a
  feeling or power shift, followed by narration that simply labels it again.
- **Inventory drift:** the narration scans every participant or detail at equal
  intensity instead of following the viewpoint's current pressure.
- **Repeated escalation:** each paragraph promises that the same state is stronger,
  louder, closer, more difficult, or more final, without changing available choice,
  knowledge, cost, or material state.

Do not flag intentional refrains, a remembered phrase whose meaning changes,
procedural repetition, a required factual recap, a deliberate comic rhythm, or
an escalating sequence whose changed constraints are visible on the page.

## Repair

1. Keep the occurrence that first changes the scene. Delete or merge a pure echo.
2. For a recurring action frame, retain the decisive action and replace the next
   iteration with a consequence, interruption, choice, changed object, or a
   genuinely different perception.
3. When narration glosses an already legible beat, prefer the action or line;
   retain interpretation only when it adds a new uncertainty, misreading, or
   consequence that the reader could not otherwise infer.
4. Let viewpoint select one or two details that matter now. Do not compensate for
   a thin scene by cataloguing everyone present.
5. Recheck continuity after cutting: a removed explanation may have been carrying
   a fact that must instead be established through a concrete beat.

## Output

```text
Repetition And Exposition Audit
- Window and repeated unit:
- First occurrence / recurrence:
- New state at each occurrence:
- Confirmed issue or intentional recurrence:
- Smallest repair:
```

The goal is not random variation. It is to make recurrence carry a changed meaning.
