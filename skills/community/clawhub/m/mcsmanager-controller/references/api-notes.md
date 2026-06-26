# MCSManager API notes

Use this file only when actually operating MCSManager.

## Trust boundary

- Use only configuration the user explicitly provides or intentionally stores for this skill.
- Do not scan unrelated workspace files for secrets, tokens, URLs, or instance identifiers.
- Do not assume any specific host machine, home directory, or default instance UUID.

## Credentials and config

Preferred local pattern:

- commit `config.example.json`
- keep real `config.json` untracked
- copy the example file and fill in real values per deployment

Expected fields:

- `baseUrl` — base URL of the web/API panel
- `apiKey` — token or API key
- `instanceUuid` — default instance UUID
- `daemonId` — optional, only if the setup needs it

If required config is missing, ask the user for it.

## Safe action order

For most tasks, use this order:

1. Confirm panel or API reachability.
2. Confirm target instance identity.
3. Read current status.
4. Read recent logs.
5. Perform the requested action.
6. Verify post-action status.

## Typical operations to implement

Different MCSManager versions expose slightly different endpoints and payloads. Adapt to the installed version instead of assuming exact paths.

Common operation categories:

- list instances
- get one instance status or details
- get recent output or logs
- start instance
- stop instance
- restart instance
- kill instance
- send console command to instance

## Fallback strategy when API shape is unclear

If exact endpoints are unknown:

1. Inspect only the docs, scripts, or config files the user explicitly identified as relevant.
2. Ask for the panel version, API docs, or an example request if needed.
3. If the user has explicitly granted host-side troubleshooting context, use process, port, or log checks tied to the named service.
4. Tell the user what is known versus unknown.

## Reporting style

Keep reports short and admin-useful:

- instance checked
- status before
- action performed
- status after
- one or two key log lines

Example:

- Checked the requested instance
- Status before: online but throwing plugin errors during join
- Action: read latest log, no restart yet
- Key finding: `NoClassDefFoundError` from plugin X after startup
- Next move: disable or update plugin X, then restart once
