# plugins

Source: https://docs.openclaw.ai/cli/plugins

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationCLI commandspluginsGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpCLI commands
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
- [openclaw plugins](#openclaw-plugins)
- [Commands](#commands)
- [Install](#install)
- [Uninstall](#uninstall)
- [Update](#update)

​`openclaw plugins`
Manage Gateway plugins/extensions (loaded in-process).
Related:

- Plugin system: [Plugins](/tools/plugin)

- Plugin manifest + schema: [Plugin manifest](/plugins/manifest)

- Security hardening: [Security](/gateway/security)

​Commands
Copy```
openclaw plugins list
openclaw plugins info <id>
openclaw plugins enable <id>
openclaw plugins disable <id>
openclaw plugins uninstall <id>
openclaw plugins doctor
openclaw plugins update <id>
openclaw plugins update --all

```

Bundled plugins ship with OpenClaw but start disabled. Use `plugins enable` to
activate them.
All plugins must ship a `openclaw.plugin.json` file with an inline JSON Schema
(`configSchema`, even if empty). Missing/invalid manifests or schemas prevent
the plugin from loading and fail config validation.
​Install
Copy```
openclaw plugins install <path-or-spec>

```

Security note: treat plugin installs like running code. Prefer pinned versions.
Npm specs are **registry-only** (package name + optional version/tag). Git/URL/file
specs are rejected. Dependency installs run with `--ignore-scripts` for safety.
Supported archives: `.zip`, `.tgz`, `.tar.gz`, `.tar`.
Use `--link` to avoid copying a local directory (adds to `plugins.load.paths`):
Copy```
openclaw plugins install -l ./my-plugin

```

​Uninstall
Copy```
openclaw plugins uninstall <id>
openclaw plugins uninstall <id> --dry-run
openclaw plugins uninstall <id> --keep-files

```

`uninstall` removes plugin records from `plugins.entries`, `plugins.installs`,
the plugin allowlist, and linked `plugins.load.paths` entries when applicable.
For active memory plugins, the memory slot resets to `memory-core`.
By default, uninstall also removes the plugin install directory under the active
state dir extensions root (`$OPENCLAW_STATE_DIR/extensions/<id>`). Use
`--keep-files` to keep files on disk.
`--keep-config` is supported as a deprecated alias for `--keep-files`.
​Update
Copy```
openclaw plugins update <id>
openclaw plugins update --all
openclaw plugins update <id> --dry-run

```

Updates only apply to plugins installed from npm (tracked in `plugins.installs`).pairingreset⌘I