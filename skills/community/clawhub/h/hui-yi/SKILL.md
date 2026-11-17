---
name: "hui-yi"
description: "Use for low-frequency archival recall when primary memory is insufficient, authorized cold-memory maintenance, or setting up and repairing automatic user-memory detection and recall. Historical wording alone does not authorize writes; frequent facts belong in primary memory."
allowed-tools: Read Write Edit Bash(python:*) Bash(python3:*) Bash(node:*)
---

# Hui Yi

Hui Yi manages the cold reinforcement layer under `memory/cold/`.

Core rule:

**Repeatedly reactivated information deserves reinforcement first. Ebbinghaus sets the pace, not the sole trigger.**

## Use Hui Yi when

- answering the user's request needs older low-frequency context that current conversation and primary memory cannot supply
- the user authorizes archiving a durable lesson, decision, troubleshooting result, or stable low-frequency background note
- the user requests cold-memory review, index repair, metadata cleanup, or retrieval-quality maintenance
- an already-authorized maintenance workflow calls for cooling selected durable daily-note content
- the user asks to set up or repair automatic user-memory detection, primary-cache recall, or the native integration

Recall order: current conversation → recent daily notes / primary memory → relevant tooling notes / learnings → cold memory only if archival context is still needed. Phrases such as “之前”, “回忆一下”, or “do you remember” do not independently select this skill or authorize a write. Read the index and a few relevant notes before opening more archive content.

Follow the user's response language. Chinese examples and schedule messages are examples, not a language requirement; prompt templates are configurable.

## Do not use Hui Yi when

- the content is today's transient note → `memory/YYYY-MM-DD.md`
- the content is a stable high-frequency fact → `MEMORY.md`
- the content is tooling, machine path, or environment setup → `TOOLS.md`
- the content is a fresh mistake or still-unvalidated lesson → `.learnings/`
- the content contains secrets, tokens, or passwords

## Boundary

OpenClaw primary memory handles:
- current chat continuity
- recent daily notes
- stable high-frequency facts
- tooling and environment notes
- fresh learnings

Hui Yi handles:
- low-frequency, high-value knowledge under `memory/cold/`
- historical context that keeps resurfacing across real conversations
- durable experience, decisions, and troubleshooting notes that should not pollute primary memory

## Automatic user memory

For “自动检测用户的记忆信息”, read `references/native-memory.md`. Use the host's native capture and recall pipeline for frequent facts. The optional legacy hook does not provide reliable automatic collection on stock OpenClaw 2026.9.5. Cold-memory search can be selected when the conversation needs archival context; the user need not name this skill or use a slash command.

`scripts/configure_native_memory.py` previews a conservative webchat-only integration. `--apply` changes the existing host config only after the audited runtime and persistent adapter are verified; it backs up the config with its access permissions, enables native dreaming and adapter recall, keeps cross-peer conversation recall off, and disables the direct built-in Active Memory entry plus the old hook. The adapter refuses unverified host upgrades, so replacement of host files cannot remove its scope checks. Native dreaming runs background models and may promote supported facts into primary memory. Consult the reference for source trust, timing, cost, excluded channels, and upgrade safeguards.

Never claim a memory is saved merely because a candidate was detected. Verify the persisted evidence; prefer newer explicit corrections and keep dated states historical.

## Files and scripts

Cold-memory area:
- `memory/cold/index.md`
- `memory/cold/tags.json`
- `memory/cold/retrieval-log.md`
- `memory/cold/_template.md`
- `memory/cold/schedule.json`
- `memory/heartbeat-state.json`

Select the narrowest operation needed:
- `scripts/search.py` / `scripts/review.py resurface`: read and rank relevant notes; `--full-text` search returns matching note text.
- `scripts/create.py`: create an authorized cold note and rebuild metadata. Use the semantic fields in `templates/note-template.md`; replace placeholders with supported facts.
- `scripts/validate.py --strict`: check note and index structure without repair.
- `scripts/rebuild.py`: rewrite index/tags and update heartbeat state from existing notes.
- `scripts/annotate_primary_cache.py`: preview a source-hash-bound annotation plan for existing `MEMORY.md`/`USER.md` bullet entries. `--apply` adds native trigger metadata only after protected backups; it does not create facts or inflate repetition counts. Use only within an authorized primary-cache repair, with facts checked against their sources and newer corrections.
- `scripts/review.py feedback` / `session`: record actual usefulness and review outcomes; do not invent review counts. `resurface --write-signals` is an explicit write option.
- `scripts/decay.py --dry-run`: preview overdue-review and verification-staleness maintenance. Apply only within an authorized maintenance task; `--rebuild` synchronizes metadata after application. Age does not automatically demote memory state.
- `scripts/cool.py status`: read cooling state; `scan` and `done` update heartbeat state and require an authorized cooling workflow.
- `scripts/scrub_metadata.py --dry-run`: preview legacy session-identifier cleanup; omit `--dry-run` to apply the authorized cleanup.
- `scripts/scheduler.py --preview`: inspect candidate ranking; this does not register a schedule or send a message.
- `core/openclaw_signal_hook.py` / `core/openclaw_runtime_probe.py`: explicitly test the adapter; use `--dry-run` to avoid signal writes and `--stdin` for message text when practical. The probe calls the adapter in process.
- `scripts/install_hook.py --dry-run`: preview optional hook installation; running without `--dry-run` installs files, and `--enable` also updates existing OpenClaw configuration.
- `scripts/smoke_test.py`: read-only validate/search/scheduler smoke against the selected archive, using fixed Python child commands. Use the test suite for isolated regression coverage.

Core modules:
- `core/safe_fs.py`: shared Python file boundary and atomic writes
- `core/signal_detect.py`
- `core/signal_pipeline.py`
- `core/openclaw_signal_hook.py`
- `core/openclaw_runtime_probe.py`
- `templates/hook/safe-fs.ts`: shared TS hook file boundary; package/install it alongside `handler.ts`

## Disclosure

- Loading this skill does not install a hook, enable background collection, register a schedule, or authorize cooling. Keep writes within the user's requested task or existing explicit maintenance authorization.
- Normal archive operations use `memory/cold/` and `memory/heartbeat-state.json`; explicit CLI path overrides select other local resources. Context-file inputs, optional hook files/logs, and OpenClaw configuration are additional declared resources. Archive scripts do not transport data over a network or extract credentials. Native integration invokes host-configured model/embedding services and reads/rewrites the potentially credential-bearing `openclaw.json` with `--apply`; the legacy installer does so with `--enable`. Never package the private config backups.
- The hook is optional and twice opt-in: `scripts/install_hook.py` copies files
  into `hooks/hui-yi-signal-hook/`, and only `--enable` flips the two
  `hooks.internal.*` keys in `openclaw.json` (after printing a disclosure; it
  refuses to create a missing config file).
- The enabled hook accepts a trusted host Hui-Yi selection or an explicit text command at the very start of mapped `context.body`: `/hui-yi <query>` or `/hui_yi <query>`. The command is case-insensitive, requires an ASCII space/tab separator and a nonempty query, and is stripped before matching. Leading whitespace, quoted/embedded/prefixed/empty commands, and commands present only in `bodyForAgent` do not activate it. Ordinary recall wording remains ignored. Hosts must not copy user-controlled fields into trusted selection or workspace metadata.
- OpenClaw 2026.9.5's native preprocessed-event mapper supplies no skill-selection metadata. The text-command path works only when the mapped body begins with that command; providers may wrap bodies and native slash-command handling may consume commands before this hook. Use the explicit CLI/adapter where that occurs. Isolated mapper-shaped tests are not channel end-to-end verification.
- Hook persistence uses activation counters and truncated SHA-256 session fingerprints. Normal and debug hook logs exclude raw bodies, identifiers, metadata, note titles/paths, and matching terms; debug adds lifecycle/count diagnostics only. Logs rotate at 256 KB. Python diagnostics also exclude raw query/session and overlap terms by default; intentionally requested retrieval results may contain note titles, paths, and text.
- Detector/pipeline `--include-sensitive` explicitly includes raw query/context and matching terms for local diagnosis. Do not use it with secrets or shared logs. Neither option exposes raw session keys; adapter/probe outputs remain limited to counts, status, safe errors, and a session hash.
- `review.py feedback --query/--action` deliberately persists those values in `memory/cold/retrieval-log.md`, separately from diagnostic logging. Supply a short, non-sensitive retrieval topic/action; safe diagnostics do not redact this requested archive record.
- Filesystem helpers require ordinary files/directories, reject symbolic links, junctions/reparse points, hard links, and special files, and recheck file identity. Python uses staged atomic replacement, copying an existing Windows file's DACL to the empty staging file before writing data. TS uses staged atomic replacement on POSIX and for new Windows files; existing Windows files use a verified file descriptor to preserve their DACL, with best-effort rollback on failure. That Windows TS update is not crash atomic. These application checks are not a kernel sandbox against a hostile same-account process concurrently replacing directories; use a trusted, OS-owned workspace.
- The archive is shared across a workspace. Session fingerprints support deduplication, not per-user authorization or tenant isolation. Separate trust domains need host-enforced workspace separation.
- `allowed-tools` and `manifest.yaml` disclose intended operations; they do not enforce an OS/runtime access-control policy.
- The cooling playbook's routing table (MEMORY.md, TOOLS.md, .learnings/,
  AGENTS.md, SOUL.md) is agent guidance. Archive scripts do not write those files;
  the separately authorized `annotate_primary_cache.py --apply` can append
  retrieval annotations to verified existing `MEMORY.md`/`USER.md` bullets.

## Sanity check

```bash
python -X utf8 -B -m unittest discover -s tests
node --experimental-strip-types --test tests/hook_security.test.mjs
```

## Status check

For a requested status check, validate the selected archive, run its smoke check when useful, and preview scheduler candidates. Inspect the host's hook status through an authorized host interface when runtime status matters. Distinguish offline test success from verified live hook behavior. A failing read-only check does not authorize index repair, installation, or configuration changes.

## Release provenance

Source version: **1.2.13**, a security, compatibility and recall upgrade. See [release notes](references/release-1.2.13.md). Registry installation metadata is not part of the source package; verify publication and independent audit status at the registry.
