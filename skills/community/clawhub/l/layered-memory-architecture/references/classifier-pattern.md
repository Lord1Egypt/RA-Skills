# Layer Classifier Pattern

Use this pattern to classify new information into the correct memory layer before writing it.

## Goal
Do not decide memory destination implicitly.
Classify first, then write.

## Inputs
For each candidate note, determine:
- scope: cross-project or project-specific
- durability: temporary, stable, or likely durable
- authority: observed event, doctrine/rule, current status snapshot, raw artifact
- recency: current session/day or older durable lesson
- actionability: whether it should shape future behavior

## Decision pattern
Apply these questions in order:

1. Is this a current operational snapshot or generated status view?
   - yes → generated summary

2. Is this a fresh event, observation, or session note that may or may not matter later?
   - yes → episodic log or project note

3. Is this tightly bound to one initiative and still changing quickly?
   - yes → project-scoped working memory

4. Is this a durable rule, doctrine, architecture note, or decision history that will matter again?
   - yes → topic doctrine

5. Is this a compact, cross-project truth that belongs in the hot path?
   - yes → hot canon

If more than one answer seems true, bias toward the lower layer first.

## Output format
When helpful, express the classification as:

```json
{
  "candidate": "short description",
  "recommended_layer": "hot-canon|topic-doctrine|project-memory|episodic-log|generated-summary",
  "confidence": "low|medium|high",
  "reason": "one sentence explaining why",
  "promotion_candidate": true,
  "needs_human_review": false
}
```

## Heuristics
### Send to hot canon when the note is:
- cross-project
- durable
- compact enough to summarize in 1-3 bullets
- likely to matter across many future sessions

### Send to topic doctrine when the note is:
- durable
- too detailed for hot canon
- useful again later
- best kept as architecture, doctrine, or playbook

### Send to project memory when the note is:
- tied to one project
- still changing
- too raw or bulky for doctrine

### Send to episodic log when the note is:
- new
- uncertain in long-term value
- a record of what happened today

### Send to generated summary when the note is:
- derived from live inputs
- rebuildable
- mainly useful for current status rather than long-term truth

## Anti-patterns
Do not:
- promote fresh notes directly into hot canon just because they feel important
- store live status as doctrine
- use project memory as a dumping ground for cross-project rules
- treat the classifier as certainty; it is a routing aid, not a law of physics
