---
name: hermes-web-tools
description: "Use when Hermes web tools fail or need configuring."
version: 1.0.0
author: Hermes Agent
license: MIT-0
metadata:
  openclaw:
    os: [linux]
    homepage: https://github.com/mina-atef-00/agent-skills
  hermes:
    tags: [hermes, web, web-search, web-extract, config, troubleshooting]
    related_skills: [hermes-agent]
---

# Hermes Web Tools (web_search / web_extract)

## Overview

How backend selection works for Hermes' two web tools, and how to diagnose a
broken `web_extract`/`web_search`. All providers now ship as bundled plugins
(`web-firecrawl`, `web-tavily`, `web-exa`, `web-parallel`, `web-keenable`,
`web-searxng`, `web-brave-free`, `web-ddgs`, `web-xai`). Plugins showing
"not enabled" in `hermes plugins list` is NORMAL — they load on demand; the
config selection is what matters.

## USER RULE — investigate first, change nothing without explicit command

The operator requires read-only investigation for Hermes config/troubleshooting tasks:
diagnose, present fix options with exact commands, and WAIT for him to pick
one. Do not run `hermes config set`, edit config.yaml, or enable/disable
anything on your own initiative, even when the fix is obvious. This overrides
the general "prefers autonomous execution" tendency.

## Backend selection (priority order, per capability)

1. `web.search_backend` / `web.extract_backend` (per-capability override)
2. `web.backend` (shared fallback; `nous` = managed Tool Gateway)
3. Auto-detect from env vars — ONLY if no selection was ever stored

**Strict selection:** a stored name is used as-is, no availability probe, no
silent swap. An unknown name surfaces an honest error naming the bad
selection. Once any selection exists, adding keys to `.env` does NOT reroute
traffic — a stale selection silently blocks otherwise-working credentials.

**Keyless free-tier ring:** zero-credential installs rotate across Exa,
Parallel, Tavily, Firecrawl, Keenable public free tiers with automatic
failover. Plus a one-shot keyless *rescue* for keyed backends on failure
(never sticky). Disable via `web.keyless_fallback: false` /
`web.keyless_rescue: false`.

## Valid backend names

| Name | Search | Extract | Notes |
|---|---|---|---|
| `tavily` | ✔ | ✔ | 1k searches/mo free key |
| `exa` | ✔ | ✔ | 1k/mo free key |
| `firecrawl` | ✔ | ✔ | keyless cloud when selected; default |
| `parallel`, `keenable` | ✔ | ✔ | keyless ring members |
| `ddgs`, `searxng`, `brave-free`, `xai` | ✔ | — | search-only |

Anything else (e.g. `trafilatura` — a Python extraction library, never a
valid Hermes backend name) errors with "no registered web extract provider
has that name".

## Diagnosis recipe

0. **Differential test FIRST — is the tool broken, or just this site?** Call the same
   tool on a known-good URL (`https://example.com`,
   `https://en.wikipedia.org/wiki/Web_scraping`). If it returns full content there,
   the original failure is *site-specific*, NOT a tool fault — stop diagnosing the
   tool/config and investigate the target site instead. This one test prevents
   pivoting into hours of needless config poking or SPA-bundle reverse-engineering
   when the only real issue is that the page renders client-side. (Session lesson:
   an "empty content" `web_extract` on one URL prompted a full Docusaurus-bundle
   reverse-engineering detour that a 2-URL differential test would have made
   unnecessary. The user explicitly redirected: "why is the web tool failing? you
   should check it out" — i.e. diagnose the failure, don't silently work around it.)
1. Reproduce: call the tool on the failing URL; read the exact error string.
2. `grep -n -A5 '^web:' ~/.hermes/config.yaml` — check stored selections.
3. `grep -oE '^(TAVILY|EXA|FIRECRAWL|PARALLEL|KEENABLE|BRAVE_SEARCH)_API_KEY' ~/.hermes/.env` — what credentials exist (names only; values are secrets).
4. Validate the stored name against the table above. Unknown name = root cause.
5. Check `hermes plugins list` for the matching `web-*` plugin (informational only).
6. Present fix options; wait for the operator's pick. Fixes need a NEW session (`/reset`) — tool config is not re-read mid-conversation.

## Common pitfalls

- **Stale/typoed selection is the #1 cause** of "web tool broken" reports. The strict-selection design (commit d7119ea2) means it errors instead of falling back — the error names the bad value directly.
- **Search can work while extract is broken**: per-capability keys resolve independently (e.g. `search_backend: ddgs` fine, `extract_backend: <invalid>` broken).
- **`hermes config set web.<key> ""`** clears a selection and re-enables auto-detect.
- Tool/toolset config changes take effect on next session, never mid-session.
- **Empty `web_extract` on a JS-SPA site is a site limitation, not a tool bug.** Sites
  built with Docusaurus / Next.js / Vite / plain SPAs serve an HTML shell
  (`<div id="__docusaurus">`) whose article text lives in JS chunks the fetcher can't
  execute. `web_extract` (Tavily) legitimately returns empty there. Confirm with the
  Step-0 differential test; if you still need the content, fetch via `curl -sSL` in the
  terminal — a Docusaurus page's real markdown is referenced by the route map inside
  `main.*.js` (search for `@site/docs/...md` keys). Do NOT conclude the tool is broken
  from a single empty extract.

## References

- `references/backend-selection-internals.md` — code paths in `tools/web_tools.py`, resolution chain, incident transcript.
