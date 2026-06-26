# Zalo Personal Plugin

Source: https://docs.openclaw.ai/plugins/zalouser

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationExtensionsZalo Personal PluginGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
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
- [Zalo Personal (plugin)](#zalo-personal-plugin)
- [Naming](#naming)
- [Where it runs](#where-it-runs)
- [Install](#install)
- [Option A: install from npm](#option-a-install-from-npm)
- [Option B: install from a local folder (dev)](#option-b-install-from-a-local-folder-dev)
- [Prerequisite: zca-cli](#prerequisite-zca-cli)
- [Config](#config)
- [CLI](#cli)
- [Agent tool](#agent-tool)

​Zalo Personal (plugin)
Zalo Personal support for OpenClaw via a plugin, using `zca-cli` to automate a normal Zalo user account.

**Warning:** Unofficial automation may lead to account suspension/ban. Use at your own risk.

​Naming
Channel id is `zalouser` to make it explicit this automates a **personal Zalo user account** (unofficial). We keep `zalo` reserved for a potential future official Zalo API integration.
​Where it runs
This plugin runs **inside the Gateway process**.
If you use a remote Gateway, install/configure it on the **machine running the Gateway**, then restart the Gateway.
​Install
​Option A: install from npm
Copy```
openclaw plugins install @openclaw/zalouser

```

Restart the Gateway afterwards.
​Option B: install from a local folder (dev)
Copy```
openclaw plugins install ./extensions/zalouser
cd ./extensions/zalouser && pnpm install

```

Restart the Gateway afterwards.
​Prerequisite: zca-cli
The Gateway machine must have `zca` on `PATH`:
Copy```
zca --version

```

​Config
Channel config lives under `channels.zalouser` (not `plugins.entries.*`):
Copy```
{
  channels: {
    zalouser: {
      enabled: true,
      dmPolicy: "pairing",
    },
  },
}

```

​CLI
Copy```
openclaw channels login --channel zalouser
openclaw channels logout --channel zalouser
openclaw channels status --probe
openclaw message send --channel zalouser --target <threadId> --message "Hello from OpenClaw"
openclaw directory peers list --channel zalouser --query "name"

```

​Agent tool
Tool name: `zalouser`
Actions: `send`, `image`, `link`, `friends`, `groups`, `me`, `status`Voice Call PluginHooks⌘I