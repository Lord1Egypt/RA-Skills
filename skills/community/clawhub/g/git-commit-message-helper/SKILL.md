---
name: git-commit-message-helper
description: >
  Suggest conventional-commit messages from a staged diff summary. Use when
  the user asks for a commit message after staging changes.
metadata: {"clawdbot":{"emoji":"💬","requires":{"bins":["git"]}}}
---

# Git Commit Message Helper

## Purpose / Overview
Produces a short conventional-commit subject (+ optional body) from changes.

## When to Use
- User says "write a commit message"
- After `git add`.

## Usage / Instructions
1. Prefer user-provided diff/stat; if missing, ask them to paste it or run `git diff --cached --stat`
2. Choose type: feat|fix|docs|refactor|test|chore.
3. Subject ≤ 72 chars, imperative mood, no trailing period.
4. Offer one primary message and two short alternatives.


## Examples
Input stat: "auth/login.ts | 12 +++++"
Output: `fix(auth): handle empty password field`

## Requirements / Dependencies
git (optional; only if the user wants you to run `git diff --cached --stat`).

## Limitations / Caveats
Does not commit or push.

## Security / Permissions
May run read-only git commands the user approves. No network.

## Description

Suggest conventional-commit messages from a staged diff summary.

## License or terms

MIT-0

## Use case

Who: anyone performing the workflow summarized as “Suggest conventional-commit messages from a staged diff summary”. Purpose: complete that workflow with guided steps from the `git-commit-message-helper` skill.

## Risks and mitigations

## References

- Git documentation: https://git-scm.com/doc

## Ethical considerations

Illegal use of this skill is not allowed. The publisher will not be accountable for outcomes arising from unlawful use under country or international law. Prohibited examples include breaking into accounts without authorization, deploying ransomware, and trafficking in stolen personal data. Misuse against third-party systems without authorization is illegal.
