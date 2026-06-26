# pairing

Source: https://docs.openclaw.ai/cli/pairing

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationCLI commandspairingGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpCLI commands
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
- [openclaw pairing](#openclaw-pairing)
- [Commands](#commands)

​`openclaw pairing`
Approve or inspect DM pairing requests (for channels that support pairing).
Related:

- Pairing flow: [Pairing](/channels/pairing)

​Commands
Copy```
openclaw pairing list whatsapp
openclaw pairing approve whatsapp <code> --notify

```

onboardplugins⌘I