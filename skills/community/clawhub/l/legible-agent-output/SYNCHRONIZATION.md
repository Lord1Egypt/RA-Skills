# Synchronization

This skill intentionally exists in **two locations**:

1. `_meta-space/.agents/skills/legible-agent-output/` — **source of truth**
   (authoritative; edit here first)
2. `_meta-space/projects/design-engineering-playbook/skills/legible-agent-output/`
   — public release copy (in the `design-engineering-playbook` subrepo that ships
   to GitHub)

The reason for the duplication: the `design-engineering-playbook` subrepo is
itself a separate GitHub repo (`monikazapisekstudio/design-engineering-playbook`)
and is periodically snapshotted out of the monorepo. Skills intended for public
release live in `design-engineering-playbook/skills/`.

## How to keep them in sync

When you edit the skill:

1. Edit the **source of truth** in `.agents/skills/legible-agent-output/`.
2. Mirror the changes to `projects/design-engineering-playbook/skills/legible-agent-output/`
   (Copy-Item -Recurse from PowerShell, or `cp -r` from bash).
3. Confirm parity: frontmatter, body, references/, examples/ all match.

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

## Differences between the two copies

The two copies are **intentionally near-identical** but not byte-equal. The
playbook copy applies the playbook's `playbook/quality-requirements.md`
contract, which means the public copy's `SKILL.md` frontmatter is rewritten
to use the playbook's `model` / `compatibility` / `metadata` fields. The body
of the skill — the 7 laws, the 6-category taxonomy, the eval loop, the
references — is identical. The difference is the playbook contract overlay,
not a difference in the skill itself.

The public copy also has these additional files that the source-of-truth
copy does not, per the playbook's `quality-requirements.md` (FR-5):

- `ATTRIBUTION.md` — third-party source attribution
- `EVIDENCE.md` — Path B eval results
- `SYNCHRONIZATION.md` — this file
- `LICENSE` — MIT license file

These four files are pure playbook contract overhead. If you ever consolidate
the two copies, preserve the playbook contract on the surviving copy.
