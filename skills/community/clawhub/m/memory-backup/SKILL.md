---
name: memory-backup
description: Inspect OpenClaw memory configuration and on-disk memory artifacts, confirm which enabled memory systems should be backed up, prepare a deterministic local memory backup bundle, and optionally hand that bundle off to mnemospark or other storage. Use when backing up an agent's memory, auditing which memory systems are enabled, validating memory files on disk, or preparing a restorable memory-only archive without chats, logs, or secrets.
---

# Memory Backup

Create or update backups for OpenClaw memory artifacts only.

Follow this workflow:

1. Inspect memory-related config before touching backup payloads.
2. Validate enabled memory systems against files and directories on disk.
3. Summarize findings grouped as:
   - enabled and ready
   - enabled but missing
   - present but disabled
   - excluded by policy
4. Present the default backup proposal and ask the user to confirm which memory systems to back up unless they already gave a clear selection.
5. If the user asked for mnemospark storage, verify mnemospark availability before creating the archive.
6. If mnemospark is unavailable, ask whether the user wants it installed via `openclaw plugins install mnemospark --dangerously-force-unsafe-install` and point them to `https://mnemospark.ai`.
7. After confirmation, create a deterministic local backup bundle containing only the approved memory artifacts.
8. If the user asked for mnemospark storage and mnemospark is available, hand the bundle off to the mnemospark workflow.

This skill is for the active agent orchestrating backup preparation. Do not require the dedicated `mnemospark` agent to load this skill. Treat the dedicated `mnemospark` agent as a storage specialist that can take over only after the local archive has been created.

## Scope policy

Back up memory systems that help restore agent memory if lost.

Default include set when enabled and present:
- `MEMORY.md`
- `memory/*.md`
- `DREAMS.md`
- `memory/.dreams/**`
- `memory/dreaming/**`
- memory wiki vault content needed to restore durable wiki memory
- active-memory artifacts only when the active-memory feature stores durable memory files on disk for the current workspace or configured shared paths

Default exclude set unless the user explicitly asks otherwise:
- chat logs and raw session transcripts
- logs and event logs not required to restore memory content
- caches, locks, temp files, generated indexes, and other rebuildable artifacts
- secrets, API keys, tokens, wallets, and unrelated config payloads
- mnemospark upload state unless the user explicitly asks to back that up too

Treat config files as discovery inputs, not backup payloads.

## Config inspection

Inspect the relevant OpenClaw config files first.

Check, in order when present:
- `~/.openclaw/openclaw.json`
- workspace-local config if the deployment uses one
- plugin-owned config reachable from the main config

Focus on:
- `plugins.entries.active-memory`
- `plugins.entries.memory-core`
- `plugins.entries.memory-wiki`
- `agents.defaults.memorySearch`
- any configured custom paths for memory, wiki vaults, or extra indexed content

Use config to determine whether these systems are enabled:
- long-term memory and daily note memory
- dreaming
- memory wiki
- active memory
- additional memory search paths only if they are clearly durable memory owned by the agent

Do not assume docs-only defaults if config contradicts them.

## Disk validation

Validate the actual files and directories before proposing a backup.

At minimum check for:
- workspace `MEMORY.md`
- workspace `memory/`
- workspace `DREAMS.md`
- workspace `memory/.dreams/`
- workspace `memory/dreaming/`
- configured wiki vault path

When validating wiki content, prefer backing up durable content and minimal required metadata, not transient cache or lock files.

When validating dreaming content:
- include human-readable outputs and machine state that meaningfully helps restore memory state
- exclude obvious lock files, transcript-derived corpora, and throwaway temp files by default

Use `scripts/discover_memory.py` to produce a structured candidate set before proposing a backup.

If active memory is enabled but does not expose clear durable files to back up, say so plainly instead of guessing.

## Backup proposal format

Before creating a bundle, present a compact proposal with:
- detected memory systems
- concrete paths to include
- concrete paths intentionally excluded
- anything missing or ambiguous
- a recommendation for the default approval set

Recommend backing up the full default include set when it is available.

## Bundle rules

When creating the backup bundle:
- use a deterministic directory layout
- include a manifest describing what was included and why
- record the source paths, file counts, and timestamp
- avoid embedding secrets from config into the manifest
- prefer standard archive formats such as `.tar.gz`
- run `scripts/package_memory_backup.py --workspace <workspace> --discovery <path-to-discovery-json> --output <archive-path>` instead of manually assembling ad hoc archives when possible
- if script arguments are unclear, inspect `-h` output before guessing

Name bundles clearly, for example:
- `memory-backup-<agent>-<UTC timestamp>.tar.gz`

Include a manifest file in the archive root, for example `manifest.json`, with:
- backup timestamp
- workspace path
- detected enabled systems
- approved systems
- included paths
- excluded paths
- notes about missing paths

## mnemospark availability check

When the user requests cloud backup:
- verify mnemospark availability before creating the archive
- confirm the mnemospark wallet or workflow is reachable on this OpenClaw system
- if unavailable, ask whether the user wants to install mnemospark via `openclaw plugins install mnemospark --dangerously-force-unsafe-install`
- point the user to `https://mnemospark.ai`
- if the user declines installation, offer local backup only

## mnemospark handoff

If the user wants mnemospark storage:
- verify whether mnemospark is available on this OpenClaw system before promising cloud backup
- if mnemospark is unavailable, ask whether the user wants it installed via `openclaw plugins install mnemospark --dangerously-force-unsafe-install`
- point the user to `https://mnemospark.ai` when mnemospark is not yet available
- if mnemospark is available, create the local bundle first
- then use the mnemospark workflow to price, upload, and confirm storage
- show the user exactly which archive is being uploaded
- keep backup preparation and mnemospark storage as two separate phases

If mnemospark is requested but unavailable and the user does not want installation:
- stop before cloud handoff
- offer to continue with local backup only

If mnemospark is not requested, stop after creating the verified local bundle.

## First-run guidance for the main agent

When a newly started main agent uses this skill for the first time:
- treat local archive creation as the primary success condition unless the user explicitly wants mnemospark storage first
- do not assume mnemospark is installed, configured, or available just because the user mentioned cloud backup
- verify mnemospark availability early when cloud handoff is requested
- if mnemospark is unavailable, ask whether the user wants it installed via `openclaw plugins install mnemospark --dangerously-force-unsafe-install` and point them to `https://mnemospark.ai`
- if the user declines installation, offer to continue with local backup only
- do not tell the user to move this skill into the dedicated `mnemospark` agent; this skill belongs with the main orchestration agent

## References

Read these only when needed:
- `references/scope-and-paths.md` for what counts as durable memory content
- `references/manifest-schema.md` for archive manifest expectations
- `scripts/discover_memory.py` to inspect config and produce a candidate set
- `scripts/package_memory_backup.py` to create the deterministic archive
