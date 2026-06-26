# Reference Implementation

These files are synced snapshots of the actual OpenClaw Pipedream integration source.

Use them when:
- debugging the OpenClaw Pipedream integration
- documenting current behavior
- comparing a proposed change against the live implementation
- tracing credential setup, agent app connection, activation, catalog loading, or tool registration

## Important current behaviors

### First-class MCP tools
Connected Pipedream apps are no longer just raw mcporter endpoints. Their MCP tools are registered into the agent runtime as normal callable tools.

### Per-agent isolation
Each agent uses its own Pipedream `external_user_id`, usually defaulting to the agent id / slug.

### Live connected-account discovery
Agent refresh uses the live Pipedream Connect accounts API when credentials are available.

### Dynamic full catalog
The full app catalog is loaded dynamically from the gateway catalog path when the user opens **Browse All Apps**.

### Real app icons
Authenticated app metadata can include `img_src`, which is passed through as `iconUrl` for UI rendering with fallback behavior.

## Files

### `pipedream-backend.ts`
Gateway handlers for:
- credentials
- catalog loading
- app connect / disconnect / activate / test
- per-agent status
- mcporter server entry generation
- live connected account discovery

### `pipedream-controller.ts`
Global Pipedream dashboard controller:
- platform credentials
- global status
- overall Pipedream UI actions

### `pipedream-views.ts`
Global Pipedream dashboard view and shared app icon rendering helpers.

### `agent-pipedream-controller.ts`
Per-agent controller for:
- app browser opening
- dynamic catalog fetch
- connected app state
- activation / test / disconnect

### `agent-pipedream-views.ts`
Per-agent view for:
- connected apps
- Browse All Apps modal
- manual slug connect
- activation / testing UI

## Source of truth

These are reference copies.

The running implementation lives in:
- `~/openclaw/src/gateway/server-methods/pipedream.ts`
- `~/openclaw/ui/src/ui/controllers/pipedream.ts`
- `~/openclaw/ui/src/ui/views/pipedream.ts`
- `~/openclaw/ui/src/ui/controllers/agent-pipedream.ts`
- `~/openclaw/ui/src/ui/views/agents-panel-pipedream.ts`

If behavior differs, trust the live OpenClaw source first and re-sync these reference files.
