# master-skill-review

A higher-privilege OpenClaw meta-skill for reviewing and improving other skills.

## What it handles
- checks whether a skill is too verbose
- finds steps that should be moved into scripts
- pushes toward lower token usage
- verifies boundaries between default actions and confirmation-required actions
- defaults to backing up the target skill before making review-driven changes

## Typical owner
Usually run by the **`master`** agent.

## Permission note
This skill may require elevated local access because it can inspect and modify other local skill folders, including `SKILL.md`, `references/`, and `scripts/`.

## Safe default
It prefers **thin markdown + heavier scripts**, and after review it should **back up first, then modify**, then show evidence of the change.
