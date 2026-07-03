# Synchronization

This skill intentionally exists in **two locations** in this monorepo:

1. `_meta-space/.agents/skills/kano-model-strategist/` — **source of truth**
   (authoritative; edit here first)
2. `_meta-space/projects/design-engineering-playbook/skills/kano-model-strategist/`
   — public release copy (in the `design-engineering-playbook` subrepo that
   ships to GitHub)

The reason for the duplication: the `design-engineering-playbook` subrepo is
itself a separate GitHub repo (`monikazapisekstudio/design-engineering-playbook`)
and is periodically snapshotted out of the monorepo. Skills intended for public
release live in `design-engineering-playbook/skills/`.

## How to keep them in sync

When you edit the skill:

1. Edit the **source of truth** in `.agents/skills/kano-model-strategist/`.
2. Run `node path/to/skill-creator/scripts/lint-skill.js .agents/skills/kano-model-strategist/`
   to confirm lint-clean.
3. Mirror the changes to `projects/design-engineering-playbook/skills/kano-model-strategist/`
   (Copy-Item -Recurse from PowerShell, or `cp -r` from bash).
4. Lint the public copy the same way to confirm parity.

A future improvement is a sync script. For now, manual mirror is fine — the
skill moves slowly and the chance of drift is low.

## What to NOT do

- **Do not edit the public copy first.** Edits must originate in the source of
  truth; the public copy is downstream.
- **Do not delete one copy "to dedupe."** Both copies serve different
  audiences: the source of truth is what the local Mavis agent runtime loads;
  the public copy is what GitHub users see. Removing either breaks that
  audience.
- **Do not symlink.** Windows symlinks for skill directories are flaky across
  Git, Drive, and OneDrive syncing. Two real copies is more reliable.
