# Security Model

OpenClaw Manager is a local Node.js skill plus a local sidecar. It is not a hosted service.

## What bootstrap does

`src/skill/bootstrap.ts` coordinates three local-only actions:

1. read local manager settings and a small set of non-secret environment variables
2. check the local sidecar health endpoint
3. start the local sidecar only after explicit one-time consent

Bootstrap does **not** upload raw chat logs, state files, or environment dumps anywhere.

## Environment variables read by the runtime

The runtime reads only local manager configuration values:

- `OPENCLAW_MANAGER_STATE_ROOT`
- `OPENCLAW_MANAGER_NODE_ID`
- `OPENCLAW_MANAGER_BIND_HOST`
- `OPENCLAW_MANAGER_SIDECAR_URL`
- `OPENCLAW_MANAGER_NO_AUTOSTART`
- `OPENCLAW_MANAGER_ALLOW_REMOTE_SIDECAR`
- `OPENCLAW_MANAGER_SERVER_PROCESS`
- `PORT`

These are used only to choose local paths, local bind host, local health-check URL, or local autostart behavior.

## Network behavior

### Bootstrap

Bootstrap only talks to the sidecar health endpoint.

- default target: `http://127.0.0.1:<PORT>/health`
- accepted by default: `127.0.0.1`, `localhost`, `::1`
- rejected by default: non-loopback sidecar URLs

You must explicitly set `OPENCLAW_MANAGER_ALLOW_REMOTE_SIDECAR=1` before a non-loopback sidecar URL is accepted.

### Connectors

Connector code exists for Telegram, WeCom, Email, and GitHub, but connectors do not make external requests by default.

External connector behavior only happens after you explicitly configure the relevant connector and provide the necessary local secrets or private config.

## Local process spawning

The runtime may spawn the local sidecar process, but only after explicit one-time consent.

- only known local entrypoints are allowed:
  - `dist/api/server.js`
  - `tsx src/api/server.ts`
- the launcher uses `shell: false`
- it does not execute arbitrary shell strings

## Sidecar exposure

The sidecar binds to `127.0.0.1` by default.

- default: local-only loopback
- optional: `0.0.0.0` or `::` only if you explicitly set `OPENCLAW_MANAGER_BIND_HOST`

The project does not expose the sidecar to LAN or the internet by default.

## Local state

Default state root:

```text
~/.openclaw/skills/manager/
```

Manager state stays local and includes:

- sessions
- runs
- event logs
- checkpoints
- thread shadows
- promotion queue
- connector bindings/configs
- snapshots
- capability facts
- local settings

## Autostart consent

Automatic sidecar startup is disabled until you explicitly allow it once.

Ways to allow it:

```bash
npm run consent:autostart
```

or:

```bash
npm run bootstrap -- --allow-autostart
```

Consent is stored locally in the manager state root. It is not sent anywhere.

## Raw data handling

- raw chat transcripts are not uploaded anywhere by default
- snapshot and capability exports are redacted by default
- anonymized capability exports do not include raw chat text

## Reporting

If you believe you found a real vulnerability, open a GitHub issue with reproduction steps or contact the maintainer privately if disclosure should be limited.
