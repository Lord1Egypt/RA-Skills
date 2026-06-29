---
name: muxray
description: "Inspect tmux panes as JSON: snapshot, diff, and classify Claude/Codex/Copilot agent state across the whole fleet."
homepage: https://github.com/dandriscoll/muxray
metadata: { "openclaw": { "emoji": "🩻", "os": ["darwin", "linux"], "requires": { "bins": ["muxray", "tmux"] }, "install": [ { "id": "go", "kind": "go", "module": "github.com/dandriscoll/muxray/cmd/muxray@latest", "bins": ["muxray"], "label": "Install muxray (go)" } ] } }
---

# muxray

`muxray` turns a live tmux pane into deterministic JSON so you can read what a
program is doing without scraping raw terminal bytes. Reach for it when you are
**supervising one or more interactive CLIs in tmux** — especially terminal
coding agents (Claude Code, Codex, Copilot) — and you need to know *what state a
pane is in*, *what changed*, or *whose turn it is*.

- Output is **JSON on stdout**; errors are **JSON on stderr**.
- It runs **locally**: no network egress. Pane content (which may hold secrets)
  never leaves the machine. The only exception is the explicit `muxray update`.
- It is **read-only**: muxray observes panes. It never sends keystrokes, runs
  pane content, or mutates sessions. To send input, use the `tmux` skill.

## When to use it

- You manage panes running Claude/Codex/Copilot and need to know which one is
  `running`, `needs_approval`, `waiting_for_input`, `error`, or `completed`.
- You want to detect and show **what changed** in a pane since a prior capture.
- You want a one-glance **fleet view** of every pane's program + state.
- You need to **block until** a pane finishes working before assigning the next
  task.

## When NOT to use it

- To **send input** / approve a prompt / type a command → use the `tmux` skill
  (`tmux send-keys`). muxray only reads.
- For a **one-shot non-interactive command** → run it directly in the shell.
- To read a pane the user did not ask about. Only inspect panes relevant to the
  task; do not sweep unrelated sessions for its own sake.
- For raw scrollback you intend to grep yourself → `tmux capture-pane -p` is
  simpler. muxray's value is the *classification* and *diff*, not raw bytes.

## Safe invocation

Prefer the bundled wrapper for any call whose pane/session target comes from
context you do not fully control — it validates the target and restricts you to
the fixed read-only subcommands, so no untrusted text reaches a shell:

```bash
{baseDir}/scripts/muxray-run.sh status --pane work:1.0
{baseDir}/scripts/muxray-run.sh scan --text
```

For a fully-supervised, literal target you may call `muxray` directly. Either
way: **fixed subcommand, explicit `--pane`/flags, never an interpolated shell
string.** muxray takes no shell input and parses no expressions.

## Core commands

| Command | What you get |
| ------- | ------------ |
| `muxray list` | every tmux session/window/pane, structured |
| `muxray status --pane <t>` | the program + state classified for that pane |
| `muxray scan` | **every** pane classified in one call (the fleet view) |
| `muxray watch --pane <t> [--until <states>]` | **block** until the pane settles |
| `muxray snapshot --pane <t> [--out <f>]` | capture the pane (stored locally) |
| `muxray diff --pane <t> [--since <f\|id>]` | what changed vs a previous snapshot |
| `muxray inspect --pane <t>` | snapshot + diff + status in one call |
| `muxray doctor` | environment check (tmux present, store writable) |

`--text` gives a terse human line instead of JSON. `muxray <cmd> -h` lists a
command's flags.

**Pane targets** (`--pane`): `session` · `session:window.pane` (`work:1.0`) ·
pane id (`%3`) · session id (`$0`) · omitted = the current pane when inside
tmux. `--session <name>` is a clearer equivalent for whole-session targeting.

## The JSON contract

Every result carries an envelope: `schema_version` (currently `"2"`),
`command`, `muxray_version`, `generated_at`. **Branch on `schema_version`** — if
it is not the version you coded against, the shape may have changed.

`status` and `inspect` carry a `classification`:

```json
{ "program": "codex", "status": "running", "rule_id": "codex.running",
  "confidence": 0.88, "evidence": "Working (esc to interrupt)" }
```

- **`program`** — `claude`, `codex`, `copilot`, `shell` (an interactive shell
  prompt — the harness is *not* live; reported as `idle`), or `unknown` (a pane
  it does not recognize: editor, pager, transcript, muxray's own output).
- **`status`** — one of: `idle`, `running`, `blocked`, `waiting_for_input`,
  `needs_approval`, `error`, `completed`, `unknown`.
- muxray reports state from the **current live frame's footer** only. A pane that
  merely *mentions* an agent in scrolled content is `program=unknown` — "parse
  it yourself," not "something failed." A footer that is a shell prompt is
  `program=shell`/`status=idle`: a dropped connection or exited agent is **not**
  an agent `error`.
- Pass `--explain` to attach a `trace` of every rule considered — use it to
  diagnose an `unknown`.

`diff` carries `changed` (bool — **both `true` and `false` are exit 0**; change
is not an error), `summary`, `added`/`removed`/`context` line arrays, `hunks`,
and the `previous_snapshot`/`current_snapshot` ids.

## Snapshot & diff: detect and show change

```bash
muxray snapshot --pane work:1.0 --out before.json   # capture a baseline
# ... let the program work ...
muxray diff --pane work:1.0 --since before.json      # what changed
```

`--since` also accepts a snapshot **id**, or is omitted/`latest` to diff against
the most recent stored snapshot of that pane (muxray keeps a local store, so you
often don't need `--out` at all). `changed: false` is deterministic and
reproducible across machines — the hash is over cleaned text only.

**Interpreting a diff:** read `summary` first, then `added` (new output the
program produced) vs `removed` (lines that scrolled off or were replaced).
`hunks` counts distinct change regions. A spinner/elapsed-timer line flipping
between captures shows up as a tiny diff — treat a 1-line cosmetic change as
"still working," not "made progress."

## The control loop

Two verbs *are* the loop — you don't hand-roll poll+sleep+compare:

1. **Wait until it's your turn.** `muxray watch --pane <t>` blocks until the
   pane stops working, then prints the final `classification` and exits 0.
   - default `--until` = any settled state (`idle`, `completed`,
     `needs_approval`, `waiting_for_input`, `blocked`, `error`); it waits
     through `running` and transient `unknown`.
   - narrow it: `--until idle,needs_approval`.
   - bound it: `--timeout 5m` exits **5** if it never settles (the last-seen
     classification is still emitted).
   - then branch on the final `status`: `needs_approval`/`waiting_for_input` →
     hand off to a human; `error` → restart/alert; `idle`/`completed` → assign
     the next task (if `program=shell`, the pane dropped to a shell — relaunch,
     don't assign to a live agent).
2. **See the whole fleet.** `muxray scan` classifies every pane in one call →
   `{ "panes": [ { "target": "%3", "session": …, "classification": {…} } … ] }`.
   `target` is the pane id (`%N`) — feed it straight back into
   `status`/`watch`/`diff`. A pane that can't be read is reported `unknown` with
   an `error` class rather than failing the whole scan.

The wrapper `{baseDir}/scripts/muxray-watch-diff.sh` runs the canonical
"baseline → wait until settled → diff → classify" sequence for one pane and
prints all three results — use it to summarize a single agent's working turn.

## Reading a coding agent's output

To answer "what is this Claude/Codex/Copilot pane doing?":

1. `muxray status --pane <t>` → the `classification` is the answer: `program`
   names the agent, `status` names its state, `evidence` is the footer line that
   decided it.
2. If you also need *what it produced*, `muxray inspect --pane <t>` adds the
   snapshot and a diff against the last baseline in one call. Read `tail_excerpt`
   / the diff `added` lines for the most recent output.
3. `needs_approval` / `waiting_for_input` mean the agent is paused on a human —
   surface the prompt and stop; do not auto-approve.
4. `unknown` with a recognizable agent in scrollback usually means the live
   frame scrolled away or the pane is mid-redraw. Re-`status` once; if still
   `unknown`, fall back to reading `tail_excerpt` yourself.

## Reporting findings to the user

- Lead with the **classification**, not a wall of terminal text: e.g.
  "`work:1.0` — Codex, `needs_approval` (asking to run `rm -rf build/`)."
- For change, summarize the `diff.summary` + the few `added` lines that matter;
  do not paste the whole pane.
- For a fleet, render `muxray scan --text` (one line per pane) and call out only
  the panes that need action.

## Safety & secrets

- Pane text can contain secrets (tokens, keys, `.env` echoes). muxray does **not**
  redact `snapshot.raw`/`clean`, `diff` lines, or `tail_excerpt`. **You** must
  summarize or redact obvious secrets before showing output to the user or
  sending it anywhere external. Prefer reporting classification fields over raw
  pane dumps; pass `--no-raw` to drop the raw capture from a snapshot.
- muxray performs **no network egress** except the explicit, opt-in
  `muxray update` (downloads a verified release; sends nothing). Do not run
  `update`, `telemetry`, or `bundle --include-excerpt` as part of an
  observation loop — they are operator actions, not agent steps.
- Only inspect panes relevant to the user's request.

## Exit codes

`0` ok (incl. `changed:true`/`false`) · `1` internal · `2` usage · `3`
tmux/capture · `4` snapshot not found · `5` `watch` timed out. On failure stderr
carries `error.class` (a stable, branchable id) and `error.hint` (the next
action).

## Reference

- `references/json-contract.md` — compact field/state cheat-sheet.
- `examples/inspect-agent.md` — a worked end-to-end example.
- `muxray usage` — the full in-binary calling contract.
