# Gateway Runbook

Source: https://docs.openclaw.ai/gateway

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationGatewayGateway RunbookGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpGateway
Gateway RunbookConfiguration and operationsSecurity and sandboxingProtocols and APIsNetworking and discovery
Remote access
Remote AccessRemote Gateway SetupTailscale
Security
Formal Verification (Security Models)
Web interfaces
WebControl UIDashboardWebChatTUI
On this page
- [Gateway runbook](#gateway-runbook)
- [5-minute local startup](#5-minute-local-startup)
- [Runtime model](#runtime-model)
- [Port and bind precedence](#port-and-bind-precedence)
- [Hot reload modes](#hot-reload-modes)
- [Operator command set](#operator-command-set)
- [Remote access](#remote-access)
- [Supervision and service lifecycle](#supervision-and-service-lifecycle)
- [Multiple gateways on one host](#multiple-gateways-on-one-host)
- [Dev profile quick path](#dev-profile-quick-path)
- [Protocol quick reference (operator view)](#protocol-quick-reference-operator-view)
- [Operational checks](#operational-checks)
- [Liveness](#liveness)
- [Readiness](#readiness)
- [Gap recovery](#gap-recovery)
- [Common failure signatures](#common-failure-signatures)
- [Safety guarantees](#safety-guarantees)

​Gateway runbook
Use this page for day-1 startup and day-2 operations of the Gateway service.
## Deep troubleshooting

Symptom-first diagnostics with exact command ladders and log signatures.## Configuration

Task-oriented setup guide + full configuration reference.
​5-minute local startup
1Start the Gateway

Copy```
openclaw gateway --port 18789
# debug/trace mirrored to stdio
openclaw gateway --port 18789 --verbose
# force-kill listener on selected port, then start
openclaw gateway --force

```

2Verify service health

Copy```
openclaw gateway status
openclaw status
openclaw logs --follow

```

Healthy baseline: `Runtime: running` and `RPC probe: ok`.3Validate channel readiness

Copy```
openclaw channels status --probe

```

Gateway config reload watches the active config file path (resolved from profile/state defaults, or `OPENCLAW_CONFIG_PATH` when set).
Default mode is `gateway.reload.mode="hybrid"`.
​Runtime model

- One always-on process for routing, control plane, and channel connections.

Single multiplexed port for:

- WebSocket control/RPC

- HTTP APIs (OpenAI-compatible, Responses, tools invoke)

- Control UI and hooks

- Default bind mode: `loopback`.

- Auth is required by default (`gateway.auth.token` / `gateway.auth.password`, or `OPENCLAW_GATEWAY_TOKEN` / `OPENCLAW_GATEWAY_PASSWORD`).

​Port and bind precedence
SettingResolution orderGateway port`--port` → `OPENCLAW_GATEWAY_PORT` → `gateway.port` → `18789`Bind modeCLI/override → `gateway.bind` → `loopback`
​Hot reload modes
`gateway.reload.mode`Behavior`off`No config reload`hot`Apply only hot-safe changes`restart`Restart on reload-required changes`hybrid` (default)Hot-apply when safe, restart when required
​Operator command set
Copy```
openclaw gateway status
openclaw gateway status --deep
openclaw gateway status --json
openclaw gateway install
openclaw gateway restart
openclaw gateway stop
openclaw logs --follow
openclaw doctor

```

​Remote access
Preferred: Tailscale/VPN.
Fallback: SSH tunnel.
Copy```
ssh -N -L 18789:127.0.0.1:18789 user@host

```

Then connect clients to `ws://127.0.0.1:18789` locally.
If gateway auth is configured, clients still must send auth (`token`/`password`) even over SSH tunnels.
See: [Remote Gateway](/gateway/remote), [Authentication](/gateway/authentication), [Tailscale](/gateway/tailscale).
​Supervision and service lifecycle
Use supervised runs for production-like reliability.

 macOS (launchd) Linux (systemd user) Linux (system service)
Copy```
openclaw gateway install
openclaw gateway status
openclaw gateway restart
openclaw gateway stop

```

LaunchAgent labels are `ai.openclaw.gateway` (default) or `ai.openclaw.<profile>` (named profile). `openclaw doctor` audits and repairs service config drift.Copy```
openclaw gateway install
systemctl --user enable --now openclaw-gateway[-<profile>].service
openclaw gateway status

```

For persistence after logout, enable lingering:Copy```
sudo loginctl enable-linger <user>

```

Use a system unit for multi-user/always-on hosts.Copy```
sudo systemctl daemon-reload
sudo systemctl enable --now openclaw-gateway[-<profile>].service

```

​Multiple gateways on one host
Most setups should run **one** Gateway.
Use multiple only for strict isolation/redundancy (for example a rescue profile).
Checklist per instance:

- Unique `gateway.port`

- Unique `OPENCLAW_CONFIG_PATH`

- Unique `OPENCLAW_STATE_DIR`

- Unique `agents.defaults.workspace`

Example:
Copy```
OPENCLAW_CONFIG_PATH=~/.openclaw/a.json OPENCLAW_STATE_DIR=~/.openclaw-a openclaw gateway --port 19001
OPENCLAW_CONFIG_PATH=~/.openclaw/b.json OPENCLAW_STATE_DIR=~/.openclaw-b openclaw gateway --port 19002

```

See: [Multiple gateways](/gateway/multiple-gateways).
​Dev profile quick path
Copy```
openclaw --dev setup
openclaw --dev gateway --allow-unconfigured
openclaw --dev status

```

Defaults include isolated state/config and base gateway port `19001`.
​Protocol quick reference (operator view)

- First client frame must be `connect`.

- Gateway returns `hello-ok` snapshot (`presence`, `health`, `stateVersion`, `uptimeMs`, limits/policy).

- Requests: `req(method, params)` → `res(ok/payload|error)`.

- Common events: `connect.challenge`, `agent`, `chat`, `presence`, `tick`, `health`, `heartbeat`, `shutdown`.

Agent runs are two-stage:

- Immediate accepted ack (`status:"accepted"`)

- Final completion response (`status:"ok"|"error"`), with streamed `agent` events in between.

See full protocol docs: [Gateway Protocol](/gateway/protocol).
​Operational checks
​Liveness

- Open WS and send `connect`.

- Expect `hello-ok` response with snapshot.

​Readiness
Copy```
openclaw gateway status
openclaw channels status --probe
openclaw health

```

​Gap recovery
Events are not replayed. On sequence gaps, refresh state (`health`, `system-presence`) before continuing.
​Common failure signatures
SignatureLikely issue`refusing to bind gateway ... without auth`Non-loopback bind without token/password`another gateway instance is already listening` / `EADDRINUSE`Port conflict`Gateway start blocked: set gateway.mode=local`Config set to remote mode`unauthorized` during connectAuth mismatch between client and gateway
For full diagnosis ladders, use [Gateway Troubleshooting](/gateway/troubleshooting).
​Safety guarantees

- Gateway protocol clients fail fast when Gateway is unavailable (no implicit direct-channel fallback).

- Invalid/non-connect first frames are rejected and closed.

- Graceful shutdown emits `shutdown` event before socket close.

Related:

- [Troubleshooting](/gateway/troubleshooting)

- [Background Process](/gateway/background-process)

- [Configuration](/gateway/configuration)

- [Health](/gateway/health)

- [Doctor](/gateway/doctor)

- [Authentication](/gateway/authentication)

Configuration⌘I