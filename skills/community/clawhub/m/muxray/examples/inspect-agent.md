# Worked example: "what is the agent in `work:1.0` doing?"

A realistic end-to-end walk-through. Commands are run via the validating
wrapper; output is abbreviated.

## 1. See the whole fleet first

```bash
{baseDir}/scripts/muxray-run.sh scan --text
```

```
  main:0.0   %1  shell    idle
* work:1.0   %4  codex    running
  work:2.0   %7  claude   needs_approval
  logs:0.0   %9  unknown  unknown
```

Two panes need attention: `%4` is working, `%7` is paused on a prompt.

## 2. Classify the paused agent

```bash
{baseDir}/scripts/muxray-run.sh status --pane work:2.0
```

```json
{ "schema_version": "2", "command": "status",
  "classification": {
    "program": "claude", "status": "needs_approval",
    "rule_id": "claude.needs_approval", "confidence": 0.95,
    "evidence": "Do you want to proceed? ❯ 1. Yes  2. No" },
  "tail_excerpt": ["Edit file src/main.go", "Do you want to proceed?", "❯ 1. Yes  2. No"] }
```

**Report to the user:** "`work:2.0` — Claude is paused asking to edit
`src/main.go` (proceed? Yes/No). Waiting on you." Do **not** auto-approve.

## 3. Summarize the working agent's turn

```bash
{baseDir}/scripts/muxray-watch-diff.sh -t work:1.0 -T 5m
```

This snapshots `%4`, blocks until Codex stops `running`, then diffs:

```json
{ "classification": { "program": "codex", "status": "completed", "rule_id": "codex.completed" } }
```
```json
{ "changed": true, "summary": "+18 lines (3 hunks)",
  "added": ["Ran 42 tests, all passing", "Wrote internal/diff/diff.go", "Done."],
  "hunks": 3 }
```

**Report:** "`work:1.0` — Codex finished: wrote `internal/diff/diff.go` and ran
42 passing tests. Ready for the next task."

## 4. A pane that dropped to a shell

```bash
{baseDir}/scripts/muxray-run.sh status --pane main:0.0
```

```json
{ "classification": { "program": "shell", "status": "idle" } }
```

This is **not** an agent error — the agent exited (or the connection dropped) and
the pane is back at a shell prompt. Relaunch the agent rather than assigning it
work.

## Redaction note

`tail_excerpt`, `diff.added/removed`, and `snapshot.raw/clean` are verbatim pane
text and may contain secrets. Summarize the classification and the few relevant
lines; never paste a full pane dump into a report or an external channel.
