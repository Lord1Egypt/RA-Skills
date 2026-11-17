# Lite runtime contract

The host must be able to read and write authorized local paths, execute Python, return stdout/stderr/exit codes, continue a tool loop, and request user confirmation for gated actions.

Available commands are `doctor`, `init`, `run`, `scan`, `build`, `validate`, `render`, `update`, `status`, and `uninstall`. Default uninstall removes only owned runtime state and preserves source notes plus derived knowledge/HTML. Removing derived outputs requires the separate `--remove-outputs --confirm-remove-outputs` gate. Commands for watching, background scheduling, semantic/model work, persistent serving, and stop are absent.

Each command returns JSON containing `status`, `code`, `message`, `artifacts`, `next_actions`, `needs_user_input`, and `data`. Treat `needs_user_input` as a gate rather than a generic failure.
