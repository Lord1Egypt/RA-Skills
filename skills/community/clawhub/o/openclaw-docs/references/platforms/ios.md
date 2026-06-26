# iOS App

Source: https://docs.openclaw.ai/platforms/ios

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationPlatforms overviewiOS AppGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpPlatforms overview
PlatformsmacOS AppLinux AppWindows (WSL2)Android AppiOS App
macOS companion app
macOS Dev SetupMenu BarVoice WakeVoice OverlayWebChatCanvasGateway LifecycleHealth ChecksMenu Bar IconmacOS LoggingmacOS PermissionsRemote ControlmacOS SigningmacOS ReleaseGateway on macOSmacOS IPCSkillsPeekaboo Bridge
On this page
- [iOS App (Node)](#ios-app-node)
- [What it does](#what-it-does)
- [Requirements](#requirements)
- [Quick start (pair + connect)](#quick-start-pair-%2B-connect)
- [Discovery paths](#discovery-paths)
- [Bonjour (LAN)](#bonjour-lan)
- [Tailnet (cross-network)](#tailnet-cross-network)
- [Manual host/port](#manual-host%2Fport)
- [Canvas + A2UI](#canvas-%2B-a2ui)
- [Canvas eval / snapshot](#canvas-eval-%2F-snapshot)
- [Voice wake + talk mode](#voice-wake-%2B-talk-mode)
- [Common errors](#common-errors)
- [Related docs](#related-docs)

​iOS App (Node)
Availability: internal preview. The iOS app is not publicly distributed yet.
​What it does

- Connects to a Gateway over WebSocket (LAN or tailnet).

- Exposes node capabilities: Canvas, Screen snapshot, Camera capture, Location, Talk mode, Voice wake.

- Receives `node.invoke` commands and reports node status events.

​Requirements

- Gateway running on another device (macOS, Linux, or Windows via WSL2).

Network path:

- Same LAN via Bonjour, **or**

- Tailnet via unicast DNS-SD (example domain: `openclaw.internal.`), **or**

- Manual host/port (fallback).

​Quick start (pair + connect)

- Start the Gateway:

Copy```
openclaw gateway --port 18789

```

In the iOS app, open Settings and pick a discovered gateway (or enable Manual Host and enter host/port).

Approve the pairing request on the gateway host:

Copy```
openclaw nodes pending
openclaw nodes approve <requestId>

```

- Verify connection:

Copy```
openclaw nodes status
openclaw gateway call node.list --params "{}"

```

​Discovery paths
​Bonjour (LAN)
The Gateway advertises `_openclaw-gw._tcp` on `local.`. The iOS app lists these automatically.
​Tailnet (cross-network)
If mDNS is blocked, use a unicast DNS-SD zone (choose a domain; example: `openclaw.internal.`) and Tailscale split DNS.
See [Bonjour](/gateway/bonjour) for the CoreDNS example.
​Manual host/port
In Settings, enable **Manual Host** and enter the gateway host + port (default `18789`).
​Canvas + A2UI
The iOS node renders a WKWebView canvas. Use `node.invoke` to drive it:
Copy```
openclaw nodes invoke --node "iOS Node" --command canvas.navigate --params &#x27;{"url":"http://<gateway-host>:18789/__openclaw__/canvas/"}&#x27;

```

Notes:

- The Gateway canvas host serves `/__openclaw__/canvas/` and `/__openclaw__/a2ui/`.

- It is served from the Gateway HTTP server (same port as `gateway.port`, default `18789`).

- The iOS node auto-navigates to A2UI on connect when a canvas host URL is advertised.

- Return to the built-in scaffold with `canvas.navigate` and `{"url":""}`.

​Canvas eval / snapshot
Copy```
openclaw nodes invoke --node "iOS Node" --command canvas.eval --params &#x27;{"javaScript":"(() => { const {ctx} = window.__openclaw; ctx.clearRect(0,0,innerWidth,innerHeight); ctx.lineWidth=6; ctx.strokeStyle=\"#ff2d55\"; ctx.beginPath(); ctx.moveTo(40,40); ctx.lineTo(innerWidth-40, innerHeight-40); ctx.stroke(); return \"ok\"; })()"}&#x27;

```

Copy```
openclaw nodes invoke --node "iOS Node" --command canvas.snapshot --params &#x27;{"maxWidth":900,"format":"jpeg"}&#x27;

```

​Voice wake + talk mode

- Voice wake and talk mode are available in Settings.

- iOS may suspend background audio; treat voice features as best-effort when the app is not active.

​Common errors

- `NODE_BACKGROUND_UNAVAILABLE`: bring the iOS app to the foreground (canvas/camera/screen commands require it).

- `A2UI_HOST_NOT_CONFIGURED`: the Gateway did not advertise a canvas host URL; check `canvasHost` in [Gateway configuration](/gateway/configuration).

- Pairing prompt never appears: run `openclaw nodes pending` and approve manually.

- Reconnect fails after reinstall: the Keychain pairing token was cleared; re-pair the node.

​Related docs

- [Pairing](/gateway/pairing)

- [Discovery](/gateway/discovery)

- [Bonjour](/gateway/bonjour)

Android AppmacOS Dev Setup⌘I