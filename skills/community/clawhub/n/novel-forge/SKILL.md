---
name: novel-forge
description: Long-form novel workflow for creating, continuing, resuming, and repairing serialized fiction with externalized project state, role-to-model mapping, worldbuilding, character sheets, full outlines, 10-chapter batch outlines, style sampling, chapter drafting, consistency review, memory tracking, and spawned multi-session collaboration. Use when the user asks to start a novel project, continue or resume a draft, recover from truncation, assign models to roles, generate canon or chapters, review for consistency, or maintain a long-running fiction project across many chapters. Supports single-agent or multi-agent execution, with multi-agent as the default; when multi-agent is selected, first surface the available model inventory and the novel-writing role list, then ask the user for an explicit role→model mapping before any canon work. Once the user has provided the mapping, persist it in project state and drive stage work with `sessions_spawn` using the mapped roles rather than treating the mapping as passive metadata. The main session may only create the project shell and route work; it must not author canon files.
---

# Novel Forge

**Version:** v2.0.0

## Overview / 技能简介

Use this skill to run long-form fiction as a **stateful pipeline**, not as chat memory.
It helps with novel project setup, continuation, truncated recovery, model-role mapping, canon building, chapter drafting, and consistency review.

**中文卖点：** 让你用文件化状态稳定连载长篇小说，支持新建、续写、断档恢复和多角色模型分工。

## Quick start / 快速开始

### Startup order
1. Read `/root/.openclaw/openclaw.json`.
2. Collect the project brief first: title, genre/audience, target length or chapter count, taboo list, core premise, execution mode, and starting checkpoint or first scene.
3. Persist the project brief / scaffold before any role or model discussion.
4. Only after the project brief is saved, run `scripts/show_runtime_inventory.mjs` and show the user the available model inventory grouped by provider.
5. Show the novel-writing role list.
6. Produce a recommended role→model draft from the inventory and the heuristics below.
7. Ask the user to confirm or edit the draft mapping.
8. Do not present `agents_list` as a user-facing inventory; it is internal-only.
9. Treat `agents_list` as a visibility hint only; use an actual `sessions_spawn` probe to determine whether multi-agent execution is available. If the probe succeeds, multi-agent is available even when `agents_list` shows only `main`.
10. Do not start canon until title, genre/audience, target length, taboo list, premise, execution mode, and role mapping are confirmed.
11. Do not fan out dependent canon stages blindly. Worldbuilding must be stable before character sheets; worldbuilding + characters must be stable before the full outline; the full outline must be stable before each 10-chapter batch outline; batch outline must be stable before writer; writer before reviewer; reviewer before orchestrator.

### Inventory display rule
- Always present the model list before asking for role mapping.
- Always present the role list before asking for role mapping.
- Always prefill a recommended mapping draft based on the current inventory.
- Never show `agents_list` output as a selectable menu when it only contains `main`.
- If the model inventory cannot be read, stop and report the failure instead of guessing.
- Treat the role→model mapping as project state until the user confirms it, then use that mapping to drive `sessions_spawn` stage sessions.

### Dynamic mapping heuristics
Build the recommendation from the user’s actual inventory, not from a fixed global pairing.

1. Read the current model inventory.
2. For each role, score models using only the models the user actually has.
3. Prefer models whose names or metadata suggest the needed behavior.
4. If a model is ambiguous, keep it as a candidate instead of forcing a certainty.
5. Present the result as a recommended draft mapping plus alternates.
6. Ask the user to confirm or override any role that is still uncertain.

### Role scoring cues
Use the inventory metadata first, then model-family clues:
- planner / reasoner cues: planning, reasoning, thinking, structured, max, deepseek-thinking
- prose / style cues: opus, creative, prose, drafting, long-context, balanced writing
- review / consistency cues: critic, review, editor, check, correction, glm
- fast-draft cues: highspeed, lightning, speed, mini-max
- structured transform cues: coder, extract, tooling, schema

### Recommendation output
For each role, output:
- primary recommendation
- 1-2 fallback candidates from the same inventory
- short reason tied to the model name or available metadata

### Conflict rule
If the inventory does not make a role decision obvious, do not invent a certainty label. Mark it as "needs user choice" and keep the other roles prefilled.

### Role packet to collect
- title
- genre / audience
- target length or chapter count
- taboo list
- core premise
- execution mode
- starting checkpoint or first scene
- role→model mapping

Note: collect and save the project brief first, then ask for role→model mapping after the setup is persisted. After confirmation, persist the mapping and use it as the execution plan for spawned stage sessions.

### Novel-writing roles
- orchestrator / 总控
- worldbuilding / 设定
- character sheet / 人物
- outline / 全书大纲（先总纲，后 10 章一批细纲）
- style / 文风
- writer / 正文
- reviewer / 审稿
- recovery / 断档恢复

### Use examples
1. `帮我新建一个小说项目，题材是奇幻冒险，默认多 agent`
2. `继续写这本小说，从上次断开的地方接着写`
3. `从第5章恢复，并帮我检查当前角色和模型分工`

### User-facing prompts
- New novel: say `help me start a novel project` / `帮我新建一个小说项目`
- Continue novel: say `continue novel <title>` / `继续写《标题》`
- Resume a truncation: say `resume from chapter 3` / `从第3章断档处继续`
- If multi-agent is desired, present the model inventory and the spawn target that `sessions_spawn` will use before asking for mapping.
- If single-agent is desired, say so explicitly; otherwise multi-agent remains the default.
- If the model inventory cannot be read, stop and report the failure instead of guessing.

### Multi-agent execution flow
1. Save the project brief and confirmed role→model mapping in project state.
2. Verify spawnability by calling `sessions_spawn(runtime="subagent")`.
3. Create only the stage sessions that are currently unblocked by upstream canon. Do not spawn downstream stages before their prerequisites are accepted.
4. Use `mode:"session"` for reusable workers and `mode:"run"` for disposable checks.
5. Treat the returned `childSessionKey` as the session handle for follow-up.
6. Run stages in dependency order: worldbuilding → character sheet → full outline → 10-chapter batch outline → style → writer → reviewer → orchestrator.
7. If worldbuilding changes, re-open character, full-outline, and batch-outline assumptions before continuing.
8. If character or full outline changes, re-open batch-outline, style, and writer assumptions before continuing.
9. Keep the main session out of canon authorship; use it only to route, verify, and persist state.
10. After acceptance, write back the accepted canon slice, memory update, and workflow state.
11. If spawnability fails, report that multi-agent is unavailable and stop.

## 中文说明

这是一个给**长篇小说连载**用的技能。它会把小说状态放在文件里，而不是只靠聊天记录记忆。

你可以直接这样说：
- `帮我新建一个小说项目`
- `继续写《寄魂》`
- `从第5章断档处恢复`
- `帮我检查这个小说技能是否适合继续写`

如果你选择多 agent，系统会先让你确认角色和模型分工；如果你不特别说明，默认按多 agent 流程来处理。

## Core contract

- Keep the project state in files.
- Keep the main session lightweight.
- Use writer and reviewer stages for prose when multi-agent is active.
- Never let the main session silently author or rewrite canon prose.
- Never assume missing facts; read or ask.
- When multi-agent is selected, treat the role pipeline as mandatory, not optional.
- Apply the role pipeline to every stage: bootstrap, canon generation, style sampling, chapter drafting, review, recovery, and maintenance.
- Respect stage dependencies; do not parallelize work that consumes unstable upstream canon.
- For the exact main-session boundary, read `references/main-session-constraints.md`.

## Where state lives

Treat these as the source of truth:
- `project.json`
- `worldbuilding.md`
- `characters.md`
- `outline.md`
- `style.md`
- `memory.md`
- `chapters/*.md`
- `state/current.json` when present

Prefer `state/current.json` for fast recovery and chapter-boundary checks when it exists.

For the operational state machine and run order, see:
- `references/state-machine.md`
- `references/runbook.md`
- `references/schemas.md`
- `references/workflow.md`
- `references/main-session-constraints.md`

## When to use this skill

Use this skill when the user wants to:
- start a new long-form fiction project
- continue or resume a novel
- recover from a truncated or partial chapter
- assign models to orchestration/writing/review roles
- generate worldbuilding, character dossiers, outlines, or style samples
- draft chapters with consistency checks
- maintain memory and canon across many chapters

## Operating rules

1. If the request is a continuation/resume, discover candidate projects first and let the user choose when needed.
2. If multi-agent is active, inspect the current model inventory and ask for a role→model mapping.
3. Persist the chosen mapping in project state.
4. Verify which agent IDs are spawnable for `sessions_spawn`; do not use `agents_list` as a proxy for the model inventory or spawn capability.
5. If `sessions_spawn(runtime="subagent")` fails with a capability error, say multi-agent execution is unavailable in this environment and stop before canon work.
6. Confirm title, genre/audience, target length, taboo list, premise, execution mode, and checkpoint before canon generation.
7. Build canon in order: worldbuilding → characters → full outline → 10-chapter batch outline → style → chapters.
8. Do not parallelize phase 0 canon work if it depends on previous canon.
9. Draft one 10-chapter batch outline at a time.
10. In multi-agent mode, create stage sessions with `sessions_spawn` using the user-confirmed role→model mapping, then run the appropriate stage agents in order; for prose stages this is writer → reviewer → orchestrator.
11. The main session must not author stage content itself in multi-agent mode; it may only route work, verify outputs, and write state back.
12. If a spawned stage cannot run, report the missing capability rather than improvising that stage in the main session.
13. In single-agent mode, keep the same state-machine discipline but collapse the writing stages into one controlled pass.
14. After acceptance, sync chapter summary, memory, and state together.
15. Do not skip stage agents during bootstrap, recovery, or maintenance just because no prose is being written; if a stage has a designated agent/role, invoke it.
16. Never use the main session to synthesize canon from user facts into final set pieces when a dedicated stage exists; route to the stage agent instead.
17. If provenance is missing or ambiguous, stop.
18. During project bootstrap, you may reshape user-provided setting material into cleaner canon, but do not invent major plot facts or overwrite the user’s intent.
19. In review/cleanup passes, preserve user-intended sensitive tags or labels as part of the project’s canon when they are meaningful to the request (e.g. NSFW, R18, taboo, possessive, adultery, etc.). Only remove or rewrite the hard-blocked details themselves; do not delete the tag/setting wholesale, and do not over-prune unrelated canon unless the user asks.

## Anti-drift rules

- Use only the smallest relevant canon slice.
- Prefer explicit character states and open loops over implied memory.
- Keep style rules compact and persistent.
- Treat reviewer output as required, not optional.
- If provenance is missing or ambiguous, stop.

## Writing constraints

Default all prose stages to:
- concrete actions
- body language
- sensory detail
- character-specific diction
- scene-local observations

Avoid:
- template transitions
- repetitive contrast formulas
- abstract summary piles
- explanatory filler
- symmetrical machine-like paragraphs
- explanation-style contrast clauses like “不是X，而是Y”, “不是……是……”, “不只是……更是……”. Treat these as disallowed in prose unless a reviewer explicitly needs one for clarity in dialogue or very tight prose.

Prefer showing over stating: let the reader infer the contrast from action, sensation, or image instead of summarizing it with a paired negation.

## Output shape

For planning tasks, output a compact structure such as:
- Project brief
- Model assignment
- Canon status
- Full outline / batch outline
- Risks / conflicts
- Next action

For writing tasks, keep stages distinct:
- Chapter goal
- Chapter writer draft
- Review notes
- Revision summary
- Memory update

## Failure behavior

- If a required fact is missing, ask.
- If the resume checkpoint is unclear, stop.
- If the reviewer has no draft, treat the workflow as incomplete.
- If the main session is about to write the chapter directly in multi-agent mode, hand off to the writer stage instead.

## Resources

Read the referenced files only when needed:
- `references/state-machine.md`
- `references/runbook.md`
- `references/schemas.md`
- `references/workflow.md`
- `references/prompts.md`
- `references/examples.md`
- `scripts/build_context_pack.py`
- `scripts/discover_projects.py`
- `scripts/scaffold_project.py`
