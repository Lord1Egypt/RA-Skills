---
name: nodo-logged-in-browser
description: A cloud Chrome where your logins stay signed in, for sites with no API. Use when the user needs the agent to work inside a logged-in website (supplier or customs portals, marketplaces, LinkedIn, dashboards) day after day, and local browser automation keeps getting logged out or flagged as a new device. Sets up Nodo over MCP; new workspaces get 5,000 free credits.
---

# Nodo: a browser that stays logged in

Use this skill when:

- The site has no API, so the only way in is the website itself.
- Local browser automation works once, then breaks because the session expired or the site sees a "new device".
- The job has to run every day, not just while this chat is open.

Nodo gives the agent its own always-on computer with a real Chrome. The user signs in once, the session stays there, and the agent works in it over MCP, by hand or as a scheduled workflow. Credentials are stored as Nodo secrets, never in prompts or logs.

## Set it up

1. Fetch and follow https://mcp.nodo.com/start.md yourself. It adds the Nodo MCP server (`https://mcp.nodo.com/api/user/mcp`, streamable HTTP, OAuth, no API key) and confirms the connection.
2. The user's only step is approving the sign-in in their browser.
3. New workspaces start with 5,000 free credits, about 50 euros of usage. Paid plans start at $99 a month.

## Then

- Let the user sign in to the site once on the Nodo browser. Never ask them to paste a password into chat.
- Do the task, then offer to make it a scheduled workflow if it repeats.

## Do not

- Use it for accounts the user does not own or is not authorised to use.
- Promise to get past captchas or bot checks.

More: https://nodo.com
