# Platforms - macOS

> This file contains verbatim documentation from docs.openclaw.ai
> Total pages in this section: 20

---

<!-- SOURCE: https://docs.openclaw.ai/platforms -->

# Platforms - OpenClaw

OpenClaw core is written in TypeScript. **Node is the recommended runtime**. Bun is not recommended for the Gateway (WhatsApp/Telegram bugs). Companion apps exist for macOS (menu bar app) and mobile nodes (iOS/Android). Windows and Linux companion apps are planned, but the Gateway is fully supported today. Native companion apps for Windows are also planned; the Gateway is recommended via WSL2.

## Choose your OS

*   macOS: [macOS](https://docs.openclaw.ai/platforms/macos)
*   iOS: [iOS](https://docs.openclaw.ai/platforms/ios)
*   Android: [Android](https://docs.openclaw.ai/platforms/android)
*   Windows: [Windows](https://docs.openclaw.ai/platforms/windows)
*   Linux: [Linux](https://docs.openclaw.ai/platforms/linux)

## VPS & hosting

*   VPS hub: [VPS hosting](https://docs.openclaw.ai/vps)
*   Fly.io: [Fly.io](https://docs.openclaw.ai/install/fly)
*   Hetzner (Docker): [Hetzner](https://docs.openclaw.ai/install/hetzner)
*   GCP (Compute Engine): [GCP](https://docs.openclaw.ai/install/gcp)
*   exe.dev (VM + HTTPS proxy): [exe.dev](https://docs.openclaw.ai/install/exe-dev)

## Common links

*   Install guide: [Getting Started](https://docs.openclaw.ai/start/getting-started)
*   Gateway runbook: [Gateway](https://docs.openclaw.ai/gateway)
*   Gateway configuration: [Configuration](https://docs.openclaw.ai/gateway/configuration)
*   Service status: `openclaw gateway status`

## Gateway service install (CLI)

Use one of these (all supported):

*   Wizard (recommended): `openclaw onboard --install-daemon`
*   Direct: `openclaw gateway install`
*   Configure flow: `openclaw configure` → select **Gateway service**
*   Repair/migrate: `openclaw doctor` (offers to install or fix the service)

The service target depends on OS:

*   macOS: LaunchAgent (`ai.openclaw.gateway` or `ai.openclaw.<profile>`; legacy `com.openclaw.*`)
*   Linux/WSL2: systemd user service (`openclaw-gateway[-<profile>].service`)

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/macos -->

# macOS App - OpenClaw

The macOS app is the **menu‑bar companion** for OpenClaw. It owns permissions, manages/attaches to the Gateway locally (launchd or manual), and exposes macOS capabilities to the agent as a node.

## What it does

*   Shows native notifications and status in the menu bar.
*   Owns TCC prompts (Notifications, Accessibility, Screen Recording, Microphone, Speech Recognition, Automation/AppleScript).
*   Runs or connects to the Gateway (local or remote).
*   Exposes macOS‑only tools (Canvas, Camera, Screen Recording, `system.run`).
*   Starts the local node host service in **remote** mode (launchd), and stops it in **local** mode.
*   Optionally hosts **PeekabooBridge** for UI automation.
*   Installs the global CLI (`openclaw`) via npm/pnpm on request (bun not recommended for the Gateway runtime).

## Local vs remote mode

*   **Local** (default): the app attaches to a running local Gateway if present; otherwise it enables the launchd service via `openclaw gateway install`.
*   **Remote**: the app connects to a Gateway over SSH/Tailscale and never starts a local process. The app starts the local **node host service** so the remote Gateway can reach this Mac. The app does not spawn the Gateway as a child process.

## Launchd control

The app manages a per‑user LaunchAgent labeled `ai.openclaw.gateway` (or `ai.openclaw.<profile>` when using `--profile`/`OPENCLAW_PROFILE`; legacy `com.openclaw.*` still unloads).

```
launchctl kickstart -k gui/$UID/ai.openclaw.gateway
launchctl bootout gui/$UID/ai.openclaw.gateway
```

Replace the label with `ai.openclaw.<profile>` when running a named profile. If the LaunchAgent isn’t installed, enable it from the app or run `openclaw gateway install`.

## Node capabilities (mac)

The macOS app presents itself as a node. Common commands:

*   Canvas: `canvas.present`, `canvas.navigate`, `canvas.eval`, `canvas.snapshot`, `canvas.a2ui.*`
*   Camera: `camera.snap`, `camera.clip`
*   Screen: `screen.record`
*   System: `system.run`, `system.notify`

The node reports a `permissions` map so agents can decide what’s allowed. Node service + app IPC:

*   When the headless node host service is running (remote mode), it connects to the Gateway WS as a node.
*   `system.run` executes in the macOS app (UI/TCC context) over a local Unix socket; prompts + output stay in-app.

Diagram (SCI):

```
Gateway -> Node Service (WS)
                 |  IPC (UDS + token + HMAC + TTL)
                 v
             Mac App (UI + TCC + system.run)
```

## Exec approvals (system.run)

`system.run` is controlled by **Exec approvals** in the macOS app (Settings → Exec approvals). Security + ask + allowlist are stored locally on the Mac in:

```
~/.openclaw/exec-approvals.json
```

Example:

```
{
  "version": 1,
  "defaults": {
    "security": "deny",
    "ask": "on-miss"
  },
  "agents": {
    "main": {
      "security": "allowlist",
      "ask": "on-miss",
      "allowlist": [{ "pattern": "/opt/homebrew/bin/rg" }]
    }
  }
}
```

Notes:

*   `allowlist` entries are glob patterns for resolved binary paths.
*   Raw shell command text that contains shell control or expansion syntax (`&&`, `||`, `;`, `|`, `` ` ``, `$`, `<`, `>`, `(`, `)`) is treated as an allowlist miss and requires explicit approval (or allowlisting the shell binary).
*   Choosing “Always Allow” in the prompt adds that command to the allowlist.
*   `system.run` environment overrides are filtered (drops `PATH`, `DYLD_*`, `LD_*`, `NODE_OPTIONS`, `PYTHON*`, `PERL*`, `RUBYOPT`, `SHELLOPTS`, `PS4`) and then merged with the app’s environment.
*   For shell wrappers (`bash|sh|zsh ... -c/-lc`), request-scoped environment overrides are reduced to a small explicit allowlist (`TERM`, `LANG`, `LC_*`, `COLORTERM`, `NO_COLOR`, `FORCE_COLOR`).
*   For allow-always decisions in allowlist mode, known dispatch wrappers (`env`, `nice`, `nohup`, `stdbuf`, `timeout`) persist inner executable paths instead of wrapper paths. If unwrapping is not safe, no allowlist entry is persisted automatically.

## Deep links

The app registers the `openclaw://` URL scheme for local actions.

### `openclaw://agent`

Triggers a Gateway `agent` request.

```
open 'openclaw://agent?message=Hello%20from%20deep%20link'
```

Query parameters:

*   `message` (required)
*   `sessionKey` (optional)
*   `thinking` (optional)
*   `deliver` / `to` / `channel` (optional)
*   `timeoutSeconds` (optional)
*   `key` (optional unattended mode key)

Safety:

*   Without `key`, the app prompts for confirmation.
*   Without `key`, the app enforces a short message limit for the confirmation prompt and ignores `deliver` / `to` / `channel`.
*   With a valid `key`, the run is unattended (intended for personal automations).

## Onboarding flow (typical)

1.  Install and launch **OpenClaw.app**.
2.  Complete the permissions checklist (TCC prompts).
3.  Ensure **Local** mode is active and the Gateway is running.
4.  Install the CLI if you want terminal access.

## State dir placement (macOS)

Avoid putting your OpenClaw state dir in iCloud or other cloud-synced folders. Sync-backed paths can add latency and occasionally cause file-lock/sync races for sessions and credentials. Prefer a local non-synced state path such as:

```
OPENCLAW_STATE_DIR=~/.openclaw
```

If `openclaw doctor` detects state under:

*   `~/Library/Mobile Documents/com~apple~CloudDocs/...`
*   `~/Library/CloudStorage/...`

it will warn and recommend moving back to a local path.

## Build & dev workflow (native)

*   `cd apps/macos && swift build`
*   `swift run OpenClaw` (or Xcode)
*   Package app: `scripts/package-mac-app.sh`

## Debug gateway connectivity (macOS CLI)

Use the debug CLI to exercise the same Gateway WebSocket handshake and discovery logic that the macOS app uses, without launching the app.

```
cd apps/macos
swift run openclaw-mac connect --json
swift run openclaw-mac discover --timeout 3000 --json
```

Connect options:

*   `--url <ws://host:port>`: override config
*   `--mode <local|remote>`: resolve from config (default: config or local)
*   `--probe`: force a fresh health probe
*   `--timeout <ms>`: request timeout (default: `15000`)
*   `--json`: structured output for diffing

Discovery options:

*   `--include-local`: include gateways that would be filtered as “local”
*   `--timeout <ms>`: overall discovery window (default: `2000`)
*   `--json`: structured output for diffing

Tip: compare against `openclaw gateway discover --json` to see whether the macOS app’s discovery pipeline (NWBrowser + tailnet DNS‑SD fallback) differs from the Node CLI’s `dns-sd` based discovery.

## Remote connection plumbing (SSH tunnels)

When the macOS app runs in **Remote** mode, it opens an SSH tunnel so local UI components can talk to a remote Gateway as if it were on localhost.

### Control tunnel (Gateway WebSocket port)

*   **Purpose:** health checks, status, Web Chat, config, and other control-plane calls.
*   **Local port:** the Gateway port (default `18789`), always stable.
*   **Remote port:** the same Gateway port on the remote host.
*   **Behavior:** no random local port; the app reuses an existing healthy tunnel or restarts it if needed.
*   **SSH shape:** `ssh -N -L <local>:127.0.0.1:<remote>` with BatchMode + ExitOnForwardFailure + keepalive options.
*   **IP reporting:** the SSH tunnel uses loopback, so the gateway will see the node IP as `127.0.0.1`. Use **Direct (ws/wss)** transport if you want the real client IP to appear (see [macOS remote access](https://docs.openclaw.ai/platforms/mac/remote)).

For setup steps, see [macOS remote access](https://docs.openclaw.ai/platforms/mac/remote). For protocol details, see [Gateway protocol](https://docs.openclaw.ai/gateway/protocol).

*   [Gateway runbook](https://docs.openclaw.ai/gateway)
*   [Gateway (macOS)](https://docs.openclaw.ai/platforms/mac/bundled-gateway)
*   [macOS permissions](https://docs.openclaw.ai/platforms/mac/permissions)
*   [Canvas](https://docs.openclaw.ai/platforms/mac/canvas)

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/mac/remote -->

# Remote Control - OpenClaw

## Remote OpenClaw (macOS ⇄ remote host)

This flow lets the macOS app act as a full remote control for a OpenClaw gateway running on another host (desktop/server). It’s the app’s **Remote over SSH** (remote run) feature. All features—health checks, Voice Wake forwarding, and Web Chat—reuse the same remote SSH configuration from _Settings → General_.

## Modes

*   **Local (this Mac)**: Everything runs on the laptop. No SSH involved.
*   **Remote over SSH (default)**: OpenClaw commands are executed on the remote host. The mac app opens an SSH connection with `-o BatchMode` plus your chosen identity/key and a local port-forward.
*   **Remote direct (ws/wss)**: No SSH tunnel. The mac app connects to the gateway URL directly (for example, via Tailscale Serve or a public HTTPS reverse proxy).

## Remote transports

Remote mode supports two transports:

*   **SSH tunnel** (default): Uses `ssh -N -L ...` to forward the gateway port to localhost. The gateway will see the node’s IP as `127.0.0.1` because the tunnel is loopback.
*   **Direct (ws/wss)**: Connects straight to the gateway URL. The gateway sees the real client IP.

## Prereqs on the remote host

1.  Install Node + pnpm and build/install the OpenClaw CLI (`pnpm install && pnpm build && pnpm link --global`).
2.  Ensure `openclaw` is on PATH for non-interactive shells (symlink into `/usr/local/bin` or `/opt/homebrew/bin` if needed).
3.  Open SSH with key auth. We recommend **Tailscale** IPs for stable reachability off-LAN.

## macOS app setup

1.  Open _Settings → General_.
2.  Under **OpenClaw runs**, pick **Remote over SSH** and set:
    *   **Transport**: **SSH tunnel** or **Direct (ws/wss)**.
    *   **SSH target**: `user@host` (optional `:port`).
        *   If the gateway is on the same LAN and advertises Bonjour, pick it from the discovered list to auto-fill this field.
    *   **Gateway URL** (Direct only): `wss://gateway.example.ts.net` (or `ws://...` for local/LAN).
    *   **Identity file** (advanced): path to your key.
    *   **Project root** (advanced): remote checkout path used for commands.
    *   **CLI path** (advanced): optional path to a runnable `openclaw` entrypoint/binary (auto-filled when advertised).
3.  Hit **Test remote**. Success indicates the remote `openclaw status --json` runs correctly. Failures usually mean PATH/CLI issues; exit 127 means the CLI isn’t found remotely.
4.  Health checks and Web Chat will now run through this SSH tunnel automatically.

## Web Chat

*   **SSH tunnel**: Web Chat connects to the gateway over the forwarded WebSocket control port (default 18789).
*   **Direct (ws/wss)**: Web Chat connects straight to the configured gateway URL.
*   There is no separate WebChat HTTP server anymore.

## Permissions

*   The remote host needs the same TCC approvals as local (Automation, Accessibility, Screen Recording, Microphone, Speech Recognition, Notifications). Run onboarding on that machine to grant them once.
*   Nodes advertise their permission state via `node.list` / `node.describe` so agents know what’s available.

## Security notes

*   Prefer loopback binds on the remote host and connect via SSH or Tailscale.
*   SSH tunneling uses strict host-key checking; trust the host key first so it exists in `~/.ssh/known_hosts`.
*   If you bind the Gateway to a non-loopback interface, require token/password auth.
*   See [Security](https://docs.openclaw.ai/gateway/security) and [Tailscale](https://docs.openclaw.ai/gateway/tailscale).

## WhatsApp login flow (remote)

*   Run `openclaw channels login --verbose` **on the remote host**. Scan the QR with WhatsApp on your phone.
*   Re-run login on that host if auth expires. Health check will surface link problems.

## Troubleshooting

*   **exit 127 / not found**: `openclaw` isn’t on PATH for non-login shells. Add it to `/etc/paths`, your shell rc, or symlink into `/usr/local/bin`/`/opt/homebrew/bin`.
*   **Health probe failed**: check SSH reachability, PATH, and that Baileys is logged in (`openclaw status --json`).
*   **Web Chat stuck**: confirm the gateway is running on the remote host and the forwarded port matches the gateway WS port; the UI requires a healthy WS connection.
*   **Node IP shows 127.0.0.1**: expected with the SSH tunnel. Switch **Transport** to **Direct (ws/wss)** if you want the gateway to see the real client IP.
*   **Voice Wake**: trigger phrases are forwarded automatically in remote mode; no separate forwarder is needed.

## Notification sounds

Pick sounds per notification from scripts with `openclaw` and `node.invoke`, e.g.:

```
openclaw nodes notify --node <id> --title "Ping" --body "Remote gateway ready" --sound Glass
```

There is no global “default sound” toggle in the app anymore; callers choose a sound (or none) per request.

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/mac/bundled-gateway -->

# Gateway on macOS - OpenClaw

## Gateway on macOS (external launchd)

OpenClaw.app no longer bundles Node/Bun or the Gateway runtime. The macOS app expects an **external** `openclaw` CLI install, does not spawn the Gateway as a child process, and manages a per‑user launchd service to keep the Gateway running (or attaches to an existing local Gateway if one is already running).

## Install the CLI (required for local mode)

You need Node 22+ on the Mac, then install `openclaw` globally:

```
npm install -g openclaw@<version>
```

The macOS app’s **Install CLI** button runs the same flow via npm/pnpm (bun not recommended for Gateway runtime).

## Launchd (Gateway as LaunchAgent)

Label:

*   `ai.openclaw.gateway` (or `ai.openclaw.<profile>`; legacy `com.openclaw.*` may remain)

Plist location (per‑user):

*   `~/Library/LaunchAgents/ai.openclaw.gateway.plist` (or `~/Library/LaunchAgents/ai.openclaw.<profile>.plist`)

Manager:

*   The macOS app owns LaunchAgent install/update in Local mode.
*   The CLI can also install it: `openclaw gateway install`.

Behavior:

*   “OpenClaw Active” enables/disables the LaunchAgent.
*   App quit does **not** stop the gateway (launchd keeps it alive).
*   If a Gateway is already running on the configured port, the app attaches to it instead of starting a new one.

Logging:

*   launchd stdout/err: `/tmp/openclaw/openclaw-gateway.log`

## Version compatibility

The macOS app checks the gateway version against its own version. If they’re incompatible, update the global CLI to match the app version.

## Smoke check

```
openclaw --version

OPENCLAW_SKIP_CHANNELS=1 \
OPENCLAW_SKIP_CANVAS_HOST=1 \
openclaw gateway --port 18999 --bind loopback
```

Then:

```
openclaw gateway call health --url ws://127.0.0.1:18999 --timeout 3000
```

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/mac/skills -->

# Skills - OpenClaw

## Skills (macOS)

The macOS app surfaces OpenClaw skills via the gateway; it does not parse skills locally.

## Data source

*   `skills.status` (gateway) returns all skills plus eligibility and missing requirements (including allowlist blocks for bundled skills).
*   Requirements are derived from `metadata.openclaw.requires` in each `SKILL.md`.

## Install actions

*   `metadata.openclaw.install` defines install options (brew/node/go/uv).
*   The app calls `skills.install` to run installers on the gateway host.
*   The gateway surfaces only one preferred installer when multiple are provided (brew when available, otherwise node manager from `skills.install`, default npm).

## Env/API keys

*   The app stores keys in `~/.openclaw/openclaw.json` under `skills.entries.<skillKey>`.
*   `skills.update` patches `enabled`, `apiKey`, and `env`.

## Remote mode

*   Install + config updates happen on the gateway host (not the local Mac).

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/mac/peekaboo -->

# Peekaboo Bridge - OpenClaw

## Peekaboo Bridge (macOS UI automation)

OpenClaw can host **PeekabooBridge** as a local, permission‑aware UI automation broker. This lets the `peekaboo` CLI drive UI automation while reusing the macOS app’s TCC permissions.

## What this is (and isn’t)

*   **Host**: OpenClaw.app can act as a PeekabooBridge host.
*   **Client**: use the `peekaboo` CLI (no separate `openclaw ui ...` surface).
*   **UI**: visual overlays stay in Peekaboo.app; OpenClaw is a thin broker host.

## Enable the bridge

In the macOS app:

*   Settings → **Enable Peekaboo Bridge**

When enabled, OpenClaw starts a local UNIX socket server. If disabled, the host is stopped and `peekaboo` will fall back to other available hosts.

## Client discovery order

Peekaboo clients typically try hosts in this order:

1.  Peekaboo.app (full UX)
2.  Claude.app (if installed)
3.  OpenClaw.app (thin broker)

Use `peekaboo bridge status --verbose` to see which host is active and which socket path is in use. You can override with:

```
export PEEKABOO_BRIDGE_SOCKET=/path/to/bridge.sock
```

## Security & permissions

*   The bridge validates **caller code signatures**; an allowlist of TeamIDs is enforced (Peekaboo host TeamID + OpenClaw app TeamID).
*   Requests time out after ~10 seconds.
*   If required permissions are missing, the bridge returns a clear error message rather than launching System Settings.

## Snapshot behavior (automation)

Snapshots are stored in memory and expire automatically after a short window. If you need longer retention, re‑capture from the client.

## Troubleshooting

*   If `peekaboo` reports “bridge client is not authorized”, ensure the client is properly signed or run the host with `PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1` in **debug** mode only.
*   If no hosts are found, open one of the host apps (Peekaboo.app or OpenClaw.app) and confirm permissions are granted.

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/mac/dev-setup -->

# macOS Dev Setup - OpenClaw

## macOS Developer Setup

This guide covers the necessary steps to build and run the OpenClaw macOS application from source.

## Prerequisites

Before building the app, ensure you have the following installed:

1.  **Xcode 26.2+**: Required for Swift development.
2.  **Node.js 22+ & pnpm**: Required for the gateway, CLI, and packaging scripts.

## 1\. Install Dependencies

Install the project-wide dependencies:

## 2\. Build and Package the App

To build the macOS app and package it into `dist/OpenClaw.app`, run:

```
./scripts/package-mac-app.sh
```

If you don’t have an Apple Developer ID certificate, the script will automatically use **ad-hoc signing** (`-`). For dev run modes, signing flags, and Team ID troubleshooting, see the macOS app README: [https://github.com/openclaw/openclaw/blob/main/apps/macos/README.md](https://github.com/openclaw/openclaw/blob/main/apps/macos/README.md)

> **Note**: Ad-hoc signed apps may trigger security prompts. If the app crashes immediately with “Abort trap 6”, see the [Troubleshooting](https://docs.openclaw.ai/platforms/mac/dev-setup#troubleshooting) section.

## 3\. Install the CLI

The macOS app expects a global `openclaw` CLI install to manage background tasks. **To install it (recommended):**

1.  Open the OpenClaw app.
2.  Go to the **General** settings tab.
3.  Click **“Install CLI”**.

Alternatively, install it manually:

```
npm install -g openclaw@<version>
```

## Troubleshooting

### Build Fails: Toolchain or SDK Mismatch

The macOS app build expects the latest macOS SDK and Swift 6.2 toolchain. **System dependencies (required):**

*   **Latest macOS version available in Software Update** (required by Xcode 26.2 SDKs)
*   **Xcode 26.2** (Swift 6.2 toolchain)

**Checks:**

```
xcodebuild -version
xcrun swift --version
```

If versions don’t match, update macOS/Xcode and re-run the build.

### App Crashes on Permission Grant

If the app crashes when you try to allow **Speech Recognition** or **Microphone** access, it may be due to a corrupted TCC cache or signature mismatch. **Fix:**

1.  Reset the TCC permissions:
    
    ```
    tccutil reset All ai.openclaw.mac.debug
    ```
    
2.  If that fails, change the `BUNDLE_ID` temporarily in [`scripts/package-mac-app.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/package-mac-app.sh) to force a “clean slate” from macOS.

### Gateway “Starting…” indefinitely

If the gateway status stays on “Starting…”, check if a zombie process is holding the port:

```
openclaw gateway status
openclaw gateway stop

# If you’re not using a LaunchAgent (dev mode / manual runs), find the listener:
lsof -nP -iTCP:18789 -sTCP:LISTEN
```

If a manual run is holding the port, stop that process (Ctrl+C). As a last resort, kill the PID you found above.

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/mac/menu-bar -->

# Menu Bar - OpenClaw

## Menu Bar Status Logic

## What is shown

*   We surface the current agent work state in the menu bar icon and in the first status row of the menu.
*   Health status is hidden while work is active; it returns when all sessions are idle.
*   The “Nodes” block in the menu lists **devices** only (paired nodes via `node.list`), not client/presence entries.
*   A “Usage” section appears under Context when provider usage snapshots are available.

## State model

*   Sessions: events arrive with `runId` (per-run) plus `sessionKey` in the payload. The “main” session is the key `main`; if absent, we fall back to the most recently updated session.
*   Priority: main always wins. If main is active, its state is shown immediately. If main is idle, the most recently active non‑main session is shown. We do not flip‑flop mid‑activity; we only switch when the current session goes idle or main becomes active.
*   Activity kinds:
    *   `job`: high‑level command execution (`state: started|streaming|done|error`).
    *   `tool`: `phase: start|result` with `toolName` and `meta/args`.

## IconState enum (Swift)

*   `idle`
*   `workingMain(ActivityKind)`
*   `workingOther(ActivityKind)`
*   `overridden(ActivityKind)` (debug override)

### ActivityKind → glyph

*   `exec` → 💻
*   `read` → 📄
*   `write` → ✍️
*   `edit` → 📝
*   `attach` → 📎
*   default → 🛠️

### Visual mapping

*   `idle`: normal critter.
*   `workingMain`: badge with glyph, full tint, leg “working” animation.
*   `workingOther`: badge with glyph, muted tint, no scurry.
*   `overridden`: uses the chosen glyph/tint regardless of activity.

## Status row text (menu)

*   While work is active: `<Session role> · <activity label>`
    *   Examples: `Main · exec: pnpm test`, `Other · read: apps/macos/Sources/OpenClaw/AppState.swift`.
*   When idle: falls back to the health summary.

## Event ingestion

*   Source: control‑channel `agent` events (`ControlChannel.handleAgentEvent`).
*   Parsed fields:
    *   `stream: "job"` with `data.state` for start/stop.
    *   `stream: "tool"` with `data.phase`, `name`, optional `meta`/`args`.
*   Labels:
    *   `exec`: first line of `args.command`.
    *   `read`/`write`: shortened path.
    *   `edit`: path plus inferred change kind from `meta`/diff counts.
    *   fallback: tool name.

## Debug override

*   Settings ▸ Debug ▸ “Icon override” picker:
    *   `System (auto)` (default)
    *   `Working: main` (per tool kind)
    *   `Working: other` (per tool kind)
    *   `Idle`
*   Stored via `@AppStorage("iconOverride")`; mapped to `IconState.overridden`.

## Testing checklist

*   Trigger main session job: verify icon switches immediately and status row shows main label.
*   Trigger non‑main session job while main idle: icon/status shows non‑main; stays stable until it finishes.
*   Start main while other active: icon flips to main instantly.
*   Rapid tool bursts: ensure badge does not flicker (TTL grace on tool results).
*   Health row reappears once all sessions idle.

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/mac/voice-overlay -->

# Voice Overlay - OpenClaw

## Voice Overlay Lifecycle (macOS)

Audience: macOS app contributors. Goal: keep the voice overlay predictable when wake-word and push-to-talk overlap.

## Current intent

*   If the overlay is already visible from wake-word and the user presses the hotkey, the hotkey session _adopts_ the existing text instead of resetting it. The overlay stays up while the hotkey is held. When the user releases: send if there is trimmed text, otherwise dismiss.
*   Wake-word alone still auto-sends on silence; push-to-talk sends immediately on release.

## Implemented (Dec 9, 2025)

*   Overlay sessions now carry a token per capture (wake-word or push-to-talk). Partial/final/send/dismiss/level updates are dropped when the token doesn’t match, avoiding stale callbacks.
*   Push-to-talk adopts any visible overlay text as a prefix (so pressing the hotkey while the wake overlay is up keeps the text and appends new speech). It waits up to 1.5s for a final transcript before falling back to the current text.
*   Chime/overlay logging is emitted at `info` in categories `voicewake.overlay`, `voicewake.ptt`, and `voicewake.chime` (session start, partial, final, send, dismiss, chime reason).

## Next steps

1.  **VoiceSessionCoordinator (actor)**
    *   Owns exactly one `VoiceSession` at a time.
    *   API (token-based): `beginWakeCapture`, `beginPushToTalk`, `updatePartial`, `endCapture`, `cancel`, `applyCooldown`.
    *   Drops callbacks that carry stale tokens (prevents old recognizers from reopening the overlay).
2.  **VoiceSession (model)**
    *   Fields: `token`, `source` (wakeWord|pushToTalk), committed/volatile text, chime flags, timers (auto-send, idle), `overlayMode` (display|editing|sending), cooldown deadline.
3.  **Overlay binding**
    *   `VoiceSessionPublisher` (`ObservableObject`) mirrors the active session into SwiftUI.
    *   `VoiceWakeOverlayView` renders only via the publisher; it never mutates global singletons directly.
    *   Overlay user actions (`sendNow`, `dismiss`, `edit`) call back into the coordinator with the session token.
4.  **Unified send path**
    *   On `endCapture`: if trimmed text is empty → dismiss; else `performSend(session:)` (plays send chime once, forwards, dismisses).
    *   Push-to-talk: no delay; wake-word: optional delay for auto-send.
    *   Apply a short cooldown to the wake runtime after push-to-talk finishes so wake-word doesn’t immediately retrigger.
5.  **Logging**
    *   Coordinator emits `.info` logs in subsystem `ai.openclaw`, categories `voicewake.overlay` and `voicewake.chime`.
    *   Key events: `session_started`, `adopted_by_push_to_talk`, `partial`, `finalized`, `send`, `dismiss`, `cancel`, `cooldown`.

## Debugging checklist

*   Stream logs while reproducing a sticky overlay:
    
    ```
    sudo log stream --predicate 'subsystem == "ai.openclaw" AND category CONTAINS "voicewake"' --level info --style compact
    ```
    
*   Verify only one active session token; stale callbacks should be dropped by the coordinator.
*   Ensure push-to-talk release always calls `endCapture` with the active token; if text is empty, expect `dismiss` without chime or send.

## Migration steps (suggested)

1.  Add `VoiceSessionCoordinator`, `VoiceSession`, and `VoiceSessionPublisher`.
2.  Refactor `VoiceWakeRuntime` to create/update/end sessions instead of touching `VoiceWakeOverlayController` directly.
3.  Refactor `VoicePushToTalk` to adopt existing sessions and call `endCapture` on release; apply runtime cooldown.
4.  Wire `VoiceWakeOverlayController` to the publisher; remove direct calls from runtime/PTT.
5.  Add integration tests for session adoption, cooldown, and empty-text dismissal.

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/mac/webchat -->

# WebChat - OpenClaw

## WebChat (macOS app)

The macOS menu bar app embeds the WebChat UI as a native SwiftUI view. It connects to the Gateway and defaults to the **main session** for the selected agent (with a session switcher for other sessions).

*   **Local mode**: connects directly to the local Gateway WebSocket.
*   **Remote mode**: forwards the Gateway control port over SSH and uses that tunnel as the data plane.

## Launch & debugging

*   Manual: Lobster menu → “Open Chat”.
*   Auto‑open for testing:
    
    ```
    dist/OpenClaw.app/Contents/MacOS/OpenClaw --webchat
    ```
    
*   Logs: `./scripts/clawlog.sh` (subsystem `ai.openclaw`, category `WebChatSwiftUI`).

## How it’s wired

*   Data plane: Gateway WS methods `chat.history`, `chat.send`, `chat.abort`, `chat.inject` and events `chat`, `agent`, `presence`, `tick`, `health`.
*   Session: defaults to the primary session (`main`, or `global` when scope is global). The UI can switch between sessions.
*   Onboarding uses a dedicated session to keep first‑run setup separate.

## Security surface

*   Remote mode forwards only the Gateway WebSocket control port over SSH.

## Known limitations

*   The UI is optimized for chat sessions (not a full browser sandbox).

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/mac/child-process -->

# Gateway Lifecycle - OpenClaw

## Gateway lifecycle on macOS

The macOS app **manages the Gateway via launchd** by default and does not spawn the Gateway as a child process. It first tries to attach to an already‑running Gateway on the configured port; if none is reachable, it enables the launchd service via the external `openclaw` CLI (no embedded runtime). This gives you reliable auto‑start at login and restart on crashes. Child‑process mode (Gateway spawned directly by the app) is **not in use** today. If you need tighter coupling to the UI, run the Gateway manually in a terminal.

## Default behavior (launchd)

*   The app installs a per‑user LaunchAgent labeled `ai.openclaw.gateway` (or `ai.openclaw.<profile>` when using `--profile`/`OPENCLAW_PROFILE`; legacy `com.openclaw.*` is supported).
*   When Local mode is enabled, the app ensures the LaunchAgent is loaded and starts the Gateway if needed.
*   Logs are written to the launchd gateway log path (visible in Debug Settings).

Common commands:

```
launchctl kickstart -k gui/$UID/ai.openclaw.gateway
launchctl bootout gui/$UID/ai.openclaw.gateway
```

Replace the label with `ai.openclaw.<profile>` when running a named profile.

## Unsigned dev builds

`scripts/restart-mac.sh --no-sign` is for fast local builds when you don’t have signing keys. To prevent launchd from pointing at an unsigned relay binary, it:

*   Writes `~/.openclaw/disable-launchagent`.

Signed runs of `scripts/restart-mac.sh` clear this override if the marker is present. To reset manually:

```
rm ~/.openclaw/disable-launchagent
```

## Attach-only mode

To force the macOS app to **never install or manage launchd**, launch it with `--attach-only` (or `--no-launchd`). This sets `~/.openclaw/disable-launchagent`, so the app only attaches to an already running Gateway. You can toggle the same behavior in Debug Settings.

## Remote mode

Remote mode never starts a local Gateway. The app uses an SSH tunnel to the remote host and connects over that tunnel.

## Why we prefer launchd

*   Auto‑start at login.
*   Built‑in restart/KeepAlive semantics.
*   Predictable logs and supervision.

If a true child‑process mode is ever needed again, it should be documented as a separate, explicit dev‑only mode.

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/mac/xpc -->

# macOS IPC - OpenClaw

## OpenClaw macOS IPC architecture

**Current model:** a local Unix socket connects the **node host service** to the **macOS app** for exec approvals + `system.run`. A `openclaw-mac` debug CLI exists for discovery/connect checks; agent actions still flow through the Gateway WebSocket and `node.invoke`. UI automation uses PeekabooBridge.

## Goals

*   Single GUI app instance that owns all TCC-facing work (notifications, screen recording, mic, speech, AppleScript).
*   A small surface for automation: Gateway + node commands, plus PeekabooBridge for UI automation.
*   Predictable permissions: always the same signed bundle ID, launched by launchd, so TCC grants stick.

## How it works

### Gateway + node transport

*   The app runs the Gateway (local mode) and connects to it as a node.
*   Agent actions are performed via `node.invoke` (e.g. `system.run`, `system.notify`, `canvas.*`).

### Node service + app IPC

*   A headless node host service connects to the Gateway WebSocket.
*   `system.run` requests are forwarded to the macOS app over a local Unix socket.
*   The app performs the exec in UI context, prompts if needed, and returns output.

Diagram (SCI):

```
Agent -> Gateway -> Node Service (WS)
                      |  IPC (UDS + token + HMAC + TTL)
                      v
                  Mac App (UI + TCC + system.run)
```

### PeekabooBridge (UI automation)

*   UI automation uses a separate UNIX socket named `bridge.sock` and the PeekabooBridge JSON protocol.
*   Host preference order (client-side): Peekaboo.app → Claude.app → OpenClaw.app → local execution.
*   Security: bridge hosts require an allowed TeamID; DEBUG-only same-UID escape hatch is guarded by `PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1` (Peekaboo convention).
*   See: [PeekabooBridge usage](https://docs.openclaw.ai/platforms/mac/peekaboo) for details.

## Operational flows

*   Restart/rebuild: `SIGN_IDENTITY="Apple Development: <Developer Name> (<TEAMID>)" scripts/restart-mac.sh`
    *   Kills existing instances
    *   Swift build + package
    *   Writes/bootstraps/kickstarts the LaunchAgent
*   Single instance: app exits early if another instance with the same bundle ID is running.

## Hardening notes

*   Prefer requiring a TeamID match for all privileged surfaces.
*   PeekabooBridge: `PEEKABOO_ALLOW_UNSIGNED_SOCKET_CLIENTS=1` (DEBUG-only) may allow same-UID callers for local development.
*   All communication remains local-only; no network sockets are exposed.
*   TCC prompts originate only from the GUI app bundle; keep the signed bundle ID stable across rebuilds.
*   IPC hardening: socket mode `0600`, token, peer-UID checks, HMAC challenge/response, short TTL.

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/mac/canvas -->

# Canvas - OpenClaw

## Canvas (macOS app)

The macOS app embeds an agent‑controlled **Canvas panel** using `WKWebView`. It is a lightweight visual workspace for HTML/CSS/JS, A2UI, and small interactive UI surfaces.

## Where Canvas lives

Canvas state is stored under Application Support:

*   `~/Library/Application Support/OpenClaw/canvas/<session>/...`

The Canvas panel serves those files via a **custom URL scheme**:

*   `openclaw-canvas://<session>/<path>`

Examples:

*   `openclaw-canvas://main/` → `<canvasRoot>/main/index.html`
*   `openclaw-canvas://main/assets/app.css` → `<canvasRoot>/main/assets/app.css`
*   `openclaw-canvas://main/widgets/todo/` → `<canvasRoot>/main/widgets/todo/index.html`

If no `index.html` exists at the root, the app shows a **built‑in scaffold page**.

## Panel behavior

*   Borderless, resizable panel anchored near the menu bar (or mouse cursor).
*   Remembers size/position per session.
*   Auto‑reloads when local canvas files change.
*   Only one Canvas panel is visible at a time (session is switched as needed).

Canvas can be disabled from Settings → **Allow Canvas**. When disabled, canvas node commands return `CANVAS_DISABLED`.

## Agent API surface

Canvas is exposed via the **Gateway WebSocket**, so the agent can:

*   show/hide the panel
*   navigate to a path or URL
*   evaluate JavaScript
*   capture a snapshot image

CLI examples:

```
openclaw nodes canvas present --node <id>
openclaw nodes canvas navigate --node <id> --url "/"
openclaw nodes canvas eval --node <id> --js "document.title"
openclaw nodes canvas snapshot --node <id>
```

Notes:

*   `canvas.navigate` accepts **local canvas paths**, `http(s)` URLs, and `file://` URLs.
*   If you pass `"/"`, the Canvas shows the local scaffold or `index.html`.

## A2UI in Canvas

A2UI is hosted by the Gateway canvas host and rendered inside the Canvas panel. When the Gateway advertises a Canvas host, the macOS app auto‑navigates to the A2UI host page on first open. Default A2UI host URL:

```
http://<gateway-host>:18789/__openclaw__/a2ui/
```

### A2UI commands (v0.8)

Canvas currently accepts **A2UI v0.8** server→client messages:

*   `beginRendering`
*   `surfaceUpdate`
*   `dataModelUpdate`
*   `deleteSurface`

`createSurface` (v0.9) is not supported. CLI example:

```
cat > /tmp/a2ui-v0.8.jsonl <<'EOFA2'
{"surfaceUpdate":{"surfaceId":"main","components":[{"id":"root","component":{"Column":{"children":{"explicitList":["title","content"]}}}},{"id":"title","component":{"Text":{"text":{"literalString":"Canvas (A2UI v0.8)"},"usageHint":"h1"}}},{"id":"content","component":{"Text":{"text":{"literalString":"If you can read this, A2UI push works."},"usageHint":"body"}}}]}}
{"beginRendering":{"surfaceId":"main","root":"root"}}
EOFA2

openclaw nodes canvas a2ui push --jsonl /tmp/a2ui-v0.8.jsonl --node <id>
```

Quick smoke:

```
openclaw nodes canvas a2ui push --node <id> --text "Hello from A2UI"
```

## Triggering agent runs from Canvas

Canvas can trigger new agent runs via deep links:

*   `openclaw://agent?...`

Example (in JS):

```
window.location.href = "openclaw://agent?message=Review%20this%20design";
```

The app prompts for confirmation unless a valid key is provided.

## Security notes

*   Canvas scheme blocks directory traversal; files must live under the session root.
*   Local Canvas content uses a custom scheme (no loopback server required).
*   External `http(s)` URLs are allowed only when explicitly navigated.

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/mac/permissions -->

# macOS Permissions - OpenClaw

macOS permission grants are fragile. TCC associates a permission grant with the app’s code signature, bundle identifier, and on-disk path. If any of those change, macOS treats the app as new and may drop or hide prompts.

## Requirements for stable permissions

*   Same path: run the app from a fixed location (for OpenClaw, `dist/OpenClaw.app`).
*   Same bundle identifier: changing the bundle ID creates a new permission identity.
*   Signed app: unsigned or ad-hoc signed builds do not persist permissions.
*   Consistent signature: use a real Apple Development or Developer ID certificate so the signature stays stable across rebuilds.

Ad-hoc signatures generate a new identity every build. macOS will forget previous grants, and prompts can disappear entirely until the stale entries are cleared.

## Recovery checklist when prompts disappear

1.  Quit the app.
2.  Remove the app entry in System Settings -> Privacy & Security.
3.  Relaunch the app from the same path and re-grant permissions.
4.  If the prompt still does not appear, reset TCC entries with `tccutil` and try again.
5.  Some permissions only reappear after a full macOS restart.

Example resets (replace bundle ID as needed):

```
sudo tccutil reset Accessibility ai.openclaw.mac
sudo tccutil reset ScreenCapture ai.openclaw.mac
sudo tccutil reset AppleEvents
```

## Files and folders permissions (Desktop/Documents/Downloads)

macOS may also gate Desktop, Documents, and Downloads for terminal/background processes. If file reads or directory listings hang, grant access to the same process context that performs file operations (for example Terminal/iTerm, LaunchAgent-launched app, or SSH process). Workaround: move files into the OpenClaw workspace (`~/.openclaw/workspace`) if you want to avoid per-folder grants. If you are testing permissions, always sign with a real certificate. Ad-hoc builds are only acceptable for quick local runs where permissions do not matter.

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/mac/signing -->

# macOS Signing - OpenClaw

## mac signing (debug builds)

This app is usually built from [`scripts/package-mac-app.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/package-mac-app.sh), which now:

*   sets a stable debug bundle identifier: `ai.openclaw.mac.debug`
*   writes the Info.plist with that bundle id (override via `BUNDLE_ID=...`)
*   calls [`scripts/codesign-mac-app.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/codesign-mac-app.sh) to sign the main binary and app bundle so macOS treats each rebuild as the same signed bundle and keeps TCC permissions (notifications, accessibility, screen recording, mic, speech). For stable permissions, use a real signing identity; ad-hoc is opt-in and fragile (see [macOS permissions](https://docs.openclaw.ai/platforms/mac/permissions)).
*   uses `CODESIGN_TIMESTAMP=auto` by default; it enables trusted timestamps for Developer ID signatures. Set `CODESIGN_TIMESTAMP=off` to skip timestamping (offline debug builds).
*   inject build metadata into Info.plist: `OpenClawBuildTimestamp` (UTC) and `OpenClawGitCommit` (short hash) so the About pane can show build, git, and debug/release channel.
*   **Packaging requires Node 22+**: the script runs TS builds and the Control UI build.
*   reads `SIGN_IDENTITY` from the environment. Add `export SIGN_IDENTITY="Apple Development: Your Name (TEAMID)"` (or your Developer ID Application cert) to your shell rc to always sign with your cert. Ad-hoc signing requires explicit opt-in via `ALLOW_ADHOC_SIGNING=1` or `SIGN_IDENTITY="-"` (not recommended for permission testing).
*   runs a Team ID audit after signing and fails if any Mach-O inside the app bundle is signed by a different Team ID. Set `SKIP_TEAM_ID_CHECK=1` to bypass.

## Usage

```
# from repo root
scripts/package-mac-app.sh               # auto-selects identity; errors if none found
SIGN_IDENTITY="Developer ID Application: Your Name" scripts/package-mac-app.sh   # real cert
ALLOW_ADHOC_SIGNING=1 scripts/package-mac-app.sh    # ad-hoc (permissions will not stick)
SIGN_IDENTITY="-" scripts/package-mac-app.sh        # explicit ad-hoc (same caveat)
DISABLE_LIBRARY_VALIDATION=1 scripts/package-mac-app.sh   # dev-only Sparkle Team ID mismatch workaround
```

### Ad-hoc Signing Note

When signing with `SIGN_IDENTITY="-"` (ad-hoc), the script automatically disables the **Hardened Runtime** (`--options runtime`). This is necessary to prevent crashes when the app attempts to load embedded frameworks (like Sparkle) that do not share the same Team ID. Ad-hoc signatures also break TCC permission persistence; see [macOS permissions](https://docs.openclaw.ai/platforms/mac/permissions) for recovery steps.

`package-mac-app.sh` stamps the bundle with:

*   `OpenClawBuildTimestamp`: ISO8601 UTC at package time
*   `OpenClawGitCommit`: short git hash (or `unknown` if unavailable)

The About tab reads these keys to show version, build date, git commit, and whether it’s a debug build (via `#if DEBUG`). Run the packager to refresh these values after code changes.

## Why

TCC permissions are tied to the bundle identifier _and_ code signature. Unsigned debug builds with changing UUIDs were causing macOS to forget grants after each rebuild. Signing the binaries (ad‑hoc by default) and keeping a fixed bundle id/path (`dist/OpenClaw.app`) preserves the grants between builds, matching the VibeTunnel approach.

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/mac/icon -->

# Menu Bar Icon - OpenClaw

Author: steipete · Updated: 2025-12-06 · Scope: macOS app (`apps/macos`)

*   **Idle:** Normal icon animation (blink, occasional wiggle).
*   **Paused:** Status item uses `appearsDisabled`; no motion.
*   **Voice trigger (big ears):** Voice wake detector calls `AppState.triggerVoiceEars(ttl: nil)` when the wake word is heard, keeping `earBoostActive=true` while the utterance is captured. Ears scale up (1.9x), get circular ear holes for readability, then drop via `stopVoiceEars()` after 1s of silence. Only fired from the in-app voice pipeline.
*   **Working (agent running):** `AppState.isWorking=true` drives a “tail/leg scurry” micro-motion: faster leg wiggle and slight offset while work is in-flight. Currently toggled around WebChat agent runs; add the same toggle around other long tasks when you wire them.

Wiring points

*   Voice wake: runtime/tester call `AppState.triggerVoiceEars(ttl: nil)` on trigger and `stopVoiceEars()` after 1s of silence to match the capture window.
*   Agent activity: set `AppStateStore.shared.setWorking(true/false)` around work spans (already done in WebChat agent call). Keep spans short and reset in `defer` blocks to avoid stuck animations.

Shapes & sizes

*   Base icon drawn in `CritterIconRenderer.makeIcon(blink:legWiggle:earWiggle:earScale:earHoles:)`.
*   Ear scale defaults to `1.0`; voice boost sets `earScale=1.9` and toggles `earHoles=true` without changing overall frame (18×18 pt template image rendered into a 36×36 px Retina backing store).
*   Scurry uses leg wiggle up to ~1.0 with a small horizontal jiggle; it’s additive to any existing idle wiggle.

Behavioral notes

*   No external CLI/broker toggle for ears/working; keep it internal to the app’s own signals to avoid accidental flapping.
*   Keep TTLs short (<10s) so the icon returns to baseline quickly if a job hangs.

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/mac/voicewake -->

# Voice Wake - OpenClaw

## Voice Wake & Push-to-Talk

## Modes

*   **Wake-word mode** (default): always-on Speech recognizer waits for trigger tokens (`swabbleTriggerWords`). On match it starts capture, shows the overlay with partial text, and auto-sends after silence.
*   **Push-to-talk (Right Option hold)**: hold the right Option key to capture immediately—no trigger needed. The overlay appears while held; releasing finalizes and forwards after a short delay so you can tweak text.

## Runtime behavior (wake-word)

*   Speech recognizer lives in `VoiceWakeRuntime`.
*   Trigger only fires when there’s a **meaningful pause** between the wake word and the next word (~0.55s gap). The overlay/chime can start on the pause even before the command begins.
*   Silence windows: 2.0s when speech is flowing, 5.0s if only the trigger was heard.
*   Hard stop: 120s to prevent runaway sessions.
*   Debounce between sessions: 350ms.
*   Overlay is driven via `VoiceWakeOverlayController` with committed/volatile coloring.
*   After send, recognizer restarts cleanly to listen for the next trigger.

## Lifecycle invariants

*   If Voice Wake is enabled and permissions are granted, the wake-word recognizer should be listening (except during an explicit push-to-talk capture).
*   Overlay visibility (including manual dismiss via the X button) must never prevent the recognizer from resuming.

## Sticky overlay failure mode (previous)

Previously, if the overlay got stuck visible and you manually closed it, Voice Wake could appear “dead” because the runtime’s restart attempt could be blocked by overlay visibility and no subsequent restart was scheduled. Hardening:

*   Wake runtime restart is no longer blocked by overlay visibility.
*   Overlay dismiss completion triggers a `VoiceWakeRuntime.refresh(...)` via `VoiceSessionCoordinator`, so manual X-dismiss always resumes listening.

## Push-to-talk specifics

*   Hotkey detection uses a global `.flagsChanged` monitor for **right Option** (`keyCode 61` + `.option`). We only observe events (no swallowing).
*   Capture pipeline lives in `VoicePushToTalk`: starts Speech immediately, streams partials to the overlay, and calls `VoiceWakeForwarder` on release.
*   When push-to-talk starts we pause the wake-word runtime to avoid dueling audio taps; it restarts automatically after release.
*   Permissions: requires Microphone + Speech; seeing events needs Accessibility/Input Monitoring approval.
*   External keyboards: some may not expose right Option as expected—offer a fallback shortcut if users report misses.

## User-facing settings

*   **Voice Wake** toggle: enables wake-word runtime.
*   **Hold Cmd+Fn to talk**: enables the push-to-talk monitor. Disabled on macOS < 26.
*   Language & mic pickers, live level meter, trigger-word table, tester (local-only; does not forward).
*   Mic picker preserves the last selection if a device disconnects, shows a disconnected hint, and temporarily falls back to the system default until it returns.
*   **Sounds**: chimes on trigger detect and on send; defaults to the macOS “Glass” system sound. You can pick any `NSSound`\-loadable file (e.g. MP3/WAV/AIFF) for each event or choose **No Sound**.

## Forwarding behavior

*   When Voice Wake is enabled, transcripts are forwarded to the active gateway/agent (the same local vs remote mode used by the rest of the mac app).
*   Replies are delivered to the **last-used main provider** (WhatsApp/Telegram/Discord/WebChat). If delivery fails, the error is logged and the run is still visible via WebChat/session logs.

## Forwarding payload

*   `VoiceWakeForwarder.prefixedTranscript(_:)` prepends the machine hint before sending. Shared between wake-word and push-to-talk paths.

## Quick verification

*   Toggle push-to-talk on, hold Cmd+Fn, speak, release: overlay should show partials then send.
*   While holding, menu-bar ears should stay enlarged (uses `triggerVoiceEars(ttl:nil)`); they drop after release.

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/mac/release -->

# macOS Release - OpenClaw

This app now ships Sparkle auto-updates. Release builds must be Developer ID–signed, zipped, and published with a signed appcast entry.

## Prereqs

*   Developer ID Application cert installed (example: `Developer ID Application: <Developer Name> (<TEAMID>)`).
*   Sparkle private key path set in the environment as `SPARKLE_PRIVATE_KEY_FILE` (path to your Sparkle ed25519 private key; public key baked into Info.plist). If it is missing, check `~/.profile`.
*   Notary credentials (keychain profile or API key) for `xcrun notarytool` if you want Gatekeeper-safe DMG/zip distribution.
    *   We use a Keychain profile named `openclaw-notary`, created from App Store Connect API key env vars in your shell profile:
        *   `APP_STORE_CONNECT_API_KEY_P8`, `APP_STORE_CONNECT_KEY_ID`, `APP_STORE_CONNECT_ISSUER_ID`
        *   `echo "$APP_STORE_CONNECT_API_KEY_P8" | sed 's/\\n/\n/g' > /tmp/openclaw-notary.p8`
        *   `xcrun notarytool store-credentials "openclaw-notary" --key /tmp/openclaw-notary.p8 --key-id "$APP_STORE_CONNECT_KEY_ID" --issuer "$APP_STORE_CONNECT_ISSUER_ID"`
*   `pnpm` deps installed (`pnpm install --config.node-linker=hoisted`).
*   Sparkle tools are fetched automatically via SwiftPM at `apps/macos/.build/artifacts/sparkle/Sparkle/bin/` (`sign_update`, `generate_appcast`, etc.).

## Build & package

Notes:

*   `APP_BUILD` maps to `CFBundleVersion`/`sparkle:version`; keep it numeric + monotonic (no `-beta`), or Sparkle compares it as equal.
*   If `APP_BUILD` is omitted, `scripts/package-mac-app.sh` derives a Sparkle-safe default from `APP_VERSION` (`YYYYMMDDNN`: stable defaults to `90`, prereleases use a suffix-derived lane) and uses the higher of that value and git commit count.
*   You can still override `APP_BUILD` explicitly when release engineering needs a specific monotonic value.
*   For `BUILD_CONFIG=release`, `scripts/package-mac-app.sh` now defaults to universal (`arm64 x86_64`) automatically. You can still override with `BUILD_ARCHS=arm64` or `BUILD_ARCHS=x86_64`. For local/dev builds (`BUILD_CONFIG=debug`), it defaults to the current architecture (`$(uname -m)`).
*   Use `scripts/package-mac-dist.sh` for release artifacts (zip + DMG + notarization). Use `scripts/package-mac-app.sh` for local/dev packaging.

```
# From repo root; set release IDs so Sparkle feed is enabled.
# This command builds release artifacts without notarization.
# APP_BUILD must be numeric + monotonic for Sparkle compare.
# Default is auto-derived from APP_VERSION when omitted.
SKIP_NOTARIZE=1 \
BUNDLE_ID=ai.openclaw.mac \
APP_VERSION=2026.3.8 \
BUILD_CONFIG=release \
SIGN_IDENTITY="Developer ID Application: <Developer Name> (<TEAMID>)" \
scripts/package-mac-dist.sh

# `package-mac-dist.sh` already creates the zip + DMG.
# If you used `package-mac-app.sh` directly instead, create them manually:
# If you want notarization/stapling in this step, use the NOTARIZE command below.
ditto -c -k --sequesterRsrc --keepParent dist/OpenClaw.app dist/OpenClaw-2026.3.8.zip

# Optional: build a styled DMG for humans (drag to /Applications)
scripts/create-dmg.sh dist/OpenClaw.app dist/OpenClaw-2026.3.8.dmg

# Recommended: build + notarize/staple zip + DMG
# First, create a keychain profile once:
#   xcrun notarytool store-credentials "openclaw-notary" \
#     --apple-id "<apple-id>" --team-id "<team-id>" --password "<app-specific-password>"
NOTARIZE=1 NOTARYTOOL_PROFILE=openclaw-notary \
BUNDLE_ID=ai.openclaw.mac \
APP_VERSION=2026.3.8 \
BUILD_CONFIG=release \
SIGN_IDENTITY="Developer ID Application: <Developer Name> (<TEAMID>)" \
scripts/package-mac-dist.sh

# Optional: ship dSYM alongside the release
ditto -c -k --keepParent apps/macos/.build/release/OpenClaw.app.dSYM dist/OpenClaw-2026.3.8.dSYM.zip
```

## Appcast entry

Use the release note generator so Sparkle renders formatted HTML notes:

```
SPARKLE_PRIVATE_KEY_FILE=/path/to/ed25519-private-key scripts/make_appcast.sh dist/OpenClaw-2026.3.8.zip https://raw.githubusercontent.com/openclaw/openclaw/main/appcast.xml
```

Generates HTML release notes from `CHANGELOG.md` (via [`scripts/changelog-to-html.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/changelog-to-html.sh)) and embeds them in the appcast entry. Commit the updated `appcast.xml` alongside the release assets (zip + dSYM) when publishing.

## Publish & verify

*   Upload `OpenClaw-2026.3.8.zip` (and `OpenClaw-2026.3.8.dSYM.zip`) to the GitHub release for tag `v2026.3.8`.
*   Ensure the raw appcast URL matches the baked feed: `https://raw.githubusercontent.com/openclaw/openclaw/main/appcast.xml`.
*   Sanity checks:
    *   `curl -I https://raw.githubusercontent.com/openclaw/openclaw/main/appcast.xml` returns 200.
    *   `curl -I <enclosure url>` returns 200 after assets upload.
    *   On a previous public build, run “Check for Updates…” from the About tab and verify Sparkle installs the new build cleanly.

Definition of done: signed app + appcast are published, update flow works from an older installed version, and release assets are attached to the GitHub release.

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/mac/logging -->

# macOS Logging - OpenClaw

## Rolling diagnostics file log (Debug pane)

OpenClaw routes macOS app logs through swift-log (unified logging by default) and can write a local, rotating file log to disk when you need a durable capture.

*   Verbosity: **Debug pane → Logs → App logging → Verbosity**
*   Enable: **Debug pane → Logs → App logging → “Write rolling diagnostics log (JSONL)”**
*   Location: `~/Library/Logs/OpenClaw/diagnostics.jsonl` (rotates automatically; old files are suffixed with `.1`, `.2`, …)
*   Clear: **Debug pane → Logs → App logging → “Clear”**

Notes:

*   This is **off by default**. Enable only while actively debugging.
*   Treat the file as sensitive; don’t share it without review.

## Unified logging private data on macOS

Unified logging redacts most payloads unless a subsystem opts into `privacy -off`. Per Peter’s write-up on macOS [logging privacy shenanigans](https://steipete.me/posts/2025/logging-privacy-shenanigans) (2025) this is controlled by a plist in `/Library/Preferences/Logging/Subsystems/` keyed by the subsystem name. Only new log entries pick up the flag, so enable it before reproducing an issue.

## Enable for OpenClaw (`ai.openclaw`)

*   Write the plist to a temp file first, then install it atomically as root:

```
cat <<'EOF' >/tmp/ai.openclaw.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>DEFAULT-OPTIONS</key>
    <dict>
        <key>Enable-Private-Data</key>
        <true/>
    </dict>
</dict>
</plist>
EOF
sudo install -m 644 -o root -g wheel /tmp/ai.openclaw.plist /Library/Preferences/Logging/Subsystems/ai.openclaw.plist
```

*   No reboot is required; logd notices the file quickly, but only new log lines will include private payloads.
*   View the richer output with the existing helper, e.g. `./scripts/clawlog.sh --category WebChat --last 5m`.

## Disable after debugging

*   Remove the override: `sudo rm /Library/Preferences/Logging/Subsystems/ai.openclaw.plist`.
*   Optionally run `sudo log config --reload` to force logd to drop the override immediately.
*   Remember this surface can include phone numbers and message bodies; keep the plist in place only while you actively need the extra detail.

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/mac/health -->

# Health Checks - OpenClaw

## Health Checks on macOS

How to see whether the linked channel is healthy from the menu bar app.

*   Status dot now reflects Baileys health:
    *   Green: linked + socket opened recently.
    *   Orange: connecting/retrying.
    *   Red: logged out or probe failed.
*   Secondary line reads “linked · auth 12m” or shows the failure reason.
*   “Run Health Check” menu item triggers an on-demand probe.

## Settings

*   General tab gains a Health card showing: linked auth age, session-store path/count, last check time, last error/status code, and buttons for Run Health Check / Reveal Logs.
*   Uses a cached snapshot so the UI loads instantly and falls back gracefully when offline.
*   **Channels tab** surfaces channel status + controls for WhatsApp/Telegram (login QR, logout, probe, last disconnect/error).

## How the probe works

*   App runs `openclaw health --json` via `ShellExecutor` every ~60s and on demand. The probe loads creds and reports status without sending messages.
*   Cache the last good snapshot and the last error separately to avoid flicker; show the timestamp of each.

## When in doubt

*   You can still use the CLI flow in [Gateway health](https://docs.openclaw.ai/gateway/health) (`openclaw status`, `openclaw status --deep`, `openclaw health --json`) and tail `/tmp/openclaw/openclaw-*.log` for `web-heartbeat` / `web-reconnect`.

