# Telegram Allowlist Hardening

Source: https://docs.openclaw.ai/experiments/plans/group-policy-hardening

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationExperimentsTelegram Allowlist HardeningGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpCLI commands
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
- [Telegram Allowlist Hardening](#telegram-allowlist-hardening)
- [Summary](#summary)
- [What changed](#what-changed)
- [Examples](#examples)
- [Why it matters](#why-it-matters)
- [Related docs](#related-docs)

​Telegram Allowlist Hardening
**Date**: 2026-01-05

**Status**: Complete

**PR**: #216
​Summary
Telegram allowlists now accept `telegram:` and `tg:` prefixes case-insensitively, and tolerate
accidental whitespace. This aligns inbound allowlist checks with outbound send normalization.
​What changed

- Prefixes `telegram:` and `tg:` are treated the same (case-insensitive).

- Allowlist entries are trimmed; empty entries are ignored.

​Examples
All of these are accepted for the same ID:

- `telegram:123456`

- `TG:123456`

- `tg:123456`

​Why it matters
Copy/paste from logs or chat IDs often includes prefixes and whitespace. Normalizing avoids
false negatives when deciding whether to respond in DMs or groups.
​Related docs

- [Group Chats](/channels/groups)

- [Telegram Provider](/channels/telegram)

Cron Add HardeningWorkspace Memory Research⌘I