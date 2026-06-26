# system

Source: https://docs.openclaw.ai/cli/system

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationCLI commandssystemGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpCLI commands
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
- [openclaw system](#openclaw-system)
- [Common commands](#common-commands)
- [system event](#system-event)
- [system heartbeat last|enable|disable](#system-heartbeat-last%7Cenable%7Cdisable)
- [system presence](#system-presence)
- [Notes](#notes)

​`openclaw system`
System-level helpers for the Gateway: enqueue system events, control heartbeats,
and view presence.
​Common commands
Copy```
openclaw system event --text "Check for urgent follow-ups" --mode now
openclaw system heartbeat enable
openclaw system heartbeat last
openclaw system presence

```

​`system event`
Enqueue a system event on the **main** session. The next heartbeat will inject
it as a `System:` line in the prompt. Use `--mode now` to trigger the heartbeat
immediately; `next-heartbeat` waits for the next scheduled tick.
Flags:

- `--text <text>`: required system event text.

- `--mode <mode>`: `now` or `next-heartbeat` (default).

- `--json`: machine-readable output.

​`system heartbeat last|enable|disable`
Heartbeat controls:

- `last`: show the last heartbeat event.

- `enable`: turn heartbeats back on (use this if they were disabled).

- `disable`: pause heartbeats.

Flags:

- `--json`: machine-readable output.

​`system presence`
List the current system presence entries the Gateway knows about (nodes,
instances, and similar status lines).
Flags:

- `--json`: machine-readable output.

​Notes

- Requires a running Gateway reachable by your current config (local or remote).

- System events are ephemeral and not persisted across restarts.

statustui⌘I