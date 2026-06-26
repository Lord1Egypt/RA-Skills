# browser

Source: https://docs.openclaw.ai/cli/browser

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationCLI commandsbrowserGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpCLI commands
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
- [openclaw browser](#openclaw-browser)
- [Common flags](#common-flags)
- [Quick start (local)](#quick-start-local)
- [Profiles](#profiles)
- [Tabs](#tabs)
- [Snapshot / screenshot / actions](#snapshot-%2F-screenshot-%2F-actions)
- [Chrome extension relay (attach via toolbar button)](#chrome-extension-relay-attach-via-toolbar-button)
- [Remote browser control (node host proxy)](#remote-browser-control-node-host-proxy)

​`openclaw browser`
Manage OpenClaw’s browser control server and run browser actions (tabs, snapshots, screenshots, navigation, clicks, typing).
Related:

- Browser tool + API: [Browser tool](/tools/browser)

- Chrome extension relay: [Chrome extension](/tools/chrome-extension)

​Common flags

- `--url <gatewayWsUrl>`: Gateway WebSocket URL (defaults to config).

- `--token <token>`: Gateway token (if required).

- `--timeout <ms>`: request timeout (ms).

- `--browser-profile <name>`: choose a browser profile (default from config).

- `--json`: machine-readable output (where supported).

​Quick start (local)
Copy```
openclaw browser --browser-profile chrome tabs
openclaw browser --browser-profile openclaw start
openclaw browser --browser-profile openclaw open https://example.com
openclaw browser --browser-profile openclaw snapshot

```

​Profiles
Profiles are named browser routing configs. In practice:

- `openclaw`: launches/attaches to a dedicated OpenClaw-managed Chrome instance (isolated user data dir).

- `chrome`: controls your existing Chrome tab(s) via the Chrome extension relay.

Copy```
openclaw browser profiles
openclaw browser create-profile --name work --color "#FF5A36"
openclaw browser delete-profile --name work

```

Use a specific profile:
Copy```
openclaw browser --browser-profile work tabs

```

​Tabs
Copy```
openclaw browser tabs
openclaw browser open https://docs.openclaw.ai
openclaw browser focus <targetId>
openclaw browser close <targetId>

```

​Snapshot / screenshot / actions
Snapshot:
Copy```
openclaw browser snapshot

```

Screenshot:
Copy```
openclaw browser screenshot

```

Navigate/click/type (ref-based UI automation):
Copy```
openclaw browser navigate https://example.com
openclaw browser click <ref>
openclaw browser type <ref> "hello"

```

​Chrome extension relay (attach via toolbar button)
This mode lets the agent control an existing Chrome tab that you attach manually (it does not auto-attach).
Install the unpacked extension to a stable path:
Copy```
openclaw browser extension install
openclaw browser extension path

```

Then Chrome → `chrome://extensions` → enable “Developer mode” → “Load unpacked” → select the printed folder.
Full guide: [Chrome extension](/tools/chrome-extension)
​Remote browser control (node host proxy)
If the Gateway runs on a different machine than the browser, run a **node host** on the machine that has Chrome/Brave/Edge/Chromium. The Gateway will proxy browser actions to that node (no separate browser control server required).
Use `gateway.nodes.browser.mode` to control auto-routing and `gateway.nodes.browser.node` to pin a specific node if multiple are connected.
Security + remote setup: [Browser tool](/tools/browser), [Remote access](/gateway/remote), [Tailscale](/gateway/tailscale), [Security](/gateway/security)approvalschannels⌘I