# setup

Source: https://docs.openclaw.ai/cli/setup

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationCLI commandssetupGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpCLI commands
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
- [openclaw setup](#openclaw-setup)
- [Examples](#examples)

​`openclaw setup`
Initialize `~/.openclaw/openclaw.json` and the agent workspace.
Related:

- Getting started: [Getting started](/start/getting-started)

- Wizard: [Onboarding](/start/onboarding)

​Examples
Copy```
openclaw setup
openclaw setup --workspace ~/.openclaw/workspace

```

To run the wizard via setup:
Copy```
openclaw setup --wizard

```

sessionsskills⌘I