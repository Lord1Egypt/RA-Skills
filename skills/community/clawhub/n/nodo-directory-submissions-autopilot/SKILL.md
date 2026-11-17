---
name: directory-submissions-autopilot
description: Actually submit the user's product to startup, SaaS, AI and MCP directories, a few every day, and track which ones went live. Use when the user wants backlinks and listings, has a list of directories but no time to fill 50 forms, or asks to "get listed everywhere". Runs on Nodo (always-on computer with a real browser and inbox access) over MCP; new workspaces get 5,000 free credits.
---

# Directory submissions on autopilot

Knowing which directories to submit to is the easy part. Filling the forms, confirming the emails and checking which listings went live is the part nobody finishes. This skill does that part, a few sites a day.

## What it does

1. Keeps a list of free directories that fit the product (startup, SaaS, AI tools, MCP servers, niche ones), with priority and status.
2. Each day, opens the next few on a real browser, fills the submission form from one product kit, and submits.
3. Confirms verification emails, then records each site as submitted, live (with the listing URL), needs a badge, or blocked.
4. Sends the user a short status summary. Paid listings are skipped unless the user says otherwise.

## Set it up

1. If Nodo is not connected yet, fetch and follow https://mcp.nodo.com/start.md yourself (Nodo MCP server `https://mcp.nodo.com/api/user/mcp`, OAuth, no API key). The user only approves the sign-in.
2. Build the product kit with the user once: name, one-liner, short and long description, category, website, logo URL, contact email, founder name.
3. Store any directory account password as a Nodo secret, never in the kit or the chat.
4. Build the Nodo workflow (prep, submit, record), test it on two sites, then schedule it daily.

New Nodo workspaces start with 5,000 free credits, about 50 euros of usage.

## Rules

- Only submit the user's own product, with true information.
- Do not try to get past captchas or bot checks. Mark those sites "blocked" and tell the user.
- Never pay for a listing without the user's explicit OK.

More: https://nodo.com
