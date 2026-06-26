# OpenClaw Platforms Reference

## Table of Contents
- [Overview](#overview)
- [macOS](#macos)
- [Windows](#windows)
- [Linux](#linux)
- [iOS](#ios)
- [Android](#android)
- [VPS Hosting](#vps-hosting)
- [Web UI (Control UI & Dashboard)](#web-ui-control-ui--dashboard)

## Overview

OpenClaw core is written in TypeScript. **Node is the recommended runtime.** Bun is not recommended for the Gateway (known issues with WhatsApp and Telegram channels).

Companion apps exist for:
- **macOS**: menu bar app (available)
- **iOS**: internal preview (not publicly distributed yet)
- **Android**: source available, not publicly released

**Gateway service install target by OS:**
- macOS: LaunchAgent (`ai.openclaw.gateway` or `ai.openclaw.<profile>`)
- Linux/WSL2: systemd user service (`openclaw-gateway[-<profile>].service`)
- Native Windows: Scheduled Task (`OpenClaw Gateway` or `OpenClaw Gateway (<profile>)`) with per-user Startup-folder fallback

---

## macOS

### What the macOS App Does

The macOS app is the **menu-bar companion** for OpenClaw. It:
- Shows native notifications and status in the menu bar
- Owns TCC prompts (Notifications, Accessibility, Screen Recording, Microphone, Speech Recognition, Automation/AppleScript)
- Runs or connects to the Gateway (local or remote)
- Exposes macOS-only tools (Canvas, Camera, Screen Recording, `system.run`)
- Starts the local node host service in **remote** mode (launchd), and stops it in **local** mode
- Optionally hosts **PeekabooBridge** for UI automation
- Installs the global CLI (`openclaw`) on request via npm, pnpm, or bun (app prefers npm, then pnpm, then bun)

### Local vs Remote Mode

**Local** (default): the app attaches to a running local Gateway if present; otherwise enables the launchd service via `openclaw gateway install`.

**Remote**: the app connects to a Gateway over SSH/Tailscale and never starts a local process. The app starts the local **node host service** so the remote Gateway can reach this Mac.

Gateway discovery prefers Tailscale MagicDNS names over raw tailnet IPs, so the Mac app recovers more reliably when tailnet IPs change.

### Launchd Control

The app manages a per-user LaunchAgent labeled `ai.openclaw.gateway` (or `ai.openclaw.<profile>` with `--profile`/`OPENCLAW_PROFILE`; legacy `com.openclaw.*` still unloads).

```bash
launchctl kickstart -k gui/$UID/ai.openclaw.gateway
launchctl bootout gui/$UID/ai.openclaw.gateway
```

### Node Capabilities (macOS)

Common commands exposed:
- Canvas: `canvas.present`, `canvas.navigate`, `canvas.eval`, `canvas.snapshot`, `canvas.a2ui.*`
- Camera: `camera.snap`, `camera.clip`
- Screen: `screen.snapshot`, `screen.record`
- System: `system.run`, `system.notify`

The node reports a `permissions` map so agents can decide what's allowed.

**Node service + app IPC architecture:**
```
Gateway → Node Service (WS)
                 |  IPC (UDS + token + HMAC + TTL)
                 v
             Mac App (UI + TCC + system.run)
```

When the headless node host service is running (remote mode), it connects to the Gateway WS as a node. `system.run` executes in the macOS app (UI/TCC context) over a local Unix socket; prompts + output stay in-app.

### Exec Approvals (system.run)

`system.run` is controlled by **Exec approvals** in Settings → Exec approvals. Stored at `~/.openclaw/exec-approvals.json`.

```json
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

**Notes:**
- `allowlist` entries are glob patterns for resolved binary paths
- Raw shell command text containing shell control/expansion syntax (`&&`, `||`, `;`, `|`, `` ` ``, `$`, `<`, `>`, `(`, `)`) is treated as an allowlist miss
- Choosing "Always Allow" in the prompt adds that command to the allowlist
- Environment overrides are filtered (drops `PATH`, `DYLD_*`, `LD_*`, `NODE_OPTIONS`, `PYTHON*`, `PERL*`, `RUBYOPT`, `SHELLOPTS`, `PS4`)
- For shell wrappers (`bash|sh|zsh ... -c/-lc`), request-scoped env overrides are reduced to: `TERM`, `LANG`, `LC_*`, `COLORTERM`, `NO_COLOR`, `FORCE_COLOR`
- For allow-always decisions, known dispatch wrappers (`env`, `nice`, `nohup`, `stdbuf`, `timeout`) persist inner executable paths instead of wrapper paths

### Deep Links

The app registers the `openclaw://` URL scheme.

**`openclaw://agent`** — Triggers a Gateway `agent` request:
```bash
open 'openclaw://agent?message=Hello%20from%20deep%20link'
```

Query parameters:
- `message` (required)
- `sessionKey` (optional)
- `thinking` (optional)
- `deliver` / `to` / `channel` (optional)
- `timeoutSeconds` (optional)
- `key` (optional — unattended mode key)

**Safety:**
- Without `key`, the app prompts for confirmation and enforces a short message limit
- With a valid `key`, the run is unattended (intended for personal automations)

### Onboarding Flow (Typical)

1. Install and launch **OpenClaw.app**
2. Complete the permissions checklist (TCC prompts)
3. Ensure **Local** mode is active and the Gateway is running
4. Install the CLI if you want terminal access

### State Dir Placement (macOS)

Avoid putting your OpenClaw state dir in iCloud or other cloud-synced folders (can add latency and cause file-lock/sync races for sessions and credentials).

Prefer: `OPENCLAW_STATE_DIR=~/.openclaw`

Paths `openclaw doctor` warns about:
- `~/Library/Mobile Documents/com~apple~CloudDocs/...`
- `~/Library/CloudStorage/...`

### Build & Dev Workflow (Native)

```bash
cd apps/macos && swift build
swift run OpenClaw  # or Xcode
scripts/package-mac-app.sh  # package app
```

### Debug Gateway Connectivity (macOS CLI)

```bash
cd apps/macos
swift run openclaw-mac connect --json
swift run openclaw-mac discover --timeout 3000 --json
```

Connect options:
- `--url <ws://host:port>`: override config
- `--mode <local|remote>`: resolve from config (default: config or local)
- `--probe`: force a fresh health probe
- `--timeout <ms>`: request timeout (default: `15000`)
- `--json`: structured output for diffing

Discovery options:
- `--include-local`: include gateways filtered as "local"
- `--timeout <ms>`: overall discovery window (default: `2000`)
- `--json`: structured output for diffing

Tip: compare against `openclaw gateway discover --json` to see whether the macOS app’s discovery pipeline (`local.` plus configured wide-area domain, with wide-area and Tailscale Serve fallbacks) differs from the Node CLI’s `dns-sd` based discovery.

### Remote Connection Plumbing (SSH Tunnels)

When in **Remote** mode, the app opens an SSH tunnel.

**Control tunnel (Gateway WebSocket port):**
- Purpose: health checks, status, Web Chat, config, and other control-plane calls
- Local port: the Gateway port (default `18789`), always stable
- SSH shape: `ssh -N -L <local>:127.0.0.1:<remote>` with BatchMode + ExitOnForwardFailure + keepalive options
- Note: the SSH tunnel uses loopback, so the gateway will see the node IP as `127.0.0.1`. Use **Direct (ws/wss)** transport if you want the real client IP.

---

## Windows

OpenClaw supports both **native Windows** and **WSL2**. WSL2 is the more stable path and recommended for the full experience.

Native Windows companion apps are not yet available. The live docs state: "We do not have a Windows companion app yet. Contributions are welcome if you want contributions to make it happen."

### WSL2 (Recommended)

- Follow [Getting Started](/start/getting-started) inside WSL
- Official WSL2 guide: https://learn.microsoft.com/windows/wsl/install

**Step-by-step WSL2 install:**

1. **Install WSL2 + Ubuntu** (PowerShell as Admin):
```powershell
wsl --install
# Or pick a distro explicitly:
wsl --list --online
wsl --install -d Ubuntu-24.04
```
Reboot if Windows asks.

2. **Enable systemd** (required for gateway install):
```bash
sudo tee /etc/wsl.conf >/dev/null <<'EOF'
[boot]
systemd=true
EOF
```
Then from PowerShell: `wsl --shutdown`, then re-open Ubuntu.

Verify: `systemctl --user status`

3. **Install OpenClaw** (inside WSL):
```bash
git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm build
pnpm ui:build
pnpm openclaw onboard --install-daemon
```

If developing from source instead of first-time onboarding, use the source dev loop:
```bash
pnpm install
pnpm openclaw setup   # first run only (or after resetting config/workspace)
pnpm gateway:watch
```

### Native Windows Status

What works well today:
- Website installer via `install.ps1`
- Local CLI use: `openclaw --version`, `openclaw doctor`, `openclaw plugins list --json`
- Embedded local-agent/provider smoke

Current caveats:
- `openclaw onboard --non-interactive` expects a reachable local gateway unless you pass `--skip-health`
- `openclaw gateway install` tries Windows Scheduled Tasks first (preferred because they provide better supervisor status)
- If Scheduled Task creation is denied, the **fallback service mode still auto-starts after login through the current user's Startup folder**
- If `schtasks` itself wedges, OpenClaw aborts that path quickly and falls back

**Native Windows smoke test (no gateway service required):**
```powershell
openclaw agent --local --agent main --thinking low -m "Reply with exactly WINDOWS-HATCH-OK."
```

**Native CLI only (no gateway service install):**
```powershell
openclaw onboard --non-interactive --skip-health
openclaw gateway run
```

**Managed startup on native Windows:**
```powershell
openclaw gateway install
openclaw gateway status --json
```

### Gateway Auto-Start Before Windows Login

```bash
# Inside WSL: keep user services running without login
sudo loginctl enable-linger "$(whoami)"

# Inside WSL: install the OpenClaw gateway user service
openclaw gateway install

# PowerShell as Administrator: start WSL automatically at Windows boot
schtasks /create /tn "WSL Boot" /tr "wsl.exe -d Ubuntu --exec /bin/true" /sc onstart /ru SYSTEM
```

Replace `Ubuntu` with your distro name from `wsl --list --verbose`.

**Verify startup chain** (after reboot, before Windows sign-in):
```bash
systemctl --user is-enabled openclaw-gateway.service
systemctl --user status openclaw-gateway.service --no-pager
```

### Expose WSL Services Over LAN (portproxy)

WSL has its own virtual network. To forward a Windows port to a WSL service:

```powershell
$Distro = "Ubuntu-24.04"
$ListenPort = 2222
$TargetPort = 22

$WslIp = (wsl -d $Distro -- hostname -I).Trim().Split(" ")[0]
if (-not $WslIp) { throw "WSL IP not found." }

netsh interface portproxy add v4tov4 listenaddress=0.0.0.0 listenport=$ListenPort `
  connectaddress=$WslIp connectport=$TargetPort
```

Allow port through Windows Firewall (one-time):
```powershell
New-NetFirewallRule -DisplayName "WSL SSH $ListenPort" -Direction Inbound `
  -Protocol TCP -LocalPort $ListenPort -Action Allow
```

Refresh portproxy after WSL restarts:
```powershell
netsh interface portproxy delete v4tov4 listenport=$ListenPort listenaddress=0.0.0.0 | Out-Null
netsh interface portproxy add v4tov4 listenport=$ListenPort listenaddress=0.0.0.0 `
  connectaddress=$WslIp connectport=$TargetPort | Out-Null
```

**Notes:**
- SSH from another machine targets the **Windows host IP**: `ssh user@windows-host -p 2222`
- Remote nodes must point at a **reachable** Gateway URL (not `127.0.0.1`)
- Use `listenaddress=0.0.0.0` for LAN access; `127.0.0.1` keeps it local only

---

## Linux

The Gateway is fully supported on Linux. **Node is the recommended runtime.** Bun is not recommended (WhatsApp/Telegram bugs).

Native Linux companion apps are planned.

### Beginner Quick Path (VPS)

1. Install Node 24 (recommended; Node 22 LTS, currently `22.14+`, still works for compatibility): `curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash - && sudo apt install -y nodejs`
2. `npm i -g openclaw@latest`
3. `openclaw onboard --install-daemon`
4. From your laptop: `ssh -N -L 18789:127.0.0.1:18789 <user>@<host>`
5. Open `http://127.0.0.1:18789/` and authenticate with the configured shared secret (token by default; password if you set `gateway.auth.mode: "password"`)

**Systemd unit note:** `openclaw gateway install` and `openclaw onboard --install-daemon` already render the current canonical unit for you; write one by hand only when you need a custom system/service-manager setup. The full service guidance lives in the Gateway runbook.

Full Linux server guide: [Linux Server](/vps). Step-by-step VPS example: [exe.dev](/install/exe-dev)

### Gateway Service Install

```bash
openclaw onboard --install-daemon
# OR
openclaw gateway install
# OR
openclaw configure  # then select Gateway service
```

Repair/migrate: `openclaw doctor`

### System Control (systemd User Unit)

OpenClaw installs a systemd **user** service by default. Use a **system** service for shared or always-on servers.

**Minimal unit:**
```ini
[Unit]
Description=OpenClaw Gateway (profile: <profile>, v<version>)
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/local/bin/openclaw gateway --port 18789
Restart=always
RestartSec=5
TimeoutStopSec=30
TimeoutStartSec=30
SuccessExitStatus=0 143
KillMode=control-group

[Install]
WantedBy=default.target
```

```bash
systemctl --user enable --now openclaw-gateway.service
```

### Memory Pressure and OOM Kills

On Linux, OpenClaw biases transient child processes to be killed before the Gateway when possible.

For eligible Linux child spawns, OpenClaw starts the child through a short `/bin/sh` wrapper that raises the child's own `oom_score_adj` to `1000`, then `exec`s the real command.

**Covered child process surfaces:**
- Supervisor-managed command children
- PTY shell children
- MCP stdio server children
- OpenClaw-launched browser/Chrome processes

The wrapper is Linux-only and is skipped when `/bin/sh` is unavailable. Also skipped if child env sets `OPENCLAW_CHILD_OOM_SCORE_ADJ=0`, `false`, `no`, or `off`.

**Verify:**
```bash
cat /proc/<child-pid>/oom_score_adj
# Expected: 1000 for covered children; Gateway should keep its normal score (usually 0)
```

**Note:** This does not replace normal memory tuning. If a VPS or container repeatedly kills children, increase the memory limit, reduce concurrency, or add stronger resource controls such as systemd `MemoryMax=` or container-level memory limits.

---

## iOS

**Availability**: internal preview — NOT publicly distributed yet.

### What it Does

- Connects to a Gateway over WebSocket (LAN or tailnet)
- Exposes node capabilities: Canvas, Screen snapshot, Camera capture, Location, Talk mode, Voice wake
- Receives `node.invoke` commands and reports node status events

### Requirements

- Gateway running on another device
- Network path: same LAN via Bonjour, OR tailnet via unicast DNS-SD, OR manual host/port (fallback)

### Quick Start

1. Start the Gateway: `openclaw gateway --port 18789`
2. In the iOS app, open Settings and pick a discovered gateway (or enable Manual Host and enter host/port)
3. Approve pairing: `openclaw devices list && openclaw devices approve <requestId>`
4. Verify: `openclaw nodes status`

Optional: if the iOS node always connects from a tightly controlled subnet, opt in to first-time node auto-approval:
```json5
{
  gateway: {
    nodes: {
      pairing: {
        autoApproveCidrs: ["192.168.1.0/24"],
      },
    },
  },
}
```
Disabled by default. Applies only to fresh `role: node` pairing with no requested scopes. Operator/browser pairing and role/scope/metadata/public-key changes still require manual approval.

### Relay-Backed Push (Official Builds)

Official distributed iOS builds use an external push relay. Gateway config required:
```json5
{
  gateway: {
    push: {
      apns: {
        relay: {
          baseUrl: "https://relay.example.com",
        },
      },
    },
  },
}
```

**How it works:** The iOS app registers with the relay using App Attest and the app receipt. The relay returns an opaque relay handle plus a registration-scoped send grant. The app includes the paired gateway identity in relay registration so the relay-backed registration is delegated to that specific gateway. Another gateway cannot reuse that stored registration, even if it somehow obtains the handle.

**Compatibility note:** `OPENCLAW_APNS_RELAY_BASE_URL` still works as a temporary env override for the gateway. If the app later connects to a different gateway or a build with a different relay base URL, it refreshes the relay registration instead of reusing the old binding.

**Authentication and trust flow (hop by hop):**
1. `iOS app → gateway`: normal Gateway auth flow + device pairing; operator session is used to call `gateway.identity.get`
2. `iOS app → relay`: App Attest proof + app receipt; validates bundle ID and official/production distribution path. **This blocks local Xcode/dev builds from using the hosted relay** (a local build may be signed, but it does not satisfy the official Apple distribution proof the relay expects)
3. `Gateway identity delegation`: relay returns handle + send grant delegated to that specific gateway identity
4. `Gateway → relay`: gateway signs send request with its own device identity; relay verifies both stored send grant and gateway signature
5. `Relay → APNs`: relay owns production APNs credentials; gateway never stores the raw APNs token for relay-backed official builds

**What the gateway does NOT need for this path:**
- No deployment-wide relay token.
- No direct APNs key for official/TestFlight relay-backed sends.

**Expected operator flow:**
1. Install the official/TestFlight iOS build
2. Set `gateway.push.apns.relay.baseUrl` on the gateway
3. Pair the app to the gateway and let it finish connecting
4. The app publishes `push.apns.register` automatically after it has an APNs token, operator session is connected, and relay registration succeeds
5. After that, `push.test`, reconnect wakes, and wake nudges can use the stored relay-backed registration

**For local/manual builds without the relay:**
```bash
export OPENCLAW_APNS_TEAM_ID="TEAMID"
export OPENCLAW_APNS_KEY_ID="KEYID"
export OPENCLAW_APNS_PRIVATE_KEY_P8="$(cat /path/to/AuthKey_KEYID.p8)"
```

These are gateway-host runtime env vars. `apps/ios/fastlane/.env` only stores App Store Connect / TestFlight auth (such as `ASC_KEY_ID` and `ASC_ISSUER_ID`); it does **not** configure direct APNs delivery for local iOS builds.

**Recommended gateway-host APNs key storage:**
```bash
mkdir -p ~/.openclaw/credentials/apns
chmod 700 ~/.openclaw/credentials/apns
mv /path/to/AuthKey_KEYID.p8 ~/.openclaw/credentials/apns/AuthKey_KEYID.p8
chmod 600 ~/.openclaw/credentials/apns/AuthKey_KEYID.p8
export OPENCLAW_APNS_PRIVATE_KEY_PATH="$HOME/.openclaw/credentials/apns/AuthKey_KEYID.p8"
```

### Discovery Paths

**Bonjour (LAN)**: iOS app browses `_openclaw-gw._tcp` on `local.` AND, when configured, the same wide-area DNS-SD discovery domain. Same-LAN gateways appear automatically from `local.`; cross-network discovery can use the configured wide-area domain without changing the beacon type.

**Tailnet (cross-network)**: Use unicast DNS-SD zone (e.g., `openclaw.internal.`) and Tailscale split DNS.

**Manual host/port**: In Settings, enable **Manual Host** and enter gateway host + port (default `18789`).

### Canvas + A2UI

The iOS node renders a WKWebView canvas. Use `node.invoke` to drive it:
```bash
openclaw nodes invoke --node "iOS Node" --command canvas.navigate --params '{"url":"http://<gateway-host>:18789/__openclaw__/canvas/"}'
```

Canvas commands:
```bash
openclaw nodes invoke --node "iOS Node" --command canvas.eval --params '{"javaScript":"document.title"}'
openclaw nodes invoke --node "iOS Node" --command canvas.snapshot --params '{"maxWidth":900,"format":"jpeg"}'
```

The Gateway canvas host serves `/__openclaw__/canvas/` and `/__openclaw__/a2ui/` (same port as `gateway.port`, default `18789`).

**Auto-navigate**: The iOS node auto-navigates to A2UI on connect when a canvas host URL is advertised. Return to the built-in scaffold with `canvas.navigate` and `{"url":""}`.

### Voice Wake + Talk Mode

Available in Settings. iOS may suspend background audio — treat voice features as best-effort when the app is not active.

### Common Errors

- `NODE_BACKGROUND_UNAVAILABLE`: bring the iOS app to the foreground
- `A2UI_HOST_NOT_CONFIGURED`: the Gateway did not advertise a canvas host URL; check `canvasHost` in Gateway configuration
- Pairing prompt never appears: run `openclaw devices list` and approve manually
- Reconnect fails after reinstall: the Keychain pairing token was cleared; re-pair the node

---

## Android

> **Note**: The Android app has NOT been publicly released yet. Source code available in repo under `apps/android`. Build with Java 17 and Android SDK: `./gradlew :app:assemblePlayDebug`

### Support Snapshot

- Role: companion node app (Android does NOT host the Gateway)
- Gateway required: yes (run it on macOS, Linux, or Windows via WSL2)

### Connection Requirements

- Android connects directly to the Gateway WebSocket (`role: node`)
- For Tailscale/public hosts: requires secure endpoint (`wss://` or Tailscale Serve)
- Cleartext `ws://` supported on private LAN addresses / `.local` hosts, plus `localhost`, `127.0.0.1`, and the Android emulator bridge (`10.0.2.2`)
- **Important**: Tailnet/public mobile pairing does **not** use raw tailnet IP `ws://` endpoints — use Tailscale Serve instead

### Connection Runbook

1. **Start the Gateway**:
```bash
openclaw gateway --port 18789 --verbose
```

For remote Android access over Tailscale:
```bash
openclaw gateway --tailscale serve
```

2. **Verify discovery** (optional):
```bash
dns-sd -B _openclaw-gw._tcp local.
openclaw gateway discover --json
```

3. **Connect from Android**: In the Android app, the app keeps its gateway connection alive via a **foreground service** (persistent notification). Open the **Connect** tab and use **Setup Code** or **Manual** mode. For private LAN hosts, `ws://` still works. For Tailscale/public hosts, turn on TLS and use a `wss://` / Tailscale Serve endpoint.

4. **Approve pairing**:
```bash
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
```

Optional: if the Android node always connects from a tightly controlled subnet, opt in to first-time node auto-approval:
```json5
{
  gateway: {
    nodes: {
      pairing: {
        autoApproveCidrs: ["192.168.1.0/24"],
      },
    },
  },
}
```
Disabled by default. Applies only to fresh `role: node` pairing with no requested scopes.

After the first successful pairing, Android auto-reconnects on launch: manual endpoint (if enabled), otherwise the last discovered gateway (best-effort).

5. **Verify node connected**:
```bash
openclaw nodes status
openclaw gateway call node.list --params "{}"
```

### Tailnet Discovery (cross-network)

Android NSD/mDNS discovery won't cross networks (for example Vienna ⇄ London cross-tailnet). For cross-network via Tailscale, use Wide-Area Bonjour / unicast DNS-SD:
1. Set up a DNS-SD zone (e.g., `openclaw.internal.`) on the gateway host
2. Configure Tailscale split DNS for your chosen domain

**Note:** Discovery alone is not sufficient for tailnet/public Android pairing. The discovered route still needs a secure endpoint (`wss://` or Tailscale Serve).

Compare discovery against: `openclaw gateway discover --json` (shows `local.` plus the configured wide-area domain in one pass, uses the resolved service endpoint instead of TXT-only hints).

### Chat + History

- `chat.history` (display-normalized; inline directive tags are stripped from visible text, plain-text tool-call XML payloads (including `<tool_call>...</tool_call>`, `<function_call>...</function_call>`, `<tool_calls>...</tool_calls>`, `<function_calls>...</function_calls>`, and truncated tool-call blocks) and leaked ASCII/full-width model control tokens are stripped, pure silent-token assistant rows such as exact `NO_REPLY` / `no_reply` are omitted, and oversized rows can be replaced with placeholders)
- `chat.send`
- `chat.subscribe` → `event:"chat"` (best-effort push updates)

### Canvas + Camera

**Navigate node to Gateway Canvas Host:**
```bash
openclaw nodes invoke --node "<Android Node>" --command canvas.navigate --params '{"url":"http://<gateway-hostname>.local:18789/__openclaw__/canvas/"}'
```

Canvas commands (foreground only):
- `canvas.eval`, `canvas.snapshot`, `canvas.navigate`
- A2UI: `canvas.a2ui.push`, `canvas.a2ui.reset` (`canvas.a2ui.pushJSONL` is a legacy alias)

Camera commands (foreground only; permission-gated):
- `camera.snap` (jpg)
- `camera.clip` (mp4)

### Voice + Expanded Android Command Surface

- Voice: single mic on/off flow with transcript capture and `talk.speak` playback. Local system TTS is used only when `talk.speak` is unavailable. Voice stops when the app leaves the foreground.
- Voice wake/talk-mode toggles are currently removed from Android UX/runtime

Additional Android command families (availability depends on device + permissions):
- `device.status`, `device.info`, `device.permissions`, `device.health`
- `notifications.list`, `notifications.actions`
- `photos.latest`
- `contacts.search`, `contacts.add`
- `calendar.events`, `calendar.add`
- `callLog.search`, `sms.search`
- `motion.activity`, `motion.pedometer`

### Assistant Entrypoints

Android supports launching OpenClaw from the system assistant trigger (Google Assistant). Uses Android **App Actions** metadata declared in the app manifest — no extra gateway config needed.

### Notification Forwarding Config

```json5
{
  notifications: {
    allowPackages: ["com.slack", "com.whatsapp"],
    denyPackages: ["com.android.systemui"],
    quietHours: {
      start: "22:00",
      end: "07:00",
    },
    rateLimit: 5,
  },
}
```

| Key | Type | Description |
|---|---|---|
| `notifications.allowPackages` | string[] | Only forward notifications from these packages |
| `notifications.denyPackages` | string[] | Never forward from these packages (applied after allowPackages) |
| `notifications.quietHours.start` | string (HH:mm) | Start of quiet hours window (local device time) |
| `notifications.quietHours.end` | string (HH:mm) | End of quiet hours window |
| `notifications.rateLimit` | number | Maximum forwarded notifications per package per minute |

Notification forwarding requires the Android Notification Listener permission.

**Note:** The notification picker also uses safer behavior for forwarded notification events, preventing accidental forwarding of sensitive system notifications.

---

## VPS Hosting

### Provider Options

- **Railway**: one-click, browser setup
- **Northflank**: one-click, browser setup
- **DigitalOcean**: simple paid VPS
- **Oracle Cloud**: always Free ARM tier
- **Fly.io**: Fly Machines
- **Hetzner**: Docker on Hetzner VPS
- **Hostinger**: VPS with one-click setup
- **GCP**: Compute Engine
- **Azure**: Linux VM
- **exe.dev**: VM with HTTPS proxy
- **Raspberry Pi**: ARM self-hosted

**AWS (EC2 / Lightsail / free tier)** also works well.

### How Cloud Setups Work

- The **Gateway runs on the VPS** and owns state + workspace
- You connect from your laptop or phone via the **Control UI** or **Tailscale/SSH**
- Treat the VPS as the source of truth and **back up** the state + workspace regularly
- Secure default: keep the Gateway on loopback and access it via SSH tunnel or Tailscale Serve
- If you bind to `lan` or `tailnet`, require `gateway.auth.token` or `gateway.auth.password`

**Shared company agent on a VPS:**
Running a single agent for a team is valid when every user is in the same trust boundary and the agent is business-only. Keep it on a dedicated runtime (VPS/VM/container + dedicated OS user/accounts). Do not sign that runtime into personal Apple/Google accounts or personal browser/password-manager profiles. If users are adversarial to each other, split by gateway/host/OS user.

**Using nodes with a VPS:**
Keep the Gateway in the cloud and pair nodes on local devices (Mac/iOS/Android/headless). Nodes provide local screen/camera/canvas and `system.run` capabilities while the Gateway stays in the cloud.

### Startup Tuning for Small VMs

```bash
grep -q 'NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache' ~/.bashrc || cat >> ~/.bashrc <<'EOF'
export NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
mkdir -p /var/tmp/openclaw-compile-cache
export OPENCLAW_NO_RESPAWN=1
EOF
source ~/.bashrc
```

- `NODE_COMPILE_CACHE` improves repeated command startup times
- `OPENCLAW_NO_RESPAWN=1` avoids extra startup overhead from a self-respawn path
- First command run warms the cache; subsequent runs are faster

**systemd tuning:**
```bash
systemctl --user edit openclaw-gateway.service
```
```ini
[Service]
Environment=OPENCLAW_NO_RESPAWN=1
Environment=NODE_COMPILE_CACHE=/var/tmp/openclaw-compile-cache
Restart=always
RestartSec=2
```

The live docs also recommend `TimeoutStartSec=90` in the systemd tuning checklist and suggest preferring SSD-backed disks for state/cache paths to reduce cold-start penalties.

### Raspberry Pi

Run a persistent, always-on Gateway on a Raspberry Pi.

**Prerequisites:**
- Raspberry Pi 4 or 5, 2 GB+ RAM (4 GB recommended)
- MicroSD card (16 GB+) or USB SSD
- 64-bit Raspberry Pi OS Lite (**do NOT use 32-bit**)
- About 30 minutes

**Setup steps:**
1. Flash with Raspberry Pi Imager (64-bit OS, enable SSH, set hostname/user/WiFi)
2. Connect via SSH
3. Update: `sudo apt update && sudo apt upgrade -y && sudo apt install -y git curl build-essential`
4. Set timezone: `sudo timedatectl set-timezone America/Chicago`
5. Install Node.js 24: `curl -fsSL https://deb.nodesource.com/setup_24.x | sudo -E bash - && sudo apt install -y nodejs`
6. Add swap (for 2 GB or less):
```bash
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```
7. Install OpenClaw: `curl -fsSL https://openclaw.ai/install.sh | bash`
8. Run onboarding: `openclaw onboard --install-daemon`
9. Verify: `openclaw status && systemctl --user status openclaw-gateway.service`

**Access Control UI (from your laptop):**
```bash
ssh user@gateway-host 'openclaw dashboard --no-open'
ssh -N -L 18789:127.0.0.1:18789 user@gateway-host
```

**Performance tips:**
- **Use a USB SSD** — SD cards are slow and wear out
- Enable module compile cache (see above)
- Reduce memory: `echo 'gpu_mem=16' | sudo tee -a /boot/config.txt && sudo systemctl disable bluetooth`

**Troubleshooting:**
- Out of memory: verify swap with `free -h`, disable unused services
- Slow performance: use USB SSD, check `vcgencmd get_throttled` (should return `0x0`)
- Service won't start: `journalctl --user -u openclaw-gateway.service --no-pager -n 100`; verify lingering: `sudo loginctl enable-linger "$(whoami)"`
- ARM binary issues: verify `uname -m` shows `aarch64`
- WiFi drops: `sudo iwconfig wlan0 power off`

---

## Web UI (Control UI & Dashboard)

### Overview

The Gateway serves a small **browser Control UI** (Vite + Lit) from the same port as the Gateway WebSocket:
- Default: `http://<host>:18789/`
- Optional prefix: set `gateway.controlUi.basePath` (e.g., `/openclaw`)

### Configuration

```json5
{
  gateway: {
    controlUi: { enabled: true, basePath: "/openclaw" }, // basePath optional
  },
}
```

Control UI is **enabled by default** (`controlUi.enabled: true` in the config schema).

The Control UI fetches runtime settings from `/__openclaw/control-ui-config.json`, gated by the same gateway auth as the rest of the HTTP surface.

### Tailscale Access

**Integrated Serve (recommended):**
```json5
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "serve" },
  },
}
```
Open `https://<magicdns>/` (or your configured `gateway.controlUi.basePath`).

**Tailnet bind + token:**
```json5
{
  gateway: {
    bind: "tailnet",
    controlUi: { enabled: true },
    auth: { mode: "token", token: "your-token" },
  },
}
```

**Public internet (Funnel):**
```json5
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "funnel" },
    auth: { mode: "password" }, // or OPENCLAW_GATEWAY_PASSWORD
  },
}
```

### Security Notes

- Gateway auth is required by default (token, password, trusted-proxy, or Tailscale Serve identity headers)
- Non-loopback binds still **require** gateway auth
- For non-loopback Control UI deployments, set `gateway.controlUi.allowedOrigins` explicitly
- `gateway.controlUi.dangerouslyAllowHostHeaderOriginFallback=true` is a dangerous security downgrade
- **Browser-origin WS auth attempts are always throttled with loopback exemption disabled** (defense-in-depth against browser-based localhost brute force); repeated failures from the same normalized `Origin` are locked out temporarily in their own bucket

### Building the UI

```bash
pnpm ui:build
```

Static files served from `dist/control-ui`.

### Dashboard

Quick open (local Gateway): `http://127.0.0.1:18789/` or `http://localhost:18789/`

Open from CLI:
```bash
openclaw dashboard
```

**Authentication** is enforced at the WebSocket handshake via:
- `connect.params.auth.token`
- `connect.params.auth.password`
- Tailscale Serve identity headers when `gateway.auth.allowTailscale: true`
- trusted-proxy identity headers when `gateway.auth.mode: "trusted-proxy"`

**If you see "unauthorized" / 1008:**
- Ensure the gateway is reachable
- For `AUTH_TOKEN_MISMATCH`, clients may do one trusted retry with a cached device token
- Retrieve or supply the shared secret: `openclaw config get gateway.auth.token`
- In the dashboard settings, paste the token or password into the auth field

**Shared-secret token source**: `gateway.auth.token` (or `OPENCLAW_GATEWAY_TOKEN`). `openclaw dashboard` can pass it via URL fragment for one-time bootstrap.

**Device pairing (first connection)**: Even if you're on the same Tailnet, a one-time pairing approval is required.

```bash
openclaw devices list
openclaw devices approve <requestId>
```

Direct local loopback browser connections (`127.0.0.1` / `localhost`) are auto-approved. Each browser profile generates a unique device ID.

If the browser is already paired and you change it from read access to write/admin access, this is treated as an approval upgrade, not a silent reconnect — OpenClaw keeps the old approval active, blocks the broader reconnect, and asks you to approve the new scope set explicitly.

**Personal identity (browser-local):** The Control UI supports a per-browser personal identity (display name and avatar) attached to outgoing messages for attribution in shared sessions. It lives in browser storage, is scoped to the current browser profile, and is not synced to other devices or persisted server-side beyond transcript authorship metadata.

### Control UI Capabilities

- Chat with the model via Gateway WS (`chat.history`, `chat.send`, `chat.abort`, `chat.inject`)
- Talk to OpenAI Realtime directly from the browser via WebRTC
- Stream tool calls + live tool output cards in Chat
- Channels: status, QR login, per-channel config
- Sessions: list + per-session model/thinking/fast/verbose/trace/reasoning overrides
- Dreams: dreaming status, enable/disable, Dream Diary reader
- Cron jobs: list/add/edit/run/enable/disable + run history
- Skills: status, enable/disable, install, API key updates
- Nodes: list + caps
- Exec approvals: edit gateway or node allowlists + ask policy
- Config: view/edit `~/.openclaw/openclaw.json` with `config.get`/`config.set`/`config.apply` + restart with validation. Config writes include a base-hash guard to prevent clobbering concurrent edits. Config writes also preflight active SecretRef resolution — unresolved active submitted refs are rejected before write. Config schema + form rendering via `config.schema`/`config.schema.lookup`. Raw JSON editor available only when the snapshot can safely round-trip
- Debug: status/health/models snapshots + event log + manual RPC calls
- Logs: live tail of gateway file logs with filter/export
- Update: run a package/git update + restart with a restart report

**Language support**: `en`, `zh-CN`, `zh-TW`, `pt-BR`, `de`, `es`, `ja-JP`, `ko`, `fr`, `tr`, `uk`, `id`, `pl`, `th`

**Locale picker**: Overview → Gateway Access → Language (NOT under Appearance)

**Chat behavior:**
- `chat.send` is **non-blocking**: acks immediately with `{ runId, status: "started" }`, response streams via `chat` events
- Re-sending with the same `idempotencyKey` returns `{ status: "in_flight" }` while running, and `{ status: "ok" }` after completion
- Aborted partial assistant text persists into transcript history when buffered output exists, marked with abort metadata
- During an active send and the final history refresh, the chat view keeps local optimistic user/assistant messages visible if `chat.history` briefly returns an older snapshot; the canonical transcript replaces those once the Gateway history catches up
- `chat.inject` appends an assistant note to the session transcript and broadcasts a `chat` event for UI-only updates (no agent run, no channel delivery)
- The chat header model and thinking pickers patch the active session immediately through `sessions.patch` (persistent session overrides, not one-turn-only)
- When fresh Gateway session usage reports show high context pressure, the chat composer shows a context notice and compact button
- Talk mode uses a registered realtime voice provider (browser WebRTC). The Gateway mints a short-lived Realtime client secret with `talk.realtime.session`; the browser sends microphone audio directly to OpenAI and relays `openclaw_agent_consult` tool calls back through `chat.send`. The browser never receives the standard OpenAI API key

**Hosted embeds**: `gateway.controlUi.embedSandbox`:
- `strict`: disables script execution inside hosted embeds
- `scripts`: allows interactive embeds (default)
- `trusted`: adds `allow-same-origin` on top of `allow-scripts`

**Content Security Policy**: Only same-origin assets and `data:` URLs are allowed for images. Remote avatar URLs from channel metadata are replaced with the built-in logo/badge.

**Control UI over plain HTTP:**
- Needs `gateway.controlUi.allowInsecureAuth=true` for localhost in non-secure HTTP contexts
- `dangerouslyDisableDeviceAuth=true` disables device identity checks entirely (severe security downgrade)

### WebChat

The macOS/iOS SwiftUI chat UI talks directly to the Gateway WebSocket.

**Behavior:**
- Uses the same sessions and routing rules as other channels
- Deterministic routing: replies always go back to WebChat
- `chat.history` is bounded for stability (Gateway may truncate long text fields, omit heavy metadata, and replace oversized entries with `[chat.history omitted: message too large]`)
- `chat.history` is also display-normalized: strips runtime-only OpenClaw context, inbound envelope wrappers, inline delivery directive tags, plain-text tool-call XML payloads, leaked control tokens; omits assistant entries whose whole visible text is only `NO_REPLY`/`no_reply`
- `chat.inject` appends an assistant note directly to the transcript and broadcasts it to the UI (no agent run)
- Gateway persists aborted partial assistant text into transcript history when buffered output exists, marked with abort metadata
- History is always fetched from the gateway (no local file watching)
- If the gateway is unreachable, WebChat is read-only

**Configuration:**
- `gateway.webchat.chatHistoryMaxChars`: maximum character count for text fields in `chat.history` responses. Per-request `maxChars` can also be sent by the client to override this default for a single `chat.history` call

**Control UI agents tools panel:**
- **Available Right Now**: uses `tools.effective(sessionKey=...)` — shows what the current session can actually use at runtime, including core, plugin, and channel-owned tools
- **Tool Configuration**: uses `tools.catalog` — focused on profiles, overrides, and catalog semantics
- Runtime availability is session-scoped. Switching sessions on the same agent can change the **Available Right Now** list
- The config editor does not imply runtime availability; effective access still follows policy precedence (`allow`/`deny`, per-agent and provider/channel overrides)

**Dev server + remote Gateway:**
```text
http://localhost:5173/?gatewayUrl=ws://<gateway-host>:18789
```

Optional one-time auth:
```text
http://localhost:5173/?gatewayUrl=wss://<gateway-host>:18789#token=<gateway-token>
```
