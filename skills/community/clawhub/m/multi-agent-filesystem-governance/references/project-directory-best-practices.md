# Project Directory Best Practices

Use this file when deciding where long-lived code repositories should live versus where temporary verification work should happen.

## Core rule

Use a dedicated long-term project root for real code repositories.

Default recommendation:

- `~/projects/<repo>` for active, durable code projects

Use temporary locations only for short-lived validation, reproduction, or one-off experiments.

## Recommended split

### Long-lived project repositories

Put active repositories that may be maintained, tested, released, or revisited into:

- `~/projects/<repo>`

Why:

- stable path for repeated work
- separate from agent runtime/config directories
- separate from temp cleanup risk
- easier to back up, monitor, and document

### Temporary verification work

Put throwaway clones, fast reproduction attempts, and one-off debugging into:

- `/tmp/...`

Why:

- easy to discard
- low commitment
- useful for isolated experiments before deciding a repo deserves a durable home

Do not leave the only important copy of a project in `/tmp`.

## What to avoid for long-term repositories

Do not keep formal project repositories long-term in:

- agent runtime/config trees such as `~/.openclaw/...`
- skill directories
- download folders
- note or knowledge-vault directories
- generic temp/scratch directories

These locations are better suited to runtime state, skills, intake, notes, or disposable work—not stable project ownership.

## Promotion rule

A good default workflow is:

1. use `/tmp/...` for quick reproduction or trial edits
2. once the work becomes ongoing, move or re-clone into `~/projects/<repo>`
3. keep future testing, release work, and maintenance in the durable project root

## Multi-agent guidance

For multi-agent environments:

- use `~/projects/<repo>` as the stable project root when a repository is meant to persist
- keep agent-private scratch files in private workspaces, not mixed into the project root unless they are project-relevant
- use temp clones for risky or disposable experiments when you do not want to disturb the durable repository

## Fast decision table

- **Need a real home for an active repo** -> `~/projects/<repo>`
- **Just reproducing or testing quickly** -> `/tmp/...`
- **Agent runtime/config/state** -> keep in runtime/config directories, not project roots
- **Downloaded but untriaged archive or zip** -> intake/download area first, not `~/projects` yet

## One-line rule

Use `~/projects` for durable code projects and `/tmp` for temporary experiments.
