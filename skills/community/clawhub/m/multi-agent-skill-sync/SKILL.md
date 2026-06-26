---
name: skill-sync
description: One source of truth for local AI agent skills: audit Codex, Claude, OpenClaw, OpenCode, workspace skills, and shared roots; score hygiene, diff conflicting installs, deduplicate into one canonical source, and migrate the same layout across machines with restorable backups.
homepage: https://github.com/LearnPrompt/skill-sync
---

# Skill Sync

## When To Use

Use this skill when the user wants to:

- scan local skills across Codex, Claude, OpenClaw, OpenCode, workspace `./skills`, and shared roots
- see which skills are `shared`, `duplicate`, `compatible`, `specific`, or `mixed`
- choose one canonical source and replace duplicate copies with symlinks
- preview or apply convergence onto one preferred root such as `~/.agents/skills`
- export a portable layout manifest and import the same topology on another machine
- restore a previous dedupe or import run

Do not use this skill when the task is only about one host and no cross-host comparison or symlink management is needed.

## Fast Path

Scan the machine and get the hygiene score plus recommended actions:

```bash
python3 scripts/skill_sync.py
```

List only shared and host-specific skills:

```bash
python3 scripts/skill_sync.py --status shared,specific --list-names
```

Inspect one conflicting portable skill:

```bash
python3 scripts/skill_sync.py --diff rapid-ocr
```

Preview safe dedupe:

```bash
python3 scripts/skill_sync.py --dedupe --strategy strict
```

Preview a single-root convergence plan:

```bash
python3 scripts/skill_sync.py --adopt-root agents
```

Apply convergence with backups:

```bash
python3 scripts/skill_sync.py --adopt-root agents --apply
```

Restore the latest run:

```bash
python3 scripts/skill_sync.py --restore latest
python3 scripts/skill_sync.py --restore latest --apply
```

## Workflow

1. Scan first.
   Run `python3 scripts/skill_sync.py` and read the hygiene score and recommended actions.
2. Review risky groups before mutation.
   Use `--status compatible --list-names`, `--status mixed --list-names`, and `--diff <skill>`.
3. Preview convergence.
   Use `--dedupe --strategy strict` for identical groups, or `--adopt-root <platform>` to converge around one root.
4. Apply only when the plan looks right.
   Add `--apply` to execute symlink creation or replacement.
5. Export or import machine layouts when needed.
   Use `--export-manifest` and `--import-manifest` for cross-machine reuse.
6. Restore from backup if needed.
   Use `--restore <run-id|latest>` and add `--apply` to roll back.

## Safety Rules

- The script always scans and reports before mutation.
- It only auto-links portable directory-based skills that contain `SKILL.md`.
- It never overwrites an existing destination without first moving it into `~/.skill-sync/backups/<run-id>/originals/...`.
- `--strategy strict` only dedupes identical portable skills.
- `--strategy prefer-latest` and `--strategy trust-high` may select the newest portable copy when content differs.
- `--restore latest --apply` replays the last backup manifest in reverse.

## Roots Scanned

- `<current-workdir>/skills`
- `~/.codex/skills`
- `~/.agents/skills`
- `~/.claude/skills`
- `~/.claude/skills/anthropic-skills/skills`
- `~/.config/opencode/skills`
- `~/.openclaw/skills`
- `~/.openclaw/extensions/*/skills`

## Status Model

- `shared`: the same real directory is visible from multiple hosts, usually through symlinks
- `duplicate`: multiple hosts have the same portable skill content, but not via the same real path yet
- `compatible`: multiple hosts have portable `SKILL.md` skills with the same name, but different content
- `specific`: the skill appears on only one host
- `mixed`: the same skill name exists on multiple hosts, but with different formats or incompatible content

If you need the detection details or compatibility notes, read [references/compatibility.md](./references/compatibility.md).
