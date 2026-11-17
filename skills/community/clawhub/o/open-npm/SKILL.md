---
name: open-npm
description: Open npm in Brave. Use when the user asks to use npm for this purpose.
---

# open-npm

Open npm in Brave.

## Browser behavior

1. Focus the existing Brave browser if it is running.
2. Reuse a relevant existing tab when possible.
3. Navigate directly to `https://www.npmjs.com/`.
4. Wait for the page to load.
5. Verify the expected npm page or search results are visible.

## Scope

This skill only opens the requested page. It does not submit forms, place orders, make payments, or modify account settings.

## Authentication and privacy

- Reuse an existing authenticated browser session when available.
- Never enter passwords, authentication codes, API keys, payment details, or other credentials.
- If authentication is required, stop at the login page and tell the user.
- Do not create accounts.

## Success condition

The expected npm page is visibly loaded and verified.
