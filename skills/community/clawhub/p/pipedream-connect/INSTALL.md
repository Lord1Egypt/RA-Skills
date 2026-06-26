# Installation Guide for Agents

Use this guide when installing or validating the OpenClaw Pipedream integration.

## Security notice

Before installation or migration, inform the user that:

- `PIPEDREAM_CLIENT_ID` and `PIPEDREAM_CLIENT_SECRET` are stored in the OpenClaw vault:
  - `~/.openclaw/secrets.json`
- non-secret Pipedream config is stored in:
  - `~/.openclaw/workspace/config/pipedream-credentials.json`
- mcporter server entries are stored in:
  - `~/.openclaw/workspace/config/mcporter.json`
- OAuth access tokens may appear in mcporter Authorization headers and should be treated as sensitive short-lived credentials
- optional token-refresh cron jobs persist until removed

## Prerequisites

Verify:

```bash
openclaw --version
which mcporter
openclaw gateway status
```

## Main setup flow

### 1) Configure platform credentials
In the OpenClaw dashboard Pipedream tab, save:
- Client ID
- Client Secret
- Project ID
- Environment

Prefer `production` for normal use.

### 2) Connect apps per agent
In **Agents → [Agent] → Tools → Pipedream**:
- verify the agent external user id
- connect an app
- complete OAuth
- refresh if needed
- activate the app if activation is required

### 3) Browse the full catalog
Use **Browse All Apps** to load the full dynamic catalog.

Do not assume the static frontend app list is authoritative.

## Optional token refresh automation

If the environment still relies on periodic token refresh via cron, install the included script:

```bash
bash ~/.openclaw/workspace/skills/pipedream-connect/scripts/setup-cron.sh
```

Review the generated cron entry before keeping it.

## Validation checklist

After setup, verify:

### Credentials
```bash
cat ~/.openclaw/workspace/config/pipedream-credentials.json
```
Confirm it contains non-secret config only.

### Vault
```bash
cat ~/.openclaw/secrets.json
```
Confirm the Pipedream client credentials exist there.

### Gateway RPCs
Confirm the gateway exposes current Pipedream RPCs such as:
- `pipedream.status`
- `pipedream.catalog`
- `pipedream.agent.status`
- `pipedream.connect`
- `pipedream.disconnect`
- `pipedream.activate`
- `pipedream.test`

### Connected apps
Open the agent Pipedream panel and refresh. Connected apps should come from the live accounts API when credentials are available.

### First-class tools
After activation, connected app MCP tools should appear as ordinary agent tools, not only as raw mcporter server endpoints.

### Catalog and icons
Open **Browse All Apps** and verify:
- the full dynamic catalog loads
- real app icons render when `iconUrl` is present
- broken/missing icons fall back safely

## Troubleshooting

### `unknown method: pipedream.*`
Rebuild and restart the gateway.

### Connected app missing
Check:
- credentials
- project/environment
- external user id
- live accounts API response
- activation state

### Tools missing after app connection
Check:
- app shows in `pipedream.agent.status`
- matching mcporter server exists
- runtime tool registration is importing the connected MCP tools

### Wrong or stale icon
Check:
- catalog path uses authenticated Pipedream app metadata
- `img_src` is mapped to `iconUrl`
- UI is not rendering stale static metadata

## Important file locations

| File | Purpose |
|------|---------|
| `~/.openclaw/secrets.json` | Vault-stored Pipedream client credentials |
| `~/.openclaw/workspace/config/pipedream-credentials.json` | Non-secret Pipedream config |
| `~/.openclaw/workspace/config/mcporter.json` | MCP server config for connected apps |
| `~/.openclaw/workspace/config/integrations/pipedream/{agentId}.json` | Per-agent Pipedream config |
| `~/.openclaw/workspace/skills/pipedream-connect/scripts/pipedream-token-refresh.py` | Optional token refresh script |
