# Changelog

All notable changes to the `interagent-queue` skill are recorded here.

This file starts at 1.3.0. Version **1.2.0** was published to ClawHub on **2026-07-22** from a
working copy that was not under version control — `interagent-queue` only entered git with the
repository combine (ADR-001 Phase 1, 2026-08-26), whose earliest commit postdates that release.
The 1.2.0 section below was therefore reconstructed by diffing the published package
(`interagent-queue-1.2.0.zip`, sha256 `8865544e…9ef0`) against the tree, not from history.

## 1.3.0 — "Registry identity, and a cursor that refuses to rewind" — FINAL under this name

> **This skill is renamed to `miab-observer` and continues there at 2.0.0.** 1.3.0 is the last
> release published as `interagent-queue`. Skill identity is keyed on the frontmatter `name`, so
> installs cannot follow a rename — `miab-observer` must be installed deliberately, and the
> script moved from `scripts/interagent_queue.py` to `scripts/miab_observer.py`, so cron
> `--command` lines need updating. On-disk state is keyed on `CLAW_HOME` / `LYRA_WORKSPACE` and
> carries over untouched. Migration steps are at the top of SKILL.md.
>
> Entries below this line, and the 1.2.0 entry, describe releases that shipped as
> `interagent-queue`. They are left under that name deliberately: they are a record of what was
> published, not of what the skill is called now.

First release since the skill entered version control, and the first published from the combined
`miab-broker` + `interagent-queue` repository.

### Fixed

- **A corrupt state file no longer replays the entire ledger.** `load_state()` swallowed every
  exception and fell through to the same `{"enabled": false, "last_processed_line": 0}` default
  it uses for a genuine fresh start. A truncated or malformed `queue_state.json` therefore
  rewound the cursor to 0 without a word, and the next `process` wrote every ledger record that
  had ever existed into the log. The failure mode duplicated the output this observer exists to
  produce, which is worse than not running.

  A missing state file is still a fresh start. A present-but-unusable one — unparseable, not a
  JSON object, or carrying a `last_processed_line` that is not a non-negative integer — now exits
  `1` with `{"ok": false, ...}` on stderr, rewinds nothing, and writes nothing. Recovery is the
  operator's deliberate choice: repair the file, or delete it to accept a full replay. Documented
  in SKILL.md §4.

  Present in 1.2.0 and every install since 2026-07-22.

### Changed

- **The closed-bottle message sink now lives here** (ADR-001 T23). `notify_closed_bottles.py` and
  `notify_closed_dryrun.py` moved from `miab-broker/scripts/`, where they had become tracked files
  during the repository combine. A delivery sink is a reader concern, and while the broker CLI
  never called them, a package containing a script that shells out to `openclaw message send`
  cannot honestly declare `network: []` — the broker's scoping of that claim to the CLI lived in
  prose, which no scanner reads. The broker's declaration is now true without qualification, and
  this skill declares the egress instead. Documented in SKILL.md §3a.

  Carried over from the broker's changelog, since the script moved: **`CLAW_CLOSED_TARGET` is
  required** and the notifier fails closed with `{"ok": false, ...}` and a non-zero exit when it
  is unset. The previous hardcoded channel-id default is gone — it was both a secret in committed
  text and a way to mistarget delivery on a host that never configured the notifier.

  This is a relocation, not the merge. The two sinks still keep separate cursors and separate
  dedup state; unifying them is ADR-001 item 7, still Phase 2. `notify_closed_dryrun.py` is still
  a separate script rather than a `--dry-run` flag (item 10).

- **The broker's agent registry is now authoritative for display names** (Q9). `who()` resolves
  through `agent-registry.json` first, falling back to this file's built-in `AGENT_MAP` only for
  agents that have never been registered, and lookups are case-folded to match the broker's
  canonical form. `AGENT_MAP` had duplicated the persona↔function mapping the registry owns since
  broker T14, and the copy silently fell back to the raw name on a miss — which is why `SPECTRE`
  and `ECHO` rendered inconsistently. Adds one env var, `CLAW_REGISTRY`, and one read-only file
  read; the registry is cached per process and never mutated.
- **Install paths in the documentation are no longer hardcoded.** The command examples said
  `python3 Skills/interagent-queue/scripts/interagent_queue.py`, which is correct only for one
  install layout. They now use `<interagent-queue>/scripts/interagent_queue.py`, resolved against
  wherever the skill is installed.
- **§3 no longer names host home directories.** The multi-platform note illustrated itself with
  two literal `/Users/<name>` paths. The point it was making — that every location resolves from
  the environment and nothing is hardcoded to a host — is now made without them.

### Added

- **Renderers for `authority-override` and `corrupt`.** An event type the writer can emit but the
  reader cannot render returns `None` from `format_event()` and is dropped by `collect_new()`, so
  an unrendered type is *invisible* rather than broken — no ordinary test catches it. `corrupt`
  shipped that way in broker 1.2.0; `authority-override` (broker 2.0.0, T15) came within a backlog
  note of repeating it. The repository's `tests/contract/` now derives the writer's event list from
  its own AST and asserts a renderer exists for each, so this class of gap fails CI instead of
  going quiet.
- **A `permissions` block in the frontmatter.** 1.2.0 declared none. Every environment variable
  either script reads is listed — `CLAW_HOME`, `LYRA_WORKSPACE`, `CLAW_LEDGER`,
  `CLAW_QUEUE_STATE`, `CLAW_QUEUE_LOG`, `CLAW_REGISTRY` for the log sink, and
  `CLAW_CLOSED_TARGET`, `CLAW_CLOSED_STATE`, `CLAW_CLOSED_ACCOUNT` for the message sink — along
  with the files read and written. A partial declaration would be worse than none: it is an
  assertion a scanner can falsify.
- **A non-empty `network` declaration**, covering the message sink's delegated egress. The
  notifier opens no socket itself; it shells out to `openclaw message send`, whose transport and
  destination are configured outside this skill. Declared anyway, because the skill does cause
  egress. The log sink — the default path, and all of `interagent_queue.py` — still touches
  nothing but the local filesystem.
- **A declared minimum `miab-broker` version: 2.0.0** (Q7). The floor is set by identity, not by
  the ledger format — the `displayName` and `aliases` fields `who()` reads were added by broker
  T14 in 2.0.0, and against an older broker every agent silently falls back to `AGENT_MAP`, which
  is the inconsistency the registry lookup exists to fix.
- **`skill-card.md` is now in the repository.** It shipped in the 1.2.0 package but existed
  nowhere in source, so publishing from a clean checkout would have dropped or regressed it.
- **This changelog.** Its absence is why the 1.2.0 baseline had to be recovered by downloading
  the published package and diffing it.

## 1.2.0 — published 2026-07-22

Reconstructed from the published package; no source history exists for this release or earlier.

Ledger observer over `miab-broker`'s append-only callback ledger, with a once-only cursor, the
`on` / `off` / `status` / `process` / `peek` command surface, `AGENT_MAP`-based display names, and
renderers for `create`, `forward`, `return`, `resolve`, `cancel` and `fail`. State at
`$LYRA_WORKSPACE/state/callbacks/queue_state.json`; log at `$CLAW_HOME/logs/interagent-queue.log`.
