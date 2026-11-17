---
name: open-pinterest
description: Open Pinterest in the user's Brave browser and take the user to the Pinterest homepage. Use when the user asks to open, visit, or go to Pinterest.
---

# Open Pinterest

Open Pinterest in the user's Brave browser.

## Browser behavior

1. Focus the existing Brave browser if it is already running.
2. Reuse an existing Pinterest tab when one is already open instead of creating a duplicate.
3. Otherwise navigate to `https://www.pinterest.com/`.
4. Wait for the page to load.
5. Verify that Pinterest is visibly loaded before reporting success.

## Authentication

- Reuse the user's existing authenticated browser session when available.
- Never enter passwords, authentication codes, API keys, or other credentials.
- If Pinterest asks the user to sign in, stop there and tell the user authentication is required.
- Do not create accounts or modify account settings.

## Scope

This skill only opens and verifies Pinterest. It does not search, post, like, comment, follow, message, upload, purchase, or otherwise modify the user's account unless explicitly asked separately.

## Duplicate-tab handling

Prefer an existing Pinterest tab. If none exists, open one destination tab only.

## Success condition

The Pinterest homepage is visibly loaded in Brave and the destination has been verified.
