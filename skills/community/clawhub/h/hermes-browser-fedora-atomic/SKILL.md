---
name: hermes-browser-fedora-atomic
version: 1.0.0
author: Hermes Agent
license: MIT-0
description: "Use when Hermes browser fails on Fedora Atomic / bootc."
metadata:
  openclaw:
    os: [linux]
    homepage: https://github.com/mina-atef-00/agent-skills
  hermes:
    tags: [hermes, browser, chromium, fedora-atomic, bootc, playwright, agent-browser, troubleshooting, config]
---

# Hermes Browser on Fedora Atomic

## Overview
Hermes has four browser backends (CDP -> Camofox -> agent-browser local Chromium -> Browserbase). On a Fedora Atomic / bootc (immutable) host the default config can fail in two ways that look identical from the outside ("browser tool fails"), and the naive fix (point a CDP URL at a manually-launched browser) is fragile across reboots. This skill captures the diagnosis and the durable local-mode fix.

## When to Use
- `browser_exec` or built-in `browser_*` tools fail with "Nous Tool Gateway not available" or "default browser is not a supported Chromium browser".
- User is on Fedora Atomic / bootc and you are setting up local browser automation.
- `web_extract` returns empty for a site that clearly has content (Docusaurus / Next.js SPA).
- User wants Hermes to use a local Chromium while keeping a non-Chromium browser (e.g. Zen / Firefox) as their OS default.

## Backend resolution (engine: auto)
Priority at runtime: CDP (`cdp_url` / `BROWSER_CDP_URL`) -> Camofox (`CAMOFOX_URL`) -> agent-browser local Chromium -> Browserbase. `browser.cloud_provider` overrides: `local` forces the built-in local Chromium; `browser-use` / `browserbase` / `firecrawl` route to cloud. `browser.use_gateway: true` makes browser-use prefer the **paid Nous Portal Tool Gateway**.

## The two failure modes (diagnose before fixing)
| Symptom | Root cause | Fix |
|---|---|---|
| "Nous Tool Gateway is not available (not entitled or unreachable)" | `browser.use_gateway: true` routes to paid Nous Portal gateway you are not subscribed to | `use_gateway: false` |
| "default browser is not a supported Chromium browser" (real-profile fallback) | `browser.use_real_profile: true` clones your **OS-default browser's** profile into a Chromium; fails if default is Gecko/Firefox (e.g. Zen) | `use_real_profile: false` (clean throwaway Chromium profile; OS default untouched) |

Both are config issues, NOT a broken web tool. `web_extract` / `web_search` work independently and were never the problem.

## The durable fix (local mode)
1. In `~/.hermes/config.yaml` under `browser:`:
   ```yaml
   cloud_provider: local
   use_gateway: false
   use_real_profile: false
   ```
   (`cdp_url` is only consumed by `browser_exec` / cloud modes — see below; safe to leave or remove.)
2. Install Hermes's own Chromium (user-space, no system image change):
   ```bash
   npx --yes agent-browser install     # DO NOT add --with-deps on Fedora Atomic
   ```
   Lands at `~/.agent-browser/browsers/chrome-<ver>/` (survives reboot; not in `/tmp`).
3. Built-in `browser_*` tools now auto-launch / reap this Chromium. Reboot-safe — there is no static port to keep alive.

### Why NOT `--with-deps`
`--with-deps` runs the OS package manager for Chromium's shared libs. On Fedora Atomic that path assumes classic `dnf` and will not use `rpm-ostree` — it fails or behaves wrongly. Skip it: the desktop / flatpak stack already provides the needed libs, so local Chromium launches fine without it. If a missing `.so` appears later, layer just that lib with `sudo rpm-ostree install <lib>` deliberately.

## CRITICAL: browser_exec != built-in browser tools
- **Built-in `browser_*` tools** (navigate / snapshot / click / type / scroll …) ride Hermes's managed local Chromium. This is the working path.
- **`browser_exec`** is the separate **Browser-Use Python harness**. It reads `cdp_url` / `BU_CDP_URL` and expects a **dedicated, externally-running** Chrome on that port (e.g. `:9222`) — it does NOT use Hermes's managed Playwright Chromium. As of this version it has also failed with `ModuleNotFoundError: No module named 'browser_helpers'` (harness venv packaging bug). To verify local mode, do NOT rely on `browser_exec`; use the built-in tools or the `agent-browser` CLI (see below). Making `browser_exec` work requires both a repaired harness venv AND a running `:9222` Chrome — a separate, lower-value rabbit hole.

## Verification recipe (no browser_exec)
```bash
# navigate + dump rendered text of any URL (proves local Chromium + SPA rendering)
npx --yes agent-browser read https://docs.b.ai/llmservice
# confirm the browser process reaps after close (no orphan / no dead port)
npx --yes agent-browser close
pgrep -af "agent-browser/browsers/chrome" | grep -v pgrep || echo "reaped OK"
```

## Pitfalls
- **`web_extract` empty on SPAs.** Docusaurus / Next.js shells return only an empty `<div>` to headless fetchers; content lives in JS chunks. Either drive a real browser (local Chromium) or, read-only, `curl` the page's JS bundle and grep the route->chunk map. `web_extract` itself is fine on normal server-rendered sites.
- **`cdp_url` is not "inert."** It is ignored by built-in tools in local mode but is the live target for `browser_exec`. Don't assume removing the running `:9222` browser is consequence-free if `browser_exec` is still enabled.
- **Don't install a flatpak / system Chromium "for Hermes."** Local mode downloads its own Chrome-for-Testing; a separate flatpak install is redundant and unused (safe to remove).
- **Keep the user's OS default browser.** `use_real_profile: false` decouples Hermes from the OS default — Zen (or any Gecko) can stay default.

## See also
- `references/commands-and-config.md` — exact config diff, install transcript, diagnostic table.
- `hermes-browsers` skill (bundled) — backend architecture and Camofox / Browserbase setup (do not duplicate here).
