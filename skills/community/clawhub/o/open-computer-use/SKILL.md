---
name: open-computer-use
description: Guidance for installing, configuring, and operating Open Computer Use, an open-source Computer Use MCP service for macOS, Linux, and Windows.
---

# Open Computer Use

## Overview

Open Computer Use is an open-source Computer Use service exposed through MCP. It lets compatible AI agents operate local desktop apps on macOS, Linux, and Windows through tools such as `list_apps`, `get_app_state`, `click`, `type_text`, `press_key`, `scroll`, `drag`, and `set_value`.

Use this skill when a user wants to install, configure, verify, troubleshoot, or operate Open Computer Use from an agent runtime such as Codex, Claude Code, Gemini CLI, opencode, or another MCP client.

## Install

Install the CLI:

```sh
npm i -g open-computer-use
```

On macOS, run it once and grant Accessibility and Screen Recording permissions:

```sh
open-computer-use
```

Windows and Linux do not require the macOS permission step.

## MCP Setup

Install into Codex:

```sh
open-computer-use install-codex-mcp
```

Or configure any MCP client manually:

```json
{
  "mcpServers": {
    "open-computer-use": {
      "command": "open-computer-use",
      "args": ["mcp"]
    }
  }
}
```

## Other Agent Integrations

Open Computer Use also includes installer commands for common agent runtimes:

```sh
open-computer-use install-codex-plugin
open-computer-use install-claude-mcp
open-computer-use install-gemini-mcp
open-computer-use install-opencode-mcp
```

## Direct CLI Calls

Use the CLI to call one tool:

```sh
open-computer-use call list_apps
open-computer-use call get_app_state --args '{"app":"TextEdit"}'
```

Run a sequence in one process so element indexes can be reused:

```sh
open-computer-use call --calls '[{"tool":"get_app_state","args":{"app":"TextEdit"}},{"tool":"press_key","args":{"app":"TextEdit","key":"Return"}}]'
```

Check setup and permissions:

```sh
open-computer-use doctor
```

## Operating Rules

- Treat Computer Use as control over the user's real desktop session.
- Ask before actions that send messages, submit forms, delete data, install software, change system settings, make purchases, or expose sensitive local information.
- Prefer accessibility element indexes from `get_app_state` over coordinate clicks when available.
- Re-read app state after important actions before continuing.
- On macOS, if tools fail due to permissions, ask the user to grant Accessibility and Screen Recording for the Open Computer Use app or runtime process.

## Project Links

- Repository: https://github.com/iFurySt/open-codex-computer-use
- npm package: https://www.npmjs.com/package/open-computer-use
