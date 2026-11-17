---
name: openclaw-memoria
version: 3.35.0
description: Local-first, multi-agent persistent memory for AI assistants. Use it to install, operate, connect, diagnose, or update Memoria on macOS.
license: Apache-2.0
homepage: https://github.com/Primo-Studio/openclaw-memoria
repository: https://github.com/Primo-Studio/openclaw-memoria
---

# Memoria

Memoria keeps persistent, local memory for AI assistants. It provides a local daemon, a web UI, an MCP server, a CLI, and a thin OpenClaw adapter for automatic recall and capture.

## Use this skill when

- Installing or updating Memoria on macOS.
- Connecting an agent to its own persistent memory.
- Inspecting memory health, the local daemon, pairing, import, sharing, or local synchronization.
- Diagnosing why recall or capture is unavailable.

## Install

Memoria is a public beta. It requires Node.js 20+; Node.js 22 LTS is recommended. On macOS, Apple Command Line Tools are also required.

```sh
curl -fsSL https://raw.githubusercontent.com/Primo-Studio/openclaw-memoria/memoria-v1/scripts/install-memoria.sh | sh
```

The installer clones the `memoria-v1` branch, installs dependencies, builds the project, initializes and starts the local daemon, enables login autostart on macOS, and opens the local web UI.

## Everyday operations

```sh
memoria ui       # open the local interface
memoria doctor   # inspect daemon, storage, and provider health
memoria agents   # list connected agents
memoria update   # update the local checkout and restart the service
```

Use the UI's Agents screen to detect, pair, and import agents. For terminal pairing, run `memoria pair <agent-type>` and use the one-time command it returns.

## OpenClaw integration

The OpenClaw adapter is intentionally thin: it calls the Memoria daemon on localhost for recall before a prompt and capture after a turn. It needs a paired instance token. When enabling automatic capture, make sure the OpenClaw plugin entry allows conversation-hook access; the installer/onboarding configures this during connection.

If Memoria is unavailable, agents should continue normally without memory rather than failing the request.

## Privacy and safety

- Data is local by default in Memoria-managed SQLite storage.
- Remote LLM providers are optional; configure one only with the user's approval.
- Do not expose pairing codes, instance tokens, admin tokens, or local UI URLs containing tokens.
- Use the review and sharing controls before making memories available across agents or machines.
- Deleting memories is permanent; confirm the target before running a forget/delete operation.
