# apply_patch Tool

Source: https://docs.openclaw.ai/tools/apply-patch

[Skip to main content](#content-area)OpenClaw home pageEnglishSearch...⌘KSearch...NavigationBuilt-in toolsapply_patch ToolGet startedInstallChannelsAgentsToolsModelsPlatformsGateway & OpsReferenceHelpOverview
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
- [apply_patch tool](#apply_patch-tool)
- [Parameters](#parameters)
- [Notes](#notes)
- [Example](#example)

​apply_patch tool
Apply file changes using a structured patch format. This is ideal for multi-file
or multi-hunk edits where a single `edit` call would be brittle.
The tool accepts a single `input` string that wraps one or more file operations:
Copy```
*** Begin Patch
*** Add File: path/to/file.txt
+line 1
+line 2
*** Update File: src/app.ts
@@
-old line
+new line
*** Delete File: obsolete.txt
*** End Patch

```

​Parameters

- `input` (required): Full patch contents including `*** Begin Patch` and `*** End Patch`.

​Notes

- Patch paths support relative paths (from the workspace directory) and absolute paths.

- `tools.exec.applyPatch.workspaceOnly` defaults to `true` (workspace-contained). Set it to `false` only if you intentionally want `apply_patch` to write/delete outside the workspace directory.

- Use `*** Move to:` within an `*** Update File:` hunk to rename files.

- `*** End of File` marks an EOF-only insert when needed.

- Experimental and disabled by default. Enable with `tools.exec.applyPatch.enabled`.

- OpenAI-only (including OpenAI Codex). Optionally gate by model via
`tools.exec.applyPatch.allowModels`.

- Config is only under `tools.exec`.

​Example
Copy```
{
  "tool": "apply_patch",
  "input": "*** Begin Patch\n*** Update File: src/index.ts\n@@\n-const foo = 1\n+const foo = 2\n*** End Patch"
}

```

Web ToolsElevated Mode⌘I