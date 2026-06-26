# approvals

Source: https://docs.openclaw.ai/cli/approvals

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationCLI commandsapprovalsGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpCLI commands
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
- [openclaw approvals](#openclaw-approvals)
- [Common commands](#common-commands)
- [Replace approvals from a file](#replace-approvals-from-a-file)
- [Allowlist helpers](#allowlist-helpers)
- [Notes](#notes)

​`openclaw approvals`
Manage exec approvals for the **local host**, **gateway host**, or a **node host**.
By default, commands target the local approvals file on disk. Use `--gateway` to target the gateway, or `--node` to target a specific node.
Related:

- Exec approvals: [Exec approvals](/tools/exec-approvals)

- Nodes: [Nodes](/nodes)

​Common commands
Copy```
openclaw approvals get
openclaw approvals get --node <id|name|ip>
openclaw approvals get --gateway

```

​Replace approvals from a file
Copy```
openclaw approvals set --file ./exec-approvals.json
openclaw approvals set --node <id|name|ip> --file ./exec-approvals.json
openclaw approvals set --gateway --file ./exec-approvals.json

```

​Allowlist helpers
Copy```
openclaw approvals allowlist add "~/Projects/**/bin/rg"
openclaw approvals allowlist add --agent main --node <id|name|ip> "/usr/bin/uptime"
openclaw approvals allowlist add --agent "*" "/usr/bin/uname"

openclaw approvals allowlist remove "~/Projects/**/bin/rg"

```

​Notes

- `--node` uses the same resolver as `openclaw nodes` (id, name, ip, or id prefix).

- `--agent` defaults to `"*"`, which applies to all agents.

- The node host must advertise `system.execApprovals.get/set` (macOS app or headless node host).

- Approvals files are stored per host at `~/.openclaw/exec-approvals.json`.

agentsbrowser⌘I