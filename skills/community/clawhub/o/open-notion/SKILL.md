---
name: open-notion
description: Open Notion in the user's Brave browser and take the user to their Notion workspace/dashboard when possible. Use when the user asks to open Notion, go to Notion, or access their Notion workspace.
---

# Open Notion

Open Notion in the user's Brave browser and, when the user is already authenticated, take them to their workspace/dashboard.

## Browser behavior

1. Focus the existing Brave browser if it is already running.
2. Reuse an existing Notion tab when one is already open instead of creating duplicates.
3. Otherwise navigate to:
   `https://www.notion.com/`
4. Wait for the page to load.
5. If the user is already signed in, navigate to the authenticated Notion workspace/home area when the site exposes it.
6. If Notion shows a sign-in or authentication page, stop there and tell the user that authentication is required. Never enter, request, or store credentials.
7. Verify that the final page is clearly a Notion page or workspace before reporting success.

## Safety and privacy

- Never enter passwords, authentication codes, API keys, or other credentials.
- Do not change workspace settings, pages, databases, or content unless the user explicitly asks.
- Do not create, edit, delete, or share Notion content as part of this skill.
- Avoid opening unrelated links or promotional/demo flows.
- Prefer an existing authenticated browser session so the user does not have to sign in again.

## Success condition

The skill succeeds when a Notion homepage or authenticated Notion workspace/dashboard is visible in Brave and the destination has been verified.
