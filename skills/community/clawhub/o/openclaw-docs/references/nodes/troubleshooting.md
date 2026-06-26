# Node Troubleshooting

Source: https://docs.openclaw.ai/nodes/troubleshooting

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationMedia and devicesNode TroubleshootingGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
Tools
Built-in tools
LobsterLLM TaskExec ToolWeb Toolsapply_patch ToolElevated ModeThinking LevelsReactions
Browser
Browser (OpenClaw-managed)Browser LoginChrome ExtensionBrowser Troubleshooting
Agent coordination
Agent SendSub-AgentsMulti-Agent Sandbox & Tools
Skills
Slash CommandsSkillsSkills ConfigClawHubPlugins
Extensions
Voice Call PluginZalo Personal Plugin
Automation
HooksCron JobsCron vs HeartbeatAutomation TroubleshootingWebhooksGmail PubSubPollsAuth Monitoring
Media and devices
NodesNode TroubleshootingImage and Media SupportAudio and Voice NotesCamera CaptureTalk ModeVoice WakeLocation Command
On this page
- [Node troubleshooting](#node-troubleshooting)
- [Command ladder](#command-ladder)
- [Foreground requirements](#foreground-requirements)
- [Permissions matrix](#permissions-matrix)
- [Pairing versus approvals](#pairing-versus-approvals)
- [Common node error codes](#common-node-error-codes)
- [Fast recovery loop](#fast-recovery-loop)

​Node troubleshooting
Use this page when a node is visible in status but node tools fail.
​Command ladder
Copy```
openclaw status
openclaw gateway status
openclaw logs --follow
openclaw doctor
openclaw channels status --probe

```

Then run node specific checks:
Copy```
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
openclaw approvals get --node <idOrNameOrIp>

```

Healthy signals:

- Node is connected and paired for role `node`.

- `nodes describe` includes the capability you are calling.

- Exec approvals show expected mode/allowlist.

​Foreground requirements
`canvas.*`, `camera.*`, and `screen.*` are foreground only on iOS/Android nodes.
Quick check and fix:
Copy```
openclaw nodes describe --node <idOrNameOrIp>
openclaw nodes canvas snapshot --node <idOrNameOrIp>
openclaw logs --follow

```

If you see `NODE_BACKGROUND_UNAVAILABLE`, bring the node app to the foreground and retry.
​Permissions matrix
CapabilityiOSAndroidmacOS node appTypical failure code`camera.snap`, `camera.clip`Camera (+ mic for clip audio)Camera (+ mic for clip audio)Camera (+ mic for clip audio)`*_PERMISSION_REQUIRED``screen.record`Screen Recording (+ mic optional)Screen capture prompt (+ mic optional)Screen Recording`*_PERMISSION_REQUIRED``location.get`While Using or Always (depends on mode)Foreground/Background location based on modeLocation permission`LOCATION_PERMISSION_REQUIRED``system.run`n/a (node host path)n/a (node host path)Exec approvals required`SYSTEM_RUN_DENIED`
​Pairing versus approvals
These are different gates:

- **Device pairing**: can this node connect to the gateway?

- **Exec approvals**: can this node run a specific shell command?

Quick checks:
Copy```
openclaw devices list
openclaw nodes status
openclaw approvals get --node <idOrNameOrIp>
openclaw approvals allowlist add --node <idOrNameOrIp> "/usr/bin/uname"

```

If pairing is missing, approve the node device first.
If pairing is fine but `system.run` fails, fix exec approvals/allowlist.
​Common node error codes

- `NODE_BACKGROUND_UNAVAILABLE` → app is backgrounded; bring it foreground.

- `CAMERA_DISABLED` → camera toggle disabled in node settings.

- `*_PERMISSION_REQUIRED` → OS permission missing/denied.

- `LOCATION_DISABLED` → location mode is off.

- `LOCATION_PERMISSION_REQUIRED` → requested location mode not granted.

- `LOCATION_BACKGROUND_UNAVAILABLE` → app is backgrounded but only While Using permission exists.

- `SYSTEM_RUN_DENIED: approval required` → exec request needs explicit approval.

- `SYSTEM_RUN_DENIED: allowlist miss` → command blocked by allowlist mode.

​Fast recovery loop
Copy```
openclaw nodes status
openclaw nodes describe --node <idOrNameOrIp>
openclaw approvals get --node <idOrNameOrIp>
openclaw logs --follow

```

If still stuck:

- Re-approve device pairing.

- Re-open node app (foreground).

- Re-grant OS permissions.

- Recreate/adjust exec approval policy.

Related:

- [/nodes/index](/nodes/index)

- [/nodes/camera](/nodes/camera)

- [/nodes/location-command](/nodes/location-command)

- [/tools/exec-approvals](/tools/exec-approvals)

- [/gateway/pairing](/gateway/pairing)

NodesImage and Media Support⌘I