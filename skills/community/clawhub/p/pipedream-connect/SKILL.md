---
name: pipedream-connect
description: Connect OpenClaw agents to thousands of apps via Pipedream Connect with per-agent OAuth isolation, first-class MCP tool exposure, live connected-account discovery, and dynamic full-catalog browsing. Use when setting up or maintaining the OpenClaw Pipedream integration, troubleshooting agent app connections, documenting the Pipedream dashboard / agent tools flow, or working on Pipedream catalog, icons, activation, and MCP tool registration behavior.
---

# Pipedream Connect

Use this skill for the OpenClaw Pipedream integration.

## Current integration summary

OpenClaw now uses this model:

- **Global Pipedream tab** = platform credentials only
- **Agent Tools → Pipedream** = per-agent app connections and activation
- **Connected Pipedream apps become first-class agent tools**
- **Connected apps are discovered live from Pipedream Connect accounts API**
- **Browse All Apps loads the full dynamic catalog on demand**
- **Catalog icons come from authenticated Pipedream app metadata (`img_src`) when available**

## Key improvements already implemented

### 1) Connected Pipedream tools are first-class tools
Connected app MCP tools are registered into the agent runtime as normal tools.

This means:
- agents do **not** need raw `mcporter call ...` bridge syntax in normal chat use
- tool catalog surfaces connected app tools directly
- execution still routes through per-agent mcporter servers under the hood

Server naming pattern:

```text
pipedream-{externalUserId}-{appSlug}
```

### 2) Per-agent connection model
Each agent gets its own Pipedream identity via `external_user_id`.

Default behavior:
- `external_user_id` defaults to the agent slug / id
- each agent gets isolated OAuth accounts and MCP tool exposure

Per-agent config path:

```text
~/.openclaw/workspace/config/integrations/pipedream/{agentId}.json
```

### 3) Live connected-account discovery
Agent refresh uses the Pipedream Connect accounts API to discover connected apps live.

Do not assume local config is the source of truth for connected apps if live API access is available.

### 4) Full app catalog is dynamic
The app browser should use the live full catalog, not a static baked-in list.

Current intended behavior:
- clicking **Browse All Apps** loads the full catalog dynamically
- do not rely on stale frontend app constants for authoritative app metadata

### 5) Real app icons now flow from Pipedream metadata
Use authenticated Pipedream app metadata when available so apps can render real icons.

Important detail:
- authenticated app endpoints expose `img_src`
- public MCP catalog endpoints may not expose equivalent icon metadata on the same path
- UI should render `iconUrl` when present and fall back safely when missing / broken

## Architecture

```text
Global Pipedream tab
  -> save platform credentials
  -> show overall status

Agents -> [Agent] -> Tools -> Pipedream
  -> set / override external user id
  -> connect app
  -> refresh connected accounts
  -> activate connected app MCP tools
  -> browse full dynamic app catalog
```

## Setup workflow

### 1) Create Pipedream credentials
In Pipedream:
- create an OAuth client
- copy `client_id` and `client_secret`
- create / select a project
- copy `project_id`

### 2) Configure OpenClaw global credentials
In the OpenClaw dashboard Pipedream tab, save:
- Client ID
- Client Secret
- Project ID
- Environment

Prefer `production` unless explicitly testing in development.

### 3) Connect apps per agent
In **Agents → [Agent] → Tools → Pipedream**:
- verify the external user id
- connect an app
- complete OAuth
- refresh
- activate the app if needed

### 4) Use the tools normally
After activation, connected MCP tools should appear as ordinary tools for that agent.

## Storage and security

### Secrets
Store `clientId` and `clientSecret` in the OpenClaw vault:

```text
~/.openclaw/secrets.json
```

### Non-secret config
Store non-secret Pipedream config in:

```text
~/.openclaw/workspace/config/pipedream-credentials.json
```

Expected non-secret fields:
- `projectId`
- `environment`
- `externalUserId`

Do not keep plaintext client secrets in normal config files.

## Runtime behavior to preserve

When editing this integration, preserve these behaviors:

1. **Connected apps remain per-agent isolated**
2. **Connected app tools remain first-class tools in the agent runtime**
3. **Live API data beats stale local display metadata**
4. **Browse All Apps uses the dynamic full catalog**
5. **Icons use `img_src` / `iconUrl` when available**
6. **UI falls back safely if an icon URL fails**

## Useful RPCs / methods

Common gateway methods involved in this integration include:

- `pipedream.status`
- `pipedream.saveCredentials`
- `pipedream.catalog`
- `pipedream.connect`
- `pipedream.disconnect`
- `pipedream.activate`
- `pipedream.test`
- `pipedream.agent.status`
- `pipedream.agent.save`
- `pipedream.agent.delete`

When documenting or debugging, confirm the exact current implementation in gateway server methods and the agent/global Pipedream UI controllers.

## Debugging guidance

### Connected app missing
Check in this order:
1. global credentials configured
2. correct project / environment
3. OAuth completed successfully
4. agent external user id is the one you expect
5. refresh calls the live accounts API successfully
6. app activation completed

### Tool missing after app connection
Check:
1. connected account is present in `pipedream.agent.status`
2. mcporter server was created for `pipedream-{externalUserId}-{appSlug}`
3. runtime tool registration is loading MCP tools into the agent catalog

### Wrong / stale icon
Check:
1. whether the catalog path is using authenticated Pipedream app metadata
2. whether `img_src` is mapped to `iconUrl`
3. whether UI is rendering from live catalog data or an old static fallback
4. whether fallback rendering is masking an image load failure

### Wrong app list behavior
If Browse uses stale frontend constants, prefer the dynamic catalog path instead.

## Shell / low-level debugging

For low-level debugging only, mcporter servers follow this pattern:

```bash
mcporter call pipedream-main-gmail.gmail-find-email \
  instruction="Find unread emails from today"
```

But for normal OpenClaw agent use, prefer the first-class tool path rather than instructing users to call mcporter directly.

## Files commonly involved

Check these areas when updating the integration:

- gateway server methods for `pipedream.*`
- global Pipedream UI view/controller
- agent Pipedream UI view/controller
- runtime tool registration path that imports connected MCP tools into the agent tool registry
- mcporter config write / refresh path

## Practical rule

If the question is about:
- credentials or project setup -> global tab
- app connection / activation -> agent tools panel
- tool availability -> runtime MCP tool registration
- icons / catalog display -> dynamic catalog path
- stale metadata -> remove static fallback dependence first
