# Model Config Exploration

Source: https://docs.openclaw.ai/experiments/proposals/model-config

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationExperimentsModel Config ExplorationGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpCLI commands
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
- [Model Config (Exploration)](#model-config-exploration)
- [Motivation](#motivation)
- [Possible direction (high level)](#possible-direction-high-level)
- [Open questions](#open-questions)

​Model Config (Exploration)
This document captures **ideas** for future model configuration. It is not a
shipping spec. For current behavior, see:

- [Models](/concepts/models)

- [Model failover](/concepts/model-failover)

- [OAuth + profiles](/concepts/oauth)

​Motivation
Operators want:

- Multiple auth profiles per provider (personal vs work).

- Simple `/model` selection with predictable fallbacks.

- Clear separation between text models and image-capable models.

​Possible direction (high level)

- Keep model selection simple: `provider/model` with optional aliases.

- Let providers have multiple auth profiles, with an explicit order.

- Use a global fallback list so all sessions fail over consistently.

- Only override image routing when explicitly configured.

​Open questions

- Should profile rotation be per-provider or per-model?

- How should the UI surface profile selection for a session?

- What is the safest migration path from legacy config keys?

Workspace Memory Research⌘I