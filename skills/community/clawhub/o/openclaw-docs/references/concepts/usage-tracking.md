# Usage Tracking

Source: https://docs.openclaw.ai/concepts/usage-tracking

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationConcept internalsUsage TrackingGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpCLI commands
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
- [Usage tracking](#usage-tracking)
- [What it is](#what-it-is)
- [Where it shows up](#where-it-shows-up)
- [Providers + credentials](#providers-%2B-credentials)

​Usage tracking
​What it is

- Pulls provider usage/quota directly from their usage endpoints.

- No estimated costs; only the provider-reported windows.

​Where it shows up

- `/status` in chats: emoji‑rich status card with session tokens + estimated cost (API key only). Provider usage shows for the **current model provider** when available.

- `/usage off|tokens|full` in chats: per-response usage footer (OAuth shows tokens only).

- `/usage cost` in chats: local cost summary aggregated from OpenClaw session logs.

- CLI: `openclaw status --usage` prints a full per-provider breakdown.

- CLI: `openclaw channels list` prints the same usage snapshot alongside provider config (use `--no-usage` to skip).

- macOS menu bar: “Usage” section under Context (only if available).

​Providers + credentials

- **Anthropic (Claude)**: OAuth tokens in auth profiles.

- **GitHub Copilot**: OAuth tokens in auth profiles.

- **Gemini CLI**: OAuth tokens in auth profiles.

- **Antigravity**: OAuth tokens in auth profiles.

- **OpenAI Codex**: OAuth tokens in auth profiles (accountId used when present).

- **MiniMax**: API key (coding plan key; `MINIMAX_CODE_PLAN_KEY` or `MINIMAX_API_KEY`); uses the 5‑hour coding plan window.

- **z.ai**: API key via env/config/auth store.

Usage is hidden if no matching OAuth/API credentials exist.Typing IndicatorsTimezones⌘I