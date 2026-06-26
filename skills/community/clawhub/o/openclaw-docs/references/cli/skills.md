# skills

Source: https://docs.openclaw.ai/cli/skills

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationCLI commandsskillsGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpCLI commands
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
- [openclaw skills](#openclaw-skills)
- [Commands](#commands)

​`openclaw skills`
Inspect skills (bundled + workspace + managed overrides) and see what’s eligible vs missing requirements.
Related:

- Skills system: [Skills](/tools/skills)

- Skills config: [Skills config](/tools/skills-config)

- ClawHub installs: [ClawHub](/tools/clawhub)

​Commands
Copy```
openclaw skills list
openclaw skills list --eligible
openclaw skills info <name>
openclaw skills check

```

setupstatus⌘I