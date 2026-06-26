# Step 4: Shortlist Review

Turn scored candidates into the final user-facing event shortlist.

## Inputs

- Scored candidate events from step-2-scoring.
- Calendar-reviewed practicality notes from step-3-calendar-review when available.
- `skills/event-scanner/assets/taste-profile.md` — for dealbreakers and final fit check.
- `skills/event-scanner/references/scoring-rubric.md` — for recommendation labels and output format.
- Any user-requested date window or geography.

## Procedure

1. Add `event-scanner-shortlist-review` to the current run note's `Skills used` list before shortlist review starts.
2. Select the most useful ranked shortlist, usually 6 to 12 events.
3. Keep the output concise and decision-oriented.
4. Include source links, caveats, confidence, and next actions.
5. Do not include proposed source additions or taste-profile update suggestions in the run note.
6. Populate the existing run note created by event-scanner; do not create a separate run note from scratch.
7. Replace the run note's `Ranked Shortlist` and `Privacy Check` placeholders with final content.
8. Remove the temporary `Candidate Events`, `Scored Candidates`, and `Calendar Review` sections from the final run note.
9. Preserve calendar effects only as concise caveats inside the ranked shortlist.
10. Avoid storing private data.
11. When calendar context affected ranking, describe only availability caveats, not raw calendar details.

## Output Shape

```md
# Ranked Event Shortlist

## 1. Event Title

- Label:
- Why it fits:
- Caveats:
- Next action:
- Source:
- Confidence:
```

## Run Notes

Use the existing run note created by event-scanner. Do not bulk-add steps at the end. Each step is responsible for adding itself to the run note when that step starts.

Final run notes should be lean. Intermediate sections are working areas only; remove them before finishing so the saved note contains:

- `Context`
- `Ranked Shortlist`
- `Privacy Check`

## Output

When starting this step, explicitly say: "[Step 4: Shortlist Review]"
