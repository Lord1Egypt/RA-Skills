---
name: git-bisect-coach
description: >
  Guide an interactive git bisect to find the commit that introduced a bug.
  Use when a regression appeared between two known commits or tags.
metadata: {"clawdbot":{"emoji":"🔎","requires":{"bins":["git"]}}}
---

# Git Bisect Coach

## Purpose / Overview
Walk the user through `git bisect` with clear good/bad labels, consistent
reproduction steps, and a clean abort path.

## When to Use
- "Worked on Monday, broken on main now"
- A good tag/commit and a bad tip are known
- The failure can be reproduced with a clear pass/fail

## Usage / Instructions
1. Confirm a clean worktree (or stash/commit first). Dirty trees confuse bisect.
2. Collect **bad** revision, **good** revision, and **reproduction steps**.
3. Start the session:
   ```bash
   git bisect start
   git bisect bad <bad-rev>
   git bisect good <good-rev>
   ```
4. For each checkout git presents:
   a. Restate the reproduction steps briefly.
   b. Ask: good, bad, or skip (untestable)?
   c. Map the answer to `git bisect good`, `git bisect bad`, or `git bisect skip`.
5. Track progress if git prints remaining steps; otherwise estimate with
   `git rev-list --count good..bad` when the user can share it.
6. When finished, summarize the first bad commit hash and subject, then:
   ```bash
   git show <commit>
   git bisect reset
   ```
7. If each step needs a build, write a tiny fixed checklist so every iteration
   stays comparable (install, migrate, smoke).
8. Early stop: `git bisect reset` and keep notes of the last tested commit.
9. Do not suggest `reset --hard` or `push --force` unless explicitly requested
   with clear understanding of impact.
10. Optional automation: sketch `git bisect run ./smoke.sh` with exit codes
    0 = good, 1 = bad, 125 = skip.

## Examples
User: "1.2.0 good, main bad; login redirect fails."
→ Provide start commands, then per-step reminders for the login test.

## Requirements / Dependencies
- Local `git`
- A reproducible pass/fail check owned by the user

## Limitations / Caveats
- Untestable mid-range commits need `skip`
- Does not modify remotes

## Security / Permissions
Suggest read-only git commands by default. Never push. Do not read or print
credential helpers or tokens from git config.

## Description

Guide an interactive git bisect to find the commit that introduced a bug.

## License or terms

MIT

## Use case

Who: anyone performing the workflow summarized as “Guide an interactive git bisect to find the commit that introduced a bug”. Purpose: complete that workflow with guided steps from the `git-bisect-coach` skill.

## Risks and mitigations

## References

- Git documentation: https://git-scm.com/doc

## Ethical considerations

Illegal use is not allowed. Activity that violates national statutes or international norms is unacceptable; The publisher will not be accountable for illegal use. Do not use this skill for stalking, doxxing, or other privacy invasions that break the law. Do not use outputs to commit fraud or deceive regulated processes.
