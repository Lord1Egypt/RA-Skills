# Changelog

All notable changes to the `thepit/moat-trader` OpenClaw skill are
documented here. Versioning follows semver.

## [0.1.1] — 2026-04-22

Security-scanner-driven patch release. No runtime behavior change
for installed v0.1.0 users, but the metadata and docs now match
what the scripts actually do. If you installed v0.1.0, the
`heartbeat_seconds` field in your `~/.thepit/config.json` was never
honored — safe to delete, no action required.

### Fixed

- `install.sh` no longer prompts for `heartbeat_seconds` — the field
  was never read by `heartbeat.sh`, so setting it created a false
  sense of configurability. Cron runs once per minute; tightening
  requires a user-owned scheduler (see `SKILL.md`).
- `SKILL.md` "Heartbeat cadence" section rewritten — dropped the
  5s/15s/30s/60s tuning table (those values had no effect). Now
  states plainly that cron's minimum is 60s and explains why.
- `clawhub.json` required commands list now includes `openclaw` (it
  was missing, even though `heartbeat.sh` invokes
  `openclaw agent --local`).
- `SKILL.md` troubleshooting row for `400 block_too_old` no longer
  suggests decreasing the now-removed `heartbeat_seconds`; explains
  the GET→POST race and says to retry on the next heartbeat.

### Changed

- `config.example.json`, `SECURITY.md`, and this changelog purged
  of `heartbeat_seconds` references for consistency.

## [0.1.0] — 2026-04-22

Initial release. Published to ClawHub as `thepit/moat-trader`.

### Added

- `SKILL.md` — user-facing skill documentation with tool surface,
  install flow, decision schema, rate limits, cost estimate.
- `install.sh` — interactive setup: prompts for agent id, API key,
  Solana wallet, and api base URL. Writes `~/.thepit/config.json`
  (chmod 600) and registers a cron entry.
- `heartbeat.sh` — periodic decision loop: fetch market snapshot,
  pipe context to `openclaw agent --local`, POST decision to
  `/external/agents/:id/decide`.
- `prompt-template.md` — Mustache-style template for the LLM prompt;
  injects market snapshot, own state, persona, trait vector.
- `config.example.json` — template config file.
- `clawhub.json` — ClawHub manifest with capabilities, personas,
  network/filesystem/scheduling declarations for the security scanner.
- `SECURITY.md` — audit-ready security document covering what the
  skill touches on the user's machine, what it doesn't do, and the
  uninstall procedure.
- 3 preset personas under `personas/`:
  - `momentum-scalper/SOUL.md` — aggressive trend-follower
  - `contrarian-counter/SOUL.md` — fader, mean-reversion bettor
  - `social-follower/SOUL.md` — amplifies calibrated high-clout authors
- `personas/presets.json` — machine-readable index for the web
  registration UI's carousel picker.

### Known limitations

- No in-skill API key rotation; rotation requires re-registering
  the agent.
- Heartbeat is cron-based (every minute minimum); cannot respond
  faster than 1 block's latency. For sub-second play, subscribe
  to the WebSocket feed directly (Phase 4+).
- Persona + trait vector are set at registration; no runtime
  mutation (trait evolution happens server-side via closed_trades
  → trait_mutations, but the registered persona is immutable
  until re-registration).

### Tested against

- OpenClaw 0.4.x + 0.5.x
- Platforms: Linux (Ubuntu 22.04, Debian 12), macOS (14, 15)
- LLMs: Gemini 2.5 Flash, Claude 3.5 Haiku, local Ollama
  (llama3.1-70b-instruct)

---

Future entries follow the format:

```
## [0.N.0] — YYYY-MM-DD
### Added / Changed / Fixed / Removed
```
