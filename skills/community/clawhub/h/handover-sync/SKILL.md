---
name: handover-sync
description: Summarize end-of-session development progress and sync project handoff documentation in Chinese or English. Use when the user asks to summarize today's changes, prepare a handover, update README and handover docs together, capture problems and TODOs before ending a session, or keep project context transferable for the next agent or teammate.
---

# Handover Sync

## Overview

Produce a concrete end-of-session summary grounded in the repository's actual changes, then update the project's handoff documents so another agent can resume work quickly.

Treat this as a documentation-sync workflow, not a chat summary. Write facts tied to files, behaviors, validations, and remaining risks.

## Language Policy

Choose the working language from the user's latest request:
- If the user asks in Chinese, write the summary and handover updates in Chinese.
- If the user asks in English, write the summary and handover updates in English.
- If the user explicitly requests bilingual output, provide both versions.

When touching an existing doc with a strong established language, preserve that document's language unless the user explicitly asks to switch or translate it. Do not silently translate old sections.

## Workflow

1. Identify the repo root and the effective summary date.
Default to the current local date unless the user asks for a different window such as "this week" or "since the last handoff".

2. Inspect existing handoff targets before writing.
Look for `handover.md`, `README.md`, and any directly related docs that explain run steps, TODOs, or known issues. If a required file does not exist, create it instead of silently skipping it.

3. Load the template that matches the working language.
- Chinese: `references/session_summary_template.md`
- English: `references/session_summary_template.en.md`

These templates define the minimum sections and quality bar. Do not compress them into vague bullets.

4. Gather evidence from the repo before drafting.
Use direct repo inspection instead of memory:
- `git status --short`
- `git diff --name-only`
- `git diff --stat`
- `git log --since "<date> 00:00:00" --oneline` when commit history matters
- targeted reads of `handover.md`, `README.md`, and the files changed today

If the directory is not a git repo, fall back to file timestamps, existing handoff history, and the files the user explicitly mentioned.

5. Derive the narrative from evidence.
Map real code and validation output into the template's required sections:
- session scope and goal
- current repository state
- actual problems encountered
- cause analysis and conclusions
- implemented fixes with file-level grounding
- validations actually performed
- environment assumptions and commands
- known pitfalls and rejected approaches
- resume guide for the next person
- remaining limitations and boundaries
- final product goal when discussed
- concrete next TODO items

6. Update documents together by default.
Unless the user explicitly narrows scope, update all of the following:
- `handover.md`
- `README.md` sections directly affected by today's conclusions
- any nearby TODO or runbook notes needed to keep the handoff accurate

Do not update only one file if the summary changes the project's current understanding.

7. Verify the docs after editing.
Read the changed sections back and check that they:
- mention concrete files, commands, failures, or behaviors
- distinguish verified facts from current judgment
- state what the next person should do first
- state which commands or setup steps were actually used
- call out unresolved issues explicitly
- leave enough context for a different agent to continue

## Writing Rules

Write in terms of observable facts. Avoid generic phrases such as "improved stability" unless the specific behavior and evidence are named.

Mark stopgap solutions clearly as MVP or temporary when they are not final production solutions.

When the user has already stated a long-term delivery target such as packaging, installer support, or a desktop release, record that target in the handoff instead of only the local patch.

If verification did not happen, say so explicitly and list what remains unverified.

If you considered multiple approaches, record which ones were rejected and why. This prevents the next person from repeating dead ends.

Always include enough repo-specific context that a new person can answer three questions quickly:
- What changed?
- What is still broken or risky?
- What should I do next, in what order?

## File Strategy

Use the repo's existing structure when present. If `handover.md` already contains historical entries, append or update it in-place instead of rewriting unrelated history.

Only touch the README sections that became stale because of today's findings. Keep README user-facing; reserve deep investigation details for the handoff unless the README truly needs them.

## Resources

### `references/session_summary_template.md`
Chinese handoff template.

### `references/session_summary_template.en.md`
English handoff template.

This skill intentionally does not require helper scripts. Use the model's normal repo inspection tools and the template above.
