# RPC Adapters

Source: https://docs.openclaw.ai/reference/rpc

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationRPC and APIRPC AdaptersGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpCLI commands
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
- [RPC adapters](#rpc-adapters)
- [Pattern A: HTTP daemon (signal-cli)](#pattern-a-http-daemon-signal-cli)
- [Pattern B: stdio child process (legacy: imsg)](#pattern-b-stdio-child-process-legacy-imsg)
- [Adapter guidelines](#adapter-guidelines)

​RPC adapters
OpenClaw integrates external CLIs via JSON-RPC. Two patterns are used today.
​Pattern A: HTTP daemon (signal-cli)

- `signal-cli` runs as a daemon with JSON-RPC over HTTP.

- Event stream is SSE (`/api/v1/events`).

- Health probe: `/api/v1/check`.

- OpenClaw owns lifecycle when `channels.signal.autoStart=true`.

See [Signal](/channels/signal) for setup and endpoints.
​Pattern B: stdio child process (legacy: imsg)

**Note:** For new iMessage setups, use [BlueBubbles](/channels/bluebubbles) instead.

- OpenClaw spawns `imsg rpc` as a child process (legacy iMessage integration).

- JSON-RPC is line-delimited over stdin/stdout (one JSON object per line).

- No TCP port, no daemon required.

Core methods used:

- `watch.subscribe` → notifications (`method: "message"`)

- `watch.unsubscribe`

- `send`

- `chats.list` (probe/diagnostics)

See [iMessage](/channels/imessage) for legacy setup and addressing (`chat_id` preferred).
​Adapter guidelines

- Gateway owns the process (start/stop tied to provider lifecycle).

- Keep RPC clients resilient: timeouts, restart on exit.

- Prefer stable IDs (e.g., `chat_id`) over display strings.

voicecallDevice Model Database⌘I