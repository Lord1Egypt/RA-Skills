# memory

Source: https://docs.openclaw.ai/cli/memory

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationCLI commandsmemoryGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpCLI commands
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
- [openclaw memory](#openclaw-memory)
- [Examples](#examples)
- [Options](#options)

​`openclaw memory`
Manage semantic memory indexing and search.
Provided by the active memory plugin (default: `memory-core`; set `plugins.slots.memory = "none"` to disable).
Related:

- Memory concept: [Memory](/concepts/memory)

- Plugins: [Plugins](/tools/plugin)

​Examples
Copy```
openclaw memory status
openclaw memory status --deep
openclaw memory status --deep --index
openclaw memory status --deep --index --verbose
openclaw memory index
openclaw memory index --verbose
openclaw memory search "release checklist"
openclaw memory status --agent main
openclaw memory index --agent main --verbose

```

​Options
Common:

- `--agent <id>`: scope to a single agent (default: all configured agents).

- `--verbose`: emit detailed logs during probes and indexing.

Notes:

- `memory status --deep` probes vector + embedding availability.

- `memory status --deep --index` runs a reindex if the store is dirty.

- `memory index --verbose` prints per-phase details (provider, model, sources, batch activity).

- `memory status` includes any extra paths configured via `memorySearch.extraPaths`.

logsmessage⌘I