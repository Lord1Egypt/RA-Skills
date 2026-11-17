---
name: perfect-handoff
description: Reconcile project knowledge, write a compact continuation handoff, and print a ready-to-paste new-session prompt. Use when asked to close out a project and hand it to a fresh session; do not trigger for ordinary implementation, code cleanup, or copy editing.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
metadata:
  version: "1.0.1"
---

# Perfect Handoff

Complete project knowledge closeout, a compact handoff document, and a ready-to-paste opener in one workflow. The new session restores and reports first, then waits for the user's next instruction.

## Select a mode

- **Closeout and handoff** (default): perform the steps below, editing project documentation only within the user's authorization.
- **Restore only**: when explicitly asked to resume, do not reconcile or write files. Read the compact handoff within its bounded-read contract, verify relevant current state, report, and wait.
- If the project root is unknown and cannot be inferred from the current directory, ask for it. Do not audit the whole workspace.

## Closeout workflow

1. **Inventory**: read the effective project rules; inspect project identity, Git state if present, the existing short handoff, and documentation indexes. Mechanically enumerate Markdown while excluding dependency, build, and cache directories. Start with indexes and task-relevant sections; do not load every file in full. In a non-Git directory, rely on file evidence and do not claim a Git snapshot.
2. **Reconcile**: read [closeout.md](references/closeout.md) only for this closeout step. Check affected documents against verified implementation and current state. Update confirmed stale facts in their existing authoritative files. Mark unresolved conflicts for follow-up. A test pass is not proof of deployment or natural runtime acceptance.
3. **Choose the entrypoint**: reuse the existing compact handoff when possible. If none exists, use the project's docs convention, or create `HANDOFF.md` at the root. When an existing handoff is long and contains unique history, preserve it and create `HANDOFF_START.md` as the short recovery map. Read any same-name file before editing. Preserve historical evidence and paths. Keep one designated start entrypoint; point from other entries to it.
4. **Capture the necessary state**: use the [template](assets/handoff-template.md) for the current goal, acceptance conditions, decisions, authorization boundaries, relevant uncommitted changes and ownership, blockers, one primary next action, prerequisites, validation, and targeted references. Fill every section with current facts, explicit unknowns, or not-applicable. Never infer missing chat history. Timestamp and source every status snapshot. Keep secondary unfinished work in a concise index rather than silently dropping it.
5. **Compress and review**: target 2,000–4,000 characters for the handoff, with a 6,000-character maximum. Do not add filler to a shorter adequate handoff. Remove repetition and process narration first; convert secondary detail into `question → file → section/symbol/search term → when to read`. Keep key constraints, blockers, decisions, current changes, and prerequisites in the handoff itself. If it still exceeds the limit, report that budget and completeness did not both pass; never truncate key information or claim completion. Update a current snapshot, not an appended session diary.
6. **Deliver**: fill in the actual absolute project root and handoff path in the template's new-session prompt. Reopen the file and run the read-only checker: `python3 <skill-dir>/scripts/check_handoff.py <handoff-path> --project-root <root>`. Do not perform the next task recorded in the handoff. Keep the handoff document in the project, report the closeout in the original conversation, and show the full paste-ready prompt there; a file link alone is not the deliverable.

## Final response in the original conversation

Use these two sections only; do not paste the full handoff, history, or test log:

1. **Project closeout**: summarize the changes and checks, unresolved or unverified items, and handoff path and character count. List cleanup candidates that were not authorized for removal. If any required part remains open, label the closeout partial.
2. **New-session handoff prompt**: show the complete prompt with the real project root and handoff path filled in, in a copyable code block. The user can paste it into a fresh session for this same project. Do not substitute a link to a prompt file or create a new session automatically.

File writing and checker output are supporting steps. The user's deliverable is the closeout and complete prompt in the original conversation.

## New-session reading contract

- Read at most 12,000 characters of the handoff and supplementary material proactively in the first turn. Start with the compact entry; add at most one located excerpt if required. Inspect file size and search before reading, control output length, and record paths, sections, and character counts.
- Follow active mandatory project rules even if they exceed the controllable budget; identify visible size risks. If a key prerequisite exceeds the budget, report the gap and pause dependent conclusions. Never skip a required constraint.
- Do not expand every link, read long specifications, goal plans, handoffs, chats, or logs in full, or rerun the closeout during recovery.
- Every later read must answer a concrete question: search, then inspect only the relevant excerpt. Do not reread unchanged material. A truncated result cannot prove full acceptance.
- Verify project identity and relevant changes. Tests, deployments, and runtime statements in the handoff are dated snapshots. Recheck only the state required for the first task; do not automatically start broad tests, collection, deployment, or production probes.
- Briefly report the goal, current facts, blockers or conflicts, first recommended task, and its acceptance condition. Then wait for the user's instruction. Historical authorization does not authorize a new external or destructive action.

## Boundaries and completeness

Before calling the handoff complete, ensure the next agent can determine what to do and why, the constraints and protected changes, what remains unknown, the first action, how to validate it, and when to stop. A necessary fact cannot be hidden only in a generic link.

By default, do not change product code, delete or bulk-replace important files, change persistent data, write long-term memory, install dependencies, commit, push, publish, deploy, or send messages. List unauthorized cleanup only as a candidate. Respect any other authorization the user gives and local safety rules. An incomplete closeout can still produce a handoff, but label it partial.

The checker validates structure, length, placeholders, and explicit local link existence. It cannot prove semantic completeness, authorization, or runtime facts. Character limits are not token counts. Do not promise to prevent all automatic context compression. If a short handoff is still followed by rapid compression, inspect mandatory rules, tool descriptions, carried history, and large outputs separately.

See [NOTICE.md](NOTICE.md) for attribution and license provenance.
