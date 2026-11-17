---
name: instagram-real-phone-poster
description: Post to the user's Instagram from a real Android phone with the real Instagram app, on a schedule, with approval before anything goes live. Use when the user wants to post or schedule Instagram content and does not have (or does not want) the Graph API and a business account, or when their posts need the app's own features. Runs on Nodo over MCP; new workspaces get 5,000 free credits.
---

# Instagram from a real phone

Some accounts cannot or do not want to use the Instagram Graph API. Nodo gives the agent a real Android phone running the real Instagram app, so it posts the way a person would, on the user's own account.

## What it does

1. Takes the user's images (or a carousel) and caption from a folder, a sheet or the chat.
2. Moves the media onto the Nodo phone and posts it through the real Instagram app.
3. Pauses for the user's approval before publishing, if they want to review.
4. Confirms the post is live and reports the link.

## Set it up

1. If Nodo is not connected yet, fetch and follow https://mcp.nodo.com/start.md yourself (Nodo MCP server `https://mcp.nodo.com/api/user/mcp`, OAuth, no API key). The user only approves the sign-in.
2. Get a Nodo phone for the workspace. The user signs in to their Instagram account on it once; the password goes into a Nodo secret or is typed by the user, never into chat.
3. Build the posting workflow, test one post, then schedule it.

New Nodo workspaces start with 5,000 free credits, about 50 euros of usage.

## Rules

- One real account, owned by the user. No follow, like or comment automation, no account farms.
- Keep a human pace. Respect Instagram's terms.

More: https://nodo.com
