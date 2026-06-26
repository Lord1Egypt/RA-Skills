# OpenClaw Config Map

Config file: `~/.openclaw/openclaw.json` (JSON5 format — comments and trailing commas allowed).

All fields are optional — OpenClaw uses safe defaults when omitted.

## Hot-Reload (no restart needed)

These changes take effect automatically when the config file is saved.

| Key | Controls |
|-----|----------|
| `agents` | Agent definitions, defaults (workspace, models, memory, sandbox, compaction, heartbeat, subagents, context pruning, media models, block streaming, typing) |
| `agents.defaults.model` | Primary model, fallbacks, per-model params, image/PDF/music/video generation models |
| `agents.defaults.models` | Model catalog — aliases, context params, transport |
| `agents.list` | Named agent array with per-agent overrides (identity, thinkingDefault, runtime, groupChat) |
| `channels` | All channel providers (Discord, Slack, Telegram, WhatsApp, Signal, BlueBubbles, Google Chat, Mattermost) |
| `channels.defaults` | Shared group policy, heartbeat, DM policy, context visibility defaults |
| `channels.discord` | Accounts, guilds, channel allowlists, voice config |
| `channels.modelByChannel` | Pin specific channel IDs to specific models |
| `bindings` | Channel-to-agent routing rules (agentId, match criteria) |
| `models` | Provider config (baseUrl, API type, catalog mode) |
| `auth` | Auth profiles, cooldown settings (per-provider), profile ordering, overloaded/rate-limited rotation |
| `tools` | Tool profiles (minimal/coding/messaging/full), allow/deny policy, exec, media, loop detection, sandbox, experimental |
| `hooks` | Internal hooks, webhooks, HTTP ingress, Gmail integration, transforms, presets |
| `cron` | Job concurrency, session retention, run logging, retry config, failure alerting |
| `session` | Scoping (per-sender/global), DM scope, thread bindings, TTL, identity links, send policy, agent-to-agent ping-pong limits, maintenance |
| `browser` | Multi-profile browser support, SSRF policy, evaluate toggle, CDP/remote profiles |
| `logging` | Log level, console style, redaction, file path, max file size, custom redaction patterns |
| `commands` | Chat commands (/model, /reset, /bash, /config) |
| `messages` | Chunk limits, streaming, TTS, response prefix templates, ack reactions, queue modes (steer/followup/collect/interrupt) |
| `env` | Environment variables, shell env loading |
| `ui` | UI preferences and theming |
| `secrets` | Secret providers (env, file, exec), trustedDirs, passEnv, mode (json/singleValue) |
| `identity` | Gateway identity metadata (now primarily configured per-agent at agents.list[].identity) |
| `acp` | Agent Communication Protocol (enabled, backend, dispatch, streaming, allowedAgents) |
| `diagnostics` | Instrumentation, OpenTelemetry export, cache traces, stuck-session warnings |
| `talk` | Voice interface (provider, ElevenLabs config, silence timeout) |
| `canvasHost` | Agent-editable HTML/CSS/JS served over gateway port |
| `nodeHost` | Node host settings (browser proxy) |
| `skills` | Skill management (allowBundled, load dirs, install preferences, per-skill config) |
| `web` | WhatsApp/Baileys web transport (reconnect, heartbeat) |
| `meta` | Auto-managed version tracking (read-only, written by OpenClaw) |
| `wizard` | Setup wizard state (read-only, written by CLI) |
| `update` | Release channel (stable/beta/dev), auto-update settings |

## Restart Required

These changes require `openclaw gateway restart` to take effect.

| Key | Controls |
|-----|----------|
| `gateway.port` | Listening port (default: 18789, dev: 19001) |
| `gateway.bind` | Bind address |
| `gateway.auth` | Auth mode and scheme |
| `gateway.tls` | HTTPS/TLS certificates (auto-generate, certPath, keyPath, caPath) |
| `gateway.tailscale` | Tailscale integration |
| `gateway.http` | HTTP server config, OpenAI-compatible endpoints (chatCompletions, responses) |
| `gateway.reload` | Hot-reload mode itself (hybrid/hot/restart/off) |
| `discovery` | mDNS advertising, health endpoints |
| `plugins` | Extension loading, slots (memory/contextEngine), per-plugin config, allow/deny lists, bundled provider discovery, install metadata |
| `plugins.bundledDiscovery` | Whether bundled provider plugins use legacy compatibility discovery or obey `plugins.allow` |
| `gateway.controlUi` | Control UI (enabled, basePath, allowedOrigins, auth) |
| `gateway.remote` | Remote gateway connection (url, transport, token) |
| `gateway.push` | APNs push notification relay |

**Removed:** `bridge` — TCP bridge is gone; nodes connect over Gateway WebSocket. `bridge.*` keys cause validation failure.

## Hot-Reload Modes

Set via `gateway.reload`:

| Mode | Behavior |
|------|----------|
| `hybrid` (default) | Auto-applies safe changes, auto-restarts for critical ones |
| `hot` | Applies safe changes only, warns when restart needed |
| `restart` | Restarts on any config change |
| `off` | No file watching |

## Config Syntax Features

**JSON5**: Comments (`//` and `/* */`), trailing commas, unquoted keys, single-quoted strings.

**Env var references**: `${VAR_NAME}` in string values. Uppercase only. Missing var = startup error.

**Config includes**: `$include: "./file.json5"` or `$include: ["a.json5", "b.json5"]` (array = deep merge, later wins). Up to 10 levels deep.

**Strict validation**: Unknown keys or bad types cause startup failure. Fix with `openclaw doctor --fix`.

## Config Shape Reference

This skill no longer mirrors example config shapes for `agents.defaults.model`, `bindings`, `channels.discord` allowlists, `auth.order`, `secrets.providers`, `acp`, `diagnostics.otel`, etc. The official docs are the canonical source for those shapes — fetch them when you need a template:

```bash
# Local package docs (shipped with installed OpenClaw):
rg -n "agents\\.defaults\\.model|auth\\.order|plugins\\.allow" "$(npm root -g)/openclaw/docs"

# Live docs cache (if refreshed):
rg -n "<key>" "$HOME/.cache/openclaw-admin/openclaw-docs/current"
```

This install's **actual** config choices (which providers are in the failover chain, which auth order is pinned, which secrets provider type is in use, dual-allowlist scope, ACP allowlist) belong in `local-install.md` under "Notable Config Choices" — not here. That keeps generic shape reference (docs) and instance-specific values (local) cleanly separated.
