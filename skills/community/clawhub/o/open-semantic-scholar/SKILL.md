---
name: open-semantic-scholar
description: Open Semantic Scholar in Brave for academic research and paper discovery. Use when the user asks to use Semantic Scholar for this purpose.
---

# open-semantic-scholar

Open Semantic Scholar in Brave for academic research and paper discovery.

## Browser behavior

1. Focus the existing Brave browser if it is running.
2. Reuse a relevant existing tab when possible.
3. Navigate directly to `https://www.semanticscholar.org/`.
4. Wait for the page to load.
5. Verify the expected Semantic Scholar page or search results are visible.

## Scope

This skill only opens the requested page. It does not submit forms, place orders, make payments, or modify account settings.

## Authentication and privacy

- Reuse an existing authenticated browser session when available.
- Never enter passwords, authentication codes, API keys, payment details, or other credentials.
- If authentication is required, stop at the login page and tell the user.
- Do not create accounts.

## Success condition

The expected Semantic Scholar page is visibly loaded and verified.
