---
name: "habitify-mcp"
description: "Connect Habitify to OpenClaw with OAuth; read habits and update progress through Habitify's hosted MCP server."
---

# Habitify MCP

1. For setup, consult https://docs.openclaw.ai/cli/mcp/registry and https://api-docs.habitify.me/mcp/ for current support. Inspect `openclaw mcp show habitify --json` before adding a definition; preserve an existing user's configuration. If absent, register the hosted server:
   ```bash
   openclaw mcp add habitify --url https://mcp.habitify.me/mcp --transport streamable-http --auth oauth
   ```
   Confirm the saved definition uses the intended endpoint and OAuth. This connects to Habitify's remote server; it does not require a local Habitify server or a Habitify API key. Use this procedure instead of the retired `habitify-protected-access` API helper; do not request a paid API key as an OAuth fallback.
2. Run `openclaw mcp login habitify` when authorization is needed. Deliver the sign-in link privately. A loopback callback must reach the machine running login, not merely the user's phone or another computer. For unreachable callbacks use the fallback printed by the login command, documented as `openclaw mcp login habitify --code <code>`; treat the code as a credential and keep it out of shared artifacts. Keep OAuth tokens in OpenClaw's managed store.
3. Run `openclaw mcp doctor habitify --probe` and discover live tool schemas. Verify end-to-end access with the read-only `list_habits_by_date` tool using a date in YYYY-MM-DD resolved from the user's timezone. Report a successful live read separately from configuration or authorization alone. If tools have not appeared after setup, check availability on a fresh turn before changing configuration or restarting services.
4. Resolve requested habits by live IDs, not guessed names. The same habit may appear in several time-of-day groups; deduplicate by ID when counting or updating. Preserve returned units, daily versus weekly targets, and status meanings. Discover current schemas before logging progress or marking habits complete, skipped, or failed. Apply bulk operations only when the user's requested scope includes every affected habit.
5. For verification, use reads only; never create progress as a connectivity test. Report subscription, authentication, and transport errors as returned. Successful OAuth alone does not establish free-plan access to every operation. Describe only capabilities exposed by the live server; do not promise habit creation or other absent tools.
