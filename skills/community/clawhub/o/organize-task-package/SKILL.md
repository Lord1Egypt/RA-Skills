---
name: organize-task-package
description: Organize discussed or evolving development, repair, testing, research, migration, or complex operational work into an executable, resumable, independently reviewable task documentation package, then derive a launch configuration from the current request and relevant task-family history for user confirmation. Use when Codex needs to record a task, create a dated task directory, split verifiable work items, freeze implementation and validation plans, create GOAL documents, arrange or reuse Worker and Reviewer sessions, coordinate parallel worktrees, confirm execution settings, maintain execution receipts, or audit task completion. Do not use for a short one-off task that does not need durable records.
---

# Organize Task Packages

## Core principles

Manage one bounded task as one directory and keep these concerns separate:

- user discussion and frozen decisions;
- executable design and validation plans;
- factual Worker execution receipts;
- Reviewer or explicit self-review findings and verdicts;
- aggregate GOAL state.

Always follow the target repository's `AGENTS.md`, coordination files, branch rules, documentation-language rules, and latest user instructions. This skill supplies defaults; it does not override project policy.

## Select the output language

Keep this skill and all bundled resources in English. Select the language used for user-facing messages and generated task documents in this order:

1. explicit user instruction for the current task;
2. target repository or documentation-path language policy;
3. dominant language of the current conversation;
4. English as the fallback.

Use one language consistently across a task package unless the project requires file-specific exceptions. Preserve code identifiers, paths, commands, schema fields, model names, status values, and quoted source text in their original form.

Bundled templates are canonical English semantic scaffolds, not a mandate that generated documents remain English. When the selected output language is not English, localize every human-facing heading, explanation, placeholder, table label, and sample sentence before presenting the package as ready. Do not translate machine-readable identifiers such as `pending`, `implemented_pending_review`, `approved`, or `launch_config_status`.

## Determine the current action

1. If the user only requests discussion or analysis, continue discussing; do not create a directory or active Goal.
2. If the user explicitly asks to record, organize, or create task documents, create or update a task package without starting implementation automatically.
3. If the user explicitly asks to execute a referenced GOAL, let the assigned Worker create an active Goal and execute it.
4. If the user asks to audit an existing implementation, read the design, execution, review records, and current implementation; do not repair it without authorization.
5. Enable multiple Workers only after the user confirms a parallel launch configuration; otherwise use one Worker.

Never interpret the existence of `GOAL.md` as authorization to create an active Goal.

## Stage 1: Recover discussion facts

Before writing design documents:

1. Read the user's original requirements, material follow-ups, confirmed decisions, rejected alternatives, and boundaries from the complete conversation.
2. If context was compacted and the source task is readable, reread it. If it is unavailable, identify the missing evidence rather than inventing decisions from memory.
3. Inspect the target repository's current implementation, existing task records, coordination state, and `git status`; distinguish current facts from plans and historical behavior.
4. Record confirmed decisions, explicit non-goals, open questions, and evidence sources separately in `design/00_discussion-decisions.md`.
5. Write files only after the user authorizes recording. Do not promote an unaccepted proposal into frozen design.

Read [design-and-planning.md](references/design-and-planning.md) for the full decision and design rules.

## Stage 2: Close material design gates

Resolve ordinary local implementation details independently, but return to the user when any of these material choices remain open:

- durable schema, file layout, migration, or compatibility policy;
- names and basic parameters of important public APIs, Agent tools, or commands;
- cross-module ownership, authorization, safety boundaries, external state, or destructive behavior;
- a bug fix choice that changes intended product semantics rather than restoring already-frozen behavior.

Mark unresolved gates as `OPEN`. Do not proceed by inserting a temporary default.

## Stage 3: Create the task package

Use the local creation date and a stable slug by default: `YYYY-MM-DD_<task_slug>`. Freeze the date after creation. Let the user or project choose the parent directory; do not force `dev_docs/implementation`.

Prefer the bundled initializer:

```bash
python scripts/init_task_package.py \
  --parent <parent-directory> \
  --slug <task-slug> \
  --title "<task title>" \
  --part core="Core behavior"
```

The script path is relative to this skill directory and refuses to overwrite an existing directory. After generation, localize the scaffold to the selected output language and replace every placeholder with task facts. See [package-structure.md](references/package-structure.md).

Default single-Worker structure:

```text
YYYY-MM-DD_<task_slug>/
├── README.md
├── GOAL.md
├── design/
│   ├── 00_discussion-decisions.md
│   └── 01_<part>.md
├── execution/
│   └── worker-main.md
└── review/
    └── reviewer-main.md
```

Do not append execution results to design prose, and do not leave Reviewer findings only in chat.

## Stage 4: Split verifiable work items

Split by capability, defect, investigation question, or operational stage rather than arbitrary file boundaries. Each work item must include:

- a stable ID and target behavior;
- frozen decisions that govern it;
- current evidence or a failure reproduction;
- implementation or execution method and impact scope;
- validation assets to add or change;
- exact commands or observable evidence;
- acceptance criteria, non-goals, dependencies, and risks.

End each part with an integrated audit across its work items: combined behavior, adjacent risks, documentation, and stale symbol or entry-point residue. Read [task-profiles.md](references/task-profiles.md) for task-type adaptations.

Validation and review scope must be proportional to owned business risk. Do not add work items or tests solely for theoretically possible malformed inputs, extreme recursion or payload sizes outside the supported contract, impossible internal states, or failures owned by a lower-level library. Such cases become blocking only when an explicit acceptance criterion, realistic public input path, threat model, or observed failure makes them relevant.

## Stage 5: Maintain three-state GOAL truth

Each work item has exactly one state:

1. `pending`: implementation or execution is incomplete;
2. `implemented_pending_review`: the Worker completed it and recorded evidence, but the configured review mode has not approved it;
3. `approved`: the configured review mode approved an exact snapshot and the Worker applied that receipt to the GOAL.

With `reviewer_mode: inherited_subagent` (default), the Reviewer writes the verdict and notifies the Worker. With explicit `reviewer_mode: self_review`, the Worker writes a concise `SELF` receipt after checking scope, validation, and task-document coverage; do not describe that receipt as independent review. Mark `approved` only when the selected mode has an exact receipt. Never replace this state machine with binary checkboxes.

Use README only for navigation and derived status. Use GOAL as the aggregate state index and execution/review documents as evidence truth. Reconcile all three at every milestone.

## Stage 5.5: Derive and confirm the launch configuration

After the task documents, design gates, and validation plan are ready, do not immediately fork or execute. Derive a recommended configuration in this priority order:

1. explicit instructions in the current user request;
2. configuration already frozen in the current task package;
3. the most recent user-confirmed, successfully used Worker/Reviewer, model, and topology from the same project and task family;
4. project defaults;
5. skill defaults.

Inherit history only when the task family matches, sessions remain usable, no incompatible active Goal exists, and permissions and worktrees are compatible. Show each concrete value and its source. If a historical value is invalid, show the fallback reason instead of guessing silently.

Present one concise launch confirmation covering: single or parallel execution, current-session role, Worker and review mode, task/session construction, model inheritance or explicit overrides, GOAL, branch/worktree/baseline, review cadence, validation scope, commit/notification/cleanup policy, and external actions such as real providers, servers, migrations, Release, or push. Freeze and execute only after the user confirms the bundle or explicitly edits individual fields.

Use human-readable task titles or stable role labels in every user-facing launch summary. Resolve the Codex sidebar title when task tools expose it. Do not lead with opaque task, thread, host, or subagent IDs; keep those only in durable execution/review receipts for exact routing. If no title exists, derive a readable label such as `<task title> — Worker` or `<Worker label> / Pre-execution Reviewer`.

For every current-session, Worker, Reviewer, and Orchestrator entry, state its construction type and source explicitly. At minimum report: readable label; context kind (`current task`, `existing sidebar task`, `new sidebar task`, or `nested subagent`); session mode (`current_task`, `reuse_fixed`, `fork_current`, `fresh`, `isolated_subagent`, or another supported mode); whether it is reused, forked, or newly created; the source context it inherits; requested model/reasoning; and the enforcement/independence boundary. Never make the user infer topology from a role name alone.

Store a single-Worker configuration in the root `GOAL.md`. Store parallel aggregate settings in the root GOAL and per-lane settings in `coordination/lanes.md`. Read [launch-configuration.md](references/launch-configuration.md) for provenance, validity checks, and the confirmation format.

## Stage 6: Run the Worker and Reviewer loop

Defaults:

- Worker: `gpt-5.6-sol`, reasoning `high`;
- Reviewer mode: `inherited_subagent` by default. The Reviewer inherits the selected Worker's model and reasoning unless the user explicitly chooses another supported topology and configuration.

Treat role models as requested configuration, not as facts, until the target context accepts them. Enforce and record them as follows:

- `current_task`: record the actual model and reasoning; a turn cannot change its own model mid-turn;
- `fresh`: pass the confirmed model and reasoning when creating the task and record the accepted launch receipt;
- `fork_current`, `fork_worker_pre_execution`, `shared_planning_base`, or `reuse_fixed`: after selecting the target, send a short configuration-only liveness turn with the confirmed model and reasoning, wait for `READY`, then send the formal dispatch with the same explicit settings;
- `isolated_subagent`: for the default Reviewer, use full pre-implementation history and parent model/reasoning inheritance. For an explicitly different or blind Reviewer, use the confirmed finite/no-history construction and separate configuration receipt.

Do not silently fall back while claiming the confirmed configuration. If the target rejects the model/reasoning pair, reports a mismatch, or cannot provide the required isolation, stop before execution and return the discrepancy for a new decision. A separate Reviewer must remain independent of the implementation under review; `self_review` must remain explicitly labeled.

For a single Worker, choose among the supported topologies in [session-topology.md](references/session-topology.md). The default is a Worker-managed Reviewer subagent that inherits the Worker's complete pre-implementation history. Explicit `self_review` is also supported when the user does not want a separate Reviewer.

Choose the least expensive topology that preserves the confirmed auditability. In independent modes, a context may implement or approve a snapshot, never both. Explicit `self_review` permits the Worker to approve only with a labeled `SELF` receipt. A Reviewer subagent created after implementation is valid only when it inherits no implementation reasoning. Apply all role, isolation, selection, and lineage rules in [session-topology.md](references/session-topology.md).

Default single-Worker topology: after launch confirmation, the selected Worker reads the frozen package, project rules, current code, HEAD, and validation boundary. Before implementation reasoning, active Goal creation, or product writes, it creates a Reviewer subagent with full current history and no model/reasoning override, so the Reviewer inherits the Worker's configuration and pre-implementation understanding. Wait for `READY_REVIEW`, then implement and reuse the same Reviewer for exact-snapshot review and re-review. With explicit `self_review`, do not create a subagent; the Worker performs the concise receipt-based check itself.

### Risk-proportional review gate

Reviewers prioritize, in order: confirmed business behavior; durable state and recovery truth; authorization, identity, concurrency, confidentiality, and destructive boundaries; public contracts used by real consumers; then realistic negative inputs. Findings must state the violated owned contract, plausible reachability, evidence, and material impact.

- `P0` and `P1` findings are blocking when supported by evidence.
- `P2` is blocking only when it affects a supported or realistically reachable path, an explicit acceptance criterion, or a high-consequence invariant. Speculative or extreme long-tail `P2` observations are follow-up, not release gates.
- `P3` and optional defense-in-depth never block approval unless the task explicitly makes them acceptance criteria.

Do not require application code to wrap every lower-level parser, recursion, memory, or malformed-data failure. For example, thousand-level JSON nesting is non-blocking unless that shape is within documented limits, crosses a realistic untrusted boundary that the application owns, or has observed failure evidence. Prefer existing library limits and bounded public-input validation over speculative wrappers.

The initial review returns all material blocking findings together. Re-review covers accepted repairs and their immediate impact. Non-blocking observations are consolidated once as residual risk; they do not trigger repeated review turns, new abstractions, or expanded test matrices.

Execution loop:

1. The Worker rereads the task package, project rules, coordination state, current code, current HEAD, working tree, and validation boundary.
2. After explicit execution authorization, apply the confirmed review mode. By default the Worker creates the full-history pre-execution Reviewer subagent, records inherited configuration and `READY_REVIEW`, and keeps it available. In `self_review` mode, record that no subagent is created.
3. Only after the selected review-mode readiness receipt does the Worker create an active Goal referencing the assigned `GOAL.md` and begin implementation.
4. The Worker completes one item, self-checks it, and appends actual paths, deviations, commands, results, durations, commits, and residual risks to the execution record.
5. The Worker marks the item `implemented_pending_review` and invokes the selected review mode on the exact snapshot.
6. The inherited Reviewer writes an independent verdict, or the Worker writes a concise `SELF` receipt covering scope, validation, task-document goals, and residual risk. The verdict separates blocking findings from non-blocking follow-up under the risk-proportional gate.
7. The Worker fixes findings and repeats the selected check. After an exact approval receipt, the Worker marks the item `approved`.
8. After all items in a part are approved, run the part-level integrated audit.
9. After all parts pass, complete final validation, commit-scope inspection, document reconciliation, and cleanup.

Read [execution-and-review.md](references/execution-and-review.md) for exact responsibilities, receipts, and notifications.

## Stage 7: Coordinate parallel execution

Recommend parallelism when current task boundaries or validated same-family history support it, but enable it only after user confirmation. Without a confirmed parallel configuration, remain single-Worker. In parallel mode, the current session becomes an event-driven Orchestrator, normally without an active Goal or continuous polling.

For a long-lived multi-slice program, prefer a manager/worker pipeline when subagent capacity is available: the parent task acts as Orchestrator/Integrator and delegates each concrete implementation slice to a bounded Worker subagent or task. The Orchestrator should not also be the routine product Writer; it owns planning decisions, lane assignment, shared integration, progress truth, and user-facing gates. Keep one product Writer per shared transaction, schema, state machine, or tightly coupled file set. Add a second Writer only for proven disjoint ownership, not merely because a slot is free.

Pipeline roles instead of serializing all activity: pre-create implementation-independent Reviewers at the frozen pre-execution boundary; let a read-only Planner prepare at most the next slice while the current Worker implements; run non-overlapping Reviewer passes concurrently only after the candidate is frozen; and let the Orchestrator integrate approved output while the next bounded Worker is being prepared. Idle Reviewer capacity is not a reason to invent more findings or wider validation.

Add `goals/` and `coordination/` to parallel packages:

- give every Worker an independent GOAL, execution record, and one-to-one Reviewer record;
- freeze ownership, write scope, dependencies, shared hotspots, pause gates, and notification targets in `coordination/lanes.md`;
- record commits, merge order, conflicts, integration validation, and cleanup in `coordination/integration.md`;
- normally isolate code-writing Workers in separate worktrees/branches unless project rules and disjoint write scopes make a shared tree safe;
- let Workers notify the Orchestrator about cross-lane decisions, blockers, pauses, completion, and integration needs;
- fork each Worker from the same frozen planning boundary, then let it read its package/code and create its inherited Reviewer before implementation, unless `self_review` was confirmed;
- clean a worktree only after review, commit, clean-state verification, and confirmed integration. Preserve any unmerged or dirty lane.

Read [parallel-orchestration.md](references/parallel-orchestration.md) for the full protocol.

## Notification boundaries

- A Worker dispatched by another task must notify its dispatcher when coordination is needed and when it completes.
- A Worker operating directly in the user's current task reports normally to the user and does not message itself.
- Default to selecting or creating the Worker only after execution is authorized; then have that Worker create its Reviewer subagent at the frozen pre-execution boundary. Create separate fresh Reviewer tasks only when the confirmed topology selects them.
- Reuse a user-designated fixed Worker/Reviewer instead of creating duplicate equivalent sessions.

Use built-in Codex task tools for task creation, fork, read, wait, and messaging.
If a needed built-in tool is absent or explicitly reports that its handler is
unavailable, use `$codex-app-task-channel` as an optional installed fallback.
Record whether delivery used `steer`, `start`, `followup`, or `queue`; queue is
durable next-turn delivery and must not be reported as same-turn steer. After a
failed built-in mutation, verify task state before fallback so an uncertain
outcome does not create a duplicate task or message.

## Completion conditions

Claim completion only when all conditions hold:

- every work item is `approved`;
- every part-level integrated audit passes;
- execution and validation evidence is complete, with failures and interruptions preserved;
- current implementation or artifacts agree with the documents, and planned behavior is not presented as implemented;
- Git, worktrees, external runs, and sensitive data are closed within user boundaries;
- no blocking finding under the configured review mode remains open;
- GOAL, README, execution, review, and coordination state agree.

Use [observed-lessons.md](references/observed-lessons.md) as the final audit checklist.
