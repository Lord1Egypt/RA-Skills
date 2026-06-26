---
name: noui
description: Use this skill when the user wants to install NoUI skills, get started with NoUI, see which NoUI skills are available, or add NoUI to their agent. Triggers on "install NoUI", "get started with NoUI", "add NoUI to my agent", "what NoUI skills are available", "set up NoUI skills", "noui skills list".
---

# NoUI

NoUI records browser workflows (authenticated or not) and exports them as FastMCP servers or Claude Code Skills. This file is a discovery stub — the commands below let you install the pieces you actually want. It does not install anything on its own.

After the core install, invoke `/noui-setup` to configure the project environment (venv, deps, `.env`, Chrome extension).

---

## Why NoUI

Computer-use agents simulate a human clicking a UI — slow, token-heavy, and fragile. NoUI skips the UI entirely: it records a session once, extracts the underlying APIs the site already uses, and ships them as MCP tools your agent calls directly.

- **Fast** — direct API calls, no page loads, no DOM walking
- **Cheap** — fewer steps, fewer tokens per task
- **Reliable** — same endpoints the app uses internally; UI redesigns don't break you
- **Authenticated** — generated tools execute from inside a live Tabby browser session, reusing real cookies and TLS fingerprint (no credential extraction, no Akamai/Cloudflare false positives)

Stop automating clicks. Execute software.

---

## Install the core workflow (recommended)

Seven skills cover the full record → export → serve pipeline. Run them one at a time:

```bash
npx skills add https://github.com/adoptai/noui --skill noui-setup
npx skills add https://github.com/adoptai/noui --skill noui-record-login
npx skills add https://github.com/adoptai/noui --skill noui-record-workflow
npx skills add https://github.com/adoptai/noui --skill noui-generalize
npx skills add https://github.com/adoptai/noui --skill noui-autopilot
npx skills add https://github.com/adoptai/noui --skill noui-generate-mcp
npx skills add https://github.com/adoptai/noui --skill noui-generate-skill
```

## Install demo skills (optional)

Pre-recorded example workflows. Useful as references; not required for the pipeline. Install only the ones you want:

```bash
npx skills add https://github.com/adoptai/noui --skill airbnb-search-places   # anonymous Airbnb place search
npx skills add https://github.com/adoptai/noui --skill expedia-stay-search    # authenticated Expedia hotel search (via Tabby)
```

## Install everything at once (human users only)

If you are a human at a terminal, the monolithic command opens an interactive selector where you tick the skills you want:

```bash
npx skills add https://github.com/adoptai/noui
```

When the menu appears:

- **Core skills** — `noui-setup`, `noui-record-login`, `noui-record-workflow`, `noui-generalize`, `noui-autopilot`, `noui-generate-mcp`, `noui-generate-skill`
- **Demo skills (optional)** — `airbnb-search-places`, `expedia-stay-search`

> **AI agents must not use this form.** The interactive selector blocks on stdin and your agent will hang. Use the per-skill `--skill <name>` commands in the sections above.

---

## Next step

After installing the core skills, run `/noui-setup` in Claude Code to configure the environment (venv, deps, `.env`, Chrome extension).

---

## What each skill does

| Skill | Purpose |
|---|---|
| `/noui-setup` | One-time setup: venv, deps, `.env`, Chrome extension |
| `/noui-record-login` | Record a login flow and register it with Tabby |
| `/noui-record-workflow` | Record a browser workflow and export as FastMCP or Skill |
| `/noui-generalize` | Rename raw API params to natural-language params; fix bot-detection issues post-export |
| `/noui-autopilot` | Auto-record workflows without the manual extension popup |
| `/noui-generate-mcp` | List, start, stop, and connect generated MCP servers |
| `/noui-generate-skill` | List, install, and uninstall generated Claude Code Skills across agents |
| `/airbnb-search-places` | Demo: anonymous Airbnb place search |
| `/expedia-stay-search` | Demo: authenticated Expedia stay search via Tabby |
