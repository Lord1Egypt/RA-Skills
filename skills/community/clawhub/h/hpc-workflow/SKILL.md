---
name: hpc-workflow
description: Set up, adapt, operate or recover an agent-operated Slurm GPU workspace using bundled scripts, nested tmux, durable allocation requests, job-local storage and verified automatic backups. Use when asked to establish an HPC workflow or operate an existing installation.
license: MIT OR MIT-0
metadata:
  author: playeriv65
  version: "0.4.1"
  repository: https://github.com/playeriv65/hpc-agent-kit
---

# Agent-operated HPC workflow

Use a local coding agent with shell access, uv and a supported authenticated HPC
connection. This skill includes its runtime under `scripts/`, site templates
under `assets/` and operating notes under `references/`. Resolve this installed
skill directory; paths below are relative to it. No separate Git checkout is
required. Read [the operating contract](references/agent-contract.md) and
[runtime requirements](references/runtime.md). Verify packaged files with
`uv run --no-project --python 3.12 python scripts/verify_bundle.py`.

The deliverable is a working connection and operating contract for the user's
actual cluster. Keep private profiles, generated bundles and logs outside this
installed directory. Record the package/core versions and installed hashes in
the site's private notes. Reuse healthy existing installations for ordinary
operation; installing this skill does not authenticate to an HPC or request GPUs.

## Establish or adapt a site

Inspect the existing connection, jobs, tmux hierarchy and operator instructions
first. Reuse a supported installation where possible. Read
[persistent SSH](references/msi-persistent-ssh.md) when adapting
an MSI/Duo route or an always-on authenticated holder, then read
[site probing](references/site-probing.md) to establish the transport, Slurm/QoS
permissions, disk-backed local paths and persistent archive location. Unknown
facts stay unknown; idle hardware does not establish project access.

Create a private profile using the observed facts and the examples under
`assets/`. Select `direct-ssh` when login-to-compute SSH is proven, or
`psc-bridge` for PSC's allocation-terminal bridge. The profile renderer rejects
unfilled values, unverified local/persistent storage, non-isolated local paths
and QoS outside the project/partition intersection. These checks validate the
provided facts; they do not discover or independently prove those facts.

Run `uv run --no-project --python 3.12 python scripts/common/profile.py PROFILE.json
--output NEW_STAGING_DIRECTORY`. Inspect the generated profile and manifest.
`uv run --no-project --python 3.12 python scripts/common/deploy_bundle.py BUNDLE`
checks frozen bytes and shows its targets;
`--apply` installs through the profile's already-authenticated exec route after
quiescent-state checks, preserving old helpers and configuration. Use deployment
within the user's authorized setup scope. Do not publish private profiles.
For upgrades or failures, read [recovery](references/recovery.md); use the shared
transactional installer and its saved backup rather than ad hoc file replacement.

The adapters are templates, not a promise that every HPC has the same policy.
For unsupported schedulers, storage layouts, GPU keys or connection mechanisms,
adapt an isolated template and test it before replacing active helpers. Keep
toolchain versions and framework setup in explicit site/repository configuration;
do not carry MSI/PSC compiler choices to an unrelated cluster.

Read [acceptance](references/acceptance.md) and perform the applicable checks.
Write the site's operating notes with its supported entry command, paths,
resource defaults, recovery commands and exact verification limits. Preserve
the user's existing transport and research data. No human initialization wizard
is required: the agent probes, writes configuration, deploys and verifies.

## Operate and recover

The login tmux owns one `gpu-request` allocation pane. Each granted job owns
`gpu-JOB_ID` compute tmux with setup, autosave and named task windows. A transport
disconnect does not establish that Slurm released the allocation.

Persist an allocation request ID before submitting:
`SITE-gpu --request ID GPU_TYPE COUNT WALLTIME`. Reuse exactly that ID and
configuration after disconnects; `SITE-gpu allocation ID` reconciles the durable
record with Slurm. Reservation or submission uncertainty never authorizes another
ID. Inspect its log, named pane and scheduler evidence; preserve ambiguous records.
READY is historical bootstrap evidence, not a current health guarantee.

Use `SITE-gpu run --job JOB_ID --request TASK_ID --wait WINDOW -- COMMAND ...`
for experiments after bootstrap. A repeated task ID must retain the same job,
window and literal command. Do not create extra `srun` steps for ordinary work.
Use the repository's launcher to recreate environments and apply its toolchain.
Read [operating lessons](references/operations.md) when adapting desktop wrappers,
preparing an application's environment/caches or observing a job through its end.
It covers allocation namespaces, argument transport and workload readiness.

`SITE-agent-state status` reports queue, routes and allocation records.
`SITE-agent-state doctor` also checks current compute access, autosave process
identity, save freshness, current-writer identity and failure counts.
`doctor --verify-backup` additionally reads the full archive chain; use it for
acceptance or suspected corruption rather than routine high-frequency polling.
Doctor uses an isolated `hpc-health` task window and records, without altering
experiments. Unreachable, stale and unchecked are distinct from healthy.

Bootstrap restores and verifies before starting work, starts autosave and waits
for a successful current-writer save. Defaults are five-minute increments,
six-hour full compaction, and a save before Slurm's end time. Immutable generations
commit through an atomic pointer; corrupt latest generations fall back to verified
predecessors. Abrupt node loss can recover only already committed data.
Store checkpoints/results explicitly on persistent storage; snapshots exclude
`.venv` and large model caches. Never classify an incomplete checkpoint as resumable.

Normal monitoring reads status and logs. Allocation retries, authentication and
destructive recovery are separate decisions: do not send repeated MFA challenges,
cancel research jobs, discard uncertain records, reset live tmux, delete evidence
or overwrite checkpoints as an automatic response to a failed observation.
