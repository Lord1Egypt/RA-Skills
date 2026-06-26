# nodes

Source: https://docs.openclaw.ai/cli/nodes

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationCLI commandsnodesGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpCLI commands
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
- [openclaw nodes](#openclaw-nodes)
- [Common commands](#common-commands)
- [Invoke / run](#invoke-%2F-run)
- [Exec-style defaults](#exec-style-defaults)

​`openclaw nodes`
Manage paired nodes (devices) and invoke node capabilities.
Related:

- Nodes overview: [Nodes](/nodes)

- Camera: [Camera nodes](/nodes/camera)

- Images: [Image nodes](/nodes/images)

Common options:

- `--url`, `--token`, `--timeout`, `--json`

​Common commands
Copy```
openclaw nodes list
openclaw nodes list --connected
openclaw nodes list --last-connected 24h
openclaw nodes pending
openclaw nodes approve <requestId>
openclaw nodes status
openclaw nodes status --connected
openclaw nodes status --last-connected 24h

```

`nodes list` prints pending/paired tables. Paired rows include the most recent connect age (Last Connect).
Use `--connected` to only show currently-connected nodes. Use `--last-connected <duration>` to
filter to nodes that connected within a duration (e.g. `24h`, `7d`).
​Invoke / run
Copy```
openclaw nodes invoke --node <id|name|ip> --command <command> --params <json>
openclaw nodes run --node <id|name|ip> <command...>
openclaw nodes run --raw "git status"
openclaw nodes run --agent main --node <id|name|ip> --raw "git status"

```

Invoke flags:

- `--params <json>`: JSON object string (default `{}`).

- `--invoke-timeout <ms>`: node invoke timeout (default `15000`).

- `--idempotency-key <key>`: optional idempotency key.

​Exec-style defaults
`nodes run` mirrors the model’s exec behavior (defaults + approvals):

- Reads `tools.exec.*` (plus `agents.list[].tools.exec.*` overrides).

- Uses exec approvals (`exec.approval.request`) before invoking `system.run`.

- `--node` can be omitted when `tools.exec.node` is set.

- Requires a node that advertises `system.run` (macOS companion app or headless node host).

Flags:

- `--cwd <path>`: working directory.

- `--env <key=val>`: env override (repeatable). Note: node hosts ignore `PATH` overrides (and `tools.exec.pathPrepend` is not applied to node hosts).

- `--command-timeout <ms>`: command timeout.

- `--invoke-timeout <ms>`: node invoke timeout (default `30000`).

- `--needs-screen-recording`: require screen recording permission.

- `--raw <command>`: run a shell string (`/bin/sh -lc` or `cmd.exe /c`).

- `--agent <id>`: agent-scoped approvals/allowlists (defaults to configured agent).

- `--ask <off|on-miss|always>`, `--security <deny|allowlist|full>`: overrides.

modelsonboard⌘I