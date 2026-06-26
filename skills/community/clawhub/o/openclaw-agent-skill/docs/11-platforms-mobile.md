# Platforms - Mobile (iOS/Android)

> This file contains verbatim documentation from docs.openclaw.ai
> Total pages in this section: 2

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/ios -->

# iOS App - OpenClaw

## iOS App (Node)

Availability: internal preview. The iOS app is not publicly distributed yet.

## What it does

*   Connects to a Gateway over WebSocket (LAN or tailnet).
*   Exposes node capabilities: Canvas, Screen snapshot, Camera capture, Location, Talk mode, Voice wake.
*   Receives `node.invoke` commands and reports node status events.

## Requirements

*   Gateway running on another device (macOS, Linux, or Windows via WSL2).
*   Network path:
    *   Same LAN via Bonjour, **or**
    *   Tailnet via unicast DNS-SD (example domain: `openclaw.internal.`), **or**
    *   Manual host/port (fallback).

## Quick start (pair + connect)

1.  Start the Gateway:

```
openclaw gateway --port 18789
```

2.  In the iOS app, open Settings and pick a discovered gateway (or enable Manual Host and enter host/port).
3.  Approve the pairing request on the gateway host:

```
openclaw devices list
openclaw devices approve <requestId>
```

4.  Verify connection:

```
openclaw nodes status
openclaw gateway call node.list --params "{}"
```

## Discovery paths

### Bonjour (LAN)

The Gateway advertises `_openclaw-gw._tcp` on `local.`. The iOS app lists these automatically.

### Tailnet (cross-network)

If mDNS is blocked, use a unicast DNS-SD zone (choose a domain; example: `openclaw.internal.`) and Tailscale split DNS. See [Bonjour](https://docs.openclaw.ai/gateway/bonjour) for the CoreDNS example.

### Manual host/port

In Settings, enable **Manual Host** and enter the gateway host + port (default `18789`).

## Canvas + A2UI

The iOS node renders a WKWebView canvas. Use `node.invoke` to drive it:

```
openclaw nodes invoke --node "iOS Node" --command canvas.navigate --params '{"url":"http://<gateway-host>:18789/__openclaw__/canvas/"}'
```

Notes:

*   The Gateway canvas host serves `/__openclaw__/canvas/` and `/__openclaw__/a2ui/`.
*   It is served from the Gateway HTTP server (same port as `gateway.port`, default `18789`).
*   The iOS node auto-navigates to A2UI on connect when a canvas host URL is advertised.
*   Return to the built-in scaffold with `canvas.navigate` and `{"url":""}`.

### Canvas eval / snapshot

```
openclaw nodes invoke --node "iOS Node" --command canvas.eval --params '{"javaScript":"(() => { const {ctx} = window.__openclaw; ctx.clearRect(0,0,innerWidth,innerHeight); ctx.lineWidth=6; ctx.strokeStyle=\"#ff2d55\"; ctx.beginPath(); ctx.moveTo(40,40); ctx.lineTo(innerWidth-40, innerHeight-40); ctx.stroke(); return \"ok\"; })()"}'
```

```
openclaw nodes invoke --node "iOS Node" --command canvas.snapshot --params '{"maxWidth":900,"format":"jpeg"}'
```

## Voice wake + talk mode

*   Voice wake and talk mode are available in Settings.
*   iOS may suspend background audio; treat voice features as best-effort when the app is not active.

## Common errors

*   `NODE_BACKGROUND_UNAVAILABLE`: bring the iOS app to the foreground (canvas/camera/screen commands require it).
*   `A2UI_HOST_NOT_CONFIGURED`: the Gateway did not advertise a canvas host URL; check `canvasHost` in [Gateway configuration](https://docs.openclaw.ai/gateway/configuration).
*   Pairing prompt never appears: run `openclaw devices list` and approve manually.
*   Reconnect fails after reinstall: the Keychain pairing token was cleared; re-pair the node.

*   [Pairing](https://docs.openclaw.ai/channels/pairing)
*   [Discovery](https://docs.openclaw.ai/gateway/discovery)
*   [Bonjour](https://docs.openclaw.ai/gateway/bonjour)

---

<!-- SOURCE: https://docs.openclaw.ai/platforms/android -->

# Android App - OpenClaw

## Android App (Node)

## Support snapshot

*   Role: companion node app (Android does not host the Gateway).
*   Gateway required: yes (run it on macOS, Linux, or Windows via WSL2).
*   Install: [Getting Started](https://docs.openclaw.ai/start/getting-started) + [Pairing](https://docs.openclaw.ai/channels/pairing).
*   Gateway: [Runbook](https://docs.openclaw.ai/gateway) + [Configuration](https://docs.openclaw.ai/gateway/configuration).
    *   Protocols: [Gateway protocol](https://docs.openclaw.ai/gateway/protocol) (nodes + control plane).

## System control

System control (launchd/systemd) lives on the Gateway host. See [Gateway](https://docs.openclaw.ai/gateway).

## Connection Runbook

Android node app ⇄ (mDNS/NSD + WebSocket) ⇄ **Gateway** Android connects directly to the Gateway WebSocket (default `ws://<host>:18789`) and uses device pairing (`role: node`).

### Prerequisites

*   You can run the Gateway on the “master” machine.
*   Android device/emulator can reach the gateway WebSocket:
    *   Same LAN with mDNS/NSD, **or**
    *   Same Tailscale tailnet using Wide-Area Bonjour / unicast DNS-SD (see below), **or**
    *   Manual gateway host/port (fallback)
*   You can run the CLI (`openclaw`) on the gateway machine (or via SSH).

### 1) Start the Gateway

```
openclaw gateway --port 18789 --verbose
```

Confirm in logs you see something like:

*   `listening on ws://0.0.0.0:18789`

For tailnet-only setups (recommended for Vienna ⇄ London), bind the gateway to the tailnet IP:

*   Set `gateway.bind: "tailnet"` in `~/.openclaw/openclaw.json` on the gateway host.
*   Restart the Gateway / macOS menubar app.

### 2) Verify discovery (optional)

From the gateway machine:

```
dns-sd -B _openclaw-gw._tcp local.
```

More debugging notes: [Bonjour](https://docs.openclaw.ai/gateway/bonjour).

#### Tailnet (Vienna ⇄ London) discovery via unicast DNS-SD

Android NSD/mDNS discovery won’t cross networks. If your Android node and the gateway are on different networks but connected via Tailscale, use Wide-Area Bonjour / unicast DNS-SD instead:

1.  Set up a DNS-SD zone (example `openclaw.internal.`) on the gateway host and publish `_openclaw-gw._tcp` records.
2.  Configure Tailscale split DNS for your chosen domain pointing at that DNS server.

Details and example CoreDNS config: [Bonjour](https://docs.openclaw.ai/gateway/bonjour).

### 3) Connect from Android

In the Android app:

*   The app keeps its gateway connection alive via a **foreground service** (persistent notification).
*   Open the **Connect** tab.
*   Use **Setup Code** or **Manual** mode.
*   If discovery is blocked, use manual host/port (and TLS/token/password when required) in **Advanced controls**.

After the first successful pairing, Android auto-reconnects on launch:

*   Manual endpoint (if enabled), otherwise
*   The last discovered gateway (best-effort).

### 4) Approve pairing (CLI)

On the gateway machine:

```
openclaw devices list
openclaw devices approve <requestId>
openclaw devices reject <requestId>
```

Pairing details: [Pairing](https://docs.openclaw.ai/channels/pairing).

### 5) Verify the node is connected

*   Via nodes status:
*   Via Gateway:
    
    ```
    openclaw gateway call node.list --params "{}"
    ```
    

### 6) Chat + history

The Android Chat tab supports session selection (default `main`, plus other existing sessions):

*   History: `chat.history`
*   Send: `chat.send`
*   Push updates (best-effort): `chat.subscribe` → `event:"chat"`

### 7) Canvas + camera

#### Gateway Canvas Host (recommended for web content)

If you want the node to show real HTML/CSS/JS that the agent can edit on disk, point the node at the Gateway canvas host. Note: nodes load canvas from the Gateway HTTP server (same port as `gateway.port`, default `18789`).

1.  Create `~/.openclaw/workspace/canvas/index.html` on the gateway host.
2.  Navigate the node to it (LAN):

```
openclaw nodes invoke --node "<Android Node>" --command canvas.navigate --params '{"url":"http://<gateway-hostname>.local:18789/__openclaw__/canvas/"}'
```

Tailnet (optional): if both devices are on Tailscale, use a MagicDNS name or tailnet IP instead of `.local`, e.g. `http://<gateway-magicdns>:18789/__openclaw__/canvas/`. This server injects a live-reload client into HTML and reloads on file changes. The A2UI host lives at `http://<gateway-host>:18789/__openclaw__/a2ui/`. Canvas commands (foreground only):

*   `canvas.eval`, `canvas.snapshot`, `canvas.navigate` (use `{"url":""}` or `{"url":"/"}` to return to the default scaffold). `canvas.snapshot` returns `{ format, base64 }` (default `format="jpeg"`).
*   A2UI: `canvas.a2ui.push`, `canvas.a2ui.reset` (`canvas.a2ui.pushJSONL` legacy alias)

Camera commands (foreground only; permission-gated):

*   `camera.snap` (jpg)
*   `camera.clip` (mp4)

See [Camera node](https://docs.openclaw.ai/nodes/camera) for parameters and CLI helpers.

### 8) Voice + expanded Android command surface

*   Voice: Android uses a single mic on/off flow in the Voice tab with transcript capture and TTS playback (ElevenLabs when configured, system TTS fallback). Voice stops when the app leaves the foreground.
*   Voice wake/talk-mode toggles are currently removed from Android UX/runtime.
*   Additional Android command families (availability depends on device + permissions):
    *   `device.status`, `device.info`, `device.permissions`, `device.health`
    *   `notifications.list`, `notifications.actions`
    *   `photos.latest`
    *   `contacts.search`, `contacts.add`
    *   `calendar.events`, `calendar.add`
    *   `motion.activity`, `motion.pedometer`

