# Captured Runner Trace Fixtures

These fixtures document the real Codex JSONL shape used by
`scripts/run-skill-evals.py`. Parser support must be based on captured traces
like these, not guessed runner event names.

Observed Codex JSONL shape:

- Top-level events include `thread.started`, `turn.started`, `item.started`,
  `item.completed`, and `turn.completed`.
- Tool calls appear under `item` objects. Shell commands use
  `item.type == "command_execution"` with `command`, `exit_code`, and `status`.
- File reads and writes are not guaranteed to appear in the captured trace; the
  current adapter only consumes explicit `file_read` and `file_write` items if a
  future Codex trace includes them.
- Token usage appears on `turn.completed` as `usage.input_tokens` and
  `usage.output_tokens`.
- Runner warnings can come from `item.type == "error"` events or from a nonzero
  return code in a manually captured `codex exec` trace.

Normalized fixture files use the runner-agnostic `normalized-v1` schema. Unit
tests should score these normalized metrics directly so ordinary pytest never
invokes a live agent or network-backed runner.
