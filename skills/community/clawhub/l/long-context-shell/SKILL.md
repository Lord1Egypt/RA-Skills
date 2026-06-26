---
name: "long-context-shell"
description: "Runs long or continuous shell commands with file-backed logs, truncated previews, and fast log scanning. Invoke when shell output may be large, ongoing, or hard to inspect directly."
---

# Long Context Shell

Use this skill when a shell command is likely to produce long output, keep running, refresh continuously, or require structured monitoring instead of raw stdout.

## Invoke When

- The command may print more than a small screen of output
- The command may run for a long time
- The command may stream continuously, such as `watch`, `top`, `tail -f`, `ping`, or log followers
- The command fails and you need a lightweight scan instead of manually reviewing a large log

## Core Behavior

- Always write stdout and stderr to a timestamped log file
- Return a compact status card instead of raw full output
- Truncate long previews by default and point to the log file for deeper inspection
- Preserve timestamps so you can inspect the latest state or a specific time window
- Offer a lightweight scan step for locating likely errors, warnings, and failures

## Tools

### `long_context_shell_run`

Run a shell command in a detached process with file-backed logging.

**Inputs**

- `command` (string, required): shell command to run
- `waitMs` (number, optional): how long to wait before returning an initial status card
- `background` (boolean, optional): force monitor-first mode and return quickly for later peeks
- `headLines` (number, optional): lines to show from the beginning of the log
- `tailLines` (number, optional): lines to show from the end of the log

**Behavior**

1. Start the command through the platform shell
2. Write stdout and stderr to a log file with timestamps
3. If `background` is true, prefer a short initial wait and return control quickly
4. Return a status card with session id, log path, line count, byte count, status, background mode, and truncated preview
5. If the command still runs, use `long_context_shell_peek` later instead of rerunning the command

### `long_context_shell_peek`

Read the latest state of an existing session or log file.

**Inputs**

- `sessionId` (string, optional): previously returned session id
- `logPath` (string, optional): direct path to a log file if session id is unavailable
- `headLines` (number, optional): lines to show from the beginning
- `tailLines` (number, optional): lines to show from the end
- `timeQuery` (string, optional): timestamp fragment to filter lines, such as `2026-03-24T10:15`

**Behavior**

1. Resolve the session or log file
2. Detect whether the process is still running or already exited
3. Return a compact status card with truncated preview
4. If `timeQuery` is present, return matching lines for that timestamp fragment

### `long_context_shell_scan`

Scan a large log for likely failures instead of manually reading the full file.

**Inputs**

- `sessionId` (string, optional): previously returned session id
- `logPath` (string, optional): direct path to a log file
- `patterns` (array of strings, optional): custom match patterns
- `contextLines` (number, optional): surrounding lines to include around each match
- `limit` (number, optional): maximum number of matches to return

**Behavior**

1. Search the log for strong failure signals such as `error`, `exception`, `failed`, `fatal`, and `timeout`
2. Rank matches by severity so likely root-cause lines appear before generic warnings
3. Return the strongest matches with line numbers, severity, and short context
4. Prefer this tool over manual full-log inspection when output is large

### `long_context_shell_stop`

Stop a running session when monitoring is no longer needed.

**Inputs**

- `sessionId` (string, required): session to stop

## Recommended Workflow

1. Use `long_context_shell_run` for long or continuous commands
2. If status is `running`, use `long_context_shell_peek` to monitor progress
3. If status is `failed` or the preview is too short to explain the problem, use `long_context_shell_scan`
4. Only read the full log manually when the scan still leaves important ambiguity

## Debug Tips

- Start with a small `waitMs` and inspect the first status card before increasing complexity
- If a command is expected to keep running, set `background: true` and observe with repeated `long_context_shell_peek`
- Use `timeQuery` with the `startedAt` timestamp prefix to zoom into a suspicious time slice without reading the whole log
- If `preview` is truncated, treat `logPath` as the source of truth and use `scan` before opening the whole file
- If `scan` misses the real issue, retry with custom `patterns` that match the toolchain, framework, or service you are debugging
- When shell quoting gets tricky, first validate the raw command directly in the terminal, then move the exact command string into `long_context_shell_run`
- Prefer short self-contained repro commands such as `node -e` or a tiny script file when debugging behavior across shells
- Remember that shell syntax can differ across Unix and Windows, so commands using pipes, redirects, or quoting may need platform-specific forms
- For continuous commands, always finish the debug loop with `long_context_shell_stop` so old sessions do not keep running in the background
- To review a human-readable end-to-end scenario, run `node manual-flow-test.js` and inspect the printed status cards and scan output

## Safety

- Do not run destructive commands without explicit user approval
- Ask before using commands that delete files, reformat disks, reboot the machine, or escalate privileges
- Prefer `long_context_shell_scan` over full-log manual review when output is large
- Use `long_context_shell_stop` when a continuous command is no longer needed, especially for `tail -f`, `watch`, or similar monitoring sessions

## Examples

- Long build:
  - `long_context_shell_run({ command: "npm run build", waitMs: 1500 })`
- Continuous output:
  - `long_context_shell_run({ command: "tail -f app.log", background: true, waitMs: 500 })`
- Check latest state:
  - `long_context_shell_peek({ sessionId: "..." })`
- Check a specific timestamp:
  - `long_context_shell_peek({ sessionId: "...", timeQuery: "2026-03-24T10:15" })`
- Scan failures:
  - `long_context_shell_scan({ sessionId: "..." })`
- Human-readable flow test:
  - `node manual-flow-test.js`
