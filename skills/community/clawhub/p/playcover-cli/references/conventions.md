# Global conventions

All CLI commands obey a shared set of conventions defined in `CLIContext.swift`. Knowing them lets you predict any command's behavior without reading its source.

## Output streams

| Helper | Stream | Use |
|--------|--------|-----|
| `CLIOut.line(...)` | **stdout** | Normal output (lines, JSON, progress) |
| `CLIOut.error(...)` | **stderr** | Errors, prefixed `Error: ` |
| `CLIOut.json(...)` | **stdout** | Pretty-printed, keys sorted |
| `CLIOut.exit(_:)` | — | Calls `Foundation.exit(_:)` to terminate |

- **stdout is for data** — pipe it, parse it, redirect it.
- **stderr is for diagnostics** — it never pollutes parsed stdout. `2>/dev/null` silences it; `2>&1` merges it.
- **JSON output is pretty-printed and key-sorted**, so it is stable across runs and friendly to diff tools.

## `--json` convention

Many read commands (`list`, `info`, `source list`, `store list`, `settings list`, `config list`) take a `--json` flag. Without it they print human-readable text; with it they print JSON to stdout.

- Prefer `--json` for any scripted or agent-driven consumption.
- JSON shapes are documented per-command in each reference file.

## Progress rendering

`CLIProgressRenderer` adapts to whether stdout is a TTY:

- **TTY** (interactive terminal): an in-place progress bar refreshed with `\r`, at most every 50ms. Format: `==> <step>` on its own line, then a bar `[=====-----] NN%`.
- **Piped / redirected** (not a TTY): one progress line per 10% boundary (`NN%`) plus `==> <step>` lines. No `\r`, so every line is a permanent record — ideal for logs.

Progress never blocks on a GUI spinner or a modal dialog. If a command needs to show progress, it uses this renderer.

## GUI suppression in CLI mode

`CLIContext.isCLI` gates every GUI-only code path. In CLI mode the following are **skipped or replaced**:

| GUI behavior | In CLI mode |
|--------------|-------------|
| `NSAlert` modal dialogs | Replaced with `CLIOut.error` to stderr + non-zero exit |
| `UNUserNotificationCenter` user notifications | Suppressed entirely |
| App Store / macOS version check that would block | Suppressed |
| KeyCover interactive password prompt (on `launch`) | Suppressed |

This means a CLI command will **never** hang waiting for a human to click a dialog. If user input is required, the command fails fast with a stderr message and a non-zero exit code.

## Async completion

Some commands kick off async work (download, install, sign, …). The CLI cannot `exit()` before that work finishes. `CLIContext.waitForCompletion()` runs the current `RunLoop` until `MainActor`/`Main-queue` work drains, then returns. Commands call it before `exit()`, so:

- A command **blocks** until its underlying task completes.
- The command's exit code reflects the task's outcome.
- Commands are **not** long-running daemons — they exit after one logical operation.

## Exit codes

| Code | Constant (`CLIExitCode`) | Meaning |
|------|--------------------------|---------|
| `0` | `success` | Operation completed successfully |
| `1` | `generalError` | Unspecified failure |
| `2` | `badArguments` | Bad argument, unknown config key, file not found, read-only field |
| `3` | `appNotFound` | No installed app matches the given bundle ID |
| `4` | `verificationFailed` | Checksum mismatch on download, or keymap bundle-ID mismatch on import |
| `5` | `cancelled` | Operation was cancelled |

### Scripting recipe

```bash
set -e
BIN="PlayCover.app/Contents/MacOS/PlayCover"

if ! "$BIN" list --json | jq -e '.[].bundleIdentifier' >/dev/null; then
  echo "no apps installed" >&2
  exit 1
fi

"$BIN" install ~/Downloads/App.ipa --play-tools --category games
case $? in
  0) echo "ok" ;;
  2) echo "bad args" >&2; exit 2 ;;
  4) echo "checksum mismatch" >&2; exit 4 ;;
  *) echo "install failed" >&2; exit 1 ;;
esac
```
