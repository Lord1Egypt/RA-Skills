# HTML Sharing Spec

Date: 2026-04-04

## Goal

Move HTML sharing into `kai-html-export` with a lightweight flow that works locally and stays safe in hosted sandboxes.

## Requirements

- Add a unified entrypoint: `scripts/share-html.py`
- Default provider is Cloudflare Pages
- Keep Vercel as an optional fallback provider
- Automatic sharing is disabled in cloud sandbox / hosted multi-tenant environments
- When automatic sharing is disabled, return manual guidance instead of starting login or deploy flows
- Keep repository dependencies unchanged; any deploy CLI remains optional and runtime-only

## Provider Scope

### Cloudflare Pages

- First version targets static `*.pages.dev` hosting only
- Support a single HTML file or a folder containing `index.html`
- Auto-stage common relative assets when the input is a single HTML file
- Reuse a stable Pages project name derived from the input path unless the user overrides it

### Vercel

- Reuse the existing deploy helper
- Keep public URL behavior by clearing `ssoProtection`

## Environment Rules

- Local machine: automatic sharing allowed
- Hosted sandbox: automatic sharing blocked
- Explicit env overrides must exist so the host can force allow/deny behavior

## Non-Goals

- No persistent multi-tenant auth flows
- No account key storage inside the skill
- No custom domain management
- No automatic sharing in hosted cloud sandboxes
