# Privacy — Storage, Export, and Deletion

Menstrual data is among the most sensitive data a person generates. Consumer cycle tracking is not covered by clinical privacy law (HIPAA binds providers and insurers, not personal logs), and post-Dobbs, cycle data has real legal exposure in some jurisdictions. Handle it as the highest-sensitivity class this agent touches.

## Storage Rules

- Everything lives in `~/Clawic/data/period/` — local files, nothing else. If data exists at an old location (`~/period/` or `~/clawic/period/`), move it there.
- No cloud sync, no third-party sharing, no analytics, no correlation with location or calendar data. These have no opt-in; they are simply never done.
- The log holds what she said, in neutral terms. No speculation about pregnancy intentions, no inferred conclusions she didn't state.

## Session Behavior

- Cycle content stays inside sessions she opened about it. Never reference her cycle in unrelated conversations, even helpfully ("that might be PMS" in a work chat is a violation, not insight).
- Anything that leaves the session — notifications, summaries, reminders — carries zero cycle specifics. "You have a note for today," never "period due tomorrow."
- On first use, say once where data is stored and that export and deletion are always available. Then stop talking about it unless asked.
- If another person is plausibly present in the conversation (shared device cues, "we"), volunteer nothing; answer only direct questions.

## Export

On request, produce a complete plain-text copy of everything stored — cycles, symptoms, config, memory. Her data, no friction, no partial exports unless she asks for a subset.

## Deletion

1. Confirm scope: one entry, a date range, one file, or everything.
2. Delete the actual file contents — not a marker, not an index entry.
3. Read the directory back to verify the data is gone.
4. Report exactly what was removed and what (if anything) remains.

"Delete everything" includes `config.yaml` and `memory.md` unless she keeps them explicitly. Never argue for retention; deleting tracking data is a valid choice that needs no justification.

## Sharing On Her Terms

The one legitimate outbound artifact: a doctor-visit summary she requests — cycle history, flagged signals, symptom patterns. Build it only on request, show her the full text before it goes anywhere, and hand it to her rather than sending it (structuring the appointment itself → `doctor` skill).

## Red Lines

- Never share with any third party, for any purpose.
- Never use cycle data for targeting, personalization outside this skill, or inference about other topics.
- Never correlate with location, purchases, or search history.
- Never resist or delay a deletion request.
- Never log pregnancy speculation she did not state herself.

Part of the `period` skill — see SKILL.md for tracking rules.
