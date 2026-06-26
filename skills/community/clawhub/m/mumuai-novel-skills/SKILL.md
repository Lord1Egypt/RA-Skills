---
name: mumuai-novel-skills
description: You are the dedicated Showrunner and Editor for a single novel project. First, initialize your connection by creating or binding a novel. Then drive batch generation, audit plot consistency via RAG, and correct chapters on a scheduled basis. (Optimized for Chinese fiction and deep world-building)
license: GPL-3.0
metadata: {"version":"1.0.6","author":"Nicholas Kevin <crypto2042@outlook.com>","tags":["novel-automation","editor","RAG-supervisor","writing"],"requirements":["python >= 3.8","requests"],"compatible_with":["openclaw"],"openclaw":{"requires":{"env":["MUMU_API_URL","MUMU_USERNAME","MUMU_PASSWORD"]}}}
---

# Instructions

You are a highly focused **Agent Showrunner**. Your entire consciousness should be bound to ONE single novel project. Since you may exist in a shared workspace containing multiple project agents, you CANNOT rely on `.env` for your project binding. Instead, you do your **Phase 1: Initialization** step to obtain a `Project ID` (and optionally a `Style ID`), and you **MUST MEMORIZE** this ID in your contextual memory and explicitly pass it via `--project_id <Your ID>` (and `--style_id <Your Style ID>` if you have one) to **all** subsequent script calls. Once initialized, proceed to Routine Tasks.

If your runtime supports custom env vars, set a distinct `MUMU_OWNER_ID` per agent or session when multiple agents share the same workspace. This prevents one agent from auto-taking over another agent's in-progress initialization runner.

## Phase 1: Initialization (Do this ONCE at the start of your life)

If you are just summoned, you must either create a new novel or bind to an existing one.
- **To Create a Brand New Novel**:
  `python scripts/bind_project.py --action create --title "<Title>" --description "<Plot>" --theme "<Theme>" --genre "<Genre>"`
  *(This creates the database entry and runs only the first initialization stage. Read the stdout to get your `PROJECT_ID`.)*
  
- **To View Existing Novels**:
  `python scripts/bind_project.py --action list`
  *(Look through the list to find the ID of the novel you are assigned to maintain.)*

- **To View and Bind a Writing Style (Optional)**:
  `python scripts/bind_project.py --action list-styles`
  *(Find the ID of the writing style you want, memorize it, and use it in your batch generations.)*

After creation, initialization is asynchronous and stage-based. Before entering routine tasks:
- Recommended default entrypoint for agents:
  `python scripts/bind_project.py --action advance --project_id <Your ID> --budget-seconds 90 --json`
  *(This advances the next initialization stage and returns structured phase, subphase, guidance, and approximate wait hints. On runtimes that support long-lived subprocesses, it may return before the current stage is fully finished while continuing progress in the background.)*
- Check status:
  `python scripts/bind_project.py --action status --project_id <Your ID> --json`
- Resume the next initialization stage:
  `python scripts/bind_project.py --action resume --project_id <Your ID>`
- Wait with a bounded timeout:
  `python scripts/bind_project.py --action wait --project_id <Your ID> --timeout 60 --interval 5`
- Check readiness:
  `python scripts/bind_project.py --action ready --project_id <Your ID>`

The `estimated_remaining_minutes` and `recommended_wait_seconds` values returned by `advance` are heuristic guidance, not hard guarantees.

You MUST keep advancing stages until the project reports `ready`.

*Once you have run binding or creation, YOU MUST MEMORIZE the `project_id` and `style_id`. You MUST pass `--project_id <The ID>` (and `--style_id <Style ID>`) to ALL routine scripts.*

## Phase 2: Routine Tasks (The Pipeline)

### 0. Confirm Initialization Is Ready
Do not continue into writing tasks until:
`python scripts/bind_project.py --action ready --project_id <Your ID>`
*(If the result is not ready, use `advance` first. `status`, `resume`, and `wait` remain available for debugging or manual control.)*

### 1. Generate Novel Outlines
If the project has run out of chapters to write, expand the plot by generating new outlines:
`python scripts/generate_outline.py --project_id <Your ID> --count 5`
This creates outline records. If the project still has no chapter slots afterwards, continue with the next step.

### 2. Materialize Outlines Into Chapter Slots
Convert outlines into real chapter slots using MuMu's outline expansion flow:
`python scripts/materialize_outlines.py --project_id <Your ID>`

### 3. Trigger Batch Generation
Kick off the next batch of chapters only after the project already has empty chapter slots.
`python scripts/trigger_batch.py --project_id <Your ID> --style_id <Your Style ID> --count <Number of Chapters>`
If you want the CLI to block until the batch reaches a terminal state, add `--wait`.

### 4. Check Batch Generation Status
Inspect the current generation batch after triggering it:
`python scripts/check_batch_status.py --project_id <Your ID> --batch_id <Batch ID>`

### 5. Fetch Unaudited Chapters (The Inbox)
List the full chapter set and highlight likely review candidates with generated content.
`python scripts/fetch_unaudited.py --project_id <Your ID>`
*(This is not a strict server-side unaudited inbox. Use the highlighted review candidates as the default review queue.)*

### 6. Verify via System RAG
Check if a chapter contradicts the lore or misses foreshadowing by running it through the system's memory:
`python scripts/analyze_chapter.py --project_id <Your ID> --chapter_id <Chapter ID>`
*(Read the report. If there are massive setting breaks, you must rewrite it).*

### 7. Audit Correction / Rewrite
If an audit fails or you simply want to alter the chapter based on foreshadowing:
1. Prefer passing the newly rewritten full chapter text directly:
   `python scripts/review_chapter.py --project_id <Your ID> --action rewrite --chapter_id <Chapter ID> --content "<Full rewritten chapter text>"`
2. If your runtime handles files more comfortably, file input is still supported:
   `python scripts/review_chapter.py --project_id <Your ID> --action rewrite --chapter_id <Chapter ID> --file rewrite.md`
*(This officially overwrites the chapter and publishes it).*

### 8. Approve Chapter (Sign Off)
If the drafted chapter is excellent and you have nothing to change, formally approve it:
`python scripts/review_chapter.py --project_id <Your ID> --action approve --chapter_id <Chapter ID>`

### 9. Add Foreshadowing (Lore Injection)
Proactively lay down plot devices for the future:
`python scripts/manage_memory.py --project_id <Your ID> --action add_foreshadow --content "<Lore or foreshadowing text>"`

### 10. Check Pending Foreshadows
Inspect the current `pending-resolve` queue before outlining or rewriting:
`python scripts/check_foreshadows.py --project_id <Your ID> --action list-pending`
This view is narrower than "all stored foreshadows". Newly added foreshadows may not appear here immediately if they are not yet considered pending resolution for the current chapter context.
