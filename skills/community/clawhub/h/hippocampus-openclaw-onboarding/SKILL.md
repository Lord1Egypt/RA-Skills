---
name: hippocampus-openclaw-onboarding
description: >
  Bootstrap OpenClaw with Hippocampus memory under a branded, repeatable setup:
  workspace, agent ID, API key or bootstrap token, and MCP wiring.
---

# Hippocampus OpenClaw Onboarding

Use this skill when connecting a new OpenClaw instance or workspace to
Hippocampus memory.

## Setup Goals

- define a stable workspace name
- assign a durable root `agent_id`
- configure gateway URL and authentication
- ensure sub-agents inherit scoped memory identity

## Preferred Flow

1. Register or sign in through the Hippocampus portal.
2. Create a root OpenClaw agent in the dashboard.
3. Copy the generated bootstrap one-liner.
4. Run:
   `npx hipokamp-mcp setup --bootstrap-token <token> --gateway <gateway-origin>`
5. Let `hipokamp-mcp` write local config under `~/.hipokamp/config.json`.
6. Verify health and first store/search round trip.

## Guidance

- Use one root agent per OpenClaw instance.
- Keep sub-agent IDs under the same workspace namespace.
- Prefer bootstrap-first setup over pasting a long-lived API key.
- Do not reuse credentials across unrelated workspaces.

## Related

- `hippocampus-memory-core` once setup is complete
- `hippocampus-subagent-memory` for child-agent isolation
- `@hippocampus/openclaw-context-engine` for native lifecycle integration
