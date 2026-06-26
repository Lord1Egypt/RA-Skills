# TOOLS.md Template

Source: https://docs.openclaw.ai/reference/templates/TOOLS

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationTemplatesTOOLS.md TemplateGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpCLI commands
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
- [TOOLS.md - Local Notes](#tools-md-local-notes)
- [What Goes Here](#what-goes-here)
- [Examples](#examples)
- [Why Separate?](#why-separate)

​TOOLS.md - Local Notes
Skills define *how* tools work. This file is for *your* specifics — the stuff that’s unique to your setup.
​What Goes Here
Things like:

- Camera names and locations

- SSH hosts and aliases

- Preferred voices for TTS

- Speaker/room names

- Device nicknames

- Anything environment-specific

​Examples
Copy```
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod

```

​Why Separate?
Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

Add whatever helps you do your job. This is your cheat sheet.SOUL.md TemplateUSER⌘I