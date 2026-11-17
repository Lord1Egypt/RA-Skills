# Parallel Worker Orchestration

## Contents

- Enablement and Orchestrator role
- Lanes and worktrees
- Worker/Reviewer pairing
- Integration and cleanup

## 1. Enablement

Parallel execution is off by default. Enable it only after user confirmation and only when the task has clear write lanes.

Do not parallelize these areas merely for speed:

- one persistence model and its migration;
- one registry, shared configuration, lockfile, or generated surface;
- one transaction, finalizer, or Release path;
- a shared design that remains open;
- a consumer that requires an unfinished provider API.

Run them serially or finish the provider first.

## 2. Orchestrator responsibilities

The current task acts as Orchestrator and:

- freezes parts, dependency graph, Worker/Reviewer pairing, and write scope;
- prepares worktrees/branches or shared-tree ownership;
- dispatches each Worker GOAL;
- receives blocker, pause, completion, and integration receipts;
- maintains root GOAL and coordination records;
- integrates reviewed outputs and runs integration validation;
- closes worktrees and branches.

By default, fork every Worker from one frozen planning boundary. After each Worker reads its package, code, and validation boundary, it creates a full-history inherited Reviewer before implementation. Fixed, fresh, or `self_review` modes are explicit overrides; see [session-topology.md](session-topology.md).

The Orchestrator normally has no active Goal and does not occupy an execution loop merely to wait. Respond to task messages or state receipts.

For multi-slice programs, the Orchestrator normally does not write slice product code. Delegate the current slice to one bounded Worker, keep shared public assembly and integration with the Orchestrator, and overlap only these independent activities:

- current-slice implementation;
- read-only planning of the next slice after its provider contract is frozen;
- implementation-independent Reviewer readiness;
- parallel comprehensive and focused review of one frozen candidate when the risk profile justifies both.

Do not split a single transaction, persistence authority, schema mutation, state machine, or tightly coupled test-first contract across multiple Workers. This creates merge and review overhead rather than useful concurrency. A second product Writer requires exact disjoint write scopes and dependency-free behavior.

When the Orchestrator owns Reviewer creation instead of the Worker, create the Worker and Reviewer contexts from the same frozen pre-implementation planning boundary. Reviewers receive design, baseline, validation scope, and later the exact candidate, but never the Worker's implementation reasoning. Record the alternative lineage explicitly.

## 3. Lane definition

Each lane declares:

- Worker, Reviewer, requested models/reasoning, enforcement methods/status, and receipts;
- assigned work items;
- impact scope and exact write scope;
- shared hotspots and no-touch scope;
- provider/consumer dependencies;
- branch, worktree, and baseline;
- validation and delivery commit;
- pause gates, notification targets, and completion conditions;
- task IDs, session modes, fork sources, and pre-execution fork point.

No lane starts from a merely planned or confirmed model. Each Worker and Reviewer context must first have an `enforced` creation, handshake-plus-dispatch, current-task, or explicit-subagent receipt. Nested subagents need separate receipts; the lane task's configuration does not configure them implicitly.

Allow only one writer for a file or business object in one coordination window. Do not review a range while its Worker is still changing it.

## 4. Worktree choice

Prefer isolated worktrees when:

- multiple Workers write code;
- lanes need independent baselines or commits;
- the shared checkout contains other active changes;
- review needs exact branch state;
- merge order is part of the task.

A shared tree is acceptable only when project rules require it, write scopes are fully disjoint, shared files are frozen, and one integrator owns commits.

## 5. One-to-one review

By default, pair each parallel Worker with an inherited pre-execution Reviewer. Explicit `self_review` lanes create no separate Reviewer and must label their receipts accordingly. One independent Reviewer may sequentially inspect unrelated lanes but may not review a range it implemented or integrated.

Each lane uses:

- `goals/<worker>.md`;
- `execution/<worker>.md`;
- `review/<reviewer>.md`.

Workers write only their lane records. The Orchestrator alone writes root GOAL and `coordination/**`.

## 6. Integration

A lane is ready only when:

- every work item is `approved`;
- the exact commit is recorded;
- its worktree is clean;
- no blocking finding remains;
- upstream dependency versions are explicit.

Integrate in dependency order. Conflict resolution is integration work owned by one integrator. Rerun focused validation affected by a conflict and re-review the new snapshot when necessary.

## 7. Cleanup

Clean a lane only when:

- its commit is integrated, or the user explicitly keeps an isolated branch;
- integration validation passes;
- the worktree is clean;
- evidence and sensitive configuration are archived according to policy;
- the user did not request preservation.

By default, remove integrated local task branches/worktrees and return to the original main branch. Never delete an unmerged, dirty, running, or still-reviewable worktree.
