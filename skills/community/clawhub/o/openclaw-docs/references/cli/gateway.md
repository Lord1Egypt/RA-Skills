# gateway

Source: https://docs.openclaw.ai/cli/gateway

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationCLI commandsgatewayGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpCLI commands
CLI ReferenceagentagentsapprovalsbrowserchannelsconfigurecrondashboarddirectorydnsdocsdoctorgatewayhealthhookslogsmemorymessagemodelsnodesonboardpairingpluginsresetSandbox CLIsecuritysessionssetupskillsstatussystemtuiuninstallupdatevoicecall
RPC and API
RPC AdaptersDevice Model Database
Templates
Default AGENTS.mdAGENTS.md TemplateBOOT.md TemplateBOOTSTRAP.md TemplateHEARTBEAT.md TemplateIDENTITYSOUL.md TemplateTOOLS.md TemplateUSER
Technical reference
Wizard ReferenceToken Use and CostsgrammY
Concept internals
TypeBoxMarkdown FormattingTyping IndicatorsUsage TrackingTimezones
Project
Credits
Release notes
Release ChecklistTests
Experiments
Onboarding and Config ProtocolCron Add HardeningTelegram Allowlist HardeningWorkspace Memory ResearchModel Config Exploration
On this page
- [Gateway CLI](#gateway-cli)
- [Run the Gateway](#run-the-gateway)
- [Options](#options)
- [Query a running Gateway](#query-a-running-gateway)
- [gateway health](#gateway-health)
- [gateway status](#gateway-status)
- [gateway probe](#gateway-probe)
- [Remote over SSH (Mac app parity)](#remote-over-ssh-mac-app-parity)
- [gateway call <method>](#gateway-call-%3Cmethod%3E)
- [Manage the Gateway service](#manage-the-gateway-service)
- [Discover gateways (Bonjour)](#discover-gateways-bonjour)
- [gateway discover](#gateway-discover)

​Gateway CLI
The Gateway is OpenClaw’s WebSocket server (channels, nodes, sessions, hooks).
Subcommands in this page live under `openclaw gateway …`.
Related docs:

- [/gateway/bonjour](/gateway/bonjour)

- [/gateway/discovery](/gateway/discovery)

- [/gateway/configuration](/gateway/configuration)

​Run the Gateway
Run a local Gateway process:
Copy```
openclaw gateway

```

Foreground alias:
Copy```
openclaw gateway run

```

Notes:

- By default, the Gateway refuses to start unless `gateway.mode=local` is set in `~/.openclaw/openclaw.json`. Use `--allow-unconfigured` for ad-hoc/dev runs.

- Binding beyond loopback without auth is blocked (safety guardrail).

- `SIGUSR1` triggers an in-process restart when authorized (enable `commands.restart` or use the gateway tool/config apply/update).

- `SIGINT`/`SIGTERM` handlers stop the gateway process, but they don’t restore any custom terminal state. If you wrap the CLI with a TUI or raw-mode input, restore the terminal before exit.

​Options

- `--port <port>`: WebSocket port (default comes from config/env; usually `18789`).

- `--bind <loopback|lan|tailnet|auto|custom>`: listener bind mode.

- `--auth <token|password>`: auth mode override.

- `--token <token>`: token override (also sets `OPENCLAW_GATEWAY_TOKEN` for the process).

- `--password <password>`: password override (also sets `OPENCLAW_GATEWAY_PASSWORD` for the process).

- `--tailscale <off|serve|funnel>`: expose the Gateway via Tailscale.

- `--tailscale-reset-on-exit`: reset Tailscale serve/funnel config on shutdown.

- `--allow-unconfigured`: allow gateway start without `gateway.mode=local` in config.

- `--dev`: create a dev config + workspace if missing (skips BOOTSTRAP.md).

- `--reset`: reset dev config + credentials + sessions + workspace (requires `--dev`).

- `--force`: kill any existing listener on the selected port before starting.

- `--verbose`: verbose logs.

- `--claude-cli-logs`: only show claude-cli logs in the console (and enable its stdout/stderr).

- `--ws-log <auto|full|compact>`: websocket log style (default `auto`).

- `--compact`: alias for `--ws-log compact`.

- `--raw-stream`: log raw model stream events to jsonl.

- `--raw-stream-path <path>`: raw stream jsonl path.

​Query a running Gateway
All query commands use WebSocket RPC.
Output modes:

- Default: human-readable (colored in TTY).

- `--json`: machine-readable JSON (no styling/spinner).

- `--no-color` (or `NO_COLOR=1`): disable ANSI while keeping human layout.

Shared options (where supported):

- `--url <url>`: Gateway WebSocket URL.

- `--token <token>`: Gateway token.

- `--password <password>`: Gateway password.

- `--timeout <ms>`: timeout/budget (varies per command).

- `--expect-final`: wait for a “final” response (agent calls).

Note: when you set `--url`, the CLI does not fall back to config or environment credentials.
Pass `--token` or `--password` explicitly. Missing explicit credentials is an error.
​`gateway health`
Copy```
openclaw gateway health --url ws://127.0.0.1:18789

```

​`gateway status`
`gateway status` shows the Gateway service (launchd/systemd/schtasks) plus an optional RPC probe.
Copy```
openclaw gateway status
openclaw gateway status --json

```

Options:

- `--url <url>`: override the probe URL.

- `--token <token>`: token auth for the probe.

- `--password <password>`: password auth for the probe.

- `--timeout <ms>`: probe timeout (default `10000`).

- `--no-probe`: skip the RPC probe (service-only view).

- `--deep`: scan system-level services too.

​`gateway probe`
`gateway probe` is the “debug everything” command. It always probes:

- your configured remote gateway (if set), and

- localhost (loopback) **even if remote is configured**.

If multiple gateways are reachable, it prints all of them. Multiple gateways are supported when you use isolated profiles/ports (e.g., a rescue bot), but most installs still run a single gateway.
Copy```
openclaw gateway probe
openclaw gateway probe --json

```

​Remote over SSH (Mac app parity)
The macOS app “Remote over SSH” mode uses a local port-forward so the remote gateway (which may be bound to loopback only) becomes reachable at `ws://127.0.0.1:<port>`.
CLI equivalent:
Copy```
openclaw gateway probe --ssh user@gateway-host

```

Options:

- `--ssh <target>`: `user@host` or `user@host:port` (port defaults to `22`).

- `--ssh-identity <path>`: identity file.

- `--ssh-auto`: pick the first discovered gateway host as SSH target (LAN/WAB only).

Config (optional, used as defaults):

- `gateway.remote.sshTarget`

- `gateway.remote.sshIdentity`

​`gateway call <method>`
Low-level RPC helper.
Copy```
openclaw gateway call status
openclaw gateway call logs.tail --params &#x27;{"sinceMs": 60000}&#x27;

```

​Manage the Gateway service
Copy```
openclaw gateway install
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
openclaw gateway uninstall

```

Notes:

- `gateway install` supports `--port`, `--runtime`, `--token`, `--force`, `--json`.

- Lifecycle commands accept `--json` for scripting.

​Discover gateways (Bonjour)
`gateway discover` scans for Gateway beacons (`_openclaw-gw._tcp`).

- Multicast DNS-SD: `local.`

- Unicast DNS-SD (Wide-Area Bonjour): choose a domain (example: `openclaw.internal.`) and set up split DNS + a DNS server; see [/gateway/bonjour](/gateway/bonjour)

Only gateways with Bonjour discovery enabled (default) advertise the beacon.
Wide-Area discovery records include (TXT):

- `role` (gateway role hint)

- `transport` (transport hint, e.g. `gateway`)

- `gatewayPort` (WebSocket port, usually `18789`)

- `sshPort` (SSH port; defaults to `22` if not present)

- `tailnetDns` (MagicDNS hostname, when available)

- `gatewayTls` / `gatewayTlsSha256` (TLS enabled + cert fingerprint)

- `cliPath` (optional hint for remote installs)

​`gateway discover`
Copy```
openclaw gateway discover

```

Options:

- `--timeout <ms>`: per-command timeout (browse/resolve); default `2000`.

- `--json`: machine-readable output (also disables styling/spinner).

Examples:
Copy```
openclaw gateway discover --timeout 4000
openclaw gateway discover --json | jq &#x27;.beacons[].wsUrl&#x27;

```

doctorhealth⌘I