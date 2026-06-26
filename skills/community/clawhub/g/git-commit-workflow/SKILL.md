---
name: "git_commit_workflow"
description: "Use when the user wants a single clean commit created from current changes with safe staging, message drafting, and non-interactive git usage."
---


# Git Commit Workflow

Use this skill when the task is to create one commit from current work.

## Workflow
1. Inspect git status, diff, branch, and recent commit style.
2. Stage only relevant changes.
3. Draft a concise commit message that reflects why the change exists.
4. Create a new commit non-interactively.
5. Report the resulting commit summary.

## Guardrails
- Never amend unless explicitly asked.
- Never bypass hooks unless explicitly asked.
- Avoid staging secrets or unrelated files.
- Do not create an empty commit.

## Example Requests
- Make one clean commit from the current working tree.
- Stage the right files and create a proper commit message.

## Inputs
- Current diff
- Branch state
- Recent commit style

## Outputs
- One non-amended commit
- Accurate commit message

## Success Criteria
- Only relevant changes were committed.
- No empty commit was created.
- Hooks and safety rules were respected.

## Non-Goals
- Amend flows unless explicitly asked
- Committing secrets or unrelated changes

## Source Provenance
Derived from `src/commands/commit.ts`.
