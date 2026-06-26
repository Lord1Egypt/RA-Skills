---
name: openclaw-memory-kit
description: Scaffold, sanitize, or share an OpenClaw multi-agent memory system with a reusable workspace, memory-lancedb-pro configuration, role prompts, task-board conventions, and startup scripts. Use when the user wants to package an existing OpenClaw memory setup for teammates, remove private details from a live config, bootstrap a fresh OpenClaw memory workspace, or turn the framework into a distributable skill.
---

# OpenClaw Memory Kit

## Quick Start

- Use `scripts/bootstrap-openclaw-memory.ps1` to generate the sharable workspace, config, env template, and launcher scripts.
- Read [references/architecture.md](references/architecture.md) when you need the conceptual model behind the memory system.
- Read [references/generated-files.md](references/generated-files.md) when you need to explain or customize the generated output.
- Read [references/sanitization.md](references/sanitization.md) when the user wants to verify which private details must never be copied.

## Workflow

1. Default to an isolated target root such as `~/.openclaw-memory-kit` unless the user asks to merge into an existing OpenClaw state directory.
2. Keep the base kit memory-focused. Treat Feishu, Telegram, WeChat, and Memos as optional follow-up integrations instead of required setup.
3. For the current tested OpenClaw build, install `memory-lancedb-pro` together with a matching local `openclaw` package inside the generated state directory. This keeps `openclaw/plugin-sdk` resolvable for the memory plugin on newer releases.
4. Never copy the source user's raw `.env`, live app IDs, channel bindings, private LAN addresses, personal scope names, or filesystem usernames. Use placeholders only.
5. Run the bootstrap script. Use `-Force` only when the user explicitly wants to overwrite an existing kit.
6. If the user wants a human-facing handoff, point them to the package-level `OPENCLAW-MEMORY-KIT.md`.

## Script

Run the generator from PowerShell:

```powershell
& "$PSScriptRoot\scripts\bootstrap-openclaw-memory.ps1" `
  -TargetRoot "$HOME\.openclaw-memory-kit" `
  -PrimaryModel "minimax/M2.5" `
  -GatewayPort 18789
```

Add `-Force` to overwrite generated files. Add `-SkipCorePluginInstall` if the user only wants files and will install plugins later.

## Output Expectations

The bootstrap script should generate:

- `openclaw.json`
- `.env.example` and a placeholder `.env` if one does not already exist
- `package.json` and `package-lock.json` when core memory dependencies are installed
- `start-gateway.ps1` and `start-gateway.cmd`
- `workspace/agents/<role>/` prompt files
- `workspace/shared/` collaboration, memory, and task system documents
- `plugins.load.paths`, `plugins.slots.memory`, and `plugins.entries.memory-lancedb-pro.config` in `openclaw.json`
- memory mirror and task board directories

## Customization Points

- Change the role lineup in the `New-RoleCatalog` function.
- Change provider/model defaults in the `New-OpenClawConfig` function.
- Keep optional channel plugins outside the base scaffold unless the user explicitly asks to prewire them.
- For current OpenClaw builds, treat Feishu as bundled-or-optional depending on the target install. Only add a manual Feishu plugin command when the target build is missing Feishu.
- The current tested memory install path is state-local npm dependencies, not `openclaw plugins install memory-lancedb-pro`, because the plugin still expects local `openclaw/plugin-sdk` resolution.
