# Changelog

## v2.1.0 (2026-05-23)

- **New:** `sync` command — unified guard + rolling in 1 call (replaces `guard`)
- **New:** Rolling session v2 — DB-backed, 2-phase (Context Guard → Rolling auto)
- **New:** Server endpoint `POST /v1/bot/session/sync` — 1 call does everything
- **Changed:** 1 cron only (5 min, `sync`) replaces 2 crons (guard 30m + sync 1h)
- **Changed:** Server decides action (none/warning/compact/rotate) — zero client logic
- **Changed:** State persisted in DB (survives server restart)
- **Kept:** `guard` command still works (alias for `sync`)
- **Kept:** `track` command for bots with per-message hooks

## v2.0.0 (2026-05-23)

- **Breaking:** Simplified API — 6 commands only (store, recall, bootstrap, save, profile, health)
- **New:** `bootstrap` — 3-tier wake-up (800 tokens, identity → context → details)
- **New:** `profile` — cognitive profile (persona + mood + goals + entities + procedures)
- **New:** `save` — replaces compact, simpler interface
- **Removed:** handoff commands (rolling session handles this server-side)
- **Removed:** context guard cron (rolling session replaces token-based switching)
- **Removed:** reflect command (server handles consolidation automatically)
- **Changed:** All session management now server-side (zero client logic)
- **Changed:** memory types expanded: +procedure, +life_event, +identity

## v1.0.0 (2026-05-10)

- Context Guard v4: reads token usage from OpenClaw sessions.json
- Session handoff: zero-gap session switching

## v0.5.0 (2026-04-20)

- Initial release with store/recall/compact/restore
- Session handoff commands
