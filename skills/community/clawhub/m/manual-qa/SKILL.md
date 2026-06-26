---
name: manual-qa
description: Generate a manual QA checklist from code changes. Use when the user wants to test a PR, commit, branch, or staged changes — or says "QA this", "test plan", "what should I test", "manual testing", or asks how to verify a change works. Also use when reviewing a PR and the user wants to know what to check before merging.
---

# Manual QA

Generate a step-by-step QA checklist from code changes, separating what the agent can verify in the terminal from what needs a human.

## Determine the change source

Use the first match:
1. **Argument is a PR URL or number** → `gh pr diff`
2. **Argument is a commit SHA** → `git show`
3. **Staged changes exist** → `git diff --cached`
4. **Current branch differs from main** → `git diff main...HEAD`
5. **Unstaged changes exist** → `git diff`

If nothing matches, tell the user there are no changes to QA.

## Analyze the changes

Read the diff carefully. Understand what the change does — not just what files changed, but the intent. Look at:
- What behavior is being added, modified, or removed
- What inputs the changed code accepts
- What side effects it has (API calls, file writes, database changes, UI updates)
- What could go wrong

## Output the QA checklist

Produce a numbered list of concrete test steps. Each step should be specific enough that someone unfamiliar with the code could follow it. Group by feature area if the change spans multiple concerns.

For each step, mark it:

- **🤖 Agent can test** — The agent can run this in the terminal right now. CLI commands, scripts, API calls with curl, file assertions, running test suites, checking build output.
- **👤 Human must test** — Requires a human. Interactive prompts (TTY-dependent), authenticated web sessions, visual/UI verification, multi-step flows across web + email + mobile, anything needing a browser the agent doesn't control, real-device testing.

Include both:
- **Happy paths** — the change works as intended with normal inputs
- **Error paths** — bad inputs, missing config, network failures, edge cases, permission errors

## Offer to run agent-testable steps

After presenting the checklist, offer to run all 🤖 steps. If the user agrees, run them and report results inline — pass/fail for each, with output on failure.

## Keep it practical

- Don't generate steps for things the diff clearly doesn't affect
- Don't suggest running the full test suite unless the change is broad — suggest targeted tests
- If the project has a test command (in package.json, Makefile, etc.), use it
- For bug fixes, include a step that reproduces the original bug and confirms it's fixed
- For new features, include a step that exercises the feature end-to-end
