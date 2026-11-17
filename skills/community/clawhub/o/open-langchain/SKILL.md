---
name: open-langchain
description: Open the LangChain website in the user's Brave browser and click "Start building" to take the user into the LangChain/LangSmith builder dashboard. Use when the user asks to open LangChain, start building with LangChain, or go to the LangChain dashboard.
---

# Open LangChain

Open LangChain and take the user directly from the public LangChain website to its builder/dashboard experience.

## Primary workflow

1. Use the host's browser/computer automation capability.
2. Open or focus the user's Brave browser.
3. Navigate to:
   `https://www.langchain.com/`
4. Wait for the page to load.
5. Locate the visible **"Start building"** call-to-action.
6. Click **"Start building"**.
7. Wait for navigation to complete.
8. Verify that the resulting page is the LangChain/LangSmith building dashboard or builder experience.
9. Report success only after the destination is visibly loaded.

## Existing browser session

Prefer the user's existing Brave session.

- If Brave is already open, reuse it.
- Open LangChain in a new tab when possible.
- If a LangChain tab already exists, focus it rather than creating unnecessary duplicates.
- Preserve the user's existing browser login/session state.

## Button handling

The homepage may contain more than one call-to-action with similar wording.

Prefer the main, visible **"Start building"** button associated with getting started with LangChain/LangSmith.

Use the rendered text and surrounding UI to identify the correct button rather than relying on fixed screen coordinates.

If the button is not immediately visible:
- scroll enough to locate it,
- or inspect accessible/UI text,
- then click it.

Do not click unrelated "Get a demo" buttons.

## Dashboard verification

After clicking "Start building", verify that the destination has actually loaded.

Acceptable verification signals include:
- a LangSmith/LangChain application or dashboard interface,
- a builder/project creation interface,
- recognizable LangSmith navigation or workspace UI,
- a URL/domain associated with the LangChain application.

If the destination asks the user to sign in, stop after the page is visibly loaded and tell the user that authentication is required. Do not enter credentials.

## User-request variants

- "Open LangChain" → open the LangChain homepage.
- "Open LangChain and start building" → open the homepage and click Start building.
- "Take me to the LangChain dashboard" → open LangChain and use Start building to reach the dashboard/builder.
- "Start building with LangChain" → perform the complete workflow.

## Failure handling

If the LangChain site cannot be reached, report the actual browser state.

If "Start building" is unavailable or the UI has changed, do not claim success. Report what was visible.

If authentication is required, leave the browser at the authentication page and ask the user to complete login themselves.

## Safety and privacy

Never request, expose, copy, or store passwords, cookies, API keys, or session tokens.

This skill only performs navigation and a user-requested button click.
