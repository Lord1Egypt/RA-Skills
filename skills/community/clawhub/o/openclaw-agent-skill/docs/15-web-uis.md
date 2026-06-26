# Web UIs

> This file contains verbatim documentation from docs.openclaw.ai
> Total pages in this section: 4

---

<!-- SOURCE: https://docs.openclaw.ai/web/control-ui -->

# Control UI - OpenClaw

## Control UI (browser)

The Control UI is a small **Vite + Lit** single-page app served by the Gateway:

*   default: `http://<host>:18789/`
*   optional prefix: set `gateway.controlUi.basePath` (e.g. `/openclaw`)

It speaks **directly to the Gateway WebSocket** on the same port.

## Quick open (local)

If the Gateway is running on the same computer, open:

*   [http://127.0.0.1:18789/](http://127.0.0.1:18789/) (or [http://localhost:18789/](http://localhost:18789/))

If the page fails to load, start the Gateway first: `openclaw gateway`. Auth is supplied during the WebSocket handshake via:

*   `connect.params.auth.token`
*   `connect.params.auth.password` The dashboard settings panel lets you store a token; passwords are not persisted. The onboarding wizard generates a gateway token by default, so paste it here on first connect.

## Device pairing (first connection)

When you connect to the Control UI from a new browser or device, the Gateway requires a **one-time pairing approval** — even if you’re on the same Tailnet with `gateway.auth.allowTailscale: true`. This is a security measure to prevent unauthorized access. **What you’ll see:** “disconnected (1008): pairing required” **To approve the device:**

```
# List pending requests
openclaw devices list

# Approve by request ID
openclaw devices approve <requestId>
```

Once approved, the device is remembered and won’t require re-approval unless you revoke it with `openclaw devices revoke --device <id> --role <role>`. See [Devices CLI](https://docs.openclaw.ai/cli/devices) for token rotation and revocation. **Notes:**

*   Local connections (`127.0.0.1`) are auto-approved.
*   Remote connections (LAN, Tailnet, etc.) require explicit approval.
*   Each browser profile generates a unique device ID, so switching browsers or clearing browser data will require re-pairing.

## Language support

The Control UI can localize itself on first load based on your browser locale, and you can override it later from the language picker in the Access card.

*   Supported locales: `en`, `zh-CN`, `zh-TW`, `pt-BR`, `de`, `es`
*   Non-English translations are lazy-loaded in the browser.
*   The selected locale is saved in browser storage and reused on future visits.
*   Missing translation keys fall back to English.

## What it can do (today)

*   Chat with the model via Gateway WS (`chat.history`, `chat.send`, `chat.abort`, `chat.inject`)
*   Stream tool calls + live tool output cards in Chat (agent events)
*   Channels: WhatsApp/Telegram/Discord/Slack + plugin channels (Mattermost, etc.) status + QR login + per-channel config (`channels.status`, `web.login.*`, `config.patch`)
*   Instances: presence list + refresh (`system-presence`)
*   Sessions: list + per-session thinking/verbose overrides (`sessions.list`, `sessions.patch`)
*   Cron jobs: list/add/edit/run/enable/disable + run history (`cron.*`)
*   Skills: status, enable/disable, install, API key updates (`skills.*`)
*   Nodes: list + caps (`node.list`)
*   Exec approvals: edit gateway or node allowlists + ask policy for `exec host=gateway/node` (`exec.approvals.*`)
*   Config: view/edit `~/.openclaw/openclaw.json` (`config.get`, `config.set`)
*   Config: apply + restart with validation (`config.apply`) and wake the last active session
*   Config writes include a base-hash guard to prevent clobbering concurrent edits
*   Config schema + form rendering (`config.schema`, including plugin + channel schemas); Raw JSON editor remains available
*   Debug: status/health/models snapshots + event log + manual RPC calls (`status`, `health`, `models.list`)
*   Logs: live tail of gateway file logs with filter/export (`logs.tail`)
*   Update: run a package/git update + restart (`update.run`) with a restart report

Cron jobs panel notes:

*   For isolated jobs, delivery defaults to announce summary. You can switch to none if you want internal-only runs.
*   Channel/target fields appear when announce is selected.
*   Webhook mode uses `delivery.mode = "webhook"` with `delivery.to` set to a valid HTTP(S) webhook URL.
*   For main-session jobs, webhook and none delivery modes are available.
*   Advanced edit controls include delete-after-run, clear agent override, cron exact/stagger options, agent model/thinking overrides, and best-effort delivery toggles.
*   Form validation is inline with field-level errors; invalid values disable the save button until fixed.
*   Set `cron.webhookToken` to send a dedicated bearer token, if omitted the webhook is sent without an auth header.
*   Deprecated fallback: stored legacy jobs with `notify: true` can still use `cron.webhook` until migrated.

## Chat behavior

*   `chat.send` is **non-blocking**: it acks immediately with `{ runId, status: "started" }` and the response streams via `chat` events.
*   Re-sending with the same `idempotencyKey` returns `{ status: "in_flight" }` while running, and `{ status: "ok" }` after completion.
*   `chat.history` responses are size-bounded for UI safety. When transcript entries are too large, Gateway may truncate long text fields, omit heavy metadata blocks, and replace oversized messages with a placeholder (`[chat.history omitted: message too large]`).
*   `chat.inject` appends an assistant note to the session transcript and broadcasts a `chat` event for UI-only updates (no agent run, no channel delivery).
*   Stop:
    *   Click **Stop** (calls `chat.abort`)
    *   Type `/stop` (or standalone abort phrases like `stop`, `stop action`, `stop run`, `stop openclaw`, `please stop`) to abort out-of-band
    *   `chat.abort` supports `{ sessionKey }` (no `runId`) to abort all active runs for that session
*   Abort partial retention:
    *   When a run is aborted, partial assistant text can still be shown in the UI
    *   Gateway persists aborted partial assistant text into transcript history when buffered output exists
    *   Persisted entries include abort metadata so transcript consumers can tell abort partials from normal completion output

## Tailnet access (recommended)

### Integrated Tailscale Serve (preferred)

Keep the Gateway on loopback and let Tailscale Serve proxy it with HTTPS:

```
openclaw gateway --tailscale serve
```

Open:

*   `https://<magicdns>/` (or your configured `gateway.controlUi.basePath`)

By default, Control UI/WebSocket Serve requests can authenticate via Tailscale identity headers (`tailscale-user-login`) when `gateway.auth.allowTailscale` is `true`. OpenClaw verifies the identity by resolving the `x-forwarded-for` address with `tailscale whois` and matching it to the header, and only accepts these when the request hits loopback with Tailscale’s `x-forwarded-*` headers. Set `gateway.auth.allowTailscale: false` (or force `gateway.auth.mode: "password"`) if you want to require a token/password even for Serve traffic. Tokenless Serve auth assumes the gateway host is trusted. If untrusted local code may run on that host, require token/password auth.

### Bind to tailnet + token

```
openclaw gateway --bind tailnet --token "$(openssl rand -hex 32)"
```

Then open:

*   `http://<tailscale-ip>:18789/` (or your configured `gateway.controlUi.basePath`)

Paste the token into the UI settings (sent as `connect.params.auth.token`).

## Insecure HTTP

If you open the dashboard over plain HTTP (`http://<lan-ip>` or `http://<tailscale-ip>`), the browser runs in a **non-secure context** and blocks WebCrypto. By default, OpenClaw **blocks** Control UI connections without device identity. **Recommended fix:** use HTTPS (Tailscale Serve) or open the UI locally:

*   `https://<magicdns>/` (Serve)
*   `http://127.0.0.1:18789/` (on the gateway host)

**Insecure-auth toggle behavior:**

```
{
  gateway: {
    controlUi: { allowInsecureAuth: true },
    bind: "tailnet",
    auth: { mode: "token", token: "replace-me" },
  },
}
```

`allowInsecureAuth` does not bypass Control UI device identity or pairing checks. **Break-glass only:**

```
{
  gateway: {
    controlUi: { dangerouslyDisableDeviceAuth: true },
    bind: "tailnet",
    auth: { mode: "token", token: "replace-me" },
  },
}
```

`dangerouslyDisableDeviceAuth` disables Control UI device identity checks and is a severe security downgrade. Revert quickly after emergency use. See [Tailscale](https://docs.openclaw.ai/gateway/tailscale) for HTTPS setup guidance.

## Building the UI

The Gateway serves static files from `dist/control-ui`. Build them with:

```
pnpm ui:build # auto-installs UI deps on first run
```

Optional absolute base (when you want fixed asset URLs):

```
OPENCLAW_CONTROL_UI_BASE_PATH=/openclaw/ pnpm ui:build
```

For local development (separate dev server):

```
pnpm ui:dev # auto-installs UI deps on first run
```

Then point the UI at your Gateway WS URL (e.g. `ws://127.0.0.1:18789`).

## Debugging/testing: dev server + remote Gateway

The Control UI is static files; the WebSocket target is configurable and can be different from the HTTP origin. This is handy when you want the Vite dev server locally but the Gateway runs elsewhere.

1.  Start the UI dev server: `pnpm ui:dev`
2.  Open a URL like:

```
http://localhost:5173/?gatewayUrl=ws://<gateway-host>:18789
```

Optional one-time auth (if needed):

```
http://localhost:5173/?gatewayUrl=wss://<gateway-host>:18789#token=<gateway-token>
```

Notes:

*   `gatewayUrl` is stored in localStorage after load and removed from the URL.
*   `token` is imported into memory for the current tab and stripped from the URL; it is not stored in localStorage.
*   `password` is kept in memory only.
*   When `gatewayUrl` is set, the UI does not fall back to config or environment credentials. Provide `token` (or `password`) explicitly. Missing explicit credentials is an error.
*   Use `wss://` when the Gateway is behind TLS (Tailscale Serve, HTTPS proxy, etc.).
*   `gatewayUrl` is only accepted in a top-level window (not embedded) to prevent clickjacking.
*   Non-loopback Control UI deployments must set `gateway.controlUi.allowedOrigins` explicitly (full origins). This includes remote dev setups.
*   `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback=true` enables Host-header origin fallback mode, but it is a dangerous security mode.

Example:

```
{
  gateway: {
    controlUi: {
      allowedOrigins: ["http://localhost:5173"],
    },
  },
}
```

Remote access setup details: [Remote access](https://docs.openclaw.ai/gateway/remote).

---

<!-- SOURCE: https://docs.openclaw.ai/web/webchat -->

# WebChat - OpenClaw

## WebChat (Gateway WebSocket UI)

Status: the macOS/iOS SwiftUI chat UI talks directly to the Gateway WebSocket.

## What it is

*   A native chat UI for the gateway (no embedded browser and no local static server).
*   Uses the same sessions and routing rules as other channels.
*   Deterministic routing: replies always go back to WebChat.

## Quick start

1.  Start the gateway.
2.  Open the WebChat UI (macOS/iOS app) or the Control UI chat tab.
3.  Ensure gateway auth is configured (required by default, even on loopback).

## How it works (behavior)

*   The UI connects to the Gateway WebSocket and uses `chat.history`, `chat.send`, and `chat.inject`.
*   `chat.history` is bounded for stability: Gateway may truncate long text fields, omit heavy metadata, and replace oversized entries with `[chat.history omitted: message too large]`.
*   `chat.inject` appends an assistant note directly to the transcript and broadcasts it to the UI (no agent run).
*   Aborted runs can keep partial assistant output visible in the UI.
*   Gateway persists aborted partial assistant text into transcript history when buffered output exists, and marks those entries with abort metadata.
*   History is always fetched from the gateway (no local file watching).
*   If the gateway is unreachable, WebChat is read-only.

*   The Control UI `/agents` Tools panel fetches a runtime catalog via `tools.catalog` and labels each tool as `core` or `plugin:<id>` (plus `optional` for optional plugin tools).
*   If `tools.catalog` is unavailable, the panel falls back to a built-in static list.
*   The panel edits profile and override config, but effective runtime access still follows policy precedence (`allow`/`deny`, per-agent and provider/channel overrides).

## Remote use

*   Remote mode tunnels the gateway WebSocket over SSH/Tailscale.
*   You do not need to run a separate WebChat server.

## Configuration reference (WebChat)

Full configuration: [Configuration](https://docs.openclaw.ai/gateway/configuration) Channel options:

*   No dedicated `webchat.*` block. WebChat uses the gateway endpoint + auth settings below.

Related global options:

*   `gateway.port`, `gateway.bind`: WebSocket host/port.
*   `gateway.auth.mode`, `gateway.auth.token`, `gateway.auth.password`: WebSocket auth (token/password).
*   `gateway.auth.mode: "trusted-proxy"`: reverse-proxy auth for browser clients (see [Trusted Proxy Auth](https://docs.openclaw.ai/gateway/trusted-proxy-auth)).
*   `gateway.remote.url`, `gateway.remote.token`, `gateway.remote.password`: remote gateway target.
*   `session.*`: session storage and main key defaults.

---

<!-- SOURCE: https://docs.openclaw.ai/web/dashboard -->

# Dashboard - OpenClaw

## Dashboard (Control UI)

The Gateway dashboard is the browser Control UI served at `/` by default (override with `gateway.controlUi.basePath`). Quick open (local Gateway):

*   [http://127.0.0.1:18789/](http://127.0.0.1:18789/) (or [http://localhost:18789/](http://localhost:18789/))

Key references:

*   [Control UI](https://docs.openclaw.ai/web/control-ui) for usage and UI capabilities.
*   [Tailscale](https://docs.openclaw.ai/gateway/tailscale) for Serve/Funnel automation.
*   [Web surfaces](https://docs.openclaw.ai/web) for bind modes and security notes.

Authentication is enforced at the WebSocket handshake via `connect.params.auth` (token or password). See `gateway.auth` in [Gateway configuration](https://docs.openclaw.ai/gateway/configuration). Security note: the Control UI is an **admin surface** (chat, config, exec approvals). Do not expose it publicly. The UI keeps dashboard URL tokens in memory for the current tab and strips them from the URL after load. Prefer localhost, Tailscale Serve, or an SSH tunnel.

## Fast path (recommended)

*   After onboarding, the CLI auto-opens the dashboard and prints a clean (non-tokenized) link.
*   Re-open anytime: `openclaw dashboard` (copies link, opens browser if possible, shows SSH hint if headless).
*   If the UI prompts for auth, paste the token from `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`) into Control UI settings.

## Token basics (local vs remote)

*   **Localhost**: open `http://127.0.0.1:18789/`.
*   **Token source**: `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`); `openclaw dashboard` can pass it via URL fragment for one-time bootstrap, but the Control UI does not persist gateway tokens in localStorage.
*   If `gateway.auth.token` is SecretRef-managed, `openclaw dashboard` prints/copies/opens a non-tokenized URL by design. This avoids exposing externally managed tokens in shell logs, clipboard history, or browser-launch arguments.
*   If `gateway.auth.token` is configured as a SecretRef and is unresolved in your current shell, `openclaw dashboard` still prints a non-tokenized URL plus actionable auth setup guidance.
*   **Not localhost**: use Tailscale Serve (tokenless for Control UI/WebSocket if `gateway.auth.allowTailscale: true`, assumes trusted gateway host; HTTP APIs still need token/password), tailnet bind with a token, or an SSH tunnel. See [Web surfaces](https://docs.openclaw.ai/web).

*   Ensure the gateway is reachable (local: `openclaw status`; remote: SSH tunnel `ssh -N -L 18789:127.0.0.1:18789 user@host` then open `http://127.0.0.1:18789/`).
*   Retrieve or supply the token from the gateway host:
    *   Plaintext config: `openclaw config get gateway.auth.token`
    *   SecretRef-managed config: resolve the external secret provider or export `OPENCLAW_GATEWAY_TOKEN` in this shell, then rerun `openclaw dashboard`
    *   No token configured: `openclaw doctor --generate-gateway-token`
*   In the dashboard settings, paste the token into the auth field, then connect.

---

<!-- SOURCE: https://docs.openclaw.ai/web/tui -->

# TUI - OpenClaw

## TUI (Terminal UI)

## Quick start

1.  Start the Gateway.

2.  Open the TUI.

3.  Type a message and press Enter.

Remote Gateway:

```
openclaw tui --url ws://<host>:<port> --token <gateway-token>
```

Use `--password` if your Gateway uses password auth.

## What you see

*   Header: connection URL, current agent, current session.
*   Chat log: user messages, assistant replies, system notices, tool cards.
*   Status line: connection/run state (connecting, running, streaming, idle, error).
*   Footer: connection state + agent + session + model + think/verbose/reasoning + token counts + deliver.
*   Input: text editor with autocomplete.

## Mental model: agents + sessions

*   Agents are unique slugs (e.g. `main`, `research`). The Gateway exposes the list.
*   Sessions belong to the current agent.
*   Session keys are stored as `agent:<agentId>:<sessionKey>`.
    *   If you type `/session main`, the TUI expands it to `agent:<currentAgent>:main`.
    *   If you type `/session agent:other:main`, you switch to that agent session explicitly.
*   Session scope:
    *   `per-sender` (default): each agent has many sessions.
    *   `global`: the TUI always uses the `global` session (the picker may be empty).
*   The current agent + session are always visible in the footer.

## Sending + delivery

*   Messages are sent to the Gateway; delivery to providers is off by default.
*   Turn delivery on:
    *   `/deliver on`
    *   or the Settings panel
    *   or start with `openclaw tui --deliver`

## Pickers + overlays

*   Model picker: list available models and set the session override.
*   Agent picker: choose a different agent.
*   Session picker: shows only sessions for the current agent.
*   Settings: toggle deliver, tool output expansion, and thinking visibility.

## Keyboard shortcuts

*   Enter: send message
*   Esc: abort active run
*   Ctrl+C: clear input (press twice to exit)
*   Ctrl+D: exit
*   Ctrl+L: model picker
*   Ctrl+G: agent picker
*   Ctrl+P: session picker
*   Ctrl+O: toggle tool output expansion
*   Ctrl+T: toggle thinking visibility (reloads history)

## Slash commands

Core:

*   `/help`
*   `/status`
*   `/agent <id>` (or `/agents`)
*   `/session <key>` (or `/sessions`)
*   `/model <provider/model>` (or `/models`)

Session controls:

*   `/think <off|minimal|low|medium|high>`
*   `/verbose <on|full|off>`
*   `/reasoning <on|off|stream>`
*   `/usage <off|tokens|full>`
*   `/elevated <on|off|ask|full>` (alias: `/elev`)
*   `/activation <mention|always>`
*   `/deliver <on|off>`

Session lifecycle:

*   `/new` or `/reset` (reset the session)
*   `/abort` (abort the active run)
*   `/settings`
*   `/exit`

Other Gateway slash commands (for example, `/context`) are forwarded to the Gateway and shown as system output. See [Slash commands](https://docs.openclaw.ai/tools/slash-commands).

## Local shell commands

*   Prefix a line with `!` to run a local shell command on the TUI host.
*   The TUI prompts once per session to allow local execution; declining keeps `!` disabled for the session.
*   Commands run in a fresh, non-interactive shell in the TUI working directory (no persistent `cd`/env).
*   Local shell commands receive `OPENCLAW_SHELL=tui-local` in their environment.
*   A lone `!` is sent as a normal message; leading spaces do not trigger local exec.

*   Tool calls show as cards with args + results.
*   Ctrl+O toggles between collapsed/expanded views.
*   While tools run, partial updates stream into the same card.

## Terminal colors

*   The TUI keeps assistant body text in your terminal’s default foreground so dark and light terminals both stay readable.
*   If your terminal uses a light background and auto-detection is wrong, set `OPENCLAW_THEME=light` before launching `openclaw tui`.
*   To force the original dark palette instead, set `OPENCLAW_THEME=dark`.

## History + streaming

*   On connect, the TUI loads the latest history (default 200 messages).
*   Streaming responses update in place until finalized.
*   The TUI also listens to agent tool events for richer tool cards.

## Connection details

*   The TUI registers with the Gateway as `mode: "tui"`.
*   Reconnects show a system message; event gaps are surfaced in the log.

## Options

*   `--url <url>`: Gateway WebSocket URL (defaults to config or `ws://127.0.0.1:<port>`)
*   `--token <token>`: Gateway token (if required)
*   `--password <password>`: Gateway password (if required)
*   `--session <key>`: Session key (default: `main`, or `global` when scope is global)
*   `--deliver`: Deliver assistant replies to the provider (default off)
*   `--thinking <level>`: Override thinking level for sends
*   `--timeout-ms <ms>`: Agent timeout in ms (defaults to `agents.defaults.timeoutSeconds`)

Note: when you set `--url`, the TUI does not fall back to config or environment credentials. Pass `--token` or `--password` explicitly. Missing explicit credentials is an error.

## Troubleshooting

No output after sending a message:

*   Run `/status` in the TUI to confirm the Gateway is connected and idle/busy.
*   Check the Gateway logs: `openclaw logs --follow`.
*   Confirm the agent can run: `openclaw status` and `openclaw models status`.
*   If you expect messages in a chat channel, enable delivery (`/deliver on` or `--deliver`).
*   `--history-limit <n>`: History entries to load (default 200)

## Connection troubleshooting

*   `disconnected`: ensure the Gateway is running and your `--url/--token/--password` are correct.
*   No agents in picker: check `openclaw agents list` and your routing config.
*   Empty session picker: you might be in global scope or have no sessions yet.

