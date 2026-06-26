# directory

Source: https://docs.openclaw.ai/cli/directory

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationCLI commandsdirectoryGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpCLI commands
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
- [openclaw directory](#openclaw-directory)
- [Common flags](#common-flags)
- [Notes](#notes)
- [Using results with message send](#using-results-with-message-send)
- [ID formats (by channel)](#id-formats-by-channel)
- [Self (“me”)](#self-%E2%80%9Cme%E2%80%9D)
- [Peers (contacts/users)](#peers-contacts%2Fusers)
- [Groups](#groups)

​`openclaw directory`
Directory lookups for channels that support it (contacts/peers, groups, and “me”).
​Common flags

- `--channel <name>`: channel id/alias (required when multiple channels are configured; auto when only one is configured)

- `--account <id>`: account id (default: channel default)

- `--json`: output JSON

​Notes

- `directory` is meant to help you find IDs you can paste into other commands (especially `openclaw message send --target ...`).

- For many channels, results are config-backed (allowlists / configured groups) rather than a live provider directory.

- Default output is `id` (and sometimes `name`) separated by a tab; use `--json` for scripting.

​Using results with `message send`
Copy```
openclaw directory peers list --channel slack --query "U0"
openclaw message send --channel slack --target user:U012ABCDEF --message "hello"

```

​ID formats (by channel)

- WhatsApp: `+15551234567` (DM), `1234567890-1234567890@g.us` (group)

- Telegram: `@username` or numeric chat id; groups are numeric ids

- Slack: `user:U…` and `channel:C…`

- Discord: `user:<id>` and `channel:<id>`

- Matrix (plugin): `user:@user:server`, `room:!roomId:server`, or `#alias:server`

- Microsoft Teams (plugin): `user:<id>` and `conversation:<id>`

- Zalo (plugin): user id (Bot API)

- Zalo Personal / `zalouser` (plugin): thread id (DM/group) from `zca` (`me`, `friend list`, `group list`)

​Self (“me”)
Copy```
openclaw directory self --channel zalouser

```

​Peers (contacts/users)
Copy```
openclaw directory peers list --channel zalouser
openclaw directory peers list --channel zalouser --query "name"
openclaw directory peers list --channel zalouser --limit 50

```

​Groups
Copy```
openclaw directory groups list --channel zalouser
openclaw directory groups list --channel zalouser --query "work"
openclaw directory groups members --channel zalouser --group-id <id>

```

dashboarddns⌘I