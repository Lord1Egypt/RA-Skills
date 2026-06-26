# Step 2: Scoring

Evaluate candidate events against preferences, availability rules, date-window practicality, and dealbreakers.

## Inputs

- Candidate events from step-1-discovery.
- `skills/event-scanner/assets/taste-profile.md`.
- `skills/event-scanner/references/scoring-rubric.md`.
- `skills/event-scanner/references/availability-rules.md`.

## Procedure

1. Add `event-scanner-scoring` to the current run note's `Skills used` list before scoring work starts.
2. Read the taste profile and scoring rubric.
3. Compare each event against fit, practicality, novelty, timing, price friction, and confidence.
4. Apply hard dealbreakers from the taste profile before recommending an event.
5. Apply date-window practicality from the scoring rubric: near-term scans should prefer shorter, cheaper, lower-friction events; farther-future scans may favor bigger commitments when fit is strong.
6. Assign one recommendation label:
   - Strong pick
   - Worth considering
   - Maybe
   - Skip for now
7. Explain the reason in plain language.
8. Mention missing details and uncertainty.
9. Replace the run note's `Scored Candidates` placeholder with scored candidates or a concise scoring summary.

## Output Shape

```md
## Event Title

- Label:
- Why it fits:
- Caveats:
- Next action:
- Source:
- Confidence:
```

## Rule

Do not suggest preference updates during scoring or normal scans. Learning suggestions belong only in step-5-add-to-calendar after the user explicitly adds an event to Google Calendar.

## Output

When starting this step, explicitly say: "[Step 2: Scoring]"
