---
name: helena
description: Use Helena, Enrich Labs' AI marketing agent, to research, plan, create, schedule, publish, and analyze marketing for a connected brand. Use when the user asks for Helena or Enrich Labs, or wants cross-channel marketing work performed through their connected Enrich Labs account.
---

# Helena

Helena is a separate marketing agent with the user's Enrich Labs brand context and connected marketing platforms. Send marketing work to Helena when it benefits from that context or those integrations; answer simple general marketing questions directly.

## Connect Helena

Helena requires an Enrich Labs account with MCP access. Some capabilities also require a connected marketing platform, sufficient credits, or a higher Enrich Labs plan.

1. Inspect the current configuration with `openclaw mcp show helena --json`.
2. If `helena` is missing, tell the user that setup will add Enrich Labs as a remote MCP server and open a browser for sign-in. After they agree, run:

   ```bash
   openclaw mcp set helena '{"url":"https://agent.enrichlabs.ai/api/mcp","transport":"streamable-http","auth":"oauth"}'
   openclaw mcp login helena
   ```

3. If `helena` already points somewhere else, do not overwrite it without explicit confirmation. If it has the correct URL but needs authorization, run `openclaw mcp login helena`.
4. Never ask the user to paste an Enrich Labs password, OAuth code, access token, or refresh token into chat. Let the browser flow handle credentials. In a headless environment, follow the safe `--code` fallback printed by OpenClaw.
5. Verify the connection with `openclaw mcp doctor helena --probe`. If the tool is not available in the current conversation afterward, ask the user to start a new conversation or restart their OpenClaw gateway.

If Enrich Labs reports that MCP access is unavailable for the selected brand, explain the account or plan requirement and direct the user to <https://enrichlabs.ai/mcp>. Do not retry in a loop.

## Delegate marketing work

Use the MCP tool from the `helena` server whose underlying name is `send_turn`.

- Send a clear, self-contained `message` containing the user's goal, audience, constraints, relevant dates, and requested output.
- Omit `sessionId` for a new task. Reuse the returned `sessionId` for related follow-ups, but not for unrelated work.
- Preserve the user's approval boundary. If they asked for a plan, draft, or analysis, explicitly tell Helena not to publish, send, spend, delete, or change live data. Only request those actions when the user clearly authorized them.
- Clarify before requesting an ambiguous action that could publish content, contact people, spend money, change a live campaign, or delete data.
- Do not include unrelated secrets or private conversation history in the message.
- Report Helena's actual result without inventing success. Preserve useful links, mention actions taken, and render returned image assets inline when supported.

When Helena asks a necessary follow-up question, ask the user and then continue with the same `sessionId`.
