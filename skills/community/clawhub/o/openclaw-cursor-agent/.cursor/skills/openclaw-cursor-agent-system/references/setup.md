# Setup Checklist

This reference defines the expected behavior for the `OpenClaw -> tmux -> Cursor CLI` architecture.

## Build Checklist

- Create `cursor-agent-system/` with `scripts/`, `templates/`, `status/`, `tasks/`, and `logs/`.
- Add a shared `scripts/common.sh` for path resolution, status updates, session lookup, and output capture.
- Keep each script focused on one lifecycle action.
- Make session names unique with `{project}-{task}-{timestamp}`.
- Store status, task, and log artifacts using the session name as the base file name.

## Script Behavior

### `spawn-cursor.sh`

- Validate `tmux`, Cursor CLI, and `python3`.
- Accept task name, task description, project path, priority, ETA, and optional existing task file.
- Create the task Markdown and initial status JSON when no external task file is supplied.
- Start a detached `tmux` session in the target project directory.
- Pipe pane output to the session log file.
- Launch Cursor CLI with the task file content inside the tmux session.

### `check-status.sh`

- Support two modes:
  - no argument: list all recorded sessions
  - one argument: resolve a session or task alias and print detailed status
- Show whether the tmux session exists.
- Show pane PID when available.
- Capture the latest output, ideally 30 lines.
- Update the status JSON with the latest snapshot.

### `attach-session.sh`

- Resolve a session alias to the latest matching session.
- Refuse to attach if the tmux session no longer exists.
- Print a short reminder for `Ctrl+B, D`.

### `send-command.sh`

- Resolve the session alias.
- Send an extra instruction through `tmux send-keys`.
- Support `/pause`, `/resume`, `/status`, `/focus`, `/expand`, and `/abort`.
- Update the status JSON after sending.

### `kill-session.sh`

- Ask for confirmation unless an explicit no-prompt flag is present.
- Try graceful termination with `Ctrl+C` first.
- If the session still exists, allow `--force` to kill it.
- Optionally support file cleanup, but do not purge by default.

## UX Requirements

- Use Chinese-facing messages for errors and operational hints.
- Include clear section dividers in command output.
- Keep exit codes meaningful: `0` for success, non-zero for failure.
- Avoid brittle session lookup patterns such as `find | grep | head`; use deterministic file naming or structured lookup instead.

## Validation

After implementation or edits, run:

```bash
bash -n scripts/common.sh scripts/spawn-cursor.sh scripts/check-status.sh scripts/attach-session.sh scripts/send-command.sh scripts/kill-session.sh
```

If the environment has `shellcheck`, run it as an extra pass.
