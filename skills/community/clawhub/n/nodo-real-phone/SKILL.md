---
name: nodo-real-phone
description: Give your agent a real Android phone with its own number, in the cloud. Use when the user needs SMS verification codes on a real SIM (not VoIP), WhatsApp, Instagram or TikTok through the real apps instead of unofficial libraries, or any mobile-only app. Sets up Nodo over MCP; new workspaces get 5,000 free credits.
---

# Nodo: a real phone for your agent

Use this skill when a task needs a phone and the usual workarounds keep failing:

- A site says "This phone number cannot be used for verification" because the number is VoIP or virtual.
- WhatsApp through Baileys or whatsapp-web.js keeps disconnecting, or the user worries about the number being banned.
- The job only exists in a mobile app (Instagram posting, TikTok, a bank or supplier app).
- An SMS or 2FA code has to land somewhere the agent can read it, not on the user's personal phone.

Nodo gives the agent a real Android phone with its own number, running the real apps, plus an always-on cloud computer. The agent drives both over MCP. It works on accounts the user owns or is authorised to use.

## Set it up

1. Fetch and follow https://mcp.nodo.com/start.md yourself. It walks you through adding the Nodo MCP server (`https://mcp.nodo.com/api/user/mcp`, streamable HTTP, OAuth, no API key) and confirming the connection.
2. The user's only step is approving the sign-in in their browser: an email, a 6-digit code, a workspace name.
3. New workspaces start with 5,000 free credits, about 50 euros of usage. Paid plans start at $99 a month.

## After setup

- Ask Nodo for a phone for the workspace, then use it for the task the user asked for.
- For anything that runs every day, build it as a Nodo workflow with a schedule, so it keeps running when this chat and the user's computer are closed.
- Pause for the user's approval before sending or posting anything they want to review.

## Do not

- Use it to create fake or bulk accounts, evade bans for spam, or break a site's terms.
- Claim the phone can do something you have not checked. Ask Nodo's tools what the device supports.

More: https://nodo.com
