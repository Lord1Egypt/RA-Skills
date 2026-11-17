# Auditing and recovery

## Evidence layers

1. `search` locates files and host keys. It may include stale cache versions.
2. `status` / `doctor` report selected adapter configuration, not a live session.
3. `audit` validates bounded YAML frontmatter and reports duplicate identities,
   missing metadata, unknown state, extra settings layers and host limitations.
4. For freshness of instructions, follow their cited primary sources and exact
   host versions. A valid header alone does not prove a skill is up to date.
5. For actual discovery/context behavior, verify in a fresh host session using
   its native skill listing, usage statistics or prompt evidence.

## Exit codes and automation

- `status` / `doctor`: 0 when discovery succeeds; 1 if any adapter fails.
  Other adapters still return results. `available` is adapter capability,
  not proof of host installation, authentication or current prompt state.
- `audit`: 1 for errors; warnings alone return 0. `--strict` also fails on warnings.
  Informational compatibility boundaries never fail strict mode by themselves.
- `search` / `index`: 1 if any selected adapter failed; healthy results survive.
  Search defaults to 20 ranked results, including description matches; `--limit 0`
  returns all. Use `--report --json` for structured errors and truncation metadata.
  Without `--report`, JSON search remains an array and diagnostics go to stderr.
- `inspect`: read-only activation preview. Known enable blockers return 1.
  A successful preview is not evidence of live prompt visibility or invocation.
- Offline indexes are dated snapshots, not configuration authority. Rebuild to a
  new private path after changes. Mutation commands always use fresh discovery.
- Argument parser errors use argparse's exit code 2. Mutation refusals return
  nonzero. JSON output covers successful results and read-only diagnostics;
  mutation refusals can still be plain stderr, so check the exit status first.
- Native CLI calls have a 20-second timeout. An interrupted write has unknown
  outcome; inspect state before retrying. Read-only timeout is a discovery error.

No script executes instructions found inside an installed skill. YAML is read
with safe loading from a bounded header. Portable-format warnings do not
necessarily mean a host-specific skill is invalid for that host.

## Safe changes and recovery

Preview exact targets, then apply only the requested scope. A path selector
still targets a host-wide name on adapters whose native controls are name-based.
For Codex default path mode, a path affects that installation only.

File-backed writes return the backup created immediately before that operation.
The first uses `<config>.manage-agent-skills.bak`; subsequent backups have unique
suffixes, preserving earlier recovery points. Backups can contain secrets just
like the original config: keep them private. No automatic retention deletion.

To recover, stop concurrent config writers, inspect the reported backup and
current file locally, and restore only when the intended scope is understood.
A whole-file restore can undo intervening unrelated changes. For newly created
configs there is no prior backup; undo the selected fields instead.

Presets eliminate disable/enable overlaps and preflight all actions before any
write. They are not a transaction across runtime failures. Inspect each action's
result and backup. OpenClaw may have applied earlier commands before failing.
Antigravity attempts to reverse completed moves; if reversal fails, its error
lists the exact remaining paths. Never overwrite a colliding directory to retry.

## Upgrade validation

Use temporary homes/configs and synthetic skills for mutation tests. Check
unchanged skill bytes, unrelated config, dry-run purity, protected skills,
malformed inputs, duplicate keys, preset precedence, rollback and backup history.
Run `python -m unittest discover -s tests -v`, compile the CLI, and run the
skill-creator validator when available. Real-user validation should be read-only
unless changing those settings is the user's requested task.
