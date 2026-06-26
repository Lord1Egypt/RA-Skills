---
name: "git_commit_pr_workflow"
description: "Use when the user wants the full git workflow: branch creation if needed, commit, push, and PR create or update with a concise summary and test plan."
---


# Git Commit PR Workflow

Use this skill for end-to-end git delivery from working tree to pull request.

## Workflow
1. Inspect branch state, diff against default branch, and existing PR state.
2. Create a feature branch if still on the default branch.
3. Stage and commit the relevant changes.
4. Push the branch.
5. Create or update the PR with a short title, summary bullets, and test plan.

## Guardrails
- No destructive git commands unless explicitly requested.
- No force push to default branches.
- Keep PR titles short and bodies structured.
- Avoid committing secrets or unrelated changes.

## Example Requests
- Commit this work, push it, and open a PR.
- Take the current changes to a polished PR with a test plan.

## Inputs
- Current git state
- Default branch
- Optional user instructions

## Outputs
- New commit
- Pushed branch
- Created or updated PR

## Success Criteria
- The right files were committed.
- The branch was pushed safely.
- The PR body accurately reflects the diff.

## Non-Goals
- Force-push workflows by default
- Interactive git rebases

## Source Provenance
Derived from `src/commands/commit-push-pr.ts`.
