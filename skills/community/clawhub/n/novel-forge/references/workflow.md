# Workflow

## 1. Project bootstrap

### 1.1 Decide execution mode
- If the request is a continuation/resume, run project discovery first and show candidate projects before anything else.
- Default to multi-agent unless the user explicitly asks for single-agent.
- If you will use multiple agents, first read `/root/.openclaw/openclaw.json`, then list the available models, and only then ask the user to map `provider/model-id` strings to roles.
- If the inventory cannot be read, stop and report the failure instead of guessing.
- If you will use a single agent, state that explicitly and do not fabricate a role table.
- If multi-agent is selected, the main session must route canon work through the role pipeline; it must not author canon prose directly.

### 1.2 Gather and lock bootstrap inputs
1. Create a project state bundle.
2. Confirm target genre, audience, tone, length or chapter count, and taboo list.
3. Confirm the core premise.
4. Require author confirmation before locking premise, hard canon, and style.
5. Treat bootstrap as locked only after title, genre/audience, target length or chapter count, taboo list, premise, execution mode, and model assignment table (if multi-agent) are all confirmed in project state.

### 1.3 Bootstrap gate criteria
Do not proceed to canon generation until all of these are satisfied:
- title exists
- genre / audience exist
- target length or chapter count exists
- taboo list exists
- premise is explicitly confirmed
- execution mode is explicit (single-agent or multi-agent)

If any item is missing, stop and ask for it instead of drafting ahead.

### 1.4 Operational state
- Treat `state/current.json` as the concise runtime snapshot when present.
- Keep it aligned with `project.json`, chapter state, batch-outline state, and recovery notes.
- Use it as the first place to check the latest chapter boundary and recovery target.
- After each accepted chapter, write back `workflow.step`, `chapter.currentChapterIndex`, `chapter.nextChapterIndex`, `recoveryCheckpoint`, and the latest state delta.
- After each accepted batch outline, write back the current 10-chapter window and its lock status.

## 2. Canon generation order

Only enter this stage after the bootstrap gate has passed.

1. Worldbuilding
2. Characters
3. Full novel outline
4. 10-chapter batch outline, if needed
5. Chapter writing beats
6. Style samples
7. Style lock

### Multi-agent execution rule
- In multi-agent mode, every stage must be executed by its designated agent/role.
- Before each stage, the main session must invoke the designated agent/role and wait for its output.
- This applies to bootstrap, canon generation, style sampling, chapter drafting, review, recovery, and maintenance.
- The main session may collect, validate, and persist outputs, but must not synthesize the stage content itself.
- The orchestrator may advance only after the required stage output exists and passes the smallest relevant validation check.

## 3. Style sampling

Use one fixed scenario for every candidate.

Do not sample style before the premise and core tone are locked; otherwise the samples will drift and mislead the author.

Suggested scenario ingredients:
- protagonist entrance
- a mild conflict
- one dialogue exchange
- one sensory detail block
- one inner thought
- one ending hook

## 4. Resume / 断档续写

When the user wants to continue from a truncated draft or restore a partial chapter:

1. Discover candidate projects first if the workspace may contain more than one active novel.
2. Present the matching projects with title, genre, latest chapter, checkpoint, and resume metadata.
3. Let the user choose the project before recovering canon.
4. Identify the last stable checkpoint.
5. Read only the project state, outline, recent summaries, and partial draft needed to recover context.
6. Separate hard canon from inferred material.
7. State the resume target before generating new prose.
8. Resume from the last stable sentence or beat boundary.
9. Never rewrite unrelated sections unless the user asks.
10. If essential facts are missing, stop and ask.
11. If the fragment is too short to recover safely, ask for the missing paragraph, summary, or chapter beat instead of manufacturing a bridge.
12. When resuming, lead with a recovery summary so the author can verify the recovered state before the prose continues.

## 5. Chapter production loop

1. Load only the relevant canon slice.
2. Draft the chapter.
3. Review against canon and style.
4. Revise if needed.
5. Archive state and memory.

### Minimal input packet
For each stage, pass only:
- stage goal
- opening state
- relevant canon slice
- forbidden deviations
- expected output shape
- current character state
- checkpoint / resume boundary, if any

For batch-outline stages, include the current 10-chapter window and what must be locked before drafting that batch.

## 6. Long-run maintenance

Run periodic checkpoints every 5–10 chapters:
- refresh summary
- compress memory
- compare outline vs reality
- identify style drift
- identify dangling plot threads
- ask the user before large retcons

### Stage failure fallback
- If a designated agent fails or returns unusable output, stop the pipeline.
- Do not synthesize the missing stage in the main session.
- Ask the user whether to retry the stage, switch to single-agent mode, or stop.
- If an accepted full outline changes, invalidate any derived 10-chapter batch outlines and regenerate them before resuming chapter drafting.

## 7. Batch writing

For 3+ chapters:
- split into small batches
- checkpoint between batches
- do not let unresolved conflicts accumulate
- keep chapter endings forward-driving
