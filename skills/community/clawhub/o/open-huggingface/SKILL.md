---
name: open-huggingface
description: Open Hugging Face in the user's Brave browser and take the user to the Hugging Face homepage. Reuse an existing Hugging Face tab/session when possible. Use when the user asks to open, visit, or go to Open Hugging Face.
---

# Open Hugging Face

Open Open Hugging Face in the user's Brave browser.

## Browser behavior

1. Focus the existing Brave browser if it is already running.
2. Reuse an existing Open Hugging Face tab when one is already open instead of creating a duplicate.
3. Otherwise navigate to:
   `https://huggingface.co/`
4. Wait for the page to load.
5. Verify that the destination is clearly the expected Open Hugging Face website before reporting success.

## Authentication

- Reuse the user's existing authenticated browser session if the site provides one.
- Do not enter passwords, authentication codes, API keys, or other credentials.
- If authentication is required, stop at the login page and tell the user that they need to sign in.
- Do not create accounts or modify account settings.

## Scope

This skill only opens and verifies the website. It does not create, edit, delete, publish, deploy, download, or otherwise modify content unless the user explicitly asks in a separate instruction.

## Duplicate-tab handling

Prefer an existing matching tab. If none exists, open one destination tab only.

## Success condition

The requested website is visibly loaded in Brave and the destination has been verified.
