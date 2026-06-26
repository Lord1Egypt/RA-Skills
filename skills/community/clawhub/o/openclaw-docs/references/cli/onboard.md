# onboard

Source: https://docs.openclaw.ai/cli/onboard

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationCLI commandsonboardGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpCLI commands
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
- [openclaw onboard](#openclaw-onboard)
- [Related guides](#related-guides)
- [Examples](#examples)
- [Common follow-up commands](#common-follow-up-commands)

​`openclaw onboard`
Interactive onboarding wizard (local or remote Gateway setup).
​Related guides

- CLI onboarding hub: [Onboarding Wizard (CLI)](/start/wizard)

- Onboarding overview: [Onboarding Overview](/start/onboarding-overview)

- CLI onboarding reference: [CLI Onboarding Reference](/start/wizard-cli-reference)

- CLI automation: [CLI Automation](/start/wizard-cli-automation)

- macOS onboarding: [Onboarding (macOS App)](/start/onboarding)

​Examples
Copy```
openclaw onboard
openclaw onboard --flow quickstart
openclaw onboard --flow manual
openclaw onboard --mode remote --remote-url ws://gateway-host:18789

```

Non-interactive custom provider:
Copy```
openclaw onboard --non-interactive \
  --auth-choice custom-api-key \
  --custom-base-url "https://llm.example.com/v1" \
  --custom-model-id "foo-large" \
  --custom-api-key "$CUSTOM_API_KEY" \
  --custom-compatibility openai

```

`--custom-api-key` is optional in non-interactive mode. If omitted, onboarding checks `CUSTOM_API_KEY`.
Non-interactive Z.AI endpoint choices:
Note: `--auth-choice zai-api-key` now auto-detects the best Z.AI endpoint for your key (prefers the general API with `zai/glm-5`).
If you specifically want the GLM Coding Plan endpoints, pick `zai-coding-global` or `zai-coding-cn`.
Copy```
# Promptless endpoint selection
openclaw onboard --non-interactive \
  --auth-choice zai-coding-global \
  --zai-api-key "$ZAI_API_KEY"

# Other Z.AI endpoint choices:
# --auth-choice zai-coding-cn
# --auth-choice zai-global
# --auth-choice zai-cn

```

Flow notes:

- `quickstart`: minimal prompts, auto-generates a gateway token.

- `manual`: full prompts for port/bind/auth (alias of `advanced`).

- Fastest first chat: `openclaw dashboard` (Control UI, no channel setup).

- Custom Provider: connect any OpenAI or Anthropic compatible endpoint,
including hosted providers not listed. Use Unknown to auto-detect.

​Common follow-up commands
Copy```
openclaw configure
openclaw agents add <name>

```

`--json` does not imply non-interactive mode. Use `--non-interactive` for scripts.nodespairing⌘I