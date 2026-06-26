# Design 0.2.0

## Goal

Turn `openai-auth-switcher-public` from a script-first operator toolkit into a **foolproof, web-first, first-run-friendly productized skill**.

The `0.2.0` release should let a user install the skill and immediately get:

- a working web entrypoint
- a chosen port
- generated admin credentials
- an SSH tunnel command
- a first-run takeover flow even when no `auth-profiles.json` exists yet

## Product statement

Install first, enter the web UI first, then complete takeover.

The absence of an auth file must no longer be treated as a fatal product failure.
It should be treated as a **first-run onboarding state**.

## Release target

- Version: `0.2.0`
- Positioning: Linux-first, web-first, onboarding-friendly public release

## Core problems in 0.1.x

1. user must understand internal file layout before getting value
2. no-auth environments fail too early
3. no guided takeover workflow
4. no one-shot installation flow for the web service
5. no explicit install summary with port, credentials, and SSH tunnel
6. insufficient handling for edge cases like occupied ports or no systemd user support

## Desired install outcome

After installation/bootstrap, print a result block like:

```text
Install complete.

Web URL (local): http://127.0.0.1:9527
Port: 9527
Username: admin
Password: <generated>

SSH tunnel:
ssh -L 9527:127.0.0.1:9527 root@<server-ip>

Status: first-run takeover required
Next step: open the page and import an existing auth file or complete first auth setup.
```

## Runtime modes

### Mode A: First-run / not yet taken over

Conditions:
- `auth-profiles.json` missing
- runtime otherwise discovered

UI behavior:
- web service starts normally
- dashboard shows onboarding state instead of fatal exception
- guided actions are visible:
  - import existing auth file
  - specify runtime auth path
  - re-check environment
  - view troubleshooting

### Mode B: Managed / active

Conditions:
- `auth-profiles.json` exists and is parseable

UI behavior:
- normal management dashboard
- slot management
- dry-run switch
- controlled switch
- rollback
- local analytics

### Mode C: Broken environment

Conditions:
- OpenClaw root / workspace / agent root cannot be found

UI behavior:
- web service still starts
- page explains the missing prerequisite in human terms
- page shows exact next-step guidance

## Port strategy

Port selection policy:

1. try `9527`
2. if occupied, try `12138`
3. if both occupied, choose an available fallback port
4. always print the actual chosen port clearly

Optional future env overrides:
- `OPENAI_AUTH_SWITCHER_WEB_PORT`
- `OPENAI_AUTH_SWITCHER_WEB_HOST`

Default host:
- `127.0.0.1`

Rationale:
- safer by default than binding `0.0.0.0`
- works naturally with SSH port forwarding

## Authentication strategy

### Default web credentials

- username: `admin`
- password: randomly generated, 16-20 chars, URL-safe/simple enough to copy

Store generated credentials in a local state file, for example:

- `state/install-info.json`
- or `state/web-admin.json`

### Required install output

Always print:
- username
- password
- port
- local URL
- SSH tunnel command

### Post-install guidance

Prompt the user to change the password after first login.

## Service strategy

### Preferred path

Use a systemd user service when available.

### Fallback path

If user-service systemd is unavailable:
- run as a managed background process
- print a status note that fallback mode is active
- provide stop/start commands

## Web UX requirements

### Top-level states

1. installing / not started
2. onboarding / first-run takeover
3. active management
4. degraded / broken environment

### UX rules

- prefer plain language over internal engineering terms
- do not expose raw stack traces to users
- every failure state must include the next action
- write operations must stay explicit and confirmable

### First-run onboarding cards

Suggested actions on the page:
- import existing `auth-profiles.json`
- point to a discovered auth file path
- re-run environment checks
- explain what takeover means
- show where the chosen state directory is stored

## Special-case handling

### Port already in use

- auto-fallback to 12138
- then to a random free port
- never fail install just because 9527 is occupied

### No systemd user session

- degrade to background process mode
- print exact control commands

### No auth file

- do not fail the web UI startup
- enter onboarding mode

### models.json exists but auth-profiles.json missing

- show: OpenClaw detected, account takeover not completed yet

### SSH-only environments

- always print SSH tunnel guidance
- do not require public Nginx/HTTPS for first use

### Existing internal/live skill on same machine

- avoid destructive interference
- keep public track isolated
- avoid overwriting live operator state

## Proposed new components

### Scripts

- `scripts/install_web_app.py`
- `scripts/pick_port.py`
- `scripts/generate_web_credentials.py`
- `scripts/bootstrap_runtime.py`
- `scripts/import_auth_file.py`
- `scripts/web_service_status.py`

### Service layer

- `service/app.py`
- `service/config.py`
- `service/runtime_state.py`
- `service/install_mode.py`

### References

- `references/first-run-web.md`
- `references/install-web-mode.md`
- `references/ssh-tunnel.md`
- `references/troubleshooting-web.md`

## Acceptance criteria for 0.2.0

### Install flow

- user can run one command and get a reachable web UI
- chosen port is printed
- generated credentials are printed
- SSH tunnel command is printed

### No-auth flow

- missing auth file does not prevent startup
- onboarding UI is shown
- next-step guidance is human-readable

### Managed flow

- existing auth environment still works
- runtime inspection and switching functions remain available

### Edge cases

- occupied ports handled automatically
- no-systemd handled with fallback mode
- errors produce actionable guidance

## Validation snapshot (2026-03-24)

Validated in the current Linux/OpenClaw environment:

- clean install reaches `systemd-user` preview mode successfully
- reinstall applies changed unit env/port correctly after `daemon-reload`
- status/runtime output no longer mislabels active systemd preview as `background-process`
- stop helper shuts down preview service cleanly and status falls back to `service_ready=false`
- `9527` occupied falls back to `12138`
- `9527` + `12138` occupied falls back to a random free port
- uninstall-like cleanup + reinstall path verified end to end

## Suggested release note theme

`0.2.0` should be marketed as the release that turns the public skill into a real first-run product, not only a toolkit.
