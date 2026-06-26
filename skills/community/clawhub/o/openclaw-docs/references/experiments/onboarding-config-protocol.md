# Onboarding and Config Protocol

Source: https://docs.openclaw.ai/experiments/onboarding-config-protocol

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationExperimentsOnboarding and Config ProtocolGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpCLI commands
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
- [Onboarding + Config Protocol](#onboarding-%2B-config-protocol)
- [Components](#components)
- [Gateway RPC](#gateway-rpc)
- [UI Hints](#ui-hints)
- [Notes](#notes)

​Onboarding + Config Protocol
Purpose: shared onboarding + config surfaces across CLI, macOS app, and Web UI.
​Components

- Wizard engine (shared session + prompts + onboarding state).

- CLI onboarding uses the same wizard flow as the UI clients.

- Gateway RPC exposes wizard + config schema endpoints.

- macOS onboarding uses the wizard step model.

- Web UI renders config forms from JSON Schema + UI hints.

​Gateway RPC

- `wizard.start` params: `{ mode?: "local"|"remote", workspace?: string }`

- `wizard.next` params: `{ sessionId, answer?: { stepId, value? } }`

- `wizard.cancel` params: `{ sessionId }`

- `wizard.status` params: `{ sessionId }`

- `config.schema` params: `{}`

Responses (shape)

- Wizard: `{ sessionId, done, step?, status?, error? }`

- Config schema: `{ schema, uiHints, version, generatedAt }`

​UI Hints

- `uiHints` keyed by path; optional metadata (label/help/group/order/advanced/sensitive/placeholder).

- Sensitive fields render as password inputs; no redaction layer.

- Unsupported schema nodes fall back to the raw JSON editor.

​Notes

- This doc is the single place to track protocol refactors for onboarding/config.

TestsCron Add Hardening⌘I