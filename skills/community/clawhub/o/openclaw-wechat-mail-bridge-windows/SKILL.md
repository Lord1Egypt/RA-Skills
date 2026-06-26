---
name: openclaw-wechat-mail-bridge-windows
description: Install, configure, run, and troubleshoot a Windows WeChat desktop automation and BHMailer/OpenClaw mail bridge bundle, including File Transfer Assistant workflows, plugin config, sidecar setup, and operations.
homepage: https://github.com/YJLi-new/OPENCLAW-SKILLS/tree/main/wechat-mail-bridge-skill/clawhub-openclaw-wechat-mail-bridge-windows
metadata: {"openclaw":{"emoji":"💬📨","homepage":"https://github.com/YJLi-new/OPENCLAW-SKILLS/tree/main/wechat-mail-bridge-skill/clawhub-openclaw-wechat-mail-bridge-windows"}}
---

# OpenClaw WeChat Mail Bridge (Windows)

Use this skill when the user wants to install, configure, run, package, or troubleshoot a Windows WeChat desktop automation bridge that connects OpenClaw, BHMailer-backed mail queries, File Transfer Assistant testing, and the Windows sidecar runtime.

## Read these files first

- First-time setup: `{baseDir}/references/install-windows.md`
- Plugin config reference: `{baseDir}/references/config.md`
- Sidecar config reference: `{baseDir}/references/sidecar-config.md`
- Runtime and operational checks: `{baseDir}/references/operations.md`
- Release notes: `{baseDir}/references/release-notes.md`

## User-facing resources in this bundle

- Config templates: `{baseDir}/config/`
- Windows helper scripts: `{baseDir}/scripts/`
- Shipped plugin release tree: `{baseDir}/bundle/plugin/`
- Shipped Windows sidecar release tree: `{baseDir}/bundle/windows-sidecar/`

## Working rules

- Start from the files inside this bundle instead of assuming host-specific paths.
- Keep secrets in local config or environment variables, never in the skill files.
- Treat WeChat desktop automation as Windows-local and the plugin control plane as OpenClaw-side.
- Prefer the top-level `scripts/*.bat` entry points for local Windows setup.
- If the user asks for deeper implementation detail, inspect the shipped source under `bundle/`.

## Search keywords and operator intents

- OpenClaw WeChat mail bridge
- Windows WeChat desktop automation
- BHMailer mail query bridge
- File Transfer Assistant testing
- Windows sidecar setup and troubleshooting
- Plugin config, startup, health probe, and sidecar EXE build
- WeChat mail commands such as `/mail`, `/watch`, `/mail-health`, `/mail-bind`, `/mail-pause`, and `/mail-resume`
