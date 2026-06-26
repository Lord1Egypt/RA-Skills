# Web

Source: https://docs.openclaw.ai/web

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationWeb interfacesWebGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpGateway
Gateway RunbookConfiguration and operationsSecurity and sandboxingProtocols and APIsNetworking and discovery
Remote access
Remote AccessRemote Gateway SetupTailscale
Security
Formal Verification (Security Models)
Web interfaces
WebControl UIDashboardWebChatTUI
On this page
- [Web (Gateway)](#web-gateway)
- [Webhooks](#webhooks)
- [Config (default-on)](#config-default-on)
- [Tailscale access](#tailscale-access)
- [Integrated Serve (recommended)](#integrated-serve-recommended)
- [Tailnet bind + token](#tailnet-bind-%2B-token)
- [Public internet (Funnel)](#public-internet-funnel)
- [Security notes](#security-notes)
- [Building the UI](#building-the-ui)

​Web (Gateway)
The Gateway serves a small **browser Control UI** (Vite + Lit) from the same port as the Gateway WebSocket:

- default: `http://<host>:18789/`

- optional prefix: set `gateway.controlUi.basePath` (e.g. `/openclaw`)

Capabilities live in [Control UI](/web/control-ui).
This page focuses on bind modes, security, and web-facing surfaces.
​Webhooks
When `hooks.enabled=true`, the Gateway also exposes a small webhook endpoint on the same HTTP server.
See [Gateway configuration](/gateway/configuration) → `hooks` for auth + payloads.
​Config (default-on)
The Control UI is **enabled by default** when assets are present (`dist/control-ui`).
You can control it via config:
Copy```
{
  gateway: {
    controlUi: { enabled: true, basePath: "/openclaw" }, // basePath optional
  },
}

```

​Tailscale access
​Integrated Serve (recommended)
Keep the Gateway on loopback and let Tailscale Serve proxy it:
Copy```
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "serve" },
  },
}

```

Then start the gateway:
Copy```
openclaw gateway

```

Open:

- `https://<magicdns>/` (or your configured `gateway.controlUi.basePath`)

​Tailnet bind + token
Copy```
{
  gateway: {
    bind: "tailnet",
    controlUi: { enabled: true },
    auth: { mode: "token", token: "your-token" },
  },
}

```

Then start the gateway (token required for non-loopback binds):
Copy```
openclaw gateway

```

Open:

- `http://<tailscale-ip>:18789/` (or your configured `gateway.controlUi.basePath`)

​Public internet (Funnel)
Copy```
{
  gateway: {
    bind: "loopback",
    tailscale: { mode: "funnel" },
    auth: { mode: "password" }, // or OPENCLAW_GATEWAY_PASSWORD
  },
}

```

​Security notes

- Gateway auth is required by default (token/password or Tailscale identity headers).

- Non-loopback binds still **require** a shared token/password (`gateway.auth` or env).

- The wizard generates a gateway token by default (even on loopback).

- The UI sends `connect.params.auth.token` or `connect.params.auth.password`.

- The Control UI sends anti-clickjacking headers and only accepts same-origin browser
websocket connections unless `gateway.controlUi.allowedOrigins` is set.

- With Serve, Tailscale identity headers can satisfy auth when
`gateway.auth.allowTailscale` is `true` (no token/password required). Set
`gateway.auth.allowTailscale: false` to require explicit credentials. See
[Tailscale](/gateway/tailscale) and [Security](/gateway/security).

- `gateway.tailscale.mode: "funnel"` requires `gateway.auth.mode: "password"` (shared password).

​Building the UI
The Gateway serves static files from `dist/control-ui`. Build them with:
Copy```
pnpm ui:build # auto-installs UI deps on first run

```

Formal Verification (Security Models)Control UI⌘I