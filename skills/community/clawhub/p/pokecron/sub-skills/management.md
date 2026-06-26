# Management — inspection, history, presets, tones

## Inspection

```bash
poke --list --channel CH --target TGT --agent AG    # active reminders in scope
poke --latest --channel CH --target TGT             # detail of the most recent
poke --show ID                                      # full detail of one
```

All three scope filters are optional. Use them when there are many
reminders and you only want the relevant slice.

## Resolution

```bash
poke --confirm ID         # mark confirmed (terminates one-off, advances recurring)
poke --cancel ID          # terminate permanently
poke --cancel-all         # terminate every active reminder
```

These bypass the reply classifier (no need for `--reply`). Use them
when the operator (you, the agent, or a script) needs to clear state
directly — not when a user's chat message arrives (that's `--reply`).

## History & stats

```bash
poke --history [N]        # tail last N lifecycle events (default 50)
poke --stats              # active count + history aggregates + mean confirm latency
```

History is append-only `.runtime/history.jsonl`. Events:

- `created` — new reminder scheduled
- `delivered` — agent received a delivery request
- `confirm` / `cancel` / `snooze` / `followup` — user reply matched
- `followup_fired` — unconfirmed-followup actually fired
- `suppressed` — a gate (DND, quiet hours, etc.) blocked a delivery

Records persist past `--cancel` / `--confirm` — the state file is gone
but the history line stays.

## Dry-run

```bash
poke <create-args> --dry-run
# DRY-RUN would-create type=remind schedule=… channel=… target=… …
```

Validates and prints what *would* be scheduled. Writes nothing to disk,
no scheduler unit, no state file. Use to sanity-check exotic flag
combinations before committing.

## Catchup behaviour

When the machine missed fires (sleep, off, suspended):

- `--catchup replay` / `--persistent` — re-run every missed occurrence
  up to `--max-catchup-runs` (default **10**, cap **64**).
- `--catchup coalesce` (default for calendar) — collapse all missed
  into a single fire.
- `--catchup none` / `--flippant` — drop missed fires.

## Tones

14 built-in: `absurdist`, `bored`, `calm`, `chaotic`, `default`,
`detached`, `helpful`, `loving`, `mean`, `passive`, `playful`, `solemn`,
`stern`, `warm`. List them with `poke --tones`.

```bash
poke --tone "warm" ...                      # one tone
poke --vector-tones --tone "anxious" ...    # opt-in ollama embedding match
```

Comma-list of tones rotates across escalation levels — see
`escalation.md` for the rotation rules. Tones live in `tones/`.
`--vector-tones` is opt-in semantic matching; it POSTs the tone/intent
text to `OLLAMA_URL` (loopback by default — non-loopback endpoints
require `POKE_ALLOW_REMOTE_OLLAMA=1`) and caches embeddings plus source
text to `.runtime/tone-embeddings.json`.

## Presets

```bash
poke --presets                              # list available
poke --preset morning-plan ...              # use a preset (other flags merge over it)
```

Built-in: `daily-standup`, `morning-plan`, `trash-day`, `water-break`.

Live in `presets/`. A preset just expands into the same flags you could
pass directly — handy shortcut, no magic.

## Path sets

Named groups of file paths for use in agent task prompts (gets expanded
into a context block).

```bash
poke --paths-save morning-plan --file ~/notes/today.md --file ~/notes/this-week.md
poke --paths-show morning-plan
poke --paths-list
poke --paths-delete morning-plan
```

In a `--task` prompt, `{{paths:morning-plan}}` expands to a newline-joined
list of the saved paths (one `- /absolute/path` per line) — it does NOT
read the files. The downstream agent decides whether to open them.

## State layout

```
.runtime/
  state/
    tr-YYYYMMDD-HHMMSS-<rand>.json   # one per active reminder
    commitments.json
    visibility.json
    path-sets.json
    .flood.json                       # rolling delivery timestamps
    .mock-scheduler.json              # only when POKE_SCHEDULER_BACKEND=mock
  history.jsonl                       # append-only lifecycle log
  hook-log.jsonl                      # append-only --pre-cmd/--post-cmd output
  openclaw-compat/                    # temp config files (auto-cleaned)
```

`POKE_STATE_DIR` overrides the state directory; `POKE_RUNTIME_DIR`
overrides the parent. Test isolation: set both to a tempdir.
