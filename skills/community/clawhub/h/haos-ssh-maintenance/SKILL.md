---
name: haos-ssh-maintenance
description: Use when Home Assistant OS needs SSH-based maintenance that cannot be completed cleanly through the Home Assistant API alone. Prefer API-first investigation for states, history, logbook, and routine automation checks; use this skill when direct filesystem access, YAML edits, custom_components inspection, HAOS shell troubleshooting, or interactive `ha` CLI work is required. Distinguish one-shot SSH commands from interactive SSH sessions: `ha` commands such as `ha core logs` may work only inside an interactive PTY-backed SSH session.
---

# HAOS SSH Maintenance

Use SSH only when API-based inspection is not enough.

## Default posture

Prefer the Home Assistant API first for:
- entity state inspection
- history and logbook
- automation listing, enable/disable, and trigger
- service-level testing

Switch to SSH when:
- files under `/config` need reading or editing
- YAML definitions must be inspected directly
- `custom_components` must be inspected
- shell-level troubleshooting is required
- `ha` CLI work is needed

Use the SSH target stored in `TOOLS.md`.

## Common HAOS paths

- `/config`
- `/config/configuration.yaml`
- `/config/automations.yaml`
- `/config/scripts.yaml`
- `/config/scenes.yaml`
- `/config/custom_components/`
- `/config/home-assistant_v2.db`

## Logs

Do not assume Home Assistant writes logs to a file by default.

Check logs in this order:
1. Home Assistant UI logs when the issue is visible there
2. interactive `ha` CLI log access such as `ha core logs`
3. Supervisor or container-side logs when available
4. file-based logs only if the environment explicitly enables them

Observed behavior for this environment:
- `ha core logs` may fail in one-shot SSH mode
- `ha core logs` works in an interactive PTY-backed SSH session

## Workflow

1. Decide whether the task is one-shot SSH or interactive SSH.
2. Start read-only.
3. Identify the smallest affected file or command path.
4. Explain the intended change before risky edits.
5. Edit minimally.
6. Verify surrounding context after the change.
7. Prefer reload over full restart when possible.
8. Report exactly what changed.

## Home Assistant YAML pitfalls

When editing Home Assistant automations or packages by hand:
- In automation YAML, use `service:` to call a service such as `shell_command.foo` or `light.turn_on`.
- Do not write `action: shell_command.foo` in YAML automations. That produces an unknown action error in this environment.
- `action` is the UI/schema concept for a step in the actions list, but in hand-written YAML the concrete service call key should be `service:`.
- After editing automation/package YAML, reload both core config and automations when possible, then validate by triggering the automation once.

## SSH modes

### One-shot SSH

Use one-shot SSH commands for:
- reading files under `/config`
- grepping YAML or custom component code
- listing directories
- small targeted edits
- quick environment inspection

One-shot SSH is appropriate for commands like:
- `cat`
- `grep`
- `sed`
- `find`
- `ls`

Do not assume `ha` CLI commands will work in one-shot mode.

### Interactive SSH

Use an interactive PTY-backed SSH session for:
- `ha core logs`
- other `ha` CLI commands that fail in one-shot mode
- shell flows that require a login session or interactive context

When running from OpenClaw, prefer a PTY-backed exec session and then send commands into the live SSH shell.

## Investigation order

### Automation problems

1. API logbook and history
2. `/config/automations.yaml`
3. `/config/scripts.yaml`
4. relevant Home Assistant or Supervisor logs

### Naming or entity-origin confusion

1. API-visible attributes and registry-derived metadata
2. YAML definitions under `/config`
3. template, MQTT, REST, command_line, utility_meter, and custom component definitions

### Integration or startup failures

1. relevant Home Assistant or Supervisor logs
2. referenced YAML blocks
3. `custom_components` if relevant

## Change boundaries

Use SSH for:
- YAML edits
- package edits
- `custom_components` inspection
- interactive `ha` CLI log inspection
- Supervisor or container-side log inspection
- shell-level checks
- targeted `.storage` inspection or edits when UI/registry-backed state must be changed directly

Do not use SSH first for:
- normal state checks
- routine entity discovery
- simple automation enable/disable/trigger actions

## `.storage` direct-edit policy

Home Assistant internal storage under `/config/.storage/` can be edited when necessary, including files such as:
- `/config/.storage/core.entity_registry`
- `/config/.storage/core.device_registry`
- `/config/.storage/core.config_entries`

Rules:
- Treat `.storage` edits as a last-resort or targeted-operation path, not the default first move.
- Back up the exact file before every edit.
- Prefer the smallest possible change to a specific entity/device/config entry.
- Expect UI names to live in `core.entity_registry`; YAML `friendly_name` overlays can override what the UI shows.
- Be aware of writeback/refresh timing: changes may not appear immediately and may require reload or restart.
- Avoid broad rewrites of `.storage` JSON unless explicitly necessary.
- Report both the file path edited and the rollback path created.

## Safety

- Read before editing.
- Change the smallest possible region.
- Avoid broad rewrites when a targeted edit is enough.
- Ask before changing behavior that affects locks, alarms, access control, or physical entry.

## Reporting

When using this skill, report:
- what path was inspected
- what was found
- what changed, if anything
- whether reload or restart is needed
