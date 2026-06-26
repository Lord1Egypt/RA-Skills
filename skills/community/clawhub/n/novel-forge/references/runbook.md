# Novel Forge Runbook

## 1. Resume or new project
- If the user says continue/resume/truncated, discover candidate projects first.
- Show the candidates with title, latest chapter, and checkpoint.
- Ask the user to choose if more than one matches.
- If only one project matches, confirm it and continue.

## 2. Model mapping
- First read `/root/.openclaw/openclaw.json`.
- Inspect the available models.
- Ask for a role→model mapping for multi-agent work before any canon work.
- Persist the mapping in `project.json.models`.
- After the mapping is chosen, verify which agent IDs are spawnable for `sessions_spawn`.
- Store role mappings as `provider/model-id` strings in project state.
- Do not treat those strings as the direct runtime payload for `sessions_spawn`; that translation belongs to the orchestration layer.
- If only one model is available, ask whether to reuse it across roles.
- If single-agent is selected, set `orchestrator` and collapse the rest into `n/a` or the same model by policy.

## 3. Bootstrap gate
Do not generate canon until these are known:
- title
- genre / audience
- target length or chapter count
- taboo list
- core premise
- execution mode
- model assignment table when multi-agent is selected
- chapter/scene checkpoint for resume work

Bootstrap is considered locked only when the above fields are persisted in project state.

## 4. Canon order
Use this order and do not parallelize phase 0:
1. Worldbuilding
2. Characters
3. Full outline
4. Volume plan if needed
5. 10-chapter batch outline
6. Style samples
7. Style lock

## 5. Chapter loop
For each chapter:
1. Load the smallest relevant canon slice.
2. Write the draft.
3. Review the draft.
4. Revise if needed.
5. Accept the chapter.
6. Update memory and state.
7. Write `state/current.json` immediately after acceptance.
8. If the full outline changes, mark any outstanding batch outline stale before the next chapter is drafted.

## 6. Resume summary
When resuming, begin with:
- what is known
- what is uncertain
- where the next prose starts

## 7. Long-run maintenance
- Refresh summaries every 2–3 chapters.
- Run a deeper canon/style audit every 5–10 chapters.
- Stop before unresolved conflicts pile up.
- If the full outline changes, invalidate any derived 10-chapter batch outlines and regenerate them before continuing.
- After each checkpoint, update `state/current.json` so the latest chapter boundary is always visible in one place.

## 8. Minimal task packet
Send writers only:
- chapter goal
- opening state
- key beats
- ending hook
- relevant canon slice
- style constraints
- forbidden deviations
- current character state

For batch-outline tasks, send the 10-chapter window, batch constraints, and any locked canon that must not change.
