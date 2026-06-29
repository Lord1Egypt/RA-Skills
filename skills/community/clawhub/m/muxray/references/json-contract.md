# muxray JSON contract — cheat-sheet

A compact reference for the fields the skill branches on. The in-binary
`muxray usage` is the authoritative source; this mirrors the load-bearing parts.

## Envelope (every result)

| Field | Meaning |
| ----- | ------- |
| `schema_version` | currently `"2"` — **branch on this**; a different value means the shape may have changed |
| `command` | the subcommand that produced this result |
| `muxray_version` | binary version |
| `generated_at` | capture timestamp |

## `classification` (from `status`, `inspect`, `scan[].classification`)

| Field | Meaning |
| ----- | ------- |
| `program` | `claude` · `codex` · `copilot` · `shell` · `unknown` |
| `status` | `idle` · `running` · `blocked` · `waiting_for_input` · `needs_approval` · `error` · `completed` · `unknown` |
| `rule_id` | id of the rule that matched (e.g. `codex.running`) |
| `confidence` | 0..1 |
| `evidence` | the footer text that decided the classification |
| `trace` | present only with `--explain`: every rule considered |

### Reading the states

| status | meaning | typical action |
| ------ | ------- | -------------- |
| `running` | actively working | wait (`watch`) |
| `idle` / `completed` | done / at rest | assign next task |
| `needs_approval` | paused on a permission prompt | surface to human; do **not** auto-approve |
| `waiting_for_input` | paused on a question | surface to human |
| `blocked` | stuck (e.g. rate-limited) | inspect / alert |
| `error` | the agent hit an error | restart / alert |
| `unknown` | not a recognized live frame | re-check once, then read the tail yourself |

### program nuances

- `program=shell` / `status=idle` → the pane dropped to a shell prompt (agent
  exited, or a remote/VM connection dropped). This is **not** an agent `error`;
  relaunch rather than assign work to it.
- `program=unknown` → an editor, pager, transcript, or muxray's own output, or a
  live frame that scrolled off. "Parse it yourself," not "something failed."

## `diff` (from `diff`, and `inspect.diff`)

| Field | Meaning |
| ----- | ------- |
| `changed` | bool — **both values are exit 0**; change is not an error |
| `summary` | one-line human summary |
| `added` / `removed` / `context` | line arrays (compact by default; `--full` to uncap) |
| `hunks` | count of distinct change regions |
| `previous_snapshot` / `current_snapshot` | snapshot ids |

## Exit codes

| code | meaning |
| ---- | ------- |
| `0` | ok (including `changed:true`/`false`) |
| `1` | internal error |
| `2` | usage error |
| `3` | tmux / capture error |
| `4` | snapshot not found |
| `5` | `watch` timed out before reaching a target state |

On failure, stderr carries a JSON object with `error.class` (stable, branchable)
and `error.hint` (the next action).
