# Packaged operating contract

## Deliver the user's working site

Read `../SKILL.md` to establish, adapt or recover an installation.
The output is an authenticated connection, reviewed private site profile,
installed helpers and a verified operating contract. Use the user's existing
route and authorization. Do not install an agent on the HPC or invent an
authentication mechanism. A natural-language setup request is the entry point.

Keep profiles, credentials, probe output and installed-site notes under `private/`
or outside the installed skill directory. Document observed login identity, authentication owner,
adapter, accounts/partitions/QoS, local and persistent paths, runtime requirements,
defaults, resource limits, installed version/hashes and recovery commands.
Separate verified facts from pending checks and requested resources from actual
grants. Validate compute capabilities on compute, not only on login nodes.

## Operating invariants

- Keep allocation ownership in login tmux and tasks in job-specific compute tmux.
  After bootstrap, route work through `SITE-gpu run`; do not create extra steps.
- Persist an allocation request ID before submitting. Replay that ID with the
  same parameters after a disconnect. An unknown scheduler result or ambiguous
  reservation must not produce another allocation or deletion of its record.
- Use stable task IDs and named windows. Inspect durable logs and completion
  records; a historical READY or running marker is not a current health check.
- Use the allocated route and repository launcher. Shared home/hostnames do not
  prove socket access; backup readiness does not prove application readiness.
  If a job leaves the queue, establish its terminal outcome with accounting.
- Use disk-backed, job-isolated local storage for environments and caches, and
  persistent storage for snapshots, results and complete checkpoints. Restore
  verifies before extraction; `.venv` is recreated with `uv sync --locked`.
- Check `SITE-agent-state doctor --verify-backup` when adopting a restored
  workspace. Distinguish `passed`, `failed`, `unknown` and `not_checked` checks.
  Workspace recovery does not resume an experiment unless it has a checkpoint.
- Use frozen bundles and the supported deployment helper for upgrades. Refuse
  live jobs, unresolved reservations and active archive writers. Retain the
  exact prior installation; inspect `deployment.json` after interruptions.

Read `recovery.md` for failure-specific actions.
Read `operations.md` for desktop transports,
compute environments, storage budgets and scoped job observation.
Preserve research jobs, uncertain records, archives and failure evidence. Do not
cancel unrelated work, overwrite checkpoints, retry MFA automatically or replace
a healthy transport. A user's setup/repair request authorizes ordinary scoped
installation; it does not authorize publication or unrelated cleanup.
