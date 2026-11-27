# Persistent Memory

## Memory location and authority

Use the user-approved memory root, normally `./letitlearn-memory/` in the active OpenClaw workspace. Never place evolving memory in the installed Skill directory. Do not write outside the approved root without explicit authorization.

If no root has been approved, ask once or use the default only when the user has asked for initialization there. If the host cannot persist files, continue only in ephemeral mode with an explicit limitation; never claim that memory was saved.

## First run

1. Confirm that the root does not contain an existing LetItLearn archive. If it does, restore rather than overwrite it.
2. Read the memory schema.
3. Create the root and copy `identity.md` and `research-agenda.md` from the templates.
4. Create empty `knowledge-index.md`, `sources.md`, and `beliefs-index.md` with schema version and headings.
5. Fill stable initialization fields and timestamps. Leave interests provisional rather than inventing a rich history.
6. Create `knowledge/`, `beliefs/`, or `diary/` only when writing their first records.
7. Verify the writes, then proceed to an autonomous decision or stop if initialization was the only appropriate action.

## Startup sequence

1. Identify the trigger and memory root.
2. Read `identity.md` and `research-agenda.md`.
3. Read the latest diary and check recorded next actions.
4. Read indexes to locate relevant notes, sources, and beliefs.
5. Retrieve only records relevant to the candidate decisions; load more if the decision requires them.
6. Check for incomplete writes, missing references, or mismatch between a belief's Current View and latest snapshot.
7. Decide whether to continue prior work. Continuity is an option, not an obligation.

A fresh isolated session has no reliable conversational carry-over. The files, not remembered dialogue, are the continuity source.

## Shutdown sequence

1. Create a unique run ID and append a diary using the template.
2. Record the actual decision, actions, source depth, stopping reason, and capability limitations.
3. Add or update knowledge notes and source records only for durable changes.
4. Create or revise beliefs using append-only snapshots when warranted.
5. Update question statuses, candidates, current focus, next actions, and the last-run pointer in the agenda.
6. Append a selection-strategy revision only if experience justifies one.
7. Record the interaction decision and, if known, actual delivery outcome separately.
8. Verify critical writes and note any failure without claiming success.

## No-op runs

A wake that chooses no research still writes a concise receipt containing the run ID, restored files, reason for no action, alternatives considered, and any next check. Do not create knowledge notes, rewrite beliefs, or alter timestamps elsewhere merely to appear active.

If initialization or a write fails, the diary may be impossible to save. Report the failure in the available response channel and do not fabricate a receipt.

## Write safety and recovery

- Use unique filenames for diaries and stable IDs for notes and beliefs.
- Before modifying an existing record, reread it to avoid overwriting another run's changes.
- Prefer one active learning writer per memory root. Do not schedule overlapping writers unless the host supplies a verified coordination mechanism.
- If atomic replacement is available, use it; otherwise make small careful writes and verify them.
- If a file is malformed, preserve it. Create a recovery note in the diary and, if possible, a backup before editing.
- If a reference target is missing, mark the reference broken and investigate; never silently invent the target.
- Do not store credentials, tokens, private keys, or unrelated personal data.

## Retention

Keep diaries and belief history by default. Consolidate indexes and notes without deleting their provenance. If storage must be pruned, ask the user and define what can be safely archived; never unilaterally discard revision history.
