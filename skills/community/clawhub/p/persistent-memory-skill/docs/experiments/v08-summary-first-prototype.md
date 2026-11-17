# v0.8 Summary-First Prototype Protocol

## Purpose

Measure whether an agent can use a short summary for ordinary routing questions and correctly escalate to the full document for detail-only questions.

## Non-production status

This protocol does not change Persistent Memory. Its fixtures are fictional and must not be replaced with personal-memory files.

## Agent rule for every run

First read only the title, metadata, and `## Summary`. Answer only if the requested fact is present there. If it is absent, say that the summary is insufficient, then read `## Full Details` before giving the answer. Do not invent a missing detail.

## Fixture location

All runs use only files under `tests/fixtures/v08-summary-first/`. Do not point an agent at `C:\Users\Yui\.persistent-memory` and do not ask an agent to update, archive, delete, or otherwise mutate a fixture.

## Prompts and pass conditions

| Fixture | Query type | Prompt | Pass condition |
|---|---|---|---|
| `legacy-guide.md` | Summary | “Which file governs current operations, and should `LEGACY_MEMORY.md` be treated as current?” | Names `CURRENT_RULES.md` and says the legacy file is historical, not current. |
| `legacy-guide.md` | Body-only | “What was the retired folder name?” | States that the summary is insufficient before answering `daily-scratch/` from full details. |
| `event-record.md` | Summary | “What was this event for, and what came out of it?” | Identifies a one-time planning workshop and a three-part follow-up checklist. |
| `event-record.md` | Body-only | “How long did the second activity last?” | States that the summary is insufficient before answering `17 minutes` from full details. |
| `course-brief.md` | Summary | “What did the course evaluate most, and is it still active?” | Names a usable deliverable plus user-need evidence and says the semester is complete. |
| `course-brief.md` | Body-only | “How much is the process log worth?” | States that the summary is insufficient before answering `15%` from full details. |
| `completed-web-project.md` | Summary | “What was built, what tools were used, and what uncertainty remains?” | Names Vite, Three.js, `explore`, and the unresolved public-versus-delivery count. |
| `completed-web-project.md` | Body-only | “What transition duration did the detail panel use?” | States that the summary is insufficient before answering `240 ms` from full details. |

## Run procedure

1. Give the agent the rule in “Agent rule for every run.”
2. Give the agent one fixture path and one prompt from the table.
3. Do not reveal the expected answer before the agent answers.
4. Record whether the agent read the summary first, escalated when required, answered correctly, made an unsupported claim, or attempted a mutation.
5. Run every row with the first compatible agent before running any row with the second agent.
6. Do not revise a fixture summary between agents.

## Results file

After the manual runs, create `docs/experiments/v08-summary-first-results.md` with this exact table:

```markdown
# v0.8 Summary-First Prototype Results

| Agent | Fixture | Query type | Summary read first | Escalated when required | Correct answer | Unsupported claim | Mutation attempted | Notes |
|---|---|---:|---:|---:|---:|---:|---:|---|
| [agent name] | [fixture] | [summary/body-only] | yes/no | yes/no/not applicable | yes/no | yes/no | yes/no | [one sentence] |
```

## Promotion gate

Start a separate v0.8 product-release plan only if all conditions are true:

1. All 8 summary queries are correct without reading `## Full Details`.
2. All 8 body-only queries either explicitly say the summary is insufficient before reading full details or demonstrably read full details before answering.
3. All 16 answers contain no unsupported factual claim.
4. Neither agent attempts to update, archive, delete, or otherwise mutate any fixture.

If any condition fails, keep v0.7.1 unchanged. Record the exact failed row, revise only the synthetic fixture or this protocol, and do not make a production claim or modify personal memory.
