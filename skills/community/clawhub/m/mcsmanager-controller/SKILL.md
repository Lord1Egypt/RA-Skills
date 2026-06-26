---
name: mcsmanager-controller
description: Control and troubleshoot MCSManager-managed Minecraft servers through the MCSManager API and clearly provided host-side context. Use when asked to start, stop, restart, inspect, or debug an MCSManager instance; read or tail server logs; send console commands; or check instance status. Use only with configuration the user explicitly provides in the task context or in a local config file the user has intentionally set up for this skill.
---

# MCSManager Controller

Use this skill to operate an MCSManager instance safely and consistently.

## Scope and safety

- Use only configuration the user explicitly provides in the prompt, session context, or a config file intentionally created for this skill.
- Do not assume a specific host, home directory, panel URL, token, or instance UUID.
- Do not search unrelated workspace files for secrets.
- Do not infer credentials from random local files.
- If required config is missing, ask for it.

## Quick workflow

1. Confirm the target instance.
   - Use the instance identifier the user provided.
   - If a dedicated skill config file exists and the user set it up for this skill, use its default instance value.
2. Prefer read-only checks first.
   - Check whether MCSManager is reachable.
   - Check whether the instance is online before restarting anything.
   - Read logs before making changes.
3. Only then perform state changes.
   - Start, stop, restart, kill, or send commands.
4. Report back clearly.
   - Say what was checked.
   - Say what changed.
   - Include the important log line or symptom.
   - If something is broken, say the broken thing directly.

## Operating rules

- Prefer the API over brittle browser clicking.
- Prefer read-only actions before writes.
- Avoid restart spam. If a start or restart fails, inspect logs before retrying.
- Preserve exact console commands when sending them.
- For dangerous commands like `stop`, `kill`, or destructive plugin actions, confirm intent unless the user explicitly asked.
- If the API details are missing, read `references/api-notes.md` and adapt to the installed MCSManager version.
- If the user wants reusable local config, use `config.json` in this skill directory.
- If `config.json` does not exist, create it by copying `config.example.json` and filling in user-provided values.

## Common tasks

### Check status

Use when the user asks whether the server is up, lagging, or crashed.

- Verify MCSManager service reachability.
- Query the target instance state.
- If the API is unavailable and the user has provided host-side access details, fall back to host-side process and port checks.

### Read logs

Use when the user reports crashes, plugin errors, failed joins, or startup problems.

- Fetch recent instance logs.
- Prioritize Java exceptions, plugin stack traces, port bind errors, world corruption, and authentication issues.
- Quote the minimal log excerpt that explains the failure.

### Send console commands

Use for commands like whitelist changes, saves, broadcasts, plugin commands, or graceful shutdowns.

- Echo the exact command in the response.
- Prefer graceful commands before hard stop actions.
- For batch commands, serialize them and avoid flooding the panel.

### Restart safely

Use when the instance is stuck, plugins need reload-by-restart, or the user asks for a restart.

- Confirm the server is actually online first.
- If players may be connected, warn about impact when appropriate.
- Stop gracefully if possible.
- Start once.
- Re-check status and read the first meaningful startup lines.

## Local config pattern

Recommended setup:
- Commit `config.example.json`.
- Keep your real `config.json` untracked.
- Put per-server values in `config.json`.
- Treat `config.json` as user-managed local config, not something to discover by rummaging through unrelated files.

## Reference file

Read `references/api-notes.md` when you need request patterns, environment conventions, or fallback strategy.
