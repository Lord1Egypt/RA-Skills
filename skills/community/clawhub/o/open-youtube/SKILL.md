---
name: open-youtube
description: Open YouTube in the user's Brave browser and take the user to YouTube's homepage. Use when the user asks to open YouTube, go to YouTube, or visit YouTube.
---

# Open YouTube

Open YouTube in the user's Brave browser.

## Browser behavior

1. Focus the existing Brave browser if it is already running.
2. Reuse an existing YouTube tab when one is already open instead of creating a duplicate.
3. Otherwise navigate to:
   `https://www.youtube.com/`
4. Wait for the page to load.
5. Verify that YouTube is visibly loaded before reporting success.

## Authentication

- Reuse the user's existing authenticated browser session when available.
- Never enter passwords, authentication codes, API keys, or other credentials.
- If YouTube asks the user to sign in, stop there and tell the user authentication is required.
- Do not create accounts or modify account settings.

## Scope

This skill only opens and verifies YouTube. It does not search for videos, play videos, subscribe, like, comment, upload, create playlists, or otherwise modify the user's YouTube account unless the user explicitly asks for those actions separately.

## Duplicate-tab handling

Prefer an existing YouTube tab. If none exists, open one destination tab only.

## Success condition

The YouTube homepage is visibly loaded in Brave and the destination has been verified.
